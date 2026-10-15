# Final inventory source packets — retained, unrun

This directory preserves the two immutable source packets prepared for the final five-profile inventory under #528. It contains source, finite review evidence and original source-check receipts only. No preparer, collector, lifecycle runtime or firmware acceptance ran during retention. No firmware or build cache is duplicated here.

| Packet | Original seal | Retained archive | Exact archive members |
| --- | --- | --- | --- |
| Lifecycle02 | `6a57502a9a97d0d9fa6049cc730aa841565a0cbd903f0af58dd2c27d2bd3970c` | [lifecycle02-source.tar.gz](lifecycle02-source.tar.gz) | 54 files, 4 directories |
| Revision03 | `6b2c7bf6e9d953d054ab666df6f5ab25b8bc184660c267c12bcce218059a99a3` | [revision03-source.tar.gz](revision03-source.tar.gz) | 68 files, 6 directories |

The source packet roots are `/tmp/pix-m7-final-inventory-review-20261015-02` and `/tmp/pix-m7-final-inventory-review-20261015-03`. Each archive includes the complete packet, including its original `SHA256SUMS`, under `packet/`. The detached [lifecycle02 seal](lifecycle02-SHA256SUMS) and [revision03 seal](revision03-SHA256SUMS) are exact copies; their relative paths describe archive contents, not this directory. Revision02 retains the original 485b9937 seal and history; revision03 retains revision02's original seal, manifest and review text. None of those originals was modified.

The [original finite lifecycle findings](lifecycle-findings.md) are copied without changes from lifecycle02's `lifecycle-references/findings.md`. They identified numeric process-group reuse and lost child wait/status on interruption. Lifecycle02 replaced numeric-group authority with the qualified PID/start-ticks/pidfd/subreaper pattern and retained actual direct-child waits. Its 87 passing checks are source checks, not runtime qualification.

Root's next review found the child signal-mask inheritance gap: the parent's protected spawn window also blocked TERM/INT in the child across exec. [Revision03's source review](revision03-source-review.md) records the narrow correction: require a single-threaded runner, restore the captured original mask in a minimal child-only callback and retain parent registration protection. The executable diff SHA256 `5a80d844facbba9bda2853efed64922810ee7298a61284099f8b518713319999` received root's finite source acceptance. Revision03's 133 passing checks parse source and compare bytes; they do not execute a candidate helper.

Revision03 also binds VM/H700 to `f8636de1d105275dbf9420bbabbbc26f79abb10f` and SM8550 to `9aa7affee9d4ad5e69725cab20b6d7ad84d93dea` at SM05. The complete product diff must be exactly the ABL recipe checksum replacement, with fixed old/new Git blobs and exact per-commit source maps. The family is explicitly mixed engineering, with no common RC identity. The inventory's ordinary admission and runtime tool checkout remain GENERIC_X64 f863.

Runtime remains pending actual successful SM acceptance and ordinary consumed receipts, followed by root's fresh resource allocation/admission. The SM final receipt template remains unresolved; no artifact names or hashes were invented. Existing notice, corresponding-source custody, retrieval, off-host recovery, physical-device and publication holds remain open. This storage verification does not close any of those gates.

[Lifecycle02's member manifest](lifecycle02-member-manifest.json), [revision03's member manifest](revision03-member-manifest.json) and [custody review](custody-review.json) record exact membership, payload bytes/SHA256, modes, numeric UID/GID, owner/group names and PAX nanosecond modification times. All 132 archive members were read back without extraction and compared with the original files. The sources were unchanged before and after. Archive compression is lossless; all original seals and historical failed-source findings remain recoverable.
