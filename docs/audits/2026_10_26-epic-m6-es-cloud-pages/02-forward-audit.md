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
- **The card reads with `fgets` into 512 bytes** (`ThreadedCloudSync.cpp:211-212`); the job reads a character at a time with a 1,024-byte cap (`CloudTransferJob.cpp:656-677`). A card line over 511 bytes arrives as two, and either half can be misread: a fragment that begins with `>>> ` is classified as one (F-04; Astra's A-4 corrected the first wording).
- **`doing copy`, `verify` and `remove` have no producer** (the folder move, #353, retired by D-CLOUD-175). The job's allowlist (`CloudTransferJob.cpp:387-389`) and the page's three strings (`GuiCloudTransfer.cpp:1027-1032`) remain (F-16).

## The why table

Generated by `tools/t18-why-table.py` at 09:55:29 UTC and regenerated at 10:51:35 UTC after Astra's A-15 added codes 6 and 10 to the fallback map (exit 0 both times; output `stage-b/why-table.md`). The packet the seats read carries the first version. It asserts eight counts: 38 ES rows, 38 unique, 34 literal script sentences, 32 shared, 2 script-only, 6 ES-only against the literals, 17 variable emitter lines, and 1 ES row with no producer after expansion. It also asserts the eight wordings exit 75 is given. The variable emitters are expanded through each script's `why_for`, the connection layer's `selection_reason` and the stamps' offline why. Against `651150fc88` it exits 1 and names seven counts (P9).

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
| 6 | `SOMETHING WENT WRONG` (:94, the default arm) | `SOME FILES DIDN'T FINISH` | same | same |
| 7 8 | `YOUR CLOUD WOULDN'T TAKE THE FILES` (:86) | `YOUR CLOUD WOULDN'T TAKE THE FILES` | **differs** (names something else) | **absent** (#909) |
| 10 | `SOMETHING WENT WRONG` (:94, the default arm) | `THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME` | same | same |
| Stopped | `IT WAS STOPPED` (:87) | `IT WAS STOPPED` | same | same |
| default | `SOMETHING WENT WRONG` (:94) | `SOMETHING WENT WRONG` | same | same |

Groups where the code and the scripts differ: 2 (expected 2: codes 6 and 10, A-15)

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
- **The fallback map** (the brief's "six words"; seven code groups since A-15). The code and the scripts' `why_for` agree on five groups. For codes **6** and **10**, `whyForCode` has no arm and falls to `SOMETHING WENT WRONG`, where the scripts say `SOME FILES DIDN'T FINISH` and, on an automatic run, `THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME`. The first version compared only the groups it listed (Astra's A-15). The header comment above it (`ThreadedCloudSync.h:93-99`) names two groups in older words and sits above `writeStamp` rather than `whyForCode`, so it is **this slice's drift** (F-13). The rule's sentence (es-player-text.md § Outcome vocabulary) says `YOUR CLOUD FOLDER WASN'T FOUND` and `YOUR CLOUD REFUSED THE TRANSFER` and claims the six are "duplicated verbatim in ThreadedCloudSync's own fallback map"; that half is **#909's** (F-14).

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
- **The fit at 640x480** of every `outcomeCandidates` list (the card's outcome line, `ThreadedCloudSync.cpp:700`), every `actionCandidates` list (`:649`, `:691`), the card's live-line candidates (`:409-425`, `:281-285`), the scan sentence's `chooseThatFits` (`GuiCloudTransfer.cpp:1020-1023`) and the page's `fitOneLine`/`fitSentences` rows are proved only by a frame: the host has no font. **Owed to the window** (§ The guest cycle). The page sizes every row `(w, 0)` (`:73-74`). Most rows go through `fitOneLine`, but the title (`:56`), the running counter (`:936-939`), the finished footer (`:913-915`) and most `doing` lines (`:1035`) do not, and those grow rather than clip. The padded-width trap (es-code-traps.md) applies to them; their fit is owed per row. The first wording of this sentence claimed every row was fitted, and Astra's A-40 refuted it.
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

## The streams

Under `docs/reviews/briefs/t18-streams.md` at `1b6588efd8` (the coordinator's, at the stage-D ruling, 11:16 UTC), serial, one commit each on the ES branch `feature/m6-es-cloud-pages-665`. The pin in `package.mk` is not moved. Every stream: its case written first and seen to FAIL on the pin's code, then the fix; `es-unit-tests` and `jobs-tests` built and run before its commit; the host `g++ -fsyntax-only` on each edited `.cpp`, or its `CANNOT` with the missing header named; the non-ASCII comment grep clean.

| Stream | Bug | Before | Commit (ES) | After | Already written | proved |
| --- | --- | --- | --- | --- | --- | --- |
| S1 the why table and the comments (PL-03, PL-08) | #1147 | `stage-e/s1-before.txt`: the two new rows and the round-trip FAIL on the pin's `CloudText.cpp`, 3 checks (`THIS BACKUP HOLDS FILES ...`, `A SYNC IS ALREADY RUNNING`, and `CHOOSE A CONNECTION ...` failing its own round-trip) | `1a1828a8b` | `stage-e/s1-after.txt`: `es-unit-tests` 187 cases PASS, `jobs-tests` 6 PASS. The syntax check: PASS for `CloudText.cpp`; `CANNOT` for `ThreadedCloudSync.cpp` and `CloudTransferJob.cpp` (`SDL_joystick.h`), the latter compiled by `jobs-tests` against its doubles. `es-untranslated` 0 in the eight. `t18-why-table.py`, normalized and re-pinned, exits 0 on the fix (40 rows, 0 script-only, 0 rows differing from their normalized form) and 1 on the pin | nothing persisted: the table is read at run time; a device with the old binary shows the English until the pin moves | fix-unit-test |
| S2 the stamp writer (PL-01) | #1145 | `stage-e/s2-before.txt`: `tools/t18-stamp-fixture.py` runs the shipped writer from the pin's file. Full disk: the previous stamp REPLACED by 0 bytes, nothing reported. Stale temporary: the stamp is the stale file. The new guard case in `AtomicFileTests.cpp` FAILs (no bool writer) | `f63ad4de4` | `stage-e/s2-after.txt`: on the fixed file, full disk keeps the stamp and the writer reports false, and a stale temporary is left alone; the pin's file still fails. `es-file-tests` 25 PASS (the guard), `es-unit-tests` 187, `jobs-tests` 6. `ThreadedCloudSync.cpp`'s syntax check `CANNOT` (`SDL_joystick.h`), while the fixture compiled the fixed writer against the real `AtomicFileUtil.cpp`. The three doubles in `tests/app-unit` return bool; `proxycards-tests` is not built here | stamps on devices are read as they are; one the old code emptied reads NOT DONE ON THIS DEVICE YET until the next run rewrites it; nothing migrated | fixture, fix-unit-test |

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
