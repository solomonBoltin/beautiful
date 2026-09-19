"""beautiful — the beauty lint.

    beautiful screen.png                       one image: score, factors, hints
    beautiful shots/ --mode=ui                 every PNG/JPEG/WebP in a directory
    beautiful --min 70 shots/*.png             exit 1 below 70 (a gate)
    beautiful --format json|github|sarif ...   machine-readable, CI annotations, code scanning
    beautiful --save-baseline b.json shots/    remember today's scores
    beautiful --baseline b.json shots/         fail on any regression > 3 points
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

from . import __version__
from .core import MODES, beauty

IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff")

ADVICE_URL = "https://github.com/solomonBoltin/beautiful#the-formula"


def expand(paths):
    """Files, directories (recursive) and globs -> a sorted list of image files."""
    out = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                out += [os.path.join(root, f) for f in files if f.lower().endswith(IMAGE_EXT)]
        elif any(ch in p for ch in "*?["):
            out += [g for g in glob.glob(p, recursive=True) if g.lower().endswith(IMAGE_EXT)]
        else:
            out.append(p)
    return sorted(dict.fromkeys(out))


def findings(path, r, min_score):
    """Lint findings for one image: one per hint, plus a score finding."""
    level_score = "error" if (min_score is not None and r["score"] < min_score) else \
        "warning" if r["score"] < 70 else "note"
    out = [{"rule": "score", "level": level_score, "path": path,
            "message": f"beauty {r['score']}/100 ({r['mode']} mode)"}]
    for h in r["hints"]:
        factor = h.split(" (", 1)[0] if " (" in h and h.split(" (", 1)[0] in r["factors"] else "composition"
        value = r["factors"].get(factor)
        lvl = "warning" if value is not None and value < 0.5 else "note"
        out.append({"rule": factor, "level": lvl, "path": path, "message": h})
    return out


def to_sarif(results, min_score):
    rules = {}
    sarif_results = []
    for path, r in results.items():
        for f in findings(path, r, min_score):
            rid = f"beautiful/{f['rule']}"
            rules.setdefault(rid, {
                "id": rid, "name": f["rule"],
                "shortDescription": {"text": f"beautiful: {f['rule']}"},
                "helpUri": ADVICE_URL,
                "properties": {"tags": ["design", "aesthetics"]},
            })
            sarif_results.append({
                "ruleId": rid, "level": f["level"],
                "message": {"text": f["message"]},
                "locations": [{"physicalLocation": {"artifactLocation": {"uri": path.replace(os.sep, "/")}}}],
                "properties": {"score": r["score"], "mode": r["mode"], "factors": r["factors"]},
            })
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json", "version": "2.1.0",
        "runs": [{"tool": {"driver": {"name": "beautiful", "version": __version__,
                                       "informationUri": "https://github.com/solomonBoltin/beautiful",
                                       "rules": list(rules.values())}},
                  "results": sarif_results}],
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="beautiful",
        description="A mathematical beauty score, 1-100, for any image - and a lint for the design it shows.",
    )
    p.add_argument("images", nargs="+", help="image files, directories (recursive) or globs")
    p.add_argument("--mode", choices=MODES, default="ui",
                   help="ui = screens and pages (default), art = paintings/photos/posters, logo = marks and icons, web = calibrated on human ratings of websites (advisory)")
    p.add_argument("--format", choices=["text", "json", "github", "sarif"], default="text",
                   help="text (default) | json (full reports) | github (workflow annotations) | sarif (code scanning)")
    p.add_argument("--json", action="store_true", help="shorthand for --format json")
    p.add_argument("--min", type=int, default=None, metavar="N", help="exit 1 if any image scores below N")
    p.add_argument("--baseline", metavar="FILE", help="JSON of previous scores; exit 1 on a regression")
    p.add_argument("--save-baseline", metavar="FILE", help="write the scores of this run as a baseline")
    p.add_argument("--tolerance", type=int, default=3, help="points a score may drop before it is a regression (default 3)")
    p.add_argument("--version", action="version", version=f"beautiful {__version__}")
    a = p.parse_args(argv)
    fmt = "json" if a.json else a.format

    for stream in (sys.stdout, sys.stderr):  # hints contain "≈" etc.; cp1252 consoles must not crash
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")

    files = expand(a.images)
    if not files:
        print("beautiful: no images found", file=sys.stderr)
        return 2

    results, failures = {}, []
    for path in files:
        try:
            r = beauty(path, a.mode)
        except Exception as e:  # keep linting the rest
            failures.append(f"{path}: {type(e).__name__}: {e}")
            continue
        results[path] = r
        if fmt == "text":
            print(f"{r['score']:3d}  {path}")
            if len(files) == 1:
                for k, v in r["factors"].items():
                    print(f"      {k:<14}{v:.2f}")
                for h in r["hints"]:
                    print(f"  ->  {h}")
        elif fmt == "github":
            for f in findings(path, r, a.min):
                lvl = {"error": "error", "warning": "warning", "note": "notice"}[f["level"]]
                print(f"::{lvl} file={path},title=beautiful {r['score']} · {f['rule']}::{f['message']}")

    if fmt == "json":
        out = results[files[0]] if len(files) == 1 and files[0] in results else results
        print(json.dumps(out, indent=2, ensure_ascii=False))
    elif fmt == "sarif":
        print(json.dumps(to_sarif(results, a.min), indent=1))

    rc = 0
    for msg in failures:
        print("beautiful: could not score " + msg, file=sys.stderr)
        rc = 2

    worst = min((r["score"] for r in results.values()), default=100)
    if a.min is not None and worst < a.min:
        print(f"beautiful: lowest score {worst} is below the required minimum {a.min}", file=sys.stderr)
        rc = 1

    if a.baseline:
        try:
            base = json.load(open(a.baseline, encoding="utf-8"))
        except FileNotFoundError:
            base = {}
            print(f"beautiful: no baseline at {a.baseline} yet (will be created by --save-baseline)", file=sys.stderr)
        regressions = [(k, base[k], r["score"]) for k, r in results.items()
                       if k in base and r["score"] < base[k] - a.tolerance]
        for k, old, new in regressions:
            print(f"beautiful: regression {k}: {old} -> {new}", file=sys.stderr)
        if regressions:
            rc = 1
    if a.save_baseline:
        json.dump({k: r["score"] for k, r in results.items()},
                  open(a.save_baseline, "w", encoding="utf-8"), indent=1, sort_keys=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
