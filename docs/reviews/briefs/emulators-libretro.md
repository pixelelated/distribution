# Brief: M6.P2 T3, RetroArch and the libretro cores (#650)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #650 differ, #650 wins and the
coordinator corrects the brief in the same session. **Version 2
(2026-10-24):** version 1 (`bc35aef3d8`) was written after T1's and T2's
briefs had each been through a futro and a stranger's proof (plan § 3,
principle 3), so the shapes those found wrong -- a count the executor
cannot reproduce, a tool's default that names a retired path, a line
number quoted from memory, a command whose variables do not survive a Bash
call, a seam described as agreement where the files disagree -- were
answered from the start; it then went through the same two readings
itself: the area epic's futro (`docs/futros/2026-10-24-m6-emulators-and-cores.md`,
#798, `179093ffd6`), whose substrate inspection found the image's
installed set readable on the host, `xmllint` and `xmlstarlet` absent, and
the order row's `read` figure a third quantity, and whose simulation added
Q4's two tiers and row classes, the host regeneration's sandbox, the
patches checked through the API, `deferred:M7-merge`, counts compared not
asserted, and the `n/a` cell for an unchanged upstream recipe; and a
stranger's proof (plan § 3, principle 3) that checked some sixty claims by
command and found thirteen wrong and twelve imprecise. Every one is
answered in the text below, and the proof is recorded at the end of § 10. **Each
command block below sets its own variables** (`D`, `B`, `A`): a Bash call
in this harness starts a fresh shell, only the working directory persists,
and the fork's tools are run by absolute path from `$D`.

## 1. Identity

- **Issue:** #650 `M6.P2 E798/T3: emulators-and-cores: RetroArch and the
  libretro cores`, slice `emulators-libretro` (`k: 3`) in
  `docs/reviews/slices.json`, third in `docs/reviews/order.md` (§ 2 of the
  order: *"#336's own prerequisite stays third"*; the order's row is on the
  P1 branch). **Epic:** #798, the area epic for **the emulators and cores**
  (`emulators-and-cores` in `docs/reviews/areas.json`: T3, T30
  `emulators-standalone`, T24 `emulators-dead-ends`), filed by the
  coordinator on 2026-10-24 under the renovation epic #339 with its futro
  as its first comment; #650, #677 and #671 are its sub-issues, retitled
  `E798/T<k>` (`milestone-phase-naming.md`). **Milestone:** M6 (`M6: Codebase
  renovation`); its body holds the live order; read it first.
  **Predecessors:** #346 (the plan), #641 (the survey, the inventory and the
  order; closed 2026-10-23), T1 #648 and T2 #649 (both accepted at hand-back
  on 2026-10-24, both `remediating` until the first image after their
  merge; their branches are unmerged and their worktrees kept; § 3 names
  what each left for this slice). **Beside it:** nothing runs in another M6
  lane when this one starts; D-WORKFLOW-190 allows a slice in another area
  beside this one later, and two slices never share a path. **The dispatch**
  is the coordinator's comment on #650 that names this brief's commit, the
  model and effort, and authorizes the two external reviewer calls and the
  `npm install` of § 1; the lane's first comment answers it.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, re-order anything, change a criterion, write a
  brief, move the M6 body, edit `slices.json`, `areas.json`, `order.md` or
  the plan, bump a pin on `next`, or decide a question of scope: those are
  the coordinator's, reached through #650, one question at a time. What this
  lane does file: its own audit punch-list issue (stage D, the code-auditor
  skill's Phase 6) and a `bug` issue for every defect it finds
  (D-WORKFLOW-187: a defect found by the renovation is a bug like any
  other; `bugs-are-agent-first.md` gives the shape, with its VM-verifiable
  criterion). Nothing else.
- **One worktree, one session.** The slice's paths are all in the
  distribution, so the lane holds one worktree: branch
  `feature/m6-emulators-libretro-650` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-libretro-650`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** (which carries the P0 branch), with the coordinator's tip
  merged in and the lane's pointer seeded (the two hashes are in the
  dispatch comment on #650). The coordinator wrote there only before the
  lane started; from the dispatch on, one session per worktree
  (D-WORKFLOW-183) and the coordinator writes nothing there. **The rules in
  this worktree are `next`'s except three files:** P1's `fork-workflow.md`
  and `instruction-files.md` (the three renovation tools added to the
  fork-tool lists) and the council skill's
  `.claude/skills/council/IMPORTED-FROM.md` (M7's Argon route, cherry-picked
  onto the coordinator branch as `033eb7ed23`, `0ceb2994c5`, `6874394d49`),
  plus whatever the coordinator's later commits added to the rules
  (`generic-x64-vm-testing.md` gained a `time-to-play` paragraph on
  2026-10-24, `8c9b1d4721`); the first commands list the diff and the
  dispatch comment names the expected files. The primary checkout is
  `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025).
  `worktrees.md`, `device-builds.md`, `CLAUDE.md` and `AGENTS.md` still name
  the legacy layout (`/workspace/repos/rocknix`, `rocknix.worktrees/`); #640
  owns that drift, and this brief's paths are the ones to use. The legacy
  checkout and every worktree beside it are the M7 lane's: read from them
  (an image, a build root, a diff), never write. The T1 and T2 worktrees
  (`m6-os-launch-control-state-648`, `m6-es-launch-path-649`, and T2's
  EmulationStation worktree under `/home/max/Development/emulationstation-next.worktrees/`)
  are other lanes': read with `git -C`, never write.
- **Model and effort:** Opus 5.5 at high effort (the maintainer, 2026-10-22:
  *"the work will be Opus 5.5"*), unless the dispatch says otherwise.
  Record what actually ran in `00-running-log.md`'s header.
- **Review depth: Extended** (plan § 6c; `slices.json`: *"the launch path
  (RetroArch's start)"*). The primary auditor is this lane (Anthropic). The
  two reviewers come from two other labs, each through the Facilitator and
  nothing else (D-WORKFLOW-049, D-WORKFLOW-137; `adversarial-council.md`
  rule 4; the code-auditor skill's Phase 4.6):
  - **GPT-6 Astra**: `tools/council/run invoke --member gpt --provider
    openrouter --prompt-file <brief> --output <file>` at `max`, the installed
    recipe (`openai/gpt-6-astra`, provider pinned to OpenAI).
  - **Gemini 4 Argon** (Google): `--member gemini-argon --provider
    openrouter` at `high`. **Its route is in this tree**: the coordinator
    branch carries M7's three commits (`fac2129787`, `1c7d283ad5`,
    `a7a3bdda4e` cherry-picked, #636/#638), so `grep -c gemini-argon
    scripts/council-invoke.ts tools/lint-audit-artifacts` prints `7` and `4`;
    T1 and T2 each ran the seat on 2026-10-23 (served `google/gemini-4-argon`
    by `Google`; T1's call about nine minutes, 16:25:30 to 16:34:19). The roster's `--member gemini` is never
    called in its place. A seat that fails identity verification is recorded
    as pending, never replaced, and at Extended depth that is the Phase 4.6
    blocker (§ 8).
  - Both reviewers run the **refutation pass alone** (the audit is epic
    tier; phases.md § Phase 4.6: two calls at Milestone tier, one otherwise),
    each prepared independently. `second-opinions/review-plan.json` is
    written before the first call (`templates.md` § Second opinion: depth
    `extended`, primary `anthropic/claude-opus-5-5`, lab `anthropic`,
    identity source the dispatch comment and the session's own metadata,
    two reviewers). Every seat item is a lead; the orchestrator re-reads the
    artifact before a row is written.
  - The runner's dependencies are not in a fresh worktree: `tools/council/run`
    execs `tools/council/node_modules/.bin/tsx`, and `node_modules/` is
    gitignored. Install once, before Phase 4.6, with `npm install --prefix
    tools/council` in the worktree (a gitignored write; the npm registry;
    `node` v24 and `npm` 11 are on the host; record the `tsx` version in
    `00-running-log.md`), then `tools/council/run verify-pins` must print its
    `OK` line and `tools/council/run test` must pass (T1 saw routing
    127/127). The key is sourced from `~/.config/council/env` (present, never
    read into a transcript, never on a command line). The dispatch comment
    on #650 is the authorization for exactly these two external calls plus a
    probe of each seat first, its provenance naming the served model.
    **During a host window of § 5 the install waits too**: it is not a
    compiler, but the agreement with the M7 lane says no new runtime of any
    kind until the return line.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-libretro-650
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-emulators-libretro-650
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md   # the files the dispatch comment lists; any other file is STALE
grep -c 'Renovation face' tools/lint-audit-artifacts; grep -c gemini-argon tools/lint-audit-artifacts   # both non-zero: the merged lint carries P1's renovation face and M7's Argon receipts, the copy T1 and T2 ran
ls tools/renovation-inventory tools/renovation-status tools/renovation-drift docs/reviews/inventory.json docs/reviews/slices.json   # P1's, present because the branch is stacked on P1 (absent on the coordinator branch)
git rev-parse --short upstream/next                                  # record it: Q4's upstream, fetched now
git merge-base next upstream/next                                    # c445081a59 on 2026-10-24; record it
git diff --quiet 8ebaf8daad HEAD -- projects/ROCKNIX/packages/emulators/libretro projects/ROCKNIX/packages/virtual/emulators && echo "slice bytes are next's at 8ebaf8daad" || echo "the slice's bytes differ from 8ebaf8daad: record the diff --stat and stop (§ 8)"
git push -u origin feature/m6-emulators-libretro-650                 # the lane's own branch, at the coordinator's merge until the first commit
test -f docs/reviews/briefs/emulators-libretro.md || { echo "the brief is not in this tree: stop"; exit 1; }
test -f docs/futros/2026-10-24-m6-emulators-and-cores.md || echo "the epic's futro is not in this tree: ask the coordinator before the first audit commit"
cat .github/sessions/saved-session-state-feature-m6-emulators-libretro-650.md   # the lane's seeded pointer
cat /tmp/m7-m6-host-coordination-20261023.txt | tail -5                          # the host's state (§ 5): a window open means no runtime
```

The order of the first session: § 3's reading first (it is the pre-flight,
`working-principles.md`; it fills the first hour), then stage A.

## 2. Scope

**344 paths of the distribution, 31,961 lines; the fork's own lines read
line by line, the rest at Q4 and Q6 first.** The membership is the
inventory's, with the three rules of `slices.json` (`k: 3`) applied as
`tools/renovation-inventory --order` applies them: a rule without `areas`
takes the slice's own area (`emulators-and-cores`); the second rule takes
`patches-and-configs` rows under `projects/ROCKNIX/packages/emulators/libretro/retroarch/**`;
the third takes `generic-packages` rows under
`projects/ROCKNIX/packages/virtual/emulators/**`. #650 says the same set as
`--order`'s membership; the filter below is the re-derivation, because
`--order` writes files (and `--slice-issues <dir>` writes forty-six issue
bodies into that directory: never run it in a worktree you keep).

**The hash.** The slice's bytes are `next`'s at **`8ebaf8daad`** (the same
hash T1 and T2 read at; `next` has not moved since). **`reviewed-at:` is the
branch's `HEAD` at stage A** (the commit the read is made at), recorded in
`00-running-log.md` and `01-research-notes.md` § Scope. The stop (§ 8) is
the slice's bytes differing from `8ebaf8daad` at stage A: then the slice was
re-based under the read and the coordinator re-baselines it. `next` moving
later is not a stop; it is drift, § 2's last paragraph.

**The counts, recorded by the survey at `eb4763e3cc` and re-derived here.**
A count that differs is a delta beside the recorded one, not a stop; the
stop is a count that cannot be produced, or two commands for one quantity
that disagree. The inventory's line count is git's numstat against the
empty tree (`docs/reviews/README.md`):

```bash
python3 -I - <<'PY'
import json, re, collections
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
rules = [({"emulators-and-cores"}, ["projects/ROCKNIX/packages/emulators/**"], ["projects/ROCKNIX/packages/emulators/standalone/**"], {"shipped", "test", "n/a"}),
         ({"patches-and-configs"}, ["projects/ROCKNIX/packages/emulators/libretro/retroarch/**"], [], None),
         ({"generic-packages"}, ["projects/ROCKNIX/packages/virtual/emulators/**"], [], None)]
def gm(p, g): return re.fullmatch(re.escape(g).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*"), p) is not None
sel = {}
for areas, inc, exc, reach in rules:
    for r in rows:
        if r["tree"] != "distribution" or r["area"] not in areas: continue
        if reach and r["reach"] not in reach: continue
        if not any(gm(r["path"], g) for g in inc) or any(gm(r["path"], g) for g in exc): continue
        sel[r["path"]] = r
t3 = list(sel.values()); L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t3), "lines", L(t3), dict(collections.Counter(r["tier"] for r in t3)), dict(collections.Counter(r["area"] for r in t3)))
print("fork-own lines", L([r for r in t3 if r["tier"] == "fork-own"]), "of which retroarch/sources/GENERIC_X64", L([r for r in t3 if r["tier"] == "fork-own" and "/sources/GENERIC_X64/" in r["path"]]))
print("vendor-carried (RetroArch's patches) lines", L([r for r in t3 if r["tier"] == "vendor-carried"]), "fork-written", len([r for r in t3 if r["tier_note"] == "fork-written"]), L([r for r in t3 if r["tier_note"] == "fork-written"]))
print("reach", dict(collections.Counter(r["reach"] for r in t3)))
for r in sorted((r for r in t3 if r["tier"] != "upstream-carried"), key=lambda r: -(r["lines"] or 0)): print(r["lines"], r["tier"], r["tier_note"] or "", r["reach"], r["path"])
PY
git ls-files projects/ROCKNIX/packages/emulators/libretro projects/ROCKNIX/packages/virtual/emulators | wc -l                              # 406: the 344 plus the cores' own patches (57 files, T42's) and anything the inventory classes otherwise; record the difference by listing it
git diff --numstat "$(git hash-object -t tree /dev/null)" 8ebaf8daad -- projects/ROCKNIX/packages/emulators/libretro/retroarch/patches | awk '{s+=$1} END {print s}'   # 1670
```

Recorded (the coordinator's run of this filter on 2026-10-24 against the
P1 tip's `inventory.json`): **344 paths, 31,961 lines; 24 fork-own paths,
6,557 lines; 299 upstream-carried; 21 vendor-carried (RetroArch's patches,
1,670 lines, 8 of them fork-written, 1,244 lines); 294 rows in
`emulators-and-cores`, 21 in `patches-and-configs`, 29 in
`generic-packages`; 342 `shipped`, 2 `n/a` (the two rotation-table
generators, build-time tools).** The order's row prints `344 paths 31,961
lines 10,185 read 5,519 fork-own 1,670 patch`, three figures of the tool's
own: its **5,519** is the filter's 6,557 without the four GENERIC_X64
configuration files (1,038 lines), whose `language` is `config` or `other`,
outside the tool's code classes (their `area` is `emulators-and-cores`; the
21 `patches-and-configs` rows are RetroArch's patches alone); its **10,185 read** is the inventory's code classes
summed whatever their tier (`recipe` 147 files 5,443 lines, `shell` 31 /
3,971, `cmake` 2 / 368, `python` 2 / 245, `udev` 9 / 80, `systemd` 6 / 78;
`tools/renovation-inventory` line 999), which leaves the **19,518 lines of
`config`** (the fifteen `retroarch.cfg` sets, the option files and the
remaps, 96 files), the 1,670 of `patch` and 567 of `other` outside it; its
**1,670** is RetroArch's 21 patches. This brief's read set is by
provenance, not by class: the 24 fork-own paths and the 8 fork-written
patches whole (the GENERIC_X64 configuration included), the 13 upstream
patches and the 299 upstream-carried paths at Q4 and Q6 first. The lane
records the three figures beside its own and names any delta. **Not in the membership, read only where a recipe points at
them:** the cores' own patch files (57, under thirty recipes' `patches/`
directories, `vitaquake2-lr` 8 and `ppsspp-lr` 7 down to one each;
`patches-and-configs` rows that T42 `patches-shipped` owns);
`distributions/ROCKNIX/config/functions` (T5's, where `add_emu_doc` 50,
`mk_system_doc` 64, `clean_es_cache` 80, `add_emu_core` 88,
`mk_es_systems` 99, `add_system_dir` 117 and `add_es_system` 127 are
defined); the 139 `config/emulators/*.conf` fragments (T5's);
`packages/emulation/**` (the generic tree's 97 emulation paths; the
inventory's `shadowed_by` is null for every row on both sides, so a shadow
relation is derived by name where Q6 needs it, a recipe name present in both
trees); the standalone emulators (`emulators/standalone/**`, T30's).

**Where the code runs on the image.** Nothing here is a process of its own:
the slice is **recipes, patches and configuration** that decide what the
image carries and how RetroArch starts. The recipes build `/usr/bin/retroarch`
(and `/usr/bin/retroarch32` where the arm root exists, `package.mk` 106 to
114), install the per-device `sources/<DEVICE>/*` into `/usr/config/retroarch`
(128 to 134; a device without a `sources/` directory fails the build at
133) and the cores into `/usr/lib/libretro` (each `*-lr` recipe's
`makeinstall_target`); the `emulators` metapackage's `makeinstall_target`
(`virtual/emulators/package.mk` 140 to the end) writes
`/etc/emulationstation/es_systems.cfg` through 583 `add_emu_core` and 142
`add_es_system` calls, then `mk_es_systems` (line 1726) and `mk_system_doc`
(1728), with every system's
launch line `RUNCMD='/usr/bin/runemu.sh %ROM% -P%SYSTEM% --core=%CORE%
--emulator=%EMULATOR% --controllers="%CONTROLLERSCONFIG%"'` unless the
system's `config/emulators/<system>.conf` sets `SYSTEM_COMMAND`
(`functions` 128 to 141), and installs the 24 `sources/*.sh` launchers and
installers as `/usr/config/modules/<name>.sh` (`install_script`, 132 to
138). **All of that installed set is readable on the host without a guest**, from
the M7 GENERIC_X64 build root's install tree
`/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system`
(world-readable, built from `069fc2704421`; read, never written): on
2026-10-24 it held 116 `usr/lib/libretro/*_libretro.so`, 19
`usr/config/modules/*.sh`, `usr/config/retroarch/` with the four tracked
files beside `Flycast.opt`, `Supafaust.opt` and `savefiles/` (other
recipes' installs), `usr/bin/retroarch` and no `retroarch32`, and the
generated table at `usr/config/emulationstation/es_systems.cfg` (83,206
bytes, 2,745 lines; 128 `<system>`, 152 `<emulator name=`, 500 `<core`
elements) -- `etc/emulationstation/es_systems.cfg` is a symlink to its
absolute path, dangling in the tree and resolving on the image (#613 is
T2's lead on the fallback). The `.tar` beside the `.img.gz` in the root's
`target/` carries the same `SYSTEM`. At run time `runemu.sh` (T1's, read at `efadfea08a`) composes
`/storage/.config/retroarch/retroarch.cfg` from `/usr/config/retroarch/`
and the settings, and starts RetroArch with the core; EmulationStation
(T2's) reads `es_systems.cfg` through `SystemData::loadConfig` and builds
the command with `FileData::getlaunchCommand`. Both lanes' audits are the
other sides of this slice's table (§ 3). **Two seams the table owns:**
`RUNCMD` puts `-P%SYSTEM%` right after `%ROM%`, and `runemu.sh` reads the
system as `${ARGUMENTS##*-P}`, the last `-P` anywhere in the line, so a ROM
path that contains `-P` is where this table meets T1's open #730
(`LaunchCommand.h` reads whole tokens, and the two readers differ by
design); and the table emits exactly five tokens (`%ROM%`, `%SYSTEM%`,
`%CORE%`, `%EMULATOR%`, `%CONTROLLERSCONFIG%`) while the interface expands
more (`%BASENAME%`, `%ROM_RAW%`, `%GAMENAME%`, `%SYSTEMNAME%`,
`%GAMEINFOXML%` are unreached because no system emits them: T2's Q6 rows),
and reads `es_systems_custom.cfg` and `es_systems_*.cfg` overlays first, an
unparseable overlay skipping every later one
(`SystemData::loadAdditionnalConfig`; #613 on the fallback symlink). A Q6
row each (§ 4), and the first two rows of § 6's interaction audit.

**Five groups, read in this order** (the slice's reason to be third is
#336 Step 1, which replaces RetroArch under the launcher for the 2D cores;
plan § 6a, `slices.json`'s `why`). Line numbers are `next`'s at
`8ebaf8daad`, from a read-only seam map the coordinator made on 2026-10-24;
each is a lead to re-read, not a verdict:

1. **RetroArch's recipe, patches and configuration** (`emulators/libretro/retroarch/`):
   `package.mk` (153 lines, fork-own, `overlap: false`): the pin at line 5,
   `bdba046fa6766380bc2457532f38e589df769aaf # v1.22.2 + fixes` (a
   libretro/RetroArch commit of 2026-06-06, after the last release
   `v1.22.2` of 2025-11-20; the sha256 at 6); the configure options (28 to
   64: `--disable-qt`, `--enable-kms`, `--enable-ffmpeg`, neon by `ARCH`,
   `librga` for `RK*`, Wayland and the window manager by `DISPLAYSERVER`),
   GL against GLES by `OPENGLES_SUPPORT`/`PREFER_GLES` (66 to 76), Vulkan
   (78 to 83), `pre_configure_target` adding `-DUDEV_TOUCH_SUPPORT` (85 to
   90), `make_target` with its `HAVE_*` list and the hand-rolled `[ $? -eq
   0 ] && echo ... || exit 1` after each of three makes (92 to 99),
   `makeinstall_target` (101 to 145: the 32-bit copy from
   `${ROOT}/build.${DISTRONAME}-${DEVICE}.arm/install_pkg/retroarch-*`,
   `43d0bc3bf4` of 2026-10-07 the fork's one commit on the file since the
   merge base; the filters; the per-device configuration; the shader
   directories' `.overlay` markers; the achievement sounds and
   `scripts/call_achievements_hooks.sh`), `post_install` enabling five
   `tmp-*.mount` units (147 to 153). **The 21 patches**: 13 are upstream's
   (`0001-Increase-glui-size` to `0010-paths`, `0011-cheevos-sounds`,
   `0012-cheevos-cmd`, `batteryplus/0001-batteryplus-capacity` under
   `PKG_PATCH_DIRS` when `BATTERYPLUS_SUPPORT=yes`, line 26), **8 are the
   fork's** (`0011-video-thread-wrapper-serialise-posters`,
   `0013-cheevos-offline-proxy-toast`, `0014-widgets-backdrop-follows-the-font`,
   `0015-video-thread-wrapper-run-a-command-once`,
   `0016-widgets-message-queue-floor`, `0017-widgets-sharp-font-sizes`,
   `0018-auto-slot-survives-content-load`,
   `0019-widgets-message-queue-keeps-its-place`; 1,244 lines; the register
   rows that made them are § 3's), and **one of upstream's is absent here**:
   `retroarch-0100-ffmpeg9-lavc63.patch`, added on `upstream/next` with the
   multimedia merge `075a7c303b` of 2026-10-17 (Q4's first disposition).
   `autostart/003-logging`, `modprobe.d/usbhid.conf`,
   `retroarch-assets/package.mk`, `retroarch-overlays/package.mk`,
   `retroarch-joypads/` (its `package.mk`, `system.d/tmp-joypads.mount`,
   and the gamepad `*.cfg` files, 22 with spaces and one with a leading
   space, which every loop over them must quote),
   `system.d/tmp-{assets,cores,database,overlays,shaders}.mount`,
   `tmpfiles.d/retroarch-userdirs.conf`, `udev.d/` (eight rules), `sounds/`,
   `scripts/`. **The per-device
   configuration**, `sources/<DEVICE>/` for fifteen devices (AMD64,
   GENERIC_X64, H700, RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450,
   SM6115, SM8250, SM8550, SM8650, SM8750; 4 or 5 files each:
   `retroarch.cfg`, `retroarch-core-options.cfg`, `retroarch64bit-append.cfg`,
   `TATE-MAME 2003-Plus.rmp`, and on the fourteen devices other than
   GENERIC_X64 a fifth, `retroarch32bit-append.cfg`): the
   GENERIC_X64 set is fork-own (`cbdb91a517` of 2026-07-01 added it;
   `eb131d112f` #263 D-QA-042 and `a5a03bd9fa` set the surface and the gl
   driver for the guest; `9fd73da845` dropped a dead armhf core-updater
   URL), the fourteen others upstream-carried. The fork builds five of the
   fifteen (H700, RK3326, RK3566, SM8550, GENERIC_X64: `device-builds.md`
   § Our devices); Q6 says what the other ten are.
2. **The `emulators` metapackage and the launch table**
   (`virtual/emulators/`, 29 paths, `generic-packages`): `package.mk`
   (1,777 lines, fork-own, `overlap: true`; the fork's delta against
   `upstream/next` is 94 lines): `PKG_EMUS` (12 to 13) and `LIBRETRO_CORES` (19 to
   31), the aarch64 additions (34 to 37), the per-device case with eleven
   arms (40 to 105: H700|RK3326, RK3399, RK3566|RK3576, RK3588, SM6115,
   SM4450, SM8250, SM8550, SM8650|SM8750, S922X, GENERIC_X64 with its
   `dolphin-sa` comment, AMD64), `X64_SKIP_CORES="parallel-n64-lr
   flycast2021-lr duckstation-lr idtech-lr"` (107 to 115, *"tracked in
   issue #16"*, which is **closed**: a Q6 and Q7 lead, the comment names a
   closed issue), the `TARGET_TYPE` split for the GitHub runner (117 to
   130), `install_script` (132 to 138), and `makeinstall_target` (140 to
   the end: one function of about 1,630 lines, the README comment at 141
   to 157, the six `add_system_dir` calls, then 583 `add_emu_core` and 142
   `add_es_system` calls, `mk_es_systems` at 1726 and `mk_system_doc` at
   1728). The 24 `sources/*.sh`
   (`Install Steam.sh` **2,755 lines, fork-own**: `6f2eb9c212`,
   `9aaaaa0f64`, `f8636de1d1` of 2026-10-14/15 on `next` rewrote it from
   upstream's `51bebf5e1d`; the M7 lane's unmerged `6101242e14` of
   2026-10-18 changes it again, +605/-6, the **only M7 delta on this
   slice's paths**, see the last paragraph of this section; `Start
   AetherSX2.sh` +20 and `Start RPCS3.sh` 2 lines against upstream; the
   rest upstream-carried), `autostart/001-controller`, `scripts/mkcontroller`,
   `tmpfiles.d/rocknix-dirs.conf`, `udev.d/99-automount.rules` (5 lines
   against upstream). Read beside it, as T5's context: `functions` 99 to
   140 (`mk_es_systems` concatenates `${ESTMP}/*.tmp` in `ls | sort` order
   and runs `xmlstarlet fo -t ... 2>/dev/null`, so a malformed fragment is
   silent at build time: a Q3 lead to prove, not a verdict) and the
   `config/emulators/<system>.conf` a system's `add_es_system` sources.
3. **The fork's own core recipes** (fork-own, in `emulators/libretro/`):
   `ppsspp-lr` (81 lines, +11/-1 against upstream; `device-builds.md` § Late
   binding names its history), `mupen64plus-lr` (+9/-1), `idtech-lr`
   (+13/-5), `fbalpha2012-lr`, `fbalpha2019-lr`, `fbneo-lr`,
   `mame2003-plus-lr`, `mame2010-lr` (+19/-1 each: the rotation-table hook,
   `d73b0499f8` *"generators skip #if 0 and strings; recipes die on their
   own"*), `desmume-lr` and `gpsp-lr` (+2/-2), `freej2me-lr` (+3/-1),
   `libretro-database` (+1/-1), `easyrpg-lr`'s three sub-recipes
   (`libspeexdsp`, `libxmp-lite`, `wildmidi`; fork-own with `overlap:
   false`: the lane reads their history for why), and the two **rotation
   tables**, `rotation-table-fba.py` (120) and `rotation-table-mame.py`
   (125): build-time Python that reads a core's sources for the games that
   rotate (`50d83513fd`, `cbaf461897`, `dcb88d933e` of 2026-09-28; `reach:
   n/a`). Every one of these carries an `overlap: true` or a fork history
   the lane reads with `git log -p` before judging a line (`engineering-practices.md`
   § Verify design intent).
4. **The upstream-carried core recipes.** `git ls-files
   'projects/ROCKNIX/packages/emulators/libretro/*/package.mk'
   'projects/ROCKNIX/packages/emulators/libretro/*/*/package.mk' | wc -l`
   prints **151** at `8ebaf8daad`; **146 are in the membership** (131 `*-lr`
   recipes, of which 11 are group 3's fork-own and **120 upstream-carried**;
   plus the fifteen others: `retroarch`, `retroarch-assets`,
   `retroarch-joypads`, `retroarch-overlays`, `libretro-database`,
   `core-info`, `common-shaders`, `glsl-shaders`, `slang-shaders`,
   `retropie-shaders`, `neocd_lr`, and `easyrpg-lr`'s four sub-recipes
   `liblcf`, `libspeexdsp`, `libxmp-lite`, `wildmidi`), and **five are not**
   (`boom3-lr`, `mame2003-lr`, `panda3ds-lr`, `play-lr`, `vitaquake3-lr`:
   their `reach` is outside this slice's rule, so they are T24's table,
   `emulators-dead-ends`; a row each in Q6 says so and reads nothing else
   of them). Pins over the 151: 144 full 40-hex hashes, 1 short hash, 6
   tags or other (the lane names the seven; `CLAUDE.md`: *"Pin git sources
   with the full commit hash"*). Hosts: 148 `github.com`, one each
   `sourceforge.net`, `gitlab.com`, `rocknix.org`. **Against `upstream/next`
   on 2026-10-24, exactly one *pin* differs** (`np2kai-lr`: `d1a40352e2`
   here, `5939e0c6d5` upstream) **but about 140 recipes differ textually**:
   upstream's `af70bd435b` added `retroarch` to every core's
   `PKG_DEPENDS_TARGET` and `aca36dbad7` took it off `mame-lr` again, and
   eight recipes differ by a few lines more (`emuscv-lr`, `dolphin-lr`,
   `mame-lr`, `pcsx_rearmed-lr`, `uae4arm-lr`, `vircon32-lr`, `same_cdi-lr`,
   `np2kai-lr`); upstream also carries what this tree has not:
   `yabadabadoo-lr/` (a recipe and a patch), `doublecherrygb-lr/patches/001-*`,
   `flycast2021-lr/patches/02-fix-postprocess-render.patch`,
   `np2kai-lr/patches/001-libretro-add-ymzadpcm.patch`, a changed
   `retroarch/sources/RK3566/retroarch.cfg`, and
   `retroarch-0100-ffmpeg9-lavc63.patch`. Q4 (a) is the 14 commits, and
   this is their size. These recipes get Q4 and Q6 first (§ 4), and the
   rest only where a Q3 lead turns up in a recipe that stays.
5. **The tests and tools that exist for these sources** (fork-only, in
   `tools/`, outside the membership; read for § 5): `tools/retroarch-wrapper-test`
   (compiles `video_thread_wrapper.c`'s posting path out of a build root
   and counts calls; written for #211; **its two default roots name the
   retired layout** `rocknix.worktrees/devices/build.ROCKNIX-H700.aarch64`
   and `rocknix.worktrees/generic-x64/build.ROCKNIX-GENERIC_X64.x86_64`,
   both absent on this host -- a `bug` to file at stage A in #699's shape,
   fixed on this branch by the tool's default-root list only, with the
   explicit path of § 5 until then), `tools/fork-package-freshness` (covers
   none of this slice: `--list` names only `aethersx2-sa` under
   `emulators/`, T30's; say so in `02`), `tools/time-to-play` and
   `tools/emulator-exit-test` (T1's measurements, § 5), `tools/ra-candidate-games`
   (which homebrew titles carry cheap achievements; a source of fixture
   ROMs), `tools/pkgcheck` (upstream's).

**Upstream's side of Q4, at the first commands' fetch:** 14 commits of
`c445081a59..upstream/next` touch the membership's two directories (the
list of 2026-10-24: `c4d353449e` aethersx2 dropped for licensing,
`075a7c303b` the multimedia merge, `bb8d0aab8e` and `8704addb6b`
yabadabadoo, `a1ea79474b` rk3566 inputplumber, `aca36dbad7` mame-lr without
the retroarch dependency, `6103571f67` the core-updates merge, `af70bd435b`
retroarch as the cores' `PKG_DEPENDS_TARGET`, `eeb33c5a37` quit hotkey
targets, `c9820d0e89` pcsx_rearmed's 32-bit core where runemu loads it,
`dc781c0c75` udev non-blocking systemctl, `096c0d4e96` and `142df62157` the
mmc resume, `6679670966` the gcc-glibc merge), against 54 fork commits on
the same paths since the base. **The closed `bug` issues** that name a
recipe, a patch or `es_systems.cfg` are Phase 1's: `gh issue list --repo
pixelelated/distribution --label bug --state closed --limit 500 --json
number,title,body`, grepped with word boundaries for `retroarch`,
`libretro`, `es_systems`, `virtual/emulators`, `rotation-table`, `core
options` (the count depends on the pattern, so record the pattern with the
count).

**The branch scan**, by one predicate: a branch is *ahead* of `next` on the
two directories when `git log --oneline next..<branch> -- <the two
directories>` prints a line. On 2026-10-24, 18 `origin` branches were
(`feature/m7-player-setup` among them, by `d9054efc46`, whose `Install
Steam.sh` is blob-equal to `next`'s; **the M7 hunk `6101242e14` is on no
`origin` branch** -- it lives on the legacy checkout's
`legacy/m7-audit-integration-603` and local branches only, T3's stage-A
correction of 2026-10-24); 44 merely *differ* (`git diff --quiet next <branch> -- ...`
non-zero), most of them older than `next`. Record the predicate, the
command and the list in `01-research-notes.md`; a branch ahead of `next` on
a slice path is a lead for the coordinator, posted on #650, not a reason to
read it.

**The M7 lane's unmerged delta (`next..069fc2704421` in the legacy
checkout, read-only):** one commit, `6101242e14` (2026-10-18, *"m7:
integrate reviewed frontend and installer repairs"*), +605/-6 on `Install
Steam.sh`. The slice reads `next`'s copy. A finding on a line that commit
changes is recorded with that fact; a punch item that would touch `Install
Steam.sh` is announced on #650 before any stream brief, so the coordinator
can order it against the M7 candidate's merge (as the coordinator's comment on #642 did for T1's
F-14 and F-03 on M7's `runemu.sh` hunks). The lane never reads the M7 worktrees for anything else.

**Drift.** `next` is `8ebaf8daad` and has not moved since the survey; the
M7 candidate's merge will move it. When it does, the coordinator merges
`next` into this branch -- never between stage A and stage D (the read must
stay a fact about one hash, plan § 8); after stage D a merge re-baselines
the slice over the diff, recorded on #650. `tools/renovation-drift` is the
coordinator's at every slice close; this lane runs it to read, never to
write.

## 3. Read first

From `next`, in this order, before any analysis (this is the first
session's first hour; stage A follows it):

- `.github/sessions/saved-session-state-next.md` (the M7 lane's canonical
  checkpoint; read for what runs on this host, not for a work queue) and
  this lane's own pointer.
- The code-auditor skill whole: `.claude/skills/code-auditor/SKILL.md` and
  its `references/phases.md`, `review-levels.md`, `templates.md`,
  `anti-patterns.md`. The slice runs under its lifecycle with the renovation
  face added (plan § 6b); stage B's Phase 2 criteria are #650's checklist,
  and Phase 3 carries § 4 below as its renovation face beside the skill's
  own faces.
- `packages/README.md` whole: the authoritative `package.mk` reference,
  the late-binding rule `tools/pkgcheck` enforces, the hook functions, the
  patch directories and `PKG_PATCH_DIRS`, the `PKG_SHA256` requirement.
  Then `packaging-and-patches.md` (its `paths:` glob matches every file of
  this slice: fields, late binding, how a patch is produced and scoped per
  device).
- Rules whose `paths:` match or whose subject is this slice:
  `device-builds.md` (§ Our devices: the four the fork builds; § After
  rebasing onto upstream, item 3: an override that sources the generic
  recipe and the `calculate_stamp` trap; § A metadata-only upstream change
  still rebuilds everything; § Late binding bites hardest in a merge,
  `ppsspp-lr`'s own history; § A build that fetches its own dependency,
  `--wrap-mode=nodownload` and the question cmake's `FetchContent` leaves;
  § A link error the source contradicts is the compile cache's; § Iterating
  on EmulationStation only for its `strings` check of what a binary carries);
  `generic-x64-vm-testing.md` (§ Headless; § A launch, a START or a walk
  waits for the interface to be idle, D-QA-057; § A RetroArch frame is
  evidence only when its surface was the panel; § Fixtures for the launch
  path; § Spin a guest down; § After every VM cycle; the `time-to-play`
  paragraph of 2026-10-24: the tool's reboot drops bind mounts); `time-to-play.md`
  whole (the two numbers are this slice's Q5, and RetroArch's start is the
  largest piece of the first); `upgrade-and-install.md` whole (every fix
  answers *Already written*, D-WORKFLOW-050; a core dropped from a device's
  list leaves its saves, states and `retroarch-core-options.cfg` lines on
  every device that carried it); `change-log.md`; `rclone-cloud-sync.md`
  only for § the save layout (the cores' save and state paths are what the
  sync moves, D-CLOUD-* in `es-player-text.md`'s tiers); the four
  EmulationStation rules are the interface's, not this slice's, and T2's
  audit is where the table's consumer is read. Then the every-session set:
  `engineering-practices.md` (§ Change stays inside the fork's lanes,
  D-UI-079; § Check upstream early, D-WORKFLOW-162; § Consider contributing
  every applicable fix upstream, D-WORKFLOW-164/165; § Verify design intent;
  § Verify the artifact; § A name is not a behaviour; § Guards must fail
  closed; § Before deleting a duplicate; § Stop after three fixes; § Nothing
  runs on a person's device; § Never edit a shell tool in flight),
  `bugs-are-agent-first.md`, `vm-first.md`, `issue-tracking.md`,
  `decision-register.md`, `learning-capture.md`, `ceremonies.md`,
  `worktrees.md` (removal; its layout is superseded, § 1), `fork-workflow.md`
  (the PR-by-content recipe this slice's fixes will one day ride; every
  package the fork introduces at its latest release, D-WORKFLOW-024),
  `milestone-phase-naming.md`, `adversarial-council.md`,
  `working-principles.md` (§ Pre-flight: say which rules were read). Known
  stale facts so they do not cost an hour (#640): the legacy paths in
  `worktrees.md`, `device-builds.md`, `instruction-files.md`, `AGENTS.md`;
  `tools/retroarch-wrapper-test`'s default roots (§ 2 group 5, § 5).
- `docs/blindspot-register.md` whole, once (74 entries; **74** is this
  slice's own shape, a fixture or a stub that silently did not engage,
  added with the futro). The entries that
  touch RetroArch and the cores: **38** (a category-level offer read as a
  standing yes: the exit test on the maintainer's device), **39** (a new
  suite that passed over a table of dashes: `time-to-play` on a guest whose
  RetroArch could not draw with the image's driver), **47** (a build that
  fetched its own dependency: pango's cairo; cmake's `FetchContent` in a
  core recipe is the same shape), **48** (an option changed without reading
  the log: four builds rediscovered *keep VIDEO on*), **50** (a log check
  that never asked whose log it was: `/var/log/exec.log`), **54** and **63**
  (a measurement on a guest whose renderer was not the device's; the gl
  driver and `Using resolution` read), **55** (54's own guard read a line
  it had not tied to its launch), **65** (a proof's substitute passed where
  the real input failed: the exit hotkey's fixture); and the general ones a
  reading repeats: 7 (host tools are not the device's), 13 (assumed done),
  30 (a resumed session built on its own summary), 46 (a name read as a
  behaviour), 51 (an open checkbox is a claim), 73 (a monitor of
  completion, not activity).
- Prior audits of these files under `docs/audits/`, **as provenance only**:
  which files were audited, when, at what tier. The skill has no Phase 2.5
  at epic tier and says to trust prior findings there; here the verdicts
  are read after stage B's own Phase 2 is written, compared then, and never
  transcribed into Phase 2 (plan § 7 item 3). The punch lists that name
  them, counted with `grep -c -E 'retroarch|libretro|es_systems|virtual/emulators|rotation-table' 05-punch-list.md`
  (the lane records the count per folder with the command; the coordinator
  did not pre-count them for this slice). **The two slices beside this one
  are the richer provenance**, read after stage B as the same rule says:
  T1's `docs/audits/2026_10_23-epic-m6-os-launch-control-state/` on the
  T1 branch (`git -C /workspace/repos/pixelelated/distribution.worktrees/m6-os-launch-control-state-648 show d3aa6a19c5:<path>`;
  `02-forward-audit.md` § `sources/scripts/runemu.sh` and § `setsettings.sh`
  are how the launcher consumes this slice's table and configuration;
  `04-analysis.md` § Renovation face Q5 has the launch timed on the guest,
  `setsettings.sh` at 127 ms a launch) and T2's
  `docs/audits/2026_10_23-epic-m6-es-launch-path/` on the T2 branch
  (`git -C /workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649 show 7041b0d710:<path>`, its tip at the hand-back; `f16cf7fc28` is its `fixed-at`;
  its `SystemData` rows are how the interface parses `es_systems.cfg`, and
  its D-WORKFLOW-192 seam -- `--netplaymode` and `--mitm-session=` on the
  launch line -- is a token the launch table's `RUNCMD` does not carry and
  the interface appends).
- Decisions by ID, cited and never re-argued. RetroArch itself: D-LAUNCH-001
  to D-LAUNCH-007 (the exit contract `runemu.sh` reads from RetroArch's
  status; the hotkey's one signal; `/var/log/exec.log` one launch's; **the
  Auto slot, patches 0018 and the configuration load, D-LAUNCH-005 and
  D-LAUNCH-007**; the capture after the game, D-LAUNCH-006), D-RA-001 to
  D-RA-004, D-RA-009, D-RA-011, D-RA-021, D-RA-022, D-RA-025, D-RA-034,
  D-RA-035, D-RA-038 (the offline achievements through the proxy in front
  of RetroArch's rcheevos: patches 0011 to 0013 are its toasts and commands),
  D-UI-057, D-UI-069, D-UI-080, D-UI-081, D-UI-083, D-UI-084, D-UI-086,
  D-UI-088, D-UI-097 to D-UI-100, D-UI-103 (the widget patches 0014, 0016,
  0017, 0019: the achievement banner's backdrop, floor, font sizes and
  place; #251, #255), D-QA-022 (`time-to-play --vm` sets the gl driver for
  the run), D-QA-036/037/039/040/042 (the soak on the device; the VM's
  surface at the panel, #263), D-QA-046/047/052, D-INFRA-010 (the launch
  log's redaction), D-CLOUD-130, D-UI-042/045, D-UI-079 (change stays inside
  the fork's lanes: a player-visible behaviour change to an upstream
  surface -- a core's default option, a device's `retroarch.cfg` value -- is
  put to the maintainer first through the coordinator; a defect or cruft in
  upstream-carried code is this program's to find and fix, #339's Tier 2
  words: *"there is no longer anyone to send them to"*), D-WORKFLOW-015,
  D-WORKFLOW-024 (a package the fork introduces at its latest release, or
  the recipe says why), D-WORKFLOW-050 (*Already written*),
  D-WORKFLOW-054/055, D-WORKFLOW-078, D-WORKFLOW-081/082/083,
  D-WORKFLOW-102, D-WORKFLOW-192 (the netplay seam). The program:
  D-WORKFLOW-181, 183, 184, 185, 186, 187, 189, 190; D-WORKFLOW-137 (depth
  and the reviewer's lab), D-WORKFLOW-049 (every seat through the
  Facilitator), D-WORKFLOW-162 (check upstream early: libretro's trackers
  and ROCKNIX's), D-WORKFLOW-164/165 (consider contributing a fix upstream;
  submissions deferred; #585 is the queue), D-WORKFLOW-132 and D-QA-012,
  D-WORKFLOW-149, D-QA-007/015, D-QA-021, D-QA-044/045/051.
  `grep -iE 'retroarch|libretro|es_systems' docs/decision-register.md`
  matches 37 rows (61 ID mentions) on 2026-10-24; the list above is the subset a reading of
  this slice re-derives from, not the whole.
- Issues whose bodies name these files, read for the planned changes and
  the known leads, not as a work queue. **Open:** #336 (the libretro runner;
  its Step 1 is why this slice is third, and § 4 draws its line), #762
  (Kronos's core options written where RetroArch does not read them: a
  defect in the table's neighbourhood, filed by T1), #598 (Backlog: compare
  the standalone emulators with the shipped cores and review defaults --
  T30's and this slice's shared question; read, do not take), #196 (the
  save state manager and RetroArch's exit auto save), #369 (parked: offer
  the fork's generic fixes to their own projects, RetroArch's among them;
  #585 is the live queue), #263 (GENERIC_X64: RetroArch's surface is the
  core's size scaled by sway), #264 (`tools/retroarch-syntax-check`,
  proposed, not built: a lead for § 5), #255 and #251 (the widget font
  sizes and the sign-in banner: the fork's patches 0014 to 0019), #79 (the
  emulator crash list), #10 (save states across build families), #21 and
  #24 (the capture's core-pins file and the conflict adapter: what the
  cores' state files mean to the sync), #163 (the offline achievements
  epic), #585 (the upstream contribution queue), #644 and #645 (the
  build-path read: its findings on recipes and the build engine ride T5,
  not this slice), #648 (T1, accepted: #702, #707, #708, #727, #730, #732
  are the launcher's side of the launch line), #649 (T2, accepted). **Closed,
  read for their history on these files:** #211 (the doubled posted command
  that crashed RetroArch on a handheld; patches 0011 and 0015;
  `tools/retroarch-wrapper-test`), #16 (the GENERIC_X64 build and its
  `X64_SKIP_CORES`; closed, still named in the recipe's comment), #226 (a
  dependency fetched at build time), #117 (the exit hotkey), #90 and #92
  (exit codes), #227 (`fork-package-freshness`); and two **open** ones read
  for the same history: #228 (webkitgtk held at 2.52.6; the compile cache's
  stale PCH is `device-builds.md`'s lesson) and #120 (the VM runner epic,
  whose exit-path cell is `tools/emulator-exit-test`). Every `gh` call carries
  `--repo pixelelated/distribution`.

## 4. The questions

All seven apply to this slice (plan § 4); none is struck. Provenance decides
the lens (plan § 3): the 24 fork-own paths and the 8 fork-written patches
get all seven in full; the 299 upstream-carried paths and the 13 upstream
patches get **Q4 and Q6 first**, and the rest only where the file stays and
a lead points at it: an upstream-carried recipe's Q1, Q2, Q3 and Q7 cells
read `n/a: upstream's recipe, unchanged here` unless its Q4 or Q6 row keeps
the file in question or a Q3 lead names it, and criterion 7 accepts that
cell (the futro's pre-mortem: sixty style items on 120 recipes nobody
changes is the failure this prevents). The slice's kind is **currency** (`slices.json`), so
Q4 is the question the whole slice answers before any other. Per file, the
evidence that answers each:

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | A recipe idiom the rest of the tree has moved past: `make_target` with a hand-rolled status echo after each `make` where the build engine already fails the package on a non-zero exit (RetroArch's 92 to 100); `PKG_TOOLCHAIN="manual"` where a standard toolchain would do; options a current RetroArch no longer reads (`retroarch.cfg` keys renamed or retired between the pin and the configuration's last edit); a `case ${DEVICE}` list repeated where a device option would carry it; Python 2 remnants or hand-rolled parsing in the two rotation tables; a `*.sh` installer that re-implements what `curl`, `tar` or the package manager do | the replacement named with its commit or its upstream line; a RetroArch option checked against the pin's `retroarch.cfg` defaults (`$B/build/retroarch-<pin>/retroarch.cfg`, read-only) |
| Q2 Standards | `packages/README.md` and `packaging-and-patches.md`, cited by section: late binding (`tools/pkgcheck <pkg>` on **every** recipe the § 5 loop finds, 152 runs: the 151 `package.mk` under `emulators/libretro/` as the glob lists them, the five outside the membership included and recorded as T24's, plus `emulators`; the loop and its counts recorded); the full-hash pin (the seven that are not, § 2 group 4); `PKG_SHA256` present and matching the pin's tarball where the recipe names a tarball URL; the copyright header with its JELOS/LibreELEC origin and a ROCKNIX line; a patch scoped per device under `patches/<DEVICE>/` where it is device-specific; quoting in `virtual/emulators/package.mk` and the 24 `*.sh` (shellcheck under § 5, each error read at its site before it is a finding, as T1 did); `set -euo pipefail` where the interpreter is bash | the rule and section cited; `pkgcheck`'s output per recipe; shellcheck's line with the lane's verdict |
| Q3 Bugs | Where each unit fails: a recipe that builds on the host and not for the device (an arm-only path, the `build.${DISTRONAME}-${DEVICE}.arm` copy at RetroArch 106 to 116 when the arm root is absent); a core in a device's `LIBRETRO_CORES` whose `add_emu_core` line names another emulator or no system; a system in `add_es_system` whose `config/emulators/<system>.conf` is missing; `mk_es_systems`'s silenced `xmlstarlet`; a `retroarch.cfg` value the device cannot honour (the GENERIC_X64 set against the guest, #263's history); a `*.sh` installer's failure path (`Install Steam.sh` at 2,755 lines: every `set -e` exit and every network failure, the host's answer being a lead and the guest's the proof); the rotation tables' parsing (their four September fixes say where they were wrong); #762's shape repeated for another core's options | a reproduction on the VM or a trace with file:line; the code-auditor evidence floor applies (host reasoning about device behaviour is a lead, not evidence); the generated `es_systems.cfg` on the image diffed against what the table says it should hold |
| Q4 Package currency | **The slice's question.** Three readings, each a table in `04`: (a) **the fork against ROCKNIX**: every recipe's `PKG_VERSION` against `upstream/next`'s (one differs on 2026-10-24, `np2kai-lr`), and the 14 commits of `c445081a59..upstream/next` on the two directories dispositioned one by one (merged already / not applicable to this fork / to merge, with the reason; the absent `retroarch-0100-ffmpeg9-lavc63.patch` and `af70bd435b`'s dependency change among them), merges included and dispositioned as `merge`; (b) **the pins against the projects**: for each of the 151 recipes, the pinned commit's date and the project's default-branch head date from the GitHub API (148 of them: `gh api repos/<owner>/<repo>/commits/<pin> --jq .commit.committer.date` and `gh api repos/<owner>/<repo>/commits?per_page=1 --jq '.[0].commit.committer.date'`; the three others by hand, with the date checked), the difference in days, and **a class per row, never an empty cell** (the script asserts every row has one before it writes the table; an empty cell is the scan's own FAIL, blindspot 39): `current`; `behind-upstream` (ROCKNIX's `upstream/next` carries a newer pin: **actionable**, the disposition `to merge` with the upstream commit named); `behind-project` (the project is ahead of both ROCKNIX and the fork: **informational** for an upstream-carried recipe, ROCKNIX's to take; a line on #585 only where the fork introduced or changed the recipe); `upstream-same` beside either; `pin-not-on-project` (the pin's commit is not on the project's default branch: a fork's hash or a force-push, the recipe's `PKG_SITE` read for which); `repo-missing` (the API answers 404: moved, renamed or archived, the `PKG_SITE` quoted). A `to merge` of a core bump names the core's own changelog or commit range read for save, state and option-format changes, cites #10, and is **never applied on this branch** (§ 5): the stream brief decides a bump, because a bump is a build. The script that produces the table is committed under the audit folder with its run's date; (c) **RetroArch itself**: the pin `bdba046fa6` (2026-06-06) against `libretro/RetroArch`'s master head and against its releases (`v1.22.2`, 2025-11-20, is the last; the pin is after it), with the eight fork patches re-tried against master for whether each still applies: the files each patch touches at the pin are fetched from master through the API (`gh api repos/libretro/RetroArch/contents/<path>?ref=master --jq .content | base64 -d`, into a scratch directory of their own under `.qa-scratch/`), and `patch -p1 --dry-run` is run per patch against them; no clone, no build, nothing written in a worktree | the three tables with their commands and dates; the fetch's hash recorded; `tools/fork-package-freshness` run once and its `--list` recorded to show it covers none of this slice |
| Q5 Efficiency | What the slice costs the player at launch and exit, which is where RetroArch's start sits (`time-to-play.md`; D-CLOUD-098): the two numbers on the guest beside T1's (0.73 s and 1.01 s with the tree's scripts, `--quick`, n=1; 0.64 s median of three, mean 0.67, max 0.76, and 1.01 s with the image's, `--repeat 3`) and #336's baseline (1.05 s and 2.03 s); the GENERIC_X64 `retroarch.cfg` already carries `video_driver = "gl"`, so `--vm`'s driver switch is a no-op on this image and the row says so; then what in the configuration moves them -- the GENERIC_X64 `retroarch.cfg`'s 855 lines read for the settings that cost at start (`video_shader_enable`, `rewind_enable`, `run_ahead_enabled`, `menu_*` scanning, `audio_latency`, `netplay_*`, `cheevos_*`, `content_history_size`, the core-updater URLs) with each one's cost measured where it can be (toggle, launch, read `time-to-play`'s number again) or named as unmeasured; the cores' build options (`-O` levels, LTO, `PKG_MAKE_OPTS_TARGET`) as leads for a build this lane does not run; at boot, the five `tmp-*.mount` units RetroArch enables | a measurement on the VM (`tools/time-to-play --vm`) or the named absence of one; the configuration key, its value on the image and the pin's default beside it |
| Q6 Dead ends | Is each unit reached: **by an image the fork builds** (the four devices, `device-builds.md`: a core in no built device's `LIBRETRO_CORES` after the `X64_SKIP_CORES` subtraction is unreached on every fork image -- a row each, with `Already written:` for what the core left on devices that carried it under an earlier image, and the upstream device lists that still reach it, because the fork merges upstream through them, D-WORKFLOW-185's shape, not a removal), **by the table** (a core built but named by no `add_emu_core` line; an `add_emu_core` line whose core is in no device's list; a system with no core; the five recipes outside the membership named as T24's), **by a player path** (a `sources/*.sh` whose emulator is in no built device's `PKG_EMUS`; a `retroarch.cfg` key RetroArch at the pin no longer reads; a `sources/<DEVICE>/` directory for a device the fork does not build -- ten of fifteen -- kept for upstream, a row each); **by the interface** (the five tokens the table emits against the ten the interface expands, T2's list, a row per token; the overlay files the interface reads before the table, `es_systems_custom.cfg` and `es_systems_*.cfg`); the recipe comment naming the closed #16 | the reachability table in `04` Q6: one row per `*-lr` recipe (131) with the devices whose list carries it, one per `add_es_system` system (142) with its cores and its `.conf`, one per `sources/*.sh` (24), one per `sources/<DEVICE>/` (15), one per RetroArch patch (21) with the source file it touches at the pin; one per `%TOKEN%` (the five the table emits and the five the interface expands that it does not); the search commands and their output; the generated `es_systems.cfg` from the image (§ 5) as the cross-check; **every count is compared with its differences listed, never asserted equal** (a recipe may install two `.so` or none; the 116 cores on the image against the recipe's list for GENERIC_X64 is a diff, not an equation) |
| Q7 Clarity | Can a reader new to it tell what each unit does and why in one pass: `virtual/emulators/package.mk` at 1,777 lines with a 1,630-line `makeinstall_target` (one responsibility or three: the device lists, the table, the directories); `Install Steam.sh` at 2,755 lines; a recipe whose comment names a closed issue (#16) or a retired path; copies of logic (the three `[ $? -eq 0 ] && echo` blocks; the fifteen per-device `retroarch.cfg` files, fourteen of 817 to 894 lines and AMD64's of 3,530 -- how many lines differ between any two, and whether a device file is a diff against a base in disguise); headers that say where a recipe came from | the specific unit named with what a reader stumbles on; a duplicate named with its original and the diff's size |

A finding is one question with its evidence; severity and category are the
code-auditor's, with `Renovation` as the category for Q1, Q5, Q6 and Q7
items that are not defects. A Q3 finding that is a defect is also a `bug`
issue (D-WORKFLOW-187, § 1), filed with the VM artifact that would close it.

**The #336 line.** #336 Step 1 puts a headless libretro runner (minarch
stripped of its menu, with `rc_client` and a control socket) under the
launcher **for the 2D cores**, in place of RetroArch; *"RetroArch stays the
runner for the GL cores and for netplay; the choice is per core in the
launcher, and ES does not know which ran."* Step 3, later, is the
in-process bridge. So Step 1 retires, for the 2D cores only, RetroArch's
menu and widget surface (the fork's patches 0014, 0016, 0017 and 0019 draw
the achievement banner there; 0001 to 0009 size and hide upstream's menu),
its `retroarch.cfg` as the per-game store, and the `--core=`/`--emulator=`
contract `runemu.sh` reads -- and retires nothing of the cores' recipes,
their pins, their options files or the launch table, which the runner
would read as RetroArch does. Q1, Q5 and Q7 findings confined to
RetroArch's menu and widget surface and to its configuration keys for that
surface are recorded on the punch list like any other and carried as
`deferred:#336` at Phase 7 unless the coordinator's stream brief says
otherwise; Q2 and Q3 findings there are fixed regardless, because a player
has them today (D-WORKFLOW-187); every Q4 and Q6 finding is this slice's
in full, because the cores and the table outlive the runner question.
Phase 1 reads #336's body to draw the line, and `01-research-notes.md`
§ Scope records where it was drawn.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict, as its `SKILL.md`
§ Evidence floor lists them:

1. *Tracker state is never sole evidence.* Issue state, checked AC boxes,
   and retro summaries may corroborate but can never be the ONLY evidence
   for a PASS; every PASS cites at least one primary artifact (file:line,
   executed command output, or commit diff).
2. *Mechanical evidence outranks reading.* Where a check exists, RUN it and
   record the command, exit status and counts in the criterion entry.
3. *Run it on a device, not on the host.* A verdict about runtime behaviour
   needs evidence from the target: a VM from `generic-x64-vm`, or hardware.
   Host-side reasoning about a device-side behaviour is a lead, never
   evidence. **A recipe's behaviour is a build's**, and this lane builds
   nothing (D-WORKFLOW-183): a claim about what a recipe installs is proven
   on the image the recipe produced (§ The image, below), a claim about what
   it would install after a fix is a lead for the coordinator's integration
   build and the hand-back says so per fix (plan § 6b stage H).
4. *An assertion that cannot fail is not evidence.* Before recording a PASS,
   ask what result would have produced a FAIL.
5. *Subagent output is a LEAD, never EVIDENCE.* Every fact that supports a
   verdict is re-read from the primary artifact before the verdict is
   written. Fan-out inside this lane is read-only research subagents only
   (D-WORKFLOW-183).

**What runs on the VM, and how.** Can this be done on the VM? **Yes**, for
every behaviour claim about what the image carries and how RetroArch starts:
the GENERIC_X64 image was built from these recipes and this table, runs the
same RetroArch binary (x86_64), the same `runemu.sh` and the same 640x480
panel as a handheld (`vm-first.md`), and the lane's fixture ROMs launch
through the launcher on it. **Where the guest cannot show it**, the claim is
a lead, written as such: a device-specific `sources/<DEVICE>/retroarch.cfg`
other than GENERIC_X64's (the values are read, their effect on that panel
is not measured), an arm-only recipe branch (the 32-bit RetroArch and the
`EMUS_32BIT` cores), a GL or GLES driver path the guest's software renderer
has not got (D-QA-022: `--vm` sets gl; blindspots 54 and 63), a core the
GENERIC_X64 build skips (`X64_SKIP_CORES`) or that has no x86_64 build at
all. Nothing in this slice touches a handheld, a person's cloud, a shared
QA backend, or a QA guest another lane owns.

- **The host handoff comes first, and it is a wait, not a stop.** The
  agreement in `/tmp/m7-m6-host-coordination-20261023.txt` is that **M6
  starts no runtime of any kind (no guest, no compiler, no `npm install`)
  while an M7 window is open; the coordinator's comment on #650 relaying
  M7's `resource return` is the signal this lane acts on**, and the file's
  last `== M7` block is read before any runtime (the first commands print
  it). On 2026-10-24 the M7 lane held the host from 01:33 (requested 01:27)
  to its return at 02:22 for its H700 and SM8550 image builds; the next
  window is requested the same way and may be open at dispatch.
  Stage A's reading, the counts, the branch scan, the three Q4 tables'
  commands against GitHub (API calls, not host runtime), `pkgcheck` over the
  recipes and shellcheck need nothing of the host's memory and run now;
  the guest, the unit-test compile of nothing (this slice compiles nothing
  of its own) and `tools/retroarch-wrapper-test`'s compile wait for the
  comment and run in that order when it comes.
- **The image.** Do not build one (D-WORKFLOW-183: lanes deliver branches;
  nothing in M6 builds). Use the GENERIC_X64 image the M7 lane built on
  2026-10-23 at
  `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`
  (2,122,289,964 bytes; source `069fc2704421`; its BUILD_ID
  `069fc270442134fe771258418adf4e666e0473fb` is read from the guest's
  `/etc/os-release` and recorded in `00-running-log.md`; the T1 and T2
  lanes keep copies under `/workspace/artifacts/m6-t1-20261023/` and
  `/workspace/artifacts/m6-t2-20261023/`, read-only to this lane). The M7 window of 2026-10-24 built H700 and SM8550, not GENERIC_X64, so this
  image stands; **if a newer GENERIC_X64 image exists by dispatch, the
  dispatch comment names it instead**; the brief's hashes are the older
  image's and the lane records the one it used. Copy the `.img.gz`, its
  `.sha256` and the `.identity.json` beside it into this lane's own
  artifacts directory first (a fresh `ROCKNIX_ARTIFACTS=/workspace/artifacts/m6-t3-<date>`;
  `sha256sum -c` on the copy; the `.tar` is not needed, no update runs
  here); never write in the M7 worktree. **The installed set is read first on the
  host**, from the build root's `image/system` (§ 2: the cores, the table
  at `usr/config/emulationstation/es_systems.cfg`, the configuration, the
  modules, the binary), with the counts of 2026-10-24 (116 cores, 128
  systems, 152 emulator elements, 500 core elements, 19 modules) as the
  baseline the lane re-derives; the `.tar` in `target/` holds the same
  `SYSTEM` for `unsquashfs -ll` if a listing with modes is wanted. **The
  guest is for what runs**: a launch, a `retroarch.cfg` the running
  RetroArch honours, a module script's behaviour, `time-to-play`. Then `generic-x64-vm-testing.md`
  § Headless: `gunzip`, `qemu-img convert` to qcow2, `qemu-img resize ...
  16G` (not optional), `projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm
  run --headless --daemonize` **with the lane's own instance paths and
  ports**: `--pidfile $ROCKNIX_ARTIFACTS/qemu.pid --serial
  $ROCKNIX_ARTIFACTS/serial.sock --monitor $ROCKNIX_ARTIFACTS/monitor.sock
  --vnc 21 --ssh-port 10034` (T1's guest held display 19 and port 10032,
  T2's display 20 and port 10033; both are down and stay down, but the
  numbers are theirs; the defaults `/tmp/rocknix-qemu.pid`,
  `/tmp/rocknix-qemu-serial.sock`, `/tmp/rocknix-qemu-monitor.sock`, display
  9 and port 10022 are shared with every other lane's guest; `pgrep -f
  'qemu-system-x86_6[4]' | wc -l` before starting, and `ss -ltn` for the
  port). `$D/tools/vm-serial --socket $ROCKNIX_ARTIFACTS/serial.sock wait`,
  then one root command at a time through `$D/tools/vm-serial --socket ...
  sh '<command>'` (it runs one command line; it is not an interactive
  shell). Provision an SSH key over serial as § Headless shows (the key
  lives under `$ROCKNIX_ARTIFACTS`, never in a tree). Stop the guest by its
  pidfile with `tools/vm-stop $ROCKNIX_ARTIFACTS/qemu.pid <the qcow2>`,
  never by pattern (§ Spin a guest down), and bring it up for a job and
  down when the job ends: the host is shared. Every VM cycle writes its row
  in `docs/vm-qa-log.md` (§ After every VM cycle).
- **The image is the tree, for the installed set.** The image was built
  from `next` at `069fc2704421`, whose two directories equal `8ebaf8daad`'s
  except the M7 lane's `Install Steam.sh` hunk (§ 2; `git -C
  /workspace/repos/rocknix diff --stat next 069fc2704421 -- <the two
  directories>` prints that one file), so what the guest carries under
  `/usr/lib/libretro`, `/etc/emulationstation/es_systems.cfg`,
  `/usr/config/retroarch` and `/usr/config/modules` is what the recipes at
  the read hash install, for GENERIC_X64. Record once, in
  `01-research-notes.md`: the core count on the guest (`ls
  /usr/lib/libretro/*_libretro.so | wc -l`) against the recipe's
  `LIBRETRO_CORES` for GENERIC_X64 after `X64_SKIP_CORES`; the `<system>`
  count in the generated `es_systems.cfg` against the `add_es_system` calls
  that run for the device; `/usr/config/retroarch/retroarch.cfg`'s sha256
  against the tree's `sources/GENERIC_X64/retroarch.cfg`; the installed
  `/usr/config/modules/*.sh` against the 24 sources. **A fix changes
  that**: an edited recipe or table has no image until the coordinator's
  integration build (§ 6, stage F). Until then a fix's evidence is
  `pkgcheck`, the reading, the generated-table check where it can be
  re-run on the host (`mk_es_systems`'s inputs are shell, so the lane may
  run `add_emu_core`/`add_es_system`/`mk_es_systems` from
  `distributions/ROCKNIX/config/functions` in a sandbox with `ESTMP` set
  to a scratch directory and `ROOT` to the worktree, and diff the output
  against the image's table: a host run of the build's own shell, recorded
  as such), and the walk written for the first image that carries it; the
  proof on the guest is the coordinator's at that image, and the hand-back
  says so per fix.
- **Stage A's tool trials** (after the return line). Run
  `$D/tools/time-to-play` once against this single guest before the Q5
  measurements, and record in `00-running-log.md` that it works without
  `tools/vm-pair`. Its defaults differ from this lane's: it defaults to port
  10022, so every call carries `--port 10034 --identity <key> --monitor
  $ROCKNIX_ARTIFACTS/monitor.sock --out <a directory under $ROCKNIX_ARTIFACTS>`,
  takes `--vm` (RetroArch to the gl driver for the run, restored after; the
  guest has no Vulkan; D-QA-022), `--no-configure-remote` (it would otherwise
  set up a QA cloud remote through `tools/cloud-test-backend`, a shared
  backend this slice has no business in) and `--only launch,exit,g2g
  --repeat 3` (the default cell list adds `startup`, which reboots the
  guest, and `offline` and `bounds`, which call the backend); T1 ran it
  with `--quick` too. Without a cloud the report ends `Not a pass` through
  `headline_missing` ("the exit sync had no cloud to reach"): the launch
  and g2g numbers are still the measurement, recorded with that line and
  T1's caveat (the exit sync skips at once, so the second number is not
  like for like with a configured device). **It reboots the guest when it
  seeds its ROM or changes the two cloud settings**
  (`generic-x64-vm-testing.md`, 2026-10-24): a measurement
  of a changed `retroarch.cfg` or table copies the file into place under
  `/storage` or binds it from a `/storage/.config/autostart/` hook, and
  reads the installed file's hash after the run (#797 is the flag that
  will do this). `tools/emulator-exit-test` is T1's check of the launcher;
  it is useful here only as a fixture factory: its recipe builds a 32 KiB
  Game Boy cartridge the guest can launch through `gambatte`
  (`$D/tools/emulator-exit-test --help` names the recipe; T1's running log
  calls the cartridge `T1 Verify.gb`). `$D/tools/ra-candidate-games` names
  homebrew titles with achievement sets, a second fixture source for a
  core that needs a real title; a fixture is placed under
  `/storage/roms/<system>/` on the guest by this lane and removed after.
- **The host-side checks that exist for these sources**, each run and its
  command, exit status and summary line recorded in `02-forward-audit.md`;
  a check that cannot run is recorded as such, never as a pass (each block
  sets its variables; the tools are `$D`'s, by absolute path):
  ```bash
  D=/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-libretro-650
  cd "$D"
  for f in $(git ls-files 'projects/ROCKNIX/packages/emulators/libretro/*/package.mk' 'projects/ROCKNIX/packages/emulators/libretro/*/*/package.mk' projects/ROCKNIX/packages/virtual/emulators/package.mk); do
    p=$(basename "$(dirname "$f")"); out=$("$D/tools/pkgcheck" "$p" 2>&1); rc=$?; printf '%s %s %s\n' "$rc" "$p" "$(echo "$out" | grep -c -i fail)"
  done | sort | uniq -c | sort -rn | head            # pkgcheck over every recipe: 152 runs (151 + emulators); record the rc counts and every non-zero line, and the path each run printed: the tool checks every `*/<name>/package.mk` under packages/ and projects/ (its line 157) and prints each, so a second path is a second row; on next the three easyrpg-lr sub-recipes print only their own path and `emulators` prints its one path twice
  "$D/tools/fork-package-freshness" --list | tr ' ' '\n' | grep -E 'emulators/' # aethersx2-sa only, T30's: the tool covers none of this slice; record that line
  ```
  - **shellcheck** is not installed on the host. T1 downloaded the
    release `shellcheck-v0.11.0` into its `.qa-scratch/` (gitignored) and
    ran `shellcheck -f gcc <file>` over its shell files with each file's
    own shebang (`-s bash` for a sourced fragment without one); do the
    same (a download into its own empty directory under `.qa-scratch/`,
    `sha256sum` against the release's published sum recorded, run by
    path, never from inside the download's directory) over
    `virtual/emulators/package.mk`, `functions` 99 to 140 lifted into a
    scratch file, the 24 `sources/*.sh`, `scripts/mkcontroller`,
    `autostart/001-controller`, RetroArch's `autostart/003-logging` and
    `scripts/call_achievements_hooks.sh`; every error is read at its site
    before it is a finding, as T1's `02` § shellcheck errors does;
  - **`tools/retroarch-wrapper-test`**, the closing check `slices.json`
    names for this slice (a compile: after the return line). Its default
    roots are absent on this host (§ 2 group 5), so until the lane's fix
    is on the branch it takes the explicit path, read-only from the M7
    GENERIC_X64 root:
    ```bash
    D=/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-libretro-650
    B=/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64
    python3 -I "$D/tools/retroarch-wrapper-test" "$B/build/retroarch-bdba046fa6766380bc2457532f38e589df769aaf/gfx/video_thread_wrapper.c"          # expected: posted 2000 command(s); the method ran 2000 time(s)  PASS
    python3 -I "$D/tools/retroarch-wrapper-test" "$B/build/retroarch-bdba046fa6766380bc2457532f38e589df769aaf/gfx/video_thread_wrapper.c" --gated  # read the tool's docstring for what --gated asserts before trusting either line
    ```
    (the H700 roots at `/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-03/build.pixelelated-H700.aarch64/build/retroarch-<pin>/gfx/video_thread_wrapper.c`
    and `m7-signin-h700-build-20261023-05/...` carry the same patched
    source; a build root is read, never written; the compile is a host
    `cc` of a few hundred lines);
  - **the pins against the projects** (Q4 b): a script under the audit
    folder, run once with its date recorded, `gh api` only (no clone, no
    download), `GH_PAGER=` set, bounded to the 148 `github.com` recipes and
    the three others by hand; a rate limit hit is recorded, never skipped
    over; the pin's commit may be absent from the project (a force-push, a
    fork's hash): then the row says `pin-not-on-project` and the lane reads
    the recipe's `PKG_SITE` for which fork it is;
  - **a build system that fetches at configure time** (blindspot 47, #226):
    over the build root's unpacked core sources, read-only,
    `grep -rl -E 'FetchContent|ExternalProject_Add|git clone|curl |wget ' $B/build/*-lr-*/CMakeLists.txt $B/build/*-lr-*/Makefile* 2>/dev/null | sort`
    (the pattern recorded with its hits; a hit is a Q3 lead the recipe's
    `--wrap-mode`/`FETCHCONTENT_FULLY_DISCONNECTED` answer or does not);
  - **the rotation tables** (`rotation-table-fba.py`, `rotation-table-mame.py`):
    neither takes `--help` (a wrong argument count prints the usage line;
    anything else is read as a path and the run exits 0 with no table).
    The recipes say how they are called: `python3
    ${PKG_DIR}/../rotation-table-mame.py --min 100 ${PKG_BUILD} src/drivers`
    (`mame2003-plus-lr/package.mk` line 32) and `python3
    ${PKG_DIR}/../rotation-table-fba.py --min 100 ${PKG_BUILD}`
    (`fbneo-lr/package.mk` line 43), the output to
    `${INSTALL}/usr/config/emulationstation/rotation/<core>.txt`. Run each
    the same way against the M7 root's unpacked source
    (`$B/build/mame2003-plus-lr-*/` with its `src/drivers`,
    `$B/build/fbneo-lr-*/`; read-only), the output under
    `$ROCKNIX_ARTIFACTS`, and diff it against the image's
    `usr/config/emulationstation/rotation/<core>.txt` in the install tree,
    recorded as the generators' proof;
  - **the generated table** (Q3, Q6): the image's
    `usr/config/emulationstation/es_systems.cfg` from the build root's
    install tree (it carries no credential), parsed on the host with
    `python3 -I` and `xml.etree.ElementTree` (**`xmllint` and `xmlstarlet`
    are not installed on this host**, checked 2026-10-24), the `<system>`,
    `<emulator>` and `<core>` counts and names listed against the recipe's
    calls for GENERIC_X64 with the differences named; beside it **a host
    regeneration** from the tree's own functions: in a scratch directory
    the lane owns, `bash -e` sourcing `distributions/ROCKNIX/config/functions`
    with `ROOT=$D`, `ESTMP=<scratch>/estmp`, `INSTALL=<scratch>/install`,
    `PKG_DIR=$D/projects/ROCKNIX/packages/virtual/emulators`,
    `DEVICE=GENERIC_X64`, `ARCH=x86_64`, `TARGET_TYPE=` and whatever else
    `makeinstall_target` reads (the lane lists them from the function's
    text first), then the recipe's `makeinstall_target` body; the
    formatted `es_systems.cfg` will be **empty** without `xmlstarlet`, so
    the comparison is of the pre-format `${ESTMP}/.es_systems.cfg` parsed
    with `ElementTree` against the image's, by system, emulator and core
    names; a function that `exit`s (two defaults for one system) is the
    finding, recorded with its line. Nothing of this touches `/usr` or
    `/storage` on the host: every path is the scratch's, and the run is
    recorded as a host run of the build's own shell;
  - **the guest tools above**: `time-to-play` for Q5; `vm-visual-qa` with a
    step file under `tools/vm-walks/` only if a finding needs a frame (a
    RetroArch frame is evidence only when its surface was the panel,
    `generic-x64-vm-testing.md`; the gl driver and `Using resolution` read
    first, blindspots 54, 55, 63);
  - of `tools/vm-qa`'s suites, **`wrapper`** is this slice's (it runs
    `tools/retroarch-wrapper-test`) and **`time-to-play`** its Q5 cell;
    `exit` is T1's, `quoting`, `menumap`, `french`, `vocabulary` T2's. Run
    the two tools directly, as above, rather than through the runner, which
    wants the pair up; record which in `02`.
- **A commit may land in a window with its compile queued.** The only
  compile this slice runs is `tools/retroarch-wrapper-test`'s (and
  `time-to-play`'s guest); `pkgcheck`, shellcheck, the API tables and the
  host regeneration are allowed in a window. A recipe or table commit lands
  with `pkgcheck` done and the running log naming what is queued for the
  return line; the queued check's line is written under the commit's hash
  when it runs (T2's retro asked the template to say which; this is the
  answer for this slice).
- **A Q5 measurement row names the configuration it ran with**: the sha256
  of the guest's `/storage/.config/retroarch/retroarch.cfg` after the run,
  beside the number (blindspots 54, 55, 63; T1's two uncounted runs).
- **A read is free and goes through the filter.** Every line read back from
  the guest, from an image's config, from `rclone.conf`, `system.cfg`,
  `es_settings.cfg` or `get_setting`, passes `grep -v -i -E
  'key|pass|token|user|psk'`, or is masked with `sed -E
  's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'` where the line's
  presence is the evidence (D-QA-021; `engineering-practices.md` § Nothing
  runs on a person's device). `retroarch.cfg` carries `cheevos_username`
  and `cheevos_password` keys and `netplay_nickname`; the guest's copy is
  read through the filter, and a value is never quoted even when empty.
  **The build's own defines are credential-shaped too**: a `ninja -t
  commands` line or a `make` log from a build root carries
  `-DSCREENSCRAPER_DEV_LOGIN=` and must never be pasted into an artifact,
  an issue or a transcript (T2's § 5 learned this; the pre-commit scan
  refuses it).

**What never runs in this slice:** a build of an image or a package (not
even `make docker-package`: a recipe fix's build is the coordinator's);
a credential-shaped line pasted into any artifact, issue or transcript (the
build's defines, a config's values); a command on a handheld, a person's
cloud, a shared QA cloud backend, or a QA guest this lane did not start; a
runtime of any kind while an M7 window is open; an edit to any tool while a
run of it is in flight; `pkill -f` or `kill` by pattern; bare `git stash`;
`git worktree remove --force` or `rm -rf` of any worktree
(`tools/fork-worktree remove`, and only of this lane's own); a write under
`/workspace/repos/rocknix` or any `rocknix.worktrees/*`, or in the P0, P1,
T1 or T2 worktrees (either repository); an edit to
`.github/sessions/saved-session-state-next.md` (the M7 lane's);
`--no-verify` on any push; a model call outside `tools/council/run`; a
credential or the wordlist printed; a merge of another lane's feature
branch to refresh rules (read them from `next`); `tools/renovation-inventory
--slice-issues` or `--order` without `--no-write` in a worktree that is
kept; a change to `docs/reviews/order.md`, `slices.json`, `areas.json`, the
plan, the brief, #650's criteria or the M6 body (the coordinator's,
D-WORKFLOW-189); a pin bump of RetroArch or a core on this branch **as a
fix** without a stream brief that says so (a bump is a build the lane
cannot run; Phase 7 records it as `to merge` or `deferred:` with the
upstream commit named, and the coordinator's stream brief decides); a
GitHub issue other than the audit punch-list issue and `bug` issues (§ 1).

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#650`
(`Refs #650` while any criterion is open, never a closing keyword); the
stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-emulators-libretro/00-running-log.md` | the skill's append-only flight recorder, opened first: the model and effort that ran, `reviewed-at` (the branch `HEAD` at stage A) with `8ebaf8daad` beside it, `upstream/next`'s hash and the merge base the first commands fetch, the host file's state, the image's BUILD_ID, every command with its exit status and time, each stage's entry, every wait; **every guest proof announced on a line that begins `GUEST-PROOF:`** with its time and its script, the token criterion 12 counts | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 344 paths re-derived with the filter of § 2 and the deltas beside the recorded counts (both fork-own figures); the five groups; the interacting subsystems; the branch scan; the M7 delta (one commit) by hunk; the #336 line as drawn; § Phase 1: the closed bugs grep with its pattern and count, the prior audits' counts per folder, upstream's trackers checked (D-WORKFLOW-162: libretro/RetroArch's issues for the eight fork patches' subjects, ROCKNIX's `distribution` PRs for the 14 commits) | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #650's checklist, plus a **coverage table with one row per path** (344 rows; the first cell the path in backticks, so ``grep -c '^| `projects/ROCKNIX/packages/' 02-forward-audit.md`` prints 344; then group, tier, Q1 to Q7 each answered or `n/a` with the reason, and for a fork-own path the fork commits read); § Mechanical checks (every check of § 5 with command, exit status, summary; a check that could not run says why); § Image versus tree (the installed set against the recipes, § 5); § Guest proofs (each saying image or tree, after the recorded diff; each with its `proved:` cell, below) | B onward |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5's interaction audit for the seams § 2 names (the table x `runemu.sh`'s parsing, T1's; the table x `SystemData::loadConfig`, T2's; the per-device `retroarch.cfg` x `setsettings.sh`'s writes; the cores' save paths x the sync's layout; the widget patches x the proxy's toasts) and the futro's predictions checked | B |
| Analysis | `.../04-analysis.md` | Phase 4, then § Finding Verification (4.5), then **§ Renovation face** with one subsection per question Q1 to Q7 (the lint requires all seven), **Q4 carrying the three currency tables** (the fork against ROCKNIX with the 14 dispositions; the 151 pins against the projects with dates and days; RetroArch against master and its releases with the eight patches' `--check` results), Q6 the five reachability tables, Q5 the measurements beside T1's and #336's, then § Second opinions (4.6) with the two seats' leads re-read | B, C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (written before the first call), `<member>-brief.md`, the outputs, each call's `provenance.json`; the probe of each seat | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | prints `PASS pre-issue artifacts (does not certify resolution)`; recorded in the running log | C to D |
| Punch list | `.../05-punch-list.md` | Phase 5, every item with `question: Q1..Q7` (or `none` with a reason), severity, category (`Renovation` where it is not a defect), where (file:line at `8ebaf8daad`), acceptance; the YAML `punch_index` (`templates.md`); #336-line items marked for `deferred:#336`; findings on `Install Steam.sh` marked for `deferred:M7-merge` (the M7 lane's `6101242e14` changes the file; the coordinator re-opens them over the merged file, plan § 8); a pin bump marked `to merge` with the upstream commit or the project's commit named; a removal with `removal: yes` and its `Already written:` | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #650 | `Audit: M6 T3 RetroArch and the libretro cores -- N findings (X critical, Y high)`; one checkbox per item, each agent-verifiable (D-QA-044); `tools/box-check --issue N` run on it and its line recorded | D |
| Bug issues | GitHub, label `bug`, title `Bug: ...` (`milestone-phase-naming.md` § Reactive), milestone-less and not sub-issues (T1's and T2's shape) | one per defect (D-WORKFLOW-187, D-QA-051): the code trace shape (`release-candidates.md` step 0), the `Can this be done on the VM?` line, a VM-verifiable criterion, `Already written:`; the wrapper test's retired roots is the first, at stage A | A (the tool), D |
| **The stage-D pause** | #650 | the punch list posted on #650 with the audit issue's number and the `bug` issues' numbers; **the lane waits** while the coordinator writes one remediation brief per stream of related items (plan § 6b stage E: the D-WORKFLOW-056 shape, the files owned, the test first, the `Already written:` line, commits cut from intermediates only after a green run, a stub or a fixture part of the claim; D-WORKFLOW-189) | D to E |
| Remediation | the branches the stream briefs name | each stream as its brief specifies: a recipe or table change with `pkgcheck` first and the host regeneration of the table where it applies, a `*.sh` change with its shellcheck line and a guest run of the changed path where the guest can run it, a configuration change with its measurement; a `bug` issue's fix carries its `Already written:` and names its two runs | E |
| Verification | `02-forward-audit.md` appended; `.../audit-completion.json` | every behaviour claim proven on the guest where the image can show it (§ 5), the VM cycle's row in `docs/vm-qa-log.md`; every guest proof's row carries a `proved:` cell with one of `image-set` (the installed set at `069fc2704421`, equal to the tree's for this slice), `fix-host-regen` (a table or recipe fix proven by the host regeneration and `pkgcheck`; the image is the coordinator's), `fix-guest-copy` (a configuration or `*.sh` fix proven by copying the file onto the guest), `fix-pending-image` (nothing but an image can show it: the coordinator proves it at the first image after the merge, plan § 6b stage H), or `fix-walk-pending-image` where the fix comes with a walk under `tools/vm-walks/` for the coordinator to run on that image (plan § 6b H; none is expected in this slice); the Phase 7 gate in `05` | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-emulators-libretro.md`, and the same text as a comment on #650 | the mini-retro skill's four answers with its scoped audit, in Instruction-Recommendations mode (plan § 6b G: the scope is epic tier); findings that recur become a rule edit, a tool, a blindspot entry; **what the slice did to the two time-to-play numbers** | G |
| Hand-back | #650 | `reviewed-at:` (the branch `HEAD` at stage A) and `fixed-at:` (the branch's last commit on the slice's paths) written into #650's body by the executor; one comment naming the branch tip and each artifact by path, the six checker exit codes, and per fix its `proved:` class | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-emulators-libretro-650.md` | seeded by the coordinator; the executor updates it at every checkpoint: start here, the worktree, current focus, the stage reached, next commands, merge notes | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session, headed `#650` and the thing decided or learned | every session |

Neither `tools/renovation-status` nor `tools/renovation-drift` nor
`tools/renovation-inventory` is run to write ledgers or edited here; a
defect in one is a lead on #650 (they are P1's tools, documented in
`docs/reviews/README.md`).

## 7. Acceptance

The checklist on #650 is the contract. Its first five items are plan § 6b's
contract for every slice; the rest are this slice's, written by the
coordinator with this brief (D-WORKFLOW-189). Each names the artifact that
ticks it; the coordinator ticks them at hand-back from the artifacts, not
from this lane's word.

- [ ] `docs/audits/<date>-epic-m6-emulators-libretro/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-emulators-libretro/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included: Q1 to Q7 answered in `04-analysis.md`, and every punch item's `question:` in the index.
- [ ] `second-opinions/review-plan.json` records Extended depth and two reviewers from two other labs, and each reviewer's provenance names its served model (plan § 6c, D-WORKFLOW-137).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue, or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits the read and the fixes were made at (the read made with the slice's bytes equal to `next`'s `8ebaf8daad`, the branch on the P1 tip; no EmulationStation path here, so no `fixed-at-es:`), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed` (the coordinator's regeneration).
- [ ] `01-research-notes.md` § Scope records the read hash `8ebaf8daad`, the filter of brief § 2 with its output (344 paths, 31,961 lines, 24 fork-own with 6,557 lines, 299 upstream-carried, 21 vendor-carried with 1,670 lines, or the deltas beside them, and the order row's 5,519 explained), the image's BUILD_ID, the M7 delta (`next..069fc2704421` on the two directories) by hunk, and the #336 line as drawn.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c '^| `projects/ROCKNIX/packages/' 02-forward-audit.md`` prints 344; each row's Q1 to Q7 cells answered or `n/a` with a reason (`n/a: upstream's recipe, unchanged here` is a reason for an upstream-carried recipe's Q1, Q2, Q3 and Q7 cells, § 4).
- [ ] `02-forward-audit.md` records, with command, exit status and summary line, each of: `tools/pkgcheck` over every recipe in the membership (152 runs, the path each printed, the non-zero lines listed), shellcheck over the shell sources named in § 5, `tools/retroarch-wrapper-test` against the pin's `video_thread_wrapper.c` (plain and `--gated`), the two rotation-table generators against the build root's sources, the `FetchContent` grep over the build root's core sources, the `ElementTree` parse and element counts of the image's `es_systems.cfg` beside the host regeneration's diff, `tools/time-to-play --vm` with the configuration's sha256, and `tools/fork-package-freshness --list`'s line showing it covers none of the slice; a check that could not run is recorded with the reason, never as a pass.
- [ ] `04-analysis.md` § Renovation face Q4 carries the three currency tables: (a) every recipe's pin against `upstream/next`'s with the one difference named, and the 14 commits of `c445081a59..upstream/next` on the two directories each with a disposition (merged / not applicable / to merge, with the reason); (b) one row per recipe (151) with the pin's date, the project's head date, the days between and one class of `current`, `behind-upstream`, `behind-project`, `upstream-same`, `pin-not-on-project`, `repo-missing` (no empty cell; the script's own assertion), produced by a script committed under the audit folder with its run date; every `to merge` of a core bump names the changelog or commit range read and cites #10; (c) RetroArch's pin against master and `v1.22.2`, and `git apply --check` of each of the eight fork patches against master's `video_thread_wrapper.c`, `cheevos`, `gfx/gfx_widgets*` and `command.c`, each result named.
- [ ] `04-analysis.md` § Renovation face Q5 carries the two time-to-play numbers measured on the guest beside T1's (0.73 s and 1.01 s; 0.64 s and 1.01 s) and #336's baseline (1.05 s and 2.03 s), and for every `retroarch.cfg` key named as a cost either a measured difference or the words `not measured` with why.
- [ ] `04-analysis.md` § Renovation face Q6 carries the five reachability tables of brief § 4 (131 `*-lr` recipes with the built devices that carry each; 142 systems with their cores and `.conf`; 24 `sources/*.sh` with the built devices whose `PKG_EMUS` names each; 15 `sources/<DEVICE>/` sets; 21 RetroArch patches with the source each touches), each with its search command and output; every row marked unreached by any fork image carries an `Already written:` line and what the unit exposed; the five recipes outside the membership named as T24's.
- [ ] Every proof on the guest in `02-forward-audit.md` carries a `proved:` cell reading `image-set`, `fix-host-regen`, `fix-guest-copy` or `fix-pending-image` (§ 6, Verification); ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c '^GUEST-PROOF:' 00-running-log.md`` (the convention of § 6: every guest proof is announced in the running log on a line starting with that token).
- [ ] Every punch item whose `punch_index` entry carries a `tracked: "#N"` has that `bug` issue carrying the `Can this be done on the VM?` line and a VM-verifiable criterion; every item whose entry carries `removal: yes` has an `Already written:` line in its row; every pin bump is `to merge` or `deferred:` with the commit named, never applied on this branch without a stream brief; `tools/box-check --issue N` passes on the audit issue and on each `bug` issue this lane files.
- [ ] The retro exists at `docs/retros/<date>-m6-emulators-libretro.md`, is posted on #650, and answers what the slice did to the two time-to-play numbers.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge; the five exit codes pasted on #650.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back, § 10; criterion 5's `renovation-status` clause and
the merge are the coordinator's, so that checkbox is not the lane's to
tick); **the stage-D pause** (the punch list and the
audit issue posted on #650; the lane waits for the coordinator's stream
briefs and does no remediation before them, D-WORKFLOW-189; #650's body
says the same above its checklist); **the Phase 4.6 blocker** (a reviewer
seat failing identity verification, or the route missing after all: the
other pass done, the seat recorded pending, the blocker named on #650, no
Phase 5; § 1); an explicit maintainer pause on #650; any other blocker,
named on #650 with what is needed (a count that cannot be produced or two
commands that disagree; a rule that forbids a step; a guest that will not
boot after the recipes of `generic-x64-vm-testing.md` § Debug order; the
npm install failing; the GitHub API refusing the Q4 scan after a bounded
retry); **a hash mismatch at stage A** (the slice's bytes not `8ebaf8daad`'s,
or the branch not on the P1 tip: the coordinator re-baselines); or an
execution limit, stated as such with the running log current. **The host's
window is a wait, not a stop**: the reading, the counts, the API tables and
the host checks that run no compiler go on, and the wait is in the running
log. A checkpoint is not a stop (D-WORKFLOW-149): write it and take the
next stage. A differing count is a delta, not a stop. `next` moving under
the slice is drift, not a stop. An idle session says it is idle on #650.

## 9. Ceremonies owed

- A work-log entry per session, headed by `#650`; `tools/work-log-index
  --write` after it; the weekly summary if the lane's week falls due
  (`ceremonies.md`; the W43 summary is owed by whoever's record it falls
  in, the coordinator says which on #650).
- A friction line in `docs/friction-log.md` the moment something slows,
  with `issue: #650` or the guard.
- The VM question written before every proof (§ 5 answers it for the slice,
  and names what the guest cannot show; a proof that needs something else
  the guest lacks writes its own line in `02-forward-audit.md`); a row in
  `docs/vm-qa-log.md` per VM cycle.
- The mini-retro skill at stage G, posted on #650, with its scoped audit, in
  Instruction-Recommendations mode.
- A register row the same session for any decision the slice forces (a fork
  resolved, an assumption invalidated). The ID: one above the highest
  `D-WORKFLOW` on every pushed branch (`git grep -ho 'D-WORKFLOW-[0-9]*'
  $(git branch -r --format='%(refname)') -- docs/decision-register.md | sort
  -t- -k3 -n | tail -1`) and in the M7 lane's worktree
  (`/workspace/repos/rocknix.worktrees/m7-player-setup/docs/decision-register.md`);
  on 2026-10-24 the highest Decided row on the coordinator branch is
  D-WORKFLOW-192 (191 is an open row; P1's branch carries 188 and 189; T1's
  and T2's carry 188 to 191; the M7 lane holds 171 to 180 unmerged), so
  **the next Decided row is 193**, checked again on every branch at the
  time. The lane's register is the union the stacked branch gives (P1's 188
  and 189 under the coordinator's 189 to 192), and `tools/register-check`
  runs on the worktree before the first push. A row goes at the end of the
  `## Decided` table, never after `## Open decisions` (`tools/register-check`
  refuses it there, #646).
- `tools/ceremony-check` before every push; what it reports as owed by this
  lane is paid first; what another lane owes is noted on #650. Never
  `--no-verify`. A merge with conflicts is checked for leftover markers
  before it is committed (#696), and a union of two ledgers is made by
  whole entries, never by an unanchored pattern over marker-shaped text.
- Commit messages scoped by package or device as `CLAUDE.md` says
  (`retroarch - ...`, `emulators - es_systems: ...`, `np2kai-lr - bump
  ...`) with `Refs #650` and the bug's number; `docs: ...` for the
  artifacts.
- `change-log.md`'s running log the day a player-visible change lands
  (stage E: a core's default option, a system added or removed from the
  table, a `retroarch.cfg` value).

## 10. Hand-back

The coordinator accepts the slice by reading, in this order, without
re-reviewing it: #650's checkboxes against their artifacts (§ 7); the lint's
`PASS` line on the audit folder; `second-opinions/` (two provenance files
naming two served models from two labs); the audit issue's checkboxes all
at an outcome; the coverage table's row count; `02-forward-audit.md`'s
check lines and the `proved:` cell on each guest proof; **re-running
`tools/pkgcheck` over the membership and the host regeneration of the
table once** rather than trusting the log alone, and
`tools/retroarch-wrapper-test` against the pin's source if the branch
touched a RetroArch patch; the Q4 tables' commands spot-checked (three
rows re-queried); the retro's four answers; the five checker exit codes on
#650 (with `register-check` run on a simulated merge with the coordinator
tip, as T1's acceptance did). The lane posts one hand-back comment on #650
naming the branch tip and each of those artifacts by path, writes
`reviewed-at:` and `fixed-at:` into #650's body, then says it is idle. After
acceptance the coordinator writes the hashes into `slices.json`, merges the
branch in its turn after the M7 candidate (P0, P1, T1, T2, T3), regenerates
the ledgers (§ 6, Hand-back row), and **closes #650 only when the first
image built after the merge has proved each `fix-pending-image` row**
(the slice is `remediating` until then, plan § 6b stage H). A brief that
needed the coordinator's help mid-slice, beyond the stage-D pause, the
Phase 4.6 blocker and the host's return line this brief already names, is a
defect in this brief: log the friction, and the coordinator fixes the
template in plan § 7 before the next brief.

**The two readings before dispatch** (plan § 3, principle 3). The area
epic's futro (`docs/futros/2026-10-24-m6-emulators-and-cores.md`, #798,
`179093ffd6`) inspected the substrate and simulated the lane; its findings
are in § 1's version paragraph and in the text. **The stranger's proof**,
run 2026-10-24 on version 1 (`bc35aef3d8`) by a reader with no context given
this tree and the brief, read-only, in 38 minutes: some sixty claims
checked by command, thirteen wrong (the epic and the retitle already done;
the GENERIC_X64 configs' area; the 57 patches under thirty directories, not
eleven; the functions' line numbers; the metapackage's line ranges and its
eleven case arms; 583 calls, not 584; the fifteen non-core members, not
twelve; "every other recipe byte-equal" where about 140 differ by
upstream's dependency line and upstream carries a new core, four patches
and a changed RK3566 configuration this tree lacks; the branch scan's
predicate and count; `packages/emulation`, not `packages/emulators`, with a
null `shadowed_by`; the register grep's 37 rows, not 59; #228 and #120
open and mis-described; the three status blocks, not five; `xmllint`
absent; no `--help` on the generators and a second argument for MAME's;
`vm-qa`'s `wrapper` suite), twelve imprecise (RetroArch's recipe ranges
off by one; the fifth built device, RK3326; T2's tip one commit past
`f16cf7fc28`; T1's stage-B numbers medians of three, not n=1; AMD64's
3,530-line configuration; the window's times; the Argon call's length; an
`es-code-traps.md` clause that did not say what it was cited for;
`fix-walk-pending-image` missing from the classes; `time-to-play`'s
second reboot trigger), twelve questions it would have had to ask (the
merged lint copy; #650's five criteria against the brief's fifteen; the
built-device count; the Q4 (c) method; the regeneration's artifact without
`xmlstarlet`; MAME's drivers directory; the image; the branch-scan
predicate; the `proved:` classes; criterion 12's denominator; 146 against
152 `pkgcheck` runs; the register's union), two seams the brief had not
named (the table's `-P%SYSTEM%` after `%ROM%` against `runemu.sh`'s
`${ARGUMENTS##*-P}`, T1's #730; the five tokens the table emits against the
ten the interface expands, and the overlays it reads first, T2's rows), and
the places this brief disagreed with #650 (five criteria against fifteen;
no `--no-write` caveat), the plan (the fifth `proved:` class) and itself
(146 against 152). Version 2 answers each in the text; #650's body carries
the fifteen criteria and the two never-run switches; the futro's § 1 carries
an erratum for the configs' area.
