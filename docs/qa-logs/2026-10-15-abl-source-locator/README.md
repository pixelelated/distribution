# ABL selected implementation source locator (#528 / #601)

This packet preserves two immutable originals: the source-only next-step packet
`ec9ee9a8` and the separately allocated metadata lookup `06ba6657`. The archive
contains all sealed files and both original seals, with exact source paths in
`originals-manifest.json`. Issue bodies are observed historical snapshots, not
claims about the current live tracker.

The selected SM8550 ABL v1.2 ELF is 258,048 bytes, SHA256
`8c27a70961476b327071ada2fd9b9c55dd2dcdc913eff3d33f2576133d7e398c`.
Release records declare implementation commit
`e9d37131c0c2273076468156fb0f87aa6834202b` in ROCKNIX/LinuxLoader. The public ABL
packaging repository and a distinct OpenABL source/binary are not substituted
for that implementation.

The allocated lookup made one public GitHub commit-search request, HTTP 200,
55 response bytes, with zero exact matches reported. Conditional exact-commit
and root-tree reads were not made. The original tool return was exit 0, chunk
`8fe152`; `lookup/execution-observation.json` is explicitly a retained observation
of that return, not a producer-written launcher receipt. The earlier source
inspection JSON failure and historical HTTP 404/422 observations are preserved.

The empty bounded search is not worldwide absence proof. An accessible locator
for the exact declared implementation and its recursive/fetched build inputs
and notices remains needed. This retention does not contact upstream, download
source/binaries, execute source, change the product, or grant publication/legal
clearance.

Archive readback checks exact membership, bytes, permission bits, numeric uid/gid
and decimal PAX nanosecond mtime against host-context original metadata. Directory
and access-time stability are not claimed. No original was changed or deleted.
