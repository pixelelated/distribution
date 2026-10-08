# frame-diff

baseline `/workspace/tmp/pixelelated-m7-walk527-04/baseline-subset` (build d72084ccad) against `/workspace/tmp/pixelelated-m7-walk527-04/artifacts/rocknix-images/qa-7f58b7b1c5-webdav-d-20261008-2012/walks`: 8 screens in 1 s.
masks: /workspace/repos/rocknix.worktrees/m7-p5-cloud-folder-walks/tools/vm-walks/masks.txt (7); claims: /workspace/repos/rocknix.worktrees/m7-p5-cloud-folder-walks/tools/vm-walks/claims.txt (39 live, 0 stale against another baseline).

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
| `to-change-cloud-folder/01-cloud-hub.png` | x 1249..1279, y 418..707 | 4508 px | claimed by 527 # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455 |
| `to-change-cloud-folder/02-hub-change-folder-row.png` | x 240..1039, y 187..607 | 148643 px | claimed by 527 # CHECK CLOUD FOLDERS adds a row; focused hub scrolls one row upward (#508) |
| `to-change-cloud-folder/02-hub-change-folder-row.png` | x 1249..1279, y 418..707 | 4508 px | claimed by 527 # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455 |
| `to-change-cloud-folder/03-folder-editor.png` | x 552..728, y 146..191 | 2566 px | claimed by 527 # SAVES FOLDER title and underlying CLOUD FOLDERS title replace CLOUD FOLDER/CLOUD |
| `to-change-cloud-folder/03-folder-editor.png` | x 183..413, y 226..267 | 4583 px | claimed by 409 # the same lowercase default on the other editor walk, #415 |
| `to-change-cloud-folder/03-folder-editor.png` | x 1249..1279, y 418..707 | 4508 px | claimed by 527 # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455 |
| `to-change-cloud-folder/03-folder-editor.png` | x 236..1043, y 644..718 | 60562 px | claimed by 527 # shorter selector behind the keyboard replaces the old hub and its exposed BACK strip |

**PASS** -- 20 box(es) claimed, 0 unclaimed, 0 screen(s) missing.
