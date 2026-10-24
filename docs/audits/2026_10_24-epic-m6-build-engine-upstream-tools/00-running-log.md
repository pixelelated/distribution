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
