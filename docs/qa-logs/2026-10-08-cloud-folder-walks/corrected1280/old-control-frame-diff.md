# frame-diff

baseline `/workspace/tmp/pixelelated-m7-walk527-04/baseline-subset` (build d72084ccad) against `/workspace/repos/rocknix.worktrees/conflict-resolution/docs/qa-logs/2026-10-08-cloud-folder-walks/original-control`: 8 screens in 1 s.
masks: /workspace/repos/rocknix.worktrees/m7-p5-cloud-folder-walks/tools/vm-walks/masks.txt (7); claims: /workspace/repos/rocknix.worktrees/m7-p5-cloud-folder-walks/tools/vm-walks/claims.txt (39 live, 0 stale against another baseline).

| screen | box | pixels | verdict |
| --- | --- | --- | --- |
| `confirm-cloud-folder/02-hub-change-folder-row.png` | x 240..1039, y 187..607 | 148643 px | claimed by 527 # CHECK CLOUD FOLDERS adds a row; focused hub scrolls one row upward (#508) |
| `confirm-cloud-folder/03-folder-editor.png` | x 137..1142, y 116..718 | 522061 px | **UNCLAIMED** (claim as `137 116 1143 719`) |
| `confirm-cloud-folder/03-folder-editor.png` | x 274..1005, y 743..765 | 7139 px | **UNCLAIMED** (claim as `274 743 1006 766`) |
| `confirm-cloud-folder/04-folder-result.png` | x 0..1279, y 0..799 | 1018630 px | **UNCLAIMED** (claim as `0 0 1280 800`) |
| `confirm-cloud-folder/05-after-dismiss.png` | x 0..1279, y 0..799 | 1018397 px | **UNCLAIMED** (claim as `0 0 1280 800`) |
| `to-change-cloud-folder/02-hub-change-folder-row.png` | x 240..1039, y 187..607 | 148643 px | claimed by 527 # CHECK CLOUD FOLDERS adds a row; focused hub scrolls one row upward (#508) |
| `to-change-cloud-folder/03-folder-editor.png` | x 137..1142, y 116..718 | 522061 px | **UNCLAIMED** (claim as `137 116 1143 719`) |
| `to-change-cloud-folder/03-folder-editor.png` | x 274..1005, y 743..765 | 7139 px | **UNCLAIMED** (claim as `274 743 1006 766`) |

**FAIL** -- 2 box(es) claimed, 6 unclaimed, 0 screen(s) missing.
