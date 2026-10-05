# M7.P3 replacement09 build and qualification (#409, #383)

Status updated 2026-10-05T09:07:31.077678+00:00.

## Current gate — replacement09 memory qualification passed

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

**Current priority:** UI13 ACTIVE, submissionff7a02. Actual09:06:33 launcher413999/runner414000/watcher414005/command414039 and640panel guest414781 live. Watched run20261005T090612Z-35985aae. Standard watcher5second heartbeats/5minute inactivity; active supervision within60seconds. English/French640x480/1280x960 menu captures require direct visual review and ES lifetime proof before predecessor09. No RC/device-ready claim; disconnected alerts remain #395.

**Remaining order:** UI13 → predecessor09 → subset08 → cloud-ui07 → signin-ui07 → signin-1g07 → ordinary RetroAchievements proof → P4 primary OpenAI plus Fable5.1/xhigh through the verified Facilitator → H700 DDR4/RG35XX SP arm, then aarch64. Predecessor09 requires the completed boot04 proof and an actual UI13 visual review. External inputs and P5 publication gates remain recorded. Can this be done on the VM? **Yes.**

#433/#436 remain closed from their artifact-scoped replacement08 repair proofs. #437/#438 and #439/#440/#441 are closed with published scoped evidence; actual52959=0 verifies the latter three bodies/states. Content/settings publication49305=0 put featureb7f9cac3 on nexte1f2baaf, with both remote hashes verified. #442/#443 are closed completed; actual19135=0 verifies their acceptance bodies and states. These closures do not qualify the whole candidate.


Latest normal publicationa981e3=0: featurefbc4cf75946d8d119a4066527ba51557edba90cf → next49012c27027593204c7db30d0e8bfffd8ad1c1ea, both remote hashes verified. #444 and #445 are closed completed; #445 closure/readback414e77=0 verifies allfour criteria from published evidence. Memory11 is now complete; UI13 is active.
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
