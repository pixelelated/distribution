import datetime, hashlib, json, os, pathlib, runpy, subprocess, sys, tempfile
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689')
A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped'
SEED='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1'
SOURCE='b6332dbc13f5929f05ec5ba23c44285c5ee56b38'
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def dump(p,o):write(p,json.dumps(o,indent=2,sort_keys=True)+'\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()==SEED
assert not subprocess.check_output(['git','status','--porcelain'],cwd=R)
for p,want in [('docs/reviews/briefs/patches-shipped.md','6601d6f9c6e2c548ee5c6d23a274169ccd3077923bc6fd0eb5e37aee59ada67a'),('docs/qa-logs/2026-11-02-m6-resume/t42-brief-inputs.py','e4bdc5204e523e93c7d7fd1f1ebc5f09b5722266ce576433acb57a50592991a0')]:assert sha((R/p).read_bytes())==want,p
A.mkdir(parents=True,exist_ok=False)
start=now()
write(A/'00-running-log.md',f'''# T42 patches-shipped running log (#689)

Started: {start}. Primary reader: Codex / openai/gpt-6-astra / xhigh, OpenAI.
Identity source: own live Herdr footer read in wN:p7; session 01a19d12-3d7a-7642-9108-ae06a719cdd7. Earlier T38 provenance is unchanged.
reviewed-at: {SEED}
Source baseline: {SOURCE}; P1: 2174265e9cc1b248c0fbe27fa101875984d46d6b.
Spec: docs/reviews/briefs/patches-shipped.md v2; dispatch #689 comment 6585520800.
Local provenance audit, D-WORKFLOW-184/225. No independent reviewer; no runtime result.

## Stage A — {start}

Read the dispatch, complete #689 thread and #1054 body, seed pointer, v2 brief, coordinator rules, code-auditor skill and Local methodology. The seed is clean and its parent is 07d01c898fba867e042342017fd8d5257508a28c. This lane executes continuously through D, then stops for coordinator disposition. It does not change criteria or product sources.

Can this be done on the VM? No — immutable source identity and provenance are host Git facts; runtime claims remain with their owners. No runtime is allocated.
''')
out=pathlib.Path(tempfile.mkdtemp(prefix='m6-t42-inputs.',dir='/tmp'))
receipts=[]
for name,ref in [('source',SOURCE),('seed',SEED)]:
 argv=[sys.executable,'docs/qa-logs/2026-11-02-m6-resume/t42-brief-inputs.py','--repo',str(R),'--ref',ref,'--out',str(out/name)]
 before=now();p=subprocess.run(argv,cwd=R,env={**os.environ,'LC_ALL':'C'},capture_output=True)
 write(A/f'stage-a/{name}.stdout',p.stdout.decode());write(A/f'stage-a/{name}.stderr',p.stderr.decode())
 receipts.append(dict(argv=argv,cwd=str(R),start=before,end=now(),rc=p.returncode,stdout_sha256=sha(p.stdout),stderr_sha256=sha(p.stderr)))
 dump(A/'stage-a/commands.json',receipts)
 assert p.returncode==0,name
 for f in (out/name).iterdir():
  target=A/'stage-a'/name/f.name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(f.read_bytes())
s=json.loads((out/'source/summary.json').read_text());t=json.loads((out/'seed/summary.json').read_text())
s.pop('ref');t.pop('ref');assert s==t
assert (out/'source/symlinks.json').read_bytes()==(out/'seed/symlinks.json').read_bytes()
write(A/'stage-a/comparison.out','PASS source/seed summary excluding only ref\nPASS symlinks.json byte equality\nPASS selector/native/referent identities against P1 (helper assertions)\n')
plan=dict(schema_version=1,depth='local',primary=dict(harness='Codex',model='openai/gpt-6-astra',lab='openai',effort='xhigh',identity_source='Own live Herdr footer in wN:p7, session 01a19d12-3d7a-7642-9108-ae06a719cdd7: GPT-6-Astra xhigh'),reviewers=[],tier_exception='D-WORKFLOW-184',reason='T42 is a source provenance table under plan 6c and D-WORKFLOW-225; no independent review or runtime claim.')
dump(A/'second-opinions/review-plan.json',plan)
fixture=pathlib.Path(tempfile.mkdtemp(prefix='m6-t42-local-',dir='/tmp'))/'2026_11_02-epic-t42-local-control'
mod=runpy.run_path(str(R/'tools/lint-audit-artifacts'))
proof=[]
for label,alter in [('missing-exception',True),('valid-local',False)]:
 candidate=dict(plan)
 if alter:candidate.pop('tier_exception')
 dump(fixture/'second-opinions/review-plan.json',candidate)
 bad=[];ok=[];mod['check_review_plan'](fixture,False,bad.append,ok.append)
 rc=int(bool(bad));assert rc==int(alter)
 proof.append(dict(case=label,rc=rc,fail=bad,ok=ok))
dump(A/'stage-a/local-lint-controls.json',proof)
write(A/'stage-a/local-lint-controls.out','FAIL missing-exception rc=1: local-only cannot satisfy Epic/Milestone\nPASS valid-local rc=0: real check_review_plan; no provider invocation\n')
dump(A/'stage-a/census.json',dict(start=start,end=now(),owner='m6-t5-build-engine',scope='source/record only',executed=['git immutable reads','Python input helper','real Local review-plan validator with isolated JSON fixture'],small_input_scratch=str(out),local_lint_scratch=str(fixture),source_extraction=None,build=0,compiler=0,guest=0,device_cloud=0,config_sourcing=0,fetch=0,provider_calls=0,host_ledger_writes=0,accepted_audit_replays=0,limits='This is the execution census for this lane only; no claim about unrelated host processes.'))
write(A/'01-research-notes.md',f'''# T42 research notes (#689)

Auditor: Codex / openai/gpt-6-astra / xhigh. Date: {start}.
Spec: docs/reviews/briefs/patches-shipped.md v2; reviewed-at {SEED}.

## Scope

Stage A input receipts under stage-a/ establish exactly 384 native paths, 71,387 logical Git-blob lines, 71,378 newline bytes and 3,809,748 bytes. Modes: 380 regular and four links. Reach: 379 shipped/five test. Twelve fork-written patches account for 498 lines. Native path-list SHA256: 91e980f455611fa81bc84c8ff5548abd05437452d02038cc5595f5c1521e5f07.

The separate inherited population is 50 keyed patch/override comparisons in 26 overrides. The other 24 T40 rows stay excluded. Native counts never include inherited questions. Symlink ownership remains with its native path; MangoHud's SM8750 referent stays T43 context.

## Rules and evidence boundary

Read coordinator copies of engineering-practices, packaging-and-patches, worktrees, issue-tracking, adversarial-council, decision-register, ceremonies, upgrade-and-install and vm-first; the current seed carries their coordinator versions. D-WORKFLOW-184/187/188/189/209/221/222/225 apply. The explicit dispatch and v2 brief govern the Local identity, no configuration sourcing and continuous A–D execution where historical generic methodology differs. No product/runtime action is authorized.

## Interactions

scripts/unpack:126–196 selects PATCH_ARCH, package/project/device directories, literal C order and the patch backend. x86_64 selects x86; normal patch input substitutes DEVICE/TARGET_CPU. config/functions resolves package overrides. T40 supplies questions rather than adoption verdicts. T8/T22/T27 own recipe changes, T41 owns its kernel/non-kernel table, and T3/T17 retain their patch rows. #1048/#346 own class removal; #585 receives drafts only.

## Research summary

Source/seed/P1 inputs match, including selectors and referents; no early immutable-input blocker. The real Local review-plan validator refuses a removed tier exception and accepts the actual identity. This tests the capability only, not completed audit artifacts. Readback: stage-a/local-lint-controls.json. Application and semantic tables are not yet completed; no application or runtime PASS is inferred from membership.
''')
with (A/'00-running-log.md').open('a') as f:f.write(f'\n### {now()} — A inputs and Local capability\n\nPROOF: A-01 (tool-run) — stage-a/comparison.out: source/seed summaries match excluding ref; symlinks match byte-for-byte; helper assertions bind native, selector and referent identities to P1. A differing mode/blob or selector would fail.\n\nPROOF: A-02 (tool-run) — stage-a/local-lint-controls.json: real validator rc=1 without tier exception, rc=0 with actual Local plan. No whole audit or external review claim.\n')
log=R/'docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md'
with log.open('a') as f:f.write(f'\n## {datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M UTC")} — #689 T42 Stage A source identity\n\nCodex / openai/gpt-6-astra / xhigh, T5 in wN:p7, began the explicit A–D dispatch at {SEED}. Native membership 384/71,387 logical lines and separate inherited 50/26 scope preserved. Source/seed/P1 native, selector and symlink-referent identities match; the real Local-plan validator fails without D-WORKFLOW-184 and passes with it. Receipts: docs/audits/2026_11_02-epic-m6-patches-shipped/stage-a/. No runtime, source edit or accepted-work replay. Next: source/provenance assessment through D, then coordinator disposition.\n')
pointer=R/'.github/sessions/saved-session-state-feature-m6-patches-shipped-689.md'
with pointer.open('a') as f:f.write(f'\n## Executor checkpoint — {now()}\n\nStage A input binding and Local validator capability are complete. Actual identity independently read from own footer: Codex / GPT-6-Astra / xhigh, session 01a19d12-3d7a-7642-9108-ae06a719cdd7. Audit folder docs/audits/2026_11_02-epic-m6-patches-shipped; source/seed comparisons and controls under stage-a/. Continue B through D without another approval; stop at published D. No application has been claimed, no runtime allocated, no product path changed.\n')
subprocess.run(['tools/work-log-index','--write'],cwd=R,check=True)
print('PASS Stage A source/seed/P1 inputs and Local validator capability; records written',A)
