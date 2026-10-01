# Verification and limitations — delivery v1.0

## Checks actually performed

- Reopened all 12 individual Blender files, the master library and the animated
  Blender file using Blender 4.5.9 LTS.
- Checked every asset's required object names, single root hierarchy, unit root
  scale, named moving pivots and child geometry, material assignments, mesh UV
  presence, camera and studio lighting, and collection asset metadata.
- Checked for linked Blender libraries and unpacked external image dependencies:
  none are required by the models.
- Reimported all 12 GLB files into clean Blender scenes. Compared object names,
  parent relationships, evaluated triangle counts, world-space bounding boxes,
  world-space vertex clouds and core Principled/PBR material parameters.
  All passed. The detailed numerical evidence is `verification/geometry_checks.json`.
- Rendered and visually compared Blender-source versus reimported-GLB vanity,
  faucet, glass screen and mirror under matching studio lighting. See
  `verification/GLB_COMPARISON.png`. Shape and overall appearance agree at review
  resolution; this is not a test in a browser renderer.
- Inspected the 12 previews for framing, missing surfaces, shading and obvious
  intersections. Inspected toilet lid/seat, vanity drawers and faucet lever in
  representative open poses. Fixed the initial lever opening direction.
- Fixed the initial glass preview's opaque-background behavior using transparent
  glass film, and raised the glass still's sample count to 256 to reduce alpha noise.
- Checked all 90 animation frames numerically for finite, monotonic layer motion
  and a fully assembled end pose. No simulation is involved.
- Inspected all 90 rendered frames in a contact sheet, with a larger 10-frame
  sheet spanning the sequence. No obvious clipping, disappearance or layer
  crossing was observed at review resolution. The fixed camera intentionally
  leaves more headroom as the layers assemble downward.
- Checked all 90 PNGs for RGBA mode, 640 × 640 dimensions and transparent pixels.
  Source preview alpha bounds were also checked for contact with image borders;
  all 12 previews have clear margins.
- Encoded and probed the MP4: H.264, 640 × 640, 30 fps, 90 decoded frames,
  duration 3.000 seconds. The review has no audio track. Decoded beginning,
  midpoint and ending frames were inspected separately from the PNG sources.
- ZIP packaging checks required contents and archive CRC integrity. The
  packaging script prints the result and writes `RPT_Package_Integrity.json`
  beside the ZIP; individual file hashes are inside `verification/SHA256.json`.

## What was not tested or delivered

- Human real-time playback review and listening were not performed. There is no
  voiceover or music to evaluate. The user should play the MP4 before approving timing.
- No browser/Three.js runtime test, Windows Blender GUI test, final-resolution
  render, mechanical tolerance test or production plumbing validation was performed.
- The models are clean architectural starter assets with simplified construction
  and procedural surface detail, not photogrammetry or macro-ready product CAD.
- The room shell is unfurnished. It is ready to stage the separate assets, not a
  finished replica of one of the supplied bathroom images.
- GLBs do not include Blender lights, cameras, animation clips, modifiers or
  editable curves. Modifier results and curves are exported as geometry.
  Procedural micro-bump is not baked and does not transfer. PBR material parameters
  do transfer, but glass, mirror reflections, emission and color management will
  vary with the renderer and environment lighting. Alpha renders of refractive
  objects are compositing approximations, not physically exact refraction of a
  background that is added later.
- A mirror reflects the studio environment; its dark preview is not a screen or
  a missing texture. The LED ring is emissive, but stylized glow/bloom is not baked in.
- No extruded RPT logo was created because only raster artwork was supplied.
  The original is included unchanged. A vector master or tracing approval is
  needed for that separate asset. No official brand font was supplied.
- The floor and plumbing kit are illustrative. Do not use their dimensions,
  materials or topology as installation guidance or compliance claims.

This is a reusable starter library for the stated RPT video use cases, not a
guarantee of complete coverage of future campaigns.
