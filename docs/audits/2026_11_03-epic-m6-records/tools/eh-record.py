"""New E-H command recorder; all original D tools remain unexecuted and unchanged."""
import argparse,base64,datetime,hashlib,json,os,pathlib,subprocess,sys
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=True)+'\n')
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--input',action='append',default=[]);p.add_argument('--stdin-file');p.add_argument('argv',nargs=argparse.REMAINDER);a=p.parse_args();argv=a.argv[1:] if a.argv[:1]==['--'] else a.argv
assert argv;assert set(os.sched_getaffinity(0))<=set(range(8,24));out=pathlib.Path(a.out);out=out if out.is_absolute() else A/out;out.mkdir(parents=True,exist_ok=False);inp=[]
for i,name in enumerate(a.input+([a.stdin_file] if a.stdin_file else [])):
 f=pathlib.Path(name);f=f if f.is_absolute() else R/f;assert f.is_file() and not f.is_symlink();b=f.read_bytes();item={'path':str(f),'bytes':len(b),'sha256':sha(b),'mode':oct(f.stat().st_mode & 0o777),'base64':base64.b64encode(b).decode()};write(out/('input-'+str(i)+'.json'),item);inp.append({k:v for k,v in item.items() if k!='base64'})
stdin=pathlib.Path(a.stdin_file).read_bytes() if a.stdin_file else None
start=datetime.datetime.now(datetime.timezone.utc).isoformat();proc=subprocess.run(argv,cwd=R,input=stdin,capture_output=True,env=dict(os.environ,LC_ALL='C',PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'));end=datetime.datetime.now(datetime.timezone.utc).isoformat()
for name,b in [('stdout',proc.stdout),('stderr',proc.stderr)]:write(out/(name+'.json'),{'bytes':len(b),'sha256':sha(b),'base64':base64.b64encode(b).decode()})
write(out/'receipt.json',{'argv':argv,'cwd':str(R),'start':start,'end':end,'rc':proc.returncode,'inputs':inp,'stdout_sha256':sha(proc.stdout),'stderr_sha256':sha(proc.stderr),'recorder_sha256':sha(pathlib.Path(__file__).read_bytes()),'cpu_affinity':sorted(os.sched_getaffinity(0)),'python':sys.version,'stream_transport':'base64 of exact original bytes; no raw-stream rewrite'})
sys.stdout.buffer.write(proc.stdout);sys.stderr.buffer.write(proc.stderr);print('EH_RECEIPT',out/'receipt.json','rc='+str(proc.returncode));sys.exit(proc.returncode)
