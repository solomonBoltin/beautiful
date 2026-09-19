"""Re-score every demo artefact with the current formula, so the numbers in the repo are the
numbers the code produces.

    python demo/rescore.py            # results_ui.json/md, results_art.md, ui_gallery.png,
                                      # famous (cached captures), hall of fame (cached captures)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from beautiful import beauty  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = ["composition", "alignment", "contrast", "harmony", "whitespace", "congestion", "contour", "hierarchy", "margin"]  # the fitted `ui` terms shown in the README table


def ui():
    rows = json.load(open(os.path.join(HERE, "results_ui.json")))
    labels = {r["file"]: r["label"] for r in rows}
    labels.setdefault("medium_home.png", "medium.com — home (live, rendered with beautiful.render)")
    out = []
    for f in sorted(os.listdir(os.path.join(HERE, "screens"))):
        if not f.endswith(".png"):
            continue
        r = beauty(os.path.join(HERE, "screens", f), "ui")
        out.append({"file": f, "label": labels.get(f, f), "score": r["score"], "classic": r["classic"]["score"], "factors": r["factors"], "hints": r["hints"]})
    out.sort(key=lambda x: -x["score"])
    json.dump(out, open(os.path.join(HERE, "results_ui.json"), "w"), indent=1, ensure_ascii=False)
    md = ["| `ui` | `classic` | screen | " + " | ".join(KEYS) + " |", "|---:|---:|---|" + "---:|" * len(KEYS)]
    for x in out:
        md.append(f"| **{x['score']}** | {x['classic']} | {x['label']} | " + " | ".join(f"{x['factors'][k]:.2f}" for k in KEYS) + " |")
    open(os.path.join(HERE, "results_ui.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("ui:", [(x["score"], x["file"]) for x in out])


def art():
    order = ["mandala_radial", "shield_logo", "checker", "leaf", "random_blobs", "diagonal_composition", "abstract_splashes", "random_noise"]
    rows = []
    for n in order:
        p = os.path.join(HERE, "art", n + ".png")
        a, l = beauty(p, "art"), beauty(p, "logo")
        rows.append((a["score"], l["score"], n, a["factors"], a["raw"]))
    rows.sort(key=lambda x: -x[0])
    md = ["| beauty (art) | beauty (logo) | image | composition | harmony | simplicity | fractal | fourier | thirds |",
          "|---:|---:|---|---:|---:|---:|---:|---:|---:|"]
    for a, l, n, f, raw in rows:
        md.append(f"| **{a}** | {l} | {n} | {f['composition']:.2f} | {f['harmony']:.2f} | {f['simplicity']:.2f} | "
                  f"{f['fractal']:.2f} (D={raw['fractal_dimension']:.2f}) | {f['fourier']:.2f} (α={raw['fourier_slope']:.2f}) | {f['thirds']:.2f} |")
    open(os.path.join(HERE, "results_art.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    json.dump([{"image": n, "art": a, "logo": l, "factors": f} for a, l, n, f, _ in rows],
              open(os.path.join(HERE, "results_art.json"), "w"), indent=1)
    print("art:", [(a, l, n) for a, l, n, _, _ in rows])


def famous_web():
    rows = json.load(open(os.path.join(HERE, "results_famous.json")))
    out = []
    for x in rows:
        p = os.path.join(HERE, "famous", x["site"].replace(".", "_") + ".png")
        if os.path.exists(p):
            out.append({"site": x["site"], "web": beauty(p, "web")["score"], "ui": beauty(p, "ui")["score"]})
    out.sort(key=lambda r: -r["web"])
    json.dump(out, open(os.path.join(HERE, "results_famous_web.json"), "w"), indent=1)


if __name__ == "__main__":
    py = sys.executable
    ui()
    art()
    subprocess.run([py, os.path.join(HERE, "make_gallery.py")], check=True)
    if os.path.isdir(os.path.join(HERE, "famous")):
        subprocess.run([py, os.path.join(HERE, "famous.py"), "--no-fetch"], check=True)
        famous_web()
    if os.path.isdir(os.path.join(HERE, "hall")):
        subprocess.run([py, os.path.join(HERE, "hall_of_fame.py"), "--no-fetch"], check=True)
