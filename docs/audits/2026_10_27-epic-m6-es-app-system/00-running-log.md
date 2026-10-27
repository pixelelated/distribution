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
