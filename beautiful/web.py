"""
beautiful.web
-------------
``mode="web"``: the score *calibrated on human ratings of real websites*, as opposed to the
literature-shaped formula of ``mode="ui"``.

A ridge regression from the same pixel measurements (the goodness factors, the experimental
measurements, and edge density / colourfulness with their squares) to the mean appeal ratings of
398 website screenshots (Reinecke & Gajos 2014, via the Calista mirror). The fitted model lives in
``web_model.json``, written by ``research/calibrate.py``; ``research/CALIBRATION.md`` reports how
well it does (cross-validated and on a never-seen pairwise-rated set).

The number returned is a **percentile against those 398 rated sites**: web 70 means the model
puts the image above 70 % of them. It is advisory — see the calibration report — but unlike the
``ui`` formula it was checked against what people actually preferred.
"""
from __future__ import annotations

import json
import os

import numpy as np

_MODEL = None
_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_model.json")

# what a *negative* contribution means, term by term, for the hints
ADVICE = {
    "anisotropy": "one edge direction dominates (text blocks, stripes); rated-high pages mix shapes, imagery and directions",
    "edge_orientation_entropy": "edge orientations are unusual for a rated-high page; check for noise or a single dominant texture",
    "alignment": "grid quality is far from what rated-high pages show",
    "contour_congestion": "contours crowd each other; give elements room",
    "feature_congestion": "local colour/contrast/orientation variety is high (clutter); simplify",
    "colorfulness": "colour variety is off the range rated-high pages use",
    "colorfulness²": "colourfulness is extreme (too flat or too loud)",
    "simplicity": "complexity is off the range rated-high pages use",
    "whitespace": "background share is unlike rated-high pages (very empty pages rate low on this set)",
    "edge_density": "edge density is off the preferred range",
    "edge_density²": "edge density is extreme",
    "composition": "symmetry/balance is low",
    "harmony": "hue palette does not fit a harmonic template",
    "local": "components are internally asymmetric",
    "sequence": "visual weight does not follow the reading path",
    "contrast": "figure–ground contrast is off",
}


def model() -> dict:
    global _MODEL
    if _MODEL is None:
        with open(_PATH, encoding="utf-8") as f:
            _MODEL = json.load(f)
    return _MODEL


def inputs_from_report(factors: dict, raw: dict) -> dict:
    """The model's input vector, by term name, from a mode='ui' report."""
    x = raw["experimental"]
    ed = raw["complexity"]["edge_density"]
    cf = raw["colorfulness"]["variety"]
    vals = dict(factors)
    vals.update({k: x[k] for k in ("feature_congestion", "contour_congestion", "edge_orientation_entropy", "anisotropy", "sequence")})
    vals.update({"edge_density": ed, "edge_density²": ed * ed, "colorfulness": cf, "colorfulness²": cf * cf})
    return vals


def web_score(factors: dict, raw: dict) -> dict:
    m = model()
    vals = inputs_from_report(factors, raw)
    terms = m["terms"]
    # the design matrix repeats 'colorfulness' (goodness) then 'colorfulness' (raw); keep positional order
    seq = []
    seen_cf = False
    for t in terms:
        if t == "colorfulness":
            seq.append(factors["colorfulness"] if not seen_cf else raw["colorfulness"]["variety"])
            seen_cf = True
        else:
            seq.append(vals[t])
    z = (np.array(seq, dtype=float) - np.array(m["mu"])) / np.array(m["sd"])
    contrib = z * np.array(m["coef"])
    pred = float(contrib.sum() + m["intercept"])
    cal = np.array(m["calibration_predictions_sorted"])
    percentile = float(np.searchsorted(cal, pred, side="right") / len(cal))
    score = int(round(1 + 99 * percentile))
    labels = []
    seen_cf = False
    for t in terms:
        if t == "colorfulness":
            labels.append("colorfulness" if not seen_cf else "colorfulness (raw)")
            seen_cf = True
        else:
            labels.append(t)
    contributions = {lab: round(float(c), 4) for lab, c in zip(labels, contrib)}
    worst = sorted(contributions.items(), key=lambda kv: kv[1])[:3]
    hints = [f"{k} ({v:+.2f}): {ADVICE.get(k.replace(' (raw)', ''), 'far from rated-high pages')}"
             for k, v in worst if v < -0.05]
    return {
        "score": score,
        "predicted_rating_1_9": round(pred, 3),
        "percentile_of_rated_sites": round(percentile, 3),
        "contributions": dict(sorted(contributions.items(), key=lambda kv: -abs(kv[1]))),
        "hints": hints,
        "model": {"cv_rho": m["cv_rho_rating"], "out_of_sample_rho": m["transfer_rho_comparison"],
                  "n": m["n_rating"], "generated": m["generated"]},
    }
