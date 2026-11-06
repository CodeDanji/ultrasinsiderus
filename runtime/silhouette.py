#!/usr/bin/env python3
"""Controlled-background silhouette experiment, not a general segmentation model."""
import argparse
import json
import math
import sys
from collections import deque
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps, ImageDraw

VERSION='0.1.0'
class SegmentationError(ValueError): pass

def segment(image, min_green=70, green_margin=28, min_fraction=0.015):
    """Extract one largest connected subject component from a green-screen image."""
    rgb=np.asarray(image.convert('RGB'), dtype=np.int16)
    r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    bg=(g>=min_green)&(g>=r+green_margin)&(g>=b+green_margin)
    # Require all corners to belong to the declared backdrop; no unreliable fallback.
    patch=max(1,min(rgb.shape[:2])//30)
    corners=[bg[:patch,:patch],bg[:patch,-patch:],bg[-patch:,:patch],bg[-patch:,-patch:]]
    if any(c.mean()<0.85 for c in corners):
        raise SegmentationError('Background is not uniformly green at image corners')
    candidate=~bg; height,width=candidate.shape
    visited=np.zeros(candidate.shape,dtype=bool); largest=[]
    for y,x in zip(*np.nonzero(candidate)):
        if visited[y,x]: continue
        q=deque([(int(y),int(x))]); visited[y,x]=True; component=[]
        while q:
            cy,cx=q.popleft(); component.append((cy,cx))
            for ny,nx in ((cy-1,cx),(cy+1,cx),(cy,cx-1),(cy,cx+1)):
                if 0<=ny<height and 0<=nx<width and candidate[ny,nx] and not visited[ny,nx]:
                    visited[ny,nx]=True; q.append((ny,nx))
        if len(component)>len(largest): largest=component
    if len(largest)<width*height*min_fraction:
        raise SegmentationError('Subject too small or absent')
    mask=np.zeros(candidate.shape,dtype=np.uint8)
    ys,xs=zip(*largest); mask[ys,xs]=255
    x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
    if x0<=1 or y0<=1 or x1>=width-2 or y1>=height-2:
        raise SegmentationError('Subject touches image border; retake or use complete reference')
    return Image.fromarray(mask,mode='L'), [x0,y0,x1+1,y1+1]

def run(source, output, mode="green", supplied_mask=None):
    source,output=Path(source),Path(output)
    if output.exists(): raise SegmentationError('Output directory already exists')
    with Image.open(source) as f:
        image=ImageOps.exif_transpose(f).convert('RGB')
    # A bounded processing resolution limits memory and queue time. No detail invented.
    image.thumbnail((1024,1024))
    if supplied_mask is not None:
        with Image.open(supplied_mask) as f: mask=f.convert('L')
        if mask.size!=image.size: raise SegmentationError('Supplied mask must match processed image size')
        mask=mask.point(lambda p:255 if p>=150 else 0)
        box=mask.getbbox()
        if not box: raise SegmentationError('Supplied mask is empty')
        mode='u2netp_mask_operator_selected'
    elif mode == 'green':
        mask,box=segment(image)
    elif mode == 'background':
        import os
        os.environ.setdefault('U2NET_HOME', str(Path(__file__).resolve().parent/'assets/weights'))
        try:
            from rembg import remove, new_session
        except ImportError as e:
            raise SegmentationError('Background model dependencies are missing; install requirements.txt') from e
        mask=remove(image, session=new_session('u2netp'), only_mask=True).convert('L')
        mask=mask.point(lambda p:255 if p>=150 else 0)
        # The background model can retain transparent bath edges. Restrict to the
        # largest warm skin-colour component. Experimental; skin tones/lighting
        # outside these bounds may require retaking, not a plausible fallback.
        from scipy import ndimage
        rgb=np.asarray(image,dtype=np.int16); r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
        warm=(r>g*1.035)&(r-b>12)&(g>=b*.95)
        foreground=(np.asarray(mask)>0)&warm
        foreground=ndimage.binary_opening(foreground,iterations=2)
        foreground=ndimage.binary_closing(foreground,iterations=2)
        labels,count=ndimage.label(foreground)
        if count==0: raise SegmentationError('No isolated foot region; improve lighting or background')
        sizes=np.bincount(labels.ravel()); sizes[0]=0
        foreground=ndimage.binary_fill_holes(labels==sizes.argmax())
        mask=Image.fromarray((foreground*255).astype(np.uint8))
        box=mask.getbbox()
        if not box or (box[2]-box[0])*(box[3]-box[1]) < image.width*image.height*.015:
            raise SegmentationError('No reliable foreground found; retake the photo')
        if box[0]<=1 or box[2]>=image.width-1 or box[3]>=image.height-1:
            raise SegmentationError('Foot touches a side or bottom border; retake with the full foot visible')
        # Upper ankle may naturally continue into a leg outside the photo.
        if box[1]<=1 and np.count_nonzero(np.asarray(mask)[0]) > image.width*.55:
            raise SegmentationError('Upper foreground is too broad to identify a side foot reliably')
    else:
        raise SegmentationError('Unsupported segmentation mode')
    output.mkdir(parents=True)
    rgba=image.convert('RGBA'); rgba.putalpha(mask); rgba.save(output/'foreground.png')
    mask.save(output/'mask.png')
    diagnostic=Image.composite(image, Image.blend(image,Image.new('RGB',image.size,(20,20,20)),.75),mask); ImageDraw.Draw(diagnostic).rectangle(box,outline='red',width=3)
    diagnostic.save(output/'diagnostic.png')
    (output/'segmentation.json').write_text(json.dumps({'status':'manual_review_required','method':mode,'version':'0.2.0','bbox_xyxy':box,'processed_dimensions':list(image.size),'source_file':source.name,'personalized_anatomy':False,'limitations':['Refraction, occlusion and strong reflections remain uncorrected','Silhouette does not measure internal anatomy','Manual check for missing toes, holes and background leakage required']},indent=2)+'\n')
    return box

def main():
    p=argparse.ArgumentParser(); p.add_argument('--image',type=Path,required=True); p.add_argument('--output',type=Path,required=True); a=p.parse_args()
    try: print('Review required; bbox:',run(a.image,a.output))
    except (OSError,ValueError) as e: print(f'Segmentation failed: {e}',file=sys.stderr); return 1
    return 0
if __name__=='__main__': sys.exit(main())
