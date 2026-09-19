"""Does the score know beauty when it sees it? Three sets, one question.

  acclaimed  research/top100/*.png      the 100 most acclaimed home pages (research/top100.py)
  ordinary   calista comparison set     100 random Alexa-top-5000 pages, with human pairwise ranks
  broken     rendered defects           demo/lint/bad.html + floor.html at three viewports, the
                                        unstyled captures, the lopsided samples

A useful beauty score must (1) put acclaimed above ordinary, (2) put both above broken, and
(3) still agree with the human ratings it was calibrated on. This script measures all three for
the shipped `ui` score, the `web` model and every factor (AUC = probability that a random
acclaimed page outscores a random ordinary one), then fits weights on the goodness factors that
maximise the acclaimed-vs-ordinary separation *subject to* not losing the human-rating
correlation, with 5-fold cross-validation, and writes research/BENCHMARK.md and
research/fitted_ui_weights.json. Shipping the fitted weights is a separate, deliberate step.

    python research/benchmark.py [calista_root]
"""
from __future__ import annotations

import csv
import json
import os
import sys

import numpy as np
from scipy.optimize import minimize
from scipy.stats import mannwhitneyu, spearmanr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from beautiful import beauty  # noqa: E402
from beautiful.core import WEIGHTS, spread  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FACTORS = list(WEIGHTS["ui"])
EXPERIMENTAL = ["feature_congestion", "contour_congestion", "edge_orientation_entropy", "anisotropy", "sequence"]


def auc(pos, neg):
    """Probability a random positive outscores a random negative (Mann–Whitney U / n·m)."""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if not len(pos) or not len(neg):
        return float("nan")
    u = mannwhitneyu(pos, neg, alternative="two-sided").statistic
    return float(u / (len(pos) * len(neg)))


def feats(path):
    r = beauty(path, "classic")   # literature formula; the fitted `ui` and `web` are scored alongside
    x = r["raw"]["experimental"]
    return {"score": r["score"], "ui": beauty(path, "ui")["score"], "web": beauty(path, "web")["score"],
            **{f"g_{k}": r["factors"][k] for k in FACTORS},
            **{f"x_{k}": x[k] for k in EXPERIMENTAL}}


def load_set(paths, cache):
    rows = {}
    if os.path.exists(cache):
        rows = json.load(open(cache))
    todo = [p for p in paths if p not in rows]
    for i, p in enumerate(todo, 1):
        try:
            rows[p] = feats(p)
        except Exception as e:
            print("skip", p, e)
        if i % 20 == 0:
            print(f"  {i}/{len(todo)}", flush=True)
    json.dump(rows, open(cache, "w"), indent=0)
    return {p: rows[p] for p in paths if p in rows}


def main():
    calista = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "..", "calista")
    top = json.load(open(os.path.join(HERE, "results_top100.json")))
    acclaimed = [os.path.join(HERE, r["file"]) for r in top["rows"]]
    ordinary_scores = {}
    with open(os.path.join(calista, "comparison-based-dataset", "website_scores.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ordinary_scores[os.path.join(calista, "comparison-based-dataset", "images", row["website"].replace("image", "") + ".png")] = float(row["score"])
    ordinary = [p for p in ordinary_scores if os.path.exists(p)]
    rating = {}
    for name in ("train_means_list.csv", "test_list.csv"):
        with open(os.path.join(calista, "rating-based-dataset", "preprocess", name), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rating[os.path.join(calista, "rating-based-dataset", "images", row["image"].lstrip("/").replace("_resized", ""))] = float(row["mean_score"])
    rated = [p for p in rating if os.path.exists(p)]
    broken = []
    bdir = os.path.join(HERE, "broken")
    os.makedirs(bdir, exist_ok=True)
    from beautiful.render import score_html
    for f in ("bad.html", "floor.html"):
        reps = score_html(os.path.join(ROOT, "demo", "lint", f), save_dir=bdir)
        broken += [r["image"] for r in reps.values() if "image" in r]
    broken += [os.path.join(ROOT, "demo", "screens", n) for n in ("github_login_unstyled.png", "npm_home_unstyled.png", "sample_asymmetric_ui.png", "digital_office_original.png")]

    A = load_set(acclaimed, os.path.join(HERE, "bench_acclaimed.json"))
    O = load_set(ordinary, os.path.join(HERE, "bench_ordinary.json"))
    B = load_set(broken, os.path.join(HERE, "bench_broken.json"))
    R = load_set(rated, os.path.join(HERE, "bench_rated.json"))
    print(f"acclaimed {len(A)}  ordinary {len(O)}  broken {len(B)}  rated {len(R)}")

    keys = ["score", "ui", "web"] + [f"g_{k}" for k in FACTORS] + [f"x_{k}" for k in EXPERIMENTAL]
    col = lambda S, k: [v[k] for v in S.values()]
    lines = ["# Does the score know beauty when it sees it?", "",
             f"Three sets: **{len(A)} acclaimed** home pages (research/top100.py), **{len(O)} ordinary** pages "
             "(Calista's random Alexa-top-5000 set, which also carries human pairwise ranks), and "
             f"**{len(B)} broken** renders (the lint fixtures at three viewports, unstyled and lopsided captures). "
             f"Plus the **{len(R)} human-rated** screenshots (Reinecke & Gajos 2014) the `web` model was fitted on.", "",
             "AUC = the probability that a random page from the first set outscores a random page from the second "
             "(0.5 = coin flip, 1.0 = perfect). ρ = Spearman against the human numbers.", "",
             "## 1. Every score and factor, on its own", "",
             "| signal | AUC acclaimed > ordinary | AUC acclaimed > broken | AUC ordinary > broken | ρ vs pairwise rank (ordinary) | ρ vs rating (rated) |",
             "|---|---:|---:|---:|---:|---:|"]
    yO = np.array([ordinary_scores[p] for p in O])
    yR = np.array([rating[p] for p in R])
    table = {}
    for k in keys:
        a, o, b = col(A, k), col(O, k), col(B, k)
        row = (auc(a, o), auc(a, b), auc(o, b), spearmanr(col(O, k), yO).correlation, spearmanr(col(R, k), yR).correlation)
        table[k] = row
        name = {"score": "**`classic` (literature weights)**", "ui": "**`ui` (fitted, research/fit_ui.py)**", "web": "**`web` model**"}.get(k, k.replace("g_", "").replace("x_", "*") + ("*" if k.startswith("x_") else ""))
        lines.append(f"| {name} | " + " | ".join(f"{v:.2f}" for v in row) + " |")
    lines.append("")

    # 2. fit weights on goodness factors: maximise AUC(acclaimed vs ordinary) + AUC(all vs broken), keep rho >= shipped
    gk = [f"g_{k}" for k in FACTORS]
    GA, GO, GB, GR = (np.array([[v[k] for k in gk] for v in S.values()]) for S in (A, O, B, R))

    def objective(w, GA, GO, GB, GR, yR):
        w = np.abs(w) / (np.abs(w).sum() + 1e-9)
        sA, sO, sB, sR = GA @ w, GO @ w, GB @ w, GR @ w
        a1, a2 = auc(sA, sO), auc(np.concatenate([sA, sO]), sB)
        rho = spearmanr(sR, yR).correlation
        # separation is the goal; the human-rating correlation must not get worse than the shipped weights
        penalty = max(0.0, base_rho - rho) * 2
        return -(0.6 * a1 + 0.4 * a2) + penalty

    w0 = np.array([WEIGHTS["ui"][k] for k in FACTORS])
    base_rho = spearmanr(GR @ w0, yR).correlation
    rng = np.random.RandomState(0)
    folds = [rng.permutation(len(GA))[i::5] for i in range(5)]
    cv_auc, cv_base = [], []
    for test in folds:
        train = np.setdiff1d(np.arange(len(GA)), test)
        testO = rng.choice(len(GO), size=min(len(GO), 20), replace=False)
        trainO = np.setdiff1d(np.arange(len(GO)), testO)
        best = None
        for start in [w0] + [rng.dirichlet(np.ones(len(FACTORS))) for _ in range(6)]:
            res = minimize(objective, start, args=(GA[train], GO[trainO], GB, GR, yR), method="Nelder-Mead", options={"maxiter": 600, "xatol": 1e-3, "fatol": 1e-4})
            if best is None or res.fun < best.fun:
                best = res
        w = np.abs(best.x) / np.abs(best.x).sum()
        cv_auc.append(auc(GA[test] @ w, GO[testO] @ w))
        cv_base.append(auc(GA[test] @ w0, GO[testO] @ w0))
    best = None
    for start in [w0] + [rng.dirichlet(np.ones(len(FACTORS))) for _ in range(10)]:
        res = minimize(objective, start, args=(GA, GO, GB, GR, yR), method="Nelder-Mead", options={"maxiter": 800, "xatol": 1e-3, "fatol": 1e-4})
        if best is None or res.fun < best.fun:
            best = res
    wf = np.abs(best.x) / np.abs(best.x).sum()
    fitted = {k: round(float(wf[i]), 3) for i, k in enumerate(FACTORS)}
    sA, sO, sB, sR = GA @ wf, GO @ wf, GB @ wf, GR @ wf
    lines += ["## 2. Weights fitted to separate acclaimed from ordinary (and both from broken) — first pass", "",
              "A first, linear-only pass (kept for the record; the shipped fit is research/fit_ui.py). Same linear form as the classic score; weights non-negative, sum to 1; objective 0.6·AUC(acclaimed > ordinary) + "
              "0.4·AUC(all pages > broken), with a penalty whenever the human-rating correlation drops below the shipped weights'. "
              "5-fold cross-validation over the acclaimed set (20 ordinary pages held out per fold).", "",
              "| | shipped weights | fitted weights |", "|---|---:|---:|",
              f"| AUC acclaimed > ordinary (cross-validated) | {np.mean(cv_base):.2f} | {np.mean(cv_auc):.2f} |",
              f"| AUC acclaimed > ordinary (all data) | {auc(GA @ w0, GO @ w0):.2f} | {auc(sA, sO):.2f} |",
              f"| AUC all > broken | {auc(np.concatenate([GA @ w0, GO @ w0]), GB @ w0):.2f} | {auc(np.concatenate([sA, sO]), sB):.2f} |",
              f"| ρ vs human rating (398) | {base_rho:+.2f} | {spearmanr(sR, yR).correlation:+.2f} |",
              f"| ρ vs human pairwise rank (100) | {spearmanr(GO @ w0, yO).correlation:+.2f} | {spearmanr(sO, yO).correlation:+.2f} |", "",
              "| factor | shipped | fitted |", "|---|---:|---:|"] + [f"| {k} | {WEIGHTS['ui'][k]:.2f} | {fitted[k]:.2f} |" for k in FACTORS] + [""]
    json.dump({"fitted_ui_weights": fitted, "cv_auc_acclaimed_vs_ordinary": round(float(np.mean(cv_auc)), 4),
               "shipped_cv_auc": round(float(np.mean(cv_base)), 4), "rho_rating_fitted": round(float(spearmanr(sR, yR).correlation), 4),
               "rho_rating_shipped": round(float(base_rho), 4), "n": {"acclaimed": len(A), "ordinary": len(O), "broken": len(B), "rated": len(R)}},
              open(os.path.join(HERE, "fitted_ui_weights.json"), "w"), indent=1)

    # 3. what the acclaimed pages look like, factor by factor
    lines += ["## 3. What acclaimed pages have that ordinary ones don't", "", "| factor | acclaimed median | ordinary median | broken median |", "|---|---:|---:|---:|"]
    for k in gk + [f"x_{k}" for k in EXPERIMENTAL]:
        lines.append(f"| {k[2:]} | {np.median(col(A, k)):.2f} | {np.median(col(O, k)):.2f} | {np.median(col(B, k)):.2f} |")
    lines += ["", "## How to read this", "",
              "- An AUC near 0.5 means the signal cannot tell acclaimed design from a random page; near 1.0 it can.",
              "- The `classic` formula was written from the literature, not fitted; the `web` model was fitted to 398 human ratings of 2013-era sites. Neither has seen the acclaimed set. The fitted `ui` formula (research/fit_ui.py, research/FIT.md) was fitted on the acclaimed set, so its numbers here are in-sample; read FIT.md for the cross-validated ones.",
              "- Fitted weights are only worth shipping if the cross-validated AUC beats the shipped weights *and* the human-rating correlation does not fall — both are printed above; the decision is made in the changelog, not here.",
              "- Acclaim is a designer's judgement (Awwwards, Siteinspire, brand lists); it is not the same target as crowd appeal, and the two disagree on purpose."]
    open(os.path.join(HERE, "BENCHMARK.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[:40]))
    print("fitted", fitted, "cv auc", np.mean(cv_auc), "vs", np.mean(cv_base))


if __name__ == "__main__":
    main()
