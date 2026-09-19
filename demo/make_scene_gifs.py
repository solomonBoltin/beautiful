"""Build demo/gifs/<scene>.gif for the five scenes in demo/scenes/scenes.py.

    python demo/make_scene_gifs.py            # all five (needs beautiful-score[render] + chromium)
    python demo/make_scene_gifs.py signin     # one

Each frame: the scene's HTML at t, rendered by beautiful.render (frozen Chromium, 1280×800 or
375×812), scored by the lint (pixel formula + DOM rules), then annotated with the number, the
rule error count and the top hint. The GIF is a trace of the function on a real page.
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, "scenes"))
from beautiful.render import score_html  # noqa: E402
import scenes  # noqa: E402

STEPS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
FONTS = ["/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf"]


def font(size):
    for p in FONTS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def colour(score):
    return (0x1b, 0x8a, 0x3e) if score >= 80 else (0xc7, 0x7d, 0x00) if score >= 60 else (0xc0, 0x1c, 0x1c)


def annotate(im, r, t, name, vp):
    W, H = im.size
    bar = 72 if vp == "desktop" else 96
    out = Image.new("RGB", (W, H + bar + 56), (18, 20, 26))
    out.paste(im, (0, bar))
    d = ImageDraw.Draw(out)
    big, small, mono = font(40 if vp == "desktop" else 34), font(18 if vp == "desktop" else 15), font(15 if vp == "desktop" else 13)
    d.text((20, 14), f"beauty  {r['score']}", fill=colour(r["score"]), font=big)
    errs = sum(1 for f in r.get("rules", []) if f.get("level") == "error")
    warns = sum(1 for f in r.get("rules", []) if f.get("level") == "warning")
    right = f"{errs} error{'s' if errs != 1 else ''} · {warns} warning{'s' if warns != 1 else ''}"
    if vp == "desktop":
        d.text((W - 20, 16), right, fill=(200, 204, 212), font=small, anchor="ra")
        d.text((W - 20, 42), f"beautiful {name}.html --viewports {vp}   step {t:.1f}", fill=(120, 125, 135), font=mono, anchor="ra")
    else:
        d.text((20, 58), right, fill=(200, 204, 212), font=small)
        d.text((20, 78), f"step {t:.1f}", fill=(120, 125, 135), font=mono)
    hint = next((h for h in r["hints"] if "(" in h or ":" in h), r["hints"][0] if r["hints"] else "")
    y = bar + H + 12
    width = 120 if vp == "desktop" else 44
    d.text((20, y), ("hint: " + hint)[:width], fill=(230, 232, 236), font=small)
    if len(hint) > width - 6:
        d.text((20, y + 22), hint[width - 6:2 * width - 12], fill=(230, 232, 236), font=small)
    return out


def build(name):
    fn, vp, _ = scenes.SCENES[name]
    frames_dir = os.path.join(HERE, "gifs", "frames", name)
    os.makedirs(frames_dir, exist_ok=True)
    frames, trace = [], []
    for t in STEPS:
        html = fn(t)
        path = os.path.join(frames_dir, f"{name}_{int(t*100):03d}.html")
        open(path, "w", encoding="utf-8").write(html)
        r = score_html(path, viewports=(vp,), save_dir=frames_dir)[vp]
        im = Image.open(r["image"]).convert("RGB")
        if vp == "desktop":
            im = im.resize((960, 600), Image.LANCZOS)
        else:
            im = im.resize((375, 812), Image.LANCZOS)
        fr = annotate(im, r, t, name, vp)
        frames.append(fr.convert("P", palette=Image.ADAPTIVE, colors=192))
        errs = [f["rule"] for f in r.get("rules", []) if f.get("level") == "error"]
        trace.append((t, r["score"], errs, r["hints"][:1]))
        print(f"{name} t={t:.1f} -> {r['score']:3d}  errors {errs}  {r['hints'][:1]}", flush=True)
    frames = [frames[0]] * 2 + frames + [frames[-1]] * 3
    out = os.path.join(HERE, "gifs", f"{name}.gif")
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=850, loop=0, optimize=True)
    print("wrote", out, os.path.getsize(out) // 1024, "KB")
    return trace


if __name__ == "__main__":
    names = sys.argv[1:] or list(scenes.SCENES)
    os.makedirs(os.path.join(HERE, "gifs"), exist_ok=True)
    for n in names:
        build(n)
