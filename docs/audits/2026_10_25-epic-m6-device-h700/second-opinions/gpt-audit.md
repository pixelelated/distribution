Citation shorthand: `H/` = `projects/ROCKNIX/devices/H700/`; `R/` = `projects/ROCKNIX/`; `D/` = `H/linux/dts/allwinner/`. Citations are at `8ebaf8daad` unless marked otherwise; **E6** means `feature/m6-build-engine-652`.

## 1. The pins and the atf seam

**G-1 — narrowed — Unchanged versions do not mean unchanged source identities.** Evidence: `H/packages/u-boot-DDR3/package.mk:5-9`, `H/packages/u-boot-DDR4/package.mk:5-9`, `H/packages/u-boot/package.mk:5-8`, `H/packages/h700-suspend-stub/package.mk:5-9`, `R/packages/linux/package.mk:29-32`, `R/packages/tools/atf/package.mk:17,28`; upstream atf `:17-18,29`.

The supplied comparison reports unchanged version/revision pins, and the two atf excerpts independently establish that H700 remains at 2.12.0. However, upstream copies of the other pinned recipes are not supplied, so their equality is reported context rather than a two-revision comparison I can independently reproduce here. Atf’s URL and digest identity change, so “every pin unchanged” needs that qualification; none of these literals establishes currency against the authors’ latest releases. Also, the project atf fallback is **2.10.0**, not 2.15.0—the latter assertion concerns a separate, unprovided generic recipe (`R/packages/tools/atf/package.mk:22-25`; upstream `:23-26`).

**G-2 — confirmed — H700 lacks a checksum here; upstream adds one and changes the fallback checksum.** Evidence: `R/packages/tools/atf/package.mk:15-28`; upstream `:15-29`; E6 `:15-29`.

The H700 branch at the audited commit assigns no `PKG_SHA256`; the checksum in `*)` is not inherited by the H700 case. Upstream adds H700’s `d95aaf29…`, replaces the fallback’s `696b8e53…` with `6b1d5e89…`, and changes the shared URL to `TrustedFirmware-A/trusted-firmware-a`. Strictly, upstream does not *replace an existing H700 checksum at the audited commit*: its new checksum differs from E6’s `30abf4da…`, which is paired with the old `ARM-software` URL.

**G-3 — confirmed — The checksum-pairing hazard is real.** Evidence: E6 `R/packages/tools/atf/package.mk:17-29`; upstream `:17-29`; E6 `scripts/get_archive:7-9,49-61`.

For the recorded **H700/2.12.0 archive bytes**, the coherent pairs are old URL + `30abf4da…` and new URL + `d95aaf29…`; crossing those digests produces a mismatch. For the recorded **fallback/2.10.0 archive bytes**, the pairs are old URL + `696b8e53…` and new URL + `6b1d5e89…`; crossing them likewise mismatches. A missing checksum fails before either cache or network access, whereas unsuccessful checksum verification of downloads eventually exhausts the retry loop and fails.

**G-4 — narrowed — “The fetch refuses” is not unconditional for a mixed URL/checksum pair.** Evidence: E6 `scripts/get_archive:11-23,39-65`; E6 atf `R/packages/tools/atf/package.mk:18,29`.

The cache fast path checks the stored checksum **stamp**, not the archive bytes or the contents of the URL stamp, so a matching cached old archive can satisfy a recipe carrying a changed URL. The mirror fallback can also supply bytes matching the selected checksum even when the primary URL does not. Thus the crossed-pair failures in G-3 concern the recorded archive bytes, not an immutable relationship between a URL spelling and bytes—redirects and mirrors matter. E6 demonstrably pairs the fork checksum with the old URL, but its computation and the repository-name explanation are reported provenance, not calculations independently established by these excerpts.

## 2. The configuration

**G-5 — narrowed — All 25 changed lines are accounted for; exact commit attribution is not independently shown.** Evidence: `H/linux/linux.aarch64.conf:5,7,14-16,2783,3656,7290-7292,7744,7975-7979`; upstream configuration `:25`.

The accounting is complete: eleven lines for the fork’s six additions against five removals, five GCC-related lines, two RAID6 lines, five LLVM/`INPUT_POLLDEV` lines, and two Rust-version lines. The reader gets the values and diff directions right, including `INPUT_POLLDEV` being present only in the fork’s copy. However, the endpoint diff cannot establish which commit introduced each change; the named commits require their patches or blame, which are not supplied. Calling everything except RAID6 a “toolchain refresh” also obscures that `CONFIG_INPUT_POLLDEV=y` is a configuration-symbol difference, not merely a compiler-version string.

**G-6 — narrowed — Upstream’s H700 copy is the appropriate comparison base; “fork-written” is misleading as whole-file authorship.** Evidence: `H/linux/linux.aarch64.conf:1-6` and the supplied diff at `:5-7979`.

The small same-path diff supports comparing this configuration with upstream’s H700 configuration, rather than rebasing it conceptually onto an unrelated device configuration. On the supplied provenance, describing the entire file as fork-written is an erratum: the fork contribution is the six explicit settings, not authorship of the whole generated configuration. The diff itself establishes proximity, however, not the historical introduction commit or the inventory’s intended meaning of “fork-written.”

**G-7 — narrowed — No inconsistency in the six settings is demonstrated, but the rest of the configuration is not available to clear them.** Evidence: `H/linux/linux.aarch64.conf:3656,7290-7292,7975-7979`; `docs/releases/device-facts.md:29`.

The hung-task timeout is paired with an enabled hung-task detector, and none of the six displayed additions contradicts another displayed addition. The packet does not include the remaining dependency settings or the resulting normalized build configuration, so it cannot establish that every requested symbol survives Kconfig processing. Enabling watchdog interfaces, detectors and pstore support also does not by itself prove panic policy, a functioning watchdog, or retained ramoops data; the cited device-facts row explicitly leaves the H700 observation open. I would neither file a configuration contradiction from these excerpts nor accept an unconditional “all six are effective” conclusion.

## 3. The loader and the tree

**G-8 — narrowed — The shown fresh-image generator does not activate a root-level `dtb.img`; the complete entry-point trace is missing.** Evidence: `R/config.xml:3,24`; `R/bootloader/mkimage:18-21,33-59,73-95,113`; `docs/releases/device-facts.md:15-16`.

The XML selects `dtb,extlinux,uboot`, names `dtb.img`, and adds the DDR3 overlay; the generated extlinux path references that name, while the H700 loader branch writes only the raw bootloader and `mkimage_dtb` copies the tree directory. No displayed project-generator line selects a board DTB and copies it to the boot filesystem’s `/dtb.img`. However, `scripts/mkimage`, the definition of `mkimage_all`, and any supplied custom extlinux files are absent, so the reader’s whole-pipeline “nothing writes it” assertion is not independently complete here. The two device-facts rows describe in-place updates, not a fresh-card experiment closing that gap.

**G-9 — refuted — The universal voltage fail-safe claim assumes variables are initially unset.** Evidence: `H/bootloader/update.sh:35-55`.

With initially unset variables, an ordinary empty or unrecognized reading selects no loader, while exactly 1,200,000 and 1,100,000 select DDR3 and DDR4 respectively. But neither `VDD_REG_PATH` nor `UBOOT_BIN` is initialized or cleared: an inherited DDR3 `UBOOT_BIN` survives an unrecognized voltage or missing regulator and passes the write gate, including on a hypothetical DDR4 unit. The read’s exit status is also ignored; selection examines its output rather than requiring a successful read. The reader is therefore wrong that “no input makes it write a loader it should not.”

**G-10 — narrowed — A non-`mmcblk` boot device is not explicitly rejected.** Evidence: `H/bootloader/update.sh:7-16,52-63`.

When `BOOT_DISK` is initially unset and `BOOT_PART` is not `/dev/mmcblk*`, the script leaves the destination empty but can still enter the loader-writing branch. That produces `dd … of=`, normally an open failure—not a deliberate safe skip, and not a write to stdout. Its error and status are discarded, after which the script still writes the update hint; a pre-existing nonempty `BOOT_DISK` instead bypasses discovery altogether.

**G-11 — narrowed — A missing dt-id normally preserves the old DTB, but is not explicitly validated or reported.** Evidence: `H/bootloader/update.sh:21-32`.

A failed or missing-property read normally makes the candidate path `device_trees/.dtb`; it skips the copy only because that file normally does not exist. There is no explicit nonempty-ID check, successful-read check, or requirement that the selected file was successfully refreshed by the preceding copy. Consequently, retaining the previous `dtb.img` is the ordinary fallback, not proof that the entire update is fail-safe: tree and overlay copying has already been attempted, and this failure is not reported to the caller.

**G-12 — confirmed — The F-11 correction of the project loader branches is right.** Evidence: `R/bootloader/mkimage:18-26,73-89`.

The H700 branch ends with the raw `dd` at line 21. The following `elif`, including the tree copy at line 26, is the Qualcomm branch; H700’s directory copy is the default branch of `mkimage_dtb` at line 88.

## 4. The SIMD flags

**G-13 — narrowed — The code is authoritative about the declared build settings; the table mixes flag dialects.** Evidence: `H/options:7-18`; `.claude/rules/device-builds.md:19-23`.

The aarch64 branch declares `+crc+fp+simd`, whereas `crypto-neon-fp-armv8` belongs to the arm branch’s `TARGET_FPU`. As a description of the aarch64 build flags, the table is misleading; as a hardware-capability description, it is unproved by these lines. The first reader’s recommendation to “name the arch” is itself wrong—the table already explicitly says **aarch64**. Neither that table nor the absence of an explicit `+crypto` here establishes the hardware’s crypto capabilities or every downstream package’s effective compiler flags.

**G-14 — new — Two different checks would settle the build-policy and hardware questions.** Evidence: `H/options:9-17`; `.claude/rules/device-builds.md:22-23`; `docs/releases/device-facts.md:15-16,29`.

The build-policy question needs the final compiler invocations and effective target-feature/macros from the pinned toolchain, including any package overrides—not just the device defaults. The hardware question needs an authorized device-facts record of the relevant CPU features/HWCAP on the two units; the supplied rows do not record them. Neither check has been performed here, and the appropriate immediate correction is to distinguish aarch64 flags, arm compatibility flags and observed hardware capabilities rather than prescribe `+crypto` from the table.

## 5. Verdicts on F-01 through F-11

**G-15 — narrowed — F-01.** Evidence: `R/packages/tools/atf/package.mk:17,24,28`; upstream `:17-18,24-29`; other pin locations in G-1.

No supplied evidence shows a version bump, but atf’s fetch identity changes and the other upstream recipe copies are not present for independent comparison. “Current with the reported upstream version pins” is supportable; “identical pinned inputs” or “current with the authors’ releases” is not.

**G-16 — narrowed — F-02.** Evidence: E6 `R/packages/tools/atf/package.mk:17-29`; upstream `:17-29`; E6 `scripts/get_archive:7-23,39-65`.

The missing checksum and coherent-pair merge requirement are real. Narrow the failure guarantee as in G-4, and do not attribute E6’s fail-closed implementation to the audited commit: the supplied fetch implementation is explicitly from another branch.

**G-17 — narrowed — F-03.** Evidence: `H/options:7-18`; `.claude/rules/device-builds.md:19-23`.

The architecture-specific documentation mismatch stands. The table already names the architecture, however, and a missing explicit crypto flag is not proof of an incorrect compiler setting or missing hardware capability.

**G-18 — narrowed — F-04.** Evidence: `R/config.xml:3,24`; `R/bootloader/mkimage:33-59,73-95`; `H/bootloader/update.sh:26-31`.

The displayed normal generator references an unactivated DTB name, and the updater supplies an activation path. Confirm that local gap, but reserve the universal fresh-image/nonboot conclusion until the missing top-level generator and any custom boot configuration are inspected.

**G-19 — narrowed — F-05.** Evidence: `H/config/kernel-firmware.dat:2-18`; `R/packages/linux/package.mk:223-244`.

The thirteen names match exactly, and the embedding branch is specifically aarch64 H700. The excerpts establish neither “a few hundred KB” nor harmlessness, and they do not include the firmware-loader implementation proving lookup priority. More importantly, matching duplicate names today does not eliminate the update and build-input coupling described in G-34 and G-35.

**G-20 — narrowed — F-06.** Evidence: `scripts/unpack:140-159`; `R/packages/linux/package.mk:16-18`; `H/patches/linux/0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled:1-12`.

The shown ordinary patch globs do not select this `.disabled` file, so its inactive-build disposition stands. But line 140 permits explicitly named patch files, making “the machinery only ever applies `*.patch`” too broad; the suffix is not an absolute exclusion mechanism. The claimed birth history and source-line percentage are reported context, not evidence of runtime image cost.

**G-21 — confirmed — F-07, as a placement disposition.** Evidence: `R/config.xml:4-43`; `distributions/ROCKNIX/config/functions:226-230`; `R/packages/linux/package.mk:419-425`.

The XML targets and installation loop do not restrict tree production to the particular handheld receiving the image. Within the stated two-unit scope, carrying the other thirteen sources by placement is an accurate disposition, not a reason for this read-only audit to remove them or a claim about which DTB has actually run on a board.

**G-22 — narrowed — F-08.** Evidence: `H/filesystem/usr/lib/udev/rules.d/80-clock.rules:1-2`.

The current rule explicitly performs a userspace clock set, and its upstream deletion is reported in the supplied history. Accepting that deletion in a merge can remove the rule; it does not itself prove that the effective kernel configuration and enumerated RTC provide the intended replacement behavior.

**G-23 — narrowed — F-09.** Evidence: `H/options:77-84`; `D/sun50i-h700-anbernic-rg-sp.dts:10-12`; `H/packages/u-boot-DDR3/sources/configs/anbernic_rg35xx_h700_lpddr3_defconfig:16-28`.

The unexplained zero swap settings are real. But “nothing in the device directory says which unit … and tree” overstates the absence: the RG-SP source explicitly associates its model and dt-id, and the defconfigs associate memory types with voltages. What is missing is a joined-up unit → memory → image/loader → panel/tree explanation.

**G-24 — confirmed — F-10’s mechanical duplication, not a demonstrated need for redesign.** Evidence: `H/packages/u-boot-DDR3/package.mk:4-34`; `H/packages/u-boot-DDR4/package.mk:4-34`; `H/packages/u-boot/package.mk:16-34`; `H/packages/h700-suspend-stub/package.mk:21-35`.

The recipes differ only in package name and defconfig assignment. A replacement must still produce both independently staged artifacts and accommodate the stub’s textual defconfig lookup, so parameterization has coordination costs beyond removing duplicate lines; retaining it as a design proposal is appropriate.

**G-25 — narrowed — F-11.** Evidence: `R/bootloader/mkimage:18-26,87-89`.

The loader-branch correction is confirmed by the mutually exclusive branches. The separate history-cutoff erratum depends on the reported commands and run logs, not on these source lines, and is not independently reproduced by this review.

## 6. What the first reader missed

**G-26 — new — The updater can report success after boot-file or raw-loader failure.** Evidence: `H/bootloader/update.sh:19-31,53-63`; `R/packages/sysutils/busybox/scripts/init:430-437`.

A failed read-write remount or failed DTB copy does not stop the later raw loader write, and the `dd` status is neither checked nor preserved. The final update-hint write can return success despite earlier failures, while the caller prints “Boot Files Updated” regardless of the script’s status. This is a concrete error-handling defect in a root updater, with possible bootability consequences—not merely a design question about voltage selection. It directly refutes the first reader’s “nothing … behaves wrongly” and “No bug” conclusions.

**G-27 — new — Destination validation and DTB replacement are unsafe boundaries.** Evidence: `H/bootloader/update.sh:7-16,22-31,52-55`.

The script accepts a supplied `BOOT_DISK` without checking that it is a block device or the parent of the mounted boot partition; the raw writer’s only checks concern the selected source filename. It also overwrites the live `dtb.img` directly, without a checked temporary copy and rename, so an interrupted or failed copy can destroy the previously usable file. Even the destination `device_trees` directory is assumed to exist, unlike `overlays`, which is explicitly created. These are higher-value validation and failure-containment fixes than deduplicating the two small loader recipes.

**G-28 — new — The updater has an unverified shell-dialect contract.** Evidence: `H/bootloader/update.sh:1,36,55,60-63`; `R/packages/sysutils/busybox/scripts/init:435`.

The caller explicitly invokes `sh`, but the script uses `[[ … == … ]]` and `&>`, neither of which is POSIX shell syntax. A compatible BusyBox shell may support both, so this is not proof that the shipped shell fails. On a shell without those extensions, however, detection can fail and `&>` can be parsed as background execution followed by a redirection, invalidating the intended write/sync/remount ordering; the shell configuration is needed to close this check.

**G-29 — new — The suspend-stub output/install contract is not established by the recipe.** Evidence: `H/packages/h700-suspend-stub/package.mk:29,38-40,50-54`; `R/packages/tools/atf/package.mk:39-45`.

The builds run under separate `make -C` directories with relative output names, but installation uses an unqualified `*.bin` glob; no displayed step brings those per-variant outputs into the installer’s working directory. The omitted source Makefile or build driver may arrange this, so I would not report a proven broken build from the recipe alone. Nevertheless, atf expects two exact named files in the sysroot, making output location, stale-file exclusion and installation of both artifacts concrete host-side checks the first reader did not establish.

**G-30 — new — Recipe ordering is deliberate, but the stronger invariant claims are unproved.** Evidence: `H/packages/u-boot-DDR3/package.mk:18-25`; `H/packages/u-boot-DDR4/package.mk:18-25`; `H/packages/h700-suspend-stub/package.mk:10,14-18,31-46`; `R/packages/tools/atf/package.mk:18-20`.

The visible dependency declarations avoid the obvious target-build cycle by making the stub’s u-boot dependencies unpack-only; they are not evidence of a cycle by themselves. The stub nevertheless scrapes a literal assignment from another recipe rather than consuming explicit shared metadata, which matters to F-10’s parameterization proposal. Its visible duplicate-string check does not independently prove a valid `(type, clock)` key, because line 43 remains opaque under the required mask. The reader should not certify that extraction or infer the unknown flag from the surviving text.

**G-31 — new — Both udev rules encode enumeration assumptions, not stable hardware identification.** Evidence: `H/filesystem/usr/lib/udev/rules.d/80-clock.rules:1-2`; `H/filesystem/usr/lib/udev/rules.d/wlan0.powersave.off.rules:1`.

The RTC comment names PCF8563, but the match checks only `rtc0`; a changed enumeration order could make it set time from another RTC. The WLAN rule matches the exact SDIO ancestor `mmc2:0001:1`, not an interface named `wlan0`, and applies the command to `%k`. A controller-number change can silently stop that match, and an add-only rule does not establish persistence across later power-management changes. These are currency-sensitive matching assumptions, not observed failures on either handheld.

**G-32 — narrowed — No local dt-id collision is present; mainline collisions and include availability remain unchecked.** Evidence:  
`D/sun50i-h700-anbernic-rg-sp.dts:7-12`; `D/sun50i-h700-anbernic-rg28xx.dts:7-12`; `D/sun50i-h700-anbernic-rg34xx-sp-v2-panel.dts:7-12`; `D/sun50i-h700-anbernic-rg34xx-sp.dts:7-12`; `D/sun50i-h700-anbernic-rg34xx.dts:7-12`; `D/sun50i-h700-anbernic-rg35xx-2024-rev6-panel.dts:7-10`; `D/sun50i-h700-anbernic-rg35xx-h-rev6-panel.dts:7-10`; `D/sun50i-h700-anbernic-rg35xx-plus-rev6-panel.dts:7-10`; `D/sun50i-h700-anbernic-rg35xx-pro.dts:7-12`; `D/sun50i-h700-anbernic-rg35xx-sp-v2-panel.dts:7-10`; `D/sun50i-h700-anbernic-rg40xx-h.dts:6-11`; `D/sun50i-h700-anbernic-rg40xx-h-v2-panel.dts:6-9`; `D/sun50i-h700-anbernic-rg40xx-v.dts:6-11`; `D/sun50i-h700-anbernic-rg40xx-v-v2-panel.dts:6-9`; `D/sun50i-h700-anbernic-rgcubexx.dts:7-12`.

All fifteen displayed ids are distinct and match their own filename stems; there is no demonstrated accidental inheritance of a base tree’s id. The thirteen external includes use only four distinct base filenames, while the two sibling include targets are supplied. The effective 7.2 source tree and its patches are not supplied, so neither a mainline-id collision nor a nonexistent external include can honestly be alleged or ruled out. The reader is wrong to treat checking their existence as requiring a build: this is a host-side source inspection, not a handheld-only fact.

**G-33 — new — RG40XX V has a case-sensitive identity discrepancy worth checking.** Evidence: `D/sun50i-h700-anbernic-rg40xx-v.dts:9-11`.

The root compatible is `anbernic,rg40xx-V`, with uppercase `V`, whereas its dt-id and filename use lowercase `v`. This is not a dt-id collision, but it is a concrete spelling discrepancy that can matter to exact compatible-string consumers. Without the binding or those consumers, it is a validation lead rather than proof of a broken board; the generic Allwinner compatible remains present.

**G-34 — new — Firmware duplication creates a coupled update contract, not just wasted space.** Evidence: `H/config/kernel-firmware.dat:2-18`; `R/packages/linux/package.mk:227-244`.

The reader’s “neither knows of the other” description is misleading: kernel embedding reads the `kernel-firmware` package’s `.copied-firmware` output rather than obtaining an independent copy of the firmware. Removing apparently redundant list entries can therefore deprive the embedding step of its inputs, while changing filesystem firmware alone cannot change the bytes already embedded in the kernel. Even accepting F-05’s built-in-first premise, that precedence can shadow a filesystem-only correction until the kernel is rebuilt. Matching names today is not evidence that the two update paths or their rebuild triggers remain coherent.

**G-35 — new — Firmware still depends on temporary build-tree state and potentially retained embedding inputs.** Evidence: `R/packages/linux/package.mk:224-244`; `H/packages/u-boot-DDR3/package.mk:38-42`; `H/packages/h700-suspend-stub/package.mk:50-54`.

Unlike the bootloader recipes’ documented sysroot staging, the kernel reads firmware from `get_build_dir kernel-firmware`, so that build directory must remain available even if installed filesystem copies already exist. An AUTOREMOVE or cross-job boundary therefore needs an explicit preservation/recreation contract; the supplied kernel excerpt does not establish one. Additionally, the embedding directory is created but not cleared before `find` collects every file, so a reused directory could retain obsolete inputs unless the surrounding build machinery guarantees cleanup. Both are host-build checks, not reasons to request a handheld experiment.

**G-36 — new — The normal generated boot configuration includes a production-relevant debug-shell directive.** Evidence: `H/options:30-31,71-72`; `R/bootloader/mkimage:45-49`.

`EXTRA_CMDLINE` unconditionally includes `systemd.debug_shell=ttyS0`, and the normal extlinux generator appends it without a debug-build guard. This is a request for systemd’s privileged debug shell, not merely serial logging, and deserves an explicit shipping-policy disposition. Whether the physical UART and service are usable on either unit remains an open device fact; the code nevertheless exposes an omitted security-relevant configuration choice.