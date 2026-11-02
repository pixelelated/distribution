# Stage B — incomplete, early-blocker packet

See `early-blocker.md` for the source-only disagreement, exact reproducer, retained results and coordinator question. This is not a complete Stage-B checkpoint.

- `cached-apply.py`: original runner, preserved after it exited on the firmware empty-root assertion. Do not rerun over its existing scratch trees.
- `archive-sha256.json`: fresh post-run verification of all five archive/sidecar/recipe hashes.
- `order-*.txt`, `targets-*.txt`, `tar-*.json`, `tar-*.out`: plan input and extraction receipts. Firmware has no order file from the aborted initial loop; its sole path is in `firmware-refutation.json`.
- `applies-*.txt`, `logs/`: literal initial dry-run/application output. H700's six failures are contaminated by the false failure at order 011 and do not establish product defects.
- `refute-H700-011.json`, `logs/refute-*`: first independent full-application refutation.
- `refute-dry-run.py`, `same-input-refutation.json`, `logs/same-input-*`: second refutation, asserting the dry-run and normal application use identical input tree and patch hashes.
- `firmware-refutation.json`, `logs/FIRMWARE-001.*`: both new firmware targets apply after creating the empty scratch root.

Committed filename text retains the literal `\u002d`; decode only for path comparison/source access. No Stage-A command receipt was changed.
