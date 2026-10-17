# #616 request, DOM, and trusted-input diagnostic candidate

Source preparation only. No compiler, browser, listener, VM, device, service,
provider request, sign-in, or credential use occurred for this packet.
The earlier browser-controls packets and product sources remain unchanged.

The candidate source is `prepared/cloud-signin-window.c`, SHA256
`63b8cf5725652874f361aa5fe04abe2b5f326b1cb9ae113590d5c422f9e16b6d`.
It targets the reviewed **GTK3 / webkit2gtk-4.1 / WebKitGTK 2.54.1** stack.
It is not source-compatible evidence for GTK4: that API's script-message signal
passes a different argument type. Declarations and implementation identities are
in `api-bindings.json`.

## Changed scope

1. Observe only top-level document resource requests, redirects, final HTTP
   statuses, and numeric resource-error classes/codes. Hash a printable, bounded
   User-Agent **if the sent-request signal includes it**. Never print a URI,
   query, host, header value, cookie, error message, or response body.
2. Inject a separate isolated-world script that sends one DOM UA digest and
   positive viewport geometry per document. At most eight text/email input
   events per document report numeric `isTrusted`, visibility/hit-test eligibility,
   focus, and time to two animation-frame callbacks. It never reads input values,
   changes focus, enters text, submits a form, or alters provider resources.
3. Refuse `CLOUD_SIGNIN_DEBUG` when present, including an empty value, with exit
   **78 before GTK initialization**. Native debug mode logs typed keys; it is
   unsuitable for this qualification. Other existing invalid QA616 settings
   retain exit 78. `--qa616-check` retains successful exit 0 when valid.

All original UA modes and validation, native input/OSK/popup functions, broker
argv protocol, ephemeral context, viewport/zoom, navigation restrictions, and
periodic observer code remain unchanged. The existing DMA-BUF environment
setting remains the original override behavior; this packet adds no renderer
control. Product files/pins and production deployment are outside scope.

## Claims and limits

`QA616_OBSERVER=off` disables the **existing periodic** heartbeat/evaluation.
This candidate still has small event-driven proof overhead: one isolated-world
script per document, one DOM hash, main-resource callbacks, and at most eight
input probes. Do not label it “uninstrumented.” Compare against the previous
compiled helper when measuring that additional overhead. The callback performs
style/hit-test reads for an input; a two-rAF delta is neither GPU timing nor proof
of a displayed character. A reviewed native frame and native input event remain
necessary for visible-input claims.

The `sent-request` snapshot may omit a UA added later by the network process.
The local original-plus-302-redirect echo fixture establishes whether the signal
is populated and agrees with the server in that fixture. **It never guarantees
provider wire headers.** Site quirks, redirects, and missing signals remain
possible. Missing/mismatched UA records withhold the UA-ranking claim only.
Fixed-UA provider-page status, responsiveness, and memory observations can still
be useful under separately stated limits; this probe is not a new universal
release or investigation gate.

`resource_at_callback` is the current resource counter when a DOM message
arrives, not a cryptographic navigation binding. The parser only compares the
hash observation for one resource and one document with the same fixed provider
class. Rapid/repeated navigation, multiple document messages, record exhaustion,
and missing signals require a narrower interpretation. The numeric document
identifier derives from `performance.timeOrigin`; it is not persisted state.

The probe sees top-level text/email inputs only. It cannot prove usability of
cross-origin iframes, shadow-tree controls, passwords, or other field types.
No input event may simply mean no supported input was exercised. Native GTK
input, phone-uinput delivery, and synthetic JavaScript `dispatchEvent` are
separate controls. Only a trusted, visible, hittable, focused input event counts
as positive evidence here; the fixture's untrusted event must never count.

An HTTP 200 and positive geometry do not identify a usable sign-in screen.
Provider errors, invalid OAuth clients/redirects, unsupported-browser notices,
bot/CAPTCHA challenges, consent pages, and signed-in/account-specific screens
must be classified separately by reviewed frames. Do not enter credentials,
submit consent, solve a challenge, or bypass a provider restriction. A provider
failure can still have a measured memory footprint; label it as that failure,
not successful sign-in readiness. No provider script blocking is added here.

The instrumentation emits fixed-schema lines only. Existing normal broker
page/field/authorize state remains private runtime state for its native protocol;
do not export it. The parser discards unrelated native/library log lines and
never copies their contents. Keep raw guest logs private; export only reviewed
fixed-schema results and account-free frames. Debug mode is expressly refused.

## Resource bounds

* At most 16 main resources and 64 request/response/error records per launch.
* At most 64 isolated-world messages per launch, at most eight input probes per
  document. Record exhaustion emits a fixed limit marker.
* DOM geometry retries at most 100 times at 50 ms after its first animation
  frame. A hidden/unresponsive view may never call back; it is not PASS.
* Existing periodic observer remains at most one outstanding evaluation,
  two-second cadence, and 180 samples.
* The fixture server binds **127.0.0.1:18761**, fails if occupied, accepts at most
  64 GETs, has two-second accepted-socket timeout, and stops by 240 seconds.
  Each raw header is immediately reduced to a SHA256 or `unknown`.
* Root's independent VM pressure/deadline/log guards remain required. Reuse the
  existing >=160 MiB guest-available guard and <=15-second browser cases, with
  <=160-second functional group and complete process-group cleanup. Keep the
  previously corrected **128 MiB RLIMIT_FSIZE** for WebKit/memfd and explicit
  <=1 MiB file-log caps; reinstating the old 1 MiB process file-size limit caused
  SIGXFSZ in an earlier unrelated fixture attempt.

## Reproduce the prepared source

```
python3 -I -B prepare.py \
  --repo /workspace/repos/rocknix.worktrees/m7-player-setup \
  --out /an/owned/new/output-directory
```

The directory must not exist. The tool checks exact product/template/observer
hashes and reconstructs the exact earlier compiled C hash before inserting the
new code. `prepared/provenance.json` records input hashes and changed scope.
Compilation uses the same source-path-parametric GTK3 command and pinned cached
sysroot as the accepted browser-controls compilation, substituting this C file.
It requires a fresh coordinator allocation; this packet does not run a compiler.
No change to package recipes or build trees is needed.

The existing `/tmp/pix-provider616-source-20261017/browser-launch.py` is an
**unrun source plan** for normal broker handoff. After this candidate compiles,
the coordinator must bind the new exact binary hash/path into a newly reviewed
launcher copy, retain `argv[0] == /usr/bin/cloud-signin-window`, retain native
arguments/environment, and ensure debug mode is absent. Do not silently reuse
its previous helper SHA. Its `/fixture` local-control route is supported by this
server and redirects to `/page`; provider URLs still originate in real rclone
via the installed normal broker. No production binary may be overwritten.

## First future functional allocation

Use an admitted disposable clean no-NIC VM and existing owner/process guards.
The coordinator stages the compiled helper, these two calibration files, and
verified normal-broker launcher. Do not directly launch the helper and call it
normal ES handoff. If normal broker initiation cannot reach its local authorize
page without a network, stop and record that exact prerequisite; do not replace
ES/broker handoff and silently treat it as equivalent.

Start the fixture only inside that allocation:

```
python3 -I /owned/packet/calibration-server.py --output /owned/new/echo-run
```

The assigned loopback port is checked by the actual bind. Wait for `ready.json`;
retain its PID and reap the original process on cleanup. The server has no
provider capability. The fixture supports `/start` or `/fixture` -> 302 `/page`,
`/status503` for a controlled error response, and `/drop` for a connection loss.

First qualify normal broker light-control handoff with default UA/observer off:
review the page, use native input to enter then remove a single synthetic `q`,
and actuate the fixture's “Dispatch an untrusted input event” button. The button
focuses the sample input and sends an untrusted event without setting its value.
Neither route submits anything. Native frame review must confirm the real input
and restored blank field. Expected: both redirect-hop server hashes match
populated request hashes, DOM hash matches the final request observation, the
native event is trusted/eligible/focused, and the negative event is untrusted.
Missing request hashes are a valid **unknown** outcome, not evidence that the
browser is broken. Preserve all raw originals privately and adjudicate honestly.

Then vary only UA (desktop, periodic off), then only periodic observer (default,
on). Keep viewport, renderer, phone route, pressure guard, and backend unchanged.
Finish independent synthetic HTTP503 and dropped-connection cases; these must
produce error/status evidence and must not be counted as ready sign-in pages.
Use a separate fresh log and server output per case when running the parser.
This is functional qualification, not a provider or hardware performance result.

```
python3 -I -B analyse.py --log /private/case-helper.log \
  --echo /private/case-echo/requests.json
```

`analyse.py` outputs separate header calibration, DOM/request hash observation,
input counts, HTTP statuses, and error classes. It never emits an overall provider
PASS. It rejects unexpected fields, invalid numbers/digests, and duplicate input
sequences. A later live-provider account-free matrix can reuse the already
prepared one-variable plan and owner infrastructure after independent allocation;
this packet deliberately does not build an alternate orchestration framework.

## Checks actually completed

`source-checks.json`: 24 pure host AST/preparation/parser controls PASS in
0.006 seconds (rounded), including source tampering/output collision refusal,
missing/mismatched UA, untrusted/hidden input, raw-field rejection, and unknown-UA
retention of page observations. `node --check proof.js` exited 0. This is source
and parser evidence only. New target compile, signal behavior, browser
calibration, normal broker handoff, trusted-input delivery, and provider trials
remain **UNRUN** in this packet. Source and parser checks neither verify runtime
privacy nor establish browser performance.
