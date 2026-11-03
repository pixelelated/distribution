"""Retain one new T46 command and its actual streams/input identities."""
import argparse,datetime,hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
ap=argparse.ArgumentParser()
ap.add_argument('--name',required=True)
ap.add_argument('--input',action='append',default=[])
ap.add_argument('--stdin-file')
ap.add_argument('argv',nargs=argparse.REMAINDER)
a=ap.parse_args();argv=a.argv[1:] if a.argv[:1]==['--'] else a.argv
if not argv:raise SystemExit('command required')
out=ROOT/a.name
if not out.is_relative_to(ROOT) or '..' in pathlib.PurePath(a.name).parts:raise SystemExit('invalid record path')
out.mkdir(parents=True,exist_ok=False)
inputs={}
for name in a.input+([a.stdin_file] if a.stdin_file else []):
 p=pathlib.Path(name);p=p if p.is_absolute() else REPO/p
 b=p.read_bytes();inputs[str(p)]={'bytes':len(b),'sha256':sha(b)}
stdin=pathlib.Path(a.stdin_file).read_bytes() if a.stdin_file else None
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
proc=subprocess.run(argv,cwd=REPO,input=stdin,capture_output=True,env=dict(os.environ,LC_ALL='C',PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'))
end=datetime.datetime.now(datetime.timezone.utc).isoformat()
(out/'stdout').write_bytes(proc.stdout);(out/'stderr').write_bytes(proc.stderr)
r={'argv':argv,'cwd':str(REPO),'start':start,'end':end,'rc':proc.returncode,
 'stdout_sha256':sha(proc.stdout),'stderr_sha256':sha(proc.stderr),'inputs':inputs,
 'recorder_sha256':sha(pathlib.Path(__file__).read_bytes()),'cpus':sorted(os.sched_getaffinity(0)),
 'python':sys.version,'locale':'C'}
(out/'receipt.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
sys.stdout.buffer.write(proc.stdout);sys.stderr.buffer.write(proc.stderr)
print('T46_RECEIPT '+str(out/'receipt.json')+' rc='+str(proc.returncode))
raise SystemExit(proc.returncode)
