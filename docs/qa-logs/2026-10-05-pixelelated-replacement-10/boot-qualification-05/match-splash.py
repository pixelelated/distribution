#!/usr/bin/env python3
"""Match actual guest boot crops to the approved C-renderer output.

RGB pixel agreement in the full foreground bounding rectangle includes black
LCD gaps. Threshold and rectangle are recorded; no mask or threshold tuning
from the guest. A replaced old-logo crop must fail this identical predicate.
No original frame or asset is modified.
"""
import argparse,hashlib,importlib.machinery,json,struct,zlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--frames',type=Path,required=True);p.add_argument('--reference',type=Path,required=True);p.add_argument('--old-logo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
reader=importlib.machinery.SourceFileLoader('frame_diff','tools/frame-diff').load_module()
THRESHOLD=0.995

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def bbox(im):
 w,h,rows=im;points=[(x,y) for y,row in enumerate(rows) for x in range(w) if row[x*3:x*3+3]!=b'\0\0\0']
 assert points
 return min(x for x,y in points),min(y for x,y in points),max(x for x,y in points)+1,max(y for x,y in points)+1

def score(im,ref,rect):
 if im[:2]!=ref[:2]:return 0.0
 x0,y0,x1,y1=rect;total=(x1-x0)*(y1-y0)
 equal=sum(im[2][y][3*x:3*x+3]==ref[2][y][3*x:3*x+3] for y in range(y0,y1) for x in range(x0,x1))
 return equal/total

def png(path,im):
 w,h,rows=im
 def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
 path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(b'\0'+bytes(r) for r in rows)))+chunk(b'IEND',b''))

ref=reader.read_png(a.reference);rect=bbox(ref);captures=json.loads((a.frames/'captures.json').read_text())
rows=[]
for row in captures['frames']:
 path=a.frames/row['file'];assert sha(path)==row['sha256'];rows.append({**row,'agreement':score(reader.read_png(path),ref,rect)})
assert rows
best=max(rows,key=lambda x:x['agreement']);actual=reader.read_png(a.frames/best['file']);a.output.mkdir(parents=True,exist_ok=True)
controls=[]
# Replace the complete approved logo rectangle with a nearest-neighbour sample
# of the retained upstream logo. This is an explicit injected test fixture.
w,h,pixels=actual;old=reader.read_png(a.old_logo);x0,y0,x1,y1=rect
if (w,h)==ref[:2]:
 injected=[bytearray(r) for r in pixels]
 for y in range(y0,y1):
  sy=(y-y0)*old[1]//(y1-y0)
  for x in range(x0,x1):
   sx=(x-x0)*old[0]//(x1-x0);injected[y][3*x:3*x+3]=old[2][sy][3*sx:3*sx+3]
 for name,im in [('old-logo',(w,h,injected)),('blank',(w,h,[bytes(w*3)]*h)),('wrong-resolution',(1,1,[b'\0\0\0']))]:
  value=score(im,ref,rect);controls.append({'name':name,'agreement':value,'rejected':value<THRESHOLD})
  png(a.output/(name+'.png'),im)
report={'reference':str(a.reference),'reference_sha256':sha(a.reference),'old_logo_sha256':sha(a.old_logo),'threshold':THRESHOLD,'rectangle_half_open':rect,'scored_pixels':(x1-x0)*(y1-y0),'frames':rows,'best':best,'controls':controls,'pass':best['agreement']>=THRESHOLD and len(controls)==3 and all(x['rejected'] for x in controls)}
(a.output/'result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['pass','threshold','rectangle_half_open','best','controls']}))
raise SystemExit(0 if report['pass'] else 1)
