import hashlib,json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import preflight
class PreflightTests(unittest.TestCase):
    def test_asset_integrity_and_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'assets').mkdir();asset=root/'assets/a.bin';asset.write_bytes(b'valid')
            (root/'assets/manifest.json').write_text(json.dumps({'assets':[{'path':'a.bin','sha256':hashlib.sha256(b'valid').hexdigest()}]}))
            with patch.object(preflight,'HERE',root),patch('preflight.importlib.util.find_spec',return_value=object()),patch('preflight.shutil.which',return_value='/bin/mock'),patch('preflight.subprocess.run',return_value=SimpleNamespace(returncode=0,stdout='Blender 4.3.2\n')):
                self.assertEqual(preflight.check(),[])
                asset.write_bytes(b'changed');self.assertIn('Asset checksum mismatch: a.bin',preflight.check())
                asset.unlink();self.assertIn('Missing asset: a.bin',preflight.check())
if __name__=='__main__':unittest.main()
