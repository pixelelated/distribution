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
