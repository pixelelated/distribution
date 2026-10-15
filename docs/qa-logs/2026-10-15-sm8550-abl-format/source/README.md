# #602 SM8550 ABL format: reviewed source custody

This retains the immutable source-only continuation at
`/tmp/pix-m7-sm8550-abl-format-20261015`, seal
`a21e5fb59b64de08d2d000def1e622f657711a66b54238efba5aeae2a90b0fa7`.
At source sealing, preparer, reader and independent acceptance were **UNRUN**.
This is that historical source/review snapshot, not a current runtime status
report. Any later root-owned execution and actual results belong to separate
records. `source-status.json` leaves those future outcomes null.

`source-packet.tar.gz` retains all99 original regular files (98 sealed payloads
plus SHA256SUMS) and4 directories, byte-for-byte. This includes the exact reader
and lifecycle diffs, bindings, source/metadata originals, header readback,
12 pure format controls and their actual stdout/stderr/exit observations.
No firmware, cache, ELF payload, large compiler log or full prior failure/archive
packet is included. The selected small original records already within the
sealed source remain unchanged; their prior provenance is preserved.

`review-originals.tar.gz` separately retains the exact root review and released
peer packet:6 regular files and1 directory. Root review SHA is
`c8ecf78d255ee91c7728a3bd964221df8df77cf2a4c65f65da5f76fdfcdcfd67`;
peer seal is
`f2cef8b6f198e0bc15473dbc776697e399dddee51a7497410afd1ab87b6a313e`.
Both finite source reviews found no concrete source blocker. They qualify
only the reviewed conditional source handoff, not actual reader/acceptance
execution or native hardware behavior. Exact convenience copies of the inner
seals refer to members of their archived packets, not this outer directory.

The defect is a QA classification error: the exact258048-byte signed ABL member
8c27a709 is ELF32 little-endian EM_ARM40. The correction adds only its named
path/device/full digest/size/format guard; other selected userland ELF64/AArch64
checks and all five-file source/package/staged/SYSTEM/update/raw equalities stay.
The retained controls demonstrate old refusal and bounded positive/negative
format cases without executing the bootloader or full reader. Existing upstream
checksum correction and unavailable implementation/source-notice scope remain
separate; no upstream product repair or legal clearance is claimed here.

Original SM05 source9aa7 producer20261015T081827Z-07dceee9 remains consumed
failed-investigated, command/monitor/runner1/0/1 and launcher1. The root's exact
five-file assembled-output manifest b456c925 remains unaccepted/qualificationfalse.
The proposed fresh owner is `/workspace/tmp/pix-m7-sm8550-reader-20261015-01`.
It reuses the qualified reader lifecycle, preserves original failure, and
requires fresh reader0 followed by consumed independent artifact acceptance0.
No compilation, cache copy or image regeneration is proposed. Commands explicitly
separate preflight/report review, admission and launch. Later Steam/inventory
consumers require explicit new path/schema bindings and actual outcome hashes.

`member-manifest.json` records every original locator and archive member with
SHA256/size, permission mode, UID/GID, user/group names and nanosecond mtime.
Custody readback checked all110 archive members, exact decimal PAX timestamps,
and unchanged originals. No archive was extracted. Both source and peer inner
seals were rechecked before retention and all archived members afterward.
`retention-verification.json` records these data-only checks; outer SHA256SUMS
binds this directory. This retention step executed no preparer, reader, admission,
compiler, VM, container, collector or cache scan. Root owns staging/integration
and all actual runtime. No physical boot, RC or issue closure is claimed.
