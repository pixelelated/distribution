# Epic Audit Running Log — M6.P2 T24, emulator recipes and files no shipped image builds

**Auditor:** Code Auditor skill (v1.13.0, identical to `next`'s copy: `diff -q` against `git show next:.claude/skills/code-auditor/SKILL.md`, no output), with the renovation face of `docs/reviews/plan-for-the-plan.md` § 4
**Primary model:** Claude Opus 5.5 (`claude-opus-5-5`, lab Anthropic) at high effort, in Claude Code. Identity sources: the coordinator's dispatch on #671 (issuecomment-6384884754, 2026-10-24T13:37:39Z) and the session's own metadata
**Session:** herdr agent `m6-t3-emulators`, session `a6d65411-5a44-4596-9a6c-337855905c17`, pane `wN:p6` (the T3 and T30 session; both worktrees are idle beside this one, written nowhere)
**Started:** 2026-10-24 13:38 UTC (`date -u` 13:38:23 at the first commands)
**Scope:** slice `emulators-dead-ends` (#671, `M6.P2 E798/T24`), area epic #798 (the emulators and cores), renovation epic #339, milestone M6. The membership is the inventory's `k: 24` rule, `select: rest` (brief § 2): 86 paths
**Spec:** `docs/reviews/briefs/emulators-dead-ends.md` version 2 (`c25d772b21`; its § 7 is #671's checklist, and #671 wins where they differ); `docs/reviews/plan-for-the-plan.md`
**Depth:** Local (D-WORKFLOW-184; `slices.json` k 24: a reachability table). No reviewer, no Facilitator call, no `npm install`
**Branch / worktree:** `feature/m6-emulators-dead-ends-671` at `/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-dead-ends-671`
**Read hash:** the slice's bytes are `next`'s `8ebaf8daad`; `reviewed-at` is the branch `HEAD` at stage A, `81331b499e`, recorded below
**Proof tokens:** a line in this log begins with the host token only to record a proof (criterion 11 counts them against the `proved:` cells of `02-forward-audit.md`); this header names it without starting a line with it

---

## Log Entries

### [Phase 0] 13:38-13:40 — The brief's first commands (`date -u` 13:38:23, 13:39:50)

- `git fetch origin`, `git fetch upstream --no-tags`: both exit 0. **`upstream/next` moved with this fetch**: `e0f9deb899` (the brief's) to `481c9d0d75` (two commits, `ace187c808` *heroic: upgrade to 2.22.4* and its merge; one file, not one of the 86). Q4 (a) runs against both and records each.
- Branch `feature/m6-emulators-dead-ends-671`, `HEAD` `81331b499e73717b4713544c934796c088e1a7f5` (the dispatch's hash); `git merge-base --is-ancestor 2174265e9c HEAD` exit 0: stacked on the P1 tip. `docs/reviews/inventory.json` and `slices.json` present; `tools/renovation-{inventory,status,drift}` present.
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`: eight files (127+/11-): `device-builds.md`, `engineering-practices.md`, `fork-workflow.md`, `generic-x64-vm-testing.md`, `instruction-files.md`, `code-auditor/references/templates.md`, `council/IMPORTED-FROM.md`, `tools/lint-audit-artifacts`. Exactly the eight the dispatch lists (the pointer's "seven" predates `device-builds.md`); nothing else stale.
- `next` = `8ebaf8daad8eaac6331dff6fc048fb4411d7decb`; `git merge-base 8ebaf8daad upstream/next` = `c445081a59` for both upstream heads.
- The read tree: `git archive 8ebaf8daad packages/emulation projects/ROCKNIX/packages/emulators/libretro | tar -x -C .qa-scratch/t24/at-hash` rc 0. `find -type f` counts 471; `git ls-tree -r` counts **474** (97 under `packages/emulation`, 377 under the ROCKNIX `libretro/`), of which 3 are symlinks (mode `120000`), which `find -type f` skips: the brief's 474, no delta. `.qa-scratch/` is ignored (`.gitignore:63`).
- `tools/rules-check` rc 0; `tools/register-check` rc 0 (667 IDs, each once); `tools/ceremony-check` rc 1, its one overdue line `weekly OVERDUE: 2026-W42 summary missing`: M7's week, not this lane's (brief § 1).
- `git push -u origin feature/m6-emulators-dead-ends-671`: everything up to date, tracking set. `core.hooksPath` lists `pre-push`.
- The brief is in the tree; the pointer read. The host file's last block (12:54, the M6 coordinator) says M6 holds the host, census qemu 0; `pgrep -c -x qemu-system-x86` 0 now. This slice needs no runtime and starts none.
- `df -i /tmp` 40 % (632,359 inodes free); `df -i /workspace` 20 %. No whole-tree export is planned; one would go under `/workspace/tmp/m6-t24/`.
- `gh api rate_limit`: core **4,576 / 5,000** at 13:38.

### [Stage A] 13:38-13:41 — Scope re-derived

- **Counts** (brief § 2's filter, `python3 -I`, output kept in `.qa-scratch/t24/membership.txt`): **86 paths, 2,399 lines; 86 upstream-carried; 84 `unreached`, 2 `unshipped`; languages recipe 85, cmake 1; 81 under `packages/emulation`, 5 under `projects`; 12 recipes with patches; 0 shadowed; 0 spaces**. `unshipped`: `boom3-lr` and `vitaquake3-lr`, `buildable_by` `AMD64-x86_64`. `paths.txt` 86 lines, `recipes.txt` 85. **No delta** from the brief or #671.
- **Provenance:** `git diff --name-status c445081a59 8ebaf8daad -- <86>` prints 0 lines (the fork changed none). Against `e0f9deb899` and against `481c9d0d75`: `5 M` each, the five ROCKNIX recipes. `git log c445081a59..e0f9deb899 -- <86>`: one commit, `af70bd435b` (*libretro-cores: add retroarch as PKG_DEPENDS_TARGET*); `e0f9deb899..481c9d0d75 -- <86>`: none.
- **Last touches:** `libretro-snes9x` `2dd698ba24` 2026-06-02; among the 81 LibreELEC files `e46157185c` 2026-07-22 (*libretro-cannonball: update to githash 65cb1f5*), the brief's; among all 86 `9cdcb3d437` 2026-09-03 (*libretro: update licenses*, on the five ROCKNIX recipes).
- **Branch vs hash:** `git diff --stat 8ebaf8daad HEAD -- <86>` prints nothing. The slice's bytes are `next`'s; `reviewed-at: 81331b499e`.
- Recorded in `01-research-notes.md` § Scope. Stage B starts at the reachability commands of brief § 5.
