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
