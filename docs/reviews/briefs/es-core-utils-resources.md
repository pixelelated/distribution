# Review brief: M6.P2 T36, EmulationStation's utilities, resources and renderers: the file helpers and their cache, the process and shell helpers, the string and time helpers, the fonts, the texture cache and its loader, the GL renderers (#683)

**Version 2, 2026-10-31, after the stranger's proof of version 1 (`e52274caf9`)**
(D-WORKFLOW-189; `docs/reviews/plan-for-the-plan.md` § 6b, § 6c, § 7; the
proof is `/workspace/tmp/m6-coordinator/kit/t36-proof.md`, 18 commands and
170 check rows -- 149 ok, 17 citing a correction, 4 notes -- and `##
Corrections in version 2` at the end records its sixteen corrections, cited
in the body as `proof C<n>` and its commands as `proof CMD<n>`). Written from five
read-only research files -- R1 membership and provenance, R2 the code read at
the pin, R3 tests, build and harness, R4 the inherited items, R5 the model and
the ceremony (`/workspace/tmp/m6-coordinator/kit/t36-research/`, in no tree)
-- and nothing else: every figure here is one of their quoted tool lines,
cited as `R1 C<nn>` (R1's commands C01 to C23), `R2 cmd <n>` or `R2 § <n>`,
`R3 cmd <n>` or `R3 § <n>`, `R4 item <n>` or `R4 § <n>`, `R5 C<n>` or
`R5 § <letter>`, or a line the stranger's proof printed (`proof CMD<n>`), or
a line the drafter printed on 2026-10-31 in the coordinator worktree and says
so; **`[unverified]` marks what no tool line settles, with what would settle
it**, and `## What version 2 does not settle` near the end lists every one
(version 1 listed nine; the proof settled four, narrowed four and left one,
proof U-1 to U-9). Counts by `/usr/bin/grep`,
never the shell's function (#1138). The structure is T35's brief
(`docs/reviews/briefs/es-core-window-input.md`, version 2 at `8b5d9b9b62`,
2,120 lines by `grep -c ''`, R5 C3); every T35-specific paragraph is replaced
and every boilerplate paragraph R5 § A marks *copy* is copied with this
slice's names, numbers and placeholders; the errata R5 § B lists are written
out of it (the register line from the decided table only, the placeholder
check in pieces, the tips loop recording whichever line prints,
`tools/pkgcheck` by package name, every count as its tool prints it). The
rule, register and futro lines are the coordinator worktree's at
**`4536815b6b`** (`feature/m6-renovation-plan-346`; R5 C9, C10: the tip moved
from `b3daa17ab8` under the research and `git diff --stat b3daa17ab8 HEAD`
named three files, none a rule, the register or a brief). The drafter re-read
at `153ca325b3` on 2026-10-31 at 11:30 UTC: `git diff --stat 4536815b6b
153ca325b3 -- .claude/rules docs/decision-register.md docs/es-menu-map.md
docs/blindspot-register.md docs/futros docs/reviews/briefs` printed no line,
the decided table's highest IDs printed R5 § G's nine, and `## Open
decisions` opens at `:773`. At `acc4674006` (11:39 UTC, the coordinator's
tip while version 1 was drafted) the same `awk` printed D-WORKFLOW-215
(`:771`) in place of D-WORKFLOW-214, `## Open decisions` at `:774`, and
`git diff --stat 153ca325b3 acc4674006 -- .claude/rules docs/es-menu-map.md
docs/blindspot-register.md docs/futros docs/reviews/briefs` printed no line
-- so every rule line cited here holds at all three, every register line up
to `:770` holds, and the lane re-reads them at `COHASH`. The proof read the
rules again at `e52274caf9` (`rules diff 4536815b6b..e52274caf9: []`, proof
CMD8) and the register at four hashes (`## Open decisions` `:774` at
`acc4674006` and `e52274caf9`, proof CMD9); the coordinator's tip at dispatch
is read then, as `COHASH`.

## 1. Identity

- **Issue:** #683 `M6.P2 E339/T36: interface: EmulationStation's utilities,
  resources and renderers` (read 2026-10-31T11:14:28Z by `gh --repo
  pixelelated/distribution issue view 683`: OPEN, milestone `M6: Codebase
  renovation`, no labels, **0 comments**, parent #339, REST id `5992344352`;
  R5 C8, § F), **retitled at dispatch to `M6.P2 E700/T36: interface:
  EmulationStation's utilities, resources and renderers`** and re-parented
  from #339 to #700 (`milestone-phase-naming.md`; the body's anchor reads
  *"under epic #339 until this area's epic is filed at its first dispatch
  (then re-parented and retitled `E<epic>/T36`)"*, and #700 is filed; #681
  and #682 carry `E700/T34` and `E700/T35` with parent #700; R5 § F). Slice
  `es-core-utils-resources` (`k: 36`) in `docs/reviews/slices.json`,
  thirty-sixth in `docs/reviews/order.md` (`order.md`, `slices.json` and
  `inventory.json` are the P1 branch's, which the lane's worktree is stacked
  on; not on `next`, not in the coordinator worktree; R1 read them in the P1
  research clone `/workspace/tmp/m6-coordinator/t11-research/tree` at
  `2174265e9c` by `git show`, R1 C01, C02): its § T36 opens at `order.md:643`
  and `:645` carries *"**id**: `es-core-utils-resources`; **kind**: currency;
  **lens**: cost against value"* (R1 C02). The section's lines (R1 C02):
  *"**why here**: `utils` (40,926 lines; `StringUtil`, `Platform`,
  `AtomicFileUtil`, the fork's last-good writes), `resources` (fonts,
  textures) and `renderers`"*; *"**paths** (58 paths, 50,840 lines, 50,840
  read, of which 6,212 fork-own; 0 patch and config lines; reach shipped 58):
  areas `interface`; globs `es:es-core/src/{utils,resources,renderers}/**`,
  `!es:es-core/src/utils/AtomicFileUtil.*`"*; read before none
  (D-WORKFLOW-187); *"**depth**: Independent -- an ordinary code slice"*;
  interacting subsystems *"every page; `es-code-traps.md`"*; closing evidence
  *"audit folder, lint PASS, punch list through Phase 7"*. #683's body: 27
  lines, 5 generated checkboxes, **Provenance tiers:** *fork-own 15,
  upstream-carried 43* (R5 § F). The selector is one object,
  `{"globs": ["es:es-core/src/{utils,resources,renderers}/**",
  "!es:es-core/src/utils/AtomicFileUtil.*"]}` (R1 C15), area `interface`.
  **`order.md:181` is not this slice:** `| T36 | T15 |
  `tooling-last-good-test` |` is a row of the *Renumbering, second version to
  third* table, so a "T36" in the preliminary review's answers is today's T15
  (R1 C20, C21; R1 § 6 D8). **Epic:** #700 `M6.P2 E339: Area epic: the
  interface, EmulationStation (T2, T18, T20, T21, T26, T31 to T37, T44)`
  (R5 § F): T2 #649, T18 #665, T20 #667, T21 #668, T26 #673, T31 #678, T32
  #679 and T33 #680 are accepted and their issues stay open until the
  integration moves the pin on `next` (§ 10); **T34 #681** is complete (the
  coordinator's commit *"T34 (#681) complete at 308d0f7571"*, proof K-170;
  its distribution tip now `49c6b43f27`, *"T34's held reply declared by its
  receipt's sha256 for the lint's held mode"*, the drafter's `git log -1` on
  2026-10-31; its ES branch `feature/m6-es-core-components-681` unchanged at
  `52f0ff5128`, 8 ahead of the pin, touching none of the 58, R1 C17, proof
  K-031); **T35 #682** is at stage E, its distribution branch moving, so
  **its tip is read at stage A**, never copied from here (`bb1754e581` at
  R4's read, `5d7650c1dc` at the proof's, proof K-170); its ES branch is at
  the pin, 0 ahead, with no `origin/` ref (R1 C17; R5 C12; proof K-032);
  this slice; T37 #684 and T44 after. The futro
  `docs/futros/2026-10-23-m6-interface.md` (996 lines at `4536815b6b`, R5 C5,
  C10; its last heading `:994`, *Errata from the stranger's proof of T35's
  brief*) takes a **T36 kickoff addendum** written by the coordinator with
  version 2, after the last heading present at dispatch, in T34's and T35's
  six bold-led paragraphs (R5 § C). **Milestone:** M6. **Predecessors:** T2,
  T20, T21, T26, T32, T33, T34 and T35 each routed items here by name or
  changed one of the 58 on their own ES branch; every one is listed with its
  lines and its disposition in § 2 under *Already found; do not re-find; take
  up* (R4 § 1's items 1 to 42), which points back at the rulings below.
  **Beside it:** T35's lane, the other es-core slice, possibly in flight on
  the same host; the host shared through
  `/workspace/tmp/m7-m6-host-coordination.txt`; a window for this slice is
  asked for on #683 and granted there and in that file's queue (§ 5 item 2).
- **The order's sentence is true of the membership, and this brief says what
  the title does not.** The globs give exactly the 58: the three directories
  hold 60 files at the pin and the negated glob removes exactly
  `utils/AtomicFileUtil.cpp` and `utils/AtomicFileUtil.h` (R1 C05), and
  `ES-CORE BY SLICE` prints four rows and no unassigned one -- `96 paths
  22575 lines (('es-core-window-input',), 'rest')`, `80 paths 21984 lines
  (('es-core-components',), 'non-rest')`, `58 paths 50840 lines
  (('es-core-utils-resources',), 'non-rest')`, `8 paths 3344 lines
  (('es-state-and-bridge',), 'non-rest')` (R1 C15), with `unassigned: 0` and
  `ambiguous: 0` over the whole partition (R1 C04). **The `why` names a file
  and a behaviour that are not in it:** `AtomicFileUtil` and *"the fork's
  last-good writes"* it performs are T21's (#668) by the non-rest glob
  `es:es-core/src/utils/AtomicFileUtil.*` (R1 C15: `not-in-T36 non-rest
  [('es-state-and-bridge', 21)]`, 829 and 215 lines), and the `why`'s 40,926
  is all **35** paths under `utils/` with `AtomicFileUtil.*`; this slice's
  `utils` is **33 paths, 39,882 lines** (R1 C05, C08; R1 § 6 D4). What the
  title leaves implicit: the 58 are **25 `.cpp`, 32 `.h` and one `.hpp`**
  (`utils/zip_file.hpp`), **14 under `renderers/`, 11 under `resources/`, 33
  under `utils/`**, no subdirectory (R1 C05) -- the file helpers and their
  session cache, the process and shell helpers (`Platform`), the string
  helpers with `maskSecrets`, the time helpers, the launch command's word
  (`CommandLineUtil.h`), the offline proxy's URL test, the zip reader, the
  math-expression evaluator, the thread pool, MD5, the colour parser, the
  Korean table, the fonts with the fork's tab stops, the texture data, cache
  and loader, the resource manager, and seven GL renderer pairs. **Two
  upstream headers are most of the lines:** `utils/han.h` 20,923 and
  `utils/zip_file.hpp` 10,011, `han.h + zip_file.hpp grep -c 30934` against
  `the other 56 grep -c 19906` (R1 C09; R1 § 6 D5). **"6,212 fork-own" is
  the whole lines of the 15 files the fork touched** (`TIER fork-own 15 paths
  6212 lines`, R1 C08), not the lines the fork wrote: the fork's own change
  over the 58 is **`15 files changed, 1032 insertions(+), 60 deletions(-)`**
  against the merge base and the same line against `bccd715707` (R1 C11,
  C07), 19 log lines with two merges (R1 C12); the read's tiers are
  **fork-added 6, fork-modified 9, upstream-carried 43**, and **all 43
  upstream-carried blobs are byte-identical to `rocknix/master`** (R1 C10);
  **no `renderers/` file is touched by the fork** (R1 C08, C11). § 2 carries
  the figures.
- **Ownership rulings, stated once; § 2's take-up list points here.** **T36
  owns `es-core/src/{utils,resources,renderers}/**` less
  `utils/AtomicFileUtil.*` -- the 58 paths -- and nothing else.**
  D-WORKFLOW-213 (`docs/decision-register.md:759`, T34's row) names
  *"`TextureData.cpp`, `TextureResource.cpp`, `Font.cpp`, `FileSystemUtil.cpp`
  and `OfflineProxyUrl.cpp` are T36's (#683)"* and records that *"the earlier
  briefs' 'T35's' was right for the popups and the window and wrong for the
  texture cache and the font"*; D-WORKFLOW-214 (`:768`, T35's row) adds
  *"`es-core/src/utils/Platform.cpp` (by `utils/**`: its `system()` wrapper and
  `ProcessStartInfo`) and `utils/DownloadFile.*` are T36's (#683)"* (R1 C16;
  R4 § 3; R5 § G). No other decided row names one of the 58 by file name
  with a slice number; D-INFRA-011 (`:280`) names `Platform.cpp` as a
  credential-redaction constraint, not an ownership claim (R1 C18, C20).
  **This slice's own ownership row is the coordinator's, written at dispatch
  (**D-WORKFLOW-216**: R5 § G read D-WORKFLOW-215 as the next free ID at
  `4536815b6b`, and the coordinator wrote D-WORKFLOW-215 at 11:37 UTC on
  2026-10-31 -- the test for holding a finding off the public tracker, not
  this slice's row -- so the drafter's `awk` over the decided table at
  `acc4674006` printed D-WORKFLOW-215 as the highest WORKFLOW row, `:771`,
  with `## Open decisions` at `:774`); the pointer's `Register:` line is
  filled from the decided table at `COHASH`, § 10.** The rulings:
  (a) **`utils/AtomicFileUtil.*` is T21's (#668)** by its non-rest glob, and
  with it the "last-good writes" of #683's `why`; the slice reads
  `AtomicFile::writeText` only as the tree's atomic writer against which its
  own writers are measured (R2 § 5), never as its own.
  (b) **`utils/DownloadFile.{cpp,h}` is not at the pin**: T21's
  `3ae9610b0f` adds it on T21's ES branch (`DownloadFile.cpp` 61,
  `DownloadFile.h` 29, R1 C17; R3 cmd 7, cmd 8: no curl), outside the 58 (the
  block prints `es-core/src/utils/DownloadFile.cpp NOT IN INVENTORY`, R1 C15)
  because the P1 inventory predates it (R1 § 6 D7). D-WORKFLOW-214 names it
  T36's by `utils/**`; **for this slice it is a collision named in the
  hand-back and the integration's to reconcile**, never read, reviewed or
  fixed by the lane (R4 item 20's dispatch question, answered here).
  (c) **`utils/FileSystemUtil.cpp` is T36's** by D-WORKFLOW-213 and -214; the
  places that call it T21's are superseded by those rows -- `t33-streams.md:14`,
  `:178`; T33 `04-analysis.md:73`; `es-app-system.md:969`;
  `es-app-views-scrapers.md:464`, `:793`; `es-pages.md:51`, `:407`, `:440`,
  `:625`, `:1070`; #1271's body `:38` (R4 § 8 delta 1). The lane cites the
  rows, not those lines.
  (d) **Three fixes are already on other lanes' ES branches in this slice's
  files**: T20's `d9afa5c7c` (`readAllText` under three bytes, #1177; on
  `feature/m6-es-achievements-pages-667` at `5c0ddaaeef`, `utils/FileSystemUtil.cpp`
  +4), T21's `f7c16144d` (`renameFile`'s absent source and the destination
  removed first, #1191; on `feature/m6-es-state-and-bridge-668` at
  `3ae9610b0f`, `utils/FileSystemUtil.cpp` 17 in the stat's change column) and
  T26's S8 (`GetShOutput`'s lost byte and unchecked `popen`, #1225; on
  `feature/m6-es-guimenu-673` at `757f5370ea`, `utils/Platform.cpp` `15
  insertions(+), 5 deletions(-)`) (R1 C17; R3 § 1.5; R4 items 12, 13, 23).
  **The lane reads each at stage A with `git -C <W> show <hash>` (and `git -C
  <W> diff <PIN> <tip> -- <file>`), records it as a collision with its owner
  in `02` § The merge debt and in the hand-back, and does not re-make it**;
  its own case over the same lines is the FAIL-at-pin control the merged fix
  turns green (R3 § 1.5, § 3).
  (e) **The controllers blob is T35's** (D-WORKFLOW-214 (a); T2 FD-7 posted
  it "for T36", and T35 found its premise contradicted, R4 item 37); nothing
  here.
  (f) **`Splash.h:11`'s brand is T35's**: `git grep -i pixelelated --
  es-core/src` finds that one line, and nothing in the 58 upper-cases the
  brand on its own; the formatter that could is a component's uppercase
  option (T34's), which calls this slice's `toUpper` (R2 § 1.1, cmd 16;
  D-WORKFLOW-144 `:604`).
  (g) **`tests/app-unit/fakes/utils/FileSystemUtil.h` is not the lane's to
  edit**: it doubles four of this slice's functions (`exists(const
  std::string&, bool useCache = true)`, `readAllText`, `removeFile`,
  `getFileName`) for `proxycards-tests`, `jobs-tests` and `bookkeeper-tests`,
  which put `fakes/` first (R3 § 1.3); **a T36 change to any of those four
  signatures is a collision named in the hand-back**, as T35's `Window.h` and
  T34's `AsyncNotificationComponent.h` were.
  (h) **T35's case 3.11 already FAILs at the pin in T35's harness** -- *"a
  file written by pugixml's save_file after a cached miss reads as present
  (InputManager.cpp:1187 with utils/FileSystemUtil.cpp, T36's)"*, one of the
  seven `TEST CASE:` failure lines of `RUN window-input-tests: rc 1; [doctest]
  test cases: 10 | 3 passed | 7 failed ...` (T35 `stage-c/build-tests.out:65`,
  the line's tail abridged here; proof C8, CMD15), lifting
  `FileSystemUtil.cpp:48-341` and `:1122-1147` verbatim (R3 § 1.4, cmd 14,
  cmd 15). **T36 owns the fix (the cache); T35 owns the
  case.** A stage-E stream that changes the cache's answer re-runs T35's
  case unchanged from T35's tip and records its line; the coordination is
  the coordinator's, at both lanes' pauses (§ 5 item 4).
  (i) **#1263's texture-cache half is T36's** (T32 PL-07: a picture written
  from outside ES stays hidden until a restart; `TextureData.cpp:331`, `:339`,
  `:410` are cached `exists(localFile)`), the caller's half T34's
  (D-WORKFLOW-213 (a)); #1263 (OPEN, `bug`) keeps its picture checkbox open
  for this slice's record (R4 item 1).
  (j) **`utils/Platform.cpp` is T36's** whole -- `ProcessStartInfo`,
  `runSystemCommand`, `GetShOutput`, the quit paths, the address queries
  (D-WORKFLOW-214 (b); T2 SS-1's "T35's" and `t26-streams.md:81`'s
  `es-core/src/platform/Platform.cpp` superseded: there is no `platform/`
  directory, R4 § 8 deltas 3 and 4).
  (k) **The held T34 note for T36 is the coordinator's**, delivered at
  dispatch in a scoped form; this brief does not carry it and the lane does
  not look for it (R4 item 41, § 7).
  So the lane writes no line outside the 58 (a fix in a neighbour is named
  for its owner at the pause).
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, post on #346, #585 or #909, or decide a question of scope: those
  are the coordinator's, reached through #683, one question at a time. What
  it does file: its own audit punch-list issue (stage D) and a `bug` issue
  for a defect it proves, with its trace and `Already written:` line
  (D-WORKFLOW-187). A fix lands only under a stream brief the coordinator
  writes at the stage-D pause, **on the EmulationStation branch**. The read's
  tiers are **fork-added 6 / fork-modified 9 / upstream-carried 43** (§ 2 §
  Three things the figures hide, (2), which reconciles them with the
  inventory's `fork-own` 15 / 6,212 lines). A defect in a line the fork
  wrote is the fork's to fix; a defect in an upstream line is a contained fix
  under `bugs-are-agent-first.md` rule 6 and a #585 line (D-WORKFLOW-164,
  never sent, D-WORKFLOW-165). D-UI-079's lanes (`engineering-practices.md`
  § Change stays inside the fork's lanes): the surfaces the fork's
  non-merge commits on the 58 work in (R1 C12's list) -- the credential mask (`80f52e500`, then
  `dcf7fa8c7`, `b036967fc`, `3157d1a69`, `107597312`, `893a81403`,
  `217872e32`), the font's tab stops and header measure (`a82dcdf4c`,
  `7b18c4489`), the shared SVG's raster size (`20824cc29`, #181), the launch
  command's word (`2f5fd6332`), the link test and the multi-line command
  output (`0cc13be61`, `4e34bc2d1`), the save state manager's times
  (`8b7340f5b`, `5067f7a1b`, `296aa5966`), the offline proxy's store
  (`0ec3f43ae`) (R1 C12) -- are the lanes; **the file helpers and their
  cache, `ProcessStartInfo::run`, `runSystemCommand`, `GetShOutput`, the quit
  paths, the UTF-8 case tables, the font's scaling, height and glyph cache,
  the texture loader and its VRAM budget, `TextureResource`'s map, the
  resource manager, the thread pool, the zip reader, the math evaluator and
  the seven renderer pairs are upstream surfaces** (R3 § 4: *"`renderers/`
  and `resources/` are upstream surfaces outside the fork's lanes"*) read for
  brittleness and cost (the lens) and left as upstream has them, and a
  defect in one is still ours to close when the fix is contained (rule 6).
  The read is the pin `16dbac5211`'s bytes; M7's worktrees are never read.
- **Two worktrees, one session, and four placeholders.** The distribution's
  `feature/m6-es-core-utils-resources-683` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-utils-resources-683`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** (the P1 tip; or the one the dispatch comment names) with the
  coordinator's branch merged in and the lane's pointer seeded; and the
  EmulationStation fork's `feature/m6-es-core-utils-resources-683` at
  `W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683`,
  cut by the coordinator from **the pin
  `16dbac5211eea7e70db7394372033be2be7df829`** and clean until stage E: the
  sources are read and the fixes are made there, and the pin is not moved by
  the lane. **`W` is that one path in every block of this brief, § 5's runs
  included; until it exists -- neither worktree does before dispatch (R1
  C01: `no ES worktree named *683* yet`; R5 C12: neither T36 path exists) --
  the `qa-integration` checkout at the same pin, clean, stands in, read by
  `git -C` only, and gives the same lines (every quoted ES line in R1, R2 and
  R3 was printed there).** **Four placeholders stand in this brief for
  hashes that do not exist until dispatch:** `COHASH` (the coordinator's tip
  merged into the lane's branch), `MERGE_HASH` (that merge commit, the lane's
  dispatch tip), `TIPHASH` (the lane's own tip as it moves; at stage A it is
  `MERGE_HASH`) and `V2HASH` (this brief's commit on the coordinator's branch
  at dispatch, version 2 after the proof; version 1 has no dispatch hash).
  The dispatch comment on #683 and the seeded pointer carry their values; the
  lane reads them there, never guesses them, and § 9's placeholder check
  names all four. **Three earlier lanes' ES branches touch one of the 58**
  (R1 C17): T20's `5c0ddaaeef` and T21's `3ae9610b0f` change
  `utils/FileSystemUtil.cpp`, T26's `757f5370ea` changes `utils/Platform.cpp`,
  and T21's adds `utils/DownloadFile.{cpp,h}` under the glob (rulings (b),
  (d)); T34's `52f0ff5128` and T35's branch at the pin touch none (R1 C17).
  So `Platform.cpp` is the one file changed by the fork before the pin, by an
  M6 lane and by batocera, and `FileSystemUtil.cpp` is changed by two lanes
  and by batocera but not by the fork before the pin (R1 C19). The other ES
  checkouts under `~/Development/emulationstation-next.worktrees/` are read
  with `git -C <checkout> show <hash>:<path>` only, and nothing is fetched
  (§ 10). Until the dispatch comment exists the pointer is not seeded and
  nothing starts.
- **Depth: Independent** -- one seat from another lab (plan § 6c,
  D-WORKFLOW-137; `adversarial-council.md`: an Anthropic-led audit's reviewer
  is pinned GPT-6 Astra; no Gemini seat): Astra at `max` over a trimmed,
  scanned packet (D-WORKFLOW-195 -- **the 15 fork-added and fork-modified
  files whole** (6,212 lines by `grep -c ''`, the inventory's rule, R1 C08,
  which the lane replaces with the packet's own `wc -l`) **and of the 43
  upstream-carried files only the ranges the questions cite**; **`han.h`
  (20,923) and `zip_file.hpp` (10,011) are never whole in the packet** --
  a cited range at most (R1 C09; R1 § 6 D5); the manifest names every
  trimmed file and range; nothing in the 58 is a binary), a probe then one
  refutation (one in-call retry allowed); `review-plan.json` records depth
  `independent` and the one reviewer with its served model; **exactly two
  keyed `tools/council/run invoke` calls**, every other `tools/council/run`
  call with `COUNCIL_ENV_FILE=/nonexistent` (the recipe is
  `.claude/skills/council/SKILL.md` and its `references/`; the runtime under
  `tools/council/` from `npm install --offline`, no fetch). The packet is
  scanned before it leaves. **What the scan will hit inside the 58, so the
  lane dispositions rather than stops:** `maskSecrets`'s own vocabulary in
  `StringUtil.cpp:446-804` -- the credential words it matches
  (password, pass, token, key, secret, psk, pin), `setrootpass`, `wifictl
  connect/enable`, `?y=`, `&t=`, `&p=` (R2 § 0; its name list `:513`, R4 item
  25) -- and `OfflineProxyUrl.h:29`, `const char* const StoreOnlyHeader =
  "X-RA-Store-Only: 1";` under `:27-28`'s *"As HttpReqOptions::customHeaders
  takes it, name and value in one line."* -- a fixed header line whose value
  is `1`, dispositioned *a fixed header line, no credential* -- beside the
  loopback `Base` (`:22`) (proof C5, CMD5, CMD7; R2 § 0); so
  `packet-manifest.json` records **every scan hit dispositioned by file:line**
  (library plumbing / macro name / identifier / setting name / value), and a
  hit that is a value stops the packet; no value ever reaches the packet or
  an artifact.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at stage
  A. **The session is the T1 session (`m6-t1-os-launch`), free since T16's
  close-out** (the day's work log: the T1 lane *"idle at `done` since 06:47"*
  and *"T16 complete (11:07 UTC)"*, and *"T36 (#683 ...) research launched
  ... for the free T1 session"*, R5 § D, C11).
- **The first commands** (stage A, in the distribution worktree;
  `8ebaf8daad` is `next`'s commit the P1 branch stacks on and `651150fc88` is
  `upstream/next`'s, both copied from T35's brief § 1, shared by every M6
  lane, R5 § D):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-core-utils-resources-683
cat .github/sessions/saved-session-state-feature-m6-es-core-utils-resources-683.md   # the pointer: the dispatch's two hashes; § 10 names the lines to check
git status --short | wc -l                                                   # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1               # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                # the pin; 0
git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10                     # cada856d86: the merge base with ROCKNIX's master; bccd715707 is its parent (R1 C01)
git -C "$W" rev-parse --verify rocknix/master | cut -c1-10                    # f6c542872e, read from the shared refs (R1 C01)
git -C "$W" rev-parse --verify batocera/master | cut -c1-10                   # b2ceb55a7e, read from the shared refs; context only (R1 C01)
git -C "$W" merge-base "$PIN" batocera/master | cut -c1-10                    # 1750dded8c: ROCKNIX has merged nothing from batocera since 2026-09-13 (R1 C01, C14)
for b in m6-es-launch-path-649 m6-es-cloud-pages-665 m6-es-achievements-pages-667 m6-es-state-and-bridge-668 m6-es-guimenu-673 m6-es-pages-678 m6-es-app-views-scrapers-679 m6-es-app-system-680 m6-es-core-components-681 m6-es-core-window-input-682; do printf '%s ' "$b"; git -C "$W" rev-parse --verify "origin/feature/$b" 2>&1 | cut -c1-10; done   # ten tips; R1 C17 printed 55158d2a64 d55235d4b3 5c0ddaaeef 3ae9610b0f 757f5370ea 95852f8736 b52245036f f802c55c62 52f0ff5128 for the first nine and no origin ref for T35's (R5 C12: `fatal: Needed a single revision`); each line is recorded as it prints -- a hash or `fatal:`, whichever -- and neither is a stop
tools/register-check >/dev/null && echo register-ok
date -u +%H:%M:%S; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200   # who holds the host, with the time of the read (M7 writes timestamped lines: read the whole tail); no guest before a grant on #683
```

Every ES line above printed what its comment says on 2026-10-31 by `git -C`
against `qa-integration` (R1 C01, C17; R5 C12); the `cat` cannot run before
the pointer is seeded, and `W` does not exist before dispatch; the `stacked`,
`upstream-next-is-here` and `register-ok` lines are the lane's own. The
tips loop's tenth line is T35's ES branch, which had no `origin/` ref at the
research's read: **the lane records whichever line prints** (T35's brief
expected `fatal:` for T34's ref and the ref resolved at stage A, R5 § B
item 3). The host file's tail is whatever the host is doing at the moment of
the read, so the lane records the time beside the lines; a sentence about
what the tail "shows today" is never written into an artifact without one.

## 2. Scope

**The membership, by the block that defines it** (run from the lane's
distribution worktree, stacked on the P1 branch, which holds
`docs/reviews/{inventory.json,slices.json}` at `2174265e9c` -- sha256
prefixes `d17b9cac4b2c2245` (`inventory.json`) and `49bc2745664e52f4`
(`slices.json`), R1 C06, proof C3, CMD2; the script is
T35's `membership.py` with three lines changed -- the slice id in `hits`, the
`named` list (28 paths: twelve of this slice's, then the neighbours the brief
excludes or points at, `utils/DownloadFile.cpp` among them, expected to print
`NOT IN INVENTORY`) and the `in-T36` / `not-in-T36` label; the `ES-CORE BY
SLICE` prefix is unchanged; keyword arguments are spaced `key = lambda` so
this file carries no key-equals token; and the ES lines adapted: **one line
added**, the `ls-tree ... | diff -` proof that the inventory's set equals the
pin's tree through the globs (R1 § 5). **The heredoc is saved once and run
twice** -- first against `/dev/null` to make the paths file from its own TSV,
then against that file to prove equality. **The text below is R1's
`block.sh` byte for byte** (90 lines, sha256 prefix `ebe18e98a244a77d`, R1
C06); R1 ran it on 2026-10-31 with only the `W=` line changed to the
`qa-integration` checkout (C06's one-line `diff`, C07), and the expected
lines are that run's, byte for byte. The awk reads columns 1 and 2, `tree`
and `path`, the inventory's first two by its own `columns:` line):

```bash
mkdir -p .qa-scratch/t36
cat > .qa-scratch/t36/membership.py <<'PYEOF'
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
kof={s["id"]:s["k"] for s,_ in sl}
mine=[]
for r in rows:
    if r["tree"]!="es": continue
    h,kind=hits(r)
    if h==["es-core-utils-resources"]: mine.append(r)
mine.sort(key = lambda r:r["path"])
want=[l.strip() for l in open(sys.argv[1]) if l.strip()]
got=[r["path"] for r in mine]
print("mine:",len(got),"paths.txt:",len(want),"equal:",got==want)
print("only-mine:",sorted(set(got)-set(want))); print("only-paths.txt:",sorted(set(want)-set(got)))
c=collections.Counter
print("lines:",sum(r["lines"] or 0 for r in mine), "reach:",dict(c(r["reach"] for r in mine)),"tier:",dict(c(r["tier"] for r in mine)),"lang:",dict(c(r["language"] for r in mine)))
print("fork-own lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="fork-own"))
print("read lines:",sum((r["lines"] or 0) for r in mine if r["language"] in CODE and r["tier"]!="vendor-carried" and r["reach"]!="unreached"))
print("TSV"); print("\t".join(cols))
for r in mine: print("\t".join(str(r.get(k)) for k in cols))
print("CLAIMS")
named=["es-core/src/utils/FileSystemUtil.cpp","es-core/src/utils/StringUtil.cpp","es-core/src/utils/Platform.cpp","es-core/src/utils/OfflineProxyUrl.cpp","es-core/src/utils/TimeText.cpp","es-core/src/utils/TimeUtil.cpp","es-core/src/utils/CommandLineUtil.h","es-core/src/utils/zip_file.hpp","es-core/src/resources/Font.cpp","es-core/src/resources/TabStops.h","es-core/src/resources/TextureResource.cpp","es-core/src/renderers/Renderer.cpp","es-core/src/utils/AtomicFileUtil.cpp","es-core/src/utils/AtomicFileUtil.h","es-core/src/utils/DownloadFile.cpp","es-core/src/Settings.cpp","es-core/src/SystemConf.cpp","es-core/src/HttpReq.cpp","es-core/src/components/TextComponent.cpp","es-core/src/components/MenuComponent.cpp","es-core/src/ImageIO.cpp","es-core/src/Log.cpp","es-core/src/Window.cpp","es-core/CMakeLists.txt","es-app/src/CloudText.cpp","es-app/src/ApiSystem.cpp","es-app/src/guis/GuiMenu.cpp","es-app/tests/unit/CMakeLists.txt"]
byp={r["path"]:r for r in rows if r["tree"]=="es"}
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY"); continue
    h,kind=hits(r); print(p, "in-T36" if p in got else "not-in-T36", kind, [(x,kof[x]) for x in h], "tier",r["tier"],"lines",r["lines"],"area",r["area"])
print("ES-CORE BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["tree"]=="es" and r["path"].startswith("es-core/"):
        h,kind=hits(r); cnt[(tuple(h),kind)]+=1; ln[(tuple(h),kind)]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:-kv[1]): print(v,"paths",ln[k],"lines",k)
PYEOF
python3 -I .qa-scratch/t36/membership.py /dev/null > .qa-scratch/t36/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^CLAIMS$/{p=0} p && $1=="es" {print $2}' .qa-scratch/t36/block-1.txt > .qa-scratch/t36/paths.txt
wc -l .qa-scratch/t36/paths.txt
python3 -I .qa-scratch/t36/membership.py .qa-scratch/t36/paths.txt > .qa-scratch/t36/block-2.txt
/usr/bin/grep -E '^(mine:|only-|lines:|fork-own lines:|read lines:)' .qa-scratch/t36/block-2.txt
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683; PIN=16dbac5211eea7e70db7394372033be2be7df829; MB=cada856d86
git -C "$W" ls-tree -r --name-only "$PIN" -- es-core/src/utils/ es-core/src/resources/ es-core/src/renderers/ | /usr/bin/grep -v -E '^es-core/src/utils/AtomicFileUtil\.[^/]*$' | diff - .qa-scratch/t36/paths.txt && echo "ls-tree at the pin = paths.txt"
for p in $(cat .qa-scratch/t36/paths.txt); do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l", s}'
for p in $(cat .qa-scratch/t36/paths.txt); do git -C "$W" show "$PIN:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c", s}'
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t36/paths.txt | wc -l
while IFS= read -r p; do git -C "$W" cat-file -e "bccd715707:$p" 2>/dev/null && echo "IN BASE: $p"; done < .qa-scratch/t36/paths.txt | wc -l
git -C "$W" diff --shortstat "$MB" "$PIN" -- $(cat .qa-scratch/t36/paths.txt)
git -C "$W" diff --shortstat bccd715707 "$PIN" -- $(cat .qa-scratch/t36/paths.txt)
```

Expected, at `2174265e9c` (the first pass, against `/dev/null`, writes `mine:
58 paths.txt: 0 equal: False` into `block-1.txt` with every path under
`only-mine`, R1 C07's last line; the block prints these fourteen lines, R1
C07, § 5):

```
58 .qa-scratch/t36/paths.txt
mine: 58 paths.txt: 58 equal: True
only-mine: []
only-paths.txt: []
lines: 50840 reach: {'shipped': 58} tier: {'upstream-carried': 43, 'fork-own': 15} lang: {'c++': 25, 'c-header': 32, 'c++-header': 1}
fork-own lines: 6212
read lines: 50840
ls-tree at the pin = paths.txt
wc -l 50827
grep -c 50840
52
52
 15 files changed, 1032 insertions(+), 60 deletions(-)
 15 files changed, 1032 insertions(+), 60 deletions(-)
```

The two `52` lines are the paths present at the merge base and at
`bccd715707`: the 58 less the six fork additions (R1 C10, § 5). Then, under
`CLAIMS` (read with `sed -n '/^CLAIMS$/,$p' .qa-scratch/t36/block-2.txt`), the
28 named paths with their claimants (R1 C15): the twelve of this slice `in-T36
non-rest [('es-core-utils-resources', 36)]` (their tiers and lines are the
table's); `utils/AtomicFileUtil.cpp` (829) and `.h` (215), `Settings.cpp`
(723), `SystemConf.cpp` (494), `HttpReq.cpp` (644) and
`es-app/src/ApiSystem.cpp` (3519) `not-in-T36 non-rest [('es-state-and-bridge',
21)]`; `utils/DownloadFile.cpp` `NOT IN INVENTORY`;
`components/TextComponent.cpp` (857) and `components/MenuComponent.cpp` (574)
`[('es-core-components', 34)]`; `ImageIO.cpp`, `Log.cpp`, `Window.cpp` and
`es-core/CMakeLists.txt` `not-in-T36 rest [('es-core-window-input', 35)]`;
`es-app/src/CloudText.cpp` (1409) and `es-app/tests/unit/CMakeLists.txt` (159)
`[('es-cloud-pages', 18)]`; `es-app/src/guis/GuiMenu.cpp` (11747)
`[('es-guimenu', 26)]`; and under `ES-CORE BY SLICE` the four rows of § 1.

**Three things the figures hide, settled here so the lane does not re-derive
them.** (1) **The inventory counts lines as `grep -c ''` does** over the 58
files, the unterminated last line included: **thirteen slice files end
without a newline** -- `renderers/Renderer_GL21.h` 52/53,
`renderers/Renderer_GLES10.h` 52/53, `renderers/Renderer_GLES20.h` 66/67,
`renderers/Shader.cpp` 641/642, `resources/TextureResource.cpp` 347/348,
`utils/ConcurrentVector.h` 91/92, `utils/HtmlColor.cpp` 247/248,
`utils/MathExpr.cpp` 1015/1016, `utils/MathExpr.h` 74/75,
`utils/StringListLock.cpp` 60/61, `utils/VectorEx.h` 169/170, `utils/md5.cpp`
368/369, `utils/md5.h` 94/95 (R1 C09's `<- no trailing newline` rows; `FILES
without trailing newline 13`), **none of them fork-own** (R1 C08) -- so `wc -l`
sums to **50,827** and `grep -c ''` to **50,840** (R1 C09's `TOTAL` lines),
the same bytes, two counting rules; a figure in `02` says which. The order's
*"50,840 read"* is every line: all 58 are `c++`, `c-header` or
`c++-header`, shipped, none vendor-carried (`read lines: 50840`, R1 C07). The
same two rules reach every count in this brief: `git grep -c` counts
**lines** and `git grep -o | wc -l` counts **occurrences**; § 5 states the
line form (`_("` 11 lines, R2 cmd 28; R3 cmd 17), and the occurrence forms are
the lane's first lines -- `MathExpr.cpp:95` carries two strings on one line
(R2 § 7). R3 § 1.1's per-file sizes are `grep -c .`, non-blank lines (its
own note), a third rule; this brief quotes none of them as a slice total.
(2) **"6,212 fork-own" is the lines of the 15 files the fork touched, not
the lines the fork wrote.** The inventory's `tier` is per file, so
`Font.cpp` counts whole (1311) for a 118/47 numstat, `Platform.cpp` whole
(956) for 67/9, `StringUtil.cpp` whole (1706) for 359/0 (R1 C08, C11; R1 § 6
D3); the fork's own change over the 58 is **`15 files changed, 1032
insertions(+), 60 deletions(-)`** (R1 C11 against `cada856d86`; the same line
against `bccd715707`, R1 C07; `--name-status` `6 A` + `9 M`, R1 C11). The
`+/-` split per file by `--numstat` (R1 C11): `resources/Font.cpp` 118/47,
`resources/Font.h` 10/0, `resources/TabStops.h` 49/0,
`resources/TextureData.cpp` 49/1, `utils/CommandLineUtil.h` 104/0,
`utils/OfflineProxyUrl.cpp` 21/0, `utils/OfflineProxyUrl.h` 40/0,
`utils/Platform.cpp` 67/9, `utils/Platform.h` 13/0, `utils/StringUtil.cpp`
359/0, `utils/StringUtil.h` 1/0, `utils/TimeText.cpp` 83/0, `utils/TimeText.h`
57/0, `utils/TimeUtil.cpp` 51/3, `utils/TimeUtil.h` 10/0. So the read's tiers
are **fork-added 6** (`resources/TabStops.h`, `utils/CommandLineUtil.h`,
`utils/OfflineProxyUrl.{cpp,h}`, `utils/TimeText.{cpp,h}`: absent from
`bccd715707`, the merge base, `rocknix/master` and batocera's base), **fork-modified
9** (`resources/Font.{cpp,h}`, `resources/TextureData.cpp`,
`utils/Platform.{cpp,h}`, `utils/StringUtil.{cpp,h}`, `utils/TimeUtil.{cpp,h}`)
and **upstream-carried 43** (R1 C10's `CLASS` lines), and `02` § Coverage
carries both tiers. Unlike T35's 96, no file carries a fork commit while
matching the merge base: the inventory's 15 fork-own and git's 15 changed are
the same set (R1 C19: `in one but not the other: 0`). **The fork lines that
sit inside upstream functions** (the `-U0` hunks against `cada856d86`, proof
C4, CMD5): `Font.cpp:2` (the include) and `buildTextCache`'s
`:1027-1029` and `:1105` (hunks `-913 +1027,3`, `-916,45 +1031,0`, `-1034
+1105`); the `TextureData.cpp` hunks; `Platform.cpp:855` (the masked log
line) and `:343`, `:367` (the two `isLinkInterface` calls inside
`queryIPAddresses`, hunks `-329,3 +343` and `-356,3 +367`); and
`TimeUtil.cpp`'s `toLocalTimeString` rewrite (`-189,3 +190,50`, three
upstream lines replaced); everything else the fork added is new functions
or new files (R2 § 0). The split decides § 1's line between a fork defect
and an upstream one under rule 6. (3)
**The bases** (R1 C01). `rocknix/master` is `f6c542872e` (2026-10-23, *Merge
pull request #54 from porschemad911/s922x-suspend*); the pin's merge base
with it is `cada856d86e3115fbbf0bce09dd761b0ee8fa9fd` (2026-09-23, *Refactor
wifi menu and add support for saving multiple profiles*), and `bccd715707`
(2026-09-22, *Show all ip addresses in network settings*) is its parent and
the base every earlier ES brief named; for this slice the difference is
nothing: the shortstat is the same line against both (above), and
`rev-list --count bccd715707..PIN -- <58>` prints `19`, the same as the log
from the merge base (R1 C12). `batocera/master` is `b2ceb55a7e` (2026-10-21,
*update po*) and its merge base with the pin is
`1750dded8c0fdff70630026f756a69fcad0bb995` (2026-09-13, *update po*), so
ROCKNIX has merged nothing from batocera since then. This paragraph is the one
statement of the bases; § 1's comments, § 5's expectations and § 7's checkbox
cite it.

**Merge debt: none on the 58** -- every one of the 43 upstream-carried files
is byte-identical to `rocknix/master` **and** to the merge base (`Y Y Y Y |
Y Y`, R1 C10; `IDENTICAL to rocknix/master (blob) 43`), and what separates the
pin from `rocknix/master` is the fork's own 15 files reversed (`git diff
--shortstat PIN rocknix/master -- <58>` prints `15 files changed, 60
insertions(+), 1032 deletions(-)`; `--name-status` `6 D` + `9 M`, R1 C11), so
upstream has moved none of the 58 since `cada856d86`: the count of upstream
commits on the 58 since the base is **0** (`git log --format=%h
cada856d86..rocknix/master -- <58> | grep -c .` prints `0`, rc 1), 0 on
`es-core/`, of 14 on any path (R1 C13). The record in `02` § The merge debt is
one line (§ 6), not a table. **The other lanes' pending hunks in this slice's
files are not upstream's debt but a collision list** (§ 1 (b), (d)): T20's
`utils/FileSystemUtil.cpp` (`1 file changed, 4 insertions(+)`), T21's
`utils/FileSystemUtil.cpp` with the two new `utils/DownloadFile.*` (`3 files
changed, 101 insertions(+), 6 deletions(-)` over the 58 and those two), T26's
`utils/Platform.cpp` (`1 file changed, 15 insertions(+), 5 deletions(-)`)
(R1 C17), each named in `02` § The merge debt as its owner's.
**Batocera's thirteen commits on the 58 since `1750dded8c`** (R1 C14: `13`;
35 on `es-core/` as a whole) are **a reconciliation list for the integration,
not this slice's debt**, named in `02` § The merge debt's one line as *not
ROCKNIX's*, never a debt figure and never fetched: `a0f0ea56f` 2026-10-20
*battery: fall back to the power supply type when no name matches*,
`cf64a14a5` 2026-10-18 *[WIN32] Restore screen-sized window position after a
game*, `0d805e9da` 2026-10-11 *fix: fribidi ponctuation for english text*,
`a7dbbea49` 2026-10-09 (merge), `0f9242aee` 2026-10-07 *Update
TextureData.cpp*, `9c48a461b` 2026-10-07 *svg optimization + texturedata
change to never rasterize a svg larger than screen + debug log*, `52e5cdceb`
2026-10-07 *fix fribidi multi lines*, `ab218fba1` 2026-10-02 *load slow menu
option lists in the background and fix asan errors*, `eb512bb01` 2026-09-29
(merge, #2225), `a7573d887` 2026-09-29 *fix ar language name*, `e2f207bf6`
2026-09-30 *improve es 3.x performance further*, `4c210f0a3` 2026-09-28 *fix
ar alignement*, `da80335e4` 2026-09-08 *Renderer: preserve --screensize /
--screenoffset across window size changes*; they touch **nine of the 58** --
`renderers/Renderer.cpp` 72, `renderers/Renderer_GLES30.cpp` 831,
`renderers/Shader.cpp` 26, `renderers/Shader.h` 12, `resources/Font.cpp` 68,
`resources/Font.h` 2, `resources/TextureData.cpp` 27,
`utils/FileSystemUtil.cpp` 2, `utils/Platform.cpp` 14 (the stat's change
columns; `9 files changed, 668 insertions(+), 386 deletions(-)`, R1 C14) --
and the files both batocera and the fork changed are **`Font.cpp`, `Font.h`,
`TextureData.cpp` and `Platform.cpp`** (R1 C19's `comm -12`); `Renderer.cpp`,
`Renderer_GLES30.cpp`, `Shader.cpp`, `Shader.h` and `FileSystemUtil.cpp` are
batocera-only (R1 C19). The first group is where a future rocknix merge of
batocera meets the fork's edits: **batocera's `9c48a461b` and `0f9242aee`
(never rasterize an SVG larger than the screen) against the fork's
`20824cc29` (a shared SVG rasterised at the largest size any consumer asks
for, #181), in the same file** -- read off the subjects only, no hunk read
(R1 C14); the fribidi pair against the fork's tab stops; the battery
fallback against the fork's `Platform.cpp` hunks. The hunk ranges are the
lane's `git diff 1750dded8c batocera/master -- <file>` per file, never a
merge. The pin-to-`batocera/master` distance over the 58 (`20 files changed,
747 insertions(+), 1548 deletions(-)`, R1 C14) mixes batocera's moves with the
fork's and is quoted only as the tool's line.

**The files, read whole** (lines at the pin by `grep -c ''`, the inventory's
rule, R1 C09; the fork's stat column from R1 C11, which equals the base's for
every row; the commits by R1 C12's per-commit file lists; the 15
fork-touched files one row each or one row per pair, the 43
upstream-carried grouped by what they are; a neighbour outside the 58 is
written with its owner the first time it appears; the lines are R2's at the
pin unless the cell names R3 or R4):

| File | Lines | Fork stat | Fork commits R1 C12 attributes | What it is at the pin |
| --- | ---: | ---: | --- | --- |
| `resources/Font.cpp` / `Font.h` | 1311 / 217 | 165 ++--- / 10 + | `7b18c4489` (header lines measured before the bar), `a82dcdf4c` (a later tab stop allows for the columns before it) | the fonts: `#include "resources/TabStops.h"` `:2`; the fork's `TAB_STOP_GAP` and `getTabStops` `:833-885`, `sizeTabbedText` `:887-941` (#160), `buildTextCache` taking its stops from `getTabStops` `:1027-1030` and placing a tab at `offset[0] + stop + gap` `:1105` (#308 F-ES-11); **the scaling**: `Font::get` keys the cache on `(canonical path, size * scale)` `:161-180` and the constructor scales again into `mSize` `:99-101` (0 becomes 2 `:103-104`); **`getFromTheme` `:1231-1256` starts from the already scaled `orig->mSize` when an element sets only `fontPath` (`:1238`, `:1248-1253`) and hands it to `get` `:1255`** (L-07); **the height**: `getHeight()` is `mMaxGlyphHeight * lineSpacing` `:754-757`, `mMaxGlyphHeight` 0 at `:107` **and every ASCII glyph 32..127 rasterised by the constructor at `:115-117`** (*"always initialize ASCII characters"*, `9f040f4c7` 2014-08-11 by `git log -S`, R2 cmd 8), raised only at `:420-421` (L-08); a glyph that fails to load returns NULL `:376-381`, `:385-389`, `:398-402`; **measure and draw**: `sizeText` `:714-752` (the newline glyph's advance added to the next line `:734-745`), the flag glyphs of `substituableChars` `:31` set in `OnThemeChanged` `:1258-1311` and drawn `yBot - 2 * padding` wide `:1044-1078` (L-09); **lifetime**: `sFontMap` of `weak_ptr` `:30`, `:177`, pruned only in `getTotalMemoryUsage` `:77-88`, `addReloadable` `:178`, `unload` `:145-159`, `reload` `:132-143`, `:433-456`, glyph textures up to 2048 wide `:260-261`, **`getGlyph` uploading through `Renderer::updateTexture` `:417` from whatever thread measures** (L-17); `fontoverrides/` PNGs by hex code point `:1287-1310`; `Font.h:10-11` `<ft2build.h>` and `FT_FREETYPE_H`, `Font.cpp:19` `<fribidi.h>` under `HAVE_FRIBIDI` (R3 § 2.2) |
| `resources/TabStops.h` | 49 | 49 + (new) | `a82dcdf4c` | `TabStops::fromColumns` `:26-46`: stop k = previous stop + gap + widest column k; header-only and tested (`TabStopsTests.cpp:6`, R3 § 1.2; `es-app/tests/unit/CMakeLists.txt:33` names it in a comment, R1 C22) |
| `resources/TextureData.cpp` (`.h` upstream, 126) | 739 | 50 ++- | `20824cc29` (a shared SVG is rasterised at the largest size any consumer asks for, #181) | `initSVGFromMemory` records the clamped raster size `:194-195`; `setMaxSize` before load keeps the larger box per axis for an SVG `:621-634` (writes `:630`, `:632`); `rasterizeAt` grows `mMaxSize` to the request `:687-707` (write `:705`); **`mMutex` (`TextureData.h:103`) is taken by `initSVGFromMemory` `:95`, `initFromRGBA` `:254`, `updateFromExternalRGBA` `:284`, `isLoaded` `:541`, `uploadAndBind` `:551`, `releaseVRAM` `:594`, `releaseRAM` `:607` -- not by `setMaxSize` `:615-645` or `rasterizeAt` `:670-725`** (L-10); **the cached `exists(localFile)` at `:331`, `:339`, `:410`** (#1263's half, ruling (i); R4 item 1); `toLower` on extensions `:460`, `:504`; `<vlc/vlc.h>` `:12` with **no guard**, `libvlc_instance_t`, `libvlc_media_t`, `libvlc_media_player_t` `:343-345`; `<nanosvg/nanosvg.h>`, `<nanosvg/nanosvgrast.h>` `:8-9` resolved in the tree (`external/nanosvg` a tree, R3 § 2.2) |
| `utils/CommandLineUtil.h` | 104 | 104 + (new) | `2f5fd6332` (a core is swapped only in the command's own word, not the ROM's) | `wordEnd` `:19-48`, `replaceOptionValue` `:60-100` (#308 F-CS-33), `value` inserted unquoted `:95`, `:98` (its callers pass a core name); header-only and tested (`CommandLineTests.cpp:7`, `LaunchCommandTests.cpp:10`, R3 § 1.2) |
| `utils/OfflineProxyUrl.cpp` / `.h` | 21 / 40 | 21 + / 40 + (new) | `0ec3f43ae` (an image asked of the offline proxy asks for its store only, fork #199) | `Base`, the loopback proxy address `.h:22`; `StoreOnlyHeader` `.h:29`, `const char* const StoreOnlyHeader = "X-RA-Store-Only: 1";` under `:27-28`'s *"As HttpReqOptions::customHeaders takes it, name and value in one line."* -- a fixed header line, its value `1` (proof C5, CMD5, CMD7); `isProxyUrl` `.cpp:6-21` (case-insensitive prefix, then end, `/`, `?` or `#`), which rejects a host that merely begins with the base `.h:31-37`; compiled by `es-unit-tests` (`CMakeLists.txt:64`), four cases in `OfflineProxyUrlTests.cpp` (R4 item 35); included by `WebImageComponent.cpp:7` (T34's) |
| `utils/Platform.cpp` / `.h` | 956 / 100 | 76 ++- / 13 + | `4e34bc2d1` (multi-line command output), `80f52e500` (a credential's value never reaches the log, #177), `0cc13be61` (a link is not a tunnel, #279, #280) | **`ProcessStartInfo`**: both constructors default `waitForExit` to true `:40`, `:52`; `run` `:60-194` wraps the command as `((((<cmd> 2> <log>/es_launch_stderr.log ; echo $? >&3) \| head -300 > <log>/es_launch_stdout.log) 3>&1) \| (read xs; exit $xs))` `:162` (`/dev/null` for both when the log is off `:163-164`), then `system()` and `WEXITSTATUS` `:166-168`, or without waiting a double fork and `execl("/bin/sh", "sh", "-c", ...)` returning 0 `:172-192` (L-05); **`runSystemCommand` `:853-880`**: the log line through `maskSecrets` `:855` (the fork's), a double fork, `execl("/usr/bin/sh", "sh", "-c", cmd)` `:864`, waits `:868`, `:876`, **returns 0 always `:879`**, `name` and `window` unused (L-13); **`GetShOutput` `:891-905`** (unchecked `popen` `:894`, `fgets` `:897`, `substr(0, size - 1)` `:900`; L-06) and the fork's **`GetShOutputLines` `:907-935`**; **quit**: `quitES` fires `quit` and pushes a heap `SDL_Event` never freed `:235-237` (L-18), `processQuitMode` touches `/tmp/restart.please`, `/tmp/reboot.please` or `/tmp/shutdown.please` `:241-250`, `:263-274`, `system("shutdown ...")` `:196-211`; the fork's `isLinkInterface` `:285-297` used by `queryIPAddresses` `:299-378` (`:343`, `:367`) and the new `queryInterfaceAddresses` `:380-398`; all 16 spawn lines of the slice are here (R2 cmd 17, § 5); `<SDL_events.h>` `:3`, `<ifaddrs.h>`, `<net/if.h>`, `<netinet/in.h>`, `<arpa/inet.h>` `:11-15` (R3 § 2.2); **`Platform.h` is SDL-free and `Platform.cpp` is not** (`Window.h`, `Scripting.h`, `renderers/Renderer.h`, R3 § 2.4); D-INFRA-011's text names `Platform.cpp:830` (R5 § G), the row's line at its date -- the masked log line at the pin is `:855` |
| `utils/StringUtil.cpp` / `.h` | 1706 / 96 | 359 + / 1 + | `80f52e500` (#177), `217872e32` (#258's comments), `dcf7fa8c7`, `b036967fc`, `3157d1a69`, `107597312`, `893a81403` (the masking rounds, #308 F-ES-09, PL-010, G2-E-core-01, G3-E-01) | **`maskSecrets`**, the hunk `@@ -443,6 +443,365 @@` (added lines `:446-804`): a key or flag kept and its value replaced by `<redacted>`, a value one shell word across quotes and escapes, `setrootpass` masking the rest of the line, `wifictl connect/enable` the second word, a flag or `name=` ending in a credential word, `?y=`/`&t=`/`&p=`; its name list `:513`, the `wifictl` rule `:764-784`, `--key` absent on purpose (#177; R4 item 25) (L-14); **the case helpers**: `toLower` `:329-368`, `toUpper` `:370-408`, ASCII in place, else `chars2Unicode` `:202` and a `bsearch` over two parallel tables (`tolowerUnicode` `:184-191`, `toupperUnicode` `:193-200`); **the 2-byte branch assigns (`:354-355`, `:395-396`), the 3-byte branch adds (`text[pos] += ...` `:359-361`, `:400-402`)**, the tables carrying 3-byte pairs (`0x1EA1` `:76`, `0x1EA0` `:153`, `0xFF41` `:93`, `0xFF21` `:170`, R2 cmd 16) (L-01); **`shellQuote` `:426-444`**, the fix shape of four lanes (R4 item 24); compiled by `es-unit-tests` (`:62`) and three `tests/app-unit/` targets (`:55`, `:77`, `:97`, R1 C22); `StringUtil.cpp:1406-1407` two trailing comments carrying Hangul after code, `StringUtil.h:62-68` Hangul string literals (R3 § 5) |
| `utils/TimeText.cpp` / `.h` | 83 / 57 | 83 + / 57 + (new) | `8b7340f5b` (#195, D-UI-058), `5067f7a1b` (D-UI-087), `296aa5966` (D-UI-089) | `clockText`, `dayRelation`, `whenText`, `shortYear` -- pure, not read line by line by R2 (R2 § 0); compiled by `es-unit-tests` (`:63`), `TimeTextTests.cpp:12` (R3 § 1.2) |
| `utils/TimeUtil.cpp` / `.h` | 634 / 99 | 54 ++- / 10 + | the same three | the fork's two hunks by `-U0` (proof C11, CMD5; numstat `51 3`): `-1,0 +2`, a line-2 addition, and `-189,3 +190,50`, the rewrite in which `toLocalTimeString` = the locale's `%x` + `localClockText` (the 12-hour switch read per call, `strftime` lengths taken from the return); new `localClockText`, `toShortLocalDateString`, `toRelativeLocalTimeString`; **ten of the slice's eleven `_("` lines**, upstream's: `:517` and `:588` (`never`), `:544` (`%d d`), `:548`, `:569` (`%d h`), `:552`, `:560`, `:573`, `:578` (`%d mn`), `:580` (`%d sec`) (R2 § 7); `<langinfo.h>` `:10` under `__linux__` (R3 § 2.2) |
| the file helpers: `utils/FileSystemUtil.cpp` / `.h` | 1805 / 103 | -- | -- | **no fork hunk** (R2 § 1.3); **the cache** `:48-341`: an `unordered_map<size_t, FileCache>` under a `shared_mutex` `:331-332`; reads through `queryCacheEntry` `:200-216` only while `Settings::UseFileCache()` `:203`; **a miss is stat'ed and stored** `:213-215` (via `insertEntry` `:313-324`); **a cached directory listing (`path + "/*"`, added at `:364`, `:479`) makes every path under it with no entry read as absent without a stat** (`getCacheEntry` `:277-282`); **`exists(path, false)` `:1122-1147` stats through `fromStat64`, whose Linux branch writes the entry unconditionally `:161-162`**; invalidation (`remove` `:183-198`, the entry and every ancestor's `/*`) called only by this file's writers -- `removeDirectory` `:1051`, `removeFile` `:1067`, `createDirectory` `:1097`, `writeAllText` `:1445`, `renameFile` `:1457-1458`, `copyFile` `:1506-1507`; the only full reset `FileSystemCache::reset` `:343-346`; **the reads**: `skipUtf8Bom` `:1369-1379`, `readAllBytes` `:1381-1398` (no BOM skip), `readAllLines` `:1400-1416`, `readAllText` `:1418-1427` (L-02); **the writers**: `writeAllText` `:1429-1446` (`fopen(..., "wb")` `:1434`, `fwrite`/`fclose` unchecked `:1442-1443`, `void`), `renameFile` `:1448-1465` (`true` on an absent source `:1451-1452`; `overWrite`, the default at `FileSystemUtil.h:74`, removes the destination first `:1454-1455`; `std::rename` `:1463`), `copyFile` `:1467-1510` (`true` on an absent source `:1472-1474`; truncation `:1492`; `fwrite`/`fclose` unchecked `:1500-1504`), `createDirectory` `:1089-1120` (EEXIST from a concurrent creator at `:1116`) (L-03, L-04, L-16); **`preloadFileSystemCache` `:1758-1798`**: a function-static `std::set` `:1766` unlocked `:1768-1771`, a `[&]` lambda `:1773` reading the parameter `trySaveStates` `:1775` on a detached thread `:1788`, `:1797` (L-15); `getCanonicalPath`'s fold `:726` (T2's line, not re-read, R4 item 16), the relative path by prefix `:986` (R4 item 17), `getEscapedPath` (R4 item 15, lines the lane's); three em-dash comment lines `:225`, `:287`, `:718` (R3 § 5); 14 lock lines by § 5's pattern (proof C2, CMD4, CMD6; R2 cmd 17 printed 13) |
| the texture cache and the resources: `resources/TextureResource.cpp` / `.h`; `resources/TextureDataManager.cpp` / `.h`; `resources/ResourceManager.cpp` / `.h` | 348 / 74; 381 / 108; 258 / 64 | -- | -- | **`TextureResource::get` `:100-165`**: the key at `:100` = `(canonicalPath, tile, linear, shareId)` (R4 item 2), a static map of `weak_ptr` `:12`, `:146` with no lock, and with `OptimizeVRAM` and a max size a shared, loaded texture whose size is no longer valid **released and reloaded synchronously on the caller's thread** `:110-127` (T26 L-02 / #1221 and T32 PL-07 / #1263 carry `:100-131`); **`TextureDataManager`**: an MRU list plus lookup under a `recursive_mutex` `:21-100` (`.h:100`), `cleanupVRAM` `:135-194` releasing reloadable, non-required, loaded textures until under `MaxVRAM` MiB `:139-163` and on 32-bit a 250 MiB RAM cap `:166-193`; **`TextureLoader`**: `hardware_concurrency() / 2` threads, at least 2 `:215-223`, each waiting on `!paused && (mExit \|\| !queue.empty())` `:252-253` and loading outside the lock `:269-274`; **the destructor clears the queue, sets the atomic `mExit` and `notify_all`s without holding `mLoaderLock` `:231-232`, then joins `:234-235`**; `paused` a static atomic `:284` (`.h:34`) set by `es-app/src/views/SystemView.cpp:198` (T32's) and cleared at `:226` with no notify (L-11); `ResourceManager`: `weak_ptr` lines `:229`, `:238` (`.h:34-35`, `:56`), not read further (R2 § 2.3); `MaxVRAM` 128/256/384/512 by total RAM is `Settings.cpp:233-246`, T21's (R3 § 4) |
| the renderers: `renderers/GlExtensions.cpp` / `.h`; `Renderer.cpp` / `.h`; `Renderer_GL21.cpp` / `.h`; `Renderer_GLES10.cpp` / `.h`; `Renderer_GLES20.cpp` / `.h`; `Renderer_GLES30.cpp` / `.h`; `Shader.cpp` / `.h` | 140 / 88; 1170 / 263; 459 / 53; 422 / 53; 1420 / 67; 2291 / 69; 642 / 146 | -- | -- | **no fork hunk in any of the 14** (R1 C08, C11); a GL context per renderer (`Renderer_GL21.cpp:106-107`, `Renderer_GLES10.cpp:102-103`, `Renderer_GLES20.cpp:558-577` with two fallbacks, `Renderer_GLES30.cpp:1197-1237` checking `SDL_GL_MakeCurrent`); the clip stack a file-static `std::stack<Rect>` `Renderer.cpp:31-32`, `pushClipRect` `:520-566`, `popClipRect` logging an underflow `:568-594`; `glScissor` flipped per backend; only GLES20 checks a texture create `:724-728`; **no thread check anywhere in `renderers/`** (R2 § 3); **the selection** (R3 § 2.2): `-DGLES3=1` on every device (`package.mk:25`) -> `add_definitions(-DUSE_OPENGLES_30)` (`CMakeLists.txt:361-367`); `es-core/CMakeLists.txt:278-284` appends `Renderer_GLES30.cpp` (else `Renderer_GLES20.cpp`); `Renderer_GL21.cpp` and `Renderer_GLES10.cpp` are in the unconditional list (`:244-245`) with bodies under `RENDERER_OPENGL_21` / `RENDERER_OPENGLES_10` (`Renderer_GL21.h:6-8`, `Renderer_GLES10.h:6-8`); `RENDERER_GLES_30` from `USE_OPENGLES_30` (`Renderer_GLES30.h:5-7`); `Renderer.cpp:823-872` is the selection chain, `:823` `#if defined(RENDERER_GLES_30)` to `:872` the GL21 branch's `OpenGL21Renderer rd;`, the `GLES30Renderer` instantiated inside it (proof K-077); `Renderer.h` branches on `USE_OPENGLES_30` at `:99`, `:128`, `:208`; `GlExtensions.h:6` `<GLES3/gl3.h>` under `USE_OPENGLES_30`, `:8` `<SDL_opengles2.h>`, `:10-11` the desktop branch; `ScreenSettings::fontScale()` `Renderer.cpp:1149` |
| the rest of `utils/`: `ThreadPool.cpp` / `.h`; `ZipFile.cpp` / `.h`; `zip_file.hpp`; `MathExpr.cpp` / `.h`; `md5.cpp` / `.h`; `HtmlColor.cpp` / `.h`; `Randomizer.cpp` / `.h`; `StringListLock.cpp` / `.h`; `ConcurrentVector.h`; `VectorEx.h`; `Uri.h`; `Delegate.h`; `han.h` | 230 / 77; 369 / 51; 10011; 1016 / 75; 369 / 95; 248 / 18; 53 / 19; 61 / 30; 92; 170; 144; 27; 20923 | -- | -- | `ThreadPool` threads `:26` (count `hardware_concurrency() * mThreadByCore`, or `abs()` of a negative), `:84` (start), `:91` (join), not read further; `MathExpr.cpp:61` (the theme `upper()`), `:73-80` (list compare) the only callers of `toUpper` in the 58, `:95` `_("Unknown")` and `_("None")` on one line; `zip_file.hpp`'s six write-shaped lines (`fopen\(\|ofstream`) and three `<utime.h>` (`:4536`, `:4551`, `:4568`) not read; #256's body: *"a vendored header (backup archives) -- its own PR"* (R4 item 27); `md5.cpp` is not #585's MD5 line, which is `libretro-common`'s (R4 item 40); the rest **not opened by R2** (its header names each) -- the lane reads them for the lens, `han.h` and `zip_file.hpp` by cited range only (§ 1 Depth) |

**The 19 fork commits on the 58** (`git log --oneline cada856d86..PIN --
<58>` ends at 19, `count (wc -l): 19`; `rev-list --count bccd715707..PIN --
<58>` 19; two merges among them, `370ebe416` of `rocknix/master` and
`2dae87308` of `feature/es-logging-rc11`, which history simplification keeps
because their results differ from a parent on these paths; R1 C12), the
newest `893a81403` 2026-09-29 *StringUtil: the second single-quote splice
keeps the masked value whole*, the oldest `4e34bc2d1` 2026-08-29 *Cloud: read
multi-line command output without losing the lines*; every non-merge line of
R1 C12's listing names `Max Engel`. The table's column names the rest by
subject. The lane's `02` § Coverage quotes the subjects from its own `git
log`, never from here.

**What the research checked and found sound, beyond what the table and § 5
carry, so the lane confirms rather than hunts:** the 43 upstream-carried files
are byte-identical to `rocknix/master` and to the merge base (R1 C10); the
inventory's set equals the pin's tree through the globs (R1 C07); the fork's
**`GetShOutputLines`** (`Platform.cpp:907-935`) null-checks `popen` and keeps
long lines whole; **`isLinkInterface`** (`:285-297`) keeps a tunnel's fixed
address out of "is the device connected"; **`TabStops::fromColumns`** and
**`CommandLineUtil`** are header-only and already tested; **`isProxyUrl`**
rejects a host that merely begins with the base (`OfflineProxyUrl.h:31-37`)
(R2 § 8's positives); `maskSecrets` keeps quotes and escapes whole, reads a
value inside an `sh -c '...'` string as the inner shell would, leaves `<...>`
placeholders, and a second pass is a no-op (R2 § 1.1); the three sources
`es-unit-tests` compiles pass there -- `RUN es-unit-tests: rc 0; [doctest]
test cases: 185 | 185 passed | 0 failed | 0 skipped ...` in T34's
`stage-d/build-tests.txt:55` and in T35's `stage-c/build-tests.out:55` (the
line's tail abridged here; R3 § 1.2, cmds 14, 20; proof C8, CMD15).

**What they found instead -- the leads, one line each.** § 4 carries each
lead's disposition and the question it serves, citing this table rather than
restating its lines; the lines are the pin's, read by R2 on 2026-10-31 (`git
-C <qa-integration> show 16dbac5211:<file>`, R2 cmds 3-20, 28-29) and by R4
from the lanes' records; nothing here was tested, and a lead is a fact of the
lines until the lane's proof says more. **`proved:`** is R2 § 8's column.

| Lead | Lines at the pin | Shape | Q |
| --- | --- | --- | --- |
| L-01 | `utils/StringUtil.cpp:357-362`, `:398-403` against `:352-356`, `:393-397`; tables `:76`, `:93`, `:153`, `:170`; lookup `:184-200` | `toLower`/`toUpper` corrupt any 3-byte character with a case pair: the 3-byte branch adds (`+=`) where the 2-byte branch assigns, so `toUpper` of U+1EA1 (`E1 BA A1`) leaves `C2 74 41`, an invalid lead byte then `tA`; neither branch handles a pair whose code points encode at different lengths (whether the tables hold one was not checked); French accents are 2-byte (unaffected), Vietnamese (U+1Exx) and full-width Latin are not; `proved:` by reading and hand arithmetic, not run | Q6 |
| L-02 | `utils/FileSystemUtil.cpp:1369-1379`, `:1400-1427` | a one- or two-byte file reads as `""` and as no lines: `file.read(bom, 3)` fails and `seekg(0)` does not clear `failbit` (`es-code-traps.md:212`, #245) -- recorded as a trap and **unfixed at the pin**; T20's `d9afa5c7c` fixes it on T20's branch (#1177; ruling (d)); `proved:` by reading and the trap's own record | Q5 |
| L-03 | `utils/FileSystemUtil.cpp:1451-1452`, `:1454-1455`, `:1463`; `:1472-1474`, `:1492`, `:1500-1504` | **`renameFile` and `copyFile` return `true` over an absent source; `copyFile` returns `true` over a short write; `renameFile(..., overWrite)` deletes the destination before an atomic rename, and `overWrite = false` does not protect on POSIX**; the callers that branch on the return: `HttpReq.cpp:479` then `:505-506` (`REQ_SUCCESS`, T21's) with `copyFile` as the fallback `:501-502`, `es-app/src/scrapers/Scraper.cpp:672`, `es-app/src/SaveState.cpp:154-155` (the new slot's MD5 after a `copyFile` that may have copied nothing), `es-app/src/guis/GuiMetaDataEd.cpp:483`, `es-app/src/Win32ApiSystem.cpp:745`, `:877` (R2 cmd 14); T21's `f7c16144d` fixes `renameFile` on T21's branch (#1191; ruling (d)), `copyFile` is not named by any lane (R4 items 13, 14); `proved:` by reading, the consequences unproved | Q5 |
| L-04 | `utils/FileSystemUtil.cpp:1429-1446`; `es-app/src/ThreadedCloudSync.cpp:943-948` (T18's) | **`writeAllText` cannot report a failure** (`void`, `fopen "wb"`, `fwrite` and `fclose` unchecked): **T21 PL-20 / Backlog #1186** (OPEN; `docs/reviews/briefs/es-app-system.md:654`), whose ruling moves the call sites, not the function (R4 item 14); the cloud stamp's temp-and-rename at `ThreadedCloudSync.cpp:943-948` publishes a short write over the last good stamp (D-CLOUD-078, `decision-register.md:144`); 25 call sites (R2 cmd 13: 27 lines less the definition and declaration); `proved:` by reading | Q5 |
| L-05 | `utils/Platform.cpp:40`, `:52`, `:162-168` | **`run()` pipes the command's stdout through `head -300`**: once the command's output outruns the pipe buffer, `head` exits after 300 lines and the command's next write raises SIGPIPE (status 141 read back unless the command ignores SIGPIPE) -- **a short output is held whole and exits 0**: the literal with `seq 1 400` (1,492 bytes) printed `rc=0` on the host's `/usr/bin/dash`, and with `seq 1 200000` printed `rc=141` (proof C1, CMD4, CMD12; R2's 141 was reasoned, `R2-code-read.md:93`, never run), timing-dependent in principle, one run one observation; `waitForExit` true at the launch (`es-app/src/FileData.cpp:1100-1103`), `es-app/src/main.cpp:540`, `InputManager.cpp:1272`, `Scripting.cpp:133`, `:142` (quit only), false at `Scripting.cpp:45`; the log path concatenated unquoted, `2>` binding only the last simple command of a compound `<cmd>`, the two log files overwritten by every run; **the launch wrapper, read from the source** (`projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh` at `e52274caf9`, proof C15, CMD8): `:40` `LOG_FILE="exec.log"`, the emulator run with its output appended to the log (`:491` `"${ROMNAME}" &>>${OUTPUT_LOG}`, `:500` `eval ${RUNTHIS} &>>${OUTPUT_LOG}`), and the script's own log lines sent to stdout as well (`:84` `... 2>&1 \| tee -a ${LOG_DIRECTORY}/${LOG_FILE}`) -- so the emulator's output does not reach `run()`'s pipe and the wrapper's `tee`'d log lines do; that ES's launch command is this script is **not** traced (`[unverified]`: no `es_systems` line in the recipes the proof searched, CMD13, CMD17 -- the lane's trace of the command `FileData.cpp:1100-1103` builds); `proved:` the literal's shell behaviour is a stage-A run (§ 5), the wrapper's redirects `tree`, G-07 the image's copy | Q4 |
| L-06 | `utils/Platform.cpp:891-905` | `GetShOutput`: `popen` unchecked `:894`; each 256-byte `fgets` chunk loses its last byte `:900`, so a line of 256 bytes or more loses bytes mid-line, a final line without a newline loses its last character, and lines are joined with no separator; 25 call sites in `es-app` (R2 cmd 13), the cloud ones `GuiMenu.cpp:5579`, `:5589`, `:6639`, `:6749`, `:7060`, `:7407`, `:7995`, `:8445` (T26's); **T26's S8 fixes it on T26's branch** (#1225; ruling (d)); `proved:` by reading and hand arithmetic | Q4 |
| L-07 | `resources/Font.cpp:1238`, `:1255`, `:165-166`, `:99-101` | `getFromTheme` re-scales an already scaled size when a theme element sets `fontPath` without `fontSize` -- the double scale `es-code-traps.md:109` warns about for `getSize()`, inside `Font.cpp` itself; whether the shipped theme has such an element was not checked; `proved:` by reading | Q2 |
| L-08 | `resources/Font.cpp:107`, `:115-117`, `:420-421`; `es-code-traps.md:118`; T34 L-02 (`es-core-components.md:597`) | **a rule erratum, not a code defect:** the constructor rasterises ASCII 32..127, and only ASCII raises `mMaxGlyphHeight`, so `getHeight()` is fixed after construction unless a glyph failed to load -- against `es-code-traps.md:118`'s *"the tallest glyph rasterised so far ... Measured before a label has drawn, it under-reports"*, against T34's L-02 premise (*"0 at construction"*) and against T34 PL-17 deferred as an open item to test on the same premise (R4 item 4); `proved:` by reading, `git log -S` dating the preload to 2014 | Q2 |
| L-09 | `resources/Font.cpp:728-731`, `:734-745`; the fork's `getTabStops`/`sizeTabbedText` `:833-941`; `:1044-1078` | the measured width of a substituted flag glyph exceeds the drawn width by `yTop/2`, and counts `lineHeight` when the image is missing; `sizeText` adds the newline glyph's advance; `proved:` by reading | Q2 |
| L-10 | `resources/TextureData.cpp:615-645`, `:670-725` against `:92-195` (`:95` the lock) | the fork's #181 size bookkeeping is read and written without `mMutex` while a loader thread writes the same fields under it (`:142-143`, the fork's `:194-195`); `proved:` by reading | Q2 |
| L-11 | `resources/TextureDataManager.cpp:231-235`, `:252-253`, `:284`; `es-app/src/views/SystemView.cpp:198`, `:226` (T32's) | `notify_all` without the lock (a lost wakeup at teardown); `paused` true at teardown keeps every loader asleep and the join waits forever; clearing `paused` notifies nobody; `proved:` by reading, frequency unproved | Q2 |
| L-12 | `utils/FileSystemUtil.cpp:277-282`, `:161-162`, `:183-198` | the directory-listing wildcard answers "absent" for files written after the listing by anything but this file's writers -- the cache's contract, asked by five lanes (R4 items 6-11); `exists(p, false)` refreshes the entry; `proved:` by reading | Q1 |
| L-13 | `utils/Platform.cpp:853-880` | **`runSystemCommand` returns 0 always, blocks the caller for the command's whole run and ignores `window`**; 78 call sites, none reading the return (R2 cmd 13, cmd 14: 80 lines = 78 sites + definition + declaration); **a rule erratum:** `es-native-ui.md:103` (§ Core patterns, the drafter's `grep -n` at `153ca325b3`) says *"passing `window` shows a splash while it runs"*, and at the pin nothing does (R2 § 1.2); #1220 (T26: process starts on the interface thread) is the context (R4 item 22); `proved:` by reading | Q4 |
| L-14 | `utils/StringUtil.cpp:446-804` (the `=` test inside `maskSecrets`) | a name is a credential only when the next byte is `=`, so `name: value`, a JSON `"name":"<v>"` and an HTTP `Authorization: Bearer <v>` header pass unmasked; it over-masks any word ending in a credential word (the safe direction); whether any logged line carries those shapes was not checked; the 2026-09-24 audit's gap *"a negative over the"* sweep (R4 item 25); `proved:` by reading | Q4 |
| L-15 | `utils/FileSystemUtil.cpp:1766-1797` | **`preloadFileSystemCache`: a `[&]` lambda on a detached thread reads the parameter `trySaveStates` of a function that has returned** (a dead stack slot), and the static `preloaded` set is unlocked; its callers not counted; `proved:` by reading | Q1 |
| L-16 | `utils/FileSystemUtil.cpp:1089-1120` | `createDirectory` returns `false` when a concurrent creator wins (`mkdir` EEXIST at `:1116`) for a directory that exists; `proved:` by reading | Q5 |
| L-17 | `resources/Font.cpp:30-31`, `:177`, `:417`; `resources/TextureResource.cpp:12`, `:146`; `renderers/` | static caches without locks (`Font::sFontMap`, `substituableChars`, `TextureResource::sTextureMap`, the renderer's clip stacks, R2 § 4), and `getGlyph` uploading to GL from whatever thread measures text; a question first: which threads call `Font::get`, `sizeText` or `TextureResource::get`; `proved:` unproved | Q2, Q6 |
| L-18 | `utils/Platform.cpp:235-237` | `quitES` leaks one heap `SDL_Event` per quit (`SDL_PushEvent` copies); `proved:` by reading, trivial | Q4 |

**The neighbours, and whose they are** (R1 C15; R2 § 6): `utils/AtomicFileUtil.{cpp,h}`,
`Settings`, `SystemConf`, `HttpReq` (`HttpReq.cpp:479`, `:505-506` the
`renameFile`/`copyFile` callers) and `es-app/src/ApiSystem.cpp` are
**T21's** (#668); `es-core/src/components/**` (`TextComponent.cpp`,
`MenuComponent.cpp`, `WebImageComponent.cpp:7`, `:190` the cached `exists`
before an `HttpReq` write) is **T34's** (#681); the rest of `es-core` --
`Window.cpp`, `Log.cpp` (the logger is there, not in `utils/`, R2 header),
`ImageIO.cpp`, `InputManager.cpp`, `Scripting.cpp`, `es-core/CMakeLists.txt`
(the `OfflineProxyUrl`, `TimeText` and `AtomicFileUtil` registrations) -- is
**T35's** (#682, `rest`); `es-app/src/CloudText.cpp` and
`es-app/tests/unit/CMakeLists.txt` are **T18's** (#665); `GuiMenu.cpp`
(the `GetShOutput` callers, the `shellQuote` callers `:3272`, `:6537`,
`:8421`) **T26's** (#673); `SystemView.cpp` (the loader's `paused`) T32's
(#679); `FileData.cpp` (the launch's `run()`) T2's (#649); the es-app
includers of the slice's headers are the es-app slices', not resolved file
by file by R2 (R2 § 6). **The include reach** (`git grep -l -F
'"<dir>/<header>"' -- es-app/src es-core/src`, R2 cmd 21, `all` with the 58
themselves / es-app): `utils/StringUtil.h` 112 / 59, `utils/FileSystemUtil.h`
68 / 39, `renderers/Renderer.h` 36 / 5, `utils/Platform.h` 33 / 15,
`resources/Font.h` 17 / 3, `utils/TimeUtil.h` 17 / 13,
`resources/ResourceManager.h` 16 / 2, `resources/TextureResource.h` 16 / 0;
the six `Renderer_*.h`, `GlExtensions.h`, `Shader.h`, `han.h` and
`zip_file.hpp` 0 by that pattern (reached by relative or angle includes it
does not match).

**Already found; do not re-find; take up.** Each is cited at its lines in
`02` with a disposition; the states are as R4 read them on 2026-10-31 (R4 §
4: the per-term union over the open issues printed `union count: 55`),
re-read at stage A; **asks** is R4 § 1's column -- *read* (state and keep the
invariant in `02`), *rule 6* (a contained fix put to the stage-D pause),
*pause* (a question for the pause, never the lane's ruling), *collision*
(another lane's fix already in this slice's file, ruling (d)); a ruling the
table names by letter is § 1's. The audit folders are § 3 item 8's.

| Found by | Lines at the pin | Take up as |
| --- | --- | --- |
| T32 PL-07 / **#1263** (OPEN, `bug`; T32 `02-forward-audit.md:362`, `05-punch-list.md:474`, `00-running-log.md:141`, retro `docs/retros/2026-10-27-m6-es-app-views-scrapers.md:59`, `:82`; T34's brief `:110-113`, `:666`; T34 `02:356`; #1263 body `:24`) | `TextureData.cpp:331`, `:339`, `:410` | **read** then **rule 6**: the three cached reads' answer against a file rewritten under the same path; #1263 keeps its picture checkbox open for this slice's record -- ruling (i), Q2 (R4 item 1) |
| T34's inherit item 9, *"The texture-cache contract, for T36"* (T34 `02:579`, `02:345-362`, `04:95`; T34's brief `:1045-1049`, `:1355`) | `TextureResource.cpp:100-131` (the key at `:100`) | **read**: from the cache's side, when a key is dropped and whether a rewrite on disk is ever seen while a texture lives under the key; the caller's half is written in T34's `02` -- Q2 (R4 item 2) |
| **#1221** (T26 L-02; OPEN, `bug`; *"fixed on T26's branch `aca4076c5`"*, T34's brief `:668`; T26 `03-retrospective.md:46`) | the same | **read**: the fix is the caller's (a session-named path, `exists(qrPath, false)`); cited beside the row above -- Q2 (R4 item 3) |
| T34 L-02 / PL-17 (T34 `02:103`, `:180`, `:186`; `05-punch-list.md:173`, `:458`: *"Deferred: an open item to test (the moving font height; `Font.cpp` is #683's)"*); `es-code-traps.md:118`; D-UI-050 (`:246`) | `Font.cpp:107`, `:115-117`, `:420-421`, `:754-757` | **read** first -- L-08: the premise is contradicted at the pin -- then **pause**: the rule sentence's correction is the coordinator's sweep, and whether PL-17's open item closes on this slice's positive case (3.10) -- Q2 (R4 item 4) |
| `es-code-traps.md:109` | `Font.cpp:99-101`, `:161-180` | **read**: state the scaling contract; L-07's double scale sits inside it -- Q2 (R4 item 5) |
| T35 L-07 / 3.11 / PL-04 (T35 `02:122`, `:241`, `:796`; `05-punch-list.md:41-42`; `00-running-log.md:49`, `:69`; `04-analysis.md:162`, *"worth a sentence when the fix lands"*; T35's brief `:1104-1110`, `:1458`) | `FileSystemUtil.cpp:48-341`, `:1122-1147`, `:161-162` | **read**: the cache's answer stated in `02` § The file cache; T35's fix is at its callers (`exists(path, false)` at `InputManager.cpp:893`, `:1187`, `:1250`); **ruling (h)**: T36 owns the cache's fix, T35 the case -- Q1 (R4 item 6) |
| T34 L-09 (T34 `02:110`, `04:95`; T34's brief `:604`, `:631`) | `HttpReq.cpp:344`, `:479` (T21's) through `FileSystemUtil.cpp:1457-1458`; `WebImageComponent.cpp:190` (T34's) | **read**: cite T34's answer, *"sound at the pin"*, in the writers table -- Q1 (R4 item 7) |
| T32 `04-analysis.md:138`; `es-app-views-scrapers.md:793-797`, `:1393`; `es-app-system.md:966-971`; #1263 body `:24` | the erasing writers `:1051`, `:1067`, `:1097`, `:1445`, `:1457-1458`, `:1506-1507` | **read**: one table of every writer and whether it erases; a stale answer then needs a writer outside the process -- Q1 (R4 item 8) |
| T33 L-05 (T33 `02:103`; `05-punch-list.md:127`; #1275 body `:18`; `es-app-system.md:575`, `:610`) | `FileSystemCache::reset` `:343-346` | **read**: the reset's callers and when it runs -- Q1 (R4 item 9) |
| **#1271** (OPEN, `bug`; T33 `stage-d/bugs/PL-01.md:36`, #1271 body `:38`, *"What reading cannot prove ... T21's file"*); T26's brief `es-guimenu.md:187-190` | `isRegularFile` (the sources cite `:238-240`, `:1164-1167`, `:138-148`) | **read**: does `isRegularFile` share `exists`'s entry and remember a miss -- answered from the source; #1271's "cannot prove" line is the question (ruling (c) for "T21's file") -- Q1 (R4 item 10) |
| Five line sets for one cache: T34's brief (`:144`, `:185-195`, `:203-220`), T35 (`:296`, `:323`, `:1127-1131`, `:161-162`), T33 (`:345`, `:348-350`, `:238-240`), T26 (`:138-148`, `:1164-1167`), T32 (the writers) | R2's reading at the pin: `remove` `:183-198`, `queryCacheEntry` `:200-216`, the miss stored `:213-215`, `insertEntry` `:313-324`, `reset` `:343-346` | **read**: **one reconciled table at the pin's lines**, every earlier set mapped onto it (R4's command 20 confirmed only `:144`, `:161-162`, `:185-195`, `:203-220` inside the cache struct) -- Q1, Q7 (R4 item 11) |
| **#1177** / T20 PL-09 (OPEN, `bug`, its checkbox `:21` ticked; `t20-streams.md:244-260` (S8); T20 `02:274` (commit `d9afa5c7c`), `:337` (the #585 line, batocera); T20 `03-retrospective.md:23`; `es-code-traps.md:212`) | `FileSystemUtil.cpp:1369-1379`, `:1418-1427` | **collision**: T20's fix (`file.clear()` before `seekg(0)`, `readAllLines` with it) on T20's branch; read, record, never redone; this slice's case is the FAIL-at-pin control -- ruling (d), L-02, Q5, Q7 (R4 item 12) |
| **#1191** / T21 PL-04 (OPEN, `bug`; body `:9-19`; `t21-streams.md:48-56` (S4); T21 `00-running-log.md:137` (ES `f7c16144d`); `stage-c/argon-grades.md:48` (SO-42), `astra-grades.md:57` (SO-51)) | `FileSystemUtil.cpp:1451-1452`, `:1454-1455` | **collision**: T21's fix on T21's branch; a #585 line for `renameFile` at #1191 `:21`; `copyFile`'s same shape (`:1472-1474`) is named by no lane and is this slice's -- ruling (d), L-03, Q5, Q7 (R4 item 13) |
| Backlog **#1186** (T21 PL-20; body `:1`, `:9`); #1145 (T18's `writeStamp`), #1285, #1289 (T33), #1231 (T26 moved its site, `2dd46a3e3`); T21 `02:403` (*"Left out: the definition"*); T18 `02:468` | `FileSystemUtil.cpp:1429-1443` | **pause**: whether the function itself returns its result, or is marked as superseded by `AtomicFile::writeText`; the call sites are their owners' under #1186 -- L-04, Q5 (R4 item 14) |
| T2 FD-3 (`02:58`); `es-launch-path.md:383`, `:579`; T2 `00-running-log.md:195` (`%ROM%` keeps `getEscapedPath`); T2 `second-opinions/gpt-audit.md:127` (*"I cannot certify universal `%ROM%` safety"*) | `getEscapedPath`'s character list (lines the lane's) | **read** and a unit over the shell's metacharacters: what the list leaves; **rule 6** if it leaves one a ROM name can carry -- Q3 (R4 item 15) |
| T2 `00-running-log.md:234` (*"A lead for T36 (#683)"*) | `getCanonicalPath`'s fold, 32 component indexes in a fixed array, the count unchecked (`:726`, T2's line, not re-read) | **read**; a path of more than 32 components as the case; **rule 6** if it writes past the array -- Q3 (R4 item 16) |
| T33 `stage-c/floor.md:26` (3.3 PRESENT) | a relative path by string prefix: `/storage/roms/snes2/a.png` against `/storage/roms/snes` becomes `.//a.png` (`:986`) | **read**; no disposition found in the lines R4 read -- Q3 (R4 item 17) |
| T2 FD-14 (`04-analysis.md:99`; `00:116`) | `isAbsolute` is `path[0] == '/'` off WIN32 | **read**: cite -- Q3 (R4 item 18) |
| T2 `02:44`; T1's F-07 (#730) | `CommandLineUtil.h`'s `wordEnd` | **read**: cite; the divergence from `runemu.sh` is T1's -- Q3 (R4 item 19) |
| T35's brief `:165-172` (its ruling (h)); D-WORKFLOW-214 | `utils/DownloadFile.{h,cpp}` (not at the pin) | **collision**: ruling (b) -- Q7 (R4 item 20) |
| T35 PL-03 (T35 `02:439`, `04-analysis.md:83`, `05-punch-list.md:31`, *"`utils/Platform.cpp:162-181` (T36's)"*); T2 SS-1 (`02:143`); T35's brief `:141-144` | `Platform.cpp:162-181` | **read**: what `run()` promises a caller -- a shell line, `head -300` of stdout, the stderr file; whether an argv path belongs here (#1192's second half); T35's PL-03 fix is `Scripting`'s quoting -- ruling (j), L-05, Q4 (R4 item 21) |
| `es-guimenu.md:185`; **#1220** (T26: process starts on the interface thread, no caller-side bound) | `runSystemCommand` (`:868`, `:876`) | **read**: whether the return carries the child's exit -- L-13, Q4 (R4 item 22) |
| **#1225** / T26 L-05 (OPEN, `bug`; `:10`, `:15` units ticked on T26's S8; `t26-streams.md:81`; T26 `02:92` (L-39), `:809`, `:819` (the #585 line: ROCKNIX's own, absent from batocera); `00-running-log.md:45`, `:102`; `es-guimenu.md:202`, `:800`) | `Platform.cpp:891-905` | **collision**: T26's fix on T26's branch; the joined-lines contract kept for upstream's callers -- ruling (d), L-06, Q4, Q7 (R4 item 23) |
| `shellQuote` as the fix shape of four lanes: T21 S3 (#1187), T31 PL-03 (#1238), T2 (`formatCommandLineArgument` retired), T26 S8 (`cloudShellQuote` replaced) (#1187 `:16`; `t21-streams.md:43`; `t31-streams.md:51`; T2 `00:195`; `t26-streams.md:85`) | `StringUtil.cpp:426-444` | **read** and a unit: single quotes, `'` escaped, the empty string -- the contract four fixes rest on -- Q4 (R4 item 24) |
| T21 `02:141`, `00-running-log.md:76`, `:96`; `es-state-and-bridge.md:303` (`MaskSecretsTests` 12), `:511-512`; the 2026-09-24 audit `02-forward-audit.md:482` (*"**Gap:** a negative over the"* sweep) | `maskSecrets` (`StringUtil.cpp:715-803`, the name list `:513`, the `wifictl` rule `:764-784`; `--key` absent on purpose, #177) | **read**: the mask's reach; the negative the older audit named is L-14 -- Q4 (R4 item 25) |
| **#840** (OPEN, `bug`, M7.P5; `:12`, `:20`) | the battery read in `Platform.cpp` that `BatteryLevelWatcher` (T35's) polls | **read**: the capacity read and any cache in it, for #840's VM checkbox -- Q6 (R4 item 26) |
| #256 body `:16` (*"a vendored header (backup archives) -- its own PR"*) | `zip_file.hpp` | **read**: its provenance and licence notice; the PR bucket -- Q7 (R4 item 27) |
| Backlog #791 (body `:12`, *T36's Q4 list*) | the ROCKNIX and batocera commits the fork lacks on the 58 | **read**: ROCKNIX's is none (§ 2), batocera's thirteen the list; appended to #791 by the coordinator from the lane's `02` at the stage-D pause -- Q7 (R4 item 28) |
| T35's inherit list (T35 `02:783-797`; T35's brief `:1718-1729`) | the bases, the scripts table (`Platform.cpp:162-181`), the `window-input-tests` recipe, the stand-in's rc, item 10 (the `exists` answer) | **read**: reuse the bases and recipes; T35's item 10 is the item-6 row here -- Q7 (R4 item 29) |
| T34's inherit list (T34 `02:567-579`) | item 6 the reads table (33 rows with writers), item 7 the `components-tests` recipe (`tools/t34-build-tests.sh`), item 9 | **read**: reuse; item 9 is the second row here -- Q7 (R4 item 30) |
| T20 `00-running-log.md:92`; T21 `00-running-log.md:137` | T20's `es-file-tests` (`FileSystemReadTests.cpp`), T21's `es-fs-tests` (four doubles, `tools/t21-build-tests.sh`) -- two host harnesses already compile `FileSystemUtil.cpp` | **read**: this slice's build recipe reuses or consolidates them (§ 5 item 1) -- Q7 (R4 item 31) |
| T20 retro `docs/retros/2026-10-26-m6-es-achievements-pages.md:37`, `:63`; `es-code-traps.md:60` | `FileSystemUtil.cpp`'s three em-dash comments | **read**: a stream's check judges its added lines only -- Q7 (R4 item 32) |
| T26 `00-running-log.md:107` | `Platform.cpp` by the stand-in: `CANNOT` (the SDL fake lacked `SDL_PushEvent`) | **read**: a harness fact for this slice's stand-in (§ 5 item 1) -- Q7 (R4 item 33) |
| T35's brief `:1520` | two T35 files fail the stand-in only through this slice's `utils/*.h` (`Paths`, ...) | **read**: a harness fact -- Q7 (R4 item 34) |
| `es-cloud-pages.md:210`; `es-achievements-pages.md:323`, `:441`; T35's brief `:586`; T34's brief `:240`, `:551` | `OfflineProxyUrl.{h,cpp}` | **read**: the fork file whole, its four cases -- Q7 (R4 item 35) |
| T35's brief `:586`; T34's brief `:812` | `TimeText.{h,cpp}` | **read**: the fork file whole -- Q6 (R4 item 36) |
| T2 FD-7 (posted *"for T36 (`InputManager`)"*) | the controllers blob | **none**: ruling (e) (R4 item 37) |
| T2 SD-5 (`02:134`) | `ThreadPool.cpp` named only as the pool | **none**: the counters are T2's (R4 item 38) |
| T32 `04-analysis.md:80` | `TimeUtil.cpp:514-583`, read for T32's 3.32 | **none**: cited (R4 item 39) |
| #585 body `:45`; `es-achievements-pages.md:187` | `md5.cpp` | **none**: #585's MD5 line is `libretro-common:utils/md5.c` (R4 item 40) |
| T34's held note (T34 `stage-e/retro.md:24`; `docs/retros/2026-10-31-m6-es-core-components.md:26`) | -- | the coordinator's, delivered at dispatch in a scoped form -- ruling (k) (R4 item 41) |
| #1323 (T34 PL-27: a web image's cache file name derived from its URL) | -- | **none claimed**: T34's bug; whether any half reaches this slice is the coordinator's (R4 item 42) |
| #585 (OPEN; body `:45`, the one line matching the slice's names) | -- | the lines this slice owes start with the three never posted (D-WORKFLOW-165): T20 `02:337` (`skipUtf8Bom`, batocera), #1191 `:21` (`renameFile`), T26 `02:819` (`GetShOutput`, ROCKNIX's alone) (R4 § 5), plus this slice's own -- each a line for the coordinator to post, never the lane's (Q7) |

## 3. Read first

In this order, each read in this session, and `01-research-notes.md` says
which were read (`working-principles.md` § Pre-flight):

1. **The rules**, each at the section named, with the question it serves;
   the section's own sentence is not repeated here -- open it. The line
   numbers are the coordinator worktree's at `4536815b6b` where a research
   file printed them, at `153ca325b3` where the drafter printed them, or at
   `e52274caf9` where the proof printed them (proof U-9, CMD8, CMD11; no rule
   changed between the three, the header's diffs); the lane re-reads each
   with `grep -n '^## '` at `COHASH`:

   | Rule | Line | Section | Serves |
   | --- | ---: | --- | --- |
   | `es-code-traps.md` | `:60` | Comments near a translatable string must be ASCII; judge the added lines (R4 § 6) | Q7, § 9 |
   | | `:104`, `:109` | Three things a font is not; the first: `Font::get(size, path)` scales the size (R5 § G; the drafter's `grep -n`) | Q2 (L-07) |
   | | `:118` | the second: *"`Font::getHeight()` is the tallest glyph rasterised so far"* -- **contradicted at the pin by `Font.cpp:115-117`** (L-08; R2 cites `:118-123`) | Q2, Q7 |
   | | `:127` | the third: `Utils::FileSystem::exists(path)` caches for the session | Q1 (L-12) |
   | | `:212` | A file under three bytes reads as empty (#245); R2 cites `:212-215`, R4 `:212-222` | Q5 (L-02) |
   | | `:224-236`, `:238-265` | the curl callback's length; the pooled connection -- `HttpReq`'s, **T21's**, context only (R4 § 6) | Q7 |
   | | `:139` | Pure text has a home, and a test: `CloudText`'s shape for every unit case | § 5 |
   | `es-native-ui.md` | `:103` | Core patterns: *"`runSystemCommand(cmd, name, window)` -- passing `window` shows a splash while it runs"* -- **false at the pin** (L-13; the drafter's `grep -n` at `153ca325b3`) | Q4, Q7 |
   | | `:107` | Core patterns: *"A file another process writes is read uncached"* (R5 § G; the drafter's `grep -n`; R2 cites `:108`) | Q1 |
   | | `:405` | Before the pin moves, the compiler has seen the edit: `tools/es-syntax-check`, exit 2 here | § 5, § 9 |
   | `es-player-text.md` | `:29`, `:141` | Conventions; Every fork string ships in English and French: every label through `_()`; the brand lowercase (D-WORKFLOW-144); D-UI-051 | Q6, § 9 |
   | `es-ui-style-guide.md` | `:32` | Keep the flow and its visual evidence together: the frames a stream's change carries | § 5, § 7 |
   | `engineering-practices.md` | `:12` | Change stays inside the fork's lanes: D-UI-079, § 1's lane and upstream-surface lists | every Q |
   | | `:28` | Check upstream early when troubleshooting: D-WORKFLOW-162, batocera's thirteen (§ 2), the lanes' fixes | Q7 |
   | | `:83` | Verify design intent before "fixing" an apparent bug: `git log -S` before each FAIL-at-pin lead (the `+=`, `head -300`, the `[&]`) | § 4, § 5 |
   | | `:111`, `:194` | Verify the artifact, not the report; A name is not a behaviour: `copyFile`'s `true`, `runSystemCommand`'s 0 (L-03, L-13); a total is the tool's line | § 5 |
   | | `:419` | Guards must fail closed: **a stand-in that compiles an empty translation unit has checked nothing** (§ 5 item 1); `rc=$?` on its own line; the first PASS is the one to distrust | § 5 |
   | | `:806` | Fail gracefully: the last known good state (D-CLOUD-078), L-03, L-04 | Q5 |
   | `bugs-are-agent-first.md` | `:41`, `:53` | The three classes; The rules (rule 6) | every bug |
   | `issue-tracking.md` | `:129`, `:180` | A criterion is agent-first (D-QA-044); Ticking an acceptance criterion | § 7 |
   | `upgrade-and-install.md` | `:40`, `:58` | Fixing forward is not enough; Every fix answers what was already written (D-WORKFLOW-050): **this slice writes files only through its helpers** (`writeAllText`, `copyFile`, `renameFile`, `createDirectory`, the quit flag files `/tmp/*.please`, `es_launch_stdout.log`/`es_launch_stderr.log`): a bug in a helper argues its `Already written:` line for what its callers left; the rest argue *nothing inherited* | every bug |
   | `generic-x64-vm-testing.md` | `:285-324` | The guests render in hardware (proof C13): `--gl auto` (virgl), `--gl none` (llvmpipe), frames over VNC (R3 § 4) | § 5 (every frame) |
   | | `:215`, `:448-455` | font scale 1.31 under 720 px, 1.5 under 320; frame at the handheld's size (R3 § 4) | § 5 (G-02, G-06) |
   | | `:941` | a guest costs about 2 GB of RAM (R3 § 4) | § 5 |
   | | `:100`, `:1145` | Headless, on a build host with no desktop; A settings change made from the shell is invisible to the running interface (proof C12): `run --headless --daemonize`, `tools/vm-serial`, the pidfile; `essway` stopped before a settings edit | § 5 |
   | `handheld-evidence.md` | whole | what a hang is not -- `runSystemCommand` blocking its caller for the command's run is that shape (L-13) | Q4 |
   | `vm-first.md`, `time-to-play.md`, `player-language.md`, `least-surprise.md` | whole | | § 5, Q6, Q7 |

2. **The register.** The rows that name a file or behaviour here (the
   coordinator's branch at `4536815b6b`; the line is the table's; R5 C9, §
   G; R4 § 3): **D-WORKFLOW-213** `:759` and **D-WORKFLOW-214** `:768` (the
   ownership rows of § 1); **D-INFRA-011** `:280` (*"A credential's value
   never reaches a log or a support bundle, and one helper decides what a
   credential looks like"*; its text names `Platform.cpp:830`, R1 C20, R5 §
   G, which is an `#endif` at the pin, the masked log line being `:855`,
   proof K-061 -- the constraint `maskSecrets` and `runSystemCommand`'s log line keep);
   **D-UI-050** `:246` (a size computed *"from a font whose glyphs have been
   rasterised first"*, L-08's family); **D-UI-130** to **D-UI-133** `:763-766`
   (T34's pause rulings: `TextComponent` measures at its drawn width; a
   two-line row's shares from its two fonts; the row inset a screen
   fraction; a help-icon key never through `_()`) -- **none names a T36
   file** and none is this slice's to re-decide (R4 § 3); D-WORKFLOW-144
   `:604` (the brand, ruling (f)); D-CLOUD-078 `:144` (the last known good
   state, L-04's family); D-WORKFLOW-187 `:722`, D-WORKFLOW-189 `:723`,
   D-WORKFLOW-195 `:728`, D-WORKFLOW-212 `:753`, and D-WORKFLOW-188 on the P1
   branch only (R5 § G). **No decided row names the `exists` cache,
   `readAllText`, `GetShOutput` or `shellQuote`** (R4 § 3; R5 C9: no decided
   row matches `exists\(`, `UseFileCache` or `file cache`), so the law of the
   cache is the rules' (`es-code-traps.md:127`, `es-native-ui.md:107`), and a
   row the pause may need is § 9's. Not this slice's: D-CLOUD-190 `:762`,
   D-CLOUD-191 `:767`, D-CLOUD-192 `:769`, D-CLOUD-193 `:770` (T16's cloud
   rows). **The highest decided IDs per area, read from the table above `##
   Open decisions` (`:773`) at `4536815b6b` (R5 C9, the `awk` over the
   decided table only): D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017,
   D-QA-063, D-RA-052, D-SYS-013, D-UI-133, D-WORKFLOW-214** -- D-SYS-014 is
   an open decision (`:779`), not a row (R5 § B item 1); the register is 790
   lines and `tools/register-check` printed rc 0, *"705 IDs, each once; every
   citation in the live documents names a row"* (R5 C9); the drafter's same
   `awk` at `153ca325b3` printed the same nine, and at `acc4674006`
   **D-WORKFLOW-215** (`:771`, the coordinator's row of 11:37 UTC on
   2026-10-31: the test for holding a finding off the public tracker --
   context for § 9's holds, not this slice's to cite otherwise) in place of
   D-WORKFLOW-214, with `## Open decisions` at `:774`; **this slice's
   ownership row is D-WORKFLOW-216**, written at dispatch. The pointer's `Register:`
   line is filled from the same command at `COHASH`, never from here (§ 10).
   The lane reads the cache, writer, pipe and font rows by `tools/archaeology
   'exists cache'`, `'writeAllText'`, `'head -300'` and `'getHeight'` before
   calling anything pending.
3. **The menu map** (`docs/es-menu-map.md`): **no row of this slice's own**,
   and **`tools/es-menu-map-check` reads no slice file** -- its `SOURCE_DIRS`
   at `:58` are `["es-app/src/guis", "es-core/src/guis"]` (R3 § 5), so this
   slice cannot move its count and § 7's map checkbox is worded on the rows
   a stream adds; the lane reads the map's visual-evidence section and the
   pages its guest rows frame (G-03's stamp row, G-04's elapsed-time page)
   before it frames them.
4. **The blindspots** (`docs/blindspot-register.md`): the entries the rules
   above name for this slice's shapes -- a layout computed from what it last
   produced (`es-native-ui.md`), an edit made blind to the compiler (the
   stand-in of § 5), a measurement on a guest whose renderer was not the
   device's (every frame's side), a corpus read on the wrong tree (every
   count at the hash), the self-matching kill pattern and the guard with no
   observed positive (`engineering-practices.md`) -- at the lines the proof
   printed by heading (proof U-4, CMD13, CMD17): 39 `:326` (a PASS over
   dashes, the first PASS), 44 `:445` (proven at a fixture's size), 49 `:590`
   (blind to the compiler), 54 `:720` (a renderer not the device's), 63
   `:944` (llvmpipe and softpipe), 75 `:1206` (a corpus on the wrong tree);
   **the self-matching kill pattern's entry was not found by heading**
   (`[unverified]`: the lane's `grep -n` for its words).
5. **The tests at the pin.** § 5 item 1 describes what exists; read whole
   before a case is written: `es-app/tests/unit/CMakeLists.txt` (159 lines,
   R1 C15; `es-unit-tests` compiles `utils/StringUtil.cpp`,
   `utils/TimeText.cpp`, `utils/OfflineProxyUrl.cpp` at `:62-64`; `:32-33`
   comments naming `CommandLineUtil.h` and `TabStops.h`; `:98`, `:123`,
   `:142` are T21's `AtomicFileUtil.cpp`, R1 C22; R3 § 1.2),
   `es-app/tests/unit/README.md` (`:34`, `:38` hold `CommandLineUtil.h` and
   `TabStops.h`, R2 § 1.4), the slice's test files -- `CommandLineTests.cpp:7`,
   `LaunchCommandTests.cpp:10`, `MaskSecretsTests.cpp:14`,
   `OfflineProxyUrlTests.cpp:14`, `TabStopsTests.cpp:6`, `TimeTextTests.cpp:12`
   (R3 § 1.2) --, `tests/app-unit/CMakeLists.txt` (`StringUtil.cpp` at `:55`,
   `:77`, `:97` in `proxycards-tests` `:51`, `jobs-tests` `:71`,
   `bookkeeper-tests` `:92`, none of which the lanes' scripts build, R3 §
   1.2), **its double of this slice's header
   `tests/app-unit/fakes/utils/FileSystemUtil.h`** (*"Double for
   es-core/src/utils/FileSystemUtil.h: each test program says what exists"*,
   four functions; ruling (g); R3 § 1.3) and the three tests that include it
   (`BookkeeperTests.cpp:12`, `JobsTests.cpp:11`, `ProxyCardsTests.cpp:16`);
   **T20's `FileSystemReadTests.cpp`** (70 lines by `grep -c ''`, 3
   `TEST_CASE`, proof C7, CMD13; doubles
   `bool Settings::_UseFileCache = false;`, `Paths::_instance`,
   `Paths::Paths()`, `Paths::getHomePath()`) and **T21's `FileSystemTests.cpp`**
   (177 lines by `grep -c ''`, 8 `TEST_CASE`, proof C7, CMD13; the real
   `Paths.h`, `Settings.h`,
   `utils/TimeUtil.h`, `utils/ZipFile.h`, `Paths::_instance` defined) on their
   ES branches (R3 § 1.4, cmd 23) -- the precedent for linking
   `FileSystemUtil.cpp` whole; **T35's `t35-extract.py` and
   `t35-window-input-tests.cpp`** at T35's tip, read at stage A (`bb1754e581`
   at R3's read, `5d7650c1dc` at the proof's; the 3.11 region with its
   doubles, R3 § 3, cmd 15).
6. **The walks and the frames.** `tools/vm-walks/` (18 top-level `.steps`,
   R3 cmd 20; `claims.txt`, `masks.txt`, `suite.txt`); `tools/vm-visual-qa`
   (frames over VNC, monitor `sendkey`); `tools/frame-diff` against the
   accepted baseline; `tools/vm-serial` (stamp writes, settings with ES
   stopped); `tools/vm-qa` (its report names the display and Mesa's renderer
   line; `softpipe` there means a guest on the wrong path, R3 § 4);
   `tools/font-stems` (renders a face through the image's FreeType *"the way
   RetroArch's font driver does"* -- `FT_LOAD_DEFAULT`, normal render,
   integer pens; its header `:1-22` -- the reference number for a face and
   size, not `Font.cpp`'s atlas, R3 § 4); `tools/es-launch-memory` (RSS; **no
   tool reads ES's VRAM counters**, R3 § 4); T34's help-bar heights (70/71 px
   at 640x480, 118/118 at 1280x800) as the precedent measure for a scale
   (R3 § 4).
7. **The French**: **11 `_("` lines in the 58** (R2 cmd 28; R3 cmd 17's
   `TOTAL _(" lines: 11`) -- `MathExpr.cpp:95` (`Unknown`, `None`: two
   strings on one line) and `TimeUtil.cpp` x10 (`:517`, `:544`, `:548`,
   `:552`, `:560`, `:569`, `:573`, `:578`, `:580`, `:588`: `never`, `%d d`,
   `%d h`, `%d mn`, `%d sec`), all upstream's (R2 § 7; R3 § 5);
   `tools/es-untranslated` reads `_("...")` in `es-app/src` and
   `es-core/src` (`:66-72`) and lists only strings the upstream base lacks,
   so **the slice's contribution is expected 0** unless a stream adds a
   sentence (R3 § 5). **The French catalog carries a non-empty `msgstr` for
   all seven msgids at the pin** (proof U-3, CMD4): `never` -> `jamais`, `%d
   d` -> `%d j`, `%d h` -> `%d h`, `%d mn` -> `%d mn`, `%d sec` -> `%d sec`,
   `Unknown` -> `Inconnu`, `None` -> `Aucun` (`.po` `:143`, `:1673`, `:3554`,
   `:4007`, `:4011`, `:4015`, `:4019`); the lane re-runs the catalog read as
   its own line (§ 5).
8. **The audits**, each on its lane's branch and in its folder, named here
   once and cited by section elsewhere (the distribution tips are R4 cmd
   2's of 2026-10-31 except T34's and T35's, refreshed below; the ES tips R1
   C17's): **T2**
   `docs/audits/2026_10_23-epic-m6-es-launch-path/` (`7041b0d710`; ES
   `55158d2a64`); **T18** (`6a560b9fbd`; ES `d55235d4b3`); **T20**
   `docs/audits/2026_10_26-epic-m6-es-achievements-pages/` (`ffb6b686cb`; ES
   `5c0ddaaeef`); **T21** `docs/audits/2026_10_26-epic-m6-es-state-and-bridge/`
   (`82c67e99c5`; ES `3ae9610b0f`; `tools/t21-build-tests.sh`, 113 lines,
   and its 13 fakes, R3 cmd 3, cmd 4); **T26**
   `docs/audits/2026_10_27-epic-m6-es-guimenu/` (`bcfad2144b`; ES
   `757f5370ea`); **T31** (`6ec4dda203`; ES `95852f8736`); **T32**
   (`1dd3093853`; ES `b52245036f`); **T33** (`5e3cf605df`; ES `f802c55c62`);
   **T34** (complete; `49c6b43f27`, the held reply's sidecar commit --
   `d60c88966a` at R4's read, `308d0f7571` at the proof's, proof K-170; ES
   `52f0ff5128`; its 14 fakes and `t34-build-tests.sh`, R3 cmd 3); **T35**
   (at stage E, its tip read at stage A -- `bb1754e581` at R4's read,
   `5d7650c1dc` at the proof's; ES at the pin;
   its 15 fakes, `stage-a/syntax-check.sh`, `stage-c/` cases,
   `t35-extract.py`, `t35-build-tests.sh`, R3 cmd 3, cmd 13, cmd 14) -- the
   folders' paths the lane reads from each branch's `ls-tree`. Read with `git
   -C <worktree> show <branch>:<path>`, never a checkout.
9. **The issues**: #683's own body; #1263, #1221, #1177, #1191, #1225, #1186,
   #1271, #1275, #1145, #1285, #1289, #1231, #1187, #1238, #1220, #840, #256,
   #791, #1192, #585 (R4 § 4); #700, #681, #682. States as R4 read them on
   2026-10-31: #1263, #1221, #1177, #1191, #1225, #1271, #1187, #1238, #1220,
   #840 and the caller bugs OPEN `bug`; #1186, #791, #1192 OPEN Backlog;
   #256, #585 OPEN; #683 OPEN, 0 comments (R5 C8). The lane re-reads each
   with `gh --repo pixelelated/distribution issue view` at stage A and
   records the states it saw.
10. **Time to play**: this slice sits under every frame and every press --
    the renderer draws each frame, `Font` measures and rasterises every
    string (`getGlyph` uploads on a miss, `:417`), `TextureResource::get`
    may reload synchronously on the caller's thread (`:110-127`),
    `FileSystemUtil`'s cache answers every `exists`; **on the launch path**
    `ProcessStartInfo::run` with `waitForExit` true wraps the game's command
    (`FileData.cpp:1100-1103`, `head -300` in the pipe, L-05), and
    `runSystemCommand` blocks its caller for the command's whole run (L-13;
    #1220). The retro's line names what the slice costs between a press and
    its frame on the guest -- the launch through `run()` priced from
    `docs/vm-qa-log.md`'s launch number, or `CANNOT` with the harness's
    reason -- never "nothing".

## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of the families the earlier ES briefs
used -- **a layout computed from what it last produced or from a moving
number**, **a house constant a surface does not keep**, **a prompt offered
where the key moves nothing**, **a lifetime or a thread**, **a read of a
file another process writes**, **a player sentence outside the vocabulary
or without its French**, **a structure or merge-debt fact** -- with the
lens, cost against value, asked of every upstream surface: what it costs
the player (a frame's work, a wait, a thread) against what it gives. The
leads are § 2's L-01 to L-18, cited here by number (their lines are the
table's and are not restated), and the floor's pure leads tabled at the end
of this section; each is read at its lines before it is called anything,
and the candidates marked FAIL-at-pin (§ 5) get their `git log -S` first
(`engineering-practices.md` § Verify design intent); the upstream surfaces
outside the lanes are § 1's list, read and recorded, fixed only under rule 6
(D-UI-079). For this slice the natural homes (R3 § 4): the `exists` cache is
*a read of a file another process writes*; `Font::getHeight` and the double
`fontScale` are *a layout computed from a moving number* (and L-08 asks
whether the number moves at all); `FileCache`'s `shared_mutex`, the texture
loader's teardown, `TextureData`'s unlocked fields, `ThreadPool` and
`StringListLock` are *a lifetime or a thread*; the 11 `_("` lines and the
case helpers are *a player sentence*; the three renderers no image compiles
and T21's `DownloadFile.*` under the glob are *a structure fact*. The seven
questions are R4 § 1's proposal, in T35's shape (Q1 to Q6 by subject, Q7
the lens's).

- **Q1 The file cache: what `exists` answers, who erases, who resets**
  (`es-code-traps.md:127`; `es-native-ui.md:107`; the reads and the
  threads runs). **L-12**: the cache's contract stated from the source --
  a miss stored (`:213-215`), a listing's wildcard answering "absent"
  without a stat (`:277-282`), `exists(p, false)` rewriting the entry
  (`:161-162`), the six erasing writers (`:1051`, `:1067`, `:1097`, `:1445`,
  `:1457-1458`, `:1506-1507`), the one reset (`:343-346`), and **every
  writer outside this file** (pugixml `save_file`, `std::ofstream`,
  `std::rename`, another process) invisible to it; **one reconciled table**
  over the five line sets the earlier lanes cited (the take-up table's
  items 6-11), each set mapped onto the pin's lines; **#1271's question**
  (does `isRegularFile` share the entry and remember a miss) answered from
  the source; **T34 L-09's answer** (*"sound at the pin"*) cited for
  `HttpReq`'s writes. **Ruling (h)**: T35's 3.11 FAILs at the pin in T35's
  harness; this slice decides the cache's side -- whether a contained fix
  (an erase on every writer this file cannot see is impossible; a stored
  miss that expires, or a miss never stored, is the shape to price) is put
  to the pause, or the contract stands and the rules' sentences
  (`es-code-traps.md:127`, `es-native-ui.md:107`) are the guard -- and
  states which in `02` § The file cache; T35's case is re-run unchanged
  only by a stage-E stream (§ 5 item 4). **L-15**: `preloadFileSystemCache`'s
  `[&]` lambda reading `trySaveStates` on a detached thread after its
  function returned (3.6, the ASan stand-in) and its unlocked static
  `preloaded`; its callers counted by the lane. A table: every cache entry
  point (`queryCacheEntry`, `insertEntry`, `getCacheEntry`, `remove`,
  `reset`, `fromStat64`), its lock (shared or exclusive), its callers'
  count, and the answer it gives a file another process wrote.
- **Q2 The texture and font caches** (`es-code-traps.md:104`, `:109`,
  `:118`; D-UI-050; #1263; the threads, writes and includes runs).
  **#1263's cache half** (ruling (i)): the three cached
  `exists(localFile)` at `TextureData.cpp:331`, `:339`, `:410` against a
  picture rewritten from outside under the same path; **the texture-cache
  contract** (T34's inherit item 9): `TextureResource::get`'s key
  (`:100`), when a key is dropped (the `weak_ptr` map `:12`, `:146`), and
  whether a rewrite on disk is ever seen while a texture lives under the
  key; the synchronous reload on the caller's thread (`:110-127`), priced.
  **L-10**: the fork's #181 bookkeeping (`setMaxSize`, `rasterizeAt`)
  without `mMutex` beside a loader writing the same fields under it (3.11's
  TSan stand-in), and batocera's `9c48a461b` / `0f9242aee` on the same file
  read as the reconciliation's other side (§ 2). **L-11**: the loader's
  teardown -- `notify_all` without the lock, `paused` keeping every loader
  asleep and the join waiting (3.12). **The font**: **L-07** `getFromTheme`'s
  double scale (3.16; whether the shipped theme reaches it, from the theme's
  XML on the guest, G-01); **L-08** **the rule erratum**: the constructor
  rasterises ASCII 32..127 (`Font.cpp:115-117`, 2014), so `getHeight()` is
  fixed after construction, against `es-code-traps.md:118` and T34's L-02 /
  PL-17 -- 3.8's positive is the proof, the rule sentence is **the
  coordinator's sweep** (`tools/archaeology --reversal 'tallest glyph'`),
  never the lane's edit, and whether PL-17's open item closes on it is the
  pause's; **L-09** measure against draw for a substituted glyph and the
  newline advance (3.17); **L-17** which threads call `Font::get`,
  `sizeText` or `TextureResource::get` -- a question before a claim; a
  worker that measures text reaches `getGlyph`'s GL upload off the context
  thread. A table: every cache in `resources/` (the font map, the
  substitutable characters, the glyph maps, the texture map, the data
  manager's MRU), its key, its lock or none, its eviction, and its readers'
  threads.
- **Q3 Paths and escaping** (the take-up table's items 15 to 19; no R2 lead
  -- R2 did not open these functions). **`getEscapedPath`'s character
  list** (`%ROM%` alone goes through it after T2's fix; T2's second opinion
  *"cannot certify universal `%ROM%` safety"*): what the list leaves, with
  3.19 over the shell's metacharacters, and **rule 6** if it leaves one a
  ROM name can carry; **`getCanonicalPath`'s fold** (32 component indexes,
  the count unchecked, `:726` by T2's line): 3.20, **rule 6** if it writes
  past the array; **the relative path by prefix** (`.//a.png`, `:986`):
  3.21, a disposition (none found); `isAbsolute` and `CommandLineUtil`'s
  `wordEnd` cited (T2's, T1's sides). A table: every path transform in
  `FileSystemUtil` with its input class, its output, and the case that
  holds it.
- **Q4 Processes and the shell: what `run()`, `runSystemCommand` and
  `GetShOutput` promise** (`handheld-evidence.md`; #1220; ruling (j); the
  spawns run). **L-05**: `run()`'s wrap -- `head -300` of stdout, and
  SIGPIPE with status 141 **only once the command's output outruns the pipe
  buffer** (a 400-line output, 1,492 bytes, is held whole and exits 0; 200,000
  lines printed 141, proof C1, CMD4, CMD12); the log path unquoted; `2>`
  binding only the last simple command; both logs overwritten -- with **the
  literal's two host-shell runs at stage A** (3.5) and the image's busybox
  shell on the guest (G-07); **the launch wrapper's redirects read from the
  source** (`runemu.sh:491`, `:500` append the emulator's output to its log;
  `:84` `tee`s the wrapper's own log lines to stdout, so those reach the
  pipe, proof C15) and the image's copy confirmed in G-07; that ES's launch
  command is this script is the lane's trace (proof C15: not settled); the
  callers with `waitForExit` true named. **L-13**: `runSystemCommand` returns 0 always,
  blocks its caller for the command's whole run, and ignores `name` and
  `window` -- 78 call sites, none reading the return; **the rule erratum**:
  `es-native-ui.md:103` says passing `window` shows a splash, and nothing
  does at the pin (3.7's text case and the body's lines are the proof,
  `proved: tree`); the rule sentence is **the coordinator's sweep**, not
  the lane's edit. **L-06**: `GetShOutput`'s lost byte and unchecked
  `popen` -- **T26's fix, a collision** (ruling (d)); this slice's 3.9 is
  the control and the joined-lines contract for upstream's callers is
  stated. **`shellQuote`** (3.18): the contract four lanes' fixes rest on.
  **L-14**: `maskSecrets`'s reach -- the `=`-only test leaves `name:
  value`, JSON and `Authorization:` unmasked (3.10); whether any logged
  line carries those shapes is the lane's grep over the call sites, never
  a claim from the name. **L-18**: the quit path's leaked event, recorded.
  A table: every spawn in the 58 (the 16 lines, all `Platform.cpp`), the
  shell it runs (`/bin/sh` in `run`, `/usr/bin/sh` in `runSystemCommand`),
  whether it waits, what it returns, and which thread its callers run on.
- **Q5 Writes and reads: the helpers' false successes**
  (`upgrade-and-install.md`; D-CLOUD-078; the writes run). **L-03**
  (**FAIL at the pin**, 3.2): `renameFile` and `copyFile` return `true`
  over an absent source, `copyFile` over a short write, `renameFile`'s
  destination removed before an atomic rename and `overWrite = false`
  unprotected on POSIX -- **`renameFile`'s half is T21's fix, a collision**
  (ruling (d)); **`copyFile`'s is this slice's**, with the callers that
  branch on the return (`HttpReq.cpp:479-506`, `Scraper.cpp:672`,
  `SaveState.cpp:154-155`, `GuiMetaDataEd.cpp:483`, `Win32ApiSystem.cpp:745`,
  `:877`) named for their owners. **L-04** (3.3): `writeAllText` cannot
  report a failure -- **T21 PL-20 / Backlog #1186**, whose ruling moves the
  call sites, not the function; **the pause** asks whether the function
  returns its result or is marked superseded by `AtomicFile::writeText`;
  the cloud stamp's temp-and-rename that publishes a short write
  (`ThreadedCloudSync.cpp:943-948`, T18's) named for its owner. **L-02**
  (3.4): the under-three-bytes read -- **T20's fix, a collision**; this
  slice's case is the control. **L-16** (3.15): `createDirectory`'s
  `false` for a directory a concurrent creator made. **No write in the 58
  is temp-and-rename** (R2 § 5): the tree's atomic writer is T21's. A
  table: every write site (the corrected pattern's `:1432`, `:1434`,
  `:1490`, `:1492`, the `rmdir`, `unlink`, `mkdir` and `std::rename` lines,
  `Platform.cpp:244`'s `open(O_CREAT|O_WRONLY)`), its mechanism, whether
  it is atomic, what an interrupted write leaves, and what its return
  claims.
- **Q6 Device reads, the renderers and the fork's text** (`es-player-text.md`
  § Conventions; D-WORKFLOW-144; #840; the strings, includes and non-ASCII
  runs). **L-01** (**FAIL at the pin**, 3.1): `toUpper`/`toLower` corrupt a
  3-byte character with a case pair (Vietnamese, full-width Latin), French
  2-byte accents unaffected; the brand's formatter is a component's (ruling
  (f)); **rule 6** if the fix is contained (`=` for `+=` in the two 3-byte
  branches), the different-length pairs read. **The fork's text**:
  `TimeText` and `TimeUtil`'s fork hunk (the save state manager's times,
  D-UI-058, D-UI-087, D-UI-089), whole; the 11 upstream `_("` lines and
  their French (the catalog parse, § 5; G-04's frames at 640x480 in both
  languages). **#840**: the battery read in `Platform.cpp` that T35's
  watcher polls -- the capacity read and any cache in it, for #840's VM
  checkbox. **The renderers** (no routed item names one, R4 § 1): the
  image builds `Renderer_GLES30.cpp` alone (`-DGLES3=1` ->
  `USE_OPENGLES_30`), **no lane's stand-in has parsed `Renderer.h`'s
  GLES30 branches**, and no thread check exists anywhere in `renderers/`
  (L-17's GL half); the guest runs the same source through Mesa virgl
  (G-05) and **cannot show panfrost's (H700) or Adreno's (SM8550)** -- a
  driver-specific renderer defect is an `open item to test`
  (`bugs-are-agent-first.md`), and the physical fact is the device's
  (`vm-first.md`).
- **Q7 Cost against value, the structure and the merge debt**
  (`time-to-play.md`; `engineering-practices.md` § Change stays inside the
  fork's lanes, § Check upstream early; D-UI-079, D-WORKFLOW-162; the
  membership, scope, delta, includes and non-ASCII runs). **The lens, asked
  of every upstream surface in § 1's list**: `han.h` (20,923) and
  `zip_file.hpp` (10,011) are 30,934 of the 50,840 lines (R1 C09) -- **a
  reading-scope decision, not a figure error** (R1 § 6 D5): what each
  costs the binary and the reader against what it gives (the Korean input
  table; the backup archives' reader, #256's *"its own PR"*), read by
  cited range and recorded; the thread pool's sizing
  (`hardware_concurrency() * mThreadByCore`, `ThreadPool.cpp:26`); the
  texture loader's thread count (`:215-223`); the VRAM budget's tiers (T21's
  `Settings.cpp:233-246`); **the three renderer pairs no image compiles a
  body of** (`Renderer_GL21`, `Renderer_GLES10`, `Renderer_GLES20`: in the
  unconditional CMake list, empty under the image's defines -- a structure
  fact, R3 § 2.2, § 4); `fribidi`'s branch (`HAVE_FRIBIDI`, **whether the
  image build takes it is `[unverified]`**: ES's `CMakeLists.txt:236-241` defines it when `pkg_check_modules(FRIBIDI QUIET fribidi)` finds the library, `package.mk` names no fribidi, `vlc` is built `--disable-fribidi` (`vlc/package.mk:98`), and the tree's `packages/devel/fribidi` is a dependency of `pango` (`pango/package.mk:11`), so whether it is in the sysroot when ES configures is build order, not source (proof U-1, CMD4, CMD8, CMD12, CMD13) -- G-01's `ldd`
  settles it, `image` side); `vlc/vlc.h` unguarded in `TextureData.cpp:12`; **0
  `#if...ROCKNIX` lines in the 58** (R3 cmd 17); the include reach (241
  angle-include lines, proof CMD4, of which 41 non-standard by R3's rule
  with its standard list unstated; 0 quoted external, one macro include, R3 cmd
  9). **The structure**: the 43 identical to `rocknix/master`; T21's
  `utils/DownloadFile.*` falling under the glob at T21's tip (ruling (b));
  the three lane fixes in two of the 58 (ruling (d)); the fakes' double
  (ruling (g)). **Merge debt: none** on the 58 (§ 2's one line);
  **batocera's thirteen** since `1750dded8c` on nine files, four of them
  fork-modified (`Font.cpp`, `Font.h`, `TextureData.cpp`, `Platform.cpp`),
  as the reconciliation list -- the SVG size pair against the fork's #181,
  the fribidi pair against the tab stops, the battery fallback; the hunk
  ranges the lane's `git diff 1750dded8c batocera/master -- <file>` per
  file, never a merge; #791's Q4 list appended by the coordinator from the
  lane's `02`. **The #585 lines owed** (R4 § 5): the three never posted
  (T20's `skipUtf8Bom` for batocera, #1191's `renameFile`, T26's
  `GetShOutput` for ROCKNIX) and this slice's for each upstream-carried
  defect it closes under rule 6 (the case helpers, `copyFile`,
  `preloadFileSystemCache`, the loader's teardown, `getFromTheme`) -- each
  a line the lane writes in `02` for the coordinator to post, never sent
  (D-WORKFLOW-164/165). **The map**: no row of this slice's own; the
  checker reads no slice file (§ 3 item 3).

### The floor's pure leads, carried

The research ran no case (R3 header: *"Nothing was built, compiled or run
against the pin"*), so every row is a candidate until the lane's stage C;
the seams are in the shape `file:line at the pin | the function | what a
case would catch`, each a case in `CloudText`'s shape (`es-code-traps.md` §
Pure text has a home, and a test; § 5 item 1) built by the slice's binary --
**already linked whole** in `es-unit-tests` (`StringUtil.cpp`, `TimeText.cpp`,
`OfflineProxyUrl.cpp`), **linkable whole with test-defined doubles** in T20's
and T21's shape (`FileSystemUtil.cpp` with `StringUtil.cpp` and `md5.cpp`;
`TimeUtil.cpp`, `HtmlColor.cpp`, `md5.cpp`, `Randomizer.cpp`,
`StringListLock.cpp`, `ResourceManager.cpp`, `ThreadPool.cpp` with the
`Platform` functions doubled), or an **extract** (the function's text lifted
into the case, T35's `t35-extract.py` SPECS shape, refusing on drift) where
the source is parse-only (`Platform.cpp`'s `GetShOutput`, `Font.cpp`'s
scaling, `TextureDataManager::cleanupVRAM`, `FileSystemUtil`'s
`FileCache`/`exists`) (R3 § 3). **The candidates the drafter marks
FAIL-at-pin are in bold; the coordinator's order puts L-01, L-03/L-04,
L-05, L-15, L-13 and L-08 first.** A case for a credential shape (3.10)
builds its value at run time, never as a literal (`engineering-practices.md`
§ Guards must fail closed: *"A fixture for a secret scanner is built at run
time"*).

| # | At the pin | Function | What a case would catch |
| --- | --- | --- | --- |
| **3.1** | `utils/StringUtil.cpp:357-362`, `:398-403`; tables `:76`, `:93`, `:153`, `:170` | `toUpper`, `toLower` in `es-unit-tests` | **`CHECK(toUpper("\xE1\xBA\xA1") == "\xE1\xBA\xA0")`, `CHECK(toLower("\xEF\xBC\xA1") == "\xEF\xBD\x81")` FAIL at the pin (L-01; R2 § 8)**; a 2-byte French pair PASSes beside them |
| **3.2** | `utils/FileSystemUtil.cpp:1451-1455`, `:1463`; `:1472-1474`, `:1492`, `:1500-1504` | `renameFile`, `copyFile`, `FileSystemUtil.cpp` linked whole (T21's `es-fs-tests` shape) | **`CHECK_FALSE(renameFile(<absent>, <tmp>))`, `CHECK_FALSE(copyFile(<absent>, <tmp>))`; `renameFile(<a>, <existing>, false)` keeps the existing file -- FAIL at the pin (L-03)**; T21's merged fix turns the `renameFile` half green, `copyFile`'s stays this slice's |
| **3.3** | `utils/FileSystemUtil.cpp:1429-1446` | `writeAllText` | **at the pin there is no return to test** (R2 L-04): a text case records `void` and the unchecked `fwrite`/`fclose`; the fix's case `CHECK_FALSE(writeAllText("/dev/full", "x"))` written for whatever the pause rules (T21 PL-20 / #1186) |
| **3.4** | `utils/FileSystemUtil.cpp:1369-1379`, `:1400-1427` | `readAllText`, `readAllLines` | **write `1\n`; `CHECK(readAllText(p) == "1\n")`, `CHECK(readAllLines(p).size() == 1)` FAIL at the pin (L-02)** -- the control T20's `d9afa5c7c` turns green at the integration, never re-fixed here |
| **3.5** | `utils/Platform.cpp:162-164` | the wrap's literal, run by the host's shell | **with a producer that outlives the pipe buffer, `sh -c '((((seq 1 200000 2> /dev/null ; echo $? >&3) \| head -300 > /dev/null) 3>&1) \| (read xs; exit $xs))'; echo $?` printed `141` on the host's `/usr/bin/dash`, `0` wanted (L-05; proof C1, CMD12)**; the same literal with `seq 1 400` (1,492 bytes, held whole by the pipe) printed `0` (proof CMD4) and is recorded as the PASS-at-pin control -- one run is one observation, the 141 timing-dependent in principle; stage A's runs (§ 5); the image's shell on the guest is G-07 |
| **3.6** | `utils/FileSystemUtil.cpp:1758-1798` (`:1773`, `:1775`, `:1788`, `:1797`) | `preloadFileSystemCache` under ASan | **with `ASAN_OPTIONS=detect_stack_use_after_return=1`, call it and return: a stack-use-after-return report at the pin (L-15)**; the fix captures by value |
| **3.7** | `utils/Platform.cpp:853-880` (`:879`) | `runSystemCommand`, lifted as text | **the body returns `0` at `:879` and reads neither `name` nor `window`** (L-13): the rule erratum's proof (`proved: tree`); no caller reads the return (R2 cmd 14) |
| **3.8** | `resources/Font.cpp:107`, `:115-117`, `:420-421`, `:754-757` | `getHeight` (FreeType and renderer stand-ins) | **a positive, not a FAIL**: `h = getHeight(); sizeText(<ASCII 32..126>); CHECK(getHeight() == h)` -- PASS at the pin is L-08's proof against `es-code-traps.md:118` |
| **3.9** | `utils/Platform.cpp:891-905` | `GetShOutput`, extracted | **`GetShOutput("printf '%0300d\n' 0").size()` is 299 at the pin, 300 wanted (L-06)** -- the control for T26's S8, never re-fixed here |
| **3.10** | `utils/StringUtil.cpp:446-804` | `maskSecrets` in `es-unit-tests` (`MaskSecretsTests.cpp` exists) | **a JSON `"token":"<value>"` with a non-placeholder value built at run time keeps its value at the pin (L-14)**; `name: value` and `Authorization: Bearer` the same |
| 3.11 | `resources/TextureData.cpp:615-645`, `:670-725` against `:92-195` | a `san tsan-...` stand-in | one thread `initSVGFromMemory`, the main thread `setMaxSize`: a TSan report at the pin (L-10); `vlc/vlc.h` faked, `nanosvg` from the tree |
| 3.12 | `resources/TextureDataManager.cpp:215-235`, `:252-253`, `:284` | `TextureLoader`'s teardown, with a timeout | construct, set `paused`, destroy: the join does not return inside the timeout (L-11) |
| 3.13 | `utils/FileSystemUtil.cpp:48-341`, `:1122-1147`, `:161-162` | the cache, extracted in T35's `fs_cache`/`fs_exists` shape | a positive: `exists(p)` miss, `p` written by `std::ofstream`, `exists(p, false)` true and then `exists(p)` true (the entry rewritten, L-12); a listing's wildcard then a file written under it: `exists` false without a stat |
| **3.14** | T35's `window-input-tests` case 3.11 at T35's tip (`InputManager.cpp:1187` with `FileSystemUtil.cpp`) | re-run unchanged, never edited (ruling (h)) | **FAIL at the pin** (`RUN window-input-tests: rc 1; [doctest] test cases: 10 \| 3 passed \| 7 failed ...`, T35 `stage-c/build-tests.out:65`, the tail abridged here; R3 § 1.4; proof C8, CMD15); PASS only when the cache's fix or T35's caller fix lands |
| 3.15 | `utils/FileSystemUtil.cpp:1089-1120` | `createDirectory` | two threads create one path: either returns `false` while the directory exists (L-16) |
| 3.16 | `resources/Font.cpp:99`, `:161-165`, `:1238`, `:1255`; `Renderer.cpp:1149` doubled | the scaling, extracted | `getFromTheme(elem{fontPath only}, ..., orig)->getSize() == orig->getSize()` (L-07); `fontScale()` 1.31 under 720 px, 1.5 under 320 (R3 § 4) |
| 3.17 | `resources/Font.cpp:714-752`, `:1044-1078` | `sizeText` against the cache's last vertex (stand-ins) | a substitutable code point measured wider than it is drawn; the newline's advance counted (L-09) |
| 3.18 | `utils/StringUtil.cpp:426-444` | `shellQuote` in `es-unit-tests` | single quotes around the value, `'` escaped, the empty string quoted -- PASS expected, the contract four fixes rest on (R4 item 24) |
| 3.19 | `getEscapedPath` (`FileSystemUtil.cpp`) | linked whole | each of the shell's metacharacters in a ROM name escaped or not; the ones left named (R4 item 15) |
| 3.20 | `getCanonicalPath` (`:726`, T2's line) | linked whole, ASan | a path of more than 32 components: a write past the array at the pin or not (R4 item 16) |
| 3.21 | the relative path (`:986`) | linked whole | `/storage/roms/snes2/a.png` against `/storage/roms/snes` gives `.//a.png` (R4 item 17) |
| 3.22 | `utils/TimeUtil.cpp:514-588` | `LocaleES` and `Settings` doubles | the ten `_("` shapes (`%d d`, `%d h`, `%d mn`, `%d sec`, `never`) at their thresholds; the 12-hour switch read per call |
| 3.23 | `resources/TextureDataManager.cpp:135-170` | `cleanupVRAM`, extracted | eviction from the least recent end until under `MaxVRAM` MiB; non-reloadable and required textures kept (R3 § 3) |
| 3.24 | `utils/Platform.cpp:235-237` | `quitES`, lifted as text | the `new SDL_Event` never freed (L-18); recorded |
| 3.25 | `FileSystemUtil.cpp:331-332` (`shared_mutex`); `ThreadPool.cpp:26`, `:84`, `:91`; `StringListLock.cpp`; `ConcurrentVector.h` | `san()` TSan programs (R3 § 6 item 2) | concurrent `exists` and cache writers; the pool's start and join; the list lock -- each program's first report line, or none |

## 5. The evidence floor

1. **Can this be done on the VM? Yes -- the host first, then one guest
   window granted on #683.** Every read, count and table runs on the host at
   the pin's bytes. **The host has no toolchain** (#1137):
   `tools/es-syntax-check` exits 2 on this host -- `no build root at $BROOT
   (ES_BUILD_ROOT, --root)` (its `:69`), no ninja (`:71`), no ES build
   directory (`:75`) (R3 § 5, cmd 19) -- and records that line with
   `ES_BUILD_ROOT` set, never empty; the stand-in is what runs. **The
   include graph, read not compiled** (R3 § 2.2): `NON-STD ANGLE INCLUDES:
   41` over the 58, quoted external includes `0`, one macro include
   (`Font.h:11 #include FT_FREETYPE_H`) (R3 cmd 9); `<SDL.h>` in six places
   (`GlExtensions.cpp:2`, `GlExtensions.h:3`, `Renderer.cpp:16`,
   `Renderer_GL21.cpp:11`, `Renderer_GLES10.cpp:16`, `TextureDataManager.cpp:9`),
   `<SDL_events.h>` `Platform.cpp:3`; `<GLES3/gl3.h>` `GlExtensions.h:6`
   under `USE_OPENGLES_30`, **which the image build defines** (`package.mk:25
   -DGLES3=1` -> GLSystem "OpenGL ES 3.0" -> `add_definitions(-DUSE_OPENGLES_30)`,
   `CMakeLists.txt:361-367`); `<SDL_opengles2.h>`, `<SDL_opengl.h>`,
   `<SDL_opengl_glext.h>`, `<GLES/gl.h>` in branches the image does not take;
   `<ft2build.h>` and `FT_FREETYPE_H` unguarded (`freetype` in
   `PKG_DEPENDS_TARGET`; absent on the host, `pkg-config freetype2` not
   found); `<fribidi.h>` under `HAVE_FRIBIDI` (**whether the image takes it
   is `[unverified]`**: build order, not source, proof U-1 -- G-01's `ldd`); `<nanosvg/*>` resolved in the tree;
   **`<vlc/vlc.h>` unguarded** (`vlc` in `PKG_DEPENDS_TARGET`; absent on the
   host); the POSIX network headers and `<langinfo.h>` from glibc; the
   `<Windows.h>` family never reached (R3 § 2.2, cmd 19). **`-DROCKNIX` is
   moot: 0 `#if...ROCKNIX` lines in the 58** (R3 cmd 17). `external/pugixml`
   is a gitlink at the pin, `external/nanosvg` a tree (R3 cmd 19), so the
   pugixml root is the one T35's `stage-a/` environment names, read by `git
   show` from T35's tip; rapidjson is required by the script (no
   `RAPIDJSON_INCLUDE_DIR` holding `rapidjson/document.h`: exit 2, *"nothing
   built"*, R3 § 6).
   **The stand-in check** is T35's `stage-a/syntax-check.sh` (T34's copied,
   T21's `stage-e` shape): `g++ -std=c++17 -fsyntax-only -DHAVE_INTL
   -DROCKNIX -I <fakes> -I es-app/src -I es-core/src -I external -I
   $PUGIXML_INCLUDE_DIR -I $RAPIDJSON_INCLUDE_DIR <file>`, one `rc=N <file>`
   line each, with **`[ "$n" -eq 25 ]`** in T36's copy where T35's hard-codes
   44 (R3 § 2.1), `rc=$?` on its own line; T35's record was a first run of
   `44 file(s) checked, 37 rc 0, 7 not` and a final `44 rc 0` (R3 cmd 14).
   **Fakes**: T35's 15 copied under `stage-a/fakes/` (`FreeImage.h`,
   `SDL.h`, `SDL_audio.h`, `SDL_events.h`, `SDL_joystick.h`,
   `SDL_keyboard.h`, `SDL_main.h`, `SDL_mixer.h`, `SDL_mutex.h`,
   `SDL_power.h`, `SDL_timer.h`, `alsa/asoundlib.h`, `curl/curl.h`,
   `ft2build.h`, `t35-sdl-more.h`; R3 cmd 13), **and the four this slice
   needs**: a FreeType header carrying `Font.cpp`'s eight body symbols
   (`FT IDENTIFIERS NOT IN FAKE: 8` -- `FT_Done_Face`, `FT_Get_Char_Index`,
   `FT_GlyphSlot`, `FT_Init_FreeType`, `FT_Load_Char`, `FT_LOAD_RENDER`,
   `FT_New_Memory_Face`, `FT_Set_Pixel_Sizes`) and the record types the
   opaque `FT_FaceRec_` hides; `vlc/vlc.h` (the three `libvlc_*` types and
   the calls around `TextureData.cpp:343-360`); **`GLES3/gl3.h`** (`GL
   IDENTIFIERS: 173` distinct names across `Renderer_GLES30.cpp`,
   `GlExtensions.h` and `Shader.cpp` -- an upper bound, the desktop branch
   in the count -- the largest new stand-in of any lane); and a
   `t36-sdl-gl.h` with the SDL video and GL names (`SDL IDENTIFIERS IN THE
   SIX FILES: 78; IN T35 FAKES: 109; NOT IN THE FAKES: 67` under `LC_ALL=C`;
   R3 cmd 21's 76 was taken with mis-sorted input and is superseded) (R3 §
   2.3, cmds 21, 22); each fake named in the record when the first errors
   force it; curl, pulse, udev, CEC and TTS not needed (R3 § 2.3).
   **The trap, and what checking nothing looks like**: T31 to T35's check
   defines no `USE_OPENGLES_*`, so every lane's TUs parsed `Renderer.h`'s
   **non-GLES30** branches, never the image's; **a T36 run without
   `-DUSE_OPENGLES_30` compiles `Renderer_GLES30.cpp`, `Renderer_GLES20.cpp`,
   `Renderer_GL21.cpp` and `Renderer_GLES10.cpp` as empty translation units
   -- rc 0, checking nothing** -- while `GlExtensions.h` takes the desktop
   branch (R3 § 2.2). So **the stand-in passes `-DUSE_OPENGLES_30`** (the
   macro the sources test: `GlExtensions.h:5` `#if defined(USE_OPENGLES_30)`
   with the include at `:6`, `Renderer_GLES30.h:5` with the `#define` at
   `:7`, `Renderer.h:99`, `:128`, `:208`, and at least `GlExtensions.h:64`,
   `:88`, `Renderer.cpp:959`, `Renderer_GLES30.cpp:361` to `:2172`,
   `Renderer_GLES30.h:67`, `Shader.cpp:11` to `:626` and `Shader.h:47`,
   `:90` -- proof C9, CMD4, CMD6); `-DGLES3=1` is the package's CMake option,
   which CMake turns into that macro, and **no `#if` in `es-core/src` tests
   `GLES3`**: `git grep -n -w GLES3` prints `3`, rc 0 -- `GlExtensions.h:6`
   (the include path `<GLES3/gl3.h>`) and `Renderer_GLES30.cpp:776`, `:1364`
   (two string literals) -- and `GLES3` is tested only in the top-level
   `CMakeLists.txt` (`:5`, `:9`, `:15`, `:164`, `:205`) (proof C14, U-2,
   CMD4), so `-DGLES3=1` alone on the `g++` line checks nothing. **An rc 0 on a renderer file
   is evidence only beside a positive**: the record carries, per renderer
   `.cpp`, the preprocessed TU's count of a name only its image branch
   defines (`GLES30Renderer`, inside `Renderer.cpp:823-872`'s selection
   chain) with the define and
   without it -- nonzero with, zero without -- and records `Renderer_GL21`,
   `Renderer_GLES10` and `Renderer_GLES20` as **empty under the image's
   defines** (not image code), or checks them in a second, named,
   not-the-image pass (R3 § 2.2, § 6 item 3). **The prediction** (R3 § 2.4,
   from includes, not a run): rc 0 on own headers and std only 6
   (`OfflineProxyUrl`, `Randomizer`, `StringListLock`, `TimeText`, `md5`,
   `StringUtil` with `han.h`); rc 0 through real es-core headers earlier TUs
   parsed 7 (`HtmlColor`, `ThreadPool`, `TimeUtil`, `MathExpr`, `ZipFile`,
   `FileSystemUtil`, `ResourceManager`); rc 0 with an existing fake and
   `Window.h`/`Renderer.h` 3 (`Platform`, `TextureResource`,
   `TextureDataManager`); a new fake 2 (`Font`, `TextureData`); the GL and
   SDL-GL fakes with the define 4 (`Renderer`, `Renderer_GLES30`, `Shader`,
   `GlExtensions`); empty under the image's defines 3 -- *"25 in all"*.
   T26 recorded `Platform.cpp` as `CANNOT` under T21's fakes (the SDL fake
   lacked `SDL_PushEvent`, R4 item 33) where R3 predicts rc 0 under T35's;
   T35's fakes carry the name (`files 15 PushEvent: 1` at `bb1754e581` and at
   `5d7650c1dc`, proof U-6, CMD13), the compile not run -- the first run
   decides, and the record says which fake carried the name.
   **The harness that exists** (R3 § 1.2-1.4): **3 of the 25 `.cpp` are
   compiled and run by a test target at the pin** (`StringUtil`, `TimeText`,
   `OfflineProxyUrl`, in `es-unit-tests`; `RUN es-unit-tests: rc 0;
   [doctest] test cases: 185 | 185 passed | 0 failed | 0 skipped ...` in
   T34's and T35's records, the tail abridged here, proof C8, CMD15), 2 headers tested header-only
   (`CommandLineUtil.h`, `TabStops.h`), **0 of `resources/` beyond
   `TabStops.h` and 0 of `renderers/`**; T34's run closed `TOTAL: 246 test
   cases in 6 binaries` and T35's `TOTAL: 249 test cases in 6 binaries` (R3
   § 1.4, cmds 14, 20); **`FileSystemUtil.cpp`, `md5.cpp` and
   `StringUtil.cpp` are known to compile and link on this host's `g++` with
   only `-I es-core/src -I external` and test-defined `Settings`/`Paths`
   bodies** -- on T20's and T21's branches' text, which differs from the
   pin's at `:1377` (T20) and `:1449-1468` (T21) (R3 § 1.4); T35's
   `window-input-tests` lifts `FileSystemUtil.cpp:48-341` and `:1122-1147`
   verbatim (R3 § 1.4). **No target links `FileSystemUtil.cpp`,
   `Platform.cpp`, `Font.cpp` or the texture classes at the pin** (R2 § 8).
   **The host floor is the lane's own: unit cases for the 25 seams** of §
   4's table in `CloudText`'s shape -- **first the FAIL-at-pin candidates**
   (3.1 the 3-byte pairs, 3.2 the false successes, 3.3 `writeAllText`'s
   missing return, 3.6 the dead parameter, 3.7 `runSystemCommand`'s 0, 3.8
   the height's positive; then 3.5 the pipe's literal in its two forms --
   output past the pipe buffer, `141`, and 400 lines held whole, `0`, the
   PASS-at-pin control (proof C1); then the collision controls 3.4 and 3.9,
   3.10 the mask's JSON shape, 3.14 T35's case),
   each seen to FAIL against the unfixed code before it is trusted, the stub
   checked against the unfixed code first (`engineering-practices.md` §
   Guards must fail closed), a candidate that PASSes at the pin recorded as
   such -- then the rest. **The cases are built by
   `docs/audits/<audit>/tools/t36-build-tests.sh`** (R3 § 6, described, not
   written): `git show` T35's `t35-build-tests.sh` from
   `feature/m6-es-core-window-input-682` at the tip read at stage A (T35 is
   at stage E and moving; `bb1754e581` at R3's read, `5d7650c1dc` at the
   proof's, proof K-170) -- the tip T35's acceptance names, if it has one by
   then -- renamed, the lineage line prepended (T36 <- T35 <- T34 <-
   T33 ...); **kept unchanged**: the refusals (no rapidjson or no `g++`:
   exit 2, nothing built), the `python3 -I` parse of
   `es-app/tests/unit/CMakeLists.txt` into `sources.txt`, `build()` deleting
   a stale binary first, `es-unit-tests`, `es-file-tests`, `es-conf-tests`,
   `es-fs-tests`/`es-settings-tests` when the tree names them, the "any
   other test" loop, `app-unit-tests` under `-fsanitize=address,undefined`,
   the `-D_WIN32` object and `es-file-tests-win32`, the run loop, the
   `TOTAL: N test cases in B binaries` line from the binaries' `[doctest]`
   lines, exit 0/1/2; **T35's block replaced** (`window-input-tests`,
   `t35-extract.py`, `tsan-posts`, `tsan-watchers`, `asan-watchers`) by (a)
   **a `utils-resources-tests` binary** -- `t36-extract.py` in T35's SPECS
   shape (first-line and last-line guards, exit 1 and nothing written on
   drift) for the extract-only seams, the linkable sources named whole
   (`utils/md5.cpp`, `utils/Randomizer.cpp`, `utils/StringListLock.cpp`,
   `utils/StringUtil.cpp`, `utils/HtmlColor.cpp`, `utils/TimeText.cpp`,
   `utils/TimeUtil.cpp`, `utils/FileSystemUtil.cpp` as the cases need them),
   and `t36-utils-resources-tests.cpp` defining the `Settings`, `Paths` and
   `Log` bodies; (b) the sanitizer programs through T35's `san()` with
   extra sources (3.6, 3.11, 3.25); (c) the stand-in above. **The
   include-order trap** (R3 § 6, reasoned, not run): T35's order puts `-I
   tests/app-unit/fakes` before `-I es-core/src`, and a quoted `#include
   "utils/FileSystemUtil.h"` in `FileSystemUtil.cpp` first searches
   `es-core/src/utils/` for `utils/FileSystemUtil.h` (absent) and then the
   `-I` list in order -- so with that order **the real `FileSystemUtil.cpp`
   would be compiled against the four-function double**; a binary that links
   the real file uses its own fakes directory (the `Log.h`/`LocaleES.h`
   doubles copied, no `utils/`), or `es-core/src` first, and the record
   shows which. **The total is quoted as the script's own `TOTAL: N test
   cases in B binaries` line**, never summed by hand
   (`engineering-practices.md` § A name is not a behaviour: *"A total is the
   tool's line"*). `tools/font-stems` prices the image's face at the two
   panel sizes' pixel sizes (the face read off the guest in G-01); it
   renders through FreeType as RetroArch's driver does, not through
   `Font.cpp`'s atlas, so it is the reference number beside G-02's and
   G-06's frames, never their replacement (R3 § 4). The counts and the
   generated tables run on the host.
2. **The guest window** -- one, asked for on #683 at stage B's end with its
   plan and bound (**25 minutes proposed, plus 5 of grace, two boots**: the
   plan below sums to 1,080 s, 18 minutes, by the drafter's `printf '%s\n'
   60 120 180 240 120 180 60 0 0 120 | awk '{s+=$1} END {print s}'` on
   2026-10-31, which printed `1080`; the second boot is inside it; T35's
   window was 30 + 5 for a plan of 1,560 s, R5 § D), granted explicitly by
   the coordinator on #683 and in the shared log's queue. **The queue is the
   shared file's own lines**, `/workspace/tmp/m7-m6-host-coordination.txt`
   (M7 writes timestamped lines, so the whole tail is read): a request is a
   line that names the slice, its plan and its bound; the grant is the
   coordinator's line answering it; the lane's START and RETURN each add a
   line with the census; the file is read before any guest starts (§ 1's
   last command, with the time of the read), and who holds the host is read
   there, with the time. **The conditions, stated here once -- T13's (#660,
   the first M6 lane to hold a guest window, whose shape every later window
   kept), beyond the rule file's own:** one boot of the M6 copy of the image
   (the copy the kit's `t35-vm.txt:10` names, `069fc2704421`, shared by every
   M6 lane, R5 § D; the lane's `ls -l` is the line) **started at 640x480**
   (`generic-x64-vm run --headless --daemonize --res 640x480`, #1141); **the
   image identified by two literals first** (`BUILD_ID` from
   `/etc/os-release` and the file name); **every verdict labelled by side**
   because the image's EmulationStation is M7's composition -- `pin-binary`
   only where the digest found the pin's lines unchanged against the image's
   binary, else `image`; the post contract `START HH:MM:SS UTC` / `RETURN
   HH:MM:SS UTC` as the first line of each post on #683 and a line in the
   shared host file, each with the census (`qemu N, compilers N`); **the
   START post names the detached timer that stops the guest at bound plus
   grace, or says that nothing does** (`engineering-practices.md` § A
   granted guest window names what stops the guest, #1135); the stop by
   pidfile (`tools/vm-stop`, never a pattern); the disk retired after with
   path, size and sha (D-INFRA-022); the guarded `tools/build-preflight
   --reclaim-swap` allowed once, before the guest, never beside it. **The
   guest renders in hardware**: `--gl auto` is `virtio-gpu-gl-pci` with
   Mesa **virgl** on the host's iGPU, `--gl none` is llvmpipe; the image is
   built `-DGLES3=1` like H700's, so the guest runs **the same
   `Renderer_GLES30.cpp`** through a different driver; frames come over VNC
   (`vm-visual-qa`'s RFB client), `screendump` having no surface under the
   GL scanout; `vm-qa`'s report names the display and Mesa's renderer line,
   and `softpipe` there means a guest on the wrong path (R3 § 4). **The
   second boot at 1280x800 is this slice's own need**: `fontScale()` is 1.31
   under 720 px and 1 at 1280x800 (R3 § 4), so the font's scaling is only
   seen at both; a guest's size is QEMU's flag, so the second size is a
   second boot of the same disk. **The floor's limit, said plainly**:
   panfrost's (H700) and Adreno's (SM8550) GLES behaviour, a real panel's
   scaling, and ES's VRAM counters (no tool reads them; an Info log needs
   `Debug=true` with essway stopped) are not the guest's -- a
   driver-specific renderer defect is an `open item to test`
   (`bugs-are-agent-first.md`), and the physical fact is named
   (`vm-first.md`); **no image compiles a body of `Renderer_GL21`,
   `Renderer_GLES10` or `Renderer_GLES20`** (a structure fact, not a device
   no); and **`DownloadFile` has no row**: no slice code at the pin, T21's
   file, ruling (b) (R3 § 4). The QA accounts are needed by no row
   (`tools/qa-accounts`, never printed; never the owner's, D-QA-015). Every
   proof's frames are labelled by side; a fix's frame is
   `fix-walk-pending-image`.

   | G | Behaviour only the running image shows | Walk or serial command | Expected frame or line | Bound (s) |
   | --- | --- | --- | --- | ---: |
   | G-01 | identity and side; the face, the theme, the libraries, the renderer | `vm-serial sh 'cat /etc/os-release; fbset; ls /usr/share/themes; find /usr/share -name "*.ttf" \| head; ldd /usr/bin/emulationstation \| grep -c -E "fribidi\|vlc\|freetype"; ldd /usr/bin/emulationstation \| grep -E "fribidi\|vlc\|freetype"'`; the theme's XML grepped for a `fontPath` without a `fontSize` (L-07's reach); the ES binary's digest against the pin's lines (T26's `g01-identity.txt` shape); `vm-qa`'s renderer line | `BUILD_ID=...`, `640x480`; the face path for `tools/font-stems`; whether `libfribidi` is linked (the `HAVE_FRIBIDI` answer, Q7's `[unverified]`, build order not source per proof U-1, `image` side) and `libvlc` and `libfreetype` with it; L-07's element present or absent; Mesa's virgl renderer line; every frame labelled `image` or `pin-binary` | 60 |
   | G-02 | the font's scale at 640x480 (`Font.cpp:99-101`, `:161-180`; `Renderer.cpp:1149`) | the carousel and one menu page with a help bar; `shot` each | the help bar's height and a row's text height measured by a reader (a stdlib `zlib` PNG reader, never by eye) against T34's 70/71 px precedent (R3 § 4) and `tools/font-stems`' stems for the face at the scaled size -- `image` side | 120 |
   | G-03 | the `exists` cache after a file written by another process (`FileSystemUtil.cpp:213-215`, `:277-282`; `es-native-ui.md:107`) | with ES running, a stamp or file a page reads written over `tools/vm-serial` (the lane names the page and the path in its START post, from the pages that read a script-written stamp -- *"NOT DONE ON THIS DEVICE YET after a run had stamped"*, R3 § 4); open the page; `shot`; leave and reopen; `shot` | the row's frame before and after: the remembered miss shown, or the file seen -- the unit case (3.13, 3.14) is the proof and the frame the confirmation -- `image` side | 180 |
   | G-04 | the 11 strings in English and French (`TimeUtil.cpp:517-588`; `MathExpr.cpp:95`) | the page that shows an elapsed time (the lane reads which from the callers of `TimeUtil`'s relative strings before the window and names it in START); `shot`; `systemctl stop essway`; `system.language` set to `fr_FR` over serial; ES started; the same page; `shot` | each duration string drawn at 640 in both languages without clipping, the French the catalog's (§ 5's parse) -- `image` side | 240 |
   | G-05 | the renderer through Mesa virgl (`Renderer_GLES30.cpp`; the texture cache under a scroll) | `vm-qa`'s display and renderer lines read; a gamelist with art scrolled the length of its list; `tools/es-launch-memory` before and after for RSS | frames without a missing texture or a torn clip; RSS before and after; **ES's VRAM counters `CANNOT`** (no tool reads them); the eviction (`cleanupVRAM`) is 3.23's unit case -- `image` side | 120 |
   | G-06 | the second size: the font's scale at 1280x800 | `tools/vm-stop`; `generic-x64-vm run --headless --daemonize --res 1280x800` on the same disk; `vm-serial wait`; G-02's page again; `shot` | the same measures at `fontScale()` 1 against T34's 118/118 px precedent (R3 § 4); the two sizes' ratio stated as the reader's line -- `image` side | 180 |
   | G-07 | the pipe under the image's shell, and the image's copy of the launch wrapper (`Platform.cpp:162-168`; L-05) | `vm-serial sh 'for n in 400 200000; do sh -c "((((seq 1 $n 2> /dev/null ; echo \$? >&3) \| head -300 > /dev/null) 3>&1) \| (read xs; exit \$xs))"; echo "seq $n rc=$?"; done; readlink -f $(command -v sh)'`; the image's `runemu.sh` read with `grep -n -E 'LOG_FILE=\|OUTPUT_LOG\|tee -a'` against the source's `:40`, `:84`, `:491`, `:500` (proof C15) | the two exits the image's busybox shell prints, each recorded as it prints (the host's dash printed `0` for 400 lines and `141` for 200,000, proof C1); the shell's path; the image's wrapper appending the emulator's output to its log and `tee`ing its own lines to stdout, or the difference named -- `image` side | 60 |
   | G-08 | `Renderer_GL21`, `Renderer_GLES10`, `Renderer_GLES20` | -- | `CANNOT`: no image compiles their bodies (`-DGLES3=1` on every device, R3 § 2.2); a structure fact recorded in `02` § The structure | 0 |
   | G-09 | the handhelds' GL drivers (panfrost on H700, Adreno on SM8550) | -- | `CANNOT`: a device no (`vm-first.md`); a driver-specific defect is an `open item to test` with the physical fact named | 0 |
   | G-10 | close | `tools/vm-stop` on the pidfile; the disk's size and sha; `qemu 0, compilers 0` | `retired.txt`; the leftover check; the RETURN post inside bound plus grace | 120 |

   Sum of the bounds as written: 1,080 s (18 min), the drafter's figure by
   its own command. Every frame is read back for its strings; a measurement
   in pixels is made by a reader, not by eye.
3. **What T37 inherits** is written, not tested here: the slice's
   provenance table (6 / 9 / 43 with both bases named), the file-cache table
   (every entry point, its lock, its answer to a file another process
   wrote; the reconciled line sets), the texture-and-font table (every cache
   in `resources/`, its key, lock, eviction and readers' threads), the
   processes table (the 16 spawn lines with their shells, waits and
   returns), the writes table (every write site with its mechanism and
   atomicity and what its return claims), the `utils-resources-tests` build
   recipe (the doubles, the extracts, the fakes the first errors forced, the
   include order that links the real `FileSystemUtil.cpp`), the stand-in's
   rc per file over the 25 with the renderer positives and the branches it
   did not parse, the `exists` cache's answer stated for T35's 3.11 and for
   #1263, the rule errata L-08 and L-13 as the coordinator dispositioned
   them, and the collision list (T20's, T21's and T26's fixes, T21's
   `DownloadFile.*`, the fakes' double).
4. **A fix lands only under a stream brief** at the stage-D pause, on the
   ES branch, proven twice (`fix-unit-test` through a case the build script
   links, or `fix-walk-pending-image`), the covering case run before every
   commit, under § 9's same-commit rules for the French; **a fix that
   changes `exists`, `readAllText`, `removeFile` or `getFileName`'s
   signature names the `tests/app-unit/fakes/utils/FileSystemUtil.h` double
   and its three binaries as a collision in the hand-back** (ruling (g)); **a
   fix to the cache's answer re-runs T35's 3.11 unchanged from T35's tip
   and records its line** (ruling (h)); **no stream re-makes T20's, T21's
   or T26's fix** -- a stream that must touch the same lines names the
   collision and the coordinator orders the integration (ruling (d)); a fix
   in `es-core/CMakeLists.txt` is T35's file and the integration's. The
   integration's pin bump checks the package by name, `tools/pkgcheck
   emulationstation` (a path matches nothing and exits 0 vacuously, R5 § B
   item 4).

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...* -- **the block below captures neither exit nor
time except where it says `rc=$?`; the lane wraps each run in its own
`rc=$?` line and a `date +%s` pair, or records that it did not**; a run that
cannot be made is `CANNOT` with its reason). From the distribution worktree
after the membership block; `W` the ES worktree (§ 1) -- **before dispatch,
`W` is the `qa-integration` checkout at the pin, read by `git -C` only, and
every expectation below is a line R1, R2 or R3 printed at the pin on
2026-10-31 by `git -C` against `qa-integration`, or one the stranger's
proof printed the same way that day (proof CMD3, CMD4), cited by its
comment, except the lines marked by stage** -- `PIN` the pin, `MB`
the merge base, `FILES` the 58 from the block's paths file; counts by
`/usr/bin/grep` (#1138); **every grep for `_("` is `-F`**; `rc=$?` on its
own line, never after a pipe; **no `cut` truncates an expected error line**:

```bash
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683; PIN=16dbac5211eea7e70db7394372033be2be7df829; G=/usr/bin/grep; MB=cada856d86
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t36/tmp; mkdir -p "$TMPDIR"; df -i /workspace | tail -n 1
FILES=$(cat .qa-scratch/t36/paths.txt)
# the scope (expect 58; cpp 25; h 32; hpp 1; 14 renderers, 11 resources, 33 utils -- R1 C05)
printf '%s\n' $FILES | $G -c .; printf '%s\n' $FILES | $G -c '\.cpp$'; printf '%s\n' $FILES | $G -c '\.h$'; printf '%s\n' $FILES | $G -c '\.hpp$'; printf '%s\n' $FILES | sed -E 's#^es-core/src/([^/]+)/.*#\1#' | sort | uniq -c
# the ES worktree at the pin, clean; the bases (expect the pin; 0; cada856d86; f6c542872e; b2ceb55a7e; 1750dded8c; bccd715707 the merge base's parent -- R1 C01; 14 commits cada856d86..rocknix/master on any path and 0 on es-core/ -- R1 C13)
git -C "$W" rev-parse HEAD | cut -c1-10; git -C "$W" status --short | wc -l; git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10; git -C "$W" rev-parse rocknix/master | cut -c1-10; git -C "$W" rev-parse batocera/master | cut -c1-10; git -C "$W" merge-base "$PIN" batocera/master | cut -c1-10; git -C "$W" rev-parse --short=10 "$MB^1"; git -C "$W" rev-list --count "$MB"..rocknix/master; git -C "$W" rev-list --count "$MB"..rocknix/master -- es-core/
# the lines two ways (expect wc -l 50827; grep -c 50840; no trailing newline: 13, the files § 2 names; han.h + zip_file.hpp grep -c 30934 -- R1 C09)
for p in $FILES; do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l", s}'; for p in $FILES; do git -C "$W" show "$PIN:$p" | $G -c ''; done | awk '{s+=$1} END {print "grep -c", s}'; n=0; for p in $FILES; do a=$(git -C "$W" show "$PIN:$p" | wc -l); b=$(git -C "$W" show "$PIN:$p" | $G -c ''); [ "$a" != "$b" ] && { n=$((n+1)); echo "no newline: $p $a/$b"; }; done; echo "no trailing newline: $n"; for p in es-core/src/utils/han.h es-core/src/utils/zip_file.hpp; do git -C "$W" show "$PIN:$p" | $G -c ''; done | awk '{s+=$1} END {print "han.h + zip_file.hpp grep -c", s}'
# the fork's delta (expect `15 files changed, 1032 insertions(+), 60 deletions(-)` against bccd715707 and against cada856d86 -- R1 C07, C11; `15 files changed, 60 insertions(+), 1032 deletions(-)` from the pin to rocknix/master -- R1 C11; `6 A` and `9 M` -- R1 C11; the 15 numstat rows of § 2 -- R1 C11; 19 log lines, 2 merges, and 19 from bccd715707 -- R1 C12)
git -C "$W" diff --shortstat bccd715707 "$PIN" -- $FILES; git -C "$W" diff --shortstat "$MB" "$PIN" -- $FILES; git -C "$W" diff --shortstat "$PIN" rocknix/master -- $FILES; git -C "$W" diff --name-status "$MB" "$PIN" -- $FILES | cut -c1 | sort | uniq -c; git -C "$W" diff --numstat "$MB" "$PIN" -- $FILES; git -C "$W" log --oneline "$MB".."$PIN" -- $FILES | $G -c .; git -C "$W" log --oneline --merges "$MB".."$PIN" -- $FILES | $G -c .; git -C "$W" rev-list --count bccd715707.."$PIN" -- $FILES
# upstream's delta: the merge-debt record (expect upstream commits 0 rc=1 -- R1 C13; blob-identical to rocknix/master 43 -- R1 C10; batocera on the 58: 13 commits and `9 files changed, 668 insertions(+), 386 deletions(-)` -- R1 C14; changed by both the fork and batocera: Font.cpp, Font.h, TextureData.cpp, Platform.cpp -- R1 C19)
git -C "$W" log --format=%h "$MB"..rocknix/master -- $FILES | $G -c .; rc=$?; echo "upstream commits rc=$rc"; n=0; for p in $FILES; do [ "$(git -C "$W" rev-parse "$PIN:$p")" = "$(git -C "$W" rev-parse -q --verify "rocknix/master:$p")" ] && n=$((n+1)); done; echo "identical to rocknix/master: $n"; git -C "$W" rev-list --count 1750dded8c..batocera/master -- $FILES; git -C "$W" diff --shortstat 1750dded8c batocera/master -- $FILES; comm -12 <(git -C "$W" diff --name-only "$MB" "$PIN" -- $FILES | sort) <(git -C "$W" diff --name-only 1750dded8c batocera/master -- $FILES | sort)
# the other lanes' deltas inside the 58 (expect T20 `1 file changed, 4 insertions(+)`; T26 `1 file changed, 15 insertions(+), 5 deletions(-)`; T21's stat naming utils/FileSystemUtil.cpp, and with the two DownloadFile paths `3 files changed, 101 insertions(+), 6 deletions(-)`; every other tip empty -- R1 C17; T35's ref: whichever line prints, recorded -- R5 C12 printed `fatal: Needed a single revision` for its `rev-parse --verify`)
for b in m6-es-launch-path-649 m6-es-cloud-pages-665 m6-es-achievements-pages-667 m6-es-state-and-bridge-668 m6-es-guimenu-673 m6-es-pages-678 m6-es-app-views-scrapers-679 m6-es-app-system-680 m6-es-core-components-681 m6-es-core-window-input-682; do echo "== $b"; git -C "$W" diff --stat "$PIN" "origin/feature/$b" -- $FILES 2>&1 | tail -n 2; done; git -C "$W" diff --shortstat "$PIN" origin/feature/m6-es-state-and-bridge-668 -- $FILES es-core/src/utils/DownloadFile.cpp es-core/src/utils/DownloadFile.h
# the collisions' commits (expect d9afa5c7c to resolve, an ancestor of T20's tip, its stat `FileSystemUtil.cpp | 4` -- proof U-8, CMD3; f7c16144d's stat `FileSystemUtil.cpp | 17` with the path given, its whole stat naming 8 files -- proof C6, CMD4; R4 items 12, 13; T26's S8 is the lane's read of 757f5370ea's log, R4 item 23 naming no hash)
git -C "$W" show --stat --format='%h %ad %s' --date=short d9afa5c7c -- es-core/src/utils/FileSystemUtil.cpp 2>&1; git -C "$W" show --stat --format='%h %ad %s' --date=short f7c16144d -- es-core/src/utils/FileSystemUtil.cpp 2>&1; git -C "$W" log --oneline "$PIN"..origin/feature/m6-es-guimenu-673 -- es-core/src/utils/Platform.cpp 2>&1
# the strings, two ways (expect `_(" lines TOTAL 11 in 2 files` -- R2 cmd 28, R3 cmd 17, proof K-148 -- MathExpr.cpp and TimeUtil.cpp; the occurrence count 12, MathExpr.cpp:95 carrying two strings -- R2 § 7, proof K-148)
git -C "$W" grep -c -F '_("' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "_(\" lines TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -F '_("' "$PIN" -- $FILES | wc -l; git -C "$W" grep -n -F '_("' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the French of the seven msgids (expect each with a non-empty msgstr: never jamais, %d d %d j, %d h %d h, %d mn %d mn, %d sec %d sec, Unknown Inconnu, None Aucun, at po :143 :1673 :3554 :4007 :4011 :4015 :4019 -- proof U-3, CMD4) and es-untranslated (expect the slice's contribution 0 -- R3 § 5; the tree-wide lines are the lane's)
git -C "$W" grep -n -A1 -E '^msgid "(never|%d d|%d h|%d mn|%d sec|Unknown|None)"$' "$PIN" -- locale/lang/fr/LC_MESSAGES/emulationstation2.po | sed "s/^$PIN://"
out=$(tools/es-untranslated --es-src "$W" --upstream bccd715707 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated rc=$rc"
# the log lines (expect `LOG(Log lines TOTAL 99 in 16 files` -- R2 cmd 28, proof K-149)
git -C "$W" grep -c 'LOG(Log' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "LOG(Log lines TOTAL", s, "in", NR, "files"}'
# the threads and the lifetimes (expect `threads count: 10` -- TextureDataManager.cpp 217 222 234, .h 45; FileSystemUtil.cpp 1788 1797; ThreadPool.cpp 26 84 91, .h 68 -- and one `.detach(`, FileSystemUtil.cpp:1797; weak_ptr in Font.cpp 30 177, Font.h 92, ResourceManager.cpp 229 238, .h 34 35 56, TextureResource.cpp 12 146, .h 70; `delete this` 0 rc=1 -- R2 cmd 17, § 4)
git -C "$W" grep -n -E 'std::thread|\.detach\(|std::async|pthread_create' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'std::thread|\.detach\(|std::async|pthread_create' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F '.detach(' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F 'weak_ptr' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'delete this' "$PIN" -- $FILES | $G -c .; rc=$?; echo "delete this rc=$rc"
# the locks (expect 63 lines: ResourceManager.cpp 2, TextureData.cpp 7, TextureData.h 1, TextureDataManager.cpp 12, TextureDataManager.h 7, ConcurrentVector.h 9, FileSystemUtil.cpp 14, StringListLock.cpp 5, StringListLock.h 3, ThreadPool.h 3 -- proof C2, CMD4; the same pattern without std::atomic prints 58, proof CMD6, so R2 cmd 17's 60 is neither)
git -C "$W" grep -c -E 'std::mutex|shared_mutex|recursive_mutex|lock_guard|unique_lock|shared_lock|condition_variable|std::atomic' "$PIN" -- $FILES | sed "s/^$PIN:es-core\/src\///" | tr '\n' ' '; echo; git -C "$W" grep -n -E 'std::mutex|shared_mutex|recursive_mutex|lock_guard|unique_lock|shared_lock|condition_variable|std::atomic' "$PIN" -- $FILES | $G -c .
# the process spawns (expect `spawn count: 16`, every line in utils/Platform.cpp -- R2 cmd 17, § 5)
git -C "$W" grep -n -E 'system\(|popen\(|execl|execv|fork\(' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'system\(|popen\(|execl|execv|fork\(' "$PIN" -- $FILES | $G -c .
# the writes (expect the `fopen(... "w"` lines FileSystemUtil.cpp 1432 1434 1490 1492 -- R2 cmd 28's corrected listing, the first pattern's 8 having missed them, R2 § 5; zip_file.hpp's `fopen\(|ofstream` lines 6 -- R2 cmd 17)
git -C "$W" grep -n -E 'fopen\(.*"[wa]' "$PIN" -- es-core/src/utils/FileSystemUtil.cpp es-core/src/utils/Platform.cpp | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'fopen\(|ofstream' "$PIN" -- es-core/src/utils/zip_file.hpp | $G -c .
# the helpers' reach over es-app/src and es-core/src (expect runSystemCommand\( 80, ProcessStartInfo 13, GetShOutput\( 27, GetShOutputLines\( 9, writeAllText\( 27, renameFile\( 17, copyFile\( 12, readAllText\( 38, readAllLines\( 5, AtomicFile:: 41 -- R2 cmd 13; none of the runSystemCommand lines reads the return -- R2 cmd 14)
for pat in 'runSystemCommand\(' 'ProcessStartInfo' 'GetShOutput\(' 'GetShOutputLines\(' 'writeAllText\(' 'renameFile\(' 'copyFile\(' 'readAllText\(' 'readAllLines\(' 'AtomicFile::'; do printf '%s ' "$pat"; git -C "$W" grep -n -E "$pat" "$PIN" -- es-app/src es-core/src | $G -c .; done
# the includes and the gates (expect the angle-include line count 241 -- proof CMD4; of them 41 non-standard by R3 cmd 9's rule (NON-STD ANGLE INCLUDES: 41), whose standard list is unstated, so the lane writes its own beside its filtered count; quoted external 0; the macro include Font.h:11; `#if...ROCKNIX` 0 rc=1 -- R3 cmd 17; USE_OPENGLES_30 at least at GlExtensions.h:5 :64 :88, Renderer.cpp:959, Renderer.h:99 :128 :208, Renderer_GLES30.cpp:361 to :2172, Renderer_GLES30.h:5 :67, Shader.cpp:11 to :626, Shader.h:47 :90 -- proof C9, CMD4, CMD6; `GLES3` as a whole word in es-core/src 3 rc=0 -- GlExtensions.h:6 the include path, Renderer_GLES30.cpp:776 :1364 string literals, no `#if` -- proof C14, CMD4)
git -C "$W" grep -n -E '^\s*#\s*include\s*<' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -E '^\s*#\s*include\s+[A-Z_]+' "$PIN" -- $FILES | sed "s/^$PIN://"; git -C "$W" grep -n -E '^\s*#\s*(if|ifdef|ifndef|elif)\b.*ROCKNIX' "$PIN" -- $FILES | $G -c .; rc=$?; echo "ROCKNIX gates rc=$rc"; git -C "$W" grep -n -F 'USE_OPENGLES_30' "$PIN" -- es-core/src/renderers | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -w 'GLES3' "$PIN" -- es-core/src | $G -c .; rc=$?; echo "GLES3 macro rc=$rc"
# the non-ASCII bytes (expect files with a non-ASCII byte 3 -- FileSystemUtil.cpp 3 (`//` comments 225 287 718), StringUtil.cpp 2 (1406 1407, trailing comments after code), StringUtil.h 7 (62-68, string literals); a non-ASCII comment within three lines before a `_(` 0 -- R3 cmd 17, § 5)
n=0; for f in $FILES; do c=$(git -C "$W" show "$PIN:$f" | LC_ALL=C $G -c -P '[^\x00-\x7F]'); [ "$c" != 0 ] && { echo "${f#es-core/src/}:$c"; n=$((n+1)); }; done; echo "files with a non-ascii byte: $n"; git -C "$W" grep -n -P '[^\x00-\x7F]' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the candidate lines (expect `text[pos] +=` at StringUtil.cpp `359 400`, inside 359-361 and 400-402 -- R2 § 1.1, proof K-157; `head -300` at Platform.cpp `162` and `164`, the second the log-off variant -- R2 § 1.2, proof C10; `return 0;` closing runSystemCommand at :879 -- R2 § 1.2; "always initialize ASCII" at Font.cpp:115 -- R2 § 2.1; the `[&]` lambda at FileSystemUtil.cpp:1773 -- R2 § 1.3; the three `exists(localFile` at TextureData.cpp 331 339 410 -- R4 item 1)
git -C "$W" grep -n -F 'text[pos] +=' "$PIN" -- es-core/src/utils/StringUtil.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'head -300' "$PIN" -- es-core/src/utils/Platform.cpp | sed "s/^$PIN://" | cut -d: -f2; git -C "$W" grep -n -i -F 'always initialize ascii' "$PIN" -- es-core/src/resources/Font.cpp | sed "s/^$PIN://" | cut -d: -f2; git -C "$W" grep -n -F '[&]' "$PIN" -- es-core/src/utils/FileSystemUtil.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'exists(localFile' "$PIN" -- es-core/src/resources/TextureData.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" show "$PIN:es-core/src/utils/Platform.cpp" | sed -n '853,880p' | $G -n -E 'return|name|window'
# the pipe's literal, 3.5, in two forms (expect `seq 400 rc=0` -- 1,492 bytes held whole by the pipe, the PASS-at-pin control -- and `seq 200000 rc=141` -- output past the pipe buffer, the FAIL-at-pin case, 0 wanted -- each printed on the host's /usr/bin/dash by proof C1, CMD4, CMD12; one run is one observation, the 141 timing-dependent in principle; the host's sh named beside them)
for n in 400 200000; do sh -c "((((seq 1 $n 2> /dev/null ; echo \$? >&3) | head -300 > /dev/null) 3>&1) | (read xs; exit \$xs))"; rc=$?; echo "seq $n rc=$rc"; done; seq 1 400 | wc -c; readlink -f "$(command -v sh)"
# the menu map (expect the checker's line, and its SOURCE_DIRS at :58 naming es-app/src/guis and es-core/src/guis, no slice directory -- R3 § 5)
out=$(tools/es-menu-map-check --es-src "$W" --ref "$PIN" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-menu-map-check rc=$rc"; sed -n '58p' tools/es-menu-map-check
# the compile (expect `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2 -- R3 § 5, cmd 19, #1137)
F=es-core/src/utils/Platform.cpp; out=$(ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" "$F" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-syntax-check rc=$rc"
# STAGE C -- the lane's scripts, which do not exist at stage A (expect the stand-in's `rc=N <file>` line per .cpp, 25 lines, with the renderer positives -- nonzero with -DUSE_OPENGLES_30, zero without -- beside them; the build script's own `TOTAL: N test cases in B binaries` with 0 failed and `utils-resources-tests` among the binaries; before any fix the FAIL-at-pin candidates' lines by name; T35's case 3.11 FAILing at the pin, re-run unchanged from T35's tip)
bash docs/audits/*-epic-m6-es-core-utils-resources/stage-a/syntax-check.sh 2>&1 | tail -n 27
bash docs/audits/*-epic-m6-es-core-utils-resources/tools/t36-build-tests.sh "$W" 2>&1 | tail -n 10
# STAGE A, after the pointer is read -- the removal check: TIPHASH is the lane's own tip the pointer and the dispatch comment name (MERGE_HASH at stage A); the literal word fails with `fatal: bad revision 'TIPHASH'` (expect empty) and the ES diff against the pin (expect empty before stage E)
git diff --stat TIPHASH HEAD -- packages projects tools | tail -n 1; git -C "$W" diff --stat "$PIN" HEAD | tail -n 1
```

Every expectation above is a research file's printed line or the stranger's
proof's of 2026-10-31, cited in its comment, or marked by stage; the proof
re-ran the block's host lines through `git -C` against `qa-integration` at
the pin (proof CMD3, CMD4). The proof's own are the occurrence count of `_("`
and the log line's file count, the catalog's seven lines, the 63 lock lines,
the angle-include total, the `USE_OPENGLES_30` positions, the `GLES3` count,
the collisions' stat lines and the pipe's two forms (the drafter re-ran that
loop on 2026-10-31 and it printed `seq 400 rc=0`, `seq 200000 rc=141`,
`1492` and `/usr/bin/dash`). The lane prints first: `es-untranslated`'s
tree-wide line, the menu-map checker's line, the angle-include count under
its own standard list, and the non-ASCII listing's exact lines.
The lane re-runs every one as its own line; a line that differs is recorded
beside the expectation, not argued with.

## 6. Outputs

As T26's, T31's, T32's, T33's, T34's and T35's briefs § 6; § 7 is this
section as checkboxes. The folder
`docs/audits/<yyyy_mm_dd>-epic-m6-es-core-utils-resources/`:
`00-running-log.md` to `05-punch-list.md`; `second-opinions/`
(`review-plan.json`, the probe's and the refutation's `.provenance.json`,
`packet-manifest.json`); `stage-a/` to `stage-e/` (the first commands and the
§ 5 runs under `stage-a/`, with T35's 15 fakes and the fakes the first errors
forced under `stage-a/fakes/`, the stand-in's `syntax-check.sh` and its
`syntax-check.out` with one `rc` line per `.cpp` and the renderer positives;
the window plan under `stage-b/`; the host proofs under `stage-c/`, T35's 3.11
re-run among them with its FAIL line; the walks' steps under
`stage-e/walks/`); `tools/` (the generators -- `t36-extract.py`,
`t36-build-tests.sh`, the tables' generators -- each asserting its counts and
each seen to exit 1 on a constructed drift before it is trusted);
`guest-cycle/`; the lint before D; the audit issue (`Audit: M6 T36
EmulationStation's utilities, resources and renderers -- N findings (...)`, a
sub-issue of #683; the audit issue and the bugs are the lane's,
D-WORKFLOW-189; a Backlog for a lead outside the 58 is the coordinator's,
named in the hand-back); and the retro at
`docs/retros/<date>-m6-es-core-utils-resources.md` (**what the slice did to
the two time-to-play numbers**, § 3 item 10's per-frame and per-launch work
priced from the guest and cited from `docs/vm-qa-log.md`, never "nothing" by
default; **what T37 inherits**, § 5 item 3).

**`02-forward-audit.md` carries these sections, in this order, each
generated section's row count stated as "generated, asserted" by the script
that made it:** § Coverage (58 rows, the path in backticks as the first
cell, both tiers: fork-added 6 / fork-modified 9 / upstream-carried 43 and
inventory 15 / 43), § The leads (L-01 to L-18 and 3.1 to 3.25, each with its
lines, its family, who owns it, its disposition), § The file cache (every
entry point with its lock and its answer to a file another process wrote;
the six erasing writers; the reset; the five earlier line sets reconciled
onto the pin's; #1271's question; T35's 3.11 and ruling (h);
`preloadFileSystemCache`), § The texture and font caches (every cache in
`resources/` with its key, lock, eviction and readers' threads; #1263's
three reads; the texture key's contract; the font's scale, height, measure
and glyph upload; the loader's teardown), § The paths (every transform in
`FileSystemUtil` with its input class, output and case; `getEscapedPath`'s
list), § The processes (the 16 spawn lines with their shells, waits,
returns and callers' threads; `run()`'s wrap; `runSystemCommand`;
`GetShOutput` as T26's collision; `shellQuote`'s contract; `maskSecrets`'
reach), § The writes and reads (every write site with its mechanism,
atomicity, what an interrupted write leaves and what its return claims; the
two returns the lanes fixed and the two they did not), § The device reads,
the renderers and the words (the case helpers; the battery read for #840;
`TimeText`; the 11 `_("` lines with their msgids and French; the renderer
the image builds and the three it does not; the GL thread question), § The
structure (the three non-image renderers, the include reach and the
branches the host did not parse, the stand-in's renderer positives, the 0
`ROCKNIX` gates, `han.h` and `zip_file.hpp`'s reading scope, T21's
`DownloadFile.*` under the glob, the fakes' double, **the two rule errata
L-08 and L-13 for the coordinator's sweep**, the map's checker line), § The
merge debt (one line: `cada856d86` the base against `rocknix/master`
`f6c542872e`, `bccd715707` its parent, the upstream commit count on the 58 of
0 (14 on any path), 43 of 58 blobs identical pin to master, batocera's
thirteen since `1750dded8c` on nine files, four fork-modified, as the
reconciliation list only; then T20's, T21's and T26's pending fixes in two of
the 58 and T21's two new files as collisions with their owners), § The runs,
§ The guest cycle, § The streams (stage E: **written by the coordinator after
stage D, as for T21, T26, T32, T33, T34 and T35**; the lane leaves the
heading and the pause's dispositions), § Positives, § The #585 lines owed
(one per upstream-carried defect closed under rule 6, in the shape the lane
writes, never sent; the three never posted named for the coordinator), §
What T37 inherits; every proof with `proved:`. The stage-D pause as T21's:
the punch list posted on #683, the lane waits for the coordinator's
dispositions and any stream brief.

## 7. Acceptance

The checklist on #683 becomes this section at dispatch, written there by the
coordinator in place of P1's generated ones (its fifth, naming
`tools/renovation-status`, is replaced by checkbox 5 below as T33's, T34's
and T35's were). Every checkbox names the artifact that ticks it (D-QA-044);
the coordinator ticks at acceptance, from the artifacts, never from the
hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-es-core-utils-resources/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `second-opinions/`, `stage-a/` to `stage-e/`, `tools/` and `guest-cycle/` (`ls` of the folder in the hand-back).
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-es-core-utils-resources/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`), and the same with `--issue <audit issue>` prints `PASS`; Q1 to Q7 are answered in `04-analysis.md` and every punch item carries `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: independent` and one reviewer (`gpt`, `openai/gpt-6-astra`, `max`); its probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named (read directly); `packet-manifest.json` carries the scan block with every hit dispositioned by file:line (library plumbing / macro name / identifier / setting name) and no value, the 15 fork-added and fork-modified files whole, every cited range of the 43 named, and `utils/han.h` and `utils/zip_file.hpp` never whole; `00` shows exactly two keyed invokes.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #585, #649, #665, #667, #668, #673, #678, #679, #680, #681, #682, #684, #791, #840, #1186, #1192, #1220, #1221, #1263, #1271, an M7 issue by number), withdrawn or recorded as written with its reason; `tools/box-check --issue <audit issue>` prints 0 fail; the issue is closed by the coordinator at acceptance.
- [ ] `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` in #683's header carry the lane's commits; the ES read is on the pin's bytes for the 58 files (`git -C <W> diff --stat 16dbac5211 <reviewed-at-es> -- $(cat .qa-scratch/t36/paths.txt)` empty before stage E) and nothing under the distribution's `packages/`, `projects/` or `tools/` changed at any stage against the lane's own dispatch tip (the pointer's merge hash, never `2174265e9c`).
- [ ] `01-research-notes.md` § Scope records § 2's block with its exact output lines (`mine: 58 paths.txt: 58 equal: True`; `lines: 50840 reach: {'shipped': 58} tier: {'upstream-carried': 43, 'fork-own': 15} lang: {'c++': 25, 'c-header': 32, 'c++-header': 1}`; `fork-own lines: 6212`; `read lines: 50840`; `ls-tree at the pin = paths.txt`; `wc -l 50827` and `grep -c 50840` with the thirteen files without a trailing newline; 52 at the merge base and 52 at the base; `15 files changed, 1032 insertions(+), 60 deletions(-)` twice -- or the deltas beside them) and names `cada856d86` as the merge base against `rocknix/master` with `bccd715707` as its parent and `1750dded8c` as the base against `batocera/master`.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `58`; its tier columns read fork-added 6 / fork-modified 9 / upstream-carried 43 and inventory 15 / 43.
- [ ] `02` § The runs records the counts with both rules where they differ, each as a command's own output line or the lane's figure with the command that differs named -- `_("` 11 lines and its occurrence count; `LOG(Log` 99 lines; thread lines 10 with `.detach(` 1 (`FileSystemUtil.cpp:1797`); lock lines 63 with the per-file counts (`TextureDataManager.h` 7, `ConcurrentVector.h` 9, `FileSystemUtil.cpp` 14; proof C2); spawn lines 16, all `Platform.cpp`; the `fopen(... "w"` lines `FileSystemUtil.cpp:1432`, `:1434`, `:1490`, `:1492`; the helpers' reach (R2 cmd 13's ten figures); the angle-include total (241, proof CMD4) and the 41 non-standard with the lane's standard list; 0 `ROCKNIX` gates; the `USE_OPENGLES_30` lines and the `GLES3` word count; the three files with a non-ASCII byte and 0 non-ASCII comments before a `_(`.
- [ ] `02` § The file cache, § The texture and font caches, § The paths, § The processes and § The writes and reads are each generated or asserted by a script under the audit folder's `tools/` that names its row count ("generated, asserted"), and `02` § The runs records each script seen to exit 1 on a constructed drift before it was trusted.
- [ ] `02` § The file cache has one row per cache entry point (`queryCacheEntry`, `insertEntry`, `getCacheEntry`, `remove`, `reset`, the `fromStat64` write) and per erasing writer (`FileSystemUtil.cpp:1051`, `:1067`, `:1097`, `:1445`, `:1457-1458`, `:1506-1507`) with its lock and its answer to a file another process wrote; the five earlier line sets mapped onto the pin's; #1271's `isRegularFile` question answered at its lines; T34 L-09's answer cited; L-12 and L-15 dispositioned (3.6's ASan line, 3.13's positive); T35's 3.11 re-run's line and ruling (h)'s coordination recorded.
- [ ] `02` § The texture and font caches has #1263's three reads (`TextureData.cpp:331`, `:339`, `:410`) with a disposition and G-03's frame or the unit case cited; the texture key's contract (`TextureResource.cpp:100-131`); L-07, L-09, L-10 (3.11's TSan line), L-11 (3.12's line), L-17 (the threads named, or the question left with its reason) dispositioned; **L-08 recorded as a rule erratum with 3.8's PASS line against `es-code-traps.md:118`** and T34 PL-17 named beside it for the coordinator.
- [ ] `02` § The processes has one row per spawn line (the 16) with its shell, whether it waits, what it returns and its callers' thread; L-05 with 3.5's two host-shell rcs (400 lines and past the pipe buffer) and G-07's two image-shell rcs, and the launch wrapper's redirect lines from the source (`runemu.sh:40`, `:84`, `:491`, `:500`) beside the image's copy; **L-13 recorded as a rule erratum against `es-native-ui.md:103`** with 3.7's text case; L-06 recorded as T26's collision with 3.9's control line; 3.18's `shellQuote` contract; L-14 with 3.10's line and the grep of the logged call sites.
- [ ] `02` § The writes and reads has one row per write site with its mechanism, atomicity, what an interrupted write leaves and what its return claims; L-03 with 3.2's FAIL lines (`renameFile`'s half named T21's collision, `copyFile`'s this slice's, its branching callers named for their owners); L-04 with 3.3's record and #1186; L-02 with 3.4's FAIL line as T20's collision control; L-16 with 3.15's line.
- [ ] `02` § The merge debt is one line naming `cada856d86`, `rocknix/master` (`f6c542872e`), `bccd715707` as its parent, the upstream commit count on the 58 of 0 since the base (14 on any path), 43 of 58 blobs identical between the pin and master, and batocera's thirteen commits since `1750dded8c` on nine files (four of them fork-modified: `Font.cpp`, `Font.h`, `TextureData.cpp`, `Platform.cpp`) as the reconciliation list only; then the collisions, each with its owner and its read line: T20's `d9afa5c7c` (#1177), T21's `f7c16144d` (#1191) and `utils/DownloadFile.{cpp,h}`, T26's S8 (#1225), and T34's and T35's ES tips' delta inside the 58 (empty, or named).
- [ ] `02` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason; the `es-syntax-check` line (rc 2) quoted whole, the stand-in syntax check's rc per file over the 25 with the fakes, the pugixml root and `-DUSE_OPENGLES_30`, **beside each renderer file's preprocessed-TU positive with and without the define**, and `Renderer_GL21`, `Renderer_GLES10`, `Renderer_GLES20` recorded as empty under the image's defines or checked in a named second pass; every unit case the lane wrote has its FAIL-then-PASS pair recorded against the unfixed code first, the FAIL-at-pin candidates by name (3.1 to 3.10, 3.14), and a candidate that PASSes at the pin recorded as such, not as a defect.
- [ ] `02` § The guest cycle records the window the coordinator granted on #683 (the comment's time; the START and RETURN posts with their first-line contract, the timer that stops the guest or the sentence that nothing does, and censuses, and the host file's lines beside them), the image by file name and `BUILD_ID` read from the guest at 640x480, G-01 to G-10 with their frames read back at EN and FR and each labelled by side (`image` or `pin-binary`), G-01's `ldd` lines (the `HAVE_FRIBIDI` answer), G-02's and G-06's measures by a reader beside `tools/font-stems`' numbers, G-03's two frames, G-04's French frames, G-05's renderer line and RSS with the VRAM counters `CANNOT`, G-07's image-shell rc and wrapper lines, G-08 and G-09 as `CANNOT` with the reason, the second boot at 1280x800, the disk retired with path, size and sha, the leftover check (`qemu 0, compilers 0`), and the window closed inside its bound plus grace.
- [ ] `00-running-log.md` shows no image build, no fetch (the council runtime from `npm install --offline`; `rocknix/master`, `batocera/master` and the lanes' ES tips read from the shared refs), no handheld, the owner's accounts never named or used, no hosted account, no M7 root, worktree or prep directory, no held directory opened, the guest only inside the granted window, two keyed invokes and every other council call keyless, and nothing written under the ES worktree before stage E (`00`'s own closing census).
- [ ] `04-analysis.md` § Q1 to Q7 are answered at their lines; every `bug` states its trace, its `Already written:` line (argued for the helpers' writes -- what `copyFile`, `writeAllText` and `renameFile` left for their callers on devices and in clouds -- and as *nothing inherited* where the code writes no file) and its VM line in one of the named families and passes `tools/box-check --issue N`; every #585 line owed is written in `02` in the shape the lane writes; every row of § 2's take-up table has a disposition at its lines; the § 1 rulings (a) to (k) each have their `02` row; each of #1263's, #1271's and #1186's rows in `02` quotes the id or the time of the issue's last comment as the lane read it (proof C16).
- [ ] Every proof in `02` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`; every punch item carries `question:`; `02` § What T37 inherits lists § 5 item 3's items with their lines.
- [ ] The retro exists at `docs/retros/<date>-m6-es-core-utils-resources.md`, is posted on #683 with its heading's time from `date -u` in the posting command, says what the slice did to the two time-to-play numbers (the launch through `ProcessStartInfo::run` and `runSystemCommand`'s blocking priced from the guest, or `CANNOT` with the harness's reason; cited from `docs/vm-qa-log.md`), and what T37 inherits.
- [ ] The map: **the rows a stream added, the checker's line quoted, red if it cannot see them** -- `tools/es-menu-map-check` reads no slice file (its `SOURCE_DIRS` at `:58`, R3 § 5), so this slice contributes no title; if a stage-E stream adds, moves or renames a row on a page it touches, `docs/es-menu-map.md` changes in the same commit (D-UI-039) and `tools/es-menu-map-check --es-src <W> --ref <reviewed-at-es>` prints `0 missing` on the branch as handed back, with its full output line quoted in `02` § The structure.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the distribution branch and the ES fork's `.githooks/pre-push-test` on the ES branch before the hand-back merge, and again on the coordinator's simulated merge; every fix on the ES branch has, recorded beside its commit, the covering unit case's PASS line (and its earlier FAIL), its French in the same commit where a sentence changed, `tools/es-syntax-check` PASS where a toolchain exists or else the stand-in `g++ -fsyntax-only` rc with the fakes, the pugixml root and `-DUSE_OPENGLES_30` (or `CANNOT` with the missing header named), and a clean non-ASCII grep over its added lines.
- [ ] The unit build's `TOTAL: N test cases in B binaries` line is quoted in `02` § The runs and in the hand-back from the script's own output, with 0 failed in every binary's summary after the fixes, `utils-resources-tests` among the binaries, the include order that linked the real `FileSystemUtil.cpp` named, and the FAIL-at-pin candidates' earlier FAIL lines (or their PASS-at-pin record) beside it.
- [ ] The hand-back names every collision with its owner: the `tests/app-unit/fakes/utils/FileSystemUtil.h` double and its three binaries if a signature changed (or "no signature changed"), T35's 3.11 line as re-run, T20's, T21's and T26's fixes in `FileSystemUtil.cpp` and `Platform.cpp`, and T21's `utils/DownloadFile.{cpp,h}` under the glob.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and both branches
pushed (the hand-back); the stage-D pause; an explicit maintainer pause on
#683; a blocker named on #683 (the seat failing its provenance gate twice, a
packet scan hit that is a value, two commands that disagree, a block whose
output differs from § 2's beyond the deltas it records, an upstream-carried
file that is not byte-identical to `rocknix/master`, a pointer line that
names the predecessor slice (§ 10)); **not** the host's missing toolchain,
which § 5 names and the `CANNOT` forms absorb, **not** the branches the host
cannot parse (§ 5 names them and the record says which branch was parsed),
**not** a renderer file that compiles empty without `-DUSE_OPENGLES_30`
(the define and the positive are § 5's), **not** a `utils-resources-tests`
binary that fails to build on the first try (the doubles, the extracts and
the include order are the lane's to extend; the first error names the
fake), **not** the guest's lack of the handhelds' GL drivers or of ES's VRAM
counters (G-05's and G-09's `CANNOT`), **not** T35's 3.11 FAILing at the pin
(ruling (h)), and **not** T20's, T21's or T26's fixes in this slice's files
or T21's `DownloadFile.*` under the glob, which § 1 (b) and (d) name as
collisions); an ES worktree that differs from the pin on any of the 58 files
at stage A; or an execution limit, stated as such with the running log
current. A checkpoint is not a stop. An idle session says it is idle on
#683, **and does not end a turn on a post that asks nothing**: a turn ends on
a post or a commit, never on "next is ..." (the T26 lane sat 28 minutes on
exactly that, friction 2026-10-27 10:48 UTC, as T35's brief records).

## 9. Ceremonies owed

The ceremonies every lane owes are the rules that load every session --
`learning-capture.md` (the work-log entry per session headed `#683`, its time
from `date -u` in the same command, `tools/work-log-index --write` after it),
`ceremonies.md` (a friction line the moment something slows, `issue: #683` or
the guard; `tools/ceremony-check --gate` before every push, never
`--no-verify`), `decision-register.md` (a row the same session for any
decision), `vm-first.md` (the VM question before any proof: § 5 answers it),
the mini-retro at stage G posted on #683 in Instruction-Recommendations mode
with its *adjustments* as proposals for the coordinator -- and are not
restated here. What is this slice's:

- **Four register rows the pause may need, all put to the coordinator as
  questions, never decided by the lane** (the ownership ruling of § 1 is the
  coordinator's own row, **D-WORKFLOW-216**, written at dispatch): **the
  `exists` cache** -- whether a miss stays stored for the session (and the
  rules' sentences, `es-code-traps.md:127` and `es-native-ui.md:107`, remain
  the guard) or the cache changes its answer under rule 6 (L-12, Q1, ruling
  (h); no decided row names the cache, § 3 item 2); **the file helpers'
  contract** -- whether `renameFile`, `copyFile` and `writeAllText` report
  what happened (an absent source, a short write) or keep upstream's `true`
  and `void`, beside T21's `renameFile` fix and #1186's ruling on the call
  sites (L-03, L-04, Q5); **the three-byte case** -- whether `toUpper` and
  `toLower` are fixed for 3-byte case pairs under rule 6 or recorded as
  upstream's (L-01, Q6; L-02's under-three-bytes read is T20's fix and named
  beside it, not a second row); and **the pipe** -- whether `run()` keeps
  `head -300` on every waited process's stdout or the launch's output is
  bounded another way (L-05, Q4, G-07's line). Two more may follow from the
  proofs and are named as such, not counted: **the two rule errata** (L-08's
  `es-code-traps.md:118`, L-13's `es-native-ui.md:103`), which are rule
  edits and an `archaeology --reversal` sweep the coordinator owns, not
  register rows the lane writes, and whether T34's PL-17 closes on 3.8's
  positive. The highest IDs are § 3 item 2's (at `acc4674006`: D-CLOUD-193,
  D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013,
  D-UI-133, D-WORKFLOW-215; re-read at `COHASH`); `tools/register-check` is
  the proof; D-WORKFLOW-188 is on the P1 branch only and the merge unites
  them; a row this slice forces takes an ID the coordinator assigns on #683.
- **What a hold is**: a finding is held off the public tracker only under
  D-WORKFLOW-215's test (`docs/decision-register.md:771` at `acc4674006`);
  holding is the coordinator's, and the lane never opens a held directory
  (`/workspace/tmp/m6-t34/held/` included) or looks for the held note T34
  left for this slice (ruling (k)). A finding the lane thinks that row's test
  may cover is raised with the coordinator on #683 before anything about its
  mechanism is posted.
- **The same-commit rules, stated once:** a row added, moved or renamed
  updates `docs/es-menu-map.md` in the same commit and
  `tools/es-menu-map-check` passes before it (D-UI-039; this slice's files
  hold no menu, so a stream that changes one is a stream outside the 58); a
  sentence added or changed carries its French in the same commit (D-UI-051:
  a duration string, `Unknown`/`None`, a new outcome sentence a helper's
  failure would need).
- **Every count is a tool's line** (`engineering-practices.md` § A name is
  not a behaviour): a figure in `02`, a post or the hand-back is the
  command's own output, quoted; a sum, a difference or a rate is computed by
  the command that prints it. **Every grep for `_("` by `-F`**; **no `cut` on
  an expected error line**; **a heading's time from `date -u`, never typed**.
- The ES fork's `.githooks/pre-push-test` after an ES change; a merge with
  conflicts is checked for markers; the ledgers united by whole entries; **a
  commit names its paths**; anything temporary under `/workspace/tmp/m6-t36/`
  after `df -i`, never `/tmp`; the window's record kept on the branch, the
  guest disk retired after it with the retirement recorded in `00`
  (D-INFRA-022); **`rm -rf` only as `"${VAR:?}"/...` or a literal path, in its
  own short command, never inside a `bash -c` script**.
- A fixture that rewrites no path, in a bubblewrap sandbox started with
  `--clearenv` (3.2's, 3.4's, 3.15's and 3.19 to 3.21's temporary files are
  such fixtures; 3.5's pipe runs `seq` and `head` and nothing else); **a
  credential-shaped value (3.10) assembled at run time, never a literal** --
  `.githooks/pre-commit` refuses the literal; the walks' steps under the audit
  folder's `stage-e/walks/`, never under `tools/`; the non-ASCII grep over a
  stream's added lines (`git diff -U0 HEAD -- <file>`, its `+` lines), an
  upstream hit recorded and not fixed (`FileSystemUtil.cpp`'s three em-dash
  comments and `StringUtil`'s Hangul are upstream's, R3 § 5), a glyph in a
  string literal allowed (`es-code-traps.md:60`); a generator seen to exit 1
  on a constructed drift before its table is trusted.
- **Every edited file checked for an unfilled placeholder before its
  commit**: `/usr/bin/grep -c -E '__[A-Z]+__|\b(CO|MERGE_|TIP|V2)HASH\b'`
  is 0 on the pointer, the running log and every artifact (the T31 dispatch
  entry shipped with its two timestamp and URL placeholders unfilled,
  friction 2026-10-27 12:02 UTC, as T35's brief records; the pattern is
  written in pieces here so that this line does not count itself, and the
  four names it matches are § 1's; on the filled dispatch comment only the
  `__[A-Z]+__` half must print 0, R5 § B item 2). This brief carries the four
  names as its own words -- the full pattern printed `15` on version 1 and
  the `__[A-Z]+__` half `0` (proof K-166, CMD12), and on this version the
  drafter's `grep -c` prints `16` and `0` -- so it is never copied into an
  artifact unfilled.
- Commit messages `docs: ...` on the distribution branch, with `Refs #683`;
  on the ES branch the package's convention, `Refs #683, #<bug>`; no closing
  keyword before an issue number while a criterion is open (`issue-tracking.md`).

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#683's checkboxes against their artifacts; the lint's `PASS` line on the
default phase and with `--issue`; `review-plan.json` and the two provenance
files (read directly) and the manifest's scan block; the audit issue's
checkboxes all at an outcome; the coverage table's row count (58), the
generated sections' asserted counts, § The processes' 16 spawn rows, § The
writes and reads' write sites, § The merge debt's one line and its
collisions; every Q bug with its three lines; **re-running on clones of both
branches at their tips under `/workspace/tmp/m6-coordinator/`: the
membership block, every § 5 run in full, the stand-in check with its
renderer positives and the unit build script** (no guest: the window's
record is read, not repeated), through the coordinator's acceptance script,
derived from `t34-accept.sh` with the 2026-10-31 fixes and T35's sections
ported (R5 § E); `register-check` on a simulated merge with the
coordinator's tip; the retro's answers; the five checkers' exit codes; the
collisions named against the `tests/app-unit/fakes/utils/FileSystemUtil.h`
double, against T20's, T21's and T26's fixes and T21's `DownloadFile.*`, and
against T34's and T35's ES tips; **the § 1 rulings' rows in `02`**; T35's
3.11 line and #1263's checkbox against the lane's `stage-c/` and `stage-e/`
record. The lane posts one hand-back comment naming **both tips** and each
artifact by path, writes `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and
`fixed-at-es:` into #683's body, then says it is idle. After acceptance the
coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the lint against **the audit issue**, merges the
distribution branch in its turn after the M7 candidate with the pin moved to
the ES branch's tip in the same integration commit (the ES package built
before it lands, `tools/pkgcheck emulationstation` by package name; T20's,
T21's and T26's fixes and T21's `DownloadFile.*` reconciled there),
regenerates the ledgers, posts any #585 lines in the shape the lane wrote,
files any Backlog the hand-back names, sweeps the two rule errata, and closes
#683 when every row is proven -- which is also when #649, #665, #667, #668,
#673, #678, #679, #680, #681 and #682 close (§ 1); the interface epic #700
closes when its slices have.

**The pointer the lane checks at stage A, line by line.** The seeded pointer
`.github/sessions/saved-session-state-feature-m6-es-core-utils-resources-683.md`
is written by the coordinator from T35's, and T35's was seeded from T34's. So
before the first command after `cat` the lane reads these eleven keys, each
against the one value that would be the seeding error -- **T35's** -- and
reports any that name the predecessor on #683 before going on:

| Key | Must read | The seeding error reads |
| --- | --- | --- |
| `Branch (distribution):` | `feature/m6-es-core-utils-resources-683` stacked on `feature/m6-p1-survey-641` at the P1 tip the dispatch comment names (`2174265e9c` today) | `...-es-core-window-input-682` |
| `Worktree (distribution):` | the § 1 path ending `m6-es-core-utils-resources-683` | `m6-es-core-window-input-682` |
| `Worktree (EmulationStation):` | `W` of § 1, at the pin `16dbac5211` | T35's `m6-es-core-window-input-682` checkout, or another lane's |
| `Executor:` | Opus 5.5 at high effort, the T1 session (`m6-t1-os-launch`), free since T16's close-out, as the dispatch comment on #683 names it | T35's session (the T5 session, `m6-t5-build-engine`) |
| `Epic:` | #700; T2, T18, T20, T21, T26, T31, T32, T33 accepted and open until the integration merge; T34 and T35 at the states the dispatch comment names; T37 and T44 after | "T35 accepted" before it is, or "T34 in flight" |
| `Depth:` | one seat, GPT-6 Astra at `max`; the 15 fork-added and fork-modified files whole (the 6 and the 9), the 43 upstream-carried by cited ranges, `han.h` and `zip_file.hpp` never whole; no binary in the 58 | the 13 fork-added and fork-modified files whole, the 83 upstream-carried by cited ranges |
| `The lens:` | cost against value over 58 paths, `es-core/src/{utils,resources,renderers}/**` less `utils/AtomicFileUtil.*` -- the file helpers and their cache, the process and shell helpers, the string and time helpers, the fonts, the texture cache, the renderers | `es-core/**` as `rest`, 96 paths |
| `The rule:` | nothing under the distribution's `packages/`, `projects/` or `tools/`; nothing in the ES worktree at stages A to D; nothing outside the 58 at stage E | "nothing outside the 96" |
| `The host:` | the shared log and one guest window of 25 + 5 minutes with two boots (640x480, then 1280x800), the START post naming the timer that stops the guest at bound plus grace or saying nothing does | a 30 + 5 window whose plan is the window's and the input's (the toasts, the keyboard, the dialogs) |
| `Register:` | the highest decided row per area read from the table at `COHASH` (at `acc4674006`: D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-133, D-WORKFLOW-215), plus **this slice's ownership row, D-WORKFLOW-216, which the coordinator writes at dispatch** | T35's nine (D-CLOUD-191 ... D-WORKFLOW-213), or D-WORKFLOW-214 or D-WORKFLOW-215 named as this slice's own row |
| `The brief:` | `docs/reviews/briefs/es-core-utils-resources.md` at `V2HASH` (§ 1: filled by the dispatch comment; version 1 has no dispatch hash) | `es-core-window-input.md`, or the literal word `V2HASH` |

**The readings before dispatch** (plan § 3, principle 3): the interface
epic's futro (`docs/futros/2026-10-23-m6-interface.md`, 996 lines at
`4536815b6b` by `grep -c ''`, R5 C5, C10; its last heading `:994`, the
errata from the stranger's proof of T35's brief) takes a T36 kickoff
addendum written by the coordinator with version 2, in T34's and T35's six
bold-led paragraphs (R5 § C: the plan in the order's words, with #683's
`why` naming `AtomicFileUtil` outside the membership; the assumptions; the
known unknowns, with the futro's T36 lines `:191`, `:960`, `:964`, `:986`,
`:990` as their spine; the patterns; the simulation -- an Opus lane with
only the brief auditing `AtomicFileUtil.*` because the `why` names it,
re-reading T21's `DownloadFile.*` as its own, re-making T20's, T21's or
T26's fix, fixing the `exists` cache from T35's side; the adjustments); the
stranger's proof of this version 1 is the next step, and its corrections
make version 2. This brief's hash at dispatch is `V2HASH`.

**What never runs in this slice:** an image build, a compiler beyond the
host's `g++ -fsyntax-only` (plain or with the fakes, the pugixml root and
`-DUSE_OPENGLES_30`) and the generated test build, a fetch (the council
runtime from `npm install --offline`; `rocknix/master`, `batocera/master` and
the lanes' ES tips from the shared refs), a handheld, the owner's accounts or
any hosted account, a host listener on a privileged port, a guest before a
grant on #683, M7's roots, worktrees or prep directories, a held directory
(D-WORKFLOW-215; `/workspace/tmp/m6-t34/held/`), a change outside the 58
files, a change to `docs/es-menu-map.md`, the French catalog or the audit
folder except under a stream brief, a move of the pin, a line in
`es-core/src/components/`, the rest of `es-core` (`Window.*`, `Log.*`,
`InputManager.*`, `Scripting.*`, `ImageIO.*`, `es-core/CMakeLists.txt`),
`utils/AtomicFileUtil.*`, `utils/DownloadFile.*`, `HttpReq.*`, `Settings.*`,
`SystemConf.*`, `CloudText.*`, `es-app/src/` (`ThreadedCloudSync.cpp`,
`SaveState.cpp`, `scrapers/Scraper.cpp`, `FileData.cpp`,
`views/SystemView.cpp`, `guis/GuiMenu.cpp`, `guis/GuiMetaDataEd.cpp`) or
`tests/app-unit/fakes/` without the pause's ruling on its owner, an edit to
T35's `window-input-tests` cases, a re-making of T20's `d9afa5c7c`, T21's
`f7c16144d` or T26's S8, an edit to the rule sentences L-08 and L-13 name
(the coordinator's sweep), a credential-shaped literal in a fixture, a file
written on the guest outside G-03's named path, and a theme or font changed
on the guest's image.

## What version 2 does not settle

The `[unverified]` marks left after the proof, each with the read that
settles it (proof U-1 to U-9; version 1 listed nine items, the proof
settled U-2, U-3, U-8 and U-9 and their marks are gone):

1. **`HAVE_FRIBIDI` in the image build** (Q7; § 5 item 1; G-01) --
   narrowed: ES's `CMakeLists.txt:236-241` defines it when the library is
   found, `package.mk` names no fribidi, `vlc` is built
   `--disable-fribidi`, and `pango` depends on the tree's
   `packages/devel/fribidi`, so it is build order, not source (proof U-1) --
   G-01's `ldd` line, `image` side.
2. **The blindspot entry for the self-matching kill pattern** (§ 3 item 4)
   -- partly: the six other entries' lines are the proof's (U-4); this one
   was not found by heading -- the lane's `grep -n` for its words.
3. **That ES's launch command is `runemu.sh`** (L-05; Q4) -- partly: the
   wrapper's redirects are read from the source (proof C15, U-5); the
   command `FileData.cpp:1100-1103` builds is not traced -- the lane's trace
   and G-07's read of the image's copy.
4. **`Platform.cpp` under the stand-in** (§ 5 item 1) -- partly: T35's fakes
   carry `SDL_PushEvent`, the name T26's lacked (proof U-6); the compile was
   not run -- the first run, the fake that carried the name recorded.
5. **R3 § 2.4's class table and R3 § 6's include-order trap** (§ 5 item 1)
   -- predictions from includes; they need a compiler (proof U-7) -- the
   stand-in's and the build script's first records.

**What the proof did not check, and why** (proof § Not checked): the
tracker's states (#683's body, #700, #1263, #1271, #1186 and R4's `union
count: 55`), which the lane re-reads at stage A (§ 3 item 9); the tools that
run in a checkout or reach the tracker (`es-untranslated`,
`es-menu-map-check`, `es-syntax-check`, `register-check`, `box-check`,
`pkgcheck`), whose source lines it read instead; the compiler-bound figures
(`NON-STD ANGLE INCLUDES: 41` with its standard list unstated, `GL
IDENTIFIERS: 173`, the SDL counts 78 / 109 / 67), quoted here as R3's lines
and nothing more; the lanes' audit folders beyond T34's and T35's records;
the image copy `069fc2704421`, a kit file and not a source by hash; and
behaviour beyond line anchors (L-09's `yTop/2`, L-14's `=` test, the
`glScissor` flips, `getEscapedPath`'s list, `ResourceManager`'s internals),
which are the lane's reads.

**Where the sources disagree, and what this version took:** R2 § 2.1 and
L-08 (the constructor rasterises ASCII, so the height is fixed) against R4
item 4 (the height *"a moving number"*, after `es-code-traps.md:118` and
T34's PL-17) -- this version carries R2's reading as a rule erratum with a
positive case (3.8) and leaves PL-17's closure to the pause; R2 § 1.3's
`es-native-ui.md:108` against R5 § G's `:107` -- the drafter's and the
proof's `grep -n` printed `:107`; R3 § 1.1 and § 1.5 (*"T21's file in T36's
directory"*) against R1 C16, R4 item 20 and R5 § G (D-WORKFLOW-214 names
`utils/DownloadFile.*` T36's) -- ruling (b), the coordinator's, makes it a
collision for the integration; R3 § 1.4's table against its command 4 on
the two build scripts' line counts -- neither figure is quoted here; R4 §
1's cache lines against R2 § 1.3's -- Q1's reconciled table is the lane's;
R5 § G's next free WORKFLOW ID (215) against the register at `acc4674006`
-- this slice's row is D-WORKFLOW-216; R2 cmd 17's `locks total lines: 60`
against § 5's pattern (`63`) and the same pattern without `std::atomic`
(`58`) -- `63` taken, the command's own line (proof C2); R2's *"status 141
read back"* (`R2-code-read.md:93`, reasoned, never run) against the host's
run (`rc=0` for 400 lines) -- both forms carried (proof C1); R1's sha256
prefixes (`R1-membership-provenance.md:243-244`, right) against version 1's
§ 2 (swapped) -- R1's taken (proof C3).

## Corrections in version 2

The stranger's proof of version 1 (2026-10-31,
`/workspace/tmp/m6-coordinator/kit/t36-proof.md`: 18 commands, 170 check rows
-- 149 ok, 17 citing a correction, 4 notes -- and 9 rows on the
`[unverified]` items) found the sixteen corrections below, numbered as the
proof numbers them; each names version 1's lines (`e52274caf9`), the old
words, the new words and the command that settles them. Beside them,
version 2 settled four `[unverified]` items (U-2, U-3, U-8, U-9) and narrowed
four (U-1, U-4, U-5, U-6) as the section above says, took the proof's notes
K-077 (`Renderer.cpp:823-872` is the selection chain) and K-166 (the brief
carries the four placeholder names, so it is never copied unfilled), and
refreshed the moving tips K-170 named: T34 complete with its distribution
tip `49c6b43f27` and its ES branch unchanged at `52f0ff5128`; T35's tip read
at stage A, never copied; the coordinator's tip read at dispatch as
`COHASH`.

1. **C1, the pipe literal** -- v1 `:696` (L-05), `:1100-1101` (Q4), `:1217`
   (3.5), `:1346` (§ 5 item 1's order), `:1458` (G-07), `:1552-1553` (the
   run). Old: *"after 300 lines `head` exits and the command's next write
   raises SIGPIPE"*; 3.5 *"`seq 1 400` ... prints `141` at the pin, `0`
   wanted"*; *"(expect 141 at the pin, 0 wanted -- R2 L-05 ...)"*; G-07
   *"(141 on the host is 3.5's)"*. New: SIGPIPE and 141 only once the
   output outruns the pipe buffer; 3.5 in two forms, `seq 1 200000` printing
   `141` (the FAIL-at-pin case) and `seq 1 400` printing `0` (1,492 bytes
   held whole, the PASS-at-pin control); the run a loop over both; G-07 the
   same two forms under busybox; 3.5 moved after the other FAIL-at-pin
   candidates in § 5 item 1's order. Command: proof CMD4 (`pipe literal
   rc=0`, `/usr/bin/dash`), CMD12 (`seq 200000 rc=141`, `1492`); the drafter's
   re-run of the new loop printed the same four lines.
2. **C2, the lock count** -- v1 `:650` (the files table), `:1538` (the run),
   `:1659` (§ 7). Old: *"13 lock lines (R2 cmd 17)"*; *"expect 60 lines:
   ... TextureDataManager.h 6, ConcurrentVector.h 8, FileSystemUtil.cpp
   13"*; *"lock lines 60 with the per-file counts"*. New: `14` for
   `FileSystemUtil.cpp`; `63` with `TextureDataManager.h 7`,
   `ConcurrentVector.h 9`, `FileSystemUtil.cpp 14`; the pattern without
   `std::atomic` printing `58`, so R2's 60 is neither. Command: proof CMD4,
   CMD6.
3. **C3, the sha256 prefixes** -- v1 `:367-368`. Old: *"sha256 prefixes
   `49bc2745664e52f4` and `d17b9cac4b2c2245`"* after
   `{inventory.json,slices.json}`. New: `d17b9cac4b2c2245` (`inventory.json`)
   and `49bc2745664e52f4` (`slices.json`). Command: proof CMD2 (`inventory
   sha: d17b9cac4b2c2245  slices sha: 49bc2745664e52f4`).
4. **C4, the fork lines inside upstream functions** -- v1 `:560-563`. Old:
   *"Only three fork lines sit inside upstream functions -- `Font.cpp:1-2`
   (the include), the `TextureData.cpp` hunks and `Platform.cpp:855`"*. New:
   the include at `Font.cpp:2` and `buildTextCache`'s `:1027-1029`, `:1105`;
   the `TextureData.cpp` hunks; `Platform.cpp:855`, `:343`, `:367`;
   `TimeUtil.cpp`'s `-189,3 +190,50` rewrite. Command: proof CMD5 (`-U0`
   against `cada856d86`).
5. **C5, `OfflineProxyUrl.h:29`** -- v1 `:317-319` (§ 1 Depth), `:645` (the
   files table). Old: *"`StoreOnlyHeader` (*"a header name, not a value"*,
   `:29`)"*. New: `const char* const StoreOnlyHeader = "X-RA-Store-Only:
   1";` under `:27-28`'s *"As HttpReqOptions::customHeaders takes it, name
   and value in one line."*, dispositioned *a fixed header line, no
   credential*; the old words were T34's brief's (`es-core-components.md:240`).
   Command: proof CMD5, CMD7 (`git grep -F 'not a value'` in `utils/`: no
   line), CMD11.
6. **C6, the collisions run** -- v1 `:1527-1528`. Old: `show --stat ... --
   es-core/src/utils/ 2>&1 | head -n 4` for both hashes, expecting each to
   name `FileSystemUtil.cpp`. New: the path `--
   es-core/src/utils/FileSystemUtil.cpp` and no `head`; expect `| 4` for
   `d9afa5c7c` and `| 17` for `f7c16144d`. Command: proof CMD3, CMD4.
7. **C7, the lanes' test files** -- v1 `:908`, `:910`. Old: *"64 lines, 3
   `TEST_CASE`"*; *"158 lines, 8 `TEST_CASE`"*. New: 70 and 177 lines by
   `grep -c ''`. Command: proof CMD13.
8. **C8, the abridged record strings** -- v1 `:208` (ruling (h)), `:680`
   (positives), `:1227` (3.14), `:1332` (§ 5 item 1). Old: `es-unit-tests:
   rc 0; 185 | 185 passed`; `window-input-tests: rc 1; 10 | 3 passed | 7
   failed`. New: `RUN es-unit-tests: rc 0; [doctest] test cases: 185 | 185
   passed | 0 failed | 0 skipped ...` (T34 `stage-d/build-tests.txt:55`, T35
   `stage-c/build-tests.out:55`) and `RUN window-input-tests: rc 1; [doctest]
   test cases: 10 | 3 passed | 7 failed ...` (T35 `stage-c/build-tests.out:65`),
   each marked abridged at its tail. Command: proof CMD14, CMD15.
9. **C9, the `USE_OPENGLES_30` lines** -- v1 `:1304-1305`, `:1546`. Old:
   *"the macro the sources test: `GlExtensions.h:6`, `Renderer_GLES30.h:5-7`,
   `Renderer.h:99`, `:128`, `:208`"*. New: the test at `GlExtensions.h:5`
   (the include at `:6`) and `Renderer_GLES30.h:5` (the `#define` at `:7`),
   and the run's expectation "at least" the positions the proof printed
   (`GlExtensions.h:64`, `:88`, `Renderer.cpp:959`, `Renderer_GLES30.cpp:361`
   to `:2172`, `Renderer_GLES30.h:67`, `Shader.cpp:11` to `:626`,
   `Shader.h:47`, `:90`). Command: proof CMD4, CMD6.
10. **C10, `head -300`** -- v1 `:1550`. Old: *"`head -300` at
    Platform.cpp:162"*. New: `162` and `164`, the second the log-off
    variant. Command: proof CMD4, CMD5.
11. **C11, `TimeUtil.cpp`'s hunks** -- v1 `:649`. Old: *"the fork's hunk
    `@@ -186,9 +187,56 @@`"*. New: two hunks by `-U0`, `-1,0 +2` (a line-2
    addition) and `-189,3 +190,50` (the rewrite; numstat `51 3`). Command:
    proof CMD3, CMD5.
12. **C12, a rule heading** -- v1 `:830`. Old: *"§ A settings change from
    the shell is invisible to the running interface"*. New: *"A settings
    change made from the shell is invisible to the running interface"*,
    `generic-x64-vm-testing.md:1145`. Command: proof CMD11.
13. **C13, a rule range** -- v1 `:827`. Old: `:284-325`. New: `:285-324`
    (`:285` the heading, `:325` the next). Command: proof CMD8, CMD11.
14. **C14, the `GLES3` test** -- v1 `:1307-1309` (and `:1546`, `:1911-1912`).
    Old: *"`[unverified]` until § 5's `git grep -n -w GLES3` prints, and if
    it prints nothing, `-DGLES3=1` alone on the `g++` line would check
    nothing too"*. New: the grep prints `3`, rc 0 -- an include path and two
    string literals -- so no `#if` in `es-core/src` tests `GLES3` (it is
    tested only in the top-level `CMakeLists.txt`), and `-DGLES3=1` on `g++`
    checks nothing; the mark is removed (U-2). Command: proof CMD4.
15. **C15, the launch wrapper's redirects** -- v1 `:696-698` (L-05),
    `:1899-1900` (version 1's item 5). Old: *"whether the launch wrapper
    redirects its own stdout before it reaches this pipe was not established
    (the only `runemu.sh` R2 found is a QA-log copy ...)"*. New: from the
    product copy `projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh`
    -- `:40`, `:491`, `:500` append the emulator's output to its log, `:84`
    `tee`s the wrapper's own lines to stdout -- so the emulator's output does
    not reach `run()`'s pipe and the wrapper's log lines do; G-07 reads the
    image's copy; that ES's launch command is this script stays
    `[unverified]`. Command: proof CMD8, CMD13, CMD17.
16. **C16, a § 7 clause with no artifact** -- v1 `:1669`. Old: *"#1263's,
    #1271's and #1186's bodies are read to their last comment before their
    rows are written"*. New: *"each of #1263's, #1271's and #1186's rows in
    `02` quotes the id or the time of the issue's last comment as the lane
    read it"*. Command: proof CMD12 (24 checkboxes, this clause the one
    naming no artifact).

Version 2, 2026-10-31 16:13 UTC, after the stranger's proof of version 1 (e52274caf9)

## Errata before dispatch

Found after version 2 by the futro addendum's drafter (2026-10-31; `docs/futros/2026-10-23-m6-interface.md` § T36 kickoff addendum), appended here and never edited into the sections above; where a section and this list differ, this list wins:

- **The launch does not run with SIGPIPE's default disposition.** `httplib::Server::Server()` calls `signal(SIGPIPE, SIG_IGN)` off WIN32 (`es-app/src/services/httplib.h:3605-3608`), `HttpServerThread::run` constructs one (`HttpServerThread.cpp:143`) and `main.cpp:899` starts that thread at every startup; an ignored signal stays ignored across `fork` and `exec`, so every child ES launches inherits it. § 3's 3.5 (`seq 1 200000` printing 141) and § 5's G-07 over `vm-serial` test the shell's default, not the launch: past the pipe's buffer the launch gets EPIPE and lost output, not a signal. G-07 reads `SigIgn` of the running EmulationStation on the guest (`/proc/<pid>/status`, bit `0x1000`) first, and L-05's question becomes what the launch's output does when `head -300`'s pipe is full.
- **T35's S6 moves 3.11 and the cache's writers under this brief.** T35's stream S6 (`t35-streams.md` § S6) reshapes T35's 3.11 to read through `writeDeviceConfig`'s lifted `:1187` with the cache extract as the double and fixes the callers, so at T35's accepted tip that case PASSes whatever the cache answers; ruling (h)'s re-run (this brief's 3.14) then proves the caller's half only, and 3.13 alone tests the cache. And every writer S6 moves onto `AtomicFile::writeText` becomes one the cache cannot see (`AtomicFileUtil.*` has 0 `FileSystem` lines at the pin): Q1 reads the cache's writers as a set that now includes the atomic path, and the pause rules whether `FileSystemUtil`'s cache is told of a write made beside it.
- **The futro's earlier text, corrected here, not there:** `:964` assumes `Font::getHeight` moves after construction, but `Font.cpp:115-117` rasterises ASCII in the constructor and `:419-421` raises the height for ASCII only -- correcting `es-code-traps.md:118` must not over-correct, since a non-ASCII glyph taller than ASCII (an accented French capital) never raises it; `:986`'s cache lines are `remove` `:183-198` and `queryCacheEntry` `:200-216` at the pin; `:990`'s 3.11 is an extract of the cache's lines, not a link of the real file; `:966`'s `X-RA-Store-Only` is the whole header line, name and value `1` (C5); `:189-191`'s `Platform.cpp` is T36's by D-WORKFLOW-214.
- **`HAVE_FRIBIDI` is an undeclared, build-order dependency** (pango brings fribidi; `package.mk` names none); declaring or disabling it is T37's recipe, recorded here for § 8.
- **The three renderer pairs no image compiles have three owners:** the source list is T35's (`es-core/CMakeLists.txt`), the `package.mk:25` define is T37's, the bodies are T36's; § 5's stand-in says what it checks of each.
- **No slice's audit has read `DownloadFile.*`** (T21's addition, outside the pin): it is named in § 1 (b) as a collision and nowhere as read.
- **The vendored code is read at the extraction path first.** `zip_file.hpp` (miniz) and `han.h` have no owner but this slice and are never whole in the packet; at stage B the lane reads `ZipFile::extract` (`ZipFile.cpp:253-260`) and its caller whole and weighs what it finds under D-WORKFLOW-215's test before anything is posted -- a result that meets the test is handled as a hold (the reply and the stream off the tree at mode 600 with their hashes recorded, a neutral public bug, the coordinator told by path), as T34's PL-27 was.
- **The register moved after version 1:** D-UI-134 to D-UI-137 (`decision-register.md:772-775` at `b835565cb8`) and D-WORKFLOW-215 (`:771`) are decided; the ownership row at dispatch is D-WORKFLOW-216, still unwritten at this version.
