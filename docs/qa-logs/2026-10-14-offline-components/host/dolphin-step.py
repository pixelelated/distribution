from pathlib import Path
import subprocess,sys,json,time,re,struct,zlib,hashlib
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-dolphin-preservation-581');helper=repo/'docs/qa-logs/2026-10-13-dolphin-preservation-source/installed-flow/remaining-serial/host-serial.py';receipts=r/'dolphin03-frames'
def invoke(op,review=None):
 cmd=['python3','-I','-S','-B',str(helper),op,'--repo',str(repo),'--serial',str(r/'vm/serial.sock'),'--monitor',str(r/'vm/monitor.sock'),'--receipts',str(receipts)]
 if review:cmd+=['--review',review]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=25);assert p.returncode==0,(p.stdout,p.stderr)
 return p.stdout.strip()
old=json.loads(invoke('status'));op=sys.argv[1]
if op in ['advance','next']:invoke(op,sys.argv[2])
end=time.monotonic()+18
while True:
 state=json.loads(invoke('status'))
 if state['phase']=='failed':print(json.dumps(state));raise SystemExit(1)
 if (op=='capture' or state['token']!=old['token']) and state['phase'] in ['entry','error','returned','complete','done']:break
 if time.monotonic()>end:print(json.dumps(state));raise SystemExit(2)
 time.sleep(.3)
print(json.dumps(state),flush=True)
if state['phase'] in ['entry','error','returned']:
 p=Path(invoke('capture'));b=p.read_bytes();m=re.match(rb'P6\s+(\d+)\s+(\d+)\s+255\s',b);assert m;w,h=map(int,m.groups());rgb=b[m.end():];assert len(rgb)==w*h*3
 def chunk(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
 raw=b''.join(b'\0'+rgb[y*w*3:(y+1)*w*3] for y in range(h));compressed=zlib.compress(raw);assert zlib.decompress(compressed)==raw
 out=p.with_suffix('.png');out.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+chunk(b'IDAT',compressed)+chunk(b'IEND',b''))
 out.with_suffix('.conversion.json').write_text(json.dumps({'source_ppm_sha256':hashlib.sha256(b).hexdigest(),'png_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'pixel_change':False,'size':[w,h]},indent=2)+'\n');print('FRAME='+str(out),flush=True)
