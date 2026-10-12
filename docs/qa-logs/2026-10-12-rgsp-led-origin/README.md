# RG SP LED preference origin — #561

The owner selected **Default** themselves after finding the saved preference was Red. Bounded read-only verification at 05:30:03 UTC confirms no `led.color` entry in live or recovery settings, green brightness1/red0, kernel triggers none, battery Discharging/93%, USB offline. The battery warning threshold is25. No agent setting, input or power action was sent.

## Actual behavior

The H700 platform lists default/off/green/red. `ledcontrol default` deletes the saved override and selects green; explicit red/green/off selects that output and persists the choice. The ES menu defaults an absent setting to Default and saves a selected value before calling ledcontrol. It does not declare red as a factory default. The 38 searched distribution/config/profile files have no `led.color` declaration.

The powerstate service checks every two seconds. While discharging, after at least20 iterations and at/below the configured threshold (25% when unset), it calls `led_flash`. H700 enables LED control but has `DEVICE_LED_CHARGING=false`; this path does not continuously map percentage or charging state to the red/green power LED. Hardware charging indication is a separate board behavior, not measured here. Default is green plus the low-battery warning, not an automatic graduated color scale.

## Origin evidence and a source-level lead

Earlier #534 evidence records red before and after the October9 update, and before/after the accepted October12 update. Those updates preserved the selection. The shared device-actions ledger and the four October12 stage/reboot ledgers were searched for ledcontrol/led.color/led_flash: one historical read-only battery diagnostic was found, with no direct agent LED-setting command in that inspected scope. This does not establish the first writer or prove all historical actions were logged. Do not infer that the owner selected red accidentally.

The inherited `led_flash` routine saves the prior preference in a process variable, then calls **the persistent** `ledcontrol red` setter while blinking. Only its later cleanup restores the original selection. Interruption after the setter and before restore can therefore leave a temporary warning value as the saved preference. This is a concrete source path to test, not a reproduced defect or proof of what happened on the RG SP. The H700 scripts and this flash routine are unchanged from the inspected upstream baseline through current next; a broader inherited issue is possible.

The flash condition checks whether DEVICE_LED_CHARGING is nonempty; the string `false` is nonempty. Record that branch in the fixture rather than silently treating it as a boolean. This may influence warning color, but does not itself identify the historical writer.

## Next proof

#561 owns source/action archaeology and a VM fixture for the real flash/control scripts with settings/sysfs boundaries adapted. Existing `tools/nova-led-test` demonstrates the fixture pattern but covers Nova, not this H700 flash. Exercise Default, Off, Green, Red; normal completion; termination at each setter/restore boundary; and reloading the saved preference. Preserve the unknown original cause separately from any reproducible software defect. A qualified fix must separate temporary indication from persisted user choice and preserve update settings. No product fix or runtime test is claimed in this report.

Can this be done on the VM? Yes for preference writes/interruption/command behavior. Only the observed physical LED/battery state required this device read. No new VM was started for the source investigation, and no repeated physical test is authorized.
