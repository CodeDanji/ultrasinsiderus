#!/usr/bin/env python3
"""Generate an explicitly incomplete, non-diagnostic reference anatomy prototype."""
import argparse, hashlib, json, shutil, subprocess, sys, time
from pathlib import Path
from PIL import Image, ImageDraw
from silhouette import run as segment
from photo_composite import compose
HERE=Path(__file__).resolve().parent

def generate(image, anatomy, output, blender='blender', width=1600, height=1200, mode="green", reference_views=False, supplied_mask=None, anchors=None):
    image,anatomy,output=Path(image).resolve(),Path(anatomy).resolve(),Path(output).resolve()
    exe=shutil.which(blender)
    if not image.is_file() or not anatomy.is_file() or not exe: raise ValueError('Missing image, anatomy GLB, or Blender')
    if output.exists(): raise ValueError('Output already exists')
    if width<64 or height<64: raise ValueError('Invalid dimensions')
    output.mkdir(parents=True); start=time.monotonic()
    record={'status':'processing','stages':[],'input_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),
      'reference_sha256':hashlib.sha256(anatomy.read_bytes()).hexdigest(), 'personal_internal_measurement':False, 'quality_approved':False, 'beta_validation':'pending_real_photos_and_participant_review',
      'missing_required_tissues':[], 'approximations':['Arteries approximately registered','Photo and 3D fat pads are generic illustrations, not measurements'], 'warnings':['Illustration only. Generic anatomy; no medical use.', 'Background removal is experimental; water refraction and multi-camera calibration are unvalidated.', 'Fit uses bounding box only; depth and pose are assumed.']}
    def save(): (output/'result.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    def stage(name, script, args):
        cmd=[exe,'-b','-t','2','--python-exit-code','1','--python',str(HERE/script),'--']+list(map(str,args))
        result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=900)
        (output/f'{name}.log').write_text(result.stdout,encoding='utf-8')
        if result.returncode: raise RuntimeError(f'{name} failed; see log')
        record['stages'].append(name); save()
    save()
    try:
        segment(image,output/'segmentation',mode=mode,supplied_mask=supplied_mask); record['stages'].append('segmentation'); save()
        stage('extrusion','extrude_silhouette.py',['--mask',output/'segmentation/mask.png','--output',output/'outline'])
        stage('anatomy','build_anatomy.py',['--anatomy',anatomy,'--mask-info',output/'segmentation/segmentation.json','--silhouette',output/'outline/silhouette.glb','--output',output/'anatomy']+(['--anchors',anchors] if anchors else []))
        stage('photo_layers','render_photo_layers.py',['--model',output/'anatomy/illustrative-foot.glb','--info',output/'segmentation/segmentation.json','--output',output/'photo-layers'])
        composition=compose(image,output/'segmentation',output/'photo-layers',output/'composed')
        (output/'views').mkdir()
        for layer,name in [('overview','front'),('bones','bones'),('muscles','muscles'),('vessels','vessels'),('fat','fat')]:
            shutil.copyfile(output/'composed'/f'photo-{layer}.png',output/'views'/f'{name}.png')
        record['composition']=composition
        record['stages'].append('photo_composition'); save()
        if reference_views:
            stage('reference_render','render_reference.py',['--model',output/'anatomy/illustrative-foot.glb','--output',output/'reference-views','--width',width,'--height',height,'--layers'])
        record['status']='incomplete_review_required'
        record['outputs']=['views/front.png','anatomy/illustrative-foot.glb']+[f'views/{name}.png' for name in ('bones','muscles','vessels','fat')]
    except Exception as e:
        record['status']='failed'; record['failure']=str(e); raise
    finally:
        record['elapsed_seconds']=round(time.monotonic()-start,3); save()
    return output

def main():
    p=argparse.ArgumentParser(); p.add_argument('--image',required=True,type=Path); p.add_argument('--anatomy',type=Path,default=HERE/'assets/ecorche.glb'); p.add_argument('--output',required=True,type=Path); p.add_argument('--blender',default='blender'); p.add_argument('--mask',type=Path); p.add_argument('--anchors',type=Path); p.add_argument('--reference-views',action='store_true'); p.add_argument('--mode',choices=['green','background'],default='green')
    a=p.parse_args()
    try: print('Incomplete illustrative result:',generate(a.image,a.anatomy,a.output,a.blender,mode=a.mode,reference_views=a.reference_views,supplied_mask=a.mask,anchors=a.anchors))
    except (ValueError,OSError,RuntimeError,subprocess.TimeoutExpired) as e: print(f'Generation failed: {e}',file=sys.stderr); return 1
    return 0
if __name__=='__main__': sys.exit(main())
