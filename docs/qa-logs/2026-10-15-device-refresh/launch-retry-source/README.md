# H700 launcher retry source custody

This compact archive preserves the exact sealed source-only continuation packet from `/tmp/pix-m7-h700-launch-review-20261015`, including the SM8550 derivative, original static and continuity observations, 58 original source/receipt/log copies, and the source seals. The source packet seal is `8d27d7d08dfd412ad84671d55c5215668f2a1a557c4e25e27e2740e7a4107d7b`.

The archive contains 204 regular files (203 sealed payload files plus their top SHA256SUMS) and 16 directories, with no symlinks or special files. `member-manifest.json` records exact membership, file bytes/SHA256, permission modes, UID/GID, and nanosecond mtime. Readback verified every archive member against the original source using `stat.S_IMODE` for permissions and decimal PAX mtime; the original source was rechecked unchanged afterward. Archive paths are relative to the source packet root.

The packet fixes the explicit host gateway profile while retaining canonical inner ARM then AArch64 selection. It preserves the failed owner01 result, already consumed cache-copy provenance, and eight completed normal cleans, and prepares a fresh owner02 without a second copy or clean. Source-only and runtime limits remain those in the archived README and review records. The recorded read-only continuity and static checks are preserved exactly; no new preparer, admission, compiler, VM, cache operation, runtime test, or status relabelling was performed while retaining this archive. Active owner02 results belong to root's separate original run evidence and are not asserted here.

The outer SHA256SUMS binds this README, member manifest, and archive. No disk image, full cache, private device configuration, or full native evidence archive is included.
