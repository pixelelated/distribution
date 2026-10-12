# Saved Session State

> **Saved**: 2026-10-12T17:02:12.649225+00:00
> **Branch**: feature/m7-component-inputs (record delivery); feature/m7-rocknix-20261001 (source qualification)
> **Repo**: pixelelated/distribution

## Start here

pixelelated is an immutable handheld Linux distribution, not an app. Read next's
AGENTS.md, every-session rules, docs/device-testing-policy.md and the live M7
milestone body. The harness conflict-resolution worktree is stale: leave it alone.
Primary `/workspace/repos/rocknix` stays on next. Current source worktree is
`/workspace/repos/rocknix.worktrees/m7-rocknix-20261001`; records are prepared in
`/workspace/repos/rocknix.worktrees/m7-component-inputs` and integrated into next.

The owner has selected ROCKNIX stable20261001 as the next candidate foundation:
D-WORKFLOW-161 supersedes the September29 base in D-WORKFLOW-111, retaining the
freeze discipline and D-WORKFLOW-116/117 cadence/cost policy. Exact upstream base
is `c445081a59518f37d9776e5412dd7b14910696f7`. Later upstream/next is excluded.

**No build, VM, device operation or cleanup is running.** Owner testing of accepted
bc9dfe8141 firmware can continue. All previous authorized transfers/reboots and
both cleanup batches are COMPLETE and must not be replayed. No device consent is
pending or unconsumed. A new foundation requires new proof; old artifacts remain
accepted only for their original bytes.

## Current Focus

#563 M7.P5 owns the new foundation. Isolated merge
`f370dc87873fecb683c6af73d70a2f377715f47f` has parents ca5d034488 and the exact
stable release. One conflict was resolved by preserving our entire newer
DuckStation recipe: install-m0755 already implements upstream's chmod change.
All11 other imported paths match stable and all other fork files are unchanged.
Three pkgchecks/four syntax checks/common kernel patch dry runs pass.

**Next repair is #564**, a reproduced Steam runtime replacement regression
imported from stable. The function removes the old runtime before downloading its
replacement. Adapted host failure controls: accepted predecessor preserves the
runtime; stable deletes it. No product repair or installed VM proof yet. Keep the
source merge on its qualification branch until repaired; the record delivery on
next carries no newly imported product source.

## Completed This Session

- #563 created; exact owner request, D-WORKFLOW-161 and M7 order recorded. Active
  candidate scope, source plan and rc-accept updated in ca5d034488. Intake budget:
  one source-review session, maximum3 manual conflict files, actual1.
- Exact stable merge f370dc8787 reviewed. Common Linux7.2 DP-audio patch enters
  SM8550 with DRM_MSM/DP enabled, requiring Nova kernel qualification; ABL1.2 and
  FEX's pinned Nixpkgs also require new native/artifact/source evidence. No
  established fix for the owner's #558 shutdown/bootloader observation.
- #564 filed and linked as #563 child before synthetic failure controls. Public
  `docs/qa-logs/2026-10-12-upstream-adoption/` has hashes, results and scope.
  Raw whitespace warnings belong to upstream unified-patch context bytes;
  non-patch whitespace passes. Do not rewrite patches to remove context prefixes.
- #559 corrected: monthly release intake and tracking-with-budget are already
  decided by D-WORKFLOW-116/117. Reusable selective integration/dependency/cost
  procedure remains backlog; it does not supersede current exact-base selection.
- #561 LED preference investigation moved to keep-an-eye-on monitoring by owner
  direction. Default confirmed in earlier readback; do not run the deferred VM
  interruption matrix as a new RC gate without a new reason. Historical writer
  remains unknown; led_flash's persistent setter is an unproved lead.
- #562 future read-only ROM/cloud integrity comparison filed. Current path/size
  scan and normal rclone copy are not a checksum audit of every existing local
  file. Dropbox hashes can avoid remote ROM downloads but local hashing reads the
  card. No source or personal-cloud action. Direct microSD loading is suitable for
  the owner's Nova gameplay baseline, independent of later cloud-flow testing.

## In Progress

Record publication owner is `/workspace/tmp/pixelelated-upstream-adoption-20261012/delivery01`.
At stash creation it has not started. Inspect its actual files before any action:
original run.path/build.rc, inner.rc, outer.rc, result.json, hosted-checks.json and
consumption.json determine delivery status. A consumed owner is never rerun.
Earlier afb6cb4ef7 and0fc5a41e99 record deliveries are COMPLETE; their hosted checks
and original owners succeeded and were consumed. Never replay delivery01/02 from
`/workspace/tmp/pixelelated-m7-records-20261012-*`.

This delivery publishes records to next and the isolated source branch separately;
only next runs both hosted record/wordlist workflows, while a feature push runs
wordlist. Source branch receives the new next records before its push, so its
canonical handoff is current. Read actual refs and receipts, not pre-push hashes.
No external model/audit transfer has been started or authorized for this new packet.

## Next Steps

1. Verify/finish current record and isolated-branch publication, fresh handoff proof,
   required checks and original owner consumption. Public intake packet is the
   source of facts; no repeated device read is needed to resume.
2. On feature/m7-rocknix-20261001, repair #564 before source promotion. Read relevant
   rules first. Preserve old runtime and library links through download, extraction,
   validation and activation failures; prove successful replacement, interruption/
   retry and space handling with synthetic fixtures. Never execute the full Steam
   installer on host or owner devices. Whole installer sources /etc/profile and
   performs additional Steam/FEX operations. Existing controls extracted only the
   exact function with stub transports; installed VM acceptance remains owed.
3. Complete #493 mandatory retention/capacity enforcement before ANY new full cache
   copy/build. Current entrypoints monitor but do not enforce this lifecycle yet.
   Preserve source custody, cache mount contracts and original results. Measure
   disk/RAM/swap/PSI for the next build under D-INFRA-023.
4. Freeze repaired source; new GENERIC_X64 clean and retained-storage upgrade,
   full VM/local protocols/time-to-play and required independent review precede
   H700 then SM8550 builds. Map changed kernel/ABL/FEX inputs and #528 inventory.
   Previous audits remain scoped historical proof; do not replay their transfers.
5. Qualify native/boot-chain/device facts with any newly required named permissions;
   finish #528/#344/#265 publication/source/licence gates. No public RC allocated.

## Retained operational facts

- Accepted device source bc9dfe8141d9561dc1d8502313d00a84c4566ee8, identity
  0.0.1-dev+20261011T222153Z.gbc9dfe8141d9, ES c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78,
  rclone1.75.2. #557 RG SP and Nova acceptance complete; #556 RG35XX SP untouched.
  RG SP is H700 DDR3, not the RG35XX SP model. RG SP163 protected files and5
  recovery entries preserved; Nova configured safe scope0files/settings semantics
  preserved. Automatic sync was off at acceptance, not a claim about later owner use.
  Public docs/qa-logs/2026-10-12-owner-updates/. All original owners consumed.
- #493 first64-target cleanup recovered about396GB. Additional17-tree cleanup
  finished05:05:58UTC, consumed05:06:21, recovered1,983,355,252,736bytes. All paths
  absent/unregistered; original branches retained. Available3,018,397,261,824bytes
  at that measurement, current three caches about446GB. No root command pending.
  Public docs/qa-logs/2026-10-12-storage-retention/oldtrees/completed/.
- Source custody `/workspace/artifacts/pixelelated-build-custody/issue-493-oldtrees-20261012-03`:
  702inputs/16,307independentobjects/6,855,404,363bytes verified. Preserve current
  cache launch contracts: H70003 mounted at historical h70001 prefix, SM855003 at
  sm855001, VM replacement20 at m7-pixelelated. No old physical tree is needed;
  do not rewrite retained links. Older recovery payloads/failed custody duplicates
  remain a separate #493/#555 retirement tail, not authorization for deletion.
- #558 Nova one shutdown restarted into an ABL Linux-load error, then restart
  worked. Read-only logs captured; cause unknown, no pstore record, SM8550 has
  less persistent crash evidence than H700. Charging is an unproved lead. Keep
  monitoring; optional incident method/time/cable context remains unanswered.
  No deliberate shutdown reproduction is authorized. #560 fast shutdown future.
- #528 ABL implementation/source/licence and other publication gaps remain even
  with ABL1.2. No outbound upstream message or contact has been authorized here.

## Key Files and Related Context

- `docs/qa-logs/2026-10-12-upstream-adoption/`: exact merge review and source controls.
- `docs/decision-register.md`: D-WORKFLOW-161; `docs/releases/next-candidate-scope.md`
  and `docs/releases/rc-accept.txt`: active candidate references.
- M7 live priority: https://github.com/pixelelated/distribution/milestone/7.
- #563/#564 active; #493 next-build lifecycle; #528 publication; #559/#560/#562 backlog;
  #558/#561 watch items. Private current receipts:
  `/workspace/tmp/pixelelated-upstream-adoption-20261012/`.
- Prior full checkpoint: `archived/saved-session-state-next-20261012T170212Z.md`. Its jobs/priorities are historical.

## Notes for Next Session

Shell needs require_escalated because the stale harness sandbox fails its /tmp
synthetic .git initialization (quota), and current worktrees lie outside its
writable root. Use task-owned TMPDIR under /workspace/tmp; no general sudo.
Device reads filter key/pass/token/user/psk, private hashes/configs stay private.
Mutations need named authority and tools/device-act. Device alias rg35xxsp needs
Hostname override: RG SP100.75.221.73, Nova100.84.232.105. Do not connect merely to
reconstruct known state; owners are using both.

## Open Questions

No new base-selection answer is pending. Implement the selected exact release.
#558 optional historical details remain unanswered and do not block source work.
