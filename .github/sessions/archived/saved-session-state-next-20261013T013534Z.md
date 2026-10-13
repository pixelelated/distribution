# Saved Session State

> **Saved**: 2026-10-12T22:07:06.260649+00:00
> **Branch**: feature/m7-player-setup
> **Repo**: pixelelated/distribution

## Start here

pixelelated is an immutable handheld Linux distribution, not an app. Read next's
AGENTS.md, every-session rules and device-testing-policy, then the live M7 milestone.
Harness conflict-resolution is stale; leave it alone. Primary /workspace/repos/rocknix
stays on next. Active /workspace/repos/rocknix.worktrees/m7-player-setup is
feature/m7-player-setup, starting from published515cd8e79a94b3a8596128e25e28875093f5eb50.
This session diagnosed #570 browser pressure and filed #572 packaging failure.
No product source changed, no new firmware or external audit ran. No test is still
running; all guest/probe processes exited and immediate disk/key/test files retired.

The owner's latest authority is: "If you need to test anything on the RG35XX SP,
you have my permission to do that as well when it comes to WebKit testing."
It covered the described bounded public-page launch, native screenshots, pressure
sampler and temporary cleanup through tools/device-act. Actual identified device
is H700 RG SP DDR3. No account setup, cloud data action, injected input, settings
change or reboot occurred. Device returned to ES with recovered memory. Do not
infer unrelated device authority or replay historical deployment/cleanup approvals.
Respect the scope of the current WebKit authorization without asking for it again.
No private account context, credentials or credential-derived hashes in public QA.

## Current focus

Severe H700 sign-in memory pressure is reproduced, but its historical cause is not
proved. Every tested runtime is WebKit2.54.1. The next discriminating work is a
controlled older-engine runtime comparison and real navigation/input/normal ES
handoff/recovery proof. #572 requires a scoped GStreamer package repair; supplying
missing components removed warnings without reducing browser memory. No production
optimization or downgrade has been selected. M7 then preserves the owner order
#565→#566→#567→#571, isolated stable20261001 repair/build and publication gates.
#569 configuration diagnosis was published in515cd8e79a and is closed completed.

## Completed this session

- Nine bounded VM20 cases: installed browser, September29 application/current
  engine, desktop UA, DOCUMENT_VIEWER cache, synthetic navigation/cache/focus-poll
  controls, injected GStreamer runtime pieces, accelerated VM graphics. All pages
  load, browser PSS380–394MiB and minimum available49–71MiB. No useful RAM benefit.
  Guest1024MiB assigned/791MiB visible,640x480,ES resident,4Haswell CPUs,no PSI.
  First8 software graphics, last verified virtio-gpu-gl/EGL. These are diagnostic
  direct launches, not normal ES suspension/phone bridge/authentication proof.
- Synthetic4-page80MiB-per-page fixture: maximum heartbeat gaps4.60/5.75/1.08s for
  default/cache/no-focus-probe. Potential latency lead only: one ordered trial,
  no injected input, back/popup or handoff acceptance. Do not remove the probe
  based on this one comparison; it gates safe field typing.
- Explicitly authorized H700 public-page control: simple35s leaves522MiB,
  browserPSS134.5MiB; login reaches160MiB guard at34s, minimum153MiB, browser502MiB,
  page-process430MiB (372MiB anonymous). Closing restores572MiB; same boot and ES
  process survive. All browser children exit; temporary test tree removed through
  device-act.11 reviewed native frames retained (H700720x480, VM640x480).
  Full hang, leak, JavaScript heap attribution or engine regression not proved.
- #572 source/VM failure: generic GStreamer hook removes controller required by
  shipped GL plugin; tools=disabled suppresses scanner. Fresh private-registry
  original rc1; exact retained target controller and freshly compiled matching
  scanner rc0, appsink/glupload register. Browser warnings disappear but389MiB
  PSS persists. Diagnostic injected files lived in VM only; no recipe fix yet.
- Source archive diff2.54.0→2.54.1 retained. Existing DMABuf workaround is active
  in VM children. The old246MiB Dropbox baseline was a failed page, corrected in
  #228; October5 loaded-login evidence already shows379–386MiB summed RSS. Do not
  compare RSS numerically as if it were PSS or claim every older build equivalent.
  Owner's earlier responsive source is unknown. Inspected retained inputs did not
  contain a usable older engine runtime; narrow isolated package build needed.
- Five actual watched owners/build/wrapper channels0 and exited. Original
  boot-owner rc2 unsupported--qa and graphics-owner rc2 worktree lock remain
  pre-workload failures. Corrected owners ran sequentially. No in-flight edits.
  QEMU exited;2,247,143,424allocated disk/UEFI/key bytes retired. Nothing running.
- Public compact packet: docs/qa-logs/2026-10-12-browser-isolation/README.md,
  manifest, VM/physical samples, reviewed frames/hashes, source diff, fixtures,
  original channel/retirement receipts. Physical runnable script stays private.
  #570/#572 and M7 updated/read back. #570/#572 remain open; no product closure.

## Record delivery

New owner: /workspace/tmp/pixelelated-browser-isolation-20261012/delivery02/.
state.json is prepared at checkpoint creation. publish.py, launcher-result.json,
result.json, head.txt and hosted-checks.json bind actual delivery; read them before
any retry. This commits records, fast-forwards next and pushes under existing
approval, then consumes both exact-head record/wordlist hosted checks. It is not
firmware publication. No success is implied by this prepared paragraph. Fresh
session-stash reviewer m7_browser_isolation_handoff passed source/payload/frame
hashes, raw aggregates, original results/exits/retirement, exact diff wrappers
and live milestone order. It correctly found delivery still prepared. Review
receipt: handoff-review.md in that owner. No substantive discrepancy found.

Original browser-isolation delivery01 ended1: pre-push refused a missing #570/#572
commit-message reference after local integration. Remote stayed515cd8e79a; all
original channels/exits consumed. The unpublished owned commit is corrected and
only a fresh delivery02 may push. No test result or guard is bypassed.

Prior /workspace/tmp/pixelelated-browser-feedback-20261012/delivery01 is COMPLETE,
head515cd8e79a, both hosted checks successful, actual owner exited. Do not replay.

## Next actions

1. Consume this record delivery's actual result/launcher/build/hosted-check channels
   and git readbacks. If already successful, do not replay. Keep #570/#572 open.
2. #572: scoped fork GStreamer recipe repair keeps libgstcontroller and builds/
   installs scanner at /usr/lib/gstreamer-1.0/gst-plugin-scanner. Read packaging
   rules, inherited hooks and existing trimming rationale first. Actual package
   install proof, pkgcheck and fresh-registry negative/success controls are owed;
   next assembled image verifies runtime closure. Diagnostic injection is not
   corrected package evidence. Do not mutate frozen replacement20's cache.
3. #570: provision an isolated older-engine runtime comparison against exact
   current source.2.54.0 and2.54.1 source archives remain; inspect ABI/build graph
   before choosing the narrow package build. No full cache copy/build until #493
   lifecycle enforcement. Repeat/reorder synthetic navigation and focused-field
   timing, exercise normal ES handoff and safe recovery at handheld-like limits.
   Do not treat loaded frames as usability or infer cache/process limits are safe.
   Existing mutation-free readback/source evidence suffices; no owner credential
   use is needed. No test or background build is currently running.
4. Continue #565: implement and prove an executable artifact credential gate;
   tools/fork-publish-release currently only prepares a release plan and lists
   credential inspection as still owed. Old rule prose describing its retired
   uploader is not executable proof. Preserve no-values reporting and synthetic
   negative controls; inspect final payload bytes. Add a disposable retained-
   account upgrade proof, without real account requests. Original Nova RA
   authorship remains unknown; existing private preservation receipts suffice
   to show unchanged owner state, not clean defaults.
5. #566: provider-supported dedicated pixelelated ScreenScraper identity.
   Official webapi2 page says developers request access through its forum.
   Public/shared JELOS credentials are not evidence of redistribution rights.
   Prepare a concrete request before seeking permission to contact anyone.
   Compiled-pair precedence already hides runtime developer rows; keep player
   accounts separate, backup exclusion and release gating. No provider outreach
   or credential embedding is authorized by merely filing the issue.
6. #567: conditional advance notice on UPDATE GAMELISTS that offline achievement
   preparation follows, only when the actual enabled/account/index gates apply.
   GuiMenu.cpp around8440 currently has only REALLY UPDATE GAMELISTS?. Inspect
   SystemData/ViewController actual gating. Update EN/FR canonical flow and
   source-bound640x480/1280x800 frames before promotion. #568 final-game versus
   finishing phase remains future work.
7. #571 follows those owner-ordered items before a new candidate: compact
   header in cloud_oauth REMOTE_PAGE (around958), phone_page translations near106,
   probe/poll around1257. Keep reachable/loading separate from field readiness;
   queued typing must not be sent into an unfocused page. Verify navigation,
   genuine failure/reconnect/session end, long headings, EN/FR narrow/wide
   actual browser frames and unchanged pointer/input. Existing Node controls
   are in tools/last-good-scripts-test C4 near6126; preserve their meaningful
   assertions when DOM markup changes. /home/max/.cache/ms-playwright has
   chromium1223; Playwright is in the uv cache, not global Python.
8. Repair #564 on isolated feature/m7-rocknix-20261001 before its source merge.
   #493 mandatory retention/capacity enforcement precedes ANY new full cache
   copy/build. Then freeze repaired source, clean/retained GENERIC_X64, full
   protocols/time-to-play/independent review, H700 then SM8550, and #528/#344
   publication/source/custody gates. No public RC has been allocated.

## Exact source and environment

Accepted devices bc9dfe8141d9561dc1d8502313d00a84c4566ee8, ES
c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78, rclone1.75.2. VM20 source
1a026648442321609b2288c2c9c06803817f9df2; browser C/cloud_oauth/WebKit recipe/
machine-info match device. Historical application control full source
69e6039f8fdbf971d3e6b694537f250036fdcd98 uses current2.54.1 engine.
October9→12 engine/CHASSIS unchanged;2.54.0→2.54.1 on October2, CHASSIS=handset
on October1. Engine archive/source comparison is in the packet, not runtime proof.

ES repo /home/max/Development/emulationstation-next checks out old67f92692c3.
Read accepted pin with git show and create a feature worktree from c8dc72cf9e
before editing. launchCloudSignIn ApiSystem.cpp561 opens browser then suspends
the renderer. Window::deinit unloads resources/renderer, not the entire database.
No experiment this turn measured that full handoff.

Accepted image/TAR remain in m7-pixelelated-replacement20/target. Its toolchain
symlinks require its original mount prefix /workspace/repos/rocknix.worktrees/m7-pixelelated.
This turn's small binaries compiled with retained cache mounted read-only in
Docker and task owner as /work; exact fixtures are preserved. Do not alter frozen
symlinks. Recreate a fresh private guest/key for new tests; old ones are gone.

Shell requires require_escalated: stale sandbox fails synthetic /tmp/.git mount
quota, and active worktree is outside its writable root. Use owned TMPDIR under
/workspace/tmp for hooks; no general sudo. tools/watch-build does not accept --qa;
use documented --activity-dir if needed. It locks one job per worktree, including
QA. Read tools/watch-build-submit parser before launching, use fresh owner and
consume original channels/actual exits. Active supervision required; no off-session
alert system. RG SP Tailnet100.75.221.73; rg35xxsp alias needs Hostname override.
Nova100.84.232.105. Physical mutations go through tools/device-act with applicable
authority; record physical exception before testing. Don't confuse two H700 models.

## Private evidence and retained context

- /workspace/tmp/pixelelated-browser-isolation-20261012/: original cases, samplers,
  tool owners, result channels, compile outputs, private device readback and
  plan/cleanup/action receipts. No guest/disk/key or device probe remains. Public
  packet omits physical identifiers. delivery02 owns only the new records push; failed delivery01 must not be replayed.
- /workspace/tmp/pixelelated-browser-feedback-20261012/: earlier incident and
  original reports; crash saved five snapshots/all943kernel lines. RAM610→53MiB,
  243pressure flushes; no recorded OOM/panic/storage cause. window.log lost at reset.
- /workspace/tmp/pixelelated-nova-cloud-20261012/: #569 private provenance/selected
  folder results; never post original account context. Sanitized public packet is
  docs/qa-logs/2026-10-12-cloud-configuration/. Owner sign-in author remains unknown.
- /workspace/tmp/pixelelated-browser-qa-20261012/: earlier consumed low-RAM test;
  guest/key/disk retired. Original PSI absence remains recorded.
- /workspace/tmp/pixelelated-owner-deploy-20261012/nova/: private preservation
  receipts, not authorization for new config/hash operations.

Stable20261001 c445081a59518f37d9776e5412dd7b14910696f7 selected by D-WORKFLOW-161.
Isolated feature/m7-rocknix-20261001 at62e9929fdce5d44ceb7f68150770475c568d1ac2
includes merge f370dc8787 and #564 Steam replacement defect. Keep out of next until
repaired. Prior source-intake delivery03/04 complete, original failures retained.
#493 both cleanup batches complete, source custody retained; do not replay. Last
capacity roughly3TB free/three446GB caches, not a new current measurement. Required
6.855GB custody at /workspace/artifacts/pixelelated-build-custody/issue-493-oldtrees-20261012-03
must remain. Mandatory future retention/capacity enforcement is still not implemented.
#558 shutdown/#561 LED are watch items; #562 ROM integrity/#568 final-game progress
future. #528/#344 source/licence/offhost custody gates remain; no public RC allocated.
All earlier external review packet approvals were consumed, no audit running.
Previous full checkpoint: archived/saved-session-state-next-20261012T220706Z.md
