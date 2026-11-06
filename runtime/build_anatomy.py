"""Build an illustrative foot model from a licensed reference and side silhouette.

No personal anatomy is inferred. Blood vessels and fat are NOT included.
Run via Blender with --python-exit-code 1; see README for limitations.
"""
import argparse, bmesh, hashlib, json, sys
from pathlib import Path
import bpy
from mathutils import Vector

p=argparse.ArgumentParser()
p.add_argument('--anatomy',type=Path,required=True); p.add_argument('--mask-info',type=Path,required=True)
p.add_argument('--anchors',type=Path); p.add_argument('--silhouette',type=Path,required=True); p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
if not all(f.is_file() for f in (a.anatomy,a.mask_info,a.silhouette)): raise SystemExit('Missing input file')
if a.output.exists(): raise SystemExit('Output already exists')
info=json.loads(a.mask_info.read_text()); w,h=info['processed_dimensions']; x0,y0,x1,y1=info['bbox_xyxy']
if not (0<=x0<x1<=w and 0<=y0<y1<=h): raise SystemExit('Invalid mask bounds')
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(a.anatomy.resolve()))
# Apply world transforms, retain left foot/ankle structures and cut higher portions.
parts=[]; counts={'bone':0,'muscle':0}
for obj in list(bpy.context.scene.objects):
    if obj.type!='MESH': continue
    parent=obj.parent.name.lower() if obj.parent else ''
    name=obj.name.lower()
    corners=[obj.matrix_world@Vector(c) for c in obj.bound_box]
    if 'left' not in name or min(v.z for v in corners)>0.10 or max(v.z for v in corners)<0:
        continue
    if parent=='skeleton': tissue='bone'
    elif 'muscles' in parent: tissue='muscle'
    else: continue
    mesh=obj.data.copy(); mesh.transform(obj.matrix_world)
    bm=bmesh.new(); bm.from_mesh(mesh)
    bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=0.00001,plane_co=(0,0,0.20),plane_no=(0,0,1),clear_outer=True,clear_inner=False)
    boundary=[e for e in bm.edges if e.is_boundary]
    if boundary: bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
    bm.to_mesh(mesh); bm.free()
    if len(mesh.vertices)==0: continue
    parts.append((obj.name,tissue,mesh)); counts[tissue]+=1
if counts['bone']<10 or counts['muscle']<3: raise SystemExit('Reference missing expected bone/muscle structures')
# Remove imported hierarchy. Saved mesh copies use world coordinates.
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
points=[v.co for _,_,mesh in parts for v in mesh.vertices]
# Reference foot points towards negative Y; input must be a side view pointing right.
rawx=[-p.y for p in points]; rawz=[p.z for p in points]; rawy=[p.x for p in points]
rx0,rx1=min(rawx),max(rawx); rz0,rz1=min(rawz),max(rawz); ry0,ry1=min(rawy),max(rawy)
if min(rx1-rx0,rz1-rz0,ry1-ry0)<=0: raise SystemExit('Degenerate reference bounds')
# Fit bounding rectangle inside silhouette with margins; this is not landmark fitting.
tx0=x0/w-.5; tx1=x1/w-.5; tz0=(h-y1)/w; tz1=(h-y0)/w
sx=(tx1-tx0)*0.84/(rx1-rx0); sz=(tz1-tz0)*0.88/(rz1-rz0)
sy=(tx1-tx0)*0.30/(ry1-ry0)
materials={}
for kind,color in [('bone',(0.92,0.82,0.63,1)),('muscle',(0.58,0.22,0.19,1))]:
    mat=bpy.data.materials.new(kind); mat.diffuse_color=color; mat.use_nodes=True
    mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=color
    mat.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=0.42
    materials[kind]=mat
for name,kind,mesh in parts:
    for v in mesh.vertices:
        ox,oy,oz=v.co
        v.co=(((-oy-rx0)*sx)+tx0+(tx1-tx0)*.08, (ox-(ry0+ry1)/2)*sy, (oz-rz0)*sz+tz0+(tz1-tz0)*.06)
    obj=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(obj)
    obj.data.materials.clear(); obj.data.materials.append(materials[kind])
    for face in obj.data.polygons: face.use_smooth=True
# Use a single BVH for keeping the illustrative artery on the foot surface.
from mathutils.bvhtree import BVHTree
surface_vertices=[]; surface_faces=[]
for body in bpy.context.scene.objects:
    if body.type!='MESH': continue
    offset=len(surface_vertices)
    surface_vertices.extend([body.matrix_world@v.co for v in body.data.vertices])
    surface_faces.extend([tuple(offset+i for i in p.vertices) for p in body.data.polygons])
surface=BVHTree.FromPolygons(surface_vertices,surface_faces)
# Add a separately sourced arterial reference, using an approximate bounding fit.
# This is illustrative registration, not validated anatomical fusion.
vessel_file=Path(__file__).resolve().parent/'assets/vessels.glb'
if not vessel_file.is_file(): raise SystemExit('Vascular reference is missing')
before=set(bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=str(vessel_file.resolve()))
imported=set(bpy.context.scene.objects)-before
vm=None
for obj in imported:
    if obj.type=='MESH' and obj.name.startswith('foot-arteries'):
        vm=obj.data.copy(); vm.transform(obj.matrix_world)
        bm=bmesh.new(); bm.from_mesh(vm)
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),plane_co=(0,0,0),plane_no=(-1,0,0),clear_outer=True,clear_inner=False)
        bm.to_mesh(vm); bm.free()
for obj in imported: bpy.data.objects.remove(obj,do_unlink=True)
if vm is None or not vm.vertices: raise SystemExit('Foot arterial geometry missing')
vpoints=[v.co.copy() for v in vm.vertices]
vmins=[min(v[i] for v in vpoints) for i in range(3)]; vmaxs=[max(v[i] for v in vpoints) for i in range(3)]
# Map isolated arterial foot bounds to the lower 35% of the illustrative foot.
for v in vm.vertices:
    nx,ny,nz=[(v.co[i]-vmins[i])/max(1e-8,vmaxs[i]-vmins[i]) for i in range(3)]
    v.co=(tx0+(1-ny)*(tx1-tx0)*.65+(tx1-tx0)*.20, (nx-.5)*(tx1-tx0)*.16, tz0+(nz*.22+.08)*(tz1-tz0))
artery=bpy.data.objects.new('Reference foot arteries - approximate placement',vm); bpy.context.collection.objects.link(artery)
def tissue_mat(name,color):
    mat=bpy.data.materials.new(name); mat.diffuse_color=(*color,1); mat.use_nodes=True
    mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*color,1)
    return mat
for face in vm.polygons: face.use_smooth=True
vm.materials.clear(); vm.materials.append(tissue_mat('arterial reference',(0.7,.015,.025)))
counts['arterial_reference']=1
fatmat=tissue_mat('schematic fat pad',(.92,.55,.09))
for label,x,z,scale in [('Heel',.16,.065,(.07,.075,.028)),('Forefoot',.76,.065,(.09,.085,.022))]:
    length=tx1-tx0; height=tz1-tz0
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,location=(tx0+x*length,0,tz0+z*height))
    pad=bpy.context.object; pad.name=label+' fat pad - schematic assumption'
    pad.scale=(scale[0]*length,scale[1]*length,scale[2]*height)
    pad.data.materials.append(fatmat)
    for face in pad.data.polygons: face.use_smooth=True
counts['schematic_fat_pads']=2
# Outer silhouette is kept separately: GLB round-trip cannot preserve this shader reliably.
# Optional operator-labelled external landmarks: one common affine pose fit.
# Targets approximate reference placement; they do not reveal internal anatomy.
fit_info=None
if a.anchors:
    import numpy as np
    specification=json.loads(a.anchors.read_text())
    pairs=[]
    for anchor in specification['anchors']:
        obj=bpy.data.objects.get(anchor['mesh'])
        if obj is None or obj.type!='MESH': raise SystemExit('Anchor mesh missing: '+anchor['mesh'])
        coords=np.array([tuple(obj.matrix_world@v.co) for v in obj.data.vertices])
        if anchor.get('point')=='upper_end':
            coords=coords[coords[:,2]>coords[:,2].max()-(coords[:,2].max()-coords[:,2].min())*.03]
        point=coords.mean(axis=0)
        pixel=anchor['pixel_xy']
        pairs.append((point,[pixel[0]/w-.5,(h-pixel[1])/w]))
    design=np.array([list(point)+[1] for point,_ in pairs]);targets=np.array([target for _,target in pairs])
    coefficients,_,rank,_=np.linalg.lstsq(design,targets,rcond=None)
    if rank<4: raise SystemExit('Photo anchors do not constrain a full 3D-to-2D fit')
    rowx,rowz=coefficients[:3,0],coefficients[:3,1]
    depth=np.cross(rowz,rowx);depth=depth/np.linalg.norm(depth)*np.sqrt(np.linalg.norm(rowx)*np.linalg.norm(rowz))
    reference_center=np.mean([point for point,_ in pairs],axis=0)
    for obj in bpy.context.scene.objects:
        if obj.type!='MESH': continue
        for vertex in obj.data.vertices:
            point=np.array(tuple(vertex.co)); projected=np.append(point,1)@coefficients
            vertex.co=(projected[0],(point-reference_center)@depth,projected[1])
        obj['photo_pose_fit']='operator labelled external landmarks; generic internal reference only'
    residual=design@coefficients-targets
    fit_info={'method':'common affine pose fit from manually labelled external landmarks','anchors':specification['anchors'],'coefficients':coefficients.tolist(),'anchor_rms_pixels':float(np.sqrt((residual**2).mean())*w),'personal_internal_reconstruction':False}
a.output.mkdir(parents=True)
bpy.ops.export_scene.gltf(filepath=str((a.output/'illustrative-foot.glb').resolve()),export_format='GLB')
(a.output/'model.json').write_text(json.dumps({'status':'incomplete_reference_model','photo_pose_fit':fit_info,'reference':'Ecorche, BodyParts3D and Z-Anatomy; CC BY-SA 4.0','reference_sha256':hashlib.sha256(a.anatomy.read_bytes()).hexdigest(),'counts':counts,'fit':'side silhouette bounding rectangle only','assumed_depth':True,'missing_required_tissues':[], 'approximations':['arteries approximately fitted within reference foot bounds; anatomical registration unvalidated','fat pads are schematic, not measured or a complete fat layer'], 'vessel_sha256':hashlib.sha256(vessel_file.read_bytes()).hexdigest(),'personal_internal_measurement':False,'medical_use':False,'warning':'Illustration; bones and muscles are a generic reference, not the subject\'s measured anatomy.'},indent=2)+'\n')
