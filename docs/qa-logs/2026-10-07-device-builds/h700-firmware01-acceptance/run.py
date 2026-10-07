from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys,time
owner=Path(__file__).resolve().parent
build_owner=Path('/workspace/tmp/pixelelated-m7-h700-firmware-01')
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for path,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha,path
 run=Path((build_owner/'run.path').read_text().strip())
 pids=[json.loads((build_owner/'launcher-pid.json').read_text())['pid']]+[int((run/n).read_text()) for n in ['build.pid','watcher.pid','command.pid']]
 while not (build_owner/'launcher-result.json').exists() or any(Path('/proc',str(pid)).exists() for pid in pids):
  print(datetime.now(timezone.utc).isoformat()+' waiting for H700 firmware owner completion/process exit',flush=True);time.sleep(30)
 if not (build_owner/'owner-verification.json').exists():subprocess.run(['python3','-I',str(owner/'verify-owner.py'),str(build_owner)],check=True)
 verified=json.loads((build_owner/'owner-verification.json').read_text())
 actual=json.loads((build_owner/'runtime-start.json').read_text())
 current=subprocess.check_output(['docker','ps','-aq','--no-trunc'],text=True).split()
 for row in actual['containers']:assert row['id'] not in current and not Path('/proc',str(row['host_pid'])).exists(),row['id']
 if verified['result']!='PASS':
  (owner/'artifacts/acceptance.json').write_text(json.dumps({'result':'BUILD_FAILED','owner_verified':verified,'container_exited':True,'utc':datetime.now(timezone.utc).isoformat()},indent=2)+'\n')
  raise RuntimeError('H700 firmware failed; original owner retained; no acceptance or next-device start')
 subprocess.run(['python3','-I',str(owner/'verify-firmware.py')],check=True)
 rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
