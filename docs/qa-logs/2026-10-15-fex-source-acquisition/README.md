# FEX selected-source acquisition — original failed attempt (#528)

This compact packet preserves immutable source01 `854ce160`, root source review,
all 48 offline control results, preparation and retention checks, original owner
receipts, four watched runs, failure investigation, and ordinary consumption.
The source packet's original unrun wording records its preparation state; the
root later executed the controls and acquisition. No candidate source was run
while creating this custody packet.

| Original watched stage | Run | Command / monitor / runner |
| --- | --- | --- |
| 48 offline guards | `20261015T132627Z-4c27200a` | 0 / 0 / 0 |
| Owner preparation | `20261015T132719Z-5f35da3f` | 0 / 0 / 0 |
| Retention check | `20261015T132745Z-8bb785f5` | 0 / 0 / 0 |
| Acquisition | `20261015T132811Z-4942e582` | **1 / 0 / 1** |

Acquisition launcher, wrapper, inner and outer results are also **1**. It stopped
after 35.2576 seconds: Linux 6.16.7 was acquired and its flat SHA256 verified;
libdrm 2.4.129 then returned original curl **35**, HTTP **0**, body **0 bytes**.
The root's private-stream review categorised the error as connection reset.
This was not a complete acquisition or a source/notice/publication clearance.

The verified Linux body is 152,673,392 bytes, SHA256
`5be3daa1f9427b1bdb34c4894d9c1adfac38cff674376fe0611a3065729a1a81`.
It, the zero-byte libdrm body, and four raw curl streams remain held in
`/workspace/tmp/pix-m7-fex-source-acquisition-20261015-01`. Every `.body`,
`.curl.stdout` and `.curl.stderr` is excluded from this archive. Their recorded
hashes and host-stat metadata are retained in `held-object-references.json`;
this custody operation did not reopen/hash those contents. The 152,673,452
excluded bytes were neither copied nor deleted.

Admission `66b1fc67ac104e5aa04ad8080c93f432` was consumed at
2026-10-15 13:29:59 UTC as failed-investigated, with the original 1/0/1 result,
outputs held and zero bytes deleted. The original consumed receipt is retained.
`registry/entry.original.json` is an exact byte slice of the actual registry
object; its separate provenance identifies the source snapshot, offsets and
hash. Other jobs and the registry itself were not copied or modified.

The original cleanup receipt records no signals, errors or surviving recorded
identities. This is retained prior evidence, not a fresh whole-host process or
FD claim. No collection was retried, no TLS setting was weakened, and no source
was extracted or executed during this evidence retention.

`originals-manifest.json` maps every archive member to its actual source path,
SHA256, size, permission bits, numeric ownership and nanosecond timestamps.
Archive readback checked exact bytes/membership/mode/uid/gid and decimal PAX
mtime using host-context metadata. No directory or atime stability is claimed.
Originals remain unchanged. Any missing-source continuation requires a fresh,
separately reviewed allocation and must preserve this failure and held Linux
source. Scope does not include FEX phase-B sources, notices or publication.
