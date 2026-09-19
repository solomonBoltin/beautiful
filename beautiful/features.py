"""
beautiful.features
------------------
Isolated, pixel-only beauty factors. Every function takes a numpy RGB array
(H x W x 3, float32 in [0,1]) and returns raw measurements; normalisation to
0..1 "goodness" happens in core.py, where the target ranges are documented.

Each factor cites the work it descends from (see README "Research").
"""
from __future__ import annotations

import io
import numpy as np
from PIL import Image, ImageFilter
from scipy.signal import convolve2d

EPS = 1e-6


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def to_rgb(image, size: int = 512) -> np.ndarray:
    """Load path / PIL / ndarray -> float32 RGB, longest side = size."""
    if isinstance(image, str):
        img = Image.open(image)
    elif isinstance(image, Image.Image):
        img = image
    elif isinstance(image, np.ndarray):
        arr = image if image.dtype == np.uint8 else np.clip(image * (255 if image.max() <= 1 else 1), 0, 255).astype(np.uint8)
        img = Image.fromarray(arr)
    else:
        raise TypeError("image must be a path, PIL.Image or numpy array")
    if img.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.alpha_composite(img.convert("RGBA"))
        img = bg
    img = img.convert("RGB")
    w, h = img.size
    s = size / max(w, h)
    if s < 1:
        img = img.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    return np.asarray(img, dtype=np.float32) / 255.0


def luminance(rgb: np.ndarray) -> np.ndarray:
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def sobel(g: np.ndarray) -> np.ndarray:
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    gx = convolve2d(g, kx, mode="same", boundary="symm")
    gy = convolve2d(g, kx.T, mode="same", boundary="symm")
    return np.sqrt(gx * gx + gy * gy)


def rgb_to_hsv(rgb: np.ndarray):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = rgb.max(-1); mn = rgb.min(-1); d = mx - mn
    h = np.zeros_like(mx)
    m = d > EPS
    rc = np.where(m, (mx - r) / (d + EPS), 0); gc = np.where(m, (mx - g) / (d + EPS), 0); bc = np.where(m, (mx - b) / (d + EPS), 0)
    h = np.where(mx == r, bc - gc, np.where(mx == g, 2 + rc - bc, 4 + gc - rc))
    h = (h / 6.0) % 1.0
    s = np.where(mx > EPS, d / (mx + EPS), 0)
    return h, s, mx


# --------------------------------------------------------------------------- #
# 1. colorfulness  (Hasler & Süsstrunk 2003)
# --------------------------------------------------------------------------- #
def colorfulness(rgb: np.ndarray) -> float:
    R, G, B = (rgb[..., i] * 255 for i in range(3))
    rg = R - G
    yb = 0.5 * (R + G) - B
    s = np.sqrt(rg.std() ** 2 + yb.std() ** 2)
    m = np.sqrt(rg.mean() ** 2 + yb.mean() ** 2)
    return {"hasler": float(s + 0.3 * m),      # ~0 (grey) .. ~110 (very colourful)
            "variety": float(s),               # spread of the colour cloud
            "mean_chroma": float(m)}           # how saturated the average pixel is


# --------------------------------------------------------------------------- #
# 2. colour harmony  (Cohen-Or et al. 2006 hue templates, after Matsuda)
# --------------------------------------------------------------------------- #
_TEMPLATES = {   # name: list of (centre offset deg, width deg)
    "i": [(0, 18)],
    "V": [(0, 93.6)],
    "L": [(0, 18), (90, 79.2)],
    "I": [(0, 18), (180, 18)],
    "T": [(0, 180)],
    "Y": [(0, 93.6), (180, 18)],
    "X": [(0, 93.6), (180, 93.6)],
}


def color_harmony(rgb: np.ndarray) -> dict:
    """Best-fit harmonic template: share of saturated hue mass inside the
    template's sectors, maximised over rotation. Wider templates are
    penalised so that 'T' (half the wheel) doesn't win by default."""
    h, s, v = rgb_to_hsv(rgb)
    w = (s * v).ravel()
    hd = (h.ravel() * 360.0)
    sat_mass = float(w.sum())
    if sat_mass < 0.02 * w.size:            # essentially greyscale -> 'N' template
        return {"template": "N", "fit": 1.0, "chroma_share": sat_mass / w.size}
    hist, _ = np.histogram(hd, bins=72, range=(0, 360), weights=w)
    hist = hist / (hist.sum() + EPS)
    best = ("?", 0.0)
    for name, sectors in _TEMPLATES.items():
        width = sum(wd for _, wd in sectors)
        for rot in range(0, 360, 5):
            cover = 0.0
            for off, wd in sectors:
                c = (rot + off) % 360
                lo, hi = c - wd / 2, c + wd / 2
                idx = np.arange(72) * 5 + 2.5
                inside = ((idx - lo) % 360) <= wd
                cover += hist[inside].sum()
            score = cover - 0.25 * (width / 360.0)
            if score > best[1]:
                best = (name, score)
    return {"template": best[0], "fit": float(np.clip(best[1] + 0.0, 0, 1)), "chroma_share": sat_mass / w.size}


# --------------------------------------------------------------------------- #
# 3. visual complexity / clutter
#    edge density (Mack & Oliva 2004; Rosenholtz 2007), JPEG bytes-per-pixel
#    (Rosenholtz: file size tracks subband entropy; Rigau: Kolmogorov proxy),
#    dominant colours (Miniukovich & De Angeli 2014/15)
# --------------------------------------------------------------------------- #
def complexity(rgb: np.ndarray) -> dict:
    g = luminance(rgb)
    e = sobel(g)
    edge_density = float((e > 0.15).mean())
    buf = io.BytesIO()
    Image.fromarray((rgb * 255).astype(np.uint8)).save(buf, format="JPEG", quality=75)
    bpp = len(buf.getvalue()) / (rgb.shape[0] * rgb.shape[1])
    q = (rgb * 7).round().astype(np.int32)                 # 8 levels per channel
    key = q[..., 0] * 64 + q[..., 1] * 8 + q[..., 2]
    counts = np.bincount(key.ravel(), minlength=512) / key.size
    dominant = int((counts > 0.01).sum())
    return {"edge_density": edge_density, "jpeg_bpp": float(bpp), "dominant_colors": dominant}


# --------------------------------------------------------------------------- #
# 4. white space  (Miniukovich & De Angeli 2015 "white space" metric)
# --------------------------------------------------------------------------- #
def whitespace(rgb: np.ndarray) -> float:
    q = (rgb * 15).round().astype(np.int32)
    key = q[..., 0] * 256 + q[..., 1] * 16 + q[..., 2]
    vals, counts = np.unique(key.ravel(), return_counts=True)
    bg = vals[counts.argmax()]
    bgc = np.array([bg // 256, (bg // 16) % 16, bg % 16]) / 15.0
    dist = np.abs(rgb - bgc).sum(-1)
    return float((dist < 0.12).mean())


# --------------------------------------------------------------------------- #
# 5. alignment / grid quality  (Miniukovich 2015 grid quality; Ngo 2003 regularity)
#    Edge energy projected on x and y: aligned layouts concentrate their
#    vertical edges on a few columns and horizontal edges on a few rows.
# --------------------------------------------------------------------------- #
def alignment(rgb: np.ndarray, min_run: int = 20) -> dict:
    """Only long edge runs count (container borders, column/row edges); text
    produces short runs and is ignored. Score = share of structural energy
    captured by the strongest few lines per axis, i.e. how few grid lines
    explain the layout. Pages with almost no structural lines get a low prior."""
    g = luminance(rgb)
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    vert = np.abs(convolve2d(g, kx, mode="same", boundary="symm")) > 0.08
    horz = np.abs(convolve2d(g, kx.T, mode="same", boundary="symm")) > 0.08
    out = {}
    for name, m, k in (("x", vert, 8), ("y", horz.T, 16)):
        prof = np.zeros(m.shape[1])
        pad = np.zeros((1, m.shape[1]), dtype=int)
        d = np.diff(np.vstack([pad, m.astype(int), pad]), axis=0)
        for j in range(m.shape[1]):
            st = np.where(d[:, j] == 1)[0]; en = np.where(d[:, j] == -1)[0]
            if st.size:
                runs = en - st
                prof[j] = runs[runs >= min_run].sum()
        density = prof.sum() / m.size
        if density < 0.003:
            out[name + "_alignment"] = 0.30
            out[name + "_line_density"] = float(density)
            continue
        p = np.convolve(prof, np.ones(3), mode="same"); p /= p.sum()
        out[name + "_alignment"] = float(np.sort(p)[::-1][:k].sum())
        out[name + "_line_density"] = float(density)
    return out


# --------------------------------------------------------------------------- #
# 6. figure-ground contrast  (Miniukovich; Reber et al. fluency)
# --------------------------------------------------------------------------- #
def contrast(rgb: np.ndarray) -> dict:
    g = luminance(rgb)
    e = sobel(g)
    strong = e[e > 0.08]
    edge_contrast = float(np.percentile(strong, 75)) if strong.size else 0.0
    rms = float(g.std())
    return {"edge_contrast": edge_contrast, "rms_contrast": rms}


# --------------------------------------------------------------------------- #
# 7. natural-scene statistics: fractal dimension (Taylor; Spehar) and
#    Fourier slope (Graham & Field; Redies) — used in art/photo mode
# --------------------------------------------------------------------------- #
def fractal_dimension(rgb: np.ndarray) -> float:
    g = luminance(rgb)
    e = sobel(g) > 0.15
    n = 2 ** int(np.floor(np.log2(min(e.shape))))
    e = e[:n, :n]
    sizes = [n // (2 ** k) for k in range(1, int(np.log2(n)) - 1)]
    counts = []
    for s in sizes:
        blocks = e.reshape(n // s, s, n // s, s).any(axis=(1, 3))
        counts.append(max(blocks.sum(), 1))
    coeffs = np.polyfit(np.log(1 / np.array(sizes, dtype=float)), np.log(counts), 1)
    return float(coeffs[0])


def fourier_slope(rgb: np.ndarray) -> float:
    g = luminance(rgb)
    n = min(g.shape)
    g = g[:n, :n] - g[:n, :n].mean()
    F = np.abs(np.fft.fftshift(np.fft.fft2(g))) ** 2
    y, x = np.indices(F.shape)
    r = np.hypot(x - n / 2, y - n / 2).astype(int)
    radial = np.bincount(r.ravel(), F.ravel()) / (np.bincount(r.ravel()) + EPS)
    f = np.arange(len(radial))
    m = (f > 2) & (f < n / 2)
    if m.sum() < 8:
        return -2.0
    slope = np.polyfit(np.log(f[m]), np.log(radial[m] + EPS), 1)[0]
    return float(slope)


# --------------------------------------------------------------------------- #
# 8. rule of thirds (Datta et al. 2006): edge/saliency mass near the four
#    power points; art/photo mode only
# --------------------------------------------------------------------------- #
def rule_of_thirds(rgb: np.ndarray) -> float:
    g = luminance(rgb)
    e = sobel(g)
    e = e / (e.sum() + EPS)
    H, W = e.shape
    yy, xx = np.mgrid[0:H, 0:W]
    ys, xs = yy / H, xx / W
    best = 0.0
    for py in (1 / 3, 2 / 3):
        for px in (1 / 3, 2 / 3):
            wgt = np.exp(-(((xs - px) ** 2 + (ys - py) ** 2) / (2 * 0.12 ** 2)))
            best = max(best, float((e * wgt).sum()))
    return best            # share of edge mass within ~1/8 of a power point
