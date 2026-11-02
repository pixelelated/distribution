# T41 final generator input binding — narrow D226 ruling

## Why this check is required

Stage C at `94b5b1c0b983313325dba101217761c6e5c9bca0` retains exact
program/commands/output hashes and negative assertions, but no manifest of
the exact drop/reach/header fixture input bytes. Its historical input identity
cannot be proved from a path. Do not amend those receipts, read retired scratch,
reconstruct historical inputs or relabel new bytes as the old test.

D-WORKFLOW-228 applies D-WORKFLOW-226's explicit failed-predicate exception:
close this one final-generator predicate with **new, dated controls**. This is
not new application/source qualification. T3 owns the supplemental audit
packet; T2 owns only the candidate acceptance reader and synthetic tests.

## Producer: T3, existing T41 worktree

Write under the existing audit's fresh `stage-f/generator-input-proof/`;
refuse an existing nonempty output rather than overwrite evidence. Do not
change the accepted formal generator, its Stage-A/B/C/D inputs or receipts.
The exact generator SHA256 remains
`ac6fe1ea48775d0c4c3b285b9b6811c1d12a83ed4ca2414d466ab6490989e558`.
Use `tools/t41-tables.py` from that audit, source ref
`02aab33bd9842610b0d466c9c186454dc14373ee`, and the retained
`stage-b/corrected/inventory-rows.json`. HEAD's 107 selected source modes/blobs
must match that source; read Git objects, not live extracted source trees.

Create exactly these new inputs from the retained JSON, preserving row order
and every other field. Retain the emitted JSON bytes, not just the recipe:

1. `fixtures/drop.json`: remove the last of the 107 rows. Expected refusal:
   `AssertionError: membership: expected 107 rows`.
2. `fixtures/reach.json`: change the first row whose `reach` is `shipped` to
   `test`, leaving all other fields/rows unchanged. Expected refusal:
   `AssertionError: reach: expected shipped 103/test 4`.
3. `fixtures/bytes/<selected-path>`: pick the lexicographically first selected
   patch whose first 60 lines contain a `From: ` line. Read its immutable
   bytes and replace only the first such line's prefix with `X-Proof-From: `,
   preserving its remainder and newline. This overlay contains exactly that
   one regular mode-100644 file. The unchanged generator falls back to Git
   for absent overlay paths, so do not export the other 106 files. Expected
   refusal: `AssertionError: From header census: expected 87`.

Run only three `python3 -I <audit>/tools/t41-tables.py stats` negatives,
using `--rows-from` for drop/reach and `--bytes-from` for the single-file
overlay, followed by one normal `stats` positive. Negative rc is exactly 1
with the matching final assertion line; positive rc is 0, empty stderr and
stdout byte-equal to retained `stage-c/tables/stats.txt`. This does not rerun
application, extraction, the five output modes or any entire historical stage.
No generator edit or script/config sourcing. Actual commands run once unless
a concrete implementation error requires a recorded correction.

Retain the small fixture builder/runner as `run.py`, all input/output bytes
and `manifest.json`. Manifest schema string is
`t41-final-generator-controls-v1`, with these required fields:

- `schema`, `authority` (`D-WORKFLOW-228`), `historical_input_identity`
  (`unavailable; new controls only`), `source_ref`, `stage_c_ref`, `run_head`.
- `program`: audit-relative `path`, exact `sha256`.
- `baseline_rows`: audit-relative `path`, exact `sha256`.
- `inputs`: three records with `kind` (`drop`, `reach`, `header`), proof-root
  relative `path`, `mode` string `100644`, integer `size_bytes` and `sha256`.
  Header additionally has decoded `source_path`, `baseline_blob_id` and
  `baseline_sha256`.
  The complete on-disk overlay file set must equal the sole header entry.
- `checks`: ordered `drop`, `reach`, `header`, `stats`, each carrying `kind`,
  actual `argv`, `cwd`, UTC `start`/`end`, nonnegative `elapsed_seconds`, integer
  `rc`, proof-root relative `stdout`/`stderr` paths and matching
  `stdout_sha256`/`stderr_sha256` values.
- `result`: `PASS` only when every asserted input mutation/output condition
  above holds; otherwise preserve the actual failing result and stop.

Normalize only the known filename escape for comparisons/source access. JSON
Unicode escaping in retained paths must decode to the real path. No symlinks,
absolute paths or parent traversal in the manifest's relative artifact paths.
Append a candid historical-gap/new-proof note to 00 and the final hand-back;
retain a complete input/output file list, exact builder SHA and validation
commands in README. Publish the supplemental packet as part of the final
T41 tip and continue existing E–H; no additional successful-stage gate.

## Consumer: T2, existing isolated acceptance candidate

Keep reconciling original Stage-C program/commands/output bytes as historical
support, with no claim to their missing input identities. Require the new
manifest and all files at the candidate tip. Independently check the schema,
authority, unchanged accepted inputs/program/source, exact deterministic
mutations above, complete single-file overlay membership/modes, actual command
shape, ordered rc/assertions, raw output hashes and positive byte equality.
`checker-run` may PASS only for this combined historical-receipt plus new
sealed-control evidence; its reason must distinguish the two. Missing new
packet is ABSENT/CANNOT, never PASS. A missing, altered or extra fixture or
wrong program/source/command/assertion/positive result is FAIL.

Add meaningful synthetic refusal/control cases for these predicates. Do not
execute T3's generator or run the real final acceptance from the support lane;
only immutable records and synthetic fixtures. No shared-kit installation.
Return the complete candidate and test evidence; coordinator reviews/installs
and performs final acceptance after the final lane hand-back. Neither owner
reads or invents the missing historical negative inputs.

Can this be done on the VM? No: this resolves an audit-local evidence-binding
predicate against Git bytes. No runtime, archive extraction, fetch, build,
config sourcing, host-ledger write, provider call, physical/cloud action or
other-agent permission answer. No product source is edited.
