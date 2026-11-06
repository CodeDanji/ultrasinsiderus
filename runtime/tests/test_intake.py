import json
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from spa_capture import intake, IntakeError, digest

class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.profile = {'profile_id':'p','version':'1','camera_ids':['a','b','c','d'], 'water_condition':'level', 'window_condition':'glass', 'calibration_reference':'v1'}
        self.manifest = {'session_id':'s1','profile_id':'p','profile_version':'1','consent_recorded':True,'water_present':True,'side':'left','body_part':'foot', 'captures':[]}
        for i, camera in enumerate(self.profile['camera_ids']):
            Image.new('RGB', (30, 20), (i*60, 0, 0)).save(self.root / f'{camera}.png')
            self.manifest['captures'].append({'camera_id':camera,'session_id':'s1','side':'left','body_part':'foot','captured_at':'2026-11-03T12:00:00+09:00','file':f'{camera}.png'})
        self.write()
    def tearDown(self): self.tmp.cleanup()
    def write(self):
        (self.root/'m.json').write_text(json.dumps(self.manifest))
        (self.root/'p.json').write_text(json.dumps(self.profile))
    def run_intake(self): return intake(self.root/'m.json', self.root/'p.json', self.root/'out')
    def test_success_and_no_overwrite(self):
        out = self.run_intake()
        result = json.loads((out/'result.json').read_text())
        self.assertEqual(result['status'], 'input_review_required')
        self.assertEqual(len(result['captures']), 4)
        self.assertEqual(digest(out/'originals/a.png'), digest(self.root/'a.png'))
        self.assertTrue((out/'contact-sheet.jpg').is_file())
        with self.assertRaises(IntakeError): self.run_intake()
    def test_rejects_mismatched_capture(self):
        self.manifest['captures'][0]['session_id'] = 'other'; self.write()
        with self.assertRaises(IntakeError): self.run_intake()
        self.assertFalse((self.root/'out/s1').exists())
    def test_rejects_no_consent_or_water(self):
        for key in ('consent_recorded', 'water_present'):
            self.manifest[key] = False; self.write()
            with self.assertRaises(IntakeError): self.run_intake()
            self.manifest[key] = True
    def test_rejects_duplicate_and_missing_camera(self):
        self.manifest['captures'][1]['file'] = 'a.png'; self.write()
        with self.assertRaises(IntakeError): self.run_intake()
        self.manifest['captures'][1]['file'] = 'b.png'
        self.manifest['captures'].pop(); self.write()
        with self.assertRaises(IntakeError): self.run_intake()
    def test_rejects_profile_version_and_unsafe_id(self):
        self.manifest['profile_version'] = 'wrong'; self.write()
        with self.assertRaises(IntakeError): self.run_intake()
        self.manifest['profile_version'] = '1'; self.manifest['session_id'] = '../oops'; self.write()
        with self.assertRaises(IntakeError): self.run_intake()

if __name__ == '__main__': unittest.main()
