# Running Log — M6.P2 T6, upstream's helper tools and the other distributions

**Issue:** #653 (`M6.P2 E800/T6`), slice `build-engine-upstream-tools` (`k: 6`); epic #800; renovation #339; milestone M6
**Brief:** `docs/reviews/briefs/build-engine-upstream-tools.md` version 2 (`3d60062ce5`); its § 7 is the contract, identical to #653's sixteen criteria
**Executor:** Claude Code, `anthropic/claude-opus-5-5` (Opus 5.5) at high effort; the T5 session `c649553c-8086-4db7-ad9c-248c7e41ff95`, herdr agent `m6-t5-build-engine`, pane `wN:p7` (the dispatch, issuecomment-6381781507)
**Skill:** code-auditor at epic tier, the renovation face (plan § 6b); depth **Local** (plan § 6c, D-WORKFLOW-184): no reviewer, no Facilitator call, no `npm install`
**Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-upstream-tools-653`, branch `feature/m6-build-engine-upstream-tools-653`
**Read hash:** the slice's bytes are `next`'s `8ebaf8daad`; **`reviewed-at` = `b96e1ca761`** (the branch `HEAD` at stage A; the commit carrying this log changes no slice path); `upstream/next` `e0f9deb899` at the fetch (T5 read `3421d7d178`: upstream moved; Q4 is read against the fetched tip)
**The bench:** the tree at the hash (`.qa-scratch/t6/at-hash`, an export of `tools` and `distributions`), the record (`git log`, the documents), and the M7 build roots read only through the filter. **No runtime of any kind**: no guest, no build, no compiler; a tool is read to learn its reach, never run (`distro-tool`, `download-tool`, `imgburn.sh` write)
**Can this be done on the VM?** **No** -- a reachability table over tools and files that are not on an image (brief § 5, #653's body)

Every time below is a `date -u` reading taken in the command that wrote it.

---

### [Stage A] 08:05 to 08:08 — Scope

- Read, in the order the dispatch gave:
  - the lane pointer;
  - `next:AGENTS.md` (§ The rules that bind, § Non-obvious gotchas, § The checks to run before a push);
  - `docs/reviews/plan-for-the-plan.md` whole;
  - the brief whole (version 2);
  - #653's body and the dispatch comment;
  - the futro's T6 addendum (`docs/futros/2026-10-24-m6-build-engine.md` 370 on);
  - #644 finding 24 (`docs/reviews/build-path-read.md:177`).
  - The rules: `next`'s are loaded this session. `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` lists the seven paths of brief § 1 and nothing else (`engineering-practices.md`, `fork-workflow.md`, `generic-x64-vm-testing.md`, `instruction-files.md`, `templates.md`, `council/IMPORTED-FROM.md`, `tools/lint-audit-artifacts`).
- The first commands (08:06:59):
  - `df -i /tmp` 40%;
  - the branch, stacked on `2174265e9c`;
  - `inventory.json` present;
  - the at-hash export: 267 files, under `.qa-scratch/t6/at-hash`, not `/tmp`;
  - P1's tools present;
  - `rules-check` rc 0; `register-check` rc 0 (662 IDs);
  - `ceremony-check` rc 1, `OVERDUE: 2026-W42 summary` (M7's week, not this lane's);
  - the push: up to date;
  - the host file's tail read for the protocol (no hold; M6 runs sandboxes only).
- **The scope, re-derived with brief § 2's filter:** 135 paths, 7,369 lines; upstream-carried 134, fork-own 1; reach `n/a` 108, `unreached` 27. Languages: shell 37, none 66, image 17, docker 6, python 3, other 2, config 1, font 1, markdown 1, symlink 1. All equal to the brief's. `.qa-scratch/t6/paths.txt` holds the path column.
- **Branch against the hash, over the 135:** `git diff --stat 8ebaf8daad HEAD -- $(cat paths.txt)` is empty.
- **Over the two roots whole:** 15 files, every one fork-only and outside the 135. P1 added `tools/renovation-inventory` (`00ca350666`), `renovation-status` (`af24589b1c`), `renovation-drift` (`a7cbde1737`), `register-check` (`f00ab3e163`), and the ten `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-{pass,fail}/` files (`fc88815ccb`). The coordinator's tip carried `tools/lint-audit-artifacts` (#810, merged at `e84180386d`).
- **Q4, the upstream-state loop over the 135:** 1 `differs` (`tools/pkgcheck`), 134 identical (08:07:43).

### [Stage B] 08:08 to 08:23 — Phase 1 to 4: the searches, the fixture, the tables

- **Phase 1:** #644 finding 24 read whole; T5's rows for `update_packages`, `multithread` and `build`, and its Q6 Tables 1 and 4, read with `git show` from `feature/m6-build-engine-652`; the five blindspots; the rules (`01` § Phase 1).
- **§ 5's checks**, each in `02` § Mechanical checks:
  - the two-way caller count for the 24 single tools (08:09:06); every zero searched the second way;
  - the `update-functions` and `DISTRO=` greps (08:09:58);
  - the syntax sweep (shell 37 of 37, helpers 61 of 61, Python 3 of 3; shellcheck absent);
  - `pkgcheck`'s tier (08:11:45);
  - the M7 roots read only: no `release/` directory, no other distribution's root; 0 of 28 `linux` builds printed the kernel-options message;
  - the git-writing tools' subjects: none.
- **The fixture** `tools/fx-pkgcheck.sh` (08:12:31), the only tool run: `pkgcheck`, a reader, over a fixture tree. It gives F-02.
- **Found by reading a reached tool:** `adjust_kernel_config:38` calls `check_kernel_config`. **Found by the export:** `distributions/LEIoT/kernel_options` dangles (F-03).
- **The tables:**
  - `tools/t6-tables.py` generates `02`'s coverage table (135 rows), `04`'s Q6 (33 rows, files summing to 135) and `04`'s Q4 (135 rows) from one list.
  - The criterion's `grep -c` first printed 140: five lines outside the table began with a backticked path. A fix of mine over-matched to 131; corrected to **135**.
  - The generator's first run stopped on its own assertion, which I had written too strictly (it required `Already written:` on a document-reached row); narrowed to the unreached rows.
  - I wrote "Python 2-era" for `distro-tool` without evidence; its shebang is `#!/bin/bash`. Corrected before any commit.
  - Two claims in `03` corrected after a check: the README's line range for `pkgcheck`, and that the mirror workflow copies upstream's container with `skopeo` rather than building the root `Dockerfile`.
- **Six findings, none above Low:** F-01 and F-05 doctrine (for T4); F-02 a `bug`; F-03 a #585 line; F-04 and F-06 `Renovation`. Phase 4.5 in `04`: one verdict changed (`check_kernel_config` to reached), none withdrawn.
- `git status --short -- tools distributions` is empty; no file under the two roots has changed.

PROOF: 08:09 P1 the two-way caller count for the 24 single tools, `pkgcheck` and `adjust_kernel_config` the positive controls -- `.qa-scratch/t6/callers-two-way.txt`
PROOF: 08:10 P2 every zero searched by bare name in the documents and inside the slice; `adjust_kernel_config:38` calls `check_kernel_config`
PROOF: 08:09 P3 the 62 helpers are sourced only by `tools/update-pkg:70,167`
PROOF: 08:09 P4 `config/options:24` is the only `DISTRO` setter
PROOF: 08:10 P5 shell 37 of 37 and helpers 61 of 61 `bash -n` ok; Python 3 of 3 parse
PROOF: 08:11 P6 `tools/pkgcheck` carries one fork commit, `81221658b3`, and upstream has not touched it since the base
PROOF: 08:12 P7 `tools/pkgcheck` exits 0 for a name no recipe matches, as for a clean recipe -- `tools/fx-pkgcheck.sh` (F-02)
PROOF: 08:12-08:23 P8 `distributions/LEIoT/kernel_options` is a dangling symlink, LibreELEC's since `4130b59b50` (F-03)
PROOF: 08:12-08:23 P9 the twelve `update to` commits carry a trailer `update-pkg` never writes
PROOF: 08:07 P10 Q4 over the 135: 134 identical, 1 differs

### [Stage C] 08:23 to 08:24 — Local depth: Phase 4.5 only; `05`; the pre-issue lint

- Phase 4.6 does not apply at Local depth (plan § 6c, D-WORKFLOW-184). `second-opinions/review-plan.json` carries `tier_exception` and `reason`; no call, no provenance file. Phase 4.5 is in `04`, every verdict asked what would make it false.
- `05-punch-list.md` from `tools/punch-items.py`: 6 items, all Low; PL-01 for a `bug`; PL-02 the #585 item; PL-03 for #585; PL-04 and PL-05 for #651; PL-06 for #657.
- `tools/lint-audit-artifacts docs/audits/2026_10_24-epic-m6-build-engine-upstream-tools --phase pre-issue`: **`PASS pre-issue artifacts (does not certify resolution)`**, with `ok    review-plan: local at epic tier under D-WORKFLOW-184 (plan § 6c: a reachability table is Local ...)`.

### [Stage D] 08:24 to 08:25 — The bug and the audit issue filed; the pause

- PL-01's bug **#845** (`Bug: tools/pkgcheck exits 0 when no recipe matches the package name`, label `bug`, no milestone): the code trace, `Already written:`, the VM line, two agent-verifiable checkboxes. `tools/box-check --issue 845`: 2 open, 0 fail.
- The audit issue **#846** (`Audit: M6 T6 upstream's helper tools and the other distributions -- 6 findings (0 critical, 0 high)`): labels `audit` and `punch-list`, milestone M6, a sub-issue of #653 (read back), one checkbox per item. `tools/box-check --issue 846`: 6 open, 0 fail.
- `05` carries `tracked: "#845"` and #846. The lane pauses for the coordinator's stream briefs (plan § 6b E) and edits nothing of the 135; `git status --short -- tools distributions` is empty.

### [Stage E] 08:30 to 08:42 — S1 (#845) and S2 (PL-06), from the coordinator's stream briefs (`t6-streams.md`)

- **The sweep before** (08:30:02 to 08:30:35): `tools/pkgcheck` at `8ebaf8daad`, no argument, over this worktree, whose `packages/` and `projects/` equal the hash. It exits 1 with 12 FAIL lines and 43 WARN lines. The brief expected 0 FAIL lines. These 12 already fail on real recipes, so each stream reports a delta; `02` § Leads from the sweeps reads each line.
- **S1, `7fa8bafba4`:** an argument that reaches no recipe is named on stderr, and the run exits 2. The fixture before and after is P11. The sweep after S1 shows the same 12 lines (08:32:50 to 08:33:23).
  - The fixture took a relative scratch path, so its first run (08:32:35) failed on its own stderr file and printed exit 1 for every case. That run is discarded; the script now resolves the path first.
- **S2, `44f64842b6`:** 18 names added to the late-binding list, derived from `config/options:185,197`, `source_package`, `setup_toolchain` and `scripts/build:137,140` (P14).
  - **Two names left off, against the stream brief's example list.** `TOOLCHAIN` is set before the recipe loads and is never reset. `SYSROOT_PREFIX` changes only after `post_make`; the trial sweep with it listed gave 87 FAIL lines, 66 of them on correct configure options.
  - The commit message's count of the new lines was amended before any push. It is unpushed; the remote is at `8b65f77482`.
  - The fixture's two new cases are P12. The sweep after S2 gives 21 FAIL lines (P13). Ten lines are new; one of them replaces `wireplumber:100`'s earlier line. Of the ten:
    - 3 real (`systemd:105`, `virtual/image:109,110`);
    - 7 false, from the heredoc parser (14 of all 21 lines are the parser's).
- **Records corrected:** `03` § 3.2 and § 3.5, from S2's derivation (`TOOLCHAIN` is not late). `05` is regenerated with the Phase 7 outcomes: PL-01 and PL-06 Resolved; PL-02 and PL-03 deferred to #585; PL-04 and PL-05 deferred to #651.
- `git status --short -- distributions` is empty; under `tools/`, only `tools/pkgcheck` changed. `git diff --diff-filter=D --name-only 8ebaf8daad HEAD -- tools distributions` is empty.

PROOF: 08:32-08:38 P11 `tools/pkgcheck` exits 2 for a name no recipe matches, after S1; 0 before -- `tools/fx-pkgcheck.sh` (#845)
PROOF: 08:38 P12 a global `${INSTALL}` FAILs after S2 and passed before; global `${TOOLCHAIN}` and `${SYSROOT_PREFIX}` pass throughout -- `tools/fx-pkgcheck.sh`
PROOF: 08:30-08:39 P13 the sweep over every recipe: FAIL 12, 12, 21; WARN 43 throughout; exit 1 each time
PROOF: 08:33-08:36 P14 the late names derived from where the build sets them; `TOOLCHAIN` never reset; `SYSROOT_PREFIX` reset after `post_make`, its 66 global uses correct
