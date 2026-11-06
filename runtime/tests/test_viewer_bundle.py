import base64,re,tempfile,unittest
from pathlib import Path
from build_viewer import build,HERE
class ViewerBundleTests(unittest.TestCase):
    def test_embedded_glb_is_byte_identical(self):
        model=HERE/'assets/vessels.glb'
        with tempfile.TemporaryDirectory() as d:
            output=Path(d)/'viewer.html';build(model,output)
            html=output.read_text(encoding='utf8')
            encoded=re.search(r'id="model-data" type="application/octet-stream">([^<]+)</script>',html).group(1)
            self.assertEqual(base64.b64decode(encoded),model.read_bytes())
            self.assertNotIn('__VIEWER_SCRIPT__',html)
            with self.assertRaises(ValueError):build(model,output)
if __name__=='__main__':unittest.main()
