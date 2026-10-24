# Research Notes — M6.P2 T3, RetroArch and the libretro cores

**Auditor:** Code Auditor skill (v1.13.0), primary Claude Opus 5.5 at high effort
**Date:** 2026-10-24
**Subject:** #650 (`M6.P2 E798/T3`), slice `emulators-libretro`, area epic #798
**Spec:** `docs/reviews/briefs/emulators-libretro.md` version 2 (`f650d65522`); #650's checklist

---

## Running Notes

## Scope

### The read hash

- **`reviewed-at: d606301784`** (`d606301784208a4c3c3eb22f13a0c0784c5bf604`), the branch `HEAD` at stage A. Since the dispatch's `af35d54f87` the branch has gained only the lane-start work-log commit (`e1af3b2ba5`) and the #799 tool fix (`d606301784`); neither touches the slice.
- `git diff --quiet 8ebaf8daad d606301784 -- projects/ROCKNIX/packages/emulators/libretro projects/ROCKNIX/packages/virtual/emulators` exits 0. **The slice's bytes are `next`'s at `8ebaf8daad`.**
- The branch is stacked on the P1 tip `2174265e9c` (`merge-base --is-ancestor`, exit 0).
- `upstream/next` is **`3421d7d178`** (fetched 2026-10-24 02:38 UTC). The merge base with `next` is `c445081a59518f37d9776e5412dd7b14910696f7`, the brief's figure.

### The membership, re-derived (brief § 2's filter)

The filter of brief § 2 was run with `python3 -I` against `docs/reviews/inventory.json`. The inventory was last changed by `00ca350666`, 2026-10-23T02:28:57Z, on the P1 branch. Output:

```
paths 344 lines 31961 {'upstream-carried': 299, 'fork-own': 24, 'vendor-carried': 21} {'emulators-and-cores': 294, 'patches-and-configs': 21, 'generic-packages': 29}
fork-own lines 6557 of which retroarch/sources/GENERIC_X64 1038
vendor-carried (RetroArch's patches) lines 1670 fork-written 8 1244
reach {'shipped': 342, 'n/a': 2}
```

**No delta against the recorded counts.** 344 paths and 31,961 lines; 24 fork-own paths with 6,557 lines; 299 upstream-carried; 21 vendor-carried with 1,670 lines, 8 of them fork-written with 1,244 lines. By area: 294 `emulators-and-cores`, 21 `patches-and-configs`, 29 `generic-packages`. By reach: 342 `shipped` and 2 `n/a` (the two rotation-table generators).

**The order row's three figures** (`344 paths 31,961 lines 10,185 read 5,519 fork-own 1,670 patch`):

- **5,519** is the filter's 6,557 fork-own lines less the four GENERIC_X64 configuration files' 1,038: `retroarch.cfg` 855, `retroarch-core-options.cfg` 154, `TATE-MAME 2003-Plus.rmp` 27, `retroarch64bit-append.cfg` 2. Their `language` is `config` or `other`, outside the tool's code classes. Their area is `emulators-and-cores`; the 21 `patches-and-configs` rows are RetroArch's patches alone (the futro's erratum).
- **10,185 read** is the tool's code classes summed whatever their tier (`tools/renovation-inventory` line 999).
- **1,670** is RetroArch's 21 patches.

This lane's read set goes by provenance, not by class. The 24 fork-own paths and the 8 fork-written patches are read whole, the GENERIC_X64 configuration included. The 13 upstream patches and the 299 upstream-carried paths get Q4 and Q6 first.

**The 24 fork-own paths** (lines, path under `projects/ROCKNIX/packages/`):

| Lines | Path |
| ---: | --- |
| 2,755 | `virtual/emulators/sources/Install Steam.sh` |
| 1,777 | `virtual/emulators/package.mk` |
| 855 | `emulators/libretro/retroarch/sources/GENERIC_X64/retroarch.cfg` |
| 154 | `emulators/libretro/retroarch/sources/GENERIC_X64/retroarch-core-options.cfg` |
| 153 | `emulators/libretro/retroarch/package.mk` |
| 125 | `emulators/libretro/rotation-table-mame.py` (`n/a` reach) |
| 120 | `emulators/libretro/rotation-table-fba.py` (`n/a` reach) |
| 81 | `emulators/libretro/ppsspp-lr/package.mk` |
| 49 | `emulators/libretro/idtech-lr/package.mk` |
| 46 | `emulators/libretro/mame2010-lr/package.mk` |
| 45 | `emulators/libretro/fbneo-lr/package.mk` |
| 44 | `emulators/libretro/mupen64plus-lr/package.mk` |
| 38 | `emulators/libretro/desmume-lr/package.mk` |
| 38 | `emulators/libretro/fbalpha2019-lr/package.mk` |
| 37 | `emulators/libretro/easyrpg-lr/libxmp-lite/package.mk` |
| 37 | `emulators/libretro/fbalpha2012-lr/package.mk` |
| 34 | `emulators/libretro/mame2003-plus-lr/package.mk` |
| 33 | `emulators/libretro/easyrpg-lr/wildmidi/package.mk` |
| 30 | `emulators/libretro/freej2me-lr/package.mk` |
| 29 | `emulators/libretro/easyrpg-lr/libspeexdsp/package.mk` |
| 28 | `emulators/libretro/gpsp-lr/package.mk` |
| 27 | `emulators/libretro/retroarch/sources/GENERIC_X64/TATE-MAME 2003-Plus.rmp` |
| 20 | `emulators/libretro/libretro-database/package.mk` |
| 2 | `emulators/libretro/retroarch/sources/GENERIC_X64/retroarch64bit-append.cfg` |

**The 21 RetroArch patches** (vendor-carried): 8 fork-written (`0011-video-thread-wrapper-serialise-posters` 85, `0013-cheevos-offline-proxy-toast` 188, `0014-widgets-backdrop-follows-the-font` 248, `0015-video-thread-wrapper-run-a-command-once` 89, `0016-widgets-message-queue-floor` 100, `0017-widgets-sharp-font-sizes` 230, `0018-auto-slot-survives-content-load` 181, `0019-widgets-message-queue-keeps-its-place` 123; 1,244 lines) and 13 upstream's (`0001-Increase-glui-size` 22, `0001-Increase-ozone-size` 22, `0001-Increase-ozone-widget_size` 14, `0002-quit-not-restart` 12, `0003-fix-oga-no-preferred` 54, `0004-drm-resolution` 27, `0006-no-screen-brightness` 29, `0008-disable_search` 13, `0009-hide-wayland-checkerboard` 27, `0010-paths` 51, `0011-cheevos-sounds` 83, `0012-cheevos-cmd` 42, `batteryplus/0001-batteryplus-capacity` 30; 426 lines). There is no `0005` or `0007`, and three patches share the `0001` prefix; Q7 notes this, and the cause is upstream's.

**Two commands for one set.** `git ls-files projects/ROCKNIX/packages/emulators/libretro projects/ROCKNIX/packages/virtual/emulators | wc -l` prints **406**. Classified against the membership by the same rules (`python3 -I`, the rows by path), they are **344 members and 62 outside**:

- **57 core patch files**, `patches-and-configs` rows under the cores' own `patches/` directories (50 `shipped`, 1 `test`, 6 `unreached`): T42 `patches-shipped`'s.
- **5 recipes**, `emulators-and-cores` with a reach outside the rule: `boom3-lr` (`unshipped`), `mame2003-lr` (`unreached`), `panda3ds-lr` (`unreached`), `play-lr` (`unreached`), `vitaquake3-lr` (`unshipped`). These are T24 `emulators-dead-ends`'.

Every member lies inside the two directories. `git diff --numstat <empty tree> 8ebaf8daad -- .../retroarch/patches` sums to **1,670**, equal to the inventory's vendor-carried lines.

### The five groups (the brief's reading order)

1. **RetroArch's recipe, patches and configuration** (`emulators/libretro/retroarch/`): `package.mk` (153, fork-own), the 21 patches, `autostart/`, `modprobe.d/`, `retroarch-assets`, `retroarch-overlays`, `retroarch-joypads/`, `system.d/`, `tmpfiles.d/`, `udev.d/`, `sounds/`, `scripts/`, and `sources/<DEVICE>/` for fifteen devices. The GENERIC_X64 set is fork-own; the other fourteen are upstream-carried.
2. **The `emulators` metapackage and the launch table** (`virtual/emulators/`, 29 paths): `package.mk` (1,777, fork-own) with `makeinstall_target`'s `add_emu_core`/`add_es_system` table; the 24 `sources/*.sh` (`Install Steam.sh` fork-own); `autostart/001-controller`, `scripts/mkcontroller`, `tmpfiles.d/`, `udev.d/`. `distributions/ROCKNIX/config/functions` 99 to 140 is read beside it as T5's context.
3. **The fork's own core recipes**: the eleven `*-lr` recipes above, `libretro-database`, `easyrpg-lr`'s three fork-own sub-recipes, and the two rotation tables.
4. **The upstream-carried core recipes**: Q4 and Q6 first.
5. **The tests and tools for these sources** (outside the membership, read for § 5): `tools/retroarch-wrapper-test` (#799 fixed its default roots at stage A, `d606301784`), `tools/fork-package-freshness`, `tools/time-to-play`, `tools/emulator-exit-test`, `tools/ra-candidate-games`, `tools/pkgcheck`.

### The interacting subsystems (read-only context)

| Subsystem | Its owner | The seam |
| --- | --- | --- |
| `runemu.sh`, `setsettings.sh` | T1 (#648, accepted; read at `efadfea08a`) | `RUNCMD`'s `-P%SYSTEM%` after `%ROM%` against `${ARGUMENTS##*-P}` (T1's open #730); the per-device `retroarch.cfg` against `setsettings.sh`'s writes |
| EmulationStation's launch path | T2 (#649, accepted) | `SystemData::loadConfig` parses `es_systems.cfg`; the five tokens the table emits against the interface's expansions; the overlays read first (#613); D-WORKFLOW-192's netplay tokens the interface appends |
| The build engine | T5 (#652) | `distributions/ROCKNIX/config/functions` (`add_emu_core`, `add_es_system`, `mk_es_systems`, `mk_system_doc`), `config/emulators/*.conf` |
| The proxy's rcheevos path | #163, the offline-achievements area | patches 0011 to 0013 (toasts and commands), the widget patches |
| The save layout | the cloud sync (`cloud-sync-core`) | the cores' save and state paths are what the sync moves |

### The branch scan

**Predicate:** a branch is *ahead* of `next` on the two directories when `git log --oneline next..<branch> -- <the two directories>` prints a line. **Command:** the loop over `git for-each-ref refs/remotes/origin`, run 2026-10-24 ~02:42 UTC. **Result:** 54 `origin` branches; **18 ahead**; **44 differ** (`git diff --quiet next <branch> -- ...` non-zero). These are the brief's two counts.

| Branch | Commits ahead on the slice | Last commit |
| --- | ---: | --- |
| `origin/backup/generic-x64-pre-rebase-20260714` | 6 | 2026-07-12 |
| `origin/feature/conflict-resolution` | 6 | 2026-10-07 |
| `origin/feature/m7-player-setup` | 1 (`d9054efc46`) | 2026-10-15 |
| `origin/feature/m7-rocknix-20261001` | 1 (`c7e07b84dc`) | 2026-10-12 |
| `origin/pr/01-build` to `origin/pr/10-es-pin` (ten) | 1 to 5 | 2026-09-29 |
| `origin/rclone-bisync-beta` | 1 | 2025-08-06 |
| `origin/verification-anchors/2026-09-30-rasteratops-fork-plan` and `-r2` | 1 each | 2026-09-30 |
| `origin/x64-build-fix` | 6 | 2025-10-22 |

**One correction for the coordinator (a lead, posted on #650).** The brief says `feature/m7-player-setup` is ahead "by the M7 lane's `Install Steam.sh` hunk `6101242e14`, so that delta is on `origin` too". That is not so:

- `origin/feature/m7-player-setup` (tip `cdf6643cfc`, 2026-10-15) is ahead by **`d9054efc46`** (2026-10-15, *"emulators: clear inactive achievements and isolate Steam runtime"*, 1+/1- on `Install Steam.sh`).
- That branch's `Install Steam.sh` blob is `70f52d4446`, the same as `next`'s, so the branch is ahead in history and equal in content.
- **`6101242e14` is not on `origin`.** `git branch -r --contains 6101242e14` names only `legacy/m7-audit-integration-603`, and in the legacy checkout 15 local branches carry it (the `build/m7-composed-*` and `build/m7-signin-*` ones).

### The M7 delta (`next..069fc2704421` in the legacy checkout, read-only)

`git -C /workspace/repos/rocknix diff --stat next 069fc2704421 -- <the two directories>` prints one file, `virtual/emulators/sources/Install Steam.sh`, **+605/-6**, from one commit: `6101242e14` (2026-10-18T16:32:12Z, *"m7: integrate reviewed frontend and installer repairs"*). Its eight hunks:

| Hunk (`next` lines) | What it changes |
| --- | --- |
| `@@ -207,6 +207,12 @@` `fetch_proton_latest_release` | adds a `case` that accepts only `PROTON_CACHYOS` and `PROTON_GE` as the variable prefix |
| `@@ -236,11 +242,11 @@` | replaces four `eval` assignments of release metadata with literal assignment ("never parse it as shell code") |
| `@@ -1456,6 +1462,495 @@` (the embedded Python, after `consumers`) | adds a durable v2 checkpoint/recovery layer (`DurableUnsupported`, 489 lines) |
| `@@ -1550,6 +2045,8 @@` `load_journal` | calls the v2 recovery (`d_recover`) on the journal's rows |
| `@@ -2304,6 +2801,7 @@` `install` | writes a checkpoint (`d_checkpoint(tx)`) |
| `@@ -2324,6 +2822,104 @@` `install` | adds `registry_file`/`registry`: an existing `registry.vdf` belongs to Steam or the player and is never opened for writing |
| `@@ -2340,6 +2936,9 @@` `main` | adds a `registry` mode |
| `@@ -2366,7 +2965,7 @@` | replaces `cp -f /usr/share/steam/registry.vdf` with `steam_client_state registry` |

The slice reads `next`'s copy. A finding on a line these hunks change is recorded with that fact, and any punch item on `Install Steam.sh` is marked `deferred:M7-merge` (brief § 6).

### The image

- **The image:** `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz` from `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/target/`, 2,122,289,964 bytes. It was copied with its `.sha256` and `.identity.json` to `/workspace/artifacts/m6-t3-20261024/` (02:44 UTC), and `sha256sum -c` on the copy printed `OK` (`6b4c3079bdee2f47…`).
- **Its BUILD_ID, from `.identity.json`:** `build_commit` `069fc270442134fe771258418adf4e666e0473fb`, `build_version` `0.0.1-dev+20261022T235948Z.g069fc2704421`, `dirty` `no`, device `GENERIC_X64`, arch `x86_64`. The guest's `/etc/os-release` is read when the guest is up and recorded beside this.
- The dispatch names no newer GENERIC_X64 image, so this one stands.

### The #336 line, as drawn

#336's body, read 2026-10-24, Step 1: *"A headless runner from an existing frontend, for the 2D cores first ... a control channel (a Unix socket: pause, save, load, screenshot, quit) that ES's pages and the exit hotkey talk to instead of RetroArch's config and kill. RetroArch stays the runner for the GL cores and for netplay; the choice is per core in the launcher, and ES does not know which ran."* Step 3 (later) is the in-process bridge.

**The line is drawn where the brief § 4 draws it, and #336's text adds nothing that moves it.**

- **What Step 1 retires, for the 2D cores only:** RetroArch's menu and widget surface, which means the fork's widget patches 0014, 0016, 0017 and 0019 (the achievement banner's backdrop, floor, sizes and place) and upstream's menu-sizing and hiding patches 0001 to 0009. It also retires `retroarch.cfg` as the per-game store and the `--core=`/`--emulator=` contract `runemu.sh` reads.
- **What it keeps:** the GL cores and netplay stay on RetroArch, so every patch and configuration key stays reached on those paths after Step 1.
- **What it retires of the cores' recipes, their pins, their option files and the launch table:** nothing. The runner reads them as RetroArch does.
- **So:** Q1, Q5 and Q7 findings confined to the menu and widget surface, or to its configuration keys, are carried as `deferred:#336` at Phase 7 unless a stream brief says otherwise. Q2 and Q3 findings there are fixed regardless. Every Q4 and Q6 finding is this slice's in full.
- **One addition from #336's text:** the exit hotkey and the state commands would move to the runner's socket for the 2D cores. Patches 0011, 0012 and 0015 (the posted-command path, `CMD_*` handling) stay on RetroArch's side for the GL cores, so they are not `deferred:#336`.
