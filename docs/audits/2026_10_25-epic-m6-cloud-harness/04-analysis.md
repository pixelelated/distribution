# Analysis: M6.P2 T13, the cloud test harness (#660)

Phase 4 over the nine tools at `8ebaf8daad`'s bytes. Evidence is
`02-forward-audit.md` (§ Coverage, § Assertion shapes, § The runs,
§ Positives, § Proofs) and `03-retrospective.md`. Written at stage B; the
seat's grades (§ Second opinion) and the guest cycle's lines land at stages
C and F.

## Executive summary

The harness reads both ends where blindspot 31 said it must: 24 of the 78
rows read the endpoint from the host (24, after the seat's reclassifications), and the endpoint's own `cat` refuses a
missing object on all three backends run (rc 1). Every tool that can fail on
the host was seen to fail on a constructed input. But five things a PASS
from it does not say:

1. **Which count it certifies.** The tool ends on a bare `PASSED`; its four
   descriptions say 27, 32/460, 106 and 108.
2. **That the backend changed anything.** `caps()` is read at three call
   sites, none in the single-device suite, so every backend runs the same
   34 steps.
3. **That an absence it asserts was looked for.** The endpoint's `ls` returns an empty listing with rc 0 when the path is not there, and two rows judge absence on that listing alone (F-12).
4. **That two of its cells can run at all.** A5 and RETENTION call
   `cloud_reconcile`, which was never added. They have no recorded verdict,
   and RETENTION prints two vacuous PASS lines under its FAIL.
5. **That its endpoint is the one named.** `cloud-test-backend` accepts
   `--backend` after the subcommand in silence and answers for WebDAV, rc 0.

Eight rows judge by the device's own report, three of them as round trips
through its own restore. The seat's refutation then found defects of a
different order (§ Second opinion): one cell that cannot complete (KILL1),
checks that pass on the inputs meant to fail them, and a step whose refusal
deletes the library it refused to touch.

## Acceptance-criteria scorecard

| # | Criterion (#660) | State at stage B | Artifact |
| ---: | --- | --- | --- |
| 1 | the folder holds 00 to 05 | partial: 00-04 written, 05 at stage C/D | the folder |
| 2 | lint PASS (pre-issue before D, resolution at close) | open: `review-plan.json` and 05 owed (stage C) | `tools/lint-audit-artifacts ... --phase pre-issue` |
| 3 | `review-plan.json`, provenance, the packet's scan | open: stage C | `second-opinions/` |
| 4 | the punch-list issue at Phase 7 | open: stage D-G | -- |
| 5 | `reviewed-at`/`fixed-at`; no `tools/` file outside the nine changed | the read is on `8ebaf8daad` (diff empty); no file under `tools/` changed | 01 § Scope; `git status` |
| 6 | 01 § Scope with § 2's block and the history | done | 01 § Scope |
| 7 | 02 § Coverage, 9 rows | done: the awk prints 9 | 02 § Coverage |
| 8 | 02 § Assertion shapes | done: 79 rows (34 + 44 + `CONTRACT`), generator rc 0, no delta; the device-report class listed (8, after the seat) | 02 § Assertion shapes |
| 9 | 02 § The runs | done for stage A; nothing left running | 02 § The runs |
| 10 | 02 § The guest cycle | waiting for the window on #660 | -- |
| 11 | 02 § Positives, one row per tool | done: 7 fire, 2 `none` with why | 02 § Positives |
| 12 | 00 shows none of the forbidden runs | holds so far | 00 |
| 13 | 04 § Q2, Q6, Q4, Q3 | Q2, Q4, Q6 written; Q3's `bug` issues are filed at stage D | below |
| 14 | `proved:` cells, `question:`, `box-check` | `proved:` in every 02 table; `question:` at stage D | 02 |
| 15 | the retro | stage G | -- |
| 16 | the five checkers on the branch | at hand-back | -- |

## Risk assessment

| Risk | Likelihood | Impact | Where |
| --- | --- | --- | --- |
| A green suite read as "the cloud tiers work on every backend" when no step is marked by backend | high (that is how the ledger reads it: *106 PASS each over WebDAV, SFTP and MinIO-S3*) | a backend-specific defect passes; blindspot 31's family | F-04 |
| A5 and RETENTION never run, so the discarded-saves store and the retention ordering have no proof at all | certain until the reconciler exists | T16 inherits two cells that cannot speak | F-01, F-02 |
| A backend run against the wrong endpoint because `--backend` followed the subcommand | medium (the brief itself wrote it that way) | a proof labelled SFTP that ran on WebDAV | F-03 |
| Two lanes' backends on the default ports, one `down` stopping the other's | medium on a shared host | a red run blamed on the code | F-07 |
| Host-only tests trusted for the image | low (each names its host oracle) | a busybox or rclone 1.75.2 difference passes the host | F-09 |

## Coverage boundary

Read: the nine tools whole for their oracles and positives; `cloud-round-trip`
by AST (every `step()`, every registry cell, every `caps()` call site, every
`check()`) and by hand for the eight overridden rows and the cells that
delegate (`Link.exercise`, `Pair.cloud_sha`, the `Transport` class).
Run: the four bare tests, the documented positive, the retired tool, three
backends (WebDAV, SFTP, S3) up/ls/cat/down, `--list`, and six constructed
positives. **Not run:** SMB and FTP (no stage-A run asked for them; their
images and venv are read for Q4 only), the single-device suite and CAP1-14
on a guest (the window), the PAIR, SOLO, LINK and KILL registries (two
guests, a throttled endpoint or a serial console; outside this slice's one
cycle), `cloud-census` (never: D-QA-015). Not read as code: the cloud scripts
the harness drives (T16's, T17's).

## Findings (Phase 4)

| ID | Finding | Q | Evidence (02 / 03) | proved: |
| --- | --- | --- | --- | --- |
| F-01 | A5 and RETENTION call `cloud_reconcile` (`APPLY`, line 1771), which has never existed; both fail by construction and neither has a recorded verdict | Q3 | § Proofs; § Assertion shapes | history |
| F-02 | RETENTION's last two checks (lines 2451, 2453) PASS when nothing ran: an assertion that holds only because nothing happened (blindspot 8) | Q3 | § Proofs | tree |
| F-03 | `cloud-test-backend` ignores `--backend` after the subcommand and answers for WebDAV, rc 0 (lines 57-63) | Q3 | § The runs; § Proofs | tool-run |
| F-04 | `caps()` marks no step of the single-device suite; it is read only by A14's helper and KILL1 | Q2 | § Assertion shapes | tree |
| F-05 | the tool's last line is a bare `PASSED` (line 619); its four descriptions give four counts | Q7 | § The runs | tree |
| F-06 | `cloud-pair-migration` cannot run on any tree after `e6645cb5ea`; it is retired by code | Q6 | § The runs | tool-run |
| F-07 | `vm-qa` never downs the backend after a suite; guest disks and sockets default to `/tmp`; `down` kills every listener on its port | Q1 | 03 § 3.5 | tree |
| F-08 | the rule's no-network sentence is stale (`rclone-cloud-sync.md:375`, #909) and its `paths:` names four of the nine | Q7 | 01 § The rule | tree |
| F-09 | two tools judge with the host's rclone (1.60.1-DEV, the image ships 1.75.2), two with the host's bash and coreutils | Q2 | § Coverage | tree |
| F-10 | `quay.io/minio/minio:latest`, `dperson/samba:latest` and `pyftpdlib` are unpinned | Q4 | § The runs | tool-run |
| F-12 | `cloud-test-backend ls` swallows every error (`|| true`, lines 629-633) and `backend_files()` ignores its exit (line 1838), so a listing that failed is an empty one; two rows judge absence on such a listing alone and PASS on it: `run_steps.27` ("an unselected system was not uploaded") and KILL4 ("uploaded no invalid archive") | Q3 | § Proofs | tool-run |
| F-13 | no tool among the nine proves a mixed installation under D-CLOUD-175's `/pixelelated` default (a device updated in place keeping its folder beside a fresh install, one cloud); D-CLOUD-158's gate was met on 2026-10-05 for the retired `/Rasteratops` default by `cloud-pair-migration`, now retired. **The coordinator ruled on #660 at 05:22 UTC: the proof is owed, as Backlog #1055 (the coordinator's)**; this slice defers the gap there | Q6 | 01 § The retired tool; `tools/archaeology mixed-installation` | history |
| F-14 | `tools/cloud-connections-test:37` holds a credential-shaped fixture literal at rest (a quoted value assigned to a password-named variable); T10's widened `SECRET_PATTERNS` (#935, `feature/m6-tooling-guards-657`) matches it, so once that lands the pre-commit refuses the next commit that touches the line, and the packet carried it redacted. `engineering-practices.md` § Guards must fail closed: a fixture a secret scanner would match is assembled at run time | Q2 | 02 § Proofs; `second-opinions/packet-manifest.json` `redactions` | tool-run |
| F-15 | KILL1 cannot complete: `webdav` is never assigned in `fx_kill1` and is read at line 6846 (the only assignments are locals at 5506 and 7091), so it raises a `NameError` the runners do not catch; and its preservation predicate counts a deleted cloud file as `absent`, never `TORN` (6815-6825), so deleting every copy passes "every file is v1 or whole v2" (G-30, G-35) | Q3 | 04 § Second opinion | tree |
| F-16 | CONTRACT's copy arm reports `dry-run: push ... conflicts [...] ...` on every dry run (4739), and the guard is `"conflict" in dry["out"].lower()` (4844), so "the dry-run guard fired" and "reported in a parseable form" PASS with an empty conflict list (G-31) | Q3 | 04 § Second opinion | tree |
| F-17 | verdict accounting: `prepare_device.1`'s equipment `check()` result is discarded (314), so a printed FAIL does not fail the run; the seat adds that an unknown or unsatisfiable `--only` ends PASSED and skipped KILL cells are not counted (G-32) | Q3 | 04 § Second opinion | tree |
| F-18 | step 25 PASSes on an empty probe: when `es_systems.cfg` is not found the `grep -oP` reads nothing and `orphans` is empty (1484-1494); it is also a text search of backuptool's source, so a comment can satisfy it (G-33) | Q3 | 04 § Second opinion | tree |
| F-19 | CAP13's warning check: `grep -c ... \|\| echo 0` yields `0\n0` on a log with no match, which is neither `""` nor `"0"`, so "the warning logged" PASSes with no warning (4452-4453); `Kill.count_in()` already avoids this trap (G-34) | Q3 | 04 § Second opinion | tree |
| F-20 | step 8's refusal deletes what it refused: an occupied `/storage/roms/vectrex` raises `Fail` (915-916), and `restore_device`'s `finally` then runs `rm -rf /storage/roms/vectrex` whenever `--real-roms` is off (7784-7785); against a device with a real Vectrex library, the run deletes it; LINK and KILL resets remove it without ownership too (G-44) | Q3 | 04 § Second opinion | tree |
| F-21 | the SFTP backend is not a jail: `internal-sftp -d ${DATA}` (396-397) sets a starting directory, no `ChrootDirectory` exists, and the client key placed on every guest authenticates as the host's own user (`SFTP_USER=$(id -un)`), reachable from a guest at 10.0.2.2; a guest process holding the key reaches whatever that host user can read (G-42) | Q2 | 04 § Second opinion | tree |
| F-22 | credential serialization fails open: the WebDAV/SMB/FTP stanzas fall back to the clear QA password if `rclone obscure` fails (742, 752, 762); the seat adds that the first S3 host-config write precedes its chmod and that `reset` can print "endpoint is empty" over ignored removal errors and surviving S3 objects (593-626) (G-40, G-43) | Q2 | 04 § Second opinion | tree |
| F-23 | A15 plants plain bytes named `.tar.gz` (`dev.write(..., b"this run's archive")`, ~2851), which the harness's own header (145-148) says `cloud_backup` lists and refuses since 2026-09-10; A15 fails before the behaviour it names (G-46) | Q3 | 04 § Second opinion | tree |
| F-24 | KILL5 plants three own archives and expects `own[1:] + [archive]` after retry (7094, 7151) whatever `CLOUD_BACKUP_KEEP` is, while its message claims the configured keep (G-47) | Q3 | 04 § Second opinion | tree |
| F-25 | `cloud-census` is not read-only: it runs `cloud_device_id` on the device (line 76), a helper that can heal and rewrite identity state, and sources the device's configuration (G-48) | Q6 | 04 § Second opinion | tree |
| F-26 | the seat's further leads, accepted on its citations and not re-read in this session: kill-point witnesses that write `landed` without a kill (G-36), timing windows treated as orderings (G-37), a vocabulary gate that accepts any permitted sentence and step 29 accepting any non-0/69 code (G-38; step 29's predicate re-read), the litter scan's limits (G-39), endpoint health by PID and port only (G-41), cleanup failures outside the verdict (G-45), the connections shutdown test's 50 ms timer (G-49), the explicit-empty-key Wi-Fi case needing no connect (G-50), the stamp test never asserting exit status (G-51), and the integrity verifier following symlinked ancestors (G-53) | Q3 | 04 § Second opinion | tree |
| F-11 | fixed waits stand in for an event at lines 4915, 6692, 7455 (1.5 s, found by the seat), 7496 and 7500; 6910 is a bounded negative-observation window and 5294 a poll interval inside a deadline loop (the first reader was wrong about both, G-26); the other 1-5 s sleeps are poll intervals or deliberate mtime separation | Q3 | below, Q3 | tree |

## Finding Verification (Phase 4.5)

Each finding re-read against its artifact at the hash, after it was written:

- **F-01:** `git log --all --oneline --diff-filter=A -- '*cloud_reconcile'` prints nothing. `grep -n '\bAPPLY\b'` shows lines 1771, 2388 and 2433, and line 1765's comment says *"the command fails today and the fixtures with it"*. **Verified.**
- **F-02:** with `APPLY` failing, `both_changed` left the cloud at HB and the device at HA, which is exactly what lines 2451 and 2453 assert. **Verified by reading**; a run needs two guests.
- **F-03:** re-run as `port`/`caps` in both orders: 9010 vs 9013, and WebDAV's caps vs S3's. **Verified.**
- **F-04:** `grep -n '\bcaps()'` shows `def` at 1792 and calls at 2369, 2372-2373 and 6786; the generator's `caps_keys` are empty for all 34 steps. **Verified.**
- **F-05:** line 619 prints `PASSED` or `N CHECK(S) FAILED` and nothing else on success. **Verified.**
- **F-06:** the stage-A run gave rc 2; lines 58-63. **Verified.**
- **F-07:** `vm-qa` has no `cloud-test-backend` call with `down`; lines 98-99 default to `/tmp`; `cloud-test-backend` lines 565-591. **Verified.**
- **F-08:** `rclone-cloud-sync.md:375` and lines 3-14 of its front matter. **Verified.**
- **F-09:** `cloud-connections-test` and `cloud-save-integrity-test --rclone /usr/bin/rclone` use `rclone v1.60.1-DEV`; `projects/ROCKNIX/packages/network/rclone/package.mk:7` gives `PKG_VERSION="1.75.2"`. `cloud-capture-stamp-test` and `cloud-input-test` run `bash` on `PATH` (shims first). **Verified.**
- **F-10:** `cloud-test-backend` lines 118, 134 and 212-214. **Verified.**
- **F-11:** each sleep read with its two preceding lines (Q3 below). **Verified as a lead, not a defect:** none was seen to fail.
- **F-14:** the three pattern sets sourced and run with `/usr/bin/grep -a -c -E` over the packet. Under this branch's and the primary checkout's sets: 0 lines. Under T10's widened set: 1 line, `tools/cloud-connections-test` line 37 at `8ebaf8daad`. **Verified;** the value is synthetic (`qa-only-...`), not a credential.
- **F-12:** `CLOUD_QA_STATE=/workspace/tmp/m6-t13/no-such-state tools/cloud-test-backend --backend webdav ls` (and `--backend sftp`) gives **rc 0, 0 bytes** for a data directory that does not exist. Step 27's check (`"game.rom" not in listing`, line 1567) on that listing is true. Its only companion check is the device's unit-marker protocol, so nothing in the step asserts that the selected system reached the endpoint. KILL4's (lines 7054-7056) is `not bad_up` over `backend_files(folder)`. Steps 2, 17 and 18 pair their absence check with a presence check from the same listing, so they cannot pass on an empty one. **Verified.**

## Second opinion (Phase 4.6)

**One seat, Independent depth, as planned** (`second-opinions/review-plan.json`).

- **The probe,** 05:25:06-05:25:15 UTC: served `openai/gpt-6-astra` by OpenAI at `max`. Verification, effort and provider all PASS.
- **The refutation,** 05:25:26-05:38:50 UTC, attempt 1 of 4, `finish=stop`:
  - 34,948 bytes of output, from 220,427 prompt and 36,583 completion tokens (28,431 reasoning), 803,757 ms, 0 retries;
  - served `openai/gpt-6-astra` by OpenAI, effort `max`; verification PASS (semantic, `provider_response`), effort PASS, provider PASS (`response_provider_field`);
  - `facilitator_version` `council-facilitator@1.14.1-pixelelated.2`.
- **The output was scanned before it was read:** `forbidden-terms-check --stdin` 0 hits, and `SECRET_PATTERNS` 0 lines under all three sets.
- **The packet:** `gpt-brief.md`, 746,882 bytes, sha256 `e4cda5bc...`, with one redaction (F-14).

**Grading: 53 items.**
- **Re-read in this session at their lines:** G-1, G-3, G-6, G-7, G-8, G-11, G-19, G-26, G-30 to G-35 (G-32's equipment half), G-38 (step 29), G-40, G-42, G-43, G-44, G-46, G-47, G-48 and G-52.
- **Accepted on the seat's citation and marked so:** the rest.
- **Result:** 9 confirmed, 18 narrowed and accepted, 1 refutation accepted (G-8), 25 new. **Of the new, 13 are verified defects** (F-15 to F-25); the rest are leads, collected as F-26.
- **The first reader's errors the seat found, all accepted:**
  - eight `(reviewed)` overrides claimed, six shown (G-1);
  - A3, `prepare_device.2` and step 30 misclassed (G-6, G-7), and KILL1 and step 32 misclassed the other way (G-8);
  - "the suite skips nothing" (G-19: KILL1 prints SKIP, and the suite has SKIP lines);
  - line 5294 called a fixed wait (G-26);
  - "19 rejection cases" (G-52: 17 rejection checks, one valid-packet check, one raw-semantics check).

| G | The seat | Graded | Decided by |
| --- | --- | --- | --- |
| G-1 | narrowed: six rows marked, not eight; the rule mixes setup and outcome reads | accepted | the rendered table at stage B: six `(reviewed)` |
| G-2 | confirmed steps 3/4/6; step 5's restore half and A2 have device-side verdicts | accepted | read at 766-774, 2034-2041 |
| G-3 | narrowed: 7, 9, 10, 13, A15 and A5 read via the device's rclone; A5's 0 is wrong | accepted; A5 counted by hand | 2393-2394 (a concatenated reader string) |
| G-4 | confirmed 15, 16, LINK4, KILL2, LINK1 | confirmed | -- |
| G-5 | narrowed: 12, 21, 26, A12, CAP4 certify sampled local facts; KILL3's title is stale | accepted (KILL3 on the citation) | -- |
| G-6 | A3 synthetic; `prepare_device.2` synthetic setup | accepted, reclassified | 2063 vs 2073-2078; 318-383 |
| G-7 | step 30 a planted readback | accepted, reclassified | 1675-1692 |
| G-8 | refuted: KILL1 and step 32 read both ends; KILL4 conditional | accepted, reclassified | 6811-6825; `litter_scan` 6129-6153 |
| G-9 | narrowed claims of 18, 19, 22, A11 | accepted | -- |
| G-10 | A5 and RETENTION cannot establish their outcomes; CONTRACT is not a caller | accepted | 1771, 2388, 2433 |
| G-11 | confirmed: RETENTION's 2451 and 2453 vacuous | confirmed | 2451, 2453 |
| G-12 | confirmed: `cloud-pair-migration` refuses on the checkout's file | confirmed | 58-63 |
| G-13 | step 24 proves a stubbed empty route, not a link loss; 69 is current | accepted | 1460-1478 |
| G-14, G-15 | retire the migration journey but port the mixed-installation skeleton | accepted, carried to #1055 (F-13) | -- |
| G-16 to G-18 | F-01 to F-03 narrowed or confirmed; `ls --backend s3` takes `--backend` as a path | accepted | -- |
| G-19 | F-04 narrowed: capability handling does skip (KILL1); one protocol per run is useful qualification | accepted; F-04 corrected | KILL1's SKIP at 6820-6825 |
| G-20 | F-05: the four figures are different units | accepted | -- |
| G-21 | F-06: a history claim, not a permanent guard | accepted | -- |
| G-22 | F-07: the port sweep is the non-container branch only; `vm-qa` not in the packet | accepted (`vm-qa` read by the first reader, 03 § 3.5) | 565-590 |
| G-23 | F-08: `paths:` not in the packet | accepted (read by the first reader, `rclone-cloud-sync.md` lines 3-14) | -- |
| G-24 | F-09: the versions are environment facts; the connections tests compare bytes and modes too | accepted | -- |
| G-25 | F-10 confirmed | confirmed | -- |
| G-26 | F-11: 5294 is a poll; 6910 a negative window; 7455 missed | accepted; F-11 corrected | 5288-5294, 6903-6913, 7453-7458 |
| G-27, G-28 | F-12 confirmed, with more instances: `backend_sizes()`, A9, CONTRACT item 2, KILL1, LINK2/3/5/6, step 32 | accepted; F-12 widened | 1836-1849 |
| G-29 | F-13 supported by the code | accepted | -- |
| G-30 | new: KILL1's `NameError` at 6846 | **confirmed, F-15** | 6840-6847; `grep -n 'webdav ='`: 5506, 7091 only |
| G-31 | new: CONTRACT's guard always fires | **confirmed, F-16** | 4739, 4844 |
| G-32 | new: verdict accounting | **confirmed in part, F-17** | 313-316 (the equipment half) |
| G-33 | new: step 25 vacuous | **confirmed, F-18** | 1484-1494 |
| G-34 | new: CAP13's double zero | **confirmed, F-19** | 4452-4453 |
| G-35 | new: KILL1's absent predicate | **confirmed, F-15** | 6815-6825 |
| G-36, G-37 | new: kill witnesses; timing windows | accepted as leads, F-26 | -- |
| G-38 | new: the vocabulary gate; step 29 accepts any non-0/69 | accepted; step 29 confirmed | 1665 |
| G-39 | new: the litter scan's limits | accepted as a lead, F-26 | -- |
| G-40 | new: `reset` certifies empty over errors | **confirmed, F-22** | 593-626 |
| G-41 | new: endpoint health by PID and port | accepted as a lead, F-26 | -- |
| G-42 | new: the SFTP key reaches the host user's files | **confirmed, F-21** | 396-397; `SFTP_USER` at 137-139 |
| G-43 | new: clear-password fallback | **confirmed, F-22** | 742, 752, 762 |
| G-44 | new: step 8's refusal deletes the refused library | **confirmed, F-20** | 912-918, 612-618, 7784-7785 |
| G-45 | new: cleanup outside the verdict | accepted as a lead, F-26 | -- |
| G-46 | new: A15's plain-text archive | **confirmed, F-23** | 2850-2852, 145-148 |
| G-47 | new: KILL5's keep of three | **confirmed, F-24** | 7094, 7151 |
| G-48 | new: census runs `cloud_device_id` | **confirmed, F-25** | `cloud-census:76` |
| G-49 to G-51 | new: three small tests' blind spots | accepted as leads, F-26 | -- |
| G-52 | narrowed: 17 rejection checks, not 19 | **confirmed; 02 corrected** | 16 `PASS ... rejected` lines plus the corrupt-PNG case in the stage-A output |
| G-53 | new: the verifier follows symlinked ancestors | accepted as a lead, F-26 | -- |

## Renovation face

### Q1 Modernize

One file holds the single-device suite and six registries: 7,808 lines,
77% of the slice, with one `check()`, one `Fail`, one `main()` and 46
`step()` calls. T14 found its tests good in the shape *one test, one
subject, one oracle*. Here, by contrast, a reader of a PASS line cannot
tell which of 79 rows produced it.

The registries are run by hand. CAP1-14 is about 10 minutes on one guest,
needs no cloud, and could be a `vm-qa` suite (T12's file: a lead). PAIR
needs two guests and A5 and RETENTION cannot pass, so it should not be
wired in until the reconciler exists. KILL needs the monitor and the serial
console, and LINK is already `vm-qa`'s `link` suite.

The seams are shared-host hazards (F-07). Each fix is small: `vm-qa` downs
what it brought up, and `down` stops its own pid, not every listener on its
port.

### Q2 Standards

**The oracle verdict, by `t13-shapes.py` and the lane's review (78 rows):**

| Oracle | Rows | Of which |
| --- | ---: | --- |
| both ends (the host reads the endpoint) | **24** | steps 2, 5, 8, 17, 18, 19, 22, 23, 27, 32; cells A1, A2, A8, A9, A11, A14, RETENTION, LINK2, LINK3, LINK5, LINK6, KILL1, KILL4 (conditional), KILL5 |
| a synthetic input (planted, then the device's reaction read) | **46** | the other steps that plant (1, 7, 9-11, 13-16, 20, 24, 26, 28, 29, 31) and the cells A12, A15, CAP1-14, LINK1, LINK4, LINK7, KILL1-3, KILL10-13, KILL15, KILL16, KILL18 |
| the device's own report | **8** | `run_steps.3`, `.4` and `.6` (round trips), `.12`, `.21`, `.25`, `prepare_device.1`, A5 (after the seat: A3, `prepare_device.2` and step 30 moved to synthetic, KILL1 and step 32 to both ends) |

`CONTRACT`, outside the 78, reads both ends.

**`caps()` marks, and in KILL1 it skips (the seat's G-19 corrects the first cut, which said it never skips). But it marks almost nothing.** The two
rows that read it mark by changing the expectation, not by skipping: A14
expects a null `remote_hash` on a hashless backend, and KILL1 accepts an
in-place commit where the endpoint is not atomic. No step of the
single-device suite reads it (F-04), so a WebDAV PASS and an S3 PASS are
the same 34 assertions, and nothing in the output says which capabilities
the run exercised.

**The host-rclone rows:**
- `cloud-connections-test` runs `cloud_connections` against the host's rclone 1.60.1-DEV. That is the module's choice, and its header says so.
- `cloud-save-integrity-test --rclone` uses the host's rclone as an independent oracle by design, the only second implementation among the nine.

Neither proves anything about the image's rclone 1.75.2.

**The host-bash rows:**
- `cloud-capture-stamp-test` runs `finish()` under the host's bash, with only `date` faked. CAP12 is its guest twin, under the image's busybox.
- `cloud-input-test` runs `wifictl` under host bash and coreutils inside `bwrap`.

Under D-QA-063 (T14's rule), each should say whose tools judged. Neither
does in its output.

### Q3 Bugs

- **F-01, `cloud_reconcile`:** A5 and RETENTION cannot pass, and no recorded run shows them failing. The fix is either the device script, if #22/#23 ever add it (T16's area), or a fixture that says it waits and reports `SKIP - waits for the reconciler` instead of running a command it knows does not exist. A `bug` at stage D, with the constructed case `--only A5,RETENTION --second-port`, which needs two guests.
- **F-02, RETENTION's vacuous PASS lines:** with `seen` false, the head and device-copy checks should not run. A `bug` at stage D, folded with F-01 unless the coordinator splits them.
- **F-03, `--backend` after the subcommand:** a stray argument accepted in silence. A `bug` at stage D; the constructed case is `tools/cloud-test-backend port --backend sftp` printing 9010.
- **F-05, a count that never prints:** the tool's PASS line should say how many checks it certifies, per backend. A `bug` at stage D, or a design row if the coordinator prefers.
- **The no-network step** asserts exit 69 (line 1469). The tool is right and the rule is wrong (#909's item 4; the fix is T4's `fcc7046f0e`).
- **Probes that cannot report absence (blindspot 22):**
  - `cat`'s existence check holds on all three backends (rc 1 on a missing object).
  - **`ls` does not**: both branches end in `|| true` (lines 629-633), so `backend("ls")` returns an empty string with rc 0 for a path, or a whole data directory, that is not there. `backend()`'s `check=True` (line 268) never sees a failure, and `backend_files()` (line 1838) does not even ask.
  - An absence judged on such a listing PASSes (F-12): `run_steps.27` and KILL4. Steps 2, 17 and 18 survive it because each pairs its absence check with a presence check from the same listing.
  - A `bug` at stage D. The constructed case is the `ls` above, rc 0 and empty; the fix is the stage-E `ls` failing on a missing path, and each absence check paired with a presence one.
- **F-11, the sleeps (blindspot 32):** 38 `time.sleep` calls.
  - 11 of the 1-5 s waits are poll intervals inside bounded loops.
  - 3 are deliberate mtime separations, each commented.
  - 6 stand in for an event: 4915 (4 s after a background transfer starts), 5294 (5 s), 6692 (4 s after ES restarts), 6910 (5 s after `touch_offset`), 7496 (2 s after the close key, before the save is checked) and 7500.
  - The rest are sub-second polls or computed waits.

  The six are leads, not defects: none was seen to fail.

### Q4 Currency

| Dependency | Pin | Resolved on 2026-10-25 | Source |
| --- | --- | --- | --- |
| `quay.io/minio/minio:latest` (S3) | none | `sha256:14cea493d9a3...`, `RELEASE.2025-09-07T16-13-09Z`, created 2025-09-07 (local, not pulled) | `docker image inspect` |
| `dperson/samba:latest` (SMB) | none | `sha256:66088b78a198...`, created 2020-07-03 | `docker image inspect` |
| `pyftpdlib` (FTP) | none (`pip install -q pyftpdlib`, lines 212-214) | 2.2.0, installed 2026-09-12 into the default state's venv | `pyftpdlib-2.2.0.dist-info` |
| host `rclone` (two tests' oracle) | the host's package | `v1.60.1-DEV`, against the image's `1.75.2` | `rclone version`; `package.mk:7` |

D-QA-058's baseline is WebDAV, SFTP and MinIO-S3. MinIO is the one baseline
endpoint whose version moves under `:latest`, and on this host it has not
moved in thirteen months because nothing pulls it.

### Q5 Efficiency

The single-device suite's recorded wall time is 81 s a backend (the brief's
figure). Stage A's host runs cost 4.0 s in all. The full set of registries
would add two guests (PAIR), a throttled endpoint and a serial console
(LINK, KILL), and power cuts through the monitor (KILL12, KILL13). Its
guest-minutes are not measured here; the one granted cycle measures the
suite and CAP1-14.

### Q6 Dead ends: the dispositions

These are proposals for the coordinator.

| Item | Disposition proposed | Why |
| --- | --- | --- |
| `cloud-connections-test` | keep; a lead to wire it into `vm-qa` as a host suite (T12's file) | 1.9 s, no guest, a real positive (§ Positives); its host-rclone limit stated (Q2) |
| `cloud-input-test` | keep as a hand-run host test; a lead for the OS-scripts area (Wi-Fi under the cloud prefix) | its subject is `wifictl` and `cloud_oauth`'s input, not a cloud tier; 1.0 s |
| `cloud-capture-stamp-test` | keep; CAP12 is its guest twin | 0.1 s, documented positive seen firing |
| `cloud-save-integrity-test` | keep; a lead to wire it into `vm-qa` as a host suite | 0.1 s, the only second implementation |
| `cloud-save-integrity` | keep as a hand-run verifier | it is a tool, not a test; its input manifest waits for a scoped collector (#517, D-CLOUD-181) |
| `cloud-census` | keep as a hand-run read of a handheld, never run in a slice; a lead to move it out of the cloud prefix | it asserts nothing; its subject is a person's device (D-QA-015), so its reads go through the D-QA-021 filter |
| `cloud-pair-migration` | retire (delete at stage E) | it exits 2 on every tree after `e6645cb5ea`. **Already written:** it ran only on QA guests and the QA endpoint, so nothing on a device or in a person's cloud; its proofs stay in history (`vm-qa-log.md:32`, #354 runs 96-99; the 2026-10-05 entry *Mixed-installation qualification completes*). **The gate it guarded:** D-CLOUD-158's *"the mixed-installation test runs on `tools/vm-pair` before the default ships"*, met on 2026-10-05 for the `/Rasteratops` default, which D-CLOUD-175 retired with the migration on 2026-10-07. Nothing among the nine guards a mixed installation under the `/pixelelated` default (F-13). **Ruled by the coordinator on #660 at 05:22 UTC:** the proof is owed as Backlog #1055; `cloud-pair-migration` stays retired, its removal deferred to #1055 with the gap |
| `cloud_reconcile` (never added) | the fixtures say they wait (Q3, F-01) | D-CLOUD-051, open, asks what the apply step is called; the harness should not name a command before the decision |
| `cloud_migrate_layout` (deleted) | named 0 times by `cloud-round-trip` and 8 by the tool to retire; T15's 55 are T15's | goes with `cloud-pair-migration` |
| the vendored copy (`docs/qa-logs/2026-10-07-cloud-validator/roundtrip/tools/cloud-round-trip`) | keep as evidence, unchanged | it is the 2026-10-07 record's copy (7,795 lines, `b534d174...`), not the tool, and no caller runs it |

### Q7 Clarity

A reader cannot tell from the PASS line what was certified, by which
oracle, or against which backend: the line is `PASSED`. The three
descriptions disagree:
- `vm-qa:36` says *27 steps*.
- The rule's runbook says *exit-4 timing* for a step that asserts 69, and its `paths:` covers four of the nine.
- The tool's header promises *nothing is skipped in silence*, which the suite keeps by marking nothing.

The fix is one line of output: the count of checks, the backend, and the
marked rows. The two descriptions that live elsewhere are leads.

## Instruction File Recommendations

These are proposals for the coordinator; this lane edits no rule.

1. **`rclone-cloud-sync.md`:** line 375's *exit-4 timing* becomes exit 69, which is T4's `fcc7046f0e` under #909. Its `paths:` should add the other five cloud tools, or `tools/cloud-*`.
2. **`tools/vm-qa:36`'s comment:** *27 steps* becomes 32, or better, the count the tool prints (T12's file).
3. **A line under `generic-x64-vm-testing.md`'s QA-backend notes:** `--backend` goes before the subcommand, and two lanes on one host give each run its own `CLOUD_QA_STATE`, `CLOUD_QA_PORT` and `CLOUD_QA_NAME`.

## Quality self-check

- Every finding cites a file:line at `8ebaf8daad` or a run in 02, and was re-read after it was written (Phase 4.5).
- The oracle counts come from the generator and the renderer, which can be re-run, and are not typed: 24 + 46 + 8 = 78 after the seat.
- The recorded-verdict column cites ledger rows and never summarises them: an early cut read PASS or FAIL off a row's free text and was withdrawn.
- **Not done yet:** the guest cycle, the seat, the punch list and the `bug` issues. Each is named in the scorecard with its stage.
