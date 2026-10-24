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
