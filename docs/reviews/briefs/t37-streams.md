# T37 (#684): the stream brief for stage E

Written at the pause from the lane's punch list (the audit issue #1381; the punch-list post `kit/t37-stageD-punch.md`, comment 6552279533, 02:21 UTC 2026-11-01, and the PAUSE, comment 6552281930, 02:22; the record at `264a39f6d7`), drafted by an agent from T36's shape (`docs/reviews/briefs/t36-streams.md` at `9f24bccb50`, 497 lines by `wc -l`; T35's `docs/reviews/briefs/t35-streams.md` read for a second reading) and ruled by the coordinator at 02:39 UTC 2026-11-01 (the `RULING` lines, D-WORKFLOW-189). The rulings name no register row (Draft notes, item 14). The Backlog ruling 6 names is filed by the coordinator from `kit/t37-backlog-tools.md` (`#<Backlog>` below until it has a number); the rule errata ruling 8 names are `kit/t37-rule-errata.md`. The brief is `es-recipe.md` at `566398105e` (version 2 with its errata before dispatch); where this file and the brief differ, this file wins for stage E.

**The coordinator's, drafted at T37's stage-D pause, 02:39 UTC 2026-11-01.** Read from the lane's record at the distribution tip **`264a39f6d7`** on `feature/m6-es-recipe-684` (equal to `origin/feature/m6-es-recipe-684`, this draft's `git rev-parse`) by `git show` only, never the worktree: `05-punch-list.md` (19 items, 378 lines; the Phase 7 gate `:236-258`, every row `Open`; the `punch_index` `:260-378`), `04-analysis.md` (§ The questions `:76-131`, § Second opinion `:192-250` with G-1 to G-9 `:225-245`), `02-forward-audit.md` (542 lines: § Coverage `:14-47`, § The leads `:49-112`, § The recipe `:114-224`, § The dependencies `:226-250`, § The themes and `lowerdeck` `:252-279`, § The patches `:281-332`, § The currency `:334-386`, § The structure `:388-420`, § The runs `:422-449`, § The guest cycle `:451-479`, the empty § The streams `:481-484`, § Positives `:486-501`, § The #585 lines owed `:503-518`, § What the integration inherits `:520-542`), `03-retrospective.md`, `00-running-log.md` (103 lines), `tools/t37-checks.sh` (198), `tools/t37-failfirst.sh` (78), `stage-c/checks-at-tip.out`, `stage-c/failfirst.out`, `stage-c/stamps-at-tip.txt`, `stage-c/stamps-fixed-fixture.txt`, `stage-a/s5-runs.out`, `stage-b/reads.out`, `stage-b/l01-merges.out`, `guest-cycle/g03-configs.txt`. The tracker: #1381 (19 checkboxes), the bugs #1382, #1383 and #1384 (`gh issue view N --json title,body`), T37's lines on #613 (comment 6552262443) and #1072 (comment 6552262614), the coordinator's stage-C answer (6552218931) and pause read (6552305720). The slice brief at `566398105e` (§ 1 rulings (a) to (k), § 5 item 4, § 7's 21 checkboxes, § 8, § 9's same-commit rules, § 10's hand-back, stops and never-run list, the errata before dispatch). The ES recipe read through the mask with `:39` withheld by line number at `264a39f6d7` (its `ui/` bytes `2174265e9c`'s, `02:4-5`), upstream's at `651150fc88`; the pin's `CMakeLists.txt` by `git -C <Q> show 16dbac5211:CMakeLists.txt` *(pin read)*. The register at the coordinator worktree's `5d99939390`: the highest decided rows are D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-137 and D-WORKFLOW-217 (this draft's `awk` over the decided table's ID column), so a row a stream forces takes the next ID the coordinator assigns. **Nothing under `/workspace/tmp/m6-t34/held/` or `/workspace/tmp/m6-t36/held/` was opened for this draft;** no hold is met in this slice (PL-17 judged outside D-WORKFLOW-215's test by the lane, `00:93`, and so ruled at stage C, comment 6552218931).

**The worktree and what stage E changes.** `/workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684` on `feature/m6-es-recipe-684` at `264a39f6d7`; the lane's stage-E start is the tip the dispatch comment names (`264a39f6d7`, or the coordinator's merge over it). **There is no ES worktree and no ES change** (ruling (c)): `reviewed-at-es:` and `fixed-at-es:` read `none -- no ES change` to the hand-back, and a hash there is a stop (the errata before dispatch). Stage E changes **one product file, `projects/ROCKNIX/packages/ui/emulationstation/package.mk`, never its `:5` (`PKG_VERSION`) or `:6` (`PKG_GIT_CLONE_BRANCH`)**, and otherwise only the audit folder `docs/audits/2026_11_01-epic-m6-es-recipe/` (its `tools/`, `stage-d/` and `stage-e/` included) and the day's log.

**The standing rulings for this slice, applied here and not re-asked:** the brief's § 1 (a) to (k) and D-WORKFLOW-217 (T37 owns the 15 and nothing else). (b): never `:5` or `:6`, and a pin or theme bump is a finding, never a change. (d): `tools/pkgcheck <name>` by name, each after its `find packages projects -type f -path "*/<name>/package.mk"` positive, with the control `es-theme-no-such-package` beside it. (e): no fetch. (k): every sourced-recipe call runs in a scratch export, never in the worktree, and a `build.*` root in the worktree is a stop. The errata before dispatch: **a compile START written by this lane is a stop**, not a line to acknowledge. § 5 item 4: every fix is proven twice -- `fix-fixture` (the checker's assertion FAILing on the pre-fix text and PASSing on the fix's, both lines recorded) and `fix-image-pending` (what only the integration's image shows), never claimed proven by the lane.

## The rulings

Each ruling gives the items with their lines (`05`'s), what the lane proposed (the punch-list post's table, `kit/t37-stageD-punch.md:3-23`, and its proposed stream, `:29-39`), the options the record left, and what the streams carry. The `RULING` line is the coordinator's.

1. **PL-03, PL-04, PL-05, PL-07, PL-08: the five contained recipe edits** (`05:32-42`, `:44-54`, `:56-66`, `:80-90`, `:92-102`).
   - **The items:**
     - PL-03, #1382, Low: `PKG_NEED_UNPACK="busybox"` is a bare word, so busybox never moves the ES stamp (`emulationstation/package.mk:14`; `config/functions:1114`, `:1126`).
     - PL-04, #1383, Low: the `rm` of `resources/logo.png` (`:79`) runs before `:81` makes the directory and `:82` fills it.
     - PL-05, #1384, Low: upstream's ARMSX2 *vulkan driver* filter (`651150fc88:104-108`) was dropped by four merges (`stage-b/l01-merges.out:5-8`); the tip's vulkan step ends at `:125-128`. Lowered to Low at stage D (`kit/t37-stageD-punch.md:27`).
     - PL-07, Low: a missing French catalog installs silently (`:67-68`; the pin's `CMakeLists.txt:565-578`). No bug of its own; #1381's checkbox is its tracker (`05:88`).
     - PL-08, Low: `HFS_DEV_LOGIN` builds a scraper with no `USING:` line (`:42-44`; `scripts/get_env:14`; the pin's `CMakeLists.txt:328-330`). No bug of its own (`05:100`).
   - **The lane proposed:** *Resolve in stage E* for each (`kit/t37-stageD-punch.md:7-8`, `:9`, `:11-12`): PL-03 *"`PKG_NEED_UNPACK="$(get_pkg_directory busybox)"`"*, PL-04 *"the `rm` moved after `:82`"*, PL-05 *"upstream's five ARMSX2 lines restored after `:128`"*, PL-07 *"a `makeinstall_target` line that fails when the French `.mo` is missing"*, PL-08 *"`HFS_DEV_LOGIN` added to the loop at `:42-44` (names only)"*; and *"one stream, every edit in `projects/ROCKNIX/packages/ui/emulationstation/package.mk`, so only the ES recipe's stamp moves. Never `:5` or `:6`. Each edit is proven `fix-fixture` and named `fix-image-pending`"* (`:29`).
   - **Options:** resolve as contained edits -- rule 6 for PL-03 and PL-04, whose lines are upstream's (`c445081a59:11`, `651150fc88:11`; `c445081a59:52`, `651150fc88:53`); the fork-own recipe's own lines for PL-05, PL-07 and PL-08 (`02:63-66`) -- or record.
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** PL-03 (#1382), PL-04 (#1383), PL-05 (#1384), PL-07 and PL-08 are **Resolved in stage E** as contained edits to `projects/ROCKNIX/packages/ui/emulationstation/package.mk` only -- never lines 5 or 6 (`PKG_VERSION`, `PKG_GIT_CLONE_BRANCH`), never another of the 15 -- each proven `fix-fixture` by the checker's assertion (FAIL on the pre-fix fixture, PASS after) and labelled `fix-image-pending` (no image is built here; the integration's build proves the image half). PL-07's guard is a `makeinstall_target` line that fails when the French `.mo` is missing (a new FAIL-first checker assertion); PL-08 adds `HFS_DEV_LOGIN` to the `USING:` loop at `:42-44`, names only, proven by the sandboxed sourcing count (3 before, 4 after, placeholder names assembled at run time).
   - **What the streams carry:** S1, its five edits in § The order. PL-03 and PL-04 are proven by the checker's existing assertions (`checks-at-tip.out:48-50`); PL-05, PL-07 and PL-08 by assertions S1 adds to `tools/t37-checks.sh`, each seen to FAIL on the pre-fix export before its edit is committed. "Placeholder names" is read as placeholder **values** for the four names, assembled at run time (the brief's § 9: *"a credential-shaped value (L-05's placeholders) assembled at run time, never a literal"*).
2. **PL-01 (L-03, #613): the `es_systems.cfg` fallback link** (`05:8-18`; `02:61`).
   - **The lane proposed:** *"Resolve in stage E (a contained recipe edit at `:101`, if #613 is routed here); else Defer to #613"* (`kit/t37-stageD-punch.md:5`).
   - **Options:** route #613's fix into S1; or leave it with #613's owner.
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** PL-01 is **Deferred to #613**, which is the M7 lane's (`M7.P5: Fix EmulationStation fallback systems-config symlink`, open; the candidate image already carries M7's correction at `G-03`): T37 makes no edit at `:101`; its line on #613 (comment 6552262443) is the record; a second fix of one line in two lanes would collide at the integration.
   - **What the streams carry:** nothing in S1. S0 records the deferral. The checker's `FAIL step 5 no-link-to-${INSTALL}-target (L-03): at emulationstation/package.mk:101` (`checks-at-tip.out:47`) **stays FAIL at the hand-back by design**; it flips when #613's fix reaches this recipe. G-03 is the candidate's resolving link (`g03-configs.txt:13-14`: `link=/usr/config/emulationstation/es_systems.cfg`, `resolves rc=0`).
3. **PL-02 (L-02, #1072): `emulationstation/patches/x86_64/` reached on no device** (`05:20-30`; `02:60`, `:323-326`).
   - **The lane proposed:** *"Defer to #1072 (T40 corrects the patch's GPU call first; then T37's `PKG_PATCH_DIRS+=` line or T40's rename)"* (`kit/t37-stageD-punch.md:6`).
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** PL-02 is **Deferred to #1072** (T40 corrects the patch's GPU call first; then `PKG_PATCH_DIRS+=` or the rename -- the `+=` and the four `get_available_cpu_governors` calls recorded from the seat's G-1/G-2); T37's line on #1072 (comment 6552262614) is the record.
   - **What the streams carry:** nothing in S1; no `PKG_PATCH_DIRS` line. The checker's `FAIL step 4 patch-dir-reached patches/x86_64/ (emulationstation): reached for 0 of the listed devices` (`checks-at-tip.out:43`) **stays FAIL at the hand-back by design.** The seat's G-1 and G-2 are `04:225-231`; #1072's comment carries the `+=` form and the count (*"call `get_available_cpu_governors` 4 times and `get_available_gpu_governors` 0 times"*).
4. **PL-06 (L-09): fribidi** (`05:68-78`; `02:67`, `:234-242`; D-WORKFLOW-216).
   - **The lane proposed:** *"Resolve in stage E: `fribidi` declared in `:13` (the seat's choice; the probe stays optional), the configure-log proof inherited by the integration"* (`kit/t37-stageD-punch.md:10`).
   - **Options:** declare `fribidi` in `:13`; record the build-order chain as the recipe's; or drop the optional probe (an ES change, outside the 15).
   - **The three reads** (this draft's, `git show <hash>:projects/ROCKNIX/packages/ui/emulationstation/package.mk | /usr/bin/grep -n '^PKG_DEPENDS_TARGET='`, then `/usr/bin/grep -c fribidi` on the same file):
     - `c445081a59:10`: `PKG_DEPENDS_TARGET="boost toolchain SDL2 freetype curl freeimage bash rapidjson SDL2_mixer fping p7zip alsa vlc drm_tool poppler pugixml noto-sans-cjk ${OPENGLES}"`; `fribidi` `0`.
     - `2174265e9c:13`: the same with `zstd` before `${OPENGLES}`; `fribidi` `0`.
     - `651150fc88:10`: as at `c445081a59`; `fribidi` `0`.
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** PL-06 (fribidi) is **Deferred, not Resolved:** upstream's recipe declares no `fribidi` at the base `c445081a59`, at the P1 tip or at `upstream/next` `651150fc88` (`PKG_DEPENDS_TARGET` read at all three), so declaring it is a fork-only design change, not a currency fix; the candidate's `libfribidi NOT linked` against the pin's link-when-found stays the integration's configure-log question, and the choice (declare `fribidi`, or drop the optional probe) goes to the Backlog the coordinator files (ruling 6). Record in `02` with the three reads.
   - **What the streams carry:** S0 writes the three reads into `02` § The streams' *Recorded, no stream* list and points `02` § What the integration inherits item 4 (`02:531-532`) at `#<Backlog>`. No edit at `:13`. The pin's lines stand as read: the optional probe `CMakeLists.txt:230-244` (*"It is optional on purpose ... this must never be REQUIRED"*, `:230-233`), the link `:462` *(pin read)*; T36's G-01 `libfribidi` NOT linked (`02:468`).
5. **PL-09, PL-11, PL-12, PL-13, PL-16, PL-17, PL-18, PL-19: the eight records** (`05:104-114`, `:128-162`, `:188-234`).
   - **The lane proposed** (`kit/t37-stageD-punch.md:13`, `:15-17`, `:20-23`): PL-09 *"Record: kept with its reason, a #585 line"*; PL-11 *"Record: as written, a #585 line"*; PL-12 *"Record: as written (a best-effort cache with a fallback)"*; PL-13 *"Record: the dated currency finding; the bump at the integration"*; PL-16 *"Record: the tool note (`02` § What the integration inherits item 9)"*; PL-17 *"Record under D-INFRA-006 (a mask on the verbose path is a Backlog candidate for the coordinator)"*; PL-18 *"Record: as written (upstream's legacy alias)"*; PL-19 *"Record: for upstream, a #585 line"*.
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** PL-09, PL-11, PL-12, PL-13, PL-16, PL-17, PL-18, PL-19 are **Recorded** as the lane proposed (PL-09, PL-11 and PL-19 with their `#585` lines; PL-13's bump is the integration's under D-WORKFLOW-024; PL-17 under D-INFRA-006).
   - **What the streams carry:** S0. `02:511-512` (L-06, PL-11's) and `:516-518` (PL-029, PL-09's) already hold two of the three `#585` lines; **PL-19's is new**, written by S0. No stream edits `sources/start_es.sh`, `system.d/emustation.service`, `sources/serial_number_check`, `autostart/001-emulationstation` or `:54` (ruling 1's *"never another of the 15"*). In the Phase 7 gate a record is written `**Deferred**` with its reason and an issue number (§ The record): the lint accepts only Resolved, Deferred and Withdrawn (`tools/lint-audit-artifacts:392-400` at `5d99939390`), as T35's gate did (`d828355e0a`, PL-13, PL-14, PL-18).
6. **PL-10, PL-16's tool half, PL-17's mask, and PL-06's choice: one Backlog** (`05:116-126`, `:188-198`, `:200-210`, `:68-78`).
   - **The lane proposed:** PL-10 *"Defer to Backlog #1385 (filed by the coordinator at 02:52 UTC 2026-11-01)"* (`kit/t37-stageD-punch.md:14`); PL-17's mask *"a Backlog candidate for the coordinator"* (`:21`); the PAUSE's question 4, *"whether the three recipes join `EXTRA_PACKAGES`. Proposed: a Backlog you file, naming the three fail-opens (L-21)"* (comment 6552281930).
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** PL-10, PL-16's tool half and PL-17's mask are **one Backlog the coordinator files** from `kit/t37-backlog-tools.md`: title `Backlog: the recipe checks that pass over nothing or cannot run -- pkgcheck's rc 0 on a missing name, fork-package-freshness's missing-ref fail-open and its ui/ blind spot, pixelelated-state-check --payload's mcopy dependency, the verbose build's credential defines`, one section per item quoting `05`/`04`'s words with file:line, acceptance criteria an agent can tick, the "Can this be done on the VM?" line (yes: host tool runs), no label; a fifth section carries PL-06's fribidi choice (declare or drop the probe; the three `PKG_DEPENDS_TARGET` reads quoted).
   - **What the streams carry:** S0 names `#<Backlog>` in `02` § The streams, `02` § What the integration inherits items 4 and 9, and `05`'s item table for PL-06, PL-10, PL-16 and PL-17. No stream edits `tools/pkgcheck`, `tools/fork-package-freshness`, `tools/pixelelated-state-check` or `config/functions` (T6's; the brief's § 10).
7. **PL-14: the distribution merge's six and two** (`05:164-174`; `02:334-386`).
   - **The lane proposed:** *"Defer to the distribution merge (`release-candidates.md` step 0) and #791"* (`kit/t37-stageD-punch.md:18`).
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** PL-14 is **Deferred to the distribution merge** (`release-candidates.md` step 0) and #791.
   - **What the streams carry:** S0's record. PL-05's restoration in S1 is the one hunk of `02:370-374`'s *"both moved"* recipe that S1 takes; S1's record names `git diff --shortstat 651150fc88 <fixed-at> -- projects/ROCKNIX/packages/ui/emulationstation/package.mk` beside the generated currency row (`02:347`, `+14 -34`), which stays the reviewed tip's.
8. **PL-15 (L-17, L-18): two rules describe the recipe as it is not** (`05:176-186`; `02:77-78`, `:393-397`; `04:182-185`).
   - **The lane proposed:** *"Defer to the coordinator's doc sweep"* (`kit/t37-stageD-punch.md:19`).
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** PL-15 is **the coordinator's sweep**: `kit/t37-rule-errata.md` carries, for each of the two rules `02`/`05` name, the rule file and line at `566398105e`, the sentence as it stands, the replacement the record supports (`02`'s words with their line) and the command that shows the recipe as it is; no stream.
   - **What the streams carry:** nothing. The two are `device-builds.md` § Iterating on EmulationStation (L-17) and `CLAUDE.md`'s per-device patch sentence (L-18); `02` § The structure (`:393-397`) records both as *the coordinator's, at acceptance*. The never-run list keeps both sentences (`device-builds.md:636-645`, `CLAUDE.md:143` at `566398105e`).
9. **The streams: S0, record only, then S1, the five edits.**
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** **one fix stream, S1, after a record-only S0:** S0 writes the `#585` lines, the records of ruling 5, the Backlog pointer and the three deferrals into `02` § The streams and its *Recorded, no stream* list, no stream; S1 carries the five edits in § The order (PL-03, PL-04, PL-05, PL-07, PL-08), each its own commit on the distribution branch in the recipe's convention (`emulationstation: ...`), each followed by `tools/pkgcheck emulationstation` after its `find` positive, the checker and the stamp compare, `bash -n` on the changed shell file, the non-ASCII grep over added lines, and the `Already written:` answer.
   - **What the streams carry:** the commit shape the rules ask, read at `566398105e`: `CLAUDE.md:145-150` (*"No Conventional Commits. Scope by package or device, matching history: ... `emulationstation: bump package`"*), `fork-workflow.md:90-94` (the upstream PR's `package: text` title, at most 72 characters, which the series cuts by content from these commits), the brief's § 9 (*"a recipe fix in the package's convention (`emulationstation: ...`), `Refs #684, #<bug>`; no closing keyword"*), and the recipe's history (`59a3a321d1 emulationstation: pin actionable cloud path refusals (#524)`, this draft's `git log`). So each recipe commit's subject is `emulationstation: <what>` within 72 characters, and its body carries the lines and `Refs #684, #<bug>` (#1381 for PL-07 and PL-08). "The three deferrals" are read as PL-01 (#613), PL-02 (#1072) and PL-14 (the merge, #791); PL-06 and PL-10 are deferred under the Backlog pointer (Draft notes, item 2).
10. **The hand-back.**
    - **RULING (coordinator, 02:52 UTC 2026-11-01):** the hand-back names the one distribution tip, every edit's checker line before and after, the stamp compare, `tools/pkgcheck`'s rc with its positive, the `#585` lines, the Backlog candidates, and the `fixed-at:` / `fixed-at-es: none -- no ES change` header values; S8-style guest halves do not exist here (the image proof is the integration's).
    - **What the streams carry:** § The hand-back.

11. **The lint's outcomes.** The lint accepts Resolved, Deferred and Withdrawn only.
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** the eight records of ruling 5 go in `05`'s gate as `**Deferred** | recorded ...`, as T35's gate wrote them; `02` says *recorded* in words.
12. **The FAIL-first fixture.**
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** the fixture carries PL-01's and PL-02's fixes as fixture-only lines so its exit-0 run holds, and its header says they are not T37's fixes (deferred to #613 and #1072).
13. **PL-08's proof form.**
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** the sandboxed count runs an extract of `:42-52`, never `:39` or `:40`, with placeholder names assembled at run time; counts only are printed.
14. **PL-03's stamp pair.**
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** the busybox stamp compare's FAIL before the fix is the expected result and `02` records it as `expected FAIL (the stamp did not move)`; the acceptance reads the word and does not count it as a failure.
15. **`stage-d/`.**
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** S0 writes the `stage-d/` folder § 7 checkbox 1 expects (the audit issue's and bugs' records, the pause post), before S1.
16. **PL-07 and PL-08 have no bug of their own.**
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** they stay punch items Resolved under #1381 (Low hardenings: a guard and a log line); no new bug is filed for them.
17. **The `#585` lines.**
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** PL-04's `rm` order, PL-07's catalog copy and PL-08's `USING:` loop are upstream's too: S0 writes a `#585` line for each beside PL-09's, PL-11's and PL-19's.
18. **PL-05's hidden row and the menu map.**
   - **RULING (coordinator, 02:52 UTC 2026-11-01):** restoring upstream's ARMSX2 filter hides a per-emulator feature row on devices outside the five; that row is the catalog's (`es_features.cfg`), not a menu row, so D-UI-039's menu map is unchanged; `02` records the reason and the label stays `fix-image-pending` (GENERIC_X64 ships no ARMSX2, so no VM frame exists; the integration's device build is the proof).
19. **Readings confirmed.** Ruling 4's fork recipe at the P1 tip is the fork's (the conclusion stands: `fribidi` 0 at all three reads); ruling 9's three deferrals are PL-01, PL-02 and PL-14; PL-13's D-WORKFLOW-024 reach is recorded as the draft notes it.

## The rules every stream keeps

- **Test first, then the fix; the test's FAIL is recorded before the fix lands** (`engineering-practices.md` § Guards must fail closed; the brief's § 5 item 4).
  - **Where the positive lives:** `tools/t37-checks.sh` under the audit folder's `tools/` (198 lines at `264a39f6d7`; its usage `:3-4`; its refusals, exit 2, `:20-28`: a tree holding a `.git` `:24`, an `--out` outside `/workspace/tmp` `:28`). Its steps: (1) the inventory `:38-44`; (2) `bash -n` on the seven `:46-52`; (3) `find` and `tools/pkgcheck` by name with the control `:54-63`; (4) the sourced-recipe assertions per device in the tree under `env -i` `:65-107`; (5) the install-text assertions `:109-160`; (6) the text checks `:162-181`; (7) the stamps and `--compare` `:183-196`; `TOTAL:` `:197`.
  - **The command:** `bash docs/audits/2026_11_01-epic-m6-es-recipe/tools/t37-checks.sh --tree <export> --repo /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 --commit <hash> --expect-es-pin 16dbac5211eea7e70db7394372033be2be7df829 --devices "GENERIC_X64:x86_64 H700:aarch64" --out /workspace/tmp/m6-t37/e/<run> [--compare <stamps.txt>]`, then `rc=$?` on its own line. The two devices are the stage-C runs' (`t37-failfirst.sh:11`).
  - **The lines at the tip, quoted, never summed in the head.** `TOTAL: 55 of 60 assertions` (`stage-c/checks-at-tip.out:66`), with five FAIL lines: `FAIL step 4 patch-dir-reached patches/x86_64/ (emulationstation): reached for 0 of the listed devices` (`:43`, L-02), `FAIL step 5 no-link-to-${INSTALL}-target (L-03): at emulationstation/package.mk:101` (`:47`), `FAIL step 5 no-rm-before-its-directory-is-filled (L-04): at emulationstation/package.mk:79 makeinstall_target (filled at :81)` (`:48`), `FAIL step 5 GENERIC_X64 PKG_NEED_UNPACK-words-are-directories (L-19): unresolved: busybox` and the H700 twin (`:49-50`); two WARNs, `or-true (L-07)` (`:51`) and `french-catalog-not-asserted (L-08)` (`:52`).
  - **After S1, by design:** L-04's and L-19's three FAIL lines are PASS; S1's new assertions PASS; **L-02's and L-03's stay FAIL** (rulings 2 and 3). The checker exits 1 at the hand-back with exactly those two FAIL lines, and its `TOTAL:` line is quoted as it prints. Any third FAIL line is a stop, posted on #684.
  - **Where each run goes:** `stage-e/s1-PL-nn-before.txt` (the pre-fix export), `stage-e/s1-PL-nn-after.txt` (the fix's export, with `--compare`), `stage-e/s1-PL-nn-checks.txt` (pkgcheck, `bash -n`, the grep lines, the `:39` hash pair, the diff stat), under the audit folder.
  - **Every new assertion against the unfixed text first** (T21's S11, `engineering-practices.md`): a FAIL is evidence of the defect only when the assertion reproduces the tip everywhere else, so each new assertion's before run is read in full -- every line other than its own matches `checks-at-tip.out` -- before the fix is written.
- **The scratch exports (ruling (k)).** Every sourced-recipe call runs in an export, never in the worktree.
  - **The pre-fix tree for S0 and PL-03** is the stage-A export `/workspace/tmp/m6-t37/export/` (`9fa740a91b`'s bytes, `00:33`), kept for stage E's fixtures by the PAUSE (6552281930), provided `git diff --stat 9fa740a91b <S0 commit> -- projects/ROCKNIX/packages/ui scripts config tools/pkgcheck .githooks/secret-patterns tools/forbidden-terms-check` prints no line; otherwise a fresh export of the S0 commit.
  - **Each later commit:** `( set -o pipefail; git -C <worktree> archive <hash> | tar -x -C /workspace/tmp/m6-t37/e/<short-hash>/ )`, its `rc=$?` on its own line. An export was about 2.2 GB at stage C (`00:85`: the fixed fixture `2,213,126,323` bytes), so `df -h /workspace` and `df -i /workspace` before each, at most two exports alive (the edit's parent and the edit), and each retired by `rm -rf "${E:?}"/<short-hash>` (with `E=/workspace/tmp/m6-t37/e`) in its own short command once the next edit's compare has read its `stamps.txt`. Each retirement goes in `00` with path and size (D-INFRA-022).
  - `ls -d build.*` in the worktree prints `0` after every edit and every run; a root there is a stop.
- **The stamp compare** (the brief's § 5 item 4: each fix moving exactly its own package's stamp). Run the checker with `--commit <the edit's parent>` and `--tree <the edit's export>` and `--compare <the parent export's stamps.txt>`, so `touched` is computed against the parent. The expected six step-7 lines are those of the stage-C fixture (`stage-c/failfirst.out:6-11`): `emulationstation` `moved=1 touched=1`, `es-theme-art-book-next` and `lowerdeck` `moved=0 touched=0`, on both devices.
- **The FAIL-first script follows the checker** (D-WORKFLOW-211: a fixture that relied on the defect is completed, its setup line named, no assertion changed).
  - `tools/t37-failfirst.sh` builds its fixed fixture from `2174265e9c` with the four stage-C fixes (`:17-32`). With S1's new assertions in the checker that fixture FAILs on them, and with PL-04 ruled a move, its dropped `rm` (`:28-30`) is no longer the stream's shape.
  - So S1's last record commit changes the fixture to stage E's five edits as S1 made them, plus the two deferred items' lines as **fixture-only** lines (PL-01's device link `:25-27`, PL-02's line in the `+=` form) so the fixed fixture still reaches exit 0. It adds one mutation per new assertion: the ARMSX2 block removed, the catalog guard removed, `HFS_DEV_LOGIN` removed from the loop.
  - The script is run once, after PL-08, and its `SUMMARY:` line is quoted. At stage C it printed `SUMMARY: tip exit 1; fixed fixture exit 0 then 0; 15 of 15 mutations caught; refusal exit 2` (`stage-c/failfirst.out:29`).
- **D-WORKFLOW-210's read.** A fork-only suite that asserts a shape S1 changes changes in the same commit. This draft's `git grep -n -E 'resources/logo\.png|vulkan driver|PKG_NEED_UNPACK|emulationstation2\.mo|HFS_DEV_LOGIN|USING: ' 2174265e9c -- tools .githooks .github` printed `tools/pkgcheck:47` and `tools/pkginfo:19` (field-name lists), two archived session files and one unrelated `tools/last-good-scripts-test:13821` match: no suite asserts the old shapes. The lane re-runs it at its tip and records the line.
- **The mask, and `:39`.** Every read of the recipe goes through the mask with `:39` withheld by line number (`W39`, the coordinator's answer 3 of 6551707733; `02:7-9`). **The five edits leave `:39` at `:39`:** PL-03 replaces one line at `:14`, and the rest lie below `:39`. The lane compares the output of `sed -n 39p <recipe> | sha256sum` before the edit with the same command's output after it, and prints only `equal` or `differs`, never the line or its hash in a record. A diff of the recipe is counted (`grep -c`), never printed, because it carries `:39` and `:40`.
- **Credentials by name only.** The four names are `SCREENSCRAPER_DEV_LOGIN`, `GAMESDB_APIKEY`, `CHEEVOS_DEV_LOGIN` and `HFS_DEV_LOGIN` (`scripts/get_env:14`'s `KEEP`).
  - A value for any of them in a fixture is a placeholder assembled at run time (`printf`), never a literal; `.githooks/pre-commit` refuses the literal (the brief's § 9).
  - After sourcing a recipe only named fields are printed, never `set` or `env`.
  - The hooks' patterns (`( . .githooks/secret-patterns; grep -c -E -e "$SECRET_PATTERNS" <file> )` after the compile check and a positive assembled at run time, the checker's own form `t37-checks.sh:169-174`) count `0` over every `stage-e/` file before each record commit.
- **The text checks over added lines.**
  - Non-ASCII: `git -C <worktree> diff -U0 <parent> <commit> -- <recipe> | /usr/bin/grep '^+' | /usr/bin/grep -v '^+++' | LC_ALL=C /usr/bin/grep -c -P '[^\x00-\x7F]'` prints `0`.
  - The hooks' secret pattern over the same `+` lines prints `0`; `tools/forbidden-terms-check --stdin` over them `rc=0`.
  - The recipe holds no player string, and a build-log message is ASCII.
- **Never `:5` or `:6`.** After each edit, `git -C <worktree> diff -U0 <parent> <commit> -- <recipe> | /usr/bin/grep -c -E '^[-+]PKG_(VERSION|GIT_CLONE_BRANCH)='` prints `0`, and at the hand-back the same over `git log -p <stage-E start>..<tip>` (§ 7 checkbox 5).
- **One path per recipe commit.** `git show --stat --format= <commit>` names `projects/ROCKNIX/packages/ui/emulationstation/package.mk` and nothing else. Its record is a separate `docs:` commit carrying the checker change, the `stage-e/` files, `02`'s row and the log. `tools/register-check` runs before each record commit; `tools/ceremony-check --gate` before each push (never `--no-verify`).
- **Nothing changes outside the one recipe and the audit folder.** Not the other 14 of the 15. Not `:101` (#613's), `:13` (PL-06's Backlog), or a `PKG_PATCH_DIRS` line (#1072's). Not the four patches (T40's, T42's), `virtual/image/package.mk` (T8's), ES's `CMakeLists.txt` or `es-core/CMakeLists.txt`, `scripts/`, `config/`, `tools/` outside the audit folder, any `.claude/rules/` file, `CLAUDE.md`, `AGENTS.md`, `docs/es-menu-map.md`, or the French catalog (ruling (i)). A fix that wants any of them is a question on #684 first.
- **No guest, no build, no compiler, no fetch, no keyed call, nothing on a unit.**
  - The host file `/workspace/tmp/m7-m6-host-coordination.txt` is read, never written: stage E asks no window and holds none, and **a compile START by this lane is a stop**.
  - **Every image half is `fix-image-pending`**, the integration's, on the first image built from the fixed recipe. GENERIC_X64 halves are read on its guest; a device-only half (PL-05's, outside the five) is read from that image's `SYSTEM` on the host (#1384's criterion 2).
- **A visible change keeps its flow and evidence together** (`es-ui-style-guide.md` § Keep the flow and its visual evidence together).
  - PL-05 removes a row (the *vulkan driver* feature of `armsx2-sa`, `es_features.cfg:1392-1395`) on every image built for a device outside the five. GENERIC_X64 ships no `armsx2-sa` (#1384: *"so no guest row reads the launcher"*), so no frame of it can be taken on the VM, and `docs/es-menu-map.md` is outside the lane (the brief's § 10).
  - S1's record names the flow step and says `CANNOT -- no guest carries armsx2-sa`. The map question is the coordinator's (Draft notes, item 7). The other four edits change no screen; their records say so.
- **A question for the coordinator is posted on #684**, never only on the session's screen. A turn ends on a post or a commit. If the harness refuses an edit's content, post the edit's PL number and stop that edit; the coordinator takes it (D-WORKFLOW-212). **The checkpoints are posted on #684 one line each, as each lands:** S0, then each of S1's five, with the commit, the before line and the after line.
- **Time to play.** Each edit's record says in one clause what it does to the two numbers and to boot to interface. Boot to interface is G-04's line: `essway.service` at 5.37 s, ES logging at 5.82 s, on the candidate guest (`02:471`, `:476-479`). None of the five is on the launch path or the boot path: PL-03, PL-07 and PL-08 are build-time lines; PL-04 makes `SYSTEM` 283,835 bytes smaller (#1383); PL-05 removes one feature from the catalogue ES reads, on images built for devices outside the five. All are priced on the integration's image, never here.
- **`Already written:`** per edit (D-WORKFLOW-050; the brief's § 5 item 4): what an image built from the old recipe left -- on the read-only system, replaced by the next image, or in `/storage`, which the next image does not replace. A bug's own line is quoted; an edit with no bug argues its line.

## S0 -- the records, the deferrals and the baseline (the audit folder only; rulings 2 to 9)

- **Files:** none under `projects/`. In the audit folder: `02-forward-audit.md` (§ The streams, § The #585 lines owed, § What the integration inherits), `00-running-log.md` (stage E's entries), `stage-d/` (below), `stage-e/s0-baseline.txt`, `stage-e/s0-stamps.txt`.
- **`02` § The streams** (`:481-484`): the lane's two lines are replaced by a pointer to this brief, the S0 row and a `### Recorded, no stream` list:
  - **The deferrals:**
    - PL-01 to #613 (ruling 2; T37's line, comment 6552262443; the checker's L-03 FAIL kept as its guard);
    - PL-02 to #1072 (ruling 3; comment 6552262614; the checker's L-02 FAIL kept; G-1 and G-2 recorded, `04:225-231`);
    - PL-14 to the distribution merge and #791 (ruling 7).
  - **PL-06** Deferred to `#<Backlog>` (ruling 4), with the three `PKG_DEPENDS_TARGET` reads at `c445081a59:10`, `2174265e9c:13` and `651150fc88:10`, each line quoted with its `fribidi` count `0`, and the sentence *"declaring it is a fork-only design change, not a currency fix"*.
  - **PL-10** Deferred to `#<Backlog>` (ruling 6).
  - **The eight records of ruling 5,** each with `05`'s reason:
    - PL-09 (`05:111`), with its #585 line;
    - PL-11 (`05:135`), with its #585 line;
    - PL-12 (`05:147`);
    - PL-13 (`05:159`; the bump the integration's under D-WORKFLOW-024, a new `PKG_SHA256` needing a fetch);
    - PL-16 (`05:195`; its tool half `#<Backlog>`);
    - PL-17 (`05:207`; D-INFRA-006; its mask `#<Backlog>`);
    - PL-18 (`05:219`);
    - PL-19 (`05:231`), with its #585 line.
  - **PL-15:** the coordinator's sweep (ruling 8; `kit/t37-rule-errata.md`).
- **`02` § The #585 lines owed** (`:503-518`):
  - **PL-19's line is added**, in the lane's shape: ROCKNIX, `projects/ROCKNIX/packages/ui/emulationstation/sources/serial_number_check:8-24`. *"When the path is set and the read is empty, a stored serial differs from `""`, so the empty value is stored and the warning raised"* (`05:230`). The contained guard (an empty read skips the check) is named; the item is recorded under D-UI-079.
  - **Kept:** L-06's and PL-029's lines (PL-11's and PL-09's).
  - **L-03's line** (`:508-510`) is marked *carried on #613* (PL-01 deferred; the same words are on #613's comment).
  - **L-19's line** stays, and S1's PL-03 record adds its fix commit.
  - The stage-B sentence *"proposed pending the checker's FAIL at stage C"* (`:506`) becomes the stage-E state.
- **`02` § What the integration inherits:**
  - item 4 (`:531-532`) names `#<Backlog>` for fribidi's choice;
  - item 8 (`:538-539`) names S1's five edits as `fix-image-pending`, with each one's image read (§ S1);
  - item 9 (`:540-542`) names `#<Backlog>` for the state check's `mcopy` route;
  - one item is added: PL-17's mask (`#<Backlog>`), and PL-13's `lowerdeck` bump at the integration.
- **`stage-d/`.** The folder has none at `264a39f6d7` (`git ls-tree --name-only 264a39f6d7 docs/audits/2026_11_01-epic-m6-es-recipe/`), while § 7 checkbox 1 lists `stage-a/` to `stage-e/` and the acceptance script's `FOLDER_ENTRIES` names `stage-d` (`kit/t37-accept.sh:70`). S0 writes `stage-d/` with the stage-D reads `00:99` names and the filing receipts `00:100-103` name: the issues' numbers and REST id, each `tools/box-check --issue N` line, and the pre-issue lint lines.
- **The baseline:** the checker over the S0 tree (the stage-A export, or a fresh one; § The rules) with `--commit <S0 commit>` and no `--compare`, into `stage-e/s0-baseline.txt`. Expect `TOTAL: 55 of 60 assertions` and the five FAIL lines of `checks-at-tip.out:43-50`, and its `stamps.txt` equal to `stage-c/stamps-at-tip.txt`'s six lines (`9e618e4a...`, `e31c625d...`, `7dd9f957...` on each device), copied to `stage-e/s0-stamps.txt`. A difference is a stop: S0 changes nothing the checker reads.
- **`00`:** stage E's start (the dispatch comment's id and time from `date -u`), the export's path and the `df` lines, the census (`qemu 0, compilers 0` by `guest-cycle/helpers/census.sh`, the 15-character process names, `00:73`), and `0` build roots in the worktree.
- **`05`** is not regenerated in S0; its Phase 7 table moves once, after S1 (§ The record).
- **The record:** `02` § The streams' S0 row (`proved: tree` for the records, `tool-run` for the baseline).
- **Commit:** `docs: T37 stage E S0: the records, the deferrals and the #585 lines; PL-06 and PL-10 to the Backlog; the checker's baseline at the S0 tip; stage-d/ (Refs #684, #1381)`.

## S1 -- the five recipe edits (ruling 1; `emulationstation/package.mk` only)

Five edits in this order, each its own recipe commit followed by its record commit, each re-reading its lines at its own parent: a predecessor moves the lines below it, and a moved line is named as moved, never guessed. The recipe is 141 lines at the tip (`02:28`, by `grep -c ''`); each record gives its `grep -c ''` after the edit.

### S1 PL-03 (#1382): `PKG_NEED_UNPACK` names busybox's recipe directory

- **Files:** changed `:14`. Read, not changed: `config/functions:1109-1130` (`calculate_stamp`; the word joins the path list at `:1114`, `find -L` at `:1126`); `:1057` (`get_pkg_directory`); `projects/ROCKNIX/packages/sysutils/busybox/package.mk`, which sources no global recipe (`04:233-235`, the seat's G-4 refuted).
- **Positive before:** `FAIL step 5 GENERIC_X64 PKG_NEED_UNPACK-words-are-directories (L-19): unresolved: busybox` and the H700 twin, on the S0 tree (`checks-at-tip.out:49-50`).
- **The fix:** `PKG_NEED_UNPACK="$(get_pkg_directory busybox)"` (#1382: *"the framework's own form at global scope (the vdr plugins' recipes, `packages/addons/addon-depends/vdr-plugins/*/package.mk:11-12`)"*). One line, so `:39` stays.
- **Positive after:** both L-19 lines PASS; `stamp-moves-iff-touched` as in § The rules (`emulationstation` `moved=1 touched=1`).
- **The busybox pair** (#1382's criterion 2):
  - In each of the two exports (the parent's, the fix's), and only there, append one comment line to `projects/ROCKNIX/packages/sysutils/busybox/package.mk`. Run the checker with `--commit` set to that export's own commit and `--compare` its unmutated `stamps.txt`, then revert the line with its sha256 checked back, or retire the export.
  - **At the parent:** `emulationstation` reads `moved=0 touched=0`. Busybox does not reach the stamp: the defect.
  - **At the fix:** `emulationstation` reads `moved=1 touched=0` on both devices. The step-7 line prints FAIL there, and that FAIL is the expected reading: busybox's recipe now moves the ES stamp from outside ES's directory, which is PL-03's point. `es-theme-art-book-next` and `lowerdeck` read `moved=0 touched=0` in both runs.
  - The record names the two runs as the pair. The FAIL is never read as a regression.
- **Checks:** `find packages projects -type f -path "*/emulationstation/package.mk"` (one path), then `tools/pkgcheck emulationstation; rc=$?` in the worktree (`rc=0`, no `FAIL` or `WARN` line; it sources nothing, so it writes no root), the control `es-theme-no-such-package` beside it (`rc=0 lines=0`, the fail-open `#<Backlog>` tracks); `bash -n` on the recipe; the non-ASCII and secret greps over the added line; the `:39` hash `equal`; `PKG_(VERSION|GIT_CLONE_BRANCH)` `0`.
- **`Already written:`** #1382's: *"nothing inherited -- the line decides which inputs move ES's stamp in a build root; no image, device or cloud holds the stamp, and an image built from the old recipe is byte-identical in what this line touches."*
- **Guest half:** none (#1382: *"No guest row is needed: the stamp never reaches an image"*).
- **Time to play:** none; a build-root input. ES now rebuilds when busybox's recipe changes (`04:166`).
- **#585:** `02:513-515`'s L-19 line, its evidence now this commit and the pair.
- **The record:** `02` § The streams' row (`proved: fix-fixture`; `fix-image-pending` reads *none, the stamp never reaches an image*); `stage-e/s1-PL-03-before.txt`, `-after.txt`, `-busybox-pair.txt`, `-checks.txt`.
- **Commits:** recipe `emulationstation: hash busybox's recipe directory in the stamp` (body: `:14`, the form's source, `Refs #684, #1382`); record `docs: T37 stage E S1 PL-03: the L-19 pair and the busybox stamp pair (Refs #684, #1382)`.

### S1 PL-04 (#1383): the `rm` of `logo.png` after `resources/` is filled

- **Files:** changed `:79` and the line after `:82`. Read, not changed: `:81-85`; the pin's `es-core/src/Splash.h:10-11`, `:16-17` (`04:209`).
- **Positive before:** `FAIL step 5 no-rm-before-its-directory-is-filled (L-04): at emulationstation/package.mk:79 makeinstall_target (filled at :81)` (`checks-at-tip.out:48`).
- **The fix:** the line `    rm -f ${INSTALL}/usr/config/emulationstation/resources/logo.png` moved from `:79` to directly after `:82` (`cp -a ${PKG_BUILD}/resources/* ...`), before `:83`'s `rm` of `DroidSansFallbackFull.ttf`. Net zero lines.
  - The stage-C fixture **dropped** the line (`t37-failfirst.sh:28-30`); the ruled fix **moves** it, so this edit's after line is the moved shape's first run.
  - `/usr/bin/grep -c -F 'rm -f ${INSTALL}/usr/config/emulationstation/resources/logo.png'` prints `1` before and after.
- **Positive after:** the L-04 line PASS; the stamp compare as in § The rules.
- **Checks:** as PL-03's.
- **`Already written:`** #1383's: *"every image built from this recipe carries `/usr/config/emulationstation/resources/logo.png` on its read-only system; the next image built from the fix replaces the system and the file goes with it. Nothing is in `/storage`: `post-update:32-35` links only the four `.cfg` files there, and nothing copies `resources/` out of `/usr/config`. Nothing in a cloud."*
- **Guest half:** `fix-image-pending`, #1383's criterion 2: on the GENERIC_X64 guest of the first image built from `fixed-at`, `ls /usr/config/emulationstation/resources/logo.png` reports no such file and the directory still lists its other files. G-05 read the file at 283,835 bytes (`02:472`).
- **Time to play:** none on the launch or boot path; `SYSTEM` 283,835 bytes smaller.
- **#585:** none is in `02`; the order is upstream's (`651150fc88:53` before `:55`), so a line is proposed (Draft notes, item 6).
- **The record:** `02` row; `stage-e/s1-PL-04-before.txt`, `-after.txt`, `-checks.txt`.
- **Commits:** recipe `emulationstation: drop logo.png after resources/ is filled` (body: `:79` to after `:82`, `Refs #684, #1383`); record `docs: T37 stage E S1 PL-04: the L-04 pair (Refs #684, #1383)`.

### S1 PL-05 (#1384): upstream's ARMSX2 vulkan-driver filter restored

- **Files:** changed: lines inserted between `:128` (`  fi`) and `:129` (`}`). Read, not changed: `:125-128`; `es_features.cfg:1392-1395`; `projects/ROCKNIX/packages/emulators/standalone/armsx2-sa/package.mk:25-31` (the `armsx2-turnip` predicate, `SM4450|SM6115|SM8250|SM8550|SM8650` at `:28`; this draft's read); `start_armsx2.sh:215-218` (`04:210`).
- **Positive before, written first:** two step-5 assertions S1 adds to the checker, named for example `armsx2-vulkan-driver-filter (L-01)` and `armsx2-filter-matches-armsx2-turnip (L-01)`.
  - **The first** reproduces the recipe's own ARMSX2 lines in `xml.etree` (`xmlstarlet` is not on this host, this draft's `command -v`; the stage-C fixture's form, `02:65`). It takes the device pattern and the XPath from the recipe text in the tree and applies them to a scratch copy of the tree's `es_features.cfg` for `DEVICE=SM8550` (inside the five) and `DEVICE=H700` (outside). It counts `//core[@name="armsx2-sa"]//feature[@name="vulkan driver"]` and PASSes only on `1` and `0`.
  - **The second** PASSes only when the recipe's keep-list equals `armsx2-sa/package.mk`'s `armsx2-turnip` case list, read from the tree. That is the seat's G-3 answer (`04:232`), kept true as either recipe moves.
  - **At the pre-fix export** there is no block, so the counts are `1` and `1` (`stage-b/reads.out:108`: `tip armsx2-sa vulkan driver features: 1`; #1384's criterion 1: *"at `2174265e9c` both count `1`"*): both FAIL. Counts only are printed, never a recipe line.
- **The fix:** upstream's `651150fc88:103-108` (the blank line and the five) inserted byte for byte, so the distribution merge sees the same text. `/usr/bin/grep -c armsx2 <recipe>` prints `2` after, as `stage-b/l01-merges.sh` printed for `c445081a59` and `651150fc88` (`l01-merges.out:1-2`; `0` at `2174265e9c`, `:3`). `git -C <worktree> diff -U0 651150fc88 <commit> -- <recipe> | /usr/bin/grep -c -i armsx2` is counted before and after, the diff never printed.
- **Positive after:** both PASS; the stamp compare as in § The rules.
- **Checks:** as PL-03's.
- **`Already written:`** #1384's: *"an image built from the tip's recipe carries the feature in `/usr/config/emulationstation/es_features.cfg`; `/storage/.config/emulationstation/es_features.cfg` is a link to that file (`post-update:32-35`), so the next image's catalogue replaces it. A player who chose either value has a `vulkan_driver` setting in `system.cfg` (`start_armsx2.sh:47`); after the fix the row is hidden and the saved value stays, which is harmless: the launcher ignores it wherever the bundled ICD is absent (`:216`), and on the five devices the row stays. Nothing in a cloud."*
- **Guest half:** `fix-image-pending`, #1384's criterion 2: the image built from `fixed-at` for a device outside the five carries `0` such nodes, read from its `SYSTEM` on the host. GENERIC_X64 ships no `armsx2-sa` (`virtual/emulators/package.mk:97-100`, #1384), so the screen's frame is `CANNOT` on the VM (§ The rules, the flow bullet).
- **Time to play:** none on the launch path; one `xmlstarlet` pass at build time, and one feature fewer in the catalogue on devices outside the five.
- **#585:** none; upstream carries the filter (`02:65`).
- **The record:** `02` row; `stage-e/s1-PL-05-before.txt`, `-after.txt`, `-checks.txt`; the checker's two new assertions named with what each asserts (D-WORKFLOW-210).
- **Commits:** recipe `emulationstation: restore the ARMSX2 vulkan-driver filter` (body: upstream's `651150fc88:104-108`, `b9a5d8caf1`, the four merges, `Refs #684, #1384`); record `docs: T37 stage E S1 PL-05: the ARMSX2 assertions, FAIL at the parent, PASS at the fix (Refs #684, #1384)`.

### S1 PL-07: the install stops when the French catalog is missing

- **Files:** changed: one line inserted after `:68` (`cp -a ${PKG_BUILD}/locale/lang/* ${INSTALL}/usr/config/locale`). Read, not changed: the pin's `CMakeLists.txt:565-578` (`Native language support disabled.`, `02:63`); `config/functions:6` (`die`).
- **Positive before, written first:** a step-4 assertion S1 adds, named for example `french-catalog-guard (L-08)`.
  - It runs in step 4's sourced environment (the export, `env -i`, `HOME` in scratch, so `die` is `config/functions:6`'s). It takes the recipe's `makeinstall_target` lines that name `emulationstation2.mo` and runs each in a subshell with `INSTALL` set to two scratch trees: one holding a planted empty `usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo`, one without.
  - It PASSes only when such a line exists, the first run returns `0` and the second does not.
  - **At the pre-fix export** no line names the file (`checks-at-tip.out:52`'s WARN is the same fact): FAIL. The WARN stays as the checker has it.
- **The fix:** after `:68`, a line testing `${INSTALL}/usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo` with `-f` and calling `die` with an ASCII message naming the file when it is absent. That is the path the candidate carries (`g03-configs.txt:20`: `/usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo`, 176,095 bytes).
- **Positive after:** PASS; the WARN `french-catalog-not-asserted (L-08)` no longer prints; the stamp compare as in § The rules.
- **Checks:** as PL-03's.
- **`Already written:`** argued, no bug line. The line writes nothing on a device; it decides only whether a build without the catalog completes.
  - An image built from the old recipe carried the French `.mo` on its read-only system (the candidate did, G-03) or silently lacked it; the next image replaces the system whole.
  - **What a device keeps in `/storage`:** `/usr/share/locale` is a link to `/storage/.config/locale` (`:134`). The lane reads what writes there before writing this line -- `git -C <worktree> grep -n 'config/locale' <tip> -- projects/ROCKNIX/packages` -- and says whether a device's copy of the catalog is refreshed by the next image or kept: *read both*, or *nothing inherited*, argued.
- **Guest half:** `fix-image-pending`: the catalog at that path on the first image built from `fixed-at` (G-03's read again); a build without the gettext tools stopping at this line is `CANNOT` here (it needs a build).
- **Time to play:** none; a build-time test.
- **#585:** none in `02`; upstream copies the catalog the same way (`651150fc88:41-42`) (Draft notes, item 6).
- **The record:** `02` row; `stage-e/s1-PL-07-before.txt`, `-after.txt`, `-checks.txt`.
- **Commits:** recipe `emulationstation: stop the install without the French catalog` (body: the line after `:68`, `Refs #684, #1381`); record `docs: T37 stage E S1 PL-07: the catalog guard's assertion, FAIL at the parent, PASS at the fix (Refs #684, #1381)`.

### S1 PL-08: `HFS_DEV_LOGIN` in the build log's names

- **Files:** changed `:42-44` (the `for key in` list). Read, not changed: `:45-52` (the loop prints `USING: ${key} (set)` or `WARNING: ${key} not declared, will not build support.`, names only, `:48-50`); `scripts/get_env:14` (`KEEP`); the pin's `CMakeLists.txt:303-305`, `:307-330` *(pin read)*.
- **Positive before, written first:** two step-4 assertions S1 adds, named for example `using-lines-name-every-kept-credential (L-05)` and `using-lines-print-no-value (L-05)`.
  - **The setup:** in step 4's sourced environment for the first device, the names in the tree's `scripts/get_env:14` `KEEP` (read by `sed`, names only) are set to placeholder values assembled at run time, and `pre_configure_target` runs with its stdout to a scratch file.
  - **The first** PASSes when the `^USING: ` count equals the number of names in `KEEP` (`4`).
  - **The second** PASSes when each placeholder value occurs `0` times in that file. It is a control, PASS before and after: the loop prints names only.
  - **At the pre-fix export** the first counts `3`: FAIL. `:40`'s default (built from `:39`'s local) is not reached because every name is set, and nothing from the run is printed but counts.
- **The fix:** `HFS_DEV_LOGIN` added as the loop's fourth name, the `; do` moving to its line. One line in, below `:39`.
- **Positive after:** the first PASS (`4`), the second PASS; the stamp compare as in § The rules.
- **Checks:** as PL-03's.
- **`Already written:`** nothing inherited, argued. The loop writes only build-log lines. Whether a binary carries the HFS scraper is decided by the environment at the pin's `CMakeLists.txt:328-330`, not by this line, so an image built from the old recipe is byte-identical in what the edit touches, and nothing is on a device or in a cloud.
- **Guest half:** none on an image. `fix-image-pending`: the integration build's log carries one line for `HFS_DEV_LOGIN`, `USING:` or `WARNING:`, names only.
- **Time to play:** none; a build-log line.
- **#585:** none (`02:66`: fork-own lines; upstream's loop prints values, `651150fc88:33`, a different matter, Draft notes, item 6).
- **The record:** `02` row; `stage-e/s1-PL-08-before.txt`, `-after.txt`, `-checks.txt`. Then S1's closing work: the FAIL-first script updated and run once (§ The rules), its `SUMMARY:` line in `stage-e/s1-failfirst.txt`.
- **Commits:** recipe `emulationstation: name HFS_DEV_LOGIN in the build log` (body: `:42-44`, `get_env:14`, `Refs #684, #1381`); record `docs: T37 stage E S1 PL-08: the USING-count assertions, FAIL at the parent, PASS at the fix; the FAIL-first script for stage E's set (Refs #684, #1381)`.

## Recorded, no stream

These are ruled above or carried by the brief, and listed here so the Phase 7 gate has every row:

- **PL-01:** deferred to #613 (ruling 2); the checker's L-03 FAIL kept.
- **PL-02:** deferred to #1072 (ruling 3); the checker's L-02 FAIL kept.
- **PL-06:** deferred to `#<Backlog>` (ruling 4), the three reads in `02`.
- **PL-09, PL-11, PL-12, PL-13, PL-16, PL-17, PL-18, PL-19:** recorded (ruling 5); the three #585 lines in `02`.
- **PL-10:** deferred to `#<Backlog>` (ruling 6), with PL-16's tool half and PL-17's mask.
- **PL-14:** deferred to the distribution merge and #791 (ruling 7).
- **PL-15:** the coordinator's sweep (ruling 8).
- **The leads with no punch item,** as `02` records them: L-11 design (D-WORKFLOW-166); L-12 and L-13 notes outside the lanes (D-UI-079); L-16 read (#990); L-20 design; L-22 sound (`02:72-79`).
- **The seat's G-4,** refuted (`04:233-235`).
- **#64's `:54` checkbox,** `CANNOT` from this recipe (`02:217-221`).
- **Withdrawn:** none.

## The order

The streams run S0, then S1's five in this order, one recipe commit and one record commit each, as serial commits with **no rebase** across them. Every S1 edit's assertion is seen to FAIL on its parent's export before the recipe commit.

- **S0:** the audit folder only (the records, the deferrals, the #585 lines, `stage-d/`, the baseline).
- **S1 PL-03:** `:14`.
- **S1 PL-04:** `:79` to after `:82`.
- **S1 PL-05:** between `:128` and `:129` (positions after PL-04, which moves nothing in net).
- **S1 PL-07:** after `:68` (every later line moves by one).
- **S1 PL-08:** `:42-44` (every later line moves by one).

**By file:** `projects/ROCKNIX/packages/ui/emulationstation/package.mk` is the only product file, touched by S1's five recipe commits in that order. `tools/t37-checks.sh` is touched by the record commits of PL-05, PL-07 and PL-08; `tools/t37-failfirst.sh` by PL-08's record commit; `02-forward-audit.md` by every record commit. The lane checks each claim against the commit's `git show --stat --format=`.

## The record

As T36's (`t36-streams.md` § The record), for a recipe slice:

- **`02` § The streams:** the S0 row and one row per S1 edit. Each row has the positive before, the recipe commit, the positive after, the stamp compare's six lines, `tools/pkgcheck emulationstation`'s rc beside its `find` line, `bash -n`'s rc, the `:39` hash `equal`, `Already written:`, `proved: fix-fixture`, `fix-image-pending` with the image read named (or *none* with the bug's VM line), and the `#585` line or *none* with the reason. Then the *Recorded, no stream* list.
- **The generated tables stay the reviewed tip's.** § Coverage (`lines 4561`, the recipe at 141, `02:28`, `:39`) and § The currency (`+14 -34`, `02:347`) are `2174265e9c`'s, made by `tools/t37-tables.py` and never edited by hand (`02:9-12`). S1's record gives the recipe's `grep -c ''` and `git diff --shortstat 651150fc88 <fixed-at> -- <recipe>` at `fixed-at` beside them.
- **`02` § Positives** gains the stage-E lines (the checker's PASS lines, the stamps moving for ES only). Every count is a tool's line.
- **`05`'s gate table and `punch_index`, moved together at Phase 7, after S1:**
  - `05` is generated by `tools/t37-05.py` from one item table (`05:3`), so the outcomes go into the item table and `05` is regenerated, the generator's drift run first. Its header gains `fixed-at: <tip>` and `fixed-at-es: none -- no ES change` beside `:5-6`.
  - **Resolved:** PL-03 (#1382), PL-04 (#1383), PL-05 (#1384), PL-07 and PL-08 (#1381), each with its recipe commit in backticks.
  - **Deferred:** PL-01 (#613), PL-02 (#1072), PL-06 and PL-10 (`#<Backlog>`), PL-14 (#791 and the distribution merge), PL-15 (the coordinator's sweep, #684 with the ruling comment's id).
  - **The eight records** read `**Deferred** | recorded ... (ruling 5; #684 comment <id>)`, with `#585` beside PL-09, PL-11 and PL-19 and `#<Backlog>` beside PL-16 and PL-17. The lint accepts only Resolved, Deferred and Withdrawn, each with an issue or a commit (`tools/lint-audit-artifacts:386-400`); T35's gate wrote its records that way (`d828355e0a`).
  - The index's `outcome:` word agrees with each row (`:409-432`).
- **The tools.** The checker's new assertions named in its header and in `02` § The runs, each with what it asserts and its FAIL line at the parent (D-WORKFLOW-210). The FAIL-first script's fixture change named with its setup lines (D-WORKFLOW-211).
- **The bugs and #1381.**
  - Each bug's body gets `fixed-at:` = its recipe commit (an ancestor of the hand-back tip), and its host checkboxes are ticked with their lines quoted:
    - #1382: all three;
    - #1383: 1 and 3;
    - #1384: 1 and 3.
  - The image checkboxes stay open (#1383's 2, #1384's 2), `fix-image-pending`. The bugs stay open until the branch reaches `next` and, where a checkbox needs it, the first image built from it; the coordinator closes them.
  - #1381's checkboxes are ticked from `05`'s gate as each outcome is recorded.
- **`00`.** Stage E's entries name each checker command, each export and its retirement, the census, `0` build roots in the worktree, and that no compile START was written.
- **The checks:**
  - `tools/lint-audit-artifacts docs/audits/2026_11_01-epic-m6-es-recipe/` PASS on its default `resolution` phase, and the same with `--issue 1381`.
  - `tools/box-check --issue 1381` `0 fail`, and the same on #1382, #1383 and #1384.
  - `tools/register-check` before each record commit.

## The hand-back

After stage E's record, as the brief's § 10 and T36's:

- **One hand-back comment on #684** names **the one distribution tip** of `feature/m6-es-recipe-684` on `origin`. The lane writes `reviewed-at: 9fa740a91ba9fcaa21a26cc72f0b50fac10f32df` (`00:5`, `05:5`), `reviewed-at-es: none -- no ES change`, `fixed-at: <tip>` and `fixed-at-es: none -- no ES change` into #684's body, then says it is idle.
- **The lines, quoted from the tools' own output:**
  - **Every edit's checker pair:**
    - PL-03's two L-19 lines, FAIL then PASS, and the busybox pair's two readings;
    - PL-04's L-04 line, FAIL then PASS;
    - PL-05's two ARMSX2 lines, FAIL then PASS;
    - PL-07's catalog line, FAIL then PASS;
    - PL-08's count line, FAIL `3` then PASS `4`, and its control PASS twice.
  - **The checker at the tip:** its `TOTAL:` line and its two FAIL lines, L-02 (#1072) and L-03 (#613), named as the deferrals they are. Then the checker over a fresh export of the stage-D tip `264a39f6d7`, which FAILs every new assertion but PL-08's control (`using-lines-print-no-value`, PASS at both) and the four stage-C defects, so the acceptance re-runs both directions from one script.
  - **The stamp compare** for each edit: six lines, ES `moved=1 touched=1`, the theme and `lowerdeck` `moved=0 touched=0`.
  - **`tools/pkgcheck emulationstation`'s rc** after its `find` line, at each edit and at the tip, with `es-theme-art-book-next` and `lowerdeck` by name and the control `es-theme-no-such-package` beside them.
  - **`bash -n`** on the recipe at the tip; the non-ASCII and secret counts over all of stage E's added lines (`0`, after their positives).
  - **The FAIL-first script's `SUMMARY:` line** for stage E's set.
  - `git log -p <stage-E start>..<tip> -- projects/ROCKNIX/packages/ui/emulationstation/package.mk | /usr/bin/grep -c -E '^[-+]PKG_(VERSION|GIT_CLONE_BRANCH)='` printing `0`. `git diff --stat <merge hash> <tip> -- packages projects tools` naming the one recipe (§ 7 checkbox 5; `tools` there is the top-level `tools/`, and the audit folder's `tools/` lies under `docs/`).
- **The `#585` lines:**
  - `02` § The #585 lines owed: L-19 (PL-03, with its commit), L-06 (PL-11), PL-029 (PL-09) and PL-19, in the lane's shape, never sent (D-WORKFLOW-164, -165);
  - L-03's carried on #613;
  - PL-04's and PL-07's, if the coordinator takes Draft notes item 6.
- **The Backlog candidates,** now `#<Backlog>`: PL-10 (L-10, L-21), PL-16's tool half, PL-17's mask and PL-06's choice. Any new one the stream found, named with its lines.
- **The checkers:**
  - **The five on the distribution branch,** each with its own `rc=` line: `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test`, again on the coordinator's simulated merge.
  - `tools/lint-audit-artifacts` on the default phase and with `--issue 1381`.
  - `tools/box-check --issue 1381`, and on #1382 to #1384.
- **The collisions** (§ 7's last checkbox):
  - the integration's pin-bump commit on `emulationstation/package.mk`, which S1's five hunks merge over (their positions read at the tip by `git -C <worktree> diff -U0 <stage-E start> <tip> -- <recipe> | /usr/bin/grep '^@@'`, hunk headers only, never typed);
  - #613's `:101` (the M7 lane's);
  - #1072's `PKG_PATCH_DIRS` (T40's);
  - T35's `es-core/CMakeLists.txt` renderer list and T36's bodies beside `:25`;
  - fribidi's choice (`#<Backlog>`);
  - the candidate's nine ES patches and its link (ruling (h));
  - T42's theme patches;
  - T8's `virtual/image/package.mk`.
- **The merge debt:** the recipe's two sides (`02:370-374`), narrowed by PL-05's restoration; upstream's six `ui/` files (PL-14); the two rule errata (the coordinator's sweep).
- **The image halves owed at the integration, every one `fix-image-pending`:**
  - PL-04's `ls` on the GENERIC_X64 guest;
  - PL-05's catalogue count from a non-Turnip image's `SYSTEM`;
  - PL-07's catalog on the image;
  - PL-08's build-log line;
  - PL-03 none.
- **The retro.** `docs/retros/<date>-m6-es-recipe.md`, posted on #684 with its heading's time from `date -u` in the posting command. It says what the slice did to the two time-to-play numbers and to boot to interface: G-04's 5.37 s and 5.82 s, unchanged by construction, with each edit's clause carried. It says what the integration inherits (§ 8).
- After acceptance the coordinator closes #1381 and prompts the lane for `audit-completion.json` and the lint against #1381 (the brief's § 10).

## What the next slices and the integration inherit

The brief's § 8 lists it, and `02` § What the integration inherits (`02:520-542`) is written at the hand-back. Stage E adds:

- **The five recipe lines, where they sit and how each is proven on an image** (§ The hand-back's image halves).
- **The checker's three new assertion groups** (the ARMSX2 filter and its match with `armsx2-turnip`, the catalog guard, the `USING:` count), which keep those shapes from drifting at the next merge.
- **The two FAILs the checker keeps** (L-02, L-03) and the issues that flip them, #1072 and #613.
- **The Backlog** for the checks that pass over nothing, the state check's route, the verbose build's defines and fribidi.
- **The rule errata** as the coordinator sweeps them.

T44 comes after this slice (the brief's § 1); the record names no recipe item for it `[coordinator to confirm]`.

## What never runs here

- **Tools beyond the host's text and git tools:** an image build, a package build or any compiler; a compile START in the host file; a guest; a fetch (no `git fetch`, `git ls-remote`, `gh api` of the theme's or `lowerdeck`'s repositories, no `rc-preflight`, no real `tools/fork-package-freshness` run -- only `--list` with both refs given); a keyed council call; a handheld; the owner's or any hosted account.
- **A change outside `emulationstation/package.mk` and the audit folder:** the other 14 of the 15; the four patches; `virtual/image/package.mk` or any dependency's recipe; ES's `CMakeLists.txt` or `es-core/CMakeLists.txt`; the French catalog; `docs/es-menu-map.md`; `tools/pkgcheck`, `tools/fork-package-freshness`, `tools/pixelelated-state-check` or `config/functions`; the rule and doc sentences L-17 and L-18 name (`device-builds.md:636-645`, `CLAUDE.md:143`, the coordinator's sweep).
- **These recipe lines:** `:5`, `:6` (never); `:101` (#613's); `:13`'s `fribidi` (the Backlog's); a `PKG_PATCH_DIRS` line (#1072's); `:54` (PL-11 recorded); `:39`, `:40` (the shared identity, D-WORKFLOW-166).
- **The sourced recipe in the worktree** (ruling (k)): `config/options` sourced there, or a `build.*` root left there -- a stop.
- **Credentials in the open:** a read of the recipe without the mask; a print of `:39` or of a diff carrying it; `set` or `env` after sourcing; a credential-shaped literal in a fixture; anything under `~/.ROCKNIX/` or `~/.rocknix/`.
- **Held material:** any held directory opened (`/workspace/tmp/m6-t34/held/`, `/workspace/tmp/m6-t36/held/`); none is this slice's.
- **The coordinator's work:** a Backlog filed, a post on #346, #585 or #909, an edit of #613's or #1072's body, a register row, a brief.

## Figures and lines not found in the record (ask the lane; do not guess)

1. **The ruling comment on #684.** The `#684 comment <id>` cells of § The record wait for the coordinator's post of these rulings `[coordinator to confirm]`.
2. **The Backlog's number.** `#<Backlog>` throughout until it is filed `[coordinator to confirm]`.
3. **The stage-E start.** Whether the dispatch merges the coordinator's branch over `264a39f6d7` first (as at stage A's `94d8ef8e7e`) `[coordinator to confirm]`.
4. **The checker's `TOTAL:` after S1.** No run exists; the figure is the tool's line at the hand-back. The draft names only its shape: two FAIL lines (L-02, L-03).
5. **The ARMSX2 counts per device at the tip.** `stage-b/reads.out:108` counts `1` with no device (the tip has no filter); #1384's criterion 1 says *"at `2174265e9c` both count `1`"*. The per-device lines are S1's first run.
6. **What writes `/storage/.config/locale`** (PL-07's `Already written:`) is not traced in the record. An archived session file names `/storage/.config/locale/fr/LC_MESSAGES/emulationstation2.mo` (`.github/sessions/archived/saved-session-state-next-20261011T195846Z.md:396`, this draft's `git grep`), so a device does hold a copy there.
7. **Whether `docs/es-menu-map.md` maps a per-emulator feature row** such as ARMSX2's *vulkan driver*: not read for this draft.
8. **The `+=` form of PL-02's fixture-only line** in the updated FAIL-first script: #1072's comment gives `[ "${ARCH}" = "x86_64" ] && PKG_PATCH_DIRS+=" x86_64"`, while the stage-C fixture used `PKG_PATCH_DIRS="x86_64"` (`t37-failfirst.sh:23`). The draft takes the comment's.

## Draft notes

**What this draft could not or did not read:**
- The held directories, by rule.
- `kit/t37-accept.sh` beyond a `grep` for its stage-E hooks (`:70`, `:95`, `:112-114`, `:157`, `:1161-1165`); `kit/t37-proof.md`; `01-research-notes.md` beyond its length (362 lines).
- `stage-c/verify-seat.out`; the lane's friction lines; #684's body and its pointer file.
- No sourced-recipe call, checker run or `pkgcheck` was made for this draft (a tool beyond `git`, `gh` and the text tools). Every expected FAIL or PASS in S1 is drafted from the record and the recipe's text, not observed.
- `tools/forbidden-terms-check` was not run on these three files, for the same reason. The hooks' credential pattern, compiled as `.githooks/guard-lib` does, was run (see the report).

**Rulings that seem to conflict with the lane's artifacts, and gaps no ruling covers:**
1. **Ruling 4's "at the P1 tip".** The P1 tip's recipe (`2174265e9c:13`) is the fork's, not upstream's. All three reads print `fribidi` `0`, so the ruling's conclusion stands; only its wording names the P1 tip as upstream's.
2. **Ruling 9's "the three deferrals".** Read as PL-01, PL-02 and PL-14 (rulings 2, 3, 7). PL-06 (ruling 4) and PL-10 (ruling 6) are deferrals too, written in S0 under the Backlog pointer. If the coordinator meant PL-01, PL-02 and PL-06, S0's list is the same and only the count's referent changes.
3. **Ruling 5's "Recorded" against the lint.** `tools/lint-audit-artifacts:392-400` rejects any Phase 7 outcome but Resolved, Deferred or Withdrawn. The gate writes the eight as `**Deferred** | recorded ...` with an issue number, T35's form; the coordinator's ruling comment id is the issue citation for the ones with no #585 or Backlog beside them.
4. **The checker exits 1 at the hand-back by design** (L-02, L-03 deferred). § 7 checkbox 9 asks for *"its run at the tip (FAIL naming L-03, and each of L-02, L-19 and L-04 the tracing confirmed)"*; this is consistent, and L-19 and L-04 now PASS. The FAIL-first script's *fixed fixture* must still reach exit 0, so it carries the two deferred fixes as fixture-only lines (§ The rules). A reader could take those lines for a claim that T37 fixed PL-01 or PL-02; the script's header should say they are fixture-only.
5. **PL-07 and PL-08 resolve with no bug of their own** (the lane filed bugs for PL-03 to PL-05 only, `00:101`). #1381's checkboxes are their tracker and the commits cite #1381 (D-WORKFLOW-132). If the coordinator wants a `bug` per fixed defect (T35's ruling 15 filed one per fixed item), the lane files two at S1's start.
6. **#585 lines the ruling does not name.** PL-04's `rm` order is upstream's (`651150fc88:53` before `:55`), so rule 6 and D-WORKFLOW-164 suggest a line is owed; `02:503-518` has none. PL-07's silent copy is upstream's too (`651150fc88:41-42`), an improvement rather than a defect. PL-08's loop upstream prints the value (`651150fc88:33`, `USING: ${key} = ${!key}`), which the fork changed in `144b3eccb6`; whether that change is on #585 already is not in the record. The draft proposes PL-04's line and leaves PL-07's and the loop's to the coordinator.
7. **PL-05 is a visible change** (a row gone on non-Turnip images). `es-ui-style-guide.md` asks for the flow reference and frames with the change; GENERIC_X64 cannot show the row and the lane may not edit `docs/es-menu-map.md`. Whether the map carries such a row, and who records the image's evidence, is the coordinator's.
8. **PL-13 under D-WORKFLOW-024.** The row's scope is the packages the fork introduces plus `EXTRA_PACKAGES` (`decision-register.md:335`); `lowerdeck` is upstream-carried at ROCKNIX's own pin (`05:158`). So the row reaches its bump only if the three recipes join `EXTRA_PACKAGES`, which is the Backlog's section 2 (the PAUSE's question 4).
9. **`stage-d/` is absent** at `264a39f6d7`, while § 7 checkbox 1 and `kit/t37-accept.sh:70` name it. S0 writes it from the stage-D receipts; the content is the lane's.
10. **PL-08's sandbox runs `pre_configure_target`,** which evaluates `:39` and `:40` in the sandbox's memory. Nothing is printed but counts, every name is set so `:40`'s default is not taken, and the output file is scanned for the placeholders. The coordinator may prefer the count taken from a copy of `:42-52` extracted by line number, with `:39` and `:40` never run.
11. **The busybox pair's FAIL line** (`moved=1 touched=0` at the fix) is the expected reading of #1382's criterion 2, not a regression. The acceptance script's checker-record section (`kit/t37-accept.sh:1161-1165`) should not count it as a FAIL of the stream.
12. **The RULING minutes** are this draft's clock at writing (02:39 UTC), not the minute the coordinator ruled.
13. **The rule errata's siblings.** `kit/t37-rule-errata.md` adds the same per-device sentence at `AGENTS.md:154-156` and `packaging-and-patches.md:78-80`, and the `--head maxengel:<branch>` route at `device-builds.md:641-644`. 02/05 do not name them, and the sweep decides.
14. **Register rows.** The brief's § 9 rows (fribidi, the link, the patch directory, the freshness tool's reach, a loud catalog, the ARMSX2 block) are answered by rulings 4, 2, 3, 6, 1 and 1. No ruling names a row; whether fribidi's deferral or the loud catalog takes one is the coordinator's, at an ID it assigns (the next after D-WORKFLOW-217).

## Errata at acceptance

Appended by the coordinator at T37's acceptance (05:01 UTC 2026-11-01; the hand-back `d6dde340f9`; the record read at `1fd89a16e5` and `d6dde340f9`), from `kit/t37-errata-at-acceptance.md`: the brief's words at the hash the lane read, against the record's lines. Nothing above this heading is edited (the register's append-only rule, applied to a brief).

- **Ruling 14 places the expected FAIL "before the fix"; it appears at the fix (stage E S1 PL-03; the hand-back, comment 6552950785):** `:74` reads "the busybox stamp compare's FAIL before the fix is the expected result and `02` records it as `expected FAIL (the stamp did not move)`". The brief's own S1 text at `:177-179` places it at the fix ("**At the parent:** `emulationstation` reads `moved=0 touched=0`. Busybox does not reach the stamp: the defect. **At the fix:** `emulationstation` reads `moved=1 touched=0` on both devices. The step-7 line prints FAIL there, and that FAIL is the expected reading"), and so does the run: at the parent `moved=0 touched=0` with no FAIL line, at the fix `FAIL step 7 ... emulationstation stamp-moves-iff-touched: moved=1 touched=0` on both devices (`02:786-792`; `stage-e/s1-PL-03-busybox-pair.txt`; the hand-back: "That second reading is ruling 14's expected FAIL, seen at the fix rather than before it"; the retro `:57-61` and its proposal `:171-173`, "a stream brief that names where a stamp-input fix's expected FAIL appears").
- **The `#585` lines for PL-04, PL-07 and PL-08 are owed, not conditional:** `:334` reads "PL-04's and PL-07's, if the coordinator takes Draft notes item 6". Ruling 17 in the same brief (`:78-79`) takes the item and adds PL-08: "PL-04's `rm` order, PL-07's catalog copy and PL-08's `USING:` loop are upstream's too: S0 writes a `#585` line for each beside PL-09's, PL-11's and PL-19's". The record carries all three, each marked "(ruling 17)" (`02:1048-1057`; the hand-back's `#585` list).

## Superseded at acceptance

The readings the acceptance settled; the text above stands as dispatched.

- **`fixed-at` in `05`'s header and in #684's (`t37-streams.md:294`, `:317`; `es-recipe.md:1403`, checkbox 5; the coordinator's ruling of 04:11, comment 6553258188 ask 2):** `:294` "Its header gains `fixed-at: <tip>` and `fixed-at-es: none -- no ES change` beside `:5-6`"; `:317` "The lane writes ... `fixed-at: <tip>` and `fixed-at-es: none -- no ES change` into #684's body"; checkbox 5 "`reviewed-at:` and `fixed-at:` in #684's header carry the lane's commits". A file cannot name the commit that writes it: `05:7` reads `fixed-at: c9e8d5a8df`, the last recipe commit (`git diff --name-only c9e8d5a8df 1fd89a16e5 -- packages projects tools` prints `0` paths), and #684's header carries the hand-back tip (`fixed-at: 1fd89a16e57dcddf985c24babee03f25a524a538`, read live). The first hand-back had moved all four to its tip `c00c39ffe6` on the stream brief's words (comment 6552950785, "A correction before this post"); the ruling put `05:7` back.
- **"One hand-back comment ... the one distribution tip" (`t37-streams.md:317`; ruling 10 at `:64`; `es-recipe.md:1639` "one hand-back comment naming **its one tip**"):** the acceptance read of `c00c39ffe6` posted seven asks (6553258188), closed by one amendment commit and a second hand-back post (6553382014) naming the new tip `1fd89a16e5` (the merge `52045e1b79` of the coordinator's `afe3bac032`, then the amendment). The acceptance script takes the second tip through `HANDBACK_TIP2` (`kit/t37-accept.sh:193`, `:1497-1498`). Two posts; one tip at acceptance.
- **"The S0 row and one row per S1 edit" (`t37-streams.md:290`):** the record has the S0 table row (`02:770`) and one `### S1 PL-0N` subsection per edit (`02:772-934`), each carrying every part the row asks (the positives before and after, the recipe commit, the stamp compare, `pkgcheck`, `bash -n`, `:39 equal`, `Already written:`, `proved: fix-fixture`, `fix-image-pending`, the `#585` line). A subsection is that stream's row (`kit/t37-accept-triage.md`, `streams`; the asks' preamble: "the shape, not a gap").
- **Checkbox 8's "each as a command's own output line" and checkbox 9's "`02` § The runs records" (`es-recipe.md:1406-1407`; asks 3 and 4):** the lines are quoted into `02` § The runs; a citation of `stage-a/s5-runs.out` R01-R22 or of § The streams does not suffice ("the record is read without opening `stage-a/` ... a citation is not the line"). At `1fd89a16e5` they stand at `02:470-641` (checkbox 8, copied by line range from `s5-runs.out`, which was written through the mask) and `02:642-731` (the checker's record, copied and not moved).
- **Three more readings closed by the amendment:** checkbox 10's `SECRET_PATTERNS` count "over the folder" (`:1408`; ask 6) is in `02` § The recipe over the audit folder (`02:226-237`: 167 files, matching lines 0, after a planted positive), not only over the 15 and the patches (R20) and stage E's added lines; checkbox 11's "G-01's `ldd` line beside it" (`:1409`; ask 5) is quoted in `02` § The dependencies (`02:256-260`), not only at `01:288`; § The record's "`00`. Stage E's entries name each checker command" (`t37-streams.md:307`; ask 7) means each `tools/t37-checks.sh` run with its `--commit` and `--compare` arguments (`00` § Stage E at `1fd89a16e5`).
