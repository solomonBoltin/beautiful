"""The two Bina icons redrawn as vectors from their measured geometry (nothing added, nothing removed),
then framed by the score: python demo/logos/bina.py -> demo/logos/raster/in-*-vector.{svg,png}"""
import io, itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", ".."))
from PIL import Image
from beautiful import beauty
TILE, INK, MINT_GRID, MINT_SMALL = "#1b5e4a", "#fbfcfc", "#7ecfad", "#79caa8"

def grid_mark(scale=1.0, dx=0.0, dy=0.0, size=1024, full_bleed=False, radius=0.22):
    """Geometry measured on the 454 px original, in a 450-unit tile."""
    S = 450; g = []
    g.append(f'<rect x="126" y="172" width="31" height="31" rx="8" fill="{INK}"/><rect x="126" y="218" width="31" height="62" rx="8" fill="{INK}"/>')
    # arch: outer rounded shape minus inner opening (evenodd)
    g.append(f'<path fill="{MINT_GRID}" fill-rule="evenodd" d="M172,226 a54,54 0 0 1 54,-54 h46 a54,54 0 0 1 54,54 v48 a6,6 0 0 1 -6,6 h-18 a6,6 0 0 1 -6,-6 v-48 a24,24 0 0 0 -24,-24 h-46 a24,24 0 0 0 -24,24 v48 a6,6 0 0 1 -6,6 h-18 a6,6 0 0 1 -6,-6 z"/>')
    for x in (218, 256):
        for y in (218, 256): g.append(f'<rect x="{x}" y="{y}" width="24" height="24" rx="5" fill="{INK}"/>')
    return _frame(g, S, scale, dx, dy, size, full_bleed, radius)

def small_mark(scale=1.0, dx=0.0, dy=0.0, size=1024, full_bleed=False, radius=0.22):
    """Geometry measured on the 124 px original, scaled to the same 450-unit tile."""
    S = 450; g = []
    g.append(f'<rect x="114" y="166" width="36" height="36" rx="9" fill="{INK}"/><rect x="114" y="217" width="36" height="71" rx="9" fill="{INK}"/>')
    # white arch 174 wide, 122 tall, legs 28 thick, inner opening 110 wide
    g.append(f'<path fill="{INK}" fill-rule="evenodd" d="M166,253 a87,87 0 0 1 87,-87 a87,87 0 0 1 87,87 v28 a7,7 0 0 1 -7,7 h-14 a7,7 0 0 1 -7,-7 v-28 a59,59 0 0 0 -59,-59 a59,59 0 0 0 -59,59 v28 a7,7 0 0 1 -7,7 h-14 a7,7 0 0 1 -7,-7 z"/>')
    g.append(f'<rect x="217" y="217" width="71" height="71" rx="12" fill="{MINT_SMALL}"/>')
    return _frame(g, S, scale, dx, dy, size, full_bleed, radius)

def _frame(g, S, scale, dx, dy, size, full_bleed, radius):
    tile = f'<rect width="{S}" height="{S}" fill="{TILE}"/>' if full_bleed else f'<rect width="{S}" height="{S}" rx="{S*radius}" fill="{TILE}"/>'
    # the mark is drawn around the tile centre (225,225); scale / offset move only the mark
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{size}" height="{size}">{tile}'
            f'<g transform="translate({S/2 + dx*S},{S/2 + dy*S}) scale({scale}) translate({-S/2},{-S/2})">{"".join(g)}</g></svg>')

class Raster:
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self.p = sync_playwright().start(); self.b = self.p.chromium.launch(); self.page = self.b.new_page(viewport={"width": 1024, "height": 1024})
    def png(self, s, size=1024):
        self.page.set_viewport_size({"width": size, "height": size})
        self.page.set_content(f'<html><body style="margin:0;background:#fff">{s}</body></html>')
        return Image.open(io.BytesIO(self.page.screenshot())).convert("RGB")
    def close(self): self.b.close(); self.p.stop()

if __name__ == "__main__":
    R = Raster(); report = {}
    for name, fn in (("in-grid", grid_mark), ("in-small", small_mark)):
        rows = []
        for full, scale, dx, dy in itertools.product([False, True], [0.8, 0.9, 1.0, 1.1, 1.25, 1.4, 1.6], [-0.04, -0.02, 0.0, 0.02], [-0.02, 0.0, 0.02]):
            r = beauty(R.png(fn(scale=scale, dx=dx, dy=dy, size=512, full_bleed=full), 512), "logo")
            rows.append(dict(full=full, scale=scale, dx=dx, dy=dy, score=r["score"], **{k: round(v, 2) for k, v in r["factors"].items()}))
        rows.sort(key=lambda x: -x["score"]); report[name] = rows
        print(name, "as-drawn tile-on-white:", beauty(R.png(fn(size=512), 512), "logo")["score"], " full-bleed:", beauty(R.png(fn(size=512, full_bleed=True), 512), "logo")["score"])
        for x in rows[:5]: print("  ", x)
        print("   best tile-on-white:", max((x for x in rows if not x["full"]), key=lambda x: x["score"]))
    R.close(); json.dump(report, open(os.path.join(HERE, "bina_search.json"), "w"))
