# T39 (#686) stage A: the first commands' inputs and outputs

Moved in at the stage-B completion (the coordinator's correction on #686,
issuecomment-6565986529) from the lane's scratch `/workspace/tmp/m6-t39/tmp/` and
`.qa-scratch/t39/`, as they were written on 2026-11-01 06:24-06:29 UTC. Nothing
here is a copy of the 254: the blocks' outputs are inventory rows and counts.
`00-running-log.md` § stage A and `01-research-notes.md` § Scope quote them.

| File | What it is |
| --- | --- |
| `block.sh`, `membership.py` | § 2's membership block, extracted from the brief at `89fd4e2610` by its markers (sha256 prefix `e81453b6732cdea8`, 130 lines) and the script it writes |
| `block.out` | the block's printed lines (§ 7 criterion 6's lines) |
| `membership-block-2.txt` | the block's second pass: the TSV of the 254 inventory rows, `TREE-SIDE`, `CLAIMS`, `DOCS TREE BY SLICE`, `DOCTRINE BY SLICE` |
| `paths.txt`, `text.txt` | the 254 paths and the 223 text rows the block derives |
| `split.sh`, `split.py`, `classes.tsv` | § 2's split block (sha256 prefix `afb1909c5cdc6c88`, 46 lines), its script and its per-row classes |
| `split-p1.out`, `split-tip.out` | the split under `LC_ALL=en_US.UTF-8` with the defaults, and at the dispatch tip `86ebb6dffc` (no `absent` line) |
| `order.out` | `tools/renovation-inventory --order --no-write` (rc 0) |
| `lint-local-pass.out`, `lint-local-fail.out` | the lint on T4's Local folder exported from `6ec78bbf8c` (rc 0, `PASS`), and on the same with `tier_exception` removed (rc 1) -- ruling (q) |
| `prose-check-self-test.out` | `tools/prose-check --self-test` (`self-test: PASS`) |
| `issue-states.txt` | the § 3 item 9 issues and the states read at stage A |

The `CARVE` lines, the checkers' one-line results (`rules-check`, `register-check`,
`es-menu-map-check`, `release-catalog --check`, `work-log-index --check`,
`ceremony-check`) and the host file's read were recorded in `00` and `01` as they
printed. Their full output files were not kept at stage A. Stage C reruns each one
and keeps its output under `stage-c/`.
