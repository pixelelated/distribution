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
