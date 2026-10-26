# Second opinion (Phase 4.6), M6 T21: EmulationStation's state primitives and its bridge to the OS, in pixelelated's EmulationStation fork

You are one of two independent reviewers for a read-only renovation audit of 14 files, read under a **security and state-preservation lens**. They total 9,249 lines at the EmulationStation commit `16dbac5211` (the distribution pins that commit).

- **The shell bridge:** `ApiSystem.{h,cpp}`. Four executors (`popen` or `system()`), and every page's command built from strings, some of them a player's.
- **The network client:** `HttpReq.{h,cpp}`. One process-wide `curl_multi` with no thread of its own.
- **The two stores and the fork's atomic writer:** `Settings.{h,cpp}` (`es_settings.cfg`, EmulationStation's own), `SystemConf.{h,cpp}` (`system.cfg`, the launch scripts' store), and `AtomicFileUtil.{h,cpp}` (temp-and-rename, a pid lock shared with the shell, the recovery ladder).
- **The Wi-Fi page** `GuiWifi.{h,cpp}`, and **the scraper's credentials** in `ScreenScraper.{h,cpp}`.

**What ships.** The product is an immutable handheld OS; a person updates it in place and keeps `/storage`.

- EmulationStation is its interface, at 640x480 on the smallest panel, run as root.
- The shell scripts that also write `system.cfg` (`001-functions`, `chksysconfig`, `wifictl`, `post-update`) are another slice's files, read here where they meet this code. Their lines are the distribution commit `8ebaf8daad`'s.
- The rules the code answers to are named in `03` § 3.2.

**What you get.**

- The first reader is another lab's model. You get its `02-forward-audit.md`, `03-retrospective.md` and `04-analysis.md` whole.
- Then context: the brief's questions, and the register rows the code cites.
- Then the host fixtures' outputs and the guest records.
- Then six files whole and line-numbered: `AtomicFileUtil.{h,cpp}`, `SystemConf.{h,cpp}`, `Settings.cpp` and `HttpReq.cpp`.
- Then **line-numbered excerpts** covering every line the analyses cite, with eight lines of context:
  - `ApiSystem.cpp`, `GuiWifi.cpp`, `ScreenScraper.cpp`, `HttpReq.h`, `Settings.h`, and the neighbours the analyses cite (`StringUtil.cpp`, `Scraper.cpp`, `FileSystemUtil.cpp`, `TextEditComponent.cpp`, `main.cpp`);
  - the shell writers at `8ebaf8daad`: `001-functions` and `wifictl`.
- **When a claim needs lines outside the packet, say `outside the packet` and do not guess.**

**Masking.** Every section was passed through a mask that replaces a value after `key=`, `key:`, `token=`, `user=`, `pass...=` or `psk=` with `***`; a `***` is the mask, not the code. The packet was scanned for credential shapes before it left; no hit was a value.

**Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong. Its line numbers are the pin's.

**What was run.** Nothing can be run for you.

- The unit tests were built on the host and pass at the pin.
- The fixtures ran the pin's own `SystemConf.cpp`, `AtomicFileUtil.cpp` and `StringUtil.cpp`, or lines lifted verbatim where a file needs curl or SDL. The shell writers ran at `8ebaf8daad`, unrewritten, in a sandbox. Their outputs are in the packet.
- A guest window ran on an image whose EmulationStation is a **later composition over the pin**, while its shell scripts are `8ebaf8daad`'s bytes. So a frame there is the image's, and the first reader says which code each guest proof exercised.

Answer these first, in this order:

1. **The commands (Q1; L-01, L-17, L-18, L-20).**
   - Is every double-quoted external string listed, and is L-01 reached as `02` says: the scraper's `getMD5` → `7zr` over a ROM's name, as root?
   - Is any bare join attacker-shaped after all: the Bluetooth MAC, the storage id, the bezel names from a network list?
   - Is anything blocking the interface thread with no bound that `04` § Q1 misses?
2. **The client (Q2; L-02 to L-07).**
   - Is L-02 (the header callback's read) real, and how far can it read?
   - Is L-03 (a download removes its target first) reached by default as `02` says?
   - Is the `file://` closure right: does a `file://` transfer really end with response code 0 and its bytes removed?
   - Is the `format` and `Content-Type` path closure right?
   - What does #1154's fix (verify by default, an explicit exception for media) break that the first reader does not say?
3. **The credentials (Q3; L-08, L-09, L-21).**
   - Is every sink of the Wi-Fi key, the scraper's pair and account, and the root password's default listed, at its line?
   - Is L-21 (0645 at rest, kept by every writer) right, and what else reads `system.cfg`'s mode?
4. **The writers and the readers (Q4, Q5; L-10 to L-16).**
   - Is L-10's chain real: the seed copied before the lock and the record, then recorded over it by the interface's load? Is there a path the first reader misses by which `system.cfg` is absent when a shell writer runs?
   - Is `SystemConf`'s save safe against every other writer of `system.cfg`: the shell under the same lock, `chksysconfig` with none, `post-update`'s `sed -i`?
   - Does `Settings` lose a change or a record anywhere: a save from a worker thread, a kill between the two writes, a load that refreshes the record from a file that parsed but is wrong?
   - Are `parseKeyValues`' drops (an empty value, a BOM, a carriage return) and `applyChanges`' rewrite safe for every key the shell writes?
5. **What a failure reads as (Q6; L-17, L-18, L-22).**
   - Is L-22 (`wifictl` exits 0 with no device, and the page says CONNECTED) reached as described, and is the same shape anywhere else?

Then:

6. **Refute or confirm each lead L-01 to L-22** in `02`: *confirmed*, *narrowed* (say how), or *refuted* (with the line). For the High and Medium ones in `04` § Risk assessment, also judge the severity, the fix a stream would make, and its `Already written:` line: what the code before a fix has already left on devices, and how the fix treats it.
7. **What the first reader missed:**
   - a credential reaching a log, a command line, a file or the screen;
   - a reader that turns a failure into a success or a number;
   - a writer that can lose the record;
   - a pointer used after its owner goes;
   - a string that promises what the code does not do;
   - a bound missing on the interface thread.

**Output:**

- Numbered items `{PREFIX}-1`, `{PREFIX}-2`, ..., grouped under the seven headings above.
- Each item gets one line saying *confirmed / narrowed / refuted / new*, then the `file:line` evidence, then two to five sentences.
- Do not restate the packet, and do not reproduce long code.
- Keep the whole reply under about 8,000 words.
