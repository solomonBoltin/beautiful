"""
beautiful.experimental
----------------------
Measurements with strong literature support that are NOT yet weighted in the score.
They are computed on every call and reported under ``raw["experimental"]`` so that
(a) a calibration run (research/calibrate.py) can decide their weights from human
ratings instead of from taste, and (b) agents and linters can already read them.

All functions take a float32 RGB array in [0, 1] (see features.to_rgb) and return
raw, unnormalised numbers. Each cites what it descends from and how it simplifies it.
"""
from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter, uniform_filter, zoom

from .features import EPS, luminance, sobel


def _lab_ab(rgb: np.ndarray):
    """Cheap opponent chroma channels (Hasler–Süsstrunk rg / yb), as a stand-in for CIELab a/b."""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    return r - g, 0.5 * (r + g) - b


def feature_congestion(rgb: np.ndarray, sigma: float = 3.0, levels: int = 3) -> dict:
    """Rosenholtz, Li & Nakano (2007) *Feature Congestion*, simplified.

    The original measures, at each scale of a Gaussian pyramid, the local covariance of
    colour, luminance-contrast and orientation features, takes the volume of the resulting
    covariance ellipsoid, pools over space, and combines the three feature types. The idea:
    the more the local features already vary, the harder it is to add a salient item — the
    display is cluttered.

    This version keeps that structure with cheap estimators:
      colour       : sqrt(det) of the local 2x2 covariance of the (rg, yb) opponent channels
      contrast     : local std of band-passed luminance (a DoG contrast response)
      orientation  : 1 − structure-tensor coherence where there is gradient energy
    each averaged over pixels and pyramid levels, then combined by geometric mean.
    Returns the combined value and the three parts. Higher = more cluttered.
    """
    parts = {"color": [], "contrast": [], "orientation": []}
    img = rgb
    for _ in range(levels):
        a, b = _lab_ab(img)
        m_a, m_b = gaussian_filter(a, sigma), gaussian_filter(b, sigma)
        c_aa = gaussian_filter(a * a, sigma) - m_a * m_a
        c_bb = gaussian_filter(b * b, sigma) - m_b * m_b
        c_ab = gaussian_filter(a * b, sigma) - m_a * m_b
        det = np.clip(c_aa * c_bb - c_ab * c_ab, 0, None)
        parts["color"].append(float(np.sqrt(det).mean()))

        lum = luminance(img)
        band = gaussian_filter(lum, 1.0) - gaussian_filter(lum, 3.0)
        mu = gaussian_filter(band, sigma)
        var = np.clip(gaussian_filter(band * band, sigma) - mu * mu, 0, None)
        parts["contrast"].append(float(np.sqrt(var).mean()))

        gy, gx = np.gradient(lum)
        jxx, jyy, jxy = (gaussian_filter(gx * gx, sigma), gaussian_filter(gy * gy, sigma),
                         gaussian_filter(gx * gy, sigma))
        tr = jxx + jyy
        lam = np.sqrt(np.clip((jxx - jyy) ** 2 + 4 * jxy ** 2, 0, None))
        coherence = lam / (tr + EPS)
        weight = tr / (tr.mean() + EPS)
        parts["orientation"].append(float(((1 - coherence) * weight).mean()))

        if min(img.shape[:2]) < 64:
            break
        img = zoom(img, (0.5, 0.5, 1), order=1)
    color, contrast, orient = (float(np.mean(v)) for v in parts.values())
    combined = float((max(color, EPS) * max(contrast, EPS) * max(orient, EPS)) ** (1 / 3))
    return {"feature_congestion": round(combined, 5), "color": round(color, 5),
            "contrast": round(contrast, 5), "orientation": round(orient, 5)}


def contour_congestion(rgb: np.ndarray, radius: int = 4, thresh: float = 0.12) -> float:
    """Miniukovich & De Angeli (2014) *contour congestion*, as a proxy.

    They count contour pixels that have another contour within a small distance — crowded
    contours are hard to group. Here: the share of edge pixels whose (2r+1)² neighbourhood
    is itself dense with edges. 0 = every contour has room, 1 = contours on top of contours.
    """
    g = luminance(rgb)
    edges = (sobel(g) > thresh).astype(np.float32)
    if edges.sum() < 1:
        return 0.0
    local = uniform_filter(edges, size=2 * radius + 1)
    return float((local[edges > 0]).mean())


def edge_orientation_entropy(rgb: np.ndarray, bins: int = 24) -> float:
    """Redies et al. — first-order edge-orientation entropy (Aesthetics Toolbox).

    Magnitude-weighted histogram of gradient orientation over 0..180°, Shannon entropy,
    normalised to [0, 1] by log(bins). Artworks and designed images tend to sit high (all
    orientations present, no dominant direction); pure grids sit low.
    """
    g = luminance(rgb)
    gy, gx = np.gradient(g)
    mag = np.hypot(gx, gy)
    ang = np.mod(np.arctan2(gy, gx), np.pi)
    hist, _ = np.histogram(ang, bins=bins, range=(0, np.pi), weights=mag)
    p = hist / (hist.sum() + EPS)
    p = p[p > 0]
    return float(-(p * np.log(p)).sum() / np.log(bins))


def sequence(rgb: np.ndarray) -> float:
    """Ngo, Teo & Byrne (2003) *sequence*, from pixels.

    Visual weight should decrease along the Western reading path UL → UR → LL → LR
    (quadrant weights 4, 3, 2, 1). Here weight = edge mass per quadrant; the score is the
    rank agreement (Spearman-style) between the observed ordering and the ideal one,
    mapped to [0, 1]. Only meaningful for left-to-right interfaces.
    """
    g = luminance(rgb)
    e = sobel(g)
    h, w = e.shape
    q = np.array([e[: h // 2, : w // 2].sum(), e[: h // 2, w // 2:].sum(),
                  e[h // 2:, : w // 2].sum(), e[h // 2:, w // 2:].sum()])
    if q.sum() < EPS:
        return 0.5
    ideal = np.array([4, 3, 2, 1])
    ranks = q.argsort().argsort() + 1  # 1 = lightest .. 4 = heaviest
    d = ranks - ideal
    rho = 1 - 6 * float((d * d).sum()) / (4 * (16 - 1))
    return float((rho + 1) / 2)


def anisotropy(rgb: np.ndarray) -> float:
    """Redies et al. — anisotropy of the gradient-orientation histogram (std of the
    magnitude-weighted orientation histogram, normalised). Low = orientations are used
    evenly (many artworks); high = one direction dominates (stripes, text blocks)."""
    g = luminance(rgb)
    gy, gx = np.gradient(g)
    mag = np.hypot(gx, gy)
    ang = np.mod(np.arctan2(gy, gx), np.pi)
    hist, _ = np.histogram(ang, bins=16, range=(0, np.pi), weights=mag)
    p = hist / (hist.sum() + EPS)
    return float(p.std() / (1 / 16))


def hierarchy(rgb: np.ndarray) -> float:
    """Coarse-structure share: how much of the page's luminance variation survives a blur of
    ~4% of the width. A designed page has structure at the scale of blocks — a hero, a coloured
    section, a card grid, a large heading — so a good part of its contrast is coarse; a page that
    is only running text (a plain link list, an unstyled document) is uniform grey at that scale
    and the share is low. Std of the blurred luminance over std of the original, in [0, 1].
    Not a beauty measure on its own (a lopsided page has coarse structure too); one of the
    hierarchy cues in the fitted `ui` formula. See research/FIT.md."""
    g = luminance(rgb)
    fine = float(g.std()) + EPS
    coarse = float(gaussian_filter(g, sigma=max(1.0, g.shape[1] / 25.0)).std())
    return float(min(1.0, coarse / fine))


def edge_contact(rgb: np.ndarray, band: int = 3, thresh: float = 0.12) -> dict:
    """How much content touches each edge of the viewport.

    For each border, the share of rows (left/right) or columns (top/bottom) whose outermost
    `band` pixels contain a luminance edge. Designed pages keep a margin, so the side bands are
    quiet; content that is *cut off* by the viewport (horizontal overflow, an element wider than
    the screen) produces edges right at the border along its whole height. Full-bleed images
    also touch the edges, but softly and on all sides, and they rarely carry sharp structure in
    the last three pixels. Used as a defect signal (see core.py), not as beauty.
    """
    g = luminance(rgb)
    e = sobel(g) > thresh
    h, w = e.shape

    def side(line):  # line: bool per row/col — coverage, and how fragmented the contact is
        cov = float(line.mean())
        runs = int((np.diff(np.concatenate([[0], line.astype(int), [0]])) == 1).sum())
        return {"coverage": round(cov, 4), "runs": runs}

    return {
        "left": side(e[:, :band].any(axis=1)), "right": side(e[:, w - band:].any(axis=1)),
        "top": side(e[:band, :].any(axis=0)), "bottom": side(e[h - band:, :].any(axis=0)),
    }


def all_measurements(rgb: np.ndarray) -> dict:
    fc = feature_congestion(rgb)
    return {
        "edge_contact": edge_contact(rgb),
        "feature_congestion": fc["feature_congestion"],
        "feature_congestion_parts": {k: v for k, v in fc.items() if k != "feature_congestion"},
        "contour_congestion": round(contour_congestion(rgb), 4),
        "edge_orientation_entropy": round(edge_orientation_entropy(rgb), 4),
        "anisotropy": round(anisotropy(rgb), 4),
        "sequence": round(sequence(rgb), 4),
        "hierarchy": round(hierarchy(rgb), 4),
    }


# --------------------------------------------------------------------------- #
# Corner-radius coherence (logo / icon marks).  Design systems keep one radius scale; a mark
# whose strokes end in different caps (a pill next to a squared-off foot) reads as unfinished.
# For every flat-coloured shape we take the corners of its bounding box that face the background,
# read the corner radius from how far the shape stays from that corner (a rounded corner of
# radius r keeps the shape r(√2−1) away along the diagonal) and express it relative to the
# shape's stroke thickness (twice the largest inscribed disc).  Corners with a radius larger
# than the stroke are bends (an arch), not caps, and are left out.  Coherence is 1.0 when
# every shape's cap radius sits on the same scale, and falls with the worst outlier.
# --------------------------------------------------------------------------- #
def corner_coherence(rgb: np.ndarray, min_area: int = 40) -> dict:
    from scipy import ndimage
    H, W = rgb.shape[:2]
    q = (rgb * 7).round()
    key = (q[..., 0] * 64 + q[..., 1] * 8 + q[..., 2]).astype(np.int64)
    vals, counts = np.unique(key, return_counts=True)
    order = np.argsort(-counts)
    bg_col = np.array([vals[order[0]] // 64, (vals[order[0]] // 8) % 8, vals[order[0]] % 8]) / 7.0
    is_bg = np.abs(rgb - bg_col).sum(-1) < 0.25
    shapes = []
    for v, c in zip(vals[order[1:]], counts[order[1:]]):
        if c < 0.002 * H * W:
            break
        col = np.array([v // 64, (v // 8) % 8, v % 8]) / 7.0
        if np.abs(col - bg_col).sum() < 0.3:
            continue                                       # anti-aliased shades of the background
        mask = np.abs(rgb - col).sum(-1) < 0.25
        lab, n = ndimage.label(mask)
        for i in range(1, n + 1):
            comp = lab == i
            area = int(comp.sum())
            if area < min_area:
                continue
            ys, xs = np.where(comp)
            x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
            if x1 - x0 < 4 or y1 - y0 < 4 or x0 == 0 or y0 == 0 or x1 == W - 1 or y1 == H - 1:
                continue                                   # framing (canvas corners, a full-bleed tile), not a mark
            dt = ndimage.distance_transform_edt(comp)
            t = 2.0 * float(dt.max())
            if t < 4:
                continue
            caps = []
            win = max(3, int(round(0.35 * t))); big = max(4, int(round(1.2 * t)))
            for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
                d = float(np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2).min())
                r = d / (np.sqrt(2) - 1)
                if r > 0.65 * t:
                    continue                               # a bend, not a cap
                ya, yb = max(0, cy - big), min(H, cy + big + 1); xa, xb = max(0, cx - big), min(W, cx + big + 1)
                if 2.0 * float(dt[ya:yb, xa:xb].max()) < 0.8 * t:
                    continue                               # the stroke thins out here (a tip, a taper): not a cap
                ya, yb = max(0, cy - win), min(H, cy + win + 1); xa, xb = max(0, cx - win), min(W, cx + win + 1)
                outside = ~comp[ya:yb, xa:xb]
                if outside.sum() and (~is_bg[ya:yb, xa:xb] & outside).mean() > 0.30:
                    continue                               # the corner is cut by another shape, not designed
                caps.append(r / t)
            if len(caps) >= 2 and (max(caps) - min(caps)) <= 0.15:
                shapes.append({"rho": float(np.mean(caps)), "t": round(t, 1), "box": [int(x0), int(y0), int(x1), int(y1)],
                               "colour": [round(float(x), 2) for x in col], "caps": len(caps)})
    if len(shapes) < 2:
        return {"score": 1.0, "shapes": shapes, "median": None, "outliers": []}
    med = float(np.median([s["rho"] for s in shapes]))
    for s in shapes:
        s["dev"] = round(abs(s["rho"] - med), 3)
    worst = max(s["dev"] for s in shapes)
    outliers = [s for s in shapes if s["dev"] > 0.12]
    score = float(np.clip(1.0 - (worst - 0.12) / 0.30, 0.0, 1.0))
    return {"score": round(score, 3), "median": round(med, 3), "shapes": shapes, "outliers": outliers}
