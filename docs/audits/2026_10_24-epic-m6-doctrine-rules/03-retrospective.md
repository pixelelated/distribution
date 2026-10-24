# Retrospective Audit — M6.P2 T4, the binding doctrine

Phase 3 over the doctrine. The question is not whether each sentence is well written, but whether the corpus holds where it meets the tree, the tools and the record, and where its own files meet each other.

## 3.1 Architectural coherence

- **One corpus, three readers.** Claude Code loads the rules by their globs. Crush loads all 30. Codex reads `AGENTS.md` alone. `instruction-files.md` keeps the corpus one (D-WORKFLOW-010) and `tools/rules-check` holds the index, the counts and `AGENTS.md`'s generated list. What nothing holds is the *prose* `AGENTS.md` and `CLAUDE.md` share, and the two have drifted (F-01). The architecture is sound; one sentence overstates its guard.
- **Rules point at tools, the index points at rules.** The rule-to-tool direction is checked: the 72 index rows' tools all exist (`t4-q6.py tooltable`). The tool-to-rule direction is not: 31 of 85 *Detail in* pairs name a rule that never names the tool (F-22), and one row describes a retired tool as live (F-18).

## 3.2 Project conformance

- **The front-matter standard (D-WORKFLOW-009):** `rules-check` passes all 30. The seven no-`paths:` rules each say so in their first paragraph (its `always` check).
- **The registers' contracts:**
  - `register-check` holds IDs once and every citation resolving (667 on the branch). It does not hold the open table's column shape or escaped pipes (F-23).
  - `ceremony-check` holds the blindspot guards from 52 on: every guard named in the register exists (`t4-q6.py blindspots`). Its friction line fails open (F-02).
- **The vocabulary rules applied to the rules themselves:**
  - *checkbox*, not *box*: used throughout, and `box-check` keeps its name as an identifier, which the rule allows.
  - `pixelelated` is lowercase everywhere (reader's grep, `NAMING.md`).
  - *Rasteratops* names the mirror at `CLAUDE.md:65`/`AGENTS.md:63` (F-08), against D-WORKFLOW-144's *a character, not the OS name*.

## 3.3 Spec fidelity

Every figure brief § 2 names was re-derived at the hash with no delta:
- 36 paths;
- 11,394 lines at the hash and 11,414 in the inventory;
- 24 rules and 5,179 lines loading every session;
- 181 cited IDs, 3 of them open;
- 72 tool rows;
- 8 legacy-path files;
- 74 blindspot entries, with 29 twice;
- one zero-match glob.

The deltas are the branch's, and each is named in `01` § Scope:
- `register-check`'s 667 against the brief's 660;
- the eleven paths against five;
- T2's edit at `11a2ee182f` against `f16cf7fc28`.

## 3.4 Platform conformance

The few sentences about the guest were checked against the source tree and the GENERIC_X64 install tree, by `ls` and `grep`, never by a guest:
- the `/var/log` bind (F-11);
- `realpath` (F-13);
- the ES units (F-14);
- the watchdog (F-16).

The guest would have shown the same files: `var-log.mount` is installed, and `usr/bin/realpath` is a link to `busybox`.

## 3.5 Cross-system interaction audit

### Interaction: `CLAUDE.md` x `AGENTS.md` x the rules, on the same facts

- **The shared state** is the facts every session starts from: the build commands, the counts, the VM's *no*, the device questions, the vocabulary.
- **Where they disagree:**
  - `AGENTS.md` and `CLAUDE.md` give different VM examples and decision IDs (`AGENTS.md:208-210` against `CLAUDE.md:188-190`) and different deploy questions (F-01).
  - Both repeat the same two wrong sentences, *needs OS_VERSION/BUILD_DATE exported* (F-03) and *only back up / backup is checked* (F-04). A fact copied into two files is wrong in two places when it goes stale.
  - Both say *two* interface-law documents, where `instruction-files.md` says three (F-09).
- **The guard** is `rules-check`, and it holds the count, the list and the mention, not the facts. The claim that it holds more is F-01.

### Interaction: the ES four x `docs/es-menu-map.md` and `docs/conflict-wizard-ia.md`

- **The shared state:** the interface law in two documents that load nowhere. `es-native-ui.md` § The other files names both, with what each owns. `CLAUDE.md:34` and `AGENTS.md:31` name them; `instruction-files.md:122` names them with `docs/device-testing-policy.md`.
- **The menu map is held by a tool** (`tools/es-menu-map-check`, D-UI-076, run as `vm-qa`'s `menumap` suite). The wizard IA is held by none, which `es-native-ui.md` does not claim otherwise.
- **No contradiction** beyond F-09's count.

### Interaction: the registers x the tools that read them

- **`register-check`** reads every ID and citation. It does not read the open table's columns (F-23), so a reader parsing the table misreads *Home* for six rows.
- **`ceremony-check`'s friction line** reads only lines its regex fits. 125 of 445 are skipped, so `ceremonies.md`'s promise that an entry without an issue refuses a push holds only for entries written in the shape (F-02).
- **`ceremony-check`'s guard line** is complete from 52 on.
- **`tools/archaeology`** reads all three registers; its `--reversal` option exists (futro U-3).

### Interaction: `time-to-play.md` x the register's three rows x the code

- **The rows:**
  - D-CLOUD-076 (2026-09-09): the launch cancels the sync;
  - D-CLOUD-109 (2026-09-12): it waits, bounded;
  - D-CLOUD-130 (2026-09-16): it asks STOP IT AND PLAY / KEEP WAITING.
- **The rule** describes the first two and names neither the third nor its question (`:31-35`, `:41-45`). `least-surprise.md:18-20` cites the second alone.
- **The code** ships the third, by T2's reading at the pin (`FileData.cpp:993-1008`). `es-native-ui.md` and `es-player-text.md` describe it.
- **So:** two every-session rules disagree with two others about one behaviour (F-10).

### Interaction: the briefs' stale-facts lists x the rules they name

- **Eight briefs** carry a *stale facts so they do not cost an hour* line (`01` § Phase 1). Every fact on them is real at the hash:
  - the legacy paths, 8 files (#640);
  - `OS_VERSION` (F-03);
  - the old ES owner (F-19).
- **Each lane paid for these** and wrote them into its brief, not into a rule. Nothing ties a brief's stale fact to the rule it names, so the next brief copies the line again. The ladder's answer is this slice: its findings are what those lines stop being needed for.

## The futro's predictions, checked

The doctrine futro (`docs/futros/2026-10-24-m6-doctrine.md`, § 2 unknowns, § 4 simulation, § 5 adjustments), read whole for this table. Each item is checked against what the read showed, not transcribed.

| Item | The futro | What the read showed |
| --- | --- | --- |
| U-1 | whose edit is D-QA-040's, and is it allowed | the coordinator's `f00ab3e163` (#646), on an **open** row. The contract speaks of decided rows; an open row's marker is neither a breach nor covered (F-23) |
| U-2 | how many of the 181 IDs are superseded | 34 IDs have a later row naming them near a reversal word; read one by one, 3 citations treat a superseded row as current (F-10, F-18) |
| U-3 | does `archaeology --reversal` exist | yes (its source, 3 mentions); `archaeology D-CLOUD-076` ran rc 0 |
| U-4 | how two lanes' edits to one rule merge | not exercised yet; it is stage E's |
| U-5 | does `box-check` fit the budget | one run cost 0 core calls (4,390 before and after) |
| U-6 | a third lane | none: this session took T4 (dispatch) |
| A1 | the `git archive` read tree in § 1 | used; every figure is the hash's |
| A2 | `git status --short -- <the 36>` empty at each stage-B end | recorded in `00` (0 lines) |
| A3 | the Q4 tables by a script | `tools/t4-q4.py`, committed |
| A4 | the legacy paths one item, `deferred:#640` | F-26, one item |
| A5 | `box-check` once at B, once at H, `--issue N` per issue | once at B; the rest at D and H |
| A6 | what the lane does during the pause | the retro's draft and the Q5 reader costs (§ 8) |
| A7 | the coordinator's rule edits posted on #651 | none posted since the dispatch; the branch's are listed in `01` |
| A8 | a glob change checked against the cross-reference | no glob is changed here; F-27's proposals carry the check |
| A9 | acceptance re-runs on the branch at `fixed-at` | stage H's |
| pre-mortem | 140 items, 120 of them wording | 27 findings; the Low wording ones are grouped by file for the stage-E streams |

**What the futro did not foresee:**
- the friction check failing open (F-02), which is blindspot 74's shape on a doctrine tool;
- three rules contradicting a unit file about `/var/log` (F-11);
- the index's tool-to-rule pointers (F-22);
- `council-substrate-integrity.md`'s absent defences (F-20).

Its blindspot proposal, *a corpus read on the wrong tree*, is entry 75 on the branch, and this slice's read avoided it by the at-hash tree.
