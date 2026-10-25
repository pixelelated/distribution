# Retrospective: M6.P2 T13, the cloud test harness (#660)

Phase 3: what the harness was for, what drifted, what none of it noticed,
what the record says it caught, and the seams. Every claim cites
`02-forward-audit.md` or a file:line at `8ebaf8daad`.

## 3.1 What the harness was for

The harness exists to prove the cloud tiers from both ends after
blindspot 31. That was the day MinIO's `rclone cat` of a missing key exited 0
and a check that a file *reached the cloud* passed for a file that was never
there. The answer was `cloud-test-backend cat`'s existence check (lines
650-653) and `epath()` (line 1803), so the harness reads the endpoint itself
rather than asking the device. Its five local endpoints (D-QA-058) were built
so that no proof needs a person's cloud, and stage A found them doing that:
each refused `cat` of a missing object with rc 1 and left nothing running.

## 3.2 What drifted

- **The single file grew past one reader's reach.** `cloud-round-trip` went
  from 4,953 lines to 6,989 on 2026-09-10 alone and is 7,808 now, 77% of the
  slice (01 § History). Six registries and the single-device suite share one
  file, one `check()` and one `Fail`.
- **Its four descriptions came apart.** `vm-qa:36` says 27 steps; the file
  has 32 steps in `run_steps` and 460 `check()` calls; the ledger says 106
  PASS; the work log says 108 (02 § The runs). No PASS line says which count
  it certifies.
- **Two scripts it names are not in the tree.** `cloud_reconcile` was never
  added, so A5 and RETENTION cannot pass. `cloud_migrate_layout` was deleted
  by `e6645cb5ea`, so `cloud-pair-migration` refuses with rc 2.
- **The rule drifted from the tool.** `rclone-cloud-sync.md:375` says the
  no-network step checks *"the exit-4 timing"*; the tool asserts exit 69 at
  line 1469 (#909, open, its checkboxes ticked while this tree's rule still
  carries the sentence).

## 3.3 What none of them noticed

- **`caps()` marks nothing in the single-device suite.** It is read at three
  call sites: A14's helper twice, KILL1 once (02 § Assertion shapes). The
  promise *"nothing is skipped in silence"* holds there because nothing is
  marked or skipped at all. Every backend runs the same 34 steps, and the
  backend's capabilities never change what a step asserts.
- **Eight rows judge by the device's own report** (ten before the seat's reclassifications), three of them round trips
  through the device's own restore, and four more read the remote through
  the device's rclone. Each certifies the code under test by that code's
  own output.
- **`cloud-test-backend` accepts `--backend` after the subcommand in
  silence** and answers for WebDAV, rc 0 (02 § The runs). The brief's own
  stage-A commands were written in that order, and so would any reader's be.
- **RETENTION's last two checks pass when nothing ran** (lines 2451, 2453):
  a cell that cannot run reports two PASS lines under its FAIL.

## 3.4 What the record says about catches

The harness found product defects: 19 `bug` issues name `cloud-round-trip`
as their proof (#53, #141-#143, #315, ...), and #366's eleven failures on a
`/GAMES` default were the harness catching its own fixture. The two
self-contained tests with documented positives were each seen to fire
again here: the stamp test over `f451252587`, and the integrity test with
its hash comparison defeated. Nothing in the record shows a red A5 or
RETENTION. Neither has a ledger row (02 § Assertion shapes, 8 rows with
none), so the cells that cannot pass were never reported as failing either.

## 3.5 The seams

| Seam | What crosses it | What this slice found there |
| --- | --- | --- |
| the harness x `vm-qa`'s suites | `vm-qa` runs `round-trip` and `link` (lines 295, 349) and describes the first as *27 steps* (line 36) | the count is wrong; `vm-qa` never runs `cloud-test-backend down` after a suite, so a backend outlives every run; its guest disks and sockets default to `/tmp` (lines 98-99) |
| the harness x the QA backends | `backend(...)` calls with `CLOUD_QA_BACKEND` exported (line 533) | the tool is called by environment, so the argument-order trap does not bite the harness; it bites a person at a prompt. `down` kills any listener on its port (lines 565-591), so two lanes on the default ports can stop each other's endpoint |
| the harness x the guests | SSH on 10022 (guest a, fixed), the serial and monitor sockets for LINK and KILL (defaults under `/tmp`, `cloud-round-trip` lines 503, 512) | the runtime directory and disks are parameters (`VM_QEMU_RUNTIME_DIR`, `VM_PAIR_DIR`), the SSH port is not |
| the harness x T15's shims | `last-good-scripts-test` names `cloud_migrate_layout` 55 times | the script is gone; T15's suite carries the name guarded by existence (a lead handed back, T15's) |
| the harness x the rule under #909 | `rclone-cloud-sync.md`'s `paths:` names four of the nine (`cloud-round-trip`, `cloud-test-backend`, `cloud-census`, `cloud-capture-stamp-test`) | opening the other five loads no rule; the no-network sentence is stale |
| the harness x `vm-visual-qa` under #972 | `cloud-round-trip` loads `tools/vm-visual-qa` as a module (`visual_qa()`, lines 6281-6292): for the `Monitor` class's VNC frame grab (line 6233), which the monitor-driven KILL cells use, and for KILL13's walks (`run_walk`, lines 7450 and 7494) | an open bug in that tool is a risk to those KILL cells, not to the single-device suite, which never loads it |
