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
