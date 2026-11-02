#!/usr/bin/env python3
"""Run one explicitly supplied record command, retaining bytes and actual exit."""
import datetime,hashlib,json,os,pathlib,subprocess,sys
assert set(os.sched_getaffinity(0)) <= set(range(8,24)), 'CPU affinity escaped dispatch'
out=pathlib.Path(sys.argv[1]);argv=sys.argv[2:];out.parent.mkdir(parents=True,exist_ok=True)
assert not out.with_suffix('.json').exists(), 'receipt already exists'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(x):return hashlib.sha256(x).hexdigest()
start=now();p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'LC_ALL':'C','PYTHONDONTWRITEBYTECODE':'1'})
out.with_suffix('.stdout').write_bytes(p.stdout);out.with_suffix('.stderr').write_bytes(p.stderr)
files={x:sha(pathlib.Path(x).read_bytes()) for x in argv if pathlib.Path(x).is_file()}
out.with_suffix('.json').write_text(json.dumps({'argv':argv,'cwd':os.getcwd(),'started':start,'finished':now(),'exit':p.returncode,'affinity':sorted(os.sched_getaffinity(0)),'locale':'C','program_and_direct_inputs':files,'producer_sha256':sha(pathlib.Path(__file__).read_bytes()),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)},indent=2)+'\n')
print(p.stdout.decode(errors='replace'),end='');print(p.stderr.decode(errors='replace'),end='',file=sys.stderr);sys.exit(p.returncode)
