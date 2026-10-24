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

### [Stage B] 10:15 to 10:41 — Phases 1 to 4: the three sources, the sweep, the record

- **Phase 1:**
  - **Read from this worktree:** `packaging-and-patches.md`.
  - **Read whole:**
    - `tools/fork-package-freshness`, for its hosts and six classes;
    - `tools/viewplan`;
    - `scripts/update_packages`, whose `PKG_PATH` is set at `:16`;
    - `tools/update-pkg`, whose `sed -i` is at `:26`; it is on the never-run list;
    - `tools/pkgcheck`.
  - **Read:**
    - #644 findings 15, 16 and 17 (`docs/reviews/build-path-read.md:168-170`);
    - blindspots 46, 51 and 75;
    - the futro's § 4 and § 5 (S-1 to S-12, A1 to A9).
  - **Read with `git show`:**
    - T5's `get_archive` at `52e6794ba7`;
    - T3's `q4-pins.json` and `q4-pins-table.md` (`8dbe5762bc`);
    - T6's table generator.
  - **Rules:** the ones loaded this session are `next`'s, by the stage-A diff.
- **§ 5's checks**, each in `02` § Mechanical checks with its exit status:
  - (a): 10:15:47;
  - (b): 10:15:57 to 10:19:05. The budget was 4,261, reset at 10:18:26, and read 4,949 at the end;
  - (c): 10:19:34 to 10:19:39, rc 1;
  - the hash pins: 10:20:04 to 10:20:15;
  - the HEAD probe: 10:20:44 to 10:23:08;
  - the checksum count: 10:20:53;
  - both `pkgcheck` runs: 10:21:01 to 10:21:40;
  - `viewplan`, five plans: 10:22:45 to 10:22:49;
  - the stamps;
  - the redirect fetch: 10:25:09 to 10:30:34;
  - the controls: 10:25:59;
  - the five plans' expansions: to 10:28:36;
  - the mirror: 10:31:16 to 10:31:19;
  - the 23 other paths against LibreELEC;
  - the GitHub owners: budget 4,642 → 4,548.
- **Deltas from the brief:**
  - **`ntfs-3g_ntfsprogs` is built.** The brief's `sed` cuts its name (`03` § 3.3).
  - **D-WORKFLOW-194 is one short.** The archive versions without a checksum, counted as built, are one more than it says: `libfmt`, F-01.
  - **47 sourcing overrides** that `shadowed_by` does not record, F-12.
- **Checkpoint on #654** at 10:32 (issuecomment-6383149193).
- **Written:**
  - `02`: the 266-row coverage table, § Mechanical checks, § The fetch sweep, § The #644 findings, and P1 to P13;
  - `03`: § 3.1 to 3.5, and the futro checked;
  - `04`: Phase 4.5 for each finding, and the renovation face with the 243-row Q4 table and the 16 Q7 rows;
  - `q4-table.md`, `q4-pins.json` and `tools/t7-tables.py`.

  One script builds the tables and asserts 266 and 243.

PROOF: 10:14 P1 the slice is the brief's 266 paths and 243 recipes; the branch differs from `8ebaf8daad` on none -- `01` § Scope
PROOF: 10:13 P2 13 fork-added (all absent upstream), 3 edited, 227 untouched; the freshness tool's set is the 13 -- `prov-added.txt`, `fresh-list.txt`
PROOF: 10:15 P3 (a): 227 identical, 3 differs, 13 absent-upstream; the 16 the control -- `q4a.txt`
PROOF: 10:19 P4 (b): 230 read, 13 absent, 0 not read; 61 behind LibreELEC master -- `le/`, `q4b.txt`
PROOF: 10:20 P5 (c): 4 BEHIND, 9 CURRENT (rc 1); the 7 GitHub hash pins' distances -- `q4c.txt`, `q4c-hash.txt`
PROOF: 10:28 P6 `libfmt` 9.1.0's effective `PKG_SHA256` is empty in three plans, the only empty checksum in the tree -- `probe/expand-<plan>.txt`
PROOF: 10:21 P7 `pkgcheck` 243 PASS with both copies; `sameboy-lr` fails both -- `pkgcheck-*.txt`
PROOF: 10:26 P8 the HEAD histogram; the controls answer 301 and 404 -- `probe/head.txt`, `probe/controls.txt`
PROOF: 10:31 P9 129 of 132 redirected archives match; the mirror serves the four gone sources' bytes -- `probe/fetch.txt`, `probe/mirror.txt`
PROOF: 10:23 P10 234 recipes match their cache stamp by URL; `libfmt`'s stamp is the live bytes -- `stamps-url.txt`
PROOF: 10:23 P11 the stamps agree with the plans except `btrfs-progs` on GENERIC_X64; `ntfs-3g_ntfsprogs` built in three roots -- `stamps-*.txt`, `viewplan/`
PROOF: 10:27 P12 47 ROCKNIX overrides source one of the 243; three change the effective pin -- `sourcing-overrides.txt`
PROOF: 10:39 P13 of 75 GitHub repositories the URLs name, 3 renamed, 1 gone, 1 archived, 1 a personal fork -- `gh-repo-meta.txt`

### [Stage C] 10:41 to 10:44 — Phase 4.5, the plan file, the lint

- **Phase 4.5**, in `04`: each finding is attacked.
  - F-01 is confirmed three ways: by `viewplan` (`install libfmt` in all three plans), by the effective expansion, and by `scripts/get:24-53` → `get_archive:7`.
  - F-05 is the weakest: a cgit host may recover. Its bug says *refused on three reads*.
- **Rule 4**, asked of every PASS. Each check was seen to fail where it should:
  - (a) on the 16;
  - the probe on the two controls;
  - `pkgcheck` on `sameboy-lr`;
  - the stamps on 19 old files and on `libfmt`;
  - the fetch on `libfmt`;
  - the freshness tool, BEHIND on four.
- **Found while writing PL-01:** `libfmt`'s override is absent on `upstream/next`. ROCKNIX deleted it in `6103571f67` (#3470, 2026-10-11), so the next base merge also ends F-01. Six of the 47 sourcing overrides are orphans of that kind (F-12).
- **Phase 4.6:** not applicable (Local, D-WORKFLOW-184). `second-opinions/review-plan.json` is written.
- **`05-punch-list.md`**, from `tools/punch-items.py`: fifteen items, every one `Open`.
- **`tools/lint-audit-artifacts <folder> --phase pre-issue`** (10:44:15): `PASS pre-issue artifacts (does not certify resolution)`, with `ok    review-plan: local at epic tier under D-WORKFLOW-184 (plan § 6c and slices.json k 7: a currency table is Local ...)`.

### [Incident] 10:44 to 10:47 — an unquoted heredoc ran five tools

- **What happened:** the first write of the stage-B entry above used an unquoted heredoc (`<<EOF`) whose first bullet named tools in backticks. The shell ran each name as a command substitution, with no arguments and in this worktree:
  - `packaging-and-patches.md`: not a command;
  - `tools/fork-package-freshness`: network reads;
  - `tools/viewplan`: the default plan, read only;
  - `tools/update-pkg`: printed its usage and exited, writing nothing;
  - `tools/pkgcheck`: a read-only sweep;
  - **`scripts/update_packages`, on brief § 5's never-run list.**
- **What `update_packages` did:**
  - It walked `projects/ROCKNIX/packages/virtual/emulators`' list, skipping `amiberry`, `duckstation-sa`, `flycast-sa` and `gzdoom-sa` by `config/blocklist`.
  - It **rewrote `projects/ROCKNIX/packages/emulators/standalone/hatarisa/package.mk`**: `PKG_VERSION` went `6da06056...` → `8f475ba2...`, and its `PKG_SHA256` line was deleted.
  - It fetched that archive into this worktree's gitignored `sources/hatarisa/` (three files, 10:45:11 to 10:45:13).
  - It then died at `hypseus-singe` with `FAILED COMMAND source config/options`.
- **What it did not touch:** nothing was committed, nothing was pushed, and no other worktree was written. `find /workspace/cache/rocknix-sources -newermt '2026-10-24 10:44'` prints nothing: the shared cache is untouched. `hatarisa` is T30's path (#677), and the edit was made in this worktree, not in T30's.
- **Restored at 10:47:35:**
  - `git checkout --` of the recipe and of this log (whose garbled copy held the output);
  - `git diff --quiet 8ebaf8daad -- projects/ROCKNIX/packages/emulators/standalone/hatarisa/package.mk` is true;
  - the three downloaded files removed by their literal paths, and `sources/` removed with `rmdir`;
  - `git status --short` shows no tracked change.
- **The guard:** prose that names tools is written with the Write or Edit tool, or with a quoted heredoc (`<<'EOF'`), never with an unquoted one. A friction line is in `docs/friction-log.md` (`issue: #654`).

### [Stage C, continued] 10:49 to 10:54 — the coordinator's dispositions of the stage-B leads

- **Read whole:** the coordinator's #654 comment of 10:49 (issuecomment-6383296356), #877, #879 and #849's correction. `cf3a8d8e62`'s `libfmt` recipe was read with `git show` (line 12 carries `5dea48d1...`), as was the `btrfs-progs` override at the hash (`:6` `PKG_ARCH="aarch64"`).
- **The effective `PKG_ARCH` sweep**, five plans × 243 recipes (10:50:07 to 10:51:16): one plan entry is excluded, `btrfs-progs` on GENERIC_X64, so F-11 has no sibling.
- **Written:**
  - `01` § Brief erratum (`ntfs-3g_ntfsprogs`);
  - `02`: the libfmt row → #877; F-11 corrected; F-12 withdrawn; the `PKG_ARCH` row; P14 and P15;
  - `03` and `04`: the corrections left visible; § Q4's seven pin-changing overrides by path; `04` § Codification gaps: #844 probes the mirror first;
  - `05`: PL-01 → #877, Resolved (`fix-tree`); PL-11 → #879, Deferred; PL-12 Withdrawn.
- **The pre-issue lint:** PASS (10:54).

PROOF: 10:51 P14 the effective `PKG_ARCH` excludes one plan entry of the 243: `btrfs-progs` on GENERIC_X64 -- `probe/arch-<plan>.txt`
PROOF: 10:52 P15 #877's packet `cf3a8d8e62` gives `libfmt` 9.1.0 the three witnesses' `5dea48d1...` -- `git show cf3a8d8e62:projects/ROCKNIX/packages/devel/libfmt/package.mk`

### [Stage D] 10:55 to 10:57 — the punch list, the issues, the pause

- **The four lane bugs:** #880 `wsdd2`, #881 `newt`, #882 `libmpeg2`, #883 `configtools`.
  - Each is labelled `bug` with no milestone, has a code trace with an `Already written:` line and the VM line, and is classed *dead primary URL, mirror-covered*.
  - `tools/box-check --issue N`: 2 open, 0 fail for each.
  - Each body's sha256 is read from its recipe at the hash, and checked against the mirror's fetch and the cache's stamp. A first draft carried a typed hash for `configtools` whose tail was wrong; it was caught by that comparison before filing and appears nowhere.
- **#877 is the coordinator's** (PL-01, `libfmt`), resolved by its packet.
- **The audit issue:** #884, `Audit: M6 T7 the generic packages the image builds -- 15 findings (0 critical, 0 high)`. Labels `audit` and `punch-list`, milestone M6, a sub-issue of #654. `tools/box-check --issue 884`: 15 open, 0 fail.
- **`05-punch-list.md`** is regenerated with the issue numbers. The pre-issue lint passes.
- **Stage-D pause:** the lane waits for the coordinator's stream briefs (plan § 6b E, D-WORKFLOW-189) and drafts nothing under `packages/`.

### [Stage E] 11:02 to 11:03 — S1, three `PKG_URL` lines

- **Read first:** `t7-streams.md` at `5955f07e1f` (`git show`, not merged), and plan § 6b E's heredoc rule, re-read at that commit as the stream's first act.
- **The tests, before the change (11:02):**
  - the three expanded URLs (`s1/before.txt`);
  - a fetch into the empty `s1/before-fetch/`: three MATCH;
  - the synthetic `3.10.0`: `${PKG_VERSION:0:3}` gives `3.1`, `${PKG_VERSION%.*}` gives `3.10`;
  - https for `dmidecode` answers 302 to a savannah mirror.
- **The change:** three lines by an exact-string replacement asserted to match once.
- **After the change:** the URLs are unchanged but `dmidecode`'s scheme; a fetch into the empty `s1/after-fetch/` gives three MATCH; `pkgcheck` rc 0 on all three; the fixture on the recipes' own lines (`s1/fixture.txt`).
- **Commits:** `ce74769bab` libsoup, `49bddf9b3e` ruby, `063f10154a` dmidecode. One `git add -- <file>` each, with `git status --short` read before and after. Pushed.
- **Posted on #654** at 11:03 (issuecomment-6383425820).

### [Stage F] 11:03 to 11:04 — verification and the Phase 7 gate

- **The coordinator's targets (#654, 11:03):**
  - #885 for PL-06 to PL-09;
  - #645 issuecomment-6383422228 for PL-10;
  - #585's body section for PL-02 to PL-05, PL-14's twenty and PL-15. Read from #585's body, updated 11:03:19.
- **`05` regenerated:** every item has an outcome. Resolved: PL-01, PL-13, PL-14. Deferred: PL-02 to PL-11 and PL-15. Withdrawn: PL-12.
- **`02` § Verification:** P16 to P18.

PROOF: 11:02 P16 the old `PKG_URL` lines give `3.1/` for a synthetic 3.10.0, the new give `3.10/` -- `.qa-scratch/t7/s1/fixture.txt`
PROOF: 11:02 P17 the three archives fetched from the old and the new URLs into empty directories match the unchanged `PKG_SHA256` -- `.qa-scratch/t7/s1/`
PROOF: 11:03 P18 `pkgcheck` 0 on the three; the branch's diff from `8ebaf8daad` is the three lines, no `PKG_VERSION` -- `git diff --stat 8ebaf8daad 063f10154a`

### [Stage G] 11:05 to 11:06 — the retro

- `docs/retros/2026-10-24-m6-generic-packages-reached.md` (`bcc19abd98`), posted whole on #654 (issuecomment-6383451536). It says the slice did nothing to the two time-to-play numbers.

### [Stage H] 11:06 to 11:10 — the checks and the hand-back

- **The six checkers on `bcc19abd98`** (11:06:35 to 11:09:10), `git status --short` empty:
  - `register-check` 0;
  - `work-log-index --check` 0;
  - `rules-check --quiet` 0;
  - `forbidden-terms-check` 0;
  - `.githooks/hooks-test` 0 (`PASS`);
  - `tools/lint-audit-artifacts <folder>` 0: `PASS`, with `ok    review-plan: local at epic tier under D-WORKFLOW-184 (...)`.
- **The simulated merge** with the coordinator's tip `e09b57d16c` (merge base `e7978a1ca5`; `git merge-tree --write-tree` tree `be03882049`):
  - Exported to `/workspace/tmp/m6-t7/sim-merge-110935/` after `df -i` (`/workspace` 19%).
  - It conflicts only in `docs/friction-log.md`, the 10-24 work log and `INDEX.md`, which were united with `git merge-file --union`; `decision-register.md` auto-merged.
  - The marker grep is empty; the index was regenerated.
  - `register-check`: `664 IDs, each once; every citation in the live documents names a row`, rc 0.
- **#654's body:** `reviewed-at: 4ea87f17dd`, `fixed-at: 063f10154a`, read back.
- **Over the slice:** `git diff --stat 8ebaf8daad 063f10154a -- packages` gives three files and three lines. `--diff-filter=DR` gives 0 files. `PKG_VERSION` changes: 0.
- **#884:** 15 of 15 ticked at their outcomes; `box-check` 0 open, 0 fail.
- **API budget over the slice:** 4,291 at 10:12 and 4,325 at 10:57 (the hour reset at 10:18:26 mid-loop). The loops' calls were about 245 for (b), 23 for the other paths, 11 for the hash pins, 75 for the GitHub owners and 4 for LibreELEC's commits, plus the tool's own and the tracker's.

### [Close] 11:16 to 11:16 — the completion marker

- **Accepted:** the coordinator accepted T7 at hand-back and closed #884 as completed (`closedAt` 2026-10-24T11:16:04Z).
- **The marker:** `tools/write-completion.py` (T6's, with `A` and `ISSUE = 884`) printed `#884 closed/completed, 15 ticked, 0 open; completed_at 2026-10-24T11:16:25.987460+00:00`. It wrote `audit-completion.json`, `tracker-final-readback.json` and `tracker-completion.json`, hash-binding `04`, `05` and the two receipts.
- **The full lint** (11:16:33): `PASS`, with the D-WORKFLOW-184 line.
- **`ceremony-check`** reads the marker: `audit last 2026-10-24T11:16:25... via #884`. It exits 1 only on M7's W42 summary, as at stage A.
- **The lane is idle.**
