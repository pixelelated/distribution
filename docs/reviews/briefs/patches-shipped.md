# T42 — patches shipped outside the kernel table (#689)

Version 2, coordinator specification, 2026-11-02. The canonical slice is
`patches-shipped`. The informal `patches-rest` name is not an ID. This brief
is a specification for the existing T5 session; execution begins only after
the stranger proof, corrected version, criteria and explicit dispatch.

## 1. Identity

M6.P2, area epic #1054, slice #689. Local depth under plan § 6c and
D-WORKFLOW-184: one actual reader, reviewers `[]`, no council/provider call.
Executor: existing `m6-t5-build-engine`, wN:p7, Codex / GPT-6-Astra / xhigh,
session `01a19d12-3d7a-7642-9108-ae06a719cdd7` (record its own observed
footer and preserve earlier T38 identity). T38 #685 is accepted, not reopened.

Branch `feature/m6-patches-shipped-689`; worktree
`/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689`,
created by the coordinator from the published dispatch commit. The dispatch
comment names its full seed hash. Use absolute workdirs; never the pane's
historical build-engine launch tree. No ES worktree is needed.

Source baseline for these inputs:
`b6332dbc13f5929f05ec5ba23c44285c5ee56b38`. P1 source:
`2174265e9cc1b248c0fbe27fa101875984d46d6b`; fixed upstream comparison:
`651150fc88`; merge base `c445081a59518f37d9776e5412dd7b14910696f7`.
The dispatch seed must have identical native path modes/blobs and selectors;
a changed input is a coordinator blocker, never silently re-cut membership.

## 2. Scope and runnable membership

Own exactly 384 provenance rows / 71,387 logical Git-blob lines, all
vendor-carried patch paths: 379 shipped, five test; 380 regular files and
four symlinks. Newline bytes are 71,378. Following each symlink per selected
path gives 71,477 logical lines, a different quantity. There are no native
configuration rows. Twelve paths / 498 lines are `tier_note: fork-written`,
including Dolphin's `018-nogui-achievements-lifecycle.patch`; read all twelve
line by line. Zero `fork-own` does not mean zero fork-written changes.

The residual selector is evaluated after explicit owners, not a broad
non-kernel glob. The exact path-list SHA256 is
`91e980f455611fa81bc84c8ff5548abd05437452d02038cc5595f5c1521e5f07`.
There are 172 package-prefix groups, 188 immediate directories and 13 exact
reachable_by sets (definitions and all rows in the retained report).
Three roots: packages 79/4,936; project packages 302/66,306; project patches
3/145 (paths/logical lines). These are survey facts, not an executed build
plan or runtime coverage claim.

D-WORKFLOW-225 records this ownership and method. A second, separate population is T40's **50 inherited comparisons / 26
overrides**. Use the exact retained `t42-inherited/leads.tsv` keyed by
shadowed path and override. Exclude its other 24 rows: two strict duplicates,
four symlink-applied and eighteen carried another way. Never add the 50 to
the 384 coverage denominator. Recipe owners: T8 #655 43/22, T22 #669 6/3,
T27 #674 1/1 (leads/overrides). Their accepted recipe audit is context, not
an answer to adoption.

Boundaries: T41 keeps its 107 rows, including the four H700 U-Boot patches
and one firmware patch; recipe owners are T27 and T11. T42's inherited SWIG
question concerns both DDR3/DDR4 v2026.01 source recipes, not wrapper 1.0.
T3 retains 21 RetroArch patch rows, T17 retains 18 RAOfflineProxy rows,
T11/T27 retain their device configurations. T43 retains its 432 path rows.
The MangoHud SM8550 member symlink points to a 37-line T43 SM8750 referent:
read that referent as context, without transferring path ownership. The
other three symlinks share vitaquake2's 19-line member referent. Retain link
mode, literal target and resolved source identity separately.

Run from this repository or a proof clone containing the coordinator files:

```bash
set -eu
export LC_ALL=C
SOURCE_REF=b6332dbc13f5929f05ec5ba23c44285c5ee56b38
INPUT_HELPER=docs/qa-logs/2026-11-02-m6-resume/t42-brief-inputs.py
INPUT_OUT=$(mktemp -d /tmp/m6-t42-inputs.XXXXXX)
python3 "$INPUT_HELPER" --repo "$PWD" --ref "$SOURCE_REF" --out "$INPUT_OUT/source"
python3 "$INPUT_HELPER" --repo "$PWD" --ref HEAD --out "$INPUT_OUT/seed"
```

This creates only small JSON/text inputs; no checkout or source archive goes
under /tmp. The helper uses five inspected pure selectors from P1 via AST,
then git-show/ls-tree reads. It never invokes renovation-inventory's CLI,
config sourcing or plan execution. Its successful summary reports 384,
71387, 71378, 3809748 bytes, 380/4, 12/498 and reach 379/5. The summary also binds all six selector/input files and the four referent
identities against P1. Compare source and seed summary ignoring only `ref`;
compare `symlinks.json` byte-for-byte too. Save commands, exact outputs, hashes and
exit codes under Stage A. A numerical delta is explained, not guessed; an
unexpected source/selector identity is a stop. The proof already re-derived
these figures at the source baseline; execution establishes the seed.

## 3. Read first and research sequence

Read the current coordinator rules, this brief, the complete #689 thread,
#1054's scope and `docs/reviews/plan-for-the-plan.md` §§ 4–8. Rules:
`engineering-practices.md`, `packaging-and-patches.md`, `worktrees.md`,
`issue-tracking.md`, `adversarial-council.md`, `decision-register.md`,
`ceremonies.md`, `upgrade-and-install.md` and `vm-first.md`. This coordinator
is newer than next; no refresh merge just to read its rules. Read
`.claude/skills/code-auditor/SKILL.md` and its Local/Issue-depth methodology;
record actual reader identity rather than copying the old Anthropic default.

Settled rows: D-WORKFLOW-184/187/188/189 (depth, no release gate, order and
planning owner), D-WORKFLOW-209 (no removal), D-WORKFLOW-221 (T41 boundary),
D-WORKFLOW-222 (normal application authority) and the T42 ownership row in
the dispatch. No source or recipe fix follows from owning a comparison.

Retained planning inputs at coordinator b6332dbc13:
`docs/qa-logs/2026-11-02-m6-resume/t42-membership/{report.md,reproduce.py,result.txt,verify-supplement.py}`
and `t42-inherited/{report.txt,leads.tsv,counts.json,ownership-table.md}`.
The scripts' old /tmp paths in historical reports are provenance; use the
committed copies. Do not rerun accepted T40/T8/T22/T27 audits. Read their
named immutable evidence after writing this slice's own first analysis:
T40 `88a648da0d` 02/05, T8 `f50a031158` q4-table, T22 `cbab6483dc` 02/05,
T27 `0ac98afe43` 02/05. The reports give full paths and acceptance links.
Those folders are absent from the coordinator tree; status.md is not their
acceptance source.

Inspect `scripts/unpack`, `config/functions` and the actual package recipe
resolution/patch-directory branches by source read. Preserve C order and
architecture-specific selection; `PATCH_ARCH=x86` is not `x86_64`.
Read the existing class-removal and adjacent work before proposing new work:
#1048/#346, #1056, #1071, #1072, #1104, #585, #563/#559. #997 is a test
identity/shimming bug, not the owner of a busybox version bump.

## 4. Questions and required tables

Q1 modernization: each native patch's target interfaces and conventions,
known replacements in the pinned source and the reason it is still carried. Q2 standards: origin, header claims, target,
backport and licensing attribution without a new legal opinion. Q3 defects:
a trace from exact patch/source lines to consequence; a patch applying is
not proof that its code is correct. Q4 currency: compare each selected path
and recipe pin against fixed 651150fc88; record absorbed/moved/changed claims
with whole-hunk or whole-patch evidence. Q5 efficiency: record source-visible runtime-cost implications and the
explicit absence of new boot, memory or player-step measurements; route any
needed measurement to its owner. This table makes no runtime-efficiency PASS
claim. Q6 dead ends: selected reach, symlinks, duplicate/contextual counterparts
and removal ownership. Q7 clarity and structure: missing/ambiguous header
provenance, duplication and carrying reasons. Both time-to-play numbers are untouched by this source read.

`02-forward-audit.md` has a native **Provenance** table with 384 unique rows:
path, Git mode/link target, inventory lines, reachable plans, origin/header
attribution, target version, selected recipe and full pin per plan, patch
order/context, application status and receipt, upstream status/evidence,
backport status, carrying reason, disposition and owner. No empty cell:
`unknown` or `open item: <specific missing evidence>` is honest. A dated
header is a claim, not verified upstream integration. Native disposition is
one of keep, upstream-changed, upstream-moved, superseded-at-pin, bug,
#585, inherited, or open-item; every non-keep needs its evidence and owner.
Coverage is a separate 384-row exact membership table with what was read,
not a claim to line-by-line review of 71,387 lines.

**Inherited comparisons** has exactly 50 rows, keyed by original shadowed
path + override: prior recipe owner, actual target pin(s), architecture and
feature relevance, generic patch intent, counterpart/absorbed source evidence,
prior base-merge disposition, conclusion and remaining owner. Conclusions:
already-carried, absorbed-at-pin, not-applicable-with-reason,
change-needed-with-trace, or unresolved-with-specific-evidence-needed.
No counterpart does not itself prove a missing fix. Do not collapse glibc's
seven, ffmpeg's seven, bluez's seven or systemd's three into a group verdict.
Compare the busybox and util-linux upstream additions named by T22, then
answer util-linux's gettext question separately. Systemd design collisions
remain #1104. Record H700 SWIG against both real source consumers.

**Fork-written reading** has twelve rows with all 498 lines accounted for,
change intent, owner, source trace, prior evidence and contribution status.
Keep upstream credits; draft any #585 line here, never send it. There is no
external web/provider verification budget in this table pass: mark external
claims unverified rather than implying linked material was read.

## 5. Evidence floor and safe source checks

Can this be done on the VM? No — provenance, selection and application are
facts about source bytes. Runtime effects, installed images and physical
facts remain with their owning slices. No guest or compile slot is requested.

Source comparison uses immutable Git reads. For an application claim, first
establish the selected source pin, archive SHA256, exact recipe resolution,
patch stack and feature/architecture selection without executing recipes.
Only already-cached sources under `/workspace/cache/rocknix-sources/` may be
used. A cache miss, symbolic pin that cannot be resolved statically or unknown
stack becomes an explicit open item with the missing input; never fetch,
source config/options or execute scripts/unpack to fill it.

Application checks, where inputs are established, may extract only the
needed safe source members under `/workspace/tmp/m6-t42/`. Inspect member
names, reject absolute/parent traversal and escaping symlinks, verify the
recipe hash and sidecar against archive bytes, and account for patch-created
files. Never extract into the repository or /tmp. No archive is trusted by
filename alone. Keep each package/plan stack separate; a selected symlink
uses the resolved immutable referent, while its coverage identity stays the
link path. Record unselected same-package siblings needed by a real stack as
context, not extra native members.

Match the actual `scripts/unpack:191–196` backend. Ordinary patches are
rendered with the statically established `TARGET_CPU` and `DEVICE` values
before application; preserve both literal and rendered bytes/hashes plus the
per-plan values. Fourteen native path identities require DEVICE rendering
(eleven regular members and three vitaquake2 links). A successful raw-patch
application is not a shipped-input proof. Unknown values remain open items.
Read post_unpack/pre_patch source transformations and patches skipped by the
recipe; prove the actual pre-patch input or record why it is unavailable.
Never execute arbitrary recipe functions to manufacture that state.

Use D-WORKFLOW-222: diagnostic `patch --dry-run` and complete normal
`patch -p1 -N --batch` use the same rendered bytes on equivalent copies of the
successful prefix; normal rc governs promotion. Binary/rename triggers use
the build engine's `git apply` semantics, with a check diagnostic and complete
application on an isolated candidate, explicit backend receipts, safe relative
paths and cwd confinement. No `--unsafe-paths` authority is inferred. No native
member matched those triggers in the proof; context siblings still require
classification. Unsupported or unsafe backend inputs remain open items. Persist argv, tool version, locale, wall time,
rc, stdout/stderr hashes, source/patch/input/output hashes and order per row.
A failed candidate is not promoted, and successors are blocked without
invented results. Classify applies / offset / fuzz / fails / blocked / open
item explicitly. Do not describe a context-only substring match as whole
supersession. Prove a partial-failure/non-promotion fixture before trusting
a new runner; reuse T41's method, not its results for different sources.

A small source-only run census precedes each package group. No build,
compiler, oldconfig, package install, image, guest, device/cloud operation,
network fetch, private held read or host-ledger write. No existing source,
recipe, patch, config, symlink, generator, register, rule or ledger is edited.
Audit-local tools and receipts alone may be written, plus the lane pointer,
work-log entry/index and retrospective.

## 6. Outputs and execution stages

Audit folder: `docs/audits/2026_11_02-epic-m6-patches-shipped/`.

A: 00-running-log, 01-research-notes with the scope, stage-a/ input/output
receipts, source equality and safety census. Establish the Local lint
positive/negative capability with a tiny isolated fixture, actual identity
and D-WORKFLOW-184, never replay an accepted audit. Report A, then continue
B under this dispatch if the immutable inputs match; a report is not another
approval relay. A mismatch is an early blocker.

B: 02-forward-audit, 03-retrospective, 04-analysis; all native, inherited,
fork-written, symlink, currency and application/open-item tables with raw
receipts under stage-b/. Write first observations before comparison with
prior audit verdicts. No runtime claim. Report a substantive checkpoint and
continue C when the declared scope and evidence floor are met.

C: 05-punch-list, tools/ generator/validators and fail-first controls,
second-opinions/review-plan.json (Local, actual primary, empty reviewers,
tier_exception D-WORKFLOW-184 and reason), stage-c/. Generated tables assert
exact native and inherited populations, byte/mode identity, no missing/extra
paths, nonempty cells, valid owner/disposition and receipt links. Negative
controls remove a native row, duplicate an inherited key, alter a symlink
referent identity and replace a known header with a fabricated attribution;
each must fail its own assertion. A missing input must remain unresolved,
never be converted to a PASS. Run pre-issue lint with its literal PASS line.

D: file the audit child under #689/M6 with the actual finding count and YAML
punch_index, each item's question/category/severity/ladder/next mechanism,
Already written and VM answer. File actual defects as reactive bug issues
with trace, no milestone/parent; avoid duplicates of existing owners. Write
06-audit-summary and 07-questions-for-the-maintainer, issue readbacks and
checks. Questions arise from actual unresolved choices; do not manufacture
a mandatory preference if all outcomes have named owners. Post one clean
published D checkpoint, then pause for the coordinator's stream disposition.
No product changes or removals are authorized at any stage of this brief.

After coordinator disposition, E records the allowed routes, F verifies
Phase-7 outcomes and resolution lint, G writes the final retro at
`docs/retros/<date>-m6-patches-shipped.md`, H posts one final hand-back.
Source-changing remediation, if any, requires its own owning slice/brief.

## 7. Acceptance contract

The coordinator replaces #689's generated criteria with these observations
before dispatch. These are final slice criteria, not claims made at A.

1. 00–07, stages A–D, tools/ and a one-file Local second-opinions directory exist with the declared evidence; no guest-cycle or build artifact.
2. Native membership is exactly 384 paths / 71,387 logical blob lines, newline/mode/symlink quantities separated, and the seed/source/P1 mode/blob comparisons pass.
3. Provenance and coverage each contain the exact 384 keys, with nonempty required fields and a source/receipt for every positive claim.
4. The twelve fork-written patches / 498 lines have a complete line-by-line reading record, including Dolphin, and attributed contribution/ownership dispositions.
5. Four symlinks retain link and referent identities; T43's MangoHud referent remains context and all explicit slice boundaries remain disjoint.
6. Inherited comparisons contain exactly the 50 frozen keys / 26 overrides, preserve the 24 exclusions and distinguish accepted recipe context from patch adoption.
7. All 50 feature/architecture/pin questions have evidence-backed conclusions or specific unresolved inputs with named owners; H700 targets both real source recipes, systemd collisions retain #1104.
8. Currency compares against fixed 651150fc88 and the fixed base, with source claims distinguished from linked but unread upstream claims; no fetch or moving-ref assumption.
9. Every application claim names its proved source pin, safe extraction, stack/order, literal/rendered patch and tree hashes, selected values/backend, normal/diagnostic receipts and classification; missing inputs remain open items. A partial-failure guard rejects promotion and blocks successors.
10. The asserted table generator's four negative controls fail before its positive output passes; counts by disposition and status sum to their own populations.
11. 04 answers Q1–Q7 with Q5's explicit measurement limits; 03 carries conformance, interactions and refutation; matching classified proof and running-log entries state their limits.
12. review-plan.json records the actual reader/lab/identity source, reviewers [], Local tier exception and historical identity honestly; no external review claim.
13. Pre-issue lint passes before D; final resolution lint passes normally and with the audit issue; every punch row has a Phase-7 outcome with evidence/owner.
14. Every bug has trace, Already written, VM rationale and observable criterion; issue checker returns 0 fail; unresolved bugs retain their actual state.
15. No lane commit changes native/inherited source paths, recipes, configs, tools/scripts, rules, registers or survey ledgers. Tree-diff and commit-path guards fail on a planted source edit in a disposable fixture.
16. All inherited and contribution rows name their owners and exact action; #585 lines are drafts never sent, class removal stays #1048/#346.
17. The execution census shows no build, guest, device/cloud, config sourcing, fetch or host-ledger write. Source scratch is retained until acceptance and retired only at H under its owned path.
18. Rules/register/index/ceremony/forbidden/hooks checks and the audit issue checks pass; normal branch/push checks are retained with actual exits, never pre-filled receipts.
19. Final retro states outcomes, friction, next owners and untouched time-to-play numbers; the hand-back names one clean published tip and actual artifact paths.
20. reviewed-at/fixed-at in #689 match the immutable read and final source-preserving tip; the coordinator verifies the simulated integration and records acceptance. Slice closure/status waits for its actual integration convention.

## 8. Stops and delivery

The dispatch authorizes A through D continuously, with early-blocker and
substantive checkpoint updates, then the defined D disposition gate. Do not
stop for routine successful stage boundaries. Stop on an immutable-input
mismatch, unsafe/unknown action outside this scope, failed required proof,
explicit owner pause or completed D hand-back. A missing optional source
archive is a documented open item, not permission to download it or invent
an application. A blocked predicate reports the exact command/input and owner.

## 9. Ceremonies and record custody

The coordinator writes the T42 ownership row and area-futro kickoff addendum;
the lane reads them from the immutable dispatch commit. No competing planning
or acceptance owner. Add dated work-log entries and update the index, capture
friction when it occurs, preserve all historical records. Commit only named
audit/record paths, Refs #689, actual co-author identity, no auto-close keyword.
Never edit a live producer or write another owner's completion receipt.
Use quoted heredocs/file APIs for prose and locale C for deterministic reads.

## 10. Coordinator hand-back read

Read #689's criteria against actual artifacts, raw source/hash/normal-output
receipts, all populations and negative-control results. Read the issue
outcomes, lint, protected-source diff, actual identity, final retro and
published SHA. A report alone is not acceptance. Reuse accepted evidence;
rerun only newly changed gates or a concrete unresolved predicate, not whole
historical stages. Coordinator performs integration in the milestone order,
keeps original read hashes and routes remaining actions to their named owners.

## Version 2 — stranger-proof corrections

The fresh-context reader ran the literal membership block from a local
shared-object scratch clone within ten shell invocations. Its report is
`docs/qa-logs/2026-11-02-m6-resume/t42-brief-proof/report.md`, SHA256
`82f55d29545063ec3fbb5eb8b37c45820bfcccf5e900cbf9e05463e8fb475d90`.
The proof establishes startability and source facts, not application or audit
acceptance; no individual cached archive has been qualified by the coordinator.

1. Corrected Q1/Q5/Q6/Q7 to the actual renovation questions. Q5 records missing
   runtime measurements; it does not silently exclude efficiency.
2. Required the build's rendered patch bytes, static variable values and hashes
   for ordinary patches, plus actual backend and pre-patch input semantics.
   Unknown hook or substitution inputs stay explicit open items.
3. The helper now refuses any selector/input-file drift and every referent
   mode/blob drift against P1, including the out-of-slice MangoHud target.
   The summary binds those identities, not just native membership.

The coordinator also corrects #1054's area-total criterion: its four tables
own 1,701 rows / 758,285 lines. The other explicit owners hold 41 rows /
19,256 lines, giving the unchanged 1,742 / 777,541 area total. No membership
or owner changes. Published dispatch provides the exact seed and final helper
identity; the future seed is checked independently of this baseline proof.

## Stage-D disposition — 2026-11-02

D-WORKFLOW-230 records the accepted bounded D packet at `d37670de318eb428604e4442f95defe10eade173` and the records-only E–H disposition in `docs/qa-logs/2026-11-02-m6-resume/t42-stage-d-disposition.md`. The live #689 comment explicitly dispatches it. The PPSSPP bug remains open for a separately scoped implementation; source application limitations and inherited inputs retain their owners. New final records execute their checks; accepted producers are not replayed. No product behavior or source scope changes.
