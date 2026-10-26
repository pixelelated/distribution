# Second opinion (Phase 4.6), M6 T18: EmulationStation's cloud pages, cards and text, in pixelelated's EmulationStation fork

You are one of two independent reviewers for a read-only renovation audit of 30 files, all of them the fork's, read under a **brittleness and new-functionality lens**. They total 11,193 lines at the EmulationStation commit `16dbac5211` (the distribution pins that commit).

- **The eight sources:**
  - `CloudText.{h,cpp}`, the pure text and the one protocol parser;
  - `CloudTransferJob.{h,cpp}`, a long transfer's run, apart from its page;
  - `GuiCloudTransfer.{h,cpp}`, the transfer page;
  - `ThreadedCloudSync.{h,cpp}`, the sync card.
- **The 22 unit-test files** under `es-app/tests/unit/`.

**What ships.** The product is an immutable handheld OS; a person updates it in place and keeps `/storage`.

- EmulationStation is its interface, at 640x480 on the smallest panel.
- The cloud scripts (busybox, bash, rclone 1.75.2) talk to these two readers through `>>> ` lines on a pipe, and stamp each run's outcome under `/storage/.cache/cloud_sync/`.
- One player uses one console at a time.
- The rules the code answers to are named in `03` § 3.2: the four ES rule files, the outcome vocabulary, least surprise, time to play, and fail closed.

**What you get.**

- The first reader is another lab's model. You get its `02-forward-audit.md` (whole, with its two generated tables), `03-retrospective.md` and `04-analysis.md`.
- Then context: the order's entry, the brief's questions, and the register rows the code cites.
- Then three files whole and line-numbered: `CloudTransferJob.cpp`, `ThreadedCloudSync.cpp` and `GuiCloudTransfer.cpp`.
- Then **line-numbered excerpts** of their three headers, `CloudText.h`, `CloudText.cpp` and `CloudTextTests.cpp`, covering every line the analyses cite, with eight lines of context.
- Then the callers' lines the analyses cite, from `FileData.cpp` and `GuiMenu.cpp`, also excerpted.
- **When a claim needs lines outside the packet, say `outside the packet` and do not guess.**

**Masking.** Every section was passed through a mask that replaces a value after `key=`, `key:`, `token=`, `user=`, `pass...=` or `psk=` with `***`; a `***` is the mask, not the code. The packet was scanned for credential shapes before it left, and no hit was a value.

**Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong. Its line numbers are the pin's.

**What was run.** Nothing can be run for you.

- The unit tests were built on the host and pass: 221 cases, and `tests/app-unit`'s `jobs-tests`, 6 cases.
- A guest window ran the walks on an image whose interface carries the pin's strings. Its frames are not in this packet.

Answer these first, in this order:

1. **The protocol under a pipe (`02` § The protocol; F-01 to F-05, F-18).**
   - Is every `>>> ` marker's reader right, in both readers?
   - What does a line the parser calls `Unknown` become in each?
   - Are the two wrappers' difference (`trap '' PIPE`) and its consequence (F-02) right?
   - Can `>>> pid` reach either reader from anything but the wrapper's first line, and what would a second one do (F-01)?
   - Are the rclone parsers sound against a pipe? Check the glued `Transferred:`, the 80-column cut, the `%3d` separator and U+2026, in `CloudTransferJob.cpp:410-558` and `CloudText::liveLine`.
   - Is anything parsed with `atoi` where a junk field would read as a meaningful zero?
2. **Lifetimes and threads (`02` § The lifetimes; F-06, F-07, F-19).**
   - Does anything hold a page, a card or a job across its own deletion?
   - Are the card's `mInstance` contract and its 1.5 s / 5 s linger sound against `cancelForLaunch`?
   - Is F-06 right? `writeStamp` renames an unchecked write.
   - Is F-07 right? The 2 s spin runs on the interface thread.
   - Do `stopForLaunch`, `stopByPlayer`, `requestStop` and `deliverStop` close every race their comments name?
3. **The words (`02` § The strings and § The why table; F-08 to F-15).**
   - Is each failure real against es-player-text.md as `03` quotes it?
   - Is F-08's dialog really reached over a match?
   - Does `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` really reach line 4 in English (F-11)?
   - Is the fallback map's comparison right?
4. **The tests (`02` § The tests; F-05, F-12).**
   - Does any test claim more than it checks?
   - Is the emitter table's guard what the comment at `CloudText.cpp:419-422` says?
   - Which traps are untested?

Then:

5. **Refute or confirm each finding F-01 to F-19** in `02` § Findings index: *confirmed*, *narrowed* (say how), or *refuted* (with the line). For the four proposed bugs, B1 to B4 in `04` § Q3, also judge the severity, the fix proposed, and its `Already written:` line: what the code before a fix has already left on devices and in their clouds.
6. **What the first reader missed:**
   - a defect in the whole files or the excerpts: a write judged by nothing, a pipe read that loses a line, a pointer used after its owner goes, a lock taken in the wrong order, a string that promises what the code does not do, or a stamp that can say the wrong thing;
   - a test whose subject is gone;
   - a disposition that should be different.

**Output:**

- Numbered items `{PREFIX}-1`, `{PREFIX}-2`, ..., grouped under the six headings above.
- Each item gets one line saying *confirmed / narrowed / refuted / new*, then the `file:line` evidence, then two to five sentences.
- Do not restate the packet, and do not reproduce long code.
- Keep the whole reply under about 8,000 words.
