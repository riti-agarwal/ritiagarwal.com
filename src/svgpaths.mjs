// Emits SVG path data for the portal's world map (with a California inset) and pin positions.
import { createRequire } from 'module';
import { readFileSync, writeFileSync } from 'fs';
const dep = process.argv[2], out = process.argv[3];
const require = createRequire(dep + '/package.json');
const { feature } = require('topojson-client');
const d3 = await import(dep + '/node_modules/d3-geo/src/index.js');
const load = f => { const t = JSON.parse(readFileSync(dep + '/node_modules/world-atlas/' + f)); return feature(t, t.objects.land); };
const land110 = load('land-110m.json'), land50 = load('land-50m.json');

const W = 600, TOP = 80, BOTTOM = -60, k = W / 360, H = Math.round((TOP - BOTTOM) * k);
const rad = Math.PI / 180;
const world = d3.geoEquirectangular().scale(k / rad).translate([W / 2, TOP * k]).clipExtent([[0, 0], [W, H]]);

// inset in the empty South Pacific
const box = { x: 12, y: 132, w: 150, h: 92 };
const cos36 = Math.cos(36 * rad);
const inset = d3.geoProjection((l, p) => [l * cos36, p])
  .fitExtent([[box.x + 8, box.y + 8], [box.x + box.w - 8, box.y + box.h - 8]],
    { type: 'MultiPoint', coordinates: [[-123.3, 38.3], [-117.3, 33.7]] });
inset.clipExtent([[box.x, box.y], [box.x + box.w, box.y + box.h]]);

const path = (proj, geo) => d3.geoPath(proj).digits(1)(geo);
const P = (proj, ll) => proj(ll).map(v => +v.toFixed(1));
const ca = [[-124.6, 42.1], [-114.1, 32.5]].map(ll => P(world, ll));
writeFileSync(out, JSON.stringify({
  W, H, box,
  world: path(world, land110),
  inset: path(inset, land50),
  caRect: [ca[0][0], ca[0][1], ca[1][0] - ca[0][0], ca[1][1] - ca[0][1]],
  pins: {
    bangalore: P(world, [77.59, 12.97]),
    sf: P(inset, [-122.42, 37.77]), fremont: P(inset, [-121.99, 37.55]), pasadena: P(inset, [-118.14, 34.15]),
  },
}));
console.log('W', W, 'H', H);
