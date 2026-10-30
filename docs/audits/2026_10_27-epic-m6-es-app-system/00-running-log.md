# Running log -- M6.P2 T33, EmulationStation's system layer (#680)

- **Executor:** Opus 5.5 at high effort, the T5 session (`m6-t5-build-engine`), by the coordinator's dispatch on #680 (comment 6450540818, 18:38 UTC).
- **Depth:** Independent: one seat, GPT-6 Astra at `max`, a probe and one refutation.
- **reviewed-at:** `27bd8499f1` (distribution, the lane tip the dispatch names); **reviewed-at-es:** `16dbac5211` (the pin, the ES worktree clean at it).
- **The brief:** `docs/reviews/briefs/es-app-system.md` at `c48f8b387e` (version 2). #680's body carries its § 7 checkboxes and the VM line; where they differ, the body wins.
- **The host, at 18:42 UTC** (`/tmp/m7-m6-host-coordination-20261023.txt`, its last two lines):
```

== M6 coordinator — 16:22 UTC (2026-10-27): T32 RETURN 16:22:34 ACKNOWLEDGED (the guest stopped by pidfile at 16:22:12, vm-stop rc 0; the disk retired, 2,312,372,224 bytes, sha256 a3a152ce…0627d, removed). Census now: qe
```
  Census at the read: qemu 0 (`pgrep -fc '^qemu-system'`), compilers 0. No guest runs before a grant on #680.
- **Rules:** the session's rules were loaded at its start from the T5 worktree. This lane's `.claude` differs from `next` (`git diff --quiet next -- .claude CLAUDE.md AGENTS.md` prints STALE), as on every stacked lane, and the dispatch's rule lines stand.

## Stage A (18:42 UTC)

- **§ 1's first commands** (`stage-a/first-commands.sh` / `.out`): every line prints what its comment says -- `stacked`, `upstream-next-is-here`, the pin, `cada856d86`, `f6c542872e`, `3ae9610b0`, `5c0ddaaee`, `26`, `register-ok` -- with one exception of mine: `git status --short | wc -l` printed 1, because I had made `stage-a/` before running the block.
- **The pointer** carries T33's lens and rule lines (77 paths, 16,276 lines). Its epic line still read "T20 #667 and T21 #668 briefed ... T33 to T37 after"; both are accepted and the next slices are T34 to T37. Corrected in the pointer at this commit.
- **§ 2's membership block** (`stage-a/membership.sh` / `.out`, the brief's block verbatim): `mine: 77 paths.txt: 77 equal: True`; `lines: 16276`; tiers fork-own 31, upstream-carried 46; `fork-own lines: 4522`; `read lines: 16210`; 75 text paths; `wc -l text 16272`, `grep -c text 16276`; 50 and 50; `31 files changed, 2689 insertions(+), 7 deletions(-)` twice. All as the brief expects.
- **§ 5's runs** (`stage-a/runs.sh`, the block with each comment echoed before its command; `runs.out`): every figure as its comment expects.
  - The two stage-C lines are held for stage C.
  - `TIPHASH` was run as `27bd8499f1`: empty, and the ES diff against the pin empty. The literal word prints `fatal: bad revision 'TIPHASH'`.
  - **One display slip in the brief's own command:** the plain-`g++` line's `cut -c1-90` ends inside the absolute path `$W/$F` before the error. Rerun uncut, it prints `es-app/src/MetaData.cpp:6:10: fatal error: pugixml/src/pugixml.hpp: No such file or directory`, rc 1, as expected.
- **The stand-in** (`stage-a/syntax-check.sh`, T21's; T31's 13 fakes under `stage-a/fakes/`; the pin's pugixml root; the recipe's rapidjson rebuilt under `/workspace/tmp/m6-t33/rj`, its sha matching `PKG_SHA256` and its four patches applied): **29 of 29 rc 0** over classes (a) to (d) (`stage-a/syntax-check.out`).
  - Class (e): `Win32ApiSystem.cpp` is wrapped whole in `#if WIN32` (`:1`, `:1267`) and preprocesses here to nothing that names `Win32ApiSystem::`.
  - Class (f): `ScraperCmdLine.cpp:4` includes a `platform.h` that does not exist at the pin.
- **History** (`stage-a/history.out`): 72 fork commits on the 77 since `bccd715707`, 68 non-merge.
- **Callers** (`stage-a/callers.out`): 149 quoted includes of the slice's 41 headers, from 66 files outside the 77. `CollectionSystemManager.h` 17, `PlatformId.h` 11, `Gamelist.h` 10, `Genres.h` 9.
- **Nothing else ran:** no build, no fetch, no guest, no council call. Scratch is `/workspace/tmp/m6-t33/`.

## Stage B (18:44 UTC onward)

- Stage A accepted on #680 at 18:43 UTC (the coordinator's errata: the cut in the brief's g++ line, and the pointer's epic line). The plan is in the pointer's Current focus: § 3, § 4, § 6 and § 7 read; the generators (T32's, renamed); `02` composed from `stage-b/02-template.md`; then the window request.
- **The generators** (`tools/`, T32's renamed and rewritten for T33), each asserting its counts. Each was seen to exit 1 on a wrong count and on a paths list with its file dropped (`stage-b/generators.txt`):
  - `t33-reads.py`: 83 lines, 86 calls, 4 uncached;
  - `t33-writes.py`: 11 lines, 9 compiled and 2 dead;
  - `t33-bounds.py`: 4 http, 6 process, 4 waits, 2 bounded;
  - `t33-library.py`: 11 units;
  - `t33-helpers.py`: 17 units in 27 files; 12 with a case, 7 built;
  - `t33-words.py`: 176 lines, 223 calls, 196 msgids, 0 empty.
- **One recording slip, kept as it was:** `t33-words.py`'s failure message still said `t32-words` at its first drift run. I renamed it and reran both runs, which are appended below the first. The first record is not edited.
- **`02` composed** by `tools/t33-02.py` from `stage-b/02-template.md`: coverage 77 rows (27 / 4 / 46, inventory 31 / 46), the sixteen sections of brief § 6, and the leads and the floor carried word for word with the proposed dispositions. The composer exits 1 and writes nothing on a dropped path (recorded).
- **Found while composing:** `tools/es-menu-map-check` cannot see FILTER GAMELIST BY or EDIT DYNAMIC COLLECTION FILTERS, because their titles are passed in a member initializer (`mMenu(window, _("..."))`) that none of its three patterns reads. This is recorded in `02` § The structure, with the proposed map text and the fourth pattern named for the coordinator. The lane does not change `tools/`.
- **Window plan:** `stage-b/window-plan.md`: 25 + 5 minutes; the steps sum to 1,260 s by awk; G-05, G-07 and G-09 are `CANNOT`.

## [Window] 19:00 to 19:14 UTC — the guest, granted on #680

Granted on #680 at 19:00 UTC (comment 6450973084). START 19:01:31 UTC (comment 6451000093). The guest was stopped by `tools/vm-stop` on its pidfile at 19:14:06 UTC (rc 0), 13 minutes into the 25. The image is M7's composition, so every frame below is `image`. Records and frames are under `guest-cycle/`.

| G | Result | proved: |
| --- | --- | --- |
| G-01 | `BUILD_ID=069fc270442134fe771258418adf4e666e0473fb`, `VERSION=0.0.1-dev+20261022T235948Z.g069fc2704421`, `640 480`; the slice's literals present in the installed binary (`SETTING UP YOUR CLOUD FOLDERS`, `from=checked-launch`, the two filter titles, `IN PROGRESS`, ...) | guest (`g01-identity.txt`) |
| G-02 | seeded `custom-t33.cfg` (Alpha) with the collection selected; it opens in the COLLECTIONS bundle (`g02-1-left3`, `g02-3-t33-list`); REMOVE FROM T33 on Alpha inside the bundle: the view rebuilt onto the bundle's `t33` folder, ES's pid unchanged (2308), no backtrace in the journal. **L-06 did not fault on one removal**: the heap's choice, as #246's was; the proof stays the ASan extract at stage C. The removal is written only later (the file kept its line until UPDATE GAMELISTS wrote it empty) | guest (`g02-l06.txt`, frames `g02-*`) |
| G-03 | UPDATE GAMELISTS is TOOLS's first row of GAME SETTINGS (`g03-1`), behind REALLY UPDATE GAMELISTS? YES / NO (`g03-2`); `/isIdle` `[ true ]` 8 s after YES; the three stubs listed (`g03-6-gb-list`); **no index toast**: INDEX NEW GAMES is not on in this fixture, so that half is not shown. SCREENSHOTS over 100 zero-byte captures of one stem: the first change 0.1 s after the press, settled 1.3 s later, on a four-game library: L-04's walk is not priced by this library. `/var/log/exec.log` absent (no RetroArch launch in the window): L-02's `stat` is not shown | guest (`g03-update.txt`, `g03-screenshots.txt`) |
| G-04 | **L-05 reproduced.** gb's `gamelist.xml` written from outside ES while it ran (an entry for Bravo with a description, md5 `055b53a8…`); Alpha starred (recorded at once in `recovery/gb/Alpha.xml`, `saveToXml`); QUIT > RESTART EMULATIONSTATION > YES (pid 3303 -> 4215): gb's `gamelist.xml` now holds Alpha's entry alone (md5 `d4307578…`), **Bravo's entry and its description gone**. The control, gbc's file written the same way with no dirty game, byte-identical. The recovery folder emptied by the clean exit; the path relative, only non-default fields. **Mine:** a first read at 19:07:52 was taken with REALLY RESTART EMULATIONSTATION? still open (`g04-5`) and is void as G-04's read, kept as the before-state; its "2308 before" was wrong too (2308 preceded my 19:06 systemctl restart; ES was 3303) | guest (`g04-gamelists-after.txt`, `g04-gamelists.txt`, `g04-where.txt`) |
| G-05 | `CANNOT` (no fault seam); 3.13 at stage C | -- |
| G-06 | `ScreenSaverTime` 60000 with `dim`: dimmed at 70 s (`g06-1`), the same screen awake after `shift` (`g06-2`); with `black`: a black frame (`g06-3`); 0 crash lines in essway over the boot | guest (`g06-dim.txt`, `g06b-g08-seed.txt`) |
| G-07 | `CANNOT` (no NIC) | -- |
| G-08 | the editor reached by the list's VIEW OPTIONS > OPTIONS > VIEW PAD TO KEYBOARD INFORMATION (`GuiGamelistOptions.cpp:257`; GAME OPTIONS offers no PADTOKEY row for this game); a seeded `Alpha.gb.keys` with one mapping on `up` and one on `t33unknown`: **the editor shows `T33 KNOWN` alone, and nothing says a mapping was dropped (L-28's positive)**. Seeded over serial rather than set in the editor, inside the bound; the file's shape is `load`'s at `:236-292` | guest (`g06b-g08-seed.txt`, `g08-4-editor`) |
| G-09 | `CANNOT` (no account) | -- |
| G-10 | journal: 0 crash lines; the disk `t33.qcow2` 2,309,619,712 bytes, sha256 `1409b81a…6ca9ca4`, removed; qemu 0, compilers 0 | guest (`retired.txt`, `g10-journal.txt`) |

**Also seen on the way:** VIEW OPTIONS > NAVIGATION > OTHER FILTERS on the gb list (`g08-2`), the path the proposed map text for FILTER GAMELIST BY names.

## Stage C (19:22 UTC onward; the coordinator's 19:16 instruction: stage C whole, then 05 and the audit issue, ending on the stage-D pause)

- **The include graph** (`stage-c/includes.out`): inbound 150 include lines from 66 files; outbound 380, es-core 134. Every #include form is counted. Stage A's quoted-only count was 149; the extra line is `GuiMenu.cpp:60`'s angle-bracket `LibretroRatio.h`. Drift-tested.
- **The unit build** (`stage-c/build-pin.txt`): `tools/t33-build-tests.sh` is extended to `tests/app-unit`'s `app-unit-tests`, parsed from its CMakeLists with its flags (`-g -fsanitize=address,undefined`). That file puts no `fakes/` before `es-app/src` for this target, unlike the brief's sentence. The first build of the five case files gives `app-unit-tests` 18 cases and 18 passed; the script's line is `TOTAL: 239 test cases in 5 binaries`, rc 0.
- **The six FAIL-at-pin cases**, each seen to FAIL at the pin with its `--control` (the proposed fix) PASSing. They are the `stage-c/l3NN-*.py` harnesses; their runs are in `stage-c/runs.txt`:
  - 3.9: `0.05` reads 0 STARS; `3000…` and `0999…` read "".
  - 3.13: Bravo is lost and the file is written in place.
  - 3.21: the unknown trigger is dropped and nothing is logged.
  - 3.29: three tag names have no extracted literal and no French.
  - 3.31: `india` reads nothing.
  - 3.35: the floor keeps 4 ASCII characters against 1 Japanese.
  - **Two readings sharpened:** at 3.21, the dropped mapping does not load at all (`:292` keeps a mapping only with a trigger), where the brief said "an action with no trigger". At 3.31, `usa, europe` reads region `us` alone; the region is one string, so the brief's "us,eu" is not this code's shape (recorded, not a FAIL). And `1 STARS` has no singular: a word, upstream, recorded.
- **The lifetime harnesses**, each with its control:
  - L-06: a heap-use-after-free at the pin. Only a **dynamic** collection takes `reloadCollection`'s repopulate path (`:1573`), and its root is the bundle's child (`:1302`), so G-02's plain collection could not show it.
  - L-07: a heap-use-after-free at the pin. The builder has no destructor, and its thread is never joined or deleted.
  - L-12: five direct posts bypass `AppWindow::closing()`.
  - `stage-c/runs.txt`: nine FAIL at the pin, nine controls PASS. The L-06 control's first run failed on the harness's own leaked fixture, which was then freed (D-WORKFLOW-211); the assertion did not change.
- **L-05's first cached miss:** `SystemData::getGamelistPath` (`SystemData.cpp:1653`) calls `exists(filePath)` when the systems load and again as `Gamelist.cpp:412`'s own call. A session started before a restore always holds the miss.
- **The screensaver's launch** (`SystemScreenSaver.cpp:546`, take-up row T2 `:293-294`) skips `ViewController::launch`'s format warning (`:497`) and BIOS check (`:507`). It keeps the cloud gate in `FileData::launchGame` (`FileData.cpp:993`).
- **The floor's other 35 rows** are being read by a read-only subagent (labelled as such in `stage-c/floor.md`).
- `03-retrospective.md` and `stage-c/ask.md` are written.
- **The floor's 35 rows** (`stage-c/floor.md`, the subagent's read, labelled): PRESENT 16, ABSENT 18, NO-DEFECT-CLAIM 1. The first reader re-read five at their lines. **One new defect worth a punch item:** 3.8's `Genres.cpp:304` dereferences the end iterator (`g` for `sg`). Also re-read: `FileData.cpp:1659`'s off-by-one (T2 FD-15's sibling, outside the slice) and `FileFilterIndex.cpp:579-580`'s 520 KB of stack.
- **The packet** (`stage-c/packet.py`, T32's adapted): 201 sections, 539,134 bytes, sha256 in `second-opinions/packet-manifest.json`. The forbidden-terms check found 0 sections with hits and was proven to run on a clean line. `SECRET_PATTERNS` found 0 lines and was proven to fire on a run-time fake. The words scan left 0 for review: 35 code hits and 4 prose hits were dispositioned by `(file, line)` after a masked read. 6,399 of 16,276 slice lines were sent, 29 files whole. `astra-brief.md` is the packet.
- **Keyed call 1 of 2, the probe** (19:31:25 to 19:31:43 UTC, rc 0): `READY unknown`, served `openai/gpt-6-astra` by OpenAI at `max`; identity, effort and provider verification PASS.
- **Keyed call 2 of 2, the refutation** (19:41:52 to 20:01:31 UTC, rc 0): served `openai/gpt-6-astra` by OpenAI at `max`; identity, effort and provider verification PASS; 167,998 prompt tokens and 43,931 completion tokens. **Exactly two keyed invokes, and no others.**
- **The council runtime:** `npm install --offline` in `tools/council` at 19:30:56 UTC on 2026-10-27, rc 0. `node_modules` was absent before it, and it was installed from the local cache; npm's only notes were its install-scripts warning for `esbuild`'s postinstall, which did not run. No network fetch.
- **Every council call but the seat's two ran with `COUNCIL_ENV_FILE=/nonexistent`:** `tools/council/run efforts` and `tools/council/run invoke --help`, at 19:31:13 UTC. The two keyed invokes are the probe and the refutation above (`stage-c/keyed-calls.txt`). The keyless calls were read back from the session's own transcript at the close-out (2026-10-30), since no file recorded them at the time.
- **The grades** (`stage-c/astra-grades.md`): 47 items, all accepted, each checked at the pin's lines.
  - **Corrections to this reader, fixed in place:**
    - L-06's bundle route is not established (EP-5);
    - L-07's thread *is* joined in `update()` (EP-6);
    - L-02's log read is not bounded (EP-14);
    - `SystemScreenSaver.cpp:375` is media, not the title folder (EP-17);
    - the bounds table is not exhaustive (EP-18);
    - the `.xcc` is pugixml's, and a cut one empties the collection (EP-19);
    - the `.keys` writes go through `writeAllText` (EP-21);
    - UPDATE GAMELISTS's collection-settings entry is Windows-only (EP-25);
    - the epoch is `time_t` (EP-12).
  - **New punch items:** PL-21 (EP-42), PL-22 (EP-44), PL-23 (EP-39), PL-24 (EP-40, EP-41), PL-25 (EP-38), PL-26 (EP-46). EP-36 joins PL-01, EP-37 PL-02, EP-43 PL-05, and EP-45 and EP-47 PL-19.
- **`t33-bounds.py` revised** (EP-14): `bounded=1`, drift-tested (`stage-b/generators.txt`). `05` is rendered by `tools/t33-05.py` from `stage-c/punch-items.py`: 26 items, all Open.

## Stage D (20:07 UTC)

- **The audit issue #1270**, created from `05` by `tools/t33-issue-body.py` (26 items: 0 critical, 1 high, 13 medium, 12 low, 0 info) with the labels `audit` and `punch-list` and the milestone M6, attached as a sub-issue of #680. `tools/box-check --issue 1270`: 26 open checkboxes, 0 fail (`stage-d/box-check-1270.txt`). `tools/lint-audit-artifacts --phase pre-issue --issue 1270`: PASS (`stage-d/lint-pre-issue-1270.txt`).
- **The pause:** the punch list and the questions are posted on #680. The lane waits for the coordinator's ruling and the stream brief; no bug is filed before the ruling.
- **The ruling** (20:10 UTC, #680 comment 6452429909). **Twenty bugs filed**, #1271 to #1290 (`stage-d/bugs/filed.txt`), by `tools/t33-file-bugs.py`: each carries its `05` section, the ruling, and a four-part code trace (how found, the defect at the pin, siblings, what reading cannot prove), with its `Already written:` and VM lines. Each names #680 and #1270; `05`'s **Bug:** lines and #1270's regenerated body name each bug. `tools/box-check` on #1270 and the twenty: 0 fail each (`stage-d/box-check-bugs.txt`).
- **Two of mine, fixed before anything was misfiled:** the item lookup in `stage-c/punch-items.py` was built before PL-21 to PL-26 were appended (a `KeyError` stopped the render; the lookup was rebuilt); and `tools/box-check` takes one `--issue` per run (run per issue).
- **Not filed, and asked on #680:** PL-13 (L-27) and PL-18's 3.5 were put as "recorded or a bug?" and are not in the ruling's list. The ruling's "twenty-one proposed" counts differently from `05`'s fifteen titles proposing a bug.
- **The last ruling** (20:15 UTC, #680 comment 6452522368): PL-13 and PL-18's 3.5 are bugs under rule 6. **Filed as #1291 and #1292** by `tools/t33-file-bugs.py --second`, with their traces, `Already written:` lines (3.5's: what earlier scrapes blanked stays blanked; nothing to migrate) and VM lines; box-check 0 fail on each. Before filing, the first 20 bodies were re-rendered and compared with the filed ones: the only difference is the **Bug:** line `05` gained after filing.

## Stage E (05:19 UTC 2026-10-30 onward; the brief `t33-streams.md` at the coordinator's `31561429a2`, the dispatch #680 comment 6515550000)

- **The build script's command file:** `tools/t33-build-tests.sh` in this folder. Run as `. stage-a/env.sh && bash tools/t33-build-tests.sh <W> /workspace/tmp/m6-t33/build-<point>`:
  - `build-pin` at stage C (`stage-c/build-pin.txt`);
  - `build-s3` for S3;
  - `build-s4b` for S4b's new cases over the unfixed sources, and `build-s4b-after` after its fix;
  - `build-tip` at the hand-back.
  Each prints its own `TOTAL:` line, quoted in the stream's records and in `stage-e/handback-checks.txt`. The fixtures' commands are `stage-e/handback-run.sh` (every harness at a tip, with its expected rc) and the `$` lines heading each `stage-e/sN-before.txt` and `sN-after.txt`.
- **S1a** (ES `d0d92dda6`, #1271, #1285):
  - **Before:** at the pin, `stage-c/l313-gamelist-save.py` (l313's extension) FAILs all nine checks across its seven cases (outside, inode, unparsed, recovery, media, record, kill ×3), and l313 FAILs both its lines.
  - **After:** all rc 0. l313's `--control` is guarded `CANNOT`, and its fixture was completed (D-WORKFLOW-211: the helper's extract and two doubles; no assertion changed).
  - **Generators** (D-WORKFLOW-210): `t33-reads.py` 4 → 16 uncached; `t33-writes.py` 11 → 7 lines. `t33-writes.py` now reports a file whose every write line was replaced instead of failing. Each was drift-tested.
  - **Stand-in:** `Gamelist.cpp` rc 0.
  - **The `getGamelistPath` patch** is `stage-e/patches/s1a-SystemData-getGamelistPath.patch`: it applies to the pin, and the scratch copy passes the stand-in.
  - **Read:** `PackGamelists` defaults to false (`Settings.cpp:209`), so EP-2's clear needed that setting on.
  - The ES pre-push test passes; the branch is pushed.
- **S1b** (ES `dd86d7ce2`, #1271, D-CLOUD-187):
  - **The harness:** `stage-c/l313-gamelist-merge.py`, l313's merge extension, extracts `updateGamelist`, `addFileDataNode` and MetaDataList's `set`, `appendToXML`, `overlayXML`, the changed-flag functions and `setDirty` as written.
  - **Before:** at S1a's code the cases `same`, `desc` and `default` FAIL; at the pin `same` FAILs; the `whole` control passes.
  - **After:** all four pass.
  - **Fixtures completed** (D-WORKFLOW-211): S1a's harness and l313 got an `overlayXML` double returning false, the rebuild path their cases assume; no assertion changed.
  - **Cost** on the host at `-O2`, against D-CLOUD-119's 3 s, with one dirty game:

    | Entries | Pin | S1a | S1b |
    | ---: | --- | --- | --- |
    | 1,000 | 0.7 ms | 0.8–0.9 ms | 0.8–0.9 ms |
    | 10,000 | 6.5–7.0 ms | 8.0–8.3 ms | 8.4–8.5 ms |

    The device's factor is unknown, and the harness's double does not fsync.
  - **Not done:** a doctest; `MetaData.cpp`'s includes are beyond the app-unit fakes.
  - **The lost update** inside the read-to-rename span is recorded, not closed.
  - **`setDirty()`'s callers:** `Gamelist.cpp:239`, `SystemData.cpp:259`, `services/HttpServerThread.cpp:682`, `:686`.
  - **Stand-in:** `MetaData.cpp` and `Gamelist.cpp` rc 0.
- **S2** (ES `4e9a7d166`, #1272, #1275, #1287):
  - **The harnesses:** `stage-c/l06-collections.py` (l06's extension, over the real drop/remake pair read from T2's `ViewController.cpp`) and `stage-c/s2-collection-files.py`.
  - **Before:** at the pin, `bundled` faults (heap-use-after-free) and `ep37` FAILs (the old view is moved); `nonbundled` does not fault, so Medium stands. `cfgkill`, `xcckill`, `delete` and `reset` all FAIL.
  - **After:** all pass. l06's fixture was completed with the pair (D-WORKFLOW-211), and its `--control` is guarded.
  - **Generators:** 16 → 18 uncached; 7 → 5 lines.
  - **Stand-in:** both files rc 0.
  - **EP-43's patch** for T31's `GuiGamelistFilter.cpp` is in `stage-e/patches/`; the patched scratch copy is rc 0.
  - **A correction to the brief:** `resetIndex` clears 20 facets, not nine.
- **S3** (ES `0b369b44b`, #1274, #1279, #1291, #1292, #1282, #1278):
  - **New harnesses:** `stage-c/s3-tables.py` (genre, import, xcc0) and `stage-c/l321-keys-shapes.py` (l321's NDEBUG extension, one shape per run).
  - **Before, at the pin:** l309, l321, l331 and l335 FAIL; `typenum` and `actionstr` SEGV and `trignum` aborts; `chord` loads on `up` alone; `genre` is a global-buffer-overflow; `import` blanks 5 of 5 fields; `xcc0` reads `0 STARS`. `targetobj` does not fault at the pin (undefined behaviour, quiet).
  - **After:** all rc 0.
  - **The fourth `TextFitTests` case** FAILs on the pin's header and passes here; `TOTAL: 240 test cases in 5 binaries`, 0 failed.
  - **Words:** `t33-words` reads 177 lines, 224 calls, 197 msgids, 0 empty; `es-untranslated` 704 of 704.
  - **Stand-in:** five `.cpp` rc 0.
  - **PL-12's toast patch** for T31's `GuiKeyMappingEditor.cpp` is in `stage-e/patches/`; the patched scratch copy is rc 0.
  - **#1291's `Already written:`** takes ruling 3's sentence, edited with S3's checkpoint.
- **S4a, 09:30 UTC (ES `b902cc8ba`; #1276, #1288, #1283)** -- resumed after the 05:41 usage-limit pause (#680 comment 6515896420).
  - **The fixture** `stage-c/s4a-token-check.py` (new) extracts the token component, the token branch and the helper as each tree has them, over doubles with the pin's lock shape. At the pin, `switchoff`, `account`, `reset` and `closing` FAIL; `sameacct` PASSes. `l12` FAILs at the pin with 5 direct posts. All of these are in `stage-e/s4a-before.txt`.
  - **After:** all five PASS under ASan and under TSan. `l12` reads `0 direct post(s) at -; 5 through AppWindow::post`, and its `--control` is guarded `CANNOT`. `ResetComponent` waited 0 ms, against 1999 ms at the pin.
  - **The brief's worker, changed:** there is no `ResetComponent` from the worker (the deadlock posted at 05:41). The component polls at 1000 ms while a sign-in is out, and a function-local static joins the worker before HttpReq's statics go.
  - **PL-23's test** adds the password, so a page's check for the same account after a password edit is not absorbed by the sign-in in flight. Ruling 5: no generation patch.
  - **Ruling 7:** the update check is not moved, because `canUpdate` returns for `pixelelated` at `ApiSystem.cpp:455-456`. It is recorded for the es-core slice, and #1283 keeps that checkbox open.
  - **Checks:** generators unchanged (18, 5, 197); stand-in rc 0; pre-push-test PASS.
- **S4b, 09:45 UTC (ES `a5273390e`; #1286, #1281, #1280, #1284, #1285, #1289)**
  - **Before:** five new doctest cases. The ids, the unlocks shape, the pending ids and the tail holder FAIL at the pin; the interpreter case passes. `TOTAL: 245 test cases in 5 binaries`, with es-unit-tests at 3 failed and app-unit-tests at 1. The new `stage-c/s4b-cloudoffer.py` FAILs 5 of 7 at the pin, and `stage-c/s4b-writes.py` FAILs 6 of 6.
  - **After:** `TOTAL: 245 test cases in 5 binaries`, 0 failed in every binary. The `CloudOffer` fixture passes 7 of 7 and the write fixture 6 of 6. Stand-in rc 0 for the four `.cpp` and for the ids' two consumers.
  - **Generators:** `t33-writes` goes from 5 to 2 lines, `t33-words` from 197 to 199 msgids, `t33-reads` stays at 18. `es-untranslated` reads 706 of 706.
  - **Changed from the brief, both recorded:**
    - **RunLock** also matches the script after `sh` or `bash`, because the shipped ctl is `#!/bin/bash` and argv[0] alone would never name it.
    - **The rotation cache** is keyed by the inode and the mtime's nanoseconds as well as mtime and size, which catches a rename that keeps the modtime.
  - **The lock's why** (`ANOTHER CLOUD SYNC IS RUNNING`) is missing from CloudText's table, so `outcomeFor` gives it French itself; the table row is named for the cloud slice.
  - **The l321 fakes** are completed with `AtomicFileUtil.h` (D-WORKFLOW-211).
  - **T20's collision** is named: no shared line.
- **S5, 09:51 UTC (ES `d370ac62e`; #1273, #1290)**
  - **`l07` extended:** `engine` deletes the engine while its search runs, and `l08` records which thread the second search runs on. At the pin, `drop` and `engine` FAIL with heap-use-after-free and `l08` FAILs on the calling thread. Stage C's control passes `drop` and FAILs `engine`, reading destroyed params, so the builder now copies its params.
  - **The new `stage-c/s5-bluetooth.py`** FAILs at the pin with heap-use-after-free in the constructor.
  - **After:** `drop`, `engine` and `l08` all PASS. The Bluetooth fixture runs 2 scans and 2 formats with 0 refused. `l07`'s control is guarded `CANNOT`; stand-in rc 0; generators unchanged.
- **S6, 09:52 UTC (ES `f802c55c6`; #1277)**
  - **Before:** `l329` reads `9 tag names, 3 without` and FAILs. `es-untranslated` reads 706 of 706 and cannot see the three.
  - **After:** `l329` reads `9 tag names, 0 without` (rc 0), and its control is guarded `CANNOT`. `t33-words` moves from 199 to 202 msgids; `es-untranslated` reads 709 of 709; stand-in rc 0.
  - **The words:** EN COURS, ABANDONNÉ, EN PAUSE.
- **S7, 09:54 UTC (distribution; #1270 checkbox 17, PL-17)**
  - `docs/es-menu-map.md` takes UPDATE GAMELISTS under GAME SETTINGS > TOOLS, and a new `## Game list filters` section for FILTER GAMELIST BY and EDIT DYNAMIC COLLECTION FILTERS.
  - **Checker:** `es-menu-map-check` reads `0 missing` before and after, because the pages stay invisible to it.
  - **The grep** goes from 0 to 5. Recorded in `stage-e/s7-checks.txt`.

## [Stage F] 14:30 UTC 2026-10-30 -- the record at the hand-back (the brief's § The record)
- **`05` at Phase 7**, by `tools/t33-05.py` from `stage-c/punch-items.py`'s new `RES`: 23 Resolved and 3 Deferred (PL-20 to #1235; PL-25 and PL-26 to #585). The table and the index were moved together, and the brief's § Lines are corrected. `tools/lint-audit-artifacts --phase resolution --issue 1270` reads PASS.
- **`02`:**
  - § The streams: one row per stream, S1a to S7, the exit save's cost against D-CLOUD-119, and the recorded items;
  - § The #585 lines owed: a stage-E table of 21 lines, the fork's own files named as carrying none;
  - § The merge debt: stage E's, by file.
- **PL-25:** the list is not cleared on the transfer's rescan path (`stage-e/pl25-read.txt`). The new `stage-c/pl25-screensaver.py` FAILs at the pin and the tip with heap-use-after-free; it is a lead for T2 and es-core, and severity is the coordinator's word.
- **Comments:** #1235 (`ScraperCmdLine`) and #771 (`FileData.cpp:1659`), linked in `stage-e/comment-links.md`.
- **The tip's checks** (`stage-e/handback-checks.txt`):
  - `TOTAL: 245 test cases in 5 binaries`, 0 failed in each;
  - 14 edited `.cpp` through the stand-in at rc 0;
  - `es-untranslated` 709 of 709 and `es-menu-map-check` 0 missing;
  - the pre-push test PASS;
  - generators at 18, 2, 202 and the bounds line;
  - `stage-e/handback-run.sh`: 30 runs, 0 unexpected.
- **Commands:** the build script is `tools/t33-build-tests.sh <W> <dir>`, and each fixture's command is in `stage-e/handback-run.sh`.
- **14:35 UTC:**
  - #1270's 26 checkboxes are ticked from the Phase 7 table, and `box-check --issue 1270` reads 0 open and 0 fail.
  - The 22 bugs carry `fixed-at-es: f802c55c6` with their stream's commit (22 of 22 read back), and `box-check` reads 0 fail on each.
  - The retro is `docs/retros/2026-10-30-m6-es-app-system.md`; the pointer and the work log are at the hand-back.
- **14:45 UTC, at acceptance (the coordinator's 14:42 ruling, #680 comment 6525495300): PL-25 filed as #1305.**
  - The body carries its code trace, `Already written:` nothing inherited, and `stage-c/pl25-screensaver.py` as its VM line. Medium is proposed from the trace: a crash reachable only with a non-default screensaver over a match that removes ROMs.
  - `box-check --issue 1305` reads 0 fail.
  - `02` § The merge debt names #1305, with `SystemData.cpp`'s half for the integration and `Window.cpp`'s for T35. § The streams' recorded line and #585 line 21 name it too.
  - `05`: PL-25 is Medium, its bug is #1305, and its Phase 7 row is Deferred: #1305. The lint reads PASS.
  - #1270's PL-25 row carries the bug; `box-check` reads 0 fail.
- **19:23 UTC, the close-out (the coordinator's acceptance read, #680 comment 6525576831):**
  - **The two record lines:** the build script's command file is named at the head of the stage-E section above; `02` § The streams' S4a row names the es-core half and its S4b row names T20's collision. PL-25's #1305 was already in § The merge debt (`1140125aca`).
  - **Retired under D-INFRA-022** (`stage-e/retirement.txt`): the ES worktree (47,501,898 bytes, `git worktree remove` without `--force`, the branch kept at `f802c55c6` and on origin) and `/workspace/tmp/m6-t33/` (100,573,633 bytes).
  - **`tools/write-completion.py`** (T32's, its folder and issue changed) refuses while #1270 is open, and writes nothing.
  - **Lint:** both ways PASS (`--phase resolution --issue 1270` and the folder alone).
- **19:26 UTC, the close-out's end:**
  - #1270 is closed as completed (19:25:59Z). `tools/write-completion.py` wrote `audit-completion.json`, `tracker-completion.json` and `tracker-final-readback.json` from its readback: 26 ticked, 0 open, completed_at 19:26:08Z.
  - The lint passes both ways, and `ceremony-check` reads the audit marker `ok`.
  - The pointer is idle.
- **The closing census**, the RETURN line on `/workspace/tmp/m7-m6-host-coordination.txt` at 2026-10-30T14:40:02Z, quoted in the hand-back (#680 comment 6525454771): cc1plus 0, qemu 0. No runtime reservation was held at stage E, and the guest window of 2026-10-27 returned at 19:15:07 with qemu 0 and compilers 0 (comment 6451273341).
