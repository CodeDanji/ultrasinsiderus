"""Validate installed prerequisites and bundled asset hashes without downloading."""
import hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent

def check(blender='blender'):
    errors=[]
    if sys.version_info[:2]!=(3,12):errors.append('Use Python 3.12 (the tested Python version).')
    for name in ('PIL','numpy','rembg','onnxruntime','scipy','cv2'):
        if importlib.util.find_spec(name) is None:errors.append('Missing Python module: '+name)
    for asset in json.loads((HERE/'assets/manifest.json').read_text())['assets']:
        p=HERE/'assets'/asset['path']
        if not p.is_file():errors.append('Missing asset: '+asset['path']);continue
        h=hashlib.sha256()
        with p.open('rb') as f:
            for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
        if h.hexdigest()!=asset['sha256']:errors.append('Asset checksum mismatch: '+asset['path'])
    exe=shutil.which(blender)
    if not exe:errors.append('Blender not found. Install Blender 4.3.2 or pass --blender with its full path.')
    else:
        result=subprocess.run([exe,'--version'],capture_output=True,text=True,timeout=30)
        if result.returncode or not result.stdout.startswith('Blender 4.3.2'):errors.append('Expected Blender 4.3.2; found '+result.stdout.split('\n')[0])
    return errors

if __name__=='__main__':
    errors=check(sys.argv[1] if len(sys.argv)>1 else 'blender')
    print('\n'.join(errors) if errors else 'Ready: Python, Blender and all 3 bundled assets verified.')
    raise SystemExit(bool(errors))
