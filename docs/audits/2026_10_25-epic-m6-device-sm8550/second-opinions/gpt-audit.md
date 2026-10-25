References below use **D/** = `projects/ROCKNIX/devices/SM8550/`, **T/** = `D/linux/dts/qcom/`, **I/** = `D/filesystem/usr/share/inputplumber/`, **P/** = `projects/ROCKNIX/packages/`, and **B/** = `projects/ROCKNIX/bootloader/`. Unmarked references are at `8ebaf8daad`; **@U** means `651150fc88`. Unprinted upstream copies and commit-history results remain reported evidence, not an independent re-read.

## 1. The pins and the superseded path

**G-1 — confirmed: four unchanged pins, not three.** Evidence: `P/tools/qcom-abl/package.mk:4-11`; `P/linux/package.mk:29-35`, `@U:35-41`; `P/linux-firmware/kernel-firmware/package.mk:5-9`; `P/tools/gamepadcalibration/package.mk:5-9,26-31`.

The classifications are **identical pins** for `qcom-abl` 1.0, Linux 7.2/`f9fef3d14c0d…`, `kernel-firmware` 20260309/`28fb1b57fa95…`, and `gamepadcalibration` `2077e7af7e9a…`/`f14730170a41…`. The kernel pair is directly visible; the other three upstream identities, including the SM6115-only gamepad recipe change, are supplied comparison results. The first reader correctly distinguishes pin equality from recipe equality, but `04`’s count of “three identical” pins is wrong: there are four.

**G-2 — confirmed: one absent old loader and one deleted tool.** Evidence: `P/tools/rocknix-abl/package.mk:5-8,12-17`; `P/tools/mkbootimg/package.mk:5-9`; `P/tools/openabl/package.mk@U:5-8,12-17`; `D/options@U:34,66`; `P/linux/package.mk:19`, `@U:18-20`.

The supplied history classifies `rocknix-abl` 1.2/`64034fb076ea…` as **absent upstream**, replaced by the distinct OpenABL 1.2/`28cb97d1b387…` package, and `mkbootimg` `d2bb0af5ba6d…`/`418bb875c03d…` as **deleted** by `cafbb1657d`. The visible upstream package selection and removal of the SM host-tool dependency agree with that account. Equal loader version numbers do not mean equal payloads: the project, archive, checksum and installed directory change.

**G-3 — confirmed: the other two pins differ.** Evidence: `P/linux-firmware/extra-firmware/package.mk:5-9,20`, `@U:5-9,20`; `P/tools/inputplumber/package.mk:5-12,39-44`, `@U:5-12,35-59`.

`extra-firmware` changes from `88b363e67d4f…`/`1b253d1a79ed…` to `925dfb5efbe5…`/`b994fa1c4517…`; InputPlumber changes from `v0.79.0`/`123c858139d3…` to `0.82.0`/`aaee9b65b47a…`. The latter also changes the build cost and packaging contract: a prebuilt aarch64 tree becomes a Cargo build with `rootfs/usr` assets. The unchanged SM8550 firmware-copy branch does not establish which Nova firmware bytes changed inside the new archive, and neither comparison establishes the author’s latest release.

**G-4 — narrowed: the selected boot route is superseded, not literally every unit or defect.** Evidence: `D/options:34,66`, `@U:34,66`; `projects/ROCKNIX/config.xml:130-145`, `@U:134-149`; `D/bootloader/update.sh@U:10-17,37-43`; `P/tools/qcom-abl/package.mk:4-11`.

The central replacement is real: upstream selects `arm-efi` plus OpenABL and changes the image steps to `abl,bls,dtb`. However, the fourteen-tree list survives, the reported-identical `qcom-abl` meta-recipe survives unused by this selection, and the unused disk calculation and unchecked updater execution survive. The first reader’s “every unit … settled by the next base merge” is therefore too broad: source replacement is not proof of safe migration or corrected failure handling.

**G-5 — confirmed: the BLS filename is an identity-sensitive seam.** Evidence: `P/virtual/arm-efi/package.mk@U:14-22`; `distributions/ROCKNIX/options:17,20,202-203`; `D/bootloader/update.sh@U:25-28`.

With the fork’s values, the generated entry is `loader/entries/pixelelated.conf`, titled `pixelelated`, with `boot=LABEL=ROCKNIX` and `disk=LABEL=STORAGE`. The persisted filename is distinct from display text, so D-WORKFLOW-123’s identity policy is relevant; the partition labels themselves are not being renamed by this recipe. This is not yet proof of a loader failure: the loader’s filename/default-selection contract is absent, and the recursive update copy can retain any pre-existing entries alongside the new one.

**G-6 — new: the merge must establish a coherent migration, not just names and slot contents.** Evidence: `P/linux/package.mk:391-403`; `D/bootloader/update.sh@U:19-43`; `P/virtual/arm-efi/package.mk@U:17-22`; `P/rocknix/sources/scripts/updateabl@U:7-16,84-89`; `docs/releases/device-facts.md:17`.

The missing questions include compatibility across the Android-image-to-BLS transition, handling an interrupted or failed payload copy, and recovery after both ABL slots have been changed. Upstream copies DTBs and loader configuration before flashing, but does not condition the flash on those copies succeeding. Its BLS entry does not name a DTB, while the new chroot path introduces bind-mount, cleanup and runtime-environment requirements whose returned failure the parent still ignores. L17 establishes the older deployment’s boot and ABL writes, not any of those migration properties.

## 2. The configuration

**G-7 — narrowed: all fourteen lines are accounted for, but one attribution is wrong.** Evidence: `D/linux/linux.aarch64.conf:5,7,14-16,2728,8219`; `D/linux/linux.aarch64.conf@U:5,7,14-16,25,8219` in the supplied diff.

Ten lines are the five paired version fields: compiler text, GCC `150200→160200`, Rust `109801→109901`, Rust LLVM `220108→230101`, and LLVM major `22→23`. The remaining four are the added `CC_HAS_COUNTED_BY_PTR=y`, deletion of the disabled `INPUT_POLLDEV` line, and the two states of `RAID6_PQ_BENCHMARK`. **`INPUT_POLLDEV` is not a compiler-capability line and is not replaced by `CC_HAS_COUNTED_BY_PTR`**; these are independent changes at different locations, so the first reader’s pairing is misleading.

**G-8 — confirmed: the RAID6 change is behavioural, not a toolchain stamp.** Evidence: `D/linux/linux.aarch64.conf:8219`; `D/linux/linux.aarch64.conf@U:8219`; supplied diff at `:25` and `:2728`.

Changing `RAID6_PQ_BENCHMARK` from enabled to disabled changes the kernel’s RAID6 algorithm-selection/benchmark policy and its initialization work; it is not merely recording the compiler used. No Nova timing or performance result follows from that configuration comparison. Conversely, deleting an already-disabled `INPUT_POLLDEV` entry is not evidence that polling input becomes enabled, and the compiler-capability addition is not an independently selected Nova device feature.

## 3. The loader and the tree

**G-9 — narrowed: fourteen targets are requested; exactly fourteen appended artifacts are not guaranteed.** Evidence: `D/options:25-28`; `distributions/ROCKNIX/config/functions:226-231`; `projects/ROCKNIX/config.xml:130-145`; `P/linux/package.mk:114-117,391-396`.

The helper generates exactly fourteen `qcom/<name>.dtb` make targets, and the device sources are copied into the kernel DTS tree. The append loop, however, enumerates existing `.dtb` files through a filesystem glob, not those fourteen XML entries. A clean build producing only the requested DTBs would yield the claimed fourteen, but extra or stale matching artifacts would also be appended, in glob order rather than XML order. The first reader’s P6 is consequently a requested-target/source-path proof, not proof of an exact completed build or image contents.

**G-10 — confirmed: only `mkimage_abl` is selected at the audited hash.** Evidence: `scripts/mkimage:257-266`; `B/mkimage:6-30,73-96,108-113`; `distributions/ROCKNIX/config/functions:384-400`; `projects/ROCKNIX/config.xml:130`.

The project script reaches `mkimage_all`, whose SM8550 options contain only `abl`; neither `uboot` nor `dtb` is selected. Thus both SM8550-naming branches are unreachable through this configured image-build route, independently of whether anyone could supply a `rocknix-u-boot.img`. Upstream’s `abl,bls,dtb` selection makes the DTB **step** reachable; it does not prove that the old branch body remains unchanged (`projects/ROCKNIX/config.xml@U:134`).

**G-11 — narrowed: the guards are inside `updateabl`, but they are weaker than claimed.** Evidence: `D/bootloader/update.sh:19-25`; `P/rocknix/sources/scripts/updateabl:7-36,64-73`.

With an exported `SYSTEM_ROOT` pointing to the intended new SM8550 system, the child sources that system’s `os-release` and selects its installed ELF; it does not select the card copy. The checks at `:9-36` establish an allowed **declared device family**, an existing file and two block-device paths, while `:64-67` supplies the separate checksum skip condition. They do not establish that the declared family matches the physical handheld, validate the ELF’s contents, or make the parent honor a failure. Therefore the first reader is right about the location of the basic guard, but wrong to promote it into an unconditional “safe for the ELF” conclusion.

**G-12 — confirmed: the card copy is a manual-flash input in the supplied path.** Evidence: `P/tools/rocknix-abl/package.mk:12-17`; `D/bootloader/update.sh:19-25`; `P/rocknix/sources/scripts/updateabl:19`; `P/tools/rocknix-abl/sources/README:1-6`.

The package stages the ELF and flashing scripts, and the updater copies those files to the card. The automatic writer instead reads `$SYSTEM_ROOT/usr/share/bootloader/rocknix_abl/…`; the README instructs a person to copy the card directory into Android storage and flash manually. No other reader of `/flash/rocknix_abl/` is shown, although that is a conclusion about the supplied path, not an inspection of the downloaded ABL binary.

## 4. The firmware

**G-13 — narrowed: the packaging divergence is established; “observed working” has a much smaller scope.** Evidence: `D/config/kernel-firmware.dat:2-8`; `P/linux-firmware/kernel-firmware/package.mk:39-70`; `P/linux/package.mk:83-90,208-283`; `docs/releases/device-facts.md:17-18`.

The six entries are file-install patterns, and the shown device-specific embedding chain does not include SM8550, unlike its three Qualcomm siblings. That establishes the packaging difference, not successful loading of every listed firmware item. L17 and L18 describe an older `bc9dfe8141` deployment and one active frontend observation; L18 explicitly disclaims a rendering proof. The first reader cannot derive “not a bug” or correct firmware timing at the audited hash from those observations.

**G-14 — confirmed: a documented early, cached firmware failure exists—cfg80211.** Evidence: `P/linux/package.mk:93-97,285-290`.

The recipe explicitly identifies **cfg80211 requesting `regulatory.db` during kernel initialization**, before the firmware overlay is available, receiving `-ENOENT`, and retaining the failed result with domain-00/5-GHz restrictions. This is the requested boot-order counterexample, but the supplied evidence is the recipe’s explicit explanation, not a printed cfg80211 C request site. Its config-driven dependency and embedding mitigation also defeat the broader inference “no SM8550-naming block means no embedded firmware whatsoever.” It does **not** establish the same failure for A740/GMU firmware: no corresponding DRM request/retry path is supplied.

## 5. The Nova’s files

**G-15 — confirmed: the two InputPlumber files intentionally serve the Nova.** Evidence: `I/devices/02-ayn-controller.yaml:40-63,77-89`; `I/capability_maps/ayn_mcu.yaml:9-12`; `T/qcs8550-ayn-common.dtsi:1698-1714`; `docs/releases/device-facts.md:28`.

The explicit Nova model match selects a profile whose source-device rules reference `ayn_mcu`, and that ID exists in the capability-map file. The inherited `rsinput` device named “AYN Odin2 Gamepad” explains why an AYN-named configuration can be appropriate for this Retroid board. This establishes intended configuration reach, not successful live routing: L28’s sign-in-pad observation remains “never.” Also, the actual target is `ds5`, not the `ds5-edge` described by the adjacent comments.

**G-16 — confirmed: RP6 and AYN common are real Nova dependencies.** Evidence: `T/qcs8550-retroidpocket-rpnova.dts:8-35`; `T/qcs8550-retroidpocket-rp6.dts:8,130-150,162-203,349-391`; `T/qcs8550-ayn-common.dtsi:9-15`; `projects/ROCKNIX/config.xml:131-144`.

The Nova includes RP6, which includes AYN common, and then overrides selected panel, touch and controller properties. None of the other thirteen local sources is included into that Nova-specific closure. Nevertheless, the twelve other board DTS files remain requested build targets, and AYANEO common feeds its board targets, so “not used by the Nova DTB” must not be mistaken for “not involved in building the SM8550 image.”

**G-17 — narrowed: seven other input files are not selected for native Nova input, not universally unreachable.** Evidence: `I/devices/01-ayaneo-controller-japanese.yaml:14-59`; `I/devices/01-ayaneo-controller.yaml:14-53`; `I/devices/02-ayn-thor-controller.yaml:14-38`; `D/filesystem/usr/lib/udev/hwdb.d/10-ayaneo.hwdb:1-3`; `T/qcs8550-ayn-common.dtsi:1701-1708`.

The other device profiles gate their mappings on AYANEO or Thor model strings, rather than the Nova string. The capability maps have effect through those references; their filenames alone do not determine reach. The hwdb rule is broader than a board-model rule: it could match an attached device named `AYANEO DEVICE*` on a Nova, although it does not match the inherited native “AYN Odin2 Gamepad.” Thus the placement classification is sensible, but “none can ever be used on a Nova” would be too strong.

## 6. Findings F-01 to F-08

**G-18 — narrowed: F-01.** Evidence: `D/options@U:34,66`; `projects/ROCKNIX/config.xml@U:134`; `D/bootloader/update.sh@U:19-43`; `P/virtual/arm-efi/package.mk@U:17-22`.

The boot-path replacement and identity review are valid findings. “Settled by the merge” must exclude failure handling, coherent first-boot migration, recovery, and DTB selection, none of which is established merely by importing these files.

**G-19 — confirmed: F-02’s pin classifications, with evidence limits.** Evidence: `P/linux/package.mk:29-35`, `@U:35-41`; `P/linux-firmware/extra-firmware/package.mk:5-6`, `@U:5-6`; `P/tools/inputplumber/package.mk:5-9`, `@U:5-10`; `P/linux-firmware/kernel-firmware/package.mk:5-9`.

The eight-way classification is correct as supplied: four unchanged pins, two differing pins, one absent old loader and one deleted tool. The generic-firmware lag and the unprinted recipe histories remain reported comparisons; the visible override pin does not independently prove either generic-recipe contents or author-release freshness.

**G-20 — narrowed: F-03.** Evidence: `D/config/kernel-firmware.dat:2-8`; `P/linux/package.mk:208-290`; `docs/releases/device-facts.md:17-18`.

Keep the six-entry installation/embedding distinction and the historical frontend observation. Drop the inference that this proves all firmware paths safe: the recipe itself documents an early-request failure class, while the device facts expressly do not provide rendering or firmware-request evidence.

**G-21 — refuted: F-04’s “not a bug” disposition.** Evidence: `D/bootloader/update.sh:25-37`; `P/rocknix/sources/scripts/updateabl:24-36,72-77`; `D/bootloader/update.sh@U:22-43`.

The description of unchecked steps is correct, but the claimed harmlessness is not. A failed automatic-loader update can be ignored while the parent deletes boot files and writes its success hint, and upstream retains the same unchecked progression while copying automatically consumed BLS/DTB assets.

**G-22 — narrowed: F-05.** Evidence: `P/linux/package.mk:392-396`; `P/tools/rocknix-abl/sources/README:1-6`; `P/virtual/arm-efi/package.mk@U:17-22`.

The need for a cross-file boot/update explanation remains well founded, and the supplied README is only an Android-side manual procedure. The first reader is wrong that the shown BLS entry makes the Nova tree explicit: it names a kernel and options, but no `devicetree` or equivalent board selection.

**G-23 — confirmed: F-06 for the normal build path.** Evidence: `D/patches/linux/0053-add-hynitron-touchscreen.patch.disabled:1-12`; `P/linux/package.mk:16`; `scripts/unpack:140-159`.

The `.patch.disabled` filename does not match the shown normal `*.patch` collection rules. Its large audit/source weight is therefore not equivalent to compiled kernel weight or boot-time work. “Disabled at birth” and unchanged-upstream history remain supplied history, not facts derivable from the twelve printed header lines.

**G-24 — narrowed: F-07 to intended native-board use.** Evidence: `T/qcs8550-retroidpocket-rpnova.dts:8-12`; `T/qcs8550-retroidpocket-rp6.dts:8`; `I/devices/02-ayn-controller.yaml:40-63`; `projects/ROCKNIX/config.xml:131-144`; `D/filesystem/usr/lib/udev/hwdb.d/10-ayaneo.hwdb:1`.

The three-tree/two-input-file Nova correction and the remaining thirteen/seven counts are sound. Retain “carried by placement,” but not an implication that the other trees are absent from the image build or that model-independent peripheral rules can never apply on the Nova.

**G-25 — confirmed: F-08 at the audited configuration.** Evidence: `B/mkimage:22-26,81-83,108-113`; `projects/ROCKNIX/config.xml:130`; `distributions/ROCKNIX/config/functions:384-400`; `projects/ROCKNIX/config.xml@U:134`.

Neither branch runs through SM8550’s configured `mkimage_all` at the audited hash. The strongest proof is dispatch reachability, not the reported absence of a producer for one filename; upstream changes that dispatch by adding the DTB step.

## 7. What the first reader missed

**G-26 — new: the root updater can report success after critical failure and destructive continuation.** Evidence: `D/bootloader/update.sh:17-37`; `P/rocknix/sources/scripts/updateabl:24-36`; `D/bootloader/update.sh@U:19-43`.

Under ordinary execution of the script as written, an absent ELF or missing partition makes `updateabl` return failure, but the parent continues through `/flash/boot` and `/flash/EFI` removal and finishes with `echo "UPDATE"`. A failed final read-only remount is likewise ignored, potentially leaving the boot filesystem writable while returning the hint write’s success. This is a concrete error-propagation and state-reporting defect, not merely a damaged manual-flash copy. The upstream version preserves the problem and expands the unchecked copies to files required by the new automatic boot path.

**G-27 — new: the hand-off trusts image identity, not hardware identity.** Evidence: `D/bootloader/update.sh:5,25`; `P/rocknix/sources/scripts/updateabl:7-19,31-36,72-73`; `P/tools/rocknix-abl/package.mk:13-14`.

If `SYSTEM_ROOT` names another allowed family’s image, its `HW_DEVICE` selects that family’s ELF, while the partition searches still operate on the running machine. For example, an SM8250 image declaration passes the same allowlist on a physical Nova; nothing in this hand-off compares new-image identity with independently obtained running-device identity. An earlier caller may reject that situation, but no such caller is supplied, so the first reader cannot certify that `update.sh` “makes it write nothing it should not.” The caller must also preserve the `SYSTEM_ROOT` environment contract: prefixing the executable path is not itself an explicit environment hand-off for a non-exported shell variable.

**G-28 — new: the checksum guard has an unestablished byte-range invariant and unchecked I/O.** Evidence: `P/rocknix/sources/scripts/updateabl:39-57,64-77`; `P/rocknix/sources/scripts/updateabl@U:51-69,76-89`.

The script hashes `ceil(ELF_SIZE/sector_size)` sectors from each partition but hashes only `ELF_SIZE` bytes from the ELF. Unless the ELF is sector-aligned, those are different-length inputs, so an already-written payload can repeatedly fail the equality test and trigger both writes. Alignment is not established by the supplied recipes, so this is a conditional correctness defect, not a claim that the Nova has exhibited repeated flashing. Independently, neither read nor write `dd` is checked before the final success message; the upstream chroot addition leaves both issues intact.

**G-29 — narrowed: no undefined local node/label is demonstrated by the supplied include closure.** Evidence: `T/qcs8550-ayn-thor.dts:368-370`; `T/qcs8550-ayn-common.dtsi:392-401,1698-1714`; `T/qcs8550-retroidpocket-rp6.dts:130-150`; `T/qcs8550-ayn-common.dtsi:9-15,42-56`.

The suspicious-looking Thor absolute reference `/sound/wcd-capture-dai-link/codec` is defined in AYN common, as are RP6’s `gamepad` and `/gpio-keys` references. I would not invent an undefined-label finding from those uses. A complete negative result still requires the omitted `qcs8550.dtsi`, PMIC includes and effective T41 patches; unresolved references there are a host-side source/compile question, not something requiring the Nova.

**G-30 — new: the Nova inherits a touchscreen pinctrl mismatch.** Evidence: `T/qcs8550-retroidpocket-rp6.dts:349-367`; `T/qcs8550-retroidpocket-rpnova.dts:22-27`; `T/qcs8550-ayn-common.dtsi:1587-1641`; `T/qcs8550-ayn-thor.dts:382-392`.

RP6’s touchscreen requests reset GPIO **14** and interrupt GPIO **15**, but selects the `ts_p_*` pinctrl states, which configure GPIO **24/25**. The common file already defines matching `ts_s_*` states for GPIO 14/15, and Thor uses those states for its corresponding secondary touchscreen. The Nova override changes dimensions and inversion only, so this mismatch reaches its tree unchanged. This is a defined-but-wrong-reference discrepancy, not a missing-label compile error; an actual Nova touch failure remains unobserved.

**G-31 — new: the GPT command-line difference needs an explicit, limited interpretation.** Evidence: `D/options:21,31,33-34`; `D/options@U:21,31,33-34`; `P/linux/package.mk:402`; `P/virtual/arm-efi/package.mk@U:21`.

The fork declares a GPT image but does not pass `gpt`; upstream adds that argument and carries it into the generated BLS options. That is a boot-policy difference rather than a toolchain stamp, and should be included in the migration explanation. It is **not**, by itself, proof that the fork cannot read GPT: absence of a force-scan argument does not establish failed normal GPT detection, and the relevant kernel configuration/parser path is not supplied. The adjacent “syslinux / u-boot” comment is simply stale for both actual bootloader selections.

**G-32 — new: the available identifiers do not uniquely select the Nova.** Evidence: `T/qcs8550-retroidpocket-rpnova.dts:8-12`; `T/qcs8550-retroidpocket-rp6.dts:10-14`; `T/qcs8550-retroidpocket-rp6-top-dpad.dts:8-17`; `T/qcs8550-ayn-odin2.dts:11-14`; `T/qcs8550-ayn-common.dtsi:28-30`; `P/linux/package.mk:392-396`; `P/virtual/arm-efi/package.mk@U:17-22`.

The Nova inherits RP6’s board ID `0x1001f,0` and MSM ID `0x25b,0x20000`; Odin 2’s decimal `603` is the same MSM ID, and TOP-DPAD also inherits RP6’s identifiers. The inherited `rocknix-u-boot-dt-id` likewise does not distinguish them, so an ID-only or first-match selector has multiple candidates and could choose another board. The Nova’s unique `compatible` helps only if the loader actually consumes it; neither the append loop nor the shown BLS entry establishes that contract. This is a concrete selection ambiguity to resolve from ABL/OpenABL’s selection logic, not evidence that any particular wrong tree has booted on the unit.