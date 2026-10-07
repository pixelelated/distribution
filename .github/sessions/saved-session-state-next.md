# Saved Session State

> Saved: 2026-10-07T16:30:26.058895+00:00
> Coordination branch: feature/conflict-resolution
> Repository: pixelelated/distribution

## Start here

This repository builds an immutable handheld Linux distribution, not an app.
Read AGENTS.md and canonical `.claude/rules/` from next. Primary
`/workspace/repos/rocknix` stays on next; coordination is
`/workspace/repos/rocknix.worktrees/conflict-resolution`. The preceding checkpoint
is `.github/sessions/archived/saved-session-state-next-20261007T153723Z.md`; it
retains exact accepted H700/SP and candidate16 identities, source custody,
cleanup receipts and earlier publication. Do not replay accepted tests or failed
owners. Never print credentials. Check actual processes and bytes, not old prose.

Standing authority covers fixes, host/VM QA, scoped fork commits/pushes and
H700 then SM8550 builds. The user explicitly requested parallel copy/build work.
They authorized screenshots needed to troubleshoot the SP migration; permission
persists for those captures. One separately approved directional wake input and
its follow-up capture completed at16:26UTC. Do not duplicate the input. No
confirmation input, migration retry, cloud mutation, new reboot/game/update or
public release is inferred. State-changing device actions use tools/device-act. Device reads use
the credential filter. No new external audit is owed or authorized here.

## Current Focus

M7.P5 /0.0.1: finish active SM8550 firmware and artifact acceptance after the
proved FEX repair, now including the approved migration prompt. Investigate the
owner-initiated SP migration using local evidence; do not retry personal cloud.
Milestone7's body is the ordered execution plan.

## Completed This Session

- #502 complete/closed: exact approved English and French strings in ES
  5d2fcb9b71f363cfa4813d5356f02c48ab58e139, normal-hook published on
  feature/m7-migration-copy and test/qa-integration. Compiler/gettext/source
  checks and four actual EN/FR640x480/1280x800 frames pass. All text/choices
  visible without scrolling. Temporary guest/keys/binaries retired (2.56GB).
  Packet docs/qa-logs/2026-10-07-migration-copy. Distribution pin/changelog/
  D-UI-122/123/124 published on next0553c0193ace3aebbefaae5b7b6d49253c2811d9
  (featurea963ac13d9). Current handheld firmware is unchanged.
- #503 proved ARM64 libc headers leaked into FEX x86 guest compilation via
  pkg-config. Exclude only the rebased standard include root. Exact original
  Nix/compiler/rootfs controls fail before and pass after; all configured
  guest libraries build. Fix/evidence on next6b627a38ae, featureb3aef8a38f.
  The full package now compiles, with14 installed architecture-checked ELFs.
- Original SM build01, acceptance01 and sequence01 failures remain preserved.
  Recovery01 archived730 thread logs/stamps and renamed the eight interrupted
  scopes plus partial image before advancing only the stopped checkout.
  Recovery fourzero channels/sevenseals/exits verified15:49:57. Guarded swap
  preflight passed15:49:27 after all guests/watchers exited;8GiBfree then.
- #506 helper failures are preserved:02 used scaffold guest-libs directories
  instead of actual Guest/Guest_32;03 proved the corrected helper, then hit
  canonical checkdeps's writable /nix requirement on a read-only cache mount.
  02four2/eightseals/exits accepted15:51:05; acceptance02four1/controllerFAILED.
  03four2/12seals/exits verified16:05:54; acceptance03 never submitted.
  Neither is relabeled successful; no image assembly occurred in those attempts.
- #504 read-only review found incomplete migration and missing terminal
  diagnostics; #505 owns bounded safe results at normal verbosity. Raw device
  readbacks and authorized screenshot are LOCAL ONLY in the ignored
  rg35xxsp-migration-review01 directory under today's device QA logs. The image
  initially exposed no readable error. A subsequent authorized wake and capture
  exposed the incomplete-transfer result; no confirmation or retry was performed.
  Expanded GitHub disclosure was rejected; minimal tracker status was then
  accepted/read back to the verified fork, without raw evidence upload.

## In Progress

### #492/#503/#506 — SM8550 build and artifact verification ACTIVE

Current source0553c0193ace3aebbefaae5b7b6d49253c2811d9 includes the FEX patch and
qualified ES copy. No further source change is permitted in this running tree.

- Tree `/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-01`, branch
  build/m7-pixelelated-sm8550-01. Earlier failed40f80/6b inputs are historical.
- Sequence `/workspace/tmp/pixelelated-m7-sm8550-sequence-04`, PID70714;
  state.json heartbeat every30s; controller-result.json only at terminal.
- Build `/workspace/tmp/pixelelated-m7-sm8550-build-04`; run.path names its
  exact tree-relative .build-runs directory. Read build.pid/watcher.pid/
  command.pid there and runtime-start.json for the observed container.
- Acceptance `/workspace/tmp/pixelelated-m7-sm8550-acceptance-04`; run.path
  names its watched run in primary. It follows actual builder/process/container
  exit before firmware verification. No need for a new permission checkpoint.
- Actual container00731af86051732418b7c2c567c801a5d50b9970220d24812643f7e1a86e5a0d;
  image988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39.
  Observed startup/mounts16:14:08; inside gatePASS16:14:09, canonical checkdeps
  and original/fixed14ELF proofPASS16:14:10. build_distro reached656/737 at
  16:14:30 while reinstalling warm completed packages. This is not completion.
- Global24/WebKit4. Unchanged ARM7946files/807links/245stamps carried; manifest
  SHA41b6eaa2906661b6fbea165161e958edc42846feeff11cf03c2c935b01fb1ade.
  The copy under build04/artifacts is mounted and sealed. No ARM rebuild.
- Private02 Nix cache is RW, an explicit active mutable input; exact nixpkgs
  snapshot remains RO. Do not make /nix RO: canonical checkdeps requires write.
  The new startup gate waits for observed container/mount identity before work,
  avoiding the short-lived-container race in03. No extra Nix copy/reclean/reclaim.
- Installed acceptance requires ABL/GPT/raw-update equality, identity, ARM/FEX
  bytes, new English prompt bytes and exact French catalog lookup, plus independent
  custody. Source/licence and named physical smoke/publication remain separate.
- Agent sm8550_resume_plan is supervising in this session. On resume, list live
  agents; if it no longer exists, take over these same owners without submitting
  another build. Root handles tracking updates.
  Controller emits local tracker-handoff-started/terminal.json, not external
  messages. Durable watches do not notify disconnected chat (#395): supervise
  actively and report terminal outcomes promptly. Never launch a duplicate.
- Retain recovery01/preserved and control01 snapshot/store plus build02/nix only
  while this immediate build/source-custody dependency needs them. Retire each
  only after artifact acceptance AND confirmation that source/licence custody
  no longer depends on it. Firmware acceptance alone does not clear that hold.
  Preserve compact records. ~2TB disk free, no new drive needed.

### Bounded resume readback

From this repository, run the retained read-only helper:

```bash
python3 -I docs/qa-logs/2026-10-07-device-builds/sm8550-resume04/read-status.py
```

It reads state, run.path/status and actual terminal receipt locations without
changing or submitting anything. Keep status checks within60seconds during the
active session and consume each terminal outcome before unrelated work.

The tool sandbox's /proc cannot see these HOST PIDs. A fresh-context reviewer
confirmed they appear absent inside the sandbox while host processes remain
alive. Use host-context/escalated execution for process/container readback,
matching controller70714 start_ticks48133002 and recorded container identity.
Sandbox-only absence is UNKNOWN, not exit. Do not rerun an exclusive verifier
whose owner-verification.json already exists; read and validate that receipt.

### SP investigation — approved wake and follow-up capture complete

The user said: "you may capture whatever screenshots you need on the RG 35XX SP
in order to troubleshoot this issue." That permission is already granted.
The single capture was blank; local panel/compositor/power observations and the
source's default screensaver are in the local report. The user then said: "yes, you can send a keypress to wake the screen up".
The SP review agent completed that ONE directional input through device-act and
a capture at16:26UTC without selecting a confirmation action. The frame confirms
an incomplete-transfer result but does not name the underlying error. The local
packet retains the actual frame and action receipts. Never duplicate the keypress
merely because a session disconnected. Read-only source tracing continues.
Exact-pin source tracing is now complete: `discarded` is the successful
discarded-save tier before content, not an abort marker or terminal timestamp.
Elapsed time freezes at worker completion; the generic content outcome combines
copy/check failure and cannot establish which occurred. #504's review is complete;
#505 owns future terminal diagnostics. No historical cause is claimed solved.
No migration retry is authorized. The detailed packet is deliberately ignored by
Git; only PUBLIC-SUMMARY.md and .gitignore may be staged. Do not publish raw images,
identifiers or detailed readbacks without established disclosure authority.

## Next Steps

1. Consume actual04 build and artifact acceptance results, verify all terminal
   channels/seals/process/container exits, then reconcile #492/#503/#506 and M7.
   Use existing exclusive receipts if already written; never rerun their verifier.
2. If build fails, retain all logs before retry. No ad-hoc in-flight script/source
   edits or unreviewed package clearing. Correct helper defects in fresh owners;
   do not discard successfully built packages without evidence.
3. #504's historical review is complete, including the authorized wake/frame and
   exact-pin source trace. #505 diagnostics are tracked, unimplemented. The review
   does not prove provider bytes or authorize a retry.
4. Publish remaining work/friction logs, compact resume02/04 records and checkpoint
   via scoped NEW commits/cherry-picks. Never merge the entire divergent feature
   history into next. Check rules/register/index/ceremonies through normal hooks.
   Both hosted checks passed for0553: record run37648390539 and wordlist
   run37648390468, read back through the API's exact head_sha filter. Ordinary
   run-list output was misleadingly stale. Verify the next publication separately.
   Primary next may advance with docs while the build stays0553.
   The16:33 ceremony gate passes its blocking checks but now reports12 closures
   since the accepted audit. Treat that new cadence advisory explicitly; do not
   rerun completed candidate16 evidence or silently claim the next CI passed.
5. H700 firmware/SP adoption and candidate16 common QA/audit remain accepted; no
   repeat VM matrix, Dropbox check, RA reset or external audit is needed. Remaining
   P5 gates are SM artifacts, separately named device smoke/adoption, corresponding
   source,14 licence metadata gaps, public docs and manifest-bound release assets.
   No RC designation or public release is inferred from compiling.

## Key Files Modified

Pending coordination files are the work/friction logs and index, this checkpoint
and its preserved archive, compact sm8550-resume02/04 evidence, and the minimal
public SP summary/ignore rule. Product/pin changes are already committed/pushed.
Local private SP data must stay excluded. Check git status before adding paths.

## Related Context and Notes

#492 device builds; #497 ARM handoff; #500 completed SP adoption; #502 closed copy;
#503 FEX repair; #504 review; #505 terminal diagnostics; #506 acceptance helper.
Completed candidate16, H700 bundle and physical installation hashes are in the
archived checkpoint above. Exact active owner paths beat any stale count here.

The ES source needed C++ Unicode escapes so build-style xgettext extracts the
curly quotes. A QA guest stopped without flushing had zeroed overlay files and
locale data; re-stage/hash and flush before stopping disposable guests. Final
frames are the specifically accepted matrix, not every rc0 capture. The French
button-panel overhang predates this copy; all choices stay within the screen.

Procedures and controls are retained in compact sm8550-fex-controls01,
sm8550-resume02 and sm8550-resume04 packets. Do not print giant input inventories;
extract selected keys. A process State S is ordinary waiting, not system sleep;
same boot alone cannot exclude sleep, and journal queries need explicit UTC.
