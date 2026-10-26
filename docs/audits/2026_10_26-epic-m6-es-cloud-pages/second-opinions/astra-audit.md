## 1. The protocol under a pipe

**A-1 — confirmed — F-03’s silent drop, with one state change.**  
Evidence: `CloudTransferJob.cpp:267-405`; `ThreadedCloudSync.cpp:249-335`.

The job handles all seven recognized marker kinds; the card intentionally ignores `Unit` and `Removed`. A parser result of `Unknown` becomes neither a why nor a live line in either reader, and neither reader logs it. It is not quite “nothing” on the card: its default arm clears `mWaitingForNetwork`. Correct classification does not establish correct payload handling or attribution, as the PID and tier issues below show.

**A-2 — narrowed — F-01.**  
Evidence: `CloudText.cpp:561-565`; `CloudTransferJob.cpp:272-278,153-161,637`; `ThreadedCloudSync.cpp:207,254-256,813-817,845-849`.

Neither reader enforces “the wrapper’s first line”: subsequent command output, including redirected stderr, can supply another accepted PID marker. Whether the pinned scripts actually emit one is **outside the packet**; the claimed repository-wide producer search cannot be independently verified here. A second marker overwrites `mPid`, but does not necessarily redirect an already-issued stop: the job deduplicates by signal, while an active card cancellation retains its first positive local `pid`. PID 1 is dangerous because negation produces `kill(-1, …)`, a broadcast to processes the sender may signal—not literally every process.

**A-3 — narrowed — F-02’s consequence, not the wrapper difference.**  
Evidence: `CloudTransferJob.cpp:615-624,636-638`; `ThreadedCloudSync.cpp:206-208,446-458,565-566`.

The job explicitly ignores SIGPIPE inside its brace group; the card does not. “The card’s scripts die at their next write before stamping” is too categorical: inherited signal disposition, script traps, write handling and the particular writer matter, and those implementations are **outside the packet**. The job also installs its trap **after** its PID echo, leaving that initial write unprotected. Neither cancellation path ordinarily closes the reader early, and surviving scripts would not make an already-dead ES process write its own `last-sync-*` outcome.

**A-4 — narrowed — the ordinary glued-progress case works; framing is not generally sound.**  
Evidence: `CloudTransferJob.cpp:654-677`; `ThreadedCloudSync.cpp:211-216,366`; `CloudText.cpp:813-843`.

The job explicitly splits an embedded `Transferred:`; the card’s `liveLine` finds the last such marker and can recover the following totals without preserving the preceding file line. That handles the demonstrated ordinary glue shape. But the card processes each 511-byte `fgets` fragment independently, while the job discards additional bytes after its buffer reaches 1,024 until a delimiter arrives. The first reader is wrong that a continuation necessarily “is not a protocol line”: a fragment beginning with `>>> ` can be classified as one, and either limit can damage a payload.

**A-5 — narrowed — `%3d` is handled; the broader pipe-soundness claim needs limits.**  
Evidence: `CloudTransferJob.cpp:513-554`; `GuiCloudTransfer.cpp:635-668`; `CloudTransferJob.cpp:748-750`; `CloudText.h:191-195`.

The backward separator search accepts both `name: 45%` and `name:100%`, rather than requiring `": "`, so the stated `%3d` fix is real. The page’s formatter also rejects several incomplete trailing fields instead of displaying torn speed or ETA text. Those are separate operations: accepting abbreviated size units does not prove that an actual 80-column line survives reading, splitting and formatting correctly. UTF-8 preservation is delegated to `cleanLine`; its complete implementation and the cited U+2026 test are **outside the packet**, so an end-to-end preservation verdict is not available here.

**A-6 — confirmed — junk can become meaningful zero outside the guarded status parser.**  
Evidence: `CloudText.cpp:158-174,561-565,594-597,604-635`; `CloudTransferJob.cpp:425-428,488-492,565-576`; `GuiCloudTransfer.cpp:450-455,750-760`.

PID and unit fields use `atoi`; junk becomes “no PID” or an unspecified/zero item count. Removed totals and several job-side rclone counters use the analogous `atol`, so malformed deletion totals can suppress the removal summary and affect partial/skip classification. Tier exit status is different: `wholeNumber` rejects junk as `-1`, not success. `parsePercent` likewise requires digits before `%`, so a wholly nonnumeric percentage does not silently become zero.

## 2. Lifetimes and threads

**A-7 — confirmed — the shown page/job deletion paths do not establish a use-after-free.**  
Evidence: `CloudTransferJob.cpp:54-76`; `GuiCloudTransfer.cpp:203-209,250-280,296-341,1062-1075`.

The worker owns a `shared_ptr` to its job, independently of the page. The page copies its continuations before deletion, unlocks before replacing or dismissing the job, and does not subsequently use its local job reference; an unlocked `unique_lock` does not unlock the destroyed mutex at scope exit. The posted page pointer is guarded by the weak lifetime token before dereference. There is also no demonstrated lock inversion in these paths: `start`/`dismiss` take the global job lock before the job lock, and the page releases the latter before calling them.

**A-8 — narrowed — the card’s access discipline is stronger than its lifetime promise.**  
Evidence: `ThreadedCloudSync.h:193-199`; `ThreadedCloudSync.cpp:56,68-70,716-731,773-779,793-860`.

Holding `sInstanceLock` through construction and installation prevents the worker’s clear from overtaking installation. The ordinary clear/linger/cancel interleaving is also safe against dereferencing the cleared object, because cancellation rechecks identity under the lock. But the header’s promise that the object “outlives the call” is too strong: the call releases that lock between polls and can retain an address beyond deletion; the linger is not ownership. The final SIGKILL also uses a cached PID outside the identity-checking lock, leaving a check-to-signal race, while `Window` and notification ownership guarantees are **outside the packet**.

**A-9 — narrowed — the job closes its named request races, not every cancellation race in this slice.**  
Evidence: `CloudTransferJob.cpp:79-162,200-202,272-278,684-710`; `ThreadedCloudSync.cpp:254-256,446-458,845-860`.

In the job, the finish check, stop marking and signal request share `mMutex` with finalization. Its shown `deliverStop` callers are serialized by that mutex; a pending request is delivered on PID arrival, SIGKILL cannot be downgraded, and a natural 0/9 completion clears the stop labels. This does not validate the PID’s provenance or protect against PID reuse. Nor does it establish equivalent behaviour in the card: the late-PID and completion/cancel defects described below remain there.

**A-10 — confirmed — F-06, including a missed false-success log.**  
Evidence: `ThreadedCloudSync.cpp:878-889,910-948`.

`writeStamp` attempts the rename without establishing that writing the temporary file succeeded, contrary to “written whole or not at all.” It notices rename failure only to remove the temporary file; directory failure and rename failure are not returned to its caller. Consequently, both restamping functions can log “restamped” after a failed operation. The particular unchecked `fwrite`/`fclose` implementation cited by the first reader is **outside the packet**, but the missing success judgement at this call site is visible.

**A-11 — confirmed — F-07; the budget comparison is not a justification.**  
Evidence: `FileData.cpp:997-1004`; `ThreadedCloudSync.cpp:834-862`.

The button callback calls `cancelForLaunch` synchronously, before it can select `launchWhenGone`. While that call is polling and sleeping, the interface thread cannot draw its next frame; if cancellation reaches 1.5 seconds, SIGKILL is sent without first displaying the later spinner. The instance lock is held only around individual accesses, not throughout the sleeps. Comparing this nominal two-second cancellation wait with the quoted three-second **exit-sync completion** target compares different measurements and does not establish an acceptable visible wait.

## 3. The words

**A-12 — confirmed — F-08’s wrong branch exists for a cancellable match.**  
Evidence: `GuiCloudTransfer.cpp:252-258,351-370`; `GuiCloudTransfer.h:158-162`; `GuiCloudTransfer.cpp:881-882,909-915`.

There is no Match arm in the confirmation and no Match exclusion in `cancellable()`: an unfinished, cancellable Match gets the backup/restore promise. Its own retry policy then refuses the same-command retry and selects match-specific recovery instead. Thus the mismatch is real in the page’s state machine, not disproved by a fixture that finishes before Back arrives. The particular match-construction caller and a successful rendered cancellation walk are **outside the packet**, so this is structural reachability, not a new guest observation.

**A-13 — narrowed — F-09/F-10’s text defects are visible; the panel-frequency claim is not.**  
Evidence: `GuiCloudTransfer.cpp:744-745,768-769,798-810`.

The alternative verbs and `DID NOT FINISH` are present on reachable rendering branches and conflict with the quoted canonical-verb/everyday-language requirements. The short “bring down/send up” forms are selected by measurement, however, not by a hardcoded 640×480 condition. Without fonts or frames, “that is the small panel, where most players read it” is unproved. Failure to obtain that frame does not turn a reachable prohibited wording into compliant wording.

**A-14 — narrowed — F-11’s translation path is real, but conditional.**  
Evidence: `CloudText.cpp:414-475`; `GuiMenu.cpp:5006,5043-5046`; `CloudTransferJob.cpp:280-287,302-334`; `GuiCloudTransfer.cpp:813-855`.

Both reported sentences are absent from `whySentences`, and unlisted sentences pass through unchanged. The settings-restore composition preserves `backuptool restore` output; a separately framed why followed by a non-skipped failed SETTINGS tier reaches line 4, subject to fitting/ellipsis. A completed-action callback does not hide that failure path. The actual `backuptool:1495` emission and exit status are **outside the packet**, so “it always reaches line 4” is stronger than the supplied code proves; a skipped CREATE run suppresses line 4 as reported.

**A-15 — refuted — the fallback comparison is not a verified equivalence.**  
Evidence: `ThreadedCloudSync.cpp:80-115`; `ThreadedCloudSync.h:93-99`; `CloudTextTests.cpp:659-664`.

The two old header phrases demonstrably differ from the implementation. But the comparison omits code 6: the implementation falls back to `SOMETHING WENT WRONG`, whereas the emitter fixture names `SOME FILES DIDN'T FINISH`. The fixture also distinguishes automatic 10/124 wording from the implementation’s generic 10 and “stopped answering” 124. Current script functions and the complete rule are **outside the packet**: the first reader cannot infer “agreement on every group” from its selected rows.

**A-16 — narrowed — F-15 counts unlike things together.**  
Evidence: `CloudText.cpp:407-411,432,462,1384-1387`; `ThreadedCloudSync.cpp:91-92,534-537,670-671,781`.

This is not eight competing outcome phrases for the same display slot. The count mixes complete outcomes, bare reasons, punctuation variants, a recovery instruction, and descriptions of different activities or locks. The scan-specific wording is explicitly selected by kind, while the ordinary card and page lock outcome agree. Any remaining synonym drift deserves review, but the raw string count alone does not demonstrate eight least-surprise failures.

## 4. The tests

**A-17 — confirmed — F-12; the claimed guard is not the implemented guard.**  
Evidence: `CloudText.cpp:419-422`; `CloudTextTests.cpp:632-719,722-729`.

The test iterates a typed array; it does not discover current script emitters. Its classification assertions and `isKnownWhy` check protect only the listed fixtures, and the redundant “not Unknown/not NotProtocol” assertions add no source-coverage guarantee. A new script sentence absent from that array passes unnoticed. The following spelling test is explicitly built without gettext, so it is not proof of French catalogue availability or runtime lookup.

**A-18 — narrowed — F-05 and the claimed piped-progress coverage.**  
Evidence: `CloudTextTests.cpp:859-875,907-935`; `CloudTransferJob.cpp:529-554,654-677`; `GuiCloudTransfer.cpp:635-668`.

The supplied tests genuinely exercise `liveLine` with glued totals and `parseBytes` with abbreviated units. They do not exercise the job’s character reader, its `%3d` filename separator, or the page formatter’s rejection of a complete line’s torn trailing field. Those are distinct traps, not coverage inherited from calling a related pure function. The claimed U+2026 case at `CloudTextTests.cpp:564`, and a whole-suite search establishing that no other cases exist, are **outside the packet**.

**A-19 — narrowed — passing tests do not establish the broader lifetime claims.**  
Evidence: `CloudTransferJob.cpp:87-162,684-727`; `ThreadedCloudSync.cpp:446-458,784-863`; `GuiCloudTransfer.cpp:1065-1075`.

The reported passes are accepted, but the `JobsTests.cpp` and source-reading `AtomicFileTests.cpp:792` bodies are **outside the packet**, so their exact assertions cannot be independently graded here. ASan/UBSan success is not a general data-race proof. No supplied case establishes card cancellation after a late PID, cancellation against natural completion, page deletion before posted continuation, or stamp-write failure handling. Real-pipe fragmentation, repeated/invalid PIDs, normalized why lookup, and actual translated fitting also need direct tests rather than the current table’s coverage claims.

## 5. Findings F-01–F-19 and proposed bugs B1–B4

**A-20 — narrowed — F-01, F-02, F-04.**  
Evidence: `CloudTransferJob.cpp:153-161,272-278,636-677`; `ThreadedCloudSync.cpp:206-216,254-256,845-860`.

F-01 is unsafe PID acceptance, but “every process” and unconditional redirection by a second PID overstate its effect. F-02 identifies a real wrapper asymmetry, not an unconditional proof of script death or stamp survival. F-04 identifies broken long-line framing; its continuation behaviour is less predictable than “the second half is not protocol.”

**A-21 — confirmed — F-03, F-06, F-07.**  
Evidence: `CloudTransferJob.cpp:399-405`; `ThreadedCloudSync.cpp:330-334,834-862,930-948`; `FileData.cpp:1001-1004`.

F-03’s silent discard is confirmed, with the card’s waiting-state reset noted above. F-06’s unchecked-write-to-rename sequence is confirmed, without accepting every claimed corruption consequence. F-07 is confirmed as synchronous interface-thread blocking, not as a claim that every cancellation lasts two seconds.

**A-22 — confirmed — F-08, F-10, F-12.**  
Evidence: `GuiCloudTransfer.cpp:351-370,744-769`; `CloudText.cpp:419-422`; `CloudTextTests.cpp:638-719`.

F-08 is a wrong promise on the cancellable-Match branch, although no rendered invocation is supplied. F-10’s cited wording is present and falls under the quoted language requirements. F-12 correctly identifies a source-coverage guard claimed by a comment but absent from the test.

**A-23 — narrowed — F-05, F-19.**  
Evidence: `CloudTextTests.cpp:859-875,907-935`; `CloudTransferJob.cpp:529-554,654-677`.

F-05 is established as a gap in the supplied tests, not independently as a repository-wide absence. For F-19, the reported six passing cases stand, but their complete coverage and the assertion that no standing command builds them are **outside the packet**.

**A-24 — narrowed — F-09, F-11.**  
Evidence: `GuiCloudTransfer.cpp:805-810,813-855`; `GuiMenu.cpp:5043-5046`; `CloudText.cpp:414-475`.

F-09’s wording exists, but its actual selection on the smallest shipped panel is unproved here. F-11’s missing lookup entries and conditional English line-4 path are established; the actual backend emission/status and rendered French failure are **outside the packet**.

**A-25 — narrowed — F-13, F-14.**  
Evidence: `CloudText.h:16-18,78-82`; `CloudText.cpp:410-411,424-465`; `ThreadedCloudSync.h:70,93-99,126-130`; `ThreadedCloudSync.cpp:84-94,114,516`; `GuiCloudTransfer.h:156-162`.

Several present-tense comments plainly contradict the implementation: translation being outside `CloudText`, “four” outcome words, old fallback/cancel wording, the token list, and Back leaving the page. The additional claims about `shortenWhy`’s implementation and omitted header passages are **outside the packet**. F-14 is supported only as comparison with the supplied quotations; the actual rule file and its complete SKIPPED table are **outside the packet**.

**A-26 — narrowed — F-15.**  
Evidence: `CloudText.cpp:407-411,462,1386-1387`; `ThreadedCloudSync.cpp:92,536,781`.

The finding establishes wording proliferation, not eight interchangeable outcomes violating a single contract. Distinct lock owners and recovery instructions should not be flattened merely to reduce a string-set count.

**A-27 — narrowed — F-16, F-17.**  
Evidence: `CloudTransferJob.cpp:387-390`; `GuiCloudTransfer.cpp:190-198,1027-1032`; `GuiCloudTransfer.h:76-100`; `CloudText.cpp:429,1104-1108`; `CloudTextTests.cpp:717-718`.

The alleged retirement leftovers exist, but establishing that every hook and emitter is unused requires caller/producer searches **outside the packet**. `isKnownWhy` demonstrably serves a test oracle, so “test-only” is not itself a removal argument; the same distinction applies to the stated purpose of `isKnownUnitLabel`. The `nextTime` declaration, implementation and usage census are **outside the packet**.

**A-28 — narrowed — F-18.**  
Evidence: `CloudTransferJob.cpp:267-405,636-677`; `ThreadedCloudSync.cpp:206-335`.

A shared wrapper, framing layer and trusted-PID mechanism would address genuine duplicated responsibilities. Simply copying the job reader would retain its cap/discard and marker-framing problems, while making both surfaces act identically would incorrectly erase their intentional differences.

**A-29 — narrowed — B1: Low is defensible, but the proposed guarantee and inheritance account need correction.**  
Evidence: `CloudTransferJob.cpp:615-638`; `ThreadedCloudSync.cpp:206-208,446-458,565-566`.

Low is reasonable for the demonstrated risk of interrupted reporting, but the packet does not prove universal SIGPIPE death or save corruption. Share the wrapper and install the ignored disposition before the PID echo, then test early reader closure with the actual shell/script environment; merely copying the existing string leaves its first-write window. The fix must not promise that rclone completes or that dead ES writes its own outcome. **Already written:** previous local stamps can remain while some transfer work has already happened, so “nothing inherited” is too broad even though no stamp-format migration follows; exact device/cloud residues are **outside the packet**.

**A-30 — narrowed — B2: confirmed writer defect, narrower confidence about its consequences.**  
Evidence: `ThreadedCloudSync.cpp:930-948`; `CloudText.h:115-116`; `CloudText.cpp:291-296`; `GuiMenu.cpp:5064-5068`.

Low is defensible for a local reporting-record defect, but “every truncated stamp reads as never run” is not established: the documented format accepts legacy two-field records, and the complete parser is **outside the packet**. A checked replacement writer is the right fix direction, provided its result reaches callers; `AtomicFile::writeText` is visibly available, but its exact guarantees are **outside the packet**. Test failed creation, write/close failure, rename failure and stale temporary files against preservation of the old record. **Already written:** devices may retain old, empty or truncated stamps, whose lost history cannot be reconstructed; this writer itself changes no cloud data, and preserving legacy readability matters more than inventing a migration.

**A-31 — confirmed — B3: Low text defect; the fourth arm must describe a match, not generic resumability.**  
Evidence: `GuiCloudTransfer.cpp:351-370,874-882,909-915`.

Low is appropriate for this misleading cancellation explanation. A Match-specific arm should explain what remains removed and that continuing requires another check, rather than promise that a backup or restore completes the match. A focused text/state test plus translated 640×480 rendering is better evidence than a frame alone. **Already written:** the dialog introduces no persistent format, but previously completed match deletions are not rolled back by cancellation, so “nothing inherited” must not be read as “no persistent effects.”

**A-32 — narrowed — B4: Low lookup defect; the proposed unit-test recipe is insufficient as stated.**  
Evidence: `CloudText.cpp:414-475`; `CloudTextTests.cpp:717-727`; `GuiCloudTransfer.cpp:813-855`.

Adding the missing pairs and catalogue entries is appropriate once their current emitters are verified. However, a host assertion that `localizedWhy(sentence)` equals its English input will pass both before and after adding a pair: the no-gettext build and unknown fallback both return English. The regression must check membership after protocol normalization, or use a distinguishable translation, alongside a source-reading emitter check. **Already written:** retain English stamp payloads as the documented storage format; this is a lookup/catalogue repair, not a reason to rewrite historical outcomes or cloud content.

## 6. What the first reader missed

**A-33 — new — the card can stamp a naturally completed run as launch-cancelled.**  
Evidence: `ThreadedCloudSync.cpp:446-458,514-518,565-566,716-719,813-817`; `CloudTransferJob.cpp:691-696`.

After `pclose` returns 0 or 9, the card remains reachable through `mInstance` until much later. A cancellation in that interval can set `mCancelled` before the worker samples it, causing unconditional replacement of a genuine success with 130 and the `cancelled` token—even if the signal reached nothing. The job expressly handles this completion race; the card does not. This needs a coordinated finish/cancel decision and regression tests for both orderings, not just pointer-lifetime tests.

**A-34 — new — a card stop requested before a sufficiently late PID is never delivered.**  
Evidence: `ThreadedCloudSync.cpp:254-256,813-817,845-862`; `FileData.cpp:1001-1004`; `CloudTransferJob.cpp:129-161,272-278`.

If the PID is still unavailable when the two-second polling budget ends, the card retains only `mCancelled`, not a pending signal that its PID handler delivers. A later PID assignment therefore lets the command continue while its eventual outcome is labelled cancelled. The caller’s spinner prevents immediate launch over that work, but it does not repair the missing stop request. The job’s durable request/PID handshake is the relevant model.

**A-35 — new — an unterminated rclone tail can swallow the following protocol marker.**  
Evidence: `CloudTransferJob.cpp:641-669,502-554`; `CloudText.cpp:558-559,863-866`; `ThreadedCloudSync.cpp:249-250,366`; `GuiMenu.cpp:5006`.

The job recognizes glued `Transferred:`, not a glued `>>> tier` or `>>> why`. If an unterminated per-file tail is followed directly by the composer’s echo, classification sees `NotProtocol`; the job treats it as file text and the card can discard it as a per-file line. Unknown-marker logging would not detect this loss. Whether the intervening pinned scripts always supply a separating newline is **outside the packet**, so this needs a real-pipe producer fixture rather than the first reader’s blanket “all traps handled” assurance.

**A-36 — new — an existing why-table entry cannot match its normalized protocol text.**  
Evidence: `CloudText.cpp:425,469-482,571-579`; `CloudTextTests.cpp:638-680,717-727`.

`CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.` is stored with a final period, but the protocol parser removes trailing periods. The parsed sentence therefore fails both exact membership and translation lookup despite having a table row. Comparing the two literals within each pair does not catch that mismatch, and the supplied emitter fixture list omits this sentence. Test every table entry through protocol normalization, and normalize lookup keys consistently.

**A-37 — new — a later tier’s early failure can be blamed on the preceding tier’s unit.**  
Evidence: `CloudTransferJob.cpp:280-287,308-330,333-335,352-375`; `GuiCloudTransfer.cpp:823-845`.

A tier boundary clears pending whys and announced-unit tracking, but leaves `mUnitLabel` standing. After a successful SAVES tier, a subsequent part that prints its why before announcing any unit is recorded as a SAVES failure, not as the subsequent tier’s failure. This contradicts the stated before-unit attribution rule and can name an already successful item on line 4. Attribution needs current-tier unit context separate from the last displayed label.

**A-38 — new — the composers and readers disagree about successful exit 9.**  
Evidence: `GuiMenu.cpp:5006,5046,6140-6141`; `GuiCloudTransfer.cpp:435-451`; `ThreadedCloudSync.cpp:483-495`.

The transfer composer overwrites its accumulated error with every nonzero part status, including 9: a sequence such as failure 5 followed by successful “nothing to move” 9 finishes with 9, which the page calls COMPLETED despite the failed tier. Conversely, the manual-sync composer exits immediately on restore status 9, skipping its backup half, while the card still calls 9 completed. Current scripts’ normalization of rclone 9 is **outside the packet**, but these components disagree on a status their readers explicitly support. Fix aggregation and continuation predicates together, and test composition—not merely individual status parsing.

**A-39 — new — settings-backup diagnostics are discarded before this parser can use them.**  
Evidence: `GuiMenu.cpp:5117-5125`; `CloudTransferJob.cpp:327-330`; `CloudText.cpp:451-465`.

The settings-backup caller redirects all `backuptool backup` output to `/dev/null`, unlike the restore caller. Thus any useful why it emits cannot reach the page, and an otherwise unexplained tier failure falls back to the exit-code map. Adding translation rows or strengthening the emitter table cannot repair that routing loss. The actual emitted diagnostics are **outside the packet**, but the unconditional redirection is visible and belongs with the caller’s audit.

**A-40 — narrowed — “every row is fitted, therefore no wrapping trap” is not established.**  
Evidence: `GuiCloudTransfer.cpp:56,73-74,913-915,935-939,984-986,1035`; `GuiCloudTransfer.h:171-175`.

Several paths do not pass their text through fitting: the initial title, the finished footer, the running item counter, and some activity strings are examples. Consequently the first reader’s universal explanation for why padding/wrapping cannot matter is wrong, independently of whether today’s English strings happen to fit. `TextComponent`’s implementation, actual fonts and the relevant frames are **outside the packet**. This is an unresolved rendering-proof obligation, not proof that a specific supplied frame clips.

**A-41 — narrowed — “no test whose subject is gone” was not demonstrated.**  
Evidence: `CloudTextTests.cpp:632-719,722-729`; `CloudText.cpp:429,1104-1108`; `GuiCloudTransfer.h:76-100`.

The supplied tests still exercise living parser and table functions, so I cannot honestly name a demonstrated deleted-subject test from these excerpts. But “every case’s function exists” is not the required check: a function or table row can survive after its only product flow is retired. Tests concerning `nextTime`, migration hooks or discarded-save labels, and the complete usage census, are **outside the packet**. The first reader’s negative conclusion should remain unproved pending that feature-level comparison.

**A-42 — new — two dispositions should change.**  
Evidence: `FileData.cpp:1001-1004`; `ThreadedCloudSync.cpp:834-862`; `GuiCloudTransfer.cpp:744-769,805-810`.

F-07 is an interface-blocking defect under the quoted visible-wait requirement, not merely a modernization preference; its repair needs coordination between the caller and this blocking API. F-09’s classification should not depend on whether one particular 640×480 walk selected the short candidate: reachable forbidden wording is a text defect, while the frame establishes its presentation and frequency. Conversely, F-15’s mixed string count is not sufficient grounds for a bug or wholesale wording unification.