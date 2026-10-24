# Research notes — M6.P2 T4, the binding doctrine (#651)

## Scope

**Read hash:** `8ebaf8daad8eaac6331dff6fc048fb4411d7decb` (`next`).
- **The branch at stage A** is `00e75ab135`, the dispatch's. The read is made on the hash's bytes, from `.qa-scratch/t4/at-hash/` (`git archive 8ebaf8daad <the globs>`, 36 files), and every line number in these artifacts is the hash's unless marked *branch*.
- **`upstream/next` at the read** is `481c9d0d75`. It is not compared: the doctrine is fork-own, and ROCKNIX carries none of it.

**The filter** (brief § 2, run with `python3 -I` over `docs/reviews/inventory.json`, whose header names P1's `eb4763e3cc`): the rows with `tree == distribution` and `area == doctrine`, under `.claude/rules/**`, `CLAUDE.md`, `AGENTS.md`, `NAMING.md` and `docs/{decision-register,blindspot-register,friction-log}.md`. Output, 14:34 UTC:

```
paths 36 lines 11414 {'fork-own': 36} {'markdown': 36} {'n/a': 36}
```

These are the brief's and #651's figures: **36 paths; 11,414 lines in the inventory at `eb4763e3cc`; 11,394 at `8ebaf8daad`**. The second figure was taken two ways that agree:
- `git diff --numstat <empty tree> 8ebaf8daad -- <the globs>` summed;
- `cat` of the 36 read-tree files into `wc -l`.

All 36 paths are fork-own, `markdown` and `reach: n/a`. The inventory's path set equals the tree's at the hash (`cmp` of the two sorted lists). **No delta.**

**The 36, by size at the hash:**

| Lines | Path |
| ---: | --- |
| 1,398 | `generic-x64-vm-testing.md` |
| 1,198 | `docs/blindspot-register.md` |
| 895 | `rclone-cloud-sync.md` |
| 863 | `docs/friction-log.md` |
| 836 | `engineering-practices.md` |
| 738 | `docs/decision-register.md` |
| 695 | `device-builds.md` |
| 423 | `es-native-ui.md` |
| 351 | `AGENTS.md` |
| 343 | `es-player-text.md` |
| 315 | `es-ui-style-guide.md` |
| 254 | `es-code-traps.md` |
| 254 | `worktrees.md` |
| 253 | `council-substrate-integrity.md` |
| 225 | `upgrade-and-install.md` |
| 224 | `instruction-files.md` |
| 208 | `issue-tracking.md` |
| 202 | `CLAUDE.md` |
| 191 | `fork-workflow.md` |
| 154 | `release-candidates.md` |
| 127 | `milestone-phase-naming.md` |
| 124 | `adversarial-council.md` |
| 116 | `ceremonies.md` |
| 114 | `handheld-evidence.md` |
| 113 | `packaging-and-patches.md` |
| 106 | `working-principles.md` |
| 99 | `decision-register.md` |
| 91 | `bugs-are-agent-first.md` |
| 91 | `learning-capture.md` |
| 82 | `vm-first.md` |
| 68 | `player-language.md` |
| 61 | `documentation-accuracy.md` |
| 60 | `NAMING.md` |
| 55 | `time-to-play.md` |
| 47 | `change-log.md` |
| 40 | `least-surprise.md` |

The rows above are the inventory's per-path figures. Three differ from the hash: the friction log (863 in the inventory), the decision register (738) and `instruction-files.md` (224) are the inventory's at `eb4763e3cc`, and the 20-line difference is in those three. At the hash they are 856, 728 and 221, the brief's figures. Every other file's count is the same at both; the per-file `wc -l` of the read tree is `.qa-scratch/t4/hash-lines.txt`, and it sums to 11,394.

**What loads every session.** Each rule's front matter was read at the hash and its `paths:` block parsed whole (not by `grep -A`; `.qa-scratch/t4/loads.txt`):

| Rules | Count | Lines |
| --- | ---: | ---: |
| no `paths:` key | 7 | 606 |
| `paths: "**"` | 17 | 4,573 |
| scoped | 6 | 2,820 |

- **No `paths:` key:** `bugs-are-agent-first`, `ceremonies`, `least-surprise`, `player-language`, `release-candidates`, `time-to-play`, `vm-first`.
- **Scoped:** `change-log`, `council-substrate-integrity`, `generic-x64-vm-testing`, `handheld-evidence`, `packaging-and-patches`, `rclone-cloud-sync`.

So **24 of 30 rules and 5,179 lines** load at every Claude Code session's start, plus `CLAUDE.md`'s 202. Crush loads all 30. **No delta.**

**The branch's doctrine deltas from the hash, hunk by hunk** (`git diff 8ebaf8daad 00e75ab135 -- <the 36>`: 8 files, +130/-3):

| File | Hunk (at the hash, then the branch) | What | Owner |
| --- | --- | --- | --- |
| `.claude/rules/device-builds.md` | `@@ -182,0 +183,9` | § After rebasing item 3: read every field (`PKG_SHA256`, `PKG_URL`, `PKG_ARCH`) per plan through `config/options` (`libfmt`, #877; `btrfs-progs`, #879) | coordinator, `764d30ed2e` (T7's retro) |
| `.claude/rules/engineering-practices.md` | `@@ -239,0 +240,10` | § A name is not a behaviour: a count, a line number or a hash is a claim about one tree; a hash is copied, never completed from a prefix (blindspot 75's guard) | coordinator, `ab8f750784`, extended in `e09b57d16c` |
| `.claude/rules/fork-workflow.md` | `@@ -33 +33` | the personal-paths list gains `tools/renovation-inventory`, `-drift` and `-status` | P1, `9966dbcd12`, `af24589b1c` |
| `.claude/rules/generic-x64-vm-testing.md` | `@@ -1224,0 +1225,7` | a run meant to measure the tree's scripts binds them from an autostart hook and reads the installed hash; #797 | coordinator, `8c9b1d4721` (T1's retro) |
| `.claude/rules/instruction-files.md` | `@@ -188 +188`, `@@ -194,0 +195,3` | the `lint-audit-artifacts` row names the renovation face; three rows for the renovation tools | P1, `9966dbcd12`, `af24589b1c`, `fc88815ccb` |
| `docs/blindspot-register.md` | `@@ -1198,0 +1199,52` | entries **74** (a fixture that did not engage), **75** (a corpus read on the wrong tree) and **76** (a merge chain that does not stop on its own check), appended | coordinator, `179093ffd6`, `ab8f750784`, `0921782112`, `1b8ac30421` |
| `docs/decision-register.md` | `@@ -711,0 +712,21` (decided rows), `@@ -717,0 +739,2` (open rows), `@@ -723 +746` | 21 rows appended to `## Decided`: D-WORKFLOW-181 to 190 and 192 to 199, D-INFRA-025 to 027. 2 appended to `## Open decisions`: D-WORKFLOW-191, D-SYS-014. **One row changed in place**: D-QA-040, in the open table, gained an `**Open:**` prefix | the coordinator and P1 (25 commits, `0bfd387f7b` to `e3897db16d`); D-QA-040's prefix is `f00ab3e163` (#646) |
| `docs/friction-log.md` | `@@ -856,0 +857,23` | 23 lines appended | the coordinator and the lanes (25 commits) |

**D-QA-040**, for stage B:
- **What changed:** `f00ab3e163` (*ten decided rows moved from under Open decisions into the Decided table; register-check refuses a statement row there*, #646) moved those rows with their text unchanged, and added `**Open:**` to D-QA-040, *"a genuine open question written as a statement"*. The row is in `## Open decisions` at both the hash (table at line 713) and the branch (line 734).
- **What the contract says:** `decision-register.md` makes **decided** rows append-only. An open row's settlement is a move with its ID kept. Nothing is said of a marker added to an open row.
- That is a Q2 lead, not a stop.

**The branch scan** (brief § 2's predicate: a branch is ahead when `git log next..<branch> -- <the 36>` prints a line; `.qa-scratch/t4/branch-scan.txt`):
- **20 of 70 `origin/` refs are ahead.** Every M6 lane branch is ahead, as expected: the lanes append to the registers and inherit P1's and the coordinator's rule edits by merge.
- **Rule edits outside those two histories** (`git rev-list --no-merges next..<b> -- <rules>` less the commits of `feature/m6-renovation-plan-346` and `feature/m6-p1-survey-641`; `.qa-scratch/t4/branch-scan-own.txt`):

| Branch | Commit | Files | Standing |
| --- | --- | --- | --- |
| `feature/m6-es-launch-path-649` (T2, accepted) | `11a2ee182f` 2026-10-23 | `es-native-ui.md` +5/-1 | the coordinator's by acceptance; it reaches this branch at the merge. The brief calls it `f16cf7fc28`, which is T2's tip, not the edit's commit |
| `feature/m7-manual-cloud-folders` | `e484380a34` 2026-10-07 | `fork-workflow.md`, `instruction-files.md` | the M7 lane's, not in `next` |
| `feature/conflict-resolution` | 36 commits, tip 2026-10-07 | many rules | a pre-renovation branch; a Q6 lead (a stale branch carrying doctrine `next` lacks) |
| `x64-build-fix` | 3 commits, 2025-10-22 | `CLAUDE.md` | the same |
| `verification-anchors/2026-09-30-rasteratops-fork-plan`, `-r2` | 1 each, 2026-09-30 | many rules | the same; anchors by name |

**No unaccepted M6 lane carries a rule edit of its own** (D-WORKFLOW-189 holds).
- **The M7 lane's register rows 171 to 180** are in its legacy checkout, on no fetched ref (brief § 2), and are read only when a new row's ID is chosen.

**Interacting subsystems (read-only context):**
- the four doctrine tools: `tools/rules-check`, `tools/register-check`, `tools/ceremony-check`, `tools/forbidden-terms-check`;
- `tools/archaeology`, `tools/box-check`, `.githooks/`;
- `docs/reviews/cross-reference.md` § Doctrine to area;
- the other slices' briefs and retros (their stale-facts lines);
- `docs/reviews/build-path-read.md` (#644);
- the code-auditor and mini-retro skills (T38's);
- `docs/es-menu-map.md` and `docs/conflict-wizard-ia.md` (T39's), which load nowhere.

## The reader's pass

**How the 36 were read, said plainly.**
- **This session's own pass, 25 files.** Twenty-three rules and `CLAUDE.md` were loaded into this session whole, from T3's worktree, and `cmp` shows each is byte-identical to the hash's file. Two more, `fork-workflow.md` and `instruction-files.md`, were loaded with P1's hunks on top: the hash's text is the loaded text less those listed hunks.
- **Four readers with no context, 11 files.** Brief § 5's method, read-only subagents given one group each, read the files that were not loaded: `generic-x64-vm-testing.md`; `rclone-cloud-sync.md`, `handheld-evidence.md`, `packaging-and-patches.md` and `change-log.md`; `AGENTS.md`, `NAMING.md` and `council-substrate-integrity.md`; and the three registers. Each was given the at-hash file.
- **The readers' reports are leads** (rule 5). Every item below that became a finding was re-read by this lane at the hash, with the command in `02` § Mechanical checks or § Findings. Their items left unverified are not findings.

One line per file: what a stranger stumbled on, before any auditing.

| File | What a stranger stumbled on |
| --- | --- |
| `CLAUDE.md` | :27 says *the four principles* and lists five; :34 says *Two more documents* carry interface law, where `instruction-files.md:122` says three; :88's `mkimage` *needs OS_VERSION/BUILD_DATE exported* (#644 f14) |
| `AGENTS.md` | (reader) :19-20 says both entry files *carry the same facts and are kept equal by `tools/rules-check`*, which the tool does not do; the two differ in their VM examples, the deploy questions and a dozen bullets only one carries |
| `NAMING.md` | (reader) titled *Identity classification, version 2 (#409)*, not by the file's name; *RC2*, *P0 sweep* and *FIX* are used undefined; :36-37 is time-bound (#416) |
| `adversarial-council.md` | *the two milestone passes are calls, not extra seats* needs the code-auditor reference to parse; the length-is-not-quality section is long for the seats it now concerns |
| `bugs-are-agent-first.md` | clear; the three classes and their labels read in one pass |
| `ceremonies.md` | the table says a friction entry without an issue *refuses a push of next*; a reader assumes every entry is read, and nothing says the shape the check needs (it skips 125, `02` F-02) |
| `change-log.md` | (reader) :41 cites *`es-native-ui.md` § Conventions*, a section that moved to `es-player-text.md` (the old heading's note redirects) |
| `council-substrate-integrity.md` | (reader) adopted from another estate: it names three lint scripts, `ci.yml`, `.pre-commit-config.yaml`, `.prettierignore`, `.stale-blob-allowlist` and two `.instructions.md` files that this tree does not have; *Brake #2* is undefined; issue numbers belong to another tracker |
| `decision-register.md` (rule) | clear; § Read it when is long, and its *before putting anything to the maintainer* bullet reads as a second contract |
| `device-builds.md` | § Iterating on EmulationStation names `~/Development/emulationstation-next` with `origin` `maxengel/emulationstation-next`; the checkout's `origin` is now `pixelelated/emulationstation`; seven legacy-path lines (#640) |
| `documentation-accuracy.md` | clear; its drift list is dated and says so |
| `engineering-practices.md` | 836 lines, a dozen sections from the fork's lanes to editing a running shell tool; the reader must search, not scan |
| `es-code-traps.md` | :182 *`/var/log/es_log.txt` is tmpfs, so a proof script's closing reboot wipes it*, which `generic-x64-vm-testing.md:279` and `var-log.mount` contradict |
| `es-native-ui.md` | long; the surface-tier table and the D-UI-078/093/095 paragraphs interleave, so the rule and its history are hard to tell apart |
| `es-player-text.md` | the outcome-vocabulary section carries a dated list of every sentence proposed since 2026-09-10; a reader looking for *which words are current* reads history |
| `es-ui-style-guide.md` | clear; *Known inconsistencies* is useful and says so |
| `fork-workflow.md` | :62's `gh pr create ... --head maxengel:pr/<name>` against an `origin` of `pixelelated/distribution`; the fork-only tools list is one line of 100 backticked entries (:33) |
| `generic-x64-vm-testing.md` | (reader) 1,398 lines, about 40 % dated incident narrative; :103 *SSH is off* then :124 *disabled but running*; the headless comment at :109-111 describes the pre-virgl default; terms used before their definition (*guest d*, *cell*, *LINK5*) |
| `handheld-evidence.md` | (reader) § A maintenance mask is not necessarily a boot barrier sits under § Testing it on the VM; `rocknix-evidence collect` names no path |
| `instruction-files.md` | the tool table's *Detail in* column points 31 of its 85 tool-to-rule pairs at a rule that never names the tool; :156 describes the retired `cloud-pair-migration` as current |
| `issue-tracking.md` | the *No work without an issue* section carries the 2026-10-02 counts (*17 of 29 rules stale*), which read as current |
| `learning-capture.md` | clear; § 4's stash rule names the canonical file the M7 lane owns |
| `least-surprise.md` | :18-20 cites only D-CLOUD-109 for what a launch does to a sync, where D-CLOUD-130 decides it |
| `milestone-phase-naming.md` | clear; the sub-id letters are a closed set and say so |
| `packaging-and-patches.md` | (reader) :66 and :106 name `build.ROCKNIX-<DEVICE>.<ARCH>`, where the roots are `build.pixelelated-*`; the `zip` case reads as present until *Upstream deleted* is noticed |
| `player-language.md` | clear |
| `rclone-cloud-sync.md` | (reader) :126-128 *no `PKG_SHA256`*, :616 *ships 1.74.4*, :77 *`backup/*.zip`*, :374 *the exit-4 timing* -- each true once, none now; :79-82 *ROMs and BIOS are never uploaded* against the content tier at :705 |
| `release-candidates.md` | long step 0; *An open bug is accepted only on a code trace* is a contract inside a step |
| `time-to-play.md` | :31-35 says D-CLOUD-076 *ships today* and D-CLOUD-109 replaces it; D-CLOUD-130 is not named, and the code ships it (T2) |
| `upgrade-and-install.md` | clear; § Current cloud setup policy is the newest section and reads as an addendum |
| `vm-first.md` | clear |
| `working-principles.md` | clear; the ladder is the one test this slice uses |
| `worktrees.md` | the layout diagram and seven lines name the legacy `rocknix.worktrees/` (#640) |
| `docs/blindspot-register.md` | (reader) three entry formats (table, *The fix*, *Guard:*) with no note on where each starts; 29 numbered twice (#811); entry 52's guard in prose |
| `docs/decision-register.md` | (reader) the area prefixes are never listed; the open table's header has three columns and seven rows carry four; *Settled by ... moved from the open table* and the retired-ID rows are unexplained |
| `docs/friction-log.md` | (reader) six prose blocks inside `## Entries` break the one-line promise; the documented field order drifts after 2026-10-02 |

## Phase 1: what the record already says

**The closed bugs** naming a doctrine file:
- **The command:** `gh issue list --repo pixelelated/distribution --label bug --state closed --limit 500 --json number,title,body` (139 closed bugs, 14:53 UTC), grepped with the pattern `\.claude/rules/|\b(<the 30 rule names>)\.md\b|CLAUDE\.md|AGENTS\.md|NAMING\.md`.
- **The result: 30 bugs**, #49, #119, #141, #143, #144, #145, #160, #161, #178, #182, #205, #206, #221, #226, #246, #248, #274, #275, #279, #283, #288, #305, #306, #315, #320, #325, #327, #366, #370 and #416.
- These are provenance only: they are where a rule was cited or changed in a fix, not a verdict on the rule.

**The prior audits** touching the doctrine:
- **The command:** `for f in docs/audits/*/05-punch-list.md; do grep -c -E '\.claude/rules/|CLAUDE\.md|AGENTS\.md|decision-register|blindspot-register|friction-log' "$f"; done` over the 20 punch lists in this tree. `2026_09_10-graceful-degradation/` has none.
- **The result: 7 of the 20 have a hit:**

| Audit | Hits |
| --- | ---: |
| `2026_09_06-issue-device-flashing-runbook` | 19 |
| `2026_09_13-milestone-stable-before-upstream` | 14 |
| `2026_09_12-milestone-cloud-saves-since-60` | 11 |
| `2026_09_24-milestone-rc-round-since-186` | 7 |
| `2026_09_28-milestone-audit-of-the-fixes-307` | 4 |
| `2026_09_28-milestone-audit-of-the-fix-round` | 4 |
| `2026_09_14-epic-offline-retroachievements` | 2 |

- Read as provenance after this slice's Phase 2 (plan § 7 item 3), never transcribed.

**The other briefs' stale-facts lines** (`grep -n -i 'stale facts' docs/reviews/briefs/*.md`, 8 briefs). Each is a doctrine finding a lane already paid for:

| Fact | Named in | This slice's reading | Owner |
| --- | --- | --- | --- |
| The legacy paths (`/workspace/repos/rocknix`, `rocknix.worktrees/`) | T1, T2, T3, T5, T8, T24, T30, P1 | 8 files (`02` § Mechanical checks): `worktrees.md` 7, `device-builds.md` 7, `fork-workflow.md` 3, `instruction-files.md` 2, `AGENTS.md` 2, `CLAUDE.md` 1, `es-code-traps.md` 1, `generic-x64-vm-testing.md` 1 | #640 |
| `CLAUDE.md`'s *needs OS_VERSION/BUILD_DATE exported* | T5 (#644 f14) | true of `AGENTS.md:86` too; `distributions/ROCKNIX/version:8` assigns `OS_VERSION` unconditionally after any export (`config/options:42`), and `distributions/ROCKNIX/options:212` defaults `BUILD_DATE` | this slice (F-03) |
| `device-builds.md` § Iterating on EmulationStation names an old `origin` | P1 | the checkout's `origin` is `pixelelated/emulationstation`; `rocknixfork` is still `maxengel/emulationstation-next-rocknix`; `fork-workflow.md:62`'s `--head maxengel:` is the same shape | this slice (F-19) |
| `tools/fork-worktree`'s hint prints the legacy path | T1, P1 | a tool, not a rule | #640 |
| `tools/es-syntax-check`'s default root | T2 | a tool | #699 |
| `tools/retroarch-wrapper-test`'s default roots | T3 | a tool | #799 |
| the ES pointers' `/workspace/repos/rocknix` | T2 | the ES repository's `AGENTS.md`/`CLAUDE.md`, outside the 36 | #640 |
| `device-builds.md` § Our devices is current | T1, P1 | agreed | -- |
