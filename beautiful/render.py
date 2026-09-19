"""
beautiful.render
----------------
Score HTML and URLs directly: render deterministically at a named viewport, then score the
pixels. The lint then works on *code* — a page, a component story, a dev server — without
anyone taking a screenshot by hand.

    from beautiful.render import score_html
    score_html("index.html")                       # {'desktop': report, 'tablet': report, 'mobile': report}
    score_html("<div>…</div>", viewports=["mobile"], mode="ui")
    score_html("https://example.com", viewports=["desktop"])

Two backends, picked automatically:

  playwright  (exact)  Headless Chromium via Playwright for Python — the same engine that would
                       take the screenshot, so the pixels and the score are identical to a
                       screenshot at the same viewport. No Node needed:
                           pip install "beautiful-score[render]" && playwright install chromium
  weasyprint  (static) A pure-Python CSS layout engine (no browser, no JavaScript). Fine for
                       static HTML/CSS, e-mail templates, docs; fonts and unsupported CSS make
                       its pixels differ from Chromium, so its score is *close*, not identical.
                           pip install "beautiful-score[html]"

Determinism (playwright): fixed viewport, deviceScaleFactor 1, animations and transitions
disabled, reduced-motion, fonts awaited, network idle, and a fixed clock, so the same
HTML + CSS + fonts give the same pixels — and the same score — every run.

Viewports are the ones a designer checks: desktop 1280×800, tablet 768×1024, mobile 375×812
(mobile also sends a touch/mobile user agent so responsive code sees a phone).
"""
from __future__ import annotations

import io
import os
import re
from typing import Iterable

from PIL import Image

from .core import beauty

VIEWPORTS = {
    "desktop": {"width": 1280, "height": 800, "mobile": False},
    "tablet": {"width": 768, "height": 1024, "mobile": False},
    "mobile": {"width": 375, "height": 812, "mobile": True},
}
MOBILE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
             "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
_FREEZE_CSS = "*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}"


def _kind(source: str) -> str:
    s = source.strip()
    if re.match(r"^https?://", s, re.I):
        return "url"
    if s.startswith("<") or "\n" in s:
        return "html"
    if os.path.exists(s):
        return "file"
    raise FileNotFoundError(source)


def backends_available() -> dict:
    out = {}
    try:
        import playwright.sync_api  # noqa: F401
        out["playwright"] = True
    except ImportError:
        out["playwright"] = False
    try:
        import weasyprint  # noqa: F401
        out["weasyprint"] = True
    except Exception:
        out["weasyprint"] = False
    return out


# --------------------------------------------------------------------------- #
# playwright
# --------------------------------------------------------------------------- #
class _Chromium:
    """One headless Chromium for many renders (launching is the slow part)."""

    def __init__(self):
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        self.browser = self._pw.chromium.launch()

    def render(self, source: str, viewport: str, wait_ms: int = 300, full_page: bool = False) -> Image.Image:
        vp = VIEWPORTS[viewport]
        ctx = self.browser.new_context(
            viewport={"width": vp["width"], "height": vp["height"]}, device_scale_factor=1,
            is_mobile=vp["mobile"], has_touch=vp["mobile"],
            user_agent=MOBILE_UA if vp["mobile"] else None,
            reduced_motion="reduce", color_scheme="light", locale="en-US", timezone_id="UTC",
        )
        page = ctx.new_page()
        page.clock.set_fixed_time("2026-01-01T12:00:00Z") if hasattr(page, "clock") else None
        kind = _kind(source)
        try:
            if kind == "url":
                page.goto(source, wait_until="networkidle", timeout=45000)
            elif kind == "file":
                page.goto("file://" + os.path.abspath(source), wait_until="networkidle", timeout=45000)
            else:
                page.set_content(source, wait_until="networkidle")
        except Exception:
            pass  # a slow third-party asset must not block a score; we screenshot what loaded
        try:  # a strict Content-Security-Policy may refuse the inline style; the screenshot call disables animations anyway
            page.add_style_tag(content=_FREEZE_CSS)
        except Exception:
            pass
        try:
            page.evaluate("document.fonts && document.fonts.ready")
        except Exception:
            pass
        page.wait_for_timeout(wait_ms)
        png = page.screenshot(full_page=full_page, animations="disabled", caret="hide")
        self.last_layout = self._layout_facts(page, vp)
        ctx.close()
        return Image.open(io.BytesIO(png)).convert("RGB")

    @staticmethod
    def _layout_facts(page, vp) -> dict:
        """Things the DOM knows for certain and pixels can only suspect: horizontal overflow and
        which elements stick out of the viewport."""
        try:
            return page.evaluate("""(device) => {
                // compare against the *layout* viewport: a page without <meta name=viewport> lays
                // out at 980px on a phone and is zoomed out, which is not overflow
                // documentElement.clientWidth is the layout viewport; innerWidth follows the visual
                // viewport, which mobile Chrome widens when it zooms out to fit overflowing content
                const de = document.documentElement, b = document.body;
                const vw = (de && de.clientWidth) || window.innerWidth || device;
                const sw = Math.max(de ? de.scrollWidth : 0, b ? b.scrollWidth : 0);
                const out = [];
                for (const el of document.querySelectorAll('body *')) {
                    const r = el.getBoundingClientRect();
                    if (r.width < 2 || r.height < 2) continue;
                    if (r.right > vw + 1 || r.left < -1) {
                        const id = el.id ? '#' + el.id : '';
                        const cls = el.classList.length ? '.' + [...el.classList].slice(0, 2).join('.') : '';
                        out.push({el: el.tagName.toLowerCase() + id + cls, left: Math.round(r.left), right: Math.round(r.right)});
                        if (out.length >= 8) break;
                    }
                }
                return {viewport_width: vw, device_width: device, scroll_width: sw, overflow_x: Math.max(0, sw - vw),
                        no_viewport_meta: vw > device + 1, overflowing: out};
            }""", vp["width"])
        except Exception:
            return {}

    def close(self):
        self.browser.close()
        self._pw.stop()


# --------------------------------------------------------------------------- #
# weasyprint (static, no browser)
# --------------------------------------------------------------------------- #
def _render_weasy(source: str, viewport: str) -> Image.Image:
    import weasyprint
    vp = VIEWPORTS[viewport]
    kind = _kind(source)
    kw = {"url": source} if kind == "url" else {"filename": source} if kind == "file" else {"string": source}
    css = weasyprint.CSS(string=f"@page {{ size: {vp['width']}px {vp['height']}px; margin: 0 }} " + _FREEZE_CSS)
    doc = weasyprint.HTML(**kw).render(stylesheets=[css])
    png = doc.write_png(resolution=96) if hasattr(doc, "write_png") else None
    if png is None:  # WeasyPrint ≥ 53 dropped write_png; go through PDF → first page raster if pdf2image exists
        raise RuntimeError("this WeasyPrint has no PNG output; install 'weasyprint<53' or use the playwright backend")
    im = Image.open(io.BytesIO(png)).convert("RGB")
    return im.crop((0, 0, vp["width"], min(im.height, vp["height"])))


# --------------------------------------------------------------------------- #
# public
# --------------------------------------------------------------------------- #
def render(source: str, viewport: str = "desktop", backend: str | None = None, _chromium=None) -> Image.Image:
    """HTML string / file / URL -> RGB image at the named viewport."""
    if viewport not in VIEWPORTS:
        raise ValueError(f"viewport must be one of {list(VIEWPORTS)}")
    avail = backends_available()
    backend = backend or ("playwright" if avail["playwright"] else "weasyprint" if avail["weasyprint"] else None)
    if backend is None:
        raise RuntimeError('no renderer: pip install "beautiful-score[render]" && playwright install chromium '
                           '(exact, headless Chromium) or pip install "beautiful-score[html]" (static, no browser)')
    if backend == "playwright":
        own = _chromium is None
        c = _chromium or _Chromium()
        try:
            return c.render(source, viewport)
        finally:
            if own:
                c.close()
    return _render_weasy(source, viewport)


def score_html(source: str, viewports: Iterable[str] = ("desktop", "tablet", "mobile"), mode: str = "ui",
               backend: str | None = None, save_dir: str | None = None) -> dict:
    """Render at each viewport and score. Returns {viewport: beauty report (+ 'image' path if saved)}."""
    viewports = list(viewports)
    avail = backends_available()
    use = backend or ("playwright" if avail["playwright"] else "weasyprint")
    chromium = _Chromium() if use == "playwright" else None
    out = {}
    try:
        for vp in viewports:
            im = render(source, vp, backend=use, _chromium=chromium)
            r = beauty(im, mode)
            r["viewport"] = vp
            r["backend"] = use
            layout = getattr(chromium, "last_layout", None) or {}
            if layout:
                r["layout"] = layout
                if layout.get("no_viewport_meta") and vp == "mobile":
                    r["hints"].insert(0, f"no <meta name=viewport>: the page lays out at {layout['viewport_width']}px on a phone and is shown zoomed out")
                if layout.get("overflow_x", 0) > 2:
                    who = ", ".join(x["el"] for x in layout.get("overflowing", [])[:3]) or "an element"
                    r["hints"].insert(0, f"overflow: the page is {layout['overflow_x']}px wider than the {vp} viewport "
                                         f"({who} sticks out) — horizontal scroll and clipped content")
                    if "clipping" not in r.get("penalties", {}):
                        r.setdefault("penalties", {})["overflow"] = 10
                        r["score"] = max(1, r["score"] - 10)
            if save_dir:
                os.makedirs(save_dir, exist_ok=True)
                stem = re.sub(r"[^A-Za-z0-9._-]+", "_", os.path.basename(source.strip())[:60]) or "page"
                path = os.path.join(save_dir, f"{stem}@{vp}.png")
                im.save(path)
                r["image"] = path
            out[vp] = r
    finally:
        if chromium:
            chromium.close()
    return out
