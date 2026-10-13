# Nova normal shutdown followed by restart (#558)

Owner report, October 13, 2026:

> Also, I tried to shut down the Pocket Nova, and immediately it was shutting down. I unplugged the power, and then it power-cycled and came back on. This is something we should look into. The device is on the network now via Tailscale, so if you want to look into what's happening, you can check the logs. You have my permission to do so in case there's anything that would indicate why it went into a reboot cycle despite the shutdown signal being sent.

The owner subsequently clarified:

> I used normal shutdown.

This is another reported restart after shutdown, with a new cable-timing detail.
A repeated loop or another bootloader Linux-load error was not reported. Keep
those distinct from the October 12 incident; no common cause is established.

Can this be done on the VM? The ES shutdown route is source/VM-testable.
Actual SM8550 power and cable transitions, PMIC reset reasons and bootloader
behavior require physical evidence. These captures only read existing logs
and status under the owner's explicit permission. No shutdown, reboot, input,
configuration change, cloud call or device-writing collector ran. SSH itself
may produce normal access-log entries. No script was staged on the device.

## Findings

Installed distribution remains `bc9dfe8141d9561dc1d8502313d00a84c4566ee8`,
`0.0.1-dev+20261011T222153Z.gbc9dfe8141d9`. Three bounded filtered SSH reads
ended zero at 15:57:47, 16:02:46 and 16:04:04 UTC. Original receipts and
read-only collector bytes are retained here; filtered personal log context
stays private and is indexed by size/hash. No runtime job remains.

October 13 times below are EDT (UTC minus four hours):

| Linux boot ID | Start | Requested action | Last retained journal entry |
| --- | --- | --- | --- |
| `52543b41126a41cd901cf4484e7c6d16` | 10:28:20 | Power off at 11:01:10 | 11:01:12 |
| `496eb86292f64eaea72f261a8bf5b988` | 11:01:21 | Power off at 11:17:01 | 11:17:13 |
| `2f68a63fb8fe4caf9e61bcfbfa12ffe5` | 11:53:26 | Current boot at collection | Not a completed shutdown |

Both preceding sessions explicitly requested power-off, then stopped services
and began unmounting the ROM filesystem. The retained tail stops around journal
flush shutdown. It does not show final system power-off or a reset cause.
The first request is followed by a new Linux boot 11 seconds later; that is a
useful temporal match, not proof that it is the owner's described incident.
The later request has a 36-minute gap before the current Linux boot. An optional
request for approximate incident time remains unanswered at this record.
Initial time synchronization was recorded in all three sessions; RTC boot
initialization was within several seconds of the first recorded timestamps.

- No retained selected kernel record identifies a panic or watchdog reset.
  Live and persisted pstore directories are empty. All four named boot-reason
  paths checked by the collector are absent. Missing evidence cannot exclude
  a crash or a pre-Linux event.
- Current and four rotated ES logs contain no matching quit message using the
  corrected source-aligned pattern. The earlier regex missed the literal
  `Shutting system down`; its empty result is not used as evidence. The third
  read adds `shutting` and `rebooting` and still finds no match.
- USB is online and the battery charging at 16:02:45 UTC. This describes the
  later read, not the moment of unplugging. Do not infer the earlier cable state
  from it or contradict the owner's reported sequence.
- Teardown service-activation refusals and boot-time PMIC dependency messages
  alone do not diagnose the restart. The PMIC messages recur across these boots.

## Accepted source and upstream check

At accepted ES `c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`,
`GuiMenu::openQuitMenu()` maps SHUTDOWN SYSTEM to `QuitMode::SHUTDOWN`.
`Utils::Platform::processQuitMode()` maps that to `runShutdownCommand()`, whose
Linux command is `shutdown -P -h now`. Reboot has a distinct command. Both
normal and fast shutdown reach the same power-off command; their metadata
behavior differs. This is a source trace, not a newly exercised VM shutdown.

The official release API still identifies ROCKNIX `20261001` and ABL `v1.2`
as latest releases. ABL v1.2 notes list no matching shutdown/cable fix. The
Nova DTS history still ends at July 28's spacing correction, and the DTS has
no diff between the accepted image source and stable20261001. The distribution
has Issues disabled. The [October 12 comparison](../2026-10-12-upstream-review/README.md)
remains relevant; this bounded recheck does not establish an applicable patch.

[ROCKNIX's charging documentation](https://rocknix.org/configure/fake-suspend/#charging)
describes devices restarting when powered off while charging. Charger or PMIC
behavior is therefore a lead, but that documentation does not establish that
unplugging during this Nova shutdown caused the restart or explain the earlier
Linux-load error. See `upstream-check.json` for exact checked references.

## Disposition and next evidence

**Normal power-off intent confirmed; restart cause unresolved.** The normal
shutdown clarification narrows the report without establishing a software fix.
First match the owner observation to the timestamped boot sequence if possible.
If a controlled physical reproduction becomes necessary, prepare a narrowly
bounded normal-shutdown comparison with external power absent, present, and
unplugged during shutdown, with before/after boot identities and screen outcome.
It is not running or authorized by this read-only request. Avoid repeated forced
power-offs; VM-qualify any software change before handheld verification.

Prior investigation criteria remain historical. #558 now carries this recurrence
and its remaining uncertainty; no new firmware or bootloader flash is justified
by these logs alone. M7 browser-memory qualification remains the primary work.
