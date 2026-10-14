# Native proxy integration admission — #583 / #584

Prepared only. **Every new preparer, admission helper, owner, and integration
fixture is UNRUN.** This packet changes no product, package pin, service, setting,
or previous packet. It provides one executable next experiment after coordinator
allocation and the independent DolphinTool input delivery. No runtime lease exists.

Readback used coordinator checkpoint `e0f532718e` and the complete live #583/#584
issues/comments on 2026-10-14. The checkpoint retires the prior RVZ VM and all its
owners. Nothing here reuses that allocation. Exact completed result copies are
in `evidence/`: 126 corrected padding comparisons, 44 scanner controls, and 126
routing cases passed. The prior failed imports/census runs remain historical
failures in the coordinator packet. These suites are not invoked here.

`bindings.json` fixes RAOfflineProxy
`c7ebd1b6e777f3751ff0ecdf8aba54045844e00d`, its archive/recipe and all 16 current
distribution patches, 112 resulting Python files, and the reviewed #583
`22cfb2385acce6d9c20b20d2f7f40970808777b3` padding/scanner bytes. Only
`rvz_datasource.py` differs between the baseline and candidate Python manifests.
The scanner is the exact embedded `list_jobs` code from the reviewed control
script. The earlier lazy-CLI/bytecode experiments are not part of this composition.
Preparation uses the qualified small-tree method; runtime extends the qualified
`ProxyRuntimeServer` readiness method. Their original files are reference copies,
not silently rebound historical fixtures. Licenses are retained.

The installed `libraproxy_rchash`, libzstd, and libcrypto are loaded in the future
VM; nothing is compiled, installed, or copied from a host build. Admission records
their invocation paths, resolved bytes, SHA256 and actual mappings. **The accepted
image predates the current source. A matching filename is not build provenance.**
Current source pins are recorded in the binding, but `native_provenance` must say
whether a coordinator-reviewed build receipt establishes them. With unverified
provenance, a PASS is evidence for the exact installed ELF hashes plus the exact
prepared Python composition; it cannot qualify a new production native build.

| Remaining seam | Executable assertion in `fixtures/run.py` | Evidence if it passes |
| --- | --- | --- |
| Native ISO/RVZ bridge | Real `hash_rom_candidates_result` on one public ISO and independently encoded NONE/Zstd RVZ; all three equal the admitted nonzero GameCube hash; installed bridge and Zstd appear in process maps | Exact source/native-byte integration; no repeated Python padding suite |
| Scanner into native cache | One failed ES zero-hash RVZ, real reviewed scanner, exactly one H job, real native hash, real game-ID lookup and patch/unlocks/sets/session caching via local peer | Explicit-scan handoff with an independently encoded input |
| Account/cache isolation | A and B have separate cached unlocks; unknown account cannot obtain A's cached patch/login; B cache bodies stay unchanged through A's flush | These named account paths only |
| Readiness and identity | Offline login requires HTTP 200, proxy/offline headers, Success true and exact synthetic User/Token; next-game patch ID 20; own socket inode in `/proc/net/tcp`, fd, PID/start ticks, module SHA and network namespace | Identified fixture-owned proxy endpoint, not a listener-only claim |
| False readiness | A separate local server returns HTTP 200 and forged proxy headers with unrelated User/Token; readiness must reject it | An unrelated 200 is insufficient |
| Awards and security | Queue 101, duplicate 101, 102; exactly two rows; independently recompute canonical SHA256/HMAC chain; reject hardcore 201 unchanged; preserve rows on SQLite close/reopen; tampered separate DB refuses before HTTP | Synthetic signed offline queue and same-account dedup |
| Failures and reconnect | Real closed/opened loopback peer drives real reachability probes; 401/403 login never becomes cached success; patch 500 and award 401/500 retain signed fields and expected retry state; reconnect submits exactly twice; empty flush never resends | Original failure states and successful synthetic replay, not provider award acceptance |
| Next game / cleanup | Reopen cache after flush; old unlocks ready, next-game unlocks empty, SQLite integrity ok; synthetic config bytes unchanged; no lingering threads, listeners or direct/adopted children | Explicit lifecycle exercised below, with retained receipts |

The signature is the proxy's local HMAC chain, not a server-issued/asymmetric
signature. The peer independently checks the queued achievement's chain fields,
HMAC, key ID, token/account and offset validation MD5. All usernames, tokens,
achievement definitions and signing state are disposable synthetic data. No
commercial ROM, provider credentials, existing cache, game save or award is used.

Two deliberate boundary substitutions are recorded in source: dependency discovery
returns the admitted installed paths instead of allowing `find_library` to invoke
ldconfig/compiler discovery; and `has_active_network_interface` returns true so
actual numeric-loopback HTTP probes can operate in a VM with only `lo`. Neither
hashing, decoder, SQLite, signing, HTTP forwarding, queue/flush code, nor
`is_online` is replaced. No rate limit, timeout or failure expectation is relaxed.

The Python audit guard is installed before any proxy import. It denies child
execution, outside-fixture writes/SQLite, owner-config reads, nonnumeric DNS and
all sockets except TCP IPv4 on the two allocated loopback endpoints. Negative
controls must pass before native loading. `encodings.ascii` is preloaded, retaining
the prior guard's intent without the qualified fixture's lazy-codec import failure.
The guard is not a sandbox for arbitrary C code: the no-NIC guest, immutable known
ELF inputs, private scratch mount and coordinator's outer VM owner remain required.

## Inputs and preparation, held

The #574 converter preparation at
`1c0e93b4b34501928c79f9ade5b2b4c1442331a4` has not delivered its oracle here yet.
Reference copies of its original driver/bounds/source binding are retained for
readback only. Do not run them as part of this allocation. Supply these public
synthetic artifacts later, retaining their original receipts:

```text
/run/pix583-native-inputs/
  prepared/                 # output of this packet's prepare.py
  synthetic-manifest.json   # generator's original manifest.json, renamed only
  synthetic.iso             # 0x60000 bytes, PX5740 header, exact manifest SHA/hash
  dolphin-none.rvz           # independent DolphinTool encode, block 131072
  dolphin-zstd.rvz           # independent encode, block 131072, Zstd level 3
  oracle/result.json
  oracle/encode-{none,zstd}.json
  oracle/roundtrip-{none,zstd}.json
  oracle/hash-{none,zstd}.json
  oracle/hash-{none,zstd}.stdout
  native-provenance.json
```

Oracle result must be PASS, each original child exit 0 without timeout, encode
SHA match the supplied RVZ, and both full decoded-ISO SHAs equal the supplied ISO.
Hash output must equal the generator's expected hash plus newline. Each receipt's
executable hash must match the admitted DolphinTool or recorded independent hash
binary; conversion flags and hash command are checked. This fixture never invokes
either binary. The original round-trip ISO copies need not be staged again.

Run source preparation on the host with an existing GNU patch, then stage the
verified small tree. Do not assume GNU patch exists in the guest. The preparer
checks GNU patch explicitly, records interpreter/tool identities and each original
patch exit, refuses fuzz/reversed/failed patches and changed source, and retains
`source.json` on failure after preflight. Offset diagnostics are accepted only
when the complete patch stdout exactly matches the SHA-bound qualified prior
transcript and stderr is empty; unrecorded offsets are refused. The final exact
112-file baseline and candidate manifest checks remain mandatory. See
[the offset follow-up](preparation-offset-followup/README.md) for original FAIL1
and transcript binding. It has a 45-second alarm, 5-second per-patch timeout and 10 MiB extracted
source budget. Allocate at most 32 MiB preparation output; the immutable cached
archive remains in place. No dependency install or native build is needed.

```sh
python3 -I -S -B docs/qa-logs/2026-10-14-proxy-native-integration-source/fixtures/prepare.py \
  --repo /workspace/repos/rocknix.worktrees/m7-browser-memory-570 \
  --archive /ABSOLUTE/EXISTING/RAOfflineProxy-c7ebd1b6e777f3751ff0ecdf8aba54045844e00d.tar.gz \
  --output /ABSOLUTE/FRESH/native-proxy-prepared
```

The archive SHA is
`88eef31acfa4104b20258bd5cea514ade30e6cdf35767ffc958009851d61898b`.
`--archive` is a supplied existing path, not a download instruction. Read back
packet SHA256SUMS and preparation hashes after staging. Keep staged public input
and prepared source at most 32 MiB, immutable through the run, with no symlinks or
unbound bytecode. Stage the packet itself at `/run/pix583-native-packet`.

`native-provenance.json` requires the exact accepted image SHA, a boolean
`source_pins_verified`, and a nonempty `qualification`. Use false when source
provenance is unavailable; do not invent a build receipt. If true, also supply
`build_receipt: {"path": "relative-staged-file", "bytes": N, "sha256": "..."}`
for the coordinator-reviewed receipt linking native source/recipe/patch pins and
installed ELF hashes. The fixture verifies that receipt's identity, not the truth
of an arbitrary declaration. A template with the honest unverified state is
provided. Coordinator review supplies the final admission; no edit to this sealed
packet is necessary.

After exclusive allocation, create admission by hashing the installed files
(arguments must be actual guest invocation paths; symlink targets are recorded
separately). The helper performs no load, conversion, service start or network
operation and has a 10-second limit. Inspect its JSON and retain its printed SHA:

```sh
python3 -I -S -B /run/pix583-native-packet/fixtures/admit.py \
  --image-sha256 1a23cf5740dbb69cdca76d753a0f6121c35e6e12f27649e792aeebc71e8cc490 \
  --dolphin-sha256 ACTUAL_QUALIFIED_DOLPHINTOOL_SHA256 \
  --rchash /usr/lib/libraproxy_rchash.so \
  --zstd /usr/lib/libzstd.so.1 --crypto /usr/lib/libcrypto.so.3
```

## One serialized VM entrypoint, held

Can this be done on the VM? Yes: this is synthetic GameCube input and a local
protocol peer. Coordinator records the allocation in #583/#584 before execution.
Use one fresh accepted GENERIC_X64 no-NIC guest, `lo` up, no IPv4 route, installed
Python with SQLite/native bridge/Zstd/libcrypto, and exclusive 127.0.0.1 ports
8080/18081. Refuse an occupied port; never stop an existing proxy. No settings or
credentials from the image are used. Refuse native loader overrides.

Coordinator provisions a dedicated **64 MiB tmpfs** at
`/run/pix583-native-owner`; entry requires at least 48 MiB free and verifies this
mount. Reserve another 16 MiB elsewhere for exported receipts. Inputs/packet live
outside that scratch mount. Expect only a few MiB of fixture state, but the hard
mount limit protects failure cases. The child has 512 MiB address-space, 120 CPU
seconds, 8 MiB per-file, and no core dumps; work alarm 180 seconds, cleanup alarm
10 seconds. Owner waits at most 190 seconds, then signals only identity-checked
child pidfds; adopted-child cleanup has 3 seconds. Coordinator's outer owner must
cap the complete command at **200 seconds**, retaining its original status even
if the Python owner itself cannot finish. No retry in this allocation.

The owner reuses the three qualified numeric `/proc/PID/stat` census/pidfd helper
functions byte-for-byte from `3a65a2d4d274105cd5a1b2e72c44450f7dbbdafe`.
No optional `task/children` file or process-name matching is used. An observation
error records FAIL and unknown children; it never becomes an empty census.
Parent-death SIGKILL and a new session contain the one native child. Any unexpected
descendant, cleanup signal or retained error makes this run FAIL.

Smallest integration command after that preparation/admission:

```sh
python3 -I -S -B /run/pix583-native-packet/fixtures/owner.py \
  --admission /run/pix583-native-inputs/admission.json \
  --admission-sha256 ACTUAL_REVIEWED_ADMISSION_SHA256 \
  --output /run/pix583-native-owner/run01
```

Consume `run01/owner-result.json`, exact `stdout`/`stderr`,
`payload/result.json`, native maps, source/admission/tool receipts, and the two
synthetic SQLite stores/signing state. Owner records original child exit, timeouts,
signals, numeric child observations and artifact hashes. Payload records native
hashes, queue snapshots/failure outcomes, exact stub requests, HTTP responses and
readiness identity. Preserve first failures; do not regenerate or pass by retry.
Export before unmount/retirement under coordinator control.

## Explicit remaining limits and disposition

This tests `ProxyRuntimeServer` and explicit cache/flush calls, including closed
and reopened storage and local listeners. It does **not** execute `main`,
`run_proxy_service`, systemd/socket activation, periodic workers, scanner shell
locking/pausing, or native Dolphin/rcheevos login/gameplay. The #584 script's 126
qualified full-script cases are reused as evidence; it is not rerun here. Its
bound bare HostUrl is 127.0.0.1:8080, the endpoint identified here. Its production
listener gate is not upgraded into an identity check by this fixture.

No claim of arbitrary simultaneous-account award queues: the current queue's
dedup key is achievement ID. Here only A queues awards; B cache/unlock isolation
is checked. No claim of real server token/signature acceptance, Wii hashing,
all RVZ compression modes/full commercial-disc integrity, ARM64 execution,
settings migration, abrupt power-loss durability, memory savings or gameplay.
Independent converter delivery, native build provenance/ABI, installed full
service lifecycle and Dolphin acceptance remain explicit blockers/qualifications.

Upstream disposition remains the reviewed packet's: padding for RAOfflineProxy;
scanner for the distribution control script; Dolphin routing conditionally for
ROCKNIX/distribution. No new product candidate or upstream post is created here.
D-WORKFLOW-164/165 disposition and build ordering remain coordinator-owned.
