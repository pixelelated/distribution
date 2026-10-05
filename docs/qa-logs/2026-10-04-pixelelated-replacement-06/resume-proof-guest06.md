# Fresh-context resume proof — guest06

Read-only session-stash proof by `m7_guest06_checkpoint_proof`, given only
repository paths without session history. Final observations were made at
2026-10-05 00:32–00:33 UTC. This is a handoff proof, not a code audit.
The reviewer changed no files or services and ran no tests.

The reviewer independently rehashed all 6,547 product files, 200 QA files,
180 symlinks, host options and all 14 candidate members. No mismatch against
frozen `57cbc9b981205328444d41f6c4237dc9f5736d7f`, inputs `82764873…` or
bundle `d4007387…`. ES remained clean at `c75aa3fa…`; the actual Docker image
matched the pinned digest and 24/4 job settings. Completed qa07/image07/
sweep04/settings06/link06 result channels and terminal log hashes matched;
all their recorded PIDs and the QA MinIO container were absent.

At 00:32:32 guest06 runner610223, watcher610224, command610253,
QEMU611028 and WebDAV613050 were alive with the expected owner paths.
Former held SSH742141 was absent. At 00:31:57 the case logs had advanced to
11 completed cases, 64 PASS, 0 FAIL, with G active. This was normal advancement
from the earlier checkpoint, not a terminal verdict. The 24 then-recorded
frame hashes matched; the reviewer independently inspected H/A/K frames.

All seven following owners and the supplemental cloud-ui-01 owner were
sealed and unstarted. The reviewer reconstructed the recorded execution
order and correctly kept ordinary RA, authenticated Dropbox access and P4
ahead of the first H700 build. The live milestone agreed. Actual remote
readback at 00:31:18 confirmed feature `6a0127eb…` and next `c6cf90f7…`;
local origin/next was stale. The archived checkpoint was byte-identical to
the then-published next checkpoint.

One acceptance clarification remains: #362 still says that signin-memory
stays within its bound, although the actual tool has no numerical ceiling
assertion. D-WORKFLOW-048 supplies measured comparisons and a 1 GiB loaded
page observation, not a generic enforced threshold. The criterion remains
open; reporting a successful load alone does not resolve it.

## Correction/readback proof — 01:08:29 UTC

The same reviewer independently verified the eight new completed-owner
receipts against raw files, all four result channels and terminal-log hashes.
Guest06 totals249PASS/0FAIL with33 reviewed frames. Runtime06 remainsrc1/36ms;
diagnostic01 and diagnostic02's later parser failure remain failures. The
inspection explicitly distinguishes persisted prior bytes from the live
failed write. Recomputed diagnostic batches23/29/26ms include36 exact,
timestamp-valid transfers and zero migration-journal changes. Separate trace01
is rc0; instrumented timings are not acceptance. Runtime07 records272/244ms,
28ms against unchanged30ms,12 exact transfers and14+4+13 passing assertions.
Proxy05 records20 passing assertions and only the documented pre-execution
launcher change. No unsupported original-timing cause was claimed.

At01:07:46 optins05 runner914305/watch914306/command914335 and owned QEMU
915438/915465 were active, with MinIO7e6bbbd1f20f. All completed-owner PIDs
were absent. At01:07:52 live M7 matched the recorded ordered queue. All six
later owners were unstarted. Frozen HEAD and manifest digest remained exact;
the reviewer did not repeat full hashing in this followup. Its stale proxy
sentences were corrected; #362's undefined bound remains explicitly open.
Subsequent optins completion and memory launch are primary observations.
