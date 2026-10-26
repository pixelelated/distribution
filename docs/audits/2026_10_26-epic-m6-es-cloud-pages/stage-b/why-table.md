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
