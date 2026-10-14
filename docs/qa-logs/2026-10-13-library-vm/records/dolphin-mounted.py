from pathlib import Path
import json,subprocess,time
from ui import out,remote
r=Path(__file__).parent;d=r/'dolphin-mounted-results';d.mkdir();result={'rc':1,'started':time.time()}
try:
 with (r/'dolphin-mounted-guest.py').open('rb') as f:remote('cat > /run/qa581-source/mounted.py',stdin=f)
 p=subprocess.run(json.loads((r/'ssh-command.json').read_text())+['timeout 150 unshare -m -n -- python3 -I -S -B /run/qa581-source/mounted.py'],capture_output=True,text=True,timeout=170)
 (d/'stdout').write_text(p.stdout);(d/'stderr').write_text(p.stderr);result['guest_rc']=p.returncode
 raw=out('cat /storage/qa581-mounted/result.json');(d/'result.json').write_text(raw)
 raw=remote('tar cf - -C /storage/qa581-mounted .',capture_output=True).stdout;(d/'receipts.tar').write_bytes(raw)
 assert p.returncode==0,p.stderr;assert json.loads((d/'result.json').read_text())['rc']==0
 result['rc']=0
finally:
 result['ended']=time.time();(r/'dolphin-mounted-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
