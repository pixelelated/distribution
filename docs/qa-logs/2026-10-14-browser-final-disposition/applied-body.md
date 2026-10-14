## Final software disposition — October 14

The software evidence for this investigation is complete on distribution `fac608ff89940ce358ea9b8a95e9a08a6fe26568` / ES `3178b832b8d134198b2b4eede4f725d4ed283f8c`. The original severe handheld slowdown remains unexplained and is retained as the concrete watch below. This does not claim a physical-device cure, faster provider pages, or authenticated hosted-provider success.

The earlier actual-binary comparison measured **79,882 KiB (78.01 MiB)** less ES anonymous memory in its stated common window, with three additional same-process handoff cycles. Original baseline memory-guard failures remain failures. One boot, software rendering, live-provider variability and unequal observation lengths limit the result; it is not a new final-image memory measurement. [Original measurement, frames and limits](https://github.com/pixelelated/distribution/blob/0457ac18cd061e159d19aa46f53a57eed94e42c0/docs/qa-logs/2026-10-13-es-trim-comparison/README.md).

Synthetic browser-start failure exposed stale opening feedback. The repaired compiled frontend passed native/phone retry/cancel at EN/FR640/1280 plus the recorded recovery/completion/expiry/provider-failure/Back branches, with reviewed frames and original timing/exit receipts. The tested allocator file, recovery code and selected EN/FR recovery messages carry unchanged into ES3178. [Compiled source and failure history](https://github.com/pixelelated/distribution/blob/0457ac18cd061e159d19aa46f53a57eed94e42c0/docs/qa-logs/2026-10-13-setup-qualification/README.md), [installed component branches and reviewed frames](https://github.com/pixelelated/distribution/blob/0457ac18cd061e159d19aa46f53a57eed94e42c0/docs/qa-logs/2026-10-13-setup-qualification/installed/README.md).

Final image `0.0.1-dev+20261014T230300Z.gfac608ff8994` then passed actual installed browser/phone navigation, both-page text delivery and return on the same frontend/boot, using the documented synthetic provider seams. The browser's expected cancelled-branch exit1 remains1; broker and all outer owner channels are0. Untouched clean-state inspection and default-loader checks pass; the real retained-storage update to the corrected image also passes installed default-loader/state-preservation checks. Both admissions are consumed. [Final installed UI and originals](https://github.com/pixelelated/distribution/blob/0457ac18cd061e159d19aa46f53a57eed94e42c0/docs/qa-logs/2026-10-14-corrected-image-ui/README.md), [retained update/default-loader proof](https://github.com/pixelelated/distribution/blob/0457ac18cd061e159d19aa46f53a57eed94e42c0/docs/qa-logs/2026-10-14-corrected-retained-loader/README.md).

Whole-image standard/release qualification remains separately tracked; this disposition adds no duplicate memory comparison, old-owner replay or physical corroboration gate. Historical “next” paragraphs below describe what was open at their dates and are superseded by this status.

Already written: the older frontend could retain memory and leave stale opening feedback during a failed sign-in launch. The repair changes transient handoff/recovery behavior; existing saved connections and selected cloud paths are preserved. No owner data migration or deletion is part of this fix.

### Keep an eye on — original handheld incident

The severe slowdown/full hang was not causally established or fully reproduced by the bounded VM/bench observations. On a future separately authorized recurrence on the designated RG35XX SP/H700 bench, retain exact BUILD_ID, page/navigation phase without credentials, monotonic input issue/acknowledgement/visible-update observations, browser/frontend identities, pressure/reclaim aggregates and bounded kernel logs, and whether browser close restores the same frontend and boot. A repeatable input/handoff failure or timestamped crash/pressure record tied to those identities is the concrete trigger for a new source-bound bug/VM fixture. No test, sign-in, reboot or account action is authorized by this watch. This applies the existing criterion's explicit watch alternative and D-QA-051; it does not label the incident cured.

## Earlier intake and evidence history

## Current result — actual compiled memory comparison and repeated handoff complete

Published record `0ea6eaf74ad47503c05955d1c0bd4bd00bdfb816`; both exact-head hosted checks passed, original delivery exited 0 and all recorded processes exited. ES review branch `feature/m7-es-trim-570` at `f7b71db0a70e1c48627f70847ecbc95bb1cb4a43` is published; distribution pin remains unchanged.

The actual compiled candidate reduced ES anonymous memory by **79,882 KiB (78.01 MiB)** in a bounded 1280 MiB assigned, software-profile VM comparison. Unchanged installed browser, broker and rclone; no interposer. Old/new/new/old trials: both old-binary sessions hit the memory guard after 8–9 seconds; both candidate sessions completed 60 seconds and returned normally. The common 2–6-second window was selected after the first guard stop; unequal observation lengths, one boot and live-provider variability limit the result. This does not establish faster browsing or a physical-device cure.

Three additional 25-second browser launch/close/reopen cycles passed on one unchanged ES process and boot. ES anonymous medians were 33,784 / 34,552 / 35,164 KiB. This is bounded repeat-use evidence, not a long-term leak test. Earlier compiled-source and native/phone smoke evidence remains accepted for its scope.

Ten submitted owners are consumed: nine created watched runs and one pre-run refusal. Original guard and fixture failures remain failures. The VM, UEFI state and temporary keys are removed, recovering 2,275,385,344 allocated bytes. Nineteen reviewed frames have explicit dispositions, including two rejected early black return captures; eleven frames are public. [Source identities, raw results, frame index and cleanup receipts](https://github.com/pixelelated/distribution/blob/0ea6eaf74ad47503c05955d1c0bd4bd00bdfb816/docs/qa-logs/2026-10-13-es-trim-comparison/README.md). A fresh no-context resume review reproduced the result; it was not an independent code audit.

**Next:** browser-open failure and remaining success/failure branches; broader standard-profile source-bound UI coverage, including 1280×800 and French as required; separately scoped RG35XX SP physical corroboration. Use fresh capacity admission and watched owners. Do not replay completed owners. #570 remains open; no pin promotion or new RC is claimed.

## Historical October13 compiled candidate and bounded VM smoke

ES review branch `feature/m7-es-trim-570` at `f7b71db0a70e1c48627f70847ecbc95bb1cb4a43` is published; distribution pin is unchanged. The exact seven-line allocator proposal compiles/links, and disassembly confirms teardown → malloc_trim → wait → restore. A fresh640×480 VM running that binary passed native-mode virtual-key input, actual phone-page16-character input across two page loads, and normal return with the same frontend/boot.13reviewed frames (11public); no completed authentication, physical-device cure,1280/French or full lifecycle claim. Hardware rendering was requested but separately verified runtime renderer evidence was not retained for that smoke test.

All15original owners are consumed/exited; failed ccache and setup attempts stay failed. Disk/UEFI/keys and independent package copy retired,3.17GB allocated file bytes recovered. Only the11.8MB candidate binary is held for immediate further qualification. Record `7484a2b46d` and both exact-head hosted checks pass; delivery ended0/exited. [Exact source, results and frame evidence](https://github.com/pixelelated/distribution/blob/7484a2b46d09dee87a01564bf9e7e7bdf6b60cc1/docs/qa-logs/2026-10-13-es-trim-product/README.md).

Next: actual-binary constrained-memory comparison under the fresh VM-first plan at issuecomment-6153030650, then remaining same-process lifecycle, success/failure and broader source-bound flows before pin promotion. Earlier75.73–77.64MiB diagnostic reclaim is not this binary's measured saving. #570 remains open.

Investigate a reported regression in handheld browser authentication responsiveness. Compare accepted browser engine, rendering, phone-input bridge and user-agent changes with the earlier build; distinguish device load, network/provider delay and a reproducible product regression. Do not assume the user agent is the cause.

Can this be done on the VM? Yes for navigation/input timing and source regressions with synthetic pages. Read-only owner incident load/log observations identify actual H700 constraints. Later explicit owner WebKit-test permission covered the bounded public-page launch, screenshots and cleanup recorded below; no account/cloud operation or reboot was performed.

- [x] Source-bound comparison identifies relevant changes and earliest supported good/bad evidence, retaining uncertain attribution.
- [x] Sanitized load/log observations distinguish browser, input bridge and resource/network candidates without exposing authentication contents.
- [x] Reproduce any confirmed software defect with a synthetic VM fixture, repair it and retain reviewed flow/frame and timing evidence; otherwise record a watch item with a concrete next observation.

Related #536 and #571 (phone connection-status layout); preserve #565–#567 implementation queue. Original owner report is retained privately.


## Incident and bounded VM results — October12

Retained resource aggregates show severe memory pressure during sign-in; the complete previous kernel log contains243 pressure-flush messages and no recorded OOM kill, panic, or storage error. Exact failure mechanism remains unknown. Source comparison preserves the unknown earlier-good baseline; WebKit/user-agent inputs are unchanged between the two accepted October builds. The low-memory VM loaded the simple and public login pages (original exits0) but did not reproduce the complete hang. Assigned/visible RAM, renderer and direct-launch limits are explicit. No owner device/cloud mutation or speculative production change.

Prepared source-bound evidence: docs/qa-logs/2026-10-12-browser-pressure/. Further navigation/handoff/pressure recovery proof remains open; a successful initial page load is not closure. The task-owned guest and its disk/key have been retired after compact evidence capture. #571 owns the independently diagnosed phone layout shift.


Published record: [2026-10-12-browser-pressure](https://github.com/pixelelated/distribution/blob/515cd8e79a94b3a8596128e25e28875093f5eb50/docs/qa-logs/2026-10-12-browser-pressure/README.md). Incident/source triage is published; the underlying cause and production recovery/fix remain open.

## Controlled isolation completed — October12

Nine constrained VM cases and the separately authorized H700 probe are complete, consumed and retired. Public login reaches the physical low-memory guard at34s:153MiB available,502MiB total browser PSS and430MiB page-process PSS; closing restores572MiB available with the same frontend/boot. Simple-page control leaves522MiB. No full hang or engine-specific regression is claimed.

Older application/current engine, desktop UA, cache policy and supplied GStreamer runtime pieces show no meaningful memory benefit in those VM controls (peak PSS380–394MiB). The GPU-enabled VM retained WEBKIT_DISABLE_DMABUF_RENDERER=1; it did not compare accelerated browser rendering against the disabled path. All initial pages load despite low headroom. The synthetic focus-polling latency difference requires repeated reordered trials and real navigation/input/ES-handoff proof. No production optimization is selected. Earlier October5 loaded-page evidence already shows a heavy workload; the old246MiB Dropbox number was a failed page. The existing DMABuf mitigation remains.

#572 owns confirmed missing controller/scanner packaging. Fresh-registry failure1 becomes success0 when supplied, and warnings disappear without RAM benefit. Historical October12 status: actual recipe/package repair and an older-engine comparison were then open; all runs then used2.54.1. The October13 checkpoint below supersedes those next-work directions. Source/fixtures/samples/11 reviewed frames and limits: docs/qa-logs/2026-10-12-browser-isolation/.


## Current October13 checkpoint — whole stack and renderer controls

#572 recipe/package/install/fresh-registry repair is published in2292e9a298; final assembled-image closure remains open. Isolated2.54.0 and2.54.1 comparisons both showed pressure and do not justify downgrade. The owner's upstream troubleshooting rule is published and #573 closed.

D-QA-060 designates the separate RG35XX SP browser bench, protecting saves/account configuration and other owner data. All eight physical controls across three watched owners are complete; all original launcher/wrapper/build channels0, actual owners/device units ended, temporary device files hash-verified and retired. Same boot/frontend/proxy/compositor PIDs; final546.7MiB available. No save-writing operation, game, sign-in/cloud operation, firmware change or reboot. No browser test remains running.

Idle whole-process PSS: RAOfflineProxy105MiB, ES102MiB, Tailscale43MiB, Sway26MiB; this is overhead, not evidence of a leak. Simple off/on paths load at134/164MiB browser PSS and actual Panfrost clients distinguish page-process acceleration. Final public on/off both load but hit guards at different times; their373/483MiB truncated peaks do not rank memory efficiency. Earlier three public controls stopped before load and remain incomplete. Vmstat confirms reclaim/refault work, not its original cause. Source/numeric evidence/5reviewed640x480frames/original channels/limits: docs/qa-logs/2026-10-13-browser-stack/.

The browser has no proxy dependency, but the current service owns reconnect/startup award upload, optional caching/watching and periodic refresh. Existing emulator launchers do not start it on demand. No owner proxy stop/restart was tried. VM follow-up must prove queue/DB integrity, readiness, recovery and background duties before selecting idle-footprint reduction or a browser-owned unload/restoration. See proxy-lifecycle.md.

Historical next steps after the October13 historical review (superseded by the completion record below): normal ES handoff with the same fixed synthetic page and viewport/keyboard policy, comparing no phone client, idle polling and scripted typing/drag/navigation. Measure input issuance/acknowledgement/visible application separately from page heartbeat, process/kernel/GPU load and recovery. Then independently control focus probing/background proxy load with synthetic data, followed by the2.52.6 engine boundary. The host queue controls prove coupling and retained coalescing, not incident causality or device latency. [Historical review and controls](https://github.com/pixelelated/distribution/blob/4a1274ab806bf583c78646d01fb82bb6fb8f9ef7/docs/qa-logs/2026-10-13-browser-history/README.md). No production optimization or root cause is selected; #570 remains open.

## Current trial closure and next work — October13

All22 normal-handoff/actual-authorization trials are complete and the shared VM/disk/keys retired. Evidence packets: docs/qa-logs/2026-10-13-browser-handoff/, 2026-10-13-dropbox-user-agents/, 2026-10-13-dropbox-breakpoints/. Repeated desktop UA trials are more consistently responsive, but memory remains high. CSS-width screening shows no consistent narrower-layout benefit. Cookie overlay and authentication limits remain explicit. User-agent bundle changes do not attribute execution cost to any script. No production fix selected.

Parallel source-only Herdr assignments are complete; see the component-result checkpoint below. Coordinator retains all runtime/integration and next script/CPU/reclaim attribution. The owner request and scope remain at issuecomment-6138746073. M7's ordered queue is unchanged outside step0.


## Component result and investigation disposition — October13

Corrected immutable proxy packet914b0ad is verified and integrated locally. Fresh VM20 bytecode imports with installed Python3.14.7 show median PSS26817→26427KiB (390KiB /0.38MiB), anonymous delta388KiB; six child processes exit0. The host-source5442KiB result must not be advertised as target savings: interpreter/platform/source compilation differ. Baseline and candidate synthetic source-module listeners each pass11requests, offline login payload, next-game cache responses, queued signed award/SQLite integrity across two close/reopen cycles, and upstream401 preservation. No full-service/systemd/ES/browser/provider acceptance.

All original boot/experiment/retirement channels0, actual owners exited; fresh disk/UEFI/keys removed and2,244,435,968allocated bytes recovered. Exact source, fixtures, results and retirement: docs/qa-logs/2026-10-13-proxy-memory-vm/. Independent reused-context evidence review found no blocking discrepancy; this is not a multi-model audit.

D-WORKFLOW-163 keeps the lazy import candidate diagnostic-only and prioritizes page/script CPU versus reclaim and input-to-paint. Prior real-page pressure already occurs without the proxy. #576's exact GTK4 feasibility inventory is complete, with native keyboard/dependency/sandbox constraints; production migration is deferred pending an isolated spike. No capability removed, product pin/recipe changed, or new full build started. Both worker assignments completed; next runtime belongs to the coordinator under a fresh plan. Record published at `1a37cde40ab0893c9c21c0a383c59ac0c1403b06`; both exact-head hosted checks passed, all delivery03 channels0 and owners exited. The refused delivery02 remains preserved; no published history was rewritten.

