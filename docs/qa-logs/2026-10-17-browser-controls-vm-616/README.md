# Fresh-VM functional controls for #616

Companion to the immutable
`../2026-10-17-browser-controls-616/` source packet. The coordinator has compiled
the diagnostic helper and exercised its twelve actual C configuration cases.
This packet supplies a bounded **direct-launch functional check**, not normal
EmulationStation handoff, provider performance, a browser-memory fix or a device
qualification. Its author has not run a VM, browser, listener or service.

Can this be done on the VM? Yes. Run only in the coordinator's fresh, clean-gated
GENERIC_X64 no-NIC guest. The program refuses other architectures, a non-root
guest process, additional network interfaces, changed staged inputs or an
existing output directory. The host must retain its independent VM deadline.

```sh
python3 -I /storage/OWNED/guest-check.py \
  --helper /storage/OWNED/cloud-signin-window \
  --helper-sha256 ACTUAL_VERIFIED_X86_BINARY_SHA256 \
  --html /storage/OWNED/input-control.html \
  --output /storage/OWNED/functional01
```

The HTML must exactly match the original source packet (SHA256
`f33796db2c501d8c76226d90e8b1eeff5b8476db1a62cc89de983b6c517a45d1`).
The helper must be the separately admitted and verified x86_64 build; its hash
is a required argument rather than a guessed build identity. The program
writes only its new output directory, starts its owned loopback server and
helper processes, and temporarily stops/restarts `essway.service` if initially
active. It never changes system configuration, installed programs, saves,
accounts or cloud state. Stopping the frontend in a clean disposable VM is
intentional test setup; it is not a proposed browser resource policy.

The driver finds the existing Sway executable by `/proc`, reads only required
environment keys, requires one actual Wayland socket and one Sway IPC socket,
and verifies `swaymsg get_version`. It records the compositor's PID/start
identity and checks that stopping the frontend preserves that compositor. It
does not guess `wayland-0` or a runtime path, start nested Sway, or reuse a
historical guest owner. An active frontend is restored and verified active in
the finalizer; an initially inactive frontend stays inactive.

Six cases run sequentially: default/off/clean, default/on/clean,
desktop/off/clean, desktop/on/clean, desktop/on/blocked, desktop/on/hidden.
Each has a fresh browser process and ephemeral context, with unchanged zoom
and viewport. The driver binds exactly `127.0.0.1:18761`; collision refuses,
with no port substitution. The only served page is the fixed input fixture.
Its companion adaptation permits one same-origin proof POST and makes the
blocked control cover the entire viewport regardless of font wrapping.
The exact served bytes/hash are retained. There are no provider requests or
credentials; default and explicit desktop UAs are compared without bypassing
provider restrictions.

The server records SHA256 of the actual request User-Agent and the page's
`navigator.userAgent`, plus numeric viewport geometry. It never stores the
raw UA/body, field text, cookies or arbitrary request paths. Unknown routes
refuse. The browser receives `--no-auto-keyboard` so this check does not
measure or change native keyboard behavior. The parser and mode configuration
remain the original immutable diagnostic source.

Functional assertions cover matching HTTP/DOM UA identities, actual desktop
selection, unchanged geometry, no numeric observer samples when off, numeric
samples when on, complete-load hints and unobstructed-input hints for clean
versus obstructed/hidden controls. Missing evidence fails; disabled sample
output alone is not a proof of zero observer overhead. A default desktop UA
can legitimately equal the explicit desktop result, which is recorded without
inventing a distinction. No CPU, heap, provider-ranking or performance claim
comes from these six short checks.

The driver waits at least five seconds and captures one native `grim` frame
per case using the discovered Sway environment, with a three-second timeout.
It records the path, hash and actual capture exit. **Visual review remains
pending even when a PNG exists.** The coordinator exports and views every
frame before accepting presentation/readiness. There is no frame-ack wait or
manual timing dependency. The checks record the browser's real return code;
controlled termination expects SIGTERM (`-15`), not an invented normal exit.

A separate guard process polls available memory every100ms, with a160MiB
floor, a15s browser-case deadline and a160s total deadline. Heartbeat freshness
is checked by the driver. A trigger stops the owned browser, records the
reason and prevents PASS. Process-group members are identified from kernel
PID/start/session/group metadata and signalled using pidfds; there is no broad
`pkill`. TERM has1s, followed by KILL if necessary. Unexpected main-process
exit causes the guard to clean its active browser group. The finalizer closes
the loopback listener, cleans the browser, restores frontend state and waits
for the guard's original result. The coordinator's outer VM lifecycle remains
the last-resort boundary if the guest cannot execute cleanup.

Expected output is small: `result.json`, per-case numeric results/logs, six
PNG frames, guard logs/result, served fixture and guard state. Core dumps are
disabled and the inherited process file-size ceiling is128MiB, including
browser memfd/shared-memory backing files. The browser diagnostic log has a
separate512KiB bound checked during each case. Export this compact
evidence before retiring the owned guest. A result with `pass:true` still says
`visual_review_pending:true`; it is functional evidence only until reviewed.

## Preparation status

Only Python AST parsing, embedded-JavaScript syntax parsing and source/hash
inspection have been performed by this packet's author. Runtime, process
cleanup, frame capture and service-restoration claims above describe the
driver's intended checks and remain **UNRUN** until the coordinator records
the actual results. The source packet and compiled binaries are unchanged.

## First allocated attempt and source correction

The coordinator reported that the first run of driver
`c4791fdc59a772b9da76a8ee03823b2191afdaaedc9e46cf781bd828fb969567`
ended after1.18s with the browser's actual return code `-25` (SIGXFSZ).
The inherited1MiB file-size limit also applies to browser backing files;
this is a fixture constraint, not evidence of browser memory exhaustion.
The guard did not trigger (reported minimum available403500KiB), exited0,
and the frontend was restored. The coordinator retains that original failure
receipt; it must not be overwritten by a retry.

The revised driver changes only that ceiling to128MiB. It retains the512KiB
diagnostic-log check,160MiB memory floor,15s case deadline and160s total
deadline. No `preexec_fn`, subprocess wrapper or thread-unsafe temporary limit
change is introduced. The revision is source-only until the coordinator
records a fresh attempt; SIGXFSZ's exact backing-file identity is unmeasured.

## Second allocated attempt and diagnostic revision

The second original result has been read at the coordinator's exported
`functional02/result.json`: the page loaded, HTTP UA proof exists, but no
accepted DOM POST was recorded. Browser exit was-15, the guard exited0 with
minimum available413792KiB, and the frontend was restored. The reviewed
frame shows the clean input and the JavaScript-generated control label.
The missing POST's cause is not established by the old silent handler.

This revision records up to64 fixed server event categories, including
missing/matching/other Origin, request acceptance and refusal stages. It adds
a fixed page status for requested/HTTP status/fetch rejection/CSP rejection
without URLs, exception messages, header values or field data. The original
Origin equality check is unchanged. This is diagnosis, not an assumed fix.
The runtime safety bounds and original source/binaries are unchanged.

## Matched Origin and schema diagnosis

The coordinator reports that functional03 received the POST with matching
Origin, then refused its proof schema (HTTP400). This rules out the proposed
missing-Origin explanation. The revision preserves every validation check,
schedules the proof on an animation frame, and waits at most100×50ms for
positive viewport geometry. A still-hidden view at DOMContentLoaded is a
hypothesis, not yet a measured cause. Any further schema refusal records only
fixed structural booleans, UA length and bounded numeric geometry; no UA,
request content, cookies or URLs are retained. The next actual run is UNRUN
by the packet author.

## Coordinator execution result

The coordinator executed four separately retained attempts in the allocated VM.
The final driver444ed5d4 passes all six cases in31.386s, with fixed640x457 DPR1
content geometry. Default mobile and desktop HTTP/DOM UA hashes match within
each mode and differ between modes. Observer selection and clean/blocked/hidden
controls pass; all frames were reviewed. No memory guard fired and the frontend
was restored. Full results and earlier failures are in
[the results packet](../2026-10-17-browser-controls-results-616/README.md).
The rejected earlier report did not retain numeric geometry, so zero-size timing
is a plausible explanation, not a proven historical value. The final fixture
waits for a frame and positive geometry without loosening acceptance.
