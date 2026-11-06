#!/usr/bin/env python3
"""Run a labelled, single-image, controlled-background experiment locally."""
import argparse, hashlib, json, shutil, subprocess, sys, time
from pathlib import Path
from silhouette import run as segment

HERE=Path(__file__).resolve().parent

def run(image, output, blender, width, height):
    image=Path(image).resolve(); output=Path(output).resolve()
    if not image.is_file(): raise ValueError('Input image not found')
    exe=shutil.which(blender)
    if not exe: raise ValueError('Blender executable not found')
    if output.exists(): raise ValueError('Output already exists')
    if width<64 or height<64: raise ValueError('Invalid dimensions')
    output.mkdir(parents=True)
    started=time.monotonic()
    record={'status':'processing','source_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'stages':[],
            'mode':'single_image_schematic','measured_internal_anatomy':False,
            'warnings':['Synthetic or controlled-background test only; no water validation.', 'Depth is assumed; no multi-view reconstruction.', 'No internal anatomy generated. No diagnosis.']}
    def save(): (output/'experiment.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    save()
    try:
        box=segment(image,output/'segmentation'); record['bbox_xyxy']=box; record['stages'].append('segmentation'); save()
        cmds=[('extrusion',[exe,'-b','-t','2','--python-exit-code','1','--python',str(HERE/'extrude_silhouette.py'),'--','--mask',str(output/'segmentation/mask.png'),'--output',str(output/'model')]),
              ('render',[exe,'-b','-t','2','--python-exit-code','1','--python',str(HERE/'render_reference.py'),'--','--model',str(output/'model/silhouette.glb'),'--output',str(output/'views'),'--width',str(width),'--height',str(height)])]
        for name,cmd in cmds:
            try:
                completed=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180)
            except subprocess.TimeoutExpired as e:
                raise RuntimeError(f'{name} timed out') from e
            (output/f'{name}.log').write_text(completed.stdout,encoding='utf-8')
            if completed.returncode: raise RuntimeError(f'{name} failed; inspect {name}.log')
            record['stages'].append(name); save()
        record['status']='manual_review_required'
    except Exception as e:
        record['status']='failed'; record['failure']=str(e); raise
    finally:
        record['elapsed_seconds']=round(time.monotonic()-started,3); save()
    return output

def main():
    p=argparse.ArgumentParser(description='Controlled-background schematic only; no anatomy.')
    p.add_argument('--image',required=True,type=Path); p.add_argument('--output',required=True,type=Path)
    p.add_argument('--blender',default='blender'); p.add_argument('--width',type=int,default=1600); p.add_argument('--height',type=int,default=1200)
    a=p.parse_args()
    try: print('Review required:',run(a.image,a.output,a.blender,a.width,a.height))
    except (ValueError,OSError,RuntimeError) as e: print(f'Experiment failed: {e}',file=sys.stderr); return 1
    return 0
if __name__=='__main__': sys.exit(main())
