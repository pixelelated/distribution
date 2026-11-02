#!/usr/bin/env python3
"""Current checks for only the newly appended pins-read records; no accepted replay."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,time
D=Path(__file__).resolve().parent;A=D.parents[1];R=A.parents[2];os.chdir(R)
os.environ.update(LC_ALL='C',TMPDIR='/workspace/tmp/m6-t41/tmp')
BASE='61a1a674c10d520f9d93748c5a73deaadb08b158'
def h(b):return hashlib.sha256(b).hexdigest()
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(*args):return subprocess.check_output(['git',*args])
assert not (D/'validation-final.json').exists()
(D/'checkers-final').mkdir(exist_ok=True);checks=[]
def run(name,argv,expected=0,stdin=None):
 start=stamp();tic=time.monotonic();p=subprocess.run(argv,input=stdin,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
 dest=D/'checkers-final'/(name+'.out');dest.write_bytes(p.stdout)
 checks.append(dict(name=name,argv=argv,cwd=str(R),start=start,end=stamp(),elapsed_seconds=round(time.monotonic()-tic,6),rc=p.returncode,stdout=str(dest.relative_to(D)),sha256=h(p.stdout)))
 (D/'validation-final-in-progress.json').write_text(json.dumps(checks,indent=2)+'\n')
 print(name,'rc',p.returncode,flush=True);assert p.returncode==expected,(name,p.stdout.decode()[-1200:])
 return p.stdout
start=stamp()
meta=json.loads((D/'read-record.json').read_text())
raw=json.loads((D/'source.git-show.json').read_text())['stdout'].encode();assert raw==json.loads((D/'handback.git-show.json').read_text())['stdout'].encode()
assert h(raw)==meta['source_sha256'] and raw==(R/meta['source_path']).read_bytes()
assert raw==git('show',meta['source_ref']+':'+meta['source_path'])
for c in meta['checks']:
 assert c['rc']==0
 assert h(json.loads((D/c['stdout']).read_text())['stdout'].encode())==c['stdout_sha256']
 assert h((D/c['stderr']).read_bytes())==c['stderr_sha256'] and not (D/c['stderr']).read_bytes()
ls=raw.decode().splitlines(keepends=True)
nums=[16,18,22,23,27,29,30,36,37,40,42,43,46,48,49]
quote=''.join(f'{i:6d}\t{ls[i-1]}' for i in nums)
assert quote==(D/'numbered-assignments-and-cases.out').read_text()
forward=(A/'02-forward-audit.md').read_text();assert quote in forward
for p in ['00-running-log.md','02-forward-audit.md']:
 assert (A/p).read_bytes().startswith(git('show',BASE+':'+str((A/p).relative_to(R)))),('old report rewritten',p)
frozen=git('ls-tree','-r','--name-only',BASE,'--',str(A.relative_to(R))).decode().splitlines()
frozen=[p for p in frozen if Path(p).name not in ['00-running-log.md','02-forward-audit.md']]
for p in frozen:assert (R/p).read_bytes()==git('show',BASE+':'+p),p
selected=(A/'stage-a/p1-qa-scratch/paths.txt').read_text().replace(chr(92)+'u002d','-').splitlines()
assert len(selected)==107
assert git('ls-tree','-r','-z',BASE,'--',*selected)==git('ls-tree','-r','-z','HEAD','--',*selected)
assert not git('diff',BASE,'--','packages','projects','tools','scripts','*.patch','*.conf','.claude','AGENTS.md','CLAUDE.md','docs/decision-register.md')
changed=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
allowed={str((A/p).relative_to(R)) for p in ['00-running-log.md','02-forward-audit.md']}
allowed.update(['.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md'])
assert all(p in allowed or p.startswith(str(D.relative_to(R))+'/') for p in changed),'scope drift'
for p in changed:
 b=(R/p).read_bytes();assert ('mask'+'-data0').encode() not in b
 assert not re.search(rb'__'+rb'[A-Z0-9_]+'+rb'__',b),('unfilled placeholder',p)
for name,argv in [
 ('resolution',['tools/lint-audit-artifacts',str(A.relative_to(R))]),
 ('resolution-issue',['tools/lint-audit-artifacts',str(A.relative_to(R)),'--issue','1409']),
 ('lane-box',['tools/box-check','--issue','688']),
 ('audit-box',['tools/box-check','--issue','1409']),
 ('rules',['tools/rules-check','--quiet']),
 ('register',['tools/register-check']),
 ('index',['tools/work-log-index','--check']),
 ('ceremony',['tools/ceremony-check','--gate']),
 ('whitespace',['git','diff','--check',BASE])]:run(name,argv)
packet=b'\n'.join((R/p).read_bytes() for p in sorted(changed))
run('forbidden-new-records',['tools/forbidden-terms-check','--stdin'],stdin=packet)
out=run('secret-new-records',['bash','-c','. .githooks/secret-patterns; grep -a -c -E -e "'+chr(36)+'{SECRET_PATTERNS}"'],expected=1,stdin=packet)
assert out.strip()==b'0'
result=dict(result='PASS',start=start,end=stamp(),script_sha256=h(Path(__file__).read_bytes()),prior_tip=BASE,immutable_recipe_sha256=h(raw),frozen_audit_files_unchanged=len(frozen),selected_source_paths=107,all_product_source_unchanged=True,literal_assignments=10,literal_case_labels=5,accepted_execution_replayed=False,scope='Only new pins-read records and current resolution/record checks',checks=checks)
(D/'validation-final.json').write_text(json.dumps(result,indent=2)+'\n');(D/'validation-final-in-progress.json').unlink()
print('Pins-read current-record checks PASS;',len(frozen),'prior audit files unchanged')
