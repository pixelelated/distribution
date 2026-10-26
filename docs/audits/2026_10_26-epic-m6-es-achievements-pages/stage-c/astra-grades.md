# The lane's grades of GPT-6 Astra's 55 items (T20, #667)

Each item re-read at its lines at the pin (`16dbac5211`) or the ctl (`8ebaf8daad`) before it was graded. *Accepted* means the claim holds at its lines; *in part* means a part holds; *plausible* means the shape holds and reachability rests on lines outside the packet; *rejected* means it does not hold. Where an item changes a lead, the new reading is named.

| Item | Grade | Re-read and consequence |
| --- | --- | --- |
| A-1 | accepted | The username's editable row (`:610`) and the ctl's Python argv (`raofflineproxy-ctl:616`, `:647`, `:788`: `"$(setting "${USER_KEY}")"` as an argument) are sinks the table lacked. They go into L-04. |
| A-2 | accepted | `VERIFYHOST 0` is set only inside the client-certificate branch (`HttpReq.cpp:194-201`); `02` § The credentials' paths said it as #1154 does. `VERIFYPEER 0` alone admits the self-signed listener, which is what the guest showed. L-01's text is corrected. |
| A-3 | accepted | L-02 is the `Now` branch only, as `02` says. |
| A-4 | accepted | **L-03 corrected.** `tokenOrError` reaches `:784` only when `refused` is true (`:782-786`): the server's JSON `Error`, or the empty-account sentence, which is translated. curl's message, `Unable to parse response` and `Unknown error` lead to the reconnect dialog, not to `:784`. The account page's `ra.error` (`GuiRetroAchievements.cpp:44`) and the hasher's `e.what()` remain. |
| A-5 | accepted | The callback receives the last accepted *fragment*. It becomes the modernize proposal's acceptance (Q1): an oversized record is rejected, not passed on cut. |
| A-6 | accepted | L-06 is Low on this image; the contract defect stands. |
| A-7 | in part | The rows hold. The parsers it calls outside the packet are in `OfflineAchievementsText.h` (`:130`, null counts read as unknown), read at stage B. |
| A-8 | accepted | **L-09 widened to a pin-era path.** `do_disable` writes the toggle off first (`:523-524`), then can `fail` at the hardcore restore, the record's clearing or the marker (`:538-544`), exiting 1 with the toggle off on disk while the page reverts its switch to on. |
| A-9 | accepted | TRY AGAIN restarts the ctl without the page's gates (`GuiOfflineScan.cpp:122-127`), so 77 and 78 can reach the scan page and read `COULDN'T FINISH` with the ctl's why. **`02` § The contract's "refused before the page" is corrected.** |
| A-10 | accepted | **L-07 narrowed.** With `added=unknown` the card says no count (`ProxyCards.cpp:368`). The defect is `ready=unknown` beside a numeric `added`, which T19's S8 makes possible. |
| A-11 | accepted | **L-10 raised to Medium.** At `8ebaf8daad` the `game` line carries the ROM's basename with `${name%.*}` and no replacement (`:1723`, `:1778`), and `OfflineScanJob::run` ends a line at `\r` (`:143`). A file named with a CR and then `>>> pid 1` gives the reader a second pid line, and a later CANCEL sends `kill(-1, SIGINT)` as root. ext4 `/storage/roms` admits such a name; T19's S9 replaces control characters, after integration. |
| A-12 | accepted | L-21 holds. The race needs at least one recognized hash (lookups alone with none start no thread), and the workers do write recovery metadata. "Daily" is not proved. |
| A-13 | accepted | **New, joins L-21.** The constructor pushes each `std::thread*` after creating it (`:138-139`), so the last worker can finish and `delete this` before the constructor's final `push_back`. `stop()` writes through an unretained pointer (`:403-411`). |
| A-14 | accepted | The scan job's ownership holds. |
| A-15 | accepted | — |
| A-16 | accepted | — |
| A-17 | in part | The wiring holds; the external consumers were read at stage B (`02` § The pages), outside this seat's packet. |
| A-18 | accepted | — |
| A-19 | accepted | **L-14 reframed:** the defect is the contradictory state and the restore of an obsolete preference at `disable` (`:529-540`), not the second writer as such. |
| A-20 | accepted | The caller's close is `hash_disc.c:546` (read at stage B). |
| A-21 | accepted | — |
| A-22 | accepted | — |
| A-23 | accepted | The argument is scoped to after seed expansion, as `02` states it for `advance()`. |
| A-24 | accepted | L-01 Medium; its fix and `Already written:` adopted. |
| A-25 | accepted | L-02 Medium; adopted. |
| A-26 | accepted | L-03 Low, narrowed by A-4. |
| A-27 | accepted | **L-04 corrected:** the `User-Agent` carries the URL-encoded `z=` user, only when an API login exists (`:178-185`), and rides the sign-in and the library requests too. |
| A-28 | accepted | — |
| A-29 | accepted | — |
| A-30 | accepted | L-07 Medium; its `Already written:` adopted. |
| A-31 | accepted | — |
| A-32 | accepted | L-09 Medium, widened (A-8). |
| A-33 | accepted | L-10 as A-11. |
| A-34 | accepted | — |
| A-35 | accepted | — |
| A-36 | accepted | L-13's fix belongs in `readAllText`, with 0- to 3-byte cases. |
| A-37 | accepted | As A-19. |
| A-38 | in part | The consumers are read at stage B, outside the packet. |
| A-39 | accepted | — |
| A-40 | in part | `tools/es-menu-map-check` and the map were run and read at stage A (R11). |
| A-41 | accepted | L-18 stays a note, not a translation fix. |
| A-42 | accepted | **L-19:** there is no total bound for a transfer that keeps moving; Medium, and #300's. |
| A-43 | in part | The HTTP cause is in the earlier `onError` lines (guest `g05`), so the log is not wholly lost. **L-20 lowered to Low.** The screen's `std::exception` remains. |
| A-44 | accepted | L-21 High; the fix shape and `Already written:` adopted. |
| A-45 | accepted | `mExit` is written by `stop()` and read by workers without synchronization: active, not dormant. |
| A-46 | accepted | **L-23's wording corrected:** `mCheevosIndexed` is "a library and a non-empty queue" (`:107`). |
| A-47 | accepted | — |
| A-48 | accepted | — |
| A-49 | in part | The ctl's argv (accepted into L-04). Error logs that might carry a credential: no producer shown. The `:792` log line carries `tokenOrError`, which on that branch is an error, never the token. Recorded as an inventory row, not a defect. |
| A-50 | accepted | **New, L-26.** The hasher's `std::thread*` are never joined, detached or deleted (`:138`, `:258-265`). The LED switch's callback captures its own `shared_ptr` (`:688`). The toggle's thread posts through a raw `Window*` (`:484`), where the scan job uses `AppWindow::post`. Each is Low. |
| A-51 | accepted | **New, L-27.** `storeSummary` returns `ok` after skipping every malformed line (`:252-263`). A missing or unreadable ready file reads as 0 (`:152-165`). `pendingAwardIds` returns "none" for an unreadable answer (`:271-279`). Low. |
| A-52 | accepted | **New, L-28.** `Success: true` with no `Token` returns true with an empty token, which the caller stores (`:1052-1056`, `GuiRetroAchievementsSettings.cpp:776-777`). `GetString()` on a non-string member is unchecked. Low; Medium beside #1154. |
| A-53 | accepted | **New, L-29.** A stopped hasher still toasts INDEXING COMPLETED (`:146`, only the top-up checks `mExit`). `cancel()` marks the job cancelled before the signal and ignores its failure (`OfflineScanJob.cpp:65-80`), and a second CANCEL is refused. Low. |
| A-54 | accepted | **Joins PL-13's page half:** `topUpRunning()` trusts the progress file, and a top-up reads another run's stamp by time alone. |
| A-55 | plausible | The every-frame read is bounded by the ready file's size (one id a line); a damaged large file is the case. Low, joins L-13's item. |

**Totals:** 55 items. 48 accepted, 6 in part (A-7, A-17, A-38, A-40, A-43, A-49 — most because the evidence lay outside this seat's packet), 1 plausible (A-55), 0 rejected. New leads: L-26 to L-29, and A-13 joins L-21.
