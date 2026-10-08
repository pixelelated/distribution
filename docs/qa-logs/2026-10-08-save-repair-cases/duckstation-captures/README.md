# DuckStation captures, executable packaging, and runtime closure — #521–#523

Product commit: `dda2a04aaf411b8bc13aedf5ce44ff33ce4b3d3a`.
Parent: `1ee8e5199da0bc02e6aa4ebff94b951f5e8b4804`.
The exact package files, modes, and config-directory symlinks are in
`frozen-inputs.json`; `static-checks.json` verifies their equality, Python and
shell syntax, package lint, and scoped whitespace checks.
The separate dependency commit is recorded in `dependency-final-inputs.json`;
it changes only the recipe dependency list. All capture helper, entrypoint, and
seed hashes remain equal to the original frozen manifest.

## What changes

Both shipped entrypoints call the same packaged Python helper. New config seeds
use `/storage/roms/screenshots`. Retained missing, empty, or exact `screenshots`
defaults are rewritten only after the destination accepts an actual temporary
write. Explicit custom settings and a symlink redirecting the old screenshot
directory remain unchanged. The helper does not inspect or relocate captures.

Config reads are bounded to 1 MiB and require a regular file. Duplicate relevant
keys/sections and malformed section boundaries are refused. A replacement is
staged beside the config, fsynced, checked against the original file identity and
bytes, and atomically renamed. Failure removes partial staging and a newly made
empty target. Existing unselected files remain untouched by screenshot
preparation. The game launcher has older unrelated config/savestate/card handling;
this packet does not describe those operations as a new general migration.

The package installs its unchanged AppImage bytes with mode 0755, keeps the
existing strip guard, and declares Python3 for the helper. The source download
cache is not changed. This repairs executable permission independently of later
loader/runtime prerequisites.

## Retained host controls

Can this be done on the VM? Yes. Disposable host namespaces qualify actual
launcher/package functions and local rclone behavior; the separately owned
GENERIC_X64 guest must prove the actual AppImage and screenshot action.

- `final02/summary.json`: **31 PASS, zero FAIL**, bound to exact source, harness,
  and rclone hashes. Both entrypoints; new seeds from InputPlumber/H700/AMD64;
  absent config directories; retained missing/empty/default/CRLF settings;
  explicit relative/absolute custom paths and old-directory custom symlinks;
  duplicate/oversize/nonregular config and conflicting/read-only target/config;
  forced atomic rename failure with partial-temp cleanup; repeated-launch
  stability; real-rclone capture backup/restore; actual package-function install.
- `old02/summary.json`: **four expected failures** against the parent commit.
  New and retained ordinary captures resolve outside `/storage/roms`, and the
  original recipe preserves source mode 0644. Its `installed-execution.json`
  records direct execution permission refusal. Source bytes/mode stay unchanged.
- `installed-mode-and-refusal.txt`: independent original accepted-image witness,
  pinned x64 AppImage bytes at mode 0644, direct execution exit 126.
- `host-watchers.json`: watcher logs, return codes, and status for all host runs.
  `smoke01` is a sandbox namespace-creation refusal, not a product failure;
  `smoke02` is the authorized isolated rerun. Earlier successful controls remain
  historical; final02/old02 are the final harness-bound pair.

Each case retains literal operations, before/after storage manifests, final
cloud/storage hashes, and fixture retirement receipts. The emulator boundary in
the host harness is an explicit path/capture probe. Its synthetic bytes are not
a rendered image or loadable save. Actual rendered screenshot evidence is a
separate VM requirement. Real-rclone backup/restore here uses local synthetic
roots, never a personal cloud or account.

## Historical captures and custom paths

Existing captures under `/storage/.config/duckstation/screenshots` remain there.
Changing the default does **not** back up those historical bytes. A player who
wants them in saves backup coverage must review and copy selected captures into
`/storage/roms/screenshots`, resolving filename conflicts explicitly, then verify
the copied bytes and a normal backup before choosing whether to remove originals.
No such copying or removal is automated by this change or qualification.

An explicit custom path or custom old-directory symlink remains the player's
choice. If that destination lies outside the configured saves source, this change
does not add it to saves backup. The exact source tree determines coverage;
neither an emulator screenshot setting nor a successful launch proves backup.

## Runtime boundary

Final firmware inclusion remains pending. The actual pinned AppImage outer
runtime succeeds with the corrected mode (`--appimage-offset` and version).
Its bundled application loader then reports missing `libcom_err.so.2` on the
accepted image. `runtime-initial-elf-closure.json` retains all 121 bundled
ELF/plugin hashes and loader readbacks: this is the only missing SONAME, with no
other version-resolution failures. Root filed #523 before the package dependency
addition. The isolated package owner and command are recorded by
`dependency-owner.json`, `dependency-owner-prepare.py`, and `dependency-build.sh`.
No successful screenshot or gameplay result follows from the host PASS counts.

The #523 native package build and normal `scripts/install libcom-err` completed
with exit 0 in that isolated owner. `dependency-build/` retains watcher logs,
configure/compile commands, build/install stamps, and all installed ELF metadata.
The three installed names are identical 14,480-byte ELF64 x86-64 target files,
SONAME `libcom_err.so.2`, SHA-256
`043101a87e5eaa57b786b88dfbd227be2d7768445d53b69346b547fef2e938a3`.
They appear in both package staging and the isolated image staging; the library
requires only `libc.so.6`. No host-library bytes were copied into target output.
The build ran with one compiler job and host root read-only except its own source
owner, after guarded swap maintenance and a successful preflight. The initial
preflight refusal remains recorded. `dependency-recipe01` rechecks the actual
DuckStation package function after the sole dependency addition; it passes.

Actual application startup, native screenshot, and controller input evidence is
owned separately by the VM worker under `vm-ui/`. Its results must be read before
claiming those runtime requirements complete.
The qualified target library allowed the actual pinned application to print its
version/usage. That tag intentionally returns exit 1 for `-help`, as documented
by `pinned-help-exit.json`; the help status is neither an unresolved loader error
nor proof of a running emulation session.

`vm-helper/` retains the exact installed-helper success/refusal runner and
readbacks. On the owned accepted-image guest, first default rewrite took
60.09 ms; seven unchanged-default calls took 25.57–32.90 ms. Explicit custom
settings stayed unchanged. A read-only target returned 1 with config bytes
unchanged, and the historical capture sentinel remained intact. This measures
only helper execution, not whole-emulator startup, gameplay, or image time to
play. The helper/source overlay is separate from final firmware inclusion.

`synthetic-display-rom.py` is a wholly original 512 KiB reset-ROM builder for a
bounded screenshot-writer proof: MIPS GPU setup plus a spin loop, with no copied
commercial BIOS/game bytes. Executing that fixture can prove a rendered capture
path and hotkey, not game/save compatibility.
