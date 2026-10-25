# Analysis — M6.P2 T28, the SM8550 device (Retroid Pocket Nova) (#675)

## Executive summary

- **What it read.** 29 paths, 28,053 lines and 1,570,286 bytes of `projects/ROCKNIX/devices/SM8550/`, at `8ebaf8daad`, all upstream's and all shipped on the Nova. No fork author has touched the directory since the base.
- **One file is 89 % of the bytes and 73.4 % of the lines:** a patch disabled at birth.
- **The lead answer (Q4): the Nova's whole boot path is superseded upstream.** Upstream replaced it between 2026-10-01 and 10-24, with `cafbb1657d`'s Boot Loader Spec at the core: `rocknix-abl` absent, `mkbootimg` deleted, `openabl` 1.2, dtbs under `dtbs/`, and a loader entry named from `DISTRONAME`. Every unit is *settled by the next base merge*, and what that merge must answer is #1099's.
- **The pins:** two differ (`extra-firmware`, `inputplumber`), two are absent (`rocknix-abl`, `mkbootimg`), and three are identical. The configuration is 7 / 7 against upstream's copy, all toolchain stamps and two flips, with 0 fork lines.
- **Q3 has one reading and no bug.** SM8550's six firmware entries are installed as files, never embedded in the kernel as SM8250, SM8650 and SM8750's are. The unit reaches an active frontend (device facts L17, L18), so this is a divergence, observed working.
- **Q7: the directory does not say how its device boots.** The tree is one of fourteen appended, the selection is undeclared, and no runbook section exists (#1100).
- **Four corrections to the brief:**
  - two InputPlumber files serve the Nova (`02-ayn-controller.yaml:44` matches its model line);
  - the Nova's include chain is part of the shipped unit;
  - r08's pairs are reversed;
  - `gamepadcalibration`'s file differs upstream in SM6115's branch.
- **Eight findings: 2 Low, 6 Info. No `bug`, and nothing proposes a removal.**
- **Nothing ran on the Nova; no guest, no build, no fetch.**

## Acceptance-criteria scorecard

#675's seventeen criteria (= brief § 7), at stage C before the punch-list issue. *Met* names its artifact; *waits* names the stage that ticks it.

| # | Criterion | State |
| --- | --- | --- |
| 1 | `00` and `01` to `05` | met at stage C |
| 2 | the lint `PASS` | pre-issue at stage C; resolution waits for stage H |
| 3 | `review-plan.json` independent, one reviewer; provenance on probe and refutation; the manifest with sha256s and 0 hits | stage C (`second-opinions/`) |
| 4 | every punch item at a Phase 7 outcome; `box-check` 0 fail | waits: stage D onward |
| 5 | `reviewed-at:` and `fixed-at:`; the 29 at `8ebaf8daad`'s bytes; nothing under `packages/`, `projects/` or `tools/` at A to D | the diffs are empty now (r03, r31); the header lines wait for stage H |
| 6 | `01` § Scope | met (`18f6d0b228`) |
| 7 | the coverage table, 29 rows under `## Coverage` | met: the brief's `awk` and `grep` print 29 |
| 8 | § The pins, 8 rows | met (generated) |
| 9 | § The configuration | met |
| 10 | § The loader and the tree, with the lines quoted, the device facts and upstream's commits with #1099 | met |
| 11 | § The device trees, 16 rows plus the `.disabled` row | met (generated) |
| 12 | § The runs, every § 5 command with exit, wall time, figure and *a FAIL would mean* | met (generated, 31 rows) |
| 13 | `00` shows no guest, build, handheld command, M7 read or extra keyed call | met through stage B; stage C adds the two keyed calls only |
| 14 | `04` § Q4, Q3, Q6, Q7 and § Second opinion | Q1 to Q7 met; § Second opinion at stage C |
| 15 | every proof's cell; every punch item's `question:`; every `bug` passes `box-check` | 14 proofs at stage B (15 with the seat's); `05` at stage C; no `bug` |
| 16 | the retro | waits: stage G |
| 17 | the five checkers | waits: stage H |

## Risk assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| The base merge brings BLS onto the Nova without both ABL slots' state and the entry's identity read first | Medium | High | #1099 owns it; the merge notes carry it (F-01) |
| A person flashes a truncated `/flash/rocknix_abl` ELF left by a failed update copy | Low | High | unchecked `update.sh:22`; `updateabl` does not read it; README's manual path only (F-04) |
| A bad ELF reaches both ABL slots at once | Low | High | T1's `updateabl:72-73`; L19 is the keep-an-eye-on; a design note for T1 |
| A model rename silently drops the Nova's quirks and InputPlumber layout | Low | Medium | both key on `"Retroid Pocket Nova"`; unchanged at `651150fc88` (`03` § 3.5) |
| SM8550's GPU firmware is absent from the root filesystem | Low | High | the list dies on a missing pattern at build (`kernel-firmware/package.mk:57`); observed working (F-03) |

## Coverage boundary

- **Read in full:** the 29 paths; `update.sh` line by line; the eight pin recipes at both hashes; the kernel recipe's `qcom-abl` branch and embed condition; `scripts/mkimage`'s branch; `projects/ROCKNIX/bootloader/mkimage`'s SM8550 branches; `bootloader/install`; `config.xml:130-145`; the two `distributions/ROCKNIX/config/functions` routines; `updateabl:1-77` (T1's, for the hand-off); upstream's `update.sh`, `arm-efi` and `config.xml` line; the seven device-facts rows.
- **Not read:**
  - the configuration's 8,608 lines beyond its diff, and the 55 live patches (T41's);
  - the quirks (T29's);
  - `updateabl` as a unit (T1's);
  - the M7 build cache, named and never opened.
- **Not checked:** an author's current release, the dtbs' built sizes and how the ABL selects a dtb, because they need a network, a build or the unit. They are `CANNOT` here.

## Second opinion

*Written at stage C (the seat's probe and refutation).*

## Finding Verification

Each finding re-derived from the tree after it was written (Phase 4.5):

| Finding | Re-derivation | Verdict |
| --- | --- | --- |
| F-01 | r29; `cafbb1657d`'s files at `651150fc88`: `config.xml:134`, `update.sh`, `arm-efi/package.mk:13-23`; `mkbootimg` and `rocknix-abl` absent (r12) | confirmed |
| F-02 | r12, r13, r14; `gamepadcalibration`'s diff (`48b98a02d7`, SM6115's branch); the generic `kernel-firmware` `20260622` | confirmed, with the delta |
| F-03 | r19; `kernel-firmware/package.mk:39-70`; the four confs' `DRM_MSM=y`, `EXTRA_FIRMWARE=""`; SM8550 named only in the version case at both hashes; L17, L18 | confirmed |
| F-04 | `update.sh` whole; `updateabl:7-36`; upstream's `update.sh` (0 `rm`, unchecked copies); README `:1-6` | confirmed |
| F-05 | `functions:226-231`; `:392-396`; r24; `config.xml:130-145`; no SM8550 runbook (#1100) | confirmed |
| F-06 | r05; `scripts/unpack:150-159` | confirmed |
| F-07 | `02-ayn-controller.yaml:44`; `rpnova.dts:8,11`; `rp6.dts`'s include; the 13 trees' models | confirmed, with the correction |
| F-08 | `git grep rocknix-u-boot` (one branch, five inert properties); `config.xml:130`; `functions:384-400`; upstream's `bootloader/mkimage` (0 mentions) and `config.xml:134` | confirmed |

Narrowings made while writing:
- The brief's `install:50-60` was first read as `scripts/install`. It is `projects/ROCKNIX/bootloader/install:50-61`.
- `kernel-firmware`'s die line is `:57` within `:39-70`, not `:58` within `:39-68`. Both corrections were made before commit.

## Renovation face

### Q1 Modernize

- **`update.sh`'s state:**
  - `:10-14` computes `BOOT_DISK` and nothing uses it;
  - `:17`'s remount and `:22`'s copy are unchecked;
  - `:27-31` is a cleanup marked *"REMOVE IN THE FUTURE"*.
- **The guard is `updateabl`'s, not the call's.** `:25` runs it unconditionally, and `updateabl:9-36` refuses a foreign device, a missing ELF and missing partitions; `:60-73` writes only on a difference (F-04).
- **`bootloader/mkimage:22-26`'s `rocknix-u-boot.img` branch** has no producer (F-08).
- **The fourteen-tree boot image** is a selection the trees do not declare (F-05).
- **Each is a design sentence, and the next base merge answers most of them.** Upstream's `update.sh` still leaves its copies unchecked.

### Q2 Standards

- **The `.disabled` patch:** 73.4 % of the slice, never matched by `scripts/unpack`'s globs (F-06).
- **The other boards:** 13 trees and 7 input files are AYANEO's and AYN's, carried by placement (D-WORKFLOW-185). The Nova's chain and its two InputPlumber files are the shipped unit (F-07).
- **Elsewhere:** `HW_CPU="Snapdragon 8 Gen2"` is settled by `471a2711ce`. `device-builds.md:25`'s mixed row is #1094's, cited.
- **No `pkgcheck` row:** the slice has no `package.mk`.

### Q3 Bugs

**None.** The one reading is F-03, quoted from both sides:
- **The list:** `config/kernel-firmware.dat` lists six entries, installed by `kernel-firmware/package.mk:39-70` into the image's firmware directory.
- **The embed:** the kernel recipe embeds firmware only for `"SM8250" -o "H700" -o "SM8650" -o "SM8750"` (`:83`), in the blocks at `:208-277`. No line names SM8550 outside the version case, at either hash.
- **Observed working:** all four confs build `DRM_MSM=y` with an empty `EXTRA_FIRMWARE`, and the unit reaches an active frontend (L17, L18).
- **#836** is the stamp issue for this `.dat`, cited.

`update.sh`'s hand-off makes `updateabl` write nothing it should not: the ELF and the device come from the same new tree, and the missing cases refuse (F-04). **Nothing ran on the Nova.**

### Q4 Package currency

- **The pins** (`02` § The pins, generated):
  - `qcom-abl` `1.0`, identical;
  - `rocknix-abl` `1.2`, **absent upstream** (openabl `1.0` `71d8932b33`, `1.1` `a5d0dd4d57`, `1.2` `73ffb8ee37`); its sha set by the fork's `9aa7affee9`;
  - the kernel `7.2`, the same pin;
  - `mkbootimg` **deleted** (`cafbb1657d`);
  - `extra-firmware` **differs**;
  - `kernel-firmware` `20260309`, identical (and three months behind the generic `20260622`);
  - `inputplumber` **differs** (`v0.79.0` prebuilt to `0.82.0` from source);
  - `gamepadcalibration`: the same pin, the file differing only for SM6115.
  - The authors' releases are `CANNOT (no network)`; `tools/fork-package-freshness` is the RC's check.
- **The configuration:** 7 / 7 against upstream's copy (toolchain stamps, `CC_HAS_COUNTED_BY_PTR` / `INPUT_POLLDEV`, `RAID6_PQ_BENCHMARK`), 0 fork lines, upstream's four commits. T41's row.
- **The trees:** the Nova's chain is unchanged at `651150fc88`. The panel and RP6 patches are T41's.
- **The path as a whole: *settled by the next base merge***, every unit of the `qcom-abl` boot path, with **#1099** cited for what the merge must answer (both ABL slots, `pixelelated.conf`).

### Q5 Efficiency

- **The slice: 1,570,286 bytes.**
  - The `.disabled` patch is 1,402,545 bytes (89.3 %), 20,593 lines.
  - The sixteen trees are 138,992 bytes, 6,267 lines.
  - The nine input files are 25,308 bytes, 1,067 lines.
  - `options`, `update.sh` and the `.dat` make up the rest.
- **The boot image** carries fourteen dtbs. Their built size needs a build (`CANNOT` here). The trees' source bytes, 138,992, are a proxy, not a bound, because a dtb also carries mainline's `qcs8550.dtsi` and the PMIC includes.
- **The configuration's distance** from the other Qualcomm configurations (r08): SM8650 41/36, SM8750 81/105, SM6115 228/133, SM4450 229/189, SM8250 371/204. A fact for the coordinator's parameterisation question, not a proposal.

### Q6 Dead ends

One disposition per unit (the coverage table carries each row's):

| Unit | Paths | Disposition |
| --- | ---: | --- |
| The Nova's tree and include chain (`rpnova.dts`, `rp6.dts`, `ayn-common.dtsi`) | 3 | shipped unit |
| The Nova's InputPlumber files (`02-ayn-controller.yaml`, `ayn_mcu.yaml`) | 2 | shipped unit |
| The other boards' trees | 13 | carried by placement (D-WORKFLOW-185) |
| The other boards' input files | 7 | carried by placement (D-WORKFLOW-185) |
| `options`, `bootloader/update.sh` | 2 | shipped; superseded upstream, *settled by the next base merge* (#1099) |
| `config/kernel-firmware.dat` | 1 | shipped; F-03's reading, no change |
| `patches/linux/0053-...patch.disabled` | 1 | disabled at birth, upstream's; its removal is #346's class decision |
| `bootloader/mkimage:22-26` and `:81-83` (outside the slice, read) | — | never run for SM8550; settled by the next base merge |

**Removals: none.**

### Q7 Clarity and structure

**No: a reader cannot tell from the directory how the Nova boots** (F-05).
- **Which ELF, and from where:** `rocknix_abl` reaches `/flash` and both ABL slots through `rocknix-abl`'s recipe, `update.sh` and T1's `updateabl`, outside the directory.
- **Which tree:** one of fourteen appended to one `kernel.gz` by the kernel recipe. No tree declares a dt-id, and the ABL's selection is written nowhere.
- **Where it is written down:** only `rocknix-abl/sources/README:1-6`, an Android-side manual flash. **#1100** owns the missing runbook section.
- Upstream's BLS change makes the tree explicit (`dtbs/`) and the entry readable, after the merge.
- **The `vm-first` answer for every device fact:** the seven rows named, nothing new asked of the unit.

## Instruction File Recommendations

### Coverage gaps (would have prevented)

- **None for a defect.**

### Codification gaps (proposals for the coordinator)

1. **Device briefs:** a file's ownership by device is read from its match rules, not its name. `02-ayn-controller.yaml` is the Nova's by its `model` match, though its name says AYN.
2. **Briefs that cite a short path name the file.** `install:50-60` meant `projects/ROCKNIX/bootloader/install`, while `scripts/install` exists too.

## Quality self-check

- **Blindspot 13 (assumed done):** each scorecard row names its artifact; nothing is ticked on a file's existence.
- **Blindspot 22 (a probe that cannot report absence):** each § The runs row says what a FAIL would mean, and the dt-id read's `|| true` keeps a 0 from reading as a failure.
- **Blindspot 31 (a harness that writes and reads through the same wrong path):** the update hand-off was read from both sides, `update.sh` and `updateabl`, not from either's comment.
- **Blindspot 46 (a name read as a behaviour):** F-07's correction is this blindspot caught. `02-ayn-controller.yaml` is the Nova's by its match rule, though its name says AYN.
- **Blindspot 51 (a checklist from open boxes):** the scorecard is #675's seventeen, read at dispatch.
- **Blindspot 75 (a corpus read on the wrong tree):** every figure is a command at `8ebaf8daad`. The device-facts rows were checked identical at `2174265e9c` and `8ebaf8daad`. Two citations were corrected after reading the file they named.
- **Rules read this session:** `engineering-practices.md`, `device-builds.md`, `packaging-and-patches.md`, `upgrade-and-install.md`, `release-candidates.md`, `bugs-are-agent-first.md`, `issue-tracking.md`, `vm-first.md`, `adversarial-council.md`, `decision-register.md`. Decisions: D-WORKFLOW-185, -195, -209, -123, D-QA-015, D-QA-027.
