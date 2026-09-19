"""Components: every landmark, section and control of a rendered page, cropped and scored on its own.

A page score hides a component that got uglier — a menu button whose icon slid off centre costs the
whole page one point. So each component gets its own measured beauty, keyed by a stable selector,
and a baseline remembers it; the gate fails when a component's score drops.

Scale: the crops are scored with the *classic* formula (the literature one, mode="classic"), not the
fitted `ui` model, which was trained on whole pages. For controls (buttons, tabs, switches) the
composition factor is the mean of horizontal mirror, vertical mirror and balance, because a control
is expected to be symmetric on both axes; for blocks it is the classic max(mirror, balance).
"""
from __future__ import annotations

import io
from typing import Iterable

from PIL import Image

from .core import beauty

SCALE = "classic"
MIN_W, MIN_H = 24, 16
MAX_COMPONENTS = 80

DISCOVER_JS = r"""
(vp) => {
  const out = [], seen = new Map();
  const vis = (el) => {
    const r = el.getBoundingClientRect(), c = getComputedStyle(el);
    if (r.width < %d || r.height < %d || c.display === 'none' || c.visibility === 'hidden' || parseFloat(c.opacity) <= 0.1) return false;
    if (el.checkVisibility) { try { return el.checkVisibility({opacityProperty: true, visibilityProperty: true}); } catch (e) {} }
    return true;
  };
  const keyOf = (el) => {
    let k = el.tagName.toLowerCase();
    if (el.id) return k + '#' + el.id;
    const t = el.getAttribute('data-testid') || el.getAttribute('data-component');
    if (t) return k + '[' + t + ']';
    const hashy = (c) => /\d{3,}/.test(c) || /(?=[a-z0-9]*\d)(?=[a-z0-9]*[a-z])[a-z0-9]{5,}$/i.test(c.split(/[-_]+/).pop());  // css-module / build hashes
    const cls = [...el.classList].filter(c => !/^(is-|has-|js-|active|open|hover|focus)/.test(c) && !hashy(c)).slice(0, 2);
    if (cls.length) k += '.' + cls.join('.');
    else if (el.getAttribute('role')) k += '[role=' + el.getAttribute('role') + ']';
    return k;
  };
  const push = (el, kind) => {
    if (!vis(el)) return;
    const r = el.getBoundingClientRect();
    let k = keyOf(el); const n = seen.get(k) || 0; seen.set(k, n + 1); if (n) k += ':' + n;
    out.push({key: k, kind, x: Math.round(r.left + scrollX), y: Math.round(r.top + scrollY), w: Math.round(r.width), h: Math.round(r.height)});
  };
  document.querySelectorAll('header, nav, section, article, aside, footer, form, main > div[class], [role=region], [role=banner], [role=navigation], [role=contentinfo], [role=dialog], [data-component]').forEach(el => push(el, 'block'));
  document.querySelectorAll('button, [role=button], [role=tab], [role=switch], summary, input[type=submit], a.btn, a.button, a[class*="btn"], a[class*="button"], a[class*="cta"]').forEach(el => {
    if (el.matches('button, [role=button]') || !el.closest('button, [role=button]')) push(el, 'control');
  });
  return out.slice(0, %d);
}
""" % (MIN_W, MIN_H, MAX_COMPONENTS)


def score_crop(im: Image.Image, kind: str) -> dict:
    """Classic beauty of one crop; controls are judged on both-axis symmetry."""
    r = beauty(im, SCALE)
    f = dict(r["factors"])
    sym = r.get("raw", {}).get("symmetry", {})
    if kind == "control" and all(k in sym for k in ("horizontal_mirror", "vertical_mirror", "balance")):
        f["composition"] = round((sym["horizontal_mirror"] + sym["vertical_mirror"] + sym["balance"]) / 3, 4)
    w = r.get("weights") or {}
    total = sum(w.values()) or 1.0
    s = sum(w[k] * f.get(k, 0.0) for k in w) / total
    hints = list(r.get("hints", []))[:2]
    if kind == "control" and f["composition"] < 0.7:
        hints.insert(0, "control is not symmetric on both axes: centre the icon or label, equalise the padding")
    return {"score": max(1, min(100, round(100 * s))), "factors": {k: round(v, 3) for k, v in f.items()}, "hints": hints}


def capture(page, vp: dict, screenshot: bytes | None = None) -> list:
    """Discover components in a Playwright page, crop them from one full-page screenshot, score each.
    Returns [{key, kind, rect, score, factors, hints}] in document order."""
    try:
        found = page.evaluate(DISCOVER_JS, vp)
    except Exception:
        return []
    if not found:
        return []
    try:
        png = screenshot or page.screenshot(full_page=True, animations="disabled", caret="hide")
    except Exception:
        return []
    full = Image.open(io.BytesIO(png)).convert("RGB")
    out = []
    for c in found:
        x0, y0 = max(0, c["x"]), max(0, c["y"])
        x1, y1 = min(full.width, c["x"] + c["w"]), min(full.height, c["y"] + c["h"])
        if x1 - x0 < MIN_W or y1 - y0 < MIN_H:
            continue
        crop = full.crop((x0, y0, x1, y1))
        try:
            r = score_crop(crop, c["kind"])
        except Exception:
            continue
        out.append({"key": c["key"], "kind": c["kind"], "rect": [x0, y0, x1 - x0, y1 - y0], "scale": SCALE, **r})
    return out


def baseline_entry(components: Iterable[dict]) -> dict:
    """What a baseline keeps per page: {component key: score}."""
    return {c["key"]: c["score"] for c in components}


def regressions(old: dict, new: Iterable[dict], tolerance: int) -> list:
    """Component keys whose score fell past the tolerance, as (key, old, new)."""
    out = []
    for c in new:
        if c["key"] in old and c["score"] < old[c["key"]] - tolerance:
            out.append((c["key"], old[c["key"]], c["score"]))
    return out
