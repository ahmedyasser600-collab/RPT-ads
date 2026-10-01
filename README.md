# RPT — Bathroom 3D Starter Library

12 original, editable architectural assets for renovation reels and explainers.
These are generic illustrative designs, not manufacturer products, surveyed RPT
projects, plumbing specifications or a library guaranteed to cover every future video.

## Start here

1. Open `CATALOG.png` to choose an asset.
2. Open its file in `assets/` in Blender 4.5 LTS or later. Select the named asset
   scene from the scene menu if necessary. Each asset includes a camera and three lights.
3. Move the `RPT_*_ROOT` empty to move the whole asset. Use the named pivots in
   `manifest.json` for drawers, seat, lid, lever and floor-layer motion.
4. Save campaign-specific copies outside `assets/`; keep masters unchanged.
5. Give Claude Code this folder and `CLAUDE_HANDOFF.md`, not just the catalog.

`RPT_Master_Library.blend` includes organized asset collections, separate studio
scenes and a collection-instance overview. Register this folder in Blender's Asset
Libraries preferences to access the collection assets. The supplied catalog file
groups them under RPT/Bathroom. Do not change global preferences automatically.

## Visual direction and brand

The supplied references favor realistic architectural proportions, small softened
edges, white ceramic, warm stone, fluted oak, sage/blue tile, glass and brushed metal.
These are medium-distance starter models, not scanned materials or macro-ready
manufacturing replicas. Use the same palette and studio lighting across a sequence.

RPT yellow `#F5BB1D` is a median sample of yellow pixels in the supplied raster logo.
It is NOT an official supplied color code. Lighting, exposure, AgX and the browser's
tone mapping change its rendered appearance. The editable yellow material is included
in the master; campaign graphics should use a separate flat-color overlay.

The supplied raster logo is retained unchanged in `brand/`. No vector tracing,
wordmark reconstruction or 3D extrusion was performed. There is consequently no
reconstructed-logo comparison to approve. Supply the vector master and licensed
brand font before adding an extruded logo or editable branded typography.
Catalog text uses bundled DejaVu Sans solely for documentation, not as RPT's official font.
No headline, caption or CTA is baked onto a model.

## Scale, transforms and editing

- Blender: metres, Z up, X right, front faces toward -Y. GLB: standard glTF Y-up conversion.
- Roots and moving pivots have unit scale. Primitive geometry scale is applied.
- Object locations are deliberate assembly offsets. Curves and edge modifiers remain
  editable in Blender; export copies are evaluated meshes.
- Toilet and vanity include their intended mounting height above floor; do not
  automatically ground every individual mesh.
- Materials use Principled BSDF. Replace material slots to swap finishes. Meshes
  have UVs; editable pipe paths have no authored label UVs. Create a new UV layout
  after converting a pipe if a label is needed. No product labels/screens are required here.
- Drawer translation: local -Y. Toilet opening: negative local X rotation.
  Floor separation: local +Z. Full names and suggested ranges are in the manifest.
- Ranges are documented controls, not mechanical constraint simulations. Do not
  exceed them without checking clearances.

## Included assets

| Asset | Useful video action |
|---|---|
| Wall-hung toilet | Fixture reveal; seat/lid opening |
| Fluted oak vanity | Drawer/storage reveal |
| Countertop basin | Ceramic silhouette and drain close-up |
| Mixer tap | Finish comparison; lever movement |
| Low-profile shower tray | Walk-in shower assembly |
| Glass shower screen | Spatial division |
| Rain shower set | Feature reveal |
| Illuminated mirror | Preparation and lighting area |
| Modular tile panel | Material swap or tile assembly |
| Supply/waste kit | Explain hidden services |
| Layered floor section | Explain concealed renovation layers |
| Cutaway room shell | Stage fixture layouts and before/after concepts |

The room shell has a 2.2 × 2.8 m interior and a 2.5 m wall height. It is a staging
shell, not a furnished completed bathroom. Fixtures remain modular for reuse.
The floor section exaggerates layer visibility for communication; colors, order
and thicknesses are illustrative, not installation instructions.

## Rebuild and render

Requires Blender 4.5 LTS, Python 3 with Pillow for catalogs, and ffmpeg/ffprobe for
video encoding and checking. Blender itself is not redistributed in this package.
No paid assets, services, global settings or plugins are needed.

From this folder, with Blender on PATH:

```sh
blender -b --factory-startup -t 6 --python scripts/build_library.py -- --render
blender -b animation/floor_assembly.blend -t 6 -o //frames/frame_ -a
blender -b --factory-startup -t 6 --python scripts/verify_library.py
python scripts/make_catalog.py
python scripts/encode_review.py
```

On Windows replace `blender` with the quoted path to your installed `blender.exe`.
Run these commands only in a working copy: rebuilding replaces generated asset
files, previews, the manifest and master in that copy. It never edits supplied references.

## Animation

`animation/floor_assembly.blend`: 90 frames, 30 fps, frames 1–90 = 3.0 seconds.
Five named layers begin separated, assemble from the bottom upward and hold.
Motion is explicitly keyframed and does not depend on playback history. The
transparent PNG sequence is the compositing master. MP4 is a silent opaque review
on a warm background; standard H.264 does not retain alpha.

Review settings: 640 × 640, Cycles CPU, denoising, 12 samples for animation and
24 samples for stills (256 for the glass screen), transparent RGBA, AgX. Glass
uses transparent-glass film so its background can be composited. Final-production starting point:
1080 × 1920 for a complete reel or 1440–2160 square for an overlay, Cycles 128–256
samples with denoising, fixed exposure, 30 fps. Reframe the camera when changing
aspect ratio. Inspect glass edges, soft shadows and thin lines at final resolution.
Final-resolution renders are not included or represented as tested.

## Delivery and checks

See `verification/` for actual automated results and `VERIFICATION.md` for the
checks performed, visual-review findings and limitations. Portable files use no
machine-specific textures. See `licenses/` for source asset and font notices.
