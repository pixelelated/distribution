from pathlib import Path
import json,subprocess,time
from ui import out,remote
r=Path(__file__).parent;d=r/'dolphin-followup-results';d.mkdir();result={'rc':1,'started':time.time()}
try:
 source=json.loads((r/'records/dolphin-followup-source.json').read_text())
 remote('mkdir /tmp/pix581-followup-source',capture_output=True)
 with (r/'records/dolphin-followup.tar').open('rb') as f:remote('cat > /tmp/pix581-followup-source/packet.tar',stdin=f)
 assert out('sha256sum /tmp/pix581-followup-source/packet.tar').split()[0]==source['archive_sha256']
 remote('tar xf /tmp/pix581-followup-source/packet.tar -C /tmp/pix581-followup-source',capture_output=True)
 command='cd /tmp/pix581-followup-source && timeout 90 unshare -n -- python3 -I -S -B '+source['packet']+'/message_fixture.py --repo /tmp/pix581-followup-source --output /tmp/pix581-followup-messages'
 p=subprocess.run(json.loads((r/'ssh-command.json').read_text())+[command],capture_output=True,text=True,timeout=105)
 (d/'stdout').write_text(p.stdout);(d/'stderr').write_text(p.stderr);result['guest_rc']=p.returncode
 raw=out('cat /tmp/pix581-followup-messages/result.json');(d/'result.json').write_text(raw)
 raw=remote('tar cf - -C /tmp/pix581-followup-messages .',capture_output=True).stdout;(d/'receipts.tar').write_bytes(raw)
 assert p.returncode==0,p.stderr;data=json.loads((d/'result.json').read_text());assert data['status']=='PASS' and len(data['cases'])==51
 result['rc']=0
finally:
 result['ended']=time.time();(r/'dolphin-followup-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
