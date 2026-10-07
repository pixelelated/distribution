# pixelelated 0.0.1 release readiness

## Current device builds — 2026-10-07 04:51 UTC

#492 H700 arm compatibility is accepted from frozen `43d0bc3bf4`: all 244
tasks complete, four zero results, seven unchanged seals and actual builder
exit. Independent acceptance hashed 7,866 files, checked 797 symlinks and
938 ARM ELF objects, including RetroArch and libretro cores. #497 repairs
the generated-name path mismatch with 42 original/fixed controls and package
lint; it remains open for the actual aarch64 handoff/image evidence.
Earlier failed owners, logs and interrupted package scopes are preserved.

Next is H700 aarch64 firmware, then SM8550. No bootable firmware is claimed.
The post-arm capacity gate has 161.83 GiB available against 267.74 GiB needed
for H700 firmware. #494 independently preserved all 14,489 custody objects
and completed dependency discovery. Under the subsequent D-INFRA-022 policy,
replacement09/10/12/14 offer 432.57 GiB potential net recovery: completed QA
source links are historical inputs with independently preserved exact source.
The maintainer has now requested immediate broader cleanup, prioritizing durable
test records over completed VM disks (D-INFRA-021/022, #493). Every large test
artifact now requires a named active or immediately queued test and a release
condition. The revised ordinary-payload selection is all 263 completed QA disks
and 587 old firmware files, 1,415.07 GiB; both hash passes and external-reference
classification are accepted. Five firmware files have temporary test-specific
recovery holds. The plan retains 50,983 compact records. Guest disk recreation
took about eight seconds from retained firmware, separate from boot/test time.
The broader read-only administrator process check supersedes the four-tree one.
No removal has yet occurred. See `docs/qa-logs/2026-10-07-storage-retention/`.
Physical actions, source/licence/public docs and publication remain gated.
See `docs/qa-logs/2026-10-07-device-builds/README.md`.

## Software qualification complete — 2026-10-07 02:48 UTC

Candidate 16 has completed the M7 P4 fixes audit: all eight findings have
resolved outcomes, with no deferrals or withdrawals. The approved primary
review and both Fable passes are complete; no further model call is required.

- Distribution: `ee014909137e03706e0b3020b8396be589aaa705`.
- EmulationStation: `72494bc72e3d64d4dcfeb4e6478052bbdf166c5b`.
- Immutable bundle: `7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a`.
- QA20: all 15 default suites; 78 comparison screens with no unclaimed,
  missing or stale differences; 26 actual ROCKNIX RC2 upgrade checks; clean
  and upgraded identity, virgl and software rendering accepted.
- Cloud02: 318 checks, 106 each on actual local WebDAV, SFTP and MinIO S3;
  zero failures or skips. No Dropbox credential check is required.
- Changed cloud behavior: actual interrupted-copy retry, historical shelf
  recovery, sibling preservation, truthful refusals/timeouts, original-
  connection repair, supported legacy restore and EN/FR folder routing pass.
  Direct frame reviews and original-state hashes are retained with each proof.

All accepted runs have verified terminal results, unchanged input seals and
actual process/backend cleanup. The original failed runs remain failed;
their corrected controls and later accepted runs are separately identified.
The interruption copy requested in #482 is included and already closed.

Evidence: `docs/audits/2026_10_06-milestone-m7-p4-fixes-383/08-installed-resolution.md`
and `docs/qa-logs/2026-10-07-pixelelated-replacement-16/`. The original forward
audit grades remain historical; later dispositions are mapped in audit09/10.

Acceptance is published on next `7f293a22d97317d1632952a5cf2e9d4a45bd2cb2`.
#471, #467, #468, #478, #479, #361, #386, #327, #409, #383 and observer repairs
#487/#488 are closed completed, with exact body/state readbacks. Live audit lint
confirms all eight checked findings and resolved outcomes. Current: M7.P5 #492
H700 arm build and #494 retention review, then H700 aarch64, SM8550, and the
separately gated physical/P5 work.

This is software qualification, not RC designation or release publication.
The 14 known component licence/source metadata gaps, corresponding-source
bundle, public documentation and physical-device facts retain their P5 gates.
Earlier RA award and 125-game proofs carry explicit unchanged-source/byte
custody; no new award/reset or live upstream-freshness query is claimed.
The completed two-file retirement authorizes no broader deletion.

## Historical qualification records

## Historical candidate15 status — superseded by current execution above

## Current work — P4 remediation, 2026-10-06 22:58 UTC

Both approved Fable calls and primary grading are complete. Audit #471 has
eight findings: PL-002/006/007/008 are resolved from installed evidence; four remain
open. Candidate15 is frozen at distribution
`ed5a6a51f5974deec8748fbf0dbd2f4984b690f5` and ES
`bab4df649f48847cc43d21c77c058107ad902754`. Its build, bundle, raw/update
SYSTEM equality and full QA19 pass, including all 15 default suites and actual
ROCKNIX RC2 upgrade preservation. Sweep11 classifies all 8,604 branding
contexts and all credential-pattern matches. Inventory11 retains 14 known P5
licence metadata gaps. [Evidence](../qa-logs/2026-10-06-pixelelated-replacement-15/README.md).

Installed follow-up checks exposed two remaining defects: a successful move
can leave RC2's `/GAMES-replaced` history behind, and legacy-root game rows
can show a false unsupported-system label. Neither establishes data loss.
The published repairs pass 376 real-rclone source cases and specific failing
old-source controls. They still require a new engineering image and installed
acceptance. UI04 completed, exposing a clipped French settings-read reason that remains
PL-005. Recovery06 passes all eight EN/FR behavioral cases, with verified
owner/guest/backend cleanup and all46 frames reviewed. Three frames retain
reason/instruction clipping; bounded ES source fixes pass compiler/msgfmt but
need rebuilt visual proof. Four punch findings remain open. Library01 failed its timing/isolation fixture checks and is retained under#474.
Corrected library02 passes415 assertions with11 seals, four zero results and verified cleanup.
Boot09 and bucket02 pass with verified cleanup.

Coverage05 exposes installed retry defect#479: after a real258048/8391392byte copy is killed, all original data/pointers and the recovery record survive, but actual TRY AGAIN refuses the partial destination. The exact-file resumable guard supports completed subsets, not truncated files. Allfour1/10seals and actual cleanup23:00:41/45 are retained; no retry acceptance and no data-loss claim. Repair remains within openPL003. #478 now distinguishes the successful injection from this product failure. Source repair must preserve foreign-folder refusal and original connection/pointer binding, with full regression and rebuilt16 actual interruption/UI proof.

Freshroot07 completed23:08:00; primary23:08:31 allfour0/10seals,23:08:36 actual guest/backend cleanup and free ports. Actual generated settings archive, settings/content uploads, automatic save receive/send and independent backend listing pass; every retained cloud hash rechecked against runtime bytes. Installed ES restarted, exact identity/post-payload check passes, cloud bytes unchanged. Failed06 remains allfour1 with its missing ES restart under#480. #477 settings-only and all remaining coverage dispositions are now recorded; the actual partial retry remains a separate product defect#479/#478.

Historical no-join02 completed23:18:40; primary23:18:52 verified allfour0/21seals and owner exits,23:18:55 verified both guests/backend/ports stopped. Actual RC2→retained1ac update preserves populated ROCKNIX pointers/cloud bytes. Fresh historical1ac directly reads the earlier save with its own installed client, then its supported full scan reports current/SOURCE=-, seeding does not join any of the three earlier pointers, and successful default restore transfers0bytes without the witness. All original bytes survive. Every runtime cloud hash is independently rechecked in nojoin02-acceptance-01. This supplies the exact historical negative for I354-L66; no new Rasteratops adoption gate. Failed01 remains a fixture error under#481.

Refined partial-retry-host02 completed; primary `2026-10-06T23:22:50.529406+00:00` verifies allfour0/27seals, no owner process,22focusedPASS/398fullPASS,4old-source expectedFAIL and5oldrefusal controlsPASS. Exact tested source/tool snapshots retained. The guard requires a validated prior record and verifies every destination byte against the source prefix; unrelated/missing/changed/longer files, wrong binding, failed reads/listings and unrecorded partial destinations are refused. Content is checked before creating a record or advancing any tier. Intermediate host01 and its failing missing-record Content control stay retained. Source acceptance only: installed16 must pass actual interruption/UI retry and next backup shelf before#479/PL003 can close.

Next: integrate tested source/ES fixes and build16 → actual truncated-copy/UI retry plus affected/final installed acceptance → #471/P4 closure → capacity#461 → H700 DDR4 RG35XX SP arm, thenaarch64 → named physical/P5 gates. PL001/003/004/005 remain open. No RC designation; no pending approval. #477/#480/#481 fixture criteria verified; close after evidence publication.

## Historical qualification — earlier status statements retain their dates

Replacement12 remains frozen55d8ee8f75965a560f75d187e34c9beaa93133f1;
its build, scoped preservation/native/HTTP and QA15→17 evidence are retained
[with their limitations](../qa-logs/2026-10-05-pixelelated-replacement-12/README.md).
Installed consent01 subsequently failed the positive counter control after
24 negative/restart checks. It remains failed; all owned processes exited.

#457 identifies upstream's0.0 consent-cache sentinel: during uptime below
30seconds, a granted choice is not initially read. Patch019 fixes initial and
invalidated observation without changing persisted consent or stored formats.
Selected upstream879b158 changes Android only; Linux/native trees and coupled
pins are unchanged. All16 patches apply without fuzz;818 native-enabled Linux
tests and11 integration cases for each actual303/historical865 predecessor
pass. [Source proof and failed installed run](../qa-logs/2026-10-06-proxy-consent/README.md).

Replacement14 source `7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2` built
successfully at00:59:09UTC2026-10-06:642/642tasks, allfourresults0,
actual container/process exit00:59:32. Immutable bundle
`b77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1`
verifies. [Build evidence](../qa-logs/2026-10-06-pixelelated-replacement-14/README.md).

Installed consent02 passes all30reporting/restart cases, including the
first granted counter at16.705487703seconds (7→8). Image14 verifies raw/update
SYSTEM equality; inventory10 passes with the14knownP5licence gaps retained.

QA18 completed01:41:30UTC with all15default suites and26actual ROCKNIX RC2
upgrade assertions passing. All78walk frames compare with0unclaimed changes;
installed virgl/Pixman and identity checks pass. Proxy14 completes22offline
preservation checks,18native tests with0skips and four legacyCHD cases.
Subset11 completes35loopback HTTP preservation/refusal/retry assertions.
Every owner has four zero results and verified process cleanup. No build or
QA job remains active. Timing remains a single-sample smoke with its recorded
rapid-relaunch/no-new-stamp limitation; no wider performance claim is made.

Local WebDAV, SFTP and MinIO/S3 qualification (#462) is complete: each has
106 PASS, 0 FAIL and 0 SKIP, for 318 assertions on unchanged replacement14.
All four watcher results are zero; actual cleanup verifies all owned processes,
VMs and backends exited. [Local cloud evidence](../qa-logs/2026-10-06-local-cloud/README.md).

The ordinary RetroAchievements proof is now complete: after the confirmed
reset, fresh owner ra01 passed33 assertions, no failures/skips. The real
softcore award survived exit offline, flushed on reconnect, appeared in the
provider API and was recognized on relaunch. All four results0 and actual
cleanup/account-clear verified. [Award evidence](../qa-logs/2026-10-06-ra-award/README.md).
The reset is now consumed. Those exit frames remain carousel-only evidence.
The remaining reconnect-card proof (#465) now passes separately on unchanged14:
109 assertions,23 directly reviewed frames, EN/FR at640x480 and1280x960,
success/refusal/empty-repeat controls. Allfourrc0; actualcleanup07:01:20.
[Installed UI proof](../qa-logs/2026-10-06-ra-ui/README.md) uses synthetic local
HTTP and unchanged installed components; it does not claim another real award.
Two earlier harness attempts are preserved as superseded. No job is active.

Current order: continue the serial P4 independent audit, resolve and requalify
its findings, then measured capacity, H700 arm/aarch64 and named physical/P5
gates. [Audit record](../audits/2026_10_06-milestone-m7-p4-fixes-383/README.md).
The primary audit is complete through4.5:261criteria (204PASS/36PARTIAL/3FAIL/
18SKIP),123prior comparisons and full retrospective. External Fable5.1/xhigh
blind and refutation calls are complete and verified: served Fable5.1/xhigh,
no retries, all result channels0, unchanged sealed inputs and actual owner cleanup.
All14 blind/five refutation leads are graded against primary artifacts and14
completed installed experiments. Mandatory audit#471 carries eight open findings
(1High/6Medium/1Low); final05 and all proof/cleanup receipts are retained. No
executable is running. Product unchanged; Phase7 fixes/requalification precede
P4 closure or any RC claim. #470 pre-issue validation passes, while the default
resolution check correctly refuses all eight open outcomes.

The unchanged14 content probe confirms #467: unrelated configured directories
suppress the chooser/fallback, and root game folders on an empty device are
misclassified. Three controls pass and four challenged fixtures fail; four rc1
results and actual cleanup are retained. #468 captures safe future-layout
refusal with a misleading missing-folder message. These findings prevent RC
clearance until repaired and requalified. #469 additionally records the missing
approved French phone/native finishing text. Refutation03 independently repeats
all seven content cases with identical outputs, four expected rc1 channels and
actual cleanup. No product patch/new image yet.

The earlier proof receipts above retain their original scope; passing them did
not establish these newly challenged cases. D-QA-058 keeps hosted accounts and
offsite endpoints optional; #463 remains unverified, #464 reset automation is
backlog. #466/D-WORKFLOW-149 requires continuing authorized audits after saving.
Both cross-lab calls are complete; current remediation execution is recorded above.

Frozen13 freshness caught an Android-only upstream commit before any cache
copy/build. [Exact equality evidence](../qa-logs/2026-10-06-proxy-879b158/README.md)
links the new pin to the completed source suites; no test execution is invented.

#459 completed the five approved old-tree removals: 539.34 GiB recovered,
576.45 GiB available, reserve unchanged. [Final verification](../qa-logs/2026-10-05-build-storage/approved-cleanup-20261006/README.md)
rehashed15,206retained files plus the19current bundle files; frozen14inputs,
27sourcegitinputs and230surviving backingchains pass. All protected artifacts
remain; the root watcher exited automatically. #460 fixes the cleanup helper's
read-only-directory handling with six controls. Those owners have all exited;
#462 owns the subsequent local-cloud QA run. This changes host cleanup, not product bytes or RC readiness.

#461/D-INFRA-018 now records retention review after qualification and capacity
review before the next build. The recurring planner and next cleanup batch are
infrastructure follow-up, outside the RC gate; no further deletion occurred.

#168 now has ten tested upstream drafts. Seven additional standalone drafts
cover001/002/005/007/008/013/015:40 targeted tests and169 related-suite executions
pass, with before-fix failures and exact distributed patch hashes retained.
[Contribution evidence](../qa-logs/2026-10-06-upstream-drafts/README.md).
Upstream main remains879b158. API/policy-dependent proposals have explicit
reasons in the contribution map; no upstream submission or acceptance is claimed.
The separate RA account proof is complete in the record above; no new build
has started. P4 is remediating the eight verified findings in#471; local qualification is recorded
under #462.

> Earlier dated records below preserve their original account limitations.
> D-QA-058/#462 supersedes any Dropbox-account prerequisite; #463 is optional.
> No earlier public/synthetic page is asserted to prove authenticated behavior.

## Completed installed GENERIC_X64 Pixman fallback (#447)

The permanent selector is published as next `d6e8390c93bed87efe2dcc23cd402a271cacd1c7`
(feature `2feafc12d2fea9ada9730156cb9340b01a3a4e26`). It affects only GENERIC_X64:
no negotiated virgl selects Pixman, while accelerated guests, explicit renderer
choices and unknown configurations retain their existing path. Both actual GPU
profiles pass 22 selector controls each. These 44 checks prove selection, not
installed-image qualification. #450's fixture repairs are closed with original
failures retained.

Replacement10 is frozen at that commit; manifest
`0b24bfcd0d7dad134872b88ed6a2955ddaf9cdf9d55f8a25c17fa5e2de36ad51`.
Build02 completed19:26:30 with all four result channels0; actual047d1c at
19:26:43 proves four owner processes absent and the observed container removed.
The installed selector/drop-in match frozen bytes. Cache checks passed2526399
independent files. First build attempt remains failed on swap preflight before
compilation; the installed guarded helper reclaimed swap before fresh build02.

QA14 now passes all15default suites and26actualROCKNIXRC2 upgrade checks.
Frame comparison:21expected regions,0unclaimed,0missing. All15identity frames
were directly reviewed; installed clean/upgraded virgl and upgraded software
Pixman proofs pass. Durable20:06:08/allfour0; actual2a3cd7 plus supplemental
cleanup confirms4owner/6guest PIDs absent. Single-sample timing smoke passes;
the fast game-to-game sample lacks a new sync stamp and does not establish
active-sync behavior (retained timing-review.json).

Boot05 passes all four clean/actual-upgraded software boots at640/1280 with
exact1.0matches and12negative rejections; allfourframes directly reviewed.
Installed clean software/signin14, actual-upgraded software/signin15 and
acceleratedvirgl/signin16 each pass40checks and15directlyreviewedframes.
Allnine finishing comparisons per profile match unchanged pixels without
runtime overrides or forced repaint. Actual terminal and cleanup receipts
are retained under replacement10. Authenticated trust remains separate.

Memory12 passes original10/10/50measured launches, all55sync stamps and both-
profile exit/time-to-play. Growth0/224,-448/684,0/444KiB stays below unchanged
1024/2048KiB limits. Actual owner/guest/backend cleanup verified. UI14 passes
all 70 directly reviewed English/French frames at 640x480/1280x960 and all
12 ES process-lifetime checks. Both actual 1 GiB software/Pixman workloads
load and remain responsive for 30 seconds without OOM: baseline peak
271416 KiB, public Dropbox peak 395676 KiB. Their actual loaded frames were
reviewed, all result channels are zero, and all owner/guest processes exited.

All planned affected qualification for #447 is complete. Exact receipts,
frames, sources and limitations are retained in
`docs/qa-logs/2026-10-05-pixelelated-replacement-10/README.md`.
Next: reconcile remaining P3 criteria and QA-account proofs before P4.
Earlier replacement09 evidence remains historical.
P4 and H700 follow remaining P3 acceptance; no RC/device-ready claim.

## Historical diagnosis — ROCKNIX RC2 replay and working Pixman experiment

The maintainer asked why the last ROCKNIX build had not exposed this fault.
The actual September29 RC2 image69e6039f8f (SHAe2b662ba) reproduces host-stale
software frames on today's host; native is correct. Its accelerated control
has all nine frames exactly equal. Original September29 reports explicitly
record virgl/renderD128; the sixteen recorded walks do not test browser
finishing native-versus-host. Thus renderer and coverage explain a concrete
historical blind spot; the exact September29 software-host behavior is unknown.
Source changes and new branding are not necessary to reproduce it.

Current-candidate Pixman diagnostic14 gives nine correct host/native frames;
matched GLES2/llvmpipe diagnostic15 reproduces stale/partial host frames with
the same restart/debug setup and identical actual QEMU arguments. Pixman uses
DRM dumb buffers; GLES2 uses GBM. Both use atomic DRM. Exact faulty component
is not established. All36 RC2/Pixman/GLES comparison frames were directly read.
See historical-render-comparison/rc2/README.md and pixman.md in the replacement09
QA directory. All original failures remain immutable.

Full software/Pixman signin-ui13 PASSES: durable18:41:40/all four rc0,27checks,
six intended frames directly reviewed, unchanged exact finishing reference,
original HTTP/navigator Mobile UA and actual390px phone margins. Observer
stops cleanly after354frames; public-provider peak696352KiB on8GiB. Actual
bc4afc cleanup18:42:00 confirms owner/guest absence and noQEMU. This is a
runtime-only configuration proof, not a permanent fix or RC-wide pass.

#448 fixes the historical test metadata assumption: failed diagnostic10
required newer handset metadata; fresh12/13 derive exact RC2 SYSTEM absence,
desktop UA and original finishing URI. Prepared11 is superseded/unstarted.
#449 fixes persistent observer boundaries/unique coverage: fullsignin12
reached27checks but failed on TimeoutError; its failing read phase was not
recorded. Nine actual loopback controls pass; full13 keeps every original
assertion/reference and changes only the tested observer. No result transfer
from failed12. Both scoped fixes have retained source/result/cleanup evidence.

**Historical next action (now implemented and qualified above):** #447 remained OPEN. Turn the validated Pixman
workaround into a narrow, explicit GENERIC_X64 software fallback; preserve
accelerated guests and handheld renderers. Prove clean/upgrade selection,
ES/emulator behavior, visual correctness and performance. A product change
requires a fresh candidate freeze/build and affected qualification before P4.
Do not globally override Sway, adopt legacy DRM, relax screenshot criteria,
or claim current --gl none is fixed without the runtime configuration.
Then reconcile remaining #362/#356/#365 criteria/account inputs, P4 approved
primary+Fable5.1/xhigh Facilitator review, H700 arm then aarch64 and named
physical/P5 gates. At that historical checkpoint no job remained active.


Current update: 2026-10-05, #409. Delivery #383; release contract #344;
cloud epic #354. The next RC uses lowercase **pixelelated** and the Tiny5
Duo LCD wordmark (D-WORKFLOW-144/145); the cloud default is `/pixelelated`
(D-CLOUD-174). Version remains 0.0.1. Rasteratops is a character; Blitterbot
is unchanged. The required adoption flow is **ROCKNIX → pixelelated**;
there are no fielded /Rasteratops systems requiring an additional gate.

Replacement09 historical record updated 2026-10-05T17:21:30.901110+00:00.

## Historical replacement09 qualification — superseded by replacement10

At this historical checkpoint M7.P3 was current. The candidate was source `cf511ce79b83cba7fea8b14cfa3d04fb13e4b4fb`, input manifest `817fd9ff49b1ecf6bcc859cfa38985a65fbcfe5514c33a0a5c9dd60af6cc6c6e`, immutable bundle `79d560046ee52e28b72f16588168dd7c8fb2637c1cc585713216a8ec828e9d81`. Build and inventory pass; 14 licence metadata gaps remain for P5.

Default-suite evidence is explicitly composite. QA11/tool64718 returned1 after fourteen passing suites and 16 walks/78 frames: one first-sample PREPARING region was unclaimed. Its original failure is preserved. #439 adds one measured claim; the same frames pass 20 claimed/0 unexpected/0 missing differences. Removed/narrow-claim, unrelated-screen and missing-frame controls reject. QA13/tool42880/all four rc0 verifies all 143 original artifact hashes, repeats the corrected comparison and passes all 26 actual ROCKNIX RC2 upgrade checks. The upgraded ES process survives Back/Back; all five identity frames were reviewed.

Boot04/tool90675/all four rc0 passes four clean/upgraded boots at 640x480 and 1280x960. All four matches are 1.0 at the unchanged .995 threshold; all 12 negative controls reject. Actual frames reviewed. Host verification at06:46:39 found all owner and four guest processes absent. QA13's actual upgraded disk was used. Original QA12 launch refusal and boot03 dependency failure remain intact; 16 fresh successors with 139 sealed source members passed preparation and separate readback before launch (#440, #441).

**Content qualification:** image11/tool1600 confirms identical raw-image/update SYSTEM bytes. Sweep08/tool43694 remains failed on20 previously unclassified contexts. #442 reviews15 compiler paths and5 proxy compatibility identifiers against actual bytes and consumed source. Fresh sweep09/tool81204/all four rc0 passes all20 exact contexts/60 rejecting boundary controls and ten scanner controls. Full scan57293files has zero unknown/FIX contexts and zero unclassified credentials. All851 catalogue/95 XML entries reconcile; installed theme and Tools XML pass. Actual06:52:23 sweep processes absent.

**Settings qualification:** original settings10/tool97000 rejected an inherited stale expected ES hash before race mutation (#443). Fresh settings11/tool91974 derives expected hashes from the verified candidate and records observed values. All20 installed recovery-race and29 permission/refusal checks pass; settings and installed files are restored/unchanged. Original upgraded backing hash is unchanged. Actual06:55:44 all owner and guest processes absent.

**Link-loss qualification:** link10/tool56478/all four rc0 passes all14 WebDAV/S3 interruption cases:151 PASS lines, zero failures/skips. Receiving files remain whole, markers stay correct, and plain retries complete after reconnecting. Actual07:13:44 all owner/four guest processes absent; frozen source and bundle reverified.

**Cloud qualification interrupted:** guest10/tool59031 returned143; its watcher recorded runner death07:37:31. Eight cases/47 assertions passed, K was incomplete, ten cases had not started. Original missing outer/wrapper/build result files remain missing. Actual07:42:37 all seven observed owner/guest/backend PIDs absent. No product failure or signal sender is inferred. #444 preserves the original and requires a fresh complete run.

**Cloud qualification passed:** fresh guest11 completed all19 cases/249 assertions/zero failures. Durable result08:25:35 and all four actual channels are0; submission497141=0 remains explicitly separate. Actual host verification eee27c=0 at08:26:26 found owner/guest processes absent and no QEMU. Source/bundle reverified;32 selected actual frames reviewed across all15 UI cases. Four protocol cases verify bytes/pointers/markers directly. All1708artifact hashes and140selected public files retained.

**Runtime qualification passed:** runtime12 durable result08:32:24/allfourrc0 passes14 actual inherited-archive,4 timing and13 installed-identity checks. Alternating five-sample medians269/245ms give24ms absolute difference against the unchanged30ms threshold; no migration journal activity. Actual08:33:00 owner/guest absent, backing/source/bundle unchanged.

**Proxy qualification passed:** proxy11 durable result08:41:18/allfourrc0 passes all22 unchanged installed assertions: canonical synthetic account discovery, predecessor cache/sign-in/queue reopen, base/subset mapping, original images and offline service behavior. Actual08:41:44 all owner/guest processes absent, no QEMU; source/bundle reverified. This is synthetic preservation proof, not a newly earned ordinary RA award. Original proxy10 missing-directory failure remains preserved. #445's nine fresh owners/96members and private-directory controls were independently verified and M7 read back before launch.

**Provider qualification passed:** optins11 durable result08:47:52/allfourrc0 passes S3 round-trip in120seconds and all42 mixed RC2/fresh migration assertions. Actualc3d137=0 at08:50:30 proves owner processes absent and no QEMU. Source/bundle reverified. Four public artifacts retained; all earlier failures remain preserved.

**Memory qualification passed:** memory11 durable09:04:57/allfourrc0 passes10virgl,10software and50software-with-sync measured launches after five warm-ups each. Virtual growth0KiB in all three; resident growth-208/788/624KiB, below unchanged1024/2048KiB limits. All55 sync stamps are distinct successful completions. Thirty-second sign-in page load passes with peak291924KiB; this is example.org, not provider authentication. Actualafe676=0 at09:05:33 proves all owner/guest processes absent/no QEMU; source/bundle reverified.440artifact hashes retained with raw cycle tables and stamps.

**Bilingual UI qualification passed:** UI13 durable09:17:05/allfourrc0. All70 actual EN/FR640x480/1280x960 menu/Tools frames directly reviewed; all12 ES lifetime records pass, including actual Settings Back/Back save to Updates. Dimensions and intended pages pass. Actual8c4a9d=0 at09:17:24 verifies owner/guest absent/no QEMU. Source/bundle reverified;547artifact hashes/128public files retained. Boot04 supplies the separately accepted exact clean/upgraded boot matcher and negative controls. Earlier failed/interrupted UI owners remain unchanged. #422/#431 scoped closure is verified after publication.

**RC2 recovery passed:** predecessor09 durable09:19:19/allfourrc0 passes65 assertions across five states actually produced by the old RC2 migration script on the upgraded guest COW. All payloads and pointers recover; marker failure retains retry state; repeats preserve bytes. Actual81b7e2=0 at09:20:06 verifies owner/guest absent/noQEMU; original backing/source/bundle unchanged.157artifact hashes/139public files retained.

**Subset HTTP qualification passed:** subset08 durable09:21:41/allfourrc0 passes35 installed assertions. A503 subset refusal keeps the queued award; retry refreshes its own game and uploads only the refused award. No stale deletion or duplicate base upload; empty repeat makes no request. Actualba9ad7=0 at09:22:44 proves owner/guest cleanup/noQEMU; source/bundle unchanged. Six public artifacts retain both flush results and real loopback request history. Synthetic QA data, not a new ordinary account award.

**Supplemental cloud UI passed:** cloud-ui08 durable09:43:59/allfourrc0 passes32 assertions (UI17 nineteen, UI26 thirteen). Actualc230d7=0 at09:44:34 proves owner/guest absent/noQEMU. Nine selected actual failure/completion/recovery/refusal frames reviewed;154artifact hashes/53public files retained. Source/bundle reverified. Original cloud-ui07 durable1/four failures remain intact under cloud-ui-07-failed/. #446 moves volatile fault setup after reboot and adds fail-closed executable/connectivity/failure/fired controls; three fresh owners/35sealed members prepared2c6ff8, verified before launch.

**Sign-in08 visually unaccepted:** durable09:46:40/allfourrc0 and17 commands pass; actual5960e1=0 at09:47:31 proves cleanup. All six frames reviewed; first local302 frame has incomplete repaint blocks, other five intended surfaces pass. #447 preserves command success separately from visual rejection. Public Dropbox peak706132KiB across one window/network/web process; not comparable to simple-page baseline as if equal workloads.

**Sign-in09/10 remain visually unaccepted:** both command0;09 has21 checks and10 has24. Exact finishing document and stable-screen wait do not establish the intended capture. All six original10 frames reviewed; finishing still old.10 durable10:02:16/all four rc0, actual57ee2b cleanup16:02:21 after capacity interruption. Retained signin-ui-09-unaccepted/ and signin-ui-10-unaccepted/.

**Render diagnosis:**01 completed16:12:09/all0, actual41e305 cleanup. Native grim shows Connected at0/5/15seconds while HMP shows old form.02 completed16:16:12/all0, actual3fe75e cleanup: one-frame VNC stale0/5 then correct15, HMP still old. All eight/eleven comparison frames directly reviewed and retained.02's post-resize HMP has mixed geometry; resize is not a remedy. No product cause established. QEMU10.2.1 refresh source plus one-frame client lifetime motivates a persistent read-only receiver control; that remains a hypothesis.

**Preserved diagnostic failures:**03 failed import before sign-in (Pillow absent), durable16:20:00/all1; actual1daf63 cleanup.04 stdlib encoder/import controls pass, but local HTTP-UA assertion fails before finishing. Durable16:22:46/all1, actual0c8bda cleanup. The old helper wrote request evidence only after that assertion; the offending request is unavailable. Original results remain intact under signin-render-diagnostic-03-failed/ and04-failed/. No visual qualification transfers from these runs.

**Canonical sign-in accepted:** render-diagnostic05 completed16:26:31/all four rc0, actual8f03d7 cleanup; its persistent viewer did not eliminate software-host lag. Render06 changed only graphics to actual canonical virgl: all nine native/host frames agree exactly, durable16:29:54/all0, actual321973 cleanup. Fresh full signin-ui11 completed16:35:21/all four rc0/27 checks, actual061ffa cleanup16:35:39. All six intended frames directly reviewed; exact finishing pixels match the reviewed native reference; real old/partial/wrong-size controls reject; four stable receipts pass and an actual zero-exit unsettled result rejects. Public Dropbox peak662412KiB on8GiB. No authenticated trust-page claim. The software scanout discrepancy remains unresolved under #447; no product patch or waiver. Diagnostic04's missing offending UA remains a watch observation; later request evidence is saved before assertions.

**Actual1GiB resource checks accepted:** baseline signin-1g12 and public-provider signin-provider1g04 both complete with four matching rc0 channels. Actual QEMU allocation1024MiB and guest firmware1048576KiB are verified; Linux usable810368/810372KiB is recorded separately. Both30-second workloads load, remain responsive and have no kernel OOM. Peaks: example.org264076KiB, public Dropbox387668KiB. Actual640x480 frames reviewed. Baseline cleanup95f1c2 at16:44:23; provider cleanupa04e75 at16:51:54 proves all owner/guest processes absent and no QEMU. Provider durable result16:46:03; build-log SHA58d5bd3ff31cb3a29c05fc37f3ed44b558e9338efd961ac8a61ddc20b784b678. Original signin-1g11 rejected an invented usable-RAM floor before workload; preserve its all1 failure. Fresh controls reject actual8GiB, mismatched firmware and zero/excess usable RAM. No numerical RSS ceiling is invented; different workloads/allocations are not equal-memory comparisons.

**Published evidence:** feature `1f43880a1139f13fbf503e4990e29522b911ded0` integrated with cherry-pick -x as next `9af943c7ce7966d66bc3a85222013fb2dab16b86`; both remote heads verified16:58:51. #446 closed completed with all four criteria mapped/read back (e522bf). #351 phone-spacing criterion is ticked from actual390px/12px margin measurements; authenticated trust stays open. #362's resource proof and #356/#365's supplemental UI gap are updated; broader criteria still need exact artifact reconciliation. Fresh-context handoff proof independently verified6547product/200QA/180symlinks/14bundle files,682public artifacts and all75 recorded PIDs absent at16:57:26. Its missing-publisher and stale447 closure instructions were corrected and reverified before completion.

**Legacy DRM diagnosis completed:** render-diagnostic07 durable17:04:04/all four rc0, actual037abe cleanup17:08:40. Actual software QEMU, llvmpipe and consumed WLR_DRM_NO_ATOMIC=1/legacy backend are recorded. Nine actual0/5/15second comparison frames reviewed: HMP/VNC still old at0/5, correct15; native correct throughout. This rejects legacy DRM as a remedy. The runtime-only override/debug wrapper exists only on this disposable guest; no product change or qualification claim. Retained122artifact hashes/118public files. Source/bundle reverified. Do not adopt this override as a fix.

**Historical comparison complete:** the maintainer requested isolation against pre-pixelelated builds. Source comparison proves12 actual graphics/browser/VM/capture git objects unchanged between old61b648 and currentcf511ce. Old bundle87b8c01d/imagef1af3533 is verified. Fresh old-image software08 reproduces the same host-old/partial0/5→correct15 sequence while native stays correct; accelerated09 has all nine frames exactly correct. All18new comparison frames directly reviewed; actual accelerated QEMU argv old/current is identical except owner path. Software08 durable17:17:13/all0, actual2f5df8 cleanup17:17:37; accelerated09 durable17:18:48/all0, actualf4b65f cleanup17:19:03. Frozen source and both bundles unchanged. This rules out pixelelated changes as necessary to reproduce on today's host; it does not establish historical-host or physical-device behavior. Exact component cause remains open. Read historical-render-comparison/README.md before proposing another fix.

**Earlier investigation priority:** superseded by the latest-result section above; permanent software fallback and broader regression proof remain under447.

**Monitoring limit:** diagnostic07's durable watcher recorded17:04:04 completion; the first actual host check was17:08:12. This does not meet the intended active60second observation bound. #395 retains the unconfigured disconnected destination and this actual gap. Do not present the recorder as proactive off-session delivery or say this run met active supervision.

**Remaining order:** remaining P3 software/account proofs → P4 primary OpenAI + Fable5.1/xhigh through the verified Facilitator → H700 DDR4/RG35XX SP arm, then aarch64 → separately authorized device actions/publication. Ordinary Tobu100359 is already earned; the earlier request for a reset or alternate dedicated QA account is unanswered. Authenticated Dropbox trust needs dedicated QA access; public pages/done-file stand-ins cannot replace it. Public-docs access,14P5 licence metadata gaps and #395 disconnected notification destination remain recorded. P4 has not started; no RC/device-ready claim. Can this be done on the VM? **Yes**, including all remaining software/account proofs.

Published UI13/predecessor09/subset08 evidence: featuredf13f273a0745628780ef1abfaae8f8f22c55f0b → next908bc62f94d059864a0c466eedb31ac2955fa4ec; both remote heads verified09:25:37.

Scoped #422/#431/#426 are now CLOSED completed: actual000718=0 readback verifies all criteria from published evidence. #391/#310 were already closed on earlier artifacts; their replacement09 checks are renewed evidence. Tools/status issue #416 also CLOSED completed, actual23e12e=0. No candidate-wide acceptance follows.

## Historical replacement06 qualification

The following evidence applies only to frozen57cbc replacement06 and records
the status at that time; its instructions do not override the current order.

The [M7 milestone body](https://github.com/pixelelated/distribution/milestone/7)
is the binding running order. **Historical engineering image: replacement06**,
frozen57cbc9b981205328444d41f6c4237dc9f5736d7f, built642/642 at22:49:13UTC
October4. Actual28970/allrc0 and actual runner/watcher/container cleanup pass.
The immutable bundled4007387… holds image1e16122c… and update1786a568…;
store/independent verification actual98974=0. Full inputs82764873… bind6547
product files,180links and200QA files. Previous05cache was independently
copied and checksum/inode verified2525217files before use. Guarded preflight
reclaimed swap; no helper reinstall is needed.

**Verdict: completed runtime/memory/menu checks; 640x480 boot splash match blocks qualification (#433).**
qa07 actual44253/allrc0 completed23:31UTC: all15defaults,16walks/78frames,
baseline21claimed/0unclaimed/0missing, actualRC2 preservation and exact clean/
upgraded bytes/modes. Actual ES process identity and five1280x800frames in
each phase confirm pixelelated0.0.1 and correct manual-update instructions.
All owned processes exited, independently observed23:31:18.
Image07 actual86758=0 proves flash/updateSYSTEM SHAacc5ebc280fb… equal.
Sweep04 actual4437=0:8589reviewedbrandcontexts,0FIX/UNKNOWN,70reviewedpublic
credential-patternmatches,0unclassified,10controls,95XMLentries/0orphans.
Settings06 actual60081=0:20realESrace/29installedmode checks on actual-upgrade
COW, original settings/product/backing preserved, actualcleanup23:33:43.
Link06 actual26472/allrc0 completed23:50:48UTC October4: seven WebDAV
cases PASS477s and seven S3 cases PASS459s; actual process/backend cleanup
verified23:59:43–58. Guest06 actual67203/allrc0 completed19 cases/249PASS/0FAIL;
33 selected frames inspected, all1467frames hashed; actual cleanup00:41:59.
Originalruntime06 actual38117/allrc1 failed36ms timing and remains retained.
#430 fixture repair verifies actual guest/host timestamp boundaries; all three
predeclared diagnostic batches23/29/26ms pass with real transferred bytes.
Optional trace parser failure and corrected trace-only run are retained.
Fresh runtime07 actual29491/allrc0 passes archives14/timing4/identity13 with
272/244ms medians,28ms against unchanged30ms. All source/backing/cleanup pass.
No product bytes changed; no single cause claimed for original36ms result.
Proxy05 actual57392/allrc0 passes20 installed cache/sign-in/queue/offline HTTP
preservation checks. It uses synthetic QA data, not a real new RA award.
Actual01:05:09 all owner processes absent. No RC/device claim.

qa06's original30948/allrc1 is preserved: a newly added harness expected0644
for the export profile, but Git/package/guest correctlyuse0755 (#428). Fresh
qa07 fixes only the expectation; mode controls reject644/777/600. Prior seals
are retained for the six unstarted dependents rebound toqa07. No new rebuild.

Current proxy865e21 source review:105consumed Python/native files and268
Linux/native/test files excluding two unshipped bundle builders matchaec99c;
15zero-fuzz patches, schema/coupled pins/freshness pass (#426). Installedproxy05 now passes20 preservation checks; subset02 HTTP retry
proof still remains. Inventory04 actual53198/allrc0 proves568roots,
547cache inputs,583components/525stamps and0errors, with currentproxy and
recoveredrclone archive verified. Fourteen licence-metadata gaps remain P5.
Build/source receipts: `docs/qa-logs/2026-10-04-pixelelated-replacement-06/`.
Runtime/failure receipts: `docs/qa-logs/2026-10-04-pixelelated-57cbc-qualification/`.

Optins05 actual62343/allrc0 passes S3 round-trip108s and mixed RC2/fresh
pair42 checks; source/bundle and actual01:12:58 cleanup verified. Current
memory05 actual34776/allrc0 passes VmSizegrowth0/0/0 and RSSgrowth-72/492/472KiB
for virgl10/software10/software50,55 completed sync stamps. Example.org loads
at291120KiB peak combined RSS (~284MiB). Actual01:27:37 cleanup verified.
UI06/tool35647 was interrupted: actual143, inner/outer1, no wrapper/build
exit record; watcher DIED at01:35:08. Partial captures and cleanup receipts
remain retained under ui-06, with no inferred signal sender (#431).
UI07/tool90920 completed all four panel/language walks and all result channels0;
42 actual menu/Tools frames reviewed, source/bundle pass. Actual01:52:41 all
owned processes/backends absent. Separate boot matcher fails640x480 at96.1021%
versus unchanged99.5%;1280x960 passes99.6047%, all negative controls reject.
All924 differing pixels are black instead of expected palette colors. #433
owns diagnosis; console redraw/tracing effects are unproved hypotheses. No
blind rerun, threshold waiver or RC acceptance. After accepted boot proof,
rebind only unstarted predecessor03's oldui06 gate, then predecessor03→subset02.
#429/#430 and #363 closed completed from published exact-candidate proof. Only unstarted
proxy05 was rebound to runtime07; prior seal/launcher retained.
Follow with the prepared
cloud-ui-01 proof for #365 wizard failure/recovery and #356 unsupported-marker
frames; then prepared signin-ui-01 for #351/#362 sign-in/window/phone proof. The
memory owner measures example.org loading and has no numerical memory ceiling
assertion; it does not prove provider login or redirect behavior. Authenticated
Dropbox trust-page QA access is pending. Both proof plans are in the current
qualification directory. A prepared signin-1g-01 owner follows signin-ui-01
to verify D-WORKFLOW-048's1GiB page-load budget without inventing a numerical
RSS ceiling. #362 wording is reconciled; actual proof remains pending. Then
reconcile remaining criteria, ordinary RA proof, approved P4 primary+Fable5.1/xhigh review and first
H700 DDR4/RG35XX SP build. Daybreak is not required or claimed. Ordinary RA
fixture, public-site delivery, disconnected alert destination, publication and
physical actions retain their named gates.

## Historical frozen05 qualification — superseded by replacement06

Frozen1e6a/bundlea179bd73 built successfully and passed15defaults,actualRC2
upgrade,16walks/78frames, image equality/content classification, installed
settings race20/modes29, WebDAV7/S3seven interrupted cases,19cloud-state cases/
249checks, archive14/timing4/Tools-consumer13, proxyoffline20, S3roundtrip110s/
mixedpair42, memoryvirgl10/software10/software50+exit-sync and30sHTTPS load.
VmSizegrowth0KiB/RSS608,280,620KiB. Final predecessor02 passed65 checks and
subset01 passed33 including syntheticHTTP refusal/retry/no duplicate base.

ui05 capture success produced70frames,20selected640 reviewed, with boot
match64099.586585%/1280100% against99.5% threshold and rejecting controls.
Actual ES lackedOS_NAME, so menu/update semantics failed424. That blocks05
regardless of its other passes. Corrected06 clean runtime proof above does
not retroactively change05. Oldui04 count-wrap/missing-Wi-Fi hypothesis and
predecessor01 parser failures remain recorded with later corrections.

Historical inventory03 binds05 only. Receipts in
`docs/qa-logs/2026-10-04-pixelelated-1e6a-qualification/` and
`docs/qa-logs/2026-10-04-pixelelated-replacement-05/`. The earlier02163 image
exposed600→644 shell-writer widening421 after passing defaults; corrected
source1719checks and installed05 mode/race proofs close that defect.
#320/#384/#391/#392/#366/#417/#419/#420/#421/#425 are closed with their own
proved scopes. #424/#428 are now also closed from published replacement06
proof. #422/#426 retain bilingual UI and installed proxy criteria. #427 was a
disproved fallback-glob hypothesis, closednotplanned with no source change.

The sections below retain the October2–3 review baseline and historical pins.
The final phase overview applies with the current candidate/order above.

## Historical execution update — 2026-10-03

P1 source coverage is complete:208 actor/state assignments, inherited-state
recovery and missing-remote controls,1,367 host+322 focused checks PASS.
T17/T19/T23/T26 guest cases are promoted for candidate P3 execution. Their
ES migration/settings-lock changes remain included in the current qualified
pin e6e1e4d0f91e177e182cc05b1cea74991e1cc45b.

P2 proxy preservation and current coupled dependencies pass their source
checks. #310 now passes all unchanged diagnostic memory limits: software10,
software50 with exit sync and virgl10 have zero address-space growth and
RSS growth532/364/60KiB. All exit syncs complete. #332 actual LED script tests
and guest menu reselection pass. Process/hook controls and the six armature
retests pass. Receipts are under `docs/qa-logs/2026-10-03-{proxy-refresh,
dependencies,launch-memory,led,process,push-hook}/`.

**Original503e evidence:** the cold engineering build completed642/642 tasks and image
assembly from frozen distribution503e24e10d. The corrected watcher recorded
rc0. Image/update checksums and immutable candidate-store custody pass.
**Original503e qualification:** all15 default suites have passing evidence
on the unchanged candidate:14 passed in the first run; #396 corrected the
host archive-name assertion and the complete round-trip rerun passed81s.
All16 visual walks and frame comparison pass. Source/candidate custody was
verified before and after the default run. RC2 upgrade passed18:57UTC, S3 round-trip passed107s, and mixed-install
pair migration passed42/42 at19:04UTC. All7 WebDAV link cases have passing evidence after host fixes #398/#399 and
strict LINK5 fixture correction #400; the corrected archive interruption/retry
also passes S3 without skips. Full S3 link proof exposed #401: content backup
and restore outwait an outage because they lack the saves/settings progress
stall guard. #402 owns a scan that completed before its cut could land.
The independently reset19-case640x480 guest matrix passed249/0 at20:31UTC.
#402's corrected S3 pagination now proves interruption and retry; its newly
reached failure sentence is included in #401. Focused guard controls pass18/18
on host and candidate BusyBox, and six complete-script checks pass. The full
candidate-binary host rerun passes1373 broad+322 layout checks under #403,
0FAIL/0SKIP; its predecessor's stale assertion failure is retained. #404 corrects recorded frame counts;
#405 corrects sign-in-tool help. Production virgl10 passes (VmSize0KiB,
RSS+620KiB); software10 also passes (0/52KiB). Software50 with exit sync
passes0/1228KiB with55 unique success stamps; sign-in page loading/memory
passes30s, peak total RSS292788KiB (not provider authentication). RA award100359
is already earned; the owner reset/alternate-QA-account question is pending.
Evidence: `docs/qa-logs/2026-10-03-m7-qa-01/` and
`docs/qa-logs/2026-10-03-archive-harness/rerun/`.
**Image gate #397:** original503e SYSTEM lacks the approved branding licence
and trademark policy. The correction passes byte/mode/failure staging controls
and exact assembled134e89 payload checks. The immutable replacement exists;
clean and actual RC2-upgraded guest readbacks now pass exact bytes/modes.
Receipts: `docs/qa-logs/2026-10-03-m7-replacement-qa/`.
**Replacement01 (134e89) completed:** clean/default plus separate78-frame
comparison, actual RC2 upgrade/readbacks, seven WebDAV and seven S3 link cases,
archive24+56 assertions, strict root22, local recovery23 and S3 refusal10.
All24 EN/FR640/1280 frames visually reviewed. #397/#401/#406 closed from their
published proof. Public-site screenshot4f6df54 remains local because GitHub
refused Blitterbot403; #327 remains open for delivery.

**Replacement02 at that checkpoint (61b64817bf):** build completed642tasks23:16:46UTC,
immutable bundle87b8c01d65dc22b4f29049bd0d69307a59c14c16f5223534e95058b2234ca5cd.
Includes directory-probe timing #364, root wording #407 and canonical proxy
account discovery #408. Full source regression1373+322PASS. Installed proxy
proof20, S3 refusal10, root transitions/sentence22 and archive writer/selected
journal8 now PASS. Full default15/15, actual RC2 upgrade and exact clean/upgraded readbacks now
PASS. A COW of the actual upgraded disk passes14 archive,4 timing and11
identity assertions. Installed legacy/current exit-sync medians264/241ms
are23ms apart within30ms, with exact transferred bytes. All guest/backend jobs
stopped. Receipts:2026-10-03-m7-replacement02-qualification and
2026-10-03-m7-final-runtime; previous-artifact evidence retains its scope.

Shared recorder and active session report failures, stalls and completion;
no disconnected delivery destination is configured (#395). RA ordinary award
needs the outstanding QA-account fixture answer. P4's approved primary plus
Fable5.1/xhigh Facilitator fixes review follows completed qualification. Audit
cadence remains due and unwaived; no RC claim. P5 source/licence/publication
and named device-action gates remain distinct.

**Historical review below:** all tables, numbered gaps and diagnostics below
record the2026-10-02 baseline. Their then-open source tasks are superseded by
the current execution update above and live milestone; retain them to explain
why earlier VM rounds were insufficient, not as another current work queue.

## Inputs and evidence checked at the review baseline

| Input | Observed state |
| --- | --- |
| Distribution | Feature `fcd0f20c9a`; content integrated on `next` as `df23faff6c`. Frozen ROCKNIX ancestry remains `9fd38fa87094d4f0e956d03ac6c660fe4fd5e9d6` (D-WORKFLOW-111). |
| EmulationStation | `97523542963dcc72e9ea51cfbcd26b735ff28c1f`; cloud ordering and displayed identity changes implemented and pushed. |
| Splash | `7450aa8180ae66684814dd460f31eb502b2abf61`; wordmark source and native render checks exist. |
| Build container | Selected `ghcr.io/rasteratops/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39`; consumption by the cold build is unproven. |
| Host regression suite | Pre-refresh receipt: 1,367 harness PASS, 0 FAIL, 0 SKIPPED, plus 72 focused cloud-case PASS lines and the 23-test subset-award result. Predates the libsoup/proxy refresh; not image evidence. |
| Independent initial audit | #375/#382 completed. Verified Fable 5.1/xhigh blind and refutation passes found five product issues. Closing the audit did not close those issues. |
| Latest VM artifact | Run 101 is the older unbranded input set. No cold RASTERATOPS build or 0.0.1 candidate exists. No build/VM job intentionally running at review. |
| Source preflight | Exit 2: package freshness cannot answer; bug gate fails. Used `--no-fetch --allow-unchecked device-facts`: cached refs and unchecked physical facts are explicit limitations. |
| Corrected bug gate | After removing RC2 waivers and exposing #320: 15 open issues, exit 1. This includes implemented fixes awaiting evidence, not 15 untouched defects. |

Receipts: [preflight](../qa-logs/2026-10-02-readiness/rc-preflight.log),
[freshness](../qa-logs/2026-10-02-readiness/freshness.log),
[corrected bug gate](../qa-logs/2026-10-02-readiness/bug-gate-after.log),
[host suite](../qa-logs/2026-10-02-candidate-preflight/full-host-suite.log),
[audit](../audits/2026_10_02-milestone-375-rasteratops-0-0-1/04-analysis.md),
[VM retro](../retros/2026-10-02-cloud-runs-95-101.md).

## Goals, implementation and remaining proof at the review baseline

| First-release goal | Implementation and evidence | Required closure |
| --- | --- | --- |
| Identity with safe RC2 adoption (#337, #344, #359) | OS name/version, ES wordmark, splash/theme, manual updater, reporting disablement, licences and adoption suffix implemented. Persisted/partition contracts retained. | Cold image; identity/update/network/licence readback; clean install and RC2 upgrade; image brand/secret/localisation sweeps with failing controls. |
| Preserve settings backup/restore (#349, #376, #379, #381) | Shared archive discovery reads both suffixes and actual per-device writer folders; writer retains persisted suffix. Independent populated backup tiers survive transitions. Host regressions pass. | Candidate writer→scan→restore, foreign-device disclosure, local archives and upgrade on both providers; resolve inherited recovery race #320. |
| Content restore and sign-in (#350, #351, #352, #380, #362) | Interstitial/chooser/sign-in changes and explicit cloud-root content preservation implemented; libsoup 3.8.0/WebKitGTK 2.54.1 recipes prepared. | Guest UI walks with pointer/byte assertions, English/French frames, HTTP/TLS/redirect and sign-in memory proof on rebuilt stack. |
| Safe, repeatable cloud migration (#353, #354, #356, #365, #377) | Current defaults, join/follow/settle/move, failed-listing distinction and seeding failure propagation implemented. T01–T25 table and host cases exist. | Numbered retryable transitions; strict marker versions; interrupted tier/marker publication recovery; future/malformed markers; second guest follows; actors agree on pointers/bytes. |
| Bounded startup; no surprise old folders (#363, #364, #366) | Preparation precedes startup transfer; dialog waits for actual card lifetime; backup guard uses one listing; fixtures derive defaults. | Whole-boot T08/T11/T12 and fault recovery, card frames, no old-root writes under SKIPPED, five-sample overhead <=30 ms, time-to-play. |
| Offline achievements without lost capability (#361, #384, #168) | Subset backport: 23 parity tests pass on old pin. Current pristine upstream: 104 tests pass. Isolated image-publication contribution: 105 tests pass. | Reconcile every local patch; whole-library preparation; queued never means ready; cached sign-in/games/images and pending base/subset awards survive upgrade/reconnect; host and guest proofs. |
| Stable launch and retained device behaviour (#310, #327, #332) | Memory growth unresolved. Explanation page has RC2 frames/source. Nova LED script has later brightness/default-colour work; original issue text stale. | Current mapping/10/50-cycle proof; approved wrapped paragraphs and docs frame; LED argument/reselection fixture and guest UI proof. Physical illumination is a separate device fact. |
| Reproducible, recoverable release (#344, #265) | Frozen ancestry/container pin and candidate-store helper exist; synthetic store controls pass. | Source inventory, cold log, actual manifest/digests and retained bundle; manifest-bound draft/source publication; mandatory migration and qualified device assets. Old publisher still selects date-named ROCKNIX artifacts: do not invoke it for this release. |
| Release custody (#344) | Blitterbot identity complete (#374); inherited untrusted-event workflows use hosted runners; old CI image publication disabled. | Record actual container consumption/source custody and trigger/isolation or disabled-runner fallback evidence. Bot runner inventory returned 403; absence of a local runner is not remote-host proof. Deferred infrastructure topology is separate. |

## Structural gaps behind the repeated VM rounds — review baseline

1. **Marker presence is not a version contract (#356).** Production
   `cloud_migrate_layout` calls `fleet_made()`, accepting any first line
   beginning `layout=`. It does not reject malformed/future versions.
   `write_marker()` reports failure but returns success, and completed tiers
   publish pointers before a later tier can fail. T23 proves one safe
   collision refusal, not successful interrupted retry or fleet recovery.
   `cloud_setup` also writes the marker. All writers/readers need the same
   supported-version/retry contract. The numbered dispatcher and durable
   step journal are not implemented.
2. **Saves, backups and content are independent (#365).** The 72 host
   checks include classification checks, not end-to-end execution of every
   actor for every table row. Add an actor × state coverage map; close each
   relevant cell with assertions or an explicit reason it is inapplicable.
   Retain settings-only archives, explicit empty content roots, failures
   before seeding, restricted-prefix access and retry/fleet cases.
3. **The inherited recovery race is still in pinned ES (#320).**
   `SystemConf::loadFromDisk` records last-good state after `loadUnderLock`
   returns, including a lock-busy path. A newer script write can have its
   recovery record replaced by the earlier read. The earlier audit deferred
   this for RC1/RC2; the `audit` label hid it from the bug-only preflight.
   Prove the interleaving with a failing control, fix it, compare guest bytes.
4. **Proxy success no longer always means offline-ready (#361).** The
   upstream unindexed API can return `success` with `queued=True`; the fork
   counts success as cached. The indexed path uses a different API. Reconcile
   the queue/budget boundary with a >100-game fixture before changing the
   pin. Preserve whole-library capability under D-WORKFLOW-138.
5. **Old exceptions leaked into the new gate (#385).** Preflight accepted
   #310/#327/#332/#352/#353 using RC2-era rows. These exceptions are removed
   for the first release; decisions stay in the historical ledger. Bugs
   close from evidence. Preflight's bug count is not a release-scope inventory.

Run 98 passed 15/15 while missing fresh join. Run 100 passed 15/15 while
missing the backup that recreated `/GAMES` under SKIPPED. Run 101 exposed
stale fixtures; correcting pair expectations produced 42/0 on that same
older image. Timing was 59 ms against a 30 ms criterion. These results are
useful diagnostics; they cannot qualify unbuilt bytes or untested transitions.

## Issue inventory and boundaries at the review baseline

Includes all open milestone-7 issues at review and relevant omitted issues.
An unchecked issue is not automatically missing code.

| Issues | Disposition at review |
| --- | --- |
| #337, #344 | Identity source substantially implemented; build/custody/adoption/publication criteria open. P0 remains historical evidence. |
| #349, #350, #351, #352 | Interface work exists; candidate restore/chooser/sign-in/interstitial evidence and docs reconciliation owed. |
| #353, #354, #356 | Cloud goals open, including versioned migration. Do not require all three pointers to change when populated/custom tiers are independent. |
| #357 | Disable upstream reporting in this image. Explicitly later own-telemetry design now has separate #387 outside 0.0.1. |
| #359 | Terms decided, source files exist; image licence and release-note agreement remains. |
| #361, #362, #384 | Refresh and runtime preservation remain; dependency issues belong in milestone 7. Old “frozen proxy” wording no longer describes approved direction. |
| #386 | Reconcile the additional freshness findings below, with source/consumer evidence and a final passing diagnostic. |
| #363, #364, #365, #366 | Source/harness fixes exist; actor coverage, promoted guest run, negative controls, card/timing and fixture proofs remain. |
| #367 | Six process criteria delivered; commit→issue guard and watch-job help remain. Host workflow work, not a device feature. |
| #368 | Stash/fresh-agent exercise exist; retain briefing and corrections, reconcile issue criteria and actual next work. |
| #371 | Existing-branch hook re-judges published merge history. Cherry-picking locally avoids it but is not the fix. |
| #376, #377, #379, #380, #381 | Five audit findings have fixes/host evidence; owning candidate criteria remain open. |
| #378 | Routing implemented; initial Fable calls completed. Only automatic version→depth policy remains, so the issue is outside milestone 7. This release already has a selected, authorized other-lab review under #383. |
| #383, #385 | Four-step delivery remains active; this reconciliation updates its source-freeze prerequisites, tracker, gate and handoff. |
| #310, #320, #327, #332 | Carry-forward software/evidence requires current disposition, not RC2 waivers. Expose #320 to bug gate. Do not infer #332's reselect behaviour from callback names. |
| #265 | Resolve actual versioned artifact selection/publication, not only the display number. Keep working 0.0.1. |
| #168 | Contribute general-purpose proxy fixes with receipts; upstream acceptance need not hold a locally qualified fix. |
| #309, #324 | Inspect applicable migration/archive/achievement-proof freshness items during owning work. Do not reopen every deferred audit lead as first-release scope. |

Freshness diagnostic: `glslang` 15.1.0 vs 16.6.0, `spirv-headers` 126
commits behind, `cbindgen` 0.29.2 vs 0.29.4; `tllist` 1.1.0 UNKNOWN
(Codeberg resolver did not answer). Reconcile current sources and consumers;
do not blindly bump incompatible components. RAOfflineProxy's displayed
PINNED reason is stale under D-WORKFLOW-138. Parent-coupled gamescope,
MangoHud and proxy submodules have recorded reasons and move with parents.
Frozen distribution ancestry is separate from package freshness.

Explicitly later: replacement runner and progressive inherited-code review
planning (#336/#339/#346, D-WORKFLOW-102), infrastructure topology/off-host
restore drill (#347/#348/#355, D-WORKFLOW-113), own telemetry, full site beyond
the approved placeholder and trademark registration. No broad rewrite or new
five-seat council is required to resolve these first-release defects.

## Ordered route to an RC

1. **M7.P1 — State contract and negative controls:** #356 versions, numbered steps,
   interruption/retry/fleet; #320 recovery lock; #365 actor coverage. A new
   build cannot retroactively teach RC2 to understand future markers. State
   the supported older-build boundary and prove compatible behaviour; do not
   invent a fleet-wide-upgrade prerequisite from D-CLOUD-169.
2. **M7.P2 — Qualified source inputs:** #361 proxy preservation, freshness gaps,
   changed-package checks and relevant host suites; #310/#327/#332 software
   evidence and #371/#367 host gates. Diagnostic VM images here are
   engineering builds, not RCs.
3. **M7.P3 — Freeze and build:** record distro/ES/splash commits, container
   digest, source inventory and concurrency; build pixelelated from a fresh root
   or an independently checksum/inode-verified cache. Store
   actual artifacts with manifest/digests, verify before/after QA. Never
   rename a warm root or select a newest-date glob.
4. **M7.P3 — Qualify that image:** clean install, RC2 upgrade, 15 default vm-qa
   suites plus required link/RA opt-ins, local WebDAV/SFTP/MinIO-S3, guest pair, independently
   reset promoted cases and failing controls, future-marker/retry cases,
   writer-shaped archives, pending subset flush, memory/launch/timing,
   boot/card/update/identity frames at 640×480 and Nova's 1280×960 in English
   and French, image sweeps and licence/source evidence. Close software bugs
   with traces and `Already written:` treatment of existing state.
5. **M7.P4 — Independent fixes audit:** approved primary plus Fable 5.1/xhigh through
   verified Facilitator. Do not restart #375 or count blind/refutation as
   additional seats. Resolve findings; changed product inputs require rebuild
   and renewed affected evidence before an RC claim.
6. **M7.P5 — Release staging:** exact manifest-bound draft/source bundle, release/
   adoption/recovery notes and docs. RG35XX SP migration and other supported
   devices' smoke facts remain named per-action device work; attach only
   qualified assets. Publication remains separately authorized.

Can this be done on the VM? **Yes** for software acceptance, with synthetic
providers and hardware-path fixtures. Actual board boot, boot-medium/migration
and physical LED/panel facts belong in `docs/releases/device-facts.md`.
No personal cloud is needed to prove the state machine or recovery paths.

Image-only criteria remain open until an engineering build produces their
evidence; they block RC designation, not that build. #344's old P0–P6 labels
are contract sections, explicitly mapped in the milestone body, not M7 phase
numbers. Milestone-wide delivery/release/cloud umbrellas omit P in their titles.
