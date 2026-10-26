# Analysis — M6.P2 T18, EmulationStation's cloud pages, cards and text (#665)

The lane's grades of `02`'s F-01 to F-19, before the seats. § Second opinion is written after them, with each seat's items graded.

## Executive summary

The four pairs do what the rules ask of them, and the hard parts hold:

- one parser for two readers;
- a stop as a request the run keeps;
- the stamp before the card;
- the posted step that cannot reach a deleted page.

221 unit cases pass on a host with no `cmake`.

What does not hold falls in three families:

- **The protocol under a pipe:**
  - the card's wrapper lacks the trap the job's has (F-02);
  - both readers take a pid from any line (F-01, latent);
  - an unknown marker vanishes silently (F-03).
- **Lifetimes and threads:**
  - the stamp writer renames a write it never checked (F-06);
  - the launch's stop spins on the interface thread (F-07).
- **The words:**
  - the CANCEL dialog over a match promises a recovery the backend refuses (F-08);
  - two script sentences have no translation, and one of them reaches a page (F-11);
  - two paraphrase verbs show on the small panel (F-09);
  - the comments, and the rule's half, describe older code (F-13, F-14).

The futro predicted two streams, the header comment and the why table's missing rows. Both are here, as F-13 and F-11. The rest is renovation:

- the retired folder move's leftovers (F-16);
- a dead function (F-17);
- exit 75's eight wordings (F-15);
- the test that is said to guard the why table and does not (F-12);
- the two readers' seam (F-18).

**Proposed for stage D, after the seats:** seven bugs, all Low: the lane's four (§ Q3); PL-18 (Astra's A-33 and A-34, Argon's R-11 and R-39); PL-20 (A-37); PL-22 (Argon's R-42). Two more are proposed Low by the seats (PL-05, PL-15). The rest are renovation, design or notes routed elsewhere (`05`). The coordinator disposes.

## Acceptance-criteria scorecard

#665's 19 checkboxes, at stage C (the coordinator ticks at acceptance):

| # | Checkbox (short) | State at stage C | Artifact |
| ---: | --- | --- | --- |
| 1 | `00` to `05` exist | `00` to `04` exist; `05` at stage D | the folder |
| 2 | the lint `PASS` | `--phase pre-issue` at stage C's end | `00` § Stage C |
| 3 | `review-plan.json`, provenance, manifest | at stage C | `second-opinions/` |
| 4 | the punch-list issue at its outcomes | stage D onward | the audit issue |
| 5 | `reviewed-at`, `fixed-at`, `fixed-at-es`; nothing under `packages/projects/tools` | `reviewed-at` `cbf6d7ef83` with the pin; r25 empty | `00`, r25 |
| 6 | `01` § Scope | done | `01` |
| 7 | the coverage table, 30 | done (the `awk` prints 30) | `02` § Coverage |
| 8 | § The protocol generated | done; exits 1 on drift (P8) | `tools/t18-protocol-table.py` |
| 9 | § The why table generated | done; exits 1 on drift (P9) | `tools/t18-why-table.py` |
| 10 | § The lifetimes | done, 13 rows | `02` |
| 11 | § The strings | done, except the fit at 640x480 (owed to the window) | `02` |
| 12 | § The tests | done: 221 PASS, 22 rows | `02`, r20 |
| 13 | § The runs | done, 26 rows | `02` |
| 14 | § The guest cycle | `CANNOT` until the window | `02` |
| 15 | `00`'s never-run record | held so far | `00` |
| 16 | `04` § Q3 with trace, `Already written:`, VM line, `proved:` | below | this file |
| 17 | every proof `proved:`; every punch item `question:`; every bug through `box-check` | 16 proofs; the rest at stage D | `02`, `05` |
| 18 | the retro | stage G | -- |
| 19 | the five checkers and the ES `pre-push-test` | at the hand-back | -- |

## Risk assessment

- **The highest risk to a player is F-06**, and it is small. A stamp truncated by a full `/storage` reads as NOT DONE ON THIS DEVICE YET until the next run rewrites it. No save is lost, and the next sync completes.
- **The highest risk to trust is F-08.** A player who cancels a match is told that the next backup or restore finishes it. The next match is refused until they check again (PL-001). The page's own footer then names the row to start from (`CloudText::matchRecovery`), so the dialog and the page disagree in one minute.
- **The highest risk to the code's future is F-12 with F-03.** A new `>>> why` or a new marker can land in a script, and every test still passes. A new why shows in English; a new marker vanishes. The generator here is the check the comment describes, and it lives in the distribution repository, not the ES one.

## Coverage boundary

- **Read whole:** the eight sources and `CloudTextTests.cpp`. The other 21 test files were read for subject, fixtures and the eight's functions.
- **Read as context:**
  - `tests/app-unit/` (19 files) and the eight harnesses;
  - the callers' lines where they decide what reaches the eight;
  - `FileSystemUtil.cpp`'s writer and `AtomicFileUtil.h`;
  - the scripts at `8ebaf8daad`, through the two generators.
- **Not run:**
  - `tests/app-unit`'s `app-unit-tests`, `proxycards-tests` and `bookkeeper-tests`, outside the brief's compiler scope. `jobs-tests` ran on the coordinator's yes: 6 cases PASS (F-19);
  - the harnesses, whose subjects are T26's;
  - `tools/es-syntax-check` (no toolchain; r21).
- **Owed to the window:**
  - the identification of the binary;
  - every fit at 640x480;
  - F-08's and F-09's frames;
  - the card during a sync and the page's live line;
  - `time-to-play --vm`;
  - F-02 on the real path, if the window allows (stop the interface under a sync, read the stamps).
- **Not this slice's:**
  - `GuiMenu.cpp`'s composition and its `exists()` reads (T26);
  - `FileData.cpp`'s launch gate (T2);
  - the scripts' bodies (T16, T17);
  - `cloud_content_transfer`'s TERM trap (T17's file; the lead in `02`).

## Second opinion

### The packet and the plan

- **The packet:** `second-opinions/packet.md`, 347,592 bytes, sha256 `e92cc4dc234409ac4efb375f318e7e15acbb6e8a30784c67c20cb13c640a246e`, built by `stage-c/packet.py`. Trimmed under D-WORKFLOW-195: 364 KB at the first build, 337 KB with the headers as excerpts and the register rows narrowed, 348 KB with the window's results in `02`.
- **Its contents:** the ask; `02`, `03` and `04` whole; three context sections; the job, the card and the page whole and line-numbered; the headers, `CloudText.{h,cpp}`, `CloudTextTests.cpp` and the callers' cited lines as excerpts.
- **The three-way scan** (`manifest.json`):
  - `forbidden-terms-check` 0 hits in 37 sections;
  - `SECRET_PATTERNS` 0 lines, proven to fire on a fake line built at run time;
  - 0 lines masked;
  - 194 credential-word hits, each classed. Seven were read by shape and dispositioned by name: an outcome token compared with a word (five lines), a `bool` initialised `false`, and a quotation of T2's "Not a pass:". **No value.**
- **The plan:** `second-opinions/review-plan.json`, written at 10:26Z before the first call.
- **The calls:** exactly four keyed invokes, `--max-retries 1 --per-attempt-timeout-ms 1800000 --total-timeout-ms 2400000`.
- **Argon's brief** is the packet with `{PREFIX}` as R plus the grades below: 357,825 bytes, sha256 `bd9d95799a6fc14d89a8531b8a06c701ba4ae27a40d6787b17a9dbd853b42fb3`.

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

### Gemini 4 Argon (`gemini-argon`, `google/gemini-4-argon`, `high`): 45 items, graded

**The calls:**

- Call 3, the probe: 10:49:58 to 10:50:05 UTC, PASS.
- Call 4, the refutation: 10:50:15 to 11:06:02 UTC, 36,980 bytes. **Its first attempt returned empty content** (`finish=error`, `retry(empty_content)`, after 396 s). The invoke's one allowed retry succeeded, `finish=stop`, still within the one keyed call.
- Both were served `google/gemini-4-argon` by Google (`stage-c/provenance-read.txt`).
- Argon's brief was the packet with `{PREFIX}` as R, plus the grades of Astra (357,825 bytes).

Each item was re-read at its lines before it was graded (`stage-c/rereads/`), in the same words as Astra's table.

| Item | Grade | The lane's re-read, and where it lands |
| --- | --- | --- |
| R-1 | accepted, narrowed | `case Doing:` does not clear `mCurrent`, `mChecksTotal` or `mListed`, which outrank `mDoing` on row 3 (`GuiCloudTransfer.cpp:946-1035`). A `doing` after rclone ran within the same unit shows stale rclone state; every producer at `8ebaf8daad` announces its `doing` after a fresh `>>> unit`, so it is latent. The empty `>>> why ` becomes `Unknown` after `cleanLine`'s trim, but both readers ignore an empty why anyway (`CloudTransferJob.cpp:284`), so it changes nothing: `:284` is unreachable. PL-13. |
| R-2 | accepted | As A-1. |
| R-3 | accepted | As A-3. |
| R-4 | accepted, extended | A second `>>> pid` that is junk or `0` overwrites a good pid with 0 and disarms a later stop (`CloudTransferJob.cpp:157`, `ThreadedCloudSync.cpp:816`). It is latent, since only the wrappers print the line (P14). PL-13. |
| R-5 | accepted, narrowed | The 1,024 cap drops characters and can hide a glued `Transferred:`. On A-35 the seat says "more than merely plausible": the code's own comment (`:645-647`) says the block ends without a newline, but says nothing of rclone's last block at exit. The grade stays plausible until the fixture (PL-19). |
| R-6 | accepted | `atol` in the count line can double-count a unit's files after a torn line (`CloudTransferJob.cpp:425-428`). Latent. PL-13. |
| R-7 | accepted | As A-7: `lock` and `job` dangle across `:328-343`, unused. No use after free. |
| R-8 | accepted, narrowed | Four parts. (1) and (3) are A-33 and A-34. (2): after `mInstance` is cleared (`:716-720`) a launch is allowed during the linger, and then `CloudOffer::present` (`:741`, completed runs only) and `ProxyCards::afterSync` (`:754-755`) run over a game that has started. `afterSync` (`ProxyCards.cpp:543-551`) has no running-game guard; whether `batch()` defers is the offline achievements slice's. (4): `mPid`, `mWaitingForNetwork` and `mCancelled` are `std::atomic` (`ThreadedCloudSync.h:149-151`, in the lane's read). The cached-pid SIGKILL is A-8. Mostly accepted; "refuted" is too strong for a design that holds where it is atomic. PL-18. |
| R-9 | accepted, extended | A stale `<stamp>.tmp` left by an earlier failed write is renamed over the stamp when the next `fopen` fails, a case the lane did not name. PL-01. |
| R-10 | accepted | As A-11, citing D-CLOUD-109 and D-CLOUD-129's visible wait. PL-15. |
| R-11 | accepted, **new** | The job's own window: `pclose` (`CloudTransferJob.cpp:679`) reaps before the lock at `:684`. A stop in that window marks a run that **failed** on its own (5, 69, 75) as stopped, because `:691` clears the stop flags only on 0 or 9, and the real outcome becomes `SKIPPED - YOU CANCELLED IT`. "Refuted" is right about the lane's "every race closed": the named races are closed and this one is not. PL-18. |
| R-12 | accepted | As A-13 and A-16. The 48-character scan candidate that fits beside the 36- and 43-character `NOTHING NEW` forms is an inference about one font, not a frame. PL-05 stays as written. |
| R-13 | accepted | As A-12. |
| R-14 | accepted | As A-14. |
| R-15 | accepted | As A-15. The sentinels `whyForCode` handles (69, 75, NoFolder) are in § The protocol's exit rows, not the fallback map's comparison. |
| R-16 | accepted, narrowed | The emitter table omits three rows that no test reaches through the protocol: `CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.`, `YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED` and `YOUR CLOUD FOLDER COULDN'T BE READ` (`git grep -c` in `CloudTextTests.cpp`: 0 each). `YOU WENT OFFLINE PART-WAY THROUGH` is a stamp's why and has its own case (`:747`; 12 mentions). That is why A-36 passed the tests. PL-03. |
| R-17 | accepted | As A-17, with the omitted rows of R-16. |
| R-18 | accepted | The untested list grows: the page formatter's torn fields and its four-byte separator check, the unfitted rows, normalization round-trips, a glued `>>> `, and the card's three races. PL-14. |
| R-19 | accepted | As A-2 and R-4. |
| R-20 | accepted | As A-29. |
| R-21 | accepted | As A-1. |
| R-22 | accepted | As A-4. |
| R-23 | accepted | As A-18. |
| R-24 | accepted | As A-30, with R-9's stale temporary. |
| R-25 | accepted | As A-11 and A-42. |
| R-26 | accepted | As A-31: the preview's plan is spent too, so the next match must check again. |
| R-27 | accepted | As A-13. |
| R-28 | accepted | F-10 confirmed. |
| R-29 | accepted | As A-32 and A-36. |
| R-30 | accepted | F-12, with R-16's rows. |
| R-31 | accepted, narrowed | `ThreadedCloudSync.h:158-159` and `shortenWhy`'s body (`CloudText.cpp:371-386`) are in the lane's read: both hold. |
| R-32 | accepted | F-14, with codes 6 and 10. |
| R-33 | accepted | As A-16. |
| R-34 | accepted | F-16; the census is P13 and P14. |
| R-35 | accepted | As A-27; `nextTime` is P12. |
| R-36 | accepted | As A-28. |
| R-37 | accepted | F-19; `jobs-tests` ran here (6 PASS). |
| R-38 | accepted | F-20 confirmed at its lines. |
| R-39 | accepted | The details of R-8: (1) is A-33's window and the SIGTERM to a reaped group; (2) is the linger's launch and `afterSync`. PL-18. |
| R-40 | accepted, **new**, latent | Both readers decide COMPLETED from the last code (`ThreadedCloudSync.cpp:494`, `GuiCloudTransfer.cpp:435`) without asking whether a tier failed. The card's `badTiers` drops each tier's code (`:482-483`), so a failed tier with no why gets the last command's phrase. The composers propagate a failure unless a 9 follows it: `main.cpp`'s startup composer exits the restore's code first (`[ "$_r" != 0 ] && exit "$_r"`), so a restore's 9 hides the backup's failure. Latent with A-38 (no script passes `--error-on-no-transfer`). PL-21. |
| R-41 | accepted | As R-11. PL-18. |
| R-42 | accepted, **new**, confirmed | `cloud_content_backup` and `cloud_content_restore` exit 69 after progress with only a stamp and no `>>> why` (`:336-342`, `:391-397` at `8ebaf8daad`). The page reads COULDN'T FINISH (progress), but `run()` leaves 69 out of its fallback (`CloudTransferJob.cpp:721`) and never reads `offlinePartWayWhy` as the card does (`ThreadedCloudSync.cpp:509-511`). So line 4 is blank under COULDN'T FINISH: no why, against D-UI-028. `cloud_content_restore:372` says "the page reads a 69 after progress the same way"; it does not. PL-22. |
| R-43 | accepted, **new**, confirmed | `CloudTransferJob::mWhy` is written (`:286`) and never read (`git grep -w mWhy` in the job and the page: one write, one declaration), against its comments (`:244`, `.h:173`). The no-tier fallback copies pending whys without the tier arm's de-duplication and drops them when an earlier tier failed. Every composer echoes a tier after each part, so the second half is latent. PL-23. |
| R-44 | accepted | As R-16. |
| R-45 | accepted, narrowed | It confirms A-33 to A-42. On A-41 and A-42, which are about the first reader's own claims, the seat agrees. A-39: of `backuptool`'s rows (`CloudText.cpp:437`, `:448-453`, `:461-465`), those printed only by `backup` are unreachable from the backup chain. PL-17. |

**Counts:** 45 items, all accepted, 0 rejected. Of these, R-1, R-4, R-5, R-8, R-9, R-12, R-16, R-31 and R-45 are narrowed or extended. Five are new to the lane: R-1's stale row and R-4's pid zero (both latent), and R-11/R-41, R-42 and R-43, which are confirmed. R-8 and R-39 add the linger's launch to A-33. One grade stays with the lane: A-35/R-5 remains plausible until its fixture.

## Finding Verification

Each of `02`'s findings, re-read at the pin before it was graded; the re-read is the evidence named:

| F | Re-read | Verdict |
| --- | --- | --- |
| F-01 | both `case Pid:` arms assign without a guard; `git grep '>>> pid'` at `8ebaf8daad` finds no script line (P14's method) | CONFIRMED, latent |
| F-02 | r09; `cloud_backup:2504` traps INT and TERM, not PIPE | CONFIRMED |
| F-03 | both `default:` arms; no `LOG` in either | CONFIRMED |
| F-04 | `char line[512]; fgets(line, sizeof(line), pipe)` | CONFIRMED, latent (no line that long is known) |
| F-05 | no case names `CloudTransferJob`; the per-file split and the run loop are in `CloudTransferJob.cpp` | CONFIRMED |
| F-06 | P16 | CONFIRMED |
| F-07 | P15 | CONFIRMED |
| F-08 | `askCancel`'s third arm covers every kind but Scan and Create; `transferKind` returns Match for `--match` | CONFIRMED (a frame owed) |
| F-09 | `:805-808`; the short form when `sizeText(summary).x() > mLineWidth` | CONFIRMED in the code; whether 640x480 shows it is a frame |
| F-10 | `:745`, `:769` | CONFIRMED |
| F-11 | P10; `GuiMenu.cpp:5043-5045` keeps `backuptool restore`'s output | CONFIRMED |
| F-12 | the comment against the test | CONFIRMED |
| F-13 | each line read | CONFIRMED |
| F-14 | the rule's **Why** paragraph | CONFIRMED (#909's) |
| F-15 | the generator's table | CONFIRMED |
| F-16 | P13, P14 | CONFIRMED |
| F-17 | P12 | CONFIRMED |
| F-18 | § The protocol | design |
| F-19 | `jobs-tests` built and run on the coordinator's yes: 6 PASS | CONFIRMED, and covered |
| F-20 | the 640x480 frame `match-dialog/04-match-done.png`; `CloudTransferJob.cpp:343-349` | CONFIRMED (pin-binary) |

## Renovation face

### Q1 Modernize

- **The two readers' seam** (F-18). A shared reader would take the wrapper, the read loop and the pid once, and hand each kind to the surface. The job and the card would keep only what each does with a kind.
  - The smallest step is the wrapper: one function that builds `setsid sh -c 'echo ">>> pid $$"; { trap '' PIPE; CMD ; }' 2>&1` for both, which closes F-02.
  - The next is the read loop: the job's character loop with its glued-mark split, for both, which closes F-04.
  - A proposal for the coordinator, not a stream.
- **The stamp writer onto `Utils::AtomicFile::writeText`** (F-06). The writer exists, is tested here (`AtomicFileTests.cpp`), and is already used by `Settings.cpp` and `GuiMenu.cpp:5066`. The fix is the call, not a design.
- **The launch's two waits** (F-07): the card's spin and the job's `launchWhenGone`. One shape for both is the caller's change (T2's `FileData.cpp`), routed there.
- **`CloudText.cpp` by subject.** The offline proxy's stamps and the settings archive's name could be their own text files beside their tests. A proposal, low value now.

### Q2 Standards

The checklist (`03` § 3.2): the four tiers, the confirmation shape, the help bar, the three type sizes (the page uses the theme's three: title, text, small), `exists()` 0, French for every fork string, `CMakeLists.txt` failing closed, and no secret-shaped literal at rest, all held. Where it does not:

- **F-12:** a comment claims a test guards the why table; the test reads no script. The rule's fix is to say what does guard it (the generator), or to make the guard real: a check in the distribution repository, where the scripts are.
- **F-05:** the `%3d` separator and the job's glued splitter, two of the four piped-progress traps, have no unit case. Both parsers live in `CloudTransferJob.cpp` and are not pure; moving the per-file split into `CloudText` would let the existing binary test it (Q1).
- **F-19:** the job's lifetimes are tested by `jobs-tests`, which no standing command builds; it ran here on the coordinator's yes and passed (6 cases, ASan and UBSan). A standing place for `tests/app-unit` in a suite (`tools/vm-qa`'s `lifetime` builds part of it) is the proposal.

### Q3 Bugs

**Four proposed `bug`s, all Low.** Each carries its trace, its `Already written:` line, its VM line, and the `proved:` its fix would need. The rest of Q3 is renovation. F-20 (`SNES 0 FILES`) was found in the window, after the first draft of this list.

**Family (a), the protocol under a pipe.**

- **B1 (F-02): the card's scripts die of SIGPIPE when the interface goes, before they stamp.**
  - *Trace.* `ThreadedCloudSync.cpp:206-207` wraps the command as `setsid sh -c 'echo ">>> pid $$"; CMD' 2>&1`; the job's (`CloudTransferJob.cpp:636-637`) adds `{ trap '' PIPE; ... ; }`. Its comment says why: "a part that can still end writes its stamp". With the interface gone, the card's pipe has no reader, so the scripts' next `echo` (a `>>> why`, a `log_message` to stdout) kills them. `cloud_backup`'s trap (`:2504`) is INT and TERM, not PIPE, so no stamp is written. The rows then read the run before it.
  - *Already written:* nothing inherited. The missing stamp is an absence, and the next run's stamp replaces the last one as always; nothing on a device or in a cloud needs reading or migrating.
  - *VM line:* yes. Stop `essway` under a startup or exit sync on the guest, then read `/storage/.cache/cloud_sync/last-backup` and `last-restore` against the before-snapshot. A host fixture can show the same with the two wrapper strings from the source and a pipe closed early.
  - *Proof a fix needs:* `fixture` before and after on the host (the wrapper strings run under `sh` with a reader that closes), and `fix-walk-pending-image` for the guest.
- F-01, F-03 and F-04 are latent or silent, not defects with a failure today: renovation (Q1, Q7).

**Family (b), lifetimes and threads.**

- **B2 (F-06): a short write is renamed over the good stamp.**
  - *Trace.* `ThreadedCloudSync::writeStamp` (`:930-949`) writes `path + ".tmp"` with `Utils::FileSystem::writeAllText`. That is `void` (`FileSystemUtil.cpp:1429-1446`): it returns early on a failed `fopen` and never checks `fwrite` or `fclose`. `writeStamp` then calls `std::rename(tmp, path)`. On a full `/storage`, the rename replaces a whole stamp with an empty or cut one. `CloudText::parseLastRun` reads that as `ran = false`, and the row says NOT DONE ON THIS DEVICE YET. The comment above the writer (`:878-881`) promises "written whole or not at all".
  - *Already written:* stamps written by the old writer are whole, or truncated where a disk was full. The reader already treats a truncated one as never run. The fix writes new stamps whole through `Utils::AtomicFile::writeText`, and the next run rewrites any cut one; nothing to migrate.
  - *VM line:* yes, on the host. A case that links `writeStamp`'s logic with `AtomicFileUtil` under `ulimit -f 0` (SIGXFSZ ignored, T17's S5 stand-in for a full card) shows the old stamp survive. On the guest, a loop device filled to the byte.
  - *Proof a fix needs:* `fix-unit-test`. `writeStamp` is in the card's file, which links a `Window`, so the case needs the function moved beside `CloudText` or a stand-in like `jobs-tests`' doubles. That is stage D's question.
- **F-07** (the 2 s spin on the interface thread) is a design question about the caller: renovation, routed to T2's owner.

**Family (c), the words.**

- **B3 (F-08): the CANCEL dialog over a match promises a recovery the backend refuses.**
  - *Trace.* `askCancel` (`GuiCloudTransfer.cpp:351-361`) branches on `transferKind` for Scan and Create only. A match (`TransferKind::Match`, `--match`) gets `CANCEL THIS BACKUP OR RESTORE?` and `WHAT'S ALREADY IN PLACE STAYS. THE NEXT BACKUP OR RESTORE FINISHES WHAT THIS ONE DIDN'T.` A match is neither, and its next apply is refused with SOMETHING CHANGED SINCE YOU CHECKED (PL-001, `:363-367`). The page's own done footer names the row to check again (`CloudText::matchRecovery`). This is es-native-ui.md's anti-pattern: dialog text promising behaviour the backend does not do.
  - *Already written:* nothing inherited. It is a dialog; nothing is stamped or saved.
  - *VM line:* yes in principle: a match page against the QA WebDAV with a planned removal, back pressed while it runs. In T18's window it was `CANNOT`, because a match on the fixture ends at ELAPSED 0:00, before a press lands (`02` § The guest cycle). A before-frame needs a fixture large enough to keep a match running for a second or more. The binary carries the dialog's string (`identity.out`: 1 hit).
  - *Proof a fix needs:* `fix-walk-pending-image`. A fourth arm for Match, in words for the maintainer, with French; `docs/es-menu-map.md` § Cloud updated in the same change (D-UI-039).
- **B4 (F-11): two script sentences have no row, and one reaches a page in English.**
  - *Trace.* § The why table: `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` (`backuptool:1495`) and `ANOTHER CLOUD SYNC IS RUNNING` (`cloud_setup:797`) have no `whySentences` row.
    - The first reaches the settings restore page's line 4: the chain keeps `backuptool restore`'s output (`GuiMenu.cpp:5043-5045`), and `localizedWhy` passes an unlisted sentence through as it came. It shows in English under a French `COULDN'T FINISH`.
    - The second ends the CREATE page skipped, where line 4 is not drawn.
    - The test the comment names (F-12) cannot catch either.
  - *Already written:* nothing inherited by the interface. The scripts' stamps keep their English by design, and their readers translate.
  - *VM line:* yes. The first on the guest by a settings archive carrying a member type the restore refuses (T17's fixture shape), the page's line 4 read back in French. The second has no screen to show.
  - *Proof a fix needs:* `fix-unit-test`. A `localizedWhy` case for each pair, failing before the pairs are added, plus the French rows, and the generator re-run to 0 script-only.
- **F-09** (`BRING DOWN` / `SEND UP`) is decided at the frame. If the 640x480 frame shows the short form, it is a words `bug` under player-language.md's "the canonical verb, never a paraphrase"; if the long form fits, it is renovation. The window's before-frame is the deciding evidence.
- **F-20** (the match's done page names `SNES 0 FILES`) is framed at 640x480 (`match-dialog/04-match-done.png`). A system nothing was removed from is listed beside the one that lost a file, because `CloudTransferJob.cpp:343-349` keeps every item of `>>> removed`. A words nit: renovation, unless the coordinator calls it least surprise's.
- **F-10** (`DID NOT`, `CAME DOWN`), **F-13** (the comments), **F-14** (the rule's half, #909) and **F-15** (eight wordings) are renovation.

### Q4 Package currency

- **The pin is level with ROCKNIX's master:** merge base `bccd715707` = `upstream/master`, 725 ahead, 0 behind (r04).
- **M7's work on these files beyond the pin:** none. None of the 21 `m7` refs in the ES repository carries a commit on the 30 that the pin lacks (`03` § 3.5).
- **T17's streams on the scripts these readers read:**
  - S5 (#1132) makes `--set-systems` exit 1 on a failed write; the page reads that as `COULDN'T FINISH - SOMETHING WENT WRONG` unless the script says why. Its why is a stream question for T17's branch.
  - S6 (#1133) is the pair of sentences routed to this slice; F-11 is its landing place.
- **`tools/es-syntax-check`'s default root names the legacy M7 layout** (#640). r21 sets `ES_BUILD_ROOT=/nonexistent` as the brief requires, and the tool stops at the root first, never reaching its `ninja` check.

### Q5 Efficiency

- **The two time-to-play numbers.**
  - The latest in `docs/vm-qa-log.md` that carries both: 2026-09-27, `c9f5aa7de0` (x64 run 80): 0.58 s from the interface to a first frame, 1.01 s game to game.
  - T2's run on the window's image (`/workspace/artifacts/m6-t2-20261023/ttp-q5.log`, 2026-10-23): game to game 1.01 s median of 3; the STOP IT AND PLAY answer at 1.35 s; the exit sync's stamp 0.54 s; the card gone at 6.01 s. It is marked "Not a pass": no cloud was up, so the exit sync did nothing.
  - The window, with the QA WebDAV up, measures the real exit sync.
- **The 2 s budget:** a cancellation's wait, not the exit sync's completion that D-CLOUD-119's 3 s bounds, so the two are not comparable (Astra's A-11 corrected the first wording). The window measured the question answered at 1.34 s median before the next game's first frame. The spin runs on the interface thread (F-07), so no frame is drawn while it spins: at 1.5 s the player sees the frame the dialog left.
- **The lingers:** 1.5 s on a completed run with nothing to act on, and 5 s otherwise (`ThreadedCloudSync.cpp:731`). T2's 6.01 s "card gone" is the 5 s linger after a run with an outcome to read, plus the fade.
- **The 20 ms spin** costs nothing measurable beyond holding the interface thread.

### Q6 Dead ends

Removals none: each is a proposal on the punch list for the coordinator.

- **F-16, what the retired folder move (#353) and folder step (#363) left:**
  - the `doing` words `copy`, `verify` and `remove` (`CloudTransferJob.cpp:387-389`) and their strings (`GuiCloudTransfer.cpp:1027-1032`);
  - the `DISCARDED SAVES` unit label (`CloudText.cpp:1108`);
  - the why row `YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED` (`:429`);
  - `setFailedNote` and `setDismissedAction`, which have no caller, and `setCompletedAction`'s `cancellable` parameter, never passed;
  - the comments that name them (`GuiCloudTransfer.h:76-100`, `CloudTransferJob.cpp:235-236`, `CloudText.cpp:1104-1105`).
- **F-17:** `CloudText::nextTime` has no product caller. `isKnownWhy` and `isKnownUnitLabel` are test-only, which is their job: oracles.
- **Markers parsed and never produced:** none beyond F-16's three `doing` words. `>>> tier` is ES's own composition, and `>>> offer` is read by both.
- **Test cases whose subject is gone:** none found at the function level. At the feature level it is unproved, as Astra's A-41 says: a case may test a live function of a retired flow, such as the unit labels PL-11 names.

### Q7 Clarity and structure

Can a reader tell, from the four pairs and the rules, which surface shows a sync and which a transfer, which words each may use, what each parses, and how each ends?

- **Yes, from the code and § The protocol.**
- **Less so from the comments** (F-13): the fallback map's comment names other words and sits above another function, and five comments still say "four words".
- **Less so from the rule** (F-14, #909's half).
- **Exit 75 reads eight ways** (F-15): the card's two, the page's scan word, `backuptool`'s, `cloud_setup`'s, `cloud_scan`'s, and the folder refusal's.

The two generated tables are the test this question asks for, and they pass with the findings named.

## Instruction File Recommendations

### Coverage gaps (would have prevented)

- **A comment that claims a test guards something names the test's mechanism, and the mechanism is read before the claim is repeated** (F-12). engineering-practices.md § A name is not a behaviour covers the reading; nothing asks the writer of the comment to check it. A proposal for es-code-traps.md § Pure text has a home: "a table a test holds is checked against its source by something that reads the source; a typed table is a second copy".
- **A reversal sweeps code as well as words** (F-16). decision-register.md's P-01 paragraph says "code comments, the docs, the menu map"; D-CLOUD-175's retirement left setters, words and strings. A proposal: the same paragraph names "the hooks, setters and protocol words the reversed flow used", with `tools/archaeology --reversal` run over the ES checkout too. The tool already reads it.

### Codification gaps (proposals for the coordinator)

- `tools/t18-why-table.py` as a standing check in `tools/vm-qa`'s `french` suite (the scripts' whys against the interface's rows), so a new script sentence fails a suite rather than a player's screen.
- The two wrappers in one function (Q1), and a rule line in es-code-traps.md: "a command the interface reads through a pipe ignores SIGPIPE inside its wrapper, so it outlives the reader long enough to stamp".

## Quality self-check

- Every F has a re-read and a verdict; every proof has a `proved:` cell; the counts match (16 and 16).
- The two generated tables exit 1 on a drifted tree.
- What I did not check:
  - every fit at 640x480, the binary on the image and F-08/F-09's frames are the window's;
  - `cloud_content_transfer`'s TERM trap was not followed into its caller.
