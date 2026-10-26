# Gemini 4 Argon's 45 items, graded by the first reader

Each item was re-read at its lines in the full tree at the pin (and `8ebaf8daad` for the scripts). Argon saw my grades of Astra; where it repeats an Astra item, the grade says so. **Grades:** *accepted*, *in part*, *plausible*, *rejected*. Its new leads are L-34 to L-36 in `02` § Corrections and new leads from the seats.

| Item | Argon | Grade | The first reader's reading |
| --- | --- | --- | --- |
| SO-1 | narrowed | accepted | Two quoted arguments in `unzipFile` and the PDF calls; and `getMD5` falls through to `unzipFile` (`ApiSystem.cpp:1538-1543`) when the first pipeline's answer is not one line of 32 or more characters, running `7zr` a second time over the same name. Folded into L-01. |
| SO-2 | narrowed | accepted | As Astra SO-2, plus: a `.m3u`'s first content file is what gets hashed (`ScreenScraper.cpp:295-303`), so a `.7z` named in a playlist reaches it too. `shouldExtractHashesFromArchives` is read (`SystemData.cpp:2315-2325`). Folded into L-01. |
| SO-3 | refuted | in part | As my grade of Astra SO-3: the storage line has no producer (`rocknix-config:271-273`). `getBiosInformations`' `--filter` joins a system's name from the system list, bare; the Bluetooth MAC and the bezel names are unvalidated. |
| SO-4 | new | accepted | A longer list of unbounded calls. One load or one save can take the settings lock twice, at up to 5 s each (`SystemConf.cpp:91-92`, `:218`, `:304`): up to 10 s on the interface thread. Recorded for Q1 and the retro's time-to-play line. |
| SO-5 | confirmed | accepted | The trailing bytes are kept in `mResponseHeaders`. |
| SO-6 | narrowed | accepted | As my grade of Astra SO-6, plus `ApiSystem::downloadFile` (`:2442-2460`), which takes the same path for any caller. |
| SO-7 | narrowed | accepted | As Astra SO-7; `02` corrected. |
| SO-8 | narrowed | accepted | As Astra SO-8; `Content-Type` parameters (`; charset=...`) are kept in the extension too. |
| SO-9 | new | accepted | As Astra SO-9 and SO-10. |
| SO-10 | refuted | accepted | As Astra SO-14; `02` corrected. |
| SO-11 | new | in part | Items 1, 3 and 4 hold: the `env` argv (L-25); `root.password` and the RetroAchievements password are in the same 0645 `system.cfg` (L-21 widened); the stale key in memory (L-26). Item 2 is not a sink: `get_setting wifi.key` fills a shell variable, and `nmcli -s` prints into a command substitution (`wifictl:60`, `:452`). Neither is argv or a file. |
| SO-12 | narrowed | accepted | Both readers AND the copies' modes, so a 0645 pair stays 0645 until both are narrowed. The fix's `Already written:` line must chmod the files on `/storage`. |
| SO-13 | confirmed | accepted | — |
| SO-14 | new | accepted | **The same chain as Astra SO-23, found independently;** proved by `stage-c/positives/hostname-empty.out`. L-23. |
| SO-15 | narrowed | accepted | Items 1 to 3 are Astra's SO-19, SO-18 and SO-52 (L-29, L-27). Item 4: `SystemConf`'s maps have no mutex (T2's PC-2, cited in the brief). |
| SO-16 | confirmed | accepted | As Astra SO-20, SO-21 and SO-53, plus `root = doc` when there is no `<config>` (`Settings.cpp:590-592`). L-30. |
| SO-17 | refuted | accepted | As Astra SO-22, plus three of `applyChanges`' rewrites. A `#k=` line is rewritten as a live `k=` line beside the real one (`SystemConf.cpp:384-398`, no `break`). A BOM hides the first key, which is then appended again. A key not yet in the file set to `default` is written as `key=default` (`:405`). L-34. |
| SO-18 | narrowed | accepted | As Astra SO-25 and SO-26, plus `disableWifi`, `forget_saved` and `connect_saved` exiting 0 with no device, and `setStorage`'s result ignored before the reboot flag. L-22, L-33. |
| SO-19 | narrowed | accepted | L-01. Its **`Already written:`** is the useful part: a failed extraction has already stored the empty input's digest as a game's MD5, and a fix treats that digest on a non-empty archive as unhashed. |
| SO-20 | confirmed | accepted | — |
| SO-21 | narrowed | accepted | L-03 stays Medium for `downloadFile`'s callers and the non-default filters. |
| SO-22 | confirmed | accepted | `mErrorMsg` too. |
| SO-23 | narrowed | accepted | — |
| SO-24 | confirmed | accepted | — |
| SO-25 | confirmed | accepted | — |
| SO-26 | narrowed | accepted | Adds the `env` sink (L-25). |
| SO-27 | narrowed | accepted | A leftover's own temporary starts 0600 and takes the live file's mode before the bytes (`AtomicFileUtil.cpp:115-147`). |
| SO-28 | confirmed | accepted | Its fix shape and `Already written:` line are the stream's. |
| SO-29 | confirmed | accepted | — |
| SO-30 | confirmed | accepted | — |
| SO-31 | confirmed | accepted | — |
| SO-32 | narrowed | in part | The other seven call sites are in the tree, each read (§ The writers' rows). |
| SO-33 | confirmed | accepted | — |
| SO-34 | confirmed | accepted | — |
| SO-35 | confirmed | accepted | — |
| SO-36 | narrowed | accepted | As Astra SO-27, and T20's G02. |
| SO-37 | confirmed | accepted | — |
| SO-38 | confirmed | accepted | — |
| SO-39 | narrowed | accepted | L-21's fix shape and its `Already written:` line (existing files are chmodded, not only the seed). |
| SO-40 | narrowed | accepted | L-22's fix shape: the device guard for every verb that reports a state. |
| SO-41 | new | accepted | As Astra SO-50 (L-24), found independently. |
| SO-42 | new | accepted | As Astra SO-51, plus: `renameFile`'s default `overWrite` removes the destination before `std::rename` (`FileSystemUtil.h:74`, `.cpp:1454-1455`), so the rename is not atomic. L-28. |
| SO-43 | new | accepted | As Astra SO-54, plus `getCRC32`'s empty `CRC = ` entry and its `size_t` subtraction (`ApiSystem.cpp:1582-1586`), and a `Retry-After` HTTP-date read as 0 ms (`Scraper.cpp:618-623`). L-31. |
| SO-44 | new | plausible | `GuiLoading` holds raw `this` (as Astra SO-56); BACK is refused while `mWaitingLoad`, and whether anything else deletes the page meanwhile is not settled here. The Bluetooth page's `mWaitingLoad` written from the worker is a data race by reading (`GuiBluetoothDevices.cpp:150`). L-35. |
| SO-45 | new | accepted | Item 1 is Astra SO-55 (L-32). Item 2: 501 to 503, 504 and redirect exhaustion read as `YOU'RE NOT ONLINE` to an online player (`HttpReq.cpp:462-469`, `ScreenScraper.cpp:989-990`). Item 3 is L-33. L-36. |

**Totals** (counted from the table): 45 items; 41 accepted, 3 in part, 1 plausible.
