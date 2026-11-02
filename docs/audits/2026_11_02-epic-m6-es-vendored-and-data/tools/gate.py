"""Receipt runner for explicitly enumerated T44 distribution record gates, never ES tools."""
import pathlib,sys,json,subprocess,datetime,hashlib,os
D=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-es-vendored-and-data-691')
A=D/'docs/audits/2026_11_02-epic-m6-es-vendored-and-data'
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
name=sys.argv[1];tag=sys.argv[2]
assert tag.replace('-','').isalnum()
cmds={'pre-issue':['python3','-I','tools/lint-audit-artifacts',str(A),'--phase','pre-issue'],'rules':['tools/rules-check','--quiet'],'register':['tools/register-check'],'index':['tools/work-log-index','--check'],'ceremony':['tools/ceremony-check','--gate'],'forbidden':['tools/forbidden-terms-check'],'hooks':['.githooks/hooks-test'],'diff':['git','diff','--check','48a335700d05a733703e1b58536877b91b921259'],'syntax':['python3','-I','-c','import ast,pathlib; ps=sorted(pathlib.Path("'+str(A/'tools')+'").glob("*.py")); [ast.parse(p.read_bytes(),filename=str(p)) for p in ps]; print("PASS syntax",len(ps),"new audit tools")']}
if name in ['issue-lint','issue-check']:
    issue=sys.argv[3];assert issue.isdigit()
    cmd=cmds['pre-issue']+['--issue',issue] if name=='issue-lint' else ['tools/box-check','--issue',issue]
else:cmd=cmds[name]
out=A/'stage-d'/tag;out.mkdir(exist_ok=False)
start=now();timed=False
try:
    r=subprocess.run(cmd,cwd=D,capture_output=True,timeout=1200 if name=='forbidden' else 300,env=dict(os.environ,LC_ALL='C',PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'));rc=r.returncode;stdout=r.stdout;stderr=r.stderr
except subprocess.TimeoutExpired as e:rc=124;stdout=e.stdout or b'';stderr=(e.stderr or b'')+b'\nTIMEOUT\n';timed=True
(out/'stdout').write_bytes(stdout);(out/'stderr').write_bytes(stderr)
tool=D/cmd[2] if cmd[:2]==['python3','-I'] and cmd[2]!='-c' else D/cmd[0]
receipt=dict(argv=cmd,cwd=str(D),start=start,end=now(),rc=rc,timeout_s=1200 if name=='forbidden' else 300,timed_out=timed,tool_sha256=sha(tool.read_bytes()) if tool.is_file() else None,runner_sha256=sha(pathlib.Path(__file__).read_bytes()),stdout_sha256=sha(stdout),stderr_sha256=sha(stderr),cpus=sorted(os.sched_getaffinity(0)),python=sys.version,locale='C',head=subprocess.check_output(['git','-C',str(D),'rev-parse','HEAD']).decode().strip(),inputs={p.name:sha(p.read_bytes()) for p in A.glob('0*.md')})
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print('RC',rc);print(stdout.decode(errors='replace'));print(stderr.decode(errors='replace'));raise SystemExit(rc)
