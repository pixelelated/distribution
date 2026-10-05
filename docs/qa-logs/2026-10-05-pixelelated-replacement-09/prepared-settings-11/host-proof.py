"""Copy test instrumentation only to owned VM; capture result even on failure."""
from pathlib import Path
import subprocess,json,hashlib
owner=Path(__file__).resolve().parent
base='/tmp/pixelelated-settings-race'
ssh=['ssh','-i',str(owner/'pair/qa-key'),'-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
def guest(cmd,**kwargs):return subprocess.run(ssh+[cmd],check=True,**kwargs)
guest('test ! -e '+base+' && mkdir -m 700 '+base)
for name in ['pause-unlock.so','guest-proof.py','expected.json','settings-modes-test']:
 guest('cat > '+base+'/'+name,input=(owner/name).read_bytes())
result=subprocess.run(ssh+['python3 '+base+'/guest-proof.py'],capture_output=True,text=True,timeout=240)
(owner/'artifacts/guest.log').write_text(result.stdout+result.stderr)
print(result.stdout,flush=True)
readback=subprocess.run(ssh+['cat '+base+'/result.json'],capture_output=True,text=True)
if readback.returncode==0:
 (owner/'artifacts/result.json').write_text(readback.stdout)
else:
 (owner/'artifacts/missing-result.json').write_text(json.dumps({'rc':readback.returncode}))
diag=subprocess.run(ssh+['cat '+base+'/diagnostics.json'],capture_output=True,text=True)
if diag.returncode==0:
 (owner/'artifacts/diagnostics.json').write_text(diag.stdout)
 print(diag.stdout,flush=True)
assert result.returncode==0, 'guest proof failed; original guest.log retained' 
report=json.loads(readback.stdout)
assert report['pass'] and report['checks'],report
print('PASS real installed ES settings-race checks:',len(report['checks']),flush=True)

mode_result=subprocess.run(ssh+['python3 '+base+'/settings-modes-test --profile /etc/profile.d/001-functions --chksysconfig /usr/bin/chksysconfig --busybox /usr/bin/busybox --output '+base+'/modes.json'],capture_output=True,text=True,timeout=180)
(owner/'artifacts/modes.log').write_text(mode_result.stdout+mode_result.stderr)
print(mode_result.stdout,flush=True)
mode_readback=subprocess.run(ssh+['cat '+base+'/modes.json'],capture_output=True,text=True)
if mode_readback.returncode==0:(owner/'artifacts/modes.json').write_text(mode_readback.stdout)
assert mode_result.returncode==0 and mode_readback.returncode==0, 'installed mode checks failed; original log retained'
mode_report=json.loads(mode_readback.stdout)
assert mode_report['pass'] and len(mode_report['checks'])==29
print('PASS 29 installed settings mode/refusal checks',flush=True)
