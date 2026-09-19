"""Command line: ``beautiful`` (installed script) or ``python -m beautiful``.

    beautiful screen.png                    one image: score, factors, hints
    beautiful --mode=art a.jpg b.jpg        several images: scores only
    beautiful --json screen.png             the full report as JSON
    beautiful --min 70 screen.png           exit 1 below 70 (a CI gate)
"""
from __future__ import annotations

import argparse
import json
import sys

from .core import WEIGHTS, beauty


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="beautiful",
        description="A beauty number, 1-100, for any image - computed from pixels alone.",
    )
    p.add_argument("images", nargs="+", help="PNG / JPEG / WebP paths")
    p.add_argument("--mode", choices=list(WEIGHTS), default="ui",
                   help="ui = screens and pages (default), art = paintings/photos/posters, logo = marks and icons")
    p.add_argument("--json", action="store_true", help="print the full report(s) as JSON")
    p.add_argument("--min", type=int, default=None, metavar="N",
                   help="exit with status 1 if any image scores below N")
    a = p.parse_args(argv)

    # Hints contain characters such as "≈"; a cp1252 console (Windows) must not crash on them.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")

    reports = {}
    worst = 100
    for path in a.images:
        r = beauty(path, a.mode)
        reports[path] = r
        worst = min(worst, r["score"])
        if a.json:
            continue
        print(f"{r['score']:3d}  {path}")
        if len(a.images) == 1:
            for k, v in r["factors"].items():
                print(f"      {k:<14}{v:.2f}")
            for h in r["hints"]:
                print(f"  ->  {h}")

    if a.json:
        out = reports[a.images[0]] if len(a.images) == 1 else reports
        print(json.dumps(out, indent=2, ensure_ascii=False))

    if a.min is not None and worst < a.min:
        print(f"beautiful: lowest score {worst} is below the required minimum {a.min}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
