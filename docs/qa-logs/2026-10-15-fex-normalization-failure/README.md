# FEX normalized-patch attempt: original formatting mismatch

Run `151501Z-6dcae797` downloaded the exact trusted Ubuntu package (82,352 bytes)
and both raw patches (1,193 and620 bytes). All seven actual child invocations
returned0, but the collector correctly refused the first canonical output hash.
The combined original command/monitor/runner outcome is1/0/1 and launcher1.
Owned process closure passed; failure consumption `3b38d221` preserves the result.

Patchutils0.4.3 retained two Git extended-header lines. Passive byte inspection
shows the exact290-byte normalized output, minus its recognized71-byte prefix,
is219 bytes with the required SHA256
`63a602cddfe36755593fd6c59479078f34b04a15de03b88959dc9fc69813da5d`.
The620-byte raw meson patch already equals its required SHA256
`233cf3f489f9dd6ec20befa4d5b2ebefc892ae6c69166d5c1fca9c4a9a6da144`.
This does not claim general normalizer equivalence or turn the failed collector
into success. A separate data-only custody operation must retain those exact
outputs; no further download or normalizer invocation is needed.

This compact packet retains executable source and original structured receipts,
including the exact prefix and input/output hashes. Raw HTTP streams, downloaded
package/tool bodies and patch bodies remain outside Git. No package installation,
source compilation, patch application, device action or publication occurred.
