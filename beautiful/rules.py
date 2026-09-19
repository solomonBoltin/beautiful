"""
beautiful.rules
---------------
Design rules the DOM can answer *for certain* — the part of a beauty lint that is not taste.
Runs inside the rendered page (render.py) and returns findings the way a code linter would:
rule id, level, count, examples, and the threshold that was crossed.

Every rule carries its source. Thresholds are the ones the platform guidelines and standards
agree on; where they disagree (touch targets: WCAG 24 px minimum, Apple 44 pt, Material 48 dp)
the rule reports against the strictest *floor* (24 px = error) and the platform size (44 px =
warning) separately.

    text-contrast        WCAG 2.2 SC 1.4.3 — text < 4.5:1 (3:1 for large text) against its background
    font-size            Lighthouse "legible font sizes" — text under 12 px; body text under 16 px on mobile
    touch-target         WCAG 2.5.8 (24 px floor), Apple HIG 44 pt, Material 48 dp
    line-length          Dyson 2001 / Shaikh 2005 / Bringhurst / GOV.UK — measure outside 35–100 characters
    line-height          WCAG 1.4.12 / Butterick — body text line-height under 1.2
    image-distortion     an <img> rendered at a different aspect ratio than its natural one
    text-clipped         a text element whose content is wider than its box (cut off, no ellipsis)
    viewport-meta        no <meta name=viewport> — the page lays out at 980 px on phones
    heading-order        WCAG 1.3.1 / a11y — skipped heading levels or no h1
    img-alt              WCAG 1.1.1 — images without alt
    type-noise           Refactoring UI — more than 3 font families or more than 8 distinct font sizes
"""
from __future__ import annotations

RULES_JS = r"""
(vp) => {
  const out = [];
  const add = (rule, level, message, examples, extra) => out.push({rule, level, message, examples: examples.slice(0, 5), count: examples.length, ...(extra||{})});
  const vis = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && cs.opacity !== '0' && r.bottom > 0 && r.top < vp.height * 3; };
  const tag = (el) => { const id = el.id ? '#' + el.id : ''; const cls = el.classList && el.classList.length ? '.' + [...el.classList].slice(0, 2).join('.') : ''; return el.tagName.toLowerCase() + id + cls; };
  const parseRGB = (s) => { const m = s && s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(parseFloat); return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const ratio = (a, b) => { const la = lum(a), lb = lum(b); return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05); };
  const blend = (fg, bg) => ({r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1});
  const bgOf = (el) => {  // walk up to the first opaque background; null if an image/gradient is behind
    let node = el;
    while (node && node !== document.documentElement) {
      const cs = getComputedStyle(node);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return null;
      const c = parseRGB(cs.backgroundColor);
      if (c && c.a > 0) return c.a >= 1 ? c : blend(c, {r: 255, g: 255, b: 255, a: 1});
      node = node.parentElement;
    }
    const root = parseRGB(getComputedStyle(document.documentElement).backgroundColor);
    return (root && root.a > 0) ? root : {r: 255, g: 255, b: 255, a: 1};
  };
  const textNodesOf = (el) => [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim().length > 1);

  // ---- text: contrast, size, line length, line height, clipping ----
  const lowContrast = [], tiny = [], smallBody = [], longLines = [], tightLeading = [], clipped = [];
  const families = new Set(), sizes = new Set();
  let textChars = 0, tinyChars = 0;
  for (const el of document.querySelectorAll('body *')) {
    if (!vis(el)) continue;
    const tn = textNodesOf(el);
    if (!tn.length) continue;
    const cs = getComputedStyle(el);
    const chars = tn.reduce((n, t) => n + t.textContent.trim().length, 0);
    const fs = parseFloat(cs.fontSize);
    families.add(cs.fontFamily.split(',')[0].trim().replace(/["']/g, ''));
    sizes.add(Math.round(fs));
    textChars += chars;
    if (fs < 12) { tinyChars += chars; tiny.push(tag(el) + ' ' + fs.toFixed(0) + 'px'); }
    if (vp.mobile && chars >= 80 && fs < 16 && ['p', 'li', 'td', 'div', 'span'].includes(el.tagName.toLowerCase())) smallBody.push(tag(el) + ' ' + fs.toFixed(0) + 'px');
    const fg = parseRGB(cs.color), bg = bgOf(el);
    if (fg && bg && fg.a > 0) {
      const r = ratio(fg.a < 1 ? blend(fg, bg) : fg, bg);
      const bold = parseInt(cs.fontWeight, 10) >= 700;
      const large = fs >= 24 || (bold && fs >= 18.66);
      if (r < (large ? 3 : 4.5)) lowContrast.push(tag(el) + ' ' + r.toFixed(1) + ':1');
    }
    const rect = el.getBoundingClientRect();
    if (chars >= 120) {
      const cpl = rect.width / (fs * 0.5);
      // screen studies support 45–95 CPL (Dyson & Haselgrove 2001; Shaikh & Chaparro 2005);
      // the guideline sweet spot is 60–75; flag only outside 35–100
      if (cpl > 100 || cpl < 35) longLines.push(tag(el) + ' ~' + Math.round(cpl) + ' chars/line');
      const lh = cs.lineHeight === 'normal' ? 1.2 * fs : parseFloat(cs.lineHeight);
      if (lh / fs < 1.2) tightLeading.push(tag(el) + ' ' + (lh / fs).toFixed(2));
    }
    if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0 && (cs.overflowX === 'hidden' || cs.overflow === 'hidden') && cs.textOverflow !== 'ellipsis' && cs.whiteSpace === 'nowrap')
      clipped.push(tag(el));
  }
  if (lowContrast.length) add('text-contrast', 'error', 'text below WCAG contrast (4.5:1, 3:1 for large text)', lowContrast, {source: 'WCAG 2.2 SC 1.4.3'});
  if (tiny.length) add('font-size', textChars && tinyChars / textChars > 0.4 ? 'error' : 'warning', 'text under 12px', tiny, {share: textChars ? +(tinyChars / textChars).toFixed(2) : 0, source: 'Lighthouse legible font sizes'});
  if (smallBody.length) add('font-size-mobile', 'warning', 'body text under 16px on a phone', smallBody, {source: 'Apple HIG / GOV.UK / Material'});
  if (longLines.length) add('line-length', 'warning', 'measure outside 35–100 characters per line (60–75 is the guideline sweet spot; 45–95 is what screen studies support)', longLines, {source: 'Dyson & Haselgrove 2001; Shaikh & Chaparro 2005; Bringhurst; GOV.UK'});
  if (tightLeading.length) add('line-height', 'warning', 'body text line-height under 1.2', tightLeading, {source: 'WCAG 1.4.12; Butterick'});
  if (clipped.length) add('text-clipped', 'error', 'text cut off by its box (nowrap + overflow hidden, no ellipsis)', clipped, {source: 'beautiful'});
  if (families.size > 3) add('type-noise', 'warning', families.size + ' font families on one page (keep to 1–2)', [...families], {source: 'Refactoring UI'});
  if (sizes.size > 8) add('type-noise', 'warning', sizes.size + ' distinct font sizes on one page (a type scale has 5–8)', [...sizes].sort((a, b) => a - b).map(String), {source: 'Refactoring UI; Material type scale'});

  // ---- touch targets ----
  const tinyT = [], smallT = [];
  for (const el of document.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, [role=button], [role=link], [onclick]')) {
    if (!vis(el)) continue;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    const m = Math.min(r.width, r.height);
    // WCAG 2.5.8 exceptions: inline text links (the target is the text), and native controls
    // the author did not restyle (user-agent sized). Both still get the mobile 44px advice.
    const inlineLink = el.tagName === 'A' && cs.display === 'inline';
    const nativeControl = ['SELECT', 'INPUT', 'TEXTAREA'].includes(el.tagName) && cs.appearance !== 'none';
    if (m < 24 && !inlineLink && !nativeControl) tinyT.push(tag(el) + ' ' + Math.round(r.width) + '×' + Math.round(r.height));
    else if (vp.mobile && m < 44) smallT.push(tag(el) + ' ' + Math.round(r.width) + '×' + Math.round(r.height));
  }
  if (tinyT.length) add('touch-target', 'error', 'interactive element under 24×24px', tinyT, {source: 'WCAG 2.2 SC 2.5.8'});
  if (smallT.length) add('touch-target-mobile', 'warning', 'interactive element under 44×44px on a phone', smallT, {source: 'Apple HIG 44pt; Material 48dp'});

  // ---- images ----
  const distorted = [], noAlt = [];
  for (const img of document.images) {
    if (!vis(img) || !img.naturalWidth || !img.naturalHeight) continue;
    const cs = getComputedStyle(img);
    if (!img.hasAttribute('alt')) noAlt.push(tag(img));
    if (['cover', 'contain', 'scale-down', 'none'].includes(cs.objectFit)) continue;
    const r = img.getBoundingClientRect();
    const nat = img.naturalWidth / img.naturalHeight, ren = r.width / r.height;
    if (r.width > 24 && Math.abs(nat / ren - 1) > 0.05) distorted.push(tag(img) + ' ' + (nat / ren).toFixed(2) + '× stretched');
  }
  if (distorted.length) add('image-distortion', 'error', 'image rendered at a different aspect ratio than its source', distorted, {source: 'beautiful'});
  if (noAlt.length) add('img-alt', 'warning', 'images without alt text', noAlt, {source: 'WCAG 2.2 SC 1.1.1'});

  // ---- document ----
  if (vp.mobile && !document.querySelector('meta[name=viewport]')) add('viewport-meta', 'error', 'no <meta name="viewport">: the page lays out at 980px on phones', ['head'], {source: 'Lighthouse; MDN'});
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis).map(h => +h.tagName[1]);
  if (!hs.includes(1) && document.body.innerText.trim().length > 200) add('heading-order', 'warning', 'no h1 on the page', ['body'], {source: 'WCAG 1.3.1'});
  for (let i = 1; i < hs.length; i++) if (hs[i] > hs[i - 1] + 1) { add('heading-order', 'warning', 'heading level skipped (h' + hs[i - 1] + ' → h' + hs[i] + ')', ['h' + hs[i]], {source: 'WCAG 1.3.1'}); break; }

  return out;
}
"""

PENALTY = {"error": 3}   # per distinct failing rule, capped below; warnings are free
PENALTY_CAP = 12


def run(page, vp: dict) -> list:
    """Evaluate the rules inside a Playwright page. Returns a list of findings."""
    try:
        return page.evaluate(RULES_JS, {"width": vp["width"], "height": vp["height"], "mobile": bool(vp.get("mobile"))})
    except Exception as e:  # a page that throws must not kill the score
        return [{"rule": "rules", "level": "note", "message": f"rules could not run: {type(e).__name__}", "examples": [], "count": 0}]


def apply(report: dict, findings: list, viewport: str) -> None:
    """Attach findings to a beauty report: hints, penalties (errors only), report['rules']."""
    report["rules"] = findings
    errors = [f for f in findings if f["level"] == "error"]
    if errors:
        pen = min(PENALTY_CAP, PENALTY["error"] * len(errors))
        report.setdefault("penalties", {})["rules"] = pen
        report["score"] = max(1, report["score"] - pen)
    for f in sorted(findings, key=lambda f: {"error": 0, "warning": 1, "note": 2}[f["level"]]):
        ex = ", ".join(f["examples"][:2])
        more = f" (+{f['count'] - 2} more)" if f["count"] > 2 else ""
        report["hints"].insert(0 if f["level"] == "error" else len(report["hints"]),
                               f"{f['rule']} [{f['level']}, {viewport}]: {f['message']} — {ex}{more}")
