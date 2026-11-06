#!/usr/bin/env python3
"""Local-only research prototype. Do not expose to a network or use for diagnosis."""
import shutil
import base64, binascii, io, json, os, threading, uuid, zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from generate_anatomy import generate

HERE=Path(__file__).resolve().parent
DATA=Path(os.environ.get('SPA_DATA_DIR',str(HERE/'local-sessions'))).resolve()
DATA.mkdir(parents=True,exist_ok=True)
LOCK=threading.Lock()
MAX_BODY=15*1024*1024
ALLOWED={**{name+'.png':'output/views/'+name+'.png' for name in ('bones','muscles','vessels','fat')},'diagnostic.png':'output/segmentation/diagnostic.png','input.png':'input.png','front.png':'output/views/front.png','side.png':'output/views/side.png','oblique.png':'output/views/oblique.png','model.zip':'output/model.zip','result.json':'output/result.json'}

def save_status(folder, data):
    tmp=folder/'status.tmp'; tmp.write_text(json.dumps(data,ensure_ascii=False),encoding='utf8'); tmp.replace(folder/'status.json')

def process(folder):
    try:
        save_status(folder,{'status':'processing'})
        generate(folder/'input.png', HERE/'assets/ecorche.glb',folder/'output',mode=json.loads((folder/'input-settings.json').read_text())['mode'])
        with zipfile.ZipFile(folder/'output/model.zip','x',compression=zipfile.ZIP_DEFLATED) as z:
            z.write(folder/'output/anatomy/illustrative-foot.glb','illustrative-foot.glb')
            z.write(HERE/'assets/ATTRIBUTION.md','ATTRIBUTION.md')
            z.write(HERE/'assets/VESSELS_ATTRIBUTION.md','VESSELS_ATTRIBUTION.md')
            z.writestr('README.txt','SIMULATION ONLY. Generic reference anatomy, not an ultrasound scan or medical device. Arteries are approximately aligned. Fat pads are schematic. See ATTRIBUTION.md for source credits. License: https://creativecommons.org/licenses/by-sa/4.0/ .\n')
        save_status(folder,{'status':'incomplete_review_required'})
    except Exception as e:
        save_status(folder,{'status':'failed','error':str(e)[:400]})
    finally: LOCK.release()

def begin(payload):
    if not isinstance(payload,dict) or payload.get('consent') is not True: raise ValueError('촬영 이미지 사용 동의를 확인해 주세요.')
    sample=payload.get('sample') is True
    if sample:
        source=(HERE/'references/synthetic-footbath.png').read_bytes()
    else:
        content=payload.get('image')
        if not isinstance(content,str) or len(content)>MAX_BODY: raise ValueError('이미지 파일을 확인해 주세요.')
        try: source=base64.b64decode(content,validate=True)
        except (binascii.Error,ValueError): raise ValueError('이미지 인코딩이 올바르지 않습니다.')
    if len(source)>10*1024*1024: raise ValueError('이미지는 10MB 이하여야 합니다.')
    try:
        with Image.open(io.BytesIO(source)) as im:
            if im.format not in ('JPEG','PNG') or im.width*im.height>20_000_000: raise ValueError('20MP 이하 JPEG 또는 PNG를 사용해 주세요.')
            im.verify()
        from PIL import ImageOps
        with Image.open(io.BytesIO(source)) as im:
            image=ImageOps.exif_transpose(im).convert('RGB')
    except (UnidentifiedImageError,OSError,Image.DecompressionBombError): raise ValueError('이미지를 읽을 수 없습니다.')
    if not LOCK.acquire(blocking=False): raise RuntimeError('다른 이미지가 처리 중입니다. 완료 후 다시 시도해 주세요.')
    folder=DATA/str(uuid.uuid4())
    try:
        folder.mkdir(mode=0o700)
        (folder/'input-settings.json').write_text(json.dumps({'mode':'background'}))
        image.save(folder/'input.png'); save_status(folder,{'status':'queued','sample':sample})
        threading.Thread(target=process,args=(folder,),daemon=True).start()
    except Exception:
        LOCK.release(); raise
    return folder.name

def session_path(value):
    try: return DATA/str(uuid.UUID(value))
    except (ValueError,AttributeError): return None

class Handler(BaseHTTPRequestHandler):
    def log_message(self,fmt,*args): pass
    def send_data(self,data,content_type,status=200):
        self.send_response(status); self.send_header('Content-Type',content_type); self.send_header('Content-Length',str(len(data))); self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff'); self.end_headers(); self.wfile.write(data)
    def json(self,body,status=200): self.send_data(json.dumps(body,ensure_ascii=False).encode(),'application/json; charset=utf-8',status)
    def do_GET(self):
        path=self.path.split('?',1)[0]
        if path=='/': return self.send_data((HERE/'web/index.html').read_bytes(),'text/html; charset=utf-8')
        parts=path.strip('/').split('/')
        if len(parts)>=3 and parts[:2]==['api','sessions']:
            folder=session_path(parts[2])
            if not folder or not (folder/'status.json').is_file(): return self.json({'error':'세션을 찾을 수 없습니다.'},404)
            if len(parts)==3:
                data=json.loads((folder/'status.json').read_text(encoding='utf8'))
                result=folder/'output/result.json'
                if result.exists(): data['result']=json.loads(result.read_text(encoding='utf8'))
                return self.json(data)
            if len(parts)==4 and parts[3] in ALLOWED:
                if parts[3] not in ('input.png','diagnostic.png','result.json') and not (folder/'review.json').is_file(): return self.json({'error':'먼저 발 외형 분리 결과를 확인해 주세요.'},403)
                f=folder/ALLOWED[parts[3]]
                if f.is_file():
                    kind='image/png' if f.suffix=='.png' else ('application/zip' if f.suffix=='.zip' else 'application/json')
                    return self.send_data(f.read_bytes(),kind)
        return self.json({'error':'찾을 수 없습니다.'},404)
    def do_POST(self):
        if self.headers.get('Content-Type','').split(';')[0].strip().lower() != 'application/json': return self.json({'error':'JSON 요청만 허용됩니다.'},415)
        origin=self.headers.get('Origin')
        if origin and origin not in ('http://127.0.0.1:8765','http://localhost:8765'): return self.json({'error':'허용되지 않은 요청입니다.'},403)
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length<=0 or length>MAX_BODY: raise ValueError('요청 크기가 올바르지 않습니다.')
            payload=json.loads(self.rfile.read(length))
            if not isinstance(payload,dict): raise ValueError('요청 형식이 올바르지 않습니다.')
            parts=self.path.strip('/').split('/')
            if len(parts)==4 and parts[:2]==['api','sessions'] and parts[3] in ('feedback','delete','review'):
                folder=session_path(parts[2])
                if not folder or not (folder/'status.json').is_file(): return self.json({'error':'세션이 없습니다.'},404)
                state=json.loads((folder/'status.json').read_text())
                if state['status'] in ('processing','queued'): return self.json({'error':'처리 완료 후 이용해 주세요.'},409)
                if parts[3]=='review':
                    if payload.get('approved') is not True: raise ValueError('발 외형이 맞는지 확인해 주세요.')
                    (folder/'review.json').write_text(json.dumps({'foreground_approved':True,'medical_accuracy_approved':False}))
                    return self.json({'saved':True})
                if parts[3]=='delete':
                    shutil.rmtree(folder); return self.json({'deleted':True})
                if type(payload.get('rating')) is not int or not 1<=payload['rating']<=5: raise ValueError('1~5점 평가를 선택해 주세요.')
                comment=payload.get('comment','')
                if not isinstance(comment,str) or len(comment)>1000: raise ValueError('의견은 1000자 이내로 작성해 주세요.')
                (folder/'feedback.json').write_text(json.dumps({'rating':payload['rating'],'comment':comment},ensure_ascii=False),encoding='utf8')
                return self.json({'saved':True})
            if self.path!='/api/sessions': return self.json({'error':'찾을 수 없습니다.'},404)
            session=begin(payload)
            return self.json({'id':session},202)
        except (ValueError,json.JSONDecodeError) as e: return self.json({'error':str(e)},400)
        except RuntimeError as e: return self.json({'error':str(e)},409)

if __name__=='__main__':
    for existing in DATA.iterdir():
        try:
            f=existing/'status.json'; state=json.loads(f.read_text(encoding='utf8'))
            if state.get('status') in ('queued','processing'): save_status(existing,{'status':'failed','error':'서버가 재시작되어 처리가 중단되었습니다.'})
        except (OSError,ValueError): pass
    print('로컬 연구용: http://127.0.0.1:8765',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
