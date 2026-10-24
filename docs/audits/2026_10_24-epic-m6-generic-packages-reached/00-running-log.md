# Running Log — M6.P2 T7, the generic packages the image builds

**Issue:** #654 (`M6.P2 E848/T7`), slice `generic-packages-reached` (`k: 7`); epic #848; renovation #339; milestone M6
**Brief:** `docs/reviews/briefs/generic-packages-reached.md` version 2 (`e7978a1ca5`); its § 7 is the contract, identical to #654's seventeen criteria
**Executor:** Claude Code, `anthropic/claude-opus-5-5` (Opus 5.5) at high effort; the T5 session `c649553c-8086-4db7-ad9c-248c7e41ff95`, herdr agent `m6-t5-build-engine`, pane `wN:p7` (the dispatch, issuecomment-6382955786)
**Skill:** code-auditor at epic tier, the renovation face (plan § 6b); depth **Local** (plan § 6c, D-WORKFLOW-184): no reviewer, no Facilitator call, no `npm install`
**Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-generic-packages-reached-654`, branch `feature/m6-generic-packages-reached-654`
**Read hash:** the slice's bytes are `next`'s `8ebaf8daad`; **`reviewed-at` = `4ea87f17dd`** (the branch `HEAD` at stage A; the commit carrying this log changes no slice path); `upstream/next` `e0f9deb899` at the fetch (10:12)
**The bench:** the recipes at the hash (`.qa-scratch/t7/at-hash/packages`, an export of `packages`), `upstream/next`, LibreELEC master through the GitHub contents API (no remote added), the hosts `tools/fork-package-freshness` reads, one HEAD probe per `PKG_URL`, the shared source cache's `.sha256` stamps and the five M7 roots' `build/` listings, read only. **No runtime of any kind**: no guest, no build, no compiler; no pin moved, no recipe deleted or relocated
**Can this be done on the VM?** **No** -- a currency table over recipes; its bench is the tree, the record and the release sources, all read from the host (brief § 5, #654's body)

Every time below is a `date -u` reading taken in the command that wrote it.

---

### [Stage A] 10:12 to 10:14 — Scope

- Read, in the order the dispatch gave: the dispatch comment on #654 (10:11, with the 08:57 lead and the 10:09 correction before it); the lane pointer; `docs/reviews/plan-for-the-plan.md` whole; the brief whole (version 2).
- **The rules:** this worktree's are `next`'s except seven: `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` lists `engineering-practices.md`, `fork-workflow.md`, `generic-x64-vm-testing.md`, `instruction-files.md`, `code-auditor/references/templates.md`, `council/IMPORTED-FROM.md` and `tools/lint-audit-artifacts` (115 insertions, 11 deletions), the dispatch's seven and nothing else.
- **The first commands** (10:12:33 to 10:12:55):
  - `git fetch origin`, `git fetch upstream --no-tags`: rc 0; `upstream/next` `e0f9deb899`;
  - the branch `feature/m6-generic-packages-reached-654`, stacked on `2174265e9c`; `inventory.json` present;
  - `df -i`: `/workspace` 19%, `/tmp` 40%;
  - the at-hash export: `git archive 8ebaf8daad packages` into `.qa-scratch/t7/at-hash` (gitignored), 2,546 files, rc 0; not under `/tmp`;
  - P1's tools and `slices.json` present;
  - `rules-check` rc 0; `register-check` rc 0 (662 IDs); `ceremony-check` rc 1, `OVERDUE: 2026-W42 summary missing` (M7's week, not this lane's to pay);
  - the push: up to date, `HEAD` = `origin` = `4ea87f17dd`;
  - the host file's tail (the coordinator's 09:08 retention note on `portaudio`'s cache copy, #849; M6 holds the host; no runtime here);
  - the API budget: 4,291/5,000.
- **The scope, re-derived with brief § 2's filter** on `docs/reviews/inventory.json` (`00ca350666`): **266 paths, 7,612 lines**; upstream-carried 250, fork-own 16; reach `shipped` 256, `test` 7, `n/a` 3; **243 recipes** in the twenty groups of the brief (devel 45, x11 34, addons 25, sysutils 17, audio 16, graphics 16, python 15, network 14, textproc 10, compress 9, security 9, multimedia 7, tools 6, virtual 6, web 5, debug 3, lang 2, wayland 2, databases 1, print 1); 46 with patches; 0 shadowed. Languages: recipe 243, other 6, shell 4, cmake 3, config 3, udev 2, none 2, markdown 1, text 1, systemd 1. **All equal to the brief's: no delta.** `.qa-scratch/t7/paths.txt` (266) and `recipes.txt` (243) hold the columns; the full listing is `.qa-scratch/t7/scope-out.txt`.
- **The generic recipes outside the excluded trees:** 942 at `8ebaf8daad`; the 243 are those a shipped or test plan reaches, the other 699 T23's.
- **Branch against the hash, over the 266:** `git diff --stat 8ebaf8daad HEAD -- $(cat .qa-scratch/t7/paths.txt)` is empty.
- **Provenance by git** (10:13): `--diff-filter=A` against the base `c445081a59`: 13, every one absent on `upstream/next` (`fork-only` 13); `--diff-filter=M`: 3 (`libyaml`, `libsamplerate`, `syslinux`); so 227 untouched. Over all of `packages/` against `upstream/next`: 16 A, 5 M (#645's 21 files). `tools/fork-package-freshness --list` under `packages/`: 13, and the `diff` against the fork-added 13 is empty (rc 0). `git log c445081a59..upstream/next -- packages/`: 0 commits of 325.
