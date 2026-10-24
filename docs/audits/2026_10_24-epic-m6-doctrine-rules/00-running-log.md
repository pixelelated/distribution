# Epic Audit Running Log — M6.P2 T4, the binding doctrine

**Auditor:** Code Auditor skill, with the renovation face of `docs/reviews/plan-for-the-plan.md` § 4
**Primary model:** Claude Opus 5.5 (`claude-opus-5-5`, lab Anthropic) at high effort, in Claude Code. Identity sources: the coordinator's dispatch on #651 (issuecomment-6385443829, 2026-10-24T14:32:50Z) and the session's own metadata
**Session:** herdr agent `m6-t3-emulators`, session `a6d65411-5a44-4596-9a6c-337855905c17`, pane `wN:p6`. It is the T3, T30 and T24 session; those three worktrees are accepted and idle beside this one, and nothing is written there
**Started:** 2026-10-24 14:33 UTC (`date -u` 14:33:48 at the first commands)
**Scope:** slice `doctrine-rules` (#651, `M6.P2 E807/T4`), area epic #807 (the doctrine), renovation epic #339, milestone M6. The membership is the inventory's `doctrine` rows under the globs of brief § 2: 36 paths
**Spec:** `docs/reviews/briefs/doctrine-rules.md` version 2 (`0921782112`). Its § 7 is #651's checklist, and #651 wins where they differ. Also `docs/reviews/plan-for-the-plan.md`, byte-identical (`cmp`) to the copy read whole at T24's start this session
**Depth:** Local (plan § 6c, *a doctrine read*; D-WORKFLOW-184). No reviewer, no Facilitator call, no `npm install`
**Branch / worktree:** `feature/m6-doctrine-rules-651` at `/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-rules-651`
**Read hash:** the slice's bytes are `next`'s `8ebaf8daad`, read from `.qa-scratch/t4/at-hash/`. `reviewed-at` is the branch `HEAD` at stage A, `00e75ab135`; the branch's doctrine deltas from the hash are listed below and in `01` § Scope
**Proof tokens:** a line in this log that records a proof begins with the proof token (criterion 12 counts them against the `proved:` cells of `02-forward-audit.md`); this header names it without starting a line with it

---

## Log Entries

### [Phase 0] 14:32-14:34 — The dispatch read; the brief's first commands (`date -u` 14:32:59, 14:33:48, 14:33:59)

- **The dispatch** (issuecomment-6385443829) was read first. No third lane runs: this session takes T4. The lane branch is at `00e75ab135`, stacked on P1's `2174265e9c`, with the coordinator's `c35acd3732` merged at `e3897db16d`. **Eleven paths** differ from `next`, superseding the brief's five. The depth is Local, with #810 merged here at `18747fbc52`.
- `git fetch origin` and `git fetch upstream --no-tags`: rc 0. `upstream/next` is `481c9d0d75` (it moved from `e0f9deb899` at 13:38 UTC, heroic only; it is not this slice's: no upstream carries the doctrine).
- Branch `feature/m6-doctrine-rules-651`, `HEAD` `00e75ab135c9a0a0cc1b8bf27c15a736af04764e`. `git merge-base --is-ancestor 2174265e9c HEAD` exit 0. `next` = `8ebaf8daad8eaac6331dff6fc048fb4411d7decb`.
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md NAMING.md docs/decision-register.md docs/blindspot-register.md docs/friction-log.md tools/lint-audit-artifacts`: **11 files, +226/-12**, exactly the dispatch's eleven:
  - `device-builds.md` +9;
  - `engineering-practices.md` +10;
  - `fork-workflow.md` +1/-1;
  - `generic-x64-vm-testing.md` +7;
  - `instruction-files.md` +4/-1;
  - `code-auditor/references/templates.md` +18/-1;
  - `council/IMPORTED-FROM.md` +25;
  - `docs/blindspot-register.md` +52;
  - `docs/decision-register.md` +24/-1;
  - `docs/friction-log.md` +23;
  - `tools/lint-audit-artifacts` +55/-6.

  Nothing else is stale.
- `git diff --stat 8ebaf8daad 2174265e9c -- .claude/rules CLAUDE.md AGENTS.md NAMING.md`: P1's two, `fork-workflow.md` 1+/1- and `instruction-files.md` 4+/1-.
- P1's `tools/renovation-{inventory,status,drift}`, `docs/reviews/inventory.json`, `slices.json` and `cross-reference.md`: present.
- **The read tree:** `git archive 8ebaf8daad .claude/rules CLAUDE.md AGENTS.md NAMING.md docs/decision-register.md docs/blindspot-register.md docs/friction-log.md | tar -x -C .qa-scratch/t4/at-hash` rc 0, **36 files** (`find -type f`). `.qa-scratch` is ignored.
- `tools/rules-check` rc 0; `tools/register-check` rc 0, `667 IDs, each once; every citation in the live documents names a row` (the brief's 660 is an earlier branch: the coordinator's later rows, a delta); `tools/ceremony-check` rc 1, whose one overdue line is `weekly OVERDUE: 2026-W42 summary missing`. That week is M7's, not this lane's to pay, and it is noted on #651.
- `git push -u origin feature/m6-doctrine-rules-651`: tracking set, nothing new to push.
- The brief and the epic's futro (`docs/futros/2026-10-24-m6-doctrine.md`) are in the tree, and the pointer has been read.
- **The host file's last blocks** are T8's, at 14:27 and 14:32: S4's guest cycle ended, `qemu 0`, M6 holds the host. This slice needs no runtime and starts none.
- `df -i /tmp` 40 %. `gh api rate_limit`: core **4,637 / 5,000** at 14:34.

### [Stage A] 14:34-14:37 — Scope re-derived; the branch's deltas; the branch scan

- **Counts** (brief § 2's filter, `python3 -I`, output kept in `.qa-scratch/t4/membership.txt`): **36 paths, 11,414 lines in the inventory (at P1's `eb4763e3cc`); 36 fork-own, 36 `markdown`, 36 `reach: n/a`.** The inventory's path set equals `git ls-tree -r --name-only 8ebaf8daad -- <the globs>` (`cmp`). At the hash: **11,394 lines** by numstat against the empty tree, and 11,394 by `cat | wc -l` over the read tree. **No delta** from the brief or #651.
- **What loads every session** (each rule's `paths:` block parsed whole from the front matter at the hash, `.qa-scratch/t4/loads.txt`):

  | Rules | Count | Lines |
  | --- | ---: | ---: |
  | no `paths:` | 7 | 606 |
  | `paths: "**"` | 17 | 4,573 |
  | scoped | 6 | 2,820 |

  So **24 of 30 rules and 5,179 lines** load at every Claude Code session's start, plus `CLAUDE.md`'s 202. The six scoped rules are `change-log`, `council-substrate-integrity`, `generic-x64-vm-testing`, `handheld-evidence`, `packaging-and-patches` and `rclone-cloud-sync`, the brief's six. **No delta.**
- **The branch's deltas from the hash over the 36** (`git diff 8ebaf8daad HEAD`, kept as `.qa-scratch/t4/branch-delta.diff`): 8 files, +130/-3. Each hunk and its owner is in `01` § Scope. The rule files are the five the dispatch names:
  - `device-builds.md` (coordinator, `764d30ed2e`);
  - `engineering-practices.md` (coordinator, `ab8f750784` and `e09b57d16c`);
  - `fork-workflow.md` and `instruction-files.md` (P1, `9966dbcd12`, `af24589b1c`, `fc88815ccb`);
  - `generic-x64-vm-testing.md` (coordinator, `8c9b1d4721`).

  The registers' hunks are appends, with one exception: **D-QA-040's row gained an `**Open:**` prefix** in the coordinator's `f00ab3e163` (#646), which moved ten decided rows from under `## Open decisions` to `## Decided`. D-QA-040 stayed in the open table, so the edited row is an open one, not a decided one. Whether the append-only contract speaks to open rows is a Q2 lead for stage B. **No hunk outside the dispatch's eleven paths: no stop.**
- **The branch scan** (`.qa-scratch/t4/branch-scan.txt`): 70 `origin/` refs; 20 are ahead of `next` on the 36. Commits touching a rule file that are in neither the coordinator's (`feature/m6-renovation-plan-346`) nor P1's history (`.qa-scratch/t4/branch-scan-own.txt`):
  - **M6:** one, T2's `11a2ee182f` (`es-native-ui.md` +5/-1, #699). T2 is accepted, so the edit is the coordinator's by acceptance. The brief cites it as `f16cf7fc28`, which is T2's tip and not the edit's commit: a delta.
  - **M7:** `feature/m7-manual-cloud-folders` carries `e484380a34` (2026-10-07, `fork-workflow.md` and `instruction-files.md`), which is not in `next`. It is M7's.
  - **Older branches:** `feature/conflict-resolution` (36 commits, tip 2026-10-07), `x64-build-fix` (3, 2025-10-22) and the two `verification-anchors/2026-09-30-*` branches (1 each) predate the renovation and carry rule edits `next` does not have. Each is a lead for Q6.
- `reviewed-at: 00e75ab135`. The read is on `8ebaf8daad`'s bytes.
