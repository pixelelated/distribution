from pathlib import Path
import json,subprocess,hashlib,time,tarfile,io
from ui import out,remote
r=Path(__file__).parent;result={'rc':1,'started':time.time()};d=r/'rvz-results';d.mkdir()
try:
 remote('mkdir -p /storage/qa574',capture_output=True)
 with (r/'records/rvz-controls.tar').open('rb') as f:remote('cat > /storage/qa574/controls.tar',stdin=f)
 assert out('sha256sum /storage/qa574/controls.tar').split()[0]==hashlib.sha256((r/'records/rvz-controls.tar').read_bytes()).hexdigest()
 remote('tar xf /storage/qa574/controls.tar -C /storage/qa574',capture_output=True)
 with (r/'rvz-guest.py').open('rb') as f:remote('cat > /storage/qa574/run.py',stdin=f)
 p=subprocess.run(json.loads((r/'ssh-command.json').read_text())+['timeout 180 python3 /storage/qa574/run.py'],capture_output=True,text=True,timeout=195);(d/'outer.stdout').write_text(p.stdout);(d/'outer.stderr').write_text(p.stderr);result['guest_rc']=p.returncode
 files=out('find /storage/qa574/results -maxdepth 1 -type f').splitlines()
 for f in files:
  assert Path(f).parent==Path('/storage/qa574/results')
  with (d/Path(f).name).open('wb') as h:remote('cat '+f,stdout=h)
 assert p.returncode==0,p.stderr
 assert json.loads((d/'result.json').read_text())['rc']==0
 result['rc']=0
finally:
 result['ended']=time.time();(r/'rvz-controls-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
