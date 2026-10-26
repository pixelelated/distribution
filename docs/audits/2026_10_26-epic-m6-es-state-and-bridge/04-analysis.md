# Analysis — M6.P2 T21, EmulationStation's state primitives and its bridge to the OS (#668)

The first reader's analysis (Opus 5.5), written after stages A and B and the first guest window, before any seat saw the packet. § Second opinion follows the seats.

## Executive summary

The fork's own state work holds where it was built to.
- **`AtomicFile::writeText`, `SystemConf`'s locked save and both recovery ladders** keep the old or the new file whole when killed at every one of 99 steps. On the image, each ladder recovered a cut or emptied store and told the player once.

What does not hold is at the joins between parts:
- **The shell and the recorder:** the shell's writers seed a missing `system.cfg` before the record is consulted, and the interface then records the seed over the player's record (L-10).
- **The scraper's file names and the shell:** the scraper hands a ROM's file name to `sh` inside double quotes for every `.7z` it hashes, as root, and `7zr` ships (L-01).
- **A download and the file it replaces:** a download removes the file it will replace before a byte arrives, so a failed re-scrape loses the art (L-03).
- **The Wi-Fi script and the page:** `wifictl` exits 0 with no Wi-Fi device, and the page says CONNECTED (L-22).
- **The key at rest:** `system.cfg`, which holds the Wi-Fi key, is 0645 on the image and its seed ships so (L-21).

Smaller items:
- the client reads past curl's header buffer (L-02);
- an empty value reads as its default, so D-NET-009's hostname shows BATOCERA (L-15);
- a non-numeric `led.colour` throws out of the LED page (L-16);
- two executors read a failure as success (L-17, L-18);
- a kill's temporaries are never swept (L-09).

#1154 is cited, not re-found. Its fix's design question goes to the pause.

## Acceptance-criteria scorecard

| # | Criterion (#668's body) | State at stage C | Evidence |
| ---: | --- | --- | --- |
| 1 | the folder holds `00` to `05` | `00` to `04` written; `05` at stage C's end | the folder |
| 2 | the lint `PASS` | `--phase pre-issue` at stage C's end; resolution at close | — |
| 3 | `review-plan.json`, two seats, provenance, the manifest's scan, four keyed invokes | stage C | `second-opinions/` |
| 4 | the punch-list issue at Phase 7 | stage D onward | — |
| 5 | the four header fields; the read on the pin's bytes; nothing under `packages`, `projects`, `tools` | the read is on the pin (the diff is empty); nothing changed under the three since `4844a773ca` | `02` R1, R16 |
| 6 | `01` § Scope with the block's output | met | `01` § Scope |
| 7 | § Coverage, 14 rows | met (14 by the acceptance's `awk`) | `02` § Coverage |
| 8 | § The commands, generated, its count asserted | met (143; `--expect 142` exits 1) | `tools/t21-commands.py`, `02` R19 |
| 9 | § The credentials' paths | met, with the four `wifictl` lines as the ruling asks | `02` § The credentials' paths |
| 10 | § The writers, generated, its counts asserted | met (41, 25, 10; drift exits 1) | `tools/t21-writers.py`, `02` R20 |
| 11 | § The readers | met | `02` § The readers |
| 12 | § The client | met | `02` § The client |
| 13 | § The runs | met (R1 to R24) | `02` § The runs |
| 14 | § The guest cycle | first window recorded; G6(a) and G6(b) queued for a second | `02` § The guest cycle |
| 15 | `00` shows nothing of the never-run list | met so far; four keyed invokes at stage C | `00` |
| 16 | `04` § Q1 to Q8; every `bug` with its three lines | Q1 to Q8 below; the bugs at stage D | § The questions |
| 17 | every proof `proved:`; every item `question:`; § What T26 and the OS slices inherit | met in `02`; `question:` in `05` | `02` |
| 18 | the retro | stage G | — |
| 19 | the five checkers and the ES `pre-push-test` | at the hand-back | — |

## Risk assessment

The proposed severities, for the coordinator's ruling at the pause. Each lead's evidence is in `02` § The leads.

| Lead | Proposed | Why |
| --- | --- | --- |
| L-01 | **High** | A file name the player downloaded runs as root through the scraper's `getMD5` for every `.7z` up to 128 MB. `7zr` ships, so the row is live code. The guest's positive is queued for the second window (G6(a)). |
| L-10 | **High** | The player's whole `system.cfg` record (their settings, their Wi-Fi key) is replaced by the image's defaults, and nothing tells them. How often the live file is absent at a `set_setting` after boot is not read (T22's order). |
| L-03 | Medium | A failed re-scrape, with `ScrapeOverWrite` on by default, removes art that was there; nothing says so. The guest's positive is queued (G6(b)). |
| L-21 | Medium | `wifi.key` is world-readable at rest on the image, and nothing on an upgraded device ever narrows the mode. |
| L-22 | Medium | A handheld with no Wi-Fi device (a driver that did not load) says CONNECTED and saves the network as configured. |
| L-02 | Medium | A read past a heap buffer on every response header, its length set by what follows in curl's buffer. |
| L-04 | Low | A data race on `mStatus`; no wrong outcome observed. |
| L-05 | Low | A peer's body in `es_log.txt` (with #1154, anyone's on the path). |
| L-08 | Low | The key on argv of `sh`, `timeout` and `wifictl` for their lifetime, and of `nmcli` for up to 90 s. Only root runs on the image, and the evidence page carried it 0 times on the guest. |
| L-09 | Low | Whole-store leftovers on the card after a kill, never swept. |
| L-11 | Low | A line end becomes a second key; no path sets one. |
| L-12 | Low | The default check is dead; defaults are written, not removed. |
| L-13 | Low | `Settings` takes no lock and has no mutex; D-CLOUD-079's sentence says otherwise. |
| L-14 | Low | Eight state files on the card are written in place. |
| L-15 | Low | BATOCERA shown for an empty hostname. |
| L-16 | Low | A word in `led.colour` throws out of the LED page. |
| L-17, L-18 | Low | A failure read as success: the BIOS check at launch, and a signal read as exit 0 (T20 found the image's `sh` forks, which narrows L-18). |
| L-07, L-19 | Low | A leak, an ignored result. |
| L-06 | — | #1154, cited. |
| L-20 | — | Q7's table, recorded as written. |

## Coverage boundary

- **Read whole:** the 14 at the pin. **Read where a contract crosses:** the neighbours `02` names, and the OS writers at `8ebaf8daad`.
- **Proved on the host:** by fixtures over the pin's own `SystemConf`, `AtomicFileUtil` and `StringUtil`, and by lifted lines where the file needs curl or SDL.
- **Proved on the image:** in the first window (G1 to G5). G6(a) and G6(b) wait on the second window; G6(c) and G7 are `CANNOT` for the slice.
- **Not covered:**
  - which `Settings` setters run off the interface thread;
  - the boot order that would let `set_setting` meet an absent `system.cfg` (T22's);
  - what `wifictl` prints to the journal;
  - the scrapers' behaviour with verification on (#1154's design question);
  - a ThreadSanitizer run over `HttpReq` (curl is not on this host).

## The questions

### Q1 The commands

143 command-running calls (`02` § The commands):
- 93 join nothing;
- 8 join through `shellQuote`;
- 22 join bare, each the first token of a script's own output or a fixed word;
- 16 join inside double quotes, of which the live ones are `7z` over a ROM's path (`ApiSystem.cpp:1527-1528`, `:1578-1579`, `:1659-1660`) and poppler over a manual's (`:2509`, `:2593`). That is L-01.

Script output also flows into `rocknix-es-thebezelproject install` bare (`:1484`) from the bezel list. 82 rows name a script the distribution does not ship (L-20). On the interface thread with no bound: the setters the brief names, and `getBiosInformations` at launch with CHECK BIOS AT LAUNCH on (`Settings.cpp:207`).

### Q2 The client

- One `curl_multi`, driven by whichever thread calls `status()` (`HttpReq.cpp:393-527`): a caller on the interface thread waits the request's whole length, and `timeout` and `stallTimeout` default to 0.
- The server's body for 400 to 503 is logged verbatim (L-05).
- The header callback reads past its buffer (L-02).
- `file://` is closed by the status-0 path.
- The redirect policy is `http,https`, twice; T20's S2 adds `httpsRedirectsOnly` for a credential request.
- **#1154's design question for the pause:** verify the peer by default with the image's CA bundle (present on the image: `g01-identity.txt`), keeping the 2021 exception as an explicit option the scrapers' media downloads set.

### Q3 The credentials' paths

`02` § The credentials' paths, 21 rows:
- **The Wi-Fi key:** on argv of three processes on the guest (L-08); in a 0645 file at rest (L-21); typed in the clear in a popup that has no masking mode.
- **The scraper's pair and account:** on every query, to an unverified peer. `ssid=<username>` and `devid` are unmasked in the LogDebug URL line.
- **The root password's default:** `linux`, shown on a row (`GuiMenu.cpp:3209`, T26's).
- **The read filter's blind words:** `IGDBSecret` and `ScreenScraperDevId` appear in no log line of these files.

### Q4 The writers

`02` § The writers:
- the lock asymmetry, with D-CLOUD-079's sentence (L-13);
- the shell's writers keep the file whole when killed (`shell-writers.out` K1 to K3), and their missing `fsync` is covered on ext4 by `auto_da_alloc` for a rename over an existing file;
- the seed before the record (L-10);
- the modes: 0645 from the seed, kept by every writer (L-21);
- the `.backup.tmp` sweep matches only the old name (L-09);
- eight in-place `writeAllText` state files (L-14).

`Already written:` for L-10 and L-21 is the devices whose record or mode already carries what the old code wrote. Each bug's trace says how its fix treats them.

### Q5 The readers

`02` § The readers:
- `parseKeyValues` drops an empty value (L-15), keeps a BOM in the first key and a carriage return in the value, and keeps the last duplicate;
- the ladder's cases are tested (24 + 10) and pass;
- `Settings::loadFile` has no test, and the image showed it recovering (G4b);
- the player is told once, in plain words.

### Q6 What a failure reads as

- the enumeration executor's discarded exit (L-17);
- the eleven exit reads without `WIFEXITED` (L-18);
- `wifictl`'s exit 0 with no device (L-22);
- `cloud_oauth close` ignored (L-19);
- a `LockBusy` save keeps its change in memory and says nothing on screen (`SystemConf.cpp:309-311`): the next save writes it.

### Q7 The dead paths

82 of the 143 command rows name a script the distribution does not ship at `8ebaf8daad`. Where `isScriptingSupported` has a gate (`ApiSystem.cpp:2335-2440`), the executable it checks is absent too: `BATOCERASTORE` checks `batocera-store` and `AUDIODEVICE` checks `set-audio`. `batocera-storage-manager` and `keyboardToPads` have no `ScriptId` gate there; whether a page on this image reaches them is T26's to read. Recorded as written (D-WORKFLOW-209's shape).

### Q8 The harness

- **What holds:** `AtomicFileTests` (24) and `SystemConfTests` (10) prove the ladder and the locked save, and pass at the pin. `tools/settings-modes-test` proves the shell writers' modes (#421). `tools/last-good-scripts-test` proves the shell's cut-file handling under busybox.
- **What is missing:**
  - nothing tests `Settings`;
  - nothing tests a kill at every step: this slice's `kill-writer` fixture is the first, and passes;
  - nothing tests the seed against the record: `shell-writers` S1 is the first, and fails;
  - `tools/vm-upgrade-rehearsal` seeds neither `.backup`;
  - `tools/cloud-input-test` drives `wifictl` on the host only.
- **The new cases this slice would add:** the kill sweep, S1, U1 to U3, and the four lifted cases, each failing on the pin where it is a lead.

## Renovation face

### Q1 Modernize

- One process reader for every executor, with a cap that keeps a line's head, `WIFEXITED`, and the exit returned (T20's PL-08, deferred here).
- An argv executor for every command that takes a string from outside the program (`WifiScanProcess` is the model).
- `HttpReq` with a thread of its own, or at least bounded waits off the interface thread.

### Q2 Standards

- **`engineering-practices.md` § Guards must fail closed:** L-17, L-18, L-22.
- **§ The last known good state is a record:** L-03, L-10.
- **`es-code-traps.md` § A pooled connection:** the scraper's probes.
- **D-CLOUD-079:** L-13.

### Q3 Bugs

- **High:** L-01, L-10.
- **Medium:** L-02, L-03, L-21, L-22.
- **Low:** L-04, L-05, L-07, L-08, L-09, L-11, L-12, L-13, L-14, L-15, L-16, L-17, L-18, L-19.

### Q4 Package currency

curl 8.21.0 on the image. Nothing in these files vendors a package.

### Q5 Efficiency

Every page close writes both stores and, for `SystemConf`, takes the lock twice and `fsync`s up to four times: the save, then the record when it would change. That is the time-to-play line the retro measures.

### Q6 Dead ends

L-20's 82 rows. The Windows-only branches (`:639-645`, `Win32ApiSystem.cpp`) are recorded, not dead on Windows.

### Q7 Clarity and structure

- `ApiSystem.cpp` is 3,519 lines of five kinds of work.
- `applyChanges`' dead default check (L-12) and the `removeID` sentinel (`SystemConf.cpp:359`) read as intent they do not have.

## Instruction File Recommendations

### Coverage gaps (would have prevented)

- A rule beside D-CLOUD-078: a writer that seeds a file from defaults takes the same lock as the writers and consults the record first.
- `es-code-traps.md`: curl's header callback buffer is not NUL-terminated.

### Codification gaps (proposals for the coordinator)

- A `SettingsTests.cpp` in the unit set, beside `SystemConfTests.cpp`.
- The kill sweep (`stage-b/positives/kill-writer.py`) as a standing tool for every writer of a store.

## Quality self-check

- Every figure here was produced by a command at the hash it names; three of the brief's comments were corrected that way.
- One misread was caught and redone (the CR-terminated serial lines in G1's comparison); both runs are kept.
- No lead is called a finding without its proof cell; the closed leads say what closed them.
- G6 and G7 were not run in the first window, and the reason is written.
