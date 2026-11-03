"""Narrow completion-only comparison and changed-record scan, not an audit replay."""
import argparse,base64,datetime,hashlib,json,pathlib,stat,subprocess
C=pathlib.Path(__file__).resolve().parent;R=C.parents[3];A=C.parent
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--tip');p.add_argument('--scope-only',action='store_true');args=p.parse_args();out=pathlib.Path(args.out);out=out if out.is_absolute() else C/out;out.mkdir(parents=True,exist_ok=False)
ctx=json.loads((C/'context.json').read_text());base=ctx['accepted_final'];frozen=json.loads((C/'accepted-audit-identities.json').read_text());prefix=str(C.relative_to(R))+'/'
exact={str((A/'audit-completion.json').relative_to(R)),'.github/sessions/saved-session-state-feature-m6-records-693.md','docs/work-logs/2026_11-work_logs/2026_11_03-work_log.md','docs/work-logs/INDEX.md'}
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def allowed(p):return p in exact or p.startswith(prefix)
def checkdiff(*rev):
 raw=git('diff','--raw','--no-abbrev','--no-renames','-z',*rev);parts=raw.split(b'\0');names=[]
 for i in range(0,len(parts)-1,2):
  meta=parts[i].decode().split();name=parts[i+1].decode();assert meta[-1] in ['A','M'] and meta[1]=='100644' and allowed(name),(meta,name);names.append(name)
 return names
def tree(rev):
 result={}
 for row in git('ls-tree','-rlz',rev,'--',str(A.relative_to(R))).split(b'\0'):
  if row:
   m,path=row.split(b'\t',1);mode,typ,oid,size=m.decode().split();result[path.decode()]={'mode':mode,'type':typ,'oid':oid,'bytes':int(size)}
 return result
assert tree(base)==frozen and len(frozen)==976
tip=args.tip or git('rev-parse','HEAD').decode().strip();assert git('rev-parse','HEAD').decode().strip()==tip
current=tree(tip);assert {p:current.get(p) for p in frozen}==frozen
index={}
for row in git('ls-files','--stage','-z','--',str(A.relative_to(R))).split(b'\0'):
 if row:
  m,path=row.split(b'\t',1);mode,oid,stage=m.decode().split();assert stage=='0';index[path.decode()]=(mode,oid)
for path,m in frozen.items():
 assert index.get(path)==(m['mode'],m['oid']);f=R/path;s=f.lstat();assert stat.S_ISREG(s.st_mode) and not s.st_mode&0o111;b=f.read_bytes();assert len(b)==m['bytes'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==m['oid'],path
commits=git('rev-list','--reverse',base+'..'+tip).decode().splitlines();git('merge-base','--is-ancestor',base,tip)
for c in commits:
 parents=git('show','-s','--format=%P',c).decode().split();assert len(parents)==1;checkdiff(parents[0],c)
views={'tip':checkdiff(base,tip),'index':checkdiff('--cached',base),'working':checkdiff(base)}
untracked=[p.decode() for p in git('ls-files','--others','--exclude-standard','-z').split(b'\0') if p];assert all(allowed(p) for p in untracked)
paths=set().union(*views.values(),untracked)
for path in paths:
 f=R/path;s=f.lstat();assert stat.S_ISREG(s.st_mode) and not s.st_mode&0o111,path
if args.tip:assert git('status','--porcelain=v1')==b'';paths=set(views['tip'])
source=(R/'docs/audits/README.md').read_bytes();assert len(source)==813 and sha(source)=='410e4432c01a38cda578a68fdaa730129c15a8e3e60c7305001bb40bd5a71b6c'
result={'base':base,'tip':tip,'commits':commits,'frozen_count':len(frozen),'frozen_manifest_sha256':sha(json.dumps(frozen,sort_keys=True,separators=(',',':')).encode()),'source_readme_sha256':sha(source),'views':{k:len(v) for k,v in views.items()},'untracked':len(untracked),'scope':'Only new completion records/marker, exact lane pointer, November3 day and INDEX; no accepted audit/source mutation, deletion, unsafe mode or merge.'}
if not args.scope_only:
 rows=[];chunks=[]
 for path in sorted(paths):
  f=R/path;b=f.read_bytes()
  if args.tip:assert b==git('show',tip+':'+path)
  rows.append({'path':path,'mode':'100644','bytes':len(b),'sha256':sha(b),'blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()});chunks.append((path+'\n').encode()+b+b'\n')
 data=b''.join(chunks);argv=['tools/forbidden-terms-check','--stdin'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();run=subprocess.run(argv,cwd=R,input=data,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for label,b in [('stdout',run.stdout),('stderr',run.stderr)]:(out/(label+'.json')).write_text(json.dumps({'bytes':len(b),'sha256':sha(b),'base64':base64.b64encode(b).decode()},indent=2)+'\n')
 result.update({'files':rows,'count':len(rows),'logical_bytes':sum(x['bytes'] for x in rows),'file_manifest_sha256':sha(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()),'stdin_sha256':sha(data),'argv':argv,'cwd':str(R),'start':start,'end':end,'rc':run.returncode,'scanner_sha256':sha((R/argv[0]).read_bytes()),'driver_sha256':sha(pathlib.Path(__file__).read_bytes()),'stdout_sha256':sha(run.stdout),'stderr_sha256':sha(run.stderr),'self_exclusions':'New scan output/manifest and the active outer receipt are produced afterward or outside the repository. Final --tip covers exact committed changed paths; precommit working scan is only that snapshot.'})
 (out/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');assert run.returncode==0
else:(out/'scope.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='files'}));print('PASS completion-only comparison'+(' and exact changed-record scan' if not args.scope_only else ''))
