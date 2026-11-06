"""Build a self-contained HTML viewer from the exact supplied GLB; no model edits."""
import argparse,base64,struct
from pathlib import Path
HERE=Path(__file__).resolve().parent

def build(model,output):
    model,output=Path(model),Path(output)
    data=model.read_bytes()
    if len(data)<12 or struct.unpack('<4sII',data[:12])!=(b'glTF',2,len(data)):raise ValueError('Invalid GLB header')
    if output.exists():raise ValueError('Output already exists')
    template=(HERE/'viewer/template.html').read_text(encoding='utf8')
    script=(HERE/'viewer/bundle.js').read_text(encoding='utf8').replace('</script','<\\/script')
    html=template.replace('__MODEL_DATA__',base64.b64encode(data).decode()).replace('__VIEWER_SCRIPT__',script)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(html,encoding='utf8')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.model,a.output)
