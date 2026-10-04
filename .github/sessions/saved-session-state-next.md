# Saved Session State

> Updated 2026-10-04T16:42:16Z. Previous checkpoint: `.github/sessions/archived/saved-session-state-next-20261004T164216Z.md`.

## Start here

**pixelelated** is an immutable handheld Linux distribution/build system,
forked from ROCKNIX. The next0.0.1 RC is always lowercase and uses Tiny5 Duo
LCD alone, with the Ocean Bands wordmark. Rasteratops is the lead character
and owner's GitHub handle; org pixelelated; developer bot blitterbot unchanged.
The proposed8bitkid handle was superseded. D-WORKFLOW-144/145/146, #409.
Only **ROCKNIX → pixelelated** adoption is required; the owner confirms no
fielded /Rasteratops systems. New cloud defaults use /pixelelated. Preserve
configured ROCKNIX/custom folders and existing verified move/keep choices.

Read AGENTS.md and the every-session rules from next; compare this worktree
with next before trusting its rules. Then read the live M7 milestone/#383/
#409/#410/#414/#415, docs/pixelelated/rename-plan.md, release-readiness.md
under docs/rasteratops, today's work log and the qualification receipts below.
The archived checkpoint above preserves the failed first qualification and
all earlier source/build provenance. Historical paths stay intact.

Ordinary fixes/tests/VMs, exact-commit integration onto next and normal fork
pushes remain authorized. Publication, personal-cloud mutation and physical
device actions retain named gates. No goal tool was created. Replacement qa-02 is running; its exact owner and watcher are below. Do not relaunch an old used run owner.

## Current work: replacement VM qualification is running

The owner installed the corrected host helper successfully and asked to
continue toward device builds, resolving prerequisites. #410 is now closed:
actual root metadata and helper digest, effective narrow sudo grant, busy
refusal, argument/unrelated-command denial, two idle kernel recycles and
healthy no-op all pass. No more owner bootstrap is needed.

Replacement **1600d78fe50488537ca5568d2671fe84236da6d4** assembled successfully
16:33–16:35 UTC. All 642 package tasks; command/inner/outer/watcher/tool rc0.
Frozen input checks and exact assembled proxy/identity/licence payload pass.
This is an engineering image; **no RC/device-ready claim**.

Current QA owner `/workspace/tmp/pixelelated-m7-qa-02`.
Tree `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement01`, branch
`build/m7-pixelelated-replacement01`, frozen at the full commit above.
Run `.build-runs/20261004T163803Z-9d08eda8` under that tree.
Started 16:38:03 UTC. Runner **787868**, watcher **787869**, tool session
**45175**. Poll the actual status, nested logs and tool result at most 60s
apart; announce failure, completion or suspected inactivity immediately.
Do not edit an executing script or advance the frozen tree.

```bash
cat /workspace/tmp/pixelelated-m7-qa-02/run.path
cat /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement01/.build-runs/20261004T163803Z-9d08eda8/build.status
tail -30 /workspace/tmp/pixelelated-m7-qa-02/console.log
```

Shared watch-build/watch-job checks every 5s, suspects inactivity at 5min,
and observes nested qa-02/artifacts logs. `outer.sh` records the wrapper result
inside the watched boundary; `inner.rc`, `outer.rc`, `tool-wrapper.rc`, run
`build.rc` and tool session result remain distinct. No off-session notifier is
configured (#395); do not end with an unattended job while promising alerts.

This stage runs all 15 defaults, clean installed payload readback, actual
ROCKNIX RC2 upgrade, then upgraded payload readback. The retained predecessor:
/workspace/artifacts/rocknix-images/x64-all-20260929-69e6039f8f/ROCKNIX-GENERIC_X64.x86_64-20260929.img.gz.
Keep -from-ROCKNIX on the tar; its old init checks that name. New payload
checks include exact raofflineproxy-ctl bytes/mode on both guests. No new suite
result is asserted by this launch checkpoint. Do not reuse a started owner.

## Replacement artifact, source and cache custody

Immutable bundle:
`/workspace/artifacts/pixelelated-candidates/sha256/b37f01b7e4e5a06f983dd420b4af10c0c2155564fb9071051c0772ceb0e04c3b`.

- Image `pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz`:
  SHA256 `8b8e50b4c1d5a1dc860f0c6debd268f6f7165633acd108332c1aeefba379249d`,
  2,073,133,259 bytes.
- Tar with the same stem:
  SHA256 `1ae25beb562d41fa94bd9248423023949ad1e0179290a99d359fca188bfa8ea6`,
  2,073,989,120 bytes.
- Inputs `/workspace/tmp/pixelelated-m7-replacement-01/inputs.json`:
  SHA256 `361e0da0f17ce7a04d7d1e5734fc30e11eeee100104a8b4c532d8078733413cd`;
  6,547 regular files, 180 symlinks, 1,608 recipes.
- Build owner `/workspace/tmp/pixelelated-m7-replacement-01`;
  run20261004T163309Z-9d636475, tool87085 exited0. Build runner647033/watcher647034
  exited. Actual container0fbef91a3724 used the pinned digest and uid1000:1000;
  source/identity/path receipts retained. Original cold outer143 discrepancy
  remains historical and unproved (#395); this successful wrapper is no cure claim.

Product delta from b137 is only #414's two proxy comment lines. Host watcher
inputs include the already-tested #412 progress fix. Package freshness was
rechecked live around16:26 and passes; proxyec60 is still upstream HEAD.

The original b137 cold root was copied into independent files, with original
source timestamps retained. Full rsync checksum comparison found no difference;
all 2,525,852 checked regular files have different old/new inodes. Copy run
20261004T161921Z-038d2995 finished0 at16:31; both source trees remain intact.
During quiet verification the watcher correctly warned at5min; actual process
I/O advanced, so no restart. The large per-file progress log remains outside Git.

Makefile's existing DOCKER_WORK_DIR keeps the canonical **container** path
/workspace/repos/rocknix.worktrees/m7-pixelelated while mounting only the new
replacement host tree there. Read-only non-root container probe verified
new git identity and cached compiler sysroot; actual build mount readback agrees.
Do not accidentally bind or change the preserved original host tree.
Only raofflineproxy and the replacement image stamp were cleaned. No library,
toolchain or pin changed. Same 24 global/4 WebKit workers and shared source cache.
The original consumed-source inventory is inherited through verified cache
lineage; full publication corresponding-source/licence work remains separate.

Evidence: `docs/qa-logs/2026-10-04-pixelelated-replacement-01/` and
`docs/qa-logs/2026-10-04-host-swap-rollout/`. Preparation/host proof published
feature5b3e453be48767c1ba40da23e990b5fd16fbb7a9 →
next44f542061793d284c8e14dcad8cc1d746abdf5c7; remote refs verified.
Current evidence/checkpoint commits may be newer; read HEAD.

## Next work in M7 order

1. Supervise qa-02 to its actual result. On failure, preserve the original
   report, trace/file the defect, fix and renew appropriate evidence. No gate
   bypass. On success retain exact clean/upgraded bytes and actual RC2 disk,
   rehash source/candidate and close #414 from its replacement script proof.
2. New prepared, hash-bound, **unstarted** owners:
   /workspace/tmp/pixelelated-m7-link-02,
   /workspace/tmp/pixelelated-m7-guest-02,
   /workspace/tmp/pixelelated-m7-runtime-02.
   Source copies live under the replacement evidence directory. In that order:
   WebDAV/S3 seven-cell link matrices; 19 independently reset640x480 cloud
   guest cases; COW on qa-02's **actual RC2-upgraded** disk for inherited
   archive, five-sample alternating timing with unchanged30ms bound, installed
   identity/update/stats/licence checks. All require prior outer.rc=0.
   Each has outer.sh taking the immutable bundle as its sole argument; use
   watch-build --interval5 --stall-min5 --activity-dir OWNER/artifacts
   --recursive-activity, preserve actual tool result separately.
3. Remaining P3 pair/localisation640/1280 EN/FR, launch/memory, installed proxy
   preservation and live award, brand/secret/source/licence/readiness/public-docs
   criteria. #320/#327/#352/#353/#366/#384/#391/#392 remain actual release
   bug gates, plus #414 until qualified. Close only from each acceptance proof.
   The old installed proxy fixture is docs/qa-logs/2026-10-03-proxy-runtime/
   attempt-04:20 actual packaged-module assertions with predecessor DB
   /tmp/m7-proxy-predecessor (SHA a796c1e6ce6373a6620dfa983e16de3012b6d8feb83f9a2c178f437d8c0adca5),
   no provider contact. It still needs a new bound owner/pin/identity and run.
4. P4 primary + Fable5.1/xhigh through verified Facilitator/OpenRouter fixes
   review, including rename. #375/#382 initial audit/dispositions are complete;
   do not restart. Helper audit411 is separate. Resolve findings, requalify
   changed product bytes, then make the RC call.
5. P5 source/release/adoption/recovery/public docs and H700 DDR4/RG35XX SP
   artifact after P3/P4. GENERIC_X64 cannot be flashed to that handheld.
   No physical action, personal-cloud write or publication is authorized.

## Host helper: completed, explicit idle use only

#410 closed completed with actual host evidence. Source652ec25fed →
next6e4ab570ed installed by owner; do not ask to install again.
Root-owned0755 /usr/local/sbin/pixelelated-reclaim-swap hash
acfb7936c7271cd642a628a66b9a50d2b70c765eac9dd43bca60a67a7fec0547.
Root0440 /etc/sudoers.d/zz-pixelelated-reclaim-swap; old policy absent.
Policy hash583685083f8cbeed1fab20d5ae4442c5cc164f4bbcd75d4632ee6550377f98e9
is from owner's verified installer output, not an unprivileged file read.

Before a future build, while idle, tools/build-preflight --reclaim-swap invokes
only the installed fixed action. Default is read-only. No busy/memory guard
bypass, no Docker-root or broad sudo. Actual root/process observations require
escalated host view. The first recycle passed16:17,9.578s; cache copying filled
swap again, busy refusal held; second idle recycle + healthy no-op passed
16:32:37,13.999s total. All8GiB free, same priority-1. Swap stayed free through
replacement assembly. Existing37 simulated fault controls and #411 external
review remain separately scoped. SIGKILL/power loss cannot execute cleanup.

## Preserved predecessors and repository pins

Original pixelelated tree /workspace/repos/rocknix.worktrees/m7-pixelelated,
build/m7-pixelelated, b137d8c37323abbf07788af8bf8dbd495a31e9c9; don't advance.
Bundle22533e35b95a122ebd0d7dc2b60f6e816982594af62454f5209a04be8da3512d
under /workspace/artifacts/pixelelated-candidates/sha256/. First default QA
qa-01 finished13PASS/2FAIL at07:27:52, all result codes1, no RC2 upgrade ran.
#415's corrected bounded claims make the same78frames compare cleanly, and
415 is closed; the original report remains failed. Its disks are clean-install
only. Never reuse those owners or transfer historical passes.

Older /workspace/repos/rocknix.worktrees/m7-generic-x64,
build/m7-generic-x64,61b64817bf8ab48237e51abb395484e36cbf924b; preserve.
Historical bundle87b8c01d65dc22b4f29049bd0d69307a59c14c16f5223534e95058b2234ca5cd
under /workspace/artifacts/rasteratops-candidates/sha256/ has passing scoped
replacement02/default/RC2 evidence, which is not the new artifact's result.
Both original trees retain generated emulator-support doc changes; preserve.

Feature cwd /workspace/repos/rocknix.worktrees/conflict-resolution;
primary /workspace/repos/rocknix stays next. Integrate only full explicit
commit hashes by cherry-pick, never destination-relative HEAD or whole feature
merge. Push git@github-blitterbot:pixelelated/distribution.git and verify refs.
ES /home/max/Development/emulationstation-next.worktrees/qa-integration,
test/qa-integration,c75aa3fac967ba532fd9ba1c21fa10ca024e8bc1, clean/published.
Splash /tmp/rasteratops-rc-delivery-20261002/splash,master,
8c71126ceef702528c87a4c49625e64988609f26, published.
Proxy ec60fdd0f6522790d9d1d4d20add397bbc4da945,15zero-fuzz patches,
199 upstream +8 fork controls. Tiny5 Duo LCD2.007 at
Gissio/font_Tiny5@f740beb653d6839fac1f8c794668ffcf22037342; OFL/hash in splash.
Container ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39.
Shared cache /workspace/cache/rocknix-sources; main.git mount mandatory.

## Pending external inputs

The ordinary Tobu100359 award is already earned on the dedicated QA account.
An async question this turn asks owner to reset that game's QA progress or
provide another QA account through the local secret file. No reply yet.
No account reset performed; no hardcore substitute and no vacuous award PASS.

Public-site frame4f6df54 remains local in /home/max/Development/rocknix.org,
docs/cloud-saves-native-wizard; blitterbot push to maxengel/rocknix.org403,
rasteratops/rocknix.org404. No alternate credential/fork assumed. Guide
prepared, not deployed. #395 off-session delivery destination still pending.
P4 overdue audit warning remains, not waived; no goal tool was created.
