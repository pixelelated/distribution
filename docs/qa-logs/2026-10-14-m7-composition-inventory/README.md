# M7 source composition inventory — 2026-10-14

Source-only handoff for #563, bound to coordinator `b004cd4d0751bd871bfda11292b43280895f61ea`, published `next` `0ea6eaf74ad47503c05955d1c0bd4bd00bdfb816`, the local stable intake, and live issue/milestone readbacks. The coordinator now owns EN640 runtime separately; the checkpoint's earlier “no runtime” statement is historical. No product/shared record/pin was changed, and no test suite, compiler, VM, native program, service or device was run here.

The source set can be composed without reopening accepted component work. The outstanding product investigation is **#588**. The already qualified proxy padding/scanner candidates also still need production packaging; copying their evidence commits alone does not install them. Final clean/retained, installed-service and combined UI acceptance needs an engineering image. It must not become a prerequisite for building that image.

## Exact inputs

[manifest.json](manifest.json) gives full commit IDs, each path's Git mode/blob/SHA256/size, and whether distribution bytes already match the coordinator snapshot. “Ready source” is not final-image acceptance.

| Input | Exact source and integration action |
| --- | --- |
| Stable foundation #563 | Reviewed merge `f370dc87873fecb683c6af73d70a2f377715f47f`, second parent stable20261001 `c445081a59518f37d9776e5412dd7b14910696f7`. All 12 intake reference hashes rechecked; 11 imported paths plus unchanged newer DuckStation recipe. Retain ancestry; exclude later upstream/next. |
| Steam #564/#579/#580/#582 | Final product `03e130e4b3c244337f2e6d782b392a2c444c28e7` contains the complete installer chain; include Steam recipe Python3 dependency `c41a16ad804245285914a6f5b3410f36f9abc26a`. Stable intake is already its ancestor. Do not restore the destructive stable installer while composing. |
| Browser dependencies #572 | `2292e9a2983227a62aaf7846a5b739c41b0841a7`: GStreamer override retains controller and builds scanner. Already in coordinator/next; no WebKit downgrade or GTK4 change selected. |
| Phone #571 / Wi-Fi #577 | Final `cloud_oauth` from `c75b8d1dae18b73f39edbf05b4b0927d9c8bb762`; wifictl `7b2b874cab9cc967cd151180e66d1c92e63cf11e`. Already in coordinator. |
| Dolphin preservation #581 | Compose `b2868df82ed3199e628721ad6fb3f1fb95a3a04a` → `90cd5efad765fcab49ea794122f6fcf45ff19e61` → `1a7714fd81f7c92316f54c4a3648696d1e256f88`. Five final paths: package, helper, both launchers and runemu. |
| Dolphin routing #584 | `c22554a4c0966d48ba405ef1640938d2a417817b`, `cheevos_dolphin.sh`; independent path from preservation. |
| ES #570/#567/#577/#578/#574/#575 | Compiled base `bb9e2785f88c2b9de979022a2a9ded2cbce2f954` includes all ten source commits listed in manifest. Recent default is already in `d242000a5957ad8de5288a02fb15b21d7ef04715`; no second default repair. |
| ES follow-ups | Add MD5 `314da58d68820a79b26f99a5b6c12f9bb37054d5` and French catalog chain ending `09afa4893a6a4667f2b6bd8992bd5957a2281e49`. Both descend from bb9e; neither final French branch nor bb9e includes MD5. Changed paths are disjoint. Final ES commit/pin remains to be created. |
| ES recipe / #565 / #566 | Coordinator already contains `1bf3fa1d32c719ed4e63e1d7b82288d3a80a86f6` (zstd, MIT/BSD notices) and `19221f4762298b10e44a08f2c3e7371c7ddeb0d1` (selected interim developer provisioning and precise state-gate exception). Preserve both when moving the old c8dc pin. Keep current state-check/test and release-preparation integration; these are host tools, not firmware payload. |
| Proxy #583 | Packet `22cfb2385acce6d9c20b20d2f7f40970808777b3`: install exact scanner candidate and package padding patch against current pinned/fork-patched source. Candidate SHAs: scanner `47391a3bbcaa0f2262cdee12f09bd48d17f7fedf0237a1a661a21b085b2f71f7`; decoder `b0d28c147c24c0e6909e8e754915ab4323d766b7fbd711b16c2ce949bd8f3407`. Existing 16 patches remain. |
| Proxy #588 | Separate source worker owns causal startup reproduction/correction in `proxy_service.py`. No final product commit is bound here. Integrate its accepted repair as a package patch after reviewing its baseline/candidate receipts; do not treat normal reconnect PASS as startup-window proof. |

Proxy native recipe pins remain RAOfflineProxy `c7ebd1b6e777f3751ff0ecdf8aba54045844e00d`, rcheevos `1433173220a7eaede6a9ed7a18e94117be1821e0`, libchdr `607694ca0812edfc9cc2030c64634fc2393668de`. The separate current-native-build lane supplies provenance, not a selected new pin. Preserve installed Zstd/libcrypto closure. Diagnostic lazy imports, bytecode experiments, DolphinTool and chdman test binaries are not additional production changes.

## Next integration order

1. Finish the already assigned #588 causal component work and consume the current native-build/EN640 deliveries; retain accepted tests without replay for freshness. Remaining component/native seams keep their recorded limits and original failures. A source defect found by those checks must be repaired before treating the composition as fixed.
2. In a coordinator-owned integration checkout, join the reviewed stable intake with the coordinator source state and final Steam chain. Steam already carries the intake; retain its ancestry once. Preserve newer fork pins/DuckStation, and compare the 11 stable paths plus final Steam override to the manifest. No integration is performed by this packet.
3. Compose Dolphin preservation/routing, proxy scanner/padding and accepted #588 package repair. Compose ES bb9e + MD5 + final French catalog; keep zstd/notices and #566 in the recipe. Update the ES full commit pin only after required source checks and source-bound flow/frame references are reconciled by the coordinator. Do not use broad branch replacement to erase unrelated coordinator changes.
4. Freeze exact distribution/ES revisions, inspect changed package/build inputs and run applicable existing package/syntax/patch checks. Use the delivered #493 admission and current resource measurements before compilation/cache copies. Automatic-retirement infrastructure is separate; no new wait for it is introduced.
5. Build the engineering GENERIC_X64 image. Qualify its actual payload and clean/retained upgrade, selected state and #349 restore; compiled #566 definition/URL/UI/backup behavior; final ES/backend/proxy/default-boot/native integration; frontend and emulator/save behavior; required combined suites/time-to-play and independent review. Preserve original component evidence and add only missing composition/changed-source proof. Native Dolphin/Flycast behavior needs a legitimate disposable playable fixture; malformed-disc or recording-engine refusal proof is not gameplay acceptance.
6. After that acceptance, build H700 then SM8550 with fresh admission. Requalify changed native FEX outputs, Nova kernel/common DP-audio path and ABL1.2/boot-chain facts. Complete #528/#344 custody/licence/publication gates before release designation/publication; they do not prevent producing the engineering image used to obtain evidence.

## Build inputs versus later acceptance

**Before freezing the fixed source:** finish #588, package the accepted proxy repairs, combine the two ES follow-ups, retain Steam's final transaction repair, and bind the final pin/dependencies/notices. Current-native provenance and the remaining scoped component checks follow the live serialized queue; no unexecuted packet is counted as a pass.

**After the assembled image exists:** actual #565 payload/first boot/retained storage, #566 compiled UI and backup exclusion, combined Wi-Fi/backend and phone/browser regressions, actual proxy/default boot and frontend top-up, native save/exit/relaunch behavior, clean/upgrade/restores, complete VM suites and independent audit. Installed/native failures still require repair before acceptance; this distinction does not waive any issue.

The intake changes FEX's Nix input, Steam and ABL plus SM8250 device paths and common Linux7.2 DP audio. GENERIC_X64 uses Linux7.1.2. The common7.2 patch enters SM8550 with MSM enabled; H700 does not enable MSM. Preserve the intake's device scope, rebuild affected outputs from final source, and carry ABL/FEX source/licence custody into #528. Do not attribute these changes as a Nova shutdown fix.

#558/#561 are watch items. #576 GTK4, #587 browser proxy shutdown, #586 replacement developer identity and the listed backlog are not extra RC gates. #585 outward submissions wait until after the initial build under D-WORKFLOW-165; existing local correctness checks remain required.

[tracking-readback.json](tracking-readback.json) retains the live milestone order and latest issue comments with URLs/timestamps; older issue paragraphs sometimes predate completed component proof. [static-review.json](static-review.json) records hash/ancestry checks only. Canonical menu/frame/issue/checkpoint updates remain coordinator-owned. No fresh runtime or RC claim is made.
