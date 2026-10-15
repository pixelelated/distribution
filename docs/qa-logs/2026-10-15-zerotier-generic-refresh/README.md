# ZeroTier GENERIC refresh: build, reader correction, and metadata join

This packet preserves original compact records for source
`077197e6cd3ea31f33b28aaf3882a694b3423b53`, frozen branch
`build/m7-p5-20261015-03`, build timestamp `20261015T161744Z`.
It retains the full original source packet, corrected reader02 source,
coordinator command observations, owner/launcher/resource records, original
watched runs and ordinary consumption records, and the exact tracker originals.
Historical SOURCE ONLY/UNRUN labels in source packets describe preparation.

| Original operation | Run | command/monitor/runner | launcher | Ordinary consumed admission |
| --- | --- | --- | --- | --- |
| build01 | 20261015T161906Z-85b31cf2 | 0/0/0 | 0 | 19ebce6dd8e44b299ad7abd74ff3600b |
| failed reader01 | 20261015T162636Z-fde98414 | 1/0/1 | 1 | f57142e9fc6842f7b29a4f0b061b6fcc |
| accepted reader02 | 20261015T163127Z-5682551e | 0/0/0 | 0 | ee024372b00f4314afa9fc96495b83de |
| metadata-only join | 20261015T162920Z-33308c8a | 0/0/0 | no separate launcher record | no admission receipt present in this watched metadata run |

Build01 completed the canonical `clean-zerotier-one`, `build-zerotier-one`, and
`image` stages. All stage host and inner command exits, owner and resource
results passed. Its owner recorded no signals, cleanup actions, or surviving
recorded command groups. These are original observations, not a new process or
container census during custody.

Reader01 failed because it required compiler dependency files that canonical
make does not request. The isolated source proof had explicitly added `-MD -MP`.
The preserved failed reader and initial source review did not catch that mismatch.
Reader02 preserves the image and source checks, records the actual successful
OneService compile command and object, and explicitly reports zero `.d` files
with `dependency_completeness_claim: false`. It does not inherit a complete
canonical dependency graph from the separate isolated 113-unit proof.

Reader02's original result is PASS for completed source/artifact checks,
GPT and raw/update equality, and selected installed mappings. It explicitly
sets `runtime_qualified: false`. No new VM, ARM, physical-device, release-candidate,
or publication qualification is claimed by this packet.
The retained artifact inputs/results preserve exact paths, hashes and sizes for
the image, update archive, SYSTEM and KERNEL; those payloads are excluded here.
The compressed image SHA256 is
`c5de01b869c5bb28966ab5d654b95a8ed36581c38b380ed885a5946489009932`;
the update TAR SHA256 is
`f2acfc239fd072dddfef08bec8444d149128272ba3d5b5f2ae5d6ff84890b0b6`.
Custody did not reopen or rehash those large payloads.

Reader02's initial preflight **1** remains unchanged. Its separately recorded
post-reclaim preflight is **0**. Root reported in the task transcript that the
installed guarded helper (SHA256 prefix `acfb`) successfully reclaimed
`/swap.img`, leaving `8388604 KiB` free. This is a **transcript observation only**:
no original reclaim-command receipt or complete helper hash was supplied, and
none is manufactured here. The original before/after preflight text is retained.

The metadata join is separately `PASS_METADATA_ONLY`: 2,366 component rows,
12 shared-source rows, 16 shared-source edges and two ARM companion edges.
It read 30,449,146 metadata bytes, opened zero source payloads or archives,
and left `publication_bundle_complete: false`. Its exact 4,447,095-byte index
and 16,284-byte custody worklist are retained. Later source-payload custody is
a separate operation and is not inferred from this join.

`members.json` maps every archive member to its original absolute path, exact
SHA256, bytes, mode, uid/gid and nanosecond mtime. `originals.tar.gz` retains
those original bytes and PAX metadata. The established custody helper checks
all archive members against live originals; the additional compact-record
readback verifies original channels, consumption/evidence hashes, source seals,
and metadata-join output hashes. It does not execute any candidate helper.
The six raw-image/SYSTEM/KERNEL files, build caches, source archives and source
payloads are excluded. No originals were removed, altered or moved. No build,
reader, test, VM, admission, tracker mutation, or shared canonical edit was repeated.
