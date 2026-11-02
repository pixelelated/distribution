---
slice: T41
id: patches-shipped-kernel
issue: "#688"
epic: "#1054"
area: patches-and-configs
kind: table
lens: package currency
depth: Local
version: 2
written: 2026-11-01
version_2: 2026-11-02 (the stranger's proof of version 1, kit/t41-proof.md)
author: the M6 coordinator lane (D-WORKFLOW-189)
read_refs:
  distribution: 8ebaf8daad
  p1: 2174265e9c
  coordinator: 6a12ce2d73
  inventory_head: eb4763e3cc
  merge_base: c445081a59
  upstream: 651150fc88
  t40: feature/m6-patches-dead-687 at bf3409ea18
---

# Review brief: M6.P2 T41, the kernel patches and kernel configurations the shipped and test images apply, tabled by provenance and currency (#688)

**Version 2, 2026-11-02, applies the stranger's proof of version 1**
(`/workspace/tmp/m6-coordinator/kit/t41-proof.md`, in no tree, 331 lines; its
totals `checks 112; PASS 93; MISMATCH 7; SETTLED 8; NOTE 4; corrections 7`,
read at `7d70da5972`), cited `proof K<nn>` / `proof X<nn>` / `proof C<n>`: each
correction is made in the body at its line and listed, with the open items
the proof settled and the coordinator's two rulings, in
`## Version 2: corrections from the proof`. **Version 1, 2026-11-01, was
written from five read-only research files** -- R1
membership and provenance, R2 the patches read, R3 the tests, tools and
harness, R4 the inherited items, R5 the model and the ceremony
(`/workspace/tmp/m6-coordinator/kit/t41-research/`, in no tree) -- and the
coordinator's rulings (D-WORKFLOW-189; `docs/reviews/plan-for-the-plan.md`
§ 6b, § 6c, § 7). **Every figure here is one of their quoted tool lines**,
cited as `R1 C<nn>` (R1's commands C01 to C18) or `R1 § <n>`; `R2 § <n>`,
`R2 L-<nn>` (R2's leads L-01 to L-15, never this brief's numbering) or
`R2 command <n>` (1 to 17); `R3 § <n>` or `R3 C<n>` (1 to 24); `R4 item <n>`
(1 to 28), `R4 § <n>` or `R4 command <n>` (1 to 21); `R5 § <letter>`,
`R5 § B item <n>`, `R5 § G (<letter>)` or `R5 C<n>` (C1 to C16); or a
command this drafting ran at the coordinator's tip `6a12ce2d73`, cited
`v1 read` with the command. **`[unverified]` marks what no tool line
settles, with the command that settles it**; `## Version 1: what the drafting
read did not settle` lists every one, then the places where the research
files disagree and how this brief takes each, then the checks on this file.
Counts by `/usr/bin/grep`, never the shell's function (#1138).

**The structure is T40's brief** (`docs/reviews/briefs/patches-dead.md` at
the tip, 454 lines, 16 checkboxes, the same area and epic, accepted with its
`## Errata, 2026-10-25`; R5 § A: *"of the two, T40's is the nearer model"*)
in **T39's form** (`docs/reviews/briefs/doctrine-reference.md` at the tip,
2,389 lines, 27 checkboxes; R5 § A's verdicts: `copy 8, rewrite 9, copy the
habit 2, rewrite in T39's form 1, of 20 rows`, R5 C16): the rulings as one
lettered bullet in § 1, the membership block between markers in § 2 with its
sha256 prefix, § 5's five rules with the VM paragraph inside rule 3, § 7's
first five checkboxes as plan § 6b's contract, § 8's inherit list with
owners, § 9's register table read before cited, § 10's pointer table with
the seeding-error column, and the `Version 1` section with its self-checks.
What T41 adds to T40's table is the **currency** lens the order gives it
(`order.md:695`): per row, the patch's target version, the pin of each
device that applies it, whether it applies at that pin, its upstream status
as the header claims it, its backport status and the fork's reason, and
for the one configuration the four conf-diff counts each naming its side
(§ 4 Q4; § 5's generator). **R5 § B's recurring errata are written out of
it**: every `:N` read at the hash the sentence names; every count a tool's
line (`0 fork-own` is the inventory's rule and **1** is the fork-written
count, R5 § B item 2); the locale stated beside each sort (`LC_ALL=C`, the
build's); the placeholder check in its widened form; `reviewed-at:` the
dispatch tip and `fixed-at:` the lane's last commit; one heading per
generated section; no fetch where the floor says no network; the `#585`
lines owed, not conditional; the never-edited diff over the lane's own
commits. The rule, register and futro lines are the coordinator worktree's
at **`6a12ce2d73`** (R4's and R5's header; R1, R2 and R3 read the P1 tip
`2174265e9c` by hash); the lane re-reads them at `__COHASH__`.

## 1. Identity

- **Issue:** #688 `M6.P2 E1054/T41: patches-and-configs: kernel patches and
  configurations the shipped and test images apply` (OPEN, milestone
  `M6: Codebase renovation`, no labels, 1 comment, already retitled and
  parented: parent #1054 by the API, REST id `5992347647`; R5 § A, C14; `v1
  read`: `gh --repo pixelelated/distribution issue view 688 --json
  title,state,milestone,comments` prints the title, `OPEN`, `M6: Codebase
  renovation`, `1`). The pre-dispatch body is 27 lines with 5 generated
  checkboxes (`gh --repo pixelelated/distribution issue view 688 --json
  title,body,state`, the body hashed with or without a final newline: sha256
  prefix `5f82f7ac42f4345d`, proof K23 -- version 1's `2a5a2d8d6ea5be43` named
  no command). **Its sentences are
  cited here by content, never by line number**, because the kit rewrites the
  body from § 7 at dispatch (R5 § A, T39's ruling (i) carried): the paths
  sentence *"107 paths, 40,474 lines; 0 lines read, 0 of them fork-own
  (inventory at ..."* (R5 C14; R4 § 0); the tiers line *"vendor-carried
  107"* (R5 § H, already right); the generated VM line *"No test is
  proposed: a table slice is host analysis of the tree; a removal it proposes
  is proven on the GENERIC_X64 guest before it is a punch item."* (R4 item 23;
  R5 § D), replaced by ruling (h)'s sentence; the `reviewed-at:` and
  `fixed-at:` header lines, blank (R4 item 23); the audit-folder line
  `docs/audits/<date>-epic-m6-patches-shipped-kernel/`. The one comment is
  T40's PL-03 pointer (blitterbot, 2026-10-25T05:46:50Z: *"None of the 26
  overrides behind the 50 is a kernel override, so all 50 went to #689, and
  this issue gets none."*, R4 item 1) -- **T41 inherits no lead from T40**
  (T40's errata `patches-dead.md:441`: *"#688 has none"*, R5 § A).
- **The order's row.** Slice `patches-shipped-kernel` (`k: 41`) in
  `docs/reviews/slices.json`, area `patches-and-configs`, kind `table`, lens
  `package currency`, selector `{"globs": ["projects/ROCKNIX/devices/**",
  "projects/ROCKNIX/packages/linux*/**", "packages/linux*/**",
  "!projects/ROCKNIX/devices/{H700,GENERIC_X64}/linux/*.conf"], "reach":
  ["shipped", "test"]}`, read before none, depth `Local`, `depth_reason` *"a
  provenance table"* (R1 C02, C03; R5 § 0). `docs/reviews/order.md` § T41 is
  `:693-701` (`v1 read`: `sed -n '690,703p' docs/reviews/order.md`; R1 C02):
  its why *"one provenance row per kernel patch and configuration a shipped
  image or the test image applies (#339 criterion 2), split from the other
  shipped patches so each table is one session; the fork-written H700 kernel
  patch is read line by line here (gpt would move it to `device-h700`; it
  stays with the kernel's provenance, named as that slice's interacting
  subsystem)"*; its paths line *"107 paths, 40,474 lines, -- read, of which
  -- fork-own; 40,474 patch and config lines; reach shipped 103, test 4"*;
  its interacting subsystems *"the shipped device slices and the kernel
  recipe (`device-generic-x64-and-kernel`)"*; its closing evidence *"one row
  per patch; audit folder, lint PASS"*. The area epic #1054's table carries
  the same row (R1 C15) and its acceptance for T41 (`:28-29`, R4 item 23):
  every row an image applies carries origin, upstream status, the reason
  carried, the version made against and whether it still applies; a patch
  that should apply and does not is a `bug` with its code trace; `git diff
  --stat <dispatch tip> <tip> -- '*.patch' '*.conf'` empty on the branch.
- **What each figure counts** (R1 § 2; R3 § 0; R5 § 0). **107 paths and
  40,474 lines** are the inventory's `lines` column summed at its head
  `eb4763e3cc` (R1 C07: `lines: 40474 reach: {'shipped': 103, 'test': 4}
  tier: {'vendor-carried': 107}`; R3 C19: `MEMBERS: 107 LINES: 40474`; R5
  C15: `T41 rows 107 lines 40474`). **106 `.patch` and 1 `kernel-config`**
  (R1 C07: `lang: {'patch': 106, 'kernel-config': 1}`), the one
  configuration `projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf`,
  8,608 lines (R5 C16). **Reach `shipped` 103, `test` 4**: the four `test`
  rows are `projects/ROCKNIX/packages/linux/patches/7.0/`'s, reached by
  `GENERIC_X64-x86_64` alone (R5 C16; R1 C18). **Every row is tier
  `vendor-carried`** by the tool's rule (`tools/renovation-inventory`'s
  docstring lines 37-38, R1 C16: every `*.patch` and kernel `linux*.conf`
  under `packages/` or `projects/` is), so the order's *"-- read, of which --
  fork-own"* and the tool's `0 read 0 fork-own` (R1 C14) are right by that
  rule, and **the one fork-written row shows as `tier_note: fork-written`**
  (R1 C13: `tier_note values over the 107: 1 fork-written; 106 None;`) and
  as the one blob absent at the merge base (R1 C07) -- a lane told to find
  fork-written rows by `tier` finds none (R1 § 8 delta 3; R4 item 6; R5 § B
  item 2). `last_upstream_commit` is set on 106, `overlap` 0, no binary row
  (R1 C07). **Two line figures** (ruling (a)): the inventory's and `grep -c
  ''`'s **40,474** over the 107 at the P1 hash and at the inventory head, and
  `wc -l`'s **40,473**, one under, because
  `projects/ROCKNIX/devices/SM8550/patches/linux/0004-drm-msm-a6xx-Enable-IFPC-on-Adreno-740.patch`
  has no trailing newline (`wc -l 32 grep -c 33`, R1 C09; R4 item 14's
  *"29,508 against 29,507"* over SM8550's 56 rows is the same file). The 107
  did not change between the inventory head and the P1 hash (`IH..P1:` prints
  nothing, R1 C07), nor between the P1 hash and `next` `8ebaf8daad` over the
  member directories (`git diff --stat 2174265e9c next -- <the member dirs>`
  empty, R2 command 7), and all 107 are present at `6a12ce2d73` (R5 C15:
  `present 107 of 107`).
- **Provenance** (R1 § 5; R2 § 1; R4 item 5). **106 of the 107 blobs equal
  the merge base's** `c445081a59` (R1 C07: `blob vs merge base: SAME 106`,
  `ADDED 1`) -- upstream's as carried, `last_fork_commit None` on every row
  but one (R1 C09) -- and **one was added by the fork**:
  `projects/ROCKNIX/devices/H700/patches/linux/0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch`,
  38 lines, `cbf75c0b06` 2026-09-10 (the whole `MB..P1` diff over the 107:
  `1 file changed, 38 insertions(+)`, R1 C07; `From: ROCKNIX fork
  <noreply@rocknix.org>`, R1 C10; not an ancestor of `upstream/next`, R2
  command 8, R4 command 17). Six fork commits touch the 107 since the base,
  one non-merge (`cbf75c0b06`) and five merges of `upstream/next` (R1 C10:
  `all: 6 no-merges: 1 merges: 5`). **Upstream's side**, read in the
  coordinator's object store at the local ref `upstream/next` `651150fc88`
  (2026-10-24, *Merge pull request #3547*; `v1 read`: `git -C
  /workspace/repos/pixelelated/distribution rev-parse --short=10
  upstream/next` prints `651150fc88`; the inventory's own `upstream_head` is
  `c1f1746828`, 15 commits earlier, R1 C11): **eight upstream commits touch
  the 107 since the base, seven non-merge** (R1 C11), `diff MB..651150fc88`
  over the 107 is `5 files changed, 36 insertions(+), 515 deletions(-)`, and
  at `upstream/next` **101 of the 107 are byte-identical to P1, 4 changed, 2
  gone** (R1 C11): changed -- the SM8550 configuration (`c0980b2b71`
  2026-10-02, `5f56cd5150` 10-04, `6fbefc45c6` 10-18, `dcafa74090` 10-22; 14
  lines, R2 command 11), `0104-drm-panel-Add-Retroid-Pocket-6-panel.patch`
  (`abfdcfb57f`, one line) and **both `0010-msm-resource-cleanup.patch`
  copies** (`7.0/` and `7.2/`; `9416eec2c2` 2026-10-06 *"kernel: msm dp
  resource cleanup patch fix uninit pointer"*); gone --
  `mainline/0002-input-add-input-polldev-driver.patch` (moved by `fe5216ff69`,
  authored 2026-09-16 and committed 2026-10-09, *"rocknix-joypad: update
  version"*, proof K69, to `projects/ROCKNIX/devices/RK3326/patches/linux/003-input-add-input-polldev-driver.patch`,
  a rename with 0 changed lines, R1 C16) and the fork's own 0950. Upstream
  **added 12 files under the shipped kernel directories** since the base (R1
  C11: `12 A`): six under `7.2/` (`0011-drm-msm-signal-hw_done...`,
  `0012-...qos-lut...`, `0014-...scaled-fetch-line-width`,
  `0015-...sm8250-linear-danger-lut`,
  `0017-clk-qcom-blank-dsi-panels-before-dispcc-park`,
  `0018-...preload-seven-pixels...`), four under a new `7.2.6/` (for
  `RK3566|RK3576|S922X`, moved upstream to `7.2.11`; three of them symlinks to
  `7.2/`'s, R2 command 13), two under SM8550's `patches/linux/`
  (`0508-ROCKNIX-rp6-panel-frame-length-calibration.patch`,
  `0509-ROCKNIX-thor-...`). H700's `patches/linux/` holds 33 entries at P1
  (32 patches and the `.patch.disabled`) and 32 at upstream; SM8550's 56 at
  P1 against 58 at upstream (R1 C11). **The shipped kernels' pin did not move
  upstream**: `7.2` for H700 and SM8550 at `651150fc88` as at P1, `7.1.2` for
  GENERIC_X64 at both (R1 C16; R2 § 1); 64 upstream commits reach the 107
  since 2026-06-01 at `8ebaf8daad` (R5 C15).
- **The kernels the rows are claims about** (R1 § 4; R3 § 1.1; the override
  `projects/ROCKNIX/packages/linux/package.mk` at `2174265e9c`, 432 lines,
  **read as text, never sourced**; `v1 read`: `git show
  2174265e9c:projects/ROCKNIX/packages/linux/package.mk | sed -n
  '16,18p;29,40p'`): `PKG_PATCH_DIRS="${LINUX} mainline ${DEVICE} default"`
  (`:16`), `+=" mainline-rockchip"` for `RK*` (`:18`); `case ${DEVICE}`:
  **`H700|SM4450|SM6115|SM8250|SM8550|SM8650|SM8750` -> `PKG_VERSION="7.2"`**
  (`:29-30`, `PKG_SHA256` `f9fef3d14c0df538...` at `:31`, kernel.org;
  the recipe's own comment `:33-34`: *"the patch dir 7.2 is automatically
  added as it matches the version. When we move past 7.2, remember to add
  7.2 to patch dirs"*); **`RK3326|AMD64|GENERIC_X64` -> `PKG_VERSION="7.1.2"`**
  (`:36-37`, `PKG_SHA256` `37198c93727be247...` at `:38`) with
  `PKG_PATCH_DIRS+=" 7.0"` (`:40`); `RK3576|RK3566` `7.0.2` `+=" 7.0"`;
  `S922X|RK3399` `6.18.49`; RK3588 armbian `b8e62bed7476...`. `${LINUX}` is
  set in no ROCKNIX `options` file (R1 C08, C13: `LINUX=` only in the other
  projects'), so it is the empty word for every shipped and test plan;
  `patches/${DEVICE}` and `patches/default` do not exist under the override
  (R1 C13: `7.0`, `7.2`, `mainline-rockchip`, `mainline` only) -- ruling (o).
  `KERNEL_TARGET` is `Image` on H700 and SM8550, `bzImage` on GENERIC_X64
  (R1 C06). **The fork's whole change to the two kernel recipes since the
  base is `5 insertions(+), 5 deletions(-)`** (R1 C10, C16): `GENERIC_X64`
  added to the `RK3326|AMD64` group (`dc948f59aa` 2026-08-21) and
  `CONFIG_DEFAULT_HOSTNAME` kept at the literal `"ROCKNIX"` in both recipes
  (`3d7c075f63` 2026-10-02, D-WORKFLOW-123) -- T11's lines, read here as the
  context of the *current pin* column (ruling (c)). The generic
  `packages/linux/package.mk` (358 lines) is shadowed on every plan
  (`unreached`, T25's; its 277 patches T40's class (a), R1 § 2).
- **The coordinator's rulings, stated once; § 2's take-up table and § 3's
  leads point here** (D-WORKFLOW-189):
  (a) **The lane's tree** is its worktree
  `/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-kernel-688`
  on `feature/m6-patches-shipped-kernel-688`, **cut from the coordinator's
  tip (`__COHASH__`), which carries the P1 branch since `6a12ce2d73`** (`v1
  read`: `git merge-base --is-ancestor 2174265e9c HEAD` true at `6a12ce2d73`;
  R5 § H: *"equals `COHASH` ... no merge commit"*); **no dispatch merge**, so
  this brief carries no merge-hash placeholder and the acceptance's `DISPATCH_TIP` is
  `__COHASH__` (R5 § H). § 2's block runs at the P1 hash `2174265e9c` (its
  `W` is the P1 research clone, read by `git -C` only) and **the lane re-runs
  it at its tip**, recording both totals: **107 paths; 40,474 lines by
  `grep -c ''`, 40,473 by `wc -l`** -- one file without a trailing newline,
  named above -- and reach shipped 103 / test 4 (R1 C07, C09).
  (b) **Kind table, depth Local, lens package currency: one provenance row
  per path**, 106 `.patch` and 1 `linux.aarch64.conf` (SM8550's). **The five
  non-kernel rows the globs sweep in** -- the four H700 U-Boot patches
  (`u-boot-DDR3/patches/` and `u-boot-DDR4/patches/`, two byte-identical
  pairs: `0001-Update-dram_sun50i_h616.c.patch` 25 lines and
  `0002-sunxi-axp717-charge-only-boot.patch` 114, R1 § 2, R2 command 10) and
  the one `kernel-firmware` patch
  (`projects/ROCKNIX/packages/linux-firmware/kernel-firmware/patches/kernel-firmware-02-add-brcmfmac-43xxx-configs.patch`,
  188 lines) -- **are tabled here, labelled `non-kernel`**, their
  subsystem's owner named: T27 for U-Boot (`u-boot-DDR3`'s and
  `u-boot-DDR4`'s recipes, `device-h700.md:321` *"the two identical u-boot
  patch pairs (T41's)"*, R4 item 10), T11 for the firmware recipe (R1 § 8
  delta 4 names the recipes T27's and T11's, and the inventory agrees:
  `kernel-firmware/package.mk` is area `devices`, reach `shipped`, which
  T11's `projects/ROCKNIX/packages/**` select takes first; T42's `rest` holds
  only `patches-and-configs` paths -- version 1's T42 was the coordinator's
  error, corrected in version 2). The
  title says kernel, the globs say `devices/**`, and **the table follows the
  globs** (`KIND TOTAL K5 other 5 paths 466 lines`, R1 C07) -- a delta the
  brief records (§ 2).
  (c) **No patch, conf or recipe is edited.** A table slice changes nothing
  under `packages/`, `projects/` or `tools/` (T40's shape, D-WORKFLOW-209). A
  carried patch found wrong at the pin -- the unfixed
  `0010-msm-resource-cleanup.patch` in `7.0/` and `7.2/`, fixed upstream on
  2026-10-06 by `9416eec2c2` (R2 L-01; R1 § 9) -- is a **currency row and a
  `bug` naming upstream's fix**; the fix reaches the fork with the next
  upstream base merge (the integration's, #563/#559), never as a fork edit
  of a byte-identical carried patch. The fork's own commits on the recipes
  (`dc948f59aa`, `3d7c075f63`) are read, not touched.
  (d) **The two excluded kernel configurations are the device slices'**:
  H700's (`projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf`, 8,129
  lines, `last_fork_commit cbf75c0b06`) is **T27's**, GENERIC_X64's
  (`linux.x86_64.conf`, 7,754 lines, fork-own whole) is **T11's** (R1 C07's
  `CLAIMS` CONF lines; the order's negative glob, R1 § 1). T41 tables
  SM8550's conf -- never fork-changed (`+0 -0` against the base, R2 command
  9), **7 of 7 lines equal upstream at R4's read** (T28 `02:78-90` at
  `5a60d1c825`: *7 removed / 7 added against `651150fc88`, all upstream's*,
  R4 item 4) -- and cites the two excluded only where a row needs them: the
  ramoops patch's config half lives in H700's conf (a note in that row,
  T27's; ruling (e)).
  (e) **The fork-written H700 ramoops patch**
  (`projects/ROCKNIX/devices/H700/patches/linux/0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch`,
  `cbf75c0b06`, 2026-09-10, 38 lines; D-SYS-004 `decision-register.md:164`;
  fork #104) **is the one line-by-line row**: the DTS node against the
  decision's numbers -- 1 MiB at `0x4f000000` (`reg = <0x0 0x4f000000 0x0
  0x100000>`), 512 KiB console (`console-size = <0x80000>`), four 128 KiB
  dumps (`record-size = <0x20000>`), `max-reason = <2>` (R2 § 2 `:29-35`;
  `handheld-evidence.md` § The hang-to-reboot path says the same numbers)
  -- its config half in H700's conf (the six `+CONFIG` lines of
  `cbf75c0b06`: `WATCHDOG_SYSFS=y`, `PSTORE_CONSOLE=y`, `PSTORE_RAM=y`,
  `SOFTLOCKUP_DETECTOR=y`, `DETECT_HUNG_TASK=y`,
  `DEFAULT_HUNG_TASK_TIMEOUT=120`, R2 command 8; T27's), and **a `#585` line
  owed** (D-WORKFLOW-164; the upstream offer parked in #369 `:11`, R4 item
  15) -- written in `02` § The #585 lines owed, **never sent**
  (D-WORKFLOW-165). Its upstream status: not at `upstream/next` under this
  or a `ramoops` name (R1 C11: `ramoops-named patches at upstream/next: 0`;
  upstream's H700 conf still `# CONFIG_PSTORE_RAM is not set`, R2 command
  8); whether mainline 7.2 already carries a node at `0x4f000000` is the
  lane's tarball read (L-16). Its device fact (L29 of
  `docs/releases/device-facts.md`: never observed on a board) waits on a
  deliberate crash with a yes by name (D-QA-008) and is **not** this
  slice's to run.
  (f) **Currency against upstream at `651150fc88`** -- the commit the local
  ref `upstream/next` named when this brief was read; **the ref moves** (it
  read `50433c03cc`, 59 commits on, by 2026-11-02, proof K94), so every command
  names the commit, never the ref -- is read in the coordinator's object store
  (`git -C /workspace/repos/pixelelated/distribution show 651150fc88:<path>`,
  the lane's worktree sharing it; **no fetch**):
  the files upstream changed on the globs since the base `c445081a59` (R1
  C11: `101 SAME / 4 CHANGED / 2 GONE`; the 12 added under the shipped kernel
  directories), the moved polldev patch (`mainline/0002` to RK3326's
  directory, R2 L-14), the `rocknix-joypad` patch group upstream's recipe
  `:18` adds for `RK3326|RK3399|S922X|H700` (R1 § 10: no such directory
  under the override's `patches/` at `651150fc88`; its contents `[unverified]`,
  L-14), and **upstream's never-matching quoted `=~` regex** in that line
  (R2 L-02: `[[ "${DEVICE}" =~ "RK3326|RK3399|S922X|H700" ]]` is false for
  all five device names tested, true unquoted, R2 command 14) -- a
  D-WORKFLOW-164 one-liner for ROCKNIX, a `#585` line. **Each is a row or a
  lead with its disposition: the integration carries upstream's changes;
  the lane records and never applies them.**
  (g) **applies-at-pin is proved by `patch --dry-run` (or `git apply
  --check`) against the cached pinned kernel tarballs** --
  `/workspace/cache/rocknix-sources/linux/linux-7.2.tar.xz` for H700 and
  SM8550, `linux-7.1.2.tar.xz` for GENERIC_X64, their `.sha256` beside them
  (R3 § 1.4: 160,068,116 and 158,323,320 bytes; `v1 read`: `ls
  /workspace/cache/rocknix-sources/linux/` lists the three tarballs with
  `.sha256` and `.url`; the `.sha256` of 7.2 begins `f9fef3d14c0df538`, the
  recipe's `PKG_SHA256`) -- **extracting ONLY the files a patch touches into
  the lane's own scratch under `/workspace/tmp/m6-t41/`**, in
  `scripts/unpack:127-159`'s application order (R3 § 1.1, § 1.4; R1 § 3:
  `${PKG_DIR}/patches/*.patch`, `patches/${PATCH_ARCH}/`, the `PKG_PATCH_DIRS`
  package directories, `patches/${PKG_VERSION}/`, ..., the device's
  `patches/${PKG_NAME}/` last; within a glob the shell's sort, under
  `LC_ALL=C` as the container runs); the **`PATCH_ARCH` rule** `unpack:127-133`
  (`v1 read`: `x86` first on an `x86_64` target, else
  `${TARGET_KERNEL_PATCH_ARCH:-${TARGET_ARCH}}` for a kernel package: `x86`
  for GENERIC_X64, `aarch64` for both H700 and SM8550 plans, the `arm`
  userlands included, R1 C15, R3 § 1.1). **A hunk that fails is a lead, not
  a fix.** No build, no `scripts/unpack`, no `make kconfig-*`, no
  `tools/adjust_kernel_config` or `tools/check_kernel_config` run (both
  unpack and **write the tree's conf**, R3 § 1.3), no tarball extracted
  anywhere but that scratch, retired at stage H (D-INFRA-022). **Version 2
  extends the method to the five `non-kernel` rows** (the coordinator's ruling
  on version 1's open item 7): the four U-Boot patches by the same dry-run
  against `/workspace/cache/rocknix-sources/u-boot-DDR3/u-boot-DDR3-v2026.01.tar.gz`
  and `.../u-boot-DDR4/u-boot-DDR4-v2026.01.tar.gz` (top directory
  `u-boot-2026.01/`), the firmware patch against
  `.../kernel-firmware/kernel-firmware-20260309.tar.gz` (top directory
  `linux-firmware-20260309/`), each `.sha256` read against its recipe's
  `PKG_SHA256` first, only the touched files extracted into the same scratch;
  each row's cell names its own `applies-<recipe>.txt` line.
  (h) **No guest window.** D-WORKFLOW-187's line: *Can this be done on the
  VM? No -- the tree, the history and the cached tarballs show it; nothing a
  guest shows is a provenance fact.* T40 ran none (`03 § 3.6`: *"nothing here
  ran on a device or a guest"*, R3 § 3); 9 of the 107 reach the test image
  (the 4 `mainline/`, the 4 `7.0/`, the firmware patch, R3 § 3); R3 § 3
  recommends none. **This sentence is the VM line #688's body takes** at
  dispatch (§ 5 rule 3).
  (i) **Depth Local** (D-WORKFLOW-184: a provenance table; plan § 6c):
  `second-opinions/review-plan.json` records `local`, no reviewer,
  `tier_exception: D-WORKFLOW-184`; **the lint's Local proof at stage A** as
  T38's and T39's briefs put it -- T4's finished Local folder exported from
  `6ec78bbf8c` and linted by this tip's lint (`rc=0`, a line ending `PASS`),
  then a copy with `tier_exception` removed (`rc=1`, the `FAIL` line quoted)
  -- both quoted in `00` (§ 5's `# STAGE A`).
  (j) **The generator `tools/t41-tables.py` is T40's `tools/t40-tables.py`**
  (171 lines at `e863379cec`, read by `git -C
  /workspace/repos/pixelelated/distribution.worktrees/m6-patches-dead-687 show
  e863379cec:docs/audits/2026_10_25-epic-m6-patches-dead/tools/t40-tables.py`,
  never a checkout; R1 § 7 and R3 § 4 name its parts: the asserts at `:25-26`
  and `:33`, `header()` at `:46-63`, `hashes()` at `:74`, the classes
  `:95-112`, the three duplicate strictnesses `:116-120`, the modes `stats |
  provenance | coverage | shadowed | json` at `:132-171`) **with T41's columns
  added**: the patch's target version (from its header or content), the
  current pin per device (the recipe's `case ${DEVICE}` as text: `7.2`
  H700/SM8550, `7.1.2` GENERIC_X64), applies-at-pin, upstream status by
  header (`Link:` / `Upstream-Status:`; 4 rows carry one, R2 § 1), backport
  status, the fork's reason (the carrying commit's message), and the four
  conf-diff counts each naming its side (§ 5); **its asserts are the
  FAIL-first positive**, run before the table is written and recorded in
  `00`.
  (k) **The rule-document lead** -- `packaging-and-patches.md:91` (*"Kernel
  patches live under `packages/linux/patches/<DEVICE>/`"*) and
  `CLAUDE.md:148-149` (the same sentence; `v1 read`: `grep -n
  'packages/linux/patches/<DEVICE>'` prints `packaging-and-patches.md:91` and
  `CLAUDE.md:149`, the sentence beginning on `:148`) name a directory no
  ROCKNIX device applies (R2 L-09; R4 item 16; T40 § 2's class (a)) -- **is
  the coordinator's erratum** (T4's rules), inherited, never a lane edit
  (L-09). **The nineteen header-less patches** (R1 C13: `From:` on 87 of
  106; 19 without, 17 of them hand-made diffs with neither `From:` nor
  `Subject:`, two list exports whose `From:` the exporter dropped, R2 § 1)
  get their provenance from content and `git log --follow` at ROCKNIX;
  **`unknown` is a value the table carries, never a guess**
  (`upgrade-and-install.md` § Migrations: *attribute honestly*).
  (l) **The register row** for T41's ownership is written by the coordinator
  at dispatch: D-WORKFLOW-220 is T39's at its dispatch, so **T41 takes the
  next free ID after whichever dispatches first** -- written here as
  **D-WORKFLOW-22x**; the kit fills it (§ 9; R5 § F). At `6a12ce2d73` the
  highest decided WORKFLOW row was D-WORKFLOW-219; **at `2d3c57a625`, the
  coordinator's tip at this draft's close, D-WORKFLOW-220 is T39's**
  (dispatched 2026-11-01 06:22; `decision-register.md:781`, `v1 read`: the awk
  of § 9 prints `D-WORKFLOW-220`), **so T41's row is D-WORKFLOW-221** unless
  another WORKFLOW row lands before T41's dispatch.
  (m) **Session and branch:** the T3 session `m6-t3-emulators` (free since
  T37's close-out; R5 § G (f) named T39's brief as the other claimant, and
  T39 was dispatched to the T1 session `m6-t1-os-launch` at 06:22 --
  `2d3c57a625`'s subject, `v1 read` -- so the T3 session is T41's without
  contention), branch
  `feature/m6-patches-shipped-kernel-688`, the worktree of (a); the
  pointer's eleven keys (§ 10); **no retitle** (#688 is already
  `M6.P2 E1054/T41: ...` and parented, R5 C14).
  (n) **The kickoff addendum** goes in
  `docs/futros/2026-10-25-m6-patches-and-configs.md` after `:200` at
  dispatch (the futro is 200 lines, its last heading `## Errata, after T40's
  acceptance (2026-10-25)` at `:188`, R5 § C, C1; `v1 read`: `grep -c ''`
  prints `200`), in T38's six-paragraph shape (§ 9).
  (o) **The `.patch.disabled` files beside the live patches are T27's and
  T28's rows, not T41's**:
  `projects/ROCKNIX/devices/H700/patches/linux/0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled`
  (4,036 lines, `fad6d7d27a` 2026-03-27) and
  `projects/ROCKNIX/devices/SM8550/patches/linux/0053-add-hynitron-touchscreen.patch.disabled`
  (20,593 lines, `aa458af6f9` 2026-06-29), both still at `upstream/next`,
  area `devices`, tier `upstream-carried` (R1 C13, C16; R4 item 13); the
  table names them as context so a reader of the directory is not surprised,
  and does not row them. **`${LINUX}`, `patches/${DEVICE}` and `default` in
  `PKG_PATCH_DIRS` resolve to nothing** for every shipped and test plan
  (R1 § 3; R2 § 0, L-15) and are a recorded fact, not a defect to fix here.
  (p) **Every lane turn ends on a question on #688 or on the stage's
  checkpoint post, never on a progress post**; the lane files its own audit
  issue (stage D) and a `bug` per defect it proves (D-WORKFLOW-189); **a fix
  never lands** (ruling (c)); questions of scope come to the coordinator
  through #688.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md`, the plan or any other
  `docs/reviews/` file, file a Backlog issue, post on #346, #585, #1054, #369,
  #563 or #559, or decide a question of scope: those are the coordinator's,
  reached through #688, one question at a time. What it does file: its own
  audit punch-list issue (stage D) and a `bug` issue for each defect it
  proves (ruling (p); D-WORKFLOW-187) -- here the unfixed
  `0010-msm-resource-cleanup.patch` by ruling (c), and any patch a shipped
  image should apply and does not (#1054 criterion 6). **A fix never lands
  on this branch** (ruling (c); D-WORKFLOW-209): a defect in a carried patch
  is a `bug` naming upstream's fix and the integration that brings it. A
  finding in a rule, `CLAUDE.md`, `AGENTS.md` or a register is the
  coordinator's (T4's read, #651; ruling (k)); a finding in a kernel recipe
  is T11's; in a device's conf, `options`, device tree or U-Boot recipe T27's
  or T28's; in the firmware recipe T11's; in an unshipped device's patches
  T43's (§ 8).
- **One worktree, one session, and three hash placeholders.** The
  distribution's **`feature/m6-patches-shipped-kernel-688`** at
  **`/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-kernel-688`**
  (both absent before dispatch, R5 C15), created by the coordinator, **cut
  from `feature/m6-renovation-plan-346` at `__COHASH__`**, which carries
  `feature/m6-p1-survey-641` (`2174265e9c`) since `6a12ce2d73` (ruling (a))
  -- no merge commit, so the lane's first tip is `__COHASH__` itself -- with
  the lane's pointer seeded. **There is no EmulationStation worktree**:
  nothing in the 107 is EmulationStation's. **Three placeholders stand in
  this brief for hashes that do not exist until dispatch:** `__COHASH__`
  (the coordinator's tip the branch is cut from, the dispatch tip),
  `__TIPHASH__` (the lane's own tip as it moves; at stage A it is
  `__COHASH__`) and `__V2HASH__` (this brief's commit on the coordinator's
  branch at dispatch, after the stranger's proof makes version 2; version 1
  has no dispatch hash). The dispatch comment on #688 and the seeded pointer
  carry their values; the lane reads them there, never guesses them, and
  § 9's placeholder check runs on every artifact. **No other lane's slice is
  these paths**: every one of the 107 is claimed by T41 alone (R1 C14:
  `unassigned: 0`, `ambiguous: 0`; the block's `TREE-SIDE` lines). Until the
  dispatch comment exists the pointer is not seeded and nothing starts.
  Anything temporary goes under **`/workspace/tmp/m6-t41/`** after `df -i`,
  never `/tmp` (R5 § H).
- **Review depth: Local** (plan § 6c: *"a dead-end table, a provenance
  table, a doctrine read | Local: the executor alone; the lint and the counts
  are the check"*; ruling (i)). **No external reviewer, no `npm install`, no
  Facilitator call, no `tools/council/run`.** `second-opinions/review-plan.json`
  is still written, in T4's plan's shape (read at stage A from T4's tip
  `6ec78bbf8c` as T39's § 1 does): depth `local`, the primary as that plan
  writes it, lab `anthropic`, reviewers `[]`, `tier_exception`
  `D-WORKFLOW-184` and a `reason` naming plan § 6c's row. The code-auditor
  skill's Phase 4.6 is recorded as *not applicable at Local depth*; Phase 4.5
  is done in full, and § 5's rule 4 -- what result would have produced a FAIL
  -- is asked of every PASS, because nobody else asks it here.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at stage
  A (T40's `:94-95`; T39's). **The session is ruling (m)'s**,
  `m6-t3-emulators`; its `cwd` is an earlier lane's worktree (R5 C15:
  `.../m6-emulators-libretro-650`), so the dispatch names the new worktree
  and the lane `cd`s there first.
- **The first commands** are § 5's `# STAGE A` block, whole and in order,
  after the pointer's eleven keys (§ 10) and before the membership block
  (§ 2). It carries no `git fetch` line: a by-hash read needs none, and the
  never-run list forbids it (§ 10; T40's errata at acceptance, R5 § B item
  7).

## 2. Scope

**The membership, by the block that defines it** (run from the lane's
worktree, whose `docs/reviews/{slices,inventory,areas}.json` are the P1
branch's at `2174265e9c` -- sha256 prefixes `49bc2745664e52f4`
(`slices.json`), `d17b9cac4b2c2245` (`inventory.json`) and
`985f742cfd4a2138` (`areas.json`), R1 C02, the four inventory files
byte-identical between P1 and `6a12ce2d73` by their blob ids, R1 C01; § 5's
`# STAGE A` checks all three before the block runs). The script is T39's
`membership.py` rewritten for a **glob-and-reach** slice (R1 § 6): rows of
`tree == "distribution"`, the slice id `patches-shipped-kernel`, the labels
`in-T41` / `not-in-T41`. The tree-side proof is **`TREE-SIDE`** over the
slice's own four globs **and** the `patches-and-configs` area globs applied
to `ls-tree -r` at the inventory head and at the P1 hash (1,092 paths match
the slice's globs, 771 of those the area's), with the reach filter -- the
one input no tree can give -- read from the inventory per path and counted
by value (`unreached 281, unshipped 383, shipped 103, test 4`); `GROUPS` is
by kind and directory; `reachable_by:` and `buildable_by:` are counted;
**`CLAIMS`** lists every area row under the slice's positive globs that is
not the slice's, by owner and reach, naming the 14 `CONF` rows one by one;
**`NAMED`** answers for the recipes, `scripts/unpack`, the options files and
the three shipped-and-test configurations; **`AREA BY SLICE`** sizes every
slice of the area, the partition T40's, T42's and T43's figures are checked
against; the line counts run over all 107 rows (none binary) and every blob
is compared with the merge base (`SAME` / `ADDED` / `CHANGED`). **`W` is the
P1 research clone `/workspace/tmp/m6-coordinator/t11-research/tree`, read by
`git -C` only, and `P1=2174265e9c`; `MB` is the distribution merge base
`c445081a59`.** Keyword arguments are spaced `key = lambda`. The heredoc is
saved once and run twice -- first against `/dev/null` to make the paths file
from its own TSV, then against that file to prove equality. **The text below
is R1's `block.sh` byte for byte** (148 lines, 11,779 bytes, sha256 prefix
`4d300124a6bf116f`, R1 C07, C18; R1 re-extracted it from its own text, re-ran
it from a fresh scratch and diffed the output against the expected lines:
*"re-run rc=0 lines=99; diff against the Expected: 0 differing lines
(identical)"*, R1 C18; `v1 read`: the same extraction from R1 by its markers
prints `4d300124a6bf116f`, `11779` bytes, `148` lines). The lane extracts it
from this brief at `__V2HASH__` by its markers, never retypes it, and checks
the prefix (§ 5's `# STAGE A`):

<!-- t41 block.sh begin -->
```bash
mkdir -p .qa-scratch/t41
cat > .qa-scratch/t41/membership.py <<'PYEOF'
import json, re, sys, collections
CODE = {"shell","python","recipe","c","c++","c-header","c++-header","javascript","typescript","make","cmake","systemd","udev","script","perl","lua","rust","go","assembly","shader","docker","kconfig","html","css"}
SID = "patches-shipped-kernel"
def gre(g):
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i]=="?": out+="[^/]"; i+=1
        elif g[i]=="{":
            j=g.index("}",i); out+="(?:"+"|".join(gre(x) for x in g[i+1:j].split(","))+")"; i=j+1
        else: out+=re.escape(g[i]); i+=1
    return out
def compile_globs(globs):
    inc=collections.defaultdict(list); exc=collections.defaultdict(list)
    for g in globs:
        neg=g.startswith("!"); g=g[1:] if neg else g
        tree="es" if g.startswith("es:") else "distribution"
        g=g[3:] if tree=="es" else g
        (exc if neg else inc)[tree].append(re.compile(gre(g)+r"\Z"))
    return inc,exc
def gm(comp,p,t="distribution"):
    inc,exc=comp
    return any(r.match(p) for r in inc.get(t,())) and not any(r.match(p) for r in exc.get(t,()))
doc=json.load(open("docs/reviews/slices.json"))
sl=[]
for s in doc["slices"]:
    sels=s.get("select",{}); sels=sels if isinstance(sels,list) else [sels]
    comp=[]
    for sel in sels:
        comp.append((set(sel.get("areas",[s["area"]])), compile_globs(sel["globs"]) if sel.get("globs") else None,
                     set(sel["reach"]) if sel.get("reach") else None, bool(sel.get("rest")), set(sel["tier"]) if sel.get("tier") else None))
    sl.append((s,comp))
ar=json.load(open("docs/reviews/areas.json")); ar=ar["areas"] if isinstance(ar,dict) else ar
PCA=compile_globs([a for a in ar if a["area"]=="patches-and-configs"][0]["globs"])
ME=[s for s,_ in sl if s["id"]==SID][0]; MYG=compile_globs(ME["select"]["globs"]); MYR=set(ME["select"]["reach"])
POS=compile_globs([g for g in ME["select"]["globs"] if not g.startswith("!")])
inv=json.load(open("docs/reviews/inventory.json"))
hd=inv["header"]["distribution"]
print("distribution head:",hd["head"]); print("distribution merge_base:",hd["merge_base"]); print("distribution upstream:",hd["upstream"],hd["upstream_head"])
print("header keys:",sorted(inv["header"].keys())); print("shipped_devices:",inv["header"].get("shipped_devices"),"test_devices:",inv["header"].get("test_devices"))
cols=inv["columns"]; print("columns:",cols)
rows=[dict(zip(cols,r)) for r in inv["rows"]]
def match(row,areas,comp,reach,tier):
    if row["area"] not in areas: return False
    if reach and row["reach"] not in reach: return False
    if tier and row["tier"] not in tier: return False
    if comp is None: return True
    return gm(comp,row["path"],row["tree"])
def hits(row):
    non=[s["id"] for s,c in sl if any(not rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)]
    if non: return non,"non-rest"
    return [s["id"] for s,c in sl if any(rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)],"rest"
kof={s["id"]:s["k"] for s,_ in sl}
mine=sorted((r for r in rows if r["tree"]=="distribution" and hits(r)[0]==[SID]), key = lambda r:r["path"])
want=[l.strip() for l in open(sys.argv[1]) if l.strip()]
got=[r["path"] for r in mine]
print("mine:",len(got),"paths.txt:",len(want),"equal:",got==want)
print("only-mine:",sorted(set(got)-set(want))); print("only-paths.txt:",sorted(set(want)-set(got)))
c=collections.Counter
print("lines:",sum(r["lines"] or 0 for r in mine),"reach:",dict(c(r["reach"] for r in mine)),"tier:",dict(c(r["tier"] for r in mine)))
print("lang:",dict(c(r["language"] for r in mine)),"area:",dict(c(r["area"] for r in mine)))
print("fork-own lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="fork-own"),"upstream-carried lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="upstream-carried"),"vendor-carried lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="vendor-carried"))
rd=[r for r in mine if r["language"] in CODE and r["tier"]!="vendor-carried" and r["reach"]!="unreached"]
print("read lines:",sum((r["lines"] or 0) for r in rd),"of which fork-own:",sum((r["lines"] or 0) for r in rd if r["tier"]=="fork-own"),"read rows:",[(r["path"],r["language"],r["lines"]) for r in rd])
print("overlap:",sum(1 for r in mine if r["overlap"]),"last_upstream_commit set:",sum(1 for r in mine if r["last_upstream_commit"]),"binary (lines None):",[r["path"] for r in mine if r["lines"] is None])
print("fork-own rows:",[(r["path"],r["lines"],r["last_fork_commit"]) for r in mine if r["tier"]=="fork-own"])
print("reachable_by:",dict(c(tuple(r["reachable_by"]) if isinstance(r["reachable_by"],list) else r["reachable_by"] for r in mine)))
print("buildable_by:",dict(c(tuple(r["buildable_by"]) if isinstance(r["buildable_by"],list) else r["buildable_by"] for r in mine)))
def kind(p):
    m=re.match(r"packages/linux/patches/([^/]+)/",p)
    if m: return "K1 packages/linux/patches/<dir>/", m.group(1)
    m=re.match(r"projects/ROCKNIX/packages/(linux[^/]*)/patches/([^/]+)/",p)
    if m: return "K2 projects/ROCKNIX/packages/%s/patches/<dir>/" % m.group(1), m.group(2)
    m=re.match(r"projects/ROCKNIX/devices/([^/]+)/patches/([^/]+)/",p)
    if m: return "K3 projects/ROCKNIX/devices/<DEVICE>/patches/%s/" % m.group(2), m.group(1)
    m=re.match(r"projects/ROCKNIX/devices/([^/]+)/linux/linux[^/]*\.conf\Z",p)
    if m: return "K4 projects/ROCKNIX/devices/<DEVICE>/linux/linux*.conf", m.group(1)
    return "K5 other", p.rsplit("/",1)[0]
print("GROUPS (kind | dir: paths lines | shipped test | fork-own upstream-carried vendor-carried)")
g=collections.defaultdict(lambda:[0,0,0,0,0,0,0])
for r in mine:
    x=g[kind(r["path"])]; n=r["lines"] or 0; x[0]+=1; x[1]+=n
    x[2 if r["reach"]=="shipped" else 3]+=1
    x[{"fork-own":4,"upstream-carried":5,"vendor-carried":6}[r["tier"]]]+=1
for k in sorted(g): print("  %-58s %-14s %4d %6d | %4d %4d | %3d %3d %3d" % ((k[0],k[1])+tuple(g[k])))
kt=collections.defaultdict(lambda:[0,0])
for k,v in g.items(): kt[k[0]][0]+=v[0]; kt[k[0]][1]+=v[1]
for k in sorted(kt): print("  KIND TOTAL %-50s %4d %6d" % (k,kt[k][0],kt[k][1]))
print("GROUPS TOTAL", len(mine), sum(v[1] for v in g.values()), "groups", len(g))
print("TSV"); print("\t".join(cols))
for r in mine: print("\t".join(str(r.get(k)) for k in cols))
byp={r["path"]:r for r in rows if r["tree"]=="distribution"}
print("TREE-SIDE (the slice's globs and the patches-and-configs area globs over ls-tree; reach from the inventory)")
for tf in sys.argv[2:]:
    ps=[l.strip() for l in open(tf) if l.strip()]
    mg=[p for p in ps if gm(MYG,p)]; ma=[p for p in mg if gm(PCA,p)]
    print(tf,"glob-matched:",len(mg),"also in area globs:",len(ma),"by inventory reach:",dict(c(byp[p]["reach"] if p in byp else "not-in-inventory" for p in ma)))
    der=sorted(p for p in ma if p in byp and byp[p]["reach"] in MYR)
    print(tf,"derived:",len(der),"equal to mine:",der==got,"only-derived:",sorted(set(der)-set(got)),"only-mine:",sorted(set(got)-set(der)))
print("CLAIMS (area rows under the slice's positive globs, not in the slice: owner, reach)")
cl=collections.Counter(); cll=collections.Counter()
for r in rows:
    if r["tree"]=="distribution" and r["area"]=="patches-and-configs" and gm(POS,r["path"]) and r["path"] not in got:
        h,kd=hits(r); k=(tuple((x,kof[x]) for x in h),kd,r["reach"]); cl[k]+=1; cll[k]+=(r["lines"] or 0)
        if r["path"].endswith(".conf"): print("  CONF",r["path"],"->",[(x,kof[x]) for x in h],kd,"reach",r["reach"],"tier",r["tier"],"lines",r["lines"],"last_fork_commit",r["last_fork_commit"])
for k,v in sorted(cl.items(), key = lambda kv:-kv[1]): print("  ",v,"paths",cll[k],"lines",k)
print("NAMED")
for p in ["packages/linux/package.mk","projects/ROCKNIX/packages/linux/package.mk","scripts/unpack","projects/ROCKNIX/options","projects/ROCKNIX/devices/H700/options","projects/ROCKNIX/devices/SM8550/options","projects/ROCKNIX/devices/GENERIC_X64/options","projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf","projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf","projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf"]:
    r=byp.get(p)
    if not r: print(" ",p,"NOT IN INVENTORY"); continue
    h,kd=hits(r); print(" ",p,"in-T41" if p in got else "not-in-T41",kd,[(x,kof[x]) for x in h],"tier",r["tier"],"reach",r["reach"],"lines",r["lines"],"lang",r["language"],"area",r["area"],"last_fork_commit",r["last_fork_commit"])
print("AREA BY SLICE (patches-and-configs: tree, owning slices, reach: paths lines)")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["area"]=="patches-and-configs":
        h,kd=hits(r); k=(r["tree"],tuple((x,kof[x]) for x in h),r["reach"]); cnt[k]+=1; ln[k]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:(kv[0][1],kv[0][2])): print(" ",v,"paths",ln[k],"lines",k)
st=collections.Counter(); stl=collections.Counter()
for r in rows:
    if r["area"]=="patches-and-configs":
        h,kd=hits(r); k=tuple((x,kof[x]) for x in h); st[k]+=1; stl[k]+=(r["lines"] or 0)
for k,v in sorted(st.items(), key = lambda kv:kv[0]): print("  SLICE TOTAL",v,"paths",stl[k],"lines",k)
PYEOF
W=/workspace/tmp/m6-coordinator/t11-research/tree; P1=2174265e9c; MB=c445081a59
echo "MB type: $(git -C "$W" cat-file -t "$MB")"
IH=$(python3 -I -c 'import json; print(json.load(open("docs/reviews/inventory.json"))["header"]["distribution"]["head"])')
git -C "$W" ls-tree -r --name-only "$IH" > .qa-scratch/t41/tree-ih.txt
git -C "$W" ls-tree -r --name-only "$P1" > .qa-scratch/t41/tree-p1.txt
python3 -I .qa-scratch/t41/membership.py /dev/null > .qa-scratch/t41/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^TREE-SIDE/{p=0} p && $1=="distribution" {print $2}' .qa-scratch/t41/block-1.txt > .qa-scratch/t41/paths.txt
python3 -I .qa-scratch/t41/membership.py .qa-scratch/t41/paths.txt .qa-scratch/t41/tree-ih.txt .qa-scratch/t41/tree-p1.txt > .qa-scratch/t41/block-2.txt
awk -F'\t' '/^TSV$/{p=1;getline;for(i=1;i<=NF;i++)ix[$i]=i;next} /^TREE-SIDE/{p=0} p && $1=="distribution" && $ix["lines"]!="None" {print $ix["path"]}' .qa-scratch/t41/block-2.txt > .qa-scratch/t41/text.txt
wc -l .qa-scratch/t41/paths.txt .qa-scratch/t41/text.txt
awk '/^TSV$/{s=1} /^TREE-SIDE/{s=0} !s' .qa-scratch/t41/block-2.txt | cut -c1-600
while IFS= read -r p; do git -C "$W" show "$P1:$p" | wc -l; done < .qa-scratch/t41/text.txt | awk '{s+=$1} END {print "wc -l, the text rows at the P1 hash:", s}'
while IFS= read -r p; do git -C "$W" show "$P1:$p" | /usr/bin/grep -c ''; done < .qa-scratch/t41/text.txt | awk '{s+=$1} END {print "grep -c, the text rows at the P1 hash:", s}'
while IFS= read -r p; do git -C "$W" show "$IH:$p" | /usr/bin/grep -c ''; done < .qa-scratch/t41/text.txt | awk '{s+=$1} END {print "grep -c, the text rows at the inventory head:", s}'
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t41/paths.txt | wc -l | sed 's/^/present at the merge base: /'
while IFS= read -r p; do a=$(git -C "$W" rev-parse -q --verify "$P1:$p"); b=$(git -C "$W" rev-parse -q --verify "$MB:$p" 2>/dev/null); if [ -z "$b" ]; then echo "ADDED $p"; elif [ "$a" = "$b" ]; then echo "SAME $p"; else echo "CHANGED $p"; fi; done < .qa-scratch/t41/paths.txt > .qa-scratch/t41/mb-compare.txt
awk '{n[$1]++} END {for (k in n) print "blob vs merge base:", k, n[k]}' .qa-scratch/t41/mb-compare.txt | sort
/usr/bin/grep -v '^SAME' .qa-scratch/t41/mb-compare.txt
xargs -d '\n' -a .qa-scratch/t41/paths.txt git -C "$W" diff --shortstat "$MB" "$P1" -- | sed 's/^/MB..P1:/'
xargs -d '\n' -a .qa-scratch/t41/paths.txt git -C "$W" diff --shortstat "$IH" "$P1" -- | sed 's/^/IH..P1:/'
echo "(end)"
```
<!-- t41 block.sh end -->

Expected (the first pass, with no paths file, writes `mine: 107 paths.txt: 0
equal: False` into `block-1.txt`; the block prints these lines, R1 C07's, byte
for byte -- the TSV rows between `TSV` and `TREE-SIDE` are left out by the
block's own `awk`, and the `buildable_by:` line is cut at 600 characters by
the block's own `cut`; R1 C18's re-run from a fresh scratch printed them
identically):

<!-- t41 block expected begin -->
```
MB type: commit
  107 .qa-scratch/t41/paths.txt
  107 .qa-scratch/t41/text.txt
  214 total
distribution head: eb4763e3cc9bcd729830cd85f1719bbd4f28db10
distribution merge_base: c445081a59518f37d9776e5412dd7b14910696f7
distribution upstream: upstream/next c1f1746828ca47dfc751ffe44bb47b6b259883d7
header keys: ['configs', 'distribution', 'es', 'escaped_rows', 'generated', 'generator', 'plan_runner', 'seconds', 'shipped_devices', 'test_devices']
shipped_devices: ['H700', 'SM8550'] test_devices: ['GENERIC_X64']
columns: ['tree', 'path', 'area', 'tier', 'tier_note', 'overlap', 'language', 'lines', 'patches', 'last_fork_commit', 'last_upstream_commit', 'reach', 'reachable_by', 'buildable_by', 'shadowed_by']
mine: 107 paths.txt: 107 equal: True
only-mine: []
only-paths.txt: []
lines: 40474 reach: {'shipped': 103, 'test': 4} tier: {'vendor-carried': 107}
lang: {'patch': 106, 'kernel-config': 1} area: {'patches-and-configs': 107}
fork-own lines: 0 upstream-carried lines: 0 vendor-carried lines: 40474
read lines: 0 of which fork-own: 0 read rows: []
overlap: 0 last_upstream_commit set: 106 binary (lines None): []
fork-own rows: []
reachable_by: {('H700-aarch64',): 4, ('H700-aarch64', 'H700-arm'): 32, ('SM8550-aarch64', 'SM8550-arm'): 56, ('GENERIC_X64-x86_64', 'H700-aarch64', 'SM8550-aarch64'): 1, ('GENERIC_X64-x86_64',): 4, ('H700-aarch64', 'H700-arm', 'SM8550-aarch64', 'SM8550-arm'): 6, ('GENERIC_X64-x86_64', 'H700-aarch64', 'H700-arm', 'SM8550-aarch64', 'SM8550-arm'): 4}
buildable_by: {(): 92, ('AMD64-x86_64', 'RK3326-aarch64', 'RK3399-aarch64', 'RK3566-aarch64', 'RK3576-aarch64', 'RK3588-aarch64', 'S922X-aarch64', 'SM4450-aarch64', 'SM6115-aarch64', 'SM8250-aarch64', 'SM8650-aarch64', 'SM8750-aarch64'): 1, ('AMD64-x86_64', 'RK3326-aarch64', 'RK3326-arm', 'RK3566-aarch64', 'RK3566-arm', 'RK3576-aarch64', 'RK3576-arm'): 4, ('SM4450-aarch64', 'SM4450-arm', 'SM6115-aarch64', 'SM6115-arm', 'SM8250-aarch64', 'SM8250-arm', 'SM8650-aarch64', 'SM8750-aarch64'): 6, ('AMD64-x86_64', 'RK3326-aarch64', 'RK3326-arm', 'RK3399-aarch64', 'RK3399-arm', 'RK3566-aarch64', 'RK356
GROUPS (kind | dir: paths lines | shipped test | fork-own upstream-carried vendor-carried)
  K2 projects/ROCKNIX/packages/linux/patches/<dir>/          7.0               4    585 |    0    4 |   0   0   4
  K2 projects/ROCKNIX/packages/linux/patches/<dir>/          7.2               6    651 |    6    0 |   0   0   6
  K2 projects/ROCKNIX/packages/linux/patches/<dir>/          mainline          4    648 |    4    0 |   0   0   4
  K3 projects/ROCKNIX/devices/<DEVICE>/patches/linux/        H700             32   8616 |   32    0 |   0   0  32
  K3 projects/ROCKNIX/devices/<DEVICE>/patches/linux/        SM8550           55  20900 |   55    0 |   0   0  55
  K4 projects/ROCKNIX/devices/<DEVICE>/linux/linux*.conf     SM8550            1   8608 |    1    0 |   0   0   1
  K5 other                                                   projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/patches    2    139 |    2    0 |   0   0   2
  K5 other                                                   projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/patches    2    139 |    2    0 |   0   0   2
  K5 other                                                   projects/ROCKNIX/packages/linux-firmware/kernel-firmware/patches    1    188 |    1    0 |   0   0   1
  KIND TOTAL K2 projects/ROCKNIX/packages/linux/patches/<dir>/    14   1884
  KIND TOTAL K3 projects/ROCKNIX/devices/<DEVICE>/patches/linux/   87  29516
  KIND TOTAL K4 projects/ROCKNIX/devices/<DEVICE>/linux/linux*.conf    1   8608
  KIND TOTAL K5 other                                              5    466
GROUPS TOTAL 107 40474 groups 9
TREE-SIDE (the slice's globs and the patches-and-configs area globs over ls-tree; reach from the inventory)
.qa-scratch/t41/tree-ih.txt glob-matched: 1092 also in area globs: 771 by inventory reach: {'unreached': 281, 'unshipped': 383, 'shipped': 103, 'test': 4}
.qa-scratch/t41/tree-ih.txt derived: 107 equal to mine: True only-derived: [] only-mine: []
.qa-scratch/t41/tree-p1.txt glob-matched: 1092 also in area globs: 771 by inventory reach: {'unreached': 281, 'unshipped': 383, 'shipped': 103, 'test': 4}
.qa-scratch/t41/tree-p1.txt derived: 107 equal to mine: True only-derived: [] only-mine: []
CLAIMS (area rows under the slice's positive globs, not in the slice: owner, reach)
  CONF projects/ROCKNIX/devices/AMD64/linux/linux.x86_64.conf -> [('patches-unshipped', 43)] non-rest reach unshipped tier vendor-carried lines 12445 last_fork_commit None
  CONF projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf -> [('device-generic-x64-and-kernel', 11)] non-rest reach test tier vendor-carried lines 7754 last_fork_commit cbf75c0b06 2026-09-10
  CONF projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf -> [('device-h700', 27)] non-rest reach shipped tier vendor-carried lines 8129 last_fork_commit cbf75c0b06 2026-09-10
  CONF projects/ROCKNIX/devices/RK3326/linux/linux.aarch64.conf -> [('patches-unshipped', 43)] non-rest reach unshipped tier vendor-carried lines 7218 last_fork_commit None
  CONF projects/ROCKNIX/devices/RK3399/linux/linux.aarch64.conf -> [('patches-unshipped', 43)] non-rest reach unshipped tier vendor-carried lines 6908 last_fork_commit None
  CONF projects/ROCKNIX/devices/RK3566/linux/linux.aarch64.conf -> [('patches-unshipped', 43)] non-rest reach unshipped tier vendor-carried lines 7739 last_fork_commit None
  CONF projects/ROCKNIX/devices/RK3576/linux/linux.aarch64.conf -> [('patches-unshipped', 43)] non-rest reach unshipped tier vendor-carried lines 8292 last_fork_commit None
  CONF projects/ROCKNIX/devices/RK3588/linux/linux.aarch64.conf -> [('patches-unshipped', 43)] non-rest reach unshipped tier vendor-carried lines 8894 last_fork_commit None
  CONF projects/ROCKNIX/devices/S922X/linux/linux.aarch64.conf -> [('patches-unshipped', 43)] non-rest reach unshipped tier vendor-carried lines 6976 last_fork_commit None
  CONF projects/ROCKNIX/devices/SM4450/linux/linux.aarch64.conf -> [('patches-unshipped', 43)] non-rest reach unshipped tier vendor-carried lines 8568 last_fork_commit None
  CONF projects/ROCKNIX/devices/SM6115/linux/linux.aarch64.conf -> [('patches-unshipped', 43)] non-rest reach unshipped tier vendor-carried lines 8513 last_fork_commit None
  CONF projects/ROCKNIX/devices/SM8250/linux/linux.aarch64.conf -> [('patches-unshipped', 43)] non-rest reach unshipped tier vendor-carried lines 8441 last_fork_commit None
  CONF projects/ROCKNIX/devices/SM8650/linux/linux.aarch64.conf -> [('patches-unshipped', 43)] non-rest reach unshipped tier vendor-carried lines 8603 last_fork_commit None
  CONF projects/ROCKNIX/devices/SM8750/linux/linux.aarch64.conf -> [('patches-unshipped', 43)] non-rest reach unshipped tier vendor-carried lines 8632 last_fork_commit None
   383 paths 325382 lines ((('patches-unshipped', 43),), 'non-rest', 'unshipped')
   281 paths 92480 lines ((('patches-dead', 40),), 'non-rest', 'unreached')
   1 paths 7754 lines ((('device-generic-x64-and-kernel', 11),), 'non-rest', 'test')
   1 paths 8129 lines ((('device-h700', 27),), 'non-rest', 'shipped')
NAMED
  packages/linux/package.mk not-in-T41 non-rest [('devices-unshipped', 25)] tier fork-own reach unreached lines 358 lang recipe area devices last_fork_commit 3d7c075f63 2026-10-02
  projects/ROCKNIX/packages/linux/package.mk not-in-T41 non-rest [('device-generic-x64-and-kernel', 11)] tier fork-own reach shipped lines 432 lang recipe area devices last_fork_commit 3d7c075f63 2026-10-02
  scripts/unpack not-in-T41 non-rest [('build-engine', 5)] tier upstream-carried reach n/a lines 228 lang shell area build-engine last_fork_commit None
  projects/ROCKNIX/options not-in-T41 non-rest [('device-generic-x64-and-kernel', 11)] tier upstream-carried reach shipped lines 41 lang shell area devices last_fork_commit None
  projects/ROCKNIX/devices/H700/options not-in-T41 non-rest [('device-h700', 27)] tier upstream-carried reach shipped lines 84 lang shell area devices last_fork_commit None
  projects/ROCKNIX/devices/SM8550/options not-in-T41 non-rest [('device-sm8550', 28)] tier upstream-carried reach shipped lines 81 lang shell area devices last_fork_commit None
  projects/ROCKNIX/devices/GENERIC_X64/options not-in-T41 non-rest [('device-generic-x64-and-kernel', 11)] tier fork-own reach test lines 91 lang shell area devices last_fork_commit bed8e2bb1e 2026-10-05
  projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf not-in-T41 non-rest [('device-h700', 27)] tier vendor-carried reach shipped lines 8129 lang kernel-config area patches-and-configs last_fork_commit cbf75c0b06 2026-09-10
  projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf not-in-T41 non-rest [('device-generic-x64-and-kernel', 11)] tier vendor-carried reach test lines 7754 lang kernel-config area patches-and-configs last_fork_commit cbf75c0b06 2026-09-10
  projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf in-T41 non-rest [('patches-shipped-kernel', 41)] tier vendor-carried reach shipped lines 8608 lang kernel-config area patches-and-configs last_fork_commit None
AREA BY SLICE (patches-and-configs: tree, owning slices, reach: paths lines)
  1 paths 7754 lines ('distribution', (('device-generic-x64-and-kernel', 11),), 'test')
  1 paths 8129 lines ('distribution', (('device-h700', 27),), 'shipped')
  21 paths 1670 lines ('distribution', (('emulators-libretro', 3),), 'shipped')
  18 paths 1703 lines ('distribution', (('offline-achievements', 19),), 'shipped')
  778 paths 317908 lines ('distribution', (('patches-dead', 40),), 'unreached')
  379 paths 71252 lines ('distribution', (('patches-shipped', 42),), 'shipped')
  5 paths 135 lines ('distribution', (('patches-shipped', 42),), 'test')
  103 paths 39889 lines ('distribution', (('patches-shipped-kernel', 41),), 'shipped')
  4 paths 585 lines ('distribution', (('patches-shipped-kernel', 41),), 'test')
  432 paths 328516 lines ('distribution', (('patches-unshipped', 43),), 'unshipped')
  SLICE TOTAL 1 paths 7754 lines (('device-generic-x64-and-kernel', 11),)
  SLICE TOTAL 1 paths 8129 lines (('device-h700', 27),)
  SLICE TOTAL 21 paths 1670 lines (('emulators-libretro', 3),)
  SLICE TOTAL 18 paths 1703 lines (('offline-achievements', 19),)
  SLICE TOTAL 778 paths 317908 lines (('patches-dead', 40),)
  SLICE TOTAL 384 paths 71387 lines (('patches-shipped', 42),)
  SLICE TOTAL 107 paths 40474 lines (('patches-shipped-kernel', 41),)
  SLICE TOTAL 432 paths 328516 lines (('patches-unshipped', 43),)
wc -l, the text rows at the P1 hash: 40473
grep -c, the text rows at the P1 hash: 40474
grep -c, the text rows at the inventory head: 40474
present at the merge base: 106
blob vs merge base: ADDED 1
blob vs merge base: SAME 106
ADDED projects/ROCKNIX/devices/H700/patches/linux/0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch
MB..P1: 1 file changed, 38 insertions(+)
(end)
```
<!-- t41 block expected end -->

**The tree-side derivation reaches exactly the inventory's 107** at the
inventory head and at the P1 hash (the two `TREE-SIDE` lines: `derived: 107
equal to mine: True`); `106` are present at the merge base; the merge base to
the P1 hash is ` 1 file changed, 38 insertions(+)` over the 107 and the
inventory head to the P1 hash prints nothing (R1 C07). `block-2.txt` also
holds the TSV (the 107 with every inventory column), `TREE-SIDE`, `CLAIMS`,
`NAMED` and `AREA BY SLICE`, read with
`sed -n '/^CLAIMS/,$p' .qa-scratch/t41/block-2.txt` (R1 § 6); the lane's
copy of the block's output in `01-research-notes.md` § Scope is quoted from
`block-2.txt`, never retyped, and **the P1 run's `.qa-scratch/t41/` is saved
under `stage-a/` before the tip re-run overwrites it** (the generator reads
the saved TSV, § 5). The `buildable_by:` line is cut at 600 characters by the
block's own `cut`; the TSV rows are left out by its own `awk`.

**Both line figures** (ruling (a)): **40,474** is the inventory's column over
the 107 (`GROUPS TOTAL 107 40474 groups 9`) and the `grep -c ''` of the 107 at
the P1 hash and at the inventory head alike; **40,473** is `wc -l`'s, the one
unterminated file being
`projects/ROCKNIX/devices/SM8550/patches/linux/0004-drm-msm-a6xx-Enable-IFPC-on-Adreno-740.patch`
(`wc -l 32 grep -c 33`, R1 C09). R2's `wc -l` over `git show` through `$(...)`
gives 51 fewer over the 106 patches because the substitution strips the
trailing blank line of `git format-patch` output (R2 § 0) -- a measure of the
shell, not of the files; the brief states the two above and names the file.

**The groups, by R1's `GROUPS` lines** (R1 C07: kind, directory, paths,
inventory lines, reach, tier; every row vendor-carried), with the plan that
applies each (R1 C18's `reachable_by by kind`) and the glob that selects it
(R1 § 3; R3 § 1.1):

| Kind | Directory | Paths | Lines | Reach | Applied by | Selected by |
| --- | --- | ---: | ---: | --- | --- | --- |
| K2 | `projects/ROCKNIX/packages/linux/patches/7.0/` | 4 | 585 | test | `GENERIC_X64-x86_64` alone | the word `7.0` of `PKG_PATCH_DIRS+=" 7.0"` (override `:40`) through `unpack:143` -- patches named for 7.0 applied to 7.1.2 |
| K2 | `projects/ROCKNIX/packages/linux/patches/7.2/` | 6 | 651 | shipped | `H700-aarch64`, `H700-arm`, `SM8550-aarch64`, `SM8550-arm` | `${PKG_DIR}/patches/${PKG_VERSION}/*.patch` (`unpack:153`; `PKG_VERSION="7.2"`, override `:30`; the comment `:33-34`) |
| K2 | `projects/ROCKNIX/packages/linux/patches/mainline/` | 4 | 648 | shipped | all five plans | the word `mainline` of `PKG_PATCH_DIRS` (`:16`) through `unpack:143` |
| K3 | `projects/ROCKNIX/devices/H700/patches/linux/` | 32 | 8,616 | shipped | `H700-aarch64`, `H700-arm` | `devices/${DEVICE}/patches/${PKG_NAME}/*.patch`, **the last glob** (`unpack:159`) |
| K3 | `projects/ROCKNIX/devices/SM8550/patches/linux/` | 55 | 20,900 | shipped | `SM8550-aarch64`, `SM8550-arm` | the same `unpack:159` |
| K4 | `projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf` | 1 | 8,608 | shipped | `SM8550-aarch64`, `SM8550-arm` | `kernel_config_path`'s third candidate `devices/$DEVICE/linux/linux.${TARGET_KERNEL_PATCH_ARCH:-$TARGET_ARCH}.conf` (`config/functions:1449-1472`; copied to `.config` at override `:154`, then `listnewconfig` and `yes "" \| kernel_make oldconfig`, `:306-315`); the inventory reaches it as a device file (R3 § 1.5) |
| K5 | `projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/patches/` | 2 | 139 | shipped | `H700-aarch64` alone | that package's `${PKG_DIR}/patches/*.patch` (`unpack:150`); U-Boot `v2026.01` (`u-boot-DDR3/package.mk:5`, `v1 read`) -- **non-kernel**, T27's recipe |
| K5 | `projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/patches/` | 2 | 139 | shipped | `H700-aarch64` alone | the same; the two packages differ only in `PKG_NAME` and `PKG_UBOOT_CONFIG` (`anbernic_rg35xx_h700_lpddr3_defconfig` / `..._lpddr4_defconfig`, R2 command 12) -- **non-kernel**, T27's recipe |
| K5 | `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/patches/` | 1 | 188 | shipped | `GENERIC_X64-x86_64`, `H700-aarch64`, `SM8550-aarch64` (the 64-bit plans build `kernel-firmware`) | `unpack:150`; linux-firmware `20260309` (`kernel-firmware/package.mk:5`, `v1 read`); `kernel-firmware` is in the kernel's `PKG_DEPENDS_UNPACK` on H700 and x86 (`linux/package.mk:71`, `:83-84`), its `.copied-firmware` built into the H700 kernel (`:223-244`, R2 § 0) -- **non-kernel**, T42's recipe |

`KIND TOTAL K2 14 1884`, `K3 87 29516`, `K4 1 8608`, `K5 5 466`; `GROUPS
TOTAL 107 40474 groups 9` (R1 C07). **Per plan, the patches a kernel applies
in `unpack`'s order** (`v1 read` at `2174265e9c`: the directories in the
globs' order, the files sorted under `LC_ALL=C`): **GENERIC_X64** `mainline/`
4 then `7.0/` 4, `total: 8`; **H700** `mainline/` 4, `7.2/` 6, the device
directory 32, `total: 42`; **SM8550** `mainline/` 4, `7.2/` 6, the device
directory 55, `total: 65` -- the three plans' orders are § 5's
`order-<DEVICE>.txt`, and the three totals are the lane's lines to reproduce.
GENERIC_X64 has no device patches and no row for its configuration here (T11's,
ruling (d)); it reaches `7.0/` alone, `mainline/` with the four shipped plans
and the firmware patch with the two shipped `aarch64` plans (R1 § 2).
`buildable_by:` lists, for 15 of the 107, the unshipped plans that would also
apply them (the four `7.0/` rows by AMD64, RK3326, RK3566 and RK3576; the six
`7.2/` rows by SM4450, SM6115, SM8250, SM8650 and SM8750; the firmware patch
by every unshipped 64-bit plan); 92 rows are the shipped and test plans' alone
(R1 C07).

**The five non-kernel rows** (ruling (b)): `KIND TOTAL K5 other 5 paths 466
lines`. The two U-Boot pairs are byte-identical across `u-boot-DDR3` and
`u-boot-DDR4` (R2 command 10: *all identical*); **that is the whole DDR3/DDR4
split** -- one `PKG_UBOOT_CONFIG` apart, the kernel has no part in it (R2
§ 0; D-WORKFLOW-033 parks #44). The firmware patch
(`kernel-firmware-02-add-brcmfmac-43xxx-configs.patch`, MilhouseVH, 29 Nov
2018, R2 § 1) is a LibreELEC-era patch the fork carries unchanged. The order's
title and "why here" speak of kernel patches; the membership is the globs'
(R1 § 8 delta 4) -- **a delta this brief records, not a defect**: the five are
rows labelled `non-kernel` in the kind column, with their recipe's owner in the
disposition.

**The header census** (R1 C13 over the 106 patches; R2 § 1): **`From:` on 87,
`Subject:` on 89, a `From:` naming ROCKNIX on 3** (the 0950 patch and two
SM8550 patches); **19 without `From:`** -- SM8550 13, H700 2, `7.0/` 2,
`7.2/` 2 -- of which **17 are hand-made diffs with neither `From:` nor
`Subject:`** (R2 L-05 names them: H700 `0124-battery-name`,
`0154-rocknix-dt-id`; SM8550 `0001-pcie-update-sm8550-dtsi`,
`0060-...dsx-kconfig`, `0071-HACK-fix-usb-boot-hang`, `0104`/`0105` the
Retroid panels, `0500-ROCKNIX-set-boot-fanspeed`, `0505-msm_gem-lock...`,
`0506-usbcore-add-interrupt-interval-override`, `1000-add-qcom-haptics-driver`
(6,456 lines, 7 files), `1002`, `1003`; the override's `9998` and `9999` in
both `7.0/` and `7.2/`) and two open on a `Subject:` line with the `From:`
stripped (`0121-pmdomain-qcom-rpmhpd-presync-floor-gmu-rails.patch`,
`0612-ROCKNIX-odin3-q6apm-start-mi2s-port-at-prepare.patch`). **4 rows carry
an explicit upstream line** (`v1 read` at `2174265e9c`): H700 `0160` `Link:
https://lists.infradead.org/pipermail/linux-arm-kernel/2026-July/1145685.html`
(`:11`), SM8550 `0006` `Link: https://patch.msgid.link/20250925040530...`
(`:35`), `7.2/0011` `Link: https://patch.msgid.link/20260724-adc-tm5-...`
(`:19`), `7.2/0016` `Upstream-Status: Backport
[https://lore.kernel.org/r/20260616151252...]` (`:12`) -- the only row that
says it is a backport (R2 § 1). By `From:` the authors are Philippe Simons 31,
Teguh Sobirin 7, Kailash 5, Jacob Cook 5, tiopex 4, spycat88 3, danyi 3,
map220v, brooksytech, ROCKNIX and JS Deck 2 each, and the mailing-list
authors one each (R2 command 10). Six `Subject:` lines head a squashed
series (`[PATCH 01/21]` on `0002-rg35xx-enable-HDMI-LCD.patch` over 31 files
and 2,317 lines; `[PATCH v8 0/4]` on `0008`; `[PATCH 1/7]` on `0010`; `[PATCH
v2 1/3]` on `0110`; `[PATCH 1/4]` on `0126`; `[PATCH 1/6]` on
`20260424_neil_armstrong...`), so the table carries a Files/hunks cell (R2
§ 1, L-13). R2 § 1's 106-row table is the shape the generator reproduces; the
lane regenerates it, never copies it (R2 § 1's own note).

**The bases** (R1 C01, § 0; R2 § 4). The P1 tip `2174265e9c` is the pin every
research read is at; the coordinator's tip `6a12ce2d73` carries it
(`merge-base --is-ancestor` true, `v1 read`) and the four inventory files
byte-identical (R1 C01), so **the lane's tree is the coordinator's tip, cut,
not merged** (ruling (a)). `next` is `8ebaf8daad` and is byte-identical to
the P1 tip over the member directories and the two kernel recipes (R2
command 7). Upstream is the local ref `upstream/next` `651150fc88`
(2026-10-24, *Merge pull request #3547 from spycat88/qcom-bls*; not fetched)
and the merge base `c445081a59` (2026-10-01, *Merge pull request #3413*),
ROCKNIX stable 20261001. The P1 research clone `W` has no `upstream/next`
ref (R1 C01), so every upstream read is made in the coordinator's store
(ruling (f)) and the block needs none (it compares with `MB`, which the clone
holds). This paragraph is the one statement of the bases; § 1's rulings, § 5's
expectations and § 7's checkboxes cite it.

**The tool's own row, from the worktree** (R1 C14 ran it from the clone):
`./tools/renovation-inventory --order --no-write --distribution "$W"` exits 0
with `50` lines, among them `unassigned: 0`, `ambiguous: 0` and the row
`41 patches-shipped-kernel patches-and-configs 107 paths 40,474 lines 0 read
0 fork-own 40,474 patch table` (R1 C14, the tool's spacing); the clone's
`status --short --ignored` was 2 lines before and after (R1 C14). Whether the
worktree's copy prints the same is `[unverified]` (T39's open item 4 had the
same shape); the lane records what prints and whether `git status --short
--ignored` moved.

**The neighbours, and whose they are** (R1 C07's `CLAIMS` and `NAMED`; R1
§ 7): the 14 `CONF` rows under the slice's positive globs that are not the
slice's -- **H700's `linux.aarch64.conf` (8,129 lines, `cbf75c0b06`) is T27
`device-h700`'s, GENERIC_X64's `linux.x86_64.conf` (7,754, `cbf75c0b06`) is
T11 `device-generic-x64-and-kernel`'s** (each by a second `select` entry
naming `areas: ["patches-and-configs"]`, R1 C03), and the twelve unshipped
devices' confs (AMD64 12,445 lines, RK3326, RK3399, RK3566, RK3576, RK3588,
S922X, SM4450, SM6115, SM8250, SM8650, SM8750) are T43 `patches-unshipped`'s;
the 281 `unreached` area rows under the globs (92,480 lines) are T40's and
the 383 `unshipped` (325,382 lines) T43's. `NAMED`: the two kernel recipes
are T11's (`projects/ROCKNIX/packages/linux/package.mk`, 432 lines, fork-own,
shipped) and T25's (`packages/linux/package.mk`, 358, unreached);
`scripts/unpack` is T5 `build-engine`'s (228 lines, upstream-carried); the
three devices' `options` are T27's, T28's and T11's. **The asymmetry stated
once**: T27 reads H700's configuration and T11 GENERIC_X64's, but **SM8550's
configuration is a T41 row** -- vendor-carried, never changed by the fork,
changed four times upstream since the base; T28's `select` has no second
entry (R1 § 7). The area's partition (`AREA BY SLICE`): T40 778 paths /
317,908 lines, T41 107 / 40,474, T42 384 / 71,387, T43 432 / 328,516, plus the
two carved-out confs and the patch groups `emulators-libretro` (21) and
`offline-achievements` (18) claim by glob (R1 C07).

**Two files sit beside the live patches and are not members** (ruling (o);
R1 C13, C16): H700's `0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled`
(4,036 lines) and SM8550's `0053-add-hynitron-touchscreen.patch.disabled`
(20,593 lines), both still at `upstream/next`, area `devices`, tier
`upstream-carried`, T27's and T28's rows (PL-06 of each, R4 item 13). The
override's fourth subdirectory `mainline-rockchip/` (6 paths, 791 lines) is
`RK*`'s only and T43's (R1 C13). **No symlinked `patches` directory is among
the nine** (R3 § 1.5; R5 § G (e)): `git ls-tree -r 2174265e9c | awk
'$1=="120000"'` under the member roofs prints `3` entries (`v1 read`), named
in `## Version 1` item 6 with what each points at; none is a `patches`
directory of the 107's, so #1056's gap moves no row here -- the lane's stage-A
line re-states it.

**Already found; do not re-find; take up.** Each is cited at its lines in
`02` with a disposition; the states are as R4 read them on 2026-11-01, re-read
at stage A. **Asks**: *read* (a row or a sentence in `02`/`04`), *inherit* (the
coordinator's or another owner's; § 8), *none* (recorded so the lane does not
re-find it); **no *fix*: D-WORKFLOW-209 and ruling (c)**:

| Found by | What | Take up as |
| --- | --- | --- |
| T40's PL-03 (#688's one comment, 2026-10-25T05:46:50Z; `patches-dead.md:441`; R4 item 1) | **T41 inherits no leads**: none of the 26 overrides behind the 50 shadowed rows is a kernel override; all 50 went to #689 | **none**: cite the pointing comment; T41 reads no shadowed generic patch |
| T40's two rules for T41 (#687 `:113`; errata `:447-451`; R4 item 2) | a kernel's `PATCH_ARCH` is `TARGET_KERNEL_PATCH_ARCH` (`unpack:130`); the 277 generic kernel patches are dead because `get_pkg_directory linux` resolves to the override everywhere | **read**: the *applies* column is derived from `unpack:127-159` and the recipe's `PKG_PATCH_DIRS` per device, the kernel's arch variable named (L-30) |
| the inventory's reach gaps #1049, #1056, #1086, #1101, #879, #1053 (#687 `:116`; futro `:193-195`; R4 item 3) | none of the six is a kernel-patch gap | **read**: one sentence per gap saying it moves no row of the 107, stated as a check (L-18, L-23) |
| the plan's *one diff per kernel config against its base* (futro `:72-73`; `patches-dead.md:184-187`; R4 item 4) | the two fork-edited confs are **excluded** from T41 and read by T27 (`02:80-93` at `78579255e4`) and T11 (`02:94-171` at `47672fe4a0`); SM8550's has 0 fork lines (T28 `02:78-90` at `5a60d1c825`: 7 / 7 against `651150fc88`) | **read**: the conf row cites T28's read and the four commits; the fork-written config lines live in T27's and T11's tables (ruling (d); L-19, L-27) |
| the ramoops patch (#688's body; `order.md:696`; D-SYS-004 `:164`; `handheld-evidence.md:84-85`; device-facts L29; #104 `:12` open; `device-h700.md:246-252`; R4 item 5) | the one line-by-line row | **read**: ruling (e); L-16 |
| the tier (`device-h700.md:246-252`: *cite it, do not re-tier it*; R4 item 6) | `0 fork-own` by the tool against one fork commit absent upstream | **read**: state both; whether the tier rule or `last_fork_commit` is a tooling defect is the coordinator's to file (L-17) |
| D-SYS-001 to -006 (`decision-register.md:161-165`, `:792`; `handheld-evidence.md:63-91`, `:109-113`; R4 item 7) | the kernel-side decisions the rows cite; `hang-policy.conf` and the systemd drop-in are T11's and T22's, not patches | **read**: the ramoops row names D-SYS-002/003/004 and L29 |
| currency against `upstream/next` (R4 item 8 as corrected by R4 § 6 item 2; R1 § 5; R2 § 4) | the 20-file `--name-status` on the globs; the 12 upstream additions; the moved polldev patch; `rocknix-joypad` for H700; `7.2.6/` for T43's targets; the pins unchanged for the three | **read** (Q4): one row per changed or gone member, one line per upstream addition, each *the integration carries* (ruling (f); L-01, L-14, L-22); #563/#559 named, not acted on |
| #328 (OPEN; D-QA-023, D-QA-028; R4 item 9) | the SM8550 dispcc `rcg didn't update its configuration` warning, *"Upstream ROCKNIX's kernel, not the fork's"*; `0002-qcom-dispcc-sm8550-Fix-...` already in the tree | **read**: the `0002` row cites #328 and names upstream's `0017-clk-qcom-blank-dsi-panels-before-dispcc-park.patch` as the lead the merge brings (L-20); nothing diagnosed |
| the U-Boot pairs and #44 / D-WORKFLOW-033 (`device-h700.md:194-198`, `:321`; T27 PL-10; R4 item 10) | DDR3 and DDR4 differ in `PKG_UBOOT_CONFIG` alone; which image a unit takes waits until after the release candidate | **read**: four `non-kernel` rows, the duplication named once; #44 cited, not reopened (L-12) |
| `0154-rocknix-dt-id.patch` (T27 `02:49`, `:124`; `os-device-quirks.md:207`; T25 `02:177`; R4 item 11) | read by three slices; `bootloader/update.sh` reads `rocknix-dt-id`; L15's tree open | **read**: the row names its readers and L15 (L-25) |
| `0105-drm-panel-Add-Retroid-Pocket-Nova-panel.patch` (T28 `02:140`; `device-sm8550.md:189`; R4 item 12) | adds the Nova's panel `il97680a,rpnova` | **read**: the row names the shipped unit it serves (L-26) |
| the `.disabled` patches (T27 PL-06, T28 PL-06; R4 item 13) | not `*.patch`; T27's and T28's | **none** beyond the context sentence (ruling (o); L-10) |
| the one-line discrepancy (`device-sm8550.md:161`, `:507`; R4 item 14) | 29,508 against 29,507 over SM8550's rows | **read**: the file named when the line column is summed (L-24) |
| #369 (Parked; R4 item 15) | the kernel patch's upstream offer; #585 carries no kernel line (R4 command 12) | **read**: the ramoops row's upstream disposition and its `#585` line, never sent (ruling (e); L-16) |
| the rules' kernel-patch sentence (`packaging-and-patches.md:91-93`; `CLAUDE.md:143-149`; #687 `:113`; R4 item 16) | *"Kernel patches live under `packages/linux/patches/<DEVICE>/`"*, the dead directory | **inherit**: the coordinator's erratum (ruling (k); L-09); `04` Q7 names the two lines |
| #1084, #1083, #796 (T11's; R4 items 17-19) | GENERIC_X64's conf header 6.15.6 and its `oldconfig` gap; the guest's whole-firmware install; `MAC80211_HWSIM` | **none**: T11's file; cited in Q2's sentence on the configs (L-07) and the firmware row's note (#836, T27 PL-05) |
| #704 (T1's), #1110 (M7.P5), #1099 (Backlog; T28 PL-02), #563 / #559 / #585 (M7, Backlog, Standing), #1111 / #1113-#1116 / #1154 (M7.P5) (R4 items 20-22, 26, 27) | governors; the RG35XX SP reset (the watchdog armed, pstore read); upstream's BLS boot change in the recipe's `qcom-abl` branch; the base merge, the backport procedure, the contribution queue; M7's issues | **none** or **name, do not act**: #1110 beside L29 as the one field read of the watchdog armed; #1099 beside the recipe's `makeinstall_target` (L-28); #563/#559 as the integration that carries upstream's changes |
| #1054's acceptance for T41 (`:28-29`; R4 item 23) | the five columns and the two checks | **read**: § 7 |
| the futro's asks (`:5`, `:67`, `:73`, `:96`, `:150`, `:176`, `:194`; R4 item 24) | the shadowed rows (superseded: none for T41), the config-diff clause (outside T41), the 427 / 20 counts, the symlink gap | **read**: each resolved by the item named; the kickoff addendum's *Known unknowns* spine (§ 9) |
| D-WORKFLOW-185, -187, -189, -198, -209, -162, -164, -165 (R4 items 25, 15) | the shipped set; the renovation gates no release; planning the coordinator's; modify/delete at the base merge; a table removes nothing; upstream checked early; contributions recorded, never sent | **read**: the rows that bound the table's reach, its no-edit rule and its upstream column (§ 9) |
| the device slices' retros (T11 at `47672fe4a0`, T27 at `78579255e4`, T28 at `5a60d1c825`, T25 at `9b9be6a948`; R4 item 28) | no T41 item beyond items 4, 11, 12, 14 | **none** beyond those named |

## 3. The floor: read first, then the leads

**Read first**, in this order, each in this session, and
`01-research-notes.md` says which were read (`working-principles.md` §
Pre-flight). The line numbers are the coordinator worktree's at `6a12ce2d73`
as the research printed them; the lane re-reads each with `grep -n` at
`__COHASH__`:

1. **The rules**, each at the section named; **read, never edited**
   (D-WORKFLOW-189; T4's read, #651):

   | Rule | Line or section | Serves |
   | --- | --- | --- |
   | `packaging-and-patches.md` | `:76-93` (how a patch is produced and scoped; `patches/<DEVICE>/` only via `PKG_PATCH_DIRS`); **`:91` the kernel-patch sentence that names the dead directory** (R2's header; R4 item 16) | § 5's order, L-09 |
   | `CLAUDE.md` | `:143-149` (the auto-applied directories, `scripts/unpack:127-159`; `:148-149` the same kernel sentence) (R4 item 16) | L-09 |
   | `device-builds.md` | `:19-31` (the device table: H700 the RG35XX SP and RG SP, SM8550 the Retroid Pocket Nova, GENERIC_X64 the VM), `:627-636` (two H700 flash images, one update tar), `:689-690`; `make kconfig-menuconfig-<DEVICE>` writes the tree's conf (R4 item 8; R3 § 1.3) | the per-device columns; what never runs |
   | `handheld-evidence.md` | `:24-25`, `:63-91` (the hang-to-reboot path: the watchdog at 15 s, the sysctls, ramoops 1 MiB at `0x4F000000`, 512 KiB console, four 128 KiB dumps), `:109-113` (the GENERIC_X64 profile's `i6300esb` and pstore over UEFI; H700 DRAM retention the one device fact) (R2's header; R4 item 7) | L-16 |
   | `engineering-practices.md` | § Check upstream early (D-WORKFLOW-162: the check date, links, affected/fixed versions recorded); § Consider contributing every applicable fix upstream (D-WORKFLOW-164/165: #585 the queue, nothing sent); § Verify design intent (`git log -S` before a patch is called wrong); § A name is not a behaviour (a total is the tool's line; a hash copied by a command); § Guards must fail closed (`rc=$?` on its own line; the positive first; a count echoed is not a floor) (R2's header) | § 5, every lead |
   | `upgrade-and-install.md` | § Migrations (*attribute honestly*: `unknown` is a value the consumer handles -- ruling (k)); § Every fix answers what was already written (the bug's `Already written:` line) | the origin column; every bug |
   | `vm-first.md`, `bugs-are-agent-first.md`, `issue-tracking.md` | the VM question before any proof (ruling (h)); a bug's criterion verified on the VM or moved to the other two classes (a kernel patch's run-time effect is a handheld fact, never a bug's check here); `--repo pixelelated/distribution` always; *checkbox*, not *box* (D-QA-045) | § 5 rule 3; every bug |
   | `decision-register.md`, `learning-capture.md`, `ceremonies.md`, `time-to-play.md`, `working-principles.md` | whole; `time-to-play.md`: nothing here reaches a launch path | § 9, the retro |
   | `generic-x64-vm-testing.md` | `:1350` (`CONFIG_USB_GADGET` off on GENERIC_X64) -- T11's conf; read for what a conf line means to a guest, never for a guest here | L-07 |

2. **The register** -- § 9.
3. **The blindspots** (`docs/blindspot-register.md`): 47 (pango's fetched
   cairo: a pin is a claim about the image only once the image is read),
   75 (counts from the wrong tree), 8 (an assertion that holds because
   nothing had happened yet), 14 (a guard with no observed positive) -- the
   shapes a provenance table is prone to (T40's § 3; R5 § B).
4. **The checks that exist, and what each reads of the 107** (R3 § 1, § 6).
   **No tool checks a `.patch` or a `.conf` without a build** (R3's
   one-paragraph answer):

   | Check | Reads the 107? | Its line | What its rc means here |
   | --- | --- | --- | --- |
   | `tools/pkgcheck` | **no**: `package.mk` text only (`:157`, `:169`) | rc 0 on `linux` (2 recipes), `linux-drivers`, `linux-firmware`, `kernel-firmware`, `u-boot-DDR3`, `u-boot-DDR4`, `linuxconsoletools`, **and rc 0 on `linux-no-such-package` (0 matched)** (R3 C21) | no evidence for the 107; fails open on a name that matches nothing (#1050) |
   | `tools/renovation-inventory` | **yes**: the rows are its; `selected_patch_dirs` (`:382-401`) mirrors `unpack`'s globs; `compute_reach` (`:420-483`) reaches a `.patch` iff its directory is in `reached_pdir`, a `.conf` under `devices/<D>/` by `by_device` (`:470-472`) -- because the device has a plan, not because `kernel_config_path` chose that file | `--order --no-write`: `unassigned: 0`, `ambiguous: 0`, the T41 row (R1 C14) | a full run needs the container and writes plans: **never run** here; the lane reads `inventory.json` at the tip |
   | `tools/renovation-drift` | after `fixed_at` only; rows, not lines, for a table slice (`:90-96`) | *"no slice has a `fixed_at` yet"* (`:171`) | the area's drift count after T41 closes (#1054 criterion 3); a kernel bump renaming `7.2/` is the drift it will report |
   | `tools/lint-audit-artifacts` | the folder, not the table (the pass fixture's `02` is one sentence) | `PASS`; the fail fixture's two `FAIL` lines (R3 C23) | `04 § Renovation face` Q1..Q7 and `question:` per punch item; a Local plan needs no seat and no manifest (`:92`, D-WORKFLOW-184) |
   | `.githooks/secret-patterns` / `pre-commit` | `02`'s quoted names | the inventory's own note (`:633-635`): a kernel patch name shaped like `ma-sk-...` once read as an API key to the guard | counts only, before commit (§ 5) |
   | `tools/forbidden-terms-check --stdin` | `02` | rc 0 beside its planted positive rc 1 (R3 § 6) | run before commit; rc 0 alone is not evidence |
   | `tools/adjust_kernel_config`, `tools/check_kernel_config`, `make kconfig-*` | would **write** the confs: both unpack and patch the kernel (`:19`, `:8`) and `scripts/config --file $PKG_KERNEL_CFG_FILE` the tree's conf in place (`:14-33`) | -- | **never run by a lane** (ruling (g); R3 § 1.3): a row in the table's method column, *how a conf changes and why a hand edit is overwritten by the next `kconfig-*` run* |
   | `tools/register-check`, `rules-check`, `work-log-index`, `box-check`, `ceremony-check`, `.githooks/hooks-test` | the docs and the tracker | `register-check: 715 IDs, each once; ...` at `6a12ce2d73` (`v1 read`); the rest `[unverified]` here | tripped by the lane's own writes only; the lines that print at stage A are the record |

5. **T40's record**, on its branch (`feature/m6-patches-dead-687` at
   `bf3409ea18`; the acceptance merge `e863379cec`), read with `git -C
   /workspace/repos/pixelelated/distribution.worktrees/m6-patches-dead-687
   show <hash>:<path>`, never checked out (R1 § 7; R3 § 4): `tools/t40-tables.py`
   (171 lines, the generator T41's is cut from, ruling (j)), `02 § Provenance`
   (778 rows, the column shape), `02 § The shadowed 74` (the 50 by override,
   all T42's), `stage-a/linux.out` (the five plans' `linux ->
   projects/ROCKNIX/packages/linux` and `PATCH_ARCH`: `x86` for GENERIC_X64,
   `aarch64` for both H700 and SM8550 plans, R1 C15), `stage-a/unpack-lines.out`,
   `stage-a/headers.out` (the census format: `patches 760 with Subject: 746;
   with From:+Subject: 746; without: 14`), `stage-f/counts.txt`, its `05` and
   its retro (`docs/retros/2026-10-25-m6-patches-dead.md` on its branch, 63
   lines, R5 C15: the shape § 6's retro takes). T40's `00` records the lint
   PASS three ways (`pre-issue`, resolution, `--issue 1074`, R3 § 1.7).
6. **The device slices' records**, each by `git show` at its hash (R4 § 5):
   T11 `02` § The configuration `:94-171` at `47672fe4a0` (the 6.15.6 header,
   the fork's 13 lines, the `oldconfig` gap; PL-04 -> #1084, PL-09 the
   version case at a merge); T27 `02:49`, `:86`, `:115`, `:124` at
   `78579255e4` (the dt-id, the six fork config lines, #44 and L29); T28
   `02:78-90`, `:140` at `5a60d1c825` (the conf's 7 / 7, patch `0105`); T25
   `02:177` at `9b9be6a948` (no unshipped `.dts` carries `rocknix-dt-id`).
   Their branch tips are recorded at stage A as whichever line prints (a hash
   or `fatal:`), never copied from here (R5 § B item 3).
7. **`scripts/unpack` at the tip** (`:118-165`; the rules `:127-159`, the
   apply loop `:160-196` -- T40's `stage-a/unpack-lines.out` holds it);
   `config/functions` `kernel_config_path` (`:1449-1472`) and
   `get_pkg_directory` (`:1057-1090`); the override whole (432 lines, by
   `cat -n`, never sourced); the three devices' `options`;
   `config/arch.arm:80` (`TARGET_KERNEL_PATCH_ARCH="aarch64"`) and
   `projects/ROCKNIX/devices/GENERIC_X64/options:10` (`x86_64`, pre-empted by
   `unpack:127`'s `x86`, R3 § 1.1).
8. **The issues**: #688 (its one comment), #1054 (the epic, its futro
   comment), #687 (T40's eight comments, the acceptance `:202-213`), #346,
   #1048, #1049, #1056, #1086, #1101, #879, #1053, #1050, #1051, #328, #369,
   #104, #44, #1084, #1083, #836, #796, #1099, #1100, #1110, #563, #559, #585,
   #1071, #1072 (R4 § 4). The lane re-reads each with
   `gh --repo pixelelated/distribution issue view` at stage A and records the
   states it saw; a sentence it quotes from an issue goes through the read
   mask (§ 5).
9. **Time to play: untouched.** No path of the 107 changes on this branch, so
   neither number moves (R5 § C stage G); the retro says so in those words.

**The leads, one line each, in the brief's own numbering** -- `R2 L-<nn>` is
R2's numbering, never this table's. Nothing here was tested by this lane; a
lead is a fact of the lines until the lane's proof says more. **`proved`** is
the research's column: `tree` (read at the hash), `history` (`git log`),
`tool-run` (a command's output shows it), `record` (an issue's or a row's
state). Each gets its `git log -S` (or `git log --follow` at ROCKNIX) before
it is called a defect (`engineering-practices.md` § Verify design intent).
**Every check is a `git show`, `git grep`, `git ls-tree`, `git cat-file`, `git
diff` or `git log` at a hash, a `gh --repo pixelelated/distribution` read, a
`patch --dry-run` in the lane's scratch, or a read -- never a fetch, a guest,
a build, `scripts/unpack` or a keyed call** (rulings (g), (h), (i)). `HEAD` in
a check line is the lane's worktree at the stage named; `W` is § 2's clone; a
`\|` inside a table cell is Markdown's escape for `|`, and the lane types `|`.
**The disposition column is the closed set of § 6's leads set: `row`, `bug`,
`#585`, `inherited:<owner>`, `none`.**

| Lead | Lines at the tip | Shape | proved | Check | Q | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| **L-01** | `projects/ROCKNIX/packages/linux/patches/7.0/0010-msm-resource-cleanup.patch`, `.../7.2/0010-msm-resource-cleanup.patch` (478 lines each, byte-identical; R2 L-01; R1 § 9) | **the shipped kernels and the test image carry the unfixed `0010`**: upstream rewrote both copies on 2026-10-06 (`9416eec2c2`, *"Previous version writes to field pointed by an uninitialized pointer"*); the base is 2026-10-01; the tip's `7.2/0010:15` hunk `@@ -1442,6` sets `cstate->num_mixers = 0` before `cstate` is assigned, upstream's moves the assignment first (R2 command 13) | history, tree | `git -C /workspace/repos/pixelelated/distribution diff --stat 2174265e9c 651150fc88 -- projects/ROCKNIX/packages/linux/patches/7.2/0010-msm-resource-cleanup.patch \| tail -n 1` prints ` 1 file changed, 14 insertions(+), 11 deletions(-)` (`v1 read`); `git log --format='%h %cs %s' c445081a59..651150fc88 -- <the two>` prints `9416eec2c2 2026-10-06 ...` | Q3, Q4 | **bug** (ruling (c): a currency row -- `upstream-changed`, the integration carries -- and a `bug` naming upstream's fix; whether the defect is reachable is the row's question: SM8550 builds the DPU, H700 and the x86 test image do not, L-31) |
| **L-02** | `651150fc88:projects/ROCKNIX/packages/linux/package.mk:18` (R2 L-02) | **upstream's quoted `=~` never matches**: `[[ "${DEVICE}" =~ "RK3326\|RK3399\|S922X\|H700" ]] && PKG_PATCH_DIRS+=" rocknix-joypad"` is false for all five device names, true unquoted (R2 command 14); no `patches/rocknix-joypad` directory exists anywhere at `651150fc88` (R2 command 14; R1 § 10), so today it changes nothing | tool-run | the same `[[ ]]` test over the five names, recorded; `git -C /workspace/repos/pixelelated/distribution grep -n -F 'rocknix-joypad' 651150fc88 -- projects/ROCKNIX/packages/linux/package.mk` prints `:18` | Q3, Q4 | **#585** (a D-WORKFLOW-164 one-liner for ROCKNIX, written in `02` § The #585 lines owed, never sent; ruling (f)) |
| **L-03** | `7.0/{0010,9998,9999}` against `7.2/`'s (R2 L-03) | **three byte-identical pairs**: one change made to one copy leaves the other behind; upstream's own `7.2.6/` answers it with symlinks (3 of 4, mode `120000`, R2 command 13) | tree | `for f in 0010-msm-resource-cleanup.patch 9998-silence-initramfs-unpack-warn.patch 9999-fix-rust-build-error.patch; do cmp <(git show HEAD:projects/ROCKNIX/packages/linux/patches/7.0/$f) <(git show HEAD:projects/ROCKNIX/packages/linux/patches/7.2/$f) && echo identical $f; done` prints three `identical` lines | Q7 | **inherited:T11** (the recipe's owner; a symlink is a recipe-tree change after the base merge, the maintainer's word -- § 4 question 1; never here, D-WORKFLOW-209) |
| **L-04** | `projects/ROCKNIX/devices/SM8550/patches/linux/` (R2 L-04) | **numbering collisions and mixed names**: `0053` x2, `0054` x2, `0057` x2, `0060` x3; `0031_` to `0059_` with underscores; two files without a number (`20260424_neil_armstrong...`, `v6_20260210_...`); upstream's `7.2/` now has two `0011-`; application order is the shell's sort of each glob (`unpack:150-159`), deterministic but no longer what the numbers say | tree | `git ls-tree -r --name-only HEAD -- projects/ROCKNIX/devices/SM8550/patches/linux \| /usr/bin/grep -E '\.patch$' \| sort \| sed -E 's#.*/##; s#^([0-9]+).*#\1#' \| uniq -d` prints `0053`, `0054`, `0057`, `0060` (`LC_ALL=C`; `v1 read` of the sorted names shows the order) | Q2 | **row** (the application index column, § 5; a Q2 note; no rename) |
| **L-05** | the 17 hand-made diffs and the 2 stripped exports (R2 L-05; R1 C13) | **origin unrecoverable from the file**: `diff -rupN`, `diff -ur`, `diff -Naur`, `diff --git` or a bare `---` openers | tree | the header census line `patches 106 with From: 87 with Subject: 89` (§ 5's runs); per row `git log --follow --diff-filter=A --format='%h %an %cs %s' HEAD -- <path>` for the adding commit at ROCKNIX | Q2 | **row** (origin `hand-made`; provenance from content and the adding commit; `unknown` where neither says, ruling (k)) |
| **L-06** | H700 `0008` (v8, 2026-08-04), `0110` (v2, 2025-02), `0126` (2024-10), `0160` (`Link:` 2026-07), `0002` (DE33 `01/21`, 2025-10); SM8550 `0006` (`Link:` 2025-09), `0120` (RFC `22/24`, 2025-07), `20260424_neil_armstrong` (`1/6`), `v6_20260210_...qce`; `7.2/0011` (`Link:` 2026-07), `7.2/0016` (`Upstream-Status: Backport`, lore 2026-06-16) (R2 L-06) | **mailing-list imports whose mainline status the header dates**: a patch dated before the pinned kernel's release may already be in it in another form; one that is applies only because its context still matches | tree | per row: the applies-at-pin run (§ 5) and `tar -xJOf "$S/linux/linux-7.2.tar.xz" linux-7.2/<first target> \| /usr/bin/grep -c -F -e '<a + line of the hunk>'` -- present = merged already (a `superseded at this pin` lead to T11), absent = still needed; the kernel tag named in the body, where one is, recorded as the patch's claim | Q4 | **row** (upstream status `claims mainline <tag>` where the header says it; backport status from the pin) |
| **L-07** | `projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf:3` (R2 L-07; #1084) | **a conf header of 6.15.6 under a 7.1.2 kernel**, every new option answered by `yes "" \| kernel_make oldconfig` (`package.mk:315`) -- T11's file; H700's and SM8550's say `7.2.0` (R2 command 13) | tree | `git show HEAD:projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf \| sed -n 3p` prints `# Linux/arm64 7.2.0 Kernel Configuration`; the GENERIC_X64 line is cited from #1084, not re-run | Q2 | **none** (T11's, #1084; cited in Q2's sentence on the configs) |
| **L-08** | `projects/ROCKNIX/packages/linux/package.mk:318-334` (R2 L-08) | **`distributions/ROCKNIX/kernel_options` is a soft guard**: `pre_make_target` prints `LINUX: kernel options not correct ... Please run ./tools/check_kernel_config` as a warning, never a failure | tree | `git show HEAD:projects/ROCKNIX/packages/linux/package.mk \| sed -n '318,334p'` prints the loop; `git cat-file -e HEAD:distributions/ROCKNIX/kernel_options && echo present` | Q3 | **inherited:T11** (the recipe's); the conf row's method column names it (ruling (d)) |
| **L-09** | `.claude/rules/packaging-and-patches.md:91`, `CLAUDE.md:148-149` (R2 L-09; R4 item 16) | **the rules name the dead directory as the live one**: *"Kernel patches live under `packages/linux/patches/<DEVICE>/`"* -- T40's class (a), `unreached`; the live ones are the override's `patches/{7.2,7.0,mainline}` and `devices/<DEVICE>/patches/linux/` (`unpack:159`) | tree | `grep -n 'packages/linux/patches/<DEVICE>' .claude/rules/packaging-and-patches.md CLAUDE.md` prints `:91` and `:149` (`v1 read`) | Q7 | **inherited:coordinator** (ruling (k); T4's rules; never a lane edit) |
| **L-10** | the two `.patch.disabled` (R2 L-10; R4 item 13) | disabled by rename, with no note why; never applied (`*.patch` glob) | tree | `git ls-tree -r --name-only HEAD -- projects/ROCKNIX/devices/{H700,SM8550}/patches/linux \| /usr/bin/grep -c '\.disabled$'` prints `2` | Q2, Q7 | **none** (ruling (o): T27's and T28's rows; one context sentence in `02`) |
| **L-11** | `projects/ROCKNIX/devices/SM8550/patches/linux/0501-ROCKNIX-fix-wifi-and-bt-mac.patch` (305 lines, spycat88; R2 L-11) | **the radios' MACs derived from the SoC serial** -- the hardware address the cloud device id is seeded from (D-CLOUD-068) | tree | `git show HEAD:<path> \| /usr/bin/grep -c -i -E 'serial'` prints a non-zero count | Q7 | **row** (a cross-reference to the cloud device id in the row's note; not a defect) |
| **L-12** | the four U-Boot patches (R2 L-12; R4 item 10) | **both post-date the pinned `v2026.01`**: `0002-sunxi-axp717-charge-only-boot.patch` (Kailash, 2026-09-21, `From 0000...`, 4 files incl. `Kconfig`), `0001-Update-dram_sun50i_h616.c.patch` (Philippe Simons, 2026-04-01); ROCKNIX-authored, upstream U-Boot status unknown here; identical across DDR3/DDR4 | tree | the two `cmp` lines (§ 5's runs); applies-at-pin against the cached `u-boot-DDR3-v2026.01.tar.gz` (top directory `u-boot-2026.01/`, `v1 read`) by the same method `[proposed]` -- ruling (g) names the kernel tarballs; the coordinator confirms at dispatch or the four cells read `open item` | Q4 | **row** (`non-kernel`; **inherited:T27** for the recipes and #44) |
| **L-13** | `0002`, `0008`, `0010`, `0110`, `0126`, `20260424_neil_armstrong` (R2 L-13) | **a `Subject:` that describes 1/21, 0/4, 1/7, 1/3, 1/4, 1/6 of the content** (a squashed series keeps its cover or first header) | tree | the generator's Files/hunks cell (`+++ ` lines / `@@` lines) per row | Q2, Q7 | **row** |
| **L-14** | `projects/ROCKNIX/packages/linux/patches/mainline/0002-input-add-input-polldev-driver.patch` (485 lines); upstream's `fe5216ff69` (R2 L-14; R1 § 9) | **after the base merge H700, SM8550 and GENERIC_X64 lose `input-polldev`**: upstream moved it to RK3326's directory (*"now that's the only device that needs it"*) and the SM8550 conf drops `# CONFIG_INPUT_POLLDEV is not set` in the same window; H700's `0140-rg35xx-2024-use-rocknix-joypad-driver.patch` and the `rocknix-joypad` driver package are the consumers to read | history | `git -C /workspace/repos/pixelelated/distribution show --stat --format='%h %cs %s' fe5216ff69 \| head -n 12` prints the rename with 0 changed lines; `git grep -c -i polldev HEAD -- projects/ROCKNIX/devices/H700/patches/linux projects/ROCKNIX/packages/linux-drivers` prints the consumers (`[unverified]`: R2 command 14 read RK3326's `004` only) | Q4, Q6 | **row** (`upstream-moved`, the integration carries) and **inherited:T27** (whether the H700 joypad driver still needs it is the device slice's and the integration's question) |
| **L-15** | `projects/ROCKNIX/packages/linux/package.mk:16`; `unpack:143` (R2 L-15; R1 § 3) | **`PKG_PATCH_DIRS` names `${DEVICE}` and `default` directories the override does not have, and `${LINUX}` is empty**; each skipped by `unpack:143`'s `-d` test with no message -- a `patches/H700/` created under the override by a future hand would silently start applying | tree | `for d in H700 SM8550 GENERIC_X64 default; do git cat-file -e "HEAD:projects/ROCKNIX/packages/linux/patches/$d" 2>/dev/null \|\| echo "absent $d"; done` prints four `absent`; `git grep -n -E '^\s*LINUX=' HEAD -- projects/ROCKNIX/options distributions/ROCKNIX/options config/options \| /usr/bin/grep -c ''` prints `0` | Q7 | **none** (ruling (o): a recorded fact beside the recipe line; T11's) |
| **L-16** | `projects/ROCKNIX/devices/H700/patches/linux/0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch` (38 lines; `cbf75c0b06`; R2 § 2; R4 items 5, 15) | **the one fork-written row, read line by line**: `:1-2` the hand-written `From: ROCKNIX fork` and `Subject:`; `:4-7` the body (fork #104); `:10-12` one file `arch/arm64/boot/dts/allwinner/sun50i-h616.dtsi`, one hunk `@@ -117,6 +117,26 @@` on the reserved-memory child `reg = <0x0 0x40000000 0x0 0x40000>; no-map;`; `:17-28` the address argument (kernel at `0x40080000`, U-Boot at `0x4A000000`, FDT at `0x4FA00000`, SPL stack at `0x4FE00000`, ramdisk at `0x4FF00000`); `:29-35` the node (1 MiB at `0x4f000000`, `record-size = <0x20000>`, `console-size = <0x80000>`, `max-reason = <2>`) -- D-SYS-004's numbers; the config half in H700's conf (T27's); not at `upstream/next`; parked in #369 | tree, history | `git show HEAD:<path> \| sed -n '29,35p'` prints the node; `git merge-base --is-ancestor cbf75c0b06 651150fc88 \|\| echo not-in-upstream`; `tar -xJOf "$S/linux/linux-7.2.tar.xz" linux-7.2/arch/arm64/boot/dts/allwinner/sun50i-h616.dtsi \| /usr/bin/grep -n -A2 '0x40000000 0x0 0x40000'` prints the hunk's context at or near `:117` and no `ramoops` node (R2 § 2's check) | Q1, Q3, Q4 | **#585** (ruling (e): the `#585` line in `02`, never sent; the layer -- ROCKNIX's distribution first, a mainline SoC dtsi unlikely to take a distribution's reservation (D-SYS-004) -- stated as a question, § 4 question 2) |
| **L-17** | the inventory's `tier` / `tier_note` columns over the 107 (R1 § 8 delta 3; R4 item 6) | **`0 fork-own` by the tool, one fork-written row by `tier_note`**: the rule tiers every patch `vendor-carried`; #688's body says *"0 of them fork-own"*; T27 ruled *cite it, do not re-tier it* | tool-run | the block's `tier: {'vendor-carried': 107}` and `fork-own rows: []` beside C13's `tier_note values over the 107: 1 fork-written; 106 None;` (the lane's awk over `block-2.txt`'s TSV: `awk -F'\t' ... $ix["tier_note"]=="fork-written"` prints `1`) | Q6 | **inherited:coordinator** (whether the tier rule or `last_fork_commit` is a tooling defect to file beside #1049, #1056, #1086) |
| **L-18** | #1049, #1056, #1086, #1101, #879, #1053 (R4 item 3) | **the inventory's six reach gaps**, none a kernel-patch gap: `PKG_DEPENDS_UNPACK`; symlinked `patches`; overlay sources; the kernel recipe's own unpack and copy edges (`intel-ucode`, `generic-dsi`); `PKG_ARCH` ignored; a host plan's `xmlstarlet` | record | one sentence per gap in `02` saying which row of the 107 it could move (expected none), each with its issue's state read by `gh` | Q6 | **none** (each bug's owner is the tooling area; stated as a check) |
| **L-19** | `projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf` (8,608 lines; R4 item 4; R2 § 4) | **the one configuration, never fork-changed, changed upstream four times since the base**: `+0 -0` against `c445081a59`; `7 7` against `651150fc88` -- gcc 15.2.0 -> 16.2.0, rustc 1.98 -> 1.99 / LLVM 22 -> 23, `+CONFIG_CC_HAS_COUNTED_BY_PTR=y`, `-# CONFIG_INPUT_POLLDEV is not set`, `RAID6_PQ_BENCHMARK` y -> n (`5f56cd5150`); header `# Linux/arm64 7.2.0 Kernel Configuration` level with the pin; the build copies it to `.config`, forces the hostname and `INITRAMFS_SOURCE`, disables `SWAP`/`NFS_FS`/`CIFS`/ISCSI/`WIREGUARD` by option, then `oldconfig` (R3 § 1.1); a `devices/SM8550/linux/7.2/linux.aarch64.conf`, if one appeared, would silently take precedence (`kernel_config_path`'s first candidate) | tree, history | `git diff --numstat c445081a59 HEAD -- <conf>` prints nothing; `git -C /workspace/repos/pixelelated/distribution diff --numstat 2174265e9c 651150fc88 -- <conf>` prints `7 7 ...`; the four conf-diff counts of § 5 (each naming its side) | Q4 | **row** (`upstream-changed`, the integration carries; the four counts in the row; ruling (d), (j)) |
| **L-20** | `projects/ROCKNIX/devices/SM8550/patches/linux/0002-qcom-dispcc-sm8550-Fix-disp_cc_mdss_mdp_clk_src.patch`; #328 (R4 item 9) | **#328's once-per-boot dispcc warning is upstream's kernel's**, the fork's patch set the same as stock 20260901; upstream's `0017-clk-qcom-blank-dsi-panels-before-dispcc-park.patch` (215 lines, in the qcom-bls merge) is the lead the merge brings | record | `gh --repo pixelelated/distribution issue view 328 --json state,title --jq '.state'` read at stage A; `git -C /workspace/repos/pixelelated/distribution show 651150fc88:projects/ROCKNIX/packages/linux/patches/7.2/0017-clk-qcom-blank-dsi-panels-before-dispcc-park.patch \| sed -n '1,12p'` for its subject | Q4 | **row** (the `0002` row cites #328 and names `0017`; nothing diagnosed; the integration's) |
| **L-21** | the five `non-kernel` rows (R1 § 8 delta 4; ruling (b)) | **the title says kernel, the globs say `devices/**`**: four U-Boot patches and one firmware patch among the 107 | tree | `GROUPS`'s `KIND TOTAL K5 other 5 466` line | Q7 | **row** (labelled `non-kernel`; **inherited:coordinator** for the order's wording, a delta recorded) |
| **L-22** | the 12 files upstream added under the shipped kernel directories since the base (R1 § 5; R2 § 4; R4 § 6 item 2) | **six `7.2/` patches, two SM8550 patches the shipped kernels would take at the merge; four `7.2.6/` for T43's targets**; after the merge `7.2/` holds 12, `mainline/` 3, H700 32, SM8550 57 (R2 § 4) | history | `git -C /workspace/repos/pixelelated/distribution diff --name-status c445081a59 651150fc88 -- projects/ROCKNIX/packages/linux/patches projects/ROCKNIX/devices/H700/patches/linux projects/ROCKNIX/devices/SM8550/patches/linux projects/ROCKNIX/devices/SM8550/linux \| awk '{print $1}' \| sort \| uniq -c` prints `12 A`, `1 D`, `4 M` (R1 C11) | Q4 | **row** (one line per addition in `02` § Upstream since the base, *the integration carries*; not rows of the 107) |
| **L-23** | the `120000` entries under the member roofs (R3 § 1.5; R5 § G (e); #1056) | **no symlinked `patches` directory among the nine** -- #1056's gap moves no row here; 3 symlink entries exist under the roofs at P1 (`v1 read`; named in `## Version 1` item 6) | tree | `git ls-tree -r HEAD \| awk '$1=="120000"{print $4}' \| /usr/bin/grep -E '^(projects/ROCKNIX/(devices\|packages/linux)\|packages/linux)'` with each target by `git show HEAD:<entry>`; none ends in `/patches` of a member directory | Q6 | **none** (stated as a check in `02`) |
| **L-24** | `0004-drm-msm-a6xx-Enable-IFPC-on-Adreno-740.patch` (R1 C09; R4 item 14) | **the one file without a trailing newline**: `wc -l 32 grep -c 33` | tool-run | `git show HEAD:<path> \| wc -l` and `\| /usr/bin/grep -c ''` print `32` and `33` | Q7 | **row** (named beside both totals; a delta, not a finding) |
| **L-25** | `projects/ROCKNIX/devices/H700/patches/linux/0154-rocknix-dt-id.patch` (44 lines, hand-made, 4 dts files; R4 item 11) | **read by three slices**: the dt-id the RG35XX SP's tree boots with; `bootloader/update.sh` reads `rocknix-dt-id`; device-facts L15 does not say which of the SP's two trees the LPDDR4 unit boots | tree, record | `git show HEAD:<path> \| /usr/bin/grep -c 'rocknix-dt-id'`; `git grep -n 'rocknix-dt-id' HEAD -- projects/ROCKNIX/devices/H700/bootloader` | Q2 | **row** (its readers and L15 named; **inherited:T27** for the open item) |
| **L-26** | `projects/ROCKNIX/devices/SM8550/patches/linux/0105-drm-panel-Add-Retroid-Pocket-Nova-panel.patch` (453 lines, hand-made; R4 item 12) | **adds the Nova's panel `il97680a,rpnova`** -- the shipped unit's panel driver in a header-less patch | tree | `git show HEAD:<path> \| /usr/bin/grep -c 'rpnova'` | Q2 | **row** (the shipped unit it serves named) |
| **L-27** | `projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf`, `projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf` (ruling (d); R1 § 1) | **the two excluded configurations** are T27's and T11's; the ramoops row's config half (six `+CONFIG` lines) lives in the first | tree | the block's `CLAIMS` CONF lines name both with their owners; `git show HEAD:projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf \| /usr/bin/grep -n -E '^CONFIG_PSTORE_(RAM\|CONSOLE)=y'` prints the two lines (`:7290`, `:7292` at the tip, R2 command 8) | Q6 | **none** (cited where a row needs them) |
| **L-28** | `projects/ROCKNIX/packages/linux/package.mk:385-404` (the `qcom-abl` branch); upstream's `cafbb1657d` 2026-10-22 (R4 item 22; #1099; T28 PL-02) | **upstream's Qualcomm BLS boot change reaches the kernel recipe's `makeinstall_target` at the merge**; the SM8550 rows' *version made against* stays 7.2 | history | `git -C /workspace/repos/pixelelated/distribution log --format='%h %cs %s' -1 cafbb1657d` | Q4 | **none** (T11's recipe, T28's device; #1099 named, not acted on) |
| **L-29** | `config/functions:1449-1472` (`kernel_config_path`); `config/arch.arm:80` (R3 § 1.1; R1 § 10) | **the conf's resolution for the `arm` plans**: `TARGET_KERNEL_PATCH_ARCH="aarch64"` makes the 32-bit userland's kernel read the same `linux.aarch64.conf`; the nine candidates in order, the first that exists winning | tree | `git show HEAD:config/functions \| sed -n '1449,1472p'`; `git show HEAD:config/arch.arm \| sed -n 80p` | Q7 | **row** (the conf row's method column) |
| **L-30** | `scripts/unpack:127-133`; `projects/ROCKNIX/devices/GENERIC_X64/options:10` (R3 § 1.1; T40's errata `:447-451`) | **GENERIC_X64's `TARGET_KERNEL_PATCH_ARCH=x86_64` is pre-empted by `unpack:127`'s `x86`**, so it names only the config file (`linux.x86_64.conf`); H700 and SM8550 patch as `aarch64` on both userlands | tree | `git show HEAD:scripts/unpack \| sed -n '127,133p'` (`v1 read`: the three-way rule); `git show HEAD:projects/ROCKNIX/devices/GENERIC_X64/options \| sed -n 10p` | Q7 | **row** (the `PATCH_ARCH` column per plan; ruling (g)) |
| **L-31** | `7.0/0010`, `7.2/0010`, `7.2/0013-drm-msm-dpu-fix-inline-rotation.patch`, `7.2/0016-drm-msm-dp-...` (R3 § 2 (iii)) | **applied is not built**: the Qualcomm DRM patches touch a driver an x86 or H700 config does not compile; the conf decides it | tree | `git show HEAD:projects/ROCKNIX/devices/{H700,SM8550}/linux/linux.aarch64.conf \| /usr/bin/grep -n -E '^CONFIG_DRM_MSM='` -- SM8550's prints a line, H700's does not `[unverified]`; the GENERIC_X64 line is T11's conf, read the same way | Q6 | **row** (an *applied, not built* note on those rows; the conf line quoted) |

**Not leads (checked, pass).** The 106 upstream-carried patches are
byte-identical to the merge base (R1 C07); the fork never edited a kernel
patch or the SM8550 configuration (R1 § 5); `next` moved nothing on the member
directories since the P1 tip (R2 command 7); the three pinned tarballs are
cached with their `.sha256` and `.url` (R3 § 1.4; `v1 read`), and so are
`u-boot-DDR3-v2026.01.tar.gz`, `u-boot-DDR4-v2026.01.tar.gz` and
`kernel-firmware-20260309.tar.gz` under their package directories (`v1 read`:
`ls /workspace/cache/rocknix-sources/{u-boot-DDR3,u-boot-DDR4,kernel-firmware}/`);
no record of the last builds names a kernel version (R3 § 2: `0` hits for
`linux|kernel|uname` over every `RECORD*` and `*.identity.json`), so the
version of each build is the override's `case` at its `build_commit` -- `7.2`
and `7.1.2` at the tip, `[unverified]` at `069fc2704421` and `bcc866f1f314`
(`git -C /workspace/repos/rocknix show <commit>:projects/ROCKNIX/packages/linux/package.mk
| grep -n PKG_VERSION`, a read, is the lane's if the row wants it).

## 4. The questions

The seven renovation questions of plan § 4, restated for this slice with
**package currency** as the lens (`order.md:695`) and the table as the answer
(T40's § 4 shape, R5 § A). All seven headings are written in
`04-analysis.md` § Renovation face because the lint requires them (R3
§ 1.7); **Q5 is struck in substance** (plan § 7 item 4: *"a provenance table
has no Q5"*) and says so in one sentence. Each is answered with the evidence at
its lines; the leads are § 3's, cited by number.

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | A patch written against a mechanism the kernel has since taken or retired: the mailing-list imports whose header dates them before the pinned kernel (L-06: present in the 7.2 tarball = `superseded at this pin`, a lead to T11, never a removal); the polldev driver upstream moved to RK3326 alone (L-14); the ramoops node against mainline 7.2's dtsi (L-16); upstream's `7.2.6/` symlinks as the answer to the duplicated `7.0/` triple (L-03) | the applies-at-pin run and the tarball greps (§ 5); `git log -S` on the carrying commit before a patch is called superseded |
| Q2 Standards | The patches' own conventions: a header that says what the patch is for (`From:` 87, `Subject:` 89, 17 hand-made, 2 stripped, L-05, L-13); numbering collisions and mixed names against `unpack`'s sort (L-04); `patches/<arch>` names against the arches `unpack` can produce (T40's generalised check: `x86`, `aarch64`, `arm`; none exists under the override, R1 C13); the configs' headers against the pin (L-07 cited, L-19) | the header census line; the application index column; `git ls-tree` of the nine directories |
| Q3 Bugs | **A patch a shipped image should apply and does not** (#1054 criterion 6; the applies-at-pin run's `fails`), and **a carried patch found wrong at the pin**: the unfixed `0010-msm-resource-cleanup.patch` in `7.0/` and `7.2/` (L-01, ruling (c)) -- each a `bug` with its code trace, its `Already written:` line (what the kernels built so far carry: the pre-fix bytes in every H700, SM8550 and GENERIC_X64 image since the base; the fix reaches them with the base merge) and ruling (h)'s VM line. Upstream's quoted `=~` (L-02) is upstream's defect: a `#585` line, not a fork bug | the `patch --dry-run` lines; the two `0010` diffs against `upstream/next`; `9416eec2c2`'s message |
| Q4 Currency -- **the lens** | **Per row** (§ 5's columns): the target version the header or content names; the current pin of each device that applies it (`7.2` H700/SM8550, `7.1.2` GENERIC_X64, the recipe's `case` as text); applies-at-pin; upstream status as the header claims it (`Link:`/`Upstream-Status:` on 4 rows) and as `upstream/next` shows it (`101 SAME / 4 CHANGED / 2 GONE`, R1 C11); backport status; the fork's reason (the carrying commit's message at ROCKNIX, `cbf75c0b06`'s for the one fork-written). **Per directory**: what upstream added since the base that the fork lacks (12 files, L-22), what it moved (L-14), what it changed (L-01, L-19, `0104`), the `rocknix-joypad` group (L-02, L-14) -- *the integration carries*, the lane records (ruling (f)) | the generator's table; `02` § Upstream since the base; the four conf-diff counts |
| Q5 Efficiency | **Struck in substance**: no row runs on a launch path; nothing here moves either time-to-play number. The one cost named is the integration's: 106 upstream patches re-applied at every base merge, 8 upstream commits since the base, two recipe hunks to re-apply (R1 § 4, § 5) | one sentence; `time-to-play.md` |
| Q6 Dead ends | What a kernel applies but does not build (`applied, not built`: the Qualcomm DRM patches under an H700 or x86 config, L-31); `PKG_PATCH_DIRS` words that select nothing (L-15); the `.patch.disabled` beside the live ones (L-10, context only); the inventory's reach gaps and the symlink question (L-18, L-23); the two configurations the slice does not row (L-27) | the conf's `CONFIG_DRM_MSM` line; `git cat-file -e` on the absent directories; the block's `CLAIMS` |
| Q7 Clarity | Can a reader tell what each patch is for and whether it is current in one pass: the squashed series' subjects (L-13); the duplicated triple (L-03); the five `non-kernel` rows under a kernel title (L-21); the rules' sentence naming the dead directory (L-09); the one unterminated file (L-24); the tier that hides the one fork-written row (L-17) | the Files/hunks cell; the `GROUPS` lines; `grep -n` of the two rule lines |

**The ladder, applied to every finding** (`working-principles.md` §
Enforcement depth): each punch item says which stage it sits at and the tool
that would hold it at the next -- `tools/renovation-drift` for a kernel bump
that renames `7.2/` (R3 § 1.6), a `cmp` of the `7.0/`/`7.2/` pairs in a fork
check (L-03), `tools/renovation-inventory`'s `tier_note` surfaced in `--order`
(L-17) -- or the words *no tool can*.

**The questions for the maintainer, framed here and put by the coordinator**
(the lane raises each on #688 at the stage-D pause with its evidence; it does
not ask the maintainer itself; `player-language.md` § How to apply: a decision
is put in terms of what one would see):

1. **The three `7.0/` copies that equal `7.2/`'s: keep two files, or one file
   and a symlink, as upstream's `7.2.6/` does?** (L-03) Today a fix made to
   one copy -- upstream's `9416eec2c2` fixed both by hand -- leaves the other
   behind; a symlink would make the test image's `0010` follow the shipped
   kernels'. A recipe-tree change, after the base merge, the maintainer's
   word; never this lane's edit (D-WORKFLOW-209).
2. **The ramoops patch's contribution layer: ROCKNIX's distribution (the
   H700 directory is theirs), or a mainline `sun50i-h616.dtsi` change?**
   (L-16; D-SYS-004: *"Not something mainline would take in a SoC dtsi; the
   fork carries it"*; #369 parked.) The `#585` line is written either way and
   nothing is sent (D-WORKFLOW-165); the layer decides the line's target.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict, as its `SKILL.md` §
Evidence floor lists them, restated for a table as T40's § 5 did (R5 § A):

1. *Tracker state is never sole evidence.* Every cell cites a command's output
   -- the inventory's row, a `git show` at a hash, a header line, `patch`'s
   own line, a register row, an issue's state read by `gh` -- or a
   `file:line`.
2. *Mechanical evidence outranks reading.* **A patch's header is the patch's
   own claim about its origin, recorded as such** (T40's rule 2); `unpack`'s
   directory list and the recipe's `case` are the evidence for what applies
   where; `patch --dry-run`'s line is the evidence for whether it applies.
3. *The bench is the host; no guest, no build, no plan, no network, no
   `config/options`.* **Can this be done on the VM? No -- the tree, the
   history and the cached tarballs show it; nothing a guest shows is a
   provenance fact** (ruling (h); D-WORKFLOW-187). The inventory, the
   headers, the recipe's `case` and the devices' `options` read at the hash,
   `scripts/unpack` read, `git log` and `git show`, upstream at
   `651150fc88` in the local store, and the pinned tarballs already in
   `/workspace/cache/rocknix-sources/` extracted file by file into the lane's
   scratch (ruling (g)). A patch's run-time effect -- a DTS node, a driver, a
   panel -- is a handheld fact, never tested here (R3 § 3: the guest can show
   the *effects* of nine patches, never their application, never the SM8550
   conf; the recommendation is no window). **This paragraph is the VM line
   #688's body takes in place of its generated one.**
4. *An assertion that cannot fail is not evidence.* Before recording a PASS,
   ask what result would have produced a FAIL -- at Local depth nobody else
   asks it; `tools/pkgcheck` exiting 0 on a name that matches nothing is the
   shape (R3 § 1.2), and so is `patch --dry-run` run against an empty scratch
   (every new-file hunk "applies").
5. *Subagent output is a LEAD, never EVIDENCE.* Fan-out inside this lane is
   read-only research subagents only (D-WORKFLOW-183); for this slice none is
   needed -- the generator fills 106 rows and the lane reads one patch line by
   line.

- **The reads at the tip.** The 107 are read at the lane's tip's bytes
  (ruling (a)) -- `git show HEAD:<path>` -- which are the P1 tip's (106 of
  them the merge base's); upstream's copies by `git -C
  /workspace/repos/pixelelated/distribution show 651150fc88:<path>`;
  T40's and the device slices' records by `git -C <their worktree> show
  <hash>:<path>`. Nothing is exported whole: a kernel tree is 1.5 GB per
  version, and the scratch holds only the files the patches touch.
- **A read is free and goes through the filter.** No member is a config file
  that carries a sign-in, and the one header quoted carries a `noreply`
  address (R1's header); but issue bodies and `options` files are read, so
  any line quoted from an issue goes through `engineering-practices.md`'s two
  masks (§ Nothing runs on a person's device, the `sed` of the flag form
  included), and a variable is named, never its value. **The wordlist**
  (`~/.config/rocknix/forbidden-terms`) is never read, listed or quoted
  (D-WORKFLOW-061): `tools/forbidden-terms-check` is its only reader, and the
  secret scan sources `.githooks/secret-patterns` alone, never `guard_load`.
- **The tarballs are read, never built.** `tar -tJf` lists, `tar -xJf ... -C
  <scratch> -T <members>` extracts the named members only, `sha256sum` is
  compared with the `.sha256` beside each and with the recipe's `PKG_SHA256`
  as text; no `scripts/unpack`, no `kernel_make`, no `make kconfig-*`, no
  `tools/adjust_kernel_config` or `check_kernel_config` (ruling (g); R3
  § 1.3).

**`# STAGE A` -- the first commands, before anything else** (in the lane's
worktree, under bash, after the pointer's eleven keys, § 10). `rc=$?` sits on
its own line after each command; the expected lines are research lines cited
in their comments, `v1 read` lines, or marked `[unverified]`:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-kernel-688
cd "$D"
cat .github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md   # the pointer: the dispatch's hashes; § 10 names the eleven keys to check
export LC_ALL=C; G=/usr/bin/grep; T=/workspace/tmp/m6-t41; W=/workspace/tmp/m6-coordinator/t11-research/tree; S=/workspace/cache/rocknix-sources; mkdir -p "$T/tmp" "$T/src"; df -i /workspace | tail -n 1
date -u +%Y-%m-%dT%H:%M:%SZ
git branch --show-current                                                    # feature/m6-patches-shipped-kernel-688
git status --short | $G -c ''                                                # 0
git rev-parse --short=10 HEAD                                                # __COHASH__ at stage A: the branch is cut from the coordinator's tip, no merge commit (ruling (a))
git merge-base --is-ancestor 2174265e9c HEAD && echo carries-p1              # carries-p1 (ruling (a); v1 read: true at 6a12ce2d73)
git merge-base --is-ancestor 8ebaf8daad HEAD && echo next-is-here            # next-is-here
git -C /workspace/repos/pixelelated/distribution rev-parse --short=10 upstream/next   # information only: the local ref MOVES (651150fc88 at v1; 50433c03cc on 2026-11-02, 59 commits on, proof K94); every command below pins 651150fc88, the commit the expectations were read at (ruling (f), proof X01)
sha256sum docs/reviews/slices.json docs/reviews/inventory.json docs/reviews/areas.json | cut -c1-16   # 49bc2745664e52f4, d17b9cac4b2c2245, 985f742cfd4a2138 (R1 C02): the block's inputs, present because the tip carries P1
test -d "$W" && echo clone-here                                              # clone-here: the block's W, read by git -C only (R1 C18 re-ran the block against it)
# the lint's PASS on a Local plan, before anything else (ruling (i)): T4's finished Local folder, exported from T4's tip and linted by this tip's lint; then a copy with its tier_exception removed, which must FAIL
F=$(git ls-tree -d --name-only 6ec78bbf8c docs/audits/ | $G -E -e '-epic-m6-doctrine-rules$'); echo "T4 folder: $F"   # docs/audits/2026_10_24-epic-m6-doctrine-rules (v1 read)
L=$T/lint-proof; mkdir -p "$L/pass" "$L/fail"
git archive 6ec78bbf8c "$F" | tar -x -C "$L/pass"; git archive 6ec78bbf8c "$F" | tar -x -C "$L/fail"
python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); print("t4 plan:", d.get("depth"), d.get("tier_exception"), len(d.get("reviewers") or []))' "$L/pass/$F/second-opinions/review-plan.json"   # `t4 plan: local D-WORKFLOW-184 0` (T39's proof K111 on the same folder)
python3 -I -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d.pop("tier_exception",None); json.dump(d,open(p,"w"),indent=2)' "$L/fail/$F/second-opinions/review-plan.json"
tools/lint-audit-artifacts "$L/pass/$F" > "$T/tmp/lint-local-pass.out" 2>&1; rc=$?
echo "lint, a Local plan, rc=$rc"; tail -n 3 "$T/tmp/lint-local-pass.out"   # rc=0 and a line ending `PASS`: the proof ruling (i) asks for
tools/lint-audit-artifacts "$L/fail/$F" > "$T/tmp/lint-local-fail.out" 2>&1; rc=$?
echo "lint, tier_exception removed, rc=$rc"; $G -n 'FAIL' "$T/tmp/lint-local-fail.out"   # rc=1 with `FAIL  second-opinions/review-plan.json or its call evidence is invalid: local-only cannot satisfy Epic/Milestone` (T39's K111) -- the PASS's FAIL-first
# the brief's block, extracted by its markers at __V2HASH__ and checked, never retyped (§ 2)
BR=__V2HASH__   # the pointer's value, never the literal word: unfilled, the show fails and nothing below runs
git show "$BR:docs/reviews/briefs/patches-shipped-kernel.md" > "$T/tmp/brief.md"; rc=$?
echo "brief read rc=$rc"
mkdir -p .qa-scratch/t41
python3 -I -c 'import sys,re
t=open(sys.argv[1]).read()
seg=t[t.index("<!-- t41 block.sh begin -->"):t.index("<!-- t41 block.sh end -->")]
open(".qa-scratch/t41/block.sh","w").write(re.search(r"\n```bash\n(.*?)\n```\n", seg, re.S).group(1)+"\n")
seg=t[t.index("<!-- t41 block expected begin -->"):t.index("<!-- t41 block expected end -->")]
open(".qa-scratch/t41/block-expected.txt","w").write(re.search(r"\n```\n(.*?)\n```\n", seg, re.S).group(1)+"\n")' "$T/tmp/brief.md"
sha256sum .qa-scratch/t41/block.sh | cut -c1-16; $G -c '' .qa-scratch/t41/block.sh .qa-scratch/t41/block-expected.txt   # 4d300124a6bf116f; 148 and 99 (R1 C18)
# the membership at P1 (§ 2): expect the 99 expected lines byte for byte
bash .qa-scratch/t41/block.sh > "$T/tmp/block.out" 2>&1; rc=$?
echo "block rc=$rc"; diff .qa-scratch/t41/block-expected.txt "$T/tmp/block.out" && echo "block = the brief's expected lines"
mkdir -p "$T/stage-a-p1" && cp -a .qa-scratch/t41/. "$T/stage-a-p1/"   # the P1 run's TSV and paths, saved before the tip re-run overwrites them; the generator reads this copy (§ 5)
# the same at the lane's tip (ruling (a)): W rebound to this worktree, P1 to HEAD; expect the same 99 lines [unverified]: a differing line is a delta recorded beside the expectation, and a differing `mine:` or GROUPS line a question on #688
sed -e "s#^W=/workspace/tmp/m6-coordinator/t11-research/tree; P1=2174265e9c;#W=$PWD; P1=$(git rev-parse HEAD);#" .qa-scratch/t41/block.sh > .qa-scratch/t41/block-tip.sh
$G -c -F "W=$PWD" .qa-scratch/t41/block-tip.sh                               # 1: the rebinding took
bash .qa-scratch/t41/block-tip.sh > "$T/tmp/block-tip.out" 2>&1; rc=$?
echo "block at the tip rc=$rc"; diff "$T/tmp/block.out" "$T/tmp/block-tip.out" && echo "the same lines at the tip"
# the host file, read once (ruling (h)); this slice writes no line there
H=/workspace/tmp/m7-m6-host-coordination.txt; date -u +%H:%M:%S; wc -l < "$H"; tail -n 6 "$H" | cut -c1-200   # __HOSTLINES__ at dispatch (712 at this draft's read, v1 read); read for the protocol only
```

Then the runs below. **If the lint's Local PASS does not print**, the lane
records the lint's lines in `00`, names it on #688 as one question before
stage C, and goes on with stage B's reading, which does not depend on it
(T38's and T39's contingency, the same shape).

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...*; the lane wraps each in its own `rc=$?` line and a
`date +%s` pair, or records that it did not; a run that cannot be made is
`CANNOT` with its reason). From the lane's worktree after the membership
block, under bash with `LC_ALL=C`; counts by `/usr/bin/grep`; `rc=$?` on its
own line, never after a pipe; no `cut` on an expected error line; every line
read from an issue body goes through the mask; **every expectation below is a
research file's printed line, cited in its comment, a `v1 read`, or marked
`[unverified]`, and the lane re-runs every one as its own line -- a line that
differs is recorded beside the expectation, not argued with**:

```bash
export LC_ALL=C; G=/usr/bin/grep; T=/workspace/tmp/m6-t41; S=/workspace/cache/rocknix-sources; U=/workspace/repos/pixelelated/distribution
P=.qa-scratch/t41/paths.txt   # the 107, from the P1 run of the block (saved under $T/stage-a-p1 too)
# the tool's own row (R1 C14 ran it from the clone: rc=0, 50 lines, `unassigned: 0`, `ambiguous: 0`, the T41 row) [unverified from the worktree]
git status --short --ignored | $G -c ''
./tools/renovation-inventory --order --no-write --distribution "$W" > "$T/tmp/order.out" 2>&1; rc=$?
echo "renovation-inventory --order rc=$rc lines=$($G -c '' "$T/tmp/order.out")"; $G -E '^(slices|rows|unassigned|ambiguous):|^ *41 patches-shipped-kernel ' "$T/tmp/order.out"
git status --short --ignored | $G -c ''                                      # the same count as before the run (R1 C14: 2 in the clone)
# the recipe's pins and patch directories as text, never sourced (R1 C06; v1 read): the case labels, PKG_VERSION, PKG_SHA256 and PKG_PATCH_DIRS lines
git show HEAD:projects/ROCKNIX/packages/linux/package.mk | $G -n -E '^\s*(PKG_VERSION|PKG_SHA256|PKG_PATCH_DIRS)[+]?=|^\s*[A-Z0-9|]+\)\s*$' | cut -c1-120   # :16 PKG_PATCH_DIRS="${LINUX} mainline ${DEVICE} default"; :29-31 the 7.2 group with f9fef3d1...; :36-38 RK3326|AMD64|GENERIC_X64 7.1.2 with 37198c93...; :40 PKG_PATCH_DIRS+=" 7.0"
git show HEAD:projects/ROCKNIX/packages/linux/package.mk | sed -n '33,34p'   # the recipe's own comment on the 7.2 directory (R2 § 0)
for d in H700 SM8550 GENERIC_X64; do git show "HEAD:projects/ROCKNIX/devices/$d/options" | $G -n -E 'LINUX=|KERNEL_TARGET|TARGET_KERNEL_PATCH_ARCH' | sed "s/^/$d:/"; done   # no LINUX= (R1 C08); KERNEL_TARGET Image, Image, bzImage (R1 C06); GENERIC_X64:10 TARGET_KERNEL_PATCH_ARCH="x86_64" (R3 C5)
git show HEAD:config/arch.arm | sed -n 80p                                   # TARGET_KERNEL_PATCH_ARCH="aarch64" (R3 C5)
git show HEAD:scripts/unpack | sed -n '127,159p'                             # the PATCH_ARCH rule and the globs' order (R1 C05; v1 read of :127-133)
# the nine directories' counts and the three plans' application order (v1 read at 2174265e9c: GENERIC_X64 4+4 total 8; H700 4+6+32 total 42; SM8550 4+6+55 total 65), files sorted under LC_ALL=C as the container's shell globs
order() { case "$1" in GENERIC_X64) dirs="projects/ROCKNIX/packages/linux/patches/mainline projects/ROCKNIX/packages/linux/patches/7.0";; H700|SM8550) dirs="projects/ROCKNIX/packages/linux/patches/mainline projects/ROCKNIX/packages/linux/patches/7.2 projects/ROCKNIX/devices/$1/patches/linux";; esac; for d in $dirs; do git ls-tree -r --name-only HEAD -- "$d" | $G -E '\.patch$' | sort; done; }
for dev in GENERIC_X64 H700 SM8550; do order "$dev" > "$T/order-$dev.txt"; echo "$dev total: $($G -c '' "$T/order-$dev.txt")"; done
for d in 7.0 7.2 mainline; do echo "$d: $(git ls-tree -r --name-only HEAD -- projects/ROCKNIX/packages/linux/patches/$d | $G -c -E '\.patch$')"; done   # 4, 6, 4 (R1 C13)
for d in H700 SM8550; do echo "$d: $(git ls-tree -r --name-only HEAD -- projects/ROCKNIX/devices/$d/patches/linux | $G -c -E '\.patch$') patches, $(git ls-tree -r --name-only HEAD -- projects/ROCKNIX/devices/$d/patches/linux | $G -c '\.disabled$') disabled"; done   # 32 and 1; 55 and 1 (R1 C13)
for d in H700 SM8550 GENERIC_X64 default aarch64 x86 7.1.2; do git cat-file -e "HEAD:projects/ROCKNIX/packages/linux/patches/$d" 2>/dev/null || echo "absent patches/$d"; done   # seven `absent` (R1 C13; R3 § 0): the words of PKG_PATCH_DIRS and the arch/version forms that select nothing
# the header census (R1 C13: From: 87, Subject: 89; R2 § 1: 17 hand-made)
n=0; f=0; s=0; while IFS= read -r p; do case "$p" in *.patch) n=$((n+1)); h=$(git show "HEAD:$p" | head -n 60); printf '%s\n' "$h" | $G -q -E '^From: ' && f=$((f+1)); printf '%s\n' "$h" | $G -q -E '^Subject: ' && s=$((s+1));; esac; done < "$P"; echo "patches $n with From: $f with Subject: $s"
while IFS= read -r p; do case "$p" in *.patch) git show "HEAD:$p" | $G -n -m1 -E '^(Link:|Upstream-Status:)' | sed "s#^#$p:#";; esac; done < "$P" | cut -c1-160   # 4 lines: H700 0160, SM8550 0006, 7.2/0011, 7.2/0016 (R2 § 1; v1 read)
# byte identity against the merge base and upstream (R1 C07: SAME 106, ADDED 1; R1 C11: SAME 101, CHANGED 4, GONE 2)
for B in c445081a59 651150fc88; do while IFS= read -r p; do if git -C "$U" cat-file -e "$B:$p" 2>/dev/null; then [ "$(git -C "$U" rev-parse "$B:$p")" = "$(git rev-parse "HEAD:$p")" ] && echo "vs $B SAME" || echo "vs $B CHANGED"; else echo "vs $B ABSENT"; fi; done < "$P" | sort | uniq -c; done
# upstream's changes under the shipped kernel directories since the base (R1 C11: 12 A, 1 D, 4 M) and the five files of the 107 it touched (R1 C11's name-status)
KD="projects/ROCKNIX/packages/linux/patches projects/ROCKNIX/devices/H700/patches/linux projects/ROCKNIX/devices/SM8550/patches/linux projects/ROCKNIX/devices/SM8550/linux"
git -C "$U" diff --name-status c445081a59 651150fc88 -- $KD | awk '{print $1}' | sort | uniq -c
git -C "$U" diff --name-status c445081a59 651150fc88 -- $KD | $G -E '^[DM]' | cut -c1-140
git -C "$U" diff --name-status c445081a59 651150fc88 -- $KD | $G -E '^A' | cut -c1-140
tr '\n' '\0' < "$P" | xargs -0 git -C "$U" diff --shortstat c445081a59 651150fc88 --   # ` 5 files changed, 36 insertions(+), 515 deletions(-)` (R1 C11)
tr '\n' '\0' < "$P" | xargs -0 git -C "$U" log --format='%h %cs %s' c445081a59..651150fc88 -- | cut -c1-120   # 8 lines, 7 non-merge (R1 C11)
git -C "$U" diff --stat 2174265e9c 651150fc88 -- projects/ROCKNIX/packages/linux/patches/7.2/0010-msm-resource-cleanup.patch projects/ROCKNIX/packages/linux/patches/7.0/0010-msm-resource-cleanup.patch | tail -n 1   # ` 2 files changed, 28 insertions(+), 22 deletions(-)` [unverified]: v1 read of the 7.2 copy alone printed ` 1 file changed, 14 insertions(+), 11 deletions(-)`
git -C "$U" show 651150fc88:projects/ROCKNIX/packages/linux/package.mk | sed -n '16,20p;26,53p' | cut -c1-120   # upstream's :18 rocknix-joypad line with its quoted =~ (R2 L-02); the pins: 7.2 unchanged for the H700 group, 7.1.2 for RK3326|AMD64 (GENERIC_X64 absent), 7.2.11 with 7.2.6 for RK3566|RK3576|S922X, 6.18.54 for RK3399 (R1 C16; R2 § 4)
for n in RK3326 RK3399 S922X H700 SM8550; do [[ "$n" =~ "RK3326|RK3399|S922X|H700" ]] && echo "$n quoted-match" || echo "$n no-match"; done   # five `no-match` (R2 command 14): L-02
git -C "$U" ls-tree -r --name-only 651150fc88 | $G -c -F 'rocknix-joypad/'   # the group's directory anywhere at 651150fc88: 0 under the override's patches (R1 § 10); the whole-tree count [unverified]
# the fork's side: its commits on the 107 and on the recipes (R1 C10: 6, one non-merge; the two recipe hunks)
tr '\n' '\0' < "$P" | xargs -0 git log --format='%h %cs %an %s' c445081a59..HEAD -- | cut -c1-120   # 6 lines at 2174265e9c; the coordinator's branch may add merges [unverified]
tr '\n' '\0' < "$P" | xargs -0 git log --no-merges --format='%h %cs %an %s' c445081a59..HEAD -- | cut -c1-120   # 1 line: cbf75c0b06 2026-09-10
git log --no-merges --format='%h %cs %s' c445081a59..HEAD -- projects/ROCKNIX/packages/linux/package.mk packages/linux/package.mk | cut -c1-120   # dc948f59aa 2026-08-21 and 3d7c075f63 2026-10-02 (R1 C16)
git diff --shortstat c445081a59 HEAD -- projects/ROCKNIX/packages/linux/package.mk packages/linux/package.mk   # ` 2 files changed, 5 insertions(+), 5 deletions(-)` (R1 C10)
tr '\n' '\0' < "$P" | xargs -0 git log --oneline --since=2026-06-01 HEAD -- | $G -c ''   # 64 at 8ebaf8daad (R5 C15); the tip's line is the record
# the duplicate pairs (R2 command 10: all identical) and the duplicate detector's three strictnesses (the generator)
for f in 0010-msm-resource-cleanup.patch 9998-silence-initramfs-unpack-warn.patch 9999-fix-rust-build-error.patch; do cmp <(git show "HEAD:projects/ROCKNIX/packages/linux/patches/7.0/$f") <(git show "HEAD:projects/ROCKNIX/packages/linux/patches/7.2/$f") && echo "identical 7.0/7.2 $f"; done
for f in 0001-Update-dram_sun50i_h616.c.patch 0002-sunxi-axp717-charge-only-boot.patch; do cmp <(git show "HEAD:projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/patches/$f") <(git show "HEAD:projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/patches/$f") && echo "identical DDR3/DDR4 $f"; done
# the symlink question (R3 § 1.5; R5 § G (e); v1 read: 3 entries under the roofs at P1, all ALSA ucm .conf under RK3566's and SM8750's filesystem overlays, none a patches directory)
git ls-tree -r HEAD | awk '$1=="120000"{print $4}' | $G -E '^(projects/ROCKNIX/(devices|packages/linux)|packages/linux)'
# the ramoops patch (ruling (e); R1 C10, C11; R2 command 8)
R=projects/ROCKNIX/devices/H700/patches/linux/0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch
git log --format='%h %cs %an %s' HEAD -- "$R" | cut -c1-120                 # cbf75c0b06 2026-09-10 Max Engel Handhelds keep their evidence ...
git show "HEAD:$R" | $G -c ''; git show "HEAD:$R" | sed -n '1,2p;29,35p'   # 38; the From:/Subject: and the node
git -C "$U" merge-base --is-ancestor cbf75c0b06 651150fc88 && echo in-upstream || echo not-in-upstream   # not-in-upstream
git -C "$U" ls-tree -r --name-only 651150fc88 projects/ROCKNIX/devices/H700/patches/linux | $G -c -i ramoops   # 0 (R1 C11)
git -C "$U" show 651150fc88:projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf | $G -n -E 'CONFIG_PSTORE_RAM'   # `# CONFIG_PSTORE_RAM is not set` (R2 command 8)
git show HEAD:projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf | $G -n -E '^CONFIG_(PSTORE_RAM|PSTORE_CONSOLE|WATCHDOG_SYSFS|SOFTLOCKUP_DETECTOR|DETECT_HUNG_TASK|DEFAULT_HUNG_TASK_TIMEOUT)='   # the six lines of cbf75c0b06 in T27's conf (R2 command 8: :7290, :7292 among them)
# the SM8550 configuration (rulings (d), (j)): the four conf-diff counts, each naming its side
C=projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf
git show "HEAD:$C" | sed -n 3p                                                # `# Linux/arm64 7.2.0 Kernel Configuration` (R2 § 0)
git diff --numstat c445081a59 HEAD -- "$C" | $G -c ''                        # 0: the fork never changed it (R2 command 9)
git -C "$U" diff --numstat 2174265e9c 651150fc88 -- "$C"                  # `7	7	...` (R2 command 9; T28 02:78-90)
git -C "$U" diff 2174265e9c 651150fc88 -- "$C" | $G -E '^[-+]CONFIG|^[-+]# CONFIG' | cut -c1-100   # the 14 lines (R2 command 11)
diff <(git show "HEAD:$C" | sort) <(git show HEAD:projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf | sort) | $G -c '^[<>]'   # (a) against H700's conf, same 7.2 and arch [unverified]
tar -xJf "$S/linux/linux-7.2.tar.xz" -C "$T/src" linux-7.2/arch/arm64/configs/defconfig; rc=$?
echo "defconfig extract rc=$rc"
diff <(git show "HEAD:$C" | $G -v '^#' | sort) <($G -v '^#' "$T/src/linux-7.2/arch/arm64/configs/defconfig" | sort) | $G -c '^[<>]'   # (b) against the kernel's own arm64 defconfig [unverified]
git show HEAD:projects/ROCKNIX/packages/linux/package.mk | sed -n '146,335p' | $G -o -E 'CONFIG_[A-Z0-9_]+' | sort -u > "$T/tmp/forced.txt"; $G -c '' "$T/tmp/forced.txt"   # (c) the symbols pre_make_target sets or disables (R3 § 1.1) [unverified count]
while IFS= read -r k; do printf '%s %s\n' "$k" "$(git show "HEAD:$C" | $G -c -E "^(# )?$k[= ]")"; done < "$T/tmp/forced.txt"   # whether the conf already names each
git -C "$U" show 651150fc88:$C | sed -n 3p                                # (d) upstream's header line, the same 7.2.0 [unverified]
# the tarballs (ruling (g)): each hash against its .sha256 and the recipe's PKG_SHA256 as text
for v in 7.2 7.1.2; do a=$(cut -c1-64 "$S/linux/linux-$v.tar.xz.sha256"); b=$(sha256sum "$S/linux/linux-$v.tar.xz" | cut -c1-64); [ "$a" = "$b" ] && echo "linux-$v.tar.xz = its .sha256 ($(printf '%.16s' "$a"))" || echo "linux-$v.tar.xz MISMATCH"; done   # f9fef3d14c0df538 and 37198c93727be247, the recipe's PKG_SHA256 prefixes (v1 read)
git show HEAD:projects/ROCKNIX/packages/linux/package.mk | $G -n -E '^\s*PKG_SHA256=' | cut -c1-60   # :31 f9fef3d1..., :38 37198c93... among the five
ls "$S/u-boot-DDR3" "$S/u-boot-DDR4" "$S/kernel-firmware"                     # u-boot-DDR3-v2026.01.tar.gz, u-boot-DDR4-v2026.01.tar.gz, kernel-firmware-20260309.tar.gz with .sha256 and .url (v1 read); the non-kernel rows' sources, L-12
# the removal rule's own check (ruling (c); D-WORKFLOW-209): expect no line at any stage
git diff --stat __COHASH__ HEAD -- '*.patch' '*.conf' packages projects tools scripts | tail -n 1
git log --no-merges --format=%h __COHASH__..HEAD -- '*.patch' '*.conf' packages projects tools scripts | $G -c ''   # 0
# the registers take the procedure's appends only: expect 0 removed lines
git diff __COHASH__ HEAD -- docs/decision-register.md docs/blindspot-register.md docs/friction-log.md | $G -c -E '^-([^-]|$)'
# the checkers' baseline at the dispatch tip (their lines move with the dispatch's own commits, so each line that prints is recorded beside the research's)
tools/rules-check > "$T/tmp/rules-check.out" 2>&1; rc=$?
echo "rules-check rc=$rc"; tail -n 1 "$T/tmp/rules-check.out"               # rc=0 (T39's R3 C13: 30 rule files) -- no evidence for the 107
tools/register-check > "$T/tmp/register-check.out" 2>&1; rc=$?
echo "register-check rc=$rc"; tail -n 1 "$T/tmp/register-check.out"         # rc=0; `register-check: 715 IDs, each once; ...` at 6a12ce2d73 (v1 read); the dispatch's own row moves the count
tools/work-log-index --check > "$T/tmp/index.out" 2>&1; rc=$?
echo "work-log-index rc=$rc"; tail -n 1 "$T/tmp/index.out"
tools/ceremony-check > "$T/tmp/ceremony-check.out" 2>&1; rc=$?
echo "ceremony-check rc=$rc"; tail -n 1 "$T/tmp/ceremony-check.out"         # `nothing overdue.` rc 0 at 6a12ce2d73 (R5 § I); the dispatch tip's line is the record
tools/box-check > "$T/tmp/box-check.out" 2>&1; rc=$?
echo "box-check rc=$rc"; tail -n 1 "$T/tmp/box-check.out"                   # R5 § I: `300 issue(s), 695 open checkbox(es), 0 fail` at the research's read [unverified at the tip]
.githooks/hooks-test > "$T/tmp/hooks-test.out" 2>&1; rc=$?
echo "hooks-test rc=$rc"; tail -n 1 "$T/tmp/hooks-test.out"                 # [unverified]: no research file for this brief ran it
# the issues read at stage A (states recorded; a quoted line through the mask)
gh --repo pixelelated/distribution issue view 688 --json title,state,body --jq '.title, .state, (.body | split("\n") | length)'   # the title, OPEN, and the body's line count after the coordinator's fill (27 before it, R5 C14)
for n in 328 369 104 44 1056 1049 1086 1084 563 559 585; do printf '#%s %s\n' "$n" "$(gh --repo pixelelated/distribution issue view "$n" --json state,title --jq '.state + " " + .title' | cut -c1-110)"; done
```

**The applies-at-pin run (stage B; ruling (g))** -- the one proof a build
would otherwise give, made from bytes already on the host. Per plan the lane
collects the files its patches touch, extracts those members alone from the
pinned tarball into `/workspace/tmp/m6-t41/src/<DEVICE>/`, and runs `patch
-p1 --dry-run` in `unpack`'s order; after each dry-run the patch is applied
into the scratch so the next meets the tree the build would give it (SM8550's
`0060-...synaptics-dsx-driver` then `-kconfig`, `1000-add-qcom-haptics-driver`
then `1002`/`1003`/`1005`; the `7.2/` directory before the device directory,
R3 § 1.4). **A hunk that fails is a lead, not a fix**; a file the patch creates
is absent from the archive, so `tar` exits 2 naming it and the lane records
the names (not a failure). The cell vocabulary is closed: `applies`, `applies
with offset`, `fuzz`, `fails`, `open item`.

```bash
export LC_ALL=C; G=/usr/bin/grep; T=/workspace/tmp/m6-t41; S=/workspace/cache/rocknix-sources
for plan in GENERIC_X64:7.1.2 H700:7.2 SM8550:7.2; do dev=${plan%:*}; v=${plan#*:}
  while IFS= read -r p; do git show "HEAD:$p" | $G -E '^(\+\+\+ b/|--- a/)' | sed -E 's#^(\+\+\+ b/|--- a/)##; s#[[:space:]].*$##'; done < "$T/order-$dev.txt" | $G -v -F '/dev/null' | sort -u | sed "s#^#linux-$v/#" > "$T/targets-$dev.txt"
  echo "$dev targets: $($G -c '' "$T/targets-$dev.txt")"
  mkdir -p "$T/src/$dev"; tar -xJf "$S/linux/linux-$v.tar.xz" -C "$T/src/$dev" -T "$T/targets-$dev.txt" 2> "$T/tmp/tar-$dev.err"; rc=$?
  echo "tar $dev rc=$rc not-in-archive=$($G -c 'Not found in archive' "$T/tmp/tar-$dev.err")"   # rc 2 names the files the patches create; recorded
  i=0; : > "$T/applies-$dev.txt"
  while IFS= read -r p; do i=$((i+1)); git show "HEAD:$p" > "$T/tmp/cur.patch"
    patch -p1 --dry-run -N -d "$T/src/$dev/linux-$v" < "$T/tmp/cur.patch" > "$T/tmp/dry.out" 2>&1; rc=$?
    printf '%s %03d %s rc=%s offset=%s fuzz=%s FAILED=%s\n' "$dev" "$i" "$p" "$rc" "$($G -c 'offset' "$T/tmp/dry.out")" "$($G -c 'fuzz' "$T/tmp/dry.out")" "$($G -c 'FAILED' "$T/tmp/dry.out")" >> "$T/applies-$dev.txt"
    [ "$rc" -eq 0 ] && patch -p1 -N -s -d "$T/src/$dev/linux-$v" < "$T/tmp/cur.patch" > /dev/null 2>&1   # the series advances in the scratch only
  done < "$T/order-$dev.txt"
  awk '{print $4}' "$T/applies-$dev.txt" | sort | uniq -c                    # the rc counts per plan; every `rc=0` line is `applies`, `applies with offset` or `fuzz` by its counts, every other `fails`
done
# the non-kernel five by the same method [proposed]: ruling (g) names the kernel tarballs; the coordinator confirms at dispatch, or the five cells read `open item` with the build named
tar -tzf "$S/u-boot-DDR3/u-boot-DDR3-v2026.01.tar.gz" | head -n 1            # u-boot-2026.01/ (v1 read)
tar -tzf "$S/kernel-firmware/kernel-firmware-20260309.tar.gz" | head -n 1    # linux-firmware-20260309/ (v1 read)
```

**The table's generator** is the lane's, **`tools/t41-tables.py`** in the
audit folder, cut from T40's `tools/t40-tables.py` (ruling (j); read at
`e863379cec`, never checked out). It reads only what stage A saved under
`/workspace/tmp/m6-t41/stage-a-p1/` (the block's TSV: the 107 with every
inventory column) and under `$T/` (`order-<DEVICE>.txt`, `applies-<DEVICE>.txt`,
`targets-<DEVICE>.txt`), and every patch's bytes by `git show HEAD:<path>`;
it changes nothing in the tree. **Its asserts are the FAIL-first positive**:
`107` rows and `40,474` lines, `106` `.patch` and `1` `.conf`, `103` shipped
and `4` test, the nine directories' counts (`4 6 4 32 55 1 2 2 1`), the seven
`reachable_by` groups' sizes (4, 32, 56, 1, 4, 6, 4) summing to `107`, the header census (`From:` 87,
`Subject:` 89), the application order's three totals (`8`, `42`, `65`), and
the dispositions' sum equal to the row count -- *so a missing row fails there
instead of printing an empty cell* (T40's `:8-9`). Before the tip run, the
generator is run on a mutated scratch copy of the TSV (one member row
dropped; one row's `reach` changed; one patch's `From:` line stripped in a
scratch copy read by `--bytes-from <dir>`) and **must exit non-zero naming the
assert**; the three exits and the tip run's `stats` line are quoted in `02`
§ The runs and in `00` with *a FAIL would mean ...*. Its modes are T40's
(`stats | provenance | coverage | json`), `shadowed` dropped (no shadowed
rows here) and **`currency` added** (the per-directory upstream table). **The
columns**, T40's first seven kept (path, lines, kind -- `patch`, `conf`, or
`non-kernel` for the five --, the directory, `reachable_by` as the plans, the
header's origin and subject with tag and series position, the first target,
the Files/hunks cell) and T41's added (R5 § A `[proposed]`, confirmed by the
rulings):

| Column | What fills it, and from what | Closed vocabulary |
| --- | --- | --- |
| **target version** | the header's `From <sha> Mon Sep 17 ...` line and `[PATCH vN i/M]` position; the kernel tag named in the body or the series' cover; the file name's date (`v8_20260804_...`, `20260424_...`, `v6_20260210_...`) | a tag, a sha, a date, `hand-made`, `unknown` |
| **current pin** | per `reachable_by` device, the recipe's `case` branch read as text at the tip: `7.2` for H700 and SM8550, `7.1.2` for GENERIC_X64, with the `PKG_SHA256` prefix beside it; `v2026.01` and `20260309` for the non-kernel five | the pin string |
| **applies-at-pin** | the `applies-<DEVICE>.txt` line for the row, per plan (ruling (g)) | `applies`, `applies with offset`, `fuzz`, `fails`, `open item` |
| **upstream status** | the blob at `651150fc88` (`SAME` / `CHANGED` / `ABSENT`) and the header's own claim (`Link:`, `Upstream-Status:`, a cherry-pick line), **recorded as the patch's claim, never verified against kernel.org (no network)** | `carried`, `changed upstream`, `moved upstream`, `claims mainline <tag or link>`, `fork-written`, `unknown` |
| **backport status** | from the two above and the tarball grep (L-06): a claimed mainline change present in the pinned source is `superseded at this pin` (a lead to T11, never a removal); above the pin `a backport`; no claim `unknown` | `superseded at this pin`, `a backport`, `unknown` |
| **the fork's reason** | the header's own sentence plus the adding commit at ROCKNIX, `git log --follow --diff-filter=A --format='%h %an %cs %s' HEAD -- <path>` (`cbf75c0b06` for the one fork-written; `unknown` where the history and the content say nothing, ruling (k)) | the commit and one sentence, or `unknown` |
| **disposition** | one of § 6's set | `keep`, `superseded at this pin`, `upstream-changed`, `upstream-moved`, `#585`, `bug`, `open item` |

For the one `.conf` row the generator prints the **four conf-diff counts, each
naming its side** (ruling (j); § 5's runs (a) to (d)): against H700's
`linux.aarch64.conf`, against `linux-7.2/arch/arm64/configs/defconfig`
extracted alone from the tarball, against the symbols the recipe's
`pre_make_target` forces or disables, and against `651150fc88`'s copy
(`7 7`). **Secret-pattern hygiene**: `02` quotes 107 patch names and the
inventory's own note (`:633-635`, R3 § 4.7) says a name shaped like
`ma-sk-...` once read as an API key to the guard, so before committing the
lane runs `.githooks/secret-patterns`' regex over `02` in the hooks' form
(sourced in a subshell, counts only, the runtime-built positive first) and
`tools/forbidden-terms-check --stdin < 02-forward-audit.md` (rc 0 beside the
planted positive's rc 1, § 7).

## 6. Outputs

As T40's § 6, scaled for a table slice at Local depth: no packet, no seat, no
guest, no compile (R5 § A); § 7 is this section as checkboxes. All in the
worktree, committed on its branch with messages that cite `#688` (`Refs
#688` while any criterion is open, never a closing keyword). The folder
**`docs/audits/<yyyy_mm_dd>-epic-m6-patches-shipped-kernel/`** (#688's
audit-folder line; T40's date form, `2026_10_25-...`). **The two dispositions
sets, fixed here:** a § Provenance row takes one of `keep`, `superseded at
this pin`, `upstream-changed`, `upstream-moved`, `#585`, `bug`, `open item`;
a § 3 lead takes one of `row`, `bug`, `#585`, `inherited:<owner>`, `none`,
where `<owner>` is `coordinator`, `T11`, `T27`, `T28`, `T42`, `T43` or `the
integration`.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `.../00-running-log.md` | opened first: the model and effort that ran, the session, `reviewed-at` (the dispatch tip `__COHASH__`) with `2174265e9c` and `651150fc88` beside it, every command with its exit status and time; **every check that stands as a proof announced on a line that begins `PROOF:`**; the lint's Local proof (ruling (i)) before anything else; the generator's FAIL-first exits; its closing census says no build, no `scripts/unpack`, no `kconfig-*`, no `adjust_kernel_config`, no compiler, no guest, no fetch, no council or keyed call, no held directory, and names the scratch's path (`/workspace/tmp/m6-t41/`) and its retirement at stage H (D-INFRA-022) | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: § 2's block with its sha256 prefix checked and its 99 lines at P1 and at the tip, both line figures with the unterminated file named, the tool's row, the nine directories' counts, the three plans' orders and totals, the header census, the byte-identity lines against `c445081a59` and `651150fc88`, the `.patch.disabled` and symlink sentences; § The rules read; § The take-up table of § 2 with each row's state | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #688's checklist, in this order: **§ Provenance** (107 rows, the path in backticks as the first cell, § 5's columns; generated, asserted); **§ Coverage** (107 rows: path, lines, kind, reach, disposition; generated, asserted); **§ The ramoops patch** (the one line-by-line read, L-16, with its `#585` line's text); **§ The conf** (the four counts and the method column, L-19, L-29); **§ Upstream since the base** (the 12 additions, the 1 move, the 4 changes, the `rocknix-joypad` line, each *the integration carries*; generated by the `currency` mode); **§ The non-kernel five** (ruling (b)); **§ The #585 lines owed** (the ramoops patch's; the `=~` one-liner's; never sent); **§ The runs** (every § 5 run with exit, wall time, its figure and *a FAIL would mean ...*); **§ Proofs** with `proved:` cells; **§ What the coordinator, the integration and the next slices inherit** | B |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5's interaction audit for the seams: `unpack` x the inventory x the recipe's `case` x the device directories x upstream's merges x the two excluded confs; § 3.6 time to play: *nothing* | B |
| Analysis | `.../04-analysis.md` | Phase 4, then § Finding Verification (4.5, in full), then **§ Renovation face** Q1 to Q7 (Q4 the currency table's dispositions summing to 107; Q3 the bug(s); Q5 struck in one sentence; Q7 the two rule lines named); § Second opinion reads *not applicable at Local depth (plan § 6c)* | B, C |
| Second opinions | `.../second-opinions/review-plan.json` | depth `local`, the primary in the form T4's plan writes it, lab `anthropic`, reviewers `[]`, `tier_exception` `D-WORKFLOW-184`, `reason` plan § 6c's row; **no provenance file, no packet manifest** | C |
| Tools | `.../tools/t41-tables.py` | the generator (§ 5): asserts the counts, writes § Provenance, § Coverage and § Upstream since the base; seen to exit non-zero on the three mutations before its tables are trusted | C |
| Stages | `.../stage-a/`, `.../stage-b/` | the first commands and § 5's runs, the P1 block's `.qa-scratch/t41/` copy, `order-*.txt`, `applies-*.txt`, `targets-*.txt` and the `tar` error files under `stage-a/`; the line-by-line read's notes under `stage-b/`; **no `guest-cycle/`** | A, B |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | prints `PASS pre-issue artifacts (does not certify resolution)`; recorded in `00` | C to D |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category (`Renovation` where it is not a defect), where (`file:line` at the dispatch tip), acceptance, **the ladder stage and the tool that would hold it at the next, or *no tool can***, `Already written:`, the VM line (ruling (h)); the YAML `punch_index`; an inherited item marked with its owner (`inherit:T11`, `inherit:T27`, `inherit:the integration`, ...) | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #688 | `Audit: M6 T41 the shipped kernels' patches and configurations -- N findings (X critical, Y high)`; one checkbox per item, each agent-verifiable (D-QA-044); `tools/box-check --issue N` run on it and its line recorded | D |
| Bug issues | GitHub, label `bug`, title `Bug: ...`, milestone-less and not sub-issues (`milestone-phase-naming.md` § Reactive) | the unfixed `0010-msm-resource-cleanup.patch` (L-01: the code trace from `9416eec2c2`'s message and the two diffs; `Already written:` the pre-fix bytes in every image since the base, the fix the base merge's; *Can this be done on the VM? No -- the tree and the history show it*; the criterion: `git -C <repo> diff --stat <fixed-at> upstream/next -- <the two>` empty after the base merge lands), and one per patch a shipped image should apply and does not (`fails` in `applies-<DEVICE>.txt`), if any | D |
| **The stage-D pause** | #688 | the punch list posted with the audit issue's and the bugs' numbers and § 4's two questions; **the lane waits**; a stage E exists only if the coordinator names a stream (none expected: a table slice, ruling (c)) | D |
| Verification | `02` appended; `.../audit-completion.json` | every claim proven where the tree, a tool or the register can show it; every proof's `proved:` cell one of `tree`, `history`, `tool-run`, `fixture`, `design` (T40's five); the Phase 7 gate in `05` | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-patches-shipped-kernel.md`, and the same text as a comment on #688 | T40's retro's shape (its headings on its branch, R5 C15): `**Completed:**`, `**Scope of this retro:**`, `**Commits:** reviewed-at ... fixed-at ...`, `## What the slice did to the two time-to-play numbers` (*Nothing, on either number*, in those words), `## What T42, T43, T27, T11 and the integration inherit`, the four answers, `## Adjustments, Instruction-Recommendations mode`, `## Scoped audit` | G |
| Hand-back | #688 | `reviewed-at:` and `fixed-at:` written into #688's body by the executor; one comment naming **the one tip** and each artifact by path, the checkers' exit codes | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md` | seeded by the coordinator; the executor updates it at every checkpoint (#1014) | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session, headed `#688` and the thing decided or learned | every session |

Neither `tools/renovation-status`, `tools/renovation-drift` nor
`tools/renovation-inventory` is run to write a ledger or edited here; a defect
in one is a lead on #688.

## 7. Acceptance

The checklist on #688 becomes this section at dispatch, written there by the
coordinator in place of the five generated ones (T40's § 7; T39's ruling
(i)). Its first five items are plan § 6b's contract for every slice, adapted
as T38's, T39's and T40's were; the rest are this slice's (D-WORKFLOW-189).
Every checkbox names the artifact that ticks it (D-QA-044); the coordinator
ticks at acceptance, from the artifacts, never from the hand-back's words;
where this section and #688 differ, #688 wins and the coordinator corrects the
brief.

- [ ] `docs/audits/<date>-epic-m6-patches-shipped-kernel/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `second-opinions/`, `stage-a/`, `stage-b/` and `tools/`, and no `guest-cycle/` (`ls` of the folder in the hand-back).
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-patches-shipped-kernel/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`), and the same with `--issue <audit issue>` prints `PASS`; Q1 to Q7 are headed in `04-analysis.md` (Q5 struck in one sentence) and every punch item carries `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: local`, the primary in the form T4's plan at `6ec78bbf8c` writes it, lab `anthropic`, reviewers `[]`, `tier_exception: D-WORKFLOW-184` and plan § 6c's row as the reason; `ls second-opinions/` lists that file alone; `00`'s closing census shows no `tools/council/run`, no Facilitator, no `npm install` and no keyed call.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, #585, #563, #559, #1056, #346 or a Backlog the coordinator files), withdrawn, or recorded as a design with its sentence; `tools/box-check --issue <audit issue>` prints 0 fail; the issue is closed by the coordinator at acceptance.
- [ ] `reviewed-at:` and `fixed-at:` in #688's header carry the lane's commits and no `-es` pair; `git diff --stat __COHASH__ <fixed-at> -- '*.patch' '*.conf' packages projects tools scripts | tail -n 1` prints nothing, `git log --no-merges --format=%h __COHASH__..<fixed-at> -- '*.patch' '*.conf' packages projects tools scripts | /usr/bin/grep -c ''` prints `0`, and the registers' removed-line count prints `0` (ruling (c); D-WORKFLOW-209).
- [ ] `01-research-notes.md` § Scope records § 2's membership block, its sha256 prefix `4d300124a6bf116f` checked (148 lines), with its 99 expected lines at the P1 hash byte for byte (`diff` empty) -- among them `mine: 107 paths.txt: 107 equal: True`; `lines: 40474 reach: {'shipped': 103, 'test': 4} tier: {'vendor-carried': 107}`; `lang: {'patch': 106, 'kernel-config': 1} area: {'patches-and-configs': 107}`; the two `TREE-SIDE` lines with `derived: 107 equal to mine: True`; `GROUPS TOTAL 107 40474 groups 9`; `wc -l, the text rows at the P1 hash: 40473`; `grep -c, the text rows at the P1 hash: 40474`; `present at the merge base: 106`; `blob vs merge base: SAME 106` and `ADDED 1`; `MB..P1: 1 file changed, 38 insertions(+)` -- and the tip re-run's lines beside them (`the same lines at the tip`, or each differing line as a recorded delta), with the one unterminated file named beside both totals (ruling (a)).
- [ ] `00` records, at stage A and before any other check, the lint's `PASS` on a Local plan (T4's exported folder, `t4 plan: local D-WORKFLOW-184 0`, `rc=0`) and its FAIL on the same plan with `tier_exception` removed (`rc=1`, the FAIL line quoted) -- ruling (i) -- or the lines that printed and the question raised on #688 before stage C.
- [ ] `02-forward-audit.md` § Provenance carries exactly one row per path under its own `## Provenance` heading, the path in backticks as the first cell: ``awk '/^## Provenance/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `107`; each row carries § 5's columns -- target version, the current pin per applying plan (one of `7.2`, `7.1.2`, `v2026.01`, `20260309`), applies-at-pin, upstream status, backport status, the fork's reason -- with every cell non-empty (`unknown` and `open item` are values), the five `non-kernel` rows labelled so in the kind column with their recipe's owner, and a disposition from § 6's set; `t41-tables.py`'s `stats` line prints the dispositions' counts and their total `107`.
- [ ] `02` carries a coverage table with exactly one row per path under its own `## Coverage` heading: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `107`, and the paths equal `.qa-scratch/t41/paths.txt`'s (`diff` of the sorted first cells against it is empty).
- [ ] The applies-at-pin column is filled for every `.patch` row with its command's line: `02` § The runs quotes, per plan, the `tar` line (its `rc` and `not-in-archive` count), the `applies-<DEVICE>.txt` summary (`uniq -c` of the `rc=` values over `8`, `42` and `65` lines for GENERIC_X64, H700 and SM8550), and every non-`rc=0` line in full; a `fails` row is a `bug` or a `02` lead with its hunk quoted; the four U-Boot rows and the firmware row read their result by the same method or `open item` with the reason (ruling (g); `## Version 1` item 7).
- [ ] `00` records the generator's FAIL-first before its tip run: the three mutated-copy runs each exiting non-zero with the assert's message quoted (one row dropped; one `reach` changed; one `From:` stripped), then the tip run's `stats` line (`rows 107 lines 40474`, `patch 106 conf 1`, the nine directory counts, `From: 87 Subject: 89`, the three order totals `8 42 65`, the dispositions summing to `107`) with *a FAIL would mean ...* beside each.
- [ ] `02` § The ramoops patch quotes the patch's `:29-35` node and names D-SYS-004's three numbers against it (`0x4f000000` / `0x100000`, `0x80000`, `0x20000`), the six `CONFIG_` lines of `cbf75c0b06` in H700's `linux.aarch64.conf` with their line numbers, `not-in-upstream` and `0` ramoops-named files at `651150fc88`, the tarball grep's context lines at or near `:117` of `sun50i-h616.dtsi` with no `ramoops` node, and its `#585` line under `## The #585 lines owed` with the layer stated as § 4 question 2 (ruling (e); `/usr/bin/grep -c '#585' 02-forward-audit.md` is at least `2`: this line and the `=~` one-liner's).
- [ ] `02` § The #585 lines owed carries the `=~` one-liner for `651150fc88:projects/ROCKNIX/packages/linux/package.mk:18` with the five-name test's `no-match` lines quoted (L-02), and the sentence *never sent* beside both lines (D-WORKFLOW-164, -165).
- [ ] The unfixed `0010-msm-resource-cleanup.patch` is a § Provenance row disposed `upstream-changed` in both `7.0/` and `7.2/` and a `bug` filed with its trace (`9416eec2c2`'s message, the `--stat` of the two copies against `651150fc88`), its `Already written:` line, its VM line (ruling (h)) and a criterion naming the base merge (`git diff --stat <fixed-at> upstream/next -- <the two>` empty once it lands); the bug passes `tools/box-check --issue N` with 0 fail (ruling (c)).
- [ ] `02` § The conf carries the four conf-diff counts each naming its side -- against H700's `linux.aarch64.conf`, against `linux-7.2/arch/arm64/configs/defconfig` (the `tar` extract line's `rc=0` quoted), against the recipe's forced or disabled symbols (the count of `forced.txt` and the per-symbol lines), against `651150fc88` (`7 7`) -- the header line `# Linux/arm64 7.2.0 Kernel Configuration`, `0` numstat lines against `c445081a59`, and the method column naming `kernel_config_path`'s candidates, the `oldconfig` step and the two writers never run (rulings (d), (j)).
- [ ] `02` § Upstream since the base lists the 12 additions, the 1 move and the 4 changes under the shipped kernel directories as `git -C /workspace/repos/pixelelated/distribution diff --name-status c445081a59 651150fc88 -- <the four directories>` prints them (`12 A`, `1 D`, `4 M`), each line disposed *the integration carries* (#563/#559 named, nothing applied), and the byte-identity summary against `651150fc88` reading `101 SAME`, `4 CHANGED`, `2 ABSENT` (or the lines that printed, as deltas).
- [ ] `02` § The runs records, each as a command's own output line with its exit: the tool's `--order` row with `git status --short --ignored` counts before and after; the recipe's pin and patch-directory lines by number; the three devices' `options` lines; `unpack:127-159`; the nine directories' counts and the seven `absent` directories; the header census; the two byte-identity summaries; the fork's commit lines (`cbf75c0b06` the one non-merge on the 107; `dc948f59aa` and `3d7c075f63` on the recipes; ` 2 files changed, 5 insertions(+), 5 deletions(-)`); the churn count; the five `identical` lines; the symlink entries and their targets; the two tarball hash lines (`= its .sha256`) with the recipe's `PKG_SHA256` lines beside them; the checkers' lines (`rules-check`, `register-check`, `work-log-index --check`, `ceremony-check`, `box-check`, `.githooks/hooks-test`); the secret scan in the hooks' form (compile rc at most 1, the runtime-built positive `1`, then `0` files) and `tools/forbidden-terms-check --stdin` over `02` (`rc=0`) beside the planted positive through `FORBIDDEN_PATTERNS` (`rc=1`, its line quoted) -- a check without its positive is recorded as such.
- [ ] Every lead of § 3 appears in `02` as a row, a `#585` line, a bug or an inherited item with its owner: ``/usr/bin/grep -o -w -E 'L-[0-9]{2}' 02-forward-audit.md | sort -u | /usr/bin/grep -c ''`` prints `31`; the § 1 rulings (a) to (p) each have their `02` row.
- [ ] `04-analysis.md` § Renovation face Q4 carries the currency columns' counts by value (the generator's lines: target versions by kind, pins by plan, applies-at-pin by vocabulary, upstream status by value, backport status by value, dispositions summing to `107`); Q3 the bug(s) by number; Q5 the struck sentence; Q7 the two rule lines (`packaging-and-patches.md:91`, `CLAUDE.md:148-149`) named as the coordinator's erratum; and the two time-to-play numbers named as untouched.
- [ ] § 4's two questions are written in `04` in the shape § 4 gives and posted as comments on #688 at the stage-D pause, and `02`'s row for each cites its comment's id, which `gh api repos/pixelelated/distribution/issues/comments/<id> --jq .body` reads back.
- [ ] `02` § What the coordinator, the integration and the next slices inherit lists every inherited lead of § 3 with its owner -- T27 (L-12's recipes and #44, L-14's joypad consumers, L-25's L15, L-27's H700 conf, the two `.patch.disabled`), T11 (L-03, L-07, L-08, L-15, L-27's GENERIC_X64 conf, L-28's recipe, every `superseded at this pin` row), T11 (the firmware recipe of the five `non-kernel` rows; version 2's ruling), T43 (`7.2.6/`, `mainline-rockchip/`, the twelve unshipped confs), the integration (#563/#559: L-01's fix, L-14, L-19, L-20's `0017`, L-22's 12 additions, L-02's upstream line until it is sent), the coordinator (L-09's rule erratum, L-17's tier reading, L-21's order wording, #1056 and the reach gaps of L-18) -- each at its `file:line`, and the `#585` lines owed, never sent.
- [ ] Every bug states its trace, its `Already written:` line and its VM line and passes `tools/box-check --issue N`; every punch item carries the ladder stage and the tool that would hold it at the next, or *no tool can*; every row of § 2's take-up table has a disposition at its lines.
- [ ] Every proof in `02` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture` or `design`; ``/usr/bin/grep -c 'proved:' 02-forward-audit.md`` equals ``/usr/bin/grep -c '^PROOF:' 00-running-log.md``.
- [ ] **The host file carries no line of this lane's**: `/usr/bin/grep -c -E 'T41|#688'` over the lines `/workspace/tmp/m7-m6-host-coordination.txt` gained between the dispatch comment's recorded line count (`__HOSTLINES__`) and the hand-back prints `0` -- no START, no RETURN and no compile START (ruling (h); a table slice compiles nothing; a compile START here is a stop, § 10).
- [ ] `00`'s closing census names no `scripts/unpack`, `adjust_kernel_config`, `check_kernel_config`, `kconfig-`, `make `, `kernel_make` or `config/options` invocation, no `tar -x` outside `/workspace/tmp/m6-t41/`, no `git fetch`, no guest, no compiler, and names the scratch's retirement at stage H with its path (ruling (g); D-INFRA-022): `/usr/bin/grep -c -E 'scripts/unpack|adjust_kernel_config|check_kernel_config|kconfig-|kernel_make|git fetch' 00-running-log.md`, over the command lines it logs rather than the sentences that forbid them, prints `0`.
- [ ] The retro exists at `docs/retros/<date>-m6-patches-shipped-kernel.md`, is posted on #688 with its heading's time from `date -u` in the posting command, and says what the slice did to the two time-to-play numbers (nothing, in those words) and what T42, T43, T27, T11 and the integration inherit.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the slice branch before the hand-back merge, and again on the coordinator's simulated merge; `tools/lint-audit-artifacts` prints `PASS` on the folder; the six exit codes pasted on #688.
- [ ] The hand-back is one comment on #688 naming **one tip** and each artifact by path, with `reviewed-at:` and `fixed-at:` only in #688's header; every inherited item is a row of `02` naming its owner; and `tools/box-check --issue 688` prints 0 fail.

## 8. What the coordinator, the integration and the next slices inherit

Written, not done here; `02` § What the coordinator, the integration and the
next slices inherit carries each item as a row with its lines and its owner,
and the hand-back names them (§ 7). No pin, no image, no patch and no other
lane's branch is moved by this slice, so the list holds no integration step
of its own; T41's branch merges in the coordinator's turn, its place named by
the coordinator at acceptance.

1. **T27 `device-h700`** (#674): the two U-Boot recipes whose patches are
   T41's `non-kernel` rows (L-12; the DDR3/DDR4 split is one
   `PKG_UBOOT_CONFIG`, #44 under D-WORKFLOW-033); the H700 configuration with
   the ramoops patch's six config lines (L-27; the companion of L-16); whether
   `0140-rg35xx-2024-use-rocknix-joypad-driver.patch` and the joypad driver
   still need `input-polldev` after the base merge (L-14); `0154`'s L15 open
   item (L-25); the `0203-...patch.disabled` (L-10).
2. **T11 `device-generic-x64-and-kernel`** (#658): the kernel recipe's lines
   -- the duplicated `7.0/` triple and § 4 question 1 (L-03), the
   `kernel_options` soft guard (L-08), the `PKG_PATCH_DIRS` words that select
   nothing (L-15), the `qcom-abl` branch upstream's BLS change reaches (L-28,
   #1099), the two fork hunks to carry across the base merge (`GENERIC_X64` in
   the version case, the hostname); the GENERIC_X64 configuration (L-07,
   L-27; #1084); **every `superseded at this pin` row the table turns up** (a
   drop lead to the kernel's owner, never a removal here, D-WORKFLOW-209).
3. **T42 `patches-shipped`** (#689): the `kernel-firmware` recipe behind the
   firmware row (ruling (b)); the 50 shadowed rows T40 handed it, none T41's.
4. **T43 `patches-unshipped`** (#690): upstream's `7.2.6/` for
   `RK3566|RK3576|S922X` (L-22), the override's `mainline-rockchip/`, the
   twelve unshipped configurations, RK3326's new `003-input-add-input-polldev-driver.patch`
   (L-14).
5. **The integration** (#563's base merge; #559's backport procedure): the
   `0010` fix (L-01), the moved polldev patch (L-14), the SM8550
   configuration's 14 lines (L-19), the `0104` line, the six new `7.2/` and
   two new SM8550 patches (L-22), upstream's `0017` beside #328 (L-20), the
   `rocknix-joypad` directory for H700 (L-02, L-14) -- each named in `02` as
   *the integration carries*, none applied by this lane (ruling (f)).
6. **The coordinator** (D-WORKFLOW-189): the rule erratum of
   `packaging-and-patches.md:91` and `CLAUDE.md:148-149` (L-09; T4's rules,
   #651); the tier reading that hides the one fork-written row (L-17; a
   tooling finding to file beside #1049, #1056, #1086, or not); the order's
   title against the globs (L-21); the kickoff addendum's *Adjustments*; the
   two maintainer questions of § 4, put by the coordinator.
7. **#585** (the contribution queue): the ramoops patch's line (L-16; its
   layer § 4 question 2; #369 parked) and the `=~` one-liner for ROCKNIX
   (L-02) -- each in the shape the lane writes, **never sent**
   (D-WORKFLOW-164, -165).
8. **#328**: the `0002` row's cross-reference and upstream's `0017` (L-20);
   nothing diagnosed. **#1056** and the reach gaps: the check that none moves a
   row (L-18, L-23).

## 9. The register and the ceremonies

**The register** (`docs/decision-register.md` at `6a12ce2d73`: 799 lines,
`## Open decisions` at `:782`, `v1 read`; R4 § 3's lines; R5 § F). Each row is
read before it is cited (R5 § B item 8):

| Row | Line | What it binds here |
| --- | ---: | --- |
| **D-SYS-004**; D-SYS-001, -002, -003, -005 | `:164`; `:161`, `:162`, `:163`, `:165` | ramoops 1 MiB at `0x4F000000` from the SoC dtsi, *"Not something mainline would take in a SoC dtsi; the fork carries it"*, the DRAM fact a device test with a yes (L-16); persistent `/var/log`; the watchdog at 15 s; the hang sysctls; `rocknix-evidence` (R4 item 7) |
| D-SYS-006 (open) | `:792` | a userspace watchdog; not a kernel row |
| D-QA-023, D-QA-028 | `:253`, `:328` | SM8550 built after H700 from the same `next`; the Nova under upstream's 20260901 (R4 item 26; #328) |
| D-WORKFLOW-033 | `:366` | #44 (DDR3 or DDR4) waits until after the release candidate (L-12) |
| D-WORKFLOW-123 | read at `__COHASH__` | the `"ROCKNIX"` hostname kept across the display rename (the recipe hunk `3d7c075f63`, ruling (c)) |
| D-WORKFLOW-162 | `:690` | upstream checked early: the check date, links, affected and fixed versions recorded (L-01, L-20) |
| D-WORKFLOW-164, -165 | `:698`, `:700` | contributions considered and queued in #585, never sent before the initial build (L-02, L-16) |
| D-WORKFLOW-184 | `:719` | Local for a provenance table (ruling (i)) |
| D-WORKFLOW-185 | `:720` | the shipped set H700 and SM8550; GENERIC_X64 the test image; every other target a row in the unshipped tables (the reach the membership rests on) |
| D-WORKFLOW-187 | `:722` | the renovation gates no release; the VM line (ruling (h)); the drift re-review at close (#1054 criterion 3) |
| D-WORKFLOW-188 | `:723` | the order: every path in exactly one slice (`unassigned: 0`, `ambiguous: 0`) |
| D-WORKFLOW-189 | `:724` | planning and work items the coordinator's |
| D-WORKFLOW-198 | `:732` | a modify/delete at the base merge is a read when the fork never edited the file (L-14's polldev patch) |
| D-WORKFLOW-209 | `:747` | a table removes nothing and edits no recipe (ruling (c)) |
| D-WORKFLOW-217, -218, **-219**; **-220** | `:778`, `:779`, `:780`; `:781` at `2d3c57a625` | T37's and T38's ownership rows; T38's stage-D dispositions, the last decided row at `6a12ce2d73` (R5 § F); **T39's ownership row, written at its dispatch (2026-11-01 06:22)** -- the row that takes 220 (`v1 read`) |
| D-WORKFLOW-050, -215 | read at `__COHASH__` | every bug's `Already written:` line; the hold test (none expected here) |
| D-CLOUD-068 | read at `__COHASH__` | the cloud device id seeded from a hardware address (L-11's cross-reference) |
| D-QA-008 | read at `__COHASH__` | a deliberate crash of a handheld needs a yes by name -- never this slice's |

**The highest decided IDs per area**, read from the table above `## Open
decisions` only (`v1 read` at `6a12ce2d73`:
`awk '/^## Open decisions/{exit} /^\| D-[A-Z]+-[0-9]+ /{print $2}' docs/decision-register.md | awk -F- '{n=$3+0; if(n>m[$2]) m[$2]=n} END{for(a in m) printf "D-%s-%03d\n", a, m[a]}' | sort`):
**D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052,
D-SYS-013, D-UI-137, D-WORKFLOW-219**; `tools/register-check` printed
`register-check: 715 IDs, each once; every citation in the live documents
names a row` (`v1 read`). **At `2d3c57a625`, the tip at this draft's close,
the same awk prints `D-WORKFLOW-220`** -- T39's ownership row, written at its
dispatch (`decision-register.md:781`; 800 lines, `## Open decisions` at
`:783`; `register-check: 716 IDs`, `v1 read`). **This slice's ownership row is
D-WORKFLOW-22x** (ruling (l)): T41 takes the next free WORKFLOW ID after
T39's -- **221** unless another row lands first -- written by the coordinator
at dispatch before `## Open decisions`, its `<date>` checked on the appended line alone; the row, the body
fill and the pointer's `Register:` line are filled from the same `awk` at
`__COHASH__`, never retyped (R5 § F; T37's erratum). **The row, from R5 § F's
draft with the coordinator's rulings applied** (the five `non-kernel` rows,
the two line figures, the branch cut from the tip, the applies-at-pin method):

> | D-WORKFLOW-22x | `__DATE__` | **T41 (#688) owns the provenance table of `patches-shipped-kernel` -- the 107 paths of area `patches-and-configs` under `projects/ROCKNIX/devices/**`, `projects/ROCKNIX/packages/linux*/**` and `packages/linux*/**` with reach `shipped` or `test`, less the H700 and GENERIC_X64 `linux/*.conf` (40,474 lines by the inventory's column and by `grep -c ''` at `2174265e9c`, 40,473 by `wc -l`; 106 `.patch` and one `.conf`; 103 shipped, 4 test; all vendor-carried, one fork-written by `tier_note`; five of them not the kernel's: the four H700 U-Boot patches and the one `kernel-firmware` patch, tabled as `non-kernel` with T27's and T11's recipes named) -- and edits none of them.** The table carries, per row, the patch's target version, the kernel pin of each device that applies it (the recipe's `case` branch at the read hash: `7.2` for H700 and SM8550, `7.1.2` for GENERIC_X64), whether it applies at that pin by `patch --dry-run` against the files it touches extracted from the cached pinned tarball into the lane's scratch, in `scripts/unpack`'s order, or `open item`, its upstream status as the header claims it and as `651150fc88` shows it, its backport status and the fork's reason; a row superseded at its pin is a lead to the kernel's owner (`device-generic-x64-and-kernel`), never a removal (D-WORKFLOW-209); a carried patch found wrong at the pin (the unfixed `0010-msm-resource-cleanup.patch`, fixed upstream by `9416eec2c2`) is a currency row and a `bug` naming upstream's fix, which reaches the fork with the next base merge, never as a fork edit; the fork-written H700 ramoops patch (`cbf75c0b06`, D-SYS-004) is read line by line and gets a `#585` line, not sent (D-WORKFLOW-164/165), its config half being T27's conf; the two excluded configurations are T27's and T11's. Local depth, `tier_exception` D-WORKFLOW-184, no reviewer, no guest, no build, no `scripts/unpack`, no `kconfig-*`, no network. The branch is cut from the coordinator's tip, which carries P1 (`2174265e9c`) since `6a12ce2d73`; no dispatch merge. | #688; #1054; #687; #1056; #585; #369; D-SYS-004; D-WORKFLOW-184; D-WORKFLOW-187; D-WORKFLOW-188; D-WORKFLOW-189; D-WORKFLOW-209 |

The pointer's `Register:` line is filled from the same `awk` at `__COHASH__`,
never from here (§ 10).

**Rows the pause may need, all put to the coordinator as questions, never
decided by the lane:** the `7.0/` triple as symlinks (§ 4 question 1); the
ramoops patch's contribution layer (§ 4 question 2); the tier reading as a
tooling finding (L-17); the order's title against the globs (L-21). A row
this slice forces takes an ID the coordinator assigns on #688.

**The kickoff addendum** (ruling (n)): written by the coordinator at
dispatch into `docs/futros/2026-10-25-m6-patches-and-configs.md` after
`:200` (its last heading `## Errata, after T40's acceptance (2026-10-25)` at
`:188`, R5 § C; the futro is 200 lines, `v1 read`), the area futro's first
addendum, in T38's six-paragraph shape (`docs/futros/2026-10-24-m6-doctrine.md:472`,
R5 C8): a heading `## T41 kickoff addendum (written with the brief's version
2, __DATE__)`, then **The plan, in the order's words** (`order.md:693-701`,
with the 40,474 against 40,473 fact and the five `non-kernel` rows);
**Assumptions the plan leans on and does not state** (that every row is a
kernel patch -- five are not; that `fork-own` finds the fork-written patch --
`tier_note` does; that the two fork-changed configurations are T41's -- the
order carves them out, R1 § 8 delta 6; that `0 fork-own` means no fork
commit -- one; that a `.patch` directory is the glob's -- `${LINUX}`,
`${DEVICE}` and `default` select nothing); **Known unknowns** (the futro's
`:67-73`, `:96` and `:194` as their spine, and this brief's `## Version 1`
items); **Patterns** (a count from the wrong tree, blindspot 75; a pin as a
claim about the image, blindspot 47; a duplicate edited on one side -- the
`7.0/`/`7.2/` triple; a header that under-describes a squashed series);
**What we could be missing (the simulation)** -- an Opus lane with only the
brief: edits a `.conf` to "fix" a config the pin dropped; fetches a kernel
tarball to test applies-at-pin; runs `git apply` against the generic
`packages/linux` source, the wrong kernel; runs `tools/adjust_kernel_config`
to read a config and rewrites the tree's conf; extracts a tarball into the
worktree or `/tmp`; copies the fixed `0010` from `651150fc88` into `7.0/`;
types `0 fork-authored` from T40's brief; sorts the table under the host
locale; writes one pin for all 107; counts fork-own by `tier`; calls the four
U-Boot rows kernel patches; sends the ramoops patch upstream (R5 § C);
**Adjustments before execution** -- version 2 of the brief, the stranger's
proof's corrections and the coordinator's rulings on them; then the version-2
line. Whether the addendum is also posted on #1054 is the coordinator's
(#1054's criterion 1 wants the futro's text as a comment, R5 § C).

**The ceremonies** every lane owes are the rules that load every session --
`learning-capture.md` (the work-log entry per session headed `#688`, its time
from `date -u` in the same command, `tools/work-log-index --write` after it,
in the lane's worktree only), `ceremonies.md` (a friction line the moment
something slows, `issue: #688` or the guard; `tools/ceremony-check --gate`
before every push, never `--no-verify`), `decision-register.md` (a row the
same session for any decision), `vm-first.md` (the VM question before any
proof: ruling (h) answers it), the mini-retro at stage G posted on #688 in
Instruction-Recommendations mode with its *adjustments* as proposals for the
coordinator -- and are not restated here. **D-WORKFLOW-187's drift re-review
at close**: T41's close records the churn count at its `fixed-at` so the
area's drift count has its baseline (#1054 criterion 3; R5 § I). What is this
slice's:

- **What a hold is**: a finding is held off the public tracker only under
  D-WORKFLOW-215's test; holding is the coordinator's, and the lane never
  opens a held directory (`/workspace/tmp/m6-t34/held/` and
  `/workspace/tmp/m6-t36/held/` included). None is expected in a table of
  kernel patches.
- **Every count is a tool's line** (`engineering-practices.md` § A name is not
  a behaviour): a figure in `02`, a post or the hand-back is the command's own
  output, quoted; a sum, a difference or a rate is computed by the command
  that prints it; **`rc=$?` on its own line after the command, never after a
  `$(...)` in the same word or a pipeline's last stage**; **no `cut` on an
  expected error line**; **a heading's time from `date -u`, never typed**;
  **a hash copied by a command, never completed from a prefix**.
- **Prose goes into a running log or a note through a quoted heredoc
  (`<<'EOF'`) or the Write tool, never an unquoted one** (plan § 6b): the 107
  names are full of backticks.
- **The sorts are the build's**: `LC_ALL=C` for every `sort` and glob the
  order column rests on (plan § 6b: *a host regeneration runs under `env -i`
  in the C locale, as the build does*); the locale stated beside each.
- A merge with conflicts is checked for markers; the ledgers united by whole
  entries; **a commit names its paths**; anything temporary under
  `/workspace/tmp/m6-t41/` after `df -i`, never `/tmp`; the scratch's
  extracted sources and the lint proof retired at stage H, their paths and
  retirement in `00`'s census (D-INFRA-022); **`rm -rf` only as
  `"${VAR:?}"/...` or a literal path, in its own short command, never inside a
  `bash -c` script**.
- A fixture rewrites no path outside scratch; **a credential-shaped value
  assembled at run time, never a literal** -- `.githooks/pre-commit` refuses
  the literal; a generator seen to exit non-zero on a constructed drift
  before its table is trusted.
- **Every edited file checked for an unfilled placeholder before its commit**:
  `/usr/bin/grep -c -E '__[A-Z0-9_]+__'` is 0 on the pointer, the running log
  and every artifact (the widened pattern of T38's errata before dispatch),
  and none of § 1's three hash words appears unfilled in a filled artifact.
  This brief carries the placeholder forms as its own words, so it is never
  copied into an artifact unfilled.
- Commit messages `docs: ...` on the slice branch for the audit folder, with
  `Refs #688`; no closing keyword before an issue number while a criterion is
  open (`issue-tracking.md`); `git add -A` only after `git status --short`
  shows nothing a run left behind (`.qa-scratch/` is gitignored).

## 10. Hand-back, the pointer, the host, the stops and what never runs

**The hand-back.** The coordinator accepts by reading, in this order, without
re-reviewing: #688's checkboxes against their artifacts; the lint's `PASS`
line on the default phase and with `--issue`; `review-plan.json` (Local, no
reviewer, `tier_exception` D-WORKFLOW-184) and `ls second-opinions/` showing
it alone; `00`'s stage-A lint proof (ruling (i)); the audit issue's checkboxes
all at an outcome; the provenance table's row count (107) and the coverage
table's (107) with the generator's `stats` line; every bug with its three
lines; **re-running on a clone of the slice branch at its tip under
`/workspace/tmp/m6-coordinator/`: § 2's block at P1 and at the tip, every
§ 5 run, the applies-at-pin run per plan, and `tools/t41-tables.py` with its
three mutations**, through the coordinator's acceptance script
**`kit/t41-accept.sh`**, written by **`kit/selftest/accept-t41/derive-t41.py`**
from `kit/t36-accept.sh` the way `derive-t39.py` wrote T39's (R5 § E; R3
§ 5), its self-test driver standing in the dispatch tip by the coordinator's
tip itself (no P1 merge, ruling (a)); its usage as T38's,
`AUDIT_ISSUE=<n> BUGS="<numbers>" DISPATCH_TIP=__COHASH__ bash t41-accept.sh <lane tip> <coordinator tip>`,
no ES tip. Its conventions are T38's: one `VERDICT PASS|FAIL|CANNOT|ABSENT|RAN
<section> -- <reason>` line per section, `SUMMARY: pass N, fail N, cannot N,
absent N, ran N`, `ACCEPT-RC` 0 when every section is PASS or RAN, 1 on any
FAIL, 2 on no FAIL but a CANNOT or ABSENT; `rc=$?` on its own line; counts by
`/usr/bin/grep`; every awk regex through `ENVIRON`, never `awk -v`; the whole
output through the credential mask; writes only under `ACCEPT_DIR` and `OUT`.
**Kept and re-pointed** (R5 § E): `pointer` (T41's eleven keys), `folder`
(`*-epic-m6-patches-shipped-kernel`), `dist-tip`, `product-paths`
(inverted: the lane's commits touch only its audit folder, its retro, its
pointer and its log entries; **a FAIL on any `*.patch`, `*.conf`,
`packages/`, `projects/`, `tools/` or `scripts/` change by the lane's own
commits**), `membership` (107 by § 2's block, its inputs at `2174265e9c`; the
block's sha256 prefix `4d300124a6bf116f` as `brief_block 2` extracts it),
`tree-counts` (107 / 40,474 / 40,473; 106 + 1; 103 / 4; the nine directories;
the seven `reachable_by` groups (4, 32, 56, 1, 4, 6, 4)), `issue-body` (`reviewed-at:`/`fixed-at:`, the
`-es` pair absent), `bug-bodies`, `lint`, `review-plan-local`, `lint-proof`,
`punch-list`, `ladder`, `audit-boxes`, `bug-boxes`, `scope-record`,
`read-order` (the three plans' orders), `tables` (provenance `107`, coverage
`107`), `generated`, `analysis-face`, `forbidden`, `secret`, `checker-run` and
`checker-record` (the generator's three mutations seen to fail),
`fixes-record` (expected *none*), `inherited-record` (§ 8's owners),
`proof-lines`, `lane-boxes`, `proved` (T40's five words), `rulings` ((a) to
(p)), `analysis`, `last-comments` (#688, #1054), `record-lines` (**the two
`#585` lines owed**), `generators` (`python3 -I -m py_compile` on
`t41-tables.py`), `runs-record`, `running-log`, `no-compile`, `handback`,
`retro`, `checkers`, `merge`, `runs`, `scratch`; `question-comments` (§ 4's
two). **Dropped**: every section that reads documents, skills, ES, a pin, a
guest or the host file's window (R5 § E's list; `nonascii`: a patch carries
non-ASCII legitimately). **Added**, each with a FAIL fixture seen to fail
before the section is trusted (R5 § E):

| Section | PASS when | FAIL fixture |
| --- | --- | --- |
| `patch-untouched` | `git log --no-merges --format=%h __COHASH__..<fixed-at> -- '*.patch' '*.conf' packages projects tools scripts` prints nothing (ruling (c); D-WORKFLOW-209) | a lane-shaped commit appending a byte to one of the 107 in a throwaway clone |
| `pins-read` | `02` quotes the five `PKG_VERSION` lines of `projects/ROCKNIX/packages/linux/package.mk` at the tip and the two `PKG_PATCH_DIRS` lines, and every provenance row's *current pin* is one of `7.2`, `7.1.2`, `v2026.01`, `20260309` | a provenance copy with a pin not among the four |
| `headers` | the header census line (`patches 106 with From: 87 with Subject: 89`) matches the generator's and every row without `Subject:` reads `hand-made` | a row with an empty origin cell |
| `applies-record` | every row's *applies-at-pin* is one of the closed vocabulary, and each non-`open item` cell names its `applies-<DEVICE>.txt` line; the three plans' line counts are `8`, `42`, `65`; the count of `open item` is the record's own line | a cell reading `yes` |
| `upstream-status` | the byte-identity loop's count at `651150fc88` equals the rows marked `upstream-changed` plus `upstream-moved` plus the fork-written one; every `claims mainline` cell quotes the header line it came from | a `claims mainline` row with no quoted line |
| `tarball-hashes` | the two `= its .sha256` lines quoted in `02` with the recipe's `PKG_SHA256` prefixes beside them | a hash line with a mismatching prefix |
| `device-groups` | the seven `reachable_by` groups (4, 32, 56, 1, 4, 6, 4)' sizes in `01` § Scope sum to `107` and equal the block's | one size changed |
| `fork-written` | `02` has one `#585` line for the ramoops patch (`0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch`) with its adding commit `cbf75c0b06`, one for the `=~` one-liner, and `04` § Q4 names both | a line removed |
| `non-kernel` | the five rows of `KIND TOTAL K5` carry `non-kernel` in the kind column and T27's or T11's recipe in the disposition | one labelled `patch` |
| `scratch-retired` | `00`'s census names `/workspace/tmp/m6-t41/src` retired at stage H and the hand-back's `ls -d /workspace/tmp/m6-t41/src` prints `No such file` | the directory present |

Then `register-check` on a simulated merge with the coordinator's tip; the
retro's answers; the checkers' exit codes; the inherited items' rows and their
owners with `tools/box-check --issue 688`'s line (§ 7's last checkbox); **the
§ 1 rulings' rows in `02`**. The lane posts one hand-back comment naming **its
one tip** and each artifact by path, writes `reviewed-at:` and `fixed-at:`
into #688's body, then says it is idle. **The hand-back's hashes are § 1's
placeholders, filled**: `reviewed-at:` is the commit the read was made at
(`__COHASH__`, the dispatch tip), `fixed-at:` the lane's `__TIPHASH__` when
the tables are complete, § 7's `<fixed-at>` that tip, the register's line is
read at `__COHASH__`, and the brief is cited at `__V2HASH__`; none of the
three words appears unfilled in the comment (§ 9's placeholder check). After
acceptance the coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the lint against **the audit issue**, merges the
slice branch in its turn (§ 8), carries § 8's #585 and #328 items to their
issues, writes the rule erratum into a sweep of its own (L-09), puts § 4's two
questions to the maintainer, routes the `0010` bug to the integration, and
closes #688 when every row is proven; the area epic #1054 closes when T40,
T41, T42 and T43 have.

**The pointer the lane checks at stage A, line by line.** The seeded pointer
`.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md`
is written by the coordinator from T40's and T39's. Before the first command
after `cat` the lane reads these eleven keys -- the keys verbatim from T38's
pointer, the values T41's (R5 § A, § H) -- each against the one value that
would be the seeding error, **T40's or T39's**, and reports any that names a
predecessor on #688 before going on. **The three hash words and the register
IDs are the seeding's to fill**; a pointer line still carrying one unfilled is
a seeding error too. Every figure in the *Must read* column is § 1's, § 5's or
§ 9's, copied from that one place (R5 § B item 6):

| Key | Must read | The seeding error reads |
| --- | --- | --- |
| `Branch (distribution):` | `feature/m6-patches-shipped-kernel-688`, cut from `feature/m6-renovation-plan-346` at `__COHASH__`, which carries `feature/m6-p1-survey-641` (`2174265e9c`) since `6a12ce2d73`; no merge commit; the lane's tip at stage A is `__COHASH__` | `feature/m6-patches-dead-687` *"stacked on `feature/m6-p1-survey-641` at `2174265e9c` with the coordinator's tip merged"*, or any merge-hash placeholder |
| `Worktree (distribution):` | `/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-kernel-688` | `m6-patches-dead-687` or `m6-doctrine-reference-686` |
| `Worktree (EmulationStation):` | **none**: nothing in the 107 is EmulationStation's | any ES branch or worktree named for #688 |
| `Executor:` | Opus 5.5 at high effort, in the T3 session `m6-t3-emulators` (ruling (m)) | T40's session `m6-t5-build-engine`, or T39's choice of `m6-t1-os-launch` |
| `Epic:` | #1054 (`M6.P2 E339: Area epic: the patches and kernel configurations (T40, T41, T42, T43)`); T40 (#687) accepted at `e863379cec`, closed out at `bf3409ea18`, #687 still open; T42 (#689) and T43 (#690) after | #807, or *"T23 the join target"* |
| `Depth:` | **Local -- a provenance table**: the executor alone; `review-plan.json` with reviewers `[]` and `tier_exception` D-WORKFLOW-184; no seat, no packet, no keyed call; the lint's Local proof at stage A | *"Local -- a table"* (T39's), or a seat named |
| `The lens:` | package currency over the 107 of `patches-shipped-kernel` -- the kernel patches and configurations the shipped (H700, SM8550) and test (GENERIC_X64) images apply, 106 `.patch` and 1 `.conf`, 40,474 lines by the inventory and by `grep -c`, 40,473 by `wc -l`, five rows `non-kernel`; per row the target version, the pin, applies-at-pin, upstream status, backport status, the fork's reason | *"reachability over the 778"* (T40's), or *"cost against value over the 254"* (T39's) |
| `The rule:` | **the lane edits none of the 107, no recipe, no tool, no script**; its commits touch only its audit folder, its retro, its pointer and its log entries; no `scripts/unpack`, `kconfig-*`, `adjust_kernel_config`, `check_kernel_config`, `kernel_make`, `config/options`; no fetch; no council, Facilitator or keyed call; a tarball extracted file by file into `/workspace/tmp/m6-t41/src/` only; a carried patch found wrong is a `bug` naming upstream's fix, never an edit (rulings (c), (g), (i)) | *"the lane changes only the reference documents proper"* or *"removes nothing and edits no `.patch` or `.conf`"* without the no-unpack clause |
| `The host:` | **none**: no guest window and no compile; the host file `/workspace/tmp/m7-m6-host-coordination.txt` read once at stage A for its protocol and its line count (`__HOSTLINES__` at dispatch); no START, RETURN or compile line of this lane's in it at any stage (ruling (h)) | a line naming T40, T39 or #687 |
| `Register:` | the highest decided row per area read from the table at `__COHASH__` (`__REGISTER_IDS__`; at `6a12ce2d73`: D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-137, D-WORKFLOW-219), at `2d3c57a625` D-WORKFLOW-220, T39's), plus **this slice's ownership row, D-WORKFLOW-22x, which the coordinator writes at dispatch** (221 by ruling (l), 220 being T39's since 06:22) | D-WORKFLOW-219 or D-WORKFLOW-220 named as this slice's own row |
| `The brief:` | `docs/reviews/briefs/patches-shipped-kernel.md` at `__V2HASH__` (filled by the dispatch comment; version 1 has no dispatch hash, and no such file exists at `6a12ce2d73`, R5 § H) | `patches-dead.md`, `doctrine-reference.md`, or the literal placeholder word |

**The host.** No guest window and no compile, so this slice holds no slot in
the host file's queue (ruling (h)): `/workspace/tmp/m7-m6-host-coordination.txt`
(named by T38's and T39's briefs; 712 lines at this draft's read, `v1 read`
by `wc -l`) is read once at stage A for its protocol, with the time of the
read and its line count beside the dispatch comment's (`__HOSTLINES__`); the
lane writes no line in it and posts no `START HH:MM:SS UTC` on #688; **a START
or a compile line of this lane's, in the file or on #688, is a stop**. The
guarded swap reclamation is not this slice's. No build on the host at any
time.

**The readings before dispatch** (plan § 3, principle 3): the area futro
takes the T41 kickoff addendum (ruling (n); § 9), and a stranger's proof of
this brief is run by a reader with no context before dispatch; version 2
records what it found, and its hash at dispatch is `__V2HASH__`.

**Stop only on:** every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); the stage-D pause (the punch list, the audit issue,
the bug(s) and § 4's two questions posted on #688; the lane waits for the
coordinator's word, drafting meanwhile the retro's four answers and editing
none of the 107); an explicit maintainer pause on #688; a blocker named on
#688 -- two commands that disagree, a block whose output differs from § 2's
beyond the deltas it records, a path of the 107 at the lane's tip differing
from `__COHASH__`'s, a pointer line that names T40 or T39, **a keyed call, a
`tools/council/run` call or a Facilitator run found in `00`**, **a START or a
compile line of this lane's on the host file or on #688**, a write under
`packages/`, `projects/`, `tools/` or `scripts/`, a `scripts/unpack` or
`kconfig-*` or `adjust_kernel_config` invocation, a tarball extracted outside
`/workspace/tmp/m6-t41/`; or an execution limit, stated as such with the
running log current. **Not** a stop: the absence of a reviewer (Local depth);
40,474 against 40,473 (two measures, ruling (a)); a `patch --dry-run` that
fails (a lead, ruling (g)); `tar` exiting 2 on a file a patch creates; the
lint's Local PASS not printing at stage A (a question, § 5); the tool's
`--order` row printing from the worktree with a status line moved (recorded);
`next` moving under the slice. A checkpoint is not a stop (D-WORKFLOW-149).
An idle session says it is idle on #688, **and does not end a turn on a post
that asks nothing**: a turn ends on a question on #688 or on the stage's
checkpoint post, never on "next is ..." (ruling (p)).

**What never runs in this slice:** an image build, a package build or any
compiler; `scripts/unpack`, `scripts/build`, `make kconfig-*`, `kernel_make`,
`tools/adjust_kernel_config`, `tools/check_kernel_config`, `tools/viewplan`
or `tools/renovation-inventory` without `--no-write` (ruling (g); R3 § 1.3);
`config/options` sourced anywhere, a recipe sourced anywhere (every pin is
`git show` text); a guest; a fetch -- no `git fetch`, no `git ls-remote`, no
`curl`, no `gh api` of another repository's contents (kernel.org is never
asked: upstream status is the header's claim, § 5); a council run, a
Facilitator call, any `tools/council/run` call keyed or keyless, `npm
install`; `tools/release-catalog --write`, `tools/renovation-status` or
`tools/renovation-drift` writing a ledger (`tools/work-log-index --write` after
the lane's own log entry excepted); `tools/pr-stack-check` (it makes a
worktree); a handheld; a `tar -x` outside `/workspace/tmp/m6-t41/`, into a
worktree, the cache or `/tmp`; M7's roots, worktrees or prep directories; a
held directory (D-WORKFLOW-215); `~/.config/council/env`, anything under
`~/.ROCKNIX/` or `~/.rocknix/`, the wordlist `~/.config/rocknix/forbidden-terms`
(its tool alone reads it), the user-level `~/.claude/`; a print of a
credential-shaped line or of a variable's value; `guard_load`; **an edit,
rename or removal of any `.patch`, `.conf`, recipe, `scripts/` or `tools/`
file, or of a file under `packages/` or `projects/`** (rulings (c), (o);
D-WORKFLOW-209: the table records, the maintainer decides, a fix reaches the
fork with the base merge); an edit to any `.claude/**` file, `CLAUDE.md`,
`AGENTS.md`, `NAMING.md`, a register (other than the appends the procedure
owns), `.github/sessions/saved-session-state-next.md` (T46's); the
coordinator's files (`order.md`, `slices.json`, `areas.json`, the plan, this
brief, #688's criteria, the M6 body, the futro); a post on #1054, #346, #585,
#369, #563 or #559; a checkout of T40's, T11's, T27's or T28's branch (each
is read with `git -C <worktree> show`); a push to any branch but the lane's
own; `fork-worktree sync|remove|repair`; bare `git stash`; `--no-verify`;
`git worktree remove --force` or `rm -rf` of any worktree or of a bare
variable path; a write in another lane's worktree; and a credential-shaped
literal in a fixture.

## Version 1: what the drafting read did not settle

Every open mark of version 1, with the read that settles it; then the places
where the research files disagree, and how this brief takes each; then the
checks on this file. The stranger's proof of version 1 reads this list first,
and version 2 records each item's state after it (T39's shape: **Settled**,
with where the body carries the fact and its command, or **Open**).

**The open marks** (each is a mark in the body, cited by its section):

1. **The block's lines at the lane's tip** (§ 1 (a), § 5's `# STAGE A`):
   expected identical to the P1 run's 99 lines, since the 107 did not move
   between P1 and `6a12ce2d73` (R5 C15: `present 107 of 107`; R2 command 7
   over the member directories). Settles: the stage-A `block-tip.sh` run and
   its `diff`.
2. **Whether the worktree's `tools/renovation-inventory --order --no-write`
   prints R1 C14's lines** (§ 2, § 5): R1 ran it from the clone's directory.
   Settles: the stage-A run with `git status --short --ignored` before and
   after.
3. **`tools/box-check`, `tools/ceremony-check` and `.githooks/hooks-test` at
   the dispatch tip** (§ 3 item 4, § 5): R5 C13/C15 ran `ceremony-check` at
   `6a12ce2d73` (`nothing overdue.`, rc 0); the other two no research file
   ran. Settles: their stage-A lines.
4. **The lint's Local proof** (§ 5's `# STAGE A`): T4's plan's three fields,
   the PASS line and the FAIL line -- T39's proof K111 printed them on the
   same folder at `a0fb117b8b`; this brief's tip is `6a12ce2d73`. Settles:
   the stage-A lines.
5. **The `rocknix-joypad` directory's contents at `651150fc88`** (§ 1 (f),
   L-02, L-14): R1 C16 found none under the override's `patches/`; the
   whole-tree count is the runs block's `grep -c -F 'rocknix-joypad/'` line.
   Settles: that line, and `git -C <store> ls-tree -r --name-only
   651150fc88 | /usr/bin/grep -F 'rocknix-joypad'`.
6. **The three symlink entries under the member roofs** (§ 2, L-23).
   **Settled** by `v1 read`: `git ls-tree -r 2174265e9c | awk
   '$1=="120000"{print $4}'` under the roofs prints
   `projects/ROCKNIX/devices/RK3566/filesystem/usr/share/alsa/ucm2/conf.d/aw88166/aw88166.conf`
   (-> `../../Anbernic/RG-DS-Plus/aw88166.conf`),
   `.../RK3566/filesystem/usr/share/alsa/ucm2/conf.d/simple-card/rk817_hp.conf`
   (-> `../../Anbernic/RG-DS-Plus/rk817_hp.conf`) and
   `projects/ROCKNIX/devices/SM8750/filesystem/usr/share/alsa/ucm2/conf.d/sm8750/SM8750-KONKR.conf`
   (-> `../../KONKR/PocketFitElite/KONKR-PocketFitElite.conf`) -- three ALSA
   use-case files under two unshipped devices' filesystem overlays, none a
   `patches` directory and none a member; #1056's gap moves no row of the 107.
   The lane's stage-A line re-states it.
7. **The non-kernel five's applies-at-pin by the same method** (§ 5, L-12):
   ruling (g) names the kernel tarballs; the U-Boot and firmware archives are
   cached (`v1 read`: `u-boot-DDR3-v2026.01.tar.gz`,
   `u-boot-DDR4-v2026.01.tar.gz`, `kernel-firmware-20260309.tar.gz`, top
   directories `u-boot-2026.01/` and `linux-firmware-20260309/`). Settles:
   the coordinator at dispatch -- the method extended, or the five cells read
   `open item` with the build named (`[proposed]`).
8. **The conf-diff counts (a) against H700's conf, (b) against
   `arch/arm64/configs/defconfig`, (c) the forced-symbol count** (§ 5, L-19):
   no research file ran them; (d)'s `7 7` is R2 command 9's. Settles: the
   runs block's three lines.
9. **Whether `CONFIG_DRM_MSM` is set in H700's conf** (L-31): decides the
   *applied, not built* note on the Qualcomm DRM rows. Settles:
   `git show HEAD:projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf |
   /usr/bin/grep -n -E '^CONFIG_DRM_MSM='`.
10. **The polldev consumers in H700's patches and the joypad driver** (L-14):
    R2 command 14 read RK3326's `004` only. Settles: `git grep -c -i polldev
    HEAD -- projects/ROCKNIX/devices/H700/patches/linux
    projects/ROCKNIX/packages/linux-drivers`.
11. **The applies-at-pin results** (§ 5): `8`, `42` and `65` dry-runs per
    plan; the rc counts and any `FAILED` line. Settles: the three
    `applies-<DEVICE>.txt` files and their `uniq -c` lines. The `--stat` of
    both `0010` copies against `upstream/next` (` 2 files changed, 28
    insertions(+), 22 deletions(-)` expected from the one copy's `14`/`11`,
    `v1 read`) is the runs block's line.
12. **The kernel version at the builds' commits** `069fc2704421` and
    `bcc866f1f314` (§ 3 not-leads; R3 § 2): a read of
    `projects/ROCKNIX/packages/linux/package.mk` at each in
    `/workspace/repos/rocknix`, if a row wants it. **Open**: not this slice's
    unless a row cites a built image.
13. **The members `tar` reports absent** (the files the patches create):
    recorded per plan from `tar-<DEVICE>.err`. Settles: the stage-B run.
14. **The host file's line count at dispatch** (`__HOSTLINES__`): 712 at this
    draft's read. Settles: the dispatch comment.
15. **The session's state** (`m6-t3-emulators` free since T37's close-out,
    ruling (m)): R5 C15/C16 could not read herdr's state key. **Settled in
    part** by `v1 read`: T39 went to the T1 session at 06:22 (`2d3c57a625`'s
    subject), so no other dispatch contends for T3; its state itself is the
    coordinator's `herdr agent list` at dispatch.
16. **The ownership row's ID** (ruling (l)). **Settled in part** by `v1
    read`: D-WORKFLOW-220 is T39's at `2d3c57a625` (`:781`), so T41's is
    D-WORKFLOW-221 unless another WORKFLOW row lands first; the register's awk
    at `__COHASH__` is the line that decides.
17. **Whether mainline 7.2's `sun50i-h616.dtsi` already carries a node at
    `0x4f000000`** (L-16): R2 § 2's tarball check. Settles: the stage-B
    `tar -xJOf ... | grep -n -A2 '0x40000000 0x0 0x40000'` line.
18. **The ramoops patch's contribution layer** (§ 4 question 2, L-16).
    **Open**: the maintainer's, put by the coordinator.
19. **The `7.0/` triple as symlinks** (§ 4 question 1, L-03). **Open**: the
    maintainer's, after the base merge.
20. **The adding commits of the 19 header-less rows at ROCKNIX** (L-05,
    ruling (k)): `git log --follow --diff-filter=A` per row. Settles: stage B;
    `unknown` where the history gives no author.
21. **#688's body fill at dispatch** (§ 1, § 7): the kit's. Settles: the
    `gh issue view 688 --json body` line count after the fill.
22. **The whole-tree `rocknix-joypad` count and upstream's `:16-20;26-53`
    lines** (the runs block): read in `$U`'s store. Settles: the two lines.
23. **The GENERIC_X64 conf's `CONFIG_DRM_MSM`** (L-31): T11's file, read the
    same way if the x86 `0010` row wants the note.
24. **Whether `tools/renovation-drift` and `renovation-status` are at the
    dispatch tip**: at `6a12ce2d73` the three renovation tools are (R5 C16's
    `ls` line); the tip moves nothing here. **Settled** for `6a12ce2d73`.
25. **The coordinator's tip moved under the drafting**: from `6a12ce2d73`
    (the research's hash) to `2d3c57a625` by three commits (`c1ca24f1c0` the
    T41 research fan-out's log; `86ebb6dffc` T39's dispatch with
    D-WORKFLOW-220; `2d3c57a625` its log and pointer), touching the register
    (one row), the friction log, the doctrine futro (16 lines, T39's
    addendum), the work log, its index and the coordinator's pointer
    (`git diff --stat 6a12ce2d73 2d3c57a625`: `6 files changed, 51
    insertions(+), 4 deletions(-)`, `v1 read`) -- nothing under the 107, the
    kernel recipes, `scripts/unpack`, `docs/reviews/` or the patches futro
    (200 lines at both). Every `6a12ce2d73` line in this brief is the
    research's read and stands; the lane's `__COHASH__` is later still, and
    § 5's `# STAGE A` reads every figure there. Settles: the dispatch
    comment's hashes.

**Where the research files disagree, and how this brief takes each:**

1. **R4 item 8's diff direction.** R4's first sentence read `git diff
   --name-status 651150fc88 2174265e9c` as *"upstream deleted six of the
   fork tip's `patches/7.2/`"*; R4 § 6 item 2 corrects it: the six `7.2/`
   patches and the `7.2.6/` four **exist at `upstream/next` and not at P1**
   (upstream added them), and the polldev patch exists at P1 and not upstream.
   R1 C11 (`12 A`, `1 D`, `4 M` from the base to `651150fc88`) and R2 § 4 say
   the same. **This brief takes R1's and R4's corrected reading** (L-14,
   L-22).
2. **The header-less count: 17 or 19.** R2 § 1 counts 17 hand-made diffs
   (neither `From:` nor `Subject:`); R1 C13 counts 19 without `From:` (the 17
   plus two list exports whose `From:` the exporter dropped, which carry a
   `Subject:`). Both are tool lines over different predicates. **This brief
   states both** (§ 2; L-05) and the generator prints both.
3. **The line figures.** R1's `grep -c` 40,474 and `wc -l` 40,473 over the
   107 at P1 (one unterminated file); R2's `wc -l` through `$(...)` is 51
   fewer over the 106 patches (the substitution strips the trailing blank
   line of a `format-patch` file). Different measures; **this brief takes
   R1's two** (ruling (a)) and names R2's as a measure of the shell.
4. **The firmware recipe's owner.** R1 § 8 delta 4 names the three
   non-kernel recipes T27's and T11's; R4 item 18 cites #1083/#836 as T11's
   and T8's. **Ruling (b) decides**: T27 for U-Boot, **T42 for the firmware
   recipe** (`patches-shipped`, the area's `rest`); the brief follows the
   ruling.
5. **Which `case` label selects each pin.** R5 § 0 marks it `[unverified]`;
   R1 C06 read the labels as text (`H700|SM4450|...|SM8550|...` -> `7.2`;
   `RK3326|AMD64|GENERIC_X64` -> `7.1.2`), confirmed by `v1 read`. **This
   brief takes R1's.**
6. **The futro's parenthetical** *"fork-written configs (T41's)"* (`:72-73`)
   against the order's carve-out (R1 § 8 delta 6; R4 item 4): the two
   fork-changed configurations are T27's and T11's; T41's one configuration
   is upstream's unchanged. **This brief corrects the sentence when it cites
   the futro** (ruling (d); the kickoff addendum's *Assumptions*).
7. **The test image's reach: 9 of 107.** R3 § 3's sentence (*"the test image
   carries 9 of the 107"*) is a sum over R1's `reachable_by` groups (4
   `mainline/` + 4 `7.0/` + 1 firmware). **This brief cites R3's sentence as
   R3's** and the block's `reachable_by:` groups as the tool's lines.
8. **R4 § 0's `[unverified]` non-members** `packages/linux-firmware/rtl8723bs_bt/patches` (2)
   and `packages/linux-driver-addons/**` (2), presumed unreached: R1 C07's
   `TREE-SIDE` line prints `unreached 281` under the slice's globs against
   T40's 277 generic kernel patches, so the four are `unreached` and T40's.
   **Settled by R1.**
9. **R5 § A's `0 fork-authored`** (T40's `:178`) against this slice's **1**
   (`cbf75c0b06`): not a disagreement -- T40's figure is over the 778 and
   this slice's over the 107 (R5 § B item 2 names the trap). **This brief
   states 1.**
10. **The `.sha256` files' format.** R3 § 1.4 says each tarball has a
    `.sha256` beside it; `v1 read` shows the file is 65 bytes (a hash and a
    newline, no file name), so the runs block compares `cut -c1-64` of it with
    `sha256sum`'s first field rather than running `sha256sum -c`. Not a
    disagreement; a shape the command meets.

**Checks on this file, version 1** (run from the coordinator's worktree on
the file as written to `docs/reviews/briefs/patches-shipped-kernel.md`, each
command's own line, `LC_ALL=C`, counts by `/usr/bin/grep`):

- `/usr/bin/grep -c ''` prints `2102`.
- The leads (`/usr/bin/grep -o -w -E 'L-[0-9]{2}' | sort -u | /usr/bin/grep -c ''`): `31` distinct IDs, L-01 to L-31; § 3's table carries `31` rows in its shape (`/usr/bin/grep -c -E '^\| \*\*L-[0-9]+\*\* \|'`).
- § 7's checkboxes (`awk '/^## 7\. /{p=1;next} /^## /{p=0} p' | /usr/bin/grep -c '^- \[ \]'`): `28`; `tools/box-check`'s own predicate -- its `PERSON`, `DEVICE` and `FACT` patterns read from its source at the tip and applied as its `:92-93` apply them over § 7's lines (the tracker not read): `boxes 28 fail 0`.
- The open marks (`/usr/bin/grep -c -i unverified`): `23` lines, the two sentences that define the mark among them.
- Unfilled-placeholder shapes (`/usr/bin/grep -o -E '__[A-Z0-9_]+__' | sort | uniq -c`): the six dispatch placeholders only, `48` occurrences on `42` lines -- the coordinator's tip `31` (on `29` lines, proof K109), the date `2`, the host file's line count `5`, the register IDs `1`, the lane's tip `2`, the brief's version-2 hash `7`; no merge-hash form (ruling (a)); the time placeholder unused.
- § 2's block, extracted by `brief_block 2` (`kit/t36-accept.sh`'s awk: the first bash block of `## 2.`) and by its markers alike: `148` lines, `11779` bytes, sha256 prefix `4d300124a6bf116f`, `cmp` equal to R1's `block.sh`; the expected segment between its markers `99` lines, `cmp` equal to R1 C07's output as R1 § 6 carries it (the marked segment's sha256 prefix `731a6ae863318656`); `bash -n` over the file's `4` bash blocks: rc `0` each.
- The hooks' credential regex, built as `.githooks/guard-lib` builds it (`SECRET_PATTERNS=''`, `.githooks/secret-patterns` sourced from `git show HEAD:` into a scratch file, `grep -E -e`, never `-f`, never `guard_load`): compile rc `1`, the runtime-built private-key header matched `1`, the file matched `0`. The coordinator's probe `/usr/bin/grep -c -i -E '(token|key|pass|psk)[= ]+[^ ]'` prints `21`: every hit is R1's deliberately spaced `key = lambda` (the block's own convention) or the English word *pass* / `PASS`; none carries a value.
- `tools/forbidden-terms-check --stdin < <this file>` from the coordinator's worktree: `forbidden-terms-check: 0 hits on stdin`, rc `0`; the planted positive through `FORBIDDEN_PATTERNS`: `forbidden-terms-check: 1 line(s) on stdin carry a listed word`, rc `1` (the list itself never read).
- `tools/register-check` with this file in the tree: rc `0`, `register-check: 716 IDs, each once; every citation in the live documents names a row` (`docs/reviews/briefs/` is not in its `LIVE` list, so its step 3 -- a letter where the number goes -- does not read `D-WORKFLOW-22x`); a `cites` probe of this file's own `D-[A-Z]+-[0-9]+` set against the register's rows prints `UNRESOLVED D-WORKFLOW-22` (the `22x` form cut at the letter) and `UNRESOLVED D-WORKFLOW-221` (the row the coordinator writes at dispatch, ruling (l); no row yet) -- the kit fills the first and the dispatch writes the second -- and `39` other IDs, every one naming a row.
- `D-WORKFLOW-22x` on `6` lines; `D-WORKFLOW-220` on `8` lines, each naming T39's row; `D-WORKFLOW-219` on `4` lines, each naming T38's dispositions row or the register's state at `6a12ce2d73`.
- Research citations: `R1 C<nn>` `15` distinct, `R2 L-<nn>` `15` distinct (R2's numbering, never this brief's), `v1 read` on `58` lines.

Version 1, 2026-11-01T06:36:12Z, written from the five research files and the coordinator's rulings for the coordinator's dispatch; the stranger's proof of it makes version 2

## Version 2: corrections from the proof

The stranger's proof of version 1 (`/workspace/tmp/m6-coordinator/kit/t41-proof.md`,
in no tree, 331 lines, 17 of its 18 commands) read the brief at `7d70da5972`
by hash and closed on its own totals line `checks 112; PASS 93; MISMATCH 7;
SETTLED 8; NOTE 4; corrections 7` (its C15). Each correction is applied in
the body at the line the proof names, under the coordinator's rulings
(D-WORKFLOW-189); the line is version 1's at `7d70da5972`.

| X | Version 1 line(s) | Old words | New words | The proof's command |
| --- | --- | --- | --- | --- |
| **X01** | `:1234`, ruling (f) `:291-293`, the runs `:1312`, `:1315-1323`, `:1339-1341`, `:1347-1348`, `:1355`; the leads L-01, L-02, L-14, L-19, L-20, L-22; § 7 `:1527-1530`; § 10 `:1791`; open items 5, 11 and disagreement 1 | `upstream/next` in every command and expectation | `651150fc88` -- the commit the expectations were read at; the local ref moves (`50433c03cc` on 2026-11-02, 59 commits on) and stage A records its value as information only; ruling (f) says so. The two forward-looking criteria (the `0010` bug's *"empty once the base merge lands"*, `:1492`, `:1528`) keep the ref, which is what they mean | C7, C12: `upstream/next now: 50433c03cc 2026-11-01 Merge pull request #3580 ...`; `commits between: 59`; pinned at `651150fc88` every expected line reproduces (K94, K95) |
| **X02** | `:1425`, `:1767-1768`, `:1793` | *"the four `reachable_by` groups"* | *"the seven `reachable_by` groups (4, 32, 56, 1, 4, 6, 4)"* | C2: the block's own `reachable_by:` line, seven keys, sum 107 (K15) |
| **X03** | `:1089` (L-22) | the `--name-status` over three directories expecting `12 A, 1 D, 4 M` | the fourth directory `projects/ROCKNIX/devices/SM8550/linux` added, as § 5's `KD` (`:1314`) has it | C7: `KD3 (L-22): 12 A; 1 D; 3 M;`; the fourth `M` is SM8550's `linux.aarch64.conf` (K76) |
| **X04** | `:79-80` | #688's body *"sha256 prefix `2a5a2d8d6ea5be43`"* | the command named and its print, `5f82f7ac42f4345d` | C10: `gh --repo pixelelated/distribution issue view 688 --json title,body,state`, the body hashed with and without a final newline: `5f82f7ac42f4345d` both times (K23) |
| **X05** | `:1068` (L-01) | `7.2/0010:12` hunk | `7.2/0010:15` hunk | C8, C12: `:12` is the `index` line; `15:@@ -1442,6 +1442,7 @@` (K60) |
| **X06** | `:173-174` | *"moved by `fe5216ff69` 2026-09-16"* | authored 2026-09-16, committed 2026-10-09, its subject quoted | C7, C10: `fe5216ff69 author 2026-09-16 commit 2026-10-09 rocknix-joypad: update version` (K69) |
| **X07** | `:2094` | *"on `42` lines -- the coordinator's tip `31`"* | `48` occurrences on `42` lines, the coordinator's tip `31` on `29` lines | C11: `placeholder lines 42 occ 48`; `COHASH lines 29` (K109) |
| (X01's own) | `:1666` (the draft row), § 5 rule 3 `:1186` | *"as `upstream/next` `651150fc88` shows it"*; *"`upstream/next` at `651150fc88` as a local ref"* | *"as `651150fc88` shows it"*; *"upstream at `651150fc88` in the local store"* (the substitution doubled the hash; corrected in the same version) | -- |

**The coordinator's two rulings version 1 left open:**

- **The firmware recipe's owner is T11, not T42** (ruling (b), the
  responsibility sentence of § 1, `non-kernel`'s acceptance section;
  version 1's disagreement 4). The inventory row for
  `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk` reads
  area `devices`, reach `shipped`; the first `devices` slice whose select
  takes it is T11's (`projects/ROCKNIX/packages/**`, reach shipped/test/n/a);
  T42's `rest` holds only `patches-and-configs` paths. R1 § 8 delta 4 and R4
  were right; version 1's T42 was the coordinator's error. The U-Boot
  recipes are T27's, as version 1 said (`device-h700`, by its
  `projects/ROCKNIX/devices/H700/**`).
- **The non-kernel five's applies-at-pin is by the same method** (open item
  7): ruling (g) now names the cached U-Boot and firmware tarballs and their
  top directories; the five cells carry their own `applies-<recipe>.txt`
  lines, never `open item` for want of a method.

**The open items the proof settled** (each its K-id; the body is unchanged
where version 1 already carried the fact): **1** -- at `7d70da5972` the 107
and the three JSONs equal P1's, so the tip re-run meets the P1 lines (K20);
**4** -- the lint's Local proof on T4's folder printed `PASS` (rc 0) and its
`tier_exception`-removed copy FAILed (rc 1) (K93); **5** and **22** -- the
whole-tree `rocknix-joypad` count is `1` at both upstream refs, and
`fe5216ff69` names the driver's recipe, not a patches directory (K97); **8**
in part -- (a) `2609`, (c) `17` forced symbols, (d) upstream's header line
`# Linux/arm64 7.2.0 Kernel Configuration`; (b) needs the tarball's
defconfig and stays the lane's (K98); **9** and **23** -- `CONFIG_DRM_MSM=y`
in SM8550's conf only, `0` in H700's and GENERIC_X64's (K80); **10** -- no
polldev consumer under H700's patches or the joypad driver at P1 (K70);
**11**'s `--stat` half -- both `0010` copies ` 2 files changed, 28
insertions(+), 22 deletions(-)` against `651150fc88` and today's ref (K96);
**16** -- D-WORKFLOW-221 is still free at the coordinator's tip (K91), and
is written at dispatch unless another row lands first. **Open**, as version 1
left them: 2, 3, 6's re-statement, 7's results (now by method), 8 (b), 11's
dry-runs, 12 to 15, 17 to 21, 24 and 25 -- each the lane's at its stage or
the dispatch's fill.

**What the proof could not check** (its own section) stays the lane's to
read at its stage: the research files' attributions, the issues outside
#688/#1054/#687, the other slices' tips, everything inside the tarballs (the
applies-at-pin dry-runs, L-06's and L-16's greps, the defconfig count), and
the checkers it was not allowed to run.

Version 2, 2026-11-02, the coordinator's, from the stranger's proof of version 1 and two rulings; the dispatch comment names its hash


## Stage-B method erratum — 2026-11-02T17:10:18Z (D-WORKFLOW-222)

This dated addendum supersedes ruling (g), § 5's applies-at-pin loop and
§ 7's applicability criterion **only where they treat dry-run status as the
applicability verdict or skip an entire patch after that diagnostic fails**.
The original v2 text and its execution receipts remain historical evidence.
Ownership, membership, pins, cached archives, Local depth and all source-only
limits remain as dispatched. This is a coordinator ruling under D-WORKFLOW-189.

The immutable early-blocker packet at `3cd9ca140a0da9af447a3ee2fb9cdbbbf222a95b`
(`#688` comment 6583064842) proves H700 order 011's complete patch applies to
exactly the input on which its dry run fails. `stage-b/same-input-refutation.json`
and its two named outputs record dry-run rc=1, normal application rc=0, identical
patch SHA256 and identical pre-application tree digests. The later hunk in the
concatenated input needs earlier edits to the same file. The six original H700
failure rows are method-contaminated leads, not six proved product bugs.

### Corrected execution and evidence

1. Preserve every original Stage-A/B receipt and the failed runner exactly as
   committed. Create a separately named corrected runner and packet under
   `stage-b/corrected/`; record its source hash and actual tool version. No live
   script is edited. Retain raw diagnostic text using the already accepted
   H700 0158 escape in committed records.
2. Use the same immutable source ref `02aab33bd9842610b0d466c9c186454dc14373ee`,
   the same checked archive hashes, touched-file extraction and exact C-locale
   order. Reconstruct the six plan sequences in fresh lane scratch under
   `/workspace/tmp/m6-t41/src/`, with counts **8 / 42 / 65 / 2 / 2 / 1**
   (120 plan applications over 106 patch paths). Stage B is incomplete and its
   method changed, so these runs replace the contaminated applicability
   evidence; this does not reopen accepted Stage A. Missing archive members
   must be accounted for by patch-created paths; create an empty scratch root
   when all targets are new, as the firmware refutation already established.
3. For each row, copy the current successful prefix into a fresh disposable
   candidate. Record the plan/index/path, patch SHA256, input tree digest,
   command argv and produced timestamp. Retain the same-input dry-run output
   as a diagnostic, assert that it did not change the candidate, then run the
   **complete normal application** with the same patch bytes:
   `patch -p1 -N --batch --directory <candidate>` with the patch on stdin.
   A nonzero dry run does not suppress this complete application. Both writes
   stay in the disposable touched-file copy, never the repository or cache.
4. Persist both return codes and outputs immediately. The normal application
   is authoritative: rc=0 promotes the candidate to the next prefix;
   classify `fuzz` before `applies with offset` before `applies`, using the
   **normal-application output**, not the dry-run output. Persist input/output
   tree digests. Do not promote a nonzero or timed-out candidate, even when it
   partly applied. Retain that failed candidate for inspection; keep the last
   successful prefix unchanged. Its row is `fails` with the hunk/error evidence;
   later rows in that plan are `open item: blocked by failed predecessor N`,
   not tested against a silently skipped or partially applied predecessor.
5. Before trusting the corrected summary, prove the failure path on a separate
   deliberately failing patch fixture: the successful-prefix digest stays
   unchanged, the failed candidate is not promoted, and a later row is marked
   blocked. Also retain the H700 011 positive that completes despite its
   nonzero diagnostic; the existing refutation is the before evidence, and
   the corrected run supplies the after receipt. No finding is predetermined.
6. Every authoritative row names `apply_rc`, `dry_rc`, normal offset/fuzz/FAILED
   counts, input/output digests and its receipt paths. A blocked row names the
   failed predecessor and has no invented command result. `02` § The runs
   reports the six populations separately and all nonzero application results
   and dry/apply disagreements. The provenance generator consumes the corrected
   authoritative status, covers all 120 applications and all 106 patch paths,
   and counts blocked rows explicitly. A real application failure remains a
   bug candidate or source lead under the existing evidence floor; a dry-run
   disagreement alone is not a product defect.

Complete the remaining Stage-B reads and `02-forward-audit.md`,
`03-retrospective.md`, `04-analysis.md` plus the corrected packet, then commit,
push and checkpoint on #688. Stop at the previously agreed Stage-B boundary.
No build, guest, fetch, configuration sourcing, product edit, runtime allocation
or host-ledger write is introduced. The coordinator's future `t41-accept.sh`
derivation must check this erratum and the current reader identity.

The live issue's applicability criterion and the area's futro addendum receive
this correction in the same session. D-WORKFLOW-221's original wording is kept
as history and refined by D-WORKFLOW-222. These are bounded source checks, not a
claim that any kernel or firmware boots or behaves correctly.


## Acceptance erratum — 2026-11-02T18:55:24Z (D-WORKFLOW-226)

This prospective amendment supersedes § 10's blanket replay sentence. Stage-A/B
acceptances and their immutable receipts remain valid; the resumed coordinator
reconciles those artifacts without re-executing accepted producers. Stage C's
new formal generator has its own retained five positive and three negative
receipts at `94b5b1c0b983313325dba101217761c6e5c9bca0`. None of this is final
slice acceptance. Missing evidence still produces FAIL, CANNOT or ABSENT.

The final runner's `membership` section directly reconciles the retained block,
99-line outputs, selected immutable modes/blobs, inputs and counts against P1
and the final tip. It does not execute the old block. `runs` reconciles the
accepted 120 complete normal applications and D-WORKFLOW-222 candidate/prefix
receipts, including argv, patch/source/log hashes, digest-chain links, counts,
non-promotion control and the H700-011 dry/normal disagreement. Retained tree
and archive digests are producer observations, not newly measured filesystem
state. It never re-extracts sources or reapplies patches.

`checker-run` and `lint-proof` reconcile the exact historical program/fixture
identities, commands, output/exit receipts and their expected failures and
positive controls. Confirm those program/input identities are unchanged at the
final tip. An unexpected changed accepted input is a concrete coordinator
blocker, not automatic replay or PASS. A known, explicitly scoped new artifact
or failed predicate receives its own check; no blanket replay follows.

The final, previously unsatisfied gates still execute against the candidate:
resolution lint normally and with the audit issue; current rules/register/index/
ceremony and forbidden/secret checks; syntax checks on the final audit-local
generator; live issue/checkbox checks; and the simulated integration with the
exact coordinator tip. They must preserve actual command/output/exit evidence.
Do not substitute old receipts for checks of newly changed final records.
Review the commands first, confine writes to the coordinator's owned scratch,
mask permitted logs, use the existing checkers' interfaces, and keep all
source-only/held-data/runtime limits. The integration simulation changes only
a disposable clone; it does not merge or push a live branch.

The T2 implementation candidate remains separate from shared kit files. Its
receipt predicates and synthetic fixtures are useful, but its executable final
gates must be completed and tested before installation. Authorize implementation
and synthetic-fixture verification only in that candidate; no real final
acceptance run before the lane's completed hand-back. The coordinator alone
installs, runs, reads and accepts the final runner. Its verdict/summary/exit
contract and fail-closed behavior from § 10 remain unchanged.


## Stage-D disposition — 2026-11-02T19:04:29Z (D-WORKFLOW-227)

The coordinator’s exact records-only E–H disposition is retained in
`docs/qa-logs/2026-11-02-m6-resume/t41-stage-d-disposition.md`. It defers
PL-001 to open integration bug #1408, preserves the T11 duplicate-storage
question for integration, and applies settled D-SYS-004 to the unsent ramoops
draft. The live #688 disposition comment releases execution; this document
does not claim final acceptance or a source fix. D-WORKFLOW-226 remains the
final-check contract.


## Final generator-control evidence — 2026-11-02T19:23:41Z (D-WORKFLOW-228)

D226’s exact historical negative-input condition cannot be met by the retained
Stage-C packet: its hashes bind outputs, not the three fixture inputs. The
bounded corrective check is specified in
`docs/qa-logs/2026-11-02-m6-resume/t41-generator-input-ruling.md`. T3 retains
three new negative inputs and one positive with exact identities; T2 checks
the sealed packet without invoking the producer. Historical receipts remain
unchanged and explicitly incomplete for input identity. This is the narrow
failed-predicate check allowed by D226, not replay of applications or stages.

### Final fixture-path clarification — 2026-11-02

D-WORKFLOW-228 expressly requires a retained header mutation and permits a
recorded implementation correction. At final `61a1a674c10d520f9d93748c5a73deaadb08b158`,
the suffix-only predicate in criterion 5 therefore finds two authorized audit
fixtures. The original unqualified command is nonempty, not PASS. Replace
its suffix-only test with a protected-product test plus this exact exception:
under the T41 audit, only `stage-f/generator-input-proof/fixtures/bytes/`
and its preserved `stage-f/generator-input-proof-attempt-1/fixtures/bytes/`
may contain the one deterministic D228 header path, each mode 100644 and
byte-equal to the independently reconstructed mutation. Validate the failed
attempt's recorded identity/lossless storage before accepting that copy.
No other audit `.patch`/`.conf` path is exempt. The complete `packages/`,
`projects/`, root `tools/` and `scripts/` trees, all 107 selected source
mode/blobs and zero removed register lines remain protected.

Integration whitespace checks preserve full diagnostics. The four accepted
records `01-research-notes.md`, `stage-a/order.out`,
`stage-a/run/stage-a-extra.out` and `stage-a/run/stage-a.out` may retain only
their exact accepted-D mode/blobs; the two fixtures retain exactly their
proved input bytes. Every other path must pass the normal whitespace check.
An altered old receipt, extra fixture or nonfixture whitespace remains FAIL.
No product edit, historical receipt normalization or blanket suffix/whitespace
exemption is authorized. Final integration and acceptance still execute under
D-WORKFLOW-226; this clarification alone accepts no result.

### Pins-read count correction — 2026-11-02

The § 10 `pins-read` row's "two PKG_PATCH_DIRS lines" is a specification
error. At accepted source `02aab33bd9842610b0d466c9c186454dc14373ee` and
handback `61a1a674c10d520f9d93748c5a73deaadb08b158`, the unchanged Linux
override has five anchored PKG_VERSION assignments (lines 23/30/37/43/49),
four anchored PKG_PATCH_DIRS assignments (16/27/40/46), and a separate
conditional assignment at line 18. All ten lines must be quoted literally
with their line numbers in 02, plus case-label context and the exact source
ref. Keep the distinction between the whole recipe read and T41's selected
pins: provenance rows still admit only `7.2`, `7.1.2`, `v2026.01`, `20260309`.
Other device branches are context, not new membership. The prior summary
does not satisfy this quotation requirement; append a records-only correction
and preserve every accepted source/program/receipt. No application, generator
control or whole-stage replay is required by this presentation correction.
