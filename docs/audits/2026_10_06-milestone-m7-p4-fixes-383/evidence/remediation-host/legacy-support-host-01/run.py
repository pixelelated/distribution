from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent;snap=owner/'snapshot';tree=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
assert Path.cwd()==tree
(owner/'run.path').write_text(str(tree/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
(owner/'qa.start').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')
rc=1
try:
 seal=json.loads((owner/'seal.json').read_text())
 def verify():
  for n,h in seal.items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
 verify()
 exe=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/bin/rclone')
 base=[sys.executable,'-I',str(snap/'tools/rasteratops-cloud-layout-test'),'--rclone',str(exe)]
 rows=[]
 for name,extra,expected in [('old-legacy-capability',['--ref','ed5a6a51f5974deec8748fbf0dbd2f4984b690f5','--case','PL001-legacy-support'],1),('fixed-content',['--case','PL001'],0),('all-regressions',[],0)]:
  out=owner/'artifacts'/name
  print('START',name,flush=True)
  result=subprocess.run(base+extra+['--output',str(out)])
  cases=json.loads((out/'results.json').read_text())
  if expected:
   assert len(cases)==4,cases
   expected_status={'supported':'FAIL','tiered':'PASS','bios':'FAIL','unsupported':'PASS'}
   for case in cases:
    assert case['status']==expected_status[case['case'].removeprefix('PL001-legacy-support-')],case
    if case['status']=='FAIL':assert 'incorrect system compatibility' in case['why'],case
  assert result.returncode==expected,(name,result.returncode)
  rows.append(dict(name=name,rc=result.returncode,expected_rc=expected,cases=len(cases),status='PASS'))
  (owner/'artifacts/summary.json').write_text(json.dumps(rows,indent=2)+'\n')
 verify();rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
