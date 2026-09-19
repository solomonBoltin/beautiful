"""
beautiful.model
---------------
The fitted `ui` formula (research/fit_ui.py → ui_model.json): the same explicit shape as the
literature formula — a weighted sum of goodness terms, each a documented curve over one pixel
measurement — but with the curves centred on what acclaimed pages measure and the weights fitted
to three targets at once (acclaimed > ordinary, original > degraded twin, crowd ratings).

    from beautiful.model import fitted_ui
    fitted_ui(raw) -> {"score", "factors", "weights", "hints", "model"}

`raw` is the measurement dict a `beauty()` report already carries, so nothing is computed twice.
"""
from __future__ import annotations

import json
import math
import os

_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui_model.json")
_MODEL = None

READ = {
    "composition": lambda r: r["symmetry"]["score"] / 100.0,
    "mirror": lambda r: r["symmetry"]["horizontal_mirror"],
    "balance": lambda r: r["symmetry"]["balance"],
    "local": lambda r: r["symmetry"]["local_symmetry"],
    "alignment": lambda r: 0.65 * r["alignment"]["x_alignment"] + 0.35 * r["alignment"]["y_alignment"],
    "contrast": lambda r: r["contrast"]["edge_contrast"],
    "harmony": lambda r: r["harmony"]["fit"],
    "edge_density": lambda r: r["complexity"]["edge_density"],
    "jpeg_bpp": lambda r: r["complexity"]["jpeg_bpp"],
    "colours": lambda r: r["complexity"]["dominant_colors"],
    "whitespace": lambda r: r["whitespace"],
    "colorfulness": lambda r: r["colorfulness"]["variety"],
    "congestion": lambda r: r["experimental"]["feature_congestion"],
    "contour": lambda r: r["experimental"]["contour_congestion"],
    "orientation": lambda r: r["experimental"]["edge_orientation_entropy"],
    "anisotropy": lambda r: r["experimental"]["anisotropy"],
    "hierarchy": lambda r: r["experimental"]["hierarchy"],
    "margin": lambda r: 1.0 - max(r["experimental"]["edge_contact"]["left"]["coverage"], r["experimental"]["edge_contact"]["right"]["coverage"]),
}

ADVICE = {
    "composition": "centre the main block, or balance it: equal visual weight on both sides",
    "mirror": "mirror the layout about the centre line, or balance it (see balance)",
    "balance": "the visual mass sits to one side; move or counterweight it",
    "local": "make individual components internally symmetric",
    "alignment": "snap element edges to a shared column/row grid",
    "contrast": "raise figure–ground contrast for text and controls",
    "harmony": "pull hues toward one harmonic template",
    "edge_density": "edge density (detail) is {dir} what acclaimed pages have; {act}",
    "jpeg_bpp": "visual information is {dir} what acclaimed pages carry; {act}",
    "colours": "the number of dominant colours is {dir} acclaimed pages; {act}",
    "whitespace": "background share is {dir} acclaimed pages ({centre:.0%}); {act}",
    "colorfulness": "colour variety is {dir} acclaimed pages; {act}",
    "congestion": "local clutter (feature congestion) is {dir} acclaimed pages; {act}",
    "contour": "contours crowd each other more than on acclaimed pages" ,
    "orientation": "edge orientations are {dir} acclaimed pages (they mix directions, images and type); {act}",
    "anisotropy": "one edge direction dominates {dir} acclaimed pages; {act}",
    "hierarchy": "little structure at block scale: give the page a hero, sections or a clear heading scale",
    "margin": "content runs into the left/right edge: give the page side margins (or fix the overflow)",
}
ACT = {"above": "simplify", "below": "add substance: imagery, contrast, a real hero"}


def model() -> dict | None:
    global _MODEL
    if _MODEL is None and os.path.exists(_PATH):
        with open(_PATH, encoding="utf-8") as f:
            _MODEL = json.load(f)
    return _MODEL


def fitted_ui(raw: dict) -> dict:
    m = model()
    if m is None:
        raise RuntimeError("ui_model.json missing: run research/fit_ui.py")
    factors, weights, terms = {}, {}, {}
    for t in m["terms"]:
        x = float(READ[t["name"]](raw))
        if t["kind"] == "bell":
            g = math.exp(-((x - t["centre"]) / t["width"]) ** 2)
        else:
            g = min(1.0, max(0.0, (x - t["lo"]) / (t["hi"] - t["lo"] + 1e-9)))
        factors[t["name"]] = round(g, 3)
        weights[t["name"]] = t["weight"]
        terms[t["name"]] = (x, t)
    total = sum(weights[k] * factors[k] for k in factors)
    score = int(round(1 + 99 / (1 + math.exp(-8 * (total - 0.55)))))
    hints = []
    for loss, k in sorted(((weights[k] * (1 - factors[k]), k) for k in factors), reverse=True)[:3]:
        if loss <= 0.02:
            continue
        x, t = terms[k]
        if t["kind"] == "bell":
            d = "above" if x > t["centre"] else "below"
            hints.append(f"{k} ({factors[k]:.2f}): " + ADVICE[k].format(dir=d, act=ACT[d], centre=t["centre"]))
        else:
            hints.append(f"{k} ({factors[k]:.2f}): " + ADVICE[k])
    return {"score": score, "weighted_sum": round(total, 4), "factors": factors, "weights": weights, "hints": hints,
            "model": {"fitted_on": m["fitted_on"], "cv": m.get("cv", {})}}
