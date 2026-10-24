# Running Log — M6.P2 T8, the image's own packages (projects/ROCKNIX)

**Issue:** #655 (`M6.P2 E848/T8`), slice `image-packages` (`k: 8`); epic #848; renovation #339; milestone M6
**Brief:** `docs/reviews/briefs/image-packages.md` version 2 (`dede8effec`); its § 7 is the contract, identical to #655's eighteen criteria
**Executor:** Claude Code, `anthropic/claude-opus-5-5` (Opus 5.5) at high effort; the T5 session `c649553c-8086-4db7-ad9c-248c7e41ff95`, herdr agent `m6-t5-build-engine`, pane `wN:p7` (the dispatch, issuecomment-6384032445)
**Skill:** code-auditor at epic tier, the renovation face (plan § 6b); depth **Independent** (D-WORKFLOW-184): one GPT-6 Astra seat at `max` through the Facilitator, a probe then one refutation over one bounded packet; the dispatch authorizes the two calls; a failed seat is a hold
**Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-image-packages-655`, branch `feature/m6-image-packages-655`
**Read hash:** the slice's bytes are `next`'s `8ebaf8daad`; **`reviewed-at` = `caf1de3727`** (the branch `HEAD` at stage A; the commit carrying this log changes no slice path); `upstream/next` `e0f9deb899` at the fetch (12:10)
**The bench:** the recipes, scripts, units and configs at the hash (`.qa-scratch/t8/at-hash/`), `upstream/next`, the hosts `tools/fork-package-freshness` reads, the GitHub API's `compare`, one HEAD probe per effective URL, ROCKNIX's mirror, the shared source cache's stamps, and the five M7 roots' `build/` listings and GENERIC_X64 install tree, read only. A guest only for a stage-E behaviour claim
**Can this be done on the VM?** **Yes, for every behaviour claim** (a stream's unit, script or install step, on the GENERIC_X64 guest); **no guest for the reading or the tables** (brief § 5)
**Prose:** written through Python or a quoted heredoc only (plan § 6b E; T7's incident)

Every time below is a `date -u` reading taken in the command that wrote it.

---

### [Stage A] 12:10 to 12:12 — Scope

- **Read**, in the order the dispatch gave: the dispatch comment on #655 (12:09, with T6's 08:57 lead before it); the lane pointer; `docs/reviews/plan-for-the-plan.md` (read whole for T7; its one change since, the stage-E row's three new bullets, read word by word with `git diff --word-diff e7978a1ca5 HEAD`); the brief whole (version 2).
- **Rules:** `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` lists exactly the dispatch's eight paths (127 insertions, 11 deletions).
- **The first commands** (12:10:46 to 12:10:58):
  - `git fetch`: rc 0; `upstream/next` is `e0f9deb899`;
  - the branch is stacked on `2174265e9c`; `inventory.json` is present;
  - `df -i`: `/workspace` 20%, `/tmp` 41%;
  - the at-hash export of `projects/ROCKNIX/packages`: 2,614 files under `.qa-scratch/t8/at-hash` (gitignored), rc 0;
  - P1's tools are present;
  - `rules-check` rc 0; `register-check` rc 0 (664 IDs); `ceremony-check` rc 1 on `OVERDUE: 2026-W42 summary missing` (M7's week, not this lane's);
  - the push set the upstream;
  - the host file's tail read (the coordinator's 10:36 correction on `portaudio`; census qemu 0);
  - the API budget: 4,007/5,000;
  - `~/.config/council/env` is present (not read).
- **The scope, re-derived** with brief § 2's filter on `inventory.json` (`00ca350666`). **All equal to the brief's: no delta:**
  - **485 paths, 20,644 lines**: upstream-carried 450, fork-own 35; reach `shipped` 478, `test` 6, `n/a` 1;
  - **260 recipes** (27 fork-own) in the brief's 22 groups; 60 with patches;
  - **14 paths contain spaces, and none of them is a recipe.**

  The full listing is `.qa-scratch/t8/scope-out.txt`.
- **Branch against the hash, over the 485** (`xargs -0`): empty.
- **Provenance by git:**
  - against the base: 11 A, 24 M (the fork's 35);
  - against `upstream/next`: 31 A, 87 M;
  - the absent recipes: **11 orphans, 7 fork-added**;
  - 40 upstream commits on these paths since the base; 66 recipes changed upstream;
  - `fork-package-freshness --list` under `projects/`: 34;
  - the conflict set (fork-changed ∩ upstream-changed since the base): **11**, as the brief has it.
- **A T7 erratum found here:**
  - **What T7 wrote:** `docs/audits/2026_10_24-epic-m6-generic-packages-reached/` (`05`'s PL-12, `tools/punch-items.py`) and its retro called six of the 47 sourcing overrides *orphans ROCKNIX deleted*.
  - **The fact:** three of the six (`harfbuzz-icu`, `gst-plugins-bad`, `gnutls`) are **fork-added**, absent at the base too; only `libfreeaptx`, `opus` and `libfmt` are orphans. T7's check read `upstream/next` alone, not the base.
  - **Where it is recorded:** `01` § T7 erratum here; reported on #655, since T7 is accepted and its folder is not this lane's to edit.
