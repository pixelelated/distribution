"""New completion-only recorder. No accepted producer is invoked."""
import argparse,base64,datetime,hashlib,json,os,pathlib,subprocess,sys
C=pathlib.Path(__file__).resolve().parent;R=C.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=True)+'\n')
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--input',action='append',default=[]);p.add_argument('argv',nargs=argparse.REMAINDER);a=p.parse_args();argv=a.argv[1:] if a.argv[:1]==['--'] else a.argv
assert argv and set(os.sched_getaffinity(0))<=set(range(8,24));out=pathlib.Path(a.out);out=out if out.is_absolute() else C/out;out.mkdir(parents=True,exist_ok=False);inputs=[]
for i,name in enumerate(a.input):
 f=pathlib.Path(name);f=f if f.is_absolute() else R/f;assert f.is_file() and not f.is_symlink();b=f.read_bytes();x={'path':str(f),'bytes':len(b),'sha256':sha(b),'base64':base64.b64encode(b).decode()};write(out/('input-'+str(i)+'.json'),x);inputs.append({k:v for k,v in x.items() if k!='base64'})
start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(argv,cwd=R,capture_output=True,env=dict(os.environ,LC_ALL='C',PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'));end=datetime.datetime.now(datetime.timezone.utc).isoformat()
for name,b in [('stdout',r.stdout),('stderr',r.stderr)]:write(out/(name+'.json'),{'bytes':len(b),'sha256':sha(b),'base64':base64.b64encode(b).decode()})
write(out/'receipt.json',{'argv':argv,'cwd':str(R),'start':start,'end':end,'rc':r.returncode,'inputs':inputs,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'recorder_sha256':sha(pathlib.Path(__file__).read_bytes()),'cpu_affinity':sorted(os.sched_getaffinity(0))});sys.stdout.buffer.write(r.stdout);sys.stderr.buffer.write(r.stderr);print('COMPLETION_RECEIPT',out/'receipt.json','rc='+str(r.returncode));sys.exit(r.returncode)
