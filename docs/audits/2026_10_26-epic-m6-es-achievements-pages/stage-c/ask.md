# Second opinion (Phase 4.6), M6 T20: EmulationStation's RetroAchievements and offline pages, in pixelelated's EmulationStation fork

You are one of two independent reviewers for a read-only renovation audit of 25 files, read under a **security and new-functionality lens**. They total 7,485 lines at the EmulationStation commit `16dbac5211` (the distribution pins that commit).

- **The account client:** `RetroAchievements.{h,cpp}`. It signs in, and calls the web API and the local offline proxy.
- **The pages:** `GuiRetroAchievementsSettings`, `GuiRetroAchievements` (the account) and `GuiGameAchievements` (one game).
- **The offline half,** which drives a control script, `raofflineproxy-ctl`, and reads its files: `OfflineAchievements.{h,cpp}`, `OfflineScanJob.{h,cpp}`, and the scan page `GuiOfflineScan.{h,cpp}`.
- **The game hasher:** `ThreadedHasher.{h,cpp}`.
- **Nine files of the vendored libcheevos:** a bounded GameCube RVZ reader (`rvz_hash.cpp`), its notices, and five small edits to imported files.

**What ships.** The product is an immutable handheld OS; a person updates it in place and keeps `/storage`.

- EmulationStation is its interface, at 640x480 on the smallest panel.
- RetroAchievements is a third-party service the player signs in to. The "offline proxy" is a local service on `127.0.0.1:8080` that holds awards earned offline and sends them later; `raofflineproxy-ctl` is its shell control script, run as root.
- The rules the code answers to are named in `03` § 3.2.

**What you get.**

- The first reader is another lab's model. You get its `02-forward-audit.md`, `03-retrospective.md` and `04-analysis.md` whole.
- Then context: the order's entry, the brief's questions, the register rows the code cites, and the proxy audit's (T19's) list of what it hands this slice.
- Then the host fixtures' outputs and three guest records.
- Then four files whole and line-numbered: `OfflineAchievements.cpp`, `OfflineScanJob.cpp`, `GuiOfflineScan.cpp`, `ThreadedHasher.cpp`. Then `rvz_hash.cpp` whole, and the library's diff against its import.
- Then **line-numbered excerpts** covering every line the analyses cite, with eight lines of context:
  - `RetroAchievements.cpp`, `GuiRetroAchievementsSettings.cpp`, the two account pages, `ApiSystem.cpp`, `HttpReq.{h,cpp}`, `CloudText.{h,cpp}`, `ProxyCards.cpp`, `FileSystemUtil.cpp`;
  - the control script at the distribution commit `8ebaf8daad`.
- **When a claim needs lines outside the packet, say `outside the packet` and do not guess.**

**Masking.** Every section was passed through a mask that replaces a value after `key=`, `key:`, `token=`, `user=`, `pass...=` or `psk=` with `***`; a `***` is the mask, not the code. The packet was scanned for credential shapes before it left, and no hit was a value.

**Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong. Its line numbers are the pin's.

**What was run.** Nothing can be run for you.

- The unit tests were built on the host and pass at the pin.
- Six fixtures were built from the pin's own lines; their outputs are in the packet.
- A guest window ran on an image whose EmulationStation is a **later composition over the pin**: its offline settings page differs from the pin's. So a page frame there is not the pin's page, and the first reader says which code path each guest proof exercised.

Answer these first, in this order:

1. **Credentials (`02` § The credentials' paths; Q1; L-01 to L-04).**
   - Is every sink of the username, password, token and web API key listed, at its line?
   - Is the password in a query string over an unverified peer, with redirects followed to `http`, a defect of this slice's code or only #1154's (`HttpReq.cpp`)?
   - Is the sign-in on the interface thread with no total and no stall bound (L-02) reached as `02` says?
   - What reaches the screen in a tool's words?
2. **The contract with the control script (`02` § The contract; Q2; L-05 to L-11).**
   - Are both readers' behaviours right? The 1,024-byte reader, the dropped last line, `WEXITSTATUS` without `WIFEXITED`, `>>> pid` from any line.
   - Is the guest's finding on `/bin/sh` (bash forks for a redirected command) enough to downgrade L-06?
   - Is each verb's row right against the ctl's lines?
   - Are L-07 (`unknown` read as 0) and L-09 (`disable`'s exit 1 with the toggle already off) real at the integration seam as described?
3. **Lifetimes and threads (§ The hasher, § The reader; L-19 to L-23).**
   - Is L-21 real? Can `ThreadedHasher::start` (`:383-392`) read `hasher->…` or store `mInstance` after the last `run()` thread has executed `delete this` (`:258-265`)? Is the silent lookups-alone run the short-queue case it says?
   - Does anything else hold a page, a job or a hasher across its own deletion?
   - Is the scan page's job ownership sound against CANCEL and TRY AGAIN?
4. **Files and pages (Q3, Q4; L-12 to L-18).**
   - Are the `exists(` cache readings right? Is the under-three-bytes read (L-13) right?
   - Is each dialog's button order safe, and is each row's store and save as `02` § The pages says?
   - Is HARDCORE MODE's second writer (L-14) a defect or the player's right?
5. **The library (Q6, Q7; L-24, L-25).**
   - Is each of the five edits bounded and correct (`hash_disc.c`, `md5.c`, `cheevos.cpp`, `cheevos.h`, `CMakeLists.txt`)?
   - Is `rvz_hash.cpp` safe against a hostile RVZ: integer overflow, a size taken from the file before it is bounded, a decompression bomb, a read past a buffer?
   - Is the padding argument (the bit-selection commutes with XOR) right?

Then:

6. **Refute or confirm each lead L-01 to L-25** in `02`: *confirmed*, *narrowed* (say how), or *refuted* (with the line). For the High and Medium ones in `04` § Risk assessment, also judge the severity, the fix a stream would make, and its `Already written:` line: what the code before a fix has already left on devices and in their clouds.
7. **What the first reader missed:**
   - a credential reaching a log, a command line, a file or the screen;
   - a reader that turns a failure into a success or a number;
   - a pointer used after its owner goes;
   - a string that promises what the code does not do;
   - a file read cached when another process writes it;
   - a bound missing on the interface thread.

**Output:**

- Numbered items `{PREFIX}-1`, `{PREFIX}-2`, ..., grouped under the seven headings above.
- Each item gets one line saying *confirmed / narrowed / refuted / new*, then the `file:line` evidence, then two to five sentences.
- Do not restate the packet, and do not reproduce long code.
- Keep the whole reply under about 8,000 words.
