# #565 selected-state gate source candidate

This packet delivers implementation source, not runtime qualification. Starting
distribution commit: `1a37cde40ab0893c9c21c0a383c59ac0c1403b06`, branch
`feature/m7-clean-state-565`. Only the two new tools, the release planner and this
packet change. The coordinator (w4:p2) owns shared records, GitHub, runtime and
integration. No old checkpoint command was replayed, private owner record read,
firmware extracted, fixture run, guest booted, build started or device/provider
contacted. No memory result or new Nova attribution is claimed.

The preceding revision `63e05cd728acd1d2a76dffc1c4b1d7fd75fa3fab`
corrected findings against
`a7a36c874930fb16a15197ef112e90f31820b225`: oneshot readiness, the shipped
runtime-locale link, Dolphin's ApiToken field, melonDS's explicit null sentinels,
and literal SquashFS filename reads. Revision
`ab47ce27166770d6e76a2857fd91e6d6f475d7fd` corrected the comment-only
RetroArch default and clean-startup scrub marker refusals. This revision narrowly
recognizes canonical unused ext4 directory slots after the coordinator's host
payload run failed at the positive-inode requirement. This lane has executed no
controls. Runtime and production integration remain coordinator-owned.

Can this be done on the VM? Yes: a disposable GENERIC_X64 guest can inspect its
own defaults and first-boot storage, and run the synthetic root controls. Host
payload controls need filesystem readers. Runtime remains reserved to the
coordinator; record the allocation and this answer in #565 before executing.

## Source delivered

- `tools/pixelelated-state-check`: JSON-only selected-state policy. Exit 0 passes
  the stated coverage, 1 means prohibited presence, 2 means incomplete,
  unsupported, unreadable or malformed input. No repair/deletion/config sourcing,
  provider call, upload or publication path. No credential-field hashes.
- `tools/pixelelated-state-check-test`: independent synthetic inputs and
  subprocess assertions, including unchanged bytes/modes before and after each
  root check. No import of the gate. The optional payload controls construct tiny
  filesystems and candidate bundles, exercising real readers and preparation.
- `tools/fork-publish-release`: after existing bundle/identity checks, invokes
  the gate on **every selected `.tar` and `.img.gz`**. Requires a complete policy
  pass, then re-verifies bundle bytes before returning a draft preparation plan.
  A caller cannot substitute a pass receipt or omit the check. Remaining
  qualification/custody/approval gates and prepare-only behavior remain.

Name selection followed inventory of existing `qa-accounts`,
`rasteratops-candidate-store`, `fork-publish-release`, `vm-qa`,
`vm-upgrade-rehearsal` and state/clean/credential-related tools. `qa-accounts`
mutates account state; its role is different from this read-only inspection.

## Coverage and allowed states

| Surface | Evidence reported | Clean-image / first-boot | Retained-upgrade |
| --- | --- | --- | --- |
| System/ES/RetroArch player fields | Populated account-field counts | Refuse | Runtime allowed; defaults still refuse |
| ES runtime developer fields, rclone client identity, known ES compiled URL pairs | Separate developer/service category | Refuse without inferring whose identity | Runtime allowed; compiled/default identity still refuses |
| Selected standalone INI fields and opaque token files | Account-field/file presence | Refuse | Runtime allowed |
| Rclone sections, selection, staged residue | Remote/connection categories | Refuse | Runtime allowed |
| Cloud device ID | Separate device identity presence | Refuse; does not assert copied origin | Runtime allowed |
| Cloud cache `last-*` stamps and other files | Activity/state presence, no date/status values | Refuse | Runtime allowed; malformed stamps still fail |
| Exact `log-scrubbed` marker | Separate startup, activity, preseed or retained category | Clean-image always refuses; first-boot requires complete zero-work current-boot record | One or both valid families, either order, allowed |
| Gamelists under selected config and `/storage/roms` trees | Counts of playcount and lastplayed fields indicating activity | Refuse | Runtime allowed |
| RetroArch history playlists, proxy cache | History/cache entry presence | Refuse | Runtime allowed |
| Known QA filename prefixes | QA residue indicator, masked policy path | Refuse | Runtime allowed; no author inference |
| Fresh `.img.gz` storage | Entries outside empty seed allowlist | Refuse | Not an upgrade input mode |

Required in defaults: system.cfg, es_settings.cfg, retroarch.cfg,
cloud_sync.conf, cloud_sync.conf.defaults, `/etc/retroarch.cfg`, and the ES ELF.
First-boot/retained modes additionally require the four runtime core configs and
`/storage/roms`. Optional account surfaces are enumerated even when absent.
Present malformed inputs fail; an empty settings file is not proof of clean
defaults. XML DTD/entities, conflicting config keys, broken/cyclic symlinks,
special files, mode-000 input and unsupported rclone option redirects refuse.
The parser reads data and never evaluates shell expressions.

Only `/etc/retroarch.cfg` may contain nonempty `#` comments/blank lines without
active assignments. The RetroArch recipe copies upstream's default to that path
(`package.mk:116-117`); the coordinator observed that form on untouched VM20.
The file must still be readable and regular. Missing, empty/whitespace-only,
NUL-containing, malformed assignments and include/reference directives refuse.
Sections or semicolon-only content do not qualify as this comment-only format.
Active account fields are still counted. System, cloud and runtime RetroArch
config requirements retain their existing strictness.

`cloud_log_scrub:48-57,179-206` documents and writes the exact marker
`/storage/.cache/cloud_sync/log-scrubbed`; `102-cloud-saves:22-29` invokes it
before capture or ES writes logs. On first boot the checker requires a regular
non-symlink file with exactly one `scrubbed` line followed by one
`es_log_scrubbed` line, each ending in a newline, with canonical unsigned
decimal fields, positive epochs, and files=0/lines=0. It reports
`startup-log-scrub`, presence true and count 0. Nonzero work is a separate
`cloud-log-scrub-activity` refusal, not a claim that credentials were present.
Malformed/incomplete records refuse; renamed, nested or temporary marker files
remain ordinary cloud residue. Every clean-image marker seed refuses, including
empty files and well-formed zero-work records.

For a zero-work first-boot record, epochs must be ordered and within the inspected
root's `/proc/stat` btime through btime + whole `/proc/uptime` seconds + 1. That
one-second upper rounding accounts for the writer's whole-second epochs. Missing,
unreadable, duplicate or malformed boot inputs refuse. The checker reads btime
before and after uptime and requires equality. Live proc files have size 0, so
these two fixed reads use bounded reads with type/permission/containment checks
instead of regular-file size equality. Offline roots require their own proc
snapshots; they cannot inherit the host's boot window. The fixtures provide an
independent synthetic clock and never need to modify the guest's proc files.
Clock steps can cause a conservative refusal. Matching epochs establish
consistency with a boot window, not the marker's origin; no timestamps or boot
identifiers are printed. `--require-ready` still checks unchanged boot identity.

For retained-upgrade, the writer's partial/retry behavior permits either family
alone or both in either order, each once. Its `record()` preserves existing lines
before appending: a failed cloud family followed by an ES success can become
ES-first/cloud-second on retry. Valid nonzero and historical records are
`retained-log-scrub` and allowed without a current-boot claim or clock requirement.
Duplicate families, unknown lines or malformed fields refuse. All inspection
remains read-only, and fixtures assert unchanged bytes/modes.

One source-backed clean-image exception is the exact two-link chain
`/usr/config/emulationstation/locale` → `/usr/share/locale` →
`/storage/.config/locale`, created by ES `package.mk:117-125`.
`userconfig-setup:80-88` populates the runtime target at first boot. Only when
that target is absent in clean-image mode does the gate report
`runtime-locale-deferred` and continue. It compares both raw link targets before
this exception; alternate targets, unrelated dangling links, traversal and
cycles retain refusal. Existing targets still undergo the normal walk, including
history/QA checks. A dangling target in first-boot or retained-upgrade mode
still fails. This adds no translation-content or arbitrary-secret coverage.

Static source inventory found one identical repeated `uzebox.integerscale` line
in shipped system.cfg and no duplicate keys in the 15 device RetroArch defaults.
The parser collapses exact repeats and rejects conflicting repeats; a synthetic
control covers both cases. No default configuration was changed.

Both defaults and runtime are checked independently, so an empty override cannot
hide a credential in defaults. Recovery/atomic siblings (including variable PID
suffixes) are included. Known standalone paths come from `backuptool`'s
RATOKENFILES/RATOKENSETTINGS and `cheevos_*` writers: PPSSPP, Dolphin, SkyEmu,
gopher64, ARMSX2, DuckStation, melonDS, Flycast and AetherSX2. Opaque token/cache
presence is deliberately conservative; its account validity is not tested.

Dolphin's `cheevos_dolphin.sh:57-67` writes `[Achievements] ApiToken`; the gate
now recognizes that field even when Username is absent. The melonDS writer
`cheevos_melonds.sh:35-53,99-101` and AMD64 `melonDS.ini:150-153` explicitly use
the sectionless, unquoted assignments `RA_Username=null`, `RA_Password=null`
and `RA_Token=null` for no account. Only those exact assignments in the selected
melonDS INI path (including its recovery siblings) are empty sentinels. Quoted
null, changed spelling/case, INI sections and other emulator paths do not gain
that exception. Populated username, password and token each have an independent
control; retained runtime data remains allowed and unchanged.

Reports use literal policy paths/wildcards, categories, booleans and counts.
They never echo remote names, game names, dynamic filenames, XML attributes,
config values, parser errors, child diagnostics, or secret-derived digests.
The existing release manifest's whole-artifact identity is separate from this
gate's report; no digest of an account setting is generated.

`retained-upgrade` is an inspection mode, not a wipe/migration. The gate cannot
delete or rewrite user state. Synthetic controls assert byte/mode preservation
while account/history presence is allowed. This does **not** prove an actual OS
upgrade preserves the account: the coordinator still needs a separately seeded
disposable retained-storage rehearsal and before/after in-memory or private
value-free equality evidence. No owner account should be used for it.

## Reader boundaries and blockers

Update archives: one normal root with one regular `target/SYSTEM`, no traversal,
duplicate members, symlink/hardlink members, or separate storage/config tree.
SYSTEM is copied to private temporary scratch; `unsquashfs -lln/-cat` reads the
selected surfaces without extracting the filesystem. Only the known compiled
ScreenScraper and RetroAchievements query-pair shapes are checked in ES.
Every cat read uses `-no-wildcards`, so a bracketed filename cannot read a clean
glob-matching sibling. The installed unsquashfs manual documents the flag;
literal cat behavior remains an allocated-runtime verification item. A real
synthetic SquashFS control contains contaminated `system.cfg.bak[1]` alongside
clean `system.cfg.bak1`, requires a blocked account row, and also requires release
preparation to refuse that exact payload. Unsupported reader flags fail closed.

Install images: gzip stream, DOS/GPT table with two nonoverlapping 512-byte-sector
partitions, FAT SYSTEM read with `mcopy`, and an ext4 storage seed checked with
`e2fsck -fn` / `debugfs` read-only commands. Storage may contain only directory
entries, empty `lost+found`, and an empty `.please_resize_me`; extra entries
refuse. Disk inflation uses sparse zero writes, capped at 16 GiB; SYSTEM at
4 GiB; storage partition at 512 MiB. There is no mount, loop device, appliance VM
or full cache copy. Temporary payload copies are removed when the call ends.
Abrupt host termination can leave scratch; the coordinator owns that cleanup.

Native debugfs 1.47.2 emits `/0/000000/0/0//0/` for unused slots in a freshly
allocated empty `/lost+found`. The parser skips only that exact record, including
repeated slots, before validating live entries. Any other zero-inode shape still
fails: names, live modes, ownership, nonzero sizes, alternate spelling or malformed
fields do not receive the exception. Positive-inode `.` and `..` remain required;
live entries beside unused slots still count as storage residue. This does not
change the allowed storage seed or the required `e2fsck -fn` validation.

The original PATH inventory lacked `mcopy`; the coordinator now supplies an
existing read-only utility through its allocated PATH without installing it.
Other fixture dependencies are checked before execution. No dependency was
installed or cache copied by this lane. The coordinator's ab47 host run passed
clean tar inspection and release preparation before refusing clean install-image
inspection on the unused slots. Native clean/dirty images remain the real-reader
controls. Eleven additional controls substitute only debugfs listing output via
a temporary PATH shim, using a real synthetic image and the normal payload CLI;
they are explicitly synthetic API controls, not evidence of native reader behavior.
Missing tools and unrecognized output refuse. No network operation belongs to the gate.

This is not a whole-image secret scan. Arbitrary secrets, compiled raw
GamesDB keys, unknown binaries, shell/build environment overrides, arbitrary
archives, custom ES system paths and external libraries/media are not covered.
Known QA prefixes are indicators, not an exhaustive catalog. The selected
configuration grammar is intentionally strict; an unsupported legitimate format
needs a source-backed parser change and fixture, not a bypass. Newly generated
first-boot device IDs and unrecognized cache records may require a policy
refinement after their actual writers are identified; their presence still refuses.
The next guest result is therefore an experiment, not a promised pass.

## Nova explanation retained from the accepted record

The complete #565 body and three comments were read on October 13, together with
`../2026-10-13-nova-feedback/` and `../2026-10-12-owner-feedback/`. No new private
provenance was collected. The September 30 backup/restore dates match retained
local operation evidence: restore found an absent location and completed empty;
backup transferred zero bytes. Successful completion stamps do not establish a
data transfer or identify the initiator. Nova's first fork install was an update
over existing ROCKNIX storage.

The two Recent entries contain positive playcounts and lastplayed dates from
before that first fork update. Accepted ES
`c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`,
`CollectionSystemManager.cpp:1043`, selects Recent using `PlayCount > "0"` as a
string comparison. `MetaData.cpp:84-85` defaults both fields to `"0"`.
`SystemData.cpp:1648` first checks the system ROM folder, then the ES gamelists
folder. Those paths and a lexical `00` control are reflected in this candidate.
Imported metadata can satisfy membership without a local launch. The metadata
arrival path and original account-entry author remain unknown. A preserved
upgrade, gamelist mtime or empty-default spot check cannot settle that origin.

## Coordinator evidence for earlier revisions

The coordinator ran frozen `63e05cd728acd1d2a76dffc1c4b1d7fd75fa3fab`
synthetic-root controls in its disposable guest: PASS 68/68, guest exit 0, empty
stderr, reported 3.52 seconds. This lane read the saved report at
`/workspace/tmp/pix565-clean-state-20261013/controls-owner/controls-result.json`
and confirmed its report/count, guest exit and stderr-empty fields. That result
does not qualify the new controls or this revision.

The untouched VM20 first-boot check of that same source exited 2. Its report at
`/workspace/tmp/pix565-clean-state-20261013/first-boot-owner/first-boot.serial`
has readiness clear, an input error at `/etc/retroarch.cfg`, and one cloud cache
residue refusal. The coordinator classified the two actual inputs: a regular
0644, 34,090-byte, comment-only default with zero active assignments, and the
two zero-work startup scrub lines. The saved classification evidence is
`/workspace/tmp/pix565-clean-state-20261013/classification.serial` and
`classification02.serial`. This lane inspected those saved files without
printing marker epochs or account values. No new guest, fixture, tool import or
runtime command was run here. No new first-boot pass is claimed.

The coordinator subsequently reported frozen
`ab47ce27166770d6e76a2857fd91e6d6f475d7fd` first-boot `--require-ready`
PASS/exit 0 with the normal zero-work startup marker, and root controls
PASS 113/113, guest exit 0, empty stderr, 5.90 seconds. Result/wrapper/watcher
channels and host exits were consumed; the exact VM was retired. No QA SSH key
or storage fixture was staged. These are earlier-source receipts, not a pass for
this revision. No result artifact path was supplied for those passes in the
coordinator message, so this lane records them as coordinator-reported.

The later ab47 host payload failure reached `empty_ext4` through the clean
install image and refused its empty `/lost+found` listing. This lane read
`/workspace/tmp/pix565-payload-diagnostic02-20261013/empty-directory-listing.json`:
two positive-inode directory entries (`.` and `..`) and three exact canonical
unused slots, with no other records. The original failures/results remain with
the coordinator. This correction has no executed payload receipt yet.

## Next executable experiment (coordinator only)

Use a **fresh** owner directory and a coordinator allocation, never an archived
owner. The prior VM is retired. The next experiment is host `--payload-tests`
against this exact source, using the coordinator's existing read-only mcopy PATH;
it runs root controls, native clean/dirty install images and the synthetic listing
controls. Set the given TMPDIR. These commands are prepared for the new revision
and have not been executed against it:

```sh
export TMPDIR=/workspace/tmp/pix-m7-investigation-20261013/tmp
tools/pixelelated-state-check-test --payload-tests > "$OWNER/payload-controls.json"
tools/fork-publish-release --prepare "$BUNDLE" > "$OWNER/release-plan.json"
```

The release command itself performs the final accepted payload check; run it
against the allocated immutable bundle, not a source tree or old triage receipt.
It prints no plan if the gate refuses an asset. Confirm the watcher, command and
wrapper exits before accepting the result. No preparation authorizes publishing.

Boot that exact accepted GENERIC_X64 image with fresh 16 GiB+ storage. Record its
image/source/boot identity separately, wait for autostart/frontend readiness, and
enter no account or library data. No image/port/guest is allocated by this packet.
The prepared first guest command, sent by the helper inline with this exact gate
source, is:

```sh
python3 -B -c '<inline base64-decoded gate source>' --root / --mode first-boot --require-ready
```

The original candidate `a7a36c874930fb16a15197ef112e90f31820b225` incorrectly
used `is-active rocknix-autostart.service` alone. Coordinator source review
reported that VM20 provision readback instead shows `autostart.service`
inactive with `Result=success`. No runtime was allocated to this lane. The
tracked source unit and the accepted VM20 cache's
`build.pixelelated-GENERIC_X64.x86_64/image/system/usr/lib/systemd/system/rocknix-autostart.service`
both have `Type=oneshot`, `RemainAfterExit=yes` and ExecStart invoking
`/usr/bin/autostart`. The cache contains no `autostart.service` at that checked
path. This source/observed-unit discrepancy remains explicit; no alias,
replacement, boot history or effective runtime unit definition is invented.

The corrected readiness check queries both known names and requires one loaded
unit identity running the expected autostart script; aliases may collapse to
that same identity. A successful completed oneshot can be active/exited **or**
inactive/dead. It must also have `ExecMainCode=1`, status 0, ConditionResult=yes
and nonzero ordered monotonic execution timestamps within the current uptime.
An unstarted unit's default `Result=success`, an absent unit, failed/skipped
execution, two distinct loaded runners or unsupported unit shape cannot pass.
No property values or unit diagnostics are printed on failure (`boot-not-ready`).

Source `projects/ROCKNIX/packages/sysutils/autostart/sources/autostart` starts
`rocknix-automount`, runs the config startup scripts, then creates
`/var/lock/start.games` and starts the UI. `automount` binds/mounts the ROM tree;
the frontend services then start ES. The guard therefore additionally requires
`/storage` and `/storage/roms` in mountinfo, the start.games
marker, one live `/usr/bin/emulationstation`, and unchanged boot identity through
inspection. Merely changing the hard-coded unit name or accepting any successful
inactive unit would not establish these prerequisites. The coordinator's frozen
63e run passed readiness on VM20; ab47 passed the full first-boot check including
the scrub boot-window reader. Those earlier-source receipts are preserved above.
Source/AST checks of the current correction are in `static-validation.json`.

The executable serial adapter is `run-first-boot.sh` in this packet:

```sh
docs/qa-logs/2026-10-13-clean-state-565/run-first-boot.sh "$OWNER" "$SERIAL_SOCKET"
```

It prepares a fresh script, uses existing `tools/vm-serial`, and requires the
JSON pass, the boot-ready check and the explicit guest exit marker. `vm-serial`
alone reports transport success, not the child command's exit. The serial tool
leaves its small generated script under guest `/tmp`; no fixture is planted in `/storage`.
The gate must run before any intentional test accounts/history are seeded.

Failure controls include player/runtime/default/recovery identity, separate
service identity, configured and malformed/encrypted remotes, empty-operation
stamps, imported and malformed gamelists, lexical playcount, standalone tokens,
proxy/QA residue, playlists, retained allowance, missing/empty/unreadable files,
duplicate keys, XML entities, redirection, symlink cycles and FIFO input. Payload
controls cover real clean/contaminated SquashFS/tars with the exact shipped
locale chain, altered/escaping locale links, literal bracketed filenames,
empty/contaminated ext4 install images, malformed/traversal/duplicate archives,
missing readers, and actual clean/contaminated release preparation. Dolphin
ApiToken-only and melonDS exact sentinel/populated/near-sentinel root controls
exercise the independent account-parser fixes. No fixture uses a real credential.

New controls cover comment-only defaults plus active-account, include/reference,
NUL, empty and malformed counterexamples; system/cloud/runtime requirements;
zero-work scrub recognition, stale/future/reversed epochs, nonzero work,
missing/duplicate/unknown families, malformed fields and boot snapshots,
unreadable uptime, symlinks and renamed residue. Retained cloud-only, ES-only,
cloud-first and ES-first retry records pass only their supported grammar and
retain their bytes/modes. First-boot rejects the partial/reordered forms. The
payload controls now exercise comment-only defaults and a zero-work marker
preseed inside a real synthetic SYSTEM. The self-test contains 113 expected root
controls (110 named cases and three argument/root refusals), previously passed
on frozen ab47 by the coordinator. The new unused-slot correction adds eleven
payload reader controls; no control has run against this new source yet.

## Coordinator-owned follow-through

Proposed fork-only tool registrations: add `tools/pixelelated-state-check` and
`tools/pixelelated-state-check-test` to `.githooks/pre-push` PERSONAL_PATTERNS and
the canonical `.claude/rules/fork-workflow.md` list, then regenerate the AGENTS
summary through the normal coordinator workflow. This lane did not edit them.
Record this source candidate/limits in #565, the work log/index and session
checkpoint as appropriate. No new policy decision or issue closure is asserted.
After runtime results, retain a compact source-bound packet; integration and
broader CI, upgrade evidence and all publication gates remain coordinator-owned.
