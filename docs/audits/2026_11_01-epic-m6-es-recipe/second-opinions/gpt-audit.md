## Grades

- **PL-01** -- confirmed with narrowing; severity holds: The link embeds the staging root, and the shown tar transfer preserves that target (`emulationstation/package.mk:101`; `scripts/build:139-145`; `scripts/install:164-185`). This proves a bad staged link, not a failed tip-image boot; the candidate reportedly contains a corrected link (`02-forward-audit.md:469`). The cited `config/functions:1380` and final `scripts/image` handling are not supplied.

- **PL-02** -- confirmed; severity holds: The unpacker maps `x86_64` to `x86`, while the recipe supplies no additional patch directory; consequently the shown architecture glob cannot reach `patches/x86_64/` (`scripts/unpack:127-159`; `emulationstation/package.mk:4-33`). This establishes reachability failure, not the patch’s correctness—see G-1.

- **PL-03** -- confirmed with narrowing; severity holds: `PKG_NEED_UNPACK` is appended directly to filesystem paths, without package-name resolution (`config/functions:1112-1126`); the lane reports that the bare `busybox` path finds nothing (`02-forward-audit.md:68`). This is a stamp-input defect, not evidence of a missing build-order edge; whether BusyBox should invalidate ES remains unestablished.

- **PL-04** -- confirmed with narrowing; severity holds: The removal precedes resource installation, so it does not remove the subsequently copied logo (`emulationstation/package.mk:79-82`). The splash justification is wrong: this recipe enables ROCKNIX, whose default is the wordmark; cited `Splash.h:17` belongs to the other-platform branch (`emulationstation/package.mk:19`; `16dbac5211:es-core/src/Splash.h:10-18`).

- **PL-05** -- confirmed with narrowing; severity holds: The current recipe lacks the upstream device filter, and its remaining XPath does not remove the `vulkan driver` feature (`emulationstation/package.mk:125-129`; `es_features.cfg:1392-1395`; `651150fc88:emulationstation/package.mk:104-108`). The missing policy is established, but the four-merge history and actual bundled-driver availability require the omitted history output and ARMSX2 recipe; blindly restoring the whitelist is not justified.

- **PL-06** -- confirmed with narrowing; severity Low: There is no direct dependency, but the reported plan already supplies a transitive dependency (`emulationstation/package.mk:13`; `02-forward-audit.md:233-241`). Reported absence from `ldd` does **not** establish a failed configure probe or the compiled fallback, particularly for the separately patched candidate; optional fallback is expressly supported, so Medium lacks a demonstrated functional regression (`02-forward-audit.md:126,467`; `16dbac5211:CMakeLists.txt:230-244,459-462`).

- **PL-07** -- confirmed with narrowing; severity holds: Installation has no French-catalog assertion (`emulationstation/package.mk:67-68`). However, the cited top-level block only controls `HAVE_INTL`; proving that missing tools produce a successful catalog-less build requires the omitted inclusion guard for the `i18n ALL` target, whose commands invoke those tools (`16dbac5211:CMakeLists.txt:565-578`; `16dbac5211:locale/CMakeLists.txt:1-9,25-31`).

- **PL-08** -- confirmed; severity holds: HFS has an environment-to-definition route but no corresponding status-loop entry (`scripts/get_env:14-21`; `16dbac5211:CMakeLists.txt:328-330`; `emulationstation/package.mk:42-50`). This is an observability omission, not a guard preventing scraper inclusion.

- **PL-09** -- cannot tell from the packet; severity Low (provisional): Both call sites and the ROCKNIX default are shown, but `main.cpp:101-254`—most of the parser—is missing (`start_es.sh:8`; `emustation.service:12`; `16dbac5211:es-core/src/Paths.cpp:76-81`). Writing to the same directory supplied by the alleged flag cannot distinguish parsing from ignoring it (`02-forward-audit.md:470`); the missing parser section would settle that claim.

- **PL-10** -- cannot tell from the packet; severity Low (provisional): The cited checker implementations are absent; the packet supplies the lane’s reported results rather than their selection and failure-handling code (`05-punch-list.md:102-105`; `02-forward-audit.md:70-71`). Their source and captured control runs would settle the alleged fail-opens.

- **PL-11** -- confirmed; severity holds: The extra delimiter makes `#g` a comment rather than the substitution’s global flag (`emulationstation/package.mk:54`; reported demonstration at `02-forward-audit.md:69`). None of the fifteen listed device names triggers the multiple-hyphen case, supporting Low rather than a current device failure (`02-forward-audit.md:289-318`).

- **PL-12** -- confirmed with narrowing; severity holds: `|| true` suppresses failure status, not diagnostics—the command is explicitly verbose and unredirected (`emulationstation/package.mk:73-75`). The runtime code conditionally attempts regeneration but neither checks its success nor guarantees “first-boot time only”; it subsequently exports the locale regardless (`es_settings:16-43`).

- **PL-13** -- cannot tell from the packet; severity Low (provisional): The pin is verified, but upstream HEAD and “behind” are only dated reports; neither ancestry nor changed content is supplied (`lowerdeck/package.mk:5-9`; `02-forward-audit.md:256`; `docs/reviews/briefs/es-recipe.md:1025-1030`). The dated ref record and ancestry comparison would settle currency; a different HEAD alone establishes no functional defect.

- **PL-14** -- confirmed with narrowing; severity holds: Recipe merge debt is directly visible in upstream’s additional patch-directory setting and ARMSX2 filter (`651150fc88:emulationstation/package.mk:14,104-108`; `emulationstation/package.mk:13-17,125-129`). The complete six/six/two classification and remaining hunks are reported, not independently checkable from the supplied source versions (`02-forward-audit.md:342-359`); retain Low as a merge inventory.

- **PL-15** -- cannot tell from the packet; severity Low (provisional): Neither actual documentation section is supplied, so the claimed wording cannot be checked (`05-punch-list.md:152-154`). The technical distinction is supported: package-local extra directories use `PKG_PATCH_DIRS`, whereas the project/device patch location is separately automatic (`scripts/unpack:137-159`).

- **PL-16** -- cannot tell from the packet; severity Low (provisional): The packet reports a fail-closed payload attempt and a successful extracted-root check, but omits the cited tool implementation and raw failure output (`02-forward-audit.md:442-443`; `05-punch-list.md:162-164`). If verified, this is a host-prerequisite note—not a slice defect or proof that the payload route passed.

## Added findings

### G-1 (Medium): Making `cpugov.patch` reachable activates a wrong GPU enumerator

`emulationstation/patches/x86_64/cpugov.patch:17-24` replaces `get_available_gpu_governors` with **`get_available_cpu_governors` in both branches**. Fixing directory reachability alone therefore wires the CPU enumeration into `getAvailableGpuGovernors`; validate the helper contracts and correct that substitution before enabling the patch.

### G-2 (Medium): The proposed patch-directory assignment can discard other selections

`05-punch-list.md:25` proposes replacement with `PKG_PATCH_DIRS="x86_64"`, whereas upstream appends device selections (`651150fc88:emulationstation/package.mk:14`). If those selections precede the assignment, they are lost; additionally, the unpacker selects using `TARGET_ARCH`, not the proposed test’s `ARCH`, whose equivalence at recipe-loading time is not shown (`scripts/unpack:127-145`).

### G-3 (Medium): The restored ARMSX2 whitelist needs a capability audit

SM8750 ships `armsx2-sa` but is absent from the proposed restored whitelist (`virtual/emulators/package.mk:87-90`; `651150fc88:emulationstation/package.mk:105-108`). That does **not** prove SM8750 has bundled Turnip: neither blindly restoring the list nor blindly adding SM8750 is justified without its installer. Also, the current no-Vulkan edit removes matching **choice names**, not this driver feature (`emulationstation/package.mk:126-127`; `es_features.cfg:1392-1395`).

### G-4 (Low): Resolving BusyBox’s local directory may still miss its global recipe

The framework explicitly recognizes that project recipes can source global recipes, but adds the global directory only for the current `PKG_NAME` (`config/functions:1116-1124`). If `get_pkg_directory busybox` selects such an override, PL-03’s proposed fix still omits changes in BusyBox’s sourced global recipe; the lookup implementation and both BusyBox recipes are needed to determine whether that applies here.

### G-5 (Low): `SCREENSCRAPER_SOFTNAME` is not restricted to native builds

The contrary claim at `02-forward-audit.md:66` treats `KEEP` as an allowlist. An **exported** `SCREENSCRAPER_SOFTNAME` matches neither `PATH` nor `DROP`, so `get_env` emits it, and CMake consumes it (`scripts/get_env:14-21`; `16dbac5211:CMakeLists.txt:303-305`); “forwards exactly four names” is likewise incorrect (`02-forward-audit.md:491-493`).

### G-6 (Medium): Name-only status messages do not establish build-log secrecy

Private build overrides remain supported, while CMake expands credential environment variables into compiler definitions (`emulationstation/package.mk:36-40`; `16dbac5211:CMakeLists.txt:307-309,320-330`). The framework also provides verbose compiler-command modes (`config/functions:380-381`), creating a potential value-disclosure route outside the sanitized recipe echoes (`emulationstation/package.mk:48-50`); no actual disclosure is established by this packet.

### G-7 (Low): The autostart link does not repair a real directory or a wrong symlink

For an existing real `/storage/.emulationstation` directory, `! -L` passes and `ln -sf` creates a link **inside** that directory rather than replacing it (`autostart/001-emulationstation:8-11`). Conversely, any existing symlink—including a wrong or dangling one—is skipped; this is a legacy-alias repair defect, not evidence that the pinned ROCKNIX path itself fails (`16dbac5211:es-core/src/Paths.cpp:76-79`).

### G-8 (Medium): Empty serial data is treated as a device change

A successful but empty `cat` result is not rejected (`serial_number_check:8-14`). With a previously nonempty stored serial, it takes the mismatch branch, passes an empty value to `set_setting`, and enters the warning-status path instead of treating the read as invalid (`serial_number_check:16-24`); quoting the filename alone does not fix this.

### G-9 (Low): The initial default-theme explanation contradicts the guest record

L-20 assumes no `system-theme` exists and says the first available theme is selected and saved (`02-forward-audit.md:72`). The same draft reports a first-boot `system-theme` symlink and no saved `ThemeSet`, which supports the corrected account in `04`, not that assumption (`02-forward-audit.md:468`; `04-analysis.md:114-116`).

## The fixes

**PL-01 — device path.** Choose `/usr/config/emulationstation/es_systems.cfg` as the link target, retaining `${INSTALL}` only on the destination; that removes the staging-root interpolation (`emulationstation/package.mk:101`). Do not substitute a `/storage` target without checking managed-config linking. The recipe itself creates `es_systems.cfg` only in the tools-only branch, so the normal-image producer and final link resolution still require verification (`emulationstation/package.mk:105-123`).

**PL-02 — conditional assignment versus rename.** Prefer the single rename to `patches/x86/`, **after G-1 and helper availability are resolved**: it follows the unpacker’s existing architecture mapping rather than introducing another selector (`scripts/unpack:127-133,150-154`). The proposed assignment can erase other directories, and its `ARCH` test needs lifecycle verification; an explicit-directory solution should preserve existing selections and use a selector proven valid at that point (G-2). Renaming reaches every target resolving to `PATCH_ARCH=x86`, so validate both reported x86 devices, not just AMD64 (`02-forward-audit.md:289-292`).

**PL-03 — resolved BusyBox path.** Provisionally choose directory-based stamp tracking rather than deleting the apparent invalidation intent, but include the global BusyBox recipe if its project override sources it (G-4; `config/functions:1114-1126`). This repairs hashing, not necessarily unpack/build ordering; the framework separately resolves `PKG_DEPENDS_UNPACK` names (`config/functions:1331-1334`). Retaining an unnecessary dependency causes extra ES rebuilds; dropping a genuine input dependency leaves stale builds, so the BusyBox relationship must first be traced.

**PL-05 — restored ARMSX2 block.** Choose a filter matching the actual bundled-Turnip installation predicate, not an unverified copy of upstream’s five-device list (`651150fc88:emulationstation/package.mk:104-108`). SM8750 requires an explicit determination; exposing an unavailable driver and hiding an available one are opposite possible mistakes (G-3). Also verify the launcher’s default when the feature is removed: the XML advertises the bundled driver as default, but its runtime fallback is not supplied (`es_features.cfg:1392-1395`).

**PL-06 — explicit dependency versus recorded chain.** Choose a direct `fribidi` dependency to make ES’s requirement independent of the SDL/Sway/Pango route; merely recording that route leaves it sensitive to future window-manager/dependency changes (`02-forward-audit.md:233-239`). Adding the edge alone cannot explain or repair the candidate observation, because the reported plan already contains it; verify target pkg-config results, compile definitions and linkage. Do not make upstream’s cross-platform probe universally `REQUIRED`: its optional behavior is intentional, including for Windows (`16dbac5211:CMakeLists.txt:230-244`).

## Sections I need

- **Link installation:** `config/functions:1370-1390`; `scripts/image` rootfs assembly/link-processing lines; the `es_systems.cfg` generation/install block beyond `virtual/emulators/package.mk:110`; and `userconfig-setup`/`post-update` managed-config link blocks. These would settle the normal-image target’s existence, final preservation and whether an alternative `/storage` target introduces indirection problems.

- **Patch selection and execution:** `scripts/unpack:1-119`; the `config/options`/`config/functions` lines establishing `ARCH`, `TARGET_ARCH` and recipe-loading order; the pinned `ApiSystem.cpp` governor functions; and the source/install rules for `099-freqfunctions` and `100-amd64-freqfunctions`. These would settle selector equivalence, hunk applicability, GPU helper semantics and availability on GENERIC_X64 as well as AMD64.

- **BusyBox invalidation:** complete `get_pkg_directory`/`get_global_pkg_directory` bodies in `config/functions`, plus `packages/sysutils/busybox/package.mk` and `projects/ROCKNIX/packages/sysutils/busybox/package.mk`, particularly their sourcing and build-input lines. These would settle lookup precedence, global inheritance and whether the dependency is needed.

- **ARMSX2 capability:** `armsx2-sa`’s `package.mk` device/architecture cases and bundled-Turnip download/install lines, plus its installed launcher’s driver-selection/default block. The package’s full path is not supplied; these sections would settle the whitelist, especially SM8750, and behavior when the feature disappears.

- **Candidate configuration and catalogs:** candidate recipe blob `35e5f45e79` and its nine patches; redacted CMake probe/cache, compile-definition and link records; the FriBidi recipe’s library/pkg-config installation; and `Font.cpp`’s FriBidi branches. Also needed are the top-level `add_subdirectory(locale)` guard, remaining `CMakeLists.txt:581-617`, and `locale/CMakeLists.txt:36-52`; these would distinguish dynamic-link absence from actual fallback and settle missing-tool catalog behavior.

- **Credential logging:** the verbosity condition around `config/functions:380-381` and the `scripts/build` command/logging-redaction path. Redacted records only; these would establish whether the potential compiler-command exposure is reachable and mitigated.

- **Argument parsing:** `16dbac5211:es-app/src/main.cpp:101-254` and any additional argument-dispatch code. These would settle PL-09’s “parsed nowhere” claim.

- **Checker claims:** `tools/pkgcheck:157,169` with surrounding name-selection/exit handling; `tools/fork-package-freshness:16-18,42-44,89-93` with argument/ref handling; and the cited control-run output. For PL-16, `tools/pixelelated-state-check:767-792`, its root-route handler and the captured host failure/root-pass output would settle the prerequisite diagnosis and validation coverage.

- **Currency/history:** R1 C20’s dated upstream-ref record and a lowerdeck ancestry comparison; the complete `2174265e9c..651150fc88` `ui/` diff; and `stage-b/l01-merges.out` with the relevant parent/result hunks. These would settle PL-13’s “behind,” PL-14’s complete classification and PL-05’s four-merge account.

- **Documentation:** the actual `device-builds.md` “Iterating on EmulationStation” section and `CLAUDE.md` package-patch paragraph. These would settle PL-15’s quoted drift.