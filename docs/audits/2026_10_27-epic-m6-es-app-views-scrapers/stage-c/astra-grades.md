# The seat's grades (T32, #679)

Each of GPT-6 Astra's items, graded by the first reader against the code. "Re-read" means the first reader read the lines before grading. Counted below by `awk`.

| Item | Lead | Seat's verdict | Grade | What changed |
| --- | --- | --- | --- | --- |
| EP-1 | 3.13 | confirmed | accepted | a dependency's 404 also reaches `:372-375` and discards the primary results: added to PL-02 |
| EP-2 | 3.16 | narrowed | accepted | a trap only if the fix restores retry-on-false: PL-02's wording made conditional |
| EP-3 | L-05 | narrowed | accepted | line 4 shows the raw text only for a fatal error (`GuiScraperRun.cpp:225`); a nonfatal one has no why: PL-02 |
| EP-4 | L-07 | confirmed | accepted | G-05 does not prove the media path (no results, no resolve): 02's G-05 row corrected; a media-handle fixture owed |
| EP-5 | other success paths | confirmed | accepted | a failed rename and a failed resize read as DONE (`:669-688`): added to PL-02 |
| EP-6 | L-02 | confirmed | accepted | the UAF needs no hook (a natural interleaving); the lines are the write at `:335` and the self-delete at `:241`: PL-01 corrected |
| EP-7 | L-01 | narrowed | accepted | a lock on `stop()` is not sufficient: an owned, joined worker, atomics for `mExitCode`/`mPaused`, every publication under one rule: PL-01's fix shape replaced |
| EP-8 | L-23 | confirmed | accepted | two leaks; deleting a joinable `std::thread` is not a fix: PL-14 |
| EP-9 | 3.10 | confirmed | accepted | every containing level; not every violation is a SEGV: PL-03 worded so |
| EP-10 | L-22 | confirmed | accepted | IGDB `:157`, `:159`; HfsDB's key is `token`; IGDB needs both id and secret; HfsDB's numeric-token crash not separately measured (the run stopped at IGDB's): PL-03 corrected |
| EP-11 | floor 3.2 | narrowed | accepted | `ArcadeDBJSONScraper.cpp:78`, `:87` read members without `v.IsObject()`: PL-03 |
| EP-12 | floor 3.4 | narrowed | accepted | `:124` the same: PL-03 |
| EP-13 | floor 3.7 | narrowed | accepted | the throw-then-drop trace needs the omitted helper: PL-12 marks it the subagent's read |
| EP-14 | floor 3.8 | confirmed | accepted | the container-by-container inventory (`:467-494`, `:558`, `Resources.cpp:180-187`): PL-03's owner area |
| EP-15 | L-18 | confirmed | accepted | `:652` is not a live retry path; the 30-minute gap is between searches: 02 L-18 and PL-05 corrected |
| EP-16 | L-06 | narrowed | accepted | the media retry `:596` takes no options; a stall bound does not bound Retry-After or a slow transfer; a total deadline for tokens: PL-05's fix shape |
| EP-17 | L-14 | narrowed | accepted | the per-tile read is a lead, not a measured cost: 02 and 04 so worded |
| EP-18 | L-12 | narrowed | accepted | "every other route posts" is wrong (`:276-281`, `:440`, `:476`, `:738-770`): 02 L-12 corrected |
| EP-19 | L-13 | narrowed | accepted | the removal does not free the `FileData` (`:771` commented out): 02 L-13 corrected |
| EP-20 | L-19 | narrowed | accepted | "launch callbacks", not launches; resolve an id on the interface thread: PL-11 |
| EP-21 | L-20 | narrowed | accepted | define what `/isIdle` promises; a check at execution time: PL-11 |
| EP-22 | L-21 | narrowed | accepted | `quitES`'s and `openQuitMenu_static`'s threading are outside the packet: PL-11 records the call sites, not a race |
| EP-23 | L-24 | narrowed | accepted | the setter bounds only the Content-Length branch (`:2564-2567`); chunked and lengthless reads need their own: PL-06's fix shape; the other library claims marked unverified |
| EP-24 | 3.27 | narrowed | accepted | a delta, not a cursor: the harness's wording kept to the helper: PL-13 |
| EP-25 | 3.29 | confirmed | accepted | `unsigned char` fixes the ctype precondition, not UTF-8; G-03 still unexplained: PL-13 |
| EP-26 | 3.31 | narrowed | accepted | an empty path, not proved a blank tile; a player-installed theme can reach it: PL-09 |
| EP-27 | 3.32 | confirmed | accepted | as written: PL-08 |
| EP-28 | L-16 | narrowed | accepted | conditional; the quick search passes the root's name; Basic `:182` and Carousel `:171` do delete first (04's "recorded sound" withdrawn): 02 L-16, 04 Q1, PL-16 |
| EP-29 | L-08 | narrowed | accepted | G-09 is a picture, not a manual, and its cache owner is not identified (`:806`, `:845-850`; `:817-831` is the video-snapshot branch): 04 and PL-07 corrected |
| EP-30 | L-10 | narrowed | accepted | terminology, not a missing translation: PL-10 |
| EP-31 | L-11 | narrowed | accepted | `UIMode` may be saved by `:237-239`; no guaranteed save: PL-10 |
| EP-32 | new | new | accepted | HfsDB `:345`, `:410-415`, `:464-473`: in PL-03 |
| EP-33 | new | new | accepted (re-read) | `hasAnyMedia`'s logo test inverted (`Scraper.cpp:96` against `:145`): PL-18 |
| EP-34 | new | new | accepted (tree; unproved) | the worker can `delete this` before `mHandle` is published (`:53`): in PL-01's ownership fix |
| EP-35 | new | new | accepted (re-read) | `onFileChanged` keeps a placeholder the repopulate deletes, then `GridGameListView::setCursor` reads it (`:84`): PL-17 |
| EP-36 | new | new | accepted | a manual token failure is an empty DONE; a transport failure reads INVALID CREDENTIALS: in PL-02 |
| EP-37 | new | new | accepted | a startup throw leaves `running` and not `finished` (`:35-50`, `:308-316`): in PL-01 |
| EP-38 | new | new | accepted | the manual builder's plain flag, leaked thread and no join (`ScraperSearchComponent.cpp:206`, `:220-256`): in PL-05 |
| EP-39 | new | new | accepted (recorded) | media named by stem collide across folders (`Scraper.cpp:801-811`): PL-19 |
| EP-40 | new | new | accepted (tracked) | TLS peer verification off (`HttpReq.cpp:191-192`): #1154, already open; PL-20 |

`awk -F' \\| ' '/^\| EP-/{n++; if ($4 ~ /^accepted/) a++} END{print n, a}'`: 40 items, 40 accepted (two of them re-read: EP-33, EP-35; one unproved: EP-34; one already tracked: EP-40, #1154).
