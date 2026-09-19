"""Score well-known home pages and build demo/famous_sites.png + demo/results_famous.md.

    python demo/famous.py                 # fetch 1280x800 captures via thum.io, score, render
    python demo/famous.py --no-fetch      # reuse demo/famous/*.png from a previous run

Captures are taken by a third-party screenshot service at the moment you run this, so numbers
drift as the sites change; the committed results are dated. Captures that came back blank,
blocked, or covered by a consent dialog are dropped by hand (see SKIP).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import date

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from beautiful import beauty  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "famous")
SITES = [
    "https://www.apple.com/", "https://news.ycombinator.com/", "https://www.notion.com/",
    "https://www.google.com/", "https://www.nytimes.com/", "https://www.craigslist.org/",
    "https://www.figma.com/", "https://www.wikipedia.org/", "https://github.com/",
    "https://www.berkshirehathaway.com/", "https://tailwindcss.com/", "https://www.wired.com/",
    "https://vercel.com/", "https://motherfuckingwebsite.com/", "https://stripe.com/",
    "https://www.amazon.com/", "https://www.airbnb.com/", "https://www.reddit.com/",
    "https://www.bbc.com/", "https://linear.app/",
]
SKIP = {  # bad captures on 2026-09-19 — the service, not the site
    "airbnb.com": "blank capture", "reddit.com": "bot wall", "bbc.com": "consent dialog", "linear.app": "blank capture",
}
COLS, TW, TH, PAD, LABEL_H = 4, 380, 238, 16, 44
FONTS = ["/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "C:/Windows/Fonts/arial.ttf"]


def font(size):
    for p in FONTS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def name_of(url):
    return url.split("//", 1)[1].replace("www.", "").strip("/")


def fetch(url, path):
    api = f"https://image.thum.io/get/width/1280/crop/800/noanimate/{url}"
    with urllib.request.urlopen(api, timeout=120) as r, open(path, "wb") as f:
        f.write(r.read())


def colour(score):
    return (0x1b, 0x8a, 0x3e) if score >= 80 else (0xc7, 0x7d, 0x00) if score >= 60 else (0xc0, 0x1c, 0x1c)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = []
    for url in SITES:
        name = name_of(url)
        if name in SKIP:
            continue
        path = os.path.join(OUT_DIR, name.replace(".", "_").replace("/", "_") + ".png")
        if "--no-fetch" not in sys.argv or not os.path.exists(path):
            print("fetch", url)
            fetch(url, path)
        r = beauty(path, "ui")
        rows.append({"site": name, "score": r["score"], "factors": r["factors"], "hint": r["hints"][-1] if r["hints"] else "", "file": path})
        print(f"{r['score']:3d}  {name}")
    rows.sort(key=lambda x: -x["score"])

    # markdown
    keys = ["composition", "alignment", "simplicity", "whitespace", "harmony", "colorfulness", "contrast"]
    md = [f"Captured {date.today().isoformat()} at 1280×800 via thum.io, scored with `beautiful --mode=ui`.\n",
          "| beauty | site | " + " | ".join(keys) + " |", "|---:|---|" + "---:|" * len(keys)]
    for x in rows:
        md.append(f"| **{x['score']}** | {x['site']} | " + " | ".join(f"{x['factors'][k]:.2f}" for k in keys) + " |")
    md.append("\nSkipped (bad capture, not the site's fault): " + ", ".join(f"{k} ({v})" for k, v in SKIP.items()))
    open(os.path.join(HERE, "results_famous.md"), "w").write("\n".join(md) + "\n")
    json.dump([{k: v for k, v in x.items() if k != "file"} for x in rows], open(os.path.join(HERE, "results_famous.json"), "w"), indent=1)

    # gallery
    n_rows = (len(rows) + COLS - 1) // COLS
    canvas = Image.new("RGB", (COLS * (TW + PAD) + PAD, n_rows * (TH + LABEL_H + PAD) + PAD), "white")
    d = ImageDraw.Draw(canvas)
    f_score, f_label = font(22), font(16)
    for i, x in enumerate(rows):
        im = Image.open(x["file"]).convert("RGB")
        im = im.resize((TW, round(im.height * TW / im.width)), Image.LANCZOS).crop((0, 0, TW, TH))
        cx = PAD + (i % COLS) * (TW + PAD)
        cy = PAD + (i // COLS) * (TH + LABEL_H + PAD)
        d.rectangle([cx - 1, cy - 1, cx + TW, cy + TH], outline=(210, 210, 210))
        canvas.paste(im, (cx, cy))
        d.text((cx, cy + TH + 8), str(x["score"]), fill=colour(x["score"]), font=f_score)
        d.text((cx + 46, cy + TH + 12), x["site"], fill=(40, 40, 40), font=f_label)
    out = os.path.join(HERE, "famous_sites.png")
    canvas.save(out, optimize=True)
    print("wrote", out, canvas.size)


if __name__ == "__main__":
    main()
