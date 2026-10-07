The completed #461/#490 read-only review identifies exactly 22 superseded QA
QCOW files for a separate 42.05 GiB retirement batch. Two referenced base disks
are held. All compact evidence, qualified candidate/fallback, ROCKNIX baselines,
source inputs, cache and build trees remain protected.

The exact file list, identities and SHA256 values are in
`docs/qa-logs/2026-10-07-pixelelated-replacement-16/h700-retirement-proposal/`.
The original two-file D-INFRA-019 approval is complete and does not cover this
batch. **Await explicit approval of this exact proposal; no deletion yet.**

149.25 GiB is available. The first H700 arm compatibility stage has a
conservative 185.98 GiB budget, including 100 GiB operating allowance. This
batch would leave about 191.29 GiB available. The aarch64 firmware stage needs
its own subsequent capacity review; this batch does not establish that fit.

Can this be done on the VM? No: these are host disk identities, filesystem
allocation, process/container use and host compilation facts. The VM software
qualification is already complete. No physical-device action is part of this.

- [x] The fixed-scope helper's verification-only result matches all 22 exact
  identities/hashes, independent evidence and retained base disks; no mutation.
- [x] After separate authorization, a fresh full-root dependency report has
  no unresolved observations and still accepts every named file; four result
  channels and exact source/input seals are retained for execution.
- [x] Only the named files are absent, all preserved evidence hashes and
  protected identities remain unchanged, and actual free space meets the
  H700 arm budget; retain the execution and recovery receipt.

Already written: the earlier completed batch and all original failed/accepted
QA records stay intact. This proposal deletes only local superseded QA disks;
no player device, personal cloud, candidate bundle, source or cache is changed.


Verification-only completed with all four result channels zero, four seals and actual owner exits. [Exact proposal, file list and fixed-scope helper](https://github.com/pixelelated/distribution/tree/510196b072f3bec9c108ef2ad4709e30aaa40bde/docs/qa-logs/2026-10-07-pixelelated-replacement-16/h700-retirement-proposal); [verification receipt](https://github.com/pixelelated/distribution/tree/510196b072f3bec9c108ef2ad4709e30aaa40bde/docs/qa-logs/2026-10-07-pixelelated-replacement-16/retirement-verification-01). No --apply or approval record was supplied; nothing was removed. Separate explicit approval of this exact batch is still required.


## Approval and execution — 2026-10-07T03:49:05.481617+00:00

> You have my approval to do the cleanup, and you have my approval to generate the H700 build. Following the H700 build, we should try the SM8550 build.

The exact proposal SHA256 is `ab03cbbb44674b27d6bfbeaf120d8f6f68281ec83e807d6b26df40c6da1a39c9`. A new watched owner `/workspace/tmp/pixelelated-m7-h700-qa-retirement-01` is refreshing all dependencies before the fixed 22-file removal. Approval is recorded; execution criteria remain unticked until actual removal, preservation and free-space readbacks pass. Build sequence is tracked in #492. This approval does not widen the file list.


## Completed and independently verified

Execution and acceptance are published at next `0ae8c83a4fb1240a033ca2aaf6682254db6ed22c`, `docs/qa-logs/2026-10-07-pixelelated-replacement-16/h700-qa-retirement-01/`. Fresh dependency review passed; exactly22 files were removed,42.05GiB recovered; seven protected identities, two base hashes and2,695 independent evidence hashes verified. Four results0, seven unchanged seals and all owner exits verified. Available space205,386,608,640bytes exceeded the H700 arm199,695,544,320byte budget. Approval is consumed; no wider deletion. This final result supersedes the earlier verification-only approval notice.
