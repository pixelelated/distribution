# Running log — M6.P2 T12, the VM harness (#659)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, the T5 session (`m6-t5-build-engine`).
- **Brief:** `docs/reviews/briefs/tooling-vm-harness.md`, version 2 (`74de5c1610`).
- **Dispatch:** the coordinator's comment on #659, 19:04 UTC.
- **Depth:** Independent: one GPT-6 Astra seat at `max`, through the Facilitator.
- **`reviewed-at`:** `facb2ae523`, the branch `HEAD` at stage A. Its 60 paths are byte-equal to `8ebaf8daad`.
- **The lens:** cost against value. Q5's cost table and Q6's value table are the slice's output.
- **Prose** goes in through a quoted heredoc or the Write tool; **times** come from `date -u`.

## [Stage A] 19:05 to 19:06 UTC — scope, host, no-guest controls

- **The first commands** (`.qa-scratch/t12/first-commands.txt`):
  - fetch rc 0; branch `feature/m6-tooling-vm-harness-659` at `facb2ae523`, stacked on P1 (`2174265e9c`); `inventory.json` present;
  - `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` gives 8 files, exactly the dispatch's eight paths;
  - `df -i /tmp`: 40 % used; `/workspace`: 20 %.
- **The host before anything ran:**
  - The host file's last line is the coordinator's 18:24 UTC ask to the M7 lane, about the local QA WebDAV backend's obscured `pass =` in four QA logs (#962). It is not this lane's, and it ends `Census: qemu 0, M6 compilers 0`.
  - The census at 19:05:09Z: `pgrep -c -x qemu-system-x86` gives 0.
- **Membership** (§ 2's block; `.qa-scratch/t12/membership.txt`):
  - `paths 60 lines 8790 {'fork-own': 60} {'n/a': 60} {'shell': 10, 'python': 20, 'markdown': 2, 'other': 22, 'text': 3, 'image': 3}`;
  - `the glob also selects, in other areas: 0 paths`;
  - `wc -l` over the 60 at the hash gives 8,813, the 23 newline bytes inside the three PNGs, as the brief says.
  - Equal to the brief.
- **The hash:**
  - the 60 exported from `8ebaf8daad` to `.qa-scratch/t12/at-hash/` (60 files);
  - `git diff --stat 8ebaf8daad HEAD -- <the 60>` is empty;
  - 484,627 bytes;
  - 0 of 60 on `upstream/next`;
  - 145 fork commits since `c445081a59`, 144 without merges.
- **The checkers:** `tools/rules-check --quiet` rc 0. `tools/register-check`: `674 IDs, each once; every citation in the live documents names a row`, rc 0.
- **The push:** `git push -u origin feature/m6-tooling-vm-harness-659` rc 0.
- **The VM question, before any proof:** *Can this be done on the VM?* Yes, for the harness's own behaviour (how `vm-qa` accounts a suite that cannot run, what `vm-stop` waits for, what a walk's frames are). That is one bounded GENERIC_X64 cycle (brief § 5), not yet run. Everything else is the host and the no-guest controls below. Nothing runs on a device.

### The no-guest controls (19:05:45 to 19:05:46 UTC; census 0 before and after; logs in `.qa-scratch/t12/controls/`)

| Command | Exit | Summary |
| --- | ---: | --- |
| `python3 -I tools/vm-pair-test` | 0 | `PASS 9 VM launch controls; fixtures are not a real boot claim` |
| `python3 -I tools/vm-upgrade-readiness-test` | 0 | `PASS 7 storage-readiness controls; actual guest query, synthetic states, no boot claim` |
| `python3 -I tools/vm-stop-test` | 0 | `PASS 7 vm-stop controls` |
| `python3 -I tools/vm-manager-system-check --help` | 1 | `FAIL manager system: not enough values to unpack (expected 2, got 1)`: the tool takes no `--help` (two arguments and stdin) and fails closed on anything else. A lead for stage B: its four checks are `assert` statements, stripped under `-O` or `PYTHONOPTIMIZE`. |
| `python3 -I tools/raofflineproxy-integration-test --help` | 0 | the usage; it needs an unpacked patched proxy source, read at stage B, not run |
| `tools/vm-qa --list` | 0 | 17 names: `scripts lifetime wrapper vocabulary register french quoting menumap pair-identity fresh round-trip exit time-to-play link ra-offline walks frame-diff` |
| `tools/time-to-play --help` | 0 | the usage, ending `Never for a handheld.` |
| `tools/frame-diff --help` | 0 | the usage |
| `tools/vm-visual-qa --help` | 0 | the usage (`--monitor MONITOR  QEMU monitor unix socket`) |
| `tools/vm-pair` (no arguments) | 2 | the usage; the default scratch is `/tmp/rocknix-vm-pair` (a host `/tmp` root: a stage-B Q1/Q2 lead) |
| `tools/es-syntax-check` (no arguments) | 2 | `es-syntax-check: name at least one .cpp`. **Not a pass** (`es-native-ui.md`). |

- **The find/stop grep** (§ 5's `pgrep|pkill|kill` over eight tools): 41 lines (`controls/kill-grep.txt`).
  - Every `pgrep`, `pkill` and `kill` is inside a guest-side call (`S`, `SER`, `SSH`, `g.sh`, `ssh(...)`, `guest(...)`), against RetroArch, EmulationStation, WebKit, rclone or `xprobe`.
  - None finds or stops a host QEMU, as the stranger's proof found.
  - `vm-pair`, `vm-stop` and `vm-qa` have no host-side kill; `vm-pair down`'s own stop path is read at stage B.
- **The `/tmp` grep** over the 60: 84 lines (`controls/tmp-grep.txt`). Most are guest-side (the guest's own `/tmp`). The host-side ones are leads for stage B:
  - `vm-pair:37`'s `DIR` default, `/tmp/rocknix-vm-pair`, where each `up` rebuilds a guest's disk from the image;
  - the default monitor and serial sockets and the QA key path (`ra-offline-test:65-66`, the usage lines of `time-to-play` and `emulator-exit-test`);
  - `ra-offline-test:259`'s `/tmp/ra-offline-acct.$$` and `:345`'s `.steps`;
  - `time-to-play:158`'s SSH control socket `/tmp/ttp-cm-<pid>`.

PROOF: 19:05 P1 tree: the 60 equal the brief at 8ebaf8daad (60 paths, 8,790 lines, 484,627 bytes, 145 fork commits, none upstream's) and the branch's diff over them is empty -- `.qa-scratch/t12/membership.txt`, `lines-at-hash.txt`
PROOF: 19:05 P2 tool-run: vm-pair-test 9, vm-upgrade-readiness-test 7 and vm-stop-test 7 PASS (rc 0); vm-qa --list prints 17; es-syntax-check rc 2 without a build root -- `.qa-scratch/t12/controls/`

## [Stage B] 19:07 onward — the reading, the record, and the one guest cycle

- **The reading:** the 60 are read from the export, the large tools whole (`vm-qa`, `vm-pair`, `vm-stop`, `frame-diff`, `emulator-exit-test`) and the rest by their exit and pass logic. The leads are in `03` and `04`.
- **Two read-only research agents read the record** (D-WORKFLOW-189's fan-out, with their leads re-derived here):
  - the cost side: 61 reports, 59 distinct;
  - the value side: catches, positives and callers.
  - **Re-derived by the lane:** the per-suite times and verdicts from the 61 reports (`/workspace/tmp/m6-t12/q5-rederived.txt`), and three catches against their sources (`fresh` PL-001, `quoting` blindspot 57, `menumap` #542).
  - **A deviation:** the value agent wrote, then deleted, a stray grep dump at `/tmp/claude-1000/q6-rules.txt` (its own report says so). That is a `/tmp` write by the lane's helper, against brief § 8, and the lane reports it here. No other write was made outside `/workspace/tmp/m6-t12/`.
- **The claims reconciliation** (`/workspace/tmp/m6-t12/walks-reconcile.txt`):
  - `suite.txt` holds **16** walks and `default-pre`, a delta against the brief's 17;
  - there are 22 step files, 8 of which no suite walk replays;
  - every claim matches a walk and every walk owns a claim;
  - all 391 claims are against `d72084ccad`, the host's baseline accepted 2026-09-26;
  - three are whole-frame claims (`claims.txt:38-40`, #455).
- **The times on the PROOF lines** are the cited artifacts' mtimes (`date -u -r`), corrected after the lines were first written with typed minutes.
- **A host-only probe:** `vm-manager-system-check` under `PYTHONOPTIMIZE=1` passes an empty system list (`.qa-scratch/t12/probes/manager-check-optimize.txt`).

PROOF: 19:05 P3 tree: every pgrep, pkill and kill in the eight guest-touching tools is guest-side; vm-pair, vm-stop and vm-qa have no host-side kill; vm-pair down stops by tools/vm-stop with pidfile and disk -- `.qa-scratch/t12/controls/kill-grep.txt`, `vm-pair:124-130`
PROOF: 19:23 P4 history: 61 vm-qa reports (59 distinct) give each suite's seconds and verdicts; walks 1000 s, scripts 779 s, round-trip 84.5 s, time-to-play 69 s, exit 28 s median; ra-offline in none -- `/workspace/tmp/m6-t12/q5-rederived.txt`
PROOF: 19:14 P5 tree: suite.txt's 16 walks against claims.txt's 391 lines and the 22 step files: no claim without a walk, no walk without a claim, 8 step files outside suite.txt, every key followed by wait-for-change -- `/workspace/tmp/m6-t12/walks-reconcile.txt`, `steps-profile.txt`
PROOF: 19:26 P6 tool-run: vm-manager-system-check with PYTHONOPTIMIZE=1 prints PASS (rc 0) for an empty system list and a wrong selection that the plain run refuses (rc 1) -- `.qa-scratch/t12/probes/manager-check-optimize.txt`

### The guest cycle (brief § 5), 19:23 to 19:30 UTC

- **The image:** `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`, copied from `/workspace/artifacts/m6-t1-20261023/` to `/workspace/tmp/m6-t12/cycle/`.
  - Its sha256, `6b4c3079bdee2f47bd1149aac07b11714c591b847f22157fcd6d85f39a7e08fb`, is checked against the `.img.gz.sha256` beside it: `OK`.
  - **A delta against the brief:** the `.identity.json` carries no sha256; it carries `build_commit 069fc270442134fe771258418adf4e666e0473fb`, `dirty no`.
- **Before:** census 0. The host file's line, quoted:

  `== M6 T12 lane (#659) -- 2026-10-24T19:23:39Z: census qemu 0; one GENERIC_X64 guest from pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz (sha256 6b4c3079bdee2f47bd1149aac07b11714c591b847f22157fcd6d85f39a7e08fb), pidfile /workspace/tmp/m6-t12/cycle/rocknix-qemu.pid, ssh :10022, vnc :9, 8 GiB/4 vCPU; QA cloud isolated (CLOUD_QA_STATE under /workspace/tmp/m6-t12, port 19010); runs vm-qa --skip-up --only fresh,round-trip,exit,time-to-play,frame-diff and three argument probes; stopped by tools/vm-stop; no link, no ra-offline, no handheld, no build.`
- **The disk:** gunzip, `qemu-img convert`, `resize 16G`, as `vm-pair up` does, under `/workspace/tmp/m6-t12/cycle/`. It took 8 s.
- **The launch:** `generic-x64-vm run --headless --daemonize --monitor … --serial … --pidfile /workspace/tmp/m6-t12/cycle/rocknix-qemu.pid --vnc 9 --ssh-port 10022 --mac 52:54:00:52:4E:58 vm-a.qcow2`, rc 0.
  - PID 1439420, whose command line owns the disk; census 1.
  - Serial up in 15 s. The key went in by `vm-serial`, as `vm-pair`'s `ready_one` does. SSH answered with `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"` after 27 s.
- **The guest's readings:**
  - `test -x /usr/bin/cloud_migrate_layout` rc 1 (absent);
  - guest memory used 718 of 7771 MB after boot;
  - QEMU's host VmRSS and VmHWM 2,662,384 kB (`cycle/guest-checks.txt`).
- **`vm-qa`:** `env VM_PAIR_DIR=… VM_QEMU_RUNTIME_DIR=… ROCKNIX_ARTIFACTS=… CLOUD_QA_STATE=… CLOUD_QA_PORT=19010 WALK_BASELINE=<empty dir> tools/vm-qa --skip-up --only fresh,round-trip,exit,time-to-play,frame-diff`, 19:25:39 to 19:28:45, **rc 0**.
  - **The report** (`cycle/vm-qa/report.md`): fresh PASS 1 s, round-trip PASS 84 s, exit PASS 27 s, time-to-play PASS 72 s, frame-diff SKIP 0 s.
  - **Its last line is `**PASSED with 1 suite(s) SKIPPED**`, with rc 0.**
  - **Time to play:** 0.74 s to the game's first frame, 1.59 s to the exit-sync stamp, 1.01 s game to game; the remote is reachable.
- **The argument probes:**
  - `time-to-play … --repeat 0 --only launch,exit,g2g --vm`: rc 0 in 30 s, with `cells {launch: 0, exit: 0, g2g: 0}`, `headline_missing []` and `over_budget []` (`cycle/ttp-repeat0/`).
  - `emulator-exit-test … --vm --only X`: rc 0 in 1 s, `PASSED` with no check run (`cycle/exit-onlyX.out`).
- **The stop:** `tools/vm-stop /workspace/tmp/m6-t12/cycle/rocknix-qemu.pid …/vm-a.qcow2`, rc 0 in 0.25 s (`down: owned QEMU exited (pid 1439420)`). The PID is gone and the pidfile removed.
  - The isolated backend's `down` rc 0, `status` `not running`.
  - Ports 19010, 10022 and 5909 are free; census 0.
- **After:** the host file's line, quoted:

  `== M6 T12 lane (#659) -- 2026-10-24T19:30:19Z: the cycle is done. tools/vm-stop rc 0 in 0.25 s (pid 1439420 gone, pidfile removed); the isolated QA cloud down; census qemu 0. The disk and the image copy under /workspace/tmp/m6-t12/cycle are retired next, after their record.`
- **Retired** at 19:30:49Z (D-INFRA-022; `cycle/RETIRED.txt`):
  - the disk, 2,315,583,488 bytes, sha256 `230153933c0d…`;
  - the image copy, 2,122,289,964 bytes;
  - the OVMF vars and the cycle's key.
  - The original image stays under `/workspace/artifacts/m6-t1-20261023/`.
  - The compact record is kept under the audit folder's `cycle/`, scanned before it was kept: credential-shaped lines 0, apart from one prose false positive; `forbidden-terms-check --stdin` 0 hits. No frame is needed by a claim, so none is kept.
- **The ledger:** a row in `docs/vm-qa-log.md` (2026-10-24).

PROOF: 19:28 P7 guest: vm-qa with frame-diff SKIPped (no baseline) exits 0 and prints PASSED with 1 suite(s) SKIPPED -- `cycle/vm-qa/report.md`, `cycle/t-vmqa.txt`
PROOF: 19:29 P8 guest: time-to-play --repeat 0 --only launch,exit,g2g exits 0 with every headline cell empty and headline_missing [] -- `cycle/ttp-repeat0/time-to-play.json`, `cycle/ttp-repeat0.out`
PROOF: 19:29 P9 guest: emulator-exit-test --only X prints PASSED, rc 0, with no check run -- `cycle/exit-onlyX.out`
PROOF: 19:25 P10 guest: the 069fc2704421 image ships no /usr/bin/cloud_migrate_layout, so vm-walks/cloud-epic/migration-protocol.sh refuses on it -- `cycle/guest-checks.txt`
PROOF: 19:30 P11 guest: tools/vm-stop stops the owned QEMU in 0.25 s and removes its pidfile; the guest held 2,662,384 kB resident on the host after boot -- `cycle/guest-checks.txt`, this log

## [Stage C] 19:38 onward — the second opinion (stage B committed at 19:38:11)

- **Stage B's documents** are committed in `6cc544cd56`:
  - `02`: the controls, the cycle, 11 proofs, 20 findings and the 60 coverage rows (`grep -c -E '^\| \`tools/'` gives 60);
  - `03`;
  - `04`: Q5's cost table and Q6's value table.
- **The coordinator's reading on #659, 19:33:** the cycle is accepted; criterion 9 names the `.img.gz.sha256` sidecar; F-01, F-02 and F-03 are stage-D bugs with their inputs; F-10 is a Q2/Q6 row.
- **The packet:** `tools/t12-packet.py` writes `second-opinions/gpt-brief.md` and `packet-manifest.json`.
  - **Contents:** the ask; `02`, `03` and `04` whole; the 57 text files at the hash, line-numbered; the three PNGs named with size and sha256; `vm-first.md` and `generic-x64-vm-testing.md` from `next`; the controls' and the cycle's outputs. 712,845 bytes, sha256 `b733086bc58d…`, 71 manifest parts.
  - The controls' part reads `.qa-scratch/t12/controls/summary.txt`, written from the logs before the second build.
- **The scan before it was sent (19:39:36):**
  - `.githooks/secret-patterns`, sourced as the hook sources it and checked to compile: **0 lines** (grep rc 1). Matching lines are counted, not printed.
  - `tools/forbidden-terms-check --stdin`: `0 hits`, rc 0.
- **Setup (19:39:56 to 19:40:26):**
  - `npm install --prefix tools/council` rc 0;
  - `tools/council/run verify-pins`: `OK - verifier pins match current files and every re-pin is accountable.`;
  - `tools/council/run test` rc 0: 39/39, 127/127 and 19/19, fail 0.
- **The probe:**
  - **The first attempt (19:40:53) returned rc 4,** `[FAIL local_config_error] Failed to read prompt file`: `run` resolves paths from the worktree root, and the command passed them relative to the audit folder. No seat was reached.
  - **The second (19:41:05 to 19:41:15), with absolute paths,** returned rc 0, `READY`. The provenance reads:
    - `verification PASS` (semantic), observed `openai/gpt-6-astra`, model identity from the provider's response;
    - `effort_verification PASS`, max, 349 reasoning tokens;
    - `provider_verification PASS`, OpenAI;
    - `outcome success`.
- **`review-plan.json`** was written before the refutation call: depth `independent`, scope `epic`, primary `anthropic/claude-opus-5-5`, one reviewer `gpt` (`openai/gpt-6-astra`, `openai`, `max`), OpenRouter, `allow_fallbacks false`.
- **The refutation:** `timeout 5400 tools/council/run invoke --member gpt --provider openrouter --prompt-file <abs>/gpt-brief.md --output <abs>/gpt-audit.md`, in the background.
  - **What watches it:** the harness's background task, which notifies this session when the call exits, and `/workspace/tmp/m6-t12/refutation-start.txt`, which gets its rc line.
  - **How the watch fails:** a call killed outright writes no rc line. Its output then does not appear.
- **The refutation finished** (19:41:36 to 20:16:02, `/workspace/tmp/m6-t12/refutation-start.txt`): rc 0, the first attempt.
  - **The provenance:** `verification PASS`, observed `openai/gpt-6-astra`; `effort_verification PASS`, 44,475 reasoning tokens; `outcome success`.
  - **The call:** 221,398 prompt tokens and 52,369 completion tokens, USD 2.84.
  - **The output:** `gpt-audit.md`, 4,256 words, 72 new items (G-01 to G-72), refutations of F-01 to F-20, and what the seat could not judge.
- **The grading:** a read-only helper checks each G-item's cited lines against the export (`/workspace/tmp/m6-t12/seat-verify.md`). The lane has already read G-02, G-08, G-27, G-37, G-50, G-51, G-59 and G-60 at their lines; each verdict goes into `04` § Second opinion with the artifact that decided it.

## [Stage D] the punch list, the bugs and the audit issue

- **Grading** (`04` § Second opinion): 56 confirmed (2 High, 20 Medium, 34 Low), 15 narrowed to leads, 1 withdrawn (G-18).
  - The seat's refutations of F-01 to F-20 are answered there.
  - Its corrections to Q5 and Q6 are applied: ten suites under 3 s; the host column under a default run; `ra-offline`'s default guest; #361 is an origin, not a catch; `exit` has no catch but has a positive; F-10's evidence cell.
- **`05`:** 23 items, generated by `tools/punch-items.py`, each with `question:`. The pre-issue lint prints `PASS pre-issue artifacts`.
- **The bugs:** 18, one per defect item, label `bug`, milestone M6. They are #966 to #983 (PL-01 to PL-18). `tools/box-check --issue N` gives 0 fail on each.
- **The audit issue:** #984, `Audit: M6 T12 the VM harness -- 23 findings (0 critical, 2 high, 12 medium, 9 low)`, labels `audit` and `punch-list`, milestone M6, attached as a sub-issue of #659. Its 23 checkboxes give `box-check` 0 fail.
- **The lane pauses here** for the coordinator's stream briefs (brief § 8). No file under `tools/` has changed on this branch: `git diff --stat facb2ae523 HEAD -- tools` is empty.

## [Stage E] S1: vm-qa's exit, selection and report (#966, #982; D-QA-061)

- **The stream briefs:** `docs/reviews/briefs/t12-streams.md` at `6d9898a493`, read with `git show` and not merged. The coordinator's dispatch on #659 is dated 20:57 UTC.
- **The control:** `tools/vm-harness-test` is new and host-only. Each case copies the tool under test into `.qa-scratch/t12/vm-harness-test/<case>/` beside doubles for ssh, scp, `cloud-test-backend` and `vm-pair`. TMPDIR, `ROCKNIX_ARTIFACTS`, `VM_PAIR_DIR`, `VM_QEMU_RUNTIME_DIR` and `CLOUD_QA_STATE` all point under the case directory, so no guest, device or cloud is touched and nothing is written under `/tmp`.
- **The unfixed tools:** `git archive facb2ae523 tools` was extracted to `/workspace/tmp/m6-t12/unfixed-tools/` (118 entries). The control ran against it with `--tools-from`.
- **The positives:** all seven cases fail against the unfixed runner (`streams/s1-unfixed.txt`).
  - `exit-skip` gives rc 0 over a SKIP row.
  - `only-unknown`, `only-empty` and `walk-empty` give rc 0 each.
  - `help-whole` is missing `link`, `ra-offline`, `walks` and `frame-diff`.
  - `report-unwritable` gives rc 1, but only after 3 guest calls.
  - `two-runs-one-minute` leaves 1 directory.
- **The fixes:**
  - `0ecbbb9339` (#966): a SKIP exits 3; an unknown or empty `--only`, or an empty `--walk`, exits 2.
  - `3c0b9d53c6` (#982): `--help` is whole. The report root is probed before the guest. The run directory carries seconds and is made by a `mkdir` that must succeed. A failed row or footer write is a FAIL. The footer records `bring-up Ns, fixture Ns`.
  - `ea2377f1ce`: the three list entries for `vm-harness-test`. `rules-check --quiet` rc 0; `.githooks/hooks-test` PASS.
- **After the fixes:** 7 PASS, 0 FAIL (`streams/s1-fixed.txt`). A generated report's footer reads `bring-up 0s, fixture 0s -- outside the suite rows ...`.
- **Still open:** the guest half of #966 (a real `vm-qa` run whose footer names its exit) waits for the single cycle after S5.
PROOF: 21:00 S1 fix-case: tools/vm-harness-test's seven S1 cases fail against facb2ae523's tools (0 PASS, 7 FAIL) and pass at 3c0b9d53c6 (7 PASS, 0 FAIL) -- `streams/s1-unfixed.txt`, `streams/s1-fixed.txt`

## [Stage E] S1 corrected: the report directory's claim (#982)

- **The S1 entry above is wrong on one point.** It said `two-runs-one-minute` passes at `3c0b9d53c6`. It passed there by luck.
  - **How it showed:** after S2's second commit the control printed `10 PASS; 1 FAIL`. The commit chain read that through `| tail -1 &&` and committed anyway (`813e4dd270`, whose tree is sound). Eight more runs failed 2 times.
  - **The cause:** both racing runs printed the same `report:` path. This host's `mkdir` is uutils coreutils 0.10.0 (`/usr/bin/mkdir -> ../lib/cargo/bin/coreutils/mkdir`). Of 300 pairs of racing calls on `/workspace` (ext4), both calls succeeded 41 times; with `os.mkdir`, 0 times. So `until mkdir` is no exclusive claim on this host.
  - **Upstream** (checked 21:12): no matching report. The nearest is uutils #12355 / Ubuntu bug 2152495, where concurrent `install -D` fails on EEXIST. That is the opposite direction and another command.
  - **Scope:** `git grep` over `tools`, `scripts`, `.githooks` and the cloud scripts finds no other `mkdir` used as a claim. Device scripts run busybox.
- **The fix,** `fc8754b29b`: the claim is `.vm-qa-claim`, opened with bash's noclobber (O_EXCL) inside the directory.
- **The control:**
  - `two-runs-one-minute` now runs three concurrent runs for five rounds.
  - `report-dir-claimed` is new and deterministic: an `mkdir` double answers 0 for an existing directory, as the host did, and the directories for the seconds around the start are pre-claimed.
  - Both fail at `facb2ae523` and at `3c0b9d53c6`, and both pass at `fc8754b29b` (`streams/s1-claim-correction.txt`). The whole control ran 5 times at 12 PASS, rc 0.
- **The friction line** is in `docs/friction-log.md`, citing #982.
PROOF: 21:11 S1-claim fix-case: report-dir-claimed and two-runs-one-minute fail at facb2ae523 and at 3c0b9d53c6 and pass at fc8754b29b; this host's mkdir is uutils coreutils 0.10.0 -- `streams/s1-claim-correction.txt`

## [Stage E] S2: bring-up, identity and tear-down (#969, #981)

- **The fixes:**
  - `9df1c65c68` (#969):
    - `vm-pair down`'s status is read before bring-up; 0 and 3 pass, anything else exits 1 before anything is judged.
    - `vm-pair up` runs with its own status read; a failure exits 1 naming it.
    - The guest's whole BUILD_ID is compared with the image's build: `identity.json`'s `build_commit` when the sidecar is present (an unreadable one names nothing), else the `g<12 hex>` in the name. A mismatch, or an image that names no build, exits 1.
    - The header carries `BUILD_ID <id> -- the image names <id>`.
    - The run takes the pair down at the end, recording `tear-down: vm-pair down rc N`; anything but 0 is a FAIL. An EXIT trap does the same on an earlier exit. `--keep-up` opts out and says so.
  - `813e4dd270` (#981): `fresh` reads `$PORT` and names `$GUEST`.
- **The two real images resolve:** `069fc2704421` through its sidecar (the full `069fc270442134fe…`), `6e3a2165d415` through its name.
- **The positives:** 0 PASS, 4 FAIL against `facb2ae523` (`streams/s2-unfixed.txt`):
  - `up-fails-guest-answers`: rc 0 and a green report over a failed `up`;
  - `build-id-mismatch`: rc 0 over another build's guest;
  - `down-at-end`: no `down` after `up`;
  - `fresh-port`: all five reads at 10022.
- **After the fixes:** 4 PASS, 0 FAIL (`streams/s2-fixed.txt`); the whole control 12 PASS (`streams/s1-s2-full.txt`).
- **Still open for the cycle:** the fixed runner brings the pair up from the `069fc2704421` image; the report's BUILD_ID matches the image's; `tear-down: vm-pair down rc 0`; the census reads 0 after.
- **Already written:** the 19 full runs in the record each began with a `down` whose status nobody read, and their reports name the requested image. Whether any of them judged a surviving guest cannot be known from the reports. Per the brief, that is noted for the catalog at integration; nothing on a device.
PROOF: 21:11 S2 fix-case: up-fails-guest-answers, build-id-mismatch, down-at-end and fresh-port fail at facb2ae523 (0 PASS, 4 FAIL) and pass at 813e4dd270 (4 PASS, 0 FAIL) -- `streams/s2-unfixed.txt`, `streams/s2-fixed.txt`

## [Stage E] S3: the walks' preconditions and the ES sources (#973, #974, #981)

- **The fixes:**
  - `5edb265e59` (#974):
    - Every seeding step's status is read, and the walks' preconditions run inside the suite, so a failure is a FAIL before the first walk.
    - The guest's active remote must have the backend's endpoint fields (type, url, endpoint, host, port) before anything is seeded or walked. Only those fields are read off the guest, with the dropping filter over them too.
    - Fixtures are reseeded on a manifest (every file's name and sha256 on the guest). Writing it is the positive check that the seed wrote every file.
    - A guest file the seed would overwrite that no manifest names is a refusal naming it. The content seed's paths are read from the backend's script.
  - `a68bfadcd5` (#973): a walk starts only after a new boot id and then an answering EmulationStation, each within 135 s.
  - `ca0bf841d2` (#981): the six ES_SRC suites SKIP, with both hashes in the row, unless ES_SRC's HEAD is the pin read from the build's own commit. register's row says when it ran without the interface's citations.
- **The positives:** 0 PASS, 7 FAIL against `facb2ae523` (`streams/s3-unfixed.txt`).
  - `reboot-same-boot-id`, `reboot-es-silent`, `seed-scp-fails` and `remote-not-qa`: each walks on, rc 0.
  - `reseed-manifest`: no reseed.
  - `overwrite-refused`: 1 copy and 1 cloud reset over a file no manifest names.
  - `es-src-mismatch`: rc 0, the check run on the wrong source.
- **After the fixes:** 7 PASS, 0 FAIL (`streams/s3-fixed.txt`). `remote-not-qa` also finds its stand-in credential in no output. The whole control gives 19 PASS (`streams/s1-s3-full.txt`).
- **The split:** S3's diff was split into its three commits from `HEAD` (hunk 11 held #974's `walks_ready` and #973's `wait_rebooted`). Each commit's control ran before it was committed: 16, 18 and 19 PASS, rc 0.
- **For the cycle:** the build commit `069fc270442134fe…` is not in this repo (`git cat-file -e` fails). Without it the ES pin is unreadable and the six ES suites SKIP, so the run exits 3. The cycle fetches that commit read-only first, or records the SKIPs as the answer.
- **Already written:** the walks in the record ran against the QA endpoint by construction of their runs. Fixtures seeded by the old runner have no manifest, so a `--skip-up` rerun on such a guest refuses by name until those files are removed. A fresh pair (`vm-pair up`) has none. Nothing on a device.
PROOF: 21:20 S3 fix-case: reboot-same-boot-id, reboot-es-silent, seed-scp-fails, remote-not-qa, reseed-manifest, overwrite-refused and es-src-mismatch fail at facb2ae523 (0 PASS, 7 FAIL) and pass at ca0bf841d2 (7 PASS, 0 FAIL) -- `streams/s3-unfixed.txt`, `streams/s3-fixed.txt`

## [Stage E] S4: vm-pair and vm-stop (#970)

- **Host state before the stream:** `ls -la /tmp/rocknix-vm-pair` shows an empty directory (`.` and `..` only). The census `pgrep -c -x qemu-system-x86` reads 0. Both are in `streams/s4-fixed.txt`. Whether a past `up` destroyed another session's disk is not in the record.
- **The fixes, in this order on purpose:**
  - `33b1bb8845` (vm-pair):
    - Before `up` or `reimage` removes a disk or its OVMF vars, every process this user can read is checked (an open descriptor on it, or a `qemu-system-*` argv naming it). A hit refuses, naming the pid and the argv's first word.
    - A partial `up` stops the guest that started and exits with the failed guest's status.
    - `down` stops both guests and exits with the worst status.
    - `up` and `reimage` accept 3.
  - `eddd21d7a2` (vm-stop):
    - A missing pidfile exits 3 and removes nothing.
    - One descriptor from the read to the unlink; a replaced pidfile is reported and kept. The remaining window is named in the code.
    - G-26 is in the header as a design.
  - **Why vm-pair first:** the old `vm-pair up` runs `stop_one a; stop_one b` under `set -e`, so `vm-stop`'s 3 landing first would have aborted every fresh host's `up`. Each commit's tree ran both controls at rc 0 before it was committed. `vm-pair`'s new cases also pass beside the old `vm-stop`.
- **Running the controls:** both use `tempfile`, so they ran with `TMPDIR=/workspace/tmp/m6-t12/tmp`, not `/tmp`.
- **The positives** against `facb2ae523` (`streams/s4-unfixed.txt`):
  - `disk-held-no-pidfile`: the held disk was deleted.
  - `partial-up-rollback`: guest a was left running.
  - `down-stops-both`: guest b was never stopped.
  - `pidfile-changed-under-us`: rc 0, with the replaced pidfile removed.
  - `missing-pidfile-exit-3`: rc 0. Checked on its own, because the test stops at its first failed assertion.
- **After the fixes:** `vm-pair-test` gives 9 launch controls and 3 whole-script controls, rc 0. `vm-stop-test` gives 8 controls, rc 0. No fixture process survived, and the census is 0 (`streams/s4-fixed.txt`).
- **Still open for the cycle:** `down` exits 0, and the census after is 0.
- **Already written:** `worktrees.md` and `generic-x64-vm-testing.md` describe stopping through `tools/vm-stop` by pidfile. Exit 3 goes into PL-22's packet, not here.
PROOF: 21:25 S4 fix-case: disk-held-no-pidfile, partial-up-rollback, down-stops-both, missing-pidfile-exit-3 and pidfile-changed-under-us fail against facb2ae523's vm-pair and vm-stop and pass at eddd21d7a2 (vm-pair-test and vm-stop-test rc 0) -- `streams/s4-unfixed.txt`, `streams/s4-fixed.txt`

## [Stage E] S5: the host state belongs to the worktree (#971, #979; D-INFRA-031)

- **The fixes:**
  - `3f5998bbaf` (vm-pair):
    - `VM_PAIR_DIR` defaults to `<checkout>/.qa-scratch/vm-pair`.
    - `VM_QEMU_RUNTIME_DIR` is the explicit value, else the one `$VM_PAIR_DIR/RUNTIME` records, else `${XDG_RUNTIME_DIR:-/tmp}/pixelelated-vm-<sha8 of the checkout path>`. `up` and `reimage` record it.
    - 10022, 10023, 5909 and 5910 are probed with `ss` before a launch, and a holder is refused by pid. Without `ss` the check fails closed.
    - `info` prints the resolved paths.
  - `373a366e40` (vm-qa, time-to-play, ra-offline-test, emulator-exit-test):
    - `vm-qa` exports the pair's paths, `CLOUD_QA_STATE=<checkout>/.qa-scratch/cloud-qa` and `TMPDIR=<checkout>/.qa-scratch/vm-qa-tmp/<run>`.
    - `vm-qa` refuses a backend port whose holder does not name this run's `CLOUD_QA_STATE`. The port is fixed per backend, so another checkout's server would otherwise have answered, and the walks reset and seed what they talk to.
    - `vm-qa` prints the paths in the header.
    - `time-to-play`'s ssh master socket goes under `XDG_RUNTIME_DIR`, and its key default follows the pair.
    - `ra-offline-test`'s key and sockets follow the pair, and its three fixed `/tmp` files go through mktemp.
    - `emulator-exit-test`'s usage line changes. `vm-visual-qa` is unchanged: its mkdtemp follows the TMPDIR `vm-qa` sets.
  - `f1331aba83` (vm-upgrade-rehearsal): the report root is read from `ROCKNIX_ARTIFACTS`.
- **Two readings of the brief, stated:**
  - The brief's `time-to-play:137-139` are the fixture ports at `facb2ae523`, not scratch files. The scratch is `:158` (moved) and `:803`/`:938` (they follow TMPDIR).
  - The brief keeps the report root at `${ROCKNIX_ARTIFACTS:-/workspace/artifacts}/rocknix-images`, but its acceptance wants all five printed paths under the worktree or `/run/user/1000`. The header prints pair, runtime, QA cloud, scratch and key, all under one or the other, and names the report root as the exception.
- **The positives:** 0 PASS, 5 FAIL against `facb2ae523` (`streams/s5-unfixed.txt`).
  - `two-checkouts-two-states`: two checkouts share every socket and `/tmp/rocknix-vm-pair/qa-key`.
  - `runtime-recorded`: `up` records nothing. The unfixed `down` is never run, because its `/tmp` default could be another session's.
  - `port-held-refused`: `up` launches both guests with 10022 held.
  - `no-tmp-writes`: a temp file aimed at `/tmp/`, and the key under `/tmp`.
  - `rehearsal-artifacts-root`: the report directory under `/workspace/artifacts`, seen through an `mkdir` double that does not create it.
- **After the fixes:** 5 PASS, 0 FAIL (`streams/s5-fixed.txt`). The whole set is in `streams/s1-s5-full.txt`: `vm-harness-test` 24 PASS, `vm-pair-test` and `vm-stop-test` rc 0, no fixture left. This checkout's `vm-pair info` reads `VM_PAIR_DIR=<worktree>/.qa-scratch/vm-pair VM_QEMU_RUNTIME_DIR=/run/user/1000/pixelelated-vm-1c7e8c12`.
- **Deviations, recorded as they happened:**
  - `no-tmp-writes`' first form ran the unfixed `vm-qa` with TMPDIR unset. That made `/tmp/tmp.dLtl5SdwPE` and `/tmp/tmp.YpBcMXuAU5`, which the old runner removed itself (both absent when checked).
    - The `mktemp` double now records where a file would land and makes a `/tmp`-aimed one inside the case.
    - A `find /tmp -newer <mark> -user <me> -name 'tmp.*'` around both runs then counted 0.
  - `runtime-recorded`'s first form dropped its own explicit `VM_QEMU_RUNTIME_DIR` (the test's `env()` dropped after updating). Four fixture processes outlived the run.
    - They were stopped by PID after their cmdlines were checked against this case's scratch disks.
    - The test now drops before updating and reaps every pidfile under the case.
- **Superseded:** the lane's earlier cycle overrides under `/workspace/tmp/m6-t12/` are replaced by these defaults. The stage-E cycle runs with none set.
- **Still open for the cycle:** `vm-qa <image>` from this worktree with no override set; the header's paths under the worktree or `/run/user/1000`.
- **Already written:** `~/.cache/rocknix-cloud-qa` and `/tmp/rocknix-vm-pair` are left as they are; the M7 lane's older checkout may use them. Nothing on a device.
PROOF: 21:34 S5 fix-case: two-checkouts-two-states, runtime-recorded, port-held-refused, no-tmp-writes and rehearsal-artifacts-root fail at facb2ae523 (0 PASS, 5 FAIL) and pass at f1331aba83 (5 PASS, 0 FAIL; the whole control 24 PASS) -- `streams/s5-unfixed.txt`, `streams/s5-fixed.txt`, `streams/s1-s5-full.txt`

## [Stage E] S6: time-to-play measures or fails (#967, #983; D-QA-062)

- **The fixes:**
  - `7c5d15b2d8` (#967):
    - Usage errors (exit 2): `--repeat` below 1, and an `--only` naming no cell or an unknown one.
    - The online exit sync is timed only on a completed stamp: rc 0 or 9, with the token read. A failing stamp keeps its token, its time moves to `t_sync_stamp_unmeasured`, it is named by the judge, and `over_budget` skips it.
    - A g2g row needs its stamp.
    - Every cell that ran is judged: a cell with no rows, the startup arms, the conditions.
    - A launch first ends a running RetroArch through the guest's helper, and the row records that it did.
  - `a09bfc5718` (#983):
    - G-11: `scaled` None fails qualification.
    - G-13: `seed_payload` seeds the launched ROM's saves and records the paths.
    - G-14: the kill helper is checked when installed and reinstalled after every reboot; a kill's status goes on its row and a failed kill fails the run.
    - G-15: `restore()` and the handlers exist before the first change, and the whole setup through `Frames()` runs under them. A failed backup scp stops the run.
    - G-16: a saved copy goes back whatever its size; an `.absent` marker removes a file the run created; seeded saves are removed; `read_routes` keeps every default route.
  - **The split:** hunk 19 held #967's judging and #983's kill-rc judge. The #967 file was built from `HEAD` without that block. The controls before each commit: 29 PASS, then 30.
- **The positives:** 0 PASS, 6 FAIL against `facb2ae523` (`streams/s6-unfixed.txt`).
  - `repeat-zero` and `only-empty-cells`: both run on into the guest's setup through the doubles, rc 1 at the monitor socket. P8 is the guest form: rc 0 with empty cells.
  - `sync-stamp-failed`: judged `[]`, and over budget at 9 s, so a failure was timed.
  - `g2g-no-stamp`, `cell-ran-unmeasured` and `scaled-none`: each judged `[]`.
- **After the fixes:** 6 PASS, 0 FAIL (`streams/s6-fixed.txt`).
- **Still open for the cycle:** `--quick` on guest a once. Every row must be measured or the run fails, and the exit sync's stamp must complete.
- **Already written:** the record's `time-to-play.md` files and `docs/vm-qa-log.md` stand as history. The cycle's rows are re-read in `02` and marked (*would fail under D-QA-062*) where they would. No budget changes; nothing on a device.
PROOF: 21:42 S6 fix-case: repeat-zero, only-empty-cells, sync-stamp-failed, g2g-no-stamp, cell-ran-unmeasured and scaled-none fail at facb2ae523 (0 PASS, 6 FAIL) and pass at a09bfc5718 (6 PASS, 0 FAIL) -- `streams/s6-unfixed.txt`, `streams/s6-fixed.txt`

## [Stage E] S7: emulator-exit-test and device-act refuse what they cannot prove (#968, #978)

- **The fixes:**
  - `00b8760457` (#968): `--only` takes only letters from A to D; anything else exits 2, naming it, before any guest call.
    - **The lane's choice on D:** `--only D` alone exits 2. D checks what a launch left behind, so it runs only beside A, B or C. The header, which `--help` prints, says so.
  - `c1569b7bc6` (#978):
    - The record must take a write before anything, the boot-id probe included, else exit 2. A BEGIN that cannot be written refuses the same way.
    - A failed END fails the run and says "recorded nothing".
    - The command and label are logged through the mask from `engineering-practices.md` (`key=***`). `%q` still keeps the line one line, and the mask is left unescaped.
    - A timeout says what `DEVICE_ACT_TIMEOUT` bounds.
- **The positives:** 0 PASS, 5 FAIL against `facb2ae523` (`streams/s7-unfixed.txt`).
  - `exit-only-unknown`: PASSED, rc 0, after 17 guest calls. P9 is its guest form.
  - `exit-only-d-alone`: PASSED, rc 0.
  - `act-begin-unwritable`: the act reached the fixture, rc 0.
  - `act-end-fails`: rc 0, with no word of the failed END.
  - `act-masked`: the stand-in value is in the log.
- **After the fixes:** 5 PASS, 0 FAIL (`streams/s7-fixed.txt`).
  - **The one target:** the fixture `ssh` on `PATH`; nothing reached a device (D-QA-015).
  - **A first-run failure:** `act-masked` first failed on the fix because `%q` escaped the mask to `key=\*\*\*`. The value was absent even then. `logq` now unescapes the mask.
- **Still open for the cycle:** `emulator-exit-test --only A` on guest a.
- **Already written:** `/workspace/artifacts/rocknix-device-actions.log` holds every past act's full command. The coordinator reads it through the dropping filter at integration. Nothing on a device.
PROOF: 21:45 S7 fix-case: exit-only-unknown, exit-only-d-alone, act-begin-unwritable, act-end-fails and act-masked fail at facb2ae523 (0 PASS, 5 FAIL) and pass at c1569b7bc6 (5 PASS, 0 FAIL) -- `streams/s7-unfixed.txt`, `streams/s7-fixed.txt`

## [Stage E] S8: vm-visual-qa and vm-serial (#972, #976, #983)

- **The fixes:**
  - `ff10d77c28` (#972):
    - `wait_for_change` returns `None` when no frame arrived, and `run_steps` raises naming the press. None is falsy, so `cloud-round-trip`'s callers still fail.
    - A walk short of its named shots exits 3, naming them; a frame that is not a whole image counts as missing.
    - The stdlib PPM reader raises at EOF instead of spinning.
  - `2e790e7e52` (#976):
    - `vm-serial` runs the command in a subshell and returns its status from the END marker. A missing marker exits 124 (it was 2), and no caller read 2.
    - Both drains have an absolute deadline.
    - Every ssh and scp in `vm-qa`, `emulator-exit-test` and `ra-offline-test` runs under `timeout` (`VM_SSH_BOUND`, defaults 300, 120 and 300 s).
    - A cut goes to stderr and to `SSH_CUT_LOG`. `vm-qa`'s footer counts the cuts, and `emulator-exit-test` counts them as a failure. `ra-offline-test` says them on stderr only.
    - `time-to-play`'s scp calls get 120 s.
  - `05117efe58` (#983):
    - G-35: VNC coverage is counted by pixel in both grabbers, and `vnc-grab.py` fails on an incomplete frame.
    - G-39: `dismiss_dialogs_checked` ends on "carousel", "unmoved", or a WalkFailed for "limit" and "no frame". `dismiss_dialogs` keeps returning the count.
  - **The split:** `vm-visual-qa`'s hunks were divided across the three commits. The controls before each commit: 38, 40 and 41 PASS.
- **How the cases were first run, and two fixes to them:**
  - `ssh-never-ends` first looked for the cut on `vm-qa`'s stderr. `fresh_suite` sends ssh's stderr to `/dev/null`, so the cut was enforced (8 s, not 150) but said nowhere. That is why `SSH_CUT_LOG` and the footer line exist.
  - `vnc-partial`'s double first held the connection open, so the fixed grabbers failed by timeout. The double now closes, and they fail with `vnc closed`.
  - The unix sockets of the monitor and serial doubles are under `XDG_RUNTIME_DIR`, since a case path is past the 107-byte cap. None survived the runs.
- **The positives:** 0 PASS, 6 FAIL against `facb2ae523` (`streams/s8-unfixed.txt`).
  - `screendump-fails` and `fewer-frames`: rc 0 with a WARN.
  - `ppm-truncated`: hung past 10 s.
  - `serial-false`: `sh false` rc 0.
  - `ssh-never-ends`: ran past 40 s.
  - `vnc-partial`: both grabbers returned a frame.
- **After the fixes:** 6 PASS, 0 FAIL (`streams/s8-fixed.txt`).
- **Already written:** the accepted baseline `walk-baseline` (build `d72084ccad`) was counted against `suite.txt` and the step files at that commit (`streams/s8-baseline-frame-counts.txt`). All 16 walks hold exactly the frames their steps name, 78 in all, so no recorded walk in it lost a frame silently.
- **Still open for the cycle:** `vm-serial sh false` on guest a exits non-zero, and the walks suite's frame counts equal its step files'.
- **A gap named:** `vm-serial`'s own `--socket` default is still `/tmp/rocknix-qemu-serial.sock`; S5's files did not include it. The cycle passes `--socket` explicitly. Filed as a line on #983 for S13.
PROOF: 22:00 S8 fix-case: screendump-fails, fewer-frames, ppm-truncated, serial-false, ssh-never-ends and vnc-partial fail at facb2ae523 (0 PASS, 6 FAIL) and pass at 05117efe58 (6 PASS, 0 FAIL) -- `streams/s8-unfixed.txt`, `streams/s8-fixed.txt`
PROOF: 22:00 S8-baseline history: walk-baseline (d72084ccad) holds the frames its steps name for all 16 walks (78 frames) -- `streams/s8-baseline-frame-counts.txt`

## [Stage E] S9: ra-offline-test and qa-accounts (#977, #983)

- **The order, forced:** the fixed `ra-offline-test` calls `qa-accounts --host ...`, which the old `qa-accounts` rejects, so `qa-accounts` landed first. The controls before each commit: 42, 47 and 47 PASS.
- **The fixes:**
  - `9a1300f141` (#983, G-58): `qa-accounts` takes `--host`, `--port` and `--identity`. Its RetroAchievements write is read back for equality, including the switch: the values cross ssh's stdin, and only the names that differ come back. The ScreenScraper branch keeps its name readback.
  - `33efb4d801` (#977):
    - The host and key reach `qa-accounts`.
    - From the account step on, cleanup runs once on any exit, and each of its steps is counted.
    - `absent()` makes a negative check read first.
    - `field_is` and an anchored id make the matches exact.
    - Every capture requested with `--frames` is checked by name.
    - G-45: `--guest`, and the pidfile's QEMU must name the port and both sockets, else exit 2.
    - G-52 is written into the header as a design.
  - `15b8f11334` (#969): the same trap defect in `vm-qa`'s exit trap.
- **A defect found while landing it:** `cleanup-counted` passed once and then failed five times in five. The SIGTERM landed inside `S '...disable' >/dev/null 2>&1`, and bash runs a trap inside the command it interrupted, under that command's redirections. The whole cleanup ran and its report went to `/dev/null`.
  - The tool now saves its stdout and stderr at the start and restores them in `on_exit`. After that, five of five passed.
  - `vm-qa`'s exit trap had the same shape, and was fixed in its own commit.
- **The cases' first form ran the unfixed tool into its `/tmp` socket defaults,** so it stopped at the preconditions, and those were FAILs for the wrong reason. The cases now name `--monitor` and `--serial`, which both versions take.
- **Nothing reached a guest, a device, retroarchievements.org or a credential file:**
  - `curl` answered from a fixed JSON;
  - the serial double answers markers and runs nothing;
  - `qa-accounts` was a double, except in `accounts-readback`, which ran the real one against a stand-in accounts file and an ssh double.
  - The account path never ran.
- **The positives:** 0 PASS, 6 FAIL against `facb2ae523` (`streams/s9-unfixed.txt`).
  - `negative-read-fails`: "PASS nothing listens" over a failed read.
  - `host-passed-through`: `qa-accounts 10026 ra`.
  - `cleanup-counted`: no cleanup on a stop.
  - `flushed-exact`: `flushed=10` and achievement 1003590 both accepted.
  - `endpoints-inconsistent`: no check; the run stopped at its preconditions.
  - `accounts-readback`: rc 0, "set", over a key that differs.
- **After the fixes:** 6 PASS, 0 FAIL (`streams/s9-fixed.txt`), with no fixture left.
- **Already written:** the QA account's state on the RetroAchievements side is untouched. The real-account proof stays the release procedure's.
PROOF: 22:15 S9 fix-case: negative-read-fails, host-passed-through, cleanup-counted, flushed-exact, endpoints-inconsistent and accounts-readback fail at facb2ae523 (0 PASS, 6 FAIL) and pass at 15b8f11334 (6 PASS, 0 FAIL) -- `streams/s9-unfixed.txt`, `streams/s9-fixed.txt`

## [Stage E] S10: vm-upgrade-rehearsal (#979)

- **The fix,** `82b5edf1ee`:
  - A count of zero settings archives before the update fails the rehearsal before it updates. Afterwards the archives must match by count and by name.
  - The seed's own manifest (sha256, name and size) is compared file by file, and a change is named.
  - The pair comes down on every exit after `up`, and a failed stop fails the result.
- **The doubles grew:** the `vm-pair` double forwards `ssh` and `scp` to the ssh double, and the ssh double gains `@seq:` rows, so boot ids, build ids and the manifest can change between calls. `rehearsal-clean` is the control's own control: the doubles' guest passes the rehearsal on both versions.
- **A row error, found and fixed:** the RetroArch check joins its lines with the guest's own `tr`, so its row must be one line. With three lines, both versions read FAIL, which hid the positives.
- **The positives:** against `facb2ae523` (`streams/s10-unfixed.txt`, 1 PASS, the clean control, and 3 FAIL):
  - `rehearsal-no-archive`: RESULT PASS with no archive.
  - `rehearsal-stop-fails`: RESULT PASS with a failed stop.
  - `rehearsal-hash-changed`: RESULT FAIL, but without naming the file. This is the weaker positive the brief describes; the old whole-string compare caught the change and did not say which file.
- **After the fix:** 4 PASS, 0 FAIL (`streams/s10-fixed.txt`).
- **Gated on the port-free cases only:** the pair was up, so `port-held-refused` and `runtime-recorded` waited for the end of the cycle.

## [Stage E] Two defects the stage-E cycle found in my S6 and S8 fixes (#976, #967)

- **`vm-serial`, found on real guest b.** The console sent `END<tag>` and `:<status>` in separate chunks. `run()` stopped at the bare tag, so `sh false` and `sh true` both returned 124. The double sent one chunk, which is why `serial-false` passed.
  - Fixed in `1d5dc8a698`: read until `END<tag>:<digits>` and a line end have arrived.
  - On guest b afterwards: `sh false` 1, `sh true` 0, `exit 7` 7 (`cycle-e/s8-serial-b-fixed.txt`; the failing reads are in `cycle-e/s8-serial-b.txt`).
  - `vm-pair`'s key install reads the same channel, and was flaky on a real guest until this fix.
- **`time-to-play`, found by the cycle's `--quick` on guest a.** Two things:
  - "The kill helper exited 1" was a false failure from my judge. `execute_kill` ends in `killall <every emulator name>`, which exits 1 after a clean kill, and RetroArch was gone in 0.16 s.
  - The g2g row had no stamp (`-`, token `?`) because it read the stamp once, before the stopped sync wrote it.
  - Fixed in `327e743189`: a kill is judged by its effect, and the g2g repeat waits up to 30 s for its stamp. The wait has no host case; the second cycle proves it.
- **The cases:** `serial-split-marker` fails at `05117efe58`, and `kill-judged-by-effect` fails at `a09bfc5718`; both pass at `95241c0158` (`streams/cycle-found-fixes.txt`).
- **What it says about the controls:** a double that delivers in one chunk, or a helper's exit status read as its effect, passes code a real guest breaks. That is the reason the brief puts guest acceptances in the cycle.

## [Stage E] S13: the small fixes, one commit per tool (#983)

- **The commits:**
  - `3edb5f2b89` `png-blackout` (G-62): an empty or off-image rectangle is refused; the text chunks are dropped.
  - `8e29c6e2cc` `es-untranslated` (G-63, G-64): an unreadable or empty current source exits 2; fuzzy and `msgctxt` entries are not French.
  - `181b67293a` `font-stems` (G-69): a reversed or malformed `--sizes` exits 2; failed glyphs are counted and fail the run.
  - `a4ae0aee6c` `ra-candidate-games` (G-68): the bare-list answer is read.
  - `d4ccc8b14b` `es-syntax-check` (G-65): the edit must be on the compile line (NO-SUB otherwise); the farm's statuses are read.
  - `f676d8bb5f` `es-launch-memory` (G-47): the identity is the pid plus its start time.
  - `95241c0158` `signin-memory` (G-47): the launch's status is read, the files carry a run token, and only processes started after the launch count.
- **How the commits were built:** each staged test file was `HEAD`'s plus only its own cases, and each commit was gated on the port-free cases, 50 to 60 PASS.
- **The positives:** 0 PASS, 9 FAIL against `facb2ae523` (`streams/s13-unfixed.txt`). After the fixes: 9 PASS, 0 FAIL (`streams/s13-fixed.txt`).
- **Three fixture faults fixed before the positives were trusted:**
  - `untranslated-unreadable-source` first lacked a git base, and failed for that reason.
  - `signin-memory-run-files` first matched its launch command on the `wayland-` row.
  - `launch-memory-start-time` was first a text match. It now runs the tool's own identity command against a live pid.
- **Gaps named, not fixed here** (outside S5's file list): `signin-memory`'s key default and `vm-serial`'s `--socket` default are still under `/tmp`.
PROOF: 22:45 S10 fix-case: rehearsal-no-archive, rehearsal-hash-changed and rehearsal-stop-fails fail at facb2ae523 and pass at 82b5edf1ee; rehearsal-clean passes on both -- `streams/s10-unfixed.txt`, `streams/s10-fixed.txt`
PROOF: 22:45 cycle-found fix-case: serial-split-marker fails at 05117efe58 and kill-judged-by-effect at a09bfc5718; both pass at 95241c0158 -- `streams/cycle-found-fixes.txt`
PROOF: 22:28 cycle-found guest: on guest b, vm-serial sh false 1, sh true 0, exit 7 7 after 1d5dc8a698 (124 for both before) -- `cycle-e/s8-serial-b.txt`, `cycle-e/s8-serial-b-fixed.txt`
PROOF: 22:45 S13 fix-case: the nine S13 cases fail at facb2ae523 (0 PASS, 9 FAIL) and pass at 95241c0158 (9 PASS, 0 FAIL) -- `streams/s13-unfixed.txt`, `streams/s13-fixed.txt`

## [Stage E] The stage-E pair cycle (22:14 to 22:48) and the second short cycle (22:56 to 22:59)

- **Cycle 1:**
  - **START at 22:14** under the 22:10 release. Census 0; `free -g` 41 GB available (`cycle-e/free-before.txt`).
  - **Before it:** the image matched its sidecar (`6b4c3079…`). The read-only fetch of `069fc270…` failed (`upload-pack: not our ref`), so the ES pin stayed unreadable (`02` § Why the six ES rows stayed SKIP).
  - **The run:** `tools/vm-qa <image>` from the worktree with no override, under `timeout 3600`.
  - **The report** (`cycle-e/vm-qa-report.md`):
    - BUILD_ID `069fc270442134fe…` = the image's.
    - The paths are under the worktree and `/run/user/1000`, with the report root `/workspace/artifacts` named as the brief's exception.
    - Bring-up took 75 s and the fixture 6 s; `tear-down: vm-pair down rc 0`; no ssh call was cut.
  - **The suites:**
    - PASS: pair-identity, fresh, round-trip, exit, walks (16 walks, 1029 s), frame-diff.
    - SKIP: the six ES suites (pin unreadable).
    - FAIL: scripts (326 checks; being settled by the two TMPDIR runs), wrapper (the RetroArch source is gone from the old build-root paths, host state), and time-to-play (two defects in my own S6 fix, below).
    - `vm-qa` rc 1.
  - **Acceptances met:**
    - S2: bring-up from the image, BUILD_ID matching, down rc 0, census 0 after.
    - S5: no override set, and the paths in the header.
    - S8: walks 16/16 hold the frames their steps name (`cycle-e/walks-vs-steps.txt`).
    - On guest b, while `vm-qa` drove guest a: S7 `emulator-exit-test --only A` rc 0, and S8 `vm-serial sh false` 1 (after `1d5dc8a698`).
    - **Deviation:** S7 and S8 ran on guest b, not a, because S2 needed `vm-qa` itself to take the pair down at the end.
  - **RETURN at 22:48:** census 0, 46 GB available. Disks retired: two 2.3 GB qcow2 and two OVMF stores, with their sizes and hashes in `cycle-e/retired.txt`.
- **M7 between the cycles:** M7's START landed at 22:50, within the 22:43 rule's 5 minutes, so M7 went first. Its FINAL RETURN came at 22:53, and my second cycle was released at 22:54.
  - The two scripts runs I had begun at 22:51 were stopped by PID at the release, so they would not load the host during `time-to-play`. They were restarted after the second cycle's RETURN.
- **Cycle 2:**
  - **START at 22:56;** `vm-qa <image> --only time-to-play` under `timeout 900`. Bring-up took 52 s; `tear-down: vm-pair down rc 0`; RETURN at 22:59, census 0, disks retired (`cycle-e2/`).
  - **The kill fix held:** no kill-helper failure, with RetroArch gone in 0.15 s.
  - **The g2g row still had no stamp, and the cause is the product's exit sync:** game 1's exit in the g2g repeat started no sync at all. `cloud_sync.log` has no `cloud_backup` after it, only `cloud_capture`, so no stamp was written and the 30 s wait could not help. The relaunch went 0.17 s after the kill; STOP IT AND PLAY was pressed at 1.36 s.
  - Under D-QA-062 the cell fails. The unfixed tool passed it, as token `?`. Whether an exit sync skipped with no stamp is intended or a silent outcome is put to the coordinator on #659.
- **S11's acceptance, the fixed compare over cycle 1's walks** (`cycle-e/frame-diff-fixed.md`): rc 1.
  - 78 screens of 16 walks; 43 live claims; 348 inert proposals.
  - 40 boxes claimed and 65 unclaimed: 64 are `0 0 552 708`, the Last Played backdrop, and one is `0 0 40 382` on `manager-nes/01-0-carousel.png`.
  - Cycle 1's own frame-diff PASS rested on those boxes, "claimed by 578", the proposal claims applied live.
  - Adopting the proposals or moving the baseline is the maintainer's (#346).

## [Stage E] S11 and S12 (#980; #975, #983)

- **S11:**
  - `36138c8da5` (frame-diff): an empty baseline exits 1; a scoped run compares only its walks; the `--min-pixels` sentence; a zero-size PNG is refused; `proposal:` claims are inert.
  - `476ab6e69b` (vm-walks): the three transfer masks cover only the transfer page; the 348 `#578` claims are marked `proposal:d72084ccad`, with no substance changed.
  - Written on a scratch copy while cycle 1's own frame-diff suite ran, and applied after it.
  - Against `facb2ae523`: 1 PASS (`claim-missing-still-fails`, the control's own control) and 6 FAIL (`streams/s11-unfixed.txt`). Fixed: 7 PASS (`streams/s11-fixed.txt`).
- **S12, one commit per tool:**
  - `6ca9da4831` vm-manager-system-check: explicit refusals; P6 reproduces at `facb2ae523`.
  - `6871f964c8` vm-stop-test, `b6413b19e8` vm-pair-test and `4757b48385` vm-upgrade-readiness-test: their asserts become `require()` through an `ast` rewrite.
  - `29bf33cbb8` ra-ui-test, `639b45a8a6` raofflineproxy-installed-native-test and `5988d06c9a` raofflineproxy-consent-test: each refuses under `-O` (exit 2) before argparse.
  - `930ea05d70` raofflineproxy-consent-test (G-67): the collector records the event, then `judge()` reports the problem without raising.
  - Against `facb2ae523`: 1 PASS and 7 FAIL (`streams/s12-unfixed.txt`). Fixed: 8 PASS (`streams/s12-fixed.txt`).
  - **No positive found for `vm-stop-test`:** the old test's port-reuse bind, a plain check rather than an assert, fails it under `-O` against the broken subject too.
  - **Two slips on the way:**
    - The first guard placement fell after a later import in the native test, so `--help` beat it. In `ra-ui-test`, it relied on a `sys` import that existed only inside the embedded guest script. Both guards now sit at the first import with their own `import sys`.
    - One staged gate lacked a helper (`guarded`), and that commit was redone; nothing broken was committed.
- **Every control in full on the final tree** (`streams/all-controls-final.txt`, at `930ea05d70`): `vm-harness-test` 77 PASS; `vm-pair-test`, `vm-stop-test` and `vm-upgrade-readiness-test` rc 0; no fixture left.
PROOF: 22:48 cycle guest: vm-qa <069fc2704421 image> with no override: BUILD_ID matches, tear-down vm-pair down rc 0, census 0 after, walks 16/16 frames equal to their steps -- `cycle-e/vm-qa-report.md`, `cycle-e/walks-vs-steps.txt`, `cycle-e/census-after.txt`
PROOF: 22:46 S7 guest: emulator-exit-test --only A on guest b ran part A, 3 PASS, rc 0 -- `cycle-e/s7-exit-only-a-b.txt`
PROOF: 22:59 cycle2 guest: --only time-to-play after 327e743189: no kill-helper failure; the g2g row has no stamp because no exit sync ran (cloud_sync.log) -- `cycle-e2/vm-qa-report.md`, `cycle-e2/time-to-play.json`
PROOF: 23:00 S11 guest: the fixed compare over cycle 1 walks: 65 unclaimed (64 the Last Played backdrop) once the 348 proposals are inert -- `cycle-e/frame-diff-fixed.md`
PROOF: 23:05 S11 fix-case: six cases fail at facb2ae523 and pass at 476ab6e69b; the control passes on both -- `streams/s11-unfixed.txt`, `streams/s11-fixed.txt`
PROOF: 23:05 S12 fix-case: seven cases fail at facb2ae523 and pass at 930ea05d70 (vm-stop-test: no positive found) -- `streams/s12-unfixed.txt`, `streams/s12-fixed.txt`
PROOF: 23:04 controls tool-run: every control in full at 930ea05d70: vm-harness-test 77 PASS; vm-pair-test, vm-stop-test, vm-upgrade-readiness-test rc 0 -- `streams/all-controls-final.txt`
