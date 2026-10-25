# Retrospective — M6.P2 T22, the OS's system services and platform quirks

**Auditor:** Code Auditor skill, primary Claude Opus 5.5 (Anthropic) at high effort
**Date:** 2026-10-25
**Subject:** #669: the 422 paths of `projects/ROCKNIX/packages/sysutils/**` and `hardware/**` (`quirks/devices/**` excepted), read at `8ebaf8daad`
**Evidence:** `02-forward-audit.md` (the runs, the reachability table, the units, busybox, the upstream delta, the guest cycle, the proofs L-01 to L-15)

---

## Running Notes

Phase 3 reads what the area was for, what drifted, what nobody noticed, and
the seams. Every claim cites `02` or a `file:line` at `8ebaf8daad`.

### 3.1 Architectural coherence

The area is the OS's boot spine: `scripts/init` (PID 1 in the initramfs,
1,383 fork-own lines) selects a boot target from markers and the kernel
command line. systemd brings up 29 units from this slice. `rocknix-autostart`
then runs four layers of scripts in a fixed order: platform quirks, device
quirks, `common/*`, and the player's own hooks (`02` § The guest cycle, s5).
The design is coherent, and every layer runs as root: no unit names a user
(`02` § The units).

**Two selection mechanisms, and neither is written down where a reader
lands.** `system-utils` selects at install time (`package.mk:27-34`). The
quirks select at run time: every platform is copied into every image that
has a platform of its own (`quirks/package.mk:16-18`), and `HW_DEVICE` picks
one at boot (`autostart:16-28`). So 213 files, 108,294 bytes, ship on every
image and run on none (`02` § The reachability table). Neither `package.mk`
says so. A reader of the quirks recipe sees `cp -r platforms/*` after a test
on one platform's directory and could read it either way.

### 3.2 Project conformance

| Rule | Where it bites here | Verdict |
| --- | --- | --- |
| `engineering-practices.md` § Guards must fail closed | `autostart`'s `common` and custom loops have no `-f` and an unquoted `${script}` (L-01); its other three loops and `/etc/profile`'s have the `-f` (L-02) | PARTIAL: two loops of six unguarded |
| blindspot 16 (a unit naming a binary the image lacks) | `udevil-mount@.service`'s `samba-autoshare` (L-06); `video.service` cleared (L-09) | one instance, hidden by `-` |
| blindspot 34 (busybox is not the host's tools) | `/bin/sh` is bash; busybox supplies the applets | no new instance read |
| `upgrade-and-install.md` (what the units leave on devices) | `/storage/.ssh` as a file (#740 and `post-update:54-57`), `/storage/.cache/shadow` rewritten each boot (L-11) | read; reach named |
| `vm-first.md` | the units, tty1, the autostart order and `userconfig-setup` proven on one guest; H700 and SM8550 quirks read | PASS |

### 3.3 Spec fidelity

The brief's figures all reproduce (`01` § Scope). It has two errata, both
recorded: its unit loop's credential mask hides the `User=` count it is meant
to show (L-14), and `autostart:76` runs `${script}` rather than `exec`ing it.
The brief's leads land as follows:

- **`cron.service`**: no shipped image has it (L-08).
- **`video.service`** cannot meet a missing binary (L-09).
- **`shell.service`**: a `textmode`-only root shell, with no register row (L-03).
- **A writable path the brief did not name:** `/etc/profile:19-23` (L-02).

### 3.4 Platform architecture conformance

The units are the platform's: LibreELEC's shape (`/storage/.config/autostart`,
`/storage/.config/profile.d`, `/storage/.cache/services` markers), carried
by JELOS and ROCKNIX. The fork's own additions in this area are:
- `scripts/init`;
- `input_sense`;
- the GENERIC_X64 quirks (a developer's tool, D-QA-053);
- `var-log.mount` with `storage-log.service` (#104, the persistent journal);
- `hang-policy.conf`, `20-watchdog.conf` and the pstore drop-in;
- `network-base-setup`;
- `userconfig-setup`'s `es_savestates.cfg` link (#196).

Each sits inside the platform's shape, and none adds a root-reachable
writable path the platform did not already have.

### 3.5 Cross-system interaction audit

### Interaction: the player's hooks x every root service

`/storage/.config/autostart/*` runs once a boot, as root, after every other
layer (s5). `/storage/.config/profile.d/*` is sourced by `/etc/profile`. The
services that source it are `rocknix-autostart`, `powerstate` (as its
`EnvironmentFile` and again in `powerstate.sh:11`), `network-base-setup`,
`098-deviceutils` and the five sensing scripts, and the interactive shell.
A broken file there breaks all of them at once. Both directories are the
player's by design, so the seam is fragility, not exposure.

### Interaction: udev x udevil x samba

A USB-storage or optical medium triggers `udevil-mount@<dev>.service`
(`95-udevil-mount.rules`). It mounts under `udevil.conf`, with every type
`nosuid,noexec,nodev` except btrfs (L-05), and then calls a `samba-autoshare`
no shipped image has (L-06).

### Interaction: `userconfig-setup` and `post-update` x `/storage/.ssh`

Both copy a build's developer keys to the path `/storage/.ssh`. Where no
directory exists, the copy makes a file. This is reachable only on a build
with `LOCAL_SSH_KEYS_FILE` (L-07, #740).

### Interaction: this slice x the next base merge

Upstream changed 44 of the 422 in three and a half weeks. Only the busybox
pin's http URL is settled by the merge. The two collisions (C-1 crash
logging, C-2 the sysctls) need a decision before it (`02` § The upstream
delta).

### 3.6 What's missing?

- **A record of the boot layers' order and identity.** It is proven on the
  guest here and written nowhere a maintainer reads.
- **A test that a unit's `ExecStart*` names an installed binary.** The
  `samba-autoshare` line has been silent since the unit came in.
- **A note in `quirks/package.mk` that every platform ships everywhere.**

### 3.6.5 Audit-prescription verification: the shapes, every site

| Shape | Sites hunted | Found |
| --- | --- | --- |
| a loop running or sourcing each entry of a directory | `autostart:20-25,35-40,50-53,60-65,73-76`, `/etc/profile:6-10,19-23`, `sleep.sh:84-87` | the platform, device and `HW_DEVICE` loops test `-f` and quote; `sleep.sh` tests `-x` and quotes; **the `common` loop (`:50-53`, image files) and the custom loop (`:73-76`, the player's files) neither test nor quote**; `/etc/profile` tests `-f` and sources unquoted |
| a unit naming a path the image lacks | the 29 units' `Exec*` (`24`) against the guest | `samba-autoshare` |
| a marker under `/storage` changing root behaviour at boot | `scripts/init`, the units' `Condition*` | `.please_resize_me`, `.cache/volatile-log`, `.cache/debug.rocknix` (L-10) |
| a setuid binary or an applet enabled with no caller | busybox's configuration; `find -perm -4000` on the guest | busybox alone; four applets with no caller |

### 3.7 Retrospective Summary

The slice found no unauthenticated remote path. Every root-run, writable
input is one the platform hands the player deliberately: the hook
directories, the markers, an inserted medium. The defects are brittleness
and dead lines:
- the custom autostart loop's missing guard and quoting (L-01);
- `samba-autoshare` (L-06);
- the btrfs default that contradicts its own file's warning (L-05);
- four setuid-capable applets nothing calls (L-04).

All four are in upstream-carried files and stand at `651150fc88`, so the
class decision for each is the maintainer's on #346. The fork's own 24 files
read clean on this lens.
