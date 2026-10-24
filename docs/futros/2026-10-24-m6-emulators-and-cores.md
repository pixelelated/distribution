# Futro: the emulators-and-cores area epic (#798), at T3's kickoff (#650)

**Prepared:** 2026-10-24, by the M6 coordinator lane (D-WORKFLOW-189), from
the brief `docs/reviews/briefs/emulators-libretro.md` version 1
(`bc35aef3d8`) and the tree at `next` = `8ebaf8daad`.
**Scope of this futro:** the area epic #798 (the emulators and cores: T3
#650 RetroArch and the libretro cores, T30 #677 the standalone emulators,
T24 #671 the recipes and files no shipped image builds) at the kickoff of
its first slice, T3. It covers T3's execution under its brief and the two
slices' order after it. It does not cover T30's or T24's briefs (each gets
its reading at its own dispatch), #336's runner (a spike with its own
issue), or the integration merges (the coordinator's, plan § 8).

**Upstream retros consulted:** T1's mini-retro (#648, 2026-10-24 00:58,
`docs/retros/2026-10-24-m6-os-launch-control-state.md` on the T1 branch at
`d3aa6a19c5`); T2's mini-retro (#649, `docs/retros/2026-10-23-m6-es-launch-path.md`
on the T2 branch at `f16cf7fc28`); P1's (`docs/retros/2026-10-23-m6-p1-survey.md`).
**Inputs considered:** the brief; #650's body; #798's body; the plan
(§ 3, § 4, § 6a to § 8, § 11); `docs/reviews/order.md` § 2 and the sizing
row (`tools/renovation-inventory --order --no-write`: `344 paths 31,961
lines 10,185 read 5,519 fork-own 1,670 patch currency`); `slices.json`
entries 3, 24 and 30; P1's `inventory.json` filtered by the slice's rules;
the interface futro (`docs/futros/2026-10-23-m6-interface.md`) and the OS
futro's substrate table (#695); `docs/blindspot-register.md` (73 entries);
the artifacts inspected below.

## 1. What do we know and what are we assuming?

**The plan (as written).** T3 reads RetroArch's recipe, its 21 patches and
fifteen per-device configuration sets, the 146 recipes of the membership,
the `emulators` metapackage whose `makeinstall_target` writes the launch
table, and the 24 launcher scripts, under the code-auditor lifecycle with
the renovation face; its kind is **currency**, so Q4 (the pins against
ROCKNIX and against the projects) is answered first and in three tables;
Q6 says what the four fork images reach; the eight fork-written RetroArch
patches get all seven questions; #336 Step 1's line retires only
RetroArch's menu and widget surface for the 2D cores. Extended depth, two
reviewers through the Facilitator, one worktree, no build, the guest for
what only the image can show. Then the stage-D pause, the coordinator's
stream briefs, remediation, stage F, the retro, the hand-back.

**Explicit assumptions we are relying on, each with its evidence:**

- **The membership is the inventory's at the P1 tip, and the tool applies
  the slice's own area to a rule without `areas`.** Evidence: the brief's
  filter run on 2026-10-24 against `git show 2174265e9c:docs/reviews/inventory.json`
  reproduces the tool's row exactly (`paths 344 lines 31961`), and the same
  filter without the area rule gives 395 paths (it sweeps in the cores' own
  57 patch files, which T42 owns). A hand-rolled glob is the wrong tool
  here; the brief says so.
- **The order row's `5,519 fork-own` is the filter's 6,557 without the four
  GENERIC_X64 configuration files.** Evidence: 6,557 - 1,038 = 5,519, the
  four files' lines summed from the inventory
  (`retroarch.cfg` 855, `retroarch-core-options.cfg` 154, `TATE-MAME
  2003-Plus.rmp` 27, `retroarch64bit-append.cfg` 2). *Erratum (the
  stranger's proof, 02:20): the reason is their `language` (`config` and
  `other`, outside the tool's code classes), not their area -- their area is
  `emulators-and-cores`, and the 21 `patches-and-configs` rows are
  RetroArch's patches alone. The arithmetic stands; version 2 of the brief
  says it this way.* The row's `10,185 read` is a
  third figure, the tool's `read_lines` (`tools/renovation-inventory` line
  999: `sum(r["lines"] or 0 for r in code)` over the area's **code** files
  by language, whatever their tier): `recipe`, `shell`, `cmake`, `python`,
  `udev` and `systemd` sum to 10,185; the 19,518 lines of `config` (the
  fifteen per-device `retroarch.cfg` sets and the option files) are outside
  it, and the brief reads the fork-own ones whole (§ 2 below).
- **The slice's bytes on the image are the tree's.** Evidence: `git -C
  /workspace/repos/rocknix diff --stat next 069fc2704421 -- <the two
  directories>` prints one file (`Install Steam.sh`, +605/-6), and `next`
  is `8ebaf8daad` in both checkouts.
- **The image's installed set is readable on the host without a guest.**
  Evidence (artifact inspection, 2026-10-24 01:52): the M7 GENERIC_X64 build
  root's install tree `build.pixelelated-GENERIC_X64.x86_64/image/system`
  is owned by the build user and world-readable; its
  `etc/emulationstation/es_systems.cfg` is a symlink to
  `/usr/config/emulationstation/es_systems.cfg` (dangling in the tree,
  resolving on the image), and `usr/config/emulationstation/es_systems.cfg`
  is 83,206 bytes, 2,745 lines, with 128 `<system>`, 152 `<emulator
  name=` and 500 `<core` elements; `usr/lib/libretro/` holds 116
  `*_libretro.so`; `usr/config/retroarch/` holds the four tracked files
  **plus** `Flycast.opt`, `Supafaust.opt` and `savefiles/` (other recipes'
  installs); `usr/config/modules/` holds 19 scripts (of 24 sources: the
  device's `PKG_EMUS` chooses); `usr/bin/retroarch` exists and
  `retroarch32` does not (x86_64). The `.tar` beside the `.img.gz` in
  `target/` also exists, so `SYSTEM` is extractable; the brief's version 1
  says the tar is not needed and routes the reach checks through the guest
  -- an adjustment (§ 5).
- **The build root carries the pin's sources.** Evidence:
  `build/retroarch-bdba046fa6766380bc2457532f38e589df769aaf/` with its
  `retroarch.cfg` defaults and `gfx/video_thread_wrapper.c`;
  `build/mame2003-plus-lr-a045126dad…/`, `build/fbneo-lr-f3b774987e…/`
  for the rotation tables; read-only.
- **The host has the tools the brief names, except three.** Evidence
  (`command -v`, 2026-10-24): `python3`, `gh`, `cc`, `gcc`, `git`, `jq`,
  `qemu-img`, `kpartx`, `unsquashfs` present; **`xmllint` and `xmlstarlet`
  absent** (the brief's version 1 names `xmllint --noout` for the table and
  the functions call `xmlstarlet fo`, which is in the build container
  only); **shellcheck absent** (T1 downloaded `shellcheck-v0.11.0` into its
  scratch; the brief says to do the same). Adjustments (§ 5).
- **The GitHub API budget covers the Q4 scan.** Evidence: `gh api
  rate_limit` reads 4,910 of 5,000 remaining at 01:52; the scan is about
  300 calls.
- **The reviewer route is in the tree and the key is on the host.**
  Evidence: the coordinator branch carries `033eb7ed23`, `0ceb2994c5`,
  `6874394d49`; T1 and T2 each served `google/gemini-4-argon` by Google and
  `openai/gpt-6-astra` by OpenAI through it (their `provenance.json`
  files); `~/.config/council/env` is present (never read).
- **The register's next Decided ID is 193.** Evidence (base-divergence
  check, 2026-10-24): this branch's register has 189, 190, 192 Decided and
  191 Open; P1's has 188 and 189; T1's and T2's have 188 to 191 (they
  merged this branch's tip before 192 landed); the simulated merge of this
  tip into T1's counted 660 IDs each once. No collision; 193 is free on
  every branch.
- **Nothing else runs in an M6 lane at dispatch, and the host may still be
  M7's.** Evidence: T1 and T2 idle and accepted; the coordination file's
  `== M7` blocks of 01:30, 01:37 and 01:50 (H700 producer07 active, then
  SM8550); the brief's § 5 makes the window a wait.
- **Build-vs-adopt:** not applicable; an audit slice adopts nothing. One
  line, as the skill allows.

**Confidence:** mixed. The counts, the hashes and the image's set are
verified by command; the three absent host tools and the guest-routed reach
checks are version 1 defects the stranger's proof or this futro catches
before dispatch; the Q4 scan's shape (what "behind" means for an
upstream-carried pin) is the one place the brief decides something the
plan does not spell out, and § 4 tests it.

## 2. What known unknowns need investigation?

| Unknown | Treatment | Owner / task |
| --- | --- | --- |
| Which language classes the tool's `10,185 read` sums over (so the brief states the three figures correctly) | **Resolved at writing** (the filter's rows grouped by `language`): `recipe` 147 files 5,443 lines + `shell` 31 / 3,971 + `cmake` 2 / 368 + `python` 2 / 245 + `udev` 9 / 80 + `systemd` 6 / 78 = 10,185; outside `read` are `config` (96 files, **19,518 lines**: the fifteen `retroarch.cfg` sets, the core-option files, the remaps), `patch` (21 / 1,670), `other` (29 / 567) and one `none`. So the tool reads the code and the brief reads the code *and* the fork-own configuration; version 2 says so | coordinator; done 2026-10-24 02:00 |
| Whether `tools/retroarch-wrapper-test` compiles and runs on this host's `cc` with pthreads (it has not run since #211's host; its default roots are retired) | Proceed to dispatch; the lane's stage-A tool trial after the return line; a failure is a `bug` with the error quoted, not a stop (brief § 8) | the lane, stage A |
| Whether the GitHub API returns 404 for some of the 148 `PKG_SITE` repositories (moved, archived or renamed since the pin) | Proceed; the Q4 (b) table carries a `repo-missing` class beside `pin-not-on-project`, with the `PKG_SITE` quoted; version 2 names it | coordinator (brief), the lane (table) |
| Whether the M7 candidate's merge lands `6101242e14`'s `Install Steam.sh` hunk on `next` before T3 reaches stage D | Proceed; the brief announces any finding on that file before a stream brief; the coordinator orders it against the merge; a deferral class `deferred:M7-merge` is named in version 2 | coordinator |
| How long the M7 window lasts (H700 producer07, then SM8550 build and readback) and whether it covers T3's dispatch | Proceed; the brief's stage A runs no runtime; the guest, the wrapper test's compile and `npm install` wait for the return line relayed on #650 | coordinator relays |
| Whether a host regeneration of the table (`add_emu_core`/`add_es_system`/`mk_es_systems` sourced from `distributions/ROCKNIX/config/functions`) runs outside the container: the functions read `${ROOT}`, `${ESTMP}`, `${INSTALL}`, `${PKG_DIR}`, `${DEVICE}` and call `xmlstarlet` | Investigate at stage A as a tool trial: `bash` with those variables set to scratch paths, `DEVICE=GENERIC_X64`; the pre-format `.es_systems.cfg` is the comparable output (the formatted one is empty without `xmlstarlet`); compared to the image's table by `python3 -I` with `xml.etree.ElementTree` on system, emulator and core names | the lane, stage A; version 2 writes the recipe |
| Whether `tools/pkgcheck <name>` resolves an override's name to the override or to a generic twin | **Resolved at writing:** `tools/pkgcheck` line 157 runs `find packages projects -type f -path */<name>/package.mk`, so it checks **every** recipe of that name under both trees and prints each path; `libspeexdsp`, `libxmp-lite` and `wildmidi` have no generic twin on `next` (the three print only the `easyrpg-lr/` path), `emulators` prints its one path twice. The loop records the printed path beside each verdict, and a second path is a second row | coordinator; done 2026-10-24 02:02 |

## 3. What patterns from prior work apply that we haven't named?

- **T1's method for a recipe-and-script slice** (`docs/retros/2026-10-24-m6-os-launch-control-state.md`):
  a failing case before every fix under the image's own tools; commits cut
  from intermediates only after a green run (now plan § 6b E's words);
  every fix with its two runs and its `Already written:`; device facts the
  guest cannot have kept as open items to test with P-05 notes (#728, #748,
  #758). T3 has fewer scripts and more recipes, and a recipe has no harness
  but `pkgcheck` and the build: the brief's `fix-host-regen` and
  `fix-pending-image` classes are that method's recipe-shaped form.
- **T2's four host holds** split a stream from its compile, and its retro
  asked the template to say what happens to a commit when compiling is
  forbidden. For T3 the equivalent is `pkgcheck` (a linter, allowed in a
  window) and the wrapper test (a compile, not): version 2 says a recipe
  commit may land with `pkgcheck` done and the compile queued, the running
  log naming the queue.
- **T2's classifier stops** on punch-list drafts with example strings: a
  defensive register (no quoted shell, no credential-shaped tokens, items
  by reference) from the first draft. T3's findings will quote
  `retroarch.cfg` keys (`cheevos_*`, `netplay_*`): name the key, never a
  value.
- **T2's four wrong claims about its own artifacts** before reading them:
  the brief's § 5 rule 1 and `engineering-practices.md` § Verify the
  artifact; the hand-back names counts the coordinator re-derives.
- **P1's two commands per quantity** (the survey's counting discipline):
  the brief's § 2 gives the filter and `git ls-files` for the same set and
  says what the difference is (the cores' patches); a count with one
  command is a lead.
- **The 2026-09-25 release-candidate round** (`release-candidates.md`,
  D-WORKFLOW-047): a candidate was called with webkitgtk one series behind
  and the proxy sixteen commits behind, because `fork-package-freshness`
  accepted a stated pin; a currency slice is that round's lesson made
  into a reading. The pattern to carry: a pin "behind" is a **finding
  with a disposition**, never a bump made on the slice branch (the
  brief's § 5 never-run list), because a bump is a build and the build is
  the coordinator's.
- **#226 and blindspot 47** (pango fetched its own cairo): a core recipe
  whose build system fetches at configure time (cmake `FetchContent`,
  `ExternalProject`, a `git clone` in a Makefile) is a Q3/Q6 lead the
  build root's unpacked sources can answer read-only (`grep -rl
  FetchContent $B/build/*-lr-*/CMakeLists.txt`); the brief's § 4 Q1 row
  names it, version 2 adds the grep.
- **#211 and `tools/retroarch-wrapper-test`**: a fork patch to RetroArch
  with a test that compiles the patched function out of the build root --
  the one mechanical check the eight patches have; the closing evidence
  `slices.json` names for this slice.
- **D-UI-079's line** (change stays inside the fork's lanes): T1 and T2
  each met a player-visible behaviour in upstream-carried code and put it
  to the maintainer through the coordinator (#711's overlay precedence).
  T3 will meet a per-device `retroarch.cfg` default and a core's default
  option; the brief's Q7 row and the § 3 citation route them the same way.

## 4. What could we be missing?

**Agent-execution simulation ("what if?" walkthrough):**

> Archetype simulated: a fresh Opus 5.5 lane with the brief, the tree and
> #650, starting while the M7 window is open.

- **Step: the counts (§ 2).** What if the lane runs `tools/renovation-inventory
  --order` without `--no-write`, or `--slice-issues`, to get "the tool's
  membership" as #650 says? It writes files into the worktree (the
  coordinator did exactly that in a throwaway on 2026-10-24 and removed
  them). **Plan change:** the brief names the filter as the re-derivation
  and the two switches as never-run; version 1 already does; #650's scope
  paragraph gets the same sentence.
- **Step: Q4 (b), the API scan.** What if a repository answers 404 (moved)
  or the pin is not on its default branch (a fork's hash, a force-push)?
  An empty cell in a table that passes is blindspot 39's shape. **Plan
  change:** the table's row classes are named (`current`, `behind-upstream`,
  `behind-project`, `upstream-same`, `pin-not-on-project`, `repo-missing`)
  and **an empty cell fails the scan's own check**; the script asserts
  every row has a class before it writes the table.
- **Step: Q4's verdict.** What if the lane reads "the pin's date against
  the project's head date" as "behind" for 120 upstream-carried cores
  whose pins ROCKNIX also carries, and the punch list proposes 120 bumps?
  D-WORKFLOW-186 puts ROCKNIX's currency first, and the fork adopts
  ROCKNIX's pins by merging `upstream/next`. **Plan change:** Q4 (b) has
  two tiers -- `behind-upstream` (ROCKNIX's `upstream/next` carries a newer
  pin: actionable, the disposition is `to merge` with the upstream commit)
  and `behind-project` (the project is ahead of both: informational for an
  upstream-carried recipe, a line on #585 only where the fork introduced
  or changed the recipe) -- and criterion 9 says so.
- **Step: Q6's counts.** What if the lane asserts the guest's 116 cores
  equal the recipe's list for GENERIC_X64 and the numbers differ (a recipe
  installing two `.so`, `libretro-database` installing none, a skipped
  core)? **Plan change:** the counts are *compared with the differences
  listed*, never asserted equal; version 2's § 5 says so, and the image's
  install tree on the host is the primary artifact, the guest the
  confirmation.
- **Step: `pkgcheck` over 152 recipes.** What if `tools/pkgcheck
  libspeexdsp` checks `packages/`'s generic recipe, not the fork's override
  under `easyrpg-lr/`? **Plan change:** § 2's investigation; the loop
  records the path `pkgcheck` prints beside each verdict, and a verdict on
  the wrong path is a FAIL of the loop.
- **Step: the host regeneration of the table.** What if the lane sources
  `functions` and `makeinstall_target` with `${INSTALL}` unset, and
  `install_script` writes `/usr/config/modules` on the host? **Plan
  change:** version 2 gives the sandbox recipe (every variable set to a
  scratch path, `DEVICE` and `ARCH` set, run under `bash -e` from a
  directory the lane owns) and says the formatted file will be empty
  without `xmlstarlet`, so the comparison is on the pre-format
  concatenation through `ElementTree`.
- **Step: the eight patches against master (Q4 c).** What if the lane
  clones `libretro/RetroArch` whole to run `git apply --check`? A clone is
  a download of hundreds of megabytes into a scratch, not forbidden, but
  heavy during a window. **Plan change:** fetch only the files the patches
  touch (`gh api repos/libretro/RetroArch/contents/<path>?ref=master`,
  base64-decoded into a scratch directory of their own) and run `patch
  --dry-run` per patch; version 2 writes it.
- **Step: `Install Steam.sh`.** What if the lane's shellcheck pass yields
  forty findings on a 2,755-line file the M7 lane is about to change by
  605 lines? **Plan change:** findings on that file are recorded; their
  remediation is a deferral class decided once, `deferred:M7-merge`,
  re-opened by the coordinator over the merged file (plan § 8's drift
  shape); the brief's stream briefs will not touch the file before the
  merge.
- **Step: the per-device configurations.** What if the lane proposes
  changing a `retroarch.cfg` value for a device the fork does not build
  (eleven of fifteen)? **Plan change:** the brief's Q6 already keeps them
  as rows for upstream; a Q2/Q3 defect in one is fixed where it is a
  defect on every device (the same line in all fifteen), and a value
  change is D-UI-079's question through the coordinator.
- **Step: the retro's time-to-play answer.** What if the lane measures
  with the image's `retroarch.cfg` and reports a number for a changed one
  without the hash check (T1's two uncounted runs)? **Plan change:** the
  brief already carries the bind-and-hash rule; version 2 adds that a Q5
  measurement row names the `retroarch.cfg` sha256 the guest ran with.

> Second archetype: the coordinator at integration, two weeks on.

- **Step: merging T3 after T1 and T2.** What if T3's fixes to
  `virtual/emulators/package.mk` conflict with the M7 candidate? The M7
  delta on the two directories is `Install Steam.sh` alone; `package.mk` is
  untouched there. What if **T30** (the standalone emulators) later needs
  to edit the `PKG_EMUS` lines and the standalone systems' `add_emu_core`
  lines in T3's `package.mk`? The membership gives the file to T3 and the
  standalone recipes to T30; the order runs them sequentially, so T30's
  edits land on T3's merged file (plan § 8), and T30's brief will say so.
  **Plan change:** #798's body already orders them; T30's brief carries the
  shared-file sentence when written.
- **Step: the image proof.** What if T3's `fix-pending-image` rows (a table
  fix, a recipe fix) wait for a GENERIC_X64 image that the M7 lane has no
  reason to build soon? The same wait holds T1's nine rows and T2's 21
  walks; D-WORKFLOW-191 is the open call. **Plan change:** none here; the
  dependency is named on #346 and in the M6 body.

**Pre-mortem (imagine the work failed 30 days out):**

- **Imagined failure:** on 2026-11-20 the H700 image carries three cores
  bumped from T3's punch list; two no longer load a save state written by
  the previous build (a core's state format changed between the pins), and
  a player loses a run. Root cause: a currency finding treated as a fix on
  the slice branch; the bump's `Already written:` said "nothing inherited"
  because nobody read the core's changelog for its state format; the VM
  could not run the arm build. **Plan change:** the brief's never-run list
  already refuses a bump without a stream brief; version 2 adds to Q4's
  disposition that a `to merge` of a core bump names the core's own
  changelog or commit range read for save, state and option-format
  changes, and that #10 (save states across build families) is cited on
  every such row; the stream brief, not the punch list, decides a bump.
- **Imagined failure 2:** on 2026-11-05 the lane's punch list has 60 Q1/Q2
  items on 120 upstream-carried recipes (the hand-rolled status echoes,
  the headers) and the table was never read. Root cause: the lens order
  (Q4/Q6 first for upstream-carried, the rest only where the file stays)
  was read as advice. **Plan change:** version 2's § 4 opening says the
  upstream-carried recipes' Q1, Q2, Q3 and Q7 cells read `n/a: upstream's
  recipe, unchanged here` unless a Q4 or Q6 row keeps the file in question
  or a Q3 lead points at it, and criterion 7 accepts that cell.

**Blindspot check (against `docs/blindspot-register.md`, 73 entries):**

- **39** (a suite passing over a table of dashes): applies to the Q4 (b)
  scan -- the empty-cell assertion above.
- **47** (a build that fetched its own dependency): applies to the cores'
  build systems -- the `FetchContent` grep over the build root's sources,
  read-only.
- **48** (an option changed without reading the log): applies to every
  `retroarch.cfg` and core-option line the lane would change -- `git log
  -p` first, the brief's § 3 says so.
- **54, 55, 63** (a measurement on a guest whose renderer was not the
  device's): applies to Q5 -- `--vm`, `Using resolution` read, the sha256 of
  the configuration the guest ran with.
- **65** (a proof's substitute passed where the real input failed): applies
  to a fixture ROM standing in for a real title; the row names the
  substitute and stays partial (P-05).
- **13, 46, 51** (assumed done; a name read as a behaviour; an open
  checkbox is a claim): the general ones; the brief's § 5 rule 1.
- **New entry, 74 (added with this futro):** *a fixture or a stub that
  silently does not engage, so the case tests something other than what it
  names* -- T1's sixteen faults of 2026-10-23/24, each found because the
  case's own output named the wrong thing; the guard is partial today
  (`tools/last-good-scripts-test`'s lifter takes a brace line with a
  comment, T1's `6b426ea624` on its branch) and the rest is #797.

**Replaced-mechanism archetype:** nothing in T3 replaces a mechanism; #336
would, and is not this slice. Not applicable, said so.

## 5. What adjustments or investigations must happen BEFORE execution?

**Plan edits applied (version 2 of the brief, before dispatch):**

- § 2: the three figures of the order row explained (fork-own without the
  GENERIC_X64 configs; `read` as the code files' lines by language, the
  classes named once § 2's investigation says which).
- § 2 and § 5: the image's installed set is read on the host from the M7
  build root's `image/system` (the dangling `etc/emulationstation`
  symlink resolves to `usr/config/emulationstation/es_systems.cfg`; the
  counts 128/152/500, 116 cores, 19 modules recorded as the baseline), the
  `.tar` exists beside the `.img.gz`, and the guest is the confirmation
  for what runs, not the only reader of what is installed.
- § 5: `xmllint` and `xmlstarlet` are absent on the host: `python3 -I`
  with `xml.etree.ElementTree` parses the table; the host regeneration's
  sandbox recipe with every variable set; the formatted output empty
  without `xmlstarlet`, the pre-format file compared.
- § 4 Q4 and § 7 criterion 9: the two tiers (`behind-upstream`,
  `behind-project`), the row classes including `repo-missing`, the
  empty-cell assertion, the changelog read for a `to merge` core bump with
  #10 cited.
- § 4 Q6 and § 5: counts compared with differences listed, never asserted
  equal.
- § 5: the `pkgcheck` loop records the path each run printed (the tool
  checks every recipe of the name under both trees).
- § 5: the patches' `--check` against master through `gh api
  .../contents/<path>?ref=master` and `patch --dry-run`, no clone.
- § 6 and the stream-brief deferral classes: `deferred:M7-merge` for
  `Install Steam.sh` findings until the candidate's merge.
- § 4 opening and § 7 criterion 7: the upstream-carried recipes' Q1, Q2,
  Q3 and Q7 cells may read `n/a: upstream's recipe, unchanged here`.
- § 5: a recipe commit may land in a window with `pkgcheck` done and the
  compile queued, the running log naming the queue (T2's retro).
- § 5 Q5: a measurement row names the `retroarch.cfg` sha256 the guest ran
  with.
- #650's body: the scope paragraph gets the two never-run switches of
  `tools/renovation-inventory`; the criteria replaced by the brief's § 7
  as version 2 leaves them.

**Investigation tasks opened (the coordinator, before version 2):**

- The `read` language classes (§ 2 row 1): done, above.
- `tools/pkgcheck`'s resolution of an override whose name has a generic
  twin (§ 2 row 7): done, above.

**Documented unresolved assumptions (proceeding without resolving):**

- The M7 window's end is not known; the brief makes it a wait and the
  dispatch happens with the window possibly open. Rationale: stage A runs
  no runtime, and T2 ran its stage A the same way on 2026-10-23.
- `tools/retroarch-wrapper-test` has not been run on this host since its
  roots were retired; a failure at stage A is a bug the lane files, not a
  reason to hold the dispatch. Rationale: the check is one of nine and the
  patches it covers are read regardless.
- T30's future edits to T3's `virtual/emulators/package.mk` are sequential
  by the order; no shared-path concurrency. Rationale: plan § 8 and
  D-WORKFLOW-190's "two slices never share a path" hold because T30 is
  dispatched after T3 closes or at least after T3's fixed-at.

**Blindspot register updates:**

- Entry 74 added (above), guard `tools/last-good-scripts-test` (partial)
  and #797 for the rest.

## Addendum: T30 at its kickoff (2026-10-24, from the brief `docs/reviews/briefs/emulators-standalone.md` version 1)

**What we know and assume.** T30 is an Extended currency slice with a
launch-path lens over the 35 standalone emulator recipes (543 paths, 55
fork-own, 10,695 code-class lines), run by the T3 session in a new worktree.
The assumptions, each checked at `8ebaf8daad`: the membership is the
`standalone/**` glob with every row `shipped` (543 of 543); `runemu.sh`
starts a standalone emulator through `/usr/bin/start_<core>.sh` (line 391,
with named arms for mednafen, scummvm and dolphin); the exit is
`input_sense`'s `killall ${TO_KILL}` from `/tmp/.process-kill-data`, which
`001-functions:511` writes (so a kill name is checkable against a binary
name without a device); the GENERIC_X64 image ships nine of the 35
(`dolphin-emu`, `duckstation-sa`, `flycast`, `hatarisa`, `hypseus`,
`moonlight`, `ppsspp`, `scummvm`, the `mupen64plus` set -- read from the M7
root's install tree); `tools/emulator-exit-test` drives RetroArch only (one
match for `retroarch`, none for any standalone name); the eight cheevos
scripts use no `eval`, `curl` or `jq` (a grep, not a reading: the slice
reads them); the pins fall in five shapes, two of them tarballs on a moving
branch of `ROCKNIX/packages`. **Substrate:** the lane's worktree does not
exist until dispatch; a guest needs M6 to hold the host and free content;
the Facilitator route for both seats is the one T3 used an hour before.

**Known unknowns.** Whether free content exists on the host for the nine
shipped emulators (ScummVM freeware, EmuTOS, homebrew `.pbp`/`.dol`/N64 --
to be fetched into `/workspace/tmp/m6-t30/`, never into `/storage/roms` of a
shared guest without saying so); what the cheevos scripts write and where
(`/var/log/cheevos.log`; the configs' modes) -- read masked; how
`tools/time-to-play` can be made to measure a standalone launch (it is
written for RetroArch; a hand measurement with the method stated is the
honest fallback); whether `q4-pins.py` runs over `standalone/` without
change (its recipe root is a parameter; its GitHub-only path means the
release-asset and tarball pins are hand rows).

**Patterns.** T3's whole method is the model (two-tier Q4, the regeneration
check, the `proved:` classes, the stage-D pause in under two hours); T1's
F-24 is the exit sweep's seed; #825 is the shell-line sweep's seed; #841 and
#844 are the moving-tarball pins' class; blindspot 65 (a substitute input)
governs every homebrew-title proof.

**What could we be missing (simulation).** A fresh session with the brief:
(1) **launches a standalone emulator on the guest with no content and
reads a black screen as a defect** -- the brief lists what each needs; the
row says *no free content* and the launch is an open item; (2) **reads
`GameIndex.yaml` (62,331 lines) or `mednafen.template` (17,652) line by
line** -- data, read for provenance; (3) **grades the cheevos scripts from
the `eval|curl|jq` grep** instead of reading each (the brief says the grep
is not the grading); (4) **prints a `get_setting` value** from a cheevos log
while proving the logging claim -- the masking rule is in § 5 and the
never-run list; (5) **fixes `aethersx2-sa`** that upstream deletes (class
1: every row `deferred: base merge`); (6) **treats a kill-name mismatch on
an emulator no built image ships as a High** -- the exit sweep's row class
*not shipped on any built image* exists for it; (7) **runs the guest while
M7 holds the host** -- the relay rule and the census are in § 5; (8)
**measures time to play once with no n** -- the brief asks for method and
n; a single run is a lead. **Pre-mortem:** the two seats return thirty
items about emulator configs the fork carries from upstream unchanged, the
punch list balloons to sixty, and the stream briefs take the coordinator a
day; prevention: a Q4 `behind-upstream` row for an upstream-carried config
is a disposition (*kept: upstream's*), not a fix, and the brief's grading
rule (a defect is a `bug`; a wording item rides the audit issue) keeps the
streams to the fork-own 55 and the launch-path defects.

**Adjustments before execution (into version 2):** A1 a line in § 5 that
free content is fetched into `/workspace/tmp/m6-t30/content/` and placed
on the guest by `scp` or the serial console into `/storage/roms/<system>/`,
named in the running log, never a commercial file; A2 the exit sweep's
third row class named in § 4 (it is); A3 `tools/time-to-play`'s scope
stated (RetroArch) with the hand method for standalones; A4 the grading
rule for upstream-carried configs (*kept: upstream's* unless a defect). The
stranger's proof of the brief runs beside this addendum; version 2 records
both.

### Errata to the T30 addendum (after the stranger's proof)

The addendum said the GENERIC_X64 image ships nine of the 35 with
`moonlight` among them: it carries **thirteen** (twelve binaries and
`pico-8`'s script), and `moonlight` is `packages/apps/moonlight`, not a
member. It called the kill-target lead *T1's F-24*: T1's F-24 is the shared
`log()`'s unbounded append, and the lead is **T3's PL-010** (`Start
RPCS3.sh`, fixed upstream by `eeb33c5a37`, which also edits this slice's
`start_mupen64plus.sh`). The directory holds 623 files, the slice 543: the
80 patches are T42's and T43's. `q4-pins.py` hardcodes `libretro/` and is
copied and edited, not parameterised. A lead the proof surfaced and the
addendum missed: `start_hatarisa.sh` is what the generic arm asks for and
`start_hatari.sh` is what the recipe installs, renamed upstream by
`2e7041d273`.
