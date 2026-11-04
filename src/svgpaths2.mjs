// World map v2: Natural Earth projection, 50m coastlines, graticule, California inset, pins.
import { createRequire } from 'module';
import { readFileSync, writeFileSync } from 'fs';
const dep = process.argv[2], out = process.argv[3];
const require = createRequire(dep + '/package.json');
const { feature } = require('topojson-client');
const d3 = await import(dep + '/node_modules/d3-geo/src/index.js');
const load = f => { const t = JSON.parse(readFileSync(dep + '/node_modules/world-atlas/' + f)); return feature(t, t.objects.land); };
const land50 = load('land-50m.json'), land110 = load('land-110m.json');

// fit the whole globe to the width, then keep only 78N to 58S
const W = 640;
const world = d3.geoNaturalEarth1().rotate([-10, 0]).fitWidth(W - 12, { type: 'Sphere' });
const [tx, ty] = world.translate();
world.translate([tx + 6, ty - world([0, 78])[1] + 6]);
const H = Math.round(world([0, -58])[1] + 6);
const clipY = [6, H - 6];
world.clipExtent([[0, clipY[0]], [W, clipY[1]]]);
const band = { type: 'Sphere' };

// California inset in the South Pacific
const box = { x: 22, y: 166, w: 128, h: 100 };
const cos36 = Math.cos(36 * Math.PI / 180);
const inset = d3.geoProjection((l, p) => [l * cos36, p])
  .fitExtent([[box.x + 10, box.y + 14], [box.x + box.w - 10, box.y + box.h - 10]],
    { type: 'MultiPoint', coordinates: [[-123.2, 38.2], [-117.4, 33.8]] });
inset.clipExtent([[box.x, box.y], [box.x + box.w, box.y + box.h]]);

const path = (proj, geo) => d3.geoPath(proj).digits(1)(geo);
const P = (proj, ll) => proj(ll).map(v => +v.toFixed(1));
const graticule = d3.geoGraticule().step([30, 30]).extentMinor([[-180, -58], [180, 78]])();
const ca = [[-124.6, 42.1], [-114.1, 32.5]].map(ll => P(world, ll));
writeFileSync(out, JSON.stringify({
  W, H, box,
  outline: path(world, band),
  graticule: path(world, graticule),
  world: path(world, land110),
  inset: path(inset, land50),
  caRect: [Math.min(ca[0][0], ca[1][0]), ca[0][1], Math.abs(ca[1][0] - ca[0][0]), ca[1][1] - ca[0][1]],
  pins: {
    bangalore: P(world, [77.59, 12.97]), california: P(world, [-120.5, 36.2]),
    sf: P(inset, [-122.42, 37.77]), fremont: P(inset, [-121.99, 37.55]), pasadena: P(inset, [-118.14, 34.15]),
  },
}));
console.log('ok', JSON.stringify({ box, ca, clipY }));
