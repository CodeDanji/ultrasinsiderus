import sys, unittest
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from silhouette import segment, SegmentationError

class SegmentationTests(unittest.TestCase):
    def image(self):
        a=np.zeros((100,120,3),dtype=np.uint8); a[:]=[20,210,20]; a[25:80,30:95]=[190,110,90]; return a
    def test_mask_and_noise(self):
        a=self.image(); a[2,60]=[0,0,0]
        mask,box=segment(Image.fromarray(a)); self.assertEqual(box,[30,25,95,80]); self.assertEqual(mask.getpixel((60,2)),0)
    def test_bad_backdrop(self):
        a=self.image(); a[:10,:10]=[200,200,200]
        with self.assertRaises(SegmentationError): segment(Image.fromarray(a))
    def test_clipped_subject(self):
        a=self.image(); a[0:30,30:95]=[190,110,90]
        with self.assertRaises(SegmentationError): segment(Image.fromarray(a))
    def test_no_subject(self):
        a=self.image(); a[:]=[20,210,20]
        with self.assertRaises(SegmentationError): segment(Image.fromarray(a))
if __name__=='__main__': unittest.main()
