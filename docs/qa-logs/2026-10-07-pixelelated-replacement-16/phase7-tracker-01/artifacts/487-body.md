## Accepted on candidate 16

The exact owned rewritten sshd listener title is accepted; wrong-owner/config/executable controls are rejected. All three actual backend identities and exact container image are retained, with verified PID/container disappearance and318 passing protocol assertions. The original failed observer is preserved.

[Primary acceptance](https://github.com/pixelelated/distribution/blob/7f293a22d97317d1632952a5cf2e9d4a45bd2cb2/docs/qa-logs/2026-10-07-pixelelated-replacement-16/cloud02-observer-correction/controls.json); [criterion reconciliation](https://github.com/pixelelated/distribution/blob/7f293a22d97317d1632952a5cf2e9d4a45bd2cb2/docs/audits/2026_10_06-milestone-m7-p4-fixes-383/10-closure-reconciliation.md); [fix commits and existing-state dispositions](https://github.com/pixelelated/distribution/blob/7f293a22d97317d1632952a5cf2e9d4a45bd2cb2/docs/audits/2026_10_06-milestone-m7-p4-fixes-383/08-installed-resolution.md).

Already written: this closure records verified evidence and changes no player files or cloud data; the original runtime failures and prior source states remain retained.

## Historical request and execution record

The candidate16 cloud02 SFTP round-trip is running, but the independent read-only backend observer refused its identity assertion. OpenSSH rewrites its process title into one argv element (`sshd: /usr/sbin/sshd -f <owned config> -E <owned log> [listener] ...`); the observer wrongly requires an argv element beginning with the owner directory. The actual owned PID and exact configuration/log paths are present. No protocol or product failure is inferred.

Can this be done on the VM? The round-trip is VM work; process-title/port attribution is a host fact, requiring the actual owned host PID. No device or cloud credentials are involved.

Acceptance criteria:
- [x] Retain the failed observer predicate and actual sanitized SFTP process identity.
- [x] A bounded process-title check accepts the exact owned sshd/config/log and rejects wrong-owner and wrong-config controls; capture the live SFTP backend without weakening other backend checks.
- [x] Completed cloud02 has independent result/seal/cleanup verification, all three live backend observations, and exact owned process/container disappearance.

Refs #471, #383. This is a QA-observer correction, not a product change.
