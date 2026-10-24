# frame-diff

baseline `/workspace/artifacts/rocknix-images/walk-baseline` (build d72084ccad) against `/workspace/artifacts/rocknix-images/qa-069fc27044-webdav-a-20261024-221602/walks`: 78 screens of 16 walk(s) compared in 9 s.
masks: tools/vm-walks/masks.txt (10); claims: tools/vm-walks/claims.txt (43 live, 0 stale against another baseline, 348 inert proposal(s)).

| screen | box | pixels | verdict |
| --- | --- | --- | --- |
| `back-up-page/01-cloud-hub.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `back-up-page/02-back-up-page.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `confirm-cloud-folder/01-cloud-hub.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `confirm-cloud-folder/02-hub-change-folder-row.png` | x 240..1039, y 187..639 | 133719 px | claimed by 544 # #527 CHECK CLOUD FOLDERS/scrolling plus #537 CLOUD CONNECTIONS row and shorter subtitle; exact image19/baseline/prior-hub frames reviewed |
| `confirm-cloud-folder/02-hub-change-folder-row.png` | x 240..1039, y 545..574 | 23990 px | claimed by 308 # CHANGE CLOUD FOLDER's line is YOUR SAVES ARE IN: <folder> -- one line under the row (ES 39d5a9d6d, 8-es claude F-ES-14, D-UI-023) |
| `confirm-cloud-folder/02-hub-change-folder-row.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `confirm-cloud-folder/03-folder-editor.png` | x 552..728, y 146..191 | 2566 px | claimed by 527 # SAVES FOLDER title and underlying CLOUD FOLDERS title replace CLOUD FOLDER/CLOUD |
| `confirm-cloud-folder/03-folder-editor.png` | x 183..413, y 226..267 | 4583 px | claimed by 409 # the editor now holds /pixelelated/Saves (D-CLOUD-174); measured lowercase text against the accepted ROCKNIX baseline, #415 |
| `confirm-cloud-folder/03-folder-editor.png` | x 856..934, y 584..602 | 1171 px | claimed by 544 # #538 CLEAR button replaces RESET; callback unchanged |
| `confirm-cloud-folder/03-folder-editor.png` | x 236..1043, y 644..718 | 60562 px | claimed by 527 # shorter selector behind the keyboard replaces the old hub and its exposed BACK strip |
| `confirm-cloud-folder/03-folder-editor.png` | x 273..1007, y 743..765 | 6397 px | claimed by 544 # #538 CLEAR help caption replaces RESET and re-centers the same prompts |
| `confirm-cloud-folder/03-folder-editor.png` | x 0..551, y 0..707 | 152955 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `confirm-cloud-folder/04-folder-result.png` | x 552..728, y 146..162 | 1877 px | claimed by 527 # CLOUD FOLDERS after unchanged submission, rather than old CLOUD hub |
| `confirm-cloud-folder/04-folder-result.png` | x 236..1043, y 199..718 | 240366 px | claimed by 527 # three independent path rows and selector height replace the former hub return |
| `confirm-cloud-folder/04-folder-result.png` | x 240..1039, y 545..574 | 24000 px | claimed by 308 # the same row's line on the hub reopened after the folder change (ES 39d5a9d6d); the reopened hub sits on CHANGE CLOUD FOLDER again (ES 4313a8f53, G-E2-O1) so nothing else on the frame differs |
| `confirm-cloud-folder/04-folder-result.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `confirm-cloud-folder/05-after-dismiss.png` | x 137..1142, y 116..718 | 499138 px | claimed by 527 # B now returns to the hub instead of old A reopening the keyboard; exact surfaces reviewed |
| `confirm-cloud-folder/05-after-dismiss.png` | x 183..415, y 226..267 | 9780 px | claimed by 409 # the same lowercase default after reopening the editor, #415 |
| `confirm-cloud-folder/05-after-dismiss.png` | x 274..1005, y 743..765 | 7139 px | claimed by 527 # hub CLOSE/BACK/CHOOSE help replaces keyboard editing prompts |
| `confirm-cloud-folder/05-after-dismiss.png` | x 0..551, y 0..707 | 142737 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `continue-to-systems/01-cloud-hub.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `continue-to-systems/02-back-up-page.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `continue-to-systems/03-roms-flipped.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `continue-to-systems/04-continue-focused.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `continue-to-systems/05-systems-page.png` | x 230..1043, y 470..679 | 74908 px | claimed by 308 # PICO-8 listed, 1 FILE NOT YET IN YOUR CLOUD: a system whose only file is empty (the 0-byte Splore.png) was read as nothing to move and left out (ES 52ba93160, 8a gpt); the rows below it shift down |
| `continue-to-systems/05-systems-page.png` | x 0..551, y 0..707 | 206777 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `manager-fbn/01-0-carousel.png` | x 1249..1279, y 418..707 | 4579 px | claimed by 455 # narrow restored GB panel at the right edge |
| `manager-fbn/01-0-carousel.png` | x 0..551, y 0..707 | 355159 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `manager-gb/01-0-carousel.png` | x 0..1279, y 0..707 | 814636 px | claimed by 455 # first verified Game Boy carousel, previously FBNeo |
| `manager-gb/02-1-list.png` | x 465..814, y 74..246 | 16000 px | claimed by 455 # first verified Game Boy game list |
| `manager-gb/03-2-game-options.png` | x 465..1089, y 25..246 | 15026 px | claimed by 455 # options for Ninoid, previously Ms. Pac-Man |
| `manager-gb/04-3-manager.png` | x 465..814, y 74..246 | 15910 px | claimed by 455 # actual Game Boy background and Ninoid title |
| `manager-gb/04-3-manager.png` | x 273..496, y 432..636 | 37455 px | claimed by 455 # unrotated Game Boy thumbnail and its date |
| `manager-gb/05-4-manager-next-tile.png` | x 465..814, y 74..246 | 15910 px | claimed by 455 # same actual system/game backdrop |
| `manager-gb/05-4-manager-next-tile.png` | x 273..496, y 432..636 | 37473 px | claimed by 455 # same Game Boy thumbnail, selected |
| `manager-nes/01-0-carousel.png` | x 737..1279, y 0..707 | 338149 px | claimed by 455 # restored GB neighbor and shifted next panel |
| `manager-nes/01-0-carousel.png` | x 0..39, y 0..381 | 7868 px | **UNCLAIMED** (claim as `0 0 40 382`) |
| `match-dialog/01-cloud-hub.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `match-dialog/02-cloud-hub-match-row.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `match-dialog/03-match-confirm.png` | x 0..551, y 0..707 | 142280 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `match-dialog/04-match-done.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `restore-page/01-cloud-hub.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `restore-page/02-restore-page.png` | x 250..1029, y 464..515 | 7030 px | claimed by 349 # SETTINGS dimmed, its line NO SETTINGS BACKUP FROM THIS DEVICE YET and no switch: the QA cloud holds no settings backup from this device's label, so the scan offers none (D-CLOUD-162, D-CLOUD-164 string 3); since ES 551c5a762 the row keeps the rows' inset, where 1acdaf2cce..d9493fe339 drew it flush with the panel's edge |
| `restore-page/02-restore-page.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/01-cloud-hub.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/02-back-up-page.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/03-roms-flipped.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/04-continue-focused.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/05-systems-page.png` | x 230..1043, y 470..679 | 74908 px | claimed by 308 # the same page on the frames walk |
| `run-transfer-frames/05-systems-page.png` | x 0..551, y 0..707 | 206777 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/06-selected-all.png` | x 230..1043, y 470..679 | 80284 px | claimed by 308 # the same page, all selected |
| `run-transfer-frames/06-selected-all.png` | x 0..551, y 0..707 | 206777 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/07-t02.png` | x 557..722, y 288..338 | 2601 px | claimed by 439 # first observed transfer frame may still say PREPARING... instead of SAVES / ITEM 1 OF 4; actual09 completes24files/640KB at elapsed0:04. The historical t02 name is not a two-second timing assertion; no baseline or general mask changed. |
| `run-transfer-frames/07-t02.png` | x 670..694, y 325..338 | 177 px | claimed by 308 # ITEM 1 OF 5: the PICO-8 unit counted (same change) |
| `run-transfer-frames/07-t02.png` | x 424..854, y 560..573 | 3893 px | claimed by 308 # the same footer, the frames walk |
| `run-transfer-frames/07-t02.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/08-t05.png` | x 565..714, y 288..338 | 2678 px | claimed by 308 # the run carries PICO-8's files too (26 files, 1.1 MB against 23, 640 KB) and still ends at ELAPSED 0:03 (t08: COMPLETED); the t05 sample can catch ITEM 5 OF 5 a moment before the end |
| `run-transfer-frames/08-t05.png` | x 499..782, y 560..573 | 2864 px | claimed by 308 # the same sample: the footer still THIS CAN TAKE A WHILE. |
| `run-transfer-frames/08-t05.png` | x 588..691, y 743..765 | 1210 px | claimed by 308 # the same sample: the help bar still CANCEL |
| `run-transfer-frames/08-t05.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/09-t08.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/10-t11.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/11-t14.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/12-t17.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/13-t20.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/14-t23.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/15-t26.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/16-t29.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/17-t32.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/18-t36.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/19-t40.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/20-t45.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/21-t50.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer-frames/22-t60.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer/01-cloud-hub.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer/02-back-up-page.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer/03-roms-flipped.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer/04-continue-focused.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer/05-systems-page.png` | x 0..551, y 0..707 | 226071 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer/06-selected-all.png` | x 0..551, y 0..707 | 226071 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer/07-transfer-running.png` | x 424..854, y 560..573 | 3893 px | claimed by 308 # the transfer page's footer no longer names a console letter: THIS CAN TAKE A WHILE. (ES 5a7afc4ca, F-RA-14/F-CS-07; es-ui-style-guide Interaction rules) |
| `run-transfer/07-transfer-running.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `run-transfer/08-transfer-done.png` | x 0..551, y 0..707 | 171132 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `tick-game-content/01-cloud-hub.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `tick-game-content/02-back-up-page.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `tick-game-content/03-game-content-flipped.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `tick-roms/01-cloud-hub.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `tick-roms/02-back-up-page.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `tick-roms/03-roms-flipped.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `tick-settings/01-cloud-hub.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `tick-settings/02-back-up-page.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `tick-settings/03-settings-flipped.png` | x 0..551, y 0..707 | 228838 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `to-change-cloud-folder/01-cloud-hub.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `to-change-cloud-folder/02-hub-change-folder-row.png` | x 240..1039, y 187..639 | 133719 px | claimed by 544 # #527 CHECK CLOUD FOLDERS/scrolling plus #537 CLOUD CONNECTIONS row and shorter subtitle; exact image19/baseline/prior-hub frames reviewed |
| `to-change-cloud-folder/02-hub-change-folder-row.png` | x 240..1039, y 545..574 | 23990 px | claimed by 308 # the same row on the other walk |
| `to-change-cloud-folder/02-hub-change-folder-row.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `to-change-cloud-folder/03-folder-editor.png` | x 552..728, y 146..191 | 2566 px | claimed by 527 # SAVES FOLDER title and underlying CLOUD FOLDERS title replace CLOUD FOLDER/CLOUD |
| `to-change-cloud-folder/03-folder-editor.png` | x 183..413, y 226..267 | 4583 px | claimed by 409 # the same lowercase default on the other editor walk, #415 |
| `to-change-cloud-folder/03-folder-editor.png` | x 856..934, y 584..602 | 1171 px | claimed by 544 # #538 CLEAR button replaces RESET; callback unchanged |
| `to-change-cloud-folder/03-folder-editor.png` | x 236..1043, y 644..718 | 60562 px | claimed by 527 # shorter selector behind the keyboard replaces the old hub and its exposed BACK strip |
| `to-change-cloud-folder/03-folder-editor.png` | x 273..1007, y 743..765 | 6397 px | claimed by 544 # #538 CLEAR help caption replaces RESET and re-centers the same prompts |
| `to-change-cloud-folder/03-folder-editor.png` | x 0..551, y 0..707 | 152955 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `to-manage-cloud-storage/01-cloud-hub.png` | x 0..551, y 0..707 | 201035 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `ui-settings-toggle/01-ui-settings-last-row.png` | x 0..551, y 0..707 | 201042 px | **UNCLAIMED** (claim as `0 0 552 708`) |
| `ui-settings-toggle/02-toggled.png` | x 0..551, y 0..707 | 201042 px | **UNCLAIMED** (claim as `0 0 552 708`) |

**FAIL** -- 40 box(es) claimed, 65 unclaimed, 0 screen(s) missing.
- 348 inert proposal claim(s), lines 95..570: not applied until the `proposal:` marker is removed.
