### 1. The protocol under a pipe (`02` § The protocol; F-01 to F-05, F-18)

**R-1** — *narrowed*
`CloudText.cpp:485, 555-644`, `CloudTransferJob.cpp:267-406`, `ThreadedCloudSync.cpp:249-335`
Both readers classify lines through `CloudText::classifyProtocolLine`, and the card intentionally drops `Unit` and `Removed` at `ThreadedCloudSync.cpp:330-332` while the job acts on all seven known kinds. However, several reader handlers have state flaws: `CloudTransferJob.cpp:333-336` (`case Tier:`) does not clear `mUnitLabel`, so a subsequent tier that emits `>>> why` before its first `>>> unit` is blamed on the previous tier's last unit (`:287, 310-314`; A-37). In addition, `CloudTransferJob.cpp:382-391` (`case Doing:`) does not clear `mCurrent`, `mChecksTotal`, or `mListed`, which take precedence over `mDoing` in `GuiCloudTransfer.cpp:946-1035`. Finally, because `cleanLine` trims trailing whitespace before `classifyProtocolLine` runs (`CloudTransferJob.cpp:673`, `ThreadedCloudSync.cpp:216`), a marker with an empty argument such as `">>> why "` is trimmed to `">>> why"`, fails `clean.rfind(">>> why ", 0) == 0` (`CloudText.cpp:571`), and becomes `Unknown` instead of an empty `Why` (`CloudTransferJob.cpp:284`).

**R-2** — *narrowed*
`CloudText.cpp:558, 640-641`, `CloudTransferJob.cpp:268, 399-405`, `ThreadedCloudSync.cpp:250, 330-334`
Any line starting with `">>> "` that does not match one of the seven prefixes with a trailing space is classified as `ProtocolKind::Unknown` (`CloudText.cpp:640-641`). In `CloudTransferJob::handleLine`, `Unknown` hits `default:` (`CloudTransferJob.cpp:399-403`) and returns early (`:405`) without logging or reaching the rclone parsers. In `ThreadedCloudSync::run`, `Unknown` hits `default:` (`ThreadedCloudSync.cpp:330-332`), clears `mWaitingForNetwork = false;`, and continues (`:334`) without logging or reaching `CloudText::liveLine`. The first reader is right that neither reader logs `Unknown` (F-03), and the first seat (A-1) is right that the card's `default:` also mutates `mWaitingForNetwork`.

**R-3** — *narrowed*
`CloudTransferJob.cpp:636-637`, `ThreadedCloudSync.cpp:206-207`
The two wrappers differ by `{ trap '' PIPE; ... ; }`: `CloudTransferJob.cpp:636-637` ignores `SIGPIPE` around `mCommand`, whereas `ThreadedCloudSync.cpp:206-207` does not. However, in `CloudTransferJob.cpp:637`, `echo ">>> pid $$"` sits outside `{ trap '' PIPE; ... ; }`, so its very first write is still unprotected if the pipe closes immediately (A-3). Whether the scripts themselves die before writing their stamp when EmulationStation exits depends on whether they write to the pipe before stamping and on their own signal traps, which are `outside the packet` (cited in `02` as `cloud_backup:2504`).

**R-4** — *narrowed*
`CloudText.cpp:561-565`, `CloudTransferJob.cpp:153-162, 272-279`, `ThreadedCloudSync.cpp:254-256, 815-817, 845-850, 857-861`
Within the packet, only the two wrappers at `CloudTransferJob.cpp:637` and `ThreadedCloudSync.cpp:207` emit `>>> pid` (other ES files and the scripts are `outside the packet`). Both readers assign `mPid = protocol.number` on every `Pid` line without checking whether `mPid` was already set (`CloudTransferJob.cpp:275`, `ThreadedCloudSync.cpp:255`). However, the first reader overstates what a second `>>> pid` would do: in `CloudTransferJob.cpp:159`, `mSignalSent.exchange(sig) == sig` prevents re-sending a signal already sent, and in `ThreadedCloudSync.cpp:845`, `cancelForLaunch` only re-reads `sync->mPid` while its local `pid <= 0`. Conversely, both the first reader and the first seat missed that if a second `>>> pid` line carries non-numeric text or `0` (`atoi` returns `0` at `CloudText.cpp:564`), it overwrites a valid `mPid` with `0` and disarms any subsequent stop (`CloudTransferJob.cpp:157`, `ThreadedCloudSync.cpp:816`).

**R-5** — *narrowed*
`CloudTransferJob.cpp:410-558, 654-677`, `GuiCloudTransfer.cpp:635-689`, `CloudText.cpp:485-493, 807-877`
The rclone parsers handle the `%3d` colon separator at `100%` (`CloudTransferJob.cpp:535-551`), keep UTF-8 including U+2026 (`CloudText.h:191-195`, `CloudText.cpp:485-493`; body of `cleanLine` at `:494-533` is `outside the packet`), and drop 80-column torn fields in `GuiCloudTransfer::prettyRclone` (`GuiCloudTransfer.cpp:646-668`). However, the pipe handling has two real holes against rclone's observed output: first, in `CloudTransferJob.cpp:660-669`, once `buf.size()` reaches the 1,024-byte cap, characters are dropped and a glued `"Transferred:"` marker cannot be matched or split. Second, as `CloudTransferJob.cpp:645-647` notes, piped rclone ends its redraw block after the last `" * file"` line *without a newline*; when rclone exits after that block and the script or shell immediately prints `>>> why ...` or `>>> tier ...`, neither `CloudTransferJob.cpp:663` (which splits only on `"Transferred:"`) nor `ThreadedCloudSync.cpp:212` nor `CloudText.cpp:558` splits on `">>> "` mid-line, so the protocol line is glued onto the `" * file"` line and lost (A-35, which is more than merely plausible given `:645-647`).

**R-6** — *confirmed*
`CloudText.cpp:158-175, 564, 596-597, 609-610, 620-621, 635`, `CloudTransferJob.cpp:425, 488-492, 575`, `GuiCloudTransfer.cpp:451, 750, 882`
`CloudText.cpp:596-597` uses `wholeNumber` for `>>> tier` specifically because `atoi` reads junk as `0` (success). However, `CloudText.cpp:620-621, 635` uses `atol` on `>>> removed <files>|<bytes>`, so a corrupted `files` field parses as `0`, suppressing both partial-failure detection (`GuiCloudTransfer.cpp:451`), the removal summary (`:750`), and the cut-match note (`:882`; A-6). In `CloudTransferJob.cpp:425`, `atol(body.c_str())` parses the `Transferred:` file-count line; if a malformed or torn `Transferred:` line has `'/'` and no `"iB"` or `" B"` and starts with non-digits, `files` reads as `0`, triggering `if (files < mUnitFiles) mRunFiles += mUnitFiles;` (`:426-428`) and double-counting the unit's files on the next block. And in `CloudText.cpp:564`, `atoi` on a malformed `>>> pid` line returns `0`, clearing `mPid`.

---

### 2. Lifetimes and threads (`02` § The lifetimes; F-06, F-07, F-19)

**R-7** — *narrowed*
`GuiCloudTransfer.cpp:171-175, 203-210, 250-343, 1068-1075`, `CloudTransferJob.cpp:42-77`
Neither `GuiCloudTransfer::advance()` (`GuiCloudTransfer.cpp:203-210`) nor `GuiCloudTransfer::input()` (`:296-343`) dereferences `this` after `delete this` (`:207, 328`), and the posted lambda at `:1070-1075` is safely guarded on the UI thread by `mAlive` (`:173-174`). One subtlety in `GuiCloudTransfer.cpp:250-343` should be noted: at `:326-328`, `CloudTransferJob::dismiss(mJob)` clears `sCurrent`, and `delete this` destroys `this->mJob`, which—since `job.mFinished` is already true—is normally the last `shared_ptr<CloudTransferJob>`, destroying the `CloudTransferJob` object while local variable `CloudTransferJob& job` (`:250`) and `std::unique_lock<std::mutex> lock(job.mMutex)` (`:251`) are still in scope until `:343`. No use-after-free occurs only because `lock.unlock()` was called at `:323` (so `~unique_lock()` does not touch `job.mMutex`) and `job` is not read after `:322`, but `lock` and `job` dangle across lines 328-343.

**R-8** — *refuted*
`ThreadedCloudSync.cpp:254-263, 446-458, 494, 716-758, 796-863`, `ThreadedCloudSync.h:193-200`, `FileData.cpp:993-1007`
The first reader's claim that `mInstance` and the 1.5 s / 5 s linger are sound against `cancelForLaunch` is wrong for four distinct reasons:
1. `ThreadedCloudSync::run()` reaps the child process in `pclose(pipe)` at `ThreadedCloudSync.cpp:446` and latches `const bool cancelled = mCancelled;` at `:456`, but does not clear `mInstance` until `:717-720` (after stamp I/O and `OfflineAchievements::pendingAwards()` at `:510-707`). A `cancelForLaunch` arriving between `:446` and `:456` overwrites a completed run (`ret == 0 || ret == 9`) with `CloudExit::Stopped` (`SKIPPED - YOU STARTED A GAME`, A-33); a `cancelForLaunch` arriving between `:456` and `:717` calls `::kill(-pid, SIGTERM/SIGKILL)` (`:817, 859`) on an **already-reaped PID** while its `sync->mCancelled = true` (`:813`) is ignored because `cancelled` was already latched as `false` at `:456`!
2. `run()` clears `mInstance = nullptr` at `:717-720` *before* sleeping 1.5 s or 5 s (`:731`), and then calls `CloudOffer::present(mWindow, mOffer, mOfferArgs)` (`:741`) and `ProxyCards::afterSync(mWindow)` (`:755`) *after* the sleep; if a game launches during that 1.5 s / 5 s linger (`FileData.cpp:993` sees `isRunning() == false`), the offer dialog or achievements card fires right over the launching game!
3. If `>>> pid` has not arrived before the 2 s spin in `cancelForLaunch` times out (`:845-856`), `mCancelled` is set (`:813`) but `ThreadedCloudSync.cpp:254-256` has no `deliverStop()` when `Pid` later arrives, so the child process continues running un-signalled (A-34).
4. `run()` writes `mPid` (`:255`) and `mWaitingForNetwork` (`:263, 311, 321, 326, 331, 336`) and reads `mCancelled` (`:456`) without holding `sInstanceLock` (whether their declarations in `ThreadedCloudSync.h:144-181` are `std::atomic` is `outside the packet`), and `cancelForLaunch` sends `SIGKILL` at `:859` outside `sInstanceLock` using a cached `pid` (A-8).

**R-9** — *confirmed*
`ThreadedCloudSync.cpp:878-881, 910-927, 930-949`
F-06 is right: `ThreadedCloudSync::writeStamp` (`:930-949`) writes `tmp` via `Utils::FileSystem::writeAllText` (`:944-946`, whose body in `FileSystemUtil.cpp` is `outside the packet`) and immediately calls `std::rename(tmp.c_str(), path.c_str())` (`:947`) without checking whether the write or close succeeded. On a full `/storage`, a truncated or empty `.tmp` replaces the last known good stamp at `path`, and if `writeAllText` fails to open `tmp` when a stale `.tmp` file already exists on disk, `std::rename` replaces `path` with the stale `.tmp`. In addition, `restampStoppedParts` (`:914-915, 924-925`) logs `"restamped as ..."` unconditionally because `writeStamp` returns `void` (A-10).

**R-10** — *confirmed*
`ThreadedCloudSync.cpp:834-863`, `FileData.cpp:993-1007`
F-07 is right: `FileData.cpp:1001` calls `ThreadedCloudSync::cancelForLaunch(&again, true)` synchronously inside the `GuiMsgBox` `STOP IT AND PLAY` callback on the UI thread. `cancelForLaunch` spins in `std::this_thread::sleep_for(std::chrono::milliseconds(20))` (`ThreadedCloudSync.cpp:862`) for up to `2000` ms (`:855`), sending `SIGKILL` at `1500` ms (`:857-861`), so no frame is drawn and no spinner can appear during that 2 s window. However, the first reader's `04` § Q5 wrongly compares this 2 s UI freeze to D-CLOUD-119's 3 s exit-sync completion budget (`Context 3`), whereas D-CLOUD-109 and D-CLOUD-129 require the launch stop wait to be visible behind a spinner (A-11).

**R-11** — *refuted*
`CloudTransferJob.cpp:87-162, 272-279, 679-712`
The first reader (and the first seat in A-9) claims that `stopForLaunch`, `stopByPlayer`, `requestStop`, and `deliverStop` close every race in `CloudTransferJob`. While they do close the pre-PID stop race (`:139-162, 272-279`) and the natural-completion (`ret == 0 || ret == 9`) race (`:87-127, 691-696`), a race remains open between `pclose(pipe)` at `CloudTransferJob.cpp:679` and `std::unique_lock<std::mutex> lock(mMutex)` at `:684`:
1. `pclose(pipe)` at `:679` waits for and **reaps** the child process `mPid` before `mMutex` is locked at `:684` and before `mFinished` is set to `true` at `:727`; if `stopForLaunch` or `stopByPlayer` is called in that window, `deliverStop()` (`:161`) calls `::kill(-pid, sig)` on an already-reaped PID!
2. If the command had already finished on its own with a **non-zero failure or sentinel** (`ret != 0 && ret != 9`, e.g., exit `5`, `69`, or `75`) at `:681`, and `stopForLaunch` or `stopByPlayer` arrives before `:684`, line 691 (`if ((mStoppedForGame || mStoppedByPlayer) && (ret == 0 || ret == 9))`) does **not** clear the stop flags! Line 701-704 then sets `ret = CloudExit::Stopped`, overwriting the real failure or skip sentinel of an already-finished run with `SKIPPED - YOU CANCELLED IT` / `SKIPPED - YOU STARTED A GAME`!

---

### 3. The words (`02` § The strings and § The why table; F-08 to F-15)

**R-12** — *narrowed*
`GuiCloudTransfer.cpp:351-361, 745, 769, 805-808`, `CloudText.cpp:410-466, 1386-1387`, `ThreadedCloudSync.cpp:92, 536, 781`
Against the rules quoted in `03` § 3.2 and `Context 3`, F-08 (`GuiCloudTransfer.cpp:357-358`), F-10 (`:745` `DID NOT FINISH` vs D-UI-031's contractions; `:769` `CAME DOWN`), and F-11 (`CloudText.cpp:414-466`) are genuine violations. F-09 (`GuiCloudTransfer.cpp:807-808`, `NOTHING NEW TO BRING DOWN` / `NOTHING NEW TO SEND UP`) is a genuine vocabulary violation in source, but `02`'s claim that the 640x480 panel displays it in English is unproved (`CANNOT` frame in `02` § The guest cycle, and the 36/43-char primary strings at `:805-806` are shorter than the 48-char candidate that fits `mTextFont` at `:1021`; A-13). F-15 (`02` § The why table) is narrowed because the eight exit-75 strings span three different locks (cloud sync, cloud check, `backuptool`) and four distinct UI roles (outcome line, bare `why`, modal dialog sentence, and folder-refusal recovery instruction; A-16).

**R-13** — *confirmed*
`GuiCloudTransfer.cpp:252-258, 351-371, 909-913`, `GuiCloudTransfer.h:162`
F-08's dialog is unconditionally reached when cancelling a match. While `!job.mFinished`, pressing `BUTTON_BACK` checks `cancellable()` (`GuiCloudTransfer.cpp:254`, `GuiCloudTransfer.h:162`), which is `true` for a match, and calls `askCancel()` (`GuiCloudTransfer.cpp:351-361`). Because `askCancel()` only checks `TransferKind::Scan` (`:355`) and `TransferKind::Create` (`:356`), `TransferKind::Match` falls into the default arm (`:357-358`) and promises `THE NEXT BACKUP OR RESTORE FINISHES WHAT THIS ONE DIDN'T.`, even though `retries()` (`:368-371`) and `matchRecovery()` (`:913`) refuse a repeat match without checking again.

**R-14** — *confirmed*
`GuiMenu.cpp:5006, 5040-5046, 5082`, `CloudText.cpp:414-475, 571-580`, `CloudTransferJob.cpp:280-289, 302-322`, `GuiCloudTransfer.cpp:813-856`
`THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` (`D-UI-117`, `Context 3`) reaches line 4 (`mDetail`) of the settings restore page in English when `backuptool restore` emits it as `>>> why` and exits non-zero (the `backuptool` script body is `outside the packet`). `GuiMenu.cpp:5043-5045` runs `/usr/bin/backuptool restore` inside the `SETTINGS` tier without redirecting its stdout, so `CloudTransferJob.cpp:280-289, 302-322` records the `why` in `mFailed` under `SETTINGS`. When `GuiCloudTransfer.cpp:845` formats line 4 on the failed done page, `CloudText::localizedWhy` (`CloudText.cpp:469-475`) does not find the sentence in `whySentences()` (`:423-466`) and returns the raw English string.

**R-15** — *refuted*
`ThreadedCloudSync.cpp:80-129`, `CloudText.cpp:440, 443`, `CloudTextTests.cpp:659-664`
The first reader's claim in `02` § The why table that `"The code and the scripts' why_for agree on every group"` in the fallback map is wrong. As shown by `02`'s own Why Table (rows 17 and 20) and `CloudTextTests.cpp:660, 663`, the scripts' `why_for` maps rclone exit code `6` to `"SOME FILES DIDN'T FINISH"` and code `10` (on automatic runs) to `"THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME"`, whereas `ThreadedCloudSync::whyForCode` (`ThreadedCloudSync.cpp:80-96`) and `tokenForCode` (`:103-117`) omit both `6` and `10`, collapsing them into `default:` (`"SOMETHING WENT WRONG"` / `"unknown"`; A-15). Conversely, `02`'s fallback table omits the three sentinel cases (`CloudExit::NoNetwork`, `LockHeld`, `NoFolder`) that `ThreadedCloudSync::whyForCode` does handle at `ThreadedCloudSync.cpp:91-93`.

---

### 4. The tests (`02` § The tests; F-05, F-12)

**R-16** — *confirmed*
`CloudTextTests.cpp:632-729`, `CloudText.cpp:414-466, 571-580`
Two tests in `CloudTextTests.cpp` claim more than they check, and `AtomicFileTests.cpp:792` (`outside the packet`, described in `02` § The lifetimes) only greps source text for `.detach()`. First, `CloudTextTests.cpp:632-720` claims `"every protocol shape an emitter prints classifies to a known kind"`, but only tests a static array `shapes[]` (`:638-703`) and even omits **4 of the 38 rows** in `CloudText::whySentences()` (`CloudText.cpp:425`, `:429`, `:430`, and `:460`). Second, `CloudTextTests.cpp:722-729` claims `"each why's two spellings agree, so its translation is found"`, but because `_()` is an identity macro in the unit-test build (`:725-726`) and the test checks `whySentences()` directly without passing `sentence.first` through `classifyProtocolLine` (`CloudText.cpp:571-580`) or `parseLastRun`, it failed to catch that `CloudText.cpp:425` (`"CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS."`) has a trailing period that `classifyProtocolLine` (`:577-578`) strips!

**R-17** — *confirmed*
`CloudText.cpp:419-422`, `CloudTextTests.cpp:632-721`
The comment at `CloudText.cpp:419-422` is false: `CloudTextTests.cpp:632-721` does not read any script file and cannot fail when a script adds or changes a `>>> why` line unless a developer manually edits `shapes[]`. Moreover, because `shapes[]` at `CloudTextTests.cpp:640-680` has only 34 `ProtocolKind::Why` entries against `whySentences()`'s 38 rows (`CloudText.cpp:424-465`), it does not even guard all rows already present in `CloudText.cpp`.

**R-18** — *narrowed*
`CloudTransferJob.cpp:529-555, 654-677`, `GuiCloudTransfer.cpp:56, 635-689, 913-915, 936-939, 985-1035`, `ThreadedCloudSync.cpp:446-458, 716-758, 834-863, 930-949`
Beyond the two traps named in F-05 (`CloudTransferJob.cpp:529-555`'s `%3d` colon split at `100%` and `:654-677`'s glued `"Transferred:"` character loop and 1,024-byte cap), several other traps in these files have no unit tests:
1. `GuiCloudTransfer::prettyRclone`'s 80-column torn-field dropper (`GuiCloudTransfer.cpp:646-668`) and its 4-byte UTF-8 `" · "` separator check before `LEFT` (`:678-687`; A-18);
2. `TextComponent`'s `setSize(w, 0)` wrapping trap (`GuiCloudTransfer.cpp:74`) on rows that are updated *without* `fitOneLine`: `mTitle` (`:56`), running `mCounter` (`:936-939`), most running `mActivity` branches (`:985-1035` except `:1023`), `mElapsed` (`:901, 1055`), and done `mFooter` (`:913-915`; A-40);
3. Protocol normalization round-tripping (`isKnownWhy(classifyProtocolLine(">>> why " + s.first).text)`) and mid-line `>>> ` gluing after an unterminated rclone `" * file"` line (A-35, A-36);
4. `ThreadedCloudSync::cancelForLaunch` racing with `pclose` completion (`ThreadedCloudSync.cpp:446-720`), late `>>> pid` arrival (`:845-856`), or post-linger callbacks (`:717-756`), and `writeStamp` failure handling (`:930-949`; A-19).

---

### 5. Findings F-01 to F-19 (and F-20) and proposed bugs B1 to B4

**R-19 (F-01)** — *narrowed*
`CloudTransferJob.cpp:153-162, 272-279`, `ThreadedCloudSync.cpp:254-256, 845-850`, `CloudText.cpp:561-565`
Confirmed that both readers assign `mPid = protocol.number` on every `>>> pid` line (`CloudTransferJob.cpp:275`, `ThreadedCloudSync.cpp:255`). Narrowed because `CloudTransferJob::deliverStop` only sends a given signal once (`mSignalSent.exchange(sig) == sig` at `:159`), `ThreadedCloudSync::cancelForLaunch` only re-reads `sync->mPid` while its local `pid <= 0` (`:845`), `kill(-1, ...)` signals all processes the caller has permission to signal, and a malformed `>>> pid` line (`atoi` -> `0` at `CloudText.cpp:564`) overwrites a valid `mPid` with `0` and disarms future stops.

**R-20 (F-02 / B1)** — *narrowed*
`ThreadedCloudSync.cpp:206-207`, `CloudTransferJob.cpp:636-637`
Confirmed that `ThreadedCloudSync.cpp:206-207` lacks `trap '' PIPE`, whereas `CloudTransferJob.cpp:636-637` includes it. Narrowed because `CloudTransferJob.cpp:637` places `echo ">>> pid $$"` before `{ trap '' PIPE; ... ; }`, leaving the initial echo unprotected too (A-3), and whether a script dies before stamping depends on the script writing to the pipe before its stamp (`outside the packet`). For **B1**, **Low** severity is right; the proposed fix should place `trap '' PIPE;` *before* `echo ">>> pid $$"` in a shared wrapper helper; and `Already written:` should note that when an earlier sync died on `SIGPIPE` after moving some files, the device holds stale stamps from the prior run alongside updated files on `/storage` or the cloud (though the next run overwrites the stamps, so no migration is needed).

**R-21 (F-03)** — *confirmed*
`CloudTransferJob.cpp:399-403`, `ThreadedCloudSync.cpp:330-332`
Confirmed: both `default:` arms drop `ProtocolKind::Unknown` silently without logging (`CloudTransferJob.cpp:399-403`, `ThreadedCloudSync.cpp:330-332`), and the card's `default:` also resets `mWaitingForNetwork = false` (`:331`).

**R-22 (F-04)** — *narrowed*
`ThreadedCloudSync.cpp:211-212`, `CloudTransferJob.cpp:654-677`
Confirmed that `ThreadedCloudSync.cpp:211-212` reads 512-byte chunks with `fgets` while `CloudTransferJob.cpp:660` caps lines at 1,024 bytes. Narrowed because a split in `fgets` right before `>>> ` *can* make the second half a protocol line (contrary to `02`), and `CloudTransferJob.cpp:660`'s 1,024-byte cap silently discards characters past byte 1,024, breaking both long payloads and the glued `"Transferred:"` check at `:664-665` (A-4).

**R-23 (F-05)** — *narrowed*
`CloudTransferJob.cpp:529-555, 654-677`, `GuiCloudTransfer.cpp:635-689`, `CloudTextTests.cpp:859-945`
Confirmed that the `%3d` colon separator (`CloudTransferJob.cpp:529-555`) and the glued `"Transferred:"` character splitter (`:654-677`) have no unit tests. Narrowed because `GuiCloudTransfer::prettyRclone`'s 80-column torn-field dropper (`GuiCloudTransfer.cpp:646-668`) is also untested (`CloudTextTests.cpp:866-867` only tests `CloudText::parseBytes`; A-18).

**R-24 (F-06 / B2)** — *confirmed*
`ThreadedCloudSync.cpp:878-881, 910-927, 930-949`, `GuiMenu.cpp:5066`
Confirmed: `ThreadedCloudSync::writeStamp` (`:930-949`) renames `tmp` over `path` without checking `Utils::FileSystem::writeAllText`, and `restampStoppedParts` (`:914-915, 924-925`) logs success unconditionally. For **B2**, **Low** severity is appropriate; the fix using `Utils::AtomicFile::writeText` (already used at `GuiMenu.cpp:5066`) and returning `bool` from `writeStamp` is sound; and `Already written:` is right that truncated stamps on disk already parse as `ran = false` in `CloudText::parseLastRun` (`CloudText.h:96-98`) and will be replaced on the next run.

**R-25 (F-07)** — *narrowed*
`ThreadedCloudSync.cpp:834-863`, `FileData.cpp:993-1007, 1017-1018`
Confirmed that `cancelForLaunch` spins up to 2 s on the UI thread when called from `FileData.cpp:1001`. Narrowed on two points: `04` § Q5 wrongly compares the 2 s spin against D-CLOUD-119's 3 s exit-sync budget instead of D-CLOUD-109 / D-CLOUD-129's requirement of a visible spinner (`Context 3`), and this should be disposed as a Low defect rather than merely a design note (A-11, A-42).

**R-26 (F-08 / B3)** — *confirmed*
`GuiCloudTransfer.cpp:351-371, 881-882, 909-913`
Confirmed: `GuiCloudTransfer::askCancel` (`:351-361`) gives `TransferKind::Match` the backup/restore cancel prompt (`:357-358`), promising that the next backup or restore finishes it when in fact a second match is refused without a new check (`:363-371, 909-913`). For **B3**, **Low** severity and the proposed fourth arm in `askCancel()` are right; `Already written:` should note that if a player confirmed the cancel during a match, files already removed on `/storage` stay removed and the match preview plan was consumed (`:364-365, 881-882`), though nothing in persistent config or stamps needs migration (A-31).

**R-27 (F-09)** — *narrowed*
`GuiCloudTransfer.cpp:805-808`
Confirmed that `NOTHING NEW TO BRING DOWN` and `NOTHING NEW TO SEND UP` (`GuiCloudTransfer.cpp:808`) paraphrase the canonical verbs `restore` and `back up`. Narrowed because `02` had no 640x480 frame proving the fallback is reached in English on 640x480 (`02` § The guest cycle: `CANNOT`), though the non-canonical strings in source should be fixed regardless (A-13, A-42).

**R-28 (F-10)** — *confirmed*
`GuiCloudTransfer.cpp:745, 769`
Confirmed: `ITEM DID NOT FINISH` / `ITEMS DID NOT FINISH` (`GuiCloudTransfer.cpp:745`) uses formal `DID NOT` against D-UI-031 (`Context 3`), and `CAME DOWN TOO.` (`:769`) paraphrases `restore`.

**R-29 (F-11 / B4)** — *confirmed*
`CloudText.cpp:414-475, 577-578`, `GuiMenu.cpp:5043-5045`, `GuiCloudTransfer.cpp:845`, `CloudTextTests.cpp:717-729`
Confirmed that `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` (`D-UI-117`) and `ANOTHER CLOUD SYNC IS RUNNING` are absent from `CloudText::whySentences()` (`CloudText.cpp:423-466`), and extended by A-36: `CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.` (`CloudText.cpp:425`) carries a trailing period in `whySentences()` that `classifyProtocolLine` (`:577-578`) and `parseLastRun` strip, so it also fails `localizedWhy` (`:469-475`) and stays in English. For **B4**, **Low** severity and `Already written:` are right, but the proposed unit-test proof in `04` § Q3 (`"A localizedWhy case for each pair, failing before the pairs are added"`) is **wrong**: because `_()` returns English in the gettext-free unit-test binary (`CloudTextTests.cpp:725-726`), `localizedWhy(s)` returns `s` whether or not `s` is in `whySentences()`! The test must assert `isKnownWhy(classifyProtocolLine(">>> why " + s).text)` for every row of `whySentences()` and `shapes[]` (A-32).

**R-30 (F-12)** — *confirmed*
`CloudText.cpp:419-422`, `CloudTextTests.cpp:632-721`
Confirmed: `CloudText.cpp:419-422` claims `CloudTextTests.cpp` fails on a script `why` not in `whySentences()`, whereas `CloudTextTests.cpp:632-721` checks a hand-typed array and even omits four rows of `whySentences()` (`CloudText.cpp:425, 429, 430, 460`).

**R-31 (F-13)** — *narrowed*
`ThreadedCloudSync.h:70, 93-99, 126-130`, `ThreadedCloudSync.cpp:73, 460`, `CloudText.h:9-18, 78-82, 164-170`, `CloudText.cpp:298`, `CloudTransferJob.cpp:399-403`, `GuiCloudTransfer.h:156-157`
Confirmed for every cited line present in the packet: `ThreadedCloudSync.h:70, 93-99, 126-130`, `ThreadedCloudSync.cpp:73, 460`, `CloudText.h:9-18, 78-82`, `CloudText.cpp:298`, `CloudTransferJob.cpp:399-403`, and `GuiCloudTransfer.h:156-157`. Narrowed because `ThreadedCloudSync.h:158-159` and the body of `CloudText::shortenWhy` in `CloudText.cpp` (needed to verify `CloudText.h:164-170`) are `outside the packet`.

**R-32 (F-14)** — *narrowed*
`ThreadedCloudSync.cpp:84, 86`, `GuiCloudTransfer.cpp:432, 463`
The rule file `.claude/rules/es-player-text.md` itself is `outside the packet` (only quoted in `02` and `03`). Against the code (`ThreadedCloudSync.cpp:84, 86`) and `02`'s Why Table, the drift also includes codes `6` and `10` being absent from `ThreadedCloudSync::whyForCode` (A-15).

**R-33 (F-15)** — *narrowed*
`CloudText.cpp:410, 411, 432, 462, 1387`, `ThreadedCloudSync.cpp:92, 536, 781`
Confirmed that eight exit-75 strings exist across the code and table, but narrowed because they are not eight wordings for the same message: they cover three distinct locks (sync, scan, settings `backuptool`) and four distinct UI contexts (outcome line, bare `why`, modal dialog, and folder-check recovery instruction; A-16).

**R-34 (F-16)** — *confirmed*
`CloudTransferJob.cpp:234-236, 387-389`, `GuiCloudTransfer.cpp:190-198, 221, 302, 336-340, 895-896, 1027-1032`, `GuiCloudTransfer.h:76-100, 162`, `CloudText.cpp:429, 1104-1108`, `GuiMenu.cpp:5083-5097`
Confirmed within the packet that `doing` keywords `copy`/`verify`/`remove`, unit label `DISCARDED SAVES`, why row `YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED`, `setFailedNote`, `setDismissedAction`, and `setCompletedAction`'s `cancellable` parameter are leftovers of the retired folder move (#353 / D-CLOUD-175) and folder step (#363) (whole-tree caller absence is `outside the packet`, P13/P14).

**R-35 (F-17)** — *narrowed*
`CloudText.h:187-189, 529-531`, `CloudText.cpp:469-483`, `CloudTextTests.cpp:718`
`CloudText.h:468-469` (`nextTime`) and whole-tree caller searches are `outside the packet` (P12). Narrowed because `isKnownWhy` (`CloudText.h:189`, `CloudText.cpp:477-483`) and `isKnownUnitLabel` (`CloudText.h:531`) are test-oracle entry points used by `CloudTextTests.cpp:718` and belong in the header for unit testing, not under dead ends (A-27).

**R-36 (F-18)** — *narrowed*
`CloudTransferJob.cpp:267-406, 636-682`, `ThreadedCloudSync.cpp:206-335`
Confirmed that the two protocol readers duplicate wrapper construction, pipe reading, and `>>> pid` handling. Narrowed because a shared reader must fix—not copy—`CloudTransferJob.cpp:660`'s silent 1,024-byte truncation and must preserve intentional differences between the third-tier card and fourth-tier page (A-28).

**R-37 (F-19)** — *confirmed*
`CloudTransferJob.cpp:20, 97-98, 118-119`
Confirmed from `CloudTransferJob::testPauseInStop` (`:20, 97-98, 118-119`) and `02` § Context read that the job's stop-race tests live in `tests/app-unit/JobsTests.cpp` (`outside the packet`) rather than `es-app/tests/unit/`.

**R-38 (F-20)** — *confirmed*
`CloudText.cpp:624-637`, `CloudTransferJob.cpp:338-351`, `GuiCloudTransfer.cpp:762-767`
Confirmed: `CloudText::classifyProtocolLine` (`CloudText.cpp:624-637`) and `CloudTransferJob::handleLine` (`CloudTransferJob.cpp:343-349`) keep per-system entries of `>>> removed` even when `sys.files == "0"`, causing `GuiCloudTransfer.cpp:765-767` to display `"SNES 0 FILES"` beside systems that actually had files removed.

---

### 6. What the first reader missed (including assessment of the first seat's new items)

**R-39** — *new*
`ThreadedCloudSync.cpp:446-458, 494, 510, 566, 634-635, 716-758, 796-863`, `FileData.cpp:993-1007`
Both the first reader and the first seat missed what happens after `pclose(pipe)` (`ThreadedCloudSync.cpp:446`) and across the 1.5 s / 5 s linger sleep (`:717-756`):
1. `pclose(pipe)` reaps the child at `:446` and `cancelled` is latched into a local `bool` at `:456`, but `mInstance` remains set until `:717-720` (across stamp I/O and `OfflineAchievements::pendingAwards()` at `:510-707`). If `cancelForLaunch` runs between `:456` and `:717`, it sends `SIGTERM`/`SIGKILL` (`:817, 859`) to an **already-reaped PID**, sets `sync->mCancelled = true` (`:813`) after `run()` already latched `cancelled = false`, and returns `true` (`:841`) to let the game launch while `run()` proceeds with `cancelled == false` and `completed == true`!
2. Even when `cancelForLaunch` was never called, `run()` clears `mInstance = nullptr` at `:717-720` (making `ThreadedCloudSync::isRunning()` false) *before* sleeping 1.5 s or 5 s (`:731`), and then calls `CloudOffer::present(mWindow, mOffer, mOfferArgs)` (`:741`) and `ProxyCards::afterSync(mWindow)` (`:755`) *after* the sleep—so if a player launches a game during that 1.5 s / 5 s linger (`FileData.cpp:993`), the offer dialog or achievements card is pushed onto `mWindow` over the game launch!

**R-40** — *new*
`ThreadedCloudSync.cpp:238-242, 481-499`, `GuiCloudTransfer.cpp:435-451`, `GuiMenu.cpp:5006, 6140`
Both the first reader and the first seat (which in A-38 only noted `rc=9` in `GuiMenu.cpp:5006`) missed that **both** `ThreadedCloudSync::run` (`ThreadedCloudSync.cpp:494-495`) and `GuiCloudTransfer::outcome` (`GuiCloudTransfer.cpp:435, 451`) compute `completed` (`ret == 0 || ret == 9` / `job.mExit == 0 || job.mExit == 9`) *without* checking `badTiers.empty()` / `!anyBad`, and then gate `gaps` / `o.partial` on `!completed` (`!o.completed`). This directly contradicts `ThreadedCloudSync.cpp:238-242` (`"so a run where one part finished and another did not is reported as a failure with that part's why, rather than as the last part's code"`): whenever the final command exits `0` or `9`, any failed tier in `badTiers` / `anyBad` is ignored and the run is reported as `COMPLETED`! Furthermore, `ThreadedCloudSync.cpp:482-483` discards `t.second` (the failing tier's exit code) when building `badTiers`, so if a failing tier emitted no `>>> why`, `why` at `:498` calls `whyForCode(ret)` on the last command's code instead of the failing tier's code.

**R-41** — *new*
`CloudTransferJob.cpp:87-127, 153-162, 679-712`
Both the first reader and the first seat (A-9) missed a race in `CloudTransferJob::run`: `pclose(pipe)` at `CloudTransferJob.cpp:679` reaps the child process `mPid` *before* `mMutex` is locked at `:684` and before `mFinished` is set at `:727`. If `stopForLaunch` or `stopByPlayer` runs in that window: (a) `deliverStop()` (`:161`) signals an already-reaped PID, and (b) if the child had already exited with a non-zero failure or sentinel (`ret != 0 && ret != 9`), line 691 (`if ((mStoppedForGame || mStoppedByPlayer) && (ret == 0 || ret == 9))`) does not clear the stop flags, so `:701-704` overwrites the real failure or skip sentinel with `CloudExit::Stopped` (`SKIPPED - YOU CANCELLED IT` / `SKIPPED - YOU STARTED A GAME`).

**R-42** — *new*
`CloudTransferJob.cpp:717-723`, `GuiCloudTransfer.cpp:414-419, 453-467, 813-856`
Both the first reader and the first seat missed a mismatch between `GuiCloudTransfer::outcome` (`GuiCloudTransfer.cpp:453-467`) and `CloudTransferJob::run` (`CloudTransferJob.cpp:717-723`) when a non-tiered run moves files/bytes (`progressed == true`, `:453`) and then exits `69` (`CloudExit::NoNetwork`, e.g., losing the connection mid-transfer where the script writes the offline why to its stamp rather than `>>> why`) or `75` (`CloudExit::LockHeld`):
- `GuiCloudTransfer.cpp:454, 467` sets `o.skipped = false` (because `progressed` is true, per `:414-419`) and sets line 1 (`o.word`) to `COULDN'T FINISH`.
- However, `CloudTransferJob.cpp:721` (`if (mFailed.empty() && ret != CloudExit::LockHeld && ret != CloudExit::NoNetwork)`) unconditionally excludes `NoNetwork` and `LockHeld` from `mFailed` (and never calls `CloudText::offlinePartWayWhy` as `ThreadedCloudSync.cpp:510` does), leaving `mFailed` empty and line 4 (`mDetail`) **blank** under `COULDN'T FINISH`!
- Conversely, `CloudTransferJob.cpp:721` does not exclude `CloudExit::NoFolder` (`78`), even though `GuiCloudTransfer.cpp:455` treats `NoFolder` as a skip sentinel alongside `LockHeld` and `NoNetwork`.

**R-43** — *new*
`CloudTransferJob.cpp:244, 286, 315-321, 717-724`, `CloudTransferJob.h`
Both the first reader and the first seat missed that `CloudTransferJob::mWhy` (`CloudTransferJob.cpp:286`) is dead state: it is written on every `>>> why` line (`:286`) and never read anywhere in `CloudTransferJob.cpp` or `GuiCloudTransfer.cpp`, falsifying the comment at `:244` (`"The last one is the run's why for a command with no tiers"`). Worse, for a command with no tiers, `CloudTransferJob.cpp:719-720` copies every entry of `mPendingWhys` into `mFailed` *without* the per-label deduplication that `case Tier:` performs at `:315-321` (`"The last why for an item wins"`), and if an earlier tier failed (`!mFailed.empty()`) before a final part exited without printing `>>> tier`, `:717` (`if (... && mFailed.empty() && ...)`) drops the final part's `mPendingWhys` altogether!

**R-44** — *new*
`CloudText.cpp:424-466, 577-578`, `CloudTextTests.cpp:638-680, 717-720`
While the first seat (A-36) caught that `CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.` (`CloudText.cpp:425`) has a trailing period that `classifyProtocolLine` (`:577-578`) strips, both the first reader and the first seat missed *why* `CloudTextTests.cpp:717-718` (`if (p.kind == ProtocolKind::Why) CHECK(isKnownWhy(p.text));`) did not fail on it: `shapes[]` in `CloudTextTests.cpp:640-680` has only 34 `ProtocolKind::Why` entries and omits 4 of the 38 rows in `whySentences()` (`CloudText.cpp:425`, `:429`, `:430`, and `:460`).

**R-45** — *confirmed*
`ThreadedCloudSync.cpp:446-458, 716-720, 845-863`, `CloudText.cpp:425, 577-578`, `CloudTransferJob.cpp:287, 333-336`, `GuiMenu.cpp:5006, 5125, 6140`, `GuiCloudTransfer.cpp:56, 74, 435, 913-915, 936-939, 985-1035`
Regarding the remaining new items from the first seat (GPT-6 Astra):
- **A-33, A-34, A-36, A-37, A-38, A-39, A-40, A-41, A-42** are **confirmed** against the packet's lines (`ThreadedCloudSync.cpp:446-458, 845-863`; `CloudText.cpp:425, 577-578`; `CloudTransferJob.cpp:287, 333-336`; `GuiMenu.cpp:5006, 5125, 6140`; `GuiCloudTransfer.cpp:56, 74, 435, 913-915, 936-939, 985-1035`).
- In particular, **A-38** (`GuiMenu.cpp:5006` setting `rc=$_t` when `_t` is `9`, and `GuiMenu.cpp:6140` exiting `9` after restore when rclone returns `9`) is a real logic bug in the shell composers whenever rclone exits `9` (whether any script passes `--error-on-no-transfer` is `outside the packet`, though `GuiCloudTransfer.cpp:289, 302, 435` and `ThreadedCloudSync.cpp:483, 492` explicitly treat `9` as a normal completion code).
- **A-39** (`GuiMenu.cpp:5125` redirecting `/usr/bin/backuptool backup >/dev/null 2>&1`) makes all six `backuptool` backup `>>> why` rows in `CloudText.cpp:451-453, 463-465` unreachable from that caller because `backuptool`'s stdout is discarded before reaching `CloudTransferJob`.