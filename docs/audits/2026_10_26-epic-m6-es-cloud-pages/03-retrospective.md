# Retrospective audit — M6.P2 T18, EmulationStation's cloud pages, cards and text (#665)

What the 30 files are measured against: the four ES rules, the principles (least surprise, player language, time to play), engineering-practices.md, and the register rows the code cites. Findings are `02`'s F-nn.

## 3.1 Architectural coherence

- **Four pairs, three jobs, one text library.**
  - `CloudText` is pure: no file, no window, no font. It is tested, as es-code-traps.md § Pure text has a home asks.
  - The card (`ThreadedCloudSync`) runs automatic and manual saves syncs on the third surface tier.
  - The job (`CloudTransferJob`) runs a long transfer apart from its page, and the page (`GuiCloudTransfer`) is the fourth tier, sat in since D-UI-078.
  - The split is the rules' own, and a reader can tell which surface is which from the class comments.
- **One parser, two readers** (`CloudText::classifyProtocolLine`, #145) holds. The two readers still differ in five ways, each a small seam (F-18):
  - the wrapper's `trap '' PIPE` (F-02);
  - the read loop: `fgets` 512 against a character loop with a 1,024 cap (F-04);
  - what each drops (the card drops `unit` and `removed`);
  - how each takes a pid (both from every line, F-01);
  - how the launch waits for each: the card in a spin on the interface thread, the job behind a spinner (F-07).
- **The retired folder move left its seams in the page** (F-16): three `doing` words and their strings, a label, two setters with no caller, a parameter never passed, and comments describing the move as present. D-CLOUD-175 (#508) retired the flow; the page kept the hooks it was built with. That is register-check's P-01 shape (a reversal leaves its old words behind), applied to code.
- **The text library holds more than cloud text.** The offline proxy's stamps (`parseScanStamp`, `parseRunningProgress`, `parseFlushStamp`, `scanWhy`), the folder refusals, and the settings archive's name share `CloudText.cpp`'s 1,409 lines. They have their tests beside them. A split by subject is a Q1 proposal, not a defect.

## 3.2 Project conformance

| Rule | Held | Where it does not |
| --- | --- | --- |
| es-native-ui.md, the four surface tiers | the card is third tier (0.9W, top, ends when the work does, then lingers); the page is fourth (owns the screen until dismissed; CANCEL the one way out) | -- |
| es-native-ui.md, "one floating surface at a time" | the card is created through `Window`'s queue (`createAsyncNotificationComponent`) | -- |
| es-native-ui.md, "a file another process writes is read uncached" | no `exists()` in the eight; stamps through `stat` (r11) | -- |
| es-ui-style-guide.md § Confirmations | YES first, NO last, back answers NO (`GuiCloudTransfer.cpp:354-360`) | the match's text (F-08) |
| es-ui-style-guide.md § Interaction rules | buttons by role on the help bar (`:373-392`) | -- |
| es-player-text.md § Outcome vocabulary | three words; a why; what is in place; how to recover | the why table's two missing rows (F-11); the rule's own half (F-14, #909) |
| es-player-text.md § Conventions, player-language.md | the four tiers, the two verbs, Wi-Fi, the serial comma | `BRING DOWN`, `SEND UP`, `CAME DOWN` (F-09, F-10); `DID NOT` (F-10) |
| es-code-traps.md § rclone's piped progress | the glued line, the 80-column cut, U+2026, the `%3d` separator are all handled | the `%3d` separator and the job's splitter untested (F-05) |
| es-code-traps.md § Comments near a translatable string | 0 non-ASCII comment lines (r15) | -- |
| engineering-practices.md § Guards must fail closed | a stop needs a positive pid (`pid <= 0` never signals); a tier code that is not a number is not a success (`CloudText.cpp:594-597`) | `writeStamp` proceeds past a write it never checked (F-06); a comment claims a guard the test does not have (F-12) |
| engineering-practices.md § the last known good state (D-CLOUD-078) | temp and rename | the temp is never checked before the rename (F-06) |
| least-surprise.md | the same outcome words on the card and the page | exit 75 in eight wordings (F-15) |
| time-to-play.md | the exit sync bounded; the card lingers 1.5 s on success | the 2 s spin on the interface thread (F-07) |

## 3.3 Spec fidelity

- **D-UI-078 (the page sat in, CANCEL the way out):** held (`GuiCloudTransfer.cpp:246-260`). The leavable page's seams (`rowWords`, `stillRunningSentence`, the card's refusal) stay, as the header says, for a run current between its end and its dismissal.
- **D-UI-028 / D-UI-030 (three words):** held in the code. The comments still say "four" in five places (F-13).
- **D-CLOUD-077 (fail gracefully):**
  - Held: the in-place clauses, the retry on the reporting surface, a bounded run.
  - Not held: the stamp writer can leave a truncated stamp (F-06).
  - Against the words: the match's CANCEL dialog promises a recovery the backend refuses (F-08).
- **D-CLOUD-129 / D-CLOUD-130 (the launch question, STOP IT AND PLAY / KEEP WAITING):**
  - Held: the card's cancel honours the player's answer (`evenIfPlayerStarted`), and the job's stop is marked under the run's lock.
  - D-CLOUD-109's "bounded and visible" wait is bounded (2 s) but not visible while it spins (F-07).
- **D-UI-035 (candidates, longest first):** held for the outcome line, the action line, the live line and the scan sentence. Their fit at 640x480 is owed to the window.
- **D-UI-108 (a transfer says which file of how many):** held (`ThreadedCloudSync.cpp:396-427`).
- **D-CLOUD-175 (no automatic folder migration):** no automatic flow remains reachable from the eight, but the move's hooks remain (F-16).
- **D-UI-117 (`backuptool`'s proposed sentence):** the script prints it; the interface does not know it (F-11).

## 3.4 Platform conformance

- **Every command runs under `setsid sh -c` through `popen`.** The `popen` child is not a process group leader, so `setsid` does not fork, and the command's exit status reaches `pclose`. The design holds on busybox and util-linux alike. The guest's `setsid` is the image's, and the window reads it.
- **The stamps are written to `/storage/.cache/cloud_sync/`**, device-local, as the class comment says. `Utils::FileSystem::writeAllText` is `fopen`/`fwrite`/`fclose` with no check (F-06).
- **The card measures in the row's font on the interface thread** (`AsyncNotificationComponent`), and the page measures in its own fonts. Neither measures on the worker. The host has no font, so every fit is a frame.

## 3.5 Cross-system interaction audit

### Interaction: the cloud scripts (T16, T17) x the two readers

The protocol is the contract (§ The protocol). At `8ebaf8daad` the generator finds six `doing` lines, three offers, eleven `unit` lines and three `removed` lines in the scripts, and its `why` pattern matches 109 script lines (the emitters and the functions that wrap them). Every one classifies: the emitter table test holds that for the shapes it lists. Three ways the two sides drift apart unseen:

- **a new `>>> why`** passes the test (F-12) and shows in English (F-11);
- **a new marker** is dropped silently (F-03);
- **a script that ever printed `>>> pid`** would redirect a stop (F-01).

### Interaction: the card x the script stamps under a lost interface

When EmulationStation restarts under a card's run, its scripts die of SIGPIPE at their next write (F-02). The job's survive and stamp. Neither the card's own `last-sync-<origin>` stamp nor the scripts' stamp says what happened to that run; the row then reads the run before it. The next sync completes what the dead one did not (rclone's rename on completion).

### Interaction: the page x `backuptool` (T17's S7, #1136)

`backuptool restore`'s output reaches the settings-restore page (`GuiMenu.cpp:5043-5045`), so its `>>> why` lines are the page's line 4. The one sentence the why table lacks is the one #1136's fix area prints (F-11). T17's streams did not change the sentence, which is at `8ebaf8daad` and therefore inherited.

### Interaction: the card x the launch gate (T2's `FileData.cpp`)

`cancelForLaunch` runs inside the STOP IT AND PLAY callback (`FileData.cpp:996-1005`), on the interface thread, for up to 2 s. Past it, `launchWhenGone` shows a spinner; the transfer's question goes to `launchWhenGone` at once (`:1012-1020`). T2's audit (`feature/m6-es-launch-path-649`, `02` § the launch's question over a sync) owns the caller; this slice owns the 2 s spin (F-07).

### Interaction: the page x `SystemData::rescanChangedFolders`

The page posts the rescan after a restore (`GuiCloudTransfer.cpp:335`) and captures nothing. The rescan's own holders (#246's `dropGameListView`/`remakeGameListView`, `FolderMergeTests`) are SystemData's, another slice's. Nothing of this page is held across it.

### Interaction: the card x `ProxyCards` (the offline achievements' cards)

The card hands on to `ProxyCards::afterSync` after an automatic sync that reached the network (`ThreadedCloudSync.cpp:754-755`), after its own `delete this` is decided but before it runs. `ProxyCards` takes the window, not the card. `tests/app-unit/ProxyCardsTests.cpp` doubles the card (not run here).

### Interaction: M7's open work on these files

None of the 21 `m7` refs in the ES repository carries a commit on the 30 beyond the pin (`git rev-list --count --no-merges <pin>..<ref> -- <the 30>`: 0 for each); M7's October work on them is in the pin's history. The image the window would boot, `069fc2704421`, is built from M7's `build/m7-signin-20261022-07` (T2's record); its ES commit is not in this repository, so the window identifies the binary by the literal (§ The guest cycle).
