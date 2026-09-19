"""Find the most beautiful public home pages by the formula: render candidates with headless
Chromium at 1280×800 (deterministic, no third-party screenshot service), score with `ui` and
`web`, and build demo/hall_of_fame.png + demo/results_hall_of_fame.md from the top scorers.

    pip install "beautiful-score[render]" && playwright install chromium
    python demo/hall_of_fame.py                 # ~5 min for the candidate list below
    python demo/hall_of_fame.py --no-fetch      # reuse demo/hall/*.png

Candidates are sites people cite for design (product, tool, agency, editorial, institutional).
Add yours; the point is to find what a *high* score looks like on the real web.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from beautiful import beauty  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "hall")
CANDIDATES = [
    "https://www.apple.com/", "https://linear.app/", "https://www.raycast.com/", "https://arc.net/",
    "https://www.framer.com/", "https://webflow.com/", "https://cal.com/", "https://resend.com/",
    "https://clerk.com/", "https://supabase.com/", "https://railway.com/", "https://render.com/",
    "https://www.radix-ui.com/", "https://ui.shadcn.com/", "https://basecamp.com/", "https://www.hey.com/",
    "https://www.craft.do/", "https://culturedcode.com/things/", "https://bear.app/", "https://ia.net/",
    "https://www.dropbox.com/", "https://www.spotify.com/", "https://www.nike.com/", "https://www.tesla.com/",
    "https://www.porsche.com/international/", "https://www.muji.com/", "https://www.aesop.com/",
    "https://teenage.engineering/", "https://www.gov.uk/", "https://medium.com/", "https://substack.com/",
    "https://ghost.org/", "https://mailchimp.com/", "https://www.intercom.com/", "https://slack.com/",
    "https://dribbble.com/", "https://www.awwwards.com/", "https://www.are.na/", "https://readwise.io/",
    "https://obsidian.md/", "https://www.warp.dev/", "https://zed.dev/", "https://cursor.com/",
    "https://www.anthropic.com/", "https://openai.com/", "https://mistral.ai/", "https://huggingface.co/",
    "https://kagi.com/", "https://duckduckgo.com/", "https://proton.me/", "https://signal.org/",
    "https://www.mozilla.org/", "https://brave.com/", "https://1password.com/", "https://bitwarden.com/",
    "https://stripe.com/", "https://www.figma.com/", "https://www.notion.com/", "https://vercel.com/",
    "https://tailwindcss.com/", "https://www.airbnb.com/", "https://www.pinterest.com/", "https://unsplash.com/",
    "https://www.behance.net/", "https://www.canva.com/", "https://www.loom.com/", "https://pitch.com/",
    "https://www.superhuman.com/", "https://www.lattice.com/", "https://posthog.com/", "https://sentry.io/",
    "https://www.docker.com/", "https://www.rust-lang.org/", "https://go.dev/", "https://www.python.org/",
    "https://www.swift.org/", "https://svelte.dev/", "https://astro.build/", "https://remix.run/",
]
# what the crawler actually captured on 2026-09-19 instead of the page — dropped by hand
SKIP = {
    "medium.com": "bot wall ('you have been blocked')", "unsplash.com": "bot wall ('access denied')",
    "behance.net": "rate-limit page", "porsche.com_international": "consent dialog over the page",
    "awwwards.com": "consent dialog over the page", "openai.com": "blank capture",
    "canva.com": "maintenance page",
}
COLS, TW, TH, PAD, LABEL_H, TOP_N = 4, 380, 238, 16, 44, 16
FONTS = ["/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf"]


def font(size):
    for p in FONTS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def name_of(url):
    return url.split("//", 1)[1].replace("www.", "").strip("/").replace("/", "_")


def colour(score):
    return (0x1b, 0x8a, 0x3e) if score >= 80 else (0xc7, 0x7d, 0x00) if score >= 60 else (0xc0, 0x1c, 0x1c)


def main():
    os.makedirs(OUT, exist_ok=True)
    fetch = "--no-fetch" not in sys.argv
    chromium = None
    from beautiful.render import _Chromium
    chromium = _Chromium()
    rows = []
    try:
        for url in CANDIDATES:
            name = name_of(url)
            if name in SKIP:
                continue
            path = os.path.join(OUT, name.replace(".", "_") + ".png")
            if fetch or not os.path.exists(path):
                try:
                    chromium.render(url, "desktop", wait_ms=800).save(path)
                except Exception as e:
                    print("skip", name, e)
                    continue
            im = Image.open(path)
            if im.getextrema() in [((0, 0), (0, 0), (0, 0)), ((255, 255), (255, 255), (255, 255))]:
                print("blank", name)
                continue
            r = beauty(path, "ui")
            w = beauty(path, "web")["score"]
            rows.append({"site": name, "ui": r["score"], "web": w, "factors": r["factors"], "file": path})
            print(f"ui {r['score']:3d}  web {w:3d}  {name}", flush=True)
    finally:
        if chromium:
            chromium.close()
    rows.sort(key=lambda x: -x["ui"])
    keys = ["composition", "alignment", "contrast", "harmony", "whitespace", "congestion", "contour", "hierarchy", "margin"]
    md = [f"Rendered {date.today().isoformat()} with headless Chromium at 1280×800 (`beautiful.render`), "
          f"{len(rows)} of {len(CANDIDATES)} candidates loaded. Sorted by the `ui` formula; `web` is the calibrated model.\n",
          "| ui | web | site | " + " | ".join(keys) + " |", "|---:|---:|---|" + "---:|" * len(keys)]
    for x in rows:
        md.append(f"| **{x['ui']}** | {x['web']} | {x['site']} | " + " | ".join(f"{x['factors'][k]:.2f}" for k in keys) + " |")
    md.append("\nSkipped (the capture was not the page): " + ", ".join(f"{k} ({v})" for k, v in SKIP.items()))
    open(os.path.join(HERE, "results_hall_of_fame.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    json.dump([{k: v for k, v in x.items() if k != "file"} for x in rows],
              open(os.path.join(HERE, "results_hall_of_fame.json"), "w"), indent=1)
    top = rows[:TOP_N]
    n_rows = (len(top) + COLS - 1) // COLS
    canvas = Image.new("RGB", (COLS * (TW + PAD) + PAD, n_rows * (TH + LABEL_H + PAD) + PAD), "white")
    d = ImageDraw.Draw(canvas)
    f_score, f_label = font(22), font(16)
    for i, x in enumerate(top):
        im = Image.open(x["file"]).convert("RGB")
        im = im.resize((TW, round(im.height * TW / im.width)), Image.LANCZOS).crop((0, 0, TW, TH))
        cx = PAD + (i % COLS) * (TW + PAD)
        cy = PAD + (i // COLS) * (TH + LABEL_H + PAD)
        d.rectangle([cx - 1, cy - 1, cx + TW, cy + TH], outline=(210, 210, 210))
        canvas.paste(im, (cx, cy))
        d.text((cx, cy + TH + 8), str(x["ui"]), fill=colour(x["ui"]), font=f_score)
        d.text((cx + 46, cy + TH + 12), f"{x['site']}   (web {x['web']})", fill=(40, 40, 40), font=f_label)
    out = os.path.join(HERE, "hall_of_fame.png")
    canvas.save(out, optimize=True)
    print("wrote", out, canvas.size)


if __name__ == "__main__":
    main()
