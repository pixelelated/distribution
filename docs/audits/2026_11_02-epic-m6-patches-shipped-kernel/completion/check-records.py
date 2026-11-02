#!/usr/bin/env python3
"""New completion-record checks only; preserve accepted source and execution receipts."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,time
D=Path(__file__).resolve().parent;A=D.parent;R=A.parents[2];os.chdir(R)
BASE='e481e4a4a5c296c8f12e9654b6a45c4fb27bd3b0';COORD='8b83e452459f6696ac959b4e4e5494701d5d2f93'
assert set(os.sched_getaffinity(0))==set(range(8,24))
os.environ.update(LC_ALL='C',TMPDIR='/workspace/tmp/m6-t41/tmp')
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args])
assert not (D/'validation.json').exists()
(D/'checkers').mkdir();checks=[]
def run(name,argv,expected=0,stdin=None):
 start=stamp();tic=time.monotonic();p=subprocess.run(argv,input=stdin,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
 dest=D/'checkers'/(name+'.out');dest.write_bytes(p.stdout)
 checks.append(dict(name=name,argv=argv,cwd=str(R),cpu_affinity=sorted(os.sched_getaffinity(0)),start=start,end=stamp(),elapsed_seconds=round(time.monotonic()-tic,6),rc=p.returncode,stdout=str(dest.relative_to(D)),sha256=h(p.stdout)))
 (D/'validation-in-progress.json').write_text(json.dumps(checks,indent=2)+'\n')
 print(name,'rc',p.returncode,flush=True);assert p.returncode==expected,(name,p.stdout.decode(errors='replace')[-1500:])
 return p.stdout
start=stamp();frozen=[]
old=git('ls-tree','-r','--name-only',BASE,'--',str(A.relative_to(R))).decode().splitlines()
changed_reports={str((A/x).relative_to(R)) for x in ['00-running-log.md','06-audit-summary.md']}
for p in old:
 b=(R/p).read_bytes();prior=git('show',BASE+':'+p)
 if p in changed_reports:assert b.startswith(prior),p
 else:
  assert b==prior,p;frozen.append(dict(path=p,sha256=h(b)))
(D/'accepted-file-identities.json').write_text(json.dumps(frozen,indent=2)+'\n')
assert not git('diff',BASE,'--','packages','projects','tools','scripts','*.patch','*.conf','.claude','AGENTS.md','CLAUDE.md','docs/decision-register.md','docs/reviews')
paths=(A/'stage-a/p1-qa-scratch/paths.txt').read_text().replace(chr(92)+'u002d','-').splitlines();assert len(paths)==107
for p in paths:assert (R/p).read_bytes()==git('show',BASE+':'+p)
assert (D/'coordinator-acceptance.md').read_bytes()==git('show',COORD+':docs/qa-logs/2026-11-02-m6-resume/t41-final-acceptance.md')
marker=json.loads((A/'audit-completion.json').read_text());tracker=json.loads((A/'tracker-completion.json').read_text());audit=json.loads((A/'tracker-final-readback.json').read_text())
assert marker['schema']==1 and marker['issue']==1409 and marker['completed_at']==tracker['verified_utc']
assert audit['body']==json.loads((D/'connector-audit-readback.json').read_text())['body']
assert audit['state']=='closed' and audit['state_reason']=='completed' and tracker['closed_at']==audit['closed_at']
for p,digest in marker['evidence'].items():assert h((R/p).read_bytes())==digest
lane=json.loads((D/'issue-688-readback.json').read_text());bug=json.loads((D/'issue-1408-readback.json').read_text())
assert lane['state']=='open' and len(re.findall(r'^- \[x\]',lane['body'],re.M))==28
assert re.search(r'^fixed-at: '+BASE+r'$',lane['body'],re.M)
assert re.search(r'^reviewed-at: d7dd76665983cb87dba62397691500fcf409fafe$',lane['body'],re.M)
assert bug['state']=='open' and bug['body']==(A/'stage-d/issues/0010-bug.md').read_text() and len(re.findall(r'^- \[ \]',bug['body'],re.M))==2
changed=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
allow=changed_reports|{str((A/x).relative_to(R)) for x in ['audit-completion.json','tracker-final-readback.json','tracker-completion.json']}
allow.update(['.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md'])
assert all(p in allow or p.startswith(str(D.relative_to(R))+'/') for p in changed),'completion scope drift'
for p in changed:
 b=(R/p).read_bytes();assert ('mask'+'-data0').encode() not in b,('escaped path lost',p)
 assert not re.search(rb'__'+rb'[A-Z0-9_]+'+rb'__',b),('unfilled placeholder',p)
validator="import runpy,datetime; from pathlib import Path; m=runpy.run_path('tools/ceremony-check'); ended,issue=m['completed_audit_marker'](Path('"+str((A/'audit-completion.json').relative_to(R))+"'),Path.cwd(),datetime.datetime.now(datetime.timezone.utc)); print('schema1 completion marker PASS',issue,ended.isoformat())"
for name,argv in [
 ('marker-validator',['python3','-I','-c',validator]),
 ('resolution',['tools/lint-audit-artifacts',str(A.relative_to(R))]),
 ('resolution-issue',['tools/lint-audit-artifacts',str(A.relative_to(R)),'--issue','1409']),
 ('audit-box',['tools/box-check','--issue','1409']),
 ('lane-box',['tools/box-check','--issue','688']),
 ('bug-box',['tools/box-check','--issue','1408']),
 ('rules',['tools/rules-check','--quiet']),
 ('register',['tools/register-check']),
 ('index',['tools/work-log-index','--check']),
 ('ceremony-full',['tools/ceremony-check']),
 ('ceremony-gate',['tools/ceremony-check','--gate']),
 ('whitespace',['git','diff','--check',BASE])]:run(name,argv)
packet=b'\n'.join((R/p).read_bytes() for p in sorted(changed))
run('forbidden-new-records',['tools/forbidden-terms-check','--stdin'],stdin=packet)
out=run('secret-new-records',['bash','-c','. .githooks/secret-patterns; grep -a -c -E -e "'+chr(36)+'{SECRET_PATTERNS}"'],expected=1,stdin=packet);assert out.strip()==b'0'
v=dict(result='PASS',start=start,end=stamp(),script_sha256=h(Path(__file__).read_bytes()),accepted_tip=BASE,cpu_affinity=sorted(os.sched_getaffinity(0)),frozen_audit_files_unchanged=len(frozen),source_paths_unchanged=107,marker_issue=1409,verified_utc=marker['completed_at'],accepted_headers_preserved=True,high_bug_unchanged=True,accepted_execution_replayed=False,scope='Only new completion-record checks; existing schema1 validator and full ceremony check, not accepted producer replay',checks=checks)
(D/'validation.json').write_text(json.dumps(v,indent=2)+'\n');(D/'validation-in-progress.json').unlink()
print('Completion record checks PASS;',len(frozen),'accepted audit files unchanged')
