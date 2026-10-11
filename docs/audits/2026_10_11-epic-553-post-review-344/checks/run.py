from pathlib import Path
import json,subprocess,os,hashlib,datetime,re
P=Path(__file__).resolve().parent
R=Path('/workspace/repos/rocknix.worktrees/m7-component-inputs')
E=Path('/home/max/Development/emulationstation-next.worktrees/qa-integration')
M=json.loads((P/'manifest.json').read_text());env={**os.environ,'TMPDIR':str(P/'tmp'),'PYTHONDONTWRITEBYTECODE':'1','TERM':'dumb'}
def digest_bytes(b):return hashlib.sha256(b).hexdigest()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def seal():
 for name,want in M['paths'].items():assert digest(R/name)==want,name
seal();rows=[]
def check(name,cmd,expected=0,extra=None,timeout=180):
 print('START',name,flush=True)
 with (P/(name+'.log')).open('w') as f:q=subprocess.run(cmd,cwd=R,env={**env,**(extra or {})},stdout=f,stderr=subprocess.STDOUT,timeout=timeout)
 rows.append({'name':name,'command':cmd,'returncode':q.returncode,'expected':expected});(P/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
 assert q.returncode==expected,(name,q.returncode)
 print('PASS',name,flush=True)
packages=sorted({Path(p).parent.name for p in M['paths'] if p.endswith('/package.mk')})
check('pkgcheck',['tools/pkgcheck',*packages])
check('vm-pair',['tools/vm-pair-test'])
check('readiness',['tools/vm-upgrade-readiness-test'])
check('optional-info',['tools/rocknix-info-test','--baseline',str(P/'baseline-info'),'--output',str(P/'info')])
check('es-lifetime',['python3',str(E/'tests/cloud-oauth-lifetime.py')])
src=Path('/workspace/tmp/pix541-refresh72/final-patched')
base=['tools/raofflineproxy-integration-test','--source',str(src),'--predecessor-source','/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64/build/raofflineproxy-879b158995d412af434301ebdae581f66b8b6d57']
native={'RAOFFLINEPROXY_RCHASH_LIB':str(src/'.host-qualification-541/libraproxy_rchash.so')}
helper=R/'projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed'
negative=P/'negative-helper';negative.write_text(helper.read_text().replace('time.sleep(30.0)','time.sleep(0.0)'))
check('proxy-negative',base+['--helper',str(negative)],1,native)
check('proxy-fixed',base,0,native)
for n in ['proxy-negative','proxy-fixed']:
 t=(P/(n+'.log')).read_text();assert 'Ran 12 tests' in t and 'test_existing_pause_boundaries_survive_removed_upstream_helper' in t
assert 'FAILED (failures=1)' in (P/'proxy-negative.log').read_text()
assert (P/'proxy-fixed.log').read_text().rstrip().endswith('OK')
fetch=json.loads((R/'docs/qa-logs/2026-10-11-dependency-refresh/fetch.json').read_text());archive=Path('/workspace/tmp/pix541-refresh72')
for n,x in fetch['files'].items():assert digest(archive/n)==x['sha256']
sums=(archive/'SHA256SUMS').read_text()
for arch in ['amd64','arm64']:assert fetch['files']['rclone-'+arch+'.zip']['sha256']+'  rclone-v1.75.2-linux-'+arch+'.zip' in sums
check('installed-rclone-version',['/workspace/tmp/pixelelated-m7-image20/root/usr/bin/rclone','version'])
assert 'rclone v1.75.2' in (P/'installed-rclone-version.log').read_text()
q=R/'docs/qa-logs/2026-10-11-pixelelated-replacement-20'
for name in ['webdav','sftp','s3']:
 t=(q/(name+'-round-trip.log')).read_text();assert sum(x.lstrip().startswith('PASS ') for x in t.splitlines())==108
 assert not any(x.lstrip().startswith(('FAIL ','SKIP ')) for x in t.splitlines()) and t.strip().endswith('PASSED')
for row in json.loads((q/'upgrade/result.json').read_text()):assert row['returncode']==0
raw=json.loads((q/'upgrade/actual-rehearsal.raw.json').read_text());assert digest_bytes(raw['raw_text'].encode())==raw['sha256']
assert 'PASS saves and save states byte-identical' in raw['raw_text']
assert raw['raw_text'].count('PASS storage ready in boot ')==2
u=Path('/workspace/tmp/pixelelated-m7-upgrade20');manifest=json.loads((u/'prepared-manifest.json').read_text())
for n,h in manifest.items():assert digest(u/n)==h,n
assert "'VM_QEMU_RUNTIME_DIR':str(p/'runtime')" in (u/'run.py').read_text()
terminal=json.loads((u/'launcher-result.json').read_text());assert terminal['runner_returncode']==0 and not Path('/proc',str(terminal['pid'])).exists()
seal()
(P/'result.json').write_text(json.dumps({'result':'PASS','head':M['head'],'commands':rows,'recipe_count':len(packages),'random_reverification':['545 runtime root and real upgrade original evidence','541 archive hashes, installed binary and324 original protocol assertions'],'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
print('PASS audit bounded controls and original random-claim evidence re-verification',flush=True)
