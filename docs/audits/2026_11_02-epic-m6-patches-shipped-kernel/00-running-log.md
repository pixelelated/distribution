# Running log — M6.P2 T41, the kernel patches and configurations the shipped and test images apply (#688)

- **Executor:**
  - **2026-11-02 05:26 to 05:30 UTC (Stage A execution):** Claude Opus 5.5 (`anthropic/claude-opus-5-5`) at high effort in the Antigravity CLI, session `m6-t3-emulators` (conversation `5072145d-e86c-4a8e-a22c-8f42579b4a72`; ruling (m)). Stopped at ~05:30 UTC on the account usage quota after completing the Stage-A commands and copying `stage-a/` into the audit folder.
  - **2026-11-02 15:08 UTC onward (Stage A write-up, archive/stash and checkpoint):** Gemini 4 Argon (`google/gemini-4-argon`) at high effort in the Antigravity CLI, same session `m6-t3-emulators` (switched by the owner at 15:08 UTC after the 05:30 UTC quota stop so all lanes can stash cleanly and resume in a new harness). Both served models are recorded here; the `primary` entry in `second-opinions/review-plan.json` at Stage C will record the model identity per the coordinator's instruction on #688.
- **Brief:** `docs/reviews/briefs/patches-shipped-kernel.md` at `9313492990` (version 2, 2,194 lines, sha256 `24794608bcc7a0f9dc523b95e70e74e102c0aa1ba0fde41e6a353306f6ec6b87`, prefix `24794608bcc7a0f9`; version 1 `7d70da5972`, stranger's proof `kit/t41-proof.md`).
- **Dispatch:** the coordinator's comment on #688 (`issuecomment-6569794826`, `2026-11-02T05:26:19Z`).
- **Depth:** Local (`tier_exception: D-WORKFLOW-184`, plan § 6c: a provenance table). No external reviewer seat, no Facilitator, no council call, no `npm install`, no keyed call.
- **`reviewed-at`:** `f03b64419f` (the lane's seed commit at Stage A, one commit over the coordinator's tip `d7dd766659`, which carries P1 `2174265e9c` since `6a12ce2d73` and `next` `8ebaf8daad`). Pinned upstream commit: `651150fc88` (merge base `c445081a59`; the local ref `upstream/next` is `50433c03cc`, 59 commits ahead of `651150fc88`, recorded as information only per ruling (f) and proof X01).
- **The rule (rulings (c), (g), (i); D-WORKFLOW-209):** the lane edits none of the 107, no recipe, no tool, no script; its commits touch only its audit folder, its retro, its pointer and its log entries. No build, no guest, no network fetch, no config helper, no tarball extraction outside `/workspace/tmp/m6-t41/src/`.
- **Scratch:** `/workspace/tmp/m6-t41/` (after `df -i /workspace`: 28% inodes used, 68% bytes used), never `/tmp`; to be retired at Stage H (D-INFRA-022).

## [Stage A] 2026-11-02 05:26:27Z to 05:30:28Z (stashed 15:08Z) — pointer keys, Local lint proof, membership at P1 and tip, host protocol read, and § 5 runs

### 1. The pointer's eleven keys (§ 10) and environment validation (`05:27:50Z`)

- Checked `.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md` before the first Stage-A command:
  - Unfilled placeholder scan (`/usr/bin/grep -c -E '__[A-Z0-9_]+__'`): `0` (`rc=1`).
  - All eleven keys of § 10 present (`1` each): `Branch (distribution):`, `Worktree (distribution):`, `Worktree (EmulationStation):`, `Executor:`, `Epic:`, `Depth:`, `The lens:`, `The rule:`, `The host:`, `Register:`, `The brief:`.
  - Seeding-error probes against T40 (`feature/m6-patches-dead-687`, `m6-t5-build-engine`, `reachability over the 778`, `patches-dead.md`) and T39 (`m6-doctrine-reference-686`, `m6-t1-os-launch`, `#807`, `cost against value`, `doctrine-reference.md`, `D-WORKFLOW-220` as this slice's row): `0` hits on every key line (`#687` appears only in `Epic:` as historical context `T40 (#687) accepted at e863379cec, closed out at bf3409ea18, #687 still open`).
  - `git branch --show-current`: `feature/m6-patches-shipped-kernel-688` (`rc=0`).
  - `git status --short | /usr/bin/grep -c ''`: `0`.
  - `git rev-parse --short=10 HEAD`: `f03b64419f` (`git rev-list --count d7dd766659..HEAD` = `1`, the seed commit; the dispatch comment notes this erratum to the brief's § 1 and § 10).
  - `git merge-base --is-ancestor 2174265e9c HEAD`: `carries-p1` (`rc=0`).
  - `git merge-base --is-ancestor d7dd766659 HEAD`: `cut-from-the-coordinator` (`rc=0`).
  - `git merge-base --is-ancestor 8ebaf8daad HEAD`: `next-is-here` (`rc=0`).
  - `git -C /workspace/repos/pixelelated/distribution rev-parse --short=10 upstream/next`: `50433c03cc` (information only; every upstream comparison pins `651150fc88`, proof X01).
  - `sha256sum docs/reviews/slices.json docs/reviews/inventory.json docs/reviews/areas.json | cut -c1-16`: `49bc2745664e52f4`, `d17b9cac4b2c2245`, `985f742cfd4a2138` (`rc=0`).
  - `test -d /workspace/tmp/m6-coordinator/t11-research/tree`: `clone-here` (`rc=0`).

### 2. The lint's Local proof, before anything else (ruling (i), `05:28:27Z`)

- Exported T4's finished Local folder `docs/audits/2026_10_24-epic-m6-doctrine-rules` from `6ec78bbf8c` into `/workspace/tmp/m6-t41/lint-proof/pass` and `/workspace/tmp/m6-t41/lint-proof/fail` (`rc=0`).
- Read T4's `second-opinions/review-plan.json`:
  ```text
  T4 folder: docs/audits/2026_10_24-epic-m6-doctrine-rules
  t4 plan: local D-WORKFLOW-184 0
  ```
- Ran `tools/lint-audit-artifacts` on the unmodified Local folder (`stage-a/lint-local-pass.out`) and on the copy with `tier_exception` removed (`stage-a/lint-local-fail.out`):
  ```text
  lint, a Local plan, rc=0
    ok    PL-25 answers Q4

  PASS
  lint, tier_exception removed, rc=1
  12:  FAIL  second-opinions/review-plan.json or its call evidence is invalid: local-only cannot satisfy Epic/Milestone
  91:1 CONTRACT FAILURE(S)
  ```
- PROOF: `tools/lint-audit-artifacts` at `f03b64419f` exits `0` (`PASS`) on T4's `depth: local` plan with `tier_exception: D-WORKFLOW-184` (`t4 plan: local D-WORKFLOW-184 0`) and fails closed (`rc=1`, `FAIL  second-opinions/review-plan.json or its call evidence is invalid: local-only cannot satisfy Epic/Milestone`) when `tier_exception` is removed (`stage-a/lint-local-pass.out`, `stage-a/lint-local-fail.out`).

### 3. § 2's membership block at P1 (`2174265e9c`) and at the lane's tip (`f03b64419f`) (`05:28:28Z–05:28:36Z`)

- Extracted `block.sh` and `block-expected.txt` by marker from `9313492990:docs/reviews/briefs/patches-shipped-kernel.md` (`brief read rc=0`):
  ```text
  4d300124a6bf116f
  .qa-scratch/t41/block.sh:148
  .qa-scratch/t41/block-expected.txt:99
  ```
- Ran `bash .qa-scratch/t41/block.sh > /workspace/tmp/m6-t41/tmp/block.out 2>&1` against `W=/workspace/tmp/m6-coordinator/t11-research/tree` and `P1=2174265e9c`:
  ```text
  block rc=0
  block = the brief's expected lines
  ```
  `diff .qa-scratch/t41/block-expected.txt /workspace/tmp/m6-t41/tmp/block.out` exited `0` (0 differing lines across all 99 lines). Saved the P1 run's scratch under `/workspace/tmp/m6-t41/stage-a-p1/` and committed its artifacts under `stage-a/p1-qa-scratch/` (`tree-ih.txt` sha256 `e0840a0ad48f861236a3b05360178657eb283462bfbfa296aa408215086f8a23`, 133,520 lines; `tree-p1.txt` sha256 `fa347753df4b8b49f58a59139ce1639beb957447846a35c6edad0222020b1402`, 133,521 lines, recorded in `stage-a/p1-qa-scratch/tree-listings.sha256`).
- Rebound `W` to this worktree and `P1` to `HEAD` (`f03b64419f70e965b733eb9496e4057b70316e66`; rebinding grep count `1`) and ran `bash .qa-scratch/t41/block-tip.sh > /workspace/tmp/m6-t41/tmp/block-tip.out 2>&1`:
  ```text
  block at the tip rc=0
  the same lines at the tip
  ```
  `diff /workspace/tmp/m6-t41/tmp/block.out /workspace/tmp/m6-t41/tmp/block-tip.out` exited `0` (byte-identical 99 lines; settles Version 1 open item 1).
- PROOF: § 2's membership block (`sha256` prefix `4d300124a6bf116f`, 148 lines) exits `0` at `2174265e9c` and at `f03b64419f`, matching all 99 expected lines byte-for-byte (`107` paths; `40474` lines by inventory and `/usr/bin/grep -c ''`, `40473` by `wc -l`; `106` patch and `1` kernel-config; reach `shipped: 103, test: 4`; `SAME 106` and `ADDED 1` against `c445081a59`; `stage-a/block.out`, `stage-a/block-tip.out`).

### 4. Host coordination file read (`05:28:36Z`, ruling (h))

- Read `/workspace/tmp/m7-m6-host-coordination.txt` once for its protocol and line count only:
  - UTC time: `05:28:36`
  - Line count (`wc -l`): `1045` (identical to the dispatch comment's host-lines figure on #688).
  - Tail shows M7's `SM8550-027` build and independent readback RETURN at `01:22:14Z` and the coordinator's automatic read acknowledgements (`kit/compile-ack.sh`, pid `1230737`).
  - This slice writes no line to `/workspace/tmp/m7-m6-host-coordination.txt` and runs no guest or compiler.

### 5. § 5's Stage-A runs (`05:28:36Z–05:29:21Z`, `stage-a/run/stage-a.out`)

- **Tool's `--order` row from the worktree (settles Version 1 open item 2):**
  - `git status --short --ignored | /usr/bin/grep -c ''` before: `1` (`.qa-scratch/`).
  - `./tools/renovation-inventory --order --no-write --distribution /workspace/tmp/m6-coordinator/t11-research/tree`: `rc=0`, `lines=50`, `slices: 46`, `rows: 134634 (inventory: 134634)`, `unassigned: 0`, `ambiguous: 0`, row:
    ` 41 patches-shipped-kernel             patches-and-configs       107 paths    40,474 lines        0 read        0 fork-own   40,474 patch  table   `
  - `git status --short --ignored | /usr/bin/grep -c ''` after: `1` (unchanged; `stage-a/order.out`).
- **Recipe pins, device options, and `PATCH_ARCH` / `PKG_PATCH_DIRS` rules as text (never sourced):**
  - `HEAD:projects/ROCKNIX/packages/linux/package.mk`: `:16 PKG_PATCH_DIRS="${LINUX} mainline ${DEVICE} default"`, `:29-31` `H700|SM4450|SM6115|SM8250|SM8550|SM8650|SM8750)` -> `PKG_VERSION="7.2"`, `PKG_SHA256="f9fef3d14c0df53819026f4be74459835c2a0b0dcbf5b5bbd9ea19f0829402b3"`, `:33-34` comment on automatic `7.2` patch dir, `:36-40` `RK3326|AMD64|GENERIC_X64)` -> `PKG_VERSION="7.1.2"`, `PKG_SHA256="37198c93727be247c9fb5309bb86cd5e496c61e5322cd8c4eca9476bb0b5883f"`, `PKG_PATCH_DIRS+=" 7.0"`.
  - Device `options`: `H700:25: KERNEL_TARGET="Image"`, `SM8550:25: KERNEL_TARGET="Image"`, `GENERIC_X64:10: TARGET_KERNEL_PATCH_ARCH="x86_64"`, `GENERIC_X64:24: KERNEL_TARGET="bzImage"`, no `LINUX=` in any of the three. `config/arch.arm:80`: `TARGET_KERNEL_PATCH_ARCH="aarch64"`.
  - Unpack patch-dir rules read at `:127-159` (`x86` on `x86_64`, else `${TARGET_KERNEL_PATCH_ARCH:-${TARGET_ARCH}}` for kernel packages; glob order).
- **Nine directories' counts, application orders, and absent directories:**
  - `GENERIC_X64 total: 8` (`stage-a/order-GENERIC_X64.txt`), `H700 total: 42` (`stage-a/order-H700.txt`), `SM8550 total: 65` (`stage-a/order-SM8550.txt`).
  - `7.0: 4`, `7.2: 6`, `mainline: 4`; `H700: 32 patches, 1 disabled`; `SM8550: 55 patches, 1 disabled`.
  - Seven `absent patches/<d>` lines confirmed: `absent patches/H700`, `absent patches/SM8550`, `absent patches/GENERIC_X64`, `absent patches/default`, `absent patches/aarch64`, `absent patches/x86`, `absent patches/7.1.2`.
- **Header census:**
  - `patches 106 with From: 87 with Subject: 89` (`rc=0`).
  - 4 rows carrying `Link:` or `Upstream-Status:`: H700 `0160` (`:11:Link:`), SM8550 `0006` (`:35:Link:`), `7.2/0011` (`:19:Link:`), `7.2/0016` (`:12:Upstream-Status: Backport`).
- **Byte identity against `c445081a59` and `651150fc88`:**
  - Against `c445081a59`: `106 vs c445081a59 SAME`, `1 vs c445081a59 ABSENT` (`0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch`).
  - Against `651150fc88`: `101 vs 651150fc88 SAME`, `4 vs 651150fc88 CHANGED` (SM8550 `linux.aarch64.conf`, SM8550 `0104`, `7.0/0010`, `7.2/0010`), `2 vs 651150fc88 ABSENT` (`mainline/0002-input-add-input-polldev-driver.patch` and H700 `0950`).
- **Upstream changes since `c445081a59` at `651150fc88`:**
  - Across the four shipped kernel directories (`KD`): `12 A`, `1 D`, `4 M`.
  - Over the 107 paths: `5 files changed, 36 insertions(+), 515 deletions(-)` across 8 commits (`dcafa74090`, `6fbefc45c6`, `70912f0377`, `abfdcfb57f`, `fe5216ff69`, `9416eec2c2`, `5f56cd5150`, `c0980b2b71`; 7 non-merge).
  - Both `0010-msm-resource-cleanup.patch` copies against `651150fc88`: `2 files changed, 28 insertions(+), 22 deletions(-)` (L-01).
  - Upstream `651150fc88:projects/ROCKNIX/packages/linux/package.mk:18` quoted `=~` test over `RK3326`, `RK3399`, `S922X`, `H700`, `SM8550`: five `no-match` lines (L-02); whole-tree `rocknix-joypad/` count at `651150fc88`: `1` (`projects/ROCKNIX/packages/linux-drivers/rocknix-joypad/package.mk`, not a patches dir).
- **Fork commits and recipe diff since `c445081a59`:**
  - Over the 107 paths: 6 commits (`f370dc8787`, `049765fba0`, `4497f291bd`, `7bd7f31312`, `cbf75c0b06`, `7650de7dd6`), 1 non-merge (`cbf75c0b06 2026-09-10 Max Engel Handhelds keep their evidence across a power cycle: persistent logs, a watchdog, a crash`).
  - Over the two kernel recipes: 2 non-merge commits (`3d7c075f63 2026-10-02`, `dc948f59aa 2026-08-21`), `2 files changed, 5 insertions(+), 5 deletions(-)`.
  - Churn on the 107 since `2026-06-01`: `64`.
- **Duplicate pairs and symlink entries:**
  - Three `identical 7.0/7.2` lines (`0010`, `9998`, `9999`) and two `identical DDR3/DDR4` lines (`0001`, `0002`).
  - `120000` entries under the roofs: `3` ALSA UCM `.conf` symlinks under `RK3566` and `SM8750` filesystem overlays; `0` symlinked `patches` directories (L-23, #1056).
- **The fork-written H700 ramoops patch (L-16, ruling (e)):**
  - `cbf75c0b06 2026-09-10`, `38` lines, `not-in-upstream`, `0` ramoops-named patches at `651150fc88`, `# CONFIG_PSTORE_RAM is not set` at `651150fc88:projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf:7292`, and the six `CONFIG_` lines in `HEAD:projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf` at `:3656`, `:7290`, `:7292`, `:7975`, `:7978`, `:7979`.
- **The SM8550 configuration (L-19, rulings (d), (j)):**
  - Header (`:3`): `# Linux/arm64 7.2.0 Kernel Configuration`.
  - `0` numstat lines against `c445081a59`; `7 7` against `651150fc88` (14 `[-+]` `CONFIG` lines).
  - Conf-diff counts (settles Version 1 open item 8):
    - `(a)` against `HEAD:projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf` (sorted): `2609`.
    - `(b)` extracted `linux-7.2/arch/arm64/configs/defconfig` from `/workspace/cache/rocknix-sources/linux/linux-7.2.tar.xz` into `/workspace/tmp/m6-t41/src` (`defconfig extract rc=0`); non-comment sorted diff count: `3827`.
    - `(c)` `17` symbols forced or disabled in `projects/ROCKNIX/packages/linux/package.mk:146-335` (`stage-a/forced.txt`), 15 present in SM8550's conf (`1` each) and 2 absent (`CONFIG_EXTRA_FIRMWARE_DIR 0`, `CONFIG_ISCSI_IBFT_FIND 0`).
    - `(d)` upstream `651150fc88` header (`:3`): `# Linux/arm64 7.2.0 Kernel Configuration`.
- **Tarballs and non-kernel sources (ruling (g)):**
  - `linux-7.2.tar.xz = its .sha256 (f9fef3d14c0df538)` (matches recipe `:31`).
  - `linux-7.1.2.tar.xz = its .sha256 (37198c93727be247)` (matches recipe `:38`).
  - Cached archives verified present with `.sha256` and `.url`: `kernel-firmware-20260309.tar.gz`, `u-boot-DDR3-v2026.01.tar.gz`, `u-boot-DDR4-v2026.01.tar.gz`.
- **No-edit / register removal checks and baseline checkers (settles Version 1 open item 3):**
  - `git diff --stat d7dd766659 HEAD -- '*.patch' '*.conf' packages projects tools scripts`: empty; non-merge commit count on those paths: `0`; removed lines in the three registers: `0`.
  - `rules-check rc=0` (`rules-check: 30 rule files, every one front-mattered and indexed`).
  - `register-check rc=0` (`register-check: 717 IDs, each once; every citation in the live documents names a row` — includes `D-WORKFLOW-221`, T41's ownership row added at `d7dd766659`).
  - `work-log-index rc=0` (`work-log index: current`).
  - `ceremony-check rc=0` (`nothing overdue.`).
  - `box-check rc=0` (`box-check: 300 issue(s), 626 open checkbox(es), 0 fail, 13 issue(s) with rows to re-derive against`).
  - `hooks-test rc=0` (`PASS`).
- **Issues and predecessor branch tips (`05:29:48Z`, `stage-a/run/stage-a-extra.out`):**
  - `#688` is `OPEN`, `52` body lines (after the coordinator's 28-checkbox fill at dispatch).
  - All 28 other referenced issues (#1054, #687, #346, #1048, #1049, #1056, #1086, #1101, #879, #1053, #1050, #1051, #328, #369, #104, #44, #1084, #1083, #836, #796, #1099, #1100, #1110, #563, #559, #585, #1071, #1072) are `OPEN`.
  - Predecessor slice branch tips: `feature/m6-device-generic-x64-658` `ed8c48f3cd` (read hash `47672fe4a0` present), `feature/m6-device-h700-674` `0ac98afe43` (`78579255e4` present), `feature/m6-device-sm8550-675` `5a60d1c825`, `feature/m6-devices-unshipped-672` `9b9be6a948`, `feature/m6-patches-dead-687` `bf3409ea18` (`e863379cec` present).
- **Secret-pattern collision on `0158-mmc-sunxi-mmc-mask\u002ddata0-...` found during Stage-A packaging (`15:10Z`):**
  - Scanning `docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/stage-a/` against `.githooks/secret-patterns` matched 11 files (`order-H700.txt`, and `paths.txt`, `text.txt`, `block-1.txt`, `block-2.txt`, `mb-compare.txt` under `p1-qa-scratch/` and `tip-qa-scratch/`) on H700 patch #32 (`0158`), because its filename substring after `ma` matches the unanchored `sk-[A-Za-z0-9_-]{24,}` rule in `.githooks/secret-patterns` — the exact row `docs/reviews/inventory.json` lists in `escaped_rows` (`tools/renovation-inventory:633-642`).
  - In the committed `stage-a/` copies, that single hyphen is escaped as `\u002d` (matching `inventory.json`), reducing `.githooks/secret-patterns` matches across `docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/` to `0` (`rc=1`) while keeping the raw unescaped files in `/workspace/tmp/m6-t41/` and `.qa-scratch/t41/`. Flagged on #688 for the Stage-B `02-forward-audit.md` table vs Criterion 9 (`diff` against `.qa-scratch/t41/paths.txt`) and Criterion 17 (`0` files matching `.githooks/secret-patterns`).
