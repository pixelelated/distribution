"""Exact current/committed E-H changed-path scan, with explicit self exclusions."""
import argparse,base64,datetime,hashlib,json,pathlib,subprocess,os,stat
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2];p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--tip');args=p.parse_args();out=pathlib.Path(args.out);out=out if out.is_absolute() else A/out;out.mkdir(parents=True,exist_ok=False);base='a0d4c4fda7a0c16c04d57edf921ffeb741eff19b';policy=json.loads((A/'stage-e/scope-policy.json').read_text())
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def sha(b):return hashlib.sha256(b).hexdigest()
if args.tip:
 assert git('status','--porcelain=v1')==b'';assert git('rev-parse','HEAD').decode().strip()==args.tip
 paths={p.decode() for p in git('diff','--name-only','-z',base,args.tip).split(b'\0') if p}
else:
 paths=set()
 for cmd in [('diff','--name-only','-z',base),('diff','--cached','--name-only','-z',base),('ls-files','--others','--exclude-standard','-z')]:paths.update(p.decode() for p in git(*cmd).split(b'\0') if p)
rows=[];parts=[]
for path in sorted(paths):
 assert path==policy['readme'] or path in policy['mutable'] or path in policy['exact_records'] or path in policy['new_tools'] or any(path.startswith(x) for x in policy['new_prefixes'])
 f=R/path;assert f.is_file() and not f.is_symlink() and not (f.stat().st_mode & 0o111);b=f.read_bytes()
 if args.tip:assert b==git('show',args.tip+':'+path)
 rows.append({'path':path,'mode':'100644','bytes':len(b),'sha256':sha(b),'blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()});parts.append((path+'\n').encode()+b+b'\n')
data=b''.join(parts);argv=['tools/forbidden-terms-check','--stdin'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(argv,cwd=R,input=data,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat()
for s,b in [('stdout',r.stdout),('stderr',r.stderr)]:(out/(s+'.json')).write_text(json.dumps({'bytes':len(b),'sha256':sha(b),'base64':base64.b64encode(b).decode()},indent=2)+'\n')
frozen_current={}
for row in git('ls-tree','-rz',args.tip or 'HEAD','--',policy['audit_root']).split(b'\0'):
 if row:
  meta,path=row.split(b'\t',1);mode,typ,oid=meta.decode().split();path=path.decode()
  if path in policy['frozen']:frozen_current[path]={'mode':mode,'type':typ,'oid':oid}
assert frozen_current==policy['frozen']
frozen_digest=sha(json.dumps(frozen_current,sort_keys=True,separators=(',',':')).encode())
result={'base':base,'tip':args.tip,'frozen_count':len(frozen_current),'frozen_manifest_sha256':frozen_digest,'scope_policy_sha256':sha((A/'stage-e/scope-policy.json').read_bytes()),'source_readme_sha256':sha((R/'docs/audits/README.md').read_bytes()),'files':rows,'count':len(rows),'logical_bytes':sum(x['bytes'] for x in rows),'file_manifest_sha256':sha(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()),'stdin_sha256':sha(data),'argv':argv,'cwd':str(R),'start':start,'end':end,'rc':r.returncode,'scanner_program_sha256':sha((R/argv[0]).read_bytes()),'driver_sha256':sha(pathlib.Path(__file__).read_bytes()),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'self_exclusions':'This scan output and active outer receipt are external to the enumerated input set. A working snapshot does not claim final-commit coverage; final --tip scan covers exact committed changes.'};(out/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='files'}));assert r.returncode==0;print('PASS exact enumerated E-H changed-path scan')
