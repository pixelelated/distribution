# Packaged Steam installer bridge — completed VM evidence

The single `existing-profile-dot` caller completed on the installed GENERIC_X64
VM with original installer, namespace, trace driver, fixture, VM, launcher,
command, monitor and runner results of 0. Ordinary admission
`deaa4df35a504a23b1462bd1eb0ef048` was consumed at
`2026-10-15T09:30:42.232706+00:00`. This directory retains the exact completed
export and subsequent completion/consumption receipts; no runtime was repeated
for this custody review.

The module SHA256 is
`1694f7a9b892988a67a3445c8f51031c5a5c8be02628b0be8031f233b512ad3b`.
Its provenance binds the accepted SM8550 staged/SYSTEM byte equivalence at source
`9aa7affee9d4ad5e69725cab20b6d7ad84d93dea`; the executing VM and ordinary admission
use `f8636de1d105275dbf9420bbabbbc26f79abb10f`. This mixed engineering family has
no common RC identity. The archived provenance retains the original SM producer
failure and its failed-investigated consumption alongside the later successful
reader and independent acceptance. It does not turn that producer into a
successful build result.

## Exact evidence and verification

- [Original export result](export/export-result.json), [stage result](export/guest/steam/01-existing-profile-dot/stage-result.json), and [independent readback](independent-readback.json).
- [Original host archive](export/original-records.tar.gz) and [original manifest](export/original-records.json): 82 members independently rehashed, with exact membership, bytes, modes, uid and gid also compared to the stopped owner/run originals.
- [Guest export manifest](export/guest-export-manifest.json): all 11 files independently rehashed with exact membership. The unchanged [fixture archive](export/guest/steam/01-existing-profile-dot/fixture-records.tar.gz) has 74 members verified against its original [member manifest](export/guest/steam/01-existing-profile-dot/archive-members.json).
- [Completion evidence](completion/admission-completion-evidence.json): all 14 referenced originals rehashed. [Consumed receipt](completion/admission-consumed.json) binds that evidence and the exact original runner result.
- [Archive metadata](archive-member-metadata.json) preserves the producer's member modes, ownership, names and PAX headers. Producer archive timestamps remain exactly as emitted; they are not represented as nanosecond-exact matches to original filesystem timestamps. [Copied-original metadata](copied-originals-manifest.json) records the separate exact file-copy hashes and original nanosecond timestamps.

Original host archive SHA256:
`5453b2ab2e1e42685de2fcdbca4e13bd7567f84a9c0e4b7f3982350aaec48fcf`.
Original fixture archive SHA256:
`ead6bcf4b4b5279973545df59f9e6d72cfebc2cb89357b0a01e1dab21c195b7f`.
Completion SHA256:
`53ded97d8bcbab2b437b7715da250b872417431bc0a2393bbeb0899e1e597e2a`.
Consumed receipt SHA256:
`5ba5562c887aae29249335f4251b77d332838afcc876ef5963fbcee6d1a49052`.

## Observed scope and limits

All 18 selected protected roots passed, the guest before/after parent records
are byte-identical, scratch was unmounted, and the main fixture reported no
intervention or remaining descendants. Existing host exit evidence records all
five named PIDs absent. The readback preserves ten `helper-exit` events and their
original statuses; it does not collapse events into an ambiguous call count.

The fixture deliberately uses synthetic FEX, transport and payload boundaries.
The native client exec was denied with EACCES (13), its original child exit was
126, and the complete installer returned 0. This is a portable packaged-script
bridge using installed VM dependencies, not native ARM Steam, provider,
client, gameplay, or physical-device qualification. Expected nonzero exec and
parent-exit supervision controls remain in the original archive; the all-zero
main execution claim does not apply to those deliberate controls.

The source preparation and finite reviews are retained at
[revision02](../2026-10-15-steam-artifact-bridge-plan/revision02/README.md).
Its source-only null outcomes remain historical; this separate packet supplies
actual completion evidence.

## Stopped media custody

[Stopped media identities](stopped-media-identities.json) lists the four exact
files under the original owner's `vm/`, with device/inode, size, allocation,
mode, ownership and nanosecond timestamps. It was obtained with `lstat` only.
The files total 2,711,568,384 logical bytes and 2,343,841,792 allocated bytes.
No firmware or media payload is copied here. This list supports root's ordinary
retention review after durable evidence is verified; it is not a new process,
root-FD, mount or namespace census, nor a deletion or retirement receipt.

Original owner:
`/workspace/tmp/pix-m7-steam-artifact-bridge-20261015-02`.
Original export:
`/workspace/tmp/pix-m7-steam-artifact-bridge-evidence-20261015-02`.
Original run:
`/workspace/repos/rocknix.worktrees/m7-p5-build-20261015-02/.build-runs/20261015T092639Z-3b69cb85`.
