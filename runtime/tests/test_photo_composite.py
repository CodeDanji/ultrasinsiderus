import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from photo_composite import compose

class PhotoCompositionTests(unittest.TestCase):
    def test_reference_never_changes_pixels_outside_photo_foreground(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);seg=root/'seg';layers=root/'layers';seg.mkdir();layers.mkdir()
            original=Image.new('RGB',(100,80),(120,160,180));original.save(root/'source.png')
            mask=Image.new('L',original.size);ImageDraw.Draw(mask).rectangle((30,20,70,65),fill=255);mask.save(seg/'mask.png')
            (seg/'segmentation.json').write_text(json.dumps({'processed_dimensions':[100,80],'bbox_xyxy':[30,20,71,66]}))
            for name in ('overview','bones','muscles','vessels','fat'):
                Image.new('RGBA',original.size,(250,80,50,255)).save(layers/(name+'.png'))
            record=compose(root/'source.png',seg,layers,root/'output')
            self.assertFalse(record['personal_internal_measurement'])
            for filename in record['outputs']:
                with Image.open(root/'output'/filename) as result:
                    self.assertEqual(result.getpixel((5,48+5)),original.getpixel((5,5)))
                    self.assertEqual(result.size,(100,184))
            with self.assertRaises(ValueError):compose(root/'source.png',seg,layers,root/'output')
if __name__=='__main__':unittest.main()
