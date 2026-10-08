# Saved Session State

> Saved: 2026-10-08T03:51:04.961741+00:00
> Coordination branch: feature/conflict-resolution
> Repository: pixelelated/distribution

## Start here

pixelelated is an immutable handheld Linux distribution, not an app. Read
AGENTS.md and canonical `.claude/rules/` from `next`, then this checkpoint,
M7's live ordered body and issues #510/#508. Primary checkout:
`/workspace/repos/rocknix`, branch `next`; the previously published checkpoint
is `0f073485fffa9071ccb66f0d3c54a6b67a9797aa`. This final evidence/checkpoint
change is prepared from that clean baseline; read actual HEAD before working.
Coordination checkout:
`/workspace/repos/rocknix.worktrees/conflict-resolution`, branch
`feature/conflict-resolution`. It has divergent historical work:
**never merge it wholesale into next**. Use scoped commits/cherry-picks.
Prior checkpoint: `archived/saved-session-state-next-20261008T035104Z.md`.

Authorization persists for scoped implementation, parallel agents, local
commits/pushes and synthetic host/VM proof. Device/personal-cloud actions keep
their named scope. Prior SP transfer/reboot, screenshots and wake completed;
do not repeat them. No public release or new physical action is inferred.
A general continue does not answer a specific pending scope, credential or
Herdr startup question. Never print credentials or inventory personal clouds.

## Current focus and order

**Source-overlay UI qualification is complete. No build, VM, audit or UI job
is running in this lane.** Distribution is clean at
`6f89bc7cecee5972909828103689e2c7c0711c30`; ES is clean at
`4e410dc9a816cc947f16235ad2b24824b29dd84e`. Both product branches remain
local/unpushed/unintegrated; no pin changed. Source fixes #512/#513/#514
are qualified; reconcile their tracker dispositions against the published
packet rather than rerunning completed tests. Product integration remains #508.

The owner's required ES/IA/screen-content process is already published on
next: D-WORKFLOW-155/156, both agent entrypoints, es-ui-style-guide.md, and the
menu-map evidence-index schema. Every affected flow/reference and reviewed
happy/error/cancel/retry screenshot accompanies the source before completion
or pin promotion. Copy-only and script-supplied text count. Nonvisual changes
name the exercised flow and unchanged-presentation evidence. A title-map check
is not semantic screenshot coverage. ES's AGENTS.md points to these canonical
next rules, so separate ES sessions receive the same requirement.

Completed qualification:
- 21 real-rclone restore/cache controls and 30 validator controls.
- Final broad host run `20261008T021032Z-6981bf69`: 1,311 top-level PASS,
  zero failures/skips, three actual zero channels. It was a direct invocation,
  so there is no inner.rc. All owned processes exited and nine input hashes
  stayed unchanged. Harness SHA256
  `5bb88aabeb833965c9611efb6d7ccb62c3c2567b25235ac2050bf329a3e1039b`.
- Ordinary VM WebDAV and SFTP round trips: 108 PASS each, four zero channels
  each, synthetic configuration restored before retiring the original guest.
- ES #512 logic: 183 unit cases / 4,752 assertions, syntax/catalog/vocabulary.
  Later #513/#514 change only GuiMenu literal text/catalogs, with separate
  compile/link/syntax/gettext/vocabulary proof and explicit unit carry-forward.
- Final affected-flow UI index: 99 entries, 89 reviewed screenshots, nine
  rejected screenshots retained, one pending item: CF10 assembled firmware
  clean/public ROCKNIX adoption. EN/FR at640×480 and1280×800 are represented;
  no full locale/panel permutation claim. Final index SHA256
  `9428ccff1267bc255807f4aa1dd0971054ced4e1360569461046c26df9e99768`.

Current order:
1. **#510:** resolve the still-unanswered release-scope question: ship current
   checks/create/manual instructions and defer automatic save organization,
   or include a specifically defined small-file repair. The validator direction
   is settled; no generic safe relocation API exists and no such fix is claimed.
   Do not silently mark this criterion complete or resurrect migration.
2. **#508:** after that scope decision, integrate the qualified product source
   and full pins, keeping canonical references/evidence with it. Current
   source-overlay proof is done; actual public ROCKNIX/clean adoption and
   assembled firmware inclusion remain separate gates. No new device build yet.
3. **#507:** freeze and independently audit the post-candidate16 P5 delta.
   No audit/external transfer has started. Use code-auditor's serial stages
   and the Facilitator. Old Fable approval is not a blanket new transfer;
   accepted candidate16/#471 review must not be replayed.
4. Bind qualified inputs into selected firmware, then source/licence/release
   staging and named physical smoke. No RC designation/publication yet.

M7 and #508/#510 hold this order. Reconcile their final evidence/owner state
with this checkpoint after publication. The separate website lane #511 adds
no firmware gate. Do not rerun the completed full host/ordinary VM suites
without a changed input, failure or concrete unresolved concern.

## Current source and ownership

### Distribution — #508/#510

`/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders`, branch
feature/m7-manual-cloud-folders. Local commits, unpushed/unintegrated:
- e484380a/3268015c: earlier manual setup removal/readback corrections.
- 2cffff3f38: selected-root-only content restore; failed partial listings
  refuse; scan completion binds run/config/mode/output; public key conversion
  no longer infers CONTENT_REMOTE from the saves path; obsolete TIDY text gone.
- 583c1b4df752e29f7931b41675939a24bff1e238: bounded category validator,
  explicit selected-category seeding, independent folder setters and tests.
- 75d44aea8e21cada689a47159e2ad361bb45067b: keep `remote:/` distinct from
  `remote:` when checking empty folders/seeding; an unfixed control demonstrated
  false readiness with an unreadable absolute root but a readable relative home.
- 90df1172a1cdc98865e6efc0422ed3845e5631e9: restore parent probes
  shorten each time and preserve explicit relative versus absolute roots.
  The old relative-root refusal control timed out; all 21 controls now pass.
  Metadata-only predecessor be7d810498 retains the identical tested tree.
- 6f89bc7cecee5972909828103689e2c7c0711c30: direct ROM payloads outside
  system subfolders are misplaced, not empty. No target guessing or movement;
  all 30 validator controls pass, with a failing old-source control.

Backend APIs: `cloud_setup --validation-context` is local read-only JSON;
`--validate-folders <csv saves,settings,roms,bios,media> <run-id>` returns
schema 1 findings bound to exact config/paths/run. 25 seconds total, depth 3,
4096 entries/2 MiB per listing; no hashes/downloads or account-root discovery.
`--seed-folders <explicit csv>` creates selected structure/notes; no-arg refuses.
Set saves/settings/content independently; explicit root/relative namespaces
are preserved. `cloud_scan --run-id ID` uses JSON stamps and
`--stamp-valid done ID` / `--stamp-valid content-done ID [--with-media|--media-only]`.
No old epoch stamp is a valid new result.

Root owns four committed scripts: cloud_backup, cloud_content_restore,
cloud_scan, cloud_sync_helper. rc_cloud_validator owns setup/validator tests,
completed the coordination `tools/last-good-scripts-test` adaptation and
`docs/qa-logs/2026-10-07-cloud-validator/validator/` receipts; it has released ownership. Product source
is presently committed; do not edit an in-flight script. Root owns
cloud-round-trip changes and all shared documentation. Worker must not stage
shared root changes without coordination.

Evidence: root 21 controls PASS in
`docs/qa-logs/2026-10-07-cloud-validator/content-scope/pixelelated-content-scope-07/`;
the relative-root old-source failure is in `pixelelated-content-root-unfixed-01`.
Earlier run06 has 19 PASS and remains valid for its source; rejected run04
could not start its sandbox and is not proof. Exact inputs and compact
receipts are sealed; completed root fixtures were retired with shared rclone
preserved. Validator final04 has 30 PASS. The completed worker compacted these plus the
corrected actual-image harness controls under the packet's validator/broad
folders. Verify the returned manifests. Bash/Python/package checks passed.
These are source controls, not complete new firmware qualification.

### ES UI — qualification complete; owned runtime retired

`/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup`,
branch `feature/m7-manual-cloud-setup`, clean final source
`4e410dc9a816cc947f16235ad2b24824b29dd84e`. Local/unpushed/unintegrated.
Earlier1272b/df68 preserve refreshed selections; c9fab fixes creation
cancellation grouping; baee adds the bounded byte-preserving JSON reader.
#512: `1d5397fda9d7c5c2a4c7f9390ef49b9bb4b879ce` localizes three new
failure reasons and names Scan75 contention as another check, preserving sync
wording for ordinary sync. #513: `6b473c26e8cc03cbd509b3056c60aaf84cb8dbc0`
fits saves help and content-editor titles without losing category meaning.
#514: final4e410 scopes empty-library findings to selected folder/content and
uses category-neutral manual guidance through CLOUD > CHECK CLOUD FOLDERS.

Final tested ES binary:
`94962c93775709dd3e2e7c0eefd470184c3defc41cd5c89cf917f4bcee2dd8b0`.
French catalog:
`a5fafc02b1a243dc63c9d9842efcce040ac72ae076279c77c79c8a0477180ea4`.
The final-source receipt binds five ES/catalog source hashes and six installed
scripts to their clean commits. Build07 compiled GuiMenu and linked with198
reused inputs unchanged; checks03 passed syntax/extraction/catalog/vocabulary.
The final binary/catalog were removed only after qualification and review;
retain source and hashes, not temporary compiled payloads.

UI packet: `docs/qa-logs/2026-10-07-cloud-validator/ui/README.md` and
`evidence-index.json`, `coverage.csv`, controller steps, compact source/build
receipts, original failed logs and reviewed/rejected frames. Root verified
all514 pre-retirement seals and independently viewed16 supplemental frames;
`root-supplement-review.json` binds this review to the final99-entry index.
The original `root-review.json` covers only its original42 entries.
`reference-review02.md` holds the complete affected-source inventory;
`reference-review03.md` holds the independent completed-state checkpoint and
final root disposition. `verify-ui-index.py` checks reference roots, anchors,
dimensions and hashes, not semantic coverage. Earlier frames retain their
actual source/catalog plus explicit unchanged-input reasoning.

The last positive CF14 control reached restore options → selected supported
GB system → Back. Selected configuration and nine cloud file hashes remained
equal; NO_ROM_RESTORED is retained. Four corrected empty-folder frames prove
scope/fit with an out-of-scope populated library. No alternate-folder discovery
or ROM transfer is inferred. OAuth's exact synthetic helper/setup is retained;
it proves Connected → Continue, not real provider authentication. CloudOffer
creates saves only; restore FINISH consumes its synthetic marker and returns.
CF11's nested warnings actually fire in backup logs but the plain stdout
sentences are discarded by the UI parser; actual completed-result frames and
consumer trace are separate evidence. Do not invent a visible warning.

Failed aggregates remain failed: reconstructed build01 launcher125;
build02 compile/link succeeded but msgfmt host-PATH failure ended1;
build04 compile/link/catalog succeeded but cmake host-PATH failure ended127.
Separate pinned-tool checks01 provided the actual183-case unit PASS. Build06
passed but was superseded before installation and qualifies no frame.
Mis-navigation walks stay harness-rejected despite some runner0 results.

Both disposable scopes are gone:
- Original `/workspace/tmp/pixelelated-510-es-ui`, QEMU3331538,
  SSH10210/VNC31: retired after both108-check VM suites and original UI proof.
- Supplemental `/workspace/tmp/pixelelated-510-coverage02`, QEMU3691349,
  SSH10212/VNC32: retired after complete inventory/root review at03:47UTC.
  All63 launcher PIDs exited; provider stopped; monitor/serial sockets and
  ports10212/5932 absent. Removed1,861 regular files,5,217,521,664 allocated
  bytes (4.86GiB), including guest disk/private key/compiler/binary/catalog.
  Compact retirement plan/preflight/execution/reproduction records remain.
  Root independently read back absent processes/ports/scope and all528 worker
  seals; `root-retirement-review.json` raises the final sealed file count529.

The UI and validator agents have completed and released ownership. No guest
remains to reconnect to; old port/socket/pidfile paths are historical only.
Source checkouts, accepted firmware/build roots and shared development rclone
at `/tmp/pixelelated-rc-rclone/rclone` were preserved outside that owned scope.
Do not recreate scratch merely to repeat passing tests.

## Canonical references and integration strategy

`docs/es-menu-map.md` places the cloud pages and distinguishes groups from
pages. Both pinned ES5d2fcb9b and draft ES4e410 pass the title check (52/53
screens respectively,0 missing); that is not screenshot coverage. The
replacement flow is mapped in `docs/pixelelated/cloud-folder-flow-review.md`
with CF01–CF15 screenshots/receipts; `docs/conflict-wizard-ia.md` preserves
unchanged conflict architecture and links the evidence system. The draft
change log remains explicitly in qualification. Accepted visual baseline is
still d72084ccad/78 frames, accepted2026-09-26; source overlays do not replace it.

Already published scoped coordination commits on next:
`083f4fad86` QA tools, `f6037a9133` required process, `2ab5ebbc86` non-UI
proof, `85dfe87b8a` visual checkpoint, `0f073485f` prior handoff/references.
Their coordination equivalents are5f21df7756/d07a197ea9/6ae69d761f/
907e333d70/ae6f1e347d. This final follow-up contains the completed UI packet,
canonical links, localization-rule clarification, work/friction logs and
checkpoint. Integrate only its scoped commit; never merge this divergent
coordination branch wholesale. The ES/distro product branches remain separate.

The known15-closure audit cadence belongs to #507; ceremony-check permits
ordinary evidence/fix pushes while the audit remains owed. Do not bypass the
cheap gates or replay accepted #471 to make that warning disappear.

## Separate Herdr website lane — #511

Applied `/home/max/.codex/skills/herdr-project-coordination/SKILL.md` and
installed `herdr --skill`. `HERDR_ENV=1`; preserve focus and unrelated lanes.
Main lane is `w4:p2`. New **pixelelated · Website** workspace `wG`, pane `wG:p1`,
agent `pixelelated-web`, cwd `/workspace/repos/pixelelated-website`.
**Created, not working:** Codex is blocked at “Trust this folder?”
The explicit asynchronous Trust and continue/Leave waiting question remains
unanswered. The installed Herdr skill requires confirmation before answering
that startup approval. Do not send a task or Enter until that answer arrives.
Then inspect readiness, send the scoped task and verify actual acknowledgment.

Site-only task: own the private website repository, home/cloud/ROM/BIOS guides,
portable static build and local layout/link proof, plus #511 status. Root owns
M7 and distribution documentation. Reuse selected licensed existing docs, not
the old whole-site baseline. Do not change DNS, mail or privacy or add a
firmware gate. Prepare a reviewable site before any required hosting approval.

Private repository `pixelelated/website` has published starter
`8559ab3e3c0bc4454ae8e2722fce7b72d677c2dd` on clean `main`, parent
`62b33d31fef4860f46abcb756ca697cd88ff788e` from the owner.
Bot `blitterbot` has maintain/push access, admin false. Preserve visibility.
The old local root `8423480` is archived; never force it over the owner's
history. Only README/AGENTS exist; no site build, workflow or deployment yet.

Domain **pixelelated.com** is confirmed. Owner DNS was verified on
2026-10-07 at 21:30 UTC: all three authoritative nameservers plus 1.1.1.1 and
8.8.8.8 show A records 185.199.108–111.153 and www CNAME
pixelelated.github.io. Verification TXT is present; Proton Mail MX is unchanged.
The host resolver had a negative cache; direct Host/SNI Pages requests gave
HTTP 404 and an HTTPS certificate hostname mismatch. Pages API 403 means
configuration is unknown, not disabled. No serving-site claim is justified.
See `docs/pixelelated/site-plan.md`, `site-dns.md` and the exact readbacks
`docs/qa-logs/2026-10-07-site-access/dns-after-owner-update-2130.json` and
`http-after-dns-2129.json`. Local guidance does not wait for the website;
no documentation QR destination ships before its guide is published.

Existing documentation checkout `/home/max/Development/rocknix.org` is at
`4f6df54` on `docs/cloud-saves-native-wizard`, 238 commits behind its old
cached upstream. Reuse selected MkDocs/Material guides with attribution,
following the developer-relations skill and player-language rules.

## Accepted firmware and independent follow-ups

Candidate16 passed 15 VM suites, 78 screens, 26 RC2 upgrade checks and 318
protocol assertions; all eight #471 findings are resolved. This historical
qualification remains valid for that image. Its unpublished experimental RC2
adoption is not public ROCKNIX qualification. The public baseline is ROCKNIX
20261001, tag `c445081a59518f37d9776e5412dd7b14910696f7`, with
`SYNCPATH=/GAMES` and `SYNCPATH_BACKUP=/GAMES/backup` (D-CLOUD-177).

H700 `43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa` is accepted. The authorized
SP transfer/reboot and installed identity were verified at 11:25 UTC on
2026-10-07. That firmware still contains the previous migration behavior.
SM8550's frozen checkout is
`/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-01`, branch
`build/m7-pixelelated-sm8550-01`, commit
`0553c0193ace3aebbefaae5b7b6d49253c2811d9`.
All 737 packages/build04 returned 0; independent acceptance passed at
16:52 UTC on 2026-10-07. The accepted bundle is:
`/workspace/artifacts/pixelelated-candidates/sha256/97367c3235fab7cc6d1ec2b54c390fe7ceff786612f29c9f177aaa288a33fb18`.
Raw image SHA256:
`5be73a7305991599cdad6e68535cf7c79767180b6632ce8061207822869e7c34`;
update tar SHA256:
`c9701f3f247f82b4c6a662a315cb1a054864866fc52a738e86fbc15bde662a50`.
No Nova deployment occurred. Original source custody for failed owners
01/02/03 remains preserved; a generated support-document row reorder remains
in the build tree. Release mapping, source, licences and publication remain
under #492/#344/#265/#359. Inventory12 has 583 components, 14 missing recipe
licence metadata entries and `publication_bundle_complete=false`.

Personal Dropbox preflight at `/tmp/pixelelated-dropbox-preflight-9oje01ie`
remains preparation only. The specific question to privately copy the SP's
authorization for host inventory is unanswered. No authorization copy,
personal remote request, rename or deletion occurred. This does not hold the
RC. #505 is closed not planned; its diagnostic draft stays isolated.
#509 name cleanup, #395 alerts, #432 FOSS observability and #464 RA reset
automation remain later work. No Dropbox check or fresh RA reset is required.

## Next commands and handoff

1. Read the actual answer/status of the pending #510 repair-scope question.
   No implementation, pin or build is authorized by mere elapsed time on that
   unresolved choice. Independent proof is finished and safely retained.
2. Reconcile M7/#508/#510 and the source-fix #512/#513/#514 dispositions with
   the final packet. No new source audit has run; #507 follows the scope/integration
   step, then actual firmware and public adoption proof.
3. Preserve the separate website startup question and private Dropbox question
   as unanswered unless a later explicit reply changes them. They are not RC
   blockers; do not operate a personal device/cloud or another lane by inference.
4. Before a push: tools/rules-check, tools/register-check,
   tools/work-log-index --check, tools/ceremony-check --gate. Run
   `python3 docs/qa-logs/2026-10-07-cloud-validator/verify-ui-index.py "$PWD"`
   for packet integrity, and inspect its explicitly limited coverage claims.
5. Read the archived checkpoint for historical failed owners if needed; use
   retained logs/frames/source hashes rather than recreating removed disks.

Session-stash and herdr-project-coordination skills were applied. The initial
fresh-context resume review and bounded final supplemental review are complete;
root independently reconciled the final source, coverage and retirement.
