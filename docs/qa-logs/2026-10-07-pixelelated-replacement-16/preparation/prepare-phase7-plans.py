from pathlib import Path
from datetime import datetime, timezone
import json
import re
import shutil

root=Path.cwd();a=root/'docs/audits/2026_10_06-milestone-m7-p4-fixes-383'
q=root/'docs/qa-logs/2026-10-07-pixelelated-replacement-16'
assert json.loads((q/'content-routing01-acceptance/acceptance.json').read_text())['result']=='PASS'
assert (a/'05-punch-list.md').read_text().count('  outcome: resolved')==8
stamp=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
common=f'''## Software qualification complete — {stamp}

Candidate 16 has completed the M7 P4 fixes audit: all eight findings have
resolved outcomes, with no deferrals or withdrawals. The approved primary
review and both Fable passes are complete; no further model call is required.

- Distribution: `ee014909137e03706e0b3020b8396be589aaa705`.
- EmulationStation: `72494bc72e3d64d4dcfeb4e6478052bbdf166c5b`.
- Immutable bundle: `7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a`.
- QA20: all 15 default suites; 78 comparison screens with no unclaimed,
  missing or stale differences; 26 actual ROCKNIX RC2 upgrade checks; clean
  and upgraded identity, virgl and software rendering accepted.
- Cloud02: 318 checks, 106 each on actual local WebDAV, SFTP and MinIO S3;
  zero failures or skips. No Dropbox credential check is required.
- Changed cloud behavior: actual interrupted-copy retry, historical shelf
  recovery, sibling preservation, truthful refusals/timeouts, original-
  connection repair, supported legacy restore and EN/FR folder routing pass.
  Direct frame reviews and original-state hashes are retained with each proof.

All accepted runs have verified terminal results, unchanged input seals and
actual process/backend cleanup. The original failed runs remain failed;
their corrected controls and later accepted runs are separately identified.
The interruption copy requested in #482 is included and already closed.

Evidence: `docs/audits/2026_10_06-milestone-m7-p4-fixes-383/08-installed-resolution.md`
and `docs/qa-logs/2026-10-07-pixelelated-replacement-16/`. The original forward
audit grades remain historical; later dispositions are mapped in audit09/10.

Current action: publish the acceptance and reconcile #471, #467, #468, #478,
#479, #361, #386, #327, #409, #383 and observer repairs #487/#488 with exact
body/state readbacks. Then #461 capacity/retention review, H700 DDR4 RG35XX SP
arm build, aarch64 build, and the separately gated physical/P5 work.

This is software qualification, not RC designation or release publication.
The 14 known component licence/source metadata gaps, corresponding-source
bundle, public documentation and physical-device facts retain their P5 gates.
Earlier RA award and 125-game proofs carry explicit unchanged-source/byte
custody; no new award/reset or live upstream-freshness query is claimed.
The completed two-file retirement authorizes no broader deletion.
'''
(root/'.build-runs/phase7-complete-status.md').write_text(common)
p=root/'docs/rasteratops/release-readiness.md';s=p.read_text();start=s.index('## Current execution');end=s.index('\n## ',start+1)
p.write_text(s[:start]+common+'\n## Historical qualification records\n'+s[end:])
p=root/'.github/sessions/saved-session-state-next.md';archive=root/'.github/sessions/archived/2026-10-07-before-phase7-closure.md';assert not archive.exists();shutil.copy2(p,archive)
p.write_text('''# Saved Session State

## Start here

Continue pixelelated M7 / 0.0.1. Canonical instructions equal `next`; read
AGENTS.md and the applicable rules. Code-auditor v1.13 Phase7 final acceptance
is complete. Both approved Fable transfers and grading are complete; never
replay or re-ask. One primary orchestrator, no new agents/goals/external review,
Daybreak or instruction-file edits. Continue through checkpoints.

Standing authority covers fixes, isolated VM/host QA, tracker updates and
ordinary fork commits/pushes/builds. No release publication, upstream PR,
personal-cloud or physical-device action, arbitrary root, wider deletion or
filesystem-reserve change is authorized. No permission answer is pending.

'''+common+'''
## Immediate next actions

1. Run audit resolution lint and the normal instruction/register/index checks.
2. Prepare fresh evidence publication07 from publication06, with current HEAD
   guards below. Include audit08/10, all new Q16 evidence, readiness, logs and
   both checkpoints. Use the durable watcher and normal hooks, then verify all
   four results, seals, owner exits, equal paths and exact remote refs.
3. Publish the prepared criterion-specific tracker updates, then re-read each
   body/state and the milestone. Audit lint with --issue471 verifies its eight
   checked outcomes. Retain exact tracker and publication receipts; commit them.
4. Begin #461 read-only retention/capacity report for H700 arm, then aarch64.
   No removal proposal may ignore unreadable/active/unclassified/referenced
   dependencies. Existing H700 caches measured ~28GiB arm/~110GiB aarch64 at
   historical devices1ac; this is not a fit verdict. Remeasure space after QA.

No VM/build/publication owner is currently active. Final content-routing01,
selected-content01, QA20 and cloud02 are accepted and must not be replayed.
All direct frames are recorded and hash-bound. #487 SFTP title observer and
#488 snapshot-field observer are fixed; close after evidence publication.

## Frozen inputs and published heads

- Coordination: /workspace/repos/rocknix.worktrees/conflict-resolution,
  feature/conflict-resolution at9b4e91b832489a5852950c77cf5fc8eef0c49691.
- Primary: /workspace/repos/rocknix, next at32fb5a613df15df5bc30ec7dddcdf2adf3dfbc82.
- Frozen16: /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16,
  build/m7-pixelelated-replacement16 at ee014909137e03706e0b3020b8396be589aaa705.
  Never edit/reset/sync it; its generated emulator-table diff is expected.
- ES integration: /home/max/Development/emulationstation-next.worktrees/qa-integration,
  test/qa-integration at72494bc72e3d64d4dcfeb4e6478052bbdf166c5b.
- Candidate bundle: /workspace/artifacts/pixelelated-candidates/sha256/
  7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a.
- Build input: /workspace/tmp/pixelelated-m7-replacement-16/inputs.json,
  sha256 c72c8d071186ded5e007af4f14c455557aac0e005218879452e68e3947663ee0.
- Raw/update SYSTEM match5767ee7d72f3c538259ee927ad681c63533d661997b64e6beac9d83fdc70812c.
- Selected proxy879b158995d412af434301ebdae581f66b8b6d57; installed46files match
  accepted library02. Only ES recipe differs among1608recipes versus frozen14.
  Cut-time freshness is timestamped Oct6, not a new lookup.

## Evidence and process limits

Audit: docs/audits/2026_10_06-milestone-m7-p4-fixes-383 (00/04/05/07/08/09/10).
Q16: docs/qa-logs/2026-10-07-pixelelated-replacement-16.
The command-backed source readback and final acceptance receipt hashes are in
Q16/phase7-source-readback. Earlier unchanged gates and site asset readback:
Q16/unchanged-dependency-custody. #327 site asset is committed locally, not
published. Device/P5 source and licence work remains separately tracked.

RA33 real Tobu15738/achievement100359 softcore offline→flush/API/relaunch is
complete; its reset is consumed. Library02 has415assertions/879requests. No
new credential or reset is owed. Dropbox#463 optional; #432 FOSS observability,
#464 reset automation and #395 disconnected alerts remain later work. Watchers
record local status; the primary actively consumes results. Never claim an
off-session notification exists. Ten #168 upstream drafts remain unsubmitted.

Protected: builds09/10/12/13/14/15/16 and source/preservation stores, actual
ROCKNIX RC2 baseline69e6039f8f and retained prejoin1ac, shared sources, #456
failure evidence. Exact approved nojoin01 two-QCOW retirement is complete
(9.98GiB recovered); no wider deletion. No swap reclaim during a live job.

Historical checkpoint and full prior run details:
.github/sessions/archived/2026-10-07-before-phase7-closure.md.
''')
(a/'10-closure-reconciliation.md').write_text('''# Final criterion reconciliation

This supplements the independent frozen forward audit. Original grades and
failed runs are preserved. These are evidence dispositions; exact GitHub
body/state readbacks follow ordinary evidence publication.

| Scope | Acceptance and limit |
| --- | --- |
| #467 / PL-001 | Nine installed discovery classifications; empty-local membership; old-source/old-image negative controls; supported legacy pages in EN/FR640/1280; actual selected legacy/tiered/BIOS byte restores and unsupported control; automatic/default and manual chooser with exact paths/log/journal and30direct frames; QA20/cloud02. |
| #468 / PL-004/005 | True future/malformed/config/record/write/network/missing reasons; four30.01s stock timeouts; original connection repair and actual UI retry; full EN/FR640/1280 text and French rclone config/E instructions. Original state, records and foreign endpoint preserved. |
| #478/#479 / PL-003 | Four actual258048/8391392-byte interruptions; UI retry/all original bytes/current shelf;32direct frames; host22focused/398full plus old negative/refusal controls; historical recovery and sibling preservation; final QA20/cloud02. Fresh-root07 separately proves three-tier backup and automatic save receive/send with witnesses. |
| #361 | Independent AC-I361-L123 directly grades selected-source upstream/fork suites, cold lineage, real RA33 ordinary award and UI/progress/flush. Source equality219Linux/53native files explicitly carries the818-test run; no fresh818run is claimed. Later library02 supplies415assertions/879requests. Candidate16 preserves46installed proxy files and all proxy source inputs. |
| #386 | Independent four ACs pass; retained exact source archives, parent-coupled SPIR-V disposition, actual752-byte Vulkan shader compile/link, cbindgen0.29.4/Rust1.94.1, six Codeberg controls, recipe lints, cold target consumers and cut-time freshness. Candidate16 retains1607unchanged recipes; only ES pin changes. No new live freshness claim. |
| #327 | Before/EN/FR640 explanation frames, source and French/menu/vocabulary checks; current ES page source unchanged. Exact local website asset commit4f6df54 and matching a40331aa frame hash re-read. Website publication remains P5. |
| #409 | Actual lowercase identity/defaults and state-preserving ROCKNIX adoption; actual26-check RC2 upgrade and source-defined future filename predicate; exact consumed build container/source custody; inventory/sweep/localisation; default/visual/timing qualification; completed cross-lab audit and rebuilt fixes. Future fork-to-fork update execution and P5 publication retain their original gates. |
| #383 | All named source/fixture children have their own completed evidence. Input/carry-forward gates above plus final candidate16 build/default/upgrade/pair/visual/timing/protocol proofs and eight resolved cross-lab findings satisfy its four ordered software acceptance criteria. H700 builds and physical/P5 delivery remain separately ordered. |
| #487/#488 | Original observer failures retained; three exact sshd-title rejection controls and two missing/wrong-pointer controls; unchanged runtime verdicts; actual backend/PID/container cleanup. |

Primary receipts: Q16/qa20-acceptance, cloud02-acceptance,
selected-content01-acceptance, content-routing01-acceptance,
matrix-primary-reconciliation, root-reasons-*-acceptance,
recovery-*-acceptance, partial*-02-acceptance, supplemental02-acceptance,
unchanged-dependency-custody and phase7-source-readback. Q16 means
docs/qa-logs/2026-10-07-pixelelated-replacement-16.

Audit08 records each actual repair commit and Already written disposition.
The source-readback command receipt re-derives branch inclusion and latest path
commits. Final proof manifests bind exact retained artifacts, not tracker ticks.
No RC designation, release publication, new account action or hardware result
is inferred by closing completed software work.
''')
p=a/'09-remaining-evidence.md';s=p.read_text()
s=s.replace('Full QA20 remains active.','QA20 and cloud02 now pass all final clean/upgrade/protocol gates; see08/10.')
s=s.replace('Product#479/PL003 still await full clean/upgrade/protocol qualification.','Final QA20/cloud02 now pass; #479/PL003 acceptance is complete in08/10.')
s=s.replace('The external review is complete. Four product findings remain open. Candidate16 contains the tested repairs and has passed the affected CLI/root/retry proofs; finish clean/upgrade/protocol qualification and re-derive every resolution before #471/P4 closes.','The external review and all eight command-backed resolutions are complete. Candidate16 passes affected CLI/retry/root/routing proofs, final QA20 clean/actual RC2 upgrade and318protocol checks. See08/10; device builds, physical facts and P5 publication remain separate.')
s=s.replace('#479 retains its final clean/upgrade qualification gate.','#479 final clean/upgrade/protocol qualification now passes.')
s=s.replace('Installed matrix and bilingual UI acceptance are the current gates; no cleanup approval remains pending.','Installed matrix, bilingual UI and final baseline acceptance are complete in08/10; no cleanup approval remains pending.')
p.write_text(s)
with (root/'docs/work-logs/2026_10-work_logs/2026_10_07-work_log.md').open('a') as f:f.write('\n## '+stamp.split(' ',1)[1]+' — #471 all eight findings accepted on candidate16\n\n'+common.split('\n\n',1)[1])
print('Prepared final readiness, criterion map and concise checkpoint; tracker writes still pending')
