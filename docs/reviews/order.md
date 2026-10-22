# The renovation order

**Issue:** #641 (M6.P1, the survey), carrying #346's order-and-method
criteria; epic #339; milestone M6. **Status: proposed** -- posted on #641 at
the pass-7 gate and waiting for the maintainer's yes; no slice issue is filed
before it (brief § 8). **Register row:** D-WORKFLOW-184, written at the yes.

This is the order in which the whole codebase is renovated, slice by slice,
under the plan (`plan-for-the-plan.md`). It was produced by the seven-pass
survey recorded in `p1-tracking.md`, from four generated ledgers:
`inventory.md` (every path with its tier, size and reachability),
`assessment.md` (the six ordering lenses' evidence per area),
`cross-reference.md` (every area against every other) and the slice sizes in
the block below. The hand-written input is `slices.json`; `tools/renovation-inventory
--order` sizes every slice from the inventory, proves that every tracked path
is in exactly one slice, and renders the block between the markers.

## How the order was argued

Plan § 6a's six lenses, scored per area in `p1-tracking.md` § Pass 3, decide
the order, after two fixed constraints:

1. **D-WORKFLOW-102's gates come first.** Tier 1's launch, control and state
   slice gates `0.1`; the interface's launch-path slice is read before #336
   Step 1. They are T1 and T2, and both are also where the lenses point
   (security, brittleness and planned change all score high in
   os-scripts-and-launch and interface).
2. **Each of the first three is one session.** T1 reads 11,560 lines, T2
   9,598, and T3 is a table (#346's second criterion; plan § 5).

After those, in this order of reasoning:

- **Dead ends early and cheap (reachability).** T3 (the generic packages no
  image builds, 95,398 lines) and T4 (patches no plan applies, 317,908 lines)
  are Local-depth tables: no second-opinion cost, and every removal they
  propose shrinks a later slice or table (plan § 6a).
- **Then the parts that hold a player's data or credentials (security,
  brittleness, new functionality).** T5 and T6 (cloud sync: the highest
  brittleness of the product areas, 19 blindspot entries and 47 closed
  bugs, +28,279 lines since the base), T7 (the offline achievements proxy, a
  network listener holding an account token, all fork-own), and their
  EmulationStation pages, T8 and T9, which name those scripts in 36 and 16
  files (`cross-reference.md`). Each pair is read close together because
  the defects live at the seam (plan § 5).
- **Then what #336 replaces (planned change).** T10, RetroArch and the
  libretro cores, which `runemu.sh` configures and starts and #336's runner
  replaces; read before that work begins, beside T2's gate.
- **Then the central and the small (cost against value).** T11 (the OS's
  system services, root on every device), T12 (the build engine: 884
  callers for 6,776 read lines), T13 (GuiMenu, the largest fork-own unit,
  11,883 lines), T14 (the doctrine every session obeys, where #640's
  hardcoded paths live).
- **Then the devices and what they run.** T15 to T21: the per-handheld
  quirks, the standalone emulators, one slice per shipped device (H700,
  SM8550, RK3566 with RK3326, GENERIC_X64 with the kernel recipes), and the
  image's own packages.
- **Then the rest of the interface, framework last.** T22 to T28: the other
  pages, the application core, then es-core (components, window and input,
  utilities), read after the pages that use them, then the recipe.
- **Then the harness that proves everything else.** T29 to T34: the guards,
  the cloud harness, the VM harness, the state tests, build supervision.
  These run on the host only and score low on product value, and they are
  read after the code they prove, so a slice can fix a test it found wrong.
- **Last, the tables of upstream-carried and vendored material.** T35 to
  T43: the generic packages the image builds (currency), upstream's helper
  tools, the remaining dead ends, the provenance rows for the patches the
  shipped and unshipped images apply, ES's vendored libraries and data, the
  council toolchain (by version only, plan § 2), and the records.

**Slice kinds.** A *read* slice reads its code line by line. A *currency*
slice is mostly upstream-carried: it reads its fork-own files line by line and
asks the reachability and currency questions of the rest first (plan § 2, § 3
principle 1), so its size is its fork-own lines. A *table* slice produces one
row per unit, patch or path, with the command that answers it.

**Depth** (plan § 6c, D-WORKFLOW-137): *Extended* (two reviewers from two
other labs) for the security, state-preservation and launch-path slices (T1,
T2, T5, T6, T7, T10); *Independent* for an ordinary code slice; *Local* for
tables, the doctrine read and small configuration slices. The executor is an
Anthropic model, so its reviewers are GPT-6 Astra and, for Extended, Gemini 4
Argon (plan § 6c).

**One deliberate exception to the size guide.** T32 is one file,
`tools/last-good-scripts-test`, 14,238 lines. It is kept whole because a test
split across two sessions loses its fixtures' context; plan § 5 bounds a slice
at about 8,000 to 12,000 lines *or* one unit.

**What every slice owes** is plan § 6b's per-slice procedure, from scope to
close. Each slice's issue carries its paths (the `select` of `slices.json`),
its tier, line count, lens, interacting subsystems, depth, gate, and empty
`reviewed-at` and `fixed-at` fields.

<!-- renovation-inventory --order: begin -->

Generated by `tools/renovation-inventory --order` from `slices.json` and `inventory.json` (distribution `17dee5ba42`, ES `16dbac5211`); edit `slices.json`, never this block. Every tracked path is in exactly one slice: `unassigned: 0`, `ambiguous: 0` over 134,591 rows. *Read* is code lines a slice reads line by line (code languages, not vendor-carried, not unreached); a *currency* slice reads its fork-own files line by line and checks the rest for reachability and currency (plan § 2), so its size is its fork-own lines; a table slice reads rows, not lines.

| k | Slice | Area | Kind | Lens | Paths | Lines | Read (fork-own) | Gate | Depth |
| ---: | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | the OS scripts: launch, control and state (Tier 1) | os-scripts-and-launch | read | gate (D-WORKFLOW-102), planned change (#336), security | 83 | 13,327 | 11,560 (7,441) | 0.1 (D-WORKFLOW-102) | Extended |
| 2 | EmulationStation's launch path | interface | read | gate (D-WORKFLOW-102), planned change (#336 Step 1) | 18 | 9,598 | 9,598 (9,115) | before #336 Step 1 (D-WORKFLOW-102) | Extended |
| 3 | the generic packages no image builds | generic-packages | table | reachability | 1,587 | 95,398 | 464 (0) | none | Local |
| 4 | patches and kernel configurations no plan applies | patches-and-configs | table | reachability | 778 | 317,908 | 0 (0) | none | Local |
| 5 | cloud sync: the sync, backup, restore and capture core | cloud-sync-and-saves | read | security, brittleness, new functionality | 14 | 8,316 | 7,827 (7,827) | none | Extended |
| 6 | cloud sync: setup, sign-in, connections, content and settings backups | cloud-sync-and-saves | read | security | 14 | 11,180 | 11,180 (11,180) | none | Extended |
| 7 | the offline achievements proxy | offline-achievements | read | security, new functionality | 27 | 5,369 | 3,656 (3,656) | none | Extended |
| 8 | EmulationStation's cloud pages, cards and text, with their unit tests | interface | read | brittleness, new functionality | 30 | 11,193 | 11,116 (11,116) | none | Independent |
| 9 | EmulationStation's RetroAchievements and offline pages | interface | read | security, new functionality | 16 | 4,929 | 4,929 (4,918) | none | Independent |
| 10 | RetroArch and the libretro cores | emulators-and-cores | currency | planned change (#336) | 315 | 26,570 | 4,803 (987) | none | Extended |
| 11 | the OS's system services and platform quirks | os-scripts-and-launch | read | security, brittleness | 422 | 16,604 | 10,898 (3,002) | none | Independent |
| 12 | the build engine | build-engine | read | cost against value | 242 | 13,910 | 6,776 (2,419) | none | Independent |
| 13 | EmulationStation's main menu (GuiMenu) | interface | read | new functionality, brittleness | 2 | 11,883 | 11,883 (11,883) | none | Independent |
| 14 | the doctrine: rules, skills, CLAUDE.md, AGENTS.md, the registers | doctrine | read | cost against value | 336 | 59,715 | 190 (190) | none | Local |
| 15 | the per-handheld quirks | os-scripts-and-launch | read | brittleness | 333 | 10,175 | 9,327 (389) | none | Local |
| 16 | the standalone emulators | emulators-and-cores | currency | planned change (#336) | 543 | 157,365 | 10,695 (3,104) | none | Independent |
| 17 | the H700 device (RG35XX SP, RG SP) | devices | currency | cost against value | 28 | 12,901 | 327 (0) | none | Independent |
| 18 | the SM8550 device (Retroid Pocket Nova) | devices | currency | cost against value | 29 | 28,053 | 118 (0) | none | Independent |
| 19 | the RK3566 and RK3326 devices | devices | currency | cost against value | 53 | 13,833 | 617 (0) | none | Independent |
| 20 | the GENERIC_X64 VM device, the kernel and drivers recipes, and the project's boot files | devices | read | cost against value | 64 | 11,500 | 2,902 (1,421) | none | Independent |
| 21 | the image's own packages (projects/ROCKNIX) | generic-packages | currency | package currency | 531 | 26,529 | 19,018 (6,711) | none | Independent |
| 22 | EmulationStation's other pages | interface | currency | new functionality | 78 | 16,237 | 16,237 (4,930) | none | Independent |
| 23 | EmulationStation's game list views, scrapers and services | interface | currency | cost against value | 46 | 20,196 | 20,196 (6,890) | none | Independent |
| 24 | EmulationStation's system layer: ApiSystem, game lists, collections, metadata | interface | currency | cost against value | 79 | 20,285 | 20,219 (8,531) | none | Independent |
| 25 | EmulationStation's core components | interface | currency | cost against value | 80 | 21,984 | 21,984 (9,541) | none | Independent |
| 26 | EmulationStation's window, input, settings and the rest of es-core | interface | currency | cost against value | 102 | 24,875 | 24,875 (9,059) | none | Independent |
| 27 | EmulationStation's utilities, resources and renderers | interface | currency | cost against value | 60 | 51,884 | 51,884 (7,256) | none | Independent |
| 28 | the EmulationStation recipe and themes in the distribution | interface | read | package currency | 15 | 4,561 | 327 (190) | none | Local |
| 29 | the guards: hooks, the fork CI and the checkers | tooling-and-guards | read | security, brittleness | 29 | 5,632 | 5,356 (4,970) | none | Independent |
| 30 | the cloud test harness | cloud-sync-and-saves | read | brittleness | 9 | 10,165 | 10,165 (10,165) | none | Independent |
| 31 | the VM harness | tooling-and-guards | read | cost against value | 60 | 8,790 | 7,140 (7,140) | none | Independent |
| 32 | the last-good scripts test | tooling-and-guards | read | brittleness | 1 | 14,238 | 14,238 (14,238) | none | Independent |
| 33 | the last-good, settings and state tests | tooling-and-guards | read | brittleness | 22 | 6,807 | 6,807 (6,807) | none | Independent |
| 34 | build supervision and host maintenance | tooling-and-guards | read | brittleness | 18 | 3,795 | 3,384 (3,384) | none | Independent |
| 35 | the generic packages the image builds | generic-packages | currency | package currency | 266 | 7,612 | 7,081 (483) | none | Local |
| 36 | upstream's helper tools and the other distributions | build-engine | table | reachability | 135 | 7,369 | 5,552 (169) | none | Local |
| 37 | emulator recipes and files no shipped image builds, and the rest of the area | emulators-and-cores | table | reachability | 86 | 2,399 | 51 (0) | none | Local |
| 38 | the devices the fork does not ship and the other projects | devices | table | reachability | 338 | 34,640 | 1,920 (0) | none | Local |
| 39 | patches and kernel configurations the shipped images apply | patches-and-configs | table | package currency | 575 | 153,425 | 0 (0) | none | Local |
| 40 | patches only unshipped devices apply | patches-and-configs | table | reachability | 348 | 286,952 | 0 (0) | none | Local |
| 41 | EmulationStation's vendored libraries, translations and build files | interface | table | reachability, package currency | 603 | 377,103 | 146,208 (14,487) | none | Local |
| 42 | the council toolchain and runner | tooling-and-guards | table | package currency | 52 | 25,848 | 24,508 (24,508) | none | Local |
| 43 | the records | records | table | cost against value | 126,124 | 22,982,979 | 15,392,661 (15,392,661) | none | Local |

### T1. os-scripts-and-launch: the OS scripts: launch, control and state (Tier 1)

- **id**: `os-launch-control-state`; **kind**: read; **lens**: gate (D-WORKFLOW-102), planned change (#336), security
- **why here**: D-WORKFLOW-102 makes Tier 1's launch, control and state slice the gate for 0.1; `runemu.sh` configures and starts RetroArch, which #336 replaces (`grep -ci retroarch runemu.sh` is 22); the package runs as root at boot and launch, and scores high on security and brittleness (assessment.md)
- **paths** (83 paths, 13,327 lines, 11,560 read, of which 7,441 fork-own; reach shipped 83): areas `os-scripts-and-launch`; globs `projects/ROCKNIX/packages/rocknix/**`
- **release gate**: 0.1 (D-WORKFLOW-102)
- **depth**: Extended -- launch path and state preservation (plan § 6c)
- **interacting subsystems** (read-only context): the interface's launch path (`es-launch-path`: `FileData::launchGame`, `LaunchCommand.h` read `runemu.sh`'s arguments); RetroArch and the standalone start scripts (emulators); `backuptool` and the cloud hooks (cloud slices); `system.cfg` through `get_setting`/`set_setting`
- **closing evidence**: audit folder `docs/audits/<date>-epic-m6-os-launch-control-state/` with the five phase files, `tools/lint-audit-artifacts` PASS with the renovation face, the punch-list issue resolved through Phase 7, `reviewed-at` and `fixed-at` set

### T2. interface: EmulationStation's launch path

- **id**: `es-launch-path`; **kind**: read; **lens**: gate (D-WORKFLOW-102), planned change (#336 Step 1)
- **why here**: D-WORKFLOW-102: the interface's launch-path slice is read before #336 Step 1 replaces it; `FileData::launchGame` asks over running syncs (D-UI-095), so the proxy cards and save-state bookkeeping ride the same path
- **paths** (18 paths, 9,598 lines, 9,598 read, of which 9,115 fork-own; reach shipped 18): areas `interface`; globs `es:es-app/src/{FileData,SystemData,LaunchCommand,ProxyCards}.*`, `es:es-app/src/main.cpp`, `es:es-app/src/SaveState*`
- **release gate**: before #336 Step 1 (D-WORKFLOW-102)
- **depth**: Extended -- launch path (plan § 6c)
- **interacting subsystems** (read-only context): `runemu.sh` and `setsettings.sh` (`os-launch-control-state`); the cloud sync cards (`ThreadedCloudSync`, the ES cloud slice); the proxy (offline achievements); `es_settings.cfg` and `system.cfg`
- **closing evidence**: audit folder `docs/audits/<date>-epic-m6-es-launch-path/`, lint PASS with the renovation face, punch list through Phase 7, `reviewed-at` and `fixed-at` set

### T3. generic-packages: the generic packages no image builds

- **id**: `packages-dead-ends`; **kind**: table; **lens**: reachability
- **why here**: the largest dead set: 94,879 lines no plan reaches (Kodi, the addons, the generic `busybox` and `systemd` the ROCKNIX overrides shadow); a table, cheap, and every removal shrinks later slices (plan § 6a)
- **paths** (1,587 paths, 95,398 lines, 464 read, of which 0 fork-own; reach unreached 1565, unshipped 22): areas `generic-packages`; globs `(all)`; reach `unreached`, `unshipped`
- **release gate**: none
- **depth**: Local -- a reachability table: the counts are the check (plan § 6c)
- **interacting subsystems** (read-only context): the ROCKNIX overrides that shadow generic recipes (`projects/ROCKNIX/packages/sysutils/{busybox,systemd}`); `scripts/create_addon` (addons)
- **closing evidence**: one row per unit with its reachability command and output, each removal with `Already written:` and `engineering-practices.md` § Before deleting a duplicate; audit folder, lint PASS, `reviewed-at` set

### T4. patches-and-configs: patches and kernel configurations no plan applies

- **id**: `patches-dead`; **kind**: table; **lens**: reachability
- **why here**: 778 paths, 317,908 lines: the 277 generic kernel patches the ROCKNIX `linux` override never applies, `vitaquake2-lr`'s `patches/x86_64`, the other projects' patches
- **paths** (778 paths, 317,908 lines, 0 read, of which 0 fork-own; reach unreached 778): areas `patches-and-configs`; globs `(all)`; reach `unreached`
- **release gate**: none
- **depth**: Local -- a provenance table
- **interacting subsystems** (read-only context): the packages they would patch
- **closing evidence**: one row per patch with origin, upstream status and reason, the count equal to the slice's paths; audit folder, lint PASS

### T5. cloud-sync-and-saves: cloud sync: the sync, backup, restore and capture core

- **id**: `cloud-sync-core`; **kind**: read; **lens**: security, brittleness, new functionality
- **why here**: the state model players' saves depend on: the highest brittleness of the product areas (19 blindspot entries, 47 closed bugs, 451 commits since June) and +28,279 lines since the base
- **paths** (14 paths, 8,316 lines, 7,827 read, of which 7,827 fork-own; reach shipped 14): areas `cloud-sync-and-saves`; globs `projects/ROCKNIX/packages/network/rclone/**`, `!projects/ROCKNIX/packages/network/rclone/sources/cloud_{oauth,setup,remote,connections.py,content_backup,content_restore,content_transfer,scan,folder_validate,device_id,log_scrub}`
- **release gate**: none
- **depth**: Extended -- the cloud sync and state preservation (plan § 6c)
- **interacting subsystems** (read-only context): the ES cloud cards and transfer page (the ES cloud slice); `backuptool` and the setup scripts (`cloud-setup-content`); the game-end hook and autostart (`os-launch-control-state`); `rclone-cloud-sync.md`'s invariants
- **closing evidence**: audit folder, lint PASS with the renovation face, every behaviour claim proven on the VM (`tools/cloud-round-trip`, `tools/vm-qa`), punch list through Phase 7, `reviewed-at` and `fixed-at` set

### T6. cloud-sync-and-saves: cloud sync: setup, sign-in, connections, content and settings backups

- **id**: `cloud-setup-content`; **kind**: read; **lens**: security
- **why here**: handles credentials (`rclone.conf`, OAuth tokens, the sign-in window) and the only content action that deletes (`--match`, D-CLOUD-023)
- **paths** (14 paths, 11,180 lines, 11,180 read, of which 11,180 fork-own; reach shipped 14): areas `cloud-sync-and-saves`; globs `projects/ROCKNIX/packages/network/rclone/sources/cloud_{oauth,setup,remote,connections.py,content_backup,content_restore,content_transfer,scan,folder_validate,device_id,log_scrub}`, `projects/ROCKNIX/packages/network/cloud-signin-window/**`, `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool`
- **release gate**: none
- **depth**: Extended -- security and state preservation (plan § 6c)
- **interacting subsystems** (read-only context): the sync core (`cloud-sync-core`); the ES setup wizard and transfer page; webkitgtk (#576)
- **closing evidence**: audit folder, lint PASS, VM proofs, punch list through Phase 7, `reviewed-at` and `fixed-at` set

### T7. offline-achievements: the offline achievements proxy

- **id**: `offline-achievements`; **kind**: read; **lens**: security, new functionality
- **why here**: a network listener holding the player's account token, all fork-own (+3,666), and the cheapest product area to finish; its 18 fork-written patches to the upstream proxy are read here, not in the patch tables (pass 6)
- **paths** (27 paths, 5,369 lines, 3,656 read, of which 3,656 fork-own; reach shipped 27): areas `offline-achievements`; globs `(all)` **plus** areas `patches-and-configs`; globs `projects/ROCKNIX/packages/network/raofflineproxy*/**`
- **release gate**: none
- **depth**: Extended -- a network listener and an account credential (plan § 6c)
- **interacting subsystems** (read-only context): `ProxyCards` and the RetroAchievements pages (ES); RetroArch's `rcheevos` path; #585's upstream queue
- **closing evidence**: audit folder, lint PASS, `tools/ra-offline-test` and the proxy's suites on the VM, punch list through Phase 7, `reviewed-at` and `fixed-at` set

### T8. interface: EmulationStation's cloud pages, cards and text, with their unit tests

- **id**: `es-cloud-pages`; **kind**: read; **lens**: brittleness, new functionality
- **why here**: 36 interface files name the cloud scripts (cross-reference.md); the cards, the transfer page and the text rules are the fork's
- **paths** (30 paths, 11,193 lines, 11,116 read, of which 11,116 fork-own; reach shipped 30): areas `interface`; globs `es:es-app/src/{CloudText,ThreadedCloudSync,CloudTransferJob}.*`, `es:es-app/src/guis/GuiCloud*`, `es:es-app/tests/**`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice of the fork's own pages
- **interacting subsystems** (read-only context): the cloud scripts (`cloud-sync-core`, `cloud-setup-content`); `es-player-text.md` and `es-ui-style-guide.md`
- **closing evidence**: audit folder, lint PASS, `es-unit-tests` and `tools/es-syntax-check`, frames for any visible change, punch list through Phase 7

### T9. interface: EmulationStation's RetroAchievements and offline pages

- **id**: `es-achievements-pages`; **kind**: read; **lens**: security, new functionality
- **why here**: the account pages and the offline scan, which drive the proxy (16 interface files name it)
- **paths** (16 paths, 4,929 lines, 4,929 read, of which 4,918 fork-own; reach shipped 16): areas `interface`; globs `es:es-app/src/{RetroAchievements,OfflineAchievements,ThreadedHasher,OfflineScanJob}.*`, `es:es-app/src/guis/Gui{RetroAchievements,OfflineScan,GameAchievements}*`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice; the credential handling is the proxy's slice
- **interacting subsystems** (read-only context): the proxy (`offline-achievements`); `ProxyCards` (`es-launch-path`)
- **closing evidence**: audit folder, lint PASS, `tools/ra-ui-test`, punch list through Phase 7

### T10. emulators-and-cores: RetroArch and the libretro cores

- **id**: `emulators-libretro`; **kind**: currency; **lens**: planned change (#336)
- **why here**: RetroArch is what #336's runner replaces; read before that work begins; RetroArch's patches, eight of them fork-written, are read here with the launch path (pass 6)
- **paths** (315 paths, 26,570 lines, 4,803 read, of which 987 fork-own; reach n/a 2, shipped 313): areas `emulators-and-cores`; globs `projects/ROCKNIX/packages/emulators/**`, `!projects/ROCKNIX/packages/emulators/standalone/**`; reach `shipped`, `n/a` **plus** areas `patches-and-configs`; globs `projects/ROCKNIX/packages/emulators/libretro/retroarch/**`
- **release gate**: none
- **depth**: Extended -- the launch path (RetroArch's start)
- **interacting subsystems** (read-only context): `runemu.sh` (`os-launch-control-state`); the proxy's rcheevos path (`offline-achievements`); the ES launch path (`es-launch-path`)
- **closing evidence**: audit folder, lint PASS, `tools/retroarch-wrapper-test`, punch list through Phase 7

### T11. os-scripts-and-launch: the OS's system services and platform quirks

- **id**: `os-system-services`; **kind**: read; **lens**: security, brittleness
- **why here**: busybox's configuration, the systemd units and the per-platform quirks run as root on every device
- **paths** (422 paths, 16,604 lines, 10,898 read, of which 3,002 fork-own; reach shipped 422): areas `os-scripts-and-launch`; globs `projects/ROCKNIX/packages/sysutils/**`, `projects/ROCKNIX/packages/hardware/**`, `!projects/ROCKNIX/packages/hardware/quirks/devices/**`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): `os-launch-control-state`'s scripts; the devices' options
- **closing evidence**: audit folder, lint PASS, VM proofs for boot behaviour, punch list through Phase 7

### T12. build-engine: the build engine

- **id**: `build-engine`; **kind**: read; **lens**: cost against value
- **why here**: everything else is built by it: 884 callers of its largest units for 12,328 read lines; small and central (plan § 5)
- **paths** (242 paths, 13,910 lines, 6,776 read, of which 2,419 fork-own; reach n/a 242): areas `build-engine`; globs `scripts/**`, `config/**`, `distributions/ROCKNIX/**`, `Makefile`, `Dockerfile`, `.gitignore`, `.merge-head`, `.github/**`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice; `get_env`'s secret forwarding is named for the reviewer
- **interacting subsystems** (read-only context): every package recipe; `tools/watch-build` and the admission guard (tooling); the pinned build image
- **closing evidence**: audit folder, lint PASS, `tools/pkgcheck` and a package build in the lane's own build worktree only when the brief names one, punch list through Phase 7

### T13. interface: EmulationStation's main menu (GuiMenu)

- **id**: `es-guimenu`; **kind**: read; **lens**: new functionality, brittleness
- **why here**: one file, 11,883 lines, the largest fork-own unit, where every fork page is reached from
- **paths** (2 paths, 11,883 lines, 11,883 read, of which 11,883 fork-own; reach shipped 2): areas `interface`; globs `es:es-app/src/guis/GuiMenu.*`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): every page it opens; `docs/es-menu-map.md` (D-UI-039)
- **closing evidence**: audit folder, lint PASS, `tools/es-menu-map-check`, punch list through Phase 7

### T14. doctrine: the doctrine: rules, skills, CLAUDE.md, AGENTS.md, the registers

- **id**: `doctrine`; **kind**: read; **lens**: cost against value
- **why here**: every session obeys it; a rule that lies is the most expensive cruft (plan § 5); #640's hardcoded host paths live here
- **paths** (336 paths, 59,715 lines, 190 read, of which 190 fork-own; reach n/a 336): areas `doctrine`; globs `(all)`
- **release gate**: none
- **depth**: Local -- a doctrine read (plan § 6c)
- **interacting subsystems** (read-only context): every area (25 to 29 rules govern each, cross-reference.md)
- **closing evidence**: audit folder, lint PASS, `tools/rules-check`, punch list through Phase 7

### T15. os-scripts-and-launch: the per-handheld quirks

- **id**: `os-device-quirks`; **kind**: read; **lens**: brittleness
- **why here**: 333 files over 88 handheld models: read the shipped devices' line by line and the rest as a table
- **paths** (333 paths, 10,175 lines, 9,327 read, of which 389 fork-own; reach shipped 333): areas `os-scripts-and-launch`; globs `projects/ROCKNIX/packages/hardware/quirks/devices/**`
- **release gate**: none
- **depth**: Local -- per-device configuration; the hotkey standards are the check
- **interacting subsystems** (read-only context): the device trees and options (devices)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T16. emulators-and-cores: the standalone emulators

- **id**: `emulators-standalone`; **kind**: currency; **lens**: planned change (#336)
- **why here**: the start scripts and configuration of every standalone emulator the image ships
- **paths** (543 paths, 157,365 lines, 10,695 read, of which 3,104 fork-own; reach shipped 543): areas `emulators-and-cores`; globs `projects/ROCKNIX/packages/emulators/standalone/**`; reach `shipped`, `n/a`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): `runemu.sh` (`os-launch-control-state`); the quirks; the save layout (cloud)
- **closing evidence**: audit folder, lint PASS, `tools/emulator-exit-test`, punch list through Phase 7

### T17. devices: the H700 device (RG35XX SP, RG SP)

- **id**: `device-h700`; **kind**: currency; **lens**: cost against value
- **why here**: the maintainer's test handhelds; options, device packages (u-boot DDR3/DDR4, the suspend stub), device trees and kernel configuration; its fork-written kernel configuration (8,129 lines) is read here as a diff against its base (plan § 2)
- **paths** (28 paths, 12,901 lines, 327 read, of which 0 fork-own; reach shipped 28): areas `devices`; globs `projects/ROCKNIX/devices/H700/**` **plus** areas `patches-and-configs`; globs `projects/ROCKNIX/devices/H700/linux/*.conf`
- **release gate**: none
- **depth**: Independent -- an ordinary device slice
- **interacting subsystems** (read-only context): the H700 quirks (`os-device-quirks`); the kernel patches (patches slices); `docs/device-flashing-runbook.md`
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T18. devices: the SM8550 device (Retroid Pocket Nova)

- **id**: `device-sm8550`; **kind**: currency; **lens**: cost against value
- **why here**: a shipped test device
- **paths** (29 paths, 28,053 lines, 118 read, of which 0 fork-own; reach shipped 29): areas `devices`; globs `projects/ROCKNIX/devices/SM8550/**`
- **release gate**: none
- **depth**: Independent -- an ordinary device slice
- **interacting subsystems** (read-only context): its quirks and kernel patches
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T19. devices: the RK3566 and RK3326 devices

- **id**: `device-rockchip-shipped`; **kind**: currency; **lens**: cost against value
- **why here**: the shipped Rockchip handhelds (RG353M, RG351M)
- **paths** (53 paths, 13,833 lines, 617 read, of which 0 fork-own; reach shipped 53): areas `devices`; globs `projects/ROCKNIX/devices/{RK3566,RK3326}/**`
- **release gate**: none
- **depth**: Independent -- an ordinary device slice
- **interacting subsystems** (read-only context): their quirks and kernel patches
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T20. devices: the GENERIC_X64 VM device, the kernel and drivers recipes, and the project's boot files

- **id**: `device-generic-x64-and-kernel`; **kind**: read; **lens**: cost against value
- **why here**: GENERIC_X64 is the fork's own (989 fork-own lines) and the VM every proof runs on; the kernel recipes and project bootloader serve every device; its fork-written kernel configuration (7,754 lines) is read here as a diff against its base (plan § 2)
- **paths** (64 paths, 11,500 lines, 2,902 read, of which 1,421 fork-own; reach shipped 64): areas `devices`; globs `projects/ROCKNIX/devices/GENERIC_X64/**`, `projects/ROCKNIX/packages/**`, `projects/ROCKNIX/{bootloader,filesystem}/**`, `projects/ROCKNIX/{options,config.xml}`, `packages/**`; reach `shipped`, `n/a` **plus** areas `patches-and-configs`; globs `projects/ROCKNIX/devices/GENERIC_X64/linux/*.conf`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the VM harness (tooling); every device
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T21. generic-packages: the image's own packages (projects/ROCKNIX)

- **id**: `image-packages`; **kind**: currency; **lens**: package currency
- **why here**: the ROCKNIX recipes the image installs: apps, tools, virtual packages (the emulator list), graphics, audio, network
- **paths** (531 paths, 26,529 lines, 19,018 read, of which 6,711 fork-own; reach n/a 1, shipped 530): areas `generic-packages`; globs `projects/ROCKNIX/**`; reach `shipped`, `n/a`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): every area whose package they depend on; #576 (webkitgtk)
- **closing evidence**: audit folder, lint PASS, `tools/fork-package-freshness`, punch list through Phase 7

### T22. interface: EmulationStation's other pages

- **id**: `es-pages`; **kind**: currency; **lens**: new functionality
- **why here**: the remaining pages under `guis/`: the fork-touched ones read line by line, the upstream ones checked against `rocknix/master`
- **paths** (78 paths, 16,237 lines, 16,237 read, of which 4,930 fork-own; reach shipped 78): areas `interface`; globs `es:es-app/src/guis/**`, `!es:es-app/src/guis/GuiMenu.*`, `!es:es-app/src/guis/GuiCloud*`, `!es:es-app/src/guis/Gui{RetroAchievements,OfflineScan,GameAchievements}*`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): GuiMenu (`es-guimenu`); the es-core components
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T23. interface: EmulationStation's game list views, scrapers and services

- **id**: `es-app-views-scrapers`; **kind**: currency; **lens**: cost against value
- **why here**: `views/` (8,155 lines, ViewController and the game list containers the fork changed) and the scrapers, whose ScreenScraper credentials the fork wires (#64, D-WORKFLOW-166)
- **paths** (46 paths, 20,196 lines, 20,196 read, of which 6,890 fork-own; reach shipped 46): areas `interface`; globs `es:es-app/src/{views,scrapers,services}/**`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the scrapers' developer credentials (`device-builds.md` § Build credentials); the launch path (game list to launch)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T24. interface: EmulationStation's system layer: ApiSystem, game lists, collections, metadata

- **id**: `es-app-system`; **kind**: currency; **lens**: cost against value
- **why here**: the rest of `es-app`: `ApiSystem.cpp` (3,519 fork-own lines) is the bridge to the OS scripts; game lists, collections and metadata hold the player's library
- **paths** (79 paths, 20,285 lines, 20,219 read, of which 8,531 fork-own; reach shipped 79): areas `interface`; globs `es:es-app/**`; the rest of these areas
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the OS scripts `ApiSystem` calls (`os-launch-control-state`, os-system-services); `gamelist.xml` (game content, D-CLOUD-049)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T25. interface: EmulationStation's core components

- **id**: `es-core-components`; **kind**: currency; **lens**: cost against value
- **why here**: `es-core/src/components` (21,984 lines, 9,541 fork-own): the rows, grids, menus and cards every page is built from
- **paths** (80 paths, 21,984 lines, 21,984 read, of which 9,541 fork-own; reach shipped 80): areas `interface`; globs `es:es-core/src/components/**`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): every page; `es-code-traps.md`
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T26. interface: EmulationStation's window, input, settings and the rest of es-core

- **id**: `es-core-window-input`; **kind**: currency; **lens**: cost against value
- **why here**: `Window.cpp` (one floating surface at a time, D-UI-093), `InputManager`, `Settings`, `SystemConf`, `HttpReq` (the pooled-connection trap), `GunManager` and es-core's own pages
- **paths** (102 paths, 24,875 lines, 24,875 read, of which 9,059 fork-own; reach shipped 102): areas `interface`; globs `es:es-core/**`; the rest of these areas
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): every page; `es-code-traps.md` (the pooled connection, `exists` caching, fonts)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T27. interface: EmulationStation's utilities, resources and renderers

- **id**: `es-core-utils-resources`; **kind**: currency; **lens**: cost against value
- **why here**: `utils` (40,926 lines; `StringUtil`, `Platform`, `AtomicFileUtil`, the fork's last-good writes), `resources` (fonts, textures) and `renderers`
- **paths** (60 paths, 51,884 lines, 51,884 read, of which 7,256 fork-own; reach shipped 60): areas `interface`; globs `es:es-core/src/{utils,resources,renderers}/**`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): every page; `es-code-traps.md`
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T28. interface: the EmulationStation recipe and themes in the distribution

- **id**: `es-recipe`; **kind**: read; **lens**: package currency
- **why here**: the pin, the build steps and the themes the image installs
- **paths** (15 paths, 4,561 lines, 327 read, of which 190 fork-own; reach shipped 15): areas `interface`; globs `projects/ROCKNIX/packages/ui/**`
- **release gate**: none
- **depth**: Local -- a small recipe slice
- **interacting subsystems** (read-only context): the ES tree (every `es-*` slice)
- **closing evidence**: audit folder, lint PASS, `tools/pkgcheck`

### T29. tooling-and-guards: the guards: hooks, the fork CI and the checkers

- **id**: `tooling-guards`; **kind**: read; **lens**: security, brittleness
- **why here**: the secret and wordlist guards and the ceremony state machine; 28 blindspot entries name tooling
- **paths** (29 paths, 5,632 lines, 5,356 read, of which 4,970 fork-own; reach n/a 29): areas `tooling-and-guards`; globs `.githooks/**`, `.github/**`, `tools/{forbidden-terms-check,ceremony-check,register-check,rules-check,box-check,rc-preflight,lint-audit-artifacts,archaeology,work-log-index,vocabulary-check,es-menu-map-check,fork-package-freshness,pr-stack-check,prose-check,release-catalog,renovation-inventory,fork-worktree}`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice; the secret guard is named for the reviewer
- **interacting subsystems** (read-only context): every lane's commits and pushes
- **closing evidence**: audit folder, lint PASS, `.githooks/hooks-test`, punch list through Phase 7

### T30. cloud-sync-and-saves: the cloud test harness

- **id**: `cloud-harness`; **kind**: read; **lens**: brittleness
- **why here**: `tools/cloud-round-trip` (7,808 lines) and the backends that prove the cloud slices; a harness that agrees with itself is blindspot 31
- **paths** (9 paths, 10,165 lines, 10,165 read, of which 10,165 fork-own; reach n/a 9): areas `cloud-sync-and-saves`; globs `tools/**`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the cloud slices (`cloud-sync-core`, `cloud-setup-content`)
- **closing evidence**: audit folder, lint PASS, each guard's positive recorded, punch list through Phase 7

### T31. tooling-and-guards: the VM harness

- **id**: `tooling-vm-harness`; **kind**: read; **lens**: cost against value
- **why here**: every behaviour proof runs through it (`vm-first.md`)
- **paths** (60 paths, 8,790 lines, 7,140 read, of which 7,140 fork-own; reach n/a 60): areas `tooling-and-guards`; globs `tools/{vm-*,vm-walks/**,frame-diff,time-to-play,emulator-exit-test,es-launch-memory,signin-memory,png-blackout,qa-accounts,ra-*,raofflineproxy-*,device-act,es-syntax-check,es-untranslated,font-stems}`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the GENERIC_X64 device (`device-generic-x64-and-kernel`)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T32. tooling-and-guards: the last-good scripts test

- **id**: `tooling-last-good-test`; **kind**: read; **lens**: brittleness
- **why here**: one file of 14,238 lines that proves the scripts under the image's busybox (blindspot 34): a single unit above the 12,000-line guide, kept whole because a test file split across two sessions loses its fixtures' context (plan § 5: about 8,000 to 12,000 lines, or one unit)
- **paths** (1 paths, 14,238 lines, 14,238 read, of which 14,238 fork-own; reach n/a 1): areas `tooling-and-guards`; globs `tools/last-good-scripts-test`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the OS scripts and cloud slices they prove
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T33. tooling-and-guards: the last-good, settings and state tests

- **id**: `tooling-state-tests`; **kind**: read; **lens**: brittleness
- **why here**: the `pixelelated-*`/`rasteratops-*` test family, the settings, wait-lock and upgrade tests, and their fixtures
- **paths** (22 paths, 6,807 lines, 6,807 read, of which 6,807 fork-own; reach n/a 22): areas `tooling-and-guards`; globs `tools/{settings-modes-test,melonds-upgrade-test,wait-lock-test,pixelelated-*,rasteratops-*,build-identity-test,rocknix-info-test,usb-gadget-test,nova-led-test,retroarch-wrapper-test}`, `tools/test-fixtures/**`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the OS scripts and cloud slices they prove
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T34. tooling-and-guards: build supervision and host maintenance

- **id**: `tooling-build-supervision`; **kind**: read; **lens**: brittleness
- **why here**: `watch-*`, the admission guard and the swap helper keep long jobs honest
- **paths** (18 paths, 3,795 lines, 3,384 read, of which 3,384 fork-own; reach n/a 18): areas `tooling-and-guards`; globs `tools/{watch-*,host-maintenance/**,build-preflight,fork-newdrive,fork-publish-release}`
- **release gate**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the build engine (`build-engine`)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T35. generic-packages: the generic packages the image builds

- **id**: `generic-packages-reached`; **kind**: currency; **lens**: package currency
- **why here**: upstream-carried recipes reached by a shipped plan: pins against their projects' releases
- **paths** (266 paths, 7,612 lines, 7,081 read, of which 483 fork-own; reach n/a 3, shipped 263): areas `generic-packages`; globs `packages/**`; reach `shipped`, `n/a`
- **release gate**: none
- **depth**: Local -- upstream-carried: currency first
- **interacting subsystems** (read-only context): the image's own packages (`image-packages`)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T36. build-engine: upstream's helper tools and the other distributions

- **id**: `build-engine-upstream-tools`; **kind**: table; **lens**: reachability
- **why here**: upstream tools (`distro-tool`, `mkpkg`, ...) the fork may never run, and `distributions/LibreELEC` and `LEIoT`, which nothing selects
- **paths** (135 paths, 7,369 lines, 5,552 read, of which 169 fork-own; reach n/a 108, unreached 27): areas `build-engine`; globs `tools/**`, `distributions/**`, `!distributions/ROCKNIX/**`
- **release gate**: none
- **depth**: Local -- a reachability table
- **interacting subsystems** (read-only context): the build engine (`build-engine`)
- **closing evidence**: one row per tool and distribution with its callers searched, removals with `Already written:`; audit folder, lint PASS

### T37. emulators-and-cores: emulator recipes and files no shipped image builds, and the rest of the area

- **id**: `emulators-dead-ends`; **kind**: table; **lens**: reachability
- **why here**: the generic `packages/emulation` recipes and the cores only unshipped devices build
- **paths** (86 paths, 2,399 lines, 51 read, of which 0 fork-own; reach unreached 84, unshipped 2): areas `emulators-and-cores`; globs `(all)`; the rest of these areas
- **release gate**: none
- **depth**: Local -- a reachability table
- **interacting subsystems** (read-only context): the emulator slices (`emulators-standalone`, `emulators-libretro`)
- **closing evidence**: one row per unit; audit folder, lint PASS

### T38. devices: the devices the fork does not ship and the other projects

- **id**: `devices-unshipped`; **kind**: table; **lens**: reachability
- **why here**: the unshipped devices' files and the nine LibreELEC-era projects no Makefile target builds
- **paths** (338 paths, 34,640 lines, 1,920 read, of which 0 fork-own; reach unreached 216, unshipped 122): areas `devices`; globs `projects/**`, `packages/**`, `!projects/ROCKNIX/devices/{H700,SM8550,RK3566,RK3326,GENERIC_X64}/**`; reach `unreached`, `unshipped`
- **release gate**: none
- **depth**: Local -- a reachability table
- **interacting subsystems** (read-only context): the shipped device slices
- **closing evidence**: one row per device or project; audit folder, lint PASS

### T39. patches-and-configs: patches and kernel configurations the shipped images apply

- **id**: `patches-shipped`; **kind**: table; **lens**: package currency
- **why here**: one provenance row per patch and kernel configuration a shipped image applies (#339 criterion 2): origin, merged upstream or not, the reason we carry it, the version made against, whether it still applies; the remaining fork-written patches (mesa, SDL2, shaderc, webkitgtk, woff2, zerotier-one, fex-emu, the theme, one H700 kernel patch) are read line by line in the table
- **paths** (575 paths, 153,425 lines, 0 read, of which 0 fork-own; reach shipped 575): areas `patches-and-configs`; globs `(all)`; the rest of these areas
- **release gate**: none
- **depth**: Local -- a provenance table
- **interacting subsystems** (read-only context): the packages they patch (cross-reference.md: devices 1,007, generic 505, emulators 174)
- **closing evidence**: one row per patch; audit folder, lint PASS

### T40. patches-and-configs: patches only unshipped devices apply

- **id**: `patches-unshipped`; **kind**: table; **lens**: reachability
- **why here**: 348 paths kept for devices the fork does not ship
- **paths** (348 paths, 286,952 lines, 0 read, of which 0 fork-own; reach unshipped 348): areas `patches-and-configs`; globs `(all)`; reach `unshipped`, `n/a`
- **release gate**: none
- **depth**: Local -- a provenance table
- **interacting subsystems** (read-only context): the unshipped devices (`devices-unshipped`)
- **closing evidence**: one row per patch; audit folder, lint PASS

### T41. interface: EmulationStation's vendored libraries, translations and build files

- **id**: `es-vendored-and-data`; **kind**: table; **lens**: reachability, package currency
- **why here**: `external/` (libretro-common, rcheevos, doctest, nanosvg, id3v2lib) by provenance and version; the translations and resources by coverage
- **paths** (603 paths, 377,103 lines, 146,208 read, of which 14,487 fork-own; reach shipped 603): areas `interface`; globs `es:**`, `!es:es-app/**`, `!es:es-core/**`
- **release gate**: none
- **depth**: Local -- a provenance table
- **interacting subsystems** (read-only context): the proxy's own rcheevos (`offline-achievements`)
- **closing evidence**: one row per vendored library with its version and upstream; audit folder, lint PASS

### T42. tooling-and-guards: the council toolchain and runner

- **id**: `tooling-council`; **kind**: table; **lens**: package currency
- **why here**: scaffold's export, committed byte for byte (D-WORKFLOW-088): by provenance and version only, refreshed by copying the next export (plan § 2)
- **paths** (52 paths, 25,848 lines, 24,508 read, of which 24,508 fork-own; reach n/a 52): areas `tooling-and-guards`; globs `scripts/**`, `seed/**`, `verifier-pins.json`, `council-seat-efforts.json`, `tools/council/**`
- **release gate**: none
- **depth**: Local -- a provenance table
- **interacting subsystems** (read-only context): the preliminary reviews and audits that call it
- **closing evidence**: the export's version and digest recorded; audit folder, lint PASS

### T43. records: the records

- **id**: `records`; **kind**: table; **lens**: cost against value
- **why here**: reviewed only where a record misleads a reader today (plan § 5); last, because the slices before it write records
- **paths** (126,124 paths, 22,982,979 lines, 15,392,661 read, of which 15,392,661 fork-own; reach n/a 126124): areas `records`; globs `(all)`
- **release gate**: none
- **depth**: Local -- a table
- **interacting subsystems** (read-only context): --
- **closing evidence**: one row per misleading record found, with its correction; audit folder, lint PASS

### The security, state-preservation and launch-path files

`tools/renovation-drift` reads these globs from `slices.json` (`sensitive`): a closed slice whose drift touches one re-opens at its depth, whatever its size (plan § 8).
- **security** (49 paths): `projects/ROCKNIX/packages/network/rclone/sources/cloud_{oauth,setup,remote,connections.py,log_scrub}`, `projects/ROCKNIX/packages/network/cloud-signin-window/**`, `projects/ROCKNIX/packages/network/raofflineproxy/**`, `projects/ROCKNIX/packages/rocknix/sources/scripts/{setrootpass,wifictl,usbgadget,rocknix-evidence}`, `scripts/get_env`, `.githooks/**`, `es:es-app/src/guis/GuiWifi.*`, `es:es-app/src/RetroAchievements.*`, `es:es-core/src/HttpReq.*`
- **state** (44 paths): `projects/ROCKNIX/packages/network/rclone/sources/**`, `projects/ROCKNIX/packages/rocknix/sources/scripts/{backuptool,chksysconfig,factoryreset,installtointernal,automount}`, `projects/ROCKNIX/packages/rocknix/sources/post-update`, `projects/ROCKNIX/packages/rocknix/sources/scripts/setsettings.sh`, `es:es-core/src/{Settings,SystemConf}.*`, `es:es-core/src/utils/AtomicFileUtil.*`, `es:es-app/src/{CloudTransferJob,ThreadedCloudSync,SaveStateBookkeeper,SaveStateRepository}.*`
- **launch-path** (169 paths): `projects/ROCKNIX/packages/rocknix/sources/scripts/{runemu.sh,setsettings.sh,run}`, `projects/ROCKNIX/packages/emulators/libretro/retroarch/**`, `es:es-app/src/{FileData,SystemData,LaunchCommand,ProxyCards}.*`, `es:es-app/src/main.cpp`

<!-- renovation-inventory --order: end -->

## The preliminary review of this order

Status: **pending** -- the three-seat advisory review
(`.claude/skills/council/references/review-formats.md`) runs at the end of
pass 6, before the pass-7 post on #641. This section then records `reviewed`
with the run id, or `unreviewed` with the reason, and answers each material
objection by name.
