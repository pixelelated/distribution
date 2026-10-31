# Independent review: M6 T35, EmulationStation's window, input and the rest of es-core (#682)

You are the independent reviewer for one slice of a code audit. You come from another lab than the first reader (Claude Opus 5.5). The subject is **the 96 paths of `es-core/**` outside the components** at the pin `16dbac5211eea7e70db7394372033be2be7df829`: 22,575 lines, 13 added or modified by the fork and 83 carried from ROCKNIX. The packet below carries:
- the 13 fork-added and fork-modified files whole, line-numbered at the pin;
- of the 83 upstream-carried files, only the line ranges the first reader cites, each with 8 lines of context, line-numbered;
- the first reader's `02`, `03`, `04` and `05` whole;
- the brief's § 4, the seven questions.

Every excerpt is hashed in `packet-manifest.json`. Neighbouring files (`utils/FileSystemUtil.cpp`, `utils/Platform.cpp`, the components, es-app's `main.cpp`) are not in the packet; the first reader cites their lines. Judge those claims as citations, or say you cannot tell.

**If you need other ranges to judge a claim, name them by file and line range at the end of your reply, under `## Sections I need`.** No second packet will be sent in this cycle; name them so the record shows what was missing.

**Answer these first, each with the lines you read:**
1. **PL-01, the watchers' lock** (`watchers/WatchersManager.cpp:159-203`, `:64-104`, `:126-157`). Is `mWatchersLock` held across every `check()`, and do the entry points named wait for it? Is the order list-then-observers, and can an observer's callback re-enter a locked entry point (a deadlock)?
2. **PL-02, the toast queue's order** (`Window.cpp:324-351`, `:1152-1175`). Does the queue drain newest first, and does the fix the first reader proposes (pop the front, reverse the re-queue loop) keep a toast returned under a new card in its place?
3. **PL-03, the script quoting** (`Scripting.cpp:88-149`). Which characters in an argument reach the shell unquoted at the pin? Is single-quoting every argument (with `'` escaped) sufficient for `system()` and `/bin/sh -c`?
4. **PL-04, the cache after `save_file`** (`InputManager.cpp:889-905`, `:1179-1284`). Is the second-pad overwrite reachable as described, given the cited cache lines?
5. **PL-05 and PL-06, the screensaver and the teardown** (`Window.cpp:777-792`, `:1091-1138`, `:188-207`, `:49-63`, `:1236-1260`). Is the window's half of #1305 as stated? Can a card alive at `deinit` be drawn again at the next `init()`?

**Then grade every punch item PL-01 to PL-24 in `05`.** One line each:
- `confirmed`, `confirmed with narrowing`, `refuted`, or `cannot tell from the packet`;
- why, and the line;
- the severity, if you would change it.

**Add any defect the first reader missed, as G-n**, with its lines. Be concrete and cite lines. Do not restate the packet.

---
