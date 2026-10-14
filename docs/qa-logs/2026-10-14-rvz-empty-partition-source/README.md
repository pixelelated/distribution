# #574: initialize the synthetic RVZ empty partition-table checksum

Additive source candidate, **UNRUN**. Original generator69e0e522, source packets,
attempt01 FAIL1, and all consumed owners remain immutable. Product reader,
Dolphin binary, candidate hash binary, guest driver code and oracle code are unchanged.
No native execution, fixture generation/import, build, VM or shared record edit
was performed by this worker.

## Finding and evidence boundary

Attempt01's original `oracle/decode-0.json` records real Dolphin f36a2c5f,
exit1 in0.031860342s, no timeout. `decode-0.stderr` reports that the input could
not be opened; the oracle stops there. Loader lists/help and generator succeeded.
No later conversion or hash command ran. `source-findings.json` binds the exact
coordinator originals; it does not replace or reclassify them.

The generator zero-initializes both headers, declares zero partition entries,
and never writes Header2.partition_entries_hash. That field occupies
Header2 `[0xa0,0xb4)`, absolute RVZ `[0xe8,0xfc)`. The checksum of a zero-byte
partition table is **`da39a3ee5e6b4b0d3255bfef95601890afd80709`**, not20zero bytes.

Pinned Dolphin `6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4` unconditionally
computes this digest in `WIABlob.cpp:165–175`, then returnsfalse on mismatch.
`Create()` returnsnull for that invalid reader, which produces the observed
converter error. The generic stderr is not an instrumented program-counter
trace, but source establishes a deterministic invalid field and a rejecting
predicate in the exact reader. This is a generator-format defect; earlier
agreement with our narrower hashing reader did not certify valid RVZ format.

Dated public source check,2026-10-14: official Dolphin master resolved to
`8d2ad1a662472955497e5bb79d7b9ec6999e1f0d`. Its entire `Initialize` function is
identical to our pin after removing whitespace; exact source hashes and the
normalized comparison digest are recorded. The [official format document](https://github.com/dolphin-emu/dolphin/blob/8d2ad1a662472955497e5bb79d7b9ec6999e1f0d/docs/WiaAndRvz.md)
defines this checksum over the partition count times the entry size. The
[current official reader](https://github.com/dolphin-emu/dolphin/blob/8d2ad1a662472955497e5bb79d7b9ec6999e1f0d/Source/Core/DiscIO/WIABlob.cpp)
retains the same unconditional check. No Dolphin upgrade or reader bypass is proposed.

Source review of adjacent fields (not a substitute for the next native decode):

| Field/path | Source result |
|---|---|
| Magic/version | RVZ1; version1.0.0, read-compatible0.3.0 match pinned constants. |
| Header1 digest/file length | Existing `seal()` fills exact file length and SHA1 of Header1 prefix. |
| Header2 | Size0xdc satisfies minimum0xd5; `seal()` hashes all declared bytes; compressor-data length0. |
| Compression/chunks | NONE0 or Zstd5; chunk0x20000 is a power of two above32KiB. |
| Empty partition table | Count0 × entry-size0 means zero bytes; zero-length offset read is supported. The missing digest is the first deterministic integrity mismatch. No entry-size/offset change is needed. |
| Raw region coverage | `[0x80,0x30000)` and `[0x30000,0x60000)` do not overlap. Sector rounding recovers the stored first0x80bytes; each region uses two groups. |
| Group/table storage | Four RVZ group entries, byte offsets for tables, four-byte units for group payload offsets, correct raw/group struct sizes and declared compression. Zero-length group is the documented all-zero case. |
| Later encoding | GameCube has no Wii partitions; the pinned encoder's setup retains a raw data entry. Actual encode/decode/packed/Zstd results are still owed. |

`external/libcheevos/rvz_hash.cpp` at candidate314da58d checks the first/second
header hashes and requires zero partition entries, but does not inspect this
empty-table checksum. That explains why previous hash agreement did not expose
this malformed header. This packet does not broaden the product parser or claim
its prior results establish independent format validity.

## Minimal correction and unchanged expected data

`generator.patch` adds one assignment and its explanatory comment to a **new**
copy of `make-fixtures.py`. It writes SHA1(empty) before the existing `seal()`
updates both enclosing header digests. Only three checksum fields can change;
file length, group offsets, payload bytes and every legal raw ISO byte remain the
same. The existing padding attribution and upstream licence remain unchanged.

All functions except `rvz()` have identical ASTs, including `raw_disc`, `padding`,
`oracle`, `seal` and `main`. Retained attempt01 expectations remain:

- Raw ISO393216bytes, SHA256 `83c6dacc46797bc7d4bdcb4aa2dd253c290316c07c4cda8f6ca1afb889c44121`.
- Native GameCube MD5 **`118545082f24fc195a446d1ee7bbf816`**.
- Actual Dolphin SHA256 `f36a2c5f2f31e961ce605cc1c762f1e839f1880a0b1feeba4e09a1fccaa90d5b`.
- Actual candidate hash ELF SHA256 `5e00ed65dc6ae8031c54c4309d3f1876be4b380e438a15b8281104402e9375b2`.

Candidate generator SHA256:
`1dd4eb12ed20ed2c51e24cc45041a5c688a61e9a5ac03f45f9bb4630e7cc592b`.
New RVZ output hashes are intentionally **not invented**; the next admitted
controls/generation will record them.

`header-controls.py` is prepared but UNRUN. It loads exact old/new generator
sources in a future coordinator admission, without libzstd or any native tool,
and compares NONE and packed-NONE output. It requires the historical hashes from
attempt01, unchanged raw bytes/MD5, valid enclosing hashes in both versions,
zero/mismatching old checksum, correct candidate checksum, identical lengths and
group locations, and differences confined to the three checksum fields. Resealed
zero and bit-flipped checksums remain negative controls. This selected checksum
check is not a replacement decoder or independent format acceptance.

## Visible oracle binding and next admission

The oracle itself stays byte-identical. New `oracle-source-bindings.json` changes
**only** `original_generator_sha256` to the candidate above. The new runtime
`input-bindings.json` changes just the corresponding two input descriptors
(generator and oracle bindings), plus explicit parent/scope metadata. Every other
input, actual ELF hash, sanitizer setting, child bound and total limit remains
unchanged. `source-findings.json.visible_runtime_binding_changes` records both
before/after descriptors.

Reuse the exact input layout from the immutable
`2026-10-14-independent-format-guest/README.md`. For a **fresh** public input tree:

1. Copy the four original runtime source files `guest-run.py`, `guest-work.py`,
   `guest_support.py`, `controls.py` from d92e127fa5 into
   `/tmp/pix-input/pix574-format/packet/`. Their bytes are unchanged.
2. Copy the four files in this packet's `runtime-overlay/` into that same
   `packet/`. Its `SHA256SUMS` binds the resulting exact eight-file directory,
   including the reused source. The overlay is metadata only.
3. Use new `make-fixtures.py` at `original/make-fixtures.py` and new
   `oracle-source-bindings.json` at `oracle/source-bindings.json`. Copy every other
   input from its unchanged descriptor, including immutable guest-stage.py,
   run-independent-format.py/bounded.py, the bundle, actual ELF/sanitizer files,
   evidence and padding licence. Do not put this entire handoff packet inside the
   driver's runtime packet or add unlisted files beneath `pix574-format`.
4. Coordinator admits a new no-NIC VM20 with read-only `/tmp/pix-input`, writable
   `/tmp/pix-output`, empty executable `/run/pix574-scratch` tmpfs0700/max2GiB and
   Python3.11+. One240second total budget,235seconds work plus5seconds cleanup;
   original60second conversions/15second hashes and original-exit capture remain.

Exact next guest command, after fresh coordinator admission:

```sh
python3 -I -S -B /tmp/pix-input/pix574-format/packet/guest-run.py --run-id format02
```

Use a fresh unused run ID if format02 has already been admitted. Do not rerun or
resume format01/old owner04. The same oracle must successfully decode all five
synthetic RVZs, perform both independent encodes/full roundtrips, and compare both
actual candidate hashes before acceptance. Any failure stops progress and keeps
original receipts. No bypass, changed expected MD5 or relaxed decoder condition.
Keep the independent NONE/Zstd RVZs and `native-proxy-input.json` for the separate
native-proxy test only after successful acceptance. Sys lookup remains unmeasured.

Optional separately admitted source controls, from this handoff directory:

```sh
python3 -I -S -B header-controls.py --historical-generator /workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-13-rvz-source/make-fixtures.py
```

This command is prepared, not executed by the worker. No extra general harness,
new build, product change, shared-record edit or runtime allocation is included.
