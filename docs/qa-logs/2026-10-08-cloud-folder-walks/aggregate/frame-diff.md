# frame-diff

baseline `/workspace/artifacts/rocknix-images/walk-baseline` (build d72084ccad) against `/workspace/repos/rocknix.worktrees/conflict-resolution/docs/qa-logs/2026-10-08-cloud-folder-walks/aggregate/walks`: 78 screens in 2 s.
masks: tools/vm-walks/masks.txt (7); claims: tools/vm-walks/claims.txt (39 live, 0 stale against another baseline).

| screen | box | pixels | verdict |
| --- | --- | --- | --- |
| `confirm-cloud-folder/01-cloud-hub.png` | x 1249..1279, y 418..707 | 4508 px | claimed by 527 # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455 |
| `confirm-cloud-folder/02-hub-change-folder-row.png` | x 240..1039, y 187..607 | 148643 px | claimed by 527 # CHECK CLOUD FOLDERS adds a row; focused hub scrolls one row upward (#508) |
| `confirm-cloud-folder/02-hub-change-folder-row.png` | x 1249..1279, y 418..707 | 4508 px | claimed by 527 # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455 |
| `confirm-cloud-folder/03-folder-editor.png` | x 552..728, y 146..191 | 2566 px | claimed by 527 # SAVES FOLDER title and underlying CLOUD FOLDERS title replace CLOUD FOLDER/CLOUD |
| `confirm-cloud-folder/03-folder-editor.png` | x 183..413, y 226..267 | 4583 px | claimed by 409 # the editor now holds /pixelelated/Saves (D-CLOUD-174); measured lowercase text against the accepted ROCKNIX baseline, #415 |
| `confirm-cloud-folder/03-folder-editor.png` | x 1249..1279, y 418..707 | 4508 px | claimed by 527 # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455 |
| `confirm-cloud-folder/03-folder-editor.png` | x 236..1043, y 644..718 | 60562 px | claimed by 527 # shorter selector behind the keyboard replaces the old hub and its exposed BACK strip |
| `confirm-cloud-folder/04-folder-result.png` | x 552..728, y 146..162 | 1877 px | claimed by 527 # CLOUD FOLDERS after unchanged submission, rather than old CLOUD hub |
| `confirm-cloud-folder/04-folder-result.png` | x 236..1043, y 199..718 | 264366 px | claimed by 527 # three independent path rows and selector height replace the former hub return |
| `confirm-cloud-folder/04-folder-result.png` | x 1249..1279, y 418..707 | 4508 px | claimed by 527 # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455 |
| `confirm-cloud-folder/05-after-dismiss.png` | x 137..1142, y 116..718 | 499432 px | claimed by 527 # B now returns to the hub instead of old A reopening the keyboard; exact surfaces reviewed |
| `confirm-cloud-folder/05-after-dismiss.png` | x 1249..1279, y 418..707 | 4508 px | claimed by 527 # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455 |
| `confirm-cloud-folder/05-after-dismiss.png` | x 274..1005, y 743..765 | 7139 px | claimed by 527 # hub CLOSE/BACK/CHOOSE help replaces keyboard editing prompts |
| `continue-to-systems/05-systems-page.png` | x 250..540, y 475..521 | 3693 px | claimed by 308 # PICO-8 listed, 1 FILE NOT YET IN YOUR CLOUD: a system whose only file is empty (the 0-byte Splore.png) was read as nothing to move and left out (ES 52ba93160, 8a gpt); the rows below it shift down |
| `continue-to-systems/05-systems-page.png` | x 236..1043, y 545..676 | 69385 px | claimed by 308 # PICO-8 listed, 1 FILE NOT YET IN YOUR CLOUD: a system whose only file is empty (the 0-byte Splore.png) was read as nothing to move and left out (ES 52ba93160, 8a gpt); the rows below it shift down |
| `manager-fbn/01-0-carousel.png` | x 1249..1279, y 418..707 | 4579 px | claimed by 455 # narrow restored GB panel at the right edge |
| `manager-gb/01-0-carousel.png` | x 0..1279, y 0..707 | 814636 px | claimed by 455 # first verified Game Boy carousel, previously FBNeo |
| `manager-gb/02-1-list.png` | x 465..814, y 74..134 | 13701 px | claimed by 455 # first verified Game Boy game list |
| `manager-gb/02-1-list.png` | x 544..720, y 224..246 | 2299 px | claimed by 455 # first verified Game Boy game list |
| `manager-gb/03-2-game-options.png` | x 940..1089, y 25..41 | 1677 px | claimed by 455 # options for Ninoid, previously Ms. Pac-Man |
| `manager-gb/03-2-game-options.png` | x 465..746, y 74..134 | 11059 px | claimed by 455 # options for Ninoid, previously Ms. Pac-Man |
| `manager-gb/03-2-game-options.png` | x 544..720, y 224..246 | 2290 px | claimed by 455 # options for Ninoid, previously Ms. Pac-Man |
| `manager-gb/04-3-manager.png` | x 465..814, y 74..134 | 13620 px | claimed by 455 # actual Game Boy background and Ninoid title |
| `manager-gb/04-3-manager.png` | x 544..720, y 224..246 | 2290 px | claimed by 455 # actual Game Boy background and Ninoid title |
| `manager-gb/04-3-manager.png` | x 273..496, y 432..636 | 37455 px | claimed by 455 # unrotated Game Boy thumbnail and its date |
| `manager-gb/05-4-manager-next-tile.png` | x 465..814, y 74..134 | 13620 px | claimed by 455 # same actual system/game backdrop |
| `manager-gb/05-4-manager-next-tile.png` | x 544..720, y 224..246 | 2290 px | claimed by 455 # same actual system/game backdrop |
| `manager-gb/05-4-manager-next-tile.png` | x 273..496, y 432..636 | 37473 px | claimed by 455 # same Game Boy thumbnail, selected |
| `manager-nes/01-0-carousel.png` | x 737..1279, y 0..707 | 338149 px | claimed by 455 # restored GB neighbor and shifted next panel |
| `restore-page/02-restore-page.png` | x 250..680, y 464..515 | 6251 px | claimed by 349 # SETTINGS dimmed, its line NO SETTINGS BACKUP FROM THIS DEVICE YET and no switch: the QA cloud holds no settings backup from this device's label, so the scan offers none (D-CLOUD-162, D-CLOUD-164 string 3); since ES 551c5a762 the row keeps the rows' inset, where 1acdaf2cce..d9493fe339 drew it flush with the panel's edge |
| `restore-page/02-restore-page.png` | x 971..1029, y 474..503 | 779 px | claimed by 349 # SETTINGS dimmed, its line NO SETTINGS BACKUP FROM THIS DEVICE YET and no switch: the QA cloud holds no settings backup from this device's label, so the scan offers none (D-CLOUD-162, D-CLOUD-164 string 3); since ES 551c5a762 the row keeps the rows' inset, where 1acdaf2cce..d9493fe339 drew it flush with the panel's edge |
| `run-transfer-frames/05-systems-page.png` | x 250..540, y 475..521 | 3693 px | claimed by 308 # the same page on the frames walk |
| `run-transfer-frames/05-systems-page.png` | x 236..1043, y 545..676 | 69385 px | claimed by 308 # the same page on the frames walk |
| `run-transfer-frames/06-selected-all.png` | x 250..540, y 475..521 | 3693 px | claimed by 308 # the same page, all selected |
| `run-transfer-frames/06-selected-all.png` | x 236..1043, y 545..676 | 74761 px | claimed by 308 # the same page, all selected |
| `run-transfer-frames/07-t02.png` | x 684..694, y 325..338 | 116 px | claimed by 308 # ITEM 1 OF 5: the PICO-8 unit counted (same change) |
| `run-transfer-frames/07-t02.png` | x 424..854, y 560..573 | 3893 px | claimed by 308 # the same footer, the frames walk |
| `run-transfer-frames/08-t05.png` | x 565..714, y 288..338 | 2663 px | claimed by 308 # the run carries PICO-8's files too (26 files, 1.1 MB against 23, 640 KB) and still ends at ELAPSED 0:03 (t08: COMPLETED); the t05 sample can catch ITEM 5 OF 5 a moment before the end |
| `run-transfer-frames/08-t05.png` | x 499..782, y 560..573 | 2864 px | claimed by 308 # the same sample: the footer still THIS CAN TAKE A WHILE. |
| `run-transfer-frames/08-t05.png` | x 588..691, y 743..765 | 1210 px | claimed by 308 # the same sample: the help bar still CANCEL |
| `run-transfer/07-transfer-running.png` | x 424..854, y 560..573 | 3893 px | claimed by 308 # the transfer page's footer no longer names a console letter: THIS CAN TAKE A WHILE. (ES 5a7afc4ca, F-RA-14/F-CS-07; es-ui-style-guide Interaction rules) |
| `to-change-cloud-folder/01-cloud-hub.png` | x 1249..1279, y 418..707 | 4508 px | claimed by 527 # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455 |
| `to-change-cloud-folder/02-hub-change-folder-row.png` | x 240..1039, y 187..607 | 148643 px | claimed by 527 # CHECK CLOUD FOLDERS adds a row; focused hub scrolls one row upward (#508) |
| `to-change-cloud-folder/02-hub-change-folder-row.png` | x 1249..1279, y 418..707 | 4508 px | claimed by 527 # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455 |
| `to-change-cloud-folder/03-folder-editor.png` | x 552..728, y 146..191 | 2566 px | claimed by 527 # SAVES FOLDER title and underlying CLOUD FOLDERS title replace CLOUD FOLDER/CLOUD |
| `to-change-cloud-folder/03-folder-editor.png` | x 183..413, y 226..267 | 4583 px | claimed by 409 # the same lowercase default on the other editor walk, #415 |
| `to-change-cloud-folder/03-folder-editor.png` | x 1249..1279, y 418..707 | 4508 px | claimed by 527 # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455 |
| `to-change-cloud-folder/03-folder-editor.png` | x 236..1043, y 644..718 | 60562 px | claimed by 527 # shorter selector behind the keyboard replaces the old hub and its exposed BACK strip |

**PASS** -- 48 box(es) claimed, 0 unclaimed, 0 screen(s) missing.
