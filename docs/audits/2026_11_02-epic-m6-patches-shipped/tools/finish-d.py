import pathlib,json,subprocess,datetime,hashlib
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689');A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped';D=A/'stage-d';C=A/'stage-c';now=datetime.datetime.now(datetime.timezone.utc).isoformat();issues=json.loads((D/'issues.json').read_text())
for p in [A/'05-punch-list.md',D/'audit-body.md']:
 s=p.read_text().replace('owner: coordinator #689 routes to standalone-emulator implementation owner',"owner: 'coordinator #689 routes to standalone-emulator implementation owner'")
 p.write_text(s)
q=subprocess.run(['gh','issue','edit','1411','--repo','pixelelated/distribution','--body-file',str(D/'audit-body.md')],cwd=R,capture_output=True);(D/'audit-body-update.stdout').write_bytes(q.stdout);(D/'audit-body-update.stderr').write_bytes(q.stderr);assert q.returncode==0
(D/'audit-body-update.json').write_text(json.dumps({'utc':now,'argv':['gh','issue','edit','1411','--repo','pixelelated/distribution','--body-file',str(D/'audit-body.md')],'rc':q.returncode,'stdout_sha256':hashlib.sha256(q.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(q.stderr).hexdigest()},indent=2)+'\n')
finding='''\n## Findings index\n\n| bucket | reader | finding | severity | result |\n| --- | --- | --- | --- | --- |\n| native 271 | gpt | F-T42-01 | Medium | PPSSPP nested patch is inert as SDL transformation; PL-01 / #1410 |\n\n## Verification\n\n### F-T42-01 (gpt, primary Local reader)\n\n**Verdict:** **confirmed, Medium**. Seed PPSSPP 007 lines 11–16 create a nested file; lines 17–29 add the intended SDL diff as text. scripts/unpack:191–196 applies the outer file once; recipe post_unpack does not apply the nested file. The constructed fixture in stage-b/nested-patch/receipt.json returns normal rc 0, creates the nested target and leaves sentinel SDLJoystick.cpp unchanged. This is a source-format mechanism proof, not an at-pin or runtime result. Fixed upstream's direct diff uses NKCODE_GUIDE, whereas the nested seed payload uses NKCODE_UNKNOWN. Owner must resolve intended behavior in the separate fix #1410; audit #1411 / PL-01 remains open pending coordinator disposition. Source and negative duplicate searches are retained in stage-b/source-context/.\n'''
p=A/'tools/tables.py';s=p.read_text();s+='\nwith (A/"02-forward-audit.md").open("a") as findings_out:\n findings_out.write('+repr(finding)+')\n';p.write_text(s)
q=subprocess.run(['python3',str(p)],cwd=R,capture_output=True);(D/'table-final.stdout').write_bytes(q.stdout);(D/'table-final.stderr').write_bytes(q.stderr);(D/'table-final.json').write_text(json.dumps({'utc':now,'argv':['python3',str(p)],'rc':q.returncode,'stdout_sha256':hashlib.sha256(q.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(q.stderr).hexdigest()},indent=2)+'\n');assert q.returncode==0,q.stderr.decode()
(A/'06-audit-summary.md').write_text('''# T42 Stage D audit summary

Ready for coordinator stream disposition under #689; final acceptance and E–H are pending. Reviewed-at: `9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1`. Branch: `feature/m6-patches-shipped-689`; absolute worktree: `/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689`. The final #689 publication checkpoint names the clean immutable D tip and remote readback. No source-changing permission is inferred.

## Result

[Audit #1411](https://github.com/pixelelated/distribution/issues/1411), a real child of #689 in M6, has one Medium finding (0 Critical, 0 High): PPSSPP007 creates nested patch data without changing its intended SDL target. [Reactive bug #1410](https://github.com/pixelelated/distribution/issues/1410) has no parent/milestone and remains open. PL-01 has an Open Phase-7 outcome, not a prefilled deferral or resolution. Fixed upstream's replacement changes the requested mapping, so a future owning brief must decide intended GUIDE behavior before adopting it.

## Populations and evidence

- Native Provenance and Coverage each have exactly 384 paths / 71,387 logical Git-blob lines. Four link identities are separate from referents; T43's MangoHud referent is context only. Twelve fork-written members / 498 lines were read in full, including Dolphin.
- Native worst-per-plan source application: 151 applies, 38 offset, 22 fuzz, 173 explicit open items. There are 542 package/plan groups with context siblings, not 542 native paths. Retained evidence validates 760 diagnostic/normal pairs, 3,040 output hashes and 116 safe cached-source target projections. These are not full source trees or runtime correctness results.
- Separate inherited population: 50 exact keys / 26 overrides; 21 already carried in their stated current-pin intent, seven not applicable with individual reasons, 22 specific unresolved owner inputs. The other 24 T40 rows remain excluded. Both real H700 U-Boot consumers use v2026.01; systemd design stays #1104; busybox/util-linux symlink counterparts and gettext's distinct question are retained.
- Fixed upstream 651150fc88 and the fixed base are compared by exact path/blob and literal recipe pins/includes. Component upstream URLs remain unverified. Draft contribution text remains here; nothing was sent to #585.

## Review and checks

Local actual reader: Codex / GPT-6-Astra / xhigh, OpenAI, T5 wN:p7, session 01a19d12-3d7a-7642-9108-ae06a719cdd7. Reviewers [], one-file review-plan under D-WORKFLOW-184. T38's accepted records are untouched. No external review or runtime allocation occurred.

A binds source/seed/P1 and Local lint capability. B contains tables, source comparisons and explicitly limited application proofs. C's four table mutations fail their own assertions before positive validation; working and committed-then-reverted source changes fail independent guard fixtures. Literal pre-issue lint before filing: `PASS pre-issue artifacts (does not certify resolution)`. D holds issue bodies, creation/parent/milestone readbacks and actual check outputs. Repository rules/register/index/ceremony/forbidden/hooks passed in stage-c/checks.json; final issue/new-record checks are in stage-d/checks.json. Normal publication receipts and the final external checkpoint bind the clean tip. No package recipe changed, so pkgcheck is not applicable.

## Limits and next owner

173 native application limitations and 22 inherited questions remain specific rows, not invented bugs. G202/G203 stopped on a link-producing candidate before its normal rc was serialized; those exits are unclaimed. WebKit/Samba duplicate archive members are unqualified rather than silently extracted. Full-line review of the other 372 patches, configured builds, image/upgrade tests and all runtime measurements are outside this table pass. Both time-to-play quantities are untouched.

Coordinator wN:p2 owns the stream disposition: proposed separate PPSSPP fix brief for #1410 and routing of existing owner-specific inputs. T42 stops after published D. E records authorized outcomes; F performs final resolution lint; G final retro; H accepted hand-back/owned scratch retirement follow only after disposition. This D summary is not final slice acceptance, a release gate, or a source fix.

Source scratch `/workspace/tmp/m6-t42/` remains retained until acceptance and the later H cleanup instruction. It contains source projections and synthetic fixtures only; no build/guest/device/cloud job or host-ledger reservation is owned by this lane. Historical launch/T38 trees remain untouched.
''')
(A/'07-questions-for-the-maintainer.md').write_text('''# T42 actual choices and coordinator hand-off

Stage D requests the coordinator's stream disposition, already specified by #689's dispatch. No additional maintainer preference or permission is required to complete A–D.

| Actual unresolved choice/input | Evidence | Owner / next action |
| --- | --- | --- |
| PPSSPP desired GUIDE mapping: seed nested payload requests NKCODE_UNKNOWN; fixed upstream direct diff requests NKCODE_GUIDE. | F-T42-01 / PL-01 / #1410; source-context/ppsspp-patch.stdout and ppsspp-upstream.stdout. | #689 coordinator assigns the owning PPSSPP fix brief; #677 implementation context. Decide from intended product behavior and exact-pin consumers before importing a correction. T42 does not choose a new behavior. |
| 22 inherited feature/architecture/pin inputs are unresolved. | Each I-row in 02 and inherited-decisions.json names its evidence, missing input and exact owner action. | Existing T8 #655, T22 #669, T27 #674 owners. H700 requires both pylibfdt consumers; systemd design remains #1104. No blanket adoption or removal choice is proposed. |
| 173 native paths lack a fully admitted application claim. | Per-plan stack/archive/hook/normal receipts and reasons in 02/tables.json. | #689 comparison owner routes qualification to the package/recipe owners as needed. Cache misses, dynamic input and extraction limits do not authorize fetching or runtime allocation. |
| Contribution candidates and class removal. | Twelve attributed fork-written readings and local #585 draft text; explicit existing-owner boundaries. | #585 contribution owner verifies component upstream and focused reproduction under its own scope; #1048/#346 own class removal. No submission or deletion was made. |

All current outcomes have named owners. Do not manufacture a mandatory new maintainer decision to keep the lane active. No Phase-7 row is resolved/deferred until the coordinator supplies its disposition. This lane remains available at the D boundary; it does not answer another agent's permission prompt.
''')
(A/'tools/README.md').write_text('''# T42 audit-local tools and receipt custody

Use absolute workdir `/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689`. These tools are part of the source-only audit, not product tools. Fixed input identities and authority are in 01 and brief v2. No tool grants runtime, source-fix, fetch or tracker permissions.

- `tables.py` regenerates the exact native/coverage/inherited/fork tables from retained inputs and runs four fail-first in-process assertions. The enclosing command receipts record actual process exits. It preserves reviewed-at source identity; it does not reapply patches.
- `validate.py guard ABS_REPO SEED` checks the current diff, untracked paths and every lane commit against the narrow record allowlist. It is suitable for a final new-record check. The no-argument run is the one-shot synthetic-fixture and retained-scratch verifier; it refuses to overwrite its fixture. Its original positive/negative results remain in stage-c/.
- `apply-stacks.py`, `inherited-source.py`, `nested-probe.py` produced the retained source-only receipts. They use only the owned /workspace/tmp/m6-t42 scratch and cached sources. Do not replay an accepted application to fill time. Inspect receipts and code first; unsupported transformations remain open.
- `gather.py`, `select.py`, `compare-hunks.py`, `inherited-decisions.py` are the extraction/analysis procedures used for the recorded tables. They can overwrite their generated records; they are provenance, not instructions to reopen accepted work.
- `stage-a.py`, `finish-b.py`, `stage-c.py`, `file-d.py` record one-time assembly/filing commands. Some refer to the original /tmp small-text staging files. They are not a recovery entrypoint and must not be rerun after publication; especially do not recreate tracker issues. Resume from the saved lane pointer and actual Stage D readbacks.

Application receipts use target-member projections, not full component trees. G202/G203's regular-file snapshot guard omitted the link-creating candidate exit; no positive is reconstructed. The negative table controls are actual AssertionError rejections, not subprocess rc 1; the path controls really invoke a subprocess and retain rc 1. No unobserved exit, success or review is synthesized.
''')
p=A/'tools/file-d.py';s=p.read_text().replace("assert not (D/'issues.json').exists(),'refuse duplicate issue creation'","assert not any((D/f).exists() for f in ['issues.json','created-bug.json','created-audit.json']),'refuse duplicate or partially completed issue creation'");p.write_text(s)
# Process-name census omits command lines/private arguments; it is observational, not host-ledger authority.
q=subprocess.run(['ps','-eo','pid,ppid,comm'],cwd=R,capture_output=True);(D/'process-census.stdout').write_bytes(q.stdout);assert q.returncode==0
(D/'census.json').write_text(json.dumps({'utc':now,'argv':['ps','-eo','pid,ppid,comm'],'rc':q.returncode,'stdout_sha256':hashlib.sha256(q.stdout).hexdigest(),'scope':'T42 commands allocate no runtime and do not source recipes/config. Process names are observational, not a host-allocation receipt. Existing unrelated processes are not owned or modified.','owned_source_scratch':'/workspace/tmp/m6-t42/','cleanup':'retained until acceptance and authorized H retirement','no_held_runtime':True},indent=2)+'\n')
with (A/'00-running-log.md').open('a') as f:f.write('\n### '+now+' — D packet assembled\n\n06/07 state the actual result and outstanding owners. No new mandatory maintainer preference is invented. PL-01 / #1410 remains open in audit #1411; E–H require coordinator disposition. Final D checks and clean publication follow; both time-to-play measures remain untouched.\n')
(A/'tools/finish-d.py').write_bytes(pathlib.Path(__file__).read_bytes())
print('PASS D summary/questions/issue YAML and source finding assembled')
