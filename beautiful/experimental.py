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


def all_measurements(rgb: np.ndarray) -> dict:
    fc = feature_congestion(rgb)
    return {
        "feature_congestion": fc["feature_congestion"],
        "feature_congestion_parts": {k: v for k, v in fc.items() if k != "feature_congestion"},
        "contour_congestion": round(contour_congestion(rgb), 4),
        "edge_orientation_entropy": round(edge_orientation_entropy(rgb), 4),
        "anisotropy": round(anisotropy(rgb), 4),
        "sequence": round(sequence(rgb), 4),
    }
