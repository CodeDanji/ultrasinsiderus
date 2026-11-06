#!/usr/bin/env python3
"""Stable entrypoint; resolve all bundled paths from this file, not the shell cwd."""
import argparse,os
from pathlib import Path
from preflight import check,HERE
from generate_anatomy import generate
p=argparse.ArgumentParser();p.add_argument('command',choices=['check','sample','process'])
p.add_argument('--image',type=Path);p.add_argument('--output',type=Path,default=HERE/'results/sample')
p.add_argument('--mask',type=Path);p.add_argument('--anchors',type=Path);p.add_argument('--blender',default='blender')
a=p.parse_args();errors=check(a.blender)
if errors:p.error('\n'.join(errors))
if a.command=='check':print('Ready: all runtime prerequisites and asset checksums verified.');raise SystemExit(0)
if a.command=='process' and not a.image:p.error('process requires --image')
os.environ['U2NET_HOME']=str(HERE/'assets/weights')
image=HERE/'references/synthetic-footbath.png' if a.command=='sample' else a.image
print(generate(image,HERE/'assets/ecorche.glb',a.output,blender=a.blender,mode='background',supplied_mask=a.mask,anchors=a.anchors))
