## 1. Credentials

**A-1 — narrowed — the sink inventory is not complete.**  
Evidence: `GuiRetroAchievementsSettings.cpp:610-616,767-796` (excerpt); `RetroAchievements.cpp:149,181-195,301,315,338,521,757,1037` (excerpt); `GuiRetroAchievements.cpp:334` (excerpt); `raofflineproxy-ctl:616,647,788` (excerpt).

The shown credential-bearing requests and settings bindings substantially match the inventory: password in the login URL, API key in `y=`, usernames in queries and the account title, and the returned token assigned to configuration. Missing sinks include the username’s editable settings row and, across the ctl boundary, username arguments to Python processes. Actual configuration serialization, backup filtering, and the cited summary request at `RetroAchievements.cpp:634` are **outside the packet**, so the table’s exhaustive at-rest and backup assurances cannot be independently certified here. Error-bearing log sinks also need separate treatment; “no expression explicitly logs a credential variable” is not proof that credentials cannot reach logs.

**A-2 — confirmed — L-01 is an integration defect, not merely somebody else’s `HttpReq` issue.**  
Evidence: `RetroAchievements.cpp:1035-1038`; `HttpReq.cpp:182-200,221-242` (excerpts).

This slice chooses to put the password in a URL and invokes a transport that disables certificate-chain verification and permits HTTP redirects. #1154 owns the shared transport settings, but that ownership does not remove this caller’s exposure or its credential-bearing-URL design. One correction: `VERIFYHOST=0` is conditional on client-certificate configuration, not unconditional for this sign-in; `VERIFYPEER=0` nevertheless permits an attacker’s self-signed certificate bearing the right hostname. Allowing HTTP redirects is a downgrade vulnerability, but it does **not** establish that every redirect automatically carries the original query—the redirect target must retain or reproduce it.

**A-3 — narrowed — L-02’s synchronous path exists, but it is not every page close.**  
Evidence: `GuiRetroAchievementsSettings.cpp:743-776,805-806`; `RetroAchievements.cpp:174-186,1035-1040`; `HttpReq.h:48-54`; `HttpReq.cpp:203-213` (excerpts).

The `Now` branch calls `testAccount()` synchronously inside the save callback, and that request supplies neither a total timeout nor a stall timeout. The page explicitly delegates other cases to the network watcher, so the first reader correctly limits the problem to the immediate-sign-in branch rather than all closes. The implementation of `CheevosRetry::saveSignIn` is **outside the packet**: its complete decision table is not independently proved by the comment describing changed accounts and an available address. The guest’s boot sign-in exercises transport behavior, not this page-close reachability.

**A-4 — refuted — the claimed normal path from curl/parse errors to the sign-in dialog at `:784` is wrong.**  
Evidence: `RetroAchievements.cpp:1019-1068,737,780-782`; `GuiRetroAchievementsSettings.cpp:782-792`; `GuiRetroAchievements.cpp:43-44,339-341`; `GuiGameAchievements.cpp:41-42` (excerpts); `ThreadedHasher.cpp:394-399`.

Transport failure and the ordinary parse-failure branch leave `refused` false, so this save path presents the generic reconnect message, not `tokenOrError` at `:784`. The server’s JSON `Error` really does reach that dialog after `refused` becomes true; account-summary errors also reach the account error box or subtitle, and the hasher displays `e.what()`. The game page has another verbatim sink, `ra.Title`, although its complete web-error producer is **outside the packet**. Thus L-03 survives in narrower form, but the first reader’s listed sign-in paths are not interchangeable.

## 2. The contract with the control script

**A-5 — confirmed — the two readers have materially different contracts.**  
Evidence: `ApiSystem.cpp:2277-2292` (excerpt); `OfflineScanJob.cpp:134-157`; `OfflineAchievements.cpp:51-57`.

The legacy reader processes each `fgets` fragment independently and discards a fragment whose `getline` reaches EOF without finding a newline; that explains both lost long-line heads and the dropped final unterminated line. Its callback receives the last **nonempty accepted fragment**, not necessarily the last logical stdout line. The scan reader instead retains the first 1,024 bytes, discards the remainder until a delimiter, preserves a final unterminated line, and checks `WIFEXITED`. The supplied fixture corroborates the legacy behavior; a replacement should reject oversized structured records rather than quietly treating truncated records as complete.

**A-6 — narrowed — the guest finding lowers L-06’s likelihood, not its correctness.**  
Evidence: `ApiSystem.cpp:2269,2291` (excerpt); `OfflineAchievements.cpp:54`; `GuiRetroAchievementsSettings.cpp:479-482` (excerpt); `ProxyCards.cpp:271-288,338-368` (excerpt).

`WEXITSTATUS` is used without establishing normal termination, and the supplied host fixture demonstrates a false zero for a signalled waited-on process. The observed bash wrapper means that killing the ctl normally produces a shell exit such as 137 instead; the false-zero case requires the process actually waited on by `pclose` to be signalled. That supports Low likelihood on the observed image, not a portable guarantee about every shell or image, and the guest record’s disowned final probe must not be used as evidence. A false zero produces a top-up success card only if the card’s work-detection conditions also permit an outcome to be shown.

**A-7 — confirmed — most read-only verb rows match their producers, with limited verification of the parsers.**  
Evidence: `raofflineproxy-ctl:568-619,638-647,744-800,803-819,2184-2188` (excerpts); `OfflineAchievements.cpp:108-122,239-289,323-327`.

`pending` prints a count with exits 0/1, while `pending-ids` prints all rows; the corresponding readers accept those exits and reject other statuses. `account` is accepted only on exit 0, `summary` only on exit 0, and `index-offline`’s status is merely logged, as reported. The pin’s account conversion accepts values such as booleans through Python’s `int`, so the stronger numeric contract belongs to T19’s later change, not this ctl. The definitions of the pending/account/store parsers—including the claimed handling of JSON `null` counts—are **outside the packet**.

**A-8 — narrowed — successful toggle rows are right; failure is not equivalent to unchanged state.**  
Evidence: `raofflineproxy-ctl:473-482,517-546`; `GuiRetroAchievementsSettings.cpp:479-501` (excerpts); `OfflineAchievements.cpp:168-170`.

Successful enable and disable end with the expected newline-terminated `hardcore=` line. The GUI checks only its prefix, not an exact `hardcore=0` or `hardcore=1`, and assumes every unsuccessful operation left the opposite toggle state intact. L-09 is therefore real with T19 S5, but it also has a pin-era path: disable writes the toggle off at `:523`, then can fail during hardcore restoration, record cleanup, or marker removal. “Off” here means configuration/routing state; a failed service stop does not establish that the proxy process stopped.

**A-9 — narrowed — scan gates are advisory, and top-up outcomes are conditional.**  
Evidence: `GuiRetroAchievementsSettings.cpp:328-361` (excerpt); `GuiOfflineScan.cpp:122-127,185-200,310-346`; `raofflineproxy-ctl:1163-1194,1965-1975,2196-2227,2395-2430`; `ProxyCards.cpp:274-320,370-379` (excerpts).

The claim that exits 77/78 are necessarily refused before the scan page is wrong: configuration can change after the gate, and TRY AGAIN starts the ctl directly without repeating those gates. Exit 75 is mapped to SKIPPED; cancellation initiated through this page is SKIPPED because of its local `cancelled` flag, not because exit 130 alone has that meaning. Exit 143 without a prior why becomes the reported generic failure, although previously received why/note fields can alter the displayed details. Top-up refusals generally leave no stamp or card, but polling another run’s shared progress file can incorrectly make them visible, exactly as the first reader suspected.

**A-10 — narrowed — L-07’s parsing failure is real, but “EVERYTHING’S UP TO DATE” is not inevitable.**  
Evidence: `OfflineScanJob.cpp:196-205,252-257`; `GuiOfflineScan.cpp:299-304`; `CloudText.cpp:1253-1266`; `CloudText.h:488-504`; `ProxyCards.cpp:351-368`; `raofflineproxy-ctl:2043-2045,2403-2404` (excerpts where applicable).

The scan reader turns `unknown` into zero, and the stamp parser leaves an unparseable `ready` at its default zero. However, `added=unknown` already has a separate sentinel, and the card suppresses “EVERYTHING’S UP TO DATE” when that sentinel is present; the supplied stamp fixture demonstrates the narrower case with a numeric `added`. The pin already emits **`added=unknown`**—the new integration contract is specifically **`ready=unknown`**. T19’s new producer is supplied as a handoff description rather than its changed source, while both defective consumer behaviors are directly visible here.

**A-11 — confirmed — L-10 is more than an unsupported hypothetical producer claim.**  
Evidence: `OfflineScanJob.cpp:65-78,141-150,209-218`; `raofflineproxy-ctl:1706-1723,1771-1778` (excerpt).

Any later `>>> pid` line replaces the group identifier, and PID 1 becomes the special `kill(-1, SIGINT)` operation, signalling broadly permitted processes rather than one process group. The pin’s producer prints the game basename without control-character replacement, while the consumer treats carriage return as a line delimiter. A list entry whose basename contains a carriage return followed by `>>> pid 1` can therefore manufacture that second protocol line; proving the complete ROM-to-list path requires `list_jobs`, which is **outside the packet**. The first reader cannot use S9’s later sanitization to assert that the pin has no such producer path.

## 3. Lifetimes and threads

**A-12 — confirmed — L-21 is a real source-level lifetime race.**  
Evidence: `ThreadedHasher.cpp:99-108,123-139,213-247,257-265,375-392`.

After construction starts the workers, nothing in `start()` retains the object against the final worker’s `delete this`. A valid ordering is constructor return, worker completion and deletion, then the caller’s access to `mCheevosHashes` at `:378`, `mTotal` at `:383`, or publication at `:392`; the latter can publish an already-dead pointer after the worker’s null assignment. The silent lookup-only case is concrete **when at least one hash is recognized**; zero recognized hashes start no threads and are not this race. Such workers skip ROM hashing but can still write recovery metadata, so “no file read” must not be expanded into “no filesystem work,” and daily occurrence is not proved.

**A-13 — new — the hasher’s ownership problem also precedes and outlives the cited `start()` window.**  
Evidence: `ThreadedHasher.cpp:133-139,160-164,257-263,403-413`; `ThreadedHasher.h:24,61-73`.

The upfront thread count prevents deletion until all counted workers have run, but the last worker can run before the constructor finishes inserting its `std::thread*` into `mThreads`. That permits deletion while the constructor itself is still using the object. Separately, `stop()` takes an unretained pointer and writes through it while a worker can delete it; unsynchronized singleton reads and writes remain a race even if publication is moved earlier. An atomic singleton pointer alone would not supply the missing object lifetime.

**A-14 — confirmed — the scan page’s job ownership is sound for ordinary CANCEL and TRY AGAIN.**  
Evidence: `OfflineScanJob.cpp:35-47,86-116,160-168`; `GuiOfflineScan.cpp:90-91,122-133,144-160`; `GuiRetroAchievementsSettings.cpp:321-323` (excerpt).

The detached worker holds a shared reference, queued notifications hold another, and the cancellation dialog captures the particular job rather than the page. TRY AGAIN releases the finished job without invalidating an old worker or queued callback, and `close()` copies its callback before deleting the page. The supplied callback captures a weak row, not a raw scan-page pointer. The stated post-after-window-destruction protection depends on `AppWindow::post`, whose implementation is **outside the packet**; cancellation delivery and bounded completion are separate questions from this sound ownership arrangement.

## 4. Files and pages

**A-15 — confirmed — the shown existence checks are appropriate, and L-13 is real.**  
Evidence: `OfflineAchievements.cpp:98,127,136,147,156-160,192`; `GuiRetroAchievementsSettings.cpp:633` (excerpt); `FileSystemUtil.cpp:1369-1379,1418-1426` (excerpt).

All shown ctl-written paths use `exists(..., false)`, whereas the two cached checks concern the immutable image’s ctl executable. The short-file defect is in the BOM probe: a read of three bytes from a shorter file fails, and the subsequent seek does not clear the remaining failure state. Consequently `readAllText` can return empty for `7\n`, and the ready-count reader reports zero despite one exported ID. The source and supplied fixture support that conclusion independently of the later-composition guest page.

**A-16 — narrowed — the other file contracts are mostly deliberate, but their scope matters.**  
Evidence: `OfflineAchievements.cpp:114-138,173-197`; `raofflineproxy-ctl:803-819` (excerpt); `GuiOfflineScan.cpp:285-299`.

The rename-based flush take excludes two consumers from taking the same file; checking for its presence is not itself a take, and the claimed two consumer call sites are **outside the packet**. Online-state absence defaults to online only after availability, toggle, and local-address checks, and malformed/unreadable state also follows that default. The scan page rereads ready IDs every frame only after completion when no nonnegative `ready` was received—not throughout the scan. Those are design choices distinct from the short-file bug and from treating a failed count as a measured zero.

**A-17 — narrowed — the visible store/save wiring is consistent, but the complete row table is not independently verifiable.**  
Evidence: `GuiRetroAchievementsSettings.cpp:610-645,479-523,688-714,743-807`; `Settings.cpp:413,417-425`; `SystemConf.cpp:285-296`; `Paths.cpp:94` (excerpts).

The supplied rows select configuration storage for emulator-facing options and the settings-store flag for the two EmulationStation-facing switches; the offline result also mirrors configuration and immediately saves the startup-index setting. LED changes immediately update `SystemConf`, but that callback itself does not write the file. The progress-tracker, sound, unofficial-row implementations, builder save semantics, and the claimed complete list of external key consumers are **outside the packet**. The Windows-only hardcore default is not evidence of a second live Linux store, although the complete platform branch selecting the path is also not supplied.

**A-18 — narrowed — button order is verified at the shown calls, not throughout the GUI implementation.**  
Evidence: `GuiRetroAchievementsSettings.cpp:359-361,542-544,588-589` (excerpt); `GuiOfflineScan.cpp:147-151`; `ThreadedHasher.cpp:272-275`.

The supplied confirmation calls put NO, LATER, or NOT NOW last, matching the stated safe-last rule. The scan’s running-state input handler also refuses ordinary dismissal and offers cancellation instead. The back-button accelerator/fallback implementation and the game page’s LAUNCH/BACK construction are **outside the packet**, so those additional assertions are not independently established here. M7’s page frames cannot fill that source gap for the pin.

**A-19 — narrowed — L-14 is a user-choice integration defect, not inherently an illegitimate second writer.**  
Evidence: `GuiRetroAchievementsSettings.cpp:498-501,621,636`; `raofflineproxy-ctl:468-478,529-540` (excerpts).

The player may legitimately choose hardcore, but silently leaving both hardcore and a “casual achievements only” feature apparently enabled is not a satisfactory expression of that choice. The code also saves the pre-enable hardcore preference and later restores it, potentially overwriting a newer choice made while offline achievements was on. D-RA-001 establishes the casual-only product contract; it does not by itself require a permanently locked switch. A fix should explicitly reconcile the modes—through a switch-off offer, confirmation, or clearly explained gating—rather than dismissing the conflict as merely the player’s right.

## 5. The library

**A-20 — narrowed — the five edits are locally sensible, with one ownership proof outside the packet.**  
Evidence: `hash_disc.c:428-448,450-459,471-474,487-518,535-543`; `md5.c:70-83`; `cheevos.cpp:159-174`; `cheevos.h:5-8`; `CMakeLists.txt:232-245` (diff/excerpts).

The Nintendo-disc edits check the reads they alter, widen the header sum before clamping, and avoid signed high-byte shifts; they do not establish that every read in the entire imported file is checked. Removing the leaf function’s closes is correct under caller ownership, but the alleged caller close at `hash_disc.c:546` is **outside the packet**. The MD5 `memcpy` preserves the little-endian load while avoiding alignment/effective-type violations on the guarded x86 **and VAX** branches. The wrapper and declaration correctly expose a build capability and route only enabled GameCube RVZ inputs, with failure contained by the RVZ wrapper. CMake conditionally adds the reader and fails configuration without its dependencies; actual target-library selection and installation of notices require material outside this diff.

**A-21 — confirmed — the RVZ reader bounds file-derived allocations and arithmetic before using them.**  
Evidence: `rvz_hash.cpp:24-30,159-211,225-251,307-335`.

Header sizes, raw/group counts, chunk size, physical ranges, and decoded sizes are bounded before the corresponding vector allocation or table traversal. Count multiplications fit their types after the count checks, physical-range checks use subtraction, group offsets are widened before multiplication, and raw endpoints are formed only after checking `length <= discSize - offset`. The negative-seek guard rejects an extreme negative offset before negating it, while valid positions remain within the bounded disc size. In particular, `unpack`’s initially allocated `expected` size is bounded by its caller’s chunk-derived length; it is not an unchecked allocation from a raw file field.

**A-22 — confirmed — the shown decompression and buffer-access invariants withstand the identified hostile-input shapes.**  
Evidence: `rvz_hash.cpp:100-128,184-222,264-300,315-335,349-388`; `hash_disc.c:439-459,473-474,502-518` (diff/excerpt).

Compressed input and output are bounded, only one complete compressed frame is accepted, and decompression must return exactly the expected length; cumulative decoded work is capped at 512 MiB and logical reads at 128 MiB. Packed records have input/output-length checks and a record-count limit, including for zero-length records. The apparently unchecked `groups[index]` and `cache.size() - into` are protected by the validated raw extent/group-count relationship and exact cache length. I find no file-driven overflow, premature allocation, or buffer overread in this reader, but that is not a proof about zstd/intfstream internals or a wall-clock deadline for hashing.

**A-23 — confirmed — the padding commutation argument is correctly scoped.**  
Evidence: `rvz_hash.cpp:66-97`; supplied `stage-b/positives/lfg.out`.

Selecting output bits is linear over XOR, so moving that selection across the XOR-only `advance()` passes preserves the resulting bytes, including partial-word starting positions. This argument applies **after seed expansion**; it is not a claim that arbitrary bit selection commutes with the expansion’s shifts. The fixture’s unaligned cases and deliberately failing shift-16 control support the implementation comparison. The Dolphin transcription itself and three-hasher end-to-end equality are **outside the packet**.

## 6. Disposition of L-01 through L-25

The supplied `04` contains no `Already written:` assessments to endorse; the entries below provide bounded replacements for its High/Medium findings.

**A-24 — confirmed — L-01; Medium is defensible, with account-compromise impact.**  
Evidence: `RetroAchievements.cpp:1037`; `HttpReq.cpp:183-200,222-242`; `GuiRetroAchievementsSettings.cpp:610-616,777` (excerpts).

A stream should enforce certificate verification and prohibit credential-request downgrades, then migrate away from password-bearing URLs using a service-supported protocol rather than assuming POST compatibility. **Already written:** account configuration and password-bearing requests can predate the update; a transport fix cannot retract URLs retained by recipients or intermediaries. Actual retention, backup copies, and real compromise are **outside the packet**; credential rotation is a separate exposure response, not grounds to erase achievements.

**A-25 — narrowed — L-02; retain Medium for unbounded interface unavailability.**  
Evidence: `GuiRetroAchievementsSettings.cpp:758-806`; `RetroAchievements.cpp:1035-1040`; `HttpReq.h:52-54` (excerpts).

The defect is the synchronous `Now` branch, not every close or the watcher’s sign-in. A stream should move it off the interface thread, bound total/stall time, and associate the returned token with the account revision that requested it. **Already written:** settings and possibly a returned token can already have been stored; this scheduling fix does not undo a remote sign-in or establish any need to reset persistent account data.

**A-26 — narrowed — L-03; Low wording and disclosure-surface issue.**  
Evidence: `RetroAchievements.cpp:1040-1068,737,782`; `GuiRetroAchievementsSettings.cpp:782-792`; `GuiRetroAchievements.cpp:44` (excerpts).

The refused server error and account error surface remain real, while the normal curl/parse-to-`:784` claim is false. Map failures to player-facing categories and keep appropriately sanitized detail in diagnostics rather than treating an error string as safe merely because it is not named “password.”

**A-27 — narrowed — L-04; the username header is conditional and encoded.**  
Evidence: `RetroAchievements.cpp:145-149,178-195,855-866,1035-1037` (excerpts).

The User-Agent is derived from the URL-encoded `z=` field when API credentials exist, not directly from an unencoded username on every request. The same options helper is also used by sign-in and hash-library requests, so the inventory understates those header destinations while overstating unconditional use.

**A-28 — confirmed — L-05; Low, with a real data-omission consequence.**  
Evidence: `ApiSystem.cpp:2277-2288`; `raofflineproxy-ctl:738-744` (excerpts); `OfflineAchievements.cpp:250-262`.

The summary producer does not bound title length, so the long-line case is not excluded by its contract; ordinary ctl newline output does exclude the unterminated-line case under normal operation. Replace fragment parsing with a bounded logical-line reader and explicit oversized-record failure, then reread the summary rather than modifying the store to match an incomplete display.

**A-29 — narrowed — L-06; Low on the observed wrapper arrangement.**  
Evidence: `ApiSystem.cpp:2291`; `GuiRetroAchievementsSettings.cpp:481`; `ProxyCards.cpp:338-368` (excerpts).

Only normal exits may be decoded with `WEXITSTATUS`; signal and wait-error outcomes need distinct unsuccessful statuses. The guest narrows the triggering process to the wrapper but does not repair that contract.

**A-30 — narrowed — L-07; retain Medium for invented readiness claims.**  
Evidence: `OfflineScanJob.cpp:196-205,256`; `CloudText.cpp:1253-1266`; `CloudText.h:492`; `ProxyCards.cpp:351-368` (excerpts where applicable).

A stream must distinguish measured zero, explicit unknown, and a missing final report, preserving compatibility with older numeric stamps. **Already written:** integration can leave `ready=unknown` stamps beside valid cached data, while older stamps may contain zeros that cannot retrospectively be classified as measured or invented. Updating the reader must not discard cached games or awards; these display parsers do not establish any cloud-side loss.

**A-31 — confirmed — L-08; Low, and the correction to T19 is right.**  
Evidence: `CloudText.cpp:1022-1064`; `ProxyCards.cpp:293-320,376-379`; `raofflineproxy-ctl:2012,2206-2207` (excerpts).

`TOOK_TOO_LONG` reaches top-up wording through the fallback to `scanWhy`, whereas the new S5/S7 tokens have no dedicated rows. Add appropriate mappings and refusal handling, and stop borrowing another run’s progress/stamp; merely adding exit-code labels will not fix that attribution error.

**A-32 — confirmed — L-09; retain Medium, and widen it to existing partial-failure paths.**  
Evidence: `raofflineproxy-ctl:523-546`; `GuiRetroAchievementsSettings.cpp:490-501` (excerpts); `OfflineAchievements.cpp:168-170`.

A stream should reconcile authoritative resulting state on every outcome, separately from whether all requested operations succeeded. **Already written:** the toggle may already be off on disk, hardcore may have changed, and the marker may have been removed while the interface still believes the feature is on. A service can also remain alive; do not “repair” that ambiguity by automatically re-enabling the player’s setting, and do not infer what it subsequently sent to the cloud.

**A-33 — confirmed — L-10; the Low defence-in-depth characterization is insufficiently established.**  
Evidence: `OfflineScanJob.cpp:77-78,143-150,209-218`; `raofflineproxy-ctl:1721-1723,1772-1778` (excerpt).

The process identity must come from owned process creation, or at minimum from a strictly validated first wrapper line with PID greater than 1 and no later replacement. The pin’s unsanitized name-output boundary warrants testing before calling the root-wide signal case unreachable.

**A-34 — confirmed — L-11 is a design property, not a duplicate-consumption defect.**  
Evidence: `raofflineproxy-ctl:803-819` (excerpt); `OfflineAchievements.cpp:114-127`.

The same flush file is taken exclusively by rename, and a later producer replacement is a different file for another consumer. Malformed taken content is deliberately discarded; counting all callers requires code outside the packet.

**A-35 — narrowed — L-12 is the stated online-first fallback, including malformed state.**  
Evidence: `OfflineAchievements.cpp:173-197`; `RetroAchievements.cpp:517-522` (excerpt).

It applies only with the feature available/on and a local address present, and the shown page request has a total bound. It is a connectivity-display trade, not proof that the service or account is healthy.

**A-36 — confirmed — L-13; Low and directly repairable.**  
Evidence: `FileSystemUtil.cpp:1369-1379,1418-1426` (excerpt); `OfflineAchievements.cpp:152-165`.

Clear the stream error before rewinding, or use a short-read-safe BOM probe. Include zero-, one-, two-, and three-byte cases in the shared file-reader tests rather than special-casing one-digit game IDs.

**A-37 — narrowed — L-14 is a mode-reconciliation problem.**  
Evidence: `GuiRetroAchievementsSettings.cpp:621,636`; `raofflineproxy-ctl:468-478,535-540` (excerpts).

Two writers alone are not a defect, and the supplied register does not mandate an unchangeable hardcore switch. The silently contradictory state and restoration of an obsolete preference are the actionable problems.

**A-38 — narrowed — L-15’s storage choices are supported, its exhaustive consumer proof is not supplied.**  
Evidence: `GuiRetroAchievementsSettings.cpp:695,712-714,515-520`; `Settings.cpp:413` (excerpts).

The two switches visibly use the settings-store flag, and the offline-enable flow immediately saves the startup-index choice. The cited `GuiMenu`, `SystemView`, `SystemData`, and `NetworkThread` consumers are **outside the packet**.

**A-39 — narrowed — L-16 holds for the shown call-site ordering.**  
Evidence: `GuiOfflineScan.cpp:147-151`; `ThreadedHasher.cpp:272-275`; `GuiRetroAchievementsSettings.cpp:359-361,542-544,588-589` (excerpt).

Every supplied multi-choice confirmation places the safe option last. Back-button implementation and the game page’s button construction remain outside the packet, so “every dialog is safe” is broader than this independent verification.

**A-40 — narrowed — L-17 remains reported tooling evidence, not an independently checked map defect.**  
Evidence: `GuiOfflineScan.cpp:32`; `docs/es-menu-map.md:595` (**outside the packet**).

The scan title is directly established, but the map and checker implementation needed to establish its absence and the PL-07 drift are not supplied. Keep the documentation lead, without presenting the first reader’s grep as a second source inspection.

**A-41 — narrowed — L-18 is an extraction concern, not automatically a player-language defect.**  
Evidence: `GuiRetroAchievementsSettings.cpp:671` (**outside the packet**).

The reported runtime expression would not itself furnish a literal msgid to xgettext. The source and sound-name population are missing, and arbitrary player filenames need not be translated; inspect the packaged labels before prescribing a translation fix.

**A-42 — narrowed — L-19 has no guaranteed total interface-freeze bound.**  
Evidence: `ThreadedHasher.cpp:65,299-344,375`; `RetroAchievements.cpp:855-866`; `HttpReq.cpp:203-213`; `GuiRetroAchievementsSettings.cpp:798-800` (excerpts where applicable).

“About 40 seconds offline” is a scenario estimate, not a total-time contract: a sufficiently progressing transfer can continue indefinitely because only the low-speed bound is set. Treat this as Medium interface availability work for #300, moving fetch and preparation off the interface thread rather than merely adjusting the stall value. The other claimed interface-thread callers are **outside the packet**.

**A-43 — confirmed — L-20; I would downgrade Medium to Low for this isolated symptom.**  
Evidence: `RetroAchievements.cpp:890-925`; `HttpReq.cpp:559-563` (excerpts); `ThreadedHasher.cpp:110-117,394-399`.

The exception is sliced, but the underlying HTTP failure can still be present in earlier logs, so “diagnosis lost” is not absolute. Fix both rethrows and separately replace raw exception text on screen with a translated failure category. **Already written:** generic failure logs and possibly an offline-index marker can remain; this constructor-failure path has not started its hashing workers, and the display failure itself neither removes local awards nor changes cloud achievements.

**A-44 — confirmed — L-21; retain High.**  
Evidence: `ThreadedHasher.cpp:133-139,239-245,257-265,375-392,403-413`.

Move ownership to a retained job/controller, stop self-deletion, and coordinate worker completion, singleton publication, and cancellation under a coherent lifetime model. A short-queue scheduling test plus sanitizers is appropriate; proving actual exploitation is unnecessary to establish the unsafe lifetime. **Already written:** recovery metadata, the daily lookup stamp, and a destructor-triggered top-up may already have happened before the dangling-pointer failure. Preserve those artifacts and allow safe reconciliation/reindexing; the packet does not prove corrupt or lost cloud awards.

**A-45 — narrowed — L-22 has an active `mExit` race and a potentially dormant pause race.**  
Evidence: `ThreadedHasher.h:31-32,65,72-73`; `ThreadedHasher.cpp:188,201-207,411`.

`stop()` writes the plain exit flag while workers read it without matching synchronization. Pause/resume are similarly unsafe if invoked, but their claimed absence of callers is outside the packet; atomic flags fix visibility, not the separate dangling-object problem.

**A-46 — narrowed — L-23’s “identified a game” and “never offline” wording is too strong.**  
Evidence: `ThreadedHasher.cpp:75-108,114-115,144-157`; `OfflineAchievements.cpp:309-320`; `ProxyCards.cpp:306-309,588-594` (excerpt).

`mCheevosIndexed` means that a library and a nonempty queue existed, not that a worker successfully identified a game, and connectivity may disappear after the library fetch. The constructor’s offline marker path also tests the hashing queue rather than the separate lookup-only input. The intended reconnect design is plausible, but its complete retry implementation is **outside the packet**.

**A-47 — narrowed — L-24 is upstream/provenance bookkeeping, not proof of an incorrect edit.**  
Evidence: `hash_disc.c:428-518`; `md5.c:70-83` (diff/excerpts); `rvz_hash.cpp:1-5`.

The changed imported behaviors warrant the four upstream-tracking entries described. Upstream 12.5.0 contents, the complete notices, and `package.mk:58-64` installation are **outside the packet**, so “bounded and licensed” is not fully independently verified by naming those files.

**A-48 — confirmed — L-25’s padding conclusion, not three-reader compatibility.**  
Evidence: `rvz_hash.cpp:66-97,374-388`; supplied `stage-b/positives/lfg.out`.

The algebra and fixture support the padding equivalence, including unaligned output. They do not establish container interpretation, routing, or end-to-end hash equality across EmulationStation, the proxy, and RetroArch.

## 7. What the first reader missed

**A-49 — new — credential-adjacent command and diagnostic sinks need explicit inventory entries.**  
Evidence: `raofflineproxy-ctl:616,647,750-768,788`; `RetroAchievements.cpp:307,321,340`; `GuiRetroAchievementsSettings.cpp:792`; `HttpReq.cpp:559-567`; `ApiSystem.cpp:2284` (excerpts).

The ctl passes the username in Python argv, and its account reader accesses a cached login response explicitly described as containing a session token; that token’s producer is not established as this ES sign-in. Proxy errors, HTTP errors, and the conditional `tokenOrError` logger are unredacted diagnostic sinks, while accepted script stdout is printed verbatim. No supplied producer proves that a real password, token, or API key actually leaked through those error paths, and the `:792` branch’s reachability depends on the omitted retry policy. Nevertheless, “nothing needs masking because no URL is logged” is an unjustified taint-analysis shortcut.

**A-50 — new — thread-resource retention and additional lifetime boundaries were omitted.**  
Evidence: `ThreadedHasher.cpp:138-165`; `ThreadedHasher.h:61`; `GuiRetroAchievementsSettings.cpp:438-440,474-484,688-691`; `OfflineScanJob.cpp:103-115` (excerpts where applicable).

The hasher allocates `std::thread` objects but never joins, detaches, or deletes them, leaking thread objects and unreaped joinable-thread resources across runs. The LED callback also captures its own shared switch—the self-retaining pattern the offline-toggle comment explicitly warns against. The toggle’s detached worker dereferences a raw `Window*` to post its result, unlike the scan job’s guarded posting route. Whether shutdown can destroy that window first, or component teardown clears the LED callback, is **outside the packet** and must be checked before declaring either lifetime safe.

**A-51 — new — more readers collapse incomplete knowledge into success or zero.**  
Evidence: `OfflineAchievements.cpp:152-165,250-263,271-279`; `FileSystemUtil.cpp:1418-1426` (excerpt).

`storeSummary` sets `ok=true` after silently skipping every malformed nonempty record, so a wholly unreadable logical summary can become a successful empty summary even when the process exited normally. Independently of L-13 or S8, missing/unreadable ready-file content becomes an empty vector and then a numeric zero. Pending-ID read failure likewise returns the same empty collection as “none,” although the callers’ consequences are outside the packet. These APIs need validity/completeness alongside their data; exit-code filtering alone is not an end-to-end fail-closed proof.

**A-52 — new — login accepts success without a token, and untrusted JSON types are insufficiently checked.**  
Evidence: `RetroAchievements.cpp:1044-1064,871-887,896-909`; `GuiRetroAchievementsSettings.cpp:774-780` (excerpts).

A response containing `Success: true` but no `Token` returns true, so the shown caller stores its initially empty string and suppresses the failure path. Non-object roots, non-string token/error values, and non-object library members reach RapidJSON object/string/member operations without the corresponding type checks. Those are malformed-response crash/assertion risks, especially consequential beside unverified TLS, rather than errors reliably handled by `catch (...)`. Validate the response shape and require a usable token before reporting sign-in success.

**A-53 — new — completion and cancellation wording outrun what the code establishes.**  
Evidence: `ThreadedHasher.cpp:144-157,188,411`; `OfflineScanJob.cpp:65-80`; `GuiOfflineScan.cpp:114-119,147-151`.

A stopped hasher still emits “INDEXING COMPLETED”: only the later top-up is guarded by `!mExit`. Scan cancellation marks the job cancelled before attempting the signal, ignores signal failure, and refuses subsequent cancellation attempts once that flag is set. Because the page remains until `finished`, an undelivered or ineffective cancellation has no bounded escape in the shown code. Distinguish request, acknowledged stop, and completion, without weakening the otherwise sound shared ownership or signalling unowned processes.

**A-54 — new — stale progress affects the public running predicate, not just the settings row.**  
Evidence: `CloudText.cpp:1335-1343`; `ProxyCards.cpp:274-282,314-320,568-570`; `raofflineproxy-ctl:1786,2037,2062-2070` (excerpts).

There is no additional demonstrated misuse of cached `exists` here; the missed issue is interpreting a progress file as authoritative process liveness. A foreground scan can outlast the age assumption, and its image phase can continue after `run_jobs` removes the file, yet `topUpRunning()` directly returns that file-derived result. Separately, a top-up accepts another run’s progress and identifies its stamp only by timestamp, without matching route or run identity. Use an explicit run identity/liveness contract; changing filesystem cache flags cannot repair these semantics.

**A-55 — new — interface work remains unbounded by input size even after network fixes.**  
Evidence: `GuiOfflineScan.cpp:285-299`; `OfflineAchievements.cpp:152-165`; `FileSystemUtil.cpp:1418-1426` (excerpt); `ThreadedHasher.cpp:299-344,375`.

The finished scan’s fallback reads and parses the entire ready file every frame, with no byte/count bound in the shown read path. Hasher startup also materializes and traverses the game collection before any worker is started. Large or damaged persistent inputs can therefore stall the interface independently of the HTTP timeout defects. Bound and schedule these reads explicitly, preserving uncached change detection rather than introducing the very stale-file cache the project rules prohibit.