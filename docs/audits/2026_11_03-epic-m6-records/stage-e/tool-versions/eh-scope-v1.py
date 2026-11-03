"""E-H history/index/worktree/untracked guard; no original D tool execution."""
import argparse,hashlib,json,os,pathlib,stat,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--policy',required=True);p.add_argument('--tip',default='HEAD');a=p.parse_args();R=pathlib.Path(a.repo);P=json.load(open(a.policy));base=P['base'];bad=[];checks=[]
def git(*args):return subprocess.check_output(['git','-C',str(R),*args])
def tree(ref):
 d={}
 for row in git('ls-tree','-rz',ref).split(b'\0'):
  if row:
   meta,path=row.split(b'\t',1);mode,typ,oid=meta.decode().split();d[path.decode()]={'mode':mode,'type':typ,'oid':oid}
 return d
def allowed(path):return path==P['readme'] or path in P['mutable'] or path in P['exact_records'] or path in P['new_tools'] or any(path.startswith(prefix) for prefix in P['new_prefixes'])
def error(view,path,why):bad.append({'view':view,'path':path,'reason':why})
def change(view,path,new):
 if new is None:error(view,path,'deletion/rename forbidden');return
 if not allowed(path):error(view,path,'outside exact write ownership')
 if path in P['frozen']:error(view,path,'frozen D artifact changed')
 if new['type']!='blob' or new['mode']!='100644':error(view,path,'ordinary100644 required')
 if path==P['readme'] and new['oid']!=P['after_oid']:error(view,path,'README not exact specified after blob')
def compare(view,old,new):
 paths=sorted(k for k in old.keys()|new.keys() if old.get(k)!=new.get(k))
 for path in paths:change(view,path,new.get(path))
 checks.append({'view':view,'changed_paths':len(paths),'path_set_sha256':hashlib.sha256(('\n'.join(paths)+'\n').encode()).hexdigest()})
def working(path):
 f=R/path
 try:s=f.lstat()
 except FileNotFoundError:return None
 if not stat.S_ISREG(s.st_mode):return {'mode':'120000' if stat.S_ISLNK(s.st_mode) else 'unsafe','type':'nonordinary','oid':''}
 if stat.S_IMODE(s.st_mode)!=0o644:return {'mode':'100755' if s.st_mode & 0o111 else oct(stat.S_IMODE(s.st_mode)),'type':'blob','oid':''}
 fd=os.open(f,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb') as stream:b=stream.read()
 return {'mode':'100644','type':'blob','oid':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
B=tree(base);H=tree(a.tip)
expected={k:v for k,v in B.items() if k.startswith(P['audit_root']) and k not in P['mutable']}
if expected!=P['frozen']:error('policy','frozen-manifest','not exact immutable baseline minus six mutable narratives')
rc=subprocess.run(['git','-C',str(R),'merge-base','--is-ancestor',base,a.tip],capture_output=True).returncode
if rc:error('history','base','not ancestor')
commits=git('rev-list','--reverse',base+'..'+a.tip).decode().splitlines()
for commit in commits:
 parents=git('show','-s','--format=%P',commit).decode().split()
 if len(parents)!=1:error('history',commit,'merge/root forbidden');continue
 compare('commit:'+commit,tree(parents[0]),tree(commit))
compare('protected-baseline-to-tip',B,H)
I={}
for row in git('ls-files','--stage','-z').split(b'\0'):
 if not row:continue
 meta,path=row.split(b'\t',1);mode,oid,stage=meta.decode().split();path=path.decode()
 if stage!='0':error('index',path,'unmerged index stage')
 I[path]={'mode':mode,'type':'commit' if mode=='160000' else 'blob','oid':oid}
compare('staged-index',H,I);compare('protected-baseline-to-index',B,I)
changed={p.decode() for p in git('diff-files','--name-only','-z').split(b'\0') if p}
# Unstaged changes are independent of index; restored working bytes cannot absolve a forbidden index.
for path in sorted(changed):
 if not allowed(path):error('working-tree',path,'outside exact write ownership');continue
 w=working(path)
 if I.get(path)!=w:change('working-tree',path,w)
for path,identity in P['frozen'].items():
 if H.get(path)!=identity:error('frozen-tip',path,'identity drift')
 if I.get(path)!=identity:error('frozen-index',path,'identity drift')
 if working(path)!=identity:error('frozen-working',path,'identity drift')
U=[p.decode() for p in git('ls-files','--others','--exclude-standard','-z').split(b'\0') if p]
for path in U:
 if not allowed(path):error('untracked',path,'outside exact write ownership');continue
 change('untracked',path,working(path))
for view,new in [('index-current',I.get(P['readme'])),('working-current',working(P['readme']))]:
 if new!={'mode':'100644','type':'blob','oid':P['after_oid']}:error(view,P['readme'],'exact current after identity required')
result={'base':base,'tip':git('rev-parse',a.tip).decode().strip(),'policy_sha256':hashlib.sha256(pathlib.Path(a.policy).read_bytes()).hexdigest(),'commits':len(commits),'views':checks,'unstaged_count':len(changed),'untracked_count':len(U),'frozen_count':len(P['frozen']),'refusals':bad}
print(json.dumps(result,sort_keys=True));print(('REFUSE' if bad else 'PASS')+' E-H every-commit, staged-index, working-tree, untracked and frozen identities');sys.exit(1 if bad else 0)
