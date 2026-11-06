import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import app
class AppValidationTests(unittest.TestCase):
    def test_rejects_absent_consent(self):
        with self.assertRaises(ValueError): app.begin({'sample':True,'consent':False})
    def test_rejects_bad_encoded_image(self):
        with self.assertRaises(ValueError): app.begin({'consent':True,'image':'%%%invalid'})
    def test_session_id_is_confined(self):
        self.assertIsNone(app.session_path('../other'))
        self.assertIsNone(app.session_path('etc/passwd'))
if __name__=='__main__': unittest.main()
