# RAOfflineProxy memory candidate — October 13, 2026

[#570](https://github.com/pixelelated/distribution/issues/570), bounded worker
`pix-memory`, Herdr `w4:p8`, branch `feature/m7-browser-memory-570`.
Coordinator `w4:p2` owns runtime allocation, GitHub status and integration.

**An upstreamable lazy-UI-import candidate is prepared and passes the allocated
host source checks. It is not a measured target memory fix.**
[lazy-ui-imports.patch.gz](lazy-ui-imports.patch.gz) moves two imports from module scope
into their four CLI branches. `run-service` retains four fewer proxy modules:
`menu_sdl`, `menu_input`, `ui`, and `knulli_service`. The daemon's service,
request, credential, consent, queue and storage code is byte-for-byte unchanged.
The patch is an experiment here, outside the automatically applied package
patch directory; no shipped recipe, pin or installed file changes.

## Source and upstream applicability

The exact upstream archive for `c7ebd1b6e777f3751ff0ecdf8aba54045844e00d`
matches the recipe's SHA-256. All 16 current package patches apply with fuzz zero,
followed by this candidate. [source.json](source.json) retains each patch's hash
and application output, every extracted Python source hash, and both variant
manifests. Only `linux/raofflineproxy/main.py` differs between variants. Preparation
extracts 1,512,945 bytes of Python source/tests, without dependencies or native
assets, from an existing archive; it does not copy an accepted build cache.

The patch is now stored as deterministic gzip to preserve unified-diff context
bytes without Git whitespace warnings. Its decompressed bytes are identical to
the candidate in the original commit, with SHA-256
`dfb928914db789df85e743755d6057c16a3b9164da33f869cd339c943d0a24ae`, also recorded in
[lazy-ui-imports.patch.sha256](lazy-ui-imports.patch.sha256).
The updated preparer checks that identity and feeds decompressed bytes to GNU
patch on stdin. Future preparation records retain the logical patch name and
uncompressed `sha256`, plus `artifact_name`, `artifact_sha256` and `encoding`
for the gzip file. Historical `source.json`, host receipts/results, analysis,
and the executed `check.py` remain unchanged; their evidence belongs to the
original preparation and one host run. This follow-up performs static syntax,
byte-identity and hash checks only; the modified preparer has not been rerun.

The current [upstream comparison](https://github.com/misantronic/RAOfflineProxy/compare/c7ebd1b6e777f3751ff0ecdf8aba54045844e00d...3958abcecd4762128cdb1d4c24cbf179ea4c0f44)
has four later commits: version bump, statistics label, muOS boot logging and
port fallback. `main.py` is unchanged. API release lookup still returns
`v2.1.0-alpha1` as the newest published release, although main's version string
is `2.2.0-alpha1`. These are different observations, not a newer released memory
fix. [upstream.json](upstream.json) retains the dated API comparison and searches.
The initial untyped GitHub search was rejected; successful separate issue and PR
queries are retained. No matching lazy-import PR was returned by that search;
this is not an exhaustive claim about all possible upstream reports.

Upstream [PR #209](https://github.com/misantronic/RAOfflineProxy/pull/209) is
already an ancestor of our pin (28 commits behind). Its streaming reads,
targeted achievement lookup and SQLite game-metadata index are present in the
actual packaged source. Reimplementing that large-library fix is not a new
candidate. The later free-port fallback changes `start_service_process`, not
`run_service_foreground`; our fixed-8080 consumers still need explicit review
before any future pin update.

## The one allocated host run

Can this be done on the VM? **Yes.** The coordinator recorded the distinction in
#570 and allocated one host source run before target testing: at most 60 seconds,
20 MiB scratch, no listener or provider traffic. This allocation is consumed.
Full service/VM/device work remains held.

[Original runner receipt](host-receipt.json), [all child results](host-result.json),
[versions and command](host-run.json), [derived comparison](analysis.json).
Runner and all ten children exited 0, in 1.79 seconds. All experiment scratch,
including the retained first preparation attempt, totaled 4,927,694 logical
bytes at completion. PIDs are from the tool's PID namespace. No dependency
installation, background test, service process or listener remains.

Python 3.14.4, SQLite 3.46.1, OpenSSL 3.5.5; standard library only.
`MALLOC_ARENA_MAX=2` matches the packaged unit. Image recipe currently names
Python 3.14.7; installed-runtime identification is still needed for the VM trial.

Packaging is explicit in [config/functions](../../../config/functions):
`python_compile` invokes the toolchain's `compileall.py -f -d` with the staged
installation prefix removed from the recorded filename, then removes `.py`
sources. The proxy recipe calls it on the installed module directory.
[0300-generate-legacy-pyc-bytecode.patch](../../../packages/lang/Python3/patches/0300-generate-legacy-pyc-bytecode.patch)
forces adjacent `file.pyc` output when a `cfile` is supplied and
`DONT_BUILD_LEGACY_PYC` is unset. The Python host-build hook sets that variable
for host modules and explicitly says not to set it for target compilation.

The diagnostic's explicit adjacent `.pyc` output and source removal match that
layout. With no `-O` and `PYTHONOPTIMIZE=0`, its default optimization level is
zero, matching the packaging command's unoptimized invocation. Its `dfile`
values are relative `raofflineproxy/...py` paths, whereas packaging records
installed `/usr/lib/python.../site-packages/raofflineproxy/...py` paths. These
affect code-object filenames/tracebacks; diagnostic bytecode is not claimed to
be byte-identical to the installed payload. Before target claims, identify the
**installed** interpreter version/build, executable hash, optimization flag and
SQLite/OpenSSL versions; a source recipe's version alone does not identify the
accepted image's runtime.

| Import-only sample (KiB PSS) | Baseline | Candidate |
| --- | ---: | ---: |
| First | 32653 | 27174 |
| Second | 32562 | 27127 |
| Third | 32569 | 27102 |
| Median | 32569 | 27127 |

Execution order: baseline, candidate, candidate, baseline, baseline, candidate.
The median difference is **5,442 KiB / 5.31 MiB**, with no optional UI modules in
the candidate. Pygame is absent in both: upstream already imports it inside
`run_menu_sdl`. This is Python source-import attribution with the common fixture
imports present. Python's parser/compiler allocation and retained allocator
pages can contribute. The image ships bytecode; neither this delta nor host
import time predicts target resident savings. There was no collection-pressure
trial, loaded proxy database during these samples, workload history, or browser.

Both variants also pass these real-code/synthetic-data checks:

- `run-service`, both menu commands and both image commands dispatch once with
  unchanged arguments, to mocked destinations; invalid UI arguments still fail.
- Real offline-award handling signs two awards, deduplicates a repeated award,
  refuses hardcore awards and preserves queue contents across SQLite close/open.
- Real next-game response construction returns the appropriate pending unlock,
  keeps the other game's data separate and exposes no unlock to another user.
- SQLite integrity checks pass; the independent preparation queue survives.
- Real flusher state transitions retain pending awards after mocked 401 and 503
  responses, then send two awards through mocked HTTP success and write the
  flush stamp. Credential lookup/live-achievement refresh/cache refresh and the
  flusher's sleep are mocks. This is not a real reconnect or provider test.

The guard is installed before importing proxy code. Synthetic audit events
prove rejection of connect, DNS and a production SQLite path without invoking
those operations. It denies **all** socket events, subprocesses and writes
outside the fresh synthetic state directory; proxy data paths are asserted.
The worker explicitly verifies the imported module path and the driver hashes
the prepared trees before execution. These are deliberate test substitutions,
not a runtime sandbox guarantee for arbitrary hostile code.

One preparation-only failure preceded the allocated run: the preparer rejected
a valid line offset in existing patch 002. It was corrected to retain offsets
in the report while still rejecting fuzzy application or failed hunks. Fresh
preparation passed. The host run itself had no failure or repeat.

## What the result permits

Keep this small candidate for target attribution and potential upstream review.
It does not justify suspending the proxy during browser use. The original
[lifecycle review](../2026-10-13-browser-stack/proxy-lifecycle.md) still applies:
startup/reconnect can upload awards, and emulators do not start the daemon on
demand. All that behavior remains intact here. No `SIGSTOP`, restart policy,
zram policy or preference change was selected.

The latest account-free Dropbox
[UA](../2026-10-13-dropbox-user-agents/README.md) and
[breakpoint](../2026-10-13-dropbox-breakpoints/README.md) evidence was read from
the coordinator's `m7-player-setup` checkout, read-only. Both still show pressure
without a proxy service. Reducing proxy overhead can add headroom; it cannot by
itself establish the browser incident's cause.

Source suggests the next attribution boundaries beyond CLI imports:

| Boundary | Why measure it before changing it |
| --- | --- |
| Import → first listener → first database use | Separates bytecode/modules, SQLite initialization and startup migration from retained workload. SQLite is available in the image; JSON fallback would retain a different data shape. |
| Before/after a synthetic cache batch and return to idle | Image pools retain worker threads and per-thread HTTPS connections intentionally. JSON parsing, TLS contexts and allocator high-water behavior need attribution; blindly discarding them could slow the next game/cache batch. |
| Controlled pending-award count | `flush_pending_awards` materializes the signed queue to validate chain ordering. Streaming it casually could change repair and partial-flush semantics. |
| Browser launch overlap with ES teardown | Existing handoff starts the browser before ES releases renderer/input/audio. Whole-system availability and request-ready latency matter more than one process's PSS. |

These are source-supported measurement points, not diagnoses or selected changes.
Data/source lifetimes must be measured with synthetic workloads before changing
cache limits, TLS reuse or pressure policy. Preserve sign-in validation and all
offline behavior.

## Next executable experiment and remaining blockers

The next owner is the coordinator. Source preparation can run on the host using
GNU patch and the verified archive, then the resulting small baseline/candidate
trees and their `source.json` can be staged with this packet into a disposable
guest after a fresh VM plan and exclusive allocation. Verify their file hashes
against the manifest after staging; the runtime fixtures also check those hashes.
Preparation inside the guest is an alternative only after checking that GNU
patch is installed (`patch --version` must identify GNU patch); do not assume the
guest has it or install a package under this assignment. That alternative also
needs the package recipe/patches and archive staged in the guest.
No accepted-cache copy or full build is needed. Use the guest's installed Python
and record its version, SQLite/OpenSSL, interpreter hash, source hashes, visible
RAM and `MALLOC_ARENA_MAX=2`. No owner config or real RA endpoint may be mounted.

1. Prepare the two trees with [fixtures/prepare.py](fixtures/prepare.py) and use
   [fixtures/bytecode.py](fixtures/bytecode.py) for the bytecode-only import
   comparison. This new fixture is **unrun, syntax checked only**. It compiles
   copies with the running target interpreter and imports adjacent `.pyc`
   files after removing only the copies' `.py` files. Compare before adding
   startup/database work. No saved host result may be reused as this outcome.
2. Allocate an unused loopback port and run
   [fixtures/readiness.py](fixtures/readiness.py) on each variant in sequence.
   This fixture is **unrun, syntax checked only**. It asserts real HTTP offline
   login status 200 with `Success: true` and the expected synthetic `User` and
   `Token`, cached patch and startsession readiness, queued-award integrity after
   listener close/reopen, and preservation of an upstream 401. External access
   is denied; provider behavior is mocked. It does not run the full service's
   workers, systemd, a browser, or ES and cannot close lifecycle acceptance.
3. If a useful target saving remains, compare the unchanged full service versus
   the candidate in a disposable account-free VM with a loopback fake RA server
   and egress blocked. Test startup and reconnect flush, cache/watcher work,
   interrupted SQLite transactions, controlled termination within the unit's
   15-second timeout, protocol readiness before next game, and normal ES browser
   launch/close/crash/return. Serialize ABBA trials with identical synthetic
   cache/award counts, steady-state PSS/anonymous/file pages, whole-system
   availability/PSI/refaults, and first protocol-response latency. Full-service
   fake-provider/ES orchestration is still to be prepared by the runtime owner.

Source preparation on the host, with fresh paths (first inspect `patch --version`
for GNU patch). The follow-up preparer is currently unrun:

```sh
patch --version
python3 fixtures/prepare.py --repo "$DISTRO_SOURCE" --archive "$VERIFIED_ARCHIVE" --output "$FRESH_TREES"
```

After staging and VM allocation, use the verified guest tree path below; all
values are placeholders, not resource reservations. Set `PYTHONOPTIMIZE=0` so
optimization cannot remove the fixtures' assertions. The bytecode fixture uses
the executing interpreter to compile both variants; do not stage host `.pyc`
files as the target comparison.

```sh
PYTHONOPTIMIZE=0 MALLOC_ARENA_MAX=2 timeout 60s python3 -B fixtures/bytecode.py --prepared "$GUEST_TREES" --output "$FRESH_BYTECODE_OUTPUT"
PYTHONOPTIMIZE=0 timeout 50s python3 -B fixtures/readiness.py --prepared "$GUEST_TREES" --variant baseline --state "$FRESH_BASELINE_STATE" --port "$ALLOCATED_PORT"
PYTHONOPTIMIZE=0 timeout 50s python3 -B fixtures/readiness.py --prepared "$GUEST_TREES" --variant candidate --state "$FRESH_CANDIDATE_STATE" --port "$ALLOCATED_PORT"
```

The held tests and target-bytecode attribution are the blockers to selecting the
patch, not blockers to delivering this scoped packet. No full lifecycle,
browser-usability, firmware build, upgrade or clean-install acceptance is claimed.
#570 remains unresolved. No integration, push or upstream submission was done.

Applicable sources read: supplied/root AGENTS, canonical-next checkpoint (historical
only), canonical rules, especially engineering-practices, packaging-and-patches,
vm-first, working-principles, time-to-play, least-surprise and handheld-evidence;
the whole #570 issue/comments, browser-stack lifecycle and browser-history
handoffs. Worktree rules matched `next`. Shared work log/register/checkpoint and
GitHub updates are left to the coordinator under the explicit worker boundary.
