# T6's remediation streams (#653, audit issue #846)

Written by the coordinator at T6's stage-D pause (2026-10-24, D-WORKFLOW-189),
in the D-WORKFLOW-056 shape: the files owned, the test first, the `Already
written:` line, commits cut after the checks are green. The slice's one
fork-own row, `tools/pkgcheck`, is the only file either stream touches; **no
upstream-carried file is edited or deleted** (brief § 2's policy). Nothing
builds or runs on a guest; `pkgcheck` reads recipes and prints. Commits land
on the slice branch `feature/m6-build-engine-upstream-tools-653`, cite the
item and its issue with `Refs`, keep the tool's headers, leave `git status
--short` empty (read before each commit as well as after), add a `PROOF:`
line per proof, and move the Phase 7 table and the `punch_index` at the end
of each stream. A tree export, should one be needed, goes under
`/workspace/tmp/m6-t6/` after `df -i`.

## Dispositions that are not streams (the coordinator's; the lane writes them into the Phase 7 table)

| Item | Disposition |
| --- | --- |
| PL-02 (F-04, F-06: the 22 unreached rows, the tools that do one job twice) | `deferred:#585`: the proposal is posted there in the lane's words (2026-10-24 08:3x), held under D-WORKFLOW-165; every row stays *kept: upstream's, unreached* |
| PL-03 (F-03: `distributions/LEIoT/kernel_options` dangles) | `deferred:#585`: named in the proposal; upstream's file, read only by a `DISTRO=LEIoT` build the fork never makes |
| PL-04 (F-01: the rules call `pkgcheck` upstream's) and PL-05 (F-05: `CLAUDE.md:131` lists `distro-tool`) | `deferred:#651` (T4): two rows for its Q4(b) and Q7 tables; T4's brief § 3 gains them with its next version |
| The ladder's guard (a check that an unreached tool stays unreached) | **#847** filed (a fork tool, T10's area) |

## S1. `tools/pkgcheck` refuses a name that matches no recipe (PL-01, #845) -- Low

- **Files owned:** `tools/pkgcheck` (lines 155 to 169: the selection loop and the exit).
- **The test first:** `tools/fx-pkgcheck.sh <scratch> 8ebaf8daad` prints `exit 0` for `fixture-no-such-package` (the defect); after the fix the same fixture against the working tree (`WORKTREE`) prints a non-zero exit for it, `exit 1; FAIL lines 1` for `fixturebad` and `exit 0` for `fixturegood` unchanged (#845's criterion); the no-argument run over every recipe in the tree still exits 0 with no FAIL (the sweep S2 also uses: paste its last lines). **Erratum (T6's hand-back, 2026-10-24):** the baseline is not 0 -- `tools/pkgcheck` over every recipe at `8ebaf8daad` prints 12 FAIL lines and 43 WARN lines on real recipes, unchanged by S1; S2 took it to 21, of which 14 are the parser's false positives on `wireplumber` (#657) and the rest real leads for T7/T8.
- **The change:** count the recipes the selection reached; when an argument matches none, say so on stderr naming the argument and exit 2 (a selection error, distinct from 1, a FAIL); the no-argument branch unchanged. The header's exit-status paragraph gains the new code.
- **Already written:** nothing on a device or in a cloud; a name once "checked" under a mistyped argument was never checked, and the fixed tool says so the next time (#845).
- **Proof class:** `fixture` (the fixture before and after).
- **Commit:** `pkgcheck: exit 2 when a package name matches no recipe (#845)`, `Refs #845, #846, #585` (the fork's `81221658b3` is already in the upstream series, `docs/pr-series/map.txt:20`; this change joins it).

## S2. `tools/pkgcheck`'s late-binding list names what `config/path` and `config/functions` set late (PL-06, the lead) -- Low

- **Files owned:** `tools/pkgcheck` (the list at lines 49 to 58).
- **Why here and not #657:** the tool is this slice's one fork-own row, the lead is its Q3 reading, and the change is the tool's own list; the fork CI, the `Makefile` and `scripts/` run `pkgcheck` nowhere (`git grep pkgcheck -- .github/workflows Makefile scripts` is empty), so a widened list breaks no automated run.
- **The test first:** the no-argument sweep (`tools/pkgcheck` over every recipe in the tree) before the change: its exit and FAIL count (0 expected); a fixture recipe under `.qa-scratch/t6/` that references `${TOOLCHAIN}` and `${INSTALL}` at global scope: `pkgcheck` passes it before (the gap) and FAILs it after (the positive control, in `fx-pkgcheck.sh` as a fourth case). Then the sweep after the change: **every new FAIL on a real recipe is a lead for that recipe's slice** (T7 for `packages/**`, T8 for `projects/**`'s packages, the device slices for a device's), listed in the hand-back with file:line and routed by the coordinator; the names land regardless, because a check that stays silent about a real late-binding use is the defect this slice found.
- **The change:** the names `config/path` and `config/functions` export only after a package loads and the list lacks -- `TOOLCHAIN`, `SYSROOT_PREFIX`, `INSTALL`, and the others the lead names from reading the two files (`04` § Q3; the full set is derived from `config/path`'s and `config/functions`' exports, not guessed, and the hand-back names each with its source line) -- added to the list in the file's own order; the header's list paragraph updated.
- **Already written:** nothing on a device; a recipe that violated late binding with one of the new names built as it built, and goes on building; the sweep names them for their slices.
- **Proof class:** `fixture` and the sweep's two runs (`tool-run`).
- **Commit:** `pkgcheck: check the names config/path and config/functions set after a package loads (#653)`, `Refs #653, #846`.

## Order and hand-back

S1, then S2, each handed back with one comment on #653 (the commit, the fixture lines before and after, the sweep's lines, the `punch_index` rows moved); then the close-out in T3's order: tick every checkbox of #846 from its Phase 7 outcome and run `tools/box-check --issue 846`; write `fixed-at:` into #653's body; the pre-issue lint; the retro (stage G, posted on #653, with *nothing* for the two time-to-play numbers in those words); the stage-H hand-back per the brief § 10. The coordinator closes #846 at acceptance and prompts for `audit-completion.json` and the full lint.
