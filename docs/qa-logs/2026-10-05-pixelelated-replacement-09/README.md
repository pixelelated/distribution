# M7.P3 replacement09 build and qualification (#409, #383)

Status updated 2026-10-05T17:21:30.901110+00:00.

## Current gate — remaining P3 proofs after sign-in qualification

M7.P3 is current. The frozen candidate is source `cf511ce79b83cba7fea8b14cfa3d04fb13e4b4fb`, input manifest `817fd9ff49b1ecf6bcc859cfa38985a65fbcfe5514c33a0a5c9dd60af6cc6c6e`, immutable bundle `79d560046ee52e28b72f16588168dd7c8fb2637c1cc585713216a8ec828e9d81`. Build and inventory pass; 14 licence metadata gaps remain for P5.

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

**Current priority:** #447 is a software virtual-display investigation, reproduced on both sides of the rename. Do not spend another cut assuming a branding regression. Use the matched comparison and retained Sway debug evidence to isolate the host/compositor/virtio path; unchanged source alone is not proof of identical binaries. Reconcile #362/#356/#365's broader criteria against existing artifacts. Ordinary RetroAchievements/authenticatedDropbox inputs remain pending; then P4 and H700. No job, guest or watcher is active at actual17:19:03; executed owners are immutable.

**Monitoring limit:** diagnostic07's durable watcher recorded17:04:04 completion; the first actual host check was17:08:12. This does not meet the intended active60second observation bound. #395 retains the unconfigured disconnected destination and this actual gap. Do not present the recorder as proactive off-session delivery or say this run met active supervision.

**Remaining order:** remaining P3 software/account proofs → P4 primary OpenAI + Fable5.1/xhigh through the verified Facilitator → H700 DDR4/RG35XX SP arm, then aarch64 → separately authorized device actions/publication. Ordinary Tobu100359 is already earned; the earlier request for a reset or alternate dedicated QA account is unanswered. Authenticated Dropbox trust needs dedicated QA access; public pages/done-file stand-ins cannot replace it. Public-docs access,14P5 licence metadata gaps and #395 disconnected notification destination remain recorded. P4 has not started; no RC/device-ready claim. Can this be done on the VM? **Yes**, including all remaining software/account proofs.

Published UI13/predecessor09/subset08 evidence: featuredf13f273a0745628780ef1abfaae8f8f22c55f0b → next908bc62f94d059864a0c466eedb31ac2955fa4ec; both remote heads verified09:25:37.

Scoped #422/#431/#426 are now CLOSED completed: actual000718=0 readback verifies all criteria from published evidence. #391/#310 were already closed on earlier artifacts; their replacement09 checks are renewed evidence. Tools/status issue #416 also CLOSED completed, actual23e12e=0. No candidate-wide acceptance follows.

## Preparation snapshot (historical)

Snapshot 2026-10-05T05:35:11.400623+00:00. Frozen distribution cf511ce79b83cba7fea8b14cfa3d04fb13e4b4fb,
ES f6f0c134212bc696f2f6a747c8d390a588f2f0ce, manifest 817fd9ff49b1ecf6bcc859cfa38985a65fbcfe5514c33a0a5c9dd60af6cc6c6e.
There are 6547 product files,180 symlinks and200 unchanged QA tools. The only
product change from replacement08 is the patch018 filename and removal of the
unshipped OS alias. ROCKNIX and pixelelated behavior is preserved. Proxy7252fc,
ES and splash pins stay unchanged. Source publication52870=0 verified both
remote heads; freeze90645=0 verified the exact source delta and container.

Independent build-cache copy91647 is active with the standard5s watcher and
5min inactivity warning. Actual05:34:26 runner3183093/watcher3183094/command3183123
are live in run20261005T053303Z-aecc0df2. Checksums and distinct-inode verification
must pass before the guarded idle preflight and proxy/image build. No image
build or candidate acceptance is claimed. Prepared sources were retained here
while the copy was running; no executed owner or frozen product was edited.

All18 new QA owners are sealed and unstarted. Their existing assertions,
actual Settings-save lifecycle guards and boot threshold/controls are retained.
QA11 additionally verifies the installed proxy module recognizes actual
pixelelated and exercises temporary ROCKNIX/pixelelated/unsupported-name
fixtures, including account-settings discovery. Embedded fixture newlines were
checked as actual codepoint10; no literal backslash-n fixture is used.

Order: copy/checksums/inodes → guarded idle preflight → proxy/image build →
immutable bundle → QA11/defaults/actualRC2 upgrade → boot03 → image10/sweep07/
settings09/link09/guest09/runtime10/proxy08/optins08/memory08/UI10 → predecessor06/
subset05/cloud-ui04/signin-ui04/signin-1g04 → ordinaryRA → P4 → H700 arm/aarch64.
Inventory07 may run read-only alongside QA. Prior08 passes remain scoped to08.
No RC/device-ready claim. Scoped #436/#433 repairs are closed with published08
installed evidence; remaining M7 candidate qualification is not complete.

Preparation publication first stopped before commit because two copied, sealed
harness files retain historical trailing spaces (proxy08/run.sh:51 and
settings09/host-proof.py:23). Their exact source bytes and seals are preserved.
The second manual whitespace check excludes only those two archived copies;
normal commit/push hooks and authored-file checks remain intact.

The second preparation publication was refused by the normal credential guard
before commit: two existing kernel filenames in the complete input manifest
matched its pattern. The original manifest remains unchanged in the owner;
Git retains inputs-reference.json with its digest and counts. No scanner
exemption or altered manifest is used. The candidate bundle will bind the full
original manifest, as in prior candidates.
