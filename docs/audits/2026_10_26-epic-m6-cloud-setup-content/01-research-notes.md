# Research notes — M6.P2 T17 (#664)

## Scope

**The membership block** (brief § 2, copied verbatim as `stage-a/scope.py`; run as r01 at 06:1x UTC on 2026-10-26):

```
paths 14 lines 11180 {'shipped': 14} {'fork-own': 14}
{'recipe': 1, 'c': 1, 'python': 4, 'shell': 8} {'cloud-sync-and-saves': 14}
the rclone directory in the inventory 25 16518 of which this slice's 11 8202
27 recipe fork-own projects/ROCKNIX/packages/network/cloud-signin-window/package.mk
1052 c fork-own projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c
258 python fork-own projects/ROCKNIX/packages/network/rclone/sources/cloud_connections.py
799 shell fork-own projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup
1589 shell fork-own projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore
158 shell fork-own projects/ROCKNIX/packages/network/rclone/sources/cloud_content_transfer
401 shell fork-own projects/ROCKNIX/packages/network/rclone/sources/cloud_device_id
278 python fork-own projects/ROCKNIX/packages/network/rclone/sources/cloud_folder_validate
206 shell fork-own projects/ROCKNIX/packages/network/rclone/sources/cloud_log_scrub
2830 python fork-own projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth
345 python fork-own projects/ROCKNIX/packages/network/rclone/sources/cloud_remote
362 shell fork-own projects/ROCKNIX/packages/network/rclone/sources/cloud_scan
976 shell fork-own projects/ROCKNIX/packages/network/rclone/sources/cloud_setup
1899 shell fork-own projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
14
```

**14 paths, 11,180 lines; read 14 / 11,180; tier fork-own 14; reach shipped 14.** By language: shell 8, python 4, C 1, recipe 1, all in area `cloud-sync-and-saves`. The rclone directory holds 25 inventory rows (16,518 lines), 11 of them this slice's (8,202 lines); the other 14 are T16's, and the two slices share no path. `stage-a/paths.txt` is the list, one path per line.

**Lines, modes and functions** (r02 to r05): 11,180 lines; modes 10 × `100755` and 4 × `100644`. Shell function definitions:

| File | Strict `^[a-z_]+\(\) \{$` | Loose `^[a-z_]+\(\)` |
| --- | ---: | ---: |
| `cloud_content_backup` | 17 | 22 |
| `cloud_content_restore` | 27 | 39 |
| `cloud_content_transfer` | 4 | 5 |
| `cloud_device_id` | 16 | 16 |
| `cloud_log_scrub` | 3 | 6 |
| `cloud_scan` | 11 | 17 |
| `cloud_setup` | 15 | 19 |
| `backuptool` | 19 | 23 |
| **total** | **112** | **147** |

Python: `cloud_oauth` 89 defs and 7 classes, `cloud_remote` 13 and 0, `cloud_folder_validate` 10 and 1, `cloud_connections.py` 12 and 1: 124 defs, 9 classes. The lane uses the strict count where a function count is cited.

### The provenance correction to the order

The inventory's tier is fork-own for all 14, and for thirteen that is the whole story: none of them exists in upstream `651150fc88` or in the base `c445081a59` (r29: only `backuptool` is present in either, once in each).

- **`backuptool` is the exception:** upstream and the base carry an identical **68-line** script of that name (r30: `68`, `identical`). The fork's is 1,899 lines after **79** non-merge commits since the base (r28).
- `git diff --stat 8ebaf8daad 651150fc88 -- <the 14>`: `14 files changed, 26 insertions(+), 11138 deletions(-)` (r31).
- Nothing upstream-carried is left in `backuptool` to disposition (D-WORKFLOW-209 reaches nothing here). What it means for the upstream PR bucket is the coordinator's question, cited, not decided.

### The history

`git log --no-merges c445081a59..8ebaf8daad -- <the 14>` (r25 to r27):

- **284 commits:** Max Engel 265, blitterbot 12, rasterabot 7;
- **from 2026-07-25 to 2026-10-13**;
- `--since='2026-06-01T00:00:00Z'` on `8ebaf8daad`: the same 284.

### The callers outside the 14

`git grep -l -w <name> 8ebaf8daad -- projects packages`, the 14 excluded (r32): **19 distinct files.**

```
projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm
projects/ROCKNIX/packages/multimedia/gstreamer/gst-plugins-base/package.mk
projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl
projects/ROCKNIX/packages/network/rclone/autostart/102-cloud-saves
projects/ROCKNIX/packages/network/rclone/package.mk
projects/ROCKNIX/packages/network/rclone/sources/cloud_backup
projects/ROCKNIX/packages/network/rclone/sources/cloud_capture
projects/ROCKNIX/packages/network/rclone/sources/cloud_restore
projects/ROCKNIX/packages/network/rclone/sources/cloud_saves_root
projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf
projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults
projects/ROCKNIX/packages/network/rclone/sources/rasteratops-settings-archive
projects/ROCKNIX/packages/rocknix/package.mk
projects/ROCKNIX/packages/rocknix/profile.d/001-functions
projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig
projects/ROCKNIX/packages/rocknix/sources/scripts/factoryreset
projects/ROCKNIX/packages/rocknix/sources/scripts/run
projects/ROCKNIX/packages/rocknix/sources/scripts/setrootpass
projects/ROCKNIX/packages/sysutils/systemd/scripts/network-base-setup
```

- **The install** (r33): `rclone/package.mk:67-75`, `:82` and `:88` copy the eleven scripts into `/usr/bin`; `:22` pulls in `cloud-signin-window` and `webkitgtk`.
- **The boot hook** (r24): `autostart/102-cloud-saves:29` runs `cloud_log_scrub` when it is executable.
- **The fork's tools** that name these files, by whole-word line count at `8ebaf8daad` (r34):

| Tool | Lines naming the 14 |
| --- | ---: |
| `cloud-connections-test` | 3 |
| `cloud-input-test` | 2 |
| `pixelelated-cloud-validator-test` | 22 |
| `pixelelated-content-scope-test` | 21 |
| `pixelelated-save-layout-test` | 16 |
| `signin-memory` | 4 |
| `cloud-round-trip` | 139 |
| `cloud-census` | 1 |
| `vm-qa` | 5 |
| `pixelelated-vm-cloud-boundaries` | 19 |
| `last-good-scripts-test` | 361 |

  The invoking lines are read at stage B, with the rclone each runs. `tools/cloud-connections-test` runs the host's rclone, not the image's (T13's Q2).
- **T13's oracle rows** that name this slice's scripts within its `02` § Assertion shapes: **5** (r35).

### The T16 / T17 seam, from this side

A call site is this slice's; the callee's internals are the callee's slice's.

- **`cloud_scan`** runs `cloud_content_restore --scan` and `--systems`, and `cloud_setup --folder-state` (all here). It sources `rasteratops-settings-archive` at `:328` (T16's).
- **`cloud_backup`** (T16's) calls `cloud_remote active`, `cloud_device_id` and `backuptool` (here). What each hands over and what it does with the answer is read here; the caller's reasons are T16's.
- **What these files source** (r38):

| File | Sources |
| --- | --- |
| `cloud_content_backup` | `/etc/profile` (`:21`), `cloud_content_transfer` (`:234`, `\|\| exit 1`) |
| `cloud_content_restore` | `/etc/profile` (`:25`), `cloud_content_transfer` (`:281`, `\|\| exit 1`) |
| `cloud_content_transfer` | nothing (it is sourced) |
| `cloud_device_id` | nothing |
| `cloud_log_scrub` | `/etc/profile.d/001-functions` (`:67`, errors dropped) |
| `cloud_scan` | `/etc/profile` (`:39`, errors dropped), `${archive_tool}` (`:328`) |
| `cloud_setup` | `/etc/profile` (`:44`) |
| `backuptool` | `/etc/profile` (`:8`) |

  None sources T16's `cloud_sync_helper` or a file defining `conf_valid`, `cleanup`, `finish` or `usage`.

## Deltas from the brief

1. **15 `.$$` lines in the 14, not 14** (r16). The fifteenth is `cloud_content_restore:819`, the `printf` line that opens the match plan's temp write; `:820-821` are its `mv` and `rm`.
2. **`backuptool:224` sweeps `"${STAGING_PREFIX}"*`, not `${STAGING}`.** `STAGING_PREFIX` is `/storage/.cache/backuptool-staging.` (`:762`), the script's own staging prefix, so the brief's *"every one on a script's own temporary"* holds. The prefix is defined below `sweep_leftovers()`, which runs after it is set.
3. **r07 greps the whole rclone directory**, as the brief writes it, and so prints T16's four constants as well. Within the 14 the constants are as the brief says.
4. **`tools/vocabulary-check`'s default EmulationStation checkout exists** on the host, and `ES_SRC` is unset. The lane did not read it and records `CANNOT` (r37), pending the coordinator's word on whose worktree it is.
