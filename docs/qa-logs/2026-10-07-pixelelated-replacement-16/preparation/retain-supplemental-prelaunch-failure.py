from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,socket
owner=Path('/workspace/tmp/pixelelated-m7-p4-build16-supplemental-01')
result=json.loads((owner/'launcher-result.json').read_text())
assert result['runner_returncode']==2 and (owner/'tool-wrapper.rc').read_text().strip()=='2'
assert '--activity-dir must exist' in (owner/'console.log').read_text()
assert not (owner/'qa.start').exists() and not (owner/'run.path').exists()
assert not Path('/proc',str(result['pid'])).exists()
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try: first=p.read_bytes().split(b'\0')[0].decode()
 except (OSError,UnicodeError):continue
 assert not Path(first).name.startswith('qemu-system-'),str(p)
for port in [9040,10022,10023,5909,5910]:
 with socket.socket() as s:s.bind(('127.0.0.1',port))
seals=json.loads((owner/'seal.json').read_text())
for n,h in seals.items():assert hashlib.sha256((Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16')/n).read_bytes()).hexdigest()==h,n
receipt=dict(verified_utc=datetime.now(timezone.utc).isoformat(),result='FAILED_BEFORE_RUN',launcher_returncode=2,wrapper_returncode=2,launcher_absent=result['pid'],no_qa_start=True,no_watcher_run_path=True,no_qemu=True,unbound_ports=[9040,10022,10023,5909,5910],sealed_inputs=len(seals),scope='Prelaunch argument validation only. Inner and build channels do not exist; no product test ran.')
with (owner/'prelaunch-verification.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
dest=Path('docs/qa-logs/2026-10-07-pixelelated-replacement-16/p4-build16-supplemental-01');dest.mkdir()
for p in owner.iterdir():
 if p.is_file():shutil.copy2(p,dest/p.name)
print(json.dumps(receipt))
