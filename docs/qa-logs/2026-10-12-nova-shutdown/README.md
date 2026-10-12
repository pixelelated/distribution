# Nova shutdown followed by Linux boot error (#558)

The owner reported one shutdown that restarted into a bootloader error saying Linux could not load. Restarting recovered; no recurrence was reported. Initial investigation remains **cause unknown / keep an eye on**, not a confirmed software defect or a fixed issue.

Can this be done on the VM? Source/VM checks can verify the ES quit route. SM8550 power-off, the real ABL path and this handheld's surviving journals are physical evidence. The captures here read existing records only; no collector archive, setting change, reboot, shutdown, input, screenshot, game or cloud operation was run.

Installed firmware is `bc9dfe8141d9561dc1d8502313d00a84c4566ee8`, version `0.0.1-dev+20261011T222153Z.gbc9dfe8141d9`. The same boot ID was observed at 05:04 and 05:14 UTC. Private filtered readbacks are retained at `/workspace/tmp/pixelelated-nova-shutdown-20261012`; their digests and sizes are indexed here. Raw logs include personal context and are excluded from the public packet.

## Timeline

Journal wall times below are EDT (UTC minus four hours), October 12:

| Session start | Last retained entry | Requested action |
| --- | --- | --- |
| 00:26:26 | 00:47:33 | Power off at 00:47:31 |
| 00:49:10 | 00:50:19 | Power off at 00:50:17 |
| 00:55:59 | 00:58:10 | Power off at 00:58:07 |
| 01:00:51 | 01:01:38 | Reboot at 01:01:36 |
| 01:01:47 | Current session at capture | No new action sent |

`power-intents.txt` contains the selected logind entries. They prove requests, not completion of physical power-off. Available evidence does not tie the reported error to one of these attempts. A bootloader failure before Linux starts may have no journal boot entry. The later reboot request is not attributed to the owner or a particular recovery attempt without additional evidence.

## What the logs can and cannot show

- Both live and persisted pstore directories contained zero files at 05:06 UTC. Named boot-reason paths were absent. This does not rule out a crash or a failed pre-Linux boot.
- Installed kernel configuration has `PSTORE=y`, `PSTORE_RAM=m`, and `QCOM_WDT=y`; `PSTORE_CONSOLE`, soft-lockup detection and hung-task detection are disabled. Module availability alone does not establish an active reserved-memory backend. Do not assume H700's ramoops/console coverage applies to SM8550.
- Current and four retained ES logs had no matching shutdown/fast-shutdown/quit-mode entry. The capture cannot distinguish normal from fast shutdown.
- Refused USB/Bluetooth/rfkill service-start transactions appear during teardown in both power-off and reboot sessions. They are not evidence of a cause by themselves.
- USB power was online and the battery charging at 05:14 UTC. This describes capture time only. Upstream documents restart while charging on some supported devices; whether it applies here is unresolved. See [the upstream comparison](../2026-10-12-upstream-review/README.md).
- SSH captures returned zero, but the optional `findmnt` probe in the third capture was unavailable. No journal-mount result is claimed from that command. Existing persisted boot entries establish journal availability directly. A filtered pipeline result is not a claim that every optional subcommand succeeded.
- #557 had already verified installed SYSTEM, kernel, packaged ABL files and both actual ABL slots against the accepted update. That bounds the transfer investigation; it does not prove later shutdown reliability.

## Next evidence and reproduction boundary

Optional owner context: normal shutdown, fast shutdown or power button; approximate incident time; charger/USB state. These questions refine the timeline, but lack of an answer does not turn a hypothesis into a diagnosis. On recurrence, record exact error text and cable state, then retrieve retained journals before additional reboots rotate useful records.

A future controlled power-off matrix would compare normal and fast shutdown with and without external power, recording command intent, physical off/restart outcome, and ABL error text. Each device mutation requires named approval through `tools/device-act`; no such experiment is running or authorized by this log request. First qualify software command routing on the VM if a reproducible software lead appears. ABL implementation/source access remains #528; v1.2 release notes do not establish an applicable fix.
