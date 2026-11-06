import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from silhouette import run,SegmentationError
class SuppliedMaskTests(unittest.TestCase):
    def test_operator_selected_mask_keeps_pale_interior(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);Image.new('RGB',(100,80),(230,230,235)).save(root/'photo.png')
            mask=Image.new('L',(100,80));ImageDraw.Draw(mask).rectangle((20,5,80,65),fill=255);mask.save(root/'mask.png')
            box=run(root/'photo.png',root/'result',mode='background',supplied_mask=root/'mask.png')
            self.assertEqual(box,(20,5,81,66))
            self.assertEqual(Image.open(root/'result/mask.png').getpixel((50,35)),255)
            record=json.loads((root/'result/segmentation.json').read_text());self.assertEqual(record['method'],'u2netp_mask_operator_selected')
    def test_mismatched_mask_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);Image.new('RGB',(100,80)).save(root/'photo.png');Image.new('L',(10,10),255).save(root/'mask.png')
            with self.assertRaises(SegmentationError):run(root/'photo.png',root/'result',supplied_mask=root/'mask.png')
if __name__=='__main__':unittest.main()
