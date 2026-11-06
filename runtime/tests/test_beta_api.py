import json, tempfile, threading, unittest, urllib.request, urllib.error
from pathlib import Path
from unittest.mock import patch
import app

class BetaApiTests(unittest.TestCase):
    def test_feedback_and_user_deletion(self):
        with tempfile.TemporaryDirectory() as root, patch.object(app,'DATA',Path(root)):
            sid='12345678-1234-1234-1234-123456789abc'; folder=Path(root)/sid; folder.mkdir()
            app.save_status(folder,{'status':'incomplete_review_required'})
            server=app.ThreadingHTTPServer(('127.0.0.1',0),app.Handler)
            worker=threading.Thread(target=server.serve_forever,daemon=True); worker.start()
            base=f'http://127.0.0.1:{server.server_port}/api/sessions/{sid}'
            def post(path,data):
                req=urllib.request.Request(base+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req) as r: return json.load(r)
            try:
                out=folder/'output/views';out.mkdir(parents=True);(out/'front.png').write_bytes(b'fixture')
                with self.assertRaises(urllib.error.HTTPError) as gate: urllib.request.urlopen(base+'/front.png')
                self.assertEqual(gate.exception.code,403)
                self.assertTrue(post('/review',{'approved':True})['saved'])
                with urllib.request.urlopen(base+'/front.png') as response: self.assertEqual(response.read(),b'fixture')
                with self.assertRaises(urllib.error.HTTPError) as err: post('/feedback',{'rating':0})
                self.assertEqual(err.exception.code,400)
                self.assertTrue(post('/feedback',{'rating':4,'comment':'clear'})['saved'])
                self.assertEqual(json.loads((folder/'feedback.json').read_text())['rating'],4)
                self.assertTrue(post('/delete',{})['deleted']); self.assertFalse(folder.exists())
            finally: server.shutdown(); server.server_close(); worker.join()
if __name__=='__main__': unittest.main()
