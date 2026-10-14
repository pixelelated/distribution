# Next M7 GENERIC_X64 engineering image: source-only plan

Prepared 2026-10-14 by the internal fallback lane. No compiler, container, VM,
service, cache copy, full directory measurement, admission preparation, source
publication, or shared-record mutation ran here. Source reads, small file hashes,
host counters and default read-only `build-preflight` only. The coordinator owns
the actual build and its issue-side VM-first declaration. This plan supports
starting an engineering build after source and operational prerequisites; the
new image's acceptance cannot be a prerequisite to producing that image.

## Bound inputs and available capacity

`source-inventory.json` binds coordinator `b004cd4d0751bd871bfda11292b43280895f61ea`
and composition `1ede30a1be476f65eb79614596dd4a98f2630b59`, with all 27 product-path
deltas against accepted replacement20. Composition has the two new proxy patches
and scanner. At this observation its ES recipe still selects `c8dc72cf...`.
The intended new ES commit is **c045d2ec1936c2dfc6c4777935fb2d4cd8b3bcfa**.
Root owns ES syntax review, pin promotion, final composition and publication.
Refresh the delta inventory if that integration adds other product files.

Warm cache: `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20`,
branch `build/m7-pixelelated-replacement20`, source
`1a026648442321609b2288c2c9c06803817f9df2`. The current tracked difference is the
known generated GENERIC_X64 supported-emulators documentation; it is not an
unrecorded product change. Do not reset the accepted worktree.

Accepted provenance is in coordinator
`docs/qa-logs/2026-10-11-pixelelated-replacement-20/README.md` and its
`frozen-inputs-summary.json`. Cache20 independently copied and compared
2,533,045 regular files. Its cache-ready SHA256 is
`579072a50e8785eb0625a665715c9642161bf3f286ec55254a7bbe3bc907bf2a`.
Accepted image bundle is
`bd85b1b42f0170d7d82555af09cbe18762d6fc7eae63293bd0a8043e652db548`;
image SHA256 is `1a23cf5740dbb69cdca76d753a0f6121c35e6e12f27649e792aeebc71e8cc490`
and size 2,073,682,425 bytes. Original build20b container exited0; its wrapper1
was separately diagnosed/verified under #549. Original image20 and QA20 failures
remain retained; their later accepted comparisons and composed qualification do
not rewrite those results. Clean and19→20 retained-storage evidence is accepted
parent provenance, not evidence for the next image.

The Oct12 whole replacement20 worktree measurement was **118,521,081,856 bytes**.
This is a historical upper bound for its build-root copy, not a current scan.
Its source file/hash and selected row are retained in `source-inventory.json`.
The latest host read at18:35:52UTC has **2,976,957,669,376 available disk bytes**,
54,396,952,576 MemAvailable bytes and7,011,401,728 free swap bytes. Preflight
exited0/READY in host PID namespace4026531836. Registry generation145 had one
1GiB reservation; the earlier generation144 had none. Refresh immediately before
each launch, since root's parallel work changes those values. No disk reservation
or memory reservation is created by this snapshot.

## Source delta and rebuild scope

| Package or scope | Treatment in the new isolated root |
| --- | --- |
| emulationstation | Clean/rebuild from c045d2ec; new linked zstd dependency, RVZ notices, shared ScreenScraper identity policy and composed UI/hash changes. Confirm remote clone branch makes the exact commit retrievable. `EMULATIONSTATION_SRC` mounting alone does not change PKG_VERSION or prove source selection. |
| raofflineproxy | Clean/rebuild: cap patch, RVZ padding patch020, startup handoff021 and scanner. Package recompiles `libraproxy_rchash.so`; bind its final ELF and prepared Python hashes separately from earlier native proof. |
| raofflineproxy-rcheevos / raofflineproxy-libchdr | Recipes/pins unchanged. Conservative scoped clean/re-unpack before proxy build establishes fresh selected native inputs without a global clean. |
| gstreamer | Clean/rebuild the ROCKNIX override; tools builds external scanner and cleanup now retains libgstcontroller. Version unchanged. Existing gst-plugins/GL consumers need installed loader-closure checks; no evidence currently calls for a full WebKit rebuild. |
| rclone / rocknix | Clean/rebuild/install changed cloud_oauth, runemu and wifictl. Standard build_distro already cleans rocknix and the base virtual packages; explicit list is safe in the independent copy. |
| alsa-ucm-conf / linux | Changed Qualcomm data and7.2 DP patch are outside GENERIC_X64 behavior; however calculate_stamp hashes their entire package directories. Allow their normal stamp invalidation/rebuild. GENERIC_X64 still selects kernel7.1.2; do not claim the7.2 patch executes here. |
| emulators | Standard CLEAN_OS_BASE regenerates it, including configured launcher/system lists. Install Steam source change is device-gated. |
| Dolphin / Steam / FEX / rocknix-abl / SM8250 files | Retain selected product changes but distinguish target applicability. Default GENERIC_X64 PKG_EMUS does not contain Dolphin or Steam; AMD64 is a separate case. No installed Dolphin launcher claim follows from this default VM image. Keep separately bound VM overlays/fixtures or explicitly review image inclusion before claiming that coverage. |
| Makefile / build tooling | Use final frozen checkout's current admission/watcher routes and pinned builder. Tools do not silently invalidate every package stamp. |

`scripts/build` exits on its own matching deep hash **before** walking dependencies;
dependency source changes do not generally force unchanged consumers to relink.
This plan names the required consumers explicitly. Do not copy target/release,
old image roots as acceptance artifacts, watcher state, or generated tracked docs
from the accepted parent. Copy only `build.pixelelated-GENERIC_X64.x86_64`.
The normal image build recreates its installation root. Explicitly invalidate
the new copy's `.stamps/image/build_target` because script-only edits alone do
not trigger image regeneration.

## Concrete remaining build-start facts

1. Final clean distribution commit on published `next`, exact ES pin c045d2ec and
   source retrieval through its package URL/branch; reviewed final source delta,
   applicable package lint and ES syntax checks. No source publication occurred
   in this lane. Do not allocate a public RC identifier for this engineering run.
2. Resolve a concrete **generated-documentation/admission conflict**. Current
   `build-admission.source_state()` hashes `git diff --binary HEAD --` over all
   tracked files. `nested()` requires equality. `virtual/emulators` calls
   `start_system_doc()`, which truncates and rewrites the tracked
   `documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md`.
   Subsequent parallel nested entrypoints can reject even a transient rewrite;
   replacement20 already has a final4669-byte generated diff. Suggested small
   repair: direct watched-build generated documentation into a declared ignored
   output root, preserving manual documentation generation. A tightly scoped
   generated-output classification in source_state is an alternative needing
   controls that real product edits still fail. Do not disable admission, prefill
   a dirty source, or restore the tracked file while compilation runs. This is a
   source-level risk, not a newly executed failure reproduction.
3. Fresh exact-root measurements and retention/admission reports, sequential
   cache copy with full checksum/inode verification, then consumed original copy
   results and refreshed memory/swap preflight. `measure-capacity.py` is provided
   for that next coordinator measurement; it was not executed here.
4. A reviewed run-owned build observer. Existing watch-job provides liveness,
   activity and original exits; it does **not** supply D-INFRA-023 memory/swap/PSI
   and attributed disk peaks. Root must attach/verify a sampler before launch:
   host MemAvailable/SwapFree, /proc/vmstat pswpin/pswpout deltas, memory/io PSI,
   actual build-container cgroup memory.current/peak/events/io.stat, and allocated
   build/cache/QA/output measurements with sampling cadence and limitations.
   Use the exact container identity and original owner PID/start ticks. Keep
   unrelated retained history separate from the current working set. The sampler
   must retain its own result and exit with the owner; a detached process alone
   is not supervision. No claim that this packet implements that missing sampler.

## Next coordinator commands

After source integration/publication and the generated-output repair, substitute
the verified final hash for `FINAL_PUBLISHED_NEXT_COMMIT` once. The proposed fresh
paths below are examples for the next allocation; refuse any existing path.
The packet scripts reside at the path assigned to this internal lane.

```bash
TASK_PACKET=/workspace/repos/rocknix.worktrees/m7-browser-memory-570/docs/qa-logs/2026-10-14-m7-engineering-image-plan-internal
TASK_COMMIT=FINAL_PUBLISHED_NEXT_COMMIT
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-engineering-20261014-01
TASK_MEASURE=/workspace/tmp/pix-m7-engineering-measure-20261014-01
TASK_CACHE=/workspace/tmp/pix-m7-engineering-cache-20261014-01
TASK_BUILD=/workspace/tmp/pix-m7-engineering-build-20261014-01
git -C /workspace/repos/rocknix merge-base --is-ancestor "$TASK_COMMIT" origin/next
git -C /workspace/repos/rocknix worktree add -b build/m7-engineering-20261014-01 "$TASK_TREE" "$TASK_COMMIT"
mkdir -m 700 "$TASK_MEASURE" "$TASK_CACHE" "$TASK_BUILD"
cd "$TASK_TREE"
tools/build-preflight
tools/watch-build-submit --owner "$TASK_MEASURE" -- --record-only --activity-dir "$TASK_MEASURE" -- python3 -I "$TASK_PACKET/measure-capacity.py" --perform-full-measurement --output "$TASK_MEASURE/measurements.json"
```

Supervise the measurement to its original command/watcher/runner/launcher result
and actual exits. It scans only the named accepted build root, its target folder
and shared source cache, with1800seconds per root; no whole-volume inventory.
No deletion is proposed. An explicit empty retention scan is appropriate only
for that no-deletion stage; it is not historical dependency classification.

```bash
python3 -I "$TASK_PACKET/prepare-plan.py" --checkout "$TASK_TREE" --commit "$TASK_COMMIT" --measurement "$TASK_MEASURE/measurements.json" --owner "$TASK_CACHE" --stage cache
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report --plan "$TASK_CACHE/retention-plan.json" --output "$TASK_CACHE/retention-report.json"
python3 -I tools/host-maintenance/build-admission prepare --plan "$TASK_CACHE/admission-plan.json" --output "$TASK_CACHE/admission.json"
tools/watch-build-submit --owner "$TASK_CACHE" -- --admission "$TASK_CACHE/admission.json" --activity-dir "$TASK_CACHE" -- bash "$TASK_PACKET/copy-cache.sh" "$TASK_TREE" "$TASK_CACHE" "$TASK_COMMIT"
```

Copy budget is the measured build-root allocated bytes plus8GiB metadata/copy
allowance and64GiB operating margin. `rsync -aH` preserves internal links but
creates independent destination inodes; `rsync -aHnc --delete` must report no
changes, followed by every regular-file inode comparison. No `--link-dest`,
hardlink clone or toolchain rewriting. Existing source cache/parent artifacts
already reduce available bytes; do not count them again as incremental copies.

Consume the cache admission with exact `run.path`, unchanged outputs, original0
results and SHA256 evidence for cache-ready, checksum comparison and actual
owner/watcher/launcher exits. Use `build-admission consume` from host PID namespace
4026531836. Then repeat `tools/build-preflight`. Only if swap is below its guard
threshold, with copy watcher and all other conflicting jobs actually exited,
use the reviewed `tools/build-preflight --reclaim-swap`; do not unconditionally
recycle swap or stop unrelated guests.

```bash
python3 -I "$TASK_PACKET/prepare-plan.py" --checkout "$TASK_TREE" --commit "$TASK_COMMIT" --measurement "$TASK_MEASURE/measurements.json" --owner "$TASK_BUILD" --stage build
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report --plan "$TASK_BUILD/retention-plan.json" --output "$TASK_BUILD/retention-report.json"
python3 -I tools/host-maintenance/build-admission prepare --plan "$TASK_BUILD/admission-plan.json" --output "$TASK_BUILD/admission.json"
```

Compile allowance is max(one-third measured build root,32GiB) additional build
growth +8GiB downloads +16GiB firmware +32GiB immediate two-disk QA +64GiB margin.
These are conservative allowances, not measured peaks or a promise of final use.
Current capacity is ample; recheck reservations and `f_bavail` at admission. Each
report/receipt expires after15minutes and is single-use; registry/source changes
require fresh preparation. Do not prepare the compile receipt before waiting
for a lengthy copy.

The reviewed build owner should execute the following exact inner build sequence
under its fresh admission and resource observer (retain original exits, container
identity and effective TMPDIR proof). All mutations are confined to the new copy.

```bash
export PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64
export BUILD_QUALIFIER=dev
export BUILD_TIMESTAMP=UNIQUE_RECORDED_UTC_TIMESTAMP
export DOCKER_WORK_DIR=/workspace/repos/rocknix.worktrees/m7-pixelelated
export DOCKER_EXTRA_OPTS="-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git -v /workspace/cache/rocknix-sources:$DOCKER_WORK_DIR/sources -e TMPDIR=/tmp"
for TASK_PACKAGE in emulationstation raofflineproxy-rcheevos raofflineproxy-libchdr raofflineproxy gstreamer rclone rocknix; do
  PACKAGE="$TASK_PACKAGE" make docker-package-clean || exit
done
rm -f build.pixelelated-GENERIC_X64.x86_64/.stamps/image/build_target
make docker-GENERIC_X64
```

The generated compiler wrapper hardcodes the old logical container checkout
`/workspace/repos/rocknix.worktrees/m7-pixelelated`; preserving DOCKER_WORK_DIR is
mandatory although the host path is new. The accepted old logical host worktree
need not exist. Canonical Makefile supplies UID/GID/options and pins builder
`ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39`.
Record actual consumed image ID/digest. Do not print private options or developer
credentials. Observe effective container TMPDIR and a real successful mktemp;
duplicate Config.Env entries are not themselves failure (#549). Clean-package
containers and main build need distinct observed identities if names/cidfiles are
used. Keep standard host parallelism and existing WebKit-j4 cap; no evidence
requires lowering every package's concurrency.

Submit the completed reviewed owner payload using
`tools/watch-build-submit --owner "$TASK_BUILD" -- --admission "$TASK_BUILD/admission.json" -- bash "$TASK_BUILD/run.sh"`.
`run.sh` is deliberately coordinator-owned and not fabricated here: it binds the
fresh timestamp, source assertions, original results and required sampler. The
copy and planning tools supplied here are source templates, only statically
validated; no runtime PASS is claimed for them.

## After compilation; separate engineering and RC acceptance

Compilation0 is followed by source/output binding: final exact ES/native ELF,
all prepared proxy Python/installed bytecode, scanner, rclone/rocknix scripts,
GStreamer scanner/controller/GL loader closure, notices, SYSTEM/KERNEL update
parity and image identity/hash. Preserve original failed attempts if any; do not
relabel a corrected later run as the original success. Consume admission only
with its genuine original results and retained evidence; the resulting output
holds remain, even after the byte reservation is released.

Then root allocates clean and replacement20→new retained-storage GENERIC_X64 QA:
standard VM suite plus exact changed flows, proxy startup/service queue, CHD/RVZ
hashing, ES changed screens/French/MD5, cloud/browser packaged closure and recovery,
unchanged saves/settings/selected paths, time-to-play, reviewed frames and actual
process cleanup. Bind any overlays separately, especially uninstalled Dolphin.
Accepted component fixtures narrow these checks but do not substitute for new
assembled-image behavior.

These are engineering qualification requirements. Final RC designation also needs
the current M7 issue criteria closed with artifacts, full RC preflight and
source/licence/retrieval custody, correct release identity, clean/upgrade coverage
for intended targets and separately authorized device actions. Do not call this
first combined engineering build an RC or wait for its own image evidence before
starting it. Retention review follows immediate QA: protect source/licence inputs
and compact records; release large parent/build/guest payloads when their named
immediate consumer ends. No standing fallback exemption or automatic deletion is
claimed. This packet authorizes no cleanup.
