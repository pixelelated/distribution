## 1. My findings

These are static counterexamples and gaps, not additional test runs. Paths below are relative to `tools/` unless stated otherwise.

### First: `vm-qa` accounting

A suite’s status depends only on its command’s exit status: 0 becomes PASS, 3 increments `SKIPS`, and every other nonzero status increments `FAILS` (`vm-qa:142-150`). The **runner’s exit code is the final `[ "$FAILS" = 0 ]` at line 541**; SKIPs do not affect it. The supplied cycle demonstrates this distinction: four PASS rows, one SKIP, overall rc 0. That is F-01, not a new finding.

- **G-01 — Medium — `vm-qa:74,85-90,140-150,528,541`:** `--only typo` or an empty selection can produce PASSED without running a suite; unknown names mixed with valid names are silently omitted. No selected/executed-count reconciliation exists.
- **G-02 — High — `vm-qa:55,119-125,139`:** `vm-pair down` failures are ignored, and `vm-pair up | tail -2` hides the launcher’s status. A surviving old guest or partially launched pair can supply the BUILD_ID and receive a green report naming the requested image.
- **G-03 — Medium — `vm-qa:105-110,124,278-291`:** `fresh` always tests port 10022, even when the report names guest b/d. With `--skip-up`, it also proves current links, not that those links resulted from a fresh installation.
- **G-04 — Medium — `vm-qa:163-174,186-191`; `es-untranslated:143-156`:** The lifetime, French and quoting checks can examine an arbitrary `ES_SRC` without verifying its identity against the guest image; clean host sources can qualify different shipped bytes.
- **G-05 — Medium — `vm-qa:131-139,145,533-536`:** Two runs with the same build/backend/guest in one minute reuse the directory, overwrite logs/report, and retain old frames or timing Markdown. A later run can consume evidence it did not produce.
- **G-06 — Medium — `vm-qa:132,139,149,528-541`:** Report-directory and report-write failures are not incorporated into `FAILS`; with writable suite logs but an unwritable report, the command can exit 0 without producing the promised usable report.
- **G-07 — Medium — `vm-qa:247-268`:** `pair-identity` proves an earlier Avahi publication log, not current mDNS answering. Stop Avahi after it logged the correct name and this part still passes.

### Second: `time-to-play` headline acceptance

`headline_missing` checks only existing launch/exit/g2g rows for `None`, plus limited surface and reachability checks; absent or empty arrays contribute no failure (`time-to-play:1306-1332`). `over_budget` tests only the exit-stamp median against three seconds (`:1295-1303`). `--quick` repairs the empty-repeat/selection inputs, but not the following defects (`:1017-1019`).

- **G-08 — High — `time-to-play:641-647,685-689,1184-1200,1295-1332`:** A fast new failure/malformed stamp passes when `qa-cloud:` lists successfully. Stamp status/token, successful payload seeding, actual upload, and the active sync destination are not acceptance predicates.
- **G-09 — Medium — `time-to-play:1227-1252,1306-1332,1347-1350,1399-1497`:** Startup and offline/bounds results—including errors and missing measurements—never affect acceptance. This also affects a full default run whose headline cells pass; unknown `--conditions` can run an unfaulted, mislabeled condition.
- **G-10 — Medium — `time-to-play:1306-1332`; supplied cycle `report.md`:** Game-to-game passes without a sync stamp/outcome, and exit passes without the card-disappearance measurement. The actual cycle has g2g stamp `-`, token `?`, yet PASS; it does not establish the advertised in-flight-sync outcome.
- **G-11 — Medium — `time-to-play:304-318,1193-1194,1315-1319`:** A known surface with an unreadable panel leaves `scaled=None` and passes; a g2g-only run need not have a readable surface at all. Surface qualification is performed only once, not for subsequent launches.
- **G-12 — Medium — `time-to-play:524-590,1184-1204`:** An already-running RetroArch plus changing nonblank frames can satisfy “first game frame” even if POST launches nothing. HTTP success, a new process/launch identity, and successful drawing/readiness waits are not required.
- **G-13 — Medium — `time-to-play:408-435,1045,1186,1211,1222`:** The workload remains NES `Probe.*` for a different `--rom` or the GB fallback. Quick launch/exit and g2g also both use jitter 0, allowing size-only WebDAV to skip rewritten same-sized payloads; moved bytes are not checked.
- **G-14 — Medium — `time-to-play:237-239,394-401,1047-1048,1343-1344,1390-1393`:** Startup reboots erase `/tmp/ttp-kill`, but it is not reinstalled. Later startup exits and conditions call the missing helper, ignore its failure, and can still finish green through G-09.
- **G-15 — Medium — `time-to-play:1039-1048,1063-1085,1121-1125`:** Guest mutation precedes cleanup protection; configuration-backup copies are unchecked, and monitor construction is outside `try/finally`. A missing monitor or early setup failure can leave modified guest state.
- **G-16 — Medium — `time-to-play:408-435,904-929,1088-1115`:** Restoration leaves seeded saves behind, does not remove a newly created configuration whose original was absent, and saves only one default route per family before deleting others. Restored settings are not reloaded into ES.
- **G-17 — Medium — `time-to-play:137-139,801-817,1407-1424`:** Fixed fixture ports are neither reserved nor ownership-checked. `Fixture.up()` can accept another listener after its own child failed to bind, and callers ignore a false return; “stall”, “portal” or “refused” need not be the injected condition.
- **G-18 — Low — `time-to-play:1295-1332`:** At the predicate-input level, replacing an otherwise valid headline value with a negative number or NaN passes presence checks and can evade the budget. The packet does **not** demonstrate a CLI path producing NaN.

### Third: `frame-diff` claims and baseline

Masks discard pixels; live claims exempt them from failure but report attribution. Claims match the baseline ID or `*`; their prose is not an expected-pixel assertion (`frame-diff:130-156,190-206,284-285`). Attribution happens **before clustering**, so adjacent claims do not accidentally cover their bounding-box gaps.

A baseline-known missing frame fails before claims are considered; size changes also fail regardless of claims/masks (`:298-325`). However, the expected frame inventory is only the union of files actually found, producing these additional holes:

- **G-19 — Medium — `frame-diff:244-261,287-300,344-353,395-410`:** A valid `BASELINE.txt` with no PNGs plus an empty/nonexistent run passes. `accept` also accepts any nonempty subset: frames omitted from both the accepted subset and later run disappear from coverage.
- **G-20 — Low — `vm-walks/claims.txt:77-89`; `frame-diff:130-151,284-285`:** “PROPOSAL ONLY” does not disable subsequent claim lines; they are live against the named baseline. Issue/reason text is not mandatory or validated. Whether those proposals were subsequently approved is not shown.
- **G-21 — Medium — `vm-walks/masks.txt:7-9`; `frame-diff:155-156,190-191`:** Transfer masks match every `run-transfer*/*` screen, including intermediate hub/picker screens. For example, a change at `(300,380)` in `run-transfer/01-cloud-hub.png` is invisible without any claim.
- **G-22 — Low — `frame-diff:286,327-344`:** With `--min-pixels 2`, one unclaimed changed pixel passes and can produce “Every walked screen is pixel-identical”. The tolerance is explicit, but that description and the unconditional strictness claim are false.
- **G-23 — Medium — `frame-diff:119-124`:** RGBA alpha is discarded. An alpha-only change that changes the rendered appearance compares identical without a claim or mask.
- **G-24 — Low — `frame-diff:75-95,119-127`:** PNG interlace, positive dimensions and complete decoded rows are not validated. For example, two accepted zero-dimension PNG-shaped inputs compare successfully without any pixels.
- **G-25 — Low — `vm-qa:464-466,525`; `frame-diff:287-300`:** A scoped `--walk` replay followed by `frame-diff` is compared against the entire baseline; correctly omitted, unselected walks become MISSING failures. There is no shared comparison-scope contract.

### Fourth: `vm-stop` waiting and ownership

The ordinary stop path is substantially sound: it checks the recorded PID’s argv and disk argument, holds a pidfd, rechecks start time/argv, sends SIGTERM, and polls for **that host process’s exit**, not guest shutdown readiness (`vm-stop:24-43`). The CLI bounds the default 20-second wait to `(0,60]` seconds (`:62-67`). Timeout raises before unlinking, returns 1, and does not escalate (`:42-53,68-73`). The supplied controls and reported 0.25-second stop support those cases, not all caller behavior.

- **G-26 — Medium — `vm-stop:27-39`; `vm-stop-test:29-33`:** “QEMU identity” is argv-based, not executable/file ownership. A Python process named `qemu-system-fixture` with the expected `-drive` argument is accepted—the controls deliberately demonstrate that construction.
- **G-27 — High — `vm-stop:15-17`; `vm-pair:136-137,157-158`:** Missing pidfiles count as successful stops, after which disks are deleted. A live unrecorded guest, or a third guest matching `vm-*.qcow2`, can have its disk unlinked while still running.
- **G-28 — Medium — `vm-stop:50-53`:** The final compare-and-unlink is not atomic. Another session replacing the pidfile between those operations can lose its new ownership record despite the identity recheck.
- **G-29 — Medium — `vm-pair:33,146-147,164-167`:** Partial launch/readiness failures have no rollback; `down` also stops processing after guest a’s failure. Guest a or both guests can remain live after a failed pair operation.
- **G-30 — Medium — `vm-qa:119-122,528-541`; `vm-upgrade-rehearsal:57,62,144,167-170`:** `vm-qa` never tears its pair down at completion. Rehearsal early failures bypass teardown, and its final stop failure does not change RESULT PASS or rc.
- **G-31 — Medium — `.claude/rules/generic-x64-vm-testing.md:115,202-207`:** The published boot recipe still uses raw `kill "$(cat pidfile)"`, contradicting its later exact-owner/wait rule; following that recipe bypasses both safeguards.

### Other new defects and gaps

- **G-32 — Medium — `vm-qa:115,123`; `vm-pair:113,170`; `emulator-exit-test:51,145`; `ra-offline-test:111,328`; `time-to-play:184-193`:** Attempt-count loops do not bound an established SSH command that stops answering. Several SCP/control-master operations also lack execution deadlines; `ConnectTimeout` is insufficient.
- **G-33 — Medium — `vm-visual-qa:226-239,272-280`; `vm-serial:44-51`:** Socket drains wait for silence, and screendump stabilization waits for unchanged size, without absolute deadlines. Continuous output/growth defeats their callers’ timeout promises; the walk runner’s separate 900-second wrapper only covers its own invocation.
- **G-34 — Medium — `vm-visual-qa:434-449,651-659`:** The stdlib PPM parser loops indefinitely on EOF inside an unfinished header token. Separately, an unsupported PPM can make single-shot mode print “captured …png” and exit 0 without producing that PNG.
- **G-35 — Medium — `vm-visual-qa:182-208`; `vm-walks/cloud-epic/vnc-grab.py:33-50`:** RFB coverage is summed rectangle area, not unique covered pixels; overlapping rectangles can conceal missing regions. The separate grabber additionally returns a partial zero-filled framebuffer when its deadline expires.
- **G-36 — Medium — `vm-serial:53-74,101-105,121-129`:** END receipt means success regardless of command status: `sh false` or an uploaded script exiting nonzero returns 0. A failing wait test that prints `READY` can also satisfy the substring-based readiness check.
- **G-37 — High — `vm-visual-qa:335-375,559-577`:** Missing pre/post frames count as 100% change, so `wait-for-change` succeeds precisely when it lacks the observation needed to prove a key landed. This is separate from F-08’s screenshot-warning path.
- **G-38 — Medium — `vm-visual-qa:350-367,374-375,559-560`:** Pre-key settling may expire and be ignored; subsequent unrelated animation can satisfy the key’s change test. Syntactic key/wait pairing is not a causal or intended-screen assertion.
- **G-39 — Medium — `vm-visual-qa:396-414,601-604`:** Starting dismissal on GO TO can produce GO TO → carousel → GO TO and stop on the repeated dialog while announcing “back on the carousel”. Exhausting the limit or unchanged-key retries likewise establishes no carousel identity.
- **G-40 — Medium — `vm-qa:85-90,438-445,446-511`:** An empty suite file, `--walk ,`, or failed `.steps` reads can yield an empty/truncated successful walk. The producer pipeline has no failure propagation or required walk/step/frame count.
- **G-41 — Low — `vm-visual-qa:250-269,524-530`:** Walk captures pass relative, unquoted paths to HMP. A different QEMU working directory or spaces in the output path can break capture, after which the walk continues through the warning path.
- **G-42 — Medium — `vm-qa:390-398`; `vm-walks/suite.txt:70-77`; `vm-walks/to-manage-cloud-storage.steps:7-11`:** One surviving `shared.sfc` prevents cloud reseeding on subsequent runs. The reset also does not establish the walk’s “not signed in” precondition, so reused guests can exercise different flows.
- **G-43 — High — `vm-qa:304-318,388-408`; `vm-walks/suite.txt:82,89-90`:** Any nonempty active remote is accepted as suitable. A borrowed guest retaining a non-QA connection can run destructive match/transfer walks against it; “a remote exists” is not ownership verification.
- **G-44 — Medium — `vm-qa:376-386`:** A missing fixture sentinel causes existing named ROMs/save states to be overwritten with random bytes, followed by broad mtime changes across saves/screenshots/ROM directories. No ownership or original-content restoration protects reused guest data.
- **G-45 — High — `ra-offline-test:110-117,146-157`; `time-to-play:1027,1124`; `es-launch-memory:123-130`:** SSH, serial and monitor channels are independently accepted without proving they belong to the same guest. Mismatched endpoints can measure one guest while typing into, disconnecting or capturing another.
- **G-46 — Medium — `signin-memory:105`; `emulator-exit-test:113`; `ra-offline-test:233`:** Guest cleanup uses shared pidfiles and name/pattern-wide kills. Other WebKit windows or RetroArch sessions on the same guest can be stopped; this is guest-side, not a host-QEMU pattern search.
- **G-47 — Medium — `signin-memory:85-108`; `es-launch-memory:76-79,93-95`:** Sign-in measurement ignores launch failure and can use stale shared logs/unrelated matching processes. Launch-memory selects the oldest name match, not a unique ES instance bound to its API, and checks PID without start time.
- **G-48 — Low — `es-launch-memory:118-162`:** Acceptance bounds only final-minus-baseline growth. Intermediate snapshots can exceed the supplied limits and later recover; this is not a peak-memory or per-cycle ceiling test.
- **G-49 — Medium — `emulator-exit-test:185,192-194`:** Part C explicitly deletes the marker before D asserts its absence. D cannot independently prove marker lifetime, and `--only D` supplies no launch stimulus.
- **G-50 — High — `ra-offline-test:94-96,241-243,259`; `qa-accounts:52,59-60`:** Account setup/cleanup does not receive the selected `--host` or identity; it uses localhost and `QA_KEY`/the default key. Isolated-key runs can fail, or a remote-target run can alter credentials on a different local guest.
- **G-51 — High — `ra-offline-test:231-264,524`:** Cleanup has no signal/EXIT trap and its failures do not increment `FAILS`; it can announce PASS/account-cleared after failed restoration. Remembering only “an account existed” also restores the QA account, not necessarily the account originally present.
- **G-52 — Medium — `ra-offline-test:69,84,163-165,199-221,512-516`:** Distinct guests still share the consumable QA account/achievement without a lock. Concurrent “unearned” observations can race an award or control run and invalidate attribution.
- **G-53 — Medium — `ra-offline-test:259-263,345-347`:** The shared host `/tmp/ra-offline-dismiss.steps` races creation/removal across sessions; the predictable account-log pathname is opened without exclusive creation. Neither is run-owned scratch.
- **G-54 — Medium — `ra-offline-test:269,392`:** Negative checks turn any nonzero SSH status—including transport failure—into proof of absence. A failed read can PASS “nothing listens” or “no synthetic award”.
- **G-55 — Medium — `ra-offline-test:203-205,479`:** An Achievements object missing the requested ID is reported as “unearned”, not unknown; separately, substring matching accepts `flushed=10` as `flushed=1`. These assertions do not validate the named datum exactly.
- **G-56 — Medium — `ra-offline-test:518-522`:** The control’s relaunch neither clears the previous log nor requires RetroArch to appear. A failed relaunch can reuse the old active-achievement count and PASS.
- **G-57 — Medium — `ra-offline-test:459-462,496-498,523`:** Reconnect screenshot failures are checked, but offline-exit background capture and online-exit capture failures are discarded. A frames-requested scenario can PASS with those evidence sets missing.
- **G-58 — Medium — `qa-accounts:107-115,155-158`:** Read-back verifies nonempty named fields, not equality to the requested credentials; RA enablement is announced without read-back. Failed writes leaving old nonempty values can be reported as successful provisioning.
- **G-59 — High — `device-act:38`; `signin-memory:103-115`; `ra-offline-test:136,377`; `vm-upgrade-rehearsal:78-82`:** Credential-bearing commands enter the action log; sign-in JSON prints full URLs/pages; `token = secret`/JSON-shaped values evade the RA filter; rehearsal sends credential-bearing configuration in SSH argv. These are exposed channels, not evidence that this cycle leaked a secret.
- **G-60 — High — `device-act:35-44`:** Failed BEGIN/END logging does not prevent the action or fail its result. A successful remote mutation can exit 0 and say “recorded” without the promised audit trail.
- **G-61 — Low — `device-act:10-14,39`:** The timeout supervises local SSH, not a verified remote process tree. A remote command surviving channel closure can continue after rc 124; the “command is killed” promise is too strong.
- **G-62 — Medium — `png-blackout:32,69-78`:** Empty/off-image rectangles succeed without redacting a pixel, and textual PNG metadata is retained. A successful “painted out” receipt is not sufficient evidence that an account identifier was removed.
- **G-63 — Medium — `es-untranslated:69-78,99-105,138-156`:** Unreadable source files are silently skipped, and only the upstream—not current—source must contain strings. A partial/unreadable current checkout can PASS with missing French checks.
- **G-64 — Medium — `es-untranslated:40-55,143-156`:** Fuzzy flags and translation contexts are ignored. A fuzzy or context-only nonempty translation can satisfy the check without supplying the ordinary `_()` translation used by the compiled catalogue.
- **G-65 — Medium — `es-syntax-check:89-101,133-147`:** Source substitution is not verified; quoted/response-file compiler commands can retain the cached source and report an edited file OK without compiling it. Failed header-farm operations are also unchecked.
- **G-66 — Medium — `vm-upgrade-rehearsal:65-75,95-97,154`:** Failed backup creation followed by counts `0 → 0` passes “backup archive kept”; replacement/corruption preserving the count also passes. The four seeded files are checked for hashes existing, not expected sizes, so truncated seeding can qualify.
- **G-67 — Medium — `raofflineproxy-consent-test:168-186,89-96,209-216`:** Collector validation can throw before recording an HTTP event. If a forbidden sender receives that failure and returns False, a declined case can appear to have sent zero requests despite having contacted the collector.
- **G-68 — Low — `ra-candidate-games:142-145`:** A bare-list hash response reaches `listing.get(...)` before the purported list fallback is usable and raises `AttributeError`.
- **G-69 — Low — `font-stems:113-115,172-175,203-223`:** Reversed size ranges or failed glyph loads can yield empty/partial measurements with rc 0. This is a measurement-quality gap, not a demonstrated acceptance PASS.
- **G-70 — Medium — `vm-qa:476-477`; `time-to-play:381-391`; `ra-offline-test:188-190`:** Reboot waits do not require a changed boot identity; an old/still-starting ES can satisfy them. This is distinct from merely failing to reject an exhausted wait.
- **G-71 — Low — `vm-qa:118-145,341-345,426-428,513`:** Report timing omits pair/backend startup and fixture work outside `run_suite`; selecting only host checks still requires the backend and guest. Report minutes are not complete job cost.
- **G-72 — Low — `.claude/rules/vm-first.md:59`; `vm-qa:63,529-532`; `time-to-play:1293-1302`:** Descriptions still say four suites and no timing budget, while the code has 17 suites and a failing three-second exit budget.

## 2. Refuting the first reader

### Findings F-01–F-20

- **F-01 — Agree, Medium; narrow the claim.** SKIP is not a suite PASS, and the observed run did prove four other suites. It is the zero exit that cannot mean “all requested checks passed.” A SKIP-sensitive final predicate would refute this; `vm-qa:148,528,541` and the cycle show the opposite.

- **F-02 — Agree, Low; narrow “nothing”.** Nonpositive repeats empty the repeated headlines, but default startup/conditions may still execute; valid non-headline-only selections also perform work. Validation of requested results would refute it; absent at `time-to-play:994-1021,1306-1332`. The supplied probe proves the headline-empty case.

- **F-03 — Agree, Low.** The supplied `--only X` output proves no assertions ran, not no effects: setup and cleanup still execute. Rejecting empty/unknown selections would refute it; `emulator-exit-test:44,91-116,149-196` contains no such guard.

- **F-04 — Agree, Medium for the production guard; narrow the class.** The optimize probe proves the manager failure. Other tools lose differing amounts of protection, not necessarily every assertion; native `unittest` checks remain (`raofflineproxy-installed-native-test:55-69`). Explicit checks or enforced nonoptimized invocation would refute the manager issue; `vm-qa:483` supplies neither.

- **F-05 — Agree with fall-through; disagree with unconditional PASS.** A valid unchanged framebuffer should eventually fail a tracked key; manager walks have another refusal (`vm-qa:477-499`; `vm-visual-qa:374-377,585-591`). A post-wait readiness failure would refute F-05, but is absent. Missing-frame/animation inputs are needed to establish the broader false-PASS case.

- **F-06 — Agree, Medium.** Setup failures are not connected reliably to the suite result (`vm-qa:341,389-408,426-428`). Checked propagation or asserted fixture read-back would refute it; neither is shown. A baseline comparison is not a universal substitute because claims/masks can exempt differences.

- **F-07 — Agree as a scope-reporting gap, Low.** Reduced checking is explicitly documented, not completely hidden (`vm-qa:198-212`). Mandatory ES citations or a partial-suite report would refute the gap; the packet shows neither. “Register PASS” is not necessarily false under the narrower documented contract.

- **F-08 — Agree, Medium.** A failed walk screendump only warns (`vm-visual-qa:530-532,606-611`). A required capture count/nonzero result would refute it. A baseline catches omission only when that particular frame is already expected (`frame-diff:287-300`), not merely whenever a baseline exists.

- **F-09 — Agree with the default-root risk, Medium; correct retention.** The raw image is temporary and removed after conversion (`vm-pair:137-145`). The tmpfs size/~6 GB figures are reported host observations, not independently reproducible here. Disk-backed private defaults would refute the default risk; overrides exist, but fixed SSH/VNC ports remain (`:63-64`).

- **F-10 — Agree conditionally on shared defaults, High; reject the cycle as proof of shared-state use.** `vm-qa:117-118,397-398` does not isolate the backend. However, `03` §3.5 says the cycle set private cloud state/port, and its report shows port 19010. Those overrides refute shared-default use for that run, not the unsafe default.

- **F-11 — Agree with the legacy default, Low; host absence is only reported.** `es-syntax-check:53-54` proves the path. The no-argument control stops at line 68, before checking the root at 69, so it does not prove root absence. An existing default directory would refute that host-specific assertion; only the summarized `ls` supports absence.

- **F-12 — Agree, Low.** `vm-qa:81` truncates the four named descriptions and the continuation of time-to-play’s description. Printing through the complete header would refute it; the literal range does not.

- **F-13 — Narrow to a documentation/index lead, Low.** The supplied owning rule supports the missing literal tool names, but the index itself is absent. Walk scripts already match its `tools/vm-walks/**` glob (`generic-x64-vm-testing.md:19`). Correct index entries would refute the index allegation; the packet cannot establish their absence independently.

- **F-14 — Narrow, not “nobody ever runs them”.** The claim is “the summarized search found no current operational caller.” Historical measurements/catches in `04` §Q5/Q6 already contradict the literal stronger wording. A current invocation would refute the narrowed claim; complete caller searches are not supplied.

- **F-15 — Narrow to the tested image and historical guard, Low.** The cycle proves the helper absent on one image; `migration-protocol.sh:9-12` safely refuses before writing. Another current image containing it would refute “every current image”; no inventory proves that universal claim. Historical replay value is not disproved.

- **F-16 — Narrow to no reported product catches.** “Exit: nothing at all” overstates its own table, which records a positive debounce control; the test also describes that construction (`emulator-exit-test:23-25`). A qualifying historical catch would refute the negative search result; the underlying work logs are absent.

- **F-17 — Agree with the reported concentration, not independently verified timings.** The supplied medians give `(16.7+13)/33 ≈ 90%`; the default pair launches before suites (`vm-qa:119-122`). Lazy guest-b startup/early shutdown would refute the holding-cost claim; neither appears. G-30/G-71 make the total cost larger than that account.

- **F-18 — Agree with the baseline IDs/three exemptions; narrow the conclusion, Low.** Whole-frame claims still cannot waive size changes or missing baseline-known frames (`claims.txt:38-40`; `frame-diff:298-325`). Old baselines can compare newer cuts without acceptance; `:284-315` has no run-build restriction. Narrowed claims/new baseline would remove the stated exemption; neither is shown.

- **F-19 — Agree with automatic retention, Low; quantity unverified.** `frame-diff:399-403` preserves the prior baseline. An external retirement policy would refute “nothing retires them” globally; none is supplied. Six baselines/~70 MB rests solely on the summarized `du`.

- **F-20 — Agree, Low.** Rehearsal hardcodes its output root (`vm-upgrade-rehearsal:30`); deriving it from the override would refute the finding. Note that `ra-offline-test:67` honors the override for ROM inputs, not an equivalent report-output directory.

### Q3: suite coverage and constructed inputs

- **No suite name is missing:** the table accounts for all 17 names in `vm-qa:63`, including grouped vocabulary/French/quoting/menumap rows. **Constructed inputs are missing:** unknown selection, masked startup failure, stale mDNS publication, wrong-guest fresh checks, empty current French sources, RA control relaunch failure, and zero-backup rehearsal (`vm-qa:74,121,257-291`; `es-untranslated:69-78`; `ra-offline-test:518-522`; `vm-upgrade-rehearsal:95-97,154`).

- **The strongest “none” claims are wrong:** a baseline does not prevent empty-inventory/alpha/tolerance passes (`frame-diff:119-124,287-344`), and time-to-play’s rule is not sound merely because a cell ran (`time-to-play:1295-1332`). The actual cycle’s missing g2g stamp supplies an observed coverage gap.

- **Do not invent an extra memory false PASS:** omitting launch-memory bounds is explicitly diagnostic and produces no `passed` field (`es-launch-memory:9,157-162`). Its rc 0 must not be sold as acceptance, but that documented distinction matters.

### Q5 and Q6: corrections versus unverifiable history

- **Q5’s “host only” footprint is misleading under its own “holds while running” definition:** the runner already holds the pair/backend during those suites (`vm-qa:118-122`). Their marginal workload is host-only; their run footprint is not.
- **Q5’s total needs a boundary:** startup and some fixture costs precede the measured/report interval (`vm-qa:118-145,341,426-428`); no automatic final teardown bounds lifetime.
- **Q5’s ra-offline “guest d” is not the runner default:** `--ra-offline` targets selected guest a unless changed (`vm-qa:57,105-110,358`). Standalone time-to-play also uses cloud/host fixtures, not just one guest (`time-to-play:1231-1245,1404-1424`).
- **Q5’s “nine suites under three seconds” disagrees with its displayed medians:** ten rows meet that condition. The historical median/max values themselves cannot be re-derived from the supplied outputs.
- **Q6’s historical catch rows are not independently falsified here.** But “no recorded catch” is not “no positive” or “no value”; its exit row demonstrates the distinction. “Standalone time-to-play: vm-qa only” also needs qualification: `vm-qa` invokes quick mode and separately documents manual full runs (`vm-qa:329-345`).
- **Q6 has an unresolved internal inconsistency:** `02` Coverage credits integration-test with #361, while `04` Q6 says no catch. The absent research/work logs are needed to decide whether that was a product catch, control or harness repair.

## 3. What I could not judge

- **Historical cost and value:** the 61 reports, deduplication, full-run medians/maxima, last product catches, positive controls and “no caller” searches are summaries in `02` §The record/P4 and `04` §Q5/Q6. I cannot independently verify their classifications or completeness.

- **External implementations and callers:** `cloud-test-backend`, `cloud-round-trip`, `last-good-scripts-test`, the wrapper/register/menu checkers, the launcher/profile and epic owner are not included in full. Their cited behavior remains contextual evidence, not a reviewed implementation. Likewise, the native adapter delegates legacy-CHD success to an external `exercise()` whose contract is absent (`raofflineproxy-installed-native-test:66-70`).

- **Visual correctness and claim approval:** the three fixture entries provide sizes/hashes, not pixels; baseline/run PNGs and `BASELINE.txt` are absent. I cannot verify geometry, intended screens, legitimacy of mask rectangles, review/approval of proposal claims, or whether the cycle’s measured “first frames” were actually game frames (`frame-diff:395-414`; `time-to-play:563-566`).

- **Full operational qualification:** the supplied cycle used `--skip-up`, executed four suites and skipped comparison. It did not exercise the default launch path, pair identity, walks, full timing conditions, upgrade rehearsal or real-award scenarios. Passing synthetic launch/stop/readiness controls establishes their enumerated cases, not complete lifecycle safety.

- **Artifact/image and hardware binding:** the image digest is reported from a sidecar, not independently recomputed here (`02` §The guest cycle). Neither this packet nor the VM cycle establishes handheld input, GPU, storage/power behavior, or actual visual acceptance; the supplied VM-first rule explicitly reserves such physical facts (`.claude/rules/vm-first.md:24-32,41-46`).