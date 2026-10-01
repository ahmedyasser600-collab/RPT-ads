"""Render a frame range of film.blend to PNG.

python3 render_frames.py <first> <last> <out_dir> [percent=100] [samples=24]
Frame n is written as <out_dir>/frame_<n:04d>.png; existing frames are skipped (resumable).
"""
import os
import sys

import bpy

first, last, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
percent = int(sys.argv[4]) if len(sys.argv) > 4 else 100
samples = int(sys.argv[5]) if len(sys.argv) > 5 else 24
bpy.ops.wm.open_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "film.blend"))
sc = bpy.context.scene
sc.render.resolution_percentage = percent
c = sc.cycles
c.samples, c.adaptive_threshold = samples, 0.05
c.use_denoising, c.denoiser = True, "OPENIMAGEDENOISE"
c.max_bounces, c.diffuse_bounces, c.glossy_bounces = 6, 3, 3
c.transmission_bounces = c.transparent_max_bounces = 6
c.caustics_reflective = c.caustics_refractive = False
sc.render.use_persistent_data = True
os.makedirs(out, exist_ok=True)
for f in range(first, last + 1):
    path = os.path.join(out, f"frame_{f:04d}.png")
    if os.path.exists(path):
        continue
    sc.frame_set(f)
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("done", f, flush=True)
