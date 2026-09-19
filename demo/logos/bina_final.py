"""The Bina grid mark on a single proportional unit u (the arch stroke), underline included, centred as a whole.
python demo/logos/bina_final.py -> demo/logos/raster/in-grid-final.{svg,png}"""
import io, itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", ".."))
from PIL import Image
from beautiful import beauty
TILE, INK, MINT = "#1b5e4a", "#fbfcfc", "#7ecfad"

def mark(u=30, gap=0.5, arch_h=3.6, sq=0.8, scale=0.7, dx=0.0, dy=0.0, size=1024, radius=0.22, bar=True, bar_gap=0.5, cap=0.27):
    """Everything in units of u. One cap radius for every stroke end: cap·thickness (i, arch feet, squares, underline). i: stem u wide, dot u square, half-unit gap; half-unit gap to the arch; arch 5u wide,
    3u opening, u stroke, arch_h tall; four squares sq·u in a 3u opening on the baseline; underline u thick, bar_gap below."""
    S = 450; g = []
    ih = arch_h * u                       # i stem + dot span the arch height: dot u, gap u/2, stem the rest
    x0 = 0; top = 0; base = ih
    g.append(f'<rect x="{x0}" y="{top}" width="{u}" height="{u}" rx="{u*cap:.1f}" fill="{INK}"/>')
    g.append(f'<rect x="{x0}" y="{top + 1.5*u}" width="{u}" height="{ih - 1.5*u}" rx="{u*cap:.1f}" fill="{INK}"/>')
    ax = x0 + u + gap * u; aw = 5 * u; R_out = 1.8 * u; R_in = 0.8 * u; leg_r = cap * u
    # arch = outer shape (rounded top, softly rounded feet) minus the inner opening (rounded top), even-odd
    o = (f'M{ax},{top + R_out} A{R_out},{R_out} 0 0 1 {ax + R_out},{top} H{ax + aw - R_out} A{R_out},{R_out} 0 0 1 {ax + aw},{top + R_out} '
         f'V{base - leg_r} A{leg_r},{leg_r} 0 0 1 {ax + aw - leg_r},{base} H{ax + leg_r} A{leg_r},{leg_r} 0 0 1 {ax},{base - leg_r} Z')
    i_ = (f'M{ax + u},{base} V{top + u + R_in} A{R_in},{R_in} 0 0 1 {ax + u + R_in},{top + u} H{ax + aw - u - R_in} '
          f'A{R_in},{R_in} 0 0 1 {ax + aw - u},{top + u + R_in} V{base} Z')
    g.append(f'<path fill="{MINT}" fill-rule="evenodd" d="{o} {i_}"/>')
    s = sq * u; inner = 3 * u; pitch = (inner - 2 * s) / 3        # equal gaps: edge, middle, edge
    for i in range(2):
        for j in range(2):
            g.append(f'<rect x="{ax + u + pitch + i*(s + pitch):.1f}" y="{base - s - j*(s + pitch):.1f}" width="{s:.1f}" height="{s:.1f}" rx="{s*cap:.1f}" fill="{INK}"/>')
    w = u + gap * u + aw; h = ih
    if bar:
        by = base + bar_gap * u; g.append(f'<rect x="0" y="{by:.1f}" width="{w:.1f}" height="{u}" rx="{u*cap:.1f}" fill="{MINT}"/>'); h = by + u
    tile = f'<rect width="{S}" height="{S}" rx="{S*radius}" fill="{TILE}"/>'
    # the whole mark (underline included) is centred on the tile, then scaled / nudged
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{size}" height="{size}">{tile}'
            f'<g transform="translate({S/2 + dx*S:.1f},{S/2 + dy*S:.1f}) scale({scale}) translate({-w/2:.1f},{-h/2:.1f})">{"".join(g)}</g></svg>')

class Raster:
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self.p = sync_playwright().start(); self.b = self.p.chromium.launch(); self.page = self.b.new_page(viewport={"width": 1024, "height": 1024})
    def png(self, s, size=1024):
        self.page.set_viewport_size({"width": size, "height": size}); self.page.set_content(f'<html><body style="margin:0;background:#fff">{s}</body></html>')
        return Image.open(io.BytesIO(self.page.screenshot())).convert("RGB")
    def close(self): self.b.close(); self.p.stop()

if __name__ == "__main__":
    R = Raster(); rows = []
    for bar_gap, gap, arch_h, scale, dx, dy in itertools.product([0.33, 0.5, 0.67], [0.5], [3.5, 3.6, 4.0], [0.6, 0.65, 0.7, 0.75, 0.8], [-0.02, -0.01, 0.0, 0.01, 0.02], [-0.02, -0.01, 0.0, 0.01, 0.02]):
        r = beauty(R.png(mark(bar_gap=bar_gap, gap=gap, arch_h=arch_h, scale=scale, dx=dx, dy=dy, size=512), 512), "logo"); v = r["raw"]["symmetry"]
        rows.append(dict(bar_gap=bar_gap, arch_h=arch_h, scale=scale, dx=dx, dy=dy, score=r["score"], comp=round(r["factors"]["composition"], 2), lr=round(v["horizontal_mirror"], 2), tb=round(v["vertical_mirror"], 2), bal=round(v["balance"], 2), ws=round(r["factors"]["whitespace"], 2)))
        print(len(rows), rows[-1], flush=True) if len(rows) % 75 == 0 else None
    rows.sort(key=lambda x: (-x["score"], -x["comp"])); json.dump(rows, open(os.path.join(HERE, "bina_final_search.json"), "w"))
    print("top:"); [print(" ", x) for x in rows[:8]]
    print("centred (dx=dy=0) best:", max((x for x in rows if x["dx"] == 0 and x["dy"] == 0), key=lambda x: (x["score"], x["comp"])))
    # the score keeps rising as the mark shrinks (the symmetric tile takes over), so the size is chosen by proportion: 35 % of the tile
    b = dict(bar_gap=0.33, arch_h=3.5, scale=0.8, dx=0.0, dy=0.0); s = mark(**b); im = R.png(s); r = beauty(im, "logo")
    open(os.path.join(HERE, "raster", "in-grid-final.svg"), "w").write(s); im.save(os.path.join(HERE, "raster", "in-grid-final.png"))
    print("final @1024:", r["score"], {k: round(v, 2) for k, v in r["factors"].items()}); R.close()
