# Mini Retro: M6.P2 T2, EmulationStation's launch path (#649)

**Completed:** 2026-10-23
**Scope of this retro:** the T2 lane from stage A (the ES worktree at the pin
`16dbac5211`) through the audit (stages A-D, #790's 36 items) and the five
fix streams S1-S5 to stage F, under the briefs `docs/reviews/briefs/es-launch-path.md`
v2 and `docs/reviews/briefs/t2-streams.md`. The coordinator's acceptance,
the merge into `test/qa-integration`, the pin bump and the walks on the
first image (stage H) are not this lane's and are not retro'd here.

**Branches:** ES `feature/m6-es-launch-path-649`, 35 commits on the pin,
tip `55158d2a6` (70 files, +2,718 / -469); distribution
`feature/m6-es-launch-path-649`, 54 commits citing #649.
**Delta:** `es-unit-tests` grew from 185 cases (4,795 assertions) at the pin
to 220 cases (4,917). `proxycards-tests` grew from 11 to 12 cases and
`bookkeeper-tests` from 5 to 6. There are three new python harnesses
(`launch-play-through`, `system-scan-assets`, `main-parse-args`) and seven
new pure headers with unit cases (`LaunchTemplate.h`, `LaunchCommand.h`'s
additions, `GameFiles.h`, `SaveStateFiles.h`, `SystemFolders.h`,
`SystemOverlays.h`, `SortId.h`). Of the 36 punch items, 32 are resolved,
3 deferred (#678, #684, #791) and 1 open (PL-032, waiting for the Backlog
issue at acceptance). 24 bug issues were filed (#767-#789, #792) and stay
open for their walks; 21 fix walks are listed in 02.

## What the slice did to the two time-to-play numbers

**Nothing measured yet, and nothing expected to be visible.** On the
lane's guest at the pin (`04-analysis.md` § Q5, n=3), interface to a
game's first frame was **0.65 s** median, and a game's exit to the next
game's first frame was **1.01 s** median. #336's baseline was 1.05 s and
2.03 s, but that improvement predates this slice. The fixes are not on an
image yet, so the after numbers come with the first image carrying the new
pin, in the coordinator's stage H. PL-007/034's acceptance is that G-1's
launch cell is no slower (W-3).

Read from the code, the effects on the two paths are:

- **Press to first frame: no work added on the common path.**
  - PL-007/034 runs `configureEmulators` only when the template names
    `%CONTROLLERSCONFIG%`. The shipped template does, so the launch keeps
    that cost; the boot-game store drops it.
  - PL-014 asks the gates once instead of twice.
  - PL-008 adds a lookup by path, only on a deferred launch (one that
    waited at a gate or behind the capture).
- **Exit to the next first frame: one change adds work, and it is
  unmeasured.**
  - PL-015's rescan check stats every scanned folder of a system with no
    game list, instead of its root alone. That is one stat per sub-folder,
    per such system, on the frame after each exit.
  - PL-019 moves `tend` to `process.run()`'s return. That makes the
    recorded play time correct but does not change the wait.
  - PL-012 bounds the save-state deletion's lock retries, which can only
    shorten a wait.

  The stat cost needs a system with many sub-folders and no game list to
  show at all. It should be read off the exit cell at stage H against
  1.01 s, not assumed.

## What worked well

- **Harnesses that extract the shipped function by signature and adapt to
  its shape.** Each of the six python harnesses compiles the real code with
  doubles around it and branches on the source's shape (pin or fix), so one
  file fails on `pin-src/` and passes on the tree. Every fix commit after
  #779 names both runs. This put PL-008, PL-009, PL-011, PL-018 and PL-036
  under a test without a guest.
- **Pure headers for the rules.** `LaunchTemplate.h`, `GameFiles.h`,
  `SaveStateFiles.h`, `SystemFolders.h`, `SystemOverlays.h` and `SortId.h`
  each took the rule out of a `.cpp` that needs the window, so the rule got
  doctest cases (`es-code-traps.md` § Pure text has a home). The shell
  around each stayed where it was.
- **The syntax recipe before every `.cpp` commit caught two real errors**
  before they cost a build: `SaveState.cpp` was missing `Log.h`, and
  `SystemData.cpp` had a `?:` mixing a list and a vector.
- **Reading the fix's blast radius stopped two wrong fixes.**
  - PL-020 as written (free the duplicate folder) would have left freed
    pointers in the scan's map; checking the key first avoids that.
  - The obvious delete of an arcade asset's `FileData` would have removed
    live index entries on the rescan path. Asking the test before
    allocation (PL-036) does not.
- **Brief rules 1-4 settled scope without a round.** A removal upstream
  still carries became a row (PL-027, PL-028); an upstream pick that
  conflicts with fork-own lines was deferred to #791.

## What was harder than expected

- **Four host holds** (the M7 lane's windows). The work went on with the
  reading and the host checks, but each hold split a stream from its
  compile. The 21:49 instruction asked for a one-line rename commit while
  compiling was forbidden, so `a1cbc0ccd`'s compile and unit-test lines
  come after it. That breaks #649's thirteenth item for that one commit,
  and the running log says so.
- **The safety classifier stopped the punch-list drafts three times**
  (friction 2026-10-23 20:20). The coordinator's direction (c), a
  defensive register with no example strings, unblocked it. The bug bodies
  went in by reference to 05 instead of restating it.
- **Claims about my own artifacts were wrong four times, each before I had
  read the artifact:**
  - the `Already written:` lines of PL-016 and PL-017 (amended before the
    push);
  - PL-027 ticked on #790 before its commit (unticked);
  - "this commit names both runs" on #779 (corrected, and criterion 2
    unticked);
  - "36 catalogues" (it is 35; the 36 counted `en_GB`'s msgstr line).

  Each was corrected where it landed, the same session.
- **`es-syntax-check` read a relative path against the wrong directory** and
  printed MISSING from the distribution's cwd. It was fixed under #699 (with
  `--tree`, a relative path resolves against the tree).
- **The brief's lists drifted from the tree.** It says "`tests/app-unit`'s
  three targets", and there are four (`app-unit-tests` too); all four were
  run. The coordinator's return note said "three python harnesses", and
  the brief names three that exist, so that one held.

## Discoveries that affect future work

- **PL-036, found while doing PL-020:** the folder scan leaked a `FileData`
  per arcade asset per scan, at every start and every game-list reload.
  Filed (#792) and fixed as S3's tail.
- **The seam with T1 is a contract, not a fix:** the spectator and relay
  session arguments (D-WORKFLOW-192) are emitted by ES (PL-010). They do
  nothing until `runemu.sh` reads them (#648).
- **Leads for other slices**, posted on #649 and listed in 05 § Leads:
  - `Scripting`'s quoting (T33/T21);
  - the controllers blob inside double quotes (T36);
  - detached card workers after `window.deinit` (T35/T18);
  - `cloud_capture --retire` unbounded (T16);
  - `GuiNetPlay`'s relay and spectator (T31);
  - `time-to-play.md` describing D-CLOUD-076/109 as what ships, where the
    code ships D-CLOUD-130.
- **Doctrine drift, not this lane's to fix:** the rule file `time-to-play.md`
  is stale against the code (above). Under D-WORKFLOW-189 the lane files
  only its own punch-list and bug issues, so it is handed to the
  coordinator to file.

## Adjustments to remaining work

- **Stage H (the coordinator's):** read the exit cell on the first image
  against 1.01 s with PL-015's stat in mind. Read the launch cell for W-3's
  "no slower".
- **The brief template (plan § 7):**
  - The app-unit target list should name four targets, or say "every target
    in `tests/app-unit/CMakeLists.txt`".
  - A no-compile window should say whether a commit touching a `.cpp` waits
    for its compile (the order § 7's thirteenth item assumes) or may land
    with the compile queued. Either is workable; the brief should pick one.
- No change to the order of slices.

## Scoped audit findings (Step 2.5)

- **AC conformance: PARTIAL ⚠.**
  - #649's checklist is satisfied by artifacts except three items:
    - the walks, owed at the image, which keep the bug issues open;
    - PL-032, which keeps the lint at one failure until the Backlog issue
      exists;
    - `a1cbc0ccd`'s compile line, which came after its commit (running log,
      stage F).
  - #790: 26 open checkboxes, `box-check` 0 fail.
- **Cornerstone spot-check: PASS ✓.**
  - Every new player string has its French (`es-untranslated` 706, 0
    without).
  - No non-ASCII byte in a comment of a touched file.
  - A file another process writes is read uncached (`exists(path, false)`,
    PL-024).
  - Credential call sites all quoted (`credential-quoting` 9/9).
  - Commits cite `Refs`, never a closing keyword.
- **Interaction-defect scan: PARTIAL ⚠.**
  - Proven together: PL-009 (the exit-sync claim) with the capture gate
    and a refused relaunch, in one harness (`launch-capture-gate`, 17
    checks); PL-018 (play-through) with PL-014 (gates once) in
    `launch-play-through`.
  - Untestable until T1 lands: PL-010's arguments with `runemu.sh`.
- **Futro prediction verification: SKIP ○.** No futro was written for T2.
  `docs/futros/2026-10-23-m6-os-scripts-and-launch.md` covers T1 and says
  the lanes after it get a kickoff note at dispatch. None for T2 is in
  `docs/futros/`.
- **Housekeeping (full-suite scan): PASS ✓.** At the ES tip:
  - `es-unit-tests` 220/0;
  - the four app-unit targets green under ASan+UBSan;
  - the six harnesses PASS;
  - the nine product `.cpp` files syntax-PASS;
  - the four host checks green.
- **UI review: PARTIAL ⚠.**
  - PL-024, PL-025 and PL-026 changed words a player reads; the menu map
    has their section ("Boot dialogs and the launch error box").
  - Their frames are walks W-x at the image (`fix-walk-pending-image`), so
    the evidence `es-ui-style-guide.md` § Keep the flow and its visual
    evidence together asks for lands at stage H, not before the pin bump.
- **Harness self-coverage: PASS ✓.** Each new harness was seen to fail on
  the pin's source before it passed. `es-syntax-check`'s relative-path gap
  was found landing the stream and fixed (#699).
- **Documentation freshness: PARTIAL ⚠.** The menu map was updated in the
  same change; `time-to-play.md`'s drift is handed to the coordinator
  (above).
- **Build-vs-adopt: SKIP ○.** Fixes inside existing code; no
  build-or-adopt answer was recorded for the slice.

## Practice adjustments (Instruction-Recommendations mode)

- **A claim about one's own commit, comment or count is read off the
  artifact first.** This lane broke that four times (above), and the rule
  already exists (`engineering-practices.md` § Verify the artifact, not the
  report). Moving it up a stage (`working-principles.md`) means a check: a
  `commit-msg` hook in the ES repository could refuse a `.cpp` commit whose
  body lacks a `Tests:` line naming two runs. That would have caught #779.
  This is put to the coordinator, not done here: hooks are outside this
  lane.
- **A window that forbids compiling should be paired with what happens to a
  commit** (the adjustment above). Otherwise the lane must choose between
  the instruction and the brief.

## Code-verifiable state

| Stream | Items | ES commits | Tests |
| --- | --- | --- | --- |
| S1 the command and the state file | PL-001, 007, 021, 034 | `07bed26bf`, `2f26f410f`, `3872afe5a` | `LaunchTemplateTests`, `LaunchCommandTests` |
| S2 DELETE GAME and the save-state files | PL-002, 012, 016, 017, 023, 027, 035 (half) | `65a4a4f63` ... `e88ce097d` | `GameFilesTests`, `SaveStateFilesTests`, `bookkeeper-tests` |
| S3 the systems table | PL-003, 004, 005, 015, 020, 033 (pick), 036 | `2e4877066` ... `c2e75868a` | `SystemFoldersTests`, `SystemOverlaysTests`, `SortIdTests`, `system-scan-assets.py` |
| S4 the launch chain | PL-008, 009, 013, 014, 018, 019, 022, 035 (half) | `d7c27172f` ... `2f881879c` | `launch-capture-gate.py`, `launch-deferred-state.py`, `launch-play-through.py`, `proxycards-tests` |
| S5 the process and the words | PL-006, 010, 011, 024, 025, 026, 030 | `e14ba66b2` ... `ede4ae1d6` | `main-parse-args.py`, `LaunchTemplateTests`, `LaunchCommandTests`, `es-untranslated` |
| Stage F | PL-024 (spelling), PL-035 (`ProxyCards`) | `a1cbc0ccd`, `55158d2a6` | syntax recipe, `es-unit-tests`, app-unit |

---

**Code-complete for the lane. Next: the hand-back (brief § 10), then the
coordinator's acceptance and stage H.**
