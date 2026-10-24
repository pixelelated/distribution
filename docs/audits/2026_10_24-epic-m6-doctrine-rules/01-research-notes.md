# Research notes — M6.P2 T4, the binding doctrine (#651)

## Scope

**Read hash:** `8ebaf8daad8eaac6331dff6fc048fb4411d7decb` (`next`).
- **The branch at stage A** is `00e75ab135`, the dispatch's. The read is made on the hash's bytes, from `.qa-scratch/t4/at-hash/` (`git archive 8ebaf8daad <the globs>`, 36 files), and every line number in these artifacts is the hash's unless marked *branch*.
- **`upstream/next` at the read** is `481c9d0d75`. It is not compared: the doctrine is fork-own, and ROCKNIX carries none of it.

**The filter** (brief § 2, run with `python3 -I` over `docs/reviews/inventory.json`, whose header names P1's `eb4763e3cc`): the rows with `tree == distribution` and `area == doctrine`, under `.claude/rules/**`, `CLAUDE.md`, `AGENTS.md`, `NAMING.md` and `docs/{decision-register,blindspot-register,friction-log}.md`. Output, 14:34 UTC:

```
paths 36 lines 11414 {'fork-own': 36} {'markdown': 36} {'n/a': 36}
```

These are the brief's and #651's figures: **36 paths; 11,414 lines in the inventory at `eb4763e3cc`; 11,394 at `8ebaf8daad`**. The second figure was taken two ways that agree:
- `git diff --numstat <empty tree> 8ebaf8daad -- <the globs>` summed;
- `cat` of the 36 read-tree files into `wc -l`.

All 36 paths are fork-own, `markdown` and `reach: n/a`. The inventory's path set equals the tree's at the hash (`cmp` of the two sorted lists). **No delta.**

**The 36, by size at the hash:**

| Lines | Path |
| ---: | --- |
| 1,398 | `generic-x64-vm-testing.md` |
| 1,198 | `docs/blindspot-register.md` |
| 895 | `rclone-cloud-sync.md` |
| 863 | `docs/friction-log.md` |
| 836 | `engineering-practices.md` |
| 738 | `docs/decision-register.md` |
| 695 | `device-builds.md` |
| 423 | `es-native-ui.md` |
| 351 | `AGENTS.md` |
| 343 | `es-player-text.md` |
| 315 | `es-ui-style-guide.md` |
| 254 | `es-code-traps.md` |
| 254 | `worktrees.md` |
| 253 | `council-substrate-integrity.md` |
| 225 | `upgrade-and-install.md` |
| 224 | `instruction-files.md` |
| 208 | `issue-tracking.md` |
| 202 | `CLAUDE.md` |
| 191 | `fork-workflow.md` |
| 154 | `release-candidates.md` |
| 127 | `milestone-phase-naming.md` |
| 124 | `adversarial-council.md` |
| 116 | `ceremonies.md` |
| 114 | `handheld-evidence.md` |
| 113 | `packaging-and-patches.md` |
| 106 | `working-principles.md` |
| 99 | `decision-register.md` |
| 91 | `bugs-are-agent-first.md` |
| 91 | `learning-capture.md` |
| 82 | `vm-first.md` |
| 68 | `player-language.md` |
| 61 | `documentation-accuracy.md` |
| 60 | `NAMING.md` |
| 55 | `time-to-play.md` |
| 47 | `change-log.md` |
| 40 | `least-surprise.md` |

The rows above are the inventory's per-path figures. Three differ from the hash: the friction log (863 in the inventory), the decision register (738) and `instruction-files.md` (224) are the inventory's at `eb4763e3cc`, and the 20-line difference is in those three. At the hash they are 856, 728 and 221, the brief's figures. Every other file's count is the same at both; the per-file `wc -l` of the read tree is `.qa-scratch/t4/hash-lines.txt`, and it sums to 11,394.

**What loads every session.** Each rule's front matter was read at the hash and its `paths:` block parsed whole (not by `grep -A`; `.qa-scratch/t4/loads.txt`):

| Rules | Count | Lines |
| --- | ---: | ---: |
| no `paths:` key | 7 | 606 |
| `paths: "**"` | 17 | 4,573 |
| scoped | 6 | 2,820 |

- **No `paths:` key:** `bugs-are-agent-first`, `ceremonies`, `least-surprise`, `player-language`, `release-candidates`, `time-to-play`, `vm-first`.
- **Scoped:** `change-log`, `council-substrate-integrity`, `generic-x64-vm-testing`, `handheld-evidence`, `packaging-and-patches`, `rclone-cloud-sync`.

So **24 of 30 rules and 5,179 lines** load at every Claude Code session's start, plus `CLAUDE.md`'s 202. Crush loads all 30. **No delta.**

**The branch's doctrine deltas from the hash, hunk by hunk** (`git diff 8ebaf8daad 00e75ab135 -- <the 36>`: 8 files, +130/-3):

| File | Hunk (at the hash, then the branch) | What | Owner |
| --- | --- | --- | --- |
| `.claude/rules/device-builds.md` | `@@ -182,0 +183,9` | § After rebasing item 3: read every field (`PKG_SHA256`, `PKG_URL`, `PKG_ARCH`) per plan through `config/options` (`libfmt`, #877; `btrfs-progs`, #879) | coordinator, `764d30ed2e` (T7's retro) |
| `.claude/rules/engineering-practices.md` | `@@ -239,0 +240,10` | § A name is not a behaviour: a count, a line number or a hash is a claim about one tree; a hash is copied, never completed from a prefix (blindspot 75's guard) | coordinator, `ab8f750784`, extended in `e09b57d16c` |
| `.claude/rules/fork-workflow.md` | `@@ -33 +33` | the personal-paths list gains `tools/renovation-inventory`, `-drift` and `-status` | P1, `9966dbcd12`, `af24589b1c` |
| `.claude/rules/generic-x64-vm-testing.md` | `@@ -1224,0 +1225,7` | a run meant to measure the tree's scripts binds them from an autostart hook and reads the installed hash; #797 | coordinator, `8c9b1d4721` (T1's retro) |
| `.claude/rules/instruction-files.md` | `@@ -188 +188`, `@@ -194,0 +195,3` | the `lint-audit-artifacts` row names the renovation face; three rows for the renovation tools | P1, `9966dbcd12`, `af24589b1c`, `fc88815ccb` |
| `docs/blindspot-register.md` | `@@ -1198,0 +1199,52` | entries **74** (a fixture that did not engage), **75** (a corpus read on the wrong tree) and **76** (a merge chain that does not stop on its own check), appended | coordinator, `179093ffd6`, `ab8f750784`, `0921782112`, `1b8ac30421` |
| `docs/decision-register.md` | `@@ -711,0 +712,21` (decided rows), `@@ -717,0 +739,2` (open rows), `@@ -723 +746` | 21 rows appended to `## Decided`: D-WORKFLOW-181 to 190 and 192 to 199, D-INFRA-025 to 027. 2 appended to `## Open decisions`: D-WORKFLOW-191, D-SYS-014. **One row changed in place**: D-QA-040, in the open table, gained an `**Open:**` prefix | the coordinator and P1 (25 commits, `0bfd387f7b` to `e3897db16d`); D-QA-040's prefix is `f00ab3e163` (#646) |
| `docs/friction-log.md` | `@@ -856,0 +857,23` | 23 lines appended | the coordinator and the lanes (25 commits) |

**D-QA-040**, for stage B:
- **What changed:** `f00ab3e163` (*ten decided rows moved from under Open decisions into the Decided table; register-check refuses a statement row there*, #646) moved those rows with their text unchanged, and added `**Open:**` to D-QA-040, *"a genuine open question written as a statement"*. The row is in `## Open decisions` at both the hash (table at line 713) and the branch (line 734).
- **What the contract says:** `decision-register.md` makes **decided** rows append-only. An open row's settlement is a move with its ID kept. Nothing is said of a marker added to an open row.
- That is a Q2 lead, not a stop.

**The branch scan** (brief § 2's predicate: a branch is ahead when `git log next..<branch> -- <the 36>` prints a line; `.qa-scratch/t4/branch-scan.txt`):
- **20 of 70 `origin/` refs are ahead.** Every M6 lane branch is ahead, as expected: the lanes append to the registers and inherit P1's and the coordinator's rule edits by merge.
- **Rule edits outside those two histories** (`git rev-list --no-merges next..<b> -- <rules>` less the commits of `feature/m6-renovation-plan-346` and `feature/m6-p1-survey-641`; `.qa-scratch/t4/branch-scan-own.txt`):

| Branch | Commit | Files | Standing |
| --- | --- | --- | --- |
| `feature/m6-es-launch-path-649` (T2, accepted) | `11a2ee182f` 2026-10-23 | `es-native-ui.md` +5/-1 | the coordinator's by acceptance; it reaches this branch at the merge. The brief calls it `f16cf7fc28`, which is T2's tip, not the edit's commit |
| `feature/m7-manual-cloud-folders` | `e484380a34` 2026-10-07 | `fork-workflow.md`, `instruction-files.md` | the M7 lane's, not in `next` |
| `feature/conflict-resolution` | 36 commits, tip 2026-10-07 | many rules | a pre-renovation branch; a Q6 lead (a stale branch carrying doctrine `next` lacks) |
| `x64-build-fix` | 3 commits, 2025-10-22 | `CLAUDE.md` | the same |
| `verification-anchors/2026-09-30-rasteratops-fork-plan`, `-r2` | 1 each, 2026-09-30 | many rules | the same; anchors by name |

**No unaccepted M6 lane carries a rule edit of its own** (D-WORKFLOW-189 holds).
- **The M7 lane's register rows 171 to 180** are in its legacy checkout, on no fetched ref (brief § 2), and are read only when a new row's ID is chosen.

**Interacting subsystems (read-only context):**
- the four doctrine tools: `tools/rules-check`, `tools/register-check`, `tools/ceremony-check`, `tools/forbidden-terms-check`;
- `tools/archaeology`, `tools/box-check`, `.githooks/`;
- `docs/reviews/cross-reference.md` § Doctrine to area;
- the other slices' briefs and retros (their stale-facts lines);
- `docs/reviews/build-path-read.md` (#644);
- the code-auditor and mini-retro skills (T38's);
- `docs/es-menu-map.md` and `docs/conflict-wizard-ia.md` (T39's), which load nowhere.

## The reader's pass

*Written at stage B: what a stranger stumbled on, file by file, before any auditing.*
