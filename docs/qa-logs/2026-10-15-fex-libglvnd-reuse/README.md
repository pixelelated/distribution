# Exact libglvnd source reuse

The bounded offline probe passed at 143521Z-7d559a90 with all original channels
zero. The held 839,809-byte libglvnd archive produces the exact selected recursive
NAR hash `d94f49b691b23f895bc6d54978fe465208795ed865a0fbc5230dbcfa795d631f`:
292 nodes and 6,669,360 NAR bytes. No download, source execution or filesystem
extraction occurred. The archive's flat hash remains a separate identity.

Original result: `/workspace/tmp/pix-m7-fex-libglvnd-nar-probe-20261015-01.json`.
The source plan remains historically unrun; this probe's actual result supersedes
only its libglvnd acquisition question. Held Nixpkgs and 20 patch custody, plus
two normalization-aware patch acquisitions, remain separate work.

The exact producer-written result is now retained as
[libglvnd-probe-original.json](libglvnd-probe-original.json), SHA256
`2aba531c6df7bb576c5198b4792edd1827e8d3c0bd7a40deb81d891355245e05`.
[probe-provenance.json](probe-provenance.json) records its original path, actual
host file identity and namespace, and byte/mode/uid/gid/nanosecond-mtime readback.
This is additive custody of the existing result; no probe or test was rerun.
The nested Python metadata's original uid/gid65534 are preserved as recorded,
not promoted to actual host ownership.

The existing `originals.tar.gz`, `members.json`, and `custody-verification.json`
remain unchanged: they describe 24 archive entries (21 files). The omitted probe
receipt is a separate exact file covered by the current outer seal. All original
archive members were rechecked against their retained hashes and exact metadata.
The new outer seal covers both the unchanged archive and this additive receipt.
