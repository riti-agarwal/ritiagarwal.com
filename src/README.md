# ritiagarwal.com source

`../index.html` is generated. Edit the files here, then rebuild.

| File | What it is |
|------|-----------|
| `portal.html` | The page template: styles, floor plan, rooms, and script. `{{PLACEHOLDERS}}` are filled in by the build. |
| `build_portal.py` | Fills the placeholders with map data, copies the floor-plan drawing into the phone tiles, and writes `../index.html`. |
| `svg.json` | Small equirectangular world outline (used by the framed mini map in the map room on the floor plan). |
| `svg2.json` | The map room's world map: Natural Earth outline, graticule, coastlines, California inset, pin positions. |
| `svgpaths.mjs`, `svgpaths2.mjs` | Regenerate `svg.json` / `svg2.json` from world-atlas coastlines. Only needed to change the maps. |

## Rebuild the page

```bash
python3 build_portal.py
```

## Regenerate the map data (only if you change the maps)

```bash
npm install
node svgpaths.mjs . svg.json
node svgpaths2.mjs . svg2.json
python3 build_portal.py
```

Room text lives in `portal.html` inside each `<section class="room-section">`. The floor-plan drawing is the `<svg class="plan">` block; the phone tiles reuse it automatically.
