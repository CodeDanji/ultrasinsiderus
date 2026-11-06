"""Compose explicitly illustrative anatomy in the same frame as the supplied photo.
No external photo processing service, personal internal anatomy or health metrics.
"""
import argparse,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageFilter,ImageDraw,ImageFont

def compose(source,segmentation,layers,output):
    source,segmentation,layers,output=map(Path,(source,segmentation,layers,output))
    if output.exists(): raise ValueError('Output exists')
    info=json.loads((segmentation/'segmentation.json').read_text());w,h=info['processed_dimensions'];box=info['bbox_xyxy']
    with Image.open(source) as f: image=ImageOps.exif_transpose(f).convert('RGB');image.thumbnail((1024,1024))
    mask=Image.open(segmentation/'mask.png').convert('L')
    if image.size!=(w,h) or mask.size!=(w,h):raise ValueError('Image coordinate frame mismatch')
    output.mkdir(parents=True)
    # All overlays are strictly inside the observed foreground, with a soft transition.
    inner=mask.filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(3))
    x0,y0,x1,y1=box
    yy,xx=np.mgrid[:h,:w]
    fade=np.clip((yy-y0)/max(1,(y1-y0)*.16),0,1)
    # Preserve the skin outline and end of the visible ankle, no exposed chopped ends.
    strength=np.asarray(inner,dtype=float)/255*fade
    strength=np.minimum(strength,np.asarray(mask)/255)
    mask_float=np.asarray(mask,dtype=float)/255
    inner_gold=np.asarray(mask.filter(ImageFilter.MinFilter(13)),dtype=float)/255
    titles={'overview':'내 사진과 함께 보는 내부 구조 예시','bones':'뼈 · 표준 해부학 참조','muscles':'근육 · 표준 해부학 참조','vessels':'혈관 · 표준 위치의 예시','fat':'지방패드 · 측정값이 아닌 예시 위치'}
    outputs=[]
    for layer in titles:
        raw=Image.open(layers/(layer+'.png')).convert('RGBA')
        if raw.size!=(w,h):raise ValueError('Layer camera dimensions mismatch')
        data=np.asarray(raw,dtype=float)/255
        occupied=np.nonzero(data[:,:,3]>.02)[0]
        model_fade=np.ones((h,w),dtype=float)
        if occupied.size and layer in ('overview','bones','muscles'):
            transition=max(12,int((y1-y0)*.10))
            model_fade=np.clip((yy-int(occupied.min()))/transition,0,1)
        base=np.asarray(image,dtype=float)/255
        # Gentle darker window provides depth while retaining photographic skin context.
        dark=base*(1-strength[:,:,None]*.24)
        if layer=='fat':
            # Fixed-width graphic border, never a photo-derived adipose measurement.
            rim=np.clip(mask_float-inner_gold,0,1)*fade
            # Soft illustrated pads beneath the heel/forefoot, blended into the
            # photographed skin. A faint boundary provides context, not thickness.
            pad=Image.fromarray(np.uint8(data[:,:,3]*255)).filter(ImageFilter.GaussianBlur(4))
            alpha=np.asarray(pad,dtype=float)/255*strength*.72+rim*.08
            alpha=np.clip(alpha,0,.8)
            rgb=base*(1-alpha[:,:,None])+np.array([.96,.72,.28])*alpha[:,:,None]
        else:
            alpha=data[:,:,3]*strength*model_fade*(.74 if layer in ('overview','bones','muscles') else .95)
            # Keep skin visible between separate structures and small vessels.
            if layer=='vessels':
                # Rendered highlights made fine arteries look like bright rods.
                # Preserve the actual reference paths but soften their photographic presentation.
                soft=Image.fromarray(np.uint8(alpha*255)).filter(ImageFilter.GaussianBlur(.8))
                alpha=np.asarray(soft,dtype=float)/255*strength*.75
                rgb=base*(1-alpha[:,:,None])+np.array([.64,.12,.16])*alpha[:,:,None]
            else:
                rgb=dark*(1-alpha[:,:,None])+data[:,:,:3]*alpha[:,:,None]
        result=Image.fromarray(np.uint8(np.clip(rgb*255,0,255)))
        # Export a consistent presentation card. Labels are outside the photograph.
        canvas=Image.new('RGB',(w,h+104),(244,248,246));canvas.paste(result,(0,48));draw=ImageDraw.Draw(canvas)
        font_path='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
        try: font=ImageFont.truetype(font_path,16);small=ImageFont.truetype(font_path,11)
        except OSError:font=small=ImageFont.load_default()
        draw.text((18,14),titles[layer],font=font,fill=(24,65,58));draw.text((18,h+59),'시뮬레이션 · 사진 외형에 맞춘 표준 모형이며, 개인의 실제 내부를 측정한 결과가 아닙니다.',font=small,fill=(64,88,80))
        draw.text((18,h+81),'BodyParts3D / Z-Anatomy / OrganUI  ·  CC BY-SA 4.0 & 2.1 JP  ·  See source credits',font=small,fill=(85,105,95))
        file=f'photo-{layer}.png';canvas.save(output/file);outputs.append(file)
    record={'status':'visual_review_required','outputs':outputs,'registered_image_size':[w,h],'personal_internal_measurement':False,'fat_representation':'standard illustrative heel and forefoot pads; not measured thickness or distribution','limitations':['one side photograph; no depth or water refraction reconstruction','reference structure fitting remains approximate','mask and anatomy must be reviewed before presenting to participants']}
    (output/'composition.json').write_text(json.dumps(record,indent=2)+'\n')
    return record
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--image',type=Path,required=True);p.add_argument('--segmentation',type=Path,required=True);p.add_argument('--layers',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();compose(a.image,a.segmentation,a.layers,a.output)
