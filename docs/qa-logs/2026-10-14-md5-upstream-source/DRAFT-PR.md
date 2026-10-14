Title: utils/md5: avoid unaligned word dereferences
Target: libretro/libretro-common, master
Status: local draft; not posted

`MD5_SET` casts byte input to a word pointer on i386, x86_64, and vax. Those
machines can support unaligned loads, but the C dereference still requires
alignment and a compatible access type. A downstream GameCube hash under UBSan
reached this path with an unaligned buffer and stopped at the word load.

Copy the input bytes into a local `uint32_t` with `memcpy`. This preserves the
existing little-endian word interpretation without dereferencing the input as a
word pointer. The generic path, public API, digest rounds, and original license
and attribution remain unchanged. The patch touches only `utils/md5.c`.

The separate reproducer generates eight input offsets, eleven lengths around
padding/block boundaries, and three update splits. It checks264 emitted digests
against Python hashlib and retains the expected unpatched UBSan failure.

Validation so far:

- The same implementation, using the downstream `MD5_u32plus` type name, passed
  full-library ASan/UBSan integration checks on x86_64 Linux:264 digest rows for
  each of two repaired library compositions, synthetic GameCube/Saturn ISO/CUE
  wrapper calls and16 repetitions, and Wii-helper controls. No sanitizer stderr
  was accepted. The original pristine-baseline alignment failure is retained.
- Upstream base a3194c18ba65ef89734e1898a2f61403c255d368 still contains the load.
  The helper is carried over unchanged except for using upstream's `uint32_t`.
- This upstream standalone build/runtime procedure is prepared but **UNRUN**.
  No upstream suite, other architecture, or performance result is claimed.

The local draft should gain the exact upstream before/after result before
submission. No issue number, reviewer approval, or upstream acceptance is implied.
