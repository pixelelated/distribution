# Explicit cloud folder setup — distro evidence (#508)

The distro no longer installs the migration engine. Folder scans read the selected
paths and never join or follow another device. Seeding creates the selected folders
and README files without changing credentials or pointers. Fresh defaults remain
`/pixelelated`; the normal save, settings, and selected content transfer tools remain.
ES removal, UI proof, QA caller compatibility, and atomic integration are separate
coordinated changes. This packet does not establish a new assembled firmware image.

## Source and behavior contract

`source-manifest.json` binds the base, changed source, supporting scripts, and harnesses.
`package-install.json` records the actual `makeinstall_target` staging output, including
source-equal scripts, modes, templates, and absence of `cloud_migrate_layout`.

`cloud_setup --folder-state` emits `STATE=ready|missing|no-remote`, `SAVES`, `BACKUPS`,
`CONTENT`, and `SAVES_EXISTS`. A missing selected folder is a successful observation;
no remote or an unreadable configuration/provider is nonzero. The scan has three
units as before. It does not choose a different content folder.

`--seed-folders` returns zero only after successful directory and README publication
and final readback. A failed mkdir, README write, marker operation, or final readback
is nonzero. This is a deliberate correction to older seeding that could print
`MISSING` but still return success. README files and existing payloads are retained.
Known default markers remain readable; unknown/malformed/unreadable markers refuse
before creation. A case variant is default only when backend features say it folds
case; an unknown answer refuses. Marker paths use the selected parent's actual
spelling, preserving the leading-slash semantics of SFTP. Literal root selections
remain roots; dot-only relative selections refuse rather than becoming defaults.

## Evidence and limits

- `host31/result.json`: all 31 isolated real-rclone cases passed on final script
  `67c6f9be8b2c30ad903139ee34be3ccfb64dcf7b462e1abbf0c0ec648d3860b6`.
  This includes fresh setup beside legacy data, legacy/current/custom selections,
  missing paths, explicit root content, case/relative marker handling, refusals,
  explicit setters, partial local libraries, settings archive roundtrip, and an
  interrupted-layout record at `/storage/.config/cloud-layout-migration.json`.
  The record's fields/fingerprint are synthetic; its exact bytes are kept unchanged.
- `old-scan-control/result.json`: the same no-follow assertion fails against
  `7cfdf9f73ae2a064ee4f281461e661301cb2dd65` because the old scan rewrites the pointers.
  Its watched exit1 is the expected negative control, not an infrastructure failure.
- `old-dot-control/result.json`: exact predecessor `7b3e080a…` demonstrably creates
  fresh default paths for dot-only saves/backups while leaving the selected config
  unchanged. Both observations are required by the negative control.
- `vm13-pre-dot/result.json`: 13 real guest/WebDAV cases passed on candidate16's
  hash-verified source overlay with `cloud_setup` `7b3e080a…`. The only subsequent
  product delta is dot-only path refusal. `final-dot-guards.log` proves all six
  read/seed refusal checks and unchanged settings under final `67c6f9be…` in the same
  guest; `dot-provider-unchanged.log` is the UI owner's unchanged synthetic endpoint
  hash receipt. The combined UI packet is under
  `docs/qa-logs/2026-10-07-manual-cloud-setup/es-ui/` in the integration work.
- `vm02-runner.py` matches the runner's recorded SHA256 `6f44f36e…` before the two
  post-run harness changes: correcting the startup-toggle spelling (ES was stopped
  for every script proof), and adding the focused dot cases for future replays.
  The archived bytes were reconstructed by reverting those two edits and checked
  against the previously measured hash; they were not copied at submission time.
- Provider case-folding outcomes are explicit feature controls on an isolated host
  filesystem. They do not claim authenticated Dropbox or a real case-folding server.
- `watched-runs.json`: every distro-owned launcher, runner, command, and watcher
  process exited. Earlier runs are identified as superseded. No personal device or
  cloud operation was part of this work.

The synthetic host payloads and temporary recipe installation were removed after
receipts. The one VM was handed exclusively to the ES/UI owner for its matrix and
final cleanup; this packet does not claim that cleanup is already complete.

## Reusable execution

Can this be done on the VM? Yes — #508 records candidate16 overlay and local synthetic
provider proof. Host controls are fast regressions; they do not substitute for VM or
assembled-image qualification. Use an unused private owner and actively consume its
watcher, runner, wrapper, and assertion results.

```sh
mkdir -m 700 /tmp/pixelelated-folder-host-new
mkdir -m 700 /tmp/pixelelated-folder-host-new/artifacts
tools/watch-build-submit --owner /tmp/pixelelated-folder-host-new -- \
  --activity-dir /tmp/pixelelated-folder-host-new/artifacts --recursive-activity -- \
  tools/pixelelated-cloud-folder-test \
  --output /tmp/pixelelated-folder-host-new/artifacts \
  --rclone /absolute/path/to/the/image/usr/bin/rclone --retire
```

For the VM, `tools/pixelelated-cloud-folder-vm-test --help` documents image checksum,
fresh owner, isolated ports, and optional sequential UI handoff. Its default run
stops and removes successful disposable payloads. `--keep-guest` transfers cleanup
responsibility with `guest.json`; never leave that guest without a named next owner.
A correction may reuse that exact guest with `--reuse-guest --evidence <fresh-dir>`;
its PID/disk/port identity is checked first. Every new run gets a fresh watched owner.
The final runner contains all 16 rows, including the three dot-only tier controls.

Neither a source overlay nor a staged package installation proves final artifact
inclusion. Integration must ship the matching ES removal and scripts together,
then record the chosen image's source/artifact mapping.
