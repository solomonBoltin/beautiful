"""
beautiful.rules
---------------
Design rules the DOM can answer *for certain* — the part of a beauty lint that is not taste.
Runs inside the rendered page (render.py) and returns findings the way a code linter would:
rule id, level, message, count, examples, and — from RULES — the source, why, and fix.

Every threshold is the one the guidelines and the measurements agree on (see
research/DESIGN-LINTS.md). Where they disagree (touch targets: WCAG 24 px floor, Apple 44 pt,
Material 48 dp) the strictest floor is an error and the platform figure a warning.

Levels: error = a defect nobody defends (costs points); warning = a rule most guidelines share
(free); note = a tell or a taste signal (free, never a penalty).
"""
from __future__ import annotations

RULES = {
    "text-contrast": dict(level="error", source="WCAG 2.2 SC 1.4.3", why="text under 4.5:1 (3:1 large) is unreadable for low-vision and in glare; the single most common failure on the web (WebAIM: 79 % of pages)", fix="darken the text or lighten the background until the ratio passes; check placeholders and disabled states too"),
    "font-size": dict(level="warning", source="Lighthouse legible font sizes; Google Mobile-Friendly", why="text under 12 px needs zoom; Lighthouse fails a page when most of its text is that small", fix="raise the smallest text to 12 px; body to 16 px"),
    "font-size-mobile": dict(level="warning", source="Apple HIG 17 pt; GOV.UK 16 px; Material 16 sp", why="body text under 16 px on a phone forces zoom and iOS zooms inputs", fix="body and inputs ≥ 16 px at the mobile breakpoint"),
    "touch-target": dict(level="error", source="WCAG 2.2 SC 2.5.8", why="targets under 24 × 24 px are missed; error rates exceed 40 % below 8 mm (Henze 2011)", fix="give the element ≥ 24 px in both dimensions or 24 px of clearance; inline text links and unstyled native controls are exempt"),
    "touch-target-mobile": dict(level="warning", source="Apple HIG 44 pt; Material 48 dp", why="thumb targets need ~9 mm; below 44 px accuracy drops", fix="min-height / min-width 44 px on phones, padding rather than font size"),
    "icon-off-centre": dict(level="warning", source="Material icon buttons; Apple HIG; Gestalt symmetry", why="an icon drifting off the centre of its box reads as broken and the hit area no longer matches the glyph — the commonest padding regression", fix="centre the icon with flex (align-items / justify-content) or equal padding on all four sides"),
    "dead-toggle": dict(level="error", source="WAI-ARIA APG disclosure pattern; WCAG 4.1.2", why="a toggle that flips aria-expanded but reveals nothing, or does nothing at all, is a broken control — menus and accordions die this way after a CSS change", fix="check the CSS that shows the controlled element (opacity / visibility / display) and that the handler is attached"),
    "target-spacing": dict(level="warning", source="Material 8 dp; Lighthouse tap-targets; WCAG 2.5.8 clearance", why="targets closer than 8 px are mis-tapped; WCAG accepts small targets only with a 24 px clearance circle", fix="add ≥ 8 px between adjacent targets, or enlarge them"),
    "line-length": dict(level="warning", source="Dyson & Haselgrove 2001; Shaikh & Chaparro 2005; Bringhurst; GOV.UK", why="screen studies support 45–95 characters per line; guidelines put the sweet spot at 60–75", fix="max-width around 65ch on text blocks"),
    "line-height": dict(level="warning", source="WCAG 1.4.12; Butterick", why="body text under 1.2 line-height is cramped; 1.5 is what WCAG asks layouts to tolerate", fix="line-height 1.5 for body, 1.1–1.25 for display"),
    "text-clipped": dict(level="error", source="Xcode textClipped; ATF; UIS-Hunter", why="text cut off by its box loses words", fix="allow wrapping, add text-overflow: ellipsis, or widen the container"),
    "text-overlap": dict(level="error", source="OwlEye / Nighthawk display-issue classes", why="two text blocks drawn over each other are unreadable", fix="fix the positioning or the container size; check absolute/negative margins"),
    "image-distortion": dict(level="error", source="Lighthouse image-aspect-ratio", why="a stretched image reads as broken", fix="object-fit: cover / contain, or match the box to the intrinsic ratio"),
    "image-broken": dict(level="error", source="OwlEye missing-image class; Impeccable broken-image", why="a broken placeholder is the most visible defect on a page", fix="fix the src, or remove the element"),
    "img-alt": dict(level="warning", source="WCAG 2.2 SC 1.1.1", why="images without alt are invisible to screen readers (55 % of pages fail)", fix="alt text for meaningful images, alt=\"\" for decorative"),
    "viewport-meta": dict(level="error", source="Lighthouse viewport; MDN", why="without a viewport meta the page lays out at 980 px on phones and is zoomed out", fix="<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"),
    "heading-order": dict(level="warning", source="WCAG 1.3.1; axe heading-order", why="skipped levels and a missing h1 break the outline assistive tech navigates by", fix="one h1, then h2/h3 in order"),
    "type-noise": dict(level="warning", source="Refactoring UI; Material type scale; Ant (3–5 sizes)", why="more than 2–3 families or 8 sizes means no type system", fix="one or two families; a 5–8 step scale"),
    "empty-control": dict(level="error", source="WAVE link_empty / button_empty; WebAIM Million (45 % / 30 % of pages)", why="a link or button with no accessible name cannot be used by assistive tech", fix="text content or aria-label"),
    "generic-link": dict(level="warning", source="WAVE link_suspicious; jsx-a11y anchor-ambiguous-text; Lighthouse link-text", why="\"click here\" / \"read more\" say nothing out of context", fix="name the destination in the link text"),
    "redundant-link": dict(level="warning", source="WAVE link_redundant", why="adjacent links to the same URL are read twice", fix="merge them into one link"),
    "justified-text": dict(level="warning", source="WCAG 1.4.8; WAVE text_justified", why="justified text on the web produces rivers of white space", fix="text-align: left"),
    "underlined-text": dict(level="warning", source="WAVE underline", why="underlined non-link text looks like a link", fix="use weight or italics for emphasis"),
    "all-caps-body": dict(level="warning", source="Butterick (caps only under one line); HansCo", why="long all-caps runs lose word shapes and read slowly", fix="sentence case; caps only for short labels, with +5–12 % tracking"),
    "centered-body": dict(level="warning", source="Refactoring UI; HansCo", why="centred paragraphs longer than 2–3 lines lose the reading axis", fix="left-align body text; centre only short headings"),
    "contrast-polarity": dict(level="warning", source="Piepenbrock, Mayr, Mund & Buchner 2013/2014 (N = 169)", why="light-on-dark body text under 16 px is read less accurately; the effect is largest for small text", fix="dark mode is fine for large and UI text; raise small body text to 16 px or use a light surface"),
    "near-duplicate-colours": dict(level="warning", source="Mahy 1994 (ΔE ≈ 2.3 JND); Refactoring UI; the \"inconsistent greys\" tell", why="several colours within a just-noticeable difference of each other mean tokens were not used", fix="collapse them into one token per role"),
    "too-many-hues": dict(level="warning", source="Healey 1996 (~7 hues pre-attentively); Ant / Refactoring UI palette limits", why="more than seven distinct saturated hues on one page have no hierarchy", fix="one accent, one or two secondaries, tinted neutrals"),
    "pure-black-white": dict(level="note", source="Supercharge; Hobday rule 1; Hallmark gate 7", why="#000 on #fff is harsh; tinted near-black and near-white read softer", fix="e.g. #111 on #fafafa, tinted toward the accent hue"),
    "edge-margin": dict(level="warning", source="Apple 16/20 pt; Material 16/24 dp screen-edge margins", why="text touching the viewport edge looks cramped and may be cut by device bezels", fix="≥ 16 px side padding on phones, 24 px on desktop"),
    "false-floor": dict(level="warning", source="NN/g Illusion of Completeness; CXL false bottom", why="when the first screenful ends on a clean edge with nothing peeking below, users think the page is over", fix="let an element cross the fold, or add a scroll cue"),
    "hidden-nav-desktop": dict(level="warning", source="Pernice & Budiu 2016 (N = 179): −20 % discoverability, +39 % time", why="a hamburger at desktop widths halves navigation use", fix="show the primary links when there is room"),
    "multiple-primaries": dict(level="warning", source="Balsamiq; Dannaway; KlientBoost; Von Restorff", why="more than one primary button per view means nothing is primary", fix="one filled primary; the rest secondary or text buttons"),
    "consent-asymmetry": dict(level="warning", source="deceptive.design; EDPB cookie-banner taskforce; FTC; DSA Art. 25", why="a filled Accept next to a plain or link-styled Reject steers the choice", fix="style accept and reject with equal prominence"),
    "prechecked-optin": dict(level="warning", source="deceptive.design preselection; DSA Art. 25", why="a pre-ticked marketing box is consent nobody gave", fix="unchecked by default"),
    "urgency-text": dict(level="note", source="deceptive.design fake urgency / scarcity / social proof; FTC", why="countdowns, \"only N left\" and \"N people viewing\" are the most-cited deceptive patterns; a linter cannot know if they are true", fix="remove unless the claim is real and verifiable"),
    "confirmshaming": dict(level="note", source="deceptive.design; Mathur et al.", why="a decline option phrased as self-insult manipulates", fix="\"No thanks\""),
    "placeholder-residue": dict(level="error", source="Mobile-UI-Repair null-value class; AI-slop lorem-ipsum tell", why="lorem ipsum, \"undefined\", \"null\", \"NaN\" or \"[object Object]\" on a page means it is unfinished or broken", fix="real content; guard the empty case"),
    "focus-removed": dict(level="warning", source="WCAG 2.4.7; stylelint-a11y no-outline-none; Vercel WIG", why="outline: none without a replacement leaves keyboard users lost", fix="keep the outline, or add a :focus-visible ring (outline or box-shadow) with ≥ 3:1 contrast"),
    "motion": dict(level="warning", source="WCAG 2.3.3 / C39; axe no-autoplay-audio; Vercel WIG", why="autoplaying media and looping animation without a reduced-motion alternative trigger vestibular symptoms (35 % of adults over 40)", fix="@media (prefers-reduced-motion: reduce) { … }; autoplay muted with controls; no infinite loops"),
    "distracting-element": dict(level="error", source="axe blink / marquee", why="blink and marquee are obsolete and cannot be paused", fix="remove them"),
    "spacing-scale": dict(level="warning", source="8-pt grid (10+ design systems); RL-paper D1 spacing consistency", why="gaps off a 4/8 px scale and many distinct gap values read as arbitrary", fix="a spacing scale: 4 8 12 16 24 32 48 64"),
    "ai-look": dict(level="note", source="8 sources 2025–2026 (925studios, mania.design, dev.to, Hallmark, Impeccable, taste-skill, ux-skill, Anthropic cookbook)", why="indigo→cyan gradients, Inter as display, three identical icon cards, glass panels and nested cards are the tells readers use to spot generated pages", fix="a deliberate palette and type pairing; vary section structure; cards only where elevation means something"),
    "thumb-reach": dict(level="note", source="Bergstrom-Lehtovirta & Oulasvirta 2014; Hoober 2013 (49 % one-thumb)", why="a primary control in the top-far corner of a phone is out of one-handed reach", fix="put primary actions in the bottom half or the near edge"),
}

RULES_JS = r"""
async (vp) => {
  const out = [];
  const add = (rule, level, message, examples, extra) => {
    if (!examples.length) return;
    out.push({rule, level, message, examples: examples.slice(0, 5), count: examples.length, ...(extra || {})});
  };
  const H = vp.height, W = vp.width, mobile = !!vp.mobile;
  const all = [...document.querySelectorAll('body *')];
  const rectOf = (el) => el.getBoundingClientRect();
  const cs = (el) => getComputedStyle(el);
  // an element inside an opacity:0 / visibility:hidden ancestor is invisible too — checkVisibility knows
  const vis = (el) => { const r = rectOf(el); const c = cs(el);
    if (!(r.width > 2 && r.height > 2 && c.visibility !== 'hidden' && c.display !== 'none' && c.opacity !== '0' && r.bottom > 0 && r.top < H * 3)) return false;
    if (el.checkVisibility) { try { return el.checkVisibility({opacityProperty: true, visibilityProperty: true, contentVisibilityAuto: true}); } catch (e) { return true; } }
    return true; };
  const tag = (el) => { const id = el.id ? '#' + el.id : ''; const cls = el.classList && el.classList.length ? '.' + [...el.classList].slice(0, 2).join('.') : ''; return el.tagName.toLowerCase() + id + cls; };
  const txt = (el) => (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ');
  const parseRGB = (s) => { const m = s && s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(parseFloat); return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1}; };
  const lin = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const lum = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
  const ratio = (a, b) => { const la = lum(a), lb = lum(b); return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05); };
  const blend = (fg, bg) => ({r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1});
  const rgb2hsl = (c) => { const r = c.r / 255, g = c.g / 255, b = c.b / 255, mx = Math.max(r, g, b), mn = Math.min(r, g, b); let h = 0, s = 0; const l = (mx + mn) / 2;
    if (mx !== mn) { const d = mx - mn; s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn); h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; h *= 60; } return {h, s, l}; };
  const rgb2lab = (c) => { const f = (t) => t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116;
    const R = lin(c.r), G = lin(c.g), B = lin(c.b); const X = (R * 0.4124 + G * 0.3576 + B * 0.1805) / 0.95047, Y = R * 0.2126 + G * 0.7152 + B * 0.0722, Z = (R * 0.0193 + G * 0.1192 + B * 0.9505) / 1.08883;
    return {L: 116 * f(Y) - 16, a: 500 * (f(X) - f(Y)), b: 200 * (f(Y) - f(Z))}; };
  const dE = (p, q) => Math.hypot(p.L - q.L, p.a - q.a, p.b - q.b);
  const bgOf = (el) => { let node = el;
    while (node && node !== document.documentElement) { const c = cs(node);
      if (c.backgroundImage && c.backgroundImage !== 'none') return null;
      const col = parseRGB(c.backgroundColor); if (col && col.a > 0) return col.a >= 1 ? col : blend(col, {r: 255, g: 255, b: 255, a: 1});
      node = node.parentElement; }
    const root = parseRGB(cs(document.documentElement).backgroundColor); return (root && root.a > 0) ? root : {r: 255, g: 255, b: 255, a: 1}; };
  const textNodesOf = (el) => [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim().length > 1);
  const isCode = (el) => !!el.closest('code, pre, kbd, samp, script, style');
  const interactiveSel = 'a[href], button, input:not([type=hidden]), select, textarea, [role=button], [role=link], [onclick]';
  const pageBg = (() => { const b = parseRGB(cs(document.body).backgroundColor); return b && b.a > 0 ? b : {r: 255, g: 255, b: 255, a: 1}; })();
  const isButtonLike = (el) => { const c = cs(el); const bg = parseRGB(c.backgroundColor); const t = el.tagName;
    if (!((t === 'BUTTON' || t === 'A' || el.getAttribute('role') === 'button') && bg && bg.a > 0.5 && c.display !== 'inline' && parseFloat(c.paddingLeft) >= 8)) return false;
    // "primary-style" = a filled button that stands out from the page: saturated, or strongly contrasting with the page background
    const h = rgb2hsl(bg); return h.s > 0.35 || ratio(bg, pageBg) > 4.5; };

  // ---------------- text ----------------
  const lowContrast = [], tiny = [], smallBody = [], longLines = [], tightLeading = [], clipped = [], justified = [], underlined = [], caps = [], centered = [], polarity = [], edge = [];
  const families = new Set(), sizes = new Set(); let textChars = 0, tinyChars = 0;
  const textEls = [];
  for (const el of all) {
    if (!vis(el) || isCode(el)) continue;
    const tn = textNodesOf(el); if (!tn.length) continue;
    const c = cs(el), r = rectOf(el);
    const chars = tn.reduce((n, t) => n + t.textContent.trim().length, 0);
    const fs = parseFloat(c.fontSize);
    textEls.push({el, r, chars, fs});
    families.add(c.fontFamily.split(',')[0].trim().replace(/["']/g, '')); sizes.add(Math.round(fs)); textChars += chars;
    if (fs < 12) { tinyChars += chars; tiny.push(tag(el) + ' ' + fs.toFixed(0) + 'px'); }
    if (mobile && chars >= 80 && fs < 16 && ['p', 'li', 'td', 'div', 'span'].includes(el.tagName.toLowerCase())) smallBody.push(tag(el) + ' ' + fs.toFixed(0) + 'px');
    const fg = parseRGB(c.color), bg = bgOf(el);
    if (fg && bg && fg.a > 0) {
      const fgB = fg.a < 1 ? blend(fg, bg) : fg;
      const rt = ratio(fgB, bg); const bold = parseInt(c.fontWeight, 10) >= 700; const large = fs >= 24 || (bold && fs >= 18.66);
      if (rt < (large ? 3 : 4.5)) lowContrast.push(tag(el) + ' ' + rt.toFixed(1) + ':1');
      if (chars >= 80 && fs < 16 && lum(bg) < lum(fgB)) polarity.push(tag(el) + ' ' + fs.toFixed(0) + 'px light-on-dark');
    }
    if (chars >= 120) {
      const cpl = r.width / (fs * 0.5);
      if (cpl > 100 || cpl < 35) longLines.push(tag(el) + ' ~' + Math.round(cpl) + ' chars/line');
      const lh = c.lineHeight === 'normal' ? 1.2 * fs : parseFloat(c.lineHeight);
      if (lh / fs < 1.2) tightLeading.push(tag(el) + ' ' + (lh / fs).toFixed(2));
      if (c.textAlign === 'justify') justified.push(tag(el));
      const lhpx = c.lineHeight === 'normal' ? 1.2 * fs : parseFloat(c.lineHeight);
      if (chars >= 240 && c.textAlign === 'center' && r.height / lhpx >= 4) centered.push(tag(el) + ' ' + chars + ' chars, ' + Math.round(r.height / lhpx) + ' lines');
    }
    if (chars >= 80 && c.textTransform === 'uppercase') caps.push(tag(el) + ' ' + chars + ' chars');
    if (c.textDecorationLine && c.textDecorationLine.includes('underline') && !el.closest('a') && chars >= 3 && !['U', 'INS', 'ABBR'].includes(el.tagName)) underlined.push(tag(el));
    if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0 && (c.overflowX === 'hidden' || c.overflow === 'hidden') && c.textOverflow !== 'ellipsis' && c.whiteSpace === 'nowrap') clipped.push(tag(el));
    const margin = mobile ? 8 : 12;
    if (chars >= 20 && r.width < W * 0.98 && (r.left < margin || W - r.right < margin) && r.top < H * 2) edge.push(tag(el) + ' ' + Math.round(Math.max(0, Math.min(r.left, W - r.right))) + 'px from edge');
  }
  add('text-contrast', 'error', 'text below WCAG contrast (4.5:1, 3:1 for large text)', lowContrast);
  add('font-size', textChars && tinyChars / textChars > 0.4 ? 'error' : 'warning', 'text under 12px', tiny, {share: textChars ? +(tinyChars / textChars).toFixed(2) : 0});
  add('font-size-mobile', 'warning', 'body text under 16px on a phone', smallBody);
  add('line-length', 'warning', 'measure outside 35–100 characters per line (60–75 is the sweet spot)', longLines);
  add('line-height', 'warning', 'body text line-height under 1.2', tightLeading);
  add('text-clipped', 'error', 'text cut off by its box (nowrap + overflow hidden, no ellipsis)', clipped);
  add('justified-text', 'warning', 'justified text (rivers)', justified);
  add('underlined-text', 'warning', 'underlined text that is not a link', underlined);
  add('all-caps-body', 'warning', 'long all-caps text', caps);
  add('centered-body', 'warning', 'long centred paragraph', centered);
  add('contrast-polarity', 'warning', 'small light-on-dark body text', polarity);
  add('edge-margin', 'warning', 'text touching the viewport edge', edge);
  if (families.size > 3) add('type-noise', 'warning', families.size + ' font families on one page (keep to 1–2)', [...families]);
  if (sizes.size > 8) add('type-noise', 'warning', sizes.size + ' distinct font sizes on one page (a type scale has 5–8)', [...sizes].sort((a, b) => a - b).map(String));

  // icon centring: a text-less control holding one visible child should hold it centred
  const offC = [];
  for (const el of all) {
    if (!(['A', 'BUTTON'].includes(el.tagName) || el.getAttribute('role') === 'button') || !vis(el)) continue;
    if ([...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    // the glyph may be a 2px bar whose ::before/::after draw the rest, so judge children by their own box, not vis()
    const kids = [...el.children].filter(k => { const kr = rectOf(k), kc = cs(k); return kr.width > 0 && kr.height > 0 && (kr.width > 1 || kr.height > 1) && kc.display !== 'none' && kc.visibility !== 'hidden'; });
    if (kids.length !== 1) continue;
    const r = rectOf(el), k = rectOf(kids[0]);
    if (r.width < 24 || r.height < 24 || (k.width > r.width * 0.9 && k.height > r.height * 0.9)) continue;
    const dx = (k.left + k.right - r.left - r.right) / 2, dy = (k.top + k.bottom - r.top - r.bottom) / 2;
    if (Math.abs(dx) > 2.5 || Math.abs(dy) > 2.5) offC.push(tag(el) + ' ' + [Math.abs(dx) > 2.5 ? Math.round(dx) + 'px across' : '', Math.abs(dy) > 2.5 ? Math.round(dy) + 'px down' : ''].filter(Boolean).join(', '));
  }
  add('icon-off-centre', 'warning', 'icon not centred in its control', offC);

  // toggles: a button with aria-expanded / aria-controls must change something when activated (runs after the screenshot; state is restored)
  const dead = [];
  const shown = (t) => !!t && vis(t) && parseFloat(cs(t).opacity) > 0.5 && cs(t).pointerEvents !== 'none';
  const toggles = all.filter(el => (el.tagName === 'BUTTON' || el.getAttribute('role') === 'button') && !el.closest('a') && (el.hasAttribute('aria-expanded') || el.hasAttribute('aria-controls')) && vis(el)).slice(0, 4);
  for (const el of toggles) {
    const target = el.getAttribute('aria-controls') ? document.getElementById(el.getAttribute('aria-controls')) : null;
    const before = el.getAttribute('aria-expanded'), tBefore = target ? shown(target) : null;
    try { el.click(); } catch (e) { continue; }
    await new Promise(r => setTimeout(r, 400));
    const flipped = el.getAttribute('aria-expanded') !== before, moved = target ? shown(target) !== tBefore : null;
    if (target ? !moved : !flipped) dead.push(tag(el) + (target ? ' → #' + target.id + (flipped ? ' (aria-expanded flips but the target stays ' + (tBefore ? 'visible' : 'hidden') + ')' : ' (nothing changes)') : ' (aria-expanded does not change)'));
    try { el.click(); await new Promise(r => setTimeout(r, 150)); } catch (e) {}
    if (before !== null && el.getAttribute('aria-expanded') !== before) el.setAttribute('aria-expanded', before);
  }
  add('dead-toggle', 'error', 'toggle that changes nothing when activated', dead);

  // text overlap: two text elements whose boxes intersect, neither containing the other
  const lineBoxes = (el) => { const rs = [...el.getClientRects()].filter(r => r.width > 2 && r.height > 2); return rs.length ? rs : [rectOf(el)]; };
  const overlap = [];
  const tx = textEls.filter(t => t.r.top < H * 2 && t.chars >= 3);
  for (let i = 0; i < tx.length && overlap.length < 8; i++) for (let j = i + 1; j < tx.length; j++) {
    const a = tx[i], b = tx[j];
    if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
    const ix = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left), iy = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
    if (ix <= 2 || iy <= 2) continue;
    // a wrapped inline element's bounding box covers whole lines it only partly occupies: compare line boxes
    let hit = false;
    for (const ra of lineBoxes(a.el)) { for (const rb of lineBoxes(b.el)) {
      const jx = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left), jy = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
      if (jx <= 2 || jy <= 2) continue;
      const small = Math.min(ra.width * ra.height, rb.width * rb.height);
      if (small > 0 && jx * jy / small > 0.2) { hit = true; break; } } if (hit) break; }
    if (hit) { overlap.push(tag(a.el) + ' × ' + tag(b.el)); break; }
  }
  add('text-overlap', 'error', 'text drawn over other text', overlap);

  // ---------------- controls ----------------
  const tinyT = [], tinyC = [], smallT = [], close = [], emptyC = [], genericL = [], redundantL = [], targets = [];
  const generic = /^(click here|here|read more|more|learn more|link|this|continue|go)$/i;
  let prevHref = null, prevEl = null;
  for (const el of document.querySelectorAll(interactiveSel)) {
    if (!vis(el)) continue;
    const r = rectOf(el), c = cs(el), m = Math.min(r.width, r.height);
    const inlineLink = el.tagName === 'A' && c.display === 'inline';
    const nativeControl = ['SELECT', 'INPUT', 'TEXTAREA'].includes(el.tagName) && c.appearance !== 'none';
    if (m < 24 && !inlineLink && !nativeControl) tinyC.push({el, r});
    else if (mobile && m < 44 && !inlineLink) smallT.push(tag(el) + ' ' + Math.round(r.width) + '×' + Math.round(r.height));  // a link inside running text cannot be 44 px tall; the HIG target size is for controls
    if (!inlineLink) targets.push({el, r});
    const name = (txt(el) || el.getAttribute('aria-label') || el.getAttribute('title') || (el.querySelector('img') && el.querySelector('img').alt) || (el.tagName === 'INPUT' ? (el.value || el.placeholder) : '') || '').trim();
    if (['A', 'BUTTON'].includes(el.tagName) && !name && !el.querySelector('svg[aria-label], [aria-label]')) emptyC.push(tag(el));
    if (el.tagName === 'A' && generic.test(name)) genericL.push(tag(el) + ' "' + name + '"');
    if (el.tagName === 'A' && el.href && prevHref === el.href && prevEl && prevEl.parentElement === el.parentElement) redundantL.push(tag(el));
    prevHref = el.tagName === 'A' ? el.href : null; prevEl = el;
  }
  // WCAG 2.5.8 spacing exception: a small target passes when a 24px circle centred on it meets no other target
  for (const t of tinyC) {
    const cx = (t.r.left + t.r.right) / 2, cy = (t.r.top + t.r.bottom) / 2; let clear = true;
    for (const o of targets) { if (o.el === t.el || o.el.contains(t.el) || t.el.contains(o.el)) continue;
      const dx = Math.max(o.r.left - cx, 0, cx - o.r.right), dy = Math.max(o.r.top - cy, 0, cy - o.r.bottom);
      if (dx * dx + dy * dy < 144) { clear = false; break; } }
    if (clear) { if (mobile && Math.min(t.r.width, t.r.height) < 44) smallT.push(tag(t.el) + ' ' + Math.round(t.r.width) + '×' + Math.round(t.r.height)); }
    else tinyT.push(tag(t.el) + ' ' + Math.round(t.r.width) + '×' + Math.round(t.r.height)); }
  for (let i = 0; i < targets.length && close.length < 8; i++) for (let j = i + 1; j < targets.length; j++) {
    const a = targets[i].r, b = targets[j].r;
    const gapX = Math.max(a.left, b.left) - Math.min(a.right, b.right), gapY = Math.max(a.top, b.top) - Math.min(a.bottom, b.bottom);
    const gap = Math.max(gapX, gapY);
    if (gap >= 0 && gap < 8 && (Math.min(a.width, a.height) < 44 || Math.min(b.width, b.height) < 44)) { close.push(tag(targets[i].el) + ' ↔ ' + tag(targets[j].el) + ' ' + Math.round(gap) + 'px'); break; }
  }
  add('touch-target', 'error', 'interactive element under 24×24px', tinyT);
  add('touch-target-mobile', 'warning', 'interactive element under 44×44px on a phone', smallT);
  add('target-spacing', 'warning', 'targets under 8px apart', close);
  add('empty-control', 'error', 'link or button with no accessible name', emptyC);
  add('generic-link', 'warning', 'generic link text', genericL);
  add('redundant-link', 'warning', 'adjacent links to the same URL', redundantL);

  // ---------------- images ----------------
  const distorted = [], noAlt = [], broken = [];
  for (const img of document.images) {
    if (!vis(img)) continue;
    if (img.complete && img.naturalWidth === 0 && img.getAttribute('src')) { broken.push(tag(img)); continue; }
    if (!img.naturalWidth || !img.naturalHeight) continue;
    const c = cs(img); if (!img.hasAttribute('alt')) noAlt.push(tag(img));
    if (['cover', 'contain', 'scale-down', 'none'].includes(c.objectFit)) continue;
    const r = rectOf(img); const nat = img.naturalWidth / img.naturalHeight, ren = r.width / r.height;
    if (r.width > 24 && Math.abs(nat / ren - 1) > 0.05) distorted.push(tag(img) + ' ' + (nat / ren).toFixed(2) + '× stretched');
  }
  add('image-distortion', 'error', 'image rendered at a different aspect ratio than its source', distorted);
  add('image-broken', 'error', 'broken image', broken);
  add('img-alt', 'warning', 'images without alt text', noAlt);

  // ---------------- document ----------------
  if (mobile && !document.querySelector('meta[name=viewport]')) add('viewport-meta', 'error', 'no <meta name="viewport">: the page lays out at 980px on phones', ['head']);
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis).map(h => +h.tagName[1]);
  if (!hs.includes(1) && document.body.innerText.trim().length > 200) add('heading-order', 'warning', 'no h1 on the page', ['body']);
  for (let i = 1; i < hs.length; i++) if (hs[i] > hs[i - 1] + 1) { add('heading-order', 'warning', 'heading level skipped (h' + hs[i - 1] + ' → h' + hs[i] + ')', ['h' + hs[i]]); break; }
  const distract = [...document.querySelectorAll('marquee, blink')];
  add('distracting-element', 'error', '<marquee>/<blink>', distract.map(tag));

  // residue: lorem ipsum, null/undefined/NaN/[object Object]
  const residue = [];
  for (const t of textEls) {
    if (isCode(t.el)) continue;
    const s = txt(t.el);
    if (/lorem ipsum/i.test(s)) residue.push(tag(t.el) + ' lorem ipsum');
    else if (/(^|\s)(undefined|null|NaN|\[object Object\])(\s|$|[.,;:·])/.test(s)) residue.push(tag(t.el) + ' "' + (s.match(/undefined|null|NaN|\[object Object\]/) || [''])[0] + '"');
  }
  add('placeholder-residue', 'error', 'unfinished or broken content', residue);

  // deceptive patterns the DOM can see
  const urgency = [], shame = [], preticked = [], asym = [];
  const urgRe = /(\b\d{1,2}:\d{2}:\d{2}\b|only \d+ left|\d+ people (are )?(viewing|looking)|hurry|ends (in|soon)|limited time|selling fast|\d+ (others )?bought (this )?(today|recently))/i;
  for (const t of textEls) { const s = txt(t.el); if (s.length < 200 && urgRe.test(s)) urgency.push(tag(t.el) + ' "' + s.slice(0, 40) + '"'); }
  for (const el of document.querySelectorAll('button, a[href], [role=button]')) {
    const s = txt(el); if (s.length > 22 && /^(no|nope|not now)[, ]/i.test(s) && /\b(I|my|me)\b/.test(s)) shame.push(tag(el) + ' "' + s.slice(0, 50) + '"');
  }
  for (const cb of document.querySelectorAll('input[type=checkbox]:checked')) {
    const lab = (cb.labels && cb.labels[0] ? txt(cb.labels[0]) : '') + ' ' + txt(cb.closest('label, li, div, p') || cb.parentElement || cb);
    if (/newsletter|marketing|subscribe|offers|promotions|updates|partners|third.part/i.test(lab)) preticked.push(tag(cb) + ' "' + lab.trim().slice(0, 40) + '"');
  }
  const accepts = [...document.querySelectorAll('button, a[href], [role=button]')].filter(el => vis(el) && /^(accept|agree|allow|ok|got it|yes)/i.test(txt(el)));
  for (const acc of accepts) {
    const scope = acc.closest('dialog, [role=dialog], [aria-modal], section, form, div') || document.body;
    const rej = [...scope.querySelectorAll('button, a[href], [role=button]')].find(el => el !== acc && vis(el) && /^(reject|decline|refuse|deny|no thanks|only necessary|manage|settings|customi[sz]e)/i.test(txt(el)));
    if (!rej) continue;
    const a = cs(acc), r = cs(rej), ab = parseRGB(a.backgroundColor), rb = parseRGB(r.backgroundColor);
    const aFilled = ab && ab.a > 0.5 && rgb2hsl(ab).s > 0.2, rPlain = !rb || rb.a < 0.2 || rgb2hsl(rb).s < 0.1;
    const areaA = rectOf(acc).width * rectOf(acc).height, areaR = rectOf(rej).width * rectOf(rej).height;
    if ((aFilled && rPlain) || areaA > 2.5 * areaR) asym.push(tag(acc) + ' "' + txt(acc).slice(0, 12) + '" vs ' + tag(rej) + ' "' + txt(rej).slice(0, 14) + '"');
  }
  add('urgency-text', 'note', 'urgency / scarcity / social-proof text', urgency);
  add('confirmshaming', 'note', 'decline option phrased as self-insult', shame);
  add('prechecked-optin', 'warning', 'pre-ticked marketing opt-in', preticked);
  add('consent-asymmetry', 'warning', 'accept styled far more prominently than reject', asym);

  // ---------------- colour system ----------------
  const cols = [];
  for (const el of all.slice(0, 3000)) { if (!vis(el)) continue; const c = cs(el);
    for (const v of [c.color, c.backgroundColor, c.borderTopColor]) { const p = parseRGB(v); if (p && p.a > 0.5) cols.push(p); } }
  const uniq = []; const seen = new Set();
  for (const c of cols) { const k = [Math.round(c.r), Math.round(c.g), Math.round(c.b)].join(','); if (!seen.has(k)) { seen.add(k); uniq.push({c, lab: rgb2lab(c), k}); } }
  const near = [];
  for (let i = 0; i < uniq.length && near.length < 6; i++) for (let j = i + 1; j < uniq.length; j++) {
    const d = dE(uniq[i].lab, uniq[j].lab); if (d > 0.3 && d < 2.3) { near.push('rgb(' + uniq[i].k + ') ≈ rgb(' + uniq[j].k + ') ΔE ' + d.toFixed(1)); break; } }
  if (near.length >= 3) add('near-duplicate-colours', 'warning', near.length + '+ pairs of colours within a just-noticeable difference', near);
  const hueBins = new Set();
  for (const u of uniq) { const h = rgb2hsl(u.c); if (h.s > 0.35 && h.l > 0.15 && h.l < 0.85) hueBins.add(Math.round(h.h / 30) % 12); }
  if (hueBins.size > 7) add('too-many-hues', 'warning', hueBins.size + ' distinct saturated hues', [...hueBins].map(b => (b * 30) + '°'));
  const bodyBg = parseRGB(cs(document.body).backgroundColor), bodyFg = parseRGB(cs(document.body).color);
  if (bodyBg && bodyFg && bodyBg.a > 0 && ((bodyBg.r + bodyBg.g + bodyBg.b) >= 765 && (bodyFg.r + bodyFg.g + bodyFg.b) === 0)) add('pure-black-white', 'note', 'pure #000 text on pure #fff', ['body']);

  // focus rings removed in the stylesheets; reduced-motion; keyframes
  let focusNone = 0, focusStyled = 0, reduced = false, keyframes = 0;
  for (const sheet of document.styleSheets) { let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
    const walk = (rs) => { for (const r of rs) {
      if (r.type === 4 && /prefers-reduced-motion/.test((r.media && r.media.mediaText) || r.conditionText || '')) reduced = true;
      if (r.type === 7) keyframes++;
      if (r.cssRules && r.type !== 7) walk(r.cssRules);
      if (r.selectorText && /:focus/.test(r.selectorText)) {
        const o = r.style.outlineStyle || r.style.outline; if (/none|^0$/.test(o || '')) focusNone++; else if (r.style.outline || r.style.outlineStyle || r.style.boxShadow || r.style.outlineColor) focusStyled++;
      } } };
    walk(rules); }
  if (focusNone && !focusStyled) add('focus-removed', 'warning', 'outline: none on :focus with no visible replacement', [focusNone + ' rule(s)']);
  const anims = (document.getAnimations ? document.getAnimations() : []);
  const infinite = anims.filter(a => a.effect && a.effect.getTiming && a.effect.getTiming().iterations === Infinity);
  const media = [...document.querySelectorAll('video[autoplay], audio[autoplay]')].filter(vis);
  const motion = [];
  for (const m of media) if (!m.muted) motion.push(tag(m) + ' autoplay with sound');
  if (infinite.length && !reduced) motion.push(infinite.length + ' infinite animation(s), no prefers-reduced-motion rule');
  else if (keyframes && !reduced && !infinite.length) motion.push(keyframes + ' @keyframes, no prefers-reduced-motion rule');
  add('motion', 'warning', 'motion without a reduced-motion alternative or autoplay with sound', motion);

  // ---------------- layout ----------------
  const crossing = all.some(el => { if (!vis(el)) return false; const r = rectOf(el); return r.top < H && r.bottom > H && r.height < H * 2 && r.width > 40; });
  const docH = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
  if (!crossing && docH > H * 1.3) add('false-floor', 'warning', 'the first screenful ends on a clean edge with nothing peeking below the fold', ['viewport ' + H + 'px, page ' + docH + 'px']);
  if (!mobile) {
    const navs = [...document.querySelectorAll('nav, [role=navigation]')];
    const burger = [...document.querySelectorAll('button, a')].find(b => vis(b) && (/menu|burger|hamburger/i.test(b.getAttribute('aria-label') || '') || /burger|hamburger|nav-toggle|menu-toggle/i.test(b.className || '')));
    if (burger && navs.length && !navs.some(n => [...n.querySelectorAll('a')].filter(vis).length >= 3)) add('hidden-nav-desktop', 'warning', 'primary navigation hidden behind a menu button at desktop width', [tag(burger)]);
  }
  const buttonLike = [...document.querySelectorAll('button, a[href], [role=button]')].filter(el => vis(el) && rectOf(el).top < H && isButtonLike(el));
  const byBg = {}; for (const b of buttonLike) { const c = parseRGB(cs(b).backgroundColor); const h = rgb2hsl(c); const k = Math.round(h.h / 15) + ':' + Math.round(h.l * 10); (byBg[k] = byBg[k] || []).push(b); }
  const primaries = Object.values(byBg).sort((a, b) => b.length - a.length)[0] || [];
  if (primaries.length > 1) add('multiple-primaries', 'warning', primaries.length + ' filled primary-style buttons in the first viewport', primaries.map(b => tag(b) + ' "' + txt(b).slice(0, 16) + '"'));
  if (mobile) {
    const far = buttonLike.filter(b => { const r = rectOf(b); return r.top < H * 0.25 && (r.left > W * 0.6 || r.right < W * 0.4) && txt(b).length > 0 && !/menu|search|close/i.test(txt(b) + (b.getAttribute('aria-label') || '')); });
    add('thumb-reach', 'note', 'primary-style control in the top corner of the phone screen', far.map(b => tag(b) + ' "' + txt(b).slice(0, 16) + '"'));
  }
  // spacing scale: vertical gaps between visible siblings in containers with >= 3 children
  const gaps = [];
  for (const el of all) { if (gaps.length > 400) break; const kids = [...el.children].filter(k => vis(k) && cs(k).position !== 'absolute'); if (kids.length < 3) continue;
    const rs = kids.map(rectOf).sort((a, b) => a.top - b.top);
    for (let i = 1; i < rs.length; i++) { const g = rs[i].top - rs[i - 1].bottom; if (g > 0 && g < 200 && Math.abs(rs[i].left - rs[i - 1].left) < 4) gaps.push(Math.round(g)); } }
  if (gaps.length >= 12) { const off = gaps.filter(g => g % 4 !== 0).length; const distinct = new Set(gaps).size;
    if (off / gaps.length > 0.6 && distinct > 8) add('spacing-scale', 'warning', Math.round(100 * off / gaps.length) + '% of vertical gaps are off a 4px scale (' + distinct + ' distinct values)', [...new Set(gaps)].slice(0, 8).map(g => g + 'px')); }

  // ---------------- the AI look (a note, never a penalty) ----------------
  const tells = [];
  let purple = 0, glass = 0, nested = 0;
  for (const el of all.slice(0, 3000)) { if (!vis(el)) continue; const c = cs(el);
    if (c.backgroundImage && /linear-gradient|radial-gradient/.test(c.backgroundImage)) { const stops = (c.backgroundImage.match(/rgba?\([^)]+\)/g) || []).map(parseRGB).filter(Boolean).map(rgb2hsl).filter(h => h.s > 0.3);
      if (stops.some(h => h.h >= 240 && h.h <= 300) && stops.some(h => (h.h >= 180 && h.h < 240) || (h.h > 300 && h.h <= 340)) && rectOf(el).width * rectOf(el).height > 20000) purple++; }
    if (c.backdropFilter && c.backdropFilter !== 'none' && /blur/.test(c.backdropFilter)) glass++;
  }
  for (const el of all) { if (!vis(el)) continue; const c = cs(el); const bc = parseRGB(c.borderTopColor);
    const isCard = parseFloat(c.borderRadius) >= 8 && (c.boxShadow !== 'none' || (bc && bc.a > 0 && parseFloat(c.borderTopWidth) > 0)) && rectOf(el).width > 120;
    if (!isCard || !el.parentElement) continue;
    const outer = el.parentElement.closest('[class*=card], .card'); if (outer && outer !== el && rectOf(outer).width > rectOf(el).width) nested++; }
  if (purple) tells.push(purple + ' indigo/purple→cyan gradient surface(s)');
  if (glass >= 3) tells.push(glass + ' backdrop-blur panels');
  if (nested >= 2) tells.push(nested + ' cards nested in cards');
  const rows = [...document.querySelectorAll('section, div')].filter(vis).filter(p => { const kids = [...p.children].filter(vis); if (kids.length !== 3 && kids.length !== 6) return false;
    const sig = (k) => k.tagName + ':' + [...k.children].map(x => x.tagName).join(','); const s0 = sig(kids[0]);
    return kids.every(k => sig(k) === s0) && kids.every(k => k.querySelector('svg, img') && k.querySelector('h2,h3,h4')) && Math.abs(rectOf(kids[0]).top - rectOf(kids[1]).top) < 4; });
  if (rows.length) tells.push(rows.length + ' row(s) of three identical icon-heading cards');
  const displayInter = textEls.some(t => t.fs >= 32 && /^(Inter|Roboto|Arial|Helvetica|system-ui|-apple-system)$/i.test(cs(t.el).fontFamily.split(',')[0].trim().replace(/["']/g, '')));
  if (displayInter) tells.push('Inter/Roboto/Arial/system as the display face');
  if (tells.length >= 2) add('ai-look', 'note', 'reads as generated: ' + tells.join('; '), tells);

  return out;
}
"""

PENALTY = {"error": 3}
PENALTY_CAP = 12


def run(page, vp: dict) -> list:
    """Evaluate the rules inside a Playwright page. Returns a list of findings with metadata."""
    try:
        findings = page.evaluate(RULES_JS, {"width": vp["width"], "height": vp["height"], "mobile": bool(vp.get("mobile"))})
    except Exception as e:  # a page that throws must not kill the score
        return [{"rule": "rules", "level": "note", "message": f"rules could not run: {type(e).__name__}: {str(e)[:120]}", "examples": [], "count": 0}]
    for f in findings:
        meta = RULES.get(f["rule"], {})
        f.setdefault("source", meta.get("source", ""))
        f["why"] = meta.get("why", "")
        f["fix"] = meta.get("fix", "")
    return findings


def apply(report: dict, findings: list, viewport: str) -> None:
    """Attach findings to a beauty report: hints, penalties (errors only), report['rules']."""
    report["rules"] = findings
    errors = [f for f in findings if f["level"] == "error"]
    if errors:
        pen = min(PENALTY_CAP, PENALTY["error"] * len(errors))
        report.setdefault("penalties", {})["rules"] = pen
        report["score"] = max(1, report["score"] - pen)
    order = {"error": 0, "warning": 1, "note": 2}
    for f in sorted(findings, key=lambda f: order.get(f["level"], 3)):
        ex = ", ".join(f["examples"][:2])
        more = f" (+{f['count'] - 2} more)" if f["count"] > 2 else ""
        line = f"{f['rule']} [{f['level']}, {viewport}]: {f['message']} — {ex}{more}"
        if f["level"] == "error":
            report["hints"].insert(0, line)
        else:
            report["hints"].append(line)
