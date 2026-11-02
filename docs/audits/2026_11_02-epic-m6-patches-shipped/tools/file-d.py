import pathlib,subprocess,json,hashlib,datetime,re
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689');A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped';D=A/'stage-d';D.mkdir(exist_ok=True);receipts=[]
def run(name,argv,expected=0):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(argv,cwd=R,capture_output=True);(D/(name+'.stdout')).write_bytes(p.stdout);(D/(name+'.stderr')).write_bytes(p.stderr);receipts.append({'name':name,'utc':t,'argv':argv,'cwd':str(R),'rc':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()});(D/'issue-commands.json').write_text(json.dumps(receipts,indent=2)+'\n');assert p.returncode==expected,(name,p.stdout.decode(),p.stderr.decode());return p.stdout
assert 'PASS pre-issue artifacts (does not certify resolution)' in (A/'stage-c/pre-issue-lint.stdout').read_text()
assert not any((D/f).exists() for f in ['issues.json','created-bug.json','created-audit.json']),'refuse duplicate or partially completed issue creation'
search=json.loads(run('duplicate-search',['gh','issue','list','--repo','pixelelated/distribution','--state','all','--search','"007-disable-home-pause" in:body','--json','number,title,state']));assert not search,'review existing exact-name report before filing'
(D/'bug-body.md').write_bytes(pathlib.Path('/tmp/m6-t42-bug.md').read_bytes())
bugurl=run('create-bug',['gh','issue','create','--repo','pixelelated/distribution','--title','ppsspp-sa: home-pause patch creates a nested patch instead of changing SDL','--label','bug','--body-file',str(D/'bug-body.md')]).decode().strip();bug=int(bugurl.rsplit('/',1)[1]);(D/'created-bug.json').write_text(json.dumps({'number':bug,'url':bugurl})+'\n')
punch=(A/'05-punch-list.md').read_text();index=punch.split('```yaml\n',1)[1].split('```',1)[0]
body=f'''Local audit of T42 #689, M6.P2 under area #1054. **1 finding: 0 Critical, 0 High, 1 Medium.** The native 384-path provenance/coverage population is separate from the 50 inherited comparisons / 26 overrides.

Primary reader: Codex / GPT-6-Astra / xhigh, OpenAI, T5 wN:p7, session 01a19d12-3d7a-7642-9108-ae06a719cdd7. Reviewers: []; Local under D-WORKFLOW-184/225. reviewed-at: 9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1. No external review or runtime result.

Artifact root: `docs/audits/2026_11_02-epic-m6-patches-shipped/` on `feature/m6-patches-shipped-689`; the clean immutable D tip will be linked in the #689 publication checkpoint. 02 carries all tables/receipts; 03 conformance and refutation; 04 Q1–Q7 and final-criteria limits; 05 punch details; 06/07 D summary and owner choices.

## Finding and route proposed

PL-01 / F-T42-01: Q3, Bug, Medium. PPSSPP007 outer diff adds a nested .patch; its intended SDL hunk remains text. Source trace: seed patch lines 11–29, recipe post_unpack and scripts/unpack:191–196. Constructed fixture normal rc 0 creates the nested file with unchanged SDL sentinel; this is not an application-at-pin or runtime claim. Reactive bug **#{bug}** holds the exact trace and observable criteria; it has no milestone/parent and remains open.

Already written: the selected outer patch leaves the original SDL mapping and an inert file in build source; it does not write player settings or cloud data. A future correction rebuilds the affected binary while preserving `/storage`.

Can this be done on the VM? Source/format facts are host source-fixture facts. Later input behavior can be exercised in GENERIC_X64 without a named physical exception; no runtime is allocated here.

Enforcement ladder: written/routed patch intent → audited source-target regression. Next mechanism: coordinator assigns a separate PPSSPP fix brief that first fails on the wrapper, then proves the selected direct source change and no nested target. Fixed upstream maps GUIDE to NKCODE_GUIDE while the nested seed payload requests NKCODE_UNKNOWN; the owner must resolve that intent before importing it. A narrow product-patch target guard can cover siblings with intentional exceptions. No production guard or source fix is made by this audit.

## Acceptance criteria

- [ ] PL-01 has a coordinator-approved Phase-7 disposition with evidence and owner in 05's table and matching punch_index; #{bug} retains its truthful state until its own implementation/acceptance completes.
- [ ] Final resolution `tools/lint-audit-artifacts` passes normally and with this audit issue, with actual outputs retained after disposition.
- [ ] The coordinator verifies the clean published source-preserving packet and records #689's acceptance under its integration convention.

## Bounded results

Native worst-per-plan application: 151 applies, 38 offset, 22 fuzz, 173 explicit open items. 760 recorded normal/diagnostic pairs and 116 safe cached-source target projections are checked; two link-creating UCM candidate exits were not serialized and are unclaimed. No whole-component/runtime/efficiency PASS. Inherited: 21 already-carried, seven not-applicable with individual reasons, 22 owner-specific missing inputs. Those existing comparison questions are not extra bugs. All twelve fork-written members / 498 lines were read; #585 contributions remain drafts in the packet.

Four table-corruption controls fail their own assertions; working and committed-then-reverted source edits fail protected-path fixtures. Literal pre-issue result before filing: `PASS pre-issue artifacts (does not certify resolution)`. Stage D stops for coordinator disposition; no E–H or source remediation is assumed.

```yaml
{index}```
'''
(D/'audit-body.md').write_text(body)
auditurl=run('create-audit',['gh','issue','create','--repo','pixelelated/distribution','--title','Audit: M6 T42 patches shipped - 1 finding (0 critical, 0 high)','--label','audit','--label','punch-list','--milestone','M6: Codebase renovation','--body-file',str(D/'audit-body.md')]).decode().strip();audit=int(auditurl.rsplit('/',1)[1]);(D/'created-audit.json').write_text(json.dumps({'number':audit,'url':auditurl})+'\n')
a=json.loads(run('audit-rest',['gh','api',f'repos/pixelelated/distribution/issues/{audit}']))
run('attach-audit',['gh','api','-X','POST','repos/pixelelated/distribution/issues/689/sub_issues','-F','sub_issue_id='+str(a['id'])])
a=json.loads(run('audit-readback',['gh','api',f'repos/pixelelated/distribution/issues/{audit}']));b=json.loads(run('bug-readback',['gh','api',f'repos/pixelelated/distribution/issues/{bug}']));ap=json.loads(run('audit-parent',['gh','api',f'repos/pixelelated/distribution/issues/{audit}/parent']));bp=json.loads(run('bug-parent',['gh','api',f'repos/pixelelated/distribution/issues/{bug}/parent'],expected=1))
assert a['milestone']['number']==6 and {x['name'] for x in a['labels']}=={'audit','punch-list'} and ap['number']==689
assert b['milestone'] is None and bp.get('status')=='404' and b['state']=='open' and {x['name'] for x in b['labels']}=={'bug'}
issues={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'audit':audit,'audit_url':auditurl,'audit_parent':689,'audit_milestone':6,'bug':bug,'bug_url':bugurl,'bug_parent':None,'bug_milestone':None,'bug_state':'open','finding_count':1,'critical':0,'high':0,'medium':1};(D/'issues.json').write_text(json.dumps(issues,indent=2)+'\n')
punch=punch.replace('Reactive bug issue is linked in the D readback.',f'Reactive bug: #{bug}; audit child: #{audit}. Both readbacks are in stage-d/.').replace('reactive bug remains open.',f'reactive bug #{bug} remains open. Audit child #{audit}.')
(A/'05-punch-list.md').write_text(punch)
with (A/'00-running-log.md').open('a') as f:f.write('\n### '+issues['utc']+f' — D issue custody\n\nPROOF: D-01 (tracker-readback) — reactive bug #{bug} filed with no parent/milestone, state open; audit #{audit} attached under #689/M6 with exactly one Medium finding and matching YAML. Actual gh argv/exits/readbacks are in stage-d/. Pre-issue lint passed before creation; no Phase-7 outcome or integration acceptance is prefilled.\n')
(A/'tools/file-d.py').write_bytes(pathlib.Path(__file__).read_bytes())
print(json.dumps(issues,indent=2))
