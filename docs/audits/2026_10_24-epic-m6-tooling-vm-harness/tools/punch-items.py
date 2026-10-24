#!/usr/bin/env python3
"""05-punch-list.md from one list (#659): the items, the punch_index and the Phase 7 table.

    python3 -I punch-items.py > ../05-punch-list.md
"""
HOST = "Yes, on the VM: a GENERIC_X64 guest from the newest image, or the tool's own control with synthetic inputs where it has one; nothing on a device (brief § 5)"
HOSTONLY = "Yes: host-side; the proof is the tool's control or a constructed input in the lane's worktree, no guest needed"
AWN = "nothing inherited: these are QA-host tools; what they leave is reports under `$ROCKNIX_ARTIFACTS`, disposable guests and the host's `/tmp` and `~/.cache`, never a device or a person's cloud"

I = [
 dict(f="F-01, G-01, G-40", t="`vm-qa` reports a pass that did not pass: it exits 0 over a SKIP, and an unknown or empty `--only` or `--walk` runs nothing and passes", sev="Medium", cat="Bug", q="Q3", bug=True, tracked="#966",
  area="`tools/vm-qa`", what="The exit and the footer count what was selected against what ran and passed: a SKIP is not a pass in the exit code (the coordinator decides whether a SKIP fails the run or is a distinct exit, D-QA-022), an unknown suite or walk name is refused, an empty selection is refused.",
  where="`vm-qa:74`, `:85-90`, `:141-150`, `:438-445`, `:528`, `:541`", ev="P7 (the cycle: `PASSED with 1 suite(s) SKIPPED`, rc 0); the seat's G-01, G-40", vm=HOST, aw=AWN,
  acc="a constructed run with `frame-diff` SKIPped (an empty `WALK_BASELINE`) exits non-zero or with a distinct SKIP code, quoted; `--only nosuch` and `--walk ,` exit 2, quoted; the unfixed tool's rc 0 for each recorded beside them."),
 dict(f="F-02, G-08, G-09, G-10, G-12", t="`time-to-play` accepts a measurement it did not make: zero repeats, a failing sync's stamp, a g2g without its stamp, an unjudged startup or condition, an already-running RetroArch", sev="Medium", cat="Bug", q="Q3", bug=True, tracked="#967",
  area="`tools/time-to-play`", what="Refuse `--repeat` below 1 and an `--only` naming no cell; time the exit sync only on a completed stamp (rc and token read); require g2g's stamp; judge the cells that ran beyond the three headlines; require a launch to start a RetroArch that was not running. What the headline rule accepts is the coordinator's contract (D-QA-022, D-CLOUD-122): this item names the inputs, and the rule's change is briefed.",
  where="`time-to-play:994-1021`, `:641-647`, `:685-689`, `:1227-1252`, `:1306-1332`, `:524-590`", ev="P8 (`--repeat 0`: rc 0, cells empty); the cycle's g2g row (stamp `-`, token `?`, PASS); the seat's G-08 to G-12", vm=HOST, aw=AWN,
  acc="on a guest: `--repeat 0` exits 2; a constructed failing exit-sync stamp is not timed as a sync; a g2g row without its stamp fails; each with the unfixed tool's result beside it."),
 dict(f="F-03, G-49", t="`emulator-exit-test --only` without A to D prints PASSED having checked nothing, and part D cannot prove the marker's lifetime alone", sev="Low", cat="Bug", q="Q3", bug=True, tracked="#968",
  area="`tools/emulator-exit-test`", what="Refuse an `--only` with no known part; make D's marker check independent of C's cleanup, or say it runs only after A to C.",
  where="`emulator-exit-test:38`, `:145-196`, `:185`, `:192-194`", ev="P9 (`--only X`: PASSED, rc 0)", vm=HOST, aw=AWN,
  acc="on a guest: `--only X` exits 2, quoted; `--only D` alone either constructs the marker case or is refused; the unfixed tool's PASSED beside it."),
 dict(f="G-02, G-30", t="`vm-qa`'s bring-up hides its own failure: `vm-pair down` is ignored and `up`'s status is masked by `tail`, so a surviving guest's build gets a green report naming the requested image; nothing tears the pair down", sev="High", cat="Bug", q="Q3", bug=True, tracked="#969",
  area="`tools/vm-qa`, `tools/vm-upgrade-rehearsal`", what="Fail the run when `down` or `up` fails (`PIPESTATUS`), and compare the guest's `BUILD_ID` with the image the run names; stop the pair at the end of a run that brought it up; the rehearsal fails when its stop fails.",
  where="`vm-qa:119-125`, `:139`, `:528-541`; `vm-upgrade-rehearsal:57`, `:62`, `:144`, `:167-170`", ev="the seat's G-02, G-30; verified at the lines (`seat-verify.md`)", vm=HOST, aw=AWN,
  acc="a constructed `vm-pair` double whose `up` fails while a guest answers: the fixed runner exits non-zero and names the mismatch; the unfixed one's green report beside it."),
 dict(f="G-27, G-29, F-09 (the shared directory)", t="`vm-pair` deletes the guests' disks after a stop that found no pidfile, and leaves a partial launch running", sev="High", cat="Interaction Defect", q="Q3", bug=True, tracked="#970",
  area="`tools/vm-pair`, `tools/vm-stop`", what="Before `rm` of a disk, refuse while any process holds it open (or while a QEMU's argv names it), not only while a recorded pidfile says so; roll back a partial `up`; `down` stops both guests even when one fails.",
  where="`vm-stop:15-17`; `vm-pair:136-137`, `:146-147`, `:157-158`, `:164-167`", ev="the seat's G-27, G-29; verified at the lines", vm=HOSTONLY + " (`vm-pair-test` gains the case: a live fixture holding the disk with no pidfile)", aw=AWN,
  acc="`vm-pair-test`'s new case: a live process holding `vm-a.qcow2` with no pidfile; `up` refuses and the file survives; it fails on the unfixed tool, quoted."),
 dict(f="F-09, F-10, G-05, G-17, G-53", t="The harness's host state assumes one session on the host: the pair's disks in a RAM tmpfs, fixed sockets, pidfiles and ports, the QA cloud's state per user and reset by the walks, predictable `/tmp` files, one report directory per minute", sev="Medium", cat="Interaction Defect", q="Q2", bug=True, tracked="#971",
  area="`tools/vm-pair`, `tools/vm-qa`, `tools/ra-offline-test`, `tools/time-to-play`", what="Run-owned defaults under `/workspace/tmp/<run>`, or a refusal when another session's state is present: `VM_PAIR_DIR`, `VM_QEMU_RUNTIME_DIR`, `CLOUD_QA_STATE`, `CLOUD_QA_PORT`, the report directory, the host `/tmp` files. The defaults are the coordinator's to choose (the host file; D-INFRA-022).",
  where="`vm-pair:37`, `:41`, `:63-64`; `vm-qa:98-99`, `:118`, `:131`, `:397`; `cloud-test-backend:93` (context); `ra-offline-test:259`, `:345`; `time-to-play:137-139`, `:158`", ev="`findmnt /tmp` (tmpfs 30.4G); the cycle's five overrides (`00`); the seat's G-05, G-17, G-53", vm=HOST, aw=AWN,
  acc="a second `vm-qa` started beside a running one on the same host either uses its own state (the paths printed) or refuses, quoted; nothing under `/tmp` written by a run, read by `find /tmp -newer` before and after."),
 dict(f="F-08, G-37, G-34, G-41", t="A failed screendump is silent: a walk warns and continues, and `wait-for-change` counts a missing frame as a landed key", sev="Medium", cat="Bug", q="Q3", bug=True, tracked="#972",
  area="`tools/vm-visual-qa`", what="A missing frame is a failure for `wait-for-change` (never 100 % change); a walk that captured fewer shots than its file names exits non-zero; the PPM header loop ends at EOF.",
  where="`vm-visual-qa:335-375`, `:524-530`, `:559-577`, `:434-449`, `:651-659`", ev="the seat's G-37, G-34; `frame()` returns None on a failed dump (`:306-320`)", vm=HOST + " (a monitor socket that refuses `screendump`)", aw=AWN,
  acc="a constructed monitor that accepts `sendkey` and fails `screendump`: the fixed walk exits non-zero at the first `wait-for-change`; the unfixed one exits 0, quoted."),
 dict(f="F-05, G-70", t="The walks start after a reboot wait that neither fails when EmulationStation never answers nor checks that a new boot happened", sev="Medium", cat="Bug", q="Q3", bug=True, tracked="#973",
  area="`tools/vm-qa`", what="The wait requires a changed boot id and an answering EmulationStation, and fails the walk when it does not get them.",
  where="`vm-qa:476-477`", ev="tree; the seat's G-70", vm=HOST, aw=AWN,
  acc="a constructed guest whose EmulationStation is stopped before the reboot's wait: the walk fails, quoted, where the unfixed runner walks on."),
 dict(f="F-06, G-42, G-43, G-44", t="The walks' fixture is assumed, not checked: seeding failures are silent, one surviving file skips reseeding, any active remote is accepted for destructive walks, and the manager fixture overwrites named ROMs and saves", sev="Medium", cat="Bug", q="Q2", bug=True, tracked="#974",
  area="`tools/vm-qa`", what="Check every seeding step's exit; verify the active remote is the QA backend's (its endpoint) before a walk that presses YES on a match or transfers; reseed on a manifest, not one file; refuse to overwrite a guest's own files.",
  where="`vm-qa:304-318`, `:341`, `:376-386`, `:389-408`", ev="the seat's G-42 to G-44; `match-dialog.steps:19-26`", vm=HOST, aw=AWN,
  acc="a guest whose active remote is not the QA endpoint: the walks refuse before the first walk, quoted; a seeding failure fails the suite, quoted; each beside the unfixed runner's result."),
 dict(f="F-04", t="`vm-manager-system-check` refuses with `assert`, so `-O` or `PYTHONOPTIMIZE` turns every refusal into a PASS; six more tools check with `assert`", sev="Medium", cat="Bug", q="Q2", bug=True, tracked="#975",
  area="`tools/vm-manager-system-check` (and the class: `ra-ui-test`, `raofflineproxy-consent-test`, `raofflineproxy-installed-native-test`, `vm-pair-test`, `vm-stop-test`, `vm-upgrade-readiness-test`)", what="Explicit checks that raise; the controls either the same or refuse to run optimised.",
  where="`vm-manager-system-check:12-15`", ev="P6", vm=HOSTONLY, aw=AWN,
  acc="`echo '[]' | PYTHONOPTIMIZE=1 tools/vm-manager-system-check nes gb` exits 1, quoted, where the unfixed tool's PASS is recorded (P6)."),
 dict(f="G-36, G-32, G-33", t="`vm-serial sh` returns 0 whatever the command did, and the SSH and serial channels have no execution deadline", sev="Medium", cat="Bug", q="Q3", bug=True, tracked="#976",
  area="`tools/vm-serial`, `tools/vm-pair`, `tools/vm-qa`, `tools/emulator-exit-test`, `tools/ra-offline-test`, `tools/time-to-play`, `tools/vm-visual-qa`", what="`vm-serial sh` returns the command's status (an exit marker); `vm-pair`'s key install then fails when it fails; SSH calls get an execution bound (`timeout`) and the drains an absolute deadline.",
  where="`vm-serial:44-74`, `:101-105`, `:121-129`; `vm-pair:110`; `vm-qa:115`, `:123`; `vm-visual-qa:226-239`, `:272-280`", ev="the seat's G-32, G-33, G-36", vm=HOST, aw=AWN,
  acc="on a guest: `vm-serial sh false` exits non-zero, quoted beside the unfixed tool's 0; a constructed SSH command that never ends is cut at its bound."),
 dict(f="G-50, G-51, G-54, G-55, G-56, G-57", t="`ra-offline-test`: the account goes to `127.0.0.1` with the default key whatever `--host` says, cleanup has no trap and its failures do not count, and negative checks pass on a failed read", sev="Medium", cat="Bug", q="Q3", bug=True, tracked="#977",
  area="`tools/ra-offline-test`, `tools/qa-accounts`", what="Pass host and key to `qa-accounts`; an EXIT trap runs cleanup and counts its failures; a negative check needs a successful read; exact matches for `flushed=` and the achievement id; every requested capture checked.",
  where="`ra-offline-test:94-96`, `:203-205`, `:231-264`, `:269`, `:392`, `:459-498`, `:518-524`; `qa-accounts:52`, `:59-60`", ev="the seat's G-50 to G-57; read by the lane at `:90-118` and `:231-264`", vm=HOST + " (no QA account is needed for the refusals; the account path runs only with the coordinator's yes, brief § 8)", aw=AWN,
  acc="constructed: an SSH failure during a negative check fails it, quoted; `--host 127.0.0.2` reaches `qa-accounts` with that host, quoted; each beside the unfixed tool."),
 dict(f="G-59, G-60, G-61", t="`device-act` records less than it promises: a failed log write does not stop the act or its 'recorded' line, and the whole command, a credential included, goes into the log", sev="Medium", cat="Bug", q="Q3", bug=True, tracked="#978",
  area="`tools/device-act`", what="Refuse to act when BEGIN cannot be written; END's failure fails the run; the logged command through the credential mask the rules give; the timeout's wording says what it supervises.",
  where="`device-act:35-44`", ev="read by the lane at `:28-44`; the seat's G-59 to G-61", vm="Yes, without a device: a fixture `ssh` on PATH and an unwritable log (D-QA-015: never against a device here)", aw=AWN,
  acc="with a fixture `ssh` and an unwritable `DEVICE_ACTIONS_LOG`, the fixed tool exits non-zero before the command runs, quoted; the unfixed one runs it and prints 'recorded', quoted."),
 dict(f="G-66, G-30 (the rehearsal's stop)", t="`vm-upgrade-rehearsal` passes 'backup archive kept' at zero archives before and after, and checks the seeded files' hashes exist rather than their sizes", sev="Medium", cat="Bug", q="Q3", bug=True, tracked="#979",
  area="`tools/vm-upgrade-rehearsal`", what="Require a positive archive count before the update and the same after; compare the seeded files' sizes and hashes with what was seeded; a failed stop fails the result.",
  where="`vm-upgrade-rehearsal:65-75`, `:95-97`, `:154`, `:167-170`", ev="the seat's G-66", vm=HOST, aw=AWN,
  acc="a constructed rehearsal whose backup creation fails: RESULT FAIL, quoted, beside the unfixed RESULT PASS."),
 dict(f="F-18, G-19, G-20, G-21, G-22, G-25", t="`frame-diff`'s coverage has holes: an empty baseline passes, the transfer masks cover whole walks, 'PROPOSAL ONLY' claims are live, `--min-pixels` contradicts its sentence, a scoped walk is compared with the whole baseline, and three whole-frame claims sit on a month-old baseline", sev="Low", cat="Bug", q="Q3", bug=True, tracked="#980",
  area="`tools/frame-diff`, `tools/vm-walks/masks.txt`, `claims.txt`", what="A baseline with no frames is refused; masks name screens, not walks; a proposal claim is inert until marked; the sentence matches `--min-pixels`; the compare scope follows the walks run. Moving the baseline and pruning claims is the maintainer's (`frame-diff accept`), named here.",
  where="`frame-diff:244-261`, `:286-353`, `:395-410`; `masks.txt:7-9`; `claims.txt:38-40`, `:77-89`", ev="P5; the seat's G-19 to G-25", vm=HOSTONLY + " (recorded frames)", aw=AWN,
  acc="constructed: an empty baseline with `BASELINE.txt` exits 1, quoted; a change on `run-transfer/01-cloud-hub.png` inside the transfer mask is reported, quoted; each beside the unfixed tool."),
 dict(f="F-07, G-03, G-04, G-07 (narrowed)", t="Suites that check a neighbour of their subject: `register` without the ES checkout, `fresh` on port 10022 whatever the guest, the interface checks on an `ES_SRC` not bound to the image's pin", sev="Low", cat="Bug", q="Q3", bug=True, tracked="#981",
  area="`tools/vm-qa`", what="`fresh` uses the selected guest's port; the ES-source suites compare `ES_SRC`'s HEAD with the image's pin and say so in the report; `register` says in its row that it ran without the interface's citations.",
  where="`vm-qa:105-110`, `:163-191`, `:205-215`, `:278-291`", ev="the seat's G-03, G-04", vm=HOST, aw=AWN,
  acc="`--guest b --only fresh` reads port 10023, quoted; an `ES_SRC` at a commit other than the pin makes the ES suites' rows say so, quoted."),
 dict(f="F-12, G-06, G-71", t="The report says less than it seems to: `--help` stops before four suites, a report-write failure is not a FAIL, and the minutes leave out bring-up", sev="Low", cat="Code Quality", q="Q7", bug=True, tracked="#982",
  area="`tools/vm-qa`", what="Print the whole header; count a report that cannot be written as a failure; record bring-up and fixture time in the report.",
  where="`vm-qa:81`, `:118-145`, `:132`, `:139`, `:528-541`", ev="tree; the seat's G-06, G-71", vm=HOSTONLY, aw=AWN,
  acc="`vm-qa --help` names all 17 suites, quoted; an unwritable report directory exits non-zero, quoted."),
 dict(f="G-11, G-13 to G-16, G-35, G-39, G-47, G-58, G-62 to G-65, G-67, G-68", t="Smaller gaps in the measurement and helper tools", sev="Low", cat="Code Quality", q="Q3", bug=True, tracked="#983",
  area="`time-to-play`, `vm-visual-qa`, `vnc-grab.py`, `signin-memory`, `es-launch-memory`, `qa-accounts`, `png-blackout`, `es-untranslated`, `es-syntax-check`, `raofflineproxy-consent-test`, `ra-candidate-games`", what="One fix per row of `04` § Second opinion's table for these ids: each names its line.",
  where="`04` § Second opinion, the ids listed", ev="the seat's items, each verified (`seat-verify.md`)", vm=HOST, aw=AWN,
  acc="each id's constructed input, recorded failing on the unfixed tool and passing on the fixed one, in the stream that takes it."),
 dict(f="F-14, F-15, F-16", t="What nothing runs and what has caught nothing: five tools without a current caller, suites whose only recorded failures are their own, and a walk script for a retired migration", sev="Low", cat="Renovation", q="Q6",
  area="`ra-candidate-games`, `es-launch-memory`, `signin-memory`, `font-stems`, `raofflineproxy-installed-native-test`; the `exit`, `lifetime`, `pair-identity`, `time-to-play`, `ra-offline` and `wrapper` suites; `vm-walks/cloud-epic/migration-protocol.sh`",
  what="The coordinator decides each one's fate with the maintainer (D-QA-040): a caller (a rule's instruction, a suite, the CI), a retirement under `engineering-practices.md` § Before deleting a duplicate, or a recorded reason to keep it. Cost against value is the lens, not a licence to delete (brief § 2).",
  where="`04` § Q6", ev="the value table; P10", vm=HOSTONLY, aw="nothing on devices or in clouds; a retired tool leaves its records under `docs/` as history",
  acc="each row dispositioned by the coordinator: a caller, a retirement with the duplicate check, or a recorded reason."),
 dict(f="F-17, F-19", t="The harness's cost concentrates: `walks` and `scripts` are about 30 of a default run's 33 minutes, the pair is held throughout for one 1-second suite, and accepted baselines accumulate", sev="Low", cat="Renovation", q="Q5",
  area="`tools/vm-qa`, `tools/frame-diff`", what="A lead for the coordinator: whether guest b comes up only for `pair-identity` and goes down after, whether `scripts` runs beside the guest suites, and a retirement for old baselines (D-INFRA-022).",
  where="`vm-qa:119-122`, `:270`; `frame-diff:399-403`", ev="P4; the cost table; `du` on the host", vm=HOSTONLY, aw=AWN,
  acc="the coordinator's disposition: a stream brief or a recorded reason."),
 dict(f="F-11, F-20", t="Paths: `es-syntax-check`'s default build root is the retired `rocknix.worktrees` layout, and `vm-upgrade-rehearsal` ignores `ROCKNIX_ARTIFACTS`", sev="Low", cat="Code Quality", q="Q1", tracked="deferred: #640 for `es-syntax-check:53`",
  area="`tools/es-syntax-check`, `tools/vm-upgrade-rehearsal`", what="#640 moves the default root; the rehearsal reads `ROCKNIX_ARTIFACTS` as `vm-qa` does.",
  where="`es-syntax-check:53`; `vm-upgrade-rehearsal:30`", ev="tree; `ls` on the host", vm=HOSTONLY, aw=AWN,
  acc="`es-syntax-check:53` is #640's row; `ROCKNIX_ARTIFACTS=/x tools/vm-upgrade-rehearsal ...` writes under `/x`, read in a fixture."),
 dict(f="F-13, G-31, G-72, `04` § Q7", t="The rules and the index describe the harness out of date: six tools pointed at a rule that never names them, a raw `kill` in the boot recipe, 'four suites' in `vm-first.md`, and 'every suite' in `release-candidates.md`", sev="Low", cat="Documentation", q="Q7",
  area="`.claude/rules/instruction-files.md`, `generic-x64-vm-testing.md`, `vm-first.md`, `release-candidates.md` (all on `next`)", what="Leads for the coordinator: rule edits are not this lane's (brief § 8).",
  where="`instruction-files.md` (the index rows); `generic-x64-vm-testing.md:115`; `vm-first.md:59`; `release-candidates.md` step 3", ev="`q7-descriptions.txt`; the seat's G-31, G-72", vm=HOSTONLY, aw="nothing inherited",
  acc="the coordinator's disposition of each rule row."),
 dict(f="G-07, G-23, G-24, G-26, G-28, G-38, G-45, G-46, G-48, G-52, G-69", t="The seat's narrowed items: leads, each a design the code documents or an input no caller makes", sev="Low", cat="Renovation", q="Q2",
  area="`vm-qa`, `vm-stop`, `vm-visual-qa`, `frame-diff`, `ra-offline-test`, `es-launch-memory`, `font-stems`", what="The coordinator dispositions each as a contract row, a stream or an acceptance; the reasons for narrowing are in `04` § Second opinion.",
  where="`04` § Second opinion", ev="the seat's items, verified, narrowed", vm=HOSTONLY, aw=AWN,
  acc="each lead dispositioned by the coordinator."),
]

# Phase 7, at stage F (2026-10-24): each item's outcome and its evidence. A
# fix closes when it is on next (the bug issue, not this table); the commits
# are on feature/m6-tooling-vm-harness-659, and 02 § The streams' positives
# holds each case at facb2ae523 and at the fix.
P7 = {
  "PL-01": ("Resolved", "`0ecbbb9339` (#966): a SKIP exits 3, an unknown or empty selection 2; S1's cases in 02"),
  "PL-02": ("Resolved", "`7c5d15b2d8`, `a09bfc5718`, `327e743189` (#967, #983); the cycles proved them on guest a. The g2g row fails on this image until the product stamps it: **product #1012**"),
  "PL-03": ("Resolved", "`00b8760457` (#968); `--only A` on guest b, `cycle-e/s7-exit-only-a-b.txt`"),
  "PL-04": ("Resolved", "`9df1c65c68`, `15b8f11334` (#969); cycle 1's report: BUILD_ID matches, `tear-down: vm-pair down rc 0`"),
  "PL-05": ("Resolved", "`33b1bb8845`, `eddd21d7a2` (#970); vm-pair-test and vm-stop-test rc 0"),
  "PL-06": ("Resolved", "`3f5998bbaf`, `373a366e40` (#971); cycle 1 ran with no override, its paths under the worktree and /run/user/1000. The scratch moved to a short `qa.XXXXXX` in the runtime directory, removed at exit, after the scripts suite's seven socket-length FAILs (`3eba8ce4b0`); its other 319 FAILs are location-independent, Bug #1015"),
  "PL-07": ("Resolved", "`ff10d77c28` (#972); walks 16/16 frames equal to their steps, `cycle-e/walks-vs-steps.txt`"),
  "PL-08": ("Resolved", "`a68bfadcd5` (#973); cycle 1's walks passed the new reboot wait"),
  "PL-09": ("Resolved", "`5edb265e59` (#974); cycle 1's walks seeded the QA remote and passed the endpoint check"),
  "PL-10": ("Resolved", "`6ca9da4831`, `6871f964c8`, `b6413b19e8`, `4757b48385`, `29bf33cbb8`, `639b45a8a6`, `5988d06c9a` (#975); for vm-stop-test no positive was found, recorded"),
  "PL-11": ("Resolved", "`2e790e7e52`, `1d5dc8a698` (#976); `vm-serial sh false` 1 on guest b, `cycle-e/s8-serial-b-fixed.txt`"),
  "PL-12": ("Resolved", "`33efb4d801`, `9a1300f141` (#977); the account path never ran"),
  "PL-13": ("Resolved", "`c1569b7bc6` (#978); the device-action log's redaction is the coordinator's at the merge"),
  "PL-14": ("Resolved", "`82b5edf1ee`, `f1331aba83` (#979)"),
  "PL-15": ("Resolved", "`36138c8da5`, `476ab6e69b` (#980); the fixed compare over cycle 1's walks shows 65 unclaimed boxes, and the baseline move is the maintainer's on #346"),
  "PL-16": ("Resolved", "`813e4dd270`, `ca0bf841d2` (#981); the ES pin was unreadable on this image (02); the lead is Backlog #1013 under #800"),
  "PL-17": ("Resolved", "`3c0b9d53c6`, `fc8754b29b` (#982)"),
  "PL-18": ("Resolved", "#983: `a09bfc5718`, `05117efe58`, `9a1300f141`, `930ea05d70`, `3edb5f2b89`, `8e29c6e2cc`, `181b67293a`, `a4ae0aee6c`, `d4ccc8b14b`, `f676d8bb5f`, `95241c0158`"),
  "PL-19": ("Deferred", "the coordinator's dispositions, held in Backlog #986: all kept with their callers named (PL-22's packet), except the `ra-candidate-games` retirement put to the maintainer on #346"),
  "PL-20": ("Deferred", "Backlog #987: guest b on demand, the host suites beside the guest suites, the baselines' retention"),
  "PL-21": ("Deferred", "`es-syntax-check`'s default root is #640's; the `ROCKNIX_ARTIFACTS` half is resolved by `f1331aba83` (S5)"),
  "PL-22": ("Deferred", "Backlog #988, the doctrine packet after T4's merge; S1's three list entries landed in `ea2377f1ce`"),
  "PL-23": ("Resolved", "G-24 `36138c8da5`; G-26 recorded as a design and G-28 fixed, both `eddd21d7a2`; G-45 and G-52 `33efb4d801`; G-69 `181b67293a`; G-46 kept as a design, its reason written beside each kill in `6e2d204987`; G-07, G-23, G-38 and G-48 kept as designs (the brief's reasons; G-07 a lead for #50)"),
}

def main():
  out = ["# Punch List — M6.P2 T12, the VM harness", "",
         "**Independent depth** (D-WORKFLOW-184): one GPT-6 Astra seat, graded in `04` § Second opinion. Every `where` is at `8ebaf8daad`. The bugs are #966 to #983 (one per defect item); the audit issue is #984, a sub-issue of #659. Generated by `tools/punch-items.py` from one list, so the items, the `punch_index` and the Phase 7 table agree.", "", "---", ""]
  idx = ["```yaml", "punch_index:"]
  gate = ["## Phase 7 resolution gate", "", "| Item | Outcome | Evidence |", "| --- | --- | --- |"]
  for n, x in enumerate(I, 1):
      pl = f"PL-{n:02d}"
      out += [f"## {pl}: {x['t']}", "", f"- **Severity:** {x['sev']}", f"- **Category:** {x['cat']}", f"- **Question:** {x['q']}", f"- **Source:** {x['f']}", f"- **Owner area:** {x['area']}", f"- **What:** {x['what']}", f"- **Where:** {x['where']}", f"- **Evidence:** {x['ev']}", f"- **Can this be done on the VM?** {x['vm']}", f"- **Already written:** {x['aw']}", f"- **Acceptance:** {x['acc']}"]
      if x.get("bug") or x.get("tracked"): out.append(f"- **Bug issue:** {x.get('tracked', 'filed at stage D')}")
      out.append("")
      idx += [f"- id: {pl}", f"  severity: {x['sev']}", f"  category: {x['cat']}", f"  question: {x['q']}", f"  source_finding: \"{x['f']}\"", f"  owner_area: \"{x['area'].replace(chr(34), chr(39))}\""]
      if x.get("bug") or x.get("tracked"): idx.append(f"  tracked: \"{x.get('tracked', 'bug issue filed at stage D')}\"")
      p7 = P7.get(pl)
      if p7:
          idx.append(f"  outcome: \"{p7[0].lower()}\"")
          gate.append(f"| {pl} | **{p7[0]}** | {p7[1]} |")
      else:
          idx.append("  outcome: open")
          gate.append(f"| {pl} | Open | stage D files the issue; a stage-E stream brief or the coordinator's disposition resolves |")
  idx.append("```")
  print("\n".join(out + ["## Machine-readable index", ""] + idx + [""] + gate))

if __name__ == "__main__":
    main()
