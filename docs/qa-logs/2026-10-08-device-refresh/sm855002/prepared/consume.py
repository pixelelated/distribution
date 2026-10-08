from pathlib import Path
import datetime,json,subprocess,sys,hashlib
B=Path('/workspace/tmp/pixelelated-m7-sm8550-refresh-02')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def consume(o,runpath,rcpaths):
 run=Path(runpath.read_text().strip());launch=json.loads((o/'launcher-result.json').read_text())
 channels={str(p):int(p.read_text()) for p in rcpaths+[o/'tool-wrapper.rc',run/'build.rc']};channels['launcher_returncode']=launch['runner_returncode'];assert set(channels.values())=={0},channels
 status=(run/'build.status').read_text();assert any('state:       '+s in status for s in ['completed','succeeded','finished']),status
 pids=[launch['pid']]+[int((run/n).read_text()) for n in ['build.pid','watcher.pid','command.pid']];assert not any(Path('/proc',str(pid)).exists() for pid in pids),pids
 return {'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','channels':channels,'actual_owner_pids_absent':pids,'run':str(run)}
kind=sys.argv[1]
if kind=='cache':
 proof=consume(B/'cache-launch',B/'copy.run',[B/'copy.rc',B/'copy.outer.rc'])
 for line in (B/'copy-harness.sha256').read_text().splitlines():
  h,p=line.split('  ',1);assert sha(Path(p))==h,p
 ready=json.loads((B/'cache-ready.json').read_text());assert ready['result']=='PASS' and len(ready['roots'])==3
 for r in ready['roots']:assert r['checksum_equal'] and r['independent_regular_files']>0 and (B/(r['root']+'.compare.txt')).stat().st_size==0
 proof['cache_ready']=ready;destination=B/'cache-consumption.json'
elif kind=='build':
 proof=consume(B,B/'run.path',[B/'inner.rc',B/'outer.rc'])
 for p,h in json.loads((B/'build-seal.json').read_text()).items():assert sha(Path(p))==h,p
 observer=int((B/'observer.pid').read_text());assert not Path('/proc',str(observer)).exists()
 j=json.loads((B/'inputs.json').read_text());subprocess.run(['python3','-I',str(B/'verify-source.py')],cwd=j['host_worktree'],check=True)
 observed=json.loads((B/'container-observed.json').read_text());cid=(B/'build.cid').read_text().strip();assert observed['image']==j['container_image_id'] and observed['id']==cid
 assert subprocess.run(['docker','inspect',cid],capture_output=True).returncode!=0
 assert json.loads((B/'artifacts/installed-inclusion.json').read_text())['result']=='PASS'
 proof.update(observer_exited=observer,actual_container_removed=cid,source_and_seals_unchanged=True,scope='build and installed inclusion; raw/update acceptance remains');destination=B/'build-consumption.json'
else:
 A=Path('/workspace/tmp/pixelelated-m7-sm8550-refresh-acceptance-02');proof=consume(A,A/'run.path',[A/'inner.rc',A/'outer.rc'])
 for p,h in json.loads((A/'seal.json').read_text()).items():assert sha(Path(p))==h,p
 accepted=json.loads((A/'artifacts/acceptance.json').read_text());assert accepted['result']=='PASS';proof['acceptance']=accepted;destination=A/'owner-consumption.json'
assert not destination.exists();destination.write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
