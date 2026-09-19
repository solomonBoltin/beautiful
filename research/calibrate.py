"""Calibrate `beautiful` against human ratings of website screenshots.

Data: the Calista mirror of the Reinecke & Gajos (CHI 2014) LabintheWild ratings
(398 screenshots with mean appeal ratings; CC BY-NC-SA 3.0) and Calista's own
comparison-based set (100 Alexa-top-5000 pages, Bradley–Terry scores from 5,094 pairwise
votes). Neither dataset is redistributed here.

    git clone --depth 1 https://github.com/calista-ai/website-aesthetics-datasets calista
    python research/calibrate.py calista            # ~10 min; caches features in research/features_*.csv

What it reports (research/CALIBRATION.md):
  1. Spearman rho of the current `ui` score vs mean human rating (the honest baseline).
  2. Each factor's own rho — which factors carry signal on real websites.
  3. Non-negative weights fitted on the goodness factors (the same linear form the score
     uses), 5-fold cross-validated rho, and the weights themselves.
  4. A ridge model with squared terms for complexity and colourfulness (the inverted-U the
     literature reports) and the experimental measurements, cross-validated.
  5. Transfer: everything above scored on the comparison-based set it never saw.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import nnls
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from beautiful import beauty  # noqa: E402
from beautiful.core import WEIGHTS  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FACTORS = list(WEIGHTS["ui"])
EXPERIMENTAL = ["feature_congestion", "contour_congestion", "edge_orientation_entropy", "anisotropy", "sequence"]
RAW = ["edge_density", "jpeg_bpp", "dominant_colors", "colorfulness_variety", "whitespace"]


def load_ratings(root):
    """-> [(image_path, mean_rating)] for the rating set, [(image_path, bt_score)] for the comparison set."""
    rating = {}
    for name in ("train_means_list.csv", "test_list.csv"):
        with open(os.path.join(root, "rating-based-dataset", "preprocess", name), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rel = row["image"].lstrip("/").replace("_resized", "")  # /english_resized/3.png -> english/3.png
                rating[os.path.join(root, "rating-based-dataset", "images", rel)] = float(row["mean_score"])
    comparison = {}
    with open(os.path.join(root, "comparison-based-dataset", "website_scores.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row["website"].replace("image", "") + ".png"  # website_scores.csv says "image50"; the file is 50.png
            comparison[os.path.join(root, "comparison-based-dataset", "images", name)] = float(row["score"])
    return sorted(rating.items()), sorted(comparison.items())


def features_for(path):
    r = beauty(path, "classic")   # the web model is a ridge over the literature (classic) factors
    x = r["raw"]["experimental"]
    row = {"score": r["score"], "weighted_sum": r["weighted_sum"]}
    row.update({f"g_{k}": r["factors"][k] for k in FACTORS})
    row.update({f"x_{k}": x[k] for k in EXPERIMENTAL})
    row.update({
        "r_edge_density": r["raw"]["complexity"]["edge_density"],
        "r_jpeg_bpp": r["raw"]["complexity"]["jpeg_bpp"],
        "r_dominant_colors": r["raw"]["complexity"]["dominant_colors"],
        "r_colorfulness_variety": r["raw"]["colorfulness"]["variety"],
        "r_whitespace": r["raw"]["whitespace"],
    })
    return row


def compute(items, cache):
    rows = {}
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rows[row["image"]] = {k: float(v) for k, v in row.items() if k not in ("image", "y")}
    todo = [(p, y) for p, y in items if p not in rows]
    t0 = time.time()
    for i, (p, y) in enumerate(todo, 1):
        try:
            rows[p] = features_for(p)
        except Exception as e:  # a broken PNG must not kill a 10-minute run
            print("skip", p, e)
            continue
        if i % 25 == 0:
            print(f"  {i}/{len(todo)}  {time.time() - t0:.0f}s", flush=True)
    ys = dict(items)
    keys = sorted({k for r in rows.values() for k in r})
    with open(cache, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["image", "y"] + keys)
        for p, r in rows.items():
            if p in ys:
                w.writerow([p, ys[p]] + [r.get(k, "") for k in keys])
    X = [(p, rows[p], ys[p]) for p, _ in items if p in rows]
    return X


def rho(a, b):
    return float(spearmanr(a, b).correlation)


def kfold(n, k=5, seed=0):
    idx = np.random.RandomState(seed).permutation(n)
    return [idx[i::k] for i in range(k)]


def fit_nnls(G, y):
    """Non-negative weights on goodness factors (+ intercept), sum normalised to 1 for reading."""
    A = np.hstack([G, np.ones((len(G), 1))])
    w, _ = nnls(A, y)
    return w


def ridge(X, y, lam=1.0):
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = (X - mu) / sd
    A = np.hstack([Z, np.ones((len(Z), 1))])
    I = np.eye(A.shape[1]); I[-1, -1] = 0
    w = np.linalg.solve(A.T @ A + lam * I, A.T @ y)
    return w, mu, sd


def ridge_predict(model, X):
    w, mu, sd = model
    Z = (X - mu) / sd
    return np.hstack([Z, np.ones((len(Z), 1))]) @ w


def cv_rho(X, y, fit, predict, k=5):
    folds = kfold(len(y), k)
    preds = np.zeros(len(y))
    for test in folds:
        train = np.setdiff1d(np.arange(len(y)), test)
        m = fit(X[train], y[train])
        preds[test] = predict(m, X[test])
    return rho(preds, y)


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "calista"
    rating_items, comparison_items = load_ratings(root)
    print(f"rating set: {len(rating_items)} images   comparison set: {len(comparison_items)} images")
    R = compute(rating_items, os.path.join(HERE, "features_rating.csv"))
    C = compute(comparison_items, os.path.join(HERE, "features_comparison.csv"))
    print(f"scored {len(R)} + {len(C)}")

    def mat(rows, keys):
        return np.array([[r[k] for k in keys] for _, r, _ in rows], dtype=float)

    yR = np.array([y for _, _, y in R]); yC = np.array([y for _, _, y in C])
    gk = [f"g_{k}" for k in FACTORS]
    xk = [f"x_{k}" for k in EXPERIMENTAL]
    GR, GC = mat(R, gk), mat(C, gk)
    XR, XC = mat(R, xk), mat(C, xk)
    sR, sC = mat(R, ["score"])[:, 0], mat(C, ["score"])[:, 0]

    lines = ["# Calibration against human ratings", "",
             f"Rating set: **{len(R)}** website screenshots with mean appeal ratings "
             "(Reinecke & Gajos 2014 via the Calista mirror). Comparison set: **%d** pages with "
             "Bradley–Terry scores from pairwise votes (Calista 2023). Spearman ρ throughout; "
             "5-fold cross-validation for anything fitted. Run: `python research/calibrate.py`." % len(C), ""]

    lines += ["## 1. The score as shipped", "",
              "| | rating set | comparison set |", "|---|---:|---:|",
              f"| `beauty(mode='ui')` vs human | **{rho(sR, yR):.3f}** | **{rho(sC, yC):.3f}** |", ""]

    lines += ["## 2. Each factor on its own", "", "| factor | ρ (rating) | ρ (comparison) |", "|---|---:|---:|"]
    for j, k in enumerate(FACTORS):
        lines.append(f"| {k} | {rho(GR[:, j], yR):+.3f} | {rho(GC[:, j], yC):+.3f} |")
    for j, k in enumerate(EXPERIMENTAL):
        lines.append(f"| *{k}* (experimental, unweighted) | {rho(XR[:, j], yR):+.3f} | {rho(XC[:, j], yC):+.3f} |")
    rk = [f"r_{k}" for k in RAW]
    RR, RC = mat(R, rk), mat(C, rk)
    for j, k in enumerate(RAW):
        lines.append(f"| raw {k} | {rho(RR[:, j], yR):+.3f} | {rho(RC[:, j], yC):+.3f} |")
    lines.append("")

    # 3. non-negative weights on the goodness factors — same form as the shipped score
    cv = cv_rho(GR, yR, lambda X, y: fit_nnls(X, y), lambda w, X: np.hstack([X, np.ones((len(X), 1))]) @ w)
    w = fit_nnls(GR, yR)
    wn = w[:-1] / (w[:-1].sum() + 1e-9)
    transfer = rho(np.hstack([GC, np.ones((len(GC), 1))]) @ w, yC)
    lines += ["## 3. Non-negative weights fitted on the goodness factors", "",
              f"Same linear form as the shipped score. Cross-validated ρ on the rating set: **{cv:.3f}**; "
              f"the weights fitted on all of it, applied to the comparison set it never saw: **{transfer:.3f}**.", "",
              "| factor | shipped weight | fitted weight |", "|---|---:|---:|"]
    for j, k in enumerate(FACTORS):
        lines.append(f"| {k} | {WEIGHTS['ui'][k]:.2f} | {wn[j]:.2f} |")
    lines.append("")
    json.dump({"fitted_ui_weights": {k: round(float(wn[j]), 4) for j, k in enumerate(FACTORS)},
               "cv_rho_rating": round(cv, 4), "transfer_rho_comparison": round(transfer, 4),
               "shipped_rho_rating": round(rho(sR, yR), 4), "shipped_rho_comparison": round(rho(sC, yC), 4),
               "n_rating": len(R), "n_comparison": len(C)},
              open(os.path.join(HERE, "fitted_weights.json"), "w"), indent=1)

    # 4. ridge with inverted-U terms + experimental measurements
    def design(G, X, Rw):
        ed, cf = Rw[:, RAW.index("edge_density")], Rw[:, RAW.index("colorfulness_variety")]
        return np.hstack([G, X, np.c_[ed, ed ** 2, cf, cf ** 2]])
    DR, DC = design(GR, XR, RR), design(GC, XC, RC)
    best = None
    for lam in (0.3, 1, 3, 10, 30):
        c = cv_rho(DR, yR, lambda X, y, lam=lam: ridge(X, y, lam), ridge_predict)
        if best is None or c > best[1]:
            best = (lam, c)
    model = ridge(DR, yR, best[0])
    lines += ["## 4. Ridge with inverted-U terms and the experimental measurements", "",
              f"Inputs: the {len(FACTORS)} goodness factors, the {len(EXPERIMENTAL)} experimental measurements, and "
              "edge density and colourfulness with their squares (the inverted-U). "
              f"Best λ = {best[0]}; cross-validated ρ on the rating set: **{best[1]:.3f}**; "
              f"transfer to the comparison set: **{rho(ridge_predict(model, DC), yC):.3f}**.", "",
              "| term | standardised coefficient |", "|---|---:|"]
    names = FACTORS + EXPERIMENTAL + ["edge_density", "edge_density²", "colorfulness", "colorfulness²"]
    for n, c in sorted(zip(names, model[0][:-1]), key=lambda t: -abs(t[1])):
        lines.append(f"| {n} | {c:+.3f} |")
    # export the calibrated model as the `web` mode (see beautiful/web.py)
    w_all, mu, sd = model
    preds_cal = np.sort(ridge_predict(model, DR))
    web = {
        "terms": names, "coef": [round(float(c), 6) for c in w_all[:-1]], "intercept": round(float(w_all[-1]), 6),
        "mu": [round(float(v), 6) for v in mu], "sd": [round(float(v), 6) for v in sd],
        "calibration_predictions_sorted": [round(float(v), 4) for v in preds_cal],
        "rating_scale": "Reinecke & Gajos 2014 mean appeal, 1-9",
        "cv_rho_rating": round(best[1], 4), "transfer_rho_comparison": round(rho(ridge_predict(model, DC), yC), 4),
        "lambda": best[0], "n_rating": len(R), "n_comparison": len(C), "generated": time.strftime("%Y-%m-%d"),
    }
    json.dump(web, open(os.path.join(os.path.dirname(HERE), "beautiful", "web_model.json"), "w"), indent=1)
    lines += ["", "This ridge model ships as `beauty(image, mode='web')`: the prediction is reported as a "
              "percentile against the 398 rated sites (a web score of 70 = the model puts it above 70 %% of "
              "them). Cross-validated ρ ≈ %.2f and out-of-sample ρ ≈ %.2f make it **advisory**, not a truth — "
              "the survey's own rule is ρ ≥ 0.7 to trust, < 0.5 advisory." % (best[1], web["transfer_rho_comparison"])]
    lines += ["", "## How to read this", "",
              "- Hand-crafted metric sets top out near ρ ≈ 0.6–0.7 on website ratings in the literature "
              "(Reinecke 2013: 48 % of variance; Miniukovich 2015: 49 %); learned CNNs reach r ≈ 0.85 "
              "(Webthetics). Anything in that band is as good as pixels-without-semantics get.",
              "- A factor whose sign flips between the two sets is not robust; a factor near zero on both "
              "is carrying its weight for a reason other than appeal (e.g. it makes the hints useful).",
              "- The comparison set is the honest test: nothing was fitted on it.",
              "", f"_Generated {time.strftime('%Y-%m-%d')} by research/calibrate.py; features cached in research/features_*.csv._"]
    open(os.path.join(HERE, "CALIBRATION.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
