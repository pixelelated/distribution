# Mini Retro: T18, EmulationStation's cloud pages, cards and text (#665)

**Completed:** 2026-10-26.
**Scope:** the T18 slice audit, stages A to F, `docs/audits/2026_10_26-epic-m6-es-cloud-pages/` (#1153), and its six fix streams on the ES branch `feature/m6-es-cloud-pages-665` (`16dbac5211..d55235d4b`).
**Delta:**
- 23 punch items: 9 Resolved, 10 Deferred, 4 Withdrawn.
- 8 Low bugs (#1145 to #1152), 4 with every criterion ticked.
- `es-unit-tests` 187 → 189 cases; `es-file-tests` 24 → 27; `jobs-tests` 6 → 10.
- Three host fixtures under the audit's `tools/`.

## What worked well

- **Test first, with the control kept.** Every stream's FAIL is recorded before its fix (`stage-e/s<N>-before.txt`). Where a case could only fail by not building, a control was run:
  - S5 put the job's old condition back and watched the new `jobs-tests` case fail;
  - S6's composed-run case was written against the untiered fix and failed there.
- **Fixtures that read the shipped code out of its source.** `t18-stamp-fixture.py` and `t18-wrapper-fixture.py` exercise the exact writer and wrapper at any revision. The before/after pair is one command with a different rev, and nothing is re-typed.
- **The seats' grades fed the streams directly.** Six of the eight bugs (#1146 to #1148, #1150 to #1152) carry the seats' own item IDs, so each fix states which claim it answers.

## What was harder than expected

- **The card does not build on the host** (`SDL_joystick.h`). Three of S5's four cases are proven only at the decision function and by source guard. The criterion stays open, and the question is put on #1150.
- **The criteria named the means, not only the outcome.** #1145 said "the directory made unwritable", and S2's fixture had used a full disk. The case was added at stage F rather than ticking a criterion the fixture had not run.
- **S6's first fix was right for the bug's test and wrong for the page.** The page's run is composed with tier lines (`GuiMenu.cpp:5006`), which the bug's criterion did not name. A grep for the tier composer caught it before the commit.

## What did we discover

- **The SIGPIPE trap came after the pid echo in the job's wrapper too** (the seats' A-3), not only absent from the card's. The fixture's "at once" case is what showed it.
- **A completed run could read STOPPED,** and a failed one SKIPPED - YOU CANCELLED IT, depending on when a stop landed (A-33, R-11). The one decision now lives in `CloudText::stopEndedRun` for both surfaces.
- **PL-19's glued line does not happen with rclone 1.75.2:** its final block ends in a newline.

## What adjustments are needed

- **#1143 inherits:** PL-14's untested traps (listed there), PL-11, PL-12, PL-13's seam, PL-16's refactor and PL-23. Its one reader per part also covers S6's named gap: two composed parts that end 69 without a word.
- **The integration build owes:**
  - `strings` for the S1 and S3 words with their French;
  - the frames from `stage-e/walks/` (the match's CANCEL dialog and the nothing-new done page), which need a match slow enough to press back during (#1141);
  - the card's restart proof (#1148);
  - the compile of `ThreadedCloudSync.cpp`, `CloudTransferJob.cpp` and `GuiCloudTransfer.cpp`.
- **T26 (#673)** inherits PL-17's notes and PL-21's composers' half.
- **T20** inherits:
  - `CloudText::stopEndedRun` and `followUpsAllowed` as the shared decisions;
  - the wrappers' `{ trap '' PIPE; echo ">>> pid $$"; CMD ; }` shape;
  - `CloudTransferJob::failedItems()` for its own cases.

## Time to play

The window measured the pin (`02` § The runs; `tools/time-to-play --vm --only launch,exit,g2g --repeat 3 --backend webdav`):
- interface to a game's first frame: **0.56 s**;
- the exit sync's stamp: **1.58 s**, completed 3 of 3, inside D-CLOUD-119's 3 s;
- game to game with the exit sync in flight: **1.01 s**.

What the fixes do to those numbers:
- **S5 adds no wait to the launch path.** The late pid's kill runs on the card's reader thread. The linger gate reads two counters after a linger the card already had.
- **S2's atomic write** is one rename per stamp, on the card's thread.
- Nothing was measured after the fixes. The integration build's `time-to-play` is the measurement.

## Scoped audit findings (Step 2.5)

- **AC conformance:** PARTIAL. The host criteria are ticked with their artifacts. The image's `strings`, the frames, and #1150's card cases are open and named.
- **Interaction-defect scan:** PASS. The card's commands inside the new braces were each checked with `sh -n`. The pid race is ordered by two atomics: the cancel sets the flag and then reads the pid; the reader sets the pid and then reads the flag.
- **Housekeeping:** PASS. The full host suite is green at the ES tip. `proxycards-tests` is not built here (outside the brief's suite), as S2 noted.
- **Harness self-coverage:** PASS. Each fixture was seen to report the defect on the pin before it reported the fix.

## Code-verifiable state

| Bug | Stream | ES commit | Tests |
| --- | --- | --- | --- |
| #1147 | S1 | `1a1828a8b` | 2 `CloudTextTests` cases; `t18-why-table.py` |
| #1145 | S2 | `f63ad4de4` | an `AtomicFileTests` guard; `t18-stamp-fixture.py` (4 cases) |
| #1146, #1149 | S3 | `fd85f7e36` | an `AtomicFileTests` guard |
| #1148 | S4 | `2f109d935` | `t18-wrapper-fixture.py` (4 cases) |
| #1150 | S5 | `29d500db9` | 2 `CloudTextTests` cases, an `AtomicFileTests` guard, 1 `jobs-tests` case |
| #1151, #1152 | S6 | `d55235d4b` | 3 `jobs-tests` cases |
