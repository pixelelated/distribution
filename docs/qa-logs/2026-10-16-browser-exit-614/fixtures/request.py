import argparse,base64,json,time,zlib,shlex
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('kind',choices=['serial','python','monitor','frame']);p.add_argument('value',nargs='?',default='');p.add_argument('--timeout',type=int,default=30);a=p.parse_args();r=Path('/workspace/tmp/pix-m7-browser-exit-vm-20261016-01')
spec={'type':a.kind,'timeout':a.timeout}
if a.kind=='python':
 code=Path(a.value).read_bytes();packed=base64.b64encode(zlib.compress(code)).decode();spec['type']='serial';spec['command']='python3 -I -B -c '+shlex.quote('import base64,zlib;exec(compile(zlib.decompress(base64.b64decode('+repr(packed)+')),"<qa614>","exec"))')
elif a.kind!='frame':spec['command']=a.value
out=r/'requests'/(a.name+'.json');assert not out.exists();temp=out.with_suffix('.tmp');temp.write_text(json.dumps(spec)+'\n');temp.rename(out)
end=time.monotonic()+50
while time.monotonic()<end:
 res=r/'responses'/out.name
 if res.exists():print(res.read_text());break
 time.sleep(.3)
else:print('Request still pending: '+a.name)
