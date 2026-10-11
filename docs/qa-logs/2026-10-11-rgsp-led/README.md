# RG SP red LED read-only diagnosis — #534

At2026-10-11T03:24:12Z both live and recovery settings selected `led.color=red`.
The existing pre-update preservation receipt also records red before and after
the8b511 update. Green brightness0/red1 and kernel trigger `none` agree with a
fixed software selection. Battery status Discharging, USB offline, raw capacity
100 and warning threshold25 do not support a current low-battery indication.
The owner saw97%; a later `/tmp/battery.percent` read was94. The shared
`battery_percent` reader prefers that cache over raw sysfs. The readings were
not simultaneous and no battery-accuracy claim is made.

The installed `/usr/bin/ledcontrol` is a dispatcher, not the H700 implementation.
The actual H700 implementation hash matches source; its red branch selects red
and persists the preference, while default removes it and selects green. The
current preference explains the LED. The original writer is not identified.
No configuration was changed and no corrective device action is needed to
complete this diagnosis. The owner can choose a different LED preference.

Can this be done on the VM? Software branches are visible in source; the actual
LED state/battery is a hardware fact captured through bounded read-only fields.
No new product change, VM test, screenshot, input, reboot or cloud operation.
`readback.json` holds the sanitized evidence and original-attempt limitations.
