# M7.P3 replacement09 build and qualification (#409, #383)

Status updated 2026-10-05T06:47:40.836058+00:00.

## Current gate — replacement09 boot qualification passed

M7.P3 is current. The frozen candidate is source `cf511ce79b83cba7fea8b14cfa3d04fb13e4b4fb`, input manifest `817fd9ff49b1ecf6bcc859cfa38985a65fbcfe5514c33a0a5c9dd60af6cc6c6e`, immutable bundle `79d560046ee52e28b72f16588168dd7c8fb2637c1cc585713216a8ec828e9d81`. Build and inventory pass; 14 licence metadata gaps remain for P5.

Default-suite evidence is explicitly composite. QA11/tool64718 returned1 after fourteen passing suites and 16 walks/78 frames: one first-sample PREPARING region was unclaimed. Its original failure is preserved. #439 adds one measured claim; the same frames pass 20 claimed/0 unexpected/0 missing differences. Removed/narrow-claim, unrelated-screen and missing-frame controls reject. QA13/tool42880/all four rc0 verifies all 143 original artifact hashes, repeats the corrected comparison and passes all 26 actual ROCKNIX RC2 upgrade checks. The upgraded ES process survives Back/Back; all five identity frames were reviewed.

Boot04/tool90675/all four rc0 passes four clean/upgraded boots at 640x480 and 1280x960. All four matches are 1.0 at the unchanged .995 threshold; all 12 negative controls reject. Actual frames reviewed. Host verification at06:46:39 found all owner and four guest processes absent. QA13's actual upgraded disk was used. Original QA12 launch refusal and boot03 dependency failure remain intact; 16 fresh successors with 139 sealed source members passed preparation and separate readback before launch (#440, #441).

**Current action:** image11/tool1600/all four rc0 completed; raw-image and update-tar SYSTEM payloads match SHA256 `4c7c1fcce5f9e0032d1d57f9099d32fb8de7322f77b1018ae95f3cb12210634e`. Actual06:48:09 process cleanup passed. Sweep08/tool43694 is running the content checks under the standard 5-second watcher with a 5-minute inactivity warning. Settings10 follows. The image remains an engineering candidate; the RC/device-ready gates have not passed.

**Remaining order:** sweep08 → settings10 → link10 → guest10 → runtime11 → proxy09 → optins09 → memory09 → UI11 → predecessor07 → subset06 → cloud-ui05 → signin-ui05 → signin-1g05 → ordinary RetroAchievements proof → P4 primary OpenAI plus Fable5.1/xhigh through the verified Facilitator → H700 DDR4/RG35XX SP arm, then aarch64. Predecessor07 requires the completed boot04 proof and an actual UI11 visual review. External inputs and P5 publication gates remain recorded. Can this be done on the VM? **Yes.**

#433/#436 stay closed from their artifact-scoped replacement08 repair proofs. #437/#438 are closed with published evidence. Publish the scoped #439/#440/#441 repairs and close them from their own acceptance evidence; their closure does not qualify the whole candidate.

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
