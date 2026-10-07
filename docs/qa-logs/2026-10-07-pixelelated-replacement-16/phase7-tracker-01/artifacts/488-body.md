## Accepted on candidate 16

The offline validator now requires the actual pointers field and empty root, all three downloaded hashes, unsupported flag, unchanged original snapshots and verified four-result/seal/cleanup evidence. Missing/wrong-root controls fail. The original validator failure is retained; the four passing VM cases were not replayed.

[Primary acceptance](https://github.com/pixelelated/distribution/blob/7f293a22d97317d1632952a5cf2e9d4a45bd2cb2/docs/qa-logs/2026-10-07-pixelelated-replacement-16/selected-content01-acceptance/acceptance.json); [criterion reconciliation](https://github.com/pixelelated/distribution/blob/7f293a22d97317d1632952a5cf2e9d4a45bd2cb2/docs/audits/2026_10_06-milestone-m7-p4-fixes-383/10-closure-reconciliation.md); [fix commits and existing-state dispositions](https://github.com/pixelelated/distribution/blob/7f293a22d97317d1632952a5cf2e9d4a45bd2cb2/docs/audits/2026_10_06-milestone-m7-p4-fixes-383/08-installed-resolution.md).

Already written: this closure records verified evidence and changes no player files or cloud data; the original runtime failures and prior source states remain retained.

## Historical request and execution record

The four candidate16 installed selected-content cases passed and all result/input/cleanup checks passed. The separate offline acceptance script then raised `KeyError: a`: it assumed `audit_snapshot()` nested pointers under guest `a`, although the frozen fixture's snapshot has its own explicit pointer field. No failed product assertion or new runtime test is involved.

Can this be done on the VM? The behavior has already been proved on the VM. This correction only re-reads retained host artifacts.

Acceptance criteria:
- [x] Retain the failed validator source and exact raw snapshot field structure.
- [x] The corrected validator requires the actual empty root pointer, unchanged before/after snapshot, all three downloaded payload hashes, unsupported flag, four passing cases and verified result/seal/cleanup evidence.
- [x] Missing/wrong pointer controls are rejected, and the original passing runtime evidence is retained without replay.

Refs #467, #471. This is an offline evidence-validator fix only.
