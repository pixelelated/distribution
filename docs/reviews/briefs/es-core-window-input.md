# Review brief: M6.P2 T35, EmulationStation's window, input, settings and the rest of es-core: the window and its floating surfaces, the input manager and its config file, the es-core dialogs, the theme parser, the script runner, the watchers, the log (#682)

**Version 2, 2026-10-31, after the stranger's proof of version 1 (`d402dc252f`)**
(D-WORKFLOW-189; `docs/reviews/plan-for-the-plan.md` § 6b, § 6c, § 7; the
proof is `/workspace/tmp/m6-coordinator/kit/t35-proof.md`, 12 commands, and
`## Corrections in version 2` at the end records what it found). Written from five
read-only research files -- R1 membership and provenance, R2 the code read at
the pin, R3 tests, build and harness, R4 the inherited items, R5 the model and
the ceremony (`/workspace/tmp/m6-coordinator/kit/t35-research/`, in no tree)
-- and nothing else: every figure here is one of their quoted tool lines,
cited as `R<n> C<m>` (R1's commands), `R2 cmd <m>`, `R3 cmd <m>`, `R4 § <n>`
or `R5 § <letter>`, or a line the drafter printed on 2026-10-30 in the
coordinator worktree and says so; **`[unverified]` marks what no tool line settles, with what would settle
it**; version 1 carried 22 such lines, the proof settled all but one
question (`UDEV_FOUND`, Q7 and § 5 item 1, `CANNOT` on this host with G-01's
read named), and the last section lists it.
Counts by `/usr/bin/grep`, never the shell's function (#1138). The structure
is T34's brief (`docs/reviews/briefs/es-core-components.md`, version 2 at
`a6e14fed86`, its errata section committed in `200a9a032d`); every
T34-specific paragraph is replaced and every boilerplate paragraph R5 § A
marks *copy* is copied with the slice's names, numbers and placeholders.
The rule, register, menu-map and blindspot line numbers are the coordinator
worktree's at **`a00b3354d5`** (`feature/m6-renovation-plan-346`, read by
the stranger's proof on 2026-10-31): `git diff --stat 7a32dff771 a00b3354d5
-- .claude/rules docs/decision-register.md docs/es-menu-map.md
docs/blindspot-register.md docs/futros` prints
`.claude/rules/es-player-text.md | 8 +-` (its lines from `:273` on moved by
+4, `30c3c402fd`), `docs/decision-register.md` (seven rows after
D-WORKFLOW-213 `:759`: D-CLOUD-190 `:762`, D-UI-130 to D-UI-133 `:763-766`,
D-CLOUD-191 `:767`) and `docs/futros/2026-10-23-m6-interface.md | 4 +`; the
map (989 lines) and the blindspots (1,250) are unchanged since `a8fe371b0a`,
so every map and blindspot line T34's brief cites holds here; the register's
`## Open decisions` opens at `:769`.

## 1. Identity

- **Issue:** #682 `M6.P2 E339/T35: interface: EmulationStation's window,
  input, settings and the rest of es-core` (the live title, read 2026-10-30
  at 14:38 UTC by `gh --repo pixelelated/distribution issue view 682`: OPEN,
  0 comments, 0 labels; milestone `M6: Codebase renovation` per R5 § D),
  **retitled at dispatch to `M6.P2 E700/T35: interface: EmulationStation's
  window, input, settings and the rest of es-core`**
  (`milestone-phase-naming.md`; the body says *"under epic #339 until this
  area's epic is filed"*, and #700 is filed; #681 was retitled `E700/T34` the
  same way on 2026-10-30, 2 comments on it at this read). Slice
  `es-core-window-input` (`k: 35`) in `docs/reviews/slices.json`,
  thirty-fifth in `docs/reviews/order.md` (`order.md`, `slices.json` and
  `inventory.json` are the P1 branch's, which the lane's worktree is stacked
  on; not on `next`, not in the coordinator worktree; the research read them
  in the P1 research clone `/workspace/tmp/m6-coordinator/t11-research/tree`
  at `2174265e9cc1b248c0fbe27fa101875984d46d6b` by `git show`, R1 C02; its § T35 is `order.md:633-641` (`:635` the id, kind and lens; `:637` the
paths line; `:641` the closing evidence; `:643` opens § T36), read on the P1
clone by the proof). #682's body (R5 § D): *"96 paths,
  22,575 lines; 22,575 lines read, 6,759 of them fork-own (inventory at
  `eb4763e3cc`)"*; **Provenance tiers:** fork-own 13, upstream-carried 83;
  its `why` *"`Window.cpp` (one floating surface at a time, D-UI-093),
  `InputManager`, `Settings`, `SystemConf`, `HttpReq` (the pooled-connection
  trap), `GunManager` and es-core's own pages"*; **kind currency; lens cost
  against value**; read before none (D-WORKFLOW-187); depth Independent;
  interacting subsystems *"every page; `es-code-traps.md` (the pooled
  connection, `exists` caching, fonts)"*; closing evidence *"audit folder, lint PASS, punch list through Phase 7"*
(`order.md:641` at `2174265e9c`; #682's body carries its four generated
checkboxes in its place, read by `gh` on 2026-10-31).
  The selector is one object, `{"globs": ["es:es-core/**"], "rest": true}`
  (R1 C09), area `interface`. **Epic:** #700 `M6.P2 E339: Area epic: the
  interface, EmulationStation (T2, T18, T20, T21, T26, T31 to T37, T44)`:
  T2 #649, T18 #665, T20 #667, T21 #668, T26 #673, T31 #678 and T32 #679
  are **accepted, and their issues stay open** until the integration moves
  the pin on `next` (§ 10); T33 #680 handed back at 14:40 UTC 2026-10-30 (its merged distribution tip
`947ace1966`, its ES tip `f802c55c62`) and **accepted** the same day
(`17f2bcea8d`; its audit issue #1270 CLOSED at the proof's read), its PL-25
bug **#1305** (filed 14:45 UTC on #680) routing a half here (§ 2's take-up
table, § 4 Q4); T34 #681 is in flight (dispatched 2026-10-30; its punch list
**#1307** -- *43 findings (0 critical, 1 high)* -- filed, and its stage D
ruled by the coordinator's `4e754f89c7` with D-UI-130 to D-UI-133 as its
four pause rulings; its ES branch `feature/m6-es-core-components-681` at the
pin, 0 commits ahead, R1 C19, C20; #1307's PL-04 and PL-05 route here, § 2's
take-up table, § 4 Q6); this slice; T36 #683, T37 #684 and T44 after. The futro `docs/futros/2026-10-23-m6-interface.md` (978 lines by
`/usr/bin/grep -c ''` at `a00b3354d5`; its last heading `:976`) takes a T35
kickoff addendum written by the coordinator with this version, after the T34
kickoff addendum at `:958` and the T34 proof errata at `:972`. **Milestone:** M6. **Predecessors:** T2, T20, T21, T26, T31, T32, T33 and T34 (its #1307 PL-04
and PL-05, inherited as L-28 and L-29) each routed items here by name or
named one of the 96 as context; every one is listed with its lines and its disposition in § 2
  under *Already found; do not re-find; take up*, which points back at the
  rulings below. **Beside it:** T34's lane, the other es-core slice, in
  flight on the same host; the host shared through
  `/workspace/tmp/m7-m6-host-coordination.txt` (the durable successor of
  `/tmp/m7-m6-host-coordination-20261023.txt`, which the reboot of
  2026-10-28 removed); a window for this slice is asked for on #682 and
  granted there and in that file's queue (§ 5 item 2).
- **The order's sentence is true of the membership, and this brief says
  what the title does not.** The glob is `es-core/**` as `rest`, so the 96
  are exactly es-core minus three non-rest claims: `ES-CORE BY SLICE` prints
  four rows and no unassigned one -- `96 paths 22575 lines
  (('es-core-window-input',), 'rest')`, `80 paths 21984 lines
  (('es-core-components',), 'non-rest')`, `58 paths 50840 lines
  (('es-core-utils-resources',), 'non-rest')`, `8 paths 3344 lines
  (('es-state-and-bridge',), 'non-rest')` (R1 C08). **The title and the
  `why` name three files that are not in it:** `Settings`, `SystemConf` and
  `HttpReq` are T21's (#668) by the non-rest glob
  `es:es-core/src/{Settings,SystemConf,HttpReq}.*` (`Settings.cpp`,
  `Settings.h`, `SystemConf.cpp`, `HttpReq.cpp`, `HttpReq.h` print
  `not-in-T35 non-rest [('es-state-and-bridge', 21)]`, R1 C08), so **"the
  pooled-connection trap"** (`es-code-traps.md:238`, #299, D-RA-036) is
  `HttpReq`'s stall bound and T21's context, not this slice's defect (R4
  § 8 delta 6). What the title leaves implicit: the 96 are 44 `.cpp`, 51
  `.h` and `es-core/CMakeLists.txt` (R1 C06) -- the window, the input
  manager and its config, the gun manager, the five es-core dialogs under
  `es-core/src/guis/` (six pairs: `GuiDetectDevice`, `GuiInfoPopup`,
  `GuiInputConfig`, `GuiMsgBox`, `GuiTextEditPopup`, `GuiTextEditPopupKeyboard`;
  no `GuiLoading`, which is `es-app/src/guis/`'s and T31's, R4 § 0), the
  theme parser and its storyboards, `GuiComponent`, the script runner, the
  log and its policy header, the locale, the paths, the power saver, the
  splash, the audio manager, sounds and playlists, the volume control, CEC,
  TTS, the MAME names, the image I/O, the math, the animations and the
  three watchers. **"6,759 fork-own" is the whole lines of the 13 files the
  fork touched** (R1 C07's `TIER fork-own 13 paths 6759 lines`), not the
  lines the fork wrote: the fork's own authorship over the 96 is **`13 files
  changed, 247 insertions(+), 71 deletions(-)`** (R1 C13, the same line
  against `bccd715707`, R1 C15), 19 log lines with two merges (R1 C16); the
  read's tiers are **fork-added 1 (`LogPolicy.h`), fork-modified 12,
  upstream-carried 83**, and **83 of 96 blobs are byte-identical to
  `rocknix/master`** (R1 C12). § 2 carries the figures.
- **Ownership rulings, stated once; § 2's take-up list points here.**
  **T35 owns `es-core/**` as `rest` -- the 96 paths -- and nothing else.**
  D-WORKFLOW-213 (`docs/decision-register.md:759`, T34's row) already names
  the edges from the components' side: *"the popups under
  `es-core/src/guis/`, `Window.cpp`, `ThemeData.cpp`, `GuiComponent.cpp`,
  `InputConfig.cpp`, `InputManager`, `WatchersManager.cpp`, `Scripting.cpp`
  and `es-core/CMakeLists.txt` are T35's (#682); `TextureData.cpp`,
  `TextureResource.cpp`, `Font.cpp`, `FileSystemUtil.cpp` and
  `OfflineProxyUrl.cpp` are T36's (#683); `HttpReq`, `Settings`,
  `SystemConf` and `AtomicFileUtil` are T21's (#668); `CloudText.*` is T18's
  (#665); `ScraperSearchComponent.cpp` is T33's (#680)"*; **T35's own ownership row is the coordinator's, written at dispatch** (T34's
errata `:1744`; the pointer's `Register:` line is filled from the table at
`COHASH`, § 10). The deltas R4 § 8 found where a source named another
  owner, ruled here: (a) **T2 FD-7 posted `InputManager::configureEmulators`'s
  controllers blob "for T36"** (T2 `02:62`): `InputManager.cpp` is T35's by
  the selector (R1 C08 `in-T35 rest`), so the blob's quoting half is this
  slice's Q2 and the template's half stays T3's. (b) **T2 SS-1 called
  `Platform.cpp`'s `system()` wrapper "T35's"** (T2 `02:143`):
  `es-core/src/utils/Platform.cpp` is T36's by `utils/**` and absent from
  the 96 (R4 § 8 delta 2; the futro `:191` reads it as T35's and T36's);
  T35 has nothing in it and cites `ProcessStartInfo` as T36's. (c) **T33's
  `02:730` and #1283's body call `WatchersManager.cpp` "T21's file"**: T21's
  selector holds no watcher; the lock is T35's (D-WORKFLOW-213 names it),
  and #1283's open checkbox at its body line 18 waits for this slice's
  record (§ 4 Q3). (d) **T2 FD-9 placed `Scripting` with "T33/T21"**; T33's
  `04:132` returned it to the es-core slice; it is T35's (Q5). (e)
  **`GuiLoading`** was called T35's in earlier briefs and is
  `es-app/src/guis/GuiLoading.h`, T31's (T34's erratum `:1694`). (f) **The
  pooled-connection trap** is `HttpReq`'s (T21's), above. (g) **T33's PL-25
  / #1305** (the screensaver's `FileData` list not cleared on the transfer's
  rescan path; `stage-c/pl25-screensaver.py` FAILs at the pin with a
  heap-use-after-free in the next pick, read at `947ace1966`): the rescan's
  half is T2's (`SystemData.cpp:459-473`, a stage-E patch for the
  integration), the screensaver's own list is es-app's
  (`SystemScreenSaver.cpp`, T33's), and **the window's screensaver hooks
  are T35's** -- when the list is filled and when it is cleared is decided
  at `Window.cpp:777-779` (start), `:1091-1105` (`startScreenSaver`),
  `:1107-1138` (`cancelScreenSaver`, `resetCounts` at `:1117` per the
  script's docstring), `:234-260` (controls while active) and `:792`
  (`renderScreenSaver` every frame) (R2 § 1.5; R3 § 4's `:777`, `:805`,
  `:1093-1117`): Q4's lifetime question, the fix's third half named for the
  pause. **Two collisions the integration owns, not the lane:** (h) **T21's
  `3ae9610b0`** adds five registrations to `es-core/CMakeLists.txt` --
  `src/HttpText.h`, `src/RecoveryOutcome.h`, `src/utils/DownloadFile.h`,
  `src/HttpText.cpp`, `src/utils/DownloadFile.cpp` (R1 C21) -- the one
  change any accepted lane makes to one of the 96 (R1 C20); at T21's tip
  `HttpText.{cpp,h}` and `RecoveryOutcome.h` match no non-rest es glob and
  **would fall to this slice's `rest`**, while `utils/DownloadFile.*` is
  T36's; the P1 inventory at `2174265e9c` predates them, so the 96 do not
  include them, and the lane records the CMake hunk as the integration's,
  never re-reads T21's new files as its own. (i) **Three of the nine
  doubles under `tests/app-unit/fakes/` stand in for this slice's headers**
  -- `Window.h`, `Log.h`, `LocaleES.h` (R1 C24; R3 § 1.2: `postToUiThread`
  runs at once on the posting thread, `createAsyncNotificationComponent`,
  the `LogLevel` enum, `_()` as `std::string`), written for ProxyCards'
  tests (ES `1cf15dead`) and put `BEFORE` the include path by
  `proxycards-tests`, `jobs-tests` and `bookkeeper-tests`: a T35 change to
  `Window.h`'s two signatures or to `LogLevel`'s values breaks three
  binaries' doubles and is named as a collision in the hand-back; the fakes
  are not the lane's to edit. So the earlier briefs' "T35's" was right for
  the popups and the window, and the lane writes no line outside the 96 (a
  fix in a neighbour is named for its owner at the pause).
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346, #585 or #909, or decide a question of scope:
  those are the coordinator's, reached through #682, one question at a
  time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves, with its trace and `Already written:`
  line (D-WORKFLOW-187). A fix lands only under a stream brief the
  coordinator writes at the stage-D pause, **on the EmulationStation
  branch**. The read's tiers are **fork-added 1 / fork-modified 12 /
  upstream-carried 83** (§ 2 § Three things the figures hide, (2), which
  reconciles them with the inventory's `fork-own` 13 / 6,759 lines). A
  defect in a line the fork wrote is the fork's to fix; a defect in an
  upstream line is a contained fix under `bugs-are-agent-first.md` rule 6
  (`:76`) and a #585 line (D-WORKFLOW-164, never sent, D-WORKFLOW-165).
  D-UI-079's lanes (`engineering-practices.md:12`): the surfaces the fork's
  19 commits work in -- the window's toast queue and the card's place
  (D-UI-093, `c1c0d6ddc`; `fc465b126`, `016385b52`), the message box's
  width and measure (`471e7e2e8`, `9854e7bc5`), the two text popups' CLEAR
  (`c8dc72cf9`), the log's flush and stderr mirror (`469441d4d`), the
  masked command lines (`80f52e500`), the input device scans' udev guards
  (`e6e1e4d0f`), the splash identity (`4d0c7a686`) -- are the lanes;
  **the input manager's device model and player assignment, the gun
  manager, CEC, TTS, the volume control, the audio manager and the
  playlists, the theme parser and the storyboards, the math, the watchers'
  thread, `processStorageRequest`'s dialogs, the screensaver hooks, the
  power saver, the on-screen keyboard's three layouts and the input-config
  flow are upstream surfaces** read for brittleness and cost (the lens) and
  left as upstream has them, and a defect in one is still ours to close
  when the fix is contained (rule 6). The read is the pin `16dbac5211`'s
  bytes; M7's worktrees are never read.
- **Two worktrees, one session, and four placeholders.** The distribution's
  `feature/m6-es-core-window-input-682` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-window-input-682`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** (`origin/feature/m6-p1-survey-641` resolves to
  `2174265e9c` in the coordinator worktree, read 2026-10-30 14:45 UTC; or
  the P1 tip the dispatch comment names) with the coordinator's tip merged
  in and the lane's pointer seeded; and the EmulationStation fork's
  `feature/m6-es-core-window-input-682` at
  `W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-window-input-682`,
  cut by the coordinator from **the pin
  `16dbac5211eea7e70db7394372033be2be7df829`** and clean until stage E: the
  sources are read and the fixes are made there, and the pin is not moved
  by the lane. **`W` is that one path in every block of this brief, § 5's
  runs included; until it exists -- neither worktree does before dispatch:
  `ls -d` of both paths printed `No such file or directory` and `git -C
  <qa-integration> rev-parse --verify origin/feature/m6-es-core-window-input-682`
  printed `fatal: Needed a single revision` on 2026-10-30 -- the
  `qa-integration` checkout at the same pin, clean, stands in, read by `git
  -C` only, and gives the same lines (every quoted ES line in R1, R2 and R3
  was printed there).** **Four placeholders stand in this brief for hashes
  that do not exist until dispatch:** `COHASH` (the coordinator's tip merged
  into the lane's branch), `MERGE_HASH` (that merge commit, the lane's
  dispatch tip), `TIPHASH` (the lane's own tip as it moves; at stage A it is
  `MERGE_HASH`) and `V2HASH` (this brief's commit on the coordinator's
  branch at dispatch, version 2 after the proof; version 1 has no dispatch
  hash). The dispatch comment on #682 and the seeded pointer carry their
  values; the lane reads them there, never guesses them, and § 9's
  placeholder check names all four. **One earlier lane's ES branch touches one of the 96** (R1 C20; the proof's
re-read of 2026-10-31 the same): of the nine tips only **T21 `3ae9610b0f`**
differs inside the 96, in `es-core/CMakeLists.txt` (`1 file changed, 5
insertions(+)`, ruling (h) above; its other 14 es-core files are its own,
five new files and T36's `FileSystemUtil.cpp`); T20's and T26's es-core
changes are T21's and T36's files; T34's `feature/m6-es-core-components-681`
is the pin itself (0 ahead; its `origin/` ref prints `fatal:`, recorded). So
the integration has one lane-on-lane hunk inside the slice, named and not a
stop (§ 8). The other ES checkouts
  under `~/Development/emulationstation-next.worktrees/` are read with `git
  -C <checkout> show <hash>:<path>` only, and nothing is fetched (§ 10; the
  stale `upstream/master` is § 2's). Until the dispatch comment exists the
  pointer is not seeded and nothing starts.
- **Depth: Independent** -- one seat from another lab (plan § 6c,
  D-WORKFLOW-137; `adversarial-council.md`: an Anthropic-led audit's
  reviewer is pinned GPT-6 Astra; no Gemini seat): Astra at `max` over a
  trimmed, scanned packet (D-WORKFLOW-195 -- **the 13 fork-added and
  fork-modified files whole** (6,759 lines by `grep -c ''`, the inventory's
  rule, R1 C07, which the lane replaces with the packet's own `wc -l`)
  **and of the 83 upstream-carried files only the ranges the questions
  cite**; the manifest names every trimmed file and range; nothing in the
  96 is a binary), a probe then one refutation (one in-call retry allowed);
  `review-plan.json` records depth `independent` and the one reviewer with
  its served model; **exactly two keyed `tools/council/run invoke` calls**,
  every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`
  (the runner reads that variable at `tools/council/run:21`, default
  `~/.config/council/env`; the recipe is `.claude/skills/council/SKILL.md`
  and its `references/`; the runtime under `tools/council/` from `npm
  install --offline`, no fetch). The packet is scanned before it leaves.
  **What the scan will hit inside the 96, so the lane dispositions rather
  than stops:** R2 read no credential-shaped line in any of the 96 and
  masked every quoted log line as it went (R2 cmd 8, cmd 11); the expected
  hits are identifiers and macro names -- `InputConfig.h`'s and
  `InputManager.cpp`'s `SDL_Keycode`/`SDLK_*` and `getKeyName`-shaped names,
  `GuiTextEditPopupKeyboard.cpp`'s key-button vocabulary, `Window.cpp`'s
  four Ctrl debug toggles (`:262-281`), the `maskSecrets` call sites at
  `Scripting.cpp:49`, `:122`, `:129` and `InputManager.cpp:1270`, `:1486`
  (a function name beside the words it masks, R2 § 0), `LogPolicy.h`'s
  level tags -- so `packet-manifest.json` records **every scan hit
  dispositioned by file:line** (library plumbing / macro name / identifier
  / setting name / value), and a hit that is a value stops the packet; no
  value ever reaches the packet or an artifact.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A. **The session is the T5 session (`m6-t5-build-engine`), after
  T33's close-out** (T34's errata `:1745`: *"the T5 session takes T35 after
  T33"*; T33 handed back at 14:40 UTC 2026-10-30 and its acceptance run
  started at 14:42 UTC on #680).
- **The first commands** (stage A, in the distribution worktree;
  `8ebaf8daad` is `next`'s commit the P1 branch stacks on and `651150fc88`
  is `upstream/next`'s, both copied from T34's brief `:250-256`, which read
  them again in the coordinator worktree on 2026-10-30: `651150fc88` is
  *Merge pull request #3547 from spycat88/qcom-bls*, `8ebaf8daad` is
  *browser: record provider pages and GTK4 compilation (#616)*):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-core-window-input-682
cat .github/sessions/saved-session-state-feature-m6-es-core-window-input-682.md   # the pointer: the dispatch's two hashes; § 10 names the lines to check
git status --short | wc -l                                                   # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1               # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-window-input-682; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                # the pin; 0
git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10                     # cada856d86: the merge base with ROCKNIX's master (bccd715707 is its parent, § 2; R1 C15)
git -C "$W" rev-parse --verify rocknix/master | cut -c1-10                    # f6c542872e, read from the shared refs (R1 C15)
git -C "$W" rev-parse --verify batocera/master | cut -c1-10                   # b2ceb55a7e, read from the shared refs; context only (R1 C17)
git -C "$W" merge-base "$PIN" batocera/master | cut -c1-10                    # 1750dded8c: ROCKNIX has merged nothing from batocera since 2026-09-13 (R1 C17)
for b in m6-es-launch-path-649 m6-es-cloud-pages-665 m6-es-achievements-pages-667 m6-es-state-and-bridge-668 m6-es-guimenu-673 m6-es-pages-678 m6-es-app-views-scrapers-679 m6-es-app-system-680 m6-es-core-components-681; do printf '%s ' "$b"; git -C "$W" rev-parse --verify "origin/feature/$b" 2>&1 | cut -c1-10; done   # nine tips (T33's `f802c55c62` since 2026-10-30; T34's had no origin ref at R1's read, R1 C19: a `fatal:` line there is recorded, not a stop)
tools/register-check >/dev/null && echo register-ok
date -u +%H:%M:%S; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200   # who holds the host, with the time of the read (M7 writes timestamped lines: read the whole tail); no guest before a grant on #682
```

Every ES line above printed what its comment says on 2026-10-30 by `git -C`
against `qa-integration` (R1 C15, C17, C19); the `cat` cannot run before the
pointer is seeded, and `W` does not exist before dispatch; the `stacked`, `upstream-next-is-here` and `register-ok` lines printed for
the proof on 2026-10-31 (in the P1 clone and the coordinator worktree; the
lane prints its own). The host file's tail is
whatever the host is doing at the moment of the read, so the lane records
the time beside the lines; a sentence about what the tail "shows today" is
never written into an artifact without one.

## 2. Scope

**The membership, by the block that defines it** (run from the lane's
distribution worktree, stacked on the P1 branch, which holds
`docs/reviews/{inventory.json,slices.json}`; the script is T34's
`membership.py` with three lines changed -- the slice id in `hits`, the
`named` list and the `in-T35` label; the `ES-CORE BY SLICE` prefix is
unchanged; two keyword arguments are spaced `key = lambda` so this file
carries no key-equals token. **The heredoc is saved once and run twice** --
first against `/dev/null` to make the paths file from its own TSV, then
against that file to prove equality; R1 ran both passes on 2026-10-30 with
the two JSONs read by `git show 2174265e9c:` into scratch (its variant
takes the JSON directory as a second argument, R1 C03; the lane's reads
them from its worktree as below), and the expected lines are that run's,
byte for byte (R1 C04, C05). The awk reads columns 1 and 2, `tree` and
`path`, the inventory's first two by its own `columns:` line):

```bash
mkdir -p .qa-scratch/t35
cat > .qa-scratch/t35/membership.py <<'PYEOF'
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
    if h==["es-core-window-input"]: mine.append(r)
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
named=["es-core/src/Window.cpp","es-core/src/Window.h","es-core/src/InputManager.cpp","es-core/src/InputConfig.cpp","es-core/src/GuiComponent.cpp","es-core/src/ThemeData.cpp","es-core/src/Scripting.cpp","es-core/src/Log.cpp","es-core/src/guis/GuiMsgBox.cpp","es-core/src/guis/GuiTextEditPopupKeyboard.cpp","es-core/src/guis/GuiInfoPopup.cpp","es-core/src/watchers/WatchersManager.cpp","es-core/CMakeLists.txt","es-core/src/Settings.cpp","es-core/src/Settings.h","es-core/src/SystemConf.cpp","es-core/src/HttpReq.cpp","es-core/src/HttpReq.h","es-core/src/utils/AtomicFileUtil.cpp","es-core/src/utils/AtomicFileUtil.h","es-core/src/components/MenuComponent.cpp","es-core/src/components/AsyncNotificationComponent.cpp","es-core/src/utils/FileSystemUtil.cpp","es-core/src/utils/StringUtil.cpp","es-core/src/resources/Font.cpp","es-core/src/renderers/Renderer.cpp","es-core/src/utils/OfflineProxyUrl.cpp","es-app/src/CloudText.cpp","es-app/src/main.cpp","es-app/src/ApiSystem.cpp"]
byp={r["path"]:r for r in rows if r["tree"]=="es"}
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY"); continue
    h,kind=hits(r); print(p, "in-T35" if p in got else "not-in-T35", kind, [(x,kof[x]) for x in h], "tier",r["tier"],"lines",r["lines"],"area",r["area"])
print("ES-CORE BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["tree"]=="es" and r["path"].startswith("es-core/"):
        h,kind=hits(r); cnt[(tuple(h),kind)]+=1; ln[(tuple(h),kind)]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:-kv[1]): print(v,"paths",ln[k],"lines",k)
PYEOF
python3 -I .qa-scratch/t35/membership.py /dev/null > .qa-scratch/t35/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^CLAIMS$/{p=0} p && $1=="es" {print $2}' .qa-scratch/t35/block-1.txt > .qa-scratch/t35/paths.txt
wc -l .qa-scratch/t35/paths.txt                                             # 96 (R1 C04)
python3 -I .qa-scratch/t35/membership.py .qa-scratch/t35/paths.txt > .qa-scratch/t35/block-2.txt
/usr/bin/grep -E '^(mine:|only-|lines:|fork-own lines:|read lines:)' .qa-scratch/t35/block-2.txt
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-window-input-682; PIN=16dbac5211eea7e70db7394372033be2be7df829; MB=cada856d86
for p in $(cat .qa-scratch/t35/paths.txt); do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l", s}'                  # wc -l 22567 (R1 C11)
for p in $(cat .qa-scratch/t35/paths.txt); do git -C "$W" show "$PIN:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c", s}'   # grep -c 22575 (R1 C11)
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t35/paths.txt | wc -l   # every path but LogPolicy.h (R1 C12's `N N N N` row); the count is the lane's line
while IFS= read -r p; do git -C "$W" cat-file -e "bccd715707:$p" 2>/dev/null && echo "IN BASE: $p"; done < .qa-scratch/t35/paths.txt | wc -l   # the same set
git -C "$W" diff --shortstat "$MB" "$PIN" -- $(cat .qa-scratch/t35/paths.txt)           # 13 files changed, 247 insertions(+), 71 deletions(-) (R1 C13)
git -C "$W" diff --shortstat bccd715707 "$PIN" -- $(cat .qa-scratch/t35/paths.txt)     # the same line (R1 C15)
```

Expected, at `2174265e9c` (the first pass, against `/dev/null`, prints
`mine: 96 paths.txt: 0 equal: False` with every path under `only-mine`, R1
C04; the second prints these five lines byte for byte, R1 C05):

```
mine: 96 paths.txt: 96 equal: True
only-mine: []
only-paths.txt: []
lines: 22575 reach: {'shipped': 96} tier: {'fork-own': 13, 'upstream-carried': 83} lang: {'cmake': 1, 'c-header': 51, 'c++': 44}
fork-own lines: 6759
read lines: 22575
```

then, under `CLAIMS`, the 30 named paths with their claimant (R1 C08; the
proof re-printed every row): the thirteen of this slice `in-T35 rest
[('es-core-window-input', 35)]` (their tiers and lines are the table's),
`Settings.cpp`, `Settings.h`, `SystemConf.cpp`, `HttpReq.cpp`, `HttpReq.h`,
`utils/AtomicFileUtil.{cpp,h}` and `es-app/src/ApiSystem.cpp` `not-in-T35
non-rest [('es-state-and-bridge', 21)]`, `components/MenuComponent.cpp` and
`components/AsyncNotificationComponent.cpp` `[('es-core-components', 34)]`,
`utils/FileSystemUtil.cpp`, `utils/StringUtil.cpp`, `resources/Font.cpp`,
`renderers/Renderer.cpp` and `utils/OfflineProxyUrl.cpp`
`[('es-core-utils-resources', 36)]`, `es-app/src/CloudText.cpp`
`[('es-cloud-pages', 18)]`, `es-app/src/main.cpp` `[('es-launch-path', 2)]`,
`es-app/src/guis/GuiLoading.h` `[('es-pages', 31)]` and
`es-core/src/guis/GuiLoading.h` `NOT IN INVENTORY`; and under `ES-CORE BY
SLICE` the four rows of § 1. Then the ES lines: `wc -l
22567`, `grep -c 22575`, the two `cat-file` counts, and the shortstat line
twice.

**Three things the figures hide, settled here so the lane does not
re-derive them.** (1) **The inventory counts lines as `grep -c ''` does**
over the 96 files, the unterminated last line included (`git diff-tree
--numstat` against the empty tree, `tools/renovation-inventory` at
`2174265e9c`, R1 C10): **eight slice files end without a newline** --
`MultiStateInput.cpp` 52/53, `MultiStateInput.h` 18/19,
`anim/StoryboardAnimator.cpp` 236/237, `anim/ThemeAnimation.h` 145/146,
`anim/ThemeStoryboard.cpp` 241/242, `math/Vector2f.cpp` 38/39,
`math/Vector4f.cpp` 106/107, `watchers/BatteryLevelWatcher.cpp` 8/9 (R1
C11's `<- no trailing newline` rows) -- so `wc -l` sums to **22,567** and
`grep -c ''` to **22,575** (R1 C11's `TOTAL` lines), the same bytes, two
counting rules; a figure in `02` says which. The order's *"22,575 read"* is
every line: all 96 are `c++`, `c-header` or `cmake`, shipped, none
vendor-carried (R1 C05). The same two rules reach every count in this
brief: `git grep -c` counts **lines** and `git grep -o | wc -l` counts
**occurrences**, and § 5 states the line form for `_("` (86 lines, R2 cmd
8) and `exists(` (41 lines, R2 cmd 12); the occurrence forms are the lane's
first lines. (2) **"6,759 fork-own" is the lines of the 13 files the fork
touched, not the lines the fork wrote.** The inventory's `tier` is per
file (R1 C10: *"fork-own is `git diff --name-only <merge-base> HEAD`"*), so
`Window.cpp` counts whole (1656) for a 55-line stat, `InputManager.cpp`
whole (1552) for 7, `GunManager.cpp` whole (1057) for 2 (R1 § 2); the
fork's own change over the 96 is **`13 files changed, 247 insertions(+),
71 deletions(-)`** (R1 C13 against `cada856d86`, C15 the same line against
`bccd715707`; `--name-status` `1 A` + `12 M`, R1 C15). The 13 by the stat's own columns are the table's *Fork stat* column (R1
C13); the `+/-` split per file by `--numstat` (the proof): `CMakeLists.txt`
7/0, `GunManager.cpp` 2/0, `InputConfig.cpp` 8/1, `InputManager.cpp` 5/2,
`Log.cpp` 19/40, `LogPolicy.h` 55/0, `Scripting.cpp` 3/3, `Splash.h` 4/1,
`Window.cpp` 49/6, `Window.h` 2/0, `guis/GuiMsgBox.cpp` 78/3,
`guis/GuiTextEditPopup.cpp` 1/1, `guis/GuiTextEditPopupKeyboard.cpp` 14/14.
**`ThemeData.cpp`,
`GuiComponent.cpp`, `GuiInfoPopup.cpp`, `GuiInputConfig.cpp`,
`GuiDetectDevice.cpp` and `watchers/WatchersManager.cpp` carry no fork
hunk** (R2 § 0). Six pairs have one half modified and the other not
(`Window` both; `InputConfig.cpp`, `InputManager.cpp`, `GunManager.cpp`,
`Log.cpp`, `Scripting.cpp`, `GuiMsgBox.cpp`, `GuiTextEditPopup.cpp`,
`GuiTextEditPopupKeyboard.cpp` with their `.h` untouched; `Splash.h` with
its `.cpp` untouched). So the read's tiers are **fork-added 1,
fork-modified 12, upstream-carried 83** (R1 C12's `CLASS` lines), and `02`
§ Coverage carries both tiers. One row to know about:
`guis/GuiTextEditPopupKeyboard.h` is upstream-carried and byte-identical to
the merge base while the inventory records a fork commit on it
(`last_fork_commit 1593c299f3 2026-09-10`, R1 C07): the fork touched it and
the touch is no longer a difference; recorded, not pursued. (3) **The
bases** (R1 C15, C17). `rocknix/master` is `f6c542872e` (2026-10-23, *Merge
pull request #54 from porschemad911/s922x-suspend*); the pin's merge base
with it is `cada856d86e3115fbbf0bce09dd761b0ee8fa9fd` (2026-09-23, *Refactor
wifi menu and add support for saving multiple profiles*), and `bccd715707`
(2026-09-22, *Show all ip addresses in network settings*) is its ancestor
and the base every earlier ES brief named (T34's brief `:473-477`:
`rev-list --count bccd715707..cada856d86` = 1; `bccd715707..PIN` = 725;
`cada856d86..rocknix/master` = 14; the stale `upstream/master` ref 15
behind, the same pin and refs); for this slice the difference is nothing:
the shortstat is the same line against both (above). `batocera/master` is
`b2ceb55a7e` (2026-10-21, *update po*) and its merge base with the pin is
`1750dded8c0fdff70630026f756a69fcad0bb995` (2026-09-13, *update po*), so
ROCKNIX has merged nothing from batocera since then. This paragraph is the
one statement of the bases; § 1's comments, § 5's expectations and § 7's
checkbox cite it.

**Merge debt: none on the 96** -- every one of the 83 upstream-carried files
is byte-identical to `rocknix/master` **and** to the merge base (`Y Y Y Y |
Y Y`, R1 C12; `IDENTICAL to rocknix/master 83`), and what separates the pin
from `rocknix/master` is the fork's own 13 files reversed (`13 files
changed, 71 insertions(+), 247 deletions(-)`, R1 C14; `--name-status` `1 D`
+ `12 M`, R1 C15), so upstream has moved none of the 96 since
`cada856d86`; the count of upstream commits on the 96 since the base is **0** (`git log
--format=%h cada856d86..rocknix/master -- <96> | grep -c .` prints `0`, rc 1
-- the proof; 14 commits on any path). The
record in `02` § The merge debt is one line (§ 6), not a table.
**Batocera's twelve commits on the 96 since `1750dded8c`** (R1 C17: `12`;
35 on `es-core/` as a whole) are **a reconciliation list for the
integration, not this slice's debt**, named in `02` § The merge debt's one
line as *not ROCKNIX's*, never a debt figure and never fetched (R1 C18):
`dbabd1adf` 2026-10-16 *write the players' resolved input configs for the
launcher*, `308221458` 2026-10-16 *fix zoom into the game art at launch -
fix bios check threading*, `d3b2d9192` 2026-10-16 *use pipewire for the
menu sounds to fix game start & kodi transition issue*, `98c19243e`
2026-10-15 *fix: helps merge*, `08ca272cb` 2026-10-10 *Fix Linux logger
build*, `a61c25f6b` 2026-10-05 (merge, chihiro mame names), `e75039fe9`
2026-10-05 *Virtual device - additional fix for wiimote4guns virtual
device*, `8f3ccae2e` 2026-10-04 *chihiro, namco2x6 names and flags, fix
flagless arcade names*, `ab218fba1` 2026-10-02 *load slow menu option lists
in the background and fix asan errors*, `ad104860f` 2026-09-30 *Fix rtl
aligments*, `33016e55f` 2026-09-27 *install the SIGTERM handler when logging
is disabled*, `473b4abb5` 2026-09-25 *[WIN32] Ignore VHF virtual HID devices
in lightgun detection*; they touch **nine of the 96** -- `GunManager.cpp`
83, `InputManager.cpp` 11, `Log.cpp` 17, `Window.cpp` 17, `GuiMsgBox.cpp`
17, `MameNames.cpp` 6, `AudioManager.cpp` 4, `Window.h` 2,
`animations/Animation.h` 1 (`9 files changed, 135 insertions(+), 23
deletions(-)`, R1 C18) -- and the files both batocera and the fork changed
are **`GunManager.cpp`, `InputManager.cpp`, `Log.cpp`, `Window.cpp`,
`Window.h` and `GuiMsgBox.cpp`** (R1 § 3's reading of C13 against C18, the
set § 5's `comm -12` run prints); `MameNames.cpp`, `AudioManager.cpp` and
`Animation.h` are batocera-only. The first group is where a future rocknix
merge of batocera meets the fork's edits: the input configs written for the
launcher (`dbabd1adf`) against the fork's udev guards, the SIGTERM handler
(`33016e55f`) and the logger build fix (`08ca272cb`) against the fork's
per-batch flush, the two `Window` and `GuiMsgBox` hunks against D-UI-093
and the wide box -- the hunk ranges are the lane's read, not re-derived
here. The pin-to-`batocera/master` distance over the 96 (`20 files
changed, 258 insertions(+), 345 deletions(-)`, R1 C17) mixes batocera's
moves with the fork's and with rocknix's divergence, and is quoted only as
the tool's line.

**The files, read whole** (lines at the pin by `grep -c ''`, the
inventory's rule, R1 C07/C11; the fork's stat column from R1 C13, which
equals the base's for every row; every `.cpp` of this slice is named once in `es-core/CMakeLists.txt`
unconditionally -- `CORE_SOURCES` `:146-276`, the top-level sources at
`:147-172`, the only `if(` at `:278` (GLES 3.0) and `:287` (MSVC), R3 cmd
21; seven entries carry a trailing `# batocera` comment and two headers,
`HelpPrompt.h` and `Scripting.h`, are registered nowhere (the proof) -- so
no per-file CMake column; the per-file fork-commit list is the lane's `git log
--oneline bccd715707..PIN -- <file>` (R1 C16 attributes the 19 subjects by
their text, which the table repeats where it does); the 13 fork-touched
files one row each, the 83 upstream-carried grouped by what they are; a
neighbour outside the 96 is written with its owner the first time it
appears):

| File | Lines | Fork stat | Fork commits R1 C16 attributes | What it is at the pin |
| --- | ---: | ---: | --- | --- |
| `es-core/CMakeLists.txt` | 303 | 7 + | `0ec3f43ae` (the offline proxy's store, `OfflineProxyUrl` registered), `469441d4d` (`LogPolicy.h`), the `AtomicFileUtil`/`TimeText` registrations (`b0e417df3`, `8b7340f5b`), the merge `2dae87308` (the per-file log, the proof) | `CORE_HEADERS`/`CORE_SOURCES`: the fork adds `LogPolicy.h`, `utils/AtomicFileUtil.{h,cpp}`, `utils/TimeText.{h,cpp}`, `utils/OfflineProxyUrl.{h,cpp}` (hunks at `@@ -14`, `@@ -118`, `@@ -250`, R2 § 0; the utils files are T36's, the list lines this slice's); every T35 `.cpp` named once and unconditionally (R3 cmd 21; the named-once loop prints 9 for seven `# batocera` comments and the two unregistered headers, the proof); `find_package(udev)` / `if(UDEV_FOUND) add_definitions(-DHAVE_UDEV)` is the top-level `CMakeLists.txt:255-258`, not this file (R3 § 2.2); **T21's `3ae9610b0` adds five lines** (§ 1 h) |
| `Window.cpp` / `Window.h` | 1656 / 197 | 55 ++- / 2 + | `c1c0d6ddc` (D-UI-093, fork #283), `fc465b126` (boot pointers settled before sync, cards waited for), `016385b52` (one card near full width) | the frame: `update` `:450-560` (posted functions `:464`, toasts `:466`, the top GUI alone `:542-543`, cards `:556-557`) and `render` `:689-937` (bottom and top of the stack only `:695-737`; a `GuiMsgBox` or a `"popup"`-tagged top draws the page beneath `:722-727`; **the help bar only when `mGuiStack.size() < 2 \|\| !fullScreenMenus()` `:743-745`**; popups then cards while no screensaver `:782-788`); the surface queue (§ 4 Q1): one file-static mutex `:293`, `notificationDuration` `:298-309`, `displayNotificationMessage` `:311-321`, `processNotificationMessages` `:324-351` (**returns while any card is up `:336-337`; pops one from the back `:339-340`**), `layoutNotificationPopups` `:396-416`, `createAsyncNotificationComponent` `:1152-1175` (**re-queues a running toast's words with a fresh default duration `:1164`**, stops the popups `:1165`), `hasAsyncNotifications` `:1146-1150` (h `:101`), `renderAsyncNotifications` `:1177-1234` (**centred `posX = W*0.5 - w*0.5` `:1192`**, stacked `:1194`, `:1231`, the slide-up `:1203-1215`, the fade-in `:1217-1221`), `updateAsyncNotifications` `:1236-1260` (**the one place a card is freed `:1246-1248`**); `deinit` `:188-207` and `~Window` `:49-63` **never touch the cards, the popups or the queue**; input `:215-290` (`FirstJoystickOnly` `:220-232`, screensaver controls `:234-260`, **four keyboard-only Ctrl debug toggles with the `"Debug"` gate commented out `:262-281`**, the top GUI alone `:287-288`); the help prompts `setHelpPrompts` `:1005-1078`, `renderHelpPromptsEarly` `:999-1003`; the screensaver hooks `:777-779`, `:803-813`, `:1081-1144` (§ 4 Q4, #1305); `postToUiThread` `:1276-1290`, `processPostedFunctions` `:1292-1307`, **`unregisterPostedFunctions` `:1262-1274` without the lock**; `processStorageRequest` `:1493-1656` with **four `std::thread(...).detach()` capturing `this`** and **`#include "../es-app/src/ApiSystem.h"` `:29`**, its dialogs in upstream's sentence case (D-UI-079); the containers `Window.h:123`, `:135`, `:153-154` (R2 § 1) |
| `InputManager.cpp` (`.h` upstream, 109) | 1552 | 7 ++- | `e6e1e4d0f` (udev scans released), `80f52e500` (masked log lines), the merge `370ebe416` | `init` `:76-105`, `deinit` `:153-196`; `parseEvent` `:643-887` (**`SDL_JOYDEVICEADDED` rebuilds every joystick `:849-853` then toasts `%s connected` `:854-860`; `REMOVED` toasts then rebuilds `:864-877`**; F4 pushes `SDL_QUIT` with a `new SDL_Event()` never freed `:792-800`); `rebuildAllJoysticks` `:374-630` (**`mJoysticksLock` held `:485-623`; `writeDeviceConfig` called from inside the hot-plug rebuild `:605`** under `#if !defined(BATOCERA) \|\| !defined(ROCKNIX)` `:585`); the config file (§ 4 Q2): `loadInputConfig` `:1113-1141`, `tryLoadInputConfig` `:889-972` (cached `exists` `:893`; the two "Approximative device found" logs read a null node `:946`, `:960`), **`writeDeviceConfig` `:1179-1240` writing `es_input.cfg` and `es_last_input.cfg` in place by pugixml `save_file` `:1225`, `:1232`** after a merge gated on cached `exists` `:1187`, firing `config-changed`/`controls-changed` `:1234-1235`, **`doOnFinish` `:1242-1284` running every `<inputAction type="onfinish">` `<command>` synchronously on the UI thread through `ProcessStartInfo(...).run()` `:1272`**; `loadFromSdlMapping` `:1004-1111` (`select` copied to `hotkey` `:1101-1108`); player assignment `computePlayersConfigs` `:1341-1472`; the fork's udev null guard and `udev_enumerate_unref` `:120`, `:145`, masked lines `:1270`, `:1486`; the file-static `mJoysticksLock` `:52`; `<SDL.h>` `:11`, `<libudev.h>` `:26` under `HAVE_UDEV` (R2 § 2; R3 § 2.2) |
| `InputConfig.cpp` (`.h` upstream, 176) | 446 | 9 ++- | `e6e1e4d0f` | the per-device mapping: the constructor calls udev twice per device on `HAVE_UDEV` (`isWheel` `:131`, `getDeviceParentSyspath` `:132`) with the fork's guards on every return (`:72`, `:89`, `:100`, `:109`, `:114`, `:148`, `:169`); `mapInput` lower-cases (`hotkeyenable`, `:186-189`); `isMappedTo` `:210-231`, `isMappedLike` `:233-248`, `getMappedTo` `:250-283`; `loadFromXML` `:285-309` (unknown type skipped with `LogError` `:297`, value 0 warned `:305`), `writeToXML` `:311-345`; `BUTTON_OK`/`BUTTON_BACK` mutable globals `:347-351` swapped by `AssignActionButtons` `:403-414`; **`buttonLabel` `:353-366` returns the key unchanged** (T34 L-01's chain); `.h:6` `<SDL_joystick.h>`, `:7` `<SDL_keyboard.h>`, `:5` `<CECInput.h>` -- the header every stand-in run meets first (R4 item 25) |
| `GunManager.cpp` (`.h` upstream, 155) | 1057 | 2 + | `e6e1e4d0f` | the light guns over udev: the monitor `:167-193`, `updateGuns(Window*)` `:514` polling `poll(..., 0)` `:922-930`, `readGunEvents` `:206`, `isReplacingMouse` `:855` (read by `InputManager.cpp:757`, `:770`), `udev_addGun` opening the evdev node `O_RDONLY \| O_NONBLOCK` `:974` and six `ioctl`s `:978-991`, `udev_closeGun` `:1011-1012`; connected/disconnected toasts `:686`, `:703`, `:724`, `:734`, `:1004`, `:1031` (six of the 86 `_("` lines); the fork's guard and unref in `udev_initial_gunsList` `:941`, `:960`; **no thread** (R2 cmd 10); `<SDL_syswm.h>` `:25` under `#elif WIN32` (R3 § 2.2); batocera's 83-line change here is the largest of its nine (R1 C18) |
| `Log.cpp` / `LogPolicy.h` (`Log.h` upstream, 56) | 322 / 55 | 59 ++--- / 55 +++ (new) | `469441d4d` (fork #178) | the async logger: `AsyncLogger::workerLoop` on `std::thread` `:60`, `:180`; **the file flushed every batch** (the comment *"Every batch reaches the file before the worker sleeps again"*, R2 § 0); `std::ofstream mFile` `:179`; `LogPolicy.h:1-55` whole: `levelTag`, `parseLogLevel`, `mirrorToStderr` (WARNING and ERROR always to stderr, every line at debug) pulled into a header so a unit test can hold them -- **the one of the 96 with a direct test** (`es-app/tests/unit/LogPolicyTests.cpp:13`, R1 C24, R3 § 1.1); `<SDL_timer.h>` `:11`; `Log.h` is doubled by `tests/app-unit/fakes/Log.h` (§ 1 i); the signal handler's backtrace of #246 is this file's (R3 § 2.2's "natural first T35 binary") |
| `Scripting.cpp` (`.h` upstream, 13) | 209 | 6 +- | `80f52e500` (fork #177) | the event hooks: `fireEvent` `:153-208` -- **per-event directories `:158-179`** (`<user ES>/scripts/<event>`, `<exe dir>/scripts/<event>`, `/var/run/emulationstation/scripts/<event>` `:160-164`; **every entry runs, the extension filter `:172-176` is WIN32-only**), then **single scripts `:182-207`** filtered to `.exe .cmd .bat .ps1 .sh .py` `:151`, `:201-203`, called with the event name first `:205`, the directory's `exists` cached `:193`; `executeScript` `:88-149` **quotes the script path only when it has a space `:92-93`, strips `"` from arguments and quotes them only when they contain a space `:98-113`**, `waitForExit` only for `quit` `:142`, stdout/stderr to `es_script_stdout.log`/`es_script_stderr.log` `:145-146`, `psi.run()` `:147` (`ProcessStartInfo` is `utils/Platform`, T36's); the fork masks the three WIN32-branch log lines `:49`, `:122`, `:129`, the Linux branch `:138` logs the path only; the WIN32 queue thread `:17-73` (R2 § 5.1; T2 FD-9/FD-19) |
| `Splash.h` (`.cpp` upstream, 337) | 44 | 5 +- | `4d0c7a686` (lowercase pixelelated, the LCD wordmark), `975235429` (Rasteratops and manual updates) | `#if defined(ROCKNIX)` -> `DEFAULT_SPLASH_IMAGE ":/pixelelated-wordmark.svg"`, `OLD_SPLASH_LAYOUT true` `:10-12` (R2 § 0); `Splash.cpp:7` `<SDL_events.h>`; the one `-DROCKNIX` branch R3 § 3.2 asks the lane to grep for sits here |
| `guis/GuiMsgBox.cpp` (`.h` upstream, 61) | 299 | 81 +++- | `471e7e2e8` (measured at the drawn width, #48), `9854e7bc5` (the wide box past four lines), `62e45ea6f` (the restore page) | the one-to-three-button dialog: **the back-button accelerator `:116-134`** (one button -> it `:117-120`; else the first whose upper-cased text equals `_("OK")` or `_("NO")` `:123-130`; **else the last `:132-133`**), fired by an unconfigured keyboard's RETURN/ESC/SPACE `:249-254`, `BUTTON_BACK`, or any `TYPE_BUTTON` from an unconfigured pad `:257-261`; `MSGBOX_WIDTH` 0.6 / `MSGBOX_WIDE_WIDTH` 0.8 / `MSGBOX_WIDE_LINES` 4 `:21-23`, `minWidth` 0.3 `:53`, the `tailscale.com` message at 0.9 and no icon `:88-91` (upstream ROCKNIX), icon selection `:59-86`, none on a small screen `:92`; the wide switch measured with the message's font `:140-150`; **the height measured at the drawn width `:198-203`** (`es-code-traps.md:96-98`) with the 1.225 factor `:204`; taller than the screen -> vertical autoscroll and full-screen size `:206-224`; `deleteMeAndCall` `:286-294` copies the callback, `delete this` `:289`, then calls it (T26's invariant); `getHelpPrompts` `:296-299` -> `mGrid.getHelpPrompts()` (the D-UI-034 fix is `ComponentGrid`'s, T34's); `TextToSpeech::say` three times in the constructor: `:44` and `:234` the text, `:240` the focused button's label (R2 § 4.1; the proof) |
| `guis/GuiTextEditPopup.cpp` (`.h` upstream, 33) | 86 | 2 +- | `c8dc72cf9` (`RESET` -> `CLEAR`) | the plain text popup: tag `"popup"` `:12`; buttons accept / `CLEAR` / `CANCEL` `:33-35`; grid 1x3 `:10`; 0.5 W `:48`; `BACK` deletes `:72-76`; `getHelpPrompts` `:81-86`; **no masking mode** (`.h:15-16`; T21 PL-26 / #1192) |
| `guis/GuiTextEditPopupKeyboard.cpp` (`.h` upstream, 57) | 533 | 28 ++--- | `c8dc72cf9` (`RESET` -> `CLEAR` in the three layouts, the help prompt and `makeButton`), `1593c299f`, `6d8764ec6` (the hostname keyboard); the `.h`'s two touches (`1593c299f`, `6d8764ec6`) are no longer a difference (R1 C12) | the on-screen keyboard: **its own `#define BUTTON_GRID_HORIZ_PADDING (Renderer::getScreenWidth()*0.0052083333)` `:14`, used at `:220`** as a quarter per side of each key's padding, against `MenuComponent.cpp:14`'s 0.022 (T34 L-05); `OSK_WIDTH`/`OSK_HEIGHT` full-screen under `fullScreenMenus()` else 0.78 / 0.60 `:8-9`; tag `"popup"` `:103`; `kbUs` `:17-43`, `kbFr` `:45-70`, `kbKr` `:72-97` chosen from `system.language` `:141-152`; glyphs for DEL, OK, newline `:169-192`; `_()` on multi-letter keys `:198-204`; `input` `:335-400`: `start` = OK `:341-348`, keyboard ESC closes `:350-354`, `BUTTON_BACK` closes `:357-361`, `leftshoulder` backspace `:364-373`, `rightshoulder` space `:376-386`, `y` shift `:389-390`, **`x` commits `""` and deletes the popup with no confirmation `:392-397`** (its prompt reads `CLEAR` `:453-454`); `makeButton` `:464-533`; **no masking mode** (`.h:13-14`; #1192) (R2 § 4.3) |
| the dialogs upstream-carried: `guis/GuiInfoPopup.cpp` / `.h`; `guis/GuiInputConfig.cpp` / `.h`; `guis/GuiDetectDevice.cpp` / `.h` | 115 / 37; 433 / 72; 149 / 37 | -- | -- | `GuiInfoPopup`: the toast -- `maxWidth = W * 0.9f` `:17`, `maxHeight = H * 0.2f` `:18` (D-UI-105's cap), `FONT_SIZE_MINI` `:22`, measured `:27-39`, padding 0.03 W / 0.02 H `:42-45`, top-centred `posY = H * 0.02` `:47-50`, `FADE_DURATION 250` ms `:98`, fade in/out `:103-109`, `easeOutCubic` `:111`, past `mDuration` `mRunning = false` `:90-96` (the Window deletes it at `Window.cpp:375`); `<SDL_timer.h>` `:6`. `GuiInputConfig`: the 14 prompt rows `:49-78` (`HotKeyEnable` `:73`), `HOLD_TO_SKIP_MS 1000` `:45`, hold-to-skip `:327-353`, the per-row handler `:171-241`, `assign` refusing a mapping already used except `HotKeyEnable` `:401-423`, **the `SET SELECT AS HOTKEY` / `DO NOT ASSIGN HOTKEY` box `:264-286`** (writes `hotkeyenable`, against the SDL fallback's `hotkey`), full-screen under `fullScreenMenus()` `:293-296`, **`GAMEPAD %i` with `getDeviceId() + 1` `:134` -- the SDL instance id, not the player number**; two `pgettext("joystick", ...)` families `:11-40`, `:163`, `ngettext` `:347`. `GuiDetectDevice`: the five strings `:32`, `:46`, `:52` (HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT), `:56`, `:58`; ESC skips after the first run `:94`; `exists(es_input.cfg)` on first run `:127` (R2 § 4.4-4.5; R3 § 4) |
| the component base and the theme: `GuiComponent.cpp` / `.h`; `ThemeData.cpp` / `.h`; `ThemeVariables.cpp` / `.h`; `HelpPrompt.h`; `HelpStyle.cpp` / `.h`; `BindingManager.cpp` / `.h` | 1540 / 298; 2891 / 599; 44 / 15; 27; 87 / 31; 522 / 118 | -- | -- | `GuiComponent`: `mOpacity`/`mAmbientOpacity` 255 `:20`, `getOpacity` the product `:391-397`, `setOpacity`/`setAmbientOpacity` pushed to every child `:399-423`; the animation slots `:489-584`, `animateTo` `:977-1038` honouring `PowerSaverMode`/`TransitionStyle == "instant"` `:992`; `~GuiComponent` `:28-52` (**`mWindow->removeGui(this)` first `:30`**, `EXTRACHILDREN` deleted, the rest detached `:43-51`); `input` `:54-63` and `updateChildren` `:80-93` iterate with a saved `next_it` under `TRYCATCH`; `updateHelpPrompts` `:909-922` only when `mWindow->peekGui()` is this and the tag is not `GuiLoading` `:917`; the one `LOG` `:337`. `ThemeData`: `loadFile` `:745-856` **throws** on a missing file (cached `exists` `:752-753`), a parse error `:814-816`, a missing `<theme>` `:819-821`, a missing `<formatVersion>` `:824-826`, an old version `:828-829`; `parseInclude` `:1094-1150` only **warns** (`:1120`, `:1126`, `:1139`, `:1146`); `getDefault` catches to `LogError` `:2246-2262`, `appendFile` to `LogWarning` `:2779-2798`; `ThemeFileCache` `:719-743` under a mutex; `:267` the parser's `{ "multiLine", STRING }` property entry (T34's tile reads it; `GridTextProperties::multiLine` itself is declared in T34's `GridTileComponent.h`, and `ThemeData.h` carries no `multiLine` -- the proof); 25 `LOG(Log` lines, no fork hunk; `ThemeData.h:16` pugixml; its 13 component-header includes (T34's `:623-624`). `BindingManager`: 2 `_("` lines `:136`, `:150`. `HelpStyle.cpp:3`: `resources/Font.h` -> `ft2build.h` (`Font.h:10`; the `.h` includes only `math/Vector2f.h` and three std headers; R3 § 3.3). (R2 § 5) |
| the device and audio layer: `AudioManager.cpp` / `.h`; `Sound.cpp` / `.h`; `VolumeControl.cpp` / `.h`; `CECInput.cpp` / `.h`; `TextToSpeech.cpp` / `.h`; `PowerSaver.cpp` / `.h`; `FavoriteMusicManager.cpp` / `.h`; `playlists/M3uPlaylist.cpp` / `.h`; `playlists/AnimatedGifPlaylist.cpp` / `.h` | 749 / 86; 115 / 38; 668 / 61; 376 / 38; 284 / 64; 122 / 84; 127 / 27; 87 / 26; 33 / 18 | -- | -- | `AudioManager`: `<SDL.h>` `:7`, `.h:5 <SDL_audio.h>`, `.h:8 "SDL_mixer.h"` (quoted), `id3v2lib` from `external/`; `fopen(song.c_str(), "r")` `:539`, `:610`; 19 `LOG` lines. `Sound.h:5 "SDL_mixer.h"`. `VolumeControl`: **`<pulse/pulseaudio.h>` `:14` under `_ENABLE_PULSE_`, which the image build takes (`package.mk:23 -DENABLE_PULSE=1`), the ALSA branch (`.h:9-12 <alsa/asoundlib.h>`) what the host parses**; a thread `:32`, `:203`; 32 `LOG` lines, the most in the slice. `CECInput`: `<libcec/cec.h>` under `HAVE_LIBCEC`, off in the image (`package.mk:22 -DCEC=0`); `SDL_PushEvent` `:43`. `TextToSpeech`: `<espeak/speak_lib.h>` `:54` under `_ENABLE_TTS_`, off; a thread `:92`, `.h:47`; 1 `_("` `:177`. `PowerSaver`: `<SDL.h>` `:5`, `SDL_PushEvent` `:29`. **`FavoriteMusicManager`: the favourites file appended `:71` and truncated-then-rewritten `:115`** (a kill between leaves an empty file; R2 § 2.2). The playlists: `utils/StringUtil.h`, `utils/FileSystemUtil.h` (T36's) (R3 § 2.2, § 3.3; R2 § 6) |
| the rest: `LocaleES.cpp` / `.h`; `gettext.h`; `Paths.cpp` / `.h`; `MameNames.cpp` / `.h`; `ImageIO.cpp` / `.h`; `MultiStateInput.cpp` / `.h`; `AsyncHandle.h`; `anim/StoryboardAnimator.cpp` / `.h`; `anim/ThemeAnimation.h`; `anim/ThemeStoryboard.cpp` / `.h`; `animations/Animation.h`; `animations/AnimationController.cpp` / `.h`; `animations/LambdaAnimation.h`; `math/Misc.cpp` / `.h`; `math/Transform4x4f.cpp` / `.h`; `math/Vector2f.cpp` / `.h`; `math/Vector2i.cpp` / `.h`; `math/Vector3f.cpp` / `.h`; `math/Vector4f.cpp` / `.h` | 427 / 83; 300; 363 / 112; 461 / 62; 394 / 54; 53 / 19; 57; 237 / 192; 146; 242 / 28; 12; 38 / 35; 27; 159 / 40; 329 / 53; 39 / 73; 1 / 61; 21 / 104; 107 / 101 | -- | -- | `LocaleES` takes glibc's `<libintl.h>` under `-DHAVE_INTL` (the stand-in's flag); `LocaleES.h` is doubled by `tests/app-unit/fakes/LocaleES.h` (§ 1 i). `Paths` through `utils/Platform.h` (T36's). `MameNames` and `anim/ThemeStoryboard` parse with pugixml (`MameNames.cpp:6`, `anim/ThemeStoryboard.h:5`). `ImageIO.cpp:4 <FreeImage.h>` (a fake). `MultiStateInput` includes `Window.h` (the fakes' double if copied beside it, R3 § 2.2). The `math/`, `animations/AnimationController`, `ThemeVariables` and the playlists are **pure: they link and run on the host today** (R3 § 2.2's first class); `math/Vector2i.cpp` is one line. (R3 § 2.2, § 3.3) |
| the watchers: `watchers/WatchersManager.cpp` / `.h`; `watchers/BatteryLevelWatcher.cpp` / `.h`; `watchers/NetworkStateWatcher.cpp` / `.h` | 203 / 92; 9 / 21; 21 / 25 | -- | -- | `WatchersManager::run` `:159-203`: per iteration `mThreadLock` + condvar (`wait` while paused, `wait_for(1 s)`) `:164-177`, then **`std::unique_lock<std::mutex> lock(mWatchersLock)` `:181` held for the whole walk `:185-200` -- `item->component->check()` `:196` inside it**, `NotifyComponentChanged` `:197` taking `mNotificationLock` `:128` (lock order `mWatchersLock` -> `mNotificationLock`), notifications **on the watcher thread** `:130-131`; every static entry point blocks on `mWatchersLock` meanwhile: `GetComponent<T>()` `.h:35`, `RegisterComponent` `:66`, `UnregisterComponent` `:78`, **`ResetComponent` `:92-104`** (sets `nextCheckTime = now`, cannot run `check()` itself), the destructor `:143`; `WatcherInfo` `.h:67-73` allocated `:68-73`, freed on unregister `:85-86` (EP-13) and in the destructor `:143-149`, the `IWatcher*` not owned; `new std::thread(&WatchersManager::run, this)` `:61`, `join` `:154`, `stop()` `:20-27` deletes the singleton; **`mRunning` and `mPaused` plain `bool`s `.h:85-86`, `mRunning = false` written `:151` outside any lock, read `:161`, `:172`, `:187`**; 2 `LOG` lines `:57`, `:139`; no fork hunk (R2 § 3; T33 PL-14 / #1283) |

**The 19 fork commits on the 96** (`git log --format='%h %ad %an %s'
--date=short cada856d86..PIN -- <96> | nl -ba` ends at 19; `rev-list
--count bccd715707..PIN -- <96>` 19; two merges among them, `370ebe416` and
`2dae87308`; R1 C16), 17 without merges and 2 merges (`370ebe416` 2026-09-25, of `rocknix/master`;
`2dae87308` 2026-09-15, of `feature/es-logging-rc11`), the newest
`c8dc72cf9` 2026-10-11 *emulationstation: manage cloud connections and
network recovery*, the oldest `62e45ea6f` 2026-08-27 *restore page: explain
the rows, gate the cloud check, keep LATER's promise*; the table's column
names the rest by subject. Two authors by `%an` (`Max Engel` 14,
`blitterbot` 5; three addresses by `%ae`). The issue numbers over the 19
subjects and bodies, counted by occurrence (`git log --format='%s%n%b'
bccd715707..PIN -- <96> | grep -o -E '#[0-9]+' | sort | uniq -c`): #178 and
#175 three each, #383, #199, #106 and #102 twice, the rest once (the proof's
lines). The lane's `02` § Coverage quotes the subjects from its own `git
log`, never from here.

**What the research checked and found sound, beyond what the table and § 5
carry, so the lane confirms rather than hunts:** the 83 upstream-carried
files are byte-identical to `rocknix/master` and to the merge base (R1
C12); every T35 source is named once and unconditionally in
`es-core/CMakeLists.txt` (R3 cmd 21); the French of every msgid in the 96 **is checked** (the proof's parser,
2026-10-31, at the pin): 61 distinct `_("` msgids over the ten files, every
one with a non-empty French `msgstr`, the 25 `pgettext` pairs and the 2
`ngettext` pairs too, and the fork's own added msgid is one, `CLEAR` ->
`EFFACER` (po `:6923`); the lane re-runs the parser as its own line.

**What they found instead -- the leads, one line each.** § 4 carries each
lead's disposition and the question it serves, citing this table rather
than restating its lines; the lines are the pin's, read by R2 on
2026-10-30 (`git -C <qa-integration> show 16dbac5211:<file> | nl -ba`,
R2 cmds 2-7, 16-21) and by R4 from the lanes' records; nothing here was
tested, and a lead is a fact of the lines until the lane's proof says
more.

| Lead | Lines at the pin | Shape | Q |
| --- | --- | --- | --- |
| L-01 | `Window.cpp:339-340` against `:334-335`; `:1159-1160`; `:1164` | the toast queue pops from its **back**: two toasts queued while a card is up (a pad connected then disconnected, `InputManager.cpp:856`, `:869`) show newest first, while the comment above says *"the order is the order things happened"* (D-UI-093's words); a toast re-queued under a new card gets a **fresh default duration**, not its remainder; the `:1159-1160` comment explains the re-queue loop's push order by the same LIFO fact | Q1 |
| L-02 | `Window.cpp:188-207`, `:49-63`, `:1246-1248`; the raw holders `es-app/src/ContentInstaller.h:45`, `ProxyCards.cpp:125`, `:215`, `:238`, `:244`, `:250`, `:257`, `:514`, `ThreadedBluetooth.h:20`, `:43`, `ThreadedCloudSync.h:191`, `ThreadedHasher.h:50`, `guis/GuiUpdate.h:59` (R2 cmd 20) | `deinit` and `~Window` never free a card or a popup and leave the queue; the only free is `:1248`, when `isRunning()` goes false; a card alive at `deinit` is still in the vector at the next `init()` and drawn again; what a holder may do after that is the owners' (T2 PC-1's window half, § 1 b of T34; R4 item 3) | Q4 |
| L-03 | `Window.cpp:1262-1274` against `:1278`, `:1296` | `unregisterPostedFunctions` iterates and erases `mFunctions` without `mNotificationMessagesLock`, which `postToUiThread` and `processPostedFunctions` take; what `postToUiThread` promises a poster that dies before the drain is T34 L-12's other half (R4 item 4) and #1276's context (R4 item 5) | Q4 |
| L-04 | `Window.cpp:1554-1563`, `:1572-1575`, `:1608-1619`, `:1634-1637`; `:29` | four `std::thread(...).detach()` bodies in `processStorageRequest` capture `this` and call `ApiSystem`; es-core includes es-app for it (`#include "../es-app/src/ApiSystem.h"`), the sibling of T34 L-07's `CloudText.h` include; upstream ROCKNIX's, outside the lanes | Q4, Q7 |
| L-05 | `Window.cpp:262-281` | four keyboard-only Ctrl debug toggles (G/T/I/M) with the `Settings "Debug"` gate commented out on each line: on an image with a keyboard attached a chord changes the screen with no setting; cost against value | Q7 |
| L-06 | `InputManager.cpp:1225`, `:1232`; `FavoriteMusicManager.cpp:115`; `utils/AtomicFileUtil.h:42` (T21's) | `es_input.cfg` and `es_last_input.cfg` are written in place by pugixml `save_file`, the favourites file by truncate-then-write; **zero** `AtomicFile::writeText` calls in the slice (R2 cmd 13: 7 write sites, none atomic) while the API the fork registered in this slice's CMake exists for exactly this (D-CLOUD-078's family) | Q2 |
| L-07 | `InputManager.cpp:893`, `:1187` (the reads), `:1225` (the write), `:1250` (`doOnFinish`'s read; `:420` reads the SDL mapping files); `utils/FileSystemUtil.h:35` (T36's) | a hypothesis to verify against T36's cache: `exists(path)` caches a miss for the session (`es-code-traps.md:127`); on a device whose `es_input.cfg` does not exist yet the first `writeDeviceConfig` caches the miss, writes the file, and a **second pad configured in the same session** reads `exists` false at `:1187`, skips the merge and `save_file` replaces the file with the second device alone; 41 `exists(` lines in the slice, 0 pass `false` (R2 cmd 12) | Q2 |
| L-08 | `InputManager.cpp:1242-1284` (`:1262`, `:1272`, `:1277`) | `doOnFinish` re-reads `es_input.cfg`, finds every `<inputAction type="onfinish">` and runs each `<command>` text **synchronously on the UI thread** through `ProcessStartInfo(...).run()`; a non-zero exit is a warning; the fork masks the logged line `:1270` | Q2 |
| L-09 | `InputManager.cpp:1101-1108` against `GuiInputConfig.cpp:73`, `:270-281`; `InputConfig.cpp:186-189` | two names for the pad hotkey -- the SDL-mapping fallback writes `hotkey`, the configuration page maps `HotKeyEnable` (`GuiInputConfig.cpp:273`, `:279`), stored lower-cased as `hotkeyenable` by `mapInput` (`InputConfig.cpp:188`); which one the launch scripts read is outside the slice (T3's templates); the inconsistency is a fact of these lines | Q2, Q6 |
| L-10 | `InputManager.cpp:946`, `:960` | the two "Approximative device found" `LogInfo` lines read `configNode.attribute(...)` before `configNode = item` is assigned, so they print empty attributes (pugi's null node is safe; the line is uninformative) | Q2 |
| L-11 | `watchers/WatchersManager.cpp:181-199`, `:92-104`, `:151`, `:161`, `:172`, `:187`, `:130-131`; the callers `es-app/src/NetworkThread.cpp:87-95`, `:58` (T33's) | `mWatchersLock` held across every `check()`; `ResetComponent`, `GetComponent`, `Register`/`UnregisterComponent` and the destructor wait on the UI thread for a network or battery probe; `mRunning` is an unsynchronised `bool`; notifications run on the watcher thread (T33 PL-14 / #1283's es-core half, EP-13's `WatcherInfo` lifetime; R4 items 1-2) | Q3 |
| L-12 | `guis/GuiMsgBox.cpp:116-134`, `:246-264` | the back-button accelerator: the only button; else the first named `OK` or `NO`; **else the last** -- a dialog without an `OK`/`NO` button binds back to whatever is last (T26 L-22's TRY AGAIN / CANCEL SIGN-IN; `es-ui-style-guide.md:178`); fired also by any `TYPE_BUTTON` from an **unconfigured pad** `:257-261` | Q6 |
| L-13 | `guis/GuiTextEditPopupKeyboard.cpp:14`, `:220` against `components/MenuComponent.cpp:14` (T34's) | the second `BUTTON_GRID_HORIZ_PADDING`, 0.0052083333 against the house 0.022 (`es-native-ui.md:179-183`); two definitions, one macro name, two files; T34 L-05 recorded the claim's side, this slice owns the define (R4 item 6) | Q6 |
| L-14 | `guis/GuiTextEditPopupKeyboard.cpp:392-397`, `:453-454`, `:491-496` | `x` on the keyboard, and the CLEAR button, commit `""` and delete the popup with no confirmation: one press empties a cloud folder path, a hostname or a Wi-Fi key and submits it (`es-ui-style-guide.md` § Confirmations: a consequential action asks) | Q6 |
| L-15 | `guis/GuiTextEditPopup.h:15-16`, `guis/GuiTextEditPopupKeyboard.h:13-14`; `es-app/src/guis/GuiWifi.cpp:365`, `:367` (T21's) | neither popup class takes a masking mode; the WI-FI KEY popup types in the clear (T21 PL-26, Backlog #1192; R4 item 7); the field under it is `TextEditComponent` (T34's) | Q6 |
| L-16 | `guis/GuiMsgBox.cpp:44`, `:234`, `:240` | `TextToSpeech::getInstance()->say(text)` twice in one constructor, and a third `say(btn->getText(), true)` for the focused button | Q6 |
| L-17 | `guis/GuiInputConfig.cpp:134` | the subtitle `GAMEPAD %i` prints `getDeviceId() + 1`, the SDL instance id, not the player number: the third pad plugged in reads GAMEPAD 3 whatever its seat | Q6 |
| L-18 | `Scripting.cpp:88-149` (`:92-93`, `:98-113`, `:142`), `:169-178` (`:172-176`) | `executeScript` quotes the script path only when it has a space, strips `"` from every argument and quotes an argument only when it contains a space -- a ROM `a$(id)b.zip` or a scraped name with a backtick reaches `sh` unquoted when any script sits in a hooks directory (T2 FD-9/FD-19; R4 item 18); on the device **every file** in `scripts/<event>/` runs (the extension filter is WIN32-only), fire-and-forget except `quit` | Q5 |
| L-19 | `Scripting.cpp:158-207`; `watchers/WatchersManager.cpp:29-53` | `fireEvent("game-start")` scans three per-event directories and three single-script directories on every launch, empty or not (the directory's `exists` cached `:193`); `WatchersManager::pause` on the launch path (T2 `02:83`; `time-to-play.md`) | Q7 |
| L-20 | `InputManager.cpp` `configureEmulators` (T2 `02:61-62`; the call `es-app/src/FileData.cpp:547`, T2's) | runs on every command build, its result discarded when `includeControllers == false`; the controllers blob is built from the device names the kernel reports and spliced inside the template's double quotes -- a name with `"`, `$` or a backtick breaks or expands the line (T2 FD-6, FD-7; R4 items 21-22, § 8 delta 1) | Q2, Q7 |
| L-21 | `Window.cpp:743-745`, `:999-1003`; the eight `mHelp->` lines `:745`, `:1001`, `:1009`, `:1011`, `:1012`, `:1077`, `:1397`, `:1398` (T34's run `:1422`) | with full-screen menus on, a second page gets no help bar from the Window; a page that wants one draws it itself (`es-code-traps.md:134-136`); none of the eight calls `mHelp->setOpacity`, so batocera's `9dbd4b9bf` null guard (`HelpComponent.cpp:208-213`, `:251`, T34's) has no caller here -- the callers' read T34 § 5 item 3 hands this slice (R4 item 12) | Q6 |
| L-22 | `.claude/rules/es-native-ui.md:30` against `Window.cpp:1192` and the rule's own `:192-194`, `:207-208` | the rule still calls `AsyncNotificationComponent` the *"top-right progress card"*; the card is centred at the pin (the fork's hunk) and the same rule says so twenty lines on -- a stale sentence for the coordinator's sweep (D-WORKFLOW-013's family, `tools/archaeology --reversal`), not the lane's edit | Q7 |
| L-23 | `ThemeData.cpp:745-856`, `:1094-1150`, `:2246-2262`, `:2779-2798` | `loadFile` throws on five conditions while `parseInclude` only warns on four, `getDefault` catches to `LogError` and `appendFile` to `LogWarning`: a broken include is a silent fallback, a broken root a logged one; upstream's parser, read for brittleness | Q7 |
| L-24 | `InputManager.cpp:792-800` (`:795`) | F4 pushes `SDL_QUIT` through a `new SDL_Event()` never freed (`SDL_PushEvent` copies); one event per press | Q7 |
| L-25 | `guis/GuiTextEditPopupKeyboard.h` (R1 C07's `last_fork_commit 1593c299f3` against C12's `Y Y`) | the inventory records a fork commit on a file that is byte-identical to the merge base: the touch was undone or merged away; a provenance footnote for § The merge debt, nothing to fix | Q7 |
| L-26 | `es-core/CMakeLists.txt` at T21's `3ae9610b0` (`@@ -9`, `@@ -124`, `@@ -151`, `@@ -259`, R1 C21) | the one lane-on-lane hunk inside the 96, and two of the five files it registers (`HttpText.{cpp,h}`, `RecoveryOutcome.h`) fall to this slice's `rest` at T21's tip: a collision the integration owns and the hand-back names (§ 1 h) | Q7 |
| L-27 | `Window.cpp:777-779`, `:1091-1105`, `:1107-1138` (`:1117`), `:234-260`, `:792`; `es-app/src/SystemScreenSaver.cpp:342-358`, `:378-380`, `:538-548` (T33's) ; `SystemData.cpp:459-473` (T2's) | **#1305 (T33 PL-25):** a slideshow screensaver that starts during a transfer fills its `FileData` list; the transfer's rescan deletes a game gone from disk; the next pick reads freed memory -- `stage-c/pl25-screensaver.py` FAILs at the pin and T33's tip with a heap-use-after-free in `selectGameMedia` (T33's record at `947ace1966`); the list is cleared only when the screensaver stops (`resetCounts` from `cancelScreenSaver`, `Window.cpp:1117`); nothing in the window holds the screensaver off while `GuiCloudTransfer` runs (`:777-779`) -- the window's half of a three-sided fix (R4 § 1's item 31, below) | Q4 |
| L-28 | `Window.cpp:743-745`, `:1005-1078` (`:1031-1041`, `:1050-1075`); the components' chain `ComponentTab.cpp:341`, `ComponentGrid.cpp:493`, `:522-552`, `MenuComponent.cpp:533` (T34's) | **T34 PL-05 (#1307, inherited):** on the image at 1280x800 the tabbed SCRAPEUR page's help bar carried only FERMER and RETOUR -- no SWITCH TAB and no row prompt -- pixel-identical with a row or the strip focused; T34's seat traced SWITCH TAB through the pin's components, so the empty bar is the window's bar collection (`setHelpPrompts`, T35's) or the image's composition -- this slice reads which | Q6 |
| L-29 | `Window.cpp:1005-1078` (`:1031-1041` the merge by icon); `ComponentList.cpp:568` (T34's; D-UI-133) | **T34 PL-04 / D-UI-133 (#1307, inherited):** at 1280x800 the list's CHOISIR prompt drew its icon with 0 `Unknown help icon` lines in `es_log.txt` though the catalog carries `haut/bas` for `up/down` (po `:3708-3709`, T34's proof); why the window's bar did not show the component's `_()`-wrapped key is this slice's read of what `setHelpPrompts` does to a key it does not know | Q6 |

**The neighbours, and whose they are:** `es-core/src/components/**` --
`MenuComponent.cpp:14` (the house `BUTTON_GRID_HORIZ_PADDING` 0.022 and its
`:7-13` comment), `AsyncNotificationComponent.cpp:31`, `:64`, `:112` (the
card this window places), `ComponentGrid.cpp:396-414` (`canMoveCursor`,
D-UI-034), `HelpComponent.cpp:208-213`, `:251` (`setOpacity`'s unguarded
`mGrid`), `TextEditComponent.cpp:39`, `:47` (the two posted raw `this`) --
are **T34's** (#681, in flight; R4 item 24-27's lines); `HttpReq.{cpp,h}`
(the pooled connection's `stallTimeout`, the curl header callback of
#1195), `Settings`, `SystemConf` and `utils/AtomicFileUtil.{h,cpp}`
(`writeText` `.h:42`) are **T21's** (#668); `utils/FileSystemUtil.{h,cpp}`
(the `exists` cache: `.h:35` default `enableCache = true`; the cache body
`:144`, `:203-220`, its erase `:185-195` per T34's brief),
`utils/Platform.{h,cpp}` (`ProcessStartInfo`, `system()`), `utils/StringUtil`
(`maskSecrets`), `resources/Font.cpp`, `renderers/Renderer.cpp`
(`ScreenSettings::fullScreenMenus`, `isSmallScreen`) and
`utils/OfflineProxyUrl` are **T36's** (#683); `es-app/src/CloudText.*` and
the cloud threads **T18's** (#665); `ProxyCards`, `ThreadedHasher` **T20's**
(#667); `guis/GuiMenu.*` **T26's** (#673); every other page under
`es-app/src/guis/` (`GuiLoading.h` included) **T31's** (#678); the views and
`services/HttpServerThread.cpp` (the `/quit` `:219` and `/messagebox` `:545` routes, each posting its `GuiMsgBox` through `postToUiThread` `:229`, `:559`, R4 item 30) **T32's** (#679); `AppWindow.h`, `NetworkThread.cpp`, `SystemScreenSaver.cpp`,
`main.cpp`'s exit order (`:1322` `closing()`, `:1330` `WatchersManager::stop()`,
`:1358` `window.deinit()`, R4 § 2) **T33's** and **T2's** (#680, #649). The include reach is § 5 item 1's (18 SDL angle lines over the 101, 2 quoted
`"SDL_mixer.h"`, 51 non-standard angle includes with their guards,
`Window.cpp:29` the one es-core to es-app include); the outside-includer
count per header is the lane's run (no research line).

**Already found; do not re-find; take up.** Each is cited at its lines in
`02` with a disposition; the states are as R4 read them on 2026-10-30 (R4
§ 4: the per-term union over the open issues printed `union count: 17`),
re-read at stage A; **asks** is R4 § 1's column -- *read* (state and keep
the invariant in `02`), *rule 6* (a contained fix put to the stage-D
pause), *pause* (a question for the pause, never the lane's ruling); a
ruling the table names by letter is § 1's. The audit folders are § 3 item
8's.

| Found by | Lines at the pin | Take up as |
| --- | --- | --- |
| T33 L-01 / PL-14 / #1283 (OPEN, `bug`; T33 `02:99`, `:389`, `:730`, `00:162` Ruling 7, `t33-streams.md:81`, `:147`, `:188`, `:203`; #1283 body lines 10, 18-20, 26) | `WatchersManager.cpp:80-100`, `:181-199` | **rule 6**, shape named by T33: `check()` outside `mWatchersLock` with the `WatcherInfo`'s lifetime kept (EP-13); #1283's checkbox at its line 18 stays open until this slice's record shows a line-cited read of the fixed file; the pads watcher `NetworkThread.cpp:58` and the update check `:87-95` are a second and third `check()` under the same lock (R4 items 1-2; § 1 c) -- L-11, Q3 |
| T2 PC-1 (`02:178`, `:211`, `04:142`, `05:612` *"T35/T18"*); T33 `04:135`; T34's brief `:115-120`, `:667`, `:1012-1017`; D-WORKFLOW-213 | `Window.cpp:188-207` (`deinit`), `:1236-1260`, `:1177-1234`; `main.cpp:1358` | **read** then **pause**: what the window's teardown does to its cards and in what order against `main.cpp:1358`; T34 reads the card's half (its Q4) and files the `bug` if its read proves the window, naming T18 (`ThreadedCloudSync.cpp:757`) and T20 (`ProxyCards`) for the callers; this slice owns the teardown order (R4 item 3) -- L-02, Q4 |
| T34 L-12 (its brief `:607`, `:1006-1008`) | `Window.cpp:1276-1290`, `:1292-1307`, `:1262-1274` | **read** and state the contract: what `postToUiThread` promises a poster that dies before the post runs; T34's contained fix (a weak token the posts check) is put to the pause with T33's `AppWindow` named; this slice's half is the promise (R4 item 4) -- L-03, Q4 |
| #1276 (OPEN, `bug`; T33 PL-06; body lines 10-12, 26) | `Window.cpp` `postToUiThread`; `WatchersManager.cpp:20-27` (`stop`) | **read**: the window's queue after `AppWindow::closing()` (`main.cpp:1322`) and `WatchersManager::stop()` (`:1330`) are the context for the two rows above; the fix is T33's S4a (R4 item 5) -- Q4 |
| T34 L-05 (its brief `:600`, `:951-954`, `:1406`, `:1519`, `:1679`); `es-native-ui.md:177-183` | `GuiTextEditPopupKeyboard.cpp:14`, `:220` | **pause**: delete the second copy and read the house 0.022 (the key grid would widen 4.2x), or keep the popup's own gap and correct T34's comment; a frame of the keyboard at 640x480 either way (R4 item 6; `engineering-practices.md:576`) -- L-13, Q6 |
| T21 PL-26 / Backlog #1192 (OPEN; T21 `02:143`; T34's brief `:686`) | `GuiTextEditPopup.h:15-16`, `GuiTextEditPopupKeyboard.h:13-14` | **pause**: a masking mode on both popup classes with a SHOW toggle (#1192's checkbox at its line 11: a frame at 640x480 of the key popup masked and shown, the French for the new label, `es-untranslated` naming nothing new); T34 may name `TextEditComponent` as where the field's half belongs (R4 item 7) -- L-15, Q6 |
| T26 L-22 (`02:51`); T31 `02:141`, `:640`; T34's brief `:998-999`; `es-ui-style-guide.md:177`; `es-native-ui.md:73` | `GuiMsgBox.cpp:116-134` | **read** and state the rule as the source has it (the only button; else the first named OK or NO; else the last); **pause**: whether the fall-through to the last button stays in the component (a style call T26 posted for its page; the component's half is this slice's) (R4 item 8) -- L-12, Q6 |
| T26 `02:550`, `:796` | `GuiMsgBox.cpp:286-294` | **read**: a dialog's callback runs on its own copy, so closing a page from one cannot free the running lambda -- the invariant T26's and T31's page reads rest on; state and keep (R4 item 9) -- Q4 |
| `es-code-traps.md:79-88`; T34's brief `:975-980`; D-UI-034 (register `:167`) | `GuiMsgBox.cpp:296-299`; `Window.cpp:1005-1078` | **read**: the dialog's 2x2 shape over the N x 2 button row is this slice's, the grid's `canMoveCursor` T34's; a frame of an OK-only dialog reading `OK` and no `CHOOSE` is T34's G-06 (R4 item 10) -- Q6 |
| `es-code-traps.md:134-136`; T31 L-26 / #1245 (OPEN, fixed `95852f873`); T34's brief `:672`, `:711`; the 2026-09-13 audit `02:291` | `Window.cpp:743-745`, `:999-1003` | **read**: which pages draw their own bar and why; the checker proposal is the coordinator's (R4 item 11) -- L-21, Q6 |
| T34's brief `:1354` (§ 5 item 3), `:1422`, `:137-140` (ruling g) | `Window.cpp`'s eight `mHelp->` lines | **read**: T34 writes the `setOpacity` callers' read (107 tree-wide lines, its run) for this slice; this slice takes it up for the eight lines under D-WORKFLOW-162 (R4 item 12) -- L-21, Q6 |
| T34's brief `:954-958`; `es-native-ui.md:189-194` | `Window.cpp:1183`, `:1192` | **read**: the card's position re-applied every frame must agree with `AsyncNotificationComponent.cpp:64`, `:112` (0.9 W, centred); T34 cited the two lines from this slice's file, not re-read (R4 item 13) -- Q1 |
| D-UI-093 (register `:404`); `es-native-ui.md:214-222`; F-ES-24 (the 2026-09-25 audit `02:199`, Low; `/usr/bin/grep -c 'F-ES-24' .../05-punch-list.md` printed `0`, R4 item 14) | `Window.cpp:324-351`, `:1152-1175` (ES `c1c0d6ddc`) | **read** the queue's two rules and **pause**: F-ES-24's consequence -- every toast is held while any card is up, the minutes-long hasher card included, which D-UI-079 keeps as upstream has it -- was recorded Low and never dispositioned; this slice says whether it stands or is a bug -- L-01, Q1 |
| D-UI-105, D-UI-106 (register `:429`, `:431`); `es-native-ui.md:207`, `:291`, `:384`; `es-player-text.md:31` | `GuiInfoPopup.cpp:17-18`, `:27-39`, `:47-50` | **read**: the cap and the ellipsis are the component's; the words are the pages' (R4 item 15) -- Q1 |
| T34 L-07 (its brief `:602`, `:1355`) | `Window.cpp:29`; `es-core/CMakeLists.txt` | **read**: the include's disposition is written by T34 for its own line; this slice records `Window.cpp:29`'s (R4 item 16) -- L-04, Q7 |
| #1212 (OPEN, `bug`; body line 3) | `Window.cpp:542-543` | **read**: the invariant a T21 bug's "no wrong outcome" rests on -- the Window updates and feeds only the top page (R4 item 17) -- Q4 |
| T2 FD-9 / FD-19 (`02:71`); T33 `04:132`; D-WORKFLOW-213 | `Scripting.cpp:88-148` | **rule 6**: `shellQuote` (the tree's form, `FileData.cpp:1148-1151`, T2's) on every argument, or an argv executor (#1192's second half); the precondition is a player's own script, the distribution ships none (R4 item 18; § 1 d) -- L-18, Q5 |
| T2 `02:83`; `time-to-play.md` | `Scripting.cpp:158-207`; `WatchersManager.cpp` (`pause`) | **read** and price from `docs/vm-qa-log.md`'s launch number, or `CANNOT` with the harness's reason (R4 item 19) -- L-19, Q7 |
| the 2026-09-24 audit `02:482` (the twelve `maskSecrets` sites; its gap *"a negative over the"* sweep) | `Scripting.cpp:49`, `:122`, `:129` | **read**: the mask's reach in the fork's lines; the negative that audit named is the gap (R4 item 20) -- Q5 |
| T2 FD-6 (`02:61`), FD-7 (`02:62`, posted "for T36"; § 1 a) | `InputManager.cpp` `configureEmulators`; the call `FileData.cpp:547` (T2's) | **read** and price (FD-6); **rule 6** on the blob's side (quote or reject a device name carrying `"`, `$`, a backtick), the template's side T3's (`functions:128`) (R4 items 21-22) -- L-20, Q2, Q7 |
| #54 (OPEN, no label; body lines 10, 20, 55, 58) | `InputManager.cpp` (`SDL_JOYBUTTONDOWN/UP`, `deinit` `:153-196`); `Window.cpp:199-200` | **read**: ES keeps reading the gamepad while the sign-in browser is open; `window->deinit()` calls `InputManager::deinit()`; the fix is the sign-in window's (T18's lane) with the input manager's handover named (R4 item 23) -- Q2 |
| T34 L-01 (its brief `:596`, `:989-995`, `:625`) | `InputConfig.cpp:353-366` | **read**: the fix is T34's (`ComponentList.cpp:568` drops the `_()`); this slice states what `buttonLabel` and the icon table promise a translated key (R4 item 24) -- Q6 |
| T26 `02:735`; T31 `02:565`; T34's brief `:1426` | `InputConfig.h:6` | **read**: a harness fact -- the plain `g++ -fsyntax-only` stand-in fails on `SDL_joystick.h` everywhere; the fakes and the include roots are § 5's (R4 item 25) -- § 5 |
| T34's brief `:1174` | `InputManager.h:7` (pugixml), `GunManager.h:10-13` | **read**: `InputManager.h` adds pugixml and `GunManager.h` (`<libudev.h>`, `<SDL.h>`, `<Windows.h>`) to every includer; the include reach for the build recipe and the packet (R4 item 26) -- § 5 |
| T34's brief `:623-624` | `ThemeData.cpp:267` and its 13 component-header includes | **read**: the contract T34's tile text (#27, D-UI-050, ES `2088eadb9`) reads from the theme (R4 item 27) -- Q7 |
| D-UI-021 (register `:78`); `es-native-ui.md:138-141`; T34's brief `:671`; #63, #65 (OPEN) | `Window.cpp:287-288`; `GuiComponent.cpp:54-63` | **read**: the component half is T34's (its G-05), the pages T31's; this slice states how the window hands a key to the top page and nothing else (R4 item 28) -- Q6 |
| #1178 (OPEN, `bug`; T20 `02:158`) | `GuiMsgBox.cpp` as the surface | **no T35 action**: the box shows what it is given (`GuiMsgBox text: [std::exception]`, T20's fixture); recorded so the lane does not re-find it (R4 item 29) |
| T32 `02:180`, `:196`, `:378` | `GuiMsgBox.cpp` as the surface; `services/HttpServerThread.cpp:219`, `:229`, `:545`, `:559` (T32's) | **no T35 action**: at the pin both routes post their box through `mWindow->postToUiThread`, so it is built on the interface thread (the proof; R4 item 30) -- Q4 |
| **T34 PL-05 (#1307, OPEN `audit` `punch-list`; body line 11, *tracked: the stage-D pause*)** | `Window.cpp:743-745`, `:1005-1078`; the components' chain (T34's) | **read**: the window's bar collection against the components' prompts on a tabbed page at 1280x800 (G-11 frames one), and where SWITCH TAB and the row prompt are dropped -- L-28, Q6 |
| **T34 PL-04 / D-UI-133 (#1307; body line 10)** | `Window.cpp:1005-1078` (`:1031-1041`); `ComponentList.cpp:568` (T34's) | **read**: what `setHelpPrompts` does to a translated icon key, and why no `Unknown help icon` line was written for `haut/bas` -- L-29, Q6 |
| **T33 PL-25 / #1305** (OPEN, `bug`, filed 14:45 UTC 2026-10-30 on #680; T33 `05:502-513`, `02:61` EP-38; `stage-c/pl25-screensaver.py` at `947ace1966`, `t33extract.py` beside it) | `Window.cpp:777-779`, `:1091-1138` (`:1117`), `:234-260`, `:792`; `SystemScreenSaver.cpp:342-358` (T33's); `SystemData.cpp:459-473` (T2's) | **read** then **pause**: the window's half -- whether the screensaver may start while a transfer page owns the screen (`:777-779` reads only `mTimeSinceLastInput`), whether `cancelScreenSaver`'s `resetCounts` (`:1117`) is the only path that clears the list, and what the window does to the screensaver on a rescan or a `removeGui`; T2's rescan patch and T33's screensaver retirement are the other two halves, named for their owners at the pause; the script is the FAIL-at-pin harness this slice re-runs unchanged (§ 5, 3.27) -- L-27, Q4 |
| #585 (OPEN; body 125 lines, 0 es-core matches; 33 comment lines, 0, R4 § 5) | -- | the lines this slice owes start with T33's never-posted candidate (`WatchersManager.cpp` L-01 for `rocknix/master`) and R4 § 5's four: the lock, `Scripting`'s quoting, the controllers blob, the second padding constant if deleted -- each a line for the coordinator to post, never the lane's (Q7) |

## 3. Read first

In this order, each read in this session, and `01-research-notes.md` says
which were read (`working-principles.md` § Pre-flight):

1. **The rules**, each at the section named, with the question it serves;
   the section's own sentence is not repeated here -- open it (the line numbers are the coordinator worktree's at `a00b3354d5`, the
header's hash, by `grep -n '^## '`; the stranger's proof read every one
there on 2026-10-31: `es-player-text.md`'s lines from `:273` on moved by +4
since `7a32dff771` (`30c3c402fd`, hunk `@@ -271,2 +271,6`), so T34's `:326`
reads `:330` here; the register's `## Open decisions` opens at `:769`):

   | Rule | Line | Section | Serves |
   | --- | ---: | --- | --- |
   | `es-native-ui.md` | `:22`, `:26-27` | Where things live: the es-core primitives (`GuiMsgBox`, the two text popups, `GuiInfoPopup`, `GuiInputConfig`) | Q6 |
   | | `:30` | the same list's "top-right progress card" -- **stale against `Window.cpp:1192`** (L-22) | Q7 |
   | | `:32` | The other files that carry the interface law (D-UI-039) | Q7, § 9 |
   | | `:81`, `:91`, `:93`, `:94`, `:107`, `:117` | Core patterns: the confirmation shape; the toast; the card for fast work only (D-UI-078); a file another process writes is read uncached; `Scripting::fireEvent`'s three directories | Q1, Q2, Q5, Q6 |
   | | `:121` | Tabbed pages: the strip is a focus stop (D-UI-021) -- the window hands a key to the top page and nothing else | Q6 (item 28) |
   | | `:144` | The cards at the link's return (D-UI-101, D-UI-109): the order is the order things happened | Q1 (L-01) |
   | | `:175`, `:179-183`, `:189-194`, `:199-210`, `:214-222` | Spacing: the bar's gap in one place; the card's 0.9 W centred, re-applied every frame by `Window::renderAsyncNotifications`; the four surface tiers; one floating surface at a time (D-UI-093) | Q1, Q6 (L-13, item 13, item 14) |
   | | `:350`, `:358` | Code conventions: pages provide `getHelpPrompts()`; capture `Window* window`, not the menu | Q4, Q6 |
   | | `:377`, `:384` | Anti-patterns: two surfaces for one event; the card that vanished into a `GuiInfoPopup` | Q1 |
   | | `:405` | Before the pin moves, the compiler has seen the edit (`tools/es-syntax-check`, exit 2 here) | § 5, § 9 |
   | `es-code-traps.md` | `:22` | Never rebuild a button bar from inside one of its buttons: `postToUiThread([weak]{...})` | Q4 (L-03) |
   | | `:60` | Comments near a translatable string must be ASCII | Q7, § 9 |
   | | `:79-88` | The help bar offers a direction only where it moves something (D-UI-034): the `GuiMsgBox` 2x2 shell over the N x 2 button row | Q6 (item 10) |
   | | `:91`, `:96-98` | TextComponent measures at its full width and draws at its padded one; `GuiMsgBox` measures at the drawn width (#48) | Q6 |
   | | `:104`, `:127` | Three things a font is not: the third, `exists(path)` caches for the session | Q2 (L-07), Q5 |
   | | `:134-136` | the window paragraph: no help prompts under a second page with full-screen menus; `renderHelpPromptsEarly()` | Q6 (L-21) |
   | | `:139` | Pure text has a home, and a test | § 5 (every unit case's shape) |
   | | `:191` | A rescan that deletes FileData drops the view first (#246) -- the family #1305 belongs to | Q4 (L-27) |
   | | `:238` | A pooled connection with the link gone (#299, D-RA-036): `HttpReq`'s, T21's -- context only (§ 1 f) | Q7 |
   | | `:266` | A taller GuiSettings menu keeps its old top offset: verify in 640x480 and 1280x800 frames | § 5 (G-11) |
   | `es-ui-style-guide.md` | `:32` | Keep the flow and its visual evidence together | § 5, § 7 |
   | | `:141`, `:144`, `:164` | Text: write strings upper-cased; placeholders `AUTO`, `NONE`, `<NOT SET>`; passwords display as `*********` | Q6 (L-15) |
   | | `:169`, `:171-178` | Confirmations: YES first; the back accelerator binds to `NO` or `OK` **and falls through to the last button** | Q6 (L-12; G-04, G-05) |
   | | `:197-204` | Waiting: the card for seconds; a toast when it finished | Q1 |
   | | `:232` | Buttons: BACK last; gate by existence | Q6 |
   | | `:296-304` | Interaction rules: cardinal positions, South confirms, East cancels; `getHelpPrompts()` is how players learn the assignments | Q6 |
   | `es-player-text.md` | `:25` | the brand stays lowercase (D-WORKFLOW-144) | Q6 |
   | | `:29`, `:31`, `:135` | Conventions (`:29`): every label through `_()` (`:31`); a toast is one line at 0.9 of the screen (`:135`, D-UI-105) | Q6, Q1 |
   | | `:141` | Every fork string ships in English and French (D-UI-051) | Q6, § 9 |
   | | `:264`, `:330` | the capture-failure toast follows the card (D-UI-093); TRY AGAIN on a page's help bar | Q1, Q6 |
   | `engineering-practices.md` | `:12` | Change stays inside the fork's lanes (D-UI-079): § 1's lane and upstream-surface lists | every Q |
   | | `:28` | Check upstream early (D-WORKFLOW-162): batocera's twelve (§ 2), `9dbd4b9bf`'s `setOpacity` guard (item 12) | Q7 |
   | | `:83` | Verify design intent (`git log -S` before each FAIL-at-pin lead: the LIFO pop, the second constant, the quoting) | § 4, § 5 |
   | | `:111` | Verify the artifact, not the report: *"EmulationStation abort()ed on an assert ... confirm the process is still alive before re-driving the input"* (R4 § 7) | § 5 (every guest step) |
   | | `:194`, `:250` | A name is not a behaviour; a total is the tool's line | § 5 (the `TOTAL:` line) |
   | | `:419`, `:478`, `:548` | Guards must fail closed; `rc=$?` on its own line; the first PASS is the one to distrust | § 5 |
   | | `:576` | Before deleting a duplicate, diff its behaviours (L-13's second copy is not deleted here) | Q6, Q7 |
   | `bugs-are-agent-first.md` | `:41`, `:53`, `:76` | The three classes; The rules; rule 6 | every bug |
   | `issue-tracking.md` | `:129`, `:180` | A criterion is agent-first (D-QA-044); Ticking an acceptance criterion | § 7 |
   | `upgrade-and-install.md` | `:40`, `:58`, `:74` | Fixing forward is not enough; the `Already written:` line (D-WORKFLOW-050) -- **this slice writes files**: `es_input.cfg`, `es_last_input.cfg` (`InputManager.cpp:1225`, `:1232`), the favourites file, `es_log.txt`; a bug in a writer argues its line, the rest argue *nothing inherited* | every bug |
   | `generic-x64-vm-testing.md` | `:100`, `:108-114`, `:215`, `:221-222` | Headless: `run --headless --daemonize`, `tools/vm-serial`, the pidfile; `--res 640x480` is a flag (#1141), a second size is a second boot | § 5 |
   | | `:325` | A launch, a START or a walk waits for `/isIdle` (D-QA-057) | § 5 |
   | | `:365`, `:382`, `:393` | The first key after five idle minutes only wakes (`Window.cpp:259-260`, R2 § 1.5); a restarted ES comes back on the last game list; `screendump` can serve the previous ES's last frame | § 5 (G-09) |
   | | `:448-458` | Frame at the handheld's size: a UI change is framed at 640x480 before it is called done | § 5 (every frame) |
   | | `:486` | `dismiss-dialogs` ends on the carousel where it was (`z` = B, `GuiMsgBox`'s accelerator) | § 5 |
   | | `:959` | Automated visual QA (`tools/vm-visual-qa`) | § 5 |
   | | `:1145` | A settings change from the shell is invisible to the running interface (`essway.service` stopped first) | § 5 (G-07) |
   | | `:1432` | The guest is the candidate image, not the read tree | § 5 (every frame's side) |
   | `handheld-evidence.md` | whole | what a hang is not: *"a program that has [stopped] ... none reboot the device"* -- the lock of Q3 and the UI-thread `<command>` of Q2 are that shape | Q2, Q3 |
   | `player-language.md`, `least-surprise.md`, `time-to-play.md` | whole | | Q6, Q7, § 6 |

2. **The register.** The rows that name a file or behaviour here (the
   coordinator's branch at `a00b3354d5`; the line is the table's; R2 cmd 14
   printed 18 matching lines, R4 § 3 the 16 of its own pattern): D-UI-016
   `:56` (no drawn border; `NOTIFICATION_OPACITY` 255 -- the card this
   window places), **D-UI-021** `:78` (the strip is a focus stop; the window
   delivers a key to the top page alone, `Window.cpp:287-288`), **D-UI-034**
   `:167` (a help-bar direction only where it moves the cursor), D-UI-050
   `:246` (es-app), D-UI-051 `:251`, **D-UI-078** `:344` (long work on a
   page; the card for fast work), **D-UI-079** `:345` (the lanes;
   `processStorageRequest`'s dialogs and the hasher's card sit outside
   them), D-UI-085 `:357`, D-QA-050/051 `:398-399`, **D-UI-093** `:404` (one
   floating surface at a time: `Window.cpp:331-337`, `:1156-1166`, ES
   `c1c0d6ddc`), **D-UI-105** `:429` and **D-UI-106** `:431` (the toast's
   0.9 cap and ellipsis; a titled notice is a card), D-UI-107 `:432`,
   **D-UI-109** `:434` (the cards' order at the link's return), D-RA-036
   `:428` (the pooled connection's stall bound -- `HttpReq`'s, T21's),
   D-CLOUD-156/167 `:541`, `:575`, D-WORKFLOW-137 `:589`, D-WORKFLOW-144
   `:604`, D-WORKFLOW-162 `:690`, D-WORKFLOW-187 `:722`, D-WORKFLOW-189
   `:723`, D-WORKFLOW-192 `:725`, D-WORKFLOW-195 `:728`, D-UI-128 `:756`,
   D-UI-129 `:757`, **D-WORKFLOW-213** `:759` (T34's ownership row, which
   names this slice's files); by ID only D-WORKFLOW-188 (the P1 branch's),
   D-UI-042, D-UI-045, D-WORKFLOW-155/156, 164/165, D-CLOUD-078 (the last
   known good state, L-06's family), D-CLOUD-119 (the exit sync's 3 s).
   **The highest decided IDs per area, read from the table above `## Open
decisions` (`:769`) at `a00b3354d5` on 2026-10-31 by the stranger's proof
(an `awk` over the decided table): D-CLOUD-191, D-INFRA-031, D-LAUNCH-007,
D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-133, D-WORKFLOW-213** --
D-CLOUD-190 `:762`, D-UI-130 to D-UI-133 `:763-766` (T34's four pause
rulings: `TextComponent` measures at its drawn width; a two-line row's
shares sum to 1; the row inset is a screen fraction; a help-icon key never
goes through `_()`, L-29's row) and D-CLOUD-191 `:767` landed after version
1; D-SYS-014 is an open decision (`:775`), not a row; R5 § G's reading at
`50e94e0e7f` (D-CLOUD-187, D-SYS-014) predates D-CLOUD-188 to 191 and
counted the open table. The pointer's
   `Register:` line is filled from the same command at `COHASH`, never from
   here (§ 10); `tools/register-check` is the proof. The lane reads the
   card, toast, accelerator and lock rows by `tools/archaeology 'floating
   surface'`, `'toast'`, `'back-button'` and `'WatchersManager'` before
   calling anything pending.
3. **The menu map** (`docs/es-menu-map.md`, 989 lines at `a00b3354d5` by
   `/usr/bin/grep -c ''`, unchanged since `a8fe371b0a` by the header's
   diff): `:134` (CONTROLLER & BLUETOOTH: SETTINGS · BLUETOOTH · DISPLAY
   OPTIONS · BEHAVIOR · PLAYER ASSIGNMENTS -- **no row names the
   configure-a-controller flow**, so `GuiDetectDevice` and `GuiInputConfig`
   reach the map only through that section's row; the lane reads the
   section before G-08), `:287` (the keyboard for a cloud folder path:
   *"changes only that pointer; moves no files"*, G-06's surface), `:459`
   (WI-FI KEY -- on-screen keyboard, L-15's surface), `:567-568` (A
   confirms, YES first; a help bar that lies), `:660-664` (the surface
   tiers against the data tiers), **D-UI-039 at `:668`**, **`## Not mapped`
   `:677`** (`:699` SCREENSAVER SETTINGS *"upstream screensaver page,
   unchanged here"* -- G-09 shortens its slider; `:707` KEYBOARDTOPADS and
   #63), `:776` (the sign-in window: B/Backspace closes the on-screen
   keyboard), the visual-evidence section `:26-82`. **The dialogs of this
   slice are not screens to the checker unless they construct a menu:**
   `tools/es-menu-map-check:50-55` reads `new GuiSettings(window,
   _("TITLE"))`, a direct `GuiSettings(` and `MenuComponent(window,
   _("TITLE"))` as screen titles, and its `SOURCE_DIRS` at `:58` are
   `["es-app/src/guis", "es-core/src/guis"]` (the drafter's read at
   `547cdb831a`, held at `a00b3354d5` by the proof -- the checker last changed
   at `d52e3d81c7`; R3 § 6 left the glob open) -- so the six es-core dialogs
   are scanned and, building on `ComponentGrid`/`NinePatchComponent` rather
   than `MenuComponent` (R2 § 4), are expected to contribute 0 titles; the
   lane prints the checker's per-file count before citing that 0, and § 7's
   checkbox is worded on the rows a stream adds, with the checker's line
   quoted, red if it cannot see them.
4. **The blindspots** (`docs/blindspot-register.md`, 1,250 lines at
   `a00b3354d5`, unchanged since `a8fe371b0a`; R4 § 7's grep for the
   window's words printed `1`, `:722`, a font line): 4 (`:13`: `close()`
   inside a page's own handler -- `GuiMsgBox::deleteMeAndCall`
   `:286-294` is the invariant that keeps it, item 9), 5 (`:14`:
   `MenuComponent` upper-cases row titles -- the keyboard's `_()` on
   multi-letter keys, `GuiTextEditPopupKeyboard.cpp:198-204`), 13 (`:22`:
   assumed-done from an artifact's existence), and, at T34's lines (its
   § 3 item 4, the register unchanged since), 35 (`:208`: the card composed
   a third row it had no row to draw on -- `createAsyncNotificationComponent(bool
   actionLine)` `:1152`), 44 (`:445`: a layout computed from what it last
   produced), 49 (`:590`: an edit made blind to the compiler -- the
   stand-in check of § 5), 54 (`:720`: a measurement on a guest whose
   renderer was not the device's -- every frame's side), 75 (`:1206`: a
   corpus read on the wrong tree -- every count at the hash). Blindspot 38
   (the device run without a yes) and 42 (a device's state read from the
   device) bind § 5's guest conditions by their rule text
   (`engineering-practices.md`), their lines not re-read here.
5. **The tests at the pin.** § 5 item 1 describes what exists; read whole
   before a case is written: `es-app/tests/unit/README.md` (`:12-13`,
   `:44-46`: *"functions that read nothing, ask nothing and draw nothing"*,
   T34 § 3 item 5), `es-app/tests/unit/CMakeLists.txt` (159 lines; the four
   targets, R3 § 1.1; `:30` the one comment naming a slice file,
   `LogPolicy.h`; `:114-117` the `es-conf-tests` doubles comment; `:126`
   its `fakes` root first; `:142-158` `es-file-tests-win32`, the executable
   `:146`; `es-app/tests/unit/fakes/` holds `SDL_timer.h` alone, the proof's
   `ls-tree`), **`es-app/tests/unit/LogPolicyTests.cpp:13`**
   (the one of the 96 a test exercises directly, R1 C24; its cases are the
   model for a `Log.cpp` binary), `SystemConfTests.cpp:18-20` (the real
   `Log.h`, `Paths.h`, `Settings.h` with their bodies defined in the test
   -- the precedent a T35 binary follows), `tests/app-unit/CMakeLists.txt`
   (106 lines; `:31` the sanitizer flags; `:44-46`, `:57-60`, `:79-82`,
   `:100-103` the four targets' include orders, R1 C24), **its three
   doubles of this slice's headers** `tests/app-unit/fakes/Window.h`
   (`postToUiThread` runs at once on the posting thread;
   `createAsyncNotificationComponent(bool actionLine = false)`),
   `fakes/Log.h` (the `LogLevel` enum, `FakeLog::lines()`),
   `fakes/LocaleES.h` (`_()` as `std::string`) (R3 § 1.2; § 1 i),
   `tests/app-unit/AppWindowTests.cpp` (its own local `FakeWindow`,
   testing `AppWindow.h` not `Window.cpp`), `tests/gpu-governor-save.py:14`,
   `:26-29` (four methods lifted as text -- the shape for 3.18 to 3.21),
   `tests/cloud-oauth-lifetime.py` (the ASan lifetime shape, 3.2), T33's
   `stage-c/pl25-screensaver.py` and `t33extract.py` at `947ace1966`
   (#1305's FAIL-at-pin harness, 3.27), T33's `stage-a/syntax-check.out`
   (29 es-app files `rc 0`, among them four that include `Window.h` -- the
   headers of this slice have parsed under the 13 fakes transitively, no
   T35 `.cpp` body has, R3 § 3.1), T32's `stage-e/s0-syntax-pin.txt`
   (`SystemView.cpp:469:92: error: 'SDLK_r' was not declared` -- the
   partial `SDL_keyboard.h`; `GuiMsgBox.cpp:250`, `GuiDetectDevice.cpp:94`
   and `GuiTextEditPopupKeyboard.cpp:350` will meet the same gap unless
   the lane's fakes carry `SDLK_RETURN`, `SDLK_ESCAPE`, `SDLK_SPACE`).
6. **The walks and the frames.** `tools/vm-walks/README.md:13-37` (the
   step vocabulary), `:144` (*"`up` from a page's first row lands on its
   BACK button before it wraps"*), the 18 top-level `*.steps` (22 with
   `docs/`; R3 cmd 11): **`confirm-cloud-folder.steps:1-2`** (*"SAVES
   FOLDER on-screen keyboard ... START submits once and closes the
   keyboard"*) and **`to-change-cloud-folder.steps`** (`:8` the dialog
   *"where START does nothing"*, `:35` *"the old walk mislabelled the
   selector as a keyboard"*) for G-06, `docs/networking.steps:8` (the WI-FI
   KEY keyboard against the stand-in `wifictl`), `wake.steps` (its one
   step is `wake`; *"After five idle minutes the first key only wakes the
   screensaver"*) for G-09, `match-dialog.steps:22` (`shot match-confirm`,
   a YES/NO box), `suite.txt:77` (`default-pre`), `claims.txt:59`, `:63`,
   `:67-68` (the keyboard's accepted boxes at the 1280x800 baseline
   `d72084ccad`; **no 640x480 keyboard frame is on record**, R3 § 4),
   `claims.txt:30` (the help bar's one accepted claim), `masks.txt`;
   `tools/vm-visual-qa:245-247` (`Monitor.sendkey(key, times, gap)` issues
   a plain press -- the input-config HOLD gap of G-08), `:381` (`dismiss_dialogs`
   presses `z` until the screen repeats: `GuiMsgBox`'s accelerator, every
   closing walk), `:598` (`wake` sends `shift`, ignored by the interface);
   the keys the image maps (`generic-x64-vm-testing.md` § Driving
   EmulationStation from the monitor): START = `ret`, A = `x`, B = `z`,
   X = `s`, Y = `a`, SELECT = `shift_r` -- so **the keyboard popup's `x`
   (CLEAR, L-14) is the monitor's `s`**. `tools/cloud-input-test` is **not**
   an input tool for this slice (R3 § 4: `wifictl` under bubblewrap and the
   phone page's JavaScript; 0 lines of `sendkey`, the monitor, `emulationstation`
   or `screendump`).
7. **The French**: 86 `_("` lines in 10 files (R2 cmd 8's 86; the proof's
   per-file line: `Window.cpp` 37, `GuiInputConfig.cpp` 14,
   `GuiTextEditPopupKeyboard.cpp` 11, `GunManager.cpp` 6,
   `GuiDetectDevice.cpp` 5, `InputManager.cpp` 4, `GuiMsgBox.cpp` 3,
   `GuiTextEditPopup.cpp` 3, `BindingManager.cpp` 2, `TextToSpeech.cpp` 1;
   97 occurrences; 61 distinct msgids), the pattern missing
   `pgettext("joystick", ...)` (`GuiInputConfig.cpp:11-40`, `:163`; 27
   `pgettext`/`ngettext` lines there and `GuiDetectDevice.cpp:42`'s
   `ngettext`) and `ngettext` (`:347`); **the French catalog is parsed for
   this slice's msgids** (the proof, 2026-10-31, at the pin): every one of
   the 61 has a non-empty `msgstr`, the 25 `pgettext` pairs and the 2
   `ngettext` pairs too, and the fork's own added msgid is one, `CLEAR`
   (`GuiTextEditPopup.cpp:34`, the keyboard's `:454`, `:491`) -> `EFFACER`
   (po `:6923`) -- the `Window.cpp` fork hunks add no `_("` literal; the
   lane re-runs the parser as its own line. `tools/es-untranslated`'s two
   tree-wide lines at this pin are `706 fork string(s) in the source, 706
   with French, 0 without` rc 0 against `bccd715707` and `703 fork string(s)
   in the source, 703 with French, 0 without` rc 0 against `cada856d86` (the
   proof, over the `qa-integration` checkout at the pin, `status --short`
   0), unchanged by this slice since it adds no msgid T33's run did not
   count; the tool sees only `_("...")` literals.
8. **The audits**, each on its lane's branch and in its folder, named here
   once and cited by section elsewhere (the tips are R1 C19's and R4 § 10's
   of 2026-10-30): **T2** `origin/feature/m6-es-launch-path-649`
   (`7041b0d710`; ES `55158d2a64`), `docs/audits/2026_10_23-epic-m6-es-launch-path/`
   (`02:61-62`, `:71`, `:83`, `:143`, `:178`, `:211`, `04:142`, `05:612`);
   **T18** `origin/feature/m6-es-cloud-pages-665` (ES `d55235d4b3`);
   **T20** `origin/feature/m6-es-achievements-pages-667` (`ffb6b686cb`;
   ES `5c0ddaaeef`), `docs/audits/2026_10_26-epic-m6-es-achievements-pages/`
   (`02:158`); **T21** `origin/feature/m6-es-state-and-bridge-668`
   (`82c67e99c5`; ES `3ae9610b0f`), `docs/audits/2026_10_26-epic-m6-es-state-and-bridge/`
   (`02:143`, `stage-e/syntax-check.sh:12-16`, `stage-e/fakes/` the 13);
   **T26** `origin/feature/m6-es-guimenu-673` (`bcfad2144b`; ES
   `757f5370ea`), `docs/audits/2026_10_27-epic-m6-es-guimenu/` (`02:51`,
   `:550`, `:735`, `:796`); **T31** `origin/feature/m6-es-pages-678`
   (`6ec4dda203`; ES `95852f8736`), `docs/audits/2026_10_27-epic-m6-es-pages/`
   (`02:141`, `:565`, `:640`, `tools/t31-build-tests.sh`); **T32**
   `origin/feature/m6-es-app-views-scrapers-679` (`1dd3093853`; ES
   `b52245036f`), `docs/audits/2026_10_27-epic-m6-es-app-views-scrapers/`
   (`02:180`, `:196`, `:378`, `tools/t32-build-tests.sh`,
   `stage-e/s0-syntax-pin.txt`); **T33** `origin/feature/m6-es-app-system-680`
   (`f802c55c62` the ES tip; the distribution tip `947ace1966` at the
   hand-back, `75f696b22d` at R4's read -- the lane records the one it
   reads), `docs/audits/2026_10_27-epic-m6-es-app-system/` (`00:162`,
   `02:99`, `:389`, `:730`, `:741` § What T34 to T37 inherit, `04:132`,
   `:135`, `05:502-513`, `tools/t33-build-tests.sh`, `stage-a/syntax-check.sh`,
   `stage-a/env.sh`, `stage-a/fakes/` the 13, `stage-c/pl25-screensaver.py`,
   `t33-streams.md:81`, `:147`, `:188`, `:203`); **T34**
   `feature/m6-es-core-components-681` (in flight; its folder at
   `22c0d5a2c2` held `00` and `stage-a/` only at R4's read, R4 § 9; its
   punch list is #1307), whose
   `02` § What T35 to T37 inherit (its brief `:1346-1355`: the `setOpacity`
   callers' read for this slice, the `components-tests` recipe, the tenth
   fake) is read mid-run when it lands; the older milestone audits'
   lines R4 § 9 names (`2026_09_13 02:291`, `2026_09_24 02:482`,
   `2026_09_25 02:199` F-ES-24). Read with `git -C <worktree> show
   <branch>:<path>`, never a checkout.
9. **The issues**: #682's own body; #1283, #1276, #1212, #1192, #1178,
   #54, #1270, #1305, #1307 (R4 § 4 and § 1's (g)); #585 (0 es-core lines in its
   body and comments, R4 § 5); #63, #65, #115, #149, #177, #178, #246,
   #283, #299, #48, #1137, #1138, #1141, #1192, #1195, #1245; #700, #680,
   #681. States as R4 read them on 2026-10-30: #1283, #1276, #1212, #1178
   OPEN `bug`; #1192 OPEN Backlog; #54 OPEN, no label; #1270 CLOSED (T33's
   audit issue, closed at its acceptance -- the proof's `gh` read of
   2026-10-31); #1307 OPEN `audit` `punch-list` (T34's, 43 findings; its
   PL-04 and PL-05 at body lines 10-11); #1305 OPEN `bug` (§ 1); #585 OPEN;
   #682 OPEN, 0 comments at the proof's read.
   The lane re-reads each with `gh --repo pixelelated/distribution issue
   view` at stage A and records the states it saw.
10. **Time to play**: `docs/vm-qa-log.md:9-18` (the three headline
    columns; *"No budget row exists yet"*); `time-to-play.md`'s one budget
    (the exit sync's 3 s, D-CLOUD-119). This slice sits on both paths at
    the frame and at the press: `Window::render` draws the cards and
    popups every frame (`:782-788`), `renderAsyncNotifications` holds the
    lock for the whole pass (`:1179`); `tools/time-to-play` measures the
    exit cell to *"the card leaving the screen"* (`card_gone`, its
    `:705-737`; the linger is this slice's `Window`), and the g2g cell's
    STOP IT AND PLAY is a `GuiMsgBox` of this slice (R3 § 4); on the launch
    path `Scripting::fireEvent("game-start")` scans six directories
    (`:158-207`) and `WatchersManager::pause` takes `mThreadLock` (L-19,
    T2 `02:83`). The retro's line names what the slice costs between a
    press and its frame on the guest, never "nothing".

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
leads are § 2's L-01 to L-27, cited here by number (their lines are the
table's and are not restated), and the floor's pure leads tabled at the end
of this section; each is read at its lines before it is called anything,
and the candidates marked FAIL-at-pin (§ 5) get their `git log -S` first
(`engineering-practices.md:83`); the upstream surfaces outside the lanes are
§ 1's list, read and recorded, fixed only under rule 6 (D-UI-079). For
this slice the natural homes (R3 § 5): the toast queue and the posted
functions under one lock, the watchers' lock and the detached storage
threads are *a lifetime or a thread*; the config file's in-place write and
the cached `exists` are *a read of a file another process writes*; the
second `BUTTON_GRID_HORIZ_PADDING` and the card's re-applied position are *a
house constant a surface does not keep*; the dialog's accelerator and the
help bar under a second page are *a prompt offered where the key moves
nothing*; the 86 `_("` lines and `GAMEPAD %i` are *a player sentence*;
`Window.cpp:29` and T21's CMake hunk are *a structure fact*.

- **Q1 The window's queue and its surfaces: one floating surface at a
  time** (`es-native-ui.md:144`, `:189-194`, `:207-222`;
  `es-player-text.md:135`, `:264`; D-UI-093, D-UI-105, D-UI-106, D-UI-109;
  the surfaces run). **L-01**: 3.14's extract seen to FAIL at the pin if
  two toasts queued under a card drain newest first (`back()`/`pop_back()`
  `:339-340`) against the comment's *"the order is the order things
  happened"* (`:334-335`) and D-UI-109's *"the order is the order things
  happened"*; the `git log -S 'pop_back'` of `c1c0d6ddc` first (the
  re-queue loop at `:1159-1166` pushes in popup order *because* the queue
  is LIFO, so a FIFO fix changes both); the contained fix a `front()`/`erase(begin())`
  with the re-queue loop reversed, or a record that the order is by
  design, ruled at the pause; a re-queued toast's **fresh default duration**
  `:1164` read against what the player was shown (a toast half-read then
  re-shown whole is defensible; said in `02`). **Item 14 / F-ES-24**: every
  toast is held while *any* card is up `:336-337`, the hasher's
  minutes-long card included (D-UI-079 keeps that card as upstream has
  it): the 2026-09-25 audit recorded it Low with no `04`/`05` line (R4
  item 14's `0`); this slice says whether it stands or is a bug, and the
  pause rules (a toast behind a long card is the one surface D-UI-093 and
  D-UI-078 together did not decide). **Item 13**: `:1183`, `:1192` read
  against `AsyncNotificationComponent.cpp:64`, `:112` (T34's): the 0.9 W
  centred position re-applied every frame, `:1192`, `:1205`, `:1221`,
  `:1224` the re-applications; G-02 measures the edges. **Item 15**:
  `GuiInfoPopup.cpp:17-18`, `:27-39`, `:47-50`, `:90-111`: the cap, the
  ellipsis, the fade (3.22); the words are the pages'. `notificationDuration`
  `:298-309` (3.15): the `audio.display_titles_time` setting's bounds.
  **L-22**: `es-native-ui.md:30`'s "top-right" against `:1192` -- a stale
  sentence for the coordinator's sweep (`tools/archaeology --reversal
  'top-right'`), not the lane's edit; recorded in `02` § The structure.
  A table: the queue's two containers and the lock, every enqueue, dequeue,
  layout and free (`:311`, `:324`, `:353`, `:365`, `:396`, `:418`, `:1152`,
  `:1177`, `:1236`), with the invariant each keeps and the frame that
  shows it.
- **Q2 The input's writes and the `<command>` execution**
  (`es-code-traps.md:127`; `upgrade-and-install.md:40`, `:58`; D-CLOUD-078;
  `handheld-evidence.md`; the input run). **L-06**: `es_input.cfg` and
  `es_last_input.cfg` written in place by `save_file` `:1225`, `:1232`
  while `AtomicFile::writeText` (`utils/AtomicFileUtil.h:42`, T21's) is
  registered in this slice's own CMake and called **zero** times in the 96
  (R2 cmd 13); a kill between the open and the write leaves a truncated
  mapping file -- the family of #102; the contained fix (`writeText` of
  pugixml's `save` to a string, or temp-and-rename) is put to the pause
  with T21 named for the API; **`Already written:`** is argued here, not
  assumed: a device with a half-written `es_input.cfg` today reads it as a
  parse error logged at `:1191-1194` and configures from scratch, which
  the fix does not change. **L-07**: 3.11's case with the real
  `FileSystemUtil.cpp` (T36's; T34's 3.21 shape): the miss at `:893`/`:1187`
  cached for the session, the file written at `:1225`, a second pad's
  `writeDeviceConfig` reading `exists` false and replacing the file with
  itself; seen to FAIL or PASS at the pin, the cache's erase cited from
  T36's rows (T34's brief names `FileSystemUtil.cpp:144`, `:185-195`,
  `:203-220`); a FAIL is a `bug` whose VM line is a unit case, since the
  guest has one keyboard device and no second pad (G-10's `CANNOT`).
  **L-08**: `doOnFinish` `:1242-1284` runs every `<inputAction
  type="onfinish">` `<command>` from `es_input.cfg` **synchronously on the
  UI thread** through `ProcessStartInfo(tocall).run()` `:1272` (3.13):
  what the distribution's `es_input.cfg` carries there (the lane greps
  `inputAction` in `projects/` and `packages/` -- a read, not a change),
  how long it holds the screen, and that a player's own edit of the file
  is an arbitrary command run by the interface: cost against value, and
  the quoting of its argument is Q5's executor. **L-09**: `hotkey` (the SDL
  fallback, `:1101-1108`) against `hotkeyenable` (the configuration page,
  `GuiInputConfig.cpp:73`, `:270-281`; `InputConfig.cpp:186-189`
  lower-cases): 3.12 documents both; which name the launch scripts read is
  T3's (`functions:128`), named for the pause, never read here as a defect
  of these lines alone. **L-10**: 3.10's extract: the two "Approximative
  device found" lines `:946`, `:960` print empty attributes (pugi's null
  node is safe); a one-line reorder under rule 6, a #585 line. **L-20**:
  `configureEmulators`'s blob (T2 FD-6/FD-7; the call `FileData.cpp:547`,
  T2's): the device names the kernel reports spliced inside the template's
  double quotes -- a name with `"`, `$` or a backtick breaks or expands the
  line; rule 6 on the blob's side (quote or reject the name), T3's on the
  template's; the cost of running it when `includeControllers == false` is
  priced (Q7). **Item 23 / #54**: `deinit` `:153-196` closes every joystick
  and `SDL_QuitSubSystem` `:188-189`; `Window::deinit` `:199-200` calls it
  when `deinitRenderer`; the sign-in window's grab is T18's lane, the
  handover named. **Item 24**: `buttonLabel` `:353-366` returns the key
  unchanged (3.8): the contract stated for T34's fix at
  `ComponentList.cpp:568`. **The hot-plug rebuild** `:374-630`:
  `mJoysticksLock` held `:485-623` while every joystick is opened and its
  config loaded, `writeDeviceConfig` called from inside it `:605` under
  `#if !defined(BATOCERA) || !defined(ROCKNIX)` `:585` (the lane states
  which branch the image compiles: `-DROCKNIX` is `CMakeLists.txt:132`'s,
  R3 § 3.2); `SDL_JOYDEVICEADDED` rebuilds then toasts, `REMOVED` toasts
  then rebuilds (`:849-877`): a frame's work on every hot-plug, priced. A
  table: every write site (R2 § 2.2's seven), its mechanism, atomic or
  not, the reader of what it writes and what a truncated file reads as;
  every `exists(` of the input files with its writer.
- **Q3 `WatchersManager`'s lock** (`handheld-evidence.md` § The
  hang-to-reboot path; `engineering-practices.md:111`; D-UI-078;
  #1283, #1276; the locks run). **L-11**: `run()` `:159-203` holds
  `mWatchersLock` `:181` across `item->component->check()` `:196`, so
  `GetComponent<T>()` (`.h:35`), `RegisterComponent` `:66`,
  `UnregisterComponent` `:78`, `ResetComponent` `:92-104` and the
  destructor `:143` -- every one called from the UI thread -- wait for a
  network or battery probe to return (T33 PL-14's es-core half; the
  callers `NetworkThread.cpp:58`, `:87-95`, T33's, and
  `GuiRetroAchievementsSettings.cpp:805-806`, R4 § 2); 3.1's case (a
  watcher whose `check()` sleeps; `ResetComponent` from a second thread
  measured to return only after it) seen to FAIL at the pin; the fix
  **named by T33 and shaped here under rule 6**: `check()` outside the
  lock with the `WatcherInfo`'s lifetime kept (EP-13: `UnregisterComponent`
  `:85-86` deletes it; a snapshot of due items under the lock, the
  `check()`s outside, a re-validation before `nextCheckTime` is written),
  `NotifyComponentChanged` `:197` still under `mNotificationLock` `:128`
  (lock order `mWatchersLock` -> `mNotificationLock`, never reversed by the
  fix); #1283's checkbox at its body line 18 waits for this slice's
  line-cited read of the fixed file in `stage-e/`. **`mRunning` and
  `mPaused`** plain `bool`s (`.h:85-86`), `mRunning = false` written `:151`
  outside any lock and read `:161`, `:172`, `:187`: a data race by the
  standard; 3.3's TSan run names it; `std::atomic<bool>` is a contained
  fix. **Notifications on the watcher thread** `:130-131`: what each
  `OnWatcherChanged` does (the fork's callers are T33's; this slice states
  the contract -- a listener that touches the interface must post). **The
  thread**: `new std::thread` `:61`, `join` `:154`, `stop()` `:20-27`
  deletes the singleton: against `main.cpp:1322` (`closing()`), `:1330`
  (`WatchersManager::stop()`), `:1358` (`window.deinit()`) (R4 § 2; #1276's
  context, the fix T33's S4a). **`pause`/`resume`** `:29-53` on the launch
  path (L-19): `mThreadLock` taken; priced with Q7. A table: every lock,
  every acquisition site with the thread that takes it and what it holds
  across, the lock order, and the UI-thread entry points that block.
- **Q4 Lifetimes: the window's teardown, its posted functions, its
  detached workers, and #1305** (`es-code-traps.md:22`, `:191`;
  `es-native-ui.md:358`; D-UI-078, D-UI-093; the lifetimes run).
  **L-02 / item 3 (T2 PC-1)**: `deinit` `:188-207` and `~Window` `:49-63`
  never free a card or a popup and leave the queue; the one free is
  `updateAsyncNotifications` `:1246-1248` when `isRunning()` goes false; a
  card alive at `deinit` is still in the vector at the next `init()`
  `:115-174` and drawn again; the raw holders are es-app's (R2 § 1.4's
  thirteen lines: `ContentInstaller.h:45`, `ProxyCards.cpp` x7,
  `ThreadedBluetooth.h:20`, `:43`, `ThreadedCloudSync.h:191`,
  `ThreadedHasher.h:50`, `GuiUpdate.h:59`) -- this slice states the
  teardown order against `main.cpp:1358` and what a holder may assume
  after it; T34 reads the card's half (its Q4, § 1 b) and files the `bug`
  if the window is proved, naming T18 and T20 for the callers; a
  contained fix (the cards freed in `deinit`, or a `close()` the component
  refuses after the window is gone) is the pause's. **L-03 / item 4 (T34
  L-12)**: `unregisterPostedFunctions` `:1262-1274` iterates and erases
  `mFunctions` **without** `mNotificationMessagesLock`, which
  `postToUiThread` `:1278` and `processPostedFunctions` `:1296` take;
  3.17's TSan extract names the race; the contract `postToUiThread`
  promises a poster that dies before the drain (nothing: the `void*` owner
  token and `unregisterPostedFunctions` are the poster's to call, and the
  fakes' `Window.h` runs posts at once, so no test at the pin exercises
  the queue) is written into `02`; T34's weak-token fix is put to the
  pause with T33's `AppWindow` gate (#1276, item 5) named. **L-04**: the
  four `std::thread(...).detach()` in `processStorageRequest`
  `:1554-1563`, `:1572-1575`, `:1608-1619`, `:1634-1637` capture `this`
  and call `ApiSystem` (es-core including es-app, `:29`, item 16): a read
  trace of what each touches on the interface thread after it finishes
  (its `GuiMsgBox` `:1558`, `:1614`, `:1623-1625`, `:1630-1640` posted or
  direct), upstream ROCKNIX's and outside the lanes -- recorded, a #585
  candidate only if a thread touches the window directly. **L-27 / #1305
  (T33 PL-25)**: the window's half of a three-sided fix -- `:777-779`
  starts the screensaver on `mTimeSinceLastInput` alone, so a slideshow
  can start while `GuiCloudTransfer` owns the screen; `cancelScreenSaver`
  `:1107-1138` (`resetCounts` `:1117`) is the only path that clears the
  screensaver's list; nothing in `removeGui` `:82-105` or in a rescan
  reaches the screensaver; T33's `stage-c/pl25-screensaver.py` FAILs at
  the pin with a heap-use-after-free in `selectGameMedia` (3.27, re-run
  unchanged); the rescan's half is T2's (`SystemData.cpp:459-473`), the
  list's own is T33's (`SystemScreenSaver.cpp:342-358`); the pause decides
  which half carries the fix (a window that holds the screensaver off
  while a page that owns the screen is top; a `resetCounts` on rescan; or
  the list's own clear), each named for its owner. **Item 9**:
  `deleteMeAndCall` `:286-294` copies the callback, `delete this`, then
  calls it -- the invariant T26's and T31's pages rest on; stated and kept.
  **Item 17 / #1212**: `:542-543` updates and `:287-288` feeds only the
  top page -- the invariant a T21 bug's "no wrong outcome" rests on;
  stated. **Item 30**: T32's `/quit` and `/messagebox` routes
  (`services/HttpServerThread.cpp:219`, `:545`) post their `GuiMsgBox`
  through `mWindow->postToUiThread` (`:229`, `:559`), so the constructor
  (fonts, the theme, `Renderer::getScreenWidth()` `:21-23`, `:53`) runs on
  the interface thread; recorded, no line for T32 (the proof).
  **L-24**: F4's `new SDL_Event()` never freed `:795`: one event per press,
  recorded (rule 6 if the pause wants it; a #585 line). A table: every
  `std::thread` (R2 cmd 10's 18 lines), every `.detach(` (4, all
  `Window.cpp`), every `delete this` in the slice (17 lines, the proof's grep:
  `GuiDetectDevice.cpp:99`, `:132`, `:145`; `GuiInputConfig.cpp:262`,
  `:288`; `GuiMsgBox.cpp:289`; `GuiTextEditPopup.cpp:33-35`, `:74`;
  `GuiTextEditPopupKeyboard.cpp:346`, `:352`, `:359`, `:395`, `:477`,
  `:494`, `:499`), every `postToUiThread` and its owner
  token, every raw pointer the window hands out (`createAsyncNotificationComponent`
  `:1169`) or holds (`mScreenSaver` `.h:147`, `mHelp`), who joins or frees
  it, what it touches on the interface thread.
- **Q5 `Scripting`'s quoting, and what runs the shell** (`es-native-ui.md:117`;
  `engineering-practices.md:111`; T2 FD-9/FD-19; #1192's second half;
  the scripts run). **L-18**: `executeScript` `:88-149` quotes the script
  path only when it has a space `:92-93`, strips `"` from every argument
  and quotes an argument only when it contains a space `:98-113`, no other
  escaping: 3.4's case with a `ProcessStartInfo` double shows `a$(id)b.zip`
  reaching the command string bare; the precondition is a player's own
  script in `scripts/<event>/` (the distribution ships none -- the lane
  greps `projects/` and `packages/` for `scripts/game-start` and records
  the count), so the class is a `bug` under rule 6 with a contained fix
  (`shellQuote` on every argument -- the tree's form is `FileData.cpp:1148-1151`,
  T2's; or an argv executor, #1192's second half, which is the better fix
  and the pause's call) and a #585 line. **L-18's second half**: on the
  device **every file** in a per-event directory runs (`:169-178`; the
  extension filter `:172-176` is WIN32-only), fire-and-forget except
  `quit` (`:142`), stdout/stderr to `es_script_stdout.log`/`es_script_stderr.log`
  `:145-146`; 3.5's case; a `.txt` left in the directory is executed by
  `sh` -- cost against value, recorded; the single-script pass `:182-207`
  filters to `.exe .cmd .bat .ps1 .sh .py` `:151` and passes the event
  name first `:205` (3.6). **L-19**: `fireEvent("game-start")` scans three
  per-event and three single-script directories on every launch, empty or
  not, the directory's `exists` cached `:193`: priced in Q7. **Item 20**:
  the fork's `maskSecrets` on the three WIN32-branch lines `:49`, `:122`,
  `:129`; the Linux branch `:138` logs the path only -- so the mask's reach
  on the image is nil and the 2026-09-24 audit's gap (*"a negative over
  the"* sweep) is answered here: the Linux log line carries no argument,
  the WIN32 lines are masked, the `LogDebug` at `:155` prints **the raw
  args** -- read whether a ROM path or a scraped name can carry a value
  (it cannot; a name is a name) and record it. **Q2's `<command>`**
  (`InputManager.cpp:1272`) shares the executor and is read with it. A
  table: the four `ProcessStartInfo` sites (R2 cmd 11), each with what
  builds its string, which parts are quoted, which thread runs it and
  whether it waits.
- **Q6 The popups' accelerator and padding, the help bar, and the words**
  (`es-ui-style-guide.md:169-178`, `:232`, `:296-304`; `es-code-traps.md:79-88`,
  `:134-136`; `es-native-ui.md:121`, `:179-183`; `es-player-text.md:29`,
  `:141`; D-UI-021, D-UI-034, D-UI-051, D-WORKFLOW-144; the input and
  strings runs). **L-12 / item 8**: the accelerator `:116-134` as the
  source has it (the only button; else the first named `OK` or `NO`; else
  **the last**), fired by an unconfigured keyboard's RETURN/ESC/SPACE
  `:249-254`, `BUTTON_BACK`, or **any `TYPE_BUTTON` from an unconfigured
  pad** `:257-261` -- a pad not yet configured presses *whatever is last*
  on any dialog it meets; 3.18's text lift states the three branches;
  G-04 and G-05 show the two outcomes; whether the fall-through stays in
  the component (T26 L-22's TRY AGAIN / CANCEL SIGN-IN lands on CANCEL
  SIGN-IN) is a style call for the pause, the component's half this
  slice's. **L-13 / item 6**: `GuiTextEditPopupKeyboard.cpp:14`'s
  `BUTTON_GRID_HORIZ_PADDING` at 0.0052083333 against `MenuComponent.cpp:14`'s
  0.022 (T34's) -- same macro name, two values, two files (3.19); the
  popup's per-key gap at 640 is 3.3 px against the bar's 14; the pause
  rules delete-and-widen (the key grid would grow 4.2x, R4 item 6) or keep
  the popup's own gap under its own name and correct T34's comment;
  recorded, not deleted here (`engineering-practices.md:576`); G-06's
  frame measures it. **L-14**: `x` on the keyboard `:392-397` and the CLEAR
  button `:491-496` commit `""` and delete the popup with no confirmation
  -- one press empties a cloud folder path, a hostname or a Wi-Fi key and
  submits it; `es-ui-style-guide.md:171` (a consequential action asks) and
  `least-surprise.md`: a `bug` candidate if G-06 shows the row's value
  gone after one `s`; the fix (CLEAR empties the field and leaves the
  popup open; or a YES/NO) is the pause's, with its French (D-UI-051).
  **L-15 / item 7 (#1192)**: neither popup class takes a masking mode
  (`.h:15-16`, `.h:13-14`); the field under them is `TextEditComponent`
  (T34's); the Backlog is the coordinator's, the lane states where the
  mode belongs. **L-16**: `TextToSpeech::say` three times in one constructor -- `:44` and
  `:234` say the text, `:240` the focused button's label (3.20): the second
  `say(text)` is a one-line fix under rule 6, a #585 line. **L-17**:
  `GAMEPAD %i` with `getDeviceId() + 1` `GuiInputConfig.cpp:134` -- the
  SDL instance id, not the player's seat (3.21): a player sentence that
  misleads; the fix (the player number from `computePlayersConfigs`, or
  the device name) is the pause's. **L-21 / items 10, 11, 12**: the help
  bar -- `:743-745` draws it only when `mGuiStack.size() < 2 ||
  !fullScreenMenus()`, `renderHelpPromptsEarly` `:999-1003` the hook a
  non-`MenuComponent` page uses (the save state manager, #149);
  `setHelpPrompts` `:1005-1078` merges and sorts (3.16); `GuiMsgBox::getHelpPrompts`
  `:296-299` delegates to `ComponentGrid` (T34's `canMoveCursor`, D-UI-034);
  the eight `mHelp->` lines (`:745`, `:1001`, `:1009`, `:1011`, `:1012`,
  `:1077`, `:1397`, `:1398`) call no `setOpacity`, so batocera's `9dbd4b9bf`
  guard has no caller here -- the callers' read is T34's for this slice
  (its § 5 item 3), taken up for the eight lines under D-WORKFLOW-162;
  G-04 and G-11 read which pages show a bar at 640 and 1280. **L-28 / T34 PL-05 (#1307, inherited)**: on the image at 1280x800 the
  tabbed SCRAPEUR page's help bar carried only FERMER and RETOUR, no SWITCH
  TAB and no row prompt, pixel-identical with a row or the strip focused;
  T34's seat traced SWITCH TAB through the pin's components
  (`ComponentTab.cpp:341`, `ComponentGrid.cpp:493`, `:522-552`,
  `MenuComponent.cpp:533`), so the empty bar is the window's bar collection
  (`setHelpPrompts` `:1005-1078`, the gate `:743-745`) or the image's
  composition: 3.16's extract over `setHelpPrompts` with a tabbed page's
  prompt list, and G-11's frame of a tabbed page's bar at 1280x800, say
  which -- the window's half is this slice's, the components' T34's. **L-29
  / T34 PL-04 / D-UI-133 (#1307, inherited)**: at 1280x800 the list's
  CHOISIR prompt drew its icon with 0 `Unknown help icon` lines in
  `es_log.txt` though the catalog carries `haut/bas` for `up/down` (po
  `:3708-3709`, T34's proof); why the window's bar did not show the
  component's `_()`-wrapped key (`ComponentList.cpp:568`, T34's fix site) is
  this slice's read: what `setHelpPrompts` `:1031-1041` does to a key it
  does not know (merged by icon, dropped, or passed through), stated for
  T34's fix. **Item 28**: `Window::input` `:215-290` hands a key to
  `peekGui()` alone `:287-288`
  after the `FirstJoystickOnly` filter `:220-232` and the screensaver block
  `:234-260`; `GuiComponent::input` `:54-63` iterates children with a
  saved `next_it`: the window's half of D-UI-021 stated, the strip T34's,
  the pages T31's. **The words**: the 86 `_("` lines (R2 cmd 8) against the
  catalog (item 7 of § 3; the parser run is the figure), the fork's own
  (`CLEAR` x3, the `Window.cpp` card lines) read for the four tiers and the
  two verbs (`es-player-text.md` § Conventions), `GuiDetectDevice.cpp:52`
  (HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT., with its period; po
  `:3779`) and `GuiInputConfig`'s 14
  prompts in both languages on the guest (G-07, G-08); `processStorageRequest`'s
  sentence-case dialogs `:1547-1548`, `:1601-1602` recorded as upstream's
  dialect (D-UI-079); the non-ASCII lines (the proof, `LC_ALL=C`): 28 lines in four files -- the
  keyboard's 22 glyph literals (`GuiTextEditPopupKeyboard.cpp:169-192`,
  which `es-code-traps.md:60` allows) and six upstream **comment** lines,
  `AudioManager.cpp:352`, `:362`, `:383`, `GunManager.cpp:145`,
  `InputManager.cpp:393`, `:1437` -- none on a line the fork added (its
  `-U0` diff against `cada856d86` adds 0), recorded and not fixed as
  `es-code-traps.md:60` says of an upstream hit; `InputManager.cpp:856`,
  `:869` are plain ASCII. A table: every `getHelpPrompts` and
  `input()` in the slice with the condition under which it offers or
  consumes a key; every `_("` line with its msgid and its French.
- **Q7 Cost against value, the structure and the merge debt**
  (`time-to-play.md`; `engineering-practices.md:12`, `:28`, `:576`;
  `es-code-traps.md:60`; D-UI-079, D-WORKFLOW-162, D-WORKFLOW-209; the
  membership, scope, delta, includes and non-ASCII runs). **The lens, asked
  of every upstream surface in § 1's list**: **L-05** the four
  keyboard-only Ctrl debug toggles `:262-281` with the `"Debug"` gate
  commented out -- a chord on an attached keyboard changes the screen with
  no setting; what each costs (a texture-debug overlay drawn every frame)
  against what it gives on a handheld (nothing: no keyboard); a `bug`
  candidate under rule 6 (the gate restored) or recorded, the pause's.
  **L-19** the six directory scans and `WatchersManager::pause` on every
  launch, priced from `docs/vm-qa-log.md`'s launch number and a
  `strace -c`-free read (the guest cannot time one `fireEvent`; `CANNOT`
  with that reason is allowed), **L-20**'s `configureEmulators` on every
  command build (T2 FD-6: *"small beside the launch"*), **L-23**
  `ThemeData::loadFile` throws on five conditions `:752-829` while
  `parseInclude` only warns on four `:1120-1146`, `getDefault` catches to
  `LogError` `:2246-2262` and `appendFile` to `LogWarning` `:2779-2798`: a
  broken include is a silent fallback, a broken root a logged one;
  upstream's parser, read for brittleness and recorded (no fork hunk, 25
  `LOG(Log` lines), `ThemeFileCache` `:719-743` under its mutex; **item
  27** `:267`'s `{ "multiLine", STRING }` entry read for T34's tile; the
  gun manager's `poll(..., 0)` every `updateGuns` `:922-930` and six
  `ioctl`s per gun `:978-991` on a device with no gun (the udev monitor
  idle); `VolumeControl`'s thread `:32`, `:203` and 32 `LOG` lines, the
  most in the slice; `FavoriteMusicManager.cpp:115`'s truncate-then-write
  (3.24, L-06's family, recorded); the on-screen keyboard's three layouts
  chosen from `system.language` `:141-152`. **The structure**: `Window.cpp:29`'s
  `#include "../es-app/src/ApiSystem.h"` (item 16, L-04) -- the one
  es-core to es-app include in the 96, resolving through `-I es-core/src`
  plus `../`, recorded with T34's disposition of its sibling; the include
  reach (R3 § 2.2: 18 SDL angle lines over the 101, 2 quoted `"SDL_mixer.h"`,
  51 non-standard angle includes with their guards -- `<libudev.h>` x3
  under `HAVE_UDEV`, `<pulse/pulseaudio.h>` under `_ENABLE_PULSE_` which
  the image takes (`package.mk:23`), `<libcec/*>` and `<espeak/*>` off);
  **whether `UDEV_FOUND` holds in the image build is `[unverified]`** (R3 §
  2.2: `package.mk:13` names no udev package; the proof found no
  `CMakeCache.txt` of an EmulationStation build under any
  `*/build.*/build/emulationstation-*/` on this host and M7's roots are
  never read, so the read that settles it is G-01's `ldd
  /usr/bin/emulationstation | grep -c udev` on the guest, `image` side --
  `CANNOT` until then); every
  T35 source named once and unconditionally in `es-core/CMakeLists.txt`
  (R3 cmd 21: `:147-171`, `if(` at `:278`, `:287`); **L-26** T21's
  `3ae9610b0` adds five registrations (R1 C21) -- the one lane-on-lane hunk
  inside the 96, the integration's, with `HttpText.{cpp,h}` and
  `RecoveryOutcome.h` falling to `rest` at T21's tip (§ 1 h); **L-25**
  `GuiTextEditPopupKeyboard.h`'s provenance footnote; the three `ROCKNIX` lines in the 96 (the proof's `git grep -n 'ROCKNIX'
  PIN -- <96>`): `Splash.h:10` `#if defined(ROCKNIX)`,
  `InputManager.cpp:585` `#if !defined(BATOCERA) || !defined(ROCKNIX)` and
  `Paths.cpp:76` `#if defined(ROCKNIX)` (R3 § 3.2 asked for the list). **Merge debt: none** on the 96 (§ 2's one
  line); **batocera's twelve** since `1750dded8c` on nine files, six of
  them fork-modified (R1 C17, C18; § 2), as the reconciliation list -- the
  input configs written for the launcher (`dbabd1adf`) against the fork's
  udev guards, the SIGTERM handler (`33016e55f`) and the logger build fix
  (`08ca272cb`) against the fork's per-batch flush, the `Window` and
  `GuiMsgBox` hunks against D-UI-093 and the wide box: the hunk ranges are
  the lane's `git diff 1750dded8c batocera/master -- <file>` per file,
  never a merge. **The #585 lines owed** (R4 § 5): T33's never-posted
  candidate for the lock; this slice's for the lock's fix, `Scripting`'s
  quoting, the controllers blob, the second padding constant if deleted,
  `GuiMsgBox`'s double `say`, the null-node logs, F4's leak -- each a line
  the lane writes in `02` for the coordinator to post, never sent
  (D-WORKFLOW-164/165). **The map**: no row of this slice's own; the
  checker's `SOURCE_DIRS` includes `es-core/src/guis` (§ 3 item 3), its
  per-file count quoted.

### The floor's pure leads, carried

The research ran no case (R3 § 7: *"no `-fsyntax-only` over any T35 file,
no build of any binary, no guest"*), so every row is a candidate until the
lane's stage C; the seams are in the shape `file:line at the pin | the
function | what a case would catch`, each a case in `CloudText`'s shape
(`es-code-traps.md:139`; § 5 item 1) built by the slice's binary with the
doubles R3 § 2.2 names -- the fakes' `Window.h`, `Log.h`, `LocaleES.h`
copied beside the source as `proxycards-tests` does, the test-defined
`Settings`/`Paths` bodies as `SystemConfTests.cpp` does, a
`ProcessStartInfo` double where a case must see the command string -- or
an *extract* (the function's text lifted into the case, `t33extract.py`'s
and `gpu-governor-save.py`'s shape) where the source is parse-only (R3
§ 2.2's third class: `Window.cpp`, `InputManager.cpp`, the six `guis/*`).
**The seven candidates the drafter marks FAIL-at-pin are in bold, and 3.27
is the one FAIL the research holds** (T33's record at `947ace1966`).

| # | At the pin | Function | What a case would catch |
| --- | --- | --- | --- |
| **3.1** | `watchers/WatchersManager.cpp:159-203` (`:181`, `:196`) | `run()` and `ResetComponent` `:92-104` | **a fake `IWatcher` whose `check()` sleeps 2 s; `ResetComponent` called from a second thread returns only after the sleep (L-11, #1283)**; pure, `Log.h` doubled; the fixed shape returns at once |
| 3.2 | `WatchersManager.cpp:76-90`, `:143-149`, `.h:67-73` | `UnregisterComponent`, the destructor | ASan: unregister during a running `check()`; the `WatcherInfo` freed `:86` while `:196` holds the item (EP-13); the fix's snapshot must re-validate |
| 3.3 | `WatchersManager.cpp:151`, `:161`, `:172`, `:187`, `.h:85-86` | `mRunning`, `mPaused` | TSan (`-fsanitize=thread`): the write at `:151` races the reads; `std::atomic<bool>` quiets it |
| **3.4** | `Scripting.cpp:88-149` (`:92-93`, `:98-113`) | `executeScript` with a `ProcessStartInfo` double | **`a$(id)b.zip` reaches the command string unquoted; `a b.zip` arrives quoted; a `"` inside an argument is stripped (L-18)**; the double records `tocall` |
| **3.5** | `Scripting.cpp:153-179` (`:169-178`) | `fireEvent`'s per-event pass | **a `notes.txt` placed in `<user ES>/scripts/game-start/` (a `Paths` double pointing at a temp dir) is handed to the executor on non-WIN32 (the filter `:172-176` is WIN32-only)**; the second pass `:182-207` refuses it (`:201-203`) |
| 3.6 | `Scripting.cpp:182-207` (`:151`, `:201-205`) | the single-script pass | `.sh`, `.py` run with the event name first; `.txt` skipped; a directory entry skipped `:198-199` |
| 3.7 | `InputConfig.cpp:186-189`, `:210-283`, `:285-345` | `mapInput`, `isMappedTo`, `isMappedLike`, `getMappedTo`, `loadFromXML`/`writeToXML` | `HotKeyEnable` stored as `hotkeyenable`; a hat is matched by bitmask, an axis by sign, else by id; a round trip through pugixml preserves every mapping; an unknown type is skipped with `LogError` `:297`, a value 0 warned `:305` (pugixml root, `SDL_joystick.h`/`SDL_keyboard.h` fakes, non-udev branch) |
| 3.8 | `InputConfig.cpp:353-366` | `buttonLabel` | the key returned unchanged for `up/down`, `haut/bas` and an unknown key (item 24; T34's fix is the caller's); PASS at the pin, the contract stated |
| 3.9 | `InputConfig.cpp:347-351`, `:403-414` | `AssignActionButtons` | `BUTTON_OK`/`BUTTON_BACK` swapped once under `InvertButtons`; called twice with the same setting, unchanged (idempotent) |
| **3.10** | `InputManager.cpp:889-972` (`:946`, `:960`) | `tryLoadInputConfig`'s approximate branches, extracted | **the two "Approximative device found" lines print empty `type`/`deviceGUID`/`deviceName` because `configNode` is read before `configNode = item` (L-10)**; pugixml, a `Log.h` double capturing the line |
| **3.11** | `InputManager.cpp:1179-1240` (`:1187`, `:1225`) with `utils/FileSystemUtil.cpp` (T36's) | `writeDeviceConfig`'s merge decision, extracted | **`exists(p)` miss, the file written by `save_file`, `exists(p)` again: false while the cache holds the miss (L-07; T34's 3.21 shape)** -- a second device's write then replaces the first's; PASS if the cache erases on the process's own write, cited from T36's rows |
| 3.12 | `InputManager.cpp:1004-1111` (`:1101-1108`) | `loadFromSdlMapping`, extracted | a mapping without `hotkey` gets `select` copied to `hotkey`; the configuration page writes `hotkeyenable` (L-09): the two names documented, no verdict |
| 3.13 | `InputManager.cpp:1242-1284` (`:1262`, `:1272`, `:1277`) | `doOnFinish`, extracted, with the `ProcessStartInfo` double | every `<inputAction type="onfinish">` `<command>` text handed to the executor as given, synchronously; a non-zero exit is a `LogWarning` (L-08) |
| **3.14** | `Window.cpp:324-351` (`:339-340`), `:1152-1175` (`:1164`) | `processNotificationMessages` and the re-queue, extracted | **queue [A, B] with a card up: nothing shown; card gone: B shown, then A (LIFO, L-01)**; a toast re-queued under a card returns with `notificationDuration(-1)`, not its remainder |
| 3.15 | `Window.cpp:298-309` | `notificationDuration` with a `Settings` double | `<= 0` -> `audio.display_titles_time` x 1000 when 2 < s <= 120, else 10,000; a positive value passed through |
| 3.16 | `Window.cpp:1005-1078` | `setHelpPrompts`, extracted | de-duplication by icon; `up/down` + `left/right` -> `up/down/left/right` `:1031-1041`; the sort dpad -> OK, x, y, l, r, BACK -> start/select `:1050-1075` |
| 3.17 | `Window.cpp:1262-1274` against `:1276-1290`, `:1292-1307` | `unregisterPostedFunctions` | TSan over an extract: unregister on one thread while `postToUiThread` runs on another (L-03); the fix takes the lock |
| 3.18 | `guis/GuiMsgBox.cpp:116-134`, `:246-264` | the back-button accelerator, lifted as text | the three branches present in the text (one button; `OK`/`NO`; the last); the behaviour is G-04's and G-05's (L-12) |
| **3.19** | `guis/GuiTextEditPopupKeyboard.cpp:14` against `components/MenuComponent.cpp:14` | the two `#define BUTTON_GRID_HORIZ_PADDING` | **a grep-shaped case: the macro defined in two files of the pin with the factors `0.0052083333` and `0.022` (L-13)**; the fix leaves one definition or two names |
| 3.20 | `guis/GuiMsgBox.cpp:44`, `:234`, `:240` | `TextToSpeech::say` in the constructor | the text count of `say(` in the constructor is 3 (L-16: the text twice, the focused button once); 2 after the fix |
| 3.21 | `guis/GuiInputConfig.cpp:134` | the `GAMEPAD %i` subtitle, lifted as text | `getDeviceId() + 1` is the argument (L-17); the fix's argument is the player's seat or the name |
| 3.22 | `guis/GuiInfoPopup.cpp:88-111` (`:98`, `:103-109`) | the fade, extracted | alpha 0 at t 0, 255 at 250 ms, falling from `duration - 250`, `mRunning` false past `mDuration`; `maxWidth` 0.9 W (`:17`) |
| 3.23 | `Log.cpp:60`, `:180`, `LogPolicy.h:1-55` | `AsyncLogger` against real files (the `SDL_timer.h` fake, `Settings`/`Paths` doubles as `SystemConfTests.cpp`) | every batch reaches the file before the worker sleeps (#178); WARNING and ERROR to stderr (`LogPolicyTests.cpp` holds the header's three functions already) -- the natural first binary (R3 § 2.2) |
| 3.24 | `FavoriteMusicManager.cpp:71`, `:115` | the favourites file's append and rewrite | parse-only (`Window.h`); lifted as text: `std::ios::trunc` then the write (L-06's family); recorded |
| 3.25 | `MameNames.cpp` (`:6` pugixml), `anim/ThemeStoryboard.cpp` | the parsers | a malformed file: what is warned, what throws; pugixml root, `ResourceManager.h` parsed and its `.cpp` doubled |
| 3.26 | `ThemeData.cpp:745-856`, `:1094-1150` | `loadFile`, `parseInclude` | parse-only (13 component headers to VLC): no host case; the throw/warn asymmetry recorded (L-23) |
| **3.27** | `Window.cpp:777-779`, `:1091-1138`; `SystemScreenSaver.cpp:342-358` (T33's); `SystemData.cpp:459-473` (T2's) | T33's `stage-c/pl25-screensaver.py`, re-run unchanged from `947ace1966` | **FAIL at the pin: a heap-use-after-free in `selectGameMedia` after the transfer's rescan (#1305)**; PASS only when one of the three halves lands |

## 5. The evidence floor

1. **Can this be done on the VM? Yes -- the host first, then one guest
   window granted on #682.** Every read, count and table runs on the host
   at the pin's bytes. **The host has no toolchain** (#1137):
   `tools/es-syntax-check` exits 2 on this host (`es-syntax-check: no build
   root at ... (ES_BUILD_ROOT, --root)`, its `:69`; R3 cmd 12) and records
   that line with `ES_BUILD_ROOT` set, never empty; **0 of the 44 `.cpp`
   were ever syntax-checked on the host** (T33's `stage-a/syntax-check.out`
   names 29 es-app files, four of which include `Window.h`, so **this
   slice's `Window.h`, `GuiComponent.h`, `InputConfig.h`, `InputManager.h`,
   `ThemeData.h` and `Log.h` have parsed under the 13 fakes transitively;
   no T35 `.cpp` body has**, R3 § 3.1). The host is `g++ (Ubuntu
   15.2.0-16ubuntu1) 15.2.0`, `cmake: none`, and none of `libudev.h`,
   `pulse/pulseaudio.h`, `espeak/speak_lib.h`, `libcec/cec.h`,
   `FreeImage.h`, `curl/curl.h`, `alsa/asoundlib.h` or an SDL directory
   exists under `/usr/include` (nine `No such file or directory`, R3 cmd
   17). The include graph, read not compiled (R3 § 2.2, § 3.3): **18 SDL
   angle includes over the 101 es-core files outside T34's and T36's
   directories, 0 VLC, 0 GL** (R3 cmd 4; two of the 18 are T21's,
   `HttpReq.cpp:9`, `SystemConf.cpp:17`), **2 quoted `"SDL_mixer.h"`**
   (`AudioManager.h:8`, `Sound.h:5`, R3 cmd 16), **51 non-standard angle
   includes** over the same 101 (R3 cmd 14) with their guards: `<libudev.h>`
   x3 under `HAVE_UDEV` (`GunManager.h:10`, `InputConfig.cpp:9`,
   `InputManager.cpp:26`; **whether `UDEV_FOUND` holds in the image build
   is Q7's `[unverified]`**, `CMakeLists.txt:255-258` and `package.mk:13`
   read; no `CMakeCache.txt` is reachable on this host (the proof), G-01's
   `ldd` settles it), `<pulse/pulseaudio.h>` under
   `_ENABLE_PULSE_` (`VolumeControl.cpp:14`; the image takes it,
   `package.mk:23 -DENABLE_PULSE=1`; the host parses the ALSA branch),
   `<libcec/*>` under `HAVE_LIBCEC` (off: `package.mk:22 -DCEC=0`),
   `<espeak/speak_lib.h>` under `_ENABLE_TTS_` (off), `<FreeImage.h>`
   (`ImageIO.cpp:4`, a fake), the WIN32 set (`<Windows.h>`, `<hidsdi.h>`,
   `<cfgmgr32.h>`, `<sapi.h>`, `<sphelper.h>`, `<mmdeviceapi.h>`,
   `<endpointvolume.h>`, `<mmeapi.h>`, never reached), the two `<SDL_syswm.h>`
   under WIN32 (`GunManager.cpp:25`, `Window.cpp:33`), pugixml in seven
   files/headers (`InputConfig.cpp:4`, `InputManager.cpp:10`,
   `InputManager.h:7`, `MameNames.cpp:6`, `ThemeData.h:16`,
   `anim/ThemeStoryboard.h:5`; T21's `Settings.cpp:7`), and two in-tree
   headers written with angle brackets (`InputConfig.h:5 <CECInput.h>`,
   `InputManager.h:8 <utils/Delegate.h>`). So the 44 fall in four classes
   (R3 § 3.3's table, **a prediction from includes, not a run**): **(a)
   pure, 14** (`math/*` 6, `animations/AnimationController`,
   `ThemeVariables`, `playlists/*` 2, `watchers/*` 3, `CECInput` in its
   no-CEC branch); **(b) through T36's `utils/*.h` only, 2** (`Paths`,
   `Scripting`); **(c) the pugixml root, 2** (`MameNames`,
   `anim/ThemeStoryboard`); **(d) one or two SDL fakes, 7** (`Log`,
   `PowerSaver`, `AudioManager`, `Sound`, `InputConfig`, `TextToSpeech`,
   `VolumeControl` -- the image's pulse branch not parsed); **(e) the
   headers that parsed in T33's TUs, 19** (`Window`, `GuiComponent`,
   `InputManager`, `GunManager` -- the udev branch not parsed --, `Splash`,
   `ThemeData`, `HelpStyle`, `BindingManager`, `FavoriteMusicManager`,
   `ImageIO`, `LocaleES`, `MultiStateInput`, `anim/StoryboardAnimator`, the
   six `guis/*`), 44 in all; the risk in (e) is an `SDLK_*` or
   `SDL_*Mutex` symbol used in a **body** that no header needed
   (`GuiMsgBox.cpp:250`, `GuiDetectDevice.cpp:94`,
   `GuiTextEditPopupKeyboard.cpp:350`), which the first rc 1 names; the
   proof's plain `g++` over a `git archive` of the pin: `GuiMsgBox.cpp` and
   `Window.cpp` die at `es-core/src/InputConfig.h:6:10: fatal error:
   SDL_joystick.h: No such file or directory`, `InputManager.cpp` at
   `InputManager.h:5:10` (the same header), while `WatchersManager.cpp`,
   `Scripting.cpp` and `math/Vector2f.cpp` parse plain, rc 0 -- classes (a)
   and (b) confirmed for three, `Scripting.cpp` needing no fake at all. **The
   SDL symbols the fakes must declare**: T21's `SDL_joystick.h` already
   carries `SDL_JoystickID`, `SDL_Keycode`, `SDL_Joystick`,
   `SDL_GameController`, `SDL_JoystickGUID`, the event ids,
   `SDL_PRESSED`/`RELEASED`, `SDLK_F3`/`F5`, the `Uint*`/`Sint*` typedefs,
   the five `SDL_HAT_*` masks, `SDL_mutex`, `Mix_Music`, `Mix_Chunk`, the
   ALSA typedefs and seven functions (R3 cmd 8); T32's one rc 1 was
   `'SDLK_r' was not declared` -- `SDLK_RETURN`, `SDLK_ESCAPE`,
   `SDLK_SPACE`, `SDL_GetKeyboardState`, `SDL_JoystickOpen` and the
   joystick query functions `InputManager.cpp:374-630` calls are the ones
   this slice's bodies will want, named by the first error. **The stand-in
   check** is T21's `stage-e/syntax-check.sh:12-16` (`g++ -std=c++17
   -fsyntax-only -DHAVE_INTL -I "$F" -I "$ES/es-app/src" -I "$ES/es-core/src"
   -I "$ES/external" -I "${PUGIXML_INCLUDE_DIR:?}" -I "${RAPIDJSON_INCLUDE_DIR:?}"`,
   `rc=$?` on its own line; R3 cmd 9) with T31's 13 fakes (§ 3 item 8;
   byte-identical in T21's `stage-e/fakes/`, T32's and T33's
   `stage-a/fakes/`, R3 cmd 8) copied under `stage-a/fakes/`, extended
   where the first error names a symbol, **and the pugixml root**, over
   all 44, `rc` per file recorded in T33's `syntax-check.out` shape; it
   parses the **non-udev, ALSA, no-CEC, no-TTS** branches (R3 § 3.2) --
   for CEC and TTS the image's; for pulse (certain) and udev (if
   `UDEV_FOUND`) **not** the image's, and the record says so; a
   `libudev.h` and a `pulse/pulseaudio.h` fake (declarations only) are the
   fourteenth and fifteenth fakes if the lane wants the image's branches
   parsed; `-DROCKNIX` is absent from the stand-in (`CMakeLists.txt:132`
   adds it in the image build), so `Splash.h:10-12`'s and
   `InputManager.cpp:585`'s branches are the lane's grep. **The pugixml
   root, said beside the check that needs it:** `external/pugixml` is a
   gitlink at the pin (`160000 commit 61c944895e071872370219cadade8423dc6e04dc
   external/pugixml`, R3 cmd 17), so an archive, a `git show` or a fresh
   clone carries no pugixml; the one root that works is the pin's extracted
   source `/workspace/cache/rocknix-sources/emulationstation/emulationstation-16dbac5211eea7e70db7394372033be2be7df829/external`
   (present on this host, R3 cmd 17; T33's `env.sh` also sets
   `CPATH=$PUGIXML_INCLUDE_DIR/pugixml/src` for bare `pugixml.hpp`
   includes); rapidjson at `/workspace/tmp/m6-coordinator/t21-s3/rapidjson/rapidjson-1.1.0/include`
   (present, R3 cmd 17) or the recipe's tarball unpacked under
   `/workspace/tmp/m6-t35/rj/` as T21, T32 and T33 did (no T35 file needs
   it; the script requires it). **The one cross-tree include resolves only
   through an include root**: `Window.cpp:29`'s `"../es-app/src/ApiSystem.h"`
   relative to the file is `es-core/es-app/src/ApiSystem.h`, which does not
   exist; `-I es-core/src` plus `../` is the tree root, which the stand-in
   supplies (R3 § 3.2).
   **The harness that exists: nothing compiles one of the 96.** The eight
   test targets of the two trees are § 3 item 5's (`es-unit-tests`,
   `es-file-tests`, `es-conf-tests`, `es-file-tests-win32`;
   `app-unit-tests`, `proxycards-tests`, `jobs-tests`, `bookkeeper-tests` --
   the last three with `fakes/` `BEFORE`, each copying the source under test
   into the build tree; R3 § 1.1, R1 C22-C24): **a T35 source compiled by a
   test target at the pin: 0 of 44**; the one of the 96 a test names is a
   comment (`es-app/tests/unit/CMakeLists.txt:30`) and the one a test
   includes directly is `LogPolicy.h` (`LogPolicyTests.cpp:13`); three fakes
   double this slice's headers (`Window.h`, `Log.h`, `LocaleES.h`; § 1 i),
   written for ProxyCards' tests by ES `1cf15dead` (R3 cmd 17);
   `es-app/tests/unit/fakes/` holds `SDL_timer.h` alone (`git ls-tree` at
   the pin, the proof; R1 C24 had not enumerated it), so a T35 binary under
   `es-app/tests/unit/` defines its own `Log`/`Paths` bodies as
   `SystemConfTests.cpp` does. **In the
   coordinator worktree nothing exercises a window or input surface by
   name:** `tools/vm-qa:63`'s sixteen suites name none; the 18 walks drive
   menus by key through `Window::input`; `tools/es-menu-map-check:50-58`
   reads menu constructors in `es-app/src/guis` **and `es-core/src/guis`**
   (§ 3 item 3); `tools/ra-ui-test:199` greps a guest's `es_log.txt` for
   `ProxyCards:|AsyncNotification`; `tools/time-to-play` measures the
   card's linger and the g2g dialog's answer (R3 § 4); the prior guest
   evidence is `docs/vm-qa-log.md:78`'s 21 card frames at 640x480 and
   `:107`'s help bar (`70 / 71` px at 640x480, `118 / 118` at
   1280x800), `claims.txt:59`, `:63`, `:67-68`'s keyboard boxes at
   1280x800; **not on record anywhere**: a 640x480 keyboard frame, a
   toast queued under a card, a dialog's back accelerator landing on its
   last button, the input-config flow (no walk reaches it, R3 cmd 11), a
   `WatchersManager` or `Scripting` line (the lane takes the per-name
   count over `docs/qa-logs/`'s 474 entries with `grep -rl -F <name>
   docs/qa-logs | wc -l` before claiming a zero; the drafter counted the
   entries, not the names).
   **The host floor is the lane's own: unit cases for the 27 seams** in
   `CloudText`'s shape (`es-code-traps.md:139`) -- **first the seven
   candidates and the one known FAIL** (3.1's lock wait, 3.4's unquoted
   argument, 3.5's `.txt` executed, 3.10's null-node log, 3.11's cached
   miss, 3.14's LIFO drain, 3.19's second constant; 3.27's screensaver
   script), each seen to FAIL against the unfixed extract before it is
   trusted, the stub checked against the unfixed code first
   (`engineering-practices.md:464`), then the rest. The cases are **built
   by the lane's generated script in T33's shape** (`t33-build-tests.sh`:
   the `python3 -I` parse of `es-app/tests/unit/CMakeLists.txt`, `g++
   -std=c++17 -O0 -g0 -pthread`, the include roots, the pugixml and
   rapidjson guards (exit 2 without), the `app-unit-tests` block under
   `-fsanitize=address,undefined`, the `TOTAL:` echo; R3 § 2.1; the five
   binaries at the pin are `es-unit-tests`, `es-file-tests`,
   `es-conf-tests`, `es-file-tests-win32`, `app-unit-tests`; T32's
   four-binary close read `TOTAL: 225 test cases in 4 binaries`, T33's
   five-binary total is in its own `02`), **extended to add a
   `window-input-tests` binary** in `es-conf-tests`' shape -- the real
   `.cpp` under test where it links (R3 § 2.2's first two classes:
   `WatchersManager.cpp`, `Scripting.cpp` with a `Platform.h` double,
   `InputConfig.cpp`, `Log.cpp`, `MameNames.cpp`, `anim/ThemeStoryboard.cpp`,
   the `math/`, `playlists/`), the extracts for the parse-only sources, the
   test file defining `Log`/`Settings`/`Paths` bodies, one fake SDL header
   first, its own `build` block with the fakes root (the script's "any
   other test" loop builds **without** a fakes root, R3 § 2.3) and its name
   in the `case` list -- saved as `docs/audits/<audit>/tools/t35-build-tests.sh`,
   **the total quoted as the script's `TOTAL: N test cases in B binaries`
   line** and never summed by hand (`engineering-practices.md:250`;
   T21's stage E was *"2 to 53 cases high"*). `tools/font-stems` prices a
   string's width at a pixel size for the image's face (read off the guest
   in G-01) -- the keyboard's key labels and `GAMEPAD %i` at 640 are
   numbers the host produces; it cannot run ES's `Font`. The counts and
   the generated tables run on the host.
2. **The guest window** -- one, asked for on #682 at stage B's end with its
   plan and bound (**30 minutes proposed, plus 5 of grace**: the plan below
   sums to 1,560 s, 26 minutes, by the drafter's `printf '%s\n' 60 240 0
   120 120 180 120 180 240 0 180 120 | awk '{s+=$1} END {print s}'` on
   2026-10-30, and the second boot is inside it; T34's window was 30 + 5
   for a 23.5-minute plan, T33's 25 + 5 for 21), granted explicitly by the
   coordinator on #682 and in the shared log's queue. **The queue is the
   shared file's own lines**, `/workspace/tmp/m7-m6-host-coordination.txt`
   (the durable successor of `/tmp/m7-m6-host-coordination-20261023.txt`,
   gone with the reboot of 2026-10-28; M7 writes timestamped lines, so the
   whole tail is read): a request is a line that names the slice, its
   plan and its bound; the grant is the coordinator's line answering it;
   the lane's START and RETURN each add a line with the census; the file
   is read before any guest starts (§ 1's last command, with the time of
   the read), and who holds the host is read there, with the time.
   **The conditions, stated here once -- T13's (#660, the first M6 lane to
   hold a guest window, whose shape every later window kept), beyond the
   rule file's own (§ 3's `generic-x64-vm-testing.md` rows):** one boot of
   the M6 copy of the image (`/workspace/artifacts/m6-t2-20261023/`,
   `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`,
   present on this host at T34's draft; the lane's `ls -l` is the line)
   **started at 640x480** (`generic-x64-vm run --headless --daemonize --res
   640x480`, #1141); **the image identified by two literals first**
   (`BUILD_ID` from `/etc/os-release` and the file name); **every verdict
   labelled by side** because the image's EmulationStation is M7's
   composition -- `pin-binary` only where the digest found the pin's lines
   unchanged against the image's binary, else `image`; the post contract
   `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as the first line of each
   post on #682 and a line in the shared host file, each with the census
   (`qemu N, compilers N`); **the START post names the detached timer that
   stops the guest at bound plus grace, or says that nothing does**
   (`engineering-practices.md` § A granted guest window names what stops
   the guest, #1135); the stop by pidfile (`tools/vm-stop`, never a
   pattern); the disk retired after with path, size and sha (D-INFRA-022);
   the guarded `tools/build-preflight --reclaim-swap` allowed once, before
   the guest, never beside it. **The second boot at 1280x800 is this
   slice's own need**: the keyboard popup is full-screen under
   `fullScreenMenus()` else 0.78 x 0.60 of the screen (`:8-9`), the
   dialogs' widths are fractions (`GuiMsgBox.cpp:21-23`), and
   `es-code-traps.md:266` asks for both sizes; a guest's size is QEMU's
   flag, so the second size is a second boot of the same disk. **The
   floor's limit, said plainly: a pad's hot-plug, hold or axis needs a
   pad, and the guest's input is a keyboard device and the HTTP API** (R3
   § 4: QEMU's monitor `sendkey` is a plain press, `vm-visual-qa:245-247`;
   no gamepad device is offered; `InputManager.cpp`'s joystick paths and
   `GunManager.cpp`'s udev paths run only with the hardware -- an `open
   item to test`, not a bug, with the harness gap named under
   `bugs-are-agent-first.md` rule 3: a `hold` step, or `sendkey <key> 1000`
   by hand over the monitor socket, which the lane may try once in G-08);
   CEC and TTS are compiled out; a second pad for L-07 is 3.11's unit case.
   None of these needs a device. The QA accounts are needed by no row
   (`tools/qa-accounts`, never printed; never the owner's, D-QA-015).
   Every proof's frames are labelled by side; a fix's frame is
   `fix-walk-pending-image`.

   | G | Behaviour only the running image shows | Walk or serial command | Expected frame or line | Bound (s) |
   | --- | --- | --- | --- | ---: |
   | G-01 | identity and side; the theme and the face; the input file | `vm-serial sh 'cat /etc/os-release; fbset; ls /usr/share/themes; find /usr/share -name "*.ttf" \| head; ls -l /storage/.config/emulationstation/es_input.cfg /usr/config/emulationstation/es_input.cfg 2>&1; grep -c inputAction /usr/config/emulationstation/es_input.cfg; ldd /usr/bin/emulationstation | grep -c udev'`; the ES binary's digest against the pin's lines (T26's `g01-identity.txt` shape) | `BUILD_ID=...`, `640x480`; the theme; the face path for `tools/font-stems`; whether the user `es_input.cfg` exists before any configuration (L-07's precondition) and how many `inputAction` lines the shipped one carries (L-08's); whether `libudev` is linked (1 or 0: the `UDEV_FOUND` answer, Q7's `[unverified]`, `image` side); every frame labelled `image` or `pin-binary` | 60 |
   | G-02 | a toast queued under a card, drawn in turn (D-UI-093, `Window.cpp:336-337`, `:1164`); the card at 0.9 W centred (`:1192`) | `default-pre` (`suite.txt:77`) with the WebDAV stanza seeded; reboot; the startup sync card over the carousel (`vm-qa-log:78`'s 21 frames are the precedent); a toast provoked while the card is up -- the games-list toast `Window.cpp:1505` by UPDATE GAMELISTS pressed from the menu, or the REBOOT REQUIRED toast of a setting toggled (the lane names which in its START post); `shot` at 0.4 s intervals for 6 s | the toast absent while the card is up, drawn after it leaves with its words intact; the card's left edge at x 32 and right at x 608 (0.9 x 640 = 576, centred; a stdlib `zlib` PNG reader, never by eye) -- `image` side | 240 |
   | G-03 | two toasts queued under a card shown newest first (L-01, `:339-340`) | -- | `CANNOT` in this window: no two-toast source the guest's keyboard can fire inside one card's lifetime (the pad connect/disconnect pair of `InputManager.cpp:856`, `:869` needs a pad, G-10); the proof is 3.14's extract | 0 |
   | G-04 | a YES/NO `GuiMsgBox`: back lands on NO (`GuiMsgBox.cpp:123-130`); the help bar under a second page (`Window.cpp:743-745`) | MAIN MENU > QUIT > RESTART EMULATIONSTATION; `shot`; press B (`z`); `shot`; the QUIT page itself framed for its bar | the dialog gone and EmulationStation still running (`vm-serial sh 'pgrep -c emulationstation'` unchanged across the press); the help bar carrying one CHOOSE (T34's G-03 measures the gap; this slice reads the outcome); on the QUIT page, a second-level page at 640 with full-screen menus, no bar from the Window (or the bar, and the page named) -- `image` side | 120 |
   | G-05 | a two-button dialog with neither OK nor NO: back lands on the **last** button (`:132-133`) | the lane picks one such dialog reachable on the unseeded guest and names it in its START post (T26 L-22's TRY AGAIN / CANCEL SIGN-IN needs a provider; a cloud row's refusal with a second verb, or `processStorageRequest`'s pair, read from the map first); `shot`; press B (`z`); `shot` | the last button's action taken by B -- the frame after names what happened; else `CANNOT: no two-button dialog without OK/NO is reachable without an account`, the candidates listed -- `image` side | 120 |
   | G-06 | the on-screen keyboard at 640x480: its layout, per-key gap (`GuiTextEditPopupKeyboard.cpp:14`, `:220`), START submits, ESC cancels, `x` clears and commits (`:392-397`) | `to-change-cloud-folder` then `confirm-cloud-folder` (their steps as written: START submits once); reopen the keyboard; `key esc`; `shot`; reopen; `key s` (= X); `shot` the PATHS page | the keyboard's frame with its key gap measured in columns (0.0052083333 x 640 = 3.33 px per quarter-pad, against the bar's 14); START closes it with the value kept; ESC closes it unchanged; **after `s` the popup is gone and the row's value is empty with no question asked** (L-14's positive) -- `image` side; the guest's SAVES FOLDER pointer is reseeded by `default-pre` after | 180 |
   | G-07 | the dialogs and the keyboard under French (D-UI-051): `kbFr` (`:45-70`), the YES/NO box, the detect page's sentence | `systemctl stop essway`; `system.language` set to `fr_FR` over serial (`generic-x64-vm-testing.md:1145`); ES started; G-04's dialog, G-06's keyboard, G-08's detect page; `shot` each | OUI/NON on the box; the French key labels and EFFACER (or the catalog's word for CLEAR, read from the `.po` first); the detect page's sentence in French at 640 without clipping -- `image` side | 120 |
   | G-08 | the input-config flow: HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT. (`GuiDetectDevice.cpp:52`, with its period), the hold, `GuiInputConfig`'s 14 prompts and `GAMEPAD %i` (`:134`) | CONTROLLER & BLUETOOTH SETTINGS (menu map `:134`): the configure row the lane reads from the page and names in its START post; `shot` the detect page; the hold: `sendkey x 1000` by hand over the monitor socket (the harness has no `hold` step, R3 § 4); `shot`; if the flow starts, each prompt row in turn with `key` presses, `shot` the subtitle | the sentence at 640 in both languages; whether a 1 s monitor hold registers (the detect page advances) -- if not, `CANNOT: the monitor cannot hold a key; harness gap named` under rule 3; if yes, the 14 prompts and the subtitle's number against the device id (L-17) -- `image` side | 180 |
   | G-09 | the screensaver's timer and the eaten wake press (`Window.cpp:777-779`, `:259-260`); #1305's window half: the screensaver over a page that owns the screen | UI SETTINGS > SCREENSAVER SETTINGS > SCREENSAVER AFTER to its minimum (T34's G-09 reaches the slider; the page is `## Not mapped` `:699`); wait; `shot`; `key shift` (ignored, the wake); `shot`; `key down`; `shot`; then with the stanza seeded: BACK UP SAVES TO THE CLOUD on the transfer page, left on its outcome, wait the timeout; `shot` | the dim or slideshow frame after the timeout; the carousel back and unmoved after `shift`; moved after the second key -- the eaten press made visible; **the screensaver starting over `GuiCloudTransfer`'s page, or not** (`:777-779` reads only idle time): the frame is #1305's window-half observation -- `image` side | 240 |
   | G-10 | a pad connected and disconnected: the two toasts (`InputManager.cpp:854-873`), the rebuild, the hot-plug `writeDeviceConfig` (`:605`) | -- | `CANNOT`: the guest offers no gamepad device and its keyboard is already configured; the paths are an `open item to test` with the harness gap named (a QEMU HID gamepad, if one exists, is the harness work to file) | 0 |
   | G-11 | the second size: the keyboard at 0.78 x 0.60 or full-screen (`:8-9`), the wide box (`GuiMsgBox.cpp:21-23`), the card at 1280x800 | `tools/vm-stop`; `generic-x64-vm run --headless --daemonize --res 1280x800` on the same disk; `vm-serial wait`; G-06's keyboard and G-04's dialog again; `shot` each | the keyboard's size against `fullScreenMenus()` at 1280x800 (the rule decides which branch); the dialog's width 0.6 or 0.8 of 1280 measured; the card not re-framed (`vm-qa-log:78`'s three frames stand) -- `image` side | 180 |
   | G-12 | close | `tools/vm-stop` on the pidfile; the disk's size and sha; `qemu 0, compilers 0` | `retired.txt`; the leftover check; the RETURN post inside bound plus grace | 120 |

   Sum of the bounds as written: 1,560 s (26 min), the drafter's figure by
   its own command. Every frame is read back for its strings; a
   measurement in pixels is made by a reader, not by eye.
3. **What T36 and T37 inherit** is written, not tested here: the slice's
   provenance table (1 / 12 / 83 with both bases named), the surfaces
   table (the queue's containers, lock, enqueue, dequeue, layout and free,
   with the invariant each keeps), the input table (every write site with
   its mechanism and atomicity, every `exists(` of the input files with its
   writer), the locks table (every lock, its acquisition sites and order,
   the UI-thread entry points that block), the lifetimes table, the scripts
   table (the four `ProcessStartInfo` sites), the `window-input-tests`
   build recipe (the doubles, the extracts, the pugixml root, the fakes the
   first errors forced), the stand-in's rc per file over the 44 with the
   branches it did not parse, the `exists` cache's answer (3.11) stated for
   T36's `FileSystemUtil`, and `Window.cpp:29`'s disposition.
4. **A fix lands only under a stream brief** at the stage-D pause, on the
   ES branch, proven twice (`fix-unit-test` through a case the build script
   links, or `fix-walk-pending-image`), the covering case run before every
   commit, under § 9's same-commit rules for the French; a fix that changes
   `Window.h`'s `postToUiThread` or `createAsyncNotificationComponent`
   signatures, `Log.h`'s `LogLevel` values or `LocaleES.h`'s macros names
   the three `tests/app-unit/fakes/` doubles and their three binaries as a
   collision in the hand-back (§ 1 i); a fix in `es-core/CMakeLists.txt`
   names T21's `3ae9610b0` hunk (§ 1 h).

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...* -- **the block below captures neither exit nor
time except where it says `rc=$?`; the lane wraps each run in its own
`rc=$?` line and a `date +%s` pair, or records that it did not**; a run
that cannot be made is `CANNOT` with its reason). From the distribution
worktree after the membership block; `W` the ES worktree (§ 1) -- **before dispatch, `W` is the `qa-integration` checkout at the pin, read by
`git -C` only, and every expectation below is a line R1, R2 or R3 printed at
the pin on 2026-10-30 by `git -C` against `qa-integration`, or the
stranger's proof printed on 2026-10-31 the same way, cited by its comment,
except the tool lines marked by stage** --
`PIN` the pin, `MB` the merge base, `FILES` the 96 from the block's paths
file; counts by `/usr/bin/grep` (#1138); **every grep for `_("` is `-F`**;
`rc=$?` on its own line, never after a pipe; **no `cut` truncates an
expected error line**. Every expectation is a printed line, except the
ones marked by stage, which cannot run before the lane writes their
inputs:

```bash
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-window-input-682; PIN=16dbac5211eea7e70db7394372033be2be7df829; G=/usr/bin/grep; C=8ebaf8daad; MB=cada856d86
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t35/tmp; mkdir -p "$TMPDIR"; df -i /workspace | tail -n 1
FILES=$(cat .qa-scratch/t35/paths.txt)
# the scope (expect 96; cpp 44; h 51; other 1 -- es-core/CMakeLists.txt; R1 C06)
printf '%s\n' $FILES | $G -c .; printf '%s\n' $FILES | $G -c '\.cpp$'; printf '%s\n' $FILES | $G -c '\.h$'; printf '%s\n' $FILES | $G -c -v -E '\.(cpp|h)$'
# the ES worktree at the pin, clean; the bases; the counts (expect the pin; 0; cada856d86; f6c542872e; b2ceb55a7e; 1750dded8c -- R1 C15, C17; then 725; 14; 1; 15 -- printed by the proof on 2026-10-31 at the same pin and refs; 531 without merges)
git -C "$W" rev-parse HEAD | cut -c1-10; git -C "$W" status --short | wc -l; git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10; git -C "$W" rev-parse rocknix/master | cut -c1-10; git -C "$W" rev-parse batocera/master | cut -c1-10; git -C "$W" merge-base "$PIN" batocera/master | cut -c1-10; git -C "$W" rev-list --count bccd715707.."$PIN"; git -C "$W" rev-list --count "$MB"..rocknix/master; git -C "$W" rev-list --count bccd715707.."$MB"; git -C "$W" rev-list --count upstream/master..rocknix/master
# the lines two ways (expect wc -l 22567; grep -c 22575; no trailing newline: 8, the files § 2 names; R1 C11)
for p in $FILES; do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l", s}'; for p in $FILES; do git -C "$W" show "$PIN:$p" | $G -c ''; done | awk '{s+=$1} END {print "grep -c", s}'; n=0; for p in $FILES; do a=$(git -C "$W" show "$PIN:$p" | wc -l); b=$(git -C "$W" show "$PIN:$p" | $G -c ''); [ "$a" != "$b" ] && { n=$((n+1)); echo "no newline: $p $a/$b"; }; done; echo "no trailing newline: $n"
# the fork's delta (expect `13 files changed, 247 insertions(+), 71 deletions(-)` three times -- R1 C13, C15, and C14 read from master's side; A 1; M 12 -- R1 C15's name-status; the 12 numstat rows; 19 commits with merges, 17 without, 2 merges -- R1 C16, the proof's lines)
git -C "$W" diff --shortstat bccd715707 "$PIN" -- $FILES; git -C "$W" diff --shortstat "$MB" "$PIN" -- $FILES; git -C "$W" diff --shortstat rocknix/master "$PIN" -- $FILES; git -C "$W" diff --diff-filter=A --name-only bccd715707 "$PIN" -- $FILES | $G -c .; rc=$?; echo "added rc=$rc"; git -C "$W" diff --diff-filter=M --numstat bccd715707 "$PIN" -- $FILES; git -C "$W" log --format=%h bccd715707.."$PIN" -- $FILES | $G -c .; git -C "$W" log --no-merges --format=%h bccd715707.."$PIN" -- $FILES | $G -c .; git -C "$W" log --merges --format=%h bccd715707.."$PIN" -- $FILES | $G -c .; rc=$?; echo "merges rc=$rc"
# upstream's delta: the merge-debt record (expect upstream commits 0 rc=1 and numstat 0 rc=1; identical to rocknix/master: 83; identical to cada856d86: 83; MB-vs-master identical: 96; batocera commits on the 96: 12; batocera files: 9; both-changed: 6 -- R1 C12, C14, C17, C18 and R1 § 3, every line printed by the proof on 2026-10-31)
git -C "$W" log --format=%h "$MB"..rocknix/master -- $FILES | $G -c .; rc=$?; echo "upstream commits rc=$rc"; git -C "$W" diff --numstat "$MB" rocknix/master -- $FILES | $G -c .; rc=$?; echo "upstream numstat rc=$rc"; n=0; for p in $FILES; do git -C "$W" diff --quiet rocknix/master "$PIN" -- "$p" && n=$((n+1)); done; echo "identical to rocknix/master: $n"; n=0; for p in $FILES; do git -C "$W" diff --quiet "$MB" "$PIN" -- "$p" && n=$((n+1)); done; echo "identical to cada856d86: $n"; n=0; for p in $FILES; do git -C "$W" diff --quiet "$MB" rocknix/master -- "$p" && n=$((n+1)); done; echo "MB-vs-master identical: $n"; git -C "$W" log --format=%h 1750dded8c..batocera/master -- $FILES | $G -c .; git -C "$W" diff --name-only 1750dded8c batocera/master -- $FILES | $G -c .; comm -12 <(git -C "$W" diff --name-only 1750dded8c batocera/master -- $FILES | sort) <(git -C "$W" diff --name-only "$MB" "$PIN" -- $FILES | sort) | $G -c .
# the other lanes' deltas inside the 96 (expect every stat line empty except T21's `es-core/CMakeLists.txt`, `1 file changed, 5 insertions(+)` -- R1 C20, C21, the proof's line; T34's `origin/` ref prints `fatal: bad revision` -- recorded, not a stop, R1 C19)
for b in m6-es-launch-path-649 m6-es-cloud-pages-665 m6-es-achievements-pages-667 m6-es-state-and-bridge-668 m6-es-guimenu-673 m6-es-pages-678 m6-es-app-views-scrapers-679 m6-es-app-system-680 m6-es-core-components-681; do echo "== $b"; git -C "$W" diff --stat "$PIN" "origin/feature/$b" -- $FILES 2>&1 | tail -n 1; done
# the strings, two ways (expect `_(" lines TOTAL 86 in 10 files` -- R2 cmd 8's 86, the proof's 10; the per-file -c: Window.cpp 37, guis/GuiInputConfig.cpp 14, guis/GuiTextEditPopupKeyboard.cpp 11, GunManager.cpp 6, guis/GuiDetectDevice.cpp 5, InputManager.cpp 4, guis/GuiMsgBox.cpp 3, guis/GuiTextEditPopup.cpp 3, BindingManager.cpp 2, TextToSpeech.cpp 1 -- R3 cmd 23 and the proof; the occurrence count 97)
git -C "$W" grep -c -F '_("' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "_(\" lines TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -F '_("' "$PIN" -- $FILES | wc -l; git -C "$W" grep -c -F '_("' "$PIN" -- $FILES | sed "s/^$PIN:es-core\/src\///" | tr '\n' ' '; echo
# the log lines (expect `LOG(Log lines TOTAL 158 in 20 files` -- R2 cmd 9; VolumeControl.cpp 32, ThemeData.cpp 25, InputManager.cpp 20, AudioManager.cpp 19 the four largest)
git -C "$W" grep -c 'LOG(Log' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "LOG(Log lines TOTAL", s, "in", NR, "files"}'
# the threads and the lifetimes (expect 18 matching lines -- R2 cmd 10: Log.cpp 60 180; Scripting.cpp 18 68; TextToSpeech.cpp 92, .h 47; VolumeControl.cpp 32 203; Window.cpp 1554 1563 1572 1575 1608 1619 1634 1637; watchers/WatchersManager.cpp 61, .h 88; `.detach(` 4, all Window.cpp -- R2 § 6; Scripting.cpp:68 is `new std::thread(&executeCommandsThread)` under WIN32, not a detach (the proof); `postToUiThread`: Window.cpp:1276 the definition, :1556 :1574 :1612 :1636 the calls, Window.h:91 (the proof))
git -C "$W" grep -n -E 'std::thread|\.detach\(|new std::thread|std::async' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'std::thread|\.detach\(|new std::thread|std::async' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F '.detach(' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F 'postToUiThread' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the process spawns (expect 4, all ProcessStartInfo: InputManager.cpp:1272, Scripting.cpp:43 :131 :140 -- R2 cmd 11; system( / popen( / runSystemCommand( 0 rc=1)
git -C "$W" grep -n -E '(^|[^A-Za-z_:])system\(|popen\(|runSystemCommand\(|ProcessStartInfo' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E '(^|[^A-Za-z_:])system\(|popen\(|runSystemCommand\(' "$PIN" -- $FILES | $G -c .; rc=$?; echo "shell spawns rc=$rc"
# the writes (expect 9 lines -- R2 cmd 13's seven write sites, InputManager.cpp:1225 :1232 save_file; FavoriteMusicManager.cpp:71 :115 ofstream; Log.cpp:179; AudioManager.cpp:539 :610 fopen; plus es-core/CMakeLists.txt:122 :257, the `AtomicFileUtil` registrations the alternation matches (the proof); AtomicFile:: 0 rc=1)
git -C "$W" grep -n -E 'std::ofstream|ofstream|AtomicFile|save_file\(|fopen\(|writeText|writeFile|std::rename|rename\(' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'std::ofstream|ofstream|AtomicFile|save_file\(|fopen\(|writeText|writeFile|std::rename|rename\(' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F 'AtomicFile::' "$PIN" -- $FILES | $G -c .; rc=$?; echo "atomic rc=$rc"
# the reads (expect `FileSystem::exists(` 41; uncached 0 rc=1 -- R2 cmd 12; the per-file list R2 § 2.3 names)
git -C "$W" grep -n -E 'FileSystem::exists\(' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -E 'FileSystem::exists\([^)]*,[[:space:]]*false' "$PIN" -- $FILES | $G -c .; rc=$?; echo "uncached rc=$rc"
# the input and the help bar (expect `getHelpPrompts` definitions 3 -- guis/GuiMsgBox.cpp:296, guis/GuiTextEditPopup.cpp:81, guis/GuiTextEditPopupKeyboard.cpp:449 -- and `input(InputConfig` definitions 6 -- GuiComponent.cpp:54, Window.cpp:215, guis/GuiDetectDevice.cpp:87, guis/GuiMsgBox.cpp:246, guis/GuiTextEditPopup.cpp:66, guis/GuiTextEditPopupKeyboard.cpp:335 (the proof); the eight `mHelp->` lines in Window.cpp: 745 1001 1009 1011 1012 1077 1397 1398 -- T34's brief `:1422`, R4 item 12; `mHelp->setOpacity` 0 rc=1)
git -C "$W" grep -n -E '::getHelpPrompts\(\)' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -E '::input\(InputConfig' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F 'mHelp->' "$PIN" -- es-core/src/Window.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'mHelp->setOpacity' "$PIN" -- es-core/src/Window.cpp | $G -c .; rc=$?; echo "mHelp setOpacity rc=$rc"
# the constants (expect the two BUTTON_GRID_HORIZ_PADDING definitions: components/MenuComponent.cpp:14 at 0.022 and guis/GuiTextEditPopupKeyboard.cpp:14 at 0.0052083333 -- R2 cmd 20; the keyboard's use at :220; GuiMsgBox.cpp:21-23 MSGBOX_WIDTH 0.6 / WIDE 0.8 / LINES 4; GuiInfoPopup.cpp:17-18 0.9f / 0.2f; Window.cpp:1181 PADDING_H, :1183 :1192 the card's position -- R2 § 1.3, § 4)
git -C "$W" grep -n -E 'BUTTON_GRID_HORIZ_PADDING' "$PIN" -- es-core/src/components/MenuComponent.cpp es-core/src/guis/GuiTextEditPopupKeyboard.cpp | sed "s/^$PIN://" | cut -c1-160; git -C "$W" grep -n -E 'MSGBOX_(WIDTH|WIDE_WIDTH|WIDE_LINES)|maxWidth|maxHeight|PADDING_H|posX = ' "$PIN" -- es-core/src/guis/GuiMsgBox.cpp es-core/src/guis/GuiInfoPopup.cpp es-core/src/Window.cpp | sed "s/^$PIN://" | $G -E '#define|const |float |posX' | cut -c1-160
# the includes (expect SDL/VLC/GL angle lines over the 101: 18 -- R3 cmd 4; quoted SDL: 2 -- R3 cmd 16; the cross-tree include: Window.cpp:29 -- R2 § 1.7; the named-once loop prints `named-0-times (or more than once): 9` -- seven entries named once with a trailing `# batocera` comment the anchor rejects (LocaleES.cpp, LocaleES.h, gettext.h, guis/GuiInfoPopup.cpp, guis/GuiInfoPopup.h, guis/GuiTextEditPopupKeyboard.cpp, guis/GuiTextEditPopupKeyboard.h) and two headers registered nowhere (HelpPrompt.h, Scripting.h); every .cpp of the 44 named once (the proof; R3 cmd 21's claim held for the sources); `if(` at 278 287 -- R3 cmd 21)
git -C "$W" grep -n -E '#include <SDL|#include <vlc|#include <GL' "$PIN" -- es-core/src | $G -v -E 'components|utils|resources|renderers' | $G -c .; git -C "$W" grep -n -E '#include "(SDL|vlc|GL|curl|libudev)' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -E '^\s*#\s*include\s*"\.\./' "$PIN" -- $FILES | sed "s/^$PIN://"; n=0; for p in $FILES; do [ "$p" = es-core/CMakeLists.txt ] && continue; b=${p#es-core/}; git -C "$W" grep -c -E "/${b}[[:space:]]*\$" "$PIN" -- es-core/CMakeLists.txt | sed "s/^$PIN://" | $G -q ':1$' || { echo "not once: $p"; n=$((n+1)); }; done; echo "named-0-times (or more than once): $n"; git -C "$W" grep -n -E '^\s*if\s*\(' "$PIN" -- es-core/CMakeLists.txt | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo
# the in-source gates (expect 128 lines (the proof), the ROCKNIX, BATOCERA, WIN32, HAVE_UDEV, _ENABLE_PULSE_, HAVE_LIBCEC, _ENABLE_TTS_ guards of R3 § 2.2 and R2 § 0 among them -- Splash.h:10, InputManager.cpp:585, VolumeControl.cpp:11 (its include :14), CECInput.h:7 (:8), TextToSpeech.cpp:53 (:54); `git grep -n ROCKNIX` over the 96: 3 lines, InputManager.cpp:585, Paths.cpp:76, Splash.h:10)
git -C "$W" grep -n -E '^\s*#\s*(if|ifdef|ifndef|elif)\b.*(ROCKNIX|BATOCERA|WIN32|HAVE_UDEV|_ENABLE_PULSE_|HAVE_LIBCEC|_ENABLE_TTS_|_RPI_)' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the non-ASCII bytes (expect 28 lines rc=0 under LC_ALL=C; files with a non-ascii byte: 4 -- AudioManager.cpp 3, GunManager.cpp 1, InputManager.cpp 2, guis/GuiTextEditPopupKeyboard.cpp 22, the glyph literals es-code-traps.md:60 allows; files with a non-ascii comment line: 3 -- AudioManager.cpp:352 :362 :383, GunManager.cpp:145, InputManager.cpp:393 :1437, every one upstream's: the fork's -U0 diff against cada856d86 adds 0 (the proof); InputManager.cpp:856 :869 are ASCII)
git -C "$W" grep -n -P '[^\x00-\x7F]' "$PIN" -- $FILES | $G -c .; rc=$?; echo "git grep -P rc=$rc"; n=0; for f in $FILES; do c=$(git -C "$W" show "$PIN:$f" | LC_ALL=C $G -c -P '[^\x00-\x7F]'); [ "$c" != 0 ] && { echo "${f#es-core/src/}:$c"; n=$((n+1)); }; done; echo "files with a non-ascii byte: $n"; n=0; for f in $FILES; do c=$(git -C "$W" show "$PIN:$f" | LC_ALL=C $G -c -P '^\s*//.*[^\x00-\x7F]'); [ "$c" != 0 ] && { echo "comment: ${f#es-core/src/}:$c"; n=$((n+1)); }; done; echo "files with a non-ascii comment line: $n"
# the French (expect six lines -- CANCEL 49, GAMEPAD %i 3898, SET SELECT AS HOTKEY 3915, DO NOT ASSIGN HOTKEY 3918, the detect sentence with its period 3779, CLEAR 6923 (the proof; HOTKEY ENABLE is no msgid, the key is the identifier HotKeyEnable); `^msgid ` lines 2207 -- T34's brief `:1416` at the same pin; es-untranslated `706 fork string(s) in the source, 706 with French, 0 without` rc 0 and `703 ... 0 without` rc 0 -- the proof, over the qa-integration checkout at the pin)
git -C "$W" grep -n -E '^msgid "(CLEAR|CANCEL|HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT\.|GAMEPAD %i|SET SELECT AS HOTKEY|DO NOT ASSIGN HOTKEY)"$' "$PIN" -- locale/lang/fr/LC_MESSAGES/emulationstation2.po | sed "s/^$PIN://" | cut -d: -f2,3 | tr '\n' ' '; echo; git -C "$W" grep -c -E '^msgid ' "$PIN" -- locale/lang/fr/LC_MESSAGES/emulationstation2.po | sed "s/^$PIN://"
out=$(tools/es-untranslated --es-src "$W" --upstream bccd715707 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated rc=$rc"
out=$(tools/es-untranslated --es-src "$W" --upstream "$MB" 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated(cada) rc=$rc"
# the candidate lines (expect Window.cpp `339 340` for back()/pop_back(); `1164` for notificationDuration(-1); WatchersManager.cpp `181` for the unique_lock and `196` for check(); Scripting.cpp `92 93` and `109 112` for the quoting; InputManager.cpp `946 960` for the two approximate logs, `1225 1232` save_file; GuiMsgBox.cpp `44 234` say; GuiInputConfig.cpp `134` -- R2 §§ 1-5)
git -C "$W" grep -n -E 'mNotificationMessages\.(back|pop_back)\(' "$PIN" -- es-core/src/Window.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'notificationDuration(-1)' "$PIN" -- es-core/src/Window.cpp | sed "s/^$PIN://" | cut -d: -f2; git -C "$W" grep -n -E 'unique_lock<std::mutex> lock\(mWatchersLock\)|component->check\(\)' "$PIN" -- es-core/src/watchers/WatchersManager.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'Approximative device found' "$PIN" -- es-core/src/InputManager.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'save_file(' "$PIN" -- es-core/src/InputManager.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'TextToSpeech::getInstance()->say(' "$PIN" -- es-core/src/guis/GuiMsgBox.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'getDeviceId() + 1' "$PIN" -- es-core/src/guis/GuiInputConfig.cpp | sed "s/^$PIN://" | cut -d: -f2
# the menu map (expect `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` rc 0 -- T34's brief `:1424` at the same pin, the map 989 lines and unchanged since; the checker's SOURCE_DIRS at its :58 include es-core/src/guis)
out=$(tools/es-menu-map-check --es-src "$W" --ref "$PIN" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-menu-map-check rc=$rc"; wc -l docs/es-menu-map.md; sed -n '58p' tools/es-menu-map-check
# the compile (expect `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2 -- R3 cmd 12, #1137; plain g++ on GuiMsgBox.cpp rc 1 with `es-core/src/InputConfig.h:6:10: fatal error: SDL_joystick.h: No such file or directory` -- printed by the proof for this file over a `git archive` of the pin (g++ 15.2.0; Window.cpp the same line, InputManager.cpp at InputManager.h:5:10; WatchersManager.cpp, Scripting.cpp, math/Vector2f.cpp rc 0 plain), as R4 item 25 and T31 `02:565` predicted; the pugixml root present -- R3 cmd 17; then the stand-in check over the 44 with the fakes, rc per file, R3 § 3.3's classes the prediction)
F=es-core/src/guis/GuiMsgBox.cpp; out=$(ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" "$F" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-syntax-check rc=$rc"
out=$(g++ -std=c++17 -fsyntax-only -DHAVE_INTL -I "$W/es-app/src" -I "$W/es-core/src" -I "$W/external" "$W/$F" 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 -E 'fatal error|error:'; echo "plain g++ rc=$rc"
PUGI=/workspace/cache/rocknix-sources/emulationstation/emulationstation-$PIN/external; test -d "$PUGI/pugixml/src" && echo "pugixml root present"
# STAGE C -- the lane's scripts, which do not exist at stage A (expect the stand-in's `<file>: rc N` line per .cpp, 44 lines; the build script's own `TOTAL: N test cases in B binaries` with 0 failed and `window-input-tests` among the binaries; before any fix the candidates' FAIL lines by name and 3.27's script FAILing at the pin)
bash docs/audits/*-epic-m6-es-core-window-input/stage-a/syntax-check.sh 2>&1 | tail -n 46
bash docs/audits/*-epic-m6-es-core-window-input/tools/t35-build-tests.sh "$W" 2>&1 | tail -n 10
python3 -I docs/audits/*-epic-m6-es-core-window-input/stage-c/pl25-screensaver.py "$W" 2>&1 | tail -n 3
# STAGE A, after the pointer is read -- the removal check: TIPHASH is the lane's own tip the pointer and the dispatch comment name (MERGE_HASH at stage A); the literal word fails with `fatal: bad revision 'TIPHASH'` (expect empty) and the ES diff against the pin (expect empty before stage E)
git diff --stat TIPHASH HEAD -- packages projects tools | tail -n 1; git -C "$W" diff --stat "$PIN" HEAD | tail -n 1
```

Every expectation above is a research file's printed line or the stranger's
proof's of 2026-10-31, cited in its comment; the proof's own are the four
`rev-list` counts, the `--no-merges`/`--merges` counts, the upstream-delta
zeros and the MB-vs-master 96, the `comm -12` 6, T21's stat line, the
occurrence count, the `getHelpPrompts`/`input(` definition counts, the gate
and `ROCKNIX` lists, the non-ASCII counts, the catalog lines, the
`es-untranslated` lines and the plain-`g++` first error. The lane re-runs
every one as its own line; a line that differs is recorded beside the
expectation, not argued with.

## 6. Outputs

As T26's, T31's, T32's, T33's and T34's briefs § 6; § 7 is this section as
checkboxes. The folder `docs/audits/<yyyy_mm_dd>-epic-m6-es-core-window-input/`:
`00-running-log.md` to `05-punch-list.md`; `second-opinions/`
(`review-plan.json`, the probe's and the refutation's `.provenance.json`,
`packet-manifest.json`); `stage-a/` to `stage-e/` (the first commands and
the § 5 runs under `stage-a/`, with T31's 13 fakes and any fake the first
errors forced under `stage-a/fakes/`, the stand-in's `syntax-check.sh`
and its `syntax-check.out` with one `rc` line per `.cpp`; the window plan
under `stage-b/`; the host proofs under `stage-c/`, T33's
`pl25-screensaver.py` re-run among them with its FAIL line; the walks'
steps under `stage-e/walks/`); `tools/` (the generators --
`t35-includes.py`, `t35-build-tests.sh`, the tables' generators -- each
asserting its counts and each seen to exit 1 on a constructed drift
before it is trusted); `guest-cycle/`; the lint before D; the audit issue
(`Audit: M6 T35 EmulationStation's window, input and the rest of es-core
-- N findings (...)`, a sub-issue of #682; the audit issue and the bugs are
the lane's, D-WORKFLOW-189; a Backlog for a lead outside the 96 is the
coordinator's, named in the hand-back); and the retro at
`docs/retros/<date>-m6-es-core-window-input.md` (**what the slice did to
the two time-to-play numbers**, § 3 item 10's per-frame and per-launch
work priced from the guest and cited from `docs/vm-qa-log.md`, never
"nothing" by default; **what T36 and T37 inherit**, § 5 item 3).

**`02-forward-audit.md` carries these sections, in this order, each
generated section's row count stated as "generated, asserted" by the
script that made it:** § Coverage (96 rows, the path in backticks as the
first cell, both tiers: fork-added 1 / fork-modified 12 / upstream-carried
83 and inventory 13 / 83), § The leads (L-01 to L-27 and 3.1 to 3.27, each
with its lines, its family, who owns it, its disposition), § The surfaces
(the queue's two containers and the lock; every enqueue, dequeue, layout
and free with the invariant each keeps and the frame that shows it; the
card's position against T34's component), § The input (every write site
with its mechanism and atomicity and what a truncated file reads as; every
`exists(` of the input files with its writer; the two hotkey names; the
hot-plug rebuild's cost), § The locks (every lock, its acquisition sites
and order, the UI-thread entry points that block, the thread's start and
stop against `main.cpp`'s order), § The lifetimes (every thread, detach,
`delete this`, post and raw pointer the window hands out or holds, who
joins or frees it, what it touches on the interface thread; #1305's
three halves), § The scripts (the four `ProcessStartInfo` sites, what
builds each string, which parts are quoted, which thread runs it and
whether it waits), § The words (the 86 lines with their msgids and
French, the fork's own read for the tiers and the verbs, `GAMEPAD %i`,
the glyph literals, the sentence-case dialogs recorded as upstream's),
§ The structure (`Window.cpp:29`, the include reach and the branches the
host did not parse, the unconditional CMake lists and T21's hunk, the
`ROCKNIX` gates, L-22's stale rule sentence, L-25's footnote, the map's
checker line and per-file count), § The merge debt (one line: `cada856d86`
the base against `rocknix/master` `f6c542872e`, `bccd715707` its parent
and the stale `upstream/master`, the upstream commit count on the 96 of
0 (14 on any path), 83 of 96 blobs identical pin to master and 96 of 96 base to master,
batocera's twelve since `1750dded8c` on nine files, six fork-modified, as
the reconciliation list only), § The runs, § The guest cycle, § The
streams (stage E: **written by the coordinator after stage D, as for T21,
T26, T32, T33 and T34**; the lane leaves the heading and the pause's
dispositions), § Positives, § The #585 lines owed (one per upstream-carried
defect closed under rule 6, in the shape the lane writes, never sent;
T33's lock candidate and this slice's named for the coordinator), § What
T36 and T37 inherit; every proof with `proved:`. The stage-D pause as
T21's: the punch list posted on #682, the lane waits for the coordinator's
dispositions and any stream brief.

## 7. Acceptance

The checklist on #682 becomes this section at dispatch, written there by
the coordinator in place of P1's generated ones (its fifth, naming
`tools/renovation-status`, is replaced by checkbox 5 below as T33's and
T34's were). Every checkbox names the artifact that ticks it (D-QA-044);
the coordinator ticks at acceptance, from the artifacts, never from the
hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-es-core-window-input/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `second-opinions/`, `stage-a/` to `stage-e/`, `tools/` and `guest-cycle/` (`ls` of the folder in the hand-back).
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-es-core-window-input/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`), and the same with `--issue <audit issue>` prints `PASS`; Q1 to Q7 are answered in `04-analysis.md` and every punch item carries `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: independent` and one reviewer (`gpt`, `openai/gpt-6-astra`, `max`); its probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named (read directly); `packet-manifest.json` carries the scan block with every hit dispositioned by file:line (library plumbing / macro name / identifier / setting name) and no value, the 13 fork-added and fork-modified files whole and every cited range of the 83 named; `00` shows exactly two keyed invokes.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #585, #649, #665, #667, #668, #673, #678, #679, #680, #681, #683, #54, #63, #65, #1192, #1212, #1276, #1283, #1305, an M7 issue by number), withdrawn or recorded as written with its reason; `tools/box-check --issue <audit issue>` prints 0 fail; the issue is closed by the coordinator at acceptance.
- [ ] `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` in #682's header carry the lane's commits; the ES read is on the pin's bytes for the 96 files (`git -C <W> diff --stat 16dbac5211 <reviewed-at-es> -- $(cat .qa-scratch/t35/paths.txt)` empty before stage E) and nothing under the distribution's `packages/`, `projects/` or `tools/` changed at any stage against the lane's own dispatch tip (the pointer's merge hash, never `2174265e9c`).
- [ ] `01-research-notes.md` § Scope records § 2's block with its exact output lines (`mine: 96 paths.txt: 96 equal: True`; `lines: 22575 reach: {'shipped': 96} tier: {'fork-own': 13, 'upstream-carried': 83} lang: {'cmake': 1, 'c-header': 51, 'c++': 44}`; `fork-own lines: 6759`; `read lines: 22575`; `wc -l 22567` and `grep -c 22575` with the eight files without a trailing newline; 95 at the merge base and 95 at the base (`LogPolicy.h` absent from both); `13 files changed, 247 insertions(+), 71 deletions(-)` three times -- or the deltas beside them) and names `cada856d86` as the merge base against `rocknix/master` with `bccd715707` as its parent and `1750dded8c` as the base against `batocera/master`.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `96`; its tier columns read fork-added 1 / fork-modified 12 / upstream-carried 83 and inventory 13 / 83.
- [ ] `02` § The runs records the counts with both rules where they differ -- `_("` 86 lines in 10 files and 97 occurrences; `LOG(Log` 158 lines in 20 files; `FileSystem::exists(` 41 lines, 0 uncached; thread lines 18 with `.detach(` 4 (`Window.cpp:1563`, `:1575`, `:1619`, `:1637`; `Scripting.cpp:68` is a `new std::thread` under WIN32, not a fifth) and `std::thread` at `Log.cpp:60`, `VolumeControl.cpp:32`, `TextToSpeech.cpp:92`, `WatchersManager.cpp:61`; `ProcessStartInfo` 4 and shell spawns 0; the writes grep 9 lines (7 write sites and the 2 CMake registrations) and `AtomicFile::` 0; SDL angle includes 18 over the 101 and quoted 2; the cross-tree include `Window.cpp:29`; every T35 `.cpp` named once in `es-core/CMakeLists.txt` (the two unregistered headers, `HelpPrompt.h` and `Scripting.h`, and the seven `# batocera` lines recorded) with `if(` at `:278`, `:287` -- each as a command's own output line, or the lane's figure with the command that differs named.
- [ ] `02` § The surfaces, § The input, § The locks, § The lifetimes and § The scripts are each generated or asserted by a script under the audit folder's `tools/` that names its row count ("generated, asserted"), and `02` § The runs records each script seen to exit 1 on a constructed drift before it was trusted.
- [ ] `02` § The surfaces has one row per enqueue, dequeue, layout and free of the toast queue and the card vector (`Window.cpp:311`, `:324`, `:353`, `:365`, `:396`, `:418`, `:1152`, `:1177`, `:1236`) with the invariant it keeps and the frame that shows it; the queue's order (`:339-340`) and the re-queued toast's duration (`:1164`) each with a disposition and, where a bug, 3.14's FAIL line; `:1183`, `:1192` read against `AsyncNotificationComponent.cpp:64`, `:112`; F-ES-24 dispositioned.
- [ ] `02` § The input has one row per write site (the seven of R2 cmd 13) with its mechanism, atomic or not, and what a truncated file reads as; one row per `FileSystem::exists(` of `es_input.cfg`/`es_last_input.cfg` (`InputManager.cpp:893`, `:1187`, `:1250`; `GuiDetectDevice.cpp:127`) with 3.11's answer; the two hotkey names (`:1101-1108`; `GuiInputConfig.cpp:73`, `:270-281`) stated; `doOnFinish`'s `<command>` (`:1272`) with the shipped `es_input.cfg`'s `inputAction` count from G-01; the controllers blob's quoting named for T3's half.
- [ ] `02` § The merge debt is one line naming `cada856d86`, `rocknix/master` (`f6c542872e`), `bccd715707` as its parent and the stale `upstream/master`, the upstream commit count on the 96 of 0 since the base (14 on any path), 96 of 96 blobs identical between the base and master, 83 of 96 between the pin and master, and batocera's twelve commits since `1750dded8c` on nine files (six of them fork-modified: `GunManager.cpp`, `InputManager.cpp`, `Log.cpp`, `Window.cpp`, `Window.h`, `GuiMsgBox.cpp`) as the reconciliation list only; T21's `3ae9610b0` hunk in `es-core/CMakeLists.txt` recorded as the integration's, and T34's ES tip's delta inside the 96 (empty, or named).
- [ ] `02` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason; the menu-map check's line and the checker's `:58`, both `es-untranslated` lines, the catalog lines for this slice's msgids, the C-locale non-ASCII counts (bytes and comment lines) beside `git grep -P`'s, the plain-`g++` first error quoted whole, the stand-in syntax check's rc per file over the 44 with the fakes and the pugixml root (the udev and pulse branches named as not parsed, or faked), and the unit build's `TOTAL: N test cases in B binaries` line with 0 failed are among them; every unit case the lane wrote has its FAIL-then-PASS pair recorded against the unfixed extract first, the seven candidates by name (3.1, 3.4, 3.5, 3.10, 3.11, 3.14, 3.19) and 3.27's script, and a candidate that PASSes at the pin is recorded as such, not as a defect.
- [ ] `02` § The guest cycle records the window the coordinator granted on #682 (the comment's time; the START and RETURN posts with their first-line contract, the timer that stops the guest or the sentence that nothing does, and censuses, and the host file's lines beside them), the image by file name and `BUILD_ID` read from the guest at 640x480, G-01 to G-12 with their frames read back at EN and FR and each frame labelled by side (`image` or `pin-binary`), G-02's two edge reads, G-04's process count across the press, G-05's named dialog or its `CANNOT`, G-06's three keyboard frames with the key gap measured by a reader and the empty row after `s`, G-07's French frames, G-08's hold outcome or its `CANNOT`, G-09's three screensaver frames and the transfer-page frame, G-03 and G-10 as `CANNOT` with the reason, the second boot at 1280x800, the disk retired with path, size and sha, the leftover check (`qemu 0, compilers 0`), and the window closed inside its bound plus grace.
- [ ] `00-running-log.md` shows no image build, no fetch (the council runtime from `npm install --offline`; `rocknix/master`, `batocera/master` and the lanes' ES tips read from the shared refs), no handheld, the owner's accounts never named or used, no hosted account, no M7 root, worktree or prep directory, the guest only inside the granted window, two keyed invokes and every other council call keyless, and nothing written under the ES worktree before stage E (`00`'s own closing census).
- [ ] `04-analysis.md` § Q1 to Q7 are answered at their lines; every `bug` states its trace, its `Already written:` line (argued for the writers -- `es_input.cfg`, `es_last_input.cfg`, the favourites file, the log -- and as *nothing inherited* where the code writes no file) and its VM line in one of the named families and passes `tools/box-check --issue N`; every #585 line owed is written in `02` in the shape the lane writes; every row of § 2's take-up table has a disposition at its lines; the § 1 rulings (a) to (i) each have their `02` row; #1283's and #1305's bodies are read to their last comment before their rows are written.
- [ ] Every proof in `02` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`; every punch item carries `question:`; `02` § What T36 and T37 inherit lists § 5 item 3's eleven items with their lines.
- [ ] The retro exists at `docs/retros/<date>-m6-es-core-window-input.md`, is posted on #682 with its heading's time from `date -u` in the posting command, says what the slice did to the two time-to-play numbers (the card's linger and the g2g dialog's answer measured by `tools/time-to-play`'s cells, the launch path's six directory scans and `WatchersManager::pause` priced from the guest, or `CANNOT` with the harness's reason; cited from `docs/vm-qa-log.md`), and what T36 and T37 inherit.
- [ ] The map: **the rows a stream added, the checker's line quoted, red if it cannot see them** -- this slice's six dialogs are scanned by `tools/es-menu-map-check` (its `SOURCE_DIRS` at `:58`) and contribute the titles its three patterns find (expected 0; the per-file count quoted); if a stage-E stream adds, moves or renames a row on a page it touches, or changes the configure-a-controller flow under CONTROLLER & BLUETOOTH (`docs/es-menu-map.md:134`), `docs/es-menu-map.md` changes in the same commit (D-UI-039) and `tools/es-menu-map-check --es-src <W> --ref <reviewed-at-es>` prints `0 missing` on the branch as handed back, with its full output line quoted in `02` § The structure; a title the checker reads from a member initializer and misses (#951, #965) is named there as unseen, and that is red, not `0 missing`.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the distribution branch and the ES fork's `.githooks/pre-push-test` on the ES branch before the hand-back merge, and again on the coordinator's simulated merge; every fix on the ES branch has, recorded beside its commit, the covering unit case's PASS line (and its earlier FAIL), its French in the same commit where a sentence changed (a CLEAR confirmation or a `GAMEPAD` subtitle included), `tools/es-syntax-check` PASS where a toolchain exists or else the stand-in `g++ -fsyntax-only` rc with the fakes and the pugixml root (or `CANNOT` with the missing header named), and a clean non-ASCII grep over its added lines.
- [ ] The unit build's `TOTAL: N test cases in B binaries` line is quoted in `02` § The runs and in the hand-back from the script's own output, with 0 failed in every binary's summary after the fixes, `window-input-tests` among the binaries, and the seven candidates' earlier FAIL lines (or their PASS-at-pin record) and 3.27's FAIL-at-pin line beside it.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and both
branches pushed (the hand-back); the stage-D pause; an explicit maintainer
pause on #682; a blocker named on #682 (the seat failing its provenance
gate twice, a packet scan hit that is a value, two commands that disagree,
a block whose output differs from § 2's beyond the deltas it records, an
upstream-carried file that is not byte-identical to `rocknix/master`, a
pointer line that names the predecessor slice (§ 10); **not** the host's
missing toolchain, which § 5 names and the `CANNOT` forms absorb, **not**
the udev and pulse branches the host cannot parse (§ 5 names them and the
record says which branch was parsed), **not** a `window-input-tests`
binary that fails to build on the first try (the doubles and the extracts
are the lane's to extend; the first error names the fake), **not** the
guest's lack of a pad (G-10's `CANNOT`) or a monitor that cannot hold a key
(G-08's), which § 5 names as the floor's limit, and **not** T21's hunk in
`es-core/CMakeLists.txt`, which § 1 (h) names as the integration's); an
ES worktree that differs from the pin on any of the 96 files at stage A;
or an execution limit, stated as such with the running log current. A
checkpoint is not a stop. An idle session says it is idle on #682, **and
does not end a turn on a post that asks nothing**: a turn ends on a post or
a commit, never on "next is ..." (the T26 lane sat 28 minutes on exactly
that, friction 2026-10-27 10:48 UTC).

## 9. Ceremonies owed

The ceremonies every lane owes are the rules that load every session --
`learning-capture.md` (the work-log entry per session headed `#682`, its
time from `date -u` in the same command, `tools/work-log-index --write`
after it), `ceremonies.md` (a friction line the moment something slows,
`issue: #682` or the guard; `tools/ceremony-check --gate` before every
push, never `--no-verify`), `decision-register.md` (a row the same
session for any decision), `vm-first.md` (the VM question before any
proof: § 5 answers it), the mini-retro at stage G posted on #682 in
Instruction-Recommendations mode with its *adjustments* as proposals for
the coordinator -- and are not restated here. What is this slice's:

- **Four register rows expected, all put to the coordinator at the pause,
  never decided by the lane** (the ownership ruling of § 1 is the
  coordinator's own row, written at dispatch): whether a toast held behind
  a long upstream card (the hasher's, the installer's) stands under
  D-UI-093 and D-UI-079 together or is a bug with a bound (F-ES-24, item
  14, L-01's queue read with it); whether the toast queue drains in the
  order things happened or newest first, and whether a re-queued toast
  returns whole or for its remainder (L-01, 3.14); whether
  `GuiTextEditPopupKeyboard.cpp:14`'s second `BUTTON_GRID_HORIZ_PADDING` is
  deleted for the house 0.022 or kept under its own name (L-13, T34 L-05);
  and whether `GuiMsgBox`'s back accelerator keeps its fall-through to the
  last button or a dialog without `OK`/`NO` binds back to nothing (L-12,
  T26 L-22). Two more may follow from the proofs and are named as such, not
  counted: the lock's fix shape if T33's named shape does not fit (L-11),
  and CLEAR's confirmation (L-14); the masking mode is #1192's Backlog, the
  coordinator's. The highest IDs are § 3 item 2's (D-CLOUD-191, D-INFRA-031,
  D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-133,
  D-WORKFLOW-213 at `a00b3354d5`; re-read at `COHASH`); `tools/register-check`
  is the proof; D-WORKFLOW-188 is on the P1 branch only and the merge
  unites them; a row this slice forces takes an ID the coordinator assigns
  on #682.
- **The same-commit rules, stated once:** a row added, moved or renamed
  updates `docs/es-menu-map.md` in the same commit and
  `tools/es-menu-map-check` passes before it (D-UI-039; this slice owns
  the dialogs the checker scans and the configure-a-controller flow the
  map names only by its section, so a stream that changes either expects
  one); a sentence added or changed carries its French in the same commit
  (D-UI-051: a CLEAR confirmation, a `GAMEPAD` subtitle, a reworded
  "Approximative device found" line if it is a player's -- it is a log
  line, so no).
- **Every count is a tool's line** (`engineering-practices.md:250`): a
  figure in `02`, a post or the hand-back is the command's own output,
  quoted; a sum, a difference or a rate is computed by the command that
  prints it. **Every grep for `_("` by `-F`**; **no `cut` on an expected
  error line**; **a heading's time from `date -u`, never typed**.
- The ES fork's `.githooks/pre-push-test` after an ES change; a merge with
  conflicts is checked for markers; the ledgers united by whole entries;
  **a commit names its paths**; anything temporary under
  `/workspace/tmp/m6-t35/` after `df -i`, never `/tmp`; the window's record
  kept on the branch, the guest disk retired after it with the retirement
  recorded in `00` (D-INFRA-022); **`rm -rf` only as `"${VAR:?}"/...` or a
  literal path, in its own short command, never inside a `bash -c`
  script**.
- A fixture that rewrites no path, in a bubblewrap sandbox started with
  `--clearenv` (3.5's temp directory of scripts is such a fixture; the
  `ProcessStartInfo` double never runs what it records); the walks' steps
  under the audit folder's `stage-e/walks/`, never under `tools/`; the
  non-ASCII grep over a stream's added lines (`git diff -U0 HEAD --
  <file>`, its `+` lines), an upstream hit recorded and not fixed, a glyph
  in a string literal allowed (`es-code-traps.md:60`); a generator seen to
  exit 1 on a constructed drift before its table is trusted.
- **Every edited file checked for an unfilled placeholder before its
  commit**: `/usr/bin/grep -c -E '__[A-Z]+__|\b(CO|MERGE_|TIP|V2)HASH\b'`
  is 0 on the pointer, the running log and every artifact (the T31
  dispatch entry shipped with its two timestamp and URL placeholders
  unfilled, friction 2026-10-27 12:02 UTC; the pattern is written in
  pieces here so that this line does not count itself, and the four
  names it matches are § 1's).
- Commit messages `docs: ...` on the distribution branch, with `Refs #682`;
  on the ES branch the package's convention, `Refs #682, #<bug>`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#682's checkboxes against their artifacts; the lint's `PASS` line on the
default phase and with `--issue`; `review-plan.json` and the two
provenance files (read directly) and the manifest's scan block; the audit
issue's checkboxes all at an outcome; the coverage table's row count (96),
the generated sections' asserted counts, § The input's seven write rows,
§ The locks' acquisition sites, § The merge debt's one line; every Q bug
with its three lines; **re-running on clones of both branches at their
tips under `/workspace/tmp/m6-coordinator/`: the membership block, every
§ 5 run in full, the stand-in check and the unit build script** (no guest:
the window's record is read, not repeated); `register-check` on a
simulated merge with the coordinator's tip; the retro's answers; the five
checkers' exit codes; the collisions named against the three
`tests/app-unit/fakes/` doubles, against T21's `es-core/CMakeLists.txt`
hunk and against T34's ES tip; **the § 1 rulings' rows in `02`**; #1283's
and #1305's checkboxes against the lane's `stage-e/` record. The lane
posts one hand-back comment naming **both tips** and each artifact by
path, writes `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and
`fixed-at-es:` into #682's body, then says it is idle. After acceptance
the coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the lint against **the audit issue**, merges
the distribution branch in its turn after the M7 candidate with the pin
moved to the ES branch's tip in the same integration commit (the ES
package built before it lands; T21's CMake hunk and this slice's reconciled
there), regenerates the ledgers, posts any #585 lines in the shape the
lane wrote, files any Backlog the hand-back names, and closes #682 when
every row is proven -- which is also when #649, #665, #667, #668, #673,
#678, #679, #680 and #681 close (§ 1); the interface epic #700 closes when
its slices have.

**The pointer the lane checks at stage A, line by line.** The seeded
pointer `.github/sessions/saved-session-state-feature-m6-es-core-window-input-682.md`
is written by the coordinator from T34's, and T34's was seeded from T33's,
which carried a sentence of T26's. So before the first command after `cat`
the lane reads these eleven keys, each against the one value that would be
the seeding error, and reports any that name the predecessor on #682
before going on:

| Key | Must read | The seeding error reads |
| --- | --- | --- |
| `Branch (distribution):` | `feature/m6-es-core-window-input-682` stacked on `feature/m6-p1-survey-641` at the P1 tip the dispatch comment names (`2174265e9c` today) | `...-es-core-components-681` |
| `Worktree (distribution):` | the § 1 path ending `m6-es-core-window-input-682` | `m6-es-core-components-681` |
| `Worktree (EmulationStation):` | `W` of § 1, at the pin `16dbac5211` | T34's `m6-es-core-components-681` checkout, or another lane's |
| `Executor:` | Opus 5.5 at high effort, the T5 session (`m6-t5-build-engine`), free since T33's close-out, as the dispatch comment on #682 names it | T34's session (the T3 session, `m6-t3-emulators`) |
| `Epic:` | #700; T2, T18, T20, T21, T26, T31, T32, T33 accepted and open until the integration merge; T34 in flight or accepted as the comment says; T36, T37 and T44 after | "T34 accepted" before it is, or "T33 in flight" |
| `Depth:` | one seat, GPT-6 Astra at `max`; the 13 fork-added and fork-modified files whole (`LogPolicy.h` and the 12), the 83 upstream-carried by cited ranges; no binary in the 96 | the 21 fork-modified files whole, the 59 upstream-carried by cited ranges |
| `The lens:` | cost against value over 96 paths, `es-core/**` as `rest` -- the window, the input manager and its config, the es-core dialogs, the theme parser, the script runner, the watchers, the log | `es-core/src/components/**`, 80 paths |
| `The rule:` | nothing under the distribution's `packages/`, `projects/` or `tools/`; nothing in the ES worktree at stages A to D; nothing outside the 96 at stage E | "nothing outside the 80" |
| `The host:` | the shared log and one guest window of 30 + 5 minutes with two boots, the START post naming the timer that stops the guest at bound plus grace or saying nothing does | a 30 + 5 window whose plan is the components' (the strip, the grid, the slider) |
| `Register:` | the highest decided row per area read from the table at `COHASH` (at `a00b3354d5`: D-CLOUD-191, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-133, D-WORKFLOW-213), plus **this slice's ownership row, which the coordinator writes at dispatch and whose ID is assigned then** | T34's triple (D-CLOUD-186, D-UI-128, D-UI-129), or D-WORKFLOW-213 named as this slice's own row |
| `The brief:` | `docs/reviews/briefs/es-core-window-input.md` at `V2HASH` (§ 1: filled by the dispatch comment; version 1 has no dispatch hash) | `es-core-components.md`, or the literal word `V2HASH` |

**The readings before dispatch** (plan § 3, principle 3): the interface
epic's futro (`docs/futros/2026-10-23-m6-interface.md`, 978 lines at
`a00b3354d5` by `/usr/bin/grep -c ''`; its last heading `:976` Errata from
T33's acceptance) takes a T35 kickoff addendum written by the coordinator
with this version; the stranger's proof of version 1 ran on 2026-10-31
(`/workspace/tmp/m6-coordinator/kit/t35-proof.md`) and `## Corrections in
version 2` records what it found. This brief's hash at dispatch is
`V2HASH`.

**What never runs in this slice:** an image build, a compiler beyond the
host's `g++ -fsyntax-only` (plain or with the fakes and the pugixml root)
and the generated test build, a fetch (the council runtime from `npm
install --offline`; `rocknix/master`, `batocera/master` and the lanes' ES
tips from the shared refs), a handheld, the owner's accounts or any hosted
account, a host listener on a privileged port, a guest before a grant on
#682, M7's roots, worktrees or prep directories, a change outside the 96
files, a change to `docs/es-menu-map.md`, the French catalog or the audit
folder except under a stream brief, a move of the pin, a line in
`es-core/src/components/`, `resources/`, `utils/`, `HttpReq.*`,
`Settings.*`, `SystemConf.*`, `CloudText.*`, `es-app/src/` (the
screensaver, `NetworkThread.cpp`, `main.cpp`, `SystemData.cpp`,
`ApiSystem.*`) or `tests/app-unit/fakes/` without the pause's ruling on
its owner, a deletion of `GuiTextEditPopupKeyboard.cpp:14`'s second
constant before the pause rules, a reorder of `processNotificationMessages`'s
queue before `c1c0d6ddc`'s `git log -S` is read, a `scripts/<event>/`
hook written on the guest outside 3.5's sandbox, an edit to
`es-core/CMakeLists.txt`'s lines T21's `3ae9610b0` touches, and an
`es_input.cfg` written on the guest by hand.

## Corrections in version 2

The stranger's proof of version 1 (2026-10-31, `/workspace/tmp/m6-coordinator/kit/t35-proof.md`: 12 commands, 904 batch checks over `git show` output, the membership block re-run, the § 5 runs block re-run through `git -C` against the pin, the French catalog parsed, a `git archive` of the pin compiled plain, two `gh` reads) found every correction below; each names the section it changed. The rule, register, map, blindspot, futro and tool lines are read at the coordinator worktree's `a00b3354d5` (2026-10-31T01:03:54Z); the branch moved from `4e754f89c7` to `a00b3354d5` during the proof, so the lane re-reads them at `COHASH` and records a line that moved beside the one cited here.

1. Header, § 3 items 1 to 4, § 9, § 10 -- the lines were fixed at `7a32dff771`; they are now `a00b3354d5`'s: `es-player-text.md` +4 from `:273` (`:326` -> `:330`; the toast sentence is `:135`, the `_( )` bullet `:31`, `## Conventions` `:29`), the register's `## Open decisions` at `:769` (not `:762`/`:764`), D-SYS-014 at `:775`, and the highest decided rows D-CLOUD-191, D-UI-133 (D-CLOUD-190 `:762`, D-UI-130 to D-UI-133 `:763-766`, D-CLOUD-191 `:767` landed after version 1); the map, the blindspots and every other cited line unchanged.
2. § 1, § 10 -- the futro is 978 lines (§ 1 said 974); T34's errata ownership line is `:1744` (not `:1743`); T34's brief's version 2 is 1,740 lines at `a6e14fed86` and 1,745 at HEAD.
3. § 1 -- T33 is accepted (`17f2bcea8d`, #1270 CLOSED); T34's punch list #1307 (43 findings, 0 critical, 1 high) is filed and its stage D ruled (D-UI-130 to D-UI-133); #1307's PL-04 and PL-05 are carried here as L-28 and L-29 (§ 2's lead and take-up tables, § 4 Q6).
4. § 1 -- the `order.md` § T35 range is `:633-641` and the closing evidence is its `:641` (*audit folder, lint PASS, punch list through Phase 7*); the per-lane ES deltas re-read: only T21's `es-core/CMakeLists.txt` differs (`1 file changed, 5 insertions(+)`), T34's local branch is the pin.
5. § 2, § 3 item 7, § 5, § 7 -- `_("` is 86 lines in **10** files (not 13: `GunManager.cpp` 6, `BindingManager.cpp` 2, `TextToSpeech.cpp` 1 join the seven), 97 occurrences, 61 distinct msgids, every one with a non-empty French `msgstr` at the pin (25 `pgettext` pairs and 2 `ngettext` pairs too); the fork's own added msgid is one, `CLEAR` (`Window.cpp`'s fork hunks add no literal); the detect sentence is `HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT.` with a period and `HOTKEY ENABLE` is no msgid (the § 5 grep's regex corrected to six lines); `tools/es-untranslated`'s two lines printed (`706 ... 0 without`, `703 ... 0 without`, rc 0 each).
6. § 2 table, § 5, § 7 -- the named-once loop prints 9, not 0: seven `# batocera` trailing comments and two headers registered nowhere (`HelpPrompt.h`, `Scripting.h`); every `.cpp` is named once; the top-level sources are `:147-172`, `CORE_SOURCES` `:146-276`; the writes grep prints 9 lines (7 write sites, 2 `AtomicFileUtil` registrations at `:122`, `:257`); the upstream commit count on the 96 since the base is 0 (14 on any path), § 6 and § 7 said 14.
7. § 2 table, L-07, L-09, L-16, 3.20, § 4 -- `Window.h:101` for `hasAsyncNotifications` (not `:97-98`); `InputManager.cpp`'s `exists` lines are `:420`, `:893`, `:1187`, `:1250` (not `:1225`, `:1239`); the page maps `HotKeyEnable` (`GuiInputConfig.cpp:273`, `:279`), lower-cased by `mapInput` (`InputConfig.cpp:188`); `say(` three times in `GuiMsgBox`'s constructor (`:44`, `:234`, `:240`), `delete this` `:289` (not `:290`), `isSmallScreen` `:92` (not `:93`); `ThemeData.cpp:267` is the parser's `{ "multiLine", STRING }` entry, not a `GridTextProperties` declaration (that is T34's `GridTileComponent.h`); `HelpStyle.cpp:3` (not the `.h`) includes `resources/Font.h`; the 17 `delete this` lines listed.
8. § 2 neighbours, take-up table, § 4 Q4 item 30 -- `HttpServerThread.cpp` is `es-app/src/services/HttpServerThread.cpp`, and both routes post their `GuiMsgBox` through `mWindow->postToUiThread` (`:229`, `:559`): the box is built on the interface thread, no line for T32.
9. § 4 Q6, § 5 -- the non-ASCII lines: 28 in four files, 22 of them the keyboard's glyph literals; six upstream **comment** lines in `AudioManager.cpp`, `GunManager.cpp:145`, `InputManager.cpp:393`, `:1437` (two fork-modified files, 0 fork-added lines); `InputManager.cpp:856`, `:869` are ASCII; the in-source gate lines are `VolumeControl.cpp:11`, `CECInput.h:7`, `TextToSpeech.cpp:53` (the includes one line below); the `ROCKNIX` lines are three, `Paths.cpp:76` the third.
10. § 3 items 5, 9, 10, § 5 item 1 -- `es-file-tests-win32` is `:142-158` (executable `:146`); `es-app/tests/unit/fakes/` holds `SDL_timer.h` alone; `docs/vm-qa-log.md:107` alone carries the help-bar figures; `Scripting.cpp:68` is a `new std::thread`, not a fifth `.detach(`; the plain-`g++` first error printed for `GuiMsgBox.cpp` (and `Window.cpp`; `InputManager.cpp` one header earlier; three files parse plain, rc 0).
11. § 2 (the 19 commits), § 2 table -- authors `Max Engel` 14, `blitterbot` 5 (three addresses by `%ae`); the issue numbers by occurrence stated with their rule; the per-file commit lists completed (`Splash.h` + `975235429`; `GuiMsgBox.cpp` + `62e45ea6f`; the keyboard + `1593c299f`, `6d8764ec6`; `CMakeLists.txt` + `469441d4d`, `2dae87308`; `InputManager.cpp` + `370ebe416`).
12. § 5 item 2 -- G-01 adds `ldd /usr/bin/emulationstation | grep -c udev`, the read that settles `UDEV_FOUND` (no `CMakeCache.txt` of an EmulationStation build is reachable on this host; M7's roots are never read).

**The `[unverified]` marks.** Version 1 carried 22; one question remains, `UDEV_FOUND` in the image build (§ 4 Q7 and § 5 item 1, `CANNOT` on this host, G-01's read named); every other mark is settled by a printed line cited where it stood.

**The cuts** (version 1 was 2,086 lines; version 2's count is the kit's `grep -c ''` line): § 2's `CLAIMS` paragraph (the 30 claimant rows named without their per-file lines, which the table and the block's own output carry); § 2's thirteen stat rows (the table's *Fork stat* column; the `--numstat` split kept); § 5 item 1's harness paragraph (the eight targets are § 3 item 5's; the `0 of 44` and the three doubles kept); § 2's list of the 19 fork commits by subject (the count, the two merges, the newest and oldest, the authors and the issue-number rule remain; the table's column carries the per-file subjects); § 1's per-lane ES-delta listing (now one sentence, T21's line kept); § 2's duplicated include-reach paragraph in the neighbours (now a pointer at § 5 item 1, where the figures live); § 2's French sentence under *What the research checked* (now the parser's result); § 5's closing paragraph on the unsettled expectations (now the proof's list). Every edited file:line, every criterion, the four tables (the files, the leads, the take-up, the floor) and the runs block stay whole.
