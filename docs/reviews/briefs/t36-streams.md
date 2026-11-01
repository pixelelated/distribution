# T36 (#683): the stream brief for stage E

Written at the pause from the lane's punch list (the audit issue #1358; the pause post `kit/t36-stageD-pause.md`, 00:12 UTC 2026-11-01; the record at `2e5229eed7`), drafted by an agent from T35's shape (`docs/reviews/briefs/t35-streams.md` at `960d581c12`) and ruled by the coordinator at 00:42 UTC 2026-11-01 (the `RULING` lines, D-WORKFLOW-189). The rulings name no register row; whether the brief's § 9 questions (the `exists` cache, the file helpers' contract, the three-byte case, the pipe) take rows is the coordinator's (Draft notes, item 12). The Backlog ruling 2 names is filed by the coordinator from `kit/t36-backlog-pl10.md` (`#<Backlog>` below until it has a number). The brief is `es-core-utils-resources.md` at `e29a2966bc`; where this file and the brief differ, this file wins for stage E.

**The coordinator's, drafted at T36's stage-D pause, 00:42 UTC 2026-11-01.** Read from the lane's record at the distribution tip **`2e5229eed7`** on `feature/m6-es-core-utils-resources-683` by `git show` only, never the worktree: `05-punch-list.md` (10 items, the collisions, the pauses and errata, the held table), `04-analysis.md` (the grades, the three corrections, G-1 to G-21), `02-forward-audit.md` (§§ The leads, The file cache, The texture and font caches, The paths, The processes, The writes and reads, The device reads, The structure, The merge debt, The runs, The guest cycle, Positives, The #585 lines owed), `03-retrospective.md`, `00-running-log.md`, `stage-a/runs.out`, `stage-c/build-tests.out`, `stage-c/utils-resources-tests.run.txt`, `stage-c/syntax-check-probe.out`, `stage-c/t35-311-rerun.out`, `tools/t36-build-tests.sh`, `tools/t36-extract.py`, `tools/t36-utils-resources-tests.cpp`. The tracker: the bugs' public bodies #1359 to #1371 and the audit issue #1358 (`gh issue view N --json title,body`), #1186's body. The slice brief at `e29a2966bc` (§ 1 rulings (a) to (k), § 4's floor table 3.1 to 3.25, § 5 items 1, 3 and 4, § 7, § 8, § 9, § 10). T34's PL-17 on `feature/m6-es-core-components-681` at `49c6b43f27`. A pin line the record does not carry was read at the pin by `git -C <W> show 16dbac5211:<path>` and is marked *(pin read)*. The register at the coordinator worktree's `960d581c12`: the highest decided rows are D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-014, D-UI-137 and D-WORKFLOW-216 (this draft's `awk` over the table's ID column), so a row a stream forces takes the next ID the coordinator assigns. **Nothing under `/workspace/tmp/m6-t36/held/` or `/workspace/tmp/m6-t34/held/` was opened for this draft;** the held streams below carry only what ruling 6 lets them carry.

The ES branch `feature/m6-es-core-utils-resources-683` in `W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683` is at the pin `16dbac5211eea7e70db7394372033be2be7df829` with 0 changes (`git -C <W> rev-parse HEAD`, `status --porcelain | wc -l`, this draft's read) and not on `origin` (`rev-parse --verify origin/feature/m6-es-core-utils-resources-683` prints `fatal: Needed a single revision`); it reaches `origin` with S1's push. The distribution worktree `/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-utils-resources-683` (at `2e5229eed7`) takes only the audit folder's records (`docs/audits/2026_10_31-epic-m6-es-core-utils-resources/`, its `tools/` and `stage-e/` included) and the day's log.

**The standing rulings for this slice, applied here and not re-asked:** the brief's § 1 (a) to (k) and D-WORKFLOW-216 (T36 owns the 58 and nothing else). Every item in the 58 is upstream-carried beyond the 15 whole fork files (`05:3`), so every fix is a `bug` closed under `bugs-are-agent-first.md` rule 6, its unit case seen to FAIL at the pin first. `utils/AtomicFileUtil.*` and `utils/DownloadFile.*` are T21's (rulings (a), (b)); T20's `d9afa5c7c`, T21's `f7c16144d` and T26's `a5d2d3756` are collisions, never re-made (ruling (d)); `tests/app-unit/fakes/utils/FileSystemUtil.h` is not the lane's, and a change to `exists`, `readAllText`, `removeFile` or `getFileName`'s signature is a collision named in the hand-back (ruling (g)); a fix to the cache's answer re-runs T35's 3.11 unchanged from T35's tip (ruling (h)); #1263 keeps its picture checkbox open for this record (ruling (i)). A finding is held only under D-WORKFLOW-215's test, and the lane opens no held directory but its own.

## The rulings

Each ruling gives the items with their lines (`05`'s), what the lane proposed (the pause post's table, `kit/t36-stageD-pause.md:9-42`), the options the record left, and what the streams carry. The `RULING` line is the coordinator's.

1. **PL-01 to PL-09: the nine single-defect items** (`05:13-103`; the bugs `05:9`).
   - **The items:**
     - PL-01, #1362, Medium: `toUpper`/`toLower` (`StringUtil.cpp:357-362`, `:398-403`; tables `:30`, `:105-108`, `:184-188`).
     - PL-02, #1363, Medium: `copyFile` over an absent source and a short write (`FileSystemUtil.cpp:1472-1474`, `:1500-1509`).
     - PL-03, #1364, Medium: `removeFile` leaves the deleted path cached (`:1067`, `:1080`, `:1084`).
     - PL-04, #1365, Low: `createDirectory`'s race and an existing file (`:1089-1120`, `:1093-1095`).
     - PL-05, #1366, Medium: the thumbnail reads (`TextureData.cpp:331`, `:339`, `:410`).
     - PL-06, #1359, **High**: the font atlas (`Font.cpp:258-275`).
     - PL-07, #1360, **High**: the date format's buffer (`TimeUtil.cpp:415-508`).
     - PL-08, #1361, **High**: `copyFile` onto the same inode (`FileSystemUtil.cpp:1481-1509`).
     - PL-09, #1367, Medium: `loadFromPdf`'s return (`TextureData.cpp:425-444`).
   - **The lane proposed:** *Resolve (rule 6)* for each (`kit/t36-stageD-pause.md:9-17`); *"All ten are upstream-carried, so each is a rule-6 contained fix (a guard, a bound, a return, a quote)"* (`:20`).
   - **Options:** resolve under rule 6, or record. No item's record argues for recording.
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** PL-01 to PL-09 (#1359 to #1367) are **Resolved in stage E as rule-6 contained fixes** (`bugs-are-agent-first.md` rule 6: upstream-carried defects we found are ours to close when the fix is a guard, a bound, a return, a quote). Each stream's fix is the smallest change that makes its unit case pass; a fix that wants more than a contained change pauses with a question.
   - **What the streams carry:** PL-06 in S1, PL-07 in S2, PL-02, PL-04 and PL-08 in S3, PL-03 and PL-05 in S4, PL-01 in S8, PL-09 in S9. A fix that needs more than a guard, a bound, a return or a quote stops that stream and posts the question on #683.
2. **PL-10 (#1368): the grouped findings, split** (`05:105-113`; `04:43-59`).
   - **The lane proposed:** *"Resolve the safety/overreads; your call on the minor leaks"*: G-6, G-7, G-10, G-14, G-20 and G-3 resolve; G-2, G-5, G-12, G-13 and G-21 *"Resolve or **Defer to Backlog** at your preference"* (`kit/t36-stageD-pause.md:18`).
   - **Options:** all eleven in stage E; the six in stage E and the five to a Backlog; all eleven to a Backlog.
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** PL-10 (#1368) is split: the overreads, null-dereferences and unchecked arithmetic (G-6, G-7, G-10, G-14, G-20, G-3) are **Resolved** in one stream; the leaks, races and classifications (G-2, G-5, G-12, G-13, G-21) are **Deferred to Backlog #1372** (filed by the coordinator at 00:45 UTC 2026-11-01) from `kit/t36-backlog-pl10.md` (title `Backlog: EmulationStation utils/resources: the leaks, races and classifications T36's seat found (G-2, G-5, G-12, G-13, G-21)`, one section per item quoting `05`/`04`'s words and the file:line, acceptance criteria an agent can tick, no label). At stage E the lane edits #1368's body to the Resolved set, pointing at the Backlog.
   - **What the streams carry:** S10 holds the six. #1368's body sentence *"one bug per finding at the stream, this issue the umbrella"* is replaced in that edit by the Resolved set and the Backlog's number, and the PL-10 checkbox on #1358 is edited the same way (the audit issue and the bugs are the lane's, D-WORKFLOW-189). G-11, which `05` folds into PL-03 as *"the remaining race"* (`05:39`, `04:50`), is in neither list; it is recorded with PL-03 (Draft notes, item 5).
3. **L-04: `writeAllText`'s void return** (`FileSystemUtil.cpp:1429-1446`; `05:127`; `02:376`, #1186's last comment read as 6440869119).
   - **The lane proposed:** *"Hold for #1186"* (`kit/t36-stageD-pause.md:30`).
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** L-04 (`writeAllText`'s void return, or its supersession by `AtomicFile::writeText`) is **held for #1186**; the coordinator posts the one-line pointer on #1186; no stream.
   - **What the streams carry:** nothing. Case 3.3 stays the text record it is (`tools/t36-utils-resources-tests.cpp:96-103`; its line `MESSAGE: writeAllText is void at the pin; a fix's CHECK_FALSE comes with #1186`, `stage-c/build-tests.out:19`). No stream changes `:1429-1446`.
4. **L-08 and L-13: the two rule errata** (`05:128`, `:129`; `02:417-419`).
   - **The lane proposed:** *"your sweep"* for both (`kit/t36-stageD-pause.md:31-32`).
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** L-08 (`es-code-traps.md:118`, the font height) and L-13 (`es-native-ui.md:103`, `runSystemCommand`) are **rule errata the coordinator sweeps**: `kit/t36-rule-errata.md` carries, for each, the rule file and line at `960d581c12`, the sentence as it stands, the replacement the seat's narrowing supports (`04`'s words with their line), and T34's PL-17 beside L-08; no stream.
   - **What the streams carry:** S0 runs 3.8 as the brief's linked positive (the floor table: `h = getHeight(); sizeText(<ASCII 32..126>); CHECK(getHeight() == h)`), because the 3.8 the binary holds is a text case whose comment states the erratum the wrong way round (`tools/t36-utils-resources-tests.cpp:207-214`, `:209`: *"es-code-traps.md:118 says the height is fixed; the source grows it"*). The lane records both errata in `02` § The structure as *the coordinator's, at acceptance*.
5. **L-05 and L-14: the seat's two narrowings** (`05:130-131`; `02:331-341`, `:347`, `:451`; `04:22`, `:55-56`).
   - **The lane proposed:** *"A `bug` for the quoting/mask gaps, severity pending whether a real logged sink is shown"* (`kit/t36-stageD-pause.md:33`).
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** L-05 and L-14 (the seat's narrowings: `SigIgn=0x1000` shows EPIPE, not a signal kill; a quoted flag evades the mask) are **recorded in `02` § The leads as the seat left them**; the quoting gap belongs to #1371's stream; **no further public bug**.
   - **What the streams carry:** S6 carries *the quoting gap*, read by this draft as L-05's G-18: *"`run()`'s log path interpolated unquoted; `2>` binds only the last simple command"* (`04:56`, `Platform.cpp:162`; `05:131`, *"recorded, a `bug` for the quoting"*). L-14's mask shapes (3.10, G-17 at `StringUtil.cpp:725-795`) are recorded with no stream (Draft notes, item 6). The pipe's `head -300` and its EPIPE (`02:451`) stay as recorded; 3.5's two rcs are re-run unchanged in S6.
6. **#1369, #1370, #1371: the three held findings** (`05:133-139`; `00:93`).
   - **The lane proposed:** routing to the maintainer as the coordinator's (`kit/t36-stageD-pause.md:37`).
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** the three held bugs #1369, #1370 and #1371 are **Resolved in stage E** as one stream each, the fixes the held records describe; the stream brief names only the bug number, the file and the words *the contained fix the held record describes*; the unit case is named by the bug number and its inputs are read from the held record, never written in the brief, the commit message or the case's name; the case files live where the other cases do. The coordinator tells the maintainer on #346.
   - **What the streams carry:** S5 (#1370), S6 (#1371) and S7 (#1369), under § The rules every stream keeps' held-stream bullet.
7. **The serial order for `utils/FileSystemUtil.cpp`.**
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** **serial order for `es-core/src/utils/FileSystemUtil.cpp`**, the one file touched by more than one stream: the `copyFile`/`createDirectory` stream (PL-02, PL-04, PL-08), then the cache stream (PL-03, PL-05 -- PL-05's `TextureData` read is the same stream), then #1370's, then #1371's, as serial commits in that order with no rebase across streams; every other stream is independent. Each stream names the files it touches so the lane can check the claim.
   - **What the streams carry:** S3, S4, S5, S6 in that order. **The draft's check of the claim:** under ruling 2's one stream, S10's G-14 is in `FileSystemUtil.cpp` too (`:146`, `:1063-1065`, `removeFile`, the function S4 changes), and S10 also touches `StringUtil.cpp` (after S8), `TimeUtil.cpp` (after S2), `TextureData.cpp` (after S4 and S9) and `Font.cpp` (after S1). § The order lists every file with its streams; S10 runs last so that each of its touches lands after the stream it follows (Draft notes, item 1).
8. **Owed and carried: `es-unit-tests`, the four fakes, the renderers positive** (`02:439-440`; `00:94`; `kit/t36-stageD-pause.md:39-42`; `tools/t36-build-tests.sh:35-39`).
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** **owed and carried into stage E:** `es-unit-tests` is tried once more with rapidjson 1.1.0's headers taken from the shared sources cache `/workspace/cache/rocknix-sources/` (extract to scratch, point `-DRAPIDJSON_INCLUDE_DIR` at it) or read from the legacy GENERIC_X64 build root's `build/rapidjson-1.1.0/include` (a read); if the failure is a warning promoted to an error under g++ 15, `-Wno-error` is the answer and recorded; if a genuine incompatibility, `CANNOT` with the first error whole, and the slice's three linked files stand proven by the stand-in. The stand-in's four T36 fakes and the renderers positive under `-DUSE_OPENGLES_30` run as bracketed host compiles with no M7 START open.
   - **What the streams carry:** S0. The cache holds `rapidjson/rapidjson-1.1.0.tar.gz` with its `.sha256` and `.url` (this draft's `ls`; nothing opened); no `build.ROCKNIX-GENERIC_X64.x86_64/build/rapidjson-1.1.0/include` exists under `/workspace/repos/rocknix.worktrees/*/` or `/workspace/repos/pixelelated/*/` (this draft's `ls`, the same as `02:440`), so the cache is the route.
9. **S0: the floor cases no stream holds.**
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** **S0** is the record-only stream before S1: the floor cases no stream holds (read from `02` § The leads), each run at the pin, with the `TOTAL:` line, as T35's S0 was (ruling 21 of T35's stream brief).
   - **What the streams carry:** S0's set is derived, not read: `02` § The leads' floor rows all read `pending stage C` or `tool-run` (`02:116-141`) and none reads `design` (this draft's `grep -n design` over `02` printed nothing). Against the 15 cases the binary holds (`tools/t36-utils-resources-tests.cpp:75-221`; `RUN utils-resources-tests: rc 1; [doctest] test cases: 15 | 11 passed | 4 failed`, `stage-c/build-tests.out:7`), the floor's unwritten rows are 3.6, 3.11, 3.12, 3.17, 3.22, 3.23 and 3.25; 3.5 is a stage-A tool run, 3.14 is T35's case, 3.19 and 3.20 are held (`02:134-135`). S0 writes the seven and the linked 3.8 (ruling 4).

10. **The confirmed leads with a case and no punch item** (L-07, L-09, L-10, L-11, L-15, L-18, `04:21`; 3.21's wrong result at the pin).
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** at the start of stage E the lane files one `bug` per lead whose case FAILs at the pin, with its trace (D-WORKFLOW-189: lanes file bugs); where the lead's file is already touched by a stream, the fix lands in that stream as a contained fix and the stream's `02` row names the added bug; otherwise the bug is **Deferred** to a Backlog the coordinator files from the hand-back's list. S0's set is the derived one: 3.6, 3.11, 3.12, 3.17, 3.22, 3.23, 3.25 and 3.8 as the brief's linked positive (ruling 9's `design` read as the floor rows' `pending stage C`).
11. **3.8's comment and 3.22's citation.**
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** S0 corrects 3.8's comment (`tools/t36-utils-resources-tests.cpp:209` states the erratum backwards) and either writes 3.22 or corrects `00:57`'s citation of it; a record-only stream may fix test text.
12. **The collision controls.**
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** 3.4 and 3.2's `renameFile` half, which test T20's and T21's fixes outside T36's tree, are marked `may_fail` with the reason beside them, as T35's ruling 20 did; they stay in the binary.
13. **`[-Wtemplate-body]` under g++ 15.**
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** `-Wno-error` first, then `-Wno-template-body`; if neither builds `es-unit-tests`, `CANNOT` with the first error whole, posted on #683 before any other flag is tried; the tarball in the sources cache is the headers' route (no legacy root holds rapidjson).
14. **"The quoting gap".**
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** ruling 5's quoting gap is L-05's G-18; `Platform.cpp:162-168` is S6's.
15. **G-11.**
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** PL-03's residual race G-11 is **Deferred** with the races to Backlog #1372.
16. **One bug or six.**
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** #1368 stays one bug for its six Resolved items; at stage E the lane amends #1368's and #1358's "one bug per finding" sentence to say so and points the five deferred items at Backlog #1372 by number.
17. **Ruling 7's "the one file".**
   - **RULING (coordinator, 00:45 UTC 2026-11-01):** corrected: S10 shares `Font.cpp`, `TextureData.cpp`, `FileSystemUtil.cpp` and `TimeUtil.cpp` with earlier streams; § The order's per-file stream list binds, and S10 runs last.

## The rules every stream keeps

- **Test first, then the fix; the test's FAIL is recorded before the fix lands** (`engineering-practices.md` § Guards must fail closed).
  - **Where the positive lives.** It is a case in the lane's `utils-resources-tests` (`tools/t36-utils-resources-tests.cpp`, built by `tools/t36-build-tests.sh` with `FileSystemUtil.cpp`, `StringUtil.cpp` and `md5.cpp` linked whole and the parse-only seams lifted by `tools/t36-extract.py` at `git -C <W> rev-parse HEAD`, `t36-build-tests.sh:43-52`). A refused extract is not built: *"t36-build-tests: the extracts were refused; utils-resources-tests not built"* (`:44`). The other homes are a sibling binary in the same script, for a source the binary's doubles stand in for (`TimeUtil.cpp` against the `DateTime` double, `tools/t36-utils-resources-tests.cpp:41-43`; `ZipFile.cpp` against the `computeCRC` double, `:38-40`), or a sanitizer program run by a `san()` function in T35's shape (T35's `t35-build-tests.sh:153-166`), which S0 adds to `t36-build-tests.sh`.
  - **The command:** `RAPIDJSON_INCLUDE_DIR=/workspace/tmp/m6-t36/rj/rapidjson-1.1.0/include bash docs/audits/2026_10_31-epic-m6-es-core-utils-resources/tools/t36-build-tests.sh "$W" /workspace/tmp/m6-t36/build`. The rapidjson root is `stage-c/build-tests.out:3`'s and the build directory is `:5`'s `-DT36_X` parent and `:12`'s; the invocation itself is not in the record (§ Figures not found, item 1). `RAPIDJSON_INCLUDE_DIR` must be set: `:23` reads it unguarded under `set -u` (`:13`).
  - **The lines at the pin, quoted in records, never summed in the head.** The script prints `TOTAL: N test cases in B binaries` (`:70`). At the pin it printed **`TOTAL: 15 test cases in 1 binaries`** (`stage-c/build-tests.out:26`) over `RUN utils-resources-tests: rc 1; [doctest] test cases: 15 | 11 passed | 4 failed | 0 skipped [doctest] assertions: 48 | 41 passed | 7 failed |` (`:7`), the four failing cases 3.1, 3.2, 3.4 and 3.26 (`:8-11`). `es-unit-tests` is not built by the script (`:35-39`); S0's retry decides whether it joins the line.
  - **Where each run goes.** The output at the pin goes into `stage-e/sN-before.txt`, the output after the fix into `stage-e/sN-after.txt`, and the full checks into `stage-e/sN-checks.txt`, under the audit folder.
  - **Every stub against the unfixed code first.** A case written for the fixed shape can fail for a reason the pin never had (T21's S11; `engineering-practices.md`), and a FAIL is evidence only when the double reproduces the pin everywhere else. A case that cannot be made to FAIL at the pin within a stated bound (a race, a timing) is recorded with its stub's line, and its fix waits on a question on #683. A case that FAILs at the pin on a line no ruling names is a new `bug` before any fix (D-WORKFLOW-132).
- **D-WORKFLOW-210, as it lands here.** `tools/t36-extract.py` reads the ES tip, so a stream that moves a spec'd line changes its `SPECS` entry (`t36-extract.py:14-32`) in the stream's record commit, naming what it asserted before and after.
  - `Font.cpp`'s specs after `:277` (`font_glyph_grow` `:420-421`, `font_sizetext` `:714-752`, `font_getheight` `:754-757`, `font_fromtheme_scale` `:1231-1256`) move with S1 and S10; `font_ctor_scale` `:93-120` stays.
  - `Platform.cpp`'s `run_wrap` `:162-168` changes with S6, whose first-line string (`std::string cmdOutput = "((((`) the fix may change, and `quites` `:216-239`, `runsys` `:853-880` and `gsh` `:891-905` move by S6's line delta.
  - `cleanupvram` (`TextureDataManager.cpp:135-194`) moves with no stream.
  - A new spec is added for each new lift. `tools/t36-tables.py` asserts its tables against the pin by `git show` (`00:30`) and stays the pin's; a stream changes `02`'s generated tables only through it, never by hand (`02:5`).
  - **D-WORKFLOW-211:** a fixture that relied on the defect is completed in the stream's commit, its setup line named, no assertion changed.
- **The collision controls (proposed; no ruling names them, Draft notes, item 3).** Two FAIL-at-pin lines stay FAIL at T36's tip because their fixes are other lanes': 3.4 (`readAllText`, T20's `d9afa5c7c`, #1177; `stage-c/build-tests.out:20-23`) and 3.2's `renameFile` half (`tools/t36-utils-resources-tests.cpp:90`, T21's `f7c16144d`, #1191; `stage-c/build-tests.out:15-16`). By T35's ruling 20's precedent, 3.4 is marked `doctest::may_fail` naming #1177 in S0, and 3.2 is split in S3 into its `renameFile` half (`may_fail`, naming #1191) and its `copyFile` half (S3's covering case), no assertion changed. The hand-back quotes the `may_fail` count beside the `TOTAL:` line and cites the test-case summary, since doctest's assertion summary still counts a `may_fail` case's assertions as failed (T34's acceptance erratum 9).
- **The stand-in** is the lane's own `stage-a/syntax-check.sh` with `stage-a/fakes/`, which S0 writes where the brief's § 6 and `01:62` put it: T35's 15 fakes and T36's four (FreeType, `vlc/vlc.h`, GLES3, SDL-GL), the pugixml root and `-DUSE_OPENGLES_30`. At stage C, T35's script over the 25 `.cpp` printed **`t35-syntax-check: 25 file(s) checked, 20 rc 0, 5 not`** (`stage-c/syntax-check-probe.out:36`), the five being `renderers/GlExtensions.cpp`, `renderers/Renderer.cpp`, `renderers/Shader.cpp`, `resources/Font.cpp` and `resources/TextureData.cpp` (`:2-20`).
  - It runs over every `.cpp` a stream edits, PASS before the stream's commit. A `.h` is proved through the `.cpp`s that include it, named.
  - `tools/es-syntax-check` exits 2 on this host (`es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)`, `stage-a/runs.out:232-233`), so each source is `CANNOT` with that line and the stand-in is the check.
  - An rc 0 on a renderer file is evidence only beside its positive: the preprocessed TU's count of `GLES30Renderer` nonzero with `-DUSE_OPENGLES_30` and zero without, and `Renderer_GL21`, `Renderer_GLES10` and `Renderer_GLES20` recorded as empty under the image's defines (the brief's § 5 item 1).
- **The French.** Every new or changed player sentence ships in English and French in the same commit (D-UI-051): the msgid byte for byte in `locale/lang/fr/LC_MESSAGES/emulationstation2.po`, in that file's own style. The catalog is the one path outside the 58 a stream may touch, and only for that. The slice's `_("` lines are 11, in `MathExpr.cpp` and `TimeUtil.cpp` (`_(" lines TOTAL 11 in 2 files`, `stage-a/runs.out:117`; their msgids and French `02:395-402`). **No stream below is expected to change a msgid.** After every commit, `tools/es-untranslated` prints the line it printed at the pin, `es-untranslated: 706 fork string(s) in the source, 706 with French, 0 without` (`stage-a/runs.out:144`), or names the sentence a stream added in neither list.
- **Non-ASCII comments.** The check runs over the lines the stream added (`git diff -U0 HEAD -- <file>`, its `+` lines, `grep -nP '[^\x00-\x7F]'`), never over upstream's lines. Upstream's non-ASCII bytes stay as they are: `FileSystemUtil.cpp`'s three `//` comments (`:225`, `:287`, `:718`), `StringUtil.cpp:1406-1407`, `StringUtil.h:62-68` (the brief's r17 line; `stage-a/runs.out` r17). A glyph in a string literal is allowed (`es-code-traps.md:60`, § Comments near a translatable string must be ASCII); French lives in the catalog, never in a `.cpp`.
- **One commit per stream** on the ES branch, subject `fix: T36 stage E S<n>: ... (Refs #683, #<bug>)`, no closing keyword, the files named in the body. Its record on the distribution branch is `docs: T36 stage E S<n>: ... (Refs #683)`. The ES `.githooks/pre-push-test` runs before each push, and `tools/register-check` on the distribution side before each record commit. A source a stream changes cites its bug number in an ASCII comment, nothing more; rows are cited in commit bodies.
- **Nothing changes outside the 58 and the audit folder** (the catalog as above).
  - **Other lanes' files.** `es-core/src/components/**` is T34's. `Window.*`, `Log.*`, `InputManager.*`, `Scripting.*`, `ImageIO.*` and `es-core/CMakeLists.txt` are T35's. `utils/AtomicFileUtil.*`, `utils/DownloadFile.*`, `HttpReq.*`, `Settings.*` and `SystemConf.*` are T21's. `CloudText.*` is T18's. `tests/app-unit/fakes/` and everything under `es-app/src` belong to their owners (the brief's § 10, *What never runs*).
  - **What a stream needs from another lane** is written as a patch under `stage-e/`, proven on a scratch copy of the file read by `git show`, and named under merge debt, never made here. None is expected; S7's caller in `es-app/src/ApiSystem.cpp` (#1369's public body) is the one candidate.
  - **The fakes' double.** No stream changes the signature of `exists(const std::string&, bool)`, `readAllText`, `removeFile` or `getFileName` (ruling (g)); the hand-back proves it with a `git diff 16dbac5211 <tip> -- es-core/src/utils/FileSystemUtil.h`.
  - **Another lane's fix in this slice's file** is never re-made (ruling (d)): S3 does not touch `renameFile` (`:1448-1464`, T21's) or `skipUtf8Bom` (`:1369-1379`, T20's); S6 does not touch `GetShOutput` (`Platform.cpp:891-905`, T26's).
- **The held streams (ruling 6): S5, S6's held half, S7.**
  - This brief, the stream's commit message, its case's name and every public record name only the bug number, the file and the words *the contained fix the held record describes*. The lane reads the fix's shape, the case's inputs and its expected result from its own held record (`/workspace/tmp/m6-t36/held/`, `05:137-139`), and from nowhere on the tree.
  - **The case** lives where the other cases do (`tools/t36-utils-resources-tests.cpp`, or a sibling binary or `san()` program in `t36-build-tests.sh`), is named `#<bug>` alone, reads its input and its expected result from the held record at run time through a path the run is given, and asserts only that they agree, as a bool (`CHECK(agrees)`), so doctest's `values:` line prints `true` or `false` and no input. When the held input cannot be read the case FAILs (fail closed), never skips into a pass.
  - **A sanitizer program's report goes whole to the held directory.** The public record carries only its first line, `SAN #<bug> (-fsanitize=...): rc N`, and whether a report printed, never its frames.
  - **`Already written:`** is written in the bug's neutral register: what the code before the fix left on devices and in their clouds, with no mechanism and no input, weighed under D-WORKFLOW-215 before it is posted. A line that cannot be written that way is a question on #683 first.
  - The held three's `#585` lines stay with their records (`02:471`).
- **No guest, no image build, no fetch, no keyed call, nothing on a unit.** The host can build neither EmulationStation nor an image.
  - **Every guest half is `fix-walk-pending-image`**, the coordinator's, at the integration window, on the image that carries the fix, at 640x480 and 1280x800, in English and French where words show. `tools/frame-diff` runs against the accepted baseline for every page the fork works in. A stream with no surface says *none* and cites its bug's VM line. A visible change's flow step is named in its record (`es-ui-style-guide.md` § Keep the flow and its visual evidence together).
  - **Housekeeping.** `rm -rf` only as `"${VAR:?}"/...` or a literal path, in its own short command. The scratch is `/workspace/tmp/m6-t36/` after `df -i`. Every host compile is bracketed by START and END lines in `/workspace/tmp/m7-m6-host-coordination.txt` and runs only while M7's last event is a RETURN (`00:66`, the 23:02 rule).
- **A question for the coordinator is posted on #683**, never only on the session's screen. A turn ends on a post or a commit. If the harness refuses a stream's content, post the stream's number and stop that stream; the coordinator takes it (D-WORKFLOW-212). **The checkpoints S0 to S10 are posted on #683 one line each, as each lands:** the stream, the commit, the before and after lines.
- **Time to play.** Each stream's record says in one clause what it does to the two numbers. The ones that touch the launch path are S6 (`run()`'s wrap, every launch) and S5 if the held record's function runs per launch, which its record says; the rest touch per-label, per-texture or per-copy work, priced on the integration image (`03:26`: *"The two numbers were not measured this slice"*).

## S0 -- the floor cases no stream holds, and the carried harness (the distribution branch only; rulings 8 and 9)

- **Files:** none in the ES tree. On the distribution branch: `tools/t36-utils-resources-tests.cpp` (or sibling binaries in the same build script) with new `SPECS` in `tools/t36-extract.py` for their lifts; `tools/t36-build-tests.sh` (the `san()` function, the sibling binaries, `es-unit-tests` restored if the retry builds it); `stage-a/syntax-check.sh`, `stage-a/fakes/` and `stage-a/syntax-check.out`.
- **The floor cases** (the brief's floor table; `02:121-140` for their lines):
  - **3.6** (L-15): `preloadFileSystemCache` (`FileSystemUtil.cpp:1758-1798`; `:1773`, `:1775`, `:1788`, `:1797`) under ASan with `ASAN_OPTIONS=detect_stack_use_after_return=1`. The brief marks it a FAIL-at-pin candidate: a stack-use-after-return report.
  - **3.11** (L-10): one thread `initSVGFromMemory`, the main thread `setMaxSize` (`TextureData.cpp:615-645`, `:670-725` against `:92-195`), a `san()` TSan program with the `vlc/vlc.h` fake and `nanosvg` from the tree.
  - **3.12** (L-11): `TextureLoader` constructed, `paused` set, destroyed, with a timeout (`TextureDataManager.cpp:215-235`, `:252-253`, `:284`): the join does not return inside it at the pin, or does.
  - **3.17** (L-09): `sizeText` against the cache's last vertex (`Font.cpp:714-752`, `:1044-1078`); the extract `font_sizetext` exists (`t36-extract.py:31`) and no case reads it yet.
  - **3.22**: the ten `_("` shapes at their thresholds and the 12-hour switch read per call (`TimeUtil.cpp:514-588`), with `LocaleES` and `Settings` doubles, in a sibling binary that links `TimeUtil.cpp` (the main binary's `DateTime` double, `tools/t36-utils-resources-tests.cpp:41-43`). `00:57` says the thresholds are *"host-proven (case 3.22)"*; the binary holds no 3.22 (§ Figures not found, item 4).
  - **3.23**: `cleanupVRAM`'s eviction (`TextureDataManager.cpp:135-170`); the extract `cleanupvram` exists (`t36-extract.py:29`) and no case reads it yet.
  - **3.25**: the `san()` TSan programs over the cache's `shared_mutex` (`FileSystemUtil.cpp:331-332`), `ThreadPool.cpp:26`, `:84`, `:91`, `StringListLock.cpp` and `ConcurrentVector.h`, each program's first report line or none.
  - **3.8, re-written as the brief's positive** (ruling 4): `h = getHeight(); sizeText(<ASCII 32..126>); CHECK(getHeight() == h)` with `Font.cpp` linked over S0's FreeType and renderer fakes. The text case at `tools/t36-utils-resources-tests.cpp:207-214` stays beside it, its comment `:209` corrected to the erratum's direction (D-WORKFLOW-211: no assertion changed). If the fakes cannot load a face, the record says so and the errata's edit cites the text case alone.
  - **Not S0's:** 3.19 and 3.20 are held (`02:134-135`) and their cases are the held streams'; 3.15's race shape and the copy cases are S3's; 3.5's two rcs are re-run in S6.
- **Positives before:** each run against the pin and recorded FAIL or PASS as written, never as a defect when it passes. **A FAIL here on a line no ruling names is a new `bug` before any fix** (D-WORKFLOW-132): 3.6 (L-15), 3.11 (L-10), 3.12 (L-11) and 3.17 (L-09) are such lines, CONFIRMED by the seat (`04:21`) with no punch item in `05` (Draft notes, item 2). Each new bug's number is posted on #683 with S0's checkpoint, and S1 does not wait on its ruling.
- **3.4 marked `doctest::may_fail`** naming #1177 (the proposal above), its FAIL line at the pin quoted first.
- **Ruling 8's three, each a bracketed host compile:**
  - **`es-unit-tests`.** The tarball's sha256 against `rapidjson-1.1.0.tar.gz.sha256` beside it in `/workspace/cache/rocknix-sources/rapidjson/`; extracted to `/workspace/tmp/m6-t36/rj2/`; `document.h`'s sha256 prefix compared with the stage-C extract's `da02371e1747e869` (`stage-c/build-tests.out:3`), so the record says whether the bytes differ. Then the build, with the sources parsed from `es-app/tests/unit/CMakeLists.txt` as the script's header says (`t36-build-tests.sh:4-6`). At stage C the first error was *"`rapidjson/document.h:319:82: error: assignment of read-only member 'rapidjson::GenericStringRef<CharType>::length' [-Wtemplate-body]`"* (`02:440`). If the same line prints, the build is tried once with `-Wno-error`, as the ruling says, and that line is recorded. The bracket names `-Wtemplate-body`; if `-Wno-error` leaves it an error, the record says so and the lane posts on #683 before any other flag (Draft notes, item 4). A genuine incompatibility is `CANNOT` with the first error whole, and the three linked files (`StringUtil.cpp`, `TimeText.cpp`, `OfflineProxyUrl.cpp`) stand proven by the stand-in. A built `es-unit-tests` joins the `TOTAL:` line, and its line is quoted beside T34's and T35's `185 | 185 passed` (the brief's § 5 item 1).
  - **The four fakes.** The first errors name them (`stage-c/syntax-check-probe.out:3`, `:5-7`, `:13`, `:15-17`, `:20`): `SDL_opengl.h`, `SDL_WINDOWPOS_UNDEFINED` and `SDL_Surface`, `FT_New_Memory_Face`, `FT_Set_Pixel_Sizes` and `FT_Done_Face`, and `vlc/vlc.h`. The record says which fake carried which name.
  - **The renderers positive**, per renderer `.cpp`, with and without `-DUSE_OPENGLES_30`.
- **The record:**
  - `stage-e/s0-floor.txt` with the script's `TOTAL:` line, and `stage-e/s0-checks.txt` with the stand-in's 25 `rc` lines and the renderer positives.
  - `02` § The leads' floor rows moved from `pending stage C` to their run's `proved:` value through `tools/t36-tables.py`.
  - `02` § The runs with each run's exit, wall time, figure and *a FAIL would mean ...*.
  - `00` with the host-file START and END lines of each compile.
- **Commit:** `docs: T36 stage E S0: the floor cases no stream holds, each run at the pin; es-unit-tests retried; the stand-in's four fakes and the renderers positive (Refs #683)`.

## S1 -- PL-06 (#1359): a failed font atlas leaves a freed pointer in its list (High)

- **Ruling 1.** Rule 6; `04:39`, the seat's G-1, CONFIRMED at the pin.
- **Files:**
  - **Changed:** `resources/Font.cpp` `getTextureForNewGlyph`'s fresh-atlas path: the `new FontTexture` `:258`, the `push_back` `:268`, `findEmpty` `:270`, the `delete tex` `:274` and `tex_out = NULL` `:275` *(pin read; `05:68` puts the delete at `:275`)*.
  - **Read, not changed:** `getGlyph`'s call and its `tex == NULL` return (`:395-402`); `getGlyph`'s other early returns (`:377-381`, `:385-389`); the glyph `new` `:405` (G-2, the Backlog's).
- **Unit case, before (written first):** an ASan program with `Font.cpp` linked over S0's FreeType and renderer fakes, the fake returning a glyph taller than a fresh atlas can hold (`:260-261` size the atlas), then a second glyph lookup and the font's destruction. At the pin it reports a heap-use-after-free or a double free from `mTextures`; the report's first line is the before line.
- **The fix:** the new atlas joins `mTextures` only once `findEmpty` has placed the glyph (or is popped before the `delete`), so the list never holds a freed pointer.
- **Unit case, after:** `SAN <name> (-fsanitize=address): rc 0; no sanitizer report`. The stand-in over `Font.cpp` (S0's FreeType fake). The Font specs after `:277` updated if the line count moves (D-WORKFLOW-210).
- **Checks:** the stand-in PASS before the commit; `es-syntax-check` `CANNOT` with the host's line; the non-ASCII grep over the added lines prints nothing.
- **`Already written:`** #1359's: *"nothing is written to disk or a cloud; the defect is a live-session memory error in the font cache. Nothing inherited."*
- **French:** none (`Font.cpp` carries no `_("`).
- **Guest half:** none (#1359's VM line: *"a host AddressSanitizer case over the lifted atlas path"*).
- **Time to play:** a reordering on the atlas-creation path, which runs when a font's atlases are full; off the launch path.
- **The record:** `02` § The streams' S1 row (the ASan line before, the ES commit, the line after, `Already written:`, `proved: fix-unit-test`, guest half none, no patch); `stage-e/s1-before.txt`, `s1-after.txt`, `s1-checks.txt`.
- **Commits:** ES `fix: T36 stage E S1: a font's new glyph atlas joins its list only once the glyph fits, so a failed allocation leaves no freed pointer behind (Refs #683, #1359)`; distribution `docs: T36 stage E S1: the font atlas's dangling pointer, its ASan pair (Refs #683)`. A #585 line in `02` from the upstream comparison of `getTextureForNewGlyph` in ROCKNIX `f6c542872e` and batocera `b2ceb55a7e`.

## S2 -- PL-07 (#1360): a date format over 256 bytes overruns its stack buffer (High)

- **Ruling 1.** Rule 6; `04:41`, the seat's G-9, CONFIRMED at the pin.
- **Files:**
  - **Changed:** `utils/TimeUtil.cpp` the format function at `:415-508` (`char buf[256]`, `char* s = buf`, the `*s++` writes).
  - **Read, not changed:** the `_("` lines below it (`:517` to `:588`, `02:398-402`), which move by the fix's line delta and change no msgid; the parser `:275-335`, `:400-404` (G-10, S10's); `:19-111` (G-21, the Backlog's).
- **Unit case, before (written first):** in the sibling binary S0 links `TimeUtil.cpp` into, under `-fsanitize=address`, a format string whose expansion passes 256 bytes: a `stack-buffer-overflow` report at the pin. Beside it the control: a short format's output, kept byte for byte to compare after.
- **The fix:** every write into the buffer is bounded by its end (or the result is built in a `std::string`), and a short format's output is unchanged.
- **Unit case, after:** the over-long format with no sanitizer report; the control's bytes equal its before bytes; 3.22 (S0's) still PASS.
- **Checks:** the stand-in over `TimeUtil.cpp`; `es-syntax-check` `CANNOT`; the non-ASCII grep over the added lines.
- **`Already written:`** #1360's: *"nothing on disk; a live stack overflow driven by a format string. Nothing inherited."*
- **French:** none; `es-untranslated` re-run after, as at the pin.
- **Guest half:** none (#1360's VM line: *"a host case with an over-long format string ... ASan to confirm the overrun"*).
- **Time to play:** a bound check per byte of a formatted date; off the launch path.
- **The record:** `02` § The streams' S2 row; `stage-e/s2-before.txt`, `s2-after.txt`, `s2-checks.txt`. The sibling binary's line in the `TOTAL:` line, the binary count changed and said so.
- **Commits:** ES `fix: T36 stage E S2: a date format writes only inside its buffer (Refs #683, #1360)`; distribution `docs: T36 stage E S2: the date format's bound, its ASan pair (Refs #683)`. A #585 line in `02` from the upstream comparison.

## S3 -- PL-08 (#1361), PL-02 (#1363), PL-04 (#1365): copyFile and createDirectory (High; `FileSystemUtil.cpp`, first of four)

- **Rulings 1 and 7.** Rule 6; `04:42` (G-16, CONFIRMED at the pin), `05:23-31`, `:44-52`; `02:377-381`.
- **Files** (`utils/FileSystemUtil.cpp` only):
  - **Changed:** `copyFile` `:1467-1510` (the absent source `:1472-1474`, the parent made `:1476`, the opens `:1484`, `:1492`, the loop `:1500-1501`, the closes `:1503-1504`, the erases `:1506-1507`) and `createDirectory` `:1089-1120` (the existing-path guard `:1093-1095`, the `mkdir`s `:1105` and `:1116`, the parent's recursion `:1113`) *(pin read)*.
  - **Read, not changed:** `renameFile` `:1448-1464` (T21's `f7c16144d`, #1191) and `skipUtf8Bom` `:1369-1379` (T20's `d9afa5c7c`, #1177), never re-made.
- **Unit cases, before:**
  - **3.2's `copyFile` half** FAILs at the pin: `tools/t36-utils-resources-tests.cpp:92: ERROR: CHECK_FALSE( FileSystem::copyFile(s.at("nope2"), s.at("dst2")) ) is NOT correct!` / `values: CHECK_FALSE( true )` (`stage-c/build-tests.out:17-18`). 3.2 is split into its two halves in this stream's record commit (the proposal above).
  - **Written first, each FAIL at the pin:**
    - PL-08: a file and its hard link in the scratch (`Scratch`, `:47-58`); `copyFile(file, link)` and `copyFile(file, file)` return true and leave the source empty.
    - PL-02: `copyFile(<a file>, "/dev/full")` returns true over the short write (#1363's VM line), with `/dev/full` probed as 3.3 does (`:99-100`).
    - PL-04: `createDirectory(<an existing file>)` returns true (G-15, `04:54`); and the brief's 3.15 race, two threads creating one path over a stated number of iterations, either returning false while the directory exists (L-16). If no bound makes the race FAIL at the pin, the record says so.
  - **Controls:** 3.15 as written (`:154-160`, idempotent, parents made) PASS before and after.
- **The fix:**
  - **PL-08:** `copyFile` returns false, opening nothing for writing, when the destination exists and is the same file as the source by device and inode.
  - **PL-02:** it returns false over an absent source, and when a `fwrite` writes fewer bytes than were read or the destination's `fclose` fails.
  - **PL-04:** a failed `mkdir` whose path is now a directory (an uncached test) is success, and an existing path that is not a directory is false.
- **Its callers.** The lane lists the `copyFile` and `createDirectory` call lines that branch on the return (`git grep -n -E 'copyFile\(|createDirectory\(' 16dbac5211 -- es-app/src es-core/src`). Each one in another lane is named for its owner in `02` § The writes and reads, never edited (the brief's § 7 checkbox on L-03).
- **Unit cases, after:** the four written first PASS; 3.2's `copyFile` half PASS; 3.15 PASS; T34's L-09 answer (`02:228`: the `HttpReq.cpp:344`, `:479` copies) re-read against the changed erases and said to stand or not.
- **Checks:** the stand-in over `FileSystemUtil.cpp`; `es-syntax-check` `CANNOT`; the non-ASCII grep over the added lines (upstream's `:225`, `:287`, `:718` excluded by construction).
- **`Already written:`**
  - **PL-08,** #1361's: *"the defect is in what the copy does at run time, not a format on disk. A device that already ran a same-path copy has lost that file -- no migration recovers it; the fix is forward-only and the guard prevents recurrence."*
  - **PL-02,** #1363's: *"a `copyFile` that reported success over a no-op left the destination absent or short; a device that ran it has whatever it has -- the fix is forward (correct return), and callers that trusted the return are their owners'. Nothing this fix rewrites."*
  - **PL-04,** #1365's: *"nothing on disk; a transient wrong return. Nothing inherited."*
- **French:** none.
- **Guest half:** none (the three bugs' VM lines: host cases).
- **Time to play:** one `stat` of an existing destination per copy, and one uncached directory test after a failed `mkdir`; off the launch path.
- **The record:** `02` § The streams' S3 row; `stage-e/s3-before.txt`, `s3-after.txt`, `s3-checks.txt`.
- **Commits:** ES `fix: T36 stage E S3: copyFile refuses to copy a file onto itself and reports an absent source or a short write, and createDirectory accepts a directory another creator made and refuses a file (Refs #683, #1361, #1363, #1365)`; distribution `docs: T36 stage E S3: copyFile and createDirectory, their before and after lines, 3.2 split (Refs #683)`. #585 lines for the three from the upstream comparison.

## S4 -- PL-03 (#1364), PL-05 (#1366): a removed path read as present, and the thumbnail reads (Medium; `FileSystemUtil.cpp`, second of four)

- **Rulings 1 and 7.** Rule 6; L-19 (`02:220-224`), `05:33-42`, `:54-62`; #1263's cache half (ruling (i)); ruling (h).
- **Files:**
  - **Changed:** `utils/FileSystemUtil.cpp` `removeFile` `:1059-1087` (the erase `:1067`, `isDirectory` `:1080`, `rmdir` `:1081`, `unlink` `:1084`); `resources/TextureData.cpp` `loadFromVideo`'s reads `:339` and `:410` (`05:61`), and `:331` if its record shows it is needed.
  - **Read, not changed:** the cache `FileSystemUtil.cpp:48-341`; `removeFile`'s guard `:1063-1065` (G-14, S10's); `TextureData.cpp:336` (the expiry's `removeFile`), `:341` (`createDirectory`), `:402` (libvlc's snapshot).
- **Unit cases, before:**
  - **3.26** FAILs at the pin: `tools/t36-utils-resources-tests.cpp:126: ERROR: CHECK( FileSystem::exists(p) == false ) is NOT correct!` / `values: CHECK( true == false )` (`stage-c/build-tests.out:24-25`).
  - **3.13** PASS (the control, `:144-152`).
  - **Written first: PL-05's case.** The two reads lifted (a new spec over `TextureData.cpp:322-417`) or `TextureData.cpp` linked over S0's `vlc` fake. A snapshot written outside the cache after a cached miss reads absent at `:410`, and an expired thumbnail removed and asked again reads present at `:339`: both FAIL at the pin.
- **The fix:**
  - **PL-03:** `removeFile` removes the path first (`rmdir` or `unlink`, chosen by an uncached directory test) and erases its entry after, so nothing re-reads the deleted path into the cache between.
  - **PL-05:** `exists(localFile, false)` at `:339` and `:410`.
  - G-11's in-flight stat after a reset stays the remaining race, recorded (`05:39`, `04:50`).
- **Unit cases, after:**
  - 3.26 PASS; PL-05's case PASS; 3.13 PASS.
  - **T35's 3.11 re-run unchanged** from T35's tip (ruling (h)), its line quoted. At stage C it printed `RUN window-input-tests: rc 0; [doctest] test cases: 31 | 31 passed | 0 failed | 0 skipped [doctest] assertions: 88 | 87 passed | 1 failed |` at ES `b7fdb3a24` (`stage-c/t35-311-rerun.out:88`; `02:438`).
  - `removeFile`'s signature unchanged (ruling (g)).
- **Checks:** the stand-in over `FileSystemUtil.cpp` and `TextureData.cpp` (S0's `vlc` fake); `es-syntax-check` `CANNOT`; the non-ASCII grep over the added lines.
- **`Already written:`**
  - **PL-03,** #1364's: *"the stale `true` lives only in the in-memory cache of a running session (never on disk), and ES resets after a game exit (`FileData.cpp:1113`). Nothing inherited on disk; the fix changes only in-session behaviour."*
  - **PL-05,** #1366's: *"the stale answers are in-session cache only; nothing on disk."* The draft adds, for the lane to confirm or correct: a thumbnail an earlier session removed at `:336` and did not re-extract is absent on the card, and the fixed read at `:339` sees it absent and extracts it again, so the answer is *read both*.
- **French:** none.
- **Guest half:** `fix-walk-pending-image`: #1263's frame (the MANUAL row, or a video thumbnail after its expiry) on a guest with scraped media. G-03 was not stageable on this slice's guest (`00:56`, *"the guest ships no game with a manual path"*), so it stays the open item under #1263's picture checkbox (ruling (i)).
- **Time to play:** the same syscalls in `removeFile` in a new order, and two `stat`s per video-thumbnail lookup on the texture loader's thread; off the launch path, priced with G-05's scroll on the integration image.
- **The record:** `02` § The streams' S4 row; `stage-e/s4-before.txt`, `s4-after.txt`, `s4-checks.txt`; #1263 gets a comment with `fixed-at-es` at the hand-back (T32's bug).
- **Commits:** ES `fix: T36 stage E S4: removeFile removes a path before it forgets it, so a deleted file no longer reads present, and the video thumbnail reads ask the disk (Refs #683, #1364, #1366)`; distribution `docs: T36 stage E S4: removeFile's order and the thumbnail reads, 3.26's pair, T35's 3.11 re-run (Refs #683)`. The #585 line for L-19 as `02:470` has it (ROCKNIX and batocera both, `02:223`), and PL-05's from its comparison.

## S5 -- #1370 (`FileSystemUtil.cpp`, third of four)

- **Rulings 6 and 7.** Applied over S3 and S4 in the same file.
- **Files:** `utils/FileSystemUtil.cpp` only.
- **The fix:** the contained fix the held record describes.
- **Unit case:** named `#1370`, its input and its expected result read from the held record at run time, under § The rules every stream keeps' held-stream bullet. It is seen to FAIL at the pin before the fix and to PASS after; the public lines are the doctest summary, the case's one bool line and, for a sanitizer program, its first line only.
- **Checks:** the stand-in over `FileSystemUtil.cpp`; `es-syntax-check` `CANNOT`; the non-ASCII grep over the added lines.
- **`Already written:`** written by the lane in the neutral register (the held-stream bullet).
- **French:** if the held record's fix changes a player sentence, its French in the same commit; none is expected.
- **Guest half:** whatever the held record names, at the integration window, its frames and journal lines filed in the held directory and one neutral line in `02`; or none.
- **Time to play:** one clause in the record, from the held record's own reading of where the function runs.
- **The record:** `02` § The streams' S5 row with the neutral lines only, `proved: fix-unit-test`; `stage-e/s5-before.txt`, `s5-after.txt`, `s5-checks.txt` with the neutral lines only. The #585 line stays with the record.
- **Commits:** ES `fix: T36 stage E S5: utils/FileSystemUtil.cpp, the contained fix the held record describes (Refs #683, #1370)`; distribution `docs: T36 stage E S5: #1370's neutral lines (Refs #683)`.

## S6 -- #1371 (`FileSystemUtil.cpp`, fourth of four), with ruling 5's quoting gap (`Platform.cpp:162`)

- **Rulings 5, 6 and 7.** The held half is applied over S5 in `FileSystemUtil.cpp`. The public half is in `Platform.cpp`, which no other stream touches.
- **Files:**
  - **Changed:** `utils/FileSystemUtil.cpp` (the held half); `utils/Platform.cpp` `ProcessStartInfo::run`'s wrap `:162-168` (the log path interpolated at `:162`, `:163-164` the log-off variant).
  - **Read, not changed:** `Platform.cpp:891-905` (`GetShOutput`, T26's `a5d2d3756`, #1225, never re-made); `StringUtil.cpp:426-444` (`shellQuote`, the contract 3.18 asserts, `tools/t36-utils-resources-tests.cpp:162-168`); `run()`'s callers `main.cpp:540`, `InputManager.cpp:1272`, `Scripting.cpp:133`, `:142`, `:45` and the launch `FileData.cpp:1100-1103` (`02:309`, other lanes' files).
- **The held half:** the contained fix the held record describes; its unit case named `#1371`, under the held-stream bullet.
- **The public half, unit case before (written first):** the `run_wrap` extract (`t36-extract.py:20`) assembled as `run()` assembles it and run by the host's shell, with a log directory whose name holds a space and a `<cmd>` of two simple commands each writing to stderr. At the pin the first command's stderr escapes the log and the path splits at the space: FAIL. The host's `sh` is `/usr/bin/dash` (`stage-a/runs.out:222`) and the image's is bash (`02:451`, G-07); the case runs under each shell the host has and the record names which.
- **The public half's fix:** the log path is passed through `Utils::String::shellQuote`, and the command is grouped so its `2>` covers every simple command in it; the `head -300`, the exit-status relay and `waitForExit` are unchanged (ruling 5).
- **Unit cases, after:** the held case PASS (neutral lines); the public case PASS under each shell; **3.5's two literals re-run unchanged** and their rcs quoted beside the stage-A lines `seq 400 rc=0` and `seq 200000 rc=141` (`stage-a/runs.out:219-220`). The `run_wrap` spec's first-line string and the `quites`, `runsys` and `gsh` ranges updated (D-WORKFLOW-210); 3.7, 3.9 and 3.24 PASS unchanged.
- **Checks:** the stand-in over `FileSystemUtil.cpp` and `Platform.cpp`; `es-syntax-check` `CANNOT`; the non-ASCII grep over both files' added lines.
- **`Already written:`** the held half in the neutral register; the public half: nothing inherited -- the wrap is built per launch and kept nowhere, and the two launch logs (`es_launch_stdout.log`, `es_launch_stderr.log`, `:162`) are rewritten by the next launch.
- **French:** none.
- **Guest half:** `fix-walk-pending-image` for the public half: a launch on the integration image with the log directory as shipped, the two logs read afterwards, and the launch's stderr in `es_launch_stderr.log`. The held half's guest step as the held record names it, filed in the held directory.
- **Time to play:** on the launch path. The wrap gains a quoted path and a grouping, one shell parse per launch, priced on the integration image's launch-to-first-frame number.
- **The record:** `02` § The streams' S6 row, public lines whole and the held half's neutral; `stage-e/s6-before.txt`, `s6-after.txt`, `s6-checks.txt`.
- **Commits:** ES `fix: T36 stage E S6: utils/FileSystemUtil.cpp, the contained fix the held record describes; run()'s launch log path is quoted and its redirection covers the whole command (Refs #683, #1371)`; distribution `docs: T36 stage E S6: #1371's neutral lines and run()'s quoting pair (Refs #683)`. A #585 line for the public half from the upstream comparison of `run()`; the held half's stays with its record.

## S7 -- #1369 (`ZipFile.cpp`)

- **Ruling 6.** Independent of every other stream.
- **Files:** `utils/ZipFile.cpp` only. #1369's public body names its caller in `es-app/src/ApiSystem.cpp`; if the held record's fix needs a line there, it is `stage-e/s7-caller.patch` for its owner, proven on a scratch copy read by `git show` and named under merge debt (the owner `[coordinator to confirm]`).
- **The fix:** the contained fix the held record describes.
- **Unit case:** named `#1369`, under the held-stream bullet. Linking `ZipFile.cpp` collides with the main binary's `computeCRC` double (`tools/t36-utils-resources-tests.cpp:38-40`), so the case lives in a sibling binary in the same script, or the double is dropped in this stream's record commit with the setup line named (D-WORKFLOW-211).
- **Checks:** the stand-in over `ZipFile.cpp`; `es-syntax-check` `CANNOT`; the non-ASCII grep over the added lines. `utils/zip_file.hpp` is read only where the held record reaches it and is never edited (`02:414`, #256's vendored-header bucket).
- **`Already written:`** in the neutral register.
- **French:** none expected.
- **Guest half:** as the held record names it, filed in the held directory; or none.
- **Time to play:** off the launch path (an archive extraction).
- **The record:** `02` § The streams' S7 row, neutral; `stage-e/s7-before.txt`, `s7-after.txt`, `s7-checks.txt`.
- **Commits:** ES `fix: T36 stage E S7: utils/ZipFile.cpp, the contained fix the held record describes (Refs #683, #1369)`; distribution `docs: T36 stage E S7: #1369's neutral lines (Refs #683)`.

## S8 -- PL-01 (#1362): toUpper and toLower fold a multi-byte codepoint byte by byte (Medium)

- **Ruling 1.** Rule 6; L-01 and G-8 (`04:48`, folded into PL-01).
- **Files:**
  - **Changed:** `utils/StringUtil.cpp`: `toUpper`'s `+=` `:357-362` and `toLower`'s `:398-403` (against `:352-356`, `:393-397`), the tables `:30` (`unicode_uppers`) and `:76`, `:93`, `:153`, `:170`, the `bsearch` lookup `:105-108`, the dotless `ı` `:184-188` (`02:92`, `05:17`).
  - **Read, not changed:** `startsWithIgnoreCase` `:202-210` and `proper` `:213-218` (S10's G-6 and G-7); `maskSecrets` `:446-804` (ruling 5).
- **Unit cases, before:**
  - **3.1** FAILs at the pin: `tools/t36-utils-resources-tests.cpp:82: ERROR: CHECK( String::toUpper("\xE1\xBA\xA1") == "\xE1\xBA\xA0" ) is NOT correct!` and `:83: ERROR: CHECK( String::toLower("\xEF\xBC\xA1") == "\xEF\xBD\x81" ) is NOT correct!` (`stage-c/build-tests.out:13-14`).
  - **Written first, each FAIL at the pin:** G-8's two -- a lookup that depends on the table's order (or a case asserting the table is sorted for `bsearch`), and `toUpper` of `ı` (U+0131) giving the one-byte `I`.
  - **The control:** a two-byte French pair (`é`/`É`) PASS before and after (the brief's floor table, 3.1).
- **The fix:** each codepoint is decoded whole, mapped, and re-encoded through the encoder its result needs, over a table the lookup can search.
- **Unit cases, after:** 3.1, G-8's two and the control PASS. If S0 built `es-unit-tests`, its `MaskSecretsTests` and the other cases over `StringUtil.cpp` re-run as the regression net, their line quoted.
- **Checks:** the stand-in over `StringUtil.cpp`; `es-syntax-check` `CANNOT`; the non-ASCII grep over the added lines (upstream's `:1406-1407` and `StringUtil.h:62-68` excluded by construction). A test literal for a codepoint is written as `\x` escapes, as 3.1's are.
- **`Already written:`** #1362's: *"case folding runs on in-memory strings; nothing inherited on disk."* **Argued, not assumed** (`upgrade-and-install.md`): the lane lists the callers whose folded result is written to a file -- a collection or system name, a sort key, a settings key -- with `git grep -n -E 'to(Upper|Lower)\(' 16dbac5211 -- es-app/src es-core/src`, and says for each whether a three-byte codepoint's old fold was stored. A stored one is *read both*.
- **French:** no msgid. A French string with only two-byte letters folds as before (the control).
- **Guest half:** `fix-walk-pending-image`: a frame of a label a theme or a component upper-cases (ruling (f): the component's uppercase option calls `toUpper`) carrying a three-byte codepoint, at 640x480 and 1280x800, in English and French. The lane names the surface from the guest's theme, or records the frame `CANNOT` with the reason.
- **Time to play:** a decode and an encode per codepoint where an upper-case label's text is built; off the launch path, priced on the integration image.
- **The record:** `02` § The streams' S8 row; `stage-e/s8-before.txt`, `s8-after.txt`, `s8-checks.txt`.
- **Commits:** ES `fix: T36 stage E S8: toUpper and toLower fold a whole codepoint, from a table their lookup can search (Refs #683, #1362)`; distribution `docs: T36 stage E S8: the case folding, 3.1's pair and G-8's two (Refs #683)`. A #585 line from the upstream comparison.

## S9 -- PL-09 (#1367): loadFromPdf reports failure after a page loaded (Medium)

- **Ruling 1.** Rule 6; `04:40`, the seat's G-4, CONFIRMED at the pin. Applied over S4 in `TextureData.cpp`, a separate function.
- **Files:**
  - **Changed:** `resources/TextureData.cpp` `loadFromPdf`: `retval` `:425`, the call `:441`, the return `:444` *(pin read)*.
  - **Read, not changed:** `PdfHandler->extractPdfImages` `:434`; the temporary page's `removeFile` `:439` (after S4, removed before it is forgotten).
- **Unit case, before (written first):** `TextureData.cpp` linked over S0's `vlc` fake, with a `PdfHandler` double returning one small image file in the scratch: `loadFromPdf` returns false after the page loaded: FAIL at the pin. **The control:** no page extracted, false before and after.
- **The fix:** `retval` takes `initImageFromMemory`'s result.
- **Unit case, after:** PASS; the control PASS.
- **Checks:** the stand-in over `TextureData.cpp`; `es-syntax-check` `CANNOT`; the non-ASCII grep over the added lines.
- **`Already written:`** #1367's: *"nothing on disk; a wrong return. A PDF that failed to display did so at view time; the fix is forward. Nothing inherited."*
- **French:** none.
- **Guest half:** `fix-walk-pending-image`: a game's PDF manual page opened on a guest that ships one, which this slice's guest did not (`00:56`); the open item beside S4's.
- **Time to play:** none; a return value.
- **The record:** `02` § The streams' S9 row; `stage-e/s9-before.txt`, `s9-after.txt`, `s9-checks.txt`.
- **Commits:** ES `fix: T36 stage E S9: loadFromPdf reports the page it loaded (Refs #683, #1367)`; distribution `docs: T36 stage E S9: loadFromPdf's return, its pair (Refs #683)`. A #585 line from the upstream comparison.

## S10 -- PL-10 (#1368)'s Resolved set: G-6, G-7, G-10, G-14, G-20, G-3 (Medium)

- **Ruling 2.** Rule 6, *"each a contained guard/bound/return"* (`05:110`). Runs last, after every stream whose file it shares.
- **Files, each changed after the stream named** (lines at the pin, from `04`; the lane re-reads them at its tip and names the moved lines):
  - `utils/StringUtil.cpp`, after S8: **G-6** `startsWithIgnoreCase` `:202-210`, `:1032-1042`; **G-7** `proper` `:213-218`, `:1144-1149` (`04:46-47`).
  - `utils/TimeUtil.cpp`, after S2: **G-10** the date parser `:275-335`, `:400-404` (`04:49`).
  - `utils/FileSystemUtil.cpp`, after S6: **G-14** `removeFile`'s guard `:1063-1065` with `:146` (`04:53`).
  - `resources/TextureData.cpp`, after S4 and S9: **G-20** the SVG path `:115-198`, `:205-206` (`04:58`).
  - `resources/Font.cpp`, after S1: **G-3** `rebuildTextures` `:376-388`, `:442-454` (`04:44`).
- **Unit cases, before (written first, each FAIL at the pin, in `04`'s words):**
  - **G-6:** *"`startsWithIgnoreCase("abc","abc")` advances past both terminators"*: an ASan read past the string at the pin.
  - **G-7:** *"`proper` can split a 4-byte UTF-8 char -> `length()-2` underflow into the 4-byte decoder"*: an input whose cut falls inside a four-byte character, an ASan report at the pin.
  - **G-10:** *"literals advance `s` not `parsedChars` -> day read past the input"*: in S2's sibling binary, a format with a literal over a short input, an ASan report at the pin.
  - **G-14:** *"`removeFile` of a broken symlink: the following `stat64` fails, returns true without unlinking"*: a dangling link in the scratch; `removeFile` returns true and `lstat` still finds the link at the pin.
  - **G-20:** *"SVG parsed dimensions reach unchecked `w*h*4` allocation and narrowing to int"*: an SVG whose dimensions overflow the product, under `-fsanitize=address,undefined`, a report at the pin.
  - **G-3:** *"`rebuildTextures` may deref a null face / ignore `FT_Load_Char` failure"*: S0's FreeType fake returning no face, or an error, for a cached glyph, then `reload()`; a null dereference at the pin under ASan.
  - A finding whose case cannot be made to FAIL at the pin is recorded with its stub's line, its fix waits, and the question goes on #683.
- **The fix:** for each, a guard, a bound or a return at its lines: the two string helpers stop at the string's end, the parser at its input's, `removeFile`'s guard sees a link the stat cannot follow, the SVG's product is checked before the allocation, and the rebuild skips a glyph whose face or load failed.
- **Unit cases, after:** the six PASS, each sanitizer program `rc 0; no sanitizer report`; 3.26 (S4's) and S3's cases still PASS; the Font specs updated (D-WORKFLOW-210).
- **Checks:** the stand-in over the five `.cpp`; `es-syntax-check` `CANNOT`; the non-ASCII grep over each file's added lines.
- **`Already written:`** #1368's: *"each is a live code defect; none writes a format to disk this fix must migrate. Per-finding `Already written:` lines at the stream."* The per-finding lines go into #1368's edited body. For G-14 the draft proposes: a dangling link an earlier `removeFile` reported removed is still on the card, and the fixed `removeFile` unlinks it the next time it is asked -- *read both*.
- **French:** none.
- **Guest half:** none (#1368's VM line: *"a host unit/ASan case per finding"*).
- **Time to play:** a bound per call in two string helpers that run per label and per comparison, and a check per SVG load; off the launch path, priced on the integration image.
- **#1368 and #1358.** #1368's body is edited to the six with their per-finding lines and the Backlog's number (ruling 2), and #1358's PL-10 checkbox the same way, both before this stream's checkpoint is posted.
- **The record:** `02` § The streams' S10 row (six pairs); `stage-e/s10-before.txt`, `s10-after.txt`, `s10-checks.txt`.
- **Commits:** ES `fix: T36 stage E S10: string helpers and the date parser stop at their input's end, removeFile unlinks a broken link, an SVG's size is checked before it is allocated, and a glyph rebuild skips a missing face (Refs #683, #1368)`; distribution `docs: T36 stage E S10: the six G-items' pairs, #1368 edited to the Resolved set (Refs #683)`. #585 lines for the six from the upstream comparison.

## Recorded, no stream

These are ruled above or carried by the brief, and listed here so the Phase 7 gate has every row:

- **L-04:** held for #1186 (ruling 3); 3.3 stays its text record; the coordinator's pointer on #1186.
- **L-08, L-13:** the coordinator's rule errata (ruling 4, `kit/t36-rule-errata.md`); `02` § The structure records them as *the coordinator's, at acceptance*. G-19 (`04:57`, `run()`'s `WEXITSTATUS` of a signalled child, `runSystemCommand`'s interrupted `waitpid`) is recorded with L-13.
- **L-05, L-14:** recorded as the seat left them (ruling 5); L-05's quoting is S6's; L-14's mask shapes and G-17 recorded, with 3.10 (`tools/t36-utils-resources-tests.cpp:133-142`) left as the record of the pin's reach.
- **PL-10's five:** G-2, G-5, G-12, G-13 and G-21 deferred to `#<Backlog>` (ruling 2).
- **G-11:** PL-03's remaining race, recorded with PL-03 (`05:39`).
- **The collisions:** L-02 (T20's `d9afa5c7c`, #1177, 3.4 the control), L-03's `renameFile` half (T21's `f7c16144d`, #1191, 3.2's half the control), L-06 (T26's `a5d2d3756`, #1225, 3.9 the control), T21's `utils/DownloadFile.{cpp,h}` under the glob (ruling (b)) (`05:115-121`, `02:426-431`).
- **G-08:** `Renderer_GL21`, `Renderer_GLES10` and `Renderer_GLES20` are compiled by no image, a structure fact (`02:411`).
- **#1263:** its picture checkbox stays open (ruling (i)); S4 is its cache half.
- **Leads without a punch item, for the coordinator** (Draft notes, item 2): L-07 (3.16), L-09 (3.17), L-10 (3.11), L-11 (3.12), L-15 (3.6) and L-18 (3.24) are CONFIRMED by the seat (`04:21`) and carry no item in `05`, and 3.21 (R4 item 17, `.//a.png`) asserts a wrong result at the pin with no item. L-17 is `CANNOT-TELL` (`04:23`). S0 runs the unwritten ones; a FAIL there is a new `bug` before any fix (D-WORKFLOW-132).
- **Withdrawn:** none.

## The order

The streams run S0 to S10, one commit each on the ES branch in that order (S0 on the distribution branch only), as serial commits with **no rebase across streams**. Every stream's unit cases are written and seen to FAIL at the pin before its fix (S0's are run at the pin and recorded either way). The checkpoint lines on #683 keep the stream numbers.

- **S0:** the distribution branch only: the floor, the harness, ruling 8's three.
- **S1:** `resources/Font.cpp` (`getTextureForNewGlyph`). High.
- **S2:** `utils/TimeUtil.cpp` (`:415-508`). High.
- **S3:** `utils/FileSystemUtil.cpp` (`createDirectory` `:1089-1120`, `copyFile` `:1467-1510`). High (PL-08).
- **S4:** `utils/FileSystemUtil.cpp` (`removeFile` `:1059-1087`); `resources/TextureData.cpp` (`:339`, `:410`).
- **S5:** `utils/FileSystemUtil.cpp` (#1370).
- **S6:** `utils/FileSystemUtil.cpp` (#1371); `utils/Platform.cpp` (`:162-168`).
- **S7:** `utils/ZipFile.cpp` (#1369); a `stage-e/` patch only if the held record needs a caller's line.
- **S8:** `utils/StringUtil.cpp` (the case folding).
- **S9:** `resources/TextureData.cpp` (`loadFromPdf` `:423-445`).
- **S10:** `utils/StringUtil.cpp`, `utils/TimeUtil.cpp`, `utils/FileSystemUtil.cpp`, `resources/TextureData.cpp`, `resources/Font.cpp` (the six G-items).

**By file, the streams that touch it, in order** (the claim the lane checks against each commit's `git show --stat`):

| File | Streams, in order |
| --- | --- |
| `utils/FileSystemUtil.cpp` | S3, S4, S5, S6 (ruling 7), then S10 (G-14) |
| `resources/TextureData.cpp` | S4, S9, S10 (G-20) |
| `resources/Font.cpp` | S1, S10 (G-3) |
| `utils/TimeUtil.cpp` | S2, S10 (G-10) |
| `utils/StringUtil.cpp` | S8, S10 (G-6, G-7) |
| `utils/Platform.cpp` | S6 |
| `utils/ZipFile.cpp` | S7 |

Ruling 7 names `FileSystemUtil.cpp` as the one shared file; under ruling 2's one stream for PL-10, S10 shares five (Draft notes, item 1). Each stream re-reads its lines at its own tip, so a line a predecessor moved is named as moved, never guessed.

## The record

As T35's (`t35-streams.md` § The record):

- **`02` § The streams:** one row per stream. Each row has the positive before, the ES commit, the positive after, the `Already written:` answer, `proved: fix-unit-test`, the guest half (`fix-walk-pending-image` or *none* with the bug's VM line), and the patches and the collisions named. The held streams' rows carry the neutral lines only.
- **`02` § Positives:** filled from the `sN-before` and `sN-after` lines. Every count is a tool's line.
- **`05`'s gate table and `punch_index`:** moved together at Phase 7 (`05:141-222`).
  - **Fixed, by stream:** PL-06 by S1; PL-07 by S2; PL-02, PL-04, PL-08 by S3; PL-03, PL-05 by S4; PL-01 by S8; PL-09 by S9; PL-10's six by S10.
  - **Deferred:** PL-10's five to `#<Backlog>`; L-04 to #1186. PL-10 carries both outcomes; if `tools/lint-audit-artifacts` takes one outcome per item, its evidence cell names the split (`[coordinator to confirm]`, Draft notes, item 7).
  - **The held table** (`05:133-139`): #1369 by S7, #1370 by S5, #1371 by S6, the neutral lines only.
  - **Recorded:** the rest, as above, with their reasons.
- **The tools.** The extractor's specs before and after (D-WORKFLOW-210); the sibling binaries and `san()` programs named in `t36-build-tests.sh`'s header. The #585 lines in `02` § The #585 lines owed, each with its upstream comparison (ROCKNIX `f6c542872e`, batocera `b2ceb55a7e`), the held three's kept with their records.
- **`00`.** Its stage-E entries name the build script's command and each sanitizer program's, and the host-file START and END lines for each compile.
- **The checks.**
  - `tools/lint-audit-artifacts docs/audits/2026_10_31-epic-m6-es-core-utils-resources/` PASS on its default `resolution` phase, and with `--issue 1358`.
  - `tools/box-check --issue 1358` 0 fail, and the same on #1359 to #1371 and on any bug S0 files.
  - `tools/register-check` before each record commit.

## The hand-back

After stage E's record, as the brief's § 10 and T35's:

- **One hand-back comment on #683** names **both tips**: the distribution's, and the ES tip of `feature/m6-es-core-utils-resources-683` on `origin`. The lane writes `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` into #683's body, then says it is idle.
- **The `fixed-at-es` header** goes in `05` and in the body of each bug the streams fixed: #1359 to #1368, #1369 to #1371, and any bug S0 files. A comment carrying it goes on #1263 (T32's bug). The bugs stay open until the pin moves on `next`.
- **The lines, quoted from the script's own output:**
  - The `TOTAL:` line, with 0 failed in every binary's test-case summary and `utils-resources-tests` among the binaries; the include order that linked the real `FileSystemUtil.cpp` (`-I <build>/x -I <W>/es-core/src -I <W>/external`, `stage-c/build-tests.out:5`) named.
  - The `may_fail` count beside it (3.4 and 3.2's `renameFile` half, if the proposal is ruled), with the note that doctest's assertion summary counts those assertions as failed (T34's acceptance erratum 9).
  - Every `SAN` line at `rc 0; no sanitizer report`; the held programs' first lines only.
  - The FAIL-at-pin lines beside their PASS lines: 3.1, 3.2's `copyFile` half, 3.26 and every case a stream wrote first; 3.4 and 3.2's `renameFile` half still FAIL, with their owners.
  - `es-unit-tests`' line, or its `CANNOT` with the first error whole (ruling 8).
  - **T35's 3.11 re-run** once more from T35's tip (ruling (h), `02:239`), named with the time and the tip.
- **The stand-in:** one line per edited `.cpp`, and the 25-file line re-run at the tip with the renderer positives. Each source's `es-syntax-check` is `CANNOT` with the host's line.
- **The checkers:**
  - `tools/es-untranslated`'s line with `0 without`.
  - `tools/es-menu-map-check --es-src <W> --ref <tip>` with its full line; at the pin `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` (`stage-a/runs.out:226`). The slice holds no menu, so no row moves (the brief's § 9).
  - **The five on the distribution branch**, each with its own `rc=` line: `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test`.
  - **The ES fork's `.githooks/pre-push-test`** at the tip.
  - `tools/lint-audit-artifacts` on the default phase and with `--issue 1358`; `tools/box-check --issue 1358`.
- **The collisions:**
  - **The fakes' double** (ruling (g)): `git diff 16dbac5211 <tip> -- es-core/src/utils/FileSystemUtil.h` showing none of the four signatures changed, or naming the change and its three binaries (`proxycards-tests`, `jobs-tests`, `bookkeeper-tests`).
  - **T20's, T21's and T26's fixes** (ruling (d)): `git -C <W> show <hash> -- <file>` applied with `patch --dry-run` over T36's ES tip for `d9afa5c7c` (`FileSystemUtil.cpp`, +4), `f7c16144d` (`FileSystemUtil.cpp` 17 lines, `DownloadFile.{cpp,h}` 61 and 29) and `a5d2d3756` (`Platform.cpp`, 15+/5-) (this draft's `git show --stat`), each hunk's result quoted. S3 and S6 sit beside them in the same files.
  - **T21's `utils/DownloadFile.{cpp,h}`** under the glob: named, not read.
  - **T34's and T35's ES tips' delta inside the 58:** `git -C <W> diff --stat 16dbac5211 <tip> -- es-core/src/utils es-core/src/resources es-core/src/renderers` for `52f0ff5128` and `b7fdb3a24`; both printed nothing at this draft's read.
- **The merge debt, by file:** `FileSystemUtil.cpp` (T20's and T21's hunks over S3 to S6 and S10); `Platform.cpp` (T26's over S6); any `stage-e/` patch (S7's caller, if made); the two rule errata (the coordinator's sweep, ruling 4); #1186's pointer (ruling 3); the Backlog (ruling 2).
- **The guest halves owed at the integration window, every one `fix-walk-pending-image`:** S4 (#1263's frame on a media-scraped guest), S6 (a launch's logs), S8 (an upper-cased three-byte label), S9 (a PDF manual page), and the held streams' steps as their records name them. With the flow references each changed screen updates (`es-ui-style-guide.md`).
- **The `#585` lines:** one per upstream-carried defect a stream closed, in `02` § The #585 lines owed, in the lane's shape, never sent (D-WORKFLOW-164/165); the three never posted from the collisions (T20 `02:337`, #1191 `:21`, T26 `02:819`; `02:465-468`) named for the coordinator; the held three's kept with their records.
- **The retro.** `docs/retros/<date>-m6-es-core-utils-resources.md`, posted on #683 with its heading's time from `date -u` in the posting command, says what the slice did to the two time-to-play numbers (`run()`'s wrap and `runSystemCommand`'s blocking priced from the guest, or `CANNOT` with the harness's reason, citing `docs/vm-qa-log.md`), with each stream's clause carried, and what T37 inherits.
- **The shared host file's RETURN line.**

## What T37 inherits

The brief's § 5 item 3 lists it, and `02` § What T37 inherits is written at the hand-back (`02:473-475`): the provenance table; the file-cache table; the texture-and-font table; the processes table; the writes table; the `utils-resources-tests` build recipe (the doubles, the extracts, the fakes the first errors forced, the include order that links the real `FileSystemUtil.cpp`); the stand-in's rc per file over the 25 with the renderer positives and the branches it did not parse; the `exists` cache's answer for T35's 3.11 and for #1263; the rule errata L-08 and L-13 as the coordinator dispositioned them; and the collision list.

Stage E adds to it in the retro, not here: the extractor's `SPECS` at the tip; the `san()` programs and the sibling binaries; `removeFile`'s new order and the uncached thumbnail reads (for any slice that reads the cache after a delete); `copyFile`'s and `createDirectory`'s new returns and their branching callers by owner; and the held cases' shape (a case named by its bug, reading its inputs from a held record).

## What never runs here

- **Tools beyond the host's:** an image build; a compiler beyond the host's `g++` for the unit targets, the sanitizer programs and the stand-in; a guest; a fetch; a keyed council call; anything on a unit.
- **A change outside the 58 and the audit folder.** The exceptions are a `stage-e/` patch a held record needs and the French catalog for a changed sentence, of which none is expected.
- **These paths:** `es-core/src/components/**`; `Window.*`, `Log.*`, `InputManager.*`, `Scripting.*`, `ImageIO.*`, `es-core/CMakeLists.txt`; `utils/AtomicFileUtil.*`, `utils/DownloadFile.*`, `HttpReq.*`, `Settings.*`, `SystemConf.*`, `CloudText.*`; `tests/app-unit/fakes/`; any `es-app/src` file beyond a `stage-e/` patch; `utils/zip_file.hpp` and `utils/han.h`, read only where a lead reaches them.
- **The writes ruling 3 holds:** `writeAllText` (`:1429-1446`).
- **Another lane's fix re-made:** T20's `d9afa5c7c`, T21's `f7c16144d` or T26's S8.
- **An edit to the rule sentences L-08 and L-13 name:** the coordinator's sweep.
- **The pin and the catalog's history:** a move of the pin; a hand edit of the catalog's existing entries.
- **Held material in public:** a held record's input, mechanism, expected result or sanitizer frames on the tree, in a commit message, in a case's name or in a post; and any held directory but the lane's own, opened or quoted (`/workspace/tmp/m6-t34/held/` included).
- **A credential-shaped literal in a fixture** (3.10's value is built at run time, `tools/t36-utils-resources-tests.cpp:136`).
- **A refused build:** a `t36-build-tests.sh` run whose extracts were refused. The script says so and does not build `utils-resources-tests`.

## Figures and lines not found in the record (ask the lane; do not guess)

1. **The build script's invocation.** `stage-c/build-tests.out` prints the rapidjson root (`:3`) and the compile line (`:5`), not the command that ran the script. The command above is assembled from those two lines and `:12`'s build directory.
2. **The stand-in's pugixml root.** `stage-c/syntax-check-probe.out:1` prints `g++: ... ; fakes: 15 files` and no pugixml line. The stage-E command line cannot be copied whole until S0's `stage-a/syntax-check.sh` prints it.
3. **Which copy of T35's stand-in ran at stage C.** Its lines are T35's (`t35-syntax-check: 25 file(s) checked, 20 rc 0, 5 not` and `t35-syntax-check: expected 44 files, checked 25`, `syntax-check-probe.out:36-37`); `00:77` names *"T35's syntax-check"* without the path or the hash it was read at.
4. **Case 3.22.** `00:57`: *"The thresholds are host-proven (case 3.22)"*. The binary holds no 3.22: its fifteen cases are 3.1, 3.2, 3.3, 3.4, 3.26, 3.10, 3.13, 3.15, 3.18, 3.21, 3.7, 3.9, 3.24, 3.8 and 3.16 (`tools/t36-utils-resources-tests.cpp:75-221`, `stage-c/build-tests.out:7`).
5. **PL-06's delete line.** `05:68` gives *"push_back `:268`, delete `:275`"*; at the pin `delete tex;` is `:274` and `tex_out = NULL;` `:275` *(pin read)*.
6. **PL-07's source.** `04:103` and `03:19` write *"G-7/PL-07"*; PL-07 is G-9 (`04:41`, `05:77`), and G-7 is `proper`'s underflow (`04:47`), one of S10's.
7. **Whose line each fixed item is.** The record has the upstream comparison for L-19 alone (`02:223`, ROCKNIX `f6c542872e` and batocera `b2ceb55a7e`). The #585 lines for every other stream depend on a comparison the stream makes.
8. **3.8 as the brief specified it.** The floor table asks for a linked positive (`h = getHeight(); sizeText(<ASCII 32..126>); CHECK(getHeight() == h)`); the binary's 3.8 is a text case (`tools/t36-utils-resources-tests.cpp:207-214`) whose comment `:209` reverses the erratum, and its PASS is a PASS of two substrings, not of the height.
9. **3.15 as the brief specified it.** The floor table's 3.15 is the two-thread race; the binary's 3.15 is the idempotent control (`:154-160`). The race case is S3's to write.
10. **`02:342`'s paraphrase of the rule.** It says the rule *"calls `runSystemCommand` the way to run an OS command without blocking"*; the rule's own sentence at `es-native-ui.md:103-104` is about a splash (`kit/t36-rule-errata.md` quotes it).
11. **The time-to-play prices.** *"The two numbers were not measured this slice (no game launched on the guest -- no scraped ROM)"* (`03:26`).
12. **`es-unit-tests` on this host.** No `RUN es-unit-tests` line exists in the record; the script does not build it (`t36-build-tests.sh:35-39`), and T35's re-run on this host printed `RUN es-unit-tests: not built` (`stage-c/t35-311-rerun.out:70`).

## Draft notes

**What this draft could not or did not read:**
- The held records, by rule; S5, S6's held half and S7 say only what ruling 6 lets them say, and their fix shapes, cases, `Already written:` lines and guest steps are the lane's from those records.
- #683's comment thread, the dispatch comment and the coordinator's acceptance script (`kit/t36-accept.sh`); `second-opinions/gpt-audit.md` beyond `04`'s account of it; T35's stand-in script and fakes.
- No compile was run for this draft: the `-Wno-error` question (item 4) and every FAIL-at-pin expectation in S1 to S10 are drafted from the record and the pin's text, not observed.

**Rulings that seem to conflict with the lane's artifacts, and gaps no ruling covers:**
1. **Ruling 7's "the one file touched by more than one stream".** With ruling 2's one stream for PL-10, S10 also touches `FileSystemUtil.cpp` (G-14, in `removeFile`, the function S4 changes), `StringUtil.cpp` (S8's), `TimeUtil.cpp` (S2's), `TextureData.cpp` (S4's and S9's) and `Font.cpp` (S1's). The draft keeps S10 last and lists every file's order in § The order. The other shape folds each G-item into its file's stream (G-14 into S4, G-3 into S1, G-10 into S2, G-6 and G-7 into S8, G-20 into S9), which makes ruling 7's sentence true and ruling 2's "one stream" false. The coordinator's choice.
2. **Seven leads with a case and no punch item.** The seat CONFIRMED L-07, L-09, L-10, L-11, L-15 and L-18 (`04:21`); 3.21 asserts a wrong relative path at the pin (R4 item 17); none has an item in `05` or a ruling. S0 runs 3.6 (L-15, a bold FAIL-at-pin candidate in the brief), 3.11, 3.12 and 3.17, so S0 will probably file new bugs under D-WORKFLOW-132 that no ruling disposes. The text cases 3.16 (L-07), 3.24 (L-18) and 3.21 PASS by asserting the defect's text, not as FAIL-then-PASS pairs. Each needs a stream, a Backlog or a recorded reason before Phase 7.
3. **The collision controls.** 3.4 and 3.2's `renameFile` half stay FAIL at T36's tip, so § 7's *"0 failed in every binary's summary after the fixes"* needs them marked `doctest::may_fail` (T35's ruling 20 precedent). No T36 ruling says so; the draft proposes it in § The rules every stream keeps.
4. **`-Wno-error` and `[-Wtemplate-body]`.** Ruling 8 names `-Wno-error`. The stage-C first error is printed as `error: ... [-Wtemplate-body]` (`02:440`), a diagnostic g++ 15 raises as an error by default under its own flag; whether `-Wno-error` downgrades it is not shown by the record. The draft has the lane try `-Wno-error` as ruled, record the line, and post on #683 before trying `-Wno-error=template-body` or `-Wno-template-body`.
5. **G-11** (`05:39`, `04:50`: an in-flight stat re-inserting after a reset) is in neither of ruling 2's lists; the draft records it with PL-03. A sixth Backlog section would be the other home.
6. **Ruling 5's "the quoting gap".** The draft reads it as L-05's G-18 (`run()`'s unquoted log path and `2>` binding, `Platform.cpp:162`; `05:131`: *"recorded, a `bug` for the quoting"*), which is launch-shell quoting beside #1371. That puts `Platform.cpp` in S6, a file ruling 7's order does not name. If it meant L-14's quoted flag (G-17, `StringUtil.cpp:725-795`), S6 touches `StringUtil.cpp` before S8 and § The order changes.
7. **PL-10's two outcomes in one punch item.** `05`'s gate table and `punch_index` carry one outcome per item (`05:145-222`); whether `tools/lint-audit-artifacts` accepts a split item, or PL-10 needs its deferred half named in the evidence cell, is not in the record.
8. **One bug or six.** #1368's body says *"one bug per finding at the stream, this issue the umbrella"*, and #1358's PL-10 checkbox *"one bug and case per finding"*. Ruling 2 has the lane edit #1368's body to the Resolved set, which the draft reads as #1368 staying the bug for all six. T35's ruling 15 filed one bug per fixed item. The coordinator's call.
9. **The RULING minutes** are this draft's clock at writing (00:42 UTC), not the minute the coordinator ruled.
10. **3.8's comment** (`tools/t36-utils-resources-tests.cpp:209`) states the L-08 erratum backwards; `kit/t36-rule-errata.md` says which evidence the edit can cite before and after S0's linked positive.
11. **The legacy GENERIC_X64 build root's rapidjson** does not exist on this host (this draft's `ls`; `02:440`), so ruling 8's second route is empty and the shared cache's tarball is the one source. The lane's stage-C extract may already be those bytes; S0's comparison of `document.h` says.
12. **Register rows.** The brief's § 9 put four questions to the pause. Rulings 1 and 4 answer the three-byte case (fixed under rule 6); rulings 1 and 3 the file helpers' contract (`copyFile` reports, `writeAllText` held for #1186); ruling 5 the pipe (recorded, `head -300` kept); and the `exists` cache keeps its stored-miss contract with L-19 and the thumbnail reads fixed under ruling 1. No ruling names a row; whether any is written is the coordinator's, at an ID it assigns.
13. **The held cases at acceptance.** The coordinator's acceptance re-runs the unit build on clones (the brief's § 10). A held case fails closed without its held input, so the acceptance run needs the held path given to it, or reads the held cases' lines from the lane's record.
14. **#1369's caller** is in `es-app/src/ApiSystem.cpp` (its public body); its owner is not in this record.
15. **The `Already written:` arguments the draft adds** -- S8's stored folds, S4's absent thumbnail and S10's dangling link -- are proposals from reading the code paths, not from the lane's record; the bugs' own lines say *nothing inherited* for S8 and S4.
16. **T35's re-run on this host** printed four of T35's own sanitizer programs as `BUILD FAIL` (`stage-c/t35-311-rerun.out:109-118`). They are T35's, not T36's; the hand-back's second re-run will print them again.
