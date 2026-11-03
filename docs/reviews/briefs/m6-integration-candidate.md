# M6 ordered integration candidate — v2

Owner: M6 coordinator, wN:p2, #346. This is source candidate preparation under the
maintainer's standing request to continue M6 across the existing lanes. Root owns
the order, resolutions, acceptance, eventual live integration and runtime. The
current M7 owner explicitly permits interpreting its handoff as comparison inputs,
not as release of `next`. No worker may promote a branch or select an ES pin.

## Inputs and boundary

- Distribution `next`: `8ebaf8daad8eaac6331dff6fc048fb4411d7decb`.
- Frozen M6 coordinator: `71bee11968b8a2f3b0165004f21c5498a47a6054`.
- M7 owner checkpoint: `41b5287311476efd076bf6f9efca0cc94099fbec`.
  Its product directories and complete ES package equal dated product
  `1850362563dc02720f1910faa415ed96580fa7d2`. M7's pending Nova reboot
  permission is untouched. Public RC designation is not a prerequisite for this
  source preparation; live `next` ownership remains with M7.
- ES recipe base: `16dbac5211eea7e70db7394372033be2be7df829`.
  M7 complete package tree is `adb10ce0720d571e913bc0a1c45a344518639fcd`;
  patches tree `b17587b4d1eaf7e1083f7e37af44f8e262969d35` contains 001–028
  and the separate architecture patch `x86_64/cpugov.patch`. Pin equality is not
  effective source equality. Keep recipe/hooks and patch order explicit.
- Read-only distribution object stores: `/workspace/repos/pixelelated/distribution/.git/objects`
  and `/workspace/repos/rocknix/.git/objects`. ES object store:
  `/home/max/Development/emulationstation-next/.git/objects`.
  No shared object, ref, index, configuration or worktree writes.
- First probe: `docs/qa-logs/2026-11-03-m6-integration-preparation/candidate-probe/result.json`.
  Its tree `e1049c23aa6bfaebd41f110146868b106ed1a280` in private
  `/workspace/tmp/m6-coordinator/integration-probe-20261103-s3s4gxnq/distribution.git`
  contains conflict markers and is **not** a resolved or accepted candidate.
  Merge inputs above have exact merge-base `next`; exit1 is retained.
- Probe program: `docs/qa-logs/2026-11-03-m6-integration-preparation/probe-integration.py`,
  SHA256 `2acb58f815fdf12e9ce3599f5d1dd08e742eea95ba764fecb904fabf1cf80e00`.
  Command receipts: `docs/qa-logs/2026-11-03-m6-integration-preparation/candidate-probe/commands.json`,
  SHA256 `7d8bb4be72ff8fe56114ba7e0e1eba76825b698ac266f0279fa8a6ebca40e07b`.

The prior two rounds under #346 comments6607568979/6608027633 are complete inputs,
not tasks to repeat. The five workers below own distinct deliverables. After the
stranger proof, root posts the explicit dispatch selecting the final brief hash.
Do not begin an implementation from this candidate alone.

## P1, wN:p3: handoff proof

Read this brief, the probe program and its retained result/command metadata; use
at most ten top-level commands to check the handoff's interfaces and limits. The
required artifacts are in the coordinator worktree. Identify concrete missing
inputs or contradictions. Do not re-run the actual merge probe, inspect target
bodies, change shared files, or treat this proof as code-audit acceptance. Return
a private report with exact input hashes to wN:p2, then stop. Root consumes any
correction before the four implementation dispatches. Later independent review
of returned implementations is a separate bounded task, not implied here.

## T1, wN:p4: exact fork-tool-list resolver

Implement a private Python function/CLI for the single conflicting file
`.claude/rules/fork-workflow.md` in the first probe. Read only that file's
base/M7/coordinator/probe bytes. Root's resolution specification is: preserve the
coordinator's complete file and exact existing tool order, adding M7's
`tools/vm-frontend-lifecycle/` immediately after `tools/lint-audit-artifacts` in
the unique `Fork-only tools` row. Preserve the three coordinator entries
`tools/renovation-inventory`, `tools/renovation-drift`, `tools/renovation-status`
and every other byte. Verify that M7/base/coordinator differences in
this conflict are exactly the four named additions; otherwise refuse and return
the concrete difference. Do not resolve a broader or changed input silently.

The CLI accepts explicit input blobs/files and writes a new candidate file plus
input/output SHA256 and Git-blob identities under its private root. It must refuse
wrong input identity, missing/duplicate row or insertion anchor, unexpected tool
delta, symlink output or existing output overwrite. Prove these refusals with tiny
synthetic inputs; separately read back the actual candidate against the exact
specification. No Git ref, index or root probe mutation. Root installs the returned
bytes into the eventual candidate after independent verification.

## T3, wN:p6: shared-record reconciliation helper

Implement a separately named private reconciliation helper for the twelve record
paths in the first probe result: decision-register, friction-log, nine day logs,
and INDEX. Read only those named base/M7/coordinator bytes; a missing base for a
day file means an empty ancestor, not missing evidence. Read the coordinator's
`tools/work-log-index` interface if needed; never run it against a live worktree.

Root's policy is preserve every whole historical entry/decision row from both
sides. Deduplicate only byte-identical entries. Preserve each side's relative
order; if these orders cannot both hold, refuse that file. A changed existing row,
same ID/heading with different payload, unsupported heading grammar or ambiguous
entry boundary must be returned as an unresolved explicit collision, not rewritten
or waived. Prologue differences are explicit; preserve only when byte-identical
or unambiguously additive. Do not sort the text inside entries. Keep provenance
and hashes for each selected whole entry. Regenerate INDEX only after root has
installed all resolved day files in a new private candidate; the helper returns
INDEX as pending, never concatenates generated tables.

The implementation may produce partial resolved files with a manifest naming
every unresolved file. It must never call partial output a complete merge. Prove
whole-byte preservation, both-side order, identical deduplication and refusal of
changed old rows, ambiguous timestamps, contradictory order and unsafe output
with new tiny fixtures. Preserve actual failures and return exact remaining
collisions to root. No accepted log/parser/test replay and no old tool changes.

## T2, wN:p5: construct the M7 ES comparison baseline

Create one new source-only baseline in a private Git store/index, using immutable
ES16dbac and the exact M7 001–028 patch blobs from41b528. This is a new input to
M6 composition, not a replay or recertification of an accepted M7 build. The exact
reader routes, both at `41b5287311476efd076bf6f9efca0cc94099fbec` in read-only
`/workspace/repos/rocknix`, are
`projects/ROCKNIX/packages/ui/emulationstation/package.mk` and `scripts/unpack`.
The latter defines ordering at lines124–159 and inline application at191–197;
no additional ordering/strip helper is needed. Read these immutable files without
sourcing them. Use C-locale order for this common-package comparison construction;
record that the actual unpack code uses patch-p1 or git-apply-p1 and substitutes
`@TARGET_CPU@`/`@DEVICE@` on its text route. Require those two placeholders absent
from all28 common patch payloads before strict construction; otherwise return the
specific missing selector input without guessing. This is the named common-package
overlay, not a claim about uninspected project/device patch roots. If these inputs
do not determine one common patch order, return the exact ambiguity before
application. Keep cpugov separate as an architecture-specific overlay; do not
fold it into the common ES baseline or silently rename `x86_64` to `x86`.

Use a new private bare repository with read-only ES alternates and a private
index. `git read-tree`/`git apply --cached`/`git write-tree` may write only there.
No checkout or execution of product code. Refuse immediately if strict application
fails; keep the actual output and do not add fuzz, force, rejects, reverse checks
or alternative applicability policy. `git apply` success proves this strict
construction only, not build-engine equivalence or runtime behavior. Record each
input blob/mode/SHA, argv/exit/raw streams and before/after tree. Do not invent an
exit if an operation did not run. Bind all28 exact patch identities and the recipe
and unpack identities. A failed prefix remains a failed prefix, never a baseline.

Return the private store, complete baseline tree if constructed, exact construction
receipt and a preservation contract for the full distribution package. Do not
merge accepted M6 tips yet, remove distribution patches, change the recipe, choose
a new pin or run any old producer/test/build. Root chooses composition after seeing
the actual result. Any source blobs stay only in this private `/workspace/tmp`
Git store, not in `/tmp`, the coordinator records or chat.

## T5, wN:p7: ordered private merge driver

Implement a private, generic driver taking an explicit JSON array of full commit
IDs and a caller-supplied initial commit/private bare repository. Root supplies
the final order and endpoint selection. The driver never guesses from a branch,
issue header, marker absence or worktree HEAD. It must check every object is a
commit and fail on duplicate/missing/abbreviated inputs. Disable replacement refs,
ambient Git configuration and custom drivers. Refuse repository paths outside
the new owner scratch root and refuse a non-bare/shared source repository.

For each next endpoint, run `git merge-tree --write-tree -z --messages`. On rc0,
record the complete output and create a private synthetic commit with both exact
parents and actual current timestamp/explicit synthetic author; synthetic commits
are not accepted lane commits. No external ref is changed. On rc1, stop with the
conflict tree, all conflict stages and attempted parent pair; do not advance the
candidate, resolve conflicts, select ours/theirs, or skip the endpoint. Other exits
are errors. Resume accepts only a separately root-approved resolution tree bound
to that exact failed pair and records it as a new synthetic merge. Distinguish
ancestry/no-op incorporation from an actual new source delta. A clean merge is
not acceptance and must not run tests, recipe hooks or runtime.

Prove with new tiny private Git repositories: clean merge, conflict stop/no later
endpoint attempted, missing/duplicate/abbreviated input, wrong resume parents/tree,
noncommit input, unsafe output/repository confinement, and history ancestry retained.
No real M6/M7/ES integration execution by this worker; return the program, fixtures,
manifest and exact invocation for root. No shared-kit install or old harness edits.

## Execution and return

Each implementation uses its own freshly created directory under
`/workspace/tmp/m6-<lane>-integration-20261103-*`, after current `df -B1` and `df -i`.
Record owner/purpose and retain it for the pending root integration work; no cleanup
of other scratch. Small metadata reports may be under `/tmp`. CPU8–23 throughout.
Actual harness identity is self-observed, not provider-attested. No council/provider
call, host ledger, runtime allocation, physical/cloud action or permission answer.

An early concrete blocker or a complete implementation return goes to wN:p2.
No worker waits for another worker, selects a resolution outside the named policy,
reopens accepted audits, changes source/tracker/kit files or closes an issue.
Root verifies the returned tools and bytes, constructs serial candidates, preserves
M7's source/overlay and all accepted repairs, and records any remaining compatibility
work before asking for live integration ownership or a concrete runtime choice.

Can this be done on the VM? These are Git/text construction and refusal checks,
with no claim about an image or runtime; no VM is required or allocated.

## Handoff proof and v2 correction

P1 proof6608470639 consumed v1 SHA256
`5c4cd90baab6d8d51646e817ea404dd91a8e9e8505fdf17d6478c32f8726e7ad`.
Its report SHA256 `2f1733f701edf52de58dd704b981de7c237867a87bd63461d6a6f0c91dd99dd4`
found three finite missing routes/names. V2 supplies the exact program/receipt
paths, all four tool additions and exact recipe/unpack routes above. Root read
the actual conflicting row and pinned unpack's inline ordering/application code;
no source fix or accepted producer ran. Original proof and v1 are preserved in
the integration preparation record. Implementation correctness is not implied by
the handoff proof; each returned implementation still requires its named controls.
