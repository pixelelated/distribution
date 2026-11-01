# Review brief: M6.P2 T37, the EmulationStation recipe and themes in the distribution: the pin and its build steps, the build options and the renderer define, the dependencies, the build credentials by name, the shipped theme and `lowerdeck`, the patch directories, and package currency against ROCKNIX's recipe (#684)

**Version 2, 2026-11-01 00:24:37 UTC, after the stranger's proof of version 1** (D-WORKFLOW-189;
`docs/reviews/plan-for-the-plan.md` § 6b, § 6c, § 7). Version 1 was written from five
read-only research files -- R1 membership and provenance, R2 the recipes read
at the P1 tip, R3 tests, build and harness, R4 the inherited items, R5 the
model and the ceremony (`/workspace/tmp/m6-coordinator/kit/t37-research/`, in
no tree) -- and nothing else: every figure here is one of their quoted tool
lines, cited as `R1 C<nn>` (R1's commands C01 to C23), `R2 cmd <n>` (1 to 28),
`R2 § <n>` or `R2 L-<nn>`, `R3 cmd <n>` (1 to 24), `R3 § <n>` or `R3 G<n>`,
`R4 item <n>`, `R4 § <n>` or `R4 cmd <n>`, `R5 C<n>` (C1 to C15) or
`R5 § <letter>`. **Version 2 adds the stranger's proof of version 1**,
`/workspace/tmp/m6-coordinator/kit/t37-proof.md` (358 lines; its commands
cited `proof C<n>`, C1 to C16, its corrections `proof Correction <n>`), with
every correction applied at its line and every item it settled moved into
the body with its command, and three lines of version 2's own drafting read
at the same hashes, cited `v2 read`. **`[unverified]` marks what no tool line settles, with what
would settle it**; `## Version 1: what the drafting read did not settle`
near the end lists every one still open, and
`## Version 2: corrections from the proof` lists the sixteen corrections. Counts by `/usr/bin/grep`, never the shell's
function (#1138; R5 § B item 12). The structure is T36's brief
(`docs/reviews/briefs/es-core-utils-resources.md`, version 2 at `b1f34ce658`
with its errata before dispatch at `e29a2966bc`, 2,149 lines by `grep -c ''`,
R5 § A, C2): every T36-specific paragraph is replaced; every boilerplate
paragraph R5 § A marks *copy* is copied with this slice's names and
placeholders and scaled down for a 15-path recipe read; the section map is
the coordinator's for a recipe slice (§ 3 is the floor, § 8 what the
integration inherits, § 9 the register and the ceremonies, § 10 the pointer,
the host, the hand-back, the stops and the never-run list). R5 § B's twelve
recurring errata are written out of it: the register line from the decided
table only (§ 9); the placeholder check in pieces (§ 9); every ES ref recorded
as whichever line prints (§ 1); `tools/pkgcheck` by package name (§ 1 ruling
(d)); every figure as its tool prints it, 15 against 19 paths and 4,561
against 4,650 lines each with its command (§ 1); § 10 copying § 5's and § 7's
figures from one source; each guest write named in the G-table and the
never-run list together (there are none, § 5, § 10); a row read before it is
cited, the standing slot cited by #1293 (§ 10); the shell, locale and tool
limit stated beside each expectation (§ 5); one ownership row,
D-WORKFLOW-217, cited everywhere (§ 1, § 9); each G-row's precondition named
(§ 5); and every count by `/usr/bin/grep`. The rule, register and futro lines
are the coordinator worktree's at **`de935d6ec6`**, which hold at
**`7d43f340c5`** (`feature/m6-renovation-plan-346`; R5's header, C9, C15:
`git diff --stat de935d6ec6 HEAD -- docs/decision-register.md docs/futros
.claude/rules docs/reviews/briefs` printed no line at `7d43f340c5`), and hold
at `563857ea02`, where version 1 was committed (proof C1, C10, C11), and at
`960d581c12` (v2 read:
`git diff --stat 563857ea02 960d581c12 -- docs/decision-register.md docs/futros .claude/rules docs/reviews/briefs`
printed no line); the lane re-reads them at `COHASH`.

## 1. Identity

- **Issue:** #684 `M6.P2 E339/T37: interface: the EmulationStation recipe and
  themes in the distribution` (read 2026-10-31T16:43:00Z by `gh --repo
  pixelelated/distribution issue view 684`: OPEN, milestone `M6: Codebase
  renovation`, no labels, **0 comments**, parent #339, REST id
  `5992345010`; R5 § F, C7), **retitled at dispatch to `M6.P2 E700/T37:
  interface: the EmulationStation recipe and themes in the distribution`**
  and re-parented from #339 to #700 (`milestone-phase-naming.md`; R5 § D's
  `t37-retitle.sh`; #683 already reads `M6.P2 E700/T36` with parent #700, R5
  § F). The body is 27 lines with 5 generated checkboxes (sha256 prefix
  `90c68fc0aacbf0d2`, R5 § F, C7): `:7` *"15 paths, 4,561 lines; 327 lines
  read, 190 of them fork-own (inventory at `eb4763e3cc`)"*, `:8` *"fork-own
  6, upstream-carried 9"*, `:13-14` `reviewed-at:` and `fixed-at:` only (R5
  § F). Slice `es-recipe` (`k: 37`) in `docs/reviews/slices.json`, selector
  `{"globs": ["projects/ROCKNIX/packages/ui/**"]}`, area `interface`, kind
  `read` (R1 C17); `docs/reviews/order.md` § T37 opens at `:653` (R1 C03,
  C17) and carries *"**id**: `es-recipe`; **kind**: read; **lens**: package
  currency"*, *"**why here**: the pin, the build steps and the themes the
  image installs"*, *"**paths** (15 paths, 4,561 lines, 327 read, of which
  190 fork-own; 0 patch and config lines; reach shipped 15): areas
  `interface`; globs `projects/ROCKNIX/packages/ui/**`"*, read before none,
  *"**depth**: Independent -- a small recipe read; plan § 6c names no Local
  exception for code (gpt)"*, interacting subsystems *"the ES tree (every
  `es-*` slice)"*, closing evidence *"audit folder, lint PASS,
  `tools/pkgcheck`"* (R1 C03). `order.md`, `slices.json` and
  `inventory.json` are the P1 branch's at `2174265e9c`, which the lane's
  worktree is stacked on (R1 C01, C10; read in the P1 research clone
  `/workspace/tmp/m6-coordinator/t11-research/tree` by `git -C`). Lines
  153-155 put T37 last in the interface's run, *"then the recipe"* on `:155`
  (R1 C04; proof C12, Correction 9).
  **`order.md:180` is not this slice:** `| T37 | T14 | tooling-state-tests |`
  is a row of the renumbering table (its header `| Second | Third | Slice |`),
  so a "T37" in the preliminary review's answers is today's **T14** (R1 C03,
  C04; R1 § 6 D10). **Epic:** #700 `M6.P2 E339: Area epic: the interface,
  EmulationStation (T2, T18, T20, T21, T26, T31 to T37, T44)` (R5 § F).
  **Predecessors:** T35 #682 has handed back (distribution `7321db61d3`, ES
  `d0e5b3432` at the hand-back; R4 § 9, item 41; R5 § B item 3, C15), and its
  ES ref has moved since: `origin/feature/m6-es-core-window-input-682` read
  `b7fdb3a24c`, 9 commits ahead of the pin and containing `d0e5b3432`, at the
  proof (C4, C15; Correction 4); T36 #683 is in flight (R4 § 9 read its
  folder at `3fc87774c1`, stage B), so **both lanes' tips are read at stage
  A**, never copied from here; T44 after. The futro
  `docs/futros/2026-10-23-m6-interface.md` (1012 lines, its last heading
  `:998`, *T36 kickoff addendum*; R5 § C, C4, C14) takes a **T37 kickoff
  addendum** written by the coordinator with version 2, after the last
  heading present at dispatch, in T34's to T36's six bold-led paragraphs (R5
  § C). **Milestone:** M6. **Beside it:** T36's lane, possibly on the same
  host; the host shared through `/workspace/tmp/m7-m6-host-coordination.txt`;
  a window for this slice asked for on #684 and granted there and in that
  file's queue (§ 5 item 2).
- **The order's sentence, and what each of its figures counts** (R1 § 6 D1
  to D5). **The glob reaches 19 paths; the slice is 15.** `git ls-tree -r`
  over `projects/ROCKNIX/packages/ui/` prints 19 at `2174265e9c` and at the
  inventory's head `eb4763e3cc` (R1 C07, C10; R3 cmd 1, cmd 5; R4 cmd 3, cmd
  20); the inventory's slice is the 15 of them in area `interface` (`mine:
  15 paths.txt: 15 equal: True`, R1 C10); **the four outside are the
  patches**, area `patches-and-configs`: `emulationstation/patches/x86_64/cpugov.patch`
  is **T40 `patches-dead`**'s, the three theme patches **T42
  `patches-shipped`**'s (R1 C11, C17). A selector with no `areas` key takes
  the slice's own area (R1 § 2). **4,561 lines is the 15 by `grep -c ''`**
  (R1 C10: `grep -c, the inventory paths at its head: 4561`); the 19 are
  4,650 by `grep -c ''` and 4,649 by `wc -l`, the one file without a
  trailing newline being `emulationstation/system.d/essway.service` (20 by
  `wc -l`, 21 by `grep -c`) (R1 C07); the four patches are 89 lines (R1
  C20). **"327 read" is the 9 code files** -- `shell` 4 files 100 lines,
  `recipe` 3 files 186, `systemd` 2 files 41 -- and **"190 fork-own" is the
  read lines of the fork-own files** (`SET+TIER read fork-own 190 lines`),
  not the fork-own files' size, which is 572 (`TIER fork-own 6 paths 572
  lines`) (R1 C11, C12; R1 § 6 D3). **"0 patch and config lines" counts
  vendor-carried lines** (R1 C06's legend; C10 `vendor-carried lines: 0`):
  the four `.cfg` files, `LANG config 4 paths 3878 lines`, are in the 15 and
  its 4,561 but in neither *Read* nor that column (R1 C12; R1 § 6 D4);
  `es_features.cfg` (2,039) and `es_input.cfg` (1,810) are most of the slice
  (R1 C07). **Tiers:** fork-own 6, upstream-carried 9 (R1 C11) -- git's
  classes over the 15: fork-added `es_savestates.cfg`, `Tiny5-OFL.txt` and
  `pixelelated-wordmark.svg`; fork-modified `emulationstation/package.mk`,
  `essway.service` and the theme's `package.mk`; the rest upstream-carried,
  byte-identical to the merge base (R1 C13; R1 § 6 D5). All 15 are reach
  `shipped` (R1 C10). The inventory's `overlap` (fork-own and changed
  upstream since the merge base) is True on `emulationstation/package.mk`
  and `essway.service` (R1 C11). **What the title leaves implicit:** the 15
  are 3 recipes (`emulationstation`, `lowerdeck`, `es-theme-art-book-next`),
  4 `.cfg`, 4 scripts (`autostart/001-emulationstation`,
  `sources/es_settings`, `sources/serial_number_check`,
  `sources/start_es.sh`), 2 systemd units, a font licence and an SVG (R1
  C07). No generic `packages/` directory carries any of the three names, so
  these recipes override nothing generic (R1 C09; R3 cmd 3).
- **Ownership rulings, stated once; § 2's take-up table points here.**
  **T37 owns the 15 paths of `projects/ROCKNIX/packages/ui/**` that the
  inventory assigns it, and nothing else.** No decided row names
  `projects/ROCKNIX/packages/ui/`, `es-recipe` or `lowerdeck`; **D-UI-090**
  (`decision-register.md:391`) names the theme, by its upstream offer (§ 9);
  **D-WORKFLOW-216** (`docs/decision-register.md:776`, T36's row) is the
  only one that names T37, and it routes two items here (R1 C16, C18; R4 §
  3; R5 § G; proof C12, Correction 2; v2 read at `563857ea02`:
  `awk '/^## Open decisions/{exit} {print NR": "$0}' docs/decision-register.md | /usr/bin/grep -E 'T37|art-book|lowerdeck|es-recipe|packages/ui/'`
  matches `391: | D-UI-090` and `776: | D-WORKFLOW-216` only). This slice's own ownership row is the coordinator's,
  **D-WORKFLOW-217**, written at dispatch (ruling (j)). The rulings are the
  coordinator's for this brief:
  (a) **The slice is the inventory's 15.** The four patches are named for
  T40 (`cpugov.patch`) and T42 (the three theme patches) and read only as
  the recipe reaches them: **L-02's patch directory -- the recipe's
  `PKG_PATCH_DIRS`, unset at the tip -- is T37's line; the patch's content
  is T40's** (with #1072's two acceptance shapes, *renamed to
  `patches/x86/` with the call fixed, or removed with the reason*, R4 item
  14), and the theme patches' text is T42's, their upstream offer under
  D-UI-090 (#69, R4 items 26, 27).
  (b) **The lane changes only `projects/ROCKNIX/packages/ui/**`** -- by (a),
  only the 15 -- **and never the ES recipe's `PKG_VERSION` (`:5`) or
  `PKG_GIT_CLONE_BRANCH` (`:6`) line** (R1 C08): the pin bump is the
  integration's, under D-WORKFLOW-191, which is still open
  (`decision-register.md:783`, R4 item 5, § 3). **A pin or theme bump is a
  finding with its reason, never a change** (D-WORKFLOW-024,
  D-WORKFLOW-165): a theme bump needs a new `PKG_SHA256`, which needs the
  tarball, which needs a fetch (R5 § D, ruling question 2). Nothing under
  `packages/` or `tools/`, nothing else under `projects/` --
  `projects/ROCKNIX/packages/virtual/image/package.mk:18`,
  `PKG_UI="emulationstation es-themes textviewer lowerdeck"`, included (R1
  C09; ruling (f)).
  (c) **No ES worktree.** The pin and the lane branches are read by `git -C
  /home/max/Development/emulationstation-next.worktrees/qa-integration show
  <hash>:<path>` only; that checkout's `test/qa-integration` and
  `origin/test/qa-integration` are the pin, 0 commits beyond it (R1 C15; R5
  C11), and a by-hash read does not move when another lane moves a branch
  (R5 § A). Neither `m6-es-recipe-684` path exists (R5 C11). **The body's
  `reviewed-at-es:` and `fixed-at-es:` fields read `none -- no ES change`**,
  added by the coordinator at dispatch beside the two fields #684 carries,
  and the five contract criteria are adapted to say so (§ 7).
  (d) **`tools/pkgcheck <name>`, by package name, for each of the three
  recipes after every `package.mk` edit** -- `emulationstation`,
  `es-theme-art-book-next`, `lowerdeck` -- each preceded by the `find
  packages projects -type f -path "*/<name>/package.mk"` listing as its
  positive (R3 § 6 step 3; R5 § E). **A path argument passes vacuously**
  (`tools/pkgcheck projects/ROCKNIX/packages/ui/emulationstation`: nothing,
  rc 0, R5 C11) **and so does a name that matches no recipe**
  (`es-theme-no-such-package`: 0 lines, rc 0, R3 § 1.1, cmd 10); the lane
  names the second, and `tools/fork-package-freshness`'s two like
  fail-opens (an unknown name prints the header row and exits 0, R3 § 1.3;
  a missing ref prints `fatal: bad revision 'upstream/next'` and exits 0,
  proof C8, Correction 16), in the hand-back as a **Backlog lead for the
  coordinator** to file (L-21).
  (e) **The upstream read is from the refs already in the repositories,
  dated as they stand, with no fetch:** `upstream/next` as fetched in the
  primary checkout, `651150fc88` (2026-10-24, *Merge pull request #3547 from
  spycat88/qcom-bls*; R1 C01), and `rocknix/master` in the ES repository,
  `f6c542872e` (2026-10-23, *Merge pull request #54 from
  porschemad911/s922x-suspend*; R1 C15). The theme's and `lowerdeck`'s
  authors' `HEAD`s are R1 C20's network read of 2026-10-31
  (`art-book-next-es` `9a50ef366e750aabfab29e6915a2867607212971`, the pin;
  `lowerdeck` `8fefe16e9cec4a03a540f7f256f8e0b2d1fd28f3`, not the pin
  `ab735114ab318a84e4d28c9c5f1b154e450a579a`), cited as R1's with its date and
  never refreshed by the lane: no `git ls-remote`, no `gh api`, no
  `rc-preflight` (its `base: emulationstation` fetches `rocknix/master`, R3
  § 1.4), and of `tools/fork-package-freshness` only `--list` with both refs
  given (`FRESHNESS_BASE=651150fc88 FRESHNESS_HEAD=<the tip>`, the tool's
  `:42-43`), which is pure git and is judged by its output's counts, never
  its rc (R3 § 1.3, cmd 12; proof C14, Correction 16).
  (f) **ES's top-level `CMakeLists.txt` is read for what the define does and
  is owned by no slice here -- it is named as the integration's.**
  `es-core/CMakeLists.txt` (the renderer source list) is T35's
  (D-WORKFLOW-214, -216); `virtual/image/package.mk` and
  `virtual/es-themes/package.mk` are **T8 `image-packages`**'s (R1 C11,
  C17); the dependencies' recipes are T8's, T7's, T22's and T23's (§ 2's
  neighbours).
  (g) **The three lanes' records that route items here** -- T2's PL-029,
  #1072, and D-WORKFLOW-216's two -- **are § 2's take-up table**, with R4's
  other items beside them.
  (h) **The candidate image's provenance is the integration's question, not
  T37's defect.** The M7 candidate `069fc2704421` carries the same ES
  `PKG_VERSION` but nine ES patches P1's recipe lacks and a corrected
  `es_systems.cfg` link (R3 § 2.2 C1, C2, § 2.3, cmd 21, cmd 22); the lane
  reads it and records it in § What the integration inherits.
  (i) **The French catalog, the themes' content and every ES file are
  outside the slice.** The theme recipe is the slice's; the files of the
  author's tarball it installs are not.
  (j) **D-WORKFLOW-217 is the ownership row at dispatch** (R5 § G: no
  `D-WORKFLOW-217` row at `7d43f340c5`, R5's header, C9, C15; none at
  `563857ea02`, proof C10: `D-WORKFLOW-217 ABSENT`); **D-WORKFLOW-215
  governs any hold** (`decision-register.md:771`, R5 § G), and none is
  expected in a recipe read.
  (k) **The lane never sources `config/options` in its worktree** (proof
  Correction 1). Sourcing it writes: `config/functions:801-802` set
  `_CACHE_PACKAGE_LOCAL="${BUILD}/.cache_package_local"` and
  `_CACHE_PACKAGE_GLOBAL="${BUILD}/.cache_package_global"`, so one call per
  device creates `build.<distro>-<DEVICE>.<ARCH>/` holding both files. The
  proof's call from inside the P1 research clone took
  `git status --porcelain --ignored | wc -l` from `status-before=2` to
  `status-after=4`, leaving `build.pixelelated-GENERIC_X64.x86_64/` and
  `build.pixelelated-H700.aarch64/` there (C8, C9, C10, C15). So every
  sourced-recipe call -- § 5's effective values, the patch reach, the
  stamps, the checker's steps 4 and 7 -- runs in **a scratch export of the
  tip**, `git -C <worktree> archive <tip> | tar -x -C /workspace/tmp/m6-t37/export/`,
  never a checkout; § 5's block names the two cache files as the call's
  writes there; **no `build.*` root in the worktree at any stage, and a
  `build.*` root found there is a stop** (§ 10); `00`'s census records the
  export's path and that it was retired at stage H, the plan's *Close*
  (D-INFRA-022). The research clone is read by `git -C` only, as § 2's
  block reads it.
  So the lane writes no line outside the 15 (a fix in a neighbour is named
  for its owner at the pause).
- **The division of labour (D-WORKFLOW-189), inverted for a distribution
  slice.** This lane executes. It does not re-cut the slice, change a
  criterion, write a brief, move the M6 body, edit `slices.json`,
  `areas.json`, `order.md` or the plan, file a Backlog issue, post on #346,
  #585 or #909, or decide a question of scope: those are the coordinator's,
  reached through #684, one question at a time. What it does file: its own
  audit punch-list issue (stage D) and a `bug` issue for a defect it proves,
  with its trace and `Already written:` line (D-WORKFLOW-187). **A fix lands
  only under a stream brief the coordinator writes at the stage-D pause, on
  the distribution branch, under `projects/ROCKNIX/packages/ui/**`, never in
  an ES checkout** (R5 § A). This is the first slice since T16 (#663, the
  rclone package) whose fixes would land in the distribution's `projects/`
  (R5 § A). *Kind read* still allows fixes in the recipes under a stream
  brief (R5 § F). A defect in a line the fork wrote is the fork's to fix; a
  defect in an upstream line is a contained fix under
  `bugs-are-agent-first.md` rule 6 and a #585 line (D-WORKFLOW-164, never
  sent, D-WORKFLOW-165). **D-UI-079's lanes** (`engineering-practices.md` §
  Change stays inside the fork's lanes) are the surfaces the fork's commits
  on these paths work in (R1 C12, C13; R2 § 0): the ES pin and the clone
  form (`cb50b45f6e`, and 241 of the 246 non-merge commits touching
  `emulationstation/package.mk`), the shared ScreenScraper developer
  identity and the runtime login (#566, D-WORKFLOW-166), the RVZ licence
  files and `zstd` (`84ff94fb3d`), the log loop that names a key and never
  its value (`144b3eccb6`), the Wayland wait in `essway.service`
  (`c6afa31db1`), the identity, wordmark and splash (`3d7c075f63`,
  `a9af618398`, `b137d8c373`), the Tools-icon patch (`638eedc5b3`) and the
  save-state layout `es_savestates.cfg` (`dee5d6dd0e`, #196). **The
  autostart step, `es_input.cfg`, `es_features.cfg`, `es_settings.cfg`,
  `sources/es_settings`, `sources/serial_number_check`, `sources/start_es.sh`,
  `emustation.service` and `lowerdeck`'s recipe are upstream surfaces**,
  read for currency and left as upstream has them; a defect in one is still
  ours to close when the fix is contained (rule 6; L-12, L-13 and PL-029 are
  this shape).
- **One worktree, one session, and four placeholders.** The distribution's
  **`feature/m6-es-recipe-684`** at
  **`/workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684`**,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** (the P1 tip; or the one the dispatch comment names) with
  the coordinator's branch merged in and the lane's pointer seeded. **There
  is no ES worktree** (ruling (c)): `Q=/home/max/Development/emulationstation-next.worktrees/qa-integration`
  is read by `git -C "$Q" show <hash>:<path>` only, in every block of this
  brief. **Four placeholders stand in this brief for hashes that do not
  exist until dispatch:** `COHASH` (the coordinator's tip merged into the
  lane's branch), `MERGE_HASH` (that merge commit, the lane's dispatch tip),
  `TIPHASH` (the lane's own tip as it moves; at stage A it is `MERGE_HASH`)
  and `V2HASH` (this brief's commit on the coordinator's branch at dispatch,
  version 2 after the proof; version 1 has no dispatch hash). The dispatch
  comment on #684 and the seeded pointer carry their values; the lane reads
  them there, never guesses them, and § 9's placeholder check names all
  four. **No lane changes these paths:** none of the 80 `feature/m6-*` refs,
  local and `origin`, changes anything under `projects/ROCKNIX/packages/ui/`
  against `2174265e9c` (R1 C18), and `next`'s `ui/` is byte-identical to the
  tip's (R2 § 4, cmd 1; R1 C02). Until the dispatch comment exists the
  pointer is not seeded and nothing starts.
- **Depth: Independent** -- one seat from another lab (plan § 6c,
  D-WORKFLOW-137; `adversarial-council.md`: an Anthropic-led audit's
  reviewer is pinned GPT-6 Astra): Astra at `max` over a trimmed, scanned
  packet (D-WORKFLOW-195) -- **the 9 code files whole** (the inventory's
  327 read lines, R1 C12), **with `emulationstation/package.mk:39`'s value
  masked** (the shared ScreenScraper identity's local, which no research
  file reproduces, R2's header), `es_savestates.cfg` (26) and
  `es_settings.cfg` (3) whole, **`es_features.cfg` (2,039) and
  `es_input.cfg` (1,810) by cited ranges only** (R1 C07), `Tiny5-OFL.txt`
  and the wordmark SVG named in the manifest and not sent, and the four
  patches named for their owners and cited by range only where a question
  reaches them; the lane replaces these figures with the packet's own
  `wc -l` in the manifest. No line cap for an Independent packet was found
  (R5 § A, C12), so this is the drafter's call against T36's whole part
  (6,212 lines, R5 § A). A probe then one refutation (one in-call retry
  allowed); `review-plan.json` records depth `independent` and the one
  reviewer with its served model; **exactly two keyed `tools/council/run
  invoke` calls**, every other `tools/council/run` call with
  `COUNCIL_ENV_FILE=/nonexistent` (the recipe is
  `.claude/skills/council/SKILL.md` and its `references/`; the runtime under
  `tools/council/` from `npm install --offline`, no fetch). **What the scan
  will hit, so the lane dispositions rather than stops:**
  `emulationstation/package.mk`'s five credential-name lines (`count lines:
  5`: `:30` `SCREENSCRAPER_RUNTIME_DEV_LOGIN`, `:40` the two ScreenScraper
  parameter names with `SCREENSCRAPER_DEV_LOGIN`, `:42`
  `SCREENSCRAPER_DEV_LOGIN`, `:43` `GAMESDB_APIKEY`, `:44`
  `CHEEVOS_DEV_LOGIN`; R5 C10), each dispositioned *build-variable name*
  under D-INFRA-006, D-INFRA-007 and D-WORKFLOW-166, and `:39`'s value,
  masked before the packet is built; **a value that reaches the packet stops
  it**. `es_settings.cfg`, the four scripts and the ES recipe carry no
  credential-shaped line in the hooks' own form (§ 5 item 3): it counted `0`
  on each of the six (proof C12) after a planted private-key header line
  matched `1` and a plain line `0` (C13); the other nine of the 15 were not
  scanned, and the lane's scan covers all 15.
  `packet-manifest.json` records every hit dispositioned by file:line; no
  value reaches the packet or an artifact.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at stage
  A. **The session is the T3 session (`m6-t3-emulators`), free since T34's
  close-out** (T34 ran there and its close-out ends `idle`; the day log
  names T37 *"a read slice at Independent depth for the free T3 session"*;
  R5 § A, C11).
- **The first commands** (stage A, in the distribution worktree;
  `8ebaf8daad` is `next`'s commit the P1 branch stacks on and `651150fc88`
  is `upstream/next`'s, both shared by every M6 lane, R1 C01, C02, R5 § D;
  the four scripts' shebangs are `#!/bin/bash` three times and `#!/bin/sh`
  for the autostart, R5 C10, and this block runs under bash):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684
cat .github/sessions/saved-session-state-feature-m6-es-recipe-684.md      # the pointer: the dispatch's hashes; § 10 names the eleven keys to check
git status --short | wc -l                                                 # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- projects/ROCKNIX/packages/ui | tail -n 1   # empty: 2174265e9c is next plus 64 commits, none under ui/ (R1 C02)
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched (ruling (e))
git merge-base 2174265e9c 651150fc88                                        # c445081a59518f37d9776e5412dd7b14910696f7 (R1 C01, C02)
Q=/home/max/Development/emulationstation-next.worktrees/qa-integration; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$Q" cat-file -e "$PIN^{commit}" && echo pin-here                    # pin-here (R5 § A)
git -C "$Q" rev-parse --verify rocknix/master                               # f6c542872e..., the whole line (R1 C15; R5 C11 printed the first ten)
git -C "$Q" merge-base "$PIN" rocknix/master                                # cada856d86..., the whole line (R1 C15)
for r in origin/feature/m6-es-core-window-input-682 origin/feature/m6-es-core-utils-resources-683; do printf '%s ' "$r"; git -C "$Q" rev-parse --verify "$r" 2>&1; done   # both read now: T35's printed d0e5b3432e at R5 C15 and b7fdb3a24c (9 ahead of the pin) at the proof's C4; T36's printed a `fatal:` line at the proof's C4; each line is recorded whole as it prints -- a hash or `fatal:`, no `cut` (proof Correction 4) -- and neither is a stop (R5 § B item 3)
for n in emulationstation es-theme-art-book-next lowerdeck; do find packages projects -type f -path "*/$n/package.mk"; tools/pkgcheck "$n"; rc=$?
echo "pkgcheck $n rc=$rc"; done                                              # one path each, then `rc=0` (R3 § 1.1, cmd 10)
tools/register-check >/dev/null; rc=$?
echo "register-check rc=$rc"                                                # rc=0 (R5 C10)
date -u +%H:%M:%S; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200   # who holds the host, with the time of the read; no guest before a grant on #684
```

Every expectation above is a research file's printed line, cited in its
comment; the `cat` cannot run before the pointer is seeded; the `stacked`,
`upstream-next-is-here` and `pin-here` lines are the lane's own. **`rc=$?`
sits on its own line after each command** (`engineering-practices.md` §
Capture `rc=$?` on its own line; R4 § 6 item 4 is a void reading of exactly
that shape). The host file's tail is whatever the host is doing at the
moment of the read, so the lane records the time beside the lines.

## 2. Scope

**The membership, by the block that defines it** (run from the lane's
distribution worktree, stacked on the P1 branch, which holds
`docs/reviews/{inventory.json,slices.json}` at `2174265e9c` -- sha256
prefixes `d17b9cac4b2c2245` (`inventory.json`) and `49bc2745664e52f4`
(`slices.json`), R1 C10, the same as T36's R1 C06). The script is T36's
`membership.py` rewritten for a distribution-side slice (R1 § 4): rows of
`tree == "distribution"`, the slice id `es-recipe`, the labels `in-T37` /
`not-in-T37`; it prints the inventory's distribution header and splits
*Read* by tier beside `vendor-carried lines`; it takes a second argument,
the `ls-tree` of the glob at the P1 hash, and its `CLAIMS` names every one
of those 19 paths plus six neighbours (the two virtual packages that
install T37's packages, the two copies of the ES recipe under
`docs/qa-logs/`, `tools/pkgcheck` and `tools/es-menu-map-check`); `DEPS`
finds the recipe of each of the three recipes' dependencies and its owner;
`RECIPE TREES BY SLICE` replaces T36's `ES-CORE BY SLICE`. **`W` is the P1
research clone and `P1=2174265e9c`; `MB` is the distribution merge base
`c445081a59`.** Keyword arguments are spaced `key = lambda` so this file
carries no key-equals token. **The heredoc is saved once and run twice** --
first against `/dev/null` to make the paths file from its own TSV, then
against that file to prove equality. **The text below is R1's `block.sh`
byte for byte** (115 lines, sha256 prefix `f3ef373be6535467`, R1 C10); R1
ran it unchanged on 2026-10-31 (`W` names a directory that exists) and the
expected lines are that run's, byte for byte; the proof re-ran it from this
brief's own lines and every expected line printed byte for byte (C2):

```bash
mkdir -p .qa-scratch/t37
cat > .qa-scratch/t37/membership.py <<'PYEOF'
import json, re, sys, collections
CODE = {"shell","python","recipe","c","c++","c-header","c++-header","javascript","typescript","make","cmake","systemd","udev","script","perl","lua","rust","go","assembly","shader","docker","kconfig","html","css"}
def gre(g):
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i]=="?": out+="[^/]"; i+=1
        elif g[i]=="{":
            j=g.index("}",i); out+="(?:"+"|".join(gre(x) for x in g[i+1:j].split(","))+")"; i=j+1
        else: out+=re.escape(g[i]); i+=1
    return out
def compile_globs(globs):
    inc=collections.defaultdict(list); exc=collections.defaultdict(list)
    for g in globs:
        neg=g.startswith("!"); g=g[1:] if neg else g
        tree="es" if g.startswith("es:") else "distribution"
        g=g[3:] if tree=="es" else g
        (exc if neg else inc)[tree].append(re.compile(gre(g)+r"\Z"))
    return inc,exc
doc=json.load(open("docs/reviews/slices.json"))
sl=[]
for s in doc["slices"]:
    sels=s.get("select",{}); sels=sels if isinstance(sels,list) else [sels]
    comp=[]
    for sel in sels:
        comp.append((set(sel.get("areas",[s["area"]])), compile_globs(sel["globs"]) if sel.get("globs") else None,
                     set(sel["reach"]) if sel.get("reach") else None, bool(sel.get("rest")), set(sel["tier"]) if sel.get("tier") else None))
    sl.append((s,comp))
inv=json.load(open("docs/reviews/inventory.json"))
hd=inv["header"]["distribution"]
print("distribution head:",hd["head"]); print("distribution merge_base:",hd["merge_base"]); print("distribution upstream:",hd["upstream"],hd["upstream_head"])
cols=inv["columns"]; print("columns:",cols)
rows=[dict(zip(cols,r)) for r in inv["rows"]]
def match(row,areas,comp,reach,tier):
    if row["area"] not in areas: return False
    if reach and row["reach"] not in reach: return False
    if tier and row["tier"] not in tier: return False
    if comp is None: return True
    inc,exc=comp; t=row["tree"]; p=row["path"]
    return any(r.match(p) for r in inc.get(t,())) and not any(r.match(p) for r in exc.get(t,()))
def hits(row):
    non=[s["id"] for s,c in sl if any(not rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)]
    if non: return non,"non-rest"
    return [s["id"] for s,c in sl if any(rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)],"rest"
def globhits(p):
    out=[]
    for s,c in sl:
        for a,cm,r,rest,t in c:
            if cm is None: continue
            inc,exc=cm
            if any(x.match(p) for x in inc.get("distribution",())) and not any(x.match(p) for x in exc.get("distribution",())):
                out.append((s["id"],s["k"],"rest" if rest else "non-rest")); break
    return out
kof={s["id"]:s["k"] for s,_ in sl}
mine=[]
for r in rows:
    if r["tree"]!="distribution": continue
    h,kind=hits(r)
    if h==["es-recipe"]: mine.append(r)
mine.sort(key = lambda r:r["path"])
want=[l.strip() for l in open(sys.argv[1]) if l.strip()]
got=[r["path"] for r in mine]
print("mine:",len(got),"paths.txt:",len(want),"equal:",got==want)
print("only-mine:",sorted(set(got)-set(want))); print("only-paths.txt:",sorted(set(want)-set(got)))
c=collections.Counter
print("lines:",sum(r["lines"] or 0 for r in mine), "reach:",dict(c(r["reach"] for r in mine)),"tier:",dict(c(r["tier"] for r in mine)),"lang:",dict(c(r["language"] for r in mine)))
print("fork-own lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="fork-own"))
rd=[r for r in mine if r["language"] in CODE and r["tier"]!="vendor-carried" and r["reach"]!="unreached"]
print("read lines:",sum((r["lines"] or 0) for r in rd),"of which fork-own:",sum((r["lines"] or 0) for r in rd if r["tier"]=="fork-own"),"vendor-carried lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="vendor-carried"))
print("TSV"); print("\t".join(cols))
for r in mine: print("\t".join(str(r.get(k)) for k in cols))
print("CLAIMS")
byp={r["path"]:r for r in rows if r["tree"]=="distribution"}
tree=[l.strip() for l in open(sys.argv[2]) if l.strip()]
named=tree+["projects/ROCKNIX/packages/virtual/es-themes/package.mk","projects/ROCKNIX/packages/virtual/image/package.mk","docs/qa-logs/2026-10-14-screenscraper-provisioning/attempt02/inputs/baseline/package.mk","docs/qa-logs/2026-10-14-screenscraper-provisioning/attempt02/inputs/candidate/package.mk","tools/pkgcheck","tools/es-menu-map-check"]
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY; globs:",globhits(p)); continue
    h,kind=hits(r); print(p, "in-T37" if p in got else "not-in-T37", kind, [(x,kof[x]) for x in h], "tier",r["tier"],"lines",r["lines"],"lang",r["language"],"area",r["area"])
print("DEPS")
deps=["toolchain","boost","SDL2","freetype","curl","freeimage","bash","rapidjson","SDL2_mixer","fping","p7zip","alsa","vlc","drm_tool","poppler","pugixml","noto-sans-cjk","zstd","Python3","SDL2_image","SDL2_ttf"]
for d in deps:
    rx=re.compile(r"(?:^|/)packages/(?:.*/)?"+re.escape(d)+r"/package\.mk\Z")
    found=sorted(p for p in byp if rx.search(p))
    if not found: print(d,"NO RECIPE IN INVENTORY")
    for p in found:
        h,kind=hits(byp[p]); print(d,p,kind,[(x,kof[x]) for x in h],"tier",byp[p]["tier"])
print("RECIPE TREES BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["tree"]=="distribution" and (r["path"].startswith("packages/") or r["path"].startswith("projects/ROCKNIX/packages/")):
        k=("packages/" if r["path"].startswith("packages/") else "projects/ROCKNIX/packages/",)+tuple(hits(r)[0])+(hits(r)[1],)
        cnt[k]+=1; ln[k]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:(kv[0][0],-kv[1])): print(v,"paths",ln[k],"lines",k)
PYEOF
W=/workspace/tmp/m6-coordinator/t11-research/tree; P1=2174265e9c; MB=c445081a59
git -C "$W" ls-tree -r --name-only "$P1" -- projects/ROCKNIX/packages/ui/ > .qa-scratch/t37/tree.txt
python3 -I .qa-scratch/t37/membership.py /dev/null .qa-scratch/t37/tree.txt > .qa-scratch/t37/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^CLAIMS$/{p=0} p && $1=="distribution" {print $2}' .qa-scratch/t37/block-1.txt > .qa-scratch/t37/paths.txt
wc -l .qa-scratch/t37/paths.txt .qa-scratch/t37/tree.txt
python3 -I .qa-scratch/t37/membership.py .qa-scratch/t37/paths.txt .qa-scratch/t37/tree.txt > .qa-scratch/t37/block-2.txt
/usr/bin/grep -E '^(distribution |mine:|only-|lines:|fork-own lines:|read lines:)' .qa-scratch/t37/block-2.txt
IH=$(sed -n 's/^distribution head: //p' .qa-scratch/t37/block-2.txt)
git -C "$W" ls-tree -r --name-only "$IH" -- projects/ROCKNIX/packages/ui/ | diff - .qa-scratch/t37/paths.txt && echo "ls-tree at the inventory's head = paths.txt"
diff .qa-scratch/t37/paths.txt .qa-scratch/t37/tree.txt; echo "paths.txt against ls-tree at $P1: diff rc=$?"
for p in $(cat .qa-scratch/t37/tree.txt); do git -C "$W" show "$P1:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l, every path at the P1 hash:", s}'
for p in $(cat .qa-scratch/t37/tree.txt); do git -C "$W" show "$P1:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c, every path at the P1 hash:", s}'
for p in $(cat .qa-scratch/t37/paths.txt); do git -C "$W" show "$IH:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c, the inventory paths at its head:", s}'
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t37/tree.txt | wc -l
git -C "$W" diff --shortstat "$MB" "$P1" -- projects/ROCKNIX/packages/ui/
git -C "$W" diff --shortstat "$IH" "$P1" -- projects/ROCKNIX/packages/ui/
```

Expected (the first pass, against `/dev/null`, writes `mine: 15 paths.txt:
0 equal: False` into `block-1.txt`; the block prints these lines, R1 C10's,
byte for byte; the last shortstat, the inventory head to the P1 hash, prints
nothing):

```
  15 .qa-scratch/t37/paths.txt
  19 .qa-scratch/t37/tree.txt
  34 total
distribution head: eb4763e3cc9bcd729830cd85f1719bbd4f28db10
distribution merge_base: c445081a59518f37d9776e5412dd7b14910696f7
distribution upstream: upstream/next c1f1746828ca47dfc751ffe44bb47b6b259883d7
mine: 15 paths.txt: 15 equal: True
only-mine: []
only-paths.txt: []
lines: 4561 reach: {'shipped': 15} tier: {'upstream-carried': 9, 'fork-own': 6} lang: {'shell': 4, 'config': 4, 'recipe': 3, 'systemd': 2, 'text': 1, 'image': 1}
fork-own lines: 572
read lines: 327 of which fork-own: 190 vendor-carried lines: 0
7d6
< projects/ROCKNIX/packages/ui/emulationstation/patches/x86_64/cpugov.patch
15,17d13
< projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/0001-system-style-the-logo-text-for-fullscreen-artwork.patch
< projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-pixelelated-splash.patch
< projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-tools-always-show-image.patch
6a7
> projects/ROCKNIX/packages/ui/emulationstation/patches/x86_64/cpugov.patch
13a15,17
> projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/0001-system-style-the-logo-text-for-fullscreen-artwork.patch
> projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-pixelelated-splash.patch
> projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-tools-always-show-image.patch
paths.txt against ls-tree at 2174265e9c: diff rc=1
wc -l, every path at the P1 hash: 4649
grep -c, every path at the P1 hash: 4650
grep -c, the inventory paths at its head: 4561
14
 8 files changed, 463 insertions(+), 13 deletions(-)
```

The first `diff` (the tree at the inventory's head against `paths.txt`) and
the second (`paths.txt` against the tree at the P1 hash) print the same four
patches from opposite sides: the inventory's 15 are the glob's 19 less the
four, at both hashes (R1 § 4). `14` is the paths of the 19 present at the
merge base -- the 19 less the five fork additions (R1 § 4, C13). `block-2.txt`
also holds the TSV, `CLAIMS` (the 25 named paths), `DEPS` and `RECIPE TREES
BY SLICE`, read with `sed -n '/^CLAIMS$/,$p' .qa-scratch/t37/block-2.txt`
(R1 § 4, § 5; the slice's row there: `15 paths 4561 lines
('projects/ROCKNIX/packages/', 'es-recipe', 'non-rest')`, R1 C11). The
lane's copy of the block in `01-research-notes.md` § Scope is checked
against the prefix above with `sha256sum`, never retyped.

**The bases** (R1 C01, C02, C10, C14, C15). The distribution: `next` is
`8ebaf8daad` (2026-10-17, *browser: record provider pages and GTK4
compilation (#616)*), unmoved (`rev-list --count 8ebaf8daad..next` 0, R1
C01, C08, C20); `2174265e9c` (2026-10-23) is `next` plus 64 commits, none
under `ui/` (R1 C02); the merge base with `upstream/next` is
**`c445081a59518f37d9776e5412dd7b14910696f7`** (2026-10-01, *Merge pull
request #3413 from sunshineinabox/PR_FixCI*), on `upstream/next`'s
first-parent line and equal to the inventory's recorded `merge_base` (R1
C02, C10), brought in by `f370dc8787` (2026-10-12, *distribution: merge
ROCKNIX 20261001 for M7 qualification*, R1 C02); `upstream/next` was
`c1f1746828` (2026-10-23) at the inventory and is `651150fc88` (2026-10-24)
now, `rev-list --count c445081a59..upstream/next` 330 on any path (R1 C02,
C14). The P1 research clone has no `upstream` remote (R1 C01); the lane's
worktree, a worktree of the primary checkout, has it. **The ES side:** the
pin `16dbac5211eea7e70db7394372033be2be7df829` (2026-10-15, *GuiWifi:
cancel scan worker on normal frontend exit*) is the tip of the fork's
`test/qa-integration`, local and `origin` (R1 C15). ROCKNIX's own recipe
pinned `cada856d86` at the distribution's merge base -- which is the pin's
merge base with `rocknix/master` -- then `21439dbc63` at the inventory's
upstream head, and now `f6c542872e`, `rocknix/master` itself (R1 C14,
C15). **Upstream has 14 ES commits the pin lacks (7 first-parent merges),
and the pin is 724 ahead of upstream's current pin** (R1 C15). This
paragraph is the one statement of the bases; § 1's comments, § 5's
expectations and § 7's checkboxes cite it.

**The merge debt, the distribution half** (R1 C13, C14; R1 § 6 D6, D7).
Upstream's **16 commits on `ui/` since the base** (15 to `c1f1746828`; the
sixteenth `b48d63c445`, 2026-10-23, *S922X: enable s2idle suspend*) change
**8 files, `8 files changed, 72 insertions(+), 75 deletions(-)`** (R1 C14):
the tip is **behind** on `es_features.cfg`, `start_es.sh` and
`emustation.service` (blob equal to the merge base and not to
`upstream/next`, R1 C13); **both sides changed** `emulationstation/package.mk`
and `essway.service` (the inventory's `overlap True`, R1 C11, C14); and the
tip **lacks** `patches/RK3566/fix_multistateinput.patch`,
`system.d/emustation.service.d/20-thp.conf` and
`system.d/essway.service.d/20-thp.conf` (R1 C14). What they carry (R2 § 5,
cmd 21, cmd 22): ROCKNIX's pin `cada856d86` to `f6c542872e`; upstream's
**`PKG_PATCH_DIRS+=" ${DEVICE}"`** with the RK3566 patch, whose context
matches the pin (`MultiStateInput.cpp:32-38`, `:50-53`) and which no fork
commit carries; `start_es.sh`'s `prerotate_env` and `scanout_reset_stale`;
`start.games` moving to `/run/rocknix/` in both units; the `20-thp.conf`
drop-ins (`MemoryTHP=system`); 107 lines of `es_features.cfg`; and
`essway.service`'s comment `:4` -- over
`projects/ROCKNIX/packages/ui/emulationstation/system.d/essway.service`,
`git diff -U0 c445081a59 651150fc88` prints upstream's `@@ -4 +4 @@` and
`git diff -U0 c445081a59 2174265e9c` the fork's `@@ -11,0 +12,3 @@` (proof
C15, Correction 13). Upstream's ES-recipe hunks are the distribution half of
the same features as the 14 ES commits (batteryplus, the hidden cursor, the
RP6 and Odin 3 calibration, S922X's s2idle, the scaling settings; the 14
also carry the ZRAM swap menu, `830d370cf` *GuiMenu: add a ZRAM swap menu*
merged by `40343cf6e`, which has no distribution half under `ui/`, proof
C13, Correction 12), so **this recipe's currency moves with the ES merge,
not separately** (R1 C15). **The tip to `upstream/next` over `ui/`** is
` 14 files changed, 83 insertions(+), 536 deletions(-)`
(`git diff --shortstat 2174265e9c 651150fc88 -- projects/ROCKNIX/packages/ui/`,
R1 C14, proof C3): upstream's 8 and the fork's 8, the two `overlap` files in
both -- `upstream-only 6 fork-only 6 both 2` by § 5's `comm` line (v2 read)
-- and **§ 7's currency rows count these 14 files, one row each** (proof
Correction 6). **The theme's and `lowerdeck`'s pins are the same at
all four hashes** (R1 C14). The ES half is § 8's.

**The files** (lines at the tip by `grep -c ''`, the inventory's rule, R1
C07; tier and class R1 C11, C13; the fork's stat column R1 C13's `diff
--stat`; what each is, R2 § 0, § 1, § 2):

| File under `projects/ROCKNIX/packages/ui/` | Lines | Tier; class | Fork stat | What it is at the tip |
| --- | ---: | --- | ---: | --- |
| `emulationstation/package.mk` | 141 | fork-own; fork-modified, overlap | 47 | the ES recipe: a git clone of `pixelelated/emulationstation` (`:8-9`) on `test/qa-integration` (`:6`) at the pin (`:5`), no `PKG_SHA256` (a git source, `GET_HANDLER_SUPPORT="git"` `:17`); `PKG_DEPENDS_TARGET` `:13`; the cmake options `:19-25`; the runtime login `:30`; `BATTERYPLUS` `:33`; `pre_configure_target` `:35-55`, `makeinstall_target` `:57-129`, `post_install` `:132-141` (R1 C08; R2 § 1) |
| `emulationstation/autostart/001-emulationstation` | 13 | upstream-carried | -- | the boot step linking `/storage/.emulationstation` to `/storage/.config/emulationstation` (`:8-12`) |
| `emulationstation/config/common/es_features.cfg` | 2039 | upstream-carried; behind | -- | the per-emulator feature catalogue; `armsx2` at `:1331`, `:1333`, `:1393`; 15 lines name vulkan (R2 cmd 5) |
| `emulationstation/config/common/es_input.cfg` | 1810 | upstream-carried | -- | the controller database (not read by R2: its cap) |
| `emulationstation/config/common/es_savestates.cfg` | 26 | fork-own; fork-added | 26 | the save-state layout, `emulator name="retroarch"` (`dee5d6dd0e`, 2026-09-15, #196) |
| `emulationstation/config/common/es_settings.cfg` | 3 | upstream-carried | -- | an empty `<config>` (`:1-3`; R3 § 2.2 C9) |
| `emulationstation/sources/es_settings` | 52 | upstream-carried | -- | `ExecStartPre`: the timezone, the locale, the environment import |
| `emulationstation/sources/serial_number_check` | 27 | upstream-carried | -- | the serial check |
| `emulationstation/sources/start_es.sh` | 8 | upstream-carried; behind | -- | sources `es_settings` and runs ES (`:6-8`) |
| `emulationstation/system.d/emustation.service` | 20 | upstream-carried; behind | -- | the non-sway unit |
| `emulationstation/system.d/essway.service` | 21 | fork-own; fork-modified, overlap | 3 | the sway unit; `:12-14` `ExecStartPre=/usr/bin/sway-ready`, `TimeoutStartSec=20` (`c6afa31db1`, 2026-10-09); `sway-ready` installed by `projects/ROCKNIX/packages/wayland/compositor/sway/package.mk:46` (R2 cmd 12); no trailing newline (R1 C07) |
| `lowerdeck/package.mk` | 17 | upstream-carried | -- | `bulzipke/lowerdeck` at `ab735114ab` with `PKG_SHA256`, `PKG_TOOLCHAIN="manual"`, the tree copied to `/usr/share/lowerdeck` (`:14-17`) |
| `themes/es-theme-art-book-next/package.mk` | 28 | fork-own; fork-modified | 2 | `anthonycaccese/art-book-next-es` at `9a50ef366e` with `PKG_SHA256`, `PKG_LICENSE="CUSTOM"` (`:5-9`); installed to `/usr/share/themes/es-theme-art-book-next` (`:15-16`) with the wordmark and the licence (`:17-18`, the fork's), five artwork variants removed (`:19`), four of their includes deleted (`:20`, `noir\|nintendont\|circuit\|outline`; `classic` has none, proof C5, Correction 14), a `zh` font block appended to `fonts.xml` (`:21-27`) |
| `themes/es-theme-art-book-next/sources/Tiny5-OFL.txt` | 93 | fork-own; fork-added | 93 | the Tiny5 font licence |
| `themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg` | 263 | fork-own; fork-added | 263 | the wordmark |

Outside the 15, named for their owners (R1 C07, C11, C13; ruling (a)), all
four of inventory tier `vendor-carried`, git's class beside it (proof C2's
`CLAIMS`, C3's name-status; Correction 10):
`emulationstation/patches/x86_64/cpugov.patch` (27, `vendor-carried`; git
upstream-carried; T40),
`themes/.../patches/0001-system-style-the-logo-text-for-fullscreen-artwork.patch`
(20, `vendor-carried`; git upstream-carried; T42),
`themes/.../patches/001-pixelelated-splash.patch` (31, `vendor-carried`; git
fork-added; T42) and `themes/.../patches/001-tools-always-show-image.patch`
(11, `vendor-carried`; git fork-added; T42).

**The fork's commits on `ui/`** (R1 C12, C13): **251 log lines since the
merge base, 5 of them merges** -- all five the fork's merges of
`upstream/next`, kept by history simplification -- **246 non-merge, 241 of
which touch `emulationstation/package.mk`**: the recipe's history is the ES
pin's. First in `git log --reverse` order is `cb50b45f6e` 2026-08-19 (*qa:
take upstream's ES recipe, keep the fork's source*) -- by date the range's
earliest are `6afeaa2681` (2026-07-06) and its revert `5da39f7adf`
(2026-07-07), proof C3, Correction 15 -- and the last `f8636de1d1`
2026-10-15. **The fork's change
against the base: `8 files changed, 463 insertions(+), 13 deletions(-)`**
(R1 C13). Paths added and later removed: `patches/GENERIC_X64/001-generic-x64-request-gles3-context.patch`
(`6afeaa2681`, reverted by `5da39f7adf`), `sources/rasteratops-wordmark.svg`
and `patches/001-rasteratops-splash.patch` (the identity rename,
`3d7c075f63` then `a9af618398`) (R1 C13):
`git log --diff-filter=D c445081a59..2174265e9c -- projects/ROCKNIX/packages/ui/`
prints `a9af618398` and `5da39f7adf`, and the splash patch's removal is a
rename under git's detection, so it shows as no deletion (proof C3). **The fork's hunks in the ES
recipe** (R2 § 0, cmd 4, attributed by commit message, not per hunk):
`:5-13` the source moved from upstream's tarball to the fork's clone, with
`zstd` appended to `:13` (by message `84ff94fb3d`) and `PKG_LICENSE`
changed at `:7` from `GPL` to `MIT` by `3d7c075f63` (2026-10-02) and to
`MIT AND BSD-3-Clause` by `84ff94fb3d` (2026-10-13)
(`git log -L7,7:projects/ROCKNIX/packages/ui/emulationstation/package.mk 2174265e9c`,
proof C5; L-16); `:27-30` the runtime ScreenScraper login (#566, D-WORKFLOW-166);
`:32` a comment over upstream's `BATTERYPLUS` line; `:36-40` the shared
developer identity (`:39` a local whose value no research file reproduces,
`:40` the default form built from it); `:48-50` the log loop printing
`USING: <key> (set)`, never the value (`144b3eccb6`, 2026-09-05); `:58-65`
the RVZ licence files when present; **and upstream's ARMSX2 block removed**
(L-01).

**The neighbours, and whose they are** (R1 § 5, C09, C11, C17, C20; R2 §
1): the four patches are **T40's** and **T42's** (ruling (a));
`projects/ROCKNIX/packages/virtual/image/package.mk` (113 lines, `PKG_UI` at
`:18`) and `virtual/es-themes/package.mk` (9 lines, depending on the theme
at `:7`) are **T8 `image-packages`**'s; of the dependencies, **T8** owns the
`projects/ROCKNIX` overrides (`boost`, `SDL2`, `curl`, `freeimage`,
`rapidjson`, `SDL2_mixer`, `fping`, `p7zip`, `vlc`, `poppler`,
`noto-sans-cjk`, `SDL2_image`, `SDL2_ttf`), **T7 `generic-packages-reached`**
the generic recipes (`toolchain`, `freetype`, generic `curl`, `alsa`,
`pugixml`, `zstd`, `Python3` and **`packages/devel/fribidi`**, 25 lines), **T22 `os-system-services`** `bash` and `drm_tool`, **T23
`packages-dead-ends`** the generic `packages/devel/boost` the override
shadows; `${OPENGLES}` is `mesa` at `projects/ROCKNIX/options:19` (R2 cmd
7) and in the effective value on GENERIC_X64 (R3 § 1.5), and under
`projects/ROCKNIX/` it is set only there and at `devices/AMD64/options:32`,
both `"mesa"`
(`git grep -n -E '^[[:space:]]*OPENGLES=' 2174265e9c -- projects/ROCKNIX`,
proof C14); the two copies of
the ES recipe under
`docs/qa-logs/2026-10-14-screenscraper-provisioning/attempt02/inputs/{baseline,candidate}/package.mk`
(135 and 141 lines) are **T46 `records`**'s, read, if at all, through the
mask (R1 § 5); `tools/pkgcheck` (169 lines) is **T6
`build-engine-upstream-tools`**'s and `tools/es-menu-map-check` **T10
`tooling-guards`**'s; the recipes of fribidi's chain (§ 3 L-09) are
**T8's** `projects/ROCKNIX/packages/virtual/swaywm-env` and
`projects/ROCKNIX/packages/wayland/compositor/sway` (fork-own, 71 lines),
**T7's** `packages/graphics/pango` and `packages/devel/fribidi`, and **T8's**
`projects/ROCKNIX/packages/graphics/SDL2` (`('image-packages', 8)` for
`swaywm-env` and `sway`, `('generic-packages-reached', 7)` for `pango`: the
block's `named` list extended through its second argument, proof C2); the
three scripts outside the slice that use `lowerdeck` at run time (Q5) are
the slices' that the same extended run prints for them; the ES tree is
every `es-*` slice's, with `es-core/CMakeLists.txt` T35's and ES's top-level
`CMakeLists.txt` the integration's (ruling (f)). **The extended run** is the
block's script unchanged, the extra paths appended to its second argument:
`named` is that argument plus the six, so only `CLAIMS` grows and the
block's sha256 still checks; the lane records the eight lines it prints.

```bash
{ cat .qa-scratch/t37/tree.txt; printf '%s\n' projects/ROCKNIX/packages/virtual/swaywm-env/package.mk projects/ROCKNIX/packages/wayland/compositor/sway/package.mk packages/graphics/pango/package.mk packages/devel/fribidi/package.mk projects/ROCKNIX/packages/graphics/SDL2/package.mk projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh projects/ROCKNIX/packages/rocknix/sources/scripts/vertical-check projects/ROCKNIX/packages/wayland/compositor/sway/autostart/111-sway-init; } > .qa-scratch/t37/named-extra.txt
python3 -I .qa-scratch/t37/membership.py .qa-scratch/t37/paths.txt .qa-scratch/t37/named-extra.txt | sed -n '/^CLAIMS$/,/^DEPS$/p' | /usr/bin/grep -E 'swaywm-env|compositor/sway/|graphics/pango|devel/fribidi|graphics/SDL2/|runemu|vertical-check|111-sway-init'
```

**Already found; do not re-find; take up.** Each is cited at its lines in
`02` with a disposition; the states are as R4 read them on 2026-10-31,
re-read at stage A; **asks** is R4 § 1's column -- *read* (state the
contract in `02`), *fix* (a change in the slice's own files, under a stream
brief at the stage-D pause), *integration* (the coordinator's step that the
read must make possible; § 8), *none* (recorded so the lane does not
re-find it); a ruling named by letter is § 1's.

| Found by | Lines at the tip | Take up as |
| --- | --- | --- |
| **D-WORKFLOW-216** (`decision-register.md:776`): *"`HAVE_FRIBIDI`'s undeclared build-order dependency is T37's recipe"*; T36's errata `es-core-utils-resources.md:2145`; the futro `:1004`, `:1008`, `:1010` (R1 C18; R4 item 1; R5 § C) | `emulationstation/package.mk:13` | **fix or read**: declare `fribidi` in `PKG_DEPENDS_TARGET`, or record the transitive chain R2 traced as the recipe's decision -- L-09, Q3; cite T36's G-01 `ldd` line if T36's record holds it for the same image (R5 § A) |
| **D-WORKFLOW-216**: *"the `package.mk:25` define T37's"*, the source list T35's, the bodies T36's; T36's errata `:2146` (R1 C18; R4 item 2) | `emulationstation/package.mk:25` (`-DGLES3=1"`) | **read**: what the define selects at the pin, set unconditionally while `:13` takes `${OPENGLES}` per device; the three empty pairs named for T35 and T36 -- Q2 |
| **T2 PL-029** (Low, `deferred:#684`; T2 `05-punch-list.md:488-500`, `:658`, `:953-957`; `t2-streams.md:103-104`; R4 item 12) | `emulationstation/sources/start_es.sh:8` | **fix** under rule 6 (an upstream surface): `--log-path /var/log`, which `parseArgs` (`main.cpp:75-298`) does not read, dropped -- or kept with the reason; T2's acceptance, a guest's `/var/log/es_log.txt` written after -- Q2 |
| **#1072** (OPEN, `bug`; R4 item 14) | `emulationstation/patches/x86_64/cpugov.patch` and the recipe's patch directories | **fix**: T37's half is the recipe's `PKG_PATCH_DIRS` line, T40's the patch's content and place (ruling (a)); the build is the only proof the patch applies to the pin (#1072 `:29`) -- L-02, Q6 |
| **#613** (OPEN, M7.P5; T2 `01-research-notes.md:142`, `05:623`; R4 item 13) | `emulationstation/package.mk:101` | **read**, and **fix** if the coordinator routes it: the link's target `/usr/config/emulationstation/es_systems.cfg`, independent of `INSTALL` -- L-03, Q2 |
| **#1193** (OPEN, `bug`, T21 PL-05; R4 item 15) | `config/common/es_settings.cfg` and `makeinstall_target:77-78` | **read**: the mode this recipe installs the seed with; the `system.cfg` seed is not under `ui/` -- Q2 |
| **#990** (OPEN, `bug`; R4 item 17) | `emulationstation/package.mk:7` | **read**: the licence expression from the source's licence files, which `tools/rasteratops-identity-check:143`'s fix then reads -- L-16, Q7 |
| T20's records of the RVZ notices (T20 `02:174`, `00:36`, `04:186`; R4 item 18) | `emulationstation/package.mk:58-64` | **read**: cite; the pin's `external/libcheevos/` holds both files the test at `:60` looks for (R2 cmd 28); #528 carries licence publication -- Q2 |
| The credentials (`device-builds.md:528-578`; D-INFRA-006, D-INFRA-007, D-WORKFLOW-166; #566 CLOSED; #586 OPEN, Backlog; #64 OPEN, its checkbox `:54`; R4 item 19) | `emulationstation/package.mk:30`, `:39-44` | **read**: the recipe's credential lines against D-WORKFLOW-166's route, by name only; whether #64's open checkbox is answerable from the recipe -- L-05, L-11, Q4 |
| The build options the neighbours read (T35's brief `es-core-window-input.md:1394-1399`, `:1500-1506`; T35 `02:766`, `:846`, `:883`; R4 items 20, 37) | `emulationstation/package.mk:13`, `:19-25` | **read**: one table of every `-D` the recipe passes, the CMake test it feeds and the branch it selects; no `udev` package in `:13` (T35's G-01 found libudev linked); `HAVE_UDEV`, `_ENABLE_PULSE_`, `_ENABLE_TTS_`, `HAVE_LIBCEC` the branches T35's host did not parse -- Q2, Q3 |
| NDEBUG (T33 `03-retrospective.md:36`; T32 `02:98`; R4 item 21); `CPPHTTPLIB_OPENSSL_SUPPORT` defined nowhere (`es-app-views-scrapers.md:882-887`; R4 item 22) | the build type; `:19-25` | **read**: where NDEBUG comes from; cite the HTTP server's plain-HTTP fact -- Q2 |
| pugixml (T33 `04-analysis.md:175`; T21 `00:143`; T32 `00:35`; R4 item 23) | `emulationstation/package.mk:13`, `:24` | **read**: the image links the system `pugixml` (`-DUSE_SYSTEM_PUGIXML=1`) against the gitlink copy the lanes' harnesses used -- Q3 |
| The theme (D-UI-090, `decision-register.md:391`; R4 items 25, 28) | `themes/es-theme-art-book-next/package.mk:5`, `:7` | **read**: its pin is `upstream/next`'s and its author's `HEAD` at R1 C20's read; the theme draws its own picture (`es-code-traps.md` § The picture beside a game list); `CUSTOM` licence stated from its source -- Q5 |
| **#69** (OPEN; `:52`'s checkbox, the upstream offer, open; D-UI-090; R4 item 26) | `themes/.../patches/001-tools-always-show-image.patch` (T42's text) | **read**: the offer's state; nothing is sent (D-WORKFLOW-165, #585) -- Q5 |
| The splash wordmark (D-WORKFLOW-144, -145, -146; R4 item 27) | `themes/.../package.mk:17-18`; the two `sources/` files; T42's splash patch | **read**: the recipe's copy steps against the rows; the licence shipped with the font's use -- Q5 |
| `lowerdeck` (R4 item 29) | `lowerdeck/package.mk` | **read**: currency (behind its author's `HEAD`, R1 C20) and why it is in `ui/`; installed by `PKG_UI` and used at run time by `runemu.sh:337-338`, `vertical-check:6-7`, `:143`, `:175`, `:180` and `111-sway-init:163-164`, their owners the extended run's (proof C6, Correction 11) -- Q5, Q7 |
| Currency against ROCKNIX's recipe (`release-candidates.md:29`; D-WORKFLOW-024, -162; #791 OPEN, Backlog; R4 item 30) | the 14 files of the tip-to-`upstream/next` difference (§ 2's merge debt) | **read**: one row per file -- upstream moved it, the fork moved it, or both; upstream's change the fork lacks, the fork's own, or a merge pending -- and the ES pin's 14 as #791's input -- Q7 |
| ES PRs through the distribution (D-WORKFLOW-012; #256, #322; R4 item 31) | the recipe | **read**: the recipe's part of the series' buckets -- Q7 |
| The lanes that name the recipe (`es-launch-path.md:384`, `:389-392`; T18 `02:371`; R4 item 32); iterating on ES (`device-builds.md:634-670`; R4 item 33) | `:5`, `:6` | **read**: the pin each kept image carries, from its `os-release` or binary; the bump's steps in the pin table -- Q1 |
| T36's § 5 item 3 and its stage-B lines (`es-core-utils-resources.md:1527-1541`; T36 `02-forward-audit.md:406`, `:461`; R4 items 34, 40) | `:25` | **read** when T36 hands back: the renderer positives and the collision list touch the recipe -- Q2 |
| The pin bump's inputs (R4 items 3 to 11, 39, 41) | `:5`, `:6` | **integration**: § 8 |
| #716 (T1's `post-update`; R4 item 16); rapidjson (R4 item 24); the earlier inherit lists (R4 item 35); #1231 (R4 item 36); T35's `05` (0 lines on the recipe terms, R4 item 38) | -- | **none** |

## 3. The floor: read first, then the leads

**Read first**, in this order, each in this session, and
`01-research-notes.md` says which were read (`working-principles.md` §
Pre-flight). The line numbers are the coordinator worktree's as the research
printed them (R2's header; R3 § 1.2; R4 § 3, cmd 22); the lane re-reads each
with `grep -n '^## '` at `COHASH`:

1. **The rules**, each at the section named; the section's own sentence is
   not repeated here -- open it:

   | Rule | Line | Section | Serves |
   | --- | ---: | --- | --- |
   | `packaging-and-patches.md` | `:20-24`, `:34-36`, `:76-97` | the fields (`PKG_SHA256` required for a download, n/a for a clone), late binding, generating and scoping patches (R2's header; R4 § 3) | Q1, Q6 |
   | `packages/README.md` | `:171`, `:188`, `:205`, `:280` | `configure_package`; late binding; the `pkgcheck` FAIL row (R2's header; R3 § 1.2) | every `package.mk` edit |
   | `device-builds.md` | `:528-578`, `:634-670` | § Build credentials; § Iterating on EmulationStation (`EMULATIONSTATION_SRC` only mounts; to ship, the merge into `PKG_GIT_CLONE_BRANCH` and the `PKG_VERSION` bump) (R4 § 3) | Q1, Q4 |
   | | § After rebasing, item 3 | every field read as the build reads it, through `config/options <pkg>` with `PROJECT`, `DEVICE` and `ARCH` set (R3 § 1.5) -- in the scratch export, ruling (k) | § 5 |
   | `fork-workflow.md` | `:178-179` | a fork-introduced package at its latest release or pinned with a reason (D-WORKFLOW-024; R4 § 3) | Q7 |
   | `release-candidates.md` | `:29` | the EmulationStation pin level with ROCKNIX's master (R4 § 3) | Q1, Q7 |
   | `es-native-ui.md` | `:405-415` | Before the pin moves, the compiler has seen the edit -- the integration's, not this lane's (R4 § 3) | § 8 |
   | `engineering-practices.md` | § Check upstream early; § Verify design intent; § Guards must fail closed; § Capture `rc=$?` on its own line; § Nothing runs on a person's device (the masks) | D-WORKFLOW-162; `git log -S` before each FAIL-first lead; the first PASS is the one to distrust; the read filter and the masking `sed` | § 3, § 5 |
   | `upgrade-and-install.md` | § Every fix answers what was already written | a recipe's `Already written:` line is what an image built from the old recipe left in `/storage` and on the read-only image (D-WORKFLOW-050; R5 § G) | every bug |
   | `generic-x64-vm-testing.md` | § The guest is the candidate image, not the read tree | each G-row preceded by an image-versus-tree comparison (R3 § 3) | § 5 |
   | `bugs-are-agent-first.md` (rule 6), `issue-tracking.md`, `vm-first.md`, `time-to-play.md` | whole | | every bug, § 5, § 7 |

2. **The register** -- § 9.
3. **The menu map**: the recipe holds no menu; `tools/es-menu-map-check`
   reads ES source only (R3 § 5), so this slice cannot move its count and
   writes no map line.
4. **The blindspots** (`docs/blindspot-register.md`): the entries the rules
   above name for a recipe's shapes -- a build that fetches its own
   dependency, a pinned version that is a claim about the image only once
   the image is read, a guard with no observed positive, a figure read off
   the wrong tree -- each found by the lane's `grep -n` for its words
   (`[unverified]`: no research file printed their lines).
5. **The checks that exist for a recipe** (R3 § 1): `tools/pkgcheck` (169
   lines, reads only `package.mk`, FAILs on late binding, a missing brace or
   a duplicate function, WARNs otherwise, `:44-61`, `:63-81`, `:98-112`, exit
   `[ ${FAILS} -eq 0 ]` at `:169`, selection by `find packages projects -type
   f -path */<arg>/package.mk` at `:157`); `config/options` sourcing a recipe
   (197 lines; it reads `${ROOT}/.rocknix/options` at `:134` and
   `${HOME}/.rocknix/options` at `:138-139`, so it runs under `env -i` with
   `HOME` in scratch; and it writes
   `build.<distro>-<DEVICE>.<ARCH>/.cache_package_{local,global}` through
   `config/functions:801-802`, so it runs only in the scratch export, ruling
   (k), proof Correction 1); `calculate_stamp` (`config/functions:1109-1130`: every
   regular non-dot file under the package's directories, so any edit to one
   of the files moves its own package's stamp and nothing else's); `tools/fork-package-freshness`
   and `tools/rc-preflight` (L-10, ruling (e)); `tools/es-syntax-check` exits
   2 on this host (`no build root`, #1137) and has no object in a recipe slice
   (R3 § 1.7). There is no unit-test suite for a recipe; the stand-in is § 5's
   `bash -n`, the sourced-recipe assertions and the install-text assertions.
6. **The walks and the frames**: none; the guest rows are serial reads of
   installed files (§ 5 item 2), and a frame is needed by no row.
7. **The French**: the recipe installs the catalog the ES build makes
   (`makeinstall_target:67-68`, R2 § 1) and carries no player string of its
   own; L-08 is whether a missing catalog is loud.
8. **The audits**, each on its lane's branch, read with `git -C <worktree>
   show <branch>:<path>`, never a checkout (the tips R4 § 1's command 1,
   refreshed in R4 § 9): T2 (`7041b0d710`; PL-029's `05-punch-list.md`),
   T20 (`ffb6b686cb`; the RVZ notices), T21 (`82c67e99c5`; #1193's PL-05),
   T34 (`49c6b43f27`; its `stage-e/` patches and retro), T35 (`7321db61d3`,
   handed back; its `02` § What T36 and T37 inherit at `:871` and its retro
   `docs/retros/2026-10-31-m6-es-core-window-input.md:75-81`, R4 items 37,
   39), and T36 at its tip at stage A (`docs/audits/2026_10_31-epic-m6-es-core-utils-resources`,
   `02-forward-audit.md:406`, `:461`, R4 item 40). The folders' paths are
   read from each branch's `ls-tree`.
9. **The issues**: #684's own body; #1072, #613, #1193, #990, #716 (OPEN,
   `bug`); #69, #64, #256, #322, #585, #528 (OPEN); #566 (CLOSED); #586,
   #1137, #1013, #791 (OPEN, Backlog) (R4 § 4); #700, #682, #683. The lane
   re-reads each with `gh --repo pixelelated/distribution issue view` at
   stage A and records the states it saw.
10. **Time to play**: the recipe sits on **boot to interface**, not on the
    launch path -- `essway.service`'s `sway-ready` wait (`TimeoutStartSec=20`),
    `start_es.sh`, `es_settings`' locale generation, which L-07's silent
    failure moves onto first boot (*"a minute or two on RK3326"*, R2 L-07);
    G-04 reads boot to interface from the guest's journal (R5 § A). The
    retro's line names what the slice costs there, or `CANNOT` with the
    harness's reason, never "nothing".

**The leads, one line each** -- R2's L-01 to L-18 (L-14 and L-15 folded by R2
into its § 0 and § 3, R2 § 6) with R3's readings added as L-19 to L-21, each
at its lines at `2174265e9c`; nothing here was tested, and a lead is a fact of
the lines until the lane's proof says more. **`proved:`** is the research's
column (R2 § 6). **The FAIL-first candidates come first** -- L-02's
never-applied patch, L-03's link, the two fail-open steps L-07 and L-08,
L-04's no-op `rm` -- and each gets its `git log -S` (for a word that is
only a file's name, `git log --diff-filter=A` over the file, L-02) before it
is called a defect (`engineering-practices.md` § Verify design intent). **Every check is a
`tools/pkgcheck` run, a `bash -n`, a sourced-recipe assertion through
`config/options` with `PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64`
(and H700 where the row says) in the scratch export (ruling (k)), an
install-text assertion over the recipe's
functions, a fixture in scratch, or a `git log -S` -- never a build.**

| Lead | Lines at the tip | Shape | proved | Check | Q |
| --- | --- | --- | --- | --- | --- |
| **L-02** | `emulationstation/patches/x86_64/`; the recipe's patch directories; `scripts/unpack:127-128`, `:137-138`, `:150-160` | **`cpugov.patch` never applies**: for `TARGET_ARCH=x86_64` the arch directory searched is `x86`, and the recipe sets no `PKG_PATCH_DIRS` (nothing outside recipes does); its context matches the pin (`ApiSystem.cpp:1062-1069`; the hunk `@@ -745`'s 12 old lines are found at `1061`, so with an offset, proof C14), so it would apply if routed; its body maps GPU governors to `get_available_cpu_governors` in both branches (`cpugov.patch:20-23`, T40's text) (R2 § 3, L-02; R3 § 2.2 C3) | tree, tool-run (R3 § 8: `GENERIC_X64/x86_64: source rc=0 TARGET_ARCH=x86_64 PATCH_ARCH=x86 PKG_PATCH_DIRS=[] -> patches/x86_64/: NOT REACHED`, the same verdict for `H700/aarch64`) | **FAIL-first**: the sourced-recipe patch reach for GENERIC_X64 and H700 prints `NOT REACHED` at the tip, and `t37-checks.sh` step 4 FAILs naming the directory (R3 § 6); `git log --format='%h %ad %s' --date=short --diff-filter=A 2174265e9c -- projects/ROCKNIX/packages/ui/emulationstation/patches/x86_64/cpugov.patch` for intent, which prints `40fce2a089 2026-08-20 amd64: wip am64 changes` (R2 cmd 16; proof C5; `git log -S cpugov` prints no commit, the word being the file's name and not its text, proof C3, Correction 5); the build alone proves the patch applies to the pin (#1072 `:29`, R4 item 14) | Q6 |
| **L-03** | `emulationstation/package.mk:101` (cf. `:100`, a device path) | **the `es_systems.cfg` link's target is a build-host path**: `ln -sf ${INSTALL}/usr/config/emulationstation/es_systems.cfg ${INSTALL}/etc/emulationstation/es_systems.cfg`, dangling on a device; upstream's form too (`upstream/next:75`, merge base `:74`); the M7 candidate's recipe had `/usr/config/...` and no commit in the tip's history carries it (R2 L-03; R3 § 2.2 C1, cmd 22, cmd 23); whether `scripts/install` or `scripts/image` rewrites absolute links: a grep of both for `readlink`, `symlink` or `-type l` found none (proof C7), and neither was read whole `[unverified]` -- the lane's read of both at the tip settles it | tree, history | **FAIL-first**: the install-text assertion "no `ln -s` whose target begins `${INSTALL}`" FAILs at `:101` (R3 § 6 step 5); `git log -S'ln -sf /usr/config/emulationstation/es_systems.cfg' 2174265e9c` prints no commit (R3 cmd 23; proof C14: `[]`); G-03 reads the candidate's link -- its fix, never the tip's behaviour (ruling (h)) | Q2 |
| **L-07** | `emulationstation/package.mk:73-75` (comment `:70-71`); `sources/es_settings:26-35` | **fail-open**: the `en_US.UTF-8` pre-generation by the host's `localedef` ends `\|\| true`, so a failure is silent and first boot pays for it (R2 L-07; R3 § 2.2 C6) | tree | **FAIL-first**: the install-text assertion lists each `\|\| true` with its line, a WARN the lane rules on (R3 § 6 step 5); G-03's `ls -d /usr/config/locale/en_US.UTF-8` (R3 G11) | Q2 |
| **L-08** | the pin's `CMakeLists.txt:565-578` (the message at `:577`, proof C4, Correction 7), `:614-615`; `locale/CMakeLists.txt:9`, `:25`, `:31`; the recipe's `makeinstall_target:67-68` | **fail-open**: with no `msgfmt`, `msgmerge` or `xgettext` on the build host ES prints *"Native language support disabled."* and no error, builds no `.mo`, and the recipe copies whatever `locale/lang/` holds -- French (D-UI-051) silently absent; the tools' provider on the build host is named nowhere: `Dockerfile` and `scripts/checkdeps` carry no `gettext` or `msgfmt` line (proof C6), while `packages/devel/gettext/package.mk` exists and 8 recipes name `gettext:host` -- `packages/devel/autoconf`, `quilt`, `grub` and `shared-mime-info` among them, the ES recipe not (proof C7, C8) -- so the tools would reach ES's configure by build order like fribidi, if at all `[unverified]`: the ES recipe's effective dependency closure walked in the export for a `gettext:host` link settles it, and a build's configure log shows it (R2 L-08, § 1; R3 § 2.1 steps 4-5) | tree | **FAIL-first**: an install-text assertion that `makeinstall_target` refuses when the French `.mo` is missing (no such line at the tip); G-03's `ls -l /usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo` (R3 G6); ES's CMake is read by hash and changed by no one here (ruling (f)) | Q2 |
| **L-04** | `emulationstation/package.mk:79` against `:81-82` | **the no-op `rm`**: `rm -f .../resources/logo.png` runs before `resources/` is created and filled, so it removes nothing and the pin's `resources/logo.png` ships (R2 L-04, cmd 6; R3 § 2.2 C5); its consumer is unread, so a question, not a defect yet | tree | **FAIL-first**: the install-text assertion "no `rm` of a path under a directory a later line of the same function creates or fills" FAILs at `:79` (R3 § 6 step 5); `git log -S'logo.png'` over the recipe for intent, which prints `9f1fab30f6 2025-07-13 projects: add modifications for ROCKNIX`, upstream's first line (proof C14); G-05's `ls -l .../resources/logo.png` (R3 G9) | Q2 |
| L-01 | `emulationstation/package.mk:125-129`; `es_features.cfg:1333`, `:1393`; `projects/ROCKNIX/packages/virtual/emulators/package.mk:47-49`, `:52-55`, `:58-60`, `:87-89`, `:92-94`, `:101-103` | **a merge dropped upstream's ARMSX2 block**: `b9a5d8caf1` (2026-09-24) deletes `armsx2-sa`'s *vulkan driver* feature except on `SM4450\|SM6115\|SM8250\|SM8550\|SM8650`; absent from `a06539d8ec`'s result (2026-09-29, *"Two conflicts, both resolved as the fork's file"*) while its upstream parent `6b344ab54d` had it, and again at `049765fba0`, `fa2990c1e7`, `f370dc8787`; `armsx2-sa` also ships on RK3399, RK3566/RK3576, RK3588, SM8750, S922X and AMD64, which then offer a Turnip driver that is not there -- of the fork's devices, RK3566 (R2 L-01, cmds 17-19) | history | a fixture: upstream's and the tip's two `xmlstarlet` edits reproduced in `python3 -I` with `xml.etree` over a scratch copy of `es_features.cfg` with `DEVICE=RK3566`, counting `//core[@name="armsx2-sa"]//feature[@name="vulkan driver"]` (upstream 0, tip 1, R2 § 6; the proof's read-only count over the tip's catalogue printed `tip armsx2-sa vulkan driver features: 1`, C13): the host has no `xmlstarlet` outside the build container (`command -v xmlstarlet` found none, `xmlstarlet: []`, proof C14; `Dockerfile:27` installs it and `scripts/checkdeps:78` requires it, R2 cmd 22) | Q2, Q7 |
| L-09 | `emulationstation/package.mk:13`; `projects/ROCKNIX/packages/graphics/SDL2/package.mk:47-55`; `.../virtual/swaywm-env/package.mk:14`; `.../wayland/compositor/sway/package.mk:7`; `packages/graphics/pango/package.mk:11`; the pin's `CMakeLists.txt:230-244` | **fribidi is declared only transitively**: ES finds it `QUIET` (`pkg_check_modules(FRIBIDI QUIET fribidi)` `:234-237`, `-DHAVE_FRIBIDI` `:239-241`, else the built-in reordering `:242-244`, never `REQUIRED`); `vlc` builds `--disable-fribidi` (`vlc/package.mk:98`); the chain `SDL2` (`DISPLAYSERVER=wl` and `ARCH` not `arm` add `${WINDOWMANAGER}`) -> `swaywm-env` -> `sway` -> `pango` -> `fribidi` holds on every 64-bit build -- all 15 device `options` set `DISPLAYSERVER="wl"`, every `WINDOWMANAGER` contains `swaywm-env` (14 `swaywm-env`, 1 `weston swaywm-env`) -- and breaks silently if SDL2's `arm` branch or a device's `WINDOWMANAGER` changes; T36's erratum is half right (R2 § 1, L-09, cmds 10-12, 16; the chain confirmed line by line, proof C6, C7); `packages/multimedia/libass/package.mk:11` also depends on fribidi, and whether `vlc` pulls `libass` is not read `[unverified]` -- `vlc`'s effective `PKG_DEPENDS_TARGET` in the export settles it; whether an `arm` build compiles ES is `[unverified]`: `Makefile:50`, `:55`, `:60` and `:65` run `ARCH=arm ./scripts/build_distro` for RK3588, RK3576, S922X and RK3566 (proof C14), and the sourced-recipe assertion for an `arm` plan, in the export, settles whether that plan reaches ES | tree | the sourced-recipe assertion of the effective `PKG_DEPENDS_TARGET` of `SDL2`, `swaywm-env`, `sway` and `pango` for GENERIC_X64, in the export (`device-builds.md` § After rebasing item 3); G-01's `ldd` line; D-WORKFLOW-216 routes the decision here | Q3 |
| L-05 | `emulationstation/package.mk:42-44`; `scripts/get_env:14`; the pin's `CMakeLists.txt:303-305`, `:328-330`; the pin's `es-app/src/scrapers/HfsDBScraper.cpp:1`, `:190`, `HfsDBScraper.h:6`, `Scraper.cpp:33` | the log loop names three of the four forwarded build names: **`HFS_DEV_LOGIN` builds the HFS scraper with no `USING:` line** -- the pin's `CMakeLists.txt:328` `if(DEFINED ENV{HFS_DEV_LOGIN})` and `:329` `add_definitions(-DHFS_DEV_LOGIN=...`, consumed by `HfsDBScraper.cpp:1`, `:190`, `HfsDBScraper.h:6` and `Scraper.cpp:33`, forwarded by `scripts/get_env:14` -- and, by R2, `SCREENSCRAPER_SOFTNAME` (`:303-305`) has no log line either (R2 L-05, which was right; R3 § 2.2 C7's read stopped at `:325`; proof C4, C6, Correction 3) | tree | `git -C "$Q" show "$PIN":CMakeLists.txt \| sed -n 303,330p` through the mask and `git -C "$Q" grep -n -o HFS_DEV_LOGIN "$PIN" -- es-app/src` (names and lines only); then the recipe sourced in a sandbox in the export with placeholder values for the four names, assembled at run time, counting `USING:` lines (R2 § 6: 4 for a loud recipe; 3 at the tip) | Q4 |
| L-19 | `emulationstation/package.mk:14`; `config/functions:1114`, `:1322`, `:1328`, `:1333` | `PKG_NEED_UNPACK="busybox"` is a bare name: `calculate_stamp` adds it as a path, `find -L busybox` relative to `ROOT` finds nothing, and nothing in `scripts/` reads the variable, so busybox's recipe never moves ES's stamp (R3 § 2.2 C4, cmd 16); **upstream's line**: `git show <h>:projects/ROCKNIX/packages/ui/emulationstation/package.mk \| /usr/bin/grep -n '^PKG_NEED_UNPACK='` prints `11:PKG_NEED_UNPACK="busybox"` at both `c445081a59` and `651150fc88`, and `git log -S'PKG_NEED_UNPACK'` names `9f1fab30f6` (2025-07-13, *projects: add modifications for ROCKNIX*) (proof C6, C14) -- a rule-6 candidate | tree, history | the install-text assertion "`PKG_NEED_UNPACK` words resolve to directories" FAILs at the tip (R3 § 6 step 5) | Q3 |
| L-06 | `emulationstation/package.mk:54` | `sed "s#-#_##g"`: GNU sed reads `#g` as a comment, so only the first hyphen becomes `_`; no device name at the tip has one; upstream's line (R2 L-06) | tool-run (`echo a-b-c \| sed "s#-#_##g"` printed `a_b-c`, R2 cmd 10) | `bash -n` and that one-liner; recorded as upstream's, a rule-6 candidate | Q2 |
| L-10 | `tools/fork-package-freshness:16-18`, `:42-44`, `:89-93` | **the freshness tool sees none of the three recipes**: it lists `package.mk` files absent on `upstream/next` plus `EXTRA_PACKAGES="projects/ROCKNIX/packages/network/rclone"`, and all three are present upstream (`--list`: 48 entries, none under `ui/`); were the ES recipe listed, its pin would be measured against `pixelelated/emulationstation`'s own default branch (R2 L-10; R3 § 1.3, cmd 12; R5 § A) | tree, tool-run | `FRESHNESS_BASE=651150fc88 FRESHNESS_HEAD=<the tip> tools/fork-package-freshness --list` (pure git), judged by `lines=48` and `ui=0` from its own output (proof C14), never by its rc, which is 0 even with a ref missing (L-21); its rc 0 is no currency evidence here; whether the three belong in `EXTRA_PACKAGES` is a coordinator question | Q7 |
| L-21 | `tools/pkgcheck:157`, `:169`; `tools/fork-package-freshness:42-43`, `:95`, `:101` | **both checkers pass a name that matches nothing**: `tools/pkgcheck es-theme-no-such-package` prints nothing, rc 0; `fork-package-freshness --help` prints the header row and nothing else (R3 § 1.1, § 1.3, cmd 10); **and a missing ref is a third fail-open**: in a tree with neither `upstream/next` nor `next`, `--list` printed `fatal: bad revision 'upstream/next'` and the rclone line with `rc=0` (`:42` `HEAD_REF=${FRESHNESS_HEAD:-next}`, `:43` `BASE_REF=${FRESHNESS_BASE:-upstream/next}`; proof C8, Correction 16) | tool-run | the control line beside every `pkgcheck` run and the freshness counts with both refs given (§ 5); a **Backlog lead** naming the three fail-opens in the hand-back for the coordinator to file (ruling (d)); both tools are T6's | Q7 |
| L-20 | `emulationstation/config/common/es_settings.cfg:1-3`; the pin's `es-core/src/Settings.cpp:252`, `es-app/src/CollectionSystemManager.cpp:1360-1366` | the recipe's seed is an empty `<config>`, so the default theme is ES's own default, not the recipe's (R3 § 2.2 C9): `mStringMap["ThemeSet"] = "system-theme";` at the pin's `Settings.cpp:252`, and with no set of that name installed `CollectionSystemManager.cpp:1360-1366` picks the first available (proof C13) | tree | `git -C "$Q" show "$PIN":es-core/src/Settings.cpp \| /usr/bin/grep -n '"ThemeSet"'` and `sed -n 1360,1366p` of `es-app/src/CollectionSystemManager.cpp`, both by hash; G-02's installed themes and setting | Q5 |
| L-11 | `emulationstation/package.mk:30`, `:39-40`, `:46` | with `:30` and `:40` both always set, the runtime ScreenScraper rows never appear in a recipe-built image and `:46`'s warning is unreachable for that key -- **D-WORKFLOW-166's design, recorded so no lane "fixes" it** (R2 L-11) | tree | none (design) | Q4 |
| L-12 | `emulationstation/sources/serial_number_check:12`, `:20` | an unquoted `cat ${DEVICE_SERIAL_NUMBER_PATH}`; a typo in a log line; its caller not read (R2 L-12) | tree | `bash -n`; upstream's, outside the lanes (D-UI-079) | Q2 |
| L-13 | `emulationstation/sources/es_settings:12-13`, `:47-50` | two timezone files rewritten in place; unquoted words imported from `999-export` (R2 L-13) | tree | upstream's; a note only | Q2 |
| L-16 | `emulationstation/package.mk:7` | `PKG_LICENSE` changed from `GPL` to `MIT` by `3d7c075f63` (2026-10-02) and to `MIT AND BSD-3-Clause` by `84ff94fb3d` (2026-10-13) (proof C5); the licence set's custody is #528's; #990's tool requires `MIT` (R2 L-16; R4 item 17) | history | `git log -L7,7:projects/ROCKNIX/packages/ui/emulationstation/package.mk 2174265e9c`, which prints both (proof C5) | Q7 |
| L-17 | `device-builds.md` § Iterating on EmulationStation against `emulationstation/package.mk:8` | the rule names `maxengel/emulationstation-next` and `~/Development/emulationstation-next`; `PKG_SITE` is `pixelelated/emulationstation` (R2 § 1, L-17) | tree | a rule fix, the coordinator's sweep, not the lane's edit | Q1 |
| L-18 | `CLAUDE.md` against `scripts/unpack:137-145`, `:159` | *"scope per device with `patches/<DEVICE>/`"* holds only where a recipe sets `PKG_PATCH_DIRS`; the tip's ES recipe sets none (R2 L-18); `scripts/unpack:159` also globs `${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/*.patch` with no `PKG_PATCH_DIRS`, a device scope outside the package's directory (proof C7) | tree | a doc fix (the coordinator's), or upstream's `PKG_PATCH_DIRS+=" ${DEVICE}"` adopted with the RK3566 patch (§ 2's merge debt) | Q6 |

**Not leads** -- recorded so the lane does not re-find them: `xmlstarlet` is
a host tool missing from `PKG_DEPENDS_TARGET`, and the build host provides it
(`Dockerfile:27`, `scripts/checkdeps:78`): not a defect (R2 § 1, cmd 22); the
three recipes' global scope references option variables only (`${OPENGLES}`,
`${BATTERYPLUS_SUPPORT}`, `${PKG_SITE}`, `${PKG_VERSION}`), and `pkgcheck`
agrees (R2 § 1; R3 § 1.2); the three theme patches apply at the theme's pin,
`0001-` before `001-` (R2 § 3, cmd 23); `essway.service`'s `sway-ready` is
installed on every `wl` device (R2 § 0, § 6); image builds never build
`es-unit-tests` (`ES_BUILD_TESTS` OFF, R2 § 1); `EMULATIONSTATION_SRC` only
mounts (R3 § 2.1 step 7); the pin's `external/libcheevos/` holds both RVZ
licence files, so `:60`'s test is true at the pin (R2 cmd 28).

## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its VM
line (D-WORKFLOW-187), in one of the families the earlier briefs used --
**a guard that fails open**, **an install step whose output is not what its
line says**, **a dependency taken by build order**, **a structure or
merge-debt fact**, **a currency fact** -- with the lens, **package currency**,
asked of every recipe: is it at its author's current release or pinned with a
stated reason, and is what it builds what the image carries. The leads are §
3's, cited by number; the FAIL-first ones get their `git log -S` first. The
seven questions are R4 § 1's proposal in the coordinator's order for a recipe
slice (Q1 to Q6 by subject, Q7 the lens's).

- **Q1 The pin and its bump** (`emulationstation/package.mk:5`, `:6`, `:8`,
  `:9`, `:17`; `device-builds.md` § Iterating on EmulationStation;
  `release-candidates.md:29`; D-WORKFLOW-191). State the pin and where it
  sits: `16dbac5211` is the tip of `test/qa-integration`, local and
  `origin`, the same at `2174265e9c` and `next` (blob `98cbc055d83f` at both,
  R1 C08, C15); ROCKNIX's `f6c542872e` is 14 commits the pin lacks, and the
  pin is 724 ahead (R1 C15). **No merged ES tip exists yet**
  (`test/qa-integration` is the pin; R4 item 6), so the lane states the bump's
  inputs (§ 8) and its steps -- the branches merged into the branch `:6`
  names, `:5` moved to that tip, the stamp cleared -- and moves nothing
  (ruling (b)). The pin each kept image carries is read from its
  `os-release` or its binary, never from a sidecar: the image's
  `.identity.json` does not carry the ES pin (#1013, R4 item 10), and the M7
  candidate is the pin plus nine patches (ruling (h); R3 § 2.2 C2). L-17's
  rule drift is recorded for the coordinator's sweep.
- **Q2 The build options, the renderers and the install steps**
  (`:19-25`, `:30`, `:33`, `:54`; `makeinstall_target:57-129`;
  `post_install:132-141`). **One table of every `-D` the recipe passes, the
  CMake test it feeds and the branch it selects at the pin** (R4 item 20):
  `-DROCKNIX=1`, `-DDISABLE_KODI=1`, `-DENABLE_FILEMANAGER=0`, `-DCEC=0`,
  `-DENABLE_PULSE=1`, `-DUSE_SYSTEM_PUGIXML=1`, `-DGLES3=1` (`:19-25`),
  `-DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1` (`:30`), and `-DBATTERYPLUS=1` when
  `BATTERYPLUS_SUPPORT=yes` (`:33`; `H700/options:49` sets it, the CMake test
  `:135-137`) (R2 § 1). **The define D-WORKFLOW-216 hands here:** `:25` is
  `-DGLES3=1"`, and **the recipe carries no `-DUSE_OPENGLES_30`** -- ES's
  CMake derives it: the four graphics options are mutually exclusive
  (`CMakeLists.txt:3-16`), `GLES3` gives `GLSystem "OpenGL ES 3.0"`
  (`:164-165`) and `find_package(OpenGLES3 REQUIRED)` (`:213-214`), and that
  one `GLSystem` value both adds `-DUSE_OPENGLES_30` (`:362-363`) and lists
  `Renderer_GLES30.{h,cpp}` (`es-core/CMakeLists.txt:278-280`, whose `:278`
  is `if(${GLSystem} MATCHES "OpenGL ES 3.0")`): the define does not compile
  the source, `GLSystem` selects both (proof C4, Correction 8);
  `Renderer_GLES20` is never compiled
  (`:281-283`, the else); `Renderer_GL21` and `Renderer_GLES10` are listed
  unconditionally (`:110-111`, `:244-245`) (R2 § 1, cmds 8-9). No device
  `case` surrounds `:25`, so every device builds the GLES 3.0 renderer (R2 §
  1); `${OPENGLES}` is `mesa` wherever `projects/ROCKNIX/` sets it
  (`options:19`, `devices/AMD64/options:32`, proof C14), and which devices'
  `mesa` builds provide GLES 3 headers was not read `[unverified]` (R4 item
  2) -- mesa's effective options per device in the export, or an image
  build, settle it. The bodies are T36's and the source list T35's
  (D-WORKFLOW-216); the lane names them for their owners. The effective
  options on GENERIC_X64: `BATTERYPLUS_SUPPORT` empty, `VULKAN_SUPPORT=yes`
  (so `:126-128` keeps the vulkan choices; `no` on H700),
  `EMULATION_DEVICE=yes` (no stub `es_systems.cfg`, `:105-123`) (R3 § 1.5;
  proof C8). `:54` exports `DEVICE`
  upper-cased for `CMakeLists.txt:115-117` (L-06). Where NDEBUG comes from is
  the build type's, not a line of this recipe (R4 item 21). **The install
  steps, one row each** (R2 § 1's table): the RVZ licence files `:60-65`; the
  locale tree `:67-68`; the pre-generated locale `:73-75` (L-07); the
  `.cfg` seeds `:77-78`, with their modes (#1193); the no-op `rm` `:79`
  (L-04); the resources and the CJK fallback link `:81-85`; the three sources
  `:87-90`, which reach `${PKG_BUILD}` because `scripts/unpack:65`,
  `:107-108` copies `${PKG_DIR}/sources/*` into the unpack; the binary `:94`;
  the timezone link `:96-97`; the themes link and **the `es_systems.cfg`
  link** `:99-101` (L-03, #613); the tools-only `es_systems.cfg`
  `:105-123`; the vulkan deletion `:126-128` and the lost ARMSX2 block
  (L-01); the locale links `:132-141`; with PL-029's `start_es.sh:8` flag and
  L-08's silent catalog beside them. The units and `autostart/` are installed
  by the build system's directory conventions, not by the recipe:
  `scripts/install:96-99` copies `autostart/*` to `/usr/lib/autostart/common`
  and `:107-109` `system.d/*.*` to `/usr/lib/systemd/system`
  (`git show 2174265e9c:scripts/install | sed -n '96,99p;107,109p'`, proof
  C7; R2 § 1).
- **Q3 The dependencies** (`:13`; L-09, L-19). The effective
  `PKG_DEPENDS_TARGET` on GENERIC_X64 is `boost toolchain SDL2 freetype curl
  freeimage bash rapidjson SDL2_mixer fping p7zip alsa vlc drm_tool poppler
  pugixml noto-sans-cjk zstd mesa` (`${OPENGLES}` = `mesa`, R3 § 1.5), and
  the same on H700 (proof C8);
  **fribidi** is L-09's chain and D-WORKFLOW-216's question: declare it in
  `:13`, or record the transitive chain as the recipe's decision with the
  `QUIET` branch named -- a ruling put to the pause, never made by the lane,
  and an image build is the only proof of either (§ 8). **udev**: `:13`
  names no udev package, and T35's G-01 found libudev linked (R4 item 20);
  recorded as build order like fribidi. **pugixml**: the image links the
  system package (`-DUSE_SYSTEM_PUGIXML=1`, `:24`, with `pugixml` in `:13`),
  where the lanes' harnesses used the ES gitlink's copy (R4 item 23). The
  owners of every dependency's recipe are § 2's neighbours, and `${OPENGLES}`
  under `projects/ROCKNIX/` is set only at `options:19` and
  `devices/AMD64/options:32`, both `"mesa"` (§ 2; proof C14).
- **Q4 The build credentials, by name** (`pre_configure_target:35-55`;
  `device-builds.md:528-578`; D-INFRA-006, D-INFRA-007, D-WORKFLOW-166).
  The recipe passes nothing to cmake explicitly: ES's CMake reads each name
  from the environment -- `SCREENSCRAPER_DEV_LOGIN` (`CMakeLists.txt:307-309`),
  `GAMESDB_APIKEY` (`:320-322`), `CHEEVOS_DEV_LOGIN` (`:324-326`),
  `HFS_DEV_LOGIN` (`:328-330`, consumed by the HFS scraper; L-05), plus
  `SCREENSCRAPER_SOFTNAME` (`:303-305`) and `SCREENSCRAPER_RUNTIME_DEV_LOGIN`
  (`:311-318`) (R2 § 1); `scripts/get_env:14` keeps exactly four names and
  `:15` drops the rest secret-shaped (R2 § 1; R3 § 2.2 C7, cmd 18); the log
  loop `:42-52` names three; `:40` always supplies a pair, so the warning at
  `:46` is unreachable for that key (L-11, the design). **The answer is
  names, lines and routes only:** the recipe is read through the mask, `:39`'s
  value is never printed, and the binary cannot show the names, because the
  macro names do not survive compilation (R3 G5); whether #64's open
  checkbox (`:54`) is answerable from the recipe is stated; replacement
  credentials are #586's, not a current gate.
- **Q5 The themes and `lowerdeck`** (the theme's `package.mk`; D-UI-090;
  D-WORKFLOW-144, -145, -146). The theme is pinned at
  `9a50ef366e750aabfab29e6915a2867607212971`, the same commit `upstream/next`
  pins and its author's `HEAD` at R1 C20's read, with `PKG_SHA256`
  `7ee1e93f2c4e4f7385b78680ecfa3828acf12bc616e2111d23cc66a524231125` (R1 C08,
  C14, C20; R3 § 1.5); **no pin reason is stated, and none is required**,
  because D-WORKFLOW-024's tool does not reach it (L-10). Its install steps
  (`:14-28`), its three patches (T42's text; they apply, R2 § 3), the
  upstream offer of the Tools-icon patch (#69's open checkbox, D-UI-090,
  nothing sent), the wordmark and the font licence copied beside the font's
  use, the default theme (L-20), and the theme drawing its own picture
  (R4 item 28) are each stated at their lines. **`lowerdeck`** is pinned at
  `ab735114ab318a84e4d28c9c5f1b154e450a579a` with `PKG_SHA256`
  `2677d3ce675b9704487f9f09f82728b56009f9fa7c36403086e9c655af108f42`,
  `GPL-2.0-or-later`, ROCKNIX's pin too (R1 C08, C14; R3 § 1.5; R4 § 0),
  and **behind its author's `HEAD` `8fefe16e9c`** at R1 C20's read, by a
  number of commits nobody counted (no fetch, ruling (e)). **`PKG_UI`
  installs it**: `virtual/image/package.mk:18` assigns `PKG_UI` with no
  device test and `:42` consumes it in the `else` of `:36`'s
  `if [ "${BASE_ONLY}" = "true" ]`, and the effective `BASE_ONLY` is empty on
  GENERIC_X64
  (`git show 2174265e9c:projects/ROCKNIX/packages/virtual/image/package.mk | /usr/bin/grep -n -E 'PKG_UI|BASE_ONLY'`,
  proof C7, C8; R1 C09). **Three scripts outside the slice use it at run
  time** -- `projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh:337-338`
  (`python3 /usr/share/lowerdeck/ra_proxy.py`), the same directory's
  `vertical-check:6-7`, `:143`, `:175`, `:180`, and
  `projects/ROCKNIX/packages/wayland/compositor/sway/autostart/111-sway-init:163-164`
  (`git grep -n lowerdeck 2174265e9c -- projects packages`, proof C6,
  Correction 11) -- each owned by the slice § 2's extended `named` run
  gives its path. **A bump of either is a finding with its reason** (ruling
  (b)).
- **Q6 The patches and their directories** (`scripts/unpack:124-160`;
  `packaging-and-patches.md:76-97`; L-02, L-18). The reach of every
  `patches/` subdirectory of the three packages, computed per device from
  the sourced recipe: the glob list at `scripts/unpack:150-160` (R3 § 8,
  quoted there whole), `PATCH_ARCH` `x86` for an `x86_64` target
  (`:127-128`), and the recipe's `PKG_PATCH_DIRS`, unset (R3 § 8: NOT
  REACHED for `patches/x86_64/` on GENERIC_X64 and on H700; the lane extends
  it to every device in the plan; `:159`'s device directory outside the
  package, L-18). **T37's line is the recipe's patch
  directories; the patch's text and place are T40's** (ruling (a), #1072).
  Upstream's `PKG_PATCH_DIRS+=" ${DEVICE}"` with the RK3566 patch is the
  shape a recipe uses for device patches (§ 2's merge debt; L-18). The theme
  patches apply in name order, `0001-` before `001-p` before `001-t` (R2 § 3),
  and two share the `001-` prefix (R4 item 27); the GLES 3.0 context patch
  the fork added and reverted is history only (R1 C13).
- **Q7 Package currency against upstream's recipe, the structure and the
  #585 lines** (D-WORKFLOW-024, -162, -164, -165, -012; `time-to-play.md`).
  **One row per file of the tip-to-`upstream/next` difference over `ui/`**
  (` 14 files changed, 83 insertions(+), 536 deletions(-)`, § 2; proof
  Correction 6), each saying whether upstream moved it (one of the 8 of § 2's
  merge debt), the fork moved it (one of the fork's 8), or both (the two
  `overlap` files; `upstream-only 6 fork-only 6 both 2`, § 5): upstream's
  change the fork lacks (the RK3566 patch and
  `PKG_PATCH_DIRS`, the THP drop-ins, `start_es.sh`'s two functions, the units'
  `start.games` path, `es_features.cfg`'s 107 lines, L-01's ARMSX2 block), the
  fork's own (§ 2's hunks), or a merge pending (the ES 14, #791's input) --
  **each a finding with its reason, never a merge here** (the distribution
  merge is `release-candidates.md` step 0's, R3 § 1.8). The tools that would
  measure currency and do not: L-10, L-21. The licence expression (L-16,
  #990). The recipe's part of the upstream PR series (D-WORKFLOW-012: an ES
  change reaches upstream as the package bump plus patches in the
  distribution). **The #585 lines owed**: one for each upstream-carried
  defect the lane proves -- L-03's link is upstream's form (R3 cmd 23), L-06's
  `sed` upstream's line, L-19's bare `PKG_NEED_UNPACK` upstream's line
  (proof C6) -- in the shape the lane writes, never sent
  (D-WORKFLOW-164, -165). The cost of a recipe's choice to the player is
  boot to interface (§ 3 item 10).

## 5. The evidence floor

1. **Can this be done on the VM? Yes for the reads and for what the image
   installed; no for the tip's recipe output -- the host first, then one
   guest window granted on #684.** Every read, count and table runs on the
   host at the tip's bytes; **no build runs** (a slice builds nothing), so
   **no image of the tip's recipe exists**, and a guest can show only what
   the M7 candidate installed (R3 § 3). The candidate's `ui/` differs from
   the tip's **only** in the ES `package.mk` (blob `35e5f45e79` against
   `98cbc055d8`) and nine ES patches; the theme, `lowerdeck`, the cfgs, the
   sources, the units and the autostart file are byte-identical (R3 § 2.3,
   cmd 21). So each G-row is labelled by side: **`ui-equal`** where the
   installed file comes from a `ui/` file identical in both trees, read as
   the tip's; **`candidate`** where it comes from the candidate's own recipe
   or ES (the link, the patches, the binary), read as *what the M7 line
   shipped*, never as the tip's behaviour (ruling (h)). What only a build
   can show -- a stamp, the `USING:` lines, the gettext pass, the CMake cache
   (`HAVE_FRIBIDI`, `HAVE_INTL`), the tip's recipe output, the H700 and SM8550
   branches, upstream's RK3566 patch -- is `CANNOT` for this slice and the
   integration's (R3 § 3; § 8). No record of the candidate's build log was
   found (R3 § 2.3).
2. **The guest window** -- one, asked for on #684 at stage B's end with its
   plan and bound (**15 minutes proposed, plus 5 of grace, one boot at
   640x480**: the plan below sums to 780 s, 13 minutes, by `printf '%s\n' 60
   120 120 180 120 60 120 | awk '{s+=$1} END {print s}'`, which printed
   `780`, R5 § A, C14; T36's was 25 + 5 for 1,080 s with two boots, R5 §
   A), granted explicitly by the coordinator on #684 and in the shared log's
   queue. **The queue is the shared file's own lines**,
   `/workspace/tmp/m7-m6-host-coordination.txt` (M7 writes timestamped
   lines, so the whole tail is read): a request is a line that names the
   slice, its plan and its bound; the grant is the coordinator's line
   answering it; the lane's START and RETURN each add a line with the
   census; the window queues behind T36's slot and behind any open M7
   standing or compile START (#1293; R5 § A). **The conditions, stated here
   once -- T13's (#660), whose shape every later window kept:** a **fresh
   disk** made from the M6 copy of the candidate image in its own directory
   under `/workspace/tmp/m6-t37/` (`gunzip`, `qemu-img convert`, `resize`
   to 16G), **never the `t2.qcow2` beside it**, which is a prior lane's guest
   with state (R3 § 2.3, § 3); the image is
   `/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`
   (2,122,289,964 bytes, its `.sha256` `6b4c3079bdee2f47bd1149aac07b11714c591b847f22157fcd6d85f39a7e08fb`,
   R3 § 2.3), started at 640x480 (`generic-x64-vm run --headless --daemonize
   --res 640x480`, #1141); **the image identified by two literals first**
   (`BUILD_ID` from `/etc/os-release` and the file name); every verdict
   labelled by side (item 1); headless, `tools/vm-serial` only; **every read
   through the device read filter** (`grep -v -i -E
   'key|pass|token|user|psk'`, or the masking `sed` of
   `engineering-practices.md` where the line's presence is the evidence);
   **no setting written, no reboot after first boot, no game, no cloud, no
   QA account** (R3 § 3); the post contract `START HH:MM:SS UTC` / `RETURN
   HH:MM:SS UTC` as the first line of each post on #684 and a line in the
   shared host file, each with the census (`qemu N, compilers N`); **the
   START post names the detached timer that stops the guest at bound plus
   grace, or says that nothing does** (`engineering-practices.md` § A
   granted guest window names what stops the guest, #1135); the stop by
   pidfile (`tools/vm-stop`, never a pattern); the disk retired after with
   path, size and sha (D-INFRA-022); the guarded `tools/build-preflight
   --reclaim-swap` allowed once, before the guest, never beside it. **Each
   row's precondition is a booted guest at the interface and nothing more**
   (R5 § B item 11).

   | G | What only the installed image shows | Serial command (over `tools/vm-serial sh`, filtered) | Expected line | Side | Bound (s) |
   | --- | --- | --- | --- | --- | ---: |
   | G-01 | identity; the binary; the libraries | the file name by `ls -l` on the host; `grep -E '^(BUILD_ID\|BUILD_BRANCH\|BUILD_VERSION)=' /etc/os-release`; `sha256sum /usr/bin/emulationstation`; `ldd /usr/bin/emulationstation \| grep -c -E 'fribidi\|vlc\|freetype'` and the same without `-c` | `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`, `BUILD_BRANCH="build/m7-signin-20261022-07"`; the binary `25155163fd7970f7da54b3f36d003b8c006111c894d4fe6f0c92d24d51831226` (R3 § 2.3, G1, G2); the three libraries' lines as they print -- the `HAVE_FRIBIDI` answer for the candidate's build (L-09); **T36's G-01 reads the same `ldd`: if T36's RETURN record holds it for this image, T37 cites it and does not repeat it** (R5 § A) | candidate | 60 |
   | G-02 | the themes installed, and the default | `ls /usr/share/themes/`; in `es-theme-art-book-next/`: `ls pixelelated-wordmark.svg Tiny5-OFL.txt`, `ls -d _inc/systems/artwork-*`, `grep -c -E 'include name="(noir\|nintendont\|circuit\|outline)"' theme.xml`, `grep -c 'lang="zh"' fonts.xml`, a line each fork patch adds; `readlink /etc/emulationstation/themes`; `cat /usr/config/emulationstation/es_settings.cfg`; `grep -i theme /storage/.config/emulationstation/es_settings.cfg` | the two fork files present; the five removed sets absent (`:19`); `0` (`:20`); `>= 1` (`:21-27`); both patches' lines present (R3 G3); `/storage/.config/emulationstation/themes` (`:100`); the empty `<config>`; the default the image chose (L-20: ES's `ThemeSet` default `system-theme`, else the first available set; R3 G4) | ui-equal | 120 |
   | G-03 | the configs, the link, the catalog and the locale | `sha256sum /usr/config/emulationstation/*.cfg` against the tree's `git show 2174265e9c:<path> \| sha256sum` on the host; `grep -c -i vulkan /usr/config/emulationstation/es_features.cfg`; `readlink /etc/emulationstation/es_systems.cfg` then `test -e /etc/emulationstation/es_systems.cfg; echo "resolves rc=$?"`; `stat -c '%a %n' /usr/config/emulationstation/*.cfg`; `ls -l /usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo`; `readlink /usr/share/locale /usr/lib/locale`; `ls -d /usr/config/locale/en_US.UTF-8` | the four cfg digests equal to the tree's -- `es_features.cfg` included: the effective `VULKAN_SUPPORT=yes` on GENERIC_X64 (`no` on H700) means the tip's `:126-128` does not run there (R3 § 1.5; proof C5, C8), and the candidate's own recipe is another blob (`35e5f45e79`), so the line that prints is recorded; vulkan `> 0` (R3 G12); the candidate's `/usr/config/...` link, resolving (L-03; R3 G8); the seeds' modes (#1193); the catalog present (L-08; R3 G6); `/storage/.config/locale` (`:134`); the pre-generated locale present (L-07; R3 G11) | the cfgs ui-equal; the link candidate | 120 |
   | G-04 | the services, the start and boot to interface | `systemctl show -p ActiveState,FragmentPath essway.service emustation.service`; `systemctl cat essway.service`; the `.wants` links; `sha256sum /usr/bin/start_es.sh /usr/bin/es_settings /usr/bin/serial_number_check` against the tree's on the host; `ls -l /var/log/es_log.txt`; the running ES's `cmdline` through the masking `sed`; `journalctl -b` for the interface's start, filtered | the fork's three lines in `essway.service` (R3 G13; `is-enabled` reads `disabled` for image-linked units, per the rule); the three digests equal to the tree's (R3 G14); whether `--log-path` is passed and `es_log.txt` written (PL-029, R4 item 12); boot to interface in seconds, the guest's (time to play) | ui-equal | 180 |
   | G-05 | the sources, the binary's strings and the resources | `head -n 5 /usr/bin/es_settings /usr/bin/serial_number_check` (read, never run); `strings /usr/bin/emulationstation \| grep -c -E 'SCREENSCRAPER_DEV_LOGIN\|SCREENSCRAPER_RUNTIME_DEV_LOGIN\|GAMESDB_APIKEY\|CHEEVOS_DEV_LOGIN\|HFS_DEV_LOGIN'`; `strings /usr/bin/emulationstation \| grep -c 100-amd64-freqfunctions`; `tools/pixelelated-state-check` on the ready guest; `ls -l /usr/config/emulationstation/resources/logo.png`; `readlink /usr/config/emulationstation/resources/DroidSansFallbackFull.ttf` | **counts only, never a line**: the names `0` -- the macro names do not survive compilation, so the binary cannot show presence by name, and a compiled pair's presence is the state check's value-free line (R3 G5; #565; its guest invocation `[unverified]`); `0` for the patch's string (L-02's shape, R2 § 6); `logo.png` present (L-04; R3 G9); `.../noto-cjk/NotoSansCJKsc-Regular.otf` (`:83-85`; R3 G10) | candidate | 120 |
   | G-06 | `lowerdeck` on GENERIC_X64 | `ls /usr/share/lowerdeck` | present, by the tip's recipes: `PKG_UI` names it at `virtual/image/package.mk:18` with no device test, consumed at `:42` unless `BASE_ONLY` is `true`, and the effective `BASE_ONLY` is empty on GENERIC_X64 (Q5; proof C7, C8); the line that prints is recorded (R3 G16) | ui-equal | 60 |
   | G-07 | close | `tools/vm-stop` on the pidfile; the disk's size and sha; `qemu 0, compilers 0` | `retired.txt`; the leftover check; the RETURN post inside bound plus grace | -- | 120 |

   Sum of the bounds as written: 780 s, R5 C14's command over these seven
   numbers. **The guest writes nothing** -- no row writes a file, a setting
   or a stamp -- and § 10's never-run list says the same in the same words
   (R5 § B item 7).
3. **The stand-in, and the lane's checker.** No compiler and no build;
   what runs is `bash -n` on the three recipes and the four scripts (rc 0
   for all seven at the tip, R3 § 4, cmd 23), the sourced-recipe assertions
   (§ 1.5's table; extendable to H700 and SM8550 the same way, R3 § 4), and
   `tools/pkgcheck` with a match assertion. **At stage C the lane writes
   `tools/t37-checks.sh`** under the audit folder's `tools/`, in R3 § 6's
   eight steps: (1) the inventory, 19 entries at the commit (15 plus the 4
   patches) or the named delta, with the `ui/` tree hash; (2) `bash -n` on
   the seven, one `rc=N <path>` line each; (3) for each recipe name, exactly
   one `find packages projects -path */<name>/package.mk` match, then
   `tools/pkgcheck <name>` rc 0 with no FAIL line; (4) the sourced-recipe
   assertions per device under `env -i` with `HOME` in scratch, in the tree
   `--tree` names, which is the scratch export and never the worktree (ruling
   (k)) -- the ES
   `PKG_VERSION` equal to the expected pin and 40 hex, `PKG_URL` on
   `github.com/pixelelated/`, the theme's and `lowerdeck`'s `PKG_SHA256` 64
   hex, no empty expansion in `PKG_DEPENDS_TARGET`, `PKG_CMAKE_OPTS_TARGET`
   carrying `-DGLES3=1` and `-DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1`, the
   computed `PATCH_ARCH` and `PKG_PATCH_DIRS`, and **every `patches/<sub>/`
   directory reached by some glob for some listed device, else FAIL naming
   it** (L-02); (5) the install-text assertions over `makeinstall_target` and
   `post_install` -- no `ln -s` whose target begins `${INSTALL}` (L-03), no
   `rm` of a path under a directory a later line of the same function creates
   or fills (L-04), each `|| true` listed with its line (L-07, a WARN the
   lane rules on), `PKG_NEED_UNPACK` words resolving to directories (L-19),
   and the French catalog asserted (L-08); (6) the text checks -- non-ASCII
   0, the credential scan 0 per file (counts only) **in the hooks' own form,
   not R3 § 6's `grep -c -E -f .githooks/secret-patterns`**: the file is a
   shell file that `.githooks/guard-lib:31-33` sources for one
   `SECRET_PATTERNS` regex, compile-checked at `:40-42` (`printf '' | grep
   -E -e "$SECRET_PATTERNS"`, rc at most 1), and as a `-f` list it does not
   compile (`.githooks/secret-patterns:6: Unmatched ( or \(`, the drafter's
   run on 2026-10-31, and the proof's, `rc=2`, C12) -- so the step is `( . .githooks/secret-patterns; grep
   -c -E -e "$SECRET_PATTERNS" <file> )` after the compile check, with a
   positive assembled at run time seen to match first (in this form the
   proof's planted private-key header line matched `1` and a plain line `0`,
   C13), `tools/forbidden-terms-check --stdin` rc 0 after a planted positive,
   XML well-formedness of the four `.cfg` (`python3 -I` with `xml.etree`);
   (7) `calculate_stamp` per package per device, in the export, to `stamps.txt`, and with
   `--compare` each changed stamp belonging to a package whose directory the
   diff touched and no other moved (R3 § 1.6); (8) **the FAIL-first
   positive**: the script run against a scratch export (`git archive <commit>
   | tar -x -C <scratch>`, never a checkout) carrying one mutation per
   assertion -- a global-scope `${PKG_BUILD}` line, the theme's `PKG_SHA256`
   emptied, `PKG_VERSION` abbreviated, an `ln -sf ${INSTALL}/x` restored on a
   fixed tree, a `patches/nowhere/` directory added, a non-ASCII byte --
   requiring **exit 1 naming each mutation's assertion and exit 0 on the
   unmutated export**, the stub checked against the unfixed text first
   (`engineering-practices.md` § Guards must fail closed). Refusals exit 2,
   "nothing checked": no tree, no `config/options`, a `HOME` that is not
   scratch, a `--tree` that is a git worktree (a `.git` in it, ruling (k)),
   `bash` or `python3` missing. Each command's `rc=$?` on its own
   line; the last line `TOTAL: <passed> of <checks> assertions` printed by
   the script, quoted, never summed by hand. **At the tip it is expected to
   FAIL on L-03, and on L-02, L-19 and L-04 if the lane's tracing confirms
   them** -- that run is the record's FAIL-at-tip (R3 § 6).
4. **A fix lands only under a stream brief** at the stage-D pause, on the
   distribution branch, in the 15, proven twice: **`fix-fixture`** (the
   checker's assertion FAILing on the tip's text and PASSing on the fix's,
   both lines recorded) and **`fix-image-pending`** (what only the
   integration's image build shows -- the link on the image, the patch
   applied, the catalog built), never claimed proven by the lane. After every
   `package.mk` edit `tools/pkgcheck <name>` by name; after every script edit
   `bash -n`; after either the sourced-recipe assertions and the stamps
   compared, **each fix moving exactly its own package's stamp** (R3 § 1.6).
   **No stream changes `PKG_VERSION` or `PKG_GIT_CLONE_BRANCH` of the ES
   recipe** (ruling (b)); a fix that needs ES, a dependency's recipe,
   `virtual/image/package.mk` or a patch's text names its owner at the pause
   (rulings (a), (f)). A fix's `Already written:` line says what an image built
   from the old recipe left -- on the read-only image, replaced by the next
   image, or in `/storage`, which the next image does not replace
   (`upgrade-and-install.md`; D-WORKFLOW-050).

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...*; **the block below captures neither exit nor time
except where it says `rc=$?`; the lane wraps each run in its own `rc=$?` line
and a `date +%s` pair, or records that it did not**; a run that cannot be
made is `CANNOT` with its reason). From the distribution worktree after the
membership block, under bash with `LC_ALL=C`; counts by `/usr/bin/grep`;
**every read of `emulationstation/package.mk` goes through the mask and never
prints `:39`**; `rc=$?` on its own line, never after a pipe; **no `cut`
truncates an expected error line**:

```bash
export LC_ALL=C; G=/usr/bin/grep; P1=2174265e9c; MB=c445081a59; UN=651150fc88; U=projects/ROCKNIX/packages/ui/; E=${U}emulationstation/package.mk
Q=/home/max/Development/emulationstation-next.worktrees/qa-integration; PIN=16dbac5211eea7e70db7394372033be2be7df829
export TMPDIR=/workspace/tmp/m6-t37/tmp; mkdir -p "$TMPDIR/home"; df -i /workspace | tail -n 1
M='s/((token|key|pass(w[a-z]*)?|psk|user|login|devid|apikey) *[=:] *)[^ "]*/\1***/Ig'   # the read mask, widened from engineering-practices.md's as R1 C19 did; `pass(w[a-z]*)?` covers the second ScreenScraper parameter name
# the scope (expect 19 at the tip and 15 in paths.txt -- R1 C07, C10)
git ls-tree -r --name-only "$P1" -- "$U" | wc -l; wc -l < .qa-scratch/t37/paths.txt
# the lines two ways (expect `wc -l` 4649 and `grep -c` 4650 over the 19, 4561 over the 15, the four patches 89 -- R1 C07, C10, C20)
for p in $(git ls-tree -r --name-only "$P1" -- "$U"); do git show "$P1:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l 19:", s}'
for p in $(git ls-tree -r --name-only "$P1" -- "$U"); do git show "$P1:$p" | $G -c ''; done | awk '{s+=$1} END {print "grep -c 19:", s}'
for p in $(cat .qa-scratch/t37/paths.txt); do git show "$P1:$p" | $G -c ''; done | awk '{s+=$1} END {print "grep -c 15:", s}'
# next against the tip on ui/ (expect no line -- R1 C02; R2 cmd 1)
git diff --stat 8ebaf8daad "$P1" -- "$U" | tail -n 1
# the fork's delta (expect `8 files changed, 463 insertions(+), 13 deletions(-)`; 251; 5; 246 -- R1 C12, C13)
git diff --shortstat "$MB" "$P1" -- "$U"; git log --oneline "$MB..$P1" -- "$U" | wc -l; git log --oneline --merges "$MB..$P1" -- "$U" | wc -l; git rev-list --count --no-merges "$MB..$P1" -- "$U"
# upstream's delta (expect 16; `8 files changed, 72 insertions(+), 75 deletions(-)`; `14 files changed, 83 insertions(+), 536 deletions(-)` -- R1 C14)
git rev-list --count "$MB..$UN" -- "$U"; git diff --shortstat "$MB" "$UN" -- "$U"; git diff --shortstat "$P1" "$UN" -- "$U"; git diff --name-status "$MB" "$UN" -- "$U"
# the 14 files of the tip-to-upstream/next difference by side, checkbox 13's rows (expect `upstream-only 6 fork-only 6 both 2` -- v2 read; LC_ALL=C is set above, so sort and comm agree)
up() { git diff --name-only "$MB" "$UN" -- "$U" | sort; }; fk() { git diff --name-only "$MB" "$P1" -- "$U" | sort; }; echo "upstream-only $(comm -23 <(up) <(fk) | $G -c '') fork-only $(comm -13 <(up) <(fk) | $G -c '') both $(comm -12 <(up) <(fk) | $G -c '')"
# the three recipes' pins at the base, upstream/next and the tip (expect R1 C14's lines: ES cada856d86 / f6c542872e / 16dbac5211 on test/qa-integration with the fork's PKG_SITE; lowerdeck ab735114ab and the theme 9a50ef366e at every hash)
for f in emulationstation lowerdeck themes/es-theme-art-book-next; do for h in "$MB" "$UN" "$P1"; do echo "$f @ $h: $(git show "$h:$U$f/package.mk" | $G -E '^PKG_(VERSION|SITE|GIT_CLONE_BRANCH)=' | tr '\n' ' ')"; done; done
# the ES side, by hash (expect 14; 724; cada856d86; the pin for both refs, read one at a time -- R1 C15; R3 cmd 12's two-ref rev-parse failed)
git -C "$Q" rev-list --count "$PIN..rocknix/master"; git -C "$Q" rev-list --count "rocknix/master..$PIN"; git -C "$Q" merge-base "$PIN" rocknix/master
git -C "$Q" rev-parse --short=10 test/qa-integration; git -C "$Q" rev-parse --short=10 origin/test/qa-integration
# what the define selects, by hash (expect the GLES3 lines at CMakeLists.txt:164-165, :213-214, :362-363 and the renderer lines at es-core/CMakeLists.txt:278-283 -- R2 § 1, cmds 8-9); FRIBIDI at :230-244 (R2 § 1); L-05's names at :303-330 and HFS_DEV_LOGIN's readers in es-app/src (expect HfsDBScraper.cpp:1, :190, HfsDBScraper.h:6, Scraper.cpp:33 -- proof C4), through the mask
git -C "$Q" show "$PIN:CMakeLists.txt" | $G -n -E 'GLES3|OPENGLES_30|GLSystem' ; git -C "$Q" show "$PIN:es-core/CMakeLists.txt" | sed -n '278,283p'
git -C "$Q" show "$PIN:CMakeLists.txt" | sed -n '230,244p'; git -C "$Q" show "$PIN:CMakeLists.txt" | sed -n '303,330p' | sed -E "$M"
git -C "$Q" grep -n -o HFS_DEV_LOGIN "$PIN" -- es-app/src
# syntax (expect rc=0 for each of the seven -- R3 cmd 23); an empty read is a failure, not a pass
for p in emulationstation/package.mk lowerdeck/package.mk themes/es-theme-art-book-next/package.mk emulationstation/sources/es_settings emulationstation/sources/start_es.sh emulationstation/sources/serial_number_check emulationstation/autostart/001-emulationstation; do git show "$P1:$U$p" > "$TMPDIR/one" || echo "SHOW FAILED $p"; [ -s "$TMPDIR/one" ] || echo "EMPTY $p"; bash -n "$TMPDIR/one"; rc=$?
echo "rc=$rc $p"; done
# lint by package name, the positive first, the control last (expect one path and rc=0 for each recipe; for es-theme-no-such-package no path, no line and rc=0 -- the fail-open, L-21 -- R3 § 1.1, cmd 10; stdout carries no line for any name, proof C8, and the path goes to stderr behind a carriage return, `tools/pkgcheck:158`, cleared at `:168`, proof C7 -- so R3's 0 and R5 C11's path read different streams, and `lines=` is recorded as it prints)
for n in emulationstation es-theme-art-book-next lowerdeck es-theme-no-such-package; do echo "find $n: $(find packages projects -type f -path "*/$n/package.mk" | tr '\n' ' ')"; tools/pkgcheck "$n" > "$TMPDIR/pk" 2>&1; rc=$?
echo "pkgcheck $n rc=$rc lines=$(wc -l < "$TMPDIR/pk")"; done
# the scratch export, ruling (k): every sourced-recipe call below runs there, never in the worktree (expect `export rc=0`, the tip's hash, and `worktree build roots: 0`)
X=/workspace/tmp/m6-t37/export; mkdir -p "$X"; git rev-parse HEAD > "$TMPDIR/export-tip"
( set -o pipefail; git -C "$PWD" archive HEAD | tar -x -C "$X" ); rc=$?
echo "export rc=$rc tip=$(cat "$TMPDIR/export-tip") path=$X worktree build roots: $(ls -d build.* 2>/dev/null | wc -l)"
# the effective fields as the build reads them, GENERIC_X64, in the export (expect `source rc=0` for each and R3 § 1.5's table, which the proof's C8 reproduced with this call: the pin; the clone URL and an empty PKG_SHA256; the theme's 7ee1e93f... and lowerdeck's 2677d3ce...; the ES depends ending `zstd mesa`; the ES cmake options ending `-DGLES3=1 -DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1`; `auto` / `manual` / `manual`; `busybox` / `-gold`; the stamps 9e618e4a..., e31c625d..., 7dd9f957...; BASE_ONLY and BATTERYPLUS_SUPPORT empty, VULKAN_SUPPORT=yes, EMULATION_DEVICE=yes -- proof C8); only the named fields are printed, never `set` or `env`
test -e "$X/.rocknix/options" && echo "STOP: a .rocknix/options in the export"
for n in emulationstation es-theme-art-book-next lowerdeck; do env -i HOME="$TMPDIR/home" PATH=/usr/bin:/bin PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 bash -c 'cd "$2" || exit 2; . config/options "$1" >/dev/null 2>&1; rc=$?
echo "source rc=$rc $1"; for v in PKG_VERSION PKG_URL PKG_SHA256 PKG_DEPENDS_TARGET PKG_CMAKE_OPTS_TARGET PKG_TOOLCHAIN PKG_NEED_UNPACK PKG_BUILD_FLAGS PKG_PATCH_DIRS PKG_ARCH TARGET_ARCH BASE_ONLY BATTERYPLUS_SUPPORT VULKAN_SUPPORT EMULATION_DEVICE; do printf "%s=%s\n" "$v" "${!v}"; done' _ "$n" "$X"; done
# the call's writes, named (config/functions:801-802: expect build.pixelelated-GENERIC_X64.x86_64/ in the export holding .cache_package_local and .cache_package_global, their sizes as they print -- proof C8, C10, Correction 1 -- and still `0` build roots in the worktree)
ls -l "$X"/build.*/.cache_package_local "$X"/build.*/.cache_package_global; ls -d build.* 2>/dev/null | wc -l
# the patch reach, computed in the export from the values above (expect `GENERIC_X64/x86_64: ... PATCH_ARCH=x86 PKG_PATCH_DIRS=[] -> patches/x86_64/: NOT REACHED` and the H700/aarch64 line the same -- R3 § 8); PATCH_ARCH by scripts/unpack:127-133's rule, `x86` for an x86_64 target, else TARGET_PATCH_ARCH or the arch (R3 § 2.1 step 2)
# the install text (expect `:101` among the `ln -s ... ${INSTALL}` targets -- L-03; the `rm -f` at `:79` before `:81-82` -- L-04; `|| true` at `:73-75` -- L-07; PKG_NEED_UNPACK at `:14` -- L-19; no PKG_PATCH_DIRS line -- L-02 -- R2 § 1, R3 § 2.2); every other line printed is recorded
git show "$P1:$E" | $G -n -E 'ln -sf? |rm -f|\|\| true|^PKG_NEED_UNPACK=|PKG_PATCH_DIRS' | sed -E "$M"
# the credential names, names and line numbers only (expect `count lines: 5` -- :30, :40, :42, :43, :44 -- R5 C10, proof C6; R1 C19's word-bounded pattern missed :30: `\bSCREENSCRAPER_RUNTIME_DEV_LOGIN` counts 0 against 1 without the `\b`, proof C6)
git show "$P1:$E" | $G -c -E 'SCREENSCRAPER_RUNTIME_DEV_LOGIN|SCREENSCRAPER_DEV_LOGIN|CHEEVOS_DEV_LOGIN|GAMESDB_APIKEY|HFS_DEV_LOGIN'
git show "$P1:$E" | $G -n -o -E 'SCREENSCRAPER_RUNTIME_DEV_LOGIN|SCREENSCRAPER_DEV_LOGIN|CHEEVOS_DEV_LOGIN|GAMESDB_APIKEY|HFS_DEV_LOGIN'
# ARMSX2 and vulkan in the catalog (expect armsx2 at :1331 :1333 :1393; 15 vulkan lines -- R2 cmd 5)
git show "$P1:${U}emulationstation/config/common/es_features.cfg" | $G -n -i armsx2 | cut -d: -f1 | tr '\n' ' '; echo; git show "$P1:${U}emulationstation/config/common/es_features.cfg" | $G -c -i vulkan
# the text checks over the 15 (expect NON-ASCII FILES 0, SECRET-PATTERN FILES 0, forbidden-terms rc=0 -- R3 cmd 23, over the 19; no positive was constructed there, so the lane plants one line and sees each check fire before it trusts its 0; the secret scan sources .githooks/secret-patterns as .githooks/guard-lib does, never `grep -f` on it, § 5 item 3; in that form the proof counted 0 on es_settings.cfg, the four scripts and the ES recipe after its planted positive matched 1, C12, C13, and the other nine are the lane's)
# freshness, information only, both refs given (expect `lines=48 ui=0` -- R3 cmd 12, proof C14 with these two refs; pure git; the check is the two counts, never rc=0: without its refs it prints `fatal: bad revision 'upstream/next'` and exits 0, proof C8, Correction 16, L-21; its rc 0 proves nothing for these three, L-10)
FRESHNESS_BASE="$UN" FRESHNESS_HEAD="$P1" tools/fork-package-freshness --list > "$TMPDIR/fr" 2>&1; rc=$?
echo "freshness --list rc=$rc lines=$(wc -l < "$TMPDIR/fr") ui=$($G -c 'packages/ui/' "$TMPDIR/fr")"
# the candidate's provenance, ruling (h) (expect the nine ES patches and a ui/ tree hash 9144dbe9a4d8 against the tip's 8f83424780, the theme, lowerdeck, cfgs, sources, units and autostart byte-identical -- R3 § 2.3, cmd 21)
git -C /workspace/repos/rocknix ls-tree --name-only 069fc2704421 -- "${U}emulationstation/patches/"; git -C /workspace/repos/rocknix rev-parse 069fc2704421:projects/ROCKNIX/packages/ui; git rev-parse "$P1":projects/ROCKNIX/packages/ui
# STAGE C -- the lane's checker, which does not exist at stage A; --tree is the scratch export (ruling (k)) and --repo the worktree, for its git reads (expect its FAIL-first run's `exit 1` naming each mutation, `exit 0` on the unmutated export, then at the tip FAIL naming L-03 and any of L-02, L-19, L-04 the tracing confirmed, with its own `TOTAL:` line)
bash docs/audits/*-epic-m6-es-recipe/tools/t37-checks.sh --tree "$X" --repo "$PWD" --commit "$P1" --expect-es-pin "$PIN" --devices "GENERIC_X64:x86_64 H700:aarch64" --out "$TMPDIR/checks" 2>&1 | tail -n 20
# STAGE A, after the pointer is read -- the removal check: TIPHASH is the lane's own tip the pointer and the dispatch comment name (MERGE_HASH at stage A); the literal word fails with `fatal: bad revision 'TIPHASH'` (expect no line before stage E; from stage E only paths under projects/ROCKNIX/packages/ui/)
git diff --stat TIPHASH HEAD -- packages projects tools | tail -n 1
```

Every expectation above is a research file's printed line, cited in its
comment, or marked by stage. **The lane re-runs every one as its own line; a
line that differs is recorded beside the expectation, not argued with.**
Three of the lines are the lane's own to write, because the research
printed their figures without the command that made them: the patch-reach
computation (R3 § 8 printed the verdicts), the text checks over the 15 (R3
cmd 23 ran them over the 19) and `calculate_stamp`'s invocation (R3 cmd 16
printed the stamps). The effective-values call's form is no longer open: the
proof's C8 ran `. config/options "$1"` under `env -i`, reproduced R3 § 1.5's
values and the three stamps, and wrote the two cache files, so the call runs
in the export (ruling (k)). `/workspace/repos/rocknix` is read by hash only, as R3 cmd 21 did;
whether it is one of the M7 roots the never-run list forbids is the
dispatch comment's to say (`[unverified]`), and if it is, the lane cites R3 §
2.3 and runs nothing there.

## 6. Outputs

As T26's to T36's briefs § 6, scaled down: no `stage-a/fakes/`, no stand-in
compile and no unit build (R5 § A); § 7 is this section as checkboxes. The
folder `docs/audits/<yyyy_mm_dd>-epic-m6-es-recipe/` (#684 body `:22`, R5 §
F): `00-running-log.md` to `05-punch-list.md`; `second-opinions/`
(`review-plan.json`, the probe's and the refutation's `.provenance.json`,
`packet-manifest.json`); `stage-a/` to `stage-e/` (the first commands and
§ 5's runs under `stage-a/`; the window plan under `stage-b/`; the checker's
FAIL-first run and its run at the tip under `stage-c/`; the streams' runs
under `stage-e/`); `tools/` (`t37-checks.sh` and any table generator, each
asserting its counts and each seen to exit 1 on a constructed drift before it
is trusted); `guest-cycle/`; the lint before D; the audit issue (`Audit: M6
T37 the EmulationStation recipe and themes in the distribution -- N findings
(...)`, a sub-issue of #684; the audit issue and the bugs are the lane's,
D-WORKFLOW-189; a Backlog for a lead outside the 15 is the coordinator's,
named in the hand-back); and the retro at `docs/retros/<date>-m6-es-recipe.md`
(**what the slice did to the two time-to-play numbers** -- boot to interface
from G-04, § 3 item 10, never "nothing" by default -- and **what the
integration inherits**, § 8).

**`02-forward-audit.md` carries these sections, in this order, each
generated section's row count stated as "generated, asserted" by the script
that made it:**

1. **§ Coverage** -- 15 rows, the path in backticks as the first cell, both
   tier forms: the inventory's fork-own 6 / upstream-carried 9, and git's
   classes; **the four patches are named after the table, in prose with
   their owners, never as rows**, so the row count stays the slice's.
2. **§ The leads** -- L-01 to L-21 (L-14, L-15 folded, § 3), each with its
   lines, its family, who owns it and its disposition.
3. **§ The recipe** -- Q1, Q2 and Q4: the pin table (the pin, its branch, its
   site, the three upstream pins, the kept images' pins read from their
   `os-release`); one row per `-D` with its CMake test and branch at the pin,
   and the define's chain to `Renderer_GLES30` with the three empty pairs
   named for T35 and T36; one row per install step with its line, what it
   installs and how it fails; the credentials by name and line, never a
   value; PL-029, #613 and #1193 at their lines.
4. **§ The dependencies** -- Q3: the effective `PKG_DEPENDS_TARGET` per device
   read; L-09's chain with each link's effective value; udev and pugixml;
   L-19.
5. **§ The themes and `lowerdeck`** -- Q5: the pins with their `PKG_SHA256`,
   licences and install steps; the three patches' apply order (their text
   T42's); #69's offer; the wordmark rows; the default theme; `lowerdeck`'s
   distance from its author's `HEAD` as R1 C20's dated read.
6. **§ The patches and their directories** -- Q6: one row per `patches/`
   subdirectory per device in the plan, reached or not by
   `scripts/unpack:150-160`'s globs (generated, asserted); L-02 and L-18.
7. **§ The currency** -- Q7: one row per file of the tip-to-`upstream/next`
   difference, 14 (generated, asserted), each upstream moved, the fork moved
   or both, with the 16 commits; the ES 14
   as #791's input; L-10, L-16, L-21.
8. **§ The structure** -- the 15 against the 19; the doc drifts L-17 and L-18
   for the coordinator's sweep; the candidate's provenance (ruling (h)).
9. **§ The runs** -- every § 5 command with exit, wall time, the figure and
   *a FAIL would mean ...*.
10. **§ The guest cycle** -- G-01 to G-07.
11. **§ The streams** -- stage E: **written by the coordinator after stage D,
    as for T21 to T36**; the lane leaves the heading and the pause's
    dispositions.
12. **§ Positives** -- what the read found sound, with its lines.
13. **§ The #585 lines owed** -- one per upstream-carried defect the lane
    proves, in the shape the lane writes, never sent.
14. **§ What the integration inherits** -- § 8's items with their lines.

Every proof carries `proved:`. The stage-D pause as T21's: the punch list
posted on #684, the lane waits for the coordinator's dispositions and any
stream brief.

## 7. Acceptance

The checklist on #684 becomes this section at dispatch, written there by the
coordinator in place of P1's generated ones (the fifth, naming
`tools/renovation-status`, is replaced by checkbox 5 below, as T33's to T36's
were). Every checkbox names the artifact that ticks it (D-QA-044); the
coordinator ticks at acceptance, from the artifacts, never from the
hand-back's words. **The five contract criteria come first, adapted for a
slice that changes no ES file (ruling (c)).**

- [ ] `docs/audits/<date>-epic-m6-es-recipe/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `second-opinions/`, `stage-a/` to `stage-e/`, `tools/` and `guest-cycle/` (`ls` of the folder in the hand-back).
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-es-recipe/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`), and the same with `--issue <audit issue>` prints `PASS`; Q1 to Q7 are answered in `04-analysis.md` and every punch item carries `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: independent` and one reviewer (`gpt`, `openai/gpt-6-astra`, `max`); its probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named (read directly); `packet-manifest.json` carries the scan block with every hit dispositioned by file:line (the five credential-name lines of `emulationstation/package.mk` as *build-variable name*) and no value, `:39`'s value masked, the 9 code files whole, the cited ranges of `es_features.cfg` and `es_input.cfg` named, and the OFL and the SVG named and not sent; `00` shows exactly two keyed invokes.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #585, #613, #1072, #1193, #990, #69, #64, #791, #1013, #1137, #682, #683, an M7 issue by number), withdrawn or recorded as written with its reason; `tools/box-check --issue <audit issue>` prints 0 fail; the issue is closed by the coordinator at acceptance.
- [ ] `reviewed-at:` and `fixed-at:` in #684's header carry the lane's commits and **`reviewed-at-es:` and `fixed-at-es:` read `none -- no ES change`**; nothing outside the 15 changed at any stage against the lane's own dispatch tip (the pointer's merge hash, never `2174265e9c`), and from stage E only paths under `projects/ROCKNIX/packages/ui/` (`git diff --stat <merge hash> <fixed-at> -- packages projects tools`); **no lane commit changes the ES recipe's `PKG_VERSION=` or `PKG_GIT_CLONE_BRANCH=` line** (`git log -p` over the lane's commits, `/usr/bin/grep -c -E '^[-+]PKG_(VERSION|GIT_CLONE_BRANCH)='` prints `0`, R5 § E).
- [ ] `01-research-notes.md` § Scope records § 2's block, its sha256 prefix `f3ef373be6535467` checked, with its exact output lines (`mine: 15 paths.txt: 15 equal: True`; `lines: 4561 reach: {'shipped': 15} tier: {'upstream-carried': 9, 'fork-own': 6} lang: {'shell': 4, 'config': 4, 'recipe': 3, 'systemd': 2, 'text': 1, 'image': 1}`; `fork-own lines: 572`; `read lines: 327 of which fork-own: 190 vendor-carried lines: 0`; the two `diff`s naming the four patches; `wc -l, every path at the P1 hash: 4649`, `grep -c, every path at the P1 hash: 4650`, `grep -c, the inventory paths at its head: 4561`; `14`; ` 8 files changed, 463 insertions(+), 13 deletions(-)` -- or the deltas beside them) and names `c445081a59` as the merge base with `upstream/next` `651150fc88` and `cada856d86` as the pin's with `rocknix/master` `f6c542872e`.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `15`; its tier columns read fork-own 6 / upstream-carried 9, with git's classes beside them; the four patches named after the table with T40 and T42.
- [ ] `02` § The runs records, each as a command's own output line: `tools/pkgcheck <name>` for `emulationstation`, `es-theme-art-book-next` and `lowerdeck`, each after its `find` positive with rc 0, and the control `es-theme-no-such-package` beside them; `bash -n` rc for the seven; the scratch export's path and tip, the effective fields and the stamps for GENERIC_X64 (and any other device run) from it, the two cache files the calls wrote there named, and `0` `build.*` roots in the worktree (ruling (k)); the patch reach per device; the credential-name count (`5`) with names and line numbers only; the text checks over the 15 after a planted positive; `tools/fork-package-freshness --list`'s line with both refs given, judged by `lines=48` and `ui=0` from its output and never by its rc (L-10, L-21); every run with exit, wall time, the figure and *a FAIL would mean ...*, a run that could not be made `CANNOT` with its reason.
- [ ] `tools/t37-checks.sh` exists under the audit folder's `tools/`; `02` § The runs records its FAIL-first run (exit 1 naming each mutation's assertion, exit 0 on the unmutated export, the stub checked against the unfixed text first), its run at the tip (FAIL naming L-03, and each of L-02, L-19 and L-04 the tracing confirmed) and its `TOTAL:` line quoted from its own output; every generator seen to exit 1 on a constructed drift before its table was trusted.
- [ ] `02` § The recipe has one row per `-D` the recipe passes (`:19-25`, `:30`, `:33`) with its CMake test and branch at the pin; `:25`'s chain through `GLSystem` to both `-DUSE_OPENGLES_30` and the `Renderer_GLES30` listing, with `Renderer_GL21`, `Renderer_GLES10` and `Renderer_GLES20` named for T35 (the list) and T36 (the bodies); one row per install step of `makeinstall_target` and `post_install` with its line, what it installs and how it fails; L-01, L-03, L-04, L-06, L-07 and L-08 dispositioned; PL-029 dispositioned with G-04's line; #613's and #1193's rows; the credentials by name and line (L-05 as § 3 states it, re-read at the pin's `CMakeLists.txt:303-330` through the mask with `HFS_DEV_LOGIN`'s readers; L-11 recorded as design; #64's open checkbox answered or recorded), and no value in any artifact (the hooks' `SECRET_PATTERNS`, sourced from `.githooks/secret-patterns` and compile-checked as `.githooks/guard-lib` does, counts `0` over the folder after a planted positive matched; never `grep -f` on that file, § 5 item 3).
- [ ] `02` § The dependencies records the effective `PKG_DEPENDS_TARGET` per device read, L-09's chain with each link's effective value and fribidi's question put to the pause with G-01's `ldd` line beside it, udev and pugixml as build facts, and L-19.
- [ ] `02` § The themes and `lowerdeck` records both pins with their `PKG_SHA256` and licences, the theme's install steps (`:14-28`), the three patches' apply order, #69's offer state under D-UI-090 (nothing sent), the wordmark against D-WORKFLOW-144 to -146, the default theme (L-20) and `lowerdeck`'s `HEAD` as R1 C20's dated read, with a bump of either recorded as a finding, never made.
- [ ] `02` § The patches and their directories has one row per `patches/` subdirectory of the three packages per device in the plan, with `patches/x86_64/` NOT REACHED on GENERIC_X64 and H700 as R3 § 8 printed (or the line that differs), L-02's `PKG_PATCH_DIRS` named T37's line and the patch's content and #1072's shape T40's, and L-18.
- [ ] `02` § The currency has one row per file of the tip-to-`upstream/next` difference over `ui/` -- `git diff --shortstat 2174265e9c 651150fc88 -- projects/ROCKNIX/packages/ui/` prints ` 14 files changed, 83 insertions(+), 536 deletions(-)` -- each row saying which of the three it is: upstream moved (one of the 8 of ` 8 files changed, 72 insertions(+), 75 deletions(-)` over the 16 commits `c445081a59..651150fc88`), the fork moved (one of the fork's ` 8 files changed, 463 insertions(+), 13 deletions(-)` against the base), or both (§ 5's `comm` line, `upstream-only 6 fork-only 6 both 2`), with these tool lines quoted in `02`; each row named upstream's change the fork lacks, the fork's own, or a merge pending; the ES pin's 14 named as #791's input; L-10, L-16 (#990) and L-21 dispositioned.
- [ ] `02` § The guest cycle records the window the coordinator granted on #684 (the comment's time; the START and RETURN posts with their first-line contract, the timer that stops the guest or the sentence that nothing does, and the censuses, with the host file's lines beside them), the fresh disk's path and the image by file name and `BUILD_ID` read from the guest at 640x480, G-01 to G-07 each labelled by side (`ui-equal` or `candidate`), G-05's string counts as counts only, the disk retired with path, size and sha, the leftover check (`qemu 0, compilers 0`), and the window closed inside its bound plus grace.
- [ ] `00-running-log.md` shows no image build, no compiler, no fetch (no `git fetch`, `git ls-remote` or `gh api` of the authors' repositories, no `rc-preflight`, no real `fork-package-freshness` run; the council runtime from `npm install --offline`), no handheld, the owner's accounts never named or used, no hosted account, no M7 root, worktree or prep directory, no held directory opened, no ES worktree and no write in any ES checkout, the guest only inside the granted window and writing nothing, two keyed invokes and every other council call keyless, nothing written outside the 15 at any stage, no `build.*` root in the worktree at any stage, and the scratch export's path with its retirement at stage H (`00`'s own closing census; ruling (k)).
- [ ] `04-analysis.md` § Q1 to Q7 are answered at their lines; every `bug` states its trace, its `Already written:` line (what an image built from the old recipe left on the read-only image and in `/storage`, argued) and its VM line in one of the named families and passes `tools/box-check --issue N`; every #585 line owed is written in `02` in the shape the lane writes; every row of § 2's take-up table has a disposition at its lines; the § 1 rulings (a) to (k) each have their `02` row.
- [ ] Every proof in `02` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-fixture`, `fix-image-pending` or `design`; every punch item carries `question:`; `02` § What the integration inherits lists § 8's items with their lines.
- [ ] The retro exists at `docs/retros/<date>-m6-es-recipe.md`, is posted on #684 with its heading's time from `date -u` in the posting command, says what the slice did to the two time-to-play numbers (boot to interface priced from G-04, or `CANNOT` with the harness's reason) and what the integration inherits.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the distribution branch before the hand-back merge, and again on the coordinator's simulated merge; every fix has, recorded beside its commit, its `fix-fixture` FAIL line on the tip's text and PASS line on the fix's, `tools/pkgcheck <name>` by name, `bash -n` where a script changed, and the stamps compared, each fix moving only its own package's stamp.
- [ ] The hand-back names every collision with its owner: the integration's pin-bump commit on `emulationstation/package.mk`; T35's `es-core/CMakeLists.txt` renderer list and T36's bodies beside `:25`; fribidi's decision; the candidate's nine ES patches and its link (ruling (h)); T40's `cpugov.patch` and T42's theme patches; T8's `virtual/image/package.mk`; and the Backlog leads L-10 and L-21 (its three fail-opens) for the coordinator to file.

## 8. What the integration inherits

Written, not done here; `02` § What the integration inherits carries each
item with its lines, and the hand-back names them. **T37 integrates after T35
and T36** (R4 item 4): *"... T35, T36 (with the pin moved to the ES branches'
tip), **then this branch**, its `emulationstation/package.mk` hunks merged
over that pin-bump commit, then T4's last"* (R5 § D's pointer sentence; the
lanes' pointers, R4 item 4).

1. **The pin bump, with the ES branches' merged tip.** No merged tip exists
   yet: `test/qa-integration` is the pin, local and `origin` (R1 C15; R4 item
   6). At R4 cmd 21 the branches ahead of the pin were T2 `55158d2a6` (35),
   T21 `3ae9610b0` (17), T26 `757f5370e` (14), T31 `95852f873` (13), T20
   `5c0ddaaee` (11), T33 `f802c55c6` (8), T34 `52f0ff512` (8), T32
   `b52245036` (6), T18 `d55235d4b` (6), with T36's at the pin (0); T35's was
   `d0e5b3432`, 8 ahead, at R4 item 41 (replacing item 6's T35 row), and
   `b7fdb3a24c`, 9 ahead and containing `d0e5b3432`, at the proof (C4, C15)
   -- each read at the integration's turn, never copied from here. **The steps**
   (`device-builds.md` § Iterating on EmulationStation, R4 item 33): the
   branches merged into the branch `:6` names, `:5` moved to that tip in the
   same integration commit, the stamp cleared; **before the pin lands on
   `next`**, the compiler sees every touched `.cpp` and the ES package is
   built (`es-native-ui.md:405-415`; `tools/es-syntax-check` exits 2 on this
   host, #1137, R4 item 9), the ASCII-comment grep runs over the added lines
   (only an image build runs xgettext, R2 § 5), and `tools/pkgcheck
   emulationstation` runs by name (R4 item 8). T2's `05c8e4b5e` and
   `dce0b9b6b` are on the merged tip (R4 item 11, § 5). **Until
   D-WORKFLOW-191 is decided** the rule stands as written: accepted at
   hand-back, the ES branch merged into `test/qa-integration` and the pin
   bumped, each slice's issues open as `remediating` until the first image
   carrying the pin proves each fix (R4 item 5, § 5).
2. **The French catalog merges.** At R4 cmd 21, 9 of the 10 branches ahead
   of the pin changed `locale/lang/fr`, T35's then at 0 (R4 item 7), each of
   the nine changing `fr=1` file (proof C4); T35's `d0e5b3432` changes it
   (`French-catalog files changed 1`, R4 item 41) and so does `b7fdb3a24c`
   (`1` French file, proof C15), so the count is read at the integration's
   turn. The merged catalog's
   msgids are checked against the sources (`tools/es-untranslated`) after the
   merges and before the pin moves (R4 item 7; `es-player-text.md` § Every
   fork string ships in English and French). No ruling on the merge order was
   found (R4 § 7).
3. **The three held patches and T34's commits.** T34's eight ES commits
   (`52f0ff512`, `ahead=8`) and its three patches in its own folder,
   `stage-e/s2-holders.patch`, `stage-e/s2-window.patch` and
   `stage-e/s3-msgbox.patch` (R4 item 3); `t35-streams.md:592`, *"T34's
   `s2-window.patch` is the integration's, not adopted here"* (R4 item 3);
   T35's retro, *"For T37 (the recipe that moves the pin): the eight ES
   commits, the French catalog's `GAMEPAD` entry, and the hand-back's
   dry-runs of T34's `s2-window.patch` and `s3-msgbox.patch` over T35's
   tip"* (R4 item 39). **T37 names them by hash and path in its pin table, and
   which ES file each patch touches, and applies none.** (These are T34's
   audit-folder files, not a held directory; no held directory is opened.)
4. **The define's three owners** (D-WORKFLOW-216; T36's errata `:2146`; R4
   item 2): the renderer source list (`es-core/CMakeLists.txt`) T35's, the
   define (`package.mk:25`) T37's, the bodies T36's; a change to the list or
   the define is reconciled with the other two at the integration.
5. **Fribidi.** The decision -- declared at `:13`, or the transitive chain
   recorded as the recipe's -- is the pause's; its proof is an image build's
   CMake cache or the image's `ldd` (L-09; D-WORKFLOW-216).
6. **The candidate's provenance** (ruling (h)): the M7 candidate
   `069fc2704421` built the pin plus nine ES patches the tip's recipe does
   not carry -- `001-log-entry-lifetime` to `009-recovery-observation-timeout`
   -- and a corrected `es_systems.cfg` link (R3 § 2.2 C1, C2, cmd 21); by a
   one-line heuristic 7 of 9 have no trace in the pin (R3 cmd 22). So the
   futro's *"the image's binary is the slice's bytes"* row
   (`2026-10-23-m6-interface.md:51`, by `PKG_VERSION` equality) does not
   establish it (R3 § 2.2 C2). Whether the renovation dropped them on
   purpose is a register read (`tools/archaeology <patch names>`, R3 § 2.2
   C2).
7. **The identity sidecar** does not carry the ES pin (#1013, Backlog; R4
   item 10).
8. **The distribution merge on `ui/`** -- § 2's merge debt, upstream's 16
   commits on 8 files -- is `release-candidates.md` step 0's work, not a
   slice fix (R3 § 1.8); **the ES 14** are #791's (R1 C15; R4 item 30).
9. **The fixes this slice proves**, each `fix-image-pending` until the first
   image built from the fixed recipe shows it (§ 5 item 4).

## 9. The register and the ceremonies

**The register** (`docs/decision-register.md` at `de935d6ec6`, holding at
`7d43f340c5`; the line is the table's; R5 § G, C9, C15; R4 § 3):

| Row | Line | What it binds here |
| --- | ---: | --- |
| **D-WORKFLOW-012** | `:240` | upstream PRs to `ROCKNIX/distribution:next`, `es`-prefixed for EmulationStation: an ES change reaches upstream as *"the package bump plus patches in the distribution repo"* |
| **D-WORKFLOW-024** | `:335` | a fork-introduced package at its latest upstream release, or a `# freshness: pinned --` line; its tool does not reach these three (L-10) |
| **D-WORKFLOW-162** | `:690` | upstream checked early; with **D-WORKFLOW-164** (`:698`) and **-165** (`:700`): contributions considered and queued, not sent before the initial build |
| **D-WORKFLOW-166** | `:702` | the shared ScreenScraper developer identity, interim; #586 for replacement |
| **D-INFRA-006**, **D-INFRA-007** | `:75`, `:76` | build credentials only in the options file; the line is who can download it |
| **D-WORKFLOW-213**, **-214** | `:759`, `:768` | the es-core owners; neither names T37 |
| **D-WORKFLOW-216** | `:776` | the `package.mk:25` define T37's; `HAVE_FRIBIDI`'s undeclared build-order dependency T37's recipe |
| **D-WORKFLOW-215** | `:771` | the hold test: a finding the lane thinks it may meet is raised before its mechanism is posted |
| **D-UI-090** | `:391` | the Tools-icon patch offered to art-book-next's author by pull request, words approved first -- the one decided row naming the theme |
| D-WORKFLOW-191 | `:783` (open table) | which build carries the renovation's pin bumps; the rule until decided (§ 8 item 1) |
| D-WORKFLOW-187, -189, -195, -212 | `:722`, `:723`, `:728`, `:753` | the renovation's rows every brief cites; D-WORKFLOW-188 is on the P1 branch only |
| D-WORKFLOW-047, -050; D-UI-079 | `:394`, `:408`; `:345` | a bump is never a fast follow; every bug's `Already written:` line; the lanes |
| D-WORKFLOW-144, -145, -146 | `:604`, `:608`, `:610` | the lowercase name; Tiny5 Duo LCD; the wordmark system |

**The highest decided IDs per area**, read from the table above `## Open
decisions` only (the register is 795 lines, `## Open decisions` at `:778`; the
`awk` over the decided table, R5 § G, C9, and the same nine at `7d43f340c5`,
R5 C15): **D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063,
D-RA-052, D-SYS-013, D-UI-137, D-WORKFLOW-216**; `tools/register-check`
printed *"711 IDs, each once; every citation in the live documents names a
row"* and, with `rc=$?` on its own line, `register-check rc=0` (R5 C9, C10);
the proof's `awk` over the register printed `ids decided 698 open 13` and did
not run `tools/register-check` (C10).
**This slice's ownership row is D-WORKFLOW-217**, written by the coordinator
at dispatch after `:776` and before `## Open decisions`, its `<date>` checked
on the appended line alone (R5 § D); if the table moves first it is the next
free WORKFLOW ID, and the row, the dispatch and the pointer follow it. **The
row, per ruling (a):** T37 (#684) owns the 15 paths of
`projects/ROCKNIX/packages/ui/**` the inventory assigns it -- the four
`.patch` files are T40's and T42's -- and nothing else; the ES sources are
read-only context (every `es-*` slice's; `es-core/CMakeLists.txt` T35's; ES's
top-level `CMakeLists.txt` the integration's); `PKG_VERSION` and
`PKG_GIT_CLONE_BRANCH` of `emulationstation/package.mk` are the
coordinator's, moved at the integration; `-DGLES3=1` at `:25` and the
`HAVE_FRIBIDI` declaration are T37's by D-WORKFLOW-216;
`virtual/image/package.mk` is T8's; the theme patches' upstream offer is
under D-UI-090 (R5 § D's `t37-ownrow.md`, with ruling (a)'s 15 in place of
its 19). The pointer's `Register:` line is filled from the same `awk` at
`COHASH`, never from here (§ 10).

**Rows the pause may need, all put to the coordinator as questions, never
decided by the lane:** **fribidi** -- declared at `:13`, or the transitive
chain kept as the recipe's decision (L-09); **the link** -- whether #613's
fix lands in this slice's stream (L-03); **the patch directory** -- the
recipe's `PKG_PATCH_DIRS` against #1072's relocation of the patch (L-02,
ruling (a)); **the freshness tool's reach** -- whether the three recipes join
`EXTRA_PACKAGES` (L-10); **a loud catalog** -- whether a missing French `.mo`
stops the install (L-08); **the ARMSX2 block** -- restored or recorded (L-01).
A row this slice forces takes an ID the coordinator assigns on #684.

**The ceremonies** every lane owes are the rules that load every session --
`learning-capture.md` (the work-log entry per session headed `#684`, its time
from `date -u` in the same command, `tools/work-log-index --write` after it),
`ceremonies.md` (a friction line the moment something slows, `issue: #684` or
the guard; `tools/ceremony-check --gate` before every push, never
`--no-verify`), `decision-register.md` (a row the same session for any
decision), `vm-first.md` (the VM question before any proof: § 5 answers it),
the mini-retro at stage G posted on #684 in Instruction-Recommendations mode
with its *adjustments* as proposals for the coordinator -- and are not
restated here. What is this slice's:

- **What a hold is**: a finding is held off the public tracker only under
  D-WORKFLOW-215's test; holding is the coordinator's, and the lane never
  opens a held directory (`/workspace/tmp/m6-t34/held/` and
  `/workspace/tmp/m6-t36/held/` included). None is expected in a recipe read;
  a finding the lane thinks that row's test may cover is raised with the
  coordinator on #684 before anything about its mechanism is posted.
- **The same-commit rules, stated once:** this slice's files hold no menu and
  no player string, so a stream that would change a row or a sentence is a
  stream outside the 15; a `package.mk` edit's commit records its
  `tools/pkgcheck <name>` line and its stamp comparison; a script edit's,
  its `bash -n` line.
- **Every count is a tool's line** (`engineering-practices.md` § A name is
  not a behaviour): a figure in `02`, a post or the hand-back is the
  command's own output, quoted; a sum, a difference or a rate is computed by
  the command that prints it; **`rc=$?` on its own line after the command,
  never after a `$(...)` in the same word or a pipeline's last stage**; **no
  `cut` on an expected error line**; **a heading's time from `date -u`,
  never typed**.
- **The recipe is read through the mask** (§ 5's `M`, or
  `engineering-practices.md`'s), **`:39`'s value is never printed**, and after
  sourcing a recipe only the named fields are printed, never `set` or `env`;
  nothing under `~/.ROCKNIX/` or `~/.rocknix/` is read (`config/options`
  under `env -i` with `HOME` in scratch, R3 § 1.5, and only in the scratch
  export, ruling (k)).
- A merge with conflicts is checked for markers; the ledgers united by whole
  entries; **a commit names its paths**; anything temporary under
  `/workspace/tmp/m6-t37/` after `df -i`, never `/tmp`; the scratch export
  `/workspace/tmp/m6-t37/export/` retired at stage H, its path and
  retirement in `00`'s census (ruling (k)); the window's record
  kept on the branch, the guest disk retired after it with the retirement
  recorded in `00` (D-INFRA-022); **`rm -rf` only as `"${VAR:?}"/...` or a
  literal path, in its own short command, never inside a `bash -c` script**.
- A fixture that rewrites no path outside scratch, in a bubblewrap sandbox
  started with `--clearenv` (`device-builds.md` § Temporary directories: the
  sandbox otherwise inherits the host's `TMPDIR`); **a credential-shaped
  value (L-05's placeholders) assembled at run time, never a literal** --
  `.githooks/pre-commit` refuses the literal; a generator seen to exit 1 on a
  constructed drift before its table is trusted.
- **Every edited file checked for an unfilled placeholder before its
  commit**: `/usr/bin/grep -c -E '__[A-Z]+__|\b(CO|MERGE_|TIP|V2)HASH\b'`
  is 0 on the pointer, the running log and every artifact (the pattern is
  written in pieces here so that this line does not count itself, and the
  four names it matches are § 1's; on the filled dispatch comment only the
  `__[A-Z]+__` half must print 0, R5 § B item 2). This brief carries the four
  names as its own words, so it is never copied into an artifact unfilled.
- Commit messages `docs: ...` on the distribution branch for the audit folder,
  with `Refs #684`; a recipe fix in the package's convention
  (`emulationstation: ...`, `es-theme-art-book-next: ...`), `Refs #684,
  #<bug>`; no closing keyword before an issue number while a criterion is
  open (`issue-tracking.md`).

## 10. Hand-back, the pointer, the host, the stops and what never runs

**The hand-back.** The coordinator accepts by reading, in this order, without
re-reviewing: #684's checkboxes against their artifacts; the lint's `PASS`
line on the default phase and with `--issue`; `review-plan.json` and the two
provenance files (read directly) and the manifest's scan block; the audit
issue's checkboxes all at an outcome; the coverage table's row count (15) and
the generated sections' asserted counts; every Q bug with its three lines;
**re-running on a clone of the distribution branch at its tip under
`/workspace/tmp/m6-coordinator/`: the membership block, every § 5 run in
full, `tools/t37-checks.sh` with its FAIL-first run** (no guest: the window's
record is read, not repeated; every sourced-recipe run in a scratch export
of that clone, never the clone itself, ruling (k)), through the
coordinator's acceptance script
`t37-accept.sh`, derived from `t36-accept.sh` with T16's product-path
sections ported (R5 § E: `product-paths` inverted, `pkgcheck` per package by
name, `bash-n`, `freshness` for information with both refs given,
`effective-values` in a scratch export, the no-pin-change check and the
no-`build.*`-root check; the ES, unit-build, stand-in and renderer sections
dropped); `register-check` on a simulated merge with the coordinator's tip;
the retro's answers; the five checkers' exit codes; the collisions named in §
7's last checkbox; **the § 1 rulings' rows in `02`**. The lane posts one
hand-back comment naming **its one tip** and each artifact by path, writes
`reviewed-at:` and `fixed-at:` into #684's body with `reviewed-at-es:` and
`fixed-at-es:` reading `none -- no ES change`, then says it is idle. After
acceptance the coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the lint against **the audit issue**, merges the
distribution branch in its turn after T35 and T36, its
`emulationstation/package.mk` hunks over the pin-bump commit (§ 8),
regenerates the ledgers, posts any #585 lines in the shape the lane wrote,
files any Backlog the hand-back names (L-10, L-21), sweeps the rule and doc
drifts (L-17, L-18), and closes #684 when every row is proven; the interface
epic #700 closes when its slices have.

**The pointer the lane checks at stage A, line by line.** The seeded pointer
`.github/sessions/saved-session-state-feature-m6-es-recipe-684.md` is written
by the coordinator from T36's. So before the first command after `cat` the
lane reads these eleven keys, each against the one value that would be the
seeding error -- **T36's** (R5 § A, § D) -- and reports any that name the
predecessor on #684 before going on. Every figure in the *Must read* column is
§ 1's, § 5's or § 9's, copied from that one place (R5 § B item 6):

| Key | Must read | The seeding error reads |
| --- | --- | --- |
| `Branch (distribution):` | `feature/m6-es-recipe-684` stacked on `feature/m6-p1-survey-641` at the P1 tip the dispatch comment names (`2174265e9c` today) | `...-es-core-utils-resources-683` |
| `Worktree (distribution):` | `/workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684` | `m6-es-core-utils-resources-683` |
| `Worktree (EmulationStation):` | **none**: the pin is read by `git -C /home/max/Development/emulationstation-next.worktrees/qa-integration show 16dbac5211:<path>` only (ruling (c)) | T36's `m6-es-core-utils-resources-683` checkout, or any ES branch named for #684 |
| `Executor:` | Opus 5.5 at high effort, the T3 session (`m6-t3-emulators`), free since T34's close-out, as the dispatch comment on #684 names it | T36's session (the T1 session, `m6-t1-os-launch`) |
| `Epic:` | #700; T2, T18, T20, T21, T26, T31, T32, T33 accepted and open until the integration merge; T34 complete; T35 handed back; T36 at the state the dispatch comment names; T44 after | "T36 accepted" before it is, or "T35 in flight" |
| `Depth:` | one seat, GPT-6 Astra at `max`; the 9 code files whole with `:39`'s value masked, `es_savestates.cfg` and `es_settings.cfg` whole, `es_features.cfg` and `es_input.cfg` by cited ranges, the OFL and the SVG named and not sent | the 15 fork-added and fork-modified files whole, the 43 upstream-carried by cited ranges |
| `The lens:` | package currency over the 15 of `projects/ROCKNIX/packages/ui/**` -- the ES recipe, its sources, units and seeds, the theme and `lowerdeck`; the four patches T40's and T42's | cost against value over 58 paths, `es-core/src/{utils,resources,renderers}/**` |
| `The rule:` | the lane changes only `projects/ROCKNIX/packages/ui/**` -- the 15 -- and only at stage E under a stream brief; never `config/options` sourced in the worktree, and no `build.*` root there (ruling (k)); never `PKG_VERSION` or `PKG_GIT_CLONE_BRANCH` of `emulationstation/package.mk`; nothing under `packages/` or `tools/`, nothing else under `projects/` (`virtual/image/package.mk` included); nothing in any ES checkout; `tools/pkgcheck <name>` by name after every `package.mk` edit | "nothing under the distribution's `packages/`, `projects/` or `tools/`; nothing in the ES worktree at stages A to D; nothing outside the 58 at stage E" |
| `The host:` | the shared log and one guest window of 15 + 5 minutes, one boot at 640x480, on a fresh disk from the M6 copy of the candidate; the START post naming the timer that stops the guest at bound plus grace or saying nothing does; no START while an M7 standing or compile START is open (#1293) | a 25 + 5 window with two boots (640x480, then 1280x800) |
| `Register:` | the highest decided row per area read from the table at `COHASH` (at `7d43f340c5`: D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-137, D-WORKFLOW-216), plus **this slice's ownership row, D-WORKFLOW-217, which the coordinator writes at dispatch** | T36's nine at `acc4674006` (`... D-UI-133, D-WORKFLOW-215`), or D-WORKFLOW-216 named as this slice's own row |
| `The brief:` | `docs/reviews/briefs/es-recipe.md` at `V2HASH` (§ 1: filled by the dispatch comment; version 1 has no dispatch hash) | `es-core-utils-resources.md`, or the literal word `V2HASH` |

**The host.** One file, `/workspace/tmp/m7-m6-host-coordination.txt`, read
whole before any guest starts and with the time of the read; one guest window,
asked for on #684 with its plan and bound and granted there and in the file's
queue (§ 5 item 2); the START contract -- `START HH:MM:SS UTC` as the first
line of the post on #684 and a line in the file, with the census, naming the
detached timer that stops the guest at bound plus grace or saying that nothing
does -- and the RETURN the same; **the standing-slot rule: no START while an
M7 standing or compile START is open** (#1293; R5 § A, § B item 8), and the
window queues behind T36's slot. The guarded swap reclamation once, before the
guest, never beside it. No build on the host at any time.

**The readings before dispatch** (plan § 3, principle 3): the interface
epic's futro takes a T37 kickoff addendum written by the coordinator with
version 2, in T34's to T36's six bold-led paragraphs (R5 § C): the plan in
the order's words (`order.md:653-661`, with the 19 / 4,650 against 15 / 4,561
fact); the assumptions the plan leans on and does not state (that "read"
means no fix; that the pin is the recipe's subject and not its to move; that
freshness covers the recipes; that the guest's installed files are the
recipe's bytes; that the theme's upstream can be compared without a fetch);
the known unknowns, with the futro's T37 lines (`:7`, `:51`, `:209`, `:848`,
`:1004`, `:1008`, `:1010`) as their spine; the patterns; the simulation -- an
Opus lane with only the brief that bumps `PKG_VERSION` because the lens says
currency, bumps the theme without a fetch to compute `PKG_SHA256`, runs
`tools/pkgcheck <path>` and reports PASS, cites `tools/fork-package-freshness`
rc 0 as currency, edits `virtual/image/package.mk:18` for `lowerdeck`,
"fixes" an ES `CMakeLists.txt` line the slice only reads, sources
`config/options` in its worktree and leaves a `build.*` root there (proof
Correction 1), or disables fribidi without the image build that proves the
text path; the adjustments (R5 § C). The stranger's proof of version 1
(`/workspace/tmp/m6-coordinator/kit/t37-proof.md`) made this version 2; its
corrections are `## Version 2: corrections from the proof`. This brief's
hash at dispatch is `V2HASH`.

**Stop only on:** every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); the stage-D pause; an explicit maintainer pause on
#684; a blocker named on #684 (the seat failing its provenance gate twice, a
packet scan hit that is a value, two commands that disagree, a block whose
output differs from § 2's beyond the deltas it records, a file of the 15 at
the lane's tip differing from `2174265e9c` before stage E, a pointer line
that names the predecessor slice, a `build.*` root in the worktree, ruling
(k)); **not** the host's missing toolchain
(nothing here compiles), **not** `tools/fork-package-freshness` printing
nothing for the three recipes (L-10), **not** `tools/pkgcheck`'s vacuous pass
(the control records it, L-21), **not** a `CANNOT` for what only a build
shows (§ 5 item 1), **not** the candidate's nine patches or its link (ruling
(h)), **not** an upstream read that would need a fetch (ruling (e)); or an
execution limit, stated as such with the running log current. A checkpoint is
not a stop. An idle session says it is idle on #684, **and does not end a turn
on a post that asks nothing**: a turn ends on a post or a commit, never on
"next is ...".

**What never runs in this slice:** an image build, a package build or any
compiler; a fetch -- no `git fetch`, no `git ls-remote`, no `gh api` of the
theme's or `lowerdeck`'s repositories, no `rc-preflight` (it fetches
`rocknix/master`), no real `tools/fork-package-freshness` run (only
`--list`, with both refs given); the council runtime from `npm install
--offline`; a handheld; the
owner's accounts or any hosted account; a host listener on a privileged
port; a guest before a grant on #684; M7's roots, worktrees or prep
directories; a held directory (D-WORKFLOW-215; `/workspace/tmp/m6-t34/held/`,
`/workspace/tmp/m6-t36/held/`); anything under `~/.ROCKNIX/` or
`~/.rocknix/`; a read of `emulationstation/package.mk` without the mask, a
print of `:39`, or `set`/`env` after sourcing a recipe; `config/options`
sourced in the worktree -- **no `build.*` root in the worktree at any stage;
a `build.*` root found there is a stop** (ruling (k)); an ES worktree, or a
write in any ES checkout; a change outside the 15; a change to the four
patches' content; a change to `PKG_VERSION` or `PKG_GIT_CLONE_BRANCH` of the
ES recipe; a pin or theme bump; `virtual/image/package.mk` or any
dependency's recipe; ES's `CMakeLists.txt` or `es-core/CMakeLists.txt`; the
French catalog; `docs/es-menu-map.md`; the rule and doc sentences L-17 and
L-18 name (the coordinator's sweep); `tools/pkgcheck` or
`tools/fork-package-freshness` (T6's); a credential-shaped literal in a
fixture; **any write on the guest -- no file, setting or stamp, as § 5's
G-table writes none**; and a theme or font changed on the guest's image.

## Version 1: what the drafting read did not settle

Every `[unverified]` mark above, with the read that settles it, numbered as
in version 1 so the proof's citations still resolve. Version 2 moved the
items the proof settled -- 1, 4, 6, 7, 8, 10, 11, 12 and 14 -- into the body,
each with its command, and narrowed 2, 3, 5, 9 and 17 by the proof's lines;
then the one place where the research files still disagree.

2. **Whether `scripts/install` or `scripts/image` rewrites an absolute link**
   (L-03) -- a grep of both for `readlink`, `symlink` or `-type l` found
   none (proof C7); the lane's read of both scripts whole at the tip settles
   it.
3. **The gettext tools' provider on the build host** (L-08) -- the
   `Dockerfile` and `scripts/checkdeps` carry no `gettext` or `msgfmt` line
   (proof C6), and 8 recipes name `gettext:host`, the ES recipe not (C7,
   C8); the ES recipe's effective dependency closure walked in the export
   for a `gettext:host` link settles whether build order brings the tools,
   and only a build's configure log shows that ES found them.
5. **Whether an `arm` build compiles ES** (L-09) -- `Makefile:50`, `:55`,
   `:60` and `:65` run `ARCH=arm ./scripts/build_distro` for RK3588, RK3576,
   S922X and RK3566 (proof C14); the sourced-recipe assertion for an `arm`
   plan, in the export, settles whether that plan reaches ES.
9. **Which devices' `mesa` builds provide GLES 3 headers** (Q2) --
   `${OPENGLES}` under `projects/ROCKNIX/` is `mesa` at `options:19` and
   `devices/AMD64/options:32` only (proof C14); mesa's effective options per
   device, in the export, or an image build settle it.
13. **The blindspot entries' lines** (§ 3 item 4) -- the lane's `grep -n` for
    their words (not checked by the proof).
15. **`tools/pixelelated-state-check` on a ready guest** (G-05) -- its own
    usage line read on the host before the window (not checked by the
    proof).
16. **Whether `/workspace/repos/rocknix` is one of the M7 roots** the
    never-run list forbids (§ 5's candidate read) -- the dispatch comment
    (not checked by the proof).
17. **R3 cmd 23's `SECRET-PATTERN FILES: 0` over the 19** (§ 5's text
    checks) -- R3 § 6 names the `-f` form, which does not compile against
    the patterns file (the drafter's run, and the proof's C12 with `rc=2`:
    `grep: .githooks/secret-patterns:6: Unmatched ( or \(`), and R3 does not
    print the command it ran. In the hooks' form, its planted positive
    matched first (C13), the proof counted `0` on six of the 15 (C12); **for
    the other nine and the four patches** that 0 is not evidence until the
    lane's own scan in the hooks' form prints its line (a check that cannot
    run has not passed).

**Where the research files still disagree:**

- **Fribidi's path into the sysroot.** R2 § 1 traced SDL2 -> `swaywm-env` ->
  `sway` -> `pango` -> `fribidi` and read `vlc`'s `--disable-fribidi`; R3 §
  2.2 C8 guessed `vlc` -> `libass` (*"not traced"*). The proof confirmed R2's
  chain line by line (C6, C7) and found
  `packages/multimedia/libass/package.mk:11` depending on fribidi too, so R3's
  path is not refuted: whether `vlc` pulls `libass` is L-09's open mark,
  settled by `vlc`'s effective `PKG_DEPENDS_TARGET` in the export. This brief
  takes R2's trace (L-09); either path is build order, D-WORKFLOW-216's
  question.

## Version 2: corrections from the proof

The stranger's proof of version 1,
`/workspace/tmp/m6-coordinator/kit/t37-proof.md` (358 lines), read version 1
at `563857ea02` against the sources by hash: 16 corrections, 11 settled
items, 7 partial, and *What I could not check*. Each correction is applied
at its line, one line each below. The rulings on the three heavy ones are
the coordinator's (D-WORKFLOW-189): ruling (k) for Correction 1, checkbox
13's rows for Correction 6, and the freshness counts for Correction 16;
where a fix offered two forms, the first is taken.

1. **Sourcing `config/options` writes `build.<distro>-<DEVICE>.<ARCH>/.cache_package_{local,global}`** (`config/functions:801-802`; during the proof it wrote two such roots into the P1 research clone): ruling (k) in § 1, and checkbox 19's rulings now (a) to (k); § 3's rule table, item 5 and the leads' header; § 5's scratch export and effective-values block naming the two files, the checker's steps 4 and 7, its refusals and its `--tree`; checkboxes 8 and 16; § 9's mask and temporary bullets; § 10's hand-back, `The rule:` row, simulation, stops and never-run list.
2. **D-UI-090 names the theme**: § 1's ownership rulings, with the decided-table command (no decided row names `ui/`, `es-recipe` or `lowerdeck`).
3. **L-05 is a fact** -- `HFS_DEV_LOGIN` builds the HFS scraper with no `USING:` line (the pin's `CMakeLists.txt:328-330`, `HfsDBScraper.*`, `Scraper.cpp:33`, `scripts/get_env:14`; the loop at `:42-44` names three): § 3's L-05 row, Q4, § 5's CMake comment and `git grep` line, checkbox 9; out of the open list (item 1) and the disagreements.
4. **No `cut` on the ES refs, and T35's ES ref has moved** (`b7fdb3a24c`, 9 ahead of the pin, at the proof; read at stage A): § 1's predecessors and first commands, § 5's merge-base line, § 8 items 1 and 2.
5. **L-02's intent is `git log --diff-filter=A` over `cpugov.patch`** (`40fce2a089`), not `git log -S cpugov`, which prints nothing: § 3's leads header and L-02.
6. **Checkbox 13 counts the 14 files** of ` 14 files changed, 83 insertions(+), 536 deletions(-)`, each upstream moved, the fork moved, or both, with both 8-file lines quoted: § 2's merge debt, the take-up table's currency row, Q7, § 5's `comm` line, § 6 item 7, checkbox 13.
7. **L-08's CMake range is `:565-578`** (the message at `:577`): § 3's L-08 row.
8. **`GLSystem` selects both `-DUSE_OPENGLES_30` and the `Renderer_GLES30` listing**; the define compiles nothing: Q2, checkbox 9.
9. **`order.md:153-155`**, *"then the recipe"* on `:155`: § 1.
10. **The four patches are inventory tier `vendor-carried`**, git's class beside it: § 2's list outside the 15.
11. **`lowerdeck` has three run-time users outside the slice** (`runemu.sh:337-338`, `vertical-check:6-7,143,175,180`, `111-sway-init:163-164`) besides `PKG_UI`, owned by the slices § 2's extended `named` run gives them: § 2's neighbours and that run, the take-up table, Q5; out of the disagreements.
12. **The ES 14 also carry the ZRAM swap menu**, with no distribution half under `ui/`: § 2's merge debt.
13. **`essway.service`'s two hunk headers** (`@@ -4 +4 @@`, `@@ -11,0 +12,3 @@`) replace "three lines": § 2's merge debt.
14. **The theme's `:20` deletes four includes** (`classic` has none): § 2's files table.
15. **`cb50b45f6e` is first in `git log --reverse` order**, not by date: § 2's fork commits.
16. **`tools/fork-package-freshness --list` fails open without its refs** (`fatal: bad revision 'upstream/next'`, `rc=0`): rulings (d) and (e), L-10, L-21's Backlog lead (a missing ref is the third fail-open, the proof's C8 its observation), § 5's freshness line (`FRESHNESS_BASE` and `FRESHNESS_HEAD` given, `lines=48` and `ui=0` checked, never `rc=0`), checkbox 8, § 10's never-run list.

**Settled by the proof, now in the body with their commands:** open items
1 (L-05), 4 (L-01's fixture in `python3 -I` with `xml.etree`), 6 (L-19's
line is upstream's), 7 (L-20's `system-theme` default), 8 (fribidi's chain
owners, § 2), 10 (Q2's units and autostart by `scripts/install`), 11
(`PKG_UI` unconditional; Q5, G-06), 12 (the six files' credential scan, § 1)
and 14 (the effective-values call, § 5, with ruling (k)); L-16's two commits
(§ 2, L-16); and the disagreements on 15 against 19 (ruling (a), reproduced
by the proof's C2), `SCREENSCRAPER_RUNTIME_DEV_LOGIN` at `:30` (§ 5's
credential comment), `HFS_DEV_LOGIN` (L-05), `tools/pkgcheck`'s path (stderr
behind a carriage return, § 5's lint comment), the installed
`es_features.cfg` (G-03), the French count (§ 8 item 2) and `lowerdeck`'s
consumers (Q5). From the proof's other checks: L-02's hunk found in the pin
at `1061`, so it would apply with an offset; L-18's `scripts/unpack:159`
device directory; the splash patch's removal shown as a rename (§ 2); and
H700's `VULKAN_SUPPORT=no` (Q2).

**Open after the proof:** items 2, 3, 5, 9, 13, 15, 16 and 17 of
`## Version 1: what the drafting read did not settle`, and fribidi's `libass`
path there; the owners of `lowerdeck`'s three run-time users, which the
lane's extended `named` run prints (§ 2); and the proof's *What I could not
check*, each the lane's to read at stage A or the dispatch comment's to
give: the authors' `HEAD`s (R1 C20's network read, ruling (e)); #684's body
and every issue state; the 80 `feature/m6-*` refs and `next` as a ref; the
lane-branch audit files the take-up table cites; the M7 candidate and its
image (G-01's `BUILD_ID`, the digests, the `ui/` tree hashes); the effective
`PKG_CMAKE_OPTS_TARGET`'s printed tail (the proof's own cut; the recipe's
`:19-25` and `:30` carry both options); and `tools/register-check`'s `711`
against the decided table's `ids decided 698 open 13`.

**Checks on this file**, each command's own output, run on this file as
written:

- `/usr/bin/grep -c -E '__[A-Z0-9]+__'` prints `0`.
- The hooks' credential pattern, built as `.githooks/guard-lib` at
  `563857ea02` builds it -- `.githooks/secret-patterns` sourced for its one
  `SECRET_PATTERNS` regex and compile-checked by
  `printf '' | grep -E -e "$SECRET_PATTERNS"` (rc at most 1), never `-f` --
  matched `1` on a private-key header line assembled at run time, then
  `grep -c -E -e "$SECRET_PATTERNS"` printed `0` on this file.
- `/usr/bin/grep -c '\[unverified\]'` prints `19` on version 1 and `9` on
  this file.
- `/usr/bin/grep -c ''` prints `1875`.

Version 2, 2026-11-01 00:24:37 UTC, after the stranger's proof of version 1
