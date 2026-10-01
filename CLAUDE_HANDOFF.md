# Claude Code handoff — RPT bathroom videos

## Goal and boundaries

Use these actual 3D assets in 20–30 second Italian RPT bathroom-renovation reels.
Read README.md, manifest.json and VERIFICATION.md first. Inspect CATALOG.png.
Ask the user for the specific reel objective, approved message, 2–3 motion/editing
references, CTA and voiceover audio. Do not treat the included illustrative
bathrooms as photographs of RPT's completed client work.

Keep this library read-only. Create a separate campaign folder. Preserve existing
projects and completed videos. Do not install paid services or change global settings.
Keep brand logo, headlines, captions and CTA separate from the 3D object artwork.

## Workflow A — recommended for consistent film rendering

1. Append the desired RPT collection from an asset .blend. Move its ROOT, not each mesh.
2. Put the collection into a shot scene. Use the provided studio camera/lights as
   a starting point or light the assembled room realistically.
3. Keyframe named controls at explicit frame numbers. For example, move
   `Vanity_Drawer_2.location.y` from 0 to -0.30 m; rotate `WC_Lid_Hinge.rotation_euler.x`
   from 0 to -1.4 radians. Inspect the in-between frames.
4. Render RGBA PNG frames. Composite the numbered sequence in the existing
   video pipeline; use the alpha channel rather than removing a background.
5. Add approved logo, Italian text and CTA as separate 2D layers. Maintain
   comfortable mobile safe margins and avoid placing text behind app controls.
6. Mix the user-supplied voiceover and licensed music/SFX. The demo contains no audio.
7. Encode a review, inspect it, then render production quality. Do not silently
   reuse 640 px review renders for a full-screen 1080 px final deliverable.

For the supplied sequence, PNG `frame_0001.png` corresponds to time 0;
`frame_0090.png` corresponds to 89/30 seconds. Display all 90 frames for 3 seconds.
Use explicit frame-to-time mapping and avoid cumulative timestep animation drift.

## Workflow B — browser-based 3D

Import `exports/<asset>.glb` using the existing project's glTF loader. No new
framework is required. The GLBs contain geometry, PBR materials and named roots
and pivots, not cameras, studio lights or animation clips. Add suitable environment
lighting; a mirror reflects that environment and glass requires transmission support.

GLB is Y up. Blender-space (x,y,z) corresponds to glTF (x,z,-y). A Blender drawer
translation along -Y generally becomes glTF +Z; inspect the imported hierarchy
and parent rotations before scripting. Do not assume pivot-local axes if you
flatten or reparent the glTF scene. Use the manifest names to locate nodes.

Example pseudocode:

```js
const model = await loader.loadAsync('exports/02_vanity.glb');
scene.add(model.scene);
const drawer = model.scene.getObjectByName('Vanity_Drawer_2');
const closed = drawer.position.clone();
// Inspect local axes in this renderer before translating. Preserve closed pose.
// Evaluate the pose from frame/30, not repeated position += delta operations.
```

Exported bevels and curves are baked meshes. Procedural micro-bump is not baked
to textures and does not transfer. PBR base colors/roughness/metallic/transmission
and emission transfer, but rendering is not pixel-identical. Blender AgX, studio
lighting, mirror reflections, glass transmission and emission/bloom require
renderer-specific setup. Inspect GLB renders before using them in a campaign.

## Voiceover workflow

The user intends to create natural-sounding narration with Google AI Studio.
Request the exported WAV/MP3; no Google account integration, TTS generation or
voice cloning is included in this library. If generated speech is used, do not
describe it as a recording by a human actor. Listen for Italian pronunciation,
especially “Ristrutturare per Te”, and align edits to the delivered audio rather
than assuming text-to-speech timing. Obtain approval before using any real
person's cloned voice.

## Suggested first reel structure (adapt to approved narration)

- Hook: show the floor layers separating. Message: what matters lies beneath the finish.
- Explain: plumbing kit, waterproofing layer, tile finish; no installation claims.
- Reveal: vanity, basin, shower and mirror in the room shell.
- CTA: approved RPT logo and an editable contact/consultation message.

The 3-second demo is a component of this reel, not a completed narrated campaign.

