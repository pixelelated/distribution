# Running log — M6.P2 T25, the devices the fork does not ship and the other projects (#672)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, the T5 session (`m6-t5-build-engine`), after T27's close-out.
- **Brief:** `docs/reviews/briefs/devices-unshipped.md`, version 2 (`55e414441d`, the same bytes at the branch's `HEAD`).
- **Dispatch:** the coordinator's comment on #672, 09:39 UTC on 2026-10-25.
- **Depth:** Local. A reachability table (plan § 6c, D-WORKFLOW-184). **No `tools/council/run` call, keyed or not.**
- **`reviewed-at`:** `b27889bce2`, the dispatch tip. The read is of `8ebaf8daad`'s bytes: the branch-vs-hash diff over the 397 is empty (c03), and so is `git diff --stat 8ebaf8daad HEAD -- packages projects`. Upstream `651150fc88` and the base `c445081a59` were read locally; no `git fetch` was run.
- **Can this be done on the VM? No.** This is a reachability table over files no image carries; its bench is the tree and the record.
- **What never runs here:** a build, a plan generation, a guest, a fetch, a network read, a `tools/council/run` call, a command against a handheld, an M7 root read, or a change under `packages/` or `projects/` (D-WORKFLOW-209).
- **Scratch:** `TMPDIR=/workspace/tmp/m6-t25/tmp` (`df -i /tmp` 41 %, nothing written there). Outputs are under `.qa-scratch/t25/` and `/workspace/tmp/m6-t25/runner/`, with copies in `stage-a/`.
- **Proofs:** each proof in `02`'s § Proofs has one numbered proof line here, in its stage.

## [Stage A] 09:40:42 to 09:42 UTC — the block, the checks, the positive control

- **The first commands** (brief § 1), 09:40:42: the status is clean (0); the tip is `b27889bce2`, on `7d61fe0f96` and `55e414441d`; stacked on `8ebaf8daad`; `[]` against it under `packages` and `projects`; `register-check` ok; D-WORKFLOW-209 at register line 746.
- **The host:** the host file's last line is the coordinator's 09:17 UTC T22 guest-window return. Census: qemu 0.
- **The runs:** `stage-a/runs.sh`, 17 steps from 09:41:11 UTC, each with its exit and wall time (`stage-a/runs.tsv`). **All exit 0.**
  - c01, the block: `paths 397 lines 49555 {'unreached': 216, 'unshipped': 181} {'upstream-carried': 396, 'fork-own': 1}`; `units 25`; `read 3619 rows 64 fork-own 0`; `shadowed 9`; fork-own `['packages/linux/package.mk']`; `paths.txt` 397.
  - c03, the branch against the hash: `[]`.
  - c04: 12 target lines (`44 AMD64`, `48 RK3588`, `53 RK3576`, `58 S922X`, `63 RK3566`, `68 RK3326`, `73 RK3399`, `83 SM4450`, `88 SM6115`, `93 SM8250`, `103 SM8650`, `107 SM8750`).
  - c05: `world` lacks AMD64, SM4450 and SM6115.
  - c06: 27 `PROJECT=` lines, 0 not ROCKNIX.
  - c07: against the base, `1 M packages/linux/package.mk`.
  - c08: against `651150fc88`, **39 M**.
  - c09: **65** upstream commits since the base.
  - c10: every fork commit touching a target directory is a merge (two parents each; `git log --no-merges` over all twelve lists 0).
  - c11: upstream since 2026-06-01: 7 45 12 40 20 6 58 37 55 79 41 91.
  - c12: whole-word engine references: ARM 0, Allwinner 1, Amlogic 3, Generic 4, NXP 1, Qualcomm 1, RPi 2, Rockchip 3, Samsung 1.
  - c13, c14: the hostname is `"ROCKNIX"` at `packages/linux/package.mk:132` and at the override's `:160`, both by `3d7c075f63`.
  - c15: **1,424,530 bytes**.
  - c16, c17, **the positive control:** `78:H700`, `98:SM8550` (2); the block with reach `shipped` and `/H700/` returns 28 rows, 27 in the directory and the overlay DTS.
- **One delta from the brief:** RPi's whole-word count is 2 (`create_addon:117`, `create_docker_package:90`). The brief's third site, `scripts/image:349`, reads `Distro_RPi` in a comment, which a whole-word grep does not match.
- **Nothing of the never-run list ran.** Nothing was written under `/tmp`, `/workspace/repos/rocknix*`, another lane's worktree, `packages/`, `projects/` or `tools/`.
- PROOF: P1, the membership: c01, with the positive control c16 and c17.
- PROOF: P2, the provenance: c07, c08, c09 and c10 (the fork touched one path; 39 M and 65 commits behind upstream).

## [Stage B] 09:47 to 10:03 UTC — the tables, the edge sweep, F-01

- **The runs:** `stage-b/runs.sh`, 18 steps from 09:54:22 UTC, each with its exit and wall time (`stage-b/runs.tsv`).
  - b01 to b08 are the checks; `g_*` are the generator's ten sections.
  - Exits are 0, except b03 (`pkgcheck`'s control, rc 1 by design) and b04 (the whole-tree baseline, rc 1: 12 FAIL, none in the slice).
  - A first `pkgcheck` pass at 09:47:32 counted processed files with the wrong clear code (`ESC[2K` for the tool's `ESC[K`). It was re-run at 09:47:44 and folded into b02.
- **The generator:** `tools/t25-tables.py`, sections `coverage units targets projects pins trees dead q6 q7 edges counts`, and `write` / `check` over a file's generated blocks.
  - Its first `q7` run failed its own assertion (5 near-names for 4). It had matched RK3328 against RK3326; near-names are now family wildcards (`RK356X`).
  - Its first `edges` pattern used `\s` inside an ERE bracket (a literal `s`) and matched `syslinux`. The committed pattern uses `[[:space:]]`.
- **F-01 found** during the edge sweep. The kernel recipe's `PKG_DEPENDS_UNPACK` takes `intel-ucode` on x86 (`:69-72`, `:202`) and `generic-dsi` on RK3326/RK3566 (`:81-82`, compiled for RK3576 too at `:108-111`). The inventory's plan-derived `buildable_by` misses both. T11's record has 153 `intel-ucode` entries in the guest kernel (`ed8c48f3cd`, its `02:142`). The dead class is 203, not the brief's 207.
- **Typed figures caught:** F-02's projects row (4,960 / 140,469, typed; 4,966 / 145,992, generated), and `03`'s "upstream edits the generic copy" (it does not; its one `M` is the fork's hunk). Both were corrected before commit.
- **Outputs:** `02` (397 coverage rows by the brief's grep; 14 proofs), `03`, `04`; `check` exits 0 on both generated files.
- **Nothing of the never-run list ran.** `git diff --stat 8ebaf8daad HEAD -- packages projects` is empty.
- PROOF: P3, the branch carries the hash's bytes and the engine reads match at the tip: c03, b01.
- PROOF: P4, the twelve targets, `world`, `PROJECT=`: c04, c05, c06.
- PROOF: P5, the projects: c06, c12.
- PROOF: P6, the drift: c11, b07.
- PROOF: P7, the fork's hostname edit and its twin: c13, c14.
- PROOF: P8, the weight: c15.
- PROOF: P9, `pkgcheck` with its control and baseline: b02, b03, b04.
- PROOF: P10, Q1 hosts: b05.
- PROOF: P11, the pins: `g_pins`.
- PROOF: P12, the 53 trees: `g_trees`.
- PROOF: P13, the edges and F-01: `g_edges`, b08.
- PROOF: P14, the coverage and unit tables, regenerated: `g_coverage`, `g_units`, `g_q6`, `g_counts`; `check` 0.

## [Stage C] 10:03 to 10:08 UTC — the Local plan, the punch list, the pre-issue lint

- **The plan:** `second-opinions/review-plan.json`: `depth: local`, `reviewers: []`, `tier_exception: D-WORKFLOW-184`, and the reason naming plan § 6c and `slices.json` `k 25`. **No `tools/council/run` call was made in this slice, keyed or not.**
- **`05`:** five items, PL-01 (Low) to PL-05 (Info), every one `Open` and every one with `question:`. PL-02 is the #346 class proposal's text, for the coordinator to post.
- **T27's pointer on #672 (08:41 UTC) answered:**
  - **PL-02 (the atf seam) reaches this slice through RK3399:** its `u-boot` builds `atf`'s `*)` branch, `696b8e53...` to `6b1d5e89...` upstream. Added to F-05, `03` § 3.5 and PL-05.
  - **PL-14 (an uppercase compatible):** the same grep over the 53 trees finds one, RK3576's `"cellwise,cw221X"`, matched byte for byte by its driver patch `0006` (`:966`). Not a defect; recorded in `02` § The device trees.
- **The lint:** `tools/lint-audit-artifacts docs/audits/2026_10_25-epic-m6-devices-unshipped --phase pre-issue` → `PASS pre-issue artifacts (does not certify resolution)`, with the line `review-plan: local at epic tier under D-WORKFLOW-184 (...)`. Re-run after T27's leads were folded in: `PASS`.
- **`tools/forbidden-terms-check`:** rc 0 over the tree.
- **The generated files:** `check` same on `02` and `04`.

## [Stage D] 10:09 UTC — the audit issue, and the pause

- **#1102:** *Audit: M6 T25 the devices the fork does not ship and the other projects -- 5 findings (0 critical, 0 high, 0 medium, 1 low, 4 info)*.
  - Labels `audit` and `punch-list`; milestone `M6: Codebase renovation`.
  - Attached as a sub-issue of #672 (REST id 6023277637; readback lists it under #672).
  - `tools/box-check --issue 1102`: 5 open checkboxes, 0 fail.
- **The pause:** the punch list posted on #672, asking for the coordinator's dispositions. No stream is expected: nothing here changes.

## [Stage E-F] 10:12 to 10:14 UTC — the dispositions recorded; no stream; the re-derivations at the tip

- **The dispositions** (coordinator, #672, issuecomment-6396356786, 10:12:11 UTC):
  - PL-01 deferred to #1101, a new Backlog issue, because its direction is opposite to #1086's;
  - PL-02 deferred to #346, posted by the coordinator at 10:12:12 UTC with `05` § PL-02's text;
  - PL-03, PL-04 and PL-05 resolved as records. A deferral needs an owning issue, and the merge has none yet.
  - **No stream:** `fixed-at` is the hand-back commit.
- **`05`:** each item's note, the index (`deferred:#1101`, `deferred:#346`, `resolved` ×3) and the Phase 7 table. **The resolution lint:** `PASS`, and `PASS` with `--issue 1102`.
- **Stage F:** `stage-f/runs.sh`, 12 steps from 10:13:28 UTC, all exit 0; results in `02` § Stage F.

## [Stage G-H] 10:15 to 10:15 UTC — the retro, the checkers, the hand-back

- **The retro:** `docs/retros/2026-10-25-m6-devices-unshipped.md`, posted on #672 (issuecomment-6396380888). It says the slice did nothing to the two time-to-play numbers and names what T28 inherits.
- **The friction line:** the typed figures, with the generator as guard.
- **`04`'s scorecard** is brought up to the hand-back.
- **The hand-back commit is `fixed-at`.** The six checkers run on it, and their exit codes are in the hand-back comment on #672.
- **No `tools/council/run` call, guest, build, plan generation, fetch, handheld command or M7 root read** ran in this slice, from stage A to the hand-back.
