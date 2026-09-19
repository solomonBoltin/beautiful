"""The 100 most acclaimed public home pages, rendered and scored — a benchmark for the score.

    pip install "beautiful-score[render]" && playwright install chromium
    python research/top100.py                  # ~30 min: render 130 candidates, keep the first 100 that load
    python research/top100.py --no-fetch       # reuse research/top100/*.png
    python research/top100.py --from-json      # rewrite the table and gallery from results_top100.json

Candidates: Awwwards Site-of-the-Year / Site-of-the-Day studios and winners, Siteinspire / Godly /
Lapa staples, the design-led product and brand sites that every "best website design" list repeats,
editorial and institutional sites cited for typography. The list is a judgement call, documented
here so anyone can argue with it or extend it. Captures that came back blank, blocked, or covered
by a consent dialog are dropped by hand (SKIP) and noted.

Outputs: research/top100/<site>.png (cached, git-ignored), research/results_top100.json/.md,
research/top100_gallery.png (the 24 highest by the ui score, and the 8 lowest — both matter).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import date

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from beautiful import beauty  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "top100")
CANDIDATES = [
    # product / brand sites every list repeats
    "https://www.apple.com/", "https://stripe.com/", "https://linear.app/", "https://arc.net/",
    "https://vercel.com/", "https://www.figma.com/", "https://www.notion.com/", "https://www.airbnb.com/",
    "https://pitch.com/", "https://www.raycast.com/", "https://www.framer.com/", "https://webflow.com/",
    "https://www.craft.do/", "https://culturedcode.com/things/", "https://ia.net/", "https://www.hey.com/",
    "https://basecamp.com/", "https://cal.com/", "https://resend.com/", "https://clerk.com/",
    "https://www.superhuman.com/", "https://www.loom.com/", "https://www.warp.dev/", "https://zed.dev/",
    "https://obsidian.md/", "https://readwise.io/", "https://kagi.com/", "https://1password.com/",
    "https://www.anthropic.com/", "https://mistral.ai/", "https://huggingface.co/", "https://www.rust-lang.org/",
    "https://www.swift.org/", "https://astro.build/", "https://svelte.dev/", "https://tailwindcss.com/",
    "https://www.radix-ui.com/", "https://ui.shadcn.com/", "https://posthog.com/", "https://railway.com/",
    # design studios / awwwards regulars
    "https://lusion.co/", "https://activetheory.net/", "https://www.igloo.inc/", "https://locomotive.ca/",
    "https://immersive-g.com/", "https://resn.co.nz/", "https://unseen.co/", "https://obys.agency/",
    "https://zajno.com/", "https://dogstudio.co/", "https://www.hellomonday.com/", "https://bruno-simon.com/",
    "https://aristidebenoist.com/", "https://rogierdeboeve.com/", "https://www.thisisbuild.com/", "https://www.ueno.co/",
    "https://www.instrument.com/", "https://www.huge.com/", "https://www.work.co/", "https://www.pentagram.com/",
    "https://www.ideo.com/", "https://www.frog.co/", "https://www.designstudio.com/", "https://www.koto.studio/",
    "https://www.wearecollins.com/", "https://www.mouthwash.studio/", "https://www.basicagency.com/", "https://www.fantasy.co/",
    "https://www.area17.com/", "https://www.stinkstudios.com/", "https://www.tubikstudio.com/", "https://www.metalab.com/",
    "https://www.lickd.co/", "https://www.awwwards.com/", "https://www.siteinspire.com/", "https://godly.website/",
    # editorial / institutional / typography-cited
    "https://www.nytimes.com/", "https://pudding.cool/", "https://informationisbeautiful.net/", "https://www.newyorker.com/",
    "https://www.theatlantic.com/", "https://www.bloomberg.com/", "https://www.economist.com/", "https://www.gov.uk/",
    "https://www.moma.org/", "https://www.tate.org.uk/", "https://www.metmuseum.org/", "https://www.rijksmuseum.nl/en",
    "https://www.cooperhewitt.org/", "https://www.sfmoma.org/", "https://www.guggenheim.org/", "https://www.designmuseum.org/",
    "https://fonts.google.com/", "https://www.typewolf.com/", "https://fontsinuse.com/", "https://klim.co.nz/",
    "https://www.colophon-foundry.org/", "https://pangrampangram.com/", "https://www.futurefonts.xyz/", "https://abcdinamo.com/",
    # consumer brands cited for design
    "https://www.nike.com/", "https://www.tesla.com/", "https://www.porsche.com/international/", "https://www.aesop.com/",
    "https://www.muji.com/", "https://teenage.engineering/", "https://www.dyson.com/", "https://www.bang-olufsen.com/",
    "https://www.leica-camera.com/", "https://www.hermes.com/", "https://www.patagonia.com/", "https://www.allbirds.com/",
    "https://www.glossier.com/", "https://www.warbyparker.com/", "https://www.spotify.com/", "https://www.dropbox.com/",
    "https://www.mailchimp.com/", "https://slack.com/", "https://www.intercom.com/", "https://www.canva.com/",
    "https://www.dribbble.com/", "https://www.behance.net/", "https://unsplash.com/", "https://www.pinterest.com/",
    "https://medium.com/", "https://substack.com/", "https://ghost.org/", "https://www.are.na/",
    # second wave, added after the first crawl lost 30 candidates to bot walls and consent dialogs
    "https://www.duolingo.com/", "https://www.headspace.com/", "https://www.calm.com/", "https://monzo.com/",
    "https://wise.com/", "https://www.coinbase.com/", "https://www.shopify.com/", "https://www.squarespace.com/",
    "https://gumroad.com/", "https://www.lemonsqueezy.com/", "https://mercury.com/", "https://ramp.com/",
    "https://www.rippling.com/", "https://attio.com/", "https://rive.app/", "https://spline.design/",
    "https://mobbin.com/", "https://www.sketch.com/", "https://penpot.app/", "https://miro.com/",
    "https://www.family.co/", "https://ouraring.com/", "https://www.whoop.com/", "https://bellroy.com/",
    "https://www.rapha.cc/", "https://www.everlane.com/", "https://www.uniswap.org/", "https://www.moleskine.com/",
]
SKIP = {  # what the crawler captured on 2026-09-20 instead of the page (checked by eye)
    "allbirds.com": "loading skeleton", "area17.com": "consent dialog over a black page", "dyson.com": "bot wall",
    "bang-olufsen.com": "consent dialog", "behance.net": "rate-limit page", "medium.com": "bot wall", "pentagram.com": "loader",
    "nytimes.com": "bot wall", "bloomberg.com": "bot wall (press & hold)", "unseen.co": "loader", "warbyparker.com": "maintenance page",
    "unsplash.com": "access denied", "igloo.inc": "loader", "obys.agency": "loader", "basicagency.com": "splash/loader",
    "hermes.com": "access restricted", "porsche.com": "consent dialog", "canva.com": "maintenance page", "dribbble.com": "bot challenge",
    "dogstudio.co": "loader", "activetheory.net": "browser-not-supported page", "designmuseum.org": "consent dialog",
    "guggenheim.org": "consent dialog", "aesop.com": "security verification", "mouthwash.studio": "loader", "stinkstudios.com": "consent dialog",
    "economist.com": "security verification", "tesla.com": "access denied", "patagonia.com": "bot wall", "aristidebenoist.com": "loader",
    "coinbase.com": "security verification", "ramp.com": "unstyled capture", "monzo.com": "consent dialog", "duolingo.com": "never reached network idle",
}
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
    return url.split("//", 1)[1].replace("www.", "").strip("/").split("/")[0]


def colour(score):
    return (0x1b, 0x8a, 0x3e) if score >= 80 else (0xc7, 0x7d, 0x00) if score >= 60 else (0xc0, 0x1c, 0x1c)


def is_blank(im):
    ex = im.convert("L").getextrema()
    return ex[1] - ex[0] < 8


def main():
    os.makedirs(OUT, exist_ok=True)
    fetch = "--no-fetch" not in sys.argv
    rows, skipped = [], dict(SKIP)
    if True:
        for url in CANDIDATES:
            name = name_of(url)
            if name in skipped:
                continue
            path = os.path.join(OUT, name.replace(".", "_") + ".png")
            if fetch and not os.path.exists(path):
                # each fetch in its own process with a hard wall-clock limit: one site that never
                # reaches network-idle must not hang the whole run
                code = ("import sys; from beautiful.render import render; "
                        "render(sys.argv[1], 'desktop', timeout_ms=20000).save(sys.argv[2])")
                try:
                    subprocess.run([sys.executable, "-c", code, url, path], timeout=75, check=True,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except subprocess.TimeoutExpired:
                    skipped[name] = "render hung (75 s)"
                    print("skip", name, skipped[name], flush=True)
                    continue
                except Exception as e:
                    skipped[name] = f"render failed: {type(e).__name__}"
                    print("skip", name, skipped[name], flush=True)
                    continue
            if not os.path.exists(path):
                continue
            im = Image.open(path)
            if is_blank(im):
                skipped[name] = "blank capture"
                print("blank", name, flush=True)
                continue
            r = beauty(path, "ui")            # the fitted formula (what `beauty()` returns by default)
            w = beauty(path, "web")["score"]
            rows.append({"site": name, "url": url, "ui": r["score"], "classic": r["classic"]["score"], "web": w, "factors": r["factors"],
                         "experimental": {k: v for k, v in r["raw"]["experimental"].items() if not isinstance(v, dict)},
                         "hint": r["hints"][0] if r["hints"] else "", "file": os.path.relpath(path, HERE)})
            print(f"ui {r['score']:3d}  web {w:3d}  {name}", flush=True)
    rows = rows[:100]  # the benchmark is the first 100 clean captures in candidate order
    rows.sort(key=lambda x: -x["ui"])
    json.dump({"date": date.today().isoformat(), "rows": rows, "skipped": skipped},
              open(os.path.join(HERE, "results_top100.json"), "w"), indent=1)
    write_outputs(rows, skipped)


def write_outputs(rows, skipped):
    """results_top100.md and the gallery from the scored rows (also: `--from-json`, no scoring)."""
    keys = ["composition", "alignment", "contrast", "harmony", "whitespace", "congestion", "contour", "hierarchy", "margin"]
    md = [f"# The 100 most acclaimed home pages, scored\n",
          f"Rendered {date.today().isoformat()} with headless Chromium at 1280×800 (`beautiful.render`); "
          f"{len(rows)} of {len(CANDIDATES)} candidates loaded and are listed; {len(skipped)} dropped (bot walls, "
          f"consent dialogs, blank captures — listed at the end). Sorted by the `ui` formula; `web` is the model "
          "calibrated on human ratings.\n",
          "| # | ui | classic | web | site | " + " | ".join(keys) + " | weakest |", "|---:|---:|---:|---:|---|" + "---:|" * len(keys) + "---|"]
    for i, x in enumerate(rows, 1):
        md.append(f"| {i} | **{x['ui']}** | {x.get('classic', '')} | {x['web']} | [{x['site']}]({x['url']}) | " +
                  " | ".join(f"{x['factors'][k]:.2f}" for k in keys) + f" | {x['hint'][:60]} |")
    md.append("\nDropped: " + ", ".join(f"{k} ({v})" for k, v in skipped.items()))
    open(os.path.join(HERE, "results_top100.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")

    # gallery: top 24 and bottom 8
    pick = rows[:24] + rows[-8:]
    COLS, TW, TH, PAD, LH = 4, 380, 238, 16, 44
    n_rows = (len(pick) + COLS - 1) // COLS
    canvas = Image.new("RGB", (COLS * (TW + PAD) + PAD, n_rows * (TH + LH + PAD) + PAD + 40), "white")
    d = ImageDraw.Draw(canvas)
    d.text((PAD, 10), "top 24 by the ui formula … and the bottom 8", fill=(60, 60, 60), font=font(18))
    for i, x in enumerate(pick):
        im = Image.open(os.path.join(HERE, x["file"])).convert("RGB")
        im = im.resize((TW, round(im.height * TW / im.width)), Image.LANCZOS).crop((0, 0, TW, TH))
        cx = PAD + (i % COLS) * (TW + PAD)
        cy = 40 + PAD + (i // COLS) * (TH + LH + PAD)
        d.rectangle([cx - 1, cy - 1, cx + TW, cy + TH], outline=(210, 210, 210))
        canvas.paste(im, (cx, cy))
        d.text((cx, cy + TH + 8), str(x["ui"]), fill=colour(x["ui"]), font=font(22))
        d.text((cx + 46, cy + TH + 12), f"{x['site']}   (web {x['web']})", fill=(40, 40, 40), font=font(15))
    canvas.save(os.path.join(HERE, "top100_gallery.png"), optimize=True)
    print("wrote", len(rows), "rows;", len(skipped), "skipped")


if __name__ == "__main__":
    if "--from-json" in sys.argv:
        _d = json.load(open(os.path.join(HERE, "results_top100.json")))
        write_outputs(_d["rows"], _d["skipped"])
    else:
        main()
