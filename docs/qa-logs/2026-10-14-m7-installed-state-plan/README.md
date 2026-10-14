# M7 final installed state and source identity — #565 / #566

This is a source-only qualification plan, prepared against the exact files in
`source-inputs.json` and complete live issue readbacks saved here. No build,
fixture, VM, device operation, provider request, shared-record edit or publication
ran in this lane. Root owns allocation, execution, acceptance and issue updates.
This packet does not add release criteria or repeat accepted component controls.

The coordinator source includes GENERIC_X64 Dolphin support, ES a5c7ff99,
generated functions SHA e574a017…, and the repaired Wii profile copy. These are
observed inputs, not the final build identity. During review root assigned the
existing #566 compiled-service-error mismatch to the ES worker and is correcting
commit metadata without changing product trees. Bind the actual final distribution
commit/tree, ES pin, build receipt and artifact hashes after those changes. Never
substitute this plan's observed commit for the frozen build's actual identity.

## Evidence already accepted — reuse, do not rerun as substitutes

- #565: selected ready VM20 first boot; 113 root controls and final 142
  root/payload/release-preparation controls; byte-preserving retained-mode
  checker controls. These qualify the checker, not a new OS upgrade.
- #565: ROM-only versus ROM-plus-gamelist import established Recent membership
  from metadata while selected account/activity state stayed equal. No repeat is
  needed to explain Nova. Original account writer and exact historical copy stay
  unknown; an update preserves state and does not establish its origin.
- #566: 127 root-policy controls and four recipe selections, with original
  failing baseline controls. Synthetic ELF headers are not actual ES execution.
- Current-source native proxy build and #588 service/component evidence are
  accepted within their recorded scope. Final installed source/ELF identity and
  ordinary boot remain separate. Do not replay old native/service owners.
- Replacement20's clean and real 19→20 upgrade are accepted parent provenance;
  they are not acceptance of this next image. Source/input receipts are hash-bound
  here; their original failures and retirement records remain unchanged.

## Ordered execution and resources

Can this be done on the VM? Yes for fresh/retained state, actual installed
behavior, accounts/backup and UI. The payload reader is the existing host release
preflight component and uses host filesystem readers; its successful synthetic
controls do not replace reading final files. Root records this existing split
in #565/#566 when allocating the actual run.

1. After successful image assembly, bind the actual update `.tar` and install
   `.img.gz`, SYSTEM/KERNEL equality and build source/installed outputs. Run the
   two payload gates sequentially on the host.
2. Boot one fresh candidate guest, standard 4 vCPU / 8 GiB / 16 GiB+ disk,
   640×480. Before keys, accounts, ROM metadata or other QA seeds, run the ready
   clean-state gate through serial. Capture actual installed identities.
3. After clean acceptance, run the separately owned #566 UI/backup work, with
   EN/FR 640×480 and 1280×800 sequentially. Preserve distinct frame bindings.
4. Stop/retire that guest after accepted compact evidence. Boot previous accepted
   replacement20 into a fresh owned disk, seed synthetic retained state, then
   install the *same accepted new update tar* through the actual OS update path.
   Verify changed boot/build identity, unchanged selected state and installed
   bytes. This is a genuine old→new update, not a filesystem overlay.
5. The ordinary combined suites, gameplay, time-to-play and broader upgrade/
   restore work remain root-owned existing image requirements. This packet does
   not claim those results or start another concurrent guest.

Payload child limits are 600 s each, TERM then 15 s kill grace; allow at least
1230 s plus artifact-hash I/O for its watched owner. The checker already caps
inflated image at 16 GiB, SYSTEM at 4 GiB and ext4 storage at 512 MiB. Sequential
worst-case temporary payload capacity is 20.5 GiB plus metadata; reserve 24 GiB
additional scratch and a measured operating margin, separate from retained
inputs. This is a source-derived ceiling, not the 188 MB synthetic-test peak.
State-check child readers retain their 180 s limits. Serial clean proof remains
180 s; root supplies an outer 210 s owner bound. Installed hash capture is
read-only and bounded to the listed product files/module tree; budget 120 s.
Retained rehearsal needs a fresh single-guest allocation and lifecycle ceiling
chosen from actual update size (proposed 20 min), not an old owner reused.
Do not delete failed scratch before original results and causes are retained.

## Actual payload command — executable, not executed

Inputs are the actual frozen checkout, new owner, both final files and their
independently recorded whole-artifact hashes. `payload-check.sh` checks the
unchanged selected-state tool and retained SDK mcopy identity, uses a private
mcopy symlink and scratch directory, records each original child exit and JSON,
and verifies input hashes before/after inspection. No mount, cache mutation,
provider, publication or synthetic test occurs. Root wraps this in the existing
watch-build-submit/watch-job owner and consumes every original result.

```bash
TASK_PACKET=/workspace/repos/rocknix.worktrees/m7-candidate-compose/docs/qa-logs/2026-10-14-m7-installed-state-plan
# Set TASK_TREE, TASK_OWNER, TASK_UPDATE, TASK_UPDATE_SHA, TASK_IMAGE and
# TASK_IMAGE_SHA from the actual completed build/custody record, not filenames.
tools/watch-build-submit --owner "$TASK_OWNER" -- --record-only --activity-dir "$TASK_OWNER" -- bash "$TASK_PACKET/payload-check.sh" "$TASK_TREE" "$TASK_OWNER" "$TASK_UPDATE" "$TASK_UPDATE_SHA" "$TASK_IMAGE" "$TASK_IMAGE_SHA"
```

Required artifacts: `update.json`, `update.rc`, `install.json`, `install.rc`, both
stderr files, input identities, original owner/watch/launcher/runner exits and
scratch retirement. Both reports must be selected-policy pass with zero blocked
and error counts. #566 additionally requires a nonzero
`approved-shared-developer-identity` count for the actual ES ELF and zero
unapproved `developer-service-identity` count; a clean but unprovisioned binary
must not satisfy #566. The underlying checker intentionally allows absent shared
identity for other builds. This is a #566 assertion, not a changed gate policy.

At eventual release preparation, `tools/fork-publish-release --prepare` must
still inspect every selected final asset through the existing integration. Do
not bypass it with this receipt. Its candidate-store/qualification prerequisites
must be met first; this engineering plan is not a publication command.

## Fresh boot — existing exact adapter

Run from the actual frozen checkout; it must carry the bound checker/test pair.
Before intentional state or SSH seeding:

```bash
docs/qa-logs/2026-10-13-clean-state-565/run-first-boot.sh "$TASK_CLEAN_OWNER" "$TASK_SERIAL"
```

This invokes the real `--root / --mode first-boot --require-ready` checker by
inline serial script. Require original transport exit, exactly one
`PIX_STATE_565_RC=0`, JSON pass, zero blocked/errors and a clear/present boot-ready
row. Transport success alone does not establish guest success. Preserve
`first-boot.sh`, `first-boot.serial`, parsed JSON, boot/build identity and actual
process exits. The helper leaves only its small script under guest `/tmp`.

The gate is a host tool transmitted for read-only inspection, not a firmware
package. Do not invent an installed `/usr/bin/pixelelated-state-check` path.
It checks selected defaults/runtime, no personal identity/activity/QA residue and
the exact allowed current-boot zero-work scrub marker; it is not a universal
secret scanner. Clock/readiness/parser refusals remain failures to diagnose.
After this first untouched gate passes, ordinary QA setup may proceed.

## Installed source and executing identity chain

`installed-product-paths.txt` lists the minimum concrete product mappings for
this composition, all under immutable image roots. Capture their SHA256, bytes
and mode from the final post-install/strip image root, exact final SYSTEM and
both clean/updated guests; require exact equality. Do not hash player account
values or runtime settings for publication. Collect generated default system
listing and launcher bytes after their real post-install substitutions.

Also inventory every `.pyc` under
`usr/lib/python3.14/site-packages/raofflineproxy` and both Dolphin controller
profile directories under `usr/config/dolphin-emu`. Compare relative path sets,
bytes, hashes and modes across final install root→SYSTEM→guest. Require no `.py`
left in the shipped proxy package as the actual recipe uses `python_compile`
then `python_remove_source`. Prepared input remains the exact 112 Python source
files; do not compare their SHA256 directly to bytecode or import/marshal bytecode
under a mismatched host interpreter. Bind the source manifest to the actual
package build/bytecompile/install receipt, then compare the emitted bytecode.

Concrete existing reader commands, run under the allocated owner:

```bash
# Before boot, individual final SYSTEM file reads require no full extraction.
unsquashfs -cat -no-wildcards "$TASK_SYSTEM" usr/bin/emulationstation > "$TASK_OWNER/emulationstation.installed"
sha256sum "$TASK_OWNER/emulationstation.installed"
# Repeat the literal reader for each installed-product-paths.txt entry;
# inspect symlink metadata separately, never resolve image-absolute links in host /.
# Inside each guest, use serial or the newly allocated loopback SSH transport:
sha256sum /usr/bin/emulationstation /usr/lib/libraproxy_rchash.so
sha256sum /usr/bin/dolphin-emu /usr/bin/dolphin-emu-nogui
sha256sum /usr/bin/raofflineproxy-ctl /usr/bin/start_dolphin_wii.sh
cat /etc/os-release
```

Bind the final ES pin and actual compile definitions without publishing compiler
command lines containing arbitrary credentials: assert compiled shared developer
pair and runtime fallback define are present, no unintended developer/RA override,
and record booleans plus artifact identity. The real selected-state report
classifies the installed NUL-delimited shared pair. The final ELF/call-path/frame
proof is still required; a recipe grep or ELF substring alone is not URL behavior.
Capture ES PID/start ticks, boot ID, `/proc/<pid>/exe` target and its SHA256; it
must equal the installed ES, with no QA bind/interposer left active.

For the native proxy, bind current c7eb proxy / 143317 rcheevos / 607694 libchdr
and glue/flags to the real final build. Component ELF SHA
`6349b150899f7c32971b8d9ee882934e41f2f8fc9d6a129045e15ea62096d52c`
is accepted source provenance, not a forced final hash: strip/build metadata may
change emitted bytes. Preserve that transformation chain and compare final
post-strip install→SYSTEM→guest bytes. Inspect real DT_NEEDED/exports and runtime
loader closure; do not resurrect the older `source_pins_verified:false` receipt.
Record effective proxy unit/marker/default-off state before enabling it for
root's installed-service tests. These identity reads do not rerun #588 controls.

Full native Dolphin requires actual Qt/Wayland shared libraries and plugins,
including QtSvg. Inspect actual ELF dependencies, installed resolution and
Wayland plugin loading; old SDK cache or Qt recipe intent is not closure. The
normal recipe copies `Binaries/dolphin*`; uppercase `DolphinTool` is not copied
by that glob, so this plan does not invent a required installed DolphinTool path.
Existing accepted CLI format proof is separate from native gameplay acceptance.

## Retained-state update — exact missing evidence and command plumbing

Use accepted replacement20 image SHA
`1a23cf5740dbb69cdca76d753a0f6121c35e6e12f27649e792aeebc71e8cc490`
from its retained artifact bundle; resolve the current verified store path.
Never use the owner's Nova/storage or a retired guest disk. Seed a ready baseline
with synthetic values only, keeping automatic cloud sync and achievements off.
The required fixture surfaces are:

| Surface | Before update | After actual update |
| --- | --- | --- |
| Global RA username/password/token/key | Distinct synthetic nonempty fields; assert parser sees them | Exact selected values and presence unchanged |
| ES ScreenScraper user/password and existing runtime developer fallback fields | Synthetic XML fields, safely persisted after stopping ES | Values/presence unchanged; new compiled developer pair wins; personal rows stay distinct |
| ROM-side gamelist | Tiny inert ROM plus known playcount/lastplayed; same established metadata schema | Same game entry/selected fields; Recent derives from it, no emulator launch implied |
| Cloud operation stamps | Valid synthetic historical `last-backup`/`last-restore` records in exact writer schema | Original bytes unchanged; no actual backup/restore/provider operation inferred |
| Ordinary saved settings and save files | Existing upgrade rehearsal's marker/settings/save cases | Preserve existing generic upgrade evidence too |

The fixture must assert every seed before staging the update. Keep expected
values in memory or private synthetic fixture records; public reports contain
field names/counts/equality booleans, no credentials or credential-derived hashes.
Use a source-matched parser, not `grep` aliases or line order. Do not require whole
runtime config byte equality where startup legitimately adds new defaults.
Bind before/after boot IDs and root filesystem BUILD_ID to prove a reboot into
the candidate. Run the existing checker with `--root / --mode retained-upgrade`
after readiness; its pass permits retained runtime state but does not itself
prove preservation. `--require-ready` is intentionally first-boot-only; do not
pass it with retained mode. Check the actual autostart/mount/live-ES facts in the
new boot separately.

Transport and update command sequence, once root allocates the private guest:

```bash
# After baseline readiness, seeding and a positive before-state receipt:
# stage the verified update tar via the guest's fresh loopback SSH key/port
# or an already-owned read-only input disk, never via multi-GB serial base64.
scp -i "$TASK_KEY" -P "$TASK_SSH_PORT" "$TASK_UPDATE" root@127.0.0.1:/storage/.update/
# Verify the staged whole-artifact hash through the allocated serial transport.
# Then serial: sync; reboot
# Poll changed boot ID + exact expected BUILD_ID; verify real boot readiness.
# Then run the preserved seed comparator and retained-mode checker, collect
# installed identity, empty update queue and compact before/after reports.
```

`tools/vm-upgrade-rehearsal OLD NEW EXPECTED_BUILD_PREFIX` is the existing broader
upgrade entrypoint, but cannot close these criteria unchanged: it starts two
guests and a local cloud backend, seeds no RA/ScreenScraper account or activity/
gamelist case, and its `wait_for_storage` requires active
`rocknix-autostart.service`. Accepted #565 evidence already found the alternative
unit name and valid inactive/dead successful-oneshot shape. It also lacks a
single outer lifecycle bound. Root must prepare a narrow supplementary
seed/compare wrapper or a scoped derivative using the actual readiness contract;
this packet does not pretend that wrapper exists. The accepted replacement20
upgrade runner is historical evidence with old paths and must not be replayed.

## #566 installed UI, errors and backup — remaining exact work

Existing `vm-qa --only walks` has no ScreenScraper-specific composition.
`m7-retro-achievements.steps` is seeded #422 RA navigation, not a scraper walk.
Use existing `tools/vm-visual-qa` with a newly source-bound ScreenScraper steps
file; do not submit a fictitious `--walk screenscraper` name. Frames required by
current docs/es-menu-map.md: EN/FR 640×480 and 1280×800 accounts/options, normal
hidden developer rows and distinct player/service errors. Bind final source,
compiled definitions, actual ES ELF, mode/locale, flow precondition and reviewed
frames. Root's new conditional-copy fixture supplies the service-error source
proof; final normal build must show its corresponding actual error outcome.
Runtime fallback is a separately identified build path, not the normal compiled
image. Preserve existing fallback evidence where source applicability holds;
do not disable the shared pair in the final image to manufacture that result.

The actual API URL is fixed HTTPS (`ScreenScraper.h`), with no endpoint setting.
A deterministic actual-binary error/URL fixture therefore needs explicitly scoped
transport interception or an existing accepted equivalent. Record requested
endpoint category and separate developer/player fields as booleans; never log
raw query strings. A synthetic parser fixture alone cannot establish actual
requests. The source review found one hidden-control mismatch: PairRejected
unconditionally directed to developer entries hidden in compiled builds. Root
has assigned the minimal fix. Missing-runtime-developer prompt and post-restore
developer rows are already correctly conditional; player prompts name visible
rows. Offline/maintenance/quota/probe-unknown routes do not name hidden controls.
Stale no-image-key comments in ScreenScraper.cpp and CMakeLists.txt also need
reconciliation by that assigned worker. This packet makes no product edit.

For backup exclusion, reuse the installed `/usr/bin/backuptool backup` once with
synthetic ES player/developer password fields and harmless username/theme values.
Capture the original return code, locate the exact new `.tar.gz` under
`/storage/roms/backup`, and inspect its real archived
`storage/.config/emulationstation/es_settings.cfg`: passwords/dev password absent,
username and harmless setting preserved, no compiled ELF/default image files
included, source runtime values unchanged. Inspect selected RA/token exclusions
when sharing #565's retained fixture. No cloud upload is required. Existing
`last-good-scripts-test` lines 785–837 already prove the source strip rules;
do not rerun its entire synthetic suite as a replacement for installed behavior.
No existing narrow installed archive verifier was found; root must prepare this
small value-free comparator before running. Restore/setup frames use the same
compiled-vs-runtime developer-row distinction in GuiMenu.cpp.

Completion artifacts: actual payload JSON/rc, untouched ready clean report,
final source→package→SYSTEM→executing identities, real old→new before/after
selected-state equality, retained-mode report, installed backup-member report,
final #566 source-bound frame index and original lifecycle/retirement records.
Until those exist, these are open existing criteria, not provenance or RC PASS.
