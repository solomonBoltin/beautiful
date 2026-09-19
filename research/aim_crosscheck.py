"""Cross-check against AIM (Aalto Interface Metrics, aalto-ui/aim, MIT) — issue #19.

    python research/aim_crosscheck.py ../aim ../calista     # writes research/AIM.md, research/aim_cache.json

AIM's metric classes are imported straight from its backend (no server, no MongoDB) and run on
the same screenshots our measurements see. For every AIM metric that has a counterpart in
`beautiful`, the report gives the Spearman correlation between the reference implementation and
ours, and how well each one separates acclaimed pages from ordinary ones (AUC). Inputs are
downscaled to 640 px wide for both sides — AIM at full 1280×800 takes ~55 s per image.
"""
from __future__ import annotations

import base64
import csv
import glob
import importlib
import io
import json
import os
import sys
import warnings

import numpy as np
from PIL import Image
from scipy.stats import mannwhitneyu, spearmanr

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from beautiful import beauty  # noqa: E402

AIM = {  # metric id -> (module, what it measures, our counterpart, how to read ours from a classic report)
    "m4": ("aim.metrics.m4.m4_contour_density", "contour density", "edge_density", lambda r: r["raw"]["complexity"]["edge_density"]),
    "m5": ("aim.metrics.m5.m5_figure_ground_contrast", "figure-ground contrast", "edge_contrast", lambda r: r["raw"]["contrast"]["edge_contrast"]),
    "m6": ("aim.metrics.m6.m6_contour_congestion", "contour congestion", "contour_congestion", lambda r: r["raw"]["experimental"]["contour_congestion"]),
    "m7": ("aim.metrics.m7.m7_subband_entropy", "subband entropy (clutter)", "— (issue #13)", None),
    "m8": ("aim.metrics.m8.m8_feature_congestion", "feature congestion (clutter)", "feature_congestion", lambda r: r["raw"]["experimental"]["feature_congestion"]),
    "m13": ("aim.metrics.m13.m13_luminance_std", "luminance std", "rms_contrast", lambda r: r["raw"]["contrast"]["rms_contrast"]),
    "m15": ("aim.metrics.m15.m15_colorfulness_hassler_susstrunk", "colourfulness (Hasler–Süsstrunk)", "colorfulness.hasler", lambda r: r["raw"]["colorfulness"]["hasler"]),
    "m3": ("aim.metrics.m3.m3_distinct_rgb_values", "distinct RGB values", "dominant_colors", lambda r: r["raw"]["complexity"]["dominant_colors"]),
}


def b64(im):
    buf = io.BytesIO(); im.save(buf, "PNG"); return base64.b64encode(buf.getvalue()).decode()


def prep(path, width=640):
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    return im


def run_aim(im, mods):
    out = {}
    s = b64(im)
    for k, cls in mods.items():
        try:
            out[k] = float(cls.execute_metric(s)[0])
        except Exception as e:  # noqa: BLE001
            out[k] = None
            print("  aim", k, "failed:", str(e)[:80], flush=True)
    return out


def main():
    aim_root, calista = sys.argv[1], sys.argv[2]
    sys.path.insert(0, os.path.join(aim_root, "backend"))
    mods = {k: getattr(importlib.import_module(m), "Metric") for k, (m, *_) in AIM.items()}
    top = json.load(open(os.path.join(HERE, "results_top100.json")))["rows"]
    sets = {
        "demo": sorted(glob.glob(os.path.join(ROOT, "demo", "screens", "*.png"))),
        "famous": sorted(glob.glob(os.path.join(ROOT, "demo", "famous", "*.png"))),
        "acclaimed": [os.path.join(HERE, r["file"]) for r in top[::3]][:34],
    }
    ordinary = []
    with open(os.path.join(calista, "comparison-based-dataset", "website_scores.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ordinary.append(os.path.join(calista, "comparison-based-dataset", "images", row["website"].replace("image", "") + ".png"))
    sets["ordinary"] = [p for p in ordinary if os.path.exists(p)][::3][:34]
    cache_p = os.path.join(HERE, "aim_cache.json")
    cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
    for name, paths in sets.items():
        for i, p in enumerate(paths):
            if p in cache:
                continue
            im = prep(p)
            r = beauty(im, "classic")
            row = {"set": name, "aim": run_aim(im, mods), "ours": {k: float(f(r)) for k, (_, _, _, f) in AIM.items() if f},
                   "ui": beauty(im, "ui")["score"], "classic": r["score"], "web": beauty(im, "web")["score"]}
            cache[p] = row
            json.dump(cache, open(cache_p, "w"))
            print(f"{name} {i+1}/{len(paths)} {os.path.basename(p)}", flush=True)
    rows = [cache[p] for paths in sets.values() for p in paths if p in cache]
    acc = [r for r in rows if r["set"] == "acclaimed"]; ordn = [r for r in rows if r["set"] == "ordinary"]

    def auc(pos, neg):
        pos, neg = [v for v in pos if v is not None], [v for v in neg if v is not None]
        return mannwhitneyu(pos, neg, alternative="two-sided").statistic / (len(pos) * len(neg))

    lines = ["# Cross-check against AIM (Aalto Interface Metrics)", "",
             f"AIM's metric classes (aalto-ui/aim, MIT) run directly on {len(rows)} screenshots: {len(sets['demo'])} demo screens, "
             f"{len(sets['famous'])} famous home pages, {len(acc)} acclaimed pages (every third of research/top100) and {len(ordn)} ordinary pages "
             "(every third of Calista's comparison set). Inputs downscaled to 640 px for both implementations. "
             "Metrics that need AIM's segmentation models (grid quality m21, white space m22) or a saliency/NIMA network (m9, m18) are not run; "
             "colour harmony m20 takes ~100 s per image and was left out.", "",
             "## Does our simplified implementation agree with the reference?", "",
             "| AIM metric | ours | Spearman ρ (all images) | AUC acclaimed > ordinary: AIM | ours |", "|---|---|---:|---:|---:|"]
    for k, (_, what, ours, f) in AIM.items():
        a_all = [r["aim"][k] for r in rows]
        if f:
            o_all = [r["ours"][k] for r in rows]
            ok = [(a, o) for a, o in zip(a_all, o_all) if a is not None]
            rho = spearmanr([a for a, _ in ok], [o for _, o in ok]).correlation
            lines.append(f"| {k} {what} | `{ours}` | {rho:+.2f} | {auc([r['aim'][k] for r in acc], [r['aim'][k] for r in ordn]):.2f} | {auc([r['ours'][k] for r in acc], [r['ours'][k] for r in ordn]):.2f} |")
        else:
            lines.append(f"| {k} {what} | {ours} | — | {auc([r['aim'][k] for r in acc], [r['aim'][k] for r in ordn]):.2f} | — |")
    lines += ["", "## AIM's metrics against our scores (Spearman, all images)", "", "| AIM metric | vs `ui` | vs `classic` | vs `web` |", "|---|---:|---:|---:|"]
    for k, (_, what, *_r) in AIM.items():
        a = [r["aim"][k] for r in rows]
        cells = []
        for s in ("ui", "classic", "web"):
            pairs = [(x, r[s]) for x, r in zip(a, rows) if x is not None]
            cells.append(f"{spearmanr([p for p, _ in pairs], [q for _, q in pairs]).correlation:+.2f}")
        lines.append(f"| {k} {what} | " + " | ".join(cells) + " |")
    lines += ["", "## Demo screens, side by side", "", "| screen | `ui` | AIM contour density | ours | AIM contrast | ours | AIM contour congestion | ours | AIM feature congestion | ours | AIM subband entropy |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for p in sets["demo"]:
        r = cache.get(p)
        if not r:
            continue
        a, o = r["aim"], r["ours"]
        fmt = lambda v: "—" if v is None else f"{v:.3f}"
        lines.append(f"| {os.path.basename(p)[:-4]} | {r['ui']} | {fmt(a['m4'])} | {o['m4']:.3f} | {fmt(a['m5'])} | {o['m5']:.2f} | {fmt(a['m6'])} | {o['m6']:.3f} | {fmt(a['m8'])} | {o['m8']:.4f} | {fmt(a['m7'])} |")
    lines += ["", "## How to read this", "",
              "- ρ near +1: our simplified measurement orders pages the way the reference does, so replacing it would change nothing but the scale. Near 0: the two measure different things and the name is misleading; the AIM one is the literature's.",
              "- The two AUC columns say which implementation is the better *design* signal on this data, independent of agreement.",
              "- AIM implements Miniukovich & De Angeli's metrics as published (with their thresholds); ours were written from the papers with stated simplifications (beautiful/experimental.py)."]
    open(os.path.join(HERE, "AIM.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[:24]))


if __name__ == "__main__":
    main()
