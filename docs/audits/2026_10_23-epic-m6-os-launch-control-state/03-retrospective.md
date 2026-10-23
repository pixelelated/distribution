# Retrospective — M6.P2 T1, the OS scripts: launch, control and state

**Auditor:** Code Auditor skill (v1.13.0), primary Claude Opus 5.5 (Anthropic) at high effort
**Date:** 2026-10-23
**Subject:** #648; the 83 paths at `reviewed-at` `efadfea08a` (= `8ebaf8daad`)
**Spec:** `docs/reviews/briefs/os-launch-control-state.md` v2

---

## Running Notes

### 3.1 Architectural coherence

The package is three layers that grew at different times. **The fork's state layer** (`001-functions`' writers and lock, `chksysconfig`, `rocknix-evidence`, `rocknix-corekeep`, the fork's half of `wifictl`) is coherent, documented to the decision, and covered by tests that run under the image's busybox; nothing in it failed a refutation. **The launch path** (`runemu.sh`, `setsettings.sh`) is JELOS-era code with the fork's targeted repairs (#92, #176, #196, #209, #280, #308) laid over it: the repairs are sound, the code between them is where the defects are (F-09, F-10, F-11, F-14, F-16, F-17, F-21's consumer side). **The control scripts carried from upstream** (`rocknix-config`, `rocknix-settings`, `rocknix-scraper`, `bezels.sh`, `rocknix-retroachievements-info`, `setemu.sh`, `migrate_roms`, `show_changelog`, `amionline`, `find.sh`, `error.sh`, `getoverlays`) are partly Batocera's and partly dead: ten scripts are unreached or reached only through a page nothing opens (Q6), and `rocknix-config`'s live verbs call two programs the image lacks (F-64). Orphaned or dead code: `automount`'s `start_overlay` (F-41), `runemu.sh`'s three dead variables (F-05), `usbgadget`'s deprecated verbs (F-49), the misspelled `system.cfg` keys (F-45 and the one upstream fixed).

### 3.2 Project conformance

**Instruction files whose `paths:` match** (read from this worktree, equal to `next`'s for every scoped file; § Scope lists them):

| Rule § | Relevance | Finding |
| --- | --- | --- |
| `packaging-and-patches.md` § A shipped script's tools are dependencies too | ✗ | F-62: 2 of 36 called programs declared |
| `packaging-and-patches.md` § late binding, headers | ✓ | `pkgcheck` 0; headers kept with a ROCKNIX/fork line on the fork's files |
| `upgrade-and-install.md` § Fixing forward / Every fix answers what was already written | ⚠ | F-44 (an update resets a player's DPMS choice), F-33 (`last_` copies lost on the second update), F-63 (the seed's mode stays on every device) |
| `engineering-practices.md` § Guards must fail closed | ✗ | F-29 (`setrootpass`), F-40 (`installtointernal`'s copy), F-67 (`updateabl`), F-36 (`overlays` reports a removal of a path that never existed), F-48 (`wifictl` exits 0 with no adapter) |
| `engineering-practices.md` § Verify design intent | ✓ applied | F-09's fix shape kept `:989`'s observed behaviour; F-01 narrowed after reading `SystemConf`; F-67's skip check cleared by the ELF |
| `engineering-practices.md` § A name is not a behaviour | ✓ applied | F-47's header claim tested and found not to hold; `rocknix-memory-manager` is no loop |
| `generic-x64-vm-testing.md` § What the guest's busybox lacks; § private settings modes | ✓ | every script check ran under the image's busybox or on the guest |
| `rclone-cloud-sync.md` § Critical gotchas (reachability means the remote) | ⚠ | `amionline` pings `www.google.com` (unreached, F-55) |
| `handheld-evidence.md` § what survives what | ⚠ | F-28: `upgrade.log` is overwritten at every ordinary boot, though `/var/log` persists |
| `es-player-text.md` § outcome vocabulary | · | the slice's player-facing words are `factoryreset`'s failure sentences (#119; in register) and `runemu.sh`'s M7 messages; the rest is log text |
| `time-to-play.md` | ✓ measured | Q5: 0.64 s and 1.01 s; F-03, F-09 and upstream's `25903bb59c` named for their effect |
| `least-surprise.md` | ✗ | F-01 (a slower governor chosen, the fastest one got), F-44, F-10 (neogeo's rewind silently off), F-19 (an overlay choice ignored) |
| `vm-first.md`, `bugs-are-agent-first.md` | ✓ | every behaviour claim is a guest proof or is written as a lead with its device fact |

**Blindspot register** (the entries brief § 3 names, and those this work touched):

| Entry | Does this work repeat it? |
| --- | --- |
| 7 / 34 (host tools are not the device's) | **Repeated by the brief, caught**: the `/bin/sh` dash claim was the host's own `/usr/bin/sh` through an absolute link (stage A); and `usb-gadget-test`'s default `--shell /bin/sh` is the host's dash, so the guest run was added |
| 13 (assumed done) / 51 (an open checkbox is a claim) | not repeated: the prior punch lists were provenance only; no checkbox ticked |
| 22 (a probe that cannot report absence) | **repeated in the product**: F-40 (`find -exec` returns 0 over a failed `cp`), F-36 (`remove_checked` of a mis-parsed path reports gone) |
| 30 (a resumed session built on its summary) | guarded: the running log carries commands and outputs |
| 32 (wall-clock ordering) | **repeated in my own log** twice (times written by estimate), corrected with the clock reads named |
| 33 (sentinel exit codes) | not touched in this package's fragments |
| 43 (a header's safety claim untested) | **found again**: `rocknix-evidence`'s "a process list can carry one" (F-47) and `setsettings.sh`'s comment that the `-e` slot is guarded because the line is `eval`'d, which the netplay host is not (F-14) |
| 46 (a name read as a behaviour) | **in the brief**: `rocknix-memory-manager`'s "loop" |
| 57 (a fix covering fewer sites than named) | **F-14 is its shape**: #275 quoted the values on the command line; the setting's path into `eval` was a second door |
| 62 (a fix left what was already written) | F-44, F-63 carry an `Already written:` line for that reason |
| 64 (lengthening a wait) | not repeated |
| 72 (a comment held an invariant the code stopped keeping) | F-47's header; F-14's `-e` comment |
| 73 (a monitor of completion) | n/a (no long build) |
| new | `wait_lock`'s trap replaced my proof script's own (F-22): a fixture that cleans up from an EXIT trap while sourcing a library that installs one; the friction line names it; a candidate blindspot for the retro |

**Project invariants:** *preserve player progress*: F-16 and F-17 destroy core options (not progress) at every launch, F-11 can leave stale keys; no save is touched. *Backups never contain secrets*: F-68 (pairing keys copied onto `/storage/roms` at every Bluetooth stop), a lead for T16/T17. *The filter is an allowlist*: not touched. *Upgrade and clean install*: F-28, F-33, F-44, F-58 (the x86_64 clean install loses its boot-time CPU/GPU defaults).

### 3.3 Spec fidelity

The brief's claims checked against the artifacts: three were wrong and are recorded as deltas, not stops: `/bin/sh` is bash (stage A); `rocknix-memory-manager` is a oneshot, not a loop; `tools/vocabulary-check` reads none of this slice's scripts. One brief path assumption was unreachable as written: `tools/vm-upgrade-rehearsal` uses the shared QA backend and `vm-pair` (asked on #648). The counts, the hash, the image, the M7 delta and every other host path were right.

### 3.4 Platform architecture conformance

| Check | Relevance | Finding |
| --- | --- | --- |
| Reference Implementation / Schema-Before-Code / Dogfooding / API-First | · | not this repository's model; not applicable |

### 3.5 Cross-system interaction audit

### Interaction: the launch path x the interface (T2, T21)
**State shared:** the launch command (`es_systems.cfg`'s `runemu.sh %ROM% -P%SYSTEM% --core=... --controllers=...`), `system.cfg` per-game keys (`<system>["<file>"].<key>`, `FileData.cpp:176-183`), the interface's option lists.
**Wipe risk:** a per-game key the interface writes that `get_setting` cannot find (F-21); a value the interface lets a player type that `runemu.sh` evaluates (F-14); an option the interface offers that the script cannot apply (F-01).
**Test coverage:** PARTIAL -- `emulator-exit-test` and `time-to-play` cross the seam for one ROM name without brackets and the default settings; nothing crosses it with a per-game setting, a bracketed name, netplay or a governor.
**Finding:** broken at three points, each proven on the guest.

### Interaction: the settings writers x the lock
**State shared:** `system.cfg`, `/tmp/.system.cfg.lock` (pid-only, shared with the interface's `PidLock`, D-INFRA-012).
**Wipe risk:** a writer outside the lock (F-32's two lines, F-65 latent); a cut file completed into a whole-looking one (F-32, proven).
**Test coverage:** TESTED for the guarded writers (`wait-lock-test`, `settings-modes-test`, `last-good-scripts-test`); UNTESTED for `post-update`'s lines and `rocknix-settings`.
**Finding:** risky at the unguarded writers; upstream's `25903bb59c` would change the lock to `flock`, which the interface's `PidLock` does not read (Q4: split).

### Interaction: `post-update` x `/storage`
**State shared:** `/storage/.config` (system, interface links, modules, sysctl.d, the cloud config), `/var/log/upgrade.log`.
**Wipe risk:** F-44 (a setting deleted every update), F-33 (a backup copy overwritten by a link), F-28 (its own log overwritten at the next boot), F-34 (dev-image files over the owner's).
**Test coverage:** PARTIAL -- `melonds-upgrade-test` (one block); the upgrade rehearsal not run this session (asked).
**Finding:** risky.

### Interaction: `automount` x the cloud scripts' saves root
**State shared:** what `/storage/roms` is (bind, overlay, or the internal card's own directory).
**Wipe risk:** a failed mount leaves the internal directory in place with nothing said (F-42); `cloud_saves_root` (D-CLOUD-054/055) refuses a changed card on the cloud side.
**Test coverage:** PARTIAL -- `last-good-scripts-test` covers `automount`'s fork half; a failed mount is not provoked.
**Finding:** safe for the cloud by the other side's guard; locally unreported.

### Interaction: `rocknix-bluetooth` x the content tier and Samba
**State shared:** `/storage/roms/backups/bluetooth.tar` (link keys).
**Wipe risk:** a credential leaving the device in a content backup or over the share (F-68).
**Test coverage:** UNTESTED.
**Finding:** risky; a lead for T16/T17.

### 3.6 What's missing?

Searched with `grep -rlF '<script>' tools/` (less `node_modules` and Markdown), 08:21 UTC:

- **No test exercises `setsettings.sh`'s per-core files, its parallel staging or its `match()`/`add_setting`** (`last-good-scripts-test` and `ra-offline-test` name the file for the redaction and the offline proxy's host): the gap that let F-09, F-10, F-11, F-16 and F-17 ship since the import. The group 1 proofs (`.qa-scratch/t1/proofs/group1.sh`) are the shape such cases would take.
- **No test reaches `rocknix-fake-suspend`, `paneladj`, `updateabl` or `installtointernal`** (0 tool files each); `paneladj`'s defect (F-57) and `installtointernal`'s copy status (F-40) are provable on the guest with a fixture, as this audit did.
- **No test passes a per-game setting, a bracketed ROM name or a governor through `runemu.sh`.**
- **`tools/vocabulary-check` reads none of this slice's scripts** (its `--scripts` default is the rclone sources plus `backuptool`); the slice's player-facing strings are few, but the tool's scope is narrower than the brief assumed.
- Proximate work checked for a test under another name: `tools/emulator-exit-test` (the exit path only), `tools/time-to-play` (one ROM, default settings), `tools/settings-modes-test` (the writers' modes).

### 3.6.5 Audit-prescription verification: the shapes, every site

**(A) A write to `system.cfg` outside the guarded writers** (grep for `sed -i|>>?|cp |mv |tee` naming `system.cfg`, `J_CONF`, `CFG`, `SYSTEM_CONFIG`, then the variables that hold it):

| Site | Kind | Verdict |
| --- | --- | --- |
| `post-update:159-160` (`$ a\`) | Site | FIX-NOW (F-32) |
| `post-update:202` (dpms delete) | Sibling | FIX-NOW (F-32, F-44) |
| `rocknix-settings:61-74` (through `ROCKNIX_CONFIGFILE`) | Adjacent | FILE-FOLLOWUP or fix with F-32 (F-65, unreached) |
| `001-functions:542`, `:595` (`cp -f` seed of a missing file) | Sibling | SAFE-AS-TESTED (only when the file is absent) |

**(B) A value spliced unquoted into `eval` or a `sed` program:**

| Site | Kind | Verdict |
| --- | --- | --- |
| `setsettings.sh:683`, `:688` -> `runemu.sh:355`, `:500` (netplay host) | Site | FIX-NOW (F-14) |
| `setsettings.sh:787` (`--set-shader`) | Sibling | FIX-NOW with F-14 |
| `setsettings.sh:1048-1087`, `:1123` (core option values into `sed`) | Sibling | FIX with F-19 |
| `runemu.sh:378`, `:385` (ROM name into PortMaster's `sed`) | Adjacent | FILE-FOLLOWUP (upstream path, D-UI-079 governs behaviour; the quoting is a contained fix) |
| `rocknix-memory-manager:99` (`eval` of a typed value) | Adjacent | FIX with F-52 |
| `rocknix-config:39` (`sed` of key/value) | Adjacent | with F-64's disposition |

**(C) Success reported over a no-op or a failure:**

| Site | Kind | Verdict |
| --- | --- | --- |
| `setrootpass:32-45` | Site | FIX-NOW (F-29) |
| `installtointernal:208-215` | Sibling | FIX-NOW (F-40) |
| `updateabl:69-72` | Sibling | FIX (F-67; device-only proof) |
| `factoryreset:172` + `remove_checked` | Sibling | FIX (F-36) |
| `wifictl:55-57` | Sibling | FIX (F-48) |
| `factoryreset:220-238` (rk817) | Adjacent | FILE-FOLLOWUP (F-37, unshipped hardware) |

**(D) A `#!/bin/sh` script that needs bash** (shellcheck's SC30xx over the slice, and the grep above): `usbgadget`, `rocknix-fake-suspend`, `rocknix-bluetooth`, `volume`, `getfilters`, `updateabl`, `vertical-check`, `autostart/080-network`, `bezels.sh`, `migrate_roms`, and the three autostart fragments that source `001-functions` (`001-setup`, `003-upgrade`, `007-rootpw`) plus `008-perfmode` -- 14 sites. Verdict: BY-DESIGN today (the image's `sh` is bash), but the brief itself believed otherwise, and `008-perfmode`'s fatal `.` (F-58) is a POSIX-mode consequence. One codified rule for the retro: the interpreter line says what the code needs.

**(E) A setting's value executed as a command:** `runemu.sh:131`, `:467` (F-01); no third site (grep for a line that is a lone expansion: the rest are the `${VERBOSE} &&` idiom or a continued argument).

### 3.7 Retrospective Summary

**Architectural assessment:** the fork's own state layer is sound; the launch path's inherited middle and the upstream control scripts carry the defects and the dead ends.
**Conformance:** MEDIUM -- strong where the fork has worked (lock, writers, evidence), weak on fail-closed guards in inherited scripts and on declared dependencies.
**Cross-system interactions:** identified at five seams; the launch path x interface seam is broken at three proven points and has no test that crosses it with real settings.
**Spec drift:** three brief claims wrong (recorded), one brief instruction unrunnable as written (asked).
**Missing artifacts:** tests for `setsettings.sh`'s settings, for the four untested scripts, and for the launch seam with per-game settings.
