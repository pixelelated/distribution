# Read-only retention and capacity reports

`retention-report` implements the first reporting portion of #461 and
D-INFRA-018. Run it after required qualification and before the next build:

```sh
tools/watch-build -- python3 -I tools/host-maintenance/retention-report \
  --plan /absolute/review/plan.json --output /absolute/review/report.json
```

The output must be new. The tool reads production storage and writes only the
requested report. It has no deletion, permission-changing, process-stopping,
swap or privileged mode. A successful command means the report was produced;
inspect each candidate's `eligible` and `rejection_reasons`, inventory errors
and each build's `fits_now`. A completed report can reject every removal.

The initial scope is explicitly identified, superseded QA disks. Other object
classes are rejected. Worktree removals still use `tools/fork-worktree` under
their own reviewed scope. A report does not authorize any deletion, and cannot
extend an earlier batch's approval.

The JSON plan contains:

- `scan_roots`: existing absolute project storage roots. No directory symlinks
  are followed. Read failures remain visible and prevent removal proposals.
- `reference_stores`: preservation stores inside those roots. Any exact
  candidate path in their JSON files conservatively counts as a reference,
  including unfamiliar schemas. Oversized or unreadable JSON is unresolved.
- `protected`: current and fallback candidate/build roots, upgrade baselines,
  sources, licensing inputs, shared cache and required evidence. Their identity
  observations are retained. Protection includes descendants and ancestors.
- `volume`: the filesystem whose available bytes must accommodate the build.
  Availability uses `f_bavail`; filesystem reserve is excluded.
- `candidates`: exact paths classified as `superseded-qa-disk`, each with its
  expected `identity`, owner path, original lifecycle and cleanup receipts,
  independent retained evidence paths and SHA256 values, and a hash-bound
  `superseded_by` acceptance receipt whose result is `PASS`.
- `builds`: one explicit forecast per scheduled stage, with integer
  `terms_bytes`, a written `basis`, and hash-bound measurement `evidence`.
  Include independent build/copy, artifacts, QA and operating allowances.
  Distinguish measurements from future growth estimates. For sequential
  stages, later forecasts include earlier outputs that remain on disk.
- Optional `source_fixtures`: exact protected source files that resemble disk
  images but are package test samples. Each names its identity, SHA256, source
  archive path and SHA256, and exact regular archive member. The tool compares
  the actual member bytes and rechecks the file during discovery. An altered,
  unprotected or proposed-for-removal fixture is held. This is an explicit
  per-file classification; no source directory or extension is skipped.

`identity` contains device, inode, size, nanosecond modification time,
allocated bytes, uid, hardlink count and mode, as emitted by the tool's
`identity()` function. Every proposed file is hashed and its identity read
again. Hardlinked, changed, nonregular or differently owned files are held.

The retained evidence list should cover the complete independently preserved
compact record: logs, source/input identities, reports, frames and failure
evidence. Hashing a receipt alone does not establish that this set is complete;
that selection remains part of the reviewed plan. The tool verifies all listed
bytes and independently retained copies of both completion receipts. Existing
preservation is assumed complete, so additional preservation cost is zero;
perform and verify any additional preservation before forming this plan.

Dependencies are read from actual QCOW backing chains, relevant symlinks,
hardlink counts and JSON references across preservation stores. QCOW headers
are recognized in `.img`/`.raw` files; explicitly named virtual disks are also
inspected. Unknown formats and failed chain inspection prevent proposals.
A disk that another disk references is held even when both are candidates.
Directory-entry metadata avoids repeated stat calls while retaining traversal
of every directory in the declared roots. The first production run identified
64 small shared-mime-info 2.4 MIME samples; they are classified only against
the override recipe's pinned archive and its exact four members (#490).

Active-use checks inspect actual host process arguments, recorded owner PIDs,
and all running/stopped container mounts. Any live QEMU holds all candidates.
The report does not claim a root file-descriptor census or coverage of disks
outside the declared project roots. Establish those scope boundaries before
using it for a batch. The isolated controls do not require root:

```sh
python3 -I tools/host-maintenance/test-retention-report
```

They create actual temporary QCOW files, backing chains, cross-store links,
an owned process, unreadable paths and altered evidence. They assert both
eligible independent files and refusals, and check that no disk is removed.

Before any later authorized action, refresh the report, retained evidence,
exact file identities and active-use observations. Available space and process
state are snapshots, not reservations. Preserve the approved plan digest and
verify actual recovery and retained inputs after the separate guarded action.
