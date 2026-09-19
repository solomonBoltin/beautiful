"""
beautiful.explain
-----------------
Draw what the formula sees. ``explain(image, mode)`` returns one PNG contact sheet: the image
with each factor's evidence painted over it, titled with the factor's value, so a person (or an
agent reading the file) can tell *why* the number is what it is.

    from beautiful.explain import explain
    explain("shot.png").save("shot.explain.png")
    beautiful --explain out/ shot.png            # the CLI writes <name>.explain.png

Panels (ui / web modes):
  composition   mirror axes, centre of mass vs centre, mass split left/right, and the
                mirror-difference map (red where the left half disagrees with the right)
  alignment     the strongest vertical / horizontal grid lines the layout is explained by
  whitespace    the background mask (what counts as air)
  simplicity    the edge map (what counts as complexity)
  contrast      edges coloured by their luminance step (red = weak figure–ground)
  harmony       hue wheel with the fitted template, and the dominant-colour swatches
  edges         the four border bands and how much content touches each (clipping)
Art / logo modes add fractal / Fourier / thirds panels where relevant.
"""
from __future__ import annotations

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import convolve2d

from . import features as F
from .core import beauty
from .symmetry import _balance, _structure, _to_gray, _tone

PANEL_W = 420
FONTS = ["/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "C:/Windows/Fonts/arial.ttf"]
_TEMPLATES = {  # mirror of features._TEMPLATES for drawing: (offset, width) sectors in degrees
    "i": [(0, 18)], "V": [(0, 94)], "L": [(0, 18), (90, 80)], "I": [(0, 18), (180, 18)],
    "T": [(0, 180)], "Y": [(0, 94), (180, 18)], "X": [(0, 94), (180, 94)], "N": [],
}


def _font(size):
    for p in FONTS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _fit(im: Image.Image, w: int = PANEL_W) -> Image.Image:
    return im.resize((w, max(1, round(im.height * w / im.width))), Image.LANCZOS)


def _heat(base: Image.Image, mask: np.ndarray, colour=(255, 60, 60), alpha_max=0.75) -> Image.Image:
    """Tint `base` where `mask` (0..1, same size) is high."""
    m = np.clip(mask, 0, 1)[..., None] * alpha_max
    b = np.asarray(base.convert("RGB")).astype(np.float32)
    c = np.array(colour, dtype=np.float32)
    return Image.fromarray(np.clip(b * (1 - m) + c * m, 0, 255).astype(np.uint8))


def _resize_mask(mask: np.ndarray, size) -> np.ndarray:
    return np.asarray(Image.fromarray((np.clip(mask, 0, 1) * 255).astype(np.uint8)).resize(size, Image.BILINEAR)) / 255.0


# --------------------------------------------------------------------------- #
# panels
# --------------------------------------------------------------------------- #
def panel_composition(img: Image.Image, report: dict, mode: str) -> Image.Image:
    base = _fit(img)
    w, h = base.size
    g = _to_gray(img)
    st = _structure(g)
    diff = np.abs(st - np.fliplr(st))
    diff = diff / (diff.max() + 1e-6)
    out = _heat(base, _resize_mask(diff, (w, h)), (255, 70, 70), 0.6)
    d = ImageDraw.Draw(out)
    d.line([(w // 2, 0), (w // 2, h)], fill=(120, 200, 255), width=2)
    d.line([(0, h // 2), (w, h // 2)], fill=(120, 200, 255), width=1)
    sym = report["raw"]["symmetry"]
    dx, dy = sym["mass_offset"]["dx"], sym["mass_offset"]["dy"]
    cx, cy = w / 2 * (1 + dx), h / 2 * (1 + dy)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(255, 220, 0), width=3)
    d.line([(w / 2, h / 2), (cx, cy)], fill=(255, 220, 0), width=2)
    bp = sym.get("balance_parts", {})
    f = _font(15)
    d.rectangle([0, h - 24, w, h], fill=(0, 0, 0))
    d.text((6, h - 21), f"mass L {bp.get('mass_left', 0):.0%}  R {bp.get('mass_right', 0):.0%}   mirror {sym['horizontal_mirror']:.2f}  balance {sym['balance']:.2f}",
           fill="white", font=f)
    return out


def panel_alignment(img: Image.Image, report: dict) -> Image.Image:
    base = _fit(img)
    w, h = base.size
    rgb = F.to_rgb(img, 768)
    g = F.luminance(rgb)
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    vert = np.abs(convolve2d(g, kx, mode="same", boundary="symm")) > 0.08
    horz = np.abs(convolve2d(g, kx.T, mode="same", boundary="symm")) > 0.08
    out = base.copy()
    d = ImageDraw.Draw(out)
    for m, k, axis in ((vert, 8, "x"), (horz.T, 16, "y")):
        prof = np.zeros(m.shape[1])
        pad = np.zeros((1, m.shape[1]), dtype=int)
        dd = np.diff(np.vstack([pad, m.astype(int), pad]), axis=0)
        for j in range(m.shape[1]):
            stt = np.where(dd[:, j] == 1)[0]; en = np.where(dd[:, j] == -1)[0]
            if stt.size:
                runs = en - stt
                prof[j] = runs[runs >= 20].sum()
        if prof.sum() <= 0:
            continue
        p = np.convolve(prof, np.ones(3), mode="same")
        idx = np.argsort(p)[::-1][:k]
        for i in idx:
            if p[i] <= 0:
                continue
            if axis == "x":
                x = int(i * w / m.shape[1]); d.line([(x, 0), (x, h)], fill=(80, 220, 120), width=2)
            else:
                y = int(i * h / m.shape[1]); d.line([(0, y), (w, y)], fill=(80, 160, 255), width=2)
    return out


def panel_mask(img: Image.Image, mask: np.ndarray, colour, alpha=0.65) -> Image.Image:
    base = _fit(img)
    return _heat(base, _resize_mask(mask, base.size), colour, alpha)


def panel_contrast(img: Image.Image) -> Image.Image:
    base = _fit(img)
    rgb = F.to_rgb(img, 768)
    e = F.sobel(F.luminance(rgb))
    weak = ((e > 0.08) & (e < 0.30)).astype(np.float32)
    strong = (e >= 0.30).astype(np.float32)
    out = _heat(base, _resize_mask(strong, base.size), (60, 200, 90), 0.8)
    return _heat(out, _resize_mask(weak, base.size), (255, 80, 80), 0.9)


def panel_harmony(img: Image.Image, report: dict) -> Image.Image:
    w = PANEL_W
    out = Image.new("RGB", (w, 260), (24, 26, 32))
    d = ImageDraw.Draw(out)
    rgb = F.to_rgb(img, 384)
    hh, ss, vv = F.rgb_to_hsv(rgb)
    weight = (ss * vv).ravel()
    hist, _ = np.histogram(hh.ravel() * 360, bins=72, range=(0, 360), weights=weight)
    hist = hist / (hist.max() + 1e-9)
    cx, cy, r0, r1 = 120, 128, 40, 110
    for b in range(72):
        a0, a1 = b * 5, b * 5 + 5
        col = tuple(int(255 * c) for c in _hsv_to_rgb(b * 5 / 360, 0.85, 0.95))
        rr = r0 + (r1 - r0) * hist[b]
        d.pieslice([cx - rr, cy - rr, cx + rr, cy + rr], a0 - 90, a1 - 90, fill=col)
    d.ellipse([cx - r0 + 2, cy - r0 + 2, cx + r0 - 2, cy + r0 - 2], fill=(24, 26, 32))
    har = report["raw"]["harmony"]
    tmpl = har.get("template", "N")
    d.text((cx - 12, cy - 9), tmpl, fill="white", font=_font(18))
    # palette swatches: dominant colours (8-level quantisation, > 1 %)
    q = (rgb * 7).round().astype(np.int32)
    key = q[..., 0] * 64 + q[..., 1] * 8 + q[..., 2]
    counts = np.bincount(key.ravel(), minlength=512) / key.size
    top = [k for k in np.argsort(counts)[::-1] if counts[k] > 0.01][:8]
    x = 250
    for k in top:
        c = (int(k // 64 * 255 / 7), int((k // 8) % 8 * 255 / 7), int(k % 8 * 255 / 7))
        d.rectangle([x, 40, x + 36, 76], fill=c, outline=(60, 62, 70))
        d.text((x + 2, 80), f"{counts[k]:.0%}", fill=(200, 200, 210), font=_font(11))
        x += 40
        if x > w - 40:
            break
    col = report["raw"]["colorfulness"]
    d.text((250, 120), f"template {tmpl}  fit {har.get('fit', 0):.2f}", fill="white", font=_font(14))
    d.text((250, 142), f"colourfulness {col.get('hasler', 0):.0f}  variety {col.get('variety', 0):.0f}", fill="white", font=_font(14))
    d.text((250, 164), f"{len(top)} dominant colours", fill="white", font=_font(14))
    return out


def _hsv_to_rgb(h, s, v):
    i = int(h * 6) % 6
    f = h * 6 - int(h * 6)
    p, q, t = v * (1 - s), v * (1 - f * s), v * (1 - (1 - f) * s)
    return [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)][i]


def panel_edges(img: Image.Image, report: dict) -> Image.Image:
    base = _fit(img)
    w, h = base.size
    out = base.copy()
    d = ImageDraw.Draw(out, "RGBA")
    c = report["raw"]["experimental"]["edge_contact"]
    band = 6
    for side_name, box in (("left", [0, 0, band, h]), ("right", [w - band, 0, w, h]),
                           ("top", [0, 0, w, band]), ("bottom", [0, h - band, w, h])):
        cov = c[side_name]["coverage"]
        col = (255, 60, 60, 200) if cov > 0.05 else (80, 220, 120, 140)
        d.rectangle(box, fill=col)
    f = _font(14)
    d.rectangle([0, h - 24, w, h], fill=(0, 0, 0, 220))
    d.text((6, h - 21), "  ".join(f"{k} {c[k]['coverage']:.0%}/{c[k]['runs']}" for k in ("left", "right", "top", "bottom")),
           fill="white", font=f)
    return out


# --------------------------------------------------------------------------- #
# sheet
# --------------------------------------------------------------------------- #
def explain(image, mode: str = "ui", report: dict | None = None) -> Image.Image:
    img = Image.open(image).convert("RGB") if isinstance(image, str) else image.convert("RGB")
    r = report or beauty(img, mode)
    fac = r["factors"]
    rgb = F.to_rgb(img, 768)
    panels = [("original  ·  beauty %d" % r["score"], _fit(img))]
    panels.append((f"composition {fac.get('composition', 0):.2f}  ·  red = left/right disagree, dot = centre of mass", panel_composition(img, r, mode)))
    if "alignment" in fac:
        panels.append((f"alignment {fac['alignment']:.2f}  ·  the grid lines the layout is explained by", panel_alignment(img, r)))
    if "whitespace" in fac:
        q = (rgb * 15).round().astype(np.int32)
        key = q[..., 0] * 256 + q[..., 1] * 16 + q[..., 2]
        vals, counts = np.unique(key.ravel(), return_counts=True)
        bg = vals[counts.argmax()]
        bgc = np.array([bg // 256, (bg // 16) % 16, bg % 16]) / 15.0
        mask = (np.abs(rgb - bgc).sum(-1) < 0.12).astype(np.float32)
        panels.append((f"whitespace {fac['whitespace']:.2f}  ·  blue = counts as air ({r['raw']['whitespace']:.0%})", panel_mask(img, mask, (70, 130, 255), 0.55)))
    if "simplicity" in fac:
        e = (F.sobel(F.luminance(rgb)) > 0.15).astype(np.float32)
        cpx = r["raw"]["complexity"]
        panels.append((f"simplicity {fac['simplicity']:.2f}  ·  edges {cpx['edge_density']:.0%}, {cpx['dominant_colors']} colours, {cpx['jpeg_bpp']:.2f} B/px", panel_mask(img, e, (255, 170, 0), 0.9)))
    if "contrast" in fac:
        panels.append((f"contrast {fac['contrast']:.2f}  ·  green = crisp edges, red = weak figure–ground", panel_contrast(img)))
    panels.append((f"harmony {fac.get('harmony', 0):.2f}  ·  hue wheel, fitted template, dominant colours", panel_harmony(img, r)))
    panels.append(("edges  ·  red band = content touches the border (clipping?)", panel_edges(img, r)))

    cols = 2
    gap, title_h = 14, 24
    pw = PANEL_W
    heights = [p.height for _, p in panels]
    rows = (len(panels) + cols - 1) // cols
    row_h = [max(heights[i * cols:(i + 1) * cols]) for i in range(rows)]
    sheet = Image.new("RGB", (cols * (pw + gap) + gap, sum(hh + title_h + gap for hh in row_h) + gap + 30), (14, 16, 20))
    d = ImageDraw.Draw(sheet)
    d.text((gap, 8), f"beautiful · what the formula sees · mode {r['mode']} · score {r['score']}", fill=(230, 232, 236), font=_font(16))
    y = gap + 30
    for i, (title, p) in enumerate(panels):
        c, rr = i % cols, i // cols
        if c == 0 and i > 0:
            y += row_h[rr - 1] + title_h + gap
        x = gap + c * (pw + gap)
        d.text((x, y), title[:78], fill=(200, 204, 212), font=_font(13))
        sheet.paste(p, (x, y + title_h))
    return sheet
