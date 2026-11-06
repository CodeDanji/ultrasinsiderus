import json, sys, tempfile, unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from run_experiment import run

class ExperimentTests(unittest.TestCase):
    def test_failure_record_for_bad_background(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); source=root/'input.png'; Image.new('RGB',(100,100),'white').save(source)
            with self.assertRaises(ValueError): run(source,root/'output','python',100,100)
            result=json.loads((root/'output/experiment.json').read_text())
            self.assertEqual(result['status'],'failed')
            self.assertFalse(result['measured_internal_anatomy'])
    def test_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); source=root/'input.png'; Image.new('RGB',(20,20),'green').save(source)
            out=root/'output'; out.mkdir(); (out/'keep').write_text('safe')
            with self.assertRaises(ValueError): run(source,out,'python',100,100)
            self.assertEqual((out/'keep').read_text(),'safe')
if __name__=='__main__': unittest.main()
