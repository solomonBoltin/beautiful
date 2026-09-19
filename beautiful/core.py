"""
beautiful.core
--------------
beauty(image, mode) -> dict with the final 1..100 number and every factor.

The number is a weighted sum of factor "goodness" values in 0..1, each mapped
from a raw measurement through a target curve (peak = the range the research
says people prefer), then spread over 1..100. Weights differ by mode:

  ui    : screenshots of interfaces. Left/right composition and alignment
          dominate; simplicity, white space and restrained colour are rewarded
          (Reinecke & Gajos 2013; Miniukovich & De Angeli 2015; Ngo 2003).
  art   : paintings, photos, posters. Composition still matters, but so do
          colour harmony, moderate complexity, natural-scene statistics
          (fractal dimension 1.3–1.5, Fourier slope −2…−3) and rule of thirds
          (Taylor; Spehar; Redies; Datta 2006).
  logo  : marks and icons: symmetry, balance, economy of colour and form.

Nothing here is learned from a dataset; every term is an explicit, inspectable
formula, so an agent can read the breakdown and know what to change.
"""
from __future__ import annotations

import numpy as np
from . import experimental as X
from . import features as F
from .symmetry import symmetry_report
from . import web as W

# --------------------------------------------------------------------------- #
# target curves
# --------------------------------------------------------------------------- #
def bell(x, centre, width):
    """1 at centre, falls off as a Gaussian with the given half-width."""
    return float(np.exp(-((x - centre) / width) ** 2))


def ramp(x, lo, hi):
    """0 at lo, 1 at hi (or the reverse if lo > hi), linear in between."""
    if lo > hi:
        return float(np.clip((lo - x) / (lo - hi), 0, 1))
    return float(np.clip((x - lo) / (hi - lo), 0, 1))


def spread(raw: float) -> int:
    """0..1 weighted sum -> 1..100 with a mild S-curve so the middle isn't mush."""
    s = 1 / (1 + np.exp(-8 * (raw - 0.55)))
    return int(round(1 + 99 * s))


WEIGHTS = {
    "ui":   dict(composition=0.28, alignment=0.16, simplicity=0.14, whitespace=0.10,
                 harmony=0.10, colorfulness=0.06, contrast=0.10, local=0.06),
    "art":  dict(composition=0.18, harmony=0.16, colorfulness=0.10, simplicity=0.14,
                 contrast=0.10, fractal=0.10, fourier=0.10, thirds=0.12),
    "logo": dict(composition=0.40, simplicity=0.20, harmony=0.12, whitespace=0.08,
                 contrast=0.10, economy=0.10),
}


MODES = ["ui", "art", "logo", "web", "classic"]


def beauty(image, mode: str = "ui") -> dict:
    """mode: ui (fitted to acclaimed design, degraded twins and human ratings — the default),
    art, logo, web (crowd-appeal model), classic (the literature-weighted ui formula)."""
    if mode == "ui":
        # the fitted formula (beautiful/model.py, research/fit_ui.py) consumes the classic
        # measurements, so compute those first and replace the number, factors and hints
        r = beauty(image, "classic")
        from .model import fitted_ui, model
        if model() is None:
            r["mode"] = "ui"
            return r
        f = fitted_ui(r["raw"])
        keep = [h for h in r["hints"] if h.startswith("clipping?")]
        r.update({"score": max(1, f["score"] - sum(r.get("penalties", {}).values())), "mode": "ui",
                  "factors": f["factors"], "weights": f["weights"], "weighted_sum": f["weighted_sum"],
                  "hints": keep + f["hints"], "classic": {"score": r["score"], "factors": r["factors"]}, "model": f["model"]})
        return r
    if mode == "web":
        # the model calibrated on human ratings of websites (beautiful/web.py) — it consumes the
        # ui measurements, so compute those first and then replace the number and the hints
        r = beauty(image, "classic")
        w = W.web_score(r["factors"], r["raw"])
        r.update({"score": w["score"], "mode": "web", "weights": None, "weighted_sum": None,
                  "hints": w["hints"] or ["nothing stands out against rated-high pages"], "web": w})
        return r
    if mode == "classic":
        mode = "ui"  # the literature-weighted formula, computed below under its old name
    if mode not in WEIGHTS:
        raise ValueError(f"mode must be one of {MODES}")
    rgb = F.to_rgb(image, 768)

    # ---- raw measurements -------------------------------------------------
    sym = symmetry_report(image, "ui" if mode == "ui" else "generic")
    col = F.colorfulness(rgb)
    har = F.color_harmony(rgb)
    cpx = F.complexity(rgb)
    ws = F.whitespace(rgb)
    ali = F.alignment(rgb)
    con = F.contrast(rgb)
    raw = dict(symmetry=sym, colorfulness=col, harmony=har, complexity=cpx,
               whitespace=ws, alignment=ali, contrast=con)
    # Literature-backed measurements that carry no weight yet (see experimental.py and
    # research/CALIBRATION.md): reported so calibration and linters can use them.
    raw["experimental"] = X.all_measurements(F.to_rgb(image, 384))
    if mode == "art":
        raw["fractal_dimension"] = F.fractal_dimension(rgb)
        raw["fourier_slope"] = F.fourier_slope(rgb)
        raw["rule_of_thirds"] = F.rule_of_thirds(rgb)

    # ---- goodness 0..1 per factor ---------------------------------------
    g = {}
    g["composition"] = sym["score"] / 100.0                      # symmetry + balance
    g["local"] = sym["local_symmetry"]
    g["alignment"] = 0.65 * ali["x_alignment"] + 0.35 * ali["y_alignment"]

    if mode == "ui":
        # Reinecke & Gajos: appeal falls as complexity rises; Miniukovich:
        # fewer dominant colours and lower edge density read as cleaner.
        g["simplicity"] = (0.4 * ramp(cpx["edge_density"], 0.22, 0.05)
                           + 0.35 * ramp(cpx["jpeg_bpp"], 0.16, 0.04)
                           + 0.25 * ramp(cpx["dominant_colors"], 9, 2))
        # air is good (Miniukovich 2015; the calibration set agrees): a ramp up to ~55 %
        # background, a plateau through the airy heroes people love (Apple 67 %, Medium 84 %),
        # and a fall only when the viewport is essentially empty (unstyled pages).
        g["whitespace"] = ramp(ws, 0.20, 0.55) * (1.0 if ws <= 0.90 else ramp(ws, 0.985, 0.90))
        g["colorfulness"] = bell(col["variety"], 25, 45)          # restrained palette (one bold hue is fine)
        g["contrast"] = ramp(con["edge_contrast"], 0.30, 0.80)    # crisp figure–ground
    elif mode == "art":
        g["simplicity"] = bell(cpx["edge_density"], 0.16, 0.12)   # intermediate complexity (Redies)
        g["colorfulness"] = bell(col["hasler"], 55, 35)
        g["contrast"] = ramp(con["rms_contrast"], 0.08, 0.26)
        g["fractal"] = bell(raw["fractal_dimension"], 1.4, 0.25)  # Taylor 1.3–1.5
        g["fourier"] = bell(raw["fourier_slope"], -2.5, 0.8)      # Spehar −2…−3
        g["thirds"] = ramp(raw["rule_of_thirds"], 0.10, 0.35)   # uniform edge mass ≈ 0.09
    else:  # logo
        g["simplicity"] = (0.6 * ramp(cpx["edge_density"], 0.25, 0.04)
                           + 0.4 * ramp(cpx["dominant_colors"], 10, 2))
        g["whitespace"] = bell(ws, 0.55, 0.25)
        g["contrast"] = ramp(con["edge_contrast"], 0.15, 0.5)
        g["economy"] = ramp(cpx["dominant_colors"], 8, 2)
    g["harmony"] = har["fit"]

    w = WEIGHTS[mode]
    total = sum(w[k] * g[k] for k in w)
    score = spread(total)

    # ---- defects are reported separately from beauty. Pixels can only *suspect* clipping
    # (a full-bleed image also touches the edge); the renderer knows (render.py measures
    # horizontal overflow in the DOM and applies the penalty). Here: a hint when the contact
    # with a side edge is fragmented, which is what cut-off text and controls look like.
    penalties = {}
    contact = raw["experimental"]["edge_contact"]
    suspect = None
    if mode == "ui":
        for side_name in ("right", "left"):
            c = contact[side_name]
            if c["coverage"] > 0.05 and c["runs"] >= 6:
                suspect = (side_name, c)
                break

    # ---- hints for an optimising agent ------------------------------------
    hints = list(sym.get("hints", []))
    weakest = sorted(((w[k] * (1 - g[k]), k) for k in w), reverse=True)[:3]
    advice = {
        "composition": "centre the main block; mirror controls at both ends of a row",
        "alignment": "snap element edges to a shared column/row grid",
        "simplicity": "reduce edge count, borders and the number of distinct colours",
        "whitespace": "adjust padding so ~60% of the canvas is background",
        "harmony": f"pull hues toward one harmonic template (currently best fit: {har['template']})",
        "colorfulness": "moderate saturation; keep accent colours few",
        "contrast": "raise figure–ground luminance contrast for text and controls",
        "local": "make individual components internally symmetric",
        "fractal": "aim for mid-range detail (fractal dimension ≈1.4)",
        "fourier": "balance coarse and fine structure (1/f spectrum)",
        "thirds": "place the focal element near a rule-of-thirds power point",
        "economy": "use fewer colours and shapes",
    }
    for loss, k in weakest:
        if loss > 0.03:
            hints.append(f"{k} ({g[k]:.2f}): {advice[k]}")
    if suspect:
        side_name, c = suspect
        hints.insert(0, f"clipping? content touches the {side_name} edge in {c['runs']} places over "
                        f"{int(100 * c['coverage'])}% of the height — looks cut off; check horizontal overflow "
                        f"(render the page with `beautiful page.html` to know for certain)")

    return {
        "score": score,
        "penalties": penalties,
        "mode_note": "classic",
        "mode": mode,
        "weighted_sum": round(float(total), 4),
        "factors": {k: round(float(v), 3) for k, v in g.items()},
        "weights": w,
        "raw": _rounded(raw),
        "hints": hints,
    }


def _rounded(o):
    if isinstance(o, dict):
        return {k: _rounded(v) for k, v in o.items()}
    if isinstance(o, float):
        return round(o, 4)
    return o


def beauty_score(image, mode: str = "ui") -> int:
    """The beauty number, 1..100."""
    return beauty(image, mode)["score"]
