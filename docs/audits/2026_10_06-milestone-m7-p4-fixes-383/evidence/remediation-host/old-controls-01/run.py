from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
assert not (owner/'started').exists()
(owner/'started').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat())
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
seal=json.loads((owner/'seal.json').read_text());code=1
try:
 for name,digest in seal.items(): assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
 cases=['PL001-discovery-unrelated','PL002-atomic-join-SETTINGS_REMOTE','PL003-active-sibling-custom','PL004-binding-comments','PL005-reason-future','PL006-folder-My Games','PL008-reader-escaped']
 observations=[]
 for case in cases:
  output=owner/'proof'/case
  rc=subprocess.run([sys.executable,'-I',str(owner/'tree/tools/rasteratops-cloud-layout-test'),'--ref','7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2','--case',case,'--output',str(output),'--rclone','/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement14/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/bin/rclone']).returncode
  result=json.loads((output/'results.json').read_text())
  assert rc==1 and len(result)==1 and result[0]['status']=='FAIL', (case,rc,result)
  observations.append({'case':case,'expected_old_failure':True,'actual':result[0]})
  (owner/'proof/negative-controls.json').write_text(json.dumps(observations,indent=2)+'\n')
 for name,digest in seal.items(): assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
 code=0
finally:
 (owner/'inner.rc').write_text(str(code)+'\n');(owner/'outer.rc').write_text(str(code)+'\n')
sys.exit(code)
