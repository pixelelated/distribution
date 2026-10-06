"""Execute one of the five explicitly approved removals after fresh gates."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time
REPO=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
BASE=Path('/tmp/pixelelated-approved-cleanup-20261006')
NUMBERS=['03','05','06','07','08']
number=sys.argv[1] if len(sys.argv)==2 else ''
assert number in NUMBERS, 'Only an explicitly approved tree number is accepted'
tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement'+number)
owner=Path(__file__).parent
assert os.geteuid()!=0, 'Removal must run as the ordinary build owner'
assert not tree.is_symlink() and tree.resolve()==tree and tree.is_dir()
assert not REPO.is_relative_to(tree)
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args],text=True).strip()
auth=json.loads((BASE/'authorization.json').read_text())
assert auth['issue']==459 and auth['approved_roots']==['/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement'+n for n in NUMBERS]
pre=Path('/tmp/pixelelated-cleanup-preflight-01')
assert json.loads((pre/'completion.json').read_text())['job_rc']==0
for earlier in NUMBERS[:NUMBERS.index(number)]:
 r=json.loads((BASE/('removed-'+earlier+'.json')).read_text())
 assert r['directory_absent'] and r['registration_absent'] and r['helper_rc']==0
rows=json.loads((REPO/'docs/qa-logs/2026-10-05-build-storage/custody-followup-20261006/tree-custody.json').read_text())
row=next(r for r in rows if r['tree']==str(tree))
assert subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()==row['head']
assert subprocess.check_output(['git','-C',str(tree),'branch','--show-current'],text=True).strip()==row['branch']
assert subprocess.check_output(['git','-C',str(tree),'status','--porcelain'],text=True)==row['tracked_status']
assert hashlib.sha256(subprocess.check_output(['git','-C',str(tree),'diff','--binary'])).hexdigest()==row['tracked_diff_sha256']
verified=json.loads((BASE/'preservation-reverified.json').read_text());assert verified['all_pass']
for r in verified['files']:
 s=Path(r['path']).stat()
 assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(r['dev'],r['inode'],r['bytes'],r['mtime_ns'],r['ctime_ns']),r['path']
for r in verified['manifests']:assert sha(r['path'])==r['sha256'],r['path']
protected=json.loads((BASE/'protected-before.json').read_text())
for r in protected:
 p=Path(r['path']);assert p.exists() and p.stat().st_ino==r['inode'],p
 if 'head' in r:assert subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()==r['head']
# The fresh complete scan includes source/build fixtures; re-read every surviving chain.
deps=json.loads((pre/'dependencies.json').read_text());chain_count=0
for record in deps['records']:
 p=Path(record['path'])
 if not p.exists():
  partial03=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement03')
  prior_failed=json.loads(Path('/tmp/pixelelated-approved-cleanup-03/completion.json').read_text())
  repaired=json.loads(Path('/tmp/pixelelated-approved-cleanup-repair03-01/repair-result.json').read_text())
  assert (p.is_relative_to(partial03) and prior_failed['job_rc']==1 and repaired['registered']) or any(p.is_relative_to(Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement'+n)) for n in NUMBERS[:NUMBERS.index(number)]),p
  continue
 data=json.loads(subprocess.check_output(['qemu-img','info','--force-share','--backing-chain','--output=json',str(p)],text=True))
 for item in data:
  for k in ['backing-filename','full-backing-filename']:
   if k in item:
    q=Path(item[k]);q=(q if q.is_absolute() else p.parent/q).resolve()
    assert not q.is_relative_to(tree),(p,q)
 chain_count+=1
containers=subprocess.check_output(['docker','ps','-q'],text=True).split()
for cid in containers:
 d=json.loads(subprocess.check_output(['docker','inspect',cid],text=True))[0]
 for m in d['Mounts']:
  p=Path(m['Source']).resolve();assert not (p==tree or p in tree.parents or tree in p.parents),(cid,p)
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try:first=p.read_bytes().split(b'\0',1)[0].decode()
 except (OSError,UnicodeError):continue
 assert not Path(first).name.startswith('qemu-system-'),p
# Wait briefly for the watcher's next sample after the previous removal's own PID exits.
deadline=time.monotonic()+20
while True:
 lines=(BASE/'root-watch.jsonl').read_text().splitlines();report=None
 for line in reversed(lines):
  try:report=json.loads(line);break
  except json.JSONDecodeError:continue
 if report:
  age=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(report['utc'])).total_seconds()
  okay=report['effective_uid']==0 and report['roots']==auth['approved_roots'] and report['readonly'] and not report['matches'] and not report['unreadable'] and 0<=age<15
  if okay:break
 assert time.monotonic()<deadline,'No fresh, clean root process snapshot; no removal started'
 time.sleep(1)
assert report['helper_sha256']=='4d79c6fcf725334d2d90140719164559adddb043061c05ede8e74036fd123064'
watch=Path('/proc',str(report['watcher_pid']));assert watch.is_dir() and watch.stat().st_uid==0
assert str(BASE/'watch-process-references.py').encode() in (watch/'cmdline').read_bytes().split(b'\0')
(owner/'root-before.json').write_text(json.dumps(report,indent=2)+'\n')
def space():
 s=os.statvfs('/workspace');return {'available_bytes':s.f_bavail*s.f_frsize,'free_bytes':s.f_bfree*s.f_frsize,'reserved_bytes':(s.f_bfree-s.f_bavail)*s.f_frsize}
assert sha(REPO/'tools/fork-worktree')=='421c627ad4cb66b1bf3a4796f202f827761401a0f0f9d15dde484a5fcbbd164b'
before=space();started=datetime.datetime.now(datetime.timezone.utc).isoformat()
print('Gates passed; removing approved tree',number,'with',chain_count,'surviving chains checked',flush=True)
child=subprocess.Popen([str(REPO/'tools/fork-worktree'),'remove',str(tree),'--force'],cwd=REPO)
(owner/'removal.pid').write_text(str(child.pid)+'\n')
last=None
while child.poll() is None:
 sample=space();io=''
 try:io=(Path('/proc',str(child.pid))/'io').read_text()
 except FileNotFoundError:pass
 state=(sample['available_bytes'],io)
 if state!=last:print('Removal activity',number,'available_bytes',sample['available_bytes'],'helper_pid',child.pid,flush=True);last=state
 time.sleep(5)
rc=child.wait();assert rc==0,('Removal helper failed; stop before later trees',number,rc)
assert not tree.exists(),tree
listing=git('worktree','list','--porcelain');assert 'worktree '+str(tree)+'\n' not in listing+'\n'
assert git('rev-parse',row['branch'])==row['head']
for r in protected:
 p=Path(r['path']);assert p.exists() and p.stat().st_ino==r['inode'],p
after=space();result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'started':started,'tree':str(tree),'helper_rc':rc,'helper_pid':child.pid,'directory_absent':True,'registration_absent':True,'branch_retained':row['branch'],'head_retained':row['head'],'surviving_chains_verified':chain_count,'container_count':len(containers),'root_snapshot_utc':report['utc'],'before':before,'after':after,'observed_free_byte_increase':after['free_bytes']-before['free_bytes'],'protected_paths_present':True}
with (BASE/('removed-'+number+'.json')).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print('PASS removed',number,json.dumps(result),flush=True)
