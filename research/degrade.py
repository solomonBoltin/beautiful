"""Make a broken twin of every acclaimed page — the defect-injection recipe OwlEye, Nighthawk
and UIClip train on, done with PIL so anyone can reproduce it.

    python research/degrade.py          # research/top100/*.png -> research/degraded/<site>__<defect>.png

Each page gets ONE random defect from a list a designer would call a mistake, never a matter of
taste: a block shifted off its grid, an element clipped by the viewport edge, an overlapping
duplicate, a stretched region, a low-contrast wash, clutter (random boxes), a lopsided crop, or a
colour cast. A beauty score worth shipping must prefer the original to its twin — that is the
pairwise test in research/benchmark.py.
"""
from __future__ import annotations

import json
import os
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "top100")
OUT = os.path.join(HERE, "degraded")


def shift_block(im, rng):
    """A horizontal band of the page slides sideways: misalignment / broken grid."""
    w, h = im.size
    y0 = rng.randint(int(h * 0.15), int(h * 0.6)); y1 = min(h, y0 + rng.randint(int(h * 0.15), int(h * 0.35)))
    dx = rng.choice([-1, 1]) * rng.randint(int(w * 0.06), int(w * 0.16))
    band = im.crop((0, y0, w, y1))
    out = im.copy()
    bg = im.getpixel((5, y0 + 2))
    out.paste(Image.new("RGB", (w, y1 - y0), bg), (0, y0))
    out.paste(band, (dx, y0))
    return out


def clip_edge(im, rng):
    """Content runs off the right edge: horizontal overflow."""
    w, h = im.size
    cut = rng.randint(int(w * 0.08), int(w * 0.18))
    y0 = rng.randint(int(h * 0.1), int(h * 0.5)); y1 = min(h, y0 + rng.randint(int(h * 0.2), int(h * 0.45)))
    band = im.crop((0, y0, w, y1))
    out = im.copy()
    out.paste(band, (cut, y0))
    return out


def overlap(im, rng):
    """A duplicate of a region pasted over neighbouring content: overlap / occlusion."""
    w, h = im.size
    bw, bh = rng.randint(int(w * 0.25), int(w * 0.45)), rng.randint(int(h * 0.15), int(h * 0.3))
    x0, y0 = rng.randint(0, w - bw), rng.randint(int(h * 0.1), h - bh)
    patch = im.crop((x0, y0, x0 + bw, y0 + bh))
    out = im.copy()
    out.paste(patch, (x0 + rng.randint(-bw // 2, bw // 2), y0 + rng.randint(bh // 3, bh // 2)))
    return out


def stretch(im, rng):
    """A region resampled to the wrong aspect ratio: distorted image / layout."""
    w, h = im.size
    y0 = rng.randint(int(h * 0.1), int(h * 0.5)); y1 = min(h, y0 + rng.randint(int(h * 0.25), int(h * 0.45)))
    band = im.crop((0, y0, w, y1)).resize((w, int((y1 - y0) * rng.choice([0.6, 1.5]))))
    out = im.copy()
    out.paste(band.crop((0, 0, w, min(band.height, h - y0))), (0, y0))
    return out


def wash(im, rng):
    """Contrast collapses: grey text on grey."""
    out = ImageEnhance.Contrast(im).enhance(rng.uniform(0.35, 0.55))
    return ImageEnhance.Brightness(out).enhance(rng.uniform(1.05, 1.2))


def clutter(im, rng):
    """Random boxes, badges and lines: the clutter and hierarchy loss of a busy page."""
    out = im.copy(); d = ImageDraw.Draw(out); w, h = im.size
    for _ in range(rng.randint(14, 26)):
        x0, y0 = rng.randint(0, w - 60), rng.randint(0, h - 40)
        bw, bh = rng.randint(40, int(w * 0.22)), rng.randint(14, int(h * 0.12))
        col = tuple(rng.randint(0, 255) for _ in range(3))
        d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=col, outline=(0, 0, 0))
    return out


def lopsided(im, rng):
    """The composition pushed to one side: imbalance."""
    w, h = im.size
    cut = rng.randint(int(w * 0.18), int(w * 0.3))
    side = rng.choice(["left", "right"])
    body = im.crop((cut, 0, w, h)) if side == "left" else im.crop((0, 0, w - cut, h))
    bg = im.getpixel((w - 3, h - 3))
    out = Image.new("RGB", (w, h), bg)
    out.paste(body, (0, 0) if side == "left" else (cut, 0))
    return out


def cast(im, rng):
    """A saturated colour cast over everything: palette gone wrong."""
    tint = Image.new("RGB", im.size, tuple(rng.choice([(180, 40, 200), (255, 120, 0), (0, 200, 120), (255, 0, 90)])))
    return Image.blend(im, tint, rng.uniform(0.28, 0.4))


DEFECTS = {"shift": shift_block, "clip": clip_edge, "overlap": overlap, "stretch": stretch,
           "wash": wash, "clutter": clutter, "lopsided": lopsided, "cast": cast}


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = json.load(open(os.path.join(HERE, "results_top100.json")))["rows"]
    rng = random.Random(7)
    pairs = []
    names = list(DEFECTS)
    for i, r in enumerate(rows):
        src = os.path.join(HERE, r["file"])
        im = Image.open(src).convert("RGB")
        defect = names[i % len(names)]
        out = DEFECTS[defect](im, rng)
        path = os.path.join(OUT, f"{r['site'].replace('.', '_')}__{defect}.png")
        out.save(path)
        pairs.append({"site": r["site"], "defect": defect, "original": src, "degraded": path})
    json.dump(pairs, open(os.path.join(HERE, "degraded_pairs.json"), "w"), indent=1)
    print("wrote", len(pairs), "pairs")


if __name__ == "__main__":
    main()
