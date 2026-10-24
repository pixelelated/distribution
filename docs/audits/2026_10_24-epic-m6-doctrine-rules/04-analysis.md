# Analysis — M6.P2 T4, the binding doctrine

## Executive summary

**The doctrine mostly holds.** At `8ebaf8daad`:
- every rule is front-mattered and indexed;
- every one of the 181 decision IDs it cites resolves;
- every tool its index names exists;
- every blindspot guard exists;
- only one `paths:` glob matches nothing.

The figures the brief named re-derive with no delta.

**Where it lies, it lies in three shapes.**
1. **A guard claimed and not held:**
   - `AGENTS.md` says `rules-check` keeps it equal to `CLAUDE.md`, and the two have drifted (F-01);
   - `ceremonies.md` says a friction entry without an issue refuses a push, and `ceremony-check` never sees 125 of 445 entries (F-02).
2. **A superseded row described as current:** `time-to-play.md` and `least-surprise.md` on the launch over a sync, where D-CLOUD-130 ships (F-10); the index on a retired migration test (F-18).
3. **A fact that moved under its sentence:**
   - `/var/log`'s persistence in two rules (F-11);
   - `OS_VERSION` in both entry files (F-03);
   - four `generic-x64-vm-testing.md` sentences (F-12 to F-15);
   - five `rclone-cloud-sync.md` facts (F-21), one of which would break a bump;
   - the old ES owner in a PR command (F-19);
   - ten absent defences in the rule adopted from another estate (F-20).

**27 findings:**
- **13 are Q3 findings, a rule that lies:** F-01 to F-04, F-10 to F-15, and F-19 to F-21. Grouped by file, they make 8 `bug` issues at stage D, plus the existing #808. Four are Medium (F-01, F-02, F-10, F-11), plus F-21's `PKG_SHA256` sentence; the rest are Low.
- **3 are existing issues:** #808, #811, and #640's legacy paths.
- **The rest are Low `Renovation`:** counts, names, the index's pointers, the register's shape, the load.

No Critical or High. **Nothing in the 36 was changed.** The remedies are stage E's, one stream per file for the wording items (the futro's pre-mortem rule), and a tool proposal wherever the ladder says a tool could hold the shape (F-01, F-02, F-10, F-22, F-23).

## Acceptance-criteria scorecard

#651's sixteen criteria at stage C, before the punch-list issue.

| # | Criterion (short) | State | Artifact |
| --- | --- | --- | --- |
| 1 | `00` to `05` in the folder | met at D | this folder |
| 2 | lint `PASS` with the D-WORKFLOW-184 line | pre-issue at C; resolution at H | `tools/lint-audit-artifacts --phase pre-issue` |
| 3 | `review-plan.json` Local | met at C | `second-opinions/review-plan.json` |
| 4 | every punch item at a Phase 7 outcome | after the stage-D pause | `05` § Phase 7 |
| 5 | `reviewed-at`/`fixed-at` | H (`reviewed-at: 00e75ab135`) | #651's body |
| 6 | `01` § Scope and § The reader's pass | met at B | `01` |
| 7 | the 36-row coverage table | met at B | `02` § Coverage table |
| 8 | § Mechanical checks and § Command blocks | met at B | `02` |
| 9 | the four #644 findings and T2's lead | met at B | `02` |
| 10 | Q4's four tables by a script | met at C | § Q4 below, `tools/t4-q4.py` |
| 11 | Q5's load table; time to play untouched | met at C | § Q5 below |
| 12 | Q6's reachability tables, each unreached row with `Already written:` | met at C | § Q6 below |
| 13 | proof cells equal proof lines | met at B (26 = 26) | `02` § Proofs, `00` |
| 14 | the ladder per item; each bug names its sentence; nothing of the 36 changed before a stream | D, H | `05`, the bug issues |
| 15 | the retro | G | `docs/retros/2026-10-24-m6-doctrine-rules.md` |
| 16 | the six exit codes | H | #651 |

## Code Quality Assessment

Not a code read (plan § 6c, *a doctrine read*). As prose:

### Strengths

- **The front-matter standard holds everywhere,** and `rules-check` enforces it.
- **The registers resolve:** 667 IDs once, every citation a row, every blindspot guard a path.
- **The ledgers' conventions mostly work as designed:** a reversal cites the old ID, and 27 of 72 superseded-candidate citations name the successor beside it.

### Concerns

- **Facts copied between files go stale in each copy** (F-01, F-03, F-04, F-09).
- **Narrative and rule are interleaved** in the three largest rules (F-27), so a stale sentence is hard to see. Each of F-11 to F-16 sits in a dated paragraph.

### Complexity Hotspots

`generic-x64-vm-testing.md` (1,398 lines), `rclone-cloud-sync.md` (895) and `engineering-practices.md` (836). Where the 13 Q3 findings sit: 5 in `generic-x64-vm-testing.md` (F-11 to F-15; F-11 also in `es-code-traps.md`), 3 in the entry files (F-01, F-03, F-04), 1 each in `rclone-cloud-sync.md`, `ceremonies.md`, `time-to-play.md` with `least-surprise.md`, `fork-workflow.md` and `council-substrate-integrity.md`.

## Cornerstone Conformance

- `working-principles.md`'s ladder is applied to every finding (`02`, `05`).
- `decision-register.md`'s append-only contract: no decided row was edited at the hash or on the branch. The one in-place change is to an open row (F-23).
- `upgrade-and-install.md`: the doctrine writes nothing on a device, so the `Already written:` line for each item is about what sessions did on a sentence's strength (`05`).
- D-WORKFLOW-189: no rule edited here (`git status` empty, `00`).

## Spec Fidelity

### Aligned

Every figure of brief § 2 and § 5 re-derived with no delta (`03` § 3.3). The method was § 5's as written, with two additions:
- the superseded review narrowed to a reversal word near the ID, then read by hand;
- the index's tool-to-rule direction checked (F-22).

### Diverged

- **The eleven paths and `register-check`'s 667** are the branch's, not the brief's five and 660 (`01`).
- **The brief's T2 hash** `f16cf7fc28` is T2's tip; the edit is `11a2ee182f`.

## Missing Artifacts

None for the slice. Not done, and said so:
- `tools/archaeology --reversal` over every reversal row: the superseded review is the narrower, complete form for the IDs the 33 cite;
- the guest: never needed.

## Risk Assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| a lane designs against D-CLOUD-076/109 from `time-to-play.md` | medium | a launch path built against a superseded behaviour | F-10 |
| a friction line written without the field goes unowned | medium | a slowdown nobody owns; the gate looks green | F-02 |
| an rclone bump that follows `rclone-cloud-sync.md:126-128` | low | the fetch fails on a stale `PKG_SHA256` | F-21; fails closed, cheap |
| a proof reads `/var/log` before a reboot, believing it lost | low | a wasted cycle, or a wrong conclusion about a wipe | F-11 |
| the stream edits collide with the coordinator's at the merge | medium | an evening of hand-resolution | the futro's A7: streams name their paragraphs |

## Coverage Boundary

- **Covered:**
  - all 36 paths: 25 read whole by this lane, 11 by readers whose leads were re-read;
  - every fenced block;
  - every cited ID;
  - every tool and path the 36 name;
  - every glob;
  - every blindspot entry's guard;
  - the friction log against its check.
- **Not covered:**
  - the skills, agents and settings (T38's);
  - the reference docs under `docs/` (T39's);
  - the ES repository's own `AGENTS.md`/`CLAUDE.md` pointers;
  - the readers' unverified leads (`02` § Leads);
  - the tools' own correctness beyond what a rule claims of them.

## Finding Verification (Phase 4.5)

Each finding is argued against, and every PASS is asked what would have made it a FAIL (brief § 5 rule 4).

- **F-01.**
  - *Against:* `rules-check`'s `list` check makes `AGENTS.md`'s rule list equal to the front matter, so "kept equal" is true of the list.
  - *Read:* the sentence says *the same facts*, and the facts outside the list differ (`AGENTS.md:208-210` against `CLAUDE.md:188-190`).
  - **Stands, narrowed to the facts outside the list.**
- **F-02.**
  - *Against:* the entries without the field are old, and none is owed.
  - *Read:* true today, 0 owed. But the rule's sentence is categorical and the matcher drops a shape rather than counting it, so the next such entry is unread.
  - *Would have failed:* a constructed `- 2026-10-01 12:00 UTC -- x` line is skipped by the lifted regex (it has no `issue:`), which is the failure.
  - **Stands at Medium as a guard that fails open; nothing owed.**
- **F-10.**
  - *Against:* D-CLOUD-130 keeps D-CLOUD-109's bound.
  - *Read:* 130 *"Reverses the silent cancel of #101 / D-CLOUD-109 for launches"*, and its question is a choice, not a wait. `time-to-play.md`'s *"until it lands, both sentences are true of different builds"* names neither build that ships.
  - **Stands.**
- **F-11.**
  - *Against:* `/var/log` was tmpfs once (`rclone-cloud-sync.md:366`: *"it was tmpfs unless `debugging` was on before that row"*).
  - *Read:* history; the unit binds now, at the hash and in the install tree.
  - **Stands; the three sentences describe the pre-D-SYS-001 image.**
- **F-13.**
  - *Would have failed:* `CONFIG_REALPATH` unset, or no `usr/bin/realpath` in the tree. Both are present.
  - **Stands.**
- **F-14.**
  - *Against:* the sentence means *no unit the journal shows ES under*.
  - *Read:* its words are *"there is no `emustation` unit"*, and one is installed.
  - **Stands at Low, with its point recorded as true.**
- **F-21's `PKG_SHA256`.**
  - *Would have failed:* no `PKG_SHA256=` in `rclone/package.mk`. Two are there.
  - **Stands.**
- **F-22.**
  - *Against:* a whole-word search misses a tool named by a path (`tools/x`).
  - *Read:* the search matches `x` with `tools/` before it (the `(?<![\w-])` boundary does not exclude `/`).
  - **Stands.**
- **The PASSes:**
  - each glob count was set against a known-matching glob (`**` matching every path) and a known zero;
  - the tool table, against `git cat-file -e`, which fails for an absent path (it returned non-zero for `.githooks/pre-push-test`, which the ES fork carries and this tree does not);
  - the cited-ID resolution, against `register-check`'s own pass.

## Renovation face

All seven questions apply (brief § 4). The tables are written by scripts committed in `tools/`, all reading the at-hash tree `.qa-scratch/t4/at-hash/` and `git ls-tree -r --name-only 8ebaf8daad`, never a hand table (A3):
- `t4-q4.py` for Q4;
- `t4-q6.py` for Q5 and Q6;
- `t4-coverage.py` and `t4-blocks.py` for `02`.

### Q1 Modernize

Rules written against a mechanism the tree has replaced:
- **the legacy layout** (F-26, #640): 8 files, 25 lines;
- **the old root name** `build.ROCKNIX-*` (F-17): 8 lines in 4 rules;
- **the old ES owner** (F-19);
- **the pre-virgl headless default, four of `vm-qa`'s 17 suites, and the watchdog's home** (F-16);
- **the make-target lists** (F-07);
- **five rclone facts** (F-21);
- **a retired migration test described as live** (F-18).

The register rows that retired each are cited in the finding. No rule uses a retired tool's options: every tool the 36 name exists at the hash (Q4 b).

### Q2 Standards and best practices

The doctrine's own standards, applied to it:
- **`tools/rules-check`** rc 0: 30 rules front-mattered and indexed, `AGENTS.md` in budget and listing all 30.
- **`tools/register-check`** rc 0: 667 IDs once.
- **`tools/ceremony-check`:** every ceremony `ok` but W42 (M7's).
- **The vocabulary** a rule must itself obey holds: *checkbox*, lowercase `pixelelated`. The exception is *Rasteratops* naming the build mirror (F-08).
- **What the standards do not reach:**
  - the register's open-table shape and escaped pipes (F-23);
  - the friction log's one-line shape (F-24);
  - the blindspot register's duplicate 29 (F-25, #811).

### Q3 Bugs

**13 Q3 findings, a rule that lies:** F-01 to F-04, F-10 to F-15 and F-19 to F-21, each with the artifact that contradicts it in `02` § Findings. By file they are 8 `bug` issues at stage D, plus #808 (F-05), which already exists. The class of each:

| Class | Findings |
| --- | --- |
| a guard claimed and not held | F-01, F-02 |
| a superseded row as current | F-10 |
| a fact that moved | F-03, F-04, F-11 to F-15, F-19, F-21 |
| a defence named that this tree lacks | F-20 |

### Q4 Package currency

The doctrine has no upstream, so Q4 is **currency against the fork's own record and code**, in four tables.

**(a) The decision IDs the 33 non-register files cite:** 181, with 178 decided, 3 open and 0 absent. The last column lists every later row that cites the ID with a reversal word anywhere in its text: a loose candidate list (85 IDs), narrowed below.

| ID | Table | Date | Cited by | Later rows citing it with a reversal word |
| --- | --- | --- | --- | --- |
| `D-CLOUD-003` | Decided (line 21) | 2026-08-28 | decision-register.md | none |
| `D-CLOUD-018` | Decided (line 51) | 2026-09-02 | documentation-accuracy.md | `D-CLOUD-158` |
| `D-CLOUD-023` | Decided (line 58) | 2026-09-04 | documentation-accuracy.md, es-player-text.md | none |
| `D-CLOUD-027` | Decided (line 67) | 2026-09-04 | rclone-cloud-sync.md | `D-CLOUD-045` |
| `D-CLOUD-038` | Decided (line 90) | 2026-09-06 | time-to-play.md | `D-CLOUD-053`, `D-CLOUD-072`, `D-CLOUD-109` |
| `D-CLOUD-041` | Decided (line 98) | 2026-09-06 | least-surprise.md | `D-CLOUD-107` |
| `D-CLOUD-048` | Decided (line 106) | 2026-09-06 | rclone-cloud-sync.md | `D-CLOUD-050` |
| `D-CLOUD-049` | Decided (line 107) | 2026-09-06 | es-player-text.md, rclone-cloud-sync.md | none |
| `D-CLOUD-050` | Decided (line 108) | 2026-09-06 | es-player-text.md, rclone-cloud-sync.md | `D-CLOUD-158`, `D-WORKFLOW-101` |
| `D-CLOUD-052` | Decided (line 110) | 2026-09-07 | rclone-cloud-sync.md | `D-CLOUD-044` |
| `D-CLOUD-054` | Decided (line 115) | 2026-09-08 | rclone-cloud-sync.md | `D-CLOUD-055`, `D-CLOUD-056`, `D-CLOUD-063` |
| `D-CLOUD-058` | Decided (line 120) | 2026-09-08 | rclone-cloud-sync.md | none |
| `D-CLOUD-064` | Decided (line 126) | 2026-09-08 | rclone-cloud-sync.md | `D-CLOUD-072` |
| `D-CLOUD-070` | Decided (line 136) | 2026-09-09 | rclone-cloud-sync.md | none |
| `D-CLOUD-075` | Decided (line 141) | 2026-09-09 | engineering-practices.md | none |
| `D-CLOUD-076` | Decided (line 142) | 2026-09-09 | time-to-play.md | `D-CLOUD-109`, `D-CLOUD-136` |
| `D-CLOUD-077` | Decided (line 143) | 2026-09-10 | engineering-practices.md | `D-CLOUD-078`, `D-UI-028` |
| `D-CLOUD-078` | Decided (line 144) | 2026-09-10 | engineering-practices.md, handheld-evidence.md, rclone-cloud-sync.md | `D-CLOUD-110`, `D-CLOUD-146` |
| `D-CLOUD-098` | Decided (line 189) | 2026-09-11 | AGENTS.md, CLAUDE.md, instruction-files.md, time-to-play.md | none |
| `D-CLOUD-102` | Decided (line 193) | 2026-09-12 | least-surprise.md, upgrade-and-install.md | `D-CLOUD-094`, `D-CLOUD-168` |
| `D-CLOUD-103` | Decided (line 194) | 2026-09-12 | upgrade-and-install.md | none |
| `D-CLOUD-104` | Decided (line 195) | 2026-09-12 | least-surprise.md | `D-CLOUD-101` |
| `D-CLOUD-109` | Decided (line 200) | 2026-09-12 | least-surprise.md, time-to-play.md | `D-CLOUD-101`, `D-CLOUD-110`, `D-CLOUD-111`, `D-CLOUD-112`, `D-CLOUD-129`, `D-CLOUD-130` |
| `D-CLOUD-112` | Decided (line 203) | 2026-09-12 | time-to-play.md | `D-CLOUD-136`, `D-NET-013` |
| `D-CLOUD-113` | Decided (line 204) | 2026-09-12 | AGENTS.md, es-player-text.md, least-surprise.md, time-to-play.md | `D-CLOUD-129` |
| `D-CLOUD-118` | Decided (line 216) | 2026-09-12 | rclone-cloud-sync.md | `D-CLOUD-121` |
| `D-CLOUD-119` | Decided (line 217) | 2026-09-12 | time-to-play.md | none |
| `D-CLOUD-120` | Decided (line 218) | 2026-09-12 | rclone-cloud-sync.md | none |
| `D-CLOUD-121` | Decided (line 219) | 2026-09-12 | rclone-cloud-sync.md | none |
| `D-CLOUD-122` | Open (line 720) | - | time-to-play.md | none |
| `D-CLOUD-126` | Decided (line 264) | 2026-09-13 | rclone-cloud-sync.md | `D-CLOUD-127`, `D-CLOUD-128` |
| `D-CLOUD-128` | Decided (line 271) | 2026-09-13 | generic-x64-vm-testing.md, rclone-cloud-sync.md | none |
| `D-CLOUD-130` | Decided (line 206) | 2026-09-16 | es-player-text.md | none |
| `D-CLOUD-137` | Decided (line 403) | 2026-09-25 | rclone-cloud-sync.md | none |
| `D-CLOUD-141` | Decided (line 446) | 2026-09-28 | es-player-text.md, rclone-cloud-sync.md | none |
| `D-CLOUD-142` | Decided (line 447) | 2026-09-28 | rclone-cloud-sync.md | none |
| `D-CLOUD-143` | Decided (line 448) | 2026-09-28 | rclone-cloud-sync.md | none |
| `D-CLOUD-149` | Decided (line 470) | 2026-09-28 | rclone-cloud-sync.md | none |
| `D-CLOUD-150` | Decided (line 471) | 2026-09-28 | rclone-cloud-sync.md | none |
| `D-CLOUD-151` | Decided (line 473) | 2026-09-28 | rclone-cloud-sync.md | none |
| `D-CLOUD-152` | Decided (line 474) | 2026-09-28 | rclone-cloud-sync.md | none |
| `D-CLOUD-153` | Decided (line 482) | 2026-09-28 | rclone-cloud-sync.md | `D-CLOUD-154`, `D-CLOUD-166` |
| `D-CLOUD-154` | Decided (line 494) | 2026-09-29 | rclone-cloud-sync.md | none |
| `D-CLOUD-155` | Decided (line 485) | 2026-09-29 | rclone-cloud-sync.md | none |
| `D-CLOUD-158` | Decided (line 543) | 2026-09-30 | instruction-files.md | `D-CLOUD-159`, `D-CLOUD-165`, `D-CLOUD-174`, `D-CLOUD-175` |
| `D-CLOUD-174` | Decided (line 606) | 2026-10-04 | AGENTS.md, CLAUDE.md, NAMING.md | `D-CLOUD-175` |
| `D-CLOUD-175` | Decided (line 642) | 2026-10-07 | AGENTS.md, CLAUDE.md, documentation-accuracy.md, es-player-text.md, rclone-cloud-sync.md, upgrade-and-install.md | `D-CLOUD-177`, `D-CLOUD-178`, `D-CLOUD-179` |
| `D-CLOUD-177` | Decided (line 648) | 2026-10-07 | rclone-cloud-sync.md | none |
| `D-CLOUD-178` | Decided (line 650) | 2026-10-07 | rclone-cloud-sync.md | none |
| `D-CLOUD-181` | Decided (line 666) | 2026-10-08 | engineering-practices.md, rclone-cloud-sync.md | none |
| `D-CLOUD-184` | Decided (line 682) | 2026-10-11 | rclone-cloud-sync.md | none |
| `D-INFRA-006` | Decided (line 75) | 2026-09-05 | device-builds.md | `D-INFRA-007`, `D-WORKFLOW-166` |
| `D-INFRA-007` | Decided (line 76) | 2026-09-05 | device-builds.md | none |
| `D-INFRA-010` | Decided (line 171) | 2026-09-11 | handheld-evidence.md | `D-RA-002`, `D-RA-025`, `D-RA-026`, `D-WORKFLOW-013`, `D-WORKFLOW-040` |
| `D-INFRA-015` | Decided (line 614) | 2026-10-04 | device-builds.md | none |
| `D-INFRA-018` | Decided (line 620) | 2026-10-06 | worktrees.md | `D-INFRA-021`, `D-INFRA-022` |
| `D-INFRA-021` | Decided (line 632) | 2026-10-07 | worktrees.md | `D-INFRA-022` |
| `D-INFRA-022` | Decided (line 634) | 2026-10-07 | device-builds.md, worktrees.md | none |
| `D-INFRA-023` | Decided (line 684) | 2026-10-12 | worktrees.md | none |
| `D-LAUNCH-001` | Decided (line 132) | 2026-09-08 | rclone-cloud-sync.md | none |
| `D-QA-007` | Decided (line 97) | 2026-09-06 | AGENTS.md, CLAUDE.md, generic-x64-vm-testing.md, instruction-files.md, vm-first.md | `D-QA-009`, `D-QA-017` |
| `D-QA-008` | Decided (line 100) | 2026-09-06 | handheld-evidence.md | `D-QA-011`, `D-QA-015` |
| `D-QA-009` | Decided (line 109) | 2026-09-06 | generic-x64-vm-testing.md | none |
| `D-QA-011` | Decided (line 114) | 2026-09-07 | AGENTS.md, device-builds.md, engineering-practices.md, release-candidates.md | `D-QA-030` |
| `D-QA-012` | Decided (line 119) | 2026-09-08 | AGENTS.md, CLAUDE.md, ceremonies.md, issue-tracking.md | none |
| `D-QA-015` | Decided (line 184) | 2026-09-11 | AGENTS.md, CLAUDE.md, handheld-evidence.md, vm-first.md | `D-CLOUD-159`, `D-WORKFLOW-017`, `D-WORKFLOW-020` |
| `D-QA-016` | Decided (line 249) | 2026-09-13 | vm-first.md | none |
| `D-QA-017` | Decided (line 185) | 2026-09-11 | vm-first.md | `D-QA-058` |
| `D-QA-021` | Decided (line 227) | 2026-09-12 | AGENTS.md, engineering-practices.md | none |
| `D-QA-022` | Decided (line 228) | 2026-09-12 | engineering-practices.md | none |
| `D-QA-023` | Decided (line 253) | 2026-09-13 | device-builds.md | `D-WORKFLOW-016`, `D-WORKFLOW-017`, `D-WORKFLOW-018` |
| `D-QA-033` | Decided (line 340) | 2026-09-21 | AGENTS.md | none |
| `D-QA-035` | Decided (line 342) | 2026-09-21 | generic-x64-vm-testing.md | `D-QA-059` |
| `D-QA-036` | Decided (line 343) | 2026-09-21 | release-candidates.md | `D-QA-046` |
| `D-QA-040` | Open (line 723) | - | AGENTS.md, ceremonies.md | `D-QA-047` |
| `D-QA-041` | Decided (line 367) | 2026-09-24 | generic-x64-vm-testing.md, rclone-cloud-sync.md | `D-QA-058` |
| `D-QA-043` | Decided (line 389) | 2026-09-25 | issue-tracking.md, vm-first.md | `D-QA-046` |
| `D-QA-044` | Decided (line 381) | 2026-09-25 | AGENTS.md, bugs-are-agent-first.md, ceremonies.md, instruction-files.md, issue-tracking.md, vm-first.md | `D-QA-051` |
| `D-QA-045` | Decided (line 385) | 2026-09-25 | AGENTS.md, instruction-files.md, issue-tracking.md | none |
| `D-QA-046` | Decided (line 387) | 2026-09-25 | bugs-are-agent-first.md, release-candidates.md | `D-QA-047`, `D-QA-048`, `D-QA-049`, `D-QA-051` |
| `D-QA-048` | Decided (line 392) | 2026-09-25 | release-candidates.md | `D-QA-049`, `D-WORKFLOW-054` |
| `D-QA-049` | Decided (line 393) | 2026-09-25 | release-candidates.md | `D-RA-029`, `D-WORKFLOW-047`, `D-WORKFLOW-048`, `D-WORKFLOW-053`, `D-WORKFLOW-062` |
| `D-QA-050` | Decided (line 398) | 2026-09-25 | bugs-are-agent-first.md | `D-QA-051` |
| `D-QA-051` | Decided (line 399) | 2026-09-25 | AGENTS.md, bugs-are-agent-first.md, instruction-files.md | none |
| `D-QA-057` | Decided (line 492) | 2026-09-29 | generic-x64-vm-testing.md | none |
| `D-QA-058` | Decided (line 623) | 2026-10-06 | generic-x64-vm-testing.md, rclone-cloud-sync.md, release-candidates.md, vm-first.md | none |
| `D-QA-059` | Decided (line 625) | 2026-10-06 | generic-x64-vm-testing.md | none |
| `D-RA-016` | Decided (line 294) | 2026-09-14 | engineering-practices.md | `D-RA-029`, `D-WORKFLOW-138` |
| `D-RA-030` | Decided (line 412) | 2026-09-26 | es-player-text.md, generic-x64-vm-testing.md | none |
| `D-RA-035` | Decided (line 423) | 2026-09-27 | es-native-ui.md | `D-RA-036`, `D-RA-038`, `D-UI-103`, `D-UI-104` |
| `D-RA-036` | Decided (line 428) | 2026-09-27 | es-player-text.md | `D-UI-105` |
| `D-SYS-001` | Decided (line 161) | 2026-09-10 | handheld-evidence.md, rclone-cloud-sync.md | none |
| `D-SYS-002` | Decided (line 162) | 2026-09-10 | handheld-evidence.md | none |
| `D-SYS-003` | Decided (line 163) | 2026-09-10 | handheld-evidence.md | none |
| `D-SYS-004` | Decided (line 164) | 2026-09-10 | handheld-evidence.md | none |
| `D-SYS-006` | Open (line 721) | - | handheld-evidence.md | `D-SYS-009` |
| `D-UI-021` | Decided (line 78) | 2026-09-05 | es-native-ui.md | none |
| `D-UI-022` | Decided (line 92) | 2026-09-06 | AGENTS.md, CLAUDE.md, change-log.md, es-player-text.md, es-ui-style-guide.md, least-surprise.md, player-language.md, rclone-cloud-sync.md | `D-CLOUD-042`, `D-UI-077` |
| `D-UI-023` | Decided (line 96) | 2026-09-06 | es-player-text.md, player-language.md | `D-UI-029`, `D-UI-061` |
| `D-UI-024` | Decided (line 102) | 2026-09-06 | rclone-cloud-sync.md | `D-UI-025`, `D-UI-026`, `D-UI-028` |
| `D-UI-028` | Decided (line 145) | 2026-09-10 | es-player-text.md | `D-CLOUD-127`, `D-CLOUD-166`, `D-UI-029`, `D-UI-030`, `D-UI-078` |
| `D-UI-030` | Decided (line 151) | 2026-09-10 | es-player-text.md | none |
| `D-UI-031` | Decided (line 152) | 2026-09-10 | es-player-text.md | none |
| `D-UI-034` | Decided (line 167) | 2026-09-10 | es-code-traps.md | none |
| `D-UI-035` | Decided (line 168) | 2026-09-10 | es-player-text.md, player-language.md | `D-UI-096` |
| `D-UI-039` | Decided (line 190) | 2026-09-11 | AGENTS.md, CLAUDE.md, es-native-ui.md, es-ui-style-guide.md, instruction-files.md, working-principles.md | `D-UI-060`, `D-UI-076`, `D-WORKFLOW-155`, `D-WORKFLOW-156` |
| `D-UI-040` | Decided (line 208) | 2026-09-12 | es-player-text.md, least-surprise.md | `D-CLOUD-101` |
| `D-UI-041` | Decided (line 209) | 2026-09-12 | least-surprise.md | none |
| `D-UI-042` | Decided (line 210) | 2026-09-12 | AGENTS.md, CLAUDE.md, instruction-files.md, least-surprise.md | `D-CLOUD-165`, `D-UI-113` |
| `D-UI-045` | Decided (line 224) | 2026-09-12 | AGENTS.md, CLAUDE.md, es-player-text.md, instruction-files.md, player-language.md | `D-UI-105`, `D-UI-117` |
| `D-UI-051` | Decided (line 251) | 2026-09-13 | es-player-text.md | `D-UI-096` |
| `D-UI-052` | Decided (line 263) | 2026-09-13 | rclone-cloud-sync.md | `D-UI-075` |
| `D-UI-060` | Decided (line 308) | 2026-09-15 | es-native-ui.md | `D-UI-078` |
| `D-UI-070` | Decided (line 318) | 2026-09-16 | es-native-ui.md | `D-UI-078`, `D-UI-085` |
| `D-UI-071` | Decided (line 319) | 2026-09-16 | decision-register.md | `D-UI-118` |
| `D-UI-078` | Decided (line 344) | 2026-09-21 | decision-register.md, engineering-practices.md, es-native-ui.md | `D-UI-085` |
| `D-UI-079` | Decided (line 345) | 2026-09-22 | bugs-are-agent-first.md, engineering-practices.md, es-native-ui.md | `D-QA-051` |
| `D-UI-093` | Decided (line 404) | 2026-09-25 | es-native-ui.md, es-player-text.md | none |
| `D-UI-095` | Decided (line 413) | 2026-09-26 | es-native-ui.md, es-player-text.md | none |
| `D-UI-096` | Decided (line 414) | 2026-09-26 | es-native-ui.md, es-player-text.md | none |
| `D-UI-101` | Decided (line 421) | 2026-09-27 | es-native-ui.md, es-player-text.md | `D-UI-109` |
| `D-UI-103` | Decided (line 424) | 2026-09-27 | es-native-ui.md, es-player-text.md | none |
| `D-UI-104` | Decided (line 425) | 2026-09-27 | es-player-text.md | `D-RA-036`, `D-UI-105`, `D-UI-106` |
| `D-UI-105` | Decided (line 429) | 2026-09-27 | es-player-text.md | `D-UI-106` |
| `D-UI-106` | Decided (line 431) | 2026-09-27 | es-player-text.md | none |
| `D-UI-107` | Decided (line 432) | 2026-09-27 | es-native-ui.md, es-player-text.md | none |
| `D-UI-108` | Decided (line 433) | 2026-09-27 | es-player-text.md | none |
| `D-UI-109` | Decided (line 434) | 2026-09-27 | es-native-ui.md | none |
| `D-UI-112` | Decided (line 445) | 2026-09-28 | es-player-text.md | `D-UI-115` |
| `D-UI-115` | Decided (line 456) | 2026-09-28 | rclone-cloud-sync.md | none |
| `D-UI-117` | Decided (line 479) | 2026-09-28 | es-player-text.md | none |
| `D-WORKFLOW-004` | Decided (line 229) | 2026-09-12 | AGENTS.md | none |
| `D-WORKFLOW-005` | Decided (line 230) | 2026-09-12 | AGENTS.md, CLAUDE.md | none |
| `D-WORKFLOW-006` | Decided (line 231) | 2026-09-12 | AGENTS.md | `D-WORKFLOW-064` |
| `D-WORKFLOW-007` | Decided (line 236) | 2026-09-12 | CLAUDE.md, es-ui-style-guide.md | none |
| `D-WORKFLOW-008` | Decided (line 237) | 2026-09-12 | es-code-traps.md, es-native-ui.md, es-player-text.md | none |
| `D-WORKFLOW-009` | Decided (line 238) | 2026-09-12 | AGENTS.md, CLAUDE.md | none |
| `D-WORKFLOW-010` | Decided (line 248) | 2026-09-13 | instruction-files.md | none |
| `D-WORKFLOW-012` | Decided (line 240) | 2026-09-12 | fork-workflow.md | none |
| `D-WORKFLOW-013` | Decided (line 243) | 2026-09-13 | decision-register.md | `D-CLOUD-007` |
| `D-WORKFLOW-014` | Decided (line 250) | 2026-09-13 | release-candidates.md | `D-WORKFLOW-034`, `D-WORKFLOW-068`, `D-WORKFLOW-076` |
| `D-WORKFLOW-024` | Decided (line 335) | 2026-09-20 | fork-workflow.md, release-candidates.md | `D-QA-048`, `D-WORKFLOW-047` |
| `D-WORKFLOW-028` | Decided (line 354) | 2026-09-23 | AGENTS.md, ceremonies.md, instruction-files.md | none |
| `D-WORKFLOW-034` | Decided (line 368) | 2026-09-24 | release-candidates.md | `D-QA-048`, `D-UI-118`, `D-WORKFLOW-064` |
| `D-WORKFLOW-041` | Decided (line 378) | 2026-09-24 | device-builds.md | `D-WORKFLOW-042`, `D-WORKFLOW-048` |
| `D-WORKFLOW-042` | Decided (line 379) | 2026-09-24 | release-candidates.md | `D-QA-049` |
| `D-WORKFLOW-044` | Decided (line 382) | 2026-09-25 | instruction-files.md | `D-WORKFLOW-046` |
| `D-WORKFLOW-045` | Decided (line 383) | 2026-09-25 | AGENTS.md, instruction-files.md | none |
| `D-WORKFLOW-046` | Decided (line 390) | 2026-09-25 | release-candidates.md | none |
| `D-WORKFLOW-047` | Decided (line 394) | 2026-09-25 | AGENTS.md, instruction-files.md, release-candidates.md | `D-QA-049`, `D-WORKFLOW-062`, `D-WORKFLOW-063`, `D-WORKFLOW-076` |
| `D-WORKFLOW-048` | Decided (line 397) | 2026-09-25 | device-builds.md | none |
| `D-WORKFLOW-049` | Decided (line 406) | 2026-09-26 | release-candidates.md | `D-WORKFLOW-088`, `D-WORKFLOW-137` |
| `D-WORKFLOW-050` | Decided (line 408) | 2026-09-26 | issue-tracking.md, release-candidates.md, upgrade-and-install.md | none |
| `D-WORKFLOW-061` | Decided (line 468) | 2026-09-28 | fork-workflow.md, instruction-files.md | none |
| `D-WORKFLOW-062` | Decided (line 483) | 2026-09-29 | release-candidates.md | `D-WORKFLOW-063` |
| `D-WORKFLOW-068` | Decided (line 490) | 2026-09-29 | instruction-files.md | none |
| `D-WORKFLOW-088` | Decided (line 518) | 2026-09-30 | fork-workflow.md | none |
| `D-WORKFLOW-123` | Decided (line 564) | 2026-10-01 | NAMING.md | `D-WORKFLOW-144`, `D-WORKFLOW-157` |
| `D-WORKFLOW-128` | Decided (line 569) | 2026-10-01 | NAMING.md | `D-WORKFLOW-144` |
| `D-WORKFLOW-132` | Decided (line 581) | 2026-10-02 | ceremonies.md, issue-tracking.md | none |
| `D-WORKFLOW-133` | Decided (line 582) | 2026-10-02 | AGENTS.md, CLAUDE.md, learning-capture.md | none |
| `D-WORKFLOW-137` | Decided (line 589) | 2026-10-02 | adversarial-council.md | none |
| `D-WORKFLOW-138` | Decided (line 592) | 2026-10-02 | engineering-practices.md | none |
| `D-WORKFLOW-139` | Decided (line 594) | 2026-10-02 | AGENTS.md, CLAUDE.md, issue-tracking.md, milestone-phase-naming.md | none |
| `D-WORKFLOW-141` | Decided (line 598) | 2026-10-03 | engineering-practices.md | none |
| `D-WORKFLOW-142` | Decided (line 600) | 2026-10-03 | device-builds.md | `D-WORKFLOW-148` |
| `D-WORKFLOW-143` | Decided (line 602) | 2026-10-03 | device-builds.md, engineering-practices.md, generic-x64-vm-testing.md | none |
| `D-WORKFLOW-144` | Decided (line 604) | 2026-10-04 | AGENTS.md, CLAUDE.md, NAMING.md, es-player-text.md, es-ui-style-guide.md | `D-CLOUD-174`, `D-WORKFLOW-145`, `D-WORKFLOW-151` |
| `D-WORKFLOW-145` | Decided (line 608) | 2026-10-04 | NAMING.md | `D-WORKFLOW-146` |
| `D-WORKFLOW-148` | Decided (line 617) | 2026-10-05 | engineering-practices.md, generic-x64-vm-testing.md | none |
| `D-WORKFLOW-149` | Decided (line 627) | 2026-10-06 | adversarial-council.md | none |
| `D-WORKFLOW-151` | Decided (line 644) | 2026-10-07 | NAMING.md | none |
| `D-WORKFLOW-155` | Decided (line 658) | 2026-10-08 | AGENTS.md, CLAUDE.md, es-ui-style-guide.md | `D-WORKFLOW-156` |
| `D-WORKFLOW-156` | Decided (line 660) | 2026-10-08 | es-player-text.md | none |
| `D-WORKFLOW-157` | Decided (line 670) | 2026-10-09 | NAMING.md, device-builds.md | `D-WORKFLOW-158` |
| `D-WORKFLOW-159` | Decided (line 676) | 2026-10-11 | device-builds.md | none |
| `D-WORKFLOW-162` | Decided (line 689) | 2026-10-13 | AGENTS.md, CLAUDE.md, engineering-practices.md | none |
| `D-WORKFLOW-164` | Decided (line 697) | 2026-10-14 | engineering-practices.md | none |
| `D-WORKFLOW-165` | Decided (line 699) | 2026-10-14 | engineering-practices.md | none |
| `D-WORKFLOW-166` | Decided (line 701) | 2026-10-14 | device-builds.md | none |
| `D-WORKFLOW-168` | Decided (line 707) | 2026-10-15 | release-candidates.md | none |

<!-- ids in the 33 non-register files: 181 IDs; Decided 178; Open 3; with a reversal-word citer 85 -->

**(a), narrowed: the superseded review.** A later row naming the ID within 80 characters of *reverses*, *supersedes*, *replaces*, *withdraws*, *retires* or *overrides* gives 34 candidate IDs and 72 citations of them in the 33 files. Each citation was read with its successor row's sentence:
- **27** cite the successor beside the old ID.
- **42** cite a row the later one only refines, confirms or cites.
- **3 cite a superseded row as current** (F-10, F-18).

| Cited ID | Later row(s) near a reversal word | File | Lines | Successor in the file | Verdict |
| --- | --- | --- | --- | --- | --- |
| `D-CLOUD-018` | `D-CLOUD-158` | `documentation-accuracy.md` | 34 | NO | not superseded: 158 cites it in its refs; its *reverses* is D-WORKFLOW-101 |
| `D-CLOUD-027` | `D-CLOUD-045` | `rclone-cloud-sync.md` | 366 | NO | not superseded: 045 cites it for `replaces`, the field's name |
| `D-CLOUD-038` | `D-CLOUD-109` | `time-to-play.md` | 30 | D-CLOUD-109 | successor cited beside it |
| `D-CLOUD-050` | `D-CLOUD-158` | `es-player-text.md` | 57 | NO | not superseded: as D-CLOUD-018 |
| `D-CLOUD-050` | `D-CLOUD-158` | `rclone-cloud-sync.md` | 709 | NO | not superseded: as D-CLOUD-018 |
| `D-CLOUD-076` | `D-CLOUD-109` | `time-to-play.md` | 32, 34 | D-CLOUD-109 | successor cited beside it |
| `D-CLOUD-109` | `D-CLOUD-130` | `least-surprise.md` | 19 | NO | **superseded, cited as current** (F-10) |
| `D-CLOUD-109` | `D-CLOUD-130` | `time-to-play.md` | 32, 42 | NO | **superseded, cited as current** (F-10) |
| `D-CLOUD-158` | `D-CLOUD-159`, `D-CLOUD-174`, `D-CLOUD-175` | `instruction-files.md` | 156 | NO | **superseded, cited as current**: join/move/follow retired by D-CLOUD-175 (F-18) |
| `D-CLOUD-174` | `D-CLOUD-175` | `CLAUDE.md` | 44 | D-CLOUD-175 | successor cited beside it |
| `D-CLOUD-174` | `D-CLOUD-175` | `AGENTS.md` | 41 | D-CLOUD-175 | successor cited beside it |
| `D-CLOUD-174` | `D-CLOUD-175` | `NAMING.md` | 23 | NO | not superseded: cited with 175 and 176 together |
| `D-INFRA-010` | `D-RA-025` | `handheld-evidence.md` | 55 | NO | not superseded: D-RA-025 *confirms* it |
| `D-INFRA-018` | `D-INFRA-022` | `worktrees.md` | 139 | D-INFRA-022 | successor cited beside it |
| `D-INFRA-021` | `D-INFRA-022` | `worktrees.md` | 182 | D-INFRA-022 | successor cited beside it |
| `D-QA-007` | `D-QA-017` | `generic-x64-vm-testing.md` | 220 | NO | not superseded: D-QA-017 *refines* it |
| `D-QA-007` | `D-QA-017` | `instruction-files.md` | 94 | NO | not superseded: D-QA-017 *refines* it |
| `D-QA-007` | `D-QA-017` | `vm-first.md` | 11 | D-QA-017 | successor cited beside it |
| `D-QA-007` | `D-QA-017` | `CLAUDE.md` | 190 | NO | not superseded: D-QA-017 *refines* it |
| `D-QA-007` | `D-QA-017` | `AGENTS.md` | 210 | NO | not superseded: D-QA-017 *refines* it |
| `D-QA-008` | `D-QA-015` | `handheld-evidence.md` | 114 | D-QA-015 | successor cited beside it |
| `D-QA-011` | `D-QA-030` | `device-builds.md` | 599 | NO | not superseded: D-QA-030 says *not D-QA-011* |
| `D-QA-011` | `D-QA-030` | `engineering-practices.md` | 606 | NO | not superseded: D-QA-030 says *not D-QA-011* |
| `D-QA-011` | `D-QA-030` | `release-candidates.md` | 83 | NO | not superseded: D-QA-030 says *not D-QA-011* |
| `D-QA-011` | `D-QA-030` | `AGENTS.md` | 206 | NO | not superseded: D-QA-030 says *not D-QA-011* |
| `D-QA-015` | `D-CLOUD-159` | `handheld-evidence.md` | 40 | NO | not superseded: D-CLOUD-159 cites it, does not reverse it |
| `D-QA-015` | `D-CLOUD-159` | `vm-first.md` | 12, 67 | NO | not superseded: D-CLOUD-159 cites it, does not reverse it |
| `D-QA-015` | `D-CLOUD-159` | `CLAUDE.md` | 196 | NO | not superseded: D-CLOUD-159 cites it, does not reverse it |
| `D-QA-015` | `D-CLOUD-159` | `AGENTS.md` | 206 | NO | not superseded: D-CLOUD-159 cites it, does not reverse it |
| `D-QA-044` | `D-QA-051` | `bugs-are-agent-first.md` | 37, 58 | D-QA-051 | successor cited beside it |
| `D-QA-044` | `D-QA-051` | `ceremonies.md` | 37 | NO | not superseded: D-QA-051 *refines* it |
| `D-QA-044` | `D-QA-051` | `instruction-files.md` | 190 | D-QA-051 | successor cited beside it |
| `D-QA-044` | `D-QA-051` | `issue-tracking.md` | 129 | NO | not superseded: D-QA-051 *refines* it |
| `D-QA-044` | `D-QA-051` | `vm-first.md` | 34, 39 | NO | not superseded: D-QA-051 *refines* it |
| `D-QA-044` | `D-QA-051` | `AGENTS.md` | 215 | D-QA-051 | successor cited beside it |
| `D-QA-046` | `D-QA-048`, `D-QA-049`, `D-QA-051` | `bugs-are-agent-first.md` | 38 | D-QA-051 | successor cited beside it |
| `D-QA-046` | `D-QA-048`, `D-QA-049`, `D-QA-051` | `release-candidates.md` | 108 | D-QA-048,D-QA-049 | successor cited beside it |
| `D-QA-048` | `D-QA-049` | `release-candidates.md` | 74 | D-QA-049 | successor cited beside it |
| `D-QA-049` | `D-WORKFLOW-062` | `release-candidates.md` | 19, 120 | D-WORKFLOW-062 | successor cited beside it |
| `D-QA-050` | `D-QA-051` | `bugs-are-agent-first.md` | 38, 84 | D-QA-051 | successor cited beside it |
| `D-UI-022` | `D-CLOUD-042` | `change-log.md` | 41 | NO | not superseded: D-CLOUD-042 *follows* its vocabulary |
| `D-UI-022` | `D-CLOUD-042` | `es-player-text.md` | 56 | NO | not superseded: D-CLOUD-042 *follows* its vocabulary |
| `D-UI-022` | `D-CLOUD-042` | `es-ui-style-guide.md` | 160, 161 | NO | not superseded: D-CLOUD-042 *follows* its vocabulary |
| `D-UI-022` | `D-CLOUD-042` | `least-surprise.md` | 36 | NO | not superseded: D-CLOUD-042 *follows* its vocabulary |
| `D-UI-022` | `D-CLOUD-042` | `player-language.md` | 32 | NO | not superseded: D-CLOUD-042 *follows* its vocabulary |
| `D-UI-022` | `D-CLOUD-042` | `rclone-cloud-sync.md` | 742 | NO | not superseded: D-CLOUD-042 *follows* its vocabulary |
| `D-UI-022` | `D-CLOUD-042` | `CLAUDE.md` | 185 | NO | not superseded: D-CLOUD-042 *follows* its vocabulary |
| `D-UI-022` | `D-CLOUD-042` | `AGENTS.md` | 309 | NO | not superseded: D-CLOUD-042 *follows* its vocabulary |
| `D-UI-028` | `D-UI-030` | `es-player-text.md` | 236, 241 | D-UI-030 | successor cited beside it |
| `D-UI-039` | `D-UI-076` | `es-native-ui.md` | 48 | NO | not superseded: D-UI-076 enforces it |
| `D-UI-039` | `D-UI-076` | `es-ui-style-guide.md` | 36 | NO | not superseded: D-UI-076 enforces it |
| `D-UI-039` | `D-UI-076` | `instruction-files.md` | 124 | NO | not superseded: D-UI-076 enforces it |
| `D-UI-039` | `D-UI-076` | `working-principles.md` | 89 | NO | not superseded: D-UI-076 enforces it |
| `D-UI-039` | `D-UI-076` | `CLAUDE.md` | 35 | NO | not superseded: D-UI-076 enforces it |
| `D-UI-039` | `D-UI-076` | `AGENTS.md` | 32 | NO | not superseded: D-UI-076 enforces it |
| `D-UI-060` | `D-UI-078` | `es-native-ui.md` | 241 | D-UI-078 | successor cited beside it |
| `D-UI-070` | `D-UI-078` | `es-native-ui.md` | 241 | D-UI-078 | successor cited beside it |
| `D-UI-101` | `D-UI-109` | `es-native-ui.md` | 144 | D-UI-109 | successor cited beside it |
| `D-UI-101` | `D-UI-109` | `es-player-text.md` | 104 | NO | not superseded: cited for the cards' content; D-UI-109 changed their order |
| `D-UI-104` | `D-UI-106` | `es-player-text.md` | 132 | D-UI-106 | successor cited beside it |
| `D-UI-105` | `D-UI-106` | `es-player-text.md` | 132 | D-UI-106 | successor cited beside it |
| `D-UI-112` | `D-UI-115` | `es-player-text.md` | 303 | NO | not superseded: D-UI-115 extends it (*as D-UI-112*) |
| `D-WORKFLOW-024` | `D-QA-048` | `fork-workflow.md` | 179 | NO | not superseded: D-QA-048 cites its rule |
| `D-WORKFLOW-024` | `D-QA-048` | `release-candidates.md` | 112 | D-QA-048 | successor cited beside it |
| `D-WORKFLOW-034` | `D-QA-048` | `release-candidates.md` | 92 | D-QA-048 | successor cited beside it |
| `D-WORKFLOW-041` | `D-WORKFLOW-048` | `device-builds.md` | 349 | D-WORKFLOW-048 | successor cited beside it |
| `D-WORKFLOW-042` | `D-QA-049` | `release-candidates.md` | 114 | D-QA-049 | successor cited beside it |
| `D-WORKFLOW-144` | `D-WORKFLOW-151` | `es-player-text.md` | 26 | NO | not superseded: D-WORKFLOW-151 *refines* its retention clause |
| `D-WORKFLOW-144` | `D-WORKFLOW-151` | `es-ui-style-guide.md` | 29 | NO | not superseded: D-WORKFLOW-151 *refines* its retention clause |
| `D-WORKFLOW-144` | `D-WORKFLOW-151` | `CLAUDE.md` | 41 | NO | not superseded: D-WORKFLOW-151 *refines* its retention clause |
| `D-WORKFLOW-144` | `D-WORKFLOW-151` | `AGENTS.md` | 38 | NO | not superseded: D-WORKFLOW-151 *refines* its retention clause |
| `D-WORKFLOW-144` | `D-WORKFLOW-151` | `NAMING.md` | 47 | D-WORKFLOW-151 | successor cited beside it |

<!-- superseded review: 72 citations of 34 candidate IDs; 3 cite a superseded row as current -->

**(a), the record ledgers:** the IDs the blindspot register and the friction log cite. Every one resolves. These are records citing decisions, read for completeness, not as rules.

| ID | Table | Date | Cited by | Later rows citing it with a reversal word |
| --- | --- | --- | --- | --- |
| `D-CLOUD-017` | Decided (line 50) | 2026-09-01 | blindspot-register.md | `D-CLOUD-031`, `D-CLOUD-045` |
| `D-CLOUD-053` | Decided (line 113) | 2026-09-07 | blindspot-register.md | `D-CLOUD-133`, `D-CLOUD-134`, `D-CLOUD-135`, `D-UI-073` |
| `D-CLOUD-074` | Decided (line 140) | 2026-09-09 | blindspot-register.md | none |
| `D-CLOUD-077` | Decided (line 143) | 2026-09-10 | blindspot-register.md | `D-CLOUD-078`, `D-UI-028` |
| `D-CLOUD-098` | Decided (line 189) | 2026-09-11 | blindspot-register.md | none |
| `D-CLOUD-156` | Decided (line 541) | 2026-09-30 | blindspot-register.md | `D-CLOUD-157` |
| `D-CLOUD-170` | Decided (line 578) | 2026-10-01 | friction-log.md | `D-CLOUD-173` |
| `D-CLOUD-172` | Decided (line 580) | 2026-10-02 | friction-log.md | none |
| `D-CLOUD-179` | Decided (line 662) | 2026-10-08 | friction-log.md | `D-CLOUD-180` |
| `D-CLOUD-181` | Decided (line 666) | 2026-10-08 | friction-log.md | none |
| `D-INFRA-010` | Decided (line 171) | 2026-09-11 | blindspot-register.md | `D-RA-002`, `D-RA-025`, `D-RA-026`, `D-WORKFLOW-013`, `D-WORKFLOW-040` |
| `D-INFRA-011` | Decided (line 280) | 2026-09-14 | blindspot-register.md | none |
| `D-INFRA-021` | Decided (line 632) | 2026-10-07 | friction-log.md | `D-INFRA-022` |
| `D-INFRA-022` | Decided (line 634) | 2026-10-07 | friction-log.md | none |
| `D-LAUNCH-004` | Decided (line 400) | 2026-09-25 | blindspot-register.md | `D-UI-094` |
| `D-QA-008` | Decided (line 100) | 2026-09-06 | blindspot-register.md | `D-QA-011`, `D-QA-015` |
| `D-QA-015` | Decided (line 184) | 2026-09-11 | blindspot-register.md | `D-CLOUD-159`, `D-WORKFLOW-017`, `D-WORKFLOW-020` |
| `D-QA-036` | Decided (line 343) | 2026-09-21 | friction-log.md | `D-QA-046` |
| `D-QA-041` | Decided (line 367) | 2026-09-24 | friction-log.md | `D-QA-058` |
| `D-QA-052` | Decided (line 411) | 2026-09-26 | blindspot-register.md | none |
| `D-QA-058` | Decided (line 623) | 2026-10-06 | friction-log.md | none |
| `D-RA-013` | Decided (line 299) | 2026-09-14 | blindspot-register.md | `D-RA-029` |
| `D-RA-019` | Decided (line 297) | 2026-09-14 | blindspot-register.md | none |
| `D-RA-035` | Decided (line 423) | 2026-09-27 | blindspot-register.md, friction-log.md | `D-RA-036`, `D-RA-038`, `D-UI-103`, `D-UI-104` |
| `D-UI-057` | Decided (line 302) | 2026-09-15 | blindspot-register.md | `D-UI-069` |
| `D-UI-082` | Decided (line 349) | 2026-09-23 | blindspot-register.md | `D-UI-094` |
| `D-UI-083` | Decided (line 353) | 2026-09-23 | friction-log.md | none |
| `D-UI-094` | Decided (line 407) | 2026-09-26 | blindspot-register.md | `D-UI-114` |
| `D-WORKFLOW-014` | Decided (line 250) | 2026-09-13 | blindspot-register.md | `D-WORKFLOW-034`, `D-WORKFLOW-068`, `D-WORKFLOW-076` |
| `D-WORKFLOW-038` | Decided (line 373) | 2026-09-24 | blindspot-register.md | none |
| `D-WORKFLOW-041` | Decided (line 378) | 2026-09-24 | blindspot-register.md | `D-WORKFLOW-042`, `D-WORKFLOW-048` |
| `D-WORKFLOW-050` | Decided (line 408) | 2026-09-26 | blindspot-register.md | none |
| `D-WORKFLOW-066` | Decided (line 488) | 2026-09-29 | blindspot-register.md | `D-WORKFLOW-080` |
| `D-WORKFLOW-080` | Open (line 728) | 2026-09-29 | blindspot-register.md | none |
| `D-WORKFLOW-107` | Decided (line 535) | 2026-09-30 | friction-log.md | none |
| `D-WORKFLOW-116` | Decided (line 557) | 2026-10-01 | friction-log.md | `D-WORKFLOW-161` |
| `D-WORKFLOW-119` | Decided (line 560) | 2026-10-01 | friction-log.md | none |
| `D-WORKFLOW-149` | Decided (line 627) | 2026-10-06 | friction-log.md | none |
| `D-WORKFLOW-156` | Decided (line 660) | 2026-10-08 | friction-log.md | none |
| `D-WORKFLOW-168` | Decided (line 707) | 2026-10-15 | friction-log.md | none |

<!-- ids in the two record ledgers: 40 IDs; Decided 39; Open 1; with a reversal-word citer 22 -->

**(b) The tools the 36 name**, `tools/<x>` and `.githooks/<x>`: 104 names.
- **102 are tracked at the hash** (a file, or a directory such as `tools/vm-walks/`).
- **2 are not**, and neither is a lie:
  - `.githooks/pre-push-test` is the ES fork's (`fork-workflow.md:120` says *"the ES fork's"*);
  - `tools/pixelelated-vm-cloud-boundaries.audit_reader` is a friction line naming a function inside a tool.
- **The options column** lists each `--option` written within the same span after the name. One is not in the tool's text: `vm-serial`'s `--scan`. That is a false positive, because `--scan` is `cloud_content_restore`'s, inside the `vm-serial sh '...'` string (`generic-x64-vm-testing.md:571`).
- **Options checked by hand** for the command blocks (`02` § Command blocks) all exist. The one shape that does not run as written is F-15's `watch-build` without `--record-only`.

| Tool | At the hash | Named in (first three) | Options written beside it | Options not in its text |
| --- | --- | --- | --- | --- |
| `tools/rc-preflight` | tracked | bugs-are-agent-first.md:49, device-builds.md:570, fork-workflow.md:33 (+16) | `--no-fetch` `--only` `--tree` | none |
| `tools/ceremony-check` | tracked | ceremonies.md:2, ceremonies.md:15, ceremonies.md:50 (+22) | `--gate` `--issues-only` | none |
| `tools/work-log-index` | tracked | ceremonies.md:31, ceremonies.md:62, ceremonies.md:101 (+5) | `--check` `--write` | none |
| `tools/register-check` | tracked | ceremonies.md:32, decision-register.md:21, fork-workflow.md:33 (+4) | - | none |
| `tools/box-check` | tracked | ceremonies.md:37, fork-workflow.md:33, issue-tracking.md:144 (+5) | - | none |
| `tools/archaeology` | tracked | ceremonies.md:61, ceremonies.md:74, ceremonies.md:100 (+11) | `--issue` `--reversal` | none |
| `tools/pkgcheck` | tracked | device-builds.md:232, issue-tracking.md:187, packaging-and-patches.md:34 (+5) | - | none |
| `tools/watch-build` | tracked | device-builds.md:411, device-builds.md:422, fork-workflow.md:33 (+12) | `--admission` | none |
| `tools/host-maintenance/build-admission.md` | tracked | device-builds.md:426 | - | none |
| `tools/build-preflight` | tracked | device-builds.md:454, device-builds.md:455, fork-workflow.md:33 (+4) | `--reclaim-swap` | none |
| `tools/host-maintenance/README.md` | tracked | device-builds.md:461 | - | none |
| `tools/fork-publish-release` | tracked | device-builds.md:551, device-builds.md:584, fork-workflow.md:33 (+4) | `--prepare` | none |
| `.githooks/pre-push` | tracked | device-builds.md:559, fork-workflow.md:28, fork-workflow.md:125 (+14) | - | none |
| `tools/build-identity-test` | tracked | device-builds.md:593, fork-workflow.md:33, decision-register.md:676 (+1) | - | none |
| `tools/cloud-save-integrity` | tracked | engineering-practices.md:157, fork-workflow.md:33 | - | none |
| `tools/cloud-round-trip` | tracked | engineering-practices.md:183, engineering-practices.md:576, fork-workflow.md:33 (+19) | `--host` `--monitor-socket` `--only` `--serial-socket` | none |
| `tools/watch-job` | tracked | engineering-practices.md:275, engineering-practices.md:341, fork-workflow.md:33 (+10) | `--activity-dir` `--pattern` | none |
| `tools/watch-build-submit` | tracked | engineering-practices.md:309, fork-workflow.md:33, generic-x64-vm-testing.md:811 (+5) | `--owner` | none |
| `tools/last-good-scripts-test` | tracked | engineering-practices.md:442, fork-workflow.md:33, generic-x64-vm-testing.md:1040 (+31) | `--old` | none |
| `.githooks/pre-commit` | tracked | engineering-practices.md:449, fork-workflow.md:99, blindspot-register.md:1062 (+5) | - | none |
| `.githooks/secret-patterns` | tracked | engineering-practices.md:451, fork-workflow.md:100, blindspot-register.md:1063 | - | none |
| `tools/retroarch-wrapper-test` | tracked | engineering-practices.md:459, fork-workflow.md:33 | - | none |
| `tools/vm-qa` | tracked | engineering-practices.md:490, engineering-practices.md:830, es-native-ui.md:68 (+31) | `--only` | none |
| `tools/time-to-play` | tracked | engineering-practices.md:498, fork-workflow.md:33, generic-x64-vm-testing.md:22 (+15) | - | none |
| `tools/cloud-test-backend` | tracked | engineering-practices.md:727, fork-workflow.md:33, generic-x64-vm-testing.md:20 (+22) | `--backend` | none |
| `tools/device-act` | tracked | engineering-practices.md:814, fork-workflow.md:33, AGENTS.md:206 (+4) | - | none |
| `tools/es-menu-map-check` | tracked | es-native-ui.md:52, fork-workflow.md:33, working-principles.md:92 (+3) | - | none |
| `tools/es-syntax-check` | tracked | es-native-ui.md:415, fork-workflow.md:33, AGENTS.md:141 (+1) | - | none |
| `tools/vocabulary-check` | tracked | es-player-text.md:40, fork-workflow.md:33, CLAUDE.md:185 (+4) | - | none |
| `tools/pixelelated-state-check` | tracked | fork-workflow.md:33 | - | none |
| `tools/pixelelated-state-check-test` | tracked | fork-workflow.md:33, friction-log.md:651 | - | none |
| `tools/cloud-connections-test` | tracked | fork-workflow.md:33 | - | none |
| `tools/cloud-input-test` | tracked | fork-workflow.md:33 | - | none |
| `tools/test-fixtures` | directory | fork-workflow.md:33 | - | n/a: a directory |
| `tools/cloud-save-integrity-test` | tracked | fork-workflow.md:33, friction-log.md:421 | - | none |
| `tools/cloud-capture-stamp-test` | tracked | fork-workflow.md:33, rclone-cloud-sync.md:13, rclone-cloud-sync.md:359 (+1) | - | none |
| `tools/wait-lock-test` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:413, decision-register.md:140 | - | none |
| `tools/settings-modes-test` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:1298 | - | none |
| `tools/melonds-upgrade-test` | tracked | fork-workflow.md:33, friction-log.md:439 | - | none |
| `tools/lint-audit-artifacts` | tracked | fork-workflow.md:33, decision-register.md:362, blindspot-register.md:715 (+4) | - | none |
| `tools/vm-visual-qa` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:18, generic-x64-vm-testing.md:37 (+10) | `--gif` `--monitor` `--outdir` | none |
| `tools/vm-serial` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:13, generic-x64-vm-testing.md:112 (+16) | `--scan` `--timeout` | `--scan` |
| `tools/vm-pair` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:14, generic-x64-vm-testing.md:146 (+4) | - | none |
| `tools/vm-pair-test` | tracked | fork-workflow.md:33, friction-log.md:564 | - | none |
| `tools/vm-stop` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:15, generic-x64-vm-testing.md:204 (+1) | - | none |
| `tools/vm-stop-test` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:16, generic-x64-vm-testing.md:206 (+1) | - | none |
| `tools/vm-manager-system-check` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:17, AGENTS.md:283 | - | none |
| `tools/cloud-pair-migration` | tracked | fork-workflow.md:33, decision-register.md:577 | - | none |
| `tools/rasteratops-cloud-layout-test` | tracked | fork-workflow.md:33, friction-log.md:78, friction-log.md:80 (+3) | `--archives-only` | none |
| `tools/pixelelated-content-scope-test` | tracked | fork-workflow.md:33, friction-log.md:392, friction-log.md:397 | - | none |
| `tools/pixelelated-cloud-folder-test` | tracked | fork-workflow.md:33 | - | none |
| `tools/pixelelated-cloud-folder-vm-test` | tracked | fork-workflow.md:33 | - | none |
| `tools/pixelelated-cloud-validator-test` | tracked | fork-workflow.md:33 | - | none |
| `tools/pixelelated-save-layout-test` | tracked | fork-workflow.md:33, rclone-cloud-sync.md:121, friction-log.md:425 | - | none |
| `tools/pixelelated-duckstation-capture-test` | tracked | fork-workflow.md:33 | - | none |
| `tools/rasteratops-identity-check` | tracked | fork-workflow.md:33, NAMING.md:41 | `--es` | none |
| `tools/rasteratops-candidate-store` | tracked | fork-workflow.md:33 | - | none |
| `tools/rasteratops-vm-cloud-epic` | tracked | fork-workflow.md:33 | - | none |
| `tools/pixelelated-vm-cloud-boundaries` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:12, AGENTS.md:283 (+1) | - | none |
| `tools/cloud-census` | tracked | fork-workflow.md:33, rclone-cloud-sync.md:12, AGENTS.md:286 (+1) | - | none |
| `tools/emulator-exit-test` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:21, generic-x64-vm-testing.md:639 (+2) | `--identity` `--port` `--vm` | none |
| `tools/forbidden-terms-check` | tracked | fork-workflow.md:33, fork-workflow.md:110, decision-register.md:468 | - | none |
| `tools/rules-check` | tracked | fork-workflow.md:33, milestone-phase-naming.md:124, AGENTS.md:20 (+3) | `--write-agents` | none |
| `tools/release-catalog` | tracked | fork-workflow.md:33, decision-register.md:390 | `--check` | none |
| `tools/ra-offline-test` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:334, generic-x64-vm-testing.md:510 (+11) | - | none |
| `tools/ra-ui-test` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:1171, friction-log.md:236 (+1) | - | none |
| `tools/raofflineproxy-integration-test` | tracked | fork-workflow.md:33, friction-log.md:560 | - | none |
| `tools/raofflineproxy-installed-native-test` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:1355, friction-log.md:568 | - | none |
| `tools/raofflineproxy-consent-test` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:795 | - | none |
| `tools/qa-accounts` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:1051 | - | none |
| `tools/vm-walks` | directory | fork-workflow.md:33, generic-x64-vm-testing.md:19, generic-x64-vm-testing.md:433 (+8) | - | n/a: a directory |
| `tools/fork-worktree` | tracked | fork-workflow.md:33, fork-workflow.md:160, generic-x64-vm-testing.md:66 (+10) | `--force` | none |
| `tools/fork-package-freshness` | tracked | fork-workflow.md:33, fork-workflow.md:178, release-candidates.md:111 (+6) | - | none |
| `tools/vm-upgrade-rehearsal` | tracked | fork-workflow.md:33, release-candidates.md:63, upgrade-and-install.md:84 (+3) | - | none |
| `tools/vm-upgrade-readiness-test` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:1369, friction-log.md:566 (+1) | - | none |
| `tools/frame-diff` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:1269, decision-register.md:350 (+3) | `--build` | none |
| `tools/png-blackout` | tracked | fork-workflow.md:33 | - | none |
| `tools/fork-newdrive` | tracked | fork-workflow.md:33 | - | none |
| `tools/es-untranslated` | tracked | fork-workflow.md:33 | - | none |
| `tools/font-stems` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:1235, decision-register.md:376 (+4) | - | none |
| `tools/signin-memory` | tracked | fork-workflow.md:33, decision-register.md:378, decision-register.md:397 (+2) | - | none |
| `tools/es-launch-memory` | tracked | fork-workflow.md:33, friction-log.md:96, friction-log.md:100 (+2) | - | none |
| `tools/nova-led-test` | tracked | fork-workflow.md:33, friction-log.md:104 | - | none |
| `tools/rocknix-info-test` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:1378, friction-log.md:572 | - | none |
| `tools/usb-gadget-test` | tracked | fork-workflow.md:33, generic-x64-vm-testing.md:1325, decision-register.md:674 (+1) | `--output` | none |
| `tools/ra-candidate-games` | tracked | fork-workflow.md:33 | - | none |
| `tools/host-maintenance` | directory | fork-workflow.md:33, decision-register.md:614 | - | n/a: a directory |
| `tools/pr-stack-check` | tracked | fork-workflow.md:33, decision-register.md:510, decision-register.md:511 (+2) | - | none |
| `tools/prose-check` | tracked | fork-workflow.md:33, decision-register.md:500 | - | none |
| `tools/council` | directory | fork-workflow.md:33, decision-register.md:518 | - | n/a: a directory |
| `.githooks/guard-lib` | tracked | fork-workflow.md:98, decision-register.md:468 | - | none |
| `.githooks/commit-msg` | tracked | fork-workflow.md:102 | - | none |
| `.githooks/hooks-test` | tracked | fork-workflow.md:118, decision-register.md:468 | - | none |
| `.githooks/pre-push-test` | **absent** | fork-workflow.md:120 | - | n/a: absent |
| `tools/vm-walks/suite.txt` | tracked | generic-x64-vm-testing.md:444, decision-register.md:182 | - | none |
| `tools/vm-walks/claims.txt` | tracked | generic-x64-vm-testing.md:1245 | - | none |
| `tools/vm-walks/masks.txt` | tracked | generic-x64-vm-testing.md:1248, decision-register.md:350 | - | none |
| `tools/host-maintenance/build-admission` | tracked | worktrees.md:175, CLAUDE.md:95, AGENTS.md:93 | - | none |
| `tools/vm-walks/docs/README.md` | tracked | decision-register.md:498 | - | none |
| `tools/council/run` | tracked | decision-register.md:518 | - | none |
| `tools/pixelelated-vm-cloud-boundaries.audit_reader` | **absent** | friction-log.md:280 | - | n/a: absent |
| `tools/host-maintenance/test-retention-report` | tracked | friction-log.md:342 | - | none |
| `tools/host-maintenance/retention-report` | tracked | friction-log.md:346 | - | none |
| `tools/host-maintenance/test-build-monitor` | tracked | friction-log.md:661 | - | none |

<!-- tools: 104 named; absent 2; option not in the tool's text 1; tracked 102 -->

**(c) The counts a rule states about the tree.** The script's pattern (a number before *rules*, *entries*, *tools*, *screens*, *rows*, *files* and the like) finds 5 in the 33, all dated history and true as history. The reading found the rest, each recomputed:

| Where | The count as written | Recomputed at the hash | Verdict |
| --- | --- | --- | --- |
| `CLAUDE.md:22`, `AGENTS.md:27` | *All 30* rule files | 30 (`ls .claude/rules`; `rules-check` `count`) | true |
| `CLAUDE.md:25-32` | the table under *All 30* | 29 named (#808) | wrong (F-05) |
| `CLAUDE.md:27` | *the four principles* | 5 listed | wrong (F-06) |
| `CLAUDE.md:34`, `AGENTS.md:31` | *Two (more) documents* carry interface law | 3 by `instruction-files.md:122` | inconsistent (F-09) |
| `CLAUDE.md:59-61`, `AGENTS.md:56-58` | the 13 make targets | 15 device targets in the `Makefile`, `world` 12 | incomplete (F-07) |
| `generic-x64-vm-testing.md:880` | `vm-qa` runs four things | 17 `SUITES` (`vm-qa:63`) | stale (F-16) |
| `instruction-files.md` § The fork's own tools | one row per fork tool | 72 rows, every tool present | true |
| `es-native-ui.md` § The other files | *the four ES rules* and two documents | 4 rules; the documents as F-09 | true |
| `issue-tracking.md:112`, `learning-capture.md:85` | *17 of the 29 rules stale* | a 2026-10-02 measurement, marked so | true as history |
| `working-principles.md:90` | *lost 30 screens* | D-UI-076's 2026-09-18 count, marked so | true as history |

Class counts: 10 rows; 5 true; 4 wrong, incomplete or inconsistent; 1 stale.

| File:line | The count as written |
| --- | --- |
| `issue-tracking.md:112` | ...tree, and the session had loaded 17 of the 29 rules stale from a worktree 813... |
| `issue-tracking.md:146` | ...first run, 46 of 479 open checkboxes did, which is the sweep #268... |
| `learning-capture.md:85` | ...2026-10-02 the session's own worktree had 17 of 29 rules stale (#367).... |
| `rclone-cloud-sync.md:298` | ...on the host moves 1200 files in 1.5 s otherwise, and `RCLO... |
| `working-principles.md:90` | ...enu map to be updated in the same change and lost 30 screens in... |

<!-- counts: 5 stated -->

**(d) The repo paths the 36 name in backticks:** 245.
- 123 are tracked files and 54 tracked directories.
- 49 are globs or placeholders.
- 6 are the legacy layout, marked `#640` rather than failed.
- **13 are not in the tree, and 8 of those are not lies:**
  - rocknix.org's and lorry's files: `docs/configure/cloud-sync.md`, `docs/runbooks/00-workspace-disk.md`;
  - retired paths said to be retired: the three Copilot paths, `docs/es-ui-style-guide.md`, `packages/compress/zip` (*Upstream deleted*);
  - a stated absence: `docs/architecture/adr/`.

  The other 5 are `council-substrate-integrity.md`'s, and are F-20: `.github/workflows/ci.yml`, `research/council-research/`, and its three lint scripts.

| Path | At the hash | Named in (first three) |
| --- | --- | --- |
| `scripts/council-invoke.ts` | tracked file | adversarial-council.md:39, council-substrate-integrity.md:2, council-substrate-integrity.md:52 (+8) |
| `docs/friction-log.md` | tracked file | ceremonies.md:27 |
| `docs/retros/<date>-<scope>.md` | glob or placeholder | ceremonies.md:28 |
| `docs/work-logs/<yyyy_mm>-work_logs/<yyyy>-W<ww>-summary.md` | glob or placeholder | ceremonies.md:29 |
| `docs/work-logs/<yyyy_mm>-work_logs/SUMMARY.md` | glob or placeholder | ceremonies.md:30 |
| `.claude/rules/…` | glob or placeholder | ceremonies.md:34 |
| `docs/audits/<date>-*/` | glob or placeholder | ceremonies.md:35 |
| `docs/futros/<date>-<scope>.md` | glob or placeholder | ceremonies.md:36 |
| `docs/audits/<scope>/audit-completion.json` | glob or placeholder | ceremonies.md:47 |
| `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md` | glob or placeholder | ceremonies.md:58, learning-capture.md:30, CLAUDE.md:163 (+1) |
| `docs/work-logs/INDEX.md` | tracked file | ceremonies.md:63, learning-capture.md:36 |
| `docs/decision-register.md` | tracked file | ceremonies.md:72, decision-register.md:9, decision-register.md:88 (+5) |
| `docs/blindspot-register.md` | tracked file | ceremonies.md:72, decision-register.md:90, instruction-files.md:217 (+3) |
| `.github/workflows/fork-checks.yml` | tracked file | ceremonies.md:104, AGENTS.md:351, blindspot-register.md:1195 |
| `docs/cloud-sync-changelog.md` | tracked file | change-log.md:10, instruction-files.md:116, AGENTS.md:281 (+1) |
| `.claude/skills/council/SKILL.md` | tracked file | council-substrate-integrity.md:28, council-substrate-integrity.md:188, decision-register.md:585 |
| `scripts/verify-pins.ts` | tracked file | council-substrate-integrity.md:38 |
| `scripts/lib/verifier-pins.ts` | tracked file | council-substrate-integrity.md:38, fork-workflow.md:33 |
| `scripts/lint-council-seat-efforts.ts` | tracked file | council-substrate-integrity.md:40 |
| `research/council-research/**` | glob or placeholder | council-substrate-integrity.md:146, AGENTS.md:282 |
| `.github/workflows/ci.yml` | **absent** | council-substrate-integrity.md:155 |
| `research/council-research/.*` | glob or placeholder | council-substrate-integrity.md:161, council-substrate-integrity.md:170 |
| `research/council-research/` | **absent** | council-substrate-integrity.md:162 |
| `.claude/skills/council-research/references/phase-1-independent-research.md` | tracked file | council-substrate-integrity.md:190 |
| `scripts/lint-council-research-provenance.ts` | **absent** | council-substrate-integrity.md:194 |
| `scripts/lint-no-direct-council-member-invocation.ts` | **absent** | council-substrate-integrity.md:196 |
| `.claude/skills/council-research/SKILL.md` | tracked file | council-substrate-integrity.md:223 |
| `scripts/lint-council-research-digests.ts` | **absent** | council-substrate-integrity.md:224 |
| `scripts/check-stale-blob-drift.ts` | tracked file | council-substrate-integrity.md:239, fork-workflow.md:33 |
| `docs/` | tracked directory | decision-register.md:56, es-native-ui.md:34, es-native-ui.md:35 (+9) |
| `docs/work-logs/` | tracked directory | decision-register.md:89, decision-register.md:12 |
| `.claude/rules/` | tracked directory | decision-register.md:91, learning-capture.md:13, CLAUDE.md:157 (+2) |
| `docs/architecture/adr/` | **absent** | decision-register.md:98 |
| `config/path` | tracked file | device-builds.md:14, device-builds.md:108, CLAUDE.md:105 (+1) |
| `scripts/build_distro` | tracked file | device-builds.md:15, device-builds.md:409 |
| `projects/ROCKNIX/devices/SM8550/options` | tracked file | device-builds.md:25 |
| `docs/runbooks/00-workspace-disk.md` | **absent** | device-builds.md:38 |
| `/workspace/repos/rocknix` | legacy: #640 | device-builds.md:42, worktrees.md:13, blindspot-register.md:35 |
| `/workspace/repos/rocknix.worktrees/<name>` | legacy: #640 | device-builds.md:43 |
| `scripts/get_env` | tracked file | device-builds.md:84, device-builds.md:544, decision-register.md:75 |
| `scripts/image` | tracked file | device-builds.md:100, device-builds.md:409, generic-x64-vm-testing.md:44 (+6) |
| `config/functions` | tracked file | device-builds.md:135, device-builds.md:165, blindspot-register.md:20 |
| `projects/ROCKNIX/packages/<pkg>` | glob or placeholder | device-builds.md:163 |
| `packages/README.md` | tracked file | device-builds.md:218, packaging-and-patches.md:10, CLAUDE.md:19 (+3) |
| `scripts/build` | tracked file | device-builds.md:317, device-builds.md:410, device-builds.md:500 (+1) |
| `scripts/install` | tracked file | device-builds.md:336, device-builds.md:410, decision-register.md:258 |
| `scripts/build_compat` | tracked file | device-builds.md:410 |
| `docs/releases/versioning.md` | tracked file | device-builds.md:577, generic-x64-vm-testing.md:59, decision-register.md:670 (+2) |
| `docs/device-flashing-runbook.md` | tracked file | device-builds.md:604, CLAUDE.md:198, AGENTS.md:332 (+1) |
| `docs/…` | glob or placeholder | documentation-accuracy.md:21 |
| `docs/configure/<page>.md` | glob or placeholder | documentation-accuracy.md:22 |
| `docs/configure/cloud-sync.md` | **absent** | documentation-accuracy.md:26 |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf` | tracked file | documentation-accuracy.md:29 |
| `docs/upstream/README.md` | tracked file | engineering-practices.md:68, decision-register.md:699 |
| `docs/qa-logs/2026-10-04-watch-progress/` | tracked directory | engineering-practices.md:350 |
| `docs/qa-logs/2026-10-03-watch-job/test-watch-job.py` | tracked file | engineering-practices.md:359 |
| `docs/device-testing-policy.md` | tracked file | engineering-practices.md:676, handheld-evidence.md:40, instruction-files.md:125 (+5) |
| `docs/es-menu-map.md` | tracked file | es-native-ui.md:44, es-native-ui.md:47, instruction-files.md:123 (+10) |
| `docs/conflict-wizard-ia.md` | tracked file | es-native-ui.md:45, instruction-files.md:125, CLAUDE.md:36 (+6) |
| `scripts/<event>/` | glob or placeholder | es-native-ui.md:118 |
| `docs/es-ui-style-guide.md` | **absent** | es-ui-style-guide.md:17, decision-register.md:236 |
| `.claude/` | tracked directory | fork-workflow.md:17, fork-workflow.md:30, AGENTS.md:170 |
| `plans/` | tracked directory | fork-workflow.md:17, fork-workflow.md:32, worktrees.md:211 (+2) |
| `.github/sessions/` | tracked directory | fork-workflow.md:31 |
| `.github/workflows/fork-*` | glob or placeholder | fork-workflow.md:31 |
| `scripts/council-*` | glob or placeholder | fork-workflow.md:33, decision-register.md:518 |
| `scripts/lint-council-*` | glob or placeholder | fork-workflow.md:33 |
| `scripts/build-council-prompt.ts` | tracked file | fork-workflow.md:33 |
| `scripts/write-step-seal.ts` | tracked file | fork-workflow.md:33 |
| `scripts/verify-{pins,chain,seals}.ts` | glob or placeholder | fork-workflow.md:33 |
| `scripts/setup-council-mistral-tokenizer.mjs` | tracked file | fork-workflow.md:33 |
| `scripts/forge-write-status.mjs` | tracked file | fork-workflow.md:33 |
| `scripts/owner-queue-lint.mjs` | tracked file | fork-workflow.md:33 |
| `scripts/lib/council-*` | glob or placeholder | fork-workflow.md:33 |
| `scripts/__tests__/` | tracked directory | fork-workflow.md:33 |
| `seed/` | tracked directory | fork-workflow.md:33 |
| `research/` | tracked directory | fork-workflow.md:34, decision-register.md:371 |
| `.github/copilot-instructions.md` | **absent** | fork-workflow.md:35 |
| `.github/instructions/` | **absent** | fork-workflow.md:35, instruction-files.md:11, instruction-files.md:69 |
| `.github/shared-copilot-knowledge/` | **absent** | fork-workflow.md:36 |
| `packages/` | tracked directory | fork-workflow.md:43, CLAUDE.md:124, CLAUDE.md:127 (+2) |
| `projects/` | tracked directory | fork-workflow.md:43 |
| `.github/workflows/fork-wordlist.yml` | tracked file | fork-workflow.md:111 |
| `projects/ROCKNIX/packages/network/rclone/sources/` | tracked directory | fork-workflow.md:144 |
| `projects/ROCKNIX/packages/rocknix/sources/scripts/` | tracked directory | fork-workflow.md:145 |
| `projects/ROCKNIX/packages/network/rclone/` | tracked directory | generic-x64-vm-testing.md:36, AGENTS.md:322 |
| `projects/ROCKNIX/devices/GENERIC_X64/vm/profile.json` | tracked file | generic-x64-vm-testing.md:79 |
| `config/graphic` | tracked file | generic-x64-vm-testing.md:289, generic-x64-vm-testing.md:307, decision-register.md:411 (+2) |
| `docs/vm-qa-log.md` | tracked file | generic-x64-vm-testing.md:323, generic-x64-vm-testing.md:661, instruction-files.md:118 (+5) |
| `docs/qa-frames/.../README.md` | glob or placeholder | generic-x64-vm-testing.md:514 |
| `docs/qa-logs/2026-10-13-es-trim-comparison/fixtures/clear-owned-mounts.py` | tracked file | generic-x64-vm-testing.md:1396 |
| `docs/qa-logs/2026-10-08-preupgrade-runtime/` | tracked directory | handheld-evidence.md:106 |
| `.claude/skills` | tracked directory | instruction-files.md:15 |
| `.github/sessions/saved-session-state-next.md` | tracked file | instruction-files.md:64, learning-capture.md:64, CLAUDE.md:10 (+2) |
| `../rocknix.worktrees/` | legacy: #640 | instruction-files.md:113, worktrees.md:9, worktrees.md:240 |
| `packages/**` | glob or placeholder | instruction-files.md:115, CLAUDE.md:27, AGENTS.md:285 |
| `projects/**` | glob or placeholder | instruction-files.md:115, CLAUDE.md:27, AGENTS.md:285 |
| `projects/ROCKNIX/packages/**` | glob or placeholder | instruction-files.md:116, instruction-files.md:118, CLAUDE.md:29 (+3) |
| `scripts/mkimage` | tracked file | instruction-files.md:118, CLAUDE.md:173, AGENTS.md:283 (+1) |
| `docs/**` | glob or placeholder | instruction-files.md:119, CLAUDE.md:30, AGENTS.md:284 |
| `scripts/lib/council-verification.ts` | tracked file | instruction-files.md:120, AGENTS.md:282 |
| `docs/cloud-save-integrity.md` | tracked file | instruction-files.md:172, rclone-cloud-sync.md:61, decision-register.md:666 |
| `docs/releases/catalog.md` | tracked file | instruction-files.md:192, decision-register.md:390 |
| `docs/pr-series/map.txt` | tracked file | instruction-files.md:194, decision-register.md:497 |
| `docs/releases/device-facts.md` | tracked file | issue-tracking.md:143, vm-first.md:36, decision-register.md:385 (+2) |
| `.claude/rules/*.md` | glob or placeholder | learning-capture.md:22, CLAUDE.md:20, AGENTS.md:18 (+1) |
| `docs/work-logs/2026_06-work_logs/2026_06_27-work_log.md` | tracked file | learning-capture.md:31 |
| `.github/sessions/archived/` | tracked directory | learning-capture.md:66 |
| `docs/qa-logs/2026-10-02-milestone-order/` | tracked directory | milestone-phase-naming.md:127 |
| `packages/packages.mk.template` | tracked file | packaging-and-patches.md:16 |
| `packages/packages.mk.addon_template` | tracked file | packaging-and-patches.md:16 |
| `projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk` | tracked file | packaging-and-patches.md:41 |
| `packages/compress/zip` | **absent** | packaging-and-patches.md:56, blindspot-register.md:25 |
| `packages/linux/patches/<DEVICE>/` | glob or placeholder | packaging-and-patches.md:90, CLAUDE.md:143, AGENTS.md:155 |
| `projects/ROCKNIX/packages/hardware/quirks/` | tracked directory | packaging-and-patches.md:92, CLAUDE.md:143, AGENTS.md:156 |
| `packages/emulation/libretro-*` | glob or placeholder | packaging-and-patches.md:100 |
| `projects/ROCKNIX/packages/emulators/libretro/` | tracked directory | packaging-and-patches.md:101 |
| `projects/ROCKNIX/packages/emulators/standalone/` | tracked directory | packaging-and-patches.md:102 |
| `projects/ROCKNIX/packages/…` | glob or placeholder | packaging-and-patches.md:113 |
| `docs/save-manifest-schema.md` | tracked file | rclone-cloud-sync.md:154, decision-register.md:81, decision-register.md:82 (+1) |
| `docs/audits/2026_09_29-issue-315-size-only-fix/` | tracked directory | rclone-cloud-sync.md:895 |
| `docs/releases/rc-accept.txt` | tracked file | release-candidates.md:38, decision-register.md:398, decision-register.md:415 (+3) |
| `docs/pixelelated/rename-plan.md` | tracked file | CLAUDE.md:48, AGENTS.md:45, decision-register.md:604 (+1) |
| `config/options` | tracked file | CLAUDE.md:115, AGENTS.md:114 |
| `distributions/<DISTRO>/options` | glob or placeholder | CLAUDE.md:116, AGENTS.md:115 |
| `projects/<PROJECT>/options` | glob or placeholder | CLAUDE.md:116, AGENTS.md:115 |
| `projects/<PROJECT>/devices/<DEVICE>/options` | glob or placeholder | CLAUDE.md:117, AGENTS.md:116 |
| `config/arch.<ARCH>` | glob or placeholder | CLAUDE.md:117, AGENTS.md:116 |
| `projects/<PROJECT>/packages/` | glob or placeholder | CLAUDE.md:122, AGENTS.md:121 |
| `projects/<PROJECT>/devices/<DEVICE>/` | glob or placeholder | CLAUDE.md:123, AGENTS.md:122 |
| `projects/<PROJECT>/` | glob or placeholder | CLAUDE.md:128, AGENTS.md:128 |
| `distributions/ROCKNIX/` | tracked directory | CLAUDE.md:129, AGENTS.md:130, decision-register.md:564 |
| `scripts/` | tracked directory | CLAUDE.md:130, AGENTS.md:131 |
| `projects/ROCKNIX/packages/emulators/` | tracked directory | CLAUDE.md:135, AGENTS.md:137 |
| `../rocknix.worktrees/<name>` | legacy: #640 | CLAUDE.md:158, AGENTS.md:174 |
| `projects/ROCKNIX/packages/ui/emulationstation/package.mk` | tracked file | CLAUDE.md:177, AGENTS.md:140 |
| `.claude/rules/fork-workflow.md` | tracked file | AGENTS.md:133, decision-register.md:697 |
| `research/council-runs/**` | glob or placeholder | AGENTS.md:282 |
| `.claude/skills/council-research/**` | glob or placeholder | AGENTS.md:282 |
| `.claude/skills/council/**` | glob or placeholder | AGENTS.md:282 |
| `.claude/agents/council-member-*.agent.md` | glob or placeholder | AGENTS.md:282, decision-register.md:585 |
| `projects/ROCKNIX/devices/GENERIC_X64/**` | glob or placeholder | AGENTS.md:283 |
| `projects/ROCKNIX/packages/sysutils/**` | glob or placeholder | AGENTS.md:284 |
| `projects/ROCKNIX/packages/rocknix/**` | glob or placeholder | AGENTS.md:284 |
| `projects/ROCKNIX/devices/*/linux/**` | glob or placeholder | AGENTS.md:284 |
| `projects/ROCKNIX/devices/*/patches/linux/**` | glob or placeholder | AGENTS.md:284 |
| `projects/ROCKNIX/packages/network/rclone/**` | glob or placeholder | AGENTS.md:286 |
| `projects/ROCKNIX/packages/rocknix/sources/scripts/**` | glob or placeholder | AGENTS.md:286 |
| `docs/rasteratops/p0-sweep-hits.txt` | tracked file | NAMING.md:30 |
| `docs/qa-logs/2026-10-04-pixelelated-artifact-sweep/` | tracked directory | NAMING.md:35 |
| `docs/qa-logs/2026-10-02-candidate-preflight/` | tracked directory | NAMING.md:44 |
| `docs/pixelelated/art/` | tracked directory | NAMING.md:52 |
| `.claude/rules/decision-register.md` | tracked file | decision-register.md:11 |
| `docs/savestate-compat-test.md` | tracked file | decision-register.md:63 |
| `docs/cloud-vocabulary-audit.md` | tracked file | decision-register.md:92, decision-register.md:92 |
| `docs/save-history-serial-model-addendum.md` | tracked file | decision-register.md:193 |
| `.claude/rules/least-surprise.md` | tracked file | decision-register.md:210 |
| `.claude/rules/player-language.md` | tracked file | decision-register.md:224 |
| `research/council-runs/2026-09-11-save-history-one-home/` | tracked directory | decision-register.md:234 |
| `.claude/rules/es-ui-style-guide.md` | tracked file | decision-register.md:236, decision-register.md:658, decision-register.md:660 |
| `docs/audits/2026_09_13-milestone-stable-before-upstream/` | tracked directory | decision-register.md:252 |
| `.claude/skills/code-auditor/SKILL.md` | tracked file | decision-register.md:252, decision-register.md:627 |
| `projects/ROCKNIX/packages/network/avahi/package.mk` | tracked file | decision-register.md:258 |
| `docs/audits/2026_09_13-milestone-stable-before-upstream/01-research-notes.md` | tracked file | decision-register.md:258 |
| `.github/workflows/fork-generic-x64.yml` | tracked file | decision-register.md:268 |
| `.claude/skills/code-auditor/references/phases.md` | tracked file | decision-register.md:362 |
| `.claude/rules/release-candidates.md` | tracked file | decision-register.md:394, decision-register.md:707 |
| `.claude/rules/bugs-are-agent-first.md` | tracked file | decision-register.md:399 |
| `projects/ROCKNIX/packages/network/raofflineproxy/package.mk` | tracked file | decision-register.md:416 |
| `docs/qa-frames/2026-09-26/295-*` | glob or placeholder | decision-register.md:417 |
| `docs/qa-frames/2026-09-27/` | tracked directory | decision-register.md:419 |
| `docs/qa-frames/2026-09-27/300-offline-index-toast-clipped-c9f5aa7de0-640x480.png` | tracked file | decision-register.md:429 |
| `projects/ROCKNIX/packages/network/raofflineproxy-libchdr/package.mk` | tracked file | decision-register.md:430 |
| `docs/audits/2026_09_25-milestone-rc-round-since-258/streams/briefs/` | tracked directory | decision-register.md:440 |
| `docs/audits/2026_09_28-milestone-audit-of-the-fixes-307/03-retrospective.md` | tracked file | decision-register.md:452 |
| `docs/audits/2026_09_28-milestone-audit-of-the-fixes-307/04-analysis.md` | tracked file | decision-register.md:453 |
| `docs/audits/2026_09_28-milestone-audit-of-the-fix-round/` | tracked directory | decision-register.md:467 |
| `docs/technical-appendix-cloud-sync-and-offline-achievements.md` | tracked file | decision-register.md:499 |
| `.claude/skills/release-notes/SKILL.md` | tracked file | decision-register.md:500 |
| `docs/qa-frames/2026-09-29/329/before-b-*` | glob or placeholder | decision-register.md:503 |
| `docs/qa-frames/2026-09-29/329/before-a-*` | glob or placeholder | decision-register.md:504 |
| `docs/qa-frames/2026-09-29/330/` | tracked directory | decision-register.md:506 |
| `docs/releases/pr/` | tracked directory | decision-register.md:510 |
| `scripts/lib/` | tracked directory | decision-register.md:518 |
| `seed/corpus/` | tracked directory | decision-register.md:518 |
| `.claude/rules` | tracked directory | decision-register.md:518 |
| `.claude/skills/council/COUNCIL-BUNDLE.md` | tracked file | decision-register.md:518 |
| `research/seat-probes/2026-09-30-muse-roster/` | tracked directory | decision-register.md:518 |
| `docs/rasteratops/cloud-provider-2026-09-30.md` | tracked file | decision-register.md:534 |
| `docs/rasteratops/p0-sweep.md` | tracked file | decision-register.md:550, decision-register.md:564, decision-register.md:570 |
| `projects/ROCKNIX/filesystem/etc/machine-info` | tracked file | decision-register.md:554 |
| `docs/rasteratops/support-matrix.md` | tracked file | decision-register.md:555, decision-register.md:565 |
| `docs/rasteratops/p0-updater.md` | tracked file | decision-register.md:561, decision-register.md:569 |
| `docs/rasteratops/p0-read.md` | tracked file | decision-register.md:562 |
| `scripts/image:110-111` | tracked file | decision-register.md:569 |
| `.claude/rules/issue-tracking.md` | tracked file | decision-register.md:581, decision-register.md:594, friction-log.md:45 (+3) |
| `.claude/skills/session-stash` | tracked directory | decision-register.md:582 |
| `.claude/skills/session-resume` | tracked directory | decision-register.md:582 |
| `.claude/skills/code-auditor/` | tracked directory | decision-register.md:589 |
| `docs/rasteratops/cloud-folder-state-table.md` | tracked file | decision-register.md:590 |
| `docs/rasteratops/candidate-source-plan.md` | tracked file | decision-register.md:592 |
| `.claude/rules/milestone-phase-naming.md` | tracked file | decision-register.md:594, friction-log.md:475 |
| `.claude/skills/session-resume/SKILL.md` | tracked file | decision-register.md:596 |
| `.claude/rules/ceremonies.md` | tracked file | decision-register.md:596 |
| `.claude/rules/engineering-practices.md` | tracked file | decision-register.md:598, decision-register.md:602, decision-register.md:617 (+11) |
| `.claude/rules/device-builds.md` | tracked file | decision-register.md:600, decision-register.md:701, blindspot-register.md:837 (+4) |
| `docs/pixelelated/art/README.md` | tracked file | decision-register.md:608 |
| `docs/pixelelated/art/wordmark-system.md` | tracked file | decision-register.md:610 |
| `docs/pixelelated/art/source/palettes.json` | tracked file | decision-register.md:610 |
| `docs/qa-logs/2026-10-03-dependencies/` | tracked directory | decision-register.md:612 |
| `docs/qa-logs/2026-10-04-proxy-preflight/` | tracked directory | decision-register.md:612 |
| `docs/qa-logs/2026-10-05-watch-submit/` | tracked directory | decision-register.md:617 |
| `docs/qa-logs/2026-10-05-build-storage/approved-cleanup-20261006/` | tracked directory | decision-register.md:619 |
| `.claude/rules/worktrees.md` | tracked file | decision-register.md:620, decision-register.md:632, decision-register.md:634 (+3) |
| `docs/qa-logs/2026-10-07-pixelelated-replacement-16/approved-retirement-01/` | tracked directory | decision-register.md:621 |
| `.claude/rules/generic-x64-vm-testing.md` | tracked file | decision-register.md:625, friction-log.md:26, friction-log.md:458 (+2) |
| `.claude/rules/adversarial-council.md` | tracked file | decision-register.md:627 |
| `docs/qa-logs/2026-10-07-pixelelated-replacement-16/h700-retirement-proposal/` | tracked directory | decision-register.md:629 |
| `docs/pixelelated/cloud-folder-flow-review.md` | tracked file | decision-register.md:648, decision-register.md:650, decision-register.md:664 |
| `docs/qa-logs/2026-10-13-browser-stack/` | tracked directory | decision-register.md:691 |
| `docs/qa-logs/2026-10-13-proxy-memory-vm/` | tracked directory | decision-register.md:693 |
| `docs/qa-logs/2026-10-13-gtk4-feasibility/` | tracked directory | decision-register.md:693 |
| `docs/pixelelated/site-plan.md` | tracked file | decision-register.md:705 |
| `rocknix.worktrees/rclone-cleanup` | legacy: #640 | blindspot-register.md:29 |
| `rocknix.worktrees/generic-x64` | legacy: #640 | blindspot-register.md:29 |
| `projects/ROCKNIX/devices/GENERIC_X64/options` | tracked file | blindspot-register.md:946 |
| `.claude/rules/vm-first.md` | tracked file | blindspot-register.md:1019, friction-log.md:39 |
| `docs/qa-logs/2026-10-03-watch-job/test-watch-build.py` | tracked file | friction-log.md:114 |
| `docs/qa-logs/2026-10-06-upstream-drafts/verify-drafts.py` | tracked file | friction-log.md:230 |
| `docs/qa-logs/2026-10-07-pixelelated-replacement-16/preparation/prepare-build16-final-scans-corrected.py` | tracked file | friction-log.md:328 |
| `docs/qa-logs/2026-10-07-pixelelated-replacement-16/preparation/prepare-partial-ui02.py` | tracked file | friction-log.md:334 |
| `docs/qa-logs/2026-10-07-pixelelated-replacement-16/preparation/prepare-build16-supplemental02.py` | tracked file | friction-log.md:336 |
| `docs/qa-logs/2026-10-07-pixelelated-replacement-16/cloud02-observer-correction/corrected-observer.py` | tracked file | friction-log.md:338 |
| `docs/qa-logs/2026-10-07-pixelelated-replacement-16/selected-content01-acceptance/verify.py` | tracked file | friction-log.md:340 |
| `docs/qa-logs/2026-10-07-device-builds/spirv-host-control01/probe.py` | tracked file | friction-log.md:350 |
| `docs/qa-logs/2026-10-07-device-builds/preparation/spirv-host-smoke.py` | tracked file | friction-log.md:352 |
| `docs/qa-logs/2026-10-07-device-builds/build-root-controls02/run.py` | tracked file | friction-log.md:354 |
| `docs/qa-logs/2026-10-07-storage-retention/review-extractions.py` | tracked file | friction-log.md:358 |
| `docs/qa-logs/2026-10-07-storage-retention/execute-cleanup.py` | tracked file | friction-log.md:360 |
| `docs/qa-logs/2026-10-07-device-builds/rg35xxsp-adoption01/reboot-verify.py` | tracked file | friction-log.md:364 |
| `.claude/rules/learning-capture.md` | tracked file | friction-log.md:384 |
| `.claude/rules/handheld-evidence.md` | tracked file | friction-log.md:457 |
| `docs/qa-logs/2026-10-11-regression-fixtures/suite_parser.py` | tracked file | friction-log.md:585 |
| `docs/qa-logs/2026-10-12-nova-shutdown/` | tracked directory | friction-log.md:605 |
| `docs/qa-logs/2026-10-13-es-trim-product/` | tracked directory | friction-log.md:663 |

<!-- paths: 245 named; **absent** 13; glob or placeholder 49; legacy: #640 6; tracked directory 54; tracked file 123 -->

### Q5 Efficiency

**This slice does not touch time to play.** Interface to first frame and game to game are both untouched: nothing here runs on a device.

What the doctrine costs a session:
- **24 of 30 rules and 5,179 lines** load at every Claude Code session, plus `CLAUDE.md`'s 202, so 5,381 lines before the first file is opened.
- **Codex** reads `AGENTS.md`'s 351 lines.
- **Crush** loads all 30 rules, 7,999 lines.

The table below gives each rule's lines, when it loads, and how many of the 12 areas its globs reach. That figure is computed from the inventory's `area` column and reproduces P1's `cross-reference.md` § Doctrine to area for every area it lists.

**The reader cost, and what a narrowing would buy** (A6's column):
- **`generic-x64-vm-testing.md`** (1,398 lines, on a match) loads for every lane under `projects/ROCKNIX/packages/**` and the VM tools: 11 of 12 areas. Splitting its dated narrative from its instructions (F-27) would cut what those lanes read without dropping a rule.
- **`handheld-evidence.md`'s `docs/**`** loads it for every record a session opens, 125,306 paths.
- **The 24 every-session rules** include the safety rules that must stay so:
  - `engineering-practices.md` § Nothing runs on a person's device;
  - `vm-first.md`;
  - the reboot rule.

  A narrowing proposal names these as untouched first (A8). This slice proposes none at stage B; F-27 is the item.

| Rule | Lines | Loads | Areas whose paths it reaches (of 12) |
| --- | ---: | --- | ---: |
| `adversarial-council.md` | 124 | every session | 12 |
| `bugs-are-agent-first.md` | 91 | every session | 12 |
| `ceremonies.md` | 116 | every session | 12 |
| `change-log.md` | 47 | on a match | 9 |
| `council-substrate-integrity.md` | 253 | on a match | 3 |
| `decision-register.md` | 99 | every session | 12 |
| `device-builds.md` | 695 | every session | 12 |
| `documentation-accuracy.md` | 61 | every session | 12 |
| `engineering-practices.md` | 836 | every session | 12 |
| `es-code-traps.md` | 254 | every session | 12 |
| `es-native-ui.md` | 423 | every session | 12 |
| `es-player-text.md` | 343 | every session | 12 |
| `es-ui-style-guide.md` | 315 | every session | 12 |
| `fork-workflow.md` | 191 | every session | 12 |
| `generic-x64-vm-testing.md` | 1398 | on a match | 11 |
| `handheld-evidence.md` | 114 | on a match | 6 |
| `instruction-files.md` | 221 | every session | 12 |
| `issue-tracking.md` | 208 | every session | 12 |
| `learning-capture.md` | 91 | every session | 12 |
| `least-surprise.md` | 40 | every session | 12 |
| `milestone-phase-naming.md` | 127 | every session | 12 |
| `packaging-and-patches.md` | 113 | on a match | 8 |
| `player-language.md` | 68 | every session | 12 |
| `rclone-cloud-sync.md` | 895 | on a match | 3 |
| `release-candidates.md` | 154 | every session | 12 |
| `time-to-play.md` | 55 | every session | 12 |
| `upgrade-and-install.md` | 225 | every session | 12 |
| `vm-first.md` | 82 | every session | 12 |
| `working-principles.md` | 106 | every session | 12 |
| `worktrees.md` | 254 | every session | 12 |

| Area | Rules reaching it |
| --- | ---: |
| build-engine | 25 |
| cloud-sync-and-saves | 29 |
| devices | 28 |
| doctrine | 28 |
| emulators-and-cores | 27 |
| generic-packages | 27 |
| interface | 27 |
| offline-achievements | 27 |
| os-scripts-and-launch | 29 |
| patches-and-configs | 28 |
| records | 26 |
| tooling-and-guards | 27 |

<!-- load: 12 areas; every-session lines 5179 -->

### Q6 Dead ends

**(1) The 30 rules and their globs.**
- One glob matches no tracked path: `council-substrate-integrity.md`'s `research/council-research/**`. The rule still loads through its other six globs.
- **Already written:** no session ever loaded the rule by that glob, because there is no path under it. Sessions that did load it (through `scripts/council-invoke.ts` and the rest) read its defences as in place (F-20).
- Every other rule loads every session, or on at least one tracked path.

| Rule | Lines | `paths:` | Loads | Globs matching nothing at the hash |
| --- | ---: | --- | --- | --- |
| `adversarial-council.md` | 124 | `**` 133465 | every session | none |
| `bugs-are-agent-first.md` | 91 | none (every session) | every session | none |
| `ceremonies.md` | 116 | none (every session) | every session | none |
| `change-log.md` | 47 | `projects/ROCKNIX/packages/**` 2782, `docs/cloud-sync-changelog.md` 1 | on a match | none |
| `council-substrate-integrity.md` | 253 | `research/council-research/**` 0, `research/council-runs/**` 660, `.claude/skills/council-research/**` 12, `.claude/skills/council/**` 15, `.claude/agents/council-member-*.agent.md` 8, `scripts/council-invoke.ts` 1, `scripts/lib/council-verification.ts` 1 | on a match | `research/council-research/**` |
| `decision-register.md` | 99 | `**` 133465 | every session | none |
| `device-builds.md` | 695 | `**` 133465 | every session | none |
| `documentation-accuracy.md` | 61 | `**` 133465 | every session | none |
| `engineering-practices.md` | 836 | `**` 133465 | every session | none |
| `es-code-traps.md` | 254 | `**` 133465 | every session | none |
| `es-native-ui.md` | 423 | `**` 133465 | every session | none |
| `es-player-text.md` | 343 | `**` 133465 | every session | none |
| `es-ui-style-guide.md` | 315 | `**` 133465 | every session | none |
| `fork-workflow.md` | 191 | `**` 133465 | every session | none |
| `generic-x64-vm-testing.md` | 1398 | `projects/ROCKNIX/devices/GENERIC_X64/**` 9, `projects/ROCKNIX/packages/**` 2782, `scripts/mkimage` 1, `scripts/image` 1, `tools/vm-qa` 1, `tools/pixelelated-vm-cloud-boundaries` 1, `tools/vm-serial` 1, `tools/vm-pair` 1, `tools/vm-stop` 1, `tools/vm-stop-test` 1, `tools/vm-manager-system-check` 1, `tools/vm-visual-qa` 1, `tools/vm-walks/**` 33, `tools/cloud-test-backend` 1, `tools/emulator-exit-test` 1, `tools/time-to-play` 1, `docs/vm-qa-log.md` 1 | on a match | none |
| `handheld-evidence.md` | 114 | `projects/ROCKNIX/packages/sysutils/**` 181, `projects/ROCKNIX/packages/rocknix/**` 84, `projects/ROCKNIX/devices/*/linux/**` 96, `projects/ROCKNIX/devices/*/patches/linux/**` 429, `docs/**` 125225 | on a match | none |
| `instruction-files.md` | 221 | `**` 133465 | every session | none |
| `issue-tracking.md` | 208 | `**` 133465 | every session | none |
| `learning-capture.md` | 91 | `**` 133465 | every session | none |
| `least-surprise.md` | 40 | none (every session) | every session | none |
| `milestone-phase-naming.md` | 127 | `**` 133465 | every session | none |
| `packaging-and-patches.md` | 113 | `packages/**` 2546, `projects/**` 3903 | on a match | none |
| `player-language.md` | 68 | none (every session) | every session | none |
| `rclone-cloud-sync.md` | 895 | `projects/ROCKNIX/packages/network/rclone/**` 25, `projects/ROCKNIX/packages/rocknix/sources/scripts/**` 48, `tools/cloud-round-trip` 1, `tools/cloud-test-backend` 1, `tools/cloud-census` 1, `tools/cloud-capture-stamp-test` 1, `tools/last-good-scripts-test` 1 | on a match | none |
| `release-candidates.md` | 154 | none (every session) | every session | none |
| `time-to-play.md` | 55 | none (every session) | every session | none |
| `upgrade-and-install.md` | 225 | `**` 133465 | every session | none |
| `vm-first.md` | 82 | none (every session) | every session | none |
| `working-principles.md` | 106 | `**` 133465 | every session | none |
| `worktrees.md` | 254 | `**` 133465 | every session | none |

<!-- rules: 30; every session 24 rules, 5179 lines; on a match 6 rules, 2820 lines -->

**(2) The tool index's 72 rows.**
- Every tool and every rule a row names exists at the hash.
- **The dead pointer is the other direction:** 31 of the 85 tool-to-rule pairs name a rule that never names the tool (F-22).
- **One row describes a retired tool as live:** `cloud-pair-migration` (F-18). **Already written:** a session that followed the row ran a tool that refuses with exit 2 and writes nothing (`tools/cloud-pair-migration:58-62`).

| Row | Tools named | All tracked | Rule it points at | Rule exists |
| --- | --- | --- | --- | --- |
| 1 | `build-preflight` | yes | `device-builds.md` | yes |
| 2 | `host-maintenance/` | yes | `device-builds.md` | yes |
| 3 | `archaeology` | yes | `decision-register.md` | yes |
| 4 | `ceremony-check` | yes | `ceremonies.md` | yes |
| 5 | `frame-diff` | yes | `generic-x64-vm-testing.md` | yes |
| 6 | `work-log-index` | yes | `learning-capture.md` | yes |
| 7 | `watch-job` | yes | `engineering-practices.md` | yes |
| 8 | `watch-build` | yes | `device-builds.md` | yes |
| 9 | `watch-build-submit` | yes | `engineering-practices.md` | yes |
| 10 | `fork-worktree` | yes | `worktrees.md` | yes |
| 11 | `fork-package-freshness` | yes | `fork-workflow.md` | yes |
| 12 | `vm-upgrade-rehearsal`, `vm-upgrade-readiness-test` | yes | `upgrade-and-install.md` | yes |
| 13 | `cloud-pair-migration` | yes | `rclone-cloud-sync.md` | yes |
| 14 | `es-syntax-check` | yes | `es-native-ui.md` | yes |
| 15 | `png-blackout` | yes | `generic-x64-vm-testing.md` | yes |
| 16 | `fork-newdrive` | yes | `device-builds.md` | yes |
| 17 | `fork-publish-release` | yes | `device-builds.md` | yes |
| 18 | `pixelelated-state-check` | yes | `release-candidates.md` | yes |
| 19 | `pixelelated-state-check-test` | yes | `release-candidates.md` | yes |
| 20 | `device-act` | yes | `engineering-practices.md` | yes |
| 21 | `qa-accounts` | yes | `generic-x64-vm-testing.md` | yes |
| 22 | `vm-pair`, `vm-pair-test`, `vm-serial`, `vm-visual-qa`, `vm-walks/` | yes | `generic-x64-vm-testing.md` | yes |
| 23 | `vm-qa` | yes | `generic-x64-vm-testing.md` | yes |
| 24 | `vm-stop`, `vm-stop-test` | yes | `generic-x64-vm-testing.md` | yes |
| 25 | `vm-manager-system-check` | yes | `generic-x64-vm-testing.md` | yes |
| 26 | `cloud-round-trip`, `cloud-test-backend`, `cloud-census`, `cloud-capture-stamp-test` | yes | `rclone-cloud-sync.md` | yes |
| 27 | `cloud-connections-test`, `test-fixtures/` | yes | `rclone-cloud-sync.md` | yes |
| 28 | `cloud-input-test` | yes | `generic-x64-vm-testing.md` | yes |
| 29 | `cloud-save-integrity`, `cloud-save-integrity-test` | yes | `rclone-cloud-sync.md`, `docs/cloud-save-integrity.md` | yes |
| 30 | `settings-modes-test` | yes | `generic-x64-vm-testing.md` | yes |
| 31 | `melonds-upgrade-test` | yes | `upgrade-and-install.md` | yes |
| 32 | `emulator-exit-test`, `wait-lock-test`, `last-good-scripts-test` | yes | `generic-x64-vm-testing.md` | yes |
| 33 | `time-to-play` | yes | `time-to-play.md` | yes |
| 34 | `ra-offline-test` | yes | `generic-x64-vm-testing.md` | yes |
| 35 | `ra-ui-test` | yes | `generic-x64-vm-testing.md` | yes |
| 36 | `ra-candidate-games` | yes | `generic-x64-vm-testing.md` | yes |
| 37 | `retroarch-wrapper-test` | yes | `engineering-practices.md` | yes |
| 38 | `es-menu-map-check` | yes | `es-native-ui.md` | yes |
| 39 | `es-untranslated` | yes | `es-native-ui.md` | yes |
| 40 | `font-stems` | yes | `es-native-ui.md` | yes |
| 41 | `signin-memory` | yes | `generic-x64-vm-testing.md` | yes |
| 42 | `vocabulary-check` | yes | `es-player-text.md` | yes |
| 43 | `forbidden-terms-check` | yes | `fork-workflow.md` | yes |
| 44 | `register-check` | yes | `decision-register.md` | yes |
| 45 | `lint-audit-artifacts` | yes | `issue-tracking.md` | yes |
| 46 | `rules-check` | yes | `instruction-files.md` | yes |
| 47 | `box-check` | yes | `issue-tracking.md` | yes |
| 48 | `prose-check` | yes | the `developer-relations` skill | n/a: names no rule file |
| 49 | `release-catalog` | yes | `issue-tracking.md` | yes |
| 50 | `rc-preflight` | yes | `release-candidates.md` | yes |
| 51 | `pr-stack-check` | yes | `fork-workflow.md` | yes |
| 52 | `es-launch-memory` | yes | `generic-x64-vm-testing.md` | yes |
| 53 | `build-identity-test` | yes | `device-builds.md` | yes |
| 54 | `usb-gadget-test` | yes | `generic-x64-vm-testing.md` | yes |
| 55 | `nova-led-test` | yes | `generic-x64-vm-testing.md` | yes |
| 56 | `raofflineproxy-integration-test` | yes | `generic-x64-vm-testing.md` | yes |
| 57 | `rocknix-info-test` | yes | `generic-x64-vm-testing.md` | yes |
| 58 | `raofflineproxy-installed-native-test` | yes | `generic-x64-vm-testing.md` | yes |
| 59 | `raofflineproxy-consent-test` | yes | `generic-x64-vm-testing.md` | yes |
| 60 | `rasteratops-cloud-layout-test` | yes | `rclone-cloud-sync.md` | yes |
| 61 | `pixelelated-content-scope-test` | yes | `rclone-cloud-sync.md` | yes |
| 62 | `pixelelated-cloud-folder-test` | yes | `rclone-cloud-sync.md` | yes |
| 63 | `pixelelated-cloud-folder-vm-test` | yes | `generic-x64-vm-testing.md` | yes |
| 64 | `pixelelated-cloud-validator-test` | yes | `rclone-cloud-sync.md` | yes |
| 65 | `pixelelated-save-layout-test` | yes | `rclone-cloud-sync.md` | yes |
| 66 | `pixelelated-duckstation-capture-test` | yes | `packaging-and-patches.md`, `rclone-cloud-sync.md` | yes |
| 67 | `rasteratops-vm-cloud-epic` | yes | `generic-x64-vm-testing.md` | yes |
| 68 | `pixelelated-vm-cloud-boundaries` | yes | `generic-x64-vm-testing.md` | yes |
| 69 | `rasteratops-identity-check` | yes | `release-candidates.md` | yes |
| 70 | `rasteratops-candidate-store` | yes | `release-candidates.md` | yes |
| 71 | `council/` | yes | `adversarial-council.md` | yes |
| 72 | `pkgcheck` | yes | `packaging-and-patches.md` | yes |

<!-- tooltable: 72 rows; 0 with a missing tool or rule -->

**(3) The blindspot register's 74 entries.**
- 32 name a guard path in backticks, and every one exists at the hash.
- The other 42 are all numbered below 52, and state a practice or carry *The fix* rather than a path; `ceremony-check`'s guard rule starts at 52.
- No entry names a guard that is gone, so there is no dead row and no `Already written:` is owed.
- 29 is numbered twice (#811).

| Entry | Line | Form | Guard paths named (backticked `tools/`, `.githooks/`, `.claude/rules/`) | All exist at the hash |
| ---: | ---: | --- | --- | --- |
| 1 | 10 | table row | none named | n/a |
| 2 | 11 | table row | none named | n/a |
| 3 | 12 | table row | none named | n/a |
| 4 | 13 | table row | none named | n/a |
| 5 | 14 | table row | none named | n/a |
| 6 | 15 | table row | none named | n/a |
| 7 | 16 | table row | none named | n/a |
| 8 | 17 | table row | none named | n/a |
| 9 | 18 | table row | none named | n/a |
| 10 | 19 | table row | none named | n/a |
| 11 | 20 | table row | none named | n/a |
| 12 | 21 | table row | none named | n/a |
| 13 | 22 | table row | `tools/cloud-round-trip` | yes |
| 14 | 23 | table row | `.githooks/pre-push` | yes |
| 15 | 24 | table row | `tools/fork-worktree` | yes |
| 16 | 25 | table row | none named | n/a |
| 17 | 26 | table row | `tools/fork-publish-release` | yes |
| 18 | 27 | table row | none named | n/a |
| 19 | 28 | table row | none named | n/a |
| 20 | 29 | table row | none named | n/a |
| 21 | 30 | table row | none named | n/a |
| 22 | 31 | table row | none named | n/a |
| 23 | 32 | table row | none named | n/a |
| 24 | 33 | table row | none named | n/a |
| 25 | 34 | table row | none named | n/a |
| 26 | 35 | table row | `tools/fork-worktree` | yes |
| 27 | 36 | table row | none named | n/a |
| 28 | 37 | table row | none named | n/a |
| 29 | 38 | table row | none named | n/a |
| 29 | 40 | heading | none named | n/a |
| 30 | 60 | heading | none named | n/a |
| 31 | 81 | heading | none named | n/a |
| 32 | 104 | heading | none named | n/a |
| 33 | 134 | heading | none named | n/a |
| 34 | 169 | heading | `tools/last-good-scripts-test` | yes |
| 35 | 208 | heading | none named | n/a |
| 36 | 235 | heading | none named | n/a |
| 37 | 276 | heading | none named | n/a |
| 38 | 302 | heading | none named | n/a |
| 39 | 326 | heading | `tools/time-to-play`, `tools/vm-qa` | yes |
| 40 | 355 | heading | `tools/vm-qa` | yes |
| 41 | 378 | heading | none named | n/a |
| 42 | 399 | heading | none named | n/a |
| 43 | 422 | heading | `tools/last-good-scripts-test` | yes |
| 44 | 445 | heading | none named | n/a |
| 45 | 468 | heading | none named | n/a |
| 46 | 492 | heading | none named | n/a |
| 47 | 531 | heading | none named | n/a |
| 48 | 562 | heading | none named | n/a |
| 49 | 590 | heading | `tools/es-syntax-check` | yes |
| 50 | 613 | heading | none named | n/a |
| 51 | 636 | heading | none named | n/a |
| 52 | 662 | heading | `tools/archaeology`, `tools/work-log-index` | yes |
| 53 | 695 | heading | `tools/lint-audit-artifacts` | yes |
| 54 | 720 | heading | `tools/font-stems`, `tools/time-to-play` | yes |
| 55 | 753 | heading | `tools/time-to-play` | yes |
| 56 | 778 | heading | `tools/time-to-play`, `tools/vm-qa` | yes |
| 57 | 795 | heading | `tools/vm-qa` | yes |
| 58 | 817 | heading | `.claude/rules/device-builds.md` | yes |
| 59 | 844 | heading | `tools/signin-memory` | yes |
| 60 | 864 | heading | `tools/archaeology`, `tools/last-good-scripts-test` | yes |
| 61 | 892 | heading | `tools/last-good-scripts-test` | yes |
| 62 | 913 | heading | `tools/rc-preflight` | yes |
| 63 | 944 | heading | `tools/vm-qa` | yes |
| 64 | 971 | heading | `.claude/rules/engineering-practices.md` | yes |
| 65 | 997 | heading | `.claude/rules/vm-first.md` | yes |
| 66 | 1028 | heading | `tools/lint-audit-artifacts` | yes |
| 67 | 1050 | heading | `.githooks/pre-commit`, `.githooks/secret-patterns`, `tools/last-good-scripts-test` | yes |
| 68 | 1070 | heading | `tools/lint-audit-artifacts` | yes |
| 69 | 1092 | heading | `tools/last-good-scripts-test` | yes |
| 70 | 1113 | heading | `.githooks/pre-push`, `tools/pr-stack-check` | yes |
| 71 | 1138 | heading | `tools/cloud-test-backend`, `tools/last-good-scripts-test`, `tools/vm-qa` | yes |
| 72 | 1160 | heading | `tools/last-good-scripts-test` | yes |
| 73 | 1184 | heading | `tools/watch-build`, `tools/watch-job` | yes |

<!-- blindspots: 74 entries, numbers 1 to 73, used twice: [29]; entries naming a guard path 32 -->

**(4) The retired flows,** 15 mentions, each classed:

| Mention | Class |
| --- | --- |
| `council-substrate-integrity.md:15` | its source estate's path, named as the source: fine |
| `documentation-accuracy.md:38`, `:41`, `:53` | retired and said so (D-CLOUD-175; `rclonectl`, #6) |
| `es-player-text.md:295` | *historically* `cloud_migrate_layout`: said so |
| `fork-workflow.md:35`, `:36` | the Copilot leftovers the guard still watches: said so |
| `instruction-files.md:11`, `:12`, `:69` | `.github/instructions/` gone; *seeing it means a stale worktree*: said so |
| `instruction-files.md:156` | **`cloud-pair-migration` described as live** (F-18) |
| `rclone-cloud-sync.md:168`, `:200` | `rclonectl` *removed on 2026-07-23*: said so |
| `rclone-cloud-sync.md:827` | the historical block's opening: said so |
| `rclone-cloud-sync.md:833` | present tense inside that block (Q7 wording; the block is marked historical) |

**Already written** for the one dead row: as (2) above.


**(5) The friction entries no check reads:** 125 of 445 (F-02), listed by line.
- **The check names 0 owed**, because it cannot see these.
- **Read here:** 123 carry an issue number in their text, and the other 2 (lines 37, 38) carry a guard path.
- **Already written:** these entries were never gated, and none is ownerless today. Nothing on a device or in a cloud.

| Line | Date | Why the check skips it | Issue named in the text |
| ---: | --- | --- | --- |
| 31 | 2026-09-24 | `issue:` present in another shape | #264 |
| 34 | 2026-09-26 | no `issue:` field | #295 |
| 37 | 2026-09-27 | no `issue:` field | none |
| 38 | 2026-09-27 | no `issue:` field | none |
| 39 | 2026-09-27 | no `issue:` field | #298, #305, #306 |
| 42 | 2026-10-01 | no `issue:` field | #353 |
| 60 | 2026-10-02 | no `issue:` field | #375, #381 |
| 145 | 2026-10-04 | no `issue:` field | #383, #410 |
| 179 | 2026-10-05 | no `issue:` field | #422, #436 |
| 180 | 2026-10-05 | no `issue:` field | #422 |
| 182 | 2026-10-05 | no `issue:` field | #383 |
| 184 | 2026-10-05 | no `issue:` field | #383 |
| 186 | 2026-10-05 | no `issue:` field | #437 |
| 187 | 2026-10-05 | no `issue:` field | #438 |
| 189 | 2026-10-05 | no `issue:` field | #439 |
| 190 | 2026-10-05 | no `issue:` field | #440 |
| 192 | 2026-10-05 | no `issue:` field | #441 |
| 194 | 2026-10-05 | no `issue:` field | #442 |
| 196 | 2026-10-05 | no `issue:` field | #443 |
| 198 | 2026-10-05 | no `issue:` field | #444 |
| 200 | 2026-10-05 | no `issue:` field | #445 |
| 208 | 2026-10-05 | no `issue:` field | #448 |
| 210 | 2026-10-05 | no `issue:` field | #449 |
| 214 | 2026-10-05 | no `issue:` field | #451 |
| 216 | 2026-10-05 | no `issue:` field | #452 |
| 224 | 2026-10-06 | no `issue:` field | #383, #437 |
| 246 | 2026-10-06 | no `issue:` field | #383, #444 |
| 248 | 2026-10-06 | no `issue:` field | #352, #383, #467 |
| 252 | 2026-10-06 | no `issue:` field | #383, #395 |
| 254 | 2026-10-06 | no `issue:` field | #383 |
| 256 | 2026-10-06 | no `issue:` field | #383 |
| 258 | 2026-10-06 | no `issue:` field | #383, #395 |
| 260 | 2026-10-06 | no `issue:` field | #383 |
| 262 | 2026-10-06 | no `issue:` field | #470 |
| 264 | 2026-10-06 | no `issue:` field | #395, #467, #471 |
| 266 | 2026-10-06 | `issue:` present in another shape | #471 |
| 268 | 2026-10-06 | no `issue:` field | #471 |
| 270 | 2026-10-06 | no `issue:` field | #471 |
| 272 | 2026-10-06 | no `issue:` field | #471 |
| 276 | 2026-10-06 | no `issue:` field | #413, #472 |
| 278 | 2026-10-06 | no `issue:` field | #471 |
| 280 | 2026-10-06 | no `issue:` field | #471 |
| 282 | 2026-10-06 | no `issue:` field | #471 |
| 284 | 2026-10-06 | no `issue:` field | #471 |
| 286 | 2026-10-06 | no `issue:` field | #471 |
| 288 | 2026-10-06 | no `issue:` field | #471 |
| 290 | 2026-10-06 | no `issue:` field | #471 |
| 292 | 2026-10-06 | no `issue:` field | #467, #471 |
| 295 | 2026-10-06 | no `issue:` field | #471 |
| 296 | 2026-10-06 | no `issue:` field | #468, #471 |
| 298 | 2026-10-06 | no `issue:` field | #471, #473 |
| 300 | 2026-10-06 | no `issue:` field | #468, #471, #473 |
| 302 | 2026-10-06 | no `issue:` field | #471, #474 |
| 304 | 2026-10-06 | no `issue:` field | #471, #475 |
| 306 | 2026-10-06 | no `issue:` field | #471, #476 |
| 308 | 2026-10-06 | no `issue:` field | #471, #477 |
| 310 | 2026-10-06 | no `issue:` field | #478 |
| 312 | 2026-10-06 | no `issue:` field | #479 |
| 314 | 2026-10-06 | no `issue:` field | #479, #480 |
| 336 | 2026-10-07 | no `issue:` field | #471 |
| 342 | 2026-10-07 | no `issue:` field | #461 |
| 344 | 2026-10-07 | no `issue:` field | #471, #489 |
| 346 | 2026-10-07 | no `issue:` field | #490 |
| 348 | 2026-10-07 | no `issue:` field | #493 |
| 362 | 2026-10-07 | no `issue:` field | #499 |
| 443 | 2026-10-08 | no `issue:` field | #527 |
| 457 | 2026-10-08 | `issue:` present in another shape | #519 |
| 458 | 2026-10-08 | `issue:` present in another shape | #519 |
| 507 | 2026-10-11 | no `issue:` field | #537 |
| 510 | 2026-10-11 | no `issue:` field | #537 |
| 514 | 2026-10-11 | `issue:` present in another shape | #539 |
| 515 | 2026-10-11 | `issue:` present in another shape | #537 |
| 517 | 2026-10-11 | `issue:` present in another shape | #540 |
| 536 | 2026-10-11 | no `issue:` field | #540 |
| 575 | 2026-10-11 | no `issue:` field | #548 |
| 595 | 2026-10-12 | no `issue:` field | #493, #528 |
| 613 | 2026-10-12 | `issue:` present in another shape | #569 |
| 631 | 2026-10-13 | no `issue:` field | #570 |
| 651 | 2026-10-13 | `issue:` present in another shape | #565 |
| 677 | 2026-10-14 | no `issue:` field | #581 |
| 678 | 2026-10-14 | no `issue:` field | #567 |
| 679 | 2026-10-14 | no `issue:` field | #575 |
| 681 | 2026-10-14 | no `issue:` field | #583 |
| 682 | 2026-10-14 | no `issue:` field | #584 |
| 683 | 2026-10-14 | no `issue:` field | #574, #582 |
| 685 | 2026-10-14 | no `issue:` field | #585 |
| 687 | 2026-10-14 | no `issue:` field | #558, #566 |
| 689 | 2026-10-14 | no `issue:` field | #566 |
| 691 | 2026-10-14 | no `issue:` field | #574 |
| 692 | 2026-10-14 | no `issue:` field | #583 |
| 694 | 2026-10-14 | no `issue:` field | #574 |
| 695 | 2026-10-14 | no `issue:` field | #582, #584 |
| 697 | 2026-10-14 | no `issue:` field | #574 |
| 699 | 2026-10-14 | no `issue:` field | #574 |
| 701 | 2026-10-14 | no `issue:` field | #493, #582 |
| 703 | 2026-10-14 | no `issue:` field | #583 |
| 708 | 2026-10-14 | no `issue:` field | #574, #583 |
| 714 | 2026-10-14 | no `issue:` field | #581 |
| 715 | 2026-10-14 | no `issue:` field | #583 |
| 716 | 2026-10-14 | no `issue:` field | #588 |
| 717 | 2026-10-14 | no `issue:` field | #563 |
| 727 | 2026-10-14 | no `issue:` field | #566 |
| 729 | 2026-10-14 | no `issue:` field | #566 |
| 731 | 2026-10-14 | no `issue:` field | #566 |
| 733 | 2026-10-14 | no `issue:` field | #493, #566 |
| 738 | 2026-10-14 | no `issue:` field | #565 |
| 740 | 2026-10-14 | no `issue:` field | #565, #567 |
| 742 | 2026-10-14 | no `issue:` field | #567 |
| 744 | 2026-10-14 | no `issue:` field | #572 |
| 745 | 2026-10-14 | no `issue:` field | #565, #566, #567 |
| 753 | 2026-10-15 | no `issue:` field | #592 |
| 755 | 2026-10-15 | no `issue:` field | #581 |
| 757 | 2026-10-15 | no `issue:` field | #595 |
| 759 | 2026-10-15 | no `issue:` field | #594 |
| 761 | 2026-10-15 | no `issue:` field | #596 |
| 762 | 2026-10-15 | no `issue:` field | #594 |
| 763 | 2026-10-15 | no `issue:` field | #493 |
| 765 | 2026-10-15 | no `issue:` field | #597 |
| 767 | 2026-10-15 | no `issue:` field | #597 |
| 769 | 2026-10-15 | no `issue:` field | #596 |
| 784 | 2026-10-15 | no `issue:` field | #367 |
| 786 | 2026-10-15 | no `issue:` field | #493, #602 |
| 788 | 2026-10-15 | no `issue:` field | #555, #599, #600, #602 |
| 802 | 2026-10-15 | no `issue:` field | #528, #604 |
| 847 | 2026-10-16 | no `issue:` field | #616 |

<!-- friction: 445 dated entries; 125 never seen by the check's matcher -->

### Q7 Clarity and structure

**The duplicates, with their differences.** The duplicated fact is in the left column. Each finding says which copy is right.

| Fact | Copy 1 | Copy 2 | The difference |
| --- | --- | --- | --- |
| the VM's *no* | `CLAUDE.md:188-190` (a panel, a board's memory, a battery, a GPU path; D-QA-007/017) | `AGENTS.md:208-210` (a radio, a battery, a board's boot, a panel, a tailnet; D-QA-007/033) | different examples, different second ID (F-01) |
| the device questions | `CLAUDE.md:105-107` (none) | `AGENTS.md:105` (the copy and the reboot each need a yes) | one omits D-QA-011 (F-01) |
| `mkimage`'s environment | `CLAUDE.md:88` | `AGENTS.md:86` | same, and both wrong (F-03) |
| the vocabulary check | `CLAUDE.md:185` | `AGENTS.md:309` | same, and both wrong (F-04) |
| the interface-law documents | `CLAUDE.md:34`, `AGENTS.md:31` (two) | `instruction-files.md:122` (three) | count (F-09) |
| the build commands | `CLAUDE.md:65-89` | `AGENTS.md:63-87` | byte-identical (`diff` of the two ranges), F-08's comment included |
| the five-backend table | `rclone-cloud-sync.md:548-561` | `generic-x64-vm-testing.md:582-586` | the reader's lead (same ports), not re-verified here |
| busybox's missing tools | `rclone-cloud-sync.md:723-728` | `generic-x64-vm-testing.md:540-553`, `engineering-practices.md` § Guards must fail closed | three phrasings (the reader's comparison); one names a wrong applet (F-13, re-read) |

**One responsibility per file:** `generic-x64-vm-testing.md`, `rclone-cloud-sync.md` and `engineering-practices.md` (F-27). Dated narrative inside instructions is where five of F-11 to F-16's sentences went stale unseen.

**Headings `tools/archaeology` can find:** the rules' headings name their subject. The registers' rows name theirs by ID.


## Instruction File Recommendations

The epic tier runs this mode. For this slice the recommendations *are* the punch list's streams (brief § 9). Each is a proposal for the coordinator, with its ladder rung; nothing is applied here (D-WORKFLOW-189).

### Coverage Gaps (would-have-prevented)

- **A rule that names a tool's behaviour states the tool's line it read** (F-12, F-15, F-16, F-21: four of the five facts that moved were sentences about a tool's options or defaults). The ladder's next rung for each is the tool's own `--help` cited in the sentence, so a reader checks one line.
- **A reversal row's sweep** (`decision-register.md` § A reversal ... sweeps its old words) was not run for D-CLOUD-130 (F-10) or D-CLOUD-175's tool row (F-18). The rule exists; the sweep is by hand.

### Codification Gaps (needs-new-rule)

None: every shape here is covered by a rule that exists. The gaps are tools, where the ladder says a rule broken twice should go:
- `rules-check`: a `twins` subset (F-01), the index's tool-to-rule direction (F-22), and the principles count (F-06);
- `ceremony-check`: every dated friction line as an entry (F-02);
- `register-check`: the open table's columns and escaped pipes (F-23);
- a superseded-citation check from `t4-q4.py`'s draft (F-10, F-18).

### Recommended Action Sequence

1. The bugs whose criterion is a tool's check: F-02 (`ceremony-check`), then F-01 and F-22 (`rules-check`).
2. The Medium sentences: F-10 and F-11.
3. One stream per file for the Low wording, in the merge's order, each naming its paragraphs by heading and first words (A7).
4. The legacy paths with #640.
5. #645's facts into `fork-workflow.md`, when #645 has them.

## Second opinion (Phase 4.6)

**Not applicable at Local depth** (plan § 6c, *a doctrine read*; D-WORKFLOW-184). `second-opinions/review-plan.json` records `depth: local`, `reviewers: []`, `tier_exception: D-WORKFLOW-184` and the reason. No reviewer and no Facilitator call. Phase 4.5 above was done in full.

The four readers of stage B were read-only subagents of this session's lab (brief § 5 rule 5): their reports were leads, never a second opinion.

## Quality Self-Check

- **Every count in this folder comes from a command** whose output file is under `.qa-scratch/t4/` and whose command is in `02`. The generated tables assert their rows (`t4-coverage.py` 36, `t4-blocks.py` 56) and refuse empty cells.
- **Corrected while writing, before commit:**
  - the friction list on cut lines (27 to 2);
  - *120 entries* (counted: 100);
  - the open table's cells;
  - the block rows inflating criterion 7's grep;
  - the superseded count (2 to 3, once `instruction-files.md:156` was classed);
  - the blindspot guard count (33 to 32, a separator row counted);
  - `generic-x64-vm-testing.md`'s reach (7 to 11 areas);
  - the absent-path split (9 and 4 to 8 and 5);
  - *eleven* Q3 findings (13).

  Stage B's commit message says *eleven bug candidates*; the running log records that the count is 13.
- **The readers' leads used are re-read; the rest are listed unverified** (`02` § Leads).
- **Not checked, said so:**
  - whether each superseded candidate's successor is itself superseded beyond one step: the review reads one;
  - the ES repository's pointers;
  - the tools' correctness beyond what a rule claims.
