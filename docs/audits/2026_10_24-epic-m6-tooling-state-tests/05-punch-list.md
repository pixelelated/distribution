# Punch list (Phases 5 and 6) — M6.P2 T14, the state tests (#661)

The audit issue is #1006, a sub-issue of #661. One item for each finding of `04` after the seat's grading (`04` § Second opinion), with the severities graded there. Each defect is a `bug` (D-WORKFLOW-187), and the items that are not defects carry the coordinator's disposition or lead. Seventeen bugs, #989 to #1005; five Renovation items; one conditional.

Every item answers *Can this be done on the VM?* No: the test runs on the build host, with its own fixtures and temp roots, and the proof is the test's own new case in a scratch root. No guest is involved.

## PL-01: build-identity-test fails at the hash: the state gate refuses its plain-text firmware stand-in, and its refusal cases accept any nonzero exit.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-01, G-5
- **Owner area:** the release identity tests
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-01, G-5; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #989
- **Tracked:** #989

## PL-02: rasteratops-identity-check fails at the hash on a licence literal the recipe moved past, and passes an empty gamelist and a shadowed assignment.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-02, G-6, G-36
- **Owner area:** the release identity tests
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-02, G-6, G-36; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #990
- **Tracked:** #990

## PL-03: Two cloud tests refuse the package's own rclone: pixelelated-cloud-validator-test and -duckstation-capture-test hardcode v1.75.1, the pin is 1.75.2.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-03, G-7
- **Owner area:** the cloud tests
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-03, G-7; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #991
- **Tracked:** #991

## PL-04: The real-rclone tests' sandboxes pass the caller's environment and, for three of them, the host network: a caller's TMPDIR fails them, and an RCLONE_* variable or BASH_ENV reaches the scripts.
- **Severity:** High
- **Category:** Security
- **Question:** Q2
- **Source Finding:** F-04, G-1, G-8
- **Owner area:** the cloud tests
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-04, G-1, G-8; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #992
- **Tracked:** #992

## PL-05: pixelelated-content-scope-test fails at the hash on a refusal that got safer, and several of its cases can pass without exercising what they name.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-05, G-9, G-23, G-29, G-30
- **Owner area:** the cloud tests
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-05, G-9, G-23, G-29, G-30; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #993
- **Tracked:** #993

## PL-06: pixelelated-cloud-validator-test can pass without running anything: an unknown --case passes with 0 controls, and several controls accept an empty or non-discriminating result.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-06, G-10, G-24, G-26, G-27, G-41
- **Owner area:** the cloud tests
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-06, G-10, G-24, G-26, G-27, G-41; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #994
- **Tracked:** #994

## PL-07: rocknix-info-test and nova-led-test carry their verdicts on assert and adapt production paths with unchecked replaces: under python3 -O, or PYTHONOPTIMIZE, a regression passes.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q2
- **Source Finding:** F-07, G-11, G-37
- **Owner area:** the hardware fixture tests
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-07, G-11, G-37; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #995
- **Tracked:** #995

## PL-08: retroarch-wrapper-test compares one global call count, leaves its temp sources behind, and reads a missing compiler as 'ran twice'.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-08, G-12, G-34
- **Owner area:** the RetroArch wrapper test
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-08, G-12, G-34; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #996
- **Tracked:** #996

## PL-09: The two guest tests refuse every run against current source (the migration they prove was retired by #508), and carry latent defects on their historical path: a substring kill of any QEMU naming the pair path, run even after a refused start, and a vacuous all_absent receipt; an unbound pidfile on the epic, setup failures that do not stop it, overwritten witnesses, and absence probes that pass on an ssh failure.
- **Severity:** Medium
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-09, F-10, G-2, G-13, G-14, G-21, G-22, G-23, G-33
- **Owner area:** the guest tests
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-09, F-10, G-2, G-13, G-14, G-21, G-22, G-23, G-33; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** nothing: a disposition writes nothing on a device or in a cloud
- **Acceptance:** the disposition recorded on #661 and named in Phase 7
- **Tracked:** the coordinator's disposition (#661): retire in place, with the index rows saying so, or fix the historical path; the bug count of the 21:03 ruling asks whether this is a bug or the disposition beside the stubs

## PL-10: The two retired folder-contract stubs refuse every run by design, nothing calls them, and one docstring names a stale rclone version as current coverage.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-10, F-03 (the stub's docstring)
- **Owner area:** the retired stubs
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-10, F-03 (the stub's docstring); file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** nothing: a disposition writes nothing on a device or in a cloud
- **Acceptance:** the disposition recorded on #661 and named in Phase 7
- **Tracked:** the coordinator's disposition (#661): remove with their index rows and list entries, or keep as refusing markers with the docstring corrected

## PL-11: Ten tools that still prove a live property are run by nothing in the tree: build-identity-test, nova-led-test, pixelelated-content-scope-test, pixelelated-duckstation-capture-test, pixelelated-save-layout-test, pixelelated-state-check-test, rasteratops-identity-check, usb-gadget-test, wait-lock-test, and pixelelated-cloud-validator-test.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-11, G-15
- **Owner area:** the no-caller tools
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-11, G-15; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** nothing: a disposition writes nothing on a device or in a cloud
- **Acceptance:** the disposition recorded on #661 and named in Phase 7
- **Tracked:** #986 (Backlog, T12's PL-19 shape: which suite each joins is the coordinator's)

## PL-12: Thirteen of the 21 index rows point at a Detail-in rule that never names the tool, and the two retired stubs' personal-path list entries carry no retired note.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-12, G-16
- **Owner area:** the index and its rules
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-12, G-16; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** nothing: a disposition writes nothing on a device or in a cloud
- **Acceptance:** the disposition recorded on #661 and named in Phase 7
- **Tracked:** the coordinator's lead (a rule and index edit; never made by this lane)

## PL-13: settings-modes-test and melonds-upgrade-test pass under any busybox they are given, report it as the candidate's, and settings-modes leaves host commands unshimmed and its applet path unquoted.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-13, G-4, G-17, G-39, G-41
- **Owner area:** the settings writer tests
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-13, G-4, G-17, G-39, G-41; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #997
- **Tracked:** #997

## PL-14: pixelelated-duckstation-capture-test runs its installed payload outside its sandbox and drops unknown --cases names.
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q2
- **Source Finding:** F-14, G-18, G-23
- **Owner area:** the cloud tests
- **Where:** `04-analysis.md` § Findings and § Second opinion (F-14, G-18, G-23; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #998
- **Tracked:** #998

## PL-15: The connections fixture's fake-provider guard admits a real rclone at another path and drops the stage's --config, so config create would write the caller's default configuration.
- **Severity:** Medium
- **Category:** Security
- **Question:** Q2
- **Source Finding:** G-20
- **Owner area:** the cloud fixtures
- **Where:** `04-analysis.md` § Findings and § Second opinion (G-20; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #999
- **Tracked:** #999

## PL-16: pixelelated-state-check's readiness check accepts /usr/bin/autostart anywhere in ExecStart, an argument included.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-25
- **Owner area:** the release state check
- **Where:** `04-analysis.md` § Findings and § Second opinion (G-25; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #1000
- **Tracked:** #1000

## PL-17: pixelelated-state-check's non-disclosure holds for its reports; its payload inspection writes raw selected bytes to private temp files, so the accurate guarantee is 'no value in reports', not 'no value written'.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** G-3
- **Owner area:** the release state check
- **Where:** `04-analysis.md` § Findings and § Second opinion (G-3; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** nothing: a disposition writes nothing on a device or in a cloud
- **Acceptance:** the disposition recorded on #661 and named in Phase 7
- **Tracked:** the coordinator's lead (the gate's described contract, release-candidates.md)

## PL-18: pixelelated-state-check-test credits a control when the gate fails for any reason, and never asserts its control count.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-32
- **Owner area:** the release state check
- **Where:** `04-analysis.md` § Findings and § Second opinion (G-32; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #1001
- **Tracked:** #1001

## PL-19: rasteratops-candidate-store verify resolves its argument before comparing the bundle's name with its manifest digest.
- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Source Finding:** G-38
- **Owner area:** the release candidate store
- **Where:** `04-analysis.md` § Findings and § Second opinion (G-38; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #1002
- **Tracked:** #1002

## PL-20: wait-lock-test never checks wait_lock's return status and never races two acquirers from an absent lock.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-35
- **Owner area:** the settings lock test
- **Where:** `04-analysis.md` § Findings and § Second opinion (G-35; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #1003
- **Tracked:** #1003

## PL-21: rasteratops-cloud-layout-test: the legacy backup case accepts its input archive as the new backup, and two failure controls never assert the failure.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-28, G-29, G-31
- **Owner area:** the cloud tests
- **Where:** `04-analysis.md` § Findings and § Second opinion (G-28, G-29, G-31; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #1004
- **Tracked:** #1004

## PL-22: pixelelated-save-layout-test requires both applets on every selection and lists today's source names for a historical ref.
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-40, G-41
- **Owner area:** the cloud tests
- **Where:** `04-analysis.md` § Findings and § Second opinion (G-40, G-41; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #1005
- **Tracked:** #1005

## PL-23: The lint's fail fixture couples two violations (the renovation face and question:), so a runner that checks only pass and fail would not prove either guard alone.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q3
- **Source Finding:** G-42
- **Owner area:** the lint fixtures
- **Where:** `04-analysis.md` § Findings and § Second opinion (G-42; file:line at `8ebaf8daad`, or `2174265e9c` for a lint fixture)
- **Can this be done on the VM?** No: the tree, or a test run in a scratch root, shows it
- **Already written:** nothing: a disposition writes nothing on a device or in a cloud
- **Acceptance:** the disposition recorded on #661 and named in Phase 7
- **Tracked:** the coordinator's read after T10's #945 merges: its run.sh (2444828e89) names the failure it expects, which may already answer this

## Index

```yaml
punch_index:
- id: PL-01
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-01, G-5"
  tracked: "#989"
  outcome: "resolved"
- id: PL-02
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-02, G-6, G-36"
  tracked: "#990"
  outcome: "resolved"
- id: PL-03
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-03, G-7"
  tracked: "#991"
  outcome: "resolved"
- id: PL-04
  severity: High
  category: Security
  question: Q2
  source_finding: "F-04, G-1, G-8"
  tracked: "#992"
  outcome: "resolved"
- id: PL-05
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-05, G-9, G-23, G-29, G-30"
  tracked: "#993"
  outcome: "resolved"
- id: PL-06
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-06, G-10, G-24, G-26, G-27, G-41"
  tracked: "#994"
  outcome: "resolved"
- id: PL-07
  severity: Medium
  category: Correctness
  question: Q2
  source_finding: "F-07, G-11, G-37"
  tracked: "#995"
  outcome: "resolved"
- id: PL-08
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-08, G-12, G-34"
  tracked: "#996"
  outcome: "resolved"
- id: PL-09
  severity: Medium
  category: Renovation
  question: Q6
  source_finding: "F-09, F-10, G-2, G-13, G-14, G-21, G-22, G-23, G-33"
  tracked: "#1011 (the live path, resolved); retire in place, the removal on #346"
  outcome: "resolved"
- id: PL-10
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "F-10, F-03 (the stub's docstring)"
  tracked: "retire in place, the docstring resolved; the removal on #346, the list entries #1007"
  outcome: "resolved"
- id: PL-11
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "F-11, G-15"
  tracked: "#986"
  outcome: "deferred"
- id: PL-12
  severity: Low
  category: Renovation
  question: Q7
  source_finding: "F-12, G-16"
  tracked: "#1007"
  outcome: "deferred"
- id: PL-13
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-13, G-4, G-17, G-39, G-41"
  tracked: "#997"
  outcome: "resolved"
- id: PL-14
  severity: Low
  category: Correctness
  question: Q2
  source_finding: "F-14, G-18, G-23"
  tracked: "#998"
  outcome: "resolved"
- id: PL-15
  severity: Medium
  category: Security
  question: Q2
  source_finding: "G-20"
  tracked: "#999"
  outcome: "resolved"
- id: PL-16
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "G-25"
  tracked: "#1000"
  outcome: "resolved"
- id: PL-17
  severity: Low
  category: Renovation
  question: Q7
  source_finding: "G-3"
  tracked: "a5397e2e9f; the rules' sentence #1007"
  outcome: "resolved"
- id: PL-18
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "G-32"
  tracked: "#1001"
  outcome: "resolved"
- id: PL-19
  severity: Medium
  category: Security
  question: Q3
  source_finding: "G-38"
  tracked: "#1002"
  outcome: "resolved"
- id: PL-20
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "G-35"
  tracked: "#1003"
  outcome: "resolved"
- id: PL-21
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "G-28, G-29, G-31"
  tracked: "#1004"
  outcome: "resolved"
- id: PL-22
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-40, G-41"
  tracked: "#1005"
  outcome: "resolved"
- id: PL-23
  severity: Low
  category: Renovation
  question: Q3
  source_finding: "G-42"
  tracked: "7679426e48; run.sh's lines at #945's merge"
  outcome: "resolved"
```

## Phase 7 resolution gate

At the resolution phase. Each bug's fix is on this branch, and the bug closes when it reaches `next` (no closing keyword). The items that are not streams carry the coordinator's dispositions (#661, the stream brief at `13242d182a`). Each row names the commit or the issue.

| Item | Outcome | Tracked |
| --- | --- | --- |
| PL-01 | Resolved | `3c9730bc78` (S1), #989 |
| PL-02 | Resolved | `648e9ca228` (S1), #990 |
| PL-03 | Resolved | `2f614eef1f` (S3), #991 |
| PL-04 | Resolved | `2e6639ec57` (S2), #992 |
| PL-05 | Resolved | `6b41f05962` (S4), #993 |
| PL-06 | Resolved | `6b5cd16160` (S3), #994 |
| PL-07 | Resolved | `359dd435ce`, `081f19d2f0` (S6), #995; and #1009, the scratch leak found during S7, fixed in `84a2b73140` (which cites #995) and filed after it, per the coordinator's 22:22 UTC ruling |
| PL-08 | Resolved | `0037b04172` (S7), #996 |
| PL-09 | Resolved | `6016f57a75` (S11), #1011, the live path: a refused start stops nothing, and a stop goes by pidfile in D-INFRA-031's runtime shape (the coordinator, 22:54 UTC). The disposition is the coordinator's: retire in place as a refusing marker, with the removal bundle on #346 and the index rows #1007's |
| PL-10 | Resolved | `8816d078fa` (S11), the docstring naming the coverage by tool and flow. The disposition is the coordinator's: retire in place as refusing markers, with the removal bundle on #346 and the list entries #1007's |
| PL-11 | Deferred | #986, the coordinator's Backlog, with T14's ten tools and the suites each could join; the validator's own defects are #994, resolved in `6b5cd16160` |
| PL-12 | Deferred | #1007, the T14 rules Backlog (a sub-issue of #903), made at integration in the doctrine packet; no rule was edited by this lane |
| PL-13 | Resolved | `929355c417`, `30d9339ea3`, `4e94ccd833` (S8), #997. Under --unverified-busybox a failing case exits 1 and an all-pass run exits 3, with the marker on every line in both (the coordinator, 22:29 UTC); last-good-scripts-test's host fallback is #662's lead. T15 passes a copied busybox (`--busybox "${BB_HOST}"`, `:14224`, `:14231`), which this contract refuses (CANNOT, exit 2) even for a build root's busybox; its call is #662's file, and the fix is put to the coordinator on #661 |
| PL-14 | Resolved | `fe41fca9a9`, `802bb51924` (S3), #998 |
| PL-15 | Resolved | `89efee384c`, `9df25309f3` (S2; the follow-up puts `--config` after the command, where T15's shims read it, found by the close-out's last-good-scripts-test run), #999 |
| PL-16 | Resolved | `3657e0e801` (S9), #1000: two shapes, a constant, and a tree-side drift check (the coordinator, 22:30 UTC); the gate's requirement is unchanged |
| PL-17 | Resolved | `a5397e2e9f` (S9): the header states no value in reports, and the scratch is removed on every exit, signals included; the rules' sentence is #1007's, and release-candidates.md's gate contract is unchanged |
| PL-18 | Resolved | `b74dcaa78b` (S9), #1001: the self-test-only limit is in SELF_TEST_CONTROLS' comment, and the payload half is Backlog #1010 (the coordinator, 22:46 UTC) |
| PL-19 | Resolved | `64ea405f3f` (S9), #1002 |
| PL-20 | Resolved | `bcf5a013ad` (S10), #1003 |
| PL-21 | Resolved | `c25f69d19a`, `ef31b4bf22` (S5), #1004: the backups' historical contract, rc 0, COMPLETED and the configured folder (the coordinator, 22:08 UTC) |
| PL-22 | Resolved | `15bce9aa23` (S5), #1005 |
| PL-23 | Resolved | `7679426e48` (S12): fixture-epic-m6-renovation-fail-face and fixture-epic-m6-renovation-fail-question; run.sh gains its two lines at #945's merge (the coordinator's) |
