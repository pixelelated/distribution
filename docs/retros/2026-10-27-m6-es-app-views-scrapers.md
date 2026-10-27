# Mini Retro: T32, EmulationStation's game list views, scrapers and services (#679)

**Completed:** 2026-10-27.

**Scope:** the 42 paths under `es-app/src/views/`, `views/gamelist/`, `scrapers/` and `services/` that the slice brief `docs/reviews/briefs/es-app-views-scrapers.md` (version 2) names, read at the ES pin `16dbac5211`, at Independent depth (one seat, GPT-6 Astra at `max`). The artifacts are:
- the audit, `docs/audits/2026_10_27-epic-m6-es-app-views-scrapers/`;
- the audit issue #1257: 22 items, 14 resolved and 8 deferred;
- the twelve bugs #1258 to #1269;
- the coordinator's stream brief `docs/reviews/briefs/t32-streams.md` at `1010359737`.

**Branches:**
- **The ES branch** `feature/m6-es-app-views-scrapers-679` (pixelelated/emulationstation): 6 commits, `e85735b0b` to `b52245036`. S1 to S4 and S6 are one each, and S2b is the coordinator's follow-up to the hand-back. S5 changes only the distribution's map.
- **The distribution branch** `feature/m6-es-app-views-scrapers-679` carries:
  - the records: `stage-c/`, `stage-e/`, `02` § The streams, `05`'s gate and index, and `00`;
  - the menu map's § Game list views;
  - this retro.

**Delta** (each figure is a tool's own line):
- `git diff --shortstat 16dbac5211 b52245036`: 20 files changed, 556 insertions, 190 deletions. Two files are added: `ScraperJson.h` and its test file.
- `tools/t32-build-tests.sh`: `TOTAL: 221 test cases in 4 binaries` at the pin, and `TOTAL: 225 test cases in 4 binaries` at `b52245036`, 0 failed.
- `tools/t32-bounds.py`: `bounded=0` at the pin, `bounded=9` after S2.
- `tools/t32-reads.py`: `0 uncached` at the pin, `34 uncached` after S4.
- `tools/es-untranslated`: 706 fork strings, 706 with French.

## What worked well

- **Test first, with the FAIL recorded before the fix.** Every stream's positive failed on the code before it (`stage-e/sN-before.txt`). Three harnesses found more than the brief expected:
  - `l02`'s publish case ran EP-34's window;
  - `s3-images.py` showed `:415`'s string `base_url` is a SEGV, not only a violation;
  - `s4-views.py` ran EP-35's placeholder use-after-free.
- **Extracting the pin's own functions over doubles.** It turned four seat claims and three floor items into runs (`t32extract.py`), each with a `--plain` run in the NDEBUG shape the recipe builds.
- **Generators that follow moved lines** (D-WORKFLOW-210). `t32-bounds.py` is keyed by order and the options passed, and `t32-reads.py` matches the pin's lines by order. Both read the pin as they did at stage B and read the fix as the stream meant.
- **Posting at each stream's end.** The coordinator ruled on S2's three choices before the hand-back, with no round trip.

## What was harder than expected

- **Fakes are fixtures, and they need completing.** Each stream that changed a class completed a fake (D-WORKFLOW-211), seven times in all:
  - `l02` took `mWorker`, two counters, a third counter and `HttpReq`'s codes;
  - `l316` took `status()` and the bounds;
  - `s4-views.py`'s view took the real destructor.

  The first after-run of `s4` failed on the fake's own leak, not on the code.
- **A racy positive gives different FAILs.** `l02`'s cancel case at the pin reported a use-after-free at 17:48 UTC and `cancelled 1` on the rerun. Both are the defect, but the record has to say which run gave which.
- **The brief's premises, checked at the source:**
  - `ProxyCards` is a namespace, not an instance, so no accessor was needed;
  - the fast move is not a VIEW OPTIONS row;
  - `Scraper.cpp` has a 25th `exists()` (the pin's `:808`, ES's own directory) that the sweep caught and the brief did not name.

## What did we discover

- **The recipe builds EmulationStation with NDEBUG.** Every rapidjson precondition in the scrapers is therefore a wild read, not an assertion. Three malformed bodies crash ES today (S3), and one helper, `ScraperJson.h`, removes the class.
- **A media failure was invisible end to end.** The request reported DONE, the resolve accepted it, and the page said COMPLETED (G-05's ten games read 9). S2 and S2b give each failure class its own count and why.
- **The batch scrape's lifetime had three windows, not one:**
  - CANCEL against the self-delete;
  - the creator's store against a fast worker (EP-34);
  - a startup throw that left the page running (EP-37).

  Only an owned, joined worker closes all three.
- **PL-07's picture misses in es-core,** at `TextureData.cpp:331`, `:339` and `:410`, not in the slice. Uncaching the slice's reads cannot reach it (ruling 7).

## What adjustments are needed

- **Codify the shape-first parse rule** (04 § Instruction File Recommendations): `IsObject`, `IsArray` or `IsString` before any member access on a body a network sent. A grep could audit it. This is a proposal for the coordinator, not filed here.
- **A harness's fake that mirrors a class should name the members it mirrors.** The completions above would then be one edit each, not a compile error found at the after-run. This is a practice note for the next slices' briefs.
- **The guest halves owed** are listed in the hand-back by step, for the integration window.

## Instruction recommendations

- `es-code-traps.md`: a line on rapidjson under NDEBUG (the shipped build), with `ScraperJson.h` as the pattern. This is the coordinator's to write, under the codification proposal above.

## Time to play

- **Interface to a game's first frame:** not measured for this slice; nothing was built into an image. S6 moves `POST /launch`'s lookup by path from the pool thread to the interface thread, before the launch: one walk of the library's games. The integration image's `time-to-play` cell measures it against the accepted baseline (`docs/vm-qa-log.md:9-18`; no budget row exists).
- **A game's exit to the next game's first frame:** not measured. No stream touched the exit path. The scrape's first searches moved off the interface thread (S2), which shortens SCRAPE NOW's freeze, not a launch.

## What T33 to T37 inherit

`02` § What T33 to T37 inherit, at `a0ac8e7831`:
- **The tables:** provenance, cached reads, threads and lifetimes, bounds, the scrapers' outcome routing, and `httplib.h`'s currency.
- **The map section** for the views.
- **For T33, by ruling 4:** `ScraperSearchComponent.cpp`'s manual paths (`:303`, `:321` and `:658` on the interface thread), the builder's thread (`:206`, `:220-256`), EP-36's manual token failure, and L-16's free-then-read in `CollectionSystemManager::reloadCollection`.
- **For the es-core slice:** PL-07's picture (`TextureData.cpp:331`, `:339`, `:410`).
- **For the integration:**
  - the merge debt by file: `Scraper.cpp` against T21's three commits, and `GuiScraperStart.cpp`'s patch over T31's `2fa6b5f73`;
  - the ten guest halves.

## Scoped audit (Step 2.5)

- **AC conformance: PARTIAL.** Every bug's host criteria are proved by `stage-e/` artifacts. The guest criteria wait on an image (`fix-walk-pending-image`). #1263 keeps its picture checkbox open, and #1261 keeps the T31-file half as a patch for the integration.
- **Cornerstone spot-check: PASS.**
  - `bugs-are-agent-first.md` rule 6 is applied to upstream's rows, each with a #585 line (`02` § The #585 lines owed).
  - D-UI-112: the words were built as ruled.
  - D-UI-030: every COULDN'T FINISH carries its why (S2, S2b).
  - D-UI-039: the map lands paired with S4 (S5).
  - `Already written:` is answered in every row of `02` § The streams.
- **Interaction-defect scan: PASS.**
  - S1, S2 and S2b all edit `ThreadedScraper.cpp`, and each reran `l02`.
  - S2 and S4 both edit `Scraper.cpp`; S4's sweep reran `s2-scrapers.py`'s registry and logo cases.
  - S6 reads S1's `isRunning()` under the lock.
- **Housekeeping (full suite): PASS.** `stage-e/handback-checks.txt` at `b52245036`:
  - the stand-in rc 0 on 12 of 13 sources, with `SystemView.cpp` `CANNOT` (`SDLK_r`, after the edited lines);
  - 225 unit cases, 0 failed;
  - the map check 0 missing;
  - `es-untranslated` 706/706;
  - the ES `pre-push-test` PASS.
- **Harness self-coverage: PASS.** Every new harness FAILs on the code before its stream, and each revised generator was seen to exit 1 on its constructed negative (`stage-b/generators.txt`).

## Code-verifiable state

| Stream | Bugs | ES commit | Positive |
| --- | --- | --- | --- |
| S1 | #1258, PL-14 | `e85735b0b` | `stage-c/l02-stop-after-finish.py` |
| S2 | #1259, #1261, #1262, #1267 | `bf3e8e2bd` | `stage-c/l313-request-outcome.py`, `stage-c/s2-scrapers.py`, `l316`'s 3.16 half, `tools/t32-bounds.py` |
| S3 | #1260 | `0404e76cc` | `stage-c/l310-boxart-shape.py`, `stage-c/s3-images.py`, `l316`'s L-22 half, `ScraperJsonTests.cpp` |
| S4 | #1263 to #1266 | `1655e2f4c` | `stage-c/s4-views.py`, `stage-c/l332-year-and-time.py`, `tools/t32-reads.py`, `tools/t32-words.py` |
| S5 | -- (PL-15) | the map, `cf16ff5237` | `tools/es-menu-map-check` and the grep |
| S6 | #1268, #1269 | `e594e46e3` | `stage-c/s6-api.py` |
| S2b | #1259 | `b52245036` | `stage-c/s2-scrapers.py`'s `media` and `media404` |
