# Analysis — M6.P2 T28, the SM8550 device (Retroid Pocket Nova) (#675)

## Executive summary

- **What it read.** 29 paths, 28,053 lines and 1,570,286 bytes of `projects/ROCKNIX/devices/SM8550/`, at `8ebaf8daad`, all upstream's and all shipped on the Nova. No fork author has touched the directory since the base.
- **One file is 89 % of the bytes and 73.4 % of the lines:** a patch disabled at birth.
- **The lead answer (Q4): the Nova's whole boot path is superseded upstream.** Upstream replaced it between 2026-10-01 and 10-24, with `cafbb1657d`'s Boot Loader Spec at the core: `rocknix-abl` absent, `mkbootimg` deleted, `openabl` 1.2, dtbs under `dtbs/`, and a loader entry named from `DISTRONAME`. Every unit is *settled by the next base merge*, and what that merge must answer is #1099's.
- **The pins:** two differ (`extra-firmware`, `inputplumber`), two are absent (`rocknix-abl`, `mkbootimg`), and four are identical pins. The configuration is 7 / 7 against upstream's copy: toolchain stamps, two independent option changes, and `RAID6_PQ_BENCHMARK`, a behaviour change. 0 fork lines.
- **Q3: no proven `bug`, and two candidates for the coordinator.**
  - F-04 (Medium): `update.sh` ignores `updateabl`'s failure and reports the update done, and upstream's replacement keeps that shape over files the BLS boot reads. T27's #1095 shape.
  - F-09 (Low, found by the seat): the Nova's touchscreen selects pinctrl for gpio24/25 while using gpio14/15. Its effect is unobserved.
  - F-03, a packaging divergence: none of the six firmware entries is embedded, unlike SM8250, SM8650 and SM8750 (the kernel embeds only `regulatory.db`). Its runtime effect is observed only narrowly (L17, L18).
- **Q7: the directory does not say how its device boots.** The tree is one of fourteen appended. Seven share the Nova's board-id and msm-id, so the selection is the ABL's and written nowhere; on the device the Nova's tree is chosen (D-WORKFLOW-114's 1280x960 panel). No runbook section exists (#1100).
- **Four corrections to the brief:**
  - two InputPlumber files serve the Nova (`02-ayn-controller.yaml:44` matches its model line);
  - the Nova's include chain is part of the shipped unit;
  - r08's pairs are reversed;
  - `gamepadcalibration`'s file differs upstream in SM6115's branch.
- **Nine findings: 1 Medium, 2 Low, 6 Info. No `bug` filed: F-04's disposition is the coordinator's. Nothing proposes a removal.**
- **The seat** (GPT-6 Astra at `max`, PASS): 32 items graded below.
  - 15 confirmed; 10 narrowings accepted; 2 new items accepted; 3 accepted in part.
  - 2 refuted in part by re-reads: G-27, the wrong-family case `init` refuses; G-28, the ELFs' alignment.
  - Its corrections changed F-01, F-02, F-03, F-04, F-05 and F-07, and added F-09.
- **Nothing ran on the Nova; no guest, no build, no fetch.**

## Acceptance-criteria scorecard

#675's seventeen criteria (= brief § 7), at stage C before the punch-list issue. *Met* names its artifact; *waits* names the stage that ticks it.

| # | Criterion | State |
| --- | --- | --- |
| 1 | `00` and `01` to `05` | met at stage C |
| 2 | the lint `PASS` | pre-issue at stage C; resolution waits for stage H |
| 3 | `review-plan.json` independent, one reviewer; provenance on probe and refutation; the manifest with sha256s and 0 hits | met: `second-opinions/` (both provenance files PASS, `council-facilitator@1.14.1-pixelelated.2`; 72 sources; scan 0 hits) |
| 4 | every punch item at a Phase 7 outcome; `box-check` 0 fail | waits: stage D onward |
| 5 | `reviewed-at:` and `fixed-at:`; the 29 at `8ebaf8daad`'s bytes; nothing under `packages/`, `projects/` or `tools/` at A to D | the diffs are empty now (r03, r31); the header lines wait for stage H |
| 6 | `01` § Scope | met (`18f6d0b228`) |
| 7 | the coverage table, 29 rows under `## Coverage` | met: the brief's `awk` and `grep` print 29 |
| 8 | § The pins, 8 rows | met (generated) |
| 9 | § The configuration | met |
| 10 | § The loader and the tree, with the lines quoted, the device facts and upstream's commits with #1099 | met |
| 11 | § The device trees, 16 rows plus the `.disabled` row | met (generated) |
| 12 | § The runs, every § 5 command with exit, wall time, figure and *a FAIL would mean* | met (generated, 31 rows) |
| 13 | `00` shows no guest, build, handheld command, M7 read or extra keyed call | met: two keyed calls (probe, refutation); `--help` and `verify-pins` keyless |
| 14 | `04` § Q4, Q3, Q6, Q7 and § Second opinion | met |
| 15 | every proof's cell; every punch item's `question:`; every `bug` passes `box-check` | 16 proofs; `05` at stage C; no `bug` filed |
| 16 | the retro | waits: stage G |
| 17 | the five checkers | waits: stage H |

## Risk assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| The base merge brings BLS onto the Nova without both ABL slots' state and the entry's identity read first | Medium | High | #1099 owns it; the merge notes carry it (F-01) |
| A failed `updateabl` is reported as a finished update; after the merge, the same shape could leave the old ABL with no Android image | Low | High | F-04, Medium, a candidate bug: the coordinator's call (a #1095-like stream or #1099) |
| A person flashes a truncated `/flash/rocknix_abl` ELF left by a failed update copy | Low | High | unchecked `update.sh:22`; README's manual path only (F-04) |
| The Nova's touchscreen interrupt pin runs without its intended bias | Low | Medium | F-09; effect unobserved; upstream's tree |
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

**Independent, one seat: GPT-6 Astra (`openai/gpt-6-astra`) at `max`**, through the Facilitator on OpenRouter, pinned to OpenAI, `allow_fallbacks: false` (`review-plan.json`).
- **The packet:** `gpt-brief.md`, 72 sources, 377,172 bytes, sha256 `90fdaca720aa5fa8...`, scanned 0 hits (`packet-manifest.json`).
- **The probe:** 10:46:28 to 10:46:38 UTC, `PASS`.
- **The refutation:** 10:46:53 to 10:58:08 UTC, attempt 1/4, `http=200`, 26,619 reasoning tokens, `finish=stop outcome=success`. Verification, effort and provider `PASS`; `council-facilitator@1.14.1-pixelelated.2`.
- **Exactly two keyed calls** were made in this slice. Each item is graded against a re-read (`stage-c/rereads/rereads.sh`, c01 to c07), with the seat's words quoted.

| Item | The seat's label and words | Grade, and what changed |
| --- | --- | --- |
| G-1 | confirmed: *"four unchanged pins, not three"* | **confirmed**: my count was wrong; F-02 and the summary say four identical pins |
| G-2 | confirmed: `rocknix-abl` absent, `mkbootimg` deleted | **confirmed** |
| G-3 | confirmed: two pins differ; InputPlumber's *"packaging contract"* changes | **confirmed**, the packaging note added to Q4 |
| G-4 | narrowed: *"the selected boot route is superseded, not literally every unit or defect"* | **narrowed, accepted**: F-01 now says the source moves with the merge; the fourteen-tree list and the unchecked updater survive |
| G-5 | confirmed: *"the BLS filename is an identity-sensitive seam"* | **confirmed**; `disk=LABEL=STORAGE` added (c07) |
| G-6 | new: *"the merge must establish a coherent migration, not just names and slot contents"* | **accepted**: the four migration questions are named in F-01 for #1099 |
| G-7 | narrowed: *"`INPUT_POLLDEV` is not a compiler-capability line and is not replaced by `CC_HAS_COUNTED_BY_PTR`"* | **narrowed, accepted**: c01 shows `25d24` and `2728a2728`; § The configuration corrected |
| G-8 | confirmed: *"the RAID6 change is behavioural, not a toolchain stamp"* | **confirmed**: § The configuration and Q4 say so |
| G-9 | narrowed: *"fourteen targets are requested; exactly fourteen appended artifacts are not guaranteed"* | **narrowed, accepted**: a warm tree's stale `.dtb` would be appended; § The loader says so |
| G-10 | confirmed: only `mkimage_abl` | **confirmed** |
| G-11 | narrowed: the guards *"do not establish that the declared family matches the physical handheld ... or make the parent honor a failure"* | **narrowed in part**: the parent's failure is F-04's. The family check is `init:341-368`'s (c05), outside the packet |
| G-12 | confirmed: the card copy is a manual-flash input | **confirmed** |
| G-13 | narrowed: *"'observed working' has a much smaller scope"* | **narrowed, accepted**: F-03 quotes L18's own disclaimer |
| G-14 | confirmed: *"a documented early, cached firmware failure exists -- cfg80211"* | **confirmed** (c02): F-03's "embeds none" corrected to none of the six `.dat` entries, with `regulatory.db` embedded |
| G-15 | confirmed: the two InputPlumber files serve the Nova | **confirmed**; its `ds5` / `ds5-edge` comment note is the seat's, not re-read |
| G-16 | confirmed: RP6 and AYN common are Nova dependencies | **confirmed**, with its caveat that the other trees are still built |
| G-17 | narrowed: *"not universally unreachable"*; the hwdb rule *"could match an attached device named `AYANEO DEVICE*`"* | **narrowed, accepted** in F-07 |
| G-18 | narrowed F-01 | **accepted** (with G-4, G-6) |
| G-19 | confirmed F-02 | **confirmed** |
| G-20 | narrowed F-03 | **accepted** |
| G-21 | refuted F-04's *"not a bug"* | **accepted in part**: F-04 is regraded Medium, a candidate bug. *"destructive continuation"* is narrowed, because the removed `/flash/boot` and `/flash/EFI` are not read by the `qcom-abl` boot |
| G-22 | narrowed F-05: *"the shown BLS entry ... names a kernel and options, but no `devicetree`"* | **narrowed, accepted**: the first draft's "makes the tree explicit" withdrawn |
| G-23 | confirmed F-06 | **confirmed** |
| G-24 | narrowed F-07 | **accepted** |
| G-25 | confirmed F-08 | **confirmed** |
| G-26 | new: *"the root updater can report success after critical failure"* | **accepted**, merged into F-04, with `init:427-440`'s *"Boot Files Updated."* |
| G-27 | new: *"the hand-off trusts image identity, not hardware identity"*; *"no such caller is supplied"* | **refuted in part** (c05): `init:341-368` cancels an update whose `HW_DEVICE` is incompatible with the running system's, and `init:430-431` exports `SYSTEM_ROOT`. The residue, image identity rather than hardware probing, is T1's and `init`'s design, noted |
| G-28 | new: hashes `ceil(ELF_SIZE/ss)` sectors against `ELF_SIZE` bytes, *"a conditional correctness defect"* | **refuted for the shipped payloads** (c06): every cached `abl_signed-SM8550.elf` is 258,048 bytes, aligned to 512 and 4,096, and the 1.2 archive matches the recipe's sha256. Latent for a future ELF: a lead for T1 (`updateabl`) |
| G-29 | narrowed: no undefined label demonstrated | **agreed**; no finding |
| G-30 | new: *"the Nova inherits a touchscreen pinctrl mismatch"* | **confirmed** (c03): new F-09, Low, effect unobserved |
| G-31 | new: the ` gpt` argument is *"a boot-policy difference rather than a toolchain stamp"* | **accepted**: named in F-01 for the merge |
| G-32 | new: *"the available identifiers do not uniquely select the Nova"* | **confirmed** (c04): seven trees share the board-id and msm-id. F-05 strengthened; the device selects the Nova's tree in practice (D-WORKFLOW-114's 1280x960 panel) |

**Tally (32, each once):**
- **15 confirmed:** G-1, 2, 3, 5, 8, 10, 12, 14, 15, 16, 19, 23, 25, and the new G-30 and G-32.
- **10 narrowings accepted:** G-4, 7, 9, 13, 17, 18, 20, 22, 24, 29.
- **2 new items accepted:** G-6, G-31.
- **3 accepted in part:** G-11, G-21, G-26.
- **2 refuted in part by re-reads:** G-27 (`init:341-368`), G-28 (the ELFs' alignment).

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
| F-09 | c03: `rp6.dts`'s `touchscreen@38` GPIOs 14/15 against `ts_p_*` = gpio24/25 in `ayn-common.dtsi`; Thor uses `ts_s_*`; `rpnova.dts:22-27` overrides size and inversion only | confirmed (found by the seat) |

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

**No `bug` filed; two candidates for the coordinator.**
- **F-04 (Medium):** `update.sh:25` ignores `updateabl`'s exit (1 on a missing ELF, partitions or sector size, `updateabl:24-40`). `:27-37` carry on and write `UPDATE`, and `init:427-440` prints *"Boot Files Updated."* whatever happened. Upstream keeps the shape over the BLS files. T27's #1095 shape: a stream or a #1099 requirement, the coordinator's call.
- **F-09 (Low):** the Nova's touchscreen pinctrl names gpio24/25 for gpio14/15 pins, in an upstream tree. Its effect is unobserved.

**The design question PL-04 leaves for the coordinator, in one sentence:** should SM8550's six `config/kernel-firmware.dat` entries be embedded in the kernel as its three Qualcomm siblings' are (`linux/package.mk:83`, `:208-277`; `CONFIG_DRM_MSM=y` on all four), given that the runtime is *observed only narrowly* (device-facts lines 17 and 18) and #836 already owns the `.dat`'s stamp? No change is made, and nothing is asked of the Nova.

F-03, quoted from both sides:
- **The list:** `config/kernel-firmware.dat` lists six entries, installed by `kernel-firmware/package.mk:39-70` into the image's firmware directory.
- **The embed:** the kernel recipe embeds firmware only for `"SM8250" -o "H700" -o "SM8650" -o "SM8750"` (`:83`), in the blocks at `:208-277`. No line names SM8550 outside the version case, at either hash.
- **The one embed SM8550 does get:** `regulatory.db` and its `.p7s`, for `CONFIG_CFG80211=y` (`:93-97`, `:293-302`), because a built-in `cfg80211` asks during kernel init and caches the failure (the seat's G-14).
- **Observed only narrowly:** all four confs build `DRM_MSM=y`, and the unit reaches an active frontend (L17, L18; L18 disclaims a rendering proof).
- **#836** is the stamp issue for this `.dat`, cited.

**The hand-off.** `update.sh` hands `updateabl` the new tree's ELF and family. `init:341-368` refuses an incompatible update first, and the cached ELFs are sector-aligned (G-27, G-28 refuted in part). What is wrong is the report, not the payload (F-04). **Nothing ran on the Nova.**

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
- **The configuration:** 7 / 7 against upstream's copy, 0 fork lines, upstream's four commits. T41's row.
  - toolchain stamps ×5 pairs;
  - `CC_HAS_COUNTED_BY_PTR` added and `INPUT_POLLDEV` dropped, independently;
  - `RAID6_PQ_BENCHMARK` off upstream, a behaviour change at kernel init.
- **The trees:** the Nova's chain is unchanged at `651150fc88`. The panel and RP6 patches are T41's.
- **The path as a whole:** the `qcom-abl` boot path's source moves with the next base merge. **#1099** owns what the merge must answer:
  - both ABL slots;
  - `pixelelated.conf`;
  - a coherent first boot with `rocknix_abl` left beside `openabl`;
  - failure handling (F-04);
  - DTB selection (no `devicetree` in the entry);
  - the ` gpt` argument.
  - Narrowed by the seat's G-4 and G-6.

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
- **Which tree:** one of fourteen appended to one `kernel.gz` by the kernel recipe. No tree declares a dt-id, and seven share the Nova's `qcom,board-id` and `qcom,msm-id`, so an identifier match cannot pick it. On the device the Nova's tree is selected (D-WORKFLOW-114's 1280x960 panel), by the ABL's rule, written nowhere.
- **Where it is written down:** only `rocknix-abl/sources/README:1-6`, an Android-side manual flash. **#1100** owns the missing runbook section.
- Upstream's BLS change moves the dtbs under `dtbs/`, but its entry names no `devicetree`, so the selection stays implicit after the merge (the seat's G-22).
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
