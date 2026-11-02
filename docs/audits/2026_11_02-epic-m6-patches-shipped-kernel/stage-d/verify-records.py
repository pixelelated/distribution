#!/usr/bin/env python3
"""Verify new Stage-D records; never run the generator, application or source helpers."""
from pathlib import Path
import collections,datetime,hashlib,json,os,re,subprocess,time
D=Path(__file__).resolve().parent;A=D.parent;R=A.parents[2];os.chdir(R);os.environ['LC_ALL']='C';os.environ['TMPDIR']='/workspace/tmp/m6-t41/tmp'
START='94b5b1c0b983313325dba101217761c6e5c9bca0';checks=[]
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args])
def run(name,args,expected=0):
 start=stamp();tic=time.monotonic();p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);f=D/'checkers'/(name+'.out');f.write_bytes(p.stdout);r={'name':name,'argv':args,'start':start,'elapsed_seconds':round(time.monotonic()-tic,3),'rc':p.returncode,'output':str(f.relative_to(D)),'sha256':h(p.stdout)};checks.append(r);(D/'validation-in-progress.json').write_text(json.dumps(checks,indent=2)+'\n');assert p.returncode==expected,(name,p.returncode,p.stdout.decode()[-2000:]);print(name,'rc',p.returncode,flush=True);return p.stdout
start=stamp();tic=time.monotonic()
args=['gh','api','repos/pixelelated/distribution/issues/1409'];raw=run('audit-final-api',args);(D/'issue-1409-final-readback.json').write_bytes(raw);audit=json.loads(raw)
assert audit['body']==(D/'issues/audit-final.md').read_text() and audit['state']=='open'
assert audit['milestone']['number']==6 and audit['milestone']['title']=='M6: Codebase renovation' and {x['name'] for x in audit['labels']}=={'audit','punch-list'}
bug=json.loads((D/'issue-1408-readback.json').read_text());assert bug['body']==(D/'issues/0010-bug.md').read_text() and bug['milestone'] is None and {x['name'] for x in bug['labels']}=={'bug'}
assert json.loads((D/'audit-parent-readback.json').read_text())['number']==688
absent=json.loads((D/'bug-parent-readback.json').read_text());assert absent['status']=='404' and absent['message']=='No parent issue found'
for i,cid in [(1,6585346506),(2,6585347732)]:
 q=json.loads((D/f'question-{i}-readback.json').read_text());assert q['id']==cid and q['body']==(D/'issues'/f'question-{i}.md').read_text()
 assert str(cid) in (A/'07-questions-for-the-maintainer.md').read_text() and str(cid) in (A/'02-forward-audit.md').read_text()
protected=[str((A/p).relative_to(R)) for p in ['stage-a','stage-b','stage-c','tools','second-opinions']]
old=git('ls-tree','-r','--name-only',START,'--',*protected).decode().splitlines()
for p in old:assert (R/p).read_bytes()==git('show',START+':'+p),('protected audit record changed',p)
paths=(A/'stage-a/p1-qa-scratch/paths.txt').read_text().replace(chr(92)+'u002d','-').splitlines();assert len(paths)==107
for p in paths:assert (R/p).read_bytes()==git('show',START+':'+p)
assert not git('diff','d7dd766659','--','*.patch','*.conf','packages','projects','tools','scripts')
assert not git('diff',START,'--','docs/decision-register.md','AGENTS.md','CLAUDE.md','.claude','docs/reviews')
forward=(A/'02-forward-audit.md').read_text();log=(A/'00-running-log.md').read_text();analysis=(A/'04-analysis.md').read_text();punch=(A/'05-punch-list.md').read_text()
assert (A/'stage-b/corrected/hygiene.out').read_text() in forward
for mode in ['provenance','coverage']:assert (A/'stage-b/corrected'/f'table-{mode}.txt').read_text().strip() in forward
assert len(re.findall(r'proved:',forward))==len(re.findall(r'^PROOF:',log,re.M))==12
assert re.findall(r'^\| (L-\d\d) \|',forward,re.M)==[f'L-{i:02d}' for i in range(1,32)]
assert re.findall(r'^\| ([a-p]) \|',forward,re.M)==list('abcdefghijklmnop')
score=json.loads((D/'scorecard.json').read_text());assert len(score)==28 and collections.Counter(x[1] for x in score)=={'PASS':20,'PARTIAL':8}
for i,(title,status,detail) in enumerate(score,1):
 row=f'| AC-{i:02d} | {title} | {status} | {detail} |';assert row in forward and row in analysis and row in audit['body']
assert re.findall(r'^## (PL-\d+)',punch,re.M)==['PL-001']
assert '| PL-001 | Open |' in punch and 'outcome: open' in punch and not re.search(r'outcome: (resolved|deferred|withdrawn)',punch)
assert len(re.findall(r'^- \[ \]',audit['body'],re.M))==1 and not re.search(r'^- \[[xX]\]',audit['body'],re.M)
assert len(re.findall(r'^- \[ \]',bug['body'],re.M))==2
plan=json.loads((A/'second-opinions/review-plan.json').read_text());assert plan['primary']['model']=='openai/gpt-6-astra' and plan['primary']['lab']=='openai' and plan['reviewers']==[] and plan['tier_exception']=='D-WORKFLOW-184'
assert [p.name for p in (A/'second-opinions').iterdir()]==['review-plan.json']
for name in ['06-audit-summary.md','07-questions-for-the-maintainer.md']:assert (A/name).stat().st_size>1000
changed=set(git('diff','--name-only',START).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
allow={str((A/p).relative_to(R)) for p in ['00-running-log.md','02-forward-audit.md','04-analysis.md','05-punch-list.md','06-audit-summary.md','07-questions-for-the-maintainer.md']}
allow|={'.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md'}
assert all(p in allow or p.startswith(str(D.relative_to(R))+'/') for p in changed),'outside D scope'
for p in sorted(changed):
 b=(R/p).read_bytes();assert ('mask'+'-data0').encode() not in b,('filename escape lost',p)
structural={'start':start,'elapsed_seconds':round(time.monotonic()-tic,3),'rc':0,'accepted_records_tools_plan_unchanged':len(old),'source_paths_unchanged':107,'proofs':12,'lead_rows':31,'rulings':16,'criterion_verdicts':{'PASS':20,'PARTIAL':8},'punch_items':1,'punch_outcome':'Open','issue_bodies_equal':True,'questions_equal':True,'audit_parent':688,'bug_parent':None,'protected_source_diff':'empty','scope':'Only D audit records/pointer/work-log changes'}
print('Structural record check PASS:',len(old),'accepted records/tools/plan unchanged',flush=True)
run('audit-box-final',['tools/box-check','--issue','1409'])
run('pre-issue-lint-final',['tools/lint-audit-artifacts',str(A.relative_to(R)),'--phase','pre-issue','--issue','1409'])
for name,args in [('rules',['tools/rules-check','--quiet']),('register',['tools/register-check']),('index',['tools/work-log-index','--check']),('ceremony',['tools/ceremony-check','--gate']),('whitespace',['git','diff','--check',START])]:run(name,args)
# New-record hygiene only. Positive controls are accepted B evidence quoted in 02, not replayed.
newfiles=sorted(p for p in changed if (R/p).is_file())
packet=b'\n'.join((R/p).read_bytes() for p in newfiles)
t=stamp();t0=time.monotonic();p=subprocess.run(['tools/forbidden-terms-check','--stdin'],input=packet,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);assert p.returncode==0;f=D/'checkers/forbidden-new-records.out';f.write_bytes(p.stdout);checks.append({'name':'forbidden-new-records','argv':['tools/forbidden-terms-check','--stdin'],'start':t,'elapsed_seconds':round(time.monotonic()-t0,3),'rc':p.returncode,'output':str(f.relative_to(D)),'sha256':h(p.stdout)});print(p.stdout.decode().strip(),flush=True)
t=stamp();t0=time.monotonic();args=['bash','-c','. .githooks/secret-patterns; grep -a -c -E -e "${SECRET_PATTERNS}"'];p=subprocess.run(args,input=packet,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);assert p.returncode==1 and p.stdout.strip()==b'0';f=D/'checkers/secret-new-records.out';f.write_bytes(p.stdout);checks.append({'name':'secret-new-records','argv':args,'start':t,'elapsed_seconds':round(time.monotonic()-t0,3),'rc':p.returncode,'meaning':'grep no-match, zero matching lines; positive control retained at B','output':str(f.relative_to(D)),'sha256':h(p.stdout)})
result={'result':'PASS','start':start,'end':stamp(),'script_sha256':h(Path(__file__).read_bytes()),'scope':'New D filing records only; no accepted-stage execution replay','structural':structural,'checks':checks}
(D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');(D/'validation-in-progress.json').unlink();print('Stage-D record verification PASS',flush=True)
