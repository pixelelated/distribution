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

### [Stage B] 14:37-15:01 — the reader's pass, the auditor's pass, `02`

- **The reader's pass** (`01` § The reader's pass):
  - 25 files were read whole in this session at the hash's bytes (`cmp` against T3's loaded copies: 30 of 36 identical; `fork-workflow.md` and `instruction-files.md` differ by P1's listed hunks).
  - 11 files went to four read-only readers with no context (brief § 5, rule 5), launched 14:38 and back by 14:45. Their reports are leads, and each finding taken from them was re-read here with its command.
- **The auditor's pass:**
  - § 5's checks: the six checkers, `box-check`, the globs, the IDs, the tool table and the legacy paths.
  - The Q4 and Q6 scripts: `tools/t4-q4.py` (ids, ledger-ids, tools, paths, counts) and `tools/t4-q6.py` (rules, tooltable, blindspots, retired, friction).
  - The 56 command blocks (`tools/t4-blocks.py`); the coverage table (`tools/t4-coverage.py`).
- **Corrected before commit:**
  - my first "no issue number" list for the friction log searched lines cut to 90 characters, and gave 27 where the full lines give 2;
  - `01`'s "120-entry line" was a guess, now counted as 100;
  - F-23's "7 of 11 rows carry four cells" was the reader's, recounted as 5 of four and 1 of five;
  - the command-block rows began with a rule path and inflated criterion 7's grep to 92; they are numbered now, and it prints 36.
- **`tools/box-check`** spent no core API calls: 4,390 before and after.

PROOF: 14:34 P1 the membership: 36 paths, 11,414 inventory lines, all fork-own markdown, reach n/a -- `.qa-scratch/t4/membership.txt`
PROOF: 14:37 P2 the lines at the hash: 11,394 by numstat and by `wc -l`; the inventory's 20 extra lines are in the friction log, the decision register and `instruction-files.md` -- `hash-lines.txt`
PROOF: 14:34 P3 24 of 30 rules and 5,179 lines load every session (7 no `paths:`, 17 `**`) -- `loads.txt`, `t4-q6.py rules`
PROOF: 14:35 P4 the branch's deltas over the 36: 8 files, +130/-3, owners listed; D-QA-040's `**Open:**` is `f00ab3e163` -- `branch-delta.diff`
PROOF: 14:35 P5 the branch scan: 20 of 70 refs ahead; no unaccepted M6 lane rule edit; T2's `es-native-ui.md` edit is `11a2ee182f` -- `branch-scan-own.txt`
PROOF: 14:42 P6 `rules-check` 0, `register-check` 0 (667 IDs), `ceremony-check` 1 (W42 only), `forbidden-terms-check` 0 (0 hits in 133,406 files), `hooks-test` 0 (PASS), `box-check` 0 (0 fail)
PROOF: 14:42 P7 57 `paths:` globs over 23 rules; one matches nothing at the hash and the branch, `council-substrate-integrity.md`'s `research/council-research/**` -- `globs-hash.txt`
PROOF: 14:43 P8 181 IDs cited in the 33; 178 decided, 3 open, 0 absent -- `t4-q4.py ids`
PROOF: 14:42 P9 the tool table's 72 rows, every tool and rule they name present at the hash -- `t4-q6.py tooltable`
PROOF: 14:42 P10 the legacy paths: 8 files, 25 lines (#640)
PROOF: 14:46 P11 `ceremony-check:250-252`'s friction regex, lifted and applied: 125 of 445 dated entries never seen; 2 name no issue, both a guard -- `t4-q6.py friction`
PROOF: 14:44 P12 `rules-check`'s header lists eight checks, none comparing a fact between `AGENTS.md` and `CLAUDE.md` (`AGENTS.md:19-20`)
PROOF: 14:49 P13 `OS_VERSION` assigned unconditionally (`distributions/ROCKNIX/version:8`, sourced at `config/options:42`); `BUILD_DATE` defaulted (`distributions/ROCKNIX/options:212`)
PROOF: 14:49 P14 `tools/vocabulary-check` checks SAVESTATE and Wi-Fi as well as back up / backup (its lines 12-15, 55-57)
PROOF: 14:50 P15 D-CLOUD-130 reverses D-CLOUD-109 for launches; T2's running log :114 reads `FileData.cpp:993-1008` as D-CLOUD-130
PROOF: 14:45 P16 `var-log.mount` binds `/storage/.cache/log` on `/var/log` at the hash and in the GENERIC_X64 install tree
PROOF: 14:44 P17 `fork-publish-release` makes no qcow2 or `.utm.zip`; `CONFIG_REALPATH=y` and `usr/bin/realpath -> busybox`; `emustation.service` installed; `watch-build:98` refuses without an admission or `--record-only`
PROOF: 14:45 P18 `generic-x64-vm:281-295` (virgl default), `:435` (the watchdog), `profile.json` without one, `vm-qa:63` (17 suites)
PROOF: 14:55 P19 `rclone/package.mk:7,39,43` (1.75.2, two `PKG_SHA256`), `cloud_sync-rules.txt:63-64`, `cloud_backup:747`, `cloud-round-trip:1460-1470` (exit 69), the rule's content tier at `:705-709`
PROOF: 14:54 P20 31 of the index's 85 tool-to-rule pointers name a rule that never names the tool; `cloud-pair-migration:58-62` refuses
PROOF: 14:54 P21 the ES checkout's `origin` is `pixelelated/emulationstation` (`git remote -v`, read only); `fork-workflow.md:62` names `maxengel`
PROOF: 14:58 P22 ten paths `council-substrate-integrity.md` names absent at the hash (`git cat-file -e`); its glob matches 0
PROOF: 14:56 P23 the 56 command blocks each with a verdict (`t4-blocks.py`); the seven read-only blocks ran (14:48); the drop filter printed `name=ok` only and the mask kept no value
PROOF: 14:51 P24 the superseded citations: 45 candidates, 2 cite a superseded row as current (`time-to-play.md`, `least-surprise.md`) -- `q4-superseded-review.txt`
PROOF: 14:52 P25 74 blindspot entries, 29 numbered twice; every named guard path exists -- `t4-q6.py blindspots`
PROOF: 14:50 P26 `build.ROCKNIX-` in 8 lines of 4 rules; `config/path:19` and `DISTRONAME="pixelelated"` make `build.pixelelated-*`
- `git status --short -- <the 36>`: 0 lines (none of the 36 changed at stage B).
