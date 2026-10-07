from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,subprocess,sys,time
owner=Path(__file__).resolve().parent
prior=Path('/workspace/tmp/pixelelated-m7-h700-firmware-acceptance-01')
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for p,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
 run=Path((prior/'run.path').read_text().strip())
 pids=[json.loads((prior/'launcher-pid.json').read_text())['pid']]+[int((run/n).read_text()) for n in ['build.pid','watcher.pid','command.pid']]
 while not (prior/'launcher-result.json').exists() or any(Path('/proc',str(pid)).exists() for pid in pids):
  print(datetime.now(timezone.utc).isoformat()+' waiting for accepted H700 firmware and actual verifier exits',flush=True);time.sleep(30)
 if not (prior/'owner-verification.json').exists():subprocess.run(['python3','-I',str(owner/'verify-owner.py'),str(prior)],check=True)
 assert json.loads((prior/'owner-verification.json').read_text())['result']=='PASS'
 assert json.loads((prior/'artifacts/acceptance.json').read_text())['result']=='PASS'
 (owner/'artifacts/result.json').write_text(json.dumps({'result':'PASS','accepted_owner':str(prior),'acceptance_sha256':hashlib.sha256((prior/'artifacts/acceptance.json').read_bytes()).hexdigest()},indent=2)+'\n')
 print('PASS H700 firmware artifact acceptance; SM8550 preparation may follow',flush=True)
 rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
