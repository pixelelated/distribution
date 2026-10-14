from pathlib import Path
import json,subprocess,hashlib,time,shlex
from ui import out,remote
r=Path(__file__).parent;d=r/'dolphin-results';d.mkdir();result={'rc':1,'started':time.time(),'stages':[]}
try:
 source=json.loads((r/'records/dolphin-source.json').read_text())
 remote('mkdir /run/qa581-source /tmp/pix581-run; mount -t tmpfs -o size=256M,mode=700 tmpfs /tmp/pix581-run',capture_output=True)
 with (r/'records/dolphin-controls.tar').open('rb') as f:remote('cat > /run/qa581-source/packet.tar',stdin=f)
 assert out('sha256sum /run/qa581-source/packet.tar').split()[0]==source['archive_sha256']
 remote('tar xf /run/qa581-source/packet.tar -C /run/qa581-source',capture_output=True)
 for name,args,expected,status in [('baseline','--baseline-only',1,'EXPECTED_BASELINE_FAILURE'),('candidate','',0,'PASS')]:
  command='cd /run/qa581-source && timeout 180 unshare -n -- python3 -I -S -B '+source['packet']+'/fixture.py --repo /run/qa581-source --output /tmp/pix581-run/'+name+' '+args
  t=time.time();p=subprocess.run(json.loads((r/'ssh-command.json').read_text())+[command],capture_output=True,text=True,timeout=200)
  (d/(name+'.stdout')).write_text(p.stdout);(d/(name+'.stderr')).write_text(p.stderr)
  stage={'name':name,'rc':p.returncode,'expected_rc':expected,'seconds':time.time()-t};result['stages'].append(stage)
  raw=out('cat /tmp/pix581-run/'+name+'/result.json');(d/(name+'-result.json')).write_text(raw);data=json.loads(raw)
  stage['status']=data['status'];stage['case_count']=len(data['cases'])
  raw=remote("python3 - <<'P'\nfrom pathlib import Path\nimport tarfile,sys\nr=Path('/tmp/pix581-run/"+name+"')\nwith tarfile.open(fileobj=sys.stdout.buffer,mode='w|') as t:\n for p in r.rglob('*'):\n  if p.is_file() and not p.is_symlink() and p.suffix in ['.json','.log'] and p.stat().st_size<4*1024*1024:t.add(p,arcname=str(p.relative_to(r)),recursive=False)\nP",capture_output=True).stdout
  (d/(name+'-receipts.tar')).write_bytes(raw)
  assert p.returncode==expected,(name,p.returncode,p.stderr)
  assert data['status']==status,(name,data)
 result['rc']=0
finally:
 result['ended']=time.time();(r/'dolphin-controls-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
