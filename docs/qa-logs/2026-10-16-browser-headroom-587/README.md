# Browser headroom and proxy lifecycle — #587 / #615

Four constrained-memory VM browser comparisons pass. Temporarily stopping the
actual packaged RAOfflineProxy increases the mean of the two condition medians
for available memory by **26.27MiB** in this small synthetic workload. However,
a separate busy-stop test exposes a **15-second systemd timeout / SIGKILL** while
a slow award response is in flight. This packet supports further lifecycle work;
it does **not** qualify an unconditional production stop policy or claim that
Dropbox is fixed on H700. D-RA-048 promotes this investigation into current M7.

## Exact scope

Unchanged product077197e6cd3ea31f33b28aaf3882a694b3423b53 and ES16dbac5211eea7e70db7394372033be2be7df829,
firmware0.0.1-dev+20261015T161744Z.g077197e6cd3e. Fresh GENERIC_X64 image,
QEMU/KVM four CPUs,1024MiB,640×480, software rendering,16GiB disk, no NIC.
The untouched selected-state first-boot check passes before synthetic seeding.
Actual guest MemTotal810528KiB, CMA262144KiB, no swap. This x86 layout differs
from H700's measured RAM/CMA/graphics and cannot establish hardware viability.

The normal ES cloud connection flow launches the installed cloud_oauth and
cloud-signin-window. Only rclone's authorize helper is replaced by a guest-owned
bind-mounted fixture serving a local page; its128MiB typed array is touched at
4096-byte intervals. Load, double-animation-frame readiness, focused window,
reviewed pixels and actual keyboard input are required. No provider, credentials,
cloud data or handheld is contacted. Literal fixture-only tokens are synthetic.

Actual installed proxy unit/ctl/modules are unchanged and hashed. New synthetic
login/patch caches cover two accounts and two games. Two signed offline awards
are queued, including a duplicate refusal. Original pending rows, chain,
SQLite integrity and cached login/patch/session/account separation are checked
after each normal browser run. The enabled setting, service marker and config
hash/mode remain unchanged. This is stop/start, not the destructive disable path.

## Memory comparison

Order is active, stopped, stopped, active. Each row has six samples while the
exact browser PID/start still exists during the steady phase; two stale phase
samples after close are excluded by the offline analysis, not erased.

| Case | Proxy | Median available MiB | Proxy PSS MiB |
| --- | --- | ---: | ---: |
| 1 | Active | 233.34 | 23.91 |
| 2 | Stopped | 259.07 | 0 |
| 3 | Stopped | 258.01 | 0 |
| 4 | Active | 231.20 | 22.29 |

`analysis.json` retains ranges, browser/ES/observer PSS, kernel counter deltas
and sampling duration. The independent observer occupies about7.7–7.9MiB PSS;
its smaps sampling takes roughly9–19ms every2seconds. Reclaim/allocation-stall counters remain active in some cases, including the
proxy-stopped cases; more available memory does not prove pressure is eliminated.
Full250ms polling CPU
cost and short-lived serial Python/controller overhead are not isolated. Guest
PSI is unavailable, explicitly null; the independent available-memory and90s
browser guards never fire. There is no OOM/kernel fault in the captured journal.

Normal closes take0.299–0.325s. The two stopped cases restart in1.035/1.037s
including the installed listening readiness check; cached protocol checks pass.
All four reviewed return frames show the existing ES sign-in page. The same ES
PID/start survives. These two runs per condition are a directional measurement,
not statistical proof or a speed improvement: observed readiness is2.87–4.51s.
The tiny cache's22–24MiB proxy PSS is not the earlier physical76–105MiB estimate.

## Busy stop and recovery

A subsequent, separate loopback peer test uses one unaddressed dummy interface
only to satisfy the proxy's active-interface reachability gate. QEMU still has
no NIC/default route; the configured upstream is127.0.0.1:19081. The peer returns
patch data, then drips a successful award body one byte every1.3seconds, keeping
individual reads within the HTTP timeout. The peer confirms the actual service
entered that request before ordinary `systemctl stop` is requested.

Original stop command returns0, but after15.062s the unit reports
`Result=timeout`, `ExecMainCode=2`, `ExecMainStatus=9`, `ActiveState=failed`.
The journal explicitly records SIGKILL. **Command0 does not mean clean stop.**
Both pending rows remain intact, the signature chain verifies and SQLite is ok.
This is one deliberately slow response, not proof that every interrupted upload
is lossless; server-accepted/client-unacknowledged duplication is untested.

Switching the peer to immediate success and restarting the unchanged service
makes it ready in1.041s; both fixture award requests receive successful replies
and the pending queue empties by the3.841s observation. SQLite remains ok.
This tests synthetic reconnect/flush, not the real RetroAchievements service.
The peer supplies fixture data and does not validate real server credentials.

Source trace: service.py's signal handler sets stop_requested; a watcher sets
stop_event. proxy_service.py:run_proxy_service starts the HTTP server, probes,
and synchronously flushes pending awards before reaching its stop_event loop.
flusher.py's synchronous network operations do not use that event. The installed
unit's TimeoutStopSec=15 then escalates. The observed timeout matches this path;
we have not proved it is the sole busy-worker shutdown path.

## Next executable work

Keep the browser. Under #587, first design/review an atomic quiescence or bounded
cancellation contract: detect active flush/cache work without a check/stop race;
preserve queued state and account routing; release memory only when safe; restore
only a service this browser session actually stopped. Include failed launch,
normal exit, crash, stale owner, already-disabled service and restart failure.
A SIGSTOP merely freezes memory and does not provide this headroom. Increasing
the timeout alone does not make browser launch bounded or prove work safety.

Then use a fresh VM allocation to test the slow-response counterexample,
success/auth failure/network loss, duplicate acknowledgement and restart readiness
against that candidate. Preserve these original failures. Only after portable
lifecycle proof should a new bounded H700 real-page experiment measure hardware
headroom and loaded-page responsiveness. #615 stays inconclusive for that path.
Fable/council is optional after a concrete sanitized assessment packet; none was
sent here. #613 remains the next independent package task; #607–610 precede the
next affected Nova deployment. #528 and website work remain separate.

## Custody and reproduction

- `python3 -I verify.py` verifies hashes, archive members, original exit channels,
  exact analysis reproduction, preserved settings and the negative busy-stop result.
- `analyze.py` is offline/read-only. `fixtures/` are historical executed helpers
  with absolute owner paths; never replay them into a device or reuse the retired
  allocation. Fresh runtime work requires a new owner/admission and issue plan.
- `originals/original-records.tar.gz` is a lossless archive of compact host/serial
  records, excluding disks. Its member manifest is independently checked. Separate
  guest sample gzip and small JSONs make analysis/review convenient.
- First admission attempt refused before payload: copied preparer protected all
  `/tmp`, whose identity changed. The accidental subsequent submit also refused125
  without admission. No first-attempt VM existed. Fresh preparation protected the
  exact file and checked each prerequisite before submission.
- First no-NIC browser attempt collided with the proxy on loopback8080. The source
  intentionally binds OAuth to the LAN address. A guest-only192.0.2.2 address and
 192.0.2.1 route on lo supplied that separation; this is a fixture artifact,
  not a new online-browser defect. Original failure/frame remain in the archive.
- Final observer0, matrix owner0, lifecycle launcher/wrapper/command/monitor/runner0;
  exact host/QEMU processes absent, admission5c8eeab34ebb4b30ae07af99fc0c7aa6 consumed.
  Cleanup removes the dummy/loopback route, peer, observer and bind mount; original
  rclone bytes and empty remote list verified. Installed hashes and all three
  protected synthetic config paths unchanged. Guest stopped;2,412,744,704 allocated
  disk/OVMF bytes retired. No VM or diagnostic remains active.
- Upstream head2eb6bca2169cb26c45739ed714bc92f43154c8b1 is six commits beyondc7ebd1b;
  compared changes do not select a memory fix. The original issue-search422 is
  retained; corrected explicit is:issue searches return three memory mentions
  and zero shutdown matches, not an exhaustive absence claim.
  Shutdown cancellation is a possible #585 upstream contribution after a verified
  fix/current-upstream comparison, not an already submitted or accepted patch.

## Publication monitor follow-up

Evidence commit947e0b3de0 is on both ordinary refs and all three hosted checks
passed. `publication.json` preserves the initial missing-owner submission2,
first polling watcher1 after a30s GitHub API timeout, and recovery watcher0.
The copied historical recovery helper records timed-out polls and retries within
its overall900s deadline. It changes no shared build monitor. Hosted results and
poller results remain separate; no failed original is rewritten. The independent
handoff review and corrected stale records are retained in `handoff-review.json`.
