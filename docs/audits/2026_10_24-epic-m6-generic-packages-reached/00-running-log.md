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
