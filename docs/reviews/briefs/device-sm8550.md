# Brief: M6.P2 T28, the SM8550 device (Retroid Pocket Nova) (#675)

**Version 2, 2026-10-25, the coordinator's** (D-WORKFLOW-189; version 1 the same day, corrected by a stranger's proof -- fifteen corrections, listed at the end). Written from a read-only research digest taken at `2174265e9c` (P1's tip; for these paths
the same bytes as `next` at `8ebaf8daad` and as the `20261001` base
`c445081a59`: the directory is identical at all three) and from T27's brief,
the model device slice. The stranger's proof of version 1 ran before dispatch (ten commands, from the scratch clone); this version records what it found. Every number below was pasted from a command's
output at the hash named beside it; the lane re-derives each one and writes
the delta where it differs.

## 1. Identity

- **Issue:** #675 `M6.P2 E1082/T28: devices: the SM8550 device (Retroid
  Pocket Nova)`, slice `device-sm8550` (`k: 28`) in `docs/reviews/slices.json`
  (one `select` rule: globs `projects/ROCKNIX/devices/SM8550/**`, area
  `devices`), twenty-eighth in `docs/reviews/order.md` (its § T28 paths
  line: *"29 paths, 28,053 lines, 118 read, of which 0 fork-own; 0 patch
  and config lines; reach shipped 29"*; its `why`: *"a shipped test
  device"*; kind currency, lens cost against value). **Epic:** #1082 (the
  devices: T11 #658 accepted, T27 #674 accepted and closed out, T25 #672
  running, this slice last). **Milestone:** M6. **Predecessors:** #346,
  #641, **T27 #674** (`docs/reviews/briefs/device-h700.md`: the shape of a
  device slice -- the pin table, the configuration read as a diff against
  upstream's copy, the loader-and-tree section, the DTS-by-unit table, its
  § Errata), **T11 #658** (the boot-file table in its `02` § The boot
  files; errata F-09: a merge of `next` keeps GENERIC_X64 in the kernel
  override's version case), **T1 #648** (`updateabl` is T1's file: cited
  by path and line, never re-read as this slice's), **T29 #676** (the
  quirks: `platforms/SM8550/` and `devices/Retroid Pocket Nova/`, the
  fork's only SM8550 code), **T41 #688** (the 55 live kernel patches and
  the configuration under this directory are its rows), **T5 #836** (the
  firmware embed's stamp), and the coordinator's Backlogs **#1099**
  (upstream's 2026-10-22 Qualcomm boot change at the next base merge) and
  **#1100** (the runbook's missing SM8550 section). **Beside it:** T25 in
  the T5 session, T22 in the T1 session, T15's queue in the T3 session
  (D-WORKFLOW-190); none shares a path with this slice.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346 or #585, or decide a question of scope:
  those are the coordinator's, reached through #675, one question at a
  time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves, with its trace and `Already
  written:` line (D-WORKFLOW-187). A fix lands only under a stream brief
  the coordinator writes at the stage-D pause. **Removal is never proposed
  for an upstream-carried unit** (D-WORKFLOW-209).
- **One worktree, one session.** Branch `feature/m6-device-sm8550-675` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-device-sm8550-675`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at `2174265e9c`** (`docs/reviews/{order.md,slices.json,inventory.json,status.md}` are there and on no other branch) with the coordinator's tip merged in (D-WORKFLOW-209, the device briefs, the devices futro and T27's errata live only there) and the lane's pointer
  seeded; the two hashes are in the dispatch comment on #675. Until that
  comment exists the pointer is not seeded, the first command's `cat`
  fails, and nothing starts. The session is whichever of the T1 and T3
  lanes is idle first after its current slice (T22, T15's queue); the
  dispatch comment names it; its earlier worktrees stay idle beside this
  one, read with `git show` only.
- **Depth: Independent** -- one seat, GPT-6 Astra at `max`, over a trimmed
  packet (D-WORKFLOW-195: scanned with `tools/forbidden-terms-check
  --stdin`, the pre-commit patterns and T10's widened set read with `git
  show feature/m6-tooling-guards-657:.githooks/secret-patterns`, a manifest
  with sha256s), a probe first, as T27's stage C; `review-plan.json`
  records depth `independent`, one reviewer; **exactly one keyed
  `tools/council/run invoke` pair** (the probe and the refutation), every
  other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`,
  `--help` included (T13's rule break, #1044). The T27 folder's
  `second-opinions/` is the model (its plan, manifest, probe, refutation
  and provenance files; read with `git show feature/m6-device-h700-674:docs/audits/2026_10_25-epic-m6-device-h700/second-opinions/<file>`).
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the worktree):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-device-sm8550-675
cat .github/sessions/saved-session-state-feature-m6-device-sm8550-675.md       # the pointer: the dispatch's two hashes
git status --short | wc -l                                                      # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                  # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
tools/register-check >/dev/null && echo register-ok; grep -c 'D-WORKFLOW-209' docs/decision-register.md
```

## 2. Scope

**The membership block** (T25's shape; the slice's one rule is a glob and
the area):

```bash
python3 -I - <<'PY'
import json, collections, os
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
t28 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "devices"
       and r["path"].startswith("projects/ROCKNIX/devices/SM8550/")]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t28), "lines", L(t28), dict(collections.Counter(r["reach"] for r in t28)), dict(collections.Counter(r["tier"] for r in t28)))
print(dict(collections.Counter(r["language"] for r in t28)))
CODE = {"shell", "recipe", "udev", "python", "c", "make"}
rd = [r for r in t28 if r["language"] in CODE and r["tier"] != "vendor-carried" and r["reach"] != "unreached"]
print("read", len(rd), L(rd), "fork-own", sum(1 for r in rd if r["tier"] == "fork-own"))
alld = [r for r in rows if r["tree"] == "distribution" and r["path"].startswith("projects/ROCKNIX/devices/SM8550/")]
print("whole directory in the inventory", len(alld), L(alld), dict(collections.Counter(r["area"] for r in alld)))
os.makedirs(".qa-scratch/t28", exist_ok=True)
open(".qa-scratch/t28/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t28, key=lambda r: r["path"])))
for r in sorted(t28, key=lambda r: r["path"]): print(r["reach"], r["tier"], r["lines"], r["path"])
PY
wc -l .qa-scratch/t28/paths.txt     # 29
```

Recorded (2026-10-25, at `2174265e9c`; the inventory there was generated at
`eb4763e3cc`): **29 paths, 28,053 lines; reach shipped 29; upstream-carried
29, fork-own 0; read 2 files / 118 lines / 0 fork-own** (`options` 81 and
`bootloader/update.sh` 37; the language rule reads no DTS); languages shell
2, other 3, yaml 8, devicetree 16. The whole directory holds 85 inventory
rows / 57,561 lines: the other 56 are `patches-and-configs` rows (the
8,608-line `linux/linux.aarch64.conf` and the 55 live patches, 20,899
lines), T41's -- which is why the order says *"0 patch and config lines"*
and this slice, unlike T27's, does **not** take the configuration into its
membership (the configuration shape is still read, one line and one diff,
under Q4, cited as T41's row).

**The 29, by weight.** `options` 81; `bootloader/update.sh` 37;
`config/kernel-firmware.dat` 8 (6 entries); `filesystem/` 9 files / 1,067
(`10-ayaneo.hwdb` 3; four inputplumber `capability_maps/*.yaml` 252 / 252 /
28 / 257; four `devices/*.yaml` 71 / 65 / 89 / 50 -- every one AYANEO's or
AYN's, none the Nova's); `linux/dts/qcom/` 16 files / 6,267 (two `.dtsi`:
`qcs8550-ayaneo-pocket-common.dtsi` 1,504 and `qcs8550-ayn-common.dtsi`
1,767; fourteen `.dts`, among them `qcs8550-retroidpocket-rpnova.dts` 35,
`qcs8550-retroidpocket-rp6.dts` 391 and `-rp6-top-dpad.dts` 17); and
**`patches/linux/0053-add-hynitron-touchscreen.patch.disabled`, 20,593
lines = 73.4 % of the slice**, born at that name (`aa458af6f9`,
2026-06-29, *"linux: bump SM8550 to 7.1.2"*), still upstream, never read by
`scripts/unpack` -- T27's `.disabled` disposition transfers. No
`package.mk`, no udev rule, no device `bootloader/mkimage` under the
directory: **every pin this slice reads lives in a recipe outside it**,
cited by path.

**The pins (8 rows, T27's shape; both hashes read locally):**

| Unit | Recipe (outside the slice) | At `8ebaf8daad` | At `651150fc88` | Set by |
| --- | --- | --- | --- | --- |
| `qcom-abl` (`options:34 BOOTLOADER="qcom-abl"`) | `projects/ROCKNIX/packages/tools/qcom-abl/package.mk` (11 lines, a meta recipe) | `PKG_VERSION="1.0"`, `PKG_URL=""`, no sha | identical | `7a656ea09d` 2026-01-29 |
| `rocknix-abl` (`options:66 ADDITIONAL_PACKAGES`) | `projects/ROCKNIX/packages/tools/rocknix-abl/package.mk` (18 lines) | `1.2`, sha `64034fb076ea...4cff7`, `github.com/ROCKNIX/abl/releases/download/v1.2/`; installs `usr/share/bootloader/rocknix_abl/abl_signed-${DEVICE}.elf` | **absent** -- replaced by `openabl` (`1.0` at `71d8932b33` 2026-10-14, `1.1` at `a5d0dd4d57`, `1.2` at `73ffb8ee37` 2026-10-24) | the version by `b354bfe6d6` 2026-09-30; **the sha by the fork's `9aa7affee9`** (blitterbot, 2026-10-15, #600, mirroring upstream's `15123b2951`) -- a fork identity on one pin recipe, outside the slice |
| the kernel | `projects/ROCKNIX/packages/linux/package.mk:29-35` (`H700|SM4450|SM6115|SM8250|SM8550|SM8650|SM8750)`) | `7.2`, sha `f9fef3d14c0d...402b3` | identical | the case line's commit |
| `mkbootimg` (the fork's host tool, `package.mk:19` for `SM*`) | `projects/ROCKNIX/packages/tools/mkbootimg/package.mk` | `d2bb0af5ba6d3198a3e99529c97eda1be0b5a093`, sha `418bb875...` | **deleted** (`cafbb1657d`) | `7a656ea09d` (the sha by `e0a68c95bd`) |
| `extra-firmware` (`options:63 FIRMWARE`) | `projects/ROCKNIX/packages/linux-firmware/extra-firmware/package.mk` (`:20 "SM8550") cp -a SM8550/*`) | `88b363e67d4f730feb2c3124724d26dfaa88ce76` | `925dfb5efbe5d6c3ca654f81e3e1f367f8492777` (**differs**) | `675c364c6d` 2026-09-13 |
| `kernel-firmware` (the ROCKNIX override) | `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk` | `20260309` | identical (the generic `packages/linux-firmware/kernel-firmware` is `20260622` at both: the override is three months behind -- cite, outside the slice) | (the lane reads) |
| `inputplumber` (`options:66`) | `projects/ROCKNIX/packages/tools/inputplumber/package.mk` | `v0.79.0`, a prebuilt tarball | `0.82.0`, built from source (**differs**) | (the lane reads) |
| `gamepadcalibration` (`options:66`) | `projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk` | `2077e7af7e...` | identical | (the lane reads) |

`CANNOT (no network)` for every author's current release: that check is
`tools/fork-package-freshness`'s at the RC (D-WORKFLOW-024) and is named,
not run.

**The configuration** (T41's row, read here as T27 read H700's): 8,608
lines, line 3 `# Linux/arm64 7.2.0 Kernel Configuration` against the
recipe's `7.2`; against upstream's copy at `651150fc88` **7 removed / 7
added** (compiler stamps gcc 16.2.0 against 15.2.0, RUSTC and LLVM
versions, `CC_HAS_COUNTED_BY_PTR=y` against `# INPUT_POLLDEV is not set`,
`RAID6_PQ_BENCHMARK`); **fork non-merge commits since the base: 0**;
upstream's four since (`dcafa74090` 10-22, `6fbefc45c6` 10-18,
`5f56cd5150` 10-04, `c0980b2b71` 10-02 -- the same four as H700's); added
whole by `9f1fab30f6` (2025-07-13, +8,154); tier `vendor-carried`, no
*fork-written* note. Its distance from the other Qualcomm configurations at `8ebaf8daad` (`diff <(git show 8ebaf8daad:<this conf>) <(git show 8ebaf8daad:<other conf>) | grep -c '^<'` and `'^>'`: removed / added): SM8650 36 / 41, SM8750 105 / 81, SM6115 133 / 228, SM4450 189 / 229, SM8250 204 / 371 -- a Q5 fact, not a proposal. (The T41 rows' lines sum to 29,508 in the inventory against 29,507 by `wc -l`: one patch without a trailing newline.)

**The loader and the tree (the boot path at `8ebaf8daad`).** The kernel recipe's `qcom-abl` branch (`projects/ROCKNIX/packages/linux/package.mk:387-404`, the body `:389-403`) gzips the Image, **appends every built dtb into `kernel.gz`** (`:392-396`),
adds a dummy ramdisk and runs `mkbootimg.py` with the LABEL command line
into `.image/Image`; `scripts/mkimage:257-266` is the `qcom-abl` branch (T27's erratum: `:21-23` computes `DISK_SIZE`), sourcing
`projects/ROCKNIX/bootloader/mkimage`, whose `mkimage_all`
(`distributions/ROCKNIX/config/functions:384-400`) runs the `config.xml`
steps -- for SM8550 **only `mkimage_abl`** (`bootloader/mkimage:108-111`,
which mcopies `rocknix_abl`); the `mkimage_uboot` branch naming *"SM8750, SM8650 & SM8550"* (`bootloader/mkimage:22-26`, `rocknix-u-boot.img`) has no producer and is gone upstream; `mkimage_dtb()`'s `SM8550|...)` case (`bootloader/mkimage:81-83`, copying `3rdparty/bootloader/boot`) is a second SM8550-naming branch for Q1 and Q6 to read. `config.xml:130-145` (`<SM8550
mkimage_options="abl" dtb_prefix="qcom">`) lists **14 `<file>` entries =
all fourteen `.dts`, the Nova's included**; no tree carries a
`rocknix-dt-id`, and how the ABL selects the Nova's tree from the fourteen
appended is a Q7 design question (device fact L17: it boots). `install:50-60`
is the designed echo branch (T11's F-09; the futro at :208-213). On an
update, `bootloader/update.sh` (37 lines, last changed `18d890d349`
2026-06-06): `:12` computes `BOOT_DISK` for `mmcblk` and never uses it;
`:19-23` copies `rocknix_abl/*` to `/flash/rocknix_abl`; **`:25` runs
`updateabl` unconditionally** -- `rocknix/sources/scripts/updateabl` (77
lines, T1's) finds `abl_a` and `abl_b` by PARTLABEL, compares sha256 and
`dd`s the ELF into both slots when either differs (`:64-73`; device fact
L17 recorded both slots written on 2026-10-12); `:27-31` removes
`/flash/boot` and `/flash/EFI` (*"REMOVE IN THE FUTURE"*); `:37` writes
`.boot.hint`. **Upstream replaced this path between 2026-10-01 and 2026-10-24** (18 commits on the directory, `scripts/mkimage`, `rocknix-abl` and `openabl` in `8ebaf8daad..651150fc88`: `0340192729` 10-01 adds ` gpt` to the command line; `71d8932b33` 10-14 openabl `1.0`; `cafbb1657d` 10-22 Boot Loader Spec entries, `BOOTLOADER="arm-efi"`, `mkimage_options="abl,bls,dtb"`, dtbs under `usr/share/bootloader/dtbs`, the kernel recipe without mkbootimg, `update.sh` +12; `7842b3b429` `update.sh` -6, to 43 lines; `471a2711ce`; `73ffb8ee37` 10-24 openabl `1.2`; `scripts/mkimage` at `651150fc88` still carries one `qcom-abl` mention): every unit of the path above is *settled by the next base merge*, and that merge's `Already written:` and identity seam (the loader entry upstream's `virtual/arm-efi` recipe writes -- `packages/virtual/arm-efi/package.mk` at `651150fc88`, its post_install read and the entry's name quoted by the lane; it is in no file under `scripts/`, `projects/ROCKNIX/bootloader/` or the kernel recipe) are **Backlog #1099**, the coordinator's -- cited, not re-filed.

**The device trees (16).** The Nova: `model = "Retroid Pocket Nova"`,
`compatible = "retroidpocket,rpnova", "qcom,qcs8550", "qcom,sm8550"`,
`#include "qcs8550-retroidpocket-rp6.dts"` (which includes
`qcs8550-ayn-common.dtsi`, then mainline's `qcs8550.dtsi` and `pm8550*.dtsi`);
its panel `il97680a,rpnova` comes from patch 0105 (T41's); touchscreen
1280x960 (D-WORKFLOW-114); added `3c3ac4f4ee` 2026-07-26. The other
thirteen `.dts` and both `.dtsi` are AYANEO's and AYN's boards: *carried
by placement* (D-WORKFLOW-185), built into every SM8550 boot image.

**History and delta.** Over the 29, `git log --no-merges --format='%h %an'
--since='2026-06-01T00:00:00Z' 8ebaf8daad -- $(cat paths)`: **24
non-merge commits (27 with merges), fork 0, upstream 24**; over the whole
directory 54 / 63, fork 0 (a bare `--since=2026-06-01` printed 52: T27's
erratum, reproduced). `git log --no-merges 651150fc88..8ebaf8daad -- projects/ROCKNIX/devices/SM8550` is **empty** (without `--no-merges` it lists the fork's two upstream merges, `7bd7f31312` and `7650de7dd6`): no fork author has touched the directory since the base. The upstream delta over the 29: **2 M** (`update.sh` and `options`,
+20 / -14); over the directory 4 M + 2 A (the conf, patch 0104, and two
new panel-calibration patches 0508/0509, +451 / -22). `Makefile:39,42,98-101` (in `world`, `arm` then `aarch64`); `config/options:31` defaults `DEVICE="SM8550"` (`:28-30` are a blank, a comment and the `if`). **The fork's only SM8550 code is outside the slice**:
`quirks/devices/Retroid Pocket Nova/bin/{analog_sticks_ledcontrol,battery_led_status,ledcontrol}`
(45 / 135 / 83 lines, #332's), T29's rows.

**Device facts** (`docs/releases/device-facts.md` at `2174265e9c`, cited by the Fact cell and the line at that hash, never re-asked; D-QA-015; the table has no ID column, so a row is named by its Fact cell): line 17 (the Nova's boot after the 2026-10-12 update, both ABL slots written), 18 (frontend readiness after #529), 19 (shutdown and bootloader recovery, #558, keep an eye on), 20 (Tailscale after restart), 27 (the Nova), 28 (the sign-in window's pad, #331: InputPlumber hides the AYN Odin2 Gamepad node), 31 (the stick LEDs, #332, an open item to test). The lane quotes each Fact cell beside the line. No
runbook section exists for the SM8550 (**Backlog #1100**); the only
written flash procedure is `rocknix-abl/sources/README:1-6`.

**What is not here, and where it is:** the configuration and the 55 live
patches (T41, #688); the quirks (T29, #676: `platforms/SM8550/` 24 files,
`devices/Retroid Pocket Nova/` 4 files); `updateabl` (T1, #648); the pin
recipes (`tools/qcom-abl`, `tools/rocknix-abl`, `tools/mkbootimg`, the
kernel, `extra-firmware`, `kernel-firmware`, `inputplumber`,
`gamepadcalibration`: T11's, T8's and T23's rows, cited by path); the M7
lane's build cache `m7-signin-sm8550-build-20261025-01` (named, **never
read**: a pin is read from the tree, D-INFRA-025).

## 3. Read first

- `.github/sessions/saved-session-state-next.md` and this lane's own pointer.
- **The rules this work touches** (`working-principles.md` § Pre-flight):
  `engineering-practices.md` (§ Verify the artifact; § A name is not a
  behaviour; § Nothing runs on a person's device without their yes;
  § Consider contributing every applicable fix upstream), `device-builds.md`
  (§ Our devices -- the Nova's row at line 25 is #1094's; § Installing on
  the device; § After rebasing item 3), `packaging-and-patches.md`,
  `upgrade-and-install.md` (`Already written:`; § Current cloud setup
  policy does not apply), `release-candidates.md` (step 0),
  `bugs-are-agent-first.md`, `issue-tracking.md`, `vm-first.md`,
  `handheld-evidence.md`, `adversarial-council.md` (the seat),
  `council-substrate-integrity.md`, `worktrees.md` (superseded by § 1).
- The code-auditor skill whole; *the plan* is `docs/reviews/plan-for-the-plan.md`
  (§ 4 the questions, § 6b the renovation face, § 6c the depth rule).
- **T27's brief and audit** (`docs/reviews/briefs/device-h700.md` on the
  coordinator's branch, merged into this worktree; the audit on
  `feature/m6-device-h700-674`: `git show feature/m6-device-h700-674:docs/audits/2026_10_25-epic-m6-device-h700/02-forward-audit.md`
  for § The pins, § The configuration, § The loader and the tree, § The
  device trees, § The runs; its `second-opinions/` for the seat's shape).
  **T11's audit** (`git show feature/m6-device-generic-x64-658:docs/audits/2026_10_25-epic-m6-device-generic-x64-and-kernel/02-forward-audit.md`
  § The boot files). Every ref is in the shared repository; no fetch.
- `docs/reviews/order.md` § T28 and § 1 item 4; `docs/futros/2026-10-25-m6-devices.md`
  (its T28 kickoff addendum, and :208-213 on the echo branches, :218-233
  T27's errata, :265-266 what T28 inherits).
- `docs/qa-logs/2026-10-15-sm8550-abl-format/`, `2026-10-12-nova-shutdown/`,
  `2026-10-13-nova-*` (the evidence behind L17 to L19: read, not re-made).
- `docs/blindspot-register.md` entries **13**, **22**, **31**, **46**,
  **51**, **75**.
- Decisions: D-QA-023 (the Nova under SM8550, #150), D-QA-028, D-QA-031,
  D-UI-121, D-WORKFLOW-114 (the 1280x960 panel), D-WORKFLOW-150,
  D-WORKFLOW-185, 187, 189, 195, 209, D-INFRA-025/026, D-QA-015, D-QA-027.
- Issues: #675, #1082, #674, #658, #648, #676, #688, #836, #1099, #1100,
  #1094, #150, #332, #558, #346. Every `gh` call carries
  `--repo pixelelated/distribution`.

## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`design`); the lens is currency, so Q4 leads:

- **Q4 Package currency -- the lead question.** The eight pins of § 2: the
  pin at `8ebaf8daad`, at `651150fc88` (three differ, one is absent, one is
  deleted upstream), the setting commit, and `CANNOT (no network)` for the
  author's release. The configuration's currency: its 7 / 7 against
  upstream's copy, each line attributed (compiler stamps, two option
  flips), 0 fork lines. The DTS currency: the Nova's include chain against
  the 7.2 tree (the patches that add the boards are T41's, named). **And
  the path's currency as a whole:** every unit of the `qcom-abl` boot path
  is superseded by upstream's 2026-10-22 change; the disposition is
  *settled by the next base merge* with #1099 cited for what that merge
  must answer (both ABL slots, the loader entry's name).
- **Q1 Modernize.** `update.sh:12`'s `BOOT_DISK` computed and never used;
  `:25`'s unconditional `updateabl` run (the write is conditional inside
  `updateabl:64-73`: read both and say which is the guard); the dead
  `rocknix-u-boot.img` branch in `bootloader/mkimage:22-26`; the fourteen
  trees appended into one boot image (a byte cost and a selection the
  trees do not declare) -- each a design sentence for the coordinator, no
  edit; the next base merge answers most of them.
- **Q2 Standards.** The `.disabled` patch (73.4 % of the slice, never read
  by the build); the fourteen AYANEO/AYN trees and the nine AYANEO/AYN
  filesystem files under a directory whose shipped unit is the Nova (a
  placement reading, D-WORKFLOW-185, not a removal); the Nova's row in
  `device-builds.md:25` mixing the two builds' CPUs and the arm FPU (#1094,
  cited, not re-filed); `HW_CPU="Snapdragon 8 Gen2"` against upstream's
  *"Snapdragon 8 Gen 2"* (`471a2711ce`, settled by the merge).
- **Q3 Bugs.** `updateabl`'s compare-and-write of both slots is T1's file:
  read here only for what `update.sh` hands it; a `bug` with its trace
  only if `update.sh` makes it write a loader it should not (a missing
  ELF, a wrong `${DEVICE}`), and its `Already written:` names L17's two
  slots. The `kernel-firmware.dat` list (6 entries: `rtl_nic/rtl8153a-4.fw`,
  `qca/hmtbtfw20.tlv`, `qca/hmtnv20.*`, `qcom/sm8550/a740_zap.mbn`,
  `qcom/a740_sqe.fw`, `qcom/gmu_gen70200.bin`) against the kernel recipe's embed blocks (`:83` the condition naming SM8250, H700, SM8650 and SM8750; `:208-277` the blocks), which name **no SM8550**: a finding with both quoted; cite
  #836 for the stamp; nothing re-filed there. **Nothing runs on the Nova**
  (D-QA-015, D-QA-027).
- **Q5 Efficiency.** The slice's bytes and lines by unit (the one patch
  73.4 %; the sixteen trees 6,267; the nine AYANEO/AYN files 1,067); the
  boot image's size cost of fourteen appended dtbs (`git ls-tree -r -l`
  over the trees as the upper bound; no build); the configuration's
  distance from the other Qualcomm configurations (§ 2's table), a fact
  for the coordinator's parameterisation question, not a proposal.
- **Q6 Dead ends.** The `.disabled` patch (*disabled at birth, upstream's;
  its removal is #346's class decision*); the thirteen other boards' trees
  and the AYANEO/AYN filesystem files (*carried by placement*); the dead
  `rocknix-u-boot.img` branch, `update.sh:12` and `:27-31` (*settled by the
  next base merge*, #1099). Removals none.
- **Q7 Clarity and structure.** Can a reader tell from the directory how
  the Nova boots -- which ELF, which tree of the fourteen, where
  `/flash/rocknix_abl` comes from -- without reading three recipes outside
  it? Is there a written flash and update procedure (#1100: no)? The
  `vm-first` answer for every device fact: the seven rows named, nothing
  new asked of the unit.

A finding is one question with its evidence; `Renovation` is the category
for everything here that is not a defect. The seat (Phase 4.6) grades the
findings and the dispositions; its probe comes first.

## 5. The evidence floor

1. Tracker state is never sole evidence; every cell cites a command's
   output or a file:line at `8ebaf8daad`.
2. Mechanical evidence outranks reading: `diff` counts, `git log` with the
   three fork identities (`Max Engel|blitterbot|rasterabot`), `grep -n` on
   the scripts; a comment is the author's claim (blindspot 31).
3. **The bench is the host; no guest, no build, no unit.** **Can this be
   done on the VM? Yes -- on the host, with no network:** every read, diff,
   log and script read runs on the build host at `8ebaf8daad` with
   `651150fc88` read locally; the GENERIC_X64 guest cannot be an SM8550,
   so **no guest is asked for**, and a fact only the Nova can show is a
   `device-facts.md` row (L17 to L20, L27, L28, L31), read and cited,
   **never produced here** (D-QA-015, D-QA-027: the Nova is a person's).
   `tools/council/run invoke` runs twice with the key, the probe and the
   refutation of the one seat.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.

**What never runs in this slice:** a build, a compiler, a plan generation,
a guest, a fetch, a network read of any upstream or author, a command
against the Nova or any handheld, a read of an M7 build root, a `tools/council/run` call with the key beyond the one seat's probe and refutation, and a change to any file under `packages/`, `projects/` or `tools/` at stages A to D. (A `grep -c` that prints the expected 0 exits 1: the running log's exit column says so where it happens.)

**The runs, with what the coordinator read** (the lane runs each at stage
A and records the exit, the wall time and the summary line; `TMPDIR` under
`/workspace/tmp/m6-t28/`):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-sm8550-675
cd "$D"; export TMPDIR=/workspace/tmp/m6-t28/tmp; mkdir -p "$TMPDIR" .qa-scratch/t28
# the membership block (§ 2) -> .qa-scratch/t28/paths.txt (29)
wc -l < .qa-scratch/t28/paths.txt                                                                     # 29
tr '\n' '\0' < .qa-scratch/t28/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD -- | tail -1        # empty
for p in $(cat .qa-scratch/t28/paths.txt); do printf '%s ' "$(git show "8ebaf8daad:$p" | wc -l)"; done | awk '{s=0; for(i=1;i<=NF;i++) s+=$i; print s}'   # 28053
git show 8ebaf8daad:projects/ROCKNIX/devices/SM8550/patches/linux/0053-add-hynitron-touchscreen.patch.disabled | wc -l   # 20593
# the configuration (T41's row; expect Linux/arm64 7.2.0; 8608; removed 7 added 7; fork non-merge 0; upstream's four)
C=projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf
git show "8ebaf8daad:$C" | sed -n '3p'; git show "8ebaf8daad:$C" | wc -l
git show "651150fc88:$C" > "$TMPDIR/up.conf"; git show "8ebaf8daad:$C" > "$TMPDIR/ours.conf"; echo "removed=$(diff "$TMPDIR/up.conf" "$TMPDIR/ours.conf" | grep -c '^<') added=$(diff "$TMPDIR/up.conf" "$TMPDIR/ours.conf" | grep -c '^>')"
for d in SM8650 SM8750 SM6115 SM4450 SM8250; do O=projects/ROCKNIX/devices/$d/linux/linux.aarch64.conf; printf '%s %s/%s ' "$d" "$(diff <(git show "8ebaf8daad:$C") <(git show "8ebaf8daad:$O") | grep -c '^<')" "$(diff <(git show "8ebaf8daad:$C") <(git show "8ebaf8daad:$O") | grep -c '^>')"; done; echo   # 36/41 105/81 133/228 189/229 204/371
git log --no-merges --format='%h %ad %an %s' --date=short c445081a59..8ebaf8daad -- "$C" | wc -l      # 0
git log --format='%h %ad %an %s' --date=short 8ebaf8daad..651150fc88 -- "$C" | cut -c1-100            # upstream's four
git show 8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk | sed -n '29,35p' | grep -n -E 'SM8550|PKG_VERSION' | cut -c1-120   # 7.2 (grep -n numbers are relative to the window)
git show 651150fc88:projects/ROCKNIX/packages/linux/package.mk | grep -n -E 'SM8550\)|PKG_VERSION="7' | head -3 | cut -c1-120   # the case at :35 there; the version unchanged
# the pins at both hashes (expect: qcom-abl 1.0 twice; rocknix-abl 1.2 then absent; mkbootimg then absent; extra-firmware differs; kernel-firmware 20260309 twice; inputplumber v0.79.0 then 0.82.0; gamepadcalibration identical)
for p in tools/qcom-abl tools/rocknix-abl tools/mkbootimg linux-firmware/extra-firmware linux-firmware/kernel-firmware tools/inputplumber tools/gamepadcalibration; do for h in 8ebaf8daad 651150fc88; do f="projects/ROCKNIX/packages/$p/package.mk"; if git cat-file -e "$h:$f" 2>/dev/null; then printf '%s %s: %s\n' "$p" "$h" "$(git show "$h:$f" | grep -E '^PKG_(VERSION|SHA256|URL)=' | tr '\n' ' ' | cut -c1-200)"; else printf '%s %s: absent\n' "$p" "$h"; fi; done; done | sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'
git log --format='%h %ad %an %s' --date=short -3 -- projects/ROCKNIX/packages/tools/rocknix-abl/package.mk | cut -c1-120   # 9aa7affee9 (the fork, 2026-10-15) and b354bfe6d6
git show 651150fc88:projects/ROCKNIX/packages/tools/openabl/package.mk | grep -E '^PKG_(VERSION|URL)=' | cut -c1-160   # the replacement upstream, 1.2 at 73ffb8ee37
git log --format='%h %ad %s' --date=short 8ebaf8daad..651150fc88 -- projects/ROCKNIX/packages/tools/openabl | cut -c1-100   # 1.0 71d8932b33, 1.1 a5d0dd4d57, 1.2 73ffb8ee37
# the loader and the tree (expect update.sh:12 BOOT_DISK unused; :19-23 rocknix_abl; :25 updateabl; :27-31 rm; mkimage:257-266 the branch; bootloader/mkimage:108-111 abl, :22-26 the dead u-boot branch, :81-83 mkimage_dtb's SM8550 case; config.xml 14 files)
git show 8ebaf8daad:projects/ROCKNIX/devices/SM8550/bootloader/update.sh | grep -n -E 'BOOT_DISK|rocknix_abl|updateabl|rm -rf|boot.hint' | cut -c1-120
git show 8ebaf8daad:scripts/mkimage | grep -n -E 'qcom-abl' | cut -c1-120
git show 8ebaf8daad:projects/ROCKNIX/bootloader/mkimage | grep -n -E 'SM8550|rocknix_abl|rocknix-u-boot' | cut -c1-120
git show 8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk | sed -n '387,404p' | grep -n -E 'dtb|mkbootimg|kernel.gz' | cut -c1-120   # the branch :387-404; grep -n numbers are relative to the window
git show 8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk | sed -n '83p;208,277p' | grep -n -E 'SM8|H700|EXTRA_FIRMWARE|firmware' | head -12 | cut -c1-120   # the embed blocks: no SM8550
git show 8ebaf8daad:projects/ROCKNIX/config.xml | sed -n '130,145p' | grep -c '<file>'                      # 14
git show 8ebaf8daad:projects/ROCKNIX/packages/rocknix/sources/scripts/updateabl | sed -n '60,75p' | cut -c1-120   # T1's file, read for the hand-off only: the compare and the two dd
# the DTS (expect 16; the Nova's model and compatible; no rocknix-dt-id anywhere)
git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/devices/SM8550/linux/dts | wc -l
git show 8ebaf8daad:projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-retroidpocket-rpnova.dts | grep -n -E '#include|model|compatible' | cut -c1-100
for f in $(git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/devices/SM8550/linux/dts); do git show "8ebaf8daad:$f" | grep -c 'rocknix-dt-id' || true; done | sort | uniq -c   # 16 x 0 (grep -c exits 1 on 0; the || true keeps the loop's exit 0)
# the history with the three identities (expect 24 non-merge; fork 0) and the upstream delta (expect 2 M over the 29; 4 M 2 A over the directory)
tr '\n' '\0' < .qa-scratch/t28/paths.txt | xargs -0 git log --no-merges --format='%h %an' --since='2026-06-01T00:00:00Z' 8ebaf8daad -- | tee "$TMPDIR/hist.txt" | wc -l; grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt"
git log --no-merges --format=%h 651150fc88..8ebaf8daad -- projects/ROCKNIX/devices/SM8550 | wc -l      # 0 (without --no-merges: 2, the fork's upstream merges)
tr '\n' '\0' < .qa-scratch/t28/paths.txt | xargs -0 git diff --name-status 8ebaf8daad 651150fc88 -- | cut -c1-120
git diff --name-status 8ebaf8daad 651150fc88 -- projects/ROCKNIX/devices/SM8550 | cut -c1-120
git log --format='%h %ad %s' --date=short 8ebaf8daad..651150fc88 -- projects/ROCKNIX/devices/SM8550 scripts/mkimage projects/ROCKNIX/packages/tools/rocknix-abl projects/ROCKNIX/packages/tools/openabl | cut -c1-110   # 18 commits, 10-01 to 10-24; the boot change among them
# the Makefile and the default device (expect in world; arm then aarch64; config/options:28-30)
grep -n -E '^SM8550:|SM8550' Makefile | head -5 | cut -c1-100; sed -n '28,31p' config/options   # :31 the default DEVICE
# the removal rule's own check against the dispatch tip (expect empty)
git diff --stat <dispatch tip> HEAD -- packages projects tools | tail -1
```

## 6. Outputs

As T27's brief § 6, with the folder `docs/audits/<yyyy_mm_dd>-epic-m6-device-sm8550/`:
`00` to `05`, `second-opinions/` (the seat's plan, manifest, probe and
refutation with provenance), the lint before D, the audit issue (`Audit:
M6 T28 the SM8550 device -- N findings (...)`, a sub-issue of #675), the
bugs, and the retro at `docs/retros/<date>-m6-device-sm8550.md` (what the
devices epic's close inherits: the pin table across the four device
slices, the boot-path table, the device-facts citations). **`02` carries
§ The pins (8 rows), § The configuration (7 / 7, 0 fork lines, cited as
T41's), § The loader and the tree (the boot path by line, the next base
merge's change named with #1099), § The device trees (16 rows: the board,
the include, the `model` line, shipped unit or carried by placement; the
`.disabled` patch's row), § The runs (every § 5 command with exit, wall
time, figure and *a FAIL would mean*), and a coverage table of 29.** The
stage-D pause as T27's: the punch list posted on #675, the lane waits for
the coordinator's dispositions and any stream brief.

## 7. Acceptance

The checklist on #675 becomes this section at dispatch, written there by
the coordinator in place of P1's five generated ones. Every checkbox names
the artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-device-sm8550/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-device-sm8550/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: independent` and one reviewer (`gpt`, `openai/gpt-6-astra`, `max`); the probe's and the refutation's outputs have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named; `packet-manifest.json` lists every packet file with its sha256 and the scan's result (0 hits).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #346, #1099, #1100, #1094, #836, T41's #688, T29's #676, T1's #648), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the ticked and open counts read back by the coordinator.
- [ ] `reviewed-at:` and `fixed-at:` in the checklist's header carry the lane's commits; the read is on `8ebaf8daad`'s bytes for the 29 (`git diff --stat 8ebaf8daad <reviewed-at> -- $(cat .qa-scratch/t28/paths.txt)` empty) and nothing under `packages/`, `projects/` or `tools/` changes at stages A to D (`git diff --stat <dispatch tip> <stage-D tip> -- packages projects tools` empty).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (29 paths, 28,053 lines; read 2 files / 118 lines / 0 fork-own; upstream-carried 29; shipped 29; the whole directory 85 rows, 56 of them T41's), the 16 DTS named as read though not counted, the `.disabled` patch's 20,593 lines, the configuration's diff against `651150fc88`'s copy (7 / 7) with 0 fork lines, the history (24 non-merge, fork 0), the upstream delta (2 M over the 29; 4 M 2 A over the directory) and the 2026-10-22 boot change's commits by hash.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `29`.
- [ ] `02-forward-audit.md` § The pins has one row per pinned unit (`qcom-abl`, `rocknix-abl`, the kernel, `mkbootimg`, `extra-firmware`, `kernel-firmware`, `inputplumber`, `gamepadcalibration`: 8, each recipe by path): the pin at `8ebaf8daad`, at `651150fc88` (identical / differs / absent / deleted, with upstream's replacement and its three versions named where one exists), its setting commits (the version's and the sha's where they differ: `rocknix-abl`'s sha is the fork's `9aa7affee9`), and `CANNOT (no network)` for the author's current release with `tools/fork-package-freshness` named as the RC's check.
- [ ] `02-forward-audit.md` § The configuration states the diff against upstream's own copy (7 removed / 7 added, each line attributed), 0 fork lines since the base, upstream's four commits, the header's `7.2.0` beside the recipe's `7.2`, and that the row is T41's, read here for the shape.
- [ ] `02-forward-audit.md` § The loader and the tree states, with the kernel recipe's, `scripts/mkimage`'s, `bootloader/mkimage`'s (both SM8550 branches) and `update.sh`'s lines quoted, how the Nova gets its ELF (`rocknix_abl`, `updateabl`'s two slots -- T1's file cited by line) and its tree (fourteen appended, the selection undeclared), citing the device-facts rows for the observed boot and the recovery by their Fact cells and lines, and names upstream's October boot change by its commits (`0340192729` to `73ffb8ee37`) with #1099 as its owner; no command against the Nova.
- [ ] `02-forward-audit.md` § The device trees has one row per DTS or DTSI (16): the board, the `#include` target, the `model` line (none for a `.dtsi`), and *shipped unit* (the Nova) or *carried by placement*; the `.disabled` patch's row says *disabled at birth, upstream's, 20,593 lines, never applied* with `scripts/unpack:143-159` cited.
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass.
- [ ] `00-running-log.md` shows no guest, no build, no compiler, no plan generation, no fetch, **no command against a handheld** (`ssh`, `device-act`, `scp` to a unit: 0 hits, or every hit a negation), no M7 build root read, no `tools/council/run invoke` but the one seat's probe and refutation, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent` (`--help` included), and the VM line.
- [ ] `04-analysis.md` § Q4 carries the pin table's verdicts and the boot path's *settled by the next base merge* with #1099; § Q3 the `kernel-firmware.dat` finding with the recipe's embed lines quoted and #836 cited; § Q6 a disposition per unit, removals none; § Q7 the boot-clarity answer and #1100; § Second opinion grades every seat item with the seat's words quoted.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture` or `design`; every punch item carries `question:`; every `bug` passes `tools/box-check --issue N` and carries its `Already written:` line.
- [ ] The retro exists at `docs/retros/<date>-m6-device-sm8550.md`, is posted on #675, says what the slice did to the two time-to-play numbers (nothing) and what the devices epic's close inherits.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge).

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); the stage-D pause; an explicit maintainer pause on
#675; a blocker named on #675 (a seat that fails its provenance gate twice,
two commands that disagree, a block whose output differs from § 2's beyond
the deltas it records); a branch that differs from `8ebaf8daad` on one of
the 29 at stage A; or an execution limit, stated as such with the running
log current. A checkpoint is not a stop. An idle session says it is idle
on #675, **and does not end a turn on a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#675`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #675` or the
  guard.
- The VM question written before any proof (§ 5: yes, on the host; no
  guest; nothing on the Nova).
- The mini-retro at stage G, posted on #675, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 where a fix landed.
- A register row the same session for any decision the slice forces (none
  expected); D-WORKFLOW-209 is the highest Decided row on the coordinator's
  branch on 2026-10-25 (D-WORKFLOW-188 is on the P1 branch only; the merge
  unites them); a row this slice forces takes an ID the coordinator
  assigns on #675.
- `tools/ceremony-check` before every push; never `--no-verify`; a merge
  with conflicts is checked for markers; the ledgers united by whole
  entries; **a commit names its paths**; anything temporary under
  `/workspace/tmp/m6-t28/` after `df -i`, never `/tmp`.
- Commit messages `docs: ...`, with `Refs #675`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#675's checkboxes against their artifacts; the lint's `PASS` line;
`review-plan.json` and both provenance files (read with the current
reader); the audit issue's checkboxes all at an outcome; the coverage
table's row count (29), the pins' (8) and the device trees' (16); every Q6
disposition and no removal; **re-running on a clone of the branch at the
tip under `/workspace/tmp/m6-coordinator/`: the membership block and every
§ 5 run in full**; `register-check` on a simulated merge with the
coordinator's tip (the ledgers united); the retro's answers; the six exit
codes. The lane posts one hand-back comment naming the tip and each
artifact by path, writes `reviewed-at:` and `fixed-at:` into #675's body,
then says it is idle. After acceptance the coordinator closes the audit
issue, prompts the lane for `audit-completion.json` and the full lint,
merges the branch in its turn after the M7 candidate (after T25's),
regenerates the ledgers, and closes #675 when every row is proven.

**The readings before dispatch** (plan § 3, principle 3): the epic's futro
(#1082) carries a T28 kickoff addendum written with this version, and a
stranger's proof of this brief is run by a reader with no context before
dispatch; version 2 records what each found.

## Version 2: what the stranger's proof found (2026-10-25)

Ten commands from the scratch clone at `2174265e9c`; the membership, the
configuration, the trees, the history and the delta held. The corrections:

1. `git log 651150fc88..8ebaf8daad -- <dir>` lists the fork's two upstream
   merges; only `--no-merges` is empty. The prose and the run say so.
2. The pins loop's `|| echo absent` could never fire (a pipeline's exit is
   its last stage's); it tests `git cat-file -e` first now, and carries the
   kernel, `inputplumber` and `gamepadcalibration` entries by path.
3. `rocknix-abl`'s sha was set by the fork's `9aa7affee9` (2026-10-15,
   #600), a fork identity on a pin recipe; openabl went 1.0, 1.1, 1.2 in
   three upstream commits, 1.2 on 2026-10-24.
4. The kernel recipe's `qcom-abl` branch is `:387-404` (the dtb loop
   `:392-396`); the embed-block evidence is `:83` and `:208-277`.
5. `config/options:31` carries the default `DEVICE`, not `:28-30`.
6. The Qualcomm configuration distances were one off each (36/41, 105/81,
   133/228, 189/229, 204/371), now with their command.
7. The T41 rows' line sum differs by one between the inventory and `wc -l`.
8. Upstream's boot change spans 2026-10-01 to 10-24 (18 commits), not one
   day; `update.sh`'s 43 lines are +12 then -6.
9. The two tool recipes and the kernel at `651150fc88` have § 5 commands.
10. A `grep -c` that prints the expected 0 exits 1; the running log's exit
    column says so.
11. `updateabl`'s compare is read as a line window, not a pattern.
12. Device-facts rows are named by their Fact cells and lines at the hash
    (the table has no ID column).
13. `bootloader/mkimage:81-83`, a second SM8550-naming branch, is in the
    read.
14. The loader entry upstream writes is in `virtual/arm-efi`, not under
    `scripts/` or the bootloader directory; `scripts/mkimage` upstream
    still names `qcom-abl` once.
15. `scripts/mkimage`'s `DISK_SIZE` is `:21-23`; mkbootimg's sha came with
    `e0a68c95bd`; where `docs/reviews/*` and the briefs live is said in § 1.
