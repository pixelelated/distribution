# Mini Retro: T26, EmulationStation's main menu, GuiMenu (#673)

**Completed:** 2026-10-27.

**Scope:** `es-app/src/guis/GuiMenu.cpp` and `GuiMenu.h` at the ES pin `16dbac5211`, Independent depth (one seat, GPT-6 Astra, two keyed calls). The artifacts: the audit `docs/audits/2026_10_27-epic-m6-es-guimenu/`, the audit issue #1213, one guest window (G01 to G12), and the nineteen bugs #1215 to #1233. Thirteen streams ran under the stage-D ruling (#673, 09:17 UTC) and the stream brief `docs/reviews/briefs/t26-streams.md` at `4bd066551a`.

**Branches:**
- the ES branch `feature/m6-es-guimenu-673` (pixelelated/emulationstation): 14 commits, `70a00ad13` to `757f5370e` (thirteen streams; S3 in two, its second test only, as ruled 09:51 UTC);
- the distribution branch `feature/m6-es-guimenu-673`: the records (`stage-e/`, `02` § The streams, `05`'s gate and index, `00`), the menu map's three changes, and this retro.

**Delta** (counted by `git diff --name-status 16dbac5211 HEAD` and by each tool's own line):
- 24 files and 3,095 lines added, 234 removed;
- 14 new tests under `tests/`, and 5 existing tests taught the changes (`cloud-oauth-lifetime`, `cloud-content-selection`, `cloud-set-systems-quoting`, `credential-quoting`, `CloudTextTests.cpp`);
- `tools/t26-build-tests.sh`: `TOTAL: 222 test cases in 4 binaries`, against 221 at the pin;
- the stream checks run 24 harnesses, all rc 0;
- `es-untranslated`: 746 fork strings with French, against 706 at the pin;
- credential-quoting: 9 of 9 sites quoted (`ledcontrol` gained);
- `t26-pages.py --listed`: interface-thread unbounded starts at the listed cloud sites from 15 to 0, and file-wide from 116 to 100, the 100 listed by site.

## What worked well

- **The before had to fail, and a constructed negative had to fail too.** This caught defects in my own tests every few streams:
  - S2's path test passed the pin twice before failing it for the right reason, and passed a constructed negative once.
  - S5's tool would have read 0 for code it could not see.
  - S12's killer could not see stdio at all and "passed" over zero kill points.
  - S3's test checked saves but not loads.
- **Stores with the real stores' rules.** Modelling `SystemConf::set`'s no-op on an unchanged value and `Settings`' default elision drove two decisions: S3's old-key mirror (ruled 09:51 UTC) and S9's correction of the timezone lead, which had been a call, not a write.
- **Reading each reader before a change.** S3 read `game_setting`'s fallback. S4 read the editor's write-through. S5 checked `cloud_remote`'s and `cloud_setup`'s exit codes. S9 read `powerstate.sh`'s default and `AudioManager`'s reset. S8 read batocera's `Platform.cpp` before naming the upstream.
- **Generated, not retyped.** S7's 33 script lines and their test citations came from the scripts by a generator. The bugs' bodies came from `05` by script.
- **Questions on #673 with a recommendation.** S3's mirror, S5's spinner exception and S7's rclone labels were each ruled within minutes.

## What was harder than expected

- **Turns ended on a plan.** At 10:20 the session stopped on "next is S7" with no checkpoint posted, and sat 28 minutes until the coordinator's 10:49 message. The checkpoint was posted, a memory written, and every later stream ended on its post.
- **A record command in the wrong worktree.** S5's record ran without a `cd`, so the work-log entry and its index landed in `m6-build-engine-652`. Both were restored there and nothing was committed; the friction log has the line.
- **Composed totals, again.** The S12–S13 checkpoint said 13 new tests and 6 changed; the count is 14 and 5. It is corrected in the hand-back. This is T21's lesson recurring on test counts instead of case totals.
- **Extractors over a 12,000-line file.** Each one met a different trap:
  - unbalanced `#if`/`#else` branches;
  - braces and `;` inside strings;
  - an apostrophe in a comment;
  - a forward declaration taken for the definition;
  - the setup wizard's own FINISH, matched in place of the relink's.
- **The stand-in syntax check can't compile `Platform.cpp`.** Its SDL fake lacks `SDL_PushEvent`; S8's edited function was compiled by its test instead.
- **Two acceptance checkboxes claim pin behaviour that never happened.** #1224 expects `es-untranslated` to name phrases that were never msgids. #1230 expects a pin timezone write over a stored value, which was a no-op set. Both are left open, with a reword asked of the coordinator.

## What did we discover

- **Quoting needs a run, not a read.** The brief's literal "`shellQuote` on the argument" for the LED colour leaves `$( )` live for the outer shell, and `credential-quoting.py` passes that half-quoted form. Only S10's run in bubblewrap tells the two apart.
- **Settings keeps no OFF.** A store that drops default values can't say "absent", so read-both-write-new needs the old key kept in step (S3, ruled).
- **`GetShOutput` is ROCKNIX's own,** absent from batocera, so its #585 line names ROCKNIX alone.
- **Two dead fallbacks:** `cloudContentSystemPicker`'s absent-`cloud_scan` branch (its only caller stops first), and, at the pin, `cloudOpenTransfer`'s, which S13 removed.
- **`executeScriptLegacy` echoes each line to stdout unmasked,** a channel for a create's credentials. S8's reader avoids it; the function itself is upstream's and stays.

## What adjustments are needed

- **For the integration window** (`fix-walk-pending-image`):
  - G08: the relink's not-answering dialog (S2);
  - G03 and G04: `es_settings.cfg` and `get_setting videofilter` (S3);
  - the journal after an unchanged DEVICE PASSWORD close (S4);
  - a sign-in's start timed (S5);
  - G10's three attempts (S6);
  - G11 in French: the provider list and CONNECTED TO (S7);
  - the stores' mtimes after no-change visits (S9);
  - S11's toasts and FINISH's refusal.
- **For the coordinator:** reword #1224's and #1230's first checkboxes (proposals on each issue).
- **For the interface slices:** the 100 interface-thread starts in `stage-e/s5-other-starts.txt`, and the picker's dead fallback (S13's note).
- **For #585:** the lines in `02` § The #585 lines owed (S3's two, S8's, S9's two, S10's).
- **No change to the remaining plan otherwise.**

## Instruction recommendations

Proposals for the coordinator. No rule file was edited by this lane.

1. **A test's negative is part of its first commit.** Every positive here needed a constructed failure before its PASS meant anything, and four tests were wrong until one ran. `engineering-practices.md` § Guards must fail closed says "prove the guard fires"; the stream brief could ask for `sN-after.txt` to carry at least one constructed negative's FAIL.
2. **A record step that runs from a fixed directory is a script with the `cd` in it.** The S5 slip had the same shape as T21's "a script that did not reproduce its output": a manual step whose environment was assumed.
3. **Quoting through nested shells is checked by running the command.** `credential-quoting.py` cannot see an outer shell. `tests/led-color-quoting.py`'s shape (build as written, run as `system()` does, in bubblewrap, a canary and a recording stub) generalises to every `sh -lc "…"` site.

## Time to play

From `docs/vm-qa-log.md`: interface to a game's first frame was 0.6 to 1.11 s in September's rows; it reads `Not measured` on 2026-10-14 and 2026-10-16. Nothing here was built into an image, so neither number is measured for this slice. The integration image's `time-to-play` run is owed with the window. The three costs `03` § 3.6 named, and what the streams did to each:

- **The main menu's build at START** (`GuiMenu::GuiMenu`, `:160-277`): unchanged. It starts no process.
- **A page's close before a launch:** `GuiSettings::save` still writes both stores on a close, and `SystemConf` writes only a changed key. S9 removed SOUND SETTINGS' two writes at open, which were the no-change `es_settings.cfg` rewrite G05 saw. It also removed the relink Wi-Fi page's association on an unchanged close (a `wifictl` connect under `networkApplyWifi`'s spinner, which the code's comment puts at up to the better part of two minutes) and the timezone set over a stored value, which had been a no-op. The SECURITY page's `setrootpass` on every close is BATOCERA-only and not built here.
- **Opening a cloud page:** S5 put the hub's and CLOUD CONNECTIONS' `cloud_remote list` reads on a worker, and every other listed read under a spinner, with a 5 s deadline. The hub's `cloud_setup --info` (bounded at 10 s, not in the listed sites) is unchanged. None of these sits between a launch press and a frame.

## What T31 to T37 inherit

`02` § What T31 to T37 inherit, with what the streams made of it:

- **The page builders' pattern** (§ The transitions): unchanged. S1 holds the repair picker to it.
- **The rows' store rule:** a key is written where its reader reads it, and read from the old place while the new is absent (S3). Where the store keeps no defaults, the old key is kept in step (ruled 09:51 UTC). A row writes only when the control moved (S9).
- **The readers' rule:** a file another process writes is read uncached, the regular-file test included. An image a page may still hold is asked for by its own path (S6).
- **The quoting function:** `Utils::String::shellQuote` alone; `cloudShellQuote` is gone (S8). A command run through a second shell is quoted for both, and is checked by running it (S10).
- **The commands' reader:** a cloud read goes through `cloudHelperLines` (argv, a 5 s deadline) under `cloudFetchThen`'s spinner (S5). A change goes through `cloudRemoteRun`, whole and with its status, with one `OK=` parse (S8). `GetShOutput` keeps every byte (S8).
- **The words:** a script's player sentence goes through `CloudText::scriptLines` or `whySentences`, with its French (S7). The Wi-Fi verdict is one composer (S11).
- **The upstream hunks table:** `02` § The merge debt, with `cada856d8` first. The #585 lines are in `02` § The #585 lines owed.

## Scoped audit (Step 2.5)

- **AC conformance: PARTIAL.** Every bug's host criteria are ticked from `stage-e/` artifacts. The guest criteria wait on an image (`fix-walk-pending-image`). #1224 and #1230 each keep one checkbox open for a reword.
- **Cornerstone spot-check: PASS.**
  - `bugs-are-agent-first.md` rule 6 was applied to the upstream and ROCKNIX rows, each with a #585 line.
  - D-UI-112 words were built as proposed.
  - D-UI-039: the map was updated for S2 and S11, and `es-menu-map-check` reads 0 missing at every stream.
  - `Already written:` was answered in every bug and in `02`.
- **Interaction-defect scan: PASS.** S11's new call broke S9's harness, and the next stream's checks caught it. S5's cancel ordering was checked against a serve launched before it.
- **Housekeeping (full suite): PASS.** 24 harnesses and 222 unit cases rc 0 at `757f5370e`.
- **Harness self-coverage: PASS.** Each new test has a constructed negative in its `sN-after.txt`.

## Code-verifiable state

| Stream | Bugs | ES commit | Test |
| --- | --- | --- | --- |
| S1 | #1215 | `70a00ad13` | `tests/cloud-setup-repair-lifetime.py` |
| S2 | #1216 (+PL-15) | `03183f899` | `tests/relink-row-names.py` |
| S3 | #1217, #1218 | `d9bcdfb8a`, `2b50bf112` | `tests/upstream-row-stores.py` |
| S4 | #1219 | `e96222310` | `tests/device-password-apply.py` |
| S5 | #1220 | `b7de744aa` | `tests/cloud-helper-bounds.py` |
| S6 | #1221, #1222 | `aca4076c5` | `tests/stale-file-reads.py` |
| S7 | #1223, #1224 | `072278be9` | `tests/script-text-french.py` |
| S8 | #1225 (+PL-21) | `a5d2d3756` | `tests/command-readers.py`, `tests/shell-quote-equality.py` |
| S9 | #1226, #1230 | `408f7c122` | `tests/no-change-writes.py` |
| S10 | #1227 | `01f33e33e` | `tests/led-color-quoting.py` |
| S11 | #1228, #1229, #1232 | `fb43038be` | `tests/player-words.py` |
| S12 | #1231 (#1186) | `2dd46a3e3` | `tests/theme-set-writer.py` |
| S13 | #1233 | `757f5370e` | `tests/cloud-scan-absent.py` |
