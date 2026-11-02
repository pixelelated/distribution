#!/usr/bin/env python3
"""Produce only the post-acceptance completion records from live tracker/Git reads."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,time
R=Path.cwd();A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped-kernel';D=A/'completion'
ACCEPTED='e481e4a4a5c296c8f12e9654b6a45c4fb27bd3b0';COORD='8b83e452459f6696ac959b4e4e5494701d5d2f93'
SEED='d7dd76665983cb87dba62397691500fcf409fafe'
assert set(os.sched_getaffinity(0))==set(range(8,24))
os.environ.update(LC_ALL='C',TMPDIR='/workspace/tmp/m6-t41/tmp')
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args])
assert git('rev-parse','HEAD').decode().strip()==ACCEPTED
assert not git('diff','--name-only') and not git('diff','--cached','--name-only'),'tracked start must be clean'
assert all(p.startswith(str((A/'completion').relative_to(R))+'/') for p in git('ls-files','--others','--exclude-standard').decode().splitlines())
assert D.exists() and {p.name for p in D.iterdir()}=={'initial-read'},'only preserved initial read may exist'
(D/'produce.py').write_bytes(Path(__file__).read_bytes())
commands=[]
def read(label,argv):
 start=stamp();tic=time.monotonic();p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
 (D/(label+'.stdout')).write_bytes(p.stdout);(D/(label+'.stderr')).write_bytes(p.stderr)
 commands.append(dict(label=label,argv=argv,cwd=str(R),cpu_affinity=sorted(os.sched_getaffinity(0)),start=start,end=stamp(),elapsed_seconds=round(time.monotonic()-tic,6),rc=p.returncode,stdout=label+'.stdout',stderr=label+'.stderr',stdout_sha256=h(p.stdout),stderr_sha256=h(p.stderr)))
 (D/'read-commands-in-progress.json').write_text(json.dumps(commands,indent=2)+'\n')
 assert p.returncode==0 and not p.stderr,(label,p.returncode)
 return p.stdout
# Existing schema-1 validator requires the raw REST number/state shape.
audit_raw=read('audit-1409',['gh','api','repos/pixelelated/distribution/issues/1409']);audit=json.loads(audit_raw)
lane_raw=read('lane-688',['gh','api','repos/pixelelated/distribution/issues/688']);lane=json.loads(lane_raw)
bug_raw=read('bug-1408',['gh','api','repos/pixelelated/distribution/issues/1408']);bug=json.loads(bug_raw)
assert audit['number']==1409 and audit['state']=='closed' and audit['state_reason']=='completed'
expected_audit=json.loads(Path('/workspace/tmp/m6-t41/tmp/expected-closed-audit.json').read_text())
assert audit['body']==expected_audit['body'] and audit['state']==expected_audit['state'] and audit['state_reason']==expected_audit['state_reason']
(D/'connector-audit-readback.json').write_text(json.dumps(expected_audit,indent=2)+'\n')
assert '6588269141' in audit['body']
assert len(re.findall(r'^- \[x\]',audit['body'],re.M))==1 and not re.search(r'^- \[ \]',audit['body'],re.M)
assert lane['state']=='open' and len(re.findall(r'^- \[x\]',lane['body'],re.M))==28 and not re.search(r'^- \[ \]',lane['body'],re.M)
assert re.search(r'^reviewed-at: '+SEED+r'$',lane['body'],re.M) and re.search(r'^fixed-at: '+ACCEPTED+r'$',lane['body'],re.M)
assert bug['state']=='open' and bug['body']==(A/'stage-d/issues/0010-bug.md').read_text()
assert len(re.findall(r'^- \[ \]',bug['body'],re.M))==2 and not re.search(r'^- \[[xX]\]',bug['body'],re.M)
verified=stamp()
(A/'tracker-final-readback.json').write_bytes(audit_raw)
(D/'issue-688-readback.json').write_bytes(lane_raw);(D/'issue-1408-readback.json').write_bytes(bug_raw)
tracker=dict(result='PASS',exact_bodies_and_states=True,closed_completed=[1409],verified_utc=verified,closed_at=audit['closed_at'],audit_body_sha256=h(audit['body'].encode()),lane_state='open',lane_checked=28,reviewed_at=SEED,fixed_at=ACCEPTED,bug_state='open',bug_open_criteria=2,bug_body_unchanged=True,cpu_affinity=sorted(os.sched_getaffinity(0)),reader=dict(harness='Codex',model='GPT-6-Astra',effort='xhigh',session='01a19d12-29e3-7fe0-9f41-038dac0a5deb',lane='m6-t3-emulators',pane='wN:p6',identity_basis='observed footer; not provider-attested'))
(A/'tracker-completion.json').write_text(json.dumps(tracker,indent=2)+'\n')
source='docs/qa-logs/2026-11-02-m6-resume/t41-final-acceptance.md'
acceptance=read('coordinator-acceptance',['git','show',COORD+':'+source]);(D/'coordinator-acceptance.md').write_bytes(acceptance)
authority=json.loads(Path('/workspace/tmp/m6-t41/tmp/completion-authority.json').read_text())
assert authority['id']==6588269141
(D/'authority-comment.json').write_text(json.dumps(authority,indent=2)+'\n')
(D/'acceptance-record.json').write_text(json.dumps(dict(accepted_tip=ACCEPTED,reviewed_seed=SEED,coordinator_ref=COORD,coordinator_record_path=source,record_sha256=h(acceptance),acceptance_comment=6588269141,full_final_run=dict(pass_count=53,fail_count=1,rc=1,original_result_preserved=True),separate_corrected_issue_body_gate='PASS',second_whole_suite_run=False,actual_command_receipts=4892,packet_sha256='29939223f31ed84605de318069f8820e040215bbf9cc3dcf2122925a47f7548b',simulated_coordinator='afdec2bf8b88135befcb7ec56efb3a7ea327bd73',actual_ordered_integration='not performed; coordinator-owned',tracker_verified_utc=verified,scope='Coordinator acceptance read and attributed; no accepted producer or final-suite replay'),indent=2)+'\n')
(D/'read-commands.json').write_text(json.dumps(dict(commands=commands,produced_at=stamp(),cpu_affinity=sorted(os.sched_getaffinity(0))),indent=2)+'\n')
(D/'read-commands-in-progress.json').unlink()
evidence=[A/'04-analysis.md',A/'05-punch-list.md',A/'tracker-final-readback.json',A/'tracker-completion.json',D/'coordinator-acceptance.md',D/'authority-comment.json',D/'acceptance-record.json',D/'issue-688-readback.json',D/'issue-1408-readback.json',D/'read-commands.json']
marker=dict(schema=1,issue=1409,completed_at=verified,tracker_readback=str((A/'tracker-final-readback.json').relative_to(R)),tracker_completion=str((A/'tracker-completion.json').relative_to(R)),evidence={str(p.relative_to(R)):h(p.read_bytes()) for p in evidence})
(A/'audit-completion.json').write_text(json.dumps(marker,indent=2)+'\n')
now=stamp()
entry=f"""
## Accepted audit completion record — {now}

Full #688 comment 6588269141 and coordinator {COORD}:docs/qa-logs/2026-11-02-m6-resume/t41-final-acceptance.md read. Accepted source-preserving tip is {ACCEPTED}, reviewed seed {SEED}. Live audit #1409 closed/completed at {audit['closed_at']}; exact current Deferred-outcome body/state verified at {verified}. tracker-final-readback.json and tracker-completion.json retain that receipt; audit-completion.json uses the existing schema1 with real SHA256 bindings to 04/05, tracker and acceptance evidence.

Coordinator acceptance retains the full run as 53 PASS / one reader FAIL / rc1, plus the separately corrected live issue-body gate PASS; no second complete run or rewritten result is claimed. The published acceptance preserves 4892 actual command receipts and the successful disposable integration; this lane reads that record without replay. Root owns actual ordered integration.

#688 remains open with all28 criteria checked; accepted source header pins stay seed/e481. High #1408 remains open/unfixed with its unchanged body and two unchecked source-fix criteria; PL-001 remains Deferred to integration #563/#559, never waived. T11 storage choice, D-SYS-004 distribution-layer ramoops and both never-sent drafts remain unchanged. All accepted source/program/A–H receipts and historical identities are preserved.

Actual Codex / GPT-6-Astra / xhigh, T3 wN:p6, session01a19d12-29e3-7fe0-9f41-038dac0a5deb; observed footer, not provider-attested. All local commands and their children are pinned to CPUs8–23 (actual affinity retained). Can this be done on the VM? No: this is completion bookkeeping against immutable records and live tracker state. No accepted replay, new merge, host/runtime/provider/device/cloud or other-owner action, and no permission answer. New completion-record lints/checks follow; normal commit/push and one published completion handback, then stop. #688 closure remains coordinator-owned.
"""
(A/'00-running-log.md').open('a').write(entry);(A/'06-audit-summary.md').open('a').write(entry)
p=R/'.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md';s=p.read_text()
s=re.sub(r'(?m)^> \*\*Last updated:\*\*.*$', '> **Last updated:** '+now+' by Codex / GPT-6-Astra / xhigh, T3 wN:p6; observed footer, not provider-attested.',s)
s=re.sub(r'^## Current focus .*$', '## Current focus — T41 accepted; publish completion record then stop',s,flags=re.M)
a=s.index('## Immediate next action');b=s.index('## Merge notes',a)
s=s[:a]+f"""## Immediate next action — completion-record publication, then stop

T41 is accepted at {ACCEPTED} by full #688 comment6588269141, with immutable coordinator evidence {COORD}:docs/qa-logs/2026-11-02-m6-resume/t41-final-acceptance.md. Audit #1409 is closed/completed; exact verified readback and schema1 marker are at the audit root. The completion packet is under completion/, with current check receipts at completion/validation.json.

Run only new completion-record checks, commit/push normally, and return one clean records-only completion tip/checkpoint to m6-coordinator wN:p2. Keep #688 open and preserve its accepted seed/e481 header pins. After publication stop: actual ordered integration and #688 closure remain coordinator-owned. The full acceptance run remains53 PASS/one reader FAIL/rc1; the separately corrected issue-body gate PASS reconciles that one predicate, not a second full-suite run.

No source/program/accepted A–H receipt or historical-identity change. No accepted replay/new merge/host/runtime/provider/device/cloud/other-owner action or permission answer. All local commands pinned CPUs8–23 for the separate M7 window. PL-001 remains Deferred; High #1408 open/unfixed with two unchecked fix criteria, integration #563/#559 owns uptake. T11 storage decision and never-sent distribution-layer ramoops draft persist. If Herdr is blocked, retain the result on #688 and leave owner input untouched.

"""+s[b:]
s+='\n- **Accepted completion record** ('+now+'): #1409 closed/completed readback and real schema1 evidence hashes retained; #688 all28checked/open with accepted seed/e481 headers unchanged. Completion-only publication, then stop for root-owned integration.\n';p.write_text(s)
p=R/'docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md';p.open('a').write('\n## '+now+' — #688 T41 accepted audit completion record\n\nCoordinator accepted e481 in full comment6588269141, published at8b83e452459f6696ac959b4e4e5494701d5d2f93. Exact live #1409 closed/completed readback and verification time retained with schema1 marker and actual evidence hashes. #688 remains open/all28checked with seed/e481 headers; High #1408 unchanged/open/two unchecked criteria. Original53PASS/one readerFAIL/rc1 plus separate corrected-gate PASS preserved as attributed acceptance, not another suite run. Commands pinned CPUs8–23. Only completion records/pointer/log/summary and new checks; no accepted replay, source, merge or runtime action. Normal clean completion publication then stop; ordered integration/688closure remain coordinator-owned.\n')
print('Completion marker written; verified UTC',verified)
print('Audit closed_at',audit['closed_at'],'CPU affinity',sorted(os.sched_getaffinity(0)))
