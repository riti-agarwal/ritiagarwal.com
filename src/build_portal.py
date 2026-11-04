"""Builds ../index.html from portal.html plus the map data in svg.json and svg2.json."""
import json, sys, re
import os
SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SRC, '..', 'index.html')
g = json.load(open(os.path.join(SRC, 'svg.json')))
t = open(os.path.join(SRC, 'portal.html')).read()
b, ca, p = g['box'], g['caRect'], g['pins']
f = lambda v: f'{v:g}'
vals = {
  'WORLD': g['world'], 'INSET': g['inset'],
  'CAX': f(ca[0]), 'CAY': f(ca[1]), 'CAW': f(ca[2]), 'CAH': f(ca[3]),
  'CAB': f(round(ca[1] + ca[3], 1)), 'CAR': f(round(ca[0] + ca[2], 1)),
  'BX': f(b['x']), 'BY': f(b['y']), 'BW': f(b['w']), 'BH': f(b['h']), 'BR': f(b['x'] + b['w']), 'TAGY': f(b['y'] - 4),
  'BANX': f(p['bangalore'][0]), 'BANY': f(p['bangalore'][1]), 'BANLX': f(p['bangalore'][0] + 7), 'BANLY': f(p['bangalore'][1] + 4),
  'SFX': f(p['sf'][0]), 'SFY': f(p['sf'][1]), 'SFLX': f(b['x'] + 5), 'SFLY': f(p['sf'][1] - 7),
  'FRX': f(p['fremont'][0]), 'FRY': f(p['fremont'][1]), 'FRLX': f(p['fremont'][0] + 7), 'FRLY': f(p['fremont'][1] + 4),
  'PAX': f(p['pasadena'][0]), 'PAY': f(p['pasadena'][1]), 'PALX': f(p['pasadena'][0] - 7), 'PALY': f(p['pasadena'][1] + 4),
}
g2 = json.load(open(os.path.join(SRC, 'svg2.json')))
b2, ca2, p2 = g2['box'], g2['caRect'], g2['pins']
cx, cy = p2['california']; bx, by = p2['bangalore']
mx = (cx + bx) / 2; top = min(cy, by)
px, py = p2['pasadena']; sx, sy = p2['sf']
vals.update({
  'H2': f(g2['H']), 'OUTLINE': g2['outline'], 'GRAT': g2['graticule'], 'WORLD2': g2['world'], 'INSET2': g2['inset'],
  'ARC1': f'M{f(cx)} {f(cy)} Q{f(round(mx,1))} {f(round(top - 78,1))} {f(bx)} {f(by)}',
  'ARC2': f'M{f(bx)} {f(by)} Q{f(round(mx,1))} {f(round(top - 28,1))} {f(cx)} {f(cy)}',
  'ARC3': f'M{f(px)} {f(py)} Q{f(round((px + sx) / 2 + 26,1))} {f(round((py + sy) / 2,1))} {f(sx)} {f(sy)}',
})
# the map room uses the v2 map: point the shared placeholders at it
vals.update({
  'CAX': f(ca2[0]), 'CAY': f(ca2[1]), 'CAW': f(round(ca2[2],1)), 'CAH': f(round(ca2[3],1)),
  'CAB': f(round(ca2[1] + ca2[3], 1)), 'CAR': f(round(ca2[0] + ca2[2], 1)),
  'BX': f(b2['x']), 'BY': f(b2['y']), 'BW': f(b2['w']), 'BH': f(b2['h']), 'BR': f(b2['x'] + b2['w']), 'TAGY': f(b2['y'] - 5),
  'BANX': f(bx), 'BANY': f(by), 'BANLX': f(bx + 9), 'BANLY': f(by + 5),
  'SFX': f(sx), 'SFY': f(sy), 'SFLX': f(b2['x'] + 4), 'SFLY': f(round(sy + 22, 1)),
  'FRX': f(p2['fremont'][0]), 'FRY': f(p2['fremont'][1]), 'FRLX': f(round(p2['fremont'][0] + 8, 1)), 'FRLY': f(round(p2['fremont'][1] + 5, 1)),
  'PAX': f(px), 'PAY': f(py), 'PALX': f(round(px - 8, 1)), 'PALY': f(round(py + 5, 1)),
})
out = re.sub(r'\{\{(\w+)\}\}', lambda m: vals[m.group(1)], t)
assert '{{' not in out
# phone tiles: paste a copy of the floor-plan drawing into each tile
art = out[out.index('<g id="plan-art">'):out.index('\n  </svg>\n  <div class="tiles">')]
art = art.replace('<g id="plan-art">', '', 1)
def tile(m):
    vb = m.group(1); x, y, w, h = vb.split()
    i = tile.n = getattr(tile, 'n', 0) + 1
    return (f'viewBox="{vb}"{m.group(2)}><clipPath id="tile-clip-{i}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
            f'<g clip-path="url(#tile-clip-{i})">{art}</g>')
out = re.sub(r'viewBox="([^"]+)"( role="group" aria-label="[^"]*")><!--PLAN-ART-->', tile, out)
assert '<!--PLAN-ART-->' not in out
open(OUT, 'w').write(out)
print('index.html', len(out) // 1024, 'KB')
