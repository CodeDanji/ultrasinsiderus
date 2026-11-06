"""Render registered orthographic reference layers with alpha for photo composition."""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True);p.add_argument('--info',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]); info=json.loads(a.info.read_text()); w,h=info['processed_dimensions']
if a.output.exists(): raise SystemExit('Output exists')
a.output.mkdir(parents=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);bpy.ops.import_scene.gltf(filepath=str(a.model.resolve()))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;bpy.context.view_layer.cycles.use_denoising=False
scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.resolution_percentage=100;scene.render.film_transparent=True
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.view_settings.view_transform='AgX'
scene.world.color=(.18,.18,.18)
center=Vector((0,0,h/w/2))
for pos,power,size in [((-.4,-1.1,1),80,1.4),((.8,-.6,.4),40,1),((0,.7,1),60,1.2)]:
 bpy.ops.object.light_add(type='AREA',location=pos);light=bpy.context.object;light.data.energy=power;light.data.size=size;light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(0,-3,h/w/2));camera=bpy.context.object;camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=1;scene.camera=camera
for layer in ('overview','bones','muscles','vessels','fat'):
 for obj in meshes:
  n=obj.name.lower();m=obj.data.materials[0].name if obj.data.materials else ''
  kind='fat' if 'fat pad' in n else 'vessels' if 'arteries' in n else 'muscles' if m.startswith('muscle') else 'bones'
  # Standalone vessel graphics remain context anchored to the same photo, rather than bones alone.
  obj.hide_render=kind not in ({'bones','muscles','vessels'} if layer=='overview' else {layer})
 scene.render.filepath=str((a.output/(layer+'.png')).resolve());bpy.ops.render.render(write_still=True)
(a.output/'registration.json').write_text(json.dumps({'camera':'orthographic side','image_dimensions':[w,h],'coordinate_frame':'x=pixel_x/w-0.5,z=(h-pixel_y)/w','personal_internal_measurement':False},indent=2))
