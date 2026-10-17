# Prepared #616 normal-handoff/provider work

Source preparation only, against published coordinator
`4c3eda48c724e9dc819483ae9d50f8d44edb07cf`. No compiler, listener, VM,
device, service, browser or provider request was run by this lane. Only this
new `/tmp/pix-provider616-source-20261017/` directory was written. The parent
owns every runtime allocation, integration and tracker update.

The completed six-case packet proves the tiny helper's direct-launch runtime
UA selection, observer selection and visible/covered/hidden hints. It does
**not** prove normal ES/broker handoff, native trusted typing, provider HTTP/DOM
UA binding, provider usability, input latency or memory savings. No old case
is repeated merely to make the packet larger.

## Wiring through the real broker

The current installed broker launches the absolute
`/usr/bin/cloud-signin-window`, copies its environment, and passes the provider
URL, allowed host, exit hint and optional `--no-auto-keyboard`. Its
`signin_window_running()` matches **argv[0] exactly** to that absolute path.
An exec of a helper with its scratch path as argv[0] would break `open`/`wait`.

`browser-launch.py` is a proposed temporary bind-mounted launcher. It reads a
bounded private per-case JSON, verifies the compiled helper SHA256, sets only
the existing UA/observer controls, then `execve`s that helper using the exact
broker argv[0]. No Python launcher remains resident after exec. Normal provider
URLs/queries and native options pass unchanged; no URL or PIN is logged. A
fresh launch receipt binds the case to PID/start/helper identity. A light cell
keeps a real Dropbox authorize process waiting but substitutes only the browser
page/allowed host with the fixed loopback fixture; it is explicitly a synthetic
page control, not a real provider response.

This requires no production source, broker or OS-image change. The coordinator
must record the original installed browser hash, temporary bind mount/readback,
case JSON, exact helper path, restoration and process exits in the fresh guest.
A PATH override alone will not work. A systemd manager environment change does
not retroactively change an already-running ES process, so this packet does
not propose that unreliable alternative.

Canonical paths for this prepared launcher:

- helper: `/storage/qa616-provider/cloud-signin-window-GENERIC_X64`, SHA256
  `530b0d2c7daf739eb061a415da4224a7affcec1b1837a452d182e97a03c16454`;
- case: `/run/qa616-provider/current.json`, root-owned and not group/world-writable;
- receipts: `/storage/qa616-provider/launches/`, root-owned mode0700;
- example case: `{"id":"s0-default-off-1","provider":"light","ua":"default","observer":"off"}`.

The fresh guest starts with no connection or personal data. The coordinator
can bind an owned empty configuration directory over
`/storage/.config/rclone`, which also contains the hardcoded `cloud_connections`
transaction paths, and record its before/after hash. Do not rely solely on
`RCLONE_CONFIG`: `cloud_connections.py` hardcodes its canonical path. No account
completion is allowed; any token, `signed-in` marker or populated remote is
an abort condition. Preserve private ephemeral OAuth state locally only long
enough to drive the case; do not export raw `session.json`, command lines,
provider queries, PINs or unfiltered broker output.

Actual provider generation stays in installed
`cloud_oauth serve <dropbox|drive|onedrive>` → real
`rclone authorize BACKEND --auth-no-open-browser` → rclone's own local redirect.
Do not construct a generic public login URL or manually invent OAuth parameters.
The UI starts this service and owns it. Use the normal Cloud Connections flow,
choose the provider and WITH MY PHONE, then CONTINUE. That calls
`ApiSystem::launchCloudSignIn`: installed broker `open --phone`, normal renderer
release and `malloc_trim`, installed broker `wait`, renderer restoration and
`close`. The proof must observe that chain and the same ES PID/start identity.
Starting a browser directly or stopping `essway` is not a substitute here.

The broker contains existing broad `pkill -f "rclone authorize"` calls. A fresh
single-purpose guest with no other rclone job is therefore a hard precondition
for this fixture; do not import this procedure into a personal device. This
packet neither changes nor endorses that implementation as a general cleanup
tool. Runtime guards still target exact owned process identities.

## Two instrumentation gaps are real gates

**UA binding:** the qualified helper logs the settings UA hash. Default mode
preserves WebKit's per-site quirks, so that hash need not identify the header
actually sent to a provider. The earlier localhost server/DOM match establishes
only its local requests. The current numeric observer does not return a DOM UA
hash. Do not label a provider row bound using either substitute.

WebKit2.54.1 provides `WebKitWebResource::sent-request` with a
`WebKitURIRequest`, and `webkit_uri_request_get_http_headers` reconstructs
Soup headers from that ResourceRequest. This is a candidate for a tiny
diagnostic extension, not yet a validated wire-header source. First prove the
candidate User-Agent hash agrees with the local echo on original and redirect
requests, and prove whether the header is actually populated at this signal.
If missing or mismatched, record unknown and stop the provider-UA claim;
do not introduce TLS interception or a provider-bypassing proxy.

The extension should retain only a request sequence, main-document flag,
fixed provider class, SHA256 of the User-Agent and HTTP status/error class.
No path/query, other headers, response body or cookie export. In a separately
isolated script world, take a one-shot `navigator.userAgent` hash after positive
viewport geometry. Keep this minimal binding probe identical in periodic
observer-off/on cells, and call the states **periodic observer off/on**: neither
is a claim of zero instrumentation. Preserve an installed uninstrumented helper
control separately if total instrumentation cost is measured. Site quirks,
redirect changes and subframes must be explicit.

**Trusted input:** the current helper records geometric hints and heartbeat
gaps, not input events. Extend the isolated probe with numeric
`isTrusted` input counts, an explicit editable text/email-target check and
input-handler→two-animation-frame timing. Do not record values, names or
selectors. Calibrate with the fixed local page: native broker keyboard typing
must increment the trusted count; a scripted untrusted `InputEvent` is a
negative control and must not satisfy it. Actual native frames/timestamps still
bound input-to-visible-paint; a callback alone is not a presentation proof.

For a provider, first review an unobscured form/frame and verify the focused
target is an empty editable text/email field, never password or account picker.
Then send a single synthetic character through the normal broker's native
keyboard endpoint, clear it with native Backspace, and never press Enter/Next,
submit, select an account or accept authorization consent. No credentials are
used. If a cookie overlay obscures the field, classify the untouched page
separately; any narrowly scoped cookie rejection is a recorded separate action,
not a silent readiness shortcut. Unknown/CAPTCHA/policy/error pages are not
faster working logins. A successful single-character probe is still not full
authentication compatibility.

These small helper extensions need a new exact-source compile and VM proof.
They are **not implemented or compiled in this packet**. That is the concrete
blocker to the full requested trusted-input/provider-UA matrix. The prepared
launcher can be qualified independently in the next allocation.

## First executable allocation

Can this be done on the VM? Yes. Allocate one fresh accepted077197/ES16dbac
GENERIC_X64 guest,2GiB RAM,4vCPU,640×480, software renderer, with the ordinary
isolated NAT profile needed for later providers. Run the untouched clean-state
gate before staging. Keep all other performance workloads stopped or isolated;
source-only work may continue in parallel. Record visible RAM/CMA, renderer,
proxy state, swap and original profile hash.

First **qualify the prepared wrapper in normal ES/broker light-page handoff**:
stage the verified helper and wrapper, verify/stage the already qualified
loopback fixture/server, set the fresh light case, select Dropbox/WITH MY PHONE
in the real UI, and CONTINUE. Require the wrapper receipt, the browser's exact
argv[0], broker wait process, same ES identity, frame, HTTP/DOM local UA binding,
normal Escape/return, no residual browser/uinput ownership and unchanged empty
rclone configuration. Do not stop/restart ES to simulate the handoff. This one
cell is useful without the new instrumentation but does not satisfy trusted
typing or provider binding. Controller key steps must come from reviewed current
frames and canonical UI walks, not replayed stale pixel coordinates.

Limits:75s browser lifetime,110s cell,160MiB available-memory floor,250ms
independent guard;20s cleanup. Reuse the accepted lifecycle/guard infrastructure
and exact PID/start/pidfd ownership, not archived owners. Retain the128MiB
file-size ceiling (1MiB caused SIGXFSZ); keep browser logs under512KiB and compact
samples under8MiB. Record cumulative allocation/refault/PSI/CPU counters and
per-process PSS at a lean fixed interval; do not treat those as a JS heap.
Sampler overhead is a separate control. Preserve all original failure channels.

The broker's parent owns the actual browser child and does not currently export
its return code. Kernel PID absence plus broker wait success is not that return
code. Record the observed close signal, wait outcome, exact process absence and
coordinator/lifecycle exits; if child exit provenance is required, qualify a
minimal diagnostic broker status trace before claiming it. Do not add a resident
Python supervisor silently to the1GiB memory comparison.

After wrapper handoff and new instrument controls pass, run S1 endpoint outcome
discovery. Then the reordered S2/S3 page/RAM matrix and S4 UA-only trials in
`matrix.json`. The next allocation need not run the entire matrix at once.
Fresh ephemeral contexts and actual rclone sessions are used; no persistent
remote is created. Error/blocked cells retain their memory/loading data but
are excluded from functioning-login comparisons by `adjudicate.py`.

## Evidence contract and cleanup

Keep source/tool/profile hashes, original launch/controller/watcher results,
per-case request/DOM hashes with provenance, numeric memory/CPU/reclaim samples,
trusted/untrusted event counts, input/render timestamps, reviewed frames,
explicit outcome, guard events, frontend identity and empty-config preservation.
All raw URLs/state/PINs remain private and short-lived. Full page text/resources
are unnecessary for this stage. A provider refusal is a valid observation,
not a reason to change the identity until it lets us in.

On each exit, ask installed broker to close/cancel, prove window/native-input
release and ES recovery, then apply exact-identity TERM/KILL only if the bounded
normal path fails. Stop only the owned loopback listener/observer, restore owned
bind mounts with original-hash readback, export compact evidence and consume
the allocation before deleting its owned VM payload. No artifact retention or
cleanup command is run by this source packet.
