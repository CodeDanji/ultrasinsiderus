"""Render a single existing GLB reference scene from three views in Blender.

This does not fit a model to photos. Run with Blender --background --python ... -- args.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector

p=argparse.ArgumentParser()
p.add_argument('--model',required=True,type=Path)
p.add_argument('--output',required=True,type=Path)
p.add_argument('--width',type=int,default=1600)
p.add_argument('--height',type=int,default=1200)
p.add_argument('--layers',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
if not a.model.is_file() or a.model.suffix.lower() != '.glb':
    raise SystemExit('A local GLB reference model is required')
if a.width < 64 or a.height < 64:
    raise SystemExit('Output dimensions must be at least 64 pixels')
a.output.mkdir(parents=True,exist_ok=True)
if any((a.output / f'{name}.png').exists() for name in ('front','side','oblique')) or (a.output/'render.json').exists():
    raise SystemExit('Output already exists; choose a new directory')
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(a.model.resolve()))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and not o.hide_render]
if not meshes: raise SystemExit('No visible meshes in GLB')
points=[obj.matrix_world @ Vector(corner) for obj in meshes for corner in obj.bound_box]
lo=Vector(tuple(min(v[i] for v in points) for i in range(3)))
hi=Vector(tuple(max(v[i] for v in points) for i in range(3)))
center=(lo+hi)/2; span=max(hi-lo)
if span <= 1e-8: raise SystemExit('Model has zero-size bounds')
scene=bpy.context.scene
scene.render.engine='CYCLES'; scene.cycles.samples=32; scene.cycles.use_denoising=False
bpy.context.view_layer.cycles.use_denoising=False
scene.render.resolution_x=a.width; scene.render.resolution_y=a.height; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.world.color=(0.045,0.065,0.08)
scene.view_settings.view_transform='AgX'
# Material-independent lighting for imported reference models.
bpy.ops.object.light_add(type='AREA',location=center+Vector((span*1.5,-span*2,span*2)))
light=bpy.context.object; light.data.energy=250*span*span; light.data.shape='DISK'; light.data.size=span*2
light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
for position,energy in [((-1.5,-1,1),180),((.5,2,1.5),300)]:
    bpy.ops.object.light_add(type='AREA',location=center+Vector(position)*span)
    fill=bpy.context.object; fill.data.energy=energy*span*span; fill.data.size=span*2
    fill.rotation_euler=(center-fill.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(); camera=bpy.context.object; scene.camera=camera
camera.data.type='ORTHO'; camera.data.ortho_scale=span*1.6 * max(1, a.height/a.width)
for name, direction in [('front',(0,-3,1)),('side',(3,0,1)),('oblique',(2,-2,1.5))]:
    camera.location=center+Vector(direction).normalized()*span*3
    camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str((a.output/f'{name}.png').resolve())
    bpy.ops.render.render(write_still=True)
if a.layers:
    camera.location=center+Vector((1.2,-3,1.3)).normalized()*span*3
    camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
    for layer in ['bones','muscles','vessels','fat']:
        for obj in meshes:
            name=obj.name.lower()
            kind=('fat' if 'fat pad' in name else 'vessels' if 'arteries' in name else 'muscles' if obj.data.materials and obj.data.materials[0].name.startswith('muscle') else 'bones')
            obj.hide_render=(kind!=layer and not (layer in ['muscles','vessels','fat'] and kind=='bones'))
        scene.render.filepath=str((a.output/f'{layer}.png').resolve()); bpy.ops.render.render(write_still=True)
    for obj in meshes: obj.hide_render=False
sha=hashlib.sha256(a.model.read_bytes()).hexdigest()
(a.output/'render.json').write_text(json.dumps({'status':'reference_render_only','model_sha256':sha,'views':['front.png','side.png','oblique.png'],'personalized':False,'measured_anatomy':False,'width':a.width,'height':a.height,'blender_version':bpy.app.version_string,'warning':'Generic reference. No photo fitting, image quality assessment or clinical use.'},indent=2)+'\n')
