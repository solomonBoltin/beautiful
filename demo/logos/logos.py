"""Twelve icons, three versions each: a deliberately worse one, the icon as published, and the best version the
formula could find by moving only what a designer would move (size on the canvas, optical centring, colour).

  python demo/logos/logos.py          -> demo/logos/<slug>.png (less | original | more), results_logos.json / .md

Brand marks come from Simple Icons (CC0 paths; trademarks belong to their owners) and are shown only to compare scores."""
import io, itertools, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", ".."))
from PIL import Image, ImageDraw, ImageFont
from beautiful import beauty
from in_icon import svg as in_svg

ICONS = [("googlechrome", "Chrome"), ("apple", "Apple"), ("nike", "Nike"), ("github", "GitHub"), ("slack", "Slack"), ("spotify", "Spotify"),
         ("figma", "Figma"), ("airbnb", "Airbnb"), ("target", "Target"), ("telegram", "Telegram"), ("mastercard", "Mastercard")]
HEX = json.load(open(os.path.join(HERE, "svg", "hex.json")))
S = 1024

class Raster:
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self.p = sync_playwright().start(); self.b = self.p.chromium.launch(); self.page = self.b.new_page(viewport={"width": S, "height": S})
    def png(self, body, size=S):
        self.page.set_viewport_size({"width": size, "height": size})
        self.page.set_content(f'<html><body style="margin:0;background:#fff;width:{size}px;height:{size}px;overflow:hidden">{body}</body></html>')
        return Image.open(io.BytesIO(self.page.screenshot())).convert("RGB")
    def close(self): self.b.close(); self.p.stop()

def brand(slug, scale=0.62, dx=0.0, dy=0.0, colour=None, rot=0.0, stray=False, size=S):
    """A Simple Icons path on a white square: scale = icon width / canvas, dx/dy = offset as a fraction of the canvas."""
    path = open(os.path.join(HERE, "svg", slug + ".svg")).read()
    inner = path[path.index("<path"):path.rindex("</svg>")]
    fill = colour or "#" + HEX.get(slug, "000000")
    w = size * scale; x = (size - w) / 2 + dx * size; y = (size - w) / 2 + dy * size
    stray_el = (f'<rect x="{size*0.06}" y="{size*0.06}" width="{size*0.16}" height="{size*0.05}" fill="#b0b8c4"/>'
                f'<circle cx="{size*0.9}" cy="{size*0.88}" r="{size*0.035}" fill="#e2b93b"/>') if stray else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">{stray_el}'
            f'<g transform="translate({x + w/2},{y + w/2}) rotate({rot}) translate({-w/2},{-w/2}) scale({w/24})" fill="{fill}">{inner}</g></svg>')

def in_icon(scale=1.0, dx=0, dy=0, rot=0.0, stray=False, size=S):
    s = in_svg(scale=scale, dx=dx, dy=dy, face=False, size=size)
    if rot: s = s.replace('<g transform="translate(', f'<g transform="rotate({rot} 500 500) translate(', 1)
    if stray: s = s.replace("</svg>", '<rect x="60" y="60" width="160" height="50" fill="#b0b8c4"/><circle cx="900" cy="880" r="35" fill="#e2b93b"/></svg>')
    return s

def mass_centre(im):
    g = im.convert("L").resize((128, 128)); px = g.load(); W = H = 128; mx = my = m = 0.0
    for y in range(H):
        for x in range(W):
            v = 255 - px[x, y]
            if v > 20: mx += v * x; my += v * y; m += v
    return ((mx / m) / W - 0.5, (my / m) / H - 0.5) if m else (0.0, 0.0)

def score(im): return beauty(im, "logo")

def run():
    R = Raster(); results = []; F = lambda n: ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", n) if os.path.exists("/System/Library/Fonts/Helvetica.ttc") else ImageFont.load_default()
    col = lambda s: (0x1b, 0x8a, 0x3e) if s >= 80 else (0xc7, 0x7d, 0) if s >= 60 else (0xc0, 0x1c, 0x1c)
    jobs = [(slug, name, "brand") for slug, name in ICONS] + [("in", "in (Bina)", "in")]
    for slug, name, kind in jobs:
        gen = (lambda **p: brand(slug, **p)) if kind == "brand" else in_icon
        orig_p = dict(scale=0.62) if kind == "brand" else dict(scale=1.0)
        orig = R.png(gen(**orig_p)); ro = score(orig)
        # less perfect: cramped, off-centre, tilted, plus a stray element the mark did not ask for
        less_p = dict(scale=0.9, dx=0.12, dy=0.09, rot=9, stray=True) if kind == "brand" else dict(scale=1.6, dx=110, dy=90, rot=9, stray=True)
        less = R.png(gen(**less_p)); rl = score(less)
        # more perfect: search size, optical centring and (for brand marks) colour; keep only what beats the original
        base = score(R.png(gen(**orig_p), 512))["score"]          # search at 512 against a 512 baseline; the winner is re-rendered at 1024
        best = (base + 1, None, None, None)                       # a candidate must beat the baseline by 2 points to count
        cx, cy = mass_centre(orig)
        if kind == "brand":
            grid = itertools.product([0.45, 0.55, 0.62, 0.7, 0.8], [None, "#111111"], [False, True])
            for scale, colour, centre in grid:
                p = dict(scale=scale, colour=colour, dx=-cx * scale / orig_p["scale"] if centre else 0.0, dy=-cy * scale / orig_p["scale"] if centre else 0.0)
                im = R.png(gen(**p), 512); r = score(im)
                if r["score"] > best[0]: best = (r["score"], p, None, r)
        else:
            for scale, dx, char in itertools.product([0.9, 1.0, 1.1], [-45, -30, -15, 0], [1.0, 1.3]):
                p = dict(scale=scale, dx=dx); s = in_svg(scale=scale, dx=dx, face=False, char=char, size=512); im = R.png(s, 512); r = score(im)
                if r["score"] > best[0]: best = (r["score"], dict(scale=scale, dx=dx, char=char), None, r)
        if best[1] is not None:
            more = R.png(in_svg(face=False, size=S, **best[1]) if kind == "in" else gen(**best[1])); rm = score(more)
            if rm["score"] <= ro["score"]: best = (ro["score"], None, None, None); more, rm = orig, ro
        else: more, rm = orig, ro
        # composite
        W = 300; T = Image.new("RGB", (3 * W + 40, W + 70), "white"); d = ImageDraw.Draw(T)
        for i, (lab, im, r) in enumerate((("less perfect", less, rl), ("as published", orig, ro), ("more perfect", more, rm))):
            x = 10 + i * (W + 10); d.text((x, 6), lab, fill=(90, 90, 90), font=F(15)); d.text((x + W - 62, 2), str(r["score"]), fill=col(r["score"]), font=F(30))
            T.paste(im.resize((W, W), Image.LANCZOS), (x, 40)); d.rectangle([x - 1, 39, x + W, 40 + W], outline=(220, 220, 220))
            d.text((x, 44 + W), " ".join(f"{k[:4]} {r['factors'][k]:.2f}" for k in ("composition", "simplicity", "whitespace", "harmony")), fill=(120, 120, 120), font=F(11))
        T.save(os.path.join(HERE, slug + ".png"))
        def why(a, b):
            ks = ("composition", "simplicity", "whitespace", "harmony", "economy", "contrast")
            return ", ".join(f"{k} {a['factors'][k]:.2f}→{b['factors'][k]:.2f}" for k in ks if abs(a["factors"][k] - b["factors"][k]) >= 0.05)
        results.append(dict(slug=slug, name=name, less=rl["score"], original=ro["score"], more=rm["score"], more_params=best[1] or {},
                            why_less=why(ro, rl), why_more=why(ro, rm) or "already at its optimum", hints=ro["hints"][:2]))
        print(f"{name:12s} less {rl['score']:3d}  original {ro['score']:3d}  more {rm['score']:3d}  {results[-1]['more_params']}", flush=True)
    R.close()
    json.dump(results, open(os.path.join(HERE, "..", "results_logos.json"), "w"), indent=1)
    M = ["| icon | less perfect | as published | more perfect | what the formula moved |", "|---|---:|---:|---:|---|"]
    for r in results:
        M.append(f"| {r['name']} | {r['less']} | **{r['original']}** | {r['more']} | {r['why_more']} |")
    open(os.path.join(HERE, "..", "results_logos.md"), "w").write("\n".join(M) + "\n"); print("\n".join(M))

if __name__ == "__main__": run()
