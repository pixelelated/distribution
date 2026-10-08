# PL-003 — actionable cloud-folder refusals

This packet qualifies ES commit `1d76b3da7da75794066df1c089931b890304da7a`
against the current cloud helpers. It is a source-overlay qualification on a
synthetic GENERIC_X64 guest, not an assembled firmware or release claim.
The canonical interface contract is CF05 in
[`cloud-folder-flow-review.md`](../../../pixelelated/cloud-folder-flow-review.md).

The change recognizes only bounded, fixed backend reason lines and translates
them into a reason and next action. Arbitrary provider output is never shown.
Existing backend validation, selected-path writes, and transfer behavior are
unchanged. The saves editor checks its provider; the settings/content editors
validate local syntax and leave provider access to the later category check.

## Acceptance evidence

The target matrix passed all44 outcomes: eleven in English and French at
640×480 and1280×800. [The index](evidence-index.json) binds each result frame
to its hash, source and proof kind; [root review](root-ui-review.json) records
visual acceptance. matrix05 completed at17:10UTC with four zero result channels
and all four host owner processes absent, independently verified at17:10:57UTC.
Seven outcomes per configuration exercise actual backend or frontend refusals. Four exercise
injected status rendering (busy, timeout, settings write failure, unknown),
without claiming reproduction of those underlying environmental failures.

Host qualification passed 184 cases / 4,775 assertions, both affected C++
syntax checks, catalog and vocabulary checks, and extraction of the eleven
translated messages. All 511 host input hashes were unchanged. The target
reconstruction compiled 28 production units and linked against the qualified
cache; all 648 recorded input hashes were unchanged. The running binary is
`e80b09fdee07043468154a4c9f9ec0a4fb7bdc9ba82f7c9d806b048d5cd3b010`;
the French catalog is
`f056223d0fa947a7c9790c914b7696586b168e33135c627ebbc4d1d6d530dfb4`.

## Fixture corrections and rejected attempts

Original failures remain in their raw owner records. Their aggregate statuses
are not converted into passes. The accepted-case index combines the first five
EN640 cases from matrix02, two EN640 provider cases from matrix04, and the 37
remaining cases from matrix05. All44 passed final verification.

- Early keyboard setup used an absent preference, then wrote preferences
  outside the XML root. A separate shell attempt also used an incompatible
  nounset profile. Corrected setup uses the actual `<config>` root.
- matrix01/02 incorrectly tried provider rejection on the settings row, whose
  existing setter checks syntax only. It accepted that syntactically valid
  path. A prior explanation blaming `NoSuchBucket` for the UI result was
  withdrawn. Real bucket/unreachable proofs use the saves row.
- matrix03 lost the temporary overlay during a guest reboot. None of that
  owner's attempted cases qualifies. The previous journal, kernel and boot
  records are retained; the reboot cause is undetermined.
- matrix04's injected helper bind propagated through shared mounts and
  replaced its own delegate, causing recursive execution. The exact stuck
  process was stopped, the guest mounts made private, and the production
  delegate restored. matrix05 uses atomic helper copies and bounded witnesses.

The corrected harness verifies boot ID, ES PID, actual running executable,
helper and catalog before and after every typing, submission and dismissal
phase. Each accepted attempt requires byte-equal before/after selected-path,
configuration and synthetic payload witnesses. The earlier five matrix02
cases additionally retain their separately reviewed provenance/boot linkage.

Only local synthetic WebDAV and MinIO, plus an intentionally unavailable local
port, are involved. No physical device or personal cloud was accessed. The
packet retains compact logs, scripts, manifests and screenshots; disposable
VM disks, reconstructed binaries, QA SSH keys and provider storage are excluded.
