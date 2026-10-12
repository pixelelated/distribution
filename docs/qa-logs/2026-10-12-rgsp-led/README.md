# RG SP fixed red LED follow-up — #534

Owner report: “FYI, on the latest build, the RG SP is still showing the red LED even when the battery's at 97%.”

At04:53:20UTC on October12, the accepted bc9dfe8141 build still has `led.color=red` in both live and recovery settings. Actual red brightness1, green0 and both triggers `none` match the fixed selection. USB is offline and battery status is Discharging; raw capacity100 and display cache96 were sampled at the readback, after the owner's97% observation. This is not a battery-calibration measurement.

The installed dispatcher, H700 implementation, flash helper and powerstate hashes are identical to the October11 diagnosis. The update preserved the existing color preference; no new firmware regression is established. The normal `default` action removes the fixed preference and selects green, but **no LED or settings action was requested or executed**. No reboot, screenshot, input, game or cloud operation occurred.

Can this be done on the VM? Selection logic is source-verifiable; this readback is of the RG SP's physical LED/battery state and saved choice. #534 contains the scope before the filtered read. Original writer of the red preference remains unknown.
