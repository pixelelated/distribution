# QA15: default/upgrade results and failed restart

Frozen source55d8ee8f75; immutable bundle1b3c2c04de. The runner ended
2026-10-05 23:24:04UTC with all four result channels1. Actual cleanup at
23:25:10 confirms all recorded owner/guest PIDs and the observed local
backend exited; VNC and WebDAV ports are closed. This is a failed aggregate
run, retained without replay or changed results.

All15 default suites reported PASS:16 walks and frame comparison with
20 claimed regions,0 unclaimed and0 missing screens. Actual September29
ROCKNIX RC2 upgrade passed26 assertions, including identical saves/states,
kept settings/remote/backup, quirk migration and owner configuration. Clean
installed payload/virgl checks pass; the five initial identity frames were
reviewed. Single-sample time-to-play limits remain in parent-review.

The immediate upgraded-guest restart then failed to bind VNC5909. The old
vm-pair stop signals QEMU and returns without waiting for exit; #454 tracks
the synchronous owned-process stop and fresh continuation. No upgraded
renderer/identity result is claimed from this run.

Parent inspection found a separate inherited coverage error: manager-gb
shows Final Burn Neo, as did QA14. Its earlier match-dialog frames explicitly
remove the two Game Boy files. A surviving FBNeo state thumbnail let the
manager fixture falsely appear complete; the suite did not verify selection.
#455 adds fixture recovery and an actual selected-system guard. Automated
baseline agreement is not evidence of Game Boy coverage. QA16 replays the
predecessor and all three managers on an independent copy of the upgraded
disk. Original disk, raw logs, screenshot evidence and hashes remain intact.
