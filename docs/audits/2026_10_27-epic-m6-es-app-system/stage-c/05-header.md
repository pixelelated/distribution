# Punch list — M6.P2 T33, EmulationStation's system layer (#680)

Written by the first reader (Opus 5.5) at stage C, and rendered by `tools/t33-05.py` from `stage-c/punch-items.py`. Its sources:
- `02` § The leads (L-01 to L-29, and the floor's 41 with their verdicts);
- `04` § Risk assessment;
- the guest cycle, the stage-C fixtures (`stage-c/runs.txt`) and the floor read (`stage-c/floor.md`, a subagent's, labelled);
- the seat's grades (`stage-c/astra-grades.md`).

- **reviewed-at:** `27bd8499f1` (distribution); **reviewed-at-es:** `16dbac5211` (the pin). **fixed-at** and **fixed-at-es** come at stage E.
- **Independent depth:** one seat, GPT-6 Astra at `max` (`second-opinions/review-plan.json`).
- **One item per defect or reusable improvement**, however many leads found it. PL-01 to PL-20 are the first read's, ordered by severity within the bugs proposed, then the recorded; PL-21 to PL-26 are the seat's new items (EP-39 to EP-46), appended.
- **Nothing here changes a file** under the distribution's `packages/`, `projects/` or `tools/`, or an ES file, at stages A to D. A fix lands only under a stream brief on the ES branch, proven twice. A row added, moved or renamed updates `docs/es-menu-map.md` in the same commit (D-UI-039).
- **Lines** are the pin's. "Guest" means the M6 image (M7's composition over the pin). "Fixture" means a stage-C harness that fails at the pin and passes its control.
- **Every disposition is a question** for the stage-D pause (`question:`). **Ruled 20:10 UTC** (#680 comment 6452429909): twenty bugs, #1271 to #1290, filed with their code traces by `tools/t33-file-bugs.py`; **ruled 20:15 UTC** (#680 comment 6452522368): PL-13 and PL-18's 3.5, #1291 and #1292 (`--second`). Each item's **Bug:** line names its issue.
- **The audit issue:** #1270 (a sub-issue of #680), one checkbox per item; `tools/box-check --issue 1270`: 26 open checkboxes, 0 fail.
