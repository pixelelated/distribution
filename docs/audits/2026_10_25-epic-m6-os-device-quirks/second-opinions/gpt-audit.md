*Model-directory citations are relative to `quirks/devices/`. `Nova/` means `Retroid Pocket Nova/`; `VM/` means `QEMU Standard PC (Q35 + ICH9, 2009)/`. I ran nothing; the conclusions below distinguish code traces, supplied fixture results, and device facts.*

## 1. The selection

**G-1 — confirmed — `002-autostart:6–12`; `autostart:20–43`; `quirks/package.mk:15–20`.**  
The selector uses DT `model` when that path exists, otherwise the DMI vendor/product pair, followed by slash-to-hyphen conversion. The startup loop executes direct, non-hidden entries satisfying `-f`, in shell glob order; this includes symlinks resolving to regular files, but excludes directories such as `bin/`. Platform quirks run before device quirks, and installation makes the copied regular files executable; no numeric filename prefix is required.

**G-2 — refuted — `system-utils/sources/scripts/ledcontrol:14–17`; `Nova/bin/ledcontrol:53–58`; `Nova/bin/analog_sticks_ledcontrol:28–40`.**  
The first reader is wrong that the wrappers’ unquoted `$*` is necessarily “load-bearing” for the seven numbers. In the shown call chain, `${LEDS_CONFIG}` is already split into arguments at the caller; forwarding those arguments with `"$@"` would preserve the seven-argument interface. Unquoted `$*` instead introduces another round of splitting and pathname expansion, while `"$*"` would incorrectly combine the arguments. Other callers should be checked before changing the wrappers, but the shown caller does not justify retaining `$*`.

**G-3 — narrowed — `0154-rocknix-dt-id.patch:39`; `sun50i-h700-anbernic-rg-sp.dts:10`; `autostart:31–43`; `platforms/H700/001-device_config:5–8`; `platforms/H700/010-led_control:5–9`; `Anbernic RG CubeXX/010-analog_sticks_led_control:5–7`; `Anbernic RG40XX V/bin/analog_sticks_ledcontrol:43–64`.**  
Against the supplied entry inventory, both owned H700 names select no device entry. The three matching H700 entries add stick-LED flags, control or achievements behavior, whereas the platform supplies the thermal/GPU and power-LED configuration; no omitted general-purpose quirk is identified by these bodies. That supports the static conclusion, not the unrestricted assertion that every hardware need has been established—the historical device facts are narrower (`docs/releases/device-facts.md:14,16`). The reported unset-flag diagnostic is also real: `platforms/H700/030-analog_leds:7–13` gives a malformed test under Bash when the flag is empty, returning an error and skipping the block.

**G-4 — confirmed — `sun50i-h700-anbernic-rg34xx-sp.dts:10`; `sun50i-h700-anbernic-rg34xx-sp-v2-panel.dts:10`; `qcs8550-ayn-thor.dts:11,358`; `AYANEO Pocket S Mini:1`; `Retroid Pocket 6 TOP-DPAD:1`.**  
The supplied model list’s arithmetic is right: 28 lines minus the repeated RG34XX-SP name and the non-board `AYN-Thor` sub-node gives 26 distinct board names. Its HAS rows total 15, including the two alias-selected names, leaving 11 NONE. This confirms the enumerated list and its arithmetic, not an independently rerun census of all DT sources or generated DTBs.

## 2. F-01: the Nova battery helper

**G-5 — confirmed — `Nova/bin/battery_led_status:69–85,114–133`; `tools/t29-battery-unset.py:28–45`; `stage-b/b04_fixture.out:1–4`.**  
With an empty expansion, Bash receives the three-argument test `! == battery`: the binary comparison is false, rather than a negated comparison against an empty string. Consequently the script enters the battery branch instead of breaking. For the fixture’s capacity 75 and Discharging status, the code writes brightness 255 and green intensity to all eight fabricated LED endpoints; that is a valid software result, not proof of physical illumination.

**G-6 — narrowed — `batteryledstatus.service:3–12`; `system-utils/sources/scripts/battery_led_status:10–17`.**  
The unit starts the wrapper when the unit is started, and its path condition checks only the wrapper’s existence—not whether battery mode was selected. However, `WantedBy=multi-user.target` is installation metadata, not evidence that the unit has actually been enabled or pulled into the boot transaction. The packet supplies neither its enablement call nor the installed wants-link, so “starts at every boot” is not established by this excerpt alone. Once started with the Nova identity, the wrapper does select the Nova helper.

**G-7 — narrowed — `Nova/010-analog_sticks_led_control:5–7`; `Nova/bin/ledcontrol:42–71`; `powerstate.sh:16`; `tools/t29-battery-unset.py:28,36–41`.**  
The displayed Nova startup paths do not seed `led.color`: the flag writer sets only the capability, and an argument-less Nova `ledcontrol` matches no case. But “nothing in the tree seeds it” is a wider negative claim than these excerpts establish; the real settings implementation, complete defaults and interface writer are not supplied. The fixture deliberately creates an empty settings file and replaces `/etc/profile`, so it proves the unset-input case, not that every fresh installation reaches that case.

**G-8 — narrowed — `Nova/bin/battery_led_status:14–23,72–81`; `Nova/bin/ledcontrol:68–71`; `batteryledstatus.service:9`; `docs/releases/device-facts.md:31`.**  
Quoting the variable—or using `[ "${BAT_LED_STATE}" != battery ]`—is a contained correction to this predicate. It also makes whitespace-containing or glob-containing values compare literally and makes an empty settings read terminate the helper successfully, rather than continue polling; `Restart=on-failure` would not restart that successful exit. Choosing battery through `ledcontrol` explicitly restarts the service, so that path remains available. The correction does **not** clear an already-lit LED state or apply another saved mode: the break performs no cleanup, so “the sticks stay dark” is too strong and remains a device-facts question.

**G-9 — refuted — `tools/t29-battery-unset.py:40–51`; `Retroid Pocket 6/bin/battery_led_status:11,75–76`.**  
The claimed RP6 fixture result is not reproducible by the supplied tool against the supplied, unmodified RP6 script. The tool substitutes only the profile and exports fixture paths, while RP6 overwrites `LED_PATH` and reads its battery from hard-coded `/sys` paths; its writes therefore cannot change the fixture files initialized to zero. An additional, unprovided path rewrite would be needed to substantiate that output, although RP6’s identical predicate is independently wrong by inspection. Also, this Python tool is a diagnostic, not a regression test: it prints results without asserting expectations or propagating the helper’s nonzero return code.

## 3. The fork-own five

**G-10 — narrowed — `VM/001-device_config:6–29`.**  
The every-boot heredoc is read correctly, but it contains **13** `DEVICE_*` assignments, not fourteen. It deliberately overwrites an image-owned profile file, so edits to that same file are not preserved. The literal thermal-zone glob and display defaults are configuration choices, not proof that those resources exist or behave correctly in a particular guest.

**G-11 — refuted — `VM/091-retired-vm-fixes:25–38,61–75,84–96`.**  
The first reader’s “every removal is named and hash-bound” and “No defect” conclusions are false. Without the stamp, the script checks only `-e` and then unlinks the named path, regardless of its contents; the hash and non-symlink checks belong exclusively to the stamped branch. A person can edit a file after the last old-image boot and then upgrade, or create it before this cleanup’s first run—the old quirks’ historical overwrites do not establish ownership at that point. This is a fork-own state-preservation defect, and its filename-only logging and stamp cannot reconstruct content already removed.

**G-12 — new — `VM/091-retired-vm-fixes:61–72,91–96`.**  
The “nothing remains” completion claim has another exception: `-e` treats a dangling symlink as absent, so a listed dangling link can survive while the stamp is written. First-pass cleanup should require positive ownership evidence too, or preserve unknown content before removal. Merely adding the hash guard is insufficient, because the final existence loop would then prevent stamping whenever an unknown regular file was correctly preserved. A host fixture should cover unstamped user content, both known hashes, stamped unknown content, dangling links and a missing previously-created stamp.

**G-13 — narrowed — `Nova/bin/ledcontrol:53–66`; `Nova/bin/analog_sticks_ledcontrol:11–45`.**  
The white fallback, immediate eight-LED brightness writes and exactly-seven-argument check are implemented as described. However, the first reader’s right-red example is wrong: a right RGB input of `255 0 0` produces the **BGR write `0 0 255`** at line 45, not `255 0 0`. The script checks argument count, not numeric ranges, and does not guard its output paths. This establishes the emitted channel order, not which physical colour the driver produces (`docs/releases/device-facts.md:31`).

**G-14 — new — `Nova/bin/ledcontrol:24–27,53–66`; `powerstate.sh:16`.**  
The brightness repair does not remain effective across RGB reapplication when a preset already exists. With a preset whose first field is 255, `ledcontrol brightness min` writes 32 and saves `min`, but the next `ledcontrol rgb` uses the preset’s 255 and never consults `led.brightness`. The startup call in `powerstate.sh` provides such a reapplication path when the saved mode is RGB. This is a reproducible saved-state disagreement for #332; whether the interface independently synchronizes the two settings is not shown.

**G-15 — new — `Nova/bin/battery_led_status:69,87–100,132–133`; `AYN Odin 2/bin/battery_led_status:78–94`.**  
There is a missed critical-battery recovery defect: process a Discharging sequence of 15%, 10%, then 15%. The first pass caches `D_RED`; the critical pass ends with LEDs off and `continue`s without invalidating that cache; the returning 15% pass therefore skips repainting and leaves the output off. The Odin 2 helper explicitly records `"critical"` before blinking and thus avoids this particular stale-state comparison. Quoting line 73 does not fix it; a multi-pass host fixture and cache invalidation are needed.

**G-16 — new — `Nova/bin/battery_led_status:82–85,95–129`; `AYN Odin 2/bin/battery_led_status:67–78`.**  
The Nova also lacks the Odin 2 helper’s battery-read validation. Under the same non-errexit Bash execution used by the fixture, an empty capacity with status Discharging makes each arithmetic threshold fail syntactically and then reaches the unconditional `D_GREEN` branch. A missing or unexpected status with a valid capacity can instead be treated as charging. Those are software failure-path defects, not evidence that a handheld currently returns bad data.

**G-17 — new — `Nova/bin/battery_led_status:72–74,87–94`; `Nova/bin/ledcontrol:43–59`.**  
Mode changes can lose to the critical-battery animation because the worker checks `led.color` only outside the five-blink batch, and the RGB/off cases do not stop it. Select RGB during an early blink sleep: RGB can be applied, then overwritten by the remaining battery writes, with the batch ending off. The next outer iteration sees RGB and exits without restoring it, leaving the saved mode and last output inconsistent. This needs a cancellation/coordination fix and a timed host fixture, separately from the unset-colour predicate.

## 4. Tier B’s brittleness

**G-18 — narrowed — `AYANEO Pocket S 2K/050-game-configs:6–7`; `AYN Thor/050-game-configs:8–20`; `autostart:35–40`; `AYN Odin 2/009-commander-cfg:6–11`.**  
The rewrites do run each boot and overwrite existing lines matching those exact expressions; they do not insert missing keys, and a missing file produces unchecked `sed` errors. The first reader’s proposed “009 shape” is not a drop-in fix: guarding these `sed` commands with “file does not exist” would skip existing files and fail on absent ones. Defaults must instead be applied at creation or through an explicitly bounded migration/default policy. Preventing future overwrites cannot recover an earlier user value from the now-rewritten configuration; that file is also in the backup selection (`backuptool:288`).

**G-19 — narrowed — `AYANEO Pocket EVO/bin/ledcontrol:99–102`; `AYN Odin 2 Portal/bin/ledcontrol:25–28`; `AYANEO Pocket DMG/bin/analog_sticks_ledcontrol:10–14`; `AYN Odin 2 Portal/bin/analog_sticks_ledcontrol:28–32`.**  
The unset-preset call is defective, but “turns them off” is not what these branches do. They invoke the helper with no arguments, which rejects the call without performing LED writes; whatever state previously existed can remain. The enclosing `ledcontrol` then has no local success check before saving RGB mode. Thus the software evidence is failed application and incorrect state reporting, not unconditional darkness.

**G-20 — narrowed — `call_achievements_hooks.sh:8–17`; `Anbernic RG CubeXX/bin/achievements:91–100`; `platforms/H700/bin/ledcontrol:14–44`; `AYANEO Pocket ACE/bin/ledcontrol:18–40`; `AYANEO Pocket EVO/bin/ledcontrol:18–21`.**  
The achievements hook is explicitly enabled by its own setting, rather than running unconditionally. With an unset preset, restoration fails and the last animation output can remain; with a valid preset, it requests that preset, **not** the rainbow’s last colour. The first reader therefore overstates the off/battery consequence. Moreover, `led.color` controls the power LED rather than the sticks on H700 and the ACE-derived Odin 2/DMG controller, so ignoring it is not universally a stick-restoration defect; EVO couples that mode to its sticks and needs separate treatment.

**G-21 — narrowed — `Nova/bin/ledcontrol:21–28`; `Nova/bin/battery_led_status:77–81`; `AYN Thor/bin/battery_led_status:13–22`.**  
The two dialects are real: Nova maps words to fixed values, while Thor interprets a numeric percentage. For example, numeric `50` takes Nova’s 255 fallback, and `mid` takes Thor’s 100%-brightness fallback. That is an interface-contract risk, but the supplied code does not identify which values the interface actually writes on each board. It is not yet a demonstrated explanation of the physical brightness-row symptom.

**G-22 — new — `AYN Thor/bin/battery_led_status:16–22,48–56,123–142`; `AYN Thor/bin/ledcontrol:20–45`.**  
Thor’s percentage support has an additional update defect: `led_bri` is called only when a colour-paint function runs, not on every polling pass. Changing only `led.brightness` while the battery remains in the same bucket therefore causes no new brightness write, and the shared `ledcontrol` has no `brightness` case to apply it immediately. If the caller only updates the setting, the change waits for a bucket transition or worker restart, not merely the next 15-second poll. That limitation is absent from the first reader’s account.

**G-23 — confirmed — `AYANEO Pocket ACE/020-set-xbox-gamepad:7–15`; `AYANEO Pocket DMG/bin/analog_sticks_ledcontrol:45–66`; `Anbernic RG40XX V/bin/analog_sticks_ledcontrol:43–64`; `Powkiddy x55/040-hdmi:6–13`.**  
The cited tier-B paths have no node-existence/type guard and do not check the serial setup before sending. If the containing directory is writable, `>` and `<>` can create an ordinary file at an absent `/dev` pathname; an absent sysfs attribute instead causes a write failure. The x55 excerpt is a genuine guarded counterexample. These establish conditional failure modes, not the first reader’s unsupported reassurance that the relevant nodes necessarily exist whenever these boards run.

**G-24 — new — `AYANEO Pocket ACE/bin/battery_led_status:59–74,106–107`; `AYANEO Pocket EVO/bin/battery_led_status:64–79,111–112`; `AYN Odin 2 Portal/bin/battery_led_status:78–93,125–126`; `AYN Thor/bin/battery_led_status:94–109,141–142`.**  
The critical-recovery defect in G-15 is not confined to the fork-owned Nova file. These upstream tier-B implementations have the same blink-to-off, `continue`, and unchanged-cache pattern, including their shared-file consumers. This is a concrete software defect on entries selected by shipped images, beyond F-03–F-07—not merely a naming inconsistency or a hypothetical missing node. Their fixtures must first redirect all hardware paths correctly; the supplied RP6 fixture invocation does not do that.

**G-25 — confirmed — `AYN Thor/touchcontrol:4–17`; `autostart:35–40`; `Anbernic RG40XX V/bin/analog_sticks_ledcontrol:6–7,26–31,50–60`; `AYN Odin 2/bin/analog_sticks_ledcontrol:6–7`.**  
The first reader correctly corrected the brief about `touchcontrol`: it is executable startup content that writes a rule, reloads udev and triggers input devices. RG40XX V really parses right-side colours but constructs its payload solely from left-side values; without a hardware/interface requirement, that is not enough to call the mapping wrong. The copied battery descriptions are at lines 6–7, not the cited copyright/header lines. The filename-spelling counts remain reported inventory figures; the startup rule does not distinguish those spellings.

## 5. Currency

**G-26 — narrowed — `quirks/package.mk:15–20`; `autostart:35–40`; `Retroid Pocket 6 TOP-DPAD:1`.**  
The supplied diff table totals 31 paths, but the 18/12 commit counts and “no upstream Nova change since base” remain reported history: the underlying log is not included for independent verification. Neither panel-calibration file’s body is supplied, so its calibration behavior cannot be reviewed here. The code does establish that adding those regular `040` files to the existing entries makes them installed and selected, including RP6 through its TOP-DPAD alias. “Settled by the next base merge” is therefore a reasonable import disposition, not evidence that calibration has been tested or that a merge has already settled it.

**G-27 — confirmed — `002-autostart:6–12`; `rocknix-info:3–12`.**  
Both derivations perform slash-to-hyphen conversion; the brief’s contrary claim was wrong, and the first reader corrected it. Their DT **and DMI** readers differ: `strings` filters/splits printable runs, whereas `tr -d '\0'` removes NUL bytes without that filtering. Both subsequently use an unquoted `echo` expansion, which can normalize whitespace and expand glob characters, so agreement for the supplied model names is not a general equivalence proof. `rocknix-info` recomputes its own value after sourcing the profile; that is not a replacement for the startup selector.

## 6. Verdict on each finding F-01 to F-10

**G-28 — narrowed — F-01 — `Nova/bin/battery_led_status:72–81`; `batteryledstatus.service:4–12`; `docs/releases/device-facts.md:31`.**  
The empty-value Bash defect and the Nova fixture’s writes are confirmed. The universal fresh-boot/physical-lighting claim is not: enablement, actual initialization and physical illumination are separate questions, and quoting the predicate does not actively turn anything off.

**G-29 — narrowed — F-02 — `autostart:31–43`; `platforms/H700/001-device_config:5–8`; `platforms/H700/010-led_control:5–9`; `Anbernic RG CubeXX/010-analog_sticks_led_control:5–7`.**  
The two owned names have no entry in the supplied inventory, and the other H700 entries contain the additional stick-LED behavior described. Keep the conclusion as “no missing device-entry functionality identified,” not proof of every hardware need or of the behavior of all platform helpers.

**G-30 — narrowed — F-03 — `AYANEO Pocket S 2K/050-game-configs:6–7`; `AYN Thor/050-game-configs:8–9`; `AYN Odin 2/009-commander-cfg:6–11`.**  
The matching-key overwrites and user-setting loss are real. The once-created commander file is a useful ownership contrast, but not the proposed ready-made fix for `sed` on RetroArch’s existing configuration; lack of an owned handheld is also not a valid dismissal of the software behavior.

**G-31 — narrowed — F-04 — `AYANEO Pocket EVO/bin/ledcontrol:99–102`; `AYN Odin 2 Portal/bin/ledcontrol:25–28`; `Anbernic RG CubeXX/bin/achievements:99–100`.**  
The unset-preset failure is confirmed, but it means “no new write,” not necessarily “turned off.” The achievements conclusion must distinguish unset from valid presets and distinguish power-LED modes from stick-LED modes; its blanket “off/battery leaves the last rainbow colour” claim is wrong.

**G-32 — narrowed — F-05 — `Nova/bin/ledcontrol:21–28`; `AYN Thor/bin/battery_led_status:13–22,123–142`.**  
The incompatible interpretations are confirmed. Which interface path supplies which representation is still missing, and Thor additionally fails to apply a setting-only change while its cached battery bucket remains unchanged.

**G-33 — confirmed — F-06 — `AYANEO Pocket ACE/020-set-xbox-gamepad:10–15`; `AYANEO Pocket DMG/bin/analog_sticks_ledcontrol:45–66`; `Powkiddy x55/040-hdmi:6–13`.**  
The unguarded operations and the possibility of creating a regular `/dev` file are correctly identified. Treat this as a conditional code risk; the supplied excerpts establish neither actual missing nodes on a unit nor an independently recounted tree-wide total of guard patterns.

**G-34 — confirmed — F-07 — `AYN Thor/touchcontrol:4–17`; `autostart:35–40`; `Anbernic RG40XX V/bin/analog_sticks_ledcontrol:26–31,50–60`.**  
The execution-rule observation and unused right-side parameters are real informational findings. The latter should remain informational unless a supported interface or device requirement establishes that a distinct right-side output must exist.

**G-35 — narrowed — F-08 — `quirks/package.mk:15–20`; `autostart:35–40`; `Retroid Pocket 6 TOP-DPAD:1`.**  
The import/selection implications are supported, and nothing here contradicts the reported pending-history figures. But the packet does not independently prove those history counts or the contents/effectiveness of the two panel additions; retain the merge disposition without calling it a completed correctness proof.

**G-36 — confirmed — F-09 — `002-autostart:6–12`; `rocknix-info:6–12`.**  
There are two different readers and both contain the slash conversion. Their agreement for the listed names does not remove the latent difference on short, non-printable or NUL-separated data, including DMI values.

**G-37 — narrowed — F-10 — `quirks/package.mk:15–20`; `autostart:31–43`.**  
The code supports “installed by placement, executed by selection,” and nothing here warrants deleting the upstream-carried entries. However, A is contained in B: the disjoint path accounting is **6 + 64 + 263 = 333**, not a partition of 6/70/263; that is a presentation correction to `04`’s efficiency summary, not an inventory failure. The byte total remains the supplied inventory measurement, not an independently measured installed-image cost.

## 7. What the first reader missed

**G-38 — new — `AYANEO Pocket S Mini:1`; `AYANEO Pocket S 2K/050-game-configs:6–7`; `Retroid Pocket 6 TOP-DPAD:1`; `Retroid Pocket 6/bin/ledcontrol:25–28`; `AYANEO Pocket DMG/bin/battery_led_status:1`.**  
Affected file counts must not be substituted for affected model counts. Four tier-B directories with the RetroArch rewrites cover five selected model names once S Mini is included, and the four RGB-default-hole directories likewise cover five names once TOP-DPAD is included. DMG also inherits ACE’s unquoted battery predicate through its file symlink. The inventory knows these aliases, but the findings’ impact summaries do not consistently carry their reach through.

**G-39 — new — `002-autostart:6–12`; `rocknix-info:6–12`; `system-utils/sources/scripts/battery_led_status:14–17`.**  
An existing-but-empty or unsuccessfully-read DT model is a missing selection test case. Both derivations decide whether to use DMI from path existence, not read success or a nonempty result, so neither falls back to DMI in that situation. The wrappers can then use the platform implementation rather than a named device implementation. This is a directly testable selection edge, not evidence that any current handheld’s model property is defective.

**G-40 — refuted — `quirks/package.mk:15`; `autostart:31–40`; `VM/091-retired-vm-fixes:61–72`; `Nova/bin/battery_led_status:87–100`; `docs/releases/device-facts.md:31`.**  
The first reader’s blanket disposition—upstream tier-B behavior is “not a bug here” because the fork does not own or ship those boards—is wrong: tier B is selected by boards the shipped images support, and ownership limits physical testing, not software relevance. The highest-priority correction is the VM cleanup’s deletion of unknown user content, followed by the fixture-testable battery caching and mode-change defects. Assess those against the contained-fix/host-proof standard rather than automatically assigning them to renovation. Keep actual illumination and on-unit application on #332’s device-facts row; none of the software traces closes that open item.