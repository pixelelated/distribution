# Second opinion (Phase 4.6), M6 T21: EmulationStation's state primitives and its bridge to the OS, in pixelelated's EmulationStation fork

You are one of two independent reviewers for a read-only renovation audit of 14 files, read under a **security and state-preservation lens**. They total 9,249 lines at the EmulationStation commit `16dbac5211` (the distribution pins that commit).

- **The shell bridge:** `ApiSystem.{h,cpp}`. Four executors (`popen` or `system()`), and every page's command built from strings, some of them a player's.
- **The network client:** `HttpReq.{h,cpp}`. One process-wide `curl_multi` with no thread of its own.
- **The two stores and the fork's atomic writer:** `Settings.{h,cpp}` (`es_settings.cfg`, EmulationStation's own), `SystemConf.{h,cpp}` (`system.cfg`, the launch scripts' store), and `AtomicFileUtil.{h,cpp}` (temp-and-rename, a pid lock shared with the shell, the recovery ladder).
- **The Wi-Fi page** `GuiWifi.{h,cpp}`, and **the scraper's credentials** in `ScreenScraper.{h,cpp}`.

**What ships.** The product is an immutable handheld OS; a person updates it in place and keeps `/storage`.

- EmulationStation is its interface, at 640x480 on the smallest panel, run as root.
- The shell scripts that also write `system.cfg` (`001-functions`, `chksysconfig`, `wifictl`, `post-update`) are another slice's files, read here where they meet this code. Their lines are the distribution commit `8ebaf8daad`'s.
- The rules the code answers to are named in `03` § 3.2.

**What you get.**

- The first reader is another lab's model. You get its `02-forward-audit.md`, `03-retrospective.md` and `04-analysis.md` whole.
- Then context: the brief's questions, and the register rows the code cites.
- Then the host fixtures' outputs and the guest records.
- Then six files whole and line-numbered: `AtomicFileUtil.{h,cpp}`, `SystemConf.{h,cpp}`, `Settings.cpp` and `HttpReq.cpp`.
- Then **line-numbered excerpts** covering every line the analyses cite, with eight lines of context:
  - `ApiSystem.cpp`, `GuiWifi.cpp`, `ScreenScraper.cpp`, `HttpReq.h`, `Settings.h`, and the neighbours the analyses cite (`StringUtil.cpp`, `Scraper.cpp`, `FileSystemUtil.cpp`, `TextEditComponent.cpp`, `main.cpp`);
  - the shell writers at `8ebaf8daad`: `001-functions` and `wifictl`.
- **When a claim needs lines outside the packet, say `outside the packet` and do not guess.**

**Masking.** Every section was passed through a mask that replaces a value after `key=`, `key:`, `token=`, `user=`, `pass...=` or `psk=` with `***`; a `***` is the mask, not the code. The packet was scanned for credential shapes before it left; no hit was a value.

**Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong. Its line numbers are the pin's.

**What was run.** Nothing can be run for you.

- The unit tests were built on the host and pass at the pin.
- The fixtures ran the pin's own `SystemConf.cpp`, `AtomicFileUtil.cpp` and `StringUtil.cpp`, or lines lifted verbatim where a file needs curl or SDL. The shell writers ran at `8ebaf8daad`, unrewritten, in a sandbox. Their outputs are in the packet.
- A guest window ran on an image whose EmulationStation is a **later composition over the pin**, while its shell scripts are `8ebaf8daad`'s bytes. So a frame there is the image's, and the first reader says which code each guest proof exercised.

Answer these first, in this order:

1. **The commands (Q1; L-01, L-17, L-18, L-20).**
   - Is every double-quoted external string listed, and is L-01 reached as `02` says: the scraper's `getMD5` → `7zr` over a ROM's name, as root?
   - Is any bare join attacker-shaped after all: the Bluetooth MAC, the storage id, the bezel names from a network list?
   - Is anything blocking the interface thread with no bound that `04` § Q1 misses?
2. **The client (Q2; L-02 to L-07).**
   - Is L-02 (the header callback's read) real, and how far can it read?
   - Is L-03 (a download removes its target first) reached by default as `02` says?
   - Is the `file://` closure right: does a `file://` transfer really end with response code 0 and its bytes removed?
   - Is the `format` and `Content-Type` path closure right?
   - What does #1154's fix (verify by default, an explicit exception for media) break that the first reader does not say?
3. **The credentials (Q3; L-08, L-09, L-21).**
   - Is every sink of the Wi-Fi key, the scraper's pair and account, and the root password's default listed, at its line?
   - Is L-21 (0645 at rest, kept by every writer) right, and what else reads `system.cfg`'s mode?
4. **The writers and the readers (Q4, Q5; L-10 to L-16).**
   - Is L-10's chain real: the seed copied before the lock and the record, then recorded over it by the interface's load? Is there a path the first reader misses by which `system.cfg` is absent when a shell writer runs?
   - Is `SystemConf`'s save safe against every other writer of `system.cfg`: the shell under the same lock, `chksysconfig` with none, `post-update`'s `sed -i`?
   - Does `Settings` lose a change or a record anywhere: a save from a worker thread, a kill between the two writes, a load that refreshes the record from a file that parsed but is wrong?
   - Are `parseKeyValues`' drops (an empty value, a BOM, a carriage return) and `applyChanges`' rewrite safe for every key the shell writes?
5. **What a failure reads as (Q6; L-17, L-18, L-22).**
   - Is L-22 (`wifictl` exits 0 with no device, and the page says CONNECTED) reached as described, and is the same shape anywhere else?

Then:

6. **Refute or confirm each lead L-01 to L-22** in `02`: *confirmed*, *narrowed* (say how), or *refuted* (with the line). For the High and Medium ones in `04` § Risk assessment, also judge the severity, the fix a stream would make, and its `Already written:` line: what the code before a fix has already left on devices, and how the fix treats it.
7. **What the first reader missed:**
   - a credential reaching a log, a command line, a file or the screen;
   - a reader that turns a failure into a success or a number;
   - a writer that can lose the record;
   - a pointer used after its owner goes;
   - a string that promises what the code does not do;
   - a bound missing on the interface thread.

**Output:**

- Numbered items `{PREFIX}-1`, `{PREFIX}-2`, ..., grouped under the seven headings above.
- Each item gets one line saying *confirmed / narrowed / refuted / new*, then the `file:line` evidence, then two to five sentences.
- Do not restate the packet, and do not reproduce long code.
- Keep the whole reply under about 8,000 words.


## The first reader's 02-forward-audit.md (whole)

# Forward audit — M6.P2 T21, EmulationStation's state primitives and its bridge to the OS (#668)

**Read at:** the pin `16dbac5211` (the ES worktree, clean at the pin) and the distribution at `4844a773ca` (`8ebaf8daad`'s scripts). All 14 files were read whole (`00` § Stage B). Every count here was made by a command at those hashes; the runs and their outputs are in § The runs and under `stage-a/` and `stage-b/`.

**`proved:` values:**
- `tree`: read at the lines named;
- `history`: read in the log;
- `tool-run`: a run named in § The runs;
- `fixture`: a host program over the pin's own code, or over lines lifted verbatim, under `stage-b/positives/`;
- `guest`: the window, not yet held;
- `design`: a reading of intent.

Nothing here is yet `fix-unit-test` or `fix-walk-pending-image`.

## Coverage

| Path | Lines at the pin | Read | What it answers | proved |
| --- | ---: | --- | --- | --- |
| `es-app/src/ApiSystem.cpp` | 3,519 | whole | Q1, Q3, Q5, Q6, Q7: the 143 command-running calls (§ The commands), the exit reads, the Wi-Fi key's argv, the LED parse, the dead scripts | tree, fixture, tool-run |
| `es-app/src/ApiSystem.h` | 490 | whole | Q1: `getSevenZipCommand()` is `"7zr"` (`:422`); the executors' declarations (`:466-474`) | tree |
| `es-app/src/guis/GuiWifi.cpp` | 607 | whole | Q3: the key's popup (`:360-368`), its save into `system.cfg` (`:392-394`), the scan's argv executor (`:535-582`) | tree, tool-run |
| `es-app/src/guis/GuiWifi.h` | 93 | whole | the scan's ownership (`:53-60`) | tree |
| `es-app/src/scrapers/ScreenScraper.cpp` | 1,092 | whole | Q2, Q3: the pair and the account on the query (`:34-45`, `:857-897`); media URLs and extensions from the server's XML (`:722-848`, `:900-928`); the probe without bounds (`:1030-1032`, `:1067-1068`) | tree |
| `es-app/src/scrapers/ScreenScraper.h` | 104 | whole | the API base `https://api.screenscraper.fr/api2` (`:79`) | tree |
| `es-core/src/HttpReq.cpp` | 644 | whole | Q2: every option (§ The client), the header callback's read (`:579-594`), the download that removes its target first (`:324-345`), the status that one caller completes for all (`:393-527`) | tree, fixture |
| `es-core/src/HttpReq.h` | 180 | whole | the options' defaults (`:45-88`), the user agent (`:30`) | tree |
| `es-core/src/Settings.cpp` | 723 | whole | Q4, Q5: `saveFile` (`:469-540`) with no lock and no mutex, `loadFile`'s ladder (`:549-634`) with no test | tree, fixture |
| `es-core/src/Settings.h` | 165 | whole | the maps (`:147-157`), no mutex | tree |
| `es-core/src/SystemConf.cpp` | 494 | whole | Q4, Q5: `applyChanges` (`:349-421`), the parse and the defaults (`:38-54`, `:73-80`, `:423-437`), the recorder (`:86-112`) | tree, fixture |
| `es-core/src/SystemConf.h` | 94 | whole | the pending changes' contract (`:18-28`) | tree |
| `es-core/src/utils/AtomicFileUtil.cpp` | 829 | whole | Q4, Q5: `writeText` (`:80-185`), `chooseConfig` (`:291-396`), `parseKeyValues` (`:453-469`), `PidLock` (`:549-827`) | tree, fixture |
| `es-core/src/utils/AtomicFileUtil.h` | 215 | whole | the contract each function states (`:30-211`) | tree |

## The leads

Each lead is in one of the brief's four families. Each is read at its lines and carries its proof; a lead is not a finding until stage C's grading and the coordinator's ruling.

| Lead | Q | Family | What | Where | proved |
| --- | --- | --- | --- | --- | --- |
| L-01 | Q1 | a command built from a player's string | A ROM's file name reaches `sh` inside double quotes, which leave `$`, backticks and `\` live. The scraper reaches this for every `.7z` up to 128 MB (`ScreenScraper.cpp:306-308` → `getMD5`), as root. | `ApiSystem.cpp:1527-1528`, `:1578-1579`, `:1659-1660`; poppler at `:2509`, `:2593` | tree; the window's `$(...)` ROM and `ls /usr/bin/7z*` owed |
| L-02 | Q2 | a credential's sink | `header_callback` builds a `std::string` from curl's header buffer as if it ended in a NUL; curl's does not. | `HttpReq.cpp:583` | fixture: `stage-b/positives/lifted.out`, ASan heap-buffer-overflow, READ of size 15 from a 14-byte buffer |
| L-03 | Q4 | a state write that can lose the record | A download removes the file it will replace before a byte arrives. With `ScrapeOverWrite` on by default (`Settings.cpp:198`), a re-scrape whose download fails (404 and I/O errors ignored, `Scraper.cpp:631-635`) leaves the game with no art where it had some. | `HttpReq.cpp:344`, `:328` | tree; the window's 404 from the #1154 endpoint owed |
| L-04 | Q2 | a check whose failure reads as success | One caller's `status()` writes every request's `mStatus` under `mMutex` (`:416-521`), while each request's own thread reads its `mStatus` without it (`:395`, `:640-643`): a data race. | `HttpReq.cpp:395`, `:416-521` | tree; a ThreadSanitizer run needs curl, CANNOT on this host |
| L-05 | Q2 | a credential's sink | For 400 to 503, the server's body goes verbatim into `es_log.txt` at LogError; with #1154 that body is anyone's on the path. | `HttpReq.cpp:439-473`, `:562` | tree (the brief's lead, read) |
| L-06 | Q2 | a credential's sink | #1154 cited: `VERIFYPEER` 0 on every request, `VERIFYHOST` 0 on the client-certificate path. The fix's design question goes to the pause. | `HttpReq.cpp:192`, `:200` | tree (cited, not re-found) |
| L-07 | Q2 | — | `customHeaders`' `curl_slist` is never freed. | `HttpReq.cpp:174-179` | tree |
| L-08 | Q3 | a credential's sink | (Guest: 3 processes carried it; `g03-argv.txt`.) The Wi-Fi key is argv of `sh`, `timeout` and `wifictl` for up to 150 s, then of `nmcli` for up to 90 s (`wifictl:177`). `rocknix-evidence`'s state page keeps `top -b -n 1` (`:71`), whose command column could carry it. `:642`, the brief's unbounded `enable <ssid> <key>`, is in the `#if WIN32` branch and not built on ROCKNIX. | `ApiSystem.cpp:635-637`, `:2328` | tree; the window's masked count of `/proc/*/cmdline` and of `top`'s lines owed |
| L-09 | Q3, Q4 | a credential's sink | A writer killed between its temporary's create and its rename leaves `path`.tmp.<pid>.<n>, which nothing sweeps. Since PL-063 the sweeps remove only the old shared names (`Settings.cpp:557-558`, `SystemConf.cpp:210`). For `es_settings.cfg` the leftover takes the live file's mode with the scraper's account inside. The settings archive takes the stores by exact name (`backuptool:283-292`), so the leftovers stay on the card. | `AtomicFileUtil.cpp:50-64`, `:115` | fixture: `stage-b/positives/kill-writer.out`, 42 of 99 kill points |
| L-10 | Q4 | a state write that can lose the record | With `system.cfg` absent, `set_setting` copies the image's seed before the lock and without the record (T1's file). The interface's next load then records the seeded file over the record, so the player's keys go from both files. | `001-functions:540-543`, `:595` at `8ebaf8daad`; `SystemConf.cpp:232-238`, `AtomicFileUtil.cpp:352-361` | fixture: `stage-b/positives/shell-writers.out` S1 |
| L-11 | Q4 | a state write that can lose the record | `applyChanges` writes `key + val`, so a value with a line end becomes two lines and a second key. No player or network path that sets one was found at the pin (`TextEditComponent.cpp:176-185`; `HttpApi.cpp` writes neither store). | `SystemConf.cpp:386-406`, `:414-419` | fixture: `stage-b/positives/state-units.out` U2 |
| L-12 | Q4 | — | The default check is dead: `defaults.find(key)` with `key = it + "="` never matches, so a value equal to its table default is written rather than removed. | `SystemConf.cpp:366`, `:389-391` | fixture: `state-units.out` U3 |
| L-13 | Q4 | a state write that can lose the record | `Settings` takes no lock and its maps have no mutex. D-CLOUD-079's sentence says EmulationStation's writers "take the settings lock around the read-modify-write"; `SystemConf` does, `Settings` does not. The shell only reads `es_settings.cfg` (`001-functions:622-623`). Which setters run off the interface thread is not enumerated here. | `Settings.cpp:469-540`, `.h:147-157` | tree |
| L-14 | Q4 | a state write that can lose the record | Eight `writeAllText` call sites write a file on the card in place: truncate, unchecked `fwrite` and `fclose`, no `fsync`. `ThreadedCloudSync.cpp:944` is fixed on T18's branch. | § The writers, group 2 | tree, tool-run |
| L-15 | Q5 | a check whose failure reads as success | `parseKeyValues` drops a line with an empty value, so `get` answers the table's default: `system.hostname=`, which D-NET-009 writes on purpose, reads `BATOCERA`. Its readers are `GuiMenu.cpp:9909` (the device-name row, T26's) and `ApiSystem.cpp:2917`. | `AtomicFileUtil.cpp:465`, `SystemConf.cpp:44`, `:428-434` | fixture: `state-units.out` U1 |
| L-16 | Q5 | a check whose failure reads as success | `led.colour` is parsed with `std::stoi` and no catch: a word throws out of the page's build (`GuiMenu.cpp:2989`), and `255,0,165` comes back as white. `setLEDBrightness`'s `std::stoul` is the same shape. | `ApiSystem.cpp:1868-1890`, `:2083-2087` | fixture: `lifted.out` led |
| L-17 | Q6 | a check whose failure reads as success | `executeEnumerationScript` discards the exit: a script that fails or is killed returns the lines it printed, as success. That is `getBiosInformations`, at launch with CHECK BIOS AT LAUNCH on (`Settings.cpp:207`). | `ApiSystem.cpp:2251` | fixture: `lifted.out` enum |
| L-18 | Q6 | a check whose failure reads as success | Eleven `WEXITSTATUS` reads without `WIFEXITED`: a child killed by a signal reads as exit 0, with its lines. `joinWifiNetwork` then reads `joined` from them (`:714-718`). | `ApiSystem.cpp:234` ... `:2291`, `:2319` | fixture: `lifted.out` script; T20's `reader.out` for the legacy executor |
| L-19 | Q6 | — | `cloud_oauth close`'s result is ignored. | `ApiSystem.cpp:593` | tree |
| L-21 | Q3 | a credential's sink | `system.cfg` and its `.backup` are 0645 on the image, and so is the seed it is copied from: world-readable, with the execute bit for others. `wifi.key` is in it, readable by any user. `AtomicFile::writeText` keeps a replaced file's mode (`AtomicFileUtil.cpp:127-147`) and the shell's `prepare_settings_temp` keeps the live file's and the record's shared bits, so neither ever narrows it. Git records the seed as `100644` at `8ebaf8daad` and no recipe `chmod`s it; the installed seed also differs in content (`g01-image-vs-tree.txt`), so a build step rewrites it, and that step's mode is the 0645. Which step is not traced here. | the image's `/usr/config/system/configs/system.cfg` | guest: `g02-modes.txt`, `g03-argv.txt` |
| L-22 | Q6 | a check whose failure reads as success | `wifictl` exits 0 when it has no Wi-Fi device (`:55-56`, T1's file). `ApiSystem::enableWifi` reads that as a connect (`:627-637`, `system() == 0`), and the page then saves `wifi.ssid` and `wifi.key` and says CONNECTED (`GuiWifi.cpp:385-395`). A handheld whose Wi-Fi driver did not load says it joined. | `wifictl:55-56`; `ApiSystem.cpp:627-637`; `GuiWifi.cpp:385-395` | guest: the connect exited 0 with no adapter (`g03-argv.txt`); the page's half is tree |
| L-20 | Q7 | — | 82 of the 143 command rows name a script the distribution does not ship at `8ebaf8daad` (§ The commands' last column). A table, recorded as written (D-WORKFLOW-209's shape). | § The commands | tool-run |

**Read and closed at stage B:**
- **`file://` from a server's media URL:** the transfer leaves curl a response code of 0. `status()` takes that to `REQ_IO_ERROR` (`HttpReq.cpp:435-473`), and the destructor removes the `.tmp` the bytes reached (`:377-378`). So a local file's text reaches only a transient temporary. Proved by tree; the window confirms it with one URL.
- **The server's `format` and `Content-Type` as a path:** `getSaveAsPath` appends them (`Scraper.cpp:779-812`, `:646-676`), but `getGenericPath` does not resolve `..` (`FileSystemUtil.cpp:642-668`). A kernel lookup through `<stem>-image.` fails, since no such directory exists. Proved by tree.
- **The Bluetooth and storage arguments:** they are joined bare (`ApiSystem.cpp:800-816`, `:984`), but each is the first token of a script's own output, a MAC address or a storage id (`GuiBluetoothDevices.cpp:131-137`, `GuiMenu.cpp:3130-3151`). Safe by shape, not by quoting. Proved by tree.
- **`maskSecrets`' `--key`:** excluded on purpose, so `batocera-hotkeys --key` keeps its key name (`StringUtil.cpp:788`; `80f52e500`, #177). Proved by history.
- **The kill-the-writer test (D-CLOUD-078):**
  - every one of 99 kill points across `writeText`, `Settings`' two writes and `SystemConf`'s save leaves the old or the new state whole (`kill-writer.out`);
  - the shell writer killed mid-write, before the rename and after it leaves the old or the new file whole (`shell-writers.out` K1-K3).

  Proved by fixture.

## The credentials' paths

One row per credential kind per sink it can reach. Read at the lines named; values are never printed, names and lines only.

| Credential | Sink | At | Mask there | proved |
| --- | --- | --- | --- | --- |
| The Wi-Fi key | argv | `ApiSystem.cpp:635-637` → `system()` `:2328`: `sh -c`, `timeout 150`, `wifictl connect`; then `connect_wifi`'s `nmcli -w 90 device wifi connect "${SSID}" password "${PSK}"` (`wifictl:177`) | none on argv | tree; guest: 3 processes carried the key in their command lines (`guest-cycle/g03-argv.txt`) |
| The netplay network's fixed key | argv and the keyfile | `create_adhoc`'s and `connect_adhoc_client`'s `802-11-wireless-security.psk "${PSK}"` (`wifictl:195`, `:209`): the sink the brief's pattern missed. They run only when `wifi.adhoc.enabled` is 1 (`:502-511`), where `PSK` is replaced by a fixed value (`:63-66`), so the player's key does not reach them. | none | tree |
| The Wi-Fi key | a file and its mode | `system.cfg` `wifi.key`, written by the page (`GuiWifi.cpp:392-394`) and by `join_wifi`'s `set_settings wifi.ssid ... wifi.key "${psk}"` (`wifictl:460`). The mode is the live file's, or 0644 when ES makes the file new (`AtomicFileUtil.cpp:115`). On the image, **`system.cfg`, its `.backup` and the shipped seed are 0645** (L-21). NetworkManager's own keyfile is 0600. | none at rest | tree; guest (`g02-modes.txt`, `g03-argv.txt`) |
| The Wi-Fi key | a log | the command line through `maskSecrets` (`ApiSystem.cpp:2325`; the `wifictl` rule `StringUtil.cpp:764-784`). The child's stdout inherits ES's, which is the journal. | masked (the command line); what `wifictl` prints is unread | tree |
| The Wi-Fi key | the evidence page | `rocknix-evidence:71`'s `top -b -n 1`, every five minutes (D-SYS-005) | none | tree; guest: 0 of `top`'s 25 lines carried it at the sampled moment, with no adapter; on a device the key lives up to 90 s in `nmcli`'s argv, which the guest cannot show |
| The Wi-Fi key | the screen | the WI-FI KEY popup, typed in the clear (`GuiWifi.cpp:365`, `:367`). Neither popup class takes a password mode (`GuiTextEditPopup.h:15-16`, `GuiTextEditPopupKeyboard.h:13-14`). | none | tree |
| The Wi-Fi key | the packet and the archive | `system.cfg` in the settings archive (`backuptool:286`; its SECRETLIST is T17's, cited) | backuptool's | tree (cited) |
| The scraper's developer pair, compiled | the binary | `SCREENSCRAPER_DEV_LOGIN` returned verbatim (`ScreenScraper.cpp:36-37`), D-WORKFLOW-166's allowed case. Which identity is compiled is the window's to read by name, never printed. | n/a | tree |
| The scraper's developer pair, runtime | a file and its mode | `ScreenScraperDevId`, `ScreenScraperDevPass` in `es_settings.cfg` (`:39-43`), 0644 when new | none at rest | tree |
| Both developer pairs | a query | `devid=..&devpassword=*** at the head of every API URL (`:859-871`, `:885-888`, `:1030-1031`) | n/a (in the URL) | tree |
| Both developer pairs | a log | `Scraper.cpp:524` logs the URL through `maskSecrets` at LogDebug: `devpassword` masked, `devid` not | partial | tree |
| Both developer pairs | the unverified peer | `api.screenscraper.fr` over https, with `VERIFYPEER` 0 (`HttpReq.cpp:192`, #1154) | none | tree; the window's #1154 positive owed |
| The player's ScreenScraper account | a file and its mode | `ScreenScraperUser`, `ScreenScraperPass` in `es_settings.cfg` (`storeInSettings=true`, `GuiScraperStart.cpp:413-420`, `GuiMenu.cpp:8371`, `:8374`), 0644 when new; a kill's leftover temporary too (L-09) | none at rest | tree, fixture |
| The player's ScreenScraper account | a query | `&ssid=&sspassword=*** when both are set (`ScreenScraper.cpp:874-878`, `:890-894`) | n/a | tree |
| The player's ScreenScraper account | a log | `Scraper.cpp:524` masks `sspassword` and leaves `ssid=<username>`; `screenScraperFailureMessage` logs the server's body (`ScreenScraper.cpp:980`), as does `HttpReq::onError` for 400-503 (L-05) | partial | tree |
| The player's ScreenScraper account | the unverified peer | as the pair (#1154) | none | tree |
| The player's ScreenScraper account | the screen | the rows are masked (`addInputTextConfigRow(..., true)`) | masked | tree |
| The RetroAchievements password and web API key (T20's) | a query, the unverified peer | through `HttpReq` (T20's `02` § The credentials' paths, cited) | as T20 found | tree (cited) |
| The root password's default | the screen | `getRootPassword` returns `root.password`, or the literal `linux` (`ApiSystem.cpp:1029-1037`), shown on a row (`GuiMenu.cpp:3209`, T26's) | none | tree |
| The root password | a log | `setrootpass` is a `maskSecrets` word (`StringUtil.cpp:753-762`) | masked | tree |

The read filter's two blind words (the brief's § 1): `IGDBSecret` and `ScreenScraperDevId`. Neither appears in these 14 files' log lines. The packet scan at stage C reads them by name.

## The commands

Generated by `tools/t21-commands.py <W> <D> --expect 143`; the table follows as it printed (`stage-b/commands.md`). Its count is checked two ways:
- **Independently:** 152 occurrences of the five call names outside comments, less the five definition lines and the four `popen`/`system` calls inside the executors' own bodies (2239, 2269, 2300, 2328), is 143.
- **The drift guard:** given `--expect 142`, the generator exits 1.

How to read it:
- **Thread:** every executor runs on its caller's; ApiSystem has none of its own.
- **Branch:** "WIN32 only" means the Windows build's branch.
- **Ships at 8ebaf8daad:** whether a file of that name exists under `projects/` or `packages/`. A compiled binary (`7zr`, poppler's tools) is the window's `ls /usr/bin`.

| Line | Function | Executor | First literal | Joined from outside | Quoting | Output read | Exit read | Thread | Branch | Script | Ships at 8ebaf8daad |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 191 | `setOverclock` | `executeScript` | `batocera-overclock set ` | mode) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-overclock` | no |
| 250 | `backupSystem` | `popen` | `rocknix-sync sync ` | device | bare | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `rocknix-sync` | no |
| 279 | `installSystem` | `popen` | `batocera-install install ` | architecture, device | bare | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `batocera-install` | no |
| 524 | `launchKodi` | `system` | `batocera-kodi ` | commandline | bare | none (inherits stdout) | WIFEXITED then WEXITSTATUS | the caller's |  | `batocera-kodi` | no |
| 573 | `launchCloudSignIn` | `system` | `` | phoneKeyboard | a variable: the command built earlier | none (inherits stdout) | the caller's | the caller's |  | `-` | - |
| 635 | `enableWifi` | `executeScript` | `timeout 150 wifictl connect ` | Utils::String::shellQuote(country)), Utils::String::shellQuo | shellQuote | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 642 | `enableWifi` | `executeScript` | `wifictl enable ` | Utils::String::shellQuote(key)), Utils::String::shellQuote(s | shellQuote | none (system) | system() == 0 (:2328) | the caller's | WIN32 only | `wifictl` | yes |
| 651 | `getWifiSecurity` | `executeScript` | `timeout 15 wifictl security ` | Utils::String::shellQuote(ssid) | shellQuote | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 660 | `connectOpenWifi` | `executeScript` | `timeout 120 wifictl connect-open ` | Utils::String::shellQuote(ssid)) | shellQuote | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 714 | `joinWifiNetwork` | `executeScript` | `timeout 120 wifictl join ` | Utils::String::shellQuote(name) | shellQuote | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 728 | `forgetWifiNetwork` | `executeScript` | `timeout 30 wifictl forget ` | Utils::String::shellQuote(name) | shellQuote | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 771 | `forgetWifiNetwork` | `executeScript` | `wifictl forget_saved ` | Utils::String::shellQuote(ssid)) | shellQuote | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 775 | `connectSavedWifiNetwork` | `executeScript` | `wifictl connect_saved ` | Utils::String::shellQuote(ssid)) | shellQuote | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 800 | `pairBluetoothDevice` | `executeScript` | `rocknix-bluetooth trust ` | deviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 805 | `connectBluetoothDevice` | `executeScript` | `rocknix-bluetooth connect ` | deviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 810 | `disconnectBluetoothDevice` | `executeScript` | `rocknix-bluetooth disconnect ` | deviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 815 | `removeBluetoothDevice` | `executeScript` | `rocknix-bluetooth remove ` | deviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 838 | `getVideoModes` | `executeEnumerationScript` | `batocera-resolution --screen \"` | output | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-resolution` | no |
| 984 | `setStorage` | `executeScript` | `rocknix-config storage ` | selected) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-config` | yes |
| 989 | `setButtonColorGameForce` | `executeScript` | `batocera-gameforce buttonColorLed ` | selected) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-gameforce` | no |
| 994 | `setPowerLedGameForce` | `executeScript` | `batocera-gameforce powerLed ` | selected) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-gameforce` | no |
| 1132 | `setAudioOutputDevice` | `system` | `set-audio set` | selected | single quotes | none (inherits stdout) | the caller's | the caller's |  | `set-audio` | no |
| 1183 | `setAudioOutputProfile` | `system` | `set-audio set-profile` | selected | single quotes | none (inherits stdout) | the caller's | the caller's |  | `set-audio` | no |
| 1484 | `installBatoceraBezel` | `executeScript` | `rocknix-es-thebezelproject install ` | bezelsystem | bare | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `rocknix-es-thebezelproject` | yes |
| 1489 | `uninstallBatoceraBezel` | `executeScript` | `rocknix-es-thebezelproject remove ` | bezelsystem | bare | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `rocknix-es-thebezelproject` | yes |
| 1528 | `getMD5` | `executeEnumerationScript` | `7zr x -so \"` | fileName | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `7zr` | binary: the window's ls |
| 1579 | `getCRC32` | `executeEnumerationScript` | `7zr l -slt \"` | fileName | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `7zr` | binary: the window's ls |
| 1660 | `unzipFile` | `executeScript` | `7zr x \"` | Utils::FileSystem::getPreferredPath(destFolder), Utils::File | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `7zr` | binary: the window's ls |
| 2257 | `executeScriptLegacy` | `executeScriptLegacy` | `` | command | a variable: the command built earlier | every line to func | WEXITSTATUS without WIFEXITED (:2291) | the caller's |  | `-` | - |
| 2504 | `formatDisk` | `executeScript` | `batocera-format format ` | disk, format | bare | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `batocera-format` | no |
| 2509 | `getPdfPageCount` | `executeEnumerationScript` | `pdfinfo \"` | fileName | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `pdfinfo` | binary: the window's ls |
| 2591 | `extractPdfImages` | `executeEnumerationScript` | `pdftoppm -r ` | fileName, page, pdfFolder, prefix, squality | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's | WIN32 only | `pdftoppm` | binary: the window's ls |
| 2593 | `extractPdfImages` | `executeEnumerationScript` | `pdftoppm -jpeg -r ` | fileName, page, pdfFolder, prefix, squality | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `pdftoppm` | binary: the window's ls |
| 2691 | `installBatoceraStorePackage` | `executeScript` | `batocera-store install \"` | name | double quotes | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `batocera-store` | no |
| 2696 | `uninstallBatoceraStorePackage` | `executeScript` | `batocera-store remove \"` | name | double quotes | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `batocera-store` | no |
| 2837 | `setTimezone` | `executeScript` | `batocera-timezone set \"` | tz | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-timezone` | no |
| 3095 | `setJoysticksHotkeys` | `executeScript` | `batocera-joysticks-hotkeys ` | params) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-joysticks-hotkeys` | no |
| 3251 | `getKeyboardtopadDevices` | `executeEnumerationScript` | `keyboardToPads --config \"` | config | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `keyboardToPads` | no |
| 3306 | `setGlobalHotkey` | `executeScript` | `batocera-hotkeys --set --config ` | action), config, key | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-hotkeys` | no |
| 3311 | `removeGlobalHotkey` | `executeScript` | `batocera-hotkeys --remove --config ` | config, key) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-hotkeys` | no |
| 3380 | `saveKeyboardtopads` | `executeScript` | `` | cmd_dev) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `-` | - |
| 3404 | `saveKeyboardtopads` | `executeScript` | `` | cmd_dev) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `-` | - |
| 3416 | `detectEvKey` | `executeEnumerationScript` | `batocera-hotkeys --detect --count 1 --nowait --evformat --device ` | device_path) | bare | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-hotkeys` | no |
| 3476 | `enableService` | `executeScript` | `batocera-services ` | serviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-services` | no |
| 3478 | `enableService` | `executeScript` | `batocera-services ` | serviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-services` | no |
| 3491 | `ejectDrive` | `executeScript` | `batocera-storage-manager eject \"` | mountPath | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-storage-manager` | no |
| 3497 | `mergeDrive` | `executeScript` | `batocera-storage-manager merge \"` | mountPath | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-storage-manager` | no |
| 3503 | `prepareDrive` | `executeScript` | `batocera-storage-manager format \"` | device, fsType | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-storage-manager` | no |
| 3509 | `ignoreDevicePermanently` | `executeScript` | `batocera-storage-manager ignore \"` | deviceId | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-storage-manager` | no |
| 3518 | `nfc_write` | `executeScript` | `batocera-nfc --write \"` | game | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-nfc` | no |

143 rows. Quoting: none joined 93, bare 22, double quotes 16, shellQuote 8, a variable: the command built earlier 2, single quotes 2. Scripts not shipped at 8ebaf8daad: 82 rows.


## The writers

Generated by `tools/t21-writers.py <W> <D> --expect-atomic 41 --expect-writeall 25 --expect-shell 10`; the tables follow as they printed (`stage-b/writers.md`). Given `--expect-shell 11`, the generator exits 1.

The 27 `writeAllText(` lines at the pin are 25 call sites, plus the function's definition and declaration (`FileSystemUtil.cpp:1429`, `.h:71`), which the generator names and leaves out. Sixteen of the 25 are `ApiSystem.cpp`'s sysfs writes. `post-update:101` edits a sysctl file (D-SYS-007), so the shell group carries `:160` and `:202` only.

### 1. `AtomicFile::` at the pin

| Where | Call | Kind | Temp-and-rename or in place | fsync | Lock | Mode | Positive check | A failure leaves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| es-app/src/guis/GuiMenu.cpp:5066 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | none (the journey record, written once per restore) | -1: 0644 when new | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/Settings.cpp:524 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | none | -1: the live file's, 0644 when new | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/Settings.cpp:533 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | none | modeOf(path, 0644) | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/Settings.cpp:617 | copy | write | temp-and-rename, through writeText | file and directory | none | the source's mode | the read's ok and the write's result | as writeText |
| es-core/src/Settings.cpp:631 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | none | modeOf(path, 0644) | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/SystemConf.cpp:91 | PidLock | write | lock file linked into place holding the pid | - | is the lock | 0644 (the lock file) | link() result; a stale holder by kill(pid, 0) | a staging file `.new.<pid>.<n>` when killed between its create and the link |
| es-core/src/SystemConf.cpp:110 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | PidLock /tmp/.system.cfg.lock (5 s) | -1: the live file's; recordLastGood: every copy's | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/SystemConf.cpp:218 | loadUnderLock | write | a recovery written back through writeText | file and directory | PidLock, re-chosen under it | every copy's shared bits | RecoveryWrite::Written | the chosen text read, the file as it was |
| es-core/src/SystemConf.cpp:304 | saveUnderLock | write | temp-and-rename, through writeText, onto the text read under the lock | file and directory | PidLock /tmp/.system.cfg.lock, 5 s | the live file's, or every copy's on a recovery | LockedSave::Written only after the rename | the old file whole; the change kept in memory (LockBusy, Unreadable, WriteFailed) |

### 2. `writeAllText(` call sites at the pin

| Where | What | Temp-and-rename or in place | fsync | Lock | Mode | Positive check | A failure leaves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| es-app/src/CaptureRotation.cpp:175 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/FileData.cpp:2213 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/KeyboardMapping.cpp:426 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/KeyboardMapping.cpp:429 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/ThreadedCloudSync.cpp:944 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/guis/GuiKeyboardLayout.cpp:164 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/guis/GuiMenu.cpp:11587 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/services/HttpApi.cpp:258 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |

Left out: the definition and the declaration, es-core/src/utils/FileSystemUtil.cpp:1429, es-core/src/utils/FileSystemUtil.h:71.

### 3. The shell writers of system.cfg at 8ebaf8daad (T1's files, read here)

| Where | What | Temp-and-rename or in place | fsync | Lock | Mode | Positive check | A failure leaves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 001-functions:435 | a rename of ${J_CONF}.tmp (write_setting_line, del_setting, sort_settings, set_settings) | temp-and-rename | none | wait_lock /tmp/.system.cfg.lock (the caller's) | the live file's and the record's shared bits (prepare_settings_temp, #421) | the pipeline's status under pipefail; mv's | the old file whole and the shared .tmp (stage-b/positives/shell-writers.out K1, K2) |
| 001-functions:467 | a rename of ${J_CONF}.tmp (write_setting_line, del_setting, sort_settings, set_settings) | temp-and-rename | none | wait_lock /tmp/.system.cfg.lock (the caller's) | the live file's and the record's shared bits (prepare_settings_temp, #421) | the pipeline's status under pipefail; mv's | the old file whole and the shared .tmp (stage-b/positives/shell-writers.out K1, K2) |
| 001-functions:498 | a rename of ${J_CONF}.tmp (write_setting_line, del_setting, sort_settings, set_settings) | temp-and-rename | none | wait_lock /tmp/.system.cfg.lock (the caller's) | the live file's and the record's shared bits (prepare_settings_temp, #421) | the pipeline's status under pipefail; mv's | the old file whole and the shared .tmp (stage-b/positives/shell-writers.out K1, K2) |
| 001-functions:603 | a rename of ${J_CONF}.tmp (write_setting_line, del_setting, sort_settings, set_settings) | temp-and-rename | none | wait_lock /tmp/.system.cfg.lock (the caller's) | the live file's and the record's shared bits (prepare_settings_temp, #421) | the pipeline's status under pipefail; mv's | the old file whole and the shared .tmp (stage-b/positives/shell-writers.out K1, K2) |
| 001-functions:542 | the image's seed copied over a missing system.cfg (set_setting, set_settings) | in place: cp | none | none: before wait_lock | the seed's (0644 shipped) through cp | none | the seed, which the interface's next load records over the player's record (shell-writers.out S1) |
| 001-functions:595 | the image's seed copied over a missing system.cfg (set_setting, set_settings) | in place: cp | none | none: before wait_lock | the seed's (0644 shipped) through cp | none | the seed, which the interface's next load records over the player's record (shell-writers.out S1) |
| chksysconfig:70 | put(): a whole copy through ${dst}.tmp (backup, restore, the reseed of system.cfg) | temp-and-rename | none | none (boot and shutdown, before and after the interface) | prepare_settings_temp's for put() | the copy's and mv's status | the old file whole |
| chksysconfig:324 | the reseed of missing files under /storage/.config | rsync's own temp-and-rename, missing files only | none | none (boot and shutdown, before and after the interface) | rsync -a: the image's | rsync's status | the old file whole |
| post-update:160 | post-update's edit at the update's first boot | in place: busybox sed -i (its own temp and rename) | none | none | sed -i's: the temp's, not always the file's | none | T1's PL-014 (cited) |
| post-update:202 | post-update's edit at the update's first boot | in place: busybox sed -i (its own temp and rename) | none | none | sed -i's: the temp's, not always the file's | none | T1's PL-014 (cited) |

Rows: AtomicFile 41 (9 writes), writeAllText 25 (16 sysfs), shell 10.

**The kill-the-writer test (D-CLOUD-078), on the host:**
- **The interface's writers** (`stage-b/positives/kill-writer.py` → `kill-writer.out`): `state-fixture` runs the pin's `SystemConf.cpp` and `AtomicFileUtil.cpp` against `SystemConfTests.cpp`'s doubles. `killer.so` sends SIGKILL before each of the writer's file-system calls in turn.
  - `writeText`: 9 kill points;
  - `Settings::saveFile`'s two writes, in its order: 18 (the pugixml serialisation is not built: no pugixml on the host);
  - `SystemConf::set` with `saveSystemConf`: 72.

  All 99 leave the live file old or new and whole, and the record old, the old live text, or new. 42 of them leave a temporary behind (L-09).
- **The shell writers** (`shell-writers.py` → `shell-writers.out`): `8ebaf8daad`'s `001-functions` sourced at its own path in bubblewrap, started with `--clearenv`. The donor image's busybox is `/usr/bin`, and no path is rewritten. A kill mid-write, before the rename and after it each leave the old or the new file whole, and the interface's next load takes the live file. The unkilled control writes the new file. S1 is L-10.

## The readers

| Parse | Edge case | Handled at | What happens | proved |
| --- | --- | --- | --- | --- |
| `parseKeyValues` (`system.cfg`) | no `=` | `AtomicFileUtil.cpp:461` | skipped | tree |
| | an empty key | `:465` | skipped | tree |
| | an empty value | `:465` | **dropped; `get` answers the table's default** (L-15) | fixture U1 |
| | a byte-order mark | none | kept in the first key, which then reads as its default; the shell's `grep '^system\.hostname='` misses it too | tree |
| | a duplicate | `:466` | the last wins | tree |
| | a comment | `:461` | `#` or `;` at column 0 only; ` #k=v` is a key with a space | tree |
| | a carriage return | none | kept in the value: `1\r` is not `1`, so `getBool` reads false | tree |
| | a file under three bytes | `readText` reads its own fd (`:195-256`) | read whole: the `readAllText` trap (`es-code-traps.md`) does not reach it | tree |
| | a missing file | `chooseConfig` → `Missing` (`:395`) | `Unable to open`, the table's defaults (`SystemConf.cpp:277-282`) | tree |
| `chooseConfig`'s ladder | live whole; a cut prefix of a whole `.tmp`; a cut prefix of a whole record; a whole record; a whole `.tmp`; damaged; missing | `:291-396` | `AtomicFileTests` 24 cases (22 lines name `chooseConfig`), `SystemConfTests` 10 against real files, all passing at the pin (`stage-a/unit-pin.txt`) | tool-run |
| `Settings::loadFile` (`es_settings.cfg`) | empty, cut or unparsable | `Settings.cpp:564-584` | the record parsed and copied back (`:617`); without one, defaults and nothing written | tree |
| | **no test** | — | no `SettingsTests.cpp`; the ladder is the window's to prove on the image (Q8) | tree |
| The player told | either store recovered | `main.cpp:1041-1042` | `YOUR SETTINGS FILE WAS DAMAGED. THE LAST GOOD COPY WAS RESTORED.`, once. The words also stand for a file that was missing, not damaged. | tree |
| `getLEDColours` (`led.colour`) | a word, a comma list, two numbers | `ApiSystem.cpp:1877-1887` | throws `stoi`; white; `255 0 0` (L-16) | fixture |

## The client

`HttpReq` has no thread of its own. One process-wide `curl_multi` (`HttpReq.cpp:21`) is driven by whichever thread calls `status()`, under one static mutex (`:19`, `:397`). That caller completes every finished request, its own and others' (`:412-523`). `wait()` polls that every 20 ms (`:638-644`), so a caller on the interface thread holds it for the request's whole length.

**Every `curl_easy_setopt`:**

| Line | Option | Value | When |
| --- | --- | --- | --- |
| `:147` | `URL` | the caller's | always |
| `:156` | `BUFFERSIZE` | 100 kB | not on Windows |
| `:167-169` | `POST`, `POSTFIELDSIZE`, `COPYPOSTFIELDS` | `dataToPost` | when set |
| `:179` | `HTTPHEADER` | `customHeaders` (the list is never freed, L-07) | when set |
| `:183` | `FOLLOWLOCATION` | 1 | always |
| `:192` | `SSL_VERIFYPEER` | **0** (#1154) | always |
| `:197-200` | `SSLCERT`, `SSLCERTTYPE`, `SSLKEY`, `SSL_VERIFYHOST` | the client certificate; **`VERIFYHOST` 0** | with a client certificate |
| `:204` | `CONNECTTIMEOUT_MS` | `connectTimeout`, 10,000 | always |
| `:206` | `TIMEOUT_MS` | `timeout` | only when > 0 (default 0: unbounded) |
| `:211`, `:213` | `LOW_SPEED_LIMIT` 1, `LOW_SPEED_TIME` | `stallTimeout` | only when > 0 (default 0) |
| `:222` | `MAXREDIRS` | 2 | always |
| `:236-242` | `REDIR_PROTOCOLS(_STR)` | `http,https` (T20's S2 adds `httpsRedirectsOnly`, at ES `5c0ddaaee`) | always |
| `:253`, `:262` | `WRITEFUNCTION`, `WRITEDATA` | `write_content`; **no size bound** | always |
| `:274` | `USERAGENT` | a Firefox 10 string (`.h:30`) | unless empty |
| `:287-288` | `COOKIEFILE`, `COOKIEJAR` | `<ES dir>/tmp/cookies.txt` (`:96-103`); its mode is the window's | `useCookieManager`, default true |
| `:291-292` | `HEADERFUNCTION`, `HEADERDATA` | `header_callback` (L-02) | always |
| `:315-316` | `PROXY`, `PROXYTYPE` | the registry's | Windows only |

**Not set:** `PROTOCOLS` (only redirects are restricted; `file://` is closed by the status-0 path, above), `NOSIGNAL`, `MAXFILESIZE`, `CAINFO`.

**Every `HttpReqOptions` field** (`HttpReq.h:45-88`):

| Field | Default |
| --- | --- |
| `outputFilename` | "" (in memory) |
| `customHeaders` | none |
| `dataToPost` | "" |
| `userAgent` | `HTTP_REQ_USERAGENT` |
| `clientCert`, `clientKey` | "" |
| `connectTimeout` | 10,000 ms |
| `timeout` | 0 |
| `stallTimeout` | 0 |
| `useCookieManager` | true |
| T20's `httpsRedirectsOnly` (after its merge) | false |

**#1154 is cited, not re-found.** Its fix's design question goes to the stage-D pause, as the brief asks: verify the peer by default with the image's CA bundle, and keep the 2021 exception as an explicit option the scrapers' media downloads set. Whether the image has the bundle, and how the scrapers behave with verification on, are the window's.

## The runs

The brief's § 5 block ran verbatim (`stage-a/runs.sh` → `runs.txt`, `runs.trace`; rc 0; the whole block under one second), every `git grep` at the pin's objects.

| Run | What | Figure | Exit | A FAIL would mean |
| --- | --- | --- | --- | --- |
| R1 | the ES worktree, the merge base, the delta | the pin; 0 changes; `bccd715707`; 14 files, 2,510 insertions, 181 deletions | 0 | a read of other bytes than the pin's |
| R2 | the executors and the exit reads | 20 lines; 15 `WEXITSTATUS` with the shims at 45-46; 11 without `WIFEXITED`; `WIFEXITED` at 528, 585, 607 | 0 | the eleven-site claim wrong |
| R3 | the quoting | `shellQuote` 13, all `wifictl`; `getSevenZipCommand()` at 1527, 1578, 1659; poppler at 2509, 2593; the comment at 631-634 | 0 | a quoting rule misread |
| R4 | the absent scripts | 105 `batocera-` lines, 36 names; `wifictl`, `rocknix-bluetooth`, `rocknix-config`, `cloud_oauth` 1 each; `set-audio`, `keyboardToPads`, `rocknix-sync`, `rocknix-resolution` 0; p7zip's `all3` (`:37`), `bin/7z*` (`:43`) | 0 | a dead path called live, or the reverse |
| R5 | the mask | `maskSecrets` at 2235, 2265, 2297, 2325; the rules at `StringUtil.cpp:715-803`, the word list at `:513`, the `wifictl` rule at `:764-784` | 0 | a log line called masked that is not |
| R6 | the client's options | as § The client | 0 | an option misstated |
| R7 | the scraper's credentials | the runtime pair 39, 40, 43; the account 874-878, 890-894; the rows at `GuiScraperStart.cpp:413-420` and `GuiMenu.cpp:8371`, `:8374`; `Scraper.cpp:524`. The compiled pair at 36-37 is a macro name the pattern does not match (read at its lines). | 0 | a credential's line missed |
| R8 | the Wi-Fi key's path | the popups at 295, 297, 365, 367; `wifictl` without a bound at 642, 767, 771, 775 (642 Windows-only); `wifictl` 557 lines. **Delta:** the pattern prints 177 and 460 of the four key lines; 195 and 209 say `psk`. | 0 | the key's lines misplaced |
| R9 | the writers | 41 `AtomicFile::` lines, 27 `writeAllText(` lines (25 call sites); the shell's renames at 435, 467, 498, 603; the seed at 542, 595; no `fsync`; `post-update`'s `sed -i` at 101 (sysctl), 160, 202 | 0 | a writer missed |
| R10 | `chksysconfig`'s lock | 0 lines | 1 (grep's none) | — (the brief expects none) |
| R11 | the readers | `parseKeyValues` 453; `chooseConfig` 291; `Settings::loadFile` 549; `main.cpp:1041` | 0 | a reader missed |
| R12 | the tests at the pin | 24, 2, 10, 12, 19, 2, 8, 3: **80**; no `SettingsTests.cpp` | 0 | a harness claim wrong |
| R13 | the host tools | `settings-modes-test`, `last-good-scripts-test`, `cloud-input-test` `--help` rc 0; `vm-upgrade-rehearsal` has none (rc 1, usage) | 0 | a tool unavailable |
| R14 | the syntax check | `es-syntax-check` rc 2 ("no build root"), its CANNOT | 2 | — |
| R15 | the host `g++` | `AtomicFileUtil.cpp` PASS; `SystemConf.cpp` CANNOT `SDL_timer.h`; `ApiSystem.cpp` CANNOT `SDL_joystick.h` (and `Settings.cpp` `pugixml.hpp`, `HttpReq.cpp` and `ScreenScraper.cpp` `curl/curl.h`, `GuiWifi.cpp` `SDL_joystick.h`) | 0 / 1 | a file called compiled that was not |
| R16 | the removal check | nothing under `packages`, `projects`, `tools` since `4844a773ca`; the ES diff against the pin empty | 0 | the rule broken |
| R17 | the generated test build (`tools/t21-build-tests.sh`) | 185 + 24 + 10 + 2 = 221 cases, all passing; the eight files 80 inside the binaries; 41 s | 0 | the tests' baseline not what the pin ships |
| R18 | `tests/wifi-profile-lifetime.py` (the errata's) | `PASS profile-choice callback survives page deletion` | 0 | the page's lifetime broken at the pin |
| R19 | `tools/t21-commands.py --expect 143` | 143 rows; the independent count 143; `--expect 142` exits 1 | 0 | a command-running call missed |
| R20 | `tools/t21-writers.py --expect-atomic 41 --expect-writeall 25 --expect-shell 10` | 41, 25 (16 sysfs), 10; `--expect-shell 11` exits 1 | 0 | a writer missed |
| R21 | `stage-b/positives/kill-writer.py` | 99 kill points, 0 broke the invariant, 42 left a temporary | 0 | a writer that loses the record when killed |
| R22 | `stage-b/positives/shell-writers.py` | K0-K3 whole; S1 the record lost | 0 | as above, for the shell |
| R23 | `stage-b/positives/state-fixture` U1-U3 | `BATOCERA`; a second key; the default written | 0 | — (each is a lead's positive) |
| R24 | `stage-b/positives/lifted` (ASan, UBSan) | header: heap-buffer-overflow (rc 1); led: throws; enum and script: failures read as success | 1, 0, 0, 0 | — (each is a lead's positive) |

## Positives

| Positive | Lead | Command | Output | proved |
| --- | --- | --- | --- | --- |
| The interface's writers killed at every step | L-09; the D-CLOUD-078 test | `python3 -I -B stage-b/positives/kill-writer.py <state-fixture> <killer.so> <scratch>` | `kill-writer.out` | fixture |
| The shell writers killed, and the seed before the record | L-10 | `python3 -I -B stage-b/positives/shell-writers.py <001-functions> <seed> <busybox> <os-release> <state-fixture> <scratch>` | `shell-writers.out` | fixture |
| An empty value, a line end, the dead default | L-15, L-11, L-12 | `state-fixture parse/get/set` | `state-units.out` | fixture |
| The header read, the LED parse, two executors' exits | L-02, L-16, L-17, L-18 | `stage-b/positives/lifted header\|led\|enum\|script` | `lifted.out` | fixture |
| `ask()`'s reader (T20's PL-08) | L-18 | T20's `stage-b/positives/reader.cpp` at `ffb6b686cb` | T20's `reader.out` | fixture (T20's) |

**The builds:**
- `g++ -std=c++17 -O0 -g -pthread -I <W>/es-app/tests/unit/fakes -I <W>/es-core/src -I <W>/external state-fixture.cpp <W>/es-core/src/SystemConf.cpp <W>/es-core/src/utils/AtomicFileUtil.cpp`;
- `gcc -shared -fPIC -O0 -o killer.so killer.c -ldl`;
- `g++ -std=c++17 -O0 -g -fsanitize=address,undefined -fno-omit-frame-pointer -I <W>/es-core/src -I <W>/external lifted.cpp <W>/es-core/src/utils/StringUtil.cpp`.

Each ran single-threaded, in seconds.

## What T26 and the OS slices inherit

- **The quoting rule.** A string from outside the program goes to a shell through `Utils::String::shellQuote` (`StringUtil.cpp:426-444`; 13 sites, all `wifictl`), or to an argv executor (`WifiScanProcess`, `posix_spawnp`, `GuiWifi.cpp:540`). Never double quotes. The double-quoted sites are § The commands' 16 rows; the live ones are L-01's.
- **The stores' keys.** `system.cfg` is the launch scripts' store and the only one they read; `es_settings.cfg` is EmulationStation's own. `addSwitch`'s bool is `storeInSettings` (`GuiSettings.cpp:391-395`, 48 rows `true`). A key written with an empty value on purpose (D-NET-009) reads as its table default in the interface (L-15). T26's rows read `system.hostname` at `GuiMenu.cpp:9909` and show `getRootPassword` at `:3209`.
- **The writers' contract.**
  - State goes through `Utils::AtomicFile::writeText`, never `writeAllText` (§ The writers, group 2's eight card files).
  - `system.cfg` is written through `saveUnderLock` under `PidLock` `/tmp/.system.cfg.lock`.
  - The record is published only after the re-read under the lock (#320).
  - A writer's own temporaries are swept (L-09).
  - The shell writers seed under the lock and from the record (L-10, T1's file).
- **The `7zr` question.** The p7zip recipe builds `all3` and installs `bin/7z*`; whether `7zr` is on the image is the window's `ls /usr/bin/7z*`. It decides whether L-01's `7z` rows and the NETPLAY gate (`ApiSystem.cpp:2370`) are live.

## The guest cycle

- **The grant and the posts:** granted on #668 at 22:41 UTC, late (the coordinator's session was down from about 21:05 to 22:39; the host was free). START at 22:43:36 UTC and RETURN at 22:49:29 UTC were each posted on #668 with the census as the first line, and mirrored in the host file.
  - START census: qemu 1 (this guest), compilers 0, :8080 0.
  - RETURN census: qemu 0, compilers 0, :8080 0, :10022 0.
  - The bound was 23:28:36 UTC; the window used six minutes.
- **The swap reclaim, run once before the guest** (`tools/build-preflight --reclaim-swap`, 22:42:21 UTC): rc 0, `READY`, swap from 8,188 to 0 MB used (`guest/reclaim.txt` in the scratch, quoted in START). At the leftover check, with no guest running, swap was back to 2,498 MB used: the host's, not this window's.
- **The image** (`g01-identity.txt`): `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`, `.sha256` OK. It ran on a fresh 16 GB qcow2 of the lane's own, at 640x480 (`fbset` `640 480`).
  - `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`, `BUILD_BRANCH="build/m7-signin-20261022-07"`.
  - **The installed EmulationStation by two literals:** the pin's `wifi picker: stopping scan worker` (1) and M7's composition's `Pending achievements stay` (1). It is M7's composition over the pin, so every frame and verdict below is the image's.
  - **The six OS files against `8ebaf8daad`** (`g01-image-vs-tree.txt`): `001-functions`, `chksysconfig`, `wifictl`, `rocknix-evidence` and `post-update` are byte-identical. The seed `system.cfg` differs (`195c35fd…` installed, `bd6fdc41…` at `8ebaf8daad`); S1's finding is the copy's order, not the seed's contents. The first comparison read every file as different because the serial lines end in CR; it was redone with them stripped, and both runs are kept.
  - `7z`, `7za`, `7zr`, `pdfinfo` and `pdftoppm` are in `/usr/bin`: the `7zr` question is answered, and L-01's `7z` and poppler rows are live code. curl 8.21.0 lists `file`; the CA bundle links are present (`/etc/ssl/certs/ca-certificates.crt`). `/storage` is ext4 `rw,noatime`, so ext4's default `auto_da_alloc` applies to the shell's rename over an existing file. `/bin/sh` is bash.
- **G2, the modes** (`g02-modes.txt`):
  - `system.cfg` and `.backup` 645;
  - `es_settings.cfg` and `.backup` 644;
  - the cookie jar `/storage/.emulationstation/tmp/cookies.txt` 644, 131 bytes, present at boot;
  - no leftover temporaries beside the stores;
  - NetworkManager's keyfile directory `/storage/.config/NetworkManager/system-connections` (`NetworkManager.conf:19`), 755. A keyfile its own writer made with a dummy key was 600; it was removed, and is not the page's join.

  proved: guest.
- **G3, the key on argv** (`g03-argv.txt`): the page's command shape, `sh -c "timeout 150 wifictl connect '<dummy>' '<dummy key>' 'US'"`, the key made on the guest and never printed.
  - The first sample counted **3** processes whose cmdline carried the key.
  - `top -b -n 1 | head -25` carried it on 0 lines.
  - The connect exited **0** with no adapter (`eth0` and `lo` only): L-22.

  proved: guest.
- **G4, the recovery ladder** (`g04a-system-cfg.txt`, `g04b-es-settings.txt`, `frames/g04a-*.png`, `frames/g04b-*.png`):
  - **`system.cfg`** was cut to 2,523 of 5,047 bytes mid-line, with its record's mtime. The interface chose the record and wrote it back; the live file equals the original, and `es_log.txt` carries the warning.
  - **`es_settings.cfg`** was emptied beside its record. The interface loaded the record and copied it back; the live file equals the original. This is the ladder with no unit test.
  - Both times the player read `YOUR SETTINGS FILE WAS DAMAGED. THE LAST GOOD COPY WAS RESTORED.` once, at 640x480.

  proved: guest.
- **G5, L-15** (`g05-hostname.txt`, `frames/g05-network-settings.png`): `set_setting system.hostname default` wrote `system.hostname=`, and NETWORK SETTINGS > HOSTNAME read **BATOCERA**. proved: guest.
- **G4 and G5's originals** were restored and verified by `cmp`, and the aside copies removed (`g45-restore.txt`, `g08-close.txt`).
- **G6 and G7: not run; `CANNOT in this window`.** The reason: just after G5's frame, the session's response was cut off by an automated safety check, and I closed the window rather than run the scraper-and-listener step or the live sign-in without reviewing them again. By the coordinator's 22:51 ruling, G6(a) and G6(b) are queued for a second 20-minute window behind M7's RETURN; G6(c) and G7 stay `CANNOT` for the slice. Until then, L-01, L-03 and #1154's scraper half rest on their stage-B evidence (tree, and `lifted.out` where it applies).
- **The close** (`g08-close.txt`, `retired.txt`): 0 ScreenScraper account keys in `es_settings.cfg`; `vm-stop` rc 0 (pid 4155351 gone). The disk `/workspace/tmp/m6-t21/guest/t21.qcow2`, 2,309,423,104 bytes, sha256 `592c453a0aaf0a7a014412c7403b1d139631835465022f83e2c17766842e0a81`, is retired and absent. The leftover check found qemu, compilers, :8080, :10022 and both sockets at 0.

## Corrections to the brief, by command

| Brief says | The run says | Where |
| --- | --- | --- |
| `wifictl`'s key lines "including 177 195 209 460" | the pattern prints 177 and 460; 195 and 209 are `psk` lines it cannot match | R8 |
| "27 `writeAllText` sites" | 27 lines, 25 call sites (sixteen sysfs), plus the definition and the declaration | R9, R20 |
| `:642` `enable <ssid> <key>`, the key on argv with no bound | `:639-645` is the `#else` of `#if !WIN32`: Windows only | L-08 |


**Trimmed for this packet (D-WORKFLOW-195):** § The commands omits its 93 rows that join no external string; § The writers omits 32 `AtomicFile::` rows that are reads, types or comments and 17 `writeAllText` rows that are sysfs or the Windows build. The full tables are in the audit folder.



## The first reader's 03-retrospective.md (whole)

# Retrospective audit — M6.P2 T21, EmulationStation's state primitives and its bridge to the OS (#668)

Written by the first reader (Opus 5.5) after stages A and B and the first guest window, before any seat saw the packet. Line numbers are the pin's (`16dbac5211`) unless they name a script, which is `8ebaf8daad`'s.

## 3.1 Architectural coherence

- **Two stores, two contracts.** `SystemConf` (`system.cfg`) is the fork's rebuilt writer: `PidLock` around the read-modify-write, `AtomicFile::writeText`, the record published after a re-read under the lock (#320), and pending changes kept across a refused save. `Settings` (`es_settings.cfg`) shares only the primitive (`writeText`) and the ladder's shape: no lock, no mutex, and no test. D-CLOUD-079's sentence describes both as locked (L-13).
- **The primitive is sound and the store around it leaves litter.** `writeText` holds under a kill at every step (99 of 99). Since PL-063 gave each write its own temporary, the old sweeps no longer match, and a kill's temporary stays for good (L-09).
- **One network client with no thread of its own.** Every `HttpReq` is completed by whichever thread next calls `status()` under one static mutex. That is why #299's silence held the interface thread, why one page's wait completes another's request, and why `mStatus` is a data race (L-04). The option set is upstream's, with the fork's `stallTimeout` added; the peer is never verified (#1154).
- **The shell bridge has three quoting rules.** `shellQuote` where the fork wrote the call (13 `wifictl` sites); double quotes where upstream did (16 rows, the live ones `7z` and poppler over a player's file name, L-01); bare where a script's own output is joined (safe by shape). The argv executor (`WifiScanProcess`) exists and is used once.

## 3.2 Project conformance

- **`engineering-practices.md` § Guards must fail closed:** `executeEnumerationScript` discards the exit (L-17), eleven exit reads take a signal for exit 0 (L-18), and `wifictl` exits 0 with no device, which the page reads as CONNECTED (L-22).
- **§ The last known good state is a record:** the shell's seed is copied before the record is consulted, and the interface then records it (L-10). A download removes the file it replaces before the bytes arrive (L-03).
- **`upgrade-and-install.md`:** a device that upgraded keeps its `system.cfg`'s mode, and the seed ships 0645, so nothing narrows it (L-21).
- **`es-code-traps.md` § A pooled connection:** the scraper's probes have no stall bound (`ScreenScraper.cpp:1030-1032`, `:1067-1068`); the hash library's fetch is T20's.
- **`es-player-text.md`:** the one sentence a recovery shows (`main.cpp:1041-1042`) is plain and said once; it says "damaged" for a file that was missing too.

## 3.3 Spec fidelity

The brief's figures held at their hashes (`01` § Scope, `02` § The runs). Three of its comments were corrected by its own commands (`02` § Corrections to the brief), and the coordinator's ruling of 22:35 took both stage-A deltas.

## 3.4 Platform conformance

- **The image is M7's composition over the pin.** Five of the six OS files are `8ebaf8daad`'s bytes; the seed `system.cfg` differs in content and is 0645 against git's 0644.
- **`/storage` is ext4 `rw,noatime`,** so the shell writers' rename without `fsync` is covered by `auto_da_alloc` when it replaces an existing file. It is not covered for the seed's `cp` over a missing file.
- **`7zr`, `pdfinfo` and `pdftoppm` ship,** so L-01's rows are live code. curl lists `file` among its protocols; the status-0 path closes it.

## 3.5 Cross-system interaction audit

### Interaction: the shell's writers (T1) x the interface's recorder

`set_setting` seeds a missing `system.cfg` before its lock and without the record. The interface's next load takes any usable, whole live file as the record (`AtomicFileUtil.cpp:352-361`, `SystemConf.cpp:232-238`), so the seed replaces the player's record. Either side alone is reasonable; together the record is lost (`shell-writers.out` S1). How the live file comes to be absent while a `set_setting` runs after boot's `chksysconfig verify` is T22's boot order, not read here.

### Interaction: D-NET-009's empty line x the interface's parse

The shell writes `system.hostname=` on purpose so `chksysconfig`'s sentinel survives. The interface's parse drops an empty value, and `get` answers the table's `BATOCERA` (`state-units.out` U1; on the image, `frames/g05-network-settings.png`).

### Interaction: `wifictl` x the Wi-Fi page

`wifictl` exits 0 with no device; `enableWifi` reads `system() == 0`; the page saves the network and the key and says CONNECTED (L-22). The key is argv of three processes while `wifictl` lives, and of `nmcli` for up to 90 s on a device (L-08).

### Interaction: the scraper x `HttpReq` x the unverified peer

Every scraper request carries the developer pair and the player's account on its query, to a peer `HttpReq` never verifies (#1154). The server's answer then decides the media URLs and the saved files' extensions. `file://` and the extension-as-path were read and closed (`02` § The leads, closed); the download that removes its target first is not closed (L-03).

### Interaction: the settings archive (T17) x a kill's leftovers

The archive takes the stores by exact name (`backuptool:283-292`), so a writer's leftover temporary stays on the card and never reaches a cloud (L-09).



## The first reader's 04-analysis.md (whole)

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
- **The Wi-Fi key:*** on argv of three processes on the guest (L-08); in a 0645 file at rest (L-21); typed in the clear in a popup that has no masking mode.
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



## Context 1: the brief's § 4

```text
## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of four families: **a command built from
a player's string** (a path, a name, a key), **a credential's sink** (argv,
a file's mode, a log, an unverified peer), **a state write that can lose
the record** (no lock, no `fsync`, in place, the seed before the record),
**a check whose failure reads as success** (a discarded exit, a signal read
as 0, a dropped line). The leads below are the digests' by shape; each is
read at its lines before it is called anything.

- **Q1 The commands.** Every command-running call with its quoting: the
  two live double-quoted paths (`7z`, poppler) against a file name carrying
  a shell metacharacter -- the constructed positive is a ROM named with a
  `$(...)` in a scratch library on the guest, never on a device; the bare
  strings from script output and the bezel list; the leaked children; the
  absent scripts' sites (a table: which gate hides each, which page could
  still reach one; recorded, since D-UI-079 keeps upstream's surfaces as
  upstream has them until a lane opens them); the blocking calls on the
  interface thread and their bounds (none for the timezone, audio,
  storage, service, hotkey and LED setters; `getBiosInformations` at launch when CHECK BIOS AT LAUNCH is on, default off -- the time-to-play line).
- **Q2 The client.** The one `curl_multi` driven by whichever thread
  calls `status()`: which callers hold the interface thread and for how
  long with `timeout` 0; the server's body logged verbatim for 400 to 503
  (peer-controlled text into `es_log.txt`); the cookie jar's file and mode;
  the redirect policy against a credential on the first query; #1154 cited
  -- and the fix's design question for the stage-D pause: verify the peer
  by default with the image's CA bundle and keep the 2021 exception as an
  explicit option the scrapers' media downloads set (the bundle's presence
  on the image and the scrapers' behaviour with verification on are the
  window's to read).
- **Q3 The credentials' paths.** The Wi-Fi key on argv of four processes for up to 150 s (and of `enable` at `:642` with no bound) and in a popup whose class has no masking mode at all (`GuiTextEditPopup` `.h:15-16`, `GuiTextEditPopupKeyboard` `.h:13-14`: a fix adds a mode, not a flag); `wifi.key` at rest
  in `system.cfg` at the file's mode; the NetworkManager keyfile's mode
  (read on the guest); `es_settings.cfg` at 0644 with the scraper's
  account and the RetroAchievements key; the developer pair compiled in
  (D-WORKFLOW-166's allowed case: which identity, and that no personal
  value is embedded -- read by name, never printed) against the runtime
  rows; the filter's two blind words; the LogDebug lines with the username
  and `devid`; `getRootPassword`'s literal default and where it is shown.
- **Q4 The writers.** The lock asymmetry (`SystemConf` locked, `Settings`
  not, the maps unguarded under a worker's save); the shell writers with no
  `fsync`; `chksysconfig` with no lock; `post-update`'s `sed -i`; **the
  seed before the record** (`set_setting:540-543`); the modes (0644 from
  EmulationStation, 0600 from the shell, the seed 0644, a replaced file's
  bits kept: what an upgraded device holds -- `upgrade-and-install.md`'s
  question, with `Already written:` the answer); the `.backup.tmp` sweep
  against `chksysconfig backup`'s temp name; the in-place `writeAllText`
  state writers outside `AtomicFile`.
- **Q5 The readers.** `parseKeyValues`' silent drops (no `=`, an empty
  key, **an empty value**, a BOM kept, the last duplicate winning) against
  what the shell writers can produce; the recovery ladder's cases and
  their tests (`SystemConfTests` 10 against real files; `AtomicFileTests`
  24); `Settings::loadFile`'s ladder with **no test at all**; the player
  told once at `main.cpp:1041-1042` (the words, `es-player-text.md`).
- **Q6 What a failure reads as.** The enumeration executor's discarded exit and `getBiosInformations` at launch with CHECK BIOS AT LAUNCH on; the `#if WIN32` shims at `:45-46` that make the Windows build read every status as an exit code (not built here; recorded); the eleven
  `WEXITSTATUS` reads without `WIFEXITED` and which pages act on them
  (T20's `ask()` among them); the last line as the result where a script
  prints two; `cloud_oauth close`'s ignored result (`:593`); the
  `LockBusy` path that keeps a change in memory and what the player sees.
- **Q7 The dead paths.** The 105 `batocera-` lines (36 names), `set-audio`, `keyboardToPads`, `rocknix-sync`, `rocknix-resolution`, `pm-*`, and the `7zr` question (the recipe's `all3` and `bin/7z*`; the image's listing in the window): a table of each site, its gate, whether a page on this
  image can reach it, and what it would do if reached -- recorded as
  written (D-WORKFLOW-209's shape: a table removes nothing; the removal is
  the renovation's later pass, #1143's family).
- **Q8 The harness.** What `tools/settings-modes-test` (#421),
  `tools/last-good-scripts-test`'s sections a and c, `AtomicFileTests`'
  24 cases, `tools/vm-upgrade-rehearsal` (no `--help`; seeds no `.backup`),
  `tools/cloud-input-test` (#535/#536) and `MaskSecretsTests` prove and do
  not; the kill-the-writer test D-CLOUD-078 names (every step, for both
  stores, on the host through the unit tests' fakes where the writer is
  pure and on the guest where it is not); for each lead this slice
  confirms, the constructed positive that fails on the pin's bytes.

```


## Context 2: the register rows

```text
| D-CLOUD-078 | 2026-09-10 | **Always keep a record of the last known good state. A failure reverts to it; a success becomes it, and the previous record is then removed (refines D-CLOUD-077).** Maintainer: *"we should always keep a record of the last known good state, which hopefully is a fairly straightforward but powerful rule. That way, if something fails, it should always revert to the last known good state. This also means we should always know when something is successful, and therefore the successful state becomes the last known good state, and we can remove the previous one."* Three obligations follow for every writer: (1) it must *know* when it succeeded -- a positive check of the artifact, never the absence of an error (engineering-practices § guards fail closed); (2) the new state replaces the old only after that check -- temp-and-rename, a marker written after the bytes are confirmed, a copy kept until the replacement is verified; (3) the superseded record is removed once, after the new one is good, so there is exactly one last-known-good at rest. Where it already holds: rclone's per-file rename, the settings-upload marker, `backuptool`'s rotation, the capture stage (content-addressed copies of every save the manifest claims), the device id's `.previous`, the `last-*` stamps. Where it does not yet: `system.cfg` and `es_settings.cfg` are rewritten in place and `chksysconfig` overwrites its `.backup` every boot with whatever is there -- so the RG SP's truncated file replaced its own good copy and defaults won (#102); a saves restore that overwrites a newer local copy keeps no previous version (`--backup-dir` would). Work: #105 (messages and retries), #104 (config files kept last-good and restored from it at boot instead of defaults), #22 (the reconciler's kept losers are this rule for saves). | #105, #104, #22, #102 |

| D-CLOUD-079 | 2026-09-10 | **The config files' last-known-good record keeps its existing name and changes its meaning: `system.cfg.backup` (and, new, `es_settings.cfg.backup`) is written only from a file that has just been validated -- at boot after the check passes and at shutdown -- via temp-and-rename; a boot that finds the live file empty, truncated, or unparsable restores it from that record and logs the recovery, and reseeds defaults only when the record is missing or invalid too; the blanket `rsync -a /usr/config/ /storage/.config` is scoped to the files actually missing (implements D-CLOUD-078 for #102's loss).** Keeping the name means one record at rest and no migration; the scripts audit recommended it over a new `.last-good`. EmulationStation's own writers rename their temp into place (`SystemConf` already writes a `.tmp` and then copies it; `Settings` writes in place) and take the settings lock around the read-modify-write. Migration copies the helper keeps forever (`cloud_sync.conf.bak`, `cloud_sync-rules.txt.bak`, `.pre-copy-default`) are removed after the next successful run, per D-CLOUD-078(3). | #105, #104, #102; docs/audits/2026_09_10-graceful-degradation |

| D-QA-021 | 2026-09-12 | **Every read of a device's or a QA guest's config goes through a secrets filter wider than the word *password*: `grep -v -i -E 'key\|pass\|token\|user\|psk'`.** A read needs no permission (D-QA-015) but lands in a transcript, and `system.cfg`, `rclone.conf`, `get_setting` output and anything piped back over SSH can carry a sign-in; rclone writes `pass =`, `user =`, `token =`, `key =`, and the network writes `psk`. The QA guests are in scope: their credentials are throwaway, their files are the same shape, and the transcript is the same transcript. A filter written as `password` let a `pass =` line through on a guest on 2026-09-12. Practice text moved into `engineering-practices.md` by the #147 sweep; long form in `docs/device-testing-policy.md` § Reading a device's output. (source: work log 2026-09-12 05:57 UTC, `6075c64f2e`; no maintainer quote on record) | #147, `6075c64f2e` |

| D-NET-002 | 2026-09-13 | **The shipped device name is the build family, and at boot it becomes this unit's own once -- `<FAMILY>-<four hex digits of the unit's id>` -- written back to `system.hostname`; a name equal to the family, or empty, is the shipped default and never something a player typed, and every other name is the player's and is never touched (extends D-NET-001).** Two units of one family on one network claimed the same DHCP name and the router's lease flipped between them; the failure read as EHOSTUNREACH and sent the maintainer to Wi-Fi and SSH rather than to a name collision (#50). The suffix comes from `cloud_device_id`, seeded from the permanent hardware address, so a reflash gives the same name; the setting is written once so it is stable and is what NETWORK SETTINGS shows. The upgrade path is the same rule: a device upgraded with its family name still set gets its own name at the first boot of the new image, and a device the player renamed keeps its name. Proven on three GENERIC_X64 guests (491f, 15ca, 0964) and by `last-good-scripts-test` case m. | #50, `d857ba04c9` |

| D-NET-009 | 2026-09-13 | **#154, option 1: `set_setting system.hostname default` (and the delete path) writes an empty `system.hostname=` line for this one key instead of removing it, so `chksysconfig`'s sentinel survives and `network-base-setup` re-derives the unit's own name on the next boot (empty is already the shipped-default branch, D-NET-002). The sentinel itself is not loosened (#102's failure shape stays guarded).** Maintainer: "With 154. It seems like option one is the more elegant path forward." The orchestrator's recommendation was the same. | #154; D-NET-002; D-NET-004; `chksysconfig`; #102 |

| D-UI-079 | 2026-09-22 | **D-UI-078's foreground-page rule applies to the lanes the fork works in -- cloud sync and cloud behaviours, game saves, Wi-Fi, the offline achievements work -- and not to upstream surfaces outside them: the game index (`ThreadedHasher`), the content installer, the OS update and the Bluetooth scan keep their background cards for now.** Maintainer, 2026-09-22, closing #241's last box: *"We don't need to alter behaviors outside of the core work we've been tackling when it comes to the game index content installer, OS update, and Bluetooth scan. Let's not alter that work quite yet. I'm more comfortable modifying work within the different lanes we've been working in around cloud sync, cloud behaviors, game saves, Wi-Fi, etc."* The scraper was named in D-UI-078 itself and is done. | #241, D-UI-078 |

| D-SYS-011 | 2026-09-28 | **A cut `system.cfg` is never completed by a shell writer or recorded as whole.** `settings_base` gives every shell writer its starting lines: a file not ending in a newline has its half line dropped and the missing keys come from a whole `.backup`; `chksysconfig backup` never records a mid-line cut. A cut exactly at a line's end is byte for byte what `forget` leaves when it removes the `wifi.*` keys, so it is left alone on purpose, with a harness case guarding against a prefix rule that would bring a forgotten key back (stream B `69b714466b`, the shell half of E1's G2-E-core-03; the interface half is ES `932b57402`). `post-update`'s `sed '$ a'` append is a lead for the next round. | #313 (E1's lead); D-CLOUD-078 |

| D-SYS-012 | 2026-09-28 | **Several settings are written as one: `set_settings` writes its keys in one rename under one lock.** `wifictl join` writes the Wi-Fi pair at once; `forget` clears the pair at once and puts it back at once if the delete fails, logging a put-back that fails (lead G2-B-11 gpt; stream B `0874b75eab`). | #313 (B's lead) |

| D-WORKFLOW-166 | 2026-10-14 | **Use the existing shared JELOS ScreenScraper developer identity as the interim choice for #566; evaluate replacement credentials separately in #586.** This refines D-QA-005/006's runtime-only policy: the intended release route provisions the selected shared developer identity so ordinary players need only their separate personal account. Dedicated credentials are not a prerequisite for the current candidate. Implementation and actual artifact/UI/backup/clean/upgrade checks remain due; this choice neither claims new provider authorization nor permits personal accounts, RA tokens or other unrelated private credentials in public images. D-INFRA-006/007 protections remain for those values; any exception must be limited to the named shared developer identity and verified by an executable check. | maintainer, 2026-10-14; #566; #586; `.claude/rules/device-builds.md` |

| D-WORKFLOW-195 | 2026-10-24 | **An Extended seat whose answer the model's output ceiling cuts on the packet is run again on a trimmed packet for that seat -- the same model, effort and provider; the analyses and tables whole, the cited files as line-numbered excerpts with context, the ask bounded -- never a model or effort substitution and never the same packet again.** `04` § Second opinion says the seats saw different evidence; an item one seat saw only in excerpt carries `excerpt`, and a disagreement that could be the excerpt's doing is resolved from the artifact, not from either seat. A fork resolved during execution on T30 (#677): Argon at `high` spent about 57k of its 65.5k output tokens reasoning on a 438 KB packet three times (`finish=length`), where T3's 308 KB packet took 30k. The maintainer may reverse it by a new row. | #677, #798; `adversarial-council.md` § Council model floor; the T30 hold post of 10:04 UTC and the coordinator's answer the same hour |
```


## Evidence: stage-b/positives/kill-writer.out

```text
== A AtomicFile::writeText: unkilled rc 0, 9 calls; live after = new
  kill before call  1: killed; live/record old/record; next load source=Live record=1; left behind 0; ok
  kill before call  2: killed; live/record old/record; next load source=Live record=1; left behind 1 system.cfg.tmp.3558484.0; ok
  A: 9 kill points, 0 broke the invariant
== B Settings::saveFile's two writes: unkilled rc 0, 18 calls; live after = new
  kill before call 11: killed; live/record new/record; next load source=Live record=1; left behind 1 system.cfg.backup.tmp.3558521.1; ok
  B: 18 kill points, 0 broke the invariant
== C SystemConf::set + saveSystemConf: unkilled rc 0, 72 calls; live after = new
  kill before call  7: killed; live/record old/record; next load source=Live record=1; left behind 1 .system.cfg.lock.new.3558551.0; ok
  C: 72 kill points, 0 broke the invariant
== result: PASS (every kill left the old or the new state whole)
(trimmed for this packet: 95 kill-point lines like the ones shown; the whole file is in the audit folder)
```


## Evidence: stage-b/positives/shell-writers.out

```text
K1 awk shadowed: bash rc 137; system.cfg old; record unchanged; next interface load source=Live record=1; left behind ['system.cfg.tmp']; ok
K2 mv shadowed: bash rc 137; system.cfg old; record unchanged; next interface load source=Live record=1; left behind ['system.cfg.tmp']; ok
K3 mv shadowed: bash rc 137; system.cfg new; record unchanged; next interface load source=Live record=1; left behind nothing; ok
K0 control (no kill): set_setting rc=0; system.cfg new; next interface load source=Live record=1
S1 system.cfg absent, record holds the player's keys: set_setting rc=0
   system.cfg after set_setting: 222 lines, marker absent, qa.setting=newer; mode 0o600
   system.cfg.backup after set_setting: 4 lines, marker present, qa.setting=record
   the interface's next load chooses: source=Live record=1
   a SystemConf load of that file (the pin's code): value=[] rc 0
   system.cfg.backup after the interface's load: 222 lines, marker absent, qa.setting=newer
== result: PASS (K0-K3) ; S1 as observed above
```


## Evidence: stage-b/positives/state-units.out

```text
== the pin's SystemConf and AtomicFile through state-fixture (21:08:57Z)
-- U1: an empty value (D-NET-009 writes system.hostname= on purpose)
keys=1 has[system.hostname]=0
value=[BATOCERA]
-- U2: a value carrying a line end, set and saved by SystemConf
set rc 0
the file's lines, values masked:
system.hostname=<value>
qa.k=<value>
wifi.ssid=<value>
root.password=***
keys=4 has[root.password]=1
-- U3: a key set to its table default (SystemConf.cpp:46, global.retroachievements.hardcore 0)
set rc 0
lines reading global.retroachievements.hardcore=0: 1
```


## Evidence: stage-b/positives/lifted.out

```text
== lifted.cpp at the pin's lines, ASan and UBSan (21:08:39Z)
-- lifted header
rc 1
==3574341==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x... at pc 0x... bp 0x... sp 0x...
READ of size 15 at 0x... thread T0
    #0 0x... in strlen ../../../../src/libsanitizer/sanitizer_common/sanitizer_common_interceptors.inc:425
    #2 0x... in std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::basic_string<std::allocator<char> >(char const*, std::allocator<char> con
    #3 0x... in HttpReqLift::header_callback(char*, unsigned long, unsigned long, void*) /workspace/repos/pixelelated/distribution.worktrees/m6-es-state-and-bridge-668/do
    #4 0x... in main /workspace/repos/pixelelated/distribution.worktrees/m6-es-state-and-bridge-668/docs/audits/2026_10_26-epic-m6-es-state-and-bridge/stage-b/positives/l
    #1 0x... in main /workspace/repos/pixelelated/distribution.worktrees/m6-es-state-and-bridge-668/docs/audits/2026_10_26-epic-m6-es-state-and-bridge/stage-b/positives/l
    #3 0x... in __libc_start_main (/usr/lib/x86_64-linux-gnu/libc.so.6+0x...) (BuildId: 066527e430a32768d82741e00b81eebb1a872294)
SUMMARY: AddressSanitizer: heap-buffer-overflow /workspace/repos/pixelelated/distribution.worktrees/m6-es-state-and-bridge-668/docs/audits/2026_10_26-epic-m6-es-state-and
-- lifted led
rc 0
led.colour=[255 0 165] -> 255 0 165
led.colour=[255 0] -> 255 0 0
led.colour=[red] -> THROWS stoi (the pin's code has no catch)
led.colour=[255,0,165] -> 255 255 255
-- lifted enum
rc 0
[printf 'a\nb\n'] -> ["a","b"]
[printf 'a\nb\n'; exit 3] -> ["a","b"]
[printf 'a\nb\n'; kill -9 $$] -> ["a","b"]
-- lifted script
rc 0
[echo joined; exit 0] -> exit 0, lines ["joined"]
[echo joined; exit 1] -> exit 1, lines ["joined"]
[echo joined; kill -9 $$] -> exit 0, lines ["joined"]
[echo joined; kill -TERM $$] -> exit 0, lines ["joined"]
```


## Evidence: guest-cycle/g01-identity.txt

```text
== G1 identity (22:44:24Z)
 18:44:24 up 0 min,  load average: 0.52, 0.12, 0.04
/dev/vda2                11.9G    173.7M     11.8G   1% /storage
OS_NAME="pixelelated"
VERSION="0.0.1-dev+20261022T235948Z.g069fc2704421"
BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"
BUILD_BRANCH="build/m7-signin-20261022-07"
	geometry 640 480 640 480 32
-- the installed EmulationStation, by two literals
pin literal (wifi picker: stopping scan worker): 1
M7 composition literal (Pending achievements stay): 1
25155163fd7970f7
-- the six OS files, hashed (compared with 8ebaf8daad on the host)
2a67891c9a3090ddae78d4b729ce7b8f5c41d853e0975b4ce0203df7789e4ab5 /etc/profile.d/001-functions
e18d619783d9bbcdd23f1f8aaf2da0786ec162195cc35e1dc3a3ffc4afa04c8e /usr/bin/chksysconfig
c89ed28a50e4be78468fcee25dcfd68e0b1c67af25657c3d0ba9318c7576a48c /usr/bin/wifictl
a9ae19e92cd11d859e6a81b3b82e7fb34a01bce6e525ac962cda76899c30c346 /usr/bin/rocknix-evidence
1e53fe8ca04f84265eaf43fe40c5cc1f2ec45c2bc1fdd13ea835ffb39d2ecdae /usr/share/post-update
195c35fd4437f1125d8066964ec7d75dae3fb37032cbe8710757fdfabc7d3a02 /usr/config/system/configs/system.cfg
-- the 7zr question and poppler
-rwxr-xr-x    1 root     root        471352 Oct  4 00:35 [1;32m/usr/bin/7z[m
-rwxr-xr-x    1 root     root       2258152 Oct  4 00:35 [1;32m/usr/bin/7z.so[m
-rwxr-xr-x    1 root     root        367664 Oct  4 00:35 [1;32m/usr/bin/7zCon.sfx[m
-rwxr-xr-x    1 root     root       1151352 Oct  4 00:35 [1;32m/usr/bin/7za[m
-rwxr-xr-x    1 root     root        770336 Oct  4 00:35 [1;32m/usr/bin/7zr[m
-rwxr-xr-x    1 root     root         64384 Oct  4 00:48 [1;32m/usr/bin/pdfinfo[m
-rwxr-xr-x    1 root     root         31112 Oct  4 00:48 [1;32m/usr/bin/pdftoppm[m
-- the CA bundle and curl
lrwxrwxrwx    1 root     root            23 Oct  4 00:35 /etc/pki/tls/certs/ca-bundle.crt -> /run/rocknix/cacert.pem
lrwxrwxrwx    1 root     root            19 Oct  4 00:35 /etc/ssl/certs/ca-certificates.crt -> /etc/ssl/cacert.pem
curl 8.21.0 (Linux) libcurl/8.21.0 OpenSSL/3.6.3 zlib/1.3.2 libidn2/2.3.8 nghttp2/1.70.0
Protocols: file ftp ftps http https ipfs ipns rtsp ws wss
-- /storage's filesystem and options
/dev/vda2 /storage ext4 rw,noatime 0 0
-- /bin/sh
lrwxrwxrwx    1 root     root             4 Oct 22 20:02 [1;36m/bin/sh[m -> [1;32mbash[m
```


## Evidence: guest-cycle/g01-image-vs-tree.txt

```text
== G1 image versus tree: installed sha256 against 8ebaf8daad (22:44:46Z); the serial lines end in CR, stripped before comparing
same  /etc/profile.d/001-functions  installed 2a67891c9a3090dd  8ebaf8daad 2a67891c9a3090dd
same  /usr/bin/chksysconfig  installed e18d619783d9bbcd  8ebaf8daad e18d619783d9bbcd
same  /usr/bin/wifictl  installed c89ed28a50e4be78  8ebaf8daad c89ed28a50e4be78
same  /usr/bin/rocknix-evidence  installed a9ae19e92cd11d85  8ebaf8daad a9ae19e92cd11d85
same  /usr/share/post-update  installed 1e53fe8ca04f8426  8ebaf8daad 1e53fe8ca04f8426
DIFFERS  /usr/config/system/configs/system.cfg  installed 195c35fd4437f112  8ebaf8daad bd6fdc41140b3c18
```


## Evidence: guest-cycle/g02-modes.txt

```text
== G2 modes (22:45:03Z)
645 root:root 5047 bytes /storage/.config/system/configs/system.cfg
645 root:root 5047 bytes /storage/.config/system/configs/system.cfg.backup
644 root:root 41 bytes /storage/.emulationstation/es_settings.cfg
644 root:root 41 bytes /storage/.emulationstation/es_settings.cfg.backup
644 root:root 131 bytes /storage/.emulationstation/tmp/cookies.txt
drwxr-xr-x    2 root     root          4096 Oct 26 18:44 [1;34m/storage/.config/system/configs[m
lrwxrwxrwx    1 root     root            33 Oct 26 18:44 [1;36m/storage/.emulationstation[m -> [1;34m/storage/.config/emulationstation[m
-- leftover temporaries beside the stores now
0
-- NetworkManager: the keyfile directory, and a keyfile its own writer makes (a dummy key, not the page's join)
5:plugins=keyfile
18:[keyfile]
19:path=/storage/.config/NetworkManager/system-connections
drwxr-xr-x    2 root     root          4096 Oct 26 18:43 [1;34m/storage/.config/NetworkManager/system-connections[m
nmcli add rc 0
600 root:root /storage/.config/NetworkManager/system-connections/T21-dummy.nmconnection
keyfiles carrying a psk line: 1
nmcli delete rc 0
T21-dummy keyfiles left: 0
```


## Evidence: guest-cycle/g03-argv.txt

```text
== G3 the key on argv (22:45:32Z)
seed 645 /usr/config/system/configs/system.cfg
network interfaces: eth0 lo 
the connect's exit: 0
samples 1; the most processes whose cmdline carried the key at once: 3
rocknix-evidence's top line (top -b -n 1 | head -25), lines carrying the key:*** 0
-- what system.cfg says after a connect with no adapter (key names only)
wifi.ssid=T21-dummy-net lines: 0
```


## Evidence: guest-cycle/g04a-system-cfg.txt

```text
== G4a system.cfg cut beside a whole record (22:46:19Z)
essway stopped: inactive
live now 2523 of 5047 bytes, last byte a line end: no
essway: active
live == the record (written back)
live == the original live file
645 5047 bytes /storage/.config/system/configs/system.cfg
645 5047 bytes /storage/.config/system/configs/system.cfg.backup
es_log lines naming the last-known-good record: 1
2026-10-26 22:46:19	[2758]	WARNING	/storage/.config/system/configs/system.cfg is missing, empty, unreadable, damaged or cut short of the record -- loading the last-known-good record /storage/.config/s
```


## Evidence: guest-cycle/g04b-es-settings.txt

```text
== G4b es_settings.cfg emptied beside a whole record (22:46:53Z)
essway stopped: inactive
live now 0 bytes
essway: active
live == the record (written back)
live == the original live file
644 41 bytes /storage/.config/emulationstation/es_settings.cfg
644 41 bytes /storage/.config/emulationstation/es_settings.cfg.backup
```


## Evidence: guest-cycle/g05-hostname.txt

```text
== G5 system.hostname= (22:47:38Z)
hostname lines before: 1
set_setting rc 0
lines reading exactly system.hostname= : 1
essway: active

== G5 the frame (22:48:55Z)
NETWORK SETTINGS > HOSTNAME reads BATOCERA (frames/g05-network-settings.png, 640x480, the image's ES: M7's composition over the pin) while system.cfg holds the line system.hostname= written by set_setting system.hostname default (D-NET-009). L-15 on the screen.
```


## es-core/src/utils/AtomicFileUtil.h @ 16dbac5211 (whole, 215 lines)

```text
    1  #pragma once
    2  #ifndef ES_CORE_UTILS_ATOMIC_FILE_UTIL_H
    3  #define ES_CORE_UTILS_ATOMIC_FILE_UTIL_H
    4  
    5  #include <functional>
    6  #include <map>
    7  #include <string>
    8  
    9  // Whole-file writes that leave either the old file or the new one on disk,
   10  // never a torn one, and the pid lock the shell's settings functions take.
   11  //
   12  // The two configuration files EmulationStation owns -- system.cfg and
   13  // es_settings.cfg -- used to be rewritten in place: truncate, then write.
   14  // A process killed between the two, or a battery that dies there, leaves an
   15  // empty or half-written file, and the boot-time check then replaced the good
   16  // copy with it (fork #102, D-CLOUD-078). Written to a temporary name, synced,
   17  // and renamed into place, the file on disk is always a complete one; the
   18  // directory is synced afterwards so the rename itself survives a power cut.
   19  //
   20  // Every guarantee in this file is POSIX's, and holds on Linux, which is all
   21  // ROCKNIX builds (#307 PL-075). The _WIN32 branches keep upstream's Windows
   22  // build compiling and nothing more: writeText there removes `path` before it
   23  // renames the temporary into place, so a crash between the two leaves no file
   24  // at all; its temporary is the shared `path`.tmp; the lock is never taken
   25  // (acquire answers true); and the mode is not kept.
   26  namespace Utils
   27  {
   28  	namespace AtomicFile
   29  	{
   30  		// Write `text` to `path` through a temporary of this call's own beside
   31  		// it (`path`.tmp.<pid>.<n>, never the shared `path`.tmp the shell's
   32  		// set_setting writes): write, fsync, rename over `path`, fsync the
   33  		// directory. True only once the rename has landed; on any failure the
   34  		// temporary is removed and `path` is untouched. Two calls at once, from
   35  		// two threads or two processes, each leave one whole file (PL-063).
   36  		// With mode -1, a file being replaced keeps its mode, and its owner
   37  		// where this process may set it (#308 F-ES-08), and a new one is made
   38  		// 0644 before umask, as the shell makes files. A mode given is the
   39  		// file's mode whether it is new or replaced: a record written beside
   40  		// a private file passes that file's (modeOf), so the copy is never
   41  		// less private than what it copies.
   42  		bool writeText(const std::string& path, const std::string& text, int mode = -1);
   43  
   44  		// The permission bits of the regular file at `path`, or `fallback`
   45  		// when there is none: what a record written beside a file should be
   46  		// made with, so the copy is no less private than the original.
   47  		int modeOf(const std::string& path, int fallback);
   48  
   49  		// Read `path` whole. `ok` (when given) says whether it was: opened,
   50  		// read to the end without an error, and -- for a regular file -- no
   51  		// shorter than its size at the open (PL-065). An empty file and a
   52  		// missing one both read ""; only the first is ok. On failure "".
   53  		std::string readText(const std::string& path, bool* ok = nullptr);
   54  
   55  		// readText(src) then writeText(dst): dst is replaced whole or not at
   56  		// all, with src's mode. False when src could not be read or dst could
   57  		// not be written.
   58  		bool copy(const std::string& src, const std::string& dst);
   59  
   60  		// Whether a key=*** configuration text is one worth reading and
   61  		// worth keeping as the last-known-good record: something in it, no
   62  		// NUL bytes (a file cut by a power failure reads as a run of them),
   63  		// and at least one key=*** line that is not a comment.
   64  		bool isUsableKeyValues(const std::string& text);
   65  
   66  		// Where a configuration's text comes from at load (SystemConf's
   67  		// system.cfg), and whether it is whole enough to become the record.
   68  		struct LoadedConfig
   69  		{
   70  			enum class Source
   71  			{
   72  				Live,        // the file itself
   73  				Temporary,   // `path`.tmp: an unfinished save's whole text, the file cut or unusable
   74  				Backup,      // `path`.backup: the last-known-good record, whole (a cut one is never taken, PL-018)
   75  				Damaged,     // the file, unusable, with nothing better: read as it is, recorded nowhere
   76  				Missing      // nothing could be read at all
   77  			};
   78  			Source source = Source::Missing;
   79  			std::string text;
   80  			bool record = false;   // may replace the last-known-good record
   81  			// The mode to write the chosen text back with, and the record:
   82  			// never less private than any copy of it on disk (G-E1-05).
   83  			int mode = 0644;
   84  		};
   85  
   86  		// The choice, from what is on disk now. Reads; writes nothing.
   87  		LoadedConfig chooseConfig(const std::string& path);
   88  
   89  		// What the load's write-back of a recovery came to.
   90  		enum class RecoveryWrite
   91  		{
   92  			None,          // nothing to write back: the live file was taken, or nothing could be read
   93  			Written,       // written back as the live file, with the settings lock held
   94  			WriteFailed,   // the lock was held and the write did not land: the file is as it was
   95  			LockBusy       // the lock stayed with a live holder past the budget: nothing written
   96  		};
   97  
   98  		// SystemConf's load: chooseConfig, and where it names a recovery --
   99  		// the whole temporary or the whole record, to be written back as the
  100  		// live file -- the choice made again with the settings lock at
  101  		// `lockPath` held, and written back under it with the mode every copy
  102  		// shares (audit of the fix round G2-E-core-02). The write-back used to
  103  		// run without the lock every other writer of the file takes, so a
  104  		// set_setting that landed between the choice and the write was lost
  105  		// under it. The answer is the choice the text was read from. With the
  106  		// lock busy past `timeoutMs` it is the first choice and nothing is
  107  		// written: the next save, under the lock, merges onto the same
  108  		// recovery (saveUnderLock).
  109  		LoadedConfig loadUnderLock(const std::string& path, const std::string& lockPath, int timeoutMs,
  110  			RecoveryWrite* wrote = nullptr);
  111  
  112  		// Whether another process holds an flock on `path` now: the cloud
  113  		// scripts' transfer lock, /var/run/cloud_sync.lock, which every
  114  		// cloud_backup, cloud_restore and content run takes for its whole
  115  		// length (PL-068). Asked the way `flock -n <path> true` asks: an
  116  		// exclusive lock tried without waiting and let go at once -- the
  117  		// scripts give a busy lock a second before they give up, so the
  118  		// instant this holds it costs them nothing. No file is nobody's lock;
  119  		// a file that cannot be opened or asked is taken as held, since the
  120  		// callers refuse on held.
  121  		bool isFlockHeld(const std::string& path);
  122  
  123  		// A key=*** text as SystemConf reads it: comment lines (# or ;)
  124  		// and lines without a key or a value skipped, the last of a repeated
  125  		// key kept.
  126  		std::map<std::string, std::string> parseKeyValues(const std::string& text);
  127  
  128  		// A change the interface made and has not saved yet (a save refused
  129  		// for the lock keeps it, PL-024): its value, and what the key held
  130  		// when the change was made -- hadBase false when it held nothing.
  131  		struct PendingChange
  132  		{
  133  			std::string value;
  134  			bool hadBase = false;
  135  			std::string base;
  136  		};
  137  
  138  		// Which pending changes a reload of the file keeps (audit of the fixes
  139  		// G-E1-03): each whose key the file still holds as it was when the
  140  		// change was made, which is then made again at the next save. A key
  141  		// the file now holds differently was written by somebody else since --
  142  		// wifictl join's wifi.ssid, a script's set_setting -- and that newer
  143  		// write wins. The answer is the changes to keep, key to value.
  144  		std::map<std::string, std::string> pendingAfterReload(const std::map<std::string, PendingChange>& pending,
  145  			const std::map<std::string, std::string>& reloaded);
  146  
  147  		// What a read-modify-write under the settings lock came to.
  148  		enum class LockedSave
  149  		{
  150  			Written,       // read, merged, written whole, with the lock held throughout
  151  			LockBusy,      // the lock stayed with a live holder past the budget: nothing read, nothing written
  152  			Unreadable,    // the lock was held and the file could not be read whole: nothing written
  153  			WriteFailed    // read and merged, and the write did not land: the file is as it was
  154  		};
  155  
  156  		// system.cfg's save (SystemConf): take the lock at `lockPath` within
  157  		// `timeoutMs`, read `path`, hand its text to `merge`, write what comes
  158  		// back whole, release. `written`, when given, gets the text that went
  159  		// to disk on Written. Nothing is written without the lock (PL-024):
  160  		// the shell's set_setting reads, writes a temporary and renames it
  161  		// under that lock, and a save made beside it -- the interface's
  162  		// snapshot of the file renamed over the shell's new one, or the other
  163  		// way round -- lost one of the two writers' keys. The caller keeps its
  164  		// changes on any answer but Written and makes them at its next save.
  165  		// A live file that is empty, cut part way through a line or unusable
  166  		// is not merged onto where chooseConfig names a recovery beside it --
  167  		// the whole temporary it is the start of, the whole record: the save
  168  		// merges onto that, with the mode every copy shares (audit of the fix
  169  		// round G2-E-core-03). `baseComplete`, when given, says whether the
  170  		// text merged onto was whole (not empty, ending in a line end): a save
  171  		// merged onto a cut file is written, and must not become the
  172  		// last-known-good record (audit of the fixes G-E1-04).
  173  		LockedSave saveUnderLock(const std::string& path, const std::string& lockPath, int timeoutMs,
  174  			const std::function<std::string(const std::string& current)>& merge, std::string* written = nullptr,
  175  			bool* baseComplete = nullptr);
  176  
  177  		// The settings lock the shell takes around every get_setting and
  178  		// set_setting (wait_lock in profile.d/001-functions): a file holding
  179  		// the owner's pid, whose creation fails when it is already there.
  180  		// Same rules, so both sides can wait on each other: a lock whose pid
  181  		// is alive is waited for; one whose pid is gone, or that names no pid,
  182  		// is stale and removed. Released only while it still carries this
  183  		// process's pid.
  184  		//
  185  		// This side's lock is linked into place already holding the pid, so
  186  		// no waiter ever sees it empty (PL-041); and a stale lock is removed
  187  		// under an flock on `path`.reap, re-read first, so two waiters that
  188  		// both judged one dead holder's lock stale cannot remove each other's
  189  		// new one; the shell's wait_lock takes the same flock. The guard is
  190  		// asked without waiting past the budget, and a guard that cannot be
  191  		// had removes nothing (audit of the fixes G-E1-01/02). The shell
  192  		// waits forever; acquire() takes a budget, because it runs on the
  193  		// interface thread.
  194  		class PidLock
  195  		{
  196  		public:
  197  			explicit PidLock(const std::string& path);
  198  			~PidLock();
  199  
  200  			// True when the lock is held. False when the budget ran out with
  201  			// a live holder still on it, or when the lock file could not be
  202  			// created at all (its directory missing) -- the caller decides
  203  			// whether to go on without it.
  204  			bool acquire(int timeoutMs);
  205  			void release();
  206  			bool held() const { return mHeld; }
  207  
  208  		private:
  209  			std::string mPath;
  210  			bool mHeld;
  211  		};
  212  	}
  213  }
  214  
  215  #endif // ES_CORE_UTILS_ATOMIC_FILE_UTIL_H
```


## es-core/src/utils/AtomicFileUtil.cpp @ 16dbac5211 (whole, 829 lines)

```text
    1  #include "utils/AtomicFileUtil.h"
    2  
    3  #include <atomic>
    4  #include <chrono>
    5  #include <cstdio>
    6  #include <cstdlib>
    7  #include <fstream>
    8  #include <sstream>
    9  #include <thread>
   10  
   11  #if !defined(_WIN32)
   12  #include <fcntl.h>
   13  #include <signal.h>
   14  #include <sys/file.h>
   15  #include <sys/stat.h>
   16  #include <sys/types.h>
   17  #include <unistd.h>
   18  #include <errno.h>
   19  #endif
   20  
   21  namespace Utils
   22  {
   23  	namespace AtomicFile
   24  	{
   25  #if !defined(_WIN32)
   26  		// fsync the directory holding `path`, so the rename that just landed
   27  		// in it is on disk too. Best effort: a filesystem that refuses to
   28  		// open a directory for reading still has the rename in its journal.
   29  		static void syncDirectoryOf(const std::string& path)
   30  		{
   31  			auto slash = path.find_last_of('/');
   32  			const std::string dir = slash == std::string::npos ? "." : slash == 0 ? "/" : path.substr(0, slash);
   33  			int fd = ::open(dir.c_str(), O_RDONLY | O_DIRECTORY);
   34  			if (fd < 0)
   35  				return;
   36  			::fsync(fd);
   37  			::close(fd);
   38  		}
   39  
   40  		// A name beside `path` that no other call -- in this process or any
   41  		// other -- is using: `path`.tmp.<pid>.<n>, created O_EXCL so a name
   42  		// left behind by a process that died and whose pid came round again
   43  		// is stepped over rather than truncated. Every writer used to share
   44  		// `path`.tmp under O_TRUNC (PL-063), and so did the shell: set_setting
   45  		// writes system.cfg.tmp with awk and renames it. Two saves at once
   46  		// truncated each other's temporary; the first renamed the shared file
   47  		// into place -- empty or half written -- and the second's rename found
   48  		// the name gone and reported a save that had not happened. The fd is
   49  		// returned open for writing, -1 on failure.
   50  		static int createTemporary(const std::string& path, std::string& tmp, int mode)
   51  		{
   52  			static std::atomic<unsigned long> counter(0);
   53  			const std::string stem = path + ".tmp." + std::to_string((long long) ::getpid()) + ".";
   54  			for (int attempt = 0; attempt < 100; attempt++)
   55  			{
   56  				tmp = stem + std::to_string(counter++);
   57  				int fd = ::open(tmp.c_str(), O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, (mode_t) mode);
   58  				if (fd >= 0)
   59  					return fd;
   60  				if (errno != EEXIST)
   61  					return -1;
   62  			}
   63  			return -1;
   64  		}
   65  #endif
   66  
   67  		int modeOf(const std::string& path, int fallback)
   68  		{
   69  #if defined(_WIN32)
   70  			(void) path;
   71  			return fallback;
   72  #else
   73  			struct stat st;
   74  			if (::stat(path.c_str(), &st) != 0 || !S_ISREG(st.st_mode))
   75  				return fallback;
   76  			return (int) (st.st_mode & 07777);
   77  #endif
   78  		}
   79  
   80  		bool writeText(const std::string& path, const std::string& text, int mode)
   81  		{
   82  #if defined(_WIN32)
   83  			const std::string tmp = path + ".tmp";
   84  			{
   85  				std::ofstream out(tmp, std::ios::binary | std::ios::trunc);
   86  				if (!out)
   87  					return false;
   88  				out.write(text.data(), (std::streamsize) text.size());
   89  				if (!out)
   90  				{
   91  					out.close();
   92  					std::remove(tmp.c_str());
   93  					return false;
   94  				}
   95  			}
   96  			std::remove(path.c_str());
   97  			if (std::rename(tmp.c_str(), path.c_str()) != 0)
   98  			{
   99  				std::remove(tmp.c_str());
  100  				return false;
  101  			}
  102  			return true;
  103  #else
  104  			// The rename puts the temporary's mode and owner on the live name,
  105  			// so a file being replaced gives the temporary its own first
  106  			// (#308 F-ES-08): system.cfg and es_settings.cfg carry the Wi-Fi
  107  			// key and the account passwords, and a file somebody had made 0600
  108  			// came back 0644 from the next save. A new file is made 0644,
  109  			// before umask, as the shell's redirections make one -- unless the
  110  			// caller names the mode, which a record of a private file does.
  111  			struct stat existing;
  112  			const bool replacing = ::stat(path.c_str(), &existing) == 0 && S_ISREG(existing.st_mode);
  113  
  114  			std::string tmp;
  115  			int fd = createTemporary(path, tmp, mode >= 0 ? 0600 : replacing ? 0600 : 0644);
  116  			if (fd < 0)
  117  				return false;
  118  			if (mode >= 0)
  119  			{
  120  				if (::fchmod(fd, (mode_t) (mode & 07777)) != 0)
  121  				{
  122  					::close(fd);
  123  					::unlink(tmp.c_str());
  124  					return false;
  125  				}
  126  			}
  127  			else if (replacing)
  128  			{
  129  				// The owner only where it differs and only as root, which is
  130  				// how ROCKNIX runs the interface; best effort, since a caller
  131  				// that cannot give a file away still wrote what it meant to.
  132  				// The mode is not best effort: a file that would come out less
  133  				// private than it was is not written.
  134  				if ((existing.st_uid != ::geteuid() || existing.st_gid != ::getegid()) && ::geteuid() == 0)
  135  				{
  136  					if (::fchown(fd, existing.st_uid, existing.st_gid) != 0)
  137  					{
  138  						// kept as it is: root that cannot chown is a filesystem without owners
  139  					}
  140  				}
  141  				if (::fchmod(fd, existing.st_mode & 07777) != 0)
  142  				{
  143  					::close(fd);
  144  					::unlink(tmp.c_str());
  145  					return false;
  146  				}
  147  			}
  148  
  149  			const char* data = text.data();
  150  			size_t left = text.size();
  151  			bool ok = true;
  152  			while (left > 0)
  153  			{
  154  				ssize_t n = ::write(fd, data, left);
  155  				if (n < 0)
  156  				{
  157  					if (errno == EINTR)
  158  						continue;
  159  					ok = false;
  160  					break;
  161  				}
  162  				data += n;
  163  				left -= (size_t) n;
  164  			}
  165  			// The data must be on disk before the rename makes it the file
  166  			// everything reads: rename first and a power cut leaves a
  167  			// complete-looking name over empty blocks.
  168  			if (ok && ::fsync(fd) != 0)
  169  				ok = false;
  170  			if (::close(fd) != 0)
  171  				ok = false;
  172  			if (!ok)
  173  			{
  174  				::unlink(tmp.c_str());
  175  				return false;
  176  			}
  177  			if (std::rename(tmp.c_str(), path.c_str()) != 0)
  178  			{
  179  				::unlink(tmp.c_str());
  180  				return false;
  181  			}
  182  			syncDirectoryOf(path);
  183  			return true;
  184  #endif
  185  		}
  186  
  187  		// Read whole, or say it was not (PL-065). This used to say ok once the
  188  		// stream had opened, whatever the read then did: an I/O error part way
  189  		// through a failing card returned the prefix as the whole file, and
  190  		// SystemConf parsed it and recorded it as the last known good. Now ok
  191  		// means every read succeeded to the end, and for a regular file that
  192  		// the end was no shorter than the size it had when it was opened -- a
  193  		// file cut under the reader is not the file. On any failure the text
  194  		// is "", as for a file that would not open.
  195  		std::string readText(const std::string& path, bool* ok)
  196  		{
  197  			if (ok != nullptr)
  198  				*ok = false;
  199  #if defined(_WIN32)
  200  			// C stdio, whose ferror says whether a read failed. The stream
  201  			// version read failbit on its ostringstream as a failure, and
  202  			// `ss << in.rdbuf()` sets it when nothing is inserted: an empty
  203  			// file came back not read (audit of the fixes G-E1-06, claude).
  204  			FILE* file = std::fopen(path.c_str(), "rb");
  205  			if (file == nullptr)
  206  				return "";
  207  			std::string text;
  208  			char buffer[65536];
  209  			size_t n;
  210  			while ((n = std::fread(buffer, 1, sizeof(buffer), file)) > 0)
  211  				text.append(buffer, n);
  212  			const bool failed = std::ferror(file) != 0;
  213  			std::fclose(file);
  214  			if (failed)
  215  				return "";
  216  			if (ok != nullptr)
  217  				*ok = true;
  218  			return text;
  219  #else
  220  			int fd = ::open(path.c_str(), O_RDONLY | O_CLOEXEC);
  221  			if (fd < 0)
  222  				return "";
  223  			struct stat st;
  224  			if (::fstat(fd, &st) != 0)
  225  			{
  226  				::close(fd);
  227  				return "";
  228  			}
  229  
  230  			std::string text;
  231  			if (S_ISREG(st.st_mode) && st.st_size > 0)
  232  				text.reserve((size_t) st.st_size);
  233  			char buffer[65536];
  234  			for (;;)
  235  			{
  236  				const ssize_t n = ::read(fd, buffer, sizeof(buffer));
  237  				if (n < 0)
  238  				{
  239  					if (errno == EINTR)
  240  						continue;
  241  					::close(fd);   // EIO part way, EISDIR on a directory: not a read
  242  					return "";
  243  				}
  244  				if (n == 0)
  245  					break;
  246  				text.append(buffer, (size_t) n);
  247  			}
  248  			::close(fd);
  249  
  250  			if (S_ISREG(st.st_mode) && (off_t) text.size() < st.st_size)
  251  				return "";
  252  			if (ok != nullptr)
  253  				*ok = true;
  254  			return text;
  255  #endif
  256  		}
  257  
  258  		bool copy(const std::string& src, const std::string& dst)
  259  		{
  260  			bool ok = false;
  261  			const std::string text = readText(src, &ok);
  262  			if (!ok)
  263  				return false;
  264  			return writeText(dst, text, modeOf(src, 0644));
  265  		}
  266  
  267  		bool isUsableKeyValues(const std::string& text)
  268  		{
  269  			if (text.empty() || text.find('\0') != std::string::npos)
  270  				return false;
  271  			std::istringstream in(text);
  272  			std::string line;
  273  			while (std::getline(in, line))
  274  			{
  275  				auto idx = line.find('=');
  276  				if (idx != std::string::npos && idx > 0 && line[0] != '#' && line[0] != ';')
  277  					return true;
  278  			}
  279  			return false;
  280  		}
  281  
  282  		// Whole, as every writer of these files leaves one: each line ends in
  283  		// a line end -- ours, the shell's awk and sed, echo >>. A text that
  284  		// stops part way through a line was cut. (A cut exactly at a line end
  285  		// cannot be told from a shorter file; nothing here pretends to.)
  286  		static bool isComplete(const std::string& text)
  287  		{
  288  			return !text.empty() && text.back() == '\n';
  289  		}
  290  
  291  		LoadedConfig chooseConfig(const std::string& path)
  292  		{
  293  			// PL-064. The start used to delete `path`.tmp unread and take the
  294  			// live file whenever one key=*** line survived in it. The writer
  295  			// before #102 wrote the temporary whole, then truncated the live
  296  			// file and copied the temporary in: killed in the copy, it left the
  297  			// live file cut short beside a whole temporary, on a device that
  298  			// may never have run a build that keeps the record. So the
  299  			// temporary is read first, and wins when it is whole and the live
  300  			// file is gone, unusable, or a cut prefix of it; and "usable" for
  301  			// the record means complete as well -- for the record's own load
  302  			// too (PL-018).
  303  			LoadedConfig out;
  304  			bool liveOk = false, tmpOk = false, backupOk = false;
  305  			const std::string live = readText(path, &liveOk);
  306  			const std::string tmp = readText(path + ".tmp", &tmpOk);
  307  			const std::string backup = readText(path + ".backup", &backupOk);
  308  			const bool tmpWhole = tmpOk && isUsableKeyValues(tmp) && isComplete(tmp);
  309  			const bool backupWhole = backupOk && isUsableKeyValues(backup) && isComplete(backup);
  310  
  311  			// The mode the chosen text goes back with, and the record: the
  312  			// permission bits every copy on disk shares, so a recovery is never
  313  			// less private than a copy it came from (audit of the fixes
  314  			// G-E1-05: a 0600 temporary came back as a 0644 file and record).
  315  			int mode = 07777;
  316  			bool any = false;
  317  			for (const std::string& copy : { path, path + ".tmp", path + ".backup" })
  318  			{
  319  				const int m = modeOf(copy, -1);
  320  				if (m >= 0)
  321  				{
  322  					mode &= m;
  323  					any = true;
  324  				}
  325  			}
  326  			out.mode = any ? mode : 0644;
  327  
  328  			// The copy stopped part way: what is there is the start of the
  329  			// temporary, short of its end.
  330  			const bool liveCut = liveOk && tmpWhole && !isComplete(live)
  331  				&& live.size() < tmp.size() && tmp.compare(0, live.size(), live) == 0;
  332  
  333  			// Or the live file stops part way through a line and is the start
  334  			// of the whole record beside it, written no earlier than the live
  335  			// file was (G-E1-04): the file was cut after the record was made
  336  			// from it, and the record is the file. A live file changed after
  337  			// the record -- a hand edit that left off the last line end -- is
  338  			// the owner's, and is read as it is.
  339  			bool cutOfRecord = false;
  340  #if defined(_WIN32)
  341  			(void) backupWhole;   // the mtime test below is POSIX's
  342  #else
  343  			if (liveOk && backupWhole && !isComplete(live) && live.size() < backup.size()
  344  				&& backup.compare(0, live.size(), live) == 0)
  345  			{
  346  				struct stat ls, bs;
  347  				cutOfRecord = ::stat(path.c_str(), &ls) == 0 && ::stat((path + ".backup").c_str(), &bs) == 0
  348  					&& ls.st_mtime <= bs.st_mtime + 1;
  349  			}
  350  #endif
  351  
  352  			if (liveOk && isUsableKeyValues(live) && !liveCut && !cutOfRecord)
  353  			{
  354  				// A temporary beside a whole file is a save that never reached
  355  				// its rename, or the shell's own write in flight; neither is the
  356  				// file. A live file that is not whole is still read -- there is
  357  				// nothing better -- but it does not become the record.
  358  				out.source = LoadedConfig::Source::Live;
  359  				out.text = live;
  360  				out.record = isComplete(live);
  361  				return out;
  362  			}
  363  			if (liveCut)
  364  			{
  365  				out.source = LoadedConfig::Source::Temporary;
  366  				out.text = tmp;
  367  				out.record = true;
  368  				return out;
  369  			}
  370  
  371  			// The record only when it is whole (audit of the fix round PL-018):
  372  			// one key=*** line was enough, so a record cut short -- the cp at
  373  			// boot before #102 left such records -- beat a whole temporary,
  374  			// and with nothing better was written back as the live file. A cut
  375  			// record is not the last known good; with nothing else, nothing is
  376  			// loaded and the defaults answer, as chksysconfig has it.
  377  			if (backupWhole)
  378  			{
  379  				out.source = LoadedConfig::Source::Backup;
  380  				out.text = backup;
  381  				return out;
  382  			}
  383  			if (tmpWhole)
  384  			{
  385  				out.source = LoadedConfig::Source::Temporary;
  386  				out.text = tmp;
  387  				out.record = true;
  388  				return out;
  389  			}
  390  			if (liveOk)
  391  			{
  392  				out.source = LoadedConfig::Source::Damaged;
  393  				out.text = live;
  394  			}
  395  			return out;
  396  		}
  397  
  398  		// A choice that is to be written back as the live file.
  399  		static bool isRecovery(const LoadedConfig& chosen)
  400  		{
  401  			return chosen.source == LoadedConfig::Source::Temporary || chosen.source == LoadedConfig::Source::Backup;
  402  		}
  403  
  404  		LoadedConfig loadUnderLock(const std::string& path, const std::string& lockPath, int timeoutMs,
  405  			RecoveryWrite* wrote)
  406  		{
  407  			if (wrote != nullptr)
  408  				*wrote = RecoveryWrite::None;
  409  
  410  			LoadedConfig chosen = chooseConfig(path);
  411  			if (!isRecovery(chosen))
  412  				return chosen;
  413  
  414  			PidLock lock(lockPath);
  415  			if (!lock.acquire(timeoutMs))
  416  			{
  417  				if (wrote != nullptr)
  418  					*wrote = RecoveryWrite::LockBusy;
  419  				return chosen;
  420  			}
  421  
  422  			// Again, with the lock: a writer that held it while this waited may
  423  			// have put a whole file in place, and that file is the one to read.
  424  			chosen = chooseConfig(path);
  425  			if (!isRecovery(chosen))
  426  				return chosen;
  427  
  428  			const bool written = writeText(path, chosen.text, chosen.mode);
  429  			if (wrote != nullptr)
  430  				*wrote = written ? RecoveryWrite::Written : RecoveryWrite::WriteFailed;
  431  			return chosen;
  432  		}
  433  
  434  		bool isFlockHeld(const std::string& path)
  435  		{
  436  #if defined(_WIN32)
  437  			(void) path;
  438  			return false;
  439  #else
  440  			int fd = ::open(path.c_str(), O_RDONLY | O_CLOEXEC);
  441  			if (fd < 0)
  442  				return errno != ENOENT;
  443  			int r;
  444  			do
  445  				r = ::flock(fd, LOCK_EX | LOCK_NB);
  446  			while (r != 0 && errno == EINTR);
  447  			const bool held = r != 0;   // EWOULDBLOCK: somebody has it; anything else: cannot tell
  448  			::close(fd);                // and the lock, if this took it, with it
  449  			return held;
  450  #endif
  451  		}
  452  
  453  		std::map<std::string, std::string> parseKeyValues(const std::string& text)
  454  		{
  455  			std::map<std::string, std::string> values;
  456  			std::istringstream in(text);
  457  			std::string line;
  458  			while (std::getline(in, line))
  459  			{
  460  				const size_t idx = line.find('=');
  461  				if (idx == std::string::npos || line.find('#') == 0 || line.find(';') == 0)
  462  					continue;
  463  				const std::string key = line.substr(0, idx);
  464  				const std::string value = line.substr(idx + 1);
  465  				if (!key.empty() && !value.empty())
  466  					values[key] = value;
  467  			}
  468  			return values;
  469  		}
  470  
  471  		std::map<std::string, std::string> pendingAfterReload(const std::map<std::string, PendingChange>& pending,
  472  			const std::map<std::string, std::string>& reloaded)
  473  		{
  474  			std::map<std::string, std::string> kept;
  475  			for (const auto& change : pending)
  476  			{
  477  				const auto now = reloaded.find(change.first);
  478  				const bool hasNow = now != reloaded.cend();
  479  				if (hasNow != change.second.hadBase)
  480  					continue;   // added or removed by somebody since
  481  				if (hasNow && now->second != change.second.base)
  482  					continue;   // rewritten by somebody since
  483  				kept[change.first] = change.second.value;
  484  			}
  485  			return kept;
  486  		}
  487  
  488  		LockedSave saveUnderLock(const std::string& path, const std::string& lockPath, int timeoutMs,
  489  			const std::function<std::string(const std::string& current)>& merge, std::string* written,
  490  			bool* baseComplete)
  491  		{
  492  
  493  			// Not without the lock (PL-024). This used to log and go ahead once
  494  			// the budget ran out -- "the player's change dropped on the floor
  495  			// is the worse outcome" -- and the change was dropped anyway,
  496  			// under the other writer's rename, or it dropped theirs. Refused,
  497  			// the change is not lost: the caller keeps it and writes it at the
  498  			// next save, which reads the other writer's file first.
  499  			PidLock lock(lockPath);
  500  			if (!lock.acquire(timeoutMs))
  501  				return LockedSave::LockBusy;
  502  
  503  			bool opened = false;
  504  			const std::string current = readText(path, &opened);
  505  #if !defined(_WIN32)
  506  			if (!opened)
  507  				return LockedSave::Unreadable;
  508  #endif
  509  			// (On Windows a file not there yet is merged onto nothing and made,
  510  			// as SystemConf always did there.)
  511  
  512  			// Never onto a file the load would not have taken as the file (audit
  513  			// of the fix round, gpt G2-E-core-03). A live file that is empty,
  514  			// cut part way through a line or unusable is asked about as the
  515  			// load asks, and where chooseConfig names the recovery -- the whole
  516  			// temporary it is the start of, the whole record -- the save merges
  517  			// onto that, written with the mode every copy shares. An empty file
  518  			// used to count as whole: a save onto one wrote the changed keys
  519  			// alone, and they became the record over a whole one. A missing
  520  			// file is still refused above, so a factory reset's empty
  521  			// /storage is not refilled from memory.
  522  			std::string base = current;
  523  			bool whole = isComplete(current);
  524  			int mode = -1;
  525  			if (!whole || !isUsableKeyValues(current))
  526  			{
  527  				const LoadedConfig chosen = chooseConfig(path);
  528  				if (isRecovery(chosen))
  529  				{
  530  					base = chosen.text;
  531  					whole = true;
  532  					mode = chosen.mode;
  533  				}
  534  			}
  535  
  536  			// A save merged onto a cut file lands (the change is the player's)
  537  			// but is not a record (G-E1-04).
  538  			if (baseComplete != nullptr)
  539  				*baseComplete = whole;
  540  
  541  			const std::string out = merge(base);
  542  			if (!writeText(path, out, mode))
  543  				return LockedSave::WriteFailed;
  544  			if (written != nullptr)
  545  				*written = out;
  546  			return LockedSave::Written;
  547  		}
  548  
  549  		PidLock::PidLock(const std::string& path) : mPath(path), mHeld(false)
  550  		{
  551  		}
  552  
  553  		PidLock::~PidLock()
  554  		{
  555  			release();
  556  		}
  557  
  558  #if !defined(_WIN32)
  559  		// The first line of a lock file, without its line end: the holder's
  560  		// pid as both sides write it ("$$\n" from the shell).
  561  		static std::string lockHolder(const std::string& text)
  562  		{
  563  			std::string holder = text.substr(0, text.find('\n'));
  564  			while (!holder.empty() && (holder.back() == '\r' || holder.back() == ' '))
  565  				holder.pop_back();
  566  			return holder;
  567  		}
  568  
  569  		// Remove the lock at `path` only if it still names `holder`, with no
  570  		// other remover between that look and the unlink (PL-041). Every
  571  		// remover of a stale lock -- this process on any thread, and the
  572  		// shell's wait_lock, which takes the same guard -- takes an flock on
  573  		// `path`.reap for the few instructions this lasts. Under it nothing
  574  		// else can change what `path` names: a stale holder is gone and cannot
  575  		// release it, a live holder only ever releases a lock naming itself,
  576  		// and every other remover waits. So the re-read and the unlink are one
  577  		// step as far as the lock's users are concerned. The guard is an
  578  		// flock, so a remover that dies holding it frees it with its last
  579  		// descriptor -- there is no stale guard to clear.
  580  		//
  581  		// The guard is asked without waiting, until `deadline` (audit of the
  582  		// fixes G-E1-01: a blocking flock here held the interface thread past
  583  		// its budget for as long as another holder kept the guard). And a
  584  		// guard that cannot be had -- the file cannot be opened, the flock
  585  		// fails, the deadline comes -- removes nothing (G-E1-02): the re-read
  586  		// and unlink without it are the race the guard is for. False then;
  587  		// the caller waits on as for a live holder, and its budget ends it.
  588  		static bool removeIfStill(const std::string& path, const std::string& holder,
  589  			std::chrono::steady_clock::time_point deadline)
  590  		{
  591  			const std::string guard = path + ".reap";
  592  			int gfd = ::open(guard.c_str(), O_RDWR | O_CREAT | O_CLOEXEC, 0644);
  593  			if (gfd < 0)
  594  				return false;
  595  			for (;;)
  596  			{
  597  				if (::flock(gfd, LOCK_EX | LOCK_NB) == 0)
  598  					break;
  599  				if (errno == EINTR)
  600  					continue;
  601  				if (errno != EWOULDBLOCK || std::chrono::steady_clock::now() >= deadline)
  602  				{
  603  					::close(gfd);
  604  					return false;
  605  				}
  606  				std::this_thread::sleep_for(std::chrono::milliseconds(5));
  607  			}
  608  			bool again = false;
  609  			const std::string current = readText(path, &again);
  610  			if (again && lockHolder(current) == holder)
  611  				::unlink(path.c_str());
  612  			::close(gfd);   // and the flock with it
  613  			return true;
  614  		}
  615  #endif
  616  
  617  		bool PidLock::acquire(int timeoutMs)
  618  		{
  619  #if defined(_WIN32)
  620  			mHeld = true;
  621  			return true;
  622  #else
  623  			if (mHeld)
  624  				return true;
  625  
  626  			const auto started = std::chrono::steady_clock::now();
  627  			const std::string mine = std::to_string((long long) ::getpid());
  628  
  629  			// The lock is made whole before anybody can see it (PL-041): the
  630  			// pid goes into a file of this call's own beside it, and that file
  631  			// is hard-linked to the lock's name, which fails with EEXIST exactly
  632  			// as the O_EXCL create did. The lock used to be created empty and
  633  			// the pid written after, with the write's result thrown away, so a
  634  			// waiter reading in between saw an empty lock -- which both sides
  635  			// take for nobody's -- and a failed write left one for good.
  636  			static std::atomic<unsigned long> counter(0);
  637  			const std::string staging = mPath + ".new." + mine + "." + std::to_string(counter++);
  638  			bool linkable = true;
  639  			{
  640  				int fd = ::open(staging.c_str(), O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0644);
  641  				if (fd < 0)
  642  					return false;   // the directory is missing or not writable: nothing to hold
  643  				const std::string line = mine + "\n";
  644  				ssize_t n;
  645  				do
  646  					n = ::write(fd, line.data(), line.size());
  647  				while (n < 0 && errno == EINTR);
  648  				const bool written = n == (ssize_t) line.size();
  649  				if (::close(fd) != 0 || !written)
  650  				{
  651  					::unlink(staging.c_str());
  652  					return false;
  653  				}
  654  			}
  655  
  656  			// The clock is read on every pass, whichever way the pass went
  657  			// (#308 F-ES-07): the budget used to be checked only after a live
  658  			// holder was found, so a lock that could never be read or never
  659  			// be removed -- a directory where the lock goes -- kept the
  660  			// interface thread in this loop for good.
  661  			auto expired = [&]() {
  662  				const long elapsed = (long) std::chrono::duration_cast<std::chrono::milliseconds>(
  663  					std::chrono::steady_clock::now() - started).count();
  664  				if (elapsed < timeoutMs)
  665  					return false;
  666  				::unlink(staging.c_str());
  667  				return true;
  668  			};
  669  
  670  			for (;;)
  671  			{
  672  				int made = -1;
  673  				if (linkable)
  674  				{
  675  					made = ::link(staging.c_str(), mPath.c_str());
  676  					if (made != 0 && errno != EEXIST)
  677  					{
  678  						// A filesystem with no hard links (EPERM, ENOTSUP): the
  679  						// create the shell makes, then the pid, and the write's
  680  						// result checked this time.
  681  						if (errno == EPERM || errno == ENOTSUP || errno == EOPNOTSUPP || errno == EXDEV || errno == EMLINK)
  682  							linkable = false;
  683  						else
  684  						{
  685  							::unlink(staging.c_str());
  686  							return false;
  687  						}
  688  					}
  689  				}
  690  				if (!linkable)
  691  				{
  692  					int fd = ::open(mPath.c_str(), O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0644);
  693  					if (fd >= 0)
  694  					{
  695  						const std::string line = mine + "\n";
  696  						const bool written = ::write(fd, line.data(), line.size()) == (ssize_t) line.size();
  697  						if (::close(fd) != 0 || !written)
  698  						{
  699  							::unlink(mPath.c_str());
  700  							::unlink(staging.c_str());
  701  							return false;
  702  						}
  703  						made = 0;
  704  					}
  705  					else if (errno != EEXIST)
  706  					{
  707  						::unlink(staging.c_str());
  708  						return false;
  709  					}
  710  				}
  711  				if (made == 0)
  712  				{
  713  					::unlink(staging.c_str());
  714  					mHeld = true;
  715  					return true;
  716  				}
  717  
  718  				// Held -- or was. Something that is not a file where the lock
  719  				// goes is nobody's lock and never will be: nothing here or in
  720  				// the shell removes a directory, so there is nothing to wait
  721  				// for.
  722  				struct stat st;
  723  				if (::lstat(mPath.c_str(), &st) == 0 && !S_ISREG(st.st_mode))
  724  				{
  725  					::unlink(staging.c_str());
  726  					return false;
  727  				}
  728  
  729  				// Read who by, and ask the kernel.
  730  				bool ok = false;
  731  				const std::string holder = lockHolder(readText(mPath, &ok));
  732  				if (!ok)
  733  				{
  734  					if (expired())
  735  						return false;
  736  					// Released between the create and the read: try again at
  737  					// once. Anything else that stops the read -- a lock this
  738  					// process may not read -- is tried again after a pause,
  739  					// until the budget is spent.
  740  					if (::access(mPath.c_str(), F_OK) == 0)
  741  						std::this_thread::sleep_for(std::chrono::milliseconds(50));
  742  					continue;
  743  				}
  744  
  745  				bool numeric = !holder.empty();
  746  				for (char c : holder)
  747  					if (c < '0' || c > '9')
  748  						numeric = false;
  749  
  750  				bool stale;
  751  				if (!numeric)
  752  				{
  753  					// Empty, or not a pid: nobody can be holding it. An
  754  					// empty file is also what the shell's own create looks
  755  					// like between its open and its write, for a few
  756  					// microseconds -- so give it a moment before deciding,
  757  					// and re-read before removing (below). This process's
  758  					// own locks are never empty (above).
  759  					std::this_thread::sleep_for(std::chrono::milliseconds(20));
  760  					stale = true;
  761  				}
  762  				else
  763  				{
  764  					const pid_t pid = (pid_t) atol(holder.c_str());
  765  					// kill 0 asks without signalling. ESRCH is the one
  766  					// answer that means gone; EPERM is a live process this
  767  					// one may not signal, which is still a live holder.
  768  					stale = pid > 0 && ::kill(pid, 0) != 0 && errno == ESRCH;
  769  				}
  770  
  771  				if (stale)
  772  				{
  773  					// Only if it still says what was read above, and with no
  774  					// other waiter between that look and the remove: two
  775  					// waiters that both judged one dead holder's lock stale
  776  					// used to be able to remove each other's new one -- the
  777  					// first removed it and took it, and the second's remove,
  778  					// two steps after its re-read, took the first's new lock
  779  					// with it (PL-041).
  780  					const bool reaped = removeIfStill(mPath, holder, started + std::chrono::milliseconds(timeoutMs));
  781  					if (expired())
  782  						return false;
  783  					// Retry at once, there is nothing to wait for -- unless the
  784  					// guard could not be had (G-E1-02), or the remove did not
  785  					// take (a directory that will not let go of the name),
  786  					// which a pause keeps from spinning.
  787  					bool still = false;
  788  					if (!reaped || (lockHolder(readText(mPath, &still)) == holder && still))
  789  						std::this_thread::sleep_for(std::chrono::milliseconds(50));
  790  					continue;
  791  				}
  792  
  793  				if (expired())
  794  					return false;
  795  				std::this_thread::sleep_for(std::chrono::milliseconds(50));
  796  			}
  797  #endif
  798  		}
  799  
  800  		void PidLock::release()
  801  		{
  802  			if (!mHeld)
  803  				return;
  804  			mHeld = false;
  805  #if !defined(_WIN32)
  806  			// Only a lock this process still holds: another process may own
  807  			// the file by now if this one's was removed as stale. A lock that
  808  			// is not there at all is looked for again for a moment: a waiter
  809  			// that moves a lock aside to judge it (the shell's own reaper may)
  810  			// puts a live holder's back within microseconds, and a release
  811  			// that gave up in that instant would leave a lock naming this
  812  			// process -- alive, and never going to release it.
  813  			const std::string mine = std::to_string((long long) ::getpid());
  814  			for (int attempt = 0; attempt < 20; attempt++)
  815  			{
  816  				bool ok = false;
  817  				const std::string holder = lockHolder(readText(mPath, &ok));
  818  				if (ok)
  819  				{
  820  					if (holder == mine)
  821  						::unlink(mPath.c_str());
  822  					return;
  823  				}
  824  				std::this_thread::sleep_for(std::chrono::milliseconds(1));
  825  			}
  826  #endif
  827  		}
  828  	}
  829  }
```


## es-core/src/SystemConf.h @ 16dbac5211 (whole, 94 lines)

```text
    1  #ifndef EMULATIONSTATION_ALL_SYSTEMCONF_H
    2  #define EMULATIONSTATION_ALL_SYSTEMCONF_H
    3  
    4  
    5  #include <string>
    6  #include <map>
    7  #include <set>
    8  #include <utility>
    9  
   10  class SystemConf 
   11  {
   12  public:
   13  	static SystemConf* getInstance();
   14  	
   15  	static bool getIncrementalSaveStates();
   16  	static bool getIncrementalSaveStatesUseCurrentSlot();
   17  
   18  	// Read system.cfg (again). keepPending keeps the changes a save has not
   19  	// made yet -- one the lock refused (PL-024) -- except where the file now
   20  	// holds a key differently than when it was changed (audit of the fixes
   21  	// G-E1-03, Utils::AtomicFile::pendingAfterReload): the Wi-Fi picker's
   22  	// reload after wifictl join wrote the network. A reload that reads
   23  	// nothing keeps them all and answers false (audit of the fix round,
   24  	// G2-E-core-06). Without it every change is dropped and the file's
   25  	// values stand, which is what a reload after a settings restore or a
   26  	// factory reset is for.
   27      bool loadSystemConf(bool keepPending = false);
   28      bool saveSystemConf();
   29  
   30  	// True when this start found system.cfg missing, empty or damaged and
   31  	// loaded its last-known-good record (system.cfg.backup) in its place,
   32  	// writing that back as the live file. main() tells the player once, after
   33  	// the interface is up (D-CLOUD-079).
   34  	static bool wasRecovered() { return sRecovered; }
   35  
   36      std::string get(const std::string &name);
   37      bool set(const std::string &name, const std::string &value);
   38  
   39  	bool getBool(const std::string &name, bool defaultValue = false);
   40  	bool setBool(const std::string &name, bool value);
   41  
   42  private:
   43  	SystemConf();
   44  	static SystemConf* sInstance;
   45  	static bool sRecovered;
   46  
   47  	// The shell's settings lock (wait_lock in profile.d/001-functions) and
   48  	// how long the interface waits for it. Members rather than literals so
   49  	// the unit tests can point them at a scratch directory and a short
   50  	// budget; nothing else sets them.
   51  	static std::string sLockPath;
   52  	static int sLockBudgetMs;
   53  	// es-app/tests/unit/SystemConfTests.cpp: a fresh instance per case,
   54  	// against real files in a scratch directory (the audit of the fix round).
   55  	friend struct SystemConfTestAccess;
   56  
   57  	// Parse key=*** lines into confMap. Comments and blank lines skipped,
   58  	// as the file has always been read.
   59  	void parseSystemConf(const std::string& text);
   60  	// The last-known-good record beside the live file: written only from
   61  	// text that has just been read whole and found well-formed, or that this
   62  	// process has just written -- never from whatever happens to be on disk.
   63  	// Made with the live file's mode, or with `recoveredMode` when a
   64  	// recovery gives one (the mode every copy on disk shares).
   65  	void recordLastGood(const std::string& text, int recoveredMode = -1);
   66  	// changedConf's keys applied to the file's text as read under the lock.
   67  	std::string applyChanges(const std::string& current);
   68  
   69  	// The file as read, and the load itself (loadSystemConf wraps it).
   70  	bool loadFromDisk();
   71  	// The last loadFromDisk read a live file the check found unusable, with
   72  	// no whole record and no whole temporary (Source::Damaged): it parsed
   73  	// what it could and returned true, so a reload that keeps its pending
   74  	// changes treats it as nothing read (the audit of the fixes, claude
   75  	// G3-E-06 -- every change looked removed by somebody).
   76  	bool mLoadDamaged = false;
   77  
   78  	std::map<std::string, std::string> confMap;
   79  	std::set<std::string> changedConf;
   80  	// For each key in changedConf: what it held when it was first changed
   81  	// since the last save (false: nothing), for a reload to tell the player's
   82  	// change from somebody else's newer write (G-E1-03).
   83  	std::map<std::string, std::pair<bool, std::string>> mPendingBase;
   84  	// The values of the text the last load parsed or the last save wrote,
   85  	// alone -- confMap also carries keys the file no longer has. A change's
   86  	// base comes from here (G2-E-core-07).
   87  	std::map<std::string, std::string> mOnDisk;
   88  
   89  
   90  	std::string mSystemConfFile;
   91  };
   92  
   93  
   94  #endif //EMULATIONSTATION_ALL_SYSTEMCONF_H
```


## es-core/src/SystemConf.cpp @ 16dbac5211 (whole, 494 lines)

```text
    1  #include "SystemConf.h"
    2  #include <iostream>
    3  #include <fstream>
    4  #include "Log.h"
    5  #include "utils/StringUtil.h"
    6  #include "utils/FileSystemUtil.h"
    7  #include "Settings.h"
    8  #include "Paths.h"
    9  #include "utils/AtomicFileUtil.h"
   10  
   11  #include <cstdio>
   12  #include <set>
   13  #include <regex>
   14  #include <string>
   15  #include <sstream>
   16  #include <iostream>
   17  #include <SDL_timer.h>
   18  
   19  static std::string mapSettingsName(const std::string& name)
   20  {
   21  	if (name == "system.language")
   22  		return "Language";
   23  
   24  	return name;
   25  }
   26  
   27  SystemConf *SystemConf::sInstance = NULL;
   28  bool SystemConf::sRecovered = false;
   29  std::string SystemConf::sLockPath = "/tmp/.system.cfg.lock";
   30  int SystemConf::sLockBudgetMs = 5000;
   31  
   32  static std::set<std::string> dontRemoveValue
   33  {
   34  	{ "audio.device" },
   35  	{ "updates.branch" }
   36  };
   37  
   38  static std::map<std::string, std::string> defaults =
   39  {
   40  	{ "kodi.enabled", "1" },
   41  	{ "kodi.atstartup", "0" },
   42  	{ "audio.bgmusic", "1" },
   43  	{ "wifi.enabled", "0" },
   44  	{ "system.hostname", "BATOCERA" }, // batocera
   45  	{ "global.retroachievements", "0" },
   46  	{ "global.retroachievements.hardcore", "0" },
   47  	{ "global.retroachievements.leaderboards", "0" },
   48  	{ "global.retroachievements.verbose", "0" },
   49  	{ "global.retroachievements.screenshot", "0" },
   50  	{ "global.retroachievements.username", "" },
   51  	{ "global.retroachievements.password", "" },
   52  	{ "global.netplay_public_announce", "1" },
   53  	{ "global.ai_service_enabled", "0" },
   54  };
   55  
   56  SystemConf::SystemConf() 
   57  {
   58  	mSystemConfFile = Paths::getSystemConfFilePath();
   59  	if (mSystemConfFile.empty())
   60  		return;
   61  
   62  	loadSystemConf();	
   63  }
   64  
   65  SystemConf *SystemConf::getInstance() 
   66  {
   67      if (sInstance == NULL)
   68          sInstance = new SystemConf();
   69  
   70      return sInstance;
   71  }
   72  
   73  void SystemConf::parseSystemConf(const std::string& text)
   74  {
   75  	// The same reading as ever (Utils::AtomicFile::parseKeyValues), kept
   76  	// alone as well for a reload's comparison (G-E1-03).
   77  	mOnDisk = Utils::AtomicFile::parseKeyValues(text);
   78  	for (const auto& kv : mOnDisk)
   79  		confMap[kv.first] = kv.second;
   80  }
   81  
   82  // One record at rest, under the name the boot scripts already use
   83  // (system.cfg.backup, D-CLOUD-079). Written whole through a temporary and a
   84  // rename, like the live file, and only when it would change -- this runs at
   85  // every start and after every save, and most of those change nothing.
   86  void SystemConf::recordLastGood(const std::string& text, int recoveredMode)
   87  {
   88  	// The load/save released its lock before reaching this publication.
   89  	// Reacquire and compare the complete current choice under the lock: a
   90  	// script's newer state must win over this call's older snapshot (#320).
   91  	Utils::AtomicFile::PidLock lock(sLockPath);
   92  	if (!lock.acquire(sLockBudgetMs))
   93  		return;
   94  	const auto current = Utils::AtomicFile::chooseConfig(mSystemConfFile);
   95  	if (current.text != text ||
   96  		(!current.record && current.source != Utils::AtomicFile::LoadedConfig::Source::Backup))
   97  		return;
   98  
   99  	// No less private than the live file it copies (#308 F-ES-08): a record
  100  	// an earlier build made 0644 beside a 0600 file is rewritten for its mode
  101  	// even when its text is the same. A recovery passes the mode every copy
  102  	// on disk shares (chooseConfig, G-E1-05): the live file may be the copy
  103  	// that could not be written back, and its mode -- or 0644 where there
  104  	// is no file -- made a 0600 temporary's text a 0644 record (audit of the
  105  	// fix round, gpt G2-E-core-05).
  106  	const std::string backup = mSystemConfFile + ".backup";
  107  	const int mode = current.mode & (recoveredMode >= 0 ? recoveredMode : 07777);
  108  	if (Utils::AtomicFile::readText(backup) == text && Utils::AtomicFile::modeOf(backup, mode) == mode)
  109  		return;
  110  	if (!Utils::AtomicFile::writeText(backup, text, mode))
  111  		LOG(LogWarning) << "Unable to write the last-known-good record " << backup;
  112  }
  113  
  114  // Read the live file if it is usable; else an unfinished save's whole
  115  // temporary where the live file was cut (PL-064); else the last-known-good
  116  // record, and put that back as the live file; else whatever is there, so a
  117  // device whose file fails this check but was fine for years reads exactly as
  118  // before, and nothing is written over it (D-CLOUD-078: never defaults over a
  119  // file that failed to parse before the recovery was tried). Which one is
  120  // Utils::AtomicFile::chooseConfig's call; the writes and the words are here.
  121  bool SystemConf::loadSystemConf(bool keepPending)
  122  {
  123  	if (mSystemConfFile.empty())
  124  		return true;
  125  
  126  	// The changes not saved yet, with what each key held when it was
  127  	// changed (G-E1-03).
  128  	std::map<std::string, Utils::AtomicFile::PendingChange> pending;
  129  	if (keepPending)
  130  	{
  131  		for (const auto& key : changedConf)
  132  		{
  133  			Utils::AtomicFile::PendingChange change;
  134  			change.value = confMap[key];
  135  			const auto base = mPendingBase.find(key);
  136  			if (base != mPendingBase.cend())
  137  			{
  138  				change.hadBase = base->second.first;
  139  				change.base = base->second.second;
  140  			}
  141  			pending[key] = change;
  142  		}
  143  	}
  144  	const auto bases = mPendingBase;
  145  	const std::set<std::string> unsaved = changedConf;
  146  	const auto onDiskBefore = mOnDisk;
  147  
  148  	changedConf.clear();
  149  	mPendingBase.clear();
  150  	mOnDisk.clear();
  151  	mLoadDamaged = false;
  152  	const bool loaded = loadFromDisk();
  153  
  154  	// Nothing read is no evidence about any key (audit of the fix round,
  155  	// gpt G2-E-core-06): the empty reading made every change to a key the
  156  	// file held look removed by somebody since, and it was dropped from the
  157  	// pending set and from memory before the false came back. The changes
  158  	// stay, with their bases and the last reading of the file, for the
  159  	// next save or the next reload that reads something.
  160  	// A damaged reading is no evidence either (claude G3-E-06): its parse has
  161  	// no usable line, and the comparison below would drop every change.
  162  	if ((!loaded || mLoadDamaged) && keepPending)
  163  	{
  164  		changedConf = unsaved;
  165  		mPendingBase = bases;
  166  		mOnDisk = onDiskBefore;
  167  		if (!unsaved.empty())
  168  			LOG(LogWarning) << "loadSystemConf: " << mSystemConfFile << (mLoadDamaged ? " was read with no usable line" : " could not be read") << " -- the " << unsaved.size()
  169  				<< " change(s) not saved yet are kept for the next save";
  170  		return false;
  171  	}
  172  
  173  	const auto kept = Utils::AtomicFile::pendingAfterReload(pending, mOnDisk);
  174  	// A change dropped here must not linger in memory where the file has no
  175  	// such key:*** the parse only adds, so the interface would go on showing a
  176  	// value nothing will ever save.
  177  	for (const auto& key : unsaved)
  178  		if (kept.find(key) == kept.cend() && mOnDisk.find(key) == mOnDisk.cend())
  179  			confMap.erase(key);
  180  
  181  	if (!pending.empty())
  182  	{
  183  		for (const auto& change : pending)
  184  			if (kept.find(change.first) == kept.cend())
  185  				LOG(LogInfo) << "loadSystemConf: " << change.first << " was changed in " << mSystemConfFile
  186  					<< " since this interface changed it -- the file's value stands";
  187  		for (const auto& kv : kept)
  188  		{
  189  			confMap[kv.first] = kv.second;
  190  			changedConf.insert(kv.first);
  191  			const auto base = bases.find(kv.first);
  192  			mPendingBase[kv.first] = base != bases.cend() ? base->second : std::make_pair(false, std::string());
  193  		}
  194  		if (!kept.empty())
  195  			LOG(LogInfo) << "loadSystemConf: " << kept.size() << " change(s) not saved yet are kept for the next save";
  196  	}
  197  	return loaded;
  198  }
  199  
  200  bool SystemConf::loadFromDisk()
  201  {
  202  
  203  	// The record's own temporary, from a build before PL-063 gave every
  204  	// write a temporary of its own, is litter: nothing else writes that name.
  205  	// system.cfg.tmp is not removed any more (PL-064): it is read below, and
  206  	// it is also the name the shell's set_setting writes and renames -- a
  207  	// start that deleted it under a script's write made the script's rename
  208  	// fail and its key vanish. chksysconfig sweeps it at boot, before any
  209  	// script runs.
  210  	std::remove((mSystemConfFile + ".backup.tmp").c_str());
  211  
  212  	// The choice, and a recovery's write-back under the settings lock the
  213  	// save and the shell's set_setting take (audit of the fix round, gpt
  214  	// G2-E-core-02, claude G2-E-core-07): the write-back used to run without
  215  	// it, and a script's write that landed between the choice and the write
  216  	// was lost under it.
  217  	Utils::AtomicFile::RecoveryWrite wrote = Utils::AtomicFile::RecoveryWrite::None;
  218  	const Utils::AtomicFile::LoadedConfig chosen = Utils::AtomicFile::loadUnderLock(mSystemConfFile, sLockPath, sLockBudgetMs, &wrote);
  219  	// No less private than any copy it came from (G-E1-05).
  220  	const int mode = chosen.mode;
  221  	const auto reportWriteBack = [this, wrote](const char* from)
  222  	{
  223  		if (wrote == Utils::AtomicFile::RecoveryWrite::WriteFailed)
  224  			LOG(LogError) << "Unable to write " << mSystemConfFile << " back from " << from;
  225  		else if (wrote == Utils::AtomicFile::RecoveryWrite::LockBusy)
  226  			LOG(LogWarning) << "loadFromDisk: the settings lock was not free within " << sLockBudgetMs << " ms; "
  227  				<< mSystemConfFile << " is read from " << from << " and not written back -- the next save writes it";
  228  	};
  229  
  230  	switch (chosen.source)
  231  	{
  232  	case Utils::AtomicFile::LoadedConfig::Source::Live:
  233  		parseSystemConf(chosen.text);
  234  		// "Usable" for the record means complete too: a file that stops part
  235  		// way through a line is read -- nothing better is there -- but never
  236  		// replaces a whole record (PL-064, PL-065).
  237  		if (chosen.record)
  238  			recordLastGood(chosen.text);
  239  		else
  240  			LOG(LogWarning) << mSystemConfFile << " does not end in a line end -- read as it is, and not recorded as the last known good";
  241  		return true;
  242  
  243  	case Utils::AtomicFile::LoadedConfig::Source::Temporary:
  244  		LOG(LogWarning) << mSystemConfFile << " is cut short or unreadable beside a whole " << mSystemConfFile
  245  			<< ".tmp that an interrupted save left -- loading that and writing it back";
  246  		parseSystemConf(chosen.text);
  247  		reportWriteBack("its .tmp");
  248  		if (wrote != Utils::AtomicFile::RecoveryWrite::LockBusy)
  249  			recordLastGood(chosen.text, mode);
  250  		sRecovered = true;
  251  		return true;
  252  
  253  	case Utils::AtomicFile::LoadedConfig::Source::Backup:
  254  		LOG(LogWarning) << mSystemConfFile << " is missing, empty, unreadable, damaged or cut short of the record -- loading the last-known-good record "
  255  			<< mSystemConfFile << ".backup and writing it back";
  256  		parseSystemConf(chosen.text);
  257  		reportWriteBack("its last-known-good record");
  258  		// The same text: only the record's mode can change, to the one every
  259  		// copy shares, which the live file is written with (claude
  260  		// G2-E-core-04 b: a record an earlier build made 0644 stayed so beside
  261  		// the 0600 file until the next save).
  262  		if (wrote != Utils::AtomicFile::RecoveryWrite::LockBusy)
  263  			recordLastGood(chosen.text, mode);
  264  		sRecovered = true;
  265  		return true;
  266  
  267  	case Utils::AtomicFile::LoadedConfig::Source::Damaged:
  268  		// Unusable by the check, with no whole record and no whole
  269  		// temporary (a record cut short is not taken, PL-018). Read the live file as it always was read -- a file this
  270  		// check is wrong about still works -- and record nothing: there is no
  271  		// good copy to record.
  272  		LOG(LogError) << mSystemConfFile << " has no usable key=*** line and no whole last-known-good record; reading it as it is";
  273  		parseSystemConf(chosen.text);
  274  		mLoadDamaged = true;
  275  		return true;
  276  
  277  	case Utils::AtomicFile::LoadedConfig::Source::Missing:
  278  		break;
  279  	}
  280  
  281  	LOG(LogError) << "Unable to open " << mSystemConfFile;
  282  	return false;
  283  }
  284  
  285  bool SystemConf::saveSystemConf()
  286  {
  287  	if (mSystemConfFile.empty())
  288  		return Settings::getInstance()->saveFile();	
  289  
  290  	if (changedConf.empty())
  291  		return false;
  292  
  293  	// The shell's settings lock (wait_lock in profile.d/001-functions), held
  294  	// across the read-modify-write: set_setting reads the file, writes a
  295  	// temporary and renames it under the same lock, and a save that read or
  296  	// renamed beside it put one writer's snapshot over the other's. Five
  297  	// seconds is the budget, on the interface thread. A live holder still on
  298  	// the lock past it is logged and nothing is written (PL-024): this used to
  299  	// save anyway, and lost either the script's key or the player's. The
  300  	// changes stay in changedConf, and the next save -- any page closing,
  301  	// any set-and-save -- writes them over whatever the script left.
  302  	std::string out;
  303  	bool baseWhole = true;
  304  	const Utils::AtomicFile::LockedSave saved = Utils::AtomicFile::saveUnderLock(mSystemConfFile, sLockPath, sLockBudgetMs,
  305  		[this](const std::string& current) { return applyChanges(current); }, &out, &baseWhole);
  306  
  307  	switch (saved)
  308  	{
  309  	case Utils::AtomicFile::LockedSave::LockBusy:
  310  		LOG(LogWarning) << "saveSystemConf: the settings lock was not free within 5s; nothing written -- the changes are kept for the next save";
  311  		return false;
  312  	case Utils::AtomicFile::LockedSave::Unreadable:
  313  		LOG(LogError) << "Unable to open for saving :  " << mSystemConfFile << " -- the changes are kept for the next save";
  314  		return false;
  315  	case Utils::AtomicFile::LockedSave::WriteFailed:
  316  		// Written to a temporary of its own, synced, and renamed over the
  317  		// live file (D-CLOUD-079, PL-063); a failure leaves the file whole.
  318  		LOG(LogError) << "Unable to write " << mSystemConfFile << " -- the changes are kept for the next save";
  319  		return false;
  320  	case Utils::AtomicFile::LockedSave::Written:
  321  		break;
  322  	}
  323  
  324  	changedConf.clear();
  325  	mPendingBase.clear();
  326  	// The file is now what this save wrote: the base the next change is
  327  	// compared with (G2-E-core-07).
  328  	mOnDisk = Utils::AtomicFile::parseKeyValues(out);
  329  
  330  	// What was just written is, by construction, the newest good state, so
  331  	// it becomes the record (D-CLOUD-078: a success becomes the last known
  332  	// good). recordLastGood reacquires the lock and revalidates that snapshot;
  333  	// a script may have published a newer state since this save released it.
  334  	// Unless it was merged onto a file cut short: the record then keeps the
  335  	// keys the cut lost (audit of the fixes G-E1-04).
  336  	if (baseWhole)
  337  		recordLastGood(out);
  338  	else
  339  		LOG(LogWarning) << "saveSystemConf: " << mSystemConfFile << " was cut short when this save read it -- written, and not recorded as the last known good";
  340  
  341  	return true;
  342  }
  343  
  344  // This save's keys, applied to the file as it is on disk now (read under
  345  // the lock): a key already there is rewritten in place, or removed when it
  346  // went back to its default or to nothing; a new one goes at the end. Every
  347  // other line is left exactly as the file had it -- the shell's writes
  348  // included.
  349  std::string SystemConf::applyChanges(const std::string& current)
  350  {
  351  	/* Read all lines in a vector */
  352  	std::vector<std::string> fileLines;
  353  	std::string line;
  354  
  355  	std::istringstream filein(current);
  356  	while (std::getline(filein, line))
  357  		fileLines.push_back(line);
  358  
  359  	static std::string removeID = "$^�(p$^mpv$�rpver$^vper$vper$^vper$vper$vper$^vperv^pervncvizn";
  360  
  361  	int lastTime = SDL_GetTicks();
  362  
  363  	/* Save new value if exists */
  364  	for (auto& it : changedConf)
  365  	{
  366  		std::string key = it + "=";
  367  		char key0 = key[0];
  368  
  369  		bool lineFound = false;
  370  
  371  		for (auto& currentLine : fileLines)
  372  		{
  373  			if (currentLine.size() < 3)
  374  				continue;
  375  
  376  			char fc = currentLine[0];
  377  			if (fc != key0 && currentLine[1] != key0)
  378  				continue;
  379  
  380  			int idx = currentLine.find(key);
  381  			if (idx == std::string::npos)
  382  				continue;
  383  
  384  			if (idx == 0 || (idx == 1 && (fc == ';' || fc == '#')))
  385  			{
  386  				std::string val = confMap[it];
  387  				if ((!val.empty() && val != "auto" && val != "default") || dontRemoveValue.find(it) != dontRemoveValue.cend())
  388  				{
  389  					auto defaultValue = defaults.find(key);
  390  					if (defaultValue != defaults.cend() && defaultValue->second == val)
  391  						currentLine = removeID;
  392  					else
  393  						currentLine = key + val;
  394  				}
  395  				else 
  396  					currentLine = removeID;
  397  
  398  				lineFound = true;
  399  			}
  400  		}
  401  
  402  		if (!lineFound)
  403  		{
  404  			std::string val = confMap[it];
  405  			if (!val.empty() && val != "auto")
  406  				fileLines.push_back(key + val);
  407  		}
  408  	}
  409  
  410  	lastTime = SDL_GetTicks() - lastTime;
  411  
  412  	LOG(LogDebug) << "saveSystemConf :  " << lastTime;
  413  
  414  	std::string out;
  415  	for (int i = 0; i < fileLines.size(); i++) 
  416  	{
  417  		if (fileLines[i] != removeID)
  418  			out += fileLines[i] + "\n";
  419  	}
  420  	return out;
  421  }
  422  
  423  std::string SystemConf::get(const std::string &name) 
  424  {
  425  	if (mSystemConfFile.empty())
  426  		return Settings::getInstance()->getString(mapSettingsName(name));
  427  	
  428  	auto it = confMap.find(name);
  429  	if (it != confMap.cend())
  430  		return it->second;
  431  
  432  	auto dit = defaults.find(name);
  433  	if (dit != defaults.cend())
  434  		return dit->second;
  435  
  436      return "";
  437  }
  438  
  439  bool SystemConf::set(const std::string &name, const std::string &value) 
  440  {
  441  	if (mSystemConfFile.empty())
  442  		return Settings::getInstance()->setString(mapSettingsName(name), value == "auto" ? "" : value);
  443  
  444  	if (confMap.count(name) == 0 || confMap[name] != value)
  445  	{
  446  		// What the key held before this run of changes, once: a reload
  447  		// compares it with the file (G-E1-03). Held in the file, as last
  448  		// read or written -- not in confMap, which keeps keys the file no
  449  		// longer has: one another writer removed, one the last save wrote
  450  		// away. The reload found such a key missing where the base said it
  451  		// was, and dropped the change as removed by somebody since (audit of
  452  		// the fix round, gpt G2-E-core-07, claude G2-E-core-09).
  453  		if (changedConf.find(name) == changedConf.cend())
  454  		{
  455  			const auto it = mOnDisk.find(name);
  456  			mPendingBase[name] = it == mOnDisk.cend() ? std::make_pair(false, std::string()) : std::make_pair(true, it->second);
  457  		}
  458  		confMap[name] = value;
  459  		changedConf.insert(name);
  460  		return true;
  461  	}
  462  
  463  	return false;
  464  }
  465  
  466  bool SystemConf::getBool(const std::string &name, bool defaultValue)
  467  {
  468  	if (mSystemConfFile.empty())
  469  		return Settings::getInstance()->getBool(mapSettingsName(name));
  470  
  471  	if (defaultValue)
  472  		return get(name) != "0";
  473  
  474  	return get(name) == "1";
  475  }
  476  
  477  bool SystemConf::setBool(const std::string &name, bool value)
  478  {
  479  	if (mSystemConfFile.empty())
  480  		return Settings::getInstance()->setBool(mapSettingsName(name), value);
  481  
  482  	return set(name, value  ? "1" : "0");
  483  }
  484  
  485  bool SystemConf::getIncrementalSaveStates()
  486  {
  487  	auto valGSS = SystemConf::getInstance()->get("global.incrementalsavestates");
  488  	return valGSS != "0" && valGSS != "2";
  489  }
  490  
  491  bool SystemConf::getIncrementalSaveStatesUseCurrentSlot()
  492  {
  493  	return SystemConf::getInstance()->get("global.incrementalsavestates") == "2";
  494  }
```


## es-core/src/Settings.cpp @ 16dbac5211: lines 1-28 (excerpt of 723)

```text
    1  #include "Settings.h"
    2  
    3  #include "utils/FileSystemUtil.h"
    4  #include "Log.h"
    5  #include "Scripting.h"
    6  #include "utils/Platform.h"
    7  #include <pugixml/src/pugixml.hpp>
    8  #include <algorithm>
    9  #include <cstdio>
   10  #include <vector>
   11  #include "utils/StringUtil.h"
   12  #include "utils/AtomicFileUtil.h"
   13  #include "Paths.h"
   14  
   15  Settings* Settings::sInstance = NULL;
   16  bool Settings::sRecovered = false;
   17  static std::string mEmptyString = "";
   18  Delegate<ISettingsChangedEvent> Settings::settingChanged;
   19  
   20  IMPLEMENT_STATIC_BOOL_SETTING(DebugText, false)
   21  IMPLEMENT_STATIC_BOOL_SETTING(DebugImage, false)
   22  IMPLEMENT_STATIC_BOOL_SETTING(DebugGrid, false)
   23  IMPLEMENT_STATIC_BOOL_SETTING(DebugMouse, false)
   24  IMPLEMENT_STATIC_BOOL_SETTING(ShowControllerActivity, true)
   25  IMPLEMENT_STATIC_BOOL_SETTING(ShowControllerBattery, true)
   26  IMPLEMENT_STATIC_BOOL_SETTING(DrawClock, true)
   27  IMPLEMENT_STATIC_BOOL_SETTING(ClockMode12, false)
   28  IMPLEMENT_STATIC_BOOL_SETTING(DrawFramerate, false)
```


## es-core/src/Settings.cpp @ 16dbac5211: lines 76-138 (excerpt of 723)

```text
   76  			if (mHiddenSystems.find(hiddenSystem) == mHiddenSystems.cend())
   77  				mHiddenSystems.insert(hiddenSystem);
   78  	}
   79  
   80  	if (mLoaded)
   81  		settingChanged.invoke([name](ISettingsChangedEvent* c) { c->onSettingChanged(name); });
   82  }
   83  
   84  // these values are NOT saved to es_settings.xml
   85  // since they're set through command-line arguments, and not the in-program settings menu
   86  std::vector<const char*> settings_dont_save {
   87  	{ "Debug" },
   88  	{ "DebugText" },
   89  	{ "DebugImage" },
   90  	{ "DebugGrid" },
   91  	{ "DebugMouse" },
   92  	{ "ForceKid" },
   93  	{ "ForceKiosk" },
   94  	{ "IgnoreGamelist" },
   95  	{ "HideConsole" },
   96  	{ "ShowExit" },
   97  	{ "ExitOnRebootRequired" },
   98  	{ "AlternateSplashScreen" },
   99  	{ "SplashScreen" },
  100  	{ "SplashScreenProgress" },
  101  	// { "VSync" },
  102  	{ "FullscreenBorderless" },
  103  	{ "Windowed" },
  104  	{ "WindowWidth" },
  105  	{ "WindowHeight" },
  106  	{ "ScreenWidth" },
  107  	{ "ScreenHeight" },
  108  	{ "ScreenOffsetX" },
  109  	{ "ScreenOffsetY" },
  110  	{ "ScreenRotate" },
  111  	{ "MonitorID" },
  112  	{ "PackGamelists" },
  113  	{ "BuildMultiDiskContentCache" }
  114  };
  115  
  116  Settings::Settings() : mLoaded(false)
  117  {
  118  	setDefaults();
  119  	loadFile();
  120  	mLoaded = true;
  121  }
  122  
  123  Settings* Settings::getInstance()
  124  {
  125  	if(sInstance == NULL)
  126  		sInstance = new Settings();
  127  
  128  	return sInstance;
  129  }
  130  
  131  void Settings::setDefaults()
  132  {
  133  	mWasChanged = false;
  134  	mBoolMap.clear();
  135  	mIntMap.clear();
  136  
  137  	mBoolMap["BackgroundJoystickInput"] = false;
  138  	mBoolMap["ParseGamelistOnly"] = false;
```


## es-core/src/Settings.cpp @ 16dbac5211: lines 187-218 (excerpt of 723)

```text
  187  	mStringMap["FolderViewMode"] = "always";
  188  	mStringMap["HiddenSystems"] = "";
  189  
  190  	mBoolMap["PublicWebAccess"] = false;	
  191  	mBoolMap["FirstJoystickOnly"] = false;
  192      mBoolMap["EnableSounds"] = false;
  193  	mBoolMap["ShowHelpPrompts"] = true;
  194  	mBoolMap["ScrapeRatings"] = true;
  195  	mBoolMap["ScrapeNames"] = true;	
  196  	mBoolMap["ScrapeDescription"] = true;
  197  	mBoolMap["ScrapePadToKey"] = false;
  198  	mBoolMap["ScrapeOverWrite"] = true;	
  199  	mBoolMap["ScrapeManual"] = true;
  200  	mBoolMap["ScrapeMap"] = true;
  201  	mBoolMap["IgnoreGamelist"] = false;
  202  	mBoolMap["HideConsole"] = true;
  203  	mBoolMap["QuickSystemSelect"] = true;
  204  	mBoolMap["MoveCarousel"] = true;
  205  	mBoolMap["SaveGamelistsOnExit"] = true;
  206  	mStringMap["ShowBattery"] = "text";
  207  	mBoolMap["CheckBiosesAtLaunch"] = false;
  208  	mBoolMap["RemoveMultiDiskContent"] = true;
  209  	mBoolMap["PackGamelists"] = false;
  210  	mBoolMap["BuildMultiDiskContentCache"] = false;	
  211  
  212  	mBoolMap["ShowNetworkIndicator"] = Settings::_ShowNetworkIndicator;
  213  
  214  	mBoolMap["Debug"] = false;
  215  
  216  	mBoolMap["InvertButtons"] = true;
  217  
  218  	mBoolMap["GameOptionsAtNorth"] = true;
```


## es-core/src/Settings.cpp @ 16dbac5211: lines 383-403 (excerpt of 723)

```text
  383  	mIntMap["ScreenHeight"]  = 0;
  384  	mIntMap["ScreenOffsetX"] = 0;
  385  	mIntMap["ScreenOffsetY"] = 0;
  386  	mIntMap["ScreenRotate"]  = 0;
  387  
  388  	mStringMap["INPUT P1NAME"] = "DEFAULT";
  389  	mStringMap["INPUT P2NAME"] = "DEFAULT";
  390  	mStringMap["INPUT P3NAME"] = "DEFAULT";
  391  	mStringMap["INPUT P4NAME"] = "DEFAULT";
  392  	mStringMap["INPUT P5NAME"] = "DEFAULT";
  393  	mStringMap["INPUT P6NAME"] = "DEFAULT";
  394  	mStringMap["INPUT P7NAME"] = "DEFAULT";
  395  	mStringMap["INPUT P8NAME"] = "DEFAULT";
  396  
  397  #ifdef BATOCERA
  398  	mStringMap["HOTKEY_CONTROLCENTER"] = "a";
  399  #endif
  400  
  401  	// Audio settings
  402  	mBoolMap["audio.bgmusic"] = Settings::_BackgroundMusic;
  403  	mBoolMap["audio.persystem"] = false;
```


## es-core/src/Settings.cpp @ 16dbac5211: lines 439-723 (excerpt of 723)

```text
  439  	mBoolMap["DisableTouchscreen"] = false;
  440  
  441  	mDefaultBoolMap = mBoolMap;
  442  	mDefaultIntMap = mIntMap;
  443  	mDefaultFloatMap = mFloatMap;
  444  	mDefaultStringMap = mStringMap;
  445  }
  446  
  447  template <typename K, typename V>
  448  void saveMap(pugi::xml_node &node, std::map<K, V>& map, const char* type, std::map<K, V>& defaultMap, V defaultValue)
  449  {
  450  	for(auto iter = map.cbegin(); iter != map.cend(); iter++)
  451  	{
  452  		// key is on the "don't save" list, so don't save it
  453  		if(std::find(settings_dont_save.cbegin(), settings_dont_save.cend(), iter->first) != settings_dont_save.cend())
  454  			continue;
  455  
  456  		auto def = defaultMap.find(iter->first);
  457  		if (def != defaultMap.cend() && def->second == iter->second)
  458  			continue;
  459  
  460  		if (def == defaultMap.cend() && iter->second == defaultValue)
  461  			continue;
  462  
  463  		pugi::xml_node parent_node= node.append_child(type);
  464  		parent_node.append_attribute("name").set_value(iter->first.c_str());
  465  		parent_node.append_attribute("value").set_value(iter->second);
  466  	}
  467  }
  468  
  469  bool Settings::saveFile()
  470  {
  471  	if (!mWasChanged)
  472  		return false;
  473  
  474  	mWasChanged = false;
  475  
  476  	LOG(LogDebug) << "Settings::saveFile() : Saving Settings to file.";
  477  
  478  	const std::string path = Paths::getUserEmulationStationPath() + "/es_settings.cfg";
  479  
  480  	pugi::xml_document doc;
  481  
  482  	pugi::xml_node config = doc.append_child("config"); // root element
  483  
  484  	saveMap<std::string, bool>(config, mBoolMap, "bool", mDefaultBoolMap, false);
  485  	saveMap<std::string, int>(config, mIntMap, "int", mDefaultIntMap, 0);
  486  	saveMap<std::string, float>(config, mFloatMap, "float", mDefaultFloatMap, 0);
  487  
  488  	//saveMap<std::string, std::string>(config, mStringMap, "string");
  489  	for(auto iter = mStringMap.cbegin(); iter != mStringMap.cend(); iter++)
  490  	{
  491  		// key is on the "don't save" list, so don't save it
  492  		if (std::find(settings_dont_save.cbegin(), settings_dont_save.cend(), iter->first) != settings_dont_save.cend())
  493  			continue;
  494  
  495  		// Value is not known, and empty, don't save it
  496  		auto def = mDefaultStringMap.find(iter->first);
  497  		if (def == mDefaultStringMap.cend() && iter->second.empty())
  498  			continue;
  499  
  500  		// Value is know and has default value, don't save it
  501  		if (def != mDefaultStringMap.cend() && def->second == iter->second)
  502  			continue;
  503  
  504  		pugi::xml_node node = config.append_child("string");
  505  		node.append_attribute("name").set_value(iter->first.c_str());
  506  		node.append_attribute("value").set_value(iter->second.c_str());
  507  	}
  508  
  509  	// Serialised once, then written through a temporary and a rename
  510  	// (D-CLOUD-079): save_file opened the live path for writing, which
  511  	// truncates it, and a process killed before the write completed -- or a
  512  	// battery gone at that instant -- left an empty es_settings.cfg that the
  513  	// next start read as "no settings" and the next save made permanent.
  514  	// The same bytes go to the last-known-good record, because what was just
  515  	// written is, by construction, the newest good state (D-CLOUD-078).
  516  	struct StringWriter : pugi::xml_writer
  517  	{
  518  		std::string out;
  519  		void write(const void* data, size_t size) override { out.append((const char*) data, size); }
  520  	};
  521  	StringWriter writer;
  522  	doc.save(writer);
  523  
  524  	if (!Utils::AtomicFile::writeText(path, writer.out))
  525  	{
  526  		// Kept dirty, so the next save tries again rather than believing this
  527  		// one happened.
  528  		LOG(LogError) << "Settings::saveFile() : could not write " << path << "; the changes are kept for the next save";
  529  		mWasChanged = true;
  530  		return false;
  531  	}
  532  	// The record is made no less private than the live file (#308 F-ES-08).
  533  	if (!Utils::AtomicFile::writeText(path + ".backup", writer.out, Utils::AtomicFile::modeOf(path, 0644)))
  534  		LOG(LogWarning) << "Settings::saveFile() : could not write the last-known-good record " << path << ".backup";
  535  
  536  	Scripting::fireEvent("config-changed");
  537  	Scripting::fireEvent("settings-changed");
  538  
  539  	return true;
  540  }
  541  
  542  // Read the live file if it parses; else the last-known-good record beside it
  543  // (es_settings.cfg.backup), which then goes back as the live file; else
  544  // nothing -- the defaults stand and nothing is written over the file that
  545  // failed, so a start that found it damaged and a record that was missing
  546  // leaves both for somebody to look at (D-CLOUD-078, D-CLOUD-079). An empty
  547  // file is a parse failure here: pugixml reports no document element, which
  548  // is exactly what a write cut short leaves behind.
  549  void Settings::loadFile()
  550  {
  551  	const std::string path = Paths::getUserEmulationStationPath() + "/es_settings.cfg";
  552  	const std::string backup = path + ".backup";
  553  
  554  	// A temporary left by a save that never reached its rename is litter,
  555  	// not a record: nothing reads it, and the next save replaces it. The
  556  	// record's own temporary likewise.
  557  	std::remove((path + ".tmp").c_str());
  558  	std::remove((path + ".backup.tmp").c_str());
  559  
  560  	pugi::xml_document doc;
  561  	bool loaded = false;
  562  	bool fromBackup = false;
  563  	const bool liveExists = Utils::FileSystem::exists(path);
  564  	if (liveExists)
  565  	{
  566  		pugi::xml_parse_result result = doc.load_file(WINSTRINGW(path).c_str());
  567  		loaded = (bool) result;
  568  		if (!loaded)
  569  			LOG(LogError) << "Could not parse Settings file!\n   " << result.description();
  570  	}
  571  	if (!loaded && Utils::FileSystem::exists(backup))
  572  	{
  573  		doc.reset();
  574  		pugi::xml_parse_result result = doc.load_file(WINSTRINGW(backup).c_str());
  575  		if (result)
  576  		{
  577  			loaded = true;
  578  			fromBackup = true;
  579  			LOG(LogWarning) << path << " is " << (liveExists ? "damaged" : "missing")
  580  				<< " -- loading the last-known-good record " << backup << " and writing it back";
  581  		}
  582  		else
  583  			LOG(LogError) << "Could not parse the last-known-good record " << backup << "!\n   " << result.description();
  584  	}
  585  	if (!loaded)
  586  		return;
  587  
  588  	pugi::xml_node root = doc;
  589  
  590  	pugi::xml_node config = doc.child("config");
  591  	if (config)
  592  		root = config;
  593  
  594  	for(pugi::xml_node node = root.child("bool"); node; node = node.next_sibling("bool"))
  595  		setBool(node.attribute("name").as_string(), node.attribute("value").as_bool());
  596  	for(pugi::xml_node node = root.child("int"); node; node = node.next_sibling("int"))
  597  		setInt(node.attribute("name").as_string(), node.attribute("value").as_int());
  598  	for(pugi::xml_node node = root.child("float"); node; node = node.next_sibling("float"))
  599  		setFloat(node.attribute("name").as_string(), node.attribute("value").as_float());
  600  	for(pugi::xml_node node = root.child("string"); node; node = node.next_sibling("string"))
  601  		setString(node.attribute("name").as_string(), node.attribute("value").as_string());
  602  	
  603  	// Migrate old preferences
  604  	auto it = mBoolMap.find("UseCustomCollectionsSystem");
  605  	if (it != mBoolMap.cend())
  606  	{
  607  		if (it->second == false)
  608  			mStringMap["UseCustomCollectionsSystemEx"] = "false";
  609  
  610  		mBoolMap.erase(it);
  611  	}
  612  
  613  	mWasChanged = false;
  614  
  615  	if (fromBackup)
  616  	{
  617  		if (!Utils::AtomicFile::copy(backup, path))
  618  			LOG(LogError) << "Could not write " << path << " back from its last-known-good record";
  619  		sRecovered = true;
  620  	}
  621  	else
  622  	{
  623  		// The file that just parsed is the last known good: record it, and
  624  		// only when the record would change -- this runs at every start.
  625  		bool ok = false;
  626  		const std::string live = Utils::AtomicFile::readText(path, &ok);
  627  		// No less private than the live file, and rewritten for its mode
  628  		// alone where an earlier build made it wider (#308 F-ES-08).
  629  		const int mode = Utils::AtomicFile::modeOf(path, 0644);
  630  		if (ok && (live != Utils::AtomicFile::readText(backup) || Utils::AtomicFile::modeOf(backup, mode) != mode)
  631  			&& !Utils::AtomicFile::writeText(backup, live, mode))
  632  			LOG(LogWarning) << "Could not write the last-known-good record " << backup;
  633  	}
  634  }
  635  
  636  //Print a warning message if the setting we're trying to get doesn't already exist in the map, then return the value in the map.
  637  #define SETTINGS_GETSET(type, mapName, getMethodName, setMethodName, defaultValue) type Settings::getMethodName(const std::string& name) \
  638  { \
  639  	auto it = mapName.find(name); \
  640  	if (it == mapName.cend()) \
  641  		return defaultValue; \
  642  \
  643  	return it->second; \
  644  } \
  645  bool Settings::setMethodName(const std::string& name, type value) \
  646  { \
  647  	if (mapName.count(name) == 0 || mapName[name] != value) { \
  648  		mapName[name] = value; \
  649  		if (std::find(settings_dont_save.cbegin(), settings_dont_save.cend(), name) == settings_dont_save.cend()) \
  650  			mWasChanged = true; \
  651  		updateCachedSetting(name); \
  652  		return true; \
  653  	} \
  654  	return false; \
  655  }
  656  
  657  SETTINGS_GETSET(bool, mBoolMap, getBool, setBool, false);
  658  SETTINGS_GETSET(int, mIntMap, getInt, setInt, 0);
  659  SETTINGS_GETSET(float, mFloatMap, getFloat, setFloat, 0.0f);
  660  
  661  std::string Settings::getString(const std::string& name)
  662  {
  663  	auto it = mStringMap.find(name);
  664  	if (it == mStringMap.cend())
  665  		return mEmptyString;
  666  
  667  	return it->second;
  668  }
  669  
  670  bool Settings::setString(const std::string& name, const std::string& value)
  671  {
  672  	if (mStringMap.count(name) == 0 || mStringMap[name] != value)
  673  	{
  674  		if (value == "" && mStringMap.count(name) == 0)
  675  			return false;
  676  
  677  		mStringMap[name] = value;
  678  
  679  		if (std::find(settings_dont_save.cbegin(), settings_dont_save.cend(), name) == settings_dont_save.cend())
  680  			mWasChanged = true;
  681  
  682  		updateCachedSetting(name);
  683  		return true;
  684  	}
  685  
  686  	return false;
  687  }
  688  
  689  SettingType Settings::getSettingType(const std::string& name)
  690  {
  691  	if (mStringMap.find(name) != mStringMap.cend())
  692  		return SettingType::String;
  693  
  694  	if (mBoolMap.find(name) != mBoolMap.cend())
  695  		return SettingType::Bool;
  696  
  697  	if (mIntMap.find(name) != mIntMap.cend())
  698  		return SettingType::Int;
  699  
  700  	if (mFloatMap.find(name) != mFloatMap.cend())
  701  		return SettingType::Float;
  702  
  703  	return SettingType::Unknown;
  704  }
  705  
  706  std::vector<std::string> Settings::getSettingsNames()
  707  {
  708  	std::vector<std::string> ret;
  709  	
  710  	for (auto item : mStringMap)
  711  		ret.push_back(item.first);
  712  
  713  	for (auto item : mBoolMap)
  714  		ret.push_back(item.first);
  715  
  716  	for (auto item : mIntMap)
  717  		ret.push_back(item.first);
  718  
  719  	for (auto item : mFloatMap)
  720  		ret.push_back(item.first);
  721  
  722  	return ret;
  723  }
```


## es-core/src/HttpReq.cpp @ 16dbac5211: lines 1-38 (excerpt of 644)

```text
    1  #include "HttpReq.h"
    2  
    3  #include "utils/FileSystemUtil.h"
    4  #include "utils/StringUtil.h"
    5  #include "Log.h"
    6  #include <assert.h>
    7  #include <thread>
    8  
    9  #include <SDL.h>
   10  #include "Paths.h"
   11  
   12  #ifdef WIN32
   13  #include <time.h>
   14  #else
   15  #include <unistd.h>
   16  #endif
   17  
   18  #include <mutex>
   19  static std::mutex mMutex;
   20  
   21  CURLM* HttpReq::s_multi_handle = curl_multi_init();
   22  
   23  std::map<CURL*, HttpReq*> HttpReq::s_requests;
   24  
   25  std::string HttpReq::urlEncode(const std::string &s)
   26  {
   27      const std::string unreserved = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~";
   28  
   29      std::string escaped="";
   30      for(size_t i=0; i<s.length(); i++)
   31      {
   32          if (unreserved.find_first_of(s[i]) != std::string::npos)
   33          {
   34              escaped.push_back(s[i]);
   35          }
   36          else
   37          {
   38              escaped.append("%");
```


## es-core/src/HttpReq.cpp @ 16dbac5211: lines 88-644 (excerpt of 644)

```text
   88  		if (nRet == ERROR_SUCCESS)
   89  			ret = szBuffer;
   90  	}
   91  
   92  	return ret;
   93  }
   94  #endif
   95  
   96  static std::string getCookiesContainerPath(bool createDirectory = true)
   97  {	
   98  	std::string cookiesPath = Utils::FileSystem::getGenericPath(Paths::getUserEmulationStationPath() + std::string("/tmp"));
   99  	if (createDirectory)
  100  		Utils::FileSystem::createDirectory(cookiesPath);
  101  
  102  	return Utils::FileSystem::getGenericPath(Utils::FileSystem::combine(cookiesPath, "cookies.txt"));
  103  }
  104  
  105  void HttpReq::resetCookies()
  106  {
  107  	auto path = getCookiesContainerPath(false);
  108  	Utils::FileSystem::removeFile(path);
  109  }
  110  
  111  HttpReq::HttpReq(const std::string& url, const std::string& outputFilename) 
  112  	: mStatus(REQ_IN_PROGRESS), mHandle(NULL), mFile(NULL)
  113  {
  114  	HttpReqOptions options;
  115  	options.outputFilename = outputFilename;	
  116  	performRequest(url, &options);
  117  }
  118  
  119  HttpReq::HttpReq(const std::string& url, HttpReqOptions* options)
  120  	: mStatus(REQ_IN_PROGRESS), mHandle(NULL), mFile(NULL)
  121  {
  122  	performRequest(url, options);
  123  }
  124  
  125  void HttpReq::performRequest(const std::string& url, HttpReqOptions* options)
  126  {
  127  	mUrl = url;
  128  
  129  	std::string outputFilename;
  130  
  131  	if (options != nullptr && !options->outputFilename.empty())
  132  		outputFilename = options->outputFilename;
  133  
  134  	mFilePath = outputFilename;
  135  	mPosition = -1;
  136  	mPercent = -1;	
  137  	mHandle = curl_easy_init();
  138  
  139  	if(mHandle == NULL)
  140  	{
  141  		mStatus = REQ_IO_ERROR;
  142  		onError("curl_easy_init failed");
  143  		return;
  144  	}
  145  
  146  	//set the url
  147  	CURLcode err = curl_easy_setopt(mHandle, CURLOPT_URL, url.c_str());
  148  	if(err != CURLE_OK)
  149  	{
  150  		mStatus = REQ_IO_ERROR;
  151  		onError(curl_easy_strerror(err));
  152  		return;
  153  	}
  154  
  155  #ifndef WIN32
  156  	err = curl_easy_setopt(mHandle, CURLOPT_BUFFERSIZE, 102400L); // Batocera - 100kB instead of 16
  157  	if(err != CURLE_OK)
  158  	{
  159  		mStatus = REQ_IO_ERROR;
  160  		onError(curl_easy_strerror(err));
  161  		return;
  162  	}
  163  #endif
  164  
  165  	if (options != nullptr && !options->dataToPost.empty())
  166  	{
  167  		curl_easy_setopt(mHandle, CURLOPT_POST, 1L);
  168  		curl_easy_setopt(mHandle, CURLOPT_POSTFIELDSIZE, options->dataToPost.length());
  169  		curl_easy_setopt(mHandle, CURLOPT_COPYPOSTFIELDS, options->dataToPost.c_str());
  170  	}
  171  
  172  	if (options != nullptr && options->customHeaders.size() > 0)
  173  	{
  174  		struct curl_slist *hs = nullptr;
  175  
  176  		for (auto header : options->customHeaders)
  177  			hs = curl_slist_append(hs, header.c_str());
  178  
  179  		curl_easy_setopt(mHandle, CURLOPT_HTTPHEADER, hs);
  180  	}
  181  
  182  	//set curl to handle redirects
  183  	err = curl_easy_setopt(mHandle, CURLOPT_FOLLOWLOCATION, 1L);
  184  	if(err != CURLE_OK)
  185  	{
  186  		mStatus = REQ_IO_ERROR;
  187  		onError(curl_easy_strerror(err));
  188  		return;
  189  	}
  190  
  191  	// Ignore expired SSL certificates
  192  	curl_easy_setopt(mHandle, CURLOPT_SSL_VERIFYPEER, 0L);
  193  
  194  	// Add client cert support
  195  	if (options != nullptr && !options->clientCert.empty() && !options->clientKey.empty()) {
  196  		// curl_easy_setopt(mHandle, CURLOPT_VERBOSE, 1L);
  197  		curl_easy_setopt(mHandle, CURLOPT_SSLCERT, options->clientCert.c_str());
  198  		curl_easy_setopt(mHandle, CURLOPT_SSLCERTTYPE, "PEM");
  199  		curl_easy_setopt(mHandle, CURLOPT_SSLKEY, options->clientKey.c_str());
  200  		curl_easy_setopt(mHandle, CURLOPT_SSL_VERIFYHOST, 0L);
  201  	}
  202  
  203  	//set curl to connection timeout
  204  	err = curl_easy_setopt(mHandle, CURLOPT_CONNECTTIMEOUT_MS, options != nullptr ? options->connectTimeout : 10000L);
  205  	if (err == CURLE_OK && options != nullptr && options->timeout > 0)
  206  		err = curl_easy_setopt(mHandle, CURLOPT_TIMEOUT_MS, options->timeout);
  207  	// A transfer under one byte a second for stallTimeout seconds ends with
  208  	// CURLE_OPERATION_TIMEDOUT: the bound for a request that may be long but
  209  	// never silent (ROCKNIX fork #299).
  210  	if (err == CURLE_OK && options != nullptr && options->stallTimeout > 0)
  211  		err = curl_easy_setopt(mHandle, CURLOPT_LOW_SPEED_LIMIT, 1L);
  212  	if (err == CURLE_OK && options != nullptr && options->stallTimeout > 0)
  213  		err = curl_easy_setopt(mHandle, CURLOPT_LOW_SPEED_TIME, options->stallTimeout);
  214  	if (err != CURLE_OK)
  215  	{
  216  		mStatus = REQ_IO_ERROR;
  217  		onError(curl_easy_strerror(err));
  218  		return;
  219  	}
  220  		
  221  	//set curl max redirects
  222  	err = curl_easy_setopt(mHandle, CURLOPT_MAXREDIRS, 2L);
  223  	if(err != CURLE_OK)
  224  	{
  225  		mStatus = REQ_IO_ERROR;
  226  		onError(curl_easy_strerror(err));
  227  		return;
  228  	}
  229  
  230  	// set curl restrict redirect protocols
  231  #if WIN32
  232  	curl_version_info_data* version_info = curl_version_info(CURLVERSION_NOW);
  233  
  234  	unsigned int major, minor, patch;
  235  	if (version_info && sscanf(version_info->version, "%u.%u.%u", &major, &minor, &patch) == 3)
  236  		err = curl_easy_setopt(mHandle, CURLOPT_REDIR_PROTOCOLS_STR, "http,https");
  237  	else 
  238  		err = curl_easy_setopt(mHandle, CURLOPT_REDIR_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS);
  239  #elif CURL_AT_LEAST_VERSION(7,85,0)
  240  	err = curl_easy_setopt(mHandle, CURLOPT_REDIR_PROTOCOLS_STR, "http,https");	
  241  #else
  242  	err = curl_easy_setopt(mHandle, CURLOPT_REDIR_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS);
  243  #endif
  244  
  245  	if(err != CURLE_OK)
  246  	{
  247  		mStatus = REQ_IO_ERROR;
  248  		onError(curl_easy_strerror(err));
  249  		return;
  250  	}
  251  
  252  	//tell curl how to write the data
  253  	err = curl_easy_setopt(mHandle, CURLOPT_WRITEFUNCTION, &HttpReq::write_content);
  254  	if(err != CURLE_OK)
  255  	{
  256  		mStatus = REQ_IO_ERROR;
  257  		onError(curl_easy_strerror(err));
  258  		return;
  259  	}
  260  
  261  	//give curl a pointer to this HttpReq so we know where to write the data *to* in our write function
  262  	err = curl_easy_setopt(mHandle, CURLOPT_WRITEDATA, this);
  263  	if(err != CURLE_OK)
  264  	{
  265  		mStatus = REQ_IO_ERROR;
  266  		onError(curl_easy_strerror(err));
  267  		return;
  268  	}
  269  
  270  	// Set user agent
  271  	std::string userAgent = options ? options->userAgent : HTTP_REQ_USERAGENT;
  272  	if (!userAgent.empty())
  273  	{
  274  		err = curl_easy_setopt(mHandle, CURLOPT_USERAGENT, userAgent.c_str());
  275  		if (err != CURLE_OK)
  276  		{
  277  			mStatus = REQ_IO_ERROR;
  278  			onError(curl_easy_strerror(err));
  279  			return;
  280  		}
  281  	}
  282  
  283  	if (options == nullptr || options->useCookieManager)
  284  	{
  285  		std::string cookiesFile = getCookiesContainerPath(); 
  286  
  287  		curl_easy_setopt(mHandle, CURLOPT_COOKIEFILE, cookiesFile.c_str());
  288  		curl_easy_setopt(mHandle, CURLOPT_COOKIEJAR, cookiesFile.c_str());
  289  	}
  290  
  291  	curl_easy_setopt(mHandle, CURLOPT_HEADERFUNCTION, &HttpReq::header_callback);
  292  	curl_easy_setopt(mHandle, CURLOPT_HEADERDATA, this);
  293  
  294  #ifdef WIN32
  295  	// Setup system proxy on Windows if required
  296  	if (_regGetDWORD(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", "ProxyEnable"))
  297  	{
  298  		auto proxyServer = _regGetString(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", "ProxyServer");
  299  		if (!proxyServer.empty())
  300  		{
  301  			std::string protocol = (url.find("https:/") == 0 ? "https=" : "http=");
  302  
  303  			size_t pxs = proxyServer.find(protocol);
  304  			if (pxs != std::string::npos)
  305  			{
  306  				size_t pxe = proxyServer.find(";", pxs);
  307  				if (pxe == std::string::npos)
  308  					proxyServer = proxyServer.substr(pxs + protocol.size());
  309  				else 
  310  					proxyServer = proxyServer.substr(pxs + protocol.size(), pxe - pxs - protocol.size());
  311  			}
  312  
  313  			if (!proxyServer.empty())
  314  			{
  315  				curl_easy_setopt(mHandle, CURLOPT_PROXY, proxyServer.c_str());
  316  				curl_easy_setopt(mHandle, CURLOPT_PROXYTYPE, CURLPROXY_HTTP);
  317  			}
  318  		}
  319  	}
  320  #endif
  321  	
  322  	std::unique_lock<std::mutex> lock(mMutex);
  323  
  324  	if (!mFilePath.empty())
  325  	{
  326  		mTempStreamPath = outputFilename + ".tmp";
  327  		
  328  		Utils::FileSystem::removeFile(mTempStreamPath);
  329  
  330  #if defined(_WIN32)
  331  		mFile = _wfopen(Utils::String::convertToWideString(mTempStreamPath).c_str(), L"wb");
  332  #else
  333  		mFile = fopen(mTempStreamPath.c_str(), "wb");		
  334  #endif
  335  
  336  		if (mFile == nullptr)
  337  		{
  338  			mStatus = REQ_IO_ERROR;
  339  			onError("IO Error (disk is Readonly ?)");			
  340  			return;
  341  		}
  342  
  343  		mPosition = 0;
  344  		Utils::FileSystem::removeFile(outputFilename);
  345  	}
  346  
  347  	//add the handle to our multi
  348  	CURLMcode merr = curl_multi_add_handle(s_multi_handle, mHandle);
  349  	if(merr != CURLM_OK)
  350  	{
  351  		closeStream();
  352  
  353  		mStatus = REQ_IO_ERROR;
  354  		onError(curl_multi_strerror(merr));
  355  		return;
  356  	}
  357  
  358  	s_requests[mHandle] = this;
  359  }
  360  
  361  void HttpReq::closeStream()
  362  {
  363  	if (mFile)
  364  	{
  365  		fflush(mFile);
  366  		fclose(mFile);
  367  		mFile = nullptr;
  368  	}
  369  }
  370  
  371  HttpReq::~HttpReq()
  372  {
  373  	std::unique_lock<std::mutex> lock(mMutex);
  374  
  375  	closeStream();
  376  	
  377  	if (!mTempStreamPath.empty())
  378  		Utils::FileSystem::removeFile(mTempStreamPath);
  379  
  380  	if(mHandle)
  381  	{
  382  		s_requests.erase(mHandle);
  383  
  384  		CURLMcode merr = curl_multi_remove_handle(s_multi_handle, mHandle);
  385  
  386  		if(merr != CURLM_OK)
  387  			LOG(LogError) << "Error removing curl_easy handle from curl_multi: " << curl_multi_strerror(merr);
  388  
  389  		curl_easy_cleanup(mHandle);
  390  	}
  391  }
  392  
  393  HttpReq::Status HttpReq::status()
  394  {
  395  	if (mStatus == REQ_IN_PROGRESS)
  396  	{
  397  		std::unique_lock<std::mutex> lock(mMutex);
  398  
  399  		int handle_count;
  400  		CURLMcode merr = curl_multi_perform(s_multi_handle, &handle_count);
  401  		if (merr != CURLM_OK && merr != CURLM_CALL_MULTI_PERFORM)
  402  		{
  403  			closeStream();
  404  
  405  			mStatus = REQ_IO_ERROR;
  406  			onError(curl_multi_strerror(merr));
  407  			return mStatus;
  408  		}
  409  
  410  		int msgs_left;
  411  		CURLMsg* msg;
  412  		while ((msg = curl_multi_info_read(s_multi_handle, &msgs_left)) != nullptr)
  413  		{
  414  			if (msg->msg == CURLMSG_DONE)
  415  			{
  416  				HttpReq* req = s_requests[msg->easy_handle];
  417  				if (req == NULL)
  418  				{
  419  					LOG(LogError) << "Cannot find easy handle!";
  420  					continue;
  421  				}
  422  
  423  				req->closeStream();
  424  
  425  				if (req->mStatus == REQ_FILESTREAM_ERROR)
  426  				{
  427  					std::string err = "File stream error (disk full ?)";
  428  					req->onError(err.c_str());
  429  				}
  430  				else if (msg->data.result == CURLE_OK)
  431  				{
  432  					int http_status_code;
  433  					curl_easy_getinfo(msg->easy_handle, CURLINFO_RESPONSE_CODE, &http_status_code);					
  434  
  435  					if (http_status_code < 200 || http_status_code > 299)
  436  					{
  437  						std::string err;
  438  
  439  						if (http_status_code >= 400 && http_status_code <= 503)
  440  						{
  441  							if (req->mFilePath.empty())
  442  							{
  443  								auto content = req->getContent();
  444  								if (!content.empty() && content.find("<body") != std::string::npos)
  445  								{
  446  									// Parse response HTML & extract body
  447  									auto body = Utils::String::extractString(content, "<body", "</body>", true);
  448  									body = Utils::String::replace(body, "\r", "");
  449  									body = Utils::String::replace(body, "\n", "");
  450  									body = Utils::String::replace(body, "</p>", "\r\n");
  451  									body = Utils::String::replace(body, "<br>", "\r\n");
  452  									body = Utils::String::replace(body, "<hr>", "\r\n");
  453  									body = Utils::String::removeHtmlTags(body);
  454  
  455  									if (!body.empty())
  456  										err = "HTTP status " + std::to_string(http_status_code) + "\r\n" + body;
  457  								}
  458  								else
  459  									err = content;
  460  							}
  461  
  462  							if (http_status_code > 500)
  463  								req->mStatus = REQ_IO_ERROR;
  464  							else
  465  								req->mStatus = (Status)http_status_code;
  466  						}						
  467  						else
  468  							req->mStatus = REQ_IO_ERROR;
  469  
  470  						if (err.empty())
  471  							err = "HTTP status " + std::to_string(http_status_code);
  472  
  473  						req->onError(err.c_str());
  474  					}
  475  					else
  476  					{
  477  						if (!req->mFilePath.empty())
  478  						{
  479  							bool renamed = Utils::FileSystem::renameFile(req->mTempStreamPath.c_str(), req->mFilePath.c_str());
  480  #if WIN32
  481  							if (renamed)
  482  							{
  483  								auto wfn = Utils::String::convertToWideString(req->mFilePath);
  484  								HANDLE hFile = CreateFileW(wfn.c_str(), GENERIC_WRITE, FILE_SHARE_WRITE, NULL, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, NULL);
  485  								if (hFile != INVALID_HANDLE_VALUE)
  486  								{
  487  									SYSTEMTIME st;
  488  									GetSystemTime(&st);              // Gets the current system time
  489  									FILETIME ft;
  490  									SystemTimeToFileTime(&st, &ft);  // Converts the current system time to file time format
  491  
  492  									SetFileTime(hFile, &ft, &ft, &ft);
  493  									CloseHandle(hFile);
  494  								}
  495  							}
  496  #endif
  497  							if (!renamed)
  498  							{
  499  								// Strange behaviour on Windows : sometimes std::rename fails if it's done too early after closing stream
  500  								// Copy file instead & try to delete it
  501  								if (Utils::FileSystem::copyFile(req->mTempStreamPath, req->mFilePath))
  502  									renamed = true;
  503  							}
  504  
  505  							if (renamed)
  506  								req->mStatus = REQ_SUCCESS;
  507  							else
  508  							{
  509  								req->mStatus = REQ_IO_ERROR;
  510  								req->onError("file rename failed");
  511  							}
  512  						}
  513  						else
  514  							req->mStatus = REQ_SUCCESS;
  515  					}
  516  				}
  517  				else
  518  				{
  519  					req->mStatus = REQ_IO_ERROR;
  520  					req->onError(curl_easy_strerror(msg->data.result));
  521  				}
  522  			}
  523  		}
  524  	}
  525  
  526  	return mStatus;
  527  }
  528  
  529  std::string HttpReq::getContent() 
  530  {
  531  	if (mFilePath.empty())
  532  		return mContent.str();
  533  
  534  	try
  535  	{
  536  		closeStream();
  537  
  538  		if (!Utils::FileSystem::exists(mTempStreamPath))
  539  			return "";
  540  
  541  		std::ifstream ifs(mTempStreamPath, std::ios_base::in | std::ios_base::binary);
  542  		if (ifs.bad())
  543  			return "";
  544  
  545  		std::stringstream ofs;
  546  		ofs << ifs.rdbuf();
  547  		ifs.close();
  548  
  549  		return ofs.str();
  550  	}
  551  	catch (...)
  552  	{
  553  		LOG(LogError) << "Error getting Http request content";
  554  	}
  555  
  556  	return "";
  557  }
  558  
  559  void HttpReq::onError(const char* msg)
  560  {
  561  	mErrorMsg = msg;
  562  	LOG(LogError) << "HttpReq::onError (" + std::to_string(mStatus) << ") : " + mErrorMsg;
  563  }
  564  
  565  std::string HttpReq::getErrorMsg()
  566  {
  567  	return mErrorMsg;
  568  }
  569  
  570  std::string HttpReq::getResponseHeader(const std::string& header)
  571  {
  572  	auto it = mResponseHeaders.find(header);
  573  	if (it != mResponseHeaders.cend())
  574  		return it->second;
  575  		
  576  	return "";
  577  }
  578  
  579  size_t HttpReq::header_callback(char *buffer, size_t size, size_t nitems, void *userdata)
  580  {
  581  	HttpReq* request = ((HttpReq*)userdata);
  582  
  583  	std::string data = Utils::String::trim(buffer);
  584  	if (!data.empty() && !Utils::String::startsWith(data, "HTTP/"))
  585  	{
  586  		auto splitPost = data.find(":");
  587  		if (splitPost != std::string::npos)
  588  			request->mResponseHeaders[Utils::String::trim(data.substr(0, splitPost))] = Utils::String::trim(data.substr(splitPost + 1));
  589  		else
  590  			request->mResponseHeaders[data] = "";
  591  	}
  592  
  593  	return nitems * size;
  594  }
  595  
  596  //used as a curl callback
  597  //size = size of an element, nmemb = number of elements
  598  //return value is number of elements successfully read
  599  size_t HttpReq::write_content(void* buff, size_t size, size_t nmemb, void* req_ptr)
  600  {
  601  	HttpReq* request = ((HttpReq*)req_ptr);
  602  		
  603  	if (request->mFilePath.empty())
  604  	{
  605  		((HttpReq*)req_ptr)->mContent.write((char*)buff, size * nmemb);
  606  		return size * nmemb;
  607  	}
  608  
  609  	FILE* file = request->mFile;
  610  	if (file == nullptr)
  611  		return 0;
  612  
  613  	size_t rs = size * nmemb;
  614  	fwrite(buff, 1, rs, file);
  615  	if (ferror(file))
  616  	{
  617  		request->closeStream();			
  618  		request->mStatus = REQ_FILESTREAM_ERROR;
  619  		request->mErrorMsg = "IO ERROR (DISK FULL?)";		
  620  
  621  		return 0;
  622  	}
  623  
  624  	curl_off_t cl = 0;
  625  	if (!curl_easy_getinfo(request->mHandle, CURLINFO_CONTENT_LENGTH_DOWNLOAD_T, &cl))
  626  	{
  627  		request->mPosition += rs;
  628  
  629  		if (cl <= 0)
  630  			request->mPercent = -1;
  631  		else
  632  			request->mPercent = (int)(request->mPosition * 100LL / cl);
  633  	}
  634  
  635  	return nmemb;
  636  }
  637  
  638  bool HttpReq::wait()
  639  {
  640  	while (status() == HttpReq::REQ_IN_PROGRESS)
  641  		std::this_thread::sleep_for(std::chrono::milliseconds(20));
  642  
  643  	return status() == HttpReq::REQ_SUCCESS;
  644  }
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 226-242 (excerpt of 3519)

```text
  226  		strtok(line, "\n");
  227  		if (flog != nullptr) 
  228  			fprintf(flog, "%s\n", line);
  229  
  230  		if (func != nullptr)
  231  			func(std::string(line));		
  232  	}
  233  
  234  	int exitCode = WEXITSTATUS(pclose(pipe));
  235  
  236  	if (flog != NULL)
  237  	{
  238  		fprintf(flog, "Exit code : %d\n", exitCode);
  239  		fclose(flog);
  240  	}
  241  
  242  	return std::pair<std::string, int>(std::string(line), exitCode);
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 556-743 (excerpt of 3519)

```text
  556  // renderer and textures were holding, which is the difference between
  557  // comfortable and marginal when WebKit needs most of a gigabyte.
  558  //
  559  // `open` returns once the window is actually up, so the screen is never blank
  560  // between ES going down and the page appearing. `wait` blocks until the page
  561  // is gone *and* the gamepad has been released, which is what ES needs before
  562  // it re-initialises -- SDL re-opens the joystick on init and would otherwise
  563  // come back with no gamepad at all.
  564  bool ApiSystem::launchCloudSignIn(Window *window, bool phoneKeyboard)
  565  {
  566  	LOG(LogDebug) << "ApiSystem::launchCloudSignIn";
  567  
  568  	// --phone tells the window not to raise its own keyboard: somebody who
  569  	// chose to type on their phone does not want the screen they are reading
  570  	// the form on covered by a keyboard they did not ask for.
  571  	const char* open = phoneKeyboard
  572  		? "/usr/bin/cloud_oauth open --phone" : "/usr/bin/cloud_oauth open";
  573  	if (system(open) != 0)
  574  	{
  575  		LOG(LogWarning) << "cloud sign-in window did not open; staying put";
  576  		return false;
  577  	}
  578  
  579  	ApiSystem::launchExternalWindow_before(window);
  580  #if defined(__GLIBC__)
  581  	// Return freed renderer heaps before waiting for sign-in (distro #570).
  582  	malloc_trim(0);
  583  #endif
  584  	int exitCode = system("/usr/bin/cloud_oauth wait");
  585  	if (WIFEXITED(exitCode))
  586  		exitCode = WEXITSTATUS(exitCode);
  587  	ApiSystem::launchExternalWindow_after(window);
  588  
  589  	// `wait` returns as soon as the sign-in lands, with the page still up
  590  	// saying "Finishing up" -- so this rebuild happens behind something
  591  	// rather than in front of a black screen. Now that we are drawing again,
  592  	// the page can go.
  593  	system("/usr/bin/cloud_oauth close");
  594  
  595  	return exitCode == 0;
  596  }
  597  
  598  bool ApiSystem::launchFileManager(Window *window) 
  599  {
  600  	LOG(LogDebug) << "ApiSystem::launchFileManager";
  601  
  602  	std::string command = "filemanagerlauncher";
  603  
  604  	ApiSystem::launchExternalWindow_before(window);
  605  
  606  	int exitCode = system(command.c_str());
  607  	if (WIFEXITED(exitCode))
  608  		exitCode = WEXITSTATUS(exitCode);
  609  
  610  	ApiSystem::launchExternalWindow_after(window);
  611  
  612  	return exitCode == 0;
  613  }
  614  
  615  #if !WIN32
  616  bool ApiSystem::enableWifi(std::string ssid, std::string key, std::string country) 
  617  {
  618  	bool ret;
  619  
  620  	// Time-boxed, because both go through nmcli to NetworkManager and the
  621  	// caller is a menu callback. wifictl connect waits up to 90 s for the
  622  	// association on a healthy stack and settles ten status polls and two
  623  	// sleeps before that; with NetworkManager itself unresponsive each
  624  	// nmcli call has only D-Bus's own timeout, and nothing above added up
  625  	// to a bound. 150 s covers the healthy worst case with room; enable is
  626  	// an rfkill call that should take no time at all.
  627  	ret = executeScript("timeout 30 wifictl enable");
  628  	if (!ret)
  629  		return ret;
  630  	
  631  	// executeScript() runs the command through a shell, so the SSID and the
  632  	// passphrase have to be quoted as literals. Double quotes are not enough:
  633  	// they still let the shell expand $, ` and \, which silently corrupts any
  634  	// passphrase containing them (and lets a crafted SSID run commands).
  635  	return executeScript("timeout 150 wifictl connect " + Utils::String::shellQuote(ssid) +
  636  			     " " + Utils::String::shellQuote(key) +
  637  			     " " + Utils::String::shellQuote(country));
  638  }
  639  #else
  640  bool ApiSystem::enableWifi(std::string ssid, std::string key)
  641  {
  642  	return executeScript("wifictl enable " + Utils::String::shellQuote(ssid) +
  643  			     " " + Utils::String::shellQuote(key));
  644  }
  645  #endif
  646  
  647  // Only the exact positive protocol answer authorizes the open-network path.
  648  std::string ApiSystem::getWifiSecurity(const std::string& ssid)
  649  {
  650  	std::vector<std::string> lines;
  651  	auto answer = executeScript("timeout 15 wifictl security " + Utils::String::shellQuote(ssid),
  652  		[&lines](const std::string line) { lines.push_back(line); });
  653  	if (answer.second == 0 && lines.size() == 1 && (lines[0] == "open" || lines[0] == "protected"))
  654  		return lines[0];
  655  	return "unknown";
  656  }
  657  
  658  bool ApiSystem::connectOpenWifi(const std::string& ssid)
  659  {
  660  	return executeScript("timeout 120 wifictl connect-open " + Utils::String::shellQuote(ssid));
  661  }
  662  
  663  bool ApiSystem::disableWifi() 
  664  {
  665  	return executeScript("timeout 30 wifictl disable");
  666  }
  667  
  668  // The three below are one nmcli call each, over D-Bus to a NetworkManager
  669  // that can stop answering (fork #102), so each is time-boxed and read by
  670  // the word it prints -- a script that printed nothing and exited 0 is not
  671  // an answer (engineering-practices: guards fail closed). Names go through
  672  // shellQuote, as enableWifi's do: they are the player's and carry anything.
  673  
  674  bool ApiSystem::getCurrentWifiSsid(std::string& ssid)
  675  {
  676  	std::vector<std::string> lines;
  677  	auto result = executeScript("timeout 10 wifictl current", [&lines](const std::string line) { lines.push_back(line); });
  678  	ssid = WifiText::parseCurrent(lines);
  679  	// 0 with the SSID, 1 for "joined to none"; anything else (2 when
  680  	// NetworkManager could not be asked, 124 from timeout) is no answer.
  681  	if (result.second == 0)
  682  		return !ssid.empty();
  683  	ssid.clear();
  684  	return result.second == 1;
  685  }
  686  
  687  bool ApiSystem::getSavedWifiNetworks(std::vector<WifiText::SavedNetwork>& networks)
  688  {
  689  	std::vector<std::string> lines;
  690  	auto result = executeScript("timeout 15 wifictl saved --ssid", [&lines](const std::string line) { lines.push_back(line); });
  691  	networks.clear();
  692  	for (const auto& line : lines)
  693  	{
  694  		if (line.empty()) continue;
  695  		WifiText::SavedNetwork network;
  696  		if (!WifiText::parseSavedDetailsLine(line, network)) { networks.clear(); return false; }
  697  		networks.push_back(network);
  698  	}
  699  	if (result.second != 0)
  700  	{
  701  		networks.clear();
  702  		return false;
  703  	}
  704  	return true;
  705  }
  706  
  707  // The picker's press on a saved network: its profile, with the key
  708  // NetworkManager holds, through wifictl join -- bounded past the 90 s
  709  // association wait the script allows itself, as enableWifi's connect is. The
  710  // name is the player's and carries anything: shellQuote.
  711  WifiText::JoinAnswer ApiSystem::joinWifiNetwork(const std::string& name)
  712  {
  713  	std::vector<std::string> lines;
  714  	auto result = executeScript("timeout 120 wifictl join " + Utils::String::shellQuote(name),
  715  		[&lines](const std::string line) { lines.push_back(line); });
  716  	WifiText::JoinAnswer answer;
  717  	answer.code = result.second != 0 ? result.second : WifiText::parseJoin(lines) ? 0 : 1;
  718  	return answer;
  719  }
  720  
  721  bool ApiSystem::forgetWifiNetwork(const std::string& name, bool& disconnected)
  722  {
  723  	disconnected = false;
  724  	if (name.empty())
  725  		return false;
  726  
  727  	std::vector<std::string> lines;
  728  	auto result = executeScript("timeout 30 wifictl forget " + Utils::String::shellQuote(name),
  729  		[&lines](const std::string line) { lines.push_back(line); });
  730  	const WifiText::ForgetOutcome outcome = WifiText::parseForget(lines);
  731  	if (result.second != 0 || !outcome.forgotten)
  732  		return false;
  733  	disconnected = outcome.disconnected;
  734  	return true;
  735  }
  736  
  737  std::vector<std::string> ApiSystem::getIpAddresses()
  738  {
  739  	LOG(LogDebug) << "ApiSystem::getIpAddresses";
  740  
  741  	return Utils::Platform::queryIPAddresses();
  742  }
  743  
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 790-838 (excerpt of 3519)

```text
  790  	executeScript("rocknix-bluetooth live_devices", func);
  791  }
  792  
  793  void ApiSystem::stopBluetoothLiveDevices()
  794  {
  795  	executeScript("rocknix-bluetooth stop_live_devices");
  796  }
  797  
  798  bool ApiSystem::pairBluetoothDevice(const std::string& deviceName)
  799  {
  800  	return executeScript("rocknix-bluetooth trust " + deviceName);
  801  }
  802  
  803  bool ApiSystem::connectBluetoothDevice(const std::string& deviceName)
  804  {
  805  	return executeScript("rocknix-bluetooth connect " + deviceName);
  806  }
  807  
  808  bool ApiSystem::disconnectBluetoothDevice(const std::string& deviceName)
  809  {
  810  	return executeScript("rocknix-bluetooth disconnect " + deviceName);
  811  }
  812  
  813  bool ApiSystem::removeBluetoothDevice(const std::string& deviceName)
  814  {
  815  	return executeScript("rocknix-bluetooth remove " + deviceName);
  816  }
  817  
  818  bool ApiSystem::scanNewBluetooth(const std::function<void(const std::string)>& func)
  819  {
  820  	return executeScript("rocknix-bluetooth trust input", func).second == 0;
  821  }
  822  
  823  std::vector<std::string> ApiSystem::getPairedBluetoothDeviceList()
  824  {
  825  	return executeEnumerationScript("rocknix-bluetooth list");
  826  }
  827  
  828  std::vector<std::string> ApiSystem::getAvailableStorageDevices() 
  829  {
  830  	return executeEnumerationScript("rocknix-config storage list");
  831  }
  832  
  833  std::vector<std::string> ApiSystem::getVideoModes(const std::string output)
  834  {
  835    if(output == "") {
  836      return executeEnumerationScript("batocera-resolution listModes");
  837    } else {
  838      return executeEnumerationScript("batocera-resolution --screen \"" + output + "\" listModes");
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 864-933 (excerpt of 3519)

```text
  864  	return executeEnumerationScript("echo no");
  865  }
  866  
  867  std::vector<std::string> ApiSystem::getSystemInformations() 
  868  {
  869  	return executeEnumerationScript("rocknix-info --full");
  870  }
  871  
  872  std::vector<BiosSystem> ApiSystem::getBiosInformations(const std::string system, bool all) 
  873  {
  874  	std::vector<BiosSystem> res;
  875  	BiosSystem current;
  876  	bool isCurrent = false;
  877  
  878  	// The default output lists problems only, which is what the launch-time
  879  	// check wants. --all adds every present file, for the BIOS CHECK page.
  880  	std::string cmd = "rocknix-systems";
  881  	if (all)
  882  		cmd += " --all";
  883  	else if (!system.empty())
  884  		cmd += " --filter " + system;
  885  
  886  	auto systems = executeEnumerationScript(cmd);
  887  	for (auto line : systems)
  888  	{
  889  		if (Utils::String::startsWith(line, "> ")) 
  890  		{
  891  			if (isCurrent)
  892  				res.push_back(current);
  893  
  894  			isCurrent = true;
  895  			current.name = std::string(std::string(line).substr(2));
  896  			current.bios.clear();
  897  		}
  898  		else 
  899  		{
  900  			BiosFile biosFile;
  901  			std::vector<std::string> tokens = Utils::String::split(line, ' ');
  902  			if (tokens.size() >= 3) 
  903  			{
  904  				biosFile.status = tokens.at(0);
  905  				biosFile.md5 = tokens.at(1);
  906  
  907  				// concatenat the ending words
  908  				std::string vname = "";
  909  				for (unsigned int i = 2; i < tokens.size(); i++) 
  910  				{
  911  					if (i > 2) vname += " ";
  912  					vname += tokens.at(i);
  913  				}
  914  				biosFile.path = vname;
  915  
  916  				current.bios.push_back(biosFile);
  917  			}
  918  		}
  919  	}
  920  
  921  	if (isCurrent)
  922  		res.push_back(current);
  923  
  924  	return res;
  925  }
  926  
  927  bool ApiSystem::generateSupportFile() 
  928  {
  929  	return executeScript("batocera-support");
  930  }
  931  
  932  std::string ApiSystem::getCurrentStorage() 
  933  {
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 974-998 (excerpt of 3519)

```text
  974  		rumblePath = joypadPath + "/rumble_enable";
  975  
  976  	if (!Utils::FileSystem::exists(rumblePath))
  977  		return "";
  978  
  979  	return rumblePath;
  980  }
  981  
  982  bool ApiSystem::setStorage(std::string selected) 
  983  {
  984  	return executeScript("rocknix-config storage " + selected);
  985  }
  986  
  987  bool ApiSystem::setButtonColorGameForce(std::string selected)
  988  {
  989  	return executeScript("batocera-gameforce buttonColorLed " + selected);
  990  }
  991  
  992  bool ApiSystem::setPowerLedGameForce(std::string selected)
  993  {
  994  	return executeScript("batocera-gameforce powerLed " + selected);
  995  }
  996  
  997  bool ApiSystem::setButtonColorR36Ultra(const std::string& selected)
  998  {
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 1021-1045 (excerpt of 3519)

```text
 1021  	return true;
 1022  }
 1023  
 1024  bool ApiSystem::forgetBluetoothControllers() 
 1025  {
 1026  	return executeScript("rocknix-config forgetBT");
 1027  }
 1028  
 1029  std::string ApiSystem::getRootPassword() 
 1030  {
 1031  	LOG(LogDebug) << "ApiSystem::getRootPassword";
 1032  	auto RootPassword = SystemConf::getInstance()->get("root.password");
 1033  	if (!RootPassword.empty())
 1034  		return RootPassword;
 1035  
 1036  	return "linux";
 1037  }
 1038  
 1039  std::vector<std::string> ApiSystem::getAvailableVideoOutputDevices() 
 1040  {
 1041  	return executeEnumerationScript("rocknix-config lsoutputs");
 1042  }
 1043  
 1044  std::vector<std::string> ApiSystem::getAvailableAudioOutputDevices() 
 1045  {
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 1476-1671 (excerpt of 3519)

```text
 1476  			res.push_back(bz);
 1477  	}
 1478  
 1479  	return res;
 1480  }
 1481  
 1482  std::pair<std::string, int> ApiSystem::installBatoceraBezel(std::string bezelsystem, const std::function<void(const std::string)>& func)
 1483  {
 1484  	return executeScript("rocknix-es-thebezelproject install " + bezelsystem, func);
 1485  }
 1486  
 1487  std::pair<std::string, int> ApiSystem::uninstallBatoceraBezel(std::string bezelsystem, const std::function<void(const std::string)>& func)
 1488  {
 1489  	return executeScript("rocknix-es-thebezelproject remove " + bezelsystem, func);
 1490  }
 1491  
 1492  std::string ApiSystem::getMD5(const std::string fileName, bool fromZipContents)
 1493  {
 1494  	LOG(LogDebug) << "getMD5 >> " << fileName;
 1495  
 1496  	// 7za x -so test.7z | md5sum
 1497  	std::string ext = Utils::String::toLower(Utils::FileSystem::getExtension(fileName));
 1498  	if (ext == ".zip" && fromZipContents)
 1499  	{
 1500  		Utils::Zip::ZipFile file;
 1501  		if (file.load(fileName))
 1502  		{
 1503  			std::string romName;
 1504  
 1505  			for (auto name : file.namelist())
 1506  			{
 1507  				if (Utils::FileSystem::getExtension(name) != ".txt" && !Utils::String::endsWith(name, "/"))
 1508  				{
 1509  					if (!romName.empty())
 1510  					{
 1511  						romName = "";
 1512  						break;
 1513  					}
 1514  
 1515  					romName = name;
 1516  				}
 1517  			}
 1518  
 1519  			if (!romName.empty())
 1520  				return file.getFileMd5(romName);
 1521  		}
 1522  	}
 1523  
 1524  #if !WIN32
 1525  	if (fromZipContents && ext == ".7z")
 1526  	{
 1527  		auto cmd = getSevenZipCommand() + " x -so \"" + fileName + "\" | md5sum";
 1528  		auto ret = executeEnumerationScript(cmd);
 1529  		if (ret.size() == 1 && ret.cbegin()->length() >= 32)
 1530  			return ret.cbegin()->substr(0, 32);
 1531  	}
 1532  #endif
 1533  
 1534  	std::string contentFile = fileName;
 1535  	std::string ret;
 1536  	std::string tmpZipDirectory;
 1537  
 1538  	if (fromZipContents && ext == ".7z")
 1539  	{
 1540  		tmpZipDirectory = Utils::FileSystem::combine(Utils::FileSystem::getTempPath(), Utils::FileSystem::getStem(fileName));
 1541  		Utils::FileSystem::deleteDirectoryFiles(tmpZipDirectory);
 1542  
 1543  		if (unzipFile(fileName, tmpZipDirectory))
 1544  		{
 1545  			auto fileList = Utils::FileSystem::getDirContent(tmpZipDirectory, true);
 1546  
 1547  			std::vector<std::string> res;
 1548  			std::copy_if(fileList.cbegin(), fileList.cend(), std::back_inserter(res), [](const std::string file) { return Utils::FileSystem::getExtension(file) != ".txt";  });
 1549  		
 1550  			if (res.size() == 1)
 1551  				contentFile = *res.cbegin();
 1552  		}
 1553  
 1554  		// if there's no file or many files ? get md5 of archive
 1555  	}
 1556  
 1557  	ret = Utils::FileSystem::getFileMd5(contentFile);
 1558  
 1559  	if (!tmpZipDirectory.empty())
 1560  		Utils::FileSystem::deleteDirectoryFiles(tmpZipDirectory, true);
 1561  
 1562  	LOG(LogDebug) << "getMD5 << " << ret;
 1563  
 1564  	return ret;
 1565  }
 1566  
 1567  std::string ApiSystem::getCRC32(std::string fileName, bool fromZipContents)
 1568  {
 1569  	LOG(LogDebug) << "getCRC32 >> " << fileName;
 1570  
 1571  	std::string ext = Utils::String::toLower(Utils::FileSystem::getExtension(fileName));
 1572  
 1573  	if (ext == ".7z" && fromZipContents)
 1574  	{
 1575  		LOG(LogDebug) << "getCRC32 is using 7z";
 1576  
 1577  		std::string fn = Utils::FileSystem::getFileName(fileName);
 1578  		auto cmd = getSevenZipCommand() + " l -slt \"" + fileName + "\"";
 1579  		auto lines = executeEnumerationScript(cmd);
 1580  		for (std::string all : lines)
 1581  		{
 1582  			int idx = all.find("CRC = ");
 1583  			if (idx != std::string::npos)
 1584  				return all.substr(idx + 6);
 1585  			else if (all.find(fn) == (all.size() - fn.size()) && all.length() > 8 && all[9] == ' ')
 1586  				return all.substr(0, 8);
 1587  		}
 1588  	}
 1589  	else if (ext == ".zip" && fromZipContents)
 1590  	{
 1591  		LOG(LogDebug) << "getCRC32 is using ZipFile";
 1592  
 1593  		Utils::Zip::ZipFile file;
 1594  		if (file.load(fileName))
 1595  		{
 1596  			std::string romName;
 1597  
 1598  			for (auto name : file.namelist())
 1599  			{
 1600  				if (Utils::FileSystem::getExtension(name) != ".txt" && !Utils::String::endsWith(name, "/"))
 1601  				{
 1602  					if (!romName.empty())
 1603  					{
 1604  						romName = "";
 1605  						break;
 1606  					}
 1607  
 1608  					romName = name;
 1609  				}
 1610  			}
 1611  
 1612  			if (!romName.empty())
 1613  				return file.getFileCrc(romName);
 1614  		}
 1615  	}
 1616  
 1617  	LOG(LogDebug) << "getCRC32 is using fileBuffer";
 1618  	return Utils::FileSystem::getFileCrc32(fileName);
 1619  }
 1620  
 1621  bool ApiSystem::unzipFile(const std::string fileName, const std::string destFolder, const std::function<bool(const std::string)>& shouldExtract)
 1622  {
 1623  	LOG(LogDebug) << "unzipFile >> " << fileName << " to " << destFolder;
 1624  
 1625  	if (!Utils::FileSystem::exists(destFolder))
 1626  		Utils::FileSystem::createDirectory(destFolder);
 1627  		
 1628  	if (Utils::String::toLower(Utils::FileSystem::getExtension(fileName)) == ".zip")
 1629  	{
 1630  		LOG(LogDebug) << "unzipFile is using ZipFile";
 1631  
 1632  		Utils::Zip::ZipFile file;
 1633  		if (file.load(fileName))
 1634  		{
 1635  			for (auto name : file.namelist())
 1636  			{
 1637  				if (Utils::String::endsWith(name, "/"))
 1638  				{
 1639  					Utils::FileSystem::createDirectory(Utils::FileSystem::combine(destFolder, name.substr(0, name.length() - 1)));
 1640  					continue;
 1641  				}
 1642  
 1643  				if (shouldExtract != nullptr && !shouldExtract(Utils::FileSystem::combine(destFolder, name)))
 1644  					continue;
 1645  
 1646  				file.extract(name, destFolder);
 1647  			}
 1648  
 1649  			LOG(LogDebug) << "unzipFile << OK";
 1650  			return true;
 1651  		}
 1652  
 1653  		LOG(LogDebug) << "unzipFile << KO Bad format ?" << fileName;
 1654  		return false;
 1655  	}
 1656  	
 1657  	LOG(LogDebug) << "unzipFile is using 7z";
 1658  
 1659  	std::string cmd = getSevenZipCommand() + " x \"" + Utils::FileSystem::getPreferredPath(fileName) + "\" -y -o\"" + Utils::FileSystem::getPreferredPath(destFolder) + "\"";
 1660  	bool ret = executeScript(cmd);
 1661  	LOG(LogDebug) << "unzipFile <<";
 1662  	return ret;
 1663  }
 1664  
 1665  bool ApiSystem::getBrightness(std::vector<BrightnessDevice>& values)
 1666  {	
 1667  	#if WIN32
 1668  	return false;
 1669  	#endif
 1670  
 1671  	auto files = Utils::FileSystem::getDirContent("/sys/class/backlight");
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 1860-1898 (excerpt of 3519)

```text
 1860  		getLEDColours(red, green, blue);
 1861  		executeScript("batocera-led-handheld block_color_changes");
 1862  		return true;
 1863  	}
 1864  
 1865  	return false;
 1866  }
 1867  
 1868  void ApiSystem::getLEDColours(int& red, int& green, int& blue)
 1869  {
 1870  	std::string colourValue = SystemConf::getInstance()->get("led.colour");
 1871  	if (colourValue.empty())
 1872  		colourValue = "255 0 165";
 1873  
 1874      std::stringstream ss(colourValue);
 1875      std::string token;
 1876  
 1877  	// Extract red value
 1878      std::getline(ss, token, ' ');
 1879      red = std::stoi(token);
 1880  
 1881  	// Extract green value
 1882      std::getline(ss, token, ' ');
 1883      green = std::stoi(token);
 1884  
 1885  	// Extract blue value
 1886      std::getline(ss, token);
 1887      blue = std::stoi(token);
 1888  
 1889  	LOG(LogInfo) << "ApiSystem::getLEDColours > LED colours are: " << red << " " << green << " " << blue;
 1890  }
 1891  
 1892  void ApiSystem::setLEDColours(int red, int green, int blue)
 1893  {
 1894  #if WIN32    
 1895      return;
 1896  #endif
 1897  
 1898  	if (mSystemLedType == LED_TYPE_NONE)
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 2072-2098 (excerpt of 3519)

```text
 2072  
 2073      int rBase = 255, gBase = 255, bBase = 255;
 2074      
 2075      // Simple parser for "R G B" or "RRGGBB" formats
 2076      if (colorStr.find(" ") != std::string::npos) {
 2077          std::vector<std::string> parts = Utils::String::split(colorStr, ' ');
 2078          if (parts.size() >= 3) {
 2079              rBase = Utils::String::toInteger(parts[0]);
 2080              gBase = Utils::String::toInteger(parts[1]);
 2081              bBase = Utils::String::toInteger(parts[2]);
 2082          }
 2083      } else if (colorStr.length() == 6) {
 2084          rBase = std::stoul(colorStr.substr(0, 2), nullptr, 16);
 2085          gBase = std::stoul(colorStr.substr(2, 2), nullptr, 16);
 2086          bBase = std::stoul(colorStr.substr(4, 2), nullptr, 16);
 2087      }
 2088  
 2089      float factor = static_cast<float>(value) / 100.0f;
 2090      int rOut = static_cast<int>(rBase * factor + 0.5f);
 2091      int gOut = static_cast<int>(gBase * factor + 0.5f);
 2092      int bOut = static_cast<int>(bBase * factor + 0.5f);
 2093  
 2094      if (LED_BRIGHTNESS_VALUE.find("rgb:l") != std::string::npos)
 2095      {
 2096          int max = Utils::String::toInteger(Utils::FileSystem::readAllText(LED_MAX_BRIGHTNESS_VALUE));
 2097          int brightnessValue = static_cast<int>(factor * max + 0.5f);
 2098          for (int i = 1; i <= 7; i++) {
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 2225-2448 (excerpt of 3519)

```text
 2225  	// NetworkManager to rescan (-w 15), sleeps, then lists; scanlist adds a
 2226  	// second rescan and sleep in front. The boxes sit past the healthy worst
 2227  	// case so they only ever close on a NetworkManager that has stopped
 2228  	// answering -- where, without them, each nmcli call would wait out
 2229  	// D-Bus on its own and the caller would wait for all of them.
 2230  	return executeEnumerationScript(scan ? "timeout 45 wifictl scanlist" : "timeout 30 wifictl list");
 2231  }
 2232  
 2233  std::vector<std::string> ApiSystem::executeEnumerationScript(const std::string command)
 2234  {
 2235  	LOG(LogDebug) << "ApiSystem::executeEnumerationScript -> " << Utils::String::maskSecrets(command);
 2236  
 2237  	std::vector<std::string> res;
 2238  
 2239  	FILE *pipe = popen(command.c_str(), "r");
 2240  
 2241  	if (pipe == NULL)
 2242  		return res;
 2243  
 2244  	char line[1024];
 2245  	while (fgets(line, 1024, pipe))
 2246  	{
 2247  		strtok(line, "\n");
 2248  		res.push_back(std::string(line));
 2249  	}
 2250  
 2251  	pclose(pipe);
 2252  	return res;
 2253  }
 2254  
 2255  std::vector<std::string> ApiSystem::executeScriptLegacy(const std::string& command) {
 2256  	std::vector<std::string> vec;
 2257  	executeScriptLegacy(command, [&vec](const std::string& line) {
 2258  		vec.push_back(line);
 2259  	});
 2260  	return vec;
 2261  }
 2262  
 2263  std::pair<std::string, int> ApiSystem::executeScriptLegacy(const std::string& command, const std::function<void(const std::string)>& func)
 2264  {
 2265  	const std::string shown = Utils::String::maskSecrets(command);
 2266  	std::cout << "ApiSystem::executeScriptLegacy -> " << shown << std::endl;
 2267  	LOG(LogInfo) << "ApiSystem::executeScriptLegacy -> " << shown;
 2268  
 2269  	FILE *pipe = popen(command.c_str(), "r");
 2270  	if (pipe == NULL)
 2271  	{
 2272  		LOG(LogError) << "Error executing " << shown;
 2273  		return std::pair<std::string, int>("Error starting command : " + shown, -1);
 2274  	}
 2275  
 2276  	std::stringstream output_stream;
 2277  	char buff[1024];
 2278  	while (fgets(buff, 1024, pipe))
 2279  	{
 2280  		std::stringstream output_stream(buff);
 2281  		std::string line;
 2282  		while (getline(output_stream, line).good()) {
 2283  			if (line.empty()) continue;
 2284  			std::cout << line << std::endl;
 2285  			if (func != nullptr) {
 2286  				func(std::string(line));
 2287  			}
 2288  		}
 2289  	}
 2290  
 2291  	int exitCode = WEXITSTATUS(pclose(pipe));
 2292  	return std::pair<std::string, int>("", exitCode);
 2293  }
 2294  
 2295  std::pair<std::string, int> ApiSystem::executeScript(const std::string command, const std::function<void(const std::string)>& func)
 2296  {
 2297  	const std::string shown = Utils::String::maskSecrets(command);
 2298  	LOG(LogInfo) << "ApiSystem::executeScript -> " << shown;
 2299  
 2300  	FILE *pipe = popen(command.c_str(), "r");
 2301  	if (pipe == NULL)
 2302  	{
 2303  		LOG(LogError) << "Error executing " << shown;
 2304  		return std::pair<std::string, int>("Error starting command : " + shown, -1);
 2305  	}
 2306  
 2307  	// Zeroed: the pair's first member is built from this buffer after the
 2308  	// loop, and a command that printed nothing -- wifictl current with no
 2309  	// network joined -- used to hand it back uninitialised.
 2310  	char line[1024] = "";
 2311  	while (fgets(line, 1024, pipe))
 2312  	{
 2313  		strtok(line, "\n");
 2314  
 2315  		if (func != nullptr)
 2316  			func(std::string(line));
 2317  	}
 2318  
 2319  	int exitCode = WEXITSTATUS(pclose(pipe));
 2320  	return std::pair<std::string, int>(line, exitCode);
 2321  }
 2322  
 2323  bool ApiSystem::executeScript(const std::string command)
 2324  {	
 2325  	const std::string shown = Utils::String::maskSecrets(command);
 2326  	LOG(LogInfo) << "Running " << shown;
 2327  
 2328  	if (system(command.c_str()) == 0)
 2329  		return true;
 2330  	
 2331  	LOG(LogError) << "Error executing " << shown;
 2332  	return false;
 2333  }
 2334  
 2335  bool ApiSystem::isScriptingSupported(ScriptId script)
 2336  {
 2337  	std::vector<std::string> executables;
 2338  
 2339  	switch (script)
 2340  	{
 2341  	case ApiSystem::THEMESDOWNLOADER:
 2342  		return true;
 2343  	case ApiSystem::RETROACHIVEMENTS:
 2344  #ifdef CHEEVOS_DEV_LOGIN
 2345  		return true;
 2346  #endif
 2347  		break;
 2348  	case ApiSystem::KODI:
 2349  		executables.push_back("kodi");
 2350  		break;
 2351  	case ApiSystem::WIFI:
 2352  		executables.push_back("wifictl");
 2353  		break;
 2354  	case ApiSystem::BLUETOOTH:
 2355  		executables.push_back("rocknix-bluetooth");
 2356  		break;
 2357  	case ApiSystem::RESOLUTION:
 2358  		executables.push_back("rocknix-resolution");
 2359  		break;
 2360  	case ApiSystem::BIOSINFORMATION:
 2361  		executables.push_back("rocknix-systems");
 2362  		break;
 2363  	case ApiSystem::DISKFORMAT:
 2364  		executables.push_back("batocera-format");
 2365  		break;
 2366  	case ApiSystem::OVERCLOCK:
 2367  		executables.push_back("batocera-overclock");
 2368  		break;
 2369  	case ApiSystem::NETPLAY:
 2370  		executables.push_back("7zr");
 2371  		break;
 2372  	case ApiSystem::PDFEXTRACTION:
 2373  		executables.push_back("pdftoppm");
 2374  		executables.push_back("pdfinfo");
 2375  		break;
 2376  	case ApiSystem::BATOCERASTORE:
 2377  		executables.push_back("batocera-store");
 2378  		break;
 2379  	case ApiSystem::THEBEZELPROJECT:
 2380  		executables.push_back("rocknix-es-thebezelproject");
 2381  		break;		
 2382  	case ApiSystem::PADSINFO:
 2383  		executables.push_back("batocera-padsinfo");
 2384  		break;
 2385  	case ApiSystem::EVMAPY:
 2386  		executables.push_back("evmapy");
 2387  		break;
 2388  	case ApiSystem::BATOCERAPREGAMELISTSHOOK:
 2389  		executables.push_back("batocera-preupdate-gamelists-hook");
 2390  		break;
 2391  	case ApiSystem::TIMEZONES:
 2392  		executables.push_back("batocera-timezone");
 2393  		break;
 2394  	case ApiSystem::AUDIODEVICE:
 2395  		executables.push_back("set-audio");
 2396  		break;		
 2397  	case ApiSystem::BACKUP:
 2398  		executables.push_back("rocknix-sync");
 2399  		break;
 2400  	case ApiSystem::INSTALL:
 2401  		executables.push_back("batocera-install");
 2402  		break;	
 2403  	case ApiSystem::SUPPORTFILE:
 2404  		executables.push_back("batocera-support");
 2405  		break;
 2406  	case ApiSystem::UPGRADE:
 2407  		executables.push_back("rocknix-update");
 2408  		break;
 2409  	case ApiSystem::UPGRADEVIATORRENT:
 2410  		executables.push_back("batocera-upgrade-torrent");
 2411  		break;
 2412  	case ApiSystem::SUSPEND:
 2413  		return (Utils::FileSystem::exists("/usr/sbin/pm-suspend") && Utils::FileSystem::exists("/usr/bin/pm-is-supported") && executeScript("/usr/bin/pm-is-supported --suspend"));
 2414  	case ApiSystem::VERSIONINFO:
 2415  		executables.push_back("batocera-version");
 2416  		break;
 2417  	case ApiSystem::READPLANEMODE:
 2418  	case ApiSystem::WRITEPLANEMODE:
 2419  		executables.push_back("batocera-planemode");
 2420  		break;
 2421  	case ApiSystem::SERVICES:
 2422  		executables.push_back("batocera-services");
 2423  		break;
 2424  	case ApiSystem::BACKGLASS:
 2425  		executables.push_back("batocera-backglass");
 2426  		break;
 2427  	case ApiSystem::NFC:
 2428  		executables.push_back("batocera-nfc");
 2429  		break;
 2430  	}
 2431  
 2432  	if (executables.size() == 0)
 2433  		return true;
 2434  
 2435  	for (auto executable : executables)
 2436  		if (!Utils::FileSystem::exists("/usr/bin/" + executable))
 2437  			return false;
 2438  
 2439  	return true;
 2440  }
 2441  
 2442  bool ApiSystem::downloadFile(const std::string url, const std::string fileName, const std::string label, const std::function<void(const std::string)>& func)
 2443  {
 2444  	if (func != nullptr)
 2445  		func("Downloading " + label);
 2446  
 2447  	HttpReq httpreq(url, fileName);
 2448  	while (httpreq.status() == HttpReq::REQ_IN_PROGRESS)
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 2497-2528 (excerpt of 3519)

```text
 2497  	return ret;
 2498  #endif
 2499  	return executeEnumerationScript("batocera-format listFstypes");
 2500  }
 2501  
 2502  int ApiSystem::formatDisk(const std::string disk, const std::string format, const std::function<void(const std::string)>& func)
 2503  {
 2504  	return executeScript("batocera-format format " + disk + " " + format, func).second;
 2505  }
 2506  
 2507  int ApiSystem::getPdfPageCount(const std::string& fileName)
 2508  {
 2509  	auto lines = executeEnumerationScript("pdfinfo \"" + fileName + "\"");
 2510  	for (auto line : lines)
 2511  	{
 2512  		auto splits = Utils::String::split(line, ':', true);
 2513  		if (splits.size() == 2 && splits[0] == "Pages")
 2514  			return atoi(Utils::String::trim(splits[1]).c_str());
 2515  	}
 2516  
 2517  	return 0;
 2518  }
 2519  
 2520  std::vector<std::string> ApiSystem::extractPdfImages(const std::string& fileName, int pageIndex, int pageCount, int quality)
 2521  {
 2522  	auto pdfFolder = Utils::FileSystem::getPdfTempPath();
 2523  
 2524  	std::vector<std::string> ret;
 2525  
 2526  	if (pageIndex < 0)
 2527  	{
 2528  		Utils::FileSystem::deleteDirectoryFiles(pdfFolder);
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 2577-2603 (excerpt of 3519)

```text
 2577  	if (pageIndex >= 0)
 2578  	{
 2579  		char buffer[12];
 2580  		sprintf(buffer, "%08d", (uint32_t)pageIndex);
 2581  		
 2582  		if (pageIndex < 0)
 2583  			prefix = "page-" + squality + "-" + std::string(buffer) + "-pdf"; // page
 2584  		else
 2585  			prefix = Utils::FileSystem::getFileName(fileName) + "-" + squality + "-" + std::string(buffer) + "-pdf"; // page
 2586  
 2587  		page = " -f " + std::to_string(pageIndex) + " -l " + std::to_string(pageIndex + pageCount - 1);
 2588  	}
 2589  
 2590  #if WIN32
 2591  	executeEnumerationScript("pdftoppm -r "+ squality + page +" \"" + fileName + "\" \""+ pdfFolder +"/" + prefix +"\"");
 2592  #else
 2593  	executeEnumerationScript("pdftoppm -jpeg -r "+ squality +" -cropbox" + page + " \"" + fileName + "\" \"" + pdfFolder + "/" + prefix + "\"");
 2594  #endif
 2595  
 2596  	int time = SDL_GetTicks() - lastTime;
 2597  	std::string text = std::to_string(time);
 2598  	
 2599  	for (auto file : Utils::FileSystem::getDirContent(pdfFolder, false))
 2600  	{
 2601  		auto ext = Utils::String::toLower(Utils::FileSystem::getExtension(file));
 2602  		if (ext != ".jpg" && ext != ".png" && ext != ".ppm")
 2603  			continue;
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 2907-2930 (excerpt of 3519)

```text
 2907  {
 2908  	auto res = executeEnumerationScript("cat /boot/boot/batocera.board");
 2909  	if (res.size() > 0)
 2910  		return res[0];
 2911  
 2912  	return "";
 2913  }
 2914  
 2915  std::string ApiSystem::getHostsName()
 2916  {
 2917  	auto hostName = SystemConf::getInstance()->get("system.hostname");
 2918  	if (!hostName.empty())
 2919  		return hostName;
 2920  
 2921  	return "127.0.0.1";
 2922  }
 2923  
 2924  bool ApiSystem::emuKill()
 2925  {
 2926  	LOG(LogDebug) << "ApiSystem::emuKill";
 2927  	return executeScript("batocera-es-swissknife --emukill");
 2928  }
 2929  
 2930  void ApiSystem::suspend()
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 3478-3518 (excerpt of 3519)

```text
 3478  		res = executeScript("batocera-services " + std::string(enable ? "start" : "stop") + " " + serviceName);
 3479  	
 3480  	return res;
 3481  }
 3482  
 3483  std::vector<std::string> ApiSystem::getEjectableDrives()
 3484  {
 3485      return executeEnumerationScript("batocera-storage-manager list_ejectable");
 3486  }
 3487  
 3488  bool ApiSystem::ejectDrive(const std::string& mountPath)
 3489  {
 3490      std::string cmd = "batocera-storage-manager eject \"" + mountPath + "\"";
 3491      return executeScript(cmd);
 3492  }
 3493  
 3494  bool ApiSystem::mergeDrive(const std::string& mountPath)
 3495  {
 3496      std::string cmd = "batocera-storage-manager merge \"" + mountPath + "\"";
 3497      return executeScript(cmd);
 3498  }
 3499  
 3500  bool ApiSystem::prepareDrive(const std::string& device, const std::string& fsType)
 3501  {
 3502      std::string cmd = "batocera-storage-manager format \"" + device + "\" \"" + fsType + "\"";
 3503      return executeScript(cmd);
 3504  }
 3505  
 3506  bool ApiSystem::ignoreDevicePermanently(const std::string& deviceId)
 3507  {
 3508      std::string cmd = "batocera-storage-manager ignore \"" + deviceId + "\"";
 3509      return executeScript(cmd);
 3510  }
 3511  
 3512  bool ApiSystem::nfc_is_available() {
 3513    return Utils::FileSystem::exists("/var/run/batocera-nfc.running");
 3514  }
 3515  
 3516  bool ApiSystem::nfc_write(const std::string& game) {
 3517    std::string cmd = "batocera-nfc --write \"" + game + "\"";
 3518    return executeScript(cmd);
```


## es-app/src/guis/GuiWifi.cpp @ 16dbac5211: lines 272-408 (excerpt of 607)

```text
  272  // name NetworkManager holds a profile for joins, the one the device is on
  273  // needs nothing, any other is asked for its key. Not trimmed: a name may
  274  // begin or end with a space, and it is matched as NetworkManager has it.
  275  void GuiWifi::onManualInput()
  276  {
  277  	if (mWaitingLoad || mScan)
  278  		return;
  279  
  280  	auto onName = [this](const std::string& name)
  281  	{
  282  		if (name.empty())
  283  			return;
  284  		const auto profile = WifiText::preferredProfile(name, mSaved);
  285  		if (mSavedKnown && WifiText::profilesForSsid(name, mSaved).size() > 1 && profile.empty())
  286  		{
  287  			chooseProfile(name);
  288  			return;
  289  		}
  290  		act(WifiText::manualAction(name, mCurrent, mSaved, mSavedKnown), name,
  291  			profile.empty() ? WifiText::manualJoinName(name, mCurrent, mCurrentProfile) : profile);
  292  	};
  293  
  294  	if (Settings::getInstance()->getBool("UseOSK"))
  295  		mWindow->pushGui(new GuiTextEditPopupKeyboard(mWindow, mTitle, "", onName, false));
  296  	else
  297  		mWindow->pushGui(new GuiTextEditPopup(mWindow, mTitle, "", onName, false));
  298  }
  299  
  300  // A saved network: its profile, with the key NetworkManager holds, behind
  301  // the spinner -- wifictl join waits up to 90 s for the association, as
  302  // connect does, and the screen would otherwise freeze for it. The script
  303  // also moves the settings wifi.ssid and wifi.key onto the joined network,
  304  // so the paths that connect from the settings (the restore wizard, the
  305  // ENABLE WI-FI switch) still name the network the player is on; SystemConf
  306  // is re-read so the interface sees the same file.
  307  void GuiWifi::join(const std::string& name, const std::string& profile)
  308  {
  309  	Window* window = mWindow;
  310  	mWaitingLoad = true;
  311  	LOG(LogInfo) << "wifi picker: joining the saved network " << name << " (profile " << profile << ")";
  312  	window->pushGui(new GuiLoading<WifiText::JoinAnswer>(window, _("CONNECTING TO WI-FI"),
  313  		[profile](IGuiLoadingHandler*) { return ApiSystem::getInstance()->joinWifiNetwork(profile); },
  314  		[this, window, name, profile](WifiText::JoinAnswer answer)
  315  		{
  316  			mWaitingLoad = false;
  317  			const int code = answer.code;
  318  			if (!answer.joined())
  319  			{
  320  				LOG(LogWarning) << "wifi picker: could not join the saved network " << name << " (profile " << profile << ", wifictl join exited " << code << ")";
  321  				// The advice by what happened (WifiText::joinFailure, #308
  322  				// F-WF-03/06): NetworkManager not answering is not a key that
  323  				// changed, and forgetting the network on that advice would
  324  				// lose a profile that was fine.
  325  				const std::string advice = WifiText::joinFailure(code) == WifiText::JoinFailure::ServiceNotAnswering
  326  					? _("THE WI-FI SERVICE DIDN'T ANSWER. TRY AGAIN IN A MOMENT.")
  327  					: _("IF ITS KEY HAS CHANGED, FORGET IT UNDER MANAGE SAVED NETWORKS AND JOIN IT AGAIN WITH THE NEW KEY.");
  328  				window->pushGui(new GuiMsgBox(window,
  329  					Utils::String::format(_("COULDN'T CONNECT TO %s.").c_str(), name.c_str()) + "\n\n" + advice, _("OK")));
  330  				return;
  331  			}
  332  			// Re-read for what the join wrote (wifi.ssid, wifi.key), keeping
  333  			// any change this interface has not saved yet -- one the settings
  334  			// lock refused -- unless the join wrote that key (G-E1-03).
  335  			SystemConf::getInstance()->loadSystemConf(true);
  336  			joined(name);
  337  		}));
  338  }
  339  
  340  // Any other network: its key first -- empty for an open network -- then
  341  // the connection wifictl connect makes, which leaves a profile behind for
  342  // next time. On success the settings take the network and its key, as they
  343  // did when the row edited them: the network configured last, for the paths
  344  // that connect from the settings.
  345  void GuiWifi::checkSecurityAndConnect(const std::string& name)
  346  {
  347  	mWaitingLoad = true;
  348  	mWindow->pushGui(new GuiLoading<std::string>(mWindow, _("CHECKING WI-FI NETWORK"),
  349  		[name](IGuiLoadingHandler*) { return ApiSystem::getInstance()->getWifiSecurity(name); },
  350  		[this, name](const std::string& security)
  351  		{
  352  			mWaitingLoad = false;
  353  			if (security == "open")
  354  				connect(name, "", true);
  355  			else
  356  				askKeyAndConnect(name);
  357  		}));
  358  }
  359  
  360  void GuiWifi::askKeyAndConnect(const std::string& name)
  361  {
  362  	auto onKey = [this, name](const std::string& key) { connect(name, key); };
  363  
  364  	if (Settings::getInstance()->getBool("UseOSK"))
  365  		mWindow->pushGui(new GuiTextEditPopupKeyboard(mWindow, _("WI-FI KEY"), "", onKey, false));
  366  	else
  367  		mWindow->pushGui(new GuiTextEditPopup(mWindow, _("WI-FI KEY"), "", onKey, false));
  368  }
  369  
  370  void GuiWifi::connect(const std::string& name, const std::string& key, bool openNetwork)
  371  {
  372  	Window* window = mWindow;
  373  	mWaitingLoad = true;
  374  	LOG(LogInfo) << "wifi picker: connecting to " << name;
  375  #if !WIN32
  376  	const std::string country = SystemConf::getInstance()->get("wifi.country");
  377  	auto apply = [name, key, country, openNetwork](IGuiLoadingHandler*) { return openNetwork ? ApiSystem::getInstance()->connectOpenWifi(name) : ApiSystem::getInstance()->enableWifi(name, key, country); };
  378  #else
  379  	auto apply = [name, key, openNetwork](IGuiLoadingHandler*) { return openNetwork ? ApiSystem::getInstance()->connectOpenWifi(name) : ApiSystem::getInstance()->enableWifi(name, key); };
  380  #endif
  381  	window->pushGui(new GuiLoading<bool>(window, _("CONNECTING TO WI-FI"), apply,
  382  		[this, window, name, key, openNetwork](bool ok)
  383  		{
  384  			mWaitingLoad = false;
  385  			if (!ok)
  386  			{
  387  				LOG(LogWarning) << "wifi picker: could not connect to " << name;
  388  				window->pushGui(new GuiMsgBox(window,
  389  					Utils::String::format(_("COULDN'T CONNECT TO %s.").c_str(), name.c_str()) + "\n\n" + (openNetwork ? _("REFRESH THE NETWORK LIST AND TRY AGAIN.") : _("CHECK THE KEY AND TRY AGAIN.")), _("OK")));
  390  				return;
  391  			}
  392  			SystemConf::getInstance()->set("wifi.ssid", name);
  393  			SystemConf::getInstance()->set("wifi.key", key);
  394  			SystemConf::getInstance()->saveSystemConf();
  395  			joined(name);
  396  		}));
  397  }
  398  
  399  // The picker's job is done: the toast says so over whatever the page
  400  // returns to, and the page that opened the picker rebuilds to read the
  401  // connection back. The callback is copied out first -- it belongs to that
  402  // page, and this component is gone before it runs.
  403  void GuiWifi::joined(const std::string& name)
  404  {
  405  	Window* window = mWindow;
  406  	auto onJoined = mOnJoined;
  407  	// <glyph> <subject> : <outcome>, one space after the glyph, as every
  408  	// toast (#308 F-WF-08); CONNECTED is the row's word for the same fact.
```


## es-app/src/guis/GuiWifi.cpp @ 16dbac5211: lines 522-593 (excerpt of 607)

```text
  522  		if (worker->thread.joinable())
  523  			worker->thread.join();
  524  		worker->scan.reset();
  525  		mScan.reset();
  526  	}
  527  	const bool reused = mScan != nullptr;
  528  	if (!mScan)
  529  	{
  530  		mScan = std::make_shared<Scan>();
  531  		worker->scan = mScan;
  532  		auto scan = mScan;
  533  		try
  534  		{
  535  			worker->thread = std::thread([scan, rescan]
  536  			{
  537  				try
  538  				{
  539  					Answer answer;
  540  					const auto range = WifiScanProcess::read({"wifictl", rescan ? "scanlist" : "list"}, std::chrono::seconds(rescan ? 45 : 30), &scan->cancelled);
  541  					answer.inRangeKnown = range.code == 0;
  542  					answer.inRange = range.lines;
  543  
  544  					// Match ApiSystem's saved/current protocol, but reject signal
  545  					// and read failures too. No singleton or GUI is worker-owned.
  546  					if (!scan->cancelled.load(std::memory_order_acquire))
  547  					{
  548  						const auto saved = WifiScanProcess::read({"wifictl", "saved", "--ssid"}, std::chrono::seconds(15), &scan->cancelled);
  549  						answer.savedKnown = saved.code == 0;
  550  						if (answer.savedKnown)
  551  							for (const auto& line : saved.lines)
  552  							{
  553  								WifiText::SavedNetwork network;
  554  								if (!WifiText::parseSavedDetailsLine(line, network))
  555  								{
  556  									answer.savedKnown = false;
  557  									break;
  558  								}
  559  								answer.saved.push_back(network);
  560  							}
  561  						if (!answer.savedKnown)
  562  							answer.saved.clear();
  563  					}
  564  
  565  					if (!scan->cancelled.load(std::memory_order_acquire))
  566  					{
  567  						const auto current = WifiScanProcess::read({"wifictl", "current"}, std::chrono::seconds(10), &scan->cancelled);
  568  						answer.current = WifiText::parseCurrent(current.lines);
  569  						answer.currentKnown = (current.code == 0 && !answer.current.empty()) || current.code == 1;
  570  						if (current.code != 0)
  571  							answer.current.clear();
  572  					}
  573  					scan->answer = std::move(answer);
  574  				}
  575  				catch (...)
  576  				{
  577  					// The default answer is unknown, not a successful empty scan.
  578  					LOG(LogWarning) << "wifi picker: scan worker failed";
  579  				}
  580  				LOG(LogInfo) << "wifi picker: scan worker finished";
  581  				scan->ready.store(true, std::memory_order_release);
  582  			});
  583  		}
  584  		catch (const std::exception&)
  585  		{
  586  			LOG(LogWarning) << "wifi picker: could not start scan worker";
  587  			mScan->ready.store(true, std::memory_order_release);
  588  		}
  589  	}
  590  
  591  	if (mMenu.getList()->getScrollingVelocity() != 0)
  592  		mMenu.getList()->stopScrolling();
  593  	auto transform = Transform4x4f::Identity();
```


## es-app/src/scrapers/ScreenScraper.cpp @ 16dbac5211: lines 19-53 (excerpt of 1092)

```text
   19  #include <cstring>
   20  #include <thread>
   21  
   22  // bezel-16-9 
   23  // bezel-4-3
   24  
   25  using namespace PlatformIds;
   26  
   27  #if defined(SCREENSCRAPER_DEV_LOGIN) || defined(SCREENSCRAPER_RUNTIME_DEV_LOGIN)
   28  
   29  // A compiled developer pair takes precedence. Runtime-only builds read it
   30  // from settings under SCRAPER > ACCOUNTS (#64); normal distribution builds
   31  // supply it at build time and hide those developer rows (#566). Callers check
   32  // for empty and say what is missing rather than letting the API answer with
   33  // a login error.
   34  std::string screenScraperDevLogin()
   35  {
   36  #if defined(SCREENSCRAPER_DEV_LOGIN)
   37  	return SCREENSCRAPER_DEV_LOGIN;
   38  #else
   39  	const std::string id = Settings::getInstance()->getString("ScreenScraperDevId");
   40  	const std::string pass = Settings::getInstance()->getString("ScreenScraperDevPass");
   41  	if (id.empty() || pass.empty())
   42  		return "";
   43  	return "devid=" + HttpReq::urlEncode(id) + "&devpassword=*** + HttpReq::urlEncode(pass);
   44  #endif
   45  }
   46  
   47  /**
   48  	List of systems and thein IDs from
   49  	https://www.screenscraper.fr/api/systemesListe.php?devid=xxx&devpassword=***
   50  **/
   51  const std::map<PlatformId, unsigned short> screenscraper_platformid_map{
   52  	{ THREEDO, 29 },
   53  	{ ACTIONMAX, 81 },
```


## es-app/src/scrapers/ScreenScraper.cpp @ 16dbac5211: lines 257-338 (excerpt of 1092)

```text
  257  
  258  	for (auto platform : platforms)
  259  		if (screenscraper_platformid_map.find(platform) != screenscraper_platformid_map.cend())
  260  			return true;
  261  
  262  	return false;
  263  }
  264  
  265  void ScreenScraperScraper::generateRequests(const ScraperSearchParams& params,
  266  	std::queue<std::unique_ptr<ScraperRequest>>& requests,
  267  	std::vector<ScraperSearchResult>& results)
  268  {
  269  	std::string path;
  270  
  271  	ScreenScraperRequest::ScreenScraperConfig ssConfig;
  272  
  273  	// FCA Fix for names override not working on Retropie
  274  	if (params.nameOverride.length() == 0)
  275  	{
  276  		if (Utils::FileSystem::isDirectory(params.game->getPath()))
  277  			path = ssConfig.getGameSearchUrl(params.game->getDisplayName());
  278  		else 
  279  			path = ssConfig.getGameSearchUrl(params.game->getFileName());
  280  
  281  		path += "&romtype=rom";
  282  
  283  		std::string fileNameToHash = params.game->getFullPath();
  284  		auto length = Utils::FileSystem::getFileSize(fileNameToHash);
  285  
  286  		if (length > 1024 * 1024 && !params.game->getMetadata(MetaDataId::Md5).empty()) // 1Mb
  287  		{
  288  			path += "&md5=" + Utils::String::toUpper(params.game->getMetadata(MetaDataId::Md5));
  289  
  290  			if (!params.game->getMetadata(MetaDataId::Crc32).empty())
  291  				path += "&crc=" + Utils::String::toUpper(params.game->getMetadata(MetaDataId::Crc32));
  292  		}
  293  		else
  294  		{
  295  			if (params.game->hasContentFiles() && Utils::String::toLower(Utils::FileSystem::getExtension(fileNameToHash)) == ".m3u")
  296  			{
  297  				auto content = params.game->getContentFiles();
  298  				if (content.size())
  299  				{
  300  					fileNameToHash = (*content.begin());
  301  					length = Utils::FileSystem::getFileSize(fileNameToHash);
  302  				}
  303  			}
  304  
  305  			// Use md5 to search scrapped game
  306  			if (length > 0 && length <= 131072 * 1024) // 128 Mb max
  307  			{		
  308  				std::string md5 = ApiSystem::getInstance()->getMD5(fileNameToHash, params.system->shouldExtractHashesFromArchives());
  309  				if (!md5.empty())
  310  				{
  311  					params.game->setMetadata(MetaDataId::Md5, md5);
  312  					path += "&md5=" + Utils::String::toUpper(md5);
  313  
  314  					std::string crc = params.game->getMetadata(MetaDataId::Crc32);
  315  					if (!crc.empty())
  316  						path += "&crc=" + Utils::String::toUpper(params.game->getMetadata(MetaDataId::Crc32));
  317  				}
  318  			}
  319  		}	
  320  		
  321  		path += "&romtaille=" + std::to_string(length);
  322  	}
  323  	else
  324  	{
  325  		std::string name = Utils::String::replace(params.nameOverride, "_", " ");
  326  		name = Utils::String::replace(name, "-", " ");		
  327  
  328  		path = ssConfig.getGameSearchUrl(name, true);
  329  	}
  330  
  331  	auto& platforms = params.system->getPlatformIds();
  332  	std::vector<unsigned short> p_ids;
  333  
  334  	// Get the IDs of each platform from the ScreenScraper list
  335  	for (auto platformIt = platforms.cbegin(); platformIt != platforms.cend(); platformIt++)
  336  	{
  337  		auto mapIt = screenscraper_platformid_map.find(*platformIt);
  338  		if (mapIt != screenscraper_platformid_map.cend())
```


## es-app/src/scrapers/ScreenScraper.cpp @ 16dbac5211: lines 692-738 (excerpt of 1092)

```text
  692  			ss << ratingVal;
  693  			result.mdl.set(MetaDataId::Rating, ss.str());
  694  		}
  695  		else 
  696  			result.mdl.set(MetaDataId::Rating, "-1");
  697  
  698  		if (Settings::getInstance()->getBool("ScrapePadToKey") && game.child("sp2kcfg"))
  699  			result.p2k = game.child("sp2kcfg").text().get();
  700  
  701  		// Media super-node
  702  		pugi::xml_node media_list = game.child("medias");
  703  
  704  		if (media_list)
  705  		{
  706  			// ScraperRegion applies only to medias -> Import into romlang during findMedia(), as it's searched first
  707  			std::string regionOverride = Settings::getInstance()->getString("ScraperRegion");
  708  			if (!regionOverride.empty())
  709  			{
  710  				region = romlang;
  711  				romlang = regionOverride;
  712  			}
  713  
  714  			std::vector<std::string> ripList = getRipList(Settings::getInstance()->getString("ScrapperImageSrc"));
  715  			if (!ripList.empty())
  716  			{
  717  				pugi::xml_node art = findMedia(media_list, ripList, romlang, region);
  718  				if (art)
  719  				{
  720  					// Sending a 'softname' containing space will make the image URLs returned by the API also contain the space. 
  721  					//  Escape any spaces in the URL here
  722  					result.urls[MetaDataId::Image] = ScraperSearchItem(ensureUrl(art.text().get()), art.attribute("format") ? "." + std::string(art.attribute("format").value()) : "");
  723  
  724  					// Ask for the same image, but with a smaller size, for the thumbnail displayed during scraping
  725  					// result.urls[MetaDataId::Thumbnail] = imageUrl + "&maxheight=250";
  726  				}
  727  				else
  728  					LOG(LogDebug) << "Failed to find media XML node for image";
  729  			}
  730  
  731  			if (!Settings::getInstance()->getString("ScrapperThumbSrc").empty() &&
  732  				Settings::getInstance()->getString("ScrapperThumbSrc") != Settings::getInstance()->getString("ScrapperImageSrc"))
  733  			{
  734  				ripList = getRipList(Settings::getInstance()->getString("ScrapperThumbSrc"));
  735  				if (!ripList.empty())
  736  				{
  737  					pugi::xml_node art = findMedia(media_list, ripList, romlang, region);
  738  					if (art)
```


## es-app/src/scrapers/ScreenScraper.cpp @ 16dbac5211: lines 849-936 (excerpt of 1092)

```text
  849  		}
  850  
  851  		out_results.push_back(result);
  852  	} // game
  853  
  854  	LOG(LogDebug) << "ScreenScraperRequest::processGame <<";
  855  }
  856  
  857  std::string ScreenScraperRequest::ScreenScraperConfig::getGameSearchUrl(const std::string gameName, bool jeuRecherche) const
  858  {	
  859  	std::string ret = API_URL_BASE
  860  		+ "/jeuInfos.php?" + screenScraperDevLogin() +
  861  		+ "&softname=" + HttpReq::urlEncode(VERSIONED_SOFT_NAME)
  862  		+ "&output=xml"
  863  		+ "&romnom=" + HttpReq::urlEncode(gameName);
  864  
  865  	if (jeuRecherche)
  866  	{
  867  		ret = std::string(API_URL_BASE)
  868  			+ "/jeuRecherche.php?" + screenScraperDevLogin() +
  869  			+ "&softname=" + HttpReq::urlEncode(VERSIONED_SOFT_NAME)
  870  			+ "&output=xml"
  871  			+ "&recherche=" + HttpReq::urlEncode(gameName);
  872  	}
  873  
  874  	std::string user = Settings::getInstance()->getString("ScreenScraperUser");
  875  	std::string pass = Settings::getInstance()->getString("ScreenScraperPass");
  876  
  877  	if (!user.empty() && !pass.empty())
  878  		ret = ret + "&ssid=" + HttpReq::urlEncode(user) + "&sspassword=*** + HttpReq::urlEncode(pass);
  879  
  880  	return ret;
  881  }
  882  
  883  std::string ScreenScraperRequest::ScreenScraperConfig::getUserInfoUrl() const
  884  {
  885  	std::string ret = API_URL_BASE
  886  		+ "/ssuserInfos.php?" + screenScraperDevLogin() +
  887  		+ "&softname=" + HttpReq::urlEncode(VERSIONED_SOFT_NAME)
  888  		+ "&output=xml";
  889  
  890  	std::string user = Settings::getInstance()->getString("ScreenScraperUser");
  891  	std::string pass = Settings::getInstance()->getString("ScreenScraperPass");
  892  
  893  	if (!user.empty() && !pass.empty())
  894  		ret = ret + "&ssid=" + HttpReq::urlEncode(user) + "&sspassword=*** + HttpReq::urlEncode(pass);
  895  
  896  	return ret;
  897  }
  898  
  899  
  900  std::string ScreenScraperRequest::ensureUrl(const std::string& url)
  901  {
  902  	std::string ret = Utils::String::replace(
  903  		Utils::String::replace(url, " ", "%20"),
  904  		"#screenscraperserveur#", "https://www.screenscraper.fr/");
  905  
  906  	if (Settings::getInstance()->getBool("FastScrap"))
  907  	{
  908  		Utils::Uri uri(url);
  909  
  910  		auto gameid = uri.arguments["jeuid"];
  911  		auto systemeid = uri.arguments["systemeid"];
  912  		auto media = uri.arguments["media"];
  913  
  914  		if (!gameid.empty() && !systemeid.empty() && !media.empty())
  915  		{
  916  			auto region = Utils::String::extractString(media, "(", ")", true);
  917  			media = Utils::String::replace(media, region, "");
  918  			region = Utils::String::extractString(region, "(", ")", false);
  919  
  920  			if (media == "video" || media == "video-normalized")
  921  				ret = "https://www.screenscraper.fr/medias/" + systemeid + "/" + gameid + "/" + media + ".mp4";
  922  			else if (media != "manuel" && media != "map")
  923  				ret = "https://www.screenscraper.fr/image.php?gameid=" + gameid + "&media=" + media + "&hd=0&region=" + region + "&num=&version=&maxwidth=1920&maxheight=1080";
  924  		}
  925  	}
  926  
  927  	return ret;
  928  }
  929  
  930  ScreenScraperUser ScreenScraperRequest::processUserInfo(const pugi::xml_document& xmldoc)
  931  {
  932  	LOG(LogDebug) << "ScreenScraperRequest::processUserInfo >>";
  933  
  934  	ScreenScraperUser user;
  935  
  936  	pugi::xml_node data = xmldoc.child("Data");
```


## es-app/src/scrapers/ScreenScraper.cpp @ 16dbac5211: lines 968-1092 (excerpt of 1092)

```text
  968  // asked with a bad developer pair together with an account it blames the
  969  // account ("Verifier les identifiants utilisateurs"), while asked with the
  970  // pair alone it blames the pair ("Verifier vos identifiants developpeur").
  971  // EmulationStation used to put that body on screen as it came. So: the body
  972  // goes to the log; a login failure is told apart by one call with the pair
  973  // alone -- made only after a failure, so a scrape that starts makes no
  974  // extra request -- and the screen gives recovery guidance for this build's
  975  // credential source. No code on screen: it is in the log (D-UI-028).
  976  static std::string screenScraperFailureMessage(HttpReq& req, const ScreenScraperRequest::ScreenScraperConfig& config)
  977  {
  978  	const int status = req.status();
  979  	const std::string body = Utils::String::trim(Utils::String::removeHtmlTags(req.getErrorMsg()));
  980  	LOG(LogError) << "ScreenScraper refused the user-info request: HTTP " << status << ": " << body;
  981  	const std::string lower = Utils::String::toLower(body);
  982  
  983  	// No answer at all -- no route, no DNS, a timeout, a cut link: curl got
  984  	// no HTTP status, and the body is curl's own sentence, which the tests
  985  	// below would read as the server's ("Couldn't resolve host" used to come
  986  	// out as SCREENSCRAPER ANSWERED WITH AN ERROR). Say the player is
  987  	// offline and stop; no credential is named, none was looked at
  988  	// (#151 PL-07).
  989  	if (status == HttpReq::REQ_IO_ERROR || status == HttpReq::REQ_IN_PROGRESS)
  990  		return _("YOU'RE NOT ONLINE. TRY AGAIN WHEN YOU ARE.");
  991  
  992  	// The status is the one thing the API says in a form a program can
  993  	// read; HttpReq names every code it documents. Only 403 covers both
  994  	// credentials, and on this endpoint its body always says "utilisateurs"
  995  	// -- with a bad pair, with no pair at all -- so the body cannot say
  996  	// which; the probe below can.
  997  	switch (status)
  998  	{
  999  	case HttpReq::REQ_401_FORBIDDEN:
 1000  		return _("SCREENSCRAPER IS OPEN TO ITS MEMBERS ONLY RIGHT NOW. TRY AGAIN LATER.");
 1001  	case HttpReq::REQ_426_SERVERMAINTENANCE:
 1002  		return _("SCREENSCRAPER IS DOWN FOR MAINTENANCE. TRY AGAIN LATER.");
 1003  	case HttpReq::REQ_426_BLACKLISTED:
 1004  		return _("SCREENSCRAPER HAS BLOCKED THIS VERSION OF THE SCRAPER.");
 1005  	case HttpReq::REQ_429_TOOMANYREQUESTS:
 1006  		return _("SCREENSCRAPER IS BUSY. TRY AGAIN IN A MINUTE.");
 1007  	case HttpReq::REQ_430_TOOMANYSCRAPS:
 1008  		return _("YOU HAVE REACHED TODAY'S SCREENSCRAPER QUOTA. TRY AGAIN TOMORROW.");
 1009  	case HttpReq::REQ_430_TOOMANYFAILURES:
 1010  		return _("TOO MANY FAILED SCREENSCRAPER REQUESTS TODAY. TRY AGAIN TOMORROW.");
 1011  	case HttpReq::REQ_403_BADLOGIN:
 1012  		break;
 1013  	default:
 1014  		if (lower.find("maintenance") != std::string::npos || lower.find("ferm") != std::string::npos)
 1015  			return _("SCREENSCRAPER IS DOWN FOR MAINTENANCE. TRY AGAIN LATER.");
 1016  		if (lower.find("identifiant") == std::string::npos && lower.find("login") == std::string::npos)
 1017  			return _("SCREENSCRAPER ANSWERED WITH AN ERROR. TRY AGAIN LATER.");
 1018  		break;
 1019  	}
 1020  
 1021  	// The pair alone, first. A rejected pair answers 200 with a sentence,
 1022  	// not XML; an accepted one lists the systems with or without an account
 1023  	// (tested with the public JELOS pair, 2026-09-13: systemesListe.php
 1024  	// answers the pair alone with 200 XML while ssuserInfos.php gives the
 1025  	// same pair 403). So the probe settles the pair before the account is
 1026  	// looked at. It used to run only once an account was set, and a player
 1027  	// with a mistyped pair and no account was told to add an account, added
 1028  	// one, and failed again on the pair -- two failures where one would do
 1029  	// (#151 PL-06).
 1030  	HttpReq probe(config.API_URL_BASE + "/systemesListe.php?" + screenScraperDevLogin()
 1031  		+ "&softname=" + HttpReq::urlEncode(VERSIONED_SOFT_NAME) + "&output=xml");
 1032  	probe.wait();
 1033  	// Three answers, not two: accepted (200 and XML), rejected (200 and a
 1034  	// sentence), and nothing worth reading (a timeout, a 429, a maintenance
 1035  	// page, a link that dropped between the two requests). Only the second
 1036  	// blames the pair. The third used to, and sent a player whose link had
 1037  	// just gone to check a password that was fine (#151 PL-07).
 1038  	enum { PairAccepted, PairRejected, PairUnknown } pair = PairUnknown;
 1039  	if (probe.status() == HttpReq::REQ_SUCCESS)
 1040  		pair = Utils::String::trim(probe.getContent()).find("<?xml") == 0 ? PairAccepted : PairRejected;
 1041  	LOG(LogInfo) << "ScreenScraper developer pair alone: HTTP " << probe.status()
 1042  		<< (pair == PairAccepted ? ", accepted" : pair == PairRejected ? ", rejected" : ", no usable answer");
 1043  	if (pair == PairUnknown)
 1044  		return _("COULDN'T REACH SCREENSCRAPER. TRY AGAIN.");
 1045  	if (pair == PairRejected)
 1046  	{
 1047  #if defined(SCREENSCRAPER_DEV_LOGIN)
 1048  		return _("SCREENSCRAPER REJECTED THIS SYSTEM'S ACCESS.\nCHECK FOR A SYSTEM UPDATE OR REPORT THE PROBLEM.");
 1049  #else
 1050  		return _("SCREENSCRAPER REJECTED THE DEVELOPER ID OR PASSWORD.\nCHECK THEM UNDER SCRAPER > ACCOUNTS.");
 1051  #endif
 1052  	}
 1053  
 1054  	// The pair is fine and the API still refused: it needs an account on
 1055  	// this request and on every game request, so with none configured the
 1056  	// account is what is missing. Say that, rather than that a password
 1057  	// they never typed was rejected.
 1058  	if (Settings::getInstance()->getString("ScreenScraperUser").empty() || Settings::getInstance()->getString("ScreenScraperPass").empty())
 1059  		return _("SCREENSCRAPER NEEDS YOUR ACCOUNT TO SCRAPE.\nADD IT UNDER SCRAPER > ACCOUNTS.");
 1060  	return _("SCREENSCRAPER REJECTED YOUR USERNAME OR PASSWORD.\nCHECK THEM UNDER SCRAPER > ACCOUNTS.");
 1061  }
 1062  
 1063  int ScreenScraperScraper::getThreadCount(std::string &result)
 1064  {
 1065  	ScreenScraperRequest::ScreenScraperConfig ssConfig;
 1066  	std::string url = ssConfig.getUserInfoUrl();
 1067  	HttpReq httpreq(url);
 1068  	httpreq.wait();
 1069  	if (httpreq.status() != HttpReq::REQ_SUCCESS)
 1070  	{
 1071  		result = screenScraperFailureMessage(httpreq, ssConfig);
 1072  		return -1;
 1073  	}
 1074  
 1075  	auto content = httpreq.getContent();
 1076  
 1077  	pugi::xml_document doc;
 1078  	pugi::xml_parse_result parseResult = doc.load_string(content.c_str());
 1079  	if (parseResult)
 1080  	{
 1081  		auto userInfo = ScreenScraperRequest::processUserInfo(doc);
 1082  		
 1083  		// userInfo.maxRequestsPerMin / userInfo.maxthreads;
 1084  
 1085  		if (userInfo.maxthreads > 0)
 1086  			return userInfo.maxthreads;
 1087  	}	
 1088  
 1089  	return 1;
 1090  }
 1091  
 1092  #endif
```


## es-core/src/HttpReq.h @ 16dbac5211: lines 1-180 (excerpt of 180)

```text
    1  #pragma once
    2  #ifndef ES_CORE_HTTP_REQ_H
    3  #define ES_CORE_HTTP_REQ_H
    4  
    5  #include <curl/curl.h>
    6  #include <map>
    7  #include <sstream>
    8  #include <fstream>
    9  #include <string>
   10  #include <vector>
   11  #include <stdio.h>
   12  
   13  /* Usage:
   14   * HttpReq myRequest("www.google.com", "/index.html");
   15   * //for blocking behavior: while(myRequest.status() == HttpReq::REQ_IN_PROGRESS);
   16   * //for non-blocking behavior: check if(myRequest.status() != HttpReq::REQ_IN_PROGRESS) in some sort of update method
   17   * 
   18   * //once one of those completes, the request is ready
   19   * if(myRequest.status() != REQ_SUCCESS)
   20   * {
   21   *    //an error occurred
   22   *    LOG(LogError) << "HTTP request error - " << myRequest.getErrorMessage();
   23   *    return;
   24   * }
   25   *
   26   * std::string content = myRequest.getContent();
   27   * //process contents...
   28  */
   29  
   30  #define HTTP_REQ_USERAGENT "Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0"
   31  
   32  class HttpCookie
   33  {
   34  public:
   35  	std::string name;
   36  	std::string value;
   37  };
   38  
   39  class HttpCookieContainer
   40  {
   41  public:
   42  	std::vector<HttpCookie> cookies;
   43  };
   44  
   45  class HttpReqOptions
   46  {
   47  public:
   48  	HttpReqOptions() 
   49  	{
   50  		userAgent = HTTP_REQ_USERAGENT;
   51  		useCookieManager = true;
   52  		connectTimeout = 10000L;
   53  		timeout = 0L;
   54  		stallTimeout = 0L;
   55  	}
   56  
   57  	HttpReqOptions(const std::string& filename)
   58  	{
   59  		outputFilename = filename;
   60  		userAgent = HTTP_REQ_USERAGENT;
   61  		useCookieManager = true;
   62  		connectTimeout = 10000L;
   63  		timeout = 0L;
   64  		stallTimeout = 0L;
   65  	}
   66  
   67  	std::string outputFilename;
   68  	std::vector<std::string> customHeaders;
   69  	std::string dataToPost;
   70  	std::string userAgent;
   71  	// Client certificate files in .pem format
   72  	std::string clientCert, clientKey;
   73  
   74  	long connectTimeout;
   75  	// The whole request, connect included, in milliseconds; 0 (the default)
   76  	// leaves it unbounded, as every request was before. A caller asking a
   77  	// local service sets it, so a service that hangs cannot hold a page.
   78  	long timeout;
   79  	// Seconds a transfer may move no byte before it ends with an error; 0
   80  	// (the default) leaves a silent connection to TCP, which retries a
   81  	// dead peer for a quarter of an hour. For a request that may be long
   82  	// but must never be silent: the hash library's fetch on a pooled
   83  	// connection whose link had gone held the interface thread for twelve
   84  	// minutes on the VM (ROCKNIX fork #299), while a total bound would cut
   85  	// a slow but moving download.
   86  	long stallTimeout;
   87  	bool useCookieManager;
   88  };
   89  
   90  class HttpReq
   91  {
   92  public:
   93  	HttpReq(const std::string& url, HttpReqOptions* options = nullptr);
   94  	HttpReq(const std::string& url, const std::string& outputFilename);
   95  
   96  	~HttpReq();
   97  
   98  	enum Status
   99  	{
  100  		REQ_IN_PROGRESS = 0,
  101  		REQ_IO_ERROR	= 3,				
  102  		REQ_FILESTREAM_ERROR = 4,		
  103  
  104  		REQ_SUCCESS = 200,
  105  		REQ_400_BADREQUEST = 400,
  106  		REQ_401_FORBIDDEN = 401,
  107  		REQ_403_BADLOGIN = 403,
  108  		REQ_404_NOTFOUND = 404,
  109  		
  110  		REQ_426_SERVERMAINTENANCE = 423,
  111  		REQ_426_BLACKLISTED = 426,
  112  		REQ_429_TOOMANYREQUESTS = 429,
  113  
  114  		REQ_430_TOOMANYSCRAPS = 430,
  115  		REQ_430_TOOMANYFAILURES = 431,
  116  		REQ_500_INTERNALSERVERERROR = 500
  117  	};
  118  
  119  	Status status(); //process any received data and return the status afterwards
  120  
  121  	std::string getErrorMsg();
  122  
  123  	std::string getContent(); // mStatus must be REQ_SUCCESS
  124  
  125  	// int saveContent(const std::string filename, bool checkMedia = false);
  126  
  127  	static std::string urlEncode(const std::string &s);
  128  	static bool isUrl(const std::string& s);
  129  
  130  	int getPercent() { return mPercent; }
  131  	int64_t getPosition() { return mPosition; }
  132  
  133  	std::string getUrl() { return mUrl; }
  134  	std::string getFilePath() { return mFilePath; }	
  135  	std::map<std::string, std::string>& getResponseHeaders() { return mResponseHeaders; }
  136  	std::string getResponseHeader(const std::string& header);
  137  
  138  	bool wait();
  139  
  140  	static void resetCookies();
  141  
  142  private:
  143  	void performRequest(const std::string& url, HttpReqOptions* options);
  144  	void closeStream();
  145  
  146  	static size_t write_content(void* buff, size_t size, size_t nmemb, void* req_ptr);
  147  	static size_t header_callback(char *buffer, size_t size, size_t nitems, void *userdata);
  148  
  149  	//static int update_progress(void* req_ptr, double dlTotal, double dlNow, double ulTotal, double ulNow);
  150  
  151  	//god dammit libcurl why can't you have some way to check the status of an individual handle
  152  	//why do I have to handle ALL messages at once
  153  	static std::map<CURL*, HttpReq*> s_requests;
  154  
  155  	static CURLM* s_multi_handle;
  156  
  157  	void onError(const char* msg);
  158  
  159  	CURL* mHandle;
  160  
  161  	Status mStatus;
  162  
  163  	// string steam mode
  164  	std::stringstream mContent;
  165  
  166  	// file stream mode
  167  	std::string   mFilePath;
  168  	std::string   mTempStreamPath;	
  169  	FILE*		  mFile;	
  170  
  171  	std::string mErrorMsg;
  172  	std::string mUrl;
  173  
  174  	int mPercent;
  175  	int64_t mPosition;
  176  
  177  	std::map<std::string, std::string> mResponseHeaders;	
  178  };
  179  
  180  #endif // ES_CORE_HTTP_REQ_H
```


## es-core/src/Settings.h @ 16dbac5211: lines 132-165 (excerpt of 165)

```text
  132  	DEFINE_INT_SETTING(RecentlyScrappedFilter)
  133  
  134  	static Delegate<ISettingsChangedEvent> settingChanged;
  135  
  136  	const std::set<std::string>& getHiddenSystems() { return mHiddenSystems; }
  137  
  138  private:
  139  	static Settings* sInstance;
  140  	static bool sRecovered;
  141  
  142  	Settings();
  143  
  144  	//Clear everything and load default values.
  145  	void setDefaults();
  146  
  147  	std::map<std::string, bool> mBoolMap;
  148  	std::map<std::string, int> mIntMap;
  149  	std::map<std::string, float> mFloatMap;
  150  	std::map<std::string, std::string> mStringMap;
  151  
  152  	bool mWasChanged;
  153  
  154  	std::map<std::string, bool> mDefaultBoolMap;
  155  	std::map<std::string, int> mDefaultIntMap;
  156  	std::map<std::string, float> mDefaultFloatMap;
  157  	std::map<std::string, std::string> mDefaultStringMap;	
  158  
  159  	std::set<std::string> mHiddenSystems;
  160  
  161  	bool mLoaded;
  162  	void updateCachedSetting(const std::string& name);
  163  };
  164  
  165  #endif // ES_CORE_SETTINGS_H
```


## es-core/src/utils/StringUtil.cpp @ 16dbac5211: lines 418-452 (excerpt of 1706)

```text
  418  			const size_t len = strEnd - strBegin + 1;
  419  			if (strBegin == 0 && len == _string.length())
  420  				return _string;
  421  
  422  			return _string.substr(strBegin, strEnd - strBegin + 1);
  423  
  424  		} // trim
  425  
  426  		std::string shellQuote(const std::string& _string)
  427  		{
  428  			// Wrap the value in single quotes so it reaches the command as one
  429  			// literal argument. Inside single quotes the shell expands nothing,
  430  			// so $, `, \, " and whitespace survive untouched; a single quote
  431  			// itself has to leave the quoted run, be escaped, and re-enter it.
  432  			std::string quoted = "'";
  433  
  434  			for (auto character : _string)
  435  			{
  436  				if (character == '\'')
  437  					quoted += "'\\''";
  438  				else
  439  					quoted += character;
  440  			}
  441  
  442  			return quoted + "'";
  443  
  444  		} // shellQuote
  445  
  446  		// ------------------------------------------------------------ maskSecrets
  447  		//
  448  		// A credential's value never reaches a log (D-INFRA-011): every command
  449  		// line, URL or query EmulationStation logs goes through here first, at
  450  		// every level (fork #177). The key or flag stays and the value reads
  451  		// <redacted>, so the line still says what ran; an empty value stays
  452  		// empty, since whether a credential is set may be shown and only what it
```


## es-core/src/utils/StringUtil.cpp @ 16dbac5211: lines 497-528 (excerpt of 1706)

```text
  497  		{
  498  			return maskIsSpace(c) || c == '&' || c == ';' || c == '|' || c == '\'' || c == '"';
  499  		}
  500  
  501  		static std::string maskLower(const std::string& word)
  502  		{
  503  			std::string lower = word;
  504  			for (auto& c : lower)
  505  				if (c >= 'A' && c <= 'Z')
  506  					c = (char)(c - 'A' + 'a');
  507  			return lower;
  508  		}
  509  
  510  		// Does a lower-cased name end in a word that means "credential"?
  511  		static bool maskIsSecretName(const std::string& lower)
  512  		{
  513  			static const char* const words[] = { "password", "pass", "token", "key", "secret", "psk", "pin" };
  514  			for (const char* word : words)
  515  			{
  516  				const size_t len = strlen(word);
  517  				if (lower.size() >= len && lower.compare(lower.size() - len, len, word) == 0)
  518  					return true;
  519  			}
  520  			return false;
  521  		}
  522  
  523  		// What quote `pos` sits inside, reading the line from its start as the
  524  		// shell would: 0 at the top level, else the quote character.
  525  		static char maskQuoteAt(const std::string& s, size_t pos)
  526  		{
  527  			char quote = 0;
  528  			for (size_t i = 0; i < pos && i < s.size(); ++i)
```


## es-core/src/utils/StringUtil.cpp @ 16dbac5211: lines 707-811 (excerpt of 1706)

```text
  707  
  708  		static size_t maskCopySpaces(const std::string& s, size_t pos, std::string& out)
  709  		{
  710  			while (pos < s.size() && maskIsSpace(s[pos]))
  711  				out += s[pos++];
  712  			return pos;
  713  		}
  714  
  715  		std::string maskSecrets(const std::string& _string)
  716  		{
  717  			const std::string& s = _string;
  718  			std::string out;
  719  			out.reserve(s.size());
  720  
  721  			std::string previous; // the word before this one, lower-cased
  722  			size_t i = 0;
  723  			while (i < s.size())
  724  			{
  725  				if (!maskIsWordChar(s[i]))
  726  				{
  727  					out += s[i++];
  728  					continue;
  729  				}
  730  
  731  				const size_t start = i;
  732  				while (i < s.size() && maskIsWordChar(s[i]))
  733  					++i;
  734  
  735  				const std::string word = maskLower(s.substr(start, i - start));
  736  				out.append(s, start, i - start);
  737  
  738  				// name=value, or a one-letter RetroAchievements key after ? or &
  739  				const bool queryKey = (word == "y" || word == "t" || word == "p")
  740  					&& start > 0 && (s[start - 1] == '?' || s[start - 1] == '&');
  741  
  742  				if (i < s.size() && s[i] == '=' && (queryKey || maskIsSecretName(word)))
  743  				{
  744  					out += '=';
  745  					++i;
  746  					i = maskAppendValue(s, i, maskValueEnd(s, i), out);
  747  					previous = word;
  748  					continue;
  749  				}
  750  
  751  				if (i < s.size() && maskIsSpace(s[i]))
  752  				{
  753  					if (word == "setrootpass")
  754  					{
  755  						i = maskCopySpaces(s, i, out);
  756  						size_t end = s.size();
  757  						while (end > i && maskIsSpace(s[end - 1]))
  758  							--end;
  759  						i = maskAppendValue(s, i, end, out);
  760  						previous = word;
  761  						continue;
  762  					}
  763  
  764  					if (word == "wifictl")
  765  					{
  766  						size_t j = i;
  767  						while (j < s.size() && maskIsSpace(s[j]))
  768  							++j;
  769  						size_t k = j;
  770  						while (k < s.size() && maskIsWordChar(s[k]))
  771  							++k;
  772  
  773  						const std::string sub = maskLower(s.substr(j, k - j));
  774  						if (sub == "connect" || sub == "enable")
  775  						{
  776  							out.append(s, i, k - i);
  777  							i = maskCopySpaces(s, k, out);
  778  							const size_t ssidEnd = maskValueEnd(s, i); // the SSID is no secret
  779  							out.append(s, i, ssidEnd - i);
  780  							i = maskCopySpaces(s, ssidEnd, out);
  781  							i = maskAppendValue(s, i, maskValueEnd(s, i), out);
  782  							previous = sub;
  783  							continue;
  784  						}
  785  					}
  786  
  787  					const bool flag = word.size() > 1 && word[0] == '-'
  788  						&& ((word == "-p" && previous != "mkdir") || (word != "--key" && maskIsSecretName(word)));
  789  					if (flag)
  790  					{
  791  						i = maskCopySpaces(s, i, out);
  792  						i = maskAppendValue(s, i, maskValueEnd(s, i), out);
  793  						previous = word;
  794  						continue;
  795  					}
  796  				}
  797  
  798  				previous = word;
  799  			}
  800  
  801  			return out;
  802  
  803  		} // maskSecrets
  804  
  805  		std::string replace(const std::string& _string, const std::string& _replace, const std::string& _with)
  806  		{
  807  			if (_replace.empty())
  808  				return _string;
  809  
  810  			std::string string = _string;
  811  			
```


## es-app/src/scrapers/Scraper.cpp @ 16dbac5211: lines 417-468 (excerpt of 813)

```text
  417  
  418  		std::string suffix = "image";
  419  		switch (url.first)
  420  		{
  421  		case MetaDataId::Video: suffix = "video";  resize = false; break;
  422  		case MetaDataId::FanArt: suffix = "fanart"; resize = false; break;
  423  		case MetaDataId::BoxBack: suffix = "boxback"; resize = false; break;
  424  		case MetaDataId::BoxArt: suffix = "box"; resize = false; break;
  425  		case MetaDataId::Wheel: suffix = "wheel"; resize = false; break;		
  426  		case MetaDataId::TitleShot: suffix = "titleshot"; break;
  427  		case MetaDataId::Manual: suffix = "manual"; resize = false;  break;
  428  		case MetaDataId::Magazine: suffix = "magazine"; resize = false;  break;
  429  		case MetaDataId::Map: suffix = "map"; resize = false; break;
  430  		case MetaDataId::Cartridge: suffix = "cartridge"; break;
  431  		case MetaDataId::Bezel: suffix = "bezel"; resize = false; break;
  432  		}
  433  
  434  		auto ext = url.second.format;
  435  		if (ext.empty())
  436  			ext = Utils::FileSystem::getExtension(url.second.url);
  437  
  438  		std::string resourcePath = Scraper::getSaveAsPath(search.game, url.first, ext);
  439  
  440  		if (!overWriteMedias && Utils::FileSystem::exists(resourcePath))
  441  		{
  442  			mResult.mdl.set(url.first, resourcePath);
  443  			if (mResult.urls.find(url.first) != mResult.urls.cend())
  444  				mResult.urls[url.first].url = "";
  445  
  446  			continue;
  447  		}
  448  
  449  		mFuncs.push_back(new ResolvePair(
  450  			[this, url, resourcePath, resize] 
  451  			{ 
  452  				return downloadImageAsync(url.second.url, resourcePath, resize); 
  453  			},
  454  			[this, url](ImageDownloadHandle* result)
  455  			{
  456  				auto finalFile = result->getImageFileName();
  457  
  458  				if (Utils::FileSystem::getFileSize(finalFile) > 0)
  459  					mResult.mdl.set(url.first, finalFile);
  460  
  461  				if (mResult.urls.find(url.first) != mResult.urls.cend())
  462  					mResult.urls[url.first].url = "";
  463  			},
  464  			suffix, result.mdl.getName()));
  465  	}
  466  
  467  	auto it = mFuncs.cbegin();
  468  	if (it == mFuncs.cend())
```


## es-app/src/scrapers/Scraper.cpp @ 16dbac5211: lines 512-708 (excerpt of 813)

```text
  512  			mSource = (*next)->source;
  513  			mCurrentItem = (*next)->name;
  514  			(*next)->Run();
  515  		}
  516  	}
  517  	
  518  	if(mFuncs.empty())
  519  		setStatus(ASYNC_DONE);
  520  }
  521  
  522  std::unique_ptr<ImageDownloadHandle> MDResolveHandle::downloadImageAsync(const std::string& url, const std::string& saveAs, bool resize)
  523  {
  524  	LOG(LogDebug) << "downloadImageAsync : " << Utils::String::maskSecrets(url) << " -> " << saveAs;
  525  
  526  	return std::unique_ptr<ImageDownloadHandle>(new ImageDownloadHandle(url, saveAs, 
  527  		resize ? Settings::getInstance()->getInt("ScraperResizeWidth") : 0,
  528  		resize ? Settings::getInstance()->getInt("ScraperResizeHeight") : 0));
  529  }
  530  
  531  ImageDownloadHandle::ImageDownloadHandle(const std::string& url, const std::string& path, int maxWidth, int maxHeight) : 
  532  	mSavePath(path), mMaxWidth(maxWidth), mMaxHeight(maxHeight)
  533  {
  534  	mRetryCount = 0;
  535  	mOverQuotaPendingTime = 0;
  536  	mOverQuotaRetryDelay = OVERQUOTA_RETRY_DELAY;
  537  	mOverQuotaRetryCount = OVERQUOTA_RETRY_COUNT;
  538  
  539  	HttpReqOptions options;
  540  	options.outputFilename = path;
  541  
  542  	if (url.find("screenscraper") != std::string::npos && url.find("/medias/") != std::string::npos)
  543  	{
  544  		auto splits = Utils::String::split(url, '/', true);
  545  		if (splits.size() > 1)
  546  			options.customHeaders.push_back("Referer: https://" + splits[1] + "/gameinfos.php?gameid=" + splits[splits.size() - 2] + "&action=onglet&zone=gameinfosmedias");
  547  	}
  548  
  549  	if (url.find("screenscraper") != std::string::npos && (path.find(".jpg") != std::string::npos || path.find(".png") != std::string::npos) && url.find("media=map") == std::string::npos)
  550  	{
  551  		Utils::Uri uri(url);
  552  
  553  		if (maxWidth > 0)
  554  		{
  555  			uri.arguments.set("maxwidth", std::to_string(maxWidth));
  556  			uri.arguments.set("maxheight", std::to_string(maxWidth));
  557  		}
  558  		else if (maxHeight > 0)
  559  		{
  560  			uri.arguments.set("maxwidth", std::to_string(maxHeight));
  561  			uri.arguments.set("maxheight", std::to_string(maxHeight));
  562  		}
  563  
  564  		mRequest = new HttpReq(uri.toString(), &options);
  565  	}
  566  	else
  567  		mRequest = new HttpReq(url, &options);
  568  }
  569  
  570  ImageDownloadHandle::~ImageDownloadHandle()
  571  {
  572  	delete mRequest;
  573  }
  574  
  575  int ImageDownloadHandle::getPercent()
  576  {
  577  	if (mRequest->status() == HttpReq::REQ_IN_PROGRESS)
  578  		return mRequest->getPercent();
  579  
  580  	return -1;
  581  }
  582  
  583  void ImageDownloadHandle::update()
  584  {
  585  	if (mOverQuotaPendingTime > 0)
  586  	{
  587  		int lastTime = SDL_GetTicks();
  588  		if (lastTime - mOverQuotaPendingTime > mOverQuotaRetryDelay)
  589  		{
  590  			mOverQuotaPendingTime = 0;
  591  
  592  			LOG(LogDebug) << "REQ_429_TOOMANYREQUESTS : Retrying";
  593  
  594  			std::string url = mRequest->getUrl();
  595  			delete mRequest;
  596  			mRequest = new HttpReq(url, mSavePath);
  597  		}
  598  
  599  		return;
  600  	}
  601  
  602  	HttpReq::Status status = mRequest->status();
  603  
  604  	if (status == HttpReq::REQ_IN_PROGRESS)
  605  		return;
  606  	
  607  	if (status == HttpReq::REQ_429_TOOMANYREQUESTS)
  608  	{
  609  		mRetryCount++;
  610  		if (mRetryCount >= mOverQuotaRetryCount)
  611  		{
  612  			setStatus(ASYNC_DONE); // Ignore error
  613  			return;
  614  		}
  615  
  616  		setStatus(ASYNC_IN_PROGRESS);
  617  
  618  		auto retryDelay = mRequest->getResponseHeader("Retry-After");
  619  		if (!retryDelay.empty())
  620  		{
  621  			mOverQuotaRetryCount = 1;
  622  			mOverQuotaRetryDelay = Utils::String::toInteger(retryDelay) * 1000;
  623  		}
  624  
  625  		mOverQuotaPendingTime = SDL_GetTicks();
  626  		LOG(LogDebug) << "REQ_429_TOOMANYREQUESTS : Retrying in " << mOverQuotaRetryDelay << " seconds";
  627  		return;
  628  	}
  629  
  630  	// Ignored errors
  631  	if (status == HttpReq::REQ_404_NOTFOUND || status == HttpReq::REQ_IO_ERROR)
  632  	{
  633  		setStatus(ASYNC_DONE);
  634  		return;
  635  	}
  636  
  637  	// Blocking errors
  638  	if (status != HttpReq::REQ_SUCCESS)
  639  	{
  640  		setError(status, Utils::String::removeHtmlTags(mRequest->getErrorMsg()));
  641  		return;
  642  	}
  643  
  644  	if (status == HttpReq::REQ_SUCCESS && mStatus == ASYNC_IN_PROGRESS)
  645  	{
  646  		std::string ext = Utils::String::toLower(Utils::FileSystem::getExtension(mSavePath));
  647  
  648  		// Make sure extension is the good one, according to the response 'Content-Type'
  649  		std::string contentType = mRequest->getResponseHeader("Content-Type");
  650  		if (!contentType.empty())
  651  		{
  652  			std::string trueExtension;
  653  			if (Utils::String::startsWith(contentType, "image/"))
  654  			{
  655  				trueExtension = "." + contentType.substr(6);
  656  				if (trueExtension == ".jpeg")
  657  					trueExtension = ".jpg";
  658  				else if (trueExtension == ".svg+xml")
  659  					trueExtension = ".svg";
  660  
  661  			}
  662  			else if (Utils::String::startsWith(contentType, "video/"))
  663  			{
  664  				trueExtension = "." + contentType.substr(6);
  665  				if (trueExtension == ".quicktime")
  666  					trueExtension = ".mov";
  667  			}
  668  
  669  			if (!trueExtension.empty() && trueExtension != ext)
  670  			{
  671  				auto newFileName = Utils::FileSystem::changeExtension(mSavePath, trueExtension);
  672  				if (Utils::FileSystem::renameFile(mSavePath, newFileName))
  673  				{
  674  					mSavePath = newFileName;
  675  					ext = trueExtension;
  676  				}
  677  			}
  678  		}
  679  
  680  		// It's an image ?
  681  		if (mSavePath.find("-fanart") == std::string::npos && mSavePath.find("-bezel") == std::string::npos && mSavePath.find("-map") == std::string::npos && (ext == ".jpg" || ext == ".jpeg" || ext == ".png" || ext == ".bmp" || ext == ".gif"))
  682  		{
  683  			try { resizeImage(mSavePath, mMaxWidth, mMaxHeight); }
  684  			catch(...) { }
  685  		}
  686  	}
  687  
  688  	setStatus(ASYNC_DONE);
  689  }
  690  
  691  //you can pass 0 for width or height to keep aspect ratio
  692  bool resizeImage(const std::string& path, int maxWidth, int maxHeight)
  693  {
  694  	// nothing to do
  695  	if(maxWidth == 0 && maxHeight == 0)
  696  		return true;
  697  
  698  	FREE_IMAGE_FORMAT format = FIF_UNKNOWN;
  699  	FIBITMAP* image = NULL;
  700  	
  701  	//detect the filetype
  702  #if WIN32
  703  	format = FreeImage_GetFileTypeU(Utils::String::convertToWideString(path).c_str(), 0);
  704  	if(format == FIF_UNKNOWN)
  705  		format = FreeImage_GetFIFFromFilenameU(Utils::String::convertToWideString(path).c_str());
  706  #else
  707  	format = FreeImage_GetFileType(path.c_str(), 0);
  708  	if(format == FIF_UNKNOWN)
```


## es-app/src/scrapers/Scraper.cpp @ 16dbac5211: lines 771-813 (excerpt of 813)

```text
  771  	FreeImage_Unload(imageRescaled);
  772  
  773  	if(!saved)
  774  		LOG(LogError) << "Failed to save resized image!";
  775  
  776  	return saved;
  777  }
  778  
  779  std::string Scraper::getSaveAsPath(FileData* game, const MetaDataId metadataId, const std::string& extension)
  780  {
  781  	std::string suffix = "image";
  782  	std::string folder = "images";
  783  
  784  	switch (metadataId)
  785  	{
  786  	case MetaDataId::Thumbnail: suffix = "thumb"; break;
  787  	case MetaDataId::Marquee: suffix = "marquee"; break;
  788  	case MetaDataId::Video: suffix = "video"; folder = "videos"; break;
  789  	case MetaDataId::FanArt: suffix = "fanart"; break;
  790  	case MetaDataId::BoxBack: suffix = "boxback"; break;
  791  	case MetaDataId::BoxArt: suffix = "box"; break;
  792  	case MetaDataId::Wheel: suffix = "wheel"; break;
  793  	case MetaDataId::TitleShot: suffix = "titleshot"; break;
  794  	case MetaDataId::Manual: suffix = "manual"; folder = "manuals";  break;
  795  	case MetaDataId::Magazine: suffix = "magazine"; folder = "magazines"; break;
  796  	case MetaDataId::Map: suffix = "map"; break;
  797  	case MetaDataId::Cartridge: suffix = "cartridge"; break;
  798  	case MetaDataId::Bezel: suffix = "bezel"; break;
  799  	}
  800  
  801  	auto system = game->getSourceFileData()->getSystem();
  802  
  803  	const std::string subdirectory = system->getName();
  804  	const std::string name = Utils::FileSystem::getStem(game->getPath()) + "-" + suffix;
  805  
  806  	std::string path = system->getRootFolder()->getPath() + "/" + folder + "/";
  807  
  808  	if(!Utils::FileSystem::exists(path))
  809  		Utils::FileSystem::createDirectory(path);
  810  
  811  	path += name + extension;
  812  	return path;
  813  }
```


## es-core/src/utils/FileSystemUtil.cpp @ 16dbac5211: lines 634-676 (excerpt of 1805)

```text
  634  				path.replace(offset, 1, "\\");
  635  
  636  			return path;
  637  #else
  638  			return _path;
  639  #endif
  640  		}
  641  
  642  		std::string getGenericPath(const std::string& _path)
  643  		{
  644  			if (_path.empty())
  645  				return _path;
  646  
  647  			std::string path   = _path;
  648  			size_t      offset = std::string::npos;
  649  
  650  			// remove "\\\\?\\"
  651  			if(path[0] == '\\' && (path.find("\\\\?\\")) == 0)
  652  				path.erase(0, 4);
  653  
  654  			// convert '\\' to '/'
  655  			while ((offset = path.find('\\')) != std::string::npos)
  656  				path[offset] = '/';// .replace(offset, 1, "/");
  657  
  658  			// remove double '/'
  659  			while((offset = path.find("//")) != std::string::npos)
  660  				path.erase(offset, 1);
  661  
  662  			// remove trailing '/'
  663  			while(path.length() && ((offset = path.find_last_of('/')) == (path.length() - 1)))
  664  				path.erase(offset, 1);
  665  
  666  			// return generic path
  667  			return path;
  668  		}
  669  
  670  		std::string getEscapedPath(const std::string& _path)
  671  		{
  672  			std::string path = getGenericPath(_path);
  673  
  674  #if defined(_WIN32)
  675  			// windows escapes stuff by just putting everything in quotes
  676  			return '"' + getPreferredPath(path) + '"';
```


## es-core/src/utils/FileSystemUtil.cpp @ 16dbac5211: lines 1051-1093 (excerpt of 1805)

```text
 1051  			FileCache::remove(path);
 1052  #if WIN32			
 1053  			return RemoveDirectoryW(Utils::String::convertToWideString(getPreferredPath(_path)).c_str());
 1054  #else
 1055  			return (rmdir(path.c_str()) == 0);
 1056  #endif
 1057  		}
 1058  
 1059  		bool removeFile(const std::string& _path)
 1060  		{
 1061  			std::string path = getGenericPath(_path);
 1062  
 1063  			// don't remove if it doesn't exists
 1064  			if (!exists(path, false))
 1065  				return true;
 1066  
 1067  			FileCache::remove(path);
 1068  #if WIN32			
 1069  			if (isDirectory(_path))
 1070  				return RemoveDirectoryW(Utils::String::convertToWideString(getPreferredPath(_path)).c_str());
 1071  						
 1072  			if (!DeleteFileW(Utils::String::convertToWideString(_path).c_str()))
 1073  			{
 1074  				SetFileAttributesW(Utils::String::convertToWideString(_path).c_str(), FILE_ATTRIBUTE_NORMAL);
 1075  				return DeleteFileW(Utils::String::convertToWideString(_path).c_str());
 1076  			}
 1077  
 1078  			return true;
 1079  #else
 1080  			if (isDirectory(_path))
 1081  				return (rmdir(path.c_str()) == 0);
 1082  
 1083  			// try to remove file
 1084  			return (unlink(path.c_str()) == 0);
 1085  #endif
 1086  
 1087  		} // removeFile
 1088  
 1089  		bool createDirectory(const std::string& _path)
 1090  		{
 1091  			std::string path = getGenericPath(_path);
 1092  
 1093  			// don't create if it already exists
```


## es-core/src/utils/FileSystemUtil.cpp @ 16dbac5211: lines 1421-1473 (excerpt of 1805)

```text
 1421  
 1422  			skipUtf8Bom(t);
 1423  
 1424  			std::stringstream buffer;
 1425  			buffer << t.rdbuf();
 1426  			return buffer.str();
 1427  		}
 1428  
 1429  		void writeAllText(const std::string& fileName, const std::string& text)
 1430  		{
 1431  #if defined(_WIN32)
 1432  			FILE* file = _wfopen(Utils::String::convertToWideString(fileName).c_str(), L"wb");
 1433  #else
 1434  			FILE* file = fopen(fileName.c_str(), "wb");
 1435  #endif
 1436  			if (file == nullptr)
 1437  				return;		
 1438  
 1439  			void* buffer = (void*) text.data();
 1440  			size_t size = text.size();
 1441  
 1442  			fwrite(buffer, 1, size, file);
 1443  			fclose(file);
 1444  
 1445  			FileCache::remove(getGenericPath(fileName));
 1446  		}
 1447  
 1448  		bool renameFile(const std::string& src, const std::string& dst, bool overWrite)
 1449  		{
 1450  			std::string path = getGenericPath(src);			
 1451  			if (!exists(path, false))
 1452  				return true;
 1453  
 1454  			if (overWrite && exists(dst, false))
 1455  				removeFile(dst);
 1456  
 1457  			FileCache::remove(path);
 1458  			FileCache::remove(dst);
 1459  
 1460  #if WIN32			
 1461  			return MoveFileW(Utils::String::convertToWideString(path).c_str(), Utils::String::convertToWideString(dst).c_str());
 1462  #else
 1463  			return std::rename(src.c_str(), dst.c_str()) == 0;
 1464  #endif
 1465  		}
 1466  
 1467  		bool copyFile(const std::string& src, const std::string& dst)
 1468  		{
 1469  			std::string path = getGenericPath(src);
 1470  			std::string pathD = getGenericPath(dst);
 1471  
 1472  			// don't remove if it doesn't exists
 1473  			if (!exists(path, false))
```


## es-core/src/components/TextEditComponent.cpp @ 16dbac5211: lines 60-102 (excerpt of 400)

```text
   60  	onTextChanged();
   61  }
   62  
   63  std::string TextEditComponent::getValue() const
   64  {
   65  	return mText;
   66  }
   67  
   68  void TextEditComponent::textInput(const char* text)
   69  {
   70  	if (mEditing)
   71  	{
   72  		mCursorRepeatDir = 0;
   73  		if (text[0] == '\b')
   74  		{
   75  			if (mCursor > 0)
   76  			{
   77  				size_t newCursor = Utils::String::prevCursor(mText, mCursor);
   78  				mText.erase(mText.begin() + newCursor, mText.begin() + mCursor);
   79  				mCursor = (unsigned int)newCursor;
   80  			}
   81  		}
   82  		else if (mCursor > 2 && Utils::String::isKorean(text) && Utils::String::isKorean(mText.substr(mCursor - 3, 3).c_str()))
   83  		{
   84  			Utils::String::koreanTextInput(text, mText, mCursor);
   85  		}
   86  		else {
   87  			mText.insert(mCursor, text);
   88  			size_t newCursor = Utils::String::nextCursor(mText, mCursor);
   89  			mCursor = (unsigned int)newCursor;
   90  		}
   91  	}
   92  
   93  	onTextChanged();
   94  	onCursorChanged();
   95  }
   96  
   97  bool TextEditComponent::hasAnyKeyPressed()
   98  {
   99  	bool anyKeyPressed = false;
  100  
  101  	int numKeys;
  102  	const Uint8* keys = SDL_GetKeyboardState(&numKeys);
```


## es-core/src/components/TextEditComponent.cpp @ 16dbac5211: lines 162-193 (excerpt of 400)

```text
  162  		if (mEditing)
  163  			stopEditing();
  164  
  165  		return false;
  166  	}
  167  
  168  	if((config->isMappedTo(BUTTON_OK, input) || (config->getDeviceId() == DEVICE_KEYBOARD && input.id == SDLK_RETURN)) && mFocused && !mEditing)
  169  	{
  170  		startEditing();
  171  		return true;
  172  	}
  173  
  174  	if(mEditing)
  175  	{
  176  		if(config->getDeviceId() == DEVICE_KEYBOARD && input.id == SDLK_RETURN)
  177  		{
  178  			if(isMultiline())
  179  			{
  180  				textInput("\n");
  181  			}
  182  			else
  183  			{
  184  				stopEditing();
  185  				return false;
  186  			}
  187  
  188  			return true;
  189  		}
  190  
  191  		if((config->getDeviceId() == DEVICE_KEYBOARD && input.id == SDLK_ESCAPE)) // || (config->getDeviceId() != DEVICE_KEYBOARD && config->isMappedTo(BUTTON_BACK, input)))
  192  		{
  193  			stopEditing();
```


## es-core/src/components/TextEditComponent.cpp @ 16dbac5211: lines 367-386 (excerpt of 400)

```text
  367  			if (!mEditing)
  368  				cursorColor = (ThemeData::getMenuTheme()->Text.color & 0xFFFFFF00) | (unsigned char) (getOpacity() * 0.25f);
  369  
  370  			Renderer::drawRect(cursorPos.x(), cursorPos.y() + (mFont->getHeight() - cursorHeight) / 2, 2.0f, cursorHeight, cursorColor, cursorColor); // 0x000000FF
  371  		}
  372  	}
  373  }
  374  
  375  bool TextEditComponent::isMultiline()
  376  {
  377  	return (getSize().y() > mFont->getHeight() * 1.25f);
  378  }
  379  
  380  Vector2f TextEditComponent::getTextAreaPos() const
  381  {
  382  	return Vector2f(TEXT_PADDING_HORIZ / 2.0f, TEXT_PADDING_VERT / 2.0f);
  383  }
  384  
  385  Vector2f TextEditComponent::getTextAreaSize() const
  386  {
```


## es-app/src/main.cpp @ 16dbac5211: lines 1026-1050 (excerpt of 1368)

```text
 1026  			LOG(LogInfo) << "journey: the continuation starts (" << (journeyTiers.known ? "the ticked tiers" : "an earlier build's marker: everything") << ")";
 1027  			window.pushGui(new GuiCloudTransfer(&window, cmd, _("RESTORING FROM THE CLOUD"), items, itemsAfterContent));
 1028  			}, _("LATER"), [journeyMarker, journeyRecord] {
 1029  			std::remove(journeyMarker.c_str());
 1030  			Utils::FileSystem::removeFile(journeyRecord);
 1031  			}));
 1032  	}
 1033  
 1034  	// Either configuration file was found missing, empty or damaged at this
 1035  	// start and its last-known-good record was loaded and written back in its
 1036  	// place (Settings::loadFile, SystemConf::loadSystemConf; D-CLOUD-079).
 1037  	// Said once, here, where the interface is up to say it: the alternative
 1038  	// was the RG SP's morning -- every setting back at its default and no
 1039  	// word why (fork #102). Pushed before the one-shot prompts above so it
 1040  	// sits under them and is read after they are dealt with.
 1041  	if (Settings::wasRecovered() || SystemConf::wasRecovered())
 1042  		window.pushGui(new GuiMsgBox(&window, _("YOUR SETTINGS FILE WAS DAMAGED. THE LAST GOOD COPY WAS RESTORED."), _("OK")));
 1043  
 1044  	// A settings restore that was cut off -- the power gone while the archive
 1045  	// was being written over the live tree -- was undone at this boot by
 1046  	// chksysconfig from the copy backuptool had taken aside, or could not be;
 1047  	// the marker says which (D-CLOUD-078, KILL18). Consumed on OK, not on
 1048  	// display, so a power cut with the message up leaves it for the next
 1049  	// boot. Read uncached: another process wrote it.
 1050  	const std::string revertedMarker = "/storage/.config/.restore-reverted";
```


## es-app/src/guis/GuiMenu.cpp @ 16dbac5211: lines 2977-3000 (excerpt of 11747)

```text
 2977  	}
 2978  
 2979  #ifdef BATOCERA
 2980  	s->addEntry(_("DMD"), true, [this] { openDmdSettings(); });
 2981  #endif
 2982  
 2983  #ifdef BATOCERA
 2984          s->addEntry(_("MULTISCREENS"), true, [this] { openMultiScreensSettings(); });
 2985  #endif
 2986  
 2987  #ifdef BATOCERA
 2988  	int red, green, blue;
 2989  	bool ledSupported = ApiSystem::getInstance()->getLED(red, green, blue);
 2990  
 2991  	if (ledSupported) {
 2992  		s->addGroup(_("LED HARDWARE"));
 2993  
 2994  		auto led_enabled_switch = std::make_shared<SwitchComponent>(mWindow);
 2995  		bool isEnabled = ApiSystem::getInstance()->isLEDEnabled();
 2996  		led_enabled_switch->setState(isEnabled);
 2997  		s->addWithLabel(_("ENABLE LED"), led_enabled_switch);
 2998  		
 2999  		// Only display RGB color sliders and modes if the hardware is NOT monochrome
 3000  		if (!ApiSystem::getInstance()->isLEDMonochrome()) {
```


## es-app/src/guis/GuiMenu.cpp @ 16dbac5211: lines 3120-3161 (excerpt of 11747)

```text
 3120  
 3121  					if (tokens.size() >= 3) {
 3122  						// concatenat the ending words
 3123  						std::string vname = "";
 3124  						for (unsigned int i = 2; i < tokens.size(); i++) {
 3125  							if (i > 2) vname += " ";
 3126  							vname += tokens.at(i);
 3127  						}
 3128  						optionsStorage->add(vname, (*it), selectedStorage == std::string("DEV " + tokens.at(1)));
 3129  					}
 3130  				} else {
 3131  				  std::vector<std::string> tokens = Utils::String::split(*it, ' ');
 3132  				  if (tokens.size() == 1) {
 3133  					optionsStorage->add((*it), (*it), selectedStorage == (*it));
 3134  				  } else {
 3135  				    // concatenat the ending words
 3136  				    std::string vname = "";
 3137  				    for (unsigned int i = 1; i < tokens.size(); i++) {
 3138  				      if (i > 1) vname += " ";
 3139  				      vname += tokens.at(i);
 3140  				    }
 3141  				    optionsStorage->add(_(vname.c_str()), tokens.at(0), selectedStorage == tokens.at(0));
 3142  				  }
 3143  				}
 3144  		}
 3145  
 3146  		s->addWithLabel(_("STORAGE DEVICE"), optionsStorage);
 3147  		s->addSaveFunc([optionsStorage, selectedStorage, s]
 3148  		{
 3149  			if (optionsStorage->changed())
 3150  			{
 3151  				ApiSystem::getInstance()->setStorage(optionsStorage->getSelected());
 3152  				s->setVariable("reboot", true);
 3153  			}
 3154  		});
 3155  	}
 3156  
 3157  	// backup
 3158  	if (ApiSystem::getInstance()->isScriptingSupported(ApiSystem::BACKUP))
 3159  		s->addEntry(_("BACKUP USER DATA"), true, [this] { mWindow->pushGui(new GuiBackupStart(mWindow)); });
 3160  
 3161  	if (ApiSystem::getInstance()->isScriptingSupported(ApiSystem::INSTALL))
```


## es-app/src/guis/GuiMenu.cpp @ 16dbac5211: lines 3197-3220 (excerpt of 11747)

```text
 3197  	  if (isFullUI)
 3198  	    s->addEntry(_("SERVICES"), true, [this] { openServicesSettings(); });
 3199  	}
 3200  
 3201  	// Security
 3202  	s->addEntry(_("SECURITY"), true, [this, s] 
 3203  	{
 3204  		GuiSettings *securityGui = new GuiSettings(mWindow, _("SECURITY").c_str());
 3205  		auto securityEnabled = std::make_shared<SwitchComponent>(mWindow);
 3206  		securityEnabled->setState(SystemConf::getInstance()->get("system.security.enabled") == "1");
 3207  		securityGui->addWithDescription(_("ENFORCE SECURITY"), _("Require a password for accessing the network share."), securityEnabled);
 3208  
 3209  		auto rootpassword = std::make_shared<TextComponent>(mWindow, ApiSystem::getInstance()->getRootPassword(), ThemeData::getMenuTheme()->Text.font, ThemeData::getMenuTheme()->Text.color);
 3210  		securityGui->addWithLabel(_("ROOT PASSWORD"), rootpassword);
 3211  
 3212  #ifdef BATOCERA
 3213  		auto cpuMitigations = std::make_shared<SwitchComponent>(mWindow);
 3214  		cpuMitigations->setState(ApiSystem::getInstance()->areCpuMitigationsEnabled());
 3215  		securityGui->addWithDescription(
 3216  			_("CPU SECURITY MITIGATIONS"),
 3217  			_("Disabling mitigations may improve performance on some systems at the cost of reduced protection against certain CPU vulnerabilities."),
 3218  			cpuMitigations);
 3219  #endif
 3220  
```


## es-app/src/guis/GuiMenu.cpp @ 16dbac5211: lines 5042-5083 (excerpt of 11747)

```text
 5042  			const bool rest = wantSaves || wantContent || wantMedia;
 5043  			add("SETTINGS", std::string("echo '>>> unit SETTINGS||' ; /usr/bin/cloud_restore --yes --system-only"
 5044  				" && { echo '>>> doing unpack' ; /usr/bin/backuptool restore")
 5045  				+ (rest ? " --then-cloud" : "") + " --no-restart ; }");
 5046  			cmd += " ; exit $rc";
 5047  			const std::string question = rest
 5048  				? _("RESTORE SETTINGS FIRST, THEN RESTART?\n\nYOUR EXISTING CONFIGURATION IS REPLACED. ANYTHING ELSE YOU TICKED IS RESTORED AFTER THE RESTART. WI-FI AND ACCOUNT PASSWORDS MUST BE RE-ENTERED.")
 5049  				: _("RESTORE SETTINGS, THEN RESTART?\n\nYOUR EXISTING CONFIGURATION IS REPLACED. WI-FI AND ACCOUNT PASSWORDS MUST BE RE-ENTERED.");
 5050  			window->pushGui(new GuiMsgBox(window, question, _("YES"),
 5051  				[window, s, cmd, rest, wantSaves, wantContent, wantMedia]
 5052  				{
 5053  					const std::string record = JourneyTiers::PATH;
 5054  					if (rest)
 5055  					{
 5056  						Utils::FileSystem::createDirectory(Utils::FileSystem::getParent(record));
 5057  						// This restore's ticks, or no record at all: an earlier
 5058  						// attempt's record at the same path was read as this one's
 5059  						// when the write failed (audit of the fixes, E2 gpt G-E2-01).
 5060  						// No record leaves the start with a marker and nothing to
 5061  						// read: it offers everything and its prompt names
 5062  						// everything. A record that can be neither replaced nor
 5063  						// removed stops the restore here, before anything changes.
 5064  						const JourneyTiers::Replaced replaced = JourneyTiers::replaceRecord(
 5065  							JourneyTiers::record(wantSaves, wantContent, wantMedia),
 5066  							[&record](const std::string& text) { return Utils::AtomicFile::writeText(record, text); },
 5067  							[&record]() { return Utils::FileSystem::removeFile(record); },
 5068  							[&record]() { return Utils::FileSystem::exists(record, false); });
 5069  						if (replaced == JourneyTiers::Replaced::NoRecord)
 5070  							LOG(LogWarning) << "restore: the journey record could not be written to " << record << "; the start will offer everything";
 5071  						else if (replaced == JourneyTiers::Replaced::OldRecordStands)
 5072  						{
 5073  							LOG(LogError) << "restore: an earlier journey record at " << record << " could be neither replaced nor removed; the restore was not started";
 5074  							s->close();
 5075  							window->pushGui(new GuiMsgBox(window, _("COULDN'T SAVE WHAT YOU TICKED, SO NOTHING WAS RESTORED."), _("OK")));
 5076  							return;
 5077  						}
 5078  					}
 5079  					else if (Utils::FileSystem::exists(record, false))
 5080  						Utils::FileSystem::removeFile(record);
 5081  					s->close();
 5082  					auto page = new GuiCloudTransfer(window, cmd, _("RESTORING SETTINGS FROM THE CLOUD"), 1);
 5083  					page->setCompletedAction([]
```


## es-app/src/guis/GuiMenu.cpp @ 16dbac5211: lines 8357-8384 (excerpt of 11747)

```text
 8357  #endif
 8358  				// Written here: the rows set memory only, and a page with no
 8359  				// save function writes no file (GuiSettings::save).
 8360  				ra->onFinalize([s, reopen] { SystemConf::getInstance()->saveSystemConf(); s->close(); reopen(); });
 8361  				window->pushGui(ra);
 8362  			});
 8363  
 8364  		if (!ssUser.empty())
 8365  			addCredentialRow(_("SCREENSCRAPER") + " (" + ssUser + ")",
 8366  				_("YOUR USERNAME WAS RESTORED; THE PASSWORD WAS NOT."),
 8367  				!Settings::getInstance()->getString("ScreenScraperPass").empty(),
 8368  				[window, s, reopen]
 8369  			{
 8370  				auto ss = new GuiSettings(window, _("SCREENSCRAPER"));
 8371  				ss->addInputTextConfigRow(_("PASSWORD"), "ScreenScraperPass", true, true);
 8372  #if defined(SCREENSCRAPER_RUNTIME_DEV_LOGIN) && !defined(SCREENSCRAPER_DEV_LOGIN)
 8373  				// The developer password is held back from backups too (#64).
 8374  				ss->addInputTextConfigRow(_("DEVELOPER PASSWORD"), "ScreenScraperDevPass", true, true);
 8375  #endif
 8376  				ss->onFinalize([s, reopen] { Settings::getInstance()->saveFile(); s->close(); reopen(); });
 8377  				window->pushGui(ss);
 8378  			});
 8379  	}
 8380  
 8381  	// Netplay's password is stripped too, but it is only meaningful to a
 8382  	// player who has netplay switched on.
 8383  	if (SystemConf::getInstance()->getBool("global.netplay"))
 8384  	{
```


## es-app/src/guis/GuiMenu.cpp @ 16dbac5211: lines 9892-9938 (excerpt of 11747)

```text
 9892  	{
 9893  		if (ipList->empty())
 9894  			return;
 9895  
 9896  		std::string text = _("AVAILABLE IP ADDRESSES:\n\n");
 9897  		for (const auto& address : *ipList)
 9898  			text += address + "\n";
 9899  		text.pop_back();
 9900  
 9901  		window->pushGui(new GuiMsgBox(window, text, _("OK"), nullptr));
 9902  	});
 9903  
 9904  	// What this device is called on the network. system.hostname keeps whatever
 9905  	// the player typed; the network only takes letters, digits and hyphens, so
 9906  	// network-base-setup applies the cleaned form at boot and this says what
 9907  	// that form is -- shown only when it differs from the name they gave, since
 9908  	// otherwise it repeats the HOSTNAME row below (#106).
 9909  	const std::string deviceName = SystemConf::getInstance()->get("system.hostname");
 9910  	const std::string networkName = CloudText::cleanHostname(deviceName);
 9911  	if (!networkName.empty() && networkName != deviceName)
 9912  		s->addWithLabel(_("NETWORK NAME"), std::make_shared<TextComponent>(mWindow, networkName, font, color));
 9913  
 9914  	auto status = std::make_shared<TextComponent>(mWindow, _("CHECKING..."), font, color);
 9915  	s->addWithLabel(_("INTERNET STATUS"), status);
 9916  
 9917  	networkSettingsFillIn(window, s, ip, ipList, status);
 9918  
 9919  	// Network Indicator
 9920  	auto networkIndicator = std::make_shared<SwitchComponent>(mWindow);
 9921  	networkIndicator->setState(Settings::getInstance()->getBool("ShowNetworkIndicator"));
 9922  	s->addWithLabel(_("SHOW NETWORK INDICATOR"), networkIndicator);
 9923  	s->addSaveFunc([networkIndicator] { Settings::getInstance()->setBool("ShowNetworkIndicator", networkIndicator->getState()); });
 9924  
 9925  	s->addGroup(_("SETTINGS"));
 9926  
 9927  #if !WIN32
 9928  	// Hostname
 9929  	s->addInputTextConfigRow(_("HOSTNAME"), "system.hostname", false);
 9930  #endif
 9931  
 9932  	// Wifi enable
 9933  	auto enable_wifi = std::make_shared<SwitchComponent>(mWindow);
 9934  	enable_wifi->setState(baseWifiEnabled);
 9935  	s->addWithLabel(_("ENABLE WI-FI"), enable_wifi, selectWifiEnable);
 9936  
 9937  #ifdef RK3399
 9938          // Add option to disable RG552 wifi gpio
```


## es-app/src/guis/GuiMenu.cpp @ 16dbac5211: lines 11579-11595 (excerpt of 11747)

```text
11579  	std::string fileName = path + "/" + themeSet + ".cfg";
11580  
11581  	if (fileData.empty())
11582  	{
11583  		if (Utils::FileSystem::exists(fileName))
11584  			Utils::FileSystem::removeFile(fileName);
11585  	}
11586  	else
11587  		Utils::FileSystem::writeAllText(fileName, fileData);
11588  
11589  }
11590  
11591  void GuiMenu::loadSubsetSettings(const std::string themeName)
11592  {
11593  	std::string path = Paths::getUserEmulationStationPath() + "/themesettings";
11594  	if (!Utils::FileSystem::exists(path))
11595  		Utils::FileSystem::createDirectory(path);
```


## es-app/src/guis/GuiBluetoothDevices.cpp @ 16dbac5211: lines 117-160 (excerpt of 160)

```text
  117  		[this, window](bool ret)
  118  		{
  119  			mWaitingLoad = false;
  120  			mWindow->pushGui(new GuiMsgBox(mWindow, _("BLUETOOTH DEVICES HAVE BEEN DELETED."), _("OK")));
  121  			delete this;
  122  		}));	
  123  }
  124  
  125  void GuiBluetoothDevices::onRemoveDevice(const std::string& id, const std::string& name)
  126  {
  127  	if (mWaitingLoad)
  128  		return;
  129  
  130  	std::string deviceName = name;
  131  	std::string macAddress = id;
  132  
  133  	auto idx = macAddress.find(" ");
  134  	if (idx != std::string::npos)
  135  	{
  136  		deviceName = macAddress.substr(idx + 1);
  137  		macAddress = macAddress.substr(0, idx);
  138  	}
  139  
  140  	if (deviceName.empty())
  141  		deviceName = macAddress;
  142  
  143  	Window* window = mWindow;
  144  	window->pushGui(new GuiMsgBox(window, Utils::String::format(_("ARE YOU SURE YOU WANT TO REMOVE '%s' ?").c_str(), deviceName.c_str()),
  145  		_("YES"), [this, window, macAddress]
  146  		{ 			
  147  			window->pushGui(new GuiLoading<bool>(window, _("PLEASE WAIT"),
  148  				[this, window, macAddress](auto gui)
  149  				{
  150  					mWaitingLoad = true;
  151  					return ApiSystem::getInstance()->removeBluetoothDevice(macAddress);
  152  				},
  153  				[this, window](bool ret)
  154  				{
  155  					mWaitingLoad = false;
  156  					load();
  157  				}));
  158  		},
  159  		_("NO"), nullptr));
  160  }
```


## 001-functions @ 8ebaf8daad: lines 2-24 (excerpt of 707)

```text
    2  # Copyright (C) 2019-present Shanti Gilbert (https://github.com/shantigilbert)
    3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    4  
    5  . /etc/os-release
    6  
    7  export XDG_RUNTIME_DIR=/var/run/0-runtime-dir
    8  export PATH="/usr/bin:/usr/local/bin:/storage/bin:${PATH}"
    9  export SDL_GAMECONTROLLERCONFIG_FILE="/storage/.config/SDL-GameControllerDB/gamecontrollerdb.txt"
   10  
   11  J_DIR="/storage/.config/system"
   12  J_CONF="${J_DIR}/configs/system.cfg"
   13  J_CONF_LOCK="/tmp/.system.cfg.lock"
   14  ES_CONF="/storage/.emulationstation/es_settings.cfg"
   15  
   16  function tocon() {
   17    echo -ne "\033[1000H\033[2K==> ${*}" >/dev/console
   18  }
   19  
   20  function log() {
   21    SOURCE=${1//\/*\//}
   22    MESSAGE=${*#${1}}
   23    MESSAGE=${MESSAGE# }
   24    logger -t ${SOURCE} "${MESSAGE}"
```


## 001-functions @ 8ebaf8daad: lines 352-449 (excerpt of 707)

```text
  352  #   - when the last good copy (system.cfg.backup) is whole -- non-empty,
  353  #     ending in a newline, carrying the hostname line -- the keys the cut
  354  #     took, and the half line's, come back from it;
  355  #   - an empty file with a whole copy beside it starts from the copy.
  356  #
  357  # The journal says which. A whole file is its own lines, unchanged. Returns
  358  # non-zero when the file cannot be read (a missing one included: the
  359  # callers' temporary then holds nothing they would rename).
  360  function settings_base() {
  361    local rec="${J_CONF}.backup" n say=""
  362    [ -r "${J_CONF}" ] || return 1
  363    if [ -s "${J_CONF}" ] && [ -z "$(tail -c 1 "${J_CONF}" 2>/dev/null)" ]
  364    then
  365      cat "${J_CONF}"
  366      return
  367    fi
  368    n=$(wc -l < "${J_CONF}") || return 1
  369    if [ -s "${rec}" ] && [ -z "$(tail -c 1 "${rec}" 2>/dev/null)" ] && grep -q '^system\.hostname=' "${rec}" 2>/dev/null
  370    then
  371      awk -v n="${n}" 'FILENAME == ARGV[1] { if (FNR <= n) { print; k = $0; sub(/=.*/, "", k); have[k] = 1 } next }
  372                       { k = $0; sub(/=.*/, "", k); if (!(k in have)) print }' "${J_CONF}" "${rec}" || return 1
  373      say="system.cfg was cut short; this write starts from its whole lines and takes the rest from system.cfg.backup"
  374    else
  375      head -n "${n}" "${J_CONF}" || return 1
  376      [ -s "${J_CONF}" ] && say="system.cfg was cut short and has no whole copy beside it; this write keeps its whole lines and drops the cut one"
  377    fi
  378    if [ -n "${say}" ]
  379    then
  380      if command -v logger >/dev/null 2>&1; then logger -t system.cfg "${say}"; else echo "system.cfg: ${say}" >&2; fi
  381    fi
  382    return 0
  383  }
  384  
  385  function prepare_settings_temp() {
  386    # The rename must not widen a private live file or recovery record (#421).
  387    # Set the temporary's mode while it is empty, including an old temporary
  388    # left by an interrupted writer. Callers hold the settings lock where used.
  389    local tmp="${1}" source bits mode=0777 found=0
  390    shift
  391    [ ! -L "${tmp}" ] && { [ ! -e "${tmp}" ] || [ -f "${tmp}" ]; } || return 1
  392    for source in "$@"; do
  393      [ "${source}" != "${tmp}" ] || return 1
  394      [ -e "${source}" ] || continue
  395      bits=$(stat -L -c %a "${source}") || return 1
  396      [[ "${bits}" =~ ^[0-7]{1,4}$ ]] || return 1
  397      mode=$((mode & 8#${bits}))
  398      found=1
  399    done
  400    [ "${found}" = 1 ] || mode=0600
  401    # Never relax the caller's umask either.
  402    bits=$(umask); [[ "${bits}" =~ ^[0-7]{1,4}$ ]] || return 1
  403    printf -v bits '%o' "$((mode & ~8#${bits} & 0777))"
  404    ( umask 077; : > "${tmp}" ) && chmod "${bits}" "${tmp}"
  405  }
  406  
  407  # One key, one write, one rename, under a lock the caller holds: awk prints
  408  # every line but the key's, then the key's new line, into a temporary
  409  # beside the file, and the temporary is renamed over it -- so the file goes
  410  # from the old content to the new in a single step, and an empty file (a
  411  # torn write left it so) gets its one line the same way. It used to be
  412  # del_setting (a rename) and then an append, with the lock released and
  413  # retaken in between: a kill between the two lost the key (D-CLOUD-078,
  414  # #105). Then it was one sed -i, `/^k=/d` and `$a k=v`, which loses the
  415  # key whenever its line is the LAST line of the file: `d` ends the cycle
  416  # and `$a` never runs for that line, so every key that sat last in
  417  # system.cfg read as its default after being set (KILL10/KILL11 on the VM,
  418  # 2026-09-10). The key is matched literally (a dot in it is a dot), and the
  419  # value crosses through the environment, so `/`, `&`, `\` and spaces are
  420  # nobody's to interpret.
  421  #
  422  # Returns 0 only when the new file is in place: the awk and the rename both
  423  # succeeded. The failure branch used to end in the rm of the temporary, so
  424  # the function's status was the rm's -- 0 -- and a write that never landed
  425  # (a full card, a read-only folder) was reported to every caller as done
  426  # (#307 PL-011).
  427  #
  428  # It writes onto settings_base's lines, not the file's bytes: see there.
  429  function write_setting_line() {
  430    if prepare_settings_temp "${J_CONF}.tmp" "${J_CONF}" "${J_CONF}.backup" \
  431       && ( set -o pipefail
  432         settings_base | K="${1}" V="${2}" awk 'BEGIN { k = ENVIRON["K"]; v = ENVIRON["V"] }
  433                                                index($0, k "=") != 1 { print }
  434                                                END { print k "=" v }' ) > "${J_CONF}.tmp" 2>/dev/null \
  435       && mv -f "${J_CONF}.tmp" "${J_CONF}"
  436    then
  437      return 0
  438    fi
  439    rm -f "${J_CONF}.tmp"
  440    return 1
  441  }
  442  #
  443  # Any other key's line is removed by the same literal match the writer uses:
  444  # `sed -i "/^${1}=/d"` read the key as a pattern, so deleting foo.bar also
  445  # removed foo_bar and fooXbar (#308, the gpt seat's F-PB-16) -- and through
  446  # one temporary and one rename, with the status returned, as the writer.
  447  function del_setting() {
  448    local rc=0
  449    wait_lock || return 1
```


## 001-functions @ 8ebaf8daad: lines 520-633 (excerpt of 707)

```text
  520    fi
  521  }
  522  
  523  # The device name in the only form the network accepts: letters, digits and
  524  # hyphens, at most 63 of them, no hyphen at either end. Anything else -- a
  525  # space, an underscore, punctuation, a run of hyphens -- becomes one hyphen, so "RG SP" is
  526  # applied as RG-SP rather than refused by hostnamed and left as whatever
  527  # NetworkManager put there (fork #106). EmulationStation's HOSTNAME row keeps
  528  # the same rule at entry (GuiMenu, cleanHostname); this is the fallback for a
  529  # value already stored. Empty in, empty out: the caller decides the default.
  530  function clean_hostname() {
  531    printf '%s' "${1}" | sed -E 's/[^A-Za-z0-9]+/-/g; s/^-+//; s/-+$//' | cut -c1-63 | sed -E 's/-+$//'
  532  }
  533  
  534  function set_setting() {
  535  
  536    if [ ! -d "/storage/.config/system/configs" ]
  537    then
  538      mkdir -p /storage/.config/system/configs
  539    fi
  540    if [ ! -e "/storage/.config/system/configs/system.cfg" ]
  541    then
  542      cp -f /usr/config/system/configs/system.cfg /storage/.config/system/configs/system.cfg
  543    fi
  544  
  545    if [[ "${1}" =~ ^[[:alnum:]] ]]
  546    then
  547      if [ "${2}" = "default" ]
  548      then
  549        # Removes the line -- or, for system.hostname, empties it: see there.
  550        del_setting "${1}"
  551      else
  552        # One write under one lock hold (write_setting_line says why), and the
  553        # write's own status returned past the lock's release (#307 PL-011).
  554        local rc
  555        wait_lock || return 1
  556        write_setting_line "${1}" "${2}"; rc=$?
  557        rm -f "${J_CONF_LOCK}"
  558        return ${rc}
  559      fi
  560    fi
  561  }
  562  
  563  # Several keys in one write and one rename, under one hold of the lock: a
  564  # pair that must agree -- wifi.ssid and wifi.key -- is never left half
  565  # written by a failure between two set_setting calls, where the network's
  566  # name moved and its key did not (#307, the audit of the fix round, gpt
  567  # G2-B-11). Arguments are key value pairs; "default" removes a key's line
  568  # as set_setting does, except system.hostname's, which is emptied
  569  # (D-NET-009). Returns 0 only when the new file is in place; nothing is
  570  # written when the arguments are not whole pairs of keys that start with a
  571  # letter or digit.
  572  function set_settings() {
  573    local n=0 rc k v
  574    local -a pairs=()
  575    [ $# -gt 0 ] && [ $(( $# % 2 )) -eq 0 ] || return 1
  576    while [ $# -gt 0 ]
  577    do
  578      k="${1}"; v="${2}"; shift 2
  579      [[ "${k}" =~ ^[[:alnum:]] ]] || return 1
  580      n=$((n + 1))
  581      if [ "${v}" = "default" ] && [ "${k}" != "system.hostname" ]
  582      then
  583        pairs+=("SK${n}=${k}" "SV${n}=" "SD${n}=1")
  584      else
  585        [ "${v}" = "default" ] && v=""
  586        pairs+=("SK${n}=${k}" "SV${n}=${v}" "SD${n}=0")
  587      fi
  588    done
  589    if [ ! -d "/storage/.config/system/configs" ]
  590    then
  591      mkdir -p /storage/.config/system/configs
  592    fi
  593    if [ ! -e "/storage/.config/system/configs/system.cfg" ]
  594    then
  595      cp -f /usr/config/system/configs/system.cfg /storage/.config/system/configs/system.cfg
  596    fi
  597    wait_lock || return 1
  598    if prepare_settings_temp "${J_CONF}.tmp" "${J_CONF}" "${J_CONF}.backup" \
  599       && ( set -o pipefail
  600         settings_base | env "${pairs[@]}" SN="${n}" awk 'BEGIN { n = ENVIRON["SN"]; for (j = 1; j <= n; j++) { k[j] = ENVIRON["SK" j]; v[j] = ENVIRON["SV" j]; d[j] = ENVIRON["SD" j] } }
  601                                                       { for (j = 1; j <= n; j++) if (index($0, k[j] "=") == 1) next; print }
  602                                                       END { for (j = 1; j <= n; j++) if (d[j] != 1) print k[j] "=" v[j] }' ) > "${J_CONF}.tmp" 2>/dev/null \
  603       && mv -f "${J_CONF}.tmp" "${J_CONF}"
  604    then
  605      rc=0
  606    else
  607      rm -f "${J_CONF}.tmp"
  608      rc=1
  609    fi
  610    rm -f "${J_CONF_LOCK}"
  611    return ${rc}
  612  }
  613  
  614  function battery_percent() {
  615    if [ -f /tmp/battery.percent ]; then
  616      cat /tmp/battery.percent
  617    else
  618      awk 'BEGIN {FS="="} /POWER_SUPPLY_CAPACITY=/ {print $2}' /sys/class/power_supply/[Bb][Aa][Tt]*/uevent 2>/dev/null
  619    fi
  620  }
  621  
  622  function get_es_setting() {
  623    echo $(sed -n "s|\s*<${1} name=\"${2}\" value=\"\(.*\)\" />|\1|p" ${ES_CONF})
  624  }
  625  
  626  function fbwidth() {
  627    local ORIENTATION=$(</sys/devices/virtual/graphics/fbcon/rotate)
  628    if [ "${ORIENTATION}" = "0" ]
  629    then
  630      fbset | awk '/geometry/ {print $2}'
  631    else
  632      fbset | awk '/geometry/ {print $3}'
  633    fi
```


## wifictl @ 8ebaf8daad: lines 30-74 (excerpt of 557)

```text
   30  ###                               second line when it was the one in use, and clears wifi.ssid /
   31  ###                               wifi.key when they name it; exit 1, nothing printed, when it is
   32  ###                               not a remembered network or the delete failed; exit 2 when
   33  ###                               NetworkManager could not be asked
   34  ###     wifictl join <name>       join a saved network with the key NetworkManager holds for it
   35  ###                               (the picker's press on a SAVED row): prints "joined" once its
   36  ###                               profile is active and moves wifi.ssid / wifi.key onto it; exit 1,
   37  ###                               nothing printed, when it is not a saved network or the
   38  ###                               activation failed; exit 2 when NetworkManager could not be asked
   39  ###
   40  
   41  WIFI_TYPE=$(get_setting wifi.adhoc.enabled)
   42  NETWORK_ADDRESS="192.168.80"
   43  ADHOC_CLIENT_ID=$(get_setting wifi.adhoc.id)
   44  [ -z "${ADHOC_CLIENT_ID}" ] && ADHOC_CLIENT_ID="1"
   45  NETPLAY_SSID="NETPLAY_AP"
   46  WIFI_DEV="$(ls /sys/class/net | grep -m1 ^wlan)"
   47  
   48  # Typed scan/security/join callers must not read an unavailable radio as success.
   49  if [ "${1}" = list ] || [ "${1}" = scanlist ] || \
   50     [ "${1}" = security ] || [ "${1}" = connect-open ]; then
   51    [ -n "${WIFI_DEV}" ] && [ -d "/sys/class/net/${WIFI_DEV}" ] && [ -n "${NMCLI}" ] || exit 2
   52  fi
   53  
   54  # Exit the script if the WiFi device isn't available
   55  [ -z "${WIFI_DEV}" ] && exit 0
   56  [ ! -d "/sys/class/net/${WIFI_DEV}" ] && exit 0
   57  [ -z "${NMCLI}" ] && exit 0
   58  
   59  SSID="${2:-$(get_setting wifi.ssid 2>/dev/null)}"
   60  PSK=*** wifi.key 2>/dev/null)}"
   61  COUNTRY="${4:-$(get_setting wifi.country | tr -d '[:space:]' 2>/dev/null)}"
   62  
   63  if [ "${WIFI_TYPE}" = "1" ]; then
   64    SSID="${NETPLAY_SSID}"
   65    PSK=***
   66  fi
   67  
   68  ###
   69  ### Functions...
   70  ###
   71  
   72  # Wait for iwd to start and have a device available. A successful query that
   73  # never sees the adapter is exit 1; a failed final query keeps its status.
   74  # Connection/AP callers still make their own operation the final result.
```


## wifictl @ 8ebaf8daad: lines 142-223 (excerpt of 557)

```text
  142    while IFS= read -r line; do
  143      [ -n "${line}" ] || continue
  144      profile="${line%$'\t'*}"
  145      saved_ssid=$("${NMCLI}" --escape no -g 802-11-wireless.ssid connection show id "${profile}" 2>/dev/null) || return 1
  146      [ "${profile}" != "${name}" ] && [ "${saved_ssid}" != "${name}" ] || return 1
  147    done <<< "${rows}"
  148    wait_for_wifi
  149    "${NMCLI}" -w 90 device wifi connect "${name}" ifname "${WIFI_DEV}" >/dev/null 2>&1
  150  }
  151  
  152  connect_wifi() {
  153    wait_for_wifi
  154    # Ensure NM has the device ready and has scanned
  155    for i in $(seq 1 10); do
  156      "${NMCLI}" -t -f DEVICE,STATE dev status 2>/dev/null | grep -q "^${WIFI_DEV}:disconnected" && break
  157      "${NMCLI}" -t -f DEVICE,STATE dev status 2>/dev/null | grep -q "^${WIFI_DEV}:connected" && break
  158      sleep 1
  159    done
  160    "${NMCLI}" dev wifi rescan ifname "${WIFI_DEV}" 2>/dev/null
  161    sleep 2
  162    # If a keyfile profile for this SSID already exists but is incomplete (e.g. missing
  163    # 802-11-wireless-security.key-mgmt), NM fails connection-update with "key-mgmt: property is missing".
  164    # Drop the stale profile so "device wifi connect" creates a clean one.
  165    # Two lines taken from ROCKNIX's own saved-network work (spycat88,
  166    # b1f8464241; the merged design D-UI-118, #318): with no key given, a
  167    # profile NetworkManager already holds for the name is brought up before
  168    # anything is deleted and rebuilt -- the settings-driven paths (ENABLE
  169    # WI-FI, the restore wizard) reach a saved network that way -- and a keyed
  170    # connect stores the key in the profile explicitly (psk-flags 0), so a
  171    # later join can read it.
  172    if [ -z "${PSK}" ] && "${NMCLI}" -w 30 connection up id "${SSID}" ifname "${WIFI_DEV}" >/dev/null 2>&1; then
  173      return 0
  174    fi
  175    "${NMCLI}" connection delete id "${SSID}" >/dev/null 2>&1 || true
  176    if [ -n "${PSK}" ]; then
  177      "${NMCLI}" -w 90 device wifi connect "${SSID}" password "${PSK}" ifname "${WIFI_DEV}" >/dev/null 2>&1 || return 1
  178      "${NMCLI}" connection modify "${SSID}" wifi-sec.psk-flags 0 >/dev/null 2>&1 || true
  179    else
  180      "${NMCLI}" -w 90 device wifi connect "${SSID}" ifname "${WIFI_DEV}" >/dev/null 2>&1
  181    fi
  182  }
  183  
  184  create_adhoc() {
  185    wait_for_wifi
  186    # NetworkManager drives iwd into AP mode itself (Device.Mode + AP.Start).
  187    # Switching the mode behind its back only makes NM force the device back to
  188    # station mode, so the netplay AP has to be a NetworkManager connection.
  189    # No DHCP: the clients derive their address from the local play ID.
  190    "${NMCLI}" connection delete id "${SSID}" >/dev/null 2>&1
  191    "${NMCLI}" connection add type wifi ifname "${WIFI_DEV}" con-name "${SSID}" ssid "${SSID}" \
  192      802-11-wireless.mode ap \
  193      802-11-wireless.band bg \
  194      802-11-wireless-security.key-mgmt wpa-psk \
  195      802-11-wireless-security.psk "${PSK}" \
  196      ipv4.method manual ipv4.addresses "${NETWORK_ADDRESS}.${ADHOC_CLIENT_ID}/24" \
  197      ipv6.method disabled || return 1
  198    "${NMCLI}" -w 30 connection up id "${SSID}" || return 1
  199  }
  200  
  201  connect_adhoc_client() {
  202    destroy_adhoc
  203    # Static lease: the netplay host runs no DHCP server, so the client
  204    # address is derived from the local play ID. Autoconnect stays off so a
  205    # vanished host doesn't keep the device from returning to ordinary
  206    # networks; rejoining is an explicit wifictl connect (ES toggle).
  207    "${NMCLI}" connection add type wifi ifname "${WIFI_DEV}" con-name "${SSID}" ssid "${SSID}" \
  208      802-11-wireless-security.key-mgmt wpa-psk \
  209      802-11-wireless-security.psk "${PSK}" \
  210      ipv4.method manual ipv4.addresses "${NETWORK_ADDRESS}.${ADHOC_CLIENT_ID}/24" \
  211      ipv6.method disabled connection.autoconnect no || return 1
  212    # The iwd backend fails "connection up" instantly when the SSID is not in
  213    # the scan cache yet, so make sure the host AP shows up first
  214    for i in $(seq 1 15); do
  215      "${NMCLI}" device wifi rescan ifname "${WIFI_DEV}" >/dev/null 2>&1
  216      sleep 2
  217      "${NMCLI}" -t -f SSID device wifi list ifname "${WIFI_DEV}" 2>/dev/null | grep -q "^${SSID}$" && break
  218    done
  219    "${NMCLI}" -t -f SSID device wifi list ifname "${WIFI_DEV}" 2>/dev/null | grep -q "^${SSID}$" || return 1
  220    # The host may still be coming up
  221    for i in $(seq 1 3); do
  222      "${NMCLI}" -w 20 connection up id "${SSID}" && return 0
  223      sleep 3
```


## wifictl @ 8ebaf8daad: lines 407-473 (excerpt of 557)

```text
  407  # then the settings wifi.ssid and wifi.key follow the profile, so the paths
  408  # that connect from the settings -- the ENABLE WI-FI switch, the restore
  409  # wizard -- name the network the player is on; the key is
  410  # read from NetworkManager and never printed. pin_wifi then prefers this
  411  # network at the next boot and resume. A name that is not a saved wireless
  412  # network, or an activation that fails: nothing printed, exit 1. NetworkManager
  413  # not answering: exit 2, so a caller cannot read a silence as a refusal.
  414  # The profile active on this device's adapter, by name, unescaped. A
  415  # profile's ACTIVE in saved_wifi says it is up somewhere -- on any adapter.
  416  wifi_dev_connection() {
  417    "${NMCLI}" -t -f GENERAL.CONNECTION device show "${WIFI_DEV}" 2>/dev/null | sed -n 's/^GENERAL\.CONNECTION://p' | nm_unescape
  418  }
  419  
  420  join_wifi() {
  421    local name="${1}" rows state psk
  422    [ -n "${name}" ] || return 1
  423    rows=$(saved_wifi) || return 2
  424    state=$(saved_state "${rows}" "${name}")
  425    [ -n "${state}" ] || return 1
  426    # Judged on the adapter the picker speaks for (WIFI_DEV, as current_wifi
  427    # is): a profile already up on another adapter read as "active" and
  428    # skipped the activation, and "joined" was said while this adapter stayed
  429    # on another network (#307 PL-031). So the profile is brought up on
  430    # WIFI_DEV by name, and joined is said only once WIFI_DEV reads it.
  431    if [ "$(wifi_dev_connection)" != "${name}" ]; then
  432      "${NMCLI}" -w 90 connection up id "${name}" ifname "${WIFI_DEV}" >/dev/null 2>&1 || return 1
  433      [ "$(wifi_dev_connection)" = "${name}" ] || return 1
  434    fi
  435    # The key as NetworkManager holds it, byte for byte. -g is terse output,
  436    # which escapes ':' and '\' in a value -- ab:cd\ef12345 came back as
  437    # ab\:cd\\ef12345 on the target's nmcli (guest d, 2026-09-27) and that was
  438    # stored as wifi.key -- so --escape no (#307 PL-003). Its status is read
  439    # before anything is written: a read that failed is not an open network,
  440    # and writing its empty answer over wifi.key cleared the key of a network
  441    # the device is on (#308 claude F-WF-02). An empty key is written only
  442    # when the profile has no key management -- an open network; a keyed one
  443    # whose key did not come back leaves the settings as they were. Either
  444    # way the device is joined, and says so.
  445    #
  446    # And wifi.ssid is the network's SSID, not the profile's name: the two
  447    # differ for a renamed profile or one NetworkManager deduplicated ("Home
  448    # 1"), and connect -- which the settings-driven paths run -- looks the
  449    # SSID up in the scan, where a profile's name is not found (#308 claude
  450    # F-WF-12, gpt F-WF-03).
  451    local keyed ssid
  452    if psk=*** --escape no -s -g 802-11-wireless-security.psk connection show id "${name}" 2>/dev/null) \
  453       && ssid=$("${NMCLI}" --escape no -g 802-11-wireless.ssid connection show id "${name}" 2>/dev/null) \
  454       && [ -n "${ssid}" ]; then
  455      if [ -z "${psk}" ]; then
  456        keyed=$("${NMCLI}" --escape no -g 802-11-wireless-security.key-mgmt connection show id "${name}" 2>/dev/null) || keyed="unread"
  457      fi
  458      if [ -z "${psk}" ] && [ -n "${keyed}" ]; then
  459        logger -t wifictl "joined ${name}; its key did not come back from NetworkManager, so the Wi-Fi settings were left as they were" 2>/dev/null
  460      elif ! set_settings wifi.ssid "${ssid}" wifi.key "${psk}"; then
  461        # One write for the pair (set_settings): a second write failing after
  462        # the first left this network's SSID with the last network's key, and
  463        # nothing said so (#307, the audit of the fix round, gpt G2-B-11).
  464        # The device is joined either way, and says so.
  465        logger -t wifictl "joined ${name}; its Wi-Fi settings could not be saved, so they were left as they were" 2>/dev/null
  466      fi
  467    else
  468      logger -t wifictl "joined ${name}; its key or SSID could not be read from NetworkManager, so the Wi-Fi settings were left as they were" 2>/dev/null
  469    fi
  470    pin_wifi
  471    echo "joined"
  472    return 0
  473  }
```


## wifictl @ 8ebaf8daad: lines 477-523 (excerpt of 557)

```text
  477  
  478    PHY=$(basename "$(readlink /sys/class/net/${WIFI_DEV}/phy80211)")
  479    if iwctl adapter "$PHY" show | grep -q 'SupportedModes.*ap'; then
  480      exit 0
  481    else
  482      exit 1
  483    fi
  484  }
  485  
  486  case "${1}" in
  487    enable)
  488      rfkill unblock wifi
  489      ;;
  490    disable)
  491      rfkill block wifi
  492      ;;
  493    pin)
  494      pin_wifi
  495      ;;
  496    security)
  497      wifi_security "${2}"
  498      ;;
  499    connect-open)
  500      connect_open_wifi "${2}"
  501      ;;
  502    connect)
  503      if [ "${WIFI_TYPE}" = "1" ] && \
  504         [ "${ADHOC_CLIENT_ID}" = "1" ]; then
  505        create_adhoc
  506      elif [ "${WIFI_TYPE}" = "1" ]; then
  507        connect_adhoc_client
  508      else
  509        destroy_adhoc
  510        connect_wifi
  511      fi
  512    ;;
  513    disconnect)
  514      if [ "${WIFI_TYPE}" = "1" ]; then
  515        destroy_adhoc
  516      else
  517        "${NMCLI}" device disconnect "${WIFI_DEV}" >/dev/null 2>&1
  518      fi
  519      ;;
  520    reconnect)
  521      /usr/bin/wifictl disconnect
  522      /usr/bin/wifictl connect
  523      ;;
```


## chksysconfig @ 8ebaf8daad: lines 47-114 (excerpt of 342)

```text
   47  # carriage return, printable ASCII, and everything above 0x7F for UTF-8 --
   48  # and never as classes. This read `[:print:][:space:]` for a day, which GNU
   49  # tr on the build host understands and the device's busybox tr does not:
   50  # it deleted the eight characters inside the brackets and left the rest, so
   51  # every real system.cfg was "not text", the shutdown and boot-time backups
   52  # were refused, and a damaged live file found its last good copy "damaged
   53  # too" and was reseeded from the image defaults -- the RG SP's morning
   54  # (#102) reproduced by the fix meant to end it (guest d, 2026-09-10).
   55  # tools/last-good-scripts-test now runs these checks through the image's
   56  # busybox, which is where it should have failed first.
   57  valid() {
   58    local f="$1"
   59    [ -s "${f}" ] || return 1
   60    [ "$(LC_ALL=C tr -d '\11\12\15\40-\176\200-\377' < "${f}" | head -c 1 | wc -c)" -eq 0 ] || return 1
   61    grep -q '^system\.hostname=' "${f}" || return 1
   62    ! LC_ALL=C grep -qvE '^[[:space:]]*$|^[^=[:space:]][^=]*=' "${f}"
   63  }
   64  
   65  # One file replaces another whole or not at all: copy to a temporary name in
   66  # the same directory, then rename over the target.
   67  put() {
   68    local src="$1" dst="$2"
   69    if prepare_settings_temp "${dst}.tmp" "${src}" "${dst}" \
   70       && cat "${src}" > "${dst}.tmp" && mv -f "${dst}.tmp" "${dst}"; then
   71      return 0
   72    fi
   73    rm -f "${dst}.tmp"
   74    return 1
   75  }
   76  
   77  # The record is written only from a whole file: valid, and ending in a
   78  # newline. Every writer ends system.cfg with one -- the interface's
   79  # SystemConf, the shell's awk and sort, the image's seed -- so a file that
   80  # does not was cut mid-line by a torn write, and its half line is not the
   81  # owner's; the shell's writers no longer complete such a line either
   82  # (settings_base in 001-functions). The last good copy stays as it is, and
   83  # the log says why (#307, the audit of the fix round; stream E1's lead
   84  # G2-E-core-03). A cut that fell exactly at a line's end cannot be told from
   85  # a file whose last keys were removed on purpose -- forget clears wifi.ssid
   86  # and wifi.key, which sort last -- and is taken as whole.
   87  backup() {
   88    if ! valid "${CFG}"; then
   89      say "not backing up system.cfg: it is empty, not text, or damaged; the last good copy stays as it is"
   90      return 1
   91    fi
   92    if [ -n "$(tail -c 1 "${CFG}" 2>/dev/null)" ]; then
   93      say "not backing up system.cfg: its last line was cut short; the last good copy stays as it is"
   94      return 1
   95    fi
   96    put "${CFG}" "${BACKUP}" || { say "could not write system.cfg.backup"; return 1; }
   97  }
   98  
   99  restore() {
  100    if ! valid "${BACKUP}"; then
  101      say "cannot restore system.cfg: the last good copy is missing or damaged too"
  102      return 1
  103    fi
  104    put "${BACKUP}" "${CFG}" || { say "could not write system.cfg from its last good copy"; return 1; }
  105    say "restored system.cfg from its last good copy (system.cfg.backup)"
  106  }
  107  
  108  # A settings restore that was cut off -- the power gone between tar starting
  109  # to write the archive over the live tree and the reboot that follows --
  110  # leaves the tree half from the archive and half from before, and nothing
  111  # running to notice. backuptool writes the path of the copy it took aside
  112  # into .restore-in-progress before it extracts and removes it after; a marker
  113  # still here at boot means the restore never finished, so the copy goes back
  114  # over the tree and EmulationStation is left .restore-reverted to say so once
```


## chksysconfig @ 8ebaf8daad: lines 254-338 (excerpt of 342)

```text
  254    #
  255    # Except when it is the only good copy there is: the live file cut and no
  256    # usable record beside it -- a device updated from before the record
  257    # existed (#102), whose writer's last save never reached its rename. The
  258    # interface's SystemConf reads such a whole .tmp when the live file is cut
  259    # (#307 PL-064, stream E1), but this runs first at sysinit and deleted it,
  260    # so the defaults were reseeded over a whole copy of the player's settings.
  261    # A .tmp that is itself usable is put in place instead, and said.
  262    #
  263    # A .tmp that could not be moved into place is kept, not swept: it was the
  264    # only good copy (#307, the audit of the fixes, gpt G-B-10).
  265    if [ -e "${CFG}.tmp" ]; then
  266      if ! valid "${CFG}" && ! valid "${BACKUP}" && valid "${CFG}.tmp"; then
  267        if mv -f "${CFG}.tmp" "${CFG}"; then
  268          say "system.cfg was cut and had no good copy; the whole one a write left beside it (system.cfg.tmp) was put in place"
  269        else
  270          say "system.cfg was cut and had no good copy; the whole one beside it (system.cfg.tmp) could not be put in place and is kept"
  271          kept_tmp=1
  272        fi
  273      else
  274        rm -f "${CFG}.tmp"
  275      fi
  276    fi
  277  
  278    if ! valid "${CFG}"; then
  279      if [ ! -e "${CFG}" ]; then
  280        state="missing"
  281      elif [ ! -s "${CFG}" ]; then
  282        state="empty"
  283      else
  284        state="damaged"
  285      fi
  286      say "system.cfg is ${state}; recovering"
  287      if restore; then
  288        recovered=1
  289      elif [ -n "${kept_tmp}" ]; then
  290        # Not reseeded: the defaults would be written through system.cfg.tmp,
  291        # the very file that is the good copy. The interface reads a whole
  292        # .tmp when the live file is cut (#307 PL-064).
  293        say "system.cfg is left as it is; system.cfg.tmp beside it is the good copy"
  294      else
  295        # Neither the live file nor the record is usable: the image's copy is
  296        # all that is left. The one file, not the whole config tree.
  297        if put "${DEFAULT_ROOT}/system/configs/system.cfg" "${CFG}"; then
  298          say "system.cfg was reseeded from the image defaults: there was no good copy to restore"
  299        else
  300          say "could not reseed system.cfg from the image defaults"
  301        fi
  302        recovered=1
  303      fi
  304    fi
  305  
  306    # Reseed what is missing from the config tree -- and only what is missing.
  307    #
  308    # This used to be `rsync -a /usr/config/ /storage/.config`, which also
  309    # replaced every file that merely differed from the image's copy:
  310    # es_settings.cfg, retroarch.cfg, the lot, whenever one retroarch file was
  311    # absent or system.cfg had lost its hostname line (#102's "defaults won").
  312    # --ignore-existing leaves every file that is present alone. An empty
  313    # retroarch file is not a config, so it is removed first and reseeded like
  314    # a missing one.
  315    local f missing=0
  316    for f in "${CONFIG_ROOT}/retroarch/retroarch-core-options.cfg" \
  317             "${CONFIG_ROOT}/retroarch/retroarch.cfg"; do
  318      if [ -e "${f}" ] && [ ! -s "${f}" ]; then
  319        rm -f "${f}"
  320      fi
  321      [ -s "${f}" ] || missing=1
  322    done
  323    if [ "${missing}" -eq 1 ] || [ "${recovered}" -eq 1 ]; then
  324      if rsync -a --ignore-existing "${DEFAULT_ROOT}/" "${CONFIG_ROOT}"; then
  325        say "reseeded missing files under ${CONFIG_ROOT} from the image; files already present were left alone"
  326      else
  327        say "could not reseed missing files under ${CONFIG_ROOT} from the image"
  328      fi
  329    fi
  330  }
  331  
  332  case ${1} in
  333    verify)
  334      verify
  335    ;;
  336    backup)
  337      backup
  338    ;;
```


## rocknix-evidence @ 8ebaf8daad: lines 47-88 (excerpt of 265)

```text
   47  device_label() {
   48    local model
   49    [ -r /proc/device-tree/model ] && model=$(tr -d '\0' < /proc/device-tree/model 2>/dev/null)
   50    [ -n "${model}" ] || model=$(cat /sys/class/dmi/id/product_name 2>/dev/null)
   51    [ -n "${model}" ] || model="device"
   52    printf '%s' "${model}" | sed -E 's/[^A-Za-z0-9]+/-/g; s/^-+//; s/-+$//' | cut -c1-40
   53  }
   54  
   55  section() { printf '\n===== %s\n' "$1"; }
   56  
   57  # One page of state. Every command is best-effort and time-boxed so a device
   58  # that is already struggling is not held up by its own diagnostics.
   59  write_snapshot() {
   60    echo "rocknix-evidence snapshot $(date '+%Y-%m-%d %H:%M:%S %Z')"
   61    echo "boot_id $(cat /proc/sys/kernel/random/boot_id 2>/dev/null)"
   62    echo "uptime $(cut -d' ' -f1 /proc/uptime 2>/dev/null)s   loadavg $(cat /proc/loadavg 2>/dev/null)"
   63    echo "build $(sed -n 's/^BUILD_ID=//p' /etc/os-release 2>/dev/null | tr -d '"')"
   64    section "memory"; free -m 2>/dev/null
   65    section "pressure"; for p in cpu memory io; do [ -r "/proc/pressure/${p}" ] && { printf '%s: ' "${p}"; head -1 "/proc/pressure/${p}"; }; done
   66    section "storage"; df -h /storage /tmp 2>/dev/null
   67    section "thermal"; for z in /sys/class/thermal/thermal_zone*; do [ -r "${z}/temp" ] && printf '%s %s %s\n' "$(basename "${z}")" "$(cat "${z}/type" 2>/dev/null)" "$(cat "${z}/temp" 2>/dev/null)"; done
   68    section "watchdog"; ls /sys/class/watchdog/ 2>/dev/null || echo "none"
   69    for w in /sys/class/watchdog/watchdog*; do [ -d "${w}" ] && printf '%s identity=%s state=%s timeout=%s\n' "$(basename "${w}")" "$(cat "${w}/identity" 2>/dev/null)" "$(cat "${w}/state" 2>/dev/null)" "$(cat "${w}/timeout" 2>/dev/null)"; done
   70    section "pstore (unread dumps)"; ls -la /sys/fs/pstore/ 2>/dev/null | tail -n +2
   71    section "processes"; timeout 10 top -b -n 1 2>/dev/null | head -25
   72    section "cloud sync"; ls -la /storage/.cache/cloud_sync/ 2>/dev/null | tail -n +2
   73    if flock -n /var/run/cloud_sync.lock true 2>/dev/null; then echo "lock: free"; else echo "lock: HELD (a sync is running)"; fi
   74    section "kernel, last 40 lines"; timeout 10 journalctl -k -n 40 --no-pager -o short-monotonic 2>/dev/null
   75  }
   76  
   77  # systemd-pstore.service archives a crash dump at boot, but its condition
   78  # (/sys/fs/pstore not empty) is checked about two seconds in, and on a UEFI
   79  # machine the previous boot's dump is not visible there yet: the panic left
   80  # fifteen chunks in the variable store and the service was skipped as "unmet
   81  # condition" while the chunks appeared a little later (VM, 2026-09-10).
   82  # ramoops on a handheld is visible from the first moment, so this is belt
   83  # and braces there -- but a dump left unread is the one piece of evidence
   84  # this whole tree exists for, so the first snapshot after boot archives
   85  # whatever the early service missed, with systemd's own tool.
   86  archive_unread_pstore() {
   87    [ -n "$(ls -A /sys/fs/pstore 2>/dev/null)" ] || return 0
   88    [ -x /usr/lib/systemd/systemd-pstore ] || return 0
```


## backuptool @ 8ebaf8daad: lines 272-308 (excerpt of 1899)

```text
  272  
  273  # es_systems.cfg / es_features.cfg are OS-managed symlinks into /usr/config;
  274  # backing up their content and restoring it as regular files would freeze the
  275  # systems list at the backup-time version, so they are deliberately excluded.
  276  #
  277  # /storage/.cache/bluetooth/* was in upstream's list and is not in this one,
  278  # on purpose (747362fe36, #18): Bluetooth link keys are a credential for one
  279  # adapter and useless on another. A restore on the same device keeps its
  280  # pairings -- it never touches that folder -- and a new device pairs its
  281  # controllers again. A legacy zip that still holds them puts them back, as
  282  # it always did (#308 claude F-BR-16).
  283  DEFAULT=(
  284      /storage/.config/fancontrol.conf
  285      /storage/.config/backuptool.conf
  286      /storage/.config/system/configs/system.cfg
  287      /storage/.config/ppsspp/*
  288      /storage/.config/retroarch/*
  289      /storage/.config/moonlight/*
  290      /storage/.config/game/*
  291      ${ESPATH}/es_settings.cfg
  292      ${ESPATH}/es_input.cfg
  293      ${ESPATH}/scripts/*
  294      ${ESPATH}/themesettings/*
  295      ${ESPATH}/collections/*
  296      # Player-supplied presentation assets. Not ROMs and not BIOS, so content
  297      # sync does not carry them; not saves either. They were in no tier at all
  298      # until this line, which is the kind of gap that is only discovered when
  299      # somebody restores a device and finds their overlays gone.
  300      #
  301      # They live here rather than in content sync because they are small and
  302      # change with the configuration they belong to. A large bezel pack is the
  303      # exception, and it will grow this archive -- which is uploaded whole on
  304      # every backup, so a player with hundreds of megabytes of overlays should
  305      # know that. See #45 on archive size generally.
  306      /storage/roms/bezels/*
  307      /storage/roms/themes/*
  308      # Systems whose content EmulationStation keeps outside /storage/roms.
```


## The first reader's grades of the first seat (GPT-6 Astra)

The other seat's 58 items were graded against the code; read them as the first reader's judgement, not as evidence. Refute a grade where the code says otherwise.

# GPT-6 Astra's 58 items, graded by the first reader

Each item was re-read at its lines in the full tree at the pin (and `8ebaf8daad` for the scripts), including the lines the packet did not carry. **Grades:** *accepted*, *in part* (what holds and what does not), *plausible* (not settled by reading), *rejected* (with the line). The new leads are L-23 to L-33 in `02` § Corrections and new leads from the seats.

| Item | Astra | Grade | The first reader's reading |
| --- | --- | --- | --- |
| SO-1 | narrowed | accepted | Arguments, not calls: `unzipFile` quotes source and destination; the PDF prefix derives from the file name. The generator's table counts calls; its "joined" column names every joined expression. |
| SO-2 | narrowed | accepted | L-01's reach is conditional: no name override, no existing MD5 above 1 MiB, a positive size, and archive hashing on, which `SystemData.cpp:2315-2325` leaves on for every system but seven arcade-class platforms. `getSevenZipCommand()` is `"7zr"` (`ApiSystem.h:422`). High stands. |
| SO-3 | refuted | in part | **The storage half is right about the code and wrong about reach:** the DEV branch stores the whole line (`GuiMenu.cpp:3127`), but `rocknix-config storage` exits 0 and prints nothing at `8ebaf8daad` (`:271-273`), so no line exists. My "safe by shape" was the wrong reason; the right one is no producer. The Bluetooth MAC is unvalidated, and its producer is the script's output. The bezel names are unvalidated. |
| SO-4 | new | accepted | `cloud_oauth` open, wait and close, the suspend query, PDF and download have no bound in this layer. It is a list, not a demonstrated freeze. |
| SO-5 | confirmed | accepted | The over-read runs to the next NUL; 15 bytes is one instance. |
| SO-6 | narrowed | accepted, and narrower | `overWriteMedias` is `ScrapeOverWrite && search.overWriteMedias` (`Scraper.cpp:400`), and the scrape page sets the latter false under GAMES MISSING ANY MEDIA (`GuiScraperStart.cpp:99`), the default filter (`Settings.cpp:224`). **L-03 is not reached by default**; it is reached under ALL GAMES or MISSING ALL MEDIA. |
| SO-7 | narrowed | accepted | `02`'s closure claimed a window confirmation that G6(c) never gave; corrected. A memory-mode `file://` request's bytes reach `getContent()` before the error. No memory-mode request in these files takes a server-supplied URL; the media path is file-mode. |
| SO-8 | narrowed | accepted | The closure depends on no `<stem>-image.<x>` directory or symlink existing on `/storage`. Not a containment guarantee. |
| SO-9 | new | accepted | The 429 retry rebuilds the request from URL and path (`Scraper.cpp:596`), dropping options. A design note for #1154's fix. |
| SO-10 | new | accepted | Certificate failures read as `YOU'RE NOT ONLINE` (`ScreenScraper.cpp:989-990`); `VERIFYHOST` 0 on the client-certificate path. Design notes for #1154. |
| SO-11 | narrowed | rejected in part | The popups' constructors are read (`GuiTextEditPopup.h:15-16`, `GuiTextEditPopupKeyboard.h:13-14`): neither takes a password parameter. The rest holds. |
| SO-12 | new | accepted | **New sink:** `set_settings` passes `SV<n>=<value>` as arguments to `env` (`001-functions:600-602`), so `join_wifi`'s key (`wifictl:460`) is in `env`'s argv while `awk` runs. `write_setting_line`'s `K`/`V` are environment, readable only as `/proc/<pid>/environ` by the same user. L-25. |
| SO-13 | narrowed | accepted | The compiled identity is the window's or the build's, not read. The cookie jar is 0644; its contents were not read. |
| SO-14 | refuted | accepted | **`02` was wrong:** `Scraper.cpp:524` logs the *media* download URL, not the API query. No line in these files logs the API URL with the pair or the account. `GuiMenu.cpp:8365` shows the restored ScreenScraper username in a row's label. Corrected in `02`. |
| SO-15 | confirmed | accepted | — |
| SO-16 | narrowed | accepted | The shell intersects with the umask (`001-functions:400-404`), so 0645 survives only under a umask of 022 or narrower in others' bits. "Kept by every writer" is withdrawn. The seed's build step is not traced, as `02` said. |
| SO-17 | confirmed | accepted | Plus: `chksysconfig` can end with no file when restore, reseed and rsync all fail. |
| SO-18 | narrowed | accepted | The lock protects only cooperating writers; `chksysconfig`'s `put` and the seed's `cp` do not take it. |
| SO-19 | new | accepted | `chksysconfig backup` writes `system.cfg.backup.tmp` (`:69-70`, `dst` the record), the name `SystemConf.cpp:210` removes at the interface's start, believing nothing else writes it. A start during a shutdown backup is unlikely; Low. L-29. |
| SO-20 | narrowed | accepted | A failed record write logs and returns success with the dirty flag cleared (`Settings.cpp:533-534`), so the record is not retried. L-30. |
| SO-21 | new | accepted | Any well-formed XML parses as settings (`Settings.cpp:566-601`), and the record is re-read from the path after the parse. Low. L-30. |
| SO-22 | refuted | accepted | "Last nonempty wins"; `getBool(..., true)` reads `0\r` as true. `02` § The readers corrected. |
| SO-23 | new | accepted, and **proved further** | **New High (L-23):** the HOSTNAME row saves an empty value with no check (`GuiSettings.cpp`, `updateVal`; `GuiMenu.cpp:9929`), `applyChanges` removes the line, and the record follows. At the next boot `chksysconfig verify` finds both copies without the sentinel and reseeds the image's defaults. The interface then records those defaults: **every setting is lost from both files** (`stage-c/positives/hostname-empty.out`, the pin's `SystemConf` and `8ebaf8daad`'s `chksysconfig`; the host's `grep` stands in for the image's). |
| SO-24 | new | accepted | `loadSystemConf` clears `mOnDisk` and the pending sets but not `confMap` (`SystemConf.cpp:148-152`), and the parse only adds. After an open network's join writes `wifi.key=`, the interface keeps the previous key in memory. What reads it next is not traced. L-26. |
| SO-25 | narrowed | accepted | The toast is `joined()` at `GuiWifi.cpp:403-413`: `CONNECTED`. Open networks are guarded. |
| SO-26 | new | accepted | `saved` with no device is an empty success; the Bluetooth bulk delete ignores its result. Low. L-33. |
| SO-27 | narrowed | accepted | The decoder defect is the reaped shell's; on the image `sh` is bash, which forks (T20's G02). |
| SO-28 | narrowed | accepted | As SO-2. |
| SO-29 | confirmed | accepted | — |
| SO-30 | narrowed | accepted | As SO-6: reached under the non-default filters. L-03 goes Low to Medium. |
| SO-31 | confirmed | accepted | — |
| SO-32 | narrowed | accepted | Memory-mode only; HTML transformed. |
| SO-33 | confirmed | accepted | — |
| SO-34 | confirmed | accepted | — |
| SO-35 | narrowed | accepted | Adds SO-12's sink. |
| SO-36 | confirmed | accepted | A leftover can be empty or partial; the lock's staging file holds a pid, not a credential. |
| SO-37 | confirmed | accepted | — |
| SO-38 | narrowed | accepted | — |
| SO-39 | confirmed | accepted | A bare-key fix would delete the hostname default; per-key reset semantics first (L-23 is the same family). |
| SO-40 | narrowed | accepted | — |
| SO-41 | narrowed | in part | The eight call sites are each read in the tree (§ The writers' generated rows); T18's fix is `f63ad4de4` on its branch, cited in the brief. |
| SO-42 | narrowed | accepted | As SO-24. |
| SO-43 | confirmed | accepted | — |
| SO-44 | confirmed | accepted | `ViewController.cpp:507-509` acts on it at launch. |
| SO-45 | narrowed | accepted | The eleven sites are R2's command output, each at its line. |
| SO-46 | confirmed | accepted | — |
| SO-47 | narrowed | accepted | An inventory, as `02` says. |
| SO-48 | narrowed | accepted | As SO-16. |
| SO-49 | narrowed | accepted | — |
| SO-50 | new | accepted | **New (L-24):** `int http_status_code; curl_easy_getinfo(..., CURLINFO_RESPONSE_CODE, &http_status_code)` (`HttpReq.cpp:432-433`), where curl writes a `long`: eight bytes into four, on every completed transfer, on the x86-64 guest and on aarch64 handhelds. |
| SO-51 | new | accepted | `closeStream` ignores `fflush`'s and `fclose`'s results; `renameFile` returns true when the source is absent (`FileSystemUtil.cpp:1451-1452`); two requests for one destination share `<path>.tmp`. L-28. |
| SO-52 | new | accepted | A cut live file not recognised as recoverable (newer than its record) is merged and saved whole without a record write (`SystemConf.cpp:336-339`), and the **next load records it** over the whole record (`AtomicFileUtil.cpp:352-361`), the cut keys gone. L-27. |
| SO-53 | new | accepted | `Settings`' recovery copies with the record's mode; its recording uses the live file's, which can widen a private record (`Settings.cpp:617`, `:629-631`). L-30. |
| SO-54 | new | accepted | An extraction that fails hands `md5sum` empty input, whose digest is accepted as the game's (`ApiSystem.cpp:1527-1530`); invalid user-info XML reads as one thread. L-31. |
| SO-55 | new | accepted | `sRecovered` is set when the write-back fails or the lock is busy; the sentence says RESTORED. L-32. |
| SO-56 | narrowed | plausible | Not settled here; `GuiLoading` holds raw `this`, and `BACK` is refused while `mWaitingLoad`. |
| SO-57 | new | accepted | The directory `fsync`'s failure is discarded (`AtomicFileUtil.cpp:29-37`); the header calls it best effort. A wording correction in `02`. |
| SO-58 | new | accepted | A lock budget is not a frame bound. Recorded for Q1 and the retro's time-to-play line. |

**Totals** (counted from the table): 58 items; 54 accepted (SO-6 and SO-23 further than Astra put them), 2 in part (SO-3, SO-41), 1 rejected in part (SO-11), 1 plausible (SO-56).
