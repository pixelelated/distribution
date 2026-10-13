# #574: retry retained failed GameCube RVZ hashes

**Separate source-only follow-up; all compiler/runtime controls UNRUN.**
ES commit `2d875d33de8d3796bf3b4401ce35f6ca1592cd55` directly follows the
immutable reader commit `4142943a407de75ad789039bf44359552262909d` on
`feature/m7-rvz-hashing-574`. The initial distribution packet is sealed at
`6325c1ba58a3ba6d63a95ef4a40c74970655e0e2`; none of its files or receipts
is changed by this additive `retry/` packet. The original packet's retained
zero-hash blocker describes that original commit, not this follow-up.

## Exact source seam and intent

The follow-up changes only:

- `es-app/src/GameCubeRvzHashRetry.h`: a pure eligibility predicate.
- `es-app/src/ThreadedHasher.cpp`: queue eligibility and the individual forced
  read, plus a wrapper checking the build capability and platform mapping.
- `external/libcheevos/cheevos.h/.cpp`: a build-capability query. The actual
  hash dispatch, decoder, and short-read guards remain unchanged.

Two gates require repair. `CheevosIndex::take(false, zeroHash, emptyId)`
returns Lookup. Even if a failed entry reaches the worker, the unchanged
`FileData::checkCheevosHash(false)` returns immediately for any nonempty
stored hash. The new predicate selects Hash in `ThreadedHasher::start`, then
`run` passes `mForce || retryGameCubeRvzHash(game)` to the existing FileData
method. No metadata is cleared merely to enqueue work. Existing hash/ID
recovery writes remain where they were.

Read history is retained as exact `git show` patches:

| Commit | Intent preserved |
| --- | --- |
| `878b22c43508923b9db673e5706d201098441135` | FileData's stored-hash short circuit and explicit force parameter date to the initial hashing integration. |
| `25820d0a7b7c2daf2c02e92cf53d759bd417fc03` | Hash failures began returning the all-zero sentinel while the queue began skipping stored hashes. Intent inferred from the same diff: avoid repeated failed reads; the commit message does not state a format-specific retry policy. |
| `f80083a1968c23b93a627b56455dc6978f6a1475` | A valid hash without an ID receives a library lookup without reading the ROM; IDs are persisted after lookup. |
| `29b5d6fdc0829451e48a6d7da8300056de89dfa8` | Silent lookup-only passes are limited to once per day. Runs with hash work use the existing hash-work path. |
| `cce9ab12ab535d2d0716a78deb26d11c363204e8` | Startup/link-up indexing and missing-library behavior. |
| `636065877c4c56d0051d32d26060875eeb05f636` | One index attempt per game list reload; a second start caused duplicate offline waits. No second start is added here. |
| `cc8c5ccb4942695c395ac455a93929f69cc0e1d8` | Missing hash library empties the queue and counts zero work before worker creation. This constructor path remains byte-identical. |

No GuiMenu, Settings, FileData, SystemData, ViewController, CheevosIndex,
catalog, token, sign-in, or offline-award code is edited. No dependency or
license change is added by the MIT retry helper.

## Eligibility and limits

The additional retry requires all of these: the RVZ reader was compiled in;
the system has exactly one platform ID and it is GameCube; the extension is
`.rvz` ignoring ASCII case; the trimmed ID is empty or the existing `0`
no-ID marker; and the trimmed hash is missing, not 32 hexadecimal characters,
or the all-zero failure sentinel.

A valid nonzero hash with no ID stays a lookup. A positive ID or an unfamiliar
nonempty ID value prevents the additional retry, even beside a bad hash.
For example, `opaque`, `-1`, and noncanonical `000` IDs are preserved. The
predicate examines trimmed strings without rewriting them. The existing
forced-all and missing-hash behavior still applies independently; this is
not a change to their historical policy. Other consoles/formats and ambiguous
mixed-platform systems gain no new eligibility. No owner metadata is loaded
or normalized by this source task.

The reader still supports only the initial packet's bounded GameCube RVZ
NONE/Zstandard subset. Eligibility does not inspect compression metadata or
promise a successful hash: BZIP2/LZMA/LZMA2, Wii, oversized chunks, invalid
containers, and other rejected inputs can still fail. A remaining failed
entry may be attempted once on each later eligible index run; there is no
inner retry loop or extra index start. CPU/time cost of repeated rejected
entries is unmeasured.

**Existing flow boundary:** ordinary Update Gamelists calls
`GuiMenu::updateGameLists` → `ViewController::reloadAllGames` →
`SystemData::loadConfig(window)` → `startIndexesAtStart` →
`ThreadedHasher::start(..., false, true)`. `CheevosCheckIndexesAtStart` must
be enabled, the system must pass the existing visibility/support gates, and
the hash library must be available for the worker to run. The source default
of that preference is false; this packet makes no claim about the installed
image's setting. An unconditional retry with the preference off would need
the SystemData/ViewController start seam outside this assignment. That seam
was reported before proceeding; no setting or menu change is proposed here.

## Static evidence and UNRUN controls

`source-review.json` binds the reader/retry files, immutable predecessors,
and relevant unchanged source. Static comparison shows that ThreadedHasher
outside the helper/includes and two retry sites is byte-identical, including
the library fetch/offline path, lookup cadence, ID persistence, and offline
top-up. The wrapper outside its new capability query is byte-identical.
Whitespace checks passed; prepared Python was AST-parsed without importing
or executing it. These checks do not prove C++ compilation, queue behavior,
file reads, UI behavior, or preservation on a running image.

Can this be done on the VM? **Yes.** The prepared controls need only synthetic
metadata and the initial packet's self-created non-bootable ISO/RVZ data.
Coordinator owns allocation and the written plan. No compiler, fixture,
decoder, runtime, test suite, VM, account, or award operation ran here.

After allocation, the smallest additional executable control is:

```sh
cmake -S docs/qa-logs/2026-10-13-rvz-source/retry -B "$PIX574_RETRY_BUILD" \
  -DCMAKE_TOOLCHAIN_FILE="$PIX574_TOOLCHAIN" -DES_SOURCE="$PIX574_ES"
cmake --build "$PIX574_RETRY_BUILD" --target pix574-retry-control --parallel 1
# In the allocated guest, under the coordinator's bounded runner:
"$PIX574_RETRY_BINARY"
```

Expected: 27 named PASS lines, no stderr, rc 0. The control compiles the real
new predicate, unchanged CheevosIndex, and its StringUtil dependency. It
compares original queue policy with additional eligibility. It does not mock
FileData or claim to execute ThreadedHasher. Source and binary hashes/build
provenance must accompany the result.

`run-hash-controls.py` is an independently bound copy of the original runner
for the follow-up source. It consumes the initial generator's manifest and
does not generate data. After building the initial harness against this
follow-up, run it on the already allocated synthetic fixture directory:

```sh
python3 run-hash-controls.py --binary "$PIX574_BINARY" \
  --es-source "$PIX574_ES" --fixtures "$PIX574_CASES"
```

Its `--baseline` still means the original composed `a7dcdbb38009d8d2a81c7c2b4bc1d8c2d0d38a20`
reader baseline, where RVZ is expected to fail. Do not present this as a retry
baseline run. The original packet and its runner remain bound to the initial
reader source. Both runners record binary identity; neither can prove the
build-to-binary connection without coordinator build receipts.

| Criterion | Prepared evidence/control | Runtime still owed |
| --- | --- | --- |
| Retained zero/invalid hash and absent ID becomes hash work | Real predicate + old policy, controls for zero/short/nonhex/missing/whitespace hash, no ID and `0`, case-insensitive extension | Installed Update Gamelists on synthetic retained state must log the actual hash read, save the correct nonzero hash, and resolve only a matching synthetic library entry. |
| FileData's cached-hash guard is bypassed only for repair | Source-bound per-entry force at the worker call | Instrumented read count and recovery file; exactly one hash attempt per entry/run. |
| Legitimate entries/other formats preserved | Controls for valid unknown/indexed hash, positive/opaque IDs, ISO/CHD/archive/other console/mixed mapping/reader disabled/force-all | Compare synthetic metadata before/after and record zero new ROM reads for valid lookup/indexed controls. |
| Offline and settings behavior retained | Byte-identical library/offline/cadence/start flow; no new start or setting | Missing library must cause no hash read or metadata write; disabled indexing must start nothing; offline pending awards/cache remain unchanged. |
| Correct reader + retry combination | Follow-up-bound raw/RVZ/invalid/truncated runner, UNRUN | Compile/link, equivalence, rejected modes, sanitizer/repeated-handle, GC/Wii ISO and CHD regressions; no in-game Dolphin claim. |

Coordinator owns canonical flow references and reviewed exact-source frames.
No new player-facing strings or translation changes are proposed. The initial
packet's other unresolved compiler/VM/format/memory limitations still apply.
