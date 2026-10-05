#!/usr/bin/env python3
"""Capture actual guest boot frames; a separate matcher assigns the verdict."""
import argparse,hashlib,importlib.machinery,json,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--monitor',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--seconds',type=float,default=40);a=p.parse_args()
assert not a.output.exists();a.output.mkdir(parents=True)
visual=importlib.machinery.SourceFileLoader('vm_visual','tools/vm-visual-qa').load_module()
mon=visual.Monitor(a.monitor);frames=[];start=time.monotonic()
try:
 while time.monotonic()-start<a.seconds:
  frame=a.output/f'{len(frames):03d}.ppm'
  if not mon.screendump(str(frame.resolve()),settle=.1):raise RuntimeError('guest frame capture failed')
  png=frame.with_suffix('.png');assert visual._ppm_to_png_stdlib(str(frame),str(png));frame.unlink()
  frames.append({'file':png.name,'elapsed_seconds':round(time.monotonic()-start,3),'sha256':hashlib.sha256(png.read_bytes()).hexdigest()})
  if len(frames)%10==0:print('CAPTURED guest boot frames',len(frames),flush=True)
  time.sleep(.1)
finally:mon.close()
assert frames
(a.output/'captures.json').write_text(json.dumps({'scope':'actual QEMU scanout, unmodified guest boot','frames':frames},indent=2)+'\n')
print('PASS boot frame capture only; branding classification remains required',len(frames),flush=True)
