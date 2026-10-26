| # | Sentence | ES row (`CloudText.cpp`) | Literal emitters at `a8de42ffbc` | Filled by a variable emitter | Status |
| ---: | --- | --- | --- | --- | --- |
| 1 | `YOUR CLOUD STORAGE ISN'T SET UP YET` | :428 | cloud_backup:940, cloud_content_backup:107, cloud_content_restore:144, cloud_restore:993 | `selection_reason` cloud_connections.py:70 | shared |
| 2 | `CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS` | :429 | -- | `selection_reason` cloud_connections.py:69 | ES row; filled by a variable emitter |
| 3 | `COULDN'T REACH YOUR CLOUD - CHECK YOUR SIGN-IN` | :430 | cloud_backup:979, cloud_restore:1032 | -- | shared |
| 4 | `YOUR CLOUD STOPPED ANSWERING` | :431 | cloud_backup:1044, cloud_restore:1093, cloud_scan:124, cloud_scan:159, cloud_setup:343, cloud_setup:350, cloud_setup:400 | `why_for` cloud_backup:831, cloud_backup:842, cloud_content_backup:280, cloud_content_restore:327, cloud_restore:837, cloud_restore:848 | shared |
| 5 | `YOUR CLOUD SYNC SETTINGS COULDN'T BE READ` | :432 | cloud_backup:1218, cloud_backup:1224, cloud_backup:1308, cloud_backup:1764, cloud_content_backup:98, cloud_content_backup:192, cloud_content_backup:204, cloud_content_restore:135, cloud_content_restore:229, cloud_content_restore:241, cloud_content_restore:258, cloud_restore:1267, cloud_restore:1273, cloud_restore:1357, cloud_restore:1832, cloud_scan:323, cloud_setup:319, cloud_setup:323, cloud_setup:324 | -- | shared |
| 6 | `YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED` | :433 | -- | -- | **ES-only: no producer at the rev** |
| 7 | `YOUR CLOUD FOLDER COULDN'T BE READ` | :434 | cloud_scan:163, cloud_setup:384, cloud_setup:413 | -- | shared |
| 8 | `YOUR CLOUD SETTINGS CHANGED. CHECK AGAIN` | :435 | cloud_scan:222 | -- | shared |
| 9 | `ANOTHER CLOUD CHECK IS RUNNING` | :436 | cloud_scan:361 | -- | shared |
| 10 | `YOUR CLOUD FOLDERS COULDN'T BE CREATED` | :437 | cloud_setup:818, cloud_setup:881 | -- | shared |
| 11 | `CHECK WHAT WOULD CHANGE FIRST` | :438 | cloud_content_restore:908 | -- | shared |
| 12 | `AN OLD FOLDER SETTING IS IN THE WAY` | :439 | cloud_backup:1236, cloud_restore:1285 | -- | shared |
| 13 | `YOUR SAVES FOLDER ISN'T ON THIS DEVICE` | :440 | cloud_backup:1616 | -- | shared |
| 14 | `THIS DEVICE'S SETTINGS BACKUP IS DAMAGED` | :441 | cloud_backup:2196, backuptool:1503, backuptool:1539 | -- | shared |
| 15 | `THE COPY IN YOUR CLOUD ISN'T COMPLETE` | :442 | cloud_backup:2307 | -- | shared |
| 16 | `COULDN'T FIND YOUR CLOUD FOLDER` | :443 | cloud_scan:123 | `why_for` cloud_backup:830, cloud_content_backup:279, cloud_content_restore:326, cloud_restore:836 | shared |
| 17 | `SOME FILES DIDN'T FINISH` | :444 | -- | `why_for` cloud_backup:832, cloud_content_backup:281, cloud_content_restore:328, cloud_restore:838 | ES row; filled by a variable emitter |
| 18 | `YOUR CLOUD WOULDN'T TAKE THE FILES` | :445 | cloud_scan:125 | `why_for` cloud_backup:833, cloud_content_backup:282, cloud_content_restore:329, cloud_restore:839 | shared |
| 19 | `IT WAS STOPPED` | :446 | -- | `why_for` cloud_backup:834, cloud_content_backup:283, cloud_content_restore:330, cloud_restore:840 | ES row; filled by a variable emitter |
| 20 | `THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME` | :447 | -- | `why_for` cloud_backup:840, cloud_restore:846 | ES row; filled by a variable emitter |
| 21 | `SOMETHING WENT WRONG` | :448 | cloud_content_backup:613, cloud_content_restore:896, cloud_scan:126, cloud_scan:132, cloud_scan:327 | `why_for` cloud_backup:844, cloud_content_backup:284, cloud_content_restore:331, cloud_restore:850 | shared |
| 22 | `COULDN'T TELL WHICH CARD YOUR SAVES ARE ON` | :449 | cloud_saves_root:137 | -- | shared |
| 23 | `YOUR SAVES ARE ON A DIFFERENT CARD` | :450 | cloud_saves_root:156 | -- | shared |
| 24 | `YOUR SAVES CHANGED CARDS PART-WAY THROUGH` | :451 | cloud_saves_root:177 | -- | shared |
| 25 | `THERE'S NO SETTINGS BACKUP ON THIS DEVICE YET` | :452 | backuptool:1480 | -- | shared |
| 26 | `COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS` | :453 | backuptool:1533, backuptool:1560, backuptool:1613, backuptool:1629, backuptool:1678 | -- | shared |
| 27 | `THE RESTORE COULDN'T FINISH` | :454 | backuptool:1586, backuptool:1793, backuptool:1796 | -- | shared |
| 28 | `THIS DEVICE CAN'T MAKE A SETTINGS BACKUP` | :455 | backuptool:1835 | -- | shared |
| 29 | `THE BACKUP COULDN'T FINISH WHILE GATHERING YOUR SETTINGS` | :456 | backuptool:1917 | -- | shared |
| 30 | `THE BACKUP COULDN'T FINISH` | :457 | backuptool:1886, backuptool:1923 | -- | shared |
| 31 | `SOMETHING CHANGED SINCE YOU CHECKED` | :462 | cloud_content_backup:732, cloud_content_restore:818, cloud_content_restore:902, cloud_content_restore:978, cloud_content_restore:1510 | -- | shared |
| 32 | `COULDN'T RECORD WHICH CARD YOUR SAVES ARE ON` | :463 | cloud_saves_root:185 | -- | shared |
| 33 | `YOU WENT OFFLINE PART-WAY THROUGH` | :464 | -- | the stamp's why cloud_backup:735, cloud_content_backup:340, cloud_content_restore:395, cloud_restore:736 | ES row; filled by a variable emitter |
| 34 | `THIS DEVICE CAN'T RESTORE SETTINGS` | :465 | backuptool:1468, backuptool:1496 | -- | shared |
| 35 | `A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING` | :466 | backuptool:1473, backuptool:1841 | -- | shared |
| 36 | `THERE'S NOTHING TO BACK UP YET` | :467 | backuptool:1915 | -- | shared |
| 37 | `A SIGN-IN WAS FOUND IN THE BACKUP` | :468 | backuptool:1919 | -- | shared |
| 38 | `YOUR OWN BACKUP LIST NAMES A FOLDER A BACKUP CAN'T CARRY` | :469 | backuptool:1921 | -- | shared |
| 39 | `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` | :473 | backuptool:1556 | -- | shared |
| 40 | `A SYNC IS ALREADY RUNNING` | :474 | cloud_setup:797 | -- | shared |

Counts: es_rows 40 (expected 40), es_unique 40 (expected 40), literal 34 (expected 34), shared_literal 34 (expected 34), script_only 0 (expected 0), es_only_literal 6 (expected 6), variable_lines 17 (expected 17), es_only_unproduced 1 (expected 1), es_dotted 0 (expected 0)
ES rows that differ from their normalized form: none
Variable emitter lines: cloud_backup:973, cloud_backup:1508, cloud_backup:1516, cloud_backup:1690, cloud_backup:2425, cloud_content_backup:815, cloud_content_restore:1004, cloud_content_restore:1027, cloud_content_restore:1075, cloud_content_restore:1457, cloud_content_restore:1582, cloud_restore:1026, cloud_restore:1530, cloud_restore:1538, cloud_restore:2225, cloud_scan:143, cloud_scan:157
ES-only with no producer: `YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED`
Pairs whose two spellings differ: none

**The fallback map** (`ThreadedCloudSync::whyForCode` at the pin; `why_for` in the scripts; the header comment `ThreadedCloudSync.h:93-99`; `es-player-text.md` § Outcome vocabulary's **Why** sentence):

| Code | Code says (`ThreadedCloudSync.cpp`) | Scripts' `why_for` | Header comment | Rule |
| --- | --- | --- | --- | --- |
| 3 4 | `COULDN'T FIND YOUR CLOUD FOLDER` (:85) | `COULDN'T FIND YOUR CLOUD FOLDER` | **differs** (names something else) | **differs**: says `YOUR CLOUD FOLDER WASN'T FOUND` (#909) |
| 5 124 | `YOUR CLOUD STOPPED ANSWERING` (:86) | `YOUR CLOUD STOPPED ANSWERING` | **differs** (names something else) | same |
| 6 | `SOMETHING WENT WRONG` (:95, the default arm) | `SOME FILES DIDN'T FINISH` | **differs** (names something else) | same |
| 7 8 | `YOUR CLOUD WOULDN'T TAKE THE FILES` (:87) | `YOUR CLOUD WOULDN'T TAKE THE FILES` | **differs** (names something else) | **absent** (#909) |
| 10 | `SOMETHING WENT WRONG` (:95, the default arm) | `THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME` | **differs** (names something else) | same |
| Stopped | `IT WAS STOPPED` (:88) | `IT WAS STOPPED` | **differs** (names something else) | same |
| default | `SOMETHING WENT WRONG` (:95) | `SOMETHING WENT WRONG` | **differs** (names something else) | same |

Groups where the code and the scripts differ: 2 (expected 2: codes 6 and 10, A-15)

**Exit 75's wordings** (every string the eight and the scripts give a held lock):

| Wording | Where |
| --- | --- |
| `SKIPPED - ANOTHER CLOUD CHECK IS RUNNING` | CloudText.cpp:410 |
| `SKIPPED - A SYNC IS ALREADY RUNNING` | CloudText.cpp:411 |
| `ANOTHER CLOUD CHECK IS RUNNING` | CloudText.cpp:436 |
| `A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING` | CloudText.cpp:466 |
| `A SYNC IS ALREADY RUNNING` | CloudText.cpp:474 |
| `WAIT FOR THE CURRENT CLOUD TASK TO FINISH, THEN TRY AGAIN.` | CloudText.cpp:1396 |
| `A SYNC IS ALREADY RUNNING` | ThreadedCloudSync.cpp:93 |
| `SKIPPED - A SYNC IS ALREADY RUNNING` | ThreadedCloudSync.cpp:538 |
| `A SYNC IS ALREADY RUNNING.` | ThreadedCloudSync.cpp:783 |
| `ANOTHER CLOUD CHECK IS RUNNING` | cloud_scan:361 (a script's `>>> why`) |
| `A SYNC IS ALREADY RUNNING` | cloud_setup:797 (a script's `>>> why`) |
| `A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING` | backuptool:1473, backuptool:1841 (a script's `>>> why`) |

Distinct wordings: 7 (expected 7: cloud_setup says A SYNC IS ALREADY RUNNING since T17's S6)
