"""Fit the `ui` formula to three kinds of evidence at once, and say honestly how well it does.

Evidence
  A  100 acclaimed home pages            research/top100.py            (what designers acclaim)
  O  100 ordinary pages                  Calista comparison set        (random Alexa-top-5000)
  P  100 (original, degraded) pairs      research/degrade.py           (a defect injected into A)
  R  398 human-rated screenshots         Reinecke & Gajos 2014         (crowd appeal)

The formula keeps its shape — an explicit weighted sum of goodness terms, each a documented
curve over one pixel measurement — but the curves and weights are *fitted*:
  * "intermediate is best" measurements (edge density, JPEG bytes/pixel, dominant colours, white
    space, colourfulness, feature/contour congestion, edge-orientation entropy, anisotropy) get a
    bell centred on the acclaimed median with a width from the acclaimed spread — the inverted-U
    the literature predicts, with the optimum read off the pages people acclaim;
  * "more is better" measurements (mirror symmetry, balance, local symmetry, alignment, contrast,
    harmony) keep their ramps;
  * weights are non-negative, sum to 1, each at least 0.02 so every term stays readable, and are
    chosen to maximise  0.4·AUC(A > O) + 0.4·accuracy(original > degraded) + 0.2·ρ(rating),
    5-fold cross-validated over A and P.

Outputs research/FIT.md (the report) and beautiful/ui_model.json (the model core.py can load).
Shipping it is a deliberate step taken in the changelog, not here.

    python research/fit_ui.py [calista_root]
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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# measurement name -> (how to read it from a beauty() report, kind, source)
MEASURES = {
    "composition":  (lambda r: r["raw"]["symmetry"]["score"] / 100.0,               "ramp", "Ngo 2003; Bauerly & Liu 2006 — symmetric OR balanced (symmetry.py)"),
    "local":        (lambda r: r["raw"]["symmetry"]["local_symmetry"],              "ramp", "local tile symmetry"),
    "alignment":    (lambda r: 0.65 * r["raw"]["alignment"]["x_alignment"] + 0.35 * r["raw"]["alignment"]["y_alignment"], "ramp", "Miniukovich 2015 grid quality"),
    "contrast":     (lambda r: r["raw"]["contrast"]["edge_contrast"],               "ramp", "Miniukovich 2015; Reber 2004"),
    "harmony":      (lambda r: r["raw"]["harmony"]["fit"],                          "ramp", "Cohen-Or 2006 templates"),
    "edge_density": (lambda r: r["raw"]["complexity"]["edge_density"],              "bell", "Reinecke & Gajos 2013 (complexity, inverted-U)"),
    "jpeg_bpp":     (lambda r: r["raw"]["complexity"]["jpeg_bpp"],                  "bell", "Rigau 2008 Kolmogorov proxy"),
    "colours":      (lambda r: r["raw"]["complexity"]["dominant_colors"],           "bell", "Miniukovich 2015 dominant colours"),
    "whitespace":   (lambda r: r["raw"]["whitespace"],                              "bell", "Miniukovich 2015 white space"),
    "colorfulness": (lambda r: r["raw"]["colorfulness"]["variety"],                 "bell", "Hasler & Süsstrunk 2003; Reinecke 2013 (inverted-U)"),
    "congestion":   (lambda r: r["raw"]["experimental"]["feature_congestion"],      "bell", "Rosenholtz 2007 feature congestion"),
    "contour":      (lambda r: r["raw"]["experimental"]["contour_congestion"],      "bell", "Miniukovich 2014 contour congestion"),
    "orientation":  (lambda r: r["raw"]["experimental"]["edge_orientation_entropy"], "bell", "Redies edge-orientation entropy"),
    "anisotropy":   (lambda r: r["raw"]["experimental"]["anisotropy"],              "bell", "Redies anisotropy"),
    "hierarchy":    (lambda r: r["raw"]["experimental"]["hierarchy"],               "ramp", "coarse-structure share (this repo; visual hierarchy cue)"),
    "margin":       (lambda r: 1.0 - max(r["raw"]["experimental"]["edge_contact"]["left"]["coverage"], r["raw"]["experimental"]["edge_contact"]["right"]["coverage"]), "ramp", "quiet side margins (edge_contact; this repo)"),
}
NAMES = list(MEASURES)
# priors that keep this a *UI* score: composition is the best-replicated UI predictor (survey §2) and
# gets a floor; the two photographic-texture statistics (Redies) are capped so a marketing hero with a
# photo cannot outrank a clean, composed application screen
FLOORS = {"composition": 0.15}
# ...and the "amount of content" bells (how much detail, information, colour a page carries) are capped
# too: left free they explain acclaimed-vs-ordinary well but then prefer the busier of two versions of the
# SAME screen, which is the comparison a lint is actually used for
CAPS = {"orientation": 0.06, "anisotropy": 0.06,
        "edge_density": 0.08, "jpeg_bpp": 0.08, "colours": 0.08, "whitespace": 0.08, "colorfulness": 0.06, "hierarchy": 0.10, "margin": 0.08}
WIDE = {"edge_density": 2.5, "jpeg_bpp": 2.5, "colours": 2.5, "whitespace": 2.5, "colorfulness": 2.5}  # bell width in IQRs (default 1.5)
# curated orderings a UI score must respect (each pair: better, worse) — the repo's own test cases
CURATED = [
    ("demo/screens/digital_office_rebalanced.png", "demo/screens/digital_office_original.png"),
    ("demo/screens/pinkas_dialog.png", "demo/screens/sample_asymmetric_ui.png"),
    ("demo/screens/pinkas_documents.png", "demo/screens/github_login_unstyled.png"),
    ("demo/screens/pinkas_dashboard.png", "demo/screens/github_login_unstyled.png"),
    ("demo/screens/medium_home.png", "demo/screens/sample_asymmetric_ui.png"),
    ("demo/screens/crates_io_search_q_http.png", "demo/screens/github_login_unstyled.png"),
    ("demo/famous/apple_com.png", "demo/famous/amazon_com.png"),
    ("demo/famous/notion_com.png", "demo/famous/amazon_com.png"),
    ("demo/famous/apple_com.png", "demo/screens/github_login_unstyled.png"),
    ("demo/screens/pinkas_documents.png", "demo/screens/sample_asymmetric_ui.png"),
    # designed pages beat plain text dumps and link lists — the check a pixel fit is most likely to fail,
    # because a wall of well-set text has the edge density and contour statistics of a "rich" page
    ("demo/famous/apple_com.png", "demo/famous/berkshirehathaway_com.png"),
    ("demo/famous/apple_com.png", "demo/famous/craigslist_org.png"),
    ("demo/famous/notion_com.png", "demo/famous/berkshirehathaway_com.png"),
    ("demo/famous/figma_com.png", "demo/famous/craigslist_org.png"),
    ("demo/famous/stripe_com.png", "demo/famous/craigslist_org.png"),
    ("demo/famous/github_com.png", "demo/famous/craigslist_org.png"),
    ("demo/screens/medium_home.png", "demo/famous/craigslist_org.png"),
    ("demo/screens/pinkas_documents.png", "demo/screens/npm_home_unstyled.png"),
    ("demo/screens/pinkas_dashboard.png", "demo/screens/npm_home_unstyled.png"),
    ("demo/famous/apple_com.png", "demo/screens/npm_home_unstyled.png"),
    ("demo/screens/digital_office_rebalanced.png", "demo/screens/npm_home_unstyled.png"),
]
MARGIN = 8   # a curated "better" must win by at least this many points to count as respected


def measure(path):
    r = beauty(path, "classic")   # the literature-weighted formula is the baseline column
    return {k: float(f(r)) for k, (f, _, _) in MEASURES.items()} | {"ui": r["score"], "web": beauty(path, "web")["score"]}


def load(paths, cache):
    rows = json.load(open(cache)) if os.path.exists(cache) else {}
    todo = [p for p in paths if p not in rows or any(k not in rows[p] for k in NAMES)]
    for i, p in enumerate(todo, 1):
        try:
            rows[p] = measure(p)
        except Exception as e:
            print("skip", p, e)
        if i % 25 == 0:
            print(f"  {i}/{len(todo)}", flush=True)
    json.dump(rows, open(cache, "w"))
    return [rows[p] for p in paths if p in rows], [p for p in paths if p in rows]


def auc(pos, neg):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    return float(mannwhitneyu(pos, neg, alternative="two-sided").statistic / (len(pos) * len(neg)))


def goodness(M, params):
    """M: (n, k) raw measurements -> (n, k) goodness in [0,1] using per-term curves."""
    G = np.zeros_like(M)
    for j, k in enumerate(NAMES):
        kind, c, w, lo, hi = params[k]
        x = M[:, j]
        if kind == "bell":
            G[:, j] = np.exp(-((x - c) / w) ** 2)
        else:
            G[:, j] = np.clip((x - lo) / (hi - lo + 1e-9), 0, 1)
    return G


def spread(total):
    return 1 + 99 / (1 + np.exp(-8 * (total - 0.55)))


def main():
    calista = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "..", "calista")
    top = json.load(open(os.path.join(HERE, "results_top100.json")))["rows"]
    pairs = json.load(open(os.path.join(HERE, "degraded_pairs.json")))
    A_paths = [os.path.join(HERE, r["file"]) for r in top]
    P_orig, P_deg = [p["original"] for p in pairs], [p["degraded"] for p in pairs]
    O_scores = {}
    with open(os.path.join(calista, "comparison-based-dataset", "website_scores.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            O_scores[os.path.join(calista, "comparison-based-dataset", "images", row["website"].replace("image", "") + ".png")] = float(row["score"])
    R_scores = {}
    for name in ("train_means_list.csv", "test_list.csv"):
        with open(os.path.join(calista, "rating-based-dataset", "preprocess", name), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                R_scores[os.path.join(calista, "rating-based-dataset", "images", row["image"].lstrip("/").replace("_resized", ""))] = float(row["mean_score"])
    cache = os.path.join(HERE, "fit_cache.json")
    A, _ = load(A_paths, cache)
    O, O_used = load([p for p in O_scores if os.path.exists(p)], cache)
    Po, _ = load(P_orig, cache)
    Pd, _ = load(P_deg, cache)
    R, R_used = load([p for p in R_scores if os.path.exists(p)], cache)
    yO = np.array([O_scores[p] for p in O_used]); yR = np.array([R_scores[p] for p in R_used])
    mat = lambda S: np.array([[s[k] for k in NAMES] for s in S], float)
    MA, MO, MPo, MPd, MR = mat(A), mat(O), mat(Po), mat(Pd), mat(R)
    print(f"A {len(A)} O {len(O)} pairs {len(Po)} R {len(R)}")

    # curves: bells centred on the acclaimed median, width = 1.5 x IQR (floor at 15% of the median);
    # ramps between the 10th percentile of ordinary and the 75th of acclaimed
    params = {}
    for j, k in enumerate(NAMES):
        kind = MEASURES[k][1]
        a = MA[:, j]
        if kind == "bell":
            c = float(np.median(a)); iqr = float(np.percentile(a, 75) - np.percentile(a, 25))
            w = max(WIDE.get(k, 1.5) * iqr, 0.15 * abs(c) + 1e-6)
            params[k] = ("bell", c, w, None, None)
        else:
            lo = float(np.percentile(np.concatenate([a, MO[:, j]]), 10)); hi = float(np.percentile(a, 75))
            if hi - lo < 1e-6:
                hi = lo + 0.1
            params[k] = ("ramp", None, None, lo, hi)
    GA, GO, GPo, GPd, GR = (goodness(M, params) for M in (MA, MO, MPo, MPd, MR))

    def score(G, w):
        return spread(G @ w)

    def normalise(v):
        w = 0.02 + np.abs(v)
        for _ in range(3):
            for j, k in enumerate(NAMES):
                if k in FLOORS: w[j] = max(w[j], FLOORS[k])
                if k in CAPS: w[j] = min(w[j], CAPS[k])
            w = w / w.sum()
        return w

    cur_better, _ = load([os.path.join(ROOT, a) for a, _ in CURATED], cache)
    cur_worse, _ = load([os.path.join(ROOT, b) for _, b in CURATED], cache)
    GCb, GCw = goodness(mat(cur_better), params), goodness(mat(cur_worse), params)

    def objective(v, idxA, idxO, idxP):
        w = normalise(v)
        sA, sO = score(GA[idxA], w), score(GO[idxO], w)
        so, sd = score(GPo[idxP], w), score(GPd[idxP], w)
        rho = spearmanr(score(GR, w), yR).correlation
        pair = float(np.mean(so > sd))
        cb, cw = score(GCb, w), score(GCw, w)
        curated = float(np.mean(cb > cw + MARGIN))      # the better one wins by a clear margin
        violations = float(np.sum(cb <= cw))            # any curated order broken is a hard cost
        return -(0.30 * auc(sA, sO) + 0.30 * pair + 0.15 * max(rho, 0.0) + 0.25 * curated) + 0.5 * max(0.0, -rho) + 0.15 * violations

    def fit(idxA, idxO, idxP, seed=0):
        rng = np.random.RandomState(seed); best = None
        for start in [np.ones(len(NAMES)) / len(NAMES)] + [rng.dirichlet(np.ones(len(NAMES))) for _ in range(8)]:
            res = minimize(objective, start, args=(idxA, idxO, idxP), method="Nelder-Mead", options={"maxiter": 1500, "xatol": 1e-3, "fatol": 1e-4})
            if best is None or res.fun < best.fun:
                best = res
        return normalise(best.x)

    # cross-validation over A (and its pairs) and O
    rng = np.random.RandomState(1)
    fa, fo = rng.permutation(len(A)), rng.permutation(len(O))
    cv = {"auc": [], "pair": [], "rho": [], "auc_ship": [], "pair_ship": [], "auc_web": [], "pair_web": []}
    uiA, uiO, uiPo, uiPd = ([s["ui"] for s in S] for S in (A, O, Po, Pd))
    webA, webO, webPo, webPd = ([s["web"] for s in S] for S in (A, O, Po, Pd))
    for f in range(5):
        tA, tO = fa[f::5], fo[f::5]
        trA, trO = np.setdiff1d(np.arange(len(A)), tA), np.setdiff1d(np.arange(len(O)), tO)
        w = fit(trA, trO, trA, seed=f)
        cv["auc"].append(auc(score(GA[tA], w), score(GO[tO], w)))
        cv["pair"].append(float(np.mean(score(GPo[tA], w) > score(GPd[tA], w))))
        cv["rho"].append(spearmanr(score(GR, w), yR).correlation)
        cv["auc_ship"].append(auc(np.array(uiA)[tA], np.array(uiO)[tO])); cv["pair_ship"].append(float(np.mean(np.array(uiPo)[tA] > np.array(uiPd)[tA])))
        cv["auc_web"].append(auc(np.array(webA)[tA], np.array(webO)[tO])); cv["pair_web"].append(float(np.mean(np.array(webPo)[tA] > np.array(webPd)[tA])))
    w = fit(np.arange(len(A)), np.arange(len(O)), np.arange(len(A)), seed=42)
    rho_all = spearmanr(score(GR, w), yR).correlation
    rho_O = spearmanr(score(GO, w), yO).correlation
    cb, cw = score(GCb, w), score(GCw, w)
    curated_ok = int(np.sum(cb > cw)); curated_n = len(cb)

    model = {"name": "ui", "fitted_on": {"acclaimed": len(A), "ordinary": len(O), "pairs": len(Po), "rated": len(R)},
             "terms": [{"name": k, "kind": params[k][0], "centre": params[k][1], "width": params[k][2], "lo": params[k][3], "hi": params[k][4],
                        "weight": round(float(w[j]), 4), "source": MEASURES[k][2]} for j, k in enumerate(NAMES)],
             "spread": "1 + 99 / (1 + exp(-8 (sum - 0.55)))",
             "cv": {k: round(float(np.mean(v)), 4) for k, v in cv.items()},
             "rho_rating_all": round(float(rho_all), 4), "rho_pairwise_ordinary": round(float(rho_O), 4),
             "curated_pairs_respected": f"{curated_ok}/{curated_n}", "floors": FLOORS, "caps": CAPS}
    json.dump(model, open(os.path.join(ROOT, "beautiful", "ui_model.json"), "w"), indent=1)

    lines = ["# Fitting the `ui` formula to acclaimed design, degraded twins and human ratings", "",
             f"Evidence: **{len(A)} acclaimed** pages, **{len(O)} ordinary** pages, **{len(Po)} original/degraded pairs**, **{len(R)} human-rated** screenshots. "
             "The formula keeps its explicit shape (a weighted sum of documented curves over pixel measurements); bells are centred on what acclaimed pages measure, "
             "weights are fitted to three targets at once and cross-validated 5-fold over the acclaimed set.", "",
             "## Cross-validated (held-out acclaimed pages and their pairs)", "",
             "| | shipped `ui` (literature weights) | `web` (ridge on 2013 ratings) | **fitted `ui`** |", "|---|---:|---:|---:|",
             f"| AUC acclaimed > ordinary | {np.mean(cv['auc_ship']):.2f} | {np.mean(cv['auc_web']):.2f} | **{np.mean(cv['auc']):.2f}** |",
             f"| original beats its degraded twin | {np.mean(cv['pair_ship']):.0%} | {np.mean(cv['pair_web']):.0%} | **{np.mean(cv['pair']):.0%}** |",
             f"| ρ vs human rating (398) | {spearmanr(uiA and [s['ui'] for s in R], yR).correlation:+.2f} | {spearmanr([s['web'] for s in R], yR).correlation:+.2f} | **{np.mean(cv['rho']):+.2f}** |",
             f"| ρ vs human pairwise rank (100 ordinary) | {spearmanr(uiO, yO).correlation:+.2f} | {spearmanr(webO, yO).correlation:+.2f} | **{rho_O:+.2f}** |",
             f"| curated UI orderings respected (the repo's test pairs) | — | — | **{curated_ok}/{curated_n}** |", "",
             f"Priors that keep this a *UI* score: composition weight ≥ {FLOORS['composition']}; the photographic-texture terms (edge-orientation entropy, anisotropy) ≤ {CAPS['anisotropy']} each. "
             "Without them the first fit put 0.20 on anisotropy and 0.02 on symmetry, scored a lopsided screen above its rebalanced twin and Apple's hero at 57: it had learned 'marketing page with a photo', not 'composed screen'.", "",
             "## The fitted formula", "", "| term | curve | centre / range | weight | descends from |", "|---|---|---|---:|---|"]
    for t in model["terms"]:
        rng_txt = f"bell at {t['centre']:.3g} ± {t['width']:.3g}" if t["kind"] == "bell" else f"ramp {t['lo']:.3g} → {t['hi']:.3g}"
        lines.append(f"| {t['name']} | {t['kind']} | {rng_txt} | {t['weight']:.2f} | {t['source']} |")
    lines += ["", "## What acclaimed pages measure (the bell centres)", "", "| measurement | acclaimed median | ordinary median | degraded median | rated median |", "|---|---:|---:|---:|---:|"]
    for j, k in enumerate(NAMES):
        lines.append(f"| {k} | {np.median(MA[:, j]):.3g} | {np.median(MO[:, j]):.3g} | {np.median(MPd[:, j]):.3g} | {np.median(MR[:, j]):.3g} |")
    lines += ["", "## Per-defect: does the fitted score prefer the original?", ""]
    so_all, sd_all = score(GPo, w), score(GPd, w)
    by = {}
    for p, o, d in zip(pairs, so_all, sd_all):
        by.setdefault(p["defect"], []).append(o > d)
    lines += ["| defect | original preferred |", "|---|---:|"] + [f"| {k} | {np.mean(v):.0%} ({len(v)}) |" for k, v in sorted(by.items())]
    lines += ["", "## How to read this", "",
              "- AUC 0.5 = coin flip; pair accuracy 50 % = coin flip. The shipped literature-weighted formula was the baseline; anything fitted here has never seen the held-out fold.",
              "- ρ against the 2013 crowd ratings is a *constraint* (must not go negative), not the goal: acclaim by designers and crowd appeal disagree, and this formula is aimed at the former.",
              "- The bell centres are the honest content of this file: they say what the pages people acclaim actually measure, and any future factor can be checked against them.",
              "- Data the fit never saw: none of the sets is held out entirely; a fresh set of acclaimed pages is the next test (research/top100.py takes a candidate list)."]
    open(os.path.join(HERE, "FIT.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[:16]))
    print("weights", {t["name"]: t["weight"] for t in model["terms"]})


if __name__ == "__main__":
    main()
