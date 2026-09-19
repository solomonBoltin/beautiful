"""
beautiful/symmetry.py
-----------------
Score any image (UI screenshot, logo, drawing, artwork) for symmetry / balance
on a 1-100 scale, so an agent can iterate toward a more harmonious composition.

Public API
----------
    symmetry_score(image) -> int                  # 1..100
    symmetry_report(image) -> dict                # score + per-axis breakdown

`image` may be a file path, a PIL.Image, or an HxW / HxWx3 numpy array.

How the score is built
----------------------
1. Convert to grayscale, resize to a fixed working size (aspect-preserved
   letterbox is NOT used - we squash to square so mirror comparison is on
   the image's own frame, which is what a designer means by "is this
   balanced inside its canvas").
2. Build two representations:
     - tone   : blurred luminance (captures mass / large shapes)
     - edges  : Sobel gradient magnitude (captures structure, ignores flat fill)
3. For each transform T in {horizontal mirror, vertical mirror, 180 rotation}
   measure agreement between the image and T(image):
     sim = 1 - mean|A - T(A)| / (mean|A| + eps)      on edges (content-weighted)
     tone_sim = 1 - mean|A - T(A)|                    on tone
   The edge term is normalised by edge mass so that a mostly-blank canvas with
   one asymmetric element is punished, and a busy but symmetric canvas is not.
4. Balance: distance of the "visual centre of mass" (edge-weighted) from the
   geometric centre, per axis.
5. Composite:
     mirror = max(horizontal, vertical)   (a strong single axis is what humans
                                           perceive as "symmetric")
     score = 0.55*mirror + 0.15*rotational + 0.15*mean(h,v) + 0.15*balance
   then mapped through a gentle contrast curve to spread 1..100.
"""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageFilter

WORK = 256          # working resolution (square)
EPS = 1e-6


# --------------------------------------------------------------------------- #
# loading / preprocessing
# --------------------------------------------------------------------------- #
def _to_gray(image) -> np.ndarray:
    """Return float32 grayscale array in [0,1], WORK x WORK."""
    if isinstance(image, str):
        img = Image.open(image)
    elif isinstance(image, Image.Image):
        img = image
    elif isinstance(image, np.ndarray):
        arr = image
        if arr.dtype != np.uint8:
            arr = np.clip(arr * (255 if arr.max() <= 1.0 else 1), 0, 255).astype(np.uint8)
        img = Image.fromarray(arr)
    else:
        raise TypeError("image must be path, PIL.Image or numpy array")

    if img.mode in ("RGBA", "LA", "P"):
        # composite onto white so transparent logos behave like on a page
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.alpha_composite(img.convert("RGBA"))
        img = bg
    img = img.convert("L").resize((WORK, WORK), Image.LANCZOS)
    return np.asarray(img, dtype=np.float32) / 255.0


def _tone(g: np.ndarray) -> np.ndarray:
    pil = Image.fromarray((g * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))
    return np.asarray(pil, dtype=np.float32) / 255.0


def _edges(g: np.ndarray) -> np.ndarray:
    """Sobel gradient magnitude, lightly blurred, normalised to [0,1]."""
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    ky = kx.T
    gx = _conv2(g, kx)
    gy = _conv2(g, ky)
    mag = np.sqrt(gx * gx + gy * gy)
    pil = Image.fromarray(np.clip(mag / (mag.max() + EPS) * 255, 0, 255).astype(np.uint8))
    pil = pil.filter(ImageFilter.GaussianBlur(1.5))
    return np.asarray(pil, dtype=np.float32) / 255.0


def _conv2(a: np.ndarray, k: np.ndarray) -> np.ndarray:
    from scipy.signal import convolve2d
    return convolve2d(a, k, mode="same", boundary="symm")


# --------------------------------------------------------------------------- #
# symmetry measures
# --------------------------------------------------------------------------- #
def _corr(a: np.ndarray, b: np.ndarray) -> float:
    """Pearson correlation clipped to 0..1. Flat inputs count as fully similar."""
    a = a - a.mean(); b = b - b.mean()
    na, nb = np.sqrt((a * a).sum()), np.sqrt((b * b).sum())
    if na < 1e-4 or nb < 1e-4:
        return 1.0 if (na < 1e-4 and nb < 1e-4) else 0.0
    return float(np.clip((a * b).sum() / (na * nb), 0.0, 1.0))


def _sim_abs(a: np.ndarray, b: np.ndarray, scale: float) -> float:
    return float(np.clip(1.0 - np.abs(a - b).mean() / scale, 0.0, 1.0))


def _structure(g: np.ndarray) -> np.ndarray:
    """Coarse layout map: blur enough that text and chart internals dissolve
    into tonal blocks, so what remains is the arrangement of containers and
    their visual weight (contrast)."""
    pil = Image.fromarray((g * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
    return np.asarray(pil, dtype=np.float32) / 255.0


def _axis_score(gray: np.ndarray, tone: np.ndarray, edges: np.ndarray, transform, struct=None, mode="generic") -> float:
    # correlation on raw gray and on edges kills noise (uncorrelated with its flip)
    c_gray = _corr(gray, transform(gray))
    c_edge = _corr(edges, transform(edges))
    t_abs = _sim_abs(tone, transform(tone), 0.20)
    fine = 0.45 * c_gray + 0.35 * c_edge + 0.20 * t_abs
    if struct is None:
        s = fine
    else:
        # structural scale: layout boxes + visual weight, tolerant of glyph detail
        c_struct = _corr(struct, transform(struct))
        c_sedge = _corr(_edges(struct), transform(_edges(struct)))
        coarse = 0.6 * c_struct + 0.4 * c_sedge
        s = (0.2 * fine + 0.8 * coarse) if mode == "ui" else (0.5 * fine + 0.5 * coarse)
    # sharpen: one visibly broken element should cost more than a few points
    return float(s ** (1.3 if mode == "ui" else 2.5))


def _local_symmetry(gray: np.ndarray, n: int = 3) -> float:
    """Mean mirror symmetry inside an n x n grid of tiles, weighted by tile
    contrast. Rewards UIs / artworks built from symmetric components even when
    the whole canvas is not mirror-symmetric."""
    h, w = gray.shape
    th, tw = h // n, w // n
    num = den = 0.0
    for i in range(n):
        for j in range(n):
            t = gray[i * th:(i + 1) * th, j * tw:(j + 1) * tw]
            wgt = float(t.std()) + 1e-3
            s = max(_corr(t, np.fliplr(t)), _corr(t, np.flipud(t)))
            num += wgt * s
            den += wgt
    return num / den


def _balance(tone: np.ndarray, mode: str = "generic") -> tuple[float, float, float]:
    """(balance_score, dx, dy): visual mass = deviation from the border colour."""
    h, w = tone.shape
    hist, bins = np.histogram(tone, bins=32, range=(0, 1))
    k = int(hist.argmax())
    bg = float((bins[k] + bins[k + 1]) / 2)          # dominant tone = background
    m = np.abs(tone - bg) + EPS
    ys, xs = np.mgrid[0:h, 0:w]
    cx = (xs * m).sum() / m.sum()
    cy = (ys * m).sum() / m.sum()
    dx = (cx - (w - 1) / 2) / (w / 2)
    dy = (cy - (h - 1) / 2) / (h / 2)
    # screens scroll, so being top-heavy within a viewport is normal
    off = np.hypot(dx, 0.4 * dy) if mode == "ui" else np.hypot(dx, dy)
    return float(np.exp(-(off / 0.30) ** 2)), float(dx), float(dy)


def _curve(x: float) -> float:
    x = np.clip(x, 0, 1)
    return float(1 / (1 + np.exp(-9 * (x - 0.55))))


# --------------------------------------------------------------------------- #
# public API
# --------------------------------------------------------------------------- #
def symmetry_report(image, mode: str = "generic") -> dict:
    """mode: "generic" (art, logos, anything) or "ui" (screens: left/right symmetry
    dominates, top/bottom is a weak secondary cue, glyph detail is tolerated)."""
    g = _to_gray(image)
    tone = _tone(g)
    edges = _edges(g)

    st = _structure(g)
    h = _axis_score(g, tone, edges, np.fliplr, st, mode)
    v = _axis_score(g, tone, edges, np.flipud, st, mode)
    r = _axis_score(g, tone, edges, lambda a: np.rot90(a, 2), st, mode)
    loc = _local_symmetry(st if mode == "ui" else g)
    bal, dx, dy = _balance(tone, mode)

    if mode == "ui":
        mirror = 0.8 * h + 0.2 * v
        raw = 0.55 * mirror + 0.05 * r + 0.15 * loc + 0.25 * bal
    else:
        mirror = max(h, v)
        raw = 0.50 * mirror + 0.10 * (h + v) / 2 + 0.05 * r + 0.15 * loc + 0.20 * bal
    score = int(round(1 + 99 * _curve(raw)))

    dominant = "horizontal" if h >= v else "vertical"
    hints = []
    if bal < 0.6:
        side = ("right" if dx > 0 else "left") if abs(dx) > abs(dy) else ("bottom" if dy > 0 else "top")
        hints.append(f"visual weight sits toward the {side}; shift or counterweight it")
    if mirror < 0.5:
        hints.append("no strong mirror axis; align key elements to the centre line or use a grid")
    elif h < 0.5 <= v:
        hints.append("top/bottom symmetry is fine but left/right halves differ")
    elif v < 0.5 <= h:
        hints.append("left/right symmetry is fine but top/bottom halves differ")
    if loc < 0.4:
        hints.append("individual components are themselves asymmetric; tidy internal alignment")

    return {
        "score": score,
        "raw": round(float(raw), 4),
        "horizontal_mirror": round(h, 4),
        "vertical_mirror": round(v, 4),
        "rotational_180": round(r, 4),
        "local_symmetry": round(loc, 4),
        "balance": round(bal, 4),
        "mass_offset": {"dx": round(dx, 3), "dy": round(dy, 3)},
        "dominant_axis": dominant,
        "mode": mode,
        "hints": hints,
    }


def symmetry_score(image, mode: str = "generic") -> int:
    """Return an integer 1..100: 100 = perfectly symmetric / balanced.
    Use mode="ui" for screenshots of interfaces."""
    return symmetry_report(image, mode)["score"]


if __name__ == "__main__":
    import sys, json
    for p in sys.argv[1:]:
        print(p, json.dumps(symmetry_report(p), indent=2))
