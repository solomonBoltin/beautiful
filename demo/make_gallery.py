"""Rebuild demo/ui_gallery.png from demo/results_ui.json + demo/screens/*.png.

    python demo/make_gallery.py            # writes demo/ui_gallery.png

Pure Pillow, no matplotlib. Score colour: green >= 80, amber 60-79, red < 60.
"""
from __future__ import annotations

import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
COLS, THUMB_W, THUMB_H, PAD, LABEL_H = 4, 380, 238, 16, 48   # 16:10 thumbnails, cropped from the top
FONT_CANDIDATES = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arial.ttf",
]


def font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow < 10.1
        return ImageFont.load_default()


def colour(score):
    return (0x1b, 0x8a, 0x3e) if score >= 80 else (0xc7, 0x7d, 0x00) if score >= 60 else (0xc0, 0x1c, 0x1c)


def main():
    rows = json.load(open(os.path.join(HERE, "results_ui.json")))
    rows = sorted(rows, key=lambda r: -r["score"])
    thumbs = []
    for r in rows:
        im = Image.open(os.path.join(HERE, "screens", r["file"])).convert("RGB")
        h = round(im.height * THUMB_W / im.width)
        im = im.resize((THUMB_W, h), Image.LANCZOS)
        thumbs.append(im.crop((0, 0, THUMB_W, min(h, THUMB_H))))
    thumb_h = THUMB_H
    cell_w, cell_h = THUMB_W + PAD, thumb_h + LABEL_H + PAD
    n_rows = (len(rows) + COLS - 1) // COLS
    canvas = Image.new("RGB", (COLS * cell_w + PAD, n_rows * cell_h + PAD), "white")
    d = ImageDraw.Draw(canvas)
    f_score, f_label = font(20), font(15)
    for i, (r, t) in enumerate(zip(rows, thumbs)):
        x = PAD + (i % COLS) * cell_w
        y = PAD + (i // COLS) * cell_h
        d.rectangle([x - 1, y - 1, x + THUMB_W, y + thumb_h], outline=(210, 210, 210))
        canvas.paste(t, (x, y))
        d.text((x, y + thumb_h + 10), str(r["score"]), fill=colour(r["score"]), font=f_score)
        d.text((x + 42, y + thumb_h + 14), r["label"], fill=(40, 40, 40), font=f_label)
    out = os.path.join(HERE, "ui_gallery.png")
    canvas.save(out, optimize=True)
    print("wrote", out, canvas.size)


if __name__ == "__main__":
    main()
