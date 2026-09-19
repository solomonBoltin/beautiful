"""Score the images named by INPUT_IMAGES (globs), write a markdown table to beautiful-table.md
and to $GITHUB_OUTPUT (table, min-score), append it to the job summary, and exit 1 below INPUT_MIN."""
import glob
import os
import sys

from beautiful import beauty

for _stream in (sys.stdout, sys.stderr):  # the table has emoji; a cp1252 console (Windows) must not crash on it
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

mode = os.environ.get("INPUT_MODE", "ui") or "ui"
min_req = os.environ.get("INPUT_MIN", "").strip()
files = sorted({f for g in os.environ["INPUT_IMAGES"].split() for f in glob.glob(g, recursive=True)})
if not files:
    print("beautiful: no images matched", os.environ["INPUT_IMAGES"], file=sys.stderr)
    sys.exit(1)

keys = ["composition", "alignment", "simplicity", "whitespace", "harmony", "contrast"]
rows, lowest = [], 100
for f in files:
    r = beauty(f, mode)
    lowest = min(lowest, r["score"])
    hint = next((h for h in r["hints"] if "(" in h), r["hints"][0] if r["hints"] else "")
    rows.append((r["score"], f, r["factors"], hint))
rows.sort(key=lambda x: -x[0])

def badge(s):
    return "🟢" if s >= 80 else "🟡" if s >= 60 else "🔴"

lines = ["<!-- beautiful-score -->", f"### beauty scores (`--mode={mode}`)", "",
         "| | beauty | image | " + " | ".join(keys) + " | weakest factor |",
         "|:-:|---:|---|" + "---:|" * len(keys) + "---|"]
for s, f, fac, hint in rows:
    lines.append(f"| {badge(s)} | **{s}** | `{f}` | " + " | ".join(f"{fac.get(k, 0):.2f}" for k in keys) + f" | {hint} |")
lines += ["", "<sub>1–100, computed from pixels alone by [beautiful](https://github.com/solomonBoltin/beautiful). "
              "Differences under 3 points are noise.</sub>"]
table = "\n".join(lines)
print(table)
open("beautiful-table.md", "w", encoding="utf-8").write(table + "\n")
if "GITHUB_OUTPUT" in os.environ:
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as out:
        out.write(f"min-score={lowest}\n")
        out.write("table<<BEAUTIFUL_EOF\n" + table + "\nBEAUTIFUL_EOF\n")
if "GITHUB_STEP_SUMMARY" in os.environ:
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as s:
        s.write(table + "\n")
if min_req and lowest < int(min_req):
    print(f"::error::lowest beauty score {lowest} is below the required minimum {min_req}")
    sys.exit(1)
