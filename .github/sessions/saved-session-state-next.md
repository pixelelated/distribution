# Saved Session State

> Updated 2026-10-04T17:22:39Z. Previous checkpoint: `.github/sessions/archived/saved-session-state-next-20261004T172239Z.md`.

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
device actions retain named gates. No goal tool was created. No job remains running; completed receipts and unfinished source/artifact work are below. Do not relaunch a used run owner.

## Current work: finish artifact classification, then rebuild corrected source

No build, VM or artifact-analysis job is running. Actual host readbacks
confirmed the completed runners/watchers/guests exited. #410 remains fully
completed; do not ask for another helper installation.

Frozen replacement1600d78fe50488537ca5568d2671fe84236da6d4 built642/642 and
now passes all15 default suites,1689 script assertions,16 walks/78 walk frames
plus16 timing frames, actual ROCKNIX RC2 upgrade, exact clean/upgraded payload
readbacks and before/after source/candidate custody. qa-02 run
20261004T163803Z-9d08eda8 finished17:13:52 UTC, every result0 including actual
tool45175. Its real RC2-upgraded disk remains under its owner/pair/vm-a.qcow2.
Receipt: docs/qa-logs/2026-10-04-pixelelated-replacement-qualification/.

The broader source/staging review found #416: five Tools descriptions still
used old project text/links, the memory status heading said Rasteratops and
the bucket example used rocknix. #417 is inherited invalid XML: raw ampersand
in touchHLE description. Both are fixed locally in the feature tree; these
changes are not in frozen1600. Names/paths/attribution remain compatible. The
identity tool now checks Tools XML and player fields. Old malformed XML and
old text fail; corrected source/XML/shell/vocabulary pass. Evidence:
docs/qa-logs/2026-10-04-pixelelated-brand-text/. Source/evidence commit status
may have advanced; inspect git HEAD/status, then integrate explicit hashes.

image-01's attempted parallel analysis was refused by the worktree lock(rc2).
image-02 then failed before extraction on missing ES_SRC(rc1, #418). Fresh
image-03 explicitly supplies it; actual-environment preflight passes. Its
run20261004T171722Z-0c6a3fd1 finished17:17:32, all results0 including tool44613.
Image and update SYSTEM match SHA256
8f034d028da6c1afb404670e2aac27348aa785f23a21372022b048ff41fac841.
Evidence: docs/qa-logs/2026-10-04-pixelelated-image-analysis/.

Actual extracted root: /workspace/tmp/pixelelated-m7-image-03/root (6.5GB).
No image binary was executed. One extracted mode000 file usr/cache/shadow
was made0400 only in this owned analysis copy so scans cannot silently skip
it; original mode is retained in extraction-read-permissions.json. Never
print its contents. All1038 brand-bearing files match original staging bytes
exactly; brand-files.json retains every file hash. Classification is unfinished.

Discovery material, preliminary and outside Git:
- /tmp/pixelelated-staging-brand-paths.json (1038paths) and
  /tmp/pixelelated-staging-brand-discovery.json. Initial row counts were
  7716 build/toolchain contexts,398 attribution,482unclassified.
- /tmp/pixelelated-brand-unclassified.json is a filtered316-row review aid,
  excluding localization/ES/systemd contexts; not the full hit list.
- /tmp/pixelelated-brand-discovery.py records the preliminary scanner, not a
  qualified universal classifier. Inspect each remaining consumer, then bind
  the complete allowlist/classification to NAMING.md v2 and the artifact.
- /tmp/pixelelated-staging-secret-paths.txt and
  /tmp/pixelelated-staging-secret-discovery.json hold20 broad-pattern file
  matches, with offsets/types/hash only (no matching values printed). They
  are mostly public identifier substrings, SSH security-key algorithm names,
  an AWS example, and PEM parser/self-test constants. Do not call this a zero
  secret sweep until every actual candidate match is classified and controls
  work. /tmp/pixelelated-secret-discovery.py is the preliminary script.

Inspected consumer facts: Tools install-rocknix.svg renders a neutral drive
and Install to Internal (PNG/source retained), not an old logo. Locale hits
refer to the retained ROCKNIX partition or historical comments. ES standalone
ROCKNIX is legacy identity fallback/compatibility, ROCKNIX-Emulationstation is
the scraper client identity, /rocknix is the input-config path consumer. Proxy
module names/detectors/update platform remain compatibility identifiers. These
facts guide classification; they do not waive unknown hits.

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

1. Publish source corrections and retained completed QA/extraction receipts,
   update/read back M7 and issues. Close414 from its actual replacement scripts
   proof; close418 from the corrected extraction proof. Keep416/417 open for
   new-image verification. Current live M7/383/409/344 already record these
   findings and the revised order; refresh with completed results.
2. Finish actual artifact brand/secret/localisation and source/licence/readiness
   mapping before a corrected freeze. Resolve all discovered product misses
   together; no brand-wide PASS from targeted checks. Preserve every failure.
3. Freeze a new replacement tree/input manifest from published corrected next,
   preserving1600 and b137. Reuse verified cache through independent files and
   the canonical container path, as documented below. Build through shared
   watcher, retain actual tool/outer results and immutable custody.
4. Bind fresh owners to the new artifact. Existing hash-bound UNSTARTED owners
   are preparation templates bound to1600, not qualification of future bytes:
   /workspace/tmp/pixelelated-m7-link-02, -guest-02, -runtime-02,
   /workspace/tmp/pixelelated-m7-proxy-01, -optins-01, -memory-01, -ui-01.
   Source copies are under replacement-01/{link,guest,runtime,proxy,optins,
   memory,ui}-stage. Defaults/actual RC2 first; then seven-cell WebDAV/S3 link
   matrices;19 independent cloud cases; COW on actual upgraded disk for
   archive/timing/identity;20 packaged-proxy preservation assertions;S3 roundtrip
   and mixed RC2/fresh pair;virgl10/software10/software50+sync and sign-in
   load;EN/FR640x480/1280x960 frames and visual review. Respect prior-success
   guards, owned cleanup and unchanged memory/timing limits. No live RA
   account is used by the synthetic proxy preservation fixture.
5. Remaining ordinary RA award fixture, full sweeps and bug criteria; then
   approved P4 primary + Fable5.1/xhigh via verified Facilitator/OpenRouter.
   Initial #375/#382 audit/dispositions are complete; helper411 is separate.
   Resolve findings and requalify changed bytes before RC designation.
6. P5 source/release/adoption/recovery/public docs and first H700 DDR4/RG35XX SP
   build after P3/P4. No physical action, personal-cloud write or publication
   authorized by this continuation. GENERIC_X64 cannot be flashed to it.

All long jobs use tools/watch-build --interval 5 --stall-min 5 with nested
activity and connected supervision at most60s apart. The shared recorder
refuses two owners in one tree. No disconnected destination is configured
(#395); do not leave a job unattended while promising future alerts.

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
