"""Render a frame range of film.blend to PNG (resumable).

Inside Blender (recommended on a PC with a graphics card):
  blender -b --python render_frames.py -- <first> <last> <out_dir> [percent=100] [samples=128] [gpu]
As a Python module (bpy):
  python3 render_frames.py <first> <last> <out_dir> [percent] [samples] [gpu]

Frame n is written as <out_dir>/frame_<n:04d>.png; frames that already exist are skipped,
so an interrupted render can simply be started again.
"""
import os
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
first, last, out = int(argv[0]), int(argv[1]), os.path.abspath(argv[2])
percent = int(argv[3]) if len(argv) > 3 else 100
samples = int(argv[4]) if len(argv) > 4 else 128
use_gpu = len(argv) > 5 and argv[5].lower() == "gpu"

bpy.ops.wm.open_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "film.blend"))
sc = bpy.context.scene

if use_gpu:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for backend in ("OPTIX", "CUDA", "HIP", "ONEAPI", "METAL"):
        try:
            prefs.compute_device_type = backend
        except TypeError:
            continue
        prefs.get_devices()
        gpus = [d for d in prefs.devices if d.type == backend]
        if gpus:
            for d in prefs.devices:
                d.use = d.type == backend
            sc.cycles.device = "GPU"
            print("GPU rendering with", backend, [d.name for d in gpus], flush=True)
            break
    else:
        print("No supported GPU found: rendering on CPU", flush=True)

sc.render.resolution_percentage = percent
c = sc.cycles
c.samples, c.adaptive_threshold = samples, 0.02
c.use_denoising, c.denoiser = True, "OPENIMAGEDENOISE"
c.max_bounces, c.diffuse_bounces, c.glossy_bounces = 8, 4, 4
c.transmission_bounces = c.transparent_max_bounces = 8
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
