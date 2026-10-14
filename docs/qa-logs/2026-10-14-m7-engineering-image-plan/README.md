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
and composition `7aab15fc9a1ceab18125ec096a8e6f7f03bdae95`, with all 32 product-path
deltas against accepted replacement20. Composition has the two new proxy patches
and scanner. At this observation its ES recipe still selects `c8dc72cf...`.
The intended final ES commit is **a5c7ff998831c8215f135a42a6f695e75230451d**,
whose product/header/catalog/build files are identical to syntax-reviewed
c045d2ec1936c2dfc6c4777935fb2d4cd8b3bcfa; it adds the published fixture history.
Root owns ES syntax review, pin promotion, final composition and publication.
The coordinator subsequently integrated native7aab and the published ES pin at
08553b715b97fcda97238acf587d1e7aaec6b5ca. Its generated-doc repair and a possible
Wii profile-copy correction are still being qualified. Refresh the delta
inventory against the final published source; this packet does not invent that hash.

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

The coordinator's watched exact-root measurement completed at **18:55:50UTC**:
accepted build root **112,126,599,168 bytes**, parent target4,148,326,400 bytes,
shared source cache68,114,972,672 bytes; available disk **2,976,949,006,336 bytes**.
`capacity-measurement.json` is the unchanged small receipt from coordinator
`docs/qa-logs/2026-10-14-m7-capacity-runtime/measurement.json`; original runner,
launcher and actual-exit proof remain with that coordinator packet. No scan ran
in this lane. Existing parent/cache allocations already reduce available bytes.
The older Oct12 whole-worktree figure118,521,081,856 is retained as historical
provenance, superseded for planning by this exact build-root measurement.

`host-capacity.json` retains the18:35:52 snapshot:54,396,952,576 MemAvailable bytes,
7,011,401,728 free swap bytes, preflight0/READY, host PID namespace4026531836,
registry generation145 with one1GiB reservation. Root's later preflight remained
READY with about51GB available RAM and6.7GB free swap. Refresh preflight,
reservations and volume availability immediately before each launch; neither
receipt creates a reservation. Root also checked that developer credentials and
build overrides were absent and the mounted ~/.ROCKNIX/options had comments only;
repeat presence-only checks if the environment changes, without printing values.

## Source delta and rebuild scope

| Package or scope | Treatment in the new isolated root |
| --- | --- |
| emulationstation | Clean/rebuild from a5c7ff99; new linked zstd dependency, RVZ notices, shared ScreenScraper identity policy and composed UI/hash changes. Confirm remote clone branch makes the exact commit retrievable. `EMULATIONSTATION_SRC` mounting alone does not change PKG_VERSION or prove source selection. |
| raofflineproxy | Clean/rebuild: cap patch, RVZ padding patch020, startup handoff021 and scanner. Package recompiles `libraproxy_rchash.so`; bind its final ELF and prepared Python hashes separately from earlier native proof. |
| raofflineproxy-rcheevos / raofflineproxy-libchdr | Recipes/pins unchanged. Conservative scoped clean/re-unpack before proxy build establishes fresh selected native inputs without a global clean. |
| gstreamer | Clean/rebuild the ROCKNIX override; tools builds external scanner and cleanup now retains libgstcontroller. Version unchanged. Existing gst-plugins/GL consumers need installed loader-closure checks; no evidence currently calls for a full WebKit rebuild. |
| rclone / rocknix | Clean/rebuild/install changed cloud_oauth, runemu and wifictl. Standard build_distro already cleans rocknix and the base virtual packages; explicit list is safe in the independent copy. |
| alsa-ucm-conf / linux | Changed Qualcomm data and7.2 DP patch are outside GENERIC_X64 behavior; however calculate_stamp hashes their entire package directories. Allow their normal stamp invalidation/rebuild. GENERIC_X64 still selects kernel7.1.2; do not claim the7.2 patch executes here. |
| emulators | Standard CLEAN_OS_BASE regenerates it, including configured launcher/system lists. Install Steam source change is device-gated. |
| Dolphin / Qt6 / ECM / HIDAPI | New GENERIC_X64-only source7aab15fc now selects full standalone Dolphin6094cfcf with nogui+Qt, native GC/Wii lists and Tools entry, OGL default and repaired config links. Rebuild/install Dolphin; build missing Qt6 host+target, ECM and HIDAPI through normal dependencies. Do not substitute earlier DolphinTool-only output. Native source/byte/loader and actual gameplay remain new-image checks. |
| Steam / FEX / rocknix-abl / SM8250 files | Retain selected product changes but distinguish target applicability. Default GENERIC_X64 still does not select Steam/FEX, Dolphin libretro, Triforce or WiiWare. AMD64 remains a separate case. Keep separately bound overlays/fixtures for those uninstalled paths. |
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

1. Final clean distribution commit on published `next`, exact ES pin a5c7ff99 and
   source retrieval through its package URL/branch; reviewed final source delta,
   applicable package lint and ES syntax checks. No source publication occurred
   in this lane. Do not allocate a public RC identifier for this engineering run.
2. Integrate and qualify the generated-documentation repair. The separate
   `2026-10-14-generated-doc-output-internal` packet redirects watched generation
   into `${BUILD}/documentation/PER_DEVICE_DOCUMENTATION/${DEVICE}`, preserving
   manual tracked-doc output and the complete source fingerprint. Actual accepted
   replacement20 scheduling has a guaranteed nested image entry after generation;
   this is not only a hypothetical parallel race. This owner's expected final
   functions SHA256 is
   `e574a017b83e0da4d9360017ed14d1edcab86eb979efcad1b15fd4bc76407baa`.
   A different reviewed repair requires resealing that binding before launch.
3. Use the accepted18:55 measurement while fresh, then a fresh retention/admission
   report for sequential cache copy. Require full checksum/inode verification,
   consume original copy results and refresh memory/swap preflight. Refresh the
   measurement only when its age or changed roots require it; no duplicate scan
   is a prerequisite merely because this packet provides a measurement tool.
4. Review the concrete owner and operating bounds below. `build-owner.py`,
   `host-resources.py` and `inner-build.py` implement one supervised command family.
   They are statically checked source proposals, not runtime-qualified tools yet.
   The first bounded clean stage qualifies the actual mount, UID/GID, TMPDIR,
   cgroup and observation-handshake contracts before any cold compilation; do not
   delay the independent cache copy behind a new broad observer test campaign.

## Next coordinator commands

After source integration/publication and the generated-output repair, substitute
the verified final hash for `FINAL_PUBLISHED_NEXT_COMMIT` once. The proposed fresh
paths below are examples for the next allocation; refuse any existing path.
The packet scripts reside at the path assigned to this internal lane.

```bash
TASK_PACKET=/workspace/repos/rocknix.worktrees/m7-browser-memory-570/docs/qa-logs/2026-10-14-m7-engineering-image-plan-internal
TASK_COMMIT=FINAL_PUBLISHED_NEXT_COMMIT
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-engineering-20261014-01
TASK_MEASUREMENT=/workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-14-m7-capacity-runtime/measurement.json
TASK_CACHE=/workspace/tmp/pix-m7-engineering-cache-20261014-01
TASK_BUILD=/workspace/tmp/pix-m7-engineering-build-20261014-01
git -C /workspace/repos/rocknix merge-base --is-ancestor "$TASK_COMMIT" origin/next
git -C /workspace/repos/rocknix worktree add -b build/m7-engineering-20261014-01 "$TASK_TREE" "$TASK_COMMIT"
mkdir -m 700 "$TASK_CACHE" "$TASK_BUILD"
cd "$TASK_TREE"
tools/build-preflight
```

The accepted measurement above is usable for24hours while the named roots
remain unchanged. `prepare-plan.py` checks its timestamp. If it must be refreshed,
allocate a fresh measurement owner and submit `measure-capacity.py
--perform-full-measurement --output <owner>/measurements.json` under
`watch-build-submit --owner <owner> -- --record-only --activity-dir <owner> --
python3 -I ...`; retain original command/watcher/runner/launcher results and
actual exits. It scans only the three named roots, with1800seconds per root.
No deletion is proposed. An empty retention scan is appropriate only for this
no-deletion stage; it is not historical dependency classification.

```bash
python3 -I "$TASK_PACKET/prepare-plan.py" --checkout "$TASK_TREE" --commit "$TASK_COMMIT" --measurement "$TASK_MEASUREMENT" --owner "$TASK_CACHE" --stage cache
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
python3 -I "$TASK_PACKET/prepare-owner.py" --checkout "$TASK_TREE" --commit "$TASK_COMMIT" --owner "$TASK_BUILD" --cache-ready "$TASK_CACHE/cache-ready.json" --timestamp UNIQUE_UTC_YYYYMMDDTHHMMSSZ
# Review build-inputs.json before creating the fresh report/receipt.
python3 -I "$TASK_PACKET/prepare-plan.py" --checkout "$TASK_TREE" --commit "$TASK_COMMIT" --measurement "$TASK_MEASUREMENT" --owner "$TASK_BUILD" --stage build
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report --plan "$TASK_BUILD/retention-plan.json" --output "$TASK_BUILD/retention-report.json"
python3 -I tools/host-maintenance/build-admission prepare --plan "$TASK_BUILD/admission-plan.json" --output "$TASK_BUILD/admission.json"
tools/watch-build-submit --owner "$TASK_BUILD" -- --admission "$TASK_BUILD/admission.json" -- python3 -I "$TASK_BUILD/build-owner.py"
```

Compile allowance is max(one-third measured build root,32GiB) additional warm
package growth +88GiB new Qt/Dolphin allowance +8GiB downloads +16GiB firmware
+32GiB immediate two-disk QA +64GiB margin. The88GiB is itemized as Qt source
expansion8GiB, host objects32GiB, target objects32GiB, installations8GiB and
Dolphin/LTO/new dependencies8GiB. Native source inventory establishes only a
6,013,419,520-byte Qt tar stream and a173,273,422-byte historical Dolphin export;
it does not measure their full build allocations. The extra terms are explicit
initial budget ceilings to supervise, not forecasts or measured peaks. Refresh
the budget and use a fresh owner/admission if observations invalidate them; do
not quietly extend a bound during a run.

`native-dependencies.json` is the exact7aab15fc source inventory. Qt6.10.3's
1,315,591,828-byte archive and ECM/HIDAPI archives are cached; integrity still
needs normal package verification. VM20 has no inspected Qt host tools or target
config/libs, ECM config or HIDAPI target library. Qt enables seven host modules,
eleven target modules including Wayland. Its existing recipe installs selected
qtbase outputs: verify that final Svg/Wayland module/plugin loader dependencies
needed by Dolphin are actually retained. No prior DolphinTool peak bounds this
full Qt/Dolphin build. Existing fmt9.1 stays selected globally; verify Dolphin's
bundled fmt12 fallback rather than bumping unrelated packages.

These are conservative allowances, not a promise of final use.
Current capacity is ample; recheck reservations and `f_bavail` at admission. Each
report/receipt expires after15minutes and is single-use; registry/source changes
require fresh preparation. Do not prepare the compile receipt before waiting
for a lengthy copy.

## Concrete owner and resource observation

`prepare-owner.py` only copies three small helpers and seals `build-inputs.json`;
it does not launch or reserve. The owner verifies clean frozen source, final ES,
generated-doc repair, verified cache-ready, admission ownership and helper hashes.
It then sequentially runs the canonical `make docker-package-clean` for
emulationstation, raofflineproxy-rcheevos, raofflineproxy-libchdr, raofflineproxy,
gstreamer, rclone, rocknix and dolphin-sa; builds qt6 and dolphin-sa with
`make docker-package`; invalidates only the new image stamp; then runs
`make docker-GENERIC_X64`. A nonzero original stage stops the sequence. There is
no global clean; missing providers build through normal dependencies.

The generated compiler wrapper hardcodes the old logical container checkout
`/workspace/repos/rocknix.worktrees/m7-pixelelated`; the owner preserves that
DOCKER_WORK_DIR while mounting the independent new host checkout. The canonical
Makefile supplies UID/GID/options and pinned builder
`ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39`.
Each stage has a unique container name/label/cidfile. Before inner make, the
host checks the actual image ID, selected digest, UID/GID, checkout/owner mounts
and Docker resource limits; it acknowledges the inner ready file's random nonce.
The inner helper waits for that acknowledgment, checks its container identity,
affinity and `nproc`, effective TMPDIR=/tmp with actual mktemp, watched-run marker,
and effective cgroup memory/swap bounds. This makes short clean-container
observation deterministic. Config.Env duplicate entries do not themselves fail.

Cold clean/Qt/Dolphin stages use the first four permitted CPU IDs and24GiB memory
with no container swap, CONCURRENCY_MAKE_LEVEL=4. The image uses the full permitted
CPU set,40GiB memory/no container swap, normal package concurrency and the existing
WebKit-j4 cap. CPU affinity binds Dolphin's `-flto=$(nproc)`; CPU quota alone does
not. These are declared operating bounds, not measured requirements. The family
deadline is6hours, with bounded cleanup/readback afterward. A reviewed limit change
requires new inputs/admission before launch; do not extend bounds during a run.

The resource observer belongs to that owner; no detached sampler remains.
Host samples every5seconds retain MemAvailable, SwapFree, pswpin/pswpout counters,
memory/io PSI and available volume bytes. It stops the family if RAM falls below
8GiB, free swap below20%, host OOM count increases or disk falls below64GiB.
Container samples retain memory.current/peak/events, memory/io PSI and io.stat;
final peak/events are read **before** canonical Docker --rm destroys the cgroup.
Original inner make, Docker/host make and owner results remain separate.

Allocation scans cover the new build root, shared source cache, target, release
and owner. A complete initial scan precedes every producer; periodic scans start
600seconds after the prior scan, each root with180seconds maximum. Live `du`
failures consisting solely of ENOENT are retained with original rc/stderr/partial
stdout and marked incomplete; they do not fail a healthy build. Any other scan
error fails. After containers and host command groups actually exit, a complete
final scan is required for PASS. An interrupted periodic scan is also retained
as incomplete. Reported maxima are sampled allocations, not continuous or atomic
peaks; maxima during gaps remain unknown. Only complete samples check incremental
growth against the admitted budget. Independent volume-floor checks continue
while scans run. Shared cache updates are sequential; concurrent external writes
would weaken attribution and can make the quiescent scan fail.

On stage, deadline, resource or observation failure, the owner stops only its
verified container, then terminates its own command groups, records original
exits and refuses later stages. Quiescence failure prevents a misleading final
scan. Successful helper records are `owner-result.json`, `resource-result.json`,
each stage's `host-result.json`, `inner-result.json`, `container-observed.json`
and handshake/cgroup files, alongside the canonical watcher/runner/launcher
records. Root must consume the genuine original results and verify actual exits.
A helper PASS establishes this execution contract; it does not qualify the image.
No runtime PASS is claimed for these source templates here.

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
process cleanup. Newly selected native Dolphin requires both ELF/Qt loader
closures, GC/Wii/Tools entries, actual correctly sized OGL/virgl gameplay with
legitimate redistributable playable fixtures, ordinary save/reload, manual state
save/load, exit/relaunch and preservation through the actual ES/runemu/launcher
chain. Prior refusal inputs and nonbootable format discs cannot prove native
gameplay. Bind any remaining overlays separately from installed-image behavior.
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
