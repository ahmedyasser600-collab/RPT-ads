"""Assemble the RPT bathroom stage from the read-only master library.

Appends the asset collections from RPT_Master_Library.blend into a new scene,
places each one by moving its *_ROOT empty only, sets up interior lighting and a
9:16 camera, and saves campaigns/rpt-30s-rate/blender/stage.blend.
The library files are never modified.

Run: python3 build_stage.py   (bpy 4.5) — or blender -b --python build_stage.py
"""
import math
import os

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LIB = os.path.join(REPO, "RPT_Master_Library.blend")
OUT = os.path.join(HERE, "stage.blend")

# Layout in metres (Blender: X right, -Y front, Z up). Room interior: x ±1.10, y -1.40..1.35.
# (collection, root location, root Z rotation in degrees)
LAYOUT = {
    "RPT_12_room_shell": ((0.0, 0.0, 0.0), 0),
    "RPT_05_shower_tray": ((-0.65, 0.75, 0.0), 90),     # 0.90 wide x 1.20 deep walk-in
    "RPT_07_rain_shower": ((-0.65, 1.33, 0.0), 0),
    "RPT_06_glass_screen": ((-0.176, 0.89, 0.0), 90),    # on the tray edge, open at the front
    "RPT_02_vanity": ((0.40, 1.095, 0.0), 0),         # x -0.115..0.915: clear of glass and walls
    "RPT_03_basin": ((0.40, 1.07, 0.831), 0),
    "RPT_04_faucet": ((0.40, 1.31, 0.831), 0),
    "RPT_08_mirror": ((0.40, 1.33, 1.12), 0),
    "RPT_10_plumbing": ((0.40, 1.26, 0.0), 0),
    "RPT_01_toilet": ((-0.82, -0.45, 0.0), -90),
    "RPT_11_floor_layers": ((-0.65, 0.75, -0.40), 0),   # parked below the floor for the cutaway
    "RPT_09_tiles": ((0.40, 1.338, 1.0), 0),            # spare panel, used in the assembly shot
}


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = "RPT_Stage"

    with bpy.data.libraries.load(LIB, link=False) as (src, dst):
        dst.collections = [c for c in src.collections if c in LAYOUT]
    for coll in dst.collections:
        scene.collection.children.link(coll)
        root = bpy.data.objects[coll.name + "_ROOT"]
        loc, rot = LAYOUT[coll.name]
        root.location = loc
        root.rotation_euler = (0, 0, math.radians(rot))
    # Spare tile panel and floor section start hidden; shots enable them.
    for name in ("RPT_09_tiles", "RPT_11_floor_layers"):
        bpy.data.collections[name].hide_render = True

    # World: soft neutral-warm ambient.
    world = bpy.data.worlds.new("RPT_World")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.92, 0.88, 0.82, 1)
    bg.inputs[1].default_value = 0.35
    scene.world = world

    # Lights: one warm key from the open front-left (fixed light direction for the whole film),
    # a soft ceiling panel and the mirror's own LED ring.
    def area(name, loc, rot, size, energy, color):
        data = bpy.data.lights.new(name, "AREA")
        data.size, data.energy, data.color = size, energy, color
        obj = bpy.data.objects.new(name, data)
        obj.location, obj.rotation_euler = loc, [math.radians(a) for a in rot]
        scene.collection.objects.link(obj)
        return obj

    area("Key_FrontLeft", (-1.6, -2.4, 2.6), (60, 0, -35), 2.0, 900, (1.0, 0.93, 0.84))
    area("Ceiling_Panel", (0.0, 0.2, 2.45), (0, 0, 0), 1.2, 250, (1.0, 0.96, 0.9))
    area("Fill_Right", (2.2, 0.0, 1.4), (0, 70, 0), 1.5, 150, (0.95, 0.97, 1.0))

    cam_data = bpy.data.cameras.new("RPT_Cam")
    cam_data.lens = 24
    cam = bpy.data.objects.new("RPT_Cam", cam_data)
    cam.location = (0.15, -2.9, 1.35)
    cam.rotation_euler = (math.radians(88), 0, 0)
    scene.collection.objects.link(cam)
    scene.camera = cam

    r = scene.render
    r.engine = "CYCLES"
    r.resolution_x, r.resolution_y = 1080, 1920
    r.fps = 30
    scene.cycles.device = "CPU"
    scene.cycles.samples = 64
    scene.cycles.use_denoising = True
    scene.view_settings.view_transform = "AgX"
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print("saved", OUT)


if __name__ == "__main__":
    main()
