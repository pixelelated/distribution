# Saved Session State

> Saved: 2026-10-07T18:07:14.611527+00:00
> Coordination branch: feature/conflict-resolution
> Repository: pixelelated/distribution

## Start here

pixelelated is an immutable Linux distribution for handheld gaming devices.
This repository cross-compiles firmware, not an app. Read AGENTS.md and the
canonical `.claude/rules/` from `next`. The primary checkout is
`/workspace/repos/rocknix` on next; this coordination checkout is
`/workspace/repos/rocknix.worktrees/conflict-resolution`. Read the live M7
milestone body for ordered priorities. The previous checkpoint is
`archived/saved-session-state-next-20261007T180714Z.md`; older archives retain full candidate16/H700 custody.

User authorization persists for scoped implementation, parallel work, host/VM
checks, commits/pushes, and H700 then SM8550 builds. Product firmware publication,
new handheld input/reboot/update and personal-cloud mutation retain named scope.
The one approved SP wake input already completed; do not repeat it. Screenshots
were separately authorized. Raw SP evidence remains local/ignored. Do not replay
accepted firmware jobs or QA simply because the session resumed.

## Current Focus

M7.P5 #508: remove cloud-folder migration, retain ordinary linking, folder/README
creation, explicit selection and normal sync/restore. Fresh configurations use
`/pixelelated`; existing sign-ins and configured paths remain. D-CLOUD-175 records
the maintainer's direction. No automatic join/follow, boot migration prompt or
optional TIDY row should remain. Qualify scripts and EN/FR screens, then freeze
the P5 delta for #507's independent audit and include it in selected firmware.
The accepted device builds still contain the previous migration implementation.

## Completed this session

- Corrected the historical answer: submitted ROCKNIX/distribution PR3404
  head4c83ebede40af27a375ced4cac72983be5715944 and ES PR40 sourceca300dd41
  already included an OPTIONAL migration preview with MOVE / LEAVE THEM.
  The engine began in2233a98114 on September1. Both PRs closed without merging.
  Automatic startup/fleet-follow behavior came later. Do not claim all migration
  began at the hard fork; normal setup and the optional tidier coexisted.
- The user approved #505's exact diagnostic patch, then replaced that approach
  with manual cloud setup. The patch is applied only in isolated
  `/workspace/repos/rocknix.worktrees/m7-migration-diagnostics`, unintegrated,
  unpushed, without a new VM test. #505 CLOSED NOT_PLANNED, superseded by #508.
  The old automatic-review rejection is resolved, not a pending approval.
- Created #508 with quoted direction, VM-first answer and acceptance artifacts.
  M7's top priority, P5 row and historical P1 disposition now agree. #507 audit
  follows the settled replacement; no external review call has started.
- Root updated current policy/register, cloud docs, menu map, readiness and
  support matrix; preserved historical migration evidence as historical.
- Host Dropbox preflight found empty mode0600 default config and no usable
  authorization. Prepared private metadata-only inventory; zero remote requests.

## In progress: source and proof owners

Distribution owner `/root/sp_migration_review`:
`/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders`, branch
`feature/m7-manual-cloud-folders`, base7cfdf9f73ae2a064ee4f281461e661301cb2dd65.
Uncommitted replacement removes engine/installation, makes cloud_scan read
cloud_setup --folder-state (STATE=ready|missing|no-remote, SAVES/BACKUPS/CONTENT,
SAVES_EXISTS), and seeds selected folders without pointer rewrites. Unknown or
malformed current-layout markers must still refuse. Existing config bytes stay.
Twenty-three initial host controls reported PASS at
`/tmp/pixelelated-508-host01`; exact old source reproduced silent auto-follow.
Package staging and pkgcheck pass. Reviewer found relative paths could bypass
marker checks, and the interrupted-state fixture used the wrong historical path;
fix and rerun before final qualification. No final firmware inclusion claimed.
A fresh synthetic candidate16 guest has completed11 initial script cases, owner
`/workspace/tmp/pixelelated-508-vm01`, SSH10158/VNC58/WebDAV9058. Initial PASS is retained in artifacts/result.json; current cloud_setup bytes
differ from those inputs, so this is not qualification of the later corrections.
Recorded QEMU PID860697 and guest.json assign the guest to sp_migration_review;
confirm host liveness and explicit handoff before ES takes control. Corrected
script proof hands the same guest to ES, avoiding a second retained disk. Active QA callers of cloud_migrate_layout also need a
compatibility sweep; historical migration suites must not run on new firmware.

ES owner `/root/terminal_handoff_review`:
`/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup`,
branch `feature/m7-manual-cloud-setup`, base5d2fcb9b71f363cfa4813d5356f02c48ab58e139.
Uncommitted removal covers boot/optional migration pages, dead move parser/types,
locale strings, and silent content adoption. Setup now checks seeding rc, offers
TRY AGAIN on failure, and only claims readiness on success. Root flagged the
unconditional connection checkmark; owner made it success-only. Compile actual
changed production objects/relink using candidate16 inputs read-only, then actual
EN/FR640x480 and1280x800 frames. Initial host01 correctly refused applying the
production syntax helper to a unit-test source. host02 passed six production
syntax checks/vocabulary but stopped on a trailing blank line. Both are failed
owners. host03 failed one stale known-why assertion; host04 then compiled and
linked all six changed production objects at18:09:16,178 tests/1886 assertions
PASS and accepted input hashes unchanged. Owner /tmp/pixelelated-508-es-host04
contains the binary and artifacts/fr.mo. Actual VM frames remain pending the
corrected script proof and guest handoff. Inspect latest owner announced by agent;
never edit its running shell. Owner dirs `/tmp/pixelelated-508-es-host0*` contain
launcher-result.json, inner.rc, tool-wrapper.rc, console.log and .build-runs.

Reviewer `/root/handoff_review` completed its read-only distro review, identifying
marker aliases and root-default substitution plus the fixture-record mismatch.
The private Dropbox procedure is under
`/tmp/pixelelated-dropbox-preflight-9oje01ie` (0700); REVIEW.md/inventory.py/manifest
and preflight summaries. Multiple Dropbox sections now require explicit remote
selection; any failed stat is incomplete, never presumed absent. No credentials
read and no provider requests. Current pending user question explicitly asks
permission to copy SP authorization privately to this host for metadata inventory.
Do not infer a response; the user may instead supply a host config or defer.
No remote move/copy/delete or handheld rclone execution is authorized. Inventory
is independent of the software release and stays private.

## Accepted SM8550 artifact and custody

Frozen tree `/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-01`, branch
`build/m7-pixelelated-sm8550-01`, HEAD0553c0193ace3aebbefaae5b7b6d49253c2811d9.
Do not advance it merely because next gains records. Frozen PRODUCT inputs
are unchanged; the build generated one support-document PS2 row reorder, whose
exact diff is retained. Do not call the entire checkout clean.

Independent bundle:
`/workspace/artifacts/pixelelated-candidates/sha256/97367c3235fab7cc6d1ec2b54c390fe7ceff786612f29c9f177aaa288a33fb18`

- img.gz:1611493379bytes, SHA256
  5be73a7305991599cdad6e68535cf7c79767180b6632ce8061207822869e7c34
- tar:1616117760bytes, SHA256
  c9701f3f247f82b4c6a662a315cb1a054864866fc52a738e86fbc15bde662a50
- SYSTEM:4cf70aaa6a40d73a5858433370ef9842301454722a5de42c8fe9798d311a3f11
- Raw/update SYSTEM/kernel/ABL equality, GPT, identity,187ARM handoff files,
  14FEX ELF files, installed English and compiled French migration copy pass.
  Scratch disks/extractions removed.

Owners `/workspace/tmp/pixelelated-m7-sm8550-{sequence,build,acceptance}-04`
are TERMINAL PASS. All recorded owner/controller PIDs and actual container
00731af86051732418b7c2c567c801a5d50b9970220d24812643f7e1a86e5a0d are absent.
Read existing verification receipts; never rerun exclusive verifiers.
`docs/qa-logs/2026-10-07-device-builds/sm8550-resume04/terminal/` retains compact
proof. Full terminal packet `/workspace/tmp/pixelelated-m7-sm8550-terminal-04`
is independently hashed. The retained read-status.py is read-only.

Recovery01/preserved, control01 sources/snapshot and build02/nix still have a
source-custody review hold. Artifact acceptance alone does not authorize their
retirement. No broad cleanup, swap operation or new drive is needed now.

## Next steps

1. Inspect live agent messages and actual watcher artifacts; continue source
   review and fixes. Retain failed checks and verify exact corrected bytes.
   Guest script proof and actual UI frames must finish before their payloads
   are retired. Record terminal results and actual owner exits.
2. Integrate checked ES into test/qa-integration through normal hooks, then
   distribution pin/scripts and coordination docs. Do not push unreviewed drafts.
   Root coordination branch is divergent: cherry-pick ONLY its new scoped
   commit to next, never merge the whole historical branch. Fresh #508 feature
   branches start from next and can use their documented normal integration.
3. Publish evidence/log/checkpoint through normal checks. Freeze #508/P5 delta
   for #507 code-auditor, following serial stages and verified cross-lab routing.
   Prepare and obtain any required exact safe-payload disclosure authorization
   before external calls; do not reuse old audit-transfer approval blindly.
4. Bind qualified new inputs into the chosen firmware, then reconcile affected
   tests/image evidence. Source overlays are not already shipped fixes. Preserve
   accepted candidate16 and device artifacts as exact historical baselines.
5. Continue #492 input comparison and #344/#265/#359 release staging: inventory12
   has583components and14 missing recipe-licence entries; corresponding-source
   retrieval/hash proof, manifest-selected versioned draft publisher, release
   notes/public docs and each named board's physical smoke remain outstanding.
   No Nova deployment, new SP update/reboot or RC designation has happened.

## Fresh-context handoff proof

/root/m7_manual_setup_handoff independently read only this repository and its
instructions. It found the correct #508 scope and authorization boundaries,
verified tree bases/owners and highlighted source-hash drift and the stale
canonical next checkpoint. Current cloud_setup needs its corrected proof;
this scoped coordination checkpoint must reach next before resume is safe.
Do not merge this branch wholesale.

## Checks and operational notes

Prior published featureb89e7170cb8b81971d254cfb2254391ee5f8ff99 and
next7cfdf9f73ae2a064ee4f281461e661301cb2dd65. Both wordlist checks PASS
37657953188/37657971868; next record run37657971781 fails ONLY15-closure
independent audit cadence, now owned by #507. Local current rules/register/prose
checks pass; final checks follow finished source and evidence. Candidate16/#471
is not reopened. New record CI may remain red until the actual new audit completes.

Watchers record lifecycle but do not deliver disconnected chat alerts (#395).
An active owner must consume outcomes. Read PIDs in the host namespace and match
start identity; a PID invisible inside the sandbox is unknown, not exited.
Never edit a running shell, rerun an exclusive verifier or blindly replay a
partially successful GitHub mutation. Retain compact inputs/results/logs/frames;
remove completed disposable VM disks/payloads when their test ends (D-INFRA-022).
About2TB free after approved cleanup; no swap action or new drive is owed.

#432FOSS observability and #464RA reset automation remain backlog. No Dropbox
QA credential or new RA reset is a release gate. Personal Dropbox recovery is
separate and waits for exact credential/inventory and later action authority.
