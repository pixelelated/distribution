from pathlib import Path
import argparse,json,subprocess,sys,struct,zlib,hashlib
p=argparse.ArgumentParser();p.add_argument('owner',type=Path);p.add_argument('operation');p.add_argument('--review');a=p.parse_args()
repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');fixture=repo/'docs/qa-logs/2026-10-14-dolphin-english640-source/host-serial.py'
cmd=['python3','-I','-S','-B',str(fixture),a.operation,'--repo','/workspace/repos/rocknix.worktrees/m7-dolphin-preservation-581','--serial',str(a.owner/'vm/serial.sock'),'--monitor',str(a.owner/'vm/monitor.sock'),'--receipts',str(a.owner/'frames')]
if a.review:cmd+=['--review',a.review]
r=subprocess.run(cmd,capture_output=True,text=True,timeout=45);sys.stderr.write(r.stderr)
if r.returncode:sys.stdout.write(r.stdout);raise SystemExit(r.returncode)
if a.operation!='capture':print(r.stdout,end='');raise SystemExit(0)
s=Path(r.stdout.strip());assert s.is_relative_to(a.owner/'frames') and s.suffix=='.ppm'
with s.open('rb') as f:
 assert f.readline().strip()==b'P6';w,h=map(int,f.readline().split());assert f.readline().strip()==b'255';raw=f.read()
assert (w,h)==(640,480) and len(raw)==w*h*3
chunk=lambda t,b:struct.pack('!I',len(b))+t+b+struct.pack('!I',zlib.crc32(t+b)&0xffffffff)
scan=b''.join(b'\0'+raw[i:i+w*3] for i in range(0,len(raw),w*3));encoded=zlib.compress(scan);assert zlib.decompress(encoded)==scan
out=s.with_suffix('.png');out.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!IIBBBBB',w,h,8,2,0,0,0))+chunk(b'IDAT',encoded)+chunk(b'IEND',b''))
out.with_suffix('.conversion.json').write_text(json.dumps({'ppm':str(s),'ppm_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'png_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'pixels_sha256':hashlib.sha256(raw).hexdigest(),'size':[w,h],'lossless_scanlines_checked':True},indent=2)+'\n')
print(str(out))
