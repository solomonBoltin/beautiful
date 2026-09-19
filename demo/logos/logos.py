"""Icons, three versions each: a deliberately worse one, the icon as published, and the best version the
formula could find by moving only what a designer would move (size on the canvas, optical centring, colour).

  python demo/logos/logos.py          -> demo/logos/<slug>.png (less | original | more), results_logos.json / .md

Brand marks come from Simple Icons (CC0 paths; trademarks belong to their owners) and are shown only to compare
scores. Raster icons in demo/logos/raster/ are used exactly as supplied: the mark is lifted off its tile and only
re-placed (size, position) inside it."""
import io, itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", ".."))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from beautiful import beauty

ICONS = [("googlechrome", "Chrome"), ("apple", "Apple"), ("nike", "Nike"), ("github", "GitHub"), ("slack", "Slack"), ("spotify", "Spotify"),
         ("figma", "Figma"), ("airbnb", "Airbnb"), ("target", "Target"), ("telegram", "Telegram"), ("mastercard", "Mastercard")]
RASTER = [("in-small", "in (Bina, app icon)"), ("in-grid", "in (Bina, grid mark)")]
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

class Tile:
    """A raster app icon: a flat tile with a mark on it. The mark is lifted (alpha = distance from the tile colour)
    so it can be re-placed; the tile itself, corners included, is never touched."""
    def __init__(self, path):
        im = Image.open(path).convert("RGBA"); bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
        im = bg.convert("RGB").resize((S, S), Image.LANCZOS); self.base = im
        a = np.asarray(im).astype(np.int16); inner = a[S // 4: 3 * S // 4, S // 4: 3 * S // 4].reshape(-1, 3)
        vals, counts = np.unique(inner, axis=0, return_counts=True); self.tile = tuple(int(v) for v in vals[counts.argmax()])
        dist = np.abs(a - np.array(self.tile)).sum(2)
        mark = dist > 60; mark[: S // 8] = mark[-S // 8:] = False; mark[:, : S // 8] = mark[:, -S // 8:] = False   # ignore the tile's corners
        ys, xs = np.where(mark); pad = 24                                   # the soft edge of an upscaled icon extends past the hard mask
        self.box = (max(0, xs.min() - pad), max(0, ys.min() - pad), min(S, xs.max() + 1 + pad), min(S, ys.max() + 1 + pad))
        soft = dist > 4; soft[: S // 8] = soft[-S // 8:] = False; soft[:, : S // 8] = soft[:, -S // 8:] = False
        alpha = np.clip(dist / 90.0, 0, 1); alpha[~soft] = 0
        crop = im.crop(self.box); al = Image.fromarray((alpha[self.box[1]:self.box[3], self.box[0]:self.box[2]] * 255).astype(np.uint8))
        self.mark = crop.copy(); self.mark.putalpha(al)
        from PIL import ImageFilter
        self.hole = al.filter(ImageFilter.MaxFilter(9)).point(lambda v: 255 if v > 0 else 0)   # the mark's footprint, dilated, to paint over
        m = alpha[self.box[1]:self.box[3], self.box[0]:self.box[2]]; yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
        self.mass = ((xx * m).sum() / m.sum() / m.shape[1], (yy * m).sum() / m.sum() / m.shape[0])   # centre of mass within the crop, 0..1
    def compose(self, scale=1.0, dx=0.0, dy=0.0, rot=0.0, stray=False, size=S):
        # every version, the published one included, goes through the same lift-and-replace, so resampling cannot favour one
        im = self.base.copy(); im.paste(Image.new("RGB", self.mark.size, self.tile), self.box[:2], self.hole)
        mk = self.mark.resize((max(1, round(self.mark.width * scale)), max(1, round(self.mark.height * scale))), Image.LANCZOS)
        if rot: mk = mk.rotate(-rot, Image.BICUBIC, expand=True)
        bx = (self.box[0] + self.box[2]) / 2 + dx * S; by = (self.box[1] + self.box[3]) / 2 + dy * S
        im.paste(mk, (round(bx - mk.width / 2), round(by - mk.height / 2)), mk)
        if stray:
            d = ImageDraw.Draw(im); d.rectangle([S * 0.12, S * 0.12, S * 0.28, S * 0.17], fill=(176, 184, 196)); d.ellipse([S * 0.82, S * 0.80, S * 0.89, S * 0.87], fill=(226, 185, 59))
        return im.resize((size, size), Image.LANCZOS) if size != S else im

def mass_centre(im):
    g = im.convert("L").resize((128, 128)); px = g.load(); W = H = 128; mx = my = m = 0.0
    for y in range(H):
        for x in range(W):
            v = 255 - px[x, y]
            if v > 20: mx += v * x; my += v * y; m += v
    return ((mx / m) / W - 0.5, (my / m) / H - 0.5) if m else (0.0, 0.0)

def score(im): return beauty(im, "logo")

def run():
    R = Raster(); results = []
    F = lambda n: ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", n) if os.path.exists("/System/Library/Fonts/Helvetica.ttc") else ImageFont.load_default()
    col = lambda s: (0x1b, 0x8a, 0x3e) if s >= 80 else (0xc7, 0x7d, 0) if s >= 60 else (0xc0, 0x1c, 0x1c)
    draw = lambda x, size=S: R.png(x, size) if isinstance(x, str) else x
    jobs = [(slug, name, "brand") for slug, name in ICONS] + [(slug, name, "raster") for slug, name in RASTER]
    for slug, name, kind in jobs:
        if kind == "brand":
            gen = lambda size=S, **p: brand(slug, size=size, **p); orig_p = dict(scale=0.62)
            less_p = dict(scale=0.9, dx=0.12, dy=0.09, rot=9, stray=True)
        else:
            tile = Tile(os.path.join(HERE, "raster", slug + ".png")); gen = tile.compose; orig_p = dict(scale=1.0)
            less_p = dict(scale=1.5, dx=0.10, dy=0.08, rot=9, stray=True)
        orig = draw(gen(**orig_p)); ro = score(orig)
        less = draw(gen(**less_p)); rl = score(less)
        # more perfect: search size, optical centring and (for brand marks) colour; a candidate must beat the original by 2 points
        base = score(draw(gen(size=512, **orig_p), 512))["score"]; best = (base + 1, None)
        if kind == "brand":
            cx, cy = mass_centre(orig)
            cands = [dict(scale=sc, colour=co, dx=-cx * sc / orig_p["scale"] if ce else 0.0, dy=-cy * sc / orig_p["scale"] if ce else 0.0)
                     for sc, co, ce in itertools.product([0.45, 0.55, 0.62, 0.7, 0.8], [None, "#111111"], [False, True])]
        else:
            # optical centring: move the mark so its centre of mass sits on the tile centre
            mx = (tile.box[0] + (tile.mass[0]) * (tile.box[2] - tile.box[0])) / S - 0.5; my = (tile.box[1] + tile.mass[1] * (tile.box[3] - tile.box[1])) / S - 0.5
            cands = [dict(scale=sc, dx=-mx * sc if ce else 0.0, dy=-my * sc if ce else 0.0) for sc, ce in itertools.product([0.8, 0.9, 1.0, 1.15, 1.3, 1.5], [False, True])]
        for p in cands:
            r = score(draw(gen(size=512, **p), 512))
            if r["score"] > best[0]: best = (r["score"], p)
        more, rm = orig, ro
        if best[1] is not None:
            cand = draw(gen(**best[1])); rc = score(cand)
            if rc["score"] > ro["score"]: more, rm = cand, rc
            else: best = (ro["score"], None)
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
        print(f"{name:22s} less {rl['score']:3d}  original {ro['score']:3d}  more {rm['score']:3d}  {results[-1]['more_params']}", flush=True)
    R.close()
    json.dump(results, open(os.path.join(HERE, "..", "results_logos.json"), "w"), indent=1)
    M = ["| icon | less perfect | as published | more perfect | what the formula moved |", "|---|---:|---:|---:|---|"]
    for r in results: M.append(f"| {r['name']} | {r['less']} | **{r['original']}** | {r['more']} | {r['why_more']} |")
    open(os.path.join(HERE, "..", "results_logos.md"), "w").write("\n".join(M) + "\n"); print("\n".join(M))
    files = [r["slug"] for r in results]; ims = [Image.open(os.path.join(HERE, f + ".png")) for f in files]
    w, h = ims[0].size; cols = 2; rows = (len(ims) + 1) // 2
    G = Image.new("RGB", (cols * w + 30, rows * h + 10 * (rows + 1)), "white")
    for i, im in enumerate(ims): G.paste(im, (10 + (i % cols) * (w + 10), 10 + (i // cols) * (h + 10)))
    G.resize((G.width // 2, G.height // 2), Image.LANCZOS).save(os.path.join(HERE, "..", "logos_gallery.png"), optimize=True)

if __name__ == "__main__": run()
