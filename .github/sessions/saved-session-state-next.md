# Saved Session State

> **Saved**: 2026-10-12T20:45:14.417006+00:00
> **Branch**: feature/m7-player-setup
> **Repo**: pixelelated/distribution

## Start here

pixelelated is an immutable handheld Linux distribution. This is a build system,
not an app. Read next's AGENTS.md, every-session rule files and device-testing-policy
first, then the live M7 milestone. Harness conflict-resolution is stale; leave it
alone. Primary /workspace/repos/rocknix stays on next. Current worktree is
/workspace/repos/rocknix.worktrees/m7-player-setup, feature/m7-player-setup, from
next960b4d8c358b1e74b501ffdc329532be67cf7f6e. This delivery is records only.
There are no product edits, new firmware builds, or external audits this session.

All historical device deployments/reboots/cleanup approvals are consumed.
Read-only incident inspection was authorized; no new handheld mutation,
screenshot, input, sign-in, or cloud operation was performed. Owner devices
remain in normal use. No diagnostic VM or build is running after this checkpoint.
No private configuration, original incident account context, credential value or
credential-derived hash belongs in the public record.

## Current focus

Owner explicitly requested #565 → #566 → #567. Three subsequent reports became
#569 cloud provenance, #570 slow browser/hard reset, and #571 stable compact phone
connection status. #569 read-only diagnosis is complete; close only after this
record is published. #570 retained incident/VM triage is complete but its
underlying failure/recovery investigation remains open. No product fix has been
implemented for #565–#567, #570, or #571. M7 preserves that fact and the ordered
foundation/build gates below. Do not describe this documentation as repaired code.

## Completed this session

- #565/#566/#567 moved from backlog into M7.P5 at the owner's explicit request.
  Worktree created from current next; stable20261001 merge remains isolated.
- #569: local saved-backend and successful in-device sign-in history explain
  save-action availability. October9/12 preservation receipts retain existing
  selected folders. The original sign-in author is unknown; no current live
  provider reauthentication was performed. Public value-free packet:
  docs/qa-logs/2026-10-12-cloud-configuration/. Private diagnosis includes the
  specific old paths and provenance timeline; read it only if needed, never post.
- #570: post-reset readonly captures saved five device snapshots and all943
  previous kernel lines. Available RAM610→94→75→53MiB, WebKit roughly480–500MiB,
  and243 journal pressure flushes support severe memory pressure. No retained
  OOM kill, panic, storage I/O error, or pstore file establishes exact cause.
  GPU/clock warnings occur at boot before the browser and recur after reset.
  Browser window.log was volatile and did not survive. Do not claim a proved
  leak, user-agent regression, or successful crash reproduction.
- Bounded diagnostic VM20:1024MiB assigned rather than canonical8192MiB,
 640x480/software graphics; visible RAM791MiB and no guest PSI. Existing
  signin-memory loads example.org35s (279MiB summed peak RSS) and public login90s
  (385MiB). Both original results0 and reviewed frames prove initial page load,
  not authenticated navigation or input responsiveness. Direct launch leaves
  ES resident and local keyboard visible; this is not the real phone handoff.
  All browser processes later absent, available memory recovered to401MiB;
  immediate free-after118MiB was transient. Full device hang not reproduced.
- Watched boot/simple/provider owners all exited0. Exact QEMU stopped through
  tools/vm-stop; disk, UEFI store and QA key retired (2,245,111,808 allocated
  bytes). Retain compact docs/qa-logs/2026-10-12-browser-pressure/ only. Private
  owner /workspace/tmp/pixelelated-browser-qa-20261012 now has no live guest.
- #565 clean VM accounts: seven known default/runtime config surfaces contain
  zero populated player/developer account fields. This adds clean-boot proof,
  not universal secret absence, a retained-account upgrade, or a release gate.
- #571 source cause identified: cloud_oauth's open/loading already mean a live
  browser, but the phone changes from a short padded Connected banner to a
  longer loading paragraph. Different geometry moves controls. D-UI-126 records
  compact fixed header, accessible glyph and long-name ellipsis. No UI code or
  new baseline has landed; preserve the separate focused-field input gate.

## Record delivery

Owner directory: /workspace/tmp/pixelelated-browser-feedback-20261012/delivery01/.
state.json is prepared at checkpoint creation; publish.py, result.json,
head.txt and hosted-checks.json bind actual delivery. It pushes records to next
under existing commit/push authorization, not firmware publication. Inspect those
receipts before retrying; an absent result is not success or authority to replay
completed operations. Fresh-context agent m7_browser_incident_handoff verified
source/frame hashes, stopped jobs, retired payloads, issue order and boundaries.
Its two documentation ambiguities (owner-account request scope and delivery
locator) were corrected before commit. No product/audit acceptance is inferred.

## Next actions

1. Check this record delivery's actual git/hosted-check receipts; do not assume
   prepared documentation is pushed. The intended publication is the records
   commit merged into next by fast-forward. Both worktree and main began clean
   at960b4d8c35. Close #569 only with published evidence; #570/#571 stay open.
2. #570: reproduce bounded longer navigation/input and actual ES handoff in a
   disposable low-memory VM. Distinguish page working set from engine changes
   and hardware renderer pressure. Prior WebKit DMABuf workaround is still in
   the accepted source; don't remove it. A strict per-process limit may stop
   hangs while breaking login, so require ordinary navigation and explicit
   pressure/recovery proof before selecting a production change. Optional owner
   question: initial sign-in page versus password/verification at freeze; no
   answer is a new physical-test permission. No further device read is needed
   just to reconstruct known facts.
3. Continue #565: implement and prove an executable artifact credential gate;
   tools/fork-publish-release currently only prepares a release plan and lists
   credential inspection as still owed. Old rule prose describing its retired
   uploader is not executable proof. Preserve no-values reporting and synthetic
   negative controls; inspect final payload bytes. Add a disposable retained-
   account upgrade proof, without real account requests. Original Nova RA
   authorship remains unknown; existing private preservation receipts suffice
   to show unchanged owner state, not clean defaults.
4. #566: provider-supported dedicated pixelelated ScreenScraper identity.
   Official webapi2 page says developers request access through its forum.
   Public/shared JELOS credentials are not evidence of redistribution rights.
   Prepare a concrete request before seeking permission to contact anyone.
   Compiled-pair precedence already hides runtime developer rows; keep player
   accounts separate, backup exclusion and release gating. No provider outreach
   or credential embedding is authorized by merely filing the issue.
5. #567: conditional advance notice on UPDATE GAMELISTS that offline achievement
   preparation follows, only when the actual enabled/account/index gates apply.
   GuiMenu.cpp around8440 currently has only REALLY UPDATE GAMELISTS?. Inspect
   SystemData/ViewController actual gating. Update EN/FR canonical flow and
   source-bound640x480/1280x800 frames before promotion. #568 final-game versus
   finishing phase remains future work.
6. #571 follows those owner-ordered items before a new candidate: compact
   header in cloud_oauth REMOTE_PAGE (around958), phone_page translations near106,
   probe/poll around1257. Keep reachable/loading separate from field readiness;
   queued typing must not be sent into an unfocused page. Verify navigation,
   genuine failure/reconnect/session end, long headings, EN/FR narrow/wide
   actual browser frames and unchanged pointer/input. Existing Node controls
   are in tools/last-good-scripts-test C4 near6126; preserve their meaningful
   assertions when DOM markup changes. /home/max/.cache/ms-playwright has
   chromium1223; Playwright is in the uv cache, not global Python.
7. Repair #564 on isolated feature/m7-rocknix-20261001 before its source merge.
   #493 mandatory retention/capacity enforcement precedes ANY new full cache
   copy/build. Then freeze repaired source, clean/retained GENERIC_X64, full
   protocols/time-to-play/independent review, H700 then SM8550, and #528/#344
   publication/source/custody gates. No public RC has been allocated.

## Exact source and environment

Accepted devices: bc9dfe8141d9561dc1d8502313d00a84c4566ee8, ES
c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78, rclone1.75.2. Accepted VM20:
1a026648442321609b2288c2c9c06803817f9df2. Browser C/cloud_oauth/WebKit recipe/
machine-info bytes match across those two sources. October9→12 did not change
WebKit or CHASSIS; September29→current changed2.54.0→2.54.1 and CHASSIS=handset.
Owner's earlier responsive baseline is not source-bound.

ES repo /home/max/Development/emulationstation-next currently checks out old
67f92692c3; read accepted pin with git show, create a separate feature worktree
from c8dc72cf9e before editing. launchCloudSignIn in ApiSystem.cpp561 opens the
browser then suspends the renderer. Window::deinit unloads resources/renderer;
it does not discard the whole game database or exit the process. Incident
snapshots cannot prove actual memory freed.

Accepted image/TAR reside in m7-pixelelated-replacement20/target. Recreating a
16GiB diagnostic disk is cheap and intentional; no retained diagnostic disk.
Use canonical generic-x64-vm unless explicitly documenting the low-memory
fixture override. Never mistake assigned1024MiB for observed guest RAM or a
loaded first page for successful authentication.

Shell requires require_escalated: stale harness sandbox fails synthetic /tmp/.git
mount with quota errors, and active worktree is outside its writable root.
Use task-owned TMPDIR under /workspace/tmp. No general sudo. RG SP is H700 DDR3,
not RG35XX SP; Tailnet100.75.221.73. Nova100.84.232.105. SSH alias rg35xxsp needs
Hostname override. Read only with credential filtering; mutations through
 tools/device-act require applicable named authority, none new here.

## Private evidence locations

- /workspace/tmp/pixelelated-nova-cloud-20261012/: #569 original report,
  value-free classifiers and private folder/provenance results. Automatic
  review rejected posting the original incident account context; sanitized
  issue succeeded. Do not retry posting private context.
- /workspace/tmp/pixelelated-browser-feedback-20261012/: original #570/#571
  reports, crash/readback.json and kernel-readback.json, tracker before/after.
- /workspace/tmp/pixelelated-browser-qa-20261012/: consumed VM diagnostic
  scripts/results; disk and keys gone. Earlier optional PSI probe failed because
  guest has no file; original error was preserved, not hidden by page PASS.
- /workspace/tmp/pixelelated-owner-deploy-20261012/nova/: existing private
  before/after #557 preservation receipts; no new owner config hashes captured.

## Retained release facts

Stable20261001 exact c445081a59518f37d9776e5412dd7b14910696f7 selected by
D-WORKFLOW-161. Isolated source branch62e9929fdce5d44ceb7f68150770475c568d1ac2
contains merge f370dc8787 and #564 Steam replacement regression; keep out of
next until repaired. Source-intake delivery03/04 completed before this session;
original failed deliveries remain failures, do not replay them.

All #557 deployments and both #493 cleanup batches complete; about3TB free,
three retained caches roughly446GB. Preserve historical container mount paths
for H70003/SM855003/VM20; never rewrite retained symlinks or mutate frozen trees.
#558 Nova shutdown and #561 LED are watch items; #562 ROM integrity future;
#528 source/licence/offhost custody holds remain. All earlier external audit
approvals were consumed; a new external packet needs applicable authorization.
Full previous checkpoint: archived/saved-session-state-next-20261012T204514Z.md.
