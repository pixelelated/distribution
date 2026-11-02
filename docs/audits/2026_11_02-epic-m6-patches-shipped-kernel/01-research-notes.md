# Research notes — M6.P2 T41, the kernel patches and configurations the shipped and test images apply (#688)

## Scope

The membership is defined by § 2's `block.sh` in `docs/reviews/briefs/patches-shipped-kernel.md` at `9313492990` (version 2, sha256 prefix `24794608bcc7a0f9`, 2,194 lines), extracted by its HTML markers and never retyped, and run from the lane's worktree (`feature/m6-patches-shipped-kernel-688` at `f03b64419f`, cut from the coordinator's `d7dd766659`, which carries P1 `2174265e9c` since `6a12ce2d73` and `next` `8ebaf8daad`). The three input JSONs at the tip match P1's (`slices.json` sha256 prefix `49bc2745664e52f4`, `inventory.json` `d17b9cac4b2c2245`, `areas.json` `985f742cfd4a2138`).

- **Extracted block (`stage-a/p1-qa-scratch/block.sh`):** sha256 prefix `4d300124a6bf116f` (`4d300124a6bf116f`), `148` lines (`11,779` bytes); expected output (`stage-a/p1-qa-scratch/block-expected.txt`): `99` lines.
- **`reviewed-at`:** `f03b64419f` (the seed commit over `d7dd766659`); P1 hash `2174265e9c`; inventory head `eb4763e3cc9bcd729830cd85f1719bbd4f28db10`; merge base `c445081a59518f37d9776e5412dd7b14910696f7`; pinned upstream commit `651150fc88` (local ref `upstream/next` at Stage A read `50433c03cc`, 59 commits on, recorded as information only per ruling (f) and proof X01).

### 1. § 2's membership block at P1 (`2174265e9c`) and at the tip (`f03b64419f`)

Running `bash .qa-scratch/t41/block.sh` (`stage-a/block.out`) against `W=/workspace/tmp/m6-coordinator/t11-research/tree` and `P1=2174265e9c` exited `0` and matched the 99 expected lines byte for byte (`diff .qa-scratch/t41/block-expected.txt /workspace/tmp/m6-t41/tmp/block.out` empty: `block = the brief's expected lines`):

```text
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

- **Tip re-run (`stage-a/block-tip.out`, `W` bound to this worktree, `P1` bound to `HEAD` `f03b64419f`):** `block at the tip rc=0`; `diff /workspace/tmp/m6-t41/tmp/block.out /workspace/tmp/m6-t41/tmp/block-tip.out` is empty (`the same lines at the tip`, 0 differing lines).
- **Both line figures and the one unterminated file (ruling (a)):**
  - **`40,474` (`40474`)** is the inventory's `lines` column (`GROUPS TOTAL 107 40474 groups 9`) and `/usr/bin/grep -c ''` over the 107 at P1 (`2174265e9c`), at the inventory head (`eb4763e3cc`), and at the tip (`f03b64419f`).
  - **`40,473` (`40473`)** is `wc -l`'s total at P1 and at the tip, one line fewer because `projects/ROCKNIX/devices/SM8550/patches/linux/0004-drm-msm-a6xx-Enable-IFPC-on-Adreno-740.patch` has no trailing newline (`wc -l` `32`, `/usr/bin/grep -c ''` `33`; L-24).

### 2. The seven `reachable_by` groups (`device-groups`, sum = `107`)

From the block's `reachable_by:` line (`4, 32, 56, 1, 4, 6, 4`, summing to `107`):

| `reachable_by` tuple | Rows | What they are |
| --- | ---: | --- |
| `('H700-aarch64',)` | 4 | the 4 H700 U-Boot patches (`u-boot-DDR3/patches` 2, `u-boot-DDR4/patches` 2; `non-kernel`) |
| `('H700-aarch64', 'H700-arm')` | 32 | `projects/ROCKNIX/devices/H700/patches/linux/*.patch` |
| `('SM8550-aarch64', 'SM8550-arm')` | 56 | `projects/ROCKNIX/devices/SM8550/patches/linux/*.patch` (55) + `projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf` (1) |
| `('GENERIC_X64-x86_64', 'H700-aarch64', 'SM8550-aarch64')` | 1 | `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/patches/kernel-firmware-02-add-brcmfmac-43xxx-configs.patch` (`non-kernel`) |
| `('GENERIC_X64-x86_64',)` | 4 | `projects/ROCKNIX/packages/linux/patches/7.0/*.patch` (`test` reach) |
| `('H700-aarch64', 'H700-arm', 'SM8550-aarch64', 'SM8550-arm')` | 6 | `projects/ROCKNIX/packages/linux/patches/7.2/*.patch` |
| `('GENERIC_X64-x86_64', 'H700-aarch64', 'H700-arm', 'SM8550-aarch64', 'SM8550-arm')` | 4 | `projects/ROCKNIX/packages/linux/patches/mainline/*.patch` |
| **Total** | **107** | `4 + 32 + 56 + 1 + 4 + 6 + 4 = 107` |

### 3. The tool's `--order` row, the nine directories, the three plans' application orders, the header census, byte identity, `.patch.disabled`, and symlinks

- **`tools/renovation-inventory --order --no-write --distribution /workspace/tmp/m6-coordinator/t11-research/tree` (`stage-a/order.out`):**
  ```text
  renovation-inventory --order rc=0 lines=50
  slices: 46
  rows: 134634 (inventory: 134634)
  unassigned: 0
  ambiguous: 0
   41 patches-shipped-kernel             patches-and-configs       107 paths    40,474 lines        0 read        0 fork-own   40,474 patch  table   
  ```
  `git status --short --ignored | /usr/bin/grep -c ''` was `1` before and `1` after.
- **The nine directories' counts (`GROUPS`):**
  - `K2` `projects/ROCKNIX/packages/linux/patches/7.0/`: `4` paths, `585` lines (`test`).
  - `K2` `projects/ROCKNIX/packages/linux/patches/7.2/`: `6` paths, `651` lines (`shipped`).
  - `K2` `projects/ROCKNIX/packages/linux/patches/mainline/`: `4` paths, `648` lines (`shipped`).
  - `K3` `projects/ROCKNIX/devices/H700/patches/linux/`: `32` paths, `8616` lines (`shipped`), plus `1` `.disabled` file (`0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled`, 4,036 lines, T27's row).
  - `K3` `projects/ROCKNIX/devices/SM8550/patches/linux/`: `55` paths, `20900` lines (`shipped`), plus `1` `.disabled` file (`0053-add-hynitron-touchscreen.patch.disabled`, 20,593 lines, T28's row).
  - `K4` `projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf`: `1` path, `8608` lines (`shipped`).
  - `K5` `projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/patches`: `2` paths, `139` lines (`shipped`, `non-kernel`, T27's recipe).
  - `K5` `projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/patches`: `2` paths, `139` lines (`shipped`, `non-kernel`, T27's recipe).
  - `K5` `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/patches`: `1` path, `188` lines (`shipped`, `non-kernel`, T11's recipe per version 2's ruling).
  - Seven uncreated patch directories under `projects/ROCKNIX/packages/linux/patches/`: `absent patches/H700`, `absent patches/SM8550`, `absent patches/GENERIC_X64`, `absent patches/default`, `absent patches/aarch64`, `absent patches/x86`, `absent patches/7.1.2`.
- **The three plans' kernel patch application orders (`LC_ALL=C`, `scripts/unpack:127-159`):**
  - `GENERIC_X64 total: 8` (`mainline/` 4 + `7.0/` 4; `stage-a/order-GENERIC_X64.txt`).
  - `H700 total: 42` (`mainline/` 4 + `7.2/` 6 + `devices/H700/patches/linux/` 32; `stage-a/order-H700.txt`).
  - `SM8550 total: 65` (`mainline/` 4 + `7.2/` 6 + `devices/SM8550/patches/linux/` 55; `stage-a/order-SM8550.txt`).
- **The header census over the 106 `.patch` files:**
  - `patches 106 with From: 87 with Subject: 89` (19 without `From:`, of which 17 are hand-made diffs with neither `From:` nor `Subject:`, and 2 carry `Subject:` with `From:` stripped: SM8550 `0121` and `0612`).
  - 4 rows carry `Link:` or `Upstream-Status:`:
    - `projects/ROCKNIX/devices/H700/patches/linux/0160-phy-sun4i-usb-disable-the-clock-that-was-enabled.patch:11:Link: https://lists.infradead.org/pipermail/linux-arm-kernel/2026-July/1145685.html`
    - `projects/ROCKNIX/devices/SM8550/patches/linux/0006-add-hw_params-callback-function-to-drm_connector_hdmi_audio_ops.patch:35:Link: https://patch.msgid.link/20250925040530.520525-1-dmitry.baryshkov@linaro.org`
    - `projects/ROCKNIX/packages/linux/patches/7.2/0011-thermal-adc-tm5-drop-iio-val-int-check.patch:19:Link: https://patch.msgid.link/20260724-adc-tm5-drop-iio-val-int-check-v1-1-730d6f050794@linaro.org`
    - `projects/ROCKNIX/packages/linux/patches/7.2/0016-drm-msm-dp-return-0-from-audio_prepare-when-cable-is-disconnected.patch:12:Upstream-Status: Backport [https://lore.kernel.org/r/20260616151252.2750298-1-quic_aiquny@quicinc.com]`
- **Byte identity against `c445081a59` (merge base) and `651150fc88` (upstream):**
  ```text
        1 vs c445081a59 ABSENT
      106 vs c445081a59 SAME
        2 vs 651150fc88 ABSENT
        4 vs 651150fc88 CHANGED
      101 vs 651150fc88 SAME
  ```
- **The two `.patch.disabled` files and the symlink check:**
  - Two `.patch.disabled` files sit beside the live patches (`H700/patches/linux/0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled`, 4,036 lines; `SM8550/patches/linux/0053-add-hynitron-touchscreen.patch.disabled`, 20,593 lines); neither matches `*.patch` in `unpack` and they belong to T27 and T28 (ruling (o); L-10).
  - Under the member roofs, `git ls-tree -r HEAD | awk '$1=="120000"{print $4}'` prints 3 ALSA UCM `.conf` symlinks under `RK3566` and `SM8750` filesystem overlays (`aw88166.conf`, `rk817_hp.conf`, `SM8750-KONKR.conf`); none is a `patches` directory, so #1056's symlink gap moves no row of the 107 (L-23).

## The rules read

Read at `f03b64419f` (never edited; D-WORKFLOW-189, T4's read #651):

- `.claude/rules/packaging-and-patches.md:76-93` (`:91` carries *"Kernel patches live under `packages/linux/patches/<DEVICE>/`"*, naming the dead generic directory — L-09, inherited by the coordinator).
- `CLAUDE.md:143-149` and `AGENTS.md:151-159` (`CLAUDE.md:149` and `AGENTS.md:159` carry the same `packages/linux/patches/<DEVICE>/` sentence alongside T37 L-18's `patches/<arch>/` and `devices/<DEVICE>/patches/<pkg>/` addition).
- `.claude/rules/device-builds.md:19-31`, `:627-636`, `:689-690` (shipped H700 and SM8550, test GENERIC_X64; `make kconfig-menuconfig-<DEVICE>` writes the tree's conf and never runs here).
- `.claude/rules/handheld-evidence.md:24-25`, `:63-91`, `:109-113` (watchdog 15 s, hang sysctls, H700 ramoops 1 MiB at `0x4F000000`, 512 KiB console, four 128 KiB dumps, `max-reason = <2>`).
- `.claude/rules/engineering-practices.md` (§ Check upstream early D-WORKFLOW-162; § Consider contributing D-WORKFLOW-164/165; § Verify design intent; § A name is not a behaviour; § Guards must fail closed; `rc=$?` on its own line; widened credential mask).
- `.claude/rules/upgrade-and-install.md` (*attribute honestly*: `unknown` is a value the table carries; `Already written:` on every bug).
- `.claude/rules/vm-first.md`, `.claude/rules/bugs-are-agent-first.md`, `.claude/rules/issue-tracking.md`, `.claude/rules/decision-register.md`, `.claude/rules/learning-capture.md`, `.claude/rules/ceremonies.md`, `.claude/rules/time-to-play.md`, `.claude/rules/working-principles.md`, `.claude/rules/generic-x64-vm-testing.md:1350`.
- `docs/decision-register.md` rows D-SYS-001 to -006, D-QA-008, -023, -028, D-WORKFLOW-033, -050, -123, -162, -164, -165, -184, -185, -187, -188, -189, -198, -209, -215, -217 to -221 (`D-WORKFLOW-221` at `:782`, T41's ownership row), D-CLOUD-068.
- `docs/blindspot-register.md` rows 8, 14, 47, 75.

## The take-up table of § 2

Each item from § 2's take-up table, verified at Stage A (`f03b64419f`):

| Found by | What | Take up as | Stage-A state |
| --- | --- | --- | --- |
| T40's PL-03 (#688 comment 1, `2026-10-25T05:46:50Z`) | None of the 26 overrides behind T40's 50 shadowed rows is a kernel override; all 50 went to #689 | **none** | Verified on #688; cited in `02` |
| T40's two rules for T41 (#687 `:113`; `patches-dead.md:447-451`) | Kernel `PATCH_ARCH` is `TARGET_KERNEL_PATCH_ARCH` (`unpack:130`, `x86` on `x86_64`, `aarch64` on H700/SM8550); 277 generic kernel patches dead because `get_pkg_directory linux` resolves to the override | **read** (L-30) | Verified in `scripts/unpack:127-159`, `config/arch.arm:80`, `GENERIC_X64/options:10` |
| Inventory reach gaps #1049, #1056, #1086, #1101, #879, #1053 | None of the six is a kernel-patch gap | **read** (L-18, L-23) | All 6 issues verified `OPEN`; 0 symlinked `patches` dirs under the roofs |
| Plan's *one diff per kernel config against its base* | H700 conf (`8129` lines) is T27's, GENERIC_X64 conf (`7754` lines) is T11's; SM8550 conf (`8608` lines) has `0` fork lines and `7 7` against `651150fc88` | **read** (ruling (d); L-19, L-27) | All four conf-diff counts run at Stage A (`2609`, `3827`, `17` forced symbols, `7 7` upstream) |
| The ramoops patch (`0950`, `cbf75c0b06`, D-SYS-004, #104) | The one fork-written row (`38` lines), read line by line | **read** (ruling (e); L-16) | Verified `38` lines, `not-in-upstream`, 6 `CONFIG_` lines in H700's conf |
| The tier (`0 fork-own` vs `1 fork-written` by `tier_note`) | Inventory rule tiers all `.patch`/`.conf` as `vendor-carried`; `tier_note` marks `0950` `fork-written` | **read** / **inherited:coordinator** (L-17) | Both figures verified in `block.out` and TSV |
| D-SYS-001 to -006 | Kernel-side evidence decisions; `hang-policy.conf` and systemd drop-in are T11's and T22's | **read** | Verified in `docs/decision-register.md:161-165, 793` |
| Currency against `651150fc88` | `12 A`, `1 D`, `4 M` across the 4 shipped kernel dirs; `101 SAME`, `4 CHANGED`, `2 ABSENT` over the 107; pins unchanged (`7.2`, `7.1.2`) | **read** (ruling (f); L-01, L-02, L-14, L-22) | Verified in `$U` at `651150fc88` |
| #328 (OPEN; D-QA-023, D-QA-028) | SM8550 dispcc warning on stock kernel; `0002` in tree; upstream `7.2/0017` added at `651150fc88` | **read** (L-20) | `#328` verified `OPEN`; `7.2/0017` present in `12 A` |
| U-Boot pairs and #44 / D-WORKFLOW-033 | `u-boot-DDR3` and `u-boot-DDR4` patch pairs byte-identical | **read** (L-12; **inherited:T27**) | Both `cmp` runs printed `identical DDR3/DDR4` |
| `0154-rocknix-dt-id.patch` | Read by T27, T13, T25; `bootloader/update.sh` consumer; L15 open | **read** (L-25; **inherited:T27**) | Ready for Stage-B row |
| `0105-drm-panel-Add-Retroid-Pocket-Nova-panel.patch` | Adds the Nova's panel `il97680a,rpnova` | **read** (L-26) | Ready for Stage-B row |
| The `.patch.disabled` files (T27 PL-06, T28 PL-06) | `1` in H700, `1` in SM8550; not `*.patch` | **none** beyond context sentence (ruling (o); L-10) | Counted (`1 disabled` each) |
| The one-line discrepancy (`40,474` vs `40,473`) | `0004-drm-msm-a6xx-Enable-IFPC-on-Adreno-740.patch` has no trailing newline (`33` vs `32`) | **read** (L-24) | Named above in § Scope |
| #369 (Parked) and #585 | Ramoops upstream offer parked in #369; `#585` line owed, never sent | **read** (ruling (e); L-16) | `#369` and `#585` verified `OPEN` |
| Rules' kernel-patch sentence (`packaging-and-patches.md:91`, `CLAUDE.md:149`, `AGENTS.md:159`) | Names dead `packages/linux/patches/<DEVICE>/` | **inherit** (`inherited:coordinator`, ruling (k); L-09) | Line numbers verified at `f03b64419f` |
| #1084, #1083, #836, #796 (T11's) | GENERIC_X64 conf header `6.15.6`, whole-firmware install, stamp, `MAC80211_HWSIM` | **none** (cited in Q2 and firmware row) | All 4 issues verified `OPEN` |
| #704, #1110, #1099, #563, #559, #585, #1071, #1072 | Context issues | **none** or **name, do not act** | States verified `OPEN` at Stage A |
| #1054's acceptance for T41 (`:28-29`) | Five columns and two checks | **read** (§ 7) | Incorporated in § 7 |
| Area futro's asks and kickoff addendum (`docs/futros/2026-10-25-m6-patches-and-configs.md:202`) | Added by the coordinator at `d7dd766659` | **read** | Present in tree at `f03b64419f` |
| D-WORKFLOW-185, -187, -189, -198, -209, -162, -164, -165, -221 | Bounds reach, no-edit rule, upstream column, and T41 ownership | **read** | Verified in `docs/decision-register.md` |
| Device slices' retros (T11, T27, T28, T25) | No extra T41 items beyond those above | **none** | Branch tips and read commits verified present |
