from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import datetime,hashlib,json,os,subprocess,time
b=Path('/tmp/pixelelated-approved-cleanup-20261006');repo=Path('/workspace/repos/rocknix.worktrees/conflict-resolution');owner=Path(__file__).parent
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args],text=True).strip()
records=[];listing=git(repo,'worktree','list','--porcelain')+'\n'
for number in ['03','05','06','07','08']:
 r=json.loads((b/('removed-'+number+'.json')).read_text());assert r['helper_rc']==0 and not Path(r['tree']).exists()
 assert 'worktree '+r['tree']+'\n' not in listing
 assert git(repo,'rev-parse',r['branch_retained'])==r['head_retained']
 o=Path('/tmp/pixelelated-approved-cleanup-'+number+('-v2' if number=='03' else '-v3'))
 assert json.loads((o/'completion.json').read_text())['job_rc']==0
 assert not Path('/proc',(o/'removal.pid').read_text().strip()).exists()
 records.append(r)
protected=json.loads((b/'protected-before.json').read_text())
for r in protected:
 p=Path(r['path']);assert p.exists() and p.stat().st_ino==r['inode'],p
 if 'head' in r:assert git(p,'rev-parse','HEAD')==r['head']
previous=json.loads((b/'preservation-reverified.json').read_text());todo={r['path']:r['sha256'] for r in previous['files']}
for r in previous['manifests']:assert sha(r['path'])==r['sha256']
bundle=Path('/workspace/artifacts/pixelelated-candidates/sha256/b77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1')
assert sha(bundle/'manifest.json')==bundle.name
manifest=json.loads((bundle/'manifest.json').read_text())
for name,info in manifest['files'].items():todo[str(bundle/name)]=info['sha256']
def check(item):
 p,want=item;size=Path(p).stat().st_size;assert sha(p)==want,p;return size
done=total=0;last=time.monotonic()
with ThreadPoolExecutor(max_workers=4) as pool:
 for f in as_completed([pool.submit(check,item) for item in todo.items()]):
  total+=f.result();done+=1
  if time.monotonic()-last>5:
   print('Rehashed',done,'/',len(todo),'files;',total,'bytes',flush=True);last=time.monotonic()
print('PASS all retained files and current bundle hashes',done,total,flush=True)
source=json.loads((repo/'docs/qa-logs/2026-10-05-build-storage/preservation-20261006/runtime-02/source-custody.json').read_text());gitinputs={}
for row in source['trees']:
 m=json.loads(Path(row['manifest']).read_text());assert sha(row['manifest'])==row['sha256']
 for rec in m['records']:
  for c in rec.get('cache',[]):
   if 'git_head' in c:gitinputs[Path(source['source_cache'])/rec['package']/c['name']]=c
for p,c in gitinputs.items():
 assert git(p,'rev-parse','HEAD')==c['git_head']
 assert [x.strip() for x in git(p,'submodule','status','--recursive').splitlines()]==[x.strip() for x in c['submodules']]
print('PASS retained source git inputs',len(gitinputs),flush=True)
subprocess.run(['/usr/bin/python3','-I','/workspace/tmp/pixelelated-m7-replacement-14/verify-source.py'],cwd='/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement14',check=True)
deps=json.loads(Path('/tmp/pixelelated-cleanup-preflight-01/dependencies.json').read_text());chains=0;removed_fixtures=0
for rec in deps['records']:
 p=Path(rec['path'])
 if not p.exists():
  assert any(p.is_relative_to(Path(r['tree'])) for r in records),p
  removed_fixtures+=1;continue
 data=json.loads(subprocess.check_output(['qemu-img','info','--force-share','--backing-chain','--output=json',str(p)],text=True))
 for item in data:
  for k in ['backing-filename','full-backing-filename']:
   if k in item:
    q=Path(item[k]);q=(q if q.is_absolute() else p.parent/q).resolve()
    assert not any(q.is_relative_to(Path(r['tree'])) for r in records),(p,q)
 chains+=1
rootreport=json.loads((b/'root-watch.jsonl').read_text().splitlines()[-1]);assert rootreport['effective_uid']==0 and rootreport['all_five_directories_absent']
assert not Path('/proc',str(rootreport['watcher_pid'])).exists(),'Root watcher has not exited yet'
st=os.statvfs('/workspace');after={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'available_bytes':st.f_bavail*st.f_frsize,'free_bytes':st.f_bfree*st.f_frsize,'reserved_bytes':(st.f_bfree-st.f_bavail)*st.f_frsize}
before=json.loads((b/'execution-before.json').read_text());assert before['reserved_bytes']==after['reserved_bytes']
r={'utc':after['utc'],'all_pass':True,'removals':records,'protected_paths_verified':len(protected),'retention_manifests_verified':len(previous['manifests']),'retained_files_rehashed':len(previous['files']),'total_files_rehashed_including_current_bundle':done,'bytes_rehashed':total,'source_git_inputs_verified':len(gitinputs),'current_bundle_files_verified':len(manifest['files']),'current_frozen_input_verifier_passed':True,'surviving_backing_chains_verified':chains,'removed_internal_fixtures':removed_fixtures,'root_watcher_pid_absent':rootreport['watcher_pid'],'before':before,'after':after,'observed_free_byte_increase':after['free_bytes']-before['free_bytes'],'reserved_bytes_unchanged':True,'scope':'Live filesystem delta includes small concurrent host changes; no whole-host atomic allocation claim'}
(b/'final-verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
