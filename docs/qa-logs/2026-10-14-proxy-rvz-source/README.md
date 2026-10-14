# #583 — RVZ offline-proxy source packet, 2026-10-14

**Adaptation is warranted, but RVZ support is already present.** The packaged
proxy has its own RVZ reader. Three distinct source findings must not be collapsed
into the ES decoder failure in #574:

1. The proxy's padding generator loses the remaining bytes of a word when a
   generated run starts at an offset not divisible by four. A minimal independent
   upstream candidate is prepared here.
2. The distribution's scan treats ES's all-zero failure hash as evidence that a
   system was indexed, then suppresses the independent proxy hashing route for
   that folder. A narrowly scoped, deliberate-scan recovery candidate is prepared.
3. Dolphin's launch script does not consume the distribution's offline-proxy
   toggle. It writes the configured custom host, which is empty by default.
   Enabling the packaged service alone does not establish Dolphin offline use.
   A specific repair boundary and tests are proposed below; no routing change is
   included in these candidates.

Evidence level: **source inspection and static checks only**. All newly prepared
controls are **UNRUN**. No proxy/fixture/native library was imported or executed;
no compiler, browser, service, VM, account, provider, owner ROM, or award action
was used. Public GitHub reads are recorded in [research/receipts.json](research/receipts.json).
No existing Steam packet, product file, package pin, shared record, or issue was
edited. The coordinator owns allocation, #583/#574 updates, and integration.

## Exact source and upstream comparison

[bindings.json](bindings.json) records full hashes and origins:

- Distribution checkout `a824edbd209d1971b2c814cf86528bae0add9c51`;
  inspected `next` = `0ea6eaf74ad47503c05955d1c0bd4bd00bdfb816`.
  The proxy recipe, both scan helpers, service unit, rcheevos recipe, and Dolphin
  achievements script agree with that `next` byte for byte.
- RAOfflineProxy `c7ebd1b6e777f3751ff0ecdf8aba54045844e00d`, archive SHA256
  `88eef31acfa4104b20258bd5cea514ade30e6cdf35767ffc958009851d61898b`.
  Read-only prepared source: `/workspace/tmp/pix541-refresh72/final-patched`.
  All 15 inspected module identities match the prior sealed baseline source manifest;
  all 16 local patch identities are retained. No accepted cache was changed/copied.
- rcheevos `1433173220a7eaede6a9ed7a18e94117be1821e0`; its exact verified source
  archive supplied only the retained `hash_disc.c` inspection copy.
- ES diagnostic baseline `c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`;
  Dolphin 2606, `6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4`.
  This is not a statement that later ES fixes are absent from the coordinator's
  composed candidate; #574 owns that composition and its runtime receipts.
- Current proxy main on October 14:
  `2d19684e0800f6da33ff1841d27e083c1e467142`; latest release
  [v2.2.0-alpha1](https://github.com/misantronic/RAOfflineProxy/releases/tag/v2.2.0-alpha1).
  The [five-commit comparison](https://github.com/misantronic/RAOfflineProxy/compare/c7ebd1b6e777f3751ff0ecdf8aba54045844e00d...2d19684e0800f6da33ff1841d27e083c1e467142)
  changes version/docs/platform/service-port behavior, not the decoder or hash
  bridge. The fetched current decoder is byte-identical to this pin's decoder.
- [Upstream #51](https://github.com/misantronic/RAOfflineProxy/issues/51) was closed
  by `aa70bbaf54c7ffa31c42b5c3b2af416c823d3af9`, the July 18 Linux RVZ port, already
  included. Do not import it again as a fix. RVZ issue/PR and GameCube issue searches
  include closed reports; #8 is an Android crash report, #5 early caching coverage,
  #89 HTTP403 lookup failure. None proves this incident. Searches for padding
  issues and PRs returned zero at this read; this is a scoped search, not a claim
  that no duplicate can exist. The first exploratory RVZ query lacked an issue/PR
  qualifier and returned HTTP422; corrected qualified queries are retained.

Local patches 001/003/005/007–013/015/016/018/019 concern response handling,
flush stamps, refresh survival, sign-in, consent, images, network bounds, or
platform identity. 002 filters the synthetic warning achievement; 004 removes
an old game-count limit. None changes RVZ extension selection, parsing, or the
native datasource entry point. The package compiles that glue entry point and
installs the entire Python module directory. The two scan helpers are separate
fork source, not one of these upstream patches.

## Exact discovery → hash → cache paths

| Boundary | Source and behavior |
| --- | --- |
| Extension/discovery | `rom_hashing.supported_rom_extensions()` includes `.rvz`; `rom_browser.is_supported_browser_file()` lowercases suffixes. `raofflineproxy-ctl` includes `gamecube wii` in `SCAN_SYSTEMS`. This is not an extension omission. |
| ES handoff | `ctl:list_jobs/read_index` reads gamelist plus only matching-parent recovery files. A nonempty hash in any row puts the whole folder in `indexed_dirs`. Only positive IDs with a nonempty hash become `I` jobs; those reuse ES's hash through `cache_indexed()`, without opening or hashing ROM contents or asking `gameid`. |
| Failure suppression | ES baseline `RetroAchievements.cpp:935–950` returns 32 zeroes when hashing fails. That string satisfies the folder index test. The subsequent independent walk skips the folder; zero/no-ID RVZ entries produce no job. A zero hash with an erroneous positive ID can even produce an `I` job. A failure sentinel is not a successfully computed hash without an RA match. |
| Independent path | In unindexed allowed folders, a deliberate scan produces `H` jobs. `add_rom_to_cache()` → `hash_candidates_for_manual_cache()` → `hash_rom_candidates()` → `_generate_candidates()` selects `_generate_rvz_candidates()` on `.rvz`. Smart Cache and configured folder watching have independent discovery routes; they do not make the explicit scanner's omission disappear. |
| Decoder/native bridge | `FileReadSource` reads the container; `RvzDataSource` supplies random-access decompressed bytes to ctypes callbacks. `raproxy_hash_disc_datasource` installs a datasource file reader and tries `RC_CONSOLE_GAMECUBE` and `RC_CONSOLE_WII`. This is distinct from ES's baseline custom **CD** reader. The GameCube hasher checks the raw magic at 0x1c and hashes the partition header/apploader and DOL segments. |
| Lookup/cache | Independent candidates go to hash-keyed `gameid`; a successful ID leads to `cache_game`: account-specific patch, softcore unlocks, hash/account achievementsets, and session rows, plus source path/aliases. A confirmed lookup miss is cached for seven days; an empty hash-candidate list returns a hash failure before enqueue/lookup. Thus adding `.rvz` to an allowlist would not repair these other boundaries. |
| Offline consumption | The proxy serves cached login/game/set/session responses and queues casual awards through its existing authentication and signing paths. Request/cache keys depend on hash, game and account, not the filename extension. A correct hash and an `I` job do not prove complete preparation, login acceptance, successful emulator routing, or offline award/reconnect behavior. |

`es_export.py` exports cached game IDs from database metadata to
`cached_game_ids.txt`; it does not repair gamelist hashes or invoke ES indexing.
A ready count or exported ID is not itself proof of hash/account completeness.

The recipe's native bridge does not itself decode RVZ. GameCube zstd decoding
also needs `libzstd.so.1`; Wii reconstruction uses `libcrypto.so.3`. Python binds
these lazily. The proxy recipe has no direct dependency on zstd/OpenSSL; other
image dependencies may supply them. Verify installed ELF/library identity and
availability before claiming target hashing, even though upstream #51 reported
them on its own ROCKNIX device. No new package dependency/pin is selected here.

RVZ parsing currently supports NONE and Zstandard (compression 0/5), not every
valid Dolphin compression choice (BZIP2/LZMA/LZMA2), and not WIA. Smart Cache's
Dolphin discovery list also names WIA/GCM; discovery is not decoder support.
The owner's compression/member details were not inspected. No conversion of
owner games is proposed. Additional codec coverage would belong in
RAOfflineProxy as a separately qualified feature with per-codec ISO-equivalence
and bounded-malformed-input tests; it is not selected as this incident's fix. Missing-library and unsupported-format errors require
separate accurate failure feedback; `RvzDataSource.open` currently collapses
parse exceptions to `None`. Native callback exceptions/truncation and overlapping
native hasher calls need the separate malformed/concurrency VM gate below.

## Candidate A: byte-accurate padding, upstream RAOfflineProxy

[candidates/rvz_datasource.py](candidates/rvz_datasource.py) changes only
`_generate_rvz_bytes`. It skips complete words, retains the zero-to-three leading
bytes needed from the partial word, writes the requested bytes, and slices away
that prefix. It does not change codecs, formats, credentials, cache schemas,
queueing, or award handling. The additional output allocation is at most three
bytes. Existing aligned behavior should be identical; runtime proof is UNRUN.

The original helper's writer increments its word index after any partial word.
Calling it to discard one byte therefore resumes at byte four. The
[official RVZ format](https://github.com/dolphin-emu/dolphin/blob/2606/docs/WiaAndRvz.md#prng-algorithm)
requires advancing by the precise byte offset modulo 32KiB. Pinned Dolphin's
`LaggedFibonacciGenerator::Forward(size_t)` and `GetBytes` retain byte position.
The format permits literal lengths that put the next generated record at an
unaligned offset. Its unusual output shift of **18** is intentional and retained.

This is a decoder correctness finding, **not yet the cause of an observed RA hash
mismatch**: normal padding may fall outside rcheevos' hashed ranges. The prepared
container proves the reading seam only when run; a native hashing fixture must
place controlled bytes in actual hashed ranges and compare ISO/RVZ identities.

Upstream destination: **misantronic/RAOfflineProxy**, GPL-3.0-only Linux decoder;
minimal independent patch plus seed/offset and packed-record controls. Exact
current-main bytes match, so the same candidate applies there. Before submission,
retain failing baseline/passing candidate receipts and independently compare with
Dolphin's actual reader. No claim of a Dolphin defect; no submission was made.

## Candidate B: recover failed RVZ indexing in a deliberate scan

[candidates/raofflineproxy-ctl](candidates/raofflineproxy-ctl) admits **only** RVZ
entries with the exact 32-zero sentinel to the existing `H` walk for `mode=all`.
It never forwards a zero RVZ sentinel as an indexed ID/hash pair. Nonzero hashes
with no set, newly added unindexed games inside an indexed folder, and automatic
`mode=indexed` top-ups keep their current policy. Cache completeness/account
checks, directory exclusions, existing scan-root allowlist, history order, cap,
cursor, and request pacing remain in effect. Custom folders outside that existing
walk are still ES's responsibility; this is not a broadened filesystem scan.

This exception is a proposal for review against **D-RA-013**, whose original
intent is explicit in `8c03cbb6e77cb2514e74672dc477a8f8da1057cc`: avoid repeated
hashing/lookups for known unmatched games and follow ES's index. Do not simply
remove `indexed_dirs`, treat all missing IDs as hash failures, or change automatic
top-up into a full rehash. If the accepted ES repair always reindexes old failure
sentinels successfully, this recovery candidate may be unnecessary for that flow;
its separate value is allowing the player's deliberate scan to use the already
present independent reader after an ES read failure.

Contribution disposition: **fork-specific distribution integration** at present.
Current ROCKNIX's queried proxy package path returned404 (retained); do not submit
this helper diff to RAOfflineProxy as though it were upstream source. Offer the
policy with an eventual ROCKNIX offline-proxy integration, or retain it locally
with this reason. ES's own RVZ fix remains a separate ROCKNIX/EmulationStation
contribution owned by #574. The MD5 alignment candidate belongs to
**libretro/libretro-common `utils/md5.c`**, per the coordinator's corrected source
attribution, and is not part of this packet.

## Dolphin routing disposition — necessary separate integration work

The current launch script writes `HostUrl` from
`global.retroachievements.customhost` at every GameCube/Wii launch. The package
unit uses `main run-service`; that branch runs the server and bypasses
`_patch_emulator_configs`. The offline toggle changes its own setting and
hardcore, not customhost. Therefore a default empty customhost does not route
Dolphin to this packaged proxy. The script and upstream comparison are retained.
[ROCKNIX PR3038](https://github.com/ROCKNIX/distribution/pull/3038) already supplies
custom-host support and is included; [proxy PR50](https://github.com/misantronic/RAOfflineProxy/pull/50)
documents its Dolphin integration. Neither proves this fork's toggle is wired.

Smallest recommended repair: in `cheevos_dolphin.sh`, choose the loopback host at
launch only when the offline toggle is exactly1, raw hardcore is exactly0, and
the same read-only listener predicate used by PPSSPP succeeds. Preserve the
configured custom host for toggle-off/hardcore/unknown/unavailable cases; retain
separate no-listener/unreadable-table diagnostics. Never modify saved customhost,
credentials, or global hardcore in the launcher. This preserves the upstream
custom-host contract and the fork's existing raw-value security gate. Do not
invoke upstream config patchers or restart the service as a workaround.

No routing source patch is bundled: it needs synthetic full-script configuration
controls (toggle0/1, hardcore0/1/empty, customhost empty/nonempty, IPv4/mapped IPv6/
IPv6-only/unreadable tables, missing token, disabled RA) before composition. That
is a narrowly defined follow-up, not a request to launch owner games. Upstream
destination is the **distribution integration**, not Dolphin's decoder. A direct
ROCKNIX contribution depends on an equivalent toggle/service contract; the custom
host feature itself is already merged. Preserve #581's separately owned save-path
work when composing.

## Prepared first VM experiment — UNRUN

Can this be done on the VM? **Yes.** The first command needs only stock Python3
and coreutils timeout in a disposable no-NIC guest; no installed proxy, native
library, ROM, compiler, account, or listener is needed. The coordinator records
allocation in #583 before execution. Stage this verified packet unchanged, verify
`SHA256SUMS`, then from its directory run once:

```sh
timeout --signal=TERM --kill-after=5s 45s python3 -I -S -B fixtures/probe.py --output /run/pix583-source01
```

Retain the original command exit/stdout/stderr, `result.json`, and changed packet
identities if rejected. Do not pass by retrying; a fixture error is its own receipt.
The driver refuses changed input hashes and an existing output directory. It sets
512MiB address-space,30CPU-second,2MiB single-file and40-second alarm limits;
expected synthetic scratch is below16MiB, checked at completion.16MiB is an
assertion, not a kernel aggregate quota; use a coordinator-owned finite guest
scratch allocation (32MiB sufficient) if a hard aggregate bound is required.
No children are created by the driver; outer timeout bounds failure/cleanup.

The driver denies socket creation/native loading/process creation and out-of-scope
file access, then checks three denial controls before executing prepared source.
It preloads only stdlib modules. It runs the complete sealed Python `list_jobs`
heredocs, **not the ctl shell**. Imports for config/history/Storage are explicit
synthetic adapters; the SQLite cache is disposable and includes a pending-award
sentinel checked byte-for-byte. `/usr/bin` supplemental config enumeration is
refused by the guard and follows the source's OSError skip. Real user config and
credentials are never loaded. The walker cap is injected as2 to exercise cursor
behavior cheaply; production is5000. This is source-path coverage, not full scan
caller, SQLite queue, authentication, or award qualification.

Prepared checks: aligned/unaligned padding across word/buffer/sector boundaries,
actual NONE RVZ packed-record reading, truncated/bad-magic/bad-header/unsupported
container controls, old all-zero-folder omission, mixed/indexed/automatic/fresh
cases, stale/current recovery metadata, cached/partial/different-account rows,
empty-file exclusion, and cursor continuation. Baseline padding mismatch is an
expected reproduction recorded separately; the candidate must match the independent
spec-derived byte oracle. Native codec calls are explicitly refused. No synthetic
file is described as a recognized RA title.

Subsequent serialized allocation, after that receipt: reuse #574's independently
validated nonbootable ISO/RVZ corpus and its known content hashes, stage the exact
installed `libraproxy_rchash` and Python/codec identities, and compare direct proxy
hashes to ISO/ES for NONE and Zstandard, packed unaligned groups, and malformed
header/table/group inputs. Require deterministic no-candidate/no-lookup on failures,
bounded RSS/CPU, balanced descriptors, and serialized hashing first. The native
bridge's global pending-datasource pointer and Python callback exception boundary
warrant explicit overlap/truncation controls before concurrent safety is claimed.
No native hasher was built or loaded in this assignment.

Then exercise actual I/H helper calls using only synthetic SQLite and a private
fake RA transport: valid match/cache hit, supported-but-unmatched, codec failure,
HTTP401/403/429, patch/unlocks/sets failures, second account, duplicate award,
offline login account/token checks, pending queue preservation, and reconnect to
**only** the synthetic endpoint. Verify no codec failure becomes a cached GameID0
and no partial data is labeled ready. These integration controls are a plan, not
implemented by `probe.py`. Full Dolphin gameplay, real RA sets/sign-in/award
acceptance, ARM64 native execution, and installed-image startup remain unqualified.
Do not restart the owner's proxy: startup can flush queued awards.

## Acceptance mapping and immutable packet use

#583 criterion1 (exact source/path/upstream): supplied here with bound bytes.
Criterion2 (repair or no-op with synthetic VM regression): candidates and first
fixture prepared; **UNRUN, checkbox remains open**. Criterion3 (combined #574
qualification): handoff above, coordinator-owned and incomplete. Criterion4
(canonical contribution rule): coordinator-owned D-WORKFLOW-164, not edited or
verified here. Criterion5 (independent upstream disposition): recorded per finding;
no issue/PR submission, broad package bump, or native acceptance claim.

Compressed candidate patches retain exact unified-diff bytes; their uncompressed
SHA256 values and source/candidate identities are in `bindings.json`. Decompress
in memory and feed patch stdin only in a separate source preparation tree after
checking those hashes; do not apply into this historical packet. Complete proposed
files are provided for review. The first fixture requires no patch utility.

Static validation: `python3 -I -S -B static-check.py` completed with original
exit0 on host Python3.14.4; [static-result.json](static-result.json) records AST,
source identity, exact patch regeneration, and whitespace results. This command
never imports a fixture or proxy module. Existing trailing whitespace in the
retained Dolphin format document and rcheevos source is preserved as `.gz` with
uncompressed `.sha256` companions. `SHA256SUMS` seals the whole packet.
