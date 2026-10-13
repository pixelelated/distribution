# #567 fixed-endpoint library fixture — source only, UNRUN

This packet closes the executable-harness gap in the immutable
[library setup handoff](../2026-10-13-library-setup-source/README.md). It supplies
a disposable-guest runner, a loopback TLS endpoint server, an explicit
`raofflineproxy-ctl` seam, and synthetic prehashed gamelists. No production
source, old packet, catalog, shared record or pin changes. Coordinator w4:p2
owns admission, VM preparation, execution, frames and integration.

**No runtime result is claimed.** The three executable sources were neither
executed nor imported. Static checks parse their AST, XML and source bindings;
they do not prove Python namespace availability in an installed image, TLS,
ES startup, rendering, indexing or cleanup. The earlier #565/#571/#575 and
library-baseline receipts are not evidence for this fixture.

## Exact boundary and prerequisites

The fixture launches the installed ES binary directly on the coordinator's
already-running Wayland compositor, within new private mount and network
namespaces. It never starts/stops a service. It requires root in a disposable
VM, the exact expected BUILD_ID and ES SHA256, and a declared full ES source
commit. That declaration must be backed by the coordinator's build receipt;
a binary hash alone does not establish its source.

The **parent guest must have only loopback, with no virtual NIC**. This is
deliberately stronger than removing the default route: existing services or
privileged Unix-socket brokers cannot forward to a physical/host network.
The child additionally gets a new network namespace with only `lo` brought up.
No bridge, veth, tunnel, forwarding, DNS listener or external upstream exists.
The fixture refuses a parent NIC before starting children or mounting anything.

There is one concrete allocation prerequisite: the current
`projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm` always emits `-netdev`
and its matching `-device ...,netdev=net0,...`; it has no no-NIC run mode.
For this fresh allocation the coordinator must prepare/review QEMU argv with
those two argument pairs removed and `-nic none` added. Preserve its disk,
UEFI, display, RAM, serial, monitor and watcher ownership. Appending `-nic none`
while leaving the explicit `net0` device does **not** satisfy the prerequisite.
Use serial for commands and transfer; there is no SSH forwarding in this VM.
No old owner, port, disk, process or launcher command is reusable authorization.

Installed prerequisites are source-backed: Python 3.14.7 with SSL (Python3
recipe depends on OpenSSL), OpenSSL CLI, util-linux `mount`, BusyBox `ip`,
GENERIC_X64 `CONFIG_NAMESPACES=y`/`CONFIG_NET_NS=y`. The runner checks Python
`os.unshare`, mount/network constants, pidfd cleanup functions, installed
resources/theme/locales, readable hosts/resolver/trust files and the Wayland
socket. Actual syscall/mount failures retain their original child exit and
refuse the run. It does not install missing tools or fall back to an uncontained
listener. BusyBox and target util-linux do **not** ship the `unshare` command;
the runner uses Python's syscall wrapper, not an assumed CLI.

## Guest installation and first command (prepared, not run)

1. Allocate the isolated guest above through the coordinator's current watched
   owner. Stop/hold its frontend service using the coordinator's service-lifetime
   procedure; source units are `essway.service`/`emustation.service`. Preserve
   its compositor. The fixture refuses any existing `emulationstation` process.
   Do not run `start_es.sh`: it sources `es_settings` and changes settings before
   launching ES. This fixture invokes only the binary after isolation.
2. Transfer only this packet to `/tmp/pix567-fixture` through the owned serial or
   another already approved offline staging mechanism. Verify `SHA256SUMS` and
   preserve executable modes. No files go in the guest's real `/storage`.
3. Supply candidate-bound values for `PIX567_BUILD_ID`, `PIX567_ES_SHA256`,
   `PIX567_ES_SOURCE`, `PIX567_XDG`, and `PIX567_WAYLAND`. The last two name the
   current compositor's actual runtime directory/socket, not a historical guess.
   The service's source default runtime directory is `/var/run/0-runtime-dir`.
4. The first **fixture** command in that allocated guest is:

```sh
python3 /tmp/pix567-fixture/run-fixture.py \
  --disposable-guest --case success --output /tmp/pix567-success-en640 \
  --expected-build "${PIX567_BUILD_ID:?candidate BUILD_ID required}" \
  --expected-es-sha256 "${PIX567_ES_SHA256:?candidate binary SHA256 required}" \
  --es-source-commit "${PIX567_ES_SOURCE:?candidate ES commit required}" \
  --xdg-runtime-dir "${PIX567_XDG:?current Wayland runtime required}" \
  --wayland-display "${PIX567_WAYLAND:?current Wayland socket required}" \
  --language en_US --trigger api
```

Do not pipe this command through a success-producing wrapper. The owner must
consume its original process exit and `result.json`, `worker-result.json`,
`worker.stderr`, ES/listener stdout/stderr and each `*.exit.json` command result.
Use a new `/tmp/pix567-NAME` output for every case. Repeat by replacing `--case`
with `failure`, `no-account`, or `no-new-work`; do not rerun a completed owner.

## What is installed, and how it reverts

Inside the child only, `/` becomes recursively private. Five binds cover
`/storage`, `/etc/hosts`, `/etc/resolv.conf`, `/etc/nsswitch.conf` and
`/usr/bin/raofflineproxy-ctl`. The first is fresh synthetic storage under the
output directory; no player storage is read/copied into it. Three small
resolver files map only `retroachievements.org` to `127.0.0.1`, use `hosts: files`
and provide a loopback-only resolver fallback. The last bind is the explicit
Python seam. The runner reads back bound file hashes and saves mountinfo;
it does not use `mountpoint -q` to infer a file bind.

No trust store is edited or bound. ES sets `CURLOPT_SSL_VERIFYPEER=0`, while
hostname checking stays at libcurl's default for these calls. The runner
creates a one-day self-signed certificate with the exact DNS SAN. Only its
own readiness client loads that certificate as a trust anchor. The generated
private key stays mode 0600 in guest `/tmp` and is removed on normal/error
cleanup; it is never a committed fixture or evidence artifact. The runner
records and compares the original public CA bundle before/after the child.

Settings, gamelists, cookies, recovery and simulated proxy stamps exist only
under the synthetic storage bind. Resources, locales and theme are symlinks to
installed read-only defaults, not expensive copies. ES logs use the output's
`logs/` directory. ES may also use its ordinary guest `/tmp` lock paths; this is
one serialized disposable-guest run, not a retained-storage test.

The listener and ES are child processes with PID/start-tick records. TLS
readiness requires a real validated handshake and exact synthetic response,
not merely a pidfile. ES readiness requires its local API and exactly one
initial library-load log, with no indexing requests consumed at startup.

The worker asks ES's `/quit`, waits for its original exit, then terminates and
reaps the listener (its signal handler exits normally). Forced exits fail the
fixture. The outer owner bounds the whole child process group to 240 seconds,
records timeout/cancellation and the original return code, and retires any
remaining processes identified by **both fresh namespace identities**, using
pidfds. Stragglers make the result fail. Mounts disappear with their namespace;
the parent compares hosts/resolver/trust/code hashes, mountinfo and the original
storage mount identity. Never unmount or overwrite the guest's global files to
"restore" these private binds. Archive receipts, remove only the owned `/tmp`
packet/results when accepted, and retire the disposable VM through its owner.
If the owner itself is forcibly killed, retire the VM; do not claim cleanup
from a missing result. No service is restarted automatically.

## Cases and required counts

All `.gb` files are short text saying they are not ROMs. Their system command
is `/bin/false`. Each game has a synthetic MD5-shaped metadata string; this
tests the existing **prehashed/no-ID lookup** path, not ROM hashing or gameplay.
One already identified game prevents startup from consuming the new-work
stimulus. Only after ES is ready does the runner add `new.gb` and its gamelist
entry, then issue `/reloadgames` or let the coordinator use the UI.

The listener's mandatory controls precede ES: one official-list readiness
request, two HTTP refusals (unknown endpoint and wrong Host), one wrong-SNI TLS
refusal, unknown-name resolution refusal, and an unreachable TEST-NET address.
They have separate `tls-controls.json` counts. The table is the **ES delta**:

| Case | hashlibrary / official list | new ID persisted | after-index calls / actual ES-observed exit | simulated games prepared |
| --- | --- | --- | --- | --- |
| success | 1 / 1 | 1 | 1 / 0 | 1 |
| failure (hashlibrary HTTP 503) | 1 / 1 | 0 | 0 / none | 0 |
| no-account | 1 / 1 | 1 | 1 / 77 | 0 |
| no-new-work | 0 / 0 | 0 | 0 / none | 0 |
| UI NO, any case | 0 / 0 | 0 | 0 / none | 0 |

Every successful YES case needs exactly one additional library-load log.
NO needs no additional load. The failure case needs `Game Hash failed :`.
Zero-count cases wait for the rescan barrier and a quiet interval; an API
request merely being accepted cannot pass them. Unexpected ctl verbs, extra
TLS/HTTP requests, changed text stubs, exit disagreement, absent identity
metadata, unexpected simulated stamps or extra rescans fail. Top-up events
are checked against the actual exit ES logs from `executeScriptLegacy`, not
only the seam's self-reported intention. Final shutdown must add no requests.
`/isIdle` alone is insufficient while the UI thread is synchronously fetching
the library: `ThreadedHasher::mInstance` may not yet be assigned. Work cases
therefore require the actual recovery/top-up or failure-log observation. Every
case also requires a normal ES quit and unchanged final request counts; the
main loop must consume the queued quit after the rescan returns. `observed.json`
is provisional; only the final worker/outer results establish success.

The seam recognizes read-only pending/summary/account queries as empty.
For successful `topup --after-index` it first reads the **actual ES recovery
XML**, then writes a synthetic one-game-added stamp/ready list and exits 0.
For no-account it exits 77 without a stamp, matching the installed ctl's
pre-probe refusal contract. No account fields, login data or real cache are
created. This does **not** test the installed backend's account detection,
HTTP probe, SQLite cache, authenticated download, cache revalidation or ordinary
reconnect path. Those remain separate coordinator-owned backend tests.

## UI fixture and remaining qualification

Use `--trigger ui` for the same isolated data/endpoints. After `armed.json`,
capture Game Settings → UPDATE GAMELISTS → the existing confirmation, choose
YES or NO, then write exactly that choice to the output's `ui-choice.txt`
through serial. The runner does not inject input. It waits up to 100 seconds
for the choice. After observation, `frame-ready.json` allows up to 25 seconds
to finish frames; create `frames-done` to release it. This holds the process,
not the lifetime of a transient card: capture progress/outcome as it appears.
The initial command's 240-second total deadline still applies.

Run English and French at actual 640×480 and 1280×800 under the coordinator's
display profile; the fixture does not resize/render or take screenshots.
Record candidate binary/catalog bindings, actual dimensions, reviewed advance
notice, YES rescan/outcome, NO return, and returned responsive library. The API
mode bypasses the confirmation by production design and supplies no copy/frame
proof. This fixture keeps offline achievements and startup indexing on; the
disabled/index-off/backend-absent/busy branches in the original packet remain
separate branch qualifications. A 503 is a controlled endpoint failure, not
a physical link-loss measurement. Parent/child loopback-only topology means the
frontend's network-status icon can be offline even in the TLS success case.

Useful refusal controls (UNRUN): incorrect BUILD_ID or binary hash, reused
output, existing ES, parent NIC, unavailable namespace syscall, missing Wayland
socket, missing bind target, occupied listener port, malformed response fixture
source, and an unexpected ctl verb. Each must retain a nonzero original exit
and must not be rewritten into a success receipt. There is no retry against
the public service.

`source-bindings.json` binds the inspected production files. `static_check.py`
is a read-only AST/XML/hash check that never imports the runtime sources.
`static-result.json` records that check only. Coordinator-owned canonical flow,
copy, issue and evidence-index updates remain the original #567 proposal; this
packet introduces no product language or new recurring confirmation.

The source-only check used for this packet is:

```sh
python3 docs/qa-logs/2026-10-13-library-index-fixture/static_check.py \
  --es /home/max/Development/emulationstation-next.worktrees/m7-save-capabilities-575 \
  --distribution /workspace/repos/rocknix.worktrees/m7-clean-state-565
```

It checked 35 immutable production/reference source files, four Python ASTs
(including itself), four XML fixtures and their eligibility/prehash shapes.
The runner's result files described above do not yet exist: only the static
receipt is included in this commit. No compiler, listener, service, VM,
emulator, account, device or fixture runtime was used to produce it.
