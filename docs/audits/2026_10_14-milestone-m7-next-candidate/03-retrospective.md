# Retrospective — M7 next candidate (#590)

**Auditor:** /root/m7_audit_resume, sole serial Code Auditor; OpenAI Codex harness, exact served model unverified.
**Date:** 2026-10-15
**Subject:** Milestone delta, frozen distribution fac608ff89940ce358ea9b8a95e9a08a6fe26568 and ES3178b832b8d134198b2b4eede4f725d4ed283f8c.
**Spec:** scope-manifest.json and /tmp/pix-m7-candidate-audit-scope.md; 115 criteria from26 issue snapshots.

## Architectural assessment

The change composes existing interfaces: ES remains the controller, asynchronous Wi-Fi work owns bounded backend children, cloud and offline controllers retain their locks/state contracts, and Steam's separate client/runtime/FEX/Proton publication paths protect existing trees. Dolphin's new generic build reuses the standalone engine and launcher rather than a simulated substitute. No replacement cloud transport or default newest-wins resolver was introduced. New complexity is concentrated in the2,755-line Steam shell/Python installer and the native RVZ reader; their negative controls and exact input contracts matter more than a global suite title.

Three frozen defects remain: unbounded Proton release metadata outside the otherwise bounded installer; missing default NoGUI achievement initialization despite enabled Core configuration; and a compiled immutable Dolphin resource path that installation does not supply. The latter two are integration failures: correct components and flags did not establish the frontend and resource lifecycle. Post-freeze source repairs and selected runtime controls are supplemental, never silently substituted into the frozen snapshot.

## Instruction-file conformance

Rules read from current next; coordinator worktree rule comparison matched next at audit setup/resume. Scoped change-log, packaging, generic VM, handheld-evidence and rclone rules were included. Symbols: ✓ supported within scope; ⚠ open or bounded evidence; ✗ confirmed violation; · not applicable to this delta. A positive row is not certification of every inherited rule implementation.

| Rule | Relevance | Finding |
| --- | --- | --- |
| adversarial-council.md | ⚠ | Independent cross-lab route selected; primary exact model is unverified, external blind/refutation remains Phase4.6. No council claim. |
| bugs-are-agent-first.md | ⚠ | Known source defects have concrete original/source evidence; no RC assertion. Native remaining scope stays open. |
| ceremonies.md | ⚠ | Current audit is the milestone ceremony; punch list/lint/issue resolution remain serial gates, not assumed completed. |
| decision-register.md | ✓ | D-CLOUD-175/184, D-WORKFLOW-162/164/165/166 and existing QA boundaries used; no superseded migration gate revived. register-check0. |
| device-builds.md | ✓ | Frozen generic build/admission originals read; no auditor build, device action, or release publication. |
| documentation-accuracy.md | ⚠ | Canonical flow/frame references present; public setup documentation remains existing #577 scope. |
| engineering-practices.md | ✗ | Dolphin lifecycle/resource mismatches survive artifact review; Steam metadata breaks bounded waiting. Originals, failed controls and source provenance preserved. |
| es-code-traps.md | ✓ | Wi-Fi callbacks use guarded lifetime and stable list component; phone literals/escaping read; selected C++ syntax originals0. |
| es-native-ui.md | ✓ | Existing row/card/async conventions retained; EN/FR640/1280 frames directly reviewed. No unsupported standalone auto-state promise. |
| es-player-text.md | ✓ | Player account distinct from compiled scraper identity; Wi-Fi, saves and game-content language preserved in reviewed source/frames. |
| es-ui-style-guide.md | ✓ | Parent→child routes, cancel/return and refusal branches examined; reviewed original frames bound to source, not names alone. |
| fork-workflow.md | ⚠ | Frozen worktree/pin/source boundaries explicit; publication and upstream contribution disposition stay coordinator-owned. |
| instruction-files.md | ✓ | Current rule/skill comparison performed and scoped files read. rules-check0. |
| issue-tracking.md | ⚠ | 115 literal criteria captured; #592 requested/filed by coordinator before implementation. No auditor tracker mutation. |
| learning-capture.md | ✓ | Discoveries recorded durably in audit running log/findings; coordinator owns shared work log and rule integration. |
| least-surprise.md | ✗ | Default NoGUI achievements do not work on frozen source despite settings; missing Sys root violates normal asset lookup. Other narrowed behaviors preserve retained state. |
| milestone-phase-naming.md | ✓ | Scope anchored to current M7 plan and #590; no independent reordering or duplicate runtime allocation. |
| player-language.md | ✓ | Shorter phone status and constrained Wi-Fi/list guidance viewed; raw error/path text kept clear in selected panels. |
| release-candidates.md | ⚠ | This is an engineering snapshot audit. Full audit, new installed/native proof and later device gates are outstanding. |
| time-to-play.md | ⚠ | Memory/browser/async latency controls bounded; final image gameplay/first-frame and save/reload gates not yet satisfied. |
| upgrade-and-install.md | ✓ | Actual clean-first-boot, retained update/backup and selected account/history equality read; no clean-state-only promotion. |
| vm-first.md | ✓ | All behavior proofs examined are local VM/source/component proofs; physical/provider limitations explicit. Auditor launches none. |
| working-principles.md | ⚠ | Evidence and preservation discipline followed; confirmed component-composition gaps require repair. |
| worktrees.md | ✓ | Exact named frozen checkout retained, no detached rebuild or auditor source mutation. Coordinator later commit rewording does not alter frozen fac608. |
| change-log.md | ✓ | October14/15 sections exist with component/native qualifications and distinct frozen/post-freeze status. Some conservative pending language may lag later proof but does not overclaim. |
| council-substrate-integrity.md | ⚠ | Applies to later external invocation infrastructure: Facilitator only, no direct call or council genesis. Packet preparation cannot satisfy identity verification. |
| generic-x64-vm-testing.md | ⚠ | Original stages, exact binary/image binds, failures, process reaping and cleanup directly read. No substitution of source-chroot Steam for ARM64 or private Dolphin for installed new image. |
| handheld-evidence.md | · | No physical hang/radio/power-cycle claim added; native guest artifacts retained independently of logs and screenshots. |
| packaging-and-patches.md | ✗ | Recipes pinned and package checks present; Dolphin custom install omits compiled Sys path. New #592 package fix must requalify install. |
| rclone-cloud-sync.md | ✓ | No filter/transfer policy delta. Actual selected account/stamp equality, secret-free backup and installed WebDAV/SFTP/S3 receipts preserve the interacting boundary; no hosted-account gate invented. |

## Project invariants and spec fidelity

Progress preservation is evaluated from original bytes/types and link identities, not the word safe: Steam component/full-caller maps retain old game/user/SDK/Proton/FEX roots; Dolphin path helpers refuse ambiguous real directories and preserve contents; Recent import has selected account/stamp equality independent of membership. These do not prove every native writer's save/reload behavior. No new sync allowlist or deletion-policy change appears in the product delta. Actual backup receipt excludes device accounts and cloud selection; the shared ScreenScraper developer identity is an explicitly approved build identity exception, not a player credential.

The fresh Recent default remains `favorites,recent`; token normalization preserves explicit choices. RVZ retry targets only prior failed sentinel hashes in supported GameCube scope; successful/indexed pairs do not force a broad rescan. Phone geometry changes retain the native bridge and conditional cancel/lifetime semantics. Wi-Fi failure retains prior rows while a later scan replaces them; close prevents UI use-after-free while the bounded backend read may finish. None implies instantaneous cancellation of the underlying radio/backend work.

The false frozen package comment that Core ownership makes achievements frontend-independent is a genuine spec/implementation contradiction. The missing Sys root is separately inherited packaging debt activated visibly by the lifecycle repair; it is in scope because the milestone newly includes/qualifies standalone Dolphin. Native ARM Steam execution, real client self-update and abrupt power loss are documented limits of #582's caller proof, not newly invented checkboxes. Device-specific foundation merges remain explicitly inherited/off-delta.

## Platform architecture conformance

| Check | Relevance | Finding |
| --- | --- | --- |
| Reference implementation / tenant zero | · | No tenant platform; GENERIC_X64 is a concrete qualification vehicle, with actual installed binaries distinguished from scratch sources. |
| Schema before code | ✓ | Existing receipt/state/transaction contracts retain fail-closed validation; no new cloud manifest schema was silently substituted. |
| Dogfooding gate | ⚠ | Actual VM controls and public sign-in page used; new final installed/native composition remains pending. |
| API first | ✓ | Existing ctl/HTTP/launcher contracts reused; no new duplicated cloud backend API. |
| Build versus adopt | ✓ | No standalone build-vs-adopt register found by `rg --files docs plans .github --glob '!docs/audits/**' --glob '!docs/qa-logs/**' | rg -i 'build.vs.adopt|adoption.register'` (exit1). Skill treats it advisory without that register. D-WORKFLOW-162 research and the actual upstream RVZ/proxy/Dolphin adoption records provide the applicable rule; no invented register mandate. |

## Cross-system interactions

### ES asynchronous Wi-Fi × wifictl and page lifetime

**State shared:** current result list, selection/viewport, backend job and selected network configurations.
**Wipe risk:** stale callback mutates destroyed/reopened page; failed scan replaces valid rows; forget removes a sibling connection.
**Test coverage:** TESTED for source/UI components and later actual installed WiFi03 with controlled lower backend; physical radio behavior excluded.
**Finding:** guarded shared/weak job lifetime and bounded reads inspected. Original failed scan keeps three rows, later result becomes two, disappearing selection falls back, Home connect and CafeA forget leave CafeB and active Home intact.27 started jobs/27 ends; selected restoration limited to five named configurations, not es_settings.cfg.backup. No claim of instantaneous child cancellation.

### Browser handoff × ES allocator × installed dependency closure

**State shared:** frontend process heap and browser/WebKit/GStreamer/phone lifecycle.
**Wipe risk:** allocation retained during external launch, missing shared library, stale phone page or canceled child.
**Test coverage:** TESTED within bounded allocation/open/return/cancel and installed loader controls.
**Finding:** actual malloc_trim comparison and loaded public page distinguish a memory measurement from a blank page. Final fac loader/gst-inspect checks retain GStreamer tools/network libraries. Native phone input/status originals bind their shipped source;48 retained original phone frames,24 sampled directly. Real provider sign-in and physical input are not inferred.

### Recent library import × device accounts and history

**State shared:** imported gamelist metadata, selected cloud/account configuration and cloud stamps.
**Wipe risk:** copied ROMs mistaken for play history; import resets device account/last-run state.
**Test coverage:** TESTED in library03 exact unchanged-source selected-state receipt.
**Finding:** Recent membership derives playcount/history, not file presence. Three selected account configs, exact rclone/active selection and cloud-sync stamps match before/after ROM-only and history import. This is the preservation proof; membership alone was insufficient. Unknown source-device origin is not fabricated.

### Steam client × runtime/FEX/Proton × retained profile

**State shared:** Steam directory, SDK/profile aliases, runtime libraries, FEX roots, separately installed Proton families, active-client processes.
**Wipe risk:** repair deletes shared trees; uncertain stage promoted; child survives into retry; metadata request holds foreground indefinitely.
**Test coverage:** TESTED source-helper/full-caller controls, including14 additional exact-frozen callers; PARTIAL native installed execution/power loss.
**Finding:** per-component journals, strict archives, lock/identity checks and original protected maps support bounded claims. The two top-level Proton metadata calls bypass those bounds: confirmed defect. Supplemental fixed function passes installed curl/Bash normal/oversize/stall/retained-config controls. Existing client exec was denied by fixture and never counts as usability.

### ES RVZ hash retry × proxy scanner × native format libraries

**State shared:** game hashes, indexed cache, failed32-zero sentinel, source-library decoders.
**Wipe risk:** broadened rescan rewrites successful hashes, malformed compressed input commits false hash, sentinel becomes valid game identity.
**Test coverage:** TESTED bounded native/component formats and actual installed top-up; PARTIAL default Dolphin end-to-end gameplay.
**Finding:** retry restricted to failed GameCube RVZ and unsuccessful/unindexed pairs; scanner keeps successful cache. Proxy padding fix has126 old-source mismatches→0 current on unaligned corpus and aligned/invalid controls. Current installed and earlier native receipts are distinguished by bytecode/library hashes and source-pins-verified flags. No universal format coverage inferred.

### Proxy startup connectivity × signed queue and service stop/restart

**State shared:** initial connectivity value, monitor callbacks, pending signed SQLite awards and flush worker.
**Wipe risk:** initial offline→online transition lost, duplicate flush, unsigned/auth-refused award removed, shutdown leaks worker.
**Test coverage:** TESTED original actual-service negative, corrected actual-service and installed default unit plus10 bounded components.
**Finding:** original first-worker online transition never flushed; corrected boundary does once. Independently read actual timing/queue changes and SQLite integrity. Service pause/real lock/restart controls and HMAC/auth failure originals cover interactions rather than isolated functions. No new real-provider award spent.

### Dolphin HostUrl settings × default NoGUI lifecycle × immutable resources

**State shared:** configuration, achievement singleton, Core boot/thread lifetime and packaged Sys assets.
**Wipe risk:** INI produced correctly but never consumed by an initialized client; missing read-only resources undermine normal engine behavior.
**Test coverage:** BROKEN in frozen source; supplemental private candidate lifecycle tested, resource mismatch newly confirmed.
**Finding:** NoGUI lacks Init/Shutdown while Qt/Android initialize; baseline logs uninitialized client. Post-freeze candidate makes one loopback login and clean shutdown, disabled no client, early boot failure cleans up. Four badge errors then expose the absent compiled Sys root. Root #592 owns package correction; neither private candidate nor source correction proves new installed-image behavior.

### Standalone save paths × launch routing × save-state manager/cloud capture

**State shared:** physical save directories, configuration aliases, emulator/core selection and capability flags.
**Wipe risk:** path normalization discards real retained directories; manager offers unsupported standalone auto-state; cloud capture observes wrong writer/path.
**Test coverage:** TESTED refusal/preservation/UI controls and actual mount; PARTIAL native save/reload/engine binding.
**Finding:** literal source and104+51 retained controls support link-only changes/refusal behavior. Genuine native RA/Dolphin/Flycast game-save and selected engine/effective settings remain parent-owned pending final image. AC063 deliberately corrected toPARTIAL. No additional auto-state scope invented.

### Baseline harness × child reaping and frame claims

**State shared:** child liveness observations, source-root routing, browser status DOM and screen comparison claims.
**Wipe risk:** zombie mistaken for running helper; warm image harness used instead of supplied source; an unmatched frame waived by blanket claim.
**Test coverage:** TESTED original7 script failures and corrected scripts/SFTP/S3 continuation; frame claim supplement needs separate source/original review.
**Finding:** subreaper now waitpid-reaps only direct adopted children with WNOHANG while preserving stage Popen.wait; no kill disguised as success. Waiting status selector keeps nonempty/no-button checks. Original frame-diff65-unclaimed failure retained; a later host comparator result cannot silently rewrite it.

## Defect-shape enumeration

| Defect | Site / sibling / adjacent | Disposition |
| --- | --- | --- |
| Unbounded metadata | Site fetch_proton_latest_release:213; sibling callers:2748,2750 use same function | FIX-NOW #580/#590, later bounds-only change; frozen still fails. |
| Network bounds elsewhere | Adjacent runtime version curl:1060 has10/30s/128B and subprocess35s; runtime wget:1069 and Proton wget:2630 have900s/death signal/file limit; client transfer:1834 has disable/protocol/redirect/time/size/deadline checks | BY-DESIGN separate bounded transactions; no equal unbounded site found by exact `rg -n 'curl|wget|urlopen|fetch_proton_latest_release' 'projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh'`. Retained curl config of the adjacent runtime path is not given a stronger isolation claim. |
| Missing singleton lifecycle | Site NoGUI MainNoGUI.cpp; sibling Qt MainWindow.cpp:270/349 has Init/Shutdown; adjacent Android MainAndroid.cpp:524 has Init and is outside packaged desktop frontend scope | FIX-NOW NoGUI #584; Qt BY-DESIGN valid lifecycle. No global Core initialization inserted that would double-init the other frontends. |
| Missing immutable Sys root | Site custom makeinstall_target; all GetSysDirectory readers enumerated in finding-dolphin-sys-resources.md | FIX-NOW once in shared installation, #592. No per-resource loader hacks. |

## Missing artifacts and exact search trail

Missing here means not established by the artifacts examined as of this checkpoint, not a claim that no file could exist elsewhere. `rg --files docs/qa-logs --glob '!**/original-adapter/**' | rg '(installed-native-result|native.*(gameplay|save)|native-installed|native-game|frame-claims)'` located native preparations, original save-tool result and installed proxy-native result. Those are distinct from the required final gameplay/save and new Dolphin/Steam installed image. Parent's concurrent source preparation is not completion. Recent coordinator `git log -6 --format='%h %s'` shows source/QA follow-up commits, while the frozen commit remains fac608. Native preparation packets and original controls were already traced in Phase2; no fresh runtime has been launched by this auditor.

Outstanding pre-existing scope: final assembled image/clean-retained acceptance, selected native engines/gameplay/save/reload, documented corresponding-source/publication custody, public setup documentation and this audit's external/final phases. No extra fixture or accepted matrix rerun is prescribed. Frozen defects need narrow repair verification; #592 was discovered during this reverse pass and has its own source-only recommendation. Generic platform schemas, tenant objects and .kno entities are not project requirements.

## Blindspot register assessment

Each registered entry is assessed below; register duplicates number29 (table feature routing and later authorization entry), retained as29a/29b. This is74 distinct entries, not73. Full entry prose was read over the serial research/reverse phases; labels below are navigation aids. ✓ means no repeated defect found at examined seam, ⚠ limitation/pending, ✗ repeated shape, · outside this scope.

| Entry | Result | Evidence / relevance |
| --- | --- | --- |
| 1: Assumed-undone | ✓ | Archaeology and raw library/syntax originals recovered before declaring absent. |
| 2: Same-tag republish ambiguity | ✓ | Full source/image/archive hashes retained; no same-tag identity assumed. |
| 3: `GetShOutput` line-join | ✓ | Wi-Fi typed line parsing and original backend output reviewed; no new GetShOutput join dependence. |
| 4: `close()` inside a page's own handler | ✓ | Weak lifetime job and stable list avoid destroying the active button handler. |
| 5: Row-title `toUpper` | ✓ | Actual EN/FR small/large frames reviewed, labels use existing builders. |
| 6: Verifying a consumed artifact too late | ✓ | Original consumed admissions/results retained and read, not only latest summary. |
| 7: Archiving a tree that contains symlinks | ✓ | Original tar members read directly; symlink types/targets compared in preservation maps. |
| 8: Synthetic-fixture testing that proves nothing about the real pipeline | ⚠ | Synthetic Steam/native-proxy boundaries explicit; final installed gameplay not inferred. |
| 9: Treating futro predictions as decisions | ✓ | Canonical decisions used, future predictions not converted into requirements. |
| 10: Fixing forward only | ✓ | Retained paths, failed journals, retry and unchanged bytes covered alongside clean installs. |
| 11: The build tree has an upgrade path too | ✓ | Build-source/dependency bindings checked; new assembled image remains open. |
| 12: Sweeping with a rule that does not match the resolution order | ✗ | Dolphin compiled Sys resolution differs from the custom package installation destination. |
| 13: Assumed-done | ✗ | Frozen Dolphin package comment overclaims configuration-only frontend support; audit derives115 criteria independently. |
| 14: A guard stored inside what it guards | ✓ | External owner/monitor and stopped-media exports independent of test process; no guard mutation. |
| 15: A destructive command applied uniformly to non-uniform things | ✓ | Dolphin save helper distinguishes real directories/symlinks and refuses ambiguity; Steam quarantines exact owned stages. |
| 16: A runtime dependency with no build-time signal | ✗ | Dolphin Sys asset availability absent despite compile success; #572 loader closures separately corrected. |
| 17: An update path that assumes the state its create path would have produced | ✓ | Old/partial/profile-alias Steam and retained Dolphin sources covered, not only expected fresh layout. |
| 18: Answering a question about the physical world from a source that cannot know | ✓ | No physical radio, panel, device hang or ARM execution inferred from VM/source facts. |
| 19: Escaping that was right where the text used to live | ✓ | Phone HTML/JS exact bytes in actual Chromium and native input bridge reviewed. |
| 20: Editing in one worktree and building in another | ✓ | Frozen fac608/3178 identities explicit, later private candidates kept separate. |
| 21: A boundary enforced at the wrong granularity | ✓ | Protection compared at exact entries/bytes/types, not directory names only. |
| 22: A probe that cannot report absence | ✓ | Original refusals and backend-local WebDAV/S3/SFTP negative cases retained. |
| 23: Deduplicating by deleting the frequent path | ✓ | No menu deduplication removes existing account/transfer routes; Wi-Fi retains current flows. |
| 24: A definition that sits below its new consumer | ✓ | Steam function/helper definitions and global call sequence read whole; no new unset restricting array found. |
| 25: A device path written before the hardware existed | · | No physical disk-selection or formatting performed. |
| 26: A guard bound to a path that moved | ⚠ | No push by auditor; coordinator owns hook/publication validation, not inferred from audit. |
| 27: Supersession that lives only in a comment | ⚠ | Literal issue snapshots/decision supersessions read; final status propagation belongs to parent, no new stale checkbox accepted. |
| 28: Two non-destructive one-way transfers composed into a two-way sync are a recency resolver | ✓ | No new two-way copy composition; existing conflict policy unchanged and round-trip originals read. |
|29a feature has no route|✗|NoGUI compiled achievement code lacks its startup edge; ES parent routes otherwise exercised.|
|29b standing authorization|✓|No auditor device/runtime/external action; authority reserved to parent.|
| 30: A resumed session built on its own summary's claim about the code | ✓ | On resume, frozen source and originals re-read; previous summary used as locator only. |
| 31: A harness that writes and reads through the same wrong path agrees with itself | ✓ | Native endpoint/readback and independent protected maps supplement harness status. |
| 32: Causal ordering read from wall-clock timestamps that jumped mid-boot | ✓ | Durations derive monotonic clocks where relevant; boot/process/source identities separate wall-clock timestamps. |
| 33: A sentinel exit code borrowed from the exit-code space of the tool the script wraps | ✓ | Expected caller1, curl28/63, synthetic exec126 and harness0 distinguished. |
| 34: A check written for the device, proven only under the host's tools | ⚠ | Installed curl/Bash and final loader checks available; native ARM Steam explicitly unverified. |
| 35: A remedy built on an audit's claim about a default nobody read | ✓ | Settings default read at frozen Settings.cpp, exact token grammar checked. |
| 36: One backend in the harness, and its semantics mistaken for the contract | ✓ | Installed local WebDAV/SFTP/S3 receipts retained; no broad provider equivalence claim. |
| 37: A mechanism built by hand while the image carried it, switched off | ✓ | Existing ctl/rclone/ScopeGuard/atomic rename mechanisms reused; no alternate service built. |
| 38: A category-level offer read as a standing yes for every action in it (2026-09-11) | ✓ | Auditor performs no device/runtime/external action; root owns explicitly authorized allocations. |
| 39: A new suite that passed over a table of dashes (2026-09-12) | ✓ | Original per-case attempts/child statuses/nonzero controls read; no empty suite promoted. |
| 40: A suite that passed on the caller's shell (2026-09-13) | ✓ | Actual fixture interpreter/tool hashes and VM identities retained. |
| 41: Verified at a size no handheld has (2026-09-13) | ✓ | EN/FR640×480 and1280×960 frames directly viewed; phone viewport profiles identified. |
| 42: "Not me", read from the transcript instead of the device (2026-09-14) | ✓ | Parent reports treated as leads; source and original receipts read directly. |
| 43: A safety claim in a header comment, never tested (2026-09-14) | ✗ | Dolphin package comment does not supply initialization or immutable Sys files. |
| 44: Proven at a fixture's size, not the device's (2026-09-14) | ⚠ | RVZ compressed/decoded/member limits and installer archive contracts checked; full personal-library scale not claimed. |
| 45: Proven at a fixture's speed, not the device's (2026-09-16) | ⚠ | Metadata real stall/streaming oversize exercised; native device/real provider speeds unmeasured. |
| 46: A name read as a behaviour (2026-09-19) | ✗ | Core-owned AchievementManager still requires frontend Init; name alone gave wrong assurance. |
| 47: A dependency the build fetched for itself (2026-09-20) | ✓ | Actual compiled closure/package dependencies and retained build provenance examined. |
| 48: A constraint that lived only in a commit subject (2026-09-20) | ✓ | Scope/refusal/remaining-native limitations durable in issues and audit artifacts. |
| 49: An edit made blind to the compiler (2026-09-21) | ✓ | Actual original ES syntax stage0 and exact unchanged selected sources, not preparation claim. |
| 50: A log check that never asked whose log it was (2026-09-21) | ✓ | Per-case original stderr, process hashes and exact-run archives read. |
| 51: A checklist built from open boxes inherits stale boxes (2026-09-21) | ✓ | All115 verbatim criteria reconstructed; initial open/closed checkbox state does not drive verdict. |
| 52: A decisions list built from an issue's section, twice (2026-09-23) | ✓ | Canonical decision register searched/read; no issue-only decisions list substituted. |
| 53: An audit's own headline was typed, not summed (2026-09-24) | ✓ | Forward counts mechanically checked and corrections retained; final synthesis will derive current effective verdicts. |
| 54: A measurement on a guest whose renderer was not the device's (2026-09-24) | ⚠ | Browser/ES frames use declared guest profiles; no new RetroArch visual gameplay approval before actual surface proof. |
| 55: Blindspot 54's own guard read a line it had not tied to its launch (2026-09-25) | ⚠ | Pending native gameplay must bind renderer to that launch; previous log cannot satisfy it. |
| 56: A timing run passed over a sync that had no cloud to reach (2026-09-25) | ✓ | Real local endpoint readback and actual public-page loaded witness distinguish no-op runs. |
| 57: A fix that covered fewer sites than its issue named (2026-09-25) | ✓ | Metadata callers and Dolphin frontend/resource siblings explicitly enumerated. |
| 58: A link error the source contradicted, read as the code's (2026-09-25) | ✓ | Original build/container return channels and existing warning multiset separated; no warnings-as-harmless claim. |
| 59: A memory measurement that passed on a page that never loaded (2026-09-25) | ✓ | Loaded public sign-in page/repeated-open identity was checked alongside RSS. |
| 60: A harness fixture the harness did not own, and an issue filed on a log's last lines (2026-09-25) | ✓ | Fixtures have private owners and original failures; no new issue based only on summary tail. |
| 61: The suite under test started as a shell background job, so the signal it tests was ignored before it began (2026-09-26) | ✓ | Real signaled caller/child statuses and original wait channels retained; no audit replay as background shell. |
| 62: A fix corrected the writer and left what it had already written to heal by play (2026-09-26) | ✓ | Existing failed RVZ sentinel retry and retained installer recovery exercised; historical outputs not assumed healed by future play. |
| 63: The options said llvmpipe, the renderer said softpipe, and nobody read the renderer for a month (2026-09-26) | ⚠ | Actual installed native gameplay renderer remains pending, not inferred from requested backend. |
| 64: A wait was lengthened three times for an event the code had no path to produce (2026-09-27) | ✗ | Frozen NoGUI can never produce client initialization; adding wait would not fix it. |
| 65: A proof's substitute passed where the real input failed, twice in one day (2026-09-27) | ✓ | Real Steam archive layout55members, actual installed curl and original full-caller boundaries used; private candidates labeled. |
| 66: A verification pass keyed by finding number missed a Critical whose number the other seat had used (2026-09-28) | ⚠ | External findings not received yet; Phase4.6 must grade by underlying assertion, not colliding IDs. |
| 67: A credential-shaped test fixture reached history before any guard read it (2026-09-28) | ✓ | Private source/build identity values must be redacted before external packet; no player/account credentials included. |
| 68: A verdict was confirmed, re-graded, and then carried nowhere (2026-09-28) | ✓ | AC063 correction and AC091/093 evidence upgrades appended explicitly; synthesis must use effective values. |
| 69: A page test whose stubs were kinder than a browser passed a script that died at load (2026-09-29) | ✓ | Actual Chromium phone DOM/screens and native bridge input receipts reviewed. |
| 70: An upstream series shaped by the fork's process, not by the reviewers' capacity (2026-09-29) | ⚠ | Upstream contribution dispositions identify owning projects; no upstream PR series authored by auditor. |
| 71: A QA fixture seeded the product's default by its literal name, and the default moved (2026-10-01) | ✓ | Default Recent/Favorites read from source; fixtures do not silently seed a stale literal as expected default. |
| 72: A comment held an invariant the code had stopped keeping, and the guard it described ended only a subshell (2026-10-01) | ✗ | NoGUI comment promises behavior absent from executable lifecycle; metadata call escapes surrounding helper bounds. |
| 73: A monitor observed package completion instead of build activity (2026-10-03) | ✓ | Original watcher/command/runner channels plus owner/cleanup read; mere package completion not treated as final job success. |

## Retrospective summary

Architectural coherence is good at the retained-state transaction boundaries but incomplete at Dolphin composition. Overall conformance is MEDIUM while the three concrete defects and final integration evidence remain open. Cross-system tests are substantial and explicitly bounded; native gameplay/save and final installed repairs still require original results. No further confirmed source defect was found in this pass beyond the three named findings. Continue to synthesis/self-refutation and prepare the cross-lab blind packet; do not stop at this checkpoint.
