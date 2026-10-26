# Punch list — M6.P2 T18, EmulationStation's cloud pages, cards and text (#665)

**Extended depth** (two seats: GPT-6 Astra at `max`, then Gemini 4 Argon at `high`; `04` § Second opinion). The audit issue is opened at stage D as a sub-issue of #665.

- **Eight `bug`s filed at the stage-D ruling** (#665, 11:16 UTC), all Low, each with its trace, `Already written:` line and VM line:
  - #1145 (PL-01);
  - #1146 (PL-02);
  - #1147 (PL-03, with PL-08's comments);
  - #1148 (PL-04);
  - #1149 (PL-05 and PL-07, one wording bug);
  - #1150 (PL-18);
  - #1151 (PL-20);
  - #1152 (PL-22).
  - PL-15 is not a bug here: #1142.
- **The streams:** `docs/reviews/briefs/t18-streams.md` at `1b6588efd8`, S1 to S6 on the ES branch.
- **Nothing** in this list changes a file under the distribution's `packages/`, `projects/` or `tools/`, or an ES file, at stages A to D. Removals: none; every dead end is a proposal.
- **One guest window**, 10:06:23 to 10:23:21 UTC at 640x480 (`02` § The guest cycle). **Nothing ran on a person's device or cloud.**

---

## PL-01: the card's stamp writer renames an unchecked write over the good stamp (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-06
- **Owner area:** es-app/src/ThreadedCloudSync.cpp (fork-own)
- **What:**
  - **The cause:** `writeStamp` (`:930-949`) writes `<stamp>.tmp` with `Utils::FileSystem::writeAllText`, which is `void` and checks neither `fwrite` nor `fclose` (`es-core/src/utils/FileSystemUtil.cpp:1429-1446`). It then renames the file over the stamp.
  - **The effect:** on a full `/storage` a cut or empty stamp replaces a whole one, and the row reads NOT DONE ON THIS DEVICE YET, against the comment's "written whole or not at all" (`:878-881`).
  - **A stale temporary** (Argon's R-9): when `fopen` fails and an earlier failed write left `<stamp>.tmp`, the rename puts that stale file over the stamp.
  - **The log:** both restamp functions log "restamped" after a write that may have failed, because `writeStamp` returns nothing (`:910-927`; Astra's A-10).
  - **The fix:** `Utils::AtomicFile::writeText`, which is tested in this slice and already used by `Settings.cpp` and `GuiMenu.cpp:5066`, with its result returned to the callers.
- **Evidence:** P16; A-10, A-30, R-9, R-24
- **Can this be done on the VM?** Yes. On the host, a case that runs the writer under `ulimit -f 0` with SIGXFSZ ignored shows the stamp survive after the fix. On the guest, a filled loop device.
- **Already written:** devices may hold old, empty or cut stamps, and the history a cut one lost cannot be rebuilt. The fix keeps the reader's legacy readability and writes new stamps whole; the next run rewrites a cut one. Nothing to migrate (A-30).
- **Acceptance:** with creation, the write, the close or the rename made to fail, and with a stale temporary present, the previous stamp's bytes are unchanged and the caller is told (a case that fails on the unfixed writer); with a normal write the new stamp is whole
- **Disposition note:** a `bug`, #1145, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8`

## PL-02: the CANCEL confirmation over a match promises that the next backup or restore finishes it (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-08
- **Owner area:** es-app/src/guis/GuiCloudTransfer.cpp (fork-own)
- **What:**
  - **The cause:** `askCancel` (`:351-361`) has words for a check and a create only.
  - **The effect:** a match gets `CANCEL THIS BACKUP OR RESTORE?` / `... THE NEXT BACKUP OR RESTORE FINISHES WHAT THIS ONE DIDN'T.` The next apply is refused with SOMETHING CHANGED SINCE YOU CHECKED (PL-001), and the page's own footer names the match's row (`CloudText::matchRecovery`).
  - **The fix:** a fourth arm for Match, in the maintainer's words, with French, and `docs/es-menu-map.md` § Cloud updated in the same change. It says what stays removed and that going on needs another check (A-31).
- **Evidence:** `02` § The strings; `guest-cycle/identity.out` (the string, 1 hit)
- **Can this be done on the VM?** Yes, given a fixture large enough for a match to run for a second. In the window it was `CANNOT` (a match ended at 0:00). The coordinator ruled the proof `fix-walk-pending-image`, with the before-frame owed to the integration build's walk.
- **Already written:** the dialog persists nothing, but a cancelled match's deletions stand and are not rolled back. The words must say so; nothing is migrated (A-31).
- **Acceptance:** a focused text and state case for the Match arm; and at 640x480, back pressed over a running match shows the match's own confirmation, its words read back, and NO returns to the run
- **Disposition note:** a `bug`, #1146, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8`

## PL-03: two script sentences have no row in the why table, and `backuptool`'s reaches the settings-restore page in English (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-11, F-12
- **Owner area:** es-app/src/CloudText.cpp (fork-own), with its French catalog rows
- **What:**
  - **The gap:** `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` (`backuptool:1495`) and `ANOTHER CLOUD SYNC IS RUNNING` (`cloud_setup:797`) have no `whySentences` pair.
  - **And a row that never matches** (Astra's A-36): `CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.` is stored with its full stop (`CloudText.cpp:425`). `classifyProtocolLine` and `parseLastRun` strip trailing full stops (`:577-578`, `:324-325`), so `localizedWhy` never finds it and it shows in English. It is the one such row.
  - **Why the tests passed** (Argon's R-16): the emitter table omits three rows that no test reaches through the protocol (`CHOOSE A CONNECTION ...`, `YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED`, `YOUR CLOUD FOLDER COULDN'T BE READ`).
  - **The effect:** when the SETTINGS part fails (not skips) with the why framed before it (A-14), the first reaches the settings restore page's line 4, because the chain keeps `backuptool restore`'s output (`GuiMenu.cpp:5043-5045`). It shows in English under a French outcome word.
  - **The comment:** `CloudText.cpp:419-422` says the test fails on a why a script prints that is missing. The test's table is typed and reads no script (F-12).
  - **The fix:** the two pairs and their French; the comment says what does check the table (`tools/t18-why-table.py`, or its promotion, PL-16).
- **Evidence:** P9, P10; `02` § The why table; A-14, A-17, A-32, A-36
- **Can this be done on the VM?** Yes. A `localizedWhy` case per pair on the host, failing before. On the guest, a settings archive the restore refuses, with the page's line 4 read in French.
- **Already written:** nothing inherited by the interface. The stamps keep the scripts' English by design.
- **Acceptance:** for every row, `isKnownWhy(classifyProtocolLine(">>> why " + row).text)` holds, which fails today on the full-stop row and on the two missing ones. A `localizedWhy` case cannot fail in a build without gettext (A-32). The generator reports `script_only 0` and compares the normalized text; a French frame of the refusal's line 4 reads French
- **Disposition note:** a `bug`, #1147, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8`

## PL-04: the card's scripts die of SIGPIPE when the interface goes, before they stamp (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-02
- **Owner area:** es-app/src/ThreadedCloudSync.cpp (fork-own)
- **What:**
  - **The cause:** the card's wrapper (`:206-207`) lacks the job's `trap '' PIPE` (`CloudTransferJob.cpp:636-637`), whose comment gives its purpose: a part that can still end writes its stamp.
  - **The effect:** with the interface gone, the card's scripts die at their next `echo`, before their stamp, and the rows read the run before.
  - **The fix:** the same wrapper for both, with the ignored disposition installed **before** the pid echo; the job's trap comes after it, so its first write is unprotected too (A-29). It must not promise that rclone completes, nor that a dead interface writes its own outcome.
- **Evidence:** r09; `03` § 3.5
- **Can this be done on the VM?** Yes. On the host, the two wrapper strings run under `sh` with the reader closed early. On the guest, `essway` stopped under a startup sync, then the stamps read.
- **Already written:** no stamp format changes. Earlier stamps can stand while some transfer work had already happened, and the next run's stamp replaces them; nothing is migrated (A-29).
- **Acceptance:** with the reader closed mid-run, the script's stamp is written under the fixed wrapper and not under the unfixed one
- **Disposition note:** a `bug`, #1148, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8`

## PL-05: `NOTHING NEW TO BRING DOWN` / `TO SEND UP` paraphrase the two verbs on the small panel

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-09
- **Owner area:** es-app/src/guis/GuiCloudTransfer.cpp
- **What:** the forms shown when `NOTHING NEW - YOU ALREADY HAD IT ALL` does not fit the line (`:805-808`); player-language.md asks for the canonical verb. The short forms are chosen by measurement, not by a panel size: how often a player sees them is the frame the window could not take (#1141). Whether they are wrong is not.
- **Evidence:** `02` § The strings; `guest-cycle/identity.out` (`NOTHING NEW TO SEND UP`, 1 hit)
- **Can this be done on the VM?** Yes, once #1141's walks run at 640x480.
- **Already written:** nothing.
- **Acceptance:** a 640x480 frame of a back up with nothing new, its line read back in the canonical verbs
- **Disposition note:** a `bug`, #1149, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8`

## PL-06: the match's done page names a system nothing was removed from

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q3
- **Source Finding:** F-20
- **Owner area:** es-app/src/CloudTransferJob.cpp
- **What:** at 640x480, `GB 1 FILE · 4 KB   SNES 0 FILES` (`guest-cycle/frames/640-match-done.png`). `handleLine` keeps every item of `>>> removed` (`:338-351`), a zero included. Either the script omits a zero, or the reader skips one.
- **Evidence:** P19
- **Can this be done on the VM?** Yes: the same walk.
- **Already written:** nothing.
- **Acceptance:** the done page lists only systems from which files were removed
- **Disposition note:** recorded as written, with its frame (`guest-cycle/frames/640-match-done.png`)

## PL-07: words in the formal register, and a third verb

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q3
- **Source Finding:** F-10
- **Owner area:** es-app/src/guis/GuiCloudTransfer.cpp
- **What:** `ITEM DID NOT FINISH` / `ITEMS DID NOT FINISH` (`:745`), where D-UI-031's register says `DIDN'T`; `FILES YOUR CLOUD HAD AND THIS DEVICE DIDN'T CAME DOWN TOO.` (`:769`, framed at 1280x800 in the stopped run).
- **Evidence:** `02` § The strings
- **Can this be done on the VM?** Yes: frames.
- **Already written:** nothing.
- **Acceptance:** the words put to the maintainer and changed with French, or recorded as kept
- **Disposition note:** a `bug`, #1149, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8`

## PL-08: comments that describe an older code (the futro's predicted stream)

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-13
- **Owner area:** the eight sources
- **What:**
  - the fallback map's comment names `WASN'T FOUND` and `REFUSED THE TRANSFER`, and sits above `writeStamp` (`ThreadedCloudSync.h:93-99`);
  - `SKIPPED - A GAME WAS STARTED` (`:70`);
  - the token list without `player-cancelled` and `no-folder` (`:126-130`);
  - `COMPLETED WITH GAPS` (`:158-159`);
  - "four words" (`ThreadedCloudSync.cpp:73`, `:460`; `CloudText.h:78-82`; `CloudText.cpp:298`);
  - the translation contract (`CloudText.h:9-18`);
  - `shortenWhy`'s two shapes (`:164-170`);
  - "Pid is the card's" (`CloudTransferJob.cpp:399-403`);
  - the leavable page's orphan line (`GuiCloudTransfer.h:156-157`).
- **Evidence:** `02` § Findings index; the generated fallback map
- **Can this be done on the VM?** Yes: a comment change; `tools/es-syntax-check` where a toolchain exists, else the host `g++ -fsyntax-only`, and the non-ASCII comment grep clean.
- **Already written:** nothing.
- **Acceptance:** each line says what the code at the pin does
- **Disposition note:** fixed in S1 with PL-03 (#1147)

## PL-09: the rule's half of the drift

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-14
- **Owner area:** .claude/rules/es-player-text.md (#909's)
- **What:** § Outcome vocabulary's **Why** sentence names `YOUR CLOUD FOLDER WASN'T FOUND` and `YOUR CLOUD REFUSED THE TRANSFER`, and claims them duplicated verbatim in the fallback map. The SKIPPED table lacks `SKIPPED - YOUR CLOUD FOLDER ISN'T SET UP YET` and `SKIPPED - YOU CANCELLED IT`.
- **Evidence:** P10
- **Can this be done on the VM?** Not a VM question: a rule's text.
- **Already written:** nothing.
- **Acceptance:** the rule's sentence matches `whyForCode` at the pin
- **Disposition note:** deferred:#909 (the coordinator's line posted there)

## PL-10: exit 75 in eight wordings

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-15
- **Owner area:** the eight, and the scripts (`cloud_setup`, `cloud_scan`, `backuptool`)
- **What:** the card's two, the page's scan word, the why row, the folder refusal's, `cloud_setup`'s, `cloud_scan`'s and `backuptool`'s (§ The why table). They are not eight outcomes for one slot: some are reasons, some recovery lines, and two name another lock (A-16). A review of synonyms, not a unification.
- **Evidence:** P10
- **Can this be done on the VM?** Not a VM question: words.
- **Already written:** nothing.
- **Acceptance:** the coordinator's choice of which to keep, recorded
- **Disposition note:** recorded as written: the eight wordings listed in `02` § The why table

## PL-11: what the retired folder move and folder step left behind

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-16
- **Owner area:** es-app/src/CloudTransferJob.cpp, guis/GuiCloudTransfer.{h,cpp}, CloudText.cpp
- **What:**
  - the `doing` words `copy`, `verify` and `remove` and their three strings;
  - the `DISCARDED SAVES` label;
  - the why row `YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED`;
  - `setFailedNote` and `setDismissedAction`, which have no caller;
  - the `cancellable` parameter, never passed;
  - the comments that name them.
- **Evidence:** P13, P14
- **Can this be done on the VM?** Yes: a removal proved by the unit tests and the walks unchanged.
- **Already written:** the French catalog carries the three strings and the label; a removal takes their rows too.
- **Acceptance:** removals none at stages A to D; a proposal the coordinator rules on
- **Disposition note:** deferred:#1143 (removals proposed, none made here)

## PL-12: `CloudText::nextTime` has no product caller

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-17
- **Owner area:** es-app/src/CloudText.{h,cpp}
- **What:** declared and tested; the exit card composes its own sentences. `isKnownWhy` and `isKnownUnitLabel` are test-only, which is their job.
- **Evidence:** P12
- **Can this be done on the VM?** Yes: the unit tests.
- **Already written:** nothing.
- **Acceptance:** kept with its reason, or proposed for removal
- **Disposition note:** deferred:#1143

## PL-13: the protocol's latent edges

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q3
- **Source Finding:** F-01, F-03, F-04; A-6; R-1, R-4, R-6
- **Owner area:** es-app/src/CloudTransferJob.cpp, ThreadedCloudSync.cpp
- **What:**
  - **F-01:** both readers take a pid from any `>>> pid` line, and `>>> pid 1` would signal every process. Only the wrappers print one.
  - **F-03:** an unknown marker vanishes without a log line.
  - **F-04:** the card's `fgets` 512 splits a longer line.
  - **R-1:** `case Doing:` leaves `mCurrent`, `mChecksTotal` and `mListed`, which outrank `mDoing` on row 3. Every producer announces its `doing` after a fresh unit, so it is latent.
  - **R-4:** a junk or 0 second `>>> pid` sets the pid to 0 and disarms a stop.
  - **R-6:** `atol` on a torn count line can double-count a unit's files.
  - None fails today. Each is a line of hardening: take the first pid, `LOG` an unknown marker once, use the job's reader.
- **Evidence:** `02` § The protocol
- **Can this be done on the VM?** Yes, with the unit tests' fixtures.
- **Already written:** nothing.
- **Acceptance:** recorded, or taken into the Q1 seam's stream
- **Disposition note:** recorded as written; folded into the seam #1143 names

## PL-14: two piped-progress traps without a case

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** F-05
- **Owner area:** es-app/src/CloudTransferJob.cpp; es-app/tests/unit
- **What:**
  - the `%3d` separator at 100% (`:529-551`), the job's glued splitter (`:654-677`) and the page formatter's torn-field rejection (`GuiCloudTransfer.cpp:635-668`) have no unit case (A-18). Moving the per-file split into `CloudText` lets the existing binary test it;
  - no case covers the card's cancel after a late pid or against a natural completion, a page deleted before its posted step, or a failed stamp write (A-19);
  - the page formatter's four-byte separator check before `LEFT` (`GuiCloudTransfer.cpp:678-687`), a normalization round-trip for every why row, and a glued `>>> ` (Argon's R-18);
  - the fit is owed per row: the title, the running counter, the finished footer and most `doing` lines are set without `fitOneLine` and grow rather than clip (A-40).
- **Evidence:** `02` § The tests
- **Can this be done on the VM?** Yes: the host unit tests.
- **Already written:** nothing.
- **Acceptance:** a case per trap, failing on a parser that splits on `": "`
- **Disposition note:** the unfitted rows fixed in S3 (#1149's stream); the untested traps' cases with the streams that touch them

## PL-15: the launch's stop spins up to 2 s on the interface thread

- **Severity:** Info
- **Category:** Design
- **Question:** Q5
- **Source Finding:** F-07
- **Owner area:** es-app/src/ThreadedCloudSync.cpp (the spin); es-app/src/FileData.cpp (the caller, T2's)
- **What:** `cancelForLaunch` (`:834-863`) runs inside the STOP IT AND PLAY callback (`FileData.cpp:1001`), so nothing is drawn while it spins. 02 compared it with D-CLOUD-119's 3 s, which is the exit sync's own completion target, a different measure (A-11). The transfer's question waits behind `launchWhenGone`'s spinner instead. The window measured the question answered at 1.34 s and the next game's first frame at 1.01 s.
- **Evidence:** P15, P20
- **Can this be done on the VM?** Yes: `time-to-play`'s game-to-game cell, frames during the wait.
- **Already written:** nothing.
- **Acceptance:** routed to the launch path's owner (T2's) with the measurement
- **Disposition note:** deferred:#1142 (the coordinator's, under #700: T2's bounded wait on the wrong thread)

## PL-16: one reader for the two surfaces, and the why table's check where the scripts are

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** F-18, F-12, F-19
- **Owner area:** the eight; tools/ (the coordinator's)
- **What:**
  - **The readers:** the wrapper, the framing and a trusted pid, built once for both (`04` § Q1), without copying the job's cap and discard, and without erasing the surfaces' intended differences (A-28).
  - **A check where the scripts are:** `tools/t18-why-table.py` promoted into `tools/vm-qa`'s `french` suite, so a new script sentence fails a suite.
  - **`tests/app-unit` in a suite:** `jobs-tests` passed here (6 cases), but no standing command builds it.
- **Evidence:** `02` § The protocol, § The why table, § The tests
- **Can this be done on the VM?** Yes.
- **Already written:** nothing.
- **Acceptance:** proposals ruled on by the coordinator
- **Disposition note:** the one-reader refactor deferred:#1143; the two suites deferred:#1144 (under #903)

## PL-17: notes for other slices, and the harness

- **Severity:** Info
- **Category:** Design
- **Question:** Q7
- **Source Finding:** the window's frames; F-19
- **Owner area:** T26 (`GuiMenu.cpp`); #903 (the harness)
- **What:**
  - **For T26**, read from frames of `GuiMenu.cpp`'s pages at 640x480:
    - the hub's `BRING DATA BACK ONTO THIS DEVICE.` (`640-cloud-hub.png`), a paraphrase of *restore*;
    - the match confirmation's `... IS DOWNLOADED AT THE SAME TIME.` (`640-match-confirm.png`), a word the rule keeps out of labels.
  - **For the harness:** #1141, `vm-pair` at 1280x800 and the transfer walks at 640x480.
  - **For T17:** #1140, `cloud_content_transfer`'s TERM exiting 143.
  - **For T26** (Astra's A-39): the settings backup's chain discards `backuptool backup`'s output (`GuiMenu.cpp:5125`), its whys included, unlike the restore's.
- **Evidence:** `guest-cycle/frames/`
- **Can this be done on the VM?** Yes.
- **Already written:** nothing.
- **Acceptance:** each routed by number
- **Disposition note:** routed: the T26 notes posted on #673; #1141 (the harness); #1140 (T17's TERM)

## PL-18: a stop or cancel against a run that is ending, a cancel before a late pid, and the linger's launch (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** A-33, A-34 (Astra, new); R-8, R-11, R-39, R-41 (Argon, new)
- **Owner area:** es-app/src/ThreadedCloudSync.cpp, es-app/src/CloudTransferJob.cpp; ProxyCards.cpp's guard is the offline achievements slice's
- **What:**
  - **A-33:** the card samples `mCancelled` after `pclose` (`:446-458`) while `mInstance` still names it until `:716-720`. A cancel in that interval turns a run that completed into `SKIPPED - YOU STARTED A GAME`, with its stamp 130 `cancelled`. The job clears its stop on a natural 0 or 9 (`CloudTransferJob.cpp:691-696`); the card has no such check.
  - **R-11 and R-41, the job's own window:** `pclose` (`CloudTransferJob.cpp:679`) reaps before the lock at `:684`. A stop in that window marks a run that failed on its own (5, 69, 75) as stopped, because `:691` clears the stop only on 0 or 9, and its real outcome reads `SKIPPED - YOU CANCELLED IT`.
  - **R-8 and R-39, the linger:** once `mInstance` is cleared (`:716-720`), a launch is allowed during the 1.5 s or 5 s linger. Then `CloudOffer::present` (`:741`) and `ProxyCards::afterSync` (`:754-755`) run over the game that started; `afterSync` has no running-game guard (`ProxyCards.cpp:543-551`).
  - **A-34:** when the pid has not arrived within the 2 s budget (`:845-863`), nothing keeps the stop for it. The run goes on and ends labelled cancelled. The job keeps a pending request that its pid line delivers.
- **Evidence:** the re-reads at the pin (`04` § Second opinion)
- **Can this be done on the VM?** Yes. On the host, the card's decision moved into pure code with both orderings as cases. On the guest, a cancel timed at a sync's end (`time-to-play`'s game-to-game cell is the shape).
- **Already written:** `last-sync-exit` and `last-sync-startup` stamps on devices may read 130 `cancelled` for runs that completed; their rows say SKIPPED where COMPLETED was true. The next run's stamp replaces them; nothing to migrate.
- **Acceptance:** a completion that a cancel races reads COMPLETED, and a failure that a stop races keeps its own outcome, in both readers; a stop before a late pid is delivered when the pid arrives; nothing the card raises after its linger lands over a game that started in it
- **Disposition note:** a `bug`, #1150, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8`

## PL-19: a protocol line glued to an unterminated rclone tail

- **Severity:** Info (plausible)
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** A-35 (Astra, new)
- **Owner area:** es-app/src/CloudTransferJob.cpp, ThreadedCloudSync.cpp
- **What:** the job splits a glued `Transferred:` but not a glued `>>> `. If rclone's last per-file line ends without a newline and a composer's `echo '>>> tier ...'` follows at once, the marker arrives inside a non-protocol line and is lost, and with it a part's outcome. Whether rclone's final block ends in a newline when it exits is unread.
- **Evidence:** the code at `CloudTransferJob.cpp:641-669`; no fixture yet
- **Can this be done on the VM?** Yes. A host fixture pipes the donor's rclone 1.75.2 through the job's reader with a composer's echo after it; or the guest's `run-transfer` walk once #1141 lets it run.
- **Already written:** nothing.
- **Acceptance:** the fixture shows whether the marker survives; if not, the readers split on `>>> ` as they split on `Transferred:`
- **Disposition note:** S4's fixture first; a fix only if it falls

## PL-20: a part's early why is blamed on the previous part's unit (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** A-37 (Astra, new)
- **Owner area:** es-app/src/CloudTransferJob.cpp
- **What:** a tier line clears the pending whys and the units since it (`:333-335`) but not `mUnitLabel`, which labels the next why (`:287`). A part that says why before its first `>>> unit` (`cloud_content_restore`'s early refusals, for one) has the why filed under the previous part's unit, which may have completed. Line 4 then names the wrong item.
- **Evidence:** the re-read at the pin
- **Can this be done on the VM?** Yes. `jobs-tests`' shape (the shipped job with doubles) runs a composed command whose second part prints a why before its unit.
- **Already written:** nothing persisted. Line 4 is the page's.
- **Acceptance:** that run's line 4 names the second part, not the first
- **Disposition note:** a `bug`, #1151, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8`

## PL-21: a 9 after a failed part reads COMPLETED

- **Severity:** Info (latent)
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** A-38 (Astra, new); R-40 (Argon, new)
- **Owner area:** es-app/src/guis/GuiCloudTransfer.cpp (`outcome()`); es-app/src/guis/GuiMenu.cpp (the composers, T26's)
- **What:**
  - **The composer:** `GuiMenu.cpp:5006` sets `rc` from any nonzero part, a 9 included, so a failed part followed by a 9 ends 9.
  - **The page:** `outcome()` (`:435`) calls 0 or 9 COMPLETED without asking the tiers.
  - **The manual sync:** its composer (`GuiMenu.cpp:6140`) skips the backup on a restore's 9.
  - **Both readers** decide COMPLETED from the last code without asking the tiers (`ThreadedCloudSync.cpp:494`, `GuiCloudTransfer.cpp:435`). The card's `badTiers` drops each tier's code (`:482-483`), so a failed tier with no why gets the last command's phrase (R-40).
  - **The startup composer** (`main.cpp`) exits the restore's code first, so a restore's 9 hides the backup's failure.
  - **Why it is latent:** at `8ebaf8daad` no script passes `--error-on-no-transfer`, so rclone returns 9 only when a player's own `RCLONEOPTS` carries the flag.
- **Evidence:** the re-reads; `git grep error-on-no-transfer` at `8ebaf8daad`: 0
- **Can this be done on the VM?** Yes: `jobs-tests`' shape with a composed `exit 5`, then `exit 9`.
- **Already written:** nothing persisted beyond the run's stamps, which the scripts write per part.
- **Acceptance:** the page's word follows the failed tier; the composers' handling of 9 recorded for T26
- **Disposition note:** the readers' half recorded as written (latent); the composers' half posted on #673

## PL-22: a content transfer the network cut part-way reads COULDN'T FINISH with no why (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** R-42 (Argon, new)
- **Owner area:** es-app/src/CloudTransferJob.cpp
- **What:**
  - **The scripts:** `cloud_content_backup` and `cloud_content_restore` exit 69 after progress with only a stamp, `69 gaps YOU WENT OFFLINE PART-WAY THROUGH`, and no `>>> why` (`:336-342`, `:391-397` at `8ebaf8daad`).
  - **The page:** it reads the run as COULDN'T FINISH, because it progressed (`GuiCloudTransfer.cpp:453-467`). But `run()` leaves 69 out of its fallback (`CloudTransferJob.cpp:721`) and never reads `CloudText::offlinePartWayWhy` as the card does (`ThreadedCloudSync.cpp:509-511`). Line 4 is blank: an outcome with no why, against D-UI-028.
  - **The scripts' own comment** (`cloud_content_restore:372`) says the page reads a 69 after progress the same way; it does not.
- **Evidence:** the re-read (`04` § Second opinion, R-42)
- **Can this be done on the VM?** Yes. The guest's QA WebDAV cut by `cloud-test-backend`'s dead port part-way through a content transfer; line 4 read back. Or `jobs-tests`' shape with a command that writes the stamp and exits 69.
- **Already written:** the scripts' stamps already carry the why, so the rows under the toggles say it; only the page's line is missing. Nothing to migrate.
- **Acceptance:** that run's line 4 reads `YOU WENT OFFLINE PART-WAY THROUGH` in the interface's language
- **Disposition note:** a `bug`, #1152, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8`

## PL-23: the job's run why is written and never read

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** R-43 (Argon, new)
- **Owner area:** es-app/src/CloudTransferJob.{h,cpp}
- **What:** `mWhy` is written on every why (`:286`) and read nowhere (`git grep -w mWhy`), against its comments (`:244`, `.h:173`). The no-tier fallback (`:717-720`) copies pending whys without the tier arm's de-duplication, and drops them when an earlier tier failed. Every composer echoes a tier after each part, so the second half is latent.
- **Evidence:** the re-read
- **Can this be done on the VM?** Yes: the unit tests and `jobs-tests`.
- **Already written:** nothing.
- **Acceptance:** `mWhy` removed or read; the fallback's behaviour recorded
- **Disposition note:** deferred:#1143

## Phase 7 resolution gate

Every item is open until stage F; each row then takes its outcome (resolved with its commit, deferred to a named issue, or recorded as a design with its sentence). The dispositions are the coordinator's stage-D ruling (#665, 11:16 UTC).

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | at the stage-D pause; disposition: a `bug`, #1145, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8` |
| PL-02 | Open | at the stage-D pause; disposition: a `bug`, #1146, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8` |
| PL-03 | Open | at the stage-D pause; disposition: a `bug`, #1147, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8` |
| PL-04 | Open | at the stage-D pause; disposition: a `bug`, #1148, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8` |
| PL-05 | Open | at the stage-D pause; disposition: a `bug`, #1149, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8` |
| PL-06 | Open | at the stage-D pause; disposition: recorded as written, with its frame (`guest-cycle/frames/640-match-done.png`) |
| PL-07 | Open | at the stage-D pause; disposition: a `bug`, #1149, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8` |
| PL-08 | Open | at the stage-D pause; disposition: fixed in S1 with PL-03 (#1147) |
| PL-09 | Open | at the stage-D pause; disposition: deferred:#909 (the coordinator's line posted there) |
| PL-10 | Open | at the stage-D pause; disposition: recorded as written: the eight wordings listed in `02` § The why table |
| PL-11 | Open | at the stage-D pause; disposition: deferred:#1143 (removals proposed, none made here) |
| PL-12 | Open | at the stage-D pause; disposition: deferred:#1143 |
| PL-13 | Open | at the stage-D pause; disposition: recorded as written; folded into the seam #1143 names |
| PL-14 | Open | at the stage-D pause; disposition: the unfitted rows fixed in S3 (#1149's stream); the untested traps' cases with the streams that touch them |
| PL-15 | Open | at the stage-D pause; disposition: deferred:#1142 (the coordinator's, under #700: T2's bounded wait on the wrong thread) |
| PL-16 | Open | at the stage-D pause; disposition: the one-reader refactor deferred:#1143; the two suites deferred:#1144 (under #903) |
| PL-17 | Open | at the stage-D pause; disposition: routed: the T26 notes posted on #673; #1141 (the harness); #1140 (T17's TERM) |
| PL-18 | Open | at the stage-D pause; disposition: a `bug`, #1150, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8` |
| PL-19 | Open | at the stage-D pause; disposition: S4's fixture first; a fix only if it falls |
| PL-20 | Open | at the stage-D pause; disposition: a `bug`, #1151, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8` |
| PL-21 | Open | at the stage-D pause; disposition: the readers' half recorded as written (latent); the composers' half posted on #673 |
| PL-22 | Open | at the stage-D pause; disposition: a `bug`, #1152, filed at the stage-D ruling (#665, 11:16 UTC); fixed by a stream under `t18-streams.md` at `1b6588efd8` |
| PL-23 | Open | at the stage-D pause; disposition: deferred:#1143 |

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-06"
  outcome: "open"
- id: PL-02
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-08"
  outcome: "open"
- id: PL-03
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-11, F-12"
  outcome: "open"
- id: PL-04
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-02"
  outcome: "open"
- id: PL-05
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-09"
  outcome: "open"
- id: PL-06
  severity: "Info"
  category: Renovation
  question: Q3
  source_finding: "F-20"
  outcome: "open"
- id: PL-07
  severity: "Low"
  category: Renovation
  question: Q3
  source_finding: "F-10"
  outcome: "open"
- id: PL-08
  severity: "Info"
  category: Renovation
  question: Q7
  source_finding: "F-13"
  outcome: "open"
- id: PL-09
  severity: "Info"
  category: Renovation
  question: Q7
  source_finding: "F-14"
  outcome: "open"
- id: PL-10
  severity: "Info"
  category: Renovation
  question: Q7
  source_finding: "F-15"
  outcome: "open"
- id: PL-11
  severity: "Info"
  category: Renovation
  question: Q6
  source_finding: "F-16"
  outcome: "open"
- id: PL-12
  severity: "Info"
  category: Renovation
  question: Q6
  source_finding: "F-17"
  outcome: "open"
- id: PL-13
  severity: "Info"
  category: Renovation
  question: Q3
  source_finding: "F-01, F-03, F-04; A-6; R-1, R-4, R-6"
  outcome: "open"
- id: PL-14
  severity: "Info"
  category: Renovation
  question: Q2
  source_finding: "F-05"
  outcome: "open"
- id: PL-15
  severity: "Info"
  category: Design
  question: Q5
  source_finding: "F-07"
  outcome: "open"
- id: PL-16
  severity: "Info"
  category: Renovation
  question: Q1
  source_finding: "F-18, F-12, F-19"
  outcome: "open"
- id: PL-17
  severity: "Info"
  category: Design
  question: Q7
  source_finding: "the window's frames; F-19"
  outcome: "open"
- id: PL-18
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "A-33, A-34 (Astra, new); R-8, R-11, R-39, R-41 (Argon, new)"
  outcome: "open"
- id: PL-19
  severity: "Info"
  category: Correctness
  question: Q3
  source_finding: "A-35 (Astra, new)"
  outcome: "open"
- id: PL-20
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "A-37 (Astra, new)"
  outcome: "open"
- id: PL-21
  severity: "Info"
  category: Correctness
  question: Q3
  source_finding: "A-38 (Astra, new); R-40 (Argon, new)"
  outcome: "open"
- id: PL-22
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "R-42 (Argon, new)"
  outcome: "open"
- id: PL-23
  severity: "Info"
  category: Renovation
  question: Q6
  source_finding: "R-43 (Argon, new)"
  outcome: "open"
```
