# T44 — EmulationStation's vendored libraries, translations and build files (#691)

Version 1 candidate, coordinator, 2026-11-02. This is preparation while
T43 executes. A separate stranger proof, v2 corrections, live criteria and
an explicit dispatch naming both worktrees precede execution. T46 stays last.

## 1. Identity

M6.P2, interface epic #700, slice #691, canonical `es-vendored-and-data`.
Kind table; lenses reachability and package currency. Local actual primary,
reviewers [], D-WORKFLOW-184 and plan §6c; no external reviewer or council.
Intended executor: existing T2, `m6-t2-es-launch`, wN:p5, session
`01a19d12-1c5f-7022-8053-102f6a94b7fe`. Record the actual observed harness,
model and effort at execution; retain historical report identities.

The coordinator creates distribution branch `feature/m6-es-vendored-and-data-691`
in `/workspace/repos/pixelelated/distribution.worktrees/m6-es-vendored-and-data-691`
and the same branch name in ES worktree
`/home/max/Development/emulationstation-next.worktrees/m6-es-vendored-and-data-691`.
The live dispatch supplies the exact distribution seed. The ES seed is
accepted T2 `55158d2a64c69fe295fb4e67fd174424a71b1b4d`, tree
`64b90eb8cb07bdfcd690c74ff6bc980ae490657c`. Both proposed worktrees are
created only after proof; never use the historical launch checkout or
change the primary ES checkout. All A–D edits are distribution audit records.

P1 `2174265e9cc1b248c0fbe27fa101875984d46d6b` fixes ownership and survey
ES `16dbac5211eea7e70db7394372033be2be7df829`. Distribution source context
is `c348d43dddc4bddbe1055d20d37431503283b817`; the recipe still pins survey
ES. Neither that recipe nor `test/qa-integration` proves later accepted
changes were integrated. Fixed ES comparisons are fork base
`cada856d86e3115fbbf0bce09dd761b0ee8fa9fd` and upstream
`e282b05627c0d2193c19d7cc526176e047530c3d`; no moving refs.

**Baseline choice:** read the accepted T2 tree, which contains the shared
PL-024 catalogue correction required by #691 comment6375264017. Separately
read accepted later French deltas at the four companion refs in §3. They
are coverage obligations, not a synthesized integrated source. None contains
the T2 tip. No branch merge, source-copy overlay, recipe pin promotion or M7
baseline selection is authorized. Area #700 owns later integration and drift.

## 2. Scope and runnable membership

Keep **594 native survey keys** distinct from **three post-survey T2 test
additions** and **four accepted companion branch records**. This does not
recut `slices.json`. Non-rest assignments take precedence: naive603 paths
outside es-app/es-core minus nine T20 rows/2,556 lines equals594. The nine
are enumerated by the helper; no duplicate libcheevos review or ownership.

Survey facts:374,547 inventory lines;51 fork-own/543 upstream-carried;
143,710 generated CODE lines/11,989 fork-own CODE lines. Those last two
are a formula, not a table read budget or completed reading. The594 entries
are593 blobs and one gitlink:583 mode100644,10 mode100755,one160000;
543 Git-text,50 binary,zero symlinks. Git-text has374,546 logical lines and
374,530 newline bytes. The extra inventory line is the synthetic gitlink
`external/pugixml@61c944895e071872370219cadade8423dc6e04dc`, not readable
source. Do not initialize/fetch it. An empty mp3 fixture is Git-text with
zero lines; suffixes are not binary or executable classifications.

At accepted T2, the same594 keys have374,720 text logical lines,
374,704 newline bytes and40,999,100 blob bytes. Modes/kinds stay fixed;
554 native identities are unchanged and40 changed:36 catalogue/template
files and four root tests. Three added root tests total450 logical lines:
`tests/launch-play-through.py`, `tests/main-parse-args.py`,
`tests/system-scan-assets.py`. Keep these supplemental rows separate from
the594, with their existing T2 behavior owner. Survey tiers remain dated
survey facts; a mechanical later rename does not silently redefine them.

Survey groups:external334/135,991 inventory lines;locale38/158,693;
resources147/70,536;tests35/3,824;CMake15/1,496;root17/3,408;
.githooks6/526;.github2/73. Locale contains35 PO catalogues plus one POT,
and two other files. Resources contain101 text/46 binary, including eight
fonts. A filename, binary size or absence of a selected caller is not a
removal verdict. No font/image/media rendering is claimed.

The51 survey fork-own paths are46 added plus five changed. The7,134-line
doctest import is unchanged vendor content, not fork-authored code. At the
primary pin, the40 other survey fork-own CODE files contain5,017 lines;
read those and the450 supplemental test lines completely for structure,
ownership and assumptions. Read other fork-modified deltas and build/resource/
catalogue interfaces directly. Vendored bodies receive table/provenance
coverage, not an invented143,710-line semantic audit.

Run this block in one shell invocation, from the proof clone or actual
distribution worktree. ES_REPO may point to its private read-only proof
object store; execution uses the explicitly dispatched ES worktree.

```bash
set -eu
export LC_ALL=C
ES_REPO=/home/max/Development/emulationstation-next
INPUT_HELPER=docs/qa-logs/2026-11-02-m6-resume/t44-brief-inputs.py
INPUT_OUT=$(mktemp -d /tmp/m6-t44-inputs.XXXXXX)
python3 "$INPUT_HELPER" --repo "$PWD" --ref c348d43dddc4bddbe1055d20d37431503283b817 --es-repo "$ES_REPO" --out "$INPUT_OUT/source"
python3 "$INPUT_HELPER" --repo "$PWD" --ref HEAD --es-repo "$ES_REPO" --es-ref 55158d2a64c69fe295fb4e67fd174424a71b1b4d --out "$INPUT_OUT/seed"
python3 - "$INPUT_OUT" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1])
for name in ('native.json', 'additions.json', 'companions.json'):
    assert (p/'source'/name).read_bytes() == (p/'seed'/name).read_bytes(), name
a = json.loads((p/'source/summary.json').read_bytes())
b = json.loads((p/'seed/summary.json').read_bytes())
for x in (a, b):
    x.pop('distribution_ref'); x.pop('es_ref')
assert a == b
print('PASS T44 immutable input equality; native594 / additions3 / companions4')
PY
```

The helper reads Git objects, derives the non-rest-before-rest selector,
binds six P1 inputs and the distribution recipe, verifies the retained
survey manifest SHA256
`16b1da3ad4a7e4b3c7a6aadbd901c2502c940d20da697136babc27474d767965`,
and binds the entire ES seed tree to accepted T2. During execution, also
pass `--es-ref HEAD` against the actual assigned ES worktree. Any unexpected
input drift stops for the coordinator; a count with a reproducible honest
explanation is recorded as a delta, never silently substituted. Outputs
are small metadata only. Retain exact argv, times, exits and hashes in A.

## 3. Read first and research sequence

Read full #691/#700, the dispatch, plan §§4–8, order T44 and current
coordinator rules. This branch is newer than next; read current rules
without merging unrelated lane histories. Applicable rules: worktrees,
engineering-practices, issue-tracking, adversarial-council, ceremonies,
decision-register, instruction-files, vm-first, handheld-evidence and the
four ES rules. Read code-auditor's evidence floor and Local methodology;
its historical Anthropic default is not this executor's identity.
Blindspots13/47/51/75 cover artifact proof, installed/source distinction,
completed work and wrong-tree counts. D-WORKFLOW-184/187/188/189/209/225
govern Local tables, order, ownership, no removal and evidence reuse.

Preparation lives at `docs/qa-logs/2026-11-02-m6-resume/t44-preparation/`:
P1 membership report/manifests and T2 accepted-context RETURN/readbacks.
They are leads to verify from the named objects. Write first independent
provenance/build/catalogue observations before opening prior verdicts.
Then compare, without replay, the accepted owners:

| Owner | ES ref | Distribution evidence ref |
| --- | --- | --- |
| T2 #649 | 55158d2a64c69fe295fb4e67fd174424a71b1b4d | 7041b0d710363ddac7ae1b047ebae3e182548631 |
| T21 #668 | 3ae9610b0f3fb61d23eb6a2c3459ad19f962e2b1 | 82c67e99c5726e6980605790642e798c196e421c |
| T34 #681 | 52f0ff5128cf96bfcdec9082ded75347ecea11e6 | 49c6b43f2708f46c9d2f147c609d7d9f702c2557 |
| T35 #682 | b7fdb3a24c859ce91f9fd381bb0956901b8d23cb | d828355e0ac3b9c639c394adbcf9aeb65c0db22c |
| T36 #683 | 9c1bd5f093cfc1ccd42640282226b7b970442ef1 | 4127382d34db90298a9fd1e0c2ef185ad03b84ea |

PL-024 commit `a1cbc0ccd96cbd95f3355375609f71f1b50c7113` changed35 PO,
one POT and FileData.cpp:37 files/38 exact UKNOWN→UNKNOWN replacements.
The38 include en_GB msgstr; other translations are unchanged. The old
36-catalogue note and37-line log are historical errors, not authority.
T2 PL-025 adds three French entries separately. Later accepted T21/T34/T35
add6/1/1 French entries; T36 has zero outside-app/core change. Their French
files retain the old key. Enumerate exact msgid/msgstr deltas and source
call sites at each owner's pin; do not label them integrated or refile
the settled spelling defect. Every external/ identity is unchanged across
these accepted refs. Keep source-call context outside native ownership.

Root tests and hooks are native T44 table paths; tests are not authority
to reopen the behavior they exercise. `es-app/tests/**` belongs to T18;
the root fake AsyncNotification component's behavior seam still belongs
to T18. `es-core/CMakeLists.txt` belongs to T35, including its T21 test
registration context. The nine excluded libcheevos rows belong to T20;
T36's core zip_file/han sources are not external/ members. Read existing
owning issues before duplicating inherited defects. No accepted tests run.

Provenance leads to verify: doctest2.4.12 import324f9c483d9b4a11249c47888b40fb5cc691be7f;
rcheevos root12.2.1 and nested10.7.0 are distinct markers, not one version;
libretro-common has an import identity, not a proven package semver;
id3v2lib CMake2.0 versus historical README1.0 and flattened gitlink history;
NanoSVG import/update commits, not an invented release label. Pugixml is
the gitlink above while the distribution recipe sets USE_SYSTEM_PUGIXML=1.
Read root/external/locale CMake and call sites statically before making
build reachability claims. No dependency removal or compatibility claim.

## 4. Questions and tables

Q1 modernization: provenance and interfaces that need an owning update.
Q2 standards: attribution, licensing, build/test separation and catalogue
format. Q3 defects: exact trace and refutation, distinct from stale context.
Q4 currency: exact imported/current-pinned comparison, carrying reason and
dated primary upstream release evidence or a specific missing input.
Q5: no runtime efficiency audit in this provenance table; record N/A with
reason and both time-to-play quantities unmeasured. Q6 reachability: source
build/resource/catalogue consumers and unproved installed reach; no removal.
Q7 clarity: import boundaries, generated files and ownership of next action.

02 has Provenance and Coverage tables, each with594 unique native keys,
plus a separate three-row post-survey test table and four companion branch
records. Per-key columns: path/kind/mode/blob; survey tier and lines;
primary identity/lines/delta; group; origin/import/version/license evidence;
source consumer/build condition; reading coverage; currency/disposition;
specific limit; existing next owner/action and receipt. No blank evidence
cells; unknown names what is missing. Binary/gitlink rows are metadata,
never fictitious line readings. Every total must come from the actual keyed
tables and the helper's named populations.

Add a vendored-group table for libretro-common, rcheevos, id3v2lib, nanosvg,
doctest, pugixml and external/CMake integration; separate import version,
local delta, license/source marker and currently known upstream evidence.
Add35 PO coverage rows plus the POT row, including plural/context/format/
fuzzy/untranslated counts only where a retained parser establishes them.
A count is syntactic coverage, not translation quality. Companion French
entries have separate branch/source evidence and integration obligations.
Build/resource/test tables identify exact writers/readers and guarded
configurations without running CMake, hooks or asset generators.

## 5. Evidence floor and permitted checks

Can this be done on the VM? No runtime behavior is proposed: this is a
source provenance table. Any future behavior or removal proof belongs to
an owning fix brief and GENERIC_X64. No build, compiler, guest, physical,
cloud, cache/archive, device or host allocation is requested.

Allowed: immutable Git reads; static text/AST/XML/PO parsing in memory;
new audit-local metadata/assertion tools and fixtures; record lints; public
primary upstream release/license pages for dated currency comparison.
No remote Git fetch, submodule expansion, source-tree export or execution
of catalogue/update/CMake/hook/test/package/config scripts. A fetched web
page is read-only context, never permission to download source or call a
model provider. Unavailable release evidence is a precise open input.
Do not imply latest version from a local header or an unvisited URL.

Use metadata fixtures to prove five refusals: missing native key, gitlink
misrepresented as source, doctest miscredited as fork-written, omitted or
falsely integrated companion delta, and changed immutable source identity.
Each fails its own asserted condition; the complete positive passes.
Retain exact fixture inputs, generator and output hashes, argv, version,
locale, actual start/end and exit. A parser's limits and malformed-input
control accompany any derived catalogue count. No existing audit producer
or accepted test is rerun to satisfy these new table assertions.

The new evidence uses the lint's existing proof classes
tree/history/tool-run/fixture/design and matching PROOF lines. A constructed
fixture proves its mechanism, not installed effect. Before a new bug,
inspect its full existing owner, write Already written, trace/consequence/
refutation and VM rationale. Keep inherited issues with their current owners.

Write only distribution audit records/tools, lane pointer, dated log/index
and retro. ES stays exactly at its seed, with no source commit. No product,
recipe, catalogue, rule, register, survey map, host-ledger or historical-lane
edit. No private-held/credential read or another lane's permission answer.
All source/record subprocesses stay on CPUs8–23. Small text/JSON scratch
may use /tmp; no source exports or wholesale archive extraction anywhere.

## 6. Outputs and continuous stages

Audit root `docs/audits/2026_11_02-epic-m6-es-vendored-and-data/` (fixed
start-date name even if execution crosses UTC midnight).
A:00-running-log.md,01-research-notes.md,stage-a/input bindings and actual
ES/distribution seeds. Prove Local-lint positive/reviewer-count negative
with a tiny isolated fixture, then proceed. First independent observations
precede historical verdict comparison.
B:02-forward-audit.md,03-retrospective.md,04-analysis.md,stage-b/ with
the native/supplement/companion tables, full fork-code reading register,
provenance/history/consumer traces and qualified currency evidence.
C:05-punch-list.md and asserted audit-local tools/controls,stage-c/, and
one second-opinions/review-plan.json recording actual primary/lab/identity
source, Local, reviewers[] and D-WORKFLOW-184 reason. No provider call.

D: pre-issue lint with `--phase pre-issue`, then audit child of691 in M6
with actual severity/count, prioritized items and YAML question/ladder/
next mechanism/acceptance. Reactive bugs have no milestone/parent and
do not duplicate existing owners. Write06-audit-summary.md,
07-questions-for-the-maintainer.md and stage-d/exact tracker readbacks.
Ask only real unresolved choices; do not reopen recorded decisions.
Post one clean published D checkpoint and stop for root stream disposition.
A–D are continuous, with substantive updates and early concrete blockers.

After disposition: E records outcomes; F new resolution and final record
gates; G `docs/retros/<date>-m6-es-vendored-and-data.md` and exact posted
retro; H receipt-bound owned scratch retirement and clean published handback.
Keep external final commit/push/remote/status receipts bound to the actual
tip. No receipt-only commit loop, worker merge or source promotion. Marker
and audit closure wait for explicit root final acceptance.

## 7. Acceptance criteria

Root installs the final proved version in live691 before execution.

1. 00–07, stage A–D records/tools and one Local plan exist under the named audit root.
2. Helper output binds six P1 selectors/ledgers, recipe,594 native rows and the complete unchanged primary ES tree to the actual seeds.
3. Survey374547 versus text374546 and primary374720 lines, kinds/modes/gitlink and dated51/543 tiers reconcile; no synthetic source or reading claim.
4. Provenance/Coverage each contain594 unique nonempty native rows; three450-line post-survey tests and four companion branch records stay separate.
5. Nine T20 exclusions and T18/T21/T34/T35/T36/T37 behavior/build boundaries remain explicit with existing owners; no recut or duplicate bug.
6. The40 primary fork-own CODE rows/5017 lines plus450 supplemental lines have a complete reading register; doctest's7134 lines are verified unchanged import, not authored-code credit.
7. PL-024's35PO/37files/38replacements, separate T2 French additions and later6/1/1 entries have exact source evidence; no combined-tree or integrated-key claim.
8. Vendored groups bind import/mode/blob/version/license evidence and carried reasons; dual rcheevos markers, id3v2lib history and pugixml system selection are qualified correctly.
9. Catalogue/resource/build/test tables bind exact source writers/readers/conditions; any syntactic counts have parser limits, failing input and retained raw evidence.
10. Q1–Q7, conformance/doctrine/interactions/self-refutation and prior-evidence comparison are complete; current currency has dated primary evidence or a specific open input.
11. Five asserted table refusals fail and positive passes; exact program/fixture/input/output/exit bindings exist without replaying accepted producers.
12. Actual Local primary/lab/identity source and historical provenance are truthful; reviewers[] and no independent-review claim.
13. Pre-issue lint and, after disposition, both normal/issue resolution lints print their actual PASS; every punch item has an evidenced Phase-7 outcome.
14. Reactive bugs carry trace/Already written/VM rationale and observable criteria; issue checks pass and unresolved bugs remain open.
15. Whole ES seed and distribution source/rules/selector identities remain unchanged; per-commit allowed-record guard and a planted source-edit negative verify confinement.
16. Census/retirement names only receipt-bound owned scratch; no runtime/provider/host/device/cloud action, source export, accepted replay or permission relay.
17. Rules/register/index/ceremony/forbidden/hooks checks and exact tracker readbacks pass with actual exits; final publication binds the clean final tip and unchanged ES seed.
18. Posted retro and final handback retain outcomes, friction, next owners, companion-integration limits and unmeasured time-to-play.
19. reviewed-at/fixed-at bind distribution seed/final and reviewed-at-es/fixed-at-es both bind55158; a separate companion manifest names four accepted refs. Area integration remains future work.
20. Root verifies new integration/record gates and final acceptance; completion marker follows acceptance and slice closure/status follows actual ordered area integration.

## 8. Stops and delivery

Stop at mismatched immutable inputs, an uncorrectable required predicate,
out-of-scope action, explicit owner pause, published D, or authorized final H.
Missing optional currency/provenance inputs become specific open items;
they do not justify invented PASS or stopping other authorized analysis.
No execution from this candidate before explicit dispatch after T43.

## 9. Ceremonies and custody

Root retains order, baseline, ownership, brief/criteria/register and final
acceptance. The executor owns one worktree pair and its audit records.
Append actual UTC timestamped worklog; regenerate INDEX; record friction
and actual identity without changing old provenance. Use normal hooks and
Refs #691, not premature closing keywords. Producer receipts remain theirs;
root's later observations stay separate. No source fix without a stream brief.

## 10. Coordinator handback read

Reconcile exact keyed tables/accepted receipt identities against the live
criteria; read the named source/proof/owner limits rather than re-auditing
accepted stages. Run new final record/integration checks on a disposable
exact-tip merge, preserving whole log entries and regenerating INDEX.
No ES merge is implied by a distribution-record simulation. Preserve
literal failures and any narrow correction as separate evidence. Audit
closure and acceptance do not close inherited bugs or claim integrated
ES/image behavior. No baseline or upstream pin changes follow automatically.
