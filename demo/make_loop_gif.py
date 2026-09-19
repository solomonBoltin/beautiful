"""Render demo/loop.gif: a card whose button walks back to the centre while the score climbs.

    python demo/make_loop_gif.py          # writes demo/loop.gif and demo/loop_frames/*.png

Pure Pillow. Each frame is rendered, scored with beauty(mode="ui"), and annotated with the
number and the top hint, so the GIF is a real trace of the function, not a mock-up.
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from beautiful import beauty  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 960, 600
OFFSETS = [220, 180, 140, 100, 60, 30, 0]
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


def render_card(offset: int) -> Image.Image:
    """A sign-in card. `offset` shifts the button and the field labels off the card's axis."""
    im = Image.new("RGB", (W, H), (244, 246, 250))
    d = ImageDraw.Draw(im)
    cx, cy, cw, ch = W // 2, H // 2, 420, 400
    x0, y0 = cx - cw // 2, cy - ch // 2
    d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], 18, fill="white", outline=(222, 226, 233))
    d.rectangle([cx - 24, y0 + 36, cx + 24, y0 + 84], fill=(0, 46, 95))       # logo mark
    d.rounded_rectangle([cx - 90, y0 + 112, cx + 90, y0 + 126], 6, fill=(60, 66, 80))  # title
    for i in range(2):                                                          # two inputs
        y = y0 + 160 + i * 68
        d.rounded_rectangle([x0 + 40, y, x0 + cw - 40, y + 44], 8, fill=(248, 249, 251), outline=(210, 214, 222))
        d.rounded_rectangle([x0 + 52 + offset // 2, y + 17, x0 + 52 + 90 + offset // 2, y + 27], 4, fill=(190, 194, 204))
    bx = cx - 130 + offset                                                      # the button
    d.rounded_rectangle([bx, y0 + 312, bx + 260, y0 + 356], 10, fill=(0, 46, 95))
    d.rounded_rectangle([bx + 100, y0 + 329, bx + 160, y0 + 339], 4, fill="white")
    return im


def colour(score):
    return (0x1b, 0x8a, 0x3e) if score >= 80 else (0xc7, 0x7d, 0x00) if score >= 60 else (0xc0, 0x1c, 0x1c)


def main():
    frames_dir = os.path.join(HERE, "loop_frames")
    os.makedirs(frames_dir, exist_ok=True)
    f_big, f_small, f_mono = font(44), font(18), font(16)
    frames, rows = [], []
    for off in OFFSETS:
        card = render_card(off)
        path = os.path.join(frames_dir, f"offset_{off:03d}.png")
        card.save(path)
        r = beauty(path, "ui")
        rows.append((off, r["score"]))
        fr = card.copy()
        d = ImageDraw.Draw(fr)
        d.rectangle([0, 0, W, 64], fill=(18, 20, 26))
        d.text((24, 12), f"beauty  {r['score']}", fill=colour(r["score"]), font=f_big)
        d.text((W - 24, 14), f"button offset {off:>3} px", fill=(200, 204, 212), font=f_small, anchor="ra")
        d.text((W - 24, 38), "beautiful --mode=ui card.png", fill=(120, 125, 135), font=f_mono, anchor="ra")
        hint = next((h for h in r["hints"] if "(" in h), r["hints"][0] if r["hints"] else "")
        d.rectangle([0, H - 44, W, H], fill=(18, 20, 26))
        d.text((24, H - 32), ("hint: " + hint)[:110], fill=(230, 232, 236), font=f_small)
        frames.append(fr.convert("P", palette=Image.ADAPTIVE, colors=128))
    frames += [frames[-1]] * 3                         # hold the final frame
    out = os.path.join(HERE, "loop.gif")
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=900, loop=0, optimize=True)
    print("wrote", out)
    for off, s in rows:
        print(f"{off:>4} px  ->  {s}")


if __name__ == "__main__":
    main()
