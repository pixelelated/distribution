# Mini Retro: T21, EmulationStation's state primitives and its bridge to the OS (#668)

**Completed:** 2026-10-27.

**Scope:** the 14 paths at the ES pin `16dbac5211`, the audit `docs/audits/2026_10_26-epic-m6-es-state-and-bridge/`, the audit issue #1184, the nineteen bugs #1185 to #1207 (less the coordinator's Backlogs between them), the OS scripts' four halves #1208 to #1211, and #1154.

**Branches:**
- the ES branch `feature/m6-es-state-and-bridge-668`: thirteen streams of mine and the coordinator's S3, from `ba0e82c1f` to `3ae9610b0`;
- the distribution branch `feature/m6-es-state-and-bridge-668`: the records (`stage-e/`, `stage-f/`, `02` § The streams, `00`).

**Delta** (each binary's own summary line; see *Code-verifiable state*): from `221` cases in four binaries at the pin to `TOTAL: 278 test cases in 7 binaries` at the tip, 0 failed. Three new host targets: `es-fs-tests`, `es-settings-tests`, `es-scraper-tests`.

## What worked well

- **A stub that keeps the pin's behaviour, then the fix.** Every stream added its pure function or its member with the pin's logic first, recorded the FAIL against it, and only then wrote the fix. Where the shipped file could be compiled against doubles (`SystemConf.cpp`, `AtomicFileUtil.cpp`, `FileSystemUtil.cpp`, `Settings.cpp`), the "before" ran the real file instead.
- **A syntax check for the files the host cannot build.** Stand-in SDL, curl, FreeType and FreeImage headers (`stage-e/fakes/`) and the build's `-DHAVE_INTL` let `ApiSystem.cpp`, `HttpReq.cpp`, `main.cpp`, the scrapers and four pages take `g++ -fsyntax-only` (`stage-e/syntax-check.sh`). It was proven to fail on a misspelt copy before it was trusted. From S10 on, no edit was "read twice" only, and S1's, S4's and S6's earlier edits were checked after the fact.
- **The recipe's own inputs, not a fetch.** pugixml came from the recipe's source cache at the submodule's commit (`61c944895e`), so `Settings` and the scraper's readers got real tests without the worktree's submodule.
- **Questions put on #668 with a recommendation**, each ruled within minutes: the text row's refusal, the marker and where it does not apply, the BIOS page's sentence, PL-21's reading.
- **Bodies copied, not re-drafted.** The nineteen bugs and the four OS halves took their text from `05` by script (`/workspace/tmp/m6-t21/stageD/bugs.py`).

## What was harder than expected

- **Three responses stopped by an automated safety check:** `05` twice and S3's read. The coordinator wrote `05` and S3 (D-WORKFLOW-212); the friction is Backlog #1183.
- **Totals written without adding them up.** The case totals I posted for S2 to S13 were composed, not counted, and all were too high, by 2 to 53. Every binary had passed; only the sums were wrong. Corrected in `02`, `00` and on #668. The build script now prints `TOTAL` from the binaries' own lines.
- **A commit named before it existed.** S11's rows first carried a placeholder hash, replaced before the record was committed; every ES commit in `02` § The streams was then checked to resolve.
- **A stub that was not the pin's whole logic.** S11's first stub left out the pin's spaced base-colour branch and failed a case the pin passes; it was completed and the before rerun.
- **A script that did not reproduce its output.** `hostname-empty.py`'s step 3 had been run by hand at stage C; it is now in the script.
- **Doctest in a forked child.** A child that raised `SIGTERM` ran doctest's handler and printed a second summary; the child now takes the default disposition.

## What did we discover

- **The next load published what a save had refused to record** (`stage-e/s2-nextload-probe.txt`). That led to S2's marker, with its limit stated in `02`.
- **`Settings` cannot take the marker:** it rewrites from memory, so a key the record has and the file lacks is a reset, not a loss (ruled 01:20 UTC).
- **New status classes need the scraper's skip list too.** `Scraper.cpp` skipped `REQ_IO_ERROR` per game (`:372`, `:631`), so S12 added the two new classes there, or a 503 would have become a per-game error.
- **`Retry-After` is read at two sites** (`:356`, `:628`); the brief named one.
- **`getMD5`'s pipeline exit is `md5sum`'s** without pipefail, so S10's exit adds nothing there; S3's reader of the digest stays the check.
- **The Wi-Fi page's completions are safe by the window's shape** (PL-21, withdrawn): only the top page is updated or receives input, and every bulk deletion goes from the top.

## What adjustments are needed

- **For the integration window** (all `fix-walk-pending-image`):
  - S1: clear HOSTNAME, reboot, read the settings and `system.hostname=`;
  - S6: the Wi-Fi page with no network (the dialog's frame);
  - S10: the BIOS page with a check that fails;
  - S12: the recovery dialog in its three outcomes, and ScreenScraper's three transport sentences;
  - S14: the self-signed listener, CANNOT on this host (T20's `guest-cycle/scripts/tls-probe.py` shape);
  - and `time-to-play` on the image.
- **For the OS round** (#695): #1208 (the seed before the lock), #1209 (`wifictl`'s device guard), #1210 (the key on argv, with #1204's page half), #1211 (`chksysconfig backup`'s name).
- **For #585:** the lines S4 and S7 touched are upstream's (`renameFile`, `HttpReq`'s header, response code, list and body), as is S3's.
- **No change to the remaining plan otherwise.**

## Instruction recommendations

Proposals for the coordinator (Instruction-Recommendations mode). No rule file was edited by this lane.

1. **A number in a record is quoted from the tool that counted it**, never composed. `engineering-practices.md` § Verify the artifact covers claims about behaviour; this is the same rule for counts. The guard here is the build script's `TOTAL` line. A rule line, or a lint that compares a record's stated total with its log, would generalise it.
2. **A syntax check for EmulationStation sources on a host without the image's toolchain.** `tools/es-syntax-check` exits 2 here, and the brief's fallback was "read twice". `stage-e/syntax-check.sh` with `stage-e/fakes/` is a candidate for that tool's host mode. It checks the file's own C++ only, which it says.
3. **A pin-behaviour stub is checked against the pin before its FAIL is recorded.** S11's incomplete stub showed that a stub's FAIL can be the stub's own. A cheap control: run the stub's cases on the pin's lifted output where one exists, as `stage-b/positives/lifted.out` did.

## Time to play

**Measured:** nothing after the fixes. The integration build's `time-to-play` is the measurement; T18's figures for the pin stand (0.56 s, 1.58 s, 1.01 s).

**Where this slice's changes sit, by reading:**
- **`Settings::saveFile` now waits for the settings lock** (S8, up to 5 s). Its callers are a page's close, the F3 key and the exit's `LastSystem` (`ViewController.cpp:93`, `:911`); none is in `FileData::launchGame`. That is the same place `SystemConf`'s save already waited at the pin.
- **The launch's BIOS check** (S10's follow-up) runs only with `CheckBiosesAtLaunch`, off by default, and with `ran` false it now adds nothing.
- **At start:** the narrowing (S5) is one `chmod` per store copy, once. The sweeps (S9) are one directory read per store at start and after each save.
- **The peer's verification** (S14) is on HTTPS requests, none of which is between the press and the first frame.

## Scoped audit findings (Step 2.5)

- **AC conformance:** PASS. #1184 is at Phase 7, with `tools/lint-audit-artifacts` at the resolution phase PASS and against #1184 PASS (`stage-f/`). `box-check` reports 0 fail. The bugs carry `fixed-at-es` and stay open until the pin moves.
- **Cornerstone spot-check:** PASS.
  - Every new player sentence has its French in the same commit, and `es-untranslated` names none of them (S6, S12, S10's follow-up).
  - No stream added a non-ASCII comment (each `stage-e/sN-checks.txt`).
  - The words are the brief's proposed ones (D-UI-112).
- **Interaction-defect scan:** PASS with three notes:
  - the sweeps leave `.unrecorded`, the shared names and `chksysconfig`'s name alone (S9's case);
  - the recovery outcome and the marker are independent (S12 sets one per start, the marker per save);
  - the new statuses meet the scraper's skip list (S12).
- **Futro prediction verification:** n/a (no futro for this slice).
- **Housekeeping (full-suite scan):** PASS. `TOTAL: 278 test cases in 7 binaries`, 0 failed, at the ES tip.
- **Harness self-coverage:** PASS.
  - The syntax check, `kill-writer.py --after-start` and the `TOTAL` line were each seen to do their job: a misspelt copy fails; 42 leftovers before S9 and 0 after; 277 matched the recomputed sum.
  - The listener positive is the one check this host cannot give (S14).

## Code-verifiable state

| Stream | ES commit | Tests added (each binary's own count) | Cases at the step | Failed |
| --- | --- | --- | --- | --- |
| S1 | `ba0e82c1f` | `es-unit-tests` +1, `es-conf-tests` +8 | 230 | 0 |
| S2 | `8cf52e263` | `es-conf-tests` +2 | 232 | 0 |
| S4 | `f7c16144d` | `es-fs-tests` 8 (new) | 240 | 0 |
| S5 | `94791c4ed` | `es-file-tests` +3, `es-conf-tests` +1 | 244 | 0 |
| S3 (merged) | `13a688804, merge f2561bbe4` | `es-unit-tests` +4 | 248 | 0 |
| S6 | `00669ccd9` | `es-unit-tests` +1 | 249 | 0 |
| S7 | `8629d5d08` | `es-unit-tests` +3 | 252 | 0 |
| S2, marker | `eeeaa462c` | `es-conf-tests` +1 | 253 | 0 |
| S8 | `80c8cbcaa` | `es-settings-tests` 4 (new) | 257 | 0 |
| S9 | `c4341c335` | `es-file-tests` +1, `es-conf-tests` +2, `es-settings-tests` +1 | 261 | 0 |
| S10 | `31b49999e` | `es-unit-tests` +4 | 265 | 0 |
| S11 | `eeee95265` | `es-unit-tests` +2 | 267 | 0 |
| S12 | `e38dcdefd` | `es-unit-tests` +5, `es-conf-tests` +1, `es-settings-tests` +1 | 274 | 0 |
| S10, follow-up | `a73ed9efc` | `es-unit-tests` +1 | 275 | 0 |
| S13 | `44d3c7e25` | `es-scraper-tests` 2 (new) | 277 | 0 |
| S14 | `3ae9610b0` | `es-unit-tests` +1 | 278 | 0 |
