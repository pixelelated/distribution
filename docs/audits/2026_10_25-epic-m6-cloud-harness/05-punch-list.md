# Punch list (Phases 5 and 6) — M6.P2 T13, the cloud test harness (#660)

The audit issue is #1073, a sub-issue of #660. One item per finding of `04` after the seat's grading (`04` § Second opinion), with the severities graded there. Each proven defect is a `bug` (D-WORKFLOW-187) filed at stage D (#1057 to #1070, and #1081 for PL-22 after the coordinator's ruling); its fix is a stage-E stream under a brief the coordinator writes after the stage-D pause. The items that are not bugs are designs, leads or deferrals, each named where it goes.

## PL-01: cloud-round-trip: A5 and RETENTION call cloud_reconcile, which has never existed, and RETENTION prints two PASS lines when nothing ran
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-01, F-02, G-10, G-11
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-01, F-02, G-10, G-11; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** No: the tool and its constructed case run on the build host; no guest is needed
- **Already written:** #1057's *Already written:* line
- **Acceptance:** the criteria of #1057
- **Tracked:** #1057

## PL-02: cloud-test-backend: --backend after the subcommand is accepted in silence and the tool answers for another backend
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-03, G-18
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-03, G-18; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** No: the tool and its constructed case run on the build host; no guest is needed
- **Already written:** #1058's *Already written:* line
- **Acceptance:** the criteria of #1058
- **Tracked:** #1058

## PL-03: cloud-round-trip: the run's verdict does not account for what it checked (a bare PASSED, a discarded equipment check, an unsatisfiable --only)
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-05, F-17, G-20, G-32
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-05, F-17, G-20, G-32; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** No: the tool and its constructed case run on the build host; no guest is needed
- **Already written:** #1059's *Already written:* line
- **Acceptance:** the criteria of #1059
- **Tracked:** #1059

## PL-04: cloud-test-backend ls and reset report a failure as an empty endpoint, and cloud-round-trip's absence-only checks pass on it
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-12, F-22, G-27, G-28, G-40
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-12, F-22, G-27, G-28, G-40; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** No: the tool and its constructed case run on the build host; no guest is needed
- **Already written:** #1060's *Already written:* line
- **Acceptance:** the criteria of #1060
- **Tracked:** #1060

## PL-05: cloud-connections-test carries a credential-shaped fixture literal at rest that T10's widened pre-commit pattern matches
- **Severity:** Low
- **Category:** Hygiene
- **Question:** Q2
- **Source Finding:** F-14
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-14; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** No: the tool and its constructed case run on the build host; no guest is needed
- **Already written:** #1061's *Already written:* line
- **Acceptance:** the criteria of #1061
- **Tracked:** #1061

## PL-06: cloud-round-trip: KILL1 raises NameError before its verdict, and its preservation predicate passes a deleted cloud file
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-15, G-30, G-35
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-15, G-30, G-35; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** Yes: the fixed cell's run on one QA guest is the proof; the defect is shown on the host from the code
- **Already written:** #1062's *Already written:* line
- **Acceptance:** the criteria of #1062
- **Tracked:** #1062

## PL-07: cloud-round-trip: CONTRACT's dry-run conflict guard fires on every dry run, so a missed conflict passes
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-16, G-31
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-16, G-31; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** No: the tool and its constructed case run on the build host; no guest is needed
- **Already written:** #1063's *Already written:* line
- **Acceptance:** the criteria of #1063
- **Tracked:** #1063

## PL-08: cloud-round-trip: step 25 passes when its probe finds no ES paths at all
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-18, G-33
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-18, G-33; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** Yes: the fixed cell's run on one QA guest is the proof; the defect is shown on the host from the code
- **Already written:** #1064's *Already written:* line
- **Acceptance:** the criteria of #1064
- **Tracked:** #1064

## PL-09: cloud-round-trip: CAP13's warning check passes when no warning was logged (grep -c || echo 0 yields 0 twice)
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-19, G-34
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-19, G-34; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** No: the tool and its constructed case run on the build host; no guest is needed
- **Already written:** #1065's *Already written:* line
- **Acceptance:** the criteria of #1065
- **Tracked:** #1065

## PL-10: cloud-round-trip: step 8 refuses an occupied /storage/roms/vectrex and its cleanup then deletes it
- **Severity:** High
- **Category:** Safety
- **Question:** Q3
- **Source Finding:** F-20, G-44
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-20, G-44; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** No: the tool and its constructed case run on the build host; no guest is needed
- **Already written:** #1066's *Already written:* line
- **Acceptance:** the criteria of #1066
- **Tracked:** #1066

## PL-11: cloud-test-backend: the SFTP QA endpoint is not confined to its data directory, and its guest key authenticates as the host's own user
- **Severity:** High
- **Category:** Security
- **Question:** Q2
- **Source Finding:** F-21, G-42
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-21, G-42; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** No: the tool and its constructed case run on the build host; no guest is needed
- **Already written:** #1067's *Already written:* line
- **Acceptance:** the criteria of #1067; its second checkbox was rewritten under the coordinator's ruling on #660 (06:17 UTC) to what the artifact proves -- the QA key is the only credential accepted, a QA-key login under any user name is confined to the data directory and reaches no shell and no host account -- and ticked from the evidence on #1067 (issuecomment-6394310968)
- **Tracked:** #1067

## PL-12: cloud-test-backend: connection stanzas fall back to the clear password when rclone obscure fails
- **Severity:** Low
- **Category:** Security
- **Question:** Q2
- **Source Finding:** F-22, G-43
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-22, G-43; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** No: the tool and its constructed case run on the build host; no guest is needed
- **Already written:** #1068's *Already written:* line
- **Acceptance:** the criteria of #1068
- **Tracked:** #1068

## PL-13: cloud-round-trip: A15 uploads plain bytes named .tar.gz, which cloud_backup refuses, so A15 fails before the behaviour it names
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-23, G-46
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-23, G-46; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** Yes: the fixed cell's run on one QA guest is the proof; the defect is shown on the host from the code
- **Already written:** #1069's *Already written:* line
- **Acceptance:** the criteria of #1069
- **Tracked:** #1069

## PL-14: cloud-round-trip: KILL5 expects three archives after retention whatever CLOUD_BACKUP_KEEP says
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-24, G-47
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-24, G-47; file:line at `8ebaf8daad`)
- **Can this be done on the VM?** Yes: the fixed cell's run on one QA guest is the proof; the defect is shown on the host from the code
- **Already written:** #1070's *Already written:* line
- **Acceptance:** the criteria of #1070
- **Tracked:** #1070

## PL-15: caps() marks no step of the single-device suite, and nothing in a run's output says which capabilities the backend had
- **Severity:** Low
- **Category:** Design
- **Question:** Q2
- **Source Finding:** F-04, G-19
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` (F-04, G-19)
- **Can this be done on the VM?** No: the tree shows it; no guest is needed
- **Already written:** nothing
- **Acceptance:** a design recorded here: running one assertion set over several real protocols is useful qualification (G-19); the missing piece is the backend's capabilities printed beside the verdict, which #1059's verdict line carries
- **Tracked:** #1059

## PL-16: cloud-pair-migration is retired by code, and no tool proves a mixed installation under D-CLOUD-175's /pixelelated default
- **Severity:** Medium
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-06, F-13, G-12, G-14, G-15, G-21, G-29
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` (F-06, F-13, G-12, G-14, G-15, G-21, G-29)
- **Can this be done on the VM?** No: the tree shows it; no guest is needed
- **Already written:** it ran only on QA guests; its proofs stay in history (`docs/vm-qa-log.md:32`; the 2026-10-05 entry)
- **Acceptance:** deferred to #1055 (the coordinator's ruling on #660, 05:22 UTC): the proof is owed there, and the tool's removal waits for its skeleton to be ported (G-14)
- **Tracked:** #1055

## PL-17: vm-qa never downs the QA backend it brought up, and its guest disks and sockets default to /tmp; cloud-test-backend's down kills any listener on its port
- **Severity:** Medium
- **Category:** Brittleness
- **Question:** Q1
- **Source Finding:** F-07, G-22
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` (F-07, G-22)
- **Can this be done on the VM?** No: the tree shows it; no guest is needed
- **Already written:** nothing
- **Acceptance:** a lead for `vm-qa` (T12's file) and for `cloud-test-backend`'s `down` (the port sweep is the non-container branch, G-22); deferred to #1075, the coordinator's Backlog (the stage-D question)
- **Tracked:** #1075

## PL-18: rclone-cloud-sync.md says the no-network step checks exit 4 (the tool asserts 69), and its paths: names four of the nine
- **Severity:** Low
- **Category:** Documentation
- **Question:** Q7
- **Source Finding:** F-08, G-23
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` (F-08, G-23)
- **Can this be done on the VM?** No: the tree shows it; no guest is needed
- **Already written:** nothing
- **Acceptance:** deferred to #909 for the stale sentence (T4's fix `fcc7046f0e`), and to the coordinator for `paths:` (a rule edit is the coordinator's)
- **Tracked:** #909

## PL-19: four tools judge with the host's rclone or the host's bash without saying so in their output (D-QA-063)
- **Severity:** Low
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** F-09, G-24
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` (F-09, G-24)
- **Can this be done on the VM?** No: the tree shows it; no guest is needed
- **Already written:** nothing
- **Acceptance:** a lead: each prints whose tools judged; deferred to #1076, the coordinator's Backlog
- **Tracked:** #1076

## PL-20: the QA backends' MinIO and Samba images are unpinned :latest and pyftpdlib is installed unpinned
- **Severity:** Low
- **Category:** Currency
- **Question:** Q4
- **Source Finding:** F-10, G-25
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` (F-10, G-25)
- **Can this be done on the VM?** No: the tree shows it; no guest is needed
- **Already written:** nothing
- **Acceptance:** a lead: pin by digest and version, and print the resolved identity in `caps`; deferred to #1077, the coordinator's Backlog
- **Tracked:** #1077

## PL-21: fixed waits stand in for an event at cloud-round-trip:4915, 6692, 7455, 7496 and 7500 (blindspot 32)
- **Severity:** Low
- **Category:** Brittleness
- **Question:** Q3
- **Source Finding:** F-11, G-26, G-37
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` (F-11, G-26, G-37)
- **Can this be done on the VM?** No: the tree shows it; no guest is needed
- **Already written:** nothing
- **Acceptance:** leads, none seen failing; deferred to #1078, the coordinator's Backlog with G-37's timing windows
- **Tracked:** #1078

## PL-22: cloud-census is not read-only: it runs cloud_device_id over SSH on the host it reads (tools/cloud-census:76)
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q6
- **Source Finding:** F-25, G-48
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` (F-25, G-48)
- **Can this be done on the VM?** No: the tree shows it; no guest is needed
- **Already written:** #1081's *Already written:* line
- **Acceptance:** the criteria of #1081 (the coordinator's 05:52 UTC ruling on #660: drop the call; stage E's third stream, with #1061)
- **Tracked:** #1081

## PL-23: the seat's further leads, accepted on its citations and not re-read: kill witnesses, the vocabulary gate, the litter scan, endpoint health, cleanup outside the verdict, three small tests' blind spots, the verifier's symlinked ancestors
- **Severity:** Low
- **Category:** Brittleness
- **Question:** Q3
- **Source Finding:** F-26, G-36, G-37, G-38, G-39, G-41, G-45, G-49, G-50, G-51, G-53
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` (F-26, G-36, G-37, G-38, G-39, G-41, G-45, G-49, G-50, G-51, G-53)
- **Can this be done on the VM?** No: the tree shows it; no guest is needed
- **Already written:** nothing
- **Acceptance:** deferred to #1079, the coordinator's Backlog, each with its G-number and lines
- **Tracked:** #1079

## PL-24: six of the seven uncalled tools have no caller; three host tests could be vm-qa host suites
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** 04 § Q6
- **Owner area:** the cloud test harness
- **Where:** `04-analysis.md` (04 § Q6)
- **Can this be done on the VM?** No: the tree shows it; no guest is needed
- **Already written:** nothing
- **Acceptance:** the dispositions in 04 § Q6: keep `cloud-connections-test`, `cloud-input-test`, `cloud-capture-stamp-test`, `cloud-save-integrity-test` and `cloud-save-integrity`; the wiring into `vm-qa` is T12's file, deferred to #1080, the coordinator's Backlog
- **Tracked:** #1080

## Index

```yaml
punch_index:
- id: PL-01
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-01, F-02, G-10, G-11"
  tracked: "#1057"
  outcome: "open"
- id: PL-02
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-03, G-18"
  tracked: "#1058"
  outcome: "resolved"
- id: PL-03
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-05, F-17, G-20, G-32"
  tracked: "#1059"
  outcome: "resolved"
- id: PL-04
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-12, F-22, G-27, G-28, G-40"
  tracked: "#1060"
  outcome: "resolved"
- id: PL-05
  severity: Low
  category: Hygiene
  question: Q2
  source_finding: "F-14"
  tracked: "#1061"
  outcome: "resolved"
- id: PL-06
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-15, G-30, G-35"
  tracked: "#1062"
  outcome: "resolved"
- id: PL-07
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-16, G-31"
  tracked: "#1063"
  outcome: "resolved"
- id: PL-08
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-18, G-33"
  tracked: "#1064"
  outcome: "resolved"
- id: PL-09
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-19, G-34"
  tracked: "#1065"
  outcome: "resolved"
- id: PL-10
  severity: High
  category: Safety
  question: Q3
  source_finding: "F-20, G-44"
  tracked: "#1066"
  outcome: "resolved"
- id: PL-11
  severity: High
  category: Security
  question: Q2
  source_finding: "F-21, G-42"
  tracked: "#1067"
  outcome: "open"
- id: PL-12
  severity: Low
  category: Security
  question: Q2
  source_finding: "F-22, G-43"
  tracked: "#1068"
  outcome: "resolved"
- id: PL-13
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-23, G-46"
  tracked: "#1069"
  outcome: "resolved"
- id: PL-14
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-24, G-47"
  tracked: "#1070"
  outcome: "resolved"
- id: PL-15
  severity: Low
  category: Design
  question: Q2
  source_finding: "F-04, G-19"
  tracked: "#1059"
  outcome: "resolved"
- id: PL-16
  severity: Medium
  category: Renovation
  question: Q6
  source_finding: "F-06, F-13, G-12, G-14, G-15, G-21, G-29"
  tracked: "#1055"
  outcome: "deferred"
- id: PL-17
  severity: Medium
  category: Brittleness
  question: Q1
  source_finding: "F-07, G-22"
  tracked: "#1075"
  outcome: "deferred"
- id: PL-18
  severity: Low
  category: Documentation
  question: Q7
  source_finding: "F-08, G-23"
  tracked: "#909"
  outcome: "deferred"
- id: PL-19
  severity: Low
  category: Standards
  question: Q2
  source_finding: "F-09, G-24"
  tracked: "#1076"
  outcome: "deferred"
- id: PL-20
  severity: Low
  category: Currency
  question: Q4
  source_finding: "F-10, G-25"
  tracked: "#1077"
  outcome: "deferred"
- id: PL-21
  severity: Low
  category: Brittleness
  question: Q3
  source_finding: "F-11, G-26, G-37"
  tracked: "#1078"
  outcome: "deferred"
- id: PL-22
  severity: Medium
  category: Correctness
  question: Q6
  source_finding: "F-25, G-48"
  tracked: "#1081"
  outcome: "resolved"
- id: PL-23
  severity: Low
  category: Brittleness
  question: Q3
  source_finding: "F-26, G-36, G-37, G-38, G-39, G-41, G-45, G-49, G-50, G-51, G-53"
  tracked: "#1079"
  outcome: "deferred"
- id: PL-24
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "04 § Q6"
  tracked: "#1080"
  outcome: "deferred"
```

## Phase 7 resolution gate

After the guest cycle (#660: START 07:52, RETURN 08:10 UTC; the record `stage-e/cycle/`, `02` § The guest cycle). A bug closes when its fix reaches `next` (no closing keyword); the six whose guest criterion waits are Open until the cycle's lines are in 02 § The guest cycle. The non-bug items carry the coordinator's dispositions (#660, 05:22 and 05:52 UTC).

| Item | Outcome | Tracked |
| --- | --- | --- |
| PL-01 | Open | fixed in `09ca086062` (#1057); its guest criterion was **not met** on the cycle (#660, 08:10 RETURN): step 5b with device b being guest a itself was refused by the harness's #91 guard (one id, one MAC), rc 2; it needs a two-guest window |
| PL-02 | Resolved | `0cceb65207` (#1058) |
| PL-03 | Resolved | `e71d077882`, `cee4bf481d` (#1059: the verdict line, the refusals, the equipment stop; nothing checked exits 3 under the 06:33 UTC ruling) |
| PL-04 | Resolved | `7345a65e9d` (backend half), `1e28ba8f94` (harness half) (#1060) |
| PL-05 | Resolved | `1911fee4df` (#1061) |
| PL-06 | Resolved | `332bda1515` (#1062); on the guest (`a5522b8eb8`, `stage-e/cycle/f-kill1.out`) KILL1 reached its verdict (21 passed, 3 failed: the re-runs exit 124 under the throttle, a new finding for stage F) |
| PL-07 | Resolved | `539622b9d7` (#1063) |
| PL-08 | Resolved | `bde357126c` (#1064); on the guest step 25 read 128 ES paths (`stage-e/cycle/vm-qa-webdav/round-trip.log`) |
| PL-09 | Resolved | `f7482f9684`, `a70b4889a3` (#1065; the needle corrected in-window to the image's words); on the guest CAP13 PASSED with the warning present and FAILED with it absent (`stage-e/cycle/f-cap13-*.out`) |
| PL-10 | Resolved | `7f0e527800` (#1066) |
| PL-11 | Open | fixed in `94c050ed5a` (#1067: the confinement proven, the second criterion ticked under the 06:17 ruling), but the guest cycle found a regression: over the new `rclone serve sftp` endpoint the suite fails 7 content-tier checks that the old sshd endpoint passes on the same guest (`stage-e/cycle/vm-qa-sftp/`, `u-suite-sftp.out`); the coordinator's call on #660 (RETURN, 08:10) |
| PL-12 | Resolved | `91267b0dda` (#1068) |
| PL-13 | Resolved | `0c538b1f74` (#1069); on the guest A15 reached its verdict with the backup landing (36 passed, 2 failed: two log-wording checks failing on both trees, a separate finding for stage F) |
| PL-14 | Resolved | `77e7b16193` (#1070); on the guest KILL5 PASSED at keep 3 and at `CLOUD_BACKUP_KEEP=2` (`stage-e/cycle/f-kill5-keep*.out`) |
| PL-15 | Resolved | `e71d077882` (#1059: the backend's capabilities on the verdict line) |
| PL-16 | Deferred | #1055, the coordinator's mixed-installation Backlog (05:22 UTC ruling); the tool stays retired |
| PL-17 | Deferred | #1075 |
| PL-18 | Deferred | #909 (the stale sentence); the rule's `paths:` is the coordinator's rule-edit packet |
| PL-19 | Deferred | #1076 |
| PL-20 | Deferred | #1077 |
| PL-21 | Deferred | #1078 |
| PL-22 | Resolved | `bf2832ce5b` (#1081) |
| PL-23 | Deferred | #1079 |
| PL-24 | Deferred | #1080 |
