# Scripts and remaining local cloud baseline — #589

Run `20261015T000858Z-720211a2` ended on October 15 at 00:21:39 UTC.
The scripts suite passed in 521 seconds, SFTP round-trip in 67 seconds and
local MinIO/S3 round-trip in 111 seconds on the unchanged fac608ff image.
The previous WebDAV round-trip and other 12 passing baseline rows are retained;
they were not repeated. Screenshot comparison was handled separately under #591.

Observation-time reaping retained adopted children's original wait statuses;
the current Popen child kept its own wait. The corrected waiting-text selector
passed the existing full scripts suite. Original failed baseline02 evidence is
preserved under `../2026-10-15-qualification-followups/`.

All original outer result channels returned zero, with no timeout, cleanup
error, surviving child or QEMU process. The local backend container and its owned
temporary volume were removed; guest settings and paths were restored. Admission
79388669ce794151a311188d62ef684c was consumed after root reviewed the originals.
The stopped disks and temporary data remain pending guarded retirement, not
ongoing testing. This is local protocol proof, not authenticated Dropbox proof.
