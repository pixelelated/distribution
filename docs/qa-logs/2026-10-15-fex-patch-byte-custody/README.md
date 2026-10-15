# Exact FEX patch byte custody — #528

Original run `20261015T152840Z-b3a8aaf1` completed command/monitor/runner
0/0/0 and launcher0. The offline collector retained both canonical patch inputs
without a download, normalizer invocation, source execution or patch application.
Admission `a411e5039539450b8e744758bd9f99f6` was ordinarily consumed at
2026-10-15T15:28:57.557757+00:00, with all outputs held and no deletion.

The exact identities remain distinct:

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| Original large-file response body, retained as context | 1,193 | `61b196be57e03fa7cef42d2d654e6b1351efe0c930757e4e8ec3b16eade6bb6f` |
| Original failed normalizer intermediate | 290 | `73f296735999f7fcb84cd9fa9c6ca9dd26b659382d6402416ddf488a677c2ac1` |
| Canonical large-file patch: exact bytes 71–289 of that intermediate | 219 | `63a602cddfe36755593fd6c59479078f34b04a15de03b88959dc9fc69813da5d` |
| Canonical meson patch: unchanged original patch body | 620 | `233cf3f489f9dd6ec20befa4d5b2ebefc892ae6c69166d5c1fca9c4a9a6da144` |

The fixed 71-byte prefix is two Git extended-header lines; its exact bytes and
source/output bindings are retained in the plan and destination manifest. This
selection makes no general normalizer-equivalence claim and changes no expected
hash. The 839 canonical bytes and 1,483 provenance bytes are preserved together.

Destination
`/workspace/artifacts/pixelelated-release-sources/m7-fex-normalized-patches-20261015-01`
contains five files totaling 10,275 bytes, including manifest SHA256
`648e044b5b9945828b8c82b7cdf5fe1125f8ad8d2d476b2ae9d309aeb6bd7ea5`.
The original success consumer verified exact membership, hashes, immutable modes,
original exit channels and process absence before consuming the admission.

Earlier normalizer run `20261015T151501Z-6dcae797` remains failed:
command/monitor/runner1/0/1, launcher1, zero completed normalized patches,
with all three downloads and seven original tool waits0. Its original
failed-investigated consumption `3b38d221fb5f4d3cb7e83845e290780f`, failure,
root investigation and child receipts remain unchanged within the source packet.
This later byte-custody success does not relabel the earlier producer.

`originals.tar.gz` retains the exact source packet (source seal
`fe9bc7820d8ccc40bb81ba5890915a19ac1d18f113af84c1e3276de119f08bd7`),
coordinator wrapper receipts, actual owner results, original watched run and
consumed record, and the small canonical destination. Historical SOURCE ONLY /
UNRUN labels describe preparation; the separate original run records establish
subsequent execution. Other source archives, acquired tool binaries, package
archives, raw HTTP status/error streams and signed HTTP streams are excluded.
The small patch bodies are source/provenance text, not transport logs.

`members.json` records exact original paths, SHA256, bytes, modes, uid/gid and
nanosecond mtimes. Retention ran in the actual host context: uid/gid1000,
PID namespace4026531836 and user namespace4026531837. Archive readback compared
all member bytes and metadata with the originals. Any nested historical sandbox
metadata remains producer-written evidence, not substituted host ownership.
`custody-verification.json` records this finite archive verification.

This packet is compact retention of completed work. No collector, normalizer,
tests, build, VM, admission or cleanup was repeated. Source integration,
applicable notices, independent retrieval, off-host custody and publication
remain separate; no complete release-source or license clearance is asserted.
