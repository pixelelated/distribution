# #588 startup reconnect repair — source-only handoff

Status: **prepared and statically checked; every runtime fixture is UNRUN**.
This internal fallback packet is separate from the authentication-blocked Herdr
lane. It owns only this directory. No product file, package pin, shared record,
device, service, VM, compiler, account or provider was changed or launched.

The proposed seven-line addition carries the startup probe's observation into
`ConnectivityMonitor` before `start()`. Its first real probe now flushes on the
previously lost false-to-true transition. An already-online startup still flushes
only once. The added branch checks `stop_event` before starting a flush. Monitor
construction, the initial synchronous flush/corruption report, the periodic loop,
15-second interval, queue locking, signing, authentication, retry policy and
shutdown sequence stay unchanged. An independently constructed monitor defaults
to an offline prior observation; its first online result consequently flushes.

The baseline `proxy_service.py` SHA256 is
`42fbdb000f64e791fcee4437448e1841f8b6ebd81bb97d358f84fcfe98f65a75`.
The candidate is
`432bb07ac6b0abcdcb38800d7c75a92c768b2b6bea583a1bab6834bb7f7b0d00`.
The losslessly stored patch's decompressed SHA256 is
`6e8992555e7c6f6616be48ec7e3e2f5626718bb08d1ebc243e0f466ebc912d22`.
`bindings.json` binds all 112 immutable prepared Python files, exact replacement
text and the preparation receipt. The other 111 Python files are unchanged.
The fixture and patch are separate: no scheduling barrier belongs in the product.

## Evidence and design intent

Read the [live issue](https://github.com/pixelelated/distribution/issues/588),
coordinator commit `b004cd4d0751bd871bfda11292b43280895f61ea`, and
`../2026-10-14-proxy-service-runtime/{README.md,attempt04/analysis.json,attempt05/analysis.json,startup-window-upstream.json}`.
Attempt04 observed online/queued/no flush, but did not control the startup
window. Attempt05's 139.59-second normal lifecycle explicitly observed an initial
offline worker result. Its accepted success does not close this separate case.

`upstream-history.json` contains read-only public history excerpts and exact
patch hashes. The original implementation
[`8c4c1f9`](https://github.com/misantronic/RAOfflineProxy/commit/8c4c1f9196099983c5444b2aa5c006ac227dbdd8)
intended softcore awards to flush on return online, with a startup flush followed
by a transition monitor. The reachability refactor
[`36c1e18`](https://github.com/misantronic/RAOfflineProxy/commit/36c1e1894fc2b4401e90c224e0d4760bc7ae7525)
kept both separate observations. Early-listener change
[`174d2b6`](https://github.com/misantronic/RAOfflineProxy/commit/174d2b6db483b5cf71cc1392500b36da8e6dcb03)
protects boot-to-game connectivity; this repair leaves that ordering intact.
The coordinator's exact upstream `2d19684e` source has the same sequence. This
supports fixing the handoff, with runtime causality still to establish. No claim
that upstream has no related issue is made. #585 owns contribution disposition
after the initial build and qualification; no submission occurred.

Local archaeology found today's #588 work-log entry and earlier offline-award
design/audit history. Its sandboxed issue search failed to connect; the explicit
authenticated read of live #588 succeeded separately. No new maintainer decision
is inferred. Coordinator owns the shared work-log/issue updates.

## Next source command

From the assigned checkout:

```sh
python3 docs/qa-logs/2026-10-14-proxy-startup-race-internal/check-source.py \
  --prepared /workspace/tmp/pix583-native-prepared-20261014-02
```

This checks hashes, fixture syntax, patch identity, unchanged periodic-loop and
cleanup ASTs without importing or executing product code. `static-result.json`
records the performed checks. Add `--candidate-output /tmp/FRESH-CANDIDATE` to
create a new small Python-only candidate tree. The original `source.json` remains
preparation provenance; `manifest.json` separately binds the repaired Python
bytes. The immutable original preparation must never be edited.

## Controlled source regression fixture

Can this be done on the VM? **Yes**, as already recorded in #588. Only the
coordinator allocates a fresh no-NIC guest and owner. The fixture refuses a guest
with any interface besides `lo`, forbids sockets and subprocesses, and writes
only to its new `/run` result tree. It uses real `ConnectivityMonitor`, an
AST-extracted exact startup slice, real queue insertion/dedup, signing, SQLite,
credential resolver, flusher and auth/error classification. Reachability and
HTTP GET/POST transport replies are controlled in-process substitutes. No native
hashing, actual service startup or network-probe qualification is claimed here.

The controller waits until the first monitor probe has entered, changes the
controlled connection only after the main false return, and releases the worker.
Real thread scheduling, `Event.wait(15)` and the flusher's three-second delay are
retained. The next natural poll must be observed, at least 15 seconds after the
first wait. Initial probing is bounded by a five-second fixture barrier, not a
shortened product timer. Ten candidate cases cover startup reconnect, already
online, persistent offline, ordinary reconnect, HTTP 401/403, HTTP 500, stop
during the first probe, stop before monitor start, and offline stop/reopen with
the exact pending SQLite row. Unrelated synthetic account cache/config bytes,
signed identity, retry count, integrity and joined-before-close are checked.

Inside the freshly allocated guest, after staging the packet and exact sources
at the named `/run` paths, the coordinator's watched payload can invoke:

```sh
PIX588_ALLOCATED_VM=yes python3 -I -B /run/pix588-packet/component-fixture.py \
  --source /run/pix588-baseline --variant baseline --cases startup-window \
  --output /run/pix588-baseline-result
PIX588_ALLOCATED_VM=yes python3 -I -B /run/pix588-packet/component-fixture.py \
  --source /run/pix588-candidate --variant candidate --cases all \
  --output /run/pix588-candidate-result
```

These are **separate original commands**, not a fail-fast shell chain. Preserve
each original return code. Expected baseline is **1**, with the exact causal
failure signature and an unchanged signed pending row; candidate is **0**.
`check-results.py --kind component` consumes the two result files and original
rc files; any import/guard/thread/cleanup failure is not a reproduced baseline.
Do not run this on the host. Cap: 240 seconds wall time, 45 seconds CPU with a
50-second hard cap, 512 MiB address space and 8 MiB per output file. No child
process is created. The outer watched owner still owns termination and delivery.

## Actual-main/systemd causal fixture

`make-service-packet.py` creates a fresh derivative of the accepted execution
packet. First restore its exact original 57 files with the coordinator's
`../2026-10-14-chd-native-runtime/coordinator/materialize-execution-packet.py`;
the original execution-manifest hash must be
`ad733a64f06e1bebd35c2b7f26242386bd588cf3502606a5addc6648fa5421a0`.
Do not point at the compressed storage representation as executable input.

```sh
python3 docs/qa-logs/2026-10-14-chd-native-runtime/coordinator/materialize-execution-packet.py \
  --source docs/qa-logs/2026-10-14-proxy-reconnect-observation-source \
  --destination /tmp/FRESH-ACCEPTED-EXECUTION
python3 docs/qa-logs/2026-10-14-proxy-startup-race-internal/make-service-packet.py \
  --execution-packet /tmp/FRESH-ACCEPTED-EXECUTION \
  --destination /tmp/FRESH-BASELINE-SERVICE --variant baseline
python3 docs/qa-logs/2026-10-14-proxy-startup-race-internal/make-service-packet.py \
  --execution-packet /tmp/FRESH-ACCEPTED-EXECUTION \
  --destination /tmp/FRESH-CANDIDATE-SERVICE --variant candidate
```

These preparation commands were checked locally with fresh `/tmp` destinations;
they do not launch anything. Both 58-file derivatives parse. The original owner,
cgroup guard, unit, unit-reference helper, census and cleanup AST are unchanged;
the controller is explicitly mode 0755. Compressed diffs retain the exact
observer and driver changes. `static-result.json` binds both generated manifests.

The narrow driver first creates a signed award through the real offline proxy,
then gracefully stops and confirms the exact row. Its second actual startup is
armed. `startup_gate.py`, called only by the existing profile observer, records
the real main probe's false return and holds the monitor **before** its first
actual forced probe. The controller confirms that process and row, starts the
accepted synthetic loopback peer, records the listener-open event, and atomically
releases that exact process. The original probe and HTTP paths run. The driver
observes the first and next natural online monitor returns, queue, application
count, original service stop status and SQLite integrity before asserting the
result. Baseline's original driver/owner exit1 remains failure evidence;
candidate requires original0. No crash/restart or 60-second worker suite is
replayed merely to repeat already accepted lifecycle05 evidence.

The added barrier has a ten-second deadline; its 50ms stop-aware wait only
controls fixture scheduling. It never rewrites a product wait or probe. The
existing 240-second driver, 272-second owner child wait, 280-second systemd owner,
kernel memory/task limits and cleanup remain. Expect roughly 30–45 seconds per
causal run; no bound may be extended after launch. Fresh baseline/candidate
owners and the coordinator's original 900-second VM wrapper (including its
private unified-cgroup boot) remain necessary. No owner/admission from earlier
attempts may be replayed.

Stage each derivative under the original guest packet paths expected by its
owner and observer, with its matching Python tree. This adapter preserves the
accepted installed-library binding and `source_pins_verified=false`. If the
coordinator supplies newly built native ELFs, separately rebind exact library
identities, recompute seals and retain their build/closure receipts before
launch. A changed filename is never native-source provenance. Candidate
`source.json` retains original preparation provenance while the service binding
explicitly records the post-preparation source repair.

`check-results.py --kind service` checks the narrow causal outcome and original
driver rc files. Coordinator must additionally consume original owner, wrapper,
watcher, host PID-exit, unit-reference, cgroup, cleanup and retirement receipts.
Installed composed-source service proof on the next assembled image and clean/
retained-storage qualification are still owed. No #588 acceptance checkbox can
be closed from this source-only packet alone.
