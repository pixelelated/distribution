# Epic Audit Running Log — M6.P2 T30, the standalone emulators

**Auditor:** Code Auditor skill (v1.13.0, identical to `next`'s copy: `diff -q` against `git show next:.claude/skills/code-auditor/SKILL.md`, no output), with the renovation face of `docs/reviews/plan-for-the-plan.md` § 4
**Primary model:** Claude Opus 5.5 (`claude-opus-5-5`, lab Anthropic) at high effort, in Claude Code. Identity sources: the coordinator's dispatch on #677 (issuecomment-6381895209, 2026-10-24T08:16:35Z) and the session's own metadata
**Session:** herdr agent `m6-t3-emulators`, session `a6d65411-5a44-4596-9a6c-337855905c17`, pane `wN:p6` (the T3 session; its T3 worktree is idle beside this one, written nowhere)
**Started:** 2026-10-24 08:17 UTC (`date -u` 08:17:51 at the first commands)
**Scope:** slice `emulators-standalone` (#677, `M6.P2 E798/T30`), area epic #798 (the emulators and cores), renovation epic #339, milestone M6. The membership is the inventory's `k: 30` rules (brief § 2): 543 paths
**Spec:** `docs/reviews/briefs/emulators-standalone.md` version 2 (`b81fc193a1`; its § 7 is #677's checklist, and #677 wins where they differ); `docs/reviews/plan-for-the-plan.md`
**Depth:** Extended (two reviewers from two other labs: GPT-6 Astra `--member gpt` at `max`, Gemini 4 Argon `--member gemini-argon` at `high`; probes first, then one refutation packet to each independently)
**Branch / worktree:** `feature/m6-emulators-standalone-677` at `/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-standalone-677`
**Read hash:** the slice's bytes are `next`'s `8ebaf8daad`; `reviewed-at` is the branch `HEAD` at stage A, recorded below
**Proof tokens:** a line in this log begins with the guest token or the host token only to record a proof (criterion 12 counts them against the `proved:` cells of `02-forward-audit.md`); this header names them without starting a line with either

---

## Log Entries

### [Phase 0] 08:17-08:18 — The brief's first commands (`date -u` 08:17:51, 08:18:32)

- `git fetch origin`, `git fetch upstream --no-tags`: both exit 0.
- Branch `feature/m6-emulators-standalone-677`, `HEAD` `c7e3dfcc87411ab3c92c41ce49539a7e9328d84b` (the dispatch's hash); `git merge-base --is-ancestor 2174265e9c HEAD` exit 0: stacked on the P1 tip. `docs/reviews/inventory.json` and `slices.json` present; `tools/renovation-{inventory,status,drift}` present.
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`: seven files (115+/11-): `engineering-practices.md`, `fork-workflow.md`, `generic-x64-vm-testing.md`, `instruction-files.md`, `code-auditor/references/templates.md`, `council/IMPORTED-FROM.md`, `tools/lint-audit-artifacts`. Exactly the seven paths brief § 1 names; nothing stale.
- `grep -c 'Renovation face' tools/lint-audit-artifacts` 4; `grep -c gemini-argon scripts/council-invoke.ts` 7.
- `next` = `8ebaf8daad8eaac6331dff6fc048fb4411d7decb`. **`upstream/next` = `e0f9deb89926f0febd81084dc947ad93d52db132`** (Q4's upstream, fetched now; T3 read `3421d7d178`). `git merge-base next upstream/next` = `c445081a59518f37d9776e5412dd7b14910696f7`.
- The read tree: `git archive 8ebaf8daad projects/ROCKNIX/packages/emulators/standalone | tar -x -C .qa-scratch/t30/at-hash` rc 0, 623 files (543 members + 80 patches, brief § 2). `.qa-scratch/` is ignored (`.gitignore:63`).
- `git diff --stat 8ebaf8daad HEAD -- projects/ROCKNIX/packages/emulators/standalone`: **empty**. The slice's bytes are `next`'s.
- `tools/rules-check` rc 0; `tools/register-check` rc 0 (662 IDs, each once); `tools/ceremony-check` rc 1, its one overdue line `weekly OVERDUE: 2026-W42 summary missing`: M7's week, noted, not this lane's (the coordinator's 08:16 note on T3).
- `git push -u origin feature/m6-emulators-standalone-677`: up to date, tracking set. `core.hooksPath` lists `pre-push`.
- The brief is in the tree. The host file's last M7 block is the **05:42:07 resource return** (line 106); the M6 blocks after it (07:13, 07:21) open no hold. **M6 holds the host.** Census: `pgrep -c -x qemu-system-x86` 0, `pgrep -fc 'make docker-[A-Z]'` 0; `free -g` 41 G available, swap 3 of 7 G used; `/workspace` 1.7 T free.
- `df -i /tmp` 40 % (633,260 inodes free); `df -i /workspace` 19 %. Exports go under `/workspace/tmp/m6-t30/`.
- `~/.config/council/env` present (not read). `node` v24.21.0, `npm` 11.19.0; `tools/council/node_modules` absent (the install comes before Phase 4.6).

### [Stage A] 08:19-08:22 — Scope re-derived; T3's tools copied

- **Counts** (brief § 2's filter, `python3 -I`, 08:19:07): 543 paths, 157,365 lines; 55 fork-own / 7,421 lines; 488 upstream-carried; all `shipped`; 105 code-class files / 10,695 lines, 3,104 fork-own (shell 55 / 6,635, recipe 47 / 2,651, python 2 / 483, c 1 / 926); 35 recipes; thirteen fork-own `package.mk`. **No delta** from the brief or #677. Recorded in `01` § Scope with the fork-own table (55 rows).
- **Tree against membership:** `git ls-tree` 623 = 543 + 80 `.patch`; `comm -3` in the C locale prints nothing. In the session's `en_US` locale `comm` refused the input as unsorted, which is T3's S2 trap again; re-run under `LC_ALL=C`.
- **Start scripts:** 40 `start_*.sh`. The 41 at `order.md:787` is the same set plus `Start Duckstation.sh` (a case-insensitive count gives 41). Recorded; no disagreement.
- **Upstream:** 38 commits on `standalone/` since the base, all after `8ebaf8daad`; `git diff --stat upstream/next 8ebaf8daad` 144 files, +71,085/-1,034. The fork has 41 commits on the membership since the base. Exit-sweep leads before reading: `eeb33c5a37`, `4a6415c033` (duckstation-sa → `duckstation-qt`).
- **Device × recipe:** the metapackage's arms evaluated per device under `env -i` from a copy in `.qa-scratch/t30/meta/`, and the inventory's `reachable_by` per `package.mk`; the two agree. **H700 17, SM8550 35, GENERIC_X64 15** by the arms. The brief's image list is thirteen, so `amiberry` and `yabasanshiro-sa` are a Q6 lead for the image-set check.
- **Tools** copied by path from T3's folder at `b3cb4ec8c5` into `docs/audits/2026_10_24-epic-m6-emulators-standalone/tools/`, each with a provenance comment after its copyright line: `q4-pins.py`, `q4c-patches.sh`, `regen-es-systems.sh`, `s2-regen-check.sh`, `punch-items.py`, `coverage-table.py`, `audit-issue-body.py`, `set-outcome.py`, `write-completion.py`. One change so far: `q4-pins.py` lines 64-65 (T3's 59-60) read `standalone/`. `diff` against T3's file shows only the header and those two lines; `py_compile` passes. The first `sed` used `#` as its delimiter on a comment and failed. A line count off by one left line 65 at `libretro`; the diff caught it and it was fixed before commit.
- **`reviewed-at` candidate:** `c7e3dfcc87` (HEAD at stage A; the membership's bytes are `8ebaf8daad`'s). Final at hand-back.
