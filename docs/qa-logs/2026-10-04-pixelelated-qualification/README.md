# pixelelated candidate qualification — first run failed

Refs #383, #409, #395, #414, #415. Can this be done on the VM? Yes: two fresh GENERIC_X64
guests from the verified22533e35b95a bundle, then an actual ROCKNIX RC2 update
rehearsal and exact installed payload readbacks. No handheld or personal cloud.

## Historical launch record

First stage started06:54:19UTC on2026-10-04. Owner
`/workspace/tmp/pixelelated-m7-qa-01`; run
`/workspace/repos/rocknix.worktrees/m7-pixelelated/.build-runs/20261004T065419Z-2eb808cf`.
Runner2152966/watcher2152982, shared5s heartbeat/5min suspected inactivity,
recursive owned artifacts. Tool session4686 is actively supervised at most60s
apart; no disconnected delivery is configured. At06:56UTC both guests had
bootedb137d8c373 and answered SSH; the scripts suite was writing fresh output.
No suite or whole-image verdict is claimed by this launch record.

The prepared qualify/source/payload harness hashes verify. Source copies are
in the earlier build-preparation directory. The fixed `outer.sh` writes its
qualification wrapper result **inside the watched command boundary**, before
the runner/outer tool can finish. `inner.rc`, `outer.rc`, run build.rc/status
and eventual tool-session exit remain distinct observations. This improves
result retention; it does not claim to resolve #395's prior143 discrepancy.

The ordered prepared link/guest/runtime stages follow this stage only on0.
Their source copies and commands are in the build-preparation directory.
Later pair/localisation/memory/proxy/image sweeps and P4 remain required.

## Completion — 2026-10-04 07:27:52 UTC

All15 defaults finished:13 PASS, scripts/frame-diff FAIL. Command, inner,
outer and tool-session4686 all returned1; the watcher retained finished/rc1.
Actual host readback at07:28 found no runner2152966, watcher2152982, QEMU or
owned guest pidfiles. The backend cleanup reported down. No QA job remains.
The active session reported completion immediately upon the terminal read.
This demonstrates this run's result delivery, not disconnected notification.

Scripts:1,688 PASS/1 FAIL,0 skipped. F-RA-07/28 found the stale schema-review
pin after the final proxy refresh. Current-Storage SQL reads passed. #414
corrects the comment and adds an early guard, delivered in next1f5b800391.
It remains open for corrected image bytes and renewed scripts-suite proof.

Visuals: all16 walks produced78 frames. Three unclaimed text regions caused
the initial frame-diff failure. #415 inspected the actual baseline/current
pairs and corrected only the lowercase /pixelelated/Saves claims. Recomparison
of the same78 frames passes21 changed regions,0 unclaimed,0 missing. Missing,
undersized and outside-text negative controls fail. Baseline and original
frames are unchanged; details in ../2026-10-04-pixelelated-folder-claims/.

The original report is retained verbatim and remains failed. The successful
frame recomparison does not change its rc or the scripts failure. The upgrade
rehearsal and exact clean/upgraded payload checks did not execute after the
failed default gate. Prepared link/guest/runtime stages likewise remain
unstarted and their existing success guards must not be bypassed. A corrected
image needs new run owners and a fresh qualification sequence.

Post-failure source/input and candidate rehashes are retained separately.
No RC or device-ready claim. Corrected helper bootstrap #410 is still absent;
host swap is full, and the next image build waits for the safe host preflight.
