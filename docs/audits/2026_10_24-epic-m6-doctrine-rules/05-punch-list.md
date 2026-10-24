# Punch List — M6.P2 T4, the binding doctrine

**Local depth** (plan § 6c, D-WORKFLOW-184): no reviewer; Phase 4.5 is in `04`. **25 items:**
- **5 Medium:** PL-01, PL-02, PL-10, PL-11 and PL-18.
- **20 Low.**
- **Bugs:** 8 filed by this lane (#904 to #911), 2 existing (#808, #811), and 2 other issues (#640, #645).

Each item says the rung of `working-principles.md`'s ladder its rule sits at, and the tool that would hold it at the next rung, or *no tool can*.

**Nothing in the 36 is changed here.** Every edit waits for a stage-E stream brief, one stream per file for the Low wording items (the futro's pre-mortem rule). The audit issue is #912, a sub-issue of #651. The outcomes are open until the coordinator's dispositions after the stage-D pause.

---

## PL-01: `AGENTS.md:19-20` says `tools/rules-check` keeps it and `CLAUDE.md` equal
- **Severity:** Medium
- **Category:** Code Quality
- **Question:** Q3
- **Source Finding:** F-01
- **Owner area:** the entry files: `AGENTS.md`, `CLAUDE.md`, and `tools/rules-check`
- **What:** `AGENTS.md:19-20` says `tools/rules-check` keeps it and `CLAUDE.md` equal; the tool checks a count, a list and a mention, and the facts differ
- **Where:** `02-forward-audit.md` § Findings, F-01
- **Ladder:** written (the sentence claims audited); next rung: `rules-check` with a `twins` check over a named subset of shared facts, seen to fail on a constructed difference
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** sessions read it at every start; none traced to it
- **Acceptance:** #904's first criterion: the sentence names what the tool checks, or the check exists and fails on a constructed difference
- **Tracked:** #904

## PL-02: `ceremony-check:250-252` skips any friction line its regex does not fit (125 of 445), while `ceremonies.md` says an entry without an issue refuses a push
- **Severity:** Medium
- **Category:** Code Quality
- **Question:** Q3
- **Source Finding:** F-02
- **Owner area:** the ceremony state machine: `tools/ceremony-check`, `ceremonies.md`
- **What:** `ceremony-check:250-252` skips any friction line its regex does not fit (125 of 445), while `ceremonies.md` says an entry without an issue refuses a push
- **Where:** `02-forward-audit.md` § Findings, F-02
- **Ladder:** audited, failing open; next rung: `ceremony-check` itself, reading every dated line as an entry
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** 125 entries never gated; none ownerless today
- **Acceptance:** #905's criteria: a constructed entry without the field is owed under the fixed tool and `ok` under the unfixed one
- **Tracked:** #905

## PL-03: `CLAUDE.md:88` and `AGENTS.md:86`: `mkimage` *needs OS_VERSION/BUILD_DATE exported* (#644 f14)
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q3
- **Source Finding:** F-03
- **Owner area:** the entry files
- **What:** `CLAUDE.md:88` and `AGENTS.md:86`: `mkimage` *needs OS_VERSION/BUILD_DATE exported* (#644 f14)
- **Where:** `02-forward-audit.md` § Findings, F-03
- **Ladder:** written; next rung: no tool can: a comment's claim about an environment needs the build
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** carried in briefs' stale-facts lines, not acted on
- **Acceptance:** #904's second criterion
- **Tracked:** #904

## PL-04: `CLAUDE.md:185` and `AGENTS.md:309`: only back up / backup is checked mechanically
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q3
- **Source Finding:** F-04
- **Owner area:** the entry files
- **What:** `CLAUDE.md:185` and `AGENTS.md:309`: only back up / backup is checked mechanically; `vocabulary-check` also checks SAVESTATE and Wi-Fi
- **Where:** `02-forward-audit.md` § Findings, F-04
- **Ladder:** written; next rung: a `rules-check` line comparing the sentence with `vocabulary-check`'s header; the sentence citing the header is enough
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing inherited
- **Acceptance:** #904's third criterion
- **Tracked:** #904

## PL-05: `CLAUDE.md:25-32` names 29 of 30 rules
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q3
- **Source Finding:** F-05
- **Owner area:** `CLAUDE.md`'s rule table and `rules-check`'s `mention`
- **What:** `CLAUDE.md:25-32` names 29 of 30 rules; `mention` accepts the name anywhere
- **Where:** `02-forward-audit.md` § Findings, F-05
- **Ladder:** audited, narrower than its sentence; next rung: `rules-check` reading the table, not the file (#808)
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing inherited
- **Acceptance:** #808's criteria
- **Tracked:** #808

## PL-06: `CLAUDE.md:27`: *the four principles*, five listed
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-06
- **Owner area:** `CLAUDE.md`
- **What:** `CLAUDE.md:27`: *the four principles*, five listed
- **Where:** `02-forward-audit.md` § Findings, F-06
- **Ladder:** written; next rung: a `rules-check` count of that cell; the word is enough
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing inherited
- **Acceptance:** `CLAUDE.md`'s cell names the count its list has

## PL-07: the make-target lists omit `SM4450` and `GENERIC_X64`
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** F-07
- **Owner area:** the entry files and the `Makefile`
- **What:** the make-target lists omit `SM4450` and `GENERIC_X64`; `make world` is not the listed set
- **Where:** `02-forward-audit.md` § Findings, F-07
- **Ladder:** written; next rung: a `rules-check` line comparing the list with the `Makefile`'s device targets
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing inherited
- **Acceptance:** both lists match the `Makefile`'s device targets at `fixed-at`, or say they are examples, and `world` is described as `Makefile:42` has it

## PL-08: *pull Rasteratops mirror* (`CLAUDE.md:65`, `AGENTS.md:63`)
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** F-08
- **Owner area:** the entry files
- **What:** *pull Rasteratops mirror* (`CLAUDE.md:65`, `AGENTS.md:63`); the image is `ghcr.io/pixelelated/build` and Rasteratops is a character (D-WORKFLOW-144)
- **Where:** `02-forward-audit.md` § Findings, F-08
- **Ladder:** written; next rung: `tools/rasteratops-identity-check` reading the entry files for the brand in a current role
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing inherited
- **Acceptance:** `grep -n 'Rasteratops mirror' CLAUDE.md AGENTS.md` prints nothing at `fixed-at`

## PL-09: *two* interface-law documents (`CLAUDE.md:34`, `AGENTS.md:31`) against `instruction-files.md:122`'s three
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-09
- **Owner area:** the entry files and `instruction-files.md`
- **What:** *two* interface-law documents (`CLAUDE.md:34`, `AGENTS.md:31`) against `instruction-files.md:122`'s three
- **Where:** `02-forward-audit.md` § Findings, F-09
- **Ladder:** written; next rung: a `rules-check` count across the three files
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing inherited
- **Acceptance:** the three files name the same documents at `fixed-at`

## PL-10: the launch over a running sync described as D-CLOUD-076/109, where D-CLOUD-130 decides and ships
- **Severity:** Medium
- **Category:** Code Quality
- **Question:** Q3
- **Source Finding:** F-10
- **Owner area:** `time-to-play.md`, `least-surprise.md`
- **What:** the launch over a running sync described as D-CLOUD-076/109, where D-CLOUD-130 decides and ships
- **Where:** `02-forward-audit.md` § Findings, F-10
- **Ladder:** written; next rung: a check that flags a rule citing an ID a later row reverses (`tools/t4-q4.py`'s superseded column, 3 hits in 45), or `tools/archaeology --reversal` run with each reversal row
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** T2 routed the drift; no design built on it in the record
- **Acceptance:** #906's criteria
- **Tracked:** #906

## PL-11: three sentences say `/var/log` does not survive a boot
- **Severity:** Medium
- **Category:** Code Quality
- **Question:** Q3
- **Source Finding:** F-11
- **Owner area:** `generic-x64-vm-testing.md`, `es-code-traps.md`
- **What:** three sentences say `/var/log` does not survive a boot; `var-log.mount` binds `/storage/.cache/log`
- **Where:** `02-forward-audit.md` § Findings, F-11
- **Ladder:** written; next rung: no tool can: a sentence about a unit is checked by reading the unit, which the corrected sentence cites
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** none traced
- **Acceptance:** #907's criteria
- **Tracked:** #907

## PL-12: `fork-publish-release` and the UTM bundle
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q3
- **Source Finding:** F-12, F-13, F-14, F-15
- **Owner area:** `generic-x64-vm-testing.md`
- **What:** `fork-publish-release` and the UTM bundle; `realpath`; the `emustation` unit; `watch-build` without `--record-only`
- **Where:** `02-forward-audit.md` § Findings, F-12, F-13, F-14, F-15
- **Ladder:** written; next rung: no tool can beyond citing each tool's own `--help` or header line in the sentence
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** `:808` fails closed; nothing inherited
- **Acceptance:** #908's criteria
- **Tracked:** #908

## PL-13: the headless comment's display, four of `vm-qa`'s 17 suites, the watchdog's home
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** F-16
- **Owner area:** `generic-x64-vm-testing.md`
- **What:** the headless comment's display, four of `vm-qa`'s 17 suites, the watchdog's home
- **Where:** `02-forward-audit.md` § Findings, F-16
- **Ladder:** written; next rung: no tool can; with #908's stream
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing inherited
- **Acceptance:** each of the three sentences matches `generic-x64-vm:281-295`, `vm-qa:63` and `generic-x64-vm:435` at `fixed-at`

## PL-14: `build.ROCKNIX-*` in 8 lines
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** F-17
- **Owner area:** `device-builds.md`, `packaging-and-patches.md`, `es-code-traps.md`, `worktrees.md`
- **What:** `build.ROCKNIX-*` in 8 lines; the roots are `build.pixelelated-*` (`config/path:19`)
- **Where:** `02-forward-audit.md` § Findings, F-17
- **Ladder:** written; next rung: a `rules-check` list of retired names, beside #640's paths
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing inherited
- **Acceptance:** `grep -c 'build\.ROCKNIX-' .claude/rules/*.md` is 0 at `fixed-at`, or each line marks itself historical

## PL-15: the index describes the retired `cloud-pair-migration` as current (`:156`)
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-18
- **Owner area:** `instruction-files.md`
- **What:** the index describes the retired `cloud-pair-migration` as current (`:156`)
- **Where:** `02-forward-audit.md` § Findings, F-18
- **Ladder:** routed; next rung: `rules-check`'s `tools` check: a tool whose header says retired has a row that says so
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** a session following the row met exit 2; nothing written
- **Acceptance:** `:156` says retired, as `:205-206` do, matching `cloud-pair-migration:58-62`

## PL-16: `--head maxengel:pr/<name>` against `origin` `pixelelated`
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q3
- **Source Finding:** F-19
- **Owner area:** `fork-workflow.md`, `device-builds.md`
- **What:** `--head maxengel:pr/<name>` against `origin` `pixelelated`; the ES checkout's old `origin`
- **Where:** `02-forward-audit.md` § Findings, F-19
- **Ladder:** written; next rung: no tool can: the command reads its owner from `git remote` instead
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** no PR cut since D-WORKFLOW-165
- **Acceptance:** #910's criteria
- **Tracked:** #910

## PL-17: ten defences named that this tree lacks
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q3
- **Source Finding:** F-20
- **Owner area:** `council-substrate-integrity.md`
- **What:** ten defences named that this tree lacks; a zero-match glob; *Brake #2* undefined
- **Where:** `02-forward-audit.md` § Findings, F-20
- **Ladder:** written; next rung: the re-review `instruction-files.md` names; `rules-check` could check a rule's named paths exist
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** sessions read the absent lints as in place; the Facilitator's own checks exist
- **Acceptance:** #911's criteria
- **Tracked:** #911

## PL-18: *no `PKG_SHA256`* (two are pinned), *ships 1.74.4*, the `.zip` archive, exit 4, the scope paragraph
- **Severity:** Medium
- **Category:** Code Quality
- **Question:** Q3
- **Source Finding:** F-21
- **Owner area:** `rclone-cloud-sync.md`
- **What:** *no `PKG_SHA256`* (two are pinned), *ships 1.74.4*, the `.zip` archive, exit 4, the scope paragraph
- **Where:** `02-forward-audit.md` § Findings, F-21
- **Ladder:** written; next rung: no tool can short of `pkgcheck` reading prose; the sentences cite the recipe's lines
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** the bump to 1.75.2 carried its checksums; nothing inherited
- **Acceptance:** #909's criteria
- **Tracked:** #909

## PL-19: 31 of 85 *Detail in* pairs name a rule that never names the tool
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-22
- **Owner area:** `instruction-files.md` and the eight rules it points at
- **What:** 31 of 85 *Detail in* pairs name a rule that never names the tool
- **Where:** `02-forward-audit.md` § Findings, F-22
- **Ladder:** routed; next rung: `rules-check`'s `tools` check: the rule a row names must name the tool
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** a reader sent for detail found none; nothing written
- **Acceptance:** `tools/t4-q6.py`-style search prints 0 unnamed pairs at `fixed-at`, or each row names the rule that carries the detail

## PL-20: the open table's header against its rows' cells
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** F-23
- **Owner area:** `docs/decision-register.md`, `tools/register-check`
- **What:** the open table's header against its rows' cells; D-QA-040's and D-RA-006's in-place changes; six decided rows' unescaped pipes
- **Where:** `02-forward-audit.md` § Findings, F-23
- **Ladder:** audited for IDs, not shape; next rung: `register-check`: column count per table and escaped pipes inside code spans
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** a reader misparses six open rows and six decided ones; no data
- **Acceptance:** `register-check` reports the column shape and passes at `fixed-at`; the contract's sentence on open rows is a new row if the coordinator decides one (append-only)

## PL-21: six prose blocks in `## Entries`
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** F-24
- **Owner area:** `docs/friction-log.md`
- **What:** six prose blocks in `## Entries`; the entry shape drifts
- **Where:** `02-forward-audit.md` § Findings, F-24
- **Ladder:** written; next rung: `ceremony-check` with #905's fix, refusing a non-entry line in `## Entries`
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** the prose blocks were never gated (with PL-02)
- **Acceptance:** no non-entry line under `## Entries` at `fixed-at`, or the check names them

## PL-22: entry 29 numbered twice
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q2
- **Source Finding:** F-25
- **Owner area:** `docs/blindspot-register.md`
- **What:** entry 29 numbered twice
- **Where:** `02-forward-audit.md` § Findings, F-25
- **Ladder:** written; next rung: `ceremony-check` refusing a repeated entry number
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing inherited
- **Acceptance:** #811's criteria
- **Tracked:** #811

## PL-23: the legacy layout, 25 lines
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** F-26
- **Owner area:** 8 files: `worktrees.md`, `device-builds.md`, `fork-workflow.md`, `instruction-files.md`, `AGENTS.md`, `CLAUDE.md`, `es-code-traps.md`, `generic-x64-vm-testing.md`
- **What:** the legacy layout, 25 lines
- **Where:** `02-forward-audit.md` § Findings, F-26
- **Ladder:** written; next rung: a `rules-check` list of retired paths once #640 cuts over
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** the legacy checkout still exists and is the M7 lane's; nothing to migrate
- **Acceptance:** #640's cutover; the 25 lines name the layout #640 says is current
- **Tracked:** #640

## PL-24: 5,179 lines every session
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q5
- **Source Finding:** F-27
- **Owner area:** `generic-x64-vm-testing.md`, `rclone-cloud-sync.md`, `engineering-practices.md`, `handheld-evidence.md`'s glob
- **What:** 5,179 lines every session; the three largest rules mix dated narrative with instruction; `docs/**` loads `handheld-evidence.md` for any record
- **Where:** `02-forward-audit.md` § Findings, F-27
- **Ladder:** written; next rung: no tool can: a split or a narrower glob is a proposal, checked against `cross-reference.md` § Doctrine to area with the safety rules named untouched (A8)
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing inherited
- **Acceptance:** the coordinator's disposition: a stream brief with the reader cost and the cross-reference check, or withdrawn with the reason

## PL-25: upstream's PR rules (the freeze, the merge queue, the template, the artifact links) are not in the rule
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** #644 f18
- **Owner area:** `fork-workflow.md`
- **What:** upstream's PR rules (the freeze, the merge queue, the template, the artifact links) are not in the rule
- **Where:** `02-forward-audit.md` § Findings, #644 f18
- **Ladder:** written; next rung: no tool can: facts from upstream's process
- **Can this be done on the VM?** No: the tree, the tool or the register shows it (brief § 5)
- **Already written:** no series cut (D-WORKFLOW-165)
- **Acceptance:** `fork-workflow.md` states #645's established facts at `fixed-at`
- **Tracked:** #645

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: Medium
  category: Code Quality
  question: Q3
  source_finding: "F-01"
  owner_area: "the entry files: `AGENTS.md`, `CLAUDE.md`, and `tools/rules-check`"
  tracked: "#904"
  outcome: "open"
- id: PL-02
  severity: Medium
  category: Code Quality
  question: Q3
  source_finding: "F-02"
  owner_area: "the ceremony state machine: `tools/ceremony-check`, `ceremonies.md`"
  tracked: "#905"
  outcome: "open"
- id: PL-03
  severity: Low
  category: Code Quality
  question: Q3
  source_finding: "F-03"
  owner_area: "the entry files"
  tracked: "#904"
  outcome: "open"
- id: PL-04
  severity: Low
  category: Code Quality
  question: Q3
  source_finding: "F-04"
  owner_area: "the entry files"
  tracked: "#904"
  outcome: "open"
- id: PL-05
  severity: Low
  category: Code Quality
  question: Q3
  source_finding: "F-05"
  owner_area: "`CLAUDE.md`'s rule table and `rules-check`'s `mention`"
  tracked: "#808"
  outcome: "open"
- id: PL-06
  severity: Low
  category: Renovation
  question: Q7
  source_finding: "F-06"
  owner_area: "`CLAUDE.md`"
  outcome: "open"
- id: PL-07
  severity: Low
  category: Renovation
  question: Q1
  source_finding: "F-07"
  owner_area: "the entry files and the `Makefile`"
  outcome: "open"
- id: PL-08
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "F-08"
  owner_area: "the entry files"
  outcome: "open"
- id: PL-09
  severity: Low
  category: Renovation
  question: Q7
  source_finding: "F-09"
  owner_area: "the entry files and `instruction-files.md`"
  outcome: "open"
- id: PL-10
  severity: Medium
  category: Code Quality
  question: Q3
  source_finding: "F-10"
  owner_area: "`time-to-play.md`, `least-surprise.md`"
  tracked: "#906"
  outcome: "open"
- id: PL-11
  severity: Medium
  category: Code Quality
  question: Q3
  source_finding: "F-11"
  owner_area: "`generic-x64-vm-testing.md`, `es-code-traps.md`"
  tracked: "#907"
  outcome: "open"
- id: PL-12
  severity: Low
  category: Code Quality
  question: Q3
  source_finding: "F-12, F-13, F-14, F-15"
  owner_area: "`generic-x64-vm-testing.md`"
  tracked: "#908"
  outcome: "open"
- id: PL-13
  severity: Low
  category: Renovation
  question: Q1
  source_finding: "F-16"
  owner_area: "`generic-x64-vm-testing.md`"
  outcome: "open"
- id: PL-14
  severity: Low
  category: Renovation
  question: Q1
  source_finding: "F-17"
  owner_area: "`device-builds.md`, `packaging-and-patches.md`, `es-code-traps.md`, `worktrees.md`"
  outcome: "open"
- id: PL-15
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "F-18"
  owner_area: "`instruction-files.md`"
  outcome: "open"
- id: PL-16
  severity: Low
  category: Code Quality
  question: Q3
  source_finding: "F-19"
  owner_area: "`fork-workflow.md`, `device-builds.md`"
  tracked: "#910"
  outcome: "open"
- id: PL-17
  severity: Low
  category: Code Quality
  question: Q3
  source_finding: "F-20"
  owner_area: "`council-substrate-integrity.md`"
  tracked: "#911"
  outcome: "open"
- id: PL-18
  severity: Medium
  category: Code Quality
  question: Q3
  source_finding: "F-21"
  owner_area: "`rclone-cloud-sync.md`"
  tracked: "#909"
  outcome: "open"
- id: PL-19
  severity: Low
  category: Renovation
  question: Q7
  source_finding: "F-22"
  owner_area: "`instruction-files.md` and the eight rules it points at"
  outcome: "open"
- id: PL-20
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "F-23"
  owner_area: "`docs/decision-register.md`, `tools/register-check`"
  outcome: "open"
- id: PL-21
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "F-24"
  owner_area: "`docs/friction-log.md`"
  outcome: "open"
- id: PL-22
  severity: Low
  category: Code Quality
  question: Q2
  source_finding: "F-25"
  owner_area: "`docs/blindspot-register.md`"
  tracked: "#811"
  outcome: "open"
- id: PL-23
  severity: Low
  category: Renovation
  question: Q1
  source_finding: "F-26"
  owner_area: "8 files: `worktrees.md`, `device-builds.md`, `fork-workflow.md`, `instruction-files.md`, `AGENTS.md`, `CLAUDE.md`, `es-code-traps.md`, `generic-x64-vm-testing.md`"
  tracked: "#640"
  outcome: "open"
- id: PL-24
  severity: Low
  category: Renovation
  question: Q5
  source_finding: "F-27"
  owner_area: "`generic-x64-vm-testing.md`, `rclone-cloud-sync.md`, `engineering-practices.md`, `handheld-evidence.md`'s glob"
  outcome: "open"
- id: PL-25
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "#644 f18"
  owner_area: "`fork-workflow.md`"
  tracked: "#645"
  outcome: "open"
```

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | awaiting the coordinator's dispositions |
| PL-02 | Open | awaiting the coordinator's dispositions |
| PL-03 | Open | awaiting the coordinator's dispositions |
| PL-04 | Open | awaiting the coordinator's dispositions |
| PL-05 | Open | awaiting the coordinator's dispositions |
| PL-06 | Open | awaiting the coordinator's dispositions |
| PL-07 | Open | awaiting the coordinator's dispositions |
| PL-08 | Open | awaiting the coordinator's dispositions |
| PL-09 | Open | awaiting the coordinator's dispositions |
| PL-10 | Open | awaiting the coordinator's dispositions |
| PL-11 | Open | awaiting the coordinator's dispositions |
| PL-12 | Open | awaiting the coordinator's dispositions |
| PL-13 | Open | awaiting the coordinator's dispositions |
| PL-14 | Open | awaiting the coordinator's dispositions |
| PL-15 | Open | awaiting the coordinator's dispositions |
| PL-16 | Open | awaiting the coordinator's dispositions |
| PL-17 | Open | awaiting the coordinator's dispositions |
| PL-18 | Open | awaiting the coordinator's dispositions |
| PL-19 | Open | awaiting the coordinator's dispositions |
| PL-20 | Open | awaiting the coordinator's dispositions |
| PL-21 | Open | awaiting the coordinator's dispositions |
| PL-22 | Open | awaiting the coordinator's dispositions |
| PL-23 | Open | awaiting the coordinator's dispositions |
| PL-24 | Open | awaiting the coordinator's dispositions |
| PL-25 | Open | awaiting the coordinator's dispositions |
