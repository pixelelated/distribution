## 1. New findings

Package paths below are relative to `projects/ROCKNIX/packages/`. `installer`, `111-sway-init`, and `sway-ready` denote the corresponding full paths printed in the packet. “Diff” citations refer to the supplied `git diff upstream/next 8ebaf8daad -- <path>` output. Conditional failures below are static deductions, not observed image failures.

- **G-01 — High — `installer:200–376`:** Destructive installation has no checked success path. Failures of `dd`, partitioning, formatting, mounting, or copying can be followed by “Install Complete”; the progress pipeline does not explicitly propagate the producer’s failure. A failed mount also lets subsequent copying target the ordinary temporary directory instead.

- **G-02 — High — `installer:89–118,142–143,207`:** Target exclusion is based on textual mount-source names, not the underlying block-device graph. A disk backing `/dev/mapper`/MD mounts, or active swap, can remain selectable and reach the wipe. The unanchored substitutions also confuse names such as `/dev/sda` and `/dev/sdaa`, especially when processing several mounted partitions of one disk.

- **G-03 — Medium — `installer:173–180,207,280–289`:** `PARTID` is set to `p` for MMC/NVMe but never reset for an ordinary disk. Select an MMC/NVMe device, cancel a confirmation, then select `/dev/sda`: the installer can wipe `/dev/sda` and subsequently address nonexistent `/dev/sdap1` and `/dev/sdap2`.

- **G-04 — Medium — `installer:241–261,416–420`:** Partition sizing assumes 512-byte sectors while passing the result to `parted unit s`; a 4Kn target gets an oversized system partition or partitioning failure. Separately, flooring capacity to decimal GB and testing `>=2200` switches to GPT later than the script’s own stated \(2^{41}\)-byte DOS limit.

- **G-05 — Medium — `installer:321–339,518–530`:** Generated Syslinux/EFI files are installed **before** recursively copying `/flash/*`, which can overwrite them with installation-media configuration. When those source files exist, source boot arguments or installer settings can survive; the parsed alternate kernel/system image names are not used by the shown generated configuration.

- **G-06 — Low — `installer:43–46,553–558`:** The controller helper is backgrounded without retaining its PID or installing exit cleanup. The cleanup after the unconditional main loop is unreachable. Termination outside the intended poweroff path therefore has no script-level guarantee of releasing the helper.

- **G-07 — Medium — `sway-ready:16–29`:** The fallback Wayland/runtime-directory values are used to construct socket paths but are not exported or passed to `wlr-randr`. If the corresponding environment variables are absent or unexported, the socket test and the Wayland client can address different sessions, causing a false readiness timeout.

- **G-08 — Low — `sway-ready:7,21–35`:** Fifteen seconds is not a hard execution bound. The deadline is checked only between iterations; an in-flight timeout, its kill grace, `jq`, and the final sleep can extend it. Profile sourcing occurs before the deadline is established and is also unbounded.

- **G-09 — Medium — `111-sway-init:28–56`:** DRM selection takes the first connector name before checking connectivity and extracts only one digit of its card number. A disconnected first GPU can hide a connected later GPU; `card10` becomes `card1`. Selecting the last connected glob entry also does not implement the comment’s general HDMI/DP priority.

- **G-10 — Medium — `111-sway-init:87–90,113–127,143–159`:** `WLR_CON` is written before the Retroid add-on and Pocket DS branches change `con`. Whenever those branches change the selected connector, consumers of the environment file see a different primary output from the subsequent configuration and SDL priority.

- **G-11 — Medium — `111-sway-init:75–80,203–213`:** With an external output selected, the internal panel is explicitly disabled. The Pocket S 2K override can then designate that same internal panel as primary without re-enabling it, and reuses the external-output rotation decision.

- **G-12 — Low — `111-sway-init:156–173,186–200`:** Dual-screen configuration assumes a second connected connector exists. If only one is enumerated, it emits empty-output commands and an incomplete display-priority value rather than rejecting or falling back from that topology.

- **G-13 — Low — `111-sway-init:143–150`:** `pgrep -x /usr/bin/wvkbd-mobintl` tests a full pathname against the process-name field, not the command line. An ordinarily named running keyboard therefore does not satisfy the Pocket DS test that should power its display on.

- **G-14 — Low — `network/avahi/system.d/avahi-daemon.service:3–8,20–21`:** `After=network-base.service` neither pulls that service into the transaction nor requires it to succeed. Starting Avahi without a queued/successful hostname setup can violate the unit’s advertised “after the device has its name” contract; other units may close this gap, but none is supplied.

- **G-15 — Medium — `apps/mangohud/package.mk:66–91`:** Three configure-time `curl` downloads—ImGui, ImPlot, and spdlog—remain outside the declared, checksum-checked source mechanism. Offline configuration can fail, and changed tag archives can enter the build without verification. The Vulkan subproject checks at `:58–63` do not cover these downloads, nor does T5’s archive guard.

- **G-16 — Medium — `virtual/image/package.mk:109–110`:** Independently of F-02’s load-time placement, `ln -sf` is not safe destination replacement: an existing destination directory, or symlink to an existing directory, is followed. It can create a nested link outside the staging tree if that directory resolves onto the host. An empty `INSTALL` also makes the destination `/opt`. Merely moving these commands into a hook does not address these cases.

- **G-17 — Medium — `network/tailscale/package.mk:15–30`:** Architecture-specific archives have different hashes but the unpack hook names one architecture-independent cache file, `tailscale-${PKG_VERSION}.tgz`. With shared `SOURCES`, the variants cannot coexist there; concurrent fetch/unpack needs an exclusion guarantee or one plan can consume another architecture’s replacement archive.

- **G-18 — Medium — `compat/box86/package.mk:18–29,70–86`; `compat/lib32/package.mk:8,22–25`:** These recipes consume another architecture’s build/install tree without expressing that cross-root dependency here. Box86 additionally selects donor directories with version wildcards. Missing donor artifacts fail a clean isolated build; retained multiple versions can make copies fail or mix provenance. Existing stamps do not establish the required ordering or donor identity.

- **G-19 — Medium — `compat/lib32/package.mk:32–39`:** The ICD-copy loop silently skips manifests whose `library_path` has no slash. For a donor using a filename-only library reference, the library can be copied into the bundle while its ICD is omitted, with no postcondition checking that the corresponding 32-bit driver remains discoverable.

- **G-20 — Medium — `scripts/get_archive:4–11`; `52e6794ba7:scripts/get_archive:11–18`:** Both cache-hit paths trust the stored checksum stamp without hashing the cached archive. Corruption or replacement of the archive while its stamps remain intact is accepted, including by the supplied T5 implementation. This is distinct from a recipe lacking a checksum.

- **G-21 — Medium — supplied diff for `devel/glibc/package.mk`, hunks at `+60` and `+70`:** The current `s|-O.|-O3|g` transformation turns `-Ofast` into invalid `-O3ast`; it also leaves separately supplied `-ffast-math` intact. Builds using those flags can fail. The incoming diff contains a materially different, explicit treatment of both cases.

- **G-22 — Medium — `network/simple-http-server/system.d/simple-http-server.service:7` (diff):** The root password’s command substitution is unquoted inside the shell command. A password containing whitespace or glob characters can become multiple or altered arguments instead of the intended authentication value. This is argument splitting, not proof of shell-command injection.

- **G-23 — Medium — `wayland/util/wlr-randr/profile.d/010-wlr-randr:7–11` (diff):** The resolution parser takes a line after **every** `Modes` block and expands the result unquoted. If the returned report contains multiple outputs, the refresh-rate command receives multiple resolution words rather than one mode for the selected output.

- **G-24 — Low — `apps/m8c/config/GENERIC_X64/config.ini:30–31`:** Decrease-jazz-velocity and toggle-audio share scancode `69`. This is a binding collision requiring an intentional mode-exclusion explanation; if both handlers are active in the same context, the actions cannot be selected independently.

- **G-25 — Low — `scripts/update_packages:18–32`:** The missing-package guard cannot catch a failed directory lookup: `p` is nonempty in this loop, and `f` has already acquired `/package.mk`. A missing match therefore becomes `/package.mk`, not “skip”; multiple directory matches are likewise not rejected before sourcing/editing.

- **G-26 — Low — `q4-table.md:10,193,229,234`; supplied `gamepadtester`, `atf`, and `wlroots` diffs; `sway/package.mk:12–21`:** Several “upstream pin” summaries are branch literals, not demonstrated effective pins for all three plans. The shown newer GamepadTester and wlroots pins are device-specific, and ATF remains 2.10.0 outside H700. The supplied `effective.txt` “pins differ” extract also omits ATF. These summaries are unsafe as uniform post-merge pin predictions.

- **G-27 — Medium — `graphics/glslang/package.mk:7–9,18,35–38`; `graphics/spirv-tools/package.mk:18,36–40`; `base-merge.txt` (`spirv-headers`):** The proposed two-recipe shader-tool resolution omits a simultaneous **third** modify/delete conflict, `spirv-headers`. Resolving glslang and SPIRV-Tools together is insufficient to establish that the required three-way pin relationship survives the merge.

## 2. Refuting the first reader

### The findings

- **F-01 — Agree with the checksum defect; narrow the reach and closure claims.**  
  The missing x86_64/arm checksums are explicit at `network/simple-http-server/package.mk:12–23`; T5 refuses them at `scripts/get_archive:7–8`. False if the active branch supplies a checksum or the package is not reached. `virtual/network/package.mk:25–27` is conditional, not “every image” by itself. `effective.txt` confirms the GENERIC_X64 gap, but the #890 fix bytes are not supplied.

- **F-02 — Agree, Medium.**  
  False if the commands execute only inside an installation hook. They are visibly global at `virtual/image/package.mk:109–110`, and the reported `config/options` result—the three staging-tree symlinks—corroborates the side effect. G-16 is an additional destination-safety problem, not a reason to withdraw F-02.

- **F-03 — Agree, Low, as an observed unavailable primary URL.**  
  False if the configured origin successfully serves the expected archive. `devel/libaio/package.mk:10` matches the URL that returned 404 in `probe/head.txt`; the packet also reports a ranged-GET 404. The reported mirror `sha256sum` match mitigates availability risk; it does not refute the primary-URL defect or prove permanent disappearance.

- **F-04 — Agree, Low, with the same temporal qualification.**  
  False if the configured asset is available with the expected bytes. `tools/rocknix-abl/package.mk:5–8` and `probe/head.txt` support the observed 404; the reported mirror hash matches `:6`. Neither a currently working mirror nor the proposed `openabl` migration establishes that the existing primary works.

- **F-05 — Low, but the “behind” comparison remains independently unverified here.**  
  The installed pin is unquestionably 1.18.4 (`graphics/cairo/package.mk:16–20`). False if 1.18.6 is not the applicable stable release, or an intentional constraint requires the older pin. `q4-table.md:103` asserts the release-listing result, but the packet supplies neither that listing nor its raw command output. The recipe explains a minimum-version requirement, not an indefinite hold (`:7–15`).

- **F-06 — Agree with the structural limitation, Low; correct its scope.**  
  False if selection includes modified shared paths or parsing resolves their effective values. The added-only selector and lexical reader are explicit (`tools/fork-package-freshness:46,89–92`). But “all 19 edited recipes are outside its set” is false: `q4c.txt` includes edited orphans `glslang` and `rocknix-abl`. It also hides libfmt’s effective 9.1.0 override behind `INHERITED` (`effective.txt`; `q4-table.md:85`). The precise Rust `LOCAL` misclassification still needs the omitted URL/verdict code and recipe bytes.

- **F-07 — Agree, Low; do not imply an observed collision or compromised fetch.**  
  False if these are merely display abbreviations of full recipe pins, or the applicable rule permits abbreviations. `q4c-hash.txt` supplies seven-character pins for all six named packages while printing full pins for other recipes. That supports the short-pin finding; it shows no ambiguity or collision at the audit time.

- **F-08 — Agree, Low, against the checker rather than Moonlight.**  
  False if both definitions execute in one branch or the checker understands mutually exclusive definitions. `apps/moonlight/package.mk:12–45` establishes the `if`/`else`; `tools/pkgcheck:147–150` establishes the whole-file textual duplicate test. The reported failure is therefore not evidence of duplicate runtime behavior.

- **F-09 — Agree, Low, as integration work—not nine demonstrated runtime defects.**  
  False for these exact heads if the reported conflicts do not exist, or if a resolved merge has already replaced this simulation. `base-merge.txt` confirms the nine relevant conflicts. The packet contains no resolved merge. GCC’s unexplained local hold is visible at `lang/gcc/package.mk:4–8`; the adequacy of its history is not independently shown.

- **F-10 — Agree with the dangling invocation, Low; reject the blanket unreachability argument.**  
  False if the script is installed/generated before activation, or the unit/rule cannot activate on the supported hardware. `units-exec.txt` reports the absent executable, and the service/rule explicitly connect it to matching PCI devices (`xorg-configure@.service:8`; `97-xorg.rules:8,13–17`). A statement about one virtio GPU’s class cannot establish that no GENERIC_X64 deployment matches those rules.

- **F-11 — Agree, Medium, but strictly conditional on resolution.**  
  False as a downgrade if the override is retained or the generic pin is raised; false as a compatibility failure if the chosen combination is compatible. The generic 16.5.0 and local 16.6.0 are explicit (`upstream/next:packages/graphics/vulkan/glslang/package.mk:9`; local `:10`). Crucially, `base-merge.txt` says **our version is left in the tree**. No automatic or silent downgrade occurred, and no compilation failure is proved. Include G-27’s headers conflict.

- **F-12 — Retain Low as an inventory/review item; disagree with its unconditional outcome.**  
  False that all eleven are automatically dropped if modified overrides remain unresolved—and `base-merge.txt` explicitly shows that for glslang and rocknix-abl. Matching dependency names also does not establish API compatibility, and does not cover a rename to `openabl`. The “after” values need the qualifications below.

### The eleven conflict dispositions

The conflict messages establish the nine conflicts, not the correctness of their resolutions or the resulting build. The packet does not supply all eleven upstream/base hunks or the two automatically merged file bodies (`base-merge.txt`).

1. **Gamescope — Narrow.** Preserve the fork’s dependency preparation **and** the incoming pin, rather than interpreting “keep ours” as whole-file checkout. The revision guards are useful (`apps/gamescope/package.mk:50–61`), but neither those guards nor the reported wrap agreement prove “the auto-merge builds.” The wrap API payloads and a build are absent.

2. **Cairo — Conditional, incomplete as written.** Keeping xcb/xlib-xcb options also requires keeping their dependencies for Wayland, not only Meson switches (`graphics/cairo/package.mk:33–36,56–65`). The upstream sourcing shape and final generic pin are not supplied sufficiently to sign off the result.

3. **glslang — The warning holds; the predicted deletion does not happen automatically.** The supplied generic is 16.5.0, but the modify/delete output leaves our 16.6.0 file in the tree (`base-merge.txt`; generic `package.mk:9`; local `:10`).

4. **SPIRV-Tools — Resolve a triple, not a pair.** Include SPIRV-Headers and preserve or deliberately retire the GCC-12 host workaround (`graphics/spirv-tools/package.mk:26–40`; `base-merge.txt`, headers conflict). “Resolve with glslang” alone is insufficient.

5. **GCC — Incomplete.** The fork enables libatomic for **arm as well as aarch64 and x86_64**, and conditionally installs it (`lang/gcc/package.mk:10–17,77–86`). Adopting an aarch64-only restructuring plus the x86_64 case would lose the ARM case. Also inspect inherited generic state before deciding whether the 15.2.0 hold can remain.

6. **`gamelist.xml` — Preserve the merged changes, not the entire ours file.** Ours still contains the AetherSX2 entry (`misc/modules/sources/gamelist.xml:171–183`). If upstream’s reported removal is intended, whole-file “keep ours” would restore it. Coordinate that decision with the emulator’s separate modify/delete conflict in `base-merge.txt`.

7. **gst-plugins-base — Preserve build enablement as well as installation.** The recipe needs `-Dapp=enabled`, its GL dependencies, and the retained payload (`multimedia/gstreamer/gst-plugins-base/package.mk:8,31–35,93–108`). Keeping only the install hook while restoring disabled app-plugin options would make its own required-payload check fail.

8. **GStreamer — Correct the claimed distinction.** Ours already removes `/usr/share` (`multimedia/gstreamer/gstreamer/package.mk:49–53`). That removal is not an unexamined upstream-only behavior. Preserve both registry and tools/scanner enablement (`:18,23,36`), not merely “the registry.”

9. **NetworkManager — Plausible, not independently established as “same change.”** Our required value is explicit (`network/networkmanager/config/NetworkManager.conf:8–13`). The upstream hunk is absent. Dropping a redundant comment is harmless only after confirming that the resolved configuration retains `hostname-mode=none`.

10. **rocknix-abl — Make migration verification a prerequisite to deletion.** The current payload and path are explicit (`tools/rocknix-abl/package.mk:12–17`), while `base-merge.txt` leaves ours unresolved. No supplied `openabl` recipe or SM8550 bootloader consumer proves that taking deletion is safe.

11. **`111-sway-init` — “Both” is not yet a resolution.** Ours already masks/unmasks essway and contains Thor Lite handling (`:19–26,83–85,186–200`), so these cannot simply be treated as absent additions. Preserve Virtual detection/software cursors (`:31,59–63`); obtain the actual upstream AFBC/device hunks and address G-09 through G-13 before declaring the union safe.

### The orphan “after the base merge” column

- **It does not hold unconditionally.** On the reported classification, nine deletions are uncontested; glslang and rocknix-abl are explicitly retained as unresolved modify/delete cases. Those two cells must describe **a chosen deletion resolution**, not the merge’s automatic result (`base-merge.txt`).

- **Most replacement pins are reported, not independently demonstrated by supplied generic bytes.** The generic glslang 16.5.0 is shown. Libfmt 12.2.0 is demonstrated as the *current SM8550 effective value*, not as a resolved post-merge expansion for all plans (`effective.txt`). The remaining generic replacement values need their source/output evidence.

- **Cargo’s cell is not an effective pin.** `$(get_pkg_version rust)` is an expression requiring evaluation in the merged tree (`q4-table.md:179`). Consequently, the count of five changes is not a complete demonstrated post-merge census: it excludes the separately discussed conditional glslang downgrade and leaves Cargo’s result unresolved.

- **“Dependants resolve by name” is too weak.** It says nothing about the compatibility of libfmt 9→12 or other replacement implementations; it does not establish the rocknix-abl→openabl migration at all (`q4-table.md:85,210`; `tools/rocknix-abl/package.mk:12–17`).

### Q4 `current` claims and the update mover

- **No unsupported literal `current` claim is apparent in the supplied Q4 rows.** Rocknix-splash’s `current` has an `identical`, zero/zero comparison to the recipe’s own repository (`q4c-hash.txt`, rocknix-splash; `tools/rocknix-splash/package.mk:5–9`). The project-column `CURRENT` values for glslang and tllist have corresponding `q4c.txt` outputs. These establish the stated snapshot comparisons—not universal freshness or release suitability.

- **The demonstrated table defect is elsewhere:** branch literals and sourcing conversions are not sufficient evidence of effective post-merge pins; see G-26. Likewise, `INHERITED` is not a substitute for reading post-source overrides, particularly libfmt (`effective.txt`; `q4c.txt`).

- **Eleven eligible recipes does not mean eleven actual pin changes or eleven archive-fetch refusals.** Several selected hash pins already compare identical to HEAD, and the script explicitly skips changing an equal pin (`q4c-hash.txt`; `scripts/update_packages:36–45`). The update-set contains nine hash pins, not eleven; Moonlight uses a git URL (`apps/moonlight/package.mk:32–34`), so T5’s *archive* checksum guard does not establish its refusal.

- **The updater is worse on failure than “moves to branch head” suggests.** For archives, checksum deletion is outside the successful-version-lookup branch; even a no-op or failed lookup reaches it. The later substitution expects an empty checksum assignment that the preceding deletion removed (`scripts/update_packages:36–61`). This strengthens the already acknowledged updater/checksum problem, rather than proving a successful eleven-package update.

## 3. What I could not judge

- **Actual readiness wiring and session identity.** Installing `sway-ready` is shown, but its caller, essway’s gating/restart behavior, `/etc/profile`, and the actual compositor socket configuration are not (`sway/package.mk:42–49`; `sway-ready:5–20`). I cannot establish that its failure stops ES, that its defaults match the running compositor, or that its output check observes the intended session.

- **Runtime display behavior and configuration intent.** No connector census, generated Sway configuration, or device execution accompanies the topology-sensitive branches (`111-sway-init:31–56,113–224`). M8C’s handlers are also absent: G-24 is a demonstrated binding collision, not proof that both actions fire together (`config.ini:30–31`).

- **Avahi’s complete dependency and off-switch contract.** The defaults service, hostname-setting service, notification callback, and image drop-ins are missing. They may compensate for G-14 or expose other ordering failures (`avahi-daemon.service:6–8`; `network/avahi/package.mk:102–118`). Directive acceptance does not establish those semantics.

- **Installer platform assumptions and failure containment.** `/etc/installer.conf`, the bootloader update helper, actual device graphs, and launcher/unit behavior are absent (`installer:33,89–118,310`). The script also uses `source` and substring expansion under `/bin/sh` (`:1,40,524,528`); whether that fails depends on the image’s actual shell, which the packet does not establish.

- **Complete post-source override state.** GCC visibly resets version, checksum, and URL coherently (`lang/gcc/package.mk:4–8`); that alone does not reveal generic fields or hooks already derived from the original version. The other five resetting overrides are not supplied in full. I need current and merged generic bytes plus effective source names, URLs, checksums, dependencies, and hook options—not merely an absence of assignments before sourcing.

- **Merged build/ABI compatibility.** The wrap payloads, exact `known_good.json`/SPIRV-Tools `DEPS` contents, most generic replacement recipes, and resolved merge tree are missing (`gamescope/package.mk:50–61`; `glslang/package.mk:7–9,18`; `base-merge.txt`). Pin-policy comments establish a coupling requirement, not that a particular mismatched combination fails to compile.

- **Full source availability and artifact integrity.** The 82 HTTP-200 responses were not byte-verified by the reported sweep (`probe/head.txt` histogram). `probe/git.txt` proves ref advertisement, not successful acquisition of every pinned commit and its submodules. `record-stamps.txt` proves stamp presence, not matching recipe provenance, architecture, runnable binaries, or ABI correctness.

- **Fix closure and some checker exonerations.** The #890 fix and final #852 patch are not supplied; T5’s excerpt shows the checksum gate but not its claimed TLS changes (`52e6794ba7:scripts/get_archive:1–20`). The WirePlumber heredoc sites are also missing, so its reported parser failures cannot all be independently dismissed from the supplied FAIL lines.

- **Coverage and currency beyond the delivered evidence.** The asserted inventory counts do not substitute for omitted file bodies, generated coverage rows, generator logic, or release-source receipts. In particular, Cairo’s latest-release assertion lacks its raw listing, while the non-GitHub hash comparisons explicitly remain unknown (`q4-table.md:103`; `q4c-hash.txt`). I would not extend this second reading into certification of all 485 paths or all three images.