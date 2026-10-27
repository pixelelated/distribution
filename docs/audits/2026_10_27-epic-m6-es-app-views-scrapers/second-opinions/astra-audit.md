I distinguish a source-level defect from a reproduced failure and from a constructed control. Conclusions about upstream files below are limited to the supplied excerpts; omitted implementations are **outside the packet**, not presumed safe.

## 1. The scrape’s outcome

### EP-1 — 3.13 — **confirmed**

The three outcomes are incorrectly successful:

- Spent 429 retries set `ASYNC_DONE` at `Scraper.cpp:343–347`.
- A long Retry-After, when `retryOn249()` is false, does so at `Scraper.cpp:351–360`.
- `REQ_IO_ERROR` does so at `Scraper.cpp:372–375`.

None sets an error. The empty-result case becomes a successful worker completion at `ThreadedScraper.cpp:125–129`, and the page chooses COMPLETED when neither cancellation nor errors are recorded (`GuiScraperRun.cpp:138–144`).

**Making these `setError(status, ...)` would not stop the batch.** IO error is code 3 and rate limiting is 429 (`HttpReq.h:100–115`); neither belongs to the seven fatal statuses at `ThreadedScraper.cpp:157–159`. They reach the error-count branch at `ThreadedScraper.cpp:169–173`. A file-stream error, code 4, **does** stop it.

**Change:** retain the finding and the nonfatal fix. Narrow “404 DONE is right” to the intended primary-search no-match case: a dependency request also reaches `Scraper.cpp:372–375`, bypassing the final processing of the saved primary response at `Scraper.cpp:317–337`. Its missing images can therefore discard otherwise available metadata.

### EP-2 — 3.16 — **narrowed**

The Boolean-contract mismatch is real: IGDB returns false on a parse error and on an empty or non-array response (`IGDBScraper.cpp:313–331`), while `ScraperHttpRequest::update()` discards that return (`Scraper.cpp:336–337`).

But **it is not a trap for the minimal 3.13 fix**. Changing the IO/429 branches to `setError(status, ...)` does not start interpreting `process()`’s Boolean. The supplied `l313` control itself still prints DONE for a false-returning processor.

It becomes a trap **only if the fix also restores retry-on-false**. Such a change must distinguish:

- a legitimate empty array;
- a malformed response;
- an actual retry request.

A parse error already calls `setError()` inside `process()` (`IGDBScraper.cpp:319–324`), after the base’s initial DONE assignment. It is not presently converted back to success merely because the Boolean is ignored. Conversely, `{}` returns without setting an error (`IGDBScraper.cpp:327–331`), so it does remain successful.

**Change:** describe the dependency as conditional. The return-value control repairs the comment’s contract, not all response-outcome semantics. ScreenScraper’s claimed retry-on-false implementation is **outside the packet**.

### EP-3 — L-05 — **narrowed**

Raw transport/provider text can enter the common error path at `Scraper.cpp:381` and `Scraper.cpp:640`; removing HTML tags does not turn it into the project’s outcome vocabulary.

However, the first reader overstates what reaches line 4:

- Fatal errors populate `sProgress.failure` (`ThreadedScraper.cpp:157–167`).
- Nonfatal errors populate the count, not that sentence (`ThreadedScraper.cpp:169–173`).
- The page displays the sentence **only when `p.failed`** (`GuiScraperRun.cpp:225`).

Thus converting an IO error or exhausted 429 to a nonfatal error gives COULDN’T FINISH, but still no line-4 explanation.

**Change:** replace “every scraper error reaches line 4” with “fatal errors can expose raw error text; nonfatal failures have no why on line 4.” The claimed ScreenScraper exception cannot be checked from its omitted implementation.

### EP-4 — L-07 — **confirmed**

The media handle independently treats exhausted 429s, 404s and IO errors as DONE (`Scraper.cpp:607–614`, `Scraper.cpp:631–635`). Its completion callback clears the outstanding URL even when no nonempty file exists (`Scraper.cpp:454–462`), and resolution can finish normally (`Scraper.cpp:503–519`). The batch then accepts the result (`ThreadedScraper.cpp:135–149`).

Two qualifications matter:

1. **G-05 does not prove this media path.** With no search results, media resolution is never entered (`ThreadedScraper.cpp:118–129`). The supplied seven-harness record contains no separate `ImageDownloadHandle` result.
2. “No file” is not the only possible consequence. The callback accepts any positive file size (`Scraper.cpp:458–459`); whether a failed transfer leaves partial bytes requires the omitted `HttpReq` error/cleanup implementation.

**Change:** retain the code finding, remove the claimed media-path guest positive, and obtain a media-handle fixture. Before changing common failures to ERROR, inspect the resolve destructor: the error branch deletes the pairs without clearing `mFuncs` (`Scraper.cpp:495–501`), while that destructor is **outside the packet**.

### EP-5 — 3.17 / other success paths in `update()` — **confirmed**

There are further failure-to-success paths:

- A failed rename does not set an error (`Scraper.cpp:669–677`).
- `resizeImage()`’s false return is ignored, and its exceptions are swallowed (`Scraper.cpp:681–684`).
- The handle then unconditionally becomes DONE (`Scraper.cpp:688`).

The resize function has explicit failure returns for detection, unsupported formats, rescaling and saving (`Scraper.cpp:711–727`, `Scraper.cpp:753–776`). Consequently, successful HTTP delivery is being treated as successful asset preparation.

There are also response-schema failures that merely warn and return: missing GamesDB game/include data, for example (`GamesDBJSONScraper.cpp:590–602`), after the base has already assigned DONE.

**Change:** distinguish transport success, valid response, successful file creation and successful media preparation. Fixing only IO/429 classification does not establish that distinction.

## 2. The thread’s lifetime

### EP-6 — L-02 — **confirmed**

The use-after-free does **not** require the harness’s hook. A natural interleaving is:

1. `stop()` copies `mInstance` (`ThreadedScraper.cpp:325`).
2. The worker publishes `finished`, releases the mutex, and deletes itself (`ThreadedScraper.cpp:232–241`).
3. `stop()` obtains the progress mutex, marks cancellation, then writes through its saved pointer (`ThreadedScraper.cpp:329–335`).

The destructor’s clearing of the global pointer does not invalidate that local copy (`ThreadedScraper.cpp:76`). Nor does `catch (...)` protect an invalid memory write.

The confirmation dialog makes a late call possible: its YES callback invokes `stop()` without rechecking progress (`GuiScraperRun.cpp:110–116`), even though the earlier page input check examined `finished` (`GuiScraperRun.cpp:94–99`).

**Change:** keep both findings—UAF and cancellation overwriting completion—but cite the actual write at **335** and self-delete at **241**. The hook forces a feasible scheduling window; it does not create the underlying ownership defect.

### EP-7 — L-01, with L-03 — **narrowed**

The proposed mutex change addresses one window, but **is not a sufficient lifetime fix as stated**.

Required additional conditions are visible in the code:

- The pointer load **and its use** in `stop()` must remain protected; protecting only the null check is insufficient (`ThreadedScraper.cpp:325–335`).
- Every publication/clear must obey the same ownership rule—including the destructor, post-delete clear, start and exception path (`ThreadedScraper.cpp:76`, `:242`, `:292–316`).
- `isRunning()` is another unsynchronized reader (`ThreadedScraper.h:77`), including its API caller (`HttpServerThread.cpp:306`).
- Locking only `stop()` does not synchronize the worker’s plain `mExitCode` reads, or `mPaused` (`ThreadedScraper.cpp:179–192`; `ThreadedScraper.h:80–81`, `:111–114`). These require atomics or consistently locked access.
- `stop()` requests termination but does not wait for it (`ThreadedScraper.cpp:323–337`). The worker can still access `mWindow` and enqueue raw-game callbacks (`ThreadedScraper.cpp:275–285`).

For the stated exit caller, detaching is not a shutdown barrier. **`main.cpp`’s call and teardown order are outside the packet.** They must be checked before claiming safe exit.

**Change:** specify an owned worker with completion/join semantics, synchronized singleton access, and a serialized completion-versus-cancellation decision. Include the additional publication race in EP-34; the proposed control does not cover it.

### EP-8 — L-23 — **confirmed**

Finished logical workers are erased without deletion at `ThreadedScraper.cpp:220`. The destructor deletes only workers still present in the vector (`ThreadedScraper.cpp:69–74`).

Separately, the heap-allocated `std::thread` created at `ThreadedScraper.cpp:53` is neither joined, detached nor deleted anywhere in the supplied whole implementation.

**Change:** distinguish the two leaks:

- Drained `ScraperThread` objects leak; cancellation/fatal termination can still delete the remaining ones.
- Every successfully launched run leaks its thread handle and leaves it unreaped.

“Delete on erase” addresses the first. Simply deleting a still-joinable `std::thread` is not a fix; joining oneself is not an option either. An external owner should reap it.

## 3. The parses

The important distinction throughout is **member-value type versus containing-object type**. Checking `IsString()` after `HasMember()` does not make `HasMember()` safe on a non-object. Also, a violated rapidjson precondition under `NDEBUG` is not a promise that every input crashes: the supplied array cases demonstrate violations without a crash.

### EP-9 — 3.10 — **confirmed**

The unchecked object-member sites shown are:

- `GamesDBJSONScraper.cpp:590`: `doc.HasMember("data")`, then `doc["data"].HasMember("games")`, and the nested `operator[]` reads, without root/data object checks.
- `GamesDBJSONScraper.cpp:596`: the nested game-array reference depends on those preceding accesses.
- `GamesDBJSONScraper.cpp:598`: `doc["include"].HasMember("boxart")` without checking `include` is an object.
- `GamesDBJSONScraper.cpp:605`: nested `operator[]` access to boxart.
- `GamesDBJSONScraper.cpp:607`: two `boxart.HasMember()` calls **before** `boxart.IsObject()`.

The harness’s `"boxart":"x"` crash supports the release-build consequence. It does not establish that every malformed shape crashes.

**Change:** retain the finding, use shape-first guards at every containing level, and avoid describing all precondition violations as observed SEGVs. The GamesDB build gate remains `Scraper.cpp:29–31`.

### EP-10 — L-22 — **confirmed**

The precise sites are:

- IGDB: unchecked containing-object `HasMember()` at `IGDBScraper.cpp:157`; unchecked token `operator[]`/`GetString()` at **159**.
- HfsDB: unchecked containing-object `HasMember()` at `HfsDBScraper.cpp:202`; unchecked token `operator[]`/`GetString()` at **204**.

HfsDB’s field is `"token"`, not `"access_token"`.

IGDB’s request is reached only when **both** its client ID and secret are nonempty (`IGDBScraper.cpp:143–150`), not merely a client ID. Its registry entry is unconditional (`Scraper.cpp:37`).

**Change:** correct the locations and prerequisites. The supplied failing run crashes at the IGDB numeric-token case before showing a failing HfsDB numeric-token invocation. HfsDB has the same source defect, but do not describe its numeric-token crash as separately measured by that record.

### EP-11 — floor 3.2 — **narrowed**

The value-type checks hold, but the blanket safety verdict does not:

- `ArcadeDBJSONScraper.cpp:78` calls `v.HasMember()` and `v[...]` without first establishing `v.IsObject()`. The `GetString()` at **82** is value-type guarded.
- The same containing-object omission exists at **87**; the `GetInt()` at **91** is value-type guarded.
- The scalar overload at **94–100** correctly checks `IsInt()` before `GetInt()`.

The callers and response/game parser needed to prove that `v` is always an object are **outside the packet**.

**Change:** say “safe member-value reads for object inputs,” not an unrestricted “holds.” Read the callers or put the object check in the helpers, then test non-object game elements.

### EP-12 — floor 3.4 — **narrowed**

For an object input, the media-value check is sound: `IsString()` precedes the `GetString()` at `ArcadeDBJSONScraper.cpp:124–125`.

But the `HasMember()` and `operator[]` at **124** still require the containing `v` to be an object. This function does not check it.

**Change:** preserve the precedence/non-string-skipping conclusion, but condition its parse-safety verdict on a caller-proved object invariant. That caller proof is **outside the packet**.

### EP-13 — floor 3.7 — **narrowed**

The array indexing itself is guarded: `IsArray()` and nonzero size precede `v[i]` and `v[0]` (`GamesDBJSONScraper.cpp:295–309`). Each element’s fields are then delegated to `getStringOrThrow()` (`GamesDBJSONScraper.cpp:302–306`, `:309`).

The supplied excerpt does **not** contain that file’s helper implementation or the outer catch at the cited 624. Therefore I can verify the field-request/fallback sequence, but not independently complete the reported “throws, then drops the whole game” trace.

**Change:** distinguish malformed fields in an object from a non-object array element. The latter is not necessarily a catchable `runtime_error`; it depends on the omitted helper’s containing-object check. Test both under `NDEBUG`.

### EP-14 — floor 3.8 and parse coverage — **confirmed**

The additional visible unsafe sites are substantial:

| Location | Unchecked read |
|---|---|
| `GamesDBJSONScraper.cpp:558` | Root `HasMember`, `doc["data"].HasMember`, and nested `operator[]`, without object checks |
| `GamesDBJSONScraper.cpp:467` | `imageDoc.HasMember("data")`, after a parse with no error/object check |
| `GamesDBJSONScraper.cpp:469–470` | `data`/`base_url` member access and `medium.GetString()` without containing-object/string checks |
| `GamesDBJSONScraper.cpp:472–473` | Corresponding accesses and `large.GetString()` |
| `GamesDBJSONScraper.cpp:475–477` | `data`/`images` member access and ID indexing without object checks; only the final array is checked |
| `GamesDBJSONScraper.cpp:487–488` | Element `HasMember("type")` without `IsObject()`, then unchecked `GetString()` |
| `GamesDBJSONScraper.cpp:490–491` | The corresponding filename accesses |
| `GamesDBJSONScraper.cpp:493–494` | `side.GetString()` is value-type guarded, but its preceding element `HasMember()` still lacks an object check |
| `GamesDBJSONScraperResources.cpp:180–181`, `:187` | Root/data `HasMember` and nested indexing without root/data object checks; checking the final resource object is too late |

There are also the HfsDB containing-object omissions detailed in **EP-32**, which the first reader missed.

**Change:** replace “four sites” with a container-by-container inventory. A complete slice-wide inventory is **outside the packet**: notably the IGDB game parser, ArcadeDB response/game parser, HfsDB media guards preceding `:400`, GamesDB’s omitted helpers/resource iteration, and `HttpApi.cpp:179–201`. I cannot certify or invent their `Get*` sites. In particular, the shown `HttpApi.cpp:170–178` parse-error check alone does not establish safe subsequent member access.

## 4. The interface thread and bounds

### EP-15 — L-18 — **confirmed**, with a narrower manual-path claim

The initial batch chain is synchronous:

`start()` calls `Process()` (`ThreadedScraper.cpp:308–310`), which calls `ProcessNextGame()` for the initial workers (`:43–50`), which calls `ScraperThread::run()` (`:64`), which calls `search()` (`:100`). `search()` immediately calls `generateRequests()` (`Scraper.cpp:190–194`). **Only afterward** is the batch’s `std::thread` created (`ThreadedScraper.cpp:53`).

Thus the token waits at `IGDBScraper.cpp:150–151` and `HfsDBScraper.cpp:195–196` run on the calling interface thread at batch start.

The later uncaught throw is reachable with these conditions:

- another game remains to be handed out on the worker (`ThreadedScraper.cpp:214–217`);
- at least 1,800 seconds have elapsed since the last search, because each search refreshes the local timestamp (`IGDBScraper.cpp:138`, `:177`; `HfsDBScraper.cpp:172`, `:222`);
- token acquisition then fails for non-manual parameters (`IGDBScraper.cpp:169–172`; `HfsDBScraper.cpp:214–217`).

There is no catch around the worker loop (`ThreadedScraper.cpp:177–243`). The catch in `start()` cannot catch an exception escaping another thread.

The manual named-search and retry calls are indeed synchronous (`ScraperSearchComponent.cpp:303`, `:658`). But **652 is not an independently established live retry path**: the builder becomes DONE only with a nonnull handle, which extraction then returns (`ScraperSearchComponent.cpp:236–245`).

**Change:** retain the batch freeze and conditional termination finding. Do not replace the required inter-search gap with merely “a run lasting 30 minutes,” or count line 652 as demonstrated reachability.

### EP-16 — L-06 — **narrowed**

The default options provide a 10-second connect bound, but zero total and stall bounds (`HttpReq.h:48–65`). `wait()` adds no bound (`HttpReq.cpp:638–644`).

The easily missed construction is **the media retry**:

```text
Scraper.cpp:596 — new HttpReq(url, mSavePath)
```

It does not reuse the initial options from `Scraper.cpp:539–567`. Adding `stallTimeout` only to those options therefore does not carry it into that retry. The resource fetch also needs explicit treatment: `GamesDBJSONScraperResources.cpp:153` supplies no options.

Furthermore, a stall bound:

- does not bound the separate Retry-After wait (`Scraper.cpp:291–305`, `:351–366`, `:585–625`);
- does not bound a transfer that continues above the low-speed threshold (`HttpReq.cpp:207–213`);
- does not make `stop()` a wait-for-completion operation (`ThreadedScraper.cpp:323–337`).

**Change:** require bounds on every construction and retry, cap retry scheduling separately, and use a total deadline for small token exchanges. “Add a stall timeout” is not a complete end-to-end bound.

### EP-17 — L-14 — **narrowed**

The SCREENSHOTS tile decorator really calls `DisplayAspect::forScreenshot(file)` (`GridGameListView.cpp:40–47`).

But **“one capture-record read per item at populate, before the first frame” is not proved by these excerpts**. The decorator’s invocation policy and `DisplayAspect`’s implementation are **outside the packet**. Registration of a callback is not proof of when or how often it runs. The visible populate loop calls `mGrid.add()` and later `mGrid.update(0)` (`GridGameListView.cpp:205–219`).

The guest timing record contains only near-identical settle times (`guest-cycle/g02-l14-timings.txt:1–3`), and the supplied guest account says the actual grid was not reached.

**Change:** retain a performance lead, not a measured populate-cost finding. Instrument callback count/thread and actual file reads under a theme that renders the grid.

## 5. The services

### EP-18 — L-12 — **narrowed**

The handler is configured under the server’s pool (`HttpServerThread.cpp:143–147`) and directly calls `displayNotificationMessage()` rather than posting it (`HttpServerThread.cpp:562–575`).

That establishes **call-site thread placement**, not an internal Window race. Whether that method itself queues or locks is **outside the packet**.

The statement “every other route posts” is wrong: numerous routes read application objects directly, and the mutation handlers below do too (`HttpServerThread.cpp:276–281`, `:440`, `:476`, `:738–770`).

**Change:** retain the off-interface call as a lead, inspect the callee before asserting a toast-queue race, and separate request-size limits from the guest’s demonstrated one-line visual clipping.

### EP-19 — L-13 — **narrowed**

The off-interface operations are real:

- Media import writes the file and mutates metadata before the posted notification (`HttpApi.cpp:258–260`; `HttpServerThread.cpp:440–443`).
- JSON import runs before its posted notification (`HttpServerThread.cpp:476–479`).
- Removal loads data, removes recovery entries/files, and modifies virtual-folder membership on the handler thread (`HttpServerThread.cpp:738–770`).

However, **the removal handler does not delete the `FileData` object**: that deletion is commented out (`HttpServerThread.cpp:771`). Do not conflate filesystem deletion with freeing that object.

Nor does the out-of-system guest response establish general path containment. `loadGamelistFile()`’s rules are **outside the packet**.

**Change:** keep the threading/lifetime finding, include the raw pointers captured for later notifications, and prove containment and synchronization separately. The floor’s unchecked write result at `HttpApi.cpp:258–261` also deserves an explicit disposition; it is already noticed, not a new finding.

### EP-20 — L-19 — **narrowed**

The handler traverses live system/game structures and posts a raw `FileData*` for every matching entry, without a break (`HttpServerThread.cpp:613–629`). A queued pointer is not made safe merely by executing its eventual use on the interface thread.

But “two launches” should read **“two launch callbacks”**: the omitted `ViewController::launch()` implementation may reject or serialize them. Likewise, actual pointer invalidation requires the competing reload trace.

**Change:** retain the lifetime hazard. Resolve a stable identifier on the interface thread rather than carrying an unowned pointer across the queue, and test a reload between lookup and callback execution.

### EP-21 — L-20 — **narrowed**

The route’s idle predicate checks only the listed game/scraper/installer/hasher/updater states (`HttpServerThread.cpp:304–309`). It is not a general “all work finished” predicate.

The `/reloadgames` handler also contains no idle check before posting `GuiMenu::updateGameLists()` (`HttpServerThread.cpp:533–542`). However, the downstream implementation and its gates are **outside the packet**. “No check in this route” is proved; “no downstream exclusion” is not.

**Change:** define what `/isIdle` promises to the QA walks, then include every relevant activity. Any reload admission check must occur at execution time too; checking before enqueueing alone would leave a race.

### EP-22 — L-21 — **narrowed**

The direct calls to `quitES()` are on the handler path (`HttpServerThread.cpp:241`, `:249`, `:257`). Whether those calls are unsafe depends on the omitted implementation—an event-posting quit function could legitimately be callable there.

The confirmation paths also differ:

- `confirm=switchscreen` explicitly posts a dialog, under `#if BATOCERA` (`HttpServerThread.cpp:224–230`).
- `confirm=menu` directly calls `GuiMenu::openQuitMenu_static()` (`HttpServerThread.cpp:234–238`); any internal posting is **outside the packet**.

**Change:** correct the blanket confirmation-path description, and establish the quit/menu callees’ threading contracts before calling these proven races.

### EP-23 — L-24 and the remaining httplib request path — **narrowed**

The payload-limit concern is justified. The default is effectively unlimited (`httplib.h:71–72`). More importantly, the shown dispatch applies `payload_max_length` only to the Content-Length branch:

- chunked input calls `read_content_chunked(strm, out)` (`httplib.h:2559–2560`);
- input without Content-Length calls `read_content_without_length(strm, out)` (`httplib.h:2561–2562`);
- the explicit size comparison follows only in the length-bearing branch (`httplib.h:2564–2567`).

**The proposed one-line setter is not an established fix for the reported chunked defect.** A cumulative bound must also cover those other paths. The complete chunk loop and receiving/accumulation callback are **outside the packet**, so this excerpt alone cannot certify all enforcement points.

For the other requested mechanisms:

- **Parse/exception failures:** the excerpt stops at the declaration of `chunk_len` (`httplib.h:2483`). Its conversion and worker exception containment are outside the packet.
- **Mount traversal:** no mount-point setup is shown in the supplied server setup/routes. The application instead passes constructed resource paths to `ResourceManager` (`HttpServerThread.cpp:791–792`, `:808–810`). Its normalization and filesystem fallback are outside the packet.
- **Header injection:** the header parser, decoder and response-header serializer are outside the packet. The first reader’s specific “mechanism absent” conclusion cannot be independently verified here.

The exposure distinction is correctly stated: default loopback versus public bind is explicit (`Settings.cpp:190`; `HttpServerThread.cpp:823–828`).

**Change:** keep the limit finding, withdraw “one-line contained fix” as closure, and mark the other library-security conclusions as unverified from this packet. An old-library fingerprint is not proof either of another vulnerability or of its absence.

## 6. The views

### EP-24 — 3.27 — **narrowed**

The helper is wrong for arbitrary jumps: it repairs a negative value only once and rejects all positive counts at least the size (`SystemView.cpp:272–280`). The fast path passes ±10 (`SystemView.cpp:331`).

But the negative helper result is passed as a **movement delta**, not used here to index the entries (`SystemView.cpp:406–413`). The first reader’s later distinction is right: helper out-of-range results do not establish an out-of-range carousel cursor or crash.

The positive early return is a separate behavioral asymmetry: forward movement can be a no-op where −10 modulo the size is not (`SystemView.cpp:274–275`, `:331`).

**Change:** keep the arithmetic defect and forward-no-op case. Avoid the harness wording that says it directly leaves “the carousel cursor” outside the range. The actual wrapping implementation is outside the packet.

### EP-25 — 3.29 — **confirmed**

The non-Korean branches take a single byte and pass plain `char` to `toupper()` (`ISimpleGameListView.cpp:511`, `:554`, `:603`). That both mishandles UTF-8 initials and violates the ctype input requirement where that byte is negative.

The reverse scan’s break assumes a contiguous run of matching initials (`ISimpleGameListView.cpp:491–518`); under a non-name sort it can select the last run rather than the first matching game.

**Change:** retain both findings. Casting to unsigned char fixes only the ctype precondition, not UTF-8 handling. Neither finding explains Alpha remaining selected after an ASCII D jump in a name-sorted list; the caller/application trace remains outside the supplied code.

### EP-26 — 3.31 — **narrowed**

The return-path finding is certain: IMAGE exits at `GridGameListView.cpp:135–136`, preventing its later fallback and the thumbnail return (`:144–153`).

The stronger visual claim is not certain from this packet. An empty path is passed to the grid (`GridGameListView.cpp:208`), but the real `FileData::getImagePath()` and tile fallback rendering are outside the packet. An empty path need not mean an entirely blank tile.

**Change:** describe the proven missing fallback, retain the intent question, and validate it with the real grid. The guest’s one theme is not evidence that no supported or player-installed theme can expose it.

### EP-27 — 3.32 — **confirmed**

Both remaining defects are direct:

- `RELEASEDATE_ASCENDING` is tested twice, omitting the distinct descending value (`GameNameFormatter.cpp:83–89`; `FileSorts.h:22–23`).
- Displayed game-time hours wrap modulo 24 (`GameNameFormatter.cpp:171–185`).

The correction concerning the detailed row is right. It calls `secondsToString()` (`DetailedContainer.cpp:1049`), whose non-clock path restores the day into hours for this case (`TimeUtil.cpp:564–569`).

**Change:** fix the formatter only for these defects; do not reintroduce a second play-time-wrap finding against the detailed row.

### EP-28 — L-16 — **narrowed**

The packet establishes a **conditional free-before-read sequence**, not the complete UAF:

- Only the filtered-custom-collection branch clears this root (`CollectionSystemManager.cpp:1112–1117`, `:1573–1576`).
- Clearing deletes children only when `mOwnsChildrens` is true (`FileData.cpp:2321–2328`).
- Reloading a view can read its old cursor and path (`ViewController.cpp:1140–1143`).

What is missing is the ownership construction, the relevant bundle/cursor identity, and the `SystemData*` reload overload linking the call at `CollectionSystemManager.cpp:1589` to the supplied view-replacement implementation. Those are **outside the packet**.

The proposed guest path also needs checking: quick search passes **the view root’s system name**, not the selected child collection’s name (`ISimpleGameListView.cpp:453–464`).

Two corrections:

- The old view is retained through a local smart pointer at `CollectionSystemManager.cpp:1586–1593`; its mere use after reload is not itself proof that the view was freed.
- “Nothing freed first” is false for `BasicGameListView.cpp:182` and `CarouselGameListView.cpp:171`: their preceding removal paths delete the game (`BasicGameListView.cpp:174–177`; `CarouselGameListView.cpp:164–166`). The potentially protective ordering is **remove from the list before deleting**, not “no deletion.”

**Change:** keep L-16 carried and conditional. Do not promote it to a demonstrated UAF without closing those identity/ownership links.

### EP-29 — L-08 — **narrowed**

The relevant existence gates are present for alternative images, marquee/metadata images, manual/magazine and map (`DetailedContainer.cpp:817–831`, `:863–873`, `:899–916`). The manual/map existence checks are specifically the **PreloadMedias-off** branches.

The guest account proves a **picture** remained absent until restart, not a manual. The retrospective and analysis incorrectly retell G-09 as a manual positive. Also, the picture’s exact cache owner cannot be assigned from that observation alone: the ordinary image path is set at `DetailedContainer.cpp:806`, `:845–850`, while `:817–831` is inside the video-snapshot branch.

**Change:** correct the guest description, retain the external-writer/cache lead, and do not claim a particular gate or “until launch” invalidation without its implementation. The filesystem-cache implementation is outside the packet.

### EP-30 — L-10 — **narrowed**

The two English prompts are distinct and both go through gettext (`ISimpleGameListView.cpp:714`, `:732–734`). The supplied generated catalog table reports the inconsistent French terminology at `po:218–219` versus `po:233–234`.

That supports the terminology correction, not a missing-translation finding. The actual catalog file/path is outside the packet.

**Change:** retain the one-catalog-line correction on the supplied catalog evidence; do not change the action logic or describe the held prompt as untranslated.

### EP-31 — L-11 — **narrowed**

The literal English dialog and bare OK are confirmed at `SystemView.cpp:233–234`.

But “the UIMode write is not saved” is too absolute. If clearing HiddenSystems changes that setting, the subsequent `saveFile()` can persist UIMode too (`SystemView.cpp:237–239`). What is missing is an **independent, guaranteed save** when only UIMode changes.

**Change:** translate the literal and make persistence explicit. Keep the withdrawal of the alleged empty French translation for the separate all-hidden dialog (`SystemView.cpp:243`).

## New items

### EP-32 — new: HfsDB nested values lack object checks — **new**

**Family:** a check whose failure reads as success.

Additional unsafe member operations are visible:

- `HfsDBScraper.cpp:345`: `v.HasMember("medias")` and `v["medias"]` without a local object check.
- `HfsDBScraper.cpp:410–415`: `game.HasMember("system")`, `game["system"]`, then `system.HasMember("id")` without checking the system value is an object. `GetInt()` itself is value-type guarded.
- `HfsDBScraper.cpp:464–473`: each metadata array element reaches `HasMember("name")` and `HasMember("value")` without `metadata.IsObject()`. The subsequent `GetString()` calls are value-type guarded, but the containing-object reads are not.

The media `GetString()` at `HfsDBScraper.cpp:400` cannot separately be condemned: its preceding guards are outside the packet.

**Proof:** use a valid response fixture with a string/scalar metadata element, and an arcade result whose `system` is non-object, under the recipe’s `NDEBUG` build. Require rejection without precondition violations.

**Change:** extend the shape-first work beyond the token parsers and GamesDB.

### EP-33 — new: inverted logo-presence predicate — **new**

**Family:** a check whose failure reads as success.

`hasAnyMedia()` counts a marquee only when `ScrapperLogoSrc` is **empty** (`Scraper.cpp:95–97`). The corresponding missing-media test correctly uses **nonempty** (`Scraper.cpp:144–146`).

For a game whose sole enabled media is an existing logo, the “has any” predicate can therefore report false. Conversely, a disabled logo source can make it report true.

**Proof:** an existing marquee, no other media, and a provider supporting Wheel/Marquee; toggle the logo-source setting between empty and nonempty.

**Change:** correct the predicate and test it separately from L-09’s cache behavior.

### EP-34 — new: the worker can delete its owner before thread-handle publication — **new**

**Family:** a lifetime or a thread.

At `ThreadedScraper.cpp:53`, the new thread can begin executing before the assignment to the owner’s `mHandle` has completed. A sufficiently fast worker can finish and execute `delete this` (`ThreadedScraper.cpp:220–241`) before the creating thread stores the returned pointer into that member.

This is another possible write into the freed owner, independent of CANCEL.

**Proof:** schedule a completed one-game worker through termination before allowing the creator’s handle assignment; check the pin under ASan. The control must keep the owner alive through publication and completion.

**Change:** include this in the ownership fix. A mutex around `stop()` does not address it.

### EP-35 — new: rebuilding an empty list retains a freed synthetic cursor — **new**

**Family:** a lifetime or a thread.

`ISimpleGameListView::onFileChanged()` saves the placeholder cursor, repopulates, then passes the saved pointer to `setCursor()` (`ISimpleGameListView.cpp:112–125`).

For an empty grid, repopulation creates another placeholder (`GridGameListView.cpp:214–215`, `:249–253`). `createNoEntriesPlaceholder()` deletes the previous owned placeholder (`ISimpleGameListView.cpp:929–934`). The saved pointer is now dangling. Grid’s failed-lookup path then dereferences its cursor argument (`GridGameListView.cpp:84–87`).

**Proof:** start with an empty grid, deliver a non-metadata file-change notification that leaves it empty, and run through the real failed-cursor-lookup path under ASan.

**Change:** do not restore a synthetic cursor that population replaces. This is a more local lifetime trace than L-16 and deserves its own fixture.

### EP-36 — new: manual token failures become successful empty searches — **new**

**Family:** a check whose failure reads as success.

When token acquisition fails, both scrapers simply return without requests for manual parameters (`IGDBScraper.cpp:169–175`; `HfsDBScraper.cpp:214–220`). Normal manual searches explicitly set that flag (`ScraperSearchComponent.cpp:296–303`).

`Scraper::search()` returns the handle anyway (`Scraper.cpp:190–194`), and an empty request queue becomes DONE (`Scraper.cpp:250–254`). Missing credentials or a failed token request can therefore become “no results.”

The same Boolean also collapses non-manual token-network failures into INVALID CREDENTIALS, regardless of why acquisition failed (`IGDBScraper.cpp:150–172`; `HfsDBScraper.cpp:195–217`).

**Proof:** force token acquisition failure with manual parameters and assert ERROR rather than empty DONE; separately distinguish credentials rejection from transport failure.

**Change:** propagate a typed token-acquisition outcome in both modes, rather than using throw-versus-empty-queue as the distinction.

### EP-37 — new: failed startup leaves a running progress snapshot — **new**

**Family:** a lifetime or a thread.

`Process()` publishes `running=true`, `finished=false` before generating initial requests (`ThreadedScraper.cpp:35–50`). If generation throws, `start()` deletes the instance and shows a dialog but does not finalize that snapshot (`ThreadedScraper.cpp:308–316`).

Thus `isRunning()` can be false while `progress()` still describes an unfinished run. A page displaying that snapshot only offers cancellation, whose `stop()` immediately returns for a null instance (`GuiScraperRun.cpp:94–99`, `:122–126`; `ThreadedScraper.cpp:325–327`).

**Proof:** inject a startup search exception and assert a terminal failed snapshot. Whether the actual caller leaves `GuiScraperRun` displayed requires the start-page implementation, **outside the packet**.

**Change:** finalize progress on startup failure, or make startup failure explicit to the page owner.

### EP-38 — new: the manual request builder has its own thread-ownership defects — **new**

**Family:** a lifetime or a thread.

The supplied complete builder class has:

- an unsynchronized plain completion flag written by its worker and read by the interface (`ScraperSearchComponent.cpp:220`, `:225`, `:256`);
- a heap thread allocation that is joined but then overwritten with null without deletion (`ScraperSearchComponent.cpp:206`, `:230–234`);
- no destructor that cancels or joins an outstanding worker (`ScraperSearchComponent.cpp:197–259`).

Its worker also uses raw `this` and `mSearch` state (`ScraperSearchComponent.cpp:203–213`). Destruction-while-running reachability needs the omitted search-owner destructor; the flag race and completed-thread allocation leak do not.

**Proof:** TSan a completion/update overlap, leak-check repeated completed searches, and inspect/test cancellation while token acquisition is blocked.

**Change:** do not treat “it runs off the interface thread and catches exceptions” as a complete lifetime solution. Give the builder owned, joined worker state.

### EP-39 — new: different ROM paths collide in media filenames — **new**

**Family:** a check whose failure reads as success.

`getSaveAsPath()` identifies a game only by its stem beneath a system-wide media directory (`Scraper.cpp:801–811`). Two games in the same system such as `a/game.zip` and `b/game.zip` therefore receive the same image path.

With overwrite disabled, the second can silently adopt the first game’s existing media (`Scraper.cpp:438–446`). With overwrite enabled, they target the same file.

**Proof:** two distinct paths with the same stem and source system; assert the current save paths collide, then resolve different fixture images for both.

**Change:** use a stable collision-resistant game identity or relative-path scheme, while preserving/migrating already recorded media paths.

### EP-40 — new: HTTPS peer verification is disabled in the shared request layer — **new**

**Family:** a check whose failure reads as success. **Neighbour finding; owner outside these 42 files.**

The shared request setup unconditionally disables certificate-chain verification (`HttpReq.cpp:191–192`). This is broader than the comment’s “expired certificates”: an untrusted certificate chain is not rejected. The shown separate hostname-verification disable is conditional on client certificates (`HttpReq.cpp:195–200`), so I am **not** claiming hostname checks are universally disabled.

This changes the threat model for the network-controlled JSON findings: a response need not necessarily originate from the genuine provider.

**Proof:** against a controlled TLS endpoint with a matching hostname but untrusted chain, show the pin accepts the response and a verification-enabled control rejects it. The image’s CA provisioning is outside the packet.

**Change:** record the dependency with the shared HTTP owner and coordinate certificate verification with truthful transport-error reporting; do not quietly broaden the T32 patch.

## Highest priorities

1. **Thread ownership and local dangling pointers — EP-6, EP-7, EP-34, EP-35.** These threaten the interface process through normal scrape completion/cancellation or list refresh. The proposed lock-only fix leaves important lifetime paths open.
2. **Release-build parse safety — EP-9, EP-10, EP-14, EP-32**, with **EP-40** coordinated separately. IGDB’s token defect is in an always-registered scraper; malformed-input rejection must not depend on assertions.
3. **Bounded token acquisition and later-thread exception handling — EP-15–16.** The initial wait blocks the interface before CANCEL can help; later acquisition can escape the worker entirely.
4. **Truthful outcomes — EP-1–5 and EP-36–37.** Preserve batch continuation while reporting errors; do not trade false COMPLETED for a permanently unfinished page.
5. **Media identity and enabled API safety — EP-39 and EP-19–23.** Persistent wrong-media overwrites deserve more weight than display cosmetics. WEB ACCESS’s default-off state limits exposure, but does not make an ineffective chunked-body fix acceptable.