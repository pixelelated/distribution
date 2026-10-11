from pathlib import Path
import json,hashlib,subprocess,copy
p=Path(__file__).resolve().parent;b=Path('/workspace/tmp/pixelelated-m7-build20b');e=Path('/workspace/tmp/pix549-container-tmp01');j=json.loads((p/'inputs.json').read_text())
original=json.loads((b/'launcher-result.json').read_text());assert original['runner_returncode']==1 and not Path('/proc/'+str(original['pid'])).exists()
assert (b/'inner.rc').read_text().strip()=='1' and (b/'outer.rc').read_text().strip()=='1'
w=json.loads((e/'docker-wait20b.json').read_text());assert w['wait_returncode']==0 and w['stdout'].strip()=='0' and not w['stderr']
a=json.loads((e/'actual-container20b.json').read_text())
assert a['container_id']==(b/'build.cid').read_text().strip()
assert (p/'inputs.json').read_bytes()==(b/'inputs.json').read_bytes()
def verify(o):
 assert o['image']==j['container_image_id'] and o['user']=='1000:1000'
 assert o['working_dir']=='/workspace/repos/rocknix.worktrees/m7-pixelelated'
 assert any(x['Source']==j['host_worktree'] and x['Destination']==o['working_dir'] for x in o['mounts'])
 assert o['effective_tmpdir']=='/tmp' and o['mktemp_returncode']==0
verify(a)
controls=[]
for field,value in [('effective_tmpdir','/unmounted-host'),('mktemp_returncode',1),('user','0:0')]:
 bad=copy.deepcopy(a);bad[field]=value
 try:verify(bad)
 except AssertionError:controls.append({'case':field,'refused':True})
 else:raise AssertionError('negative accepted '+field)
assert len(a['configured_tmpdir_entries'])==2,'original duplicate shape must be retained'
assert 'AssertionError:' in (b/'console.log').read_text() and 'temporary==' in (b/'console.log').read_text()
subprocess.run(['python3',str(b/'verify-source.py')],check=True)
subprocess.run(['python3',str(p/'verify-installed.py')],check=True)
(p/'result.json').write_text(json.dumps({'result':'PASS','original_wrapper_returncode':1,'actual_build_container_returncode':0,'resolved_monitor_assertion':'Docker retains both configured TMPDIR entries; actual runtime and mktemp use /tmp','actual_container_sha256':hashlib.sha256((e/'actual-container20b.json').read_bytes()).hexdigest(),'controls':controls,'installed_verification':'installed-result.json'},indent=2)+'\n')
print('PASS independent monitoring resolution and actual assembled files; original wrapper remains1',flush=True)
