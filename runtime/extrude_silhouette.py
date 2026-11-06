"""Construct a schematic constant-depth 3D extrusion of an input mask.
Blender only; intentionally not a reconstruction or personal internal anatomy.
"""
import argparse, json, sys
from pathlib import Path
import bpy
p=argparse.ArgumentParser()
p.add_argument('--mask',required=True,type=Path); p.add_argument('--output',required=True,type=Path)
p.add_argument('--resolution',type=int,default=128); p.add_argument('--depth-ratio',type=float,default=0.22)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
if not a.mask.is_file() or not 32<=a.resolution<=512 or not 0<a.depth_ratio<=1:
    raise SystemExit('Invalid mask, resolution or depth ratio')
if a.output.exists(): raise SystemExit('Output already exists')
image=bpy.data.images.load(str(a.mask.resolve()),check_existing=False)
if image.size[0]<2 or image.size[1]<2: raise SystemExit('Invalid mask dimensions')
# Nearest sampling is sufficient for an explicitly schematic approximation.
width,height=image.size[:]; pixels=list(image.pixels)
w=a.resolution; h=max(1,round(w*height/width)); depth=a.depth_ratio
vertices=[]; faces=[]; active=0
for y in range(h):
    sy=min(height-1,int((y+0.5)*height/h)); x=0
    while x<w:
        sx=min(width-1,int((x+0.5)*width/w))
        if pixels[(sy*width+sx)*4]<0.5: x+=1; continue
        start=x
        while x<w and pixels[(sy*width+min(width-1,int((x+0.5)*width/w)))*4]>=0.5: x+=1
        x0=start/w-0.5; x1=x/w-0.5; z0=y/w; z1=(y+1)/w
        k=len(vertices); vertices += [(xx,yy,zz) for zz in (z0,z1) for yy in (-depth/2,depth/2) for xx in (x0,x1)]
        faces += [tuple(k+i for i in f) for f in ((0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3))]
        active+=x-start
if not active: raise SystemExit('Empty mask')
a.output.mkdir(parents=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
mesh=bpy.data.meshes.new('Schematic silhouette'); mesh.from_pydata(vertices,[],faces); mesh.update()
obj=bpy.data.objects.new('Schematic constant-depth silhouette',mesh); bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active=obj; obj.select_set(True)
mat=bpy.data.materials.new('Illustrative surface'); mat.diffuse_color=(0.12,0.55,0.65,1); obj.data.materials.append(mat)
bpy.ops.export_scene.gltf(filepath=str((a.output/'silhouette.glb').resolve()),export_format='GLB')
(a.output/'model.json').write_text(json.dumps({'status':'schematic_only','source_mask':a.mask.name,'depth_ratio_assumed':depth,'mask_grid':[w,h],'nonempty_cells':active,'personalized_internal_anatomy':False,'warning':'Single image extruded to assumed constant depth; no actual depth or internal anatomy measured.'},indent=2)+'\n')
