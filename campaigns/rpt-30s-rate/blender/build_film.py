"""Build film.blend: the 30s RPT reel timeline on top of stage.blend.

Frame n shows time (n-1)/30 s. 3D runs frames 1-780; frames 781-900 are the 2D end card.
Every motion is keyframed at explicit frames (no simulation, no cumulative steps).

  S1   1-120  doorway reveal onto vanity / basin / mirror, mirror LED switches on
  S2 121-270  cutaway: finishes removed, plumbing on the wall, floor layers separate and settle
  S3 271-480  assembly: tiles settle, tray, shower, glass slides in, vanity + basin + tap,
              mirror, drawer opens and closes
  S4 481-690  completed bathroom, slow move (financing panel is a 2D overlay)
  S5 691-780  strongest composition, slow push (end card follows in 2D)

Run after build_stage.py:  python3 build_film.py
"""
import math
import os

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, "stage.blend"))
scene = bpy.context.scene
scene.name = "RPT_Film"
scene.frame_start, scene.frame_end = 1, 780
O = bpy.data.objects


# ------------------------------------------------------------------ helpers

def key(obj, path, frame, value, interp="BEZIER"):
    """Set obj.<path> = value and keyframe it at an explicit frame."""
    target = obj
    attr = path
    if "." in path:
        head, attr = path.rsplit(".", 1)
        target = obj.path_resolve(head)
    setattr(target, attr, value)
    obj.keyframe_insert(data_path=path, frame=frame)
    for fc in obj.animation_data.action.fcurves:
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                if int(kp.co.x) == frame:
                    kp.interpolation = interp
                    kp.easing = "AUTO"


def visible(obj, frame, on):
    """Show/hide an object (and its children) for rendering from `frame`, with constant steps."""
    for o in [obj] + list(obj.children_recursive):
        o.hide_render = not on
        o.keyframe_insert("hide_render", frame=frame)
        for fc in o.animation_data.action.fcurves:
            if fc.data_path == "hide_render":
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"


def move_in(obj, f0, f1, offset, base=None):
    """Assembled in S1 (frames 1-120), then jump to base+offset at f0 and ease into base by f1."""
    base = Vector(base if base is not None else obj.location)
    key(obj, "location", 1, base, "CONSTANT")
    key(obj, "location", 120, base, "CONSTANT")   # hold, no drift while hidden in S2
    key(obj, "location", f0, base + Vector(offset))
    key(obj, "location", f1, base)


def box(name, size, loc, mat):
    mesh = bpy.data.meshes.new(name)
    sx, sy, sz = (s / 2 for s in size)
    verts = [(x, y, z) for x in (-sx, sx) for y in (-sy, sy) for z in (-sz, sz)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(mat)
    obj = bpy.data.objects.new(name, mesh)
    obj.location = loc
    scene.collection.objects.link(obj)
    return obj


# ------------------------------------------------------------------ look-dev

world = scene.world
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.96, 0.93, 0.88, 1)   # warm studio backdrop, also what the mirror sees
bg.inputs[1].default_value = 1.1
# Seen directly (or in the mirror) the backdrop is a clean bright warm white; lighting stays soft.
nt = world.node_tree
lp = nt.nodes.new("ShaderNodeLightPath")
backdrop = nt.nodes.new("ShaderNodeBackground")
backdrop.inputs[0].default_value = (0.97, 0.94, 0.89, 1)
backdrop.inputs[1].default_value = 3.2
mix = nt.nodes.new("ShaderNodeMixShader")
seen = nt.nodes.new("ShaderNodeMath")
seen.operation = "MAXIMUM"
nt.links.new(lp.outputs["Is Camera Ray"], seen.inputs[0])
nt.links.new(lp.outputs["Is Glossy Ray"], seen.inputs[1])
nt.links.new(seen.outputs[0], mix.inputs[0])
nt.links.new(bg.outputs[0], mix.inputs[1])
nt.links.new(backdrop.outputs[0], mix.inputs[2])
nt.links.new(mix.outputs[0], nt.nodes["World Output"].inputs[0])
scene.view_settings.exposure = -0.85
scene.view_settings.look = "AgX - Medium High Contrast"

for name in ("Key_FrontLeft", "Ceiling_Panel", "Fill_Right"):
    bpy.data.objects.remove(O[name])


def area(name, loc, target, size, energy, color):
    data = bpy.data.lights.new(name, "AREA")
    data.size, data.energy, data.color = size, energy, color
    obj = bpy.data.objects.new(name, data)
    obj.location = loc
    obj.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    scene.collection.objects.link(obj)
    return obj


# One fixed light direction for the whole film: warm key from high front-left.
area("Key_HighLeft", (-1.4, -0.9, 3.9), (0.2, 0.9, 0.6), 1.6, 650, (1.0, 0.90, 0.78))
area("Soft_Top", (0.3, 0.3, 3.2), (0.3, 0.6, 0.0), 2.4, 260, (1.0, 0.96, 0.90))
area("Fill_FrontRight", (2.6, -2.2, 1.6), (0.3, 0.8, 1.0), 2.0, 140, (0.96, 0.97, 1.0))

# Doorway wall (staging geometry only, library Stone material); used in S1.
stone = bpy.data.materials["Stone"]
door_l, door_r, door_h, wall_y = 0.15, 0.95, 2.10, -1.48
front = [
    box("Stage_Front_Left", (door_l + 1.26, 0.16, 2.5), ((door_l - 1.26) / 2, wall_y, 1.25), stone),
    box("Stage_Front_Right", (1.26 - door_r, 0.16, 2.5), ((door_r + 1.26) / 2, wall_y, 1.25), stone),
    box("Stage_Front_Lintel", (door_r - door_l, 0.16, 2.5 - door_h), ((door_l + door_r) / 2, wall_y, (2.5 + door_h) / 2), stone),
]

# ------------------------------------------------------------------ cameras + markers


def camera(name, lens=24):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    data.sensor_fit = "VERTICAL"
    cam = bpy.data.objects.new(name, data)
    scene.collection.objects.link(cam)
    return cam


def aim(cam, frame, loc, target, interp="BEZIER"):
    cam.location = loc
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    for path in ("location", "rotation_euler"):
        cam.keyframe_insert(path, frame=frame)
    for fc in cam.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            if int(kp.co.x) == frame:
                kp.interpolation = interp


VANITY = (0.40, 1.25, 1.15)
ROOM = (0.0, 0.6, 1.0)

c1 = camera("Cam_S1_Doorway", 22)
aim(c1, 1, (0.55, -3.7, 1.45), VANITY)
aim(c1, 120, (0.45, -1.05, 1.42), VANITY)

c2 = camera("Cam_S2_Cutaway", 24)
aim(c2, 121, (1.60, -1.80, 2.50), (-0.15, 0.90, 0.38))
aim(c2, 270, (1.40, -1.55, 2.30), (-0.17, 0.93, 0.36))

c3 = camera("Cam_S3_Assembly", 24)
aim(c3, 271, (2.10, -2.60, 2.30), (0.05, 0.70, 0.75))
aim(c3, 480, (1.10, -3.00, 1.75), (0.05, 0.75, 0.95))

c4 = camera("Cam_S4_Finished", 24)
aim(c4, 481, (0.25, -2.75, 1.40), (0.15, 0.6, 1.0))
aim(c4, 690, (0.55, -2.50, 1.35), (0.15, 0.6, 1.0))

c5 = camera("Cam_S5_Hero", 28)
aim(c5, 691, (0.10, -2.40, 1.30), (0.22, 1.1, 1.05))
aim(c5, 780, (0.12, -2.15, 1.28), (0.22, 1.1, 1.05))

for frame, cam in ((1, c1), (121, c2), (271, c3), (481, c4), (691, c5)):
    m = scene.timeline_markers.new(cam.name, frame=frame)
    m.camera = cam
scene.camera = c1

# ------------------------------------------------------------------ S1: doorway + LED

for w in front:
    visible(w, 1, True)
    visible(w, 121, False)

led_bsdf = bpy.data.materials["LED"].node_tree.nodes["Principled BSDF"]
strength = led_bsdf.inputs["Emission Strength"]
strength.default_value = 0.0
strength.keyframe_insert("default_value", frame=20)
strength.default_value = 3.0
strength.keyframe_insert("default_value", frame=45)

# ------------------------------------------------------------------ S2: cutaway

finished = ["RPT_02_vanity_ROOT", "RPT_03_basin_ROOT", "RPT_04_faucet_ROOT", "RPT_08_mirror_ROOT",
            "RPT_05_shower_tray_ROOT", "RPT_06_glass_screen_ROOT", "RPT_07_rain_shower_ROOT"]
for n in finished:
    visible(O[n], 1, True)
    visible(O[n], 121, False)   # cut to the cutaway: fixtures removed

tiles = sorted([o for o in O if o.name.startswith("Room_Sage_Tile")], key=lambda o: (round(o.location.z, 2), o.location.x))
for t in tiles:
    visible(t, 1, True)
    visible(t, 121, False)

floor = O["RPT_11_floor_layers_ROOT"]
bpy.data.collections["RPT_11_floor_layers"].hide_render = False
floor.location = (-0.65, 0.75, -0.226)          # finish sits 3 mm proud of the room floor
visible(floor, 1, False)
visible(floor, 121, True)
visible(floor, 271, False)
# Layers separate (manifest ranges) then settle back, bottom-up.
LAYERS = [("Floor_01_Screed", 0.17), ("Floor_02_Membrane", 0.34), ("Floor_03_Adhesive", 0.51), ("Floor_04_Finish", 0.68)]
for i, (name, top) in enumerate(LAYERS):
    layer = O[name]
    key(layer, "location", 121, Vector((0, 0, 0)))
    key(layer, "location", 150 + i * 6, Vector((0, 0, top)))
    key(layer, "location", 205, Vector((0, 0, top)))
    key(layer, "location", 250 + i * 4, Vector((0, 0, 0)))

plumb = O["RPT_10_plumbing_ROOT"]
visible(plumb, 1, False)
visible(plumb, 121, True)
visible(plumb, 420, False)                       # hidden again once the vanity is back

# ------------------------------------------------------------------ S3: assembly

for i, t in enumerate(tiles):                     # tiles settle onto the wall, bottom-up, row by row
    f0 = 271 + i * 2
    visible(t, f0, True)
    move_in(t, f0, f0 + 14, (0, -0.35, 0.0))

move_in(O["RPT_05_shower_tray_ROOT"], 330, 352, (0, 0, 0.55))
visible(O["RPT_05_shower_tray_ROOT"], 330, True)
move_in(O["RPT_07_rain_shower_ROOT"], 345, 368, (0, -0.45, 0))
visible(O["RPT_07_rain_shower_ROOT"], 345, True)
move_in(O["RPT_06_glass_screen_ROOT"], 360, 390, (0, -0.55, 0))      # glass slides along the tray edge
visible(O["RPT_06_glass_screen_ROOT"], 360, True)
move_in(O["RPT_02_vanity_ROOT"], 380, 404, (0.0, -0.55, 0))
visible(O["RPT_02_vanity_ROOT"], 380, True)
move_in(O["RPT_03_basin_ROOT"], 398, 416, (0, 0, 0.35))
visible(O["RPT_03_basin_ROOT"], 398, True)
move_in(O["RPT_04_faucet_ROOT"], 408, 422, (0, 0, 0.25))
visible(O["RPT_04_faucet_ROOT"], 408, True)
move_in(O["RPT_08_mirror_ROOT"], 412, 432, (0, 0, 0.45))
visible(O["RPT_08_mirror_ROOT"], 412, True)

drawer = O["Vanity_Drawer_2"]                     # manifest: local Y, range -0.32..0
key(drawer, "location", 440, Vector((0, 0, 0)))
key(drawer, "location", 452, Vector((0, -0.30, 0)))
key(drawer, "location", 466, Vector((0, -0.30, 0)))
key(drawer, "location", 478, Vector((0, 0, 0)))

# Everything stays assembled from here to the end of the 3D part (S4, S5).
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "film.blend"))
print("saved film.blend")
