# Forward Audit — M6.P2 T4, the binding doctrine

## Running Notes

- **What this is.** A read of the 36 files every session obeys: the 30 rules, `CLAUDE.md`, `AGENTS.md`, `NAMING.md` and the three registers.
  - The read is at `8ebaf8daad`'s bytes (`.qa-scratch/t4/at-hash/`).
  - The branch's deltas from the hash are `01` § Scope's.
  - No file of the 36 is edited at stage B; each session ends with `git status --short -- <the 36>` empty (`00`).
- **The bench is the tree, the tools and the register.** Can this be done on the VM? **No, for nearly all of it** (brief § 5). The few guest-shaped sentences (the `/var/log` bind, `realpath`, the ES units) were settled from the source tree and the GENERIC_X64 install tree, read by `ls` and `grep`, so no guest ran.
- **Phase 2's criteria are #651's sixteen** (= brief § 7), entered at the end of this file.
- **The readers.** Four read-only readers with no context read 11 of the 36 (`01` § The reader's pass). Every finding below that came from a reader was re-read by this lane, and its command is in the finding.

## Mechanical checks (brief § 5)

Each check: the command as run (from the worktree root; `S=.qa-scratch/t4`), its exit status, and its summary line.

| Check | Command | Exit | Summary |
| --- | --- | --- | --- |
| `tools/rules-check` | `"$D/tools/rules-check" > $S/rules-check.out` (14:39) | 0 | 44 `ok` lines and the summary `rules-check: 30 rule files, every one front-mattered and indexed` |
| `tools/register-check` | `"$D/tools/register-check"` (14:39) | 0 | `667 IDs, each once; every citation in the live documents names a row` (the branch's; the brief's 660 was an earlier branch) |
| `tools/ceremony-check` | `"$D/tools/ceremony-check"` (14:39) | 1 | one `DUE weekly OVERDUE: 2026-W42 summary missing` (M7's week); `friction`, `guards`, `checkboxes` (box-check: 300 issues, 809 open, 0 fail), `rules`, `register`, `index`, `retro`, `audit`, `futro`, `hygiene` all `ok` |
| `tools/forbidden-terms-check` | `"$D/tools/forbidden-terms-check"` (14:42) | 0 | `0 hits in 133406 tracked files`; the wordlist itself not read |
| `.githooks/hooks-test` | `"$D/.githooks/hooks-test"` (14:42) | 0 | `PASS` |
| `tools/box-check` | `"$D/tools/box-check"` (14:42; `rate_limit` 4,390 before and after) | 0 | `box-check: 300 issue(s), 809 open checkbox(es), 0 fail, 30 issue(s) with rows to re-derive against` |
| the `paths:` globs | brief § 5's loop at the branch; the same globs matched against `git ls-tree -r --name-only 8ebaf8daad` at the hash (`t4-q6.py rules`) | 0 | 57 globs over 23 rules (7 rules have no `paths:`); **one glob matches nothing at both: `council-substrate-integrity.md`'s `research/council-research/**`**; counts differ between hash and branch only by tree size |
| the cited IDs | `grep -ohE 'D-[A-Z]+-[0-9]+' <the 33 at the hash> \| sort -u \| wc -l` | 0 | **181**; `t4-q4.py ids`: 178 in `## Decided`, 3 in `## Open decisions`, 0 absent |
| the tool table | brief § 5's loop over the at-hash `instruction-files.md`, plus `git cat-file -e 8ebaf8daad:tools/<t>` | 0 | 72 rows (first tool of each), none missing at the hash or on the branch; `t4-q6.py tooltable`: every tool and every rule a row names exists |
| the legacy paths | `grep -c 'repos/rocknix\|rocknix\.worktrees' <the 33 at the hash>` | 0 | 8 files: `worktrees.md` 7, `device-builds.md` 7, `fork-workflow.md` 3, `instruction-files.md` 2, `AGENTS.md` 2, `CLAUDE.md` 1, `es-code-traps.md` 1, `generic-x64-vm-testing.md` 1 -- the brief's eight, #640's |
| the friction matcher | `ceremony-check`'s friction regex lifted from `git show 8ebaf8daad:tools/ceremony-check` (line 250) and applied to the at-hash log (`t4-q6.py friction`) | 0 | 445 dated entries; **125 never matched**, so the check counts them neither as owed nor as covered (116 have no `issue:` field, 9 another shape). Of the 125, 2 name no issue anywhere (lines 37, 38), and both name a guard path. F-02 |
| the blindspot guards | `t4-q6.py blindspots` | 0 | 74 entries numbered 1 to 73, **29 used twice** (#811); 33 name a guard path in backticks, every one existing at the hash. `ceremony-check`'s `guards` line covers 52 on |
| the retired flows | `t4-q6.py retired` (`cloud_migrate_layout`, join/follow, `rclonectl`, `.github/instructions`, Copilot) | 0 | 15 mentions: 13 say the thing is retired; `instruction-files.md:156` describes the retired `cloud-pair-migration` as current (F-18); `rclone-cloud-sync.md:833` is present tense inside the historical block :827 opens (Q7) |
| the superseded citations | `t4-q4.py ids` (a later row citing the ID with a reversal word), narrowed to a reversal word within 80 characters of the ID (34 IDs), then each successor row's sentence read | 0 | 45 citations in a file that does not cite the successor; read one by one, **2 cite a superseded row as current**: `time-to-play.md:32,42` and `least-surprise.md:19` (D-CLOUD-109, reversed for launches by D-CLOUD-130; F-10); the rest refine, confirm or merely cite (D-QA-017 *refines* D-QA-007; D-QA-030 *not D-QA-011*; D-RA-025 *confirms* D-INFRA-010) |
| `tools/vm-qa` suites | -- | -- | none of `vm-qa`'s suites reads the doctrine; recorded, not run |
| the closed bugs | `gh issue list --label bug --state closed --limit 500` grepped (`01` § Phase 1) | 0 | 139 closed, 30 name a doctrine file |
| the command blocks | `t4-blocks.py` (below) | 0 | 56 blocks: 7 ran and passed, 13 not commands, 35 checked for their tools and options or not runnable here with the reason, 1 checked wrong (7 + 13 + 35 + 1 = 56) (`council-substrate-integrity.md:75`) |

## The four #644 findings and T2's lead

| Finding | Brief § 3's disposition | What the reading found | This slice's disposition |
| --- | --- | --- | --- |
| **2** (the fork's build documentation is the accurate one) | keep | `CLAUDE.md:65-68`'s `make docker-image-pull` of the pinned digest is the fork's path (`Makefile:138-139`, `ghcr.io/pixelelated/build@sha256:988c0ba5...`); its comment *pull Rasteratops mirror* names the mirror by the retired brand (F-08) | kept; the comment's word is F-08 |
| **5** (the entry points enter the watcher and refuse without an admission) | `CLAUDE.md` and `device-builds.md` already say so | both say so: `CLAUDE.md` § Build & development commands (*automatically use `tools/watch-build`*; *Builds require a current single-use capacity/retention admission*), `device-builds.md` § Before a build | kept; the refusal message is T9's |
| **14** (`CLAUDE.md`'s `OS_VERSION/BUILD_DATE`) | correct the sentence | wrong in **two** files: `CLAUDE.md:88` and `AGENTS.md:86`. `config/options:42` sources `distributions/ROCKNIX/version`, whose `:8` assigns `OS_VERSION="0.0.1"` unconditionally, so an export is overwritten; `distributions/ROCKNIX/options:212` defaults `BUILD_DATE` | F-03, a `bug` |
| **18** (upstream's PR rules into `fork-workflow.md`) | write the facts #645 establishes | #645 is **open** (read 14:53): the facts are not yet established | `deferred:#645` |
| **T2's lead** (`time-to-play.md` on the launch-over-sync rows) | say which build the rule describes | `time-to-play.md:31-35` says D-CLOUD-076's cancel *ships today* and D-CLOUD-109's wait replaces it. The register's three rows: D-CLOUD-076 (2026-09-09, cancel), D-CLOUD-109 (2026-09-12, *Supersedes D-CLOUD-076's cancel*), **D-CLOUD-130** (2026-09-16, *every sync or transfer a game launch would interrupt asks ... STOP IT AND PLAY / KEEP WAITING ... Reverses the silent cancel of #101 / D-CLOUD-109 for launches*). The code: T2 read `FileData.cpp:993-1008` at the pin as D-CLOUD-130 (`docs/audits/2026_10_23-epic-m6-es-launch-path/00-running-log.md:114` on `feature/m6-es-launch-path-649`). The rule names no D-CLOUD-130, and `least-surprise.md:18-20` cites D-CLOUD-109 alone | F-10, a `bug` |

**The other twenty-two #644 findings, each with its carrier** (`build-path-read.md`'s last column), so none is taken here:

| Findings | Carrier |
| --- | --- |
| 1, 3, 4, 8, 9, 11, 22 | T5 |
| 6, 7 | T9 |
| 10, 26 | #585 |
| 12 | T11 |
| 13 | T5 and T9 |
| 15 | T7 and T8 |
| 16 | T8 |
| 17 | #645 |
| 19, 21 | T10 |
| 20 | #637's lane |
| 23 | T12 |
| 24 | T6 |
| 25 | T32 |

## Findings, written as each was re-read

Each finding carries:
- its questions, severity and category;
- the line at the hash;
- the artifact that contradicts or confirms it;
- its rung on `working-principles.md`'s ladder: written, routed, evidenced, audited or self-examining, with the tool that would hold it one rung higher, or *no tool can*.

A Q3 finding, a rule that lies, is a `bug` at stage D (D-WORKFLOW-187).

### F-01 (Q3, Q7; Medium; bug): `AGENTS.md` says `tools/rules-check` keeps it and `CLAUDE.md` equal; the tool checks a count, a list and a mention, and the files differ

- **The claim:** `AGENTS.md:19-20`: *"Both files carry the same facts and are kept equal by `tools/rules-check` (D-WORKFLOW-045)"*.
- **What the tool checks:** `tools/rules-check`'s header (lines 11-27 at the hash) lists `front`, `always`, `index`, `count` (an "All N" sentence), `agents` (the 32 KiB budget), `list` (the generated block), `mention` (each rule named in `CLAUDE.md`) and `tools`. None compares a fact between the two files.
- **The facts differ, by the reader's comparison, re-read here:**
  - the VM's *no* examples: `AGENTS.md:208-210` gives a radio, a battery, a board's boot, a panel and a tailnet with D-QA-007/033; `CLAUDE.md:188-190` gives a panel, a board's memory, a battery and a GPU path with D-QA-007/017;
  - the deploy questions: `AGENTS.md:105` asks for the copy and the reboot, while `CLAUDE.md:105-107` asks for neither;
  - a dozen bullets only one file carries: `fork-package-freshness`, `archaeology`, the absolute `hooksPath` and the shell-tool rule in `AGENTS.md`, and the ES-rules-absent-in-old-worktrees line in `CLAUDE.md`.
- **The cost:** a Codex session and a Claude Code session start from different facts while the file says they do not.
- **Ladder:** the claim says *audited*; the rule is *written*. A tool could hold a named subset (the counts, the build commands, the VM examples) as a `twins` check in `rules-check`. Short of that, the sentence says what the tool holds.

### F-02 (Q3; Medium; bug): `ceremonies.md` says a friction entry without an issue refuses a push; `tools/ceremony-check` never reads an entry without an `issue:` field

- **The rule:** `ceremonies.md`'s table: *"a line in `docs/friction-log.md` with `issue: #N` or `guard` ... an issue or a guard within 3 days ... refuses a push of next"*. § What a friction entry is: *"An entry without an issue expires in three days and refuses the next push"*.
- **The tool:** `tools/ceremony-check:250-252` at the hash matches `- (\d{4}-\d\d-\d\d) .*issue:\s*(#\d+|none|guard)` and **`continue`s on no match**. An entry the pattern does not fit is counted neither as owed nor as covered.
- **The count:** at the hash, **125 of 445 dated entries are never seen** (116 have no `issue:` field, 9 have another shape: `issues: #N`, `Issue #N`, a colon after the date).
- **Nothing is owed today.** Of the 125, 2 name no issue anywhere (lines 37 and 38, 2026-09-27), and both name a guard path. But the next line written without the field passes silently, which is `engineering-practices.md` § Guards must fail closed.
- **The fix belongs in the tool:** every dated `- YYYY-MM-DD` line is an entry, and one with no `issue:`/`guard` field is owed. The rule's sentence is then true.
- **Ladder:** the rule claims *audited*; the audit fails open. The tool is the holder; its proof is a constructed line with no field, seen to refuse.

### F-03 (Q3; Low; bug): `CLAUDE.md:88` and `AGENTS.md:86` say `scripts/image mkimage` *"needs OS_VERSION/BUILD_DATE exported"* (#644 finding 14)

- **`OS_VERSION`:** `config/options:42` sources `distributions/ROCKNIX/version`, whose `:8` assigns `OS_VERSION="0.0.1"` unconditionally, so an exported value is overwritten.
- **`BUILD_DATE`:** `distributions/ROCKNIX/options:212` defaults it (`${BUILD_DATE:-$(date -u ...)}`).
- **So:** neither needs exporting, and an `OS_VERSION` export does nothing.
- **Ladder:** written; *no tool can* check a comment's claim about an environment short of running the build. The fix is the sentence.

### F-04 (Q3; Low; bug): `CLAUDE.md:185` and `AGENTS.md:309` say only *back up* / *backup* is checked mechanically

- `tools/vocabulary-check` at the hash also checks *SAVESTATE* written as one word and *Wi-Fi* without its hyphen. Its header, lines 12-15 and 55-57, names #148's fourteen SAVESTATE labels.
- **Ladder:** written; the tool's own header is the source. A `rules-check` line could compare the two, but the cheaper fix is the sentence, which names the tool's header.

### F-05 (Q3; Low; existing bug #808): `CLAUDE.md`'s rule table names 29 of the 30

- `milestone-phase-naming` is absent from the table (`CLAUDE.md:25-32`). It is named in prose at :161, which satisfies `rules-check`'s substring `mention` check. #808, filed 2026-10-24, owns the fix to the tool and the table.

### F-06 (Q7; Low; Renovation): `CLAUDE.md:27` says *"the four principles"* and lists five

- `least-surprise`, `player-language`, `time-to-play`, `vm-first` and `bugs-are-agent-first`. The fifth was added (D-QA-051) without the count.
- **Ladder:** a `rules-check` count of that cell would hold it. The fix is the word.

### F-07 (Q1; Low; Renovation): the make-target lists omit `SM4450` and `GENERIC_X64`, and `make world` is not the listed set

- `CLAUDE.md:59-61` and `AGENTS.md:56-58` list 13 targets.
- The `Makefile` has `SM4450:` (:83) and `GENERIC_X64:` (:111) too.
- `world:` (:42) builds 12 devices: it includes GENERIC_X64 and excludes AMD64 and SM6115.

### F-08 (Q2; Low; Renovation): *"pull Rasteratops mirror"*

- `CLAUDE.md:65` and `AGENTS.md:63`.
- **The image:** the `Makefile` pins `ghcr.io/pixelelated/build@sha256:...` (:138-139).
- **The rule:** *Rasteratops is a character, not the OS name* (`CLAUDE.md` § Current project identity, `NAMING.md`, D-WORKFLOW-144/151).

### F-09 (Q7; Low; Renovation): *"Two documents carry interface law"*, against three

- `CLAUDE.md:34` (*"Two more documents"*) and `AGENTS.md:31` say two.
- `instruction-files.md:122` says three, adding `docs/device-testing-policy.md`.

### F-10 (Q3, Q4; Medium; bug): `time-to-play.md` describes two superseded rows as what ships; `least-surprise.md` cites the superseded one

- **The rule:** `time-to-play.md:31-35` says the cancel of D-CLOUD-076 ships and that D-CLOUD-109's bounded wait replaces it. `:41-45` states D-CLOUD-109's wait as the rule.
- **The register:** D-CLOUD-130 (2026-09-16) reverses D-CLOUD-109 for launches: the launch *asks*, STOP IT AND PLAY / KEEP WAITING, and nothing is cancelled until the player answers.
- **The code:** T2 read it as D-CLOUD-130 (`FileData.cpp:993-1008` at the pin; T2's running log :114). `es-native-ui.md` § Anything automatic ... and `es-player-text.md` § Conventions describe D-CLOUD-130's question.
- **Also stale:** `least-surprise.md:18-20` says *"never cancelled by a launch; it finishes or fails with a reason (D-CLOUD-109)"*, where the player may now stop it.
- **Ladder:** written. `tools/archaeology --reversal` is the sweep a reversal row's change was meant to run (`decision-register.md` § A reversal ... sweeps its old words); *no tool runs it by itself*. A check that flags a rule citing an ID that a later row says it reverses would hold the class (`t4-q4.py`'s superseded column is that check's draft, with 2 hits in 45).

### F-11 (Q3; Medium; bug): three sentences say `/var/log` does not survive a boot; it is a bind of `/storage/.cache/log`

- **The three sentences:**
  - `generic-x64-vm-testing.md:763`: *"`/var/log` is lost on shutdown"*;
  - `:1003`: *"`/var/log` does not survive"*;
  - `es-code-traps.md:182`: *"`/var/log/es_log.txt` is tmpfs, so a proof script's closing reboot wipes it"*.
- **The unit:** `projects/ROCKNIX/packages/sysutils/busybox/system.d/var-log.mount` at the hash (`What=/storage/.cache/log`, `Where=/var/log`, `Options=bind`) and the GENERIC_X64 install tree's copy say the same.
- **The other rules agree with the unit:** `generic-x64-vm-testing.md:279`, `:735` (*"survive a reboot"*) and `rclone-cloud-sync.md:366` (D-SYS-001).
- **The cost:** a proof that reads a log before a reboot because the rule says it will vanish, or trusts a wipe that does not happen.
- **Ladder:** written; *no tool can* tie a sentence to a unit file short of a guest read. The proof of the fix is the unit, cited in the sentence.

### F-12 to F-15 (Q3; Low; bug, one with F-16): four sentences in `generic-x64-vm-testing.md` the tree contradicts

- **F-12 `:692`**: `tools/fork-publish-release` *"converts the raw image into the sparse disk size ... and packages that same qcow2 into `.utm.zip`"*. The tool's header at the hash says it *"Prepare[s] GitHub release identity ... No upload"*, with 0 mentions of `qcow2` or `utm`. The UTM bundle is `generic-x64-vm utm --output` (`:82-86`).
- **F-13 `:545`** lists `realpath` among the applets the guest's busybox lacks. `busybox-target.conf` has `CONFIG_REALPATH=y`, and the install tree's `usr/bin/realpath` links to `busybox`.
- **F-14 `:748`**: *"there is no `emustation` unit"*. `emustation.service` is installed (`usr/lib/systemd/system/` in the GENERIC_X64 tree) beside `essway.service`. The sentence's point, that the ES log is `essway`'s, stands.
- **F-15 `:808`**: *"Use the shared `tools/watch-build` runner around the frozen checkout's test command"*, with no `--record-only`. As written, that is refused (`watch-build:98`, *build admission required*). `CLAUDE.md` says QA jobs use `--record-only`.

### F-16 (Q1; Low; Renovation): three tool behaviours `generic-x64-vm-testing.md` describes from before their change

- `:109-111`'s headless comment (`virtio-gpu-pci, -display none`) is the `--gl none` path. The default is `virtio-gpu-gl-pci` with `egl-headless` (`generic-x64-vm:281-295`), as `:296-308` says.
- `:880` has `vm-qa` running *"the scripts test, the round-trip suite, the emulator-exit cell and every walk"*. `SUITES` (`vm-qa:63`) has 17.
- `:911`: *"The profile carries QEMU's `i6300esb` watchdog"*. `profile.json` has none; `generic-x64-vm:435` adds it.

### F-17 (Q1; Low; Renovation): build roots named `build.ROCKNIX-*`

- **The tree:** `config/path:19` builds `${BUILD_BASE}.${DISTRONAME}-${DEVICE}.${TARGET_ARCH}`, with `DISTRONAME="pixelelated"` (`distributions/ROCKNIX/options:17`). Every M7 root is `build.pixelelated-*`.
- **The rules:** 8 lines in 4 rules say `build.ROCKNIX-`:
  - `device-builds.md` 4 (its own § Where to build already says `build.pixelelated-H700.arm`);
  - `packaging-and-patches.md` 2;
  - `es-code-traps.md` 1;
  - `worktrees.md` 1.

### F-18 (Q1, Q6; Low; Renovation): the index describes the retired `cloud-pair-migration` as current

- **The row:** `instruction-files.md:156` describes it as *"the mixed-installation test ... the folder's join, move and follow"* (D-CLOUD-158).
- **The tool:** it refuses at the hash (`tools/cloud-pair-migration:58-62`, *"This migration suite is retired"*, exit 2; D-CLOUD-175/#508).
- **The siblings:** the rows at `:205` and `:206` say *retired; refuses execution* for their two retired tools.

### F-19 (Q1, Q3; Low; bug for `:62`): the old ES layout and owner

- **The ES checkout:** `device-builds.md:624-632` names `~/Development/emulationstation-next` with `origin` `maxengel/emulationstation-next`. The checkout's `origin` is `pixelelated/emulationstation` now (`git remote -v`, read only); `rocknixfork` is still `maxengel/emulationstation-next-rocknix`.
- **The PR command:** `fork-workflow.md:62` builds an upstream PR with `--head maxengel:pr/<name>` while `:4` and the remote say `origin` is `pixelelated/distribution`. As written, it names a head in another owner's fork.
- **No PR is cut now** (D-WORKFLOW-165).

### F-20 (Q3, Q6; Low; bug, a re-review request): `council-substrate-integrity.md` names defences this tree does not have

The rule was adopted verbatim from another estate (its `:14-16`; `instruction-files.md`: *refreshed by deliberate re-review, not edited here*).
- **Absent at the hash:**
  - `scripts/lint-council-research-provenance.ts` (`:76`, `:86`, `:194`);
  - `scripts/lint-council-research-digests.ts` (`:88`);
  - `scripts/lint-no-direct-council-member-invocation.ts` (`:138`, `:196`);
  - `.github/workflows/ci.yml` (`:155`);
  - `.pre-commit-config.yaml` and `.prettierignore` (`:161-162`);
  - `.stale-blob-allowlist` (`:109`, `:241`);
  - two `.claude/rules/*.instructions.md` (`:198`, `:202`);
  - `research/council-research/` (`:146`, `:162`).
- **The glob** `research/council-research/**` matches nothing.
- **The table at `:131`** heads the defences *"all in place"*.
- **Also:** *"Brake #2"* (`:81`) is defined nowhere in the file, and its issue numbers are another tracker's.
- **What exists:** `council-invoke.ts`, `council-verification.ts`, `verify-pins.ts` and `check-stale-blob-drift.ts` (the reader's checks, re-read here for the four absent scripts by `git cat-file -e`).
- **Ladder:** written; the remedy is the re-review the index names, not an edit here.

### F-21 (Q3, Q1; Low, one Medium; bug): `rclone-cloud-sync.md` states five facts the package has moved past

- **`:126-128` (Medium):** *"there is no `PKG_SHA256` ... To bump rclone, change `PKG_VERSION` only"*. `rclone/package.mk:39,43` pin a `PKG_SHA256` per arch, so a bump that follows the sentence fails its fetch.
- **`:616-618`:** *"the device ships 1.74.4"*. `PKG_VERSION="1.75.2"`.
- **`:77`, `:133-134`, `:232-236`:** *"`backup/*.zip` (the settings-backup archive)"* and *"match it with `--include=*.zip`"*. `cloud_sync-rules.txt:63-64` carries `*.zip` and `*.tar.gz`, and the archives are `tar.gz` now (`cloud_backup:747`).
- **`:374-375`:** *"`tools/cloud-round-trip` asserts ... the exit-4 timing"*. It asserts exit 69 (`cloud-round-trip:1460-1470`).
- **`:84-94`:** the scope guardrail (*"every cloud-sync change must serve syncing only that set"*) and *"ROM/BIOS distribution is not part of the gamesave sync flows"* predate the content tier, which `:705-709` describes (`cloud_content_backup --selected`, D-CLOUD-050).

### F-22 (Q7, Q3; Low; Renovation): the tool index's *Detail in* column points 31 of 85 tool-to-rule pairs at a rule that never names the tool

- **The 31** (`instruction-files.md` § The fork's own tools; a whole-word search of each named rule):
  - `generic-x64-vm-testing.md` 10;
  - `rclone-cloud-sync.md` 9;
  - `release-candidates.md` 4;
  - `upgrade-and-install.md` 2;
  - `es-native-ui.md` 2;
  - `issue-tracking.md` 2;
  - `device-builds.md` 1;
  - `packaging-and-patches.md` 1.
- **The cost:** a reader sent to the rule for the detail finds none.
- **Ladder:** routed. `rules-check`'s `tools` check could assert that the named rule names the tool (audited).

### F-23 (Q2, Q7; Low; Renovation): the decision register's open table and six decided rows

- **The open-table header** has three columns (`| ID | Question | Home |`). Of its 11 rows, 5 follow it, 5 carry four cells (a date added) and D-RA-006 carries five, so a reader of the table misreads *Home* for six rows (cell counts at the hash, pipes inside backticks not counted).
- **Two open rows were changed in place:**
  - D-QA-040 gained `**Open:**` (`f00ab3e163`, #646, on the branch, not at the hash);
  - D-RA-006 carries a dated 2026-09-18 amendment in a fifth cell.

  The contract (`decision-register.md` § The contract) speaks of decided rows only, so it neither forbids nor allows an edit to an open row.
- **Six decided rows** carry an unescaped `|` inside backticks, which splits the cell in GFM: D-UI-024, D-CLOUD-068, D-CLOUD-072, D-INFRA-010, D-UI-083 and D-SYS-010.
- **Ladder:** `register-check` audits IDs and placement. It could also check the column count, the escaped pipes and an open row's history (audited).

### F-24 (Q2, Q7; Low; Renovation): the friction log is not one line per entry

- Six prose blocks sit inside `## Entries` (lines 171-177, 488-502, 508-512, 519-534, 537-540, 719-725, the reader's list, re-read by line number), against the *one line* the file's own preamble promises.
- The entry shape also drifts: `—` for `--`, ISO `T` times, no time, `issue:` first.
- With F-02, a parser that trusts the shape misses entries.

### F-25 (Q2; Low; existing bug #811): the blindspot register numbers two entries 29

- A table row (`:38`) and a heading (`:40`) are both 29. `t4-q6.py blindspots` confirms it is the only duplicate. #811 owns it.

### F-26 (Q1; Low; deferred to #640): the legacy layout in 8 files

- `/workspace/repos/rocknix` and `rocknix.worktrees/` appear in 25 lines across 8 files (`02` § Mechanical checks).
- #640 owns the cutover, which comes after the M7 candidate (D-INFRA-026). The text changes when #640 says the paths have moved.

### F-27 (Q5, Q7; Renovation): what the doctrine costs a session, and the largest rule

- **The cost per session:** 24 rules and 5,179 lines load at every Claude Code session, plus `CLAUDE.md`'s 202. Crush loads all 11,394 lines.
- **The largest rule:** `generic-x64-vm-testing.md` is 1,398 lines. It loads on any `projects/ROCKNIX/packages/**` path, so every emulator, OS, cloud and proxy lane reads it.
- **Its one-responsibility question:** by the reader's read, about 40 % of it is dated incident narrative. The process-matching advice appears three times (`:185-195`, `:544-553`, `:1091-1093`) with three patterns, and kill-by-PID three times.
- **`handheld-evidence.md`'s `docs/**`** matches 125,306 paths, so it loads for any session that opens a record.
- **No glob is narrowed and no rule is split here:** each is a proposal for a stream brief with its reader cost stated (`04` § Q5).

### Leads (not this slice's findings)

- **Pre-renovation branches carry doctrine `next` lacks:** `feature/conflict-resolution` (36 commits, 2026-10-07), `x64-build-fix` (2025-10-22), and `verification-anchors/2026-09-30-*`. They are branch hygiene and outside the 36; for the coordinator.
- **Reader items not re-verified here,** and so not findings:
  - the `/tmp/qmon.sock` and `/tmp/mon.sock` monitor names;
  - `pkill -x mc` at `generic-x64-vm-testing.md:493`;
  - the resolver advice at `:266-271` against `:532-534`;
  - `handheld-evidence.md`'s D-QA-008 citation;
  - `packaging-and-patches.md`'s `PKG_DEPENDS_TARGET` *Required*;
  - the decision register's ID gaps (D-CLOUD-006, 139, 140; D-NET-011) and its out-of-order dates.

  Each is for the stream that edits the file.
## Proofs

Every proof is a line of `00-running-log.md` with the same number, and its cell is one of `tree`, `tool-run` or `history` (brief § 6).

| # | What | Command / artifact | Result | Cell |
| --- | --- | --- | --- | --- |
| P1 | the membership | brief § 2's filter over the inventory (14:34), `membership.txt` | 36 paths, 11,414 inventory lines, all fork-own markdown, `reach: n/a` | proved: tool-run |
| P2 | the lines at the hash, two ways | numstat against the empty tree; `cat` of the read tree into `wc -l`; per file `hash-lines.txt` | 11,394 both; the 20-line difference is three files | proved: tree |
| P3 | what loads every session | each rule's `paths:` block parsed whole (`t4-q6.py rules`) | 24 of 30 rules, 5,179 lines | proved: tree |
| P4 | the branch's deltas and their owners | `git diff 8ebaf8daad HEAD`, `git log` per file, `git log -S'| D-QA-040 | **Open:**'` | 8 files; D-QA-040's marker is `f00ab3e163` | proved: history |
| P5 | the branch scan | `git rev-list --no-merges next..<b>` less the coordinator's and P1's commits | no unaccepted M6 lane rule edit; T2's is `11a2ee182f` | proved: history |
| P6 | the six checkers and `box-check` | `rules-check`, `register-check`, `ceremony-check`, `forbidden-terms-check`, `hooks-test`, `box-check` (14:39-14:42) | rc 0, 0, 1 (W42 only), 0, 0, 0 | proved: tool-run |
| P7 | the `paths:` globs | brief § 5's loop and `t4-q6.py rules` at the hash | 57 globs; one matches nothing (`research/council-research/**`) | proved: tree |
| P8 | the cited IDs | `grep -ohE` over the 33; `t4-q4.py ids` | 181; 178 decided, 3 open, 0 absent | proved: tree |
| P9 | the tool table | brief § 5's loop; `t4-q6.py tooltable` | 72 rows, none missing | proved: tree |
| P10 | the legacy paths | `grep -c` over the 33 | 8 files, 25 lines | proved: tree |
| P11 | the friction matcher fails open | `ceremony-check:250-252` read at the hash; its regex lifted and applied (`t4-q6.py friction`) | 125 of 445 entries never seen | proved: tree |
| P12 | `rules-check` keeps no fact equal between the entry files | `rules-check`'s header (lines 11-27) beside `AGENTS.md:19-20` | the eight checks, none a fact comparison | proved: tree |
| P13 | `OS_VERSION` and `BUILD_DATE` | `config/options:42`, `distributions/ROCKNIX/version:8`, `distributions/ROCKNIX/options:212` | the export is overwritten; the date defaults | proved: tree |
| P14 | `vocabulary-check`'s scope | its header and lines 55-57 at the hash | SAVESTATE and Wi-Fi checked too | proved: tree |
| P15 | the launch-over-sync rows | D-CLOUD-076, 109, 130 read; T2's running log :114 at its branch | D-CLOUD-130 reverses 109 for launches; the code ships it | proved: history |
| P16 | `/var/log` is a bind | `var-log.mount` at the hash and in the GENERIC_X64 install tree | `What=/storage/.cache/log`, `Options=bind` | proved: tree |
| P17 | four `generic-x64-vm-testing.md` sentences | `fork-publish-release`'s header and `grep -c qcow2` (0); `CONFIG_REALPATH=y` and `usr/bin/realpath -> busybox`; `emustation.service` installed; `watch-build:98` | each contradicted | proved: tree |
| P18 | three tool behaviours from before their change | `generic-x64-vm:281-295,435`, `profile.json` (0 watchdog lines), `vm-qa:63` | each changed | proved: tree |
| P19 | five `rclone-cloud-sync.md` facts | `rclone/package.mk:7,39,43`, `cloud_sync-rules.txt:63-64`, `cloud_backup:747`, `cloud-round-trip:1460-1470`, the rule's `:705-709` | each moved | proved: tree |
| P20 | the index's pointers and `cloud-pair-migration` | a whole-word search of each named rule; `cloud-pair-migration:58-62` | 31 of 85 unnamed; the tool refuses | proved: tree |
| P21 | the old ES owner | `git -C ~/Development/emulationstation-next remote -v` (read only), `fork-workflow.md:62` | `origin` is `pixelelated/emulationstation`; the command names `maxengel` | proved: tree |
| P22 | `council-substrate-integrity.md`'s absent defences | `git cat-file -e 8ebaf8daad:<p>` for each, `t4-q4.py paths` | ten paths absent; the glob matches 0 | proved: tree |
| P23 | the command blocks | `t4-blocks.py`; the seven read-only blocks run (14:48), the two filters on a fake line | 56 blocks, each with a verdict; the filters keep no value | proved: tool-run |
| P24 | the superseded citations | `t4-q4.py ids`, the narrowed candidates, each successor row's sentence read | 2 of 45 cite a superseded row as current | proved: history |
| P25 | the blindspot guards | `t4-q6.py blindspots` | 74 entries, 29 twice; every named guard exists | proved: tree |
| P26 | the `build.ROCKNIX-` names | `grep -c 'build\.ROCKNIX-'` over the 33; `config/path:19`; `DISTRONAME` | 8 lines in 4 rules; the roots are `build.pixelelated-*` | proved: tree |

## Criterion entries: #651's checklist (= brief § 7), at the end of Phase 2

Each entry names the artifact that will tick it; the coordinator ticks at hand-back. *Met at B* where this phase shows it.

1. **The folder holds `00` to `05`.** `00` to `02` now; `03` and `04` at stages B and C; `05` at D.
2. **The lint prints `PASS`.** `--phase pre-issue` before D, the default phase at close.
3. **`review-plan.json`.** Local, no reviewer, plan § 6c's row (stage C).
4. **Every punch item at a Phase 7 outcome.** After the stage-D pause.
5. **`reviewed-at:`/`fixed-at:` in #651's body.** `reviewed-at: 00e75ab135` at H; `renovation-status` after the merge (the coordinator's).
6. **`01` § Scope and § The reader's pass.** *Met at B.* Read hash, filter output, both counts, the always-loaded figure, the deltas hunk by hunk with owners, and a reader's line for each of the 36.
7. **The coverage table.** *Met at B.* 36 rows, the path first in backticks, Q1 to Q7 each answered or `none` with what was read (`t4-coverage.py`).
8. **§ Mechanical checks and § Command blocks.** *Met at B.* Every check named, with command, exit and summary; 56 blocks, each with a verdict; nothing that could not run is recorded as a pass.
9. **§ The four #644 findings and T2's lead.** *Met at B*, with the other twenty-two named with their carriers.
10. **`04` § Q4, four tables written by a script.** Stage C (`tools/t4-q4.py`).
11. **`04` § Q5's load table.** Stage C, naming the two time-to-play numbers as untouched.
12. **`04` § Q6's reachability tables.** Stage C (`tools/t4-q6.py`).
13. **The proof count.** Each proof above carries its cell; the count of those cells equals the count of the log's proof lines. *Met at B* (26 = 26), re-counted at F.
14. **Every punch item's ladder stage; each `tracked:` bug names its sentence; nothing of the 36 changed before a stream.** D and H. `git status --short -- <the 36>` is empty at the end of B (`00`).
15. **The retro.** G.
16. **The six exit codes.** H.

## Command blocks (every fenced block in the 36 files, at the hash)

Generated by `tools/t4-blocks.py <read-tree> <paths.txt>`, which refuses when a block has no verdict or a verdict no block.

| # | Block (file:line at the hash) | Language | Lines | Verdict |
| ---: | --- | --- | ---: | --- |
| B01 | `.claude/rules/ceremonies.md:97` | bash | 4 | ran: passed -- `tools/ceremony-check` rc 1 (W42, M7's) and `--gate` rc 1 likewise; `tools/archaeology D-CLOUD-076` rc 0; `work-log-index --write` not run (it writes), `--check` rc 0 |
| B02 | `.claude/rules/council-substrate-integrity.md:75` | bash | 2 | checked: wrong -- `scripts/lint-council-research-provenance.ts` and `research/council-research/` are absent at the hash (F-20) |
| B03 | `.claude/rules/device-builds.md:58` | bash | 1 | checked -- `git worktree add -b build/...` is valid git; the path is the legacy layout (#640) |
| B04 | `.claude/rules/device-builds.md:90` | bash | 6 | not runnable here (a device build); checked: `make docker-RK3566` matches `docker-%` (Makefile:138); the mounts name the legacy checkout (#640) |
| B05 | `.claude/rules/device-builds.md:147` | bash | 4 | not runnable here (deletes build-root files); a recovery recipe for a warm root |
| B06 | `.claude/rules/device-builds.md:244` | - | 2 | not a command (linker output) |
| B07 | `.claude/rules/device-builds.md:259` | bash | 7 | not runnable here (needs a build root); checked: names `build.ROCKNIX-<DEVICE>.<ARCH>`, where `config/path:19` and `DISTRONAME="pixelelated"` make `build.pixelelated-*` (F-17) |
| B08 | `.claude/rules/device-builds.md:324` | bash | 1 | not runnable here (no build root in this worktree); a read-only `find` |
| B09 | `.claude/rules/device-builds.md:478` | - | 1 | not a command (compiler output) |
| B10 | `.claude/rules/device-builds.md:650` | bash | 2 | not runnable here (a build); checked: `EMULATIONSTATION_SRC` path is `~/Development/...`, the old ES layout (F-19) |
| B11 | `.claude/rules/device-builds.md:674` | bash | 7 | not runnable here (needs a build root and a crash address); checked: names the legacy roots and `build.ROCKNIX-*` (#640, F-17) |
| B12 | `.claude/rules/engineering-practices.md:665` | bash | 1 | ran: passed -- on `key=SECRET` / `name=ok` / `pass = hunter2` it printed `name=ok` only |
| B13 | `.claude/rules/engineering-practices.md:687` | bash | 1 | ran: passed -- on `token=SECRETX user:alice PASS verdict` it printed `token=*** user:*** PASS verdict`: no value, the verdict kept |
| B14 | `.claude/rules/es-code-traps.md:145` | - | 4 | not runnable here (needs the ES tree and a build root); checked: `B=` names the legacy root and `build.ROCKNIX-GENERIC_X64` (#640, F-17) |
| B15 | `.claude/rules/es-native-ui.md:317` | cpp | 4 | not a command (C++) |
| B16 | `.claude/rules/es-native-ui.md:414` | bash | 1 | not runnable here (an ES checkout and a build root); checked: `tools/es-syntax-check` exists with `--with`; its default root is #699's |
| B17 | `.claude/rules/es-ui-style-guide.md:102` | cpp | 2 | not a command (C++) |
| B18 | `.claude/rules/es-ui-style-guide.md:173` | cpp | 1 | not a command (C++) |
| B19 | `.claude/rules/es-ui-style-guide.md:241` | cpp | 4 | not a command (C++) |
| B20 | `.claude/rules/fork-workflow.md:48` | bash | 14 | not runnable here (creates a worktree, pushes, opens a PR; D-WORKFLOW-165 defers submissions); checked: `--head maxengel:pr/<name>` names an owner other than `origin`'s `pixelelated` (F-19); worktree paths are the legacy layout (#640) |
| B21 | `.claude/rules/fork-workflow.md:129` | bash | 1 | not run (writes git config); checked: `git config --get core.hooksPath` reads `/workspace/repos/pixelelated/distribution/.githooks`, which lists `pre-push` |
| B22 | `.claude/rules/fork-workflow.md:186` | bash | 4 | not runnable here (moves and pushes `next`, the coordinator's); valid git |
| B23 | `.claude/rules/generic-x64-vm-testing.md:46` | bash | 2 | not runnable here (a build); checked: `docker-GENERIC_X64` matches `docker-%`; the mounts name the legacy checkout (#640) |
| B24 | `.claude/rules/generic-x64-vm-testing.md:82` | bash | 4 | not runnable here (a guest); checked: `generic-x64-vm` has `run`, `utm` and `--output` |
| B25 | `.claude/rules/generic-x64-vm-testing.md:106` | bash | 9 | not runnable here (a guest); checked: `--headless`, `--daemonize`, `vm-serial wait`/`sh` exist; the comment's display (`virtio-gpu-pci, -display none`) is the `--gl none` path, not the default (F-16) |
| B26 | `.claude/rules/generic-x64-vm-testing.md:129` | bash | 2 | not runnable here (a guest); checked: `vm-serial sh` exists |
| B27 | `.claude/rules/generic-x64-vm-testing.md:566` | bash | 5 | not runnable here (the shared QA backend and a guest); checked: `cloud-test-backend` has `up`, `reset`, `--backend`, `seed-content`, `seed-device` (case arms 402, 593, 843, 869) |
| B28 | `.claude/rules/generic-x64-vm-testing.md:706` | bash | 2 | not runnable here (`sudo`); a one-time host setup |
| B29 | `.claude/rules/generic-x64-vm-testing.md:900` | bash | 2 | not runnable here (guests); checked: `vm-qa` has `--skip-up`, `--only`, `--backend`, `--guest` |
| B30 | `.claude/rules/generic-x64-vm-testing.md:972` | bash | 2 | not runnable here (a guest); checked: `vm-visual-qa` has `--monitor`, `run`, `--outdir`; the socket name differs from the tool's default (a lead) |
| B31 | `.claude/rules/generic-x64-vm-testing.md:1207` | - | 2 | not a command (RetroArch log) |
| B32 | `.claude/rules/handheld-evidence.md:44` | - | 1 | not runnable here (a device command); checked: `projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-evidence` has `collect` |
| B33 | `.claude/rules/instruction-files.md:24` | yaml | 5 | not a command (the front-matter template) |
| B34 | `.claude/rules/instruction-files.md:80` | bash | 1 | ran: passed -- `diff -q .claude/rules/vm-first.md <(git -C /workspace/repos/rocknix show next:...)` rc 0; it reads the legacy checkout's `next` (#640), which is `8ebaf8daad` today |
| B35 | `.claude/rules/issue-tracking.md:22` | bash | 1 | not run (creates an issue); checked: `gh issue create --repo ... --title --body-file` is valid |
| B36 | `.claude/rules/milestone-phase-naming.md:48` | text | 1 | not a command (the title grammar) |
| B37 | `.claude/rules/milestone-phase-naming.md:64` | text | 5 | not a command (example titles) |
| B38 | `.claude/rules/packaging-and-patches.md:65` | bash | 4 | not runnable here (needs a build root); checked: `IMG=build.ROCKNIX-<DEVICE>.<ARCH>` is the old root name (F-17) |
| B39 | `.claude/rules/packaging-and-patches.md:82` | bash | 5 | not runnable here (writes a patch into a recipe); valid `diff`/`git diff` |
| B40 | `.claude/rules/rclone-cloud-sync.md:503` | - | 1 | not a command (rclone output) |
| B41 | `.claude/rules/rclone-cloud-sync.md:538` | bash | 7 | not runnable here (the shared QA backend and a guest); checked: `cloud-test-backend` `up`/`ls`/`down`/`--backend`, `cloud-round-trip --host --port --identity` exist |
| B42 | `.claude/rules/rclone-cloud-sync.md:600` | bash | 4 | not runnable here (the shared QA backend and a guest); checked as the block above |
| B43 | `.claude/rules/upgrade-and-install.md:73` | - | 2 | not a command (the `Already written:` template) |
| B44 | `.claude/rules/worktrees.md:17` | - | 5 | not a command (the legacy layout diagram, #640) |
| B45 | `.claude/rules/worktrees.md:45` | bash | 1 | not run (`sync` fast-forwards every build worktree, the M7 lane's); checked: `fork-worktree` has `sync` |
| B46 | `.claude/rules/worktrees.md:119` | bash | 5 | ran: passed for `list` (rc 0, 62 lines); `remove`, `--preserve`, `--force`, `repair` not run (they write); checked: all exist |
| B47 | `.claude/rules/worktrees.md:213` | bash | 4 | not runnable here (moves `next`, creates a worktree); valid git; legacy paths (#640) |
| B48 | `.claude/rules/worktrees.md:222` | bash | 1 | not runnable here (creates a worktree); valid git; legacy path (#640) |
| B49 | `.claude/rules/worktrees.md:228` | bash | 3 | ran: passed for `list`; `remove` and `prune` not run (they write); legacy path (#640) |
| B50 | `AGENTS.md:63` | bash | 4 | not runnable here (pulls an image, builds); checked: `docker-image-pull`, `docker-shell` targets exist, `docker-package` is `docker-%` running `package` (Makefile:120, 138); the comment's *Rasteratops mirror* is `ghcr.io/pixelelated/build` (Makefile:139; F-08) |
| B51 | `AGENTS.md:72` | bash | 5 | not runnable here (builds); checked: `RK3588`, `kconfig-menuconfig-%` targets and `scripts/build`, `clean`, `checkdeps` exist |
| B52 | `AGENTS.md:82` | bash | 4 | not runnable here (builds); checked: scripts exist; the comment *needs OS_VERSION/BUILD_DATE exported* is wrong (F-03) |
| B53 | `AGENTS.md:342` | bash | 5 | ran: passed -- `pkgcheck rclone` rc 0, `rules-check` rc 0, `register-check` rc 0, `work-log-index --check` rc 0; `ceremony-check --gate` rc 1 on W42 only |
| B54 | `CLAUDE.md:65` | bash | 4 | not runnable here (as `AGENTS.md:63`); checked as that block (F-08) |
| B55 | `CLAUDE.md:74` | bash | 5 | not runnable here (as `AGENTS.md:72`); checked as that block |
| B56 | `CLAUDE.md:84` | bash | 4 | not runnable here (as `AGENTS.md:82`); the comment is wrong (F-03) |

<!-- t4-blocks: 56 blocks; checked 1; checked: wrong 1; not a command 13; not run 3; not runnable here 31; ran: passed 5; ran: passed for `list` 2 -->

## Coverage table: one row per path (36)

Generated by `tools/t4-coverage.py <read-tree> <paths.txt> <q6-rules.md>`. A cell names the finding that answers its question, or says `none` with what was read. *ok* in Q2 means `tools/rules-check`'s front-matter and index checks pass for the file.

| Path | Group | Lines at the hash | Loads | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |
| --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| `AGENTS.md` | 1 | 351 | the entry file | F-07, F-08, F-26 | within Codex's budget; names all 30 (`rules-check` `agents`, `list`) | F-01, F-03, F-04 | IDs resolve | 351 lines; Codex reads it whole | none: a pointer file | F-01, F-09 |
| `CLAUDE.md` | 1 | 202 | the entry file | F-07, F-08, F-26 | F-08 (the brand) | F-03, F-04, F-05 | IDs resolve (`t4-q4.py ids`); F-04's tool scope | 202 lines, every session | none: a pointer file | F-06, F-09; differs from `AGENTS.md` (F-01) |
| `NAMING.md` | 1 | 60 | nowhere | time-bound #416 line (reader; not re-verified) | `pixelelated` lowercase throughout (grep) | none found by this lane; the reader checked its paths (a lead, not re-run here) | D-WORKFLOW-128/144/151, D-CLOUD-174-176 resolve | 60 lines; loads nowhere | none | title is the issue's, not the file's (`01`) |
| `.claude/rules/adversarial-council.md` | 2 | 124 | every session | none | ok | none found | IDs resolve | every session | none | the seat-length section is long for the seats it now concerns |
| `.claude/rules/bugs-are-agent-first.md` | 2 | 91 | every session | none | ok; says *no `paths:`* in its first paragraph | none found | IDs resolve | every session | none | none |
| `.claude/rules/ceremonies.md` | 2 | 116 | every session | none | ok | F-02 | IDs resolve | every session | none | none |
| `.claude/rules/change-log.md` | 2 | 47 | on a match | none | ok | none found | IDs resolve | on a match (`projects/ROCKNIX/packages/**`, the change log) | none | `:41` cites the moved § Conventions (redirected by `es-native-ui.md`) |
| `.claude/rules/decision-register.md` | 2 | 99 | every session | none | ok | none found | IDs resolve | every session | none | silent on open rows (F-23) |
| `.claude/rules/documentation-accuracy.md` | 2 | 61 | every session | none: retired tools said retired | ok | none found | IDs resolve | every session | none: its drift list is dated | none |
| `.claude/rules/instruction-files.md` | 2 | 221 | every session | F-18, F-26 | front matter ok (`rules-check`) | F-22 | 72 tools all exist (`t4-q6.py tooltable`) | every session | F-18 | F-22 |
| `.claude/rules/issue-tracking.md` | 2 | 208 | every session | none | ok | none found | D-QA-044 refined by D-QA-051, both cited where they apply | every session | none | dated counts (*46 of 479*) read as history |
| `.claude/rules/learning-capture.md` | 2 | 91 | every session | none | ok | none found | IDs resolve | every session | none | dated counts (*17 of 29*) read as history |
| `.claude/rules/least-surprise.md` | 2 | 40 | every session | none | ok | F-10 (`:18-20`) | F-10: D-CLOUD-109 cited, D-CLOUD-130 in force | every session | none | none |
| `.claude/rules/milestone-phase-naming.md` | 2 | 127 | every session | none | ok | none found | IDs resolve | every session | none | none |
| `.claude/rules/player-language.md` | 2 | 68 | every session | none | ok | none found | IDs resolve | every session | none | none |
| `.claude/rules/time-to-play.md` | 2 | 55 | every session | F-10 | ok | F-10 | F-10: D-CLOUD-076/109 cited as current | every session; this slice changes neither number | none | none |
| `.claude/rules/vm-first.md` | 2 | 82 | every session | none | ok | none found | D-QA-007, D-QA-044 (both still decided; refined, not reversed) | every session | none | none |
| `.claude/rules/working-principles.md` | 2 | 106 | every session | none | ok | none found: its index rows name rules that exist | IDs resolve | every session | none | none: the ladder is the slice's own test |
| `.claude/rules/device-builds.md` | 3 | 695 | every session | F-17, F-19, F-26 | ok | none found beyond F-19; #644 f5 holds | IDs resolve | every session; 695 lines | none | F-22 (`fork-newdrive`) |
| `.claude/rules/engineering-practices.md` | 3 | 836 | every session | none | ok | none found in the sections re-read (the filters ran as written, `02` § Command blocks) | IDs resolve | every session; 836 lines | none | F-27: a dozen sections |
| `.claude/rules/fork-workflow.md` | 3 | 191 | every session | F-19, F-26 | ok; the personal-paths list matches the hook (`rules-check` `tools`) | F-19 (`:62`) | #644 f18 waits on #645 | every session | none | the fork-only tools list is one 100-entry line |
| `.claude/rules/packaging-and-patches.md` | 3 | 113 | on a match | F-17 | ok | none found by this lane; the reader's `PKG_DEPENDS_TARGET` lead not re-verified | IDs resolve | on a match (`packages/**`, `projects/**`) | none | `:28-47` repeat `CLAUDE.md` nearly verbatim (reader) |
| `.claude/rules/release-candidates.md` | 3 | 154 | every session | none | ok | none found | D-QA-049 reversed by D-WORKFLOW-062, which it cites | every session | none | F-22 (four tools pointed here, unnamed) |
| `.claude/rules/upgrade-and-install.md` | 3 | 225 | every session | none | ok | none found | IDs resolve | every session | none | F-22 (two tools pointed here, unnamed) |
| `.claude/rules/worktrees.md` | 3 | 254 | every session | F-17, F-26 | ok | none beyond #640's paths | IDs resolve | every session | none | none |
| `.claude/rules/council-substrate-integrity.md` | 4 | 253 | on a match | none | description is long (adopted verbatim; `instruction-files.md` excuses it) | F-20 | IDs resolve | on a match | F-20: `research/council-research/**` matches 0 | another estate's names (F-20) |
| `.claude/rules/es-code-traps.md` | 4 | 254 | every session | F-17, F-26 | ok | F-11 (`:182`) | IDs resolve | every session (`**`) | none | none |
| `.claude/rules/es-native-ui.md` | 4 | 423 | every session | none | ok | none found | D-CLOUD-130's question described | every session (`**`) | none | F-22 (two tools pointed here, unnamed) |
| `.claude/rules/es-player-text.md` | 4 | 343 | every session | none | ok | none found | D-UI-101 cited for the cards' content (D-UI-109 changed their order) | every session (`**`) | none | the outcome section reads as a dated list |
| `.claude/rules/es-ui-style-guide.md` | 4 | 315 | every session | none | ok | none found | IDs resolve | every session (`**`) | none | none |
| `.claude/rules/generic-x64-vm-testing.md` | 4 | 1398 | on a match | F-16, F-26 | ok | F-11, F-12, F-13, F-14, F-15 | IDs resolve | on a match; 1,398 lines, the largest | none | F-27 |
| `.claude/rules/handheld-evidence.md` | 4 | 114 | on a match | none | ok | none found: every fact the reader checked holds | IDs resolve | on a match; its `docs/**` matches 125,306 paths (F-27) | none | a maintenance-mask section under the VM heading (reader) |
| `.claude/rules/rclone-cloud-sync.md` | 4 | 895 | on a match | F-21 | ok | F-21 | IDs resolve; D-CLOUD-050 cited where the content tier is | on a match; 895 lines | 13 retired mentions said retired (`t4-q6.py retired`) | F-22; duplicates of other rules (reader) |
| `docs/blindspot-register.md` | 5 | 1198 | a register (loads nowhere) | none | F-25 (#811) | none: a record | 40 IDs cited across the two ledgers resolve (`t4-q4.py ledger-ids`) | 1,198 lines; read by `ceremony-check` `guards` | every named guard exists (`t4-q6.py blindspots`) | three entry formats (reader) |
| `docs/decision-register.md` | 5 | 728 | a register (loads nowhere) | none | F-23 | none: a record | the ledger itself; `register-check` 667 IDs once | 728 lines at the hash; read by `archaeology`, `register-check` | none: a decided row cited by nothing is a record | F-23 |
| `docs/friction-log.md` | 5 | 856 | a register (loads nowhere) | none | F-24 | F-02 (its check) | IDs resolve | 856 lines; read by `ceremony-check` `friction` | F-02: 125 entries no check reads | F-24 |

<!-- t4-coverage: 36 rows -->
