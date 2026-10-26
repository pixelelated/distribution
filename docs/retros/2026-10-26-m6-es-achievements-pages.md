# Mini Retro: T20, EmulationStation's RetroAchievements and offline pages (#667)

**Completed:** 2026-10-26.

**Scope:** the 25 paths at the ES pin `16dbac5211`, the audit `docs/audits/2026_10_26-epic-m6-es-achievements-pages/`, the audit issue #1167, and the eleven bugs #1170 to #1180.

**Branches:**
- the ES branch `feature/m6-es-achievements-pages-667`, eleven stream commits (`698040b5c` to `5c0ddaaee`);
- the distribution branch `feature/m6-es-achievements-pages-667`, the record and S12 (`087bafdb98`).

**Delta:**
- `es-unit-tests` 185 → 209 cases, `es-file-tests` 24 → 27, `jobs-tests` 6 → 10, `proxycards-tests` 11 → 14, and the new `hasher-tests` with 6.
- Fork strings with French: 706 → 711, 0 without.

## What worked well

- **Lifting the pin's logic verbatim into pure code** before fixing it gave every stream an honest "before" without a toolchain:
  - the sign-in request (S2), the toggle's decision (S4), the readers (S5), the account comparison (S6), the dialog texts (S9) and the JSON parses (S11);
  - each case failed against the lift, then passed after the fix;
  - where the shipped source could be compiled against doubles (`hasher-tests`, `es-file-tests`, `jobs-tests`, `proxycards-tests`), the "before" ran the real file instead.
- **`hasher-tests` under ASan turned L-21, read at stage B, into a sanitizer report** (heap-use-after-free at `start()`), plus 36 leaked threads, from the pin's own `ThreadedHasher.cpp`. A defect only a sanitizer could show became a standing case.
- **The guest window was spent on the shared code paths:** the startup hasher's log, the ready file under the row, and the sign-in's `HttpReq` against a self-signed listener. That held up even though the image's pages turned out to be M7's.
- **The scripts:**
  - `tools/t20-stream-checks.sh` made eleven pre-commit check runs identical;
  - `close-bug.py` and `record-stream.py` kept the bugs, `02` and `05` consistent;
  - every stream's bookkeeping took one command.

## What was harder than expected

- **The image's EmulationStation was M7's composition over the pin.** One identity literal proved "contains the pin", not "is the pin". The difference surfaced at the first page frame, not at step 1 (the friction log, 17:45 UTC; Backlog #1169 carries the two-literal check).
- **Two errors of mine on the guest:**
  - a kill by pattern (`pgrep … | head`) hit a `sleep` that was not the test's;
  - an `openssl req` under `set -e`, with its output silenced, stopped without a word.

  Both are in `00`. The first is in the friction log.
- **`tools/ra-ui-test` was CANNOT in the window.** It rightly refuses a guest a lane has left state on; two of its three refusals were states I had made in earlier steps. Running it first, on the clean guest, would have avoided that.
- **The checks script's non-ASCII step was wrong at first use.** It judged a changed file's upstream lines (three em dashes in `FileSystemUtil.cpp`, at the pin too) instead of the stream's own. It was corrected and given a control (`stage-e/s8-checks-first-run.txt`).
- **Two hazards had to be designed out of the cases.**
  - **S3's:** a `>>> pid 1` case at the pin, cancelled, would really `kill(-1)` this user's processes. The cases plant a group the test owns, and never cancel the pid-1 case.
  - **S10's:** a naive HARDCORE MODE lock would undo the ctl's restore through the child page. The child now writes `SystemConf` before the row.

## What did we discover

- **The RVZ padding shift of 18 is Dolphin's specification, not a slip.** It was withdrawn before it was written, and the fixture against Dolphin's generator is the proof (`stage-b/positives/lfg.out`).
- **Bash forks for a redirected command,** so on the image L-06 needs the wrapping shell itself to die by a signal (`guest-cycle/g02`). The reader's contract defect stays with T21 (#668).
- **A pin-era path of L-09:** `disable` writes the toggle off before it can fail (A-8, R-8), not only after T19's S5.
- **L-10 is reachable at the pin** through an unreplaced ROM name with a carriage return (A-11, R-5), which raised it to Medium.
- **#1154's unfixed half is proved on the guest:** the sign-in reached a self-signed listener that `curl` refused (`guest-cycle/g07`).
- **The vendored rcheevos client logs in by POST** (`rc_api_user.c:27-39`), which settled S2's design from the tree, not the network.

## What adjustments are needed

- **For the integration build's window:** eight walks under `stage-e/walks/` (S1, S2, S3, S4, S6, S8, S9, S10), all `fix-walk-pending-image`. The S2 walk needs the probe given a `do_POST` that logs key names only.
- **For T21 (#668):** the shared process reader (PL-08) with its fixture `stage-b/positives/reader.cpp`, and S2's one `HttpReqOptions` field, `httpsRedirectsOnly`.
- **For T26 (#673):** the gates (`GuiMenu.cpp:188-191`) and the title's source.
- **For the coordinator:** the five #585 lines in `02` § The #585 lines; Backlogs #1168 and #1169 as filed.
- **No change to the remaining plan otherwise.**

## Instruction recommendations

Proposals for the coordinator (§ 9: Instruction-Recommendations mode). No rule file was edited by this lane.

1. **`es-code-traps.md` § Comments near a translatable string:** its grep runs over whole touched files, so it flags upstream's existing non-ASCII comments. Three em dashes in `FileSystemUtil.cpp` at the pin did that here.
   - Recommend judging the added lines: `git diff -U0 HEAD -- <file>`, its `+` lines, then the same pattern.
   - xgettext still reads the whole file, so the whole-file grep stays the image build's question.
   - The control is in `stage-e/s8-checks-first-run.txt`.
2. **`generic-x64-vm-testing.md`, for a lane's guest window:**
   - run `tools/ra-ui-test` first, on the clean guest, before any step leaves state it refuses;
   - read the image's ES identity by two literals, the pin's and the composition's (Backlog #1169).
3. **A stream-checks runner for EmulationStation lanes.** `tools/t20-stream-checks.sh` is this lane's own copy of the generated build and checks, kept in the audit folder. It is a candidate for one fork tool, with `es-syntax-check`'s `CANNOT` form. That would be `learning-capture.md` § 3's procedure-to-tool step, owed to whichever issue the coordinator names.

## Time to play

**The measurement:** T18's window measured the pin (`tools/time-to-play --vm --only launch,exit,g2g --repeat 3 --backend webdav`; T18's retro and `docs/vm-qa-log.md`'s table):
- interface to a game's first frame: **0.56 s**;
- the exit sync's stamp: **1.58 s**, inside D-CLOUD-119's 3 s;
- game to game: **1.01 s**.

**Where this slice's files sit on a launch (checked by reading `FileData::launchGame`):**
- **One place, the top-up gate** (`FileData.cpp:1045-1057`): a launch while a top-up runs asks STOP IT AND PLAY / KEEP WAITING, and `launchWhenGone` waits on `ProxyCards::topUpRunning()`.
  - S7 changed what that reads: a flag held exactly while this process's ctl runs, where it read the progress file.
  - So a scan's file, or a dead run's, no longer makes a launch ask.
  - The wait ends when the ctl process ends, not when its file is removed.
  - That can only remove a question and shorten a wait. It adds none.
- **Off the launch path:**
  - the hasher runs at the game list update and at startup (S1, S9, S11);
  - the sign-in runs at the settings page's close, and is now off the interface thread (S6);
  - the scan is its own page (S3, S5);
  - nothing here runs between the press and the first frame.
- **Nothing was measured after the fixes.** The integration build's `time-to-play` is the measurement.

## Scoped audit findings (Step 2.5)

- **AC conformance:** PASS. #667's checkboxes are the hand-back's to tick from the artifacts. #1167 is at Phase 7, with the full lint `PASS` and `box-check` 0 fail. The eleven bugs are ticked from `stage-e/` and stay open until the pin moves.
- **Cornerstone spot-check:** PASS.
  - Every new player string has French (`es-untranslated` 711 of 711).
  - No stream added a non-ASCII comment (each `stage-e/sN-checks.txt`).
  - `es-player-text.md`'s register holds: everyday words, no tool's words, and the verbs.
- **Interaction-defect scan:** PASS with two notes.
  - S7's `topUpRunning()` meets the launch gate (above).
  - S10's lock meets the child page's mirror; the order was made explicit, `SystemConf` before the row.
- **Futro prediction verification:** n/a (no futro for this slice).
- **Housekeeping (full-suite scan):** PASS. Every unit binary and app target passes at the ES tip under the generated build (`stage-e/s11-checks.txt`).
- **Harness self-coverage:** PARTIAL. The checks script's non-ASCII step needed a control after its first use (above). The page sources stay `CANNOT` for the host's syntax check, so their changes are verified by reading and by the image build.

## Code-verifiable state

| Stream | Bug | ES commit | Tests |
| --- | --- | --- | --- |
| S1 | #1170 | `698040b5c` | `hasher-tests` 3 (ASan) |
| S2 | #1171 | `d3137f992` | `es-unit-tests` +2 |
| S3 | #1172 | `ad2989aa5` | `jobs-tests` +3 |
| S4 | #1173 | `f85061f14` | `es-unit-tests` +4 |
| S5 | #1174 | `274a71add` | `es-unit-tests` +4, `jobs-tests` +1, `proxycards-tests` +1 |
| S6 | #1175 | `2d8a0a135` | `es-unit-tests` +3 |
| S7 | #1176 | `d7a30f0c6` | `es-unit-tests` +1, `proxycards-tests` +2 |
| S8 | #1177 | `d9afa5c7c` | `es-file-tests` +3 |
| S9 | #1178 | `61d7152b0` | `es-unit-tests` +3, `hasher-tests` +3 |
| S10 | #1179 | `2b521c34b` | `es-unit-tests` +1 |
| S11 | #1180 | `5c0ddaaee` | `es-unit-tests` +6 |
| S12 | — | `087bafdb98` (distribution) | `es-menu-map-check` 0 missing |
