# Research notes — M7 P4 fixes (#383)

**Auditor:** code-auditor skill
**Date:** 2026-10-06
**Subject:** independent Milestone-tier fixes review
**Spec:** M7 / #383 and its owning issues, scoped release-readiness record.

## Running notes

Phase0 established the qualified UI prerequisite and immutable product inputs.
Phase1 research is next; no acceptance verdict or external review is complete.

## Prior-audit provenance map

Pending primary-source enumeration; preserve per-AC verdict sequestration.

## Tier B coverage

Current UI prerequisite: `docs/qa-logs/2026-10-06-ra-ui/visual-review.json` maps
all23 frames to original PNG hashes. Broader in-scope visual proofs will be
mapped during research; this entry does not grade their acceptance criteria.

## Scope from primary #383 (read07:06UTC)

The four exact parent criteria are retained in inputs/issues/383.md under
Ordered acceptance criteria. They span cloud actor/predecessor recovery,
archive/root/listing fixes, proxy/dependency/identity refresh, clean+RC2 upgrade,
VM/pair/visual/timing proof and this independent review. They require checking
owning issue criteria, not merely counting closed issues. H700 and physical/P5
publication are subsequent phases. Source helpers will map the constituent
criteria and artifacts; the orchestrator will re-read every verdict-supporting
source and execute available checks.

Captured110 M7 issue metadata records;107 issue bodies exclude prior audit
issues375/382/411. Current #465 is closed after publication. No acceptance
criterion has an independent audit verdict yet.

### Scope binding and first reconciliation observation — 2026-10-06T07:11:05.669640+00:00

Directly read prior375 research header only (no answer key): its qualified run101
baseline is distro b2378d9c33196f24066f1bcd233e14fa88211001 and ES
e108699ea313ecd5ec64b4310a4ea665e05ca19f. The current frozen target is
7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2 / ESf6f0c134212bc696f2f6a747c8d390a588f2f0ce.
The old prior notes distinguish image from newer host harness; repeat that check
for each retained proof. Current scope is P1–P3 remediation and P4 verification,
not the deferred physical/publication contract sections of344.

M7's top paragraph accurately records P4 started, but a later **Current/next**
paragraph still says UI outstanding and noP4; its VM question likewise says
remaining UI proof. Canonical checkpoint also predates audit start. These are
tracking reconciliation defects, not product failures; correct without altering
the snapshotted spec or expanding runtime gates.

Phase1.4.5 read-only research helpers are mapping cloud, proxy/dependencies,
and identity/VM/infra sources. Helpers supply leads only; root performs all
commands and re-reads all facts supporting a verdict. Two completed threads
were reused after a second new spawn hit the agent thread limit. No reviewer
seat or fresh-session independence is attributed to these helpers.

### Primary retro, futro and retained-proof boundaries

Read the entire 2026-10-02 cloud-runs95–101 retro and remediation futro.
The retro intentionally subsumed its duplicate Step2.5 into prior375. Its
five pattern→guard mappings concern folder classification, source-derived
defaults, independently reset guest cases, visible card lifetime, and criterion
reconciliation. Its later delivery receipt links actor-case-map, promoted
runner, and current visual artifacts, without declaring every image gate done.
The futro binds tests→fixes→combined image→independent review, and flags
writer-shaped archives, empty settings-only roots, explicit empty content,
unknown-vs-absent provider states and card lifetime as adversarial priorities.

Read all 2026-10-05-p3-reconciliation/README.md. The focused boundary owner
actually ran36 cases on replacement10, including literal layout1→2 and nine
fault/retry sequences with a distinct second guest. It deliberately retains
replacement09 UI/upgrade/archive proofs as09 evidence. The directory includes
pre-run gap inventory and a superseding completion section; don't treat either
summary as raw evidence. Source equality from09→10 and10→14 must be checked.

Git diff baseline→frozen product/build paths spans86 files,2165 additions and
1012 deletions. It includes rclone migration/archive/content guards, proxy
refresh/consent, dependencies, Sway/virgl resource cleanup, identity/reporting,
manual updater, splash/theme, LED quirks and build guards. The council harness
changes under scripts are audit tooling, not shipped image payload.

### Primary source and evidence-continuity inventory

Ran `git diff --quiet 7afa9efcfc0 -- projects packages distributions config
scripts/build scripts/image scripts/install`: rc0. Current product reads thus
match the frozen target for those paths. ES checkout HEAD is exactly
f6f0c134212bc696f2f6a747c8d390a588f2f0ce; baseline→current ES delta spans18
files (including rules/tests),722 additions/25 removals. Stored the complete
product/build diff and ES product diff under inputs/ for reproducible review.

`inputs/criterion-inventory.json` mechanically preserves455 raw checkbox lines
from107 issue bodies, including section headings and exact line numbers. This
is an enumeration, not455 current scoped acceptance criteria: histories,
deferred P5 criteria and superseded text need explicit disposition. No checkbox
state is used as proof. The live spec snapshot is immutable; later reconciled
tracker bodies are saved separately.

Directly read candidate-product-delta.json:09→10 changes only the GENERIC_X64
wrapper, service drop-in and README. Directly read current sign-in continuity:
14 installed cloud-signin-window hashfc9a3473 and cloud_oauth hashc9982e28
match prior10, with CHASSIS=handset. This establishes those named bytes only;
the rest of the carried runtime proof needs source/dependency mapping.

Prior410 research header scopes a separate host privilege-boundary issue:
Codex/OpenAI plus Fable5.1/xhigh, one refutation call;30 initial/35 final tests
and retained negative memory guard. Its scope excludes M7.P4 and image review.
No prior AC verdicts or reviewer output bodies were opened.

### Custody recheck — 2026-10-06T07:13:51.352071+00:00

UI SHA256SUMS:302/302 rc0; manifest-addressed bundle verify:rc0,19files.
An audit-local input reader flagged seven symlink mismatches because
Path.readlink converted the raw target to a Path and dropped a trailing slash.
Direct os.readlink comparison shows all seven exactly match the manifest.
All6550 product and207 QA hashes matched. The first failure is retained;
use the existing frozen verify-inputs.py, which correctly uses os.readlink,
to independently complete custody verification. This is a reader error, not
a candidate/source mutation.

Directly read runtime12 timing comparison: five-sample medians legacy269ms /
current245ms, difference24ms against unchanged30ms, zero migration journal
delta, source12a231698b70a8b83eb9d1fd1bc593f4507313030635a6750392f5fd19130a03.
It remains a09 execution;14 smoke cannot replace that scope. Direct archive
selector read confirms first nonempty identity directory wins before caller
label filtering; Phase2 must compare mixed-label fixtures and intended
current→legacy→previous→flat precedence before calling it a defect.

### Verified custody and complete helper handoff

The canonical frozen verify-inputs.py ran from replacement14 with its exact ES
checkout:rc0. It verifies6550 product files,207 QA files,180 raw symlink targets,
exact distro/ES heads, clean ES source and bundle input equality. Receipt is
evidence/frozen-inputs-canonical.json. All19 immutable candidate files and302
UI evidence hashes verify. The superseded audit-local reader failure is retained.

Fresh git comparison recorded in evidence/candidate-product-continuity.json:
09→10 only changes the GENERIC_X64 renderer wrapper/drop-in/README;10→14 only
changes proxy package, coupled libchdr recipe, consent patch019 and ctl. Cloud
source and ES inputs are unchanged across these boundaries. This is a source
continuity fact, not an automatic runtime or binary-equivalence verdict.

All three research helpers completed. Their detailed path maps, AC locations
and coverage cautions are saved in inputs/research-leads.md. They are labelled
as leads, never evidence or extra model perspectives. Primary rereading is
still required before each verdict. No prior AC answer key was opened.

M7 current paragraph and phase table are reconciled with exact live readback
under inputs/tracker-reconciliation/. The original spec snapshot remains
unchanged. #383 owns this in-progress review; Phase6 will create its audit/
punch-list issue after the required phases. No early audit completion marker
is added, and the existing overdue-audit ceremony remains outstanding.

## Research checkpoint — Phase1 still in progress

Planned: four ordered gates (regression coverage, fixes, exact combined build
and VM proof, independent fixes review). Scope crosses cloud/state, proxy,
identity/VM and release-input boundaries; physical/publication phases remain
separate.107 primary bodies,455 raw checkbox lines and both source deltas are
captured. Prior375 and410 provenance is scoped without importing verdicts.

Remaining Phase1 work: read each owning primary body/source and resolve the
current-versus-historical criterion inventory; map applicable rule/decision
and blindspot obligations; finish prior-review coverage/TierB provenance.
Then write each Phase2 criterion's exact text, primary evidence, executable
check and attempted refutation before assigning any verdict. Only after all
independent grades may Phase2.5 open prior answer keys. Phases3/4/4.5 then
precede Fable5.1/xhigh blind and refutation calls through the Facilitator.

Priority research cautions are archive directory-vs-label selection, actual
kill-vs-injected-fault coverage, installed byte continuity, the updater network
capture criterion, future same-name update acceptance, unchanged-source
performance evidence, P5/public-docs boundaries and watcher delivery scope.
None has yet been promoted to a confirmed audit finding.

### Resumed primary research

Read the exact current acceptance text for the parent383 and cloud/archive/
identity/proxy owning issues from the preserved inventory; historical344
contract sections explicitly place physical/publication work after software
qualification. Re-read migration/privacy/agent-first rules and the existing
durable runner's launch/monitor contract. The archive selector's directory
precedence and label policy remain a research question, not a proven defect.
The #466 continuity correction governs execution only; product7afa9efcfc0 and
all review scope/depth inputs remain frozen.

### 2026-10-06T14:56:36.361260+00:00 — archive directory precedence intent verified

Read cloud_restore2030–2170, cloud_scan190–247, shared selector and D-CLOUD-067/
068. Directory precedence current→legacy→previous→flat is explicit persisted
identity policy, not an accidental newest-global search. The console chooses
its own label inside the selected directory, then deliberately falls back to
NEWEST with a warning; the UI's MINE gate is separate. A foreign archive in
the current directory suppressing a compatible archive in an older directory
is therefore not independently a defect without contradicting that policy.
Retain mixed-label controls and verify scan/restore agree; do not broaden
recursive discovery or silently restore other device folders.

Read remaining exact cloud/provider/proxy/numbered-migration criteria from
inputs for351–365. Their constraints distinguish five-sample timing from smoke,
actual second guests from reset configurations, and public UA from hosted
authentication. Physical/publication and D-QA-058 optional accounts retain
separate scope. The live host check has passed menu-map and schema and is
exercising independently reset migration states; no grade from a running job.

### 2026-10-06T15:00:01.961064+00:00 — migration and bounded content transfer source read

Read cloud_migrate_layout key-presence/backup-pointer helpers100–150, pointer/
merge transitions660–795, strict marker and JSON recovery validation960–1305,
and copy/check/delete relocation480–615. Explicit empty content roots differ
from absent keys; marker bytes accept only literal1/2; failed listing is not
absence; recovery paths/config identity are validated before operations.
Copy completion and verification precede pointer movement and listed-source
deletion. Need complete494–515/615–655 read before a relocation verdict.
Read all cloud_content_transfer: high-water progress, bounded idle expiry,
scoped traps and explicit rclone/tee PID teardown avoid timeout stamp success.
These are research observations; actor/guest negative controls remain required.

Completed the relocation read at494–515/615–655: same-folder moves are
refused before writes; a destination nested under source is excluded from its
own input list; successful merge verification requires every listed old name
to exist at destination, with differing bytes intentionally preserved on a
replacement shelf. Pointer readback precedes listed-source deletion. The
negative actor cases must prove those ordering guards, not only final files.

### 2026-10-06T15:02:33.042637+00:00 — scope and inherited failure modes

Read exact111-style cloud/state owning criteria (320,349–356,363–366,376/377/
379/380/381,390/391/392,401/407/421,429/430/462) from the captured primary
bodies. They include historical name wording superseded by D-WORKFLOW-144,
public-site delivery and physical frames that remain later gates. Do not drop
those clauses from the final coverage table or count all455 raw lines as
current product acceptance. Read blindspot register initial table and35–42: real
backend failure semantics, source-derived defaults, positive/negative controls,
actual target tools, native-size surfaces, operation ownership and current
runtime state govern the proof. The skill summary of twelve blindspots is
stale; the actual register has entries through73 and is authoritative.

### 2026-10-06T15:05:06.996906+00:00 — cross-system criteria and Tier B inventory

Read exact owning acceptance text for proxy/dependencies, identity/VM, memory,
LED software, native input preservation and UI (310/327/332/337/357/359/361/
362/383/384/386/408/409/414/419/424/426/433/436/447/451/452/454/455/457/465).
Read344 contract criteria with section names: P2b/P3/P4 are later hardware/
publication gates, P5/P6 post-release; neither is the current executionP4.
No current telemetry/upgrade claim can be justified by the old brand words
only; network capture and future-name acceptance remain evidence leads.

Read blindspots43–73, especially exact-run logs, real loaded-page memory,
renderer/surface identity, installed dependency provenance, controlled failure
and source-to-fixture drift. Their relevance will be graded in Phase3, not
assumed from a table count. Earlier entries17–24 were reread for the whole
update pipeline, file-level tier ownership and strict false/unknown probes.

Primary Tier B manifests read: replacement09 guest11 maps15 UI cases/32
selected original frames; cloud-ui08 maps9 UI17/UI26 frames. Replacement10
signin14/15/16 map15 frames each; ui14 maps70 menu/Tools frames; boot05 maps
four clean/upgrade640/1280 frames. Current14 QA18 walk review maps21 selected
walk frames, with separate initial/upgrade/software/timing reviews. RA UI
qualified03 maps23 original full-panel EN/FR640/1280 frames; prior failed01/02
remain distinct. These are visual-review inputs, not new pixel inspection or
current14 executions of the09/10 flows. Primary frame/refutation checks follow
where scope changed or a flow was not covered.

### 2026-10-06T15:06:04.962491+00:00 — exact scope inventory and research summary

Read the remaining supporting host/process acceptance text. Found that the raw
checkbox inventory captured only first lines for multiline criteria; preserved
it unchanged and restored continuations from the exact issue body in
inputs/scoped-criteria.json. This is an audit-reader correction, not a product
defect. 12 criteria needed continuation lines.

The scope manifest assigns every raw criterion:261 forward criteria across51
owning product/qualification issues and344 release boundary;190 supporting
historical host/process criteria for Phase3 trust/interaction review;4 later
versioning criteria from265. Supporting dispositions are not PASS grades and
are not claims of repeating privileged cleanup or every prior build. Forward
entries will quote exact text; explicit later/historical clauses retain their
own reason, never disappearing into a green umbrella.

Prior provenance:375 is the prior cloud/release fixes baselineb2378d9c33/
ESe108699ea, with primary plus Fable blind/refutation;410 is separate privileged
host-helper review, primary plus Fable refutation. Their answers remain closed
until2.5. September29/313 is a historical source for320, not a current image
qualification. The sole October2–6 phase retro subsumes Step2.5 in375; Tier B
inputs are enumerated above. No new page-scale design review is substituted
for those existing proofs.

Planned scope: coverage first, structural fixes, qualified dependencies and
combined immutable image, then this independent cross-lab audit. Source delta
is86 product/build files and18 ES files; archived raw diffs and exact frozen
inputs bind the review. Constraints: no data loss, current compatible upstream,
ROCKNIX→pixelelated adoption, honest synthetic/runtime boundaries, target tools,
serial audit gates and no prior-answer anchoring. Red flags to refute: actual
kill versus injected failure, archive selection intent, updater network proof,
future-name update validation, exact installed continuity, timing ownership,
public docs/P5 boundaries and background delivery. Phase1 research is settled
for this scope; proceed immediately to independent Phase2 entries.

### Continued cloud proof review

Replacement14 local reports each name7afa9efcfc and the immutable bundle: WebDAV86s, SFTP73s, S3110s; completion records106/0/0 each and actual process/backend cleanup. The initial provenance UNSTARTED field is historical, superseded by terminal receipts. Focused replacement10 boundary proof uses genuinely distinct guests (boot IDs3df800d3.../aef12ea9...), but faults return operation failure; that is not itself a real mid-copy kill. Foreign-only UI hostname assertion remains a narrow evidence gap pending wider search.

### Phase2 content-location lead — requires executable confirmation

Read cloud_setup:497–566: AT_PATH counts **every directory** under a nonempty configured CONTENT_REMOTE, while AT_ROOT filters through local content directories and fallback FOUND requires ROMs/BIOS. The D proof empties the configured content folder and places Photos/Documents at the account root. It does not challenge a configured content folder containing only unrelated directories. Under #352's criterion “no ROMs/ and no known system folder,” that input appears able to report STATE=ok and suppress both fallback discovery and the chooser. This is a source-derived lead, not yet a reproduced product defect. Read GuiMenu content-location routing, perform literal/history search and an actual installed-guest negative/positive probe before disposition. Preserve the existing passing empty-folder frame as its narrower evidence.

Directly viewed original640x480 F outcome and D question/chooser/systems frames: failure names the stopped cloud with CLOSE/TRY AGAIN; the empty-folder question is clear; Documents/Photos appear as selectable cloud folders, not systems; the content page lists NES only. The D walk cancels the manual chooser rather than selecting a folder, so manual-selection/journal acceptance needs a separate receipt.

### Installed content probe confirms classification asymmetry

Fresh seven-case content-probe01 completed on exact14, no product binary changed. Controls empty-configured, genuine tiered-configured and unrelated-explicit-root pass. Unrelated configured directory returns ok and blocks a real default Content fallback; tiered explicit root returns empty. A valid legacy cloud gb directory with an empty local gb also returns empty: cloud_content_backup:430–454 lists only local folders already carrying content (has_content), so it cannot serve as the supported-system predicate for restoring onto an empty device. This is the direct cause, not a credential or VM-resource failure. Criterion failures I352-L33/L44 are recorded; explicit-root sibling is retained for Phase3 prescription verification. Four process channels rc1 and exact cleanup verified15:27:11UTC. No background worker remains.

### Marker refusal reason is lost across the script/UI boundary

Direct original UI26 future-refusal640px frame and UI26-future-script.log both say COULDN’T FIND YOUR CLOUD FOLDER. `cloud_migrate_layout::read_marker` accurately detects unsupported marker and returns application4; `cloud_scan::read_folder` discards its explanation and `why_for_rc` treats4 as rclone missing directory. Writes/marker/pointers remain protected. Criterion I356-L76 reassessed PARTIAL for this presentation defect. Earlier inferred newer-build wording was corrected immediately, with the correction retained in00/02 and ledger metadata.

### 2026-10-06T15:49:19.902967+00:00 — newly required sign-in strings have no French route

D-CLOUD-164 includes the phone close question and finishing page; cloud_oauth serves literal English and cloud-signin-window.c FINISHING_PAGE is one static English data URL. Actual installed matching bytes and EN frames establish the implementation; no French-mode guest test is claimed. Catalogue translation elsewhere cannot affect these independent processes. I351-L62 FAIL, with scoped repair/VM proof owed.

- Phase2 UI465 primary inspection: read the complete fixture’s installed Storage/flusher path, actual address removal/restoration, settings-before-ES ordering, pending checks, immutable module census and bounded outcome polling. Directly reviewed all ten qualified EN/FR640 baseline/sending/sent/dismissed/empty-repeat images: baselines and repeats are empty, both translated cards fit. Remaining1280 and refusal frames are next; no grade yet. The fixture explicitly disables background proxy scheduling and invokes the real installed flusher; it does not independently prove automatic scheduler behavior.
