# Actual proxy service lifecycle — #583 / #584, prepared only

**UNRUN.** This is one next serialized proof, with no product change, source pin
promotion, runtime reservation or new native build. Coordinator checkpoint
`62f3ba31b247a94414fb77155ad4ea9a0c5005ac` and complete live issue/comment reads are
retained under `evidence/`. The accepted independent-format attempt02 and native
proxy attempt01 remain accepted at their original scope; this packet invokes
neither suite, preparer nor converter. No old owner or disk is reused.

Can this be done on the VM? **Yes:** an allocated no-NIC GENERIC_X64 guest can run
the actual `main`/`run-service` path and installed systemd against entirely
synthetic storage and a numeric-loopback protocol peer. Coordinator records the
new allocation in the issues. No owner/account/provider input is required.

The remaining distinction is concrete. The accepted native fixture called
`ProxyRuntimeServer` and explicit flush functions. Here the packaged unit's
unchanged `ExecStart=/usr/bin/python3 -m raofflineproxy.main run-service` and
`ExecStartPost=/usr/bin/raofflineproxy-ctl listening --wait 30` run under PID1.
The latter only proves an IPv4-capable listener; the fixture additionally binds
its inode/fd to systemd MainPID, numeric PID/start identity, service.pid/status,
network namespace, exact source and expected cached User/Token/game response.
An unrelated listener is never taken as service readiness. The already accepted
126 routing and impostor controls are not replayed.

`bindings.json` fixes all 112 prepared Python files, the 16-patch composition,
corrected RVZ reader, exact packaged unit/controller, and accepted old-image ELF
hashes. Use the existing `/workspace/tmp/pix583-native-prepared-20261014-02` tree;
do not prepare it again. `source_pins_verified` stays **false**. Hashing old-image
ELFs at a new boot cannot establish current native-build provenance.

## One executable sequence, not a new general test harness

| New seam | Assertion / retained artifact |
| --- | --- |
| Unit condition and real startup | Absent synthetic marker skips start; present marker starts actual main, real packaged readiness exits 0, PID/socket/status/body agree, all five worker `run` methods enter with original timers |
| Graceful stop | One newly queued synthetic A/104 signed row survives byte-for-field; original ExecMain exit 0, pid file removed/status stopped, five workers joined before SQLite closes, old PID absent |
| Explicit restart | A separate start and actual `systemctl restart` create distinct owned incarnations with unchanged pending row and valid cached sign-in |
| `Restart=on-failure` | One deliberately **idle** SIGKILL retains original code 2/status 9, then original five-second systemd policy creates exactly one automatic restart with queue intact; no replaying the command to turn failure into success |
| Natural background reconnect | Start the local peer after recovery; actual ConnectivityMonitor flushes A/104 once within its 15-second polling cycle. Peer independently checks the original HMAC/chain fields. No explicit flush call is made |
| Natural queue-worker/lock boundary | Seed one synthetic hash-to-game mapping in the disposable queue. Hold its actual bulk-run lock through the first natural 60-second poll; no lookup/drain occurs. Release it; the second natural poll resolves the mapping through the peer and retires the queued item |
| Other worker lifetime | Empty FolderWatcher poll and consent-disabled UsageReporter pass occur at 60 seconds; PeriodicRefresh stays in its original one-hour wait. Graceful final stop joins all five before storage close |
| Final ownership | Original systemctl/child exits, service journal, observer events, queue snapshots, requests and source/ELF/tool/boot identities; SQLite integrity, protected synthetic settings/key bytes, empty owned cgroup and no surviving driver children |

The seeded hash `e5830000000000000000000000000001` is a deliberately fabricated
mapping to already cached synthetic game10. It is not a new ROM hash/parity
claim. The SQLite/key seed is an exact copy of the accepted native fixture's
synthetic final state, with no pending awards. The existing local peer,
cached-readiness functions and numeric census/pidfd functions are reused
byte-for-byte in `reference_native.py` and `census.py`. The small `owner.py`
adapts the accepted owner only for paths, no old admission argument and the new
bounded driver timeout; `owner-reference.py` preserves its original bytes.

## Boundary and observations

The packaged unit is copied under the new, fixed name
`pix583-service-proof.service`, never enabled. A recorded drop-in gives it only
synthetic `/storage`, a minimal synthetic `/etc/profile` for the unchanged
controller's listener command, the exact staged controller and Python tree,
resource limits and source observers. The condition path is reset to the owned
synthetic marker because systemd evaluates conditions outside the unit's mount
namespace. The installed proxy must be inactive and ports8080/18081 free; the
fixture never stops an existing proxy. Boot-marker reconciliation and real
profile helpers are consequently outside this proof.

`bootstrap/sitecustomize.py` runs before actual main. It verifies the storage
bind identity, source and ELF hashes, installs fail-closed file/SQLite/exec and
loopback socket guards with negative controls, then observes selected Python
call/return events. It changes only the same dependency-discovery and
loopback-interface boundaries used by accepted native attempt01. It does not
replace worker bodies, timers, signals, storage, HTTP, signing or flushing.
Observer overhead prevents treating these timings as performance measurements.
Unexpected imports/library loads/child execution fail; they are not silently
stubbed. Native code is still contained by the disposable no-NIC guest, not by
claims that a Python audit hook sandboxes arbitrary C.

The service unit is `BindsTo` the fresh systemd owner with explicit ordering.
If the owner exits, systemd stops this fixture's service. The driver also stops
and verifies only its sealed unit/cgroup in `finally`, then removes its two
temporary unit files and reloads definitions. On unknown quiescence or changed
unit identity it retains FAIL and the files for coordinator inspection. The
systemd owner has its own finite lifetime; no process-name scanning or broad
kill is used. The deliberate unit SIGKILL is a test input, distinct from owner
cleanup intervention, which fails the run.

## Stage and first execution — HELD

Use a **fresh** accepted VM20, cgroup v2 and systemd PID1, only `lo`, no route,
exclusive TCP127.0.0.1:8080/18081. The installed Python/systemd/Bash/controller
targets and three recorded native ELF paths must exist. Their actual hashes,
invocation paths and boot identity are recorded. An unsupported systemd mount
directive, missing prerequisite or changed ELF refuses; install nothing.

Coordinator stages this sealed packet read-only at `/run/pix583-service-packet`
and the already verified prepared tree at
`/run/pix583-service-inputs/prepared`. Total staged data <=8MiB. No oracle/ROM
copies, host dependency installation, compilation or re-preparation is needed.
Provision a dedicated **64MiB tmpfs** at `/run/pix583-service-owner` with >=48MiB
free; reserve16MiB for exported receipts. All names/paths below must be unused.

```sh
systemd-run --wait --unit=pix583-service-proof-owner \
  --property=RuntimeMaxSec=280s --property=TimeoutStopSec=20s \
  --property=KillMode=control-group --property=MemoryMax=1G \
  /usr/bin/python3 -I -S -B /run/pix583-service-packet/owner.py \
  --output /run/pix583-service-owner/run01
```

Driver:240s work +30s cleanup,768MiB AS/120CPU seconds/4MiB per file. Actual
proxy unit:512MiB memory and AS/120CPU seconds/4MiB per file/64 tasks, original
15s stop timeout,5s restart delay and5 starts/300s limit. Four starts are planned;
the start-limit exhaustion branch is not exercised. The outer coordinator owner
caps the command at310s plus10s forced cleanup and records its original exit.
Normal duration is governed by two real60-second polls, not shortened timers.

Consume `run01/owner-result.json`, `payload/result.json`, `commands.json` and
all original command stdout/stderr, service stdout/stderr/journal, per-PID
observer records and pending snapshots before any further allocation. The
expected idle-crash exit remains9; no clean-exit event is required for that
incarnation. Every graceful incarnation requires actual worker-stop/storage
ordering. If the owner itself dies, collect its systemd original result and
verify both units/cgroups stopped before exporting/retiring the guest. Do not
silently retry this packet or reset the start limit to force it through.

## What still needs a build or separate acceptance

- **Current native source provenance and final installed dependencies require
  compiled artifacts.** Produce or reuse provenance-bound builds of the selected
  rcheevos/bridge/libchdr/Dolphin composition and qualify the assembled image;
  already qualified unchanged builds need not be repeated. Another fixture with
  VM20's old ELFs cannot make source_pins_verified true.
- **Final-image integration requires the assembled image:** packaged Python and
  dependencies without PYTHONPATH/bind overlays, real boot-marker/toggle ordering,
  clean/retained storage, frontend notice/UI and actual Dolphin host behavior.
  This copied-unit proof cannot check those boxes.
- **CHD/native parity needs the already scoped converter/native allocation,**
  not a fake CHD or a repetition of accepted NONE/Zstd parity. Native Dolphin
  client/gameplay behavior remains separate from cached HTTP contract proof.
- **Remaining lifecycle branches do not inherently need a full-image build:**
  a nonempty folder scan, production controller scan/pause locking, active
  request interruption, start-limit exhaustion and the one-hour refresh pass
  need their own justified bounds if still material. This proof covers the
  queue worker's own bulk lock, not that shell scanner's separate lock.
- No real provider acceptance, concurrent multi-account award queue, power-loss
  durability, memory saving or browser-owned shutdown policy is claimed.
  Browser experiment#587 stays backlog under D-RA-047, not a new M7 gate.

This is a fork systemd-integration QA packet. Existing upstream dispositions
remain padding → RAOfflineProxy, scanner → distro, and routing → conditional
ROCKNIX integration (#585/D-WORKFLOW-164/165). No new product fix or upstream
submission is selected. Historical packets and shared records are unchanged.
`preparation-history.json` retains one source-binding preparation mistake
(wrong manifest key, exit1); no product/fixture ran. Static validation is recorded
separately and cannot confer runtime acceptance.
