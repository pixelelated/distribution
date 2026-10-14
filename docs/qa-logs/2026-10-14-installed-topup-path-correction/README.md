# Installed #567 path expectation correction

Owner02 failed in `backend-state.py:74`, expecting the absolute ROM path. The
exported database contains `/gb/new.gb`, exactly the product's intended stored
form. `raofflineproxy-cache-indexed:132` calls `normalize_cached_rom_path`;
prepared `rom_browser.py:126-133` keeps the last two segments, and its documented
consumer at145-146 explains that this stays stable across mounts/devices.
Existing upstream-source test at462-465 checks `/mnt/roms/gb/Tetris.gb` becomes
`/gb/Tetris.gb`. This indexed writer dates to8c03cbb6e77, September14.

The archive's database is36,864bytes, SHA256
`77f39d966025924d24489821ed585f3a6a991d62e0d522295ae3a54991c82bb9`.
Its WAL is0bytes. Read-only immutable querying of an exact private byte copy
reports integrity `ok`, no pending award, new patch `/gb/new.gb`, and unchanged
old patch `/storage/roms/gb/existing.gb`. Original evidence, error and actual
exit1 remain preserved. No disk read or product replay was necessary.

`backend-state.patch` changes one string literal, retaining a strict exact
assertion. The old absolute seed remains untouched and still must be preserved.
All cache payload/category, readiness, stamp, queue, log, observer and cleanup
checks remain. Nothing in the failed run is promoted to PASS: later statements
were not reached. This is a fixture correction, not a product patch.

Ready source derivative: `lifecycle/`, SHA256SUMS `ff5ad016074817f3f2d19d4708fec7ba68ef4af9c99e131301758225b615e10f`.
Corrected adapter archive: `adapter-originals.tar.gz`, SHA256 `de6936b1a552f3b6ee45f553f846990268d0372395d80bfd248d17e1047b57bd`;
inner SHA256SUMS `56d85cd64ff189676c4a97c6a48ffb818ad4a9d6c2c4d041b60d0e51ad9b6d9b`. The lifecycle executable diff changes only three
hash constants to bind this derivative. Use its README's existing preparation
command with a fresh owner03, completed final custody and explicit coordinator
`--clean-checkout`; root alone allocates runtime. The original clean02 and
installed adapter seals remain byte-for-byte intact. No runtime was run here.

Static checks: all adapter and lifecycle Python ASTs parse; exact manifests and
archive byte roundtrip verified. This is not runtime acceptance. Evidence and
source identities are in derivation.json and evidence/database-readback.json.
