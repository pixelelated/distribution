# Save integrity controls — #517

The synthetic controls use disposable host files and an independent qualified
rclone hash oracle. `synthetic-controls.txt` records 24 passing controls:
valid data, altered/truncated/missing bytes, hash/manifest/read failures,
stale remote metadata, malformed PNG/RZIP/RASTATE, unsupported raw semantics,
and Dropbox block boundaries. Personal data was not used as a test fixture.

The separately authorized private operational read completed with a stable
selected inventory and successful provider-hash/structure checks within their
stated coverage. Local counterpart comparison and installed-source analysis
are retained privately. No device setting, save payload or cloud object was
changed by the review. No game was launched, and historical progress/core
compatibility are not certified. Earlier stage/timing logs remain independent
evidence, not a complete per-file migration record.

`docs/cloud-save-integrity.md` describes scope, packet contract, limits and
carry-forward into #515/#508. Exact account inventories, paths, timestamps,
file hashes, bytes and device observations are deliberately not published.
