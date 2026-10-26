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

- Numbered items `R-1`, `R-2`, ..., grouped under the six headings above.
- Each item gets one line saying *confirmed / narrowed / refuted / new*, then the `file:line` evidence, then two to five sentences.
- Do not restate the packet, and do not reproduce long code.
- Keep the whole reply under about 8,000 words.


## The first reader's 02-forward-audit.md (whole)

# Forward audit — M6.P2 T18, EmulationStation's cloud pages, cards and text (#665)

Read at the pin `16dbac5211eea7e70db7394372033be2be7df829` (the ES worktree, clean), with the scripts at the distribution's `8ebaf8daad`. The lane's tip `cbf6d7ef83` is `reviewed-at`. The lens is brittleness and new functionality (brief § 4).

Each finding is `F-nn` here and graded in `04`. Each proof is `P-nn` with its `proved:` cell, numbered as in `00`.

## Coverage

One row per path of the 30 (brief § 2's block; `01` § Scope). "Read" is whole unless it says otherwise.

| Path | Lines | What it is | Read | Findings | proved |
| --- | ---: | --- | --- | --- | --- |
| `es-app/src/CloudText.h` | 589 | the pure text's contract: 47 declarations, the outcome enum, the protocol kinds | whole | F-13 (`:9-18`, `:78-82`, `:164-170`), F-17 | tree |
| `es-app/src/CloudText.cpp` | 1,409 | the pure code: stamps, protocol, whys, units, sizes, live lines, scan stamps, folder refusals | whole | F-01, F-03, F-11, F-12, F-13 (`:298`), F-15, F-16 (`:1104-1108`, `:429`), F-17 | tree, unit-test |
| `es-app/src/CloudTransferJob.h` | 217 | the transfer's run, apart from the page | whole | F-18 | tree |
| `es-app/src/CloudTransferJob.cpp` | 751 | the run's thread, the wrapper, `handleLine`, the stops | whole | F-01, F-03, F-05, F-13 (`:399-403`), F-16 (`:235-236`, `:387-389`), F-18 | tree |
| `es-app/src/ThreadedCloudSync.h` | 201 | the card's contract, `cancelForLaunch`, the fallback map's declarations | whole | F-13 (`:70`, `:93-99`, `:126-130`, `:158-159`) | tree |
| `es-app/src/ThreadedCloudSync.cpp` | 949 | the card: the wrapper, the reader, the outcome, the stamps, the launch cancel | whole | F-01, F-02, F-03, F-04, F-06, F-07, F-13 (`:73`, `:460`), F-15, F-18 | tree |
| `es-app/src/guis/GuiCloudTransfer.h` | 236 | the page's contract | whole | F-13 (`:156-157`), F-16 (`:76-78`, `:90-100`) | tree |
| `es-app/src/guis/GuiCloudTransfer.cpp` | 1,077 | the page: layout, input, CANCEL, outcome, the seven rows | whole | F-08, F-09, F-10, F-16 (`:1027-1032`) | tree |
| `es-app/tests/unit/AtomicFileTests.cpp` | 1,090 | `Utils::AtomicFile`; the card's detached thread read from source (`:792`) | whole | F-06 (the writer the stamps do not use) | unit-test |
| `es-app/tests/unit/AtomicFileWin32Tests.cpp` | 80 | the `_WIN32` branch of the same writer | whole | -- | unit-test |
| `es-app/tests/unit/CMakeLists.txt` | 159 | the four binaries; fails closed without rapidjson (`:72-74`) | whole | -- (positive) | unit-test |
| `es-app/tests/unit/CaptureRotationTextTests.cpp` | 164 | rotation record and launch log | whole | -- | unit-test |
| `es-app/tests/unit/CheevosIndexTests.cpp` | 62 | what the game index owes a game | whole | -- | unit-test |
| `es-app/tests/unit/CheevosRetryTests.cpp` | 112 | the sign-in retry schedule | whole | -- | unit-test |
| `es-app/tests/unit/CloudFolderValidationTests.cpp` | 84 | the folder checks' JSON | whole | -- | unit-test |
| `es-app/tests/unit/CloudTextTests.cpp` | 1,784 | 70 cases over `CloudText`; the emitter table (`:632-721`) | whole | F-05, F-12 | unit-test |
| `es-app/tests/unit/CommandLineTests.cpp` | 53 | the launch option swap | whole | -- | unit-test |
| `es-app/tests/unit/DisplayAspectTextTests.cpp` | 54 | a screenshot's game | whole | -- | unit-test |
| `es-app/tests/unit/LaunchCommandTests.cpp` | 103 | what a launch command launched | whole | -- | unit-test |
| `es-app/tests/unit/LogPolicyTests.cpp` | 50 | the log's levels | whole | -- | unit-test |
| `es-app/tests/unit/MaskSecretsTests.cpp` | 242 | the credential mask; fixtures built at run time (0 hits, § The tests) | whole | -- (positive) | unit-test |
| `es-app/tests/unit/OfflineAchievementsTextTests.cpp` | 350 | the proxy's JSON | whole | -- | unit-test |
| `es-app/tests/unit/OfflineProxyUrlTests.cpp` | 65 | the proxy's address | whole | -- | unit-test |
| `es-app/tests/unit/README.md` | 77 | how the tests build; the list of record | read as context (the block's unread file) | -- | tree |
| `es-app/tests/unit/SaveStateJobQueueTests.cpp` | 170 | the save state job queue | whole | -- | unit-test |
| `es-app/tests/unit/SystemConfTests.cpp` | 506 | `system.cfg`'s load, save and record | whole | -- | unit-test |
| `es-app/tests/unit/TabStopsTests.cpp` | 50 | tabbed columns | whole | -- | unit-test |
| `es-app/tests/unit/TimeTextTests.cpp` | 149 | the time beside a save | whole | -- | unit-test |
| `es-app/tests/unit/WifiTextTests.cpp` | 352 | the Wi-Fi rows' reading of `wifictl` | whole | -- | unit-test |
| `es-app/tests/unit/fakes/SDL_timer.h` | 8 | `SDL_GetTicks` for `es-conf-tests` | whole | -- | unit-test |

The eight sources were read line by line. The 22 test files were read for their subjects, their fixtures and the functions of the eight that they name; `CloudTextTests.cpp` was read against every function it calls. The 14 test files whose subject is not cloud text are graded only on the standards a test file owes (Q2: fails closed, no secret-shaped literal, builds and passes); their subjects belong to other slices.

## Context read

| File (at the pin) | Lines | What it tests of this slice | Ran here |
| --- | ---: | --- | --- |
| `tests/app-unit/CMakeLists.txt` | 106 | builds four binaries; `jobs-tests` copies the **shipped** `CloudTransferJob.cpp` (`:69`) with `CloudText.cpp` (`:76`) | `jobs-tests` only, on the coordinator's 10:02 yes: 6 cases PASS (§ The tests); the other three not run |
| `tests/app-unit/JobsTests.cpp` | 232 | the job: a stop before the pid line (`:130`, `:135`), a completed run not called stopped (`:144`), the look-then-mark race through `testPauseInStop` (`:163`), the restamp against the before-snapshot (`:183`); doubles the card's statics (`:63-78`) | yes: 6 cases, 28 assertions PASS under ASan and UBSan |
| `tests/app-unit/ProxyCardsTests.cpp` | 599 | the card's caller `ProxyCards` against `fakes/ThreadedCloudSync.h` | no |
| `tests/app-unit/AppWindowTests.cpp` | 46 | no post reaches a closing window (the page's `postToUiThread`) | no |
| `tests/app-unit/BookkeeperTests.cpp` | 213 | the transfer lock against save state deletions | no |
| `tests/app-unit/FolderMergeTests.cpp` | 157 | a rescan keeps the objects its holders point at (the page's `:335` post, #246's shape) | no |
| `tests/app-unit/JourneyTiersTests.cpp` | 128 | the journey's composed commands (`>>> tier` producers) | no |
| `tests/app-unit/RunLockTests.cpp` | 85 | the run lock's pid | no |
| `tests/app-unit/TextFitTests.cpp` | 75 | `TextFit::fitOneLine` on characters (the page's `fitOneLine`, `:580-586`) | no |
| `tests/app-unit/main.cpp` | 2 | doctest's main | no |
| `tests/app-unit/fakes/ThreadedCloudSync.h` | 23 | the card's double: `start`, `isRunning`, the stamps | no |
| `tests/app-unit/fakes/ApiSystem.h`, `FileData.h`, `LocaleES.h`, `Log.h`, `SystemConf.h`, `Window.h`, `components/AsyncNotificationComponent.h`, `utils/FileSystemUtil.h` | 12, 9, 5, 20, 10, 12, 24, 10 | doubles for the binaries above | no |
| `tests/cloud-oauth-lifetime.py` | 184 | GuiMenu's sign-in callbacks under ASan (compiles) | no: subject is `GuiMenu.cpp`, T26's |
| `tests/cloud-sync-last-run.py` | 82 | GuiMenu's `cloudLastRunWhy` over stamps (compiles) | no: T26's |
| `tests/maintenance-why.py` | 72 | GuiMenu's `maintenanceWhy` (compiles) | no: T26's |
| `tests/cloud-set-systems-quoting.py` | 99 | GuiMenu's `cloudSetSystemsCommand` through `/bin/sh` (compiles) | no: T26's |
| `tests/cloud-gated-row.py` | 125 | GuiMenu's `cloudAddGatedEntry` (compiles) | no: T26's |
| `tests/cloud-folder-reopen.py` | 51 | reads GuiMenu's source for the reopened row (no compiler) | no: T26's |
| `tests/cloud-content-selection.py` | 272 | GuiMenu's content picker (compiles) | no: T26's |
| `tests/cloud-oauth-await.py` | 101 | GuiMenu's `cloudOAuthAwaitSession` (compiles) | no: T26's |

The `tests/app-unit/` tree is at the top of the ES repository, not under `es-app/tests/`. The eight harnesses test the callers in `GuiMenu.cpp`; none tests one of the eight sources except through `CloudText.cpp`. Only `jobs-tests` is a test of this slice's code; it ran here on the coordinator's yes (F-19).

## The protocol

Generated by `tools/t18-protocol-table.py` at 09:55:28 UTC (exit 0; output `stage-b/protocol-table.md`). It asserts 18 rows and each row's producer and reader counts. Against upstream's `651150fc88` it exits 1 and names three rows (§ Proofs, P8). Every producer and reader cell is a search hit; only the last column is the lane's words.

<!-- BEGIN GENERATED stage-b/protocol-table.md -->
| # | Marker or exit | Printed or produced by | Page reader (`CloudTransferJob.cpp`, `GuiCloudTransfer.cpp`) | Card reader (`ThreadedCloudSync.cpp`) | What the player sees |
| ---: | --- | --- | --- | --- | --- |
| 1 | `>>> pid` | es-app: CloudTransferJob.cpp:637, ThreadedCloudSync.cpp:207 | CloudTransferJob.cpp:272 | ThreadedCloudSync.cpp:254 | nothing: the process group a stop signals (`deliverStop`, `cancelForLaunch`) |
| 2 | `>>> doing` | scripts: cloud_net_ready:160, cloud_net_ready:213, cloud_scan:275, cloud_scan:292, cloud_scan:322, cloud_scan:349; es-app: main.cpp:674, main.cpp:680, main.cpp:683, GuiMenu.cpp:5044, GuiMenu.cpp:5125 | CloudTransferJob.cpp:382 | ThreadedCloudSync.cpp:257 | card: `CHECKING THE CONNECTION...` / `WAITING FOR A NETWORK...` (network), the half's word and bar (receive, send); page row 3: `PACKING UP YOUR SETTINGS...`, `PUTTING YOUR SETTINGS BACK...`, the scan's sentence, `COMPARING WITH THIS DEVICE...`; `copy`/`verify`/`remove` have no producer (the retired folder move) |
| 3 | `>>> why` | scripts: cloud_backup:790, cloud_backup:940, cloud_backup:973, cloud_backup:979, cloud_backup:1044, cloud_backup:1218, cloud_backup:1224, cloud_backup:1236 (+101 more) | CloudTransferJob.cpp:280 | ThreadedCloudSync.cpp:310 | card: the outcome line's why (`COULDN'T FINISH - <why>`), translated by `localizedWhy`; page: line 4 beside the items it stopped (§ The why table) |
| 4 | `>>> offer` | scripts: cloud_backup:1663, cloud_restore:1739, cloud_restore:1748 | CloudTransferJob.cpp:392 | ThreadedCloudSync.cpp:315 | `CloudOffer::present` after the run: the card only when it completed and was not an automatic sync's no-folder skip; the page on dismissal of a completed run with no completed action |
| 5 | `>>> tier` | es-app: main.cpp:682, main.cpp:685, GuiMenu.cpp:5006, GuiMenu.cpp:6140, GuiMenu.cpp:6141, JourneyTiers.h:138 | CloudTransferJob.cpp:290 | ThreadedCloudSync.cpp:325 | card: a run whose parts disagree reads `COULDN'T FINISH - <the failing part's why>`; page: line 2 `N OF M ITEMS DID NOT FINISH`, line 4 the parts |
| 6 | `>>> unit` | scripts: cloud_backup:1586, cloud_backup:1975, cloud_content_backup:718, cloud_content_restore:962, cloud_content_restore:1514, cloud_restore:1629, cloud_restore:1964, cloud_scan:274 (+3 more); es-app: GuiMenu.cpp:5043, GuiMenu.cpp:5125 | CloudTransferJob.cpp:352 | -- | page rows 1 and 2: the item and `ITEM i OF n` (the card drops it: `default:` at its switch) |
| 7 | `>>> removed` | scripts: cloud_content_restore:996, cloud_content_restore:1068, cloud_content_restore:1110 | CloudTransferJob.cpp:338 | -- | page line 3 `REMOVED N FILES FROM THIS DEVICE`, line 4 per system (the card drops it) |
| 8 | exit 0 | rclone's code, or a script's own success, passed through | CloudTransferJob.cpp:302, CloudTransferJob.cpp:691, GuiCloudTransfer.cpp:289, GuiCloudTransfer.cpp:435, GuiCloudTransfer.cpp:440 | ThreadedCloudSync.cpp:492, ThreadedCloudSync.cpp:494 | `COMPLETED` |
| 9 | exit 9 | rclone's code, or a script's own success, passed through | CloudTransferJob.cpp:302, CloudTransferJob.cpp:691, GuiCloudTransfer.cpp:289, GuiCloudTransfer.cpp:435, GuiCloudTransfer.cpp:440 | ThreadedCloudSync.cpp:483, ThreadedCloudSync.cpp:492, ThreadedCloudSync.cpp:494 | `COMPLETED` (rclone's nothing needed moving) |
| 10 | exit 3 / 4 | scripts: cloud_backup:830, cloud_content_backup:277, cloud_content_restore:324, cloud_restore:836 | CloudTransferJob.cpp:330, CloudTransferJob.cpp:722 | ThreadedCloudSync.cpp:84, ThreadedCloudSync.cpp:108 | `COULDN'T FINISH - COULDN'T FIND YOUR CLOUD FOLDER` |
| 11 | exit 5 | scripts: cloud_backup:831, cloud_content_backup:278, cloud_content_restore:325, cloud_restore:837 | CloudTransferJob.cpp:330, CloudTransferJob.cpp:722 | ThreadedCloudSync.cpp:85, ThreadedCloudSync.cpp:109 | `COULDN'T FINISH - YOUR CLOUD STOPPED ANSWERING` |
| 12 | exit 124 | scripts: cloud_backup:835, cloud_backup:974, cloud_content_backup:278, cloud_content_restore:325, cloud_restore:841, cloud_restore:1027, cloud_scan:124 | CloudTransferJob.cpp:330, CloudTransferJob.cpp:722 | ThreadedCloudSync.cpp:85, ThreadedCloudSync.cpp:109 | `COULDN'T FINISH - YOUR CLOUD STOPPED ANSWERING`, or the scripts' `THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME` on an automatic run |
| 13 | exit 7 / 8 | scripts: cloud_backup:833, cloud_content_backup:280, cloud_content_restore:327, cloud_restore:839 | CloudTransferJob.cpp:330, CloudTransferJob.cpp:722 | ThreadedCloudSync.cpp:86, ThreadedCloudSync.cpp:110 | `COULDN'T FINISH - YOUR CLOUD WOULDN'T TAKE THE FILES` |
| 14 | exit 69 | scripts: cloud_backup:20, cloud_content_backup:37, cloud_content_restore:74, cloud_net_ready:54, cloud_restore:21, cloud_scan:43 | CloudTransferJob.cpp:721, GuiCloudTransfer.cpp:455 | ThreadedCloudSync.cpp:91, ThreadedCloudSync.cpp:112, ThreadedCloudSync.cpp:509, ThreadedCloudSync.cpp:544, ThreadedCloudSync.cpp:615, ThreadedCloudSync.cpp:621, ThreadedCloudSync.cpp:668, ThreadedCloudSync.cpp:754 | `SKIPPED - YOU'RE NOT ONLINE` when nothing moved; `COULDN'T FINISH - YOU WENT OFFLINE PART-WAY THROUGH` when the script stamped the cut |
| 15 | exit 75 | scripts: cloud_backup:20, cloud_content_backup:37, cloud_content_restore:74, cloud_restore:21, cloud_scan:361, cloud_setup:798 | CloudTransferJob.cpp:721, GuiCloudTransfer.cpp:455, GuiCloudTransfer.cpp:460 | ThreadedCloudSync.cpp:92, ThreadedCloudSync.cpp:113, ThreadedCloudSync.cpp:534, ThreadedCloudSync.cpp:670 | `SKIPPED - A SYNC IS ALREADY RUNNING`; a scan's `SKIPPED - ANOTHER CLOUD CHECK IS RUNNING` (eight wordings in all, § The why table) |
| 16 | exit 130 | scripts: cloud_backup:2504, cloud_content_transfer:113, cloud_restore:2318 | CloudTransferJob.cpp:704 | ThreadedCloudSync.cpp:87, ThreadedCloudSync.cpp:111, ThreadedCloudSync.cpp:126, ThreadedCloudSync.cpp:458, ThreadedCloudSync.cpp:914, ThreadedCloudSync.cpp:924 | a stop this process made: `SKIPPED - YOU CANCELLED IT` / `SKIPPED - YOU STARTED A GAME`; another's: `COULDN'T FINISH - IT WAS STOPPED` |
| 17 | NoFolder (78) | es-app: ThreadedCloudSync.cpp:492 | GuiCloudTransfer.cpp:455, GuiCloudTransfer.cpp:462 | ThreadedCloudSync.cpp:93, ThreadedCloudSync.cpp:114, ThreadedCloudSync.cpp:127, ThreadedCloudSync.cpp:566 | `SKIPPED - YOUR CLOUD FOLDER ISN'T SET UP YET` with `SET IT UP: GAME SETTINGS > MANAGE CLOUD STORAGE` (the card computes it from the offer; no script exits 78) |
| 18 | default | scripts: cloud_backup:844, cloud_content_backup:282, cloud_content_restore:329, cloud_restore:850 | CloudTransferJob.cpp:330, CloudTransferJob.cpp:722 | ThreadedCloudSync.cpp:94 | `COULDN'T FINISH - SOMETHING WENT WRONG` |

Rows: 18 (expected 18).
<!-- END GENERATED -->

Read with the code:

- **Two readers, one parser.** `CloudText::classifyProtocolLine` (`CloudText.cpp:555-644`) classifies; the job (`CloudTransferJob.cpp:267-406`) and the card (`ThreadedCloudSync.cpp:249-335`) act. The card drops `unit`, `removed` and `Unknown` at its `default:` (`:330-332`); the job drops `Unknown` at its `default:` (`:399-403`). Neither logs a marker it does not know (F-03).
- **`>>> pid` is taken from every line, not the first** (`CloudTransferJob.cpp:272-279`, `ThreadedCloudSync.cpp:254-256`). Only the three wrappers print one (`CloudTransferJob.cpp:637`, `ThreadedCloudSync.cpp:207`, `OfflineScanJob.cpp:135`), and no script does at `8ebaf8daad`, so the stop's target is right today. A script that ever printed the line would redirect the stop, and `>>> pid 1` would send `kill(-1, ...)` (F-01).
- **The wrappers differ by one trap** (r09). The job's is `setsid sh -c 'echo ">>> pid $$"; { trap '' PIPE; CMD ; }' 2>&1`; the card's is `setsid sh -c 'echo ">>> pid $$"; CMD' 2>&1`. When EmulationStation goes away under a run, the job's scripts survive their next write and can still stamp; the card's die of SIGPIPE at their next `echo`, before their stamp (F-02).
- **The card reads with `fgets` into 512 bytes** (`ThreadedCloudSync.cpp:211-212`); the job reads a character at a time with a 1,024-byte cap (`CloudTransferJob.cpp:656-677`). A card line over 511 bytes arrives as two, and the second half is not a protocol line (F-04).
- **`doing copy`, `verify` and `remove` have no producer** (the folder move, #353, retired by D-CLOUD-175). The job's allowlist (`CloudTransferJob.cpp:387-389`) and the page's three strings (`GuiCloudTransfer.cpp:1027-1032`) remain (F-16).

## The why table

Generated by `tools/t18-why-table.py` at 09:55:29 UTC (exit 0; output `stage-b/why-table.md`). It asserts eight counts: 38 ES rows, 38 unique, 34 literal script sentences, 32 shared, 2 script-only, 6 ES-only against the literals, 17 variable emitter lines, and 1 ES row with no producer after expansion. It also asserts the eight wordings exit 75 is given. The variable emitters are expanded through each script's `why_for`, the connection layer's `selection_reason` and the stamps' offline why. Against `651150fc88` it exits 1 and names seven counts (P9).

<!-- BEGIN GENERATED stage-b/why-table.md -->
| # | Sentence | ES row (`CloudText.cpp`) | Literal emitters at `8ebaf8daad` | Filled by a variable emitter | Status |
| ---: | --- | --- | --- | --- | --- |
| 1 | `YOUR CLOUD STORAGE ISN'T SET UP YET` | :424 | cloud_backup:940, cloud_content_backup:107, cloud_content_restore:144, cloud_restore:993 | `selection_reason` cloud_connections.py:69 | shared |
| 2 | `CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.` | :425 | -- | `selection_reason` cloud_connections.py:68 | ES row; filled by a variable emitter |
| 3 | `COULDN'T REACH YOUR CLOUD - CHECK YOUR SIGN-IN` | :426 | cloud_backup:979, cloud_restore:1032 | -- | shared |
| 4 | `YOUR CLOUD STOPPED ANSWERING` | :427 | cloud_backup:1044, cloud_restore:1093, cloud_scan:124, cloud_scan:159, cloud_setup:343, cloud_setup:350, cloud_setup:400 | `why_for` cloud_backup:831, cloud_backup:842, cloud_content_backup:278, cloud_content_restore:325, cloud_restore:837, cloud_restore:848 | shared |
| 5 | `YOUR CLOUD SYNC SETTINGS COULDN'T BE READ` | :428 | cloud_backup:1218, cloud_backup:1224, cloud_backup:1308, cloud_backup:1764, cloud_content_backup:98, cloud_content_backup:192, cloud_content_backup:204, cloud_content_restore:135, cloud_content_restore:229, cloud_content_restore:241, cloud_content_restore:258, cloud_restore:1267, cloud_restore:1273, cloud_restore:1357, cloud_restore:1832, cloud_scan:323, cloud_setup:319, cloud_setup:323, cloud_setup:324 | -- | shared |
| 6 | `YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED` | :429 | -- | -- | **ES-only: no producer at the rev** |
| 7 | `YOUR CLOUD FOLDER COULDN'T BE READ` | :430 | cloud_scan:163, cloud_setup:384, cloud_setup:413 | -- | shared |
| 8 | `YOUR CLOUD SETTINGS CHANGED. CHECK AGAIN` | :431 | cloud_scan:222 | -- | shared |
| 9 | `ANOTHER CLOUD CHECK IS RUNNING` | :432 | cloud_scan:361 | -- | shared |
| 10 | `YOUR CLOUD FOLDERS COULDN'T BE CREATED` | :433 | cloud_setup:818, cloud_setup:881 | -- | shared |
| 11 | `CHECK WHAT WOULD CHANGE FIRST` | :434 | cloud_content_restore:906 | -- | shared |
| 12 | `AN OLD FOLDER SETTING IS IN THE WAY` | :435 | cloud_backup:1236, cloud_restore:1285 | -- | shared |
| 13 | `YOUR SAVES FOLDER ISN'T ON THIS DEVICE` | :436 | cloud_backup:1616 | -- | shared |
| 14 | `THIS DEVICE'S SETTINGS BACKUP IS DAMAGED` | :437 | cloud_backup:2196, backuptool:1450, backuptool:1486 | -- | shared |
| 15 | `THE COPY IN YOUR CLOUD ISN'T COMPLETE` | :438 | cloud_backup:2307 | -- | shared |
| 16 | `COULDN'T FIND YOUR CLOUD FOLDER` | :439 | cloud_scan:123 | `why_for` cloud_backup:830, cloud_content_backup:277, cloud_content_restore:324, cloud_restore:836 | shared |
| 17 | `SOME FILES DIDN'T FINISH` | :440 | -- | `why_for` cloud_backup:832, cloud_content_backup:279, cloud_content_restore:326, cloud_restore:838 | ES row; filled by a variable emitter |
| 18 | `YOUR CLOUD WOULDN'T TAKE THE FILES` | :441 | cloud_scan:125 | `why_for` cloud_backup:833, cloud_content_backup:280, cloud_content_restore:327, cloud_restore:839 | shared |
| 19 | `IT WAS STOPPED` | :442 | -- | `why_for` cloud_backup:834, cloud_content_backup:281, cloud_content_restore:328, cloud_restore:840 | ES row; filled by a variable emitter |
| 20 | `THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME` | :443 | -- | `why_for` cloud_backup:840, cloud_restore:846 | ES row; filled by a variable emitter |
| 21 | `SOMETHING WENT WRONG` | :444 | cloud_content_restore:894, cloud_scan:126, cloud_scan:132, cloud_scan:327 | `why_for` cloud_backup:844, cloud_content_backup:282, cloud_content_restore:329, cloud_restore:850 | shared |
| 22 | `COULDN'T TELL WHICH CARD YOUR SAVES ARE ON` | :445 | cloud_saves_root:137 | -- | shared |
| 23 | `YOUR SAVES ARE ON A DIFFERENT CARD` | :446 | cloud_saves_root:156 | -- | shared |
| 24 | `YOUR SAVES CHANGED CARDS PART-WAY THROUGH` | :447 | cloud_saves_root:177 | -- | shared |
| 25 | `THERE'S NO SETTINGS BACKUP ON THIS DEVICE YET` | :448 | backuptool:1427 | -- | shared |
| 26 | `COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS` | :449 | backuptool:1480, backuptool:1499, backuptool:1552, backuptool:1568, backuptool:1617 | -- | shared |
| 27 | `THE RESTORE COULDN'T FINISH` | :450 | backuptool:1525, backuptool:1732, backuptool:1735 | -- | shared |
| 28 | `THIS DEVICE CAN'T MAKE A SETTINGS BACKUP` | :451 | backuptool:1774 | -- | shared |
| 29 | `THE BACKUP COULDN'T FINISH WHILE GATHERING YOUR SETTINGS` | :452 | backuptool:1856 | -- | shared |
| 30 | `THE BACKUP COULDN'T FINISH` | :453 | backuptool:1825, backuptool:1862 | -- | shared |
| 31 | `SOMETHING CHANGED SINCE YOU CHECKED` | :458 | cloud_content_backup:701, cloud_content_restore:816, cloud_content_restore:900, cloud_content_restore:976, cloud_content_restore:1500 | -- | shared |
| 32 | `COULDN'T RECORD WHICH CARD YOUR SAVES ARE ON` | :459 | cloud_saves_root:185 | -- | shared |
| 33 | `YOU WENT OFFLINE PART-WAY THROUGH` | :460 | -- | the stamp's why cloud_backup:735, cloud_content_backup:338, cloud_content_restore:393, cloud_restore:736 | ES row; filled by a variable emitter |
| 34 | `THIS DEVICE CAN'T RESTORE SETTINGS` | :461 | backuptool:1415, backuptool:1443 | -- | shared |
| 35 | `A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING` | :462 | backuptool:1420, backuptool:1780 | -- | shared |
| 36 | `THERE'S NOTHING TO BACK UP YET` | :463 | backuptool:1854 | -- | shared |
| 37 | `A SIGN-IN WAS FOUND IN THE BACKUP` | :464 | backuptool:1858 | -- | shared |
| 38 | `YOUR OWN BACKUP LIST NAMES A FOLDER A BACKUP CAN'T CARRY` | :465 | backuptool:1860 | -- | shared |
| 39 | `ANOTHER CLOUD SYNC IS RUNNING` | -- | cloud_setup:797 | -- | **script-only: no ES row** |
| 40 | `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` | -- | backuptool:1495 | -- | **script-only: no ES row** |

Counts: es_rows 38 (expected 38), es_unique 38 (expected 38), literal 34 (expected 34), shared_literal 32 (expected 32), script_only 2 (expected 2), es_only_literal 6 (expected 6), variable_lines 17 (expected 17), es_only_unproduced 1 (expected 1)
Variable emitter lines: cloud_backup:973, cloud_backup:1508, cloud_backup:1516, cloud_backup:1690, cloud_backup:2425, cloud_content_backup:784, cloud_content_restore:1002, cloud_content_restore:1025, cloud_content_restore:1073, cloud_content_restore:1447, cloud_content_restore:1572, cloud_restore:1026, cloud_restore:1530, cloud_restore:1538, cloud_restore:2225, cloud_scan:143, cloud_scan:157
ES-only with no producer: `YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED`
Pairs whose two spellings differ: none

**The fallback map** (`ThreadedCloudSync::whyForCode` at the pin; `why_for` in the scripts; the header comment `ThreadedCloudSync.h:93-99`; `es-player-text.md` § Outcome vocabulary's **Why** sentence):

| Code | Code says (`ThreadedCloudSync.cpp`) | Scripts' `why_for` | Header comment | Rule |
| --- | --- | --- | --- | --- |
| 3 4 | `COULDN'T FIND YOUR CLOUD FOLDER` (:84) | `COULDN'T FIND YOUR CLOUD FOLDER` | **differs** (names something else) | **differs**: says `YOUR CLOUD FOLDER WASN'T FOUND` (#909) |
| 5 124 | `YOUR CLOUD STOPPED ANSWERING` (:85) | `YOUR CLOUD STOPPED ANSWERING` | same | same |
| 7 8 | `YOUR CLOUD WOULDN'T TAKE THE FILES` (:86) | `YOUR CLOUD WOULDN'T TAKE THE FILES` | **differs** (names something else) | **absent** (#909) |
| Stopped | `IT WAS STOPPED` (:87) | `IT WAS STOPPED` | same | same |
| default | `SOMETHING WENT WRONG` (:94) | `SOMETHING WENT WRONG` | same | same |

**Exit 75's wordings** (every string the eight and the scripts give a held lock):

| Wording | Where |
| --- | --- |
| `SKIPPED - ANOTHER CLOUD CHECK IS RUNNING` | CloudText.cpp:410 |
| `SKIPPED - A SYNC IS ALREADY RUNNING` | CloudText.cpp:411 |
| `ANOTHER CLOUD CHECK IS RUNNING` | CloudText.cpp:432 |
| `A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING` | CloudText.cpp:462 |
| `WAIT FOR THE CURRENT CLOUD TASK TO FINISH, THEN TRY AGAIN.` | CloudText.cpp:1387 |
| `A SYNC IS ALREADY RUNNING` | ThreadedCloudSync.cpp:92 |
| `SKIPPED - A SYNC IS ALREADY RUNNING` | ThreadedCloudSync.cpp:536 |
| `A SYNC IS ALREADY RUNNING.` | ThreadedCloudSync.cpp:781 |
| `ANOTHER CLOUD CHECK IS RUNNING` | cloud_scan:361 (a script's `>>> why`) |
| `ANOTHER CLOUD SYNC IS RUNNING` | cloud_setup:797 (a script's `>>> why`) |
| `A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING` | backuptool:1420, backuptool:1780 (a script's `>>> why`) |

Distinct wordings: 8 (expected 8)
<!-- END GENERATED -->

Read with the code:

- **The two script-only sentences** (F-11).
  - `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` (`backuptool:1495`) reaches a page. The settings restore's chain runs `backuptool restore` with its output kept (`GuiMenu.cpp:5043-5045`). The why lands on line 4 of the done page through `CloudText::localizedWhy`, which passes an unlisted sentence through as it came, so it is English under a translated outcome word. es-player-text.md lists it as proposed (D-UI-117).
  - `ANOTHER CLOUD SYNC IS RUNNING` (`cloud_setup:797`, exit 75 from `--seed-folders`) never shows. The CREATE page's run ends skipped (`GuiCloudTransfer.cpp:454-461`), and line 4 is not drawn on a skip (`:813`). It is one of the eight wordings of exit 75 all the same (F-15).
- **The ES row with no producer:** `YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED` (`CloudText.cpp:429`), printed by the retired `cloud_migrate_layout` (es-player-text.md says so) and by nothing at `8ebaf8daad` (F-16).
- **The test that is said to guard the table does not read the scripts** (F-12). `CloudText.cpp:419-422` says the list is the emitter table in `CloudTextTests.cpp`, "which fails on a why a script prints that is not here". The table (`CloudTextTests.cpp:632-721`) is typed, with file:line citations from older trees (`4476f90394`, `6f89bc7cec`). A script sentence missing from it, such as either of the two above, passes. This generator is the reading the comment describes.
- **The fallback map** (the brief's "six words", five code groups here). The code and the scripts' `why_for` agree on every group. The header comment above it (`ThreadedCloudSync.h:93-99`) names two groups in older words and sits above `writeStamp` rather than `whyForCode`, so it is **this slice's drift** (F-13). The rule's sentence (es-player-text.md § Outcome vocabulary) says `YOUR CLOUD FOLDER WASN'T FOUND` and `YOUR CLOUD REFUSED THE TRANSFER` and claims the six are "duplicated verbatim in ThreadedCloudSync's own fallback map"; that half is **#909's** (F-14).

## The surfaces

| Surface | Tier (es-native-ui.md) | What it shows | How it ends | What it writes | Its CANCEL | Its question |
| --- | --- | --- | --- | --- | --- | --- |
| The sync card (`ThreadedCloudSync`, an `AsyncNotificationComponent` with its action row, `:46`) | third: progress, 0.9W, top | the running word; the live line as candidates (`TRANSFERRING FILE i OF n (x OF y)` ... `x OF y`, `:409-425`); the two-half bar (`:186-196`); then the outcome line and the action line (`:700`) | lingers 1.5 s (completed, nothing to act on) or 5 s (`:731`), then fades; `delete this` (`:757`) | `last-sync-<origin>` before the card speaks (`:565-566`); a cancelled run's script stamps restamped (`:581-582`) | none on the card | the launch question over it (`FileData.cpp:993-1007`): YOUR SAVES ARE SYNCING WITH THE CLOUD. / STOP IT AND PLAY / KEEP WAITING |
| The transfer page (`GuiCloudTransfer`) | fourth: a page sat in until dismissed (D-UI-078) | seven rows (`GuiCloudTransfer.h:171-183`): the item, ITEM i OF n, the doing line, the totals, the bar or the note, elapsed, the footer | dismissed by a press once finished (`:246-343`); a completed scan or create goes on by itself (`:709`, `:1065-1076`) | nothing itself; the job restamps a stopped run's parts (`CloudTransferJob.cpp:710`) | B while it runs, when `cancellable()` (`:254-258`) | the launch gate for a run current between its end and dismissal (`stillRunningSentence`, `:518-531`; a seam since D-UI-078) |
| The CANCEL confirmation (`askCancel`, `:351-361`) | dialog | three texts by kind: the check, the create, and `CANCEL THIS BACKUP OR RESTORE?` for every other kind, a match included (F-08) | YES stops (`stopByPlayer`), NO keeps waiting | -- | NO is last and takes back | -- |
| The done page (the same page, `mShownFinished`) | fourth | the word (`:420-469`); `N OF M ITEMS DID NOT FINISH`; what moved; the failed items with their whys; what is in place; elapsed; the footer | any press closes; south retries when it did not complete and is not a match (`:265-281`); the settings restore's RESTART (`GuiMenu.cpp:5083-5096`) | -- | -- | a script's offer, raised on dismissal (`:341`) |
| `A SYNC IS ALREADY RUNNING.` (`ThreadedCloudSync.cpp:781`) | dialog, one OK | a refusal of a second start | OK | -- | -- | -- |

The help bar is the page's own (`:575-576`) and names buttons by role: CANCEL on back while running; TRY AGAIN on OK and CLOSE on back once done (`:373-392`). The footer no longer spells A and B (`:902-912`, `:1056-1060`).

## The lifetimes

| Line | What happens | What holds a pointer or reference across it | Covered by |
| --- | --- | --- | --- |
| `GuiCloudTransfer.cpp:207` | `advance()`: the run dismissed, `delete this`, then the step | the step was copied out first (`:205`); nothing of the page is touched after | `untested` (the posted call `:1070` is the only caller) |
| `GuiCloudTransfer.cpp:328` | `input()` on a finished run: `delete this` | `lock` (unlocked at `:323`; its destructor does not touch the mutex when it does not own it); `job`, a reference to `*mJob`, unused after; `window`, the actions and the offer copied before | `untested` |
| `GuiCloudTransfer.cpp:335` | `postToUiThread([] { SystemData::rescanChangedFolders(); })` | nothing captured; the rescan's own holders are #246's (`dropGameListView`/`remakeGameListView`) | `FolderMergeTests.cpp:80-144` (`app-unit-tests`; not run here) |
| `GuiCloudTransfer.cpp:1070` | the posted `advance` with `[page, alive]` | `alive` is a `weak_ptr` to `mAlive`, which the page owns and its destructor sets false (`:173-174`): a page that is gone fails the lock | `untested` |
| `ThreadedCloudSync.cpp:56` | `std::thread(&ThreadedCloudSync::run, this).detach()` | the thread holds `this` until `run()` deletes it; `start()` installs `mInstance` under `sInstanceLock` in the same hold (`:773-779`), so `run()`'s clear at `:716-720` cannot overtake it | `AtomicFileTests.cpp:792` (reads the source; ran, in `es-file-tests`) |
| `ThreadedCloudSync.cpp:716-720`, `:731` | `mInstance` cleared under the lock, then a 1.5 s or 5 s linger | a `cancelForLaunch` that took the pointer under the lock finishes with it before the clear; after it, nobody reaches the object except its own thread | `untested` |
| `ThreadedCloudSync.cpp:757` | `delete this` (the destructor closes the card and clears `mInstance` if it is still this, `:59-71`) | `mWndNotification` closed in the destructor; `CloudOffer::present` and `ProxyCards::afterSync` take the window, not the object | `untested` |
| `ThreadedCloudSync.cpp:784-864` | `cancelForLaunch`: the mark and SIGTERM under the lock; a 20 ms spin; SIGKILL at 1,500 ms; `false` at 2,000 ms | `sync` is dereferenced only while `mInstance == sync` under the lock (`:839-850`); it runs **on the interface thread** (called from `FileData.cpp:1001`), so no frame is drawn while it spins (F-07) | `untested` |
| `CloudTransferJob.cpp:65` | `std::thread([job] { job->run(); }).detach()` | the thread holds a `shared_ptr`; `sCurrent` holds another until `dismiss` | `JobsTests.cpp:111-117` (run: PASS) |
| `CloudTransferJob.cpp:87-106` | `stopForLaunch`: the look and the mark under the run's lock; SIGTERM or SIGKILL through `requestStop` | `job` is a `shared_ptr` from `current()` | `JobsTests.cpp:135`, `:163` (run: PASS) |
| `CloudTransferJob.cpp:100` | `requestStop(hard ? SIGKILL : SIGTERM)`: a SIGKILL replaces a pending SIGTERM | atomics `mStopSignal`, `mSignalSent`, `mPid` | `JobsTests.cpp:135` (run: PASS) |
| `CloudTransferJob.cpp:108-127` (`:121`) | `stopByPlayer`: the same, SIGTERM | as above | `JobsTests.cpp:130`, `:144`, `:163` (run: PASS) |
| `CloudTransferJob.cpp:139-162` | `requestStop` / `deliverStop`: whichever of the stop and the reader sees both the request and the pid sends; each signal once; `pid <= 0` never signals | the atomics; the reader thread and the stopper | `JobsTests.cpp:130`, `:135` (run: PASS) |

Nothing here holds a page or a card across its own deletion. The lifetimes that matter most (the job's stop races) are covered by `jobs-tests`, which this lane cannot build within the brief's compiler scope (F-19).

## The strings

**219 `_( )` strings in the four `.cpp` files** (r14 counted 220; the 220th is `_("")` inside a comment at `CloudText.h:527`): `CloudText.cpp` 79, `CloudTransferJob.cpp` 2, `ThreadedCloudSync.cpp` 58, `GuiCloudTransfer.cpp` 80. All were read against es-player-text.md and es-ui-style-guide.md.

- **Held:**
  - every run ends in `COMPLETED`, `COULDN'T FINISH` or `SKIPPED - <reason>` (no `FAILED`, no `SUCCEEDED`, no log path);
  - *back up* only as a verb and *backup* only as a noun (r14);
  - no `WIFI` (r14);
  - the in-place clauses are the rule's (`ThreadedCloudSync.cpp:138-140`, `GuiCloudTransfer.cpp:884-886`);
  - TRY AGAIN and CLOSE on the help bar by role (`:385-390`);
  - YES first and NO last in the confirmation (`:354-360`);
  - the serial comma where a list has three (`CloudText.cpp:1100`, `:1397`);
  - every fork string of the eight has its French (r23: `tools/es-untranslated --es-src` names none in the eight).
- **Failures, by file:line:**
  - `GuiCloudTransfer.cpp:357-358` — the CANCEL confirmation over a **match** reads `CANCEL THIS BACKUP OR RESTORE?` / `THE NEXT BACKUP OR RESTORE FINISHES WHAT THIS ONE DIDN'T.` A match is neither, and the next match is refused without a new check (PL-001; `:363-371`, `CloudText::matchRecovery`). Dialog text promising behaviour the backend does not do (es-native-ui.md, the backuptool drift lesson) (F-08).
  - `GuiCloudTransfer.cpp:807-808` — `NOTHING NEW TO BRING DOWN` / `NOTHING NEW TO SEND UP`, the forms shown when `NOTHING NEW - YOU ALREADY HAD IT ALL` does not fit the line. That is the small panel, where most players read it. *Bring down* and *send up* paraphrase *restore* and *back up* (player-language.md: "the canonical verb, never a paraphrase") (F-09).
  - `GuiCloudTransfer.cpp:745` — `ITEM DID NOT FINISH` / `ITEMS DID NOT FINISH`: the formal register D-UI-031 replaced (`DIDN'T`). `:769` `... CAME DOWN TOO.`: a third verb for a restore (F-10).
  - `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` reaches line 4 untranslated (§ The why table; F-11).
  - Exit 75 has eight wordings across the eight files and the scripts (F-15).
- **The fit at 640x480** of every `outcomeCandidates` list (the card's outcome line, `ThreadedCloudSync.cpp:700`), every `actionCandidates` list (`:649`, `:691`), the card's live-line candidates (`:409-425`, `:281-285`), the scan sentence's `chooseThatFits` (`GuiCloudTransfer.cpp:1020-1023`) and the page's `fitOneLine`/`fitSentences` rows are proved only by a frame: the host has no font. **Owed to the window** (§ The guest cycle). The page sizes every row `(w, 0)` (`:73-74`) and fits with `fitOneLine` rather than wrapping, so `TextComponent`'s padded-width trap (es-code-traps.md) does not apply to a row that never wraps.
- **The non-ASCII lines** (r15): 0 `//` comment lines with a non-ASCII byte in the 30.
  - `GuiCloudTransfer.cpp`'s nine are `·` inside string literals (`" · "` separators at `:676`, `:682`, `:760`, `:795`, `:845`, `:957`, `:959`, `:992`, `:1045`), which xgettext accepts.
  - `CloudTransferJob.cpp:347` is the same in a literal beside `_("FILE")`.
  - `CloudTransferJob.h:151` is a trailing comment on a member, with no `_( )` within reach.
  - The card spells its separator `"\xC2\xB7"` (`ThreadedCloudSync.cpp:167`, `:183`, `:392`), the pattern the brief names.

## The tests

**Built and run on the host** by `tools/t18-build-tests.sh` (r20), which generates the `g++` commands from `es-app/tests/unit/CMakeLists.txt`'s own `add_executable` and `add_library` lists:

- the compiler: g++ 15.2.0 at `-std=c++17 -O0 -g0 -pthread`;
- the include roots, by binary:
  - `es-unit-tests`: `es-app/src`, `es-core/src`, `external`, and rapidjson;
  - `es-file-tests`: `es-core/src` and `external`, with `-DES_ROOT_DIR=<tree>`;
  - `es-conf-tests`: `tests/unit/fakes` first, then `es-core/src` and `external`;
  - `es-file-tests-win32`: its one object built with `-D_WIN32`;
- the source lists, as `sources.txt` in the build directory: 28, 2, 3, and 2 plus the object;
- rapidjson: the 35-header copy at `/workspace/tmp/m6-t18/rapidjson`, every header's sha256 matching M7's prep `inputs.json` (sha256 `a5ecb968…`; `00` § Stage A).

**Results:** `es-unit-tests` 185 cases and 4,795 assertions; `es-file-tests` 24 and 3,389; `es-conf-tests` 10 and 119; `es-file-tests-win32` 2 and 14. **221 cases, 0 failed: PASS.** That equals r06's 221 `TEST_CASE` lines. A FAIL would have been a nonzero `rc` on any binary, or a case count below 221, meaning a test file left out of a list.

**`tests/app-unit`'s `jobs-tests`, built and run on the coordinator's yes** (#665, 10:02 UTC; F-19) by `tools/t18-build-jobs-tests.sh`:
- The tool generates the commands from `tests/app-unit/CMakeLists.txt`: the file's own `-g -fno-omit-frame-pointer -fsanitize=address,undefined`, its `configure_file` copies into `under-test/` (the test's copies of the shipped `CloudTransferJob.cpp` and `OfflineScanJob.cpp`, never an edit of either), and the target's six sources with the fakes first on the include path.
- **`RUN jobs-tests: rc 0; [doctest] test cases: 6 | 6 passed | 0 failed | 0 skipped [doctest] assertions: 28 | 28 passed | 0 failed`**, from 10:07:52 to 10:08:01 UTC (`stage-c/jobs-tests.out`).
- The cases are the stop before the pid (`:130`, `:135`), the completed run not called stopped (`:144`), the look-then-mark race (`:163`), the restamp against the before-snapshot (`:183`), and the scan job's post after `main()` lets go (`:210`).
- A FAIL would have been a sanitizer report or a failed case: a race or a use after free in the shipped job.

**Fixtures:** the 22 files carry no secret-shaped literal at rest (#1061). The check is `. .githooks/secret-patterns; grep -E -e "$SECRET_PATTERNS"`: 0 hits in the 22, and 1 on a control line built at run time.

| Test file | Cases | Subject | Trap of es-code-traps.md it covers |
| --- | ---: | --- | --- |
| `CloudTextTests.cpp` | 70 | `CloudText`: stamps, outcomes, protocol, whys, units, sizes, live lines, phases, the network step, the proxy's stamps, folder refusals | rclone's piped progress: the glued `Transferred:` (the `liveLine` block at `:907`), the torn `Ki`/`Mi` (`parseBytes`, `:866-867`), U+2026 kept (`cleanLine`, `:564`); "pure text has a home". **Not** the `%3d` separator at 100%, which is the job's parser (`CloudTransferJob.cpp:529-551`), nor the job's own glued splitter (`:654-677`) (F-05) |
| `AtomicFileTests.cpp` | 24 | `Utils::AtomicFile`; the card's detached thread (`:792`) | none (the last-known-good writer, engineering-practices.md) |
| `AtomicFileWin32Tests.cpp` | 2 | the `_WIN32` writer | none |
| `CaptureRotationTextTests.cpp` | 8 | rotation records | "a file under three bytes reads as empty" (`:62-100`: a record is a line that says what it is) |
| `CheevosIndexTests.cpp` | 6 | the game index | none |
| `CheevosRetryTests.cpp` | 7 | the sign-in retry | none |
| `CloudFolderValidationTests.cpp` | 4 | the folder checks | none |
| `CommandLineTests.cpp` | 2 | the option swap | none |
| `DisplayAspectTextTests.cpp` | 3 | a screenshot's game | none |
| `LaunchCommandTests.cpp` | 8 | a launch command | none |
| `LogPolicyTests.cpp` | 3 | the log's rules | none |
| `MaskSecretsTests.cpp` | 12 | the credential mask | none (its fixtures are built at run time) |
| `OfflineAchievementsTextTests.cpp` | 15 | the proxy's JSON | none |
| `OfflineProxyUrlTests.cpp` | 4 | the proxy's address | none |
| `SaveStateJobQueueTests.cpp` | 10 | the save state queue | none |
| `SystemConfTests.cpp` | 10 | `system.cfg` | none |
| `TabStopsTests.cpp` | 3 | tab stops | none |
| `TimeTextTests.cpp` | 11 | the time beside a save | none |
| `WifiTextTests.cpp` | 19 | the Wi-Fi rows | none |
| `CMakeLists.txt` | -- | the four binaries | fails closed without rapidjson (`:72-74`) |
| `README.md` | -- | the list of record | -- |
| `fakes/SDL_timer.h` | -- | `SDL_GetTicks` stand-in | -- |

The cases by binary: 185 + 24 + 10 + 2 = 221. `es-conf-tests` holds `SystemConfTests.cpp`; `es-file-tests` holds `AtomicFileTests.cpp`; `es-file-tests-win32` holds `AtomicFileWin32Tests.cpp`.

## The runs

Every § 5 command, from `stage-a/out/runs.tsv` (all started 09:37:15 to 09:37:58 UTC). Each row ends with *a FAIL would mean*.

| Run | Exit | Seconds | The figure | A FAIL would mean |
| --- | ---: | ---: | --- | --- |
| r01 block | 0 | 0.44 | 30 paths, 11,193; read 29 / 11,116; fork-own 30; shipped 30 | the inventory or the regex moved under the brief |
| r02 lines | 0 | 0.07 | 11,193 by `wc -l` | the inventory's lines are not the pin's |
| r03 in merge base | 0 | 0.03 | 0 | a file upstream also carries, whose history is not all the fork's |
| r04 pin and base | 0 | 0.03 | merge base `bccd715707` = `upstream/master`; 725 ahead, 0 behind | the pin is behind ROCKNIX's master |
| r05 sources | 0 | 0.05 | 8 / 5,429; tests 22 / 5,764 | the split the questions rest on is wrong |
| r06 test cases | 0 | 0.07 | 221 `TEST_CASE`, 1,665 checks, 19 files; `CloudTextTests` 70 / 711 | a case count the binaries' run must equal |
| r07 declarations | 0 | 0.01 | 44 under GNU `grep -E`, 47 under `grep -P`; the three `-E` misses named | (the count is 47, the coordinator's 09:44 read; #1138) |
| r08 markers and exits | 0 | 0.01 | the seven markers at `CloudText.cpp:561-616`; 75 at `:1386`; 0 and 9 at the three lines | a marker parsed nowhere the brief says |
| r09 wrappers | 0 | 0.00 | the job's `trap '' PIPE` at `:637`; the card's none at `:207` | the two wrappers already agree |
| r10 stamps | 0 | 0.01 | `STAMP_DIR :892`; tmp and rename `:943-947`; the map `CloudText.cpp:186-189` | the stamp writer moved |
| r11 exists | 0 | 0.01 | 0 in the eight; control `GuiMenu.cpp` 35, `Win32ApiSystem.cpp` 31, `Scraper.cpp` 25 | a cached `exists()` reading a stamp |
| r12 lifetimes | 0 | 0.01 | every line of § The lifetimes | a lifetime the table does not name |
| r13 why table | 0 | 0.02 | 38 / 38 / 34 / 32 / 2 / 6 / 17 | (generated and asserted in § The why table) |
| r14 strings | 0 | 0.03 | 220 occurrences (219 strings and one comment); the card 58 / 50, the page 80 / 67; `WIFI` 0 | a string the rule forbids |
| r15 xgettext | 0 | 0.07 | 0 non-ASCII comment lines | an image build stopped by xgettext |
| r16 history | 0 | 0.96 | 181; 170 / 9 / 2; 2026-07-25 to 2026-10-11 | a commit outside the three identities |
| r17 callers | 0 | 0.02 | four callers; `GuiMenu.cpp` names `/usr/bin/cloud_` on 50 lines | a caller the questions miss |
| r18 toolchain | 0 | 0.05 | no `cmake`, no `ninja`; no M6 root with an ES build or rapidjson | (it is the reason r20 is generated) |
| r19 cmake list | 0 | 0.00 | the four `add_executable` / `add_library` lines | a binary the generator does not build |
| r20 unit tests | 0 | 39.78 | 221 cases PASS (§ The tests) | a failing case, or a binary that tests less |
| r21 syntax check | 0 (the step); the tool's own 2 | 0.00 | `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)`, rc 2 with `ES_BUILD_ROOT=/nonexistent` (never empty). The brief expected a `no ninja` line; the tool stops at the missing root first | (a CANNOT, recorded as one: not a pass) |
| r22 host syntax | 0 | 0.22 | `g++ -std=c++17 -fsyntax-only` over `CloudText.cpp`: rc 0 | `CloudText.cpp` does not parse with the host's compiler |
| r23 untranslated | 0 | 0.34 | `--es-src`: 0 in the eight | a fork string with no French |
| r24 menu map | 0 | 0.14 | 55 screens, 31 mapped, 24 declared, 0 missing; § Cloud `:231`; 8 cloud walks | a screen of the pin the map neither maps nor declares |
| r25 removal rule | 0 | 0.01 | nothing under `packages`, `projects` or `tools` since `cbf6d7ef83`; the ES HEAD the pin | the lane changed what it may not |
| r26 identity literal | 0 | 0.07 | `FOLDERS ALREADY CREATED WILL STAY. YOU CAN TRY AGAIN LATER.` absent from `bccd71570` | no literal can tell this binary from the base's |
| window: `time-to-play --vm` | 0 | 163 (10:20:06 to 10:22:49) | the exit sync's stamp **1.58 s** median, completed 3 of 3, inside D-CLOUD-119's 3 s; interface to a first frame **0.56 s** and game to game **1.01 s**, recorded and not bounded (D-CLOUD-122 open); the card at 640x480: `SYNCING SAVES TO THE CLOUD` / `STARTING...` (`guest-cycle/frames/640-ttp-r1-exit-001.png`) and `SYNC SAVES` / `COMPLETED` (`640-ttp-r1-exit-004.png`) | an exit sync that did not complete, a stamp past 3 s, or a missing headline number (the tool fails then, `headline_missing`) |

Wall times are `stage-a/out/runs.tsv`'s. Every run took under a second except r20, the build and the four runs (39.78 s).

## The guest cycle

**The window:** granted by the coordinator on #665 at 10:02 UTC, first in the host file's queue (M7 had nothing queued; the grant's line is on the host file at 10:02 with the census 0). START 10:06:23 UTC, posted on #665; the bound 10:36:23 plus a 5-minute grace. The runner is `guest-cycle/run.sh`; each stage's output is kept whole, through the mask, in `guest-cycle/`.

- **The image:** `/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`, 2,122,289,964 bytes, its `.sha256` OK (`pre.out`). The guest's copy is under `/workspace/tmp/m6-t18/vm-pair/`. The cloud is `tools/cloud-test-backend --backend webdav` on the host (`up.out`).
- **The installed EmulationStation, identified before any verdict** (`identity.out`, 10:07 UTC):
  - `/etc/os-release`: `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`, `BUILD_BRANCH="build/m7-signin-20261022-07"`.
  - `/usr/bin/emulationstation` sha256 `25155163fd7970f7da54b3f36d003b8c006111c894d4fe6f0c92d24d51831226`.
  - `strings | grep -c -F` gives 1 each for the identity literal `FOLDERS ALREADY CREATED WILL STAY. YOU CAN TRY AGAIN LATER.` (added by `1272b3405`, absent from the merge base), T2's two strings, `CANCEL THIS BACKUP OR RESTORE?`, `NOTHING NEW TO SEND UP` and `COMPARING WITH THIS DEVICE...`.
  - `069fc2704421` is not in the distribution repository, so its `package.mk`'s `PKG_VERSION` cannot be read here. The binary carries every string of the pin this window checks; **a verdict below is the pin's only as far as those strings reach**.
  - `setsid` on the image is busybox's (`/usr/bin/setsid -> busybox`), the one `03` § 3.4 reasons about.
- **The panel size.** `vm-pair`'s guests run at 1280x800, and the plan did not name a resolution. The first walk run (4 walks, `walks-1280x800-stopped.out`) was stopped by its PIDs at 10:11:51. Guest a was stopped by its pidfile and relaunched at 10:12:12 on the same disk with `generic-x64-vm run --res 640x480` and `vm-pair`'s own arguments (`relaunch-640.out`; the guest's first DRM mode reads `640x480`). Every frame cited below is 640x480. `vm-pair` taking a resolution is #1141.
- **The walks at 640x480**, five passing and the transfer walks not (#1141) (`tools/vm-qa --skip-up --only walks`, `walks.out`, frames under `/workspace/tmp/m6-t18/artifacts/rocknix-images/qa-069fc27044-webdav-a-20261026-1012/`):

  | Walk | Frames | The strings read back from the frames |
  | --- | ---: | --- |
  | `to-manage-cloud-storage` | 1 | CLOUD; BACKUP AND RESTORE; BACK UP TO THE CLOUD; RESTORE FROM THE CLOUD; MATCH THIS DEVICE TO THE CLOUD; SAVE MANAGEMENT; CONNECTED TO ... WEBDAV (`GuiMenu.cpp`'s page, a caller's) |
  | `restore-page` | 2 | RESTORE FROM THE CLOUD; WHAT WOULD YOU LIKE TO RESTORE?; SAVES / GAME SAVES, SAVE STATES, AND SCREENSHOTS; ROMS AND BIOS; GAME CONTENT; SETTINGS / NO SETTINGS BACKUP FROM THIS DEVICE YET (the scan page went on by itself: `setAutoContinue`) |
  | `match-dialog` | 4 | the confirmation (`GuiMenu.cpp`'s); then **this slice's done page**: MATCHING THIS DEVICE TO THE CLOUD / COMPLETED / REMOVED 1 FILE FROM THIS DEVICE · 4 KB / **GB 1 FILE · 4 KB   SNES 0 FILES** / UPDATE GAMELISTS UNDER GAME SETTINGS TO SEE THE CHANGE. / ELAPSED 0:00 / PRESS ANY BUTTON TO CLOSE; help bar CLOSE. Every line fits at 640x480 (F-20) |
  | `to-change-cloud-folder` | 3 | `GuiMenu.cpp`'s folder pages |
  | `confirm-cloud-folder` | 5 | `GuiMenu.cpp`'s folder pages |
  | `run-transfer-frames` | 1 | **exit 3**: `key up` at its line 21 was eaten twice, and the walk ended on a game list (`01-stuck-after-up.png`). The transfer walks' key counts do not hold at 640x480: a harness gap, not a finding against the eight (#1141) |
  | `run-transfer` | -- | not run: stopped by its PID at 10:19:09, before it began, for the time the rest needed (#1141) |

- **F-08's before-frame: `CANNOT`.** `guest-cycle/f08-cancel-match.steps` confirms a match and presses back while it runs. On this fixture a match finishes at ELAPSED 0:00, and the second attempt had nothing left to match, so the press landed on the hub (`f08.out`, `/workspace/tmp/m6-t18/f08/`). The dialog's words stand on the code (`GuiCloudTransfer.cpp:357-358`) and the binary's strings (1 hit).
- **F-09's frame: `CANNOT`.** The transfer walk that would end on a back up with nothing new did not reach the page at 640x480.
- **The card during a sync is framed at 640x480** by `time-to-play`'s exit cell against the QA WebDAV (`frames/640-ttp-r1-exit-001.png`, `-004`, `-012`). It reads `SYNCING SAVES TO THE CLOUD` / `STARTING...` as it fades in, then `SYNC SAVES` / `COMPLETED` with a full bar, and is gone by the twelfth frame. Both lines fit with room to spare. **The page's live line during a transfer: `CANNOT`**: the transfer walks did not run at 640x480 (#1141).
- **The fit of the candidate lists:** the match's done page fits every line. The card's running and outcome lines fit (`COMPLETED` is a one-candidate line). A failure's outcome and action candidates (the long `COULDN'T FINISH - <why>` forms), the transfer page's live rows and the scan sentence's `chooseThatFits` were **not** framed: no failure was provoked, and the transfer walks did not run. They remain owed (§ The strings).
- **`tools/time-to-play --vm --only launch,exit,g2g --repeat 3 --backend webdav`** (10:20:06 to 10:22:49 UTC, exit 0; `ttp.out`, `time-to-play.md`, `time-to-play.json`), seconds as median / mean / max over 3. The headline numbers are in bold:

  | Cell | Measure | Seconds |
  | --- | --- | --- |
  | UI to game | the game's first frame | **0.56** / 0.63 / 0.78 |
  | the exit sync | the `last-sync-exit` stamp | **1.58** / 1.62 / 1.71; outcomes completed x3, 628 KiB seeded |
  | the exit sync | the card gone from the screen | 4.01 / 4.01 / 4.01 |
  | game to game, the exit sync in flight | the next game's first frame | **1.01** / 1.01 / 1.01 |
  | game to game | the question answered (STOP IT AND PLAY) | 1.34 / 1.33 / 1.34 |

  - The exit sync reaches a cloud here, which T2's run on the same image did not ("Not a pass: the exit sync had no cloud to reach").
  - Its stamp at 1.58 s is inside D-CLOUD-119's 3 s.
  - The card's 4.01 s is the stamp plus the 1.5 s linger of a completed run (`ThreadedCloudSync.cpp:731`) plus the fade.
  - The report's last line reads the sync's token as `?` x3 for the game-to-game cell: the launch's answer leaves no stamp the tool can read in its window. That line is the tool's own.
- **The leftover check** (`down.out`, 10:23:08 UTC): qemu 0; listeners on 9010-9099 and 10022-10023, 0; `rclone serve` 0; the backend's container 0. RETURN was posted at 10:23:21 UTC.
- **The disk, retired** (D-INFRA-022): `/workspace/tmp/m6-t18/vm-pair/vm-a.qcow2`, 2,334,785,536 bytes, sha256 `c24599965c6331f9d4d1bf88636a4d225ed6861fee503ab24c130957880514a9`, removed with its directory at 10:23 UTC. The hash is provenance: it makes no claim that the file still exists. The frames this section cites are kept in `guest-cycle/frames/`.

## Findings index

Each is graded in `04` (severity, class, `question:`, the `proved:` a fix would need):

| ID | Q | One line | Where |
| --- | --- | --- | --- |
| F-01 | Q3a | both readers take every `>>> pid` line; a second would redirect the stop, and `>>> pid 1` signals every process (latent: only the wrappers print one) | `CloudTransferJob.cpp:272-279`, `ThreadedCloudSync.cpp:254-256` |
| F-02 | Q3a | the card's wrapper has no `trap '' PIPE`: its scripts die at their next write when the interface goes, before their stamp | `ThreadedCloudSync.cpp:206-207` against `CloudTransferJob.cpp:636-637` |
| F-03 | Q3a | an unknown marker is dropped silently by both readers (blindspot 22's shape: no log line) | `CloudTransferJob.cpp:399-403`, `ThreadedCloudSync.cpp:330-332` |
| F-04 | Q3a | the card's `fgets` into 512 bytes splits a longer line; the job's reader caps at 1,024 | `ThreadedCloudSync.cpp:211-212` |
| F-05 | Q3a | the `%3d` separator and the job's glued splitter have no unit case | `CloudTransferJob.cpp:529-551`, `:654-677` |
| F-06 | Q3b | `writeStamp` renames an unchecked write over the good stamp; `Utils::AtomicFile::writeText` exists and is tested here | `ThreadedCloudSync.cpp:930-949` |
| F-07 | Q3b, Q5 | `cancelForLaunch` spins up to 2 s on the interface thread; at 1.5 s the player sees a still frame | `ThreadedCloudSync.cpp:834-863`, `FileData.cpp:1001` |
| F-08 | Q3c | the CANCEL confirmation over a match promises that the next backup or restore finishes it | `GuiCloudTransfer.cpp:357-358` |
| F-09 | Q3c | `NOTHING NEW TO BRING DOWN` / `TO SEND UP` paraphrase the two verbs, on the panel where they show | `GuiCloudTransfer.cpp:807-808` |
| F-10 | Q3c | `ITEM(S) DID NOT FINISH` in the formal register; `CAME DOWN` a third verb | `GuiCloudTransfer.cpp:745`, `:769` |
| F-11 | Q3c | the why table lacks two script sentences; backuptool's reaches line 4 in English | `CloudText.cpp:414-466`; `backuptool:1495`, `cloud_setup:797` |
| F-12 | Q2, Q7 | the comment says a test fails on a missing why; the test's table is typed and reads no script | `CloudText.cpp:419-422`, `CloudTextTests.cpp:632-721` |
| F-13 | Q7 | comments that describe an older code: the fallback map's words, `SKIPPED - A GAME WAS STARTED`, the token list, `COMPLETED WITH GAPS`, "four words", the translation contract, `shortenWhy`'s two shapes, "Pid is the card's", the leavable page | `ThreadedCloudSync.h:70`, `:93-99`, `:126-130`, `:158-159`; `ThreadedCloudSync.cpp:73`, `:460`; `CloudText.h:9-18`, `:78-82`, `:164-170`; `CloudText.cpp:298`; `CloudTransferJob.cpp:399-403`; `GuiCloudTransfer.h:156-157` |
| F-14 | Q7 | the rule's Outcome vocabulary names older words for 3/4 and 7/8, and its SKIPPED table lacks NoFolder and YOU CANCELLED IT (#909's half) | `.claude/rules/es-player-text.md` § Outcome vocabulary |
| F-15 | Q7 | exit 75 has eight wordings | § The why table |
| F-16 | Q6 | what the retired folder move (#353) and folder step (#363) left: three `doing` words and their strings, the `DISCARDED SAVES` label, one why row, `setFailedNote`, `setDismissedAction`, the `cancellable` parameter, and the comments naming them | `CloudTransferJob.cpp:235-236`, `:387-389`; `GuiCloudTransfer.cpp:1027-1032`; `GuiCloudTransfer.h:76-100`; `CloudText.cpp:429`, `:1104-1108` |
| F-17 | Q6 | `nextTime` has no product caller; `isKnownWhy` and `isKnownUnitLabel` are test-only | `CloudText.h:187-189`, `:468-469`, `:529-531` |
| F-18 | Q1 | two readers act on one protocol in two shapes (the wrappers, the pid, what each drops, the launch's two waits): the seam a shared reader would close | § The protocol |
| F-19 | Q2, Q3b | the job's stop races are tested only by `tests/app-unit`'s `jobs-tests`, which no lane's standing commands build; built and run here on the coordinator's 10:02 yes: 6 cases PASS under ASan and UBSan | `tests/app-unit/JobsTests.cpp:130-205` |
| F-20 | Q3c | the match's done page names a system nothing was removed from (`SNES 0 FILES`, framed at 640x480): every per-system item of `>>> removed` is shown, a zero included | `CloudTransferJob.cpp:343-349`; the 640x480 frame `match-dialog/04-match-done.png` |

**A lead outside the slice** (T17's file; taken by the coordinator as Backlog **#1140** under #1047 at 10:02 UTC, not graded here): `cloud_content_transfer:113-114` traps `INT` with `exit 130` and `TERM` with `exit 143`. The page's CANCEL and the launch stop send SIGTERM, and a stop's restamp reads only 130 (`CloudText.cpp:216`). Whether a content part's stamp is left at 143 depends on the calling script's own trap, which this slice did not read.

## Positives

- **One parser for two readers**, with a test that every emitter's shape classifies (`CloudTextTests.cpp:632`). The #145 lesson holds in the code.
- **A stop is a request the run keeps** (`CloudTransferJob.cpp:129-162`): the stop and the reader both call `deliverStop`, and the race with a finishing run is closed under the run's lock (`:79-106`). `jobs-tests` covers each.
- **The stamp is written before the card speaks** (`ThreadedCloudSync.cpp:555-566`). A stop restamps only the part it interrupted, by the file's identity and not the clock (`CloudText.cpp:199-235`, `ThreadedCloudSync.cpp:894-927`).
- **The page's posted step cannot reach a deleted page** (`GuiCloudTransfer.cpp:1068-1075`), and it copies what it needs before `delete this` (`:205`, `:296-322`).
- **No `Utils::FileSystem::exists` in the eight** (r11): the stamps go through `stat` (`ThreadedCloudSync.cpp:902`).
- **A bar only where a number exists** (`GuiCloudTransfer.cpp:555-569`, `CloudTransferJob.cpp:598-605`); the card's bar moves forward only within a half (`CloudText::forwardOnly`).
- **The help bar by role, never by letter** (`:373-392`, `:902-912`).
- **Every fork string of the eight has French** (r23).
- **The unit tests fail closed** without rapidjson (`CMakeLists.txt:72-74`; the generator stops the same way, exit 2). They pass on a host with no `cmake`: 221 of 221.
- **No secret-shaped literal at rest** in the 22 test files.

## Proofs

| Proof | What | proved |
| --- | --- | --- |
| P1 | the membership: 30 paths, 11,193 lines, none in the merge base (r01, r02, r03, r05) | proved: tree |
| P2 | the pin and its base: `bccd715707` = `upstream/master`, 725 ahead, 0 behind (r04) | proved: history |
| P3 | the history: 181 commits by three identities (r16) | proved: history |
| P4 | the callers outside the eight (r17) | proved: tree |
| P5 | the unit tests built from `CMakeLists.txt`'s lists and run: 221 PASS (r20) | proved: unit-test |
| P6 | the branch at the pin and nothing under `packages`/`projects`/`tools` (r25) | proved: tree |
| P7 | the protocol table generated, 18 rows, counts asserted (`tools/t18-protocol-table.py`, exit 0) | proved: tree |
| P8 | the protocol generator fails on a drifted tree: against `651150fc88`, exit 1, `` `>>> doing` scripts=0 (expected 6); `>>> offer` scripts=0 (expected 3); `>>> removed` scripts=0 (expected 3) `` | proved: fixture |
| P9 | the why generator fails on a drifted tree: against `651150fc88`, exit 1, `literal=0, shared_literal=0, script_only=0, es_only_literal=38, variable_lines=0, es_only_unproduced=38, lock_held_wordings=7` | proved: fixture |
| P10 | the why table generated, eight counts and the fallback map asserted (`tools/t18-why-table.py`, exit 0) | proved: tree |
| P11 | no secret-shaped literal in the 22 test files: 0 hits; the control line 1 | proved: fixture |
| P12 | `nextTime`, `isKnownWhy` and `isKnownUnitLabel` have no caller in `es-app/src` or `es-core/src` outside `CloudText.cpp` (`git grep -w` per declaration of the 47) | proved: tree |
| P13 | `setFailedNote` and `setDismissedAction` have no caller; `setCompletedAction`'s one caller passes no `cancellable` (`GuiMenu.cpp:5083-5096`) | proved: tree |
| P14 | `doing copy`/`verify`/`remove` and the `DISCARDED SAVES` unit have no producer at `8ebaf8daad` or in `es-app/src` (`git grep`) | proved: tree |
| P15 | `cancelForLaunch` runs on the interface thread: its one call is inside the STOP IT AND PLAY callback (`FileData.cpp:996-1005`) | proved: tree |
| P16 | `writeStamp` checks no write: `Utils::FileSystem::writeAllText` is `void`, with `fwrite` and `fclose` unchecked (`es-core/src/utils/FileSystemUtil.cpp:1429-1446`), then `std::rename` (`ThreadedCloudSync.cpp:943-948`) | proved: tree |
| P17 | the installed EmulationStation carries the pin's strings: the identity literal and five more, 1 hit each (`guest-cycle/identity.out`) | proved: pin-binary |
| P18 | `jobs-tests` built from `tests/app-unit/CMakeLists.txt` and run: 6 cases PASS under ASan and UBSan (`stage-c/jobs-tests.out`) | proved: unit-test |
| P19 | the match's done page at 640x480 names `SNES 0 FILES` (F-20; `guest-cycle/frames/640-match-done.png`) | proved: pin-binary |
| P20 | the exit sync to the QA WebDAV stamps at 1.58 s median, completed 3 of 3; game to game 1.01 s (`guest-cycle/time-to-play.md`) | proved: pin-binary |
| P21 | the sync card at 640x480 during and after a sync: `SYNCING SAVES TO THE CLOUD` / `STARTING...`, then `SYNC SAVES` / `COMPLETED` (`guest-cycle/frames/640-ttp-r1-exit-*.png`) | proved: pin-binary |



## The first reader's 03-retrospective.md (whole)

# Retrospective audit — M6.P2 T18, EmulationStation's cloud pages, cards and text (#665)

What the 30 files are measured against: the four ES rules, the principles (least surprise, player language, time to play), engineering-practices.md, and the register rows the code cites. Findings are `02`'s F-nn.

## 3.1 Architectural coherence

- **Four pairs, three jobs, one text library.**
  - `CloudText` is pure: no file, no window, no font. It is tested, as es-code-traps.md § Pure text has a home asks.
  - The card (`ThreadedCloudSync`) runs automatic and manual saves syncs on the third surface tier.
  - The job (`CloudTransferJob`) runs a long transfer apart from its page, and the page (`GuiCloudTransfer`) is the fourth tier, sat in since D-UI-078.
  - The split is the rules' own, and a reader can tell which surface is which from the class comments.
- **One parser, two readers** (`CloudText::classifyProtocolLine`, #145) holds. The two readers still differ in five ways, each a small seam (F-18):
  - the wrapper's `trap '' PIPE` (F-02);
  - the read loop: `fgets` 512 against a character loop with a 1,024 cap (F-04);
  - what each drops (the card drops `unit` and `removed`);
  - how each takes a pid (both from every line, F-01);
  - how the launch waits for each: the card in a spin on the interface thread, the job behind a spinner (F-07).
- **The retired folder move left its seams in the page** (F-16): three `doing` words and their strings, a label, two setters with no caller, a parameter never passed, and comments describing the move as present. D-CLOUD-175 (#508) retired the flow; the page kept the hooks it was built with. That is register-check's P-01 shape (a reversal leaves its old words behind), applied to code.
- **The text library holds more than cloud text.** The offline proxy's stamps (`parseScanStamp`, `parseRunningProgress`, `parseFlushStamp`, `scanWhy`), the folder refusals, and the settings archive's name share `CloudText.cpp`'s 1,409 lines. They have their tests beside them. A split by subject is a Q1 proposal, not a defect.

## 3.2 Project conformance

| Rule | Held | Where it does not |
| --- | --- | --- |
| es-native-ui.md, the four surface tiers | the card is third tier (0.9W, top, ends when the work does, then lingers); the page is fourth (owns the screen until dismissed; CANCEL the one way out) | -- |
| es-native-ui.md, "one floating surface at a time" | the card is created through `Window`'s queue (`createAsyncNotificationComponent`) | -- |
| es-native-ui.md, "a file another process writes is read uncached" | no `exists()` in the eight; stamps through `stat` (r11) | -- |
| es-ui-style-guide.md § Confirmations | YES first, NO last, back answers NO (`GuiCloudTransfer.cpp:354-360`) | the match's text (F-08) |
| es-ui-style-guide.md § Interaction rules | buttons by role on the help bar (`:373-392`) | -- |
| es-player-text.md § Outcome vocabulary | three words; a why; what is in place; how to recover | the why table's two missing rows (F-11); the rule's own half (F-14, #909) |
| es-player-text.md § Conventions, player-language.md | the four tiers, the two verbs, Wi-Fi, the serial comma | `BRING DOWN`, `SEND UP`, `CAME DOWN` (F-09, F-10); `DID NOT` (F-10) |
| es-code-traps.md § rclone's piped progress | the glued line, the 80-column cut, U+2026, the `%3d` separator are all handled | the `%3d` separator and the job's splitter untested (F-05) |
| es-code-traps.md § Comments near a translatable string | 0 non-ASCII comment lines (r15) | -- |
| engineering-practices.md § Guards must fail closed | a stop needs a positive pid (`pid <= 0` never signals); a tier code that is not a number is not a success (`CloudText.cpp:594-597`) | `writeStamp` proceeds past a write it never checked (F-06); a comment claims a guard the test does not have (F-12) |
| engineering-practices.md § the last known good state (D-CLOUD-078) | temp and rename | the temp is never checked before the rename (F-06) |
| least-surprise.md | the same outcome words on the card and the page | exit 75 in eight wordings (F-15) |
| time-to-play.md | the exit sync bounded; the card lingers 1.5 s on success | the 2 s spin on the interface thread (F-07) |

## 3.3 Spec fidelity

- **D-UI-078 (the page sat in, CANCEL the way out):** held (`GuiCloudTransfer.cpp:246-260`). The leavable page's seams (`rowWords`, `stillRunningSentence`, the card's refusal) stay, as the header says, for a run current between its end and its dismissal.
- **D-UI-028 / D-UI-030 (three words):** held in the code. The comments still say "four" in five places (F-13).
- **D-CLOUD-077 (fail gracefully):**
  - Held: the in-place clauses, the retry on the reporting surface, a bounded run.
  - Not held: the stamp writer can leave a truncated stamp (F-06).
  - Against the words: the match's CANCEL dialog promises a recovery the backend refuses (F-08).
- **D-CLOUD-129 / D-CLOUD-130 (the launch question, STOP IT AND PLAY / KEEP WAITING):**
  - Held: the card's cancel honours the player's answer (`evenIfPlayerStarted`), and the job's stop is marked under the run's lock.
  - D-CLOUD-109's "bounded and visible" wait is bounded (2 s) but not visible while it spins (F-07).
- **D-UI-035 (candidates, longest first):** held for the outcome line, the action line, the live line and the scan sentence. Their fit at 640x480 is owed to the window.
- **D-UI-108 (a transfer says which file of how many):** held (`ThreadedCloudSync.cpp:396-427`).
- **D-CLOUD-175 (no automatic folder migration):** no automatic flow remains reachable from the eight, but the move's hooks remain (F-16).
- **D-UI-117 (`backuptool`'s proposed sentence):** the script prints it; the interface does not know it (F-11).

## 3.4 Platform conformance

- **Every command runs under `setsid sh -c` through `popen`.** The `popen` child is not a process group leader, so `setsid` does not fork, and the command's exit status reaches `pclose`. The design holds on busybox and util-linux alike. The guest's `setsid` is the image's, and the window reads it.
- **The stamps are written to `/storage/.cache/cloud_sync/`**, device-local, as the class comment says. `Utils::FileSystem::writeAllText` is `fopen`/`fwrite`/`fclose` with no check (F-06).
- **The card measures in the row's font on the interface thread** (`AsyncNotificationComponent`), and the page measures in its own fonts. Neither measures on the worker. The host has no font, so every fit is a frame.

## 3.5 Cross-system interaction audit

### Interaction: the cloud scripts (T16, T17) x the two readers

The protocol is the contract (§ The protocol). At `8ebaf8daad` the generator finds six `doing` lines, three offers, eleven `unit` lines and three `removed` lines in the scripts, and its `why` pattern matches 109 script lines (the emitters and the functions that wrap them). Every one classifies: the emitter table test holds that for the shapes it lists. Three ways the two sides drift apart unseen:

- **a new `>>> why`** passes the test (F-12) and shows in English (F-11);
- **a new marker** is dropped silently (F-03);
- **a script that ever printed `>>> pid`** would redirect a stop (F-01).

### Interaction: the card x the script stamps under a lost interface

When EmulationStation restarts under a card's run, its scripts die of SIGPIPE at their next write (F-02). The job's survive and stamp. Neither the card's own `last-sync-<origin>` stamp nor the scripts' stamp says what happened to that run; the row then reads the run before it. The next sync completes what the dead one did not (rclone's rename on completion).

### Interaction: the page x `backuptool` (T17's S7, #1136)

`backuptool restore`'s output reaches the settings-restore page (`GuiMenu.cpp:5043-5045`), so its `>>> why` lines are the page's line 4. The one sentence the why table lacks is the one #1136's fix area prints (F-11). T17's streams did not change the sentence, which is at `8ebaf8daad` and therefore inherited.

### Interaction: the card x the launch gate (T2's `FileData.cpp`)

`cancelForLaunch` runs inside the STOP IT AND PLAY callback (`FileData.cpp:996-1005`), on the interface thread, for up to 2 s. Past it, `launchWhenGone` shows a spinner; the transfer's question goes to `launchWhenGone` at once (`:1012-1020`). T2's audit (`feature/m6-es-launch-path-649`, `02` § the launch's question over a sync) owns the caller; this slice owns the 2 s spin (F-07).

### Interaction: the page x `SystemData::rescanChangedFolders`

The page posts the rescan after a restore (`GuiCloudTransfer.cpp:335`) and captures nothing. The rescan's own holders (#246's `dropGameListView`/`remakeGameListView`, `FolderMergeTests`) are SystemData's, another slice's. Nothing of this page is held across it.

### Interaction: the card x `ProxyCards` (the offline achievements' cards)

The card hands on to `ProxyCards::afterSync` after an automatic sync that reached the network (`ThreadedCloudSync.cpp:754-755`), after its own `delete this` is decided but before it runs. `ProxyCards` takes the window, not the card. `tests/app-unit/ProxyCardsTests.cpp` doubles the card (not run here).

### Interaction: M7's open work on these files

None of the 21 `m7` refs in the ES repository carries a commit on the 30 beyond the pin (`git rev-list --count --no-merges <pin>..<ref> -- <the 30>`: 0 for each); M7's October work on them is in the pin's history. The image the window would boot, `069fc2704421`, is built from M7's `build/m7-signin-20261022-07` (T2's record); its ES commit is not in this repository, so the window identifies the binary by the literal (§ The guest cycle).



## The first reader's 04-analysis.md (whole)

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

**Proposed for stage D: four bugs**, all Low (§ Q3), and fifteen renovation items. The coordinator disposes.

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

*(Written after the seats: the packet, the plan, each seat's items graded.)*

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
- **The 2 s budget against D-CLOUD-119's 3 s:** inside it. But the spin runs on the interface thread (F-07), so no frame is drawn while it spins: at 1.5 s the player sees the frame the dialog left.
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
- **Test cases whose subject is gone:** none found. Every case's function exists at the pin.

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



## Context 1: docs/reviews/order.md § T18

```text
### T18. interface: EmulationStation's cloud pages, cards and text, with their unit tests

- **id**: `es-cloud-pages`; **kind**: read; **lens**: brittleness, new functionality
- **why here**: 36 interface files name the cloud scripts (cross-reference.md); the cards, the transfer page and the text rules are the fork's; the unit tests ride here because most test `CloudText`; a test of a T2 or achievements subject is read with it as context
- **paths** (30 paths, 11,193 lines, 11,116 read, of which 11,116 fork-own; 0 patch and config lines; reach shipped 30): areas `interface`; globs `es:es-app/src/{CloudText,ThreadedCloudSync,CloudTransferJob}.*`, `es:es-app/src/guis/GuiCloud*`, `es:es-app/tests/**`
- **read before**: none
- **depth**: Extended -- `ThreadedCloudSync` and `CloudTransferJob` are on the state list: the cloud sync's ES half (plan § 6c)
- **interacting subsystems** (read-only context): the cloud scripts (`cloud-sync-core`, `cloud-setup-content`); `FileData::launchGame`, which asks over a running sync (`es-launch-path`); `AtomicFileUtil` and `Settings` (`es-state-and-bridge`); `es-player-text.md` and `es-ui-style-guide.md`
- **closing evidence**: audit folder, lint PASS, `es-unit-tests` and `tools/es-syntax-check`, frames for any visible change, punch list through Phase 7

```


## Context 2: the brief's § 4

```text
## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a proof
in `02` (a `proved:` cell: `tree`, `history`, `fixture`, `unit-test`,
`pin-binary`, `design`); the lens is brittleness and new functionality, so
Q3 and Q2 lead and Q6 is small:

- **Q3 Bugs -- the lead question, in three families.** **(a) The protocol
  under a pipe.** Every line the job and the card read comes through `popen` from a `setsid sh -c` wrapper: the job's wrapper sets `trap '' PIPE` (`CloudTransferJob.cpp:636-638`) and the card's does not (`ThreadedCloudSync.cpp:206-208`) -- what happens to each when ES closes the
  pipe early (a cancel, a quit)? `classifyProtocolLine` knows seven
  markers: what does a `>>>` line it does not know become -- a why, a
  live line, nothing (blindspot 22)? The rclone parsing (`CloudTransferJob.cpp:475-531`):
  the 80-column cut, the glued block, the `%3d%%` separator, the U+2026
  shortening (`es-code-traps.md` § What rclone's piped progress actually
  looks like) -- each with a fixture line through the real parser
  (`CloudTextTests.cpp` has cases; name which trap each covers and which
  has none). **(b) Lifetimes and threads.** The job outlives the page by design (`CloudTransferJob.h`'s comment); the page `delete this` at `:207` and `:328` and posts `[page, alive]` at `:1070`; the card detaches its thread (`:56`) and deletes itself (`:757`) after a linger (`:731`); `cancelForLaunch`
  (`:784-862`) spins at 20 ms under `sInstanceLock` with a 2 s budget and
  SIGKILLs at 1.5 s -- against D-CLOUD-119's 3 s exit budget and
  D-CLOUD-109's bounded wait, is the budget the right one, and what does
  the player see at 1.5 s? `SystemData::rescanChangedFolders` posted from
  the page's callback at `:335` (#246's shape: who holds a pointer to what
  it deletes?). A test of each lifetime exists in `tests/app-unit/`
  (`fakes/ThreadedCloudSync.h`) or does not: say which. **(c) The words.**
  Every `_( )` string of the eight files (220) against `es-player-text.md`:
  the three outcome words, the why sentences, the in-place clauses, TRY
  AGAIN by position never by letter, the serial comma, *back up* / *backup*,
  Wi-Fi; `outcomeCandidates` (`ThreadedCloudSync.cpp:700`, D-UI-035) and
  every `chooseThatFits` / `sizeText` fit at 640x480 (a frame from the guest
  is the proof; `GuiCloudTransfer.cpp:74`'s `setSize(w, 0)` is the padded
  width trap); the why table against the scripts (§ 2: the rows it lacks,
  the three wordings for 75, the eight variable emitters re-derived); the
  header comment at `ThreadedCloudSync.h:94-96` against the code; the nine
  non-ASCII lines in `GuiCloudTransfer.cpp` and one each in
  `CloudTransferJob.{cpp,h}` -- string literals or comments near a `_( )`
  (the xgettext trap; `ThreadedCloudSync.cpp:167`'s `"\xC2\xB7"` escape is
  the pattern). **Each bug carries its trace, its `Already written:` line
  (a stamp an older card wrote in another shape; a `rclone.conf` or conf
  the page reads; a setting the wizard saved) and its VM line**; a fix is a
  stream on the ES branch, proven by `es-unit-tests` where the code is pure
  and by a frame at 640x480 where it draws, and reaches an image only when
  the coordinator moves the pin.
- **Q2 Standards.** The ES rules as a checklist over the eight files: the
  four surface tiers and which each surface is (`es-native-ui.md`); the
  confirmation shape and the back-button accelerator (`es-ui-style-guide.md`
  § Confirmations: the page's CANCEL confirm); `getHelpPrompts` accurate on
  every state; the three type sizes; `Utils::FileSystem::exists` nowhere in
  the eight (the digest: 0 calls -- the stamps go through `stat`), with the
  callers' `exists()` reads named as T26's; the `>>> why` sentences in
  English and French (`tools/es-untranslated` over the pin; the French
  catalog's rows for the 38); the unit tests' own standards (`CMakeLists.txt`
  fails closed without rapidjson; a fixture never carries a secret-shaped
  literal, #1061).
- **Q1 Modernize.** `CloudText` is the shape the rules ask for (pure code,
  tested); the card and the job parse the same protocol with two readers
  (`ThreadedCloudSync::run` and `CloudTransferJob::handleLine`): name the
  seam and what a shared reader would change, as a proposal. The two
  `popen` wrappers differing by a `trap` is the smallest version of the
  same question.
- **Q4 Currency.** The pin against ROCKNIX's `upstream/master` (the merge
  base is its tip; nothing upstream touches these files); M7's October
  commits on these files beyond the pin (`c8dc72cf9` and after on the
  `m7-*` branches: cited by number, never read); T17's S6 and S5 changing
  what the scripts print and exit (routed on #665); the ES syntax check's
  default root naming the legacy layout (#640).
- **Q5 Efficiency.** The two time-to-play numbers (`time-to-play.md`,
  D-CLOUD-098): the exit sync's card and `cancelForLaunch`'s 2 s budget
  against D-CLOUD-119's 3 s; `tools/time-to-play --vm` on the guest if the
  window allows, else `docs/vm-qa-log.md`'s last medians cited; the 20 ms
  spin and the 1.5 s / 5 s lingers as the costs they are.
- **Q6 Dead ends.** Functions of `CloudText.h` no caller in `es-app/src`
  reaches and no test names (the 40 declared against `git grep -w` over
  `es-app/src` and the tests); a `>>>` marker parsed and never produced by
  any script (`>>> tier` is GuiMenu's composition; `>>> offer` read by
  both); test cases whose subject is gone. Removals none: a dead function is
  a proposal on the punch list for the coordinator.
- **Q7 Clarity and structure.** Can a reader tell, from the four pairs of
  files and the rules, which surface shows a sync (the card) and which a
  transfer (the page), which words each may use, what each parses, and how
  each ends? The protocol table (§ 6) and the why table are the test; the
  rule's drift (#909) and the header comment's are cited where they
  mislead.

A finding is one question with its evidence; `Renovation` is the category
for everything here that is not a defect. The seats grade the findings and
the dispositions; each seat's probe comes first.

```


## Context 3: the register rows

```text
| D-CLOUD-077 | 2026-09-10 | **Failure is acceptable; hanging, lying, and stranding are not. Every cloud operation does what it can, leaves the last known good state in place when it cannot finish, tells the player in plain words what did not happen and how to recover, and offers the retry in reach.** Maintainer: *"I think failure is okay. We just need to make sure that we degrade gracefully. If something fails, we need to have a recovery process and a user notification process. It's easy to say, 'We weren't able to upload. Please try again.' Our standard posture might have to be that we do what we can. If we sense a failure, we then revert to the last known good state and let the user try again by messaging them."* Consequences: no outcome line names a log path or an exit code (`FAILED - SEE /var/log/cloud_sync.log` goes); a failed run says what is and is not in place (rclone's per-file rename means a cut copy leaves the old file, so "what did arrive is in place, the rest is as it was"); the page that reported the failure carries the retry (a button on the done page, the row that runs it on the card's outcome); a partial success is reported as one, never as FAILED and never as COMPLETED. Applies to the transfer page, the sync card, the wizard, the picker (a scan that fails must say so, not show an empty cloud), restore and backup of settings, and the scripts' own messages. Audit and rewording: #105. | #105; D-CLOUD-075 (bounded), D-UI-024/026 (the page), D-CLOUD-053 |

| D-UI-028 | 2026-09-10 | **Four outcome words for every cloud surface, then a why, what is in place, and how to recover.** `COMPLETED`; `COMPLETED WITH GAPS - <what>` (some of the run succeeded and some did not -- never reported as FAILED and never as COMPLETED, D-CLOUD-077); `COULDN'T FINISH - <why>` (nothing succeeded and it is not a sentinel); `SKIPPED - <reason>` only for the two sentinels (`NO NETWORK CONNECTION`, `ANOTHER CLOUD SYNC IS RUNNING`) and the launch cancel (`A GAME WAS STARTED`). The why comes from a `>>> why <sentence>` protocol line the scripts print at the failure point (rclone's taxonomy stays in the log), else from a small rc table; the in-place clause is one per verb (`WHAT WAS SENT IS IN YOUR CLOUD. THE REST IS STILL ON THIS DEVICE.`, `NOTHING ARRIVED. THIS DEVICE IS AS IT WAS.`); the recovery clause names the surface that retries (`TRY AGAIN`, or the row). `COMPLETED SUCCESSFULLY`, `SUCCEEDED`, bare `FAILED`, `STOPPED`, every log path and exit code retire from the screen. The card uses its action line for in-place + recovery; the transfer page keeps its seven fitted lines (D-UI-024) and gains `A TRY AGAIN  B CLOSE` on line 7 when the run did not complete. The row line under a toggle reads the same words with commas. Stamps gain a third field, the why token, additively. Register-of-record: the vocabulary table in `es-native-ui.md`. Fork resolved from the EmulationStation audit's proposal (docs/audits/2026_09_10-graceful-degradation). | #105 |

| D-UI-030 | 2026-09-10 | **A cloud run passes or fails; `COMPLETED WITH GAPS` is removed from the vocabulary (reverses that part of D-UI-028).** Maintainer, on getting it from a manual sync: *"if you don't know what the gaps are, it's not very helpful for you and it just makes you more anxious and trust the system less because it's working kind of. You'd rather just know it couldn't connect or it could connect."* A run whose parts disagree reads `COULDN'T FINISH - <why>` with the failing part's why, on card, page and rows alike. What did move is still said truthfully -- the card's in-place clause, the page's line 4 -- so nobody is told nothing happened when something did. The stamps keep the `gaps` token so a log can still tell a partial run from a total one. ES `cdbe284a5`. | #111 |

| D-UI-031 | 2026-09-10 | **Player-facing cloud text is everyday language, not formal register.** Maintainer, on the card after a failed sync: *"the language ... was very awkward in saying something along the lines of everything is as it was. We should use more plain language, like, don't worry, nothing's changed"*, and *"more user-friendly and just generally customer-facing and not quite so jargony."* The three "as it was" clauses became `DON'T WORRY, NOTHING CHANGED.`; `NO NETWORK CONNECTION` became `YOU'RE NOT ONLINE`; and so on through the card, the page and the scripts' own sentences. What does not change: the three tiers, the two verbs, the outcome words, `Wi-Fi`, the serial comma, two lines per row -- this is register, not vocabulary. ES `4bab23fcb`. | #108; es-native-ui.md |

| D-UI-035 | 2026-09-10 | **A row that reports an outcome is composed from candidates, longest first, and the last candidate must fit any panel.** The card's action line already did this; the reason line was one string that clipped at ~70 characters on 640x480. Now `COULDN'T FINISH - <why> - <clause>` degrades to `COULDN'T FINISH - <why>` and then `COULDN'T FINISH`, measured in the row's own font on the interface thread. `460102b91`. | #115 |

| D-CLOUD-109 | 2026-09-12 | **A sync the player can see is a sync that happens: a launch never cancels an automatic sync, it waits for it. What makes the wait acceptable is that the sync bounds itself -- a total budget of a few seconds set from measurement (#135) -- and past that budget it ends with a connectivity outcome the player can act on ("Couldn't finish: your connection looks slow or down. Check your internet connection and speed."), the publish waits for the next pass, and the game starts. A sync never takes minutes; its network bounds are time-based, not retry-count based (which answers #113), and the checks that decide connectivity run first.** Supersedes D-CLOUD-076's cancel-on-launch for automatic syncs; refines D-CLOUD-038/072. Maintainer: "canceling the sync at launch is not what the user would expect. If they think a sync is happening, they think a sync is happening ... if we're seeing it take longer than X number of seconds, we assume bad connectivity and then say, 'There was a connectivity error. Check your internet connection and speed' ... the sync should never take minutes." | #134, #22, #135, #113 |

| D-CLOUD-129 | 2026-09-15 | **A launch over a sync the player pressed, or over a back up / restore / match left running from the transfer page, is a question, not a refusal: the sentence naming the run, what stopping means, then STOP IT AND PLAY or KEEP WAITING (B keeps waiting). Stop signals the run's process group, waits behind a spinner for it to be gone (the automatic cancel's wait, so no rename lands under a game that has the save open; SIGKILL at 5 s, gives up at 20 s), then launches; the run's outcome reads SKIPPED - YOU STARTED A GAME on the card and the transfer page, and the stopped manual backup's or restore's row reads SKIPPED, A GAME WAS STARTED (this process stamps the script's file with the cancel token). An automatic sync that was signalled for the launch and had not gone within the two-second budget is waited for behind the same spinner instead of a modal.** Maintainer, on meeting the modal on the RG SP: *"it told me it was stopping so I couldn't play. That seems less than ideal. We should say for the user, would you like to cancel and play, or would you like to stop the sync or continue ... we might as well give them the option as to whether they'd like to cancel or keep waiting."* Refines D-CLOUD-113 (the deliberate transfer no longer refuses; it asks) and D-CLOUD-109 (the wait, now with a spinner and a longer leash). | #203, ES `df4053f9f` |

| D-CLOUD-130 | 2026-09-16 | **Every sync or transfer a game launch would interrupt asks the same question -- STOP IT AND PLAY / KEEP WAITING -- the automatic startup and after-a-game syncs included; nothing is cancelled until the player answers.** Maintainer, having met the exit sync's stop: *"The case I ran into hasn't been changed, correct? When I ran into it, it was an auto-save on exit, and it didn't present me with an option. If we want consistent behavior on how user-started syncs or transfers deal with a potential interruption by a game launch, we should have a consistent behavior."* Reverses the silent cancel of #101 / D-CLOUD-109 for launches; refines D-CLOUD-129. | #203, ES `e21841060` |

| D-CLOUD-119 | 2026-09-12 | **Starting budgets: the exit sync of one changed battery save on a hashed cloud within 3 s (P-13; measured 0.8 s); an offline outcome within three times the online success, about 5 s (D-CLOUD-112; four of six offline shapes already meet it, the other two by D-CLOUD-118).** Same words from the maintainer as D-CLOUD-118; recorded as starting points to tweak on feedback. A run over budget fails the runner once the cell reports against these rows. | #135 |

| D-UI-078 | 2026-09-21 | **Long work runs on a foreground page that owns the screen until it ends; the only way out while it runs is CANCEL, which says what cancelling means for that job (start over, or resume where the job supports it); backgrounding is for fast work only.** Reverses the fourth-tier shape of D-UI-060 and D-UI-070 (#186 PL-07, #187, rule commit `0462cf0141`) for the offline-achievements scan, the cloud transfer page and the scraper; the other background cards (index, content installer, OS update, Bluetooth) are classified per surface in #241. Maintainer, on the RG35XX SP at the scan page's PRESS B TO KEEP SCANNING IN THE BACKGROUND: *"we should only allow things to run in the background when they're fast. If it's something that's going to take longer time, like scraping or doing the RetroAchievements offline work, we should force that to be on a foreground page."* And on the way out: *"We could add a cancel button if we want to give them the option of backing out. That way, they would know explicitly that they would have to start over or resume if we can support that. Backgrounding is tricky because there are more edge cases we're introducing for what has to happen in order for them to then finish it, surfacing an alert when it finishes, etc."* The background shape had no end signal: a scan left with B reported only on the row that launched it, which the player had to go and find. | #241, #236, #187, D-UI-060, D-UI-070, D-UI-028, D-CLOUD-129 |

| D-UI-117 | 2026-09-28 | **A settings archive with a member outside `storage/`, or with a `.` or `..` part, is refused before the copy, the mark or any extraction**, and the console says `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK, SO NOTHING WAS CHANGED. RESTORE SETTINGS FROM THE CLOUD AGAIN, OR BACK UP SETTINGS TO REPLACE IT.` Proposed words, built into the cut per `player-language.md` § How to apply; the maintainer approves them from the build (audit of the fix round PL-028 = G2-B-05 gpt, the blind pass's S-06; stream B `c1fbf658ab`). | #313 PL-028; D-UI-045 |

| D-CLOUD-175 | 2026-10-07 | **0.0.1 uses ordinary cloud linking, folder creation and explicit folder selection; retire the cloud-folder migration engine, automatic legacy joining/following, startup migration prompts and optional tidier. Fresh configurations default to `/pixelelated`; existing credentials and selected paths remain until explicitly changed. Users populate or rearrange their cloud folders themselves.** The maintainer says only their own installation has used the fork, raises multi-gigabyte ROMs and partially installed libraries, and says "I'm fine doing a rename on my end, and then we can abandon the migration entirely". This supersedes the move/follow/setup-step portions of D-CLOUD-158 through D-CLOUD-174 and D-UI-122 through D-UI-124; normal sync, selective transfer, defaults, stored-format guards and OS upgrade preservation remain. Historical correction: optional `/GAMES` to `/ROCKNIX` tidying was already included in the unmerged September 29 upstream PRs; automation came later. The owner's partially migrated Dropbox needs separately authorized host reconciliation, never an inferred rename/delete. | #508; supersedes #505's integration plan; ROCKNIX/distribution#3404 and ROCKNIX/emulationstation-next#40; source, UI, docs and focused VM sweep tracked by #508 |
```


## es-app/src/CloudTransferJob.cpp @ 16dbac5211 (whole, 751 lines)

```text
    1  #include "CloudTransferJob.h"
    2  
    3  #include "CloudExit.h"
    4  #include "CloudText.h"
    5  #include "ThreadedCloudSync.h"
    6  #include "LocaleES.h"
    7  #include "Log.h"
    8  #include "utils/FileSystemUtil.h"
    9  #include "utils/StringUtil.h"
   10  
   11  #include <algorithm>
   12  #include <cctype>
   13  #include <cstdio>
   14  #include <cstdlib>
   15  #include <thread>
   16  #include <signal.h>
   17  #include <sys/wait.h>
   18  
   19  std::mutex CloudTransferJob::sMutex;
   20  std::function<void()> CloudTransferJob::testPauseInStop;
   21  std::shared_ptr<CloudTransferJob> CloudTransferJob::sCurrent;
   22  
   23  // The run's starting state: every counter at its starting value. Once, at
   24  // construction -- a TRY AGAIN is a new run of the same command, not this
   25  // one reset under a page that might still be reading it.
   26  CloudTransferJob::CloudTransferJob(const std::string& command, const std::string& title, int itemsExpected, int itemsAfterContent)
   27  	: mCommand(command), mTitle(title),
   28  	  mItemsExpected(itemsExpected > 0 ? itemsExpected : 0), mItemsAfterContent(itemsAfterContent > 0 ? itemsAfterContent : 0),
   29  	  mStarted(std::chrono::steady_clock::now())
   30  {
   31  	mItemIndex = 0; mItemCount = mItemsExpected; mTrailing = mItemsAfterContent; mScriptBase = 0; mLastScriptIndex = 0;
   32  	mUnitBytes = 0; mUnitFiles = 0; mRunBytes = 0; mRunFiles = 0; mRunSized = false;
   33  	mRemovedFiles = 0; mRemovedBytes = 0; mAnyTransferred = false;
   34  	mFilesThisBlock = 0; mSeenBlock = false;
   35  	mChecksDone = 0; mChecksTotal = 0; mListed = 0; mChecksThisBlock = 0;
   36  	mBytePercent = -1; mFilePercent = -1; mCheckPercent = -1; mPercent = -1;
   37  	mFinished = false; mExit = -1;
   38  	mElapsedMs = 0; mFinishedAt = 0;
   39  	mStartedAt = time(nullptr);
   40  }
   41  
   42  std::shared_ptr<CloudTransferJob> CloudTransferJob::current()
   43  {
   44  	std::unique_lock<std::mutex> lock(sMutex);
   45  	return sCurrent;
   46  }
   47  
   48  bool CloudTransferJob::running()
   49  {
   50  	auto job = current();
   51  	return job != nullptr && !job->finished();
   52  }
   53  
   54  std::shared_ptr<CloudTransferJob> CloudTransferJob::start(const std::string& command, const std::string& title,
   55  	int itemsExpected, int itemsAfterContent)
   56  {
   57  	std::unique_lock<std::mutex> lock(sMutex);
   58  	if (sCurrent != nullptr && !sCurrent->finished())
   59  		return sCurrent;
   60  
   61  	std::shared_ptr<CloudTransferJob> job(new CloudTransferJob(command, title, itemsExpected, itemsAfterContent));
   62  	sCurrent = job;
   63  	// Detached, and holding its own reference: the run ends when the command
   64  	// does, not when a page closes -- the scan job's shape.
   65  	std::thread([job] { job->run(); }).detach();
   66  	return job;
   67  }
   68  
   69  // Only the run that was shown: a TRY AGAIN may have made the next run
   70  // current between the outcome and the press that dismissed it, and that
   71  // one is still somebody's to see.
   72  void CloudTransferJob::dismiss(const std::shared_ptr<CloudTransferJob>& job)
   73  {
   74  	std::unique_lock<std::mutex> lock(sMutex);
   75  	if (job != nullptr && sCurrent == job && job->finished())
   76  		sCurrent = nullptr;
   77  }
   78  
   79  // The look and the mark are one step (audit of the fixes, E2 gpt
   80  // G-E2-05): under the run's own lock, which its end holds while it
   81  // decides whether it was stopped and says it has finished. A stop that
   82  // looked, found the run going, and was descheduled while it finished on
   83  // its own used to mark a completed run stopped after the end had cleared
   84  // the flags; now the end waits for the mark, sees it with the command's
   85  // own 0, and says COMPLETED. The signal is sent under the lock too:
   86  // deliverStop takes nothing, and a kill does not block.
   87  bool CloudTransferJob::stopForLaunch(bool hard)
   88  {
   89  	auto job = current();
   90  	if (job == nullptr)
   91  		return false;
   92  	pid_t pid = 0;
   93  	{
   94  		std::unique_lock<std::mutex> lock(job->mMutex);
   95  		if (job->mFinished)
   96  			return false;
   97  		if (testPauseInStop)
   98  			testPauseInStop();
   99  		job->mStoppedForGame = true;
  100  		job->requestStop(hard ? SIGKILL : SIGTERM);
  101  		pid = job->mPid;
  102  	}
  103  	LOG(LogInfo) << "CloudTransferJob: stopped for a game (" << (hard ? "SIGKILL" : "SIGTERM") << ", group " << pid
  104  		<< (pid > 0 ? ")" : "; sent when the run says its pid)");
  105  	return true;
  106  }
  107  
  108  bool CloudTransferJob::stopByPlayer()
  109  {
  110  	auto job = current();
  111  	if (job == nullptr)
  112  		return false;
  113  	pid_t pid = 0;
  114  	{
  115  		std::unique_lock<std::mutex> lock(job->mMutex);
  116  		if (job->mFinished)
  117  			return false;
  118  		if (testPauseInStop)
  119  			testPauseInStop();
  120  		job->mStoppedByPlayer = true;
  121  		job->requestStop(SIGTERM);
  122  		pid = job->mPid;
  123  	}
  124  	LOG(LogInfo) << "CloudTransferJob: cancelled by the player (SIGTERM, group " << pid
  125  		<< (pid > 0 ? ")" : "; sent when the run says its pid)");
  126  	return true;
  127  }
  128  
  129  // A stop is a request the run keeps, not a signal sent once (#308
  130  // 5-cloud-sync-and-saves gpt F-CS-24, claude F-CS-26). The run's pid
  131  // arrives on its first line; a stop that came before it used to set the
  132  // flag and signal nothing, and the command ran to its end under a page
  133  // that then called it stopped. Now the stop and the reader both call
  134  // deliverStop, and whichever sees the request and the pid together sends
  135  // it: the stop sets the request before it reads the pid, the reader the
  136  // pid before it reads the request, so at least one of them sees both.
  137  // A SIGKILL replaces a SIGTERM that has not got through; nothing replaces
  138  // a SIGKILL.
  139  void CloudTransferJob::requestStop(int sig)
  140  {
  141  	if (sig == SIGKILL)
  142  		mStopSignal = SIGKILL;
  143  	else
  144  	{
  145  		int none = 0;
  146  		mStopSignal.compare_exchange_strong(none, sig);
  147  	}
  148  	deliverStop();
  149  }
  150  
  151  // Each signal once: the stop and the reader can both arrive here with the
  152  // same request, and the second finds it sent.
  153  void CloudTransferJob::deliverStop()
  154  {
  155  	const int sig = mStopSignal;
  156  	const pid_t pid = mPid;
  157  	if (sig == 0 || pid <= 0)
  158  		return;
  159  	if (mSignalSent.exchange(sig) == sig)
  160  		return;
  161  	::kill(-pid, sig);
  162  }
  163  
  164  bool CloudTransferJob::finished() const
  165  {
  166  	std::unique_lock<std::mutex> lock(mMutex);
  167  	return mFinished;
  168  }
  169  
  170  time_t CloudTransferJob::finishedAt() const
  171  {
  172  	std::unique_lock<std::mutex> lock(mMutex);
  173  	return mFinished ? mFinishedAt : 0;
  174  }
  175  
  176  int CloudTransferJob::elapsedMsLocked() const
  177  {
  178  	if (mFinished)
  179  		return mElapsedMs;
  180  	return (int) std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - mStarted).count();
  181  }
  182  
  183  // The unit's last "Transferred:" pair becomes the run's. Called with mMutex
  184  // held: at the next ">>> unit", when the command exits, and when the byte
  185  // counter drops -- rclone's never does within one invocation, so a drop
  186  // means a second one started inside the unit, and what the first moved is
  187  // banked before its numbers are replaced. A drop of the count line folds
  188  // the files alone, in handleLine: the byte line of the same block comes
  189  // first and has settled the bytes by then, and folding both again here
  190  // banked the new rclone's first bytes twice whenever the old one had moved
  191  // nothing but empty files (review, 2026-09-08).
  192  void CloudTransferJob::foldUnit()
  193  {
  194  	mRunBytes += mUnitBytes;
  195  	mRunFiles += mUnitFiles;
  196  	mUnitBytes = 0;
  197  	mUnitFiles = 0;
  198  }
  199  
  200  void CloudTransferJob::handleLine(const std::string& line)
  201  {
  202  	std::unique_lock<std::mutex> lock(mMutex);
  203  
  204  	// "Transferred:   \t 1.4 GiB / 2.0 GiB, 70%, 2.5 MiB/s, ETA 3m2s"
  205  	//
  206  	// It appears twice per block: once for bytes, once for the file count
  207  	// ("0 / 6, 0%"). The byte one is the one carrying a unit, which is also
  208  	// the one somebody wants -- a count of files says nothing about how long
  209  	// this will take when the files are a save game and a disc image.
  210  	//
  211  	// The scripts talk to this page through the ">>> " markers on stdout:
  212  	//
  213  	//   ">>> unit <label>|<i>|<n>" -- an item starts: a system ("nes|2|5")
  214  	//     or a phase ("SAVES||", "SETTINGS||"). Everything per-block is reset
  215  	//     with it; the label survives. The run numbers items across the
  216  	//     whole of itself (the page's row 2, ITEM i OF n; D-UI-026), because one run
  217  	//     chains several scripts and each counts only its own units: a label
  218  	//     that differs from the current one is the next item, the same label
  219  	//     again is a re-announcement and does not advance (ES announces
  220  	//     SETTINGS before backuptool runs, then cloud_backup announces it
  221  	//     again). The script's own i|n are read for one thing: an
  222  	//     announcement carrying n says how many units that script has, so
  223  	//     n = the items counted before that script's first announcement
  224  	//     + its n + the single-item phases ES chained after it (mTrailing).
  225  	//     Until a script says, n is ES's estimate from the constructor; 0 is
  226  	//     unknown and row 2 reads ITEM i alone. i never exceeds n on the
  227  	//     page. A script whose i starts over, or that carries a count after
  228  	//     one that did not, is a new script.
  229  	//   ">>> doing <keyword>" -- what the item is busy with while rclone is
  230  	//     not running yet. "archive": backuptool is writing the settings
  231  	//     archive (its own output is discarded), and row 3 says so until the
  232  	//     next per-file, checks or totals line, or the next unit. "unpack":
  233  	//     the same tool putting one back. "scan" and "compare": cloud_scan
  234  	//     checking the cloud and comparing its content (#350); "copy",
  235  	//     "verify", "remove": the folder move's three steps (#353). Any
  236  	//     other keyword is a newer script's and is ignored rather than
  237  	//     shown raw.
  238  	//   ">>> removed <files>|<bytes>|<per-system>" -- a match's summary, for
  239  	//     the done page (below). A match cut off by the network prints it
  240  	//     before exiting 69, so the page can say what had already gone.
  241  	//   ">>> why <sentence>" -- a script saying, at the point of failure and
  242  	//     in the player's words, what went wrong (D-UI-028). Attached to the
  243  	//     unit it arrived under; before any unit, to the tier that reports
  244  	//     next. The last one is the run's why for a command with no tiers.
  245  	//   ">>> tier <label>|<rc>" -- GuiMenu's run composition reporting each
  246  	//     of its parts as it ends (SAVES, ROMS AND BIOS, SETTINGS), so the
  247  	//     done page can say which finished and which did not.
  248  	//   ">>> offer <name>|<arg>|..." -- a question the script wants put to
  249  	//     the player, and cannot put itself. Kept until the page is
  250  	//     dismissed and raised then (input); the words are CloudOffer's,
  251  	//     shared with the card.
  252  	//
  253  	// Which line is which is CloudText::classifyProtocolLine -- the one
  254  	// parser both cloud surfaces read this protocol with -- and what each
  255  	// kind does to this page stays here.
  256  	//
  257  	// It used to be a second parser living in this function, which knew
  258  	// ">>> unit" and ">>> removed" and had never heard of ">>> offer": so
  259  	// the empty-cloud question (#100, #127) was put to the player by the
  260  	// card and not by this page, on the very route a freshly set-up
  261  	// handheld takes (#145).
  262  	//
  263  	// Nothing carrying ">>> " is rclone's, so nothing carrying ">>> "
  264  	// reaches the rclone parsers below -- a marker newer than this build
  265  	// included. It is dropped deliberately here rather than left to fall
  266  	// through to matchers that were never asked about it.
  267  	const CloudText::ProtocolLine protocol = CloudText::classifyProtocolLine(line);
  268  	if (protocol.kind != CloudText::ProtocolKind::NotProtocol)
  269  	{
  270  		switch (protocol.kind)
  271  		{
  272  		case CloudText::ProtocolKind::Pid:
  273  			// run()'s own first line: the group a stop signals -- and a
  274  			// stop that came before it is sent now (requestStop).
  275  			mPid = protocol.number;
  276  			if (mStopSignal != 0)
  277  				LOG(LogInfo) << "CloudTransferJob: the run said its pid (" << protocol.number << "); sending the stop that came before it";
  278  			deliverStop();
  279  			break;
  280  		case CloudText::ProtocolKind::Why:
  281  		{
  282  			// An empty why is a why line with nothing in it: the one this
  283  			// page already had stands, and no item is blamed for it.
  284  			if (protocol.text.empty())
  285  				break;
  286  			mWhy = protocol.text;
  287  			mPendingWhys.push_back({ Utils::String::toUpper(mUnitLabel), protocol.text });
  288  			break;
  289  		}
  290  		case CloudText::ProtocolKind::Tier:
  291  		{
  292  			Tier t;
  293  			t.label = protocol.text;
  294  			t.rc = protocol.number;
  295  			t.unitsAnnounced = (int) mUnitsSinceTier.size();
  296  			t.unitsFailed = 0;
  297  			t.tierLevelFail = false;
  298  			// A tier with no label is no tier: nothing is recorded, and the
  299  			// whys waiting under it stay waiting for one that has a name.
  300  			if (t.label.empty())
  301  				break;
  302  			const bool ok = t.rc == 0 || t.rc == 9;
  303  			if (!ok)
  304  			{
  305  				std::vector<std::string> named;
  306  				for (auto& w : mPendingWhys)
  307  				{
  308  					// A why printed before any unit is the tier's own; the tier
  309  					// as a whole is the item that did not finish.
  310  					const std::string label = w.label.empty() ? t.label : w.label;
  311  					if (w.label.empty())
  312  						t.tierLevelFail = true;
  313  					else if (std::find(named.begin(), named.end(), w.label) == named.end())
  314  						named.push_back(w.label);
  315  					// The last why for an item wins; the scripts may say more
  316  					// than one thing about the same unit as they give up on it.
  317  					bool seen = false;
  318  					for (auto& f : mFailed)
  319  						if (f.label == label) { f.why = w.why; seen = true; }
  320  					if (!seen)
  321  						mFailed.push_back({ label, w.why });
  322  				}
  323  				t.unitsFailed = (int) named.size();
  324  				// A part that failed without a word: the part is the item, and
  325  				// the code supplies the why. Its units are not presumed to have
  326  				// finished, because nothing said they did.
  327  				if (mPendingWhys.empty())
  328  				{
  329  					t.tierLevelFail = true;
  330  					mFailed.push_back({ t.label, ThreadedCloudSync::whyForCode(t.rc) });
  331  				}
  332  			}
  333  			mTiers.push_back(t);
  334  			mPendingWhys.clear();
  335  			mUnitsSinceTier.clear();
  336  			break;
  337  		}
  338  		case CloudText::ProtocolKind::Removed:
  339  		{
  340  			mRemovedFiles = protocol.files;
  341  			mRemovedBytes = protocol.bytes;
  342  			mRemovedDetail.clear();
  343  			for (auto& sys : protocol.systems)
  344  			{
  345  				std::string d = sys.system + " " + sys.files + " " + std::string(sys.files == "1" ? _("FILE") : _("FILES"));
  346  				if (sys.bytes > 0)
  347  					d += " · " + CloudText::sizeLabel((unsigned long) sys.bytes);
  348  				mRemovedDetail.push_back(d);
  349  			}
  350  			break;
  351  		}
  352  		case CloudText::ProtocolKind::Unit:
  353  		{
  354  			foldUnit();   // the unit that just ended: its last totals are the run's now
  355  			const std::string label = protocol.text;
  356  			const int scriptIndex   = protocol.number;
  357  			const int scriptCount   = protocol.count;
  358  			// The next item, unless it is the current one announced again. The
  359  			// first announcement is an item whatever its label says.
  360  			if (mItemIndex == 0 || label != mUnitLabel)
  361  			{
  362  				if (scriptCount > 0 && (mLastScriptIndex == 0 || scriptIndex <= mLastScriptIndex))
  363  					mScriptBase = mItemIndex;   // a script's first announcement: what came before it is its base
  364  				mItemIndex++;
  365  				mUnitsSinceTier.push_back(Utils::String::toUpper(label));
  366  			}
  367  			mLastScriptIndex = scriptCount > 0 ? scriptIndex : 0;
  368  			if (scriptCount > 0)
  369  				mItemCount = mScriptBase + scriptCount + mTrailing;
  370  			// Never ITEM 5 OF 4: a script that announced more than anybody
  371  			// expected grows the count rather than overrun it.
  372  			if (mItemCount > 0 && mItemIndex > mItemCount)
  373  				mItemCount = mItemIndex;
  374  			mUnitLabel = label;
  375  			mDoing.clear();
  376  			mCurrent.clear(); mFileProgress.clear(); mTotals.clear(); mFilesTotals.clear(); mChecking.clear();
  377  			mFilesThisBlock = 0; mChecksThisBlock = 0; mSeenBlock = false;
  378  			mChecksDone = 0; mChecksTotal = 0; mListed = 0;
  379  			mBytePercent = -1; mFilePercent = -1; mCheckPercent = -1; mPercent = -1;
  380  			break;
  381  		}
  382  		case CloudText::ProtocolKind::Doing:
  383  			// Any keyword a newer script prints is ignored rather than shown
  384  			// raw: row 3 says what the item is doing in the player's words,
  385  			// and a word out of a script is not those.
  386  			// Keep generic progress verbs for scripts sharing this protocol.
  387  			if (protocol.text == "archive" || protocol.text == "unpack"
  388  				|| protocol.text == "scan" || protocol.text == "compare"
  389  				|| protocol.text == "copy" || protocol.text == "verify" || protocol.text == "remove")
  390  				mDoing = protocol.text;
  391  			break;
  392  		case CloudText::ProtocolKind::Offer:
  393  			// A question for the player, kept until the run is over and the
  394  			// outcome has been read: while the page is running, the run is
  395  			// all it has to say (#145, and input() raises it).
  396  			mOffer = protocol.text;
  397  			mOfferArgs = protocol.args;
  398  			break;
  399  		default:
  400  			// Pid is the card's, for the process group it may have to
  401  			// signal; a run of this kind is not cancelled for a launch (D-CLOUD-113).
  402  			// Unknown is a marker newer than this build.
  403  			break;
  404  		}
  405  		return;
  406  	}
  407  
  408  	// From here on the line is rclone's, so whatever the item was busy with
  409  	// before rclone ran is over.
  410  	if (line.rfind("Transferred:", 0) == 0)
  411  	{
  412  		std::string body = Utils::String::trim(line.substr(12));
  413  		if (body.find('/') == std::string::npos)
  414  			return;
  415  		mDoing.clear();
  416  		if (body.find("iB") == std::string::npos && body.find(" B") == std::string::npos)
  417  		{
  418  			mFilesTotals = body;   // the count line of the block: "12 / 45, 27%"
  419  			mFilePercent = parsePercent(body);
  420  			refreshPercent();
  421  			// "12 / 45" -- twelve files done so far in this unit; it only
  422  			// grows, so a smaller number is a new rclone inside the unit.
  423  			// Files only -- the bytes were settled by this block's byte line,
  424  			// which comes first (foldUnit).
  425  			const long files = atol(body.c_str());
  426  			if (files < mUnitFiles)
  427  				mRunFiles += mUnitFiles;
  428  			mUnitFiles = files;
  429  			return;
  430  		}
  431  
  432  		mTotals = body;
  433  		if (body.rfind("0 B /", 0) != 0)
  434  			mAnyTransferred = true;
  435  		// "80 KiB / 300 KiB" -- what this unit has moved so far, read from the
  436  		// first field. Recorded only when it parsed; a byte line that was
  437  		// seen at all is what lets the done page show any number.
  438  		const long bytes = CloudText::parseBytes(body.substr(0, body.find('/')));
  439  		if (bytes >= 0)
  440  		{
  441  			mRunSized = true;
  442  			if (bytes < mUnitBytes)
  443  				foldUnit();
  444  			mUnitBytes = bytes;
  445  		}
  446  		// A block that carried no per-file line had nothing in flight -- the
  447  		// unit's files are done or being checked -- so the name row does not
  448  		// keep showing a file that finished a block ago. The same for a name
  449  		// caught mid-comparison.
  450  		if (mSeenBlock && mFilesThisBlock == 0)
  451  		{
  452  			mCurrent.clear();
  453  			mFileProgress.clear();
  454  		}
  455  		if (mSeenBlock && mChecksThisBlock == 0)
  456  			mChecking.clear();
  457  		mSeenBlock = true;
  458  		mFilesThisBlock = 0;    // a new block: the next " * " line is the head of it
  459  		mChecksThisBlock = 0;
  460  
  461  		// Each percentage is its own line's last word, and a "-" parses to
  462  		// -1, so a line that prints no number clears its own value. The
  463  		// other two are not reset here: rclone prints the Checks and the
  464  		// count lines in every block once it has printed them at all (their
  465  		// counters only grow), so a value left standing is one it is about
  466  		// to overwrite a few microseconds on -- and resetting it made the
  467  		// bar read the bytes alone for that instant, 100% over a run still
  468  		// comparing. The one on screen is left as it is until this block
  469  		// has produced a number: a bar that fell back to the spinner for
  470  		// the instant between two lines would flicker once a second.
  471  		mBytePercent = parsePercent(body);
  472  		refreshPercent();
  473  		return;
  474  	}
  475  	// "Checks:                12 / 45, 27%, Listed 300" -- what rclone has
  476  	// compared rather than moved, and how much of both sides it has listed.
  477  	// Before anything is queued to compare it reads "0 / 0, -, Listed 300"
  478  	// (rclone 1.75 prints the line once checks, their total, or the listing
  479  	// is non-zero), so the listing count is the first sign of life on a run
  480  	// against a large remote. Older rclones end the line at the percentage.
  481  	if (line.rfind("Checks:", 0) == 0)
  482  	{
  483  		std::string body = Utils::String::trim(line.substr(7));
  484  		auto slash = body.find(" / ");
  485  		if (slash == std::string::npos)
  486  			return;
  487  		mDoing.clear();
  488  		mChecksDone  = atol(body.substr(0, slash).c_str());
  489  		mChecksTotal = atol(body.substr(slash + 3).c_str());
  490  		auto listed = body.find("Listed ");
  491  		if (listed != std::string::npos)
  492  			mListed = atol(body.substr(listed + 7).c_str());
  493  		mCheckPercent = parsePercent(body);
  494  		refreshPercent();
  495  		return;
  496  	}
  497  
  498  	// " *   Some Game.zip: 45% /2.5Mi, 300Ki/s, 5s" -- one per parallel
  499  	// transfer, four by default. The first names what to show; the rest are
  500  	// counted, because "and 3 more" is the difference between a device that
  501  	// looks stalled on one file and one that is saturating the link.
  502  	if (!line.empty() && line[0] == '*')
  503  	{
  504  		mDoing.clear();
  505  		std::string body = Utils::String::trim(line.substr(1));
  506  
  507  		// " *   name: checking" -- a file rclone caught mid-comparison, under
  508  		// its "Checking:" heading. Not a transfer: it is the name for the
  509  		// CHECKING line, and counting it would promise a file that never
  510  		// moves. " *   name: transferring" is one that is queued with no
  511  		// bytes yet, so there is no percentage to split on; the name is
  512  		// real and the progress is empty.
  513  		static const std::string CHECKING = ": checking";
  514  		static const std::string QUEUED   = ": transferring";
  515  		if (body.size() > CHECKING.size() && body.compare(body.size() - CHECKING.size(), CHECKING.size(), CHECKING) == 0)
  516  		{
  517  			mChecking = Utils::FileSystem::getFileName(Utils::String::trim(body.substr(0, body.size() - CHECKING.size())));
  518  			mChecksThisBlock++;
  519  			return;
  520  		}
  521  		if (body.size() > QUEUED.size() && body.compare(body.size() - QUEUED.size(), QUEUED.size(), QUEUED) == 0)
  522  			body = Utils::String::trim(body.substr(0, body.size() - QUEUED.size()));
  523  
  524  		if (mFilesThisBlock == 0)
  525  		{
  526  			// "name.zip: 45% /2.5Mi, 300Ki/s, 5s" -- the name and its progress
  527  			// arrive on one line; shown on two, so neither wraps.
  528  			//
  529  			// rclone prints the percentage as %3d, so the separator is ": " at
  530  			// 45% and ":" at 100% ("name.zip:100% /40Mi, 1Mi/s, 0s"). Splitting
  531  			// on ": " put the whole line on the name row at 100%, and the
  532  			// basename of "1Mi/s, 0s" is "s" -- the file the maintainer saw
  533  			// called "S". The separator is the last ':' followed by a
  534  			// percentage; a name may contain ':' but not ':' + digits + '%'.
  535  			size_t sep = std::string::npos;
  536  			for (size_t i = body.size(); i-- > 0; )
  537  			{
  538  				if (body[i] != ':')
  539  					continue;
  540  				size_t j = i + 1;
  541  				while (j < body.size() && body[j] == ' ')
  542  					j++;
  543  				size_t d = j;
  544  				while (d < body.size() && isdigit((unsigned char) body[d]))
  545  					d++;
  546  				if (d > j && d < body.size() && body[d] == '%')
  547  				{
  548  					sep = i;
  549  					break;
  550  				}
  551  			}
  552  			std::string name = sep == std::string::npos ? body : body.substr(0, sep);
  553  			mFileProgress = sep == std::string::npos ? "" : Utils::String::trim(body.substr(sep + 1));
  554  			mCurrent = Utils::FileSystem::getFileName(Utils::String::trim(name));
  555  		}
  556  		mFilesThisBlock++;
  557  		return;
  558  	}
  559  }
  560  
  561  // The first percentage in an rclone stats field: "12 / 45, 27%, Listed 300"
  562  // gives 27; "0 B / 0 B, -, 0 B/s, ETA -" gives -1. Only a number that was
  563  // printed is ever returned -- the caller shows a spinner for -1 rather than
  564  // a bar at a position nobody measured.
  565  int CloudTransferJob::parsePercent(const std::string& body)
  566  {
  567  	auto pp = body.find('%');
  568  	if (pp == std::string::npos || pp == 0)
  569  		return -1;
  570  	size_t st = pp;
  571  	while (st > 0 && isdigit((unsigned char) body[st - 1]))
  572  		st--;
  573  	if (st == pp)
  574  		return -1;
  575  	const int v = atoi(body.substr(st, pp - st).c_str());
  576  	return (v >= 0 && v <= 100) ? v : -1;
  577  }
  578  
  579  // The bar shows the work furthest from done, which is the lower of two
  580  // percentages: the transfer's and the checks'. A run is both -- rclone
  581  // compares as it lists and moves what differs -- and a saves backup with
  582  // one changed save among hundreds moves its bytes in a second, then spends
  583  // the run comparing. Bytes alone pinned the bar at 100% over a live
  584  // CHECKING 120 OF 400 FILES for all of it (review, 2026-09-08); the lower
  585  // of the two reads 27 -> 0 -> 89 -> 100 block by block on that run, every
  586  // number rclone's.
  587  //
  588  // The transfer's percentage is bytes: they say how long this will take when
  589  // the files are a save game and a disc image. The count of files
  590  // transferred stands in only when the bytes have no number (nothing but
  591  // empty files queued), because it counts completed files -- four disc
  592  // images moving in parallel read 0 / 4 until the first lands, and a bar
  593  // that took the lowest of all three would sit at zero for most of such a
  594  // run. A run with nothing to move has neither, and then the count of files
  595  // checked is the only measure there is -- a true one, which is more than
  596  // the spinner it replaces could say. Never a number nobody printed: with
  597  // none, mPercent keeps its last real value. Called with mMutex held.
  598  void CloudTransferJob::refreshPercent()
  599  {
  600  	int p = mBytePercent >= 0 ? mBytePercent : mFilePercent;
  601  	if (mCheckPercent >= 0 && (p < 0 || mCheckPercent < p))
  602  		p = mCheckPercent;
  603  	if (p >= 0)
  604  		mPercent = p;
  605  }
  606  
  607  void CloudTransferJob::run()
  608  {
  609  	int ret = -1;
  610  	// Braces around the whole command, not just " 2>&1" after it. The command
  611  	// is a sequence, and a trailing redirection binds to its last element only
  612  	// -- so everything the earlier tiers wrote to stderr went to the ES
  613  	// process's own stderr and never reached the page.
  614  	//
  615  	// SIGPIPE ignored inside them, as the scan's job does (OfflineScanJob):
  616  	// should this process end while the run is still going -- essway
  617  	// restarting the interface under a transfer -- the scripts' own ">>> "
  618  	// lines meet a closed pipe and fail without killing the shell, so a
  619  	// part that can still end writes its stamp. rclone's
  620  	// progress rides the same pipe, and rclone ends on a broken one, so the
  621  	// run itself is not promised to outlive the interface: each file it
  622  	// moves is renamed into place whole and the next run finishes what this
  623  	// one did not (D-CLOUD-077). While this process lives, this thread reads
  624  	// the pipe to the end whatever happens to the page.
  625  	//
  626  	// In a session of its own, saying so on its first line: setsid makes
  627  	// the shell a process group leader and ">>> pid N" tells stopForLaunch
  628  	// which group to signal, so the shell, the scripts and their rclone go
  629  	// together -- the shape ThreadedCloudSync gives its commands, for the
  630  	// same cancel (D-CLOUD-129). shellQuote, so a command with a quote in it
  631  	// survives the trip.
  632  	// The stamps before anything runs, on this thread rather than the
  633  	// interface's (a stat and a short read a stamp): what a stop's restamp
  634  	// compares against (G-E2-O2).
  635  	mStampsBefore = ThreadedCloudSync::readStamps(mCommand);
  636  	const std::string wrapped = "setsid sh -c "
  637  		+ Utils::String::shellQuote("echo \">>> pid $$\"; { trap '' PIPE; " + mCommand + " ; }") + " 2>&1";
  638  	FILE* pipe = popen(wrapped.c_str(), "r");
  639  	if (pipe != nullptr)
  640  	{
  641  		// Read a character at a time, and treat three things as ending a line:
  642  		// \n, \r, and the string "Transferred:" appearing mid-line.
  643  		//
  644  		// The third is not defensive programming, it is the observed format.
  645  		// Piped (there is no terminal here), rclone ends each redraw after the
  646  		// last " * file" line WITHOUT a newline, so the next block's
  647  		// "Transferred:" is glued onto it:
  648  		//
  649  		//   * f4.bin: 26% / 3.8 MiB, 507 KiB/sTransferred: 6.1 MiB / 22.8 MiB...
  650  		//
  651  		// Splitting on newlines alone yields one line that is neither a file
  652  		// line nor a totals line, and both halves are lost -- every block after
  653  		// the first. \r is handled because a terminal-attached run does use it.
  654  		std::string buf;
  655  		int c;
  656  		while ((c = fgetc(pipe)) != EOF)
  657  		{
  658  			if (c != '\n' && c != '\r')
  659  			{
  660  				if (buf.size() < 1024)
  661  					buf += (char) c;
  662  
  663  				static const std::string MARK = "Transferred:";
  664  				if (buf.size() > MARK.size()
  665  					&& buf.compare(buf.size() - MARK.size(), MARK.size(), MARK) == 0)
  666  				{
  667  					handleLine(cleanLine(buf.substr(0, buf.size() - MARK.size())));
  668  					buf = MARK;
  669  				}
  670  				continue;
  671  			}
  672  
  673  			handleLine(cleanLine(buf));
  674  			buf.clear();
  675  		}
  676  		if (!buf.empty())
  677  			handleLine(cleanLine(buf));
  678  
  679  		int status = pclose(pipe);
  680  		if (WIFEXITED(status))
  681  			ret = WEXITSTATUS(status);
  682  	}
  683  
  684  	std::unique_lock<std::mutex> lock(mMutex);
  685  	foldUnit();   // the last unit: no ">>> unit" follows it
  686  	// A stop that came as the command was ending, and found it done: the
  687  	// command's own 0 (or rclone's 9, nothing to move) says it completed,
  688  	// and a completed run is not called stopped (#308 gpt F-CS-24). A run
  689  	// the stop did end exits by the signal or by the scripts' trap, 130 --
  690  	// never 0.
  691  	if ((mStoppedForGame || mStoppedByPlayer) && (ret == 0 || ret == 9))
  692  	{
  693  		LOG(LogInfo) << "CloudTransferJob: the stop came after the command had finished; it completed";
  694  		mStoppedForGame = false;
  695  		mStoppedByPlayer = false;
  696  	}
  697  	// Stopped for a game, or by the player (D-UI-078): SIGTERM shows up as
  698  	// a signal or as 143, and neither is what happened. CloudExit::Stopped
  699  	// is the scripts' own word for being stopped, whoever did the stopping
  700  	// (ThreadedCloudSync does the same for the card's cancel).
  701  	const bool stopped = mStoppedForGame || mStoppedByPlayer;
  702  	if (stopped)
  703  	{
  704  		ret = CloudExit::Stopped;
  705  		// The scripts' INT/TERM trap stamped each part it was inside with 130
  706  		// and no token, and the rows under MANAGE CLOUD STORAGE read that as
  707  		// COULDN'T FINISH once this run was dismissed (#203). Say what
  708  		// happened in their place: the token the card's cancel writes for a
  709  		// game, the player's own for a cancel (CloudText's outcome tokens).
  710  		restampStoppedParts(mStoppedByPlayer ? "player-cancelled" : "cancelled");
  711  	}
  712  	mExit = ret;
  713  	// A command with no tier lines (the match; anything composed before
  714  	// them) that did not complete: what it said is its failed item -- the
  715  	// unit the why arrived under, or the why alone -- and with no why at
  716  	// all, the code's phrase for the unit that was running, if one was.
  717  	if (ret != 0 && ret != 9 && mFailed.empty() && !stopped)
  718  	{
  719  		for (auto& w : mPendingWhys)
  720  			mFailed.push_back(w);
  721  		if (mFailed.empty() && ret != CloudExit::LockHeld && ret != CloudExit::NoNetwork)
  722  			mFailed.push_back({ Utils::String::toUpper(mUnitLabel), ThreadedCloudSync::whyForCode(ret) });
  723  	}
  724  	mPendingWhys.clear();
  725  	mElapsedMs = elapsedMsLocked();
  726  	mFinishedAt = time(nullptr);
  727  	mFinished = true;
  728  	LOG(LogInfo) << "CloudTransferJob: " << mTitle << " exited " << ret
  729  		<< " (" << mRunFiles << " files, " << mRunBytes << " bytes, " << mTiers.size() << " tiers reported)";
  730  }
  731  
  732  // The part the stop interrupted, and only it: ThreadedCloudSync's rule,
  733  // shared with the card (#308 claude F-CS-05, gpt F-CS-23). This page's
  734  // table named cloud_backup's last-backup and cloud_restore's last-restore
  735  // alone, so a stopped settings part kept its trap's 130 under the settings
  736  // row, and restamped every stamp the run had written, so a saves part that
  737  // finished before the stop read as stopped.
  738  void CloudTransferJob::restampStoppedParts(const char* token)
  739  {
  740  	ThreadedCloudSync::restampStoppedParts(mCommand, mStampsBefore, mStartedAt, token);
  741  }
  742  
  743  // One line of a script's output: ANSI escapes, C0 controls and DEL dropped,
  744  // every UTF-8 byte kept, then trimmed -- CloudText::cleanLine, the rule the
  745  // sync card reads by since #308 F-CS-19. This page carried a copy of its
  746  // own; the two gave the same line for every input, and one copy is one
  747  // rule to change.
  748  std::string CloudTransferJob::cleanLine(const std::string& raw)
  749  {
  750  	return CloudText::cleanLine(raw);
  751  }
```


## es-app/src/ThreadedCloudSync.cpp @ 16dbac5211 (whole, 949 lines)

```text
    1  #include "ThreadedCloudSync.h"
    2  #include "CloudExit.h"
    3  #include "CloudOffer.h"
    4  #include "CloudText.h"
    5  #include "CloudTransferJob.h"
    6  #include "Log.h"
    7  #include "OfflineAchievements.h"
    8  #include "ProxyCards.h"
    9  #include "Window.h"
   10  #include "components/AsyncNotificationComponent.h"
   11  #include "guis/GuiMsgBox.h"
   12  #include "SystemConf.h"
   13  #include "utils/FileSystemUtil.h"
   14  #include "utils/Platform.h"
   15  #include "utils/StringUtil.h"
   16  #include <chrono>
   17  #include <cstdio>
   18  #include <ctime>
   19  #include <mutex>
   20  #include <thread>
   21  #include <signal.h>
   22  #include <sys/stat.h>
   23  #include <sys/wait.h>
   24  #include "LocaleES.h"
   25  
   26  #define ICONINDEX _U("\uF0C2 ")
   27  
   28  std::atomic<ThreadedCloudSync*> ThreadedCloudSync::mInstance(nullptr);
   29  std::mutex ThreadedCloudSync::sInstanceLock;
   30  
   31  ThreadedCloudSync::ThreadedCloudSync(Window* window, const std::string& command,
   32  	const std::string& title, const std::string& running, Origin origin)
   33  	: mWindow(window), mCommand(command), mTitle(title), mRunning(running), mOrigin(origin),
   34  	  mStartedAt(time(nullptr))
   35  {
   36  	mGameExitSync = SystemConf::getInstance()->get("cloudsaves.gameexit") == "1";
   37  	// The script stamps as they are before anything runs, so a stop can tell
   38  	// the one its trap writes from an earlier run's (G-E1-04/06).
   39  	mStampsBefore = readStamps(mCommand);
   40  	// With the action row. The default is a two-row card (title and text),
   41  	// and this was created with the default, so the recovery clause run()
   42  	// composes -- what is in place, and where to try again (D-CLOUD-077) --
   43  	// was measured, chosen, and never drawn: the card had no row to draw it
   44  	// on (guest d, 2026-09-10). The row is blank while the work runs and
   45  	// carries the clause once the outcome is known.
   46  	mWndNotification = mWindow->createAsyncNotificationComponent(true);
   47  	mWndNotification->updateTitle(ICONINDEX + (mRunning.empty() ? mTitle : mRunning));
   48  	mWndNotification->updateText(_("STARTING..."));
   49  	mWndNotification->updatePercent(-1);
   50  
   51  	// Detached: run() ends with `delete this`, so nothing is left to join
   52  	// it, and a joinable thread that has ended keeps its stack and control
   53  	// block until somebody does -- one per sync, two a game, for the life of
   54  	// the interface (#307 PL-069). This was `mHandle = new std::thread(...)`,
   55  	// never joined, detached or deleted.
   56  	std::thread(&ThreadedCloudSync::run, this).detach();
   57  }
   58  
   59  ThreadedCloudSync::~ThreadedCloudSync()
   60  {
   61  	mWndNotification->close();
   62  	mWndNotification = nullptr;
   63  
   64  	// Only if it is still us. run() clears this as soon as the work ends so
   65  	// another sync can start during the few seconds the card holds its
   66  	// result -- and if one has, the static belongs to that one now. Under
   67  	// the lock, like every other change to it (#308 F-CS-25).
   68  	std::lock_guard<std::mutex> lock(sInstanceLock);
   69  	if (ThreadedCloudSync::mInstance == this)
   70  		ThreadedCloudSync::mInstance = nullptr;
   71  }
   72  
   73  // The four outcome words and what follows them (D-UI-028, es-native-ui.md
   74  // "Outcome vocabulary"): a why, what is in place, and how to recover.
   75  // Nothing else -- no FAILED, no log path, no exit code, no rclone.
   76  
   77  // The why for an exit code the scripts did not explain with a ">>> why"
   78  // line of their own. rclone's codes; 130 is the scripts' trap, when it was
   79  // not this process that stopped them.
   80  std::string ThreadedCloudSync::whyForCode(int rc)
   81  {
   82  	switch (rc)
   83  	{
   84  		case 3: case 4: return _("COULDN'T FIND YOUR CLOUD FOLDER");
   85  		case 5: case 124: return _("YOUR CLOUD STOPPED ANSWERING");
   86  		case 7: case 8: return _("YOUR CLOUD WOULDN'T TAKE THE FILES");
   87  		case CloudExit::Stopped:   return _("IT WAS STOPPED");
   88  		// The sentinels, for a part that exited one beside a part that did
   89  		// not (the transfer page's line 4): the same words the SKIPPED
   90  		// outcome uses, so one code is never called two things.
   91  		case CloudExit::NoNetwork: return _("YOU'RE NOT ONLINE");
   92  		case CloudExit::LockHeld:  return _("A SYNC IS ALREADY RUNNING");
   93  		case CloudExit::NoFolder:  return _("YOUR CLOUD FOLDER ISN'T SET UP YET");
   94  		default:        return _("SOMETHING WENT WRONG");
   95  	}
   96  }
   97  
   98  // The short forms of a why sentence, for a panel the whole one does not fit
   99  // on (#115), are CloudText::shortenWhy and CloudText::outcomeCandidates --
  100  // pure string work, checked by es-app/tests/unit.
  101  
  102  // The stamp's one-word token for the same code, for the row's reader.
  103  std::string ThreadedCloudSync::tokenForCode(int rc)
  104  {
  105  	switch (rc)
  106  	{
  107  		case 0: case 9: return "completed";
  108  		case 3: case 4: return "folder-missing";
  109  		case 5: case 124: return "cloud-stopped";
  110  		case 7: case 8: return "cloud-refused";
  111  		case CloudExit::Stopped:   return "stopped";
  112  		case CloudExit::NoNetwork: return "no-network";
  113  		case CloudExit::LockHeld:  return "lock-held";
  114  		case CloudExit::NoFolder:  return "no-folder";
  115  		default:        return "unknown";
  116  	}
  117  }
  118  
  119  // The token read back: the phrase for one the table above wrote, "" for
  120  // one it did not (the stamp's code decides then).
  121  std::string ThreadedCloudSync::whyForToken(const std::string& token)
  122  {
  123  	if (token == "folder-missing") return whyForCode(3);
  124  	if (token == "cloud-stopped")  return whyForCode(5);
  125  	if (token == "cloud-refused")  return whyForCode(7);
  126  	if (token == "stopped")        return whyForCode(CloudExit::Stopped);
  127  	if (token == "no-folder")      return whyForCode(CloudExit::NoFolder);
  128  	return "";
  129  }
  130  
  131  // Which way the saves moved, read from the command (CloudText::verbOf): the
  132  // in-place clause is one per verb, true because rclone renames each file
  133  // into place when it is complete (D-CLOUD-077).
  134  static std::string inPlaceClause(CloudText::Verb verb, bool moved)
  135  {
  136  	switch (verb)
  137  	{
  138  		case CloudText::Verb::Sync:    return moved ? _("THE SAVES THAT MADE IT ARE ON BOTH SIDES. NOTHING ELSE CHANGED.") : _("DON'T WORRY, NOTHING CHANGED.");
  139  		case CloudText::Verb::Backup:  return moved ? _("WHAT MADE IT IS IN YOUR CLOUD. THE REST IS STILL HERE.") : _("DON'T WORRY, NOTHING CHANGED.");
  140  		case CloudText::Verb::Restore: return moved ? _("WHAT MADE IT IS ON THIS DEVICE. NOTHING ELSE CHANGED.") : _("DON'T WORRY, NOTHING CHANGED.");
  141  		default:            return "";
  142  	}
  143  }
  144  
  145  void ThreadedCloudSync::run()
  146  {
  147  	// Stream the backend's output into the notification card so the user
  148  	// sees live status (rclone --stats-one-line lines, phase banners, ...).
  149  	int ret = -1;
  150  
  151  	// What the card says and where its bar stands go through one pair of
  152  	// hands, so that a half of a composed sync is named in front of every
  153  	// line and the bar never moves back within it (D-UI-052, #157). The
  154  	// half's word first, then the line -- RECEIVING . COMPARING SAVES . 113
  155  	// OF 113 -- so the second compare count is visibly a different step
  156  	// from the first. A command that announces no halves (the after-a-game
  157  	// backup, the manual rows) reads and draws exactly as it did.
  158  	auto say = [this](const std::string& line)
  159  	{
  160  		if (mWndNotification == nullptr)
  161  			return;
  162  		std::string half;
  163  		if (mPhase == CloudText::Phase::Receiving)
  164  			half = _("RECEIVING");
  165  		else if (mPhase == CloudText::Phase::Sending)
  166  			half = _("SENDING");
  167  		mWndNotification->updateText(half.empty() ? line : half + std::string(" \xC2\xB7 ") + line);
  168  	};
  169  	// The same line offered in more than one length: the card measures the
  170  	// candidates in its own font on the interface thread and shows the first
  171  	// that fits (AsyncNotificationComponent), as the outcome line does.
  172  	auto sayAny = [this](const std::vector<std::string>& candidates)
  173  	{
  174  		if (mWndNotification == nullptr)
  175  			return;
  176  		std::string half;
  177  		if (mPhase == CloudText::Phase::Receiving)
  178  			half = _("RECEIVING");
  179  		else if (mPhase == CloudText::Phase::Sending)
  180  			half = _("SENDING");
  181  		std::vector<std::string> lines;
  182  		for (auto& line : candidates)
  183  			lines.push_back(half.empty() ? line : half + std::string(" \xC2\xB7 ") + line);
  184  		mWndNotification->updateText(lines, std::vector<std::string>());
  185  	};
  186  	auto bar = [this](int percentInPhase)
  187  	{
  188  		int next = CloudText::phaseBar(mPhase, percentInPhase);
  189  		if (mPhase != CloudText::Phase::None)
  190  			next = CloudText::forwardOnly(mBar, next);
  191  		if (next < 0)
  192  			return;
  193  		mBar = next;
  194  		if (mWndNotification != nullptr)
  195  			mWndNotification->updatePercent(next);
  196  	};
  197  
  198  	// Every command runs in a session of its own and says so on its first
  199  	// line: setsid makes the shell a process group leader, and ">>> pid N"
  200  	// tells cancelForLaunch which group to signal, so the shell, the
  201  	// scripts and their rclone children go together. Done here rather than
  202  	// by each caller because the one caller that wrapped its own command
  203  	// (the startup sync) was the only one that could be cancelled -- the
  204  	// after-a-game backup ran bare, with no group to send a signal to.
  205  	// shellQuote, so a command with a quote in it survives the trip.
  206  	const std::string wrapped = "setsid sh -c "
  207  		+ Utils::String::shellQuote("echo \">>> pid $$\"; " + mCommand) + " 2>&1";
  208  	FILE* pipe = popen(wrapped.c_str(), "r");
  209  	if (pipe != nullptr)
  210  	{
  211  		char line[512];
  212  		while (fgets(line, sizeof(line), pipe) != nullptr)
  213  		{
  214  			// One line, without controls or a terminal's escapes, its UTF-8
  215  			// kept (CloudText::cleanLine, #308 F-CS-19).
  216  			const std::string clean = CloudText::cleanLine(line);
  217  
  218  			// ">>> " lines are the scripts talking to the UI, not to the
  219  			// player. ">>> pid N" is the wrapper above saying which process
  220  			// group the command is (for cancelForLaunch); ">>> doing network"
  221  			// says cloud_net_ready is waiting for a settled connection, the
  222  			// one wait this card shows -- the startup sync (fork #94) gives
  223  			// the network up to a minute to come up after boot, and a card
  224  			// reading "Working..." for that minute says nothing about why.
  225  			// Its words follow the link (fork #192): CHECKING THE
  226  			// CONNECTION... when the interface has an address, since the
  227  			// script holds a connection that is up for a short grace and
  228  			// that is a check, not a wait; WAITING FOR A NETWORK with the
  229  			// bound otherwise, then the run goes on or ends SKIPPED as it
  230  			// always did; ">>> doing receive" and
  231  			// ">>> doing send" are a composed sync announcing each of its
  232  			// halves before it starts, which is what gives the bar its two
  233  			// halves (D-UI-052). ">>> why <sentence>" is
  234  			// the scripts saying, at the point of failure and in the
  235  			// player's words, what went wrong -- the last one is the outcome
  236  			// line's why (D-UI-028; it replaced a filter that showed any line
  237  			// containing ERROR, FAILED or WARN, which passed rclone's prose
  238  			// and dropped the scripts' own diagnoses). ">>> tier <label>|<rc>"
  239  			// is a composed command reporting each of its parts as it ends,
  240  			// so a run where one part finished and another did not is
  241  			// reported as a failure with that part's why, rather than as the last
  242  			// part's code. ">>> unit" and anything newer is for the transfer
  243  			// page and never reaches the card -- but each one says the wait
  244  			// is over, as does the first word any script prints.
  245  			//
  246  			// Which line is which is CloudText::classifyProtocolLine, so the
  247  			// shapes can be checked without a pipe (es-app/tests/unit); what
  248  			// each one does to this thread stays here.
  249  			const CloudText::ProtocolLine protocol = CloudText::classifyProtocolLine(clean);
  250  			if (protocol.kind != CloudText::ProtocolKind::NotProtocol)
  251  			{
  252  				switch (protocol.kind)
  253  				{
  254  				case CloudText::ProtocolKind::Pid:
  255  					mPid = protocol.number;
  256  					break;
  257  				case CloudText::ProtocolKind::Doing:
  258  				{
  259  					// The local answer, not the member: cancelForLaunch clears
  260  					// the flag from another thread, and this line is about the
  261  					// line just read.
  262  					const bool network = (protocol.text == "network");
  263  					mWaitingForNetwork = network;
  264  					if (network)
  265  					{
  266  						// Which words is CloudText::networkStep's call (fork
  267  						// #192): the link as the interface sees it now -- the
  268  						// same test NetworkStateWatcher makes, an address on
  269  						// an interface -- and the bound as the command spelt
  270  						// it, so the number on the card cannot drift from the
  271  						// number the shell runs. With a link the step is a
  272  						// check and reads so; without one it is a wait, said
  273  						// with its bound where the panel has room and without
  274  						// it where it has not (D-UI-055: true of what happens).
  275  						const CloudText::NetworkStepChoice choice = CloudText::networkStep(
  276  							!Utils::Platform::queryIPAddress().empty(), mCommand);
  277  						if (choice.step == CloudText::NetworkStep::Checking)
  278  							say(_("CHECKING THE CONNECTION..."));
  279  						else
  280  						{
  281  							std::vector<std::string> lines;
  282  							if (choice.waitSeconds > 0)
  283  								lines.push_back(Utils::String::format(_("WAITING FOR A NETWORK, UP TO %d SECONDS...").c_str(), choice.waitSeconds));
  284  							lines.push_back(_("WAITING FOR A NETWORK..."));
  285  							sayAny(lines);
  286  						}
  287  					}
  288  
  289  					// A half of a composed sync starting (">>> doing receive",
  290  					// ">>> doing send"; D-UI-052): the words carry its name from
  291  					// here, the bar parks at its start -- 0, then 50 -- and the
  292  					// last half's bytes are forgotten, so the compare that
  293  					// opens this half is shown as one. Announced before the
  294  					// script runs, so the seconds it spends reaching the cloud
  295  					// before rclone prints anything already read as this
  296  					// half's, rather than as the last half standing still.
  297  					const CloudText::Phase phase = CloudText::phaseOf(protocol.text);
  298  					if (phase != CloudText::Phase::None)
  299  					{
  300  						mPhase = phase;
  301  						mBytesMoving = false;
  302  						mCountShown = false;
  303  						mFilesDone = -1;
  304  						mFilesTotal = -1;
  305  						say(_("STARTING..."));
  306  						bar(-1);
  307  					}
  308  					break;
  309  				}
  310  				case CloudText::ProtocolKind::Why:
  311  					mWaitingForNetwork = false;
  312  					if (!protocol.text.empty())
  313  						mWhy = protocol.text;
  314  					break;
  315  				case CloudText::ProtocolKind::Offer:
  316  					// A script asking for a question to be put to the player
  317  					// once the run is over. The only one today: a cloud that
  318  					// answers with no saves folder in it, which is not a
  319  					// failure but does leave the player with nothing to
  320  					// restore and no obvious way forward (#100, D-CLOUD-085).
  321  					mWaitingForNetwork = false;
  322  					mOffer = protocol.text;
  323  					mOfferArgs = protocol.args;
  324  					break;
  325  				case CloudText::ProtocolKind::Tier:
  326  					mWaitingForNetwork = false;
  327  					if (!protocol.text.empty())
  328  						mTiers.push_back(std::make_pair(protocol.text, protocol.number));
  329  					break;
  330  				default:
  331  					mWaitingForNetwork = false;
  332  					break;
  333  				}
  334  				continue;
  335  			}
  336  			mWaitingForNetwork = false;
  337  
  338  			// The card shows progress; the title above it already says what
  339  			// is happening. Everything the backends print used to land here,
  340  			// which meant rules of "====================================" for
  341  			// seconds at a time, and -- during a sync, which runs a restore
  342  			// and then a backup -- banners announcing "CLOUD RESTORE UTILITY"
  343  			// and "CLOUD BACKUP UTILITY" underneath a title reading SYNCING
  344  			// SAVES. Those are written for a log read afterwards, not for
  345  			// somebody watching a handheld.
  346  			//
  347  			// So: transfer progress, and nothing else, in the player's words.
  348  			// What the line carries is CloudText::liveLine's to read (#140;
  349  			// it is what found "Elapsed time: 2.0sTransferred: 0 B / 0 B" on
  350  			// the card -- rclone glues one block's last line to the next
  351  			// block's first when it writes to a pipe). What went wrong
  352  			// arrives on the protocol line above, in the scripts' own words,
  353  			// and is said once at the end.
  354  			//
  355  			// Which words a stats line gets is CloudText::liveWords (#208), so
  356  			// the rule is checked without a pipe: a byte line with a total or
  357  			// bytes sent is the fact of the moment and reads X OF Y; a still one
  358  			// ("0 B / 0 B") is the listing and the compare and reads COMPARING
  359  			// SAVES -- it used to read NOTHING SENT YET / NOTHING RECEIVED YET,
  360  			// an outcome so far said where the player watches for progress, once
  361  			// per half of every startup and exit sync; the count line holds the
  362  			// words with its number until the bytes move, and the still byte
  363  			// line leaves it there rather than flicker the number. The check
  364  			// counter is a comparison, not a transfer: it never moves the bar by
  365  			// its own percentage, or seventy checks read as seventy uploads.
  366  			const CloudText::LiveLine live = CloudText::liveLine(clean);
  367  			if (live.kind == CloudText::LiveLine::Kind::Bytes)
  368  			{
  369  				// The byte line leaving "0 B" is the one fact the in-place
  370  				// clause turns on: something reached the other side. A total
  371  				// means rclone has queued something to move: from here the byte
  372  				// line is this half's fact.
  373  				if (live.sent > 0)
  374  					mMoved = true;
  375  				if (live.total > 0)
  376  					mBytesMoving = true;
  377  			}
  378  			// The count line names no words of its own (liveWords keeps them),
  379  			// but the byte line's words say which file is moving from it.
  380  			if (live.kind == CloudText::LiveLine::Kind::Files)
  381  			{
  382  				mFilesDone = live.sent;
  383  				mFilesTotal = live.total;
  384  			}
  385  			std::string shown;
  386  			switch (CloudText::liveWords(live, mBytesMoving, mCountShown))
  387  			{
  388  			case CloudText::LiveWords::Comparing:
  389  				shown = _("COMPARING SAVES");
  390  				break;
  391  			case CloudText::LiveWords::ComparingCount:
  392  				shown = _("COMPARING SAVES") + std::string(" \xC2\xB7 ")
  393  					+ Utils::String::format(_("%d OF %d").c_str(), (int) live.sent, (int) live.total);
  394  				mCountShown = true;
  395  				break;
  396  			case CloudText::LiveWords::Bytes:
  397  			{
  398  				// The transfer says that it is one, which file of how many, and
  399  				// how many bytes of how many, beside the bar (fork #304,
  400  				// D-UI-108; the maintainer: "transferring: file 1 of n (x KB/y
  401  				// KB)"). The half's verb stands in for TRANSFERRING where the
  402  				// sync has halves; the shorter candidates follow, longest first,
  403  				// and the card shows the first that fits (D-UI-035).
  404  				const std::string x = CloudText::sizeLabel((unsigned long) live.sent);
  405  				const std::string y = CloudText::sizeLabel((unsigned long) live.total);
  406  				const long file = CloudText::fileInFlight(mFilesDone, mFilesTotal);
  407  				const bool sending = mPhase == CloudText::Phase::Sending;
  408  				const bool receiving = mPhase == CloudText::Phase::Receiving;
  409  				std::vector<std::string> lines;
  410  				if (file > 0)
  411  				{
  412  					const std::string verbed = sending ? _("SENDING FILE %d OF %d (%s OF %s)")
  413  						: receiving ? _("RECEIVING FILE %d OF %d (%s OF %s)") : _("TRANSFERRING FILE %d OF %d (%s OF %s)");
  414  					lines.push_back(Utils::String::format(verbed.c_str(), (int) file, (int) mFilesTotal, x.c_str(), y.c_str()));
  415  					lines.push_back(Utils::String::format(_("FILE %d OF %d (%s OF %s)").c_str(), (int) file, (int) mFilesTotal, x.c_str(), y.c_str()));
  416  				}
  417  				else
  418  				{
  419  					const std::string verbed = sending ? _("SENDING %s OF %s")
  420  						: receiving ? _("RECEIVING %s OF %s") : _("TRANSFERRING %s OF %s");
  421  					lines.push_back(Utils::String::format(verbed.c_str(), x.c_str(), y.c_str()));
  422  				}
  423  				lines.push_back(Utils::String::format(_("%s OF %s").c_str(), x.c_str(), y.c_str()));
  424  				if (mWndNotification != nullptr)
  425  					mWndNotification->updateText(lines, std::vector<std::string>());
  426  				break;   // said here with the half in the verb, not through say()
  427  			}
  428  			case CloudText::LiveWords::Other:
  429  				shown = live.text;
  430  				break;
  431  			case CloudText::LiveWords::Keep:
  432  				break;
  433  			}
  434  
  435  			if (!shown.empty())
  436  				say(shown);
  437  			// The bar: the byte line's percentage, mapped into the half when
  438  			// there is one; a compare parks at the half's start, and leaves
  439  			// the bar of a run with no halves alone (D-UI-052).
  440  			if (live.kind == CloudText::LiveLine::Kind::Bytes)
  441  				bar(live.percent);
  442  			else if (live.kind == CloudText::LiveLine::Kind::Checks)
  443  				bar(-1);
  444  		}
  445  
  446  		int status = pclose(pipe);
  447  		if (WIFEXITED(status))
  448  			ret = WEXITSTATUS(status);
  449  	}
  450  
  451  	// A cancelled run ends by SIGTERM, which pclose reports as a signal or,
  452  	// when a shell sat between us and the group, as 143. Neither is what
  453  	// happened. CloudExit::Stopped is what the scripts' own trap exits with
  454  	// when somebody stops them, and what cloudLastRunDetail already reads as
  455  	// STOPPED: the same word for the same thing, whoever did the stopping.
  456  	const bool cancelled = mCancelled;
  457  	if (cancelled)
  458  		ret = CloudExit::Stopped;
  459  
  460  	// The outcome, in the four words every cloud surface uses (D-UI-028).
  461  	//
  462  	// COMPLETED when the whole run did (rclone's 9 -- nothing needed
  463  	// moving -- counts). SKIPPED for the two sentinels the scripts exit
  464  	// before touching anything (CloudExit.h) and for the launch cancel; none
  465  	// of the three is a failure, and FAILED would send somebody to a log to
  466  	// find nothing wrong. COULDN'T FINISH for everything else, with the why:
  467  	// the scripts' own sentence when they printed one, the code's phrase
  468  	// otherwise.
  469  	//
  470  	// A composed run whose parts disagree -- the startup sync's restore
  471  	// finished and its backup did not -- is a failure like any other. It
  472  	// read COMPLETED WITH GAPS for a day, and the maintainer's verdict on
  473  	// seeing one (2026-09-10) is that a half-outcome the player cannot act
  474  	// on is worse than either plain answer: "if you don't know what the gaps
  475  	// are, it's not very helpful ... it just makes you more anxious and
  476  	// trust the system less because it's working kind of. You'd rather just
  477  	// know it couldn't connect or it could connect." So the word is
  478  	// COULDN'T FINISH and the why is the failing part's; the action line
  479  	// below still says truthfully what did move. The stamp keeps the token
  480  	// so a log can still tell a partial run from a total one.
  481  	std::vector<std::string> okTiers, badTiers;
  482  	for (auto& t : mTiers)
  483  		(t.second == 0 || t.second == 9 ? okTiers : badTiers).push_back(t.first);
  484  	// A cloud with no saves folder yet: the scripts exit 0 and ask for the
  485  	// folder (">>> offer create-saves-folder"). An automatic sync does not
  486  	// raise that question -- the maintainer met it at startup on the Nova,
  487  	// 2026-10-01, and the folder is the cloud setup's and the transfer
  488  	// pages' to ask about (D-CLOUD-166, fork #353) -- it says SKIPPED with
  489  	// the row that sets it up, and stamps CloudExit::NoFolder so the row
  490  	// under SYNC SAVES DURING STARTUP says the same. A sync the player
  491  	// pressed keeps the question: they are standing there.
  492  	const bool noFolder = !cancelled && (ret == 0 || ret == 9) && mOffer == "create-saves-folder"
  493  		&& (mOrigin == Origin::Startup || mOrigin == Origin::Exit);
  494  	const bool completed = !cancelled && (ret == 0 || ret == 9) && !noFolder;
  495  	const bool gaps = !cancelled && !completed && !okTiers.empty() && !badTiers.empty();
  496  	// In the player's language: the scripts speak English whatever the
  497  	// interface does (#308 F-CS-31). The stamp below keeps mWhy as printed.
  498  	const std::string why = mWhy.empty() ? whyForCode(ret) : CloudText::localizedWhy(mWhy);
  499  
  500  	// A 69 is not always a skip (the audit of the fix round, stream A's
  501  	// lead G2-A-03 claude). The scripts exit 69 whenever the network is the
  502  	// reason -- the retry at the link's return and the offline recovery line
  503  	// read the code -- and when files had moved before the link went, the
  504  	// script's own stamp adds the gaps token and its why ("69 gaps YOU WENT
  505  	// OFFLINE PART-WAY THROUGH"), which the rows and the transfer page read
  506  	// as COULDN'T FINISH. This card read the 69 alone and said SKIPPED -
  507  	// YOU'RE NOT ONLINE, which says nothing moved. A bare 69 is still that.
  508  	std::string offlineWhy;
  509  	if (!cancelled && !gaps && ret == CloudExit::NoNetwork)
  510  		offlineWhy = CloudText::offlinePartWayWhy(readStamps(mCommand), mStampsBefore);
  511  	const bool offlineGaps = !offlineWhy.empty();
  512  
  513  	std::string outcome, token;
  514  	if (cancelled)
  515  	{
  516  		outcome = _("SKIPPED - YOU STARTED A GAME");
  517  		token = "cancelled";
  518  	}
  519  	else if (completed)
  520  	{
  521  		outcome = _("COMPLETED");
  522  		token = "completed";
  523  	}
  524  	else if (noFolder)
  525  	{
  526  		outcome = _("SKIPPED - YOUR CLOUD FOLDER ISN'T SET UP YET");
  527  		token = "no-folder";
  528  	}
  529  	else if (gaps)
  530  	{
  531  		outcome = _("COULDN'T FINISH") + std::string(" - ") + why;
  532  		token = "gaps";
  533  	}
  534  	else if (ret == CloudExit::LockHeld)
  535  	{
  536  		outcome = _("SKIPPED - A SYNC IS ALREADY RUNNING");
  537  		token = "lock-held";
  538  	}
  539  	else if (offlineGaps)
  540  	{
  541  		outcome = _("COULDN'T FINISH") + std::string(" - ") + CloudText::localizedWhy(offlineWhy);
  542  		token = "gaps";
  543  	}
  544  	else if (ret == CloudExit::NoNetwork)
  545  	{
  546  		outcome = _("SKIPPED - YOU'RE NOT ONLINE");
  547  		token = "no-network";
  548  	}
  549  	else
  550  	{
  551  		outcome = _("COULDN'T FINISH") + std::string(" - ") + why;
  552  		token = tokenForCode(ret);
  553  	}
  554  
  555  	// Before the card says anything: the stamp is the answer that outlives
  556  	// the card, so it is written first, and written whether or not there is
  557  	// still a card to say it on.
  558  	//
  559  	// The manual stamp (last-sync-manual) is the SYNC SAVES WITH THE CLOUD
  560  	// row's. A manual backup or restore is stamped by its script (last-backup,
  561  	// last-restore), which the BACK UP and RESTORE rows read; writing
  562  	// last-sync-manual for those too put a backup's outcome under the sync
  563  	// row -- LAST 00:48 - COULDN'T FINISH on a row nobody had pressed (guest
  564  	// d, 2026-09-10). Automatic origins stamp whatever they ran.
  565  	if (mOrigin != Origin::Manual || CloudText::verbOf(mCommand) == CloudText::Verb::Sync)
  566  		recordOutcome(mOrigin, noFolder ? CloudExit::NoFolder : ret, token, offlineGaps && mWhy.empty() ? offlineWhy : mWhy);
  567  
  568  	// A run stopped for a game (the player's answer to the launch question,
  569  	// D-CLOUD-129): the script's own stamp -- what the BACK UP and RESTORE
  570  	// rows read -- carries its trap's 130 and no token, which the row reads
  571  	// as COULDN'T FINISH (guest d, 2026-09-15: LAST 18:42 - COULDN'T FINISH
  572  	// for a run nobody saw fail). This process knows why it stopped; the
  573  	// stamp says so, in the shape the reader already knows, written after
  574  	// the trap's since pclose returned after it.
  575  	//
  576  	// Every origin, not the manual backup and restore alone: a startup sync
  577  	// or an exit sync a launch cancelled, and a manual sync, left the same
  578  	// 130 under the same rows (#308 5-cloud-sync-and-saves claude F-CS-05).
  579  	// And only the part the stop interrupted: the stamp its trap wrote this
  580  	// run, whichever script and flags (the settings stamps included).
  581  	if (cancelled)
  582  		restampStoppedParts(mCommand, mStampsBefore, mStartedAt, token);
  583  
  584  	// Offline achievements no longer ride this card (fork #292, D-RA-030):
  585  	// the proxy sends them the moment RetroAchievements answers, and that
  586  	// send has a card of its own on the link's return (ProxyCards). The
  587  	// exit card says what happened to the saves and nothing else.
  588  
  589  	// One surface for the whole event.
  590  	//
  591  	// The card used to vanish the instant the work ended, and the outcome
  592  	// arrived as a GuiInfoPopup: a different shape, in a different place,
  593  	// at exactly the moment somebody is looking for the answer. Two things
  594  	// appeared where one thing happened. Say it in the card that has been
  595  	// reporting all along, hold it long enough to read, and let that same
  596  	// card fade.
  597  	bool lingerShort = false;   // a completed run with nothing to act on: a shorter linger, below
  598  	if (mWndNotification != nullptr)
  599  	{
  600  		mWndNotification->updateTitle(ICONINDEX + mTitle);
  601  
  602  		// The action line, blank until now: what is in place, and how to
  603  		// recover (D-CLOUD-077). The in-place clause is the verb's; "moved"
  604  		// is whether rclone's byte totals ever left zero. The recovery
  605  		// clause names the surface that runs it again: for an automatic
  606  		// sync, when that is; for one the player pressed, the row.
  607  		// A run that ended for want of a network after bytes had left
  608  		// (cloud_backup exits 69 when the link goes part way, the S3 case):
  609  		// its outcome word is SKIPPED, which says nothing moved, so the
  610  		// in-place clause -- THE SAVES THAT MADE IT ARE ON BOTH SIDES -- is
  611  		// kept in every candidate rather than dropped first (#307 PL-072).
  612  		// A run whose script stamped the cut (offlineGaps) says COULDN'T
  613  		// FINISH above and takes the in-place clause as every failure does.
  614  		const bool moved = mMoved || offlineGaps;
  615  		const bool keepInPlace = mMoved && ret == CloudExit::NoNetwork && !cancelled && !gaps && !offlineGaps;
  616  		std::vector<std::string> action;
  617  		if (completed)
  618  		{
  619  			// A completed sync has a blank action line.
  620  		}
  621  		else if (mOrigin == Origin::Exit && ret == CloudExit::NoNetwork)
  622  		{
  623  			// The exit sync could not run for want of a connection: the
  624  			// action line says what happens next to the saves. Candidates
  625  			// longest first, as everywhere on this card: the in-place clause
  626  			// goes first when the line is short of room. And there is a
  627  			// mechanism behind the sentence (D-RA-030): the link's return
  628  			// runs the sync that is owed, with a card (ProxyCards).
  629  			const std::string inPlace = inPlaceClause(CloudText::verbOf(mCommand), moved);
  630  			// When awards earned offline wait in the proxy's queue, the line
  631  			// names them too (fork #298): they go with the saves at the link's
  632  			// return (ProxyCards). The ctl is asked here, off the interface
  633  			// thread; a device without the proxy has no awards to name.
  634  			const bool awardsWaiting = OfflineAchievements::available() && OfflineAchievements::toggleOn()
  635  				&& OfflineAchievements::pendingAwards() > 0;
  636  			if (awardsWaiting)
  637  				LOG(LogInfo) << "ThreadedCloudSync: the exit card names the achievements waiting to be sent";
  638  			// The title already says SYNCING SAVES; the line says when, and
  639  			// nothing the title said (D-UI-107).
  640  			const std::string savesWaiting = awardsWaiting
  641  				? _("THEY'LL GO UP NEXT TIME YOU'RE CONNECTED, WITH YOUR ACHIEVEMENTS.")
  642  				: _("THEY'LL GO UP NEXT TIME YOU'RE CONNECTED.");
  643  			std::vector<std::string> recoveries = { savesWaiting };
  644  			if (awardsWaiting)
  645  				recoveries.push_back(_("THEY GO UP WITH YOUR ACHIEVEMENTS WHEN YOU'RE BACK."));
  646  			// A run that moved saves before the link went keeps saying so
  647  			// in every candidate: SKIPPED above says nothing moved (#307
  648  			// PL-072, CloudText::actionCandidates).
  649  			action = CloudText::actionCandidates(inPlace, recoveries, keepInPlace);
  650  		}
  651  		else
  652  		{
  653  			const CloudText::Verb verb = CloudText::verbOf(mCommand);
  654  			// Nothing ran on a sync with no folder to sync with: no in-place
  655  			// clause, and the one line names the row (the approved action
  656  			// line, D-CLOUD-164).
  657  			const std::string inPlace = noFolder ? "" : inPlaceClause(verb, moved);
  658  
  659  			std::string recover;
  660  			if (noFolder)
  661  				recover = _("SET IT UP: GAME SETTINGS > MANAGE CLOUD STORAGE");
  662  			else if (cancelled && mGameExitSync)
  663  				recover = _("THEY GO UP WHEN YOU EXIT THE GAME.");
  664  			else if (mOrigin == Origin::Startup)
  665  				recover = _("IT'LL TRY AGAIN AT STARTUP, OR SYNC NOW FROM GAME SETTINGS.");
  666  			else if (mOrigin == Origin::Exit)
  667  				recover = _("IT'LL TRY AGAIN WHEN YOU EXIT A GAME.");
  668  			else if (ret == CloudExit::NoNetwork)
  669  				recover = _("TRY AGAIN WHEN YOU'RE ONLINE.");
  670  			else if (ret == CloudExit::LockHeld)
  671  				recover = _("WAIT FOR IT TO FINISH, THEN TRY AGAIN.");
  672  			else if (mOrigin == Origin::Manual)
  673  				recover = _("TRY AGAIN FROM GAME SETTINGS > ") + std::string(
  674  					verb == CloudText::Verb::Sync ? _("SYNC SAVES WITH THE CLOUD")
  675  					: verb == CloudText::Verb::Restore ? _("RESTORE SAVES FROM THE CLOUD")
  676  					: _("BACK UP SAVES TO THE CLOUD"));
  677  			else
  678  				recover = _("TRY AGAIN FROM MANAGE CLOUD STORAGE > BACK UP TO THE CLOUD");
  679  
  680  			// Candidates, longest first; the card measures them in the row's
  681  			// own font on the interface thread and shows the first that
  682  			// fits (AsyncNotificationComponent). If both clauses do not fit
  683  			// on the one line, the in-place clause goes first
  684  			// (es-native-ui.md): the outcome word above already implies
  685  			// it, and the recovery is the part nobody can guess. The
  686  			// startup sentence has a short form for a panel where even it
  687  			// alone does not fit.
  688  			std::vector<std::string> recoveries = { recover };
  689  			if (mOrigin == Origin::Startup && !noFolder)
  690  				recoveries.push_back(_("IT'LL TRY AGAIN NEXT STARTUP."));
  691  			action = CloudText::actionCandidates(inPlace, recoveries, keepInPlace);
  692  		}
  693  		// The outcome line, from candidates too, and for the same reason
  694  		// as the action line (#115): it is composed -- the outcome word,
  695  		// then the why -- and the why is a whole sentence. Longest first:
  696  		// the whole thing, then the why with its trailing clause dropped,
  697  		// then the outcome word alone, which fits any panel this runs on.
  698  		// A translation whose outcome line carries no " - " has no split
  699  		// to make and gets the single candidate it has today.
  700  		mWndNotification->updateText(CloudText::outcomeCandidates(outcome), action);
  701  
  702  		// A full bar on success; otherwise the bar goes, because a progress
  703  		// bar left standing under COULDN'T FINISH reads as a measure of how
  704  		// much of the failure has completed.
  705  		mWndNotification->updatePercent(completed ? 100 : -1);
  706  		lingerShort = completed && action.empty();
  707  	}
  708  
  709  	// Nothing is running any more, so stop claiming otherwise: somebody who
  710  	// wants to start another sync while the card is still up should not be
  711  	// told one is already going. Under the lock, so a cancelForLaunch that
  712  	// has just taken the pointer finishes with it before it goes -- and the
  713  	// delete below is a linger later. Whether or not there was a card: this
  714  	// used to happen only inside the card's branch, leaving a run with no
  715  	// card to the destructor's unlocked clear (#308 F-CS-25).
  716  	{
  717  		std::lock_guard<std::mutex> lock(sInstanceLock);
  718  		if (ThreadedCloudSync::mInstance == this)
  719  			ThreadedCloudSync::mInstance = nullptr;
  720  	}
  721  
  722  	if (mWndNotification != nullptr)
  723  	{
  724  		// Hold the outcome long enough to read, then let the card fade.
  725  		// Success is one word and a full bar, and somebody who just exited
  726  		// a game is standing there watching it, so a second and a half (two
  727  		// lingered -- maintainer, 2026-09-07); anything else is two lines to
  728  		// act on, so five. Five for everything dated from when a sync took
  729  		// 18 seconds -- once the exit sync came down to about five, the card
  730  		// spent as long saying it was done as it had spent working.
  731  		std::this_thread::sleep_for(std::chrono::milliseconds(lingerShort ? 1500 : 5000));
  732  	}
  733  
  734  	// A question the run asked us to put to the player, once its card has
  735  	// had its say -- and only when the run completed: an offer to create a
  736  	// folder on top of a failure is one thing too many to read at once. The
  737  	// dialog itself is CloudOffer's, shared with the transfer page, so the
  738  	// two surfaces that run these scripts cannot ask it in different words
  739  	// (#145). It pushes on the interface thread itself.
  740  	if (completed)
  741  		CloudOffer::present(mWindow, mOffer, mOfferArgs);
  742  
  743  	// The offline achievements' send card follows an automatic sync's
  744  	// (fork #292, D-RA-030): the proxy sends the moment RetroAchievements
  745  	// answers, and the link's own card stands aside while a sync card is
  746  	// up, so this end is where a batch that went during the sync is said.
  747  	// Not after a launch cancel: the player is on their way into a game.
  748  	// And not after a sync that found no network: the proxy is holding
  749  	// its awards for the link, and a card following a queue that cannot
  750  	// empty would say COULDN'T FINISH over an exit the maintainer asked to
  751  	// leave quiet (the v2 proof, 2026-09-26: the exit card's end started
  752  	// the send card offline, and the link's own card, finding one up,
  753  	// dropped the sync it owed).
  754  	if (!cancelled && ret != CloudExit::NoNetwork && (mOrigin == Origin::Exit || mOrigin == Origin::Startup))
  755  		ProxyCards::afterSync(mWindow);
  756  
  757  	delete this;
  758  }
  759  
  760  void ThreadedCloudSync::start(Window* window, const std::string& command,
  761  	const std::string& title, const std::string& running, Origin origin)
  762  {
  763  	// Or a back up, restore or match still current on the transfer page
  764  	// (fork #187; the page is sat in since D-UI-078, so this is the seam's
  765  	// guard rather than an everyday path): the scripts' flock would answer
  766  	// this run with CloudExit::LockHeld and the card would say these same
  767  	// words after starting; said here, before, in the words the flock's
  768  	// code reads as.
  769  	//
  770  	// The check and the install are one hold of the lock (#308 F-CS-25): the
  771  	// check used to be made before the lock was taken, so two starts at once
  772  	// could both find nothing running and both install a sync.
  773  	{
  774  		std::lock_guard<std::mutex> lock(sInstanceLock);
  775  		if (ThreadedCloudSync::mInstance == nullptr && !CloudTransferJob::running())
  776  		{
  777  			ThreadedCloudSync::mInstance = new ThreadedCloudSync(window, command, title, running, origin);
  778  			return;
  779  		}
  780  	}
  781  	window->pushGui(new GuiMsgBox(window, _("A SYNC IS ALREADY RUNNING.")));
  782  }
  783  
  784  bool ThreadedCloudSync::cancelForLaunch(CancelRefusal* refusal, bool evenIfPlayerStarted)
  785  {
  786  	// Stopping unless we find otherwise: it covers the sync that was
  787  	// signalled and has not gone yet, and the one that had already gone
  788  	// before we took the lock. Both are answered by trying again in a
  789  	// moment; only the player's own sync is answered by waiting.
  790  	if (refusal != nullptr)
  791  		*refusal = CancelRefusal::Stopping;
  792  
  793  	ThreadedCloudSync* sync = nullptr;
  794  	pid_t pid = 0;
  795  	{
  796  		std::lock_guard<std::mutex> lock(sInstanceLock);
  797  		sync = ThreadedCloudSync::mInstance;
  798  		if (sync == nullptr)
  799  			return false;
  800  		// The player pressed this one; a launch does not override it on its
  801  		// own -- only their answer to the question does (D-CLOUD-129).
  802  		if (!evenIfPlayerStarted && sync->mOrigin != Origin::Startup && sync->mOrigin != Origin::Exit)
  803  		{
  804  			if (refusal != nullptr)
  805  				*refusal = CancelRefusal::PlayerStarted;
  806  			return false;
  807  		}
  808  
  809  		// Cancelled before the signal, so run() finds it set however quickly
  810  		// pclose returns. The whole group: the command runs under setsid, so
  811  		// its pid is its process group, and the scripts, their rclone and any
  812  		// ping or sleep are in it.
  813  		sync->mCancelled = true;
  814  		sync->mWaitingForNetwork = false;
  815  		pid = sync->mPid;
  816  		if (pid > 0)
  817  			::kill(-pid, SIGTERM);
  818  	}
  819  
  820  	// Now wait for it to be gone, and only then let the launch go ahead.
  821  	//
  822  	// The signal is not the end of the sync; the process ending is. rclone
  823  	// copy writes each file under a temporary name and renames it into
  824  	// place when complete, and a rename that lands after the emulator has
  825  	// opened that save is the one thing this gate exists to prevent -- a
  826  	// game about to write a save must not have a restore rename over it
  827  	// underneath. So the launch waits for run() to report the process gone:
  828  	// it clears mInstance under the lock once pclose has returned, which
  829  	// is once every writer to the pipe has exited. Two seconds is the
  830  	// budget; at one and a half the group is sent SIGKILL, for an rclone
  831  	// that is slow to act on SIGTERM. Past the budget the answer is no, and
  832  	// the caller refuses the launch as it always did -- a sync that will
  833  	// not die is not one to start a game over.
  834  	const auto started = std::chrono::steady_clock::now();
  835  	bool killed = false;
  836  	for (;;)
  837  	{
  838  		{
  839  			std::lock_guard<std::mutex> lock(sInstanceLock);
  840  			if (ThreadedCloudSync::mInstance != sync)
  841  				return true;
  842  			// Its first line had not arrived when we looked -- the command
  843  			// was only just started. Signal it as soon as it says who it is.
  844  			// Safe to read: mInstance still names it, so it is not deleted.
  845  			if (pid <= 0)
  846  			{
  847  				pid = sync->mPid;
  848  				if (pid > 0)
  849  					::kill(-pid, SIGTERM);
  850  			}
  851  		}
  852  
  853  		const long elapsed = (long) std::chrono::duration_cast<std::chrono::milliseconds>(
  854  			std::chrono::steady_clock::now() - started).count();
  855  		if (elapsed >= 2000)
  856  			return false;
  857  		if (!killed && elapsed >= 1500 && pid > 0)
  858  		{
  859  			::kill(-pid, SIGKILL);
  860  			killed = true;
  861  		}
  862  		std::this_thread::sleep_for(std::chrono::milliseconds(20));
  863  	}
  864  }
  865  
  866  // /storage/.cache/cloud_sync/last-sync-<origin>: one line, "<epoch> <rc>
  867  // <token>[ <why>]" -- the first two fields the shape the scripts give
  868  // last-backup and last-restore, so one reader (GuiMenu's cloudLastRunDetail)
  869  // serves all of them; the third and any after it are additive (D-UI-028):
  870  // the one-word token names the outcome where the code alone cannot (a 130
  871  // that was a launch cancel against one that was not; a composed run that
  872  // completed with gaps), and the why is the scripts' own sentence when they
  873  // printed one, for the row to show in place of the token's phrase. Readers
  874  // split on space and read what is there. Device-local, so under .cache
  875  // rather than .config: a stamp carried in a settings backup onto a second
  876  // device would describe a run that device never made.
  877  //
  878  // Written whole or not at all. A temp file and a rename: the reader is the
  879  // menu, on another thread and possibly at this moment, and a half-written
  880  // line parses as "never" -- the one thing the stamp exists to stop the row
  881  // saying after a run.
  882  void ThreadedCloudSync::recordOutcome(Origin origin, int rc, const std::string& token, const std::string& why)
  883  {
  884  	const char* name = origin == Origin::Startup ? "startup"
  885  		: origin == Origin::Exit ? "exit"
  886  		: origin == Origin::Manual ? "manual" : nullptr;
  887  	if (name == nullptr)
  888  		return;
  889  	writeStamp(std::string("/storage/.cache/cloud_sync/last-sync-") + name, rc, token, why);
  890  }
  891  
  892  static const std::string STAMP_DIR = "/storage/.cache/cloud_sync/";
  893  
  894  std::vector<CloudText::StampText> ThreadedCloudSync::readStamps(const std::string& command)
  895  {
  896  	std::vector<CloudText::StampText> stamps;
  897  	for (auto& name : CloudText::scriptStampNames(command))
  898  	{
  899  		const std::string path = STAMP_DIR + name;
  900  		std::string version;
  901  		struct stat st;
  902  		if (::stat(path.c_str(), &st) == 0)
  903  			version = std::to_string((unsigned long long) st.st_ino) + ":" + std::to_string((long long) st.st_mtim.tv_sec)
  904  				+ "." + std::to_string((long long) st.st_mtim.tv_nsec);
  905  		stamps.push_back({ name, version.empty() ? std::string() : Utils::FileSystem::readAllText(path), version });
  906  	}
  907  	return stamps;
  908  }
  909  
  910  void ThreadedCloudSync::restampStoppedParts(const std::string& command, time_t runStarted, const std::string& token)
  911  {
  912  	for (auto& name : CloudText::stampsToRestamp(readStamps(command), runStarted))
  913  	{
  914  		writeStamp(STAMP_DIR + name, CloudExit::Stopped, token, "");
  915  		LOG(LogInfo) << "ThreadedCloudSync: " << name << " restamped as " << token;
  916  	}
  917  }
  918  
  919  void ThreadedCloudSync::restampStoppedParts(const std::string& command, const std::vector<CloudText::StampText>& before,
  920  	time_t runStarted, const std::string& token)
  921  {
  922  	for (auto& name : CloudText::stampsToRestamp(readStamps(command), runStarted, &before))
  923  	{
  924  		writeStamp(STAMP_DIR + name, CloudExit::Stopped, token, "");
  925  		LOG(LogInfo) << "ThreadedCloudSync: " << name << " restamped as " << token;
  926  	}
  927  }
  928  
  929  // One stamp file, in the shape above, whichever surface reads it.
  930  void ThreadedCloudSync::writeStamp(const std::string& path, int rc, const std::string& token, const std::string& why)
  931  {
  932  	if (!Utils::FileSystem::createDirectory(Utils::FileSystem::getParent(path)))
  933  		return;
  934  
  935  	// One line: the why is kept to printable characters and a single line
  936  	// so the reader's split cannot be confused by it.
  937  	std::string sentence;
  938  	for (char c : why)
  939  		if (c >= 32 && c < 127)
  940  			sentence += c;
  941  	sentence = Utils::String::trim(sentence);
  942  
  943  	const std::string tmp = path + ".tmp";
  944  	Utils::FileSystem::writeAllText(tmp,
  945  		std::to_string(static_cast<long long>(time(nullptr))) + " " + std::to_string(rc) + " " + token
  946  		+ (sentence.empty() ? "" : " " + sentence) + "\n");
  947  	if (std::rename(tmp.c_str(), path.c_str()) != 0)
  948  		std::remove(tmp.c_str());
  949  }
```


## es-app/src/guis/GuiCloudTransfer.cpp @ 16dbac5211 (whole, 1077 lines)

```text
    1  #include "guis/GuiCloudTransfer.h"
    2  #include "TextFit.h"
    3  
    4  #include "guis/GuiMsgBox.h"
    5  
    6  #include "CloudExit.h"
    7  #include "CloudOffer.h"
    8  #include "CloudText.h"
    9  #include "CloudTransferJob.h"
   10  #include "ThreadedCloudSync.h"
   11  #include "Window.h"
   12  #include "ThemeData.h"
   13  #include "LocaleES.h"
   14  #include "utils/StringUtil.h"
   15  #include "utils/FileSystemUtil.h"
   16  #include "Log.h"
   17  #include "SystemData.h"
   18  
   19  #include <algorithm>
   20  #include <cctype>
   21  #include <cmath>
   22  #include <cstdio>
   23  #include <cstdlib>
   24  
   25  GuiCloudTransfer::GuiCloudTransfer(Window* window, const std::string& command, const std::string& title,
   26  	int itemsExpected, int itemsAfterContent)
   27  	: GuiCloudTransfer(window, CloudTransferJob::start(command, title, itemsExpected, itemsAfterContent))
   28  {
   29  	// start() hands back a run already in flight rather than starting a
   30  	// second (the scripts' flock would refuse it), so a page opened for one
   31  	// command may be showing another's run. It shows it truthfully -- the
   32  	// title is the run's -- and it must not take the command's completed
   33  	// action when that other run ends: a settings restore's restart (#114)
   34  	// fired by somebody else's backup finishing is the case this guards.
   35  	mOtherRun = mJob->command() != command;
   36  	if (mOtherRun)
   37  		LOG(LogWarning) << "GuiCloudTransfer: a run is already in flight; showing it in place of: " << command;
   38  }
   39  
   40  GuiCloudTransfer::GuiCloudTransfer(Window* window, const std::shared_ptr<CloudTransferJob>& job)
   41  	: GuiComponent(window), mBusyAnim(window, ""), mBackground(window, ":/frame.png"),
   42  	  mJob(job), mOtherRun(false), mShownFinished(false), mShownPercent(-1), mAlive(std::make_shared<bool>(true))
   43  {
   44  	auto theme = ThemeData::getMenuTheme();
   45  	mBackground.setImagePath(theme->Background.path);
   46  	mBackground.setEdgeColor(theme->Background.color);
   47  	mBackground.setCenterColor(theme->Background.centerColor);
   48  	mBackground.setCornerSize(theme->Background.cornerSize);
   49  
   50  	const float SW = Renderer::getScreenWidth();
   51  	const float SH = Renderer::getScreenHeight();
   52  	setSize(SW, SH);
   53  
   54  	mTextFont  = theme->Text.font;
   55  	mSmallFont = theme->TextSmall.font;
   56  	mTitle    = std::make_shared<TextComponent>(window, Utils::String::toUpper(mJob->title()), theme->Title.font, theme->Title.color, ALIGN_CENTER);
   57  	mStatus   = std::make_shared<TextComponent>(window, _("PREPARING..."), mTextFont,  theme->Text.color,      ALIGN_CENTER);
   58  	mCounter  = std::make_shared<TextComponent>(window, "",                mSmallFont, theme->TextSmall.color, ALIGN_CENTER);
   59  	mActivity = std::make_shared<TextComponent>(window, "",                mTextFont,  theme->Text.color,      ALIGN_CENTER);
   60  	mDetail   = std::make_shared<TextComponent>(window, "",                mSmallFont, theme->TextSmall.color, ALIGN_CENTER);
   61  	mNote     = std::make_shared<TextComponent>(window, "",                mSmallFont, theme->TextSmall.color, ALIGN_CENTER);
   62  	mElapsed  = std::make_shared<TextComponent>(window, "",                mSmallFont, theme->TextSmall.color, ALIGN_CENTER);
   63  	mFooter   = std::make_shared<TextComponent>(window, "",                mSmallFont, theme->TextSmall.color, ALIGN_CENTER);
   64  
   65  	// One column, 0.78 of the width, every line fitted to it (fitOneLine) so a
   66  	// long ROM name is clipped rather than wrapped into the line beneath -- the
   67  	// overlap this layout replaces came from boxes that grew with their text
   68  	// while their neighbours sat at fixed heights.
   69  	const float w  = SW * 0.78f;
   70  	const float cx = SW * 0.5f;
   71  	const float x  = cx - w / 2.0f;
   72  	mLineWidth = w;
   73  	for (auto& t : { mTitle, mStatus, mCounter, mActivity, mDetail, mNote, mElapsed, mFooter })
   74  		t->setSize(w, 0);
   75  
   76  	// Rows are stacked from the fonts' own heights, not from a table of
   77  	// fractions. A TextComponent given (w, 0) is exactly font->getHeight()
   78  	// tall -- 1.5 x its tallest glyph -- and the menu fonts are the theme's:
   79  	// the shipped theme sets the title at 0.029 of the screen where ES's
   80  	// default is 0.085, so a table that clears the default is three times too
   81  	// loose for what ships. Fonts scale with min(W, H), so every row here is
   82  	// screen-relative all the same; the fractions below are what the sums
   83  	// come to.
   84  	//
   85  	//   pad  0.05 SH   above the title and below the footer. Equal: the
   86  	//                  footer used to sit on the panel's bottom edge with
   87  	//                  0.04 above the title (maintainer, 2026-09-08).
   88  	//   gap  0.02 SH   the unit of space between groups
   89  	//
   90  	//   title                          hT
   91  	//   1.5 gap
   92  	//   1 the item    2 ITEM i OF n    hM + hS   a tight pair
   93  	//   gap
   94  	//   3 the doing   4 its totals     hM + hS   a tight pair
   95  	//   0.5 gap                                  the bar is the item's, so it sits close
   96  	//   5 bar / spinner / done-note    hM        one row, whichever of the three is showing
   97  	//   1.5 gap                                  elapsed is the whole run's, so the gap opens beneath the bar
   98  	//   6 elapsed                      hS
   99  	//   gap
  100  	//   7 footer                       hS
  101  	//
  102  	//   H = 2 pad + hT + 3 hM + 4 hS + 5.5 gap
  103  	//
  104  	// Shipped theme (Roboto Bold; title 0.029, text 0.033, small 0.025 of
  105  	// min(W, H), x1.31 menu scale under 720 px):
  106  	//   640x480    hT 28.5  hM 30    hS 24    pad 24  gap 9.6   H 315 = 0.66 SH, top 0.17
  107  	//   1280x800   hT 37.5  hM 40.5  hS 31.5  pad 40  gap 16    H 453 = 0.57 SH
  108  	//   1920x1080  hT 48    hM 54    hS 42    pad 54  gap 21.6  H 605 = 0.56 SH
  109  	// ES defaults (ubuntu condensed 0.085 / 0.045 / 0.035), for a theme that
  110  	// sets no menu fonts:
  111  	//   640x480    hT 76.5  hM 42    hS 30                      H 423 = 0.88 SH
  112  	//   1920x1080  hT 135   hM 70.5  hS 55.5                    H 795 = 0.74 SH
  113  	// That is the tallest a real theme makes it. Past 0.9 SH every pitch is
  114  	// scaled down together; a glyph is two thirds of its row, so rows stay
  115  	// apart down to a factor of 0.67, further than any theme pushes it.
  116  	const float hT = theme->Title.font->getHeight();
  117  	const float hM = mTextFont->getHeight();
  118  	const float hS = mSmallFont->getHeight();
  119  	const float natural = 2 * SH * 0.05f + hT + 3 * hM + 4 * hS + 5.5f * SH * 0.02f;
  120  	const float fit = natural > SH * 0.9f ? (SH * 0.9f) / natural : 1.0f;
  121  	const float pad = SH * 0.05f * fit;
  122  	const float gap = SH * 0.02f * fit;
  123  	const float rT = hT * fit, rM = hM * fit, rS = hS * fit;
  124  	const float H = 2 * pad + rT + 3 * rM + 4 * rS + 5.5f * gap;
  125  	const float top = (SH - H) / 2.0f;
  126  
  127  	float y = top + pad;
  128  	mTitle   ->setPosition(x, y);
  129  	y += rT + 1.5f * gap;
  130  	mStatus  ->setPosition(x, y);          // 1. the item
  131  	mCounter ->setPosition(x, y + rM);     // 2. ITEM i OF n
  132  	y += rM + rS + gap;
  133  	mActivity->setPosition(x, y);          // 3. what it is doing on it
  134  	mDetail  ->setPosition(x, y + rM);     // 4. that item's files and bytes
  135  	y += rM + rS + 0.5f * gap;
  136  	// 5. The bar, the spinner and the done-note share one row, centred on it.
  137  	// The bar used to be drawn a row below the spinner it replaced, so the
  138  	// page's centre of gravity moved every time the percentage came and went.
  139  	// No caption on the spinner: line 3 already says WORKING..., and the
  140  	// caption is set at construction because BusyComponent::setText("") is a
  141  	// no-op against its empty initial state -- the default WORKING... showed
  142  	// beside the spinner, twice on one screen (maintainer, 2026-09-06).
  143  	mBusyAnim.setBackgroundVisible(false);
  144  	mBusyAnim.setSize(w, rM);
  145  	mBusyAnim.setPosition(x, y);
  146  	mBarW = SW * 0.6f;
  147  	mBarH = SH * 0.014f;
  148  	mBarX = cx - mBarW / 2.0f;
  149  	mBarY = y + (rM - mBarH) / 2.0f;
  150  	// Once the run is over the bar's row is free, and it is where the one
  151  	// thing left to do goes: a content run that changed the ROMs on this
  152  	// device is not visible in the game lists until they are rebuilt, and
  153  	// nobody should have to know that (maintainer, 2026-09-07).
  154  	mNote    ->setPosition(x, y + (rM - hS) / 2.0f);
  155  	y += rM + 1.5f * gap;
  156  	mElapsed ->setPosition(x, y);          // 6. elapsed
  157  	y += rS + gap;
  158  	mFooter  ->setPosition(x, y);          // 7. the notice; y + rS + pad == top + H
  159  
  160  	mPanelSize = Vector2f(w + SW * 0.06f, H);
  161  	mPanelPos  = Vector2f(cx - mPanelSize.x() / 2.0f, top);
  162  	mBackground.fitTo(mPanelSize, Vector3f(mPanelPos.x(), mPanelPos.y(), 0), Vector2f(-32, -32));
  163  }
  164  
  165  // Nothing to join: the run is the job's (CloudTransferJob), not this
  166  // page's. The page that owned its worker made quitting the interface wait
  167  // on a restore (before #187); since D-UI-078 the page is sat in and a run
  168  // ends by finishing or by CANCEL, so this destructor meets a finished or a
  169  // cancelled run in practice -- and a running one only if the page were
  170  // popped by something other than the player, which the job survives.
  171  GuiCloudTransfer::~GuiCloudTransfer()
  172  {
  173  	if (mAlive)
  174  		*mAlive = false;
  175  }
  176  
  177  // Set before the page is pushed and read on the interface thread alone
  178  // (input, update, getHelpPrompts), so no lock: the run's mutex guards the
  179  // run's state, and this is the page's.
  180  void GuiCloudTransfer::setAutoContinue(const std::function<void()>& action)
  181  {
  182  	if (mOtherRun)
  183  	{
  184  		LOG(LogWarning) << "GuiCloudTransfer: auto-continue refused, the page shows another command's run";
  185  		return;
  186  	}
  187  	mAutoContinue = action;
  188  }
  189  
  190  void GuiCloudTransfer::setFailedNote(const std::string& note)
  191  {
  192  	mFailedNote = note;
  193  }
  194  
  195  void GuiCloudTransfer::setDismissedAction(const std::function<void()>& action)
  196  {
  197  	mDismissedAction = action;
  198  }
  199  
  200  // The completed run's step, taken from a posted function (update() must
  201  // not delete the page it is updating): the run is dismissed as a press
  202  // would dismiss it, the page goes, and the step runs with the window.
  203  void GuiCloudTransfer::advance()
  204  {
  205  	std::function<void()> action = mAutoContinue;
  206  	CloudTransferJob::dismiss(mJob);
  207  	delete this;
  208  	if (action)
  209  		action();
  210  }
  211  
  212  void GuiCloudTransfer::setCompletedAction(const std::function<void()>& action, const std::string& helpVerb,
  213  	const std::string& footer, const std::string& note, bool cancellable)
  214  {
  215  	if (mOtherRun)
  216  	{
  217  		LOG(LogWarning) << "GuiCloudTransfer: completed action refused, the page shows another command's run";
  218  		return;
  219  	}
  220  	mCompletedAction = action;
  221  	mActionCancellable = cancellable;
  222  	mCompletedHelpVerb = helpVerb;
  223  	mCompletedFooter = footer;
  224  	mCompletedNote = note;
  225  }
  226  
  227  void GuiCloudTransfer::clearDoneRows()
  228  {
  229  	if (mNote) mNote->setText("");
  230  	if (mCounter) mCounter->setText("");
  231  	if (mDetail) mDetail->setText("");
  232  }
  233  
  234  // While the transfer runs, B asks whether to cancel it (D-UI-078: the page
  235  // is sat in, and CANCEL is the one way out); every other press is
  236  // refused, since there is nothing to choose and a stray press should not
  237  // dismiss a page somebody is waiting on. Not B either on a page whose
  238  // completed run has an action in place of an exit (setCompletedAction): a
  239  // settings restore is replacing the configuration under this process, and
  240  // there is nowhere safe to go while it does. Once it has finished the page
  241  // waits for the person rather than the other way round: any button
  242  // dismisses it, and when the run did not complete, A runs the same command
  243  // again from this page -- the surface that reported the failure carries the
  244  // retry (D-CLOUD-077, D-UI-028). A question the run asked us to put to the
  245  // player is raised as the page goes, once the outcome has been read (#145).
  246  bool GuiCloudTransfer::input(InputConfig* config, Input input)
  247  {
  248  	if (!input.value)
  249  		return true;
  250  	CloudTransferJob& job = *mJob;
  251  	std::unique_lock<std::mutex> lock(job.mMutex);
  252  	if (!job.mFinished)
  253  	{
  254  		if (cancellable() && config->isMappedTo(BUTTON_BACK, input))
  255  		{
  256  			lock.unlock();
  257  			askCancel();
  258  		}
  259  		return true;
  260  	}
  261  	const Outcome o = outcome(job);
  262  	// OK, the player's mapping: the literal "a" was back's own button on a
  263  	// swapped one, so back retried (#308 5-cloud claude F-CS-07). Not a
  264  	// match: the same apply again is always refused (retries(), below).
  265  	if (!o.completed && retries(job) && config->isMappedTo(BUTTON_OK, input))
  266  	{
  267  		// A new run of the same command; the finished one is let go, and the
  268  		// page shows the new run from its first line. The command is
  269  		// unchanged, so a backup that includes the settings archive
  270  		// re-archives on retry -- rotation keeps three, and stripping the
  271  		// parts that finished is not worth the complexity.
  272  		const std::string command = job.mCommand, title = job.mTitle;
  273  		const int items = job.mItemsExpected, after = job.mItemsAfterContent;
  274  		lock.unlock();
  275  		mJob = CloudTransferJob::start(command, title, items, after);
  276  		clearDoneRows();
  277  		mShownFinished = false;
  278  		mShownPercent = -1;
  279  		updateHelpPrompts();
  280  		return true;
  281  	}
  282  	// A restore may have brought files into folders the lists scanned at
  283  	// boot -- screenshots in particular (#82). Re-read what changed once this
  284  	// page is gone -- when any part of the run finished, not only when all
  285  	// of it did: a saves restore that landed under a ROMs restore that did
  286  	// not still put screenshots where the lists cannot see them.
  287  	bool anyTierOk = false;
  288  	for (auto& t : job.mTiers)
  289  		if (t.rc == 0 || t.rc == 9)
  290  			anyTierOk = true;
  291  	const bool restored = (o.completed || anyTierOk) && job.mCommand.find("restore") != std::string::npos;
  292  	// A completed run with an action set has nowhere to go back to
  293  	// (setCompletedAction), so the press that would have closed the page
  294  	// takes the action instead. Copied out first: the page is gone by the
  295  	// time it runs.
  296  	std::function<void()> completedAction;
  297  	if (o.completed && mCompletedAction)
  298  		completedAction = mCompletedAction;
  299  	else if (o.completed && mAutoContinue && !mOtherRun)
  300  		completedAction = mAutoContinue;   // a press in the frame before the posted step: the same step
  301  	// The close's own step when there is no completed one (setDismissedAction).
  302  	const std::function<void()> dismissedAction = completedAction ? std::function<void()>() : mDismissedAction;
  303  	// A question a script asked us to put to the player (#100, #127, #145),
  304  	// raised here rather than when the line arrived: this page ends when it
  305  	// is dismissed (es-native-ui.md, the fourth tier), and the run's outcome
  306  	// is what it exists to show. Raising the offer mid-run would put a
  307  	// dialog over a page somebody is watching, and raising it the instant
  308  	// the run ended would cover the outcome with a question about why there
  309  	// was nothing to restore -- least-surprise.md: what the screen told them
  310  	// happens first, then what to do about it.
  311  	//
  312  	// Not when the completed run has an action instead of an exit: that
  313  	// action is a restart, and a dialog it is about to take away is worse
  314  	// than no dialog. Nothing composes the two today -- a settings restore
  315  	// is its own run -- and if one ever does, the restart owns the moment.
  316  	std::string offer;
  317  	std::vector<std::string> offerArgs;
  318  	if (o.completed && !completedAction)
  319  	{
  320  		offer = job.mOffer;
  321  		offerArgs = job.mOfferArgs;
  322  	}
  323  	lock.unlock();
  324  	// The outcome has been read: the run is no longer the CLOUD page's to
  325  	// report, and its row goes back to saying what it does (fork #187).
  326  	CloudTransferJob::dismiss(mJob);
  327  	Window* window = mWindow;
  328  	delete this;
  329  	if (completedAction)
  330  	{
  331  		completedAction();
  332  		return true;
  333  	}
  334  	if (restored)
  335  		window->postToUiThread([] { SystemData::rescanChangedFolders(); });
  336  	if (dismissedAction)
  337  	{
  338  		dismissedAction();
  339  		return true;
  340  	}
  341  	CloudOffer::present(window, offer, offerArgs);
  342  	return true;
  343  }
  344  
  345  // What cancelling means, read at the moment of deciding (D-UI-023): each
  346  // file rclone moves is renamed into place whole, so what is across stays,
  347  // and the next run finishes what this one did not (D-CLOUD-077). YES first,
  348  // NO last so B answers NO. Nothing of the page is captured: the stop is a
  349  // static call on the run in flight, and the page shows the outcome as the
  350  // run ends.
  351  void GuiCloudTransfer::askCancel()
  352  {
  353  	const auto kind = CloudText::transferKind(mJob->mCommand);
  354  	mWindow->pushGui(new GuiMsgBox(mWindow,
  355  		kind == CloudText::TransferKind::Scan ? _("CANCEL THIS CHECK?\n\nNO FILES HAVE BEEN MOVED. YOU CAN CHECK AGAIN LATER.")
  356  			 : kind == CloudText::TransferKind::Create ? _("STOP CREATING FOLDERS?\n\nFOLDERS ALREADY CREATED WILL STAY. YOU CAN TRY AGAIN LATER.")
  357  			 : _("CANCEL THIS BACKUP OR RESTORE?") + std::string("\n\n")
  358  			+ _("WHAT'S ALREADY IN PLACE STAYS. THE NEXT BACKUP OR RESTORE FINISHES WHAT THIS ONE DIDN'T."),
  359  		_("YES"), [] { CloudTransferJob::stopByPlayer(); },
  360  		_("NO"), nullptr));
  361  }
  362  
  363  // Whether the same command again can do what this run did not. A match
  364  // cannot: its apply spends the preview's plan before anything runs
  365  // (cloud_content_restore, PL-001), so a second apply is refused with
  366  // SOMETHING CHANGED SINCE YOU CHECKED, and the page names the match's row
  367  // instead (CloudText::matchRecovery, #308 gpt F-CS-26).
  368  bool GuiCloudTransfer::retries(const CloudTransferJob& job)
  369  {
  370  	return CloudText::transferKind(job.mCommand) != CloudText::TransferKind::Match;
  371  }
  372  
  373  std::vector<HelpPrompt> GuiCloudTransfer::getHelpPrompts()
  374  {
  375  	std::vector<HelpPrompt> prompts;
  376  	CloudTransferJob& job = *mJob;
  377  	std::unique_lock<std::mutex> lock(job.mMutex);
  378  	if (!job.mFinished)
  379  	{
  380  		if (cancellable())
  381  			prompts.push_back(HelpPrompt(BUTTON_BACK, _("CANCEL")));
  382  		return prompts;
  383  	}
  384  	const Outcome o = outcome(job);
  385  	if (!o.completed && retries(job))
  386  		prompts.push_back(HelpPrompt(BUTTON_OK, _("TRY AGAIN")));
  387  	// The page's one exit says what it does: CLOSE, or the word the
  388  	// action was given (setCompletedAction).
  389  	prompts.push_back(HelpPrompt(BUTTON_BACK, o.completed && mCompletedAction && !mCompletedHelpVerb.empty()
  390  		? mCompletedHelpVerb : _("CLOSE")));
  391  	return prompts;
  392  }
  393  
  394  // The word for the run (D-UI-028; es-native-ui.md "Outcome vocabulary").
  395  //
  396  // COMPLETED when every part did -- rclone's 9, nothing needed moving,
  397  // counts. Everything short of that is COULDN'T FINISH, including a run
  398  // whose parts disagree: a tier that finished
  399  // beside one that did not, a unit that finished inside a tier that did not
  400  // (its later units failed with a why of their own), or a match cut off
  401  // after it had already removed files. Those used to read COMPLETED WITH
  402  // GAPS; a half-outcome the player cannot act on reads as "working kind of"
  403  // and costs more trust than a plain failure does (maintainer, 2026-09-10,
  404  // D-UI-030). `partial` survives as the flag that shapes the lines below --
  405  // what moved is still said, and line 4 still names the items that did not
  406  // finish -- but it no longer changes the word. SKIPPED for the two sentinels the
  407  // scripts exit before touching anything (CloudExit.h), when that is all
  408  // the run has to report; they are not failures, and FAILED would send
  409  // somebody to a log to find nothing wrong. COULDN'T FINISH for everything
  410  // else; the why goes on line 4 with the items it stopped. A run with no
  411  // tier lines -- the match, or a command composed before they existed -- is
  412  // read from its exit code alone, as it always was.
  413  //
  414  // Skipped means nothing was touched. A run that had moved bytes or finished
  415  // a file before the network went was cut, not skipped, and its exit 69 reads
  416  // COULDN'T FINISH like any other cut (#153, 2026-09-21: a settings archive
  417  // cut at 75 % on S3 read SKIPPED - YOU'RE NOT ONLINE over WHAT MADE IT IS IN
  418  // YOUR CLOUD, two words wrong in the same direction the vocabulary keeps
  419  // apart).
  420  GuiCloudTransfer::Outcome GuiCloudTransfer::outcome(const CloudTransferJob& job)
  421  {
  422  	Outcome o;
  423  	// Stopped by a launch the player chose over it (D-CLOUD-129): the
  424  	// card's own phrase for the same thing (ThreadedCloudSync's cancel), and
  425  	// no failed item -- nothing went wrong, and the next run finishes what
  426  	// this one did not.
  427  	if (job.mStoppedForGame || job.mStoppedByPlayer)
  428  	{
  429  		o.completed = false;
  430  		o.partial = false;
  431  		o.skipped = true;
  432  		o.word = job.mStoppedByPlayer ? _("SKIPPED - YOU CANCELLED IT") : _("SKIPPED - YOU STARTED A GAME");
  433  		return o;
  434  	}
  435  	o.completed = job.mExit == 0 || job.mExit == 9;
  436  	bool anyOk = false, anyBad = false, anyUnitOk = false;
  437  	int onlyCode = -2;   // the one code every failed tier shares, or -1 when they differ
  438  	for (auto& t : job.mTiers)
  439  	{
  440  		const bool ok = t.rc == 0 || t.rc == 9;
  441  		anyOk = anyOk || ok;
  442  		anyBad = anyBad || !ok;
  443  		if (!ok)
  444  		{
  445  			if (!t.tierLevelFail && t.unitsFailed > 0 && t.unitsAnnounced > t.unitsFailed)
  446  				anyUnitOk = true;
  447  			onlyCode = onlyCode == -2 ? t.rc : onlyCode == t.rc ? onlyCode : -1;
  448  		}
  449  	}
  450  	const bool match = job.mCommand.find("--match") != std::string::npos;
  451  	o.partial = !o.completed && ((anyOk && anyBad) || anyUnitOk || (match && job.mRemovedFiles > 0));
  452  	const int code = job.mTiers.empty() ? job.mExit : onlyCode;
  453  	const bool progressed = job.mAnyTransferred || job.mRunFiles > 0 || job.mUnitFiles > 0;
  454  	o.skipped = !o.completed && !o.partial && !progressed
  455  		&& (code == CloudExit::LockHeld || code == CloudExit::NoNetwork || code == CloudExit::NoFolder);
  456  	if (o.completed)
  457  		o.word = _("COMPLETED");
  458  	else if (o.partial)
  459  		o.word = _("COULDN'T FINISH");
  460  	else if (o.skipped && code == CloudExit::LockHeld)
  461  		o.word = CloudText::lockHeldOutcome(CloudText::transferKind(job.mCommand));
  462  	else if (o.skipped && code == CloudExit::NoFolder)
  463  		o.word = _("SKIPPED - YOUR CLOUD FOLDER ISN'T SET UP YET");
  464  	else if (o.skipped)
  465  		o.word = _("SKIPPED - YOU'RE NOT ONLINE");
  466  	else
  467  		o.word = _("COULDN'T FINISH");
  468  	return o;
  469  }
  470  
  471  // The verb's word for a run, from its command (CloudText::transferKind), in
  472  // the running form the cards use (BACKING UP SAVES, SYNCING SAVES...): the
  473  // head of the hub row's line for a run that is current while the hub is
  474  // the top page (the seam left by D-UI-078; see GuiCloudTransfer.h).
  475  std::string GuiCloudTransfer::verbWord(const CloudTransferJob& job)
  476  {
  477  	switch (CloudText::transferKind(job.mCommand))
  478  	{
  479  		case CloudText::TransferKind::Backup:  return _("BACKING UP...");
  480  		case CloudText::TransferKind::Restore: return _("RESTORING...");
  481  		case CloudText::TransferKind::Match:   return _("MATCHING...");
  482  		case CloudText::TransferKind::Scan:    return _("CHECKING...");
  483  		case CloudText::TransferKind::Create:  return _("CREATING...");
  484  		default:                               return _("WORKING...");
  485  	}
  486  }
  487  
  488  // "BACKING UP... - ITEM 2 OF 4", and the item, in the words this page's
  489  // rows 1 and 2 use, so the row and the page say the same thing about the
  490  // same run. Never an OF with nothing on either side: while the count is
  491  // unknown the row reads ITEM i alone, as the page does.
  492  GuiCloudTransfer::RowWords GuiCloudTransfer::rowWords(const std::shared_ptr<CloudTransferJob>& job)
  493  {
  494  	RowWords w;
  495  	if (job == nullptr)
  496  		return w;
  497  	std::unique_lock<std::mutex> lock(job->mMutex);
  498  	w.word = verbWord(*job);
  499  	w.counted = w.word;
  500  	if (job->mItemIndex > 0)
  501  	{
  502  		w.counted += " - " + std::string(_("ITEM")) + " " + std::to_string(job->mItemIndex);
  503  		if (job->mItemCount > 0)
  504  			w.counted += " " + std::string(_("OF")) + " " + std::to_string(job->mItemCount);
  505  		w.item = unitName(job->mUnitLabel);
  506  	}
  507  	return w;
  508  }
  509  
  510  std::string GuiCloudTransfer::outcomeWord(const std::shared_ptr<CloudTransferJob>& job)
  511  {
  512  	if (job == nullptr)
  513  		return "";
  514  	std::unique_lock<std::mutex> lock(job->mMutex);
  515  	return outcome(*job).word;
  516  }
  517  
  518  std::string GuiCloudTransfer::stillRunningSentence(const std::shared_ptr<CloudTransferJob>& job)
  519  {
  520  	if (job == nullptr)
  521  		return "";
  522  	switch (CloudText::transferKind(job->command()))
  523  	{
  524  		case CloudText::TransferKind::Backup:  return _("YOUR BACKUP TO THE CLOUD IS STILL RUNNING.");
  525  		case CloudText::TransferKind::Restore: return _("YOUR RESTORE FROM THE CLOUD IS STILL RUNNING.");
  526  		case CloudText::TransferKind::Match:   return _("THIS DEVICE IS STILL BEING MATCHED TO THE CLOUD.");
  527  		case CloudText::TransferKind::Scan:    return _("YOUR CLOUD IS STILL BEING CHECKED.");
  528  		case CloudText::TransferKind::Create:  return _("YOUR CLOUD FOLDER IS STILL BEING CREATED.");
  529  		default:                               return _("YOUR CLOUD TRANSFER IS STILL RUNNING.");
  530  	}
  531  }
  532  
  533  void GuiCloudTransfer::render(const Transform4x4f& parentTrans)
  534  {
  535  	Transform4x4f trans = parentTrans * getTransform();
  536  	Renderer::setMatrix(trans);
  537  	// Dim the whole screen: this is a takeover, and the carousel showing
  538  	// through would say the app is idle while a transfer is in flight.
  539  	Renderer::drawRect(0.f, 0.f, mSize.x(), mSize.y(), 0x000000D0);
  540  
  541  	auto theme = ThemeData::getMenuTheme();
  542  
  543  	// A themed nine-patch panel and nothing else, the same surface a menu or a
  544  	// dialog draws. What separates this page from what it covers is the dim
  545  	// above, not an outline: a stroke of its own would make it the one panel
  546  	// in the app that has one.
  547  	mBackground.render(trans);
  548  
  549  	for (auto& t : { mTitle, mStatus, mCounter, mActivity, mDetail, mNote, mElapsed, mFooter })
  550  		t->render(trans);
  551  
  552  	// The bar is drawn from the snapshot update() took under the lock, along
  553  	// with the text above it -- not from the run's percent, which its worker may have
  554  	// moved on since. One block per frame, for every row and the bar alike.
  555  	if (!mShownFinished)
  556  	{
  557  		if (mShownPercent >= 0)
  558  		{
  559  			// A bar only where there is a real number behind it. An
  560  			// indeterminate spinner is honest; a bar at an invented
  561  			// position is not. The rectangle is the constructor's, on the
  562  			// spinner's row, so the two take turns in one place.
  563  			Renderer::setMatrix(trans);
  564  			Renderer::drawRect(mBarX, mBarY, mBarW, mBarH, (theme->Text.color & 0xFFFFFF00) | 0x40);
  565  			Renderer::drawRect(mBarX, mBarY, mBarW * (mShownPercent / 100.0f), mBarH, theme->Text.color);
  566  		}
  567  		else
  568  			mBusyAnim.render(trans);
  569  	}
  570  
  571  	// The keys are the help bar's, drawn here: with full-screen menus on
  572  	// (every handheld) Window draws no help while a second page is open, so
  573  	// the footer used to spell them out as A and B (es-ui-style-guide.md,
  574  	// Interaction rules; the save state manager draws its bar the same way).
  575  	if (mWindow->peekGui() == this && Renderer::ScreenSettings::fullScreenMenus())
  576  		mWindow->renderHelpPromptsEarly(parentTrans);
  577  }
  578  
  579  // Clip to one line: a long ROM name gets an ellipsis, never a second line.
  580  std::string GuiCloudTransfer::fitOneLine(const std::shared_ptr<Font>& font, std::string text, float width)
  581  {
  582  	if (!font)
  583  		return text;
  584  	// On characters, not bytes (TextFit; #308 gpt F-CS-32).
  585  	return TextFit::fitOneLine(text, width, [&font](const std::string& t) { return font->sizeText(t).x(); });
  586  }
  587  
  588  // The scripts name their two fixed units in English (">>> unit SETTINGS||",
  589  // ">>> unit SAVES||"), and the page used to show that word as it came, so
  590  // the French page read SETTINGS over ELEMENT 1 SUR 1 (#153, 2026-09-21). A
  591  // system's name from the content scripts is a directory and stays as it is.
  592  // The composers' labels in the player's language, a system's folder as it
  593  // came (CloudText::unitLabel).
  594  std::string GuiCloudTransfer::unitName(const std::string& label)
  595  {
  596  	return CloudText::unitLabel(label);
  597  }
  598  
  599  std::string GuiCloudTransfer::fitSentences(const std::shared_ptr<Font>& font, std::string text, float width)
  600  {
  601  	if (!font)
  602  		return text;
  603  	while (font->sizeText(text).x() > width)
  604  	{
  605  		// the last sentence boundary before the end: ". " with something after it
  606  		const size_t end = text.find_last_not_of(" .");
  607  		if (end == std::string::npos)
  608  			break;
  609  		const size_t cut = text.rfind(". ", end);
  610  		if (cut == std::string::npos)
  611  			break;
  612  		text = text.substr(0, cut + 1);
  613  	}
  614  	return fitOneLine(font, text, width);
  615  }
  616  
  617  // The units table, the size parser and the two formatters live in
  618  // CloudText (#140), where the sync card shares them and the unit tests can
  619  // reach them. These three stay as the names this page's callers -- and the
  620  // content picker and the match confirmation, through sizeLabel -- use.
  621  std::string GuiCloudTransfer::sizeLabel(unsigned long bytes)
  622  {
  623  	return CloudText::sizeLabel(bytes);
  624  }
  625  
  626  std::string GuiCloudTransfer::roundSizes(const std::string& f)
  627  {
  628  	return CloudText::roundSizes(f);
  629  }
  630  
  631  // rclone's fragments in the player's units, precision and separators:
  632  //   "45% /2.5Mi, 300Ki/s, 5s"                            -> "45% OF 2.5 MB . 300 KB/S . 5S LEFT"
  633  //   "1.4 GiB / 2.0 GiB, 70%, 2.5 MiB/s, ETA 3m2s"        -> "1.40 GB OF 2.00 GB . 70% . 2.5 MB/S . 3M2S LEFT"
  634  //   "16.521 MiB / 16.521 MiB, 100%, 519.844 KiB/s, ETA 0s" -> "16.5 MB OF 16.5 MB . 100% . 520 KB/S . 0S LEFT"
  635  std::string GuiCloudTransfer::prettyRclone(std::string f)
  636  {
  637  	// Piped -- there is no terminal here -- rclone cuts every per-file line
  638  	// at 80 columns, so the last field often arrives torn: "5.722 MiB/",
  639  	// "976.547 Ki". A field is a percentage, a size (ends in B), a speed
  640  	// (ends in /s), or a time (digits and h/m/s); anything else is a
  641  	// fragment and is dropped rather than shown as "5.722 MB/". A bare "-"
  642  	// is rclone's word for a value it does not have yet -- the ETA of a
  643  	// transfer that has not started, the percentage of nothing -- and is
  644  	// dropped too: it is honest, but on the page it read as broken
  645  	// ("0 B OF 0 B . - . 0 B/S . -", review 2026-09-08).
  646  	{
  647  		std::vector<std::string> kept;
  648  		for (auto& raw : Utils::String::split(f, ',', true))
  649  		{
  650  			std::string t = Utils::String::trim(raw);
  651  			if (t.empty()) continue;
  652  			std::string tail = t;
  653  			if (tail.rfind("ETA ", 0) == 0) tail = tail.substr(4);
  654  			const bool pct   = tail.back() == '%';
  655  			const bool size  = tail.back() == 'B' || (tail.size() > 2 && tail.compare(tail.size() - 2, 2, "iB") == 0);
  656  			const bool speed = tail.size() > 2 && tail.compare(tail.size() - 2, 2, "/s") == 0;
  657  			bool time = !tail.empty() && isdigit((unsigned char) tail[0]);
  658  			for (char ch : tail) if (!(isdigit((unsigned char) ch) || ch == 'h' || ch == 'm' || ch == 's')) { time = false; break; }
  659  			if (time && isdigit((unsigned char) tail.back())) time = false;
  660  			// the first field may be "45% /2.5Mi" -- a percentage and a size in one
  661  			const bool pctSize = t.find('%') != std::string::npos && t.find('/') != std::string::npos && (size || t.back() == 'i');
  662  			if (pct || size || speed || time || pctSize)
  663  				kept.push_back(t);
  664  		}
  665  		f.clear();
  666  		for (size_t i = 0; i < kept.size(); i++)
  667  			f += (i ? ", " : "") + kept[i];
  668  	}
  669  	f = roundSizes(f);
  670  	auto rep = [&f](const std::string& from, const std::string& to) { f = Utils::String::replace(f, from, to); };
  671  	for (const auto& u : CloudText::rcloneUnits())
  672  		if (std::string(u.rclone) != u.shown)
  673  			rep(u.rclone, u.shown);
  674  	rep("ETA ", "");
  675  	rep(" / ", " OF "); rep(" /", " OF ");
  676  	rep(", ", " · ");
  677  	f = Utils::String::toUpper(f);
  678  	// a trailing duration -- digits then a unit letter, no percent, no bytes --
  679  	// is time left. The separator is four bytes, not three: the middle dot is
  680  	// two in UTF-8, and skipping three left a space on the front of the last
  681  	// segment that isdigit() refused, so LEFT was never appended (2026-09-09).
  682  	static const std::string SEP = " · ";
  683  	size_t sep = f.rfind(SEP);
  684  	std::string last = sep == std::string::npos ? f : f.substr(sep + SEP.size());
  685  	if (!last.empty() && isdigit((unsigned char) last[0]) && last.find('%') == std::string::npos
  686  		&& last.find('B') == std::string::npos && !isdigit((unsigned char) last.back()))
  687  		f += " " + std::string(_("LEFT"));
  688  	return f;
  689  }
  690  
  691  void GuiCloudTransfer::update(int deltaTime)
  692  {
  693  	GuiComponent::update(deltaTime);
  694  	mBusyAnim.update(deltaTime);
  695  	CloudTransferJob& job = *mJob;
  696  	std::unique_lock<std::mutex> lock(job.mMutex);
  697  	// One snapshot per frame for the bar (render() draws from it) and the
  698  	// rows below, so they cannot show two different stats blocks. The help
  699  	// bar changes with the page -- TRY AGAIN and CLOSE once it is done --
  700  	// and is refreshed after the lock: getHelpPrompts takes it too.
  701  	const bool justFinished = job.mFinished && !mShownFinished;
  702  	mShownFinished = job.mFinished;
  703  	mShownPercent  = job.mPercent;
  704  	// A completed run with a step of its own goes on by itself
  705  	// (setAutoContinue), from a posted function rather than from inside
  706  	// this update: the window is walking its pages, and a page deleted
  707  	// under that walk is the use-after-free a press from input() never
  708  	// risks. The token says whether the page is still here when it runs.
  709  	const bool advance = justFinished && mAutoContinue && !mOtherRun && !mAdvancePosted && outcome(job).completed;
  710  	// The run's clock, not a page's: this page may be the second one opened
  711  	// on the run, and elapsed is how long the run has been going.
  712  	const int elapsedMs = job.elapsedMsLocked();
  713  	const int mins = elapsedMs / 60000;
  714  	const int secs = (elapsedMs / 1000) % 60;
  715  	char elapsed[32];
  716  	snprintf(elapsed, sizeof(elapsed), "%d:%02d", mins, secs);
  717  
  718  	if (job.mFinished)
  719  	{
  720  		// Seven lines, the same rows as the run (D-UI-024/026), now carrying
  721  		// the outcome (D-UI-028): 1 the word; 2 how many items did not finish,
  722  		// when partial; 3 what moved; 4 the items that did not finish and why; 5
  723  		// what is in place, or what to do next; 6 elapsed; 7 the buttons.
  724  		const Outcome o = outcome(job);
  725  		const bool restore = job.mCommand.find("restore") != std::string::npos;
  726  		const bool match = job.mCommand.find("--match") != std::string::npos;
  727  		mStatus->setText(fitOneLine(mTextFont, o.word, mLineWidth));
  728  
  729  		// 2. When partial, the count: N distinct items that did not finish of the
  730  		// run's M -- the run's count when a script announced it, else what
  731  		// was reached, never fewer than N.
  732  		std::string counter;
  733  		if (o.partial)
  734  		{
  735  			std::vector<std::string> names;
  736  			for (auto& f : job.mFailed)
  737  			{
  738  				const std::string name = unitName(f.label);
  739  				if (std::find(names.begin(), names.end(), name) == names.end())
  740  					names.push_back(name);
  741  			}
  742  			const int n = (int) names.size();
  743  			const int m = std::max(std::max(job.mItemCount, job.mItemIndex), n);
  744  			counter = std::to_string(n) + " " + std::string(_("OF")) + " " + std::to_string(m) + " "
  745  				+ std::string(n == 1 && m == 1 ? _("ITEM DID NOT FINISH") : _("ITEMS DID NOT FINISH"));
  746  		}
  747  		mCounter->setText(fitOneLine(mSmallFont, counter, mLineWidth));
  748  
  749  		// 3 and 4: what moved, and what did not.
  750  		if (job.mRemovedFiles > 0)
  751  		{
  752  			// A match is mostly deletion, and rclone's totals for a deletion
  753  			// are "0 B / 0 B" -- true and useless. Line 3 carries what the
  754  			// confirmation showed instead: what went. Line 4 is per system
  755  			// when the match completed, and the items it did not reach when
  756  			// it was cut (below).
  757  			std::string removed = std::string(_("REMOVED")) + " " + std::to_string(job.mRemovedFiles) + " "
  758  				+ std::string(job.mRemovedFiles == 1 ? _("FILE FROM THIS DEVICE") : _("FILES FROM THIS DEVICE"));
  759  			if (job.mRemovedBytes > 0)
  760  				removed += " · " + sizeLabel(job.mRemovedBytes);
  761  			mActivity->setText(fitOneLine(mTextFont, removed, mLineWidth));
  762  			if (o.completed)
  763  			{
  764  				std::string detail;
  765  				for (auto& d : job.mRemovedDetail)
  766  					detail += (detail.empty() ? "" : "   ") + d;
  767  				mDetail->setText(fitOneLine(mSmallFont, detail, mLineWidth));
  768  				if (job.mAnyTransferred)
  769  					mCounter->setText(fitOneLine(mSmallFont, _("FILES YOUR CLOUD HAD AND THIS DEVICE DIDN'T CAME DOWN TOO."), mLineWidth));
  770  			}
  771  		}
  772  		else
  773  		{
  774  			// Line 3 answers for the whole run, not its last unit: the page
  775  			// used to end on "SNES  3 OF 3" over that unit's totals, or over
  776  			// nothing when the last unit only compared (#85). It carries the
  777  			// sum of every unit's final "Transferred:" pair, in the run's own
  778  			// verb -- shown on a partial run too, because what moved is the half of
  779  			// the answer that is good news. Only what rclone printed: a run
  780  			// that never printed a byte line says the word and nothing more.
  781  			//
  782  			// The count is of finished files. The bytes are rclone's
  783  			// bytes-read counter, and on a run that stopped or failed that
  784  			// includes what the transfers in flight had read when it died
  785  			// and never completed -- so a run that did not complete names
  786  			// its files and no size, rather than claim as BACKED UP bytes
  787  			// that were not.
  788  			std::string summary;
  789  			const bool sized = o.completed && job.mRunBytes > 0;
  790  			if (job.mRunSized && (job.mRunFiles > 0 || sized))
  791  			{
  792  				if (job.mRunFiles > 0)
  793  					summary = std::to_string(job.mRunFiles) + " " + std::string(job.mRunFiles == 1 ? _("FILE") : _("FILES"));
  794  				if (sized)
  795  					summary += (summary.empty() ? "" : " · ") + sizeLabel((unsigned long) job.mRunBytes);
  796  				summary += " " + std::string(restore ? _("RESTORED") : _("BACKED UP"));
  797  			}
  798  			else if (job.mRunSized && o.completed)
  799  			{
  800  				// Nothing moved and the run succeeded: everything was there
  801  				// already. On a failure the same zero means something else,
  802  				// so the sentence is not offered. The clause after the dash
  803  				// is dropped whole on a panel too narrow for it, rather than
  804  				// ending in an ellipsis -- measured in the font it is set in.
  805  				summary = restore ? _("NOTHING NEW - YOU ALREADY HAD IT ALL")
  806  				                  : _("NOTHING NEW - YOUR CLOUD ALREADY HAD IT ALL");
  807  				if (mTextFont && mTextFont->sizeText(summary).x() > mLineWidth)
  808  					summary = restore ? _("NOTHING NEW TO BRING DOWN") : _("NOTHING NEW TO SEND UP");
  809  			}
  810  			mActivity->setText(fitOneLine(mTextFont, summary, mLineWidth));
  811  			mDetail  ->setText("");
  812  		}
  813  		if (!o.completed && !o.skipped)
  814  		{
  815  			// 4. The items that did not finish, and why: "NES, SETTINGS - YOUR
  816  			// CLOUD STOPPED ANSWERING". Items sharing a why share the line's
  817  			// one dash; a second why gets its own group. A why with no item
  818  			// (the scripts spoke before any unit, and no tier line followed)
  819  			// stands alone. Not on a skip: line 1 has said the one thing
  820  			// there is to say about every part, and a list of them under it
  821  			// would read as a list of failures.
  822  			std::vector<std::pair<std::string, std::vector<std::string>>> groups;
  823  			for (auto& f : job.mFailed)
  824  			{
  825  				auto g = groups.begin();
  826  				for (; g != groups.end(); ++g)
  827  					if (g->first == f.why)
  828  						break;
  829  				if (g == groups.end())
  830  					g = groups.insert(groups.end(), std::make_pair(f.why, std::vector<std::string>()));
  831  				const std::string name = unitName(f.label);
  832  				if (!name.empty() && std::find(g->second.begin(), g->second.end(), name) == g->second.end())
  833  					g->second.push_back(name);
  834  			}
  835  			std::string detail;
  836  			for (auto& g : groups)
  837  			{
  838  				std::string names;
  839  				for (size_t i = 0; i < g.second.size(); i++)
  840  					names += (i ? ", " : "") + g.second[i];
  841  				// In the interface's language: a script says its why in
  842  				// English (">>> why"), the code's phrase is translated
  843  				// already, and localizedWhy passes one it does not list as it
  844  				// came (#308 F-CS-31).
  845  				detail += (detail.empty() ? "" : "  ·  ") + names + (names.empty() ? "" : " - ") + CloudText::localizedWhy(g.first);
  846  			}
  847  			// A folder scan already names its subject in the page title.
  848  			// Drop that redundant label before clipping the failure reason
  849  			// on a small panel. Transfer lists still keep every failed unit.
  850  			if (CloudText::transferKind(job.mCommand) == CloudText::TransferKind::Scan
  851  				&& groups.size() == 1 && groups.front().second.size() == 1
  852  				&& groups.front().second.front() == unitName("CLOUD FOLDER")
  853  				&& mSmallFont && mSmallFont->sizeText(detail).x() > mLineWidth)
  854  				detail = CloudText::localizedWhy(groups.front().first);
  855  			mDetail->setText(fitOneLine(mSmallFont, detail, mLineWidth));
  856  		}
  857  
  858  		// 5. What is in place -- one clause per verb, true because rclone
  859  		// renames each file into place when it is complete and the content
  860  		// scripts delete nothing outside a match (D-CLOUD-077) -- when the
  861  		// run did not complete. When it did, the one thing left to do: a
  862  		// content run that changed the ROMs on this device is not visible in
  863  		// the game lists until they are rebuilt, and nobody should have to
  864  		// know that (maintainer, 2026-09-07).
  865  		const bool contentRun = job.mCommand.find("cloud_content_restore") != std::string::npos;
  866  		std::string note;
  867  		if (!o.completed)
  868  		{
  869  			// Files, not bytes: rclone renames a file into place only once it
  870  			// is whole and a cut S3 PUT lands nothing, so a run that moved nine
  871  			// megabytes of one archive has put nothing anywhere (#153).
  872  			// mUnitFiles is the last unit's count where foldUnit has not run.
  873  			const bool moved = job.mRunFiles > 0 || job.mUnitFiles > 0;
  874  			// A match: what it removed, counted from what rclone deleted
  875  			// (#308 gpt F-CS-26), and nothing about the cloud having it --
  876  			// a match removes only what the cloud does not have.
  877  			if (CloudText::transferKind(job.mCommand) == CloudText::TransferKind::Scan)
  878  				note = _("NO FILES HAVE BEEN MOVED. YOU CAN CHECK AGAIN LATER.");
  879  			else if (CloudText::transferKind(job.mCommand) == CloudText::TransferKind::Create)
  880  				note = _("FOLDERS ALREADY CREATED WILL STAY. YOU CAN TRY AGAIN LATER.");
  881  			else if (match)
  882  				note = CloudText::matchRemovedNote(job.mRemovedFiles);
  883  			else if (restore)
  884  				note = moved ? _("WHAT MADE IT IS ON THIS DEVICE. NOTHING ELSE CHANGED.") : _("DON'T WORRY, NOTHING CHANGED.");
  885  			else
  886  				note = moved ? _("WHAT MADE IT IS IN YOUR CLOUD. THE REST IS STILL HERE.") : _("DON'T WORRY, NOTHING CHANGED.");
  887  		}
  888  		else if (contentRun && (job.mRemovedFiles > 0 || job.mAnyTransferred))
  889  			note = _("UPDATE GAMELISTS UNDER GAME SETTINGS TO SEE THE CHANGE.");
  890  		// A completed run whose only exit is an action says what that
  891  		// action does here, where a run that finished cleanly otherwise has
  892  		// nothing to put (setCompletedAction).
  893  		if (o.completed && mCompletedAction && !mCompletedNote.empty())
  894  			note = mCompletedNote;
  895  		if (!o.completed && !o.skipped && !mFailedNote.empty())
  896  			note = mFailedNote;
  897  		// Two sentences on a 640px panel do not fit the small font; the
  898  		// first alone says what is in place, so it is what survives.
  899  		mNote->setText(fitSentences(mSmallFont, note, mLineWidth));
  900  
  901  		mElapsed ->setText(std::string(_("ELAPSED")) + " " + elapsed);
  902  		// 7. The retry lives on the surface that reported the failure: OK
  903  		// runs the same command again (input), back closes, and the help bar
  904  		// -- drawn by this page (render) -- carries the two on the player's
  905  		// own buttons, which may be swapped; the line named them A and B
  906  		// (#308 5-cloud claude F-CS-07, gpt F-CS-36). A run that completed
  907  		// has nothing to retry.
  908  		//
  909  		// Not for a match: its apply spends the preview's plan (PL-001), so
  910  		// the same command again is refused with SOMETHING CHANGED SINCE YOU
  911  		// CHECKED. Line 7 names the row that checks again instead, as the
  912  		// card names its row (#308 gpt F-CS-26).
  913  		mFooter  ->setText(!o.completed ? (match ? CloudText::matchRecovery() : std::string())
  914  			: mCompletedAction && !mCompletedFooter.empty() ? mCompletedFooter
  915  			: _("PRESS ANY BUTTON TO CLOSE"));
  916  	}
  917  	else
  918  	{
  919  		// 1 and 2: the item, and which of how many. The item is the row that
  920  		// changes when the run moves on, so it leads; the file in flight used
  921  		// to, and the page read bottom-up -- a file, its percentage, and only
  922  		// then what they belonged to (maintainer, 2026-09-09, D-UI-026). The
  923  		// count is the whole run's (handleLine), so settings, saves and two
  924  		// systems read ITEM 1 OF 4 through ITEM 4 OF 4 whichever script is
  925  		// speaking. Never an OF with nothing on either side: while the count
  926  		// is unknown the row reads ITEM i alone.
  927  		if (job.mItemIndex == 0)
  928  		{
  929  			mStatus ->setText(_("PREPARING..."));
  930  			mCounter->setText("");
  931  		}
  932  		else
  933  		{
  934  			const std::string item = unitName(job.mUnitLabel);
  935  			mStatus->setText(item.empty() ? _("WORKING...") : fitOneLine(mTextFont, item, mLineWidth));
  936  			std::string counter = std::string(_("ITEM")) + " " + std::to_string(job.mItemIndex);
  937  			if (job.mItemCount > 0)
  938  				counter += " " + std::string(_("OF")) + " " + std::to_string(job.mItemCount);
  939  			mCounter->setText(counter);
  940  		}
  941  
  942  		// 3: what it is doing on this item -- the line that says it is alive.
  943  		// A thousand small BIOS files spend minutes between percentage
  944  		// changes, and a frozen percentage is indistinguishable from a hang.
  945  		std::string doing;
  946  		if (!job.mCurrent.empty())
  947  		{
  948  			// "TRANSFERRING name.zip . 45% OF 2.5 MB . 300 KB/S . AND 3 MORE
  949  			// FILES": a single space inside a segment and " . " between them,
  950  			// the same as every other row (#85). The name is the part that
  951  			// has to show; the rest is shed a segment at a time, least useful
  952  			// first, until the line fits this font: the AND N MORE count goes
  953  			// before the file's own progress, and last the name alone is
  954  			// clipped -- half a percentage after an ellipsis says nothing,
  955  			// and line 4 carries the item's percentage regardless.
  956  			const std::string head     = std::string(_("TRANSFERRING")) + " " + job.mCurrent;
  957  			const std::string progress = job.mFileProgress.empty() ? "" : " · " + prettyRclone(job.mFileProgress);
  958  			const std::string more     = job.mFilesThisBlock > 1
  959  				? " · " + std::string(_("AND")) + " " + std::to_string(job.mFilesThisBlock - 1) + " " + std::string(_("MORE FILES")) : "";
  960  			const auto fits = [this](const std::string& t) { return mTextFont && mTextFont->sizeText(t).x() <= mLineWidth; };
  961  			if (fits(head + progress + more))
  962  				doing = head + progress + more;
  963  			else if (fits(head + progress))
  964  				doing = head + progress;
  965  			else
  966  				doing = fitOneLine(mTextFont, head, mLineWidth);   // unchanged when it fits, clipped when it does not
  967  		}
  968  		else if (job.mChecksTotal > 0 || job.mListed > 0)
  969  		{
  970  			// Nothing in flight, plenty happening: rclone is comparing what
  971  			// is here with what is there, and for a device whose saves are
  972  			// all in the cloud already that is the whole run. It prints no
  973  			// per-file line for a comparison, so this is the count it does
  974  			// print -- and the name, when it caught one mid-comparison and
  975  			// there is room beside the count. A run that showed neither
  976  			// looked hung until it said COMPLETED (maintainer, 2026-09-08).
  977  			// Before anything is queued to compare the only count is what
  978  			// rclone has listed, and that counts both sides -- 40 saves list
  979  			// as 80 -- so it is not shown as a number the player would try
  980  			// to reconcile with their files; the spinner on row 5 is the sign
  981  			// of life until the first check is queued. The word is the card's
  982  			// (COMPARING SAVES, D-UI-075): one compare, one name, on both
  983  			// surfaces (#157).
  984  			if (job.mChecksTotal > 0)
  985  				doing = std::string(_("COMPARING")) + " " + std::to_string(job.mChecksDone) + " " + std::string(_("OF")) + " "
  986  					+ std::to_string(job.mChecksTotal) + " " + std::string(_("FILES"));
  987  			else
  988  				doing = _("COMPARING FILES...");
  989  			// the name is the line's one optional segment, and the first to go
  990  			if (!job.mChecking.empty())
  991  			{
  992  				const std::string named = doing + " · " + job.mChecking;
  993  				if (mTextFont && mTextFont->sizeText(named).x() <= mLineWidth)
  994  					doing = named;
  995  			}
  996  		}
  997  		else if (job.mDoing == "archive")
  998  		{
  999  			// backuptool is writing the settings archive and prints nothing
 1000  			// this page can use, so ES announces it (">>> doing archive") and
 1001  			// the settings item says what it is doing like every other item,
 1002  			// rather than sitting on a spinner (maintainer, 2026-09-09).
 1003  			doing = _("PACKING UP YOUR SETTINGS...");
 1004  		}
 1005  		else if (job.mDoing == "unpack")
 1006  		{
 1007  			// The same item on the way back: backuptool is extracting the
 1008  			// archive over the live configuration, and says nothing this
 1009  			// page can use either (">>> doing unpack", #114).
 1010  			doing = _("PUTTING YOUR SETTINGS BACK...");
 1011  		}
 1012  		// The scan page's one line (the approved string, D-CLOUD-164) and
 1013  		// the content scan's; the folder move's three steps (#353). Each
 1014  		// is cut to the line as every row 3 is.
 1015  		else if (job.mDoing == "scan")
 1016  		{
 1017  			// The approved sentence where it fits; at 640 px it was cut
 1018  			// mid-word (guest d, 2026-10-01), so the clause goes whole
 1019  			// (D-UI-035) before the line is clipped at all.
 1020  			doing = CloudText::chooseThatFits({ _("CHECKING WHAT SETTINGS AND CONTENT YOUR CLOUD HAS FOR THIS DEVICE..."),
 1021  				_("CHECKING WHAT YOUR CLOUD HAS FOR THIS DEVICE...") }, mLineWidth,
 1022  				[this](const std::string& t) { return mTextFont ? mTextFont->sizeText(t).x() : 0.0f; });
 1023  			doing = fitOneLine(mTextFont, doing, mLineWidth);
 1024  		}
 1025  		else if (job.mDoing == "compare")
 1026  			doing = _("COMPARING WITH THIS DEVICE...");
 1027  		else if (job.mDoing == "copy")
 1028  			doing = _("COPYING...");
 1029  		else if (job.mDoing == "verify")
 1030  			doing = _("CHECKING THE COPY...");
 1031  		else if (job.mDoing == "remove")
 1032  			doing = _("REMOVING THE OLD FOLDER...");
 1033  		else if (job.mItemIndex > 0)
 1034  			doing = _("WORKING...");
 1035  		mActivity->setText(doing);
 1036  
 1037  		// 4: this item's totals -- the count line and the byte line of the
 1038  		// last stats block. "12 / 45, 27%" -> "12 OF 45 FILES . 27%".
 1039  		std::string totals;
 1040  		if (!job.mFilesTotals.empty())
 1041  		{
 1042  			auto pct = job.mFilesTotals.find(", ");
 1043  			totals = Utils::String::replace(job.mFilesTotals.substr(0, pct), " / ", " " + std::string(_("OF")) + " ") + " " + std::string(_("FILES"));
 1044  			if (pct != std::string::npos)
 1045  				totals += " · " + job.mFilesTotals.substr(pct + 2);
 1046  		}
 1047  		// "0 B / 0 B, -, 0 B/s, ETA -" is the byte line while nothing is queued
 1048  		// to move -- the whole of a run that only compares -- and it is true of
 1049  		// nothing anybody asked about. Line 3 says what such a run is doing;
 1050  		// this line stays blank rather than read "0 B OF 0 B . 0 B/S".
 1051  		if (!job.mTotals.empty() && job.mTotals.rfind("0 B / 0 B", 0) != 0)
 1052  			totals += (totals.empty() ? "" : "   ") + prettyRclone(job.mTotals);
 1053  		mDetail->setText(fitOneLine(mSmallFont, totals, mLineWidth));
 1054  
 1055  		mElapsed->setText(std::string(_("ELAPSED")) + " " + elapsed);
 1056  		// 7. That it takes a while. How to cancel, where the page can be, is
 1057  		// the help bar's, on the player's own back button: the line said
 1058  		// PRESS B TO CANCEL, the wrong button on a swapped mapping (#308
 1059  		// 5-cloud claude F-CS-07, gpt F-CS-36).
 1060  		mFooter->setText(fitOneLine(mSmallFont, _("THIS CAN TAKE A WHILE."), mLineWidth));
 1061  	}
 1062  	lock.unlock();
 1063  	if (justFinished)
 1064  		updateHelpPrompts();
 1065  	if (advance)
 1066  	{
 1067  		mAdvancePosted = true;
 1068  		std::weak_ptr<bool> alive = mAlive;
 1069  		GuiCloudTransfer* page = this;
 1070  		mWindow->postToUiThread([page, alive]
 1071  		{
 1072  			if (auto token = alive.lock())
 1073  				if (*token)
 1074  					page->advance();
 1075  		});
 1076  	}
 1077  }
```


## es-app/src/CloudText.h @ 16dbac5211: lines 1-38 (excerpt of 589)

```text
    1  #pragma once
    2  #ifndef ES_APP_CLOUD_TEXT_H
    3  #define ES_APP_CLOUD_TEXT_H
    4  
    5  // The cloud surfaces' pure text: what a stamp line says, what a script's
    6  // protocol line means, which words a provider is known by, and how a
    7  // composed line is shortened when the panel is too narrow for all of it.
    8  //
    9  // Nothing here reads a file, asks Settings or SystemConf anything, touches
   10  // a Window, or measures a font, so all of it can be checked by a test
   11  // binary that links no more of EmulationStation than this file and
   12  // StringUtil (es-app/tests/unit). The callers keep the parts that cannot
   13  // be: the file read, the translation of an outcome into the player's
   14  // language, and the side effects a protocol line asks for.
   15  //
   16  // Translation stays outside on purpose. _() at this level would put the
   17  // player's language inside the thing under test, so the enums below name
   18  // an outcome and the caller says it in words.
   19  
   20  #include <ctime>
   21  #include <functional>
   22  #include <map>
   23  #include <string>
   24  #include <utility>
   25  #include <vector>
   26  
   27  namespace CloudText
   28  {
   29  	// The providers we put in front of people, most-likely-to-be-owned
   30  	// first: rclone's word for each service, and the words the player
   31  	// chose it by. One table, read from both sides -- the wizard's
   32  	// recommendation list and providerLabel below.
   33  	//
   34  	// This was split into two groups by how the sign-in works -- one you
   35  	// approve through a provider page, one you type a key into. That is our
   36  	// distinction, not the player's: they are choosing where their saves
   37  	// live, and the group headers made an implementation detail look like
   38  	// the question being asked. It also read as a hierarchy it is not,
```


## es-app/src/CloudText.h @ 16dbac5211: lines 70-118 (excerpt of 589)

```text
   70  
   71  	// The device name as the network takes it: ASCII letters and digits,
   72  	// any run of anything else as one hyphen, none at either end, at most
   73  	// 63. The same rule as the scripts' clean_hostname (001-functions),
   74  	// which network-base-setup applies at boot. The player's own name is
   75  	// left exactly as they typed it -- this is only what the network shows.
   76  	std::string cleanHostname(const std::string& in);
   77  
   78  	// How a run ended, in the four words every cloud surface uses
   79  	// (D-UI-028). Gaps and Failed both read COULDN'T FINISH to the player
   80  	// and differ only in where their why comes from: a composed run whose
   81  	// parts disagreed has the failing part's, and nothing to fall back on
   82  	// from an exit code that describes the whole run.
   83  	enum class Outcome
   84  	{
   85  		Completed,
   86  		Gaps,
   87  		SkippedLockHeld,
   88  		SkippedNoNetwork,
   89  		SkippedGameStarted,
   90  		SkippedCancelled,     // the player's CANCEL on the transfer page (D-UI-078)
   91  		SkippedNoFolder,      // an automatic sync with no saves folder in the cloud yet (CloudExit::NoFolder)
   92  		Failed
   93  	};
   94  
   95  	// What a stamp line says. The file read and the fallback whys stay with
   96  	// the caller; ran is false for anything this cannot make sense of, and
   97  	// a row then reads NOT DONE ON THIS DEVICE YET rather than inventing a
   98  	// date.
   99  	struct LastRun
  100  	{
  101  		bool ran = false;
  102  		time_t when = 0;
  103  		int code = 0;
  104  		std::string token;
  105  		std::string why;      // upper case, no trailing period; empty when there was none
  106  		Outcome outcome = Outcome::Completed;
  107  		bool finished = false;
  108  		bool knownToken = false;  // one of ThreadedCloudSync's tokens, not a scripts' why
  109  	};
  110  
  111  	// Whether a stamp's third field is one of the tokens EmulationStation
  112  	// writes (rather than the scripts' own sentence, underscored).
  113  	bool isOutcomeToken(const std::string& token);
  114  
  115  	// "<epoch> <rc>[ <token>[ <why...>]]" (D-UI-028), the whole file's text.
  116  	LastRun parseLastRun(const std::string& text);
  117  
  118  	// Whether the exit sync that was skipped for want of a network is still
```


## es-app/src/CloudText.h @ 16dbac5211: lines 152-228 (excerpt of 589)

```text
  152  	// that carries 69 and the gaps token, in English as the scripts wrote
  153  	// it; "" when none does -- a bare 69, where nothing moved.
  154  	std::string offlinePartWayWhy(const std::vector<StampText>& stamps, const std::vector<StampText>& before);
  155  
  156  	// Which run a stamp describes. EmulationStation stamps last-sync-exit
  157  	// and last-sync-startup as each automatic run ends, within a second or
  158  	// two of the script writing its own last-backup or last-restore, so a
  159  	// matching time says which it was. Pass 0 for a stamp that does not
  160  	// exist; the exit stamp wins a tie.
  161  	enum class RunOrigin { None, AfterLastGame, AtStartup };
  162  	RunOrigin runOrigin(time_t when, time_t exitWhen, time_t startupWhen);
  163  
  164  	// A shorter form of a why sentence, for a panel the whole one does not
  165  	// fit on (#115). Two shapes appear in the sentences the scripts emit,
  166  	// and both put the part that can go at the end: a trailing clause after
  167  	// a dash (COULDN'T REACH YOUR CLOUD - CHECK YOUR SIGN-IN) and a
  168  	// trailing sentence after a full stop. Anything else has no short form
  169  	// and comes back empty; the caller falls back to the outcome word on
  170  	// its own, which fits any panel and is still true.
  171  	std::string shortenWhy(const std::string& why);
  172  
  173  	// The forms of an outcome line, longest first (D-UI-035): the whole
  174  	// thing, then the why with its trailing clause dropped, then the
  175  	// outcome word alone. A line with no " - " has no split to make and
  176  	// gets the single candidate it has today.
  177  	std::vector<std::string> outcomeCandidates(const std::string& outcome);
  178  
  179  	// The sentences the cloud scripts print as ">>> why <SENTENCE>" -- and
  180  	// the rc-keyed ones their why_for prints -- each paired with its
  181  	// translation in the interface's language (#308 F-CS-31). The scripts
  182  	// speak English whatever the language; the card put their sentence
  183  	// beside a translated outcome word. localizedWhy returns the pair's
  184  	// translation, or the sentence as it came for one this build does not
  185  	// list (a script newer than the interface): never worse than before.
  186  	// The stamps keep the English: their readers translate.
  187  	std::vector<std::pair<std::string, std::string>> whySentences();
  188  	std::string localizedWhy(const std::string& why);
  189  	bool isKnownWhy(const std::string& why);
  190  
  191  	// One line of a cloud script's output as the card reads it: ANSI escape
  192  	// sequences and C0 controls and DEL dropped, every other byte kept --
  193  	// UTF-8 included, since a folder name in the player's language arrives
  194  	// in a ">>> offer" line and must reach the offer whole -- then trimmed.
  195  	std::string cleanLine(const std::string& raw);
  196  
  197  	// The sync card's action line when a run did not complete (D-CLOUD-077),
  198  	// longest first: what is in place and how to recover, then the recovery
  199  	// alone. `recoveries` are the recovery sentence's own forms, longest
  200  	// first. The in-place clause is the part that goes first when the line
  201  	// is short of room (es-player-text.md) -- unless keepInPlace, when every
  202  	// candidate carries it and the in-place clause alone is the last.
  203  	std::vector<std::string> actionCandidates(const std::string& inPlace,
  204  		const std::vector<std::string>& recoveries, bool keepInPlace);
  205  
  206  	// The ">>> " lines are the scripts talking to the interface, not to the
  207  	// player. Classification only: what the line is and what it carries.
  208  	// Acting on it -- the pid to signal, the card's waiting text, the why
  209  	// to keep, the offer to put to the player, the tier to record -- stays
  210  	// with the caller.
  211  	//
  212  	// Every shape any script emits is named here, whether or not the reader
  213  	// asking about it acts on one: the transfer page read ">>> unit" and
  214  	// ">>> removed" with a parser of its own and never knew about
  215  	// ">>> offer", so the empty-cloud question reached one of the two
  216  	// surfaces that run cloud_restore and not the other (#145). One parser,
  217  	// two readers, and Unknown means a marker newer than this build --
  218  	// never a marker this build simply forgot.
  219  	enum class ProtocolKind { NotProtocol, Pid, Doing, Why, Offer, Tier, Unit, Removed, Unknown };
  220  
  221  	// removed: one per system, out of the third field of
  222  	// ">>> removed 14|314572800|snes:12:300000000,gb:2:14572800". files is
  223  	// the count as the script spelt it, because the caller prints it and
  224  	// picks FILE or FILES by it; an item with fewer than two fields is not
  225  	// one and is dropped.
  226  	struct RemovedSystem
  227  	{
  228  		std::string system;   // upper case
```


## es-app/src/CloudText.h @ 16dbac5211: lines 519-535 (excerpt of 589)

```text
  519  	// (#308 5-cloud-sync-and-saves gpt F-CS-26, the page's half): what it
  520  	// removed, and the way on.
  521  	std::string matchRemovedNote(int removedFiles);
  522  	std::string matchRecovery();
  523  
  524  	// The names the transfer page gives its items, from the ">>> unit" and
  525  	// ">>> tier" labels: the ones EmulationStation composes (the transfer
  526  	// form's parts, the journey's continuation, the startup sync) paired,
  527  	// English and _(""), as whySentences pairs the scripts' whys; a label
  528  	// not listed -- a system's folder -- is shown upper-cased, as it came.
  529  	std::vector<std::pair<std::string, std::string>> unitLabels();
  530  	std::string unitLabel(const std::string& label);
  531  	bool isKnownUnitLabel(const std::string& label);
  532  
  533  	// Recognize only fixed cloud_setup explanations, never provider details or
  534  	// player paths. The worker carries an enum; the UI supplies localized copy.
  535  	enum class FolderPathRefusal
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 142-243 (excerpt of 1409)

```text
  142  	{
  143  		out.resize(63);
  144  		while (!out.empty() && out.back() == '-')
  145  			out.pop_back();
  146  	}
  147  	return out;
  148  }
  149  
  150  bool isOutcomeToken(const std::string& token)
  151  {
  152  	static const std::set<std::string> ourTokens = {
  153  		"completed", "gaps", "no-network", "lock-held", "cancelled", "player-cancelled", "stopped",
  154  		"folder-missing", "cloud-stopped", "cloud-refused", "unknown", "no-folder" };
  155  	return ourTokens.find(token) != ourTokens.cend();
  156  }
  157  
  158  // A field that is a whole number and nothing else -- an optional minus,
  159  // then digits -- within [lo, hi]. atoi read "garbage" as 0, and 0 is
  160  // success; a status that cannot be read is not one (#308 F-CS-27).
  161  static bool wholeNumber(const std::string& field, long long lo, long long hi, long long& out)
  162  {
  163  	const std::string f = Utils::String::trim(field);
  164  	size_t i = (!f.empty() && f[0] == '-') ? 1 : 0;
  165  	if (i >= f.size() || f.size() - i > 12)
  166  		return false;
  167  	for (size_t j = i; j < f.size(); j++)
  168  		if (f[j] < '0' || f[j] > '9')
  169  			return false;
  170  	const long long value = atoll(f.c_str());
  171  	if (value < lo || value > hi)
  172  		return false;
  173  	out = value;
  174  	return true;
  175  }
  176  
  177  // Every stamp each script can write, whichever flags it ran with: a
  178  // composed command runs cloud_backup twice (saves, then --system-only
  179  // settings), so which stamp a part wrote is the stamp's to say, not the
  180  // command line's. The table used to map cloud_backup to last-backup alone,
  181  // and a stopped settings part left its trap's 130 under the settings row.
  182  std::vector<std::string> scriptStampNames(const std::string& command)
  183  {
  184  	struct Part { const char* script; std::vector<const char*> stamps; };
  185  	static const std::vector<Part> PARTS = {
  186  		{ "cloud_content_backup",  { "last-content-backup" } },
  187  		{ "cloud_content_restore", { "last-content-restore", "last-content-match" } },
  188  		{ "cloud_restore",         { "last-restore", "last-settings-restore" } },
  189  		{ "cloud_backup",          { "last-backup", "last-settings-backup" } },
  190  	};
  191  	std::vector<std::string> names;
  192  	for (const Part& part : PARTS)
  193  		if (command.find(part.script) != std::string::npos)
  194  			for (const char* stamp : part.stamps)
  195  				names.push_back(stamp);
  196  	return names;
  197  }
  198  
  199  // The part the stop interrupted, and nothing else: a stamp this run wrote
  200  // with the trap's code. A part that finished before the stop keeps its
  201  // outcome, one that failed on its own keeps its why -- the table and a
  202  // time test used to restamp every stamp the run had written, so a saves
  203  // part that completed read as stopped once the settings part after it
  204  // was. A part that never started keeps its last real run's stamp.
  205  std::vector<std::string> stampsToRestamp(const std::vector<StampText>& stamps, time_t runStarted,
  206  	const std::vector<StampText>* before)
  207  {
  208  	std::vector<std::string> names;
  209  	for (auto& s : stamps)
  210  	{
  211  		const LastRun r = parseLastRun(s.text);
  212  		// The trap's stop: 130, and none of this interface's tokens -- a
  213  		// stamp that carries one was restamped after an earlier stop, and is
  214  		// that run's (audit of the fixes G-E1-06: by the time alone, one
  215  		// written in the second this run began qualified).
  216  		if (!r.ran || r.code != CloudExit::Stopped || r.knownToken)
  217  			continue;
  218  		if (before != nullptr)
  219  		{
  220  			// Written since the run began: the file is not the one read then
  221  			// (the scripts write a new file and rename it), whatever the
  222  			// clock -- a device booting with its clock behind made
  223  			// yesterday's stop look like today's (G-E1-04, the claude seat).
  224  			std::string was;
  225  			for (auto& b : *before)
  226  				if (b.name == s.name)
  227  					was = b.version;
  228  			if (!s.version.empty() && s.version != was)
  229  				names.push_back(s.name);
  230  		}
  231  		else if (r.when >= runStarted)
  232  			names.push_back(s.name);
  233  	}
  234  	return names;
  235  }
  236  
  237  std::string offlinePartWayWhy(const std::vector<StampText>& stamps, const std::vector<StampText>& before)
  238  {
  239  	for (auto& s : stamps)
  240  	{
  241  		const LastRun r = parseLastRun(s.text);
  242  		if (!r.ran || r.code != CloudExit::NoNetwork || r.token != "gaps")
  243  			continue;
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 290-306 (excerpt of 1409)

```text
  290  	r.when = when;
  291  	// "<epoch> <rc>[ <token>[ <why...>]]" (D-UI-028). The first two fields
  292  	// are what every stamp has always carried; the token is one word for
  293  	// the outcome where the code alone cannot say it (a 130 that was a
  294  	// launch cancel; a composed run whose parts disagreed), and the why
  295  	// is the scripts' own sentence when they printed one. A stamp with two
  296  	// fields -- one written before this reader -- is read from its code.
  297  	//
  298  	// The four words, with commas rather than dashes inside the outcome:
  299  	// the line already uses a dash to separate the date from it. LockHeld
  300  	// and NoNetwork are the scripts' "another sync holds the lock" and "no
  301  	// network" (CloudExit.h): the scripts write no stamp for those (nothing
  302  	// ran), but the whole-run stamps EmulationStation keeps per cause
  303  	// (last-sync-startup, -exit, -manual; fork #94) do, because under SYNC
  304  	// SAVES DURING STARTUP the player's question is what happened this
  305  	// morning, and "nothing, there was no network" answers it.
  306  	const int code = (int) status;
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 397-493 (excerpt of 1409)

```text
  397  		const std::string tail = outcome.substr(dash + 3);
  398  		const std::string shortTail = shortenWhy(tail);
  399  		if (!shortTail.empty() && shortTail != tail)
  400  			candidates.push_back(head + std::string(" - ") + shortTail);
  401  		candidates.push_back(head);
  402  	}
  403  
  404  	return candidates;
  405  }
  406  
  407  std::string lockHeldOutcome(TransferKind kind)
  408  {
  409  	return kind == TransferKind::Scan
  410  		? _("SKIPPED - ANOTHER CLOUD CHECK IS RUNNING")
  411  		: _("SKIPPED - A SYNC IS ALREADY RUNNING");
  412  }
  413  
  414  std::vector<std::pair<std::string, std::string>> whySentences()
  415  {
  416  	// Each sentence twice: as the script prints it, to match, and inside
  417  	// _(""), so xgettext carries it into the catalog and the French in
  418  	// locale/lang/fr reaches the card. Built on each call, after the
  419  	// language is chosen. The list is the emitter table in
  420  	// es-app/tests/unit/CloudTextTests.cpp, which fails on a why a script
  421  	// prints that is not here; a sentence a script changes wants its pair
  422  	// changed in the same change, or the card shows it in English again.
  423  	return {
  424  		{ "YOUR CLOUD STORAGE ISN'T SET UP YET", _("YOUR CLOUD STORAGE ISN'T SET UP YET") },
  425  		{ "CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.", _("CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.") },
  426  		{ "COULDN'T REACH YOUR CLOUD - CHECK YOUR SIGN-IN", _("COULDN'T REACH YOUR CLOUD - CHECK YOUR SIGN-IN") },
  427  		{ "YOUR CLOUD STOPPED ANSWERING", _("YOUR CLOUD STOPPED ANSWERING") },
  428  		{ "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ", _("YOUR CLOUD SYNC SETTINGS COULDN'T BE READ") },
  429  		{ "YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED", _("YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED") },
  430  		{ "YOUR CLOUD FOLDER COULDN'T BE READ", _("YOUR CLOUD FOLDER COULDN'T BE READ") },
  431  		{ "YOUR CLOUD SETTINGS CHANGED. CHECK AGAIN", _("YOUR CLOUD SETTINGS CHANGED. CHECK AGAIN") },
  432  		{ "ANOTHER CLOUD CHECK IS RUNNING", _("ANOTHER CLOUD CHECK IS RUNNING") },
  433  		{ "YOUR CLOUD FOLDERS COULDN'T BE CREATED", _("YOUR CLOUD FOLDERS COULDN'T BE CREATED") },
  434  		{ "CHECK WHAT WOULD CHANGE FIRST", _("CHECK WHAT WOULD CHANGE FIRST") },
  435  		{ "AN OLD FOLDER SETTING IS IN THE WAY", _("AN OLD FOLDER SETTING IS IN THE WAY") },
  436  		{ "YOUR SAVES FOLDER ISN'T ON THIS DEVICE", _("YOUR SAVES FOLDER ISN'T ON THIS DEVICE") },
  437  		{ "THIS DEVICE'S SETTINGS BACKUP IS DAMAGED", _("THIS DEVICE'S SETTINGS BACKUP IS DAMAGED") },
  438  		{ "THE COPY IN YOUR CLOUD ISN'T COMPLETE", _("THE COPY IN YOUR CLOUD ISN'T COMPLETE") },
  439  		{ "COULDN'T FIND YOUR CLOUD FOLDER", _("COULDN'T FIND YOUR CLOUD FOLDER") },
  440  		{ "SOME FILES DIDN'T FINISH", _("SOME FILES DIDN'T FINISH") },
  441  		{ "YOUR CLOUD WOULDN'T TAKE THE FILES", _("YOUR CLOUD WOULDN'T TAKE THE FILES") },
  442  		{ "IT WAS STOPPED", _("IT WAS STOPPED") },
  443  		{ "THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME", _("THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME") },
  444  		{ "SOMETHING WENT WRONG", _("SOMETHING WENT WRONG") },
  445  		{ "COULDN'T TELL WHICH CARD YOUR SAVES ARE ON", _("COULDN'T TELL WHICH CARD YOUR SAVES ARE ON") },
  446  		{ "YOUR SAVES ARE ON A DIFFERENT CARD", _("YOUR SAVES ARE ON A DIFFERENT CARD") },
  447  		{ "YOUR SAVES CHANGED CARDS PART-WAY THROUGH", _("YOUR SAVES CHANGED CARDS PART-WAY THROUGH") },
  448  		{ "THERE'S NO SETTINGS BACKUP ON THIS DEVICE YET", _("THERE'S NO SETTINGS BACKUP ON THIS DEVICE YET") },
  449  		{ "COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS", _("COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS") },
  450  		{ "THE RESTORE COULDN'T FINISH", _("THE RESTORE COULDN'T FINISH") },
  451  		{ "THIS DEVICE CAN'T MAKE A SETTINGS BACKUP", _("THIS DEVICE CAN'T MAKE A SETTINGS BACKUP") },
  452  		{ "THE BACKUP COULDN'T FINISH WHILE GATHERING YOUR SETTINGS", _("THE BACKUP COULDN'T FINISH WHILE GATHERING YOUR SETTINGS") },
  453  		{ "THE BACKUP COULDN'T FINISH", _("THE BACKUP COULDN'T FINISH") },
  454  		// Added with the table at next 4476f90394 (#308 follow-up): stream
  455  		// A's match, card record and layout migration, the stamp's offline
  456  		// why (a 69 with the gaps token, read by the rows), and backuptool's
  457  		// five since f0f263b8cc.
  458  		{ "SOMETHING CHANGED SINCE YOU CHECKED", _("SOMETHING CHANGED SINCE YOU CHECKED") },
  459  		{ "COULDN'T RECORD WHICH CARD YOUR SAVES ARE ON", _("COULDN'T RECORD WHICH CARD YOUR SAVES ARE ON") },
  460  		{ "YOU WENT OFFLINE PART-WAY THROUGH", _("YOU WENT OFFLINE PART-WAY THROUGH") },
  461  		{ "THIS DEVICE CAN'T RESTORE SETTINGS", _("THIS DEVICE CAN'T RESTORE SETTINGS") },
  462  		{ "A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING", _("A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING") },
  463  		{ "THERE'S NOTHING TO BACK UP YET", _("THERE'S NOTHING TO BACK UP YET") },
  464  		{ "A SIGN-IN WAS FOUND IN THE BACKUP", _("A SIGN-IN WAS FOUND IN THE BACKUP") },
  465  		{ "YOUR OWN BACKUP LIST NAMES A FOLDER A BACKUP CAN'T CARRY", _("YOUR OWN BACKUP LIST NAMES A FOLDER A BACKUP CAN'T CARRY") },
  466  	};
  467  }
  468  
  469  std::string localizedWhy(const std::string& why)
  470  {
  471  	for (auto& sentence : whySentences())
  472  		if (sentence.first == why)
  473  			return sentence.second;
  474  	return why;
  475  }
  476  
  477  bool isKnownWhy(const std::string& why)
  478  {
  479  	for (auto& sentence : whySentences())
  480  		if (sentence.first == why)
  481  			return true;
  482  	return false;
  483  }
  484  
  485  std::string cleanLine(const std::string& raw)
  486  {
  487  	// The transfer page's rule (CloudTransferJob::cleanLine, #85), which the
  488  	// card did not share: it kept printable ASCII only, and a folder name in
  489  	// the player's language lost its accented letters on the way to the
  490  	// offer (#308 F-CS-19). A terminal escape is an instruction to a
  491  	// terminal that is not here, and goes whole -- and only itself, by its
  492  	// own grammar (ECMA-48), not "to the next letter", which swallowed the
  493  	// start of a protocol line after a window title or a two-byte escape
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 547-653 (excerpt of 1409)

```text
  547  	}
  548  	if (!inPlace.empty() && !recoveries.empty())
  549  		out.push_back(inPlace + " " + recoveries.front());
  550  	for (auto& r : recoveries)
  551  		out.push_back(r);
  552  	return out;
  553  }
  554  
  555  ProtocolLine classifyProtocolLine(const std::string& clean)
  556  {
  557  	ProtocolLine out;
  558  	if (clean.rfind(">>> ", 0) != 0)
  559  		return out;
  560  
  561  	if (clean.rfind(">>> pid ", 0) == 0)
  562  	{
  563  		out.kind = ProtocolKind::Pid;
  564  		out.number = atoi(clean.substr(8).c_str());
  565  	}
  566  	else if (clean.rfind(">>> doing ", 0) == 0)
  567  	{
  568  		out.kind = ProtocolKind::Doing;
  569  		out.text = Utils::String::trim(clean.substr(10));
  570  	}
  571  	else if (clean.rfind(">>> why ", 0) == 0)
  572  	{
  573  		out.kind = ProtocolKind::Why;
  574  		std::string why = Utils::String::toUpper(Utils::String::trim(clean.substr(8)));
  575  		// The outcome line supplies its own end; a sentence's
  576  		// full stop after a dash reads as a typo.
  577  		while (!why.empty() && why.back() == '.')
  578  			why.pop_back();
  579  		out.text = why;
  580  	}
  581  	else if (clean.rfind(">>> offer ", 0) == 0)
  582  	{
  583  		out.kind = ProtocolKind::Offer;
  584  		auto parts = Utils::String::split(clean.substr(10), '|', false);
  585  		out.text = parts.size() > 0 ? Utils::String::trim(parts[0]) : "";
  586  		for (size_t i = 1; i < parts.size(); i++)
  587  			out.args.push_back(Utils::String::trim(parts[i]));
  588  	}
  589  	else if (clean.rfind(">>> tier ", 0) == 0)
  590  	{
  591  		out.kind = ProtocolKind::Tier;
  592  		auto parts = Utils::String::split(clean.substr(9), '|', false);
  593  		out.text = parts.size() > 0 ? Utils::String::toUpper(Utils::String::trim(parts[0])) : "";
  594  		// The part's exit status, 0-255; anything else -- nothing, junk -- is
  595  		// -1, which is not a success and not one of rclone's (#308 F-CS-27).
  596  		long long code = -1;
  597  		out.number = (parts.size() > 1 && wholeNumber(parts[1], 0, 255, code)) ? (int) code : -1;
  598  	}
  599  	// ">>> unit nes|2|5" -- an item starts: a system, or a phase whose
  600  	// counts are empty ("SAVES||"). The label keeps the case it came in,
  601  	// because the reader that counts items compares one announcement with
  602  	// the next; the empty fields are zero, which is the reader's "the
  603  	// script did not say".
  604  	else if (clean.rfind(">>> unit ", 0) == 0)
  605  	{
  606  		out.kind = ProtocolKind::Unit;
  607  		auto parts = Utils::String::split(clean.substr(9), '|', false);
  608  		out.text   = parts.size() > 0 ? Utils::String::trim(parts[0]) : "";
  609  		out.number = parts.size() > 1 ? atoi(Utils::String::trim(parts[1]).c_str()) : 0;
  610  		out.count  = parts.size() > 2 ? atoi(Utils::String::trim(parts[2]).c_str()) : 0;
  611  	}
  612  	// ">>> removed 14|314572800|snes:12:300000000,gb:2:14572800" -- what a
  613  	// match took off this device, in total and per system. A match cut off
  614  	// by the network prints it before exiting, so what had already gone can
  615  	// still be said.
  616  	else if (clean.rfind(">>> removed ", 0) == 0)
  617  	{
  618  		out.kind = ProtocolKind::Removed;
  619  		auto parts = Utils::String::split(clean.substr(12), '|', false);
  620  		out.files = parts.size() > 0 ? atol(Utils::String::trim(parts[0]).c_str()) : 0;
  621  		out.bytes = parts.size() > 1 ? atol(Utils::String::trim(parts[1]).c_str()) : 0;
  622  		if (parts.size() > 2)
  623  		{
  624  			for (auto& item : Utils::String::split(Utils::String::trim(parts[2]), ',', true))
  625  			{
  626  				auto f = Utils::String::split(item, ':', false);
  627  				// A system and a count are what makes an item; anything
  628  				// shorter is a torn field, and a system named with no
  629  				// number beside it is worse than one not named at all.
  630  				if (f.size() < 2)
  631  					continue;
  632  				RemovedSystem sys;
  633  				sys.system = Utils::String::toUpper(Utils::String::trim(f[0]));
  634  				sys.files  = Utils::String::trim(f[1]);
  635  				sys.bytes  = f.size() > 2 ? atol(Utils::String::trim(f[2]).c_str()) : 0;
  636  				out.systems.push_back(sys);
  637  			}
  638  		}
  639  	}
  640  	else
  641  		out.kind = ProtocolKind::Unknown;
  642  
  643  	return out;
  644  }
  645  
  646  Verb verbOf(const std::string& cmd)
  647  {
  648  	const bool restore = cmd.find("cloud_restore") != std::string::npos;
  649  	const bool backup  = cmd.find("cloud_backup")  != std::string::npos || cmd.find("backuptool") != std::string::npos;
  650  	if (restore && backup) return Verb::Sync;
  651  	if (restore) return Verb::Restore;
  652  	if (backup)  return Verb::Backup;
  653  	return Verb::Other;
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 797-888 (excerpt of 1409)

```text
  797  		}
  798  		return !a.empty() && !b.empty();
  799  	}
  800  
  801  	bool allDigits(const std::string& s)
  802  	{
  803  		return !s.empty() && s.find_first_not_of("0123456789") == std::string::npos;
  804  	}
  805  }
  806  
  807  LiveLine liveLine(const std::string& clean)
  808  {
  809  	LiveLine out;
  810  	static const std::string XFER = "Transferred:";
  811  	static const std::string CHECKS = "Checks:";
  812  
  813  	const size_t xfer = clean.rfind(XFER);
  814  	const size_t checks = clean.rfind(CHECKS);
  815  
  816  	if (xfer != std::string::npos && (checks == std::string::npos || xfer > checks))
  817  	{
  818  		std::string body = Utils::String::trim(clean.substr(xfer + XFER.size()));
  819  		// speed and ETA are for a terminal; the card has a bar
  820  		const auto eta = body.find(", ETA ");
  821  		if (eta != std::string::npos)
  822  			body = body.substr(0, eta);
  823  		std::string a, b;
  824  		int percent = -1;
  825  		if (!readPair(body, a, b, percent))
  826  			return out;
  827  		if (allDigits(a) && allDigits(b))
  828  		{
  829  			// the count line has no unit: "0 / 3, 0%"
  830  			out.kind = LiveLine::Kind::Files;
  831  			out.sent = atol(a.c_str());
  832  			out.total = atol(b.c_str());
  833  			return out;
  834  		}
  835  		const long sent = parseBytes(a);
  836  		const long total = parseBytes(b);
  837  		if (sent < 0 || total < 0)
  838  			return out;
  839  		out.kind = LiveLine::Kind::Bytes;
  840  		out.sent = sent;
  841  		out.total = total;
  842  		out.percent = percent;
  843  		return out;
  844  	}
  845  
  846  	if (checks != std::string::npos)
  847  	{
  848  		// rclone's check counter -- "Checks: 12 / 70, 17%, Listed 313" --
  849  		// is a comparison, not a transfer, and its percentage is not the
  850  		// bar's: drawn as one it reads as seventy uploads.
  851  		std::string a, b;
  852  		int percent = -1;
  853  		if (!readPair(Utils::String::trim(clean.substr(checks + CHECKS.size())), a, b, percent))
  854  			return out;
  855  		if (!allDigits(a) || !allDigits(b))
  856  			return out;
  857  		out.kind = LiveLine::Kind::Checks;
  858  		out.sent = atol(a.c_str());
  859  		out.total = atol(b.c_str());
  860  		return out;
  861  	}
  862  
  863  	// A per-file line (" * name: 32% /292.969Ki, 95.996Ki/s, 2s") is
  864  	// written for a log; the card's title already says what is moving.
  865  	if (clean.rfind("* ", 0) == 0)
  866  		return out;
  867  
  868  	// Anything else carries progress if it has a percentage or an "x / y"
  869  	// count, and is shown as it came. rclone's headers, the elapsed time
  870  	// and the scripts' banners have neither, and stay off the card.
  871  	if (clean.find('%') != std::string::npos || clean.find(" / ") != std::string::npos)
  872  	{
  873  		out.kind = LiveLine::Kind::Other;
  874  		out.text = clean;
  875  	}
  876  	return out;
  877  }
  878  
  879  LiveWords liveWords(const LiveLine& live, bool bytesMoving, bool countShown)
  880  {
  881  	switch (live.kind)
  882  	{
  883  	case LiveLine::Kind::Bytes:
  884  		// A total means rclone has queued something to move; bytes sent mean
  885  		// it is moving. Either way the byte line is the fact. "0 B / 0 B" is
  886  		// the listing and the compare: progress, said as such -- unless the
  887  		// count already says it with a number.
  888  		if (live.sent > 0 || live.total > 0)
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 1092-1116 (excerpt of 1409)

```text
 1092  // its other parts in English (audit of the fixes, E2 claude G-E2-08).
 1093  std::vector<std::pair<std::string, std::string>> CloudText::unitLabels()
 1094  {
 1095  	return {
 1096  		{ "SETTINGS", _("SETTINGS") },
 1097  		{ "SAVES", _("SAVES") },
 1098  		{ "ROMS AND BIOS", _("ROMS AND BIOS") },
 1099  		{ "GAME CONTENT", _("GAME CONTENT") },
 1100  		{ "ROMS, BIOS, AND GAME CONTENT", _("ROMS, BIOS, AND GAME CONTENT") },
 1101  		{ "RESTORING SAVES", _("RESTORING SAVES") },
 1102  		{ "BACKING UP SAVES", _("BACKING UP SAVES") },
 1103  		{ "RESTORING ROMS AND BIOS", _("RESTORING ROMS AND BIOS") },
 1104  		// The scan page's three items and the move page's set-aside (fork
 1105  		// #350, #353); SAVES and SETTINGS are the move's other two.
 1106  		{ "CLOUD FOLDER", _("CLOUD FOLDER") },
 1107  		{ "SETTINGS BACKUPS", _("SETTINGS BACKUPS") },
 1108  		{ "DISCARDED SAVES", _("DISCARDED SAVES") },
 1109  	};
 1110  }
 1111  
 1112  std::map<std::string, std::string> CloudText::parseKeyValues(const std::string& text)
 1113  {
 1114  	std::map<std::string, std::string> facts;
 1115  	for (auto& raw : Utils::String::split(text, '\n', true))
 1116  	{
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 1379-1395 (excerpt of 1409)

```text
 1379  		line == "ERROR the cloud sync settings could not be saved")
 1380  		return FolderPathRefusal::SettingsWrite;
 1381  	return FolderPathRefusal::Unknown;
 1382  }
 1383  
 1384  std::string CloudText::folderPathRefusalMessage(FolderPathRefusal reason, int exitCode)
 1385  {
 1386  	if (exitCode == 75)
 1387  		return _("WAIT FOR THE CURRENT CLOUD TASK TO FINISH, THEN TRY AGAIN.");
 1388  	if (exitCode == 124)
 1389  		return _("THE FOLDER CHECK TOOK TOO LONG. CHECK YOUR CONNECTION, THEN TRY AGAIN.");
 1390  	switch (reason)
 1391  	{
 1392  	case FolderPathRefusal::Empty:
 1393  		return _("CHOOSE A FOLDER INSIDE YOUR CLOUD STORAGE.");
 1394  	case FolderPathRefusal::InvalidName:
 1395  		return _("THIS FOLDER NAME CAN'T BE USED. CHOOSE A DIFFERENT FOLDER NAME.");
```


## es-app/src/CloudTransferJob.h @ 16dbac5211: lines 9-68 (excerpt of 217)

```text
    9  #include <ctime>
   10  #include <sys/types.h>
   11  #include <functional>
   12  #include <memory>
   13  #include <mutex>
   14  #include <string>
   15  #include <vector>
   16  
   17  // One run of a transfer command -- a back up, a restore or a match as
   18  // GuiMenu composes them, or the journey's first restore -- apart from the
   19  // page that shows it (GuiCloudTransfer): the job reads the pipe to its end
   20  // whatever happens to the page. It was built so the page could be left
   21  // with the run going on (fork #187); since D-UI-078 the page is sat in and
   22  // CANCEL is the way out, and the separation earns its keep the other way
   23  // round -- the page's lifetime never decides the run's, and a cancel is a
   24  // signal to the run, not a page closing. A 1.4 GiB restore is an hour on a
   25  // handheld's Wi-Fi, and the fourth surface tier (es-native-ui.md) is a
   26  // page that outlives the job; the scan page's OfflineScanJob is the model
   27  // this follows.
   28  //
   29  // The run is a thread of its own reading the command's stdout -- rclone's
   30  // stats blocks and the scripts' ">>> " lines; handleLine is the reader and
   31  // its comment the contract -- into the state below, and it keeps itself
   32  // alive (the thread holds the shared_ptr) until the command exits, whether
   33  // or not a page is watching. One run at a time: start() hands back the run
   34  // in flight when there is one, as the scripts' own flock would refuse a
   35  // second (CloudExit::LockHeld). A finished run stays current() until a page
   36  // has shown its outcome and been dismissed (dismiss()), so the row that
   37  // launched it can say how it went and a press can open the outcome page --
   38  // with TRY AGAIN on it -- however long nobody was watching.
   39  //
   40  // The page is the run's one view and reads the state under mMutex as a
   41  // friend: forty fields, every one of them a row on the page, and a copy of
   42  // them per frame would be the pattern for its own sake.
   43  class CloudTransferJob : public std::enable_shared_from_this<CloudTransferJob>
   44  {
   45  public:
   46  	// What each part of a composed run reported as it ended (">>> tier
   47  	// <label>|<rc>", echoed by GuiMenu's run composition after each part),
   48  	// and which items did not finish, with why (D-UI-028). A ">>> why
   49  	// <sentence>" from a script is attached to the unit it arrived under --
   50  	// or, printed before any unit, to the tier that reports next -- so the
   51  	// done page can name NES and SETTINGS and say what stopped them. A tier
   52  	// that fails with no why under it is itself the item that did not
   53  	// finish, with the code's phrase; its units are not presumed to have
   54  	// finished, because nothing said they did.
   55  	struct Tier { std::string label; int rc; int unitsAnnounced; int unitsFailed; bool tierLevelFail; };
   56  	struct Failed { std::string label; std::string why; };
   57  
   58  	// The run in flight, or the last one not yet dismissed; null when none.
   59  	static std::shared_ptr<CloudTransferJob> current();
   60  	// Whether a run is in flight.
   61  	static bool running();
   62  	// Start a run of command, or hand back the one in flight. itemsExpected
   63  	// and itemsAfterContent are the page's estimate of ITEM i OF n
   64  	// (GuiCloudTransfer's constructor says how they are counted).
   65  	static std::shared_ptr<CloudTransferJob> start(const std::string& command, const std::string& title,
   66  		int itemsExpected, int itemsAfterContent);
   67  	// The outcome has been read on a page: the run is no longer current, and
   68  	// the row that launched it goes back to saying what it does.
```


## es-app/src/CloudTransferJob.h @ 16dbac5211: lines 143-159 (excerpt of 217)

```text
  143  	// show, and the page says so rather than inventing a zero.
  144  	long mUnitBytes, mUnitFiles;
  145  	long mRunBytes, mRunFiles;
  146  	bool mRunSized;
  147  	// ">>> removed 14|314572800|snes:12:300000000,gb:2:14572800" -- a match's
  148  	// summary, rendered on the last screen in place of rclone's totals, which
  149  	// for a deletion read "0 B / 0 B" (maintainer, 2026-09-07).
  150  	long mRemovedFiles, mRemovedBytes;
  151  	std::vector<std::string> mRemovedDetail;   // "SNES 12 FILES · 300 MB", per system
  152  	bool mAnyTransferred;       // some block moved bytes: the device's ROMs changed
  153  	int mFilesThisBlock;
  154  	bool mSeenBlock;
  155  	// "Checks:  12 / 45, 27%, Listed 300" -- what rclone compared rather than
  156  	// moved. A run where everything is already in the cloud is nothing but
  157  	// checks: no bytes, no " * file" lines, and without these it looked hung.
  158  	long mChecksDone, mChecksTotal, mListed;
  159  	std::string mChecking;      // " * name: checking" -- the file being compared, if rclone caught one in flight
```


## es-app/src/CloudTransferJob.h @ 16dbac5211: lines 191-217 (excerpt of 217)

```text
  191  	std::vector<CloudText::StampText> mStampsBefore;
  192  
  193  	// Stopped for a game or by the player: the scripts' trap stamped each
  194  	// part it was inside with 130 and no token; say what happened in their
  195  	// place (#203), with the token for who stopped it.
  196  	void restampStoppedParts(const char* token);
  197  	int mElapsedMs;             // frozen when the run ends
  198  	time_t mFinishedAt;
  199  	// The command's process group (run() starts it under setsid and reads
  200  	// its ">>> pid N" first line), for stopForLaunch; and whether that
  201  	// happened. Atomics: written by the reader thread and the launch gate,
  202  	// read by the page.
  203  	std::atomic<pid_t> mPid{0};
  204  	std::atomic<bool> mStoppedForGame{false};
  205  	std::atomic<bool> mStoppedByPlayer{false};
  206  	// The signal a stop asked for (0 for none), and the last one sent: a
  207  	// stop before the pid line is kept and sent when the line arrives.
  208  	std::atomic<int> mStopSignal{0};
  209  	std::atomic<int> mSignalSent{0};
  210  	void requestStop(int sig);
  211  	void deliverStop();
  212  
  213  	static std::mutex sMutex;
  214  	static std::shared_ptr<CloudTransferJob> sCurrent;
  215  };
  216  
  217  #endif // ES_APP_CLOUD_TRANSFER_JOB_H
```


## es-app/src/ThreadedCloudSync.h @ 16dbac5211: lines 6-28 (excerpt of 201)

```text
    6  #include <string>
    7  #include <thread>
    8  #include <utility>
    9  #include <vector>
   10  #include <sys/types.h>
   11  #include "CloudText.h"
   12  #include "components/AsyncNotificationComponent.h"
   13  
   14  // Runs a headless cloud sync command in the background with a native
   15  // progress card, instead of taking over the screen with a console.
   16  class ThreadedCloudSync
   17  {
   18  public:
   19  	// Who asked for the saves to move. A run that has one leaves a stamp --
   20  	// /storage/.cache/cloud_sync/last-sync-<origin>, "<epoch> <rc>" -- that
   21  	// the cloud settings page reads back as the line under the toggle that
   22  	// caused it (fork #94). The card is gone seconds after the work ends,
   23  	// and somebody who set SYNC SAVES DURING STARTUP needs an answer to "did
   24  	// it run this morning?" from a screen that still exists.
   25  	//
   26  	// The scripts' own stamps (last-backup, last-restore) are per direction
   27  	// and skip the runs that did nothing (CloudExit::LockHeld, NoNetwork);
   28  	// this one is per cause and records the whole run, skips included,
```


## es-app/src/ThreadedCloudSync.h @ 16dbac5211: lines 52-143 (excerpt of 201)

```text
   52  	// only while the sync was still waiting for the network (fork #94); a
   53  	// transfer under way was refused, and with rclone's own timeouts as the
   54  	// only bound on a link that had dropped, that refusal could stand for
   55  	// many minutes (#103). A sync the player asked for keeps the refusal:
   56  	// Origin::Manual, and Origin::None -- the wizard's first backup and the
   57  	// folder tidy -- since they pressed it and can wait for it or stop it
   58  	// themselves.
   59  	//
   60  	// True means the launch may proceed: the sync was one of ours and has
   61  	// ended. False means it may not: nothing running, the player's own
   62  	// sync, or one that had not ended within the budget (two seconds, with
   63  	// SIGKILL to the group at one and a half). The caller refuses on false
   64  	// exactly as it always did.
   65  	//
   66  	// Works on the protocol run() gives every command: it runs under setsid,
   67  	// so its pid is its process group, and its first line is ">>> pid N".
   68  	// The group is sent SIGTERM, so the shell, the scripts and their rclone
   69  	// go together; the scripts' trap exits CloudExit::Stopped, the card says
   70  	// SKIPPED - A GAME WAS STARTED and the stamp records the same, as the
   71  	// network-wait cancel always did.
   72  	//
   73  	// `refusal`, where the caller passes one, says which false it is, so
   74  	// the launch gate can tell the player the right thing (#115). Waiting
   75  	// is the answer to their own sync and the wrong answer to one that is
   76  	// already on its way out.
   77  	enum class CancelRefusal
   78  	{
   79  		// The player pressed this sync. It is still running and was not
   80  		// asked to stop; it finishes, or they stop it.
   81  		PlayerStarted,
   82  		// An automatic sync was signalled and had not gone within the
   83  		// budget -- or had already gone by the time we looked. Either way
   84  		// it is not there to wait for; a moment later the launch works.
   85  		Stopping
   86  	};
   87  	// evenIfPlayerStarted: the player has answered STOP IT AND PLAY to the
   88  	// launch question (D-CLOUD-129; since D-CLOUD-130 it is asked over every
   89  	// sync, automatic ones included), so the origin no longer protects a
   90  	// sync they pressed; the card says SKIPPED - YOU STARTED A GAME.
   91  	static bool cancelForLaunch(CancelRefusal* refusal = nullptr, bool evenIfPlayerStarted = false);
   92  
   93  	// The outcome vocabulary's why for an exit code the scripts did not
   94  	// explain with a ">>> why" line (D-UI-028): rclone 3/4 YOUR CLOUD FOLDER
   95  	// WASN'T FOUND, 5 YOUR CLOUD STOPPED ANSWERING, 7/8 YOUR CLOUD REFUSED
   96  	// THE TRANSFER, 130 IT WAS STOPPED, else SOMETHING WENT WRONG. The token
   97  	// is the same table as one word for the stamps; whyForToken reads it
   98  	// back. Shared with the transfer page and the rows under the toggles so
   99  	// every surface says the same thing about the same code.
  100  	// One stamp file in the last-sync shape (recordOutcome's comment), at any
  101  	// path: recordOutcome's own, and a script's last-backup / last-restore
  102  	// when this process knows an outcome the script's trap could not name.
  103  	static void writeStamp(const std::string& path, int rc, const std::string& token, const std::string& why);
  104  	// A run of `command` that began at runStarted was stopped: the part its
  105  	// stop interrupted -- the script stamp its trap wrote with 130 this run
  106  	// (CloudText::stampsToRestamp) -- is restamped with `token`, the
  107  	// stopper's word for it. Parts that finished keep their outcome; parts
  108  	// that never started keep their last real run's. The card and the
  109  	// transfer page both end a stopped run through here.
  110  	static void restampStoppedParts(const std::string& command, time_t runStarted, const std::string& token);
  111  	// The same with the stamps as they were when the run began (readStamps
  112  	// at its start): a stamp is this run's when its file was written since,
  113  	// not when the clock says so (audit of the fixes G-E1-04/06). The card
  114  	// takes this snapshot; a caller that has none uses the one above.
  115  	static void restampStoppedParts(const std::string& command, const std::vector<CloudText::StampText>& before,
  116  		time_t runStarted, const std::string& token);
  117  	// Each stamp a command's scripts can write, with its text and the file's
  118  	// identity (inode and change time) now.
  119  	static std::vector<CloudText::StampText> readStamps(const std::string& command);
  120  	static std::string whyForCode(int rc);
  121  	static std::string tokenForCode(int rc);
  122  	static std::string whyForToken(const std::string& token);
  123  
  124  private:
  125  	void run();
  126  	// The stamp's fields: "<epoch> <rc> <token>[ <why>]" -- the token is one
  127  	// word for the outcome (completed, gaps, no-network, lock-held,
  128  	// cancelled, stopped, folder-missing, cloud-stopped, cloud-refused,
  129  	// unknown), the why the scripts' own sentence when they printed one
  130  	// (">>> why ..."), for the row to show instead of the token's phrase.
  131  	static void recordOutcome(Origin origin, int rc, const std::string& token, const std::string& why);
  132  
  133  	ThreadedCloudSync(Window* window, const std::string& command,
  134  	                  const std::string& title, const std::string& running,
  135  	                  Origin origin);
  136  	~ThreadedCloudSync();
  137  
  138  	std::string					mCommand;
  139  	std::string					mTitle;
  140  	std::string					mRunning;
  141  	Origin						mOrigin;
  142  	std::vector<CloudText::StampText> mStampsBefore;   // the script stamps as the run began (G-E1-04/06)
  143  	time_t						mStartedAt;   // wall clock, to tell a stamp this run wrote
```


## es-app/src/ThreadedCloudSync.h @ 16dbac5211: lines 182-201 (excerpt of 201)

```text
  182  	int							mBar{-1};
  183  	bool						mBytesMoving{false};
  184  	bool						mCountShown{false};
  185  	// rclone's file count for this half (done / of), from its count line;
  186  	// the byte line's words name the file in flight from it (fork #304).
  187  	long						mFilesDone{-1};
  188  	long						mFilesTotal{-1};
  189  
  190  	Window*						mWindow;
  191  	AsyncNotificationComponent* mWndNotification;
  192  
  193  	static std::atomic<ThreadedCloudSync*> mInstance;
  194  	// Every change to mInstance, and every use of the object it names, is
  195  	// made under this lock: start() checks and installs in one hold, run()
  196  	// clears it before the card's linger, the destructor clears it if it is
  197  	// still this one, and cancelForLaunch dereferences it -- so a caller
  198  	// that took the pointer under the lock has an object that outlives the
  199  	// call, and two starts cannot both see "none" (#308 F-CS-25).
  200  	static std::mutex			sInstanceLock;
  201  };
```


## es-app/src/guis/GuiCloudTransfer.h @ 16dbac5211: lines 6-53 (excerpt of 236)

```text
    6  #include "components/NinePatchComponent.h"
    7  #include "components/TextComponent.h"
    8  
    9  #include <functional>
   10  #include <memory>
   11  #include <string>
   12  #include <vector>
   13  
   14  // A screen for a transfer that takes minutes, not seconds.
   15  //
   16  // The progress card is the right surface for work you can keep playing
   17  // through -- a scrape, a hash. It is the wrong one for a restore: the card
   18  // closes itself when the job ends, and a 1.4 GiB restore is precisely the
   19  // thing somebody walks away from. Come back to a sleeping handheld and the
   20  // only record that anything happened is a log file.
   21  //
   22  // So a long transfer owns the screen and stays there until it is dismissed.
   23  // The result is the last thing on it, not the first thing to disappear.
   24  //
   25  // And it is sat in (D-UI-078, fork #241): the page owns the screen for the
   26  // run's length, and the one way out while it runs is CANCEL -- a
   27  // confirmation that says what cancelling means for this job (what has
   28  // moved stays, the next run finishes the rest), then the stop. Every other
   29  // press is refused while it runs, because there is nothing to choose. For
   30  // a week (#187, D-UI-060/070, the shape audit #186 PL-07 gave the scan
   31  // page) it was the other way: B left the page with the run going on
   32  // behind it, the row that launched it followed the run in its line, and a
   33  // press on that row reopened this page. The maintainer met the same B
   34  // prompt on the scan page and asked what would happen; "nothing tells you"
   35  // was the whole case, and D-UI-078 reversed it. The run is still a
   36  // CloudTransferJob apart from this page -- the job, not the page, reads
   37  // the pipe to its end -- so the seams built for the leavable page (the hub
   38  // row's line, the launch gate's question, the sync card's refusal) stay
   39  // true of a run that is current, and are reached only in the moment
   40  // between the run's end and the page's dismissal, or if this page were
   41  // ever gone while its run was not. A page whose completed run has an
   42  // action in place of an exit (a settings restore: the configuration under
   43  // this process is being replaced, #114) is the exception and takes every
   44  // button, as it did.
   45  class GuiCloudTransfer : public GuiComponent
   46  {
   47  public:
   48  	// itemsExpected: how many items ES chained into this run -- one for saves,
   49  	// one per system the picker left ticked, one for settings -- so row 2 can
   50  	// read ITEM 1 OF 4 before the first script has said anything. 0 means
   51  	// unknown, and row 2 shows ITEM i alone until a script says. A content
   52  	// script announces its own count and corrects it (it may add bios to
   53  	// what was ticked); itemsAfterContent is how many single-item phases ES
```


## es-app/src/guis/GuiCloudTransfer.h @ 16dbac5211: lines 56-108 (excerpt of 236)

```text
   56  	// (CloudTransferJob::start): the scripts' flock would refuse a second.
   57  	GuiCloudTransfer(Window* window, const std::string& command, const std::string& title,
   58  		int itemsExpected = 0, int itemsAfterContent = 0);
   59  	// The page on a run already started: the one in flight, or one that
   60  	// ended while nobody was watching and has not been dismissed.
   61  	GuiCloudTransfer(Window* window, const std::shared_ptr<CloudTransferJob>& job);
   62  	virtual ~GuiCloudTransfer();
   63  
   64  	// What the page does instead of closing, when the run completed.
   65  	//
   66  	// A settings restore replaces the configuration under a running
   67  	// EmulationStation, so there is nowhere safe to go back to: the menu
   68  	// behind this page is drawn from values the restore has just made
   69  	// stale, and the next thing that writes them puts the old ones back
   70  	// over the new. So the page's only exit becomes the action -- any
   71  	// button takes it -- and the three strings say so: `helpVerb` is the
   72  	// word on the help bar, `footer` is line 7, and `note` is line 5, what
   73  	// happens next. Nothing is called when the run did not complete; TRY
   74  	// AGAIN and CLOSE apply then exactly as they always do (#114). A page
   75  	// with an action set is not left while it runs, for the same reason.
   76  	// `cancellable` keeps B while it runs: the folder move (#353) is safe to
   77  	// interrupt -- copy and verify resume, the delete runs only after the
   78  	// verified copy -- where the settings restore is not.
   79  	void setCompletedAction(const std::function<void()>& action, const std::string& helpVerb,
   80  		const std::string& footer, const std::string& note, bool cancellable = false);
   81  	// What the page does the moment the run completes, without a press: the
   82  	// scan before the options page (fork #350, D-CLOUD-156) has no outcome
   83  	// of its own to read -- the page it opens is the outcome -- so a
   84  	// completed scan goes straight on, where a run that did not complete
   85  	// stays with its why and TRY AGAIN beside CLOSE as every page does.
   86  	// CANCEL stays while it runs. Taken on the interface thread, posted
   87  	// from update(), and refused when the page shows another command's run.
   88  	void setAutoContinue(const std::function<void()>& action);
   89  	// What the page does once it is closed without its completed action:
   90  	// a run that did not complete, or another command's run. The cloud
   91  	// folder step (D-CLOUD-170, fork #363) goes on when its scan or its
   92  	// move did not complete -- at the end of cloud setup the wizard's last
   93  	// page must still come -- where a transfer page's CLOSE goes back to
   94  	// the page underneath. Taken in place of a script's offer: the step's
   95  	// pages raise none.
   96  	void setDismissedAction(const std::function<void()>& action);
   97  	// Line 5 when the run did not complete, in place of the verb's clause:
   98  	// the folder move says what it leaves (YOUR CLOUD STILL HAS /ROCKNIX.
   99  	// NOTHING WAS REMOVED.), which no verb's words say.
  100  	void setFailedNote(const std::string& note);
  101  
  102  	void render(const Transform4x4f& parentTrans) override;
  103  	bool input(InputConfig* config, Input input) override;
  104  	std::vector<HelpPrompt> getHelpPrompts() override;
  105  	void update(int deltaTime) override;
  106  
  107  	// A size at the precision it has: "200 KB", "1.2 MB", "1.20 GB". The one
  108  	// formatter for every size a cloud page prints -- this page's summary,
```


## es-app/src/guis/GuiCloudTransfer.h @ 16dbac5211: lines 142-191 (excerpt of 236)

```text
  142  	{
  143  		bool completed;   // every part finished (0 or 9)
  144  		bool partial;     // some finished and some did not; a failure to the player
  145  		bool skipped;     // a sentinel, and nothing else to report
  146  		std::string word; // line 1
  147  	};
  148  	static Outcome outcome(const CloudTransferJob& job);
  149  	// Whether TRY AGAIN, the same command again, is offered: not for a match.
  150  	static bool retries(const CloudTransferJob& job);
  151  	// BACKING UP... / RESTORING... / MATCHING..., from the run's command.
  152  	static std::string verbWord(const CloudTransferJob& job);
  153  	// The rows only the done state writes, cleared for a TRY AGAIN so the
  154  	// new run does not start under last time's note.
  155  	void clearDoneRows();
  156  	// Whether B leaves the page while the run goes on: not when the completed
  157  	// run has an action in place of an exit.
  158  	// Whether B while it runs offers CANCEL (D-UI-078). Not on a page whose
  159  	// completed run has an action in place of an exit (setCompletedAction):
  160  	// a settings restore is replacing the configuration under this process,
  161  	// and there is nowhere safe to stop.
  162  	bool cancellable() const { return !mCompletedAction || mActionCancellable; }
  163  	// The CANCEL confirmation: what cancelling means, then
  164  	// CloudTransferJob::stopByPlayer() on YES.
  165  	void askCancel();
  166  
  167  	BusyComponent mBusyAnim;
  168  	NinePatchComponent mBackground;
  169  
  170  	std::shared_ptr<TextComponent> mTitle;
  171  	// Seven lines under the title (maintainer's layout, 2026-09-06, D-UI-024;
  172  	// the item first and numbered across the run, 2026-09-09, D-UI-026): the
  173  	// item, ITEM i OF n, what it is doing on it, that item's files and bytes,
  174  	// the bar, elapsed, and the notice. Each is one line, fitted to the
  175  	// width, so nothing wraps into the line below. Once the run is over the
  176  	// same four rows carry the outcome, the run's summary and its detail.
  177  	std::shared_ptr<TextComponent> mStatus;    // 1. the item (BIOS, NES, SAVES, SETTINGS); the outcome, once done
  178  	std::shared_ptr<TextComponent> mCounter;   // 2. ITEM i OF n, counted across the whole run
  179  	std::shared_ptr<TextComponent> mActivity;  // 3. what it is doing on that item; the run's summary, once done
  180  	std::shared_ptr<TextComponent> mDetail;    // 4. that item's files and bytes so far; the summary's detail, once done
  181  	std::shared_ptr<TextComponent> mNote;      // 5. where the bar was: what to do next, once done
  182  	std::shared_ptr<TextComponent> mElapsed;   // 6. elapsed
  183  	std::shared_ptr<TextComponent> mFooter;    // 7. the notice / press any button
  184  	std::shared_ptr<Font> mTextFont;
  185  	std::shared_ptr<Font> mSmallFont;
  186  	float mLineWidth;
  187  	static std::string fitOneLine(const std::shared_ptr<Font>& font, std::string text, float width);
  188  	// Drop whole sentences from the end before clipping: "WHAT WAS SENT IS IN
  189  	// YOUR CLOUD. THE REST IS STILL ON THIS DEVICE." keeps its first sentence
  190  	// on a panel too narrow for both, rather than ending mid-word in an
  191  	// ellipsis. The last sentence standing is clipped if even it does not fit.
```


## es-app/tests/unit/CloudTextTests.cpp @ 16dbac5211: lines 624-729 (excerpt of 1784)

```text
  624  	{
  625  		INFO(candidate);
  626  		CHECK(candidate.find(inPlace) != std::string::npos);
  627  	}
  628  	CHECK(c.front() == inPlace + " " + waiting.front());
  629  	CHECK(c.back() == inPlace);   // the shortest still says what moved
  630  }
  631  
  632  TEST_CASE("every protocol shape an emitter prints classifies to a known kind")
  633  {
  634  	struct Shape { const char* line; ProtocolKind kind; const char* from; };
  635  
  636  	// projects/ROCKNIX/packages/network/rclone/sources/ and
  637  	// projects/ROCKNIX/packages/rocknix/sources/scripts/, on next.
  638  	static const Shape shapes[] = {
  639  		// New cloud setup/check emitters at distribution 6f89bc7cec (#512).
  640  		{ ">>> why YOUR CLOUD SETTINGS CHANGED. CHECK AGAIN", ProtocolKind::Why, "cloud_scan:219" },
  641  		{ ">>> why ANOTHER CLOUD CHECK IS RUNNING", ProtocolKind::Why, "cloud_scan:358" },
  642  		{ ">>> why YOUR CLOUD FOLDERS COULDN'T BE CREATED", ProtocolKind::Why, "cloud_setup:804,867" },
  643  		// Every ">>> why" a script prints, from the scripts at next 4476f90394
  644  		// (regenerated, #308 follow-up: the table was f0f263b8cc's, and since
  645  		// then stream A's scripts print four sentences and backuptool five
  646  		// that it did not list, and ">>> unit everything" is gone -- --all
  647  		// makes each system and BIOS a unit of its own). The why_for tables
  648  		// print the rc-keyed ones; backuptool's why() and cloud_saves_root
  649  		// print theirs with echo.
  650  		{ ">>> why YOUR CLOUD STORAGE ISN'T SET UP YET", ProtocolKind::Why, "cloud_backup:843, cloud_restore:914, cloud_content_backup:95, :119, cloud_content_restore:98, :122" },
  651  		{ ">>> why COULDN'T REACH YOUR CLOUD - CHECK YOUR SIGN-IN", ProtocolKind::Why, "cloud_backup:868, cloud_restore:939" },
  652  		{ ">>> why YOUR CLOUD STOPPED ANSWERING", ProtocolKind::Why, "cloud_backup:933, :740, :751, cloud_restore:1000, :802, :813, cloud_content_backup:183, cloud_content_restore:189" },
  653  		{ ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ", ProtocolKind::Why, "cloud_backup:1011, :1017, :1475, cloud_restore:1078, :1084, :1578, cloud_content_backup:112, cloud_content_restore:115" },
  654  		{ ">>> why AN OLD FOLDER SETTING IS IN THE WAY", ProtocolKind::Why, "cloud_backup:1029, cloud_restore:1096" },
  655  		{ ">>> why CHECK WHAT WOULD CHANGE FIRST", ProtocolKind::Why, "cloud_content_restore:851 (a --match --apply with no plan)" },
  656  		{ ">>> why YOUR SAVES FOLDER ISN'T ON THIS DEVICE", ProtocolKind::Why, "cloud_backup:1379" },
  657  		{ ">>> why THIS DEVICE'S SETTINGS BACKUP IS DAMAGED", ProtocolKind::Why, "cloud_backup:1882, backuptool:1116" },
  658  		{ ">>> why THE COPY IN YOUR CLOUD ISN'T COMPLETE", ProtocolKind::Why, "cloud_backup:1993" },
  659  		{ ">>> why COULDN'T FIND YOUR CLOUD FOLDER", ProtocolKind::Why, "why_for 3|4: cloud_backup:739, cloud_restore:801, cloud_content_backup:182, cloud_content_restore:188" },
  660  		{ ">>> why SOME FILES DIDN'T FINISH", ProtocolKind::Why, "why_for 6: cloud_backup:741, cloud_restore:803, cloud_content_backup:184, cloud_content_restore:190" },
  661  		{ ">>> why YOUR CLOUD WOULDN'T TAKE THE FILES", ProtocolKind::Why, "why_for 7|8: cloud_backup:742, cloud_restore:804, cloud_content_backup:185, cloud_content_restore:191" },
  662  		{ ">>> why IT WAS STOPPED", ProtocolKind::Why, "why_for 130: cloud_backup:743, cloud_restore:805, cloud_content_backup:186, cloud_content_restore:192" },
  663  		{ ">>> why THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME", ProtocolKind::Why, "why_for 10|124 automatic: cloud_backup:749, cloud_restore:811" },
  664  		{ ">>> why SOMETHING WENT WRONG", ProtocolKind::Why, "why_for *: cloud_backup:753, cloud_restore:815, cloud_content_backup:187, cloud_content_restore:193" },
  665  		{ ">>> why SOMETHING CHANGED SINCE YOU CHECKED", ProtocolKind::Why, "cloud_content_restore:781, :824 (a match whose plan no longer matches its preview)" },
  666  		{ ">>> why COULDN'T TELL WHICH CARD YOUR SAVES ARE ON", ProtocolKind::Why, "cloud_saves_root:137" },
  667  		{ ">>> why YOUR SAVES ARE ON A DIFFERENT CARD", ProtocolKind::Why, "cloud_saves_root:156" },
  668  		{ ">>> why YOUR SAVES CHANGED CARDS PART-WAY THROUGH", ProtocolKind::Why, "cloud_saves_root:177" },
  669  		{ ">>> why COULDN'T RECORD WHICH CARD YOUR SAVES ARE ON", ProtocolKind::Why, "cloud_saves_root:185" },
  670  		{ ">>> why THIS DEVICE CAN'T RESTORE SETTINGS", ProtocolKind::Why, "backuptool:1089" },
  671  		{ ">>> why A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING", ProtocolKind::Why, "backuptool:1094, :1348" },
  672  		{ ">>> why THERE'S NO SETTINGS BACKUP ON THIS DEVICE YET", ProtocolKind::Why, "backuptool:1101" },
  673  		{ ">>> why COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS", ProtocolKind::Why, "backuptool:1175, :1206" },
  674  		{ ">>> why THE RESTORE COULDN'T FINISH", ProtocolKind::Why, "backuptool:1300, :1303" },
  675  		{ ">>> why THIS DEVICE CAN'T MAKE A SETTINGS BACKUP", ProtocolKind::Why, "backuptool:1342" },
  676  		{ ">>> why THERE'S NOTHING TO BACK UP YET", ProtocolKind::Why, "backuptool:1379" },
  677  		{ ">>> why THE BACKUP COULDN'T FINISH WHILE GATHERING YOUR SETTINGS", ProtocolKind::Why, "backuptool:1381" },
  678  		{ ">>> why A SIGN-IN WAS FOUND IN THE BACKUP", ProtocolKind::Why, "backuptool:1383" },
  679  		{ ">>> why YOUR OWN BACKUP LIST NAMES A FOLDER A BACKUP CAN'T CARRY", ProtocolKind::Why, "backuptool:1385" },
  680  		{ ">>> why THE BACKUP COULDN'T FINISH", ProtocolKind::Why, "backuptool:1387" },
  681  		{ ">>> doing network", ProtocolKind::Doing, "cloud_net_ready:160, :213" },
  682  		{ ">>> unit SAVES||", ProtocolKind::Unit, "cloud_backup:1349, cloud_restore:1408" },
  683  		{ ">>> unit SETTINGS||", ProtocolKind::Unit, "cloud_backup:1661, cloud_restore:1691" },
  684  		{ ">>> unit snes|2|5", ProtocolKind::Unit, "cloud_content_backup:572, cloud_content_restore:1363 (every run, --all included), :810 (--match --apply)" },
  685  		{ ">>> unit bios|6|6", ProtocolKind::Unit, "cloud_content_restore:1363 (--all: BIOS is a unit of its own)" },
  686  		{ ">>> removed 14|314572800|snes:12:300000000,gb:2:14572800", ProtocolKind::Removed, "cloud_content_restore:844, :915, :957" },
  687  		{ ">>> offer create-saves-folder|/ROCKNIX/Savez|/ROCKNIX/Saves", ProtocolKind::Offer, "cloud_restore:1497" },
  688  		{ ">>> offer create-saves-folder|/ROCKNIX/Saves", ProtocolKind::Offer, "cloud_restore:1506" },
  689  
  690  		// EmulationStation's own: the wrapper, and the run compositions
  691  		// that chain several scripts into one page or one card.
  692  		{ ">>> pid 1234", ProtocolKind::Pid, "ThreadedCloudSync.cpp:200, CloudTransferJob.cpp:602, OfflineScanJob.cpp:135" },
  693  		{ ">>> doing network", ProtocolKind::Doing, "main.cpp:672" },
  694  		{ ">>> doing receive", ProtocolKind::Doing, "main.cpp:678" },
  695  		{ ">>> doing send", ProtocolKind::Doing, "main.cpp:681" },
  696  		{ ">>> doing unpack", ProtocolKind::Doing, "GuiMenu.cpp:4755" },
  697  		{ ">>> doing archive", ProtocolKind::Doing, "GuiMenu.cpp:4820" },
  698  		{ ">>> unit SETTINGS||", ProtocolKind::Unit, "GuiMenu.cpp:4754, :4820" },
  699  		{ ">>> tier RESTORING SAVES|0", ProtocolKind::Tier, "main.cpp:680; GuiMenu.cpp:5845; JourneyTiers.h:97" },
  700  		{ ">>> tier BACKING UP SAVES|0", ProtocolKind::Tier, "main.cpp:683, GuiMenu.cpp:5846" },
  701  		{ ">>> tier RESTORING ROMS AND BIOS|5", ProtocolKind::Tier, "JourneyTiers.h:96" },
  702  		{ ">>> tier ROMS AND BIOS|0", ProtocolKind::Tier, "GuiMenu.cpp:4717 (the transfer page's parts, by label)" },
  703  	};
  704  
  705  	for (auto& shape : shapes)
  706  	{
  707  		INFO(std::string(shape.from) << "  ->  " << std::string(shape.line));
  708  		const ProtocolLine p = classifyProtocolLine(shape.line);
  709  		CHECK(p.kind == shape.kind);
  710  		// Said twice on purpose: the assertion above is the shape, this one
  711  		// is the rule -- no emitter's line is a line a reader cannot place.
  712  		CHECK(p.kind != ProtocolKind::Unknown);
  713  		CHECK(p.kind != ProtocolKind::NotProtocol);
  714  		// And no why an emitter prints is left in English under a
  715  		// translated outcome word: the card has its translation (#308
  716  		// F-CS-31).
  717  		if (p.kind == ProtocolKind::Why)
  718  			CHECK(isKnownWhy(p.text));
  719  	}
  720  }
  721  
  722  TEST_CASE("each why's two spellings agree, so its translation is found (#308 5 gpt F-CS-31)")
  723  {
  724  	// whySentences pairs the English a script prints with _("") of the same
  725  	// English, for xgettext to carry into the catalog. The unit build has no
  726  	// gettext, so _() hands the English back: a pair whose two copies differ
  727  	// by a letter is a sentence the card will never translate.
  728  	const auto sentences = whySentences();
  729  	CHECK(sentences.size() >= 32);
```


## es-app/tests/unit/CloudTextTests.cpp @ 16dbac5211: lines 851-886 (excerpt of 1784)

```text
  851  	CHECK(chooseThatFits(candidates, 4.0f, nullptr) == "0123456789");
  852  
  853  	// Nothing offered, nothing shown.
  854  	CHECK(chooseThatFits({}, 100.0f, measure) == "");
  855  }
  856  
  857  // ------------------------------------------------------------------- sizes
  858  
  859  TEST_CASE("parseBytes reads rclone's size fields")
  860  {
  861  	CHECK(parseBytes("0 B") == 0);
  862  	CHECK(parseBytes("80 KiB") == 81920);
  863  	CHECK(parseBytes("1.4 GiB") == 1503238554);   // 1503238553.6, rounded
  864  	CHECK(parseBytes("  878.906 KiB ") == 900000);
  865  	// the torn units of a per-file line cut at 80 columns
  866  	CHECK(parseBytes("292.969Ki") == 300000);
  867  	CHECK(parseBytes("2.5Mi") == 2621440);
  868  
  869  	// no number, an unknown unit, or something no size ever is
  870  	CHECK(parseBytes("") == -1);
  871  	CHECK(parseBytes("KiB") == -1);
  872  	CHECK(parseBytes("12 furlongs") == -1);
  873  	CHECK(parseBytes("inf") == -1);
  874  	CHECK(parseBytes("nan B") == -1);
  875  	CHECK(parseBytes("-5 KiB") == -1);
  876  }
  877  
  878  TEST_CASE("sizeLabel prints a size at the precision it has")
  879  {
  880  	CHECK(sizeLabel(0) == "0 KB");
  881  	CHECK(sizeLabel(1) == "1 KB");          // never "0 KB" for something
  882  	CHECK(sizeLabel(204800) == "200 KB");
  883  	CHECK(sizeLabel(900000) == "879 KB");
  884  	CHECK(sizeLabel(1258291) == "1.2 MB");
  885  	CHECK(sizeLabel(1288490189) == "1.20 GB");
  886  	// the unit is chosen from the value as it will print: a byte short of
```


## es-app/tests/unit/CloudTextTests.cpp @ 16dbac5211: lines 899-945 (excerpt of 1784)

```text
  899  	CHECK(roundSizes("3m2s left, 27%") == "3m2s left, 27%");
  900  	// a number whose unit did not parse is left as it was
  901  	CHECK(roundSizes("12 furlongs") == "12 furlongs");
  902  	CHECK(roundSizes("") == "");
  903  }
  904  
  905  // --------------------------------------------------------------- live line
  906  
  907  TEST_CASE("liveLine reads the byte line wherever the glue put it")
  908  {
  909  	// The card that produced #140: the block before ended without a
  910  	// newline, so its last line arrived in front of the next block's first.
  911  	auto l = liveLine("Elapsed time:         2.0sTransferred:            0 B / 0 B, -, 0 B/s, ETA -");
  912  	CHECK(l.kind == LiveLine::Kind::Bytes);
  913  	CHECK(l.sent == 0);
  914  	CHECK(l.total == 0);
  915  	CHECK(l.percent == -1);
  916  
  917  	// a busier run glues a per-file line on instead
  918  	l = liveLine("* f3.srm: 98% /292.969Ki, 71.998Ki/s, 0sTransferred:         864 KiB / 878.906 KiB, 98%, 223.999 KiB/s, ETA 0s");
  919  	CHECK(l.kind == LiveLine::Kind::Bytes);
  920  	CHECK(l.sent == 884736);
  921  	CHECK(l.total == 900000);
  922  	CHECK(l.percent == 98);
  923  
  924  	// and a line that arrived on its own reads the same
  925  	l = liveLine("Transferred:        288 KiB / 878.906 KiB, 33%, 287.998 KiB/s, ETA 2s");
  926  	CHECK(l.kind == LiveLine::Kind::Bytes);
  927  	CHECK(l.sent == 294912);
  928  	CHECK(l.total == 900000);
  929  	CHECK(l.percent == 33);
  930  
  931  	// the tab after the label is already gone by the time the card reads
  932  	// it (the pipe loop keeps printable ASCII), but a stray one is harmless
  933  	l = liveLine("Transferred:\t  878.906 KiB / 878.906 KiB, 100%, 217.241 KiB/s, ETA 0s");
  934  	CHECK(l.kind == LiveLine::Kind::Bytes);
  935  	CHECK(l.percent == 100);
  936  }
  937  
  938  TEST_CASE("liveLine tells the count line and the check counter apart")
  939  {
  940  	auto l = liveLine("Transferred:            0 / 3, 0%");
  941  	CHECK(l.kind == LiveLine::Kind::Files);
  942  	CHECK(l.sent == 0);
  943  	CHECK(l.total == 3);
  944  	CHECK(l.percent == -1);   // never the bar's
  945  
```


## es-app/src/FileData.cpp @ 16dbac5211: lines 977-1038 (excerpt of 2680)

```text
  977  	// waits behind a spinner for it to be gone -- the automatic sync's wait,
  978  	// for the same reason: a rename must not land under a game that has the
  979  	// save open -- and then launches through ViewController, launch effect
  980  	// and all; KEEP WAITING (B as well) leaves it running. Stopping is safe
  981  	// for the reason the automatic cancel is: the scripts are rclone copy,
  982  	// each file renamed into place whole, so the next run finishes what this
  983  	// one did not, and a match's deletions stop where they are. The run's
  984  	// outcome reads SKIPPED - YOU STARTED A GAME, as the card's does.
  985  	//
  986  	// One question for any sync on the card, whoever started it. STOP IT AND
  987  	// PLAY cancels it (cancelForLaunch with the player's answer, which sends
  988  	// the group SIGTERM and waits its two seconds) and launches; a sync slow
  989  	// to die is waited for behind the spinner rather than refused.
  990  	if (!captureGate(window, this, options))
  991  		return false;
  992  
  993  	if (ThreadedCloudSync::isRunning())
  994  	{
  995  		window->pushGui(new GuiMsgBox(window,
  996  			_("YOUR SAVES ARE SYNCING WITH THE CLOUD.") + "\n\n" + _("IF YOU STOP IT, THE NEXT SYNC FINISHES WHAT THIS ONE DID NOT."),
  997  			_("STOP IT AND PLAY"), [this, window, options]
  998  			{
  999  				LOG(LogInfo) << "launch: the player chose to stop the sync for a game";
 1000  				ThreadedCloudSync::CancelRefusal again = ThreadedCloudSync::CancelRefusal::Stopping;
 1001  				if (ThreadedCloudSync::cancelForLaunch(&again, true) || !ThreadedCloudSync::isRunning())
 1002  					launchNow(window, this, options);
 1003  				else
 1004  					launchWhenGone(window, this, options, [] { return ThreadedCloudSync::isRunning(); }, nullptr);
 1005  			},
 1006  			_("KEEP WAITING"), nullptr));
 1007  		return false;
 1008  	}
 1009  
 1010  	if (const std::shared_ptr<CloudTransferJob> transfer = CloudTransferJob::current(); transfer != nullptr && !transfer->finished())
 1011  	{
 1012  		window->pushGui(new GuiMsgBox(window,
 1013  			GuiCloudTransfer::stillRunningSentence(transfer) + "\n\n" + _("IF YOU STOP IT, WHAT IT HAS NOT MOVED YET WAITS FOR THE NEXT RUN."),
 1014  			_("STOP IT AND PLAY"), [this, window, options]
 1015  			{
 1016  				LOG(LogInfo) << "launch: the player chose to stop the transfer for a game";
 1017  				CloudTransferJob::stopForLaunch(false);
 1018  				launchWhenGone(window, this, options, [] { return CloudTransferJob::running(); }, [] { CloudTransferJob::stopForLaunch(true); });
 1019  			},
 1020  			_("KEEP WAITING"), nullptr));
 1021  		return false;
 1022  	}
 1023  
 1024  	// The offline achievements' two jobs ask the same question (fork #293,
 1025  	// D-UI-095). The send is the proxy's and cannot be stopped from here,
 1026  	// so its question offers to play through it: PLAY NOW launches at once
 1027  	// and the proxy goes on sending behind the game. The top-up can be
 1028  	// stopped: STOP IT AND PLAY signals the ctl and waits for it to be
 1029  	// gone, and the ctl runs again next time the device is connected. The
 1030  	// safe verb is last in both (D-UI-096).
 1031  	if (ProxyCards::sendRunning() && !playThroughSend)
 1032  	{
 1033  		window->pushGui(new GuiMsgBox(window,
 1034  			_("OFFLINE ACHIEVEMENTS ARE BEING SENT.") + "\n\n" + _("IT'LL BE A MOMENT."),
 1035  			_("PLAY NOW"), [this, window, options]
 1036  			{
 1037  				LOG(LogInfo) << "launch: the player chose to play through the send";
 1038  				sPlayThroughSend = true;
```


## es-app/src/guis/GuiMenu.cpp @ 16dbac5211: lines 4998-5014 (excerpt of 11747)

```text
 4998  		// SETTINGS) -- so the page can say which parts finished and which did
 4999  		// not: a run where one did and one did not is a failure with that part's why,
 5000  		// never the last part's code over the first part's files (D-UI-028).
 5001  		std::string cmd;
 5002  		auto add = [&cmd](const std::string& label, const std::string& part)
 5003  		{
 5004  			if (cmd.empty())
 5005  				cmd = "rc=0";
 5006  			cmd += " ; _t=0 ; { " + part + " ; } || _t=$? ; echo \">>> tier " + label + "|$_t\" ; [ \"$_t\" = 0 ] || rc=$_t";
 5007  		};
 5008  
 5009  		// A settings restore rewrites the configuration and restarts the
 5010  		// device, so it cannot be one link in a chain -- anything after it
 5011  		// would never run. The journey marker is what carries the rest
 5012  		// across the restart -- and backuptool sets it (--then-cloud), after
 5013  		// its extract has been verified, where this used to touch it before
 5014  		// the restore ran: a download that never happened, or a restore that
```


## es-app/src/guis/GuiMenu.cpp @ 16dbac5211: lines 5030-5108 (excerpt of 11747)

```text
 5030  		//
 5031  		// What else was ticked rides across the restart in a record of its own
 5032  		// (JourneyTiers, audit #307 PL-029): the start builds the continuation
 5033  		// from it, where it used to run everything whatever was ticked -- the
 5034  		// dialog promising the ticks, the continuation restoring ROMs and BIOS
 5035  		// over Wi-Fi to a player who had asked for saves. It is written on YES,
 5036  		// not before the question, so a NO leaves nothing behind. With nothing
 5037  		// else ticked there is nothing to continue: no marker is asked for, the
 5038  		// dialog does not promise one, and a record an earlier attempt left is
 5039  		// removed.
 5040  		if (!backup && wantSettings)
 5041  		{
 5042  			const bool rest = wantSaves || wantContent || wantMedia;
 5043  			add("SETTINGS", std::string("echo '>>> unit SETTINGS||' ; /usr/bin/cloud_restore --yes --system-only"
 5044  				" && { echo '>>> doing unpack' ; /usr/bin/backuptool restore")
 5045  				+ (rest ? " --then-cloud" : "") + " --no-restart ; }");
 5046  			cmd += " ; exit $rc";
 5047  			const std::string question = rest
 5048  				? _("RESTORE SETTINGS FIRST, THEN RESTART?\n\nYOUR EXISTING CONFIGURATION IS REPLACED. ANYTHING ELSE YOU TICKED IS RESTORED AFTER THE RESTART. WI-FI AND ACCOUNT PASSWORDS MUST BE RE-ENTERED.")
 5049  				: _("RESTORE SETTINGS, THEN RESTART?\n\nYOUR EXISTING CONFIGURATION IS REPLACED. WI-FI AND ACCOUNT PASSWORDS MUST BE RE-ENTERED.");
 5050  			window->pushGui(new GuiMsgBox(window, question, _("YES"),
 5051  				[window, s, cmd, rest, wantSaves, wantContent, wantMedia]
 5052  				{
 5053  					const std::string record = JourneyTiers::PATH;
 5054  					if (rest)
 5055  					{
 5056  						Utils::FileSystem::createDirectory(Utils::FileSystem::getParent(record));
 5057  						// This restore's ticks, or no record at all: an earlier
 5058  						// attempt's record at the same path was read as this one's
 5059  						// when the write failed (audit of the fixes, E2 gpt G-E2-01).
 5060  						// No record leaves the start with a marker and nothing to
 5061  						// read: it offers everything and its prompt names
 5062  						// everything. A record that can be neither replaced nor
 5063  						// removed stops the restore here, before anything changes.
 5064  						const JourneyTiers::Replaced replaced = JourneyTiers::replaceRecord(
 5065  							JourneyTiers::record(wantSaves, wantContent, wantMedia),
 5066  							[&record](const std::string& text) { return Utils::AtomicFile::writeText(record, text); },
 5067  							[&record]() { return Utils::FileSystem::removeFile(record); },
 5068  							[&record]() { return Utils::FileSystem::exists(record, false); });
 5069  						if (replaced == JourneyTiers::Replaced::NoRecord)
 5070  							LOG(LogWarning) << "restore: the journey record could not be written to " << record << "; the start will offer everything";
 5071  						else if (replaced == JourneyTiers::Replaced::OldRecordStands)
 5072  						{
 5073  							LOG(LogError) << "restore: an earlier journey record at " << record << " could be neither replaced nor removed; the restore was not started";
 5074  							s->close();
 5075  							window->pushGui(new GuiMsgBox(window, _("COULDN'T SAVE WHAT YOU TICKED, SO NOTHING WAS RESTORED."), _("OK")));
 5076  							return;
 5077  						}
 5078  					}
 5079  					else if (Utils::FileSystem::exists(record, false))
 5080  						Utils::FileSystem::removeFile(record);
 5081  					s->close();
 5082  					auto page = new GuiCloudTransfer(window, cmd, _("RESTORING SETTINGS FROM THE CLOUD"), 1);
 5083  					page->setCompletedAction([]
 5084  					{
 5085  						// The configuration on disk is no longer the one
 5086  						// this process holds. Re-read it before anything
 5087  						// can write the old values back over the restore:
 5088  						// ViewController::saveState() saves es_settings.cfg
 5089  						// on the way out whenever the player has moved to
 5090  						// another system since this boot, and that write
 5091  						// carries every other setting with it.
 5092  						Settings::getInstance()->loadFile();
 5093  						SystemConf::getInstance()->loadSystemConf();
 5094  						ViewController::configurationReplaced();
 5095  						Utils::Platform::quitES(Utils::Platform::QuitMode::REBOOT);
 5096  					}, _("RESTART"), _("PRESS ANY BUTTON TO RESTART"),
 5097  					   _("THIS DEVICE RESTARTS SO YOUR RESTORED SETTINGS TAKE EFFECT."));
 5098  					window->pushGui(page);
 5099  				}, _("NO"), nullptr));
 5100  			return;
 5101  		}
 5102  
 5103  		// Order matters on a backup: the settings archive is written last so
 5104  		// the copy that goes up is the current one.
 5105  		// --saves-only: without it the saves scripts run their settings-archive
 5106  		// phase too, and a run with SETTINGS unticked still moved the archive
 5107  		// under a SETTINGS BACKUP label the page then kept showing through the
 5108  		// ROMs (maintainer, 2026-09-06). The settings tier below is the only
```


## es-app/src/guis/GuiMenu.cpp @ 16dbac5211: lines 5117-5133 (excerpt of 11747)

```text
 5117  		// The settings item announces itself before backuptool runs, and says
 5118  		// what it is doing while the archive is written: backuptool prints
 5119  		// nothing the page can use, and without these two lines the item sat
 5120  		// on PREPARING... over a spinner while every other item showed its
 5121  		// files (maintainer, 2026-09-09, D-UI-026). cloud_backup announces
 5122  		// ">>> unit SETTINGS||" again when its turn comes; the same label, so
 5123  		// the page does not count it twice.
 5124  		if (backup && wantSettings)
 5125  			add("SETTINGS", "echo '>>> unit SETTINGS||' ; echo '>>> doing archive' ; /usr/bin/backuptool backup >/dev/null 2>&1 && /usr/bin/cloud_backup --yes --system-only");
 5126  
 5127  		// How many items the page should expect (ITEM i OF n, D-UI-026): one
 5128  		// for saves, one per system the picker left ticked, one for settings.
 5129  		// The selection is the file cloud_content_restore --set-systems wrote
 5130  		// as the picker closed -- read here rather than asked for through the
 5131  		// script, whose startup runs rclone listremotes: a process on the UI
 5132  		// thread for a number the content script corrects anyway when it
 5133  		// announces its own count (it adds bios to what was ticked). The
```


## es-app/src/guis/GuiMenu.cpp @ 16dbac5211: lines 6132-6149 (excerpt of 11747)

```text
 6132  		// (">>> tier <label>|<rc>"), so a restore that finished under a
 6133  		// backup that did not is reported with that part's why rather than as the
 6134  		// whole run failed (D-UI-028); the backup still waits on the restore.
 6135  		cloudAddGatedEntry(s, window, cloudConfigured, _("SYNC SAVES WITH THE CLOUD"),
 6136  			cloudLastRunDetail("sync-manual"), [window] {
 6137  			window->pushGui(new GuiMsgBox(window, _("SYNC GAME SAVES BOTH WAYS?\n\nTHE NEWEST COPY OF EACH SAVE IS KEPT ON BOTH SIDES. NOTHING IS DELETED.") + cloudLastRunWhy("sync-manual"), _("YES"),
 6138  				[window] {
 6139  				ThreadedCloudSync::start(window,
 6140  					"/usr/bin/cloud_restore --yes --method=copy --update --saves-only; _r=$?; echo \">>> tier RESTORING SAVES|$_r\"; [ \"$_r\" = 0 ] || exit \"$_r\";"
 6141  					" /usr/bin/cloud_backup --yes --method=copy --update --saves-only; _b=$?; echo \">>> tier BACKING UP SAVES|$_b\"; exit \"$_b\"",
 6142  					_("SYNC SAVES"), _("SYNCING SAVES"), ThreadedCloudSync::Origin::Manual);
 6143  				}, _("NO"), nullptr));
 6144  		});
 6145  		cloudAddClassRow(s, window, cloudConfigured, _("BACK UP SAVES TO THE CLOUD"), "backup", [window] {
 6146  			window->pushGui(new GuiMsgBox(window, _("BACK UP GAME SAVES, SAVE STATES, AND SCREENSHOTS TO THE CLOUD?") + cloudLastRunWhy("backup"), _("YES"),
 6147  				[window] { ThreadedCloudSync::start(window, "/usr/bin/cloud_backup --yes --saves-only", _("BACK UP SAVES"), _("BACKING UP SAVES"), ThreadedCloudSync::Origin::Manual); },
 6148  				_("NO"), nullptr));
 6149  		});
```


## The first reader's grades of the first seat (GPT-6 Astra), for your refutation too

The first seat was given the same packet. The first reader graded its items as below. Where you disagree with a grade, say so with the line. A-33 to A-39 are new findings you have not seen as text; their substance is in the grades.

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
