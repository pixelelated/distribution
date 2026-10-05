# Saved Session State

> Saved 2026-10-05T20:09:33.013355+00:00. Previous checkpoint: `.github/sessions/archived/saved-session-state-next-20261005T200933Z.md`.
> Branch feature/conflict-resolution; primary /workspace/repos/rocknix stays next.

## Start here

**pixelelated** is an immutable handheld Linux distribution/build system,
forked from ROCKNIX. Version0.0.1, always lowercase, Tiny5 Duo LCD Ocean Bands.
Rasteratops is the lead character and owner's GitHub handle; org pixelelated;
developer blitterbot unchanged. Only ROCKNIX→pixelelated adoption is required:
no fielded /Rasteratops systems. New cloud defaults /pixelelated; configured
ROCKNIX/custom choices and verified move/keep behavior remain compatible.
D-WORKFLOW-144/145/146 and D-CLOUD-174, #409.

Read AGENTS.md/every-session rules from next, compare current tree rules to
next, then this checkpoint, live M7 milestone and #383/#409/#344, today's work
log, docs/pixelelated/rename-plan.md and docs/rasteratops/release-readiness.md.
Milestone body orders current/next phases. Scoped rules load before edits.
The archive above preserves all earlier failed/successful artifact history.

User authorizes ordinary fixes/tests/isolated VMs, explicit-commit integration
onto next and normal fork pushes. Physical-device actions, personal-cloud
mutations and publication retain their named gates. No goal tool created. Prior fresh-context resume proofs are preserved with
full historical context in the checkpoint archives. Latest read-only proof
m7_pixman_frozen10_resume_proof independently verified all6549product/201QA/
180symlink inputs, six build-harness and153QA-harness members, successful cache
completion and first build refusal. Corrections: helper is already committed;
old undated proof times removed; M7 competing current priorities reconciled.
A helper installation is COMPLETE; do not ask to reinstall it.


## Current Focus — permanent GENERIC_X64 Pixman fallback (#447)

Maintainer: "Let's proceed with this fix." The selected source is now
published: feature2feafc12d2fea9ada9730156cb9340b01a3a4e26 → exact cherry-pick
nextd6e8390c93bed87efe2dcc23cd402a271cacd1c7, remote verified19:07:16.
Only GENERIC_X64 gets two startup files plus VM README. Its Sway service
wrapper reads the selected card's virtio child capability bit0: no virgl
selects Pixman; explicit renderer/render-device, virgl and unknown/multi-card
selections retain existing behavior. Shared Sway/handheld/app drivers unchanged.
No saved setting is written. File paths are under
projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/{sway,systemd/system}.

Actual selector04 passes22 checks on each real software/virgl guest,44total.
Allfour terminal0 channels; actual415e17 cleanup19:06:35 verifies six owner/
guest PIDs absent. Allthree failed predecessors remain failed:01 wrong direct
sysfs path (kernel registers DRM at transport parent),02 wrong fixture /lib
instead of /usr/lib,03 unsynced QA key lost across hard stop.04 uses correct
image loader and standard per-boot key setup plus sync. #450 fixture repair
is CLOSED from published artifacts; #447 remains OPEN for installed-image QA.
Evidence docs/qa-logs/2026-10-05-generic-x64-pixman/ (114 retained members).
These checks prove selection, not installation/rendering. Prior runtime Pixman
and actual ROCKNIX RC2 history are in the archived checkpoint and frozen09.

## Current build and running QA14

Frozen tree /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement10,
branch build/m7-pixelelated-replacement10, commitd6e8390c93bed87efe2dcc23cd402a271cacd1c7.
Original freeze/cache owner /workspace/tmp/pixelelated-m7-replacement-10.
Manifest0b24bfcd0d7dad134872b88ed6a2955ddaf9cdf9d55f8a25c17fa5e2de36ad51:
6549product/180symlinks/201QA. Product and canonical container unchanged.

Cache completed19:22:21: empty checksum comparison,2526399 independent files,
all result channels0, actualb53cb1 cleanup19:22:43/all8PIDs absent. Original root
build attempt refused swap before compilation (durable19:22:48 rc1). Its caller
lacked fail-fast; inner guard held. build-refusal.json confirms missing start/
run.path/inner.rc and actual5cc528 cleanup19:24:03. Never replay this owner.
Unrelated containers are not ours to stop. Fixed helper reclaimed swap safely.

Fresh build owner /workspace/tmp/pixelelated-m7-replacement-10-build02 has the
identical manifest/cache receipts. Actual52de55 submitted19:24:34 after
fail-fast preflight. Build completed19:26:30,642/642,allfour0. Actual047d1c
19:26:43 proves all4owner PIDs absent and observedc51a20b1 container removed.
Installed wrapper/drop-in match frozen bytes. Immutable bundle:
/workspace/artifacts/pixelelated-candidates/sha256/1c69bcf5ab6ebdc3e893a6a989545ac7a23359f0e07baef4e9c2beaca94c52b4
Image1cc9c22d63286fbe5d6bdf7f1826d5d977798a472c7f87f8546c1d272a6492bb;
tara9fa66dc63fdb42678a98c42b3abbe84d20f623eb922501bd36f0aa50dfdc1a3.
Image12 completed19:27:17/allfour0; actuald62687cleanup19:27:23/noQEMU.
Raw GPT image/update SYSTEM both5bf4888cfcb29798887f2daab0858981a969e8d3eb71797c0a0a18ffde42cf32.
Extracted root /workspace/tmp/pixelelated-m7-image-12/root.
Retained docs/qa-logs/2026-10-05-pixelelated-replacement-10/.

QA14 is COMPLETE, durable20:06:08/allfour0. Actual2a3cd7 cleanup20:06:47
plus cleanup-supplement.json proves all4owner and6guest PIDs absent/noQEMU.
All15default suites pass;16walks/78frames compare21expected regions,0unclaimed,
0missing. ActualRC2 upgrade passes26checks (external rehearsal log is retained
under qa-14/upgrade-rehearsal). Installed selection passes clean virgl,
upgraded virgl and actual upgraded software/Pixman, no runtime override.
All15actual identity frames reviewed and correct;640px long URL wraps but
retains complete address/instructions. Timing smoke passes; the quick g2g
sample lacks a new sync stamp and is not active-sync behavior proof. Read
qa14/artifacts/timing-review.json. Original reused GPU-screenshot surface
check intentionally permits aspect-correct viewport filling panel height.

QA14 evidence is retained locally at replacement10/qa-14 (180artifact hashes,
171public files plus actual rehearsal log), awaiting normal publication.
Installed fixed helper reclaimed swap again at the verified idle boundary;
actual1d0bcb=0/READY8GiBfree. No helper reinstall or busy-host reclaim.

ACTIVE boot-qualification05 /workspace/tmp/pixelelated-m7-boot-qualification-05,
submittedf15207 at20:08:12; launcher3702400; run
/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement10/.build-runs/20261005T200812Z-9cc9a8fc.
Four clean/actualQA14-upgraded software boots at640/1280. Byte-identical
original capture/matcher/references and12negative controls, threshold0.995.
Adds actual installed renderer verification. Prepared c6f2d1 initially hit
inherited readonly file mode before sealing;6d5fa7 finished preparation and
independent readback. No prior boot05 execution. Current first-clean capture
at20:08:50; no accepted result yet. Preserve exact helper sources/seals.

Poll /tmp/pixelelated-poll-owner.py OWNER [copy.run]; actual observation log
/tmp/pixelelated-active-polls.jsonl. Observe within60seconds, do not claim
perfect historical adherence. #395 still lacks disconnected delivery.

## Next Steps — execute in order

1. Observe active boot05; do not submit it again. Require matching launcher/inner/
   outer/wrapper/runner results, real guest and owner cleanup, suite artifacts
   and direct identity frames. /tmp/pixelelated-complete-durable.py OWNER 0
   checks actual host process absence; owner pair pidfiles may be removed by
   cleanup, so retain/verify every actually observed guest PID separately.
2. Build02 bundle.path is authoritative; original root10/inputs.json remains
   intentionally referenced by QA verifiers. Both input files match exactly.
   Build/cache/image12 are complete. Never rerun their owners/preparers.
3. Launch remaining prepared owners in order with
   /tmp/pixelelated-launch-fallback.py OWNER from frozen10. It checks successful
   build02, fresh owner/private dirs/seals/noQEMU before durable submission.
   Require previous result/cleanup/frame acceptance before moving onward.
4. QA14 is complete, boot05 RUNNING. Remaining SEALED/UNSTARTED owners:
   signin-ui-14 → signin-ui-15 → signin-ui-16 → memory-12 → ui-14 →
   signin-1g-13 → signin-provider1g-05, all /workspace/tmp/pixelelated-m7-.
   Prep /tmp/pixelelated-prepare-fallback-qualification.py and regressions.py
   ALREADY RAN. Independent a1a8f3 verifies153sealed files, all directory/import/
   embedded-code contracts, unchanged exact reference/stable/observer helpers.
   /tmp/pixelelated-fallback-preparation-readback.json retains this result.
   qa14 runs all15defaults/currentclaims + actualRC2 upgrade and software/virgl
   installed selector proof. signin14 cleansoftware;15 COW of qa14's actual
   upgraded disk;16 cleanvirgl. Every full sign-in proof retains original27
   checks and adds nine exact native/host comparisons, no runtime overrides or
   fullscreen manipulation. memory12 adds both-profile exit/time-to-play to
   original10/10/50launches; UI14 exercises software EN/FR640/1280; both1GiB
   workloads use software/Pixman and preserve actualallocation/OOM/load checks.
   Each owner uses standard watcher/durable submission. Require actual terminal
   results, cleanup and direct frames. semantic-dependency.py for1GiB needs
   signin14/completion.json with job_rc0/qemu_absent plus passedvisual-review.
   Retain original failures; fresh owner after any executed failure.
5. Publish exact-byte evidence, reconcile #447 criteria, then remaining P3
   accounts/criteria → approved P4 → H700 arm then aarch64 → named device/P5
   actions. No full RC claim, no product-test transfer from frozen09.

## Key Files and Context

- Committed read-only helper: docs/qa-logs/2026-10-05-generic-x64-pixman/verify-installed-renderer.py;
  read-only installed bytes/unit/realGPU/process proof copied into153sealed members.
- M7 body and #447 read back19:07 after source publication; #450 scoped closed.
- Current source publisher /tmp/pixelelated-publish-pixman-source.py ALREADY RAN;
  receipt /tmp/pixelelated-pixman-source-published.json. Never replay it.
- Prior bundle79d560... imageb9be57ee... sourcecf511ce... is immutable baseline,
  not repaired software configuration. ActualRC2 source69e6039f8f reproduces
  the fault on today's software host; originalSept29 ran virgl and did not
  compare browser finishing native/host. Exact old-host behavior remains unknown.
- No shared product dependency/application source changes since09: preserve its
  broad qualification history and renew affected graphics/upgrade tests on10.

## Integration and operational rules

Primary next and feature use exact cherry-pick -x; normal pushes through hooks,
remote git@github-blitterbot:pixelelated/distribution.git. Never rewrite frozen
product/owners or edit a shell running in flight. Host /proc is hidden inside
sandbox; actual custody requires escalated read. Fixed-port VM owners serialize;
stop named owned PIDs only, never broad pkill. tools/watch-build records five-
second heartbeat and five-minute inactivity; connected agent supervises actual
completion. #395 destination still missing, so no disconnected alert claim.

Primary nextea8144335b0e37d79389935f54515a38e5587781 includes built image evidence;
feature3dc3bcd86be8ca12be76dd03c7d451faa1a40379. This updated checkpoint and
work log andQA14 evidence are local until the next normal publication. Frozen10 stays d6e8390c.

P4 has NOT STARTED. #375/#382 initial reviews complete; don't restart them.
Read full code-auditor skill/routing then use approved primary + Fable5.1/xhigh
via verified Facilitator/OpenRouter (anthropic/claude-fable-5.1). No Daybreak,
no council/same-lab substitution. Key ~/.config/council/env, never print values.
Audit cadence is due/unwaived; normal push gate0 is not RC/audit acceptance.

ES /home/max/Development/emulationstation-next.worktrees/qa-integration,
test/qa-integration,f6f0c134212bc696f2f6a747c8d390a588f2f0ce,cleanpublished.
Splash /tmp/rasteratops-rc-delivery-20261002/splash,master,
8c71126ceef702528c87a4c49625e64988609f26,published.
Tiny5DuoLCD2.007,Gissio/font_Tiny5@f740beb653d6839fac1f8c794668ffcf22037342.
Container ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39.
Hostoptions2cf98cb38836f56f7a6d42ca1c1a5327bb743c98adb42b41831128d475922e7d;
global24/WebKit4;shared /workspace/cache/rocknix-sources;main.gitmountrequired.

## Host helper and unanswered external inputs

#410 closed: root0755 /usr/local/sbin/pixelelated-reclaim-swap,
SHA acfb7936c7271cd642a628a66b9a50d2b70c765eac9dd43bca60a67a7fec0547;
root0440 /etc/sudoers.d/zz-pixelelated-reclaim-swap; old policy absent.
Actual busy/privilege-boundary/recycle/no-op controls pass. The 37 simulated
fault tests and #411 audit remain separately scoped. No reinstall needed.
Use tools/build-preflight --reclaim-swap only while idle; default is read-only.
Never bypass the busy guard or use broad sudo.

Ordinary Tobu100359 is already earned on the dedicated QA account. The prior
async question asks the owner to reset that game or provide another QA account
through ~/.ROCKNIX/qa-accounts (0600). No reply. Never print values, reset the
account, substitute hardcore mode or report a vacuous award PASS.

Public-site frame4f6df54 is local in /home/max/Development/rocknix.org,
branch docs/cloud-saves-native-wizard. Blitterbot received403 from
maxengel/rocknix.org; rasteratops/rocknix.org returned404. No alternate
credentials or new fork are assumed. #395's off-session alert destination is
still pending. The P4 audit cadence warning is not waived.

## Backlog: build/VM QA observability #432

The maintainer asks about OTel, suggests Apache SkyWalking or ClickHouse with
“Clickwatch”, and prefers fully FOSS throughout. D-INFRA-016 records the
preference: evaluate full component licenses/resource cost and local-site or
self-hosted online deployment, likely when a dedicated second build machine
allows a separate agent/observer host. ClickStack is a possible intended name;
async clarification pending. Do not install a platform or put this in M7's
critical path. Standard HyperDX Compose currently includes MongoDB/SSPL;
record that dependency instead of assuming the bundle meets the preference.
Existing watch-build/watch-job local receipts stay authoritative; #395 still
needs verified disconnected delivery. #387 concerns separate device telemetry.

## Continuation helpers

/tmp/pixelelated-status.py OWNER emits a compact actual watcher observation.
/tmp/pixelelated-complete-durable.py OWNER EXPECTED_RC requires allchannels,
actual noQEMU and all recorded up/down/explicit owner PIDs absent. It creates
completion.json exclusively; never rerun after success.
/tmp/pixelelated-retain-10.py SHORT_OWNER EXPECTED_RC retains sealed source and
hashes all artifacts; boot PNGs retain best/control frames, all raw originals
remain local. Visual reviews must be based on actual view_image calls.
/tmp/pixelelated-launch-fallback.py OWNER is checked, no-QEMU and fail-fast;
currently permits boot05 plus the seven remaining owners. Run from frozen10.
The two preparation scripts in the earlier checkpoint ALREADY RAN.
