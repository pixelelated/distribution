"""Narrow new completion record read/scan, without importing accepted audit programs."""
import argparse,datetime,hashlib,json,os,pathlib,stat,subprocess
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-es-vendored-and-data-691')
A='docs/audits/2026_11_02-epic-m6-es-vendored-and-data'
BASE='f01abd480f4e0b337a9fcdde2cec9bc1746b525d'
ES='/home/max/Development/emulationstation-next.worktrees/m6-es-vendored-and-data-691'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def tree(ref):
 rows={}
 for row in git('ls-tree','-r','-z',ref).split(b'\0'):
  if row:
   meta,path=row.split(b'\t');rows[path.decode()]=meta.decode().split()
 return rows
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--scan',action='store_true');ap.add_argument('--final',action='store_true');args=ap.parse_args()
 base=tree(BASE);tip=git('rev-parse','HEAD').decode().strip();current=tree(tip)
 allowed={A+'/'+name for name in ['audit-completion.json','tracker-completion.json','tracker-final-readback.json']}
 allowed|={'.github/sessions/saved-session-state-feature-m6-es-vendored-and-data-691.md','docs/work-logs/2026_11-work_logs/2026_11_03-work_log.md','docs/work-logs/INDEX.md'}
 def accept(path):return path in allowed or path.startswith(A+'/completion/')
 def delta(before,after):
  changed=sorted(p for p in before.keys()|after.keys() if before.get(p)!=after.get(p))
  for p in changed:assert p in after and accept(p) and after[p][:2]==['100644','blob'],('unsafe delta',p)
  return changed
 history=[]
 for rev in git('rev-list','--reverse',BASE+'..'+tip).decode().splitlines():
  parents=git('rev-list','--parents','-n','1',rev).decode().split();assert len(parents)==2,'merge'
  history.append({'commit':rev,'parent':parents[1],'paths':delta(tree(parents[1]),tree(rev))})
 changed=set(delta(base,current))
 changed.update(x for x in git('diff','--name-only','-z',tip).decode().split('\0') if x)
 changed.update(x for x in git('ls-files','--others','--exclude-standard','-z').decode().split('\0') if x)
 records=[]
 for p in sorted(changed):
  assert accept(p),p;q=R/p
  for node in [q,*list(q.parents)[:len(pathlib.PurePosixPath(p).parts)-1]]:assert not node.is_symlink(),p
  s=q.lstat();assert stat.S_ISREG(s.st_mode) and not s.st_mode&0o111,p
  b=q.read_bytes();records.append({'path':p,'bytes':len(b),'sha256':sha(b),'mode':'100644'})
 frozen={p:v for p,v in base.items() if p.startswith(A+'/')};assert len(frozen)==440
 for p,v in frozen.items():
  q=R/p;s=q.lstat();assert stat.S_ISREG(s.st_mode) and not q.is_symlink() and not s.st_mode&0o111,p
  b=q.read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert v==['100644','blob',oid],p
 es=git('-C',ES,'rev-parse','HEAD','HEAD^{tree}').decode().splitlines()
 assert es==['55158d2a64c69fe295fb4e67fd174424a71b1b4d','64b90eb8cb07bdfcd690c74ff6bc980ae490657c']
 assert not git('-C',ES,'status','--porcelain=v1','--untracked-files=all')
 if args.final:assert not git('status','--porcelain=v1','--untracked-files=all')
 result={'result':'PASS','baseline':BASE,'tip':tip,'history':history,'preserved_accepted_audit_files':440,'frozen_manifest_sha256':sha(json.dumps(frozen,sort_keys=True).encode()),'records':records,'es':es,'es_clean':True,'final_clean':args.final,'self_exclusion':'only external postcommit receipts; current precommit invocation cannot include its not-yet-written stdout/receipt'}
 if args.scan:
  payload=b''.join((R/x['path']).read_bytes()+b'\n' for x in records);cmd=['tools/forbidden-terms-check','--stdin'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(cmd,cwd=R,input=payload,capture_output=True,timeout=120)
  result['scan']={'argv':cmd,'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdin_sha256':sha(payload),'input_bytes':len(payload),'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'rc':p.returncode,'program_sha256':sha((R/'tools/forbidden-terms-check').read_bytes())}
  print(json.dumps(result,indent=2));assert p.returncode==0,'new-record scan refused'
 else:print(json.dumps(result,indent=2))
if __name__=='__main__':main()
