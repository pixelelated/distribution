#!/usr/bin/env python3
"""Check newly changed records; reconcile accepted bytes, never replay producers."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
A=Path(__file__).resolve().parents[1]; R=A.parents[2]; os.chdir(R)
os.environ.update(LC_ALL='C', TMPDIR='/workspace/tmp/m6-t41/tmp')
D=A/(sys.argv[1] if len(sys.argv)>1 else 'stage-f')
D.mkdir(exist_ok=True); (D/'checkers').mkdir(exist_ok=True)
BASE='c9fe606e8d7e7e0f6c70cc686764d1503029d278'
checks=[]
def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(b): return hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git',*args])
def run(name,args,expected=0,stdin=None):
    start=stamp(); tic=time.monotonic()
    p=subprocess.run(args,input=stdin,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
    f=D/'checkers'/(name+'.out'); f.write_bytes(p.stdout)
    checks.append(dict(name=name,argv=args,start=start,elapsed_seconds=round(time.monotonic()-tic,3),rc=p.returncode,output=str(f.relative_to(D)),sha256=h(p.stdout)))
    (D/'validation-in-progress.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(name,'rc',p.returncode,flush=True)
    assert p.returncode==expected,(name,p.stdout.decode(errors='replace')[-1800:])
    return p.stdout
start=stamp()
# Read-only linkage metadata uses gh: connector does not expose parent linkage.
audit=json.loads(run('audit-api',['gh','api','repos/pixelelated/distribution/issues/1409']))
bug=json.loads(run('bug-api',['gh','api','repos/pixelelated/distribution/issues/1408']))
parent=json.loads(run('audit-parent',['gh','api','repos/pixelelated/distribution/issues/1409/parent']))
assert parent['number']==688 and audit['state']=='open' and bug['state']=='open'
assert audit['body']==(A/'stage-e/audit-outcome.md').read_text()
assert bug['body']==(A/'stage-d/issues/0010-bug.md').read_text()
assert audit['milestone']['number']==6 and {x['name'] for x in audit['labels']}=={'audit','punch-list'}
assert bug['milestone'] is None and {x['name'] for x in bug['labels']}=={'bug'}
assert len(re.findall(r'^- \[x\]',audit['body'],re.M))==1
assert len(re.findall(r'^- \[ \]',bug['body'],re.M))==2 and not re.search(r'^- \[[xX]\]',bug['body'],re.M)
punch=(A/'05-punch-list.md').read_text()
assert punch in audit['body'] and '| PL-001 | Deferred |' in punch and 'outcome: deferred' in punch and 'follow_up: "#1408"' in punch
protected=[str((A/x).relative_to(R)) for x in ['stage-a','stage-b','stage-c','stage-d','tools','second-opinions']]
old=git('ls-tree','-r','--name-only',BASE,'--',*protected).decode().splitlines()
manifest=[]
for p in old:
    b=(R/p).read_bytes(); assert b==git('show',BASE+':'+p),p
    manifest.append(dict(path=p,sha256=h(b)))
(D/'accepted-file-identities.json').write_text(json.dumps(manifest,indent=2)+'\n')
paths=(A/'stage-a/p1-qa-scratch/paths.txt').read_text().replace(chr(92)+'u002d','-').splitlines()
assert len(paths)==107
for p in paths: assert (R/p).read_bytes()==git('show','d7dd766659:'+p)
assert not git('diff','d7dd766659','--','packages','projects','tools','scripts')
assert not git('diff',BASE,'--','.claude','AGENTS.md','CLAUDE.md','docs/decision-register.md','docs/reviews')
forward=(A/'02-forward-audit.md').read_text(); log=(A/'00-running-log.md').read_text()
assert (A/'stage-b/corrected/hygiene.out').read_text() in forward
for m in ['provenance','coverage']:
    assert (A/'stage-b/corrected'/('table-'+m+'.txt')).read_text().strip() in forward
assert re.findall(r'^\| (L-\d\d) \|',forward,re.M)==[f'L-{i:02d}' for i in range(1,32)]
assert re.findall(r'^\| ([a-p]) \|',forward,re.M)==list('abcdefghijklmnop')
assert len(re.findall('proved:',forward))==len(re.findall(r'^PROOF:',log,re.M))==12
plan=json.loads((A/'second-opinions/review-plan.json').read_text())
assert plan['reviewers']==[] and plan['primary']['model']=='openai/gpt-6-astra' and plan['tier_exception']=='D-WORKFLOW-184'
assert [x.name for x in (A/'second-opinions').iterdir()]==['review-plan.json']
changed=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
allow={str((A/x).relative_to(R)) for x in ['00-running-log.md','02-forward-audit.md','04-analysis.md','05-punch-list.md','06-audit-summary.md','07-questions-for-the-maintainer.md']}
allow.update(['.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md','docs/retros/2026-11-02-m6-patches-shipped-kernel.md'])
prefix=[str((A/x).relative_to(R))+'/' for x in ['stage-e','stage-f','stage-g','stage-h']]
assert all(p in allow or any(p.startswith(q) for q in prefix) for p in changed),'outside authorized records'
for p in changed:
    b=(R/p).read_bytes()
    assert ('mask'+'-data0').encode() not in b,('escaped filename lost',p)
    assert not re.search(rb'__' + rb'[A-Z0-9_]+' + rb'__',b),('placeholder',p)
for name,args in [
 ('lint-resolution',['tools/lint-audit-artifacts',str(A.relative_to(R))]),
 ('lint-resolution-issue',['tools/lint-audit-artifacts',str(A.relative_to(R)),'--issue','1409']),
 ('audit-box',['tools/box-check','--issue','1409']),
 ('bug-box',['tools/box-check','--issue','1408']),
 ('lane-box',['tools/box-check','--issue','688']),
 ('rules',['tools/rules-check','--quiet']),
 ('register',['tools/register-check']),
 ('index',['tools/work-log-index','--check']),
 ('ceremony',['tools/ceremony-check','--gate']),
 ('generator-syntax',['python3','-I','-X','pycache_prefix=/workspace/tmp/m6-t41/tmp/pycache-final','-m','py_compile',str(A.relative_to(R)/'tools/t41-tables.py')]),
 ('whitespace',['git','diff','--check',BASE])]:
    run(name,args)
packet=b'\n'.join((R/p).read_bytes() for p in sorted(changed))
run('forbidden-new-records',['tools/forbidden-terms-check','--stdin'],stdin=packet)
out=run('secret-new-records',['bash','-c','. .githooks/secret-patterns; grep -a -c -E -e "'+chr(36)+'{SECRET_PATTERNS}"'],expected=1,stdin=packet)
assert out.strip()==b'0'
result=dict(result='PASS',start=start,end=stamp(),script_sha256=h(Path(__file__).read_bytes()),scope='New final records and live issue checks; immutable accepted-byte reconciliation only, no accepted producer replay',structural=dict(accepted_files_unchanged=len(old),source_paths_unchanged=107,lead_rows=31,rulings=16,proofs=12,punch_outcome='Deferred',audit_checked=1,audit_state='open',bug_unchecked=2,bug_state='open',source_diff='empty'),checks=checks)
(D/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
(D/'validation-in-progress.json').unlink()
print('Final record checks PASS;',len(old),'accepted files unchanged')
