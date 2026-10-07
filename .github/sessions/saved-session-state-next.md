# Saved Session State

> Saved: 2026-10-07T17:06:06.327418+00:00
> Coordination branch: feature/conflict-resolution
> Repository: pixelelated/distribution

## Start here

pixelelated is an immutable handheld Linux distribution, built here as complete
per-device firmware. Read AGENTS.md and the canonical `.claude/rules/` from
`next` before work. Primary `/workspace/repos/rocknix` stays on next;
coordination is `/workspace/repos/rocknix.worktrees/conflict-resolution`.
The immediately preceding checkpoint is `archived/saved-session-state-next-20261007T170606Z.md`.
It preserves the full failed-owner history; the older15:37 archive retains
accepted candidate16/H700/SP inputs. Never replay accepted jobs merely because
this session resumed. Secrets never appear in output; physical reads use the
credential filter and state-changing actions use tools/device-act.

Standing authority covers scoped fixes, host/VM QA, commits/pushes, and the
H700-then-SM8550 build sequence. The user explicitly requested parallel work.
The RG35XX SP screenshot permission persists. The separately approved ONE
wake keypress and follow-up screenshot completed16:26UTC. Do not repeat that
input. No migration retry, confirmation, new update/reboot/game launch or
release publication is authorized by that yes.

## Current Focus

M7.P5: H700 and SM8550 firmware artifacts are now accepted. The immediate
follow-up is #505's concrete diagnostics proposal and its exact implementation
approval, then focused VM proof and final selected-artifact inclusion. #507
owns the newly due independent audit of the frozen post-candidate16 P5 delta.
M7's body is the ordered execution plan. Physical/source/publication gates
remain separate. No RC designation or Nova deployment has occurred.

## Completed This Session

- #502 approved English/French migration copy is published: ES
  5d2fcb9b71f363cfa4813d5356f02c48ab58e139, distribution0553c0193ace3aebbefaae5b7b6d49253c2811d9.
  Four actual640x480/1280x800 frames and compiler/gettext checks pass. Temporary
  QA payloads were removed. Current SP firmware retains the earlier wording.
- #503 FEX repair and #506 helper corrections are complete/closed. Original
  ARM64 include contamination reproduced with exact Nix/compiler inputs;
  narrow standard-include exclusion preserves both guest architectures. Full
  FEX package and installed14ELF payloads pass. Failed01/02/03 stay historical.
- SM8550 build04: all737 packages completed, runner0 at16:51:14. Fourzero
  channels/13seals/exits verified16:51:39. Firmware acceptance PASS16:52:00;
  fourzero channels/3seals/exits and controllerPASS16:52:09. Host readback at
  16:56:37 rehashed all bundle bytes, checked independent inodes, all26sequence
  seals and actual process/container exits. No build or acceptance job remains.
- #504 historical SP review is complete/closed. Wake/frame exposes an incomplete
  transfer without the underlying cause. Source tracing confirms discarded is
  the completed discarded-save tier before content, not an abort/finish marker;
  elapsed freezes when the worker exits. Copy/check failures share the same
  generic result. No personal-cloud retry or provider-byte equality is claimed.
  Raw device data/images remain LOCAL ONLY in the ignored review folder; only
  its .gitignore and PUBLIC-SUMMARY.md are publishable under existing authority.
- #344/#265/#359 bodies reconciled from accepted evidence. Installed version
  and branding licence files are proved; corresponding source, component licence
  dispositions, publication tooling/docs and broader physical smoke remain open.
  Readiness/support-matrix docs now distinguish current proof from history.

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

## In Progress — #505 diagnostic proposal, application not approved

Fresh clean feature tree:
`/workspace/repos/rocknix.worktrees/m7-migration-diagnostics`
branch `feature/m7-migration-diagnostics`, base next0f4d701a23.
No production change has been applied there. Automatic approval review rejected
applying the diagnostic patch because production signal/failure-path changes
need explicit implementation authority. Do not work around that rejection in
another worktree. Root will present the concrete reviewed patch and ask for the
specific approval, then continue under that authorization if received.

Final sealed proposal and scratch controls: `/tmp/pixelelated-505-draft/`;
start with `README.md` and `proposed.patch`, SHA256
`8cd8ae12c52223c3c1a5b4fb333db7434cb8deed9153275c76b2e0d7ab102732`.
All 287 packet seals verify. The preparation and focused read-only review agents
are complete. All four watched owners02–05 returned zero, and their 16 owned
processes exited (host-context `owner-exit-verification.json`). All 28 disposable
fixture roots were removed. No VM/device/cloud run is underway for this proposal.
The exact patch-and-VM-test approval question was sent; await the user's reply.

The proposal adds a bounded private helper/script record (current/prior/attempt),
run/process identity, typed stage/operation/result, atomic0600files, and signal
interruption without guessing player/game intent. Initial record failure would
refuse before cloud mutation using existing rc5: this is an explicit new refusal,
not a claim of wholly unchanged behavior. Later record failure must preserve the
actual operation result and leave the run distinguishably unfinished.

The exact old-source missing-record negative control and 12 proposed positive
controls pass. Lifecycle controls cover TERM/KILL, concurrency, record failure,
early exit and bounds/privacy. Latest-attempt precedence over an older current
success is explicit and tested after acquisition-record refusal. `recipe02`
verifies exact installed bytes, mode0755, Python3 dependency and pkgcheck0.
First sandbox-unavailable controls never ran the script and are explicitly
invalidated. Read actual latest manifests/results: no final VM or
assembled firmware inclusion is claimed. After approval, apply to the isolated
feature tree, run package checks and hash-verified focused candidate16 VM overlay
proof; final selected release artifacts still need the fix included/qualified.

## Next Steps

1. Read #505's sealed concrete patch and isolated controls, obtain explicit
   implementation approval prompted by automatic review, then run the focused
   synthetic VM proof. A yes to wake the SP is not that approval or a cloud retry.
2. Freeze the resulting P5 delta for #507, using the code-auditor skill serially:
   scoped Milestone, primary plus verified cross-lab reviewer, required blind/
   refutation passes. No new external call has started. Confirm concrete safe
   payload/disclosure authority before dispatch; omit private SP records.
3. Reconcile #492's remaining input-comparison/source inventory criteria. Its
   actual H700 and SM8550 firmware criteria are proved; compilation is complete.
4. Continue #344/#265/#359:14 component licence metadata dispositions, retrievable
   corresponding sources, per-image sweeps/delta mapping, manifest-selected
   versioned draft publisher, adoption/recovery/release notes/public docs, named
   per-asset physical smoke. No accepted H700/SP transfer or VM matrix replay.
5. Publish current compact evidence, readiness docs, logs and this checkpoint as
   a scoped NEW commit/cherry-pick to next, through normal hooks. Never merge the
   divergent feature history wholesale. Read exact-head hosted results.

## Published checks and operational notes

Published prior checkpoint: feature786df869939bc45717ec52e9a2cd35c3626aa988,
next0f4d701a2333b36ad1c45b679e8987e4393212a9. Both wordlist checks pass
(runs37653130416/37653236283). Record run37653236199 fails ONLY the newly due
13-closure audit cadence; local blocking gates pass. #507 owns the follow-up.
#503/#506 then closed, so the next cadence count may be15. Candidate16/#471 is
not reopened. Read exact head_sha API results; ordinary run-list was stale.

GitHub comment/close convenience calls failed transiently. Body updates persisted;
root read back actual state before continuing. Explicit GraphQL addComment plus
REST state PATCH succeeded for #503/#506; both completed states were read back.
Never blindly replay a failed mutation without checking what persisted.

Host PIDs are invisible in the tool sandbox: use host-context reads with recorded
start identity, or report unknown. Local watchers do not deliver disconnected chat
notifications (#395). There are no longer live build or #505 draft-control
owners to supervise.

Historical accepted candidate16, H700/SP, source custody and cleanup hashes are
in the archives. #432FOSS observability/#464RA reset automation remain backlog.
No Dropbox check or new RA reset is owed.
