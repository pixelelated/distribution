# Analysis tracking: M6.P1, the survey (#641) -- 2026-10-22

The multi-pass tracking file for P1 (`docs/reviews/briefs/p1-survey.md` § 6).
Rigour: **comprehensive** (first analysis of the scope; all seven passes,
N-to-N cross-reference by area). Every count below is the output of the
command written beside it. A resumed session re-runs the command rather than
trusting the number.

## Header

| Field | Value | Command |
| --- | --- | --- |
| Executor | Opus 5.5 (`claude-opus-5-5`), high effort; Claude Code session `dbac446e-3b41-4b28-966d-0a6efe07ea2b`, Herdr pane `wN:p3` | the dispatch on #641 (no model or effort named by the maintainer; the brief's default) |
| Branch | `feature/m6-p1-survey-641`, stacked on `feature/m6-renovation-plan-346` | `git merge-base --is-ancestor origin/feature/m6-renovation-plan-346 HEAD` → true after merging the P0 tip `fac868f2fb` as `bff1ccec2a` |
| Worktree `HEAD` at survey start | `bff1ccec2a2f88596d4198335938c73daf4438df` | `git rev-parse HEAD` |
| `next` | `8ebaf8daad8eaac6331dff6fc048fb4411d7decb` | `git rev-parse next` |
| `upstream/next` | `03d71e321737a95ca7f3b8a738261dd6af790b43` | `git rev-parse upstream/next` after `git fetch upstream --no-tags` |
| Merge base `next`/`upstream/next` | `c445081a59518f37d9776e5412dd7b14910696f7` | `git merge-base next upstream/next` |
| ES pin | `16dbac5211eea7e70db7394372033be2be7df829` | `PKG_VERSION` in `projects/ROCKNIX/packages/ui/emulationstation/package.mk` |
| `rocknix/master` (ES) | `e282b05627c0d2193c19d7cc526176e047530c3d` | `git -C $ES rev-parse rocknix/master` after `git -C $ES fetch rocknix --no-tags` (moved from `cada856d8` during this fetch) |
| `batocera/master` (ES) | `b2ceb55a7e3d205a11f055b7d93c8be50cd6f9c9` | `git -C $ES rev-parse batocera/master` after `git -C $ES fetch batocera --no-tags` |
| ES merge base pin/`rocknix/master` | `cada856d86e3115fbbf0bce09dd761b0ee8fa9fd` | `git -C $ES merge-base rocknix/master $PIN` |
| ES worktree | `/home/max/Development/emulationstation-next.worktrees/m6-p1-survey`, detached at the pin | `git -C $ES worktree add --detach ...`; removed at the end with `git -C $ES worktree remove` |

`ES=/home/max/Development/emulationstation-next`.

## Counts re-derived at the start

| Quantity | Recorded (brief, `8ebaf8daad`) | Now (`bff1ccec2a`) | Delta | Command |
| --- | ---: | ---: | ---: | --- |
| tracked paths | 133,465 | 133,471 | +6 (this branch's files) | `git ls-files \| wc -l` |
| `package.mk` | 1,607 (1,040 + 567) | 1,607 (1,040 + 567) | 0 | `find packages projects -name package.mk \| wc -l`; `git ls-files 'packages/**/package.mk' 'projects/**/package.mk' \| wc -l` agrees |
| patches | 1,709 | 1,709 | 0 | `find packages projects -name '*.patch' \| wc -l`; `git ls-files` form agrees |
| fork-own (`$MB..next`) | 126,855 (125,225 `docs/`) | 126,855 (125,225) | 0 | `git diff --name-only $MB next \| wc -l` |
| fork-own (`$MB..HEAD`) | -- | 126,861 | -- | `git diff --name-only $MB HEAD \| wc -l` (the inventory's basis) |
| upstream-only | 912 | 912 | 0 | `git diff --name-only $MB upstream/next \| wc -l` |
| ES tracked at pin | 1,114 | 1,114 | 0 | `git -C $ES.worktrees/m6-p1-survey ls-files \| wc -l` |
| ES `es-app/src` + `es-core/src` | 486 | 486 | 0 | `find ... -type f \| wc -l`; `git ls-files` form agrees |
| ES fork-own | 236 | 236 | 0 | `git -C $ES diff --name-only $EMB $PIN \| wc -l` |
| ES upstream-only | -- | 2 | -- | `git -C $ES diff --name-only $EMB rocknix/master \| wc -l` |
| history, `upstream/next` | -- | 58,471 commits | -- | `git rev-list --count upstream/next` |
| history, fork side | -- | 2,871 commits | -- | `git rev-list --count $MB..next` |
| history, ES `rocknix/master` / fork side | -- | 7,477 / 724 | -- | `git -C $ES rev-list --count ...` |

No two commands for one quantity disagreed; no stop.

## Progress

- Futro: complete (`docs/futros/2026-10-22-m6-p1-survey.md`, and on #641)
- Pass 1 (Inventory): **complete** -- 134,589 rows (133,475 distribution + 1,114 ES), 12 areas, 26 plans (see § Pass 1)
- Pass 2 (Clustering): **complete** -- 12 areas with read sizes; 7 areas exceed one session and are split into 31 candidate clusters (see § Pass 2)
- Pass 3 (Assessment): **complete** -- 11 areas scored on 6 lenses from `assessment.md`; records not scored (see § Pass 3)
- Pass 4 (Cross-reference): **complete** -- 10 code areas N-to-N (90 ordered pairs, 60 with an edge), rule and patch edges, every one of the 12 areas has an edge (see § Pass 4)
- Pass 5 (Classification): **complete** -- 43 slices in `slices.json`, every one of 134,591 rows in exactly one (`--order`: unassigned 0, ambiguous 0); `order.md` rendered (see § Pass 5)
- Pass 6 (Reconciliation, then the preliminary review): reconciliation **complete** (41 fork-written vendor files moved to their code's slices, the seams named); the preliminary review next (see § Pass 6)
- Pass 7 (Action): pending -- gated on the maintainer's yes on #641

## Read first (brief § 3), what was read this session

From files, not from what loaded at session start (the instruction files load
truncated; lane-start comment on #641): the M7 stash on `next` (its opening
and running-state lines); every-session rules and `worktrees.md`,
`fork-workflow.md`, `issue-tracking.md`, `milestone-phase-naming.md`,
`learning-capture.md`, `ceremonies.md`, `decision-register.md`, `vm-first.md`,
`instruction-files.md`, `adversarial-council.md`, `engineering-practices.md`
(in context); `packaging-and-patches.md` (read from file);
`council-substrate-integrity.md` (owed before pass 6);
`docs/blindspot-register.md` (every entry's heading; 13, 51 and 64 in full);
`review-formats.md`; the multi-pass pattern outside the tree; plan § 2, § 5,
§ 6, § 6a (the whole plan was read).

## Pass 1: inventory

Generated by `tools/renovation-inventory --plans <scratch>/plans-p1` at
`61d1d016eb` (tool committed in `9966dbcd12`, unit display fixed in
`ea186f4f5f`, credential-shaped names escaped in `61d1d016eb`); plans in the pinned build image
`sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39`
(`header.plan_runner`). 3.5 s of git, 68.3 s of plans.

```
$ tools/renovation-inventory --plans <scratch>/plans-p1; echo rc=$?
paths: 133475 (git ls-files: 133475)
es-paths: 1114 (git ls-files: 1114)
patches: 1709 (find: 1709)
unassigned: 0
ambiguous: 0
escaped: 2 (rows whose path matches a credential pattern, hyphens written as \u002d)
rc=0
```

The two escaped rows are upstream kernel patch names whose `mask-...` matches
the guards' API-key pattern `sk-[A-Za-z0-9_-]{24,}` once a path is file
content (the pre-commit guard refused the first commit of the inventory);
`header.escaped_rows` names them, `json.load` returns them byte-identical,
and `grep -cE "$SECRET_PATTERNS"` over both outputs is 0.

`docs/reviews/inventory.json` is 32,526,224 bytes (945,357 gzipped; under the
futro's 50 MB stop line); `tools/forbidden-terms-check --stdin` over both
outputs: 0 hits.

**The counters were seen to fail before the zero was trusted** (brief § 5):

| Constructed failure | Command | Result |
| --- | --- | --- |
| a path in no area, pure | `tools/renovation-inventory --self-test` | `PASS distribution:y/none -> 0 area(s)`; a bare `**` refused; `self-test: PASS` |
| a path in no area, on the real tree | `--inject-path renovation-fixture/matches-no-area` | `paths: 133474 (git ls-files: 133473)`, `unassigned: 1`, rc=1 |
| a path in two areas, on the real tree | `--areas <scratch>/areas-overlap.json` (the map plus an area claiming `Makefile`) | `ambiguous: 1 ... Makefile -> build-engine, fixture-overlap`, rc=1 |
| a real gap, unplanned | the first real run | `unassigned: 1 docs/retrospective/carry-forward.md`; the directory went to `records` |

**Reachability, checked against facts independent of the tool:**

| Claim | Check | Result |
| --- | --- | --- |
| a shipped product script is reached | `cloud_backup`'s row | `shipped` by GENERIC_X64, H700, RK3326, RK3566, SM8550 aarch64/x86_64 |
| the 32-bit plans' shape | `awk '{print $1}' plan-H700-arm.txt \| sort \| uniq -c` | only `build` lines, root `arm`; the first parser kept only `:`-suffixed names and had to accept both (`install rclone`, `build arm`) |
| subdevice bootloaders | `grep u-boot plan-H700-aarch64.txt` | container plan: `u-boot-DDR3`, `u-boot-DDR4`, `atf`; host plan: none. Only H700-aarch64 (665 vs 671 lines) and RK3566-aarch64 (704 vs 712) differ between host and container |
| shadowed generic recipes | `projects/ROCKNIX/packages/sysutils/{busybox,systemd}/package.mk` | present, no `${ROOT}/packages/...` source line, so `get_pkg_directory` never resolves the generic directory: 45 and 38 generic paths unreached |
| explicit file references into a package directory | `git grep -nE '\$\{?ROOT\}?/(packages\|projects)/...'` excluding `package.mk` | none that read a file (the `create_addon` and `LINUX_DEPENDS` lines are roots) |
| the other nine projects | `git grep -lE 'projects/(ARM\|Allwinner\|...)'` over packages, projects/ROCKNIX, scripts, config, distributions, Makefile | no hit: all 407 paths unreached |

**Totals** (from `inventory.md`, generated): 134,589 rows, 24,817,974 lines;
4,420 shipped, 494 unshipped, 2,643 unreached (421,484 lines, 977 units),
127,032 `n/a`; 55 overlap paths.

**Leads for the slices** (P1 answers no Q1-Q7; each is a lead for the named
area's slice to confirm or overturn):

- *patches-and-configs, devices*: all 277 `packages/linux/patches/` are
  unreached: the ROCKNIX `linux` override takes `PKG_DIR` and its relative
  `PKG_PATCH_DIRS` resolve under it; the generic kernel patches are carried
  and never applied.
- *emulators-and-cores*: `vitaquake2-lr`'s four `patches/x86_64/` directories
  never apply: `scripts/unpack` sets `PATCH_ARCH=x86` on x86_64, and the core
  is built for AMD64-x86_64. The aarch64 siblings apply.
- *build-engine*: `distributions/ROCKNIX/config/functions:224` computes
  `SUBDEVICES` with `xmlstarlet ... 2>/dev/null`; without the tool it is
  silently empty and the plan loses bootloaders (guards fail closed). The
  container has it; `tools/viewplan` on a host does not say so.
- *generic-packages*: the generic `busybox` and `systemd` directories are
  wholly shadowed by ROCKNIX overrides (Q6 candidates, with
  `engineering-practices.md` § Before deleting a duplicate).

**Deltas against the brief:** the council toolchain is 46 of `scripts/`' 76
tracked files, not 45: `fork-workflow.md`'s list includes
`scripts/lib/verifier-pins.ts`, which the brief's list omits; it is placed
under tooling-and-guards with the rest. `podman-bin` is an upstream tool
directory, placed under build-engine.

## Pass 2: clustering

**The inventory was regenerated during this pass**, at `17dee5ba42`
(`docs/reviews/inventory.md`, committed in `fa3426bef7`), after three faults
the unit view exposed in the area map and the tool, each fixed in its own commit:

- `58948afbde`: brace alternatives were matched literally, so
  `scripts/{council-*,...}` matched nothing and the council toolchain's
  scripts sat in build-engine. The self-test's new wildcard-in-braces cases
  were seen to fail first (`FAIL brace glob scripts/council-invoke.ts`).
  After the fix:
  `Counter({'tooling-and-guards': 46})` for the 46 council files.
- `f6e1c08eb3`: `inventory.json` counted its own previous version as 137,055
  lines of doctrine; it is a record.
- `17dee5ba42`: `distributions/LibreELEC` and `LEIoT` (27 paths, 832 lines)
  read `n/a`; `config/options` defaults `DISTRO` to ROCKNIX and
  `git grep -nE '\bDISTRO='` finds nothing setting another, so they are unreached.

Counts at `17dee5ba42`: `paths: 133477 (git ls-files: 133477)`, `es-paths: 1114
(git ls-files: 1114)`, `patches: 1709 (find: 1709)`, `unassigned: 0`,
`ambiguous: 0`, `escaped: 2`.

**The cluster map.** One session reads about 8,000 to 12,000 lines (plan § 5).
Read sizes are code lines, from `inventory.md` § Read size per area; the
units are from § Largest units per area.

| Area | Code to read (fork-own + reached upstream) | Fits one session? | Candidate clusters (the units that make them) |
| --- | ---: | --- | --- |
| build-engine | 2,588 + 10,293 | about one | the engine itself (`scripts/` build, image, install, pkgbuilder, genbuildplan; `config/`; `distributions/ROCKNIX`); the upstream tools (`distro-tool`, `mkpkg`, ...) as a reachability table |
| os-scripts-and-launch | 10,832 + 20,953 | no: 3 | **launch** (`rocknix/sources/scripts/runemu.sh`, `setsettings.sh`, the start scripts); **control and state** (`chksysconfig`, `post-update`, `factoryreset`, `automount`, `wifictl`, `usbgadget`, the `rocknix` and `sysutils` units); **quirks** (`hardware/quirks`, 14,557 code lines over 608 per-device files, read per shipped device) |
| cloud-sync-and-saves | 29,172 + 0 | no: 3 | **sync core** (`cloud_backup`, `cloud_restore`, `cloud_sync_helper`, `cloud_capture`, `cloud_saves_root`, `cloud_net_ready`; 7,585 lines); **setup, connections and content** (`cloud_oauth`, `cloud_setup`, `cloud_remote`, `cloud_connections.py`, `cloud_content_*`, `cloud_scan`, `cloud_folder_validate`, `cloud_device_id`, `cloud_log_scrub`, `cloud-signin-window`, `backuptool`; 11,153); **the cloud test harness** (`tools/cloud-*`, 10,165, with `cloud-round-trip` 7,808 alone) |
| offline-achievements | 3,656 + 0 | yes | the proxy and its two source packages |
| emulators-and-cores | 4,091 + 11,407 | no: 2 | **standalone** (`emulators/standalone/*`, the largest `dolphin-sa`, `drastic-sa`, `armsx2-sa`); **libretro and RetroArch** (`emulators/libretro/*`, `retroarch`); the generic `packages/emulation` recipes are unreached (a table) |
| devices | 1,421 + 2,543 code; 75,028 other text | no: per device | one slice per shipped device (H700, SM8550, RK3566, RK3326, GENERIC_X64: options, device packages, device trees, quirk files read by diff); the unshipped devices and the nine other projects as tables |
| generic-packages | 7,194 + 18,905 | no: 3 | **the image's own** (`projects/ROCKNIX/packages/{apps,tools,virtual,...}`, 19,751 code); **generic packages reached** (`packages/*` reached, about 6,000); **the unreached generic packages** (94,879 lines: `addons`, `mediacenter/kodi`, shadowed `busybox` and `systemd`) as a dead-end table |
| interface | 97,916 + 241,540 | no: about 12 | **launch path** (`FileData.cpp` `launchGame`, `SystemData.cpp`, `ApiSystem.cpp`, `views/`); **the fork's pages** (`es-app/src/guis`, 20,321 fork-own lines of 31,639; split in two); **cloud and text** (`CloudText`, the cloud cards, `ProxyCards`, `es-app/tests/unit`); **es-core components and window** (`components`, `Window`, `InputManager`, 21,984 + ~3,200); **es-core utils, renderers, resources** (51,884); **the rest of es-app** (`services`, `scrapers`, collections, ~15,000); **the vendored libraries** (`external/`: libretro-common 87,217, rcheevos 33,547, doctest 7,134, nanosvg, id3v2lib) as a provenance table, not a read |
| patches-and-configs | 0 (vendor-carried) | no: table rows | one provenance row per patch (1,709) and per kernel config (33): **unreached patches** (778 paths, 317,908 lines; the 277 generic kernel patches among them) first and cheapest; **kernel patches of shipped devices**; **emulator and application patches** (the fork-written ones read with their package's slice); **unshipped devices' patches** |
| tooling-and-guards | 61,043 + 386 | no: 4 | **the guards** (`.githooks/*`, `forbidden-terms-check`, `ceremony-check`, `register-check`, `rules-check`, `box-check`, `rc-preflight`, `fork-workflow` CI); **the VM harness** (`vm-*`, `vm-walks/`, `frame-diff`, `time-to-play`); **last-good and state tests** (`last-good-scripts-test` 14,238 alone, the `pixelelated-*-test` family); **build supervision** (`watch-*`, `host-maintenance/`, `build-preflight`); the **council toolchain** (46 files, 13,939 + 1,534 lines) by provenance and version only (plan § 2) |
| doctrine | 190 code; 59,714 text | yes, as a doctrine read | `.claude/rules` (30 files, 8,000 lines), `.claude/skills` (12,400), `CLAUDE.md`, `AGENTS.md`, the registers, `NAMING.md`; read for rules that lie, hardcoded host paths (#640) and enforcement claims |
| records | not read | -- | reviewed only where a record misleads a reader today (plan § 5); one table slice at the end |

The three cloud figures are from `inventory.json` (`python3 -c` summing `lines` over the named paths: 7,585 over 6, 11,153 over 13, 10,165 over 9); the other exact figures are `inventory.md`'s, and the two marked `~` or *about* are rounded estimates that pass 5's per-slice counts (computed by the tool from `slices.json`) replace. Every cluster above is a lead for pass 5; the slice boundaries are drawn
after pass 4's edges.

## Pass 3: assessment

`tools/renovation-inventory --assess` wrote `docs/reviews/assessment.md`
(`wrote docs/reviews/assessment.md (11 areas; closed bugs 139, open issues 199,
friction lines 449, blindspot entries 74)`), from `inventory.json` at
`17dee5ba42` and the tracker, both issue lists under their limits (closed `bug`
limit 500 → 139; open limit 300 → 199). It was run twice: pass 4's first
matrix showed that names such as `export`, `format`, `toolchain` and
`pixelelated` matched everywhere, so they joined the stop list and the
assessment was regenerated; the numbers below are the second run's. The
mention counts (blindspots, friction, bugs, open issues) are whole-word
searches for an area's identifiers: leads, not findings. **H**, **M** and
**L** are relative across the eleven scored areas.

| Area | Security (token files) | Brittleness (blindspots / friction / closed bugs / commits since June) | New functionality (since base) | Planned change | Cost against value (read lines; callers) | Reachability |
| --- | --- | --- | --- | --- | --- | --- |
| cloud-sync-and-saves | **H**: 30 of 33; `rclone.conf` 12, `token` 13, `password` 12; the sign-in broker | **H**: 19 / 20 / 47 / 451 | **H**: +28,279 -364 | M: #576 (GTK4 sign-in) | **H** value (the state model); 29,172; 352 | none |
| os-scripts-and-launch | **H**: runs as root at boot and launch; 150 of 704; `/dev/` 110, `systemctl` 43 | **H**: 15 / 9 / 33 / 231 | M: +3,402 -668 | **H**: #336 replaces RetroArch, which `runemu.sh` configures and starts (`grep -ci retroarch runemu.sh` → 22) | **H**: 31,785; 784 | none |
| interface | **H**: credential pages; 122 of 920; `token` 74, `password` 40, `secret` 26 | **H**: 18 / 102 / 101 / 957 | **H**: +46,416 -1,362 | **H**: #336 Step 1 (D-WORKFLOW-102's gate), #576, #509 | M: 339,456 (the largest); 343 | none |
| offline-achievements | **H**: a network listener and the account token; 5 of 8 | M: 1 / 1 / 10 / 85 (all new, little history) | **H**: +3,666 -0 | L: #585 | **H**: 3,656, the cheapest product area; 35 | none |
| tooling-and-guards | M: host-only, carries the QA credentials and the secret guards; 94 of 138 | **H**: 28 / 107 / 60 / 633 | **H**: +64,917 (host) | M: #509 | L for the product: 61,433; 5 | none |
| build-engine | M: secret forwarding in `get_env`, downloads, `sudo`; 50 of 83 | M: 5 / 10 / 51 / 95 | L: +436 -93 | M: #336, #576 | **H**: 12,328 for 884 callers | L: 27 paths, 832 lines |
| devices | L: 37 of 88, mostly `/dev/` | M: 10 / 11 / 71 / 231 | L: +1,311 | M: #336, #576 | **H** per shipped device: 5,884; 793 | M: 216 unreached, 122 unshipped (28,291 lines) |
| generic-packages | L: 104 of 663, mostly `chmod` and `/dev/` | M: 5 / 17 / 17 / 906 (upstream merges) | L: +3,619 | M: #576 (webkitgtk) | M: 26,563; 204 | **H**: 1,565 unreached paths, 94,879 lines |
| emulators-and-cores | M: 44 of 276; installers' `curl`, settings' `password` | L: 0 / 2 / 12 / 155 | M: +4,222 | **H**: #336 (RetroArch is what the runner replaces) | M: 15,549; 50 | L: 84 unreached paths |
| patches-and-configs | L | L: 0 / 0 / 0 / 361 | M: +11,218 (fork-written patches) | L | **H** as a table: rows, not reading | **H**: 778 unreached (317,908 lines), 348 unshipped (286,952) |
| doctrine | L | L: 0 / 0 / 0 / 1,185 (records of the work) | -- | M: #509, #640 (hardcoded host paths) | **H**: small; every session obeys it | none |

Evidence notes that bear on the order:

- The mention counts overcount where an area's names are common words in
  this project (interface's 102 friction lines, tooling's 107); the scores
  above lean on blindspot entries and commits where that happens, and pass 5
  names the lens that placed each slice.
- **D-WORKFLOW-102's two gates bind regardless of the scores**: Tier 1's
  launch, control and state slice before `0.1`, and the interface's
  launch-path slice before #336 Step 1. Both fall in the two areas that
  score highest here, os-scripts-and-launch and interface.

## Pass 4: cross-reference

`tools/renovation-inventory --cross` wrote `docs/reviews/cross-reference.md`
(`wrote docs/reviews/cross-reference.md (10 areas, 60 directed pairs with an
edge)`). N-to-N over the ten areas with code: every ordered pair is counted
(90 cells), 60 have an edge. The first run had 69 edges, many through common
names (`export` 145 files, `toolchain` 215); those names are now stop words
and the matrix was regenerated. Two edge kinds that code text cannot show are
computed from the tree: rule to area (each `.claude/rules/*.md` `paths:` glob
resolved against the inventory), and patch to area (each patch against the
area of the package directory it sits in).

**At least one edge per area** (from the generated file unless noted):

| Area | Its strongest edges (files, identifiers named most) |
| --- | --- |
| build-engine | → generic-packages 20; ← tooling-and-guards 10 (`build_distro`, `docker`); governed by 25 rules |
| cloud-sync-and-saves | → interface 19, → os-scripts 15 (`busybox`, `autostart`, `automount`); ← interface 36 (`rclone`, `cloud_backup`, `cloud_content_restore`); ← os-scripts 10 (`backuptool`, `cloud_restore`); ← tooling 26 |
| devices | ← os-scripts 40 (`GENERIC_X64`, `ectool`, `RK3566`); ← emulators 28; 1,007 patches and configs |
| doctrine | → every area: 25 to 29 of the 30 rules govern each (rules with no `paths:` or `**`); ← tooling 0 by name after the stop list (doctrine has 2 code files) |
| emulators-and-cores | → generic 104; → interface 34; ← os-scripts 38 (`retroarch`, `drastic-sa`, `dsperate-sa`); 174 patches |
| generic-packages | ← emulators 104, ← os-scripts 84, ← interface 65 (`pugixml`, `rapidjson`); 505 patches |
| interface | → cloud 36, → os-scripts 40 (`wifictl`), → offline 16 (`raofflineproxy-ctl`, `raofflineproxy`); ← tooling 75; ← os-scripts 59 |
| offline-achievements | ← interface 16; ← tooling 12 (`raofflineproxy-refresh`); → interface 4; 18 patches |
| os-scripts-and-launch | → interface 59, → generic 84, → devices 40, → emulators 38, → cloud 10; 34 patches |
| patches-and-configs | → devices 1,007, generic-packages 505, emulators 174, os-scripts 34, offline 18, interface 4 (the packages they patch) |
| tooling-and-guards | → interface 75, → cloud 26, → os-scripts 22, → devices 22, → offline 12, → build 10 |
| records | not computed by the tool (never read). From the 21 audit folder names (`ls docs/audits`): cloud-sync-and-saves (`2026_08_24-milestone-cloud-saves-and-conflict-resolution`, `2026_09_03-milestone-cloud-sync-tiers`, `2026_09_12-milestone-cloud-saves-since-60`, `2026_10_11-epic-m7-network-cloud-344`), offline-achievements (`2026_09_14-epic-offline-retroachievements`), devices (`2026_09_06-issue-device-flashing-runbook`), tooling-and-guards (`2026_10_04-issue-410-guarded-swap`), and the release rounds across areas (`2026_09_24`, `2026_09_25`, `2026_09_28` twice, `2026_09_29` twice, `2026_10_02`, `2026_10_06`, `2026_10_08`, `2026_10_11-epic-553`, `2026_10_14`, `2026_10_15`); each slice reads its area's folders as provenance, verdicts sequestered (brief § 3) |

**Shared state** (the table in `cross-reference.md`): `system.cfg` and the
`get_setting`/`set_setting` interface, `es_settings.cfg`, `cloud_sync.conf`
and its rules, the cloud stamps and lock, `rclone.conf`, `retroarch.cfg`, the
proxy's state, `backuptool.conf`, `.cache/services`, the game hooks and the
evidence log are each touched by several areas. The seams pass 5 keeps inside
one slice, or makes a named interacting subsystem of both slices:

- **The launch path**: interface (`FileData::launchGame`, `LaunchCommand.h`),
  os-scripts (`runemu.sh`, `setsettings.sh`), emulators (RetroArch and the
  standalone start scripts), `system.cfg` and `retroarch.cfg`.
- **The cloud state model**: cloud (the scripts), interface (the cards and
  pages, 36 files naming the scripts), os-scripts (`backuptool`, the
  autostart hook, `automount`), the stamps, lock and `cloud_sync.conf`.
- **The offline achievements**: offline-achievements (the proxy), interface
  (`ProxyCards`, 16 files naming the proxy), emulators (RetroArch's
  `rcheevos` path), the proxy's state.
- **Device control**: os-scripts (`hardware/quirks`, the input and power
  scripts), devices (options, device trees), generic packages (the input
  stack).

## Pass 5: classification

`docs/reviews/slices.json` (hand-written) and `tools/renovation-inventory --order`
(`d8304fe068`, selector unions in the next commit), at the inventory of `17dee5ba42`:

```
$ tools/renovation-inventory --order
slices: 43
rows: 134591 (inventory: 134591)
unassigned: 0
ambiguous: 0
...
wrote the generated block of docs/reviews/order.md
```

The order's argument is `order.md` § How the order was argued; the lens that
placed each slice is in its block. Two drafts came before this one, and the
tool caught both:

- **First draft (41 slices):** two slices held no path (a `rest` for tooling
  and one for devices). Three exceeded a session: `es-app-rest` with 15,421
  fork-own lines, `es-core` with 25,856, `tooling-state-tests` with 21,045.
  A catch-all `**` in `devices-unshipped` was refused by the same guard
  `areas.json` has.
- **Second draft (43 slices):** the oversized ones split (es-app into views
  and scrapers, and the system layer; es-core into components, window and
  input, and utilities and resources; `last-good-scripts-test` alone). The
  empty ones dropped, and the order re-argued by lens: the gates, then the
  dead-end tables, then the data and credential areas, then what #336
  replaces.

**#346's criteria, checked against the rendered file:** every slice has a
number, area, lens, paths with line counts, release gate or none, depth with
reason, interacting subsystems and closing evidence (`grep -c '^### T[0-9]'
docs/reviews/order.md` → 43). The first three read 11,560 lines, 9,598 lines
and a table. Tier 1's launch, control and state slice is T1 and the
interface's launch-path slice is T2. The one slice over 12,000 read lines is
T32, a single 14,238-line file kept whole by plan § 5's "or one unit".

## Pass 6: reconciliation

The relationships pass 4 found, and how the order resolves each:

| Relationship | Kind | Resolution |
| --- | --- | --- |
| 41 fork-written vendor files (19,366 lines) sat in the Local-depth patch tables, away from the code they change | overlap | the proxy's 18 patches move to T7, RetroArch's 21 patches (8 fork-written) to T10, the H700 and GENERIC_X64 kernel configurations to T17 and T20, by selector unions in `slices.json`; `patches-shipped` (T39) became its area's `rest`, and its `why` names the small fork-written remainder it reads line by line. Check: 616 - 575 = 41 = 18 + 21 + 1 + 1 |
| the launch path spans T1 (`runemu.sh`), T2 (`FileData::launchGame`), T10 (RetroArch) and T16 (standalone start scripts) | dependency | T1 and T2 first (the gates), T10 before #336's work; each names the others as interacting |
| the cloud state model spans T5, T6, T8 and `backuptool` | overlap | T5 and T6 adjacent at Extended depth, T8 directly after (the scripts' contract is read before the pages that call it); `backuptool` stays in the cloud area (plan § 5) though it ships in the `rocknix` package |
| the proxy (T7), its ES pages (T9) and RetroArch's `rcheevos` path (T10) | dependency | T7 then T9 then T10 |
| generic recipes shadowed by ROCKNIX overrides (`busybox`, `systemd`) | supersession | the shadowed generic copies are in T3's dead-end table, not in the image-package slices; T3 runs before T21 and T35 so what it removes they never read |
| quirks split between platforms (T11) and handhelds (T15) | overlap | by directory, disjoint; T11 first |
| the doctrine governs every area (25 to 29 rules each) | dependency | T14, early, so rule fixes reach the later slices |
| the council toolchain is scaffold's export | conflict with line reading | T42 is a provenance table only (plan § 2; D-WORKFLOW-088) |

The result after reconciliation (`--order`, re-run): `rows: 134591
(inventory: 134591)`, `unassigned: 0`, `ambiguous: 0`.

## Item analysis table

Filled from pass 2 (one row per area).

## Relationships discovered

Filled from pass 4.
