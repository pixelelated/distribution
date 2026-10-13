# Browser speed history and phone queue controls — October 13, 2026

[#570](https://github.com/pixelelated/distribution/issues/570), extending the
[owner's historical-performance request](https://github.com/pixelelated/distribution/issues/570#issuecomment-6137434751).
This is source archaeology and a host JavaScript control, not a new VM or physical
browser measurement. No product code, settings, credentials, saves or device changed.

## What the history establishes

| Date and source | Earlier improvement or change | Accepted source today |
| --- | --- | --- |
| August30, `41db2acab6` | Removed nested compositor, screen mirroring and VNC/WebSocket transport. Commit reports a150-second→two-second page-load improvement. | `BrowserSession.start` still locates existing Sway and launches one browser client with its Wayland environment. No screen streaming. The historical timing has not been reproduced and does not bind today's page content/engine/hardware. |
| August31, ES `1e93fd1a2` | Suspend ES rendering/input/audio while sign-in owns the display. | Accepted `ApiSystem::launchCloudSignIn` still deinitializes those resources. Both current keyboard-choice call sites use it. ES process/database remain; browser starts before teardown, and frontend restores before browser closes. Recent direct-launch measurements bypassed this normal handoff. |
| September1, `9d554fe596`, `6894b153aa` and dated work log | Flatten pointer acceleration, preserve fractional deltas, coalesce moves so a60Hz drag cannot build a request for every event. | Flat profile,1:1 movement and fractional carry remain. Actual old/current JavaScript controls below confirm coalescing remains. |
| September1, ES `920421e14` | Put provider-startup wait behind GuiLoading instead of freezing the ES interface. | Distinct from provider rendering or phone round-trip latency. Do not interpret the old startup animation fix as a WebKit memory optimization. |
| September13, `6e35a5fd04` | Added native RAOfflineProxy service. | August30 tree has no proxy package. Current enabled service occupies about76–105MiB in prior bench observations. This is a real stack difference from the earliest browser work, not a dated regression against the owner's unknown last-fast build. |
| September25, `4137690ec1`, D-WORKFLOW-048 | WebKit2.54 adoption disables DMA-BUF after VM stalls. | Flag remains. Exact2.54.1 source also gates accelerated compositing off. Shared Sway does not imply accelerated WebKit. Earlier on/off physical controls were guard-truncated and do not rank performance.2.54.0 comparison does not cross the2.52→2.54 compositor boundary. |
| October1, `98e1a30362`, D-NET-016 | CHASSIS=handset selects mobile user agent. | Earlier desktop-UA/current-engine control did not lower memory materially; that single page-load control does not rule out navigation or provider-content effects. |
| October11, `bc2dceb406` | Join movement, typing and clicks in one queue; allow related authentication windows and handle Back. | Ordering fixes the old tap race. A slow typing acknowledgement now delays movement too. Related popup retains parent while open; relevant after an identity-provider popup, not an explanation for a fresh first page by itself. |

The early speed improvements were not wholesale lost. Resource availability,
engine/rendering policy and input sequencing all changed since the original work.
Release notes (`docs/cloud-sync-changelog.md`) describe current input ordering and
phone fixes; the earlier timing/pointer details are in commits and the September1
work log. None supplies a reproducible last-fast firmware/provider-page baseline.

## Phone transport: observed control, bounded claim

[manifest.json](manifest.json) binds actual pre-October11 and accepted device
`cloud_oauth` bytes. The fixture AST-extracts REMOTE_PAGE, executes its unmodified
JavaScript with a stub DOM and deferred mock fetch responses, and drives real event
handlers. It does not import/execute the broker or use uinput, Wi-Fi or an account.
[queue-result.json](queue-result.json) retains successful original outcomes.

- While a typing response is held, old code issues pointer movement; accepted code
  waits. After acknowledgement, both deliver all120 synthetic movement units.
- With only a drag,120 events become two requests in BOTH versions: one in flight
  and one accumulated. The anti-backlog optimization remains.
- With a small drag/tap and the movement response held, old code sends the click
  after its60ms timer; accepted code waits for the move acknowledgement. Reverting
  the common queue would restore the correctness defect it repaired.

The broker responds to a typing POST only after `type_text` completes. Existing
key timing deliberately spends12ms held plus22ms gap for each unshifted character;
shifted characters add44ms. For example,64 unshifted characters have2.176s of
requested sleeps before response, excluding scheduling/network delay. This is a
calculation from source, not a measured paste or incident latency. Those sleeps
predate the queue change. The fetch chain has no application-set deadline;
browser/network failure can still terminate a request. Do not blindly retry an
input POST: lost acknowledgement does not mean its keystrokes were not applied.

These controls prove an input-wait coupling, not that it caused the reported crawl
or reset. The prior heavy public-page reproduction required no phone. A repair
needs measured end-to-end input latency and must preserve move/click/text order.

Reproduce the small control without a firmware build, using a fresh output path:

```sh
python3 docs/qa-logs/2026-10-13-browser-history/fixtures/prepare.py --repo . --output /tmp/pixelelated-phone-queue-fresh
node docs/qa-logs/2026-10-13-browser-history/fixtures/queue-control.js /tmp/pixelelated-phone-queue-fresh
```

## Other concrete leads and limits

- The connected phone polls every2s after the preceding response. The server reads
  tiny page/field state files; that endpoint does not evaluate WebKit JavaScript or
  stream screenshots. This makes idle phone presence a different control from
  typing/dragging. Selecting the phone option also suppresses automatic on-screen
  keyboard raising; keep that independent from whether a phone client connects.
- WebKit's500ms focus probe runs with either keyboard choice, started once per
  process. It can inspect input geometry and request focus. There is no outstanding-
  evaluation guard before queuing another asynchronous evaluation. This predates
  the latest build; accumulation under stalls is a hypothesis. The earlier
  single synthetic no-probe trial had a smaller heartbeat gap, with similar PSS;
  repeated reordered trials and real input behavior are still needed. Removing
  it wholesale would break field readiness/keyboard behavior and completion.
- The normal ES handoff and a populated frontend/background proxy must be measured
  together. Prior browser-only PSS does not quantify frontend teardown savings,
  startup overlap or optional proxy work. Proxy workers gate on game traffic idle,
  not browser activity; activity during the incident has not been established.
- Live provider content, network delay and repeated navigation are not frozen by
  pinning firmware. Test a local fixed fixture first, then a public page with
  resource/load/input timing. A changed UA cannot be excluded solely by memory.
- H700 frequency/thermal/Panfrost behavior remains a physical corroboration lead,
  not a diagnosed fault. Current evidence includes earlier GPU clock warnings but
  no proof of a new CPU/GPU throttle causing this incident.

The dated [upstream review](../2026-10-13-webkit-versions/upstream-check.md) and
[exact renderer/lifecycle review](../2026-10-13-browser-stack/README.md) remain the
component reference: no confirmed matching upstream fix.2.52.6 is source-inspected,
not built or tested; neither an engine downgrade nor service suspension is selected.

## Next discriminating work

Can this be done on the VM? Yes. The controls below need a disposable GENERIC_X64
guest and synthetic data; only board-specific memory/GPU/power corroboration needs
the already authorized RG35XX SP bench. No owner proxy restart/account action.

1. Same local synthetic page, same viewport/keyboard setting through normal ES
   handoff: no phone client; idle client polling; scripted typing/drag/navigation.
   Measure page heartbeat, input issuance/acknowledgement/visible application,
   process PSS/CPU, kernel pressure/refaults, startup overlap and return/recovery.
   Repeat in reordered trials with settled baselines; bind source and frame states.
2. Independently compare focus probing and controlled background-service load using
   synthetic proxy data. Keep field readiness, ordering and queued awards intact;
   compare ES before/after teardown and observer overhead. Do not infer a safe proxy
   lifecycle change from lower idle PSS alone.
3. If the fixed workload remains slow without phone input, cross the actual2.52.6
   vs2.54 rendering boundary with explicit build/policy controls. Public Dropbox
   is a follow-up workload, not the only causal control. Existing graphics trials
   do not establish that turning acceleration on is a safe fix.

This refines #570's next steps within the existing M7 order. Full browser usability,
#572 assembled-image proof and the release gates remain open. No test/build remains
running after these synchronous host controls.
