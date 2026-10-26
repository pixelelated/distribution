### GPT-6 Astra (`gpt`, `openai/gpt-6-astra`, `max`): 42 items, graded

**The calls:**

- Call 1, the probe: 10:26:38 to 10:26:57 UTC, PASS.
- Call 2, the refutation: 10:27:06 to 10:47:10 UTC, one attempt, `finish=stop`, 28,540 bytes.
- Both were served `openai/gpt-6-astra` by OpenAI (`stage-c/provenance-read.txt`).

Each item was re-read at its lines at the pin before it was graded. **Accepted** means the lane takes the item as written. **Narrowed** means accepted with the limit stated. **Rejected** means the lines say otherwise. **Plausible** means the code allows it and no fixture has shown it. Where a seat said `outside the packet`, the lane's own evidence is named.

| Item | Grade | The lane's re-read, and where it lands |
| --- | --- | --- |
| A-1 | accepted | Both `default:` arms drop an unknown marker without a log line; the card's also clears `mWaitingForNetwork` (`ThreadedCloudSync.cpp:330-332`). F-03, PL-13. |
| A-2 | accepted, narrowed | The producer search the seat could not see is P14's `git grep` at `8ebaf8daad` and in `es-app/src`: only the three wrappers print `>>> pid`. "Every process" corrected: `kill(-1, ...)` reaches every process the sender may signal, which under EmulationStation's root is nearly all. A second pid does not redirect a stop already sent by the job (`mSignalSent`). F-01, PL-13. |
| A-3 | accepted | The job's trap comes after its pid echo, so its first write is unprotected too. The fix (PL-04) installs the ignored disposition before the echo. The scripts' traps were read (`cloud_backup:2504`: INT and TERM, not PIPE); whether a given write dies depends on the writer, as the seat says. F-02, PL-04. |
| A-4 | accepted | A fragment of a split line can begin with `>>> ` and be classified; 02's "the second half is not a protocol line" was too strong. Either cap can damage a payload. F-04, PL-13. |
| A-5 | accepted | The `%3d` separator is handled in the code; it is untested (F-05). U+2026: `cleanLine` keeps UTF-8 (`CloudText.cpp:485-533`), and `CloudTextTests.cpp:564` is its case. Both are in the lane's read and outside the seat's packet. |
| A-6 | accepted | `atol` on `>>> removed`'s totals and on the job's counters: junk reads 0 and can hide the removal summary. A note in PL-13. |
| A-7 | accepted | Confirms the page's and the job's deletion paths and the lock order. A positive. |
| A-8 | accepted, narrowed | The header's "outlives the call" (`ThreadedCloudSync.h:193-199`) is too strong: the call drops the lock between polls. The SIGKILL at `:859` uses a cached pid outside the lock, a check-to-signal window against pid reuse. A comment (PL-08) and a latent edge (PL-13). |
| A-9 | accepted | The job's races are closed; the card's are not (A-33, A-34). |
| A-10 | accepted, extended | Both restamp functions log "restamped" after a write that may have failed (`ThreadedCloudSync.cpp:910-927`): `writeStamp` returns nothing. The unchecked `fwrite`/`fclose` the seat could not see is P16 (`FileSystemUtil.cpp:1429-1446`). PL-01. |
| A-11 | accepted | The 2 s figure against D-CLOUD-119's 3 s compares unlike measures, as the seat says: 02's Q5 sentence is reworded. A-42 asks for a defect rather than a design note: proposed so in PL-15 for the coordinator. |
| A-12 | accepted | The match is cancellable (`cancellable()` has no Match exclusion), so the branch is reached in the page's state machine whatever a fixture's timing. PL-02. |
| A-13 | accepted | The short forms are chosen by measurement. 02's "where most players read it" is unproved and is withdrawn. A reachable non-canonical wording is a wording defect whatever the frame (A-42). PL-05. |
| A-14 | accepted, narrowed | Conditional: a SETTINGS tier that fails, not skips, with the why framed before it. `backuptool:1495` prints it (`why`, `:1495`) before `fail` (`:1496`), read at `8ebaf8daad`. PL-03. |
| A-15 | accepted | The fallback map omits codes 6 and 10: `whyForCode(6)` and `whyForCode(10)` fall to `SOMETHING WENT WRONG`, where the scripts' `why_for` says `SOME FILES DIDN'T FINISH` and, on an automatic run, `THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME`. The generator's "agree on every group" covered only the groups it listed; it now lists 6 and 10. F-13, F-14, PL-08. |
| A-16 | accepted | The eight strings are not eight outcomes for one slot: some are reasons, some recovery lines, and two name a different lock. PL-10 is reworded as a review, not a unification. |
| A-17 | accepted | F-12 as written, and the spelling test proves no catalogue (no gettext in the unit build). PL-03, PL-16. |
| A-18 | accepted | F-05's coverage is narrower still: the page formatter's torn-field rejection is untested too. PL-14. |
| A-19 | accepted | No case covers the card's cancel after a late pid or against a natural completion, a page deleted before its posted step, or a failed stamp write. PL-14 adds them. |
| A-20 | accepted | The summary of A-2 to A-4. |
| A-21 | accepted | The summary of A-1, A-10 and A-11. |
| A-22 | accepted | F-08, F-10 and F-12 confirmed. |
| A-23 | accepted, narrowed | F-19's "no standing command builds it" is the lane's reading of `tools/vm-qa`'s suites; its `lifetime` suite builds part of `tests/app-unit` (`02` § The tests). |
| A-24 | accepted | F-09 and F-11 as narrowed in A-13 and A-14. |
| A-25 | accepted | `shortenWhy`'s third shape is at `CloudText.cpp:377-379`, in the lane's read. The rule's text is in `03` § 3.2 and the generator reads it whole. |
| A-26 | accepted | As A-16. |
| A-27 | accepted, narrowed | The usage census the seat could not see is P12 to P14. "Test-only" is not a removal argument, and PL-12 says so. |
| A-28 | accepted | A shared reader must not copy the job's cap and discard, nor erase the surfaces' intended differences. PL-16 reworded. |
| A-29 | accepted | B1/PL-04: the trap goes before the pid echo. Already written: earlier stamps can stand while some transfer work had happened; the line is corrected. |
| A-30 | accepted | B2/PL-01: test failed creation, a failed write or close, a failed rename and a stale temporary; the result returned to the callers. Already written: devices may hold old, empty or cut stamps whose history cannot be rebuilt, and legacy readability is kept. |
| A-31 | accepted | B3/PL-02: the match's own words say what stays removed and that going on needs another check. Already written: a cancelled match's deletions stand. |
| A-32 | accepted | B4/PL-03: a `localizedWhy` case cannot fail in a build without gettext. The regression checks membership after protocol normalization (`isKnownWhy(classifyProtocolLine(">>> why " + s).text)`) for every row, with the generator as the emitter check. |
| A-33 | accepted, **new**, confirmed | The card samples `mCancelled` after `pclose` (`ThreadedCloudSync.cpp:446-458`), and a cancel can still land while `mInstance` names it (cleared at `:716-720`). A run that completed reads `SKIPPED - YOU STARTED A GAME`, with its stamp 130 `cancelled`. The job clears its stop flags on a natural 0 or 9 (`CloudTransferJob.cpp:691-696`); the card has no such check. The window is narrow but real. PL-18. |
| A-34 | accepted, **new**, confirmed, latent | When the pid has not arrived within the 2 s budget (`:845-863`), no stop is kept for it: the run goes on and is labelled cancelled. The wrapper's echo is the first line, so a late pid needs a stalled shell. PL-18. |
| A-35 | plausible, **new** | An rclone tail with no newline, followed at once by a composer's `echo '>>> tier ...'`, would arrive as one line, which classifies as `NotProtocol`. Whether rclone's last block ends in a newline when it exits is not read. A real-pipe fixture with the donor's rclone is the proof (PL-19). |
| A-36 | accepted, **new**, confirmed | `CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.` is stored with its full stop (`CloudText.cpp:425`); `classifyProtocolLine` strips trailing full stops (`:577-578`), so the row is never matched. It is the one such row. The generator compared the raw strings and missed it. PL-03. |
| A-37 | accepted, **new**, confirmed | A tier line clears the pending whys and the units since the tier (`CloudTransferJob.cpp:333-335`) but not `mUnitLabel`, which `:287` uses to label a why. A part that says why before its first unit is blamed on the previous part's unit, which may have succeeded. PL-20. |
| A-38 | accepted, **new**, confirmed in the code, latent | `GuiMenu.cpp:5006`'s composer sets `rc` from any nonzero part, a 9 included, so a failed part followed by a 9 ends 9. The page's `outcome()` (`GuiCloudTransfer.cpp:435`) calls 0 or 9 COMPLETED without asking the tiers. The manual sync composer (`GuiMenu.cpp:6140`) skips its backup on a restore's 9. No script passes `--error-on-no-transfer` at `8ebaf8daad`, so rclone returns 9 only for a player's own `RCLONEOPTS` carrying it. PL-21. |
| A-39 | accepted, **new** | The settings backup's chain discards `backuptool backup`'s output (`GuiMenu.cpp:5125`), its whys included. The caller's, T26's. PL-17. |
| A-40 | accepted | Not every row is fitted: the title (`:56`), the running counter (`:936-939`), the finished footer (`:913-915`) and most `doing` lines (`:1035`) are set without `fitOneLine`. With `setSize(w, 0)` they grow rather than clip. 02's sentence ("the trap does not apply to a row that never wraps") is withdrawn, and the fit is owed per row. PL-14. |
| A-41 | accepted | "No case whose subject is gone" is unproved at the feature level (a case may test a live function of a retired flow). Q6 reworded. |
| A-42 | accepted in part | F-07 is proposed as a defect for the coordinator (PL-15). F-09 is a wording defect whatever the frame (PL-05). F-15 is not a bug (PL-10). |

**Counts:** 42 items: 40 accepted, 1 accepted in part (A-42), 1 plausible (A-35), 0 rejected. Of the accepted, A-2, A-8, A-10, A-14, A-23 and A-27 are narrowed or extended. Seven are new findings, six of them confirmed: A-33, A-34, A-36, A-37, A-38 and A-39.
