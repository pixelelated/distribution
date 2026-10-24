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

### [Stage B] 13:42-13:52 — The brief § 5 checks (times from each output file's mtime; this entry written 13:57 UTC)

- **The (b) loop's first run read nothing.** I ran § 5's commands one at a time and skipped the block's `mkdir -p .qa-scratch/t24/le .qa-scratch/t24/probe`, so every `2>.qa-scratch/t24/le/err` failed and bash ran no `gh`. All 80 rows said `not-read` (`q4b-run1-noread.txt`, 13:43:14), which is the loop's fail-closed branch, so no row claimed `identical`. The second run, with the folders made, read 80 of 80. Friction line, 13:53.
- **`tools/viewplan --help`** has no help: it ran `genbuildplan.py` with no build target and printed its usage (rc 2, `xargs: scripts/pkgjson: terminated by signal 13`). It wrote nothing tracked (`git status --short` empty). The three device reads take the device from the environment, as § 5 says.
- **`tools/pkgcheck` with no argument** walks every recipe in the tree; `head -3` cut it off at 13:46:54. `pgrep` shows no survivor. The runs below name each recipe.
- **Plan lines:** a target step reads `install snes9x-lr` with no suffix, a host step `build make:host`. § 5's `awk '$2==n'` sees target steps only, so a second, wider column counts the name with any `:<kind>` suffix or inside any `wants:` list. The control reads 3 and 6.
- **The HEAD probe cannot see a dead commit.** Without `-L`, `github.com/<o>/<r>/archive/<sha>.tar.gz` answers `302` for a commit that does not exist (`0000…` on `libretro/snes9x`), and `404` only for a repository that does not exist. So the probe's 85 answers prove the repository, not the pin. For the five ROCKNIX recipes, T3's Q4 read each pin's commit date through the API; for the 81, nothing builds them. Recorded as the probe's limit, never as a pass of the pin.
- **The metapackage's two hits** for `boom3-lr` and `vitaquake3-lr` are `package.mk:1768`, the fork's `core-pins` list (`3a56a04f8b`, #21), not an `add_emu_core`. All three install trees' `core-pins` carry both rows, while no image holds either `.so`. `cloud_capture:121` is the file's one reader. F-03.

PROOF: 13:39 P1 the membership, brief § 2's filter: 86 paths, 2,399 lines, 86 upstream-carried, 84 `unreached` and 2 `unshipped`, 85 recipes and 1 cmake file -- `.qa-scratch/t24/membership.txt`
PROOF: 13:41 P2 provenance: `git diff --name-status c445081a59 8ebaf8daad -- <86>` 0 lines; `git log c445081a59..e0f9deb899 -- <86>` one commit, `af70bd435b`
PROOF: 13:41 P3 the branch against the hash: `git diff --stat 8ebaf8daad HEAD -- <86>` empty
PROOF: 13:42 P4 (a): 81 identical and 5 differs at `e0f9deb899` and at `481c9d0d75`, the two files equal (`cmp`); the control `virtual/emulators/package.mk` (fork-changed) reads differs -- `q4a-*.txt`
PROOF: 13:44 P5 (b): 80 of 80 read from LibreELEC master (budget 4,450 before, 4,339 after; the other 31 calls were shared monitors); 74 pin identical (13 of them file-identical, 61 adding only a version-stamp hunk), 6 pin moved, 0 absent, 0 not-read; the control `libretro-snes9x` reads moved (`185488cd83` against `fae2fea08f`) -- `q4b.txt`, `q4b-compare.txt`, `q4b-diffshape.txt`
PROOF: 13:45 P6 the plans: `tools/viewplan` rc 0 for GENERIC_X64 (654 steps), H700 (665), SM8550 (737); 0 of the 85 names in any plan, narrow or wide; the control `snes9x-lr` 3 and 6, `mgba-lr` 3 and 6 -- `plan-*.txt`, `reach.txt`
PROOF: 13:45 P7 the metapackage: 83 of the 85 names on no line; `boom3-lr` and `vitaquake3-lr` on one line each, `package.mk:1768` (the `core-pins` list); `idtech-lr` is skipped for GENERIC_X64 (`package.mk:111`) -- `reach.txt`
PROOF: 13:52 P8 the build edges: `git grep -l` of `PKG_DEPENDS*` lines naming each of the 85: 81 names with an edge (79 from 78 Kodi `game.libretro*` recipes, all `unreached`; 2 from `idtech-lr/package.mk:21`, under `TARGET_ARCH = x86_64`); `cyclone68000`, `mame2003-lr`, `panda3ds-lr` and `play-lr` with none -- `edges.txt`
PROOF: 13:46 P9 the record: `ls` of the five M7 roots' `build/` (579, 600, 233, 659 and 237 entries); 85 of 85 names with no build directory by `^<name>-[A-Za-z0-9]`, and none by a bare `^<name>` prefix; the controls `snes9x-lr-890b5d4455…` and `mgba-lr-e31759b24e…` in the three 64-bit roots -- `listing-*.txt`, `record.txt`
PROOF: 13:46 P10 the `.info` trace: in the GENERIC_X64, H700 and SM8550 install trees, `boom3`, `boom3_xp`, `vitaquake3`, `mame2003`, `panda3ds` and `play` each have a `.info` and no `.so` (320 `.info` per tree); the control `snes9x` has both
PROOF: 13:48 P11 `core-pins`: the three install trees' `/usr/share/rocknix/core-pins` (128, 137 and 159 lines) each carry `boom3-lr 0bea79abf5…` and `vitaquake3-lr 8ab09d1f54…`; its one reader is `cloud_capture:121`
PROOF: 13:47 P12 `pkgcheck`: the tree's copy and T6's `44f64842b6` copy, 85 PASS each, the same 2 WARN lines (`libretro-beetle-pcfx:24`, `libretro-bsnes-hd:19`, intertwined vars and funcs); every name matches exactly one recipe (T6's F-02: an unmatched name exits 0); the control `/workspace/tmp/m6-t24/pkgcheck-control` (a global `${PKG_BUILD}`) exits 1 under both copies with `late binding violation`
PROOF: 13:48 P13 the weight: the 81 are 81 files, 2,258 lines, 86,663 bytes; the 5 are 141 lines, 4,889 bytes; `packages/emulation` whole 97 files, 106,103 bytes, 16 of them T40's patches (19,440 bytes)
PROOF: 13:49 P14 Q1: the 85 resolved `PKG_URL`s are all `https://github.com` (83 archives, 2 `.git` clones) -- `urls.txt`
PROOF: 13:50 P15 Q3: HEAD without `-L`: 83 answer 302 and 2 answer 301, 0 other; the controls: a nonexistent commit answers 302 and a nonexistent repository 404, so the probe proves the repository only -- `probe/head.txt`
PROOF: 13:48 P16 the twin map: 77 LibreELEC cores; 52 twin by name and source, 5 by name only, 10 by source only, 10 none; 12 twins at LibreELEC's pin -- `twin.json` from `tools/t24-twin.py`, `tools/t24-tables.py q7`
PROOF: 13:51 P17 the five ROCKNIX pins against their projects: T3's `04-analysis.md:227, 284, 303, 307, 354` at `b3cb4ec8c5` (`git show`), each `behind-project` with upstream `same` and a pin commit date

### [Stages B-C] 13:53-14:08 — 02 to 05 written; the pre-issue lint (this entry 14:05 UTC)

- `02-forward-audit.md` has:
  - § Mechanical checks, 20 rows;
  - the reachability reads together;
  - F-01 to F-03, and the leads;
  - § Proofs P1 to P17;
  - the criterion entries;
  - the coverage table, 86 rows (`grep -c -E '^\| `(packages|projects)/'` prints 86).
- `03-retrospective.md` covers § 3.1 to § 3.5 (four seams) and the futro's T24 addendum checked item by item.
- `04-analysis.md` carries all of the skill's sections and the renovation face:
  - Q6's 86-row table, each row with its `Already written:` (86);
  - Q7's 77-row twin map;
  - Q4 (b)'s and Q7's **Total** rows, which the lint sums;
  - Phase 4.6 as not applicable, citing D-WORKFLOW-184.
- `05-punch-list.md` holds PL-01 to PL-03 (all Low, all `Renovation`, Q6), each `Open`, with the `punch_index`. `second-opinions/review-plan.json` is Local, with `tier_exception: D-WORKFLOW-184`.
- **The tables are generated:**
  - `tools/t24-tables.py <scratch> coverage|q6|q7` asserts 86, 86 and 77 rows and no empty cell;
  - `tools/t24-twin.py <export>` writes `twin.json`. It was moved from the scratch folder into the audit's `tools/`, and its by-name duplicates are now removed in the script rather than afterwards; the three tables regenerated byte-identical (`cmp`).
- **Corrected while writing, before any commit:**
  - `03`'s futro table was first written from memory of brief version 2 (A1 to A6 as errata), then replaced from the addendum (`docs/futros/2026-10-24-m6-emulators-and-cores.md:489-582`), whose A1 to A6 are adjustments;
  - "79 Kodi recipes" became 79 edges from 78 recipes (P8 corrected);
  - three generalisations in `04` § Q7 were narrowed to what P8 and the source reads show.
- `tools/lint-audit-artifacts <folder> --phase pre-issue` (14:04:26): rc 0, `PASS pre-issue artifacts (does not certify resolution)`, with `review-plan: local at epic tier under D-WORKFLOW-184 (...)` and `04 § Renovation face answers Q1 to Q7`.
- Proof count: 17 `proved:` cells in `02`, 17 proof lines here.

### [Stage D] 14:08-14:07 — the punch-list issue; the pause

- **#900** `Audit: M6 T24 emulator recipes and files no shipped image builds -- 3 findings (0 high, 0 medium, 3 low)` was created with labels `audit` and `punch-list`, milestone M6, and attached as a sub-issue of #671 (REST id 6013783886). Read back: the title, both labels, the milestone, and 3 open checkboxes.
- `tools/lint-audit-artifacts <folder> --phase pre-issue --issue 900`: `PASS pre-issue artifacts`, with `issue #900 carries a task list (3 items)` and PL-01 to PL-03 referenced.
- `tools/box-check`: rc 0; `300 issue(s), 825 open checkbox(es), 0 fail`. #900 and #671 are not among its notes.
- **The stage-D pause:** the dispositions for PL-01 to PL-03 are asked on #671. The lane is idle on this slice until they come.
