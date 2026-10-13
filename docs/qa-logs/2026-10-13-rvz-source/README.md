# #574: bounded GameCube RVZ frontend hash candidate

**Source-only candidate; not compiled or executed.** No fixture was generated
or run. No owner ROM, account, gameplay, VM, service, or installed application
was accessed. This does not close #574 or establish Dolphin in-game behavior.

ES commit: `4142943a407de75ad789039bf44359552262909d`, branch
`feature/m7-rvz-hashing-574`, isolated worktree
`/home/max/Development/emulationstation-next.worktrees/m7-rvz-hashing-574`.
Its exact parent is the coordinator's composition
`a7dcdbb38009d8d2a81c7c2b4bc1d8c2d0d38a20`. The coordinator checkout and prior
Wi-Fi/GTK4 packets are untouched. The distribution companion changes only
the ES build dependency/license installation and this evidence directory;
`PKG_VERSION` remains `c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`.

## Finding and implementation

The complete live [issue #574](https://github.com/pixelelated/distribution/issues/574)
and its one comment were read and retained, alongside the required cached
issue read. The observed nine RVZ hash failures/zero sentinels are existing
coordinator evidence, not new worker measurements. Accepted/composed ES maps
GameCube to console 16, but registers only a custom CD reader. Its GameCube
hasher opens a plain file and tests the uncompressed magic at `0x1c`.
An RVZ container is not a raw GameCube disc at that offset. This source match
explains frontend failure without implying an in-game Dolphin failure.

The candidate adds `rvz_hash.cpp/.h` and a GameCube `.rvz` dispatch in
`external/libcheevos/cheevos.cpp`. Case-insensitive extension matching is
limited to GameCube. A new iterator gets its own file callbacks; no global
file-reader callback is installed. Existing CHD/CD and other console routes
retain their original bodies. The decoder uses the existing read-only
libretro-common file stream, validates metadata, reconstructs just the chunks
requested by the existing hash algorithm, and keeps one decompressed chunk.
It creates no ISO, temporary file, subprocess, network request, or account state.

The GameCube/shared Nintendo partition hashing code had unchecked short reads
in the composed source and in the fresh upstream source. A failed decoder
could therefore still feed incomplete data to MD5. The candidate checks magic,
apploader, header, DOL table, and section reads before hashing them. It also
uses unsigned/wide header-size arithmetic and leaves file closure to the
caller on allocation failure, avoiding the old double-close path. Correct
input uses the same byte ranges and MD5 order. The shared helper also serves
Wii ISO hashing, so that unaffected-success path needs regression proof;
this change does not add Wii RVZ support.

| Supported candidate input | Explicit rejection boundary |
| --- | --- |
| GameCube RVZ versions 0.3 through 1.0 | WIA, Wii, incompatible/newer versions |
| NONE and Zstandard compression, including uncompressed individual groups | BZIP2, LZMA, LZMA2, PURGE; no fallback to hashing compressed bytes |
| Lossless RVZ packed literals and seeded padding; zero groups | Invalid packed ranges, truncated seeds/data, more than 4096 packed records per chunk |
| 32 KiB through 2 MiB power-of-two chunks | Larger/nonconforming chunks |
| Contiguous raw mappings; offset alignment and header override | Gaps, overlaps, invalid group references/ranges |
| SHA-1 checks for both container headers | Wrong header digests or inconsistent physical size |
| Up to 2 GiB virtual disc, 4 GiB container, 4096 raw entries, 65536 groups | Larger inputs/counts before allocation |
| 3 MiB maximum encoded/intermediate allocation request | Oversized table/group output or compressed input |
| 128 MiB cumulative hash reads, 512 MiB decoded work per reader | Work beyond those limits fails |

Those are source rejection bounds, not measured RSS or wall-clock limits.
The reader performs synchronous local I/O like the old hasher; it adds no
hard deadline for a blocked filesystem. Zstandard/allocator overhead, CPU,
cache behavior, and total ES worker concurrency still need measurement.
This is a hash reader, not full-disc integrity verification. Compression modes
and chunk sizes of the reported owner files were not inspected in this task.

## Fresh upstream and license research

Read-only official HTTP inputs are retained in `upstream/` and hash-bound in
`SHA256SUMS`; no downloaded code was run. Findings are dated 2026-10-13.

- [RetroArch #18316](https://github.com/libretro/RetroArch/issues/18316) reports
  frontend ISO/RVZ mismatch. Its comments point to
  [PR #18319](https://github.com/libretro/RetroArch/pull/18319), merged as
  `fcf0cc748354147760abdb3be96d6efbb1b756f6` on 2025-10-21; the reporter
  confirmed the nightly fix and closed the issue on October 23. The latest
  release API returns v1.22.2, published 2025-11-20. That tag's
  [change log](https://github.com/libretro/RetroArch/blob/v1.22.2/CHANGES.md)
  lists RVZ hashing under its 1.22.1 heading. This is release/history evidence,
  not a test of ES or proof of every RVZ mode.
- Fresh RetroArch head is `34d62da0f4abdd1ed0604c80c16fd1f47ee5f40b`.
  [cheevos_rvz.c](https://github.com/libretro/RetroArch/blob/34d62da0f4abdd1ed0604c80c16fd1f47ee5f40b/cheevos/cheevos_rvz.c)
  is 126957 bytes and GPL-3.0-or-later. It includes Wii reconstruction,
  RetroArch-local logging/headers, and the newer `HAVE_RZSTD` decoder. Its
  compression switch does not support every named compression constant.
  File history includes later Wii heap-corruption and big-endian-padding
  fixes, and the replacement of reference Zstandard by rzstd. Copying the
  initial PR or current file wholesale is not a small MIT-compatible import.
  No RetroArch implementation enters the ES candidate.
- Fresh [rcheevos](https://github.com/RetroAchievements/rcheevos/tree/1433173220a7eaede6a9ed7a18e94117be1821e0)
  is `1433173220a7eaede6a9ed7a18e94117be1821e0`; the latest release API gives
  v12.5.0, published 2026-09-14. Composed ES contains 12.2.1. The current
  GameCube path still uses file callbacks and raw-disc magic; merely upgrading
  rcheevos does not provide an RVZ decoder. Its MIT license and existing
  iterator API allow this scoped adapter without a library-wide upgrade.
- Dolphin's [format specification](https://github.com/dolphin-emu/dolphin/blob/8d2ad1a662472955497e5bb79d7b9ec6999e1f0d/docs/WiaAndRvz.md)
  and version constants were read at fresh head
  `8d2ad1a662472955497e5bb79d7b9ec6999e1f0d`. Container code here is original;
  the padding implementation is an attributed adaptation of
  [bodgit/rvz](https://github.com/bodgit/rvz/blob/bc439051cbedab7fe22a0c73bd2e7f19a310645e/internal/padding/reader.go)
  at `bc439051cbedab7fe22a0c73bd2e7f19a310645e`, licensed BSD-3-Clause.
  Its license is retained in ES as `LICENSE.rvz-padding`, with provenance in
  `RVZ-NOTICES.md`. Only a redundant final blank line differs from that
  license snapshot. A Go runtime is not imported.
- [nod](https://github.com/encounter/nod/tree/ebd80cac99b48a323200d84365e07a58cc27412d)
  has an MIT/Apache-2.0 C FFI, but its inspected 2.0.0-alpha.12 workspace
  requires Rust 1.85/edition 2024 and a larger crate/codec dependency graph.
  The default vendor filter lists aarch64/x86_64, while this distribution
  also serves arm. No Rust/Cargo dependency is introduced for this candidate.
- Exact pinned Dolphin `6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4` already
  implements `verify -a rchash`, but the distribution disables its CLI tool.
  The command initializes a Dolphin user directory/UICommon and runs a volume
  verifier before calculating the hash. It is not a cheap read-only frontend
  shortcut to enable blindly. Its GPL implementation is not linked into ES.
  No owner image was converted to work around the missing reader.

The new adapter is MIT with a BSD-3-Clause padding adaptation. Existing
libretro-common stream and rcheevos licenses remain intact. Boost SHA-1 is
header-only BSL-1.0; exact 1.91.0 header/API and license family were checked.
Zstandard 1.5.7 is used under its BSD-3-Clause option. This is file/dependency
license accounting, not a general relicensing of the frontend or its other
bundled libraries.

## Build impact

`ENABLE_RVZ_HASH` defaults on for ROCKNIX and off otherwise. When requested,
CMake requires target Zstandard and Boost headers/library; it fails rather
than silently disabling the reader. Other builds may opt in. The ES package
already depends on Boost; the companion recipe adds the direct `zstd`
dependency, declares MIT AND BSD-3-Clause, and installs the two reader notices
under `/usr/share/licenses/emulationstation` when the pinned source contains
them. No version/pin changes. Recipe bytes matched `next` and the coordinator
before this edit (baseline SHA in `source-review.json`).

The distribution already has zstd 1.5.7, Boost 1.91.0, bzip2 1.0.8, and xz
recipes; the candidate needs no new package recipe, bundled codec, Rust/Go
toolchain, or bzip2/LZMA linkage. libcheevos gains one C++ translation unit and
a transitive libzstd link. Final binary size, whether a particular image
already contains libzstd, installed license-file bytes, and target ABI/link
success are unmeasured. No cache copy or dependency build occurred.

## UNRUN fixtures and next executable experiment

Can this be done on the VM? **Yes.** Self-created data and local hash results
need no owner ROM, radio, provider account, gameplay, or award submission.
Coordinator owns the written VM-first plan, compiler/runtime allocation, and
any admission required by #493. The commands below are prepared, not run.

`make-fixtures.py` writes a small non-bootable raw GameCube image and equivalent
NONE, packed-NONE, packed-Zstandard, mixed stored/Zstandard-group, and
uppercase-extension RVZ files. The
contents are generated here, with a byte-range MD5 oracle independent of the
new C++ reader. They cover a DOL read across a chunk boundary, a second raw
region, non-sector-aligned seeded padding, and a DOL section in a zero-data
group. Output is
bounded to 32 MiB and requires a new directory. It uses only Python stdlib and
the existing target libzstd for fixture compression.

Negative controls include truncated raw/header/DOL/section/container data,
bad header digests, unsupported compression/Wii/chunk size, oversized counts
or disc size, out-of-file groups, invalid group indices, packed overflow,
corrupt Zstandard, and an executable section beyond the virtual disc.
The ordinary NES control checks a non-disc hash path. All are UNRUN; even the
synthetic files and their future hashes do not exist yet.

`hash-control.cpp` calls the actual `generateHashFromFile` wrapper, returns
0 plus a hash on success, or 2 plus `FAIL` on rejection. It also accepts
multiple console/path pairs for a same-process RVZ → ISO → NES → RVZ control.
`run-controls.py` checks source/file hashes, records executable identity,
enforces a ten-second process-group deadline per control, and compares exact
stdout/return codes. The coordinator must additionally retain the actual
build-to-binary binding and supervise the outer runner; the script's source
check alone cannot establish what a binary contains.

After coordinator allocation, prepare the harness with the approved target
toolchain and a new private build directory (`PIX574_TOOLCHAIN`, `PIX574_BUILD`,
and `PIX574_ES` must name those allocated inputs):

```sh
cmake -S docs/qa-logs/2026-10-13-rvz-source -B "$PIX574_BUILD" \
  -DCMAKE_TOOLCHAIN_FILE="$PIX574_TOOLCHAIN" \
  -DES_SOURCE="$PIX574_ES" -DENABLE_RVZ_HASH=ON
cmake --build "$PIX574_BUILD" --target pix574-hash-control --parallel 1
```

Stage the harness, fixture scripts, and adjacent `source-review.json` into the
allocated guest directory, alongside a source snapshot matching that binding.
The smallest executable equivalence experiment there is:

```sh
python3 make-fixtures.py --output "$PIX574_CASES"
python3 run-controls.py --binary "$PIX574_BINARY" \
  --es-source "$PIX574_ES" --fixtures "$PIX574_CASES"
```

Run the same generator output through a separately bound baseline harness
from `a7dcdbb38009d8d2a81c7c2b4bc1d8c2d0d38a20` with `--baseline`.
Baseline expectations are raw ISO/NES success and RVZ failure, not a claim
that those controls have passed. Old malformed-input results are deliberately
unasserted and skipped, since the old unchecked reads have no safe contract.
Follow with ASan/UBSan malformed-input and repeat/parallel-handle controls,
independent Dolphin/nod byte-equivalence checks on these synthetic inputs,
and installed ES frontend/offline-index qualification. Do not use this packet
to justify converting or reading owner ROMs.

## Open integration dependency and acceptance map

**Retained zero hashes are not automatically retried.**
`CheevosIndex::take(false, zeroHash, emptyId)` selects Lookup, not Hash; the
all-zero string is nonempty. The existing force-all route selects Hash.
This candidate intentionally does not edit catalog/index or menu code.
Coordinator must qualify the existing force-all refresh on synthetic retained
state, or assign a separate narrowly scoped failed-hash retry change before
claiming automatic recovery. A valid hash can still be unmatched by the
provider; unsupported format, unavailable set, and runtime support remain
different outcomes. No invented game IDs or award writes are part of this fix.

| #574 criterion | Delivered evidence | Still owed |
| --- | --- | --- |
| Standalone/core/build/launch configuration | Existing issue evidence; exact pinned Dolphin source/recipe reviewed | Installed/runtime selection and independent in-game support; no new gameplay proof |
| Trace frontend/index behavior | Exact callback/magic/sentinel/lookup source trace; isolated reader candidate | Real compiled wrapper equivalence and retained-zero refresh |
| Source-bound defect repair | ES commit, dependency/license companion, guarded failure paths, UNRUN controls | Target compiler/link, VM positive/negative, sanitizers, boundary/ABI and existing-format regressions |
| Accurate disposition and flow | This scoped handoff only; no new player strings | Coordinator canonical flow/docs, exact-source frontend frames, offline proxy lookup/award-preservation controls, issue/integration status |

No C++ syntax-check, CMake configure, compiler, decoder, test suite, or runtime
PASS is claimed. Actual checks: Python AST parsing of the two prepared scripts,
package shell parsing, corrected `tools/pkgcheck emulationstation` rc 0,
whitespace checks, static unchanged-route comparisons, and SHA-256 bindings.
The work budget counts decoded tables/groups, unpacked output, and zero-filled
chunks. Final static review corrected the packed/zero accounting before this
packet was sealed. Upstream snapshots retain their original whitespace.
The initial full-path pkgcheck invocation matched no package and its empty
receipt is preserved; it is not validation. Initial license EOF whitespace
was corrected before the final ES commit. Two exploratory Dolphin source
paths returned 404; the actual tool/hash/spec sources listed above were read.
