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
| L-01 | Q1 | a command built from a player's string | A ROM's file name reaches `sh` inside double quotes, which leave `$`, backticks and `\` live. The scraper reaches this for a `.7z` up to 128 MB (`ScreenScraper.cpp:306-308` → `getMD5`), as root, unless the game has a name override, an existing MD5 above 1 MiB, or an empty file, or its system is one of the seven arcade-class platforms `SystemData.cpp:2315-2325` exempts (Astra SO-2). | `ApiSystem.cpp:1527-1528`, `:1578-1579`, `:1659-1660`; poppler at `:2509`, `:2593` | tree; the window's `$(...)` ROM and `ls /usr/bin/7z*` owed |
| L-02 | Q2 | a credential's sink | `header_callback` builds a `std::string` from curl's header buffer as if it ended in a NUL; curl's does not. | `HttpReq.cpp:583` | fixture: `stage-b/positives/lifted.out`, ASan heap-buffer-overflow, READ of size 15 from a 14-byte buffer |
| L-03 | Q4 | a state write that can lose the record | A download removes the file it will replace before a byte arrives. With `ScrapeOverWrite` on (`Settings.cpp:198`) **and** the scrape page's overwrite flag set, which the default filter GAMES MISSING ANY MEDIA clears (`Scraper.cpp:400`, `GuiScraperStart.cpp:99`, `Settings.cpp:224`; Astra SO-6), a re-scrape under ALL GAMES or MISSING ALL MEDIA whose download fails (404 and I/O errors ignored, `Scraper.cpp:631-635`) leaves the game with no art where it had some. | `HttpReq.cpp:344`, `:328` | tree; the window's 404 from the #1154 endpoint owed |
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
| L-21 | Q3 | a credential's sink | `system.cfg` and its `.backup` are 0645 on the image, and so is the seed it is copied from: world-readable, with the execute bit for others. `wifi.key` is in it, readable by any user. `AtomicFile::writeText` keeps a replaced file's mode (`AtomicFileUtil.cpp:127-147`). The shell's `prepare_settings_temp` keeps the shared bits of the live file and the record, less the umask (`001-functions:385-404`): under the image's umask the 0645 survives (Astra SO-16 withdrew the universal form). Git records the seed as `100644` at `8ebaf8daad` and no recipe `chmod`s it; the installed seed also differs in content (`g01-image-vs-tree.txt`), so a build step rewrites it, and that step's mode is the 0645. Which step is not traced here. | the image's `/usr/config/system/configs/system.cfg` | guest: `g02-modes.txt`, `g03-argv.txt` |
| L-22 | Q6 | a check whose failure reads as success | `wifictl` exits 0 when it has no Wi-Fi device (`:55-56`, T1's file). `ApiSystem::enableWifi` reads that as a connect (`:627-637`, `system() == 0`), and the page then saves `wifi.ssid` and `wifi.key` and says CONNECTED (`GuiWifi.cpp:385-395`). A handheld whose Wi-Fi driver did not load says it joined. | `wifictl:55-56`; `ApiSystem.cpp:627-637`; `GuiWifi.cpp:385-395` | guest: the connect exited 0 with no adapter (`g03-argv.txt`); the page's half is tree |
| L-20 | Q7 | — | 82 of the 143 command rows name a script the distribution does not ship at `8ebaf8daad` (§ The commands' last column). A table, recorded as written (D-WORKFLOW-209's shape). | § The commands | tool-run |

**Read and closed at stage B:**
- **`file://` from a server's media URL:** the transfer leaves curl a response code of 0. `status()` takes that to `REQ_IO_ERROR` (`HttpReq.cpp:435-473`), and the destructor removes the `.tmp` the bytes reached (`:377-378`). So a local file's text reaches only a transient temporary. Proved by tree. The window's confirmation (G6(c)) was not run and is `CANNOT` for the slice. A memory-mode request's bytes still reach `getContent()` before the error (Astra SO-7); no memory-mode request in these files takes a server-supplied URL.
- **The server's `format` and `Content-Type` as a path:** `getSaveAsPath` appends them (`Scraper.cpp:779-812`, `:646-676`), but `getGenericPath` does not resolve `..` (`FileSystemUtil.cpp:642-668`). A kernel lookup through `<stem>-image.` fails, since no such directory exists. Proved by tree.
- **The Bluetooth and storage arguments:** they are joined bare (`ApiSystem.cpp:800-816`, `:984`), but each is the first token of a script's own output, a MAC address or a storage id (`GuiBluetoothDevices.cpp:131-137`, `GuiMenu.cpp:3130-3151`). Safe by shape, not by quoting. Proved by tree.
- **`maskSecrets`' `--key`:** excluded on purpose, so `batocera-hotkeys --key` keeps its key name (`StringUtil.cpp:788`; `80f52e500`, #177). Proved by history.
- **The kill-the-writer test (D-CLOUD-078):**
  - every one of 99 kill points across `writeText`, `Settings`' two writes and `SystemConf`'s save leaves the old or the new state whole (`kill-writer.out`);
  - the shell writer killed mid-write, before the rename and after it leaves the old or the new file whole (`shell-writers.out` K1-K3).

  Proved by fixture.

## Corrections and new leads from the seats

**From GPT-6 Astra** (`second-opinions/astra-audit.md`, graded in `stage-c/astra-grades.md`).

**Corrected in place above:**
- L-01's reach (SO-2) and L-03's, which is not the default (SO-6);
- the `file://` closure's wording (SO-7);
- the credentials' log rows: no API URL is logged (SO-14);
- the restored username on screen (SO-14), and the `env` argv sink (SO-12);
- L-21's universal claim (SO-16);
- the readers' duplicate and carriage-return rows (SO-22).

**The storage closure:** right in outcome and wrong in reason. The row stores the whole line (`GuiMenu.cpp:3127`), but `rocknix-config storage` prints nothing at `8ebaf8daad` (`:271-273`), so nothing reaches `setStorage` (SO-3).

**New leads:**

| Lead | Q | Family | What | Where | proved |
| --- | --- | --- | --- | --- | --- |
| L-23 | Q4 | a state write that can lose the record | **Clearing the HOSTNAME row loses every setting.** The row saves an empty value unchecked; `applyChanges` removes the line from the file and the record; the next boot's `chksysconfig verify` finds both without the sentinel and reseeds the image's defaults; the interface's next start records them over the player's record (SO-23). | `GuiSettings.cpp` `addInputTextConfigRow`'s `updateVal`; `GuiMenu.cpp:9929`; `SystemConf.cpp:386-396`; `chksysconfig:57-62`, `:278-303` | fixture: `stage-c/positives/hostname-empty.out` (the pin's `SystemConf`; `8ebaf8daad`'s `chksysconfig`, the host's `grep` standing in for the image's) |
| L-24 | Q2 | a check whose failure reads as success | `CURLINFO_RESPONSE_CODE` is read into an `int`; curl writes a `long`, eight bytes into four, on every completed transfer (SO-50). | `HttpReq.cpp:432-433` | tree |
| L-25 | Q3 | a credential's sink | A saved network's key is argv of `env` during `set_settings` (SO-12). The writer is T1's. | `001-functions:600-602`; `wifictl:460` | tree |
| L-26 | Q5 | a check whose failure reads as success | A reload keeps keys the file no longer holds: after an open network's join writes `wifi.key=`, the previous network's key stays in the interface's memory (SO-24). | `SystemConf.cpp:73-80`, `:148-179` | tree |
| L-27 | Q4 | a state write that can lose the record | A cut live file newer than its record is merged and saved whole without a record write, and the next load records it over the whole record, the cut keys gone (SO-52). | `AtomicFileUtil.cpp:343-361`, `:522-539`; `SystemConf.cpp:336-339` | tree |
| L-28 | Q2 | a check whose failure reads as success | A download is called successful without a whole artifact: `fflush` and `fclose` unchecked, `renameFile` true for an absent source, and one `.tmp` shared by requests for one path (SO-51). | `HttpReq.cpp:326-344`, `:361-368`, `:477-506`; `FileSystemUtil.cpp:1448-1463` | tree |
| L-29 | Q4 | a state write that can lose the record | The interface's start removes `system.cfg.backup.tmp`, which `chksysconfig backup` writes (SO-19). | `SystemConf.cpp:203-210`; `chksysconfig:67-70` | tree |
| L-30 | Q4, Q5 | a state write that can lose the record | `Settings`: a failed record write is not retried; any well-formed XML is taken as settings and becomes the record; the recovery copy takes the record's mode and the recording the live file's (SO-20, SO-21, SO-53). | `Settings.cpp:533-534`, `:566-632` | tree |
| L-31 | Q6 | a check whose failure reads as success | A failed `7zr` extraction hands `md5sum` empty input, and its digest is stored as the game's; invalid user-info XML reads as one thread (SO-54). | `ApiSystem.cpp:1527-1530`; `ScreenScraper.cpp:1075-1089` | tree |
| L-32 | Q5 | a check whose failure reads as success | The player is told RESTORED when the write-back failed or the lock was busy (SO-55). | `SystemConf.cpp:221-265`; `Settings.cpp:615-619`; `main.cpp:1041-1042` | tree |
| L-33 | Q6 | a check whose failure reads as success | `wifictl saved` with no device is an empty success to both readers; the Bluetooth bulk delete ignores its result (SO-26). | `ApiSystem.cpp:687-705`; `GuiWifi.cpp:548-569`; `GuiBluetoothDevices.cpp:117-121` | tree |

**From Gemini 4 Argon** (`second-opinions/argon-audit.md`, graded in `stage-c/argon-grades.md`; Argon saw the grades of Astra).

**Independent confirmations:**
- L-23, the empty HOSTNAME (Argon SO-14);
- L-24, the response-code write (Argon SO-41).

**Widened:**
- **L-01:** `getMD5` runs `7zr` a second time through `unzipFile` when the first answer is unusable, and a `.m3u`'s first content file is what gets hashed (SO-1, SO-2). Its `Already written:` line: a failed extraction has already stored the empty input's digest as a game's MD5 (SO-19).
- **L-21:** the same 0645 `system.cfg` holds `root.password` and the RetroAchievements password, and `es_settings.cfg` at 0644 holds the scraper's pair and account (SO-11, SO-39). Both readers AND the copies' modes, so the fix chmods the existing files (SO-12).
- **L-28:** `renameFile` removes its destination before the rename (SO-42).
- **L-31:** `getCRC32`'s empty `CRC = ` entry, and a `Retry-After` date read as 0 ms (SO-43).

**New:**

| Lead | Q | Family | What | Where | proved |
| --- | --- | --- | --- | --- | --- |
| L-34 | Q4 | a state write that can lose the record | `applyChanges` rewrites a `#k=` line as a live `k=` line beside the real one, misses a first key behind a BOM and appends it again, and writes a literal `key=default` for a new key set to `default` (SO-17). | `SystemConf.cpp:373-407` | tree |
| L-35 | Q4 | — | `GuiLoading` completions hold raw `this` (`GuiWifi.cpp:314`, `:350`, `:382`); the Bluetooth page's worker writes `mWaitingLoad`, which the interface thread reads (`GuiBluetoothDevices.cpp:127`, `:150`): a data race by reading; the lifetime is plausible, not settled (SO-44, Astra SO-56). | as named | tree |
| L-36 | Q6 | a check whose failure reads as success | A 501 to 504, or redirects exhausted, reads as `YOU'RE NOT ONLINE` to an online player (SO-45). | `HttpReq.cpp:462-469`; `ScreenScraper.cpp:989-990` | tree |

**Design notes for #1154's question at the pause:**
- the 429 retry rebuilds the request without its options, so a media-only exception would be lost (SO-9);
- certificate failures read as `YOU'RE NOT ONLINE` (SO-10);
- `VERIFYHOST` 0 rides with client certificates (SO-10).

**Wording:** the directory `fsync`'s failure is discarded, so "the rename itself survives a power cut" is best effort (SO-57). A five-second lock budget is not a frame bound (SO-58).

## The credentials' paths

One row per credential kind per sink it can reach. Read at the lines named; values are never printed, names and lines only.

| Credential | Sink | At | Mask there | proved |
| --- | --- | --- | --- | --- |
| The Wi-Fi key | argv, during a saved network's join | `set_settings` passes `SV<n>=<value>` as arguments to `env` (`001-functions:600-602`), so `join_wifi`'s key (`wifictl:460`) is in `env`'s argv while `awk` runs (Astra SO-12, L-25) | none | tree |
| The Wi-Fi key | argv | `ApiSystem.cpp:635-637` → `system()` `:2328`: `sh -c`, `timeout 150`, `wifictl connect`; then `connect_wifi`'s `nmcli -w 90 device wifi connect "${SSID}" password "${PSK}"` (`wifictl:177`) | none on argv | tree; guest: 3 processes carried the key in their command lines (`guest-cycle/g03-argv.txt`) |
| The netplay network's fixed key | argv and the keyfile | `create_adhoc`'s and `connect_adhoc_client`'s `802-11-wireless-security.psk "${PSK}"` (`wifictl:195`, `:209`): the sink the brief's pattern missed. They run only when `wifi.adhoc.enabled` is 1 (`:502-511`), where `PSK` is replaced by a fixed value (`:63-66`), so the player's key does not reach them. | none | tree |
| The Wi-Fi key | a file and its mode | `system.cfg` `wifi.key`, written by the page (`GuiWifi.cpp:392-394`) and by `join_wifi`'s `set_settings wifi.ssid ... wifi.key "${psk}"` (`wifictl:460`). The mode is the live file's, or 0644 when ES makes the file new (`AtomicFileUtil.cpp:115`). On the image, **`system.cfg`, its `.backup` and the shipped seed are 0645** (L-21). NetworkManager's own keyfile is 0600. | none at rest | tree; guest (`g02-modes.txt`, `g03-argv.txt`) |
| The Wi-Fi key | a log | the command line through `maskSecrets` (`ApiSystem.cpp:2325`; the `wifictl` rule `StringUtil.cpp:764-784`). The child's stdout inherits ES's, which is the journal. | masked (the command line); what `wifictl` prints is unread | tree |
| The Wi-Fi key | the evidence page | `rocknix-evidence:71`'s `top -b -n 1`, every five minutes (D-SYS-005) | none | tree; guest: 0 of `top`'s 25 lines carried it at the sampled moment, with no adapter; on a device the key lives up to 90 s in `nmcli`'s argv, which the guest cannot show |
| The Wi-Fi key | the screen | the WI-FI KEY popup, typed in the clear (`GuiWifi.cpp:365`, `:367`). Neither popup class takes a password mode (`GuiTextEditPopup.h:15-16`, `GuiTextEditPopupKeyboard.h:13-14`). | none | tree |
| The Wi-Fi key | the packet and the archive | `system.cfg` in the settings archive (`backuptool:286`; its SECRETLIST is T17's, cited) | backuptool's | tree (cited) |
| The scraper's developer pair, compiled | the binary | `SCREENSCRAPER_DEV_LOGIN` returned verbatim (`ScreenScraper.cpp:36-37`), D-WORKFLOW-166's allowed case. Which identity is compiled is the window's to read by name, never printed. | n/a | tree |
| The scraper's developer pair, runtime | a file and its mode | `ScreenScraperDevId`, `ScreenScraperDevPass` in `es_settings.cfg` (`:39-43`), 0644 when new | none at rest | tree |
| Both developer pairs | a query | `devid=..&devpassword=..` at the head of every API URL (`:859-871`, `:885-888`, `:1030-1031`) | n/a (in the URL) | tree |
| Both developer pairs | a log | no line in these files logs an API URL. `Scraper.cpp:524` logs the *media* download URL through `maskSecrets` at LogDebug, which carries the pair only if the server put it there (corrected by Astra SO-14). | n/a | tree |
| Both developer pairs | the unverified peer | `api.screenscraper.fr` over https, with `VERIFYPEER` 0 (`HttpReq.cpp:192`, #1154) | none | tree; the window's #1154 positive owed |
| The player's ScreenScraper account | a file and its mode | `ScreenScraperUser`, `ScreenScraperPass` in `es_settings.cfg` (`storeInSettings=true`, `GuiScraperStart.cpp:413-420`, `GuiMenu.cpp:8371`, `:8374`), 0644 when new; a kill's leftover temporary too (L-09) | none at rest | tree, fixture |
| The player's ScreenScraper account | a query | `&ssid=&sspassword=` when both are set (`ScreenScraper.cpp:874-878`, `:890-894`) | n/a | tree |
| The player's ScreenScraper account | a log | no API URL is logged (Astra SO-14); `screenScraperFailureMessage` logs the server's body (`ScreenScraper.cpp:980`), as does `HttpReq::onError` for 400-503 (L-05) | n/a; the body unmasked | tree |
| The player's ScreenScraper account | the unverified peer | as the pair (#1154) | none | tree |
| The player's ScreenScraper account | the screen | the password rows are masked (`addInputTextConfigRow(..., true)`); the restored account's row shows the username in its label (`GuiMenu.cpp:8365`, Astra SO-14) | the password masked, the username not | tree |
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
| 183 | `setOverscan` | `executeScript` | `rocknix-config overscan ` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-config` | yes |
| 191 | `setOverclock` | `executeScript` | `batocera-overclock set ` | mode) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-overclock` | no |
| 197 | `areCpuMitigationsEnabled` | `executeScript` | `batocera-mitigations status` | - | none joined | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `batocera-mitigations` | no |
| 207 | `setCpuMitigationsEnabled` | `executeScript` | `batocera-mitigations ` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-mitigations` | no |
| 218 | `updateSystem` | `popen` | `rocknix-update` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `rocknix-update` | yes |
| 250 | `backupSystem` | `popen` | `rocknix-sync sync ` | device | bare | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `rocknix-sync` | no |
| 279 | `installSystem` | `popen` | `batocera-install install ` | architecture, device | bare | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `batocera-install` | no |
| 308 | `scrape` | `popen` | `rocknix-scraper` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `rocknix-scraper` | yes |
| 344 | `ping` | `executeScript` | `timeout 5 sh -c 'ping -c 1 -W 2 -t 255 8.8.8.8 \|\| ping -c 1 -W 2 -t ` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `ping` | base tool |
| 350 | `torrentIsReadyForUpdate` | `popen` | `batocera-upgrade-torrent --is-file-ready-to-update` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `batocera-upgrade-torrent` | no |
| 368 | `torrentStatus` | `executeEnumerationScript` | `batocera-upgrade-torrent --status` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-upgrade-torrent` | no |
| 381 | `torrentUpdateSystem` | `popen` | `batocera-upgrade-torrent --upgrade` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `batocera-upgrade-torrent` | no |
| 411 | `canLocalUpdate` | `popen` | `batocera-upgrade --check-media-upgrade` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `batocera-upgrade` | no |
| 429 | `canArchitectureUpdate` | `popen` | `batocera-architecture-compatibility` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `batocera-architecture-compatibility` | no |
| 458 | `canUpdate` | `popen` | `rocknix-update check` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `rocknix-update` | yes |
| 511 | `launchControlcenter` | `system` | `batocera-controlcenter` | - | none joined | none (inherits stdout) | the caller's | the caller's |  | `batocera-controlcenter` | no |
| 524 | `launchKodi` | `system` | `batocera-kodi ` | commandline | bare | none (inherits stdout) | WIFEXITED then WEXITSTATUS | the caller's |  | `batocera-kodi` | no |
| 573 | `launchCloudSignIn` | `system` | `` | phoneKeyboard | a variable: the command built earlier | none (inherits stdout) | the caller's | the caller's |  | `-` | - |
| 584 | `launchCloudSignIn` | `system` | `/usr/bin/cloud_oauth wait` | - | none joined | none (inherits stdout) | WIFEXITED then WEXITSTATUS | the caller's |  | `/usr/bin/cloud_oauth` | yes |
| 593 | `launchCloudSignIn` | `system` | `/usr/bin/cloud_oauth close` | - | none joined | none (inherits stdout) | the caller's | the caller's |  | `/usr/bin/cloud_oauth` | yes |
| 606 | `launchFileManager` | `system` | `filemanagerlauncher` | - | none joined | none (inherits stdout) | WIFEXITED then WEXITSTATUS | the caller's |  | `filemanagerlauncher` | binary: the window's ls |
| 627 | `enableWifi` | `executeScript` | `timeout 30 wifictl enable` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 635 | `enableWifi` | `executeScript` | `timeout 150 wifictl connect ` | Utils::String::shellQuote(country)), Utils::String::shellQuo | shellQuote | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 642 | `enableWifi` | `executeScript` | `wifictl enable ` | Utils::String::shellQuote(key)), Utils::String::shellQuote(s | shellQuote | none (system) | system() == 0 (:2328) | the caller's | WIN32 only | `wifictl` | yes |
| 651 | `getWifiSecurity` | `executeScript` | `timeout 15 wifictl security ` | Utils::String::shellQuote(ssid) | shellQuote | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 660 | `connectOpenWifi` | `executeScript` | `timeout 120 wifictl connect-open ` | Utils::String::shellQuote(ssid)) | shellQuote | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 665 | `disableWifi` | `executeScript` | `timeout 30 wifictl disable` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 677 | `getCurrentWifiSsid` | `executeScript` | `timeout 10 wifictl current` | - | none joined | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 690 | `getSavedWifiNetworks` | `executeScript` | `timeout 15 wifictl saved --ssid` | - | none joined | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 714 | `joinWifiNetwork` | `executeScript` | `timeout 120 wifictl join ` | Utils::String::shellQuote(name) | shellQuote | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 728 | `forgetWifiNetwork` | `executeScript` | `timeout 30 wifictl forget ` | Utils::String::shellQuote(name) | shellQuote | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 763 | `isWifiAPModeSupported` | `executeScript` | `timeout 10 wifictl has_ap_mode` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 767 | `getSavedWifiNetworks` | `executeEnumerationScript` | `wifictl list_saved` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `wifictl` | yes |
| 771 | `forgetWifiNetwork` | `executeScript` | `wifictl forget_saved ` | Utils::String::shellQuote(ssid)) | shellQuote | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 775 | `connectSavedWifiNetwork` | `executeScript` | `wifictl connect_saved ` | Utils::String::shellQuote(ssid)) | shellQuote | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 780 | `enableBluetooth` | `executeScript` | `rocknix-bluetooth enable 2>&1 >/dev/null` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 785 | `disableBluetooth` | `executeScript` | `rocknix-bluetooth disable` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 790 | `startBluetoothLiveDevices` | `executeScript` | `rocknix-bluetooth live_devices` | - | none joined | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `rocknix-bluetooth` | yes |
| 795 | `stopBluetoothLiveDevices` | `executeScript` | `rocknix-bluetooth stop_live_devices` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 800 | `pairBluetoothDevice` | `executeScript` | `rocknix-bluetooth trust ` | deviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 805 | `connectBluetoothDevice` | `executeScript` | `rocknix-bluetooth connect ` | deviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 810 | `disconnectBluetoothDevice` | `executeScript` | `rocknix-bluetooth disconnect ` | deviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 815 | `removeBluetoothDevice` | `executeScript` | `rocknix-bluetooth remove ` | deviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 820 | `scanNewBluetooth` | `executeScript` | `rocknix-bluetooth trust input` | - | none joined | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `rocknix-bluetooth` | yes |
| 825 | `getPairedBluetoothDeviceList` | `executeEnumerationScript` | `rocknix-bluetooth list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-bluetooth` | yes |
| 830 | `getAvailableStorageDevices` | `executeEnumerationScript` | `rocknix-config storage list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-config` | yes |
| 836 | `getVideoModes` | `executeEnumerationScript` | `batocera-resolution listModes` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-resolution` | no |
| 838 | `getVideoModes` | `executeEnumerationScript` | `batocera-resolution --screen \"` | output | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-resolution` | no |
| 844 | `getCustomRunners` | `executeEnumerationScript` | `batocera-wine-runners` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-wine-runners` | no |
| 849 | `getAvailableBackupDevices` | `executeEnumerationScript` | `rocknix-sync list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-sync` | no |
| 854 | `getAvailableInstallDevices` | `executeEnumerationScript` | `batocera-install listDisks` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-install` | no |
| 859 | `getAvailableInstallArchitectures` | `executeEnumerationScript` | `batocera-install listArchs` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-install` | no |
| 864 | `getAvailableOverclocking` | `executeEnumerationScript` | `echo no` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `echo` | base tool |
| 869 | `getSystemInformations` | `executeEnumerationScript` | `rocknix-info --full` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-info` | yes |
| 886 | `getBiosInformations` | `executeEnumerationScript` | `rocknix-systems` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-systems` | yes |
| 929 | `generateSupportFile` | `executeScript` | `batocera-support` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-support` | no |
| 942 | `getCurrentStorage` | `popen` | `rocknix-config storage current` | - | none joined | fgets in the caller | pclose, status unread | the caller's |  | `rocknix-config` | yes |
| 984 | `setStorage` | `executeScript` | `rocknix-config storage ` | selected) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-config` | yes |
| 989 | `setButtonColorGameForce` | `executeScript` | `batocera-gameforce buttonColorLed ` | selected) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-gameforce` | no |
| 994 | `setPowerLedGameForce` | `executeScript` | `batocera-gameforce powerLed ` | selected) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-gameforce` | no |
| 1026 | `forgetBluetoothControllers` | `executeScript` | `rocknix-config forgetBT` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-config` | yes |
| 1041 | `getAvailableVideoOutputDevices` | `executeEnumerationScript` | `rocknix-config lsoutputs` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-config` | yes |
| 1052 | `getAvailableAudioOutputDevices` | `executeEnumerationScript` | `set-audio list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `set-audio` | no |
| 1059 | `getAvailableChannels` | `executeEnumerationScript` | `timeout 5 /usr/bin/sh -lc \"/usr/bin/wifictl channels\"` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `/usr/bin/wifictl` | yes |
| 1064 | `getAvailableCpuGovernors` | `executeEnumerationScript` | `/usr/bin/sh -lc \"echo \\\"default\\\"; tr \\\" \\\" \\\"\\n\\\" < /sy` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `echo` | base tool |
| 1069 | `getAvailableGpuGovernors` | `executeEnumerationScript` | `/usr/bin/sh -lc \". /etc/profile.d/099-freqfunctions; get_available_gp` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `.` | no |
| 1080 | `getAvailableDisplayModes` | `executeEnumerationScript` | `/usr/bin/sh -lc \"/usr/bin/wlr-randr \| awk '/Modes/{flag=1;next}/Posi` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `/usr/bin/wlr-randr` | binary: the window's ls |
| 1091 | `getAvailableColors` | `executeEnumerationScript` | `/usr/bin/sh -lc \"/usr/bin/ledcontrol list\"` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `/usr/bin/ledcontrol` | yes |
| 1096 | `getSleepModes` | `executeEnumerationScript` | `/usr/bin/sh -lc \"echo \\\"default\\\"; tr \\\" \\\" \\\"\\n\\\" </sys` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `echo` | base tool |
| 1109 | `getCurrentAudioOutputDevice` | `popen` | `set-audio get` | - | none joined | fgets in the caller | pclose, status unread | the caller's |  | `set-audio` | no |
| 1132 | `setAudioOutputDevice` | `system` | `set-audio set` | selected | single quotes | none (inherits stdout) | the caller's | the caller's |  | `set-audio` | no |
| 1147 | `getAvailableAudioOutputProfiles` | `executeEnumerationScript` | `set-audio list-profiles` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `set-audio` | no |
| 1160 | `getCurrentAudioOutputProfile` | `popen` | `set-audio get-profile` | - | none joined | fgets in the caller | pclose, status unread | the caller's |  | `set-audio` | no |
| 1183 | `setAudioOutputProfile` | `system` | `set-audio set-profile` | selected | single quotes | none (inherits stdout) | the caller's | the caller's |  | `set-audio` | no |
| 1459 | `getBatoceraBezelsList` | `executeEnumerationScript` | `rocknix-es-thebezelproject list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-es-thebezelproject` | yes |
| 1484 | `installBatoceraBezel` | `executeScript` | `rocknix-es-thebezelproject install ` | bezelsystem | bare | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `rocknix-es-thebezelproject` | yes |
| 1489 | `uninstallBatoceraBezel` | `executeScript` | `rocknix-es-thebezelproject remove ` | bezelsystem | bare | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `rocknix-es-thebezelproject` | yes |
| 1528 | `getMD5` | `executeEnumerationScript` | `7zr x -so \"` | fileName | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `7zr` | binary: the window's ls |
| 1579 | `getCRC32` | `executeEnumerationScript` | `7zr l -slt \"` | fileName | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `7zr` | binary: the window's ls |
| 1660 | `unzipFile` | `executeScript` | `7zr x \"` | Utils::FileSystem::getPreferredPath(destFolder), Utils::File | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `7zr` | binary: the window's ls |
| 1825 | `getLED` | `executeScript` | `batocera-led-handheld block_color_changes` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 1831 | `getLED` | `executeScript` | `batocera-led-handheld block_color_changes` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 1852 | `getLED` | `executeScript` | `batocera-led-handheld block_color_changes` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 1861 | `getLED` | `executeScript` | `batocera-led-handheld block_color_changes` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 1924 | `setLEDColours` | `executeScript` | `batocera-led-handheld set_color_force_dec ` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 2163 | `setLEDMode` | `executeScript` | `batocera-led-handheld unblock_color_changes` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 2166 | `setLEDMode` | `executeScript` | `batocera-led-handheld rainbow` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 2168 | `setLEDMode` | `executeScript` | `batocera-led-handheld chroma` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 2170 | `setLEDMode` | `executeScript` | `batocera-led-handheld pulse` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 2230 | `getWifiNetworks` | `executeEnumerationScript` | `timeout 45 wifictl scanlist` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `wifictl` | yes |
| 2257 | `executeScriptLegacy` | `executeScriptLegacy` | `` | command | a variable: the command built earlier | every line to func | WEXITSTATUS without WIFEXITED (:2291) | the caller's |  | `-` | - |
| 2413 | `isScriptingSupported` | `executeScript` | `/usr/bin/pm-is-supported --suspend` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `/usr/bin/pm-is-supported` | no |
| 2488 | `getFormatDiskList` | `executeEnumerationScript` | `batocera-format listDisks` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-format` | no |
| 2499 | `getFormatFileSystems` | `executeEnumerationScript` | `batocera-format listFstypes` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-format` | no |
| 2504 | `formatDisk` | `executeScript` | `batocera-format format ` | disk, format | bare | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `batocera-format` | no |
| 2509 | `getPdfPageCount` | `executeEnumerationScript` | `pdfinfo \"` | fileName | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `pdfinfo` | binary: the window's ls |
| 2591 | `extractPdfImages` | `executeEnumerationScript` | `pdftoppm -r ` | fileName, page, pdfFolder, prefix, squality | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's | WIN32 only | `pdftoppm` | binary: the window's ls |
| 2593 | `extractPdfImages` | `executeEnumerationScript` | `pdftoppm -jpeg -r ` | fileName, page, pdfFolder, prefix, squality | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `pdftoppm` | binary: the window's ls |
| 2622 | `getBatoceraStorePackages` | `executeEnumerationScript` | `batocera-store list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-store` | no |
| 2691 | `installBatoceraStorePackage` | `executeScript` | `batocera-store install \"` | name | double quotes | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `batocera-store` | no |
| 2696 | `uninstallBatoceraStorePackage` | `executeScript` | `batocera-store remove \"` | name | double quotes | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `batocera-store` | no |
| 2701 | `refreshBatoceraStorePackageList` | `executeScript` | `batocera-store refresh` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-store` | no |
| 2702 | `refreshBatoceraStorePackageList` | `executeScript` | `batocera-store clean-all` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-store` | no |
| 2707 | `callBatoceraPreGameListsHook` | `executeScript` | `batocera-preupdate-gamelists-hook` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-preupdate-gamelists-hook` | no |
| 2712 | `updateBatoceraStorePackageList` | `executeScript` | `batocera-store update` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-store` | no |
| 2823 | `getCurrentTimezone` | `executeEnumerationScript` | `batocera-timezone get` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-timezone` | no |
| 2827 | `getCurrentTimezone` | `executeEnumerationScript` | `batocera-timezone detect` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-timezone` | no |
| 2837 | `setTimezone` | `executeScript` | `batocera-timezone set \"` | tz | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-timezone` | no |
| 2846 | `getPadsInfo` | `executeEnumerationScript` | `batocera-padsinfo` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-padsinfo` | no |
| 2899 | `getRunningArchitecture` | `executeEnumerationScript` | `uname -m` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `uname` | base tool |
| 2908 | `getRunningBoard` | `executeEnumerationScript` | `cat /boot/boot/batocera.board` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `cat` | base tool |
| 2927 | `emuKill` | `executeScript` | `batocera-es-swissknife --emukill` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-es-swissknife` | no |
| 2933 | `suspend` | `executeScript` | `/usr/sbin/pm-suspend` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `/usr/sbin/pm-suspend` | no |
| 2939 | `replugControllers_sindenguns` | `executeScript` | `/usr/bin/virtual-sindenlightgun-remap` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `/usr/bin/virtual-sindenlightgun-remap` | no |
| 2945 | `replugControllers_wiimotes` | `executeScript` | `/usr/bin/virtual-wii-mouse-bar-remap` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `/usr/bin/virtual-wii-mouse-bar-remap` | no |
| 2951 | `replugControllers_steamdeckguns` | `executeScript` | `/usr/bin/steamdeckgun-remap` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `/usr/bin/steamdeckgun-remap` | no |
| 2956 | `isPlaneMode` | `executeEnumerationScript` | `batocera-planemode status` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-planemode` | no |
| 2971 | `setPlaneMode` | `executeScript` | `batocera-planemode ` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-planemode` | no |
| 2980 | `getServices` | `executeEnumerationScript` | `batocera-services list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-services` | no |
| 3001 | `getJoysticksHotkeys` | `executeEnumerationScript` | `batocera-joysticks-hotkeys` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-joysticks-hotkeys` | no |
| 3044 | `getJoysticksHotkeysValues` | `executeEnumerationScript` | `batocera-joysticks-hotkeys --values` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-joysticks-hotkeys` | no |
| 3052 | `getGlobalHotkeysValues` | `executeEnumerationScript` | `batocera-hotkeys --values` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-hotkeys` | no |
| 3095 | `setJoysticksHotkeys` | `executeScript` | `batocera-joysticks-hotkeys ` | params) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-joysticks-hotkeys` | no |
| 3103 | `detectGlobalHotkeys` | `executeEnumerationScript` | `batocera-hotkeys --detect` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-hotkeys` | no |
| 3147 | `getGlobalHotkeys` | `executeEnumerationScript` | `batocera-hotkeys` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-hotkeys` | no |
| 3203 | `getKeyboardtopads` | `executeEnumerationScript` | `keyboardToPads --search` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `keyboardToPads` | no |
| 3251 | `getKeyboardtopadDevices` | `executeEnumerationScript` | `keyboardToPads --config \"` | config | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `keyboardToPads` | no |
| 3306 | `setGlobalHotkey` | `executeScript` | `batocera-hotkeys --set --config ` | action), config, key | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-hotkeys` | no |
| 3311 | `removeGlobalHotkey` | `executeScript` | `batocera-hotkeys --remove --config ` | config, key) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-hotkeys` | no |
| 3319 | `getKeyboardtopadKeyValues` | `executeEnumerationScript` | `batocera-hotkeys --values` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-hotkeys` | no |
| 3380 | `saveKeyboardtopads` | `executeScript` | `` | cmd_dev) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `-` | - |
| 3404 | `saveKeyboardtopads` | `executeScript` | `` | cmd_dev) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `-` | - |
| 3416 | `detectEvKey` | `executeEnumerationScript` | `batocera-hotkeys --detect --count 1 --nowait --evformat --device ` | device_path) | bare | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-hotkeys` | no |
| 3454 | `backglassThemes` | `executeEnumerationScript` | `batocera-backglass list-themes` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-backglass` | no |
| 3465 | `restartBackglass` | `executeScript` | `/usr/bin/batocera-backglass restart` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `/usr/bin/batocera-backglass` | no |
| 3476 | `enableService` | `executeScript` | `batocera-services ` | serviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-services` | no |
| 3478 | `enableService` | `executeScript` | `batocera-services ` | serviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-services` | no |
| 3485 | `getEjectableDrives` | `executeEnumerationScript` | `batocera-storage-manager list_ejectable` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-storage-manager` | no |
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
| es-app/src/SaveStateBookkeeper.cpp:64 | isFlockHeld | read (an flock question) | - | - | asks the cloud transfer's flock | - | - | - |
| es-app/src/SaveStateBookkeeper.cpp:71 | isFlockHeld | read (an flock question) | - | - | asks the cloud transfer's flock | - | - | - |
| es-app/src/SaveStateBookkeeper.cpp:85 | isFlockHeld | read (an flock question) | - | - | asks the cloud transfer's flock | - | - | - |
| es-app/src/guis/GuiMenu.cpp:5066 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | none (the journey record, written once per restore) | -1: 0644 when new | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-app/src/guis/GuiSaveState.cpp:33 | isFlockHeld | read (an flock question) | - | - | asks the cloud transfer's flock | - | - | - |
| es-core/src/Settings.cpp:524 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | none | -1: the live file's, 0644 when new | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/Settings.cpp:533 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | none | modeOf(path, 0644) | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/Settings.cpp:617 | copy | write | temp-and-rename, through writeText | file and directory | none | the source's mode | the read's ok and the write's result | as writeText |
| es-core/src/Settings.cpp:626 | readText | read | - | - | none | - | - | - |
| es-core/src/Settings.cpp:629 | modeOf | read (mode) | - | - | none | - | - | - |
| es-core/src/Settings.cpp:630 | readText | read | - | - | none | - | - | - |
| es-core/src/Settings.cpp:631 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | none | modeOf(path, 0644) | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/SystemConf.cpp:75 | parseKeyValues | read (the parse) | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.cpp:77 | parseKeyValues | read (the parse) | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.cpp:91 | PidLock | write | lock file linked into place holding the pid | - | is the lock | 0644 (the lock file) | link() result; a stale holder by kill(pid, 0) | a staging file `.new.<pid>.<n>` when killed between its create and the link |
| es-core/src/SystemConf.cpp:94 | chooseConfig | read (the ladder) | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.cpp:96 | LoadedConfig | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:108 | readText | read | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.cpp:110 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | PidLock /tmp/.system.cfg.lock (5 s) | -1: the live file's; recordLastGood: every copy's | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/SystemConf.cpp:120 | chooseConfig | read (the ladder) | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.cpp:128 | PendingChange | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:133 | PendingChange | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:173 | pendingAfterReload | read (pending changes) | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.cpp:217 | RecoveryWrite | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:218 | loadUnderLock | write | a recovery written back through writeText | file and directory | PidLock, re-chosen under it | every copy's shared bits | RecoveryWrite::Written | the chosen text read, the file as it was |
| es-core/src/SystemConf.cpp:223 | RecoveryWrite | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:225 | RecoveryWrite | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:232 | LoadedConfig | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:243 | LoadedConfig | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:248 | RecoveryWrite | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:253 | LoadedConfig | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:262 | RecoveryWrite | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:267 | LoadedConfig | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:277 | LoadedConfig | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:304 | saveUnderLock | write | temp-and-rename, through writeText, onto the text read under the lock | file and directory | PidLock /tmp/.system.cfg.lock, 5 s | the live file's, or every copy's on a recovery | LockedSave::Written only after the rename | the old file whole; the change kept in memory (LockBusy, Unreadable, WriteFailed) |
| es-core/src/SystemConf.cpp:309 | LockedSave | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:312 | LockedSave | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:315 | LockedSave | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:320 | LockedSave | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:328 | parseKeyValues | read (the parse) | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.h:21 | pendingAfterReload | read (pending changes) | - | - | - | - | - | - |

### 2. `writeAllText(` call sites at the pin

| Where | What | Temp-and-rename or in place | fsync | Lock | Mode | Positive check | A failure leaves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| es-app/src/ApiSystem.cpp:1017 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1020 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1718 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1796 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1936 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1948 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1955 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1970 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1971 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1972 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:2104 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:2107 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:2128 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:2130 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:2132 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:2141 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/CaptureRotation.cpp:175 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/FileData.cpp:2213 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/KeyboardMapping.cpp:426 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/KeyboardMapping.cpp:429 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/ThreadedCloudSync.cpp:944 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/Win32ApiSystem.cpp:979 | the Windows build only (not built on ROCKNIX) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
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
| | a duplicate | `:466` | the last *nonempty* value wins (Astra SO-22) | tree |
| | a comment | `:461` | `#` or `;` at column 0 only; ` #k=v` is a key with a space | tree |
| | a carriage return | none | kept in the value: `getBool(k, false)` reads `1\r` as false and `getBool(k, true)` reads `0\r` as true (Astra SO-22) | tree |
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

## The streams

One row per stream of `docs/reviews/briefs/t21-streams.md` (the coordinator's, at `e3c07a9c30`). The guest walks are `fix-walk-pending-image`, the coordinator's at the integration window.

| Stream | Items (bugs) | Positive before | ES commit | Positive after | `Already written:` | proved |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | PL-01 (#1185), PL-10 (#1198), PL-11 (#1199) | `stage-e/s1-before.txt`: eight SystemConfTests cases, TextRowEditTests and the parse case FAIL; `hostname-empty.py` loses every key; U1 `BATOCERA`, U2 a second key, U3 the default written | `ba0e82c1f` | `stage-e/s1-after.txt`: 230 cases pass; the chain keeps the line, `chksysconfig verify` reseeds nothing, the next start reads the player's keys; U1 empty and present, U2 refused, U3 removed | PL-01: a device that lost its settings to the reseed keeps the defaults it has, recoverable only from a settings backup; one that saved empty and has not rebooted keeps its keys, and the next save writes `system.hostname=`. PL-10: `system.hostname=` on D-NET-009's devices reads as the device's own name (`getHostsName`). PL-11: revived `k=` lines and literal `default`s already written are read as today and not written again | fix-unit-test |
| S2 | PL-09 (#1197), PL-03's recorder half (#1189) | `stage-e/s2-before.txt`: at S1's tree the newer cut file loses the record's tail and the seed is recorded over the player's record (two SystemConfTests cases FAIL); the reversed G-E1-04 file check FAILs against S1's `AtomicFileUtil.cpp` | `8cf52e263` | `stage-e/s2-after.txt`: 230 cases pass; the kill sweep keeps old or new whole at all 115 points; the shell's own S1 picture unchanged (live is the seed plus a key: #1208's half) | PL-09: a record already overwritten by a cut file's keys cannot be given back; a cut file still on a device is now recovered at the next start. PL-03: a device whose record already took the seed keeps the seed's keys, recoverable only from a settings backup; one whose record still differs is read from it at the next start | fix-unit-test |
| S3 | PL-02 (#1187), PL-17's hash halves (#1205) | -- | -- | -- | -- | stopped by an automated safety check at the read; the coordinator's (D-WORKFLOW-212, #668 00:4x UTC) |
| S4 | PL-04 (#1191) | `stage-e/s4-before.txt`: six of es-fs-tests' eight cases FAIL on the pin's file-mode lines (the target removed before a byte, an unclosed or vanished temporary put in place, one shared `.tmp`, an unchecked close, `renameFile` true for an absent source) | `f7c16144d` | `stage-e/s4-after.txt`: 238 cases pass in the five binaries | Art already removed by a failed download is gone and is fetched again at the next scrape; from now on a failure leaves the old file. Nothing to migrate. #585: `HttpReq`'s and `renameFile`'s lines are upstream's | fix-unit-test |
| S5 | PL-05 (#1193), PL-12's modes (#1200) | `stage-e/s5-before.txt`: at S4's tree two AtomicFileTests cases and one SystemConfTests case FAIL (no narrowing; a recovery copy takes its source's mode); `writeText` with a mode given already passes, kept as the guard | `94791c4ed` | `stage-e/s5-after.txt`: 242 cases pass; `tools/settings-modes-test` PASS for the shell side, unchanged | Every upgraded device: its 0645 and 0644 stores and records are narrowed to 0600 at the interface's first start (idempotent). Narrowing cannot undo a past read. The seed's own mode in the image is the coordinator's build step, named on #1184 | fix-unit-test |
