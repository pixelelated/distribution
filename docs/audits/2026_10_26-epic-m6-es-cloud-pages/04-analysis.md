# Analysis — M6.P2 T18, EmulationStation's cloud pages, cards and text (#665)

The lane's grades of `02`'s F-01 to F-19, before the seats. § Second opinion is written after them, with each seat's items graded.

## Executive summary

The four pairs do what the rules ask of them, and the hard parts hold:

- one parser for two readers;
- a stop as a request the run keeps;
- the stamp before the card;
- the posted step that cannot reach a deleted page.

221 unit cases pass on a host with no `cmake`.

What does not hold falls in three families:

- **The protocol under a pipe:**
  - the card's wrapper lacks the trap the job's has (F-02);
  - both readers take a pid from any line (F-01, latent);
  - an unknown marker vanishes silently (F-03).
- **Lifetimes and threads:**
  - the stamp writer renames a write it never checked (F-06);
  - the launch's stop spins on the interface thread (F-07).
- **The words:**
  - the CANCEL dialog over a match promises a recovery the backend refuses (F-08);
  - two script sentences have no translation, and one of them reaches a page (F-11);
  - two paraphrase verbs show on the small panel (F-09);
  - the comments, and the rule's half, describe older code (F-13, F-14).

The futro predicted two streams, the header comment and the why table's missing rows. Both are here, as F-13 and F-11. The rest is renovation:

- the retired folder move's leftovers (F-16);
- a dead function (F-17);
- exit 75's eight wordings (F-15);
- the test that is said to guard the why table and does not (F-12);
- the two readers' seam (F-18).

**Proposed for stage D: four bugs**, all Low (§ Q3), and fifteen renovation items. The coordinator disposes.

## Acceptance-criteria scorecard

#665's 19 checkboxes, at stage C (the coordinator ticks at acceptance):

| # | Checkbox (short) | State at stage C | Artifact |
| ---: | --- | --- | --- |
| 1 | `00` to `05` exist | `00` to `04` exist; `05` at stage D | the folder |
| 2 | the lint `PASS` | `--phase pre-issue` at stage C's end | `00` § Stage C |
| 3 | `review-plan.json`, provenance, manifest | at stage C | `second-opinions/` |
| 4 | the punch-list issue at its outcomes | stage D onward | the audit issue |
| 5 | `reviewed-at`, `fixed-at`, `fixed-at-es`; nothing under `packages/projects/tools` | `reviewed-at` `cbf6d7ef83` with the pin; r25 empty | `00`, r25 |
| 6 | `01` § Scope | done | `01` |
| 7 | the coverage table, 30 | done (the `awk` prints 30) | `02` § Coverage |
| 8 | § The protocol generated | done; exits 1 on drift (P8) | `tools/t18-protocol-table.py` |
| 9 | § The why table generated | done; exits 1 on drift (P9) | `tools/t18-why-table.py` |
| 10 | § The lifetimes | done, 13 rows | `02` |
| 11 | § The strings | done, except the fit at 640x480 (owed to the window) | `02` |
| 12 | § The tests | done: 221 PASS, 22 rows | `02`, r20 |
| 13 | § The runs | done, 26 rows | `02` |
| 14 | § The guest cycle | `CANNOT` until the window | `02` |
| 15 | `00`'s never-run record | held so far | `00` |
| 16 | `04` § Q3 with trace, `Already written:`, VM line, `proved:` | below | this file |
| 17 | every proof `proved:`; every punch item `question:`; every bug through `box-check` | 16 proofs; the rest at stage D | `02`, `05` |
| 18 | the retro | stage G | -- |
| 19 | the five checkers and the ES `pre-push-test` | at the hand-back | -- |

## Risk assessment

- **The highest risk to a player is F-06**, and it is small. A stamp truncated by a full `/storage` reads as NOT DONE ON THIS DEVICE YET until the next run rewrites it. No save is lost, and the next sync completes.
- **The highest risk to trust is F-08.** A player who cancels a match is told that the next backup or restore finishes it. The next match is refused until they check again (PL-001). The page's own footer then names the row to start from (`CloudText::matchRecovery`), so the dialog and the page disagree in one minute.
- **The highest risk to the code's future is F-12 with F-03.** A new `>>> why` or a new marker can land in a script, and every test still passes. A new why shows in English; a new marker vanishes. The generator here is the check the comment describes, and it lives in the distribution repository, not the ES one.

## Coverage boundary

- **Read whole:** the eight sources and `CloudTextTests.cpp`. The other 21 test files were read for subject, fixtures and the eight's functions.
- **Read as context:**
  - `tests/app-unit/` (19 files) and the eight harnesses;
  - the callers' lines where they decide what reaches the eight;
  - `FileSystemUtil.cpp`'s writer and `AtomicFileUtil.h`;
  - the scripts at `8ebaf8daad`, through the two generators.
- **Not run:**
  - `tests/app-unit`'s `app-unit-tests`, `proxycards-tests` and `bookkeeper-tests`, outside the brief's compiler scope. `jobs-tests` ran on the coordinator's yes: 6 cases PASS (F-19);
  - the harnesses, whose subjects are T26's;
  - `tools/es-syntax-check` (no toolchain; r21).
- **Owed to the window:**
  - the identification of the binary;
  - every fit at 640x480;
  - F-08's and F-09's frames;
  - the card during a sync and the page's live line;
  - `time-to-play --vm`;
  - F-02 on the real path, if the window allows (stop the interface under a sync, read the stamps).
- **Not this slice's:**
  - `GuiMenu.cpp`'s composition and its `exists()` reads (T26);
  - `FileData.cpp`'s launch gate (T2);
  - the scripts' bodies (T16, T17);
  - `cloud_content_transfer`'s TERM trap (T17's file; the lead in `02`).

## Second opinion

*(Written after the seats: the packet, the plan, each seat's items graded.)*

## Finding Verification

Each of `02`'s findings, re-read at the pin before it was graded; the re-read is the evidence named:

| F | Re-read | Verdict |
| --- | --- | --- |
| F-01 | both `case Pid:` arms assign without a guard; `git grep '>>> pid'` at `8ebaf8daad` finds no script line (P14's method) | CONFIRMED, latent |
| F-02 | r09; `cloud_backup:2504` traps INT and TERM, not PIPE | CONFIRMED |
| F-03 | both `default:` arms; no `LOG` in either | CONFIRMED |
| F-04 | `char line[512]; fgets(line, sizeof(line), pipe)` | CONFIRMED, latent (no line that long is known) |
| F-05 | no case names `CloudTransferJob`; the per-file split and the run loop are in `CloudTransferJob.cpp` | CONFIRMED |
| F-06 | P16 | CONFIRMED |
| F-07 | P15 | CONFIRMED |
| F-08 | `askCancel`'s third arm covers every kind but Scan and Create; `transferKind` returns Match for `--match` | CONFIRMED (a frame owed) |
| F-09 | `:805-808`; the short form when `sizeText(summary).x() > mLineWidth` | CONFIRMED in the code; whether 640x480 shows it is a frame |
| F-10 | `:745`, `:769` | CONFIRMED |
| F-11 | P10; `GuiMenu.cpp:5043-5045` keeps `backuptool restore`'s output | CONFIRMED |
| F-12 | the comment against the test | CONFIRMED |
| F-13 | each line read | CONFIRMED |
| F-14 | the rule's **Why** paragraph | CONFIRMED (#909's) |
| F-15 | the generator's table | CONFIRMED |
| F-16 | P13, P14 | CONFIRMED |
| F-17 | P12 | CONFIRMED |
| F-18 | § The protocol | design |
| F-19 | `jobs-tests` built and run on the coordinator's yes: 6 PASS | CONFIRMED, and covered |
| F-20 | the 640x480 frame `match-dialog/04-match-done.png`; `CloudTransferJob.cpp:343-349` | CONFIRMED (pin-binary) |

## Renovation face

### Q1 Modernize

- **The two readers' seam** (F-18). A shared reader would take the wrapper, the read loop and the pid once, and hand each kind to the surface. The job and the card would keep only what each does with a kind.
  - The smallest step is the wrapper: one function that builds `setsid sh -c 'echo ">>> pid $$"; { trap '' PIPE; CMD ; }' 2>&1` for both, which closes F-02.
  - The next is the read loop: the job's character loop with its glued-mark split, for both, which closes F-04.
  - A proposal for the coordinator, not a stream.
- **The stamp writer onto `Utils::AtomicFile::writeText`** (F-06). The writer exists, is tested here (`AtomicFileTests.cpp`), and is already used by `Settings.cpp` and `GuiMenu.cpp:5066`. The fix is the call, not a design.
- **The launch's two waits** (F-07): the card's spin and the job's `launchWhenGone`. One shape for both is the caller's change (T2's `FileData.cpp`), routed there.
- **`CloudText.cpp` by subject.** The offline proxy's stamps and the settings archive's name could be their own text files beside their tests. A proposal, low value now.

### Q2 Standards

The checklist (`03` § 3.2): the four tiers, the confirmation shape, the help bar, the three type sizes (the page uses the theme's three: title, text, small), `exists()` 0, French for every fork string, `CMakeLists.txt` failing closed, and no secret-shaped literal at rest, all held. Where it does not:

- **F-12:** a comment claims a test guards the why table; the test reads no script. The rule's fix is to say what does guard it (the generator), or to make the guard real: a check in the distribution repository, where the scripts are.
- **F-05:** the `%3d` separator and the job's glued splitter, two of the four piped-progress traps, have no unit case. Both parsers live in `CloudTransferJob.cpp` and are not pure; moving the per-file split into `CloudText` would let the existing binary test it (Q1).
- **F-19:** the job's lifetimes are tested by `jobs-tests`, which no standing command builds; it ran here on the coordinator's yes and passed (6 cases, ASan and UBSan). A standing place for `tests/app-unit` in a suite (`tools/vm-qa`'s `lifetime` builds part of it) is the proposal.

### Q3 Bugs

**Four proposed `bug`s, all Low.** Each carries its trace, its `Already written:` line, its VM line, and the `proved:` its fix would need. The rest of Q3 is renovation. F-20 (`SNES 0 FILES`) was found in the window, after the first draft of this list.

**Family (a), the protocol under a pipe.**

- **B1 (F-02): the card's scripts die of SIGPIPE when the interface goes, before they stamp.**
  - *Trace.* `ThreadedCloudSync.cpp:206-207` wraps the command as `setsid sh -c 'echo ">>> pid $$"; CMD' 2>&1`; the job's (`CloudTransferJob.cpp:636-637`) adds `{ trap '' PIPE; ... ; }`. Its comment says why: "a part that can still end writes its stamp". With the interface gone, the card's pipe has no reader, so the scripts' next `echo` (a `>>> why`, a `log_message` to stdout) kills them. `cloud_backup`'s trap (`:2504`) is INT and TERM, not PIPE, so no stamp is written. The rows then read the run before it.
  - *Already written:* nothing inherited. The missing stamp is an absence, and the next run's stamp replaces the last one as always; nothing on a device or in a cloud needs reading or migrating.
  - *VM line:* yes. Stop `essway` under a startup or exit sync on the guest, then read `/storage/.cache/cloud_sync/last-backup` and `last-restore` against the before-snapshot. A host fixture can show the same with the two wrapper strings from the source and a pipe closed early.
  - *Proof a fix needs:* `fixture` before and after on the host (the wrapper strings run under `sh` with a reader that closes), and `fix-walk-pending-image` for the guest.
- F-01, F-03 and F-04 are latent or silent, not defects with a failure today: renovation (Q1, Q7).

**Family (b), lifetimes and threads.**

- **B2 (F-06): a short write is renamed over the good stamp.**
  - *Trace.* `ThreadedCloudSync::writeStamp` (`:930-949`) writes `path + ".tmp"` with `Utils::FileSystem::writeAllText`. That is `void` (`FileSystemUtil.cpp:1429-1446`): it returns early on a failed `fopen` and never checks `fwrite` or `fclose`. `writeStamp` then calls `std::rename(tmp, path)`. On a full `/storage`, the rename replaces a whole stamp with an empty or cut one. `CloudText::parseLastRun` reads that as `ran = false`, and the row says NOT DONE ON THIS DEVICE YET. The comment above the writer (`:878-881`) promises "written whole or not at all".
  - *Already written:* stamps written by the old writer are whole, or truncated where a disk was full. The reader already treats a truncated one as never run. The fix writes new stamps whole through `Utils::AtomicFile::writeText`, and the next run rewrites any cut one; nothing to migrate.
  - *VM line:* yes, on the host. A case that links `writeStamp`'s logic with `AtomicFileUtil` under `ulimit -f 0` (SIGXFSZ ignored, T17's S5 stand-in for a full card) shows the old stamp survive. On the guest, a loop device filled to the byte.
  - *Proof a fix needs:* `fix-unit-test`. `writeStamp` is in the card's file, which links a `Window`, so the case needs the function moved beside `CloudText` or a stand-in like `jobs-tests`' doubles. That is stage D's question.
- **F-07** (the 2 s spin on the interface thread) is a design question about the caller: renovation, routed to T2's owner.

**Family (c), the words.**

- **B3 (F-08): the CANCEL dialog over a match promises a recovery the backend refuses.**
  - *Trace.* `askCancel` (`GuiCloudTransfer.cpp:351-361`) branches on `transferKind` for Scan and Create only. A match (`TransferKind::Match`, `--match`) gets `CANCEL THIS BACKUP OR RESTORE?` and `WHAT'S ALREADY IN PLACE STAYS. THE NEXT BACKUP OR RESTORE FINISHES WHAT THIS ONE DIDN'T.` A match is neither, and its next apply is refused with SOMETHING CHANGED SINCE YOU CHECKED (PL-001, `:363-367`). The page's own done footer names the row to check again (`CloudText::matchRecovery`). This is es-native-ui.md's anti-pattern: dialog text promising behaviour the backend does not do.
  - *Already written:* nothing inherited. It is a dialog; nothing is stamped or saved.
  - *VM line:* yes in principle: a match page against the QA WebDAV with a planned removal, back pressed while it runs. In T18's window it was `CANNOT`, because a match on the fixture ends at ELAPSED 0:00, before a press lands (`02` § The guest cycle). A before-frame needs a fixture large enough to keep a match running for a second or more. The binary carries the dialog's string (`identity.out`: 1 hit).
  - *Proof a fix needs:* `fix-walk-pending-image`. A fourth arm for Match, in words for the maintainer, with French; `docs/es-menu-map.md` § Cloud updated in the same change (D-UI-039).
- **B4 (F-11): two script sentences have no row, and one reaches a page in English.**
  - *Trace.* § The why table: `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` (`backuptool:1495`) and `ANOTHER CLOUD SYNC IS RUNNING` (`cloud_setup:797`) have no `whySentences` row.
    - The first reaches the settings restore page's line 4: the chain keeps `backuptool restore`'s output (`GuiMenu.cpp:5043-5045`), and `localizedWhy` passes an unlisted sentence through as it came. It shows in English under a French `COULDN'T FINISH`.
    - The second ends the CREATE page skipped, where line 4 is not drawn.
    - The test the comment names (F-12) cannot catch either.
  - *Already written:* nothing inherited by the interface. The scripts' stamps keep their English by design, and their readers translate.
  - *VM line:* yes. The first on the guest by a settings archive carrying a member type the restore refuses (T17's fixture shape), the page's line 4 read back in French. The second has no screen to show.
  - *Proof a fix needs:* `fix-unit-test`. A `localizedWhy` case for each pair, failing before the pairs are added, plus the French rows, and the generator re-run to 0 script-only.
- **F-09** (`BRING DOWN` / `SEND UP`) is decided at the frame. If the 640x480 frame shows the short form, it is a words `bug` under player-language.md's "the canonical verb, never a paraphrase"; if the long form fits, it is renovation. The window's before-frame is the deciding evidence.
- **F-20** (the match's done page names `SNES 0 FILES`) is framed at 640x480 (`match-dialog/04-match-done.png`). A system nothing was removed from is listed beside the one that lost a file, because `CloudTransferJob.cpp:343-349` keeps every item of `>>> removed`. A words nit: renovation, unless the coordinator calls it least surprise's.
- **F-10** (`DID NOT`, `CAME DOWN`), **F-13** (the comments), **F-14** (the rule's half, #909) and **F-15** (eight wordings) are renovation.

### Q4 Package currency

- **The pin is level with ROCKNIX's master:** merge base `bccd715707` = `upstream/master`, 725 ahead, 0 behind (r04).
- **M7's work on these files beyond the pin:** none. None of the 21 `m7` refs in the ES repository carries a commit on the 30 that the pin lacks (`03` § 3.5).
- **T17's streams on the scripts these readers read:**
  - S5 (#1132) makes `--set-systems` exit 1 on a failed write; the page reads that as `COULDN'T FINISH - SOMETHING WENT WRONG` unless the script says why. Its why is a stream question for T17's branch.
  - S6 (#1133) is the pair of sentences routed to this slice; F-11 is its landing place.
- **`tools/es-syntax-check`'s default root names the legacy M7 layout** (#640). r21 sets `ES_BUILD_ROOT=/nonexistent` as the brief requires, and the tool stops at the root first, never reaching its `ninja` check.

### Q5 Efficiency

- **The two time-to-play numbers.**
  - The latest in `docs/vm-qa-log.md` that carries both: 2026-09-27, `c9f5aa7de0` (x64 run 80): 0.58 s from the interface to a first frame, 1.01 s game to game.
  - T2's run on the window's image (`/workspace/artifacts/m6-t2-20261023/ttp-q5.log`, 2026-10-23): game to game 1.01 s median of 3; the STOP IT AND PLAY answer at 1.35 s; the exit sync's stamp 0.54 s; the card gone at 6.01 s. It is marked "Not a pass": no cloud was up, so the exit sync did nothing.
  - The window, with the QA WebDAV up, measures the real exit sync.
- **The 2 s budget against D-CLOUD-119's 3 s:** inside it. But the spin runs on the interface thread (F-07), so no frame is drawn while it spins: at 1.5 s the player sees the frame the dialog left.
- **The lingers:** 1.5 s on a completed run with nothing to act on, and 5 s otherwise (`ThreadedCloudSync.cpp:731`). T2's 6.01 s "card gone" is the 5 s linger after a run with an outcome to read, plus the fade.
- **The 20 ms spin** costs nothing measurable beyond holding the interface thread.

### Q6 Dead ends

Removals none: each is a proposal on the punch list for the coordinator.

- **F-16, what the retired folder move (#353) and folder step (#363) left:**
  - the `doing` words `copy`, `verify` and `remove` (`CloudTransferJob.cpp:387-389`) and their strings (`GuiCloudTransfer.cpp:1027-1032`);
  - the `DISCARDED SAVES` unit label (`CloudText.cpp:1108`);
  - the why row `YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED` (`:429`);
  - `setFailedNote` and `setDismissedAction`, which have no caller, and `setCompletedAction`'s `cancellable` parameter, never passed;
  - the comments that name them (`GuiCloudTransfer.h:76-100`, `CloudTransferJob.cpp:235-236`, `CloudText.cpp:1104-1105`).
- **F-17:** `CloudText::nextTime` has no product caller. `isKnownWhy` and `isKnownUnitLabel` are test-only, which is their job: oracles.
- **Markers parsed and never produced:** none beyond F-16's three `doing` words. `>>> tier` is ES's own composition, and `>>> offer` is read by both.
- **Test cases whose subject is gone:** none found. Every case's function exists at the pin.

### Q7 Clarity and structure

Can a reader tell, from the four pairs and the rules, which surface shows a sync and which a transfer, which words each may use, what each parses, and how each ends?

- **Yes, from the code and § The protocol.**
- **Less so from the comments** (F-13): the fallback map's comment names other words and sits above another function, and five comments still say "four words".
- **Less so from the rule** (F-14, #909's half).
- **Exit 75 reads eight ways** (F-15): the card's two, the page's scan word, `backuptool`'s, `cloud_setup`'s, `cloud_scan`'s, and the folder refusal's.

The two generated tables are the test this question asks for, and they pass with the findings named.

## Instruction File Recommendations

### Coverage gaps (would have prevented)

- **A comment that claims a test guards something names the test's mechanism, and the mechanism is read before the claim is repeated** (F-12). engineering-practices.md § A name is not a behaviour covers the reading; nothing asks the writer of the comment to check it. A proposal for es-code-traps.md § Pure text has a home: "a table a test holds is checked against its source by something that reads the source; a typed table is a second copy".
- **A reversal sweeps code as well as words** (F-16). decision-register.md's P-01 paragraph says "code comments, the docs, the menu map"; D-CLOUD-175's retirement left setters, words and strings. A proposal: the same paragraph names "the hooks, setters and protocol words the reversed flow used", with `tools/archaeology --reversal` run over the ES checkout too. The tool already reads it.

### Codification gaps (proposals for the coordinator)

- `tools/t18-why-table.py` as a standing check in `tools/vm-qa`'s `french` suite (the scripts' whys against the interface's rows), so a new script sentence fails a suite rather than a player's screen.
- The two wrappers in one function (Q1), and a rule line in es-code-traps.md: "a command the interface reads through a pipe ignores SIGPIPE inside its wrapper, so it outlives the reader long enough to stamp".

## Quality self-check

- Every F has a re-read and a verdict; every proof has a `proved:` cell; the counts match (16 and 16).
- The two generated tables exit 1 on a drifted tree.
- What I did not check:
  - every fit at 640x480, the binary on the image and F-08/F-09's frames are the window's;
  - `cloud_content_transfer`'s TERM trap was not followed into its caller.
