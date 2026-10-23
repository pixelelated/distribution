# The renovation order

**Issue:** #641 (M6.P1, the survey), carrying #346's order-and-method
criteria; epic #339; milestone M6. **Status: proposed, fourth version** --
the second was posted on #641 at the pass-7 gate; the third absorbed the
maintainer's answer to its first question (the shipped devices,
D-WORKFLOW-185) and the weight on the build process given with it
(D-WORKFLOW-186); this one absorbs D-WORKFLOW-187 (the renovation gates no
release; the second question withdrawn), changes no slice's place or paths,
and is posted on #641 again. No slice issue is filed before the maintainer's
yes (brief § 8). **Register row:** written at the yes, with the next free
`D-WORKFLOW` ID above the P0 branch's highest (D-WORKFLOW-187 today;
re-derived with the brief § 6 greps then), citing D-WORKFLOW-185,
D-WORKFLOW-186 and D-WORKFLOW-187.

This is the order in which the whole codebase is renovated, slice by slice,
under the plan (`plan-for-the-plan.md`). It was produced by the seven-pass
survey recorded in `p1-tracking.md`, from four generated ledgers:
`inventory.md` (every path with its tier, size and reachability),
`assessment.md` (the six ordering lenses' evidence per area),
`cross-reference.md` (every area against every other), and the slice sizes in
the block below. The hand-written input is `slices.json`; `tools/renovation-inventory
--order` sizes every slice from the inventory, proves that every tracked path
is in exactly one slice, and renders the block between the markers. The
three-seat preliminary review (below) read the first version of this order;
the second was revised from its findings; the third re-sequenced the second
under the maintainer's two answers; this fourth removes the release gates
(D-WORKFLOW-187) without moving a slice. The renumbering is tabled at the end of
this section.

## How the order was argued

Plan § 6a's six lenses, scored per area in `p1-tracking.md` § Pass 3, ordered
the second version. The maintainer's answers at pass 7 put two constraints
above them, so this version is argued from five fixed constraints first, and
the lenses order what is left.

1. **The launch path is read before #336 Step 1 replaces it (D-WORKFLOW-187).**
   The renovation gates no release: it decides what is read, in what order
   and at what depth, never what ships or when. A finding that is a defect
   is filed as a bug the session it is found and reaches a release as every
   bug does (D-QA-051, `tools/rc-preflight`), owned by the release's
   milestone, never by a slice. D-WORKFLOW-102's release clause is retired;
   its placed, progressive review stands. The one prerequisite that stands is
   a reading order: Tier 1's launch, control and state slice (T1) and the
   interface's launch-path slice (T2) are read before #336 Step 1 replaces
   what they read. They are first on the order's own lenses too (planned
   change, security), and D-WORKFLOW-186 keeps them there. **What T1
   covers:** the `rocknix` package's launch, control and state scripts
   (`runemu.sh`, `setsettings.sh`, `post-update`, `chksysconfig`,
   `factoryreset`, `installtointernal`, `automount`; the updater among
   them). `backuptool` (the settings archives, T17) and the system services
   (T22) are read in their own Extended slices. The pass-7 question whether
   either should also gate `0.1` was withdrawn as outside the program
   (D-WORKFLOW-187).
2. **#336's own prerequisite stays third.** T3 is RetroArch, the libretro
   cores and `projects/ROCKNIX/packages/virtual/emulators`, whose
   `mk_es_systems` writes `es_systems.cfg`, the launch command table.
   `runemu.sh` configures and starts RetroArch, and #336's runner replaces it,
   so T3 carries #336 Step 1 as its prerequisite. That is the order's own
   reading of #336 rather than D-WORKFLOW-187's words, so D-WORKFLOW-186
   could have moved it behind the build process. It stays because it shares
   T2's prerequisite:
   behind ten build and harness slices it would hold #336 Step 1 for no
   gain, and it is itself a currency slice (the cores' pins against their
   releases), the question D-WORKFLOW-186 puts first.
3. **The build process before any device and before the rest of the
   interface (D-WORKFLOW-186).** The maintainer, 2026-10-23: *"we're going to
   find more value in likely evaluating our build process itself [...] we
   want to make sure package updates, our test harness updates, the actual
   build process, test process, and everything around that are fully up to
   date."* So T5 to T15 are one cluster, in three steps:
   - *The build, T5 to T9.* The build engine (T5), then the rest of its area
     (T6, upstream's tools and the other distributions, a Local table, so
     the engine is read whole), then package currency: the generic recipes
     the images build, pinned against their releases (T7, a table), and the
     ROCKNIX recipes the image installs (T8, a currency slice; the
     maintainer's "package updates" covers both, and T7 is first because
     T8's overrides source T7's recipes), then the supervision every long
     build runs under (T9). #644 reads ROCKNIX's documented build path
     against ours; its findings are an input to T5 and T9, not a change to
     their paths.
   - *The guards, T10.* Every slice's commits pass through them and every
     slice closes on `tools/lint-audit-artifacts`, so they follow the build
     they guard and precede everything they check.
   - *The test process, T11 to T15.* The test image first (T11: GENERIC_X64,
     the kernel recipes and the project's boot files, D-WORKFLOW-185), then
     the VM harness that boots it (T12), the cloud harness (T13), the state
     tests (T14) and the last-good scripts test (T15). The second version
     read the harness last, after the code it proves, so a slice could fix a
     test it found wrong. D-WORKFLOW-186 reverses that: a harness made
     current first is what every later slice's VM proof runs on, and a
     defect in it found late is a defect every earlier proof passed through
     (`engineering-practices.md` § Guards must fail closed). A later slice
     that finds a test wrong still fixes it; `tools/renovation-drift`
     re-opens the harness slice if the fix is large.
4. **Shipped is H700 and SM8550, and GENERIC_X64 is the test image
   (D-WORKFLOW-185).** The second version took `device-builds.md`'s five.
   - The RK3566 and RK3326 slice is dissolved: its 53 device paths are rows
     in T25. Six paths of three driver and firmware recipes only those two
     build (`generic-dsi`, `mali-bifrost`, `esp8089-firmware`) leave T11 for
     T25, and 17 paths of ROCKNIX recipes only they build (`libmali`,
     `librga`, `gpudriver`, `rkbin`, `rkmpp`, `device-switch`'s RK3326
     scripts, ...) leave T8 for T23. 72 kernel patches and configurations only those two
     apply leave the shipped kernel table (T41) for T43, and 12 other
     patches leave T42 for T43.
   - The inventory gained a fifth `reach` value, `test`: a path the
     GENERIC_X64 plan reaches and no shipped device's (31 paths: `syslinux`,
     the installer, `dmidecode`, `pciutils`, the VM device's own files). With
     only two shipped devices those would have read `unshipped` and sat in
     the dead-end tables beside paths no image needs. Every read slice that
     took `shipped` takes `test` too.
   - Unshipped is not dead. RK3566 and RK3326 are the recorded first
     widening, and every unshipped target is upstream's: a table row records
     the target; it is not a proposal to remove support the fork carries
     unchanged. Opening either target is a device build with its own issue,
     and the tables re-derive then.
   - T29's run-time derivation of the quirks models uses the shipped pair
     and the VM.
5. **Each of the first three is one session.** T1 reads 11,560 lines and T2
   11,287. T3 reads 5,519 fork-own lines plus 1,670 lines of RetroArch's
   patches (#346's second criterion; plan § 5).

After those, the lenses order the rest, as they did in the second version:

- **The parts that hold a player's data or credentials (security,
  brittleness, new functionality).** T16 and T17 are cloud sync (the highest
  brittleness of the product areas: 19 blindspot entries, 47 closed bugs,
  +28,279 lines since the base), and T18 is their EmulationStation pages,
  which name those scripts in 36 files. T19 is the offline achievements
  proxy, a network listener holding an account token, and T20 its pages. T21
  is ES's state primitives and the bridge every page uses to run the OS
  scripts. T22 is the OS's system services, run as root on every device.
  Each seam is read pair by pair, because the defects live at the seam
  (plan § 5). T18, T20 and T21 are interface slices with no reading-order
  prerequisite, so D-WORKFLOW-186 puts them after the build cluster, and their back ends
  travel with them.
- **The doctrine before all of it (cost against value).** T4 reads the
  binding doctrine (the rules, `CLAUDE.md`, `AGENTS.md`, the registers;
  #640's hardcoded paths) right after #336's three prerequisites: it is one
  Local session,
  and every later slice, the build engine's included, is read against the
  rules it states (`device-builds.md`, `packaging-and-patches.md`), so they
  are made true first.
- **Dead ends, cheap and Local (reachability).** T23 to T25 are tables: the
  generic packages no image builds, the emulator recipes no shipped image
  builds, and the devices the fork neither ships nor tests on with the other
  projects. They need no second opinion, can run beside any read slice in
  another area (plan § 6), and what they remove shrinks the later slices.
- **Then the devices and what they run.** T26 to T30: GuiMenu (the largest
  fork-own unit), one slice per shipped device (H700, SM8550), the
  per-handheld quirks and the standalone emulators.
- **Then the rest of the interface, framework last.** T31 to T37: the other
  pages, the application core, then es-core (components, window and input,
  utilities), read after the pages that use them, then the recipe.
- **Then the rest of the doctrine.** T38 and T39: the skills and the
  reference documents.
- **Last, the provenance tables.** T40 to T46: the patches no plan applies,
  the shipped and test images' kernel patches, their other patches and the
  unshipped ones; ES's vendored libraries and data; the council toolchain
  (by version only, plan § 2); the records. The patch tables follow the
  package currency slices because a bump there retires or rebases the
  patches they would otherwise tabulate.

**Renumbering, second version to third** (the preliminary review's answers
below use the second version's numbers):

| Second | Third | Slice |
| ---: | ---: | --- |
| T1 to T4 | T1 to T4 | #336's three prerequisites (the second version's gates), the doctrine |
| T13 | T5 | `build-engine` |
| T16 | T6 | `build-engine-upstream-tools` |
| T40 | T7 | `generic-packages-reached` |
| T25 | T8 | `image-packages` |
| T38 | T9 | `tooling-build-supervision` |
| T5 | T10 | `tooling-guards` |
| T19 | T11 | `device-generic-x64-and-kernel` |
| T35 | T12 | `tooling-vm-harness` |
| T34 | T13 | `cloud-harness` |
| T37 | T14 | `tooling-state-tests` |
| T36 | T15 | `tooling-last-good-test` |
| T6 to T12 | T16 to T22 | cloud, the proxy, ES's state and bridge, the system services |
| T14, T15, T17 | T23, T24, T25 | the dead-end tables |
| T18, T20, T21 | T26, T27, T28 | GuiMenu, H700, SM8550 |
| T22 | -- | `device-rockchip-shipped`, dissolved into T25, T8 to T23, T41 and T42 to T43 |
| T23, T24 | T29, T30 | the quirks, the standalone emulators |
| T26 to T33 | T31 to T38 | the other interface slices, the recipe, the skills |
| T39 | T39 | `doctrine-reference` |
| T41 to T47 | T40 to T46 | the patch tables, ES's vendored files, the council toolchain, the records |

**Slice kinds.**

- A *read* slice reads its code line by line.
- A *currency* slice is mostly upstream-carried. It reads its fork-own files
  line by line and asks the reachability and currency questions of the rest
  first (plan § 2, § 3 principle 1), so its size is its fork-own lines.
- A *prose* slice (the doctrine) reads its text, so its size is its lines.
- A *table* slice produces one row per path, generated from `inventory.json`
  and, for patches, from each patch's header. The session's work is the
  decisions: origin, applicability and removal.

**Fork-written vendor files are read with their code.** The plan (§ 2) reads
vendor-carried patches and kernel configurations by provenance only. This
order refines that rule: a patch or configuration the fork wrote
(`tier_note: fork-written`) is read line by line in the slice of the code it
changes. The proxy's patches are read in T19, RetroArch's in T3, and the
H700 and GENERIC_X64 kernel configurations in T27 and T11, as a diff against
their base. The rest stay in the tables, which read their fork-written rows
in full. The refinement is part of the order's register row.

**Depth** (plan § 6c, D-WORKFLOW-137):

- *Extended* (two reviewers from two other labs): every slice that holds a
  file on the security, state-preservation or launch-path lists below. Those
  are T1 to T3, T5, T10, T16 to T22 and T30: thirteen, as in the second
  version (the dissolved slice was Independent).
- *Independent* for an ordinary code slice.
- *Local* for tables and the doctrine.

A sensitive file that drift touches re-opens its slice **at Extended**,
whatever the slice's depth (plan § 8). The executor is an Anthropic model, so
its reviewers are GPT-6 Astra and, for Extended, Gemini 4 Argon (plan § 6c).
The maintainer may lower depths to save OpenRouter credit (plan § 11 Q3);
the depths above are the plan's rule applied, before any such choice.

**Two exceptions to the size guide.** T15 is one file,
`tools/last-good-scripts-test`, 14,238 lines. It is an explicit exception to
plan § 5, which bounds a slice by about 8,000 to 12,000 lines, one package
group or one device: a test split across two sessions loses its fixtures'
context, and the brief invites its split as a Q7 finding. T38 is 12,734 lines
of skills, which cross-reference each other.

**What every slice owes** is plan § 6b's per-slice procedure, from scope to
close. Each slice's issue carries its paths (the `select` of `slices.json`),
its tiers, line count, lens, interacting subsystems, depth, any
reading-order prerequisite (`read_before`; T1 to T3 only), and empty
`reviewed-at` and `fixed-at` fields. An EmulationStation slice records
`fixed-at-es` beside them (both trees, `tools/renovation-drift`).

<!-- renovation-inventory --order: begin -->

Generated by `tools/renovation-inventory --order` from `slices.json` and `inventory.json` (distribution `be3ddf13c5`, ES `16dbac5211`); edit `slices.json`, never this block. Every tracked path is in exactly one slice: `unassigned: 0`, `ambiguous: 0` over 134,633 rows. *Read* is code lines a slice reads line by line (code languages, not vendor-carried, not unreached); a *currency* slice reads its fork-own files line by line and checks the rest for reachability and currency (plan § 2), so its size is its fork-own lines; a table slice reads rows, one per path, not lines; a *prose* slice (the doctrine) reads its text, so its size is its lines. *Patch and config lines* are the vendor-carried files the slice holds (fork-written ones are read with their code, the rest by provenance), counted apart from *Read*.

| k | Slice | Area | Kind | Lens | Paths | Lines | Read (fork-own) | Patch and config lines | Depth |
| ---: | --- | --- | --- | --- | ---: | ---: | --- | ---: | --- |
| 1 | the OS scripts: launch, control and state (Tier 1) | os-scripts-and-launch | read | planned change (#336), security, brittleness | 83 | 13,327 | 11,560 (7,441) | 0 | Extended |
| 2 | EmulationStation's launch path | interface | read | planned change (#336 Step 1), security | 20 | 11,287 | 11,287 (10,804) | 0 | Extended |
| 3 | RetroArch and the libretro cores | emulators-and-cores | currency | planned change (#336) | 344 | 31,961 | 10,185 (5,519) | 1,670 | Extended |
| 4 | the binding doctrine: rules, CLAUDE.md, AGENTS.md, the registers | doctrine | prose | cost against value | 36 | 11,412 | 11,412 of prose | 0 | Local |
| 5 | the build engine | build-engine | read | cost against value | 242 | 13,910 | 6,776 (2,419) | 0 | Extended |
| 6 | upstream's helper tools and the other distributions | build-engine | table | reachability | 135 | 7,369 | -- (135 rows) | 0 | Local |
| 7 | the generic packages the image builds | generic-packages | table | package currency | 266 | 7,612 | -- (266 rows) | 0 | Local |
| 8 | the image's own packages (projects/ROCKNIX) | generic-packages | currency | package currency | 485 | 20,644 | 13,145 (2,179) | 0 | Independent |
| 9 | build supervision and host maintenance | tooling-and-guards | read | brittleness | 18 | 3,795 | 3,384 (3,384) | 0 | Independent |
| 10 | the guards: hooks, the fork CI and the checkers | tooling-and-guards | read | security, brittleness | 31 | 6,662 | 6,386 (6,000) | 0 | Extended |
| 11 | the GENERIC_X64 VM device, the kernel and drivers recipes, and the project's boot files | devices | read | cost against value | 58 | 10,418 | 1,820 (1,421) | 7,754 | Independent |
| 12 | the VM harness | tooling-and-guards | read | cost against value | 60 | 8,790 | 7,140 (7,140) | 0 | Independent |
| 13 | the cloud test harness | cloud-sync-and-saves | read | brittleness | 9 | 10,165 | 10,165 (10,165) | 0 | Independent |
| 14 | the last-good, settings and state tests | tooling-and-guards | read | brittleness | 32 | 6,911 | 6,807 (6,807) | 0 | Independent |
| 15 | the last-good scripts test | tooling-and-guards | read | brittleness | 1 | 14,238 | 14,238 (14,238) | 0 | Independent |
| 16 | cloud sync: the sync, backup, restore and capture core | cloud-sync-and-saves | read | security, brittleness, new functionality | 14 | 8,316 | 7,827 (7,827) | 0 | Extended |
| 17 | cloud sync: setup, sign-in, connections, content and settings backups | cloud-sync-and-saves | read | security | 14 | 11,180 | 11,180 (11,180) | 0 | Extended |
| 18 | EmulationStation's cloud pages, cards and text, with their unit tests | interface | read | brittleness, new functionality | 30 | 11,193 | 11,116 (11,116) | 0 | Extended |
| 19 | the offline achievements proxy | offline-achievements | read | security, new functionality | 27 | 5,369 | 3,656 (3,656) | 1,703 | Extended |
| 20 | EmulationStation's RetroAchievements and offline pages | interface | read | security, new functionality | 25 | 7,485 | 7,427 (7,416) | 0 | Extended |
| 21 | EmulationStation's state primitives and its bridge to the OS | interface | read | security, state preservation (the preliminary review) | 14 | 9,249 | 9,249 (9,249) | 0 | Extended |
| 22 | the OS's system services and platform quirks | os-scripts-and-launch | read | security, brittleness | 422 | 16,604 | 10,898 (3,002) | 0 | Extended |
| 23 | the generic packages no image builds | generic-packages | table | reachability | 1,604 | 95,892 | -- (1,604 rows) | 0 | Local |
| 24 | emulator recipes and files no shipped image builds, and the rest of the area | emulators-and-cores | table | reachability | 86 | 2,399 | -- (86 rows) | 0 | Local |
| 25 | the devices the fork does not ship and the other projects | devices | table | reachability | 397 | 49,555 | -- (397 rows) | 0 | Local |
| 26 | EmulationStation's main menu (GuiMenu) | interface | read | new functionality, brittleness | 2 | 11,883 | 11,883 (11,883) | 0 | Independent |
| 27 | the H700 device (RG35XX SP, RG SP) | devices | currency | cost against value | 28 | 12,901 | 327 (0) | 8,129 | Independent |
| 28 | the SM8550 device (Retroid Pocket Nova) | devices | currency | cost against value | 29 | 28,053 | 118 (0) | 0 | Independent |
| 29 | the per-handheld quirks | os-scripts-and-launch | currency | brittleness | 333 | 10,175 | 9,327 (389) | 0 | Independent |
| 30 | the standalone emulators | emulators-and-cores | currency | launch path, brittleness | 543 | 157,365 | 10,695 (3,104) | 0 | Extended |
| 31 | EmulationStation's other pages | interface | currency | new functionality | 76 | 15,537 | 15,537 (4,230) | 0 | Independent |
| 32 | EmulationStation's game list views, scrapers and services | interface | currency | cost against value | 42 | 17,311 | 17,311 (4,005) | 0 | Independent |
| 33 | EmulationStation's system layer: ApiSystem, game lists, collections, metadata | interface | currency | cost against value | 77 | 16,276 | 16,210 (4,522) | 0 | Independent |
| 34 | EmulationStation's core components | interface | currency | cost against value | 80 | 21,984 | 21,984 (9,541) | 0 | Independent |
| 35 | EmulationStation's window, input, settings and the rest of es-core | interface | currency | cost against value | 96 | 22,575 | 22,575 (6,759) | 0 | Independent |
| 36 | EmulationStation's utilities, resources and renderers | interface | currency | cost against value | 58 | 50,840 | 50,840 (6,212) | 0 | Independent |
| 37 | the EmulationStation recipe and themes in the distribution | interface | read | package currency | 15 | 4,561 | 327 (190) | 0 | Independent |
| 38 | the skills, agents and settings | doctrine | prose | cost against value | 52 | 12,734 | 12,734 of prose | 0 | Local |
| 39 | the reference documents | doctrine | table | cost against value | 253 | 38,183 | -- (253 rows) | 0 | Local |
| 40 | patches and kernel configurations no plan applies | patches-and-configs | table | reachability | 778 | 317,908 | -- (778 rows) | 317,908 | Local |
| 41 | kernel patches and configurations the shipped and test images apply | patches-and-configs | table | package currency | 107 | 40,474 | -- (107 rows) | 40,474 | Local |
| 42 | the other patches the shipped and test images apply | patches-and-configs | table | package currency | 384 | 71,387 | -- (384 rows) | 71,387 | Local |
| 43 | patches only unshipped devices apply | patches-and-configs | table | reachability | 432 | 328,516 | -- (432 rows) | 328,516 | Local |
| 44 | EmulationStation's vendored libraries, translations and build files | interface | table | reachability, package currency | 594 | 374,547 | -- (594 rows) | 0 | Local |
| 45 | the council toolchain and runner | tooling-and-guards | table | package currency | 52 | 25,848 | -- (52 rows) | 0 | Local |
| 46 | the records | records | table | cost against value | 126,149 | 22,984,459 | -- (126,149 rows) | 0 | Local |

### T1. os-scripts-and-launch: the OS scripts: launch, control and state (Tier 1)

- **id**: `os-launch-control-state`; **kind**: read; **lens**: planned change (#336), security, brittleness
- **why here**: Tier 1's launch, control and state slice (D-WORKFLOW-102's placed review), read before #336 Step 1 replaces what it reads (D-WORKFLOW-187's reading order; the renovation gates no release); `runemu.sh` configures and starts RetroArch, which #336 replaces (`grep -ci retroarch runemu.sh` is 22); the package runs as root at boot and launch, and scores high on security and brittleness (assessment.md); the slice covers this package's launch, control and state scripts (runemu.sh, setsettings.sh, post-update, chksysconfig, factoryreset, installtointernal, automount: the updater among them); `backuptool` (the settings archives) is read in `cloud-setup-content` and the system services in `os-system-services`, each at Extended depth
- **paths** (83 paths, 13,327 lines, 11,560 read, of which 7,441 fork-own; 0 patch and config lines; reach shipped 83): areas `os-scripts-and-launch`; globs `projects/ROCKNIX/packages/rocknix/**`
- **read before**: #336 Step 1 (D-WORKFLOW-187)
- **depth**: Extended -- launch path and state preservation (plan § 6c)
- **interacting subsystems** (read-only context): the interface's launch path (`es-launch-path`: `FileData::launchGame`, `ViewController`, `LaunchCommand.h` read `runemu.sh`'s arguments); `es_systems.cfg`, generated by `projects/ROCKNIX/packages/virtual/emulators` (`emulators-libretro`); ES's bridge to these scripts, `ApiSystem` (`es-state-and-bridge`); the systemd units, power and sleep scripts (`os-system-services`); the per-handheld quirks read at launch (`os-device-quirks`); `backuptool` and the cloud hooks (`cloud-setup-content`, `cloud-sync-core`); `system.cfg` through `get_setting`/`set_setting`
- **closing evidence**: audit folder `docs/audits/<date>-epic-m6-os-launch-control-state/` with `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `tools/lint-audit-artifacts` PASS with the renovation face, the punch-list issue resolved through Phase 7, `reviewed-at` and `fixed-at` set

### T2. interface: EmulationStation's launch path

- **id**: `es-launch-path`; **kind**: read; **lens**: planned change (#336 Step 1), security
- **why here**: the interface's launch-path slice is read before #336 Step 1 replaces it (D-WORKFLOW-187's reading order); `FileData::launchGame` asks over running syncs (D-UI-095), so the proxy cards and save-state bookkeeping ride the same path; `ViewController.cpp:483` is where the game list hands a game to `launchGame` (preliminary review, claude and gemini)
- **paths** (20 paths, 11,287 lines, 11,287 read, of which 10,804 fork-own; 0 patch and config lines; reach shipped 20): areas `interface`; globs `es:es-app/src/{FileData,SystemData,LaunchCommand,ProxyCards}.*`, `es:es-app/src/main.cpp`, `es:es-app/src/SaveState*`, `es:es-app/src/views/ViewController.*`
- **read before**: #336 Step 1 (D-WORKFLOW-187)
- **depth**: Extended -- launch path (plan § 6c)
- **interacting subsystems** (read-only context): `runemu.sh` and `setsettings.sh` (`os-launch-control-state`); `es_systems.cfg` and its generator (`emulators-libretro`); the cloud sync cards a launch asks over (`ThreadedCloudSync`, `es-cloud-pages`); ES's state primitives `Settings`, `SystemConf` and `AtomicFileUtil` (`es-state-and-bridge`); the proxy (`offline-achievements`); `es_settings.cfg` and `system.cfg`
- **closing evidence**: audit folder `docs/audits/<date>-epic-m6-es-launch-path/` with `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `tools/lint-audit-artifacts` PASS with the renovation face, the punch-list issue resolved through Phase 7, `reviewed-at` and `fixed-at` set

### T3. emulators-and-cores: RetroArch and the libretro cores

- **id**: `emulators-libretro`; **kind**: currency; **lens**: planned change (#336)
- **why here**: RetroArch is what #336's runner replaces; read before that work begins; RetroArch's patches, eight of them fork-written, are read here with the launch path (pass 6); `projects/ROCKNIX/packages/virtual/emulators` is read here too, because its `mk_es_systems` writes `es_systems.cfg`, the launch command table #336 rewrites
- **paths** (344 paths, 31,961 lines, 10,185 read, of which 5,519 fork-own; 1,670 patch and config lines; reach n/a 2, shipped 342): areas `emulators-and-cores`; globs `projects/ROCKNIX/packages/emulators/**`, `!projects/ROCKNIX/packages/emulators/standalone/**`; reach `shipped`, `test`, `n/a` **plus** areas `patches-and-configs`; globs `projects/ROCKNIX/packages/emulators/libretro/retroarch/**` **plus** areas `generic-packages`; globs `projects/ROCKNIX/packages/virtual/emulators/**`
- **read before**: #336 Step 1 (the order's own prerequisite: #336's runner replaces what this slice reads)
- **depth**: Extended -- the launch path (RetroArch's start)
- **interacting subsystems** (read-only context): `runemu.sh` (`os-launch-control-state`); the ES launch path (`es-launch-path`, which parses `es_systems.cfg`); the proxy's rcheevos path (`offline-achievements`); the save layout cloud sync moves (`cloud-sync-core`)
- **closing evidence**: audit folder, lint PASS, `tools/retroarch-wrapper-test`, punch list through Phase 7

### T4. doctrine: the binding doctrine: rules, CLAUDE.md, AGENTS.md, the registers

- **id**: `doctrine-rules`; **kind**: prose; **lens**: cost against value
- **why here**: every session obeys it, and a rule that lies is the most expensive cruft (plan § 5); #640's hardcoded host paths live here. Early (gemini, claude), so the rules every later slice reads are current
- **paths** (36 paths, 11,412 lines, 0 read, of which 0 fork-own; 0 patch and config lines; reach n/a 36): areas `doctrine`; globs `.claude/rules/**`, `CLAUDE.md`, `AGENTS.md`, `NAMING.md`, `docs/{decision-register,blindspot-register,friction-log}.md`
- **read before**: none
- **depth**: Local -- a doctrine read (plan § 6c)
- **interacting subsystems** (read-only context): every area (25 to 29 rules govern each, cross-reference.md)
- **closing evidence**: audit folder `docs/audits/<date>-epic-m6-doctrine-rules/` with `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `tools/lint-audit-artifacts` PASS with the renovation face, the punch-list issue resolved through Phase 7, `reviewed-at` and `fixed-at` set

### T5. build-engine: the build engine

- **id**: `build-engine`; **kind**: read; **lens**: cost against value
- **why here**: everything else is built by it: 884 callers of its largest units for 6,776 read lines (the area's 12,328 include the upstream tools of `build-engine-upstream-tools`); small and central (plan § 5); first after #336's three prerequisites and the doctrine under D-WORKFLOW-186, the maintainer's weight on the build process ahead of any device target, read against ROCKNIX's own documented build path (#644's findings) as well as the fork's rules
- **paths** (242 paths, 13,910 lines, 6,776 read, of which 2,419 fork-own; 0 patch and config lines; reach n/a 242): areas `build-engine`; globs `scripts/**`, `config/**`, `distributions/ROCKNIX/**`, `Makefile`, `Dockerfile`, `.gitignore`, `.merge-head`, `.github/**`
- **read before**: none
- **depth**: Extended -- `scripts/get_env`'s secret forwarding is on the security list (plan § 6c)
- **interacting subsystems** (read-only context): every package recipe; `tools/watch-build` and the admission guard (tooling); the pinned build image
- **closing evidence**: audit folder `docs/audits/<date>-epic-m6-build-engine/` with `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `tools/lint-audit-artifacts` PASS with the renovation face, the punch-list issue resolved through Phase 7, `reviewed-at` and `fixed-at` set; `tools/pkgcheck` where a recipe changes; no image or package build (plan § 7 item 5)

### T6. build-engine: upstream's helper tools and the other distributions

- **id**: `build-engine-upstream-tools`; **kind**: table; **lens**: reachability
- **why here**: upstream tools (`distro-tool`, `mkpkg`, ...) the fork may never run, and `distributions/LibreELEC` and `LEIoT`, which nothing selects; with the build engine, so the engine is read whole before anything it builds (D-WORKFLOW-186, the maintainer's weight on the build process ahead of any device target)
- **paths** (135 paths, 7,369 lines, -- read, of which -- fork-own; 0 patch and config lines; reach n/a 108, unreached 27): areas `build-engine`; globs `tools/**`, `distributions/**`, `!distributions/ROCKNIX/**`
- **read before**: none
- **depth**: Local -- a reachability table
- **interacting subsystems** (read-only context): the build engine (`build-engine`)
- **closing evidence**: one row per tool and distribution with its callers searched, removals with `Already written:`; audit folder, lint PASS

### T7. generic-packages: the generic packages the image builds

- **id**: `generic-packages-reached`; **kind**: table; **lens**: package currency
- **why here**: upstream-carried recipes reached by a shipped plan or the test image's: pins against their projects' releases; with the build engine under D-WORKFLOW-186, the maintainer's weight on the build process ahead of any device target ("package updates ... fully up to date")
- **paths** (266 paths, 7,612 lines, -- read, of which -- fork-own; 0 patch and config lines; reach n/a 3, shipped 256, test 7): areas `generic-packages`; globs `packages/**`; reach `shipped`, `test`, `n/a`
- **read before**: none
- **depth**: Local -- a currency table: each upstream-carried recipe's pin against its project's releases (plan § 6c)
- **interacting subsystems** (read-only context): the image's own packages (`image-packages`)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T8. generic-packages: the image's own packages (projects/ROCKNIX)

- **id**: `image-packages`; **kind**: currency; **lens**: package currency
- **why here**: the ROCKNIX recipes the image installs: apps, tools, virtual packages (the emulator list), graphics, audio, network; package currency, with the build engine under D-WORKFLOW-186, the maintainer's weight on the build process ahead of any device target
- **paths** (485 paths, 20,644 lines, 13,145 read, of which 2,179 fork-own; 0 patch and config lines; reach n/a 1, shipped 478, test 6): areas `generic-packages`; globs `projects/ROCKNIX/**`, `!projects/ROCKNIX/packages/virtual/emulators/**`; reach `shipped`, `test`, `n/a`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): every area whose package they depend on; #576 (webkitgtk)
- **closing evidence**: audit folder, lint PASS, `tools/fork-package-freshness`, punch list through Phase 7

### T9. tooling-and-guards: build supervision and host maintenance

- **id**: `tooling-build-supervision`; **kind**: read; **lens**: brittleness
- **why here**: `watch-*`, the admission guard and the swap helper keep long jobs honest; with the build engine under D-WORKFLOW-186, the maintainer's weight on the build process ahead of any device target ("the actual build process"), #644's findings an input
- **paths** (18 paths, 3,795 lines, 3,384 read, of which 3,384 fork-own; 0 patch and config lines; reach n/a 18): areas `tooling-and-guards`; globs `tools/{watch-*,host-maintenance/**,build-preflight,fork-newdrive,fork-publish-release}`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the build engine (`build-engine`)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T10. tooling-and-guards: the guards: hooks, the fork CI and the checkers

- **id**: `tooling-guards`; **kind**: read; **lens**: security, brittleness
- **why here**: the secret and wordlist guards and the ceremony state machine; 28 blindspot entries name tooling; early, because every slice's commits pass through these guards and every slice closes on `tools/lint-audit-artifacts`, and because the survey's own tools (`renovation-inventory`, `-drift`, `-status`) are what the dead-end tables trust; with the build and test cluster under D-WORKFLOW-186, the maintainer's weight on the build process ahead of any device target
- **paths** (31 paths, 6,662 lines, 6,386 read, of which 6,000 fork-own; 0 patch and config lines; reach n/a 31): areas `tooling-and-guards`; globs `.githooks/**`, `.github/**`, `tools/{forbidden-terms-check,ceremony-check,register-check,rules-check,box-check,rc-preflight,lint-audit-artifacts,archaeology,work-log-index,vocabulary-check,es-menu-map-check,fork-package-freshness,pr-stack-check,prose-check,release-catalog,renovation-inventory,renovation-drift,renovation-status,fork-worktree}`
- **read before**: none
- **depth**: Extended -- `.githooks/**`, the secret and wordlist guards, are on the security list (plan § 6c)
- **interacting subsystems** (read-only context): every lane's commits and pushes
- **closing evidence**: audit folder, lint PASS, `.githooks/hooks-test`, punch list through Phase 7

### T11. devices: the GENERIC_X64 VM device, the kernel and drivers recipes, and the project's boot files

- **id**: `device-generic-x64-and-kernel`; **kind**: read; **lens**: cost against value
- **why here**: GENERIC_X64 is the fork's own (989 fork-own lines) and the VM every proof runs on; the kernel recipes and project bootloader serve every device; its fork-written kernel configuration (7,754 lines) is read here as a diff against its base (plan § 2); the test image (D-WORKFLOW-185), read with the harness that boots it under D-WORKFLOW-186, the maintainer's weight on the build process ahead of any device target ("test process")
- **paths** (58 paths, 10,418 lines, 1,820 read, of which 1,421 fork-own; 7,754 patch and config lines; reach shipped 49, test 9): areas `devices`; globs `projects/ROCKNIX/devices/GENERIC_X64/**`, `projects/ROCKNIX/packages/**`, `projects/ROCKNIX/{bootloader,filesystem}/**`, `projects/ROCKNIX/{options,config.xml}`, `packages/**`; reach `shipped`, `test`, `n/a` **plus** areas `patches-and-configs`; globs `projects/ROCKNIX/devices/GENERIC_X64/linux/*.conf`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the VM harness (tooling); every device
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T12. tooling-and-guards: the VM harness

- **id**: `tooling-vm-harness`; **kind**: read; **lens**: cost against value
- **why here**: every behaviour proof runs through it (`vm-first.md`); read before the code it proves under D-WORKFLOW-186, the maintainer's weight on the build process ahead of any device target: the proofs every later slice runs are made current first
- **paths** (60 paths, 8,790 lines, 7,140 read, of which 7,140 fork-own; 0 patch and config lines; reach n/a 60): areas `tooling-and-guards`; globs `tools/{vm-*,vm-walks/**,frame-diff,time-to-play,emulator-exit-test,es-launch-memory,signin-memory,png-blackout,qa-accounts,ra-*,raofflineproxy-*,device-act,es-syntax-check,es-untranslated,font-stems}`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the GENERIC_X64 device (`device-generic-x64-and-kernel`)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T13. cloud-sync-and-saves: the cloud test harness

- **id**: `cloud-harness`; **kind**: read; **lens**: brittleness
- **why here**: `tools/cloud-round-trip` (7,808 lines) and the backends that prove the cloud slices; a harness that agrees with itself is blindspot 31; read before the code it proves under D-WORKFLOW-186, the maintainer's weight on the build process ahead of any device target
- **paths** (9 paths, 10,165 lines, 10,165 read, of which 10,165 fork-own; 0 patch and config lines; reach n/a 9): areas `cloud-sync-and-saves`; globs `tools/**`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the cloud slices (`cloud-sync-core`, `cloud-setup-content`)
- **closing evidence**: audit folder, lint PASS, each guard's positive recorded, punch list through Phase 7

### T14. tooling-and-guards: the last-good, settings and state tests

- **id**: `tooling-state-tests`; **kind**: read; **lens**: brittleness
- **why here**: the `pixelelated-*`/`rasteratops-*` test family, the settings, wait-lock and upgrade tests, and their fixtures; read before the code it proves under D-WORKFLOW-186, the maintainer's weight on the build process ahead of any device target
- **paths** (32 paths, 6,911 lines, 6,807 read, of which 6,807 fork-own; 0 patch and config lines; reach n/a 32): areas `tooling-and-guards`; globs `tools/{settings-modes-test,melonds-upgrade-test,wait-lock-test,pixelelated-*,rasteratops-*,build-identity-test,rocknix-info-test,usb-gadget-test,nova-led-test,retroarch-wrapper-test}`, `tools/test-fixtures/**`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the OS scripts and cloud slices they prove
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T15. tooling-and-guards: the last-good scripts test

- **id**: `tooling-last-good-test`; **kind**: read; **lens**: brittleness
- **why here**: one file of 14,238 lines that proves the scripts under the image's busybox (blindspot 34). An explicit exception to plan § 5, which bounds a slice by about 8,000 to 12,000 lines, one package group or one device: a test split across two sessions loses its fixtures' context. The brief invites the file's split as a Q7 finding; read before the code it proves under D-WORKFLOW-186, the maintainer's weight on the build process ahead of any device target
- **paths** (1 paths, 14,238 lines, 14,238 read, of which 14,238 fork-own; 0 patch and config lines; reach n/a 1): areas `tooling-and-guards`; globs `tools/last-good-scripts-test`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the OS scripts and cloud slices they prove
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T16. cloud-sync-and-saves: cloud sync: the sync, backup, restore and capture core

- **id**: `cloud-sync-core`; **kind**: read; **lens**: security, brittleness, new functionality
- **why here**: the state model players' saves depend on: the highest brittleness of the product areas (19 blindspot entries, 47 closed bugs, 451 commits since June) and +28,279 lines since the base; its closing evidence runs `tools/cloud-round-trip`, so the brief asks the executor to read the assertions it relies on for invariants rather than current behaviour (blindspot 31), ahead of `cloud-harness`
- **paths** (14 paths, 8,316 lines, 7,827 read, of which 7,827 fork-own; 0 patch and config lines; reach shipped 14): areas `cloud-sync-and-saves`; globs `projects/ROCKNIX/packages/network/rclone/**`, `!projects/ROCKNIX/packages/network/rclone/sources/cloud_{oauth,setup,remote,connections.py,content_backup,content_restore,content_transfer,scan,folder_validate,device_id,log_scrub}`
- **read before**: none
- **depth**: Extended -- the cloud sync and state preservation (plan § 6c)
- **interacting subsystems** (read-only context): the ES cloud cards and transfer page (`es-cloud-pages`); `backuptool` and the setup scripts (`cloud-setup-content`); the game-end hook and autostart (`sysutils/autostart` in `os-system-services`, `rclone/autostart` here); the save layout RetroArch and the standalone emulators write (`emulators-libretro`, `emulators-standalone`); `rclone-cloud-sync.md`'s invariants
- **closing evidence**: audit folder, lint PASS with the renovation face, every behaviour claim proven on the VM (`tools/cloud-round-trip`, `tools/vm-qa`), punch list through Phase 7, `reviewed-at` and `fixed-at` set

### T17. cloud-sync-and-saves: cloud sync: setup, sign-in, connections, content and settings backups

- **id**: `cloud-setup-content`; **kind**: read; **lens**: security
- **why here**: handles credentials (`rclone.conf`, OAuth tokens, the sign-in window) and the only content action that deletes (`--match`, D-CLOUD-023)
- **paths** (14 paths, 11,180 lines, 11,180 read, of which 11,180 fork-own; 0 patch and config lines; reach shipped 14): areas `cloud-sync-and-saves`; globs `projects/ROCKNIX/packages/network/rclone/sources/cloud_{oauth,setup,remote,connections.py,content_backup,content_restore,content_transfer,scan,folder_validate,device_id,log_scrub}`, `projects/ROCKNIX/packages/network/cloud-signin-window/**`, `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool`
- **read before**: none
- **depth**: Extended -- security and state preservation (plan § 6c)
- **interacting subsystems** (read-only context): the sync core (`cloud-sync-core`); `post-update` and `chksysconfig`, whose state `backuptool` archives (`os-launch-control-state`); `ApiSystem` and `Settings` (`es-state-and-bridge`); the ES setup wizard and transfer page; webkitgtk (#576)
- **closing evidence**: audit folder, lint PASS, VM proofs, punch list through Phase 7, `reviewed-at` and `fixed-at` set

### T18. interface: EmulationStation's cloud pages, cards and text, with their unit tests

- **id**: `es-cloud-pages`; **kind**: read; **lens**: brittleness, new functionality
- **why here**: 36 interface files name the cloud scripts (cross-reference.md); the cards, the transfer page and the text rules are the fork's; the unit tests ride here because most test `CloudText`; a test of a T2 or achievements subject is read with it as context
- **paths** (30 paths, 11,193 lines, 11,116 read, of which 11,116 fork-own; 0 patch and config lines; reach shipped 30): areas `interface`; globs `es:es-app/src/{CloudText,ThreadedCloudSync,CloudTransferJob}.*`, `es:es-app/src/guis/GuiCloud*`, `es:es-app/tests/**`
- **read before**: none
- **depth**: Extended -- `ThreadedCloudSync` and `CloudTransferJob` are on the state list: the cloud sync's ES half (plan § 6c)
- **interacting subsystems** (read-only context): the cloud scripts (`cloud-sync-core`, `cloud-setup-content`); `FileData::launchGame`, which asks over a running sync (`es-launch-path`); `AtomicFileUtil` and `Settings` (`es-state-and-bridge`); `es-player-text.md` and `es-ui-style-guide.md`
- **closing evidence**: audit folder, lint PASS, `es-unit-tests` and `tools/es-syntax-check`, frames for any visible change, punch list through Phase 7

### T19. offline-achievements: the offline achievements proxy

- **id**: `offline-achievements`; **kind**: read; **lens**: security, new functionality
- **why here**: a network listener holding the player's account token, all fork-own (+3,666), and the cheapest product area to finish; its 18 fork-written patches to the upstream proxy are read here, not in the patch tables (pass 6)
- **paths** (27 paths, 5,369 lines, 3,656 read, of which 3,656 fork-own; 1,703 patch and config lines; reach shipped 27): areas `offline-achievements`; globs `(all)` **plus** areas `patches-and-configs`; globs `projects/ROCKNIX/packages/network/raofflineproxy*/**`
- **read before**: none
- **depth**: Extended -- a network listener and an account credential (plan § 6c)
- **interacting subsystems** (read-only context): `ProxyCards` and the RetroAchievements pages (ES); RetroArch's `rcheevos` path; #585's upstream queue
- **closing evidence**: audit folder, lint PASS, `tools/ra-offline-test` and the proxy's suites on the VM, punch list through Phase 7, `reviewed-at` and `fixed-at` set

### T20. interface: EmulationStation's RetroAchievements and offline pages

- **id**: `es-achievements-pages`; **kind**: read; **lens**: security, new functionality
- **why here**: the account pages and the offline scan, which drive the proxy (16 interface files name it); with the fork-touched files of ES's vendored libcheevos (rcheevos and libretro-common), read as a diff against their imported version, since a local delta in the protocol library is invisible to a version row
- **paths** (25 paths, 7,485 lines, 7,427 read, of which 7,416 fork-own; 0 patch and config lines; reach shipped 25): areas `interface`; globs `es:es-app/src/{RetroAchievements,OfflineAchievements,ThreadedHasher,OfflineScanJob}.*`, `es:es-app/src/guis/Gui{RetroAchievements,OfflineScan,GameAchievements}*` **plus** areas `interface`; globs `es:external/libcheevos/**`
- **read before**: none
- **depth**: Extended -- `RetroAchievements.*` is on the security list: the account's credentials (plan § 6c)
- **interacting subsystems** (read-only context): the proxy (`offline-achievements`) and its own rcheevos; `ProxyCards` (`es-launch-path`); `ApiSystem` (`es-state-and-bridge`)
- **closing evidence**: audit folder, lint PASS, `tools/ra-ui-test`, punch list through Phase 7

### T21. interface: EmulationStation's state primitives and its bridge to the OS

- **id**: `es-state-and-bridge`; **kind**: read; **lens**: security, state preservation (the preliminary review)
- **why here**: `Settings`, `SystemConf` and `AtomicFileUtil` write `es_settings.cfg`, `system.cfg` and the last-good copies; `HttpReq` is the network client; `ApiSystem` assembles the shell commands every page runs, from player-entered strings (Wi-Fi, accounts); `GuiWifi` and `ScreenScraper` carry credentials. All are on the order's security or state lists, so they are cut out of their Independent slices into one Extended read (claude, gemini, gpt)
- **paths** (14 paths, 9,249 lines, 9,249 read, of which 9,249 fork-own; 0 patch and config lines; reach shipped 14): areas `interface`; globs `es:es-app/src/ApiSystem.*`, `es:es-app/src/guis/GuiWifi.*`, `es:es-app/src/scrapers/ScreenScraper.*`, `es:es-core/src/{Settings,SystemConf,HttpReq}.*`, `es:es-core/src/utils/AtomicFileUtil.*`
- **read before**: none
- **depth**: Extended -- security and state preservation (plan § 6c)
- **interacting subsystems** (read-only context): the OS scripts `ApiSystem` calls (`os-launch-control-state`, `os-system-services`, `cloud-setup-content`); `setsettings.sh` and `get_setting`, the other end of `system.cfg`; `backuptool`'s settings archives (`cloud-setup-content`); the last-good tests (`tooling-last-good-test`); `es-code-traps.md` (the pooled connection)
- **closing evidence**: audit folder `docs/audits/<date>-epic-m6-es-state-and-bridge/` with `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `tools/lint-audit-artifacts` PASS with the renovation face, the punch-list issue resolved through Phase 7, `reviewed-at` and `fixed-at` set

### T22. os-scripts-and-launch: the OS's system services and platform quirks

- **id**: `os-system-services`; **kind**: read; **lens**: security, brittleness
- **why here**: busybox's configuration, the systemd units and the per-platform quirks run as root on every device; the inventory reads a whole package as reached, so `system-utils`' per-device sources (`sources/devices/` for AMD64, GENERIC_X64, RK3399, RK3566 and S922X, `sources/autostart/AMD64`) read `shipped` although `package.mk` installs only `${DEVICE}`'s: the slice first derives which the shipped pair (H700, SM8550, which have none) and the VM install, as T29 does for the quirks, reads those line by line, and records the rest as unshipped rows (the coordinator's read of the third version)
- **paths** (422 paths, 16,604 lines, 10,898 read, of which 3,002 fork-own; 0 patch and config lines; reach shipped 422): areas `os-scripts-and-launch`; globs `projects/ROCKNIX/packages/sysutils/**`, `projects/ROCKNIX/packages/hardware/**`, `!projects/ROCKNIX/packages/hardware/quirks/devices/**`
- **read before**: none
- **depth**: Extended -- the systemd units and services run as root on every device (security lens; plan § 6c)
- **interacting subsystems** (read-only context): `os-launch-control-state`'s scripts; `ApiSystem` (`es-state-and-bridge`); the devices' options; the game-end and autostart hooks (`sysutils/autostart`, read here)
- **closing evidence**: audit folder, lint PASS, VM proofs for boot behaviour, punch list through Phase 7

### T23. generic-packages: the generic packages no image builds

- **id**: `packages-dead-ends`; **kind**: table; **lens**: reachability
- **why here**: the largest dead set: 95,398 lines no plan reaches; 620 of the inventory's unreached rows are copies shadowed by a ROCKNIX override (`shadowed_by` names it), so the package is live and only the copy may go (`engineering-practices.md` § Before deleting a duplicate). Rows are generated from `inventory.json`; the session re-derives reachability for a sample with `tools/viewplan` (two commands for one quantity) and decides the removals. Patches inside a removed directory belong to `patches-dead`'s table, which records them as removed by this slice's stream (one remediation owner)
- **paths** (1,604 paths, 95,892 lines, -- read, of which -- fork-own; 0 patch and config lines; reach unreached 1565, unshipped 39): areas `generic-packages`; globs `(all)`; reach `unreached`, `unshipped`
- **read before**: none
- **depth**: Local -- a reachability table: the counts are the check (plan § 6c)
- **interacting subsystems** (read-only context): the ROCKNIX overrides (`shadowed_by`); `patches-dead` (the patches of what this slice removes); `tools/renovation-inventory` (read in `tooling-guards` first)
- **closing evidence**: one row per unit with its reachability command and output, each removal with `Already written:` and `engineering-practices.md` § Before deleting a duplicate; audit folder, lint PASS, `reviewed-at` set

### T24. emulators-and-cores: emulator recipes and files no shipped image builds, and the rest of the area

- **id**: `emulators-dead-ends`; **kind**: table; **lens**: reachability
- **why here**: the generic `packages/emulation` recipes and the cores only unshipped devices build
- **paths** (86 paths, 2,399 lines, -- read, of which -- fork-own; 0 patch and config lines; reach unreached 84, unshipped 2): areas `emulators-and-cores`; globs `(all)`; the rest of these areas
- **read before**: none
- **depth**: Local -- a reachability table
- **interacting subsystems** (read-only context): the emulator slices (`emulators-standalone`, `emulators-libretro`)
- **closing evidence**: one row per unit; audit folder, lint PASS

### T25. devices: the devices the fork does not ship and the other projects

- **id**: `devices-unshipped`; **kind**: table; **lens**: reachability
- **why here**: the devices the fork neither ships nor tests on (D-WORKFLOW-185: it ships H700 and SM8550, GENERIC_X64 is the test image; RK3566 and RK3326, the recorded first widening, are rows here until the maintainer opens either as a device build) and the nine LibreELEC-era projects no Makefile target builds
- **paths** (397 paths, 49,555 lines, -- read, of which -- fork-own; 0 patch and config lines; reach unreached 216, unshipped 181): areas `devices`; globs `projects/**`, `packages/**`, `!projects/ROCKNIX/devices/{H700,SM8550,GENERIC_X64}/**`; reach `unreached`, `unshipped`
- **read before**: none
- **depth**: Local -- a reachability table
- **interacting subsystems** (read-only context): the shipped device slices
- **closing evidence**: one row per device or project; audit folder, lint PASS

### T26. interface: EmulationStation's main menu (GuiMenu)

- **id**: `es-guimenu`; **kind**: read; **lens**: new functionality, brittleness
- **why here**: one file, 11,883 lines, the largest fork-own unit, where every fork page is reached from
- **paths** (2 paths, 11,883 lines, 11,883 read, of which 11,883 fork-own; 0 patch and config lines; reach shipped 2): areas `interface`; globs `es:es-app/src/guis/GuiMenu.*`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): every page it opens; `setsettings.sh` (`os-launch-control-state`), which reads what GuiMenu writes; `SystemConf` (`es-state-and-bridge`); `docs/es-menu-map.md` (D-UI-039)
- **closing evidence**: audit folder, lint PASS, `tools/es-menu-map-check`, punch list through Phase 7

### T27. devices: the H700 device (RG35XX SP, RG SP)

- **id**: `device-h700`; **kind**: currency; **lens**: cost against value
- **why here**: the maintainer's test handhelds; options, device packages (u-boot DDR3/DDR4, the suspend stub), device trees and kernel configuration; its fork-written kernel configuration (8,129 lines) is read here as a diff against its base (plan § 2)
- **paths** (28 paths, 12,901 lines, 327 read, of which 0 fork-own; 8,129 patch and config lines; reach shipped 28): areas `devices`; globs `projects/ROCKNIX/devices/H700/**` **plus** areas `patches-and-configs`; globs `projects/ROCKNIX/devices/H700/linux/*.conf`
- **read before**: none
- **depth**: Independent -- an ordinary device slice
- **interacting subsystems** (read-only context): the H700 quirks (`os-device-quirks`); the kernel patches (patches slices); `docs/device-flashing-runbook.md`; the kernel recipe and project boot files (`device-generic-x64-and-kernel`); the fork-written H700 kernel patch (`patches-shipped-kernel`)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T28. devices: the SM8550 device (Retroid Pocket Nova)

- **id**: `device-sm8550`; **kind**: currency; **lens**: cost against value
- **why here**: a shipped test device
- **paths** (29 paths, 28,053 lines, 118 read, of which 0 fork-own; 0 patch and config lines; reach shipped 29): areas `devices`; globs `projects/ROCKNIX/devices/SM8550/**`
- **read before**: none
- **depth**: Independent -- an ordinary device slice
- **interacting subsystems** (read-only context): its quirks and kernel patches; the kernel recipe and project boot files (`device-generic-x64-and-kernel`)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T29. os-scripts-and-launch: the per-handheld quirks

- **id**: `os-device-quirks`; **kind**: currency; **lens**: brittleness
- **why here**: 333 files over 88 handheld models, all installed with the quirks package: the slice first derives which model directories the shipped pair (H700, SM8550) and the VM select at run time (D-WORKFLOW-185) (the board/DMI match the quirks scripts use), reads those and the fork-touched files line by line, and checks the rest for currency
- **paths** (333 paths, 10,175 lines, 9,327 read, of which 389 fork-own; 0 patch and config lines; reach shipped 333): areas `os-scripts-and-launch`; globs `projects/ROCKNIX/packages/hardware/quirks/devices/**`
- **read before**: none
- **depth**: Independent -- 9,327 code lines, mostly upstream-carried; plan § 6c's ordinary code slice (gpt)
- **interacting subsystems** (read-only context): the device trees and options (devices)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T30. emulators-and-cores: the standalone emulators

- **id**: `emulators-standalone`; **kind**: currency; **lens**: launch path, brittleness
- **why here**: the start scripts and configuration of every standalone emulator the image ships
- **paths** (543 paths, 157,365 lines, 10,695 read, of which 3,104 fork-own; 0 patch and config lines; reach shipped 543): areas `emulators-and-cores`; globs `projects/ROCKNIX/packages/emulators/standalone/**`; reach `shipped`, `test`, `n/a`
- **read before**: none
- **depth**: Extended -- the start scripts are on the launch path (plan § 6c)
- **interacting subsystems** (read-only context): `runemu.sh` (`os-launch-control-state`); the quirks; the save layout cloud sync moves (`cloud-sync-core`); `tools/emulator-exit-test`
- **closing evidence**: audit folder, lint PASS, `tools/emulator-exit-test`, punch list through Phase 7

### T31. interface: EmulationStation's other pages

- **id**: `es-pages`; **kind**: currency; **lens**: new functionality
- **why here**: the remaining pages under `guis/`: the fork-touched ones read line by line, the upstream ones checked against `rocknix/master`
- **paths** (76 paths, 15,537 lines, 15,537 read, of which 4,230 fork-own; 0 patch and config lines; reach shipped 76): areas `interface`; globs `es:es-app/src/guis/**`, `!es:es-app/src/guis/GuiMenu.*`, `!es:es-app/src/guis/GuiCloud*`, `!es:es-app/src/guis/Gui{RetroAchievements,OfflineScan,GameAchievements}*`, `!es:es-app/src/guis/GuiWifi.*`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): GuiMenu (`es-guimenu`); the es-core components
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T32. interface: EmulationStation's game list views, scrapers and services

- **id**: `es-app-views-scrapers`; **kind**: currency; **lens**: cost against value
- **why here**: `views/` (8,155 lines, ViewController and the game list containers the fork changed) and the scrapers (ScreenScraper's credential wiring is read in `es-state-and-bridge`)
- **paths** (42 paths, 17,311 lines, 17,311 read, of which 4,005 fork-own; 0 patch and config lines; reach shipped 42): areas `interface`; globs `es:es-app/src/{views,scrapers,services}/**`, `!es:es-app/src/views/ViewController.*`, `!es:es-app/src/scrapers/ScreenScraper.*`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the scrapers' developer credentials (`device-builds.md` § Build credentials); the launch path (game list to launch)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T33. interface: EmulationStation's system layer: ApiSystem, game lists, collections, metadata

- **id**: `es-app-system`; **kind**: currency; **lens**: cost against value
- **why here**: the rest of `es-app`: `ApiSystem.cpp` (3,519 fork-own lines) is the bridge to the OS scripts; game lists, collections and metadata hold the player's library
- **paths** (77 paths, 16,276 lines, 16,210 read, of which 4,522 fork-own; 0 patch and config lines; reach shipped 77): areas `interface`; globs `es:es-app/**`; the rest of these areas
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the OS scripts `ApiSystem` calls (`os-launch-control-state`, os-system-services); `gamelist.xml` (game content, D-CLOUD-049)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T34. interface: EmulationStation's core components

- **id**: `es-core-components`; **kind**: currency; **lens**: cost against value
- **why here**: `es-core/src/components` (21,984 lines, 9,541 fork-own): the rows, grids, menus and cards every page is built from
- **paths** (80 paths, 21,984 lines, 21,984 read, of which 9,541 fork-own; 0 patch and config lines; reach shipped 80): areas `interface`; globs `es:es-core/src/components/**`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): every page; `es-code-traps.md`
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T35. interface: EmulationStation's window, input, settings and the rest of es-core

- **id**: `es-core-window-input`; **kind**: currency; **lens**: cost against value
- **why here**: `Window.cpp` (one floating surface at a time, D-UI-093), `InputManager`, `Settings`, `SystemConf`, `HttpReq` (the pooled-connection trap), `GunManager` and es-core's own pages
- **paths** (96 paths, 22,575 lines, 22,575 read, of which 6,759 fork-own; 0 patch and config lines; reach shipped 96): areas `interface`; globs `es:es-core/**`; the rest of these areas
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): every page; `es-code-traps.md` (the pooled connection, `exists` caching, fonts)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T36. interface: EmulationStation's utilities, resources and renderers

- **id**: `es-core-utils-resources`; **kind**: currency; **lens**: cost against value
- **why here**: `utils` (40,926 lines; `StringUtil`, `Platform`, `AtomicFileUtil`, the fork's last-good writes), `resources` (fonts, textures) and `renderers`
- **paths** (58 paths, 50,840 lines, 50,840 read, of which 6,212 fork-own; 0 patch and config lines; reach shipped 58): areas `interface`; globs `es:es-core/src/{utils,resources,renderers}/**`, `!es:es-core/src/utils/AtomicFileUtil.*`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): every page; `es-code-traps.md`
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

### T37. interface: the EmulationStation recipe and themes in the distribution

- **id**: `es-recipe`; **kind**: read; **lens**: package currency
- **why here**: the pin, the build steps and the themes the image installs
- **paths** (15 paths, 4,561 lines, 327 read, of which 190 fork-own; 0 patch and config lines; reach shipped 15): areas `interface`; globs `projects/ROCKNIX/packages/ui/**`
- **read before**: none
- **depth**: Independent -- a small recipe read; plan § 6c names no Local exception for code (gpt)
- **interacting subsystems** (read-only context): the ES tree (every `es-*` slice)
- **closing evidence**: audit folder, lint PASS, `tools/pkgcheck`

### T38. doctrine: the skills, agents and settings

- **id**: `doctrine-skills`; **kind**: prose; **lens**: cost against value
- **why here**: the skills (code-auditor, futro, mini-retro, council) every slice's procedure runs on, and the agent definitions; read after the rules; at 12,734 lines of prose it sits just above plan § 5's guide, kept whole because the skills cross-reference each other
- **paths** (52 paths, 12,734 lines, 0 read, of which 0 fork-own; 0 patch and config lines; reach n/a 52): areas `doctrine`; globs `.claude/**`, `!.claude/rules/**`
- **read before**: none
- **depth**: Local -- a doctrine read (plan § 6c)
- **interacting subsystems** (read-only context): every area (25 to 29 rules govern each, cross-reference.md)
- **closing evidence**: audit folder `docs/audits/<date>-epic-m6-doctrine-skills/` with `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `tools/lint-audit-artifacts` PASS with the renovation face, the punch-list issue resolved through Phase 7, `reviewed-at` and `fixed-at` set

### T39. doctrine: the reference documents

- **id**: `doctrine-reference`; **kind**: table; **lens**: cost against value
- **why here**: the rest of the doctrine area: README, TRADEMARK, LICENSE and `licenses/`, `documentation/`, `plans/`, and the reference docs under `docs/` (upstream, releases, the rename, the menu map): tabled for what misleads a reader today
- **paths** (253 paths, 38,183 lines, -- read, of which -- fork-own; 0 patch and config lines; reach n/a 253): areas `doctrine`; globs `(all)`; the rest of these areas
- **read before**: none
- **depth**: Local -- a table
- **interacting subsystems** (read-only context): every area (25 to 29 rules govern each, cross-reference.md)
- **closing evidence**: audit folder `docs/audits/<date>-epic-m6-doctrine-reference/` with `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `tools/lint-audit-artifacts` PASS with the renovation face, the punch-list issue resolved through Phase 7, `reviewed-at` and `fixed-at` set

### T40. patches-and-configs: patches and kernel configurations no plan applies

- **id**: `patches-dead`; **kind**: table; **lens**: reachability
- **why here**: 778 paths, 317,908 lines: the 277 generic kernel patches the ROCKNIX `linux` override never applies, `vitaquake2-lr`'s and EmulationStation's `patches/x86_64` (which `PATCH_ARCH=x86` never selects), the other projects' patches. Rows are generated from `inventory.json` and the patch headers (`From:`, `Subject:`); the session decides origin and removal. Kept with the other patch tables (gemini): its removals shrink only those tables; claude would have run it early (recorded in `order.md`)
- **paths** (778 paths, 317,908 lines, -- read, of which -- fork-own; 317,908 patch and config lines; reach unreached 778): areas `patches-and-configs`; globs `(all)`; reach `unreached`
- **read before**: none
- **depth**: Local -- a provenance table
- **interacting subsystems** (read-only context): the packages they would patch
- **closing evidence**: one row per patch with origin, upstream status and reason, the count equal to the slice's paths; audit folder, lint PASS

### T41. patches-and-configs: kernel patches and configurations the shipped and test images apply

- **id**: `patches-shipped-kernel`; **kind**: table; **lens**: package currency
- **why here**: one provenance row per kernel patch and configuration a shipped image or the test image applies (#339 criterion 2), split from the other shipped patches so each table is one session; the fork-written H700 kernel patch is read line by line here (gpt would move it to `device-h700`; it stays with the kernel's provenance, named as that slice's interacting subsystem)
- **paths** (107 paths, 40,474 lines, -- read, of which -- fork-own; 40,474 patch and config lines; reach shipped 103, test 4): areas `patches-and-configs`; globs `projects/ROCKNIX/devices/**`, `projects/ROCKNIX/packages/linux*/**`, `packages/linux*/**`, `!projects/ROCKNIX/devices/{H700,GENERIC_X64}/linux/*.conf`; reach `shipped`, `test`
- **read before**: none
- **depth**: Local -- a provenance table
- **interacting subsystems** (read-only context): the shipped device slices and the kernel recipe (`device-generic-x64-and-kernel`)
- **closing evidence**: one row per patch; audit folder, lint PASS

### T42. patches-and-configs: the other patches the shipped and test images apply

- **id**: `patches-shipped`; **kind**: table; **lens**: package currency
- **why here**: one provenance row per patch and kernel configuration a shipped image or the test image applies (#339 criterion 2): origin, merged upstream or not, the reason we carry it, the version made against, whether it still applies; the remaining fork-written patches (mesa, SDL2, shaderc, webkitgtk, woff2, zerotier-one, fex-emu, the theme) are read line by line in the table
- **paths** (384 paths, 71,387 lines, -- read, of which -- fork-own; 71,387 patch and config lines; reach shipped 379, test 5): areas `patches-and-configs`; globs `(all)`; the rest of these areas
- **read before**: none
- **depth**: Local -- a provenance table
- **interacting subsystems** (read-only context): the packages they patch (cross-reference.md: devices 1,007, generic 505, emulators 174)
- **closing evidence**: one row per patch; audit folder, lint PASS

### T43. patches-and-configs: patches only unshipped devices apply

- **id**: `patches-unshipped`; **kind**: table; **lens**: reachability
- **why here**: the patches and kernel configurations only targets the fork neither ships nor tests on apply (D-WORKFLOW-185), RK3566's and RK3326's among them
- **paths** (432 paths, 328,516 lines, -- read, of which -- fork-own; 328,516 patch and config lines; reach unshipped 432): areas `patches-and-configs`; globs `(all)`; reach `unshipped`, `n/a`
- **read before**: none
- **depth**: Local -- a provenance table
- **interacting subsystems** (read-only context): the unshipped devices (`devices-unshipped`)
- **closing evidence**: one row per patch; audit folder, lint PASS

### T44. interface: EmulationStation's vendored libraries, translations and build files

- **id**: `es-vendored-and-data`; **kind**: table; **lens**: reachability, package currency
- **why here**: `external/` (libretro-common, rcheevos, doctest, nanosvg, id3v2lib) by provenance and version; the translations and resources by coverage; its table separates fork-added libraries (doctest, 7,134 lines, imported unchanged) from fork-modified ones (libcheevos's fork-touched files, read in `es-achievements-pages`), by comparison with the imported version
- **paths** (594 paths, 374,547 lines, -- read, of which -- fork-own; 0 patch and config lines; reach shipped 594): areas `interface`; globs `es:**`, `!es:es-app/**`, `!es:es-core/**`; the rest of these areas
- **read before**: none
- **depth**: Local -- a provenance table
- **interacting subsystems** (read-only context): the proxy's own rcheevos (`offline-achievements`)
- **closing evidence**: one row per vendored library with its version and upstream; audit folder, lint PASS

### T45. tooling-and-guards: the council toolchain and runner

- **id**: `tooling-council`; **kind**: table; **lens**: package currency
- **why here**: scaffold's export, committed byte for byte (D-WORKFLOW-088): by provenance and version only, refreshed by copying the next export (plan § 2)
- **paths** (52 paths, 25,848 lines, -- read, of which -- fork-own; 0 patch and config lines; reach n/a 52): areas `tooling-and-guards`; globs `scripts/**`, `seed/**`, `verifier-pins.json`, `council-seat-efforts.json`, `tools/council/**`
- **read before**: none
- **depth**: Local -- a provenance table
- **interacting subsystems** (read-only context): the preliminary reviews and audits that call it
- **closing evidence**: the export's version and digest recorded; audit folder, lint PASS

### T46. records: the records

- **id**: `records`; **kind**: table; **lens**: cost against value
- **why here**: reviewed only where a record misleads a reader today (plan § 5): the records the doctrine, the READMEs and the indexes link to are read; the rest are tabled by folder. Last, because the slices before it write records. Its read count is an artefact (QA logs and dumps classify as code) and is not a session size
- **paths** (126,149 paths, 22,984,459 lines, -- read, of which -- fork-own; 0 patch and config lines; reach n/a 126149): areas `records`; globs `(all)`
- **read before**: none
- **depth**: Local -- a table
- **interacting subsystems** (read-only context): --
- **closing evidence**: one row per misleading record found, with its correction; audit folder, lint PASS

### The security, state-preservation and launch-path files

`tools/renovation-drift` reads these globs from `slices.json` (`sensitive`): a closed slice whose drift touches one re-opens at its depth, whatever its size (plan § 8).
- **security** (51 paths): `projects/ROCKNIX/packages/network/rclone/sources/cloud_{oauth,setup,remote,connections.py,log_scrub}`, `projects/ROCKNIX/packages/network/cloud-signin-window/**`, `projects/ROCKNIX/packages/network/raofflineproxy/**`, `projects/ROCKNIX/packages/rocknix/sources/scripts/{setrootpass,wifictl,usbgadget,rocknix-evidence}`, `scripts/get_env`, `.githooks/**`, `es:es-app/src/guis/GuiWifi.*`, `es:es-app/src/RetroAchievements.*`, `es:es-core/src/HttpReq.*`, `es:es-app/src/scrapers/ScreenScraper.*`
- **state** (44 paths): `projects/ROCKNIX/packages/network/rclone/sources/**`, `projects/ROCKNIX/packages/rocknix/sources/scripts/{backuptool,chksysconfig,factoryreset,installtointernal,automount}`, `projects/ROCKNIX/packages/rocknix/sources/post-update`, `projects/ROCKNIX/packages/rocknix/sources/scripts/setsettings.sh`, `es:es-core/src/{Settings,SystemConf}.*`, `es:es-core/src/utils/AtomicFileUtil.*`, `es:es-app/src/{CloudTransferJob,ThreadedCloudSync,SaveStateBookkeeper,SaveStateRepository}.*`
- **launch-path** (239 paths): `projects/ROCKNIX/packages/rocknix/sources/scripts/{runemu.sh,setsettings.sh,run}`, `projects/ROCKNIX/packages/emulators/libretro/retroarch/**`, `es:es-app/src/{FileData,SystemData,LaunchCommand,ProxyCards}.*`, `es:es-app/src/main.cpp`, `es:es-app/src/views/ViewController.*`, `projects/ROCKNIX/packages/virtual/emulators/**`, `projects/ROCKNIX/packages/emulators/standalone/*/scripts/start_*.sh`

<!-- renovation-inventory --order: end -->

## The preliminary review of this order

Status: **reviewed** -- run `2026-10-22-m6-p1-order`
(`research/preliminary-reviews/2026-10-22-m6-p1-order/`), the three-seat
advisory format (`.claude/skills/council/references/review-formats.md`) on the
first version of this order (`order.md` at `d2f631e801`, with `inventory.md`,
`areas.json` and the plan). Seats: claude (`anthropic/claude-fable-5.1`,
xhigh), gemini (`google/gemini-3.8-flash`, high) and gpt
(`openai/gpt-6-astra`, max). Each was verified from its provenance before the
next (`verification.md`). All three said **ready with named changes**.
Advisory: no vote, no approval. The seats read four of the survey's seven
inputs: `assessment.md`, `cross-reference.md`, `slices.json` and the tracking
file were not embedded, so the lens scores they rest on were taken on the
order's word.

Each material objection, and its answer, in the second version's slice
numbers (the renumbering table above maps them). Where an answer names the
gates, read the reading order: D-WORKFLOW-187 retired the release gates in
the fourth version and moved no slice. The full synthesis is
`research/preliminary-reviews/2026-10-22-m6-p1-order/synthesis.md`.

| # | Objection (seats) | Answer |
| --- | --- | --- |
| 1 | Files on the order's own security and state lists sat in Independent slices; drift "at its depth" kept that (all three) | **Accepted.** The new `es-state-and-bridge` (T11, Extended) takes `ApiSystem`, `GuiWifi`, `ScreenScraper`, `Settings`, `SystemConf`, `HttpReq` and `AtomicFileUtil`. `es-cloud-pages`, `es-achievements-pages`, `os-system-services`, `build-engine` (`get_env`), `emulators-standalone` (start scripts, now on the launch-path list) and `tooling-guards` (`.githooks`) are Extended. A sensitive file re-opens at Extended |
| 2 | RetroArch's "read before #336" lived only in prose (all three) | **Accepted.** It is T3, with "before #336 Step 1" as its recorded prerequisite, beside the gates |
| 3 | The launch path's entry and command table were outside T1, T2 and T3 (claude) | **Accepted, checked first.** `ViewController.cpp:483` calls `launchGame`, so it joins T2. `virtual/emulators`' `mk_es_systems` writes `es_systems.cfg`, so it joins T3. Both are on the launch-path list, with the 41 standalone `start_*.sh` |
| 4 | Doctrine and guards too late (gemini, claude) | **Accepted.** The binding doctrine is T4 and the guards T5 |
| 5 | Dead-end tables: early (claude) or late (gemini) | **Both in part.** The four package and device dead-end tables are T14 to T17, after the security cluster; they are Local and may run beside any read slice. The patches no plan applies (T41) sit with the patch tables, whose rows are all they shrink (gemini). Claude's wish to run them earlier stands as a noted alternative |
| 6 | Cloud and proxy pairs interleaved (claude, gpt) | **Accepted.** T6, T7, T8 are cloud; T9, T10 the proxy |
| 7 | Seams missing or one-sided: ApiSystem, ES's state primitives, T1's services and quirks, T8 and the launch consumer (all three) | **Accepted.** `es-state-and-bridge` holds the ES side. Every slice's interacting subsystems now name both ends by slice id, and the shared state (`system.cfg`, `es_settings.cfg`, `es_systems.cfg`, the sync cards) |
| 8 | Read counts hid patch work, the doctrine's prose and table rows (all three) | **Accepted.** The block shows patch and config lines apart. The doctrine is a *prose* kind sized by lines, split in three (T4, T33, T39). Tables show rows and state how they are generated |
| 9 | ES's vendored libcheevos carries fork-touched files a version row cannot see (claude, gpt) | **Accepted.** Its fork-own files are read in T10 as a diff against the imported version. T45's table separates fork-added (doctest) from fork-modified libraries |
| 10 | Core toolchain packages (`glibc`, `virtual/libc`, `openssl`, `squashfs-tools`, ...) labelled unreached (gemini) | **Checked, not a mislabel; a presentation fix accepted.** Each is built from its ROCKNIX override (in every plan). What is unreached is the generic copy the override shadows, which `get_pkg_directory` never resolves. `quilt`, `gcc-aarch64` and `binutils-aarch64` appear in no plan and nothing references them. The inventory now names the override on each shadowed row (`shadowed_by`, 620 rows), and T14 must not remove a live package |
| 11 | ES's and `vitaquake2-lr`'s `patches/x86_64` may be mislabelled (claude) | **Checked, correct.** `scripts/unpack` sets `PATCH_ARCH="x86"` on x86_64, and neither recipe names `x86_64` in `PKG_PATCH_DIRS`, so neither directory ever applies. These are leads for T41, not survey errors |
| 12 | The shipped-device set (`device-builds.md`: RK3566, H700, RK3326, SM8550, GENERIC_X64) differs from plan § 5's list, which adds SM8250, S922X and SM6115 (claude) | **Put to the maintainer at pass 7.** The brief (§ 2) defines shipped by `device-builds.md`. If the three are shipped, they gain device slices and their patches move from T44 to T42 and T43. **Answered 2026-10-23 (D-WORKFLOW-185):** H700 and SM8550 ship and GENERIC_X64 is the test image, so none of the three is shipped and RK3566 and RK3326 become rows; the third version applies it |
| 13 | Quirks per model are all "shipped" by package (claude, gemini, gpt) | **Accepted.** T23 is a currency slice at Independent depth. It first derives which model directories the shipped devices select at run time |
| 14 | Removals crossing slice ownership (a removed package's patches) (gpt) | **Accepted.** T14's removals own the patches in what they remove; T41's table records them as removed by T14's stream |
| 15 | The drift contract (two repositories, an accepted-drift checkpoint, the boundary, the denominator) (gpt) | **Accepted.** `fixed_at` names each tree; `drift_checked_at` advances after an accepted drift review; under 20 % is small and 20 % or more re-opens; the share is of lines for read slices and of rows for tables. A replaced interacting subsystem is the planner's call, recorded on the slice issue |
| 16 | `renovation-drift` and `renovation-status` owned by no slice (gpt) | **Accepted.** T5 names them |
| 17 | Text errors: T12's 12,328, T32's citation of § 5, "five phase files", the opening's posting tense (claude, gpt) | **Accepted.** Corrected |

Minor findings not taken: merging the small slices (claude; gpt advised against
it), lowering the device slices to Local (claude), and moving the H700 kernel
patch into its device slice (gpt). The last stays with the kernel's provenance
table (T42), and T20 names it.
