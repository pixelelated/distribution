# Saved Session State

> Saved: 2026-10-07T19:13:55.048345+00:00
> Coordination branch: feature/conflict-resolution
> Repository: pixelelated/distribution

## Start here

pixelelated is an immutable handheld Linux distribution, built here as complete
OS images. Read AGENTS.md, canonical rules from `next`, then this checkpoint
and M7's live ordered body. Primary checkout `/workspace/repos/rocknix` is on
`next`; coordination checkout `/workspace/repos/rocknix.worktrees/conflict-resolution`
is on `feature/conflict-resolution`. Before this checkpoint, their heads were
357d88010a91d879e08d700d32a8ea8f0c9436a6 andd24d08351e respectively.
The prior checkpoint is `archived/saved-session-state-next-20261007T191355Z.md`; older archives retain full
candidate16/H700/SM8550 custody. Never restart accepted jobs from an old handoff.

This coordination branch has divergent history: cherry-pick ONLY its new
scoped coordination commit to next. Never merge the whole branch. Sibling
product drafts below remain held, local and clean. Current evidence packet
and draft changelog are not finished validator or firmware qualification.

Authorization persists for scoped implementation, parallel agents, host/VM
checks and ordinary commits/pushes. Physical actions/personal-cloud changes
retain their named scope. The SP update/reboot and single wake input already
completed; do not repeat. Screenshots were separately authorized. Cloud
credentials and inventory remain private. No new publication is implied.

## Current focus and order

1. #510/D-CLOUD-178: the owner chose a category validator, explicit smaller-file
   fixes and manual ROM/BIOS instructions. Refine concrete action plans and
   reconcile the existing paths/flow; do not ask them to choose the old design
   alternatives again. `docs/pixelelated/cloud-folder-flow-review.md` holds the
   diagram, verified history, reuse map and remaining implementation work.
2. #508: adapt and qualify the retained manual-setup drafts, then integrate.
   Product integration and new device builds remain held until this reconciled
   behavior is qualified. Existing proof is exact-source/overlay evidence.
3. #507: freeze and independently audit the resulting P5 delta. No audit or
   external transfer has started. Candidate16/P4 stays accepted;15 completed
   closures now require this new scoped review. Use code-auditor serial stages
   and the Facilitator; old Fable payload authorization is not a blanket grant.
4. Include qualified new bytes in selected firmware, then finish release
   staging and named physical smoke. No current build or QA VM is running.

**Parallel #511:** define the owned-domain website/wiki and cloud/ROM/BIOS
setup guides. The owner first requested future tracking, then a parallel path
now. Hosting is flexible (D-WORKFLOW-152/153): assess GitHub Pages first for
static pages but choose from requirements and keep portable source. A separate
ordinary site repository is preferred; inventory existing repos before
creating a duplicate. terminal_handoff_review completed the read-only inventory;
`docs/pixelelated/site-plan.md` records its findings and launch plan. The lane
has not deployed or changed DNS. The exact domain spelling question
is pending: earlier pixelelated.com versus latest pixelated.com. Do not infer
an OS rename. Website delivery does not gate firmware/local guidance.

## Chosen cloud contract

D-CLOUD-175 retires cloud_migrate_layout, automatic join/follow, startup
migration prompts and optional TIDY. D-CLOUD-176 separates folder choice from
relocation consent. D-CLOUD-177 establishes public ROCKNIX plus clean installs
as the adoption baseline, not the maintainer's experimental state. Official
release20261001/tagc445081a59518f37d9776e5412dd7b14910696f7 uses /GAMES and
/GAMES/backup, unlike unpublished /ROCKNIX/Saves layouts. Both old submitted
PRs3404/40 contained optional migration, but closed unmerged. Do not repeat
the corrected claim that all migration began at the hard fork.

D-CLOUD-178 chooses bounded read-only checks within enabled categories and
selected roots. Results distinguish missing, empty, present, recognized
misplaced and unreadable, tied to exact config/run identity. Do not scan an
entire account, infer absence everywhere or claim complete transfer integrity
or BIOS compatibility from folder readiness. Explicit progress-file fixes need
an exact plan, size/count, collision/source retention and verification policy;
there is no category repair API yet. ROM/BIOS guidance shows expected paths.
Once #511's actual guides are published, See instructions opens a QR modal
for the relevant guide, never a clickable handheld link/browser. Until then
local guidance remains useful; no speculative URL ships.

Reuse boundaries: corrected cloud_setup folder readers still have a relative
ancestor fallback needing care. --folder-state currently checks saves only;
--seed-folders creates every tier. Content mapping/system classifiers can be
extracted inertly; recursive --scan and account-root fallback are not strict
validation. Archive discovery is availability only and may generate identity
if composed carelessly. Local rocknix-systems BIOS checks remain separate.
ES scan job/category/QR helpers are useful, but transfer entrypoints mutate,
current cache stamps lack config identity, and Scan cancellation still speaks
of backup/restore. Its result lines cannot fit paths/QR; use guidance UI.

Other draft gaps: general folder setter couples all3 pointers; content restore
can fall outside selected root; cloud_backup still directs nested-folder users
to removed TIDY; EN1280 setup intro truncates. Do not call #508 finished.

## Retained drafts and proof

Distribution `/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders`, branch
feature/m7-manual-cloud-folders, base7cfdf9f73ae2a064ee4f281461e661301cb2dd65:
- e484380a3426626d84afa0c5109abeff4512dd0c removes installed migrator/old UI contract.
- 3268015c185b04a17e756829ee116c664d679b4e fixes empty relative one-component
  folders and failed partial final readback. Final cloud_setup SHA256
  a7eea3879848ec4879f279f3b7e2a2c08f3531c970ec4dd9858b09290975265c.
- Local clean, unpushed/unintegrated. Initial receipts318/files28 source entries
  independently checked; edge delta94 receipts also checked. Host43 cases,
  paired20 controls, guest10 edges + seed0, final affected81 checks PASS.

ES `/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup`,
branchfeature/m7-manual-cloud-setup, base5d2fcb9b71f363cfa4813d5356f02c48ab58e139,
local clean commit300f97d28a072b916c54dcbf108f1440e7253761. No push/pin change.
- Six production units compiled/relinked;178 cases1886 assertions PASS; final
  functional GuiMenu rebuild and French catalog checks retained.
- Binary053aa74196355df41d9cc4cdea8e3ed291c1d584d072b11b308469358814d45b;
  French e14286ee7e3a414d1c633561720ebe6efa3bc453c2a997740f74800913034554.
- EN/FR640 and FR1280 fit; EN1280 old intro truncates, explicitly not full
  visual acceptance. Actual create/failure/retry/ready, explicit content choice
  and startup preservation proved selected draft behavior, not public image
  adoption. Failed/stale-fixture frames remain labelled as failures.

Root packet `docs/qa-logs/2026-10-07-manual-cloud-setup/` includes source/edge
readbacks,9 routing controls, broad-harness and es-ui. ES SHA256SUMS digest
b59de3fa32afd6b34e67994f23fff8021c615816a8d7867187f1ef5ed9d8bdc2:
root independently checked1031 checksums and10 source entries. Broad1303 PASS
(no FAIL/SKIP) qualifies pre-edge e484/67c6; finala7ee has81 affected controls,
not a rerun of the whole broad suite. `tools/last-good-scripts-test` SHA256
2981cc8b8ab7a94c762b0560a29c8bf680136cb9abff9ede2c4fdf6d678c5bd9.

QA tools remain uncommitted in the coordination checkout and unintegrated on
next. `held-qa-tools.patch`/JSON in the packet preserve their exact bytes;
cloud-round-trip currently requires the held product folder-state contract.
The draft cloud-sync-changelog.md is also held, excluded from coordination
publication. Do not erase these deltas or call them shipped.

QA routing changes preserve ordinary13 archive cases without the deleted
engine, recover historical --ref files from git and accept --source-root.
Retired migration suites refuse absent engines before creating fixtures.
The broad01 launcher used watch-build directly in exec58141 instead of required
watch-build-submit; this is recorded friction, not claimed durable supervision.
Later focused jobs used the correct launcher.

**Cleanup complete:** guest1235151, endpoint863920, cleanup launcher1295516 and
broad controller/command/watcher1062185/1062214/1062186 absent in host namespace.
ui17 ended0 at18:55:21. QA disk, keys and1.128GB compile scratch retired.
No guest is available for further tests; create one only when needed. Never
replay exclusive verifiers or alter accepted builds to recover scratch.

## Accepted firmware and remaining release gates

H70043d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa is accepted including DDR variants
and ARM handoff; SP authorized update/reboot completed11:25. These bytes still
contain the old migration behavior. Further physical smoke remains separate.
SM8550 frozen tree `/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-01`,
branchbuild/m7-pixelelated-sm8550-01, HEAD0553c0193ace3aebbefaae5b7b6d49253c2811d9.
737 packages/build04 rc0 at16:51:14, independent acceptance16:52:00 and all
channels/seals/exits checked. A generated support-doc row reorder is retained;
product inputs unchanged, not a claim the whole tree is clean.

Independent bundle:
`/workspace/artifacts/pixelelated-candidates/sha256/97367c3235fab7cc6d1ec2b54c390fe7ceff786612f29c9f177aaa288a33fb18`
img5be73a7305991599cdad6e68535cf7c79767180b6632ce8061207822869e7c34,
tarc9701f3f247f82b4c6a662a315cb1a054864866fc52a738e86fbc15bde662a50.
Read `docs/qa-logs/2026-10-07-device-builds/sm8550-resume04/`; no Nova deployment
or RC designation. Recovery01/control01/build02 source custody holds remain.
About2TB free; no additional swap/drive cleanup owed.

Candidate16 accepted15 VM suites78screens26RC2 upgrade318protocol assertions,
all8#471 findings resolved. Preserve as historical exact-image qualification;
its experimental RC2 cloud cases do not substitute for public ROCKNIX adoption.
Remaining #492 inputs/per-image mapping and #344/#265/#359 source/licence/
publisher/docs/named physical smoke. Inventory12 has583components,14missing
recipe-licence metadata and publication_bundle_complete=false. No publication.

## Personal cloud and other follow-ups

Private `/tmp/pixelelated-dropbox-preflight-9oje01ie` is metadata-inventory
preparation only. Default host rclone config is empty; no auth/env found.
Pending question specifically asks permission to copy SP Dropbox authorization
privately to host for inventory. No answer inferred, no credentials exported,
no personal remote requests. Exact reconciliation follows inventory with its
own action scope; no blind rename/delete. This does not hold software release.

#505 CLOSED NOT_PLANNED; diagnostic draft isolated at m7-migration-diagnostics,
unintegrated. #509 active Rasteratops filename cleanup stays later. #395 alerts,
#432 FOSS observability, #464 RA reset automation remain backlog. No hosted
Dropbox credential or fresh RA reset is a gate.

## Next commands and handoff

- Read live #510/#508/#511 and M7, inspect website agent's finished inventory.
- Continue concrete validator contracts/source changes in the owned feature
  trees, then focused host/VM proof; no new device build yet.
- Use tools/watch-build-submit for long jobs, retain result/exit receipts and
  actively consume them; a status file is not a disconnected chat alert.
- Run rules-check, register-check, work-log-index --check and ceremony-check
  --gate. The current audit cadence is the known CI-only overdue item (#507).
- Publish this scoped coordination checkpoint by cherry-pick to next, never
  wholesale merge; do not accidentally include held cloud-sync-changelog.md
  as a shipped behavior claim or integrate held product drafts.

Fresh-context reader /root/validator_site_handoff verified the draft commits,
source/receipt hashes, raw1303 PASS counts, final81 controls,178/1886 unit log,
actual six host PID exits/retired disk and current M7/issues. It caught a stale
packet README that still claimed an active guest/future #510; root corrected
that README and the harness-hash label. Coordination-only integration is
explicit above. Website inventory is complete; current status is below. The reader corrections
were applied and independently rechecked: no remaining inaccurate resume
instructions, held patch matches all seven deltas, and local website state
matches. No active agent or job remains in that review.

## Website inventory and creation limitation — #511

Existing docs source `/home/max/Development/rocknix.org` is clean at4f6df54ca16121ff2cd0620407aea6434ee59147,
branchdocs/cloud-saves-native-wizard, one local commit ahead. It is MkDocs and
Material with selected reusable guides/screenshots. Remotes still name
maxengel/rocknix.org and ROCKNIX/rocknix.org. Its old branch is238 commits
behind cached upstream; do not clone it wholesale as a current site. Upstream
docs PR188 is OPEN/unmerged, unlike distribution/ES PRs3404/40.

No dedicated website repo appeared in accessible pixelelated inventory;
private Pages settings returned403, so no organization-wide absence claim.
Proposed dedicated repo is pixelelated/website. Creation was attempted with
both gh GraphQL and documented REST; both refused current blitterbot token
(Resource not accessible by personal access token; REST403). Blitterbot is
an active org member. Do not infer repository creation succeeded. Prepared starter README/AGENTS now live in a separate clean local repo,
`/workspace/repos/pixelelated-website`, branchmain,
commit8423480a166f3fe6a9673e21c79e806563b9eb49 (temporary source also retained
in /tmp/pixelelated-website-bootstrap). The proposed origin URL is configured
but remote creation failed. Repo creation and bot write access are needed
before a push; never ask for a token in chat. No workflow/deployment/hosting/DNS change was made.

For earlier domain pixelelated.com only, public DNS has no A/AAAA, www NXDOMAIN,
iwantmyname nameservers and Proton Mail MX. Old Cloudflare/Hostinger assumptions
are stale. The domain spelling question remains unanswered; do not apply DNS.
Site v1 can reuse a current static MkDocs/Material base plus selected licensed
pages, lowercase LCD wordmark, separate cloud/ROM/BIOS guides and release
links. Keep sources portable and preserve attribution. Firmware payloads do
not belong in Pages (published-site limit1GB); link release artifacts instead.
