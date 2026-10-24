# Second opinion on a code audit -- M6.P2 T12, the VM test harness, epic tier

You are a second reader of a code audit at the end of its reading stage. You cannot run commands or open the repository; everything you may cite is in the packet below, and every claim you make names the packet's `file:line` or the output it rests on. The first reader's verdicts are in the packet; do not take them as given.

The scope: 60 fork-own files (30 scripts: 20 Python, 10 bash; 22 `.steps` walk files, 3 text, 2 Markdown, 3 PNG fixtures named below by size and sha256; 8,790 lines) that make up a Linux distribution's **VM test harness**: the runner that runs 17 suites against one GENERIC_X64 image and writes one report (`tools/vm-qa`), the two-guest launcher (`tools/vm-pair`), the exact-owner stop (`tools/vm-stop`), the UI walk driver (`tools/vm-visual-qa`) with its step files, the frame comparator and its claims contract (`tools/frame-diff`, `tools/vm-walks/claims.txt`), the time-to-play measurement (`tools/time-to-play`), the exit-hotkey test, memory measurements, the offline-achievements scenarios, and their controls. Read at commit `8ebaf8daad`. The audit's lens is **cost against value**: what each suite costs in minutes and host, what it has caught, what it would miss. The first reader ran the three no-guest controls and **one bounded guest cycle** (its outputs are at the end of the packet); nothing was built, nothing touched a handheld.

Answer in three parts, in this order:

1. **Your own findings first, starting with these four**:
   - `vm-qa`'s accounting: can a run exit 0, or a suite read PASS, without having proved what it names? Where is the exit code computed, and what does a SKIP do?
   - `time-to-play`'s headline rule (`headline_missing`, `over_budget`): which inputs make it pass with nothing measured or with a number it should not trust?
   - `frame-diff`'s claims contract: can a claim, a mask or the baseline make a changed pixel invisible, and can a run pass with frames missing?
   - `vm-stop`'s wait: what it waits for, what happens on a timeout, and whether any caller can lose a guest or stop the wrong process.

   Then the rest. List every defect, gap or unsafe seam you find that is not already one of the first reader's findings. One line each: an id (G-01, G-02, ...), a severity (Critical / High / Medium / Low), the packet's `file:line`, what fails and when. Look especially for: a pass that does not depend on the thing measured; a wait that cannot time out; host state (`/tmp`, ports, the QA cloud) two sessions could share; a guest found or stopped by pattern; a credential printed.
2. **Refute the first reader.** For every finding F-01 to F-20 in `02` § Findings: agree, disagree, re-grade or narrow, and say what would make it false and whether the packet shows it. Say also whether `04` § Q3's suite-by-suite table misses a suite or a constructed input, and whether any row of `04` § Q5 or § Q6 is wrong on the packet's evidence.
3. **What you could not judge.** The claims the packet does not let you verify (the record's reports and the work logs are summarised, not included).

Keep each item to a few lines. At most 7,000 words.

# The packet

## 02-forward-audit.md (whole)

# Forward audit — M6.P2 T12, the VM harness (#659)

The 60 paths are read at `8ebaf8daad`'s bytes. The lens is cost against value (brief § 2), and the questions are plan § 4's Q1 to Q7. Line numbers are at the hash unless a row says otherwise.

## Phase 2: #659's checklist at stage B

| # | Criterion (abridged) | State at stage B | Artifact |
| --- | --- | --- | --- |
| 1 | the folder with `00` to `05` | `00` to `04` in progress; `05` at stage D | this folder |
| 2 | the lint `PASS` | before stage D, `--phase pre-issue` | stage C |
| 3 | `review-plan.json`, provenance, and the packet scanned | at stage C | `second-opinions/` |
| 4 | every item at a Phase 7 outcome | stage F | `05` |
| 5 | `reviewed-at` and `fixed-at` | `reviewed-at` `facb2ae523` (`00`) | #659's body at close |
| 6 | `01` § Scope | written | `01` |
| 7 | the coverage table, 60 rows | written below | § Coverage |
| 8 | § The controls | written below | § The controls |
| 9 | § The guest cycle | written below; the cycle was accepted on #659 at 19:33 | § The guest cycle |
| 10 | `00` shows nothing never-run | the cycle, the probes and the deviation are recorded | `00` |
| 11 | Q5's cost table | `04` § Q5 | `04` |
| 12 | Q6's value table | `04` § Q6 | `04` |
| 13 | Q3 hunted per suite | `04` § Q3 | `04` |
| 14 | Q7's three descriptions | `04` § Q7 | `04` |
| 15 | every proof with its class cell | below; equal to `00`'s PROOF count | § Proofs |
| 16 | `question:` on every item; no `tools/` change before a brief | stage D; `git diff --stat facb2ae523 HEAD -- tools` is empty | `05` |
| 17 | the retro, the checkers | stages G and H | — |

## Mechanical checks

| Check | Command | Exit | Summary |
| --- | --- | ---: | --- |
| Membership | brief § 2's block over `docs/reviews/inventory.json` | 0 | `paths 60 lines 8790`, 60 fork-own, reach `n/a` 60; 20 Python, 10 shell, 22 `.steps`, 3 text, 2 Markdown, 3 PNG |
| Lines at the hash | `git show 8ebaf8daad:<p> \| wc -l`, summed | 0 | 8,813, the 23 newline bytes in the PNGs included |
| Bytes | `git cat-file -s`, summed | 0 | 484,627 |
| Provenance | `git cat-file -e upstream/next:<p>`; `git log c445081a59..8ebaf8daad -- <the 60>` | 0 | 0 of 60 upstream; 145 commits (144 without merges) |
| Branch against hash | `git diff --stat 8ebaf8daad HEAD -- <the 60>` | 0 | empty |
| Find/stop by pattern | § 5's `pgrep\|pkill\|kill` grep over eight tools | 0 | 41 lines, all guest-side (P3) |
| `/tmp` roots | § 5's `/tmp/` grep over the 60 | 0 | 84 lines; the host-side ones are F-09 and the Q1 rows |
| Legacy paths | `git grep` for `rocknix.worktrees` or `/workspace/repos/rocknix` in the 60 | 0 | one: `es-syntax-check:53` (F-11, #640) |
| `assert` as a check | `git grep -c '^\s*assert '` over the Python | 0 | 7 tools (F-04's class) |
| Claims reconciliation | `/workspace/tmp/m6-t12/walks-reconcile.txt` | 0 | P5 |
| Q7 descriptions | `/workspace/tmp/m6-t12/q7-descriptions.txt` | 0 | the owning rule names 17 of 30; the index points six more at it (F-13) |
| Host versions | `qemu-system-x86_64 --version`; `python3 --version` | 0 | QEMU 10.2.1; Python 3.14.4 |

## The controls

Run at stage A in this worktree, 19:05:45 to 19:05:46 UTC, census 0 before and after. The logs are in `.qa-scratch/t12/controls/`.

| Control | Exit | Summary | A FAIL would mean |
| --- | ---: | --- | --- |
| `python3 -I tools/vm-pair-test` | 0 | `PASS 9 VM launch controls` | `vm-pair` could claim a guest up without its own PID owning its disk, or a launch failure could read as up |
| `python3 -I tools/vm-upgrade-readiness-test` | 0 | `PASS 7 storage-readiness controls` | the rehearsal's wait could accept a guest whose storage is not ready in the expected boot |
| `python3 -I tools/vm-stop-test` | 0 | `PASS 7 vm-stop controls` | `vm-stop` could signal a process that is not the owned QEMU, or report a stop before the exit |
| `./tools/vm-manager-system-check --help` | 1 | `FAIL manager system: not enough values to unpack` | (no `--help`; it fails closed, which is correct) |
| `./tools/raofflineproxy-integration-test --help` | 0 | the usage | (a usage line; not a test run) |
| `./tools/vm-qa --list` | 0 | 17 names | a suite added to or dropped from `SUITES` without the list moving |
| `./tools/time-to-play --help` | 0 | the usage | (a usage line) |
| `./tools/frame-diff --help` | 0 | the usage | (a usage line) |
| `./tools/vm-visual-qa --help` | 0 | the usage | (a usage line) |
| `./tools/vm-pair` | 2 | the usage | (a usage line) |
| `./tools/es-syntax-check` | 2 | `name at least one .cpp` | **not a pass**: it exits 2 without a build root, and its default root is absent (F-11) |
| `.githooks/hooks-test` | — | not run at stage A | (criterion 17's checker, at close) |

## The guest cycle

The one authorized cycle, 19:23 to 19:30 UTC; the full record is in `00` § The guest cycle and `cycle/`.

- **The image:** `069fc2704421`, sha256 `6b4c3079bdee2f47bd1149aac07b11714c591b847f22157fcd6d85f39a7e08fb`, read from the `.img.gz.sha256` sidecar, since the `.identity.json` carries no digest (criterion 9 was edited on #659 at 19:33).
- **The guest and the host:** one guest; pidfile `/workspace/tmp/m6-t12/cycle/rocknix-qemu.pid`; census 0 before and after. The host file's lines at 19:23:39Z and 19:30:19Z are quoted in `00`.
- **The run:** `vm-qa --skip-up --only fresh,round-trip,exit,time-to-play,frame-diff`, rc 0 in 3 min 6 s. Minutes per suite, against the record's medians (P4):

| Suite | This cycle | The record's median |
| --- | ---: | ---: |
| fresh | 1 s | 0 s |
| round-trip | 84 s | 84.5 s |
| exit | 27 s | 28 s |
| time-to-play | 72 s | 69 s |
| frame-diff | SKIP, 0 s | 1 s |

- **The verdict:** `**PASSED with 1 suite(s) SKIPPED**`, rc 0.
- **Time to play:** 0.74 / 1.59 / 1.01 s.
- **The probes:** `time-to-play --repeat 0` rc 0 (P8); `emulator-exit-test --only X` rc 0 (P9).
- **The stop:** `tools/vm-stop` rc 0 in 0.25 s.
- **Retired:** the disk (sha256 `230153933c0d…`) and the image copy (`cycle/RETIRED.txt`). No frame is kept: none is needed by a claim.

## The record

**The vm-qa reports** (P4; re-derived in `/workspace/tmp/m6-t12/q5-rederived.txt`; the research helper's per-report tables are in `/workspace/tmp/m6-t12/research-q5.md`):
- **Count:** 61 reports whose first line is `# vm-qa on`, in 27 folders under `docs/qa-logs/`. Two pairs are byte-identical, so there are 59 distinct runs, from 2026-10-03 to 10-15.
- **Full 15-suite runs:** 19, median 33 min (28 to 35).
- **`docs/vm-qa-log.md`:** 44 September run windows, median 25 min; its October rows carry no durations.
- **`time-to-play.log` files:** 16, in 13 folders.

**The value side** (`04` § Q6): read by a second helper and spot-checked by the lane (`00`).

## Proofs

| # | Claim | Evidence | Class |
| --- | --- | --- | --- |
| P1 | The 60 equal the brief at `8ebaf8daad`, and the branch's diff over them is empty | `.qa-scratch/t12/membership.txt`, `lines-at-hash.txt` | proved: tree |
| P2 | The three controls pass; `vm-qa --list` gives 17; `es-syntax-check` exits 2 without a root | `.qa-scratch/t12/controls/` | proved: tool-run |
| P3 | Every `pgrep`, `pkill` and `kill` in the eight guest-touching tools is guest-side; `vm-pair down` stops through `vm-stop` | `controls/kill-grep.txt`; `vm-pair:124-130` | proved: tree |
| P4 | The 61 reports' per-suite seconds and verdicts (59 distinct runs) | `/workspace/tmp/m6-t12/q5-rederived.txt` | proved: history |
| P5 | The claims reconciliation: no orphan claim and no unowned walk; 8 step files outside `suite.txt`; every key checked | `walks-reconcile.txt`, `steps-profile.txt` | proved: tree |
| P6 | `vm-manager-system-check` passes under `PYTHONOPTIMIZE=1` what it refuses without it | `.qa-scratch/t12/probes/manager-check-optimize.txt` | proved: tool-run |
| P7 | `vm-qa` exits 0 over a SKIP | `cycle/vm-qa/report.md`, `cycle/t-vmqa.txt` | proved: guest |
| P8 | `time-to-play --repeat 0` exits 0 with every headline cell empty | `cycle/ttp-repeat0/time-to-play.json` | proved: guest |
| P9 | `emulator-exit-test --only X` prints `PASSED` with no check run | `cycle/exit-onlyX.out` | proved: guest |
| P10 | The image ships no `cloud_migrate_layout`, so `migration-protocol.sh` refuses | `cycle/guest-checks.txt` | proved: guest |
| P11 | `vm-stop` stops the owned QEMU in 0.25 s; the guest held 2.54 GiB resident on the host | `cycle/guest-checks.txt`; `00` | proved: guest |

## Findings (stage B)

Severity and the punch list come at stage D. The coordinator's 19:33 reading makes F-01, F-02 and F-03 stage-D bugs, with their inputs.

| ID | Q | Finding | Where | Proof |
| --- | --- | --- | --- | --- |
| F-01 | Q3 | `vm-qa` exits 0 when a suite SKIPs: a run that has not passed reads green to a caller (`frame-diff` with no baseline; `scripts` with skipped checks, which exits 3) | `vm-qa:141-148`, `:528`, `:541` | P7 |
| F-02 | Q3 | `time-to-play` passes with nothing measured when `--repeat` is below 1 or `--only` names no headline cell: blindspot 39's shape, reachable outside `--quick` | `time-to-play:994-996`, `:1306-1332` | P8 |
| F-03 | Q3 | `emulator-exit-test --only` with none of A to D runs no check and prints `PASSED` | `emulator-exit-test:38`, `:145-196` | P9 |
| F-04 | Q2/Q3 | `vm-manager-system-check`'s refusals are `assert` statements, stripped by `-O` or `PYTHONOPTIMIZE`; six more tools, mostly controls, check with `assert` | `vm-manager-system-check:12-15` | P6 |
| F-05 | Q3 | After `systemctl reboot` the walks' wait for EmulationStation falls through after 45 tries without failing, and the walk runs anyway | `vm-qa:476-477` | tree |
| F-06 | Q2 | The walks' fixture seeding is unchecked: `reset` and `seed-content` go to `/dev/null` with no exit check, and `ensure_remote`'s return is ignored | `vm-qa:389`, `:397-398`, `:408`, `:341` | tree |
| F-07 | Q3 | `register` passes having checked less when the EmulationStation checkout is absent (its log says so) | `vm-qa:210-212` | tree |
| F-08 | Q3 | A failed screendump only warns, so a walk that captured no frame exits 0; `frame-diff` catches it only when a baseline exists | `vm-visual-qa:524-530` | tree |
| F-09 | Q1/Q2/Q5 | `vm-pair up` keeps the raw image and two qcow2 disks under `/tmp/rocknix-vm-pair` by default, on this host a 31 GB RAM tmpfs (about 6 GB per `up`); the key, sockets and pidfiles default to `/tmp` too | `vm-pair:37`, `:137-145`; `vm-qa:98-99` | tree; host `findmnt` |
| F-10 | Q2/Q6 | The QA cloud's state `~/.cache/rocknix-cloud-qa` is per user, so shared with the M7 lane, and the walks `reset` it; isolation exists (`CLOUD_QA_STATE`, `CLOUD_QA_PORT`) but nothing sets it | `vm-qa:397`; `cloud-test-backend:93` | the cycle used it |
| F-11 | Q1 | `es-syntax-check`'s default build root is the legacy `rocknix.worktrees` path, absent on the host (#640) | `es-syntax-check:53` | tree |
| F-12 | Q7 | `vm-qa --help` prints lines 5 to 38, cutting the descriptions of `link`, `ra-offline`, `walks` and `frame-diff` | `vm-qa:81` | tree |
| F-13 | Q7 | The index points six tools at `generic-x64-vm-testing.md`, which never names them (`png-blackout`, `vm-pair-test`, `signin-memory`, `es-launch-memory`, `ra-candidate-games`, `raofflineproxy-integration-test`); the three walk scripts have no index row | `instruction-files.md` on `next` | `q7-descriptions.txt` |
| F-14 | Q6 | Five tools nobody runs: `ra-candidate-games`, `es-launch-memory` and `signin-memory` have index mentions only; `font-stems` and `raofflineproxy-installed-native-test` have descriptive paragraphs only | `04` § Q6 | research, re-derived for the three |
| F-15 | Q6 | `vm-walks/cloud-epic/migration-protocol.sh` serves a retired migration and refuses on every current image | `:9-12`; `rasteratops-vm-cloud-epic:149` | P10 |
| F-16 | Q6 | Suites with no recorded catch of a product defect: `exit` (nothing at all), `wrapper` (none of its own), and `lifetime`, `pair-identity`, `time-to-play` and `ra-offline` (only their own failures) | `04` § Q6 | research, spot-checked |
| F-17 | Q5 | Cost concentrates: `walks` (16.7 min) and `scripts` (13.0 min) are about 90 % of a 33-minute default run; the default holds the pair (2 × 8 GiB) for the whole run while only `pair-identity` needs guest b | `vm-qa:119-122`, `:270` | P4 |
| F-18 | Q3 | All 391 claims are against `d72084ccad`'s baseline (2026-09-26), a month older than the newest image; three whole-frame claims exempt `manager-gb`'s first three screens while it stands | `claims.txt:38-40` | P5 |
| F-19 | Q5 | `frame-diff accept` keeps every previous baseline and nothing retires them (six kept, about 70 MB) | `frame-diff:399-403` | host `du` |
| F-20 | Q2 | `vm-upgrade-rehearsal` writes under `/workspace/artifacts` whatever `ROCKNIX_ARTIFACTS` says; `vm-qa` and `ra-offline-test` honour it | `vm-upgrade-rehearsal:30` | tree |

## Coverage

One row per path, at the hash. The Q columns answer plan § 4. `n/a` means the question does not apply to that kind of file. For a `.steps` file, Q2 counts its checked keys, Q5 its shots, Q6 who replays it, and Q7 whether a claim owns its frames.

| Path | Lines | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `tools/device-act` | 44 | log default under `/workspace/artifacts` | records boot id before and after | read only (D-QA-015) | bash | not run | rule instruction `engineering-practices.md:814-815` (on `next`) | index points to `engineering-practices.md` |
| `tools/emulator-exit-test` | 196 | none | `set -u`; checks fail closed on no answer | `--only` naming no part passes (P9) F-03 | bash | 28 s median (P4), 27 s on the cycle | called by `vm-qa` (`:296`); rule command; nothing recorded as a catch (`04` § Q6) | agree |
| `tools/es-launch-memory` | 166 | none | validates cycles and both bounds (`:39-42`) | none: bounds required for acceptance | host Python | 7.0 min for 50 cycles (research) | **nobody**: index only (F-16); caught #310 | the owning rule never names it F-13 |
| `tools/es-syntax-check` | 153 | default build root a legacy path (`:53`), absent F-11 | rc 2 without a root: not a pass (P2) | none | bash | seconds with a root | rule instruction (`es-native-ui.md`); blindspot 49 | index points to `es-native-ui.md` |
| `tools/es-untranslated` | 159 | ES_SRC default exists | rc 2 when it cannot read | none constructed | host Python | 0-1 s (P4) | `vm-qa` french (`:188`); caught #152 | the owning rule never names it (index points to `es-native-ui.md`) |
| `tools/font-stems` | 227 | none | host FreeType | not run | host Python | not recorded | **nobody** runs it: descriptive mention only (F-16); blindspot 54 | agree |
| `tools/frame-diff` | 433 | none | missing claims or masks read as empty (strict) | no baseline rc 2 (vm-qa SKIP); MISSING and size change FAIL; three whole-frame claims F-19 | host Python stdlib | 1-2 s per compare (P4); `accept` keeps every old baseline, 6 kept (~70 MB) F-20 | called by `vm-qa` (`:525`); `release-candidates.md` step 3; 5 FAIL rows in the record (`04` § Q6) | agree |
| `tools/png-blackout` | 81 | none | refuses unsupported PNGs | none | host Python stdlib | not recorded | `developer-relations/SKILL.md:175`; `vm-walks/docs/README.md:20` | the owning rule never names it F-13 |
| `tools/qa-accounts` | 159 | `~/.ROCKNIX/qa-accounts` | prints no value (read, never run) | read only | bash | not run | `ra-offline-test:259`; D-QA-016 | agree |
| `tools/ra-candidate-games` | 223 | none | read-only | not run | host Python | not recorded | **nobody**: index only (F-16) | the owning rule never names it; the index points there F-13 |
| `tools/ra-offline-test` | 524 | defaults under `/tmp` (`:65-66`); host `/tmp/ra-offline-acct.$$` (`:259`), `.steps` (`:345`) | `FAILS` with cleanup (`:287` ...) | preconditions FAIL when missing; not run here (opt-in, spends an achievement) | bash | 5.7 min and about 4 min standalone (research); never in a `vm-qa` report | opt-in in `vm-qa` (`:358`); `release-candidates.md` step 3; blindspot 50 | agree |
| `tools/ra-ui-test` | 225 | none | asserts as checks (F-04 class) | fixture-only; not run | host Python | 7.7-8.6 min, 4 runs (research) | rule mention only; #465 | agree |
| `tools/raofflineproxy-consent-test` | 230 | none | asserts as checks (F-04 class) | not run | host Python | 0.8 min with a guest boot (research) | caught #457 (`04` § Q6) | agree |
| `tools/raofflineproxy-installed-native-test` | 70 | none | refuses any skip (`:59-69`) | not run | host Python | not recorded | **nobody** runs it: a descriptive rule paragraph only (F-16) | agree |
| `tools/raofflineproxy-integration-test` | 247 | none | `unittest` result | needs an unpacked proxy; not run | host Python | 0.3 min (research) | `release-candidates.md` proxy proof; #361 | the owning rule never names it F-13 |
| `tools/signin-memory` | 129 | reads `/tmp/signin-memory.*` on the guest only | exits 1 on each FAIL (`:120-125`) | none constructed | host Python | 1.4-1.5 min standalone (research) | **nobody**: index only (F-16); decided D-WORKFLOW-038 | the owning rule never names it F-13 |
| `tools/time-to-play` | 1593 | host `/tmp/ttp-cm-<pid>` control socket (`:158`) | `headline_missing`, `over_budget` (`:1268-1283`) | `--repeat 0` or an `--only` with no headline cell passes measuring nothing (P8) F-02 | host Python | 69 s median as a suite (P4), 72 s on the cycle | called by `vm-qa` (`:342`); `time-to-play.md`; blindspots 39, 54, 55, 56, 74 | agree |
| `tools/vm-manager-system-check` | 19 | none | `assert` as the check (`:12-15`) F-04 | passes under `PYTHONOPTIMIZE=1` (P6) F-04; no `--help` (rc 1, fail closed) | host Python | milliseconds | called by `vm-qa` (`:483`) for manager walks | agree |
| `tools/vm-pair` | 185 | `DIR` default `/tmp/rocknix-vm-pair` (`:37`), a RAM tmpfs here F-09 | `set -euo pipefail`; PID verified against its disk (`:81-95`) | stop by `vm-stop` (pidfile, disk) (`:124-130`): no pattern; P3 | QEMU 10.2.1 host, `qemu-img` | two 8 GiB guests and about 6 GB of `/tmp` per `up` (P4, P11) F-09 | called by `vm-qa` (`:120-121`), `vm-upgrade-rehearsal`; `vm-pair-test` its control; recorded in blindspot 41 | header matches the code |
| `tools/vm-pair-test` | 75 | none | asserts as checks (F-04 class) | controlled launch failures, 9 cases (P2) | host Python | seconds, host only | **fork CI** `fork-checks.yml:47` | the owning rule never names it; the index points there F-13 |
| `tools/vm-qa` | 541 | host `/tmp` defaults for key, sockets, pidfiles (`:98-99`); ES_SRC default exists at the pin | `set -u`, no `pipefail`; fixture seeding unchecked (`:389`, `:397-398`, `:408`) F-06 | exits 0 over a SKIP (`:541`) F-01, P7; walks wait falls through (`:477`) F-05; `register` checks less without ES (`:210-212`) F-07 | bash only | one default run: median 33 min, the pair held throughout (P4) F-18 | callers: rules (`release-candidates.md` step 3, `generic-x64-vm-testing.md`); no CI; value per suite in `04` § Q6 | `--help` prints `:5-38` only, cutting four suites F-12; header list equals `SUITES` |
| `tools/vm-serial` | 133 | none | socket client; rc 2 on a bad call | `wait --up-to` bounded | host Python | 15 s to serial on the cycle | called by `vm-pair` (`:108`, `:110`, `:181`), `ra-offline-test:116`, `cloud-round-trip:240`; rule command `generic-x64-vm-testing.md:112-114` | agree |
| `tools/vm-stop` | 77 | none | pidfd, identity re-check, bounded wait; fail closed | timeout keeps the pidfile, rc 1, no escalation: loud; none constructed | Python 3.14 host (`pidfd_open` 3.9+) | 0.25 s on the cycle (P11) | called by `vm-pair` (`:129`); control `vm-stop-test` 7 PASS (P2) | three descriptions agree |
| `tools/vm-stop-test` | 66 | none | asserts as checks (F-04 class) | constructs delayed exit, timeout, wrong disk, wrong process | host Python | seconds, host only | not in CI; rule names it (`generic-x64-vm-testing.md`) | agree |
| `tools/vm-upgrade-readiness-test` | 87 | none | asserts as checks (F-04 class) | synthetic states, 7 cases (P2) | host Python | seconds, host only | **fork CI** `fork-checks.yml:48`; called by `last-good-scripts-test` | agree |
| `tools/vm-upgrade-rehearsal` | 170 | none | `RESULT PASS|FAIL`, exits `$fail` | fail closed on each piece | bash | 96-159 s, 19 runs (research) | `release-candidates.md` step 3; `upgrade-and-install.md` | output root ignores `ROCKNIX_ARTIFACTS` (`:30`) F-21 |
| `tools/vm-visual-qa` | 677 | none | a failed screendump only warns (`:524-530`) F-08 | eaten key: re-send then exit 3 (`:587-671`); frames missing pass F-08 | host Python stdlib | the walks suite median 1,000 s (P4) | called by `vm-qa` walks (`:498`), `ra-offline-test:346`, `es-launch-memory` | agree |
| `tools/vm-walks/README.md` | 194 | `/tmp` monitor path in its example | n/a | n/a | n/a | n/a | read by people | describes `settle` and `wait-for-change` as the code does |
| `tools/vm-walks/back-up-page.steps` | 8 | n/a | 1 keys, 1 `wait-for-change` | every key is checked (P5) | n/a | 1 shot(s) | replayed by `vm-qa` walks: `back-up-page`, `continue-to-systems`, `run-transfer`, `run-transfer-frames`, `tick-game-content`, `tick-roms`, `tick-settings` | claims via its walks (P5) |
| `tools/vm-walks/claims.txt` | 564 | n/a | n/a | 391 claims, all against `d72084ccad`; three whole-frame (`:38-40`) F-19 | n/a | n/a | read by `frame-diff` (`vm-qa:525`); every claim matches a walk (P5) | n/a |
| `tools/vm-walks/cloud-epic/migration-protocol.sh` | 165 | needs `cloud_migrate_layout`, absent from the image (P10) | refuses rc 2 before any write (`:9-12`) | refuses on every current image | n/a | not reached | sourced by `rasteratops-vm-cloud-epic:149` only; dead on current images F-15 | no index row |
| `tools/vm-walks/cloud-epic/vnc-grab.py` | 83 | none | stdlib RFB | n/a | host Python | not recorded | `rasteratops-vm-cloud-epic:67` | no index row |
| `tools/vm-walks/confirm-cloud-folder.steps` | 13 | n/a | 2 keys, 2 `wait-for-change` | every key is checked (P5) | n/a | 2 shot(s) | replayed by `vm-qa` walks: `confirm-cloud-folder` | claims via its walks (P5) |
| `tools/vm-walks/continue-to-systems.steps` | 21 | n/a | 6 keys, 6 `wait-for-change` | every key is checked (P5) | n/a | 2 shot(s) | replayed by `vm-qa` walks: `continue-to-systems`, `run-transfer`, `run-transfer-frames` | claims via its walks (P5) |
| `tools/vm-walks/docs/README.md` | 22 | n/a | n/a | n/a | n/a | n/a | read by people (#323) | agrees with the four `docs/*.steps` |
| `tools/vm-walks/docs/cloud-sync.steps` | 84 | n/a | 28 keys, 28 `wait-for-change` | every key is checked (P5) | n/a | 4 shot(s) | replayed by hand for rocknix.org (#323); no `vm-qa` caller | no claim (not a suite walk) |
| `tools/vm-walks/docs/main-menu-up-probe.steps` | 22 | n/a | 5 keys, 5 `wait-for-change` | every key is checked (P5) | n/a | 6 shot(s) | replayed by hand for rocknix.org (#323); no `vm-qa` caller | no claim (not a suite walk) |
| `tools/vm-walks/docs/networking.steps` | 79 | n/a | 22 keys, 22 `wait-for-change` | every key is checked (P5) | n/a | 5 shot(s) | replayed by hand for rocknix.org (#323); no `vm-qa` caller | no claim (not a suite walk) |
| `tools/vm-walks/docs/retro-achievements.steps` | 69 | n/a | 22 keys, 22 `wait-for-change` | every key is checked (P5) | n/a | 2 shot(s) | replayed by hand for rocknix.org (#323); no `vm-qa` caller | no claim (not a suite walk) |
| `tools/vm-walks/fixtures/arcade-vertical-raw-left.png` | 8 | n/a | n/a | n/a | n/a | n/a | copied by `vm-qa` (`:382`, `:385`); the #288 session control | n/a |
| `tools/vm-walks/fixtures/gb-160x144.png` | 3 | n/a | n/a | n/a | n/a | n/a | copied by `vm-qa` (`:381`, `:384`) for the manager walks; #243 | n/a |
| `tools/vm-walks/fixtures/nes-256x240-right.png` | 12 | n/a | n/a | n/a | n/a | n/a | copied by `vm-qa` (`:380`, `:383`); the #288 session control | n/a |
| `tools/vm-walks/fixtures/system-selected.sh` | 3 | none | writes one guest file | n/a | n/a | milliseconds | installed by `vm-qa` (`:473`) for manager walks | no index row (fixture) |
| `tools/vm-walks/m7-cloud-sync.steps` | 52 | n/a | 17 keys, 17 `wait-for-change` | every key is checked (P5) | n/a | 6 shot(s) | replayed by hand (M7); no `suite.txt` walk | no claim (not a suite walk) |
| `tools/vm-walks/m7-retro-achievements.steps` | 36 | n/a | 11 keys, 11 `wait-for-change` | every key is checked (P5) | n/a | 4 shot(s) | replayed by hand (M7); no `suite.txt` walk | no claim (not a suite walk) |
| `tools/vm-walks/manager.steps` | 33 | n/a | 6 keys, 6 `wait-for-change` | every key is checked (P5) | n/a | 5 shot(s) | replayed by `vm-qa` walks: `manager-fbn`, `manager-gb`, `manager-nes` | claims via its walks (P5) |
| `tools/vm-walks/masks.txt` | 12 | n/a | n/a | 7 masks, each explained | n/a | n/a | read by `frame-diff` | n/a |
| `tools/vm-walks/match-dialog.steps` | 26 | n/a | 4 keys, 4 `wait-for-change` | every key is checked (P5) | n/a | 3 shot(s) | replayed by `vm-qa` walks: `match-dialog` | claims via its walks (P5) |
| `tools/vm-walks/reset.steps` | 18 | n/a | 0 keys, 0 `wait-for-change` | every key is checked (P5) | n/a | 0 shot(s) | a utility leg; no `suite.txt` walk | no claim (not a suite walk) |
| `tools/vm-walks/restore-page.steps` | 12 | n/a | 2 keys, 2 `wait-for-change` | every key is checked (P5) | n/a | 1 shot(s) | replayed by `vm-qa` walks: `restore-page` | claims via its walks (P5) |
| `tools/vm-walks/run-transfer-frames.steps` | 60 | n/a | 6 keys, 6 `wait-for-change` | every key is checked (P5) | n/a | 17 shot(s) | replayed by `vm-qa` walks: `run-transfer-frames` | claims via its walks (P5) |
| `tools/vm-walks/run-transfer.steps` | 58 | n/a | 6 keys, 6 `wait-for-change` | every key is checked (P5) | n/a | 3 shot(s) | replayed by `vm-qa` walks: `run-transfer` | claims via its walks (P5) |
| `tools/vm-walks/suite.txt` | 100 | n/a | n/a | 16 walks (brief: 17) and `default-pre` | n/a | n/a | read by `vm-qa` walks (`:437`) | comments match the compositions |
| `tools/vm-walks/tick-game-content.steps` | 15 | n/a | 5 keys, 5 `wait-for-change` | every key is checked (P5) | n/a | 1 shot(s) | replayed by `vm-qa` walks: `tick-game-content` | claims via its walks (P5) |
| `tools/vm-walks/tick-roms.steps` | 16 | n/a | 3 keys, 3 `wait-for-change` | every key is checked (P5) | n/a | 1 shot(s) | replayed by `vm-qa` walks: `continue-to-systems`, `run-transfer`, `run-transfer-frames`, `tick-roms` | claims via its walks (P5) |
| `tools/vm-walks/tick-settings.steps` | 21 | n/a | 7 keys, 7 `wait-for-change` | every key is checked (P5) | n/a | 1 shot(s) | replayed by `vm-qa` walks: `tick-settings` | claims via its walks (P5) |
| `tools/vm-walks/to-change-cloud-folder.steps` | 39 | n/a | 9 keys, 9 `wait-for-change` | every key is checked (P5) | n/a | 2 shot(s) | replayed by `vm-qa` walks: `confirm-cloud-folder`, `to-change-cloud-folder` | claims via its walks (P5) |
| `tools/vm-walks/to-manage-cloud-storage.steps` | 28 | n/a | 6 keys, 6 `wait-for-change` | every key is checked (P5) | n/a | 1 shot(s) | replayed by `vm-qa` walks: `back-up-page`, `confirm-cloud-folder`, `continue-to-systems`, `match-dialog`, `restore-page`, `run-transfer`, `run-transfer-frames`, `tick-game-content`, `tick-roms`, `tick-settings`, `to-change-cloud-folder`, `to-manage-cloud-storage` | claims via its walks (P5) |
| `tools/vm-walks/ui-settings-toggle.steps` | 41 | n/a | 7 keys, 7 `wait-for-change` | every key is checked (P5) | n/a | 2 shot(s) | replayed by `vm-qa` walks: `ui-settings-toggle` | claims via its walks (P5) |
| `tools/vm-walks/wake.steps` | 7 | n/a | 0 keys, 0 `wait-for-change` | every key is checked (P5) | n/a | 0 shot(s) | a utility leg; no `suite.txt` walk | no claim (not a suite walk) |

## 03-retrospective.md (whole)

# Retrospective — M6.P2 T12, the VM harness (#659)

Phase 3, read from the history of the 60 at `8ebaf8daad` and from the record (`02` § The record). The four questions of the retro are stage G's; this file is the audit's look back at how the harness came to be what it is.

## 3.1 What the history shows

- **The commits:** 144 non-merge commits since `c445081a59`: 1 in August, 106 in September and 37 in October.
  - **The first** is `1a5368ec62` (2026-08-18, `tools: add scripted visual QA for the GENERIC_X64 VM`).
  - **The most touched** are `vm-qa` (39 commits), `vm-walks/claims.txt` (15), `vm-walks/README.md` (14), `time-to-play` (14), `vm-upgrade-rehearsal` (12), `ra-offline-test` (11) and `vm-pair` (9).
- **The harness grew one guard per failure it met,** and each guard's comment names its failure:
  - #125: the fixed waits that derailed walks became `settle` and `wait-for-change`;
  - blindspot 39: a PASS over dashes became `headline_missing`;
  - blindspot 40: `$SSHO` inherited from a shell;
  - #252: a visual change nobody meant, which became `frame-diff`;
  - #454: a stop that did not wait, which became `vm-stop`;
  - #545: a launch failure read as up, which became `vm-pair-test`.
- **The record runs from 2026-10-03 to 10-15 in `docs/qa-logs/`.** Its 59 distinct `vm-qa` runs are mostly the M7 replacement rounds. The September runs are rows in `docs/vm-qa-log.md` (44 run windows).

## 3.2 What worked

- **The guards fail closed where they were built after a failure.** `vm-stop` uses a pidfd with an identity re-check; `vm-pair` checks that the started PID owns its disk; `frame-diff` treats a MISSING frame or a size change as a FAIL; `signin-memory` FAILs without the load-finished line; `es-launch-memory` validates its cycles and bounds; `raofflineproxy-installed-native-test` refuses any skip.
- **No guest is found or stopped by pattern** (P3). The one stopping path is the pidfile and the owned disk.
- **Every walk checks every key press** (P5): 22 of 22 step files pair each `key` with a `wait-for-change`.
- **The claims contract holds together** (P5): no orphan claim, and no walk without a claim.
- **The cycle's numbers match the record's** (`02` § The guest cycle). The harness is stable in cost on today's image.

## 3.3 What was hard, as the code shows it

- **A runner whose exit and whose report disagree.** The report says `has not passed` beside a SKIP, and the exit says 0 (F-01). The comment at `vm-qa:141` (`a suite that could not run (rc 3) is shown as such, never folded into PASS`) is true of the table and not of the exit code.
- **Arguments that empty a measurement.** `time-to-play --repeat 0` and `emulator-exit-test --only X` each run nothing and pass (F-02, F-03). The guards judge what ran, and nothing judges whether anything ran.
- **Host state in `/tmp` and in the user's cache.** It was written when one session used the host. Today two lanes share it, and `/tmp` is a RAM tmpfs that ran out of inodes on 2026-10-24 (F-09, F-10).
- **A month-old baseline.** All 391 claims name `d72084ccad`'s cut (F-18). `frame-diff` has nothing to compare against for a newer cut until a maintainer accepts one.

## 3.4 What the slice inherits from earlier lanes

- **T9's D-INFRA-028:** `build-preflight` lists guests and names `vm-stop`. The harness's own stop path agrees with it (P3).
- **T1:** the exit hotkey `emulator-exit-test` drives. T1's retained `t1.qcow2` and its `ttp-*` runs sit under `/workspace/artifacts/m6-t1-20261023/`; that is a retention observation for the coordinator.
- **The legacy layout (#640):** `es-syntax-check:53`.

## 3.5 The seams

| Seam | What crosses it | What the read found |
| --- | --- | --- |
| `vm-qa` × the cloud suites × the image | `cloud-test-backend up`, `reset`, `seed-content`, `seed-device`; `cloud-round-trip` | The backend's state is per user and so shared across lanes (F-10). Seeding is unchecked (F-06). The round trip passed on the cycle in 84 s. |
| `frame-diff` × `claims.txt` × the walks × the menu map | the walk frames, 391 claims, 7 masks; `menumap` reads the ES pin | The reconciliation is clean (P5). All claims sit on one month-old baseline, with three whole-frame claims (F-18). `menumap` caught #542 (`04` § Q6). |
| `time-to-play` × the exit sync's budget (D-CLOUD-119) | `over_budget` against 3 s, on the median of the exit cell | The budget holds on the cycle (1.59 s). An empty cell is never judged (F-02). |
| the pair × the host's memory (`device-builds.md`) | 2 × 8 GiB allocated, about 6 GB of disks in the `/tmp` tmpfs | A booted guest holds 2.54 GiB resident (P11), near `device-builds.md`'s "about 2 GB". The pair's disks in RAM-backed `/tmp` are unbudgeted (F-09). |
| the harness × the M7 lane's guests (the host file) | ports 10022 to 10026, VNC :9 and :10, the default socket and pidfile names under `/tmp`, the QA cloud | Two lanes collide on the defaults. The cycle avoided them only by setting `VM_PAIR_DIR`, `VM_QEMU_RUNTIME_DIR`, `ROCKNIX_ARTIFACTS`, `CLOUD_QA_STATE` and `CLOUD_QA_PORT` by hand (F-09, F-10). |

## 04-analysis.md (whole)

# Analysis — M6.P2 T12, the VM harness (#659)

## Executive summary

The harness is the fork's bench for every behaviour proof (`vm-first.md`). Read through the lens of cost against value, it is sound where it was rebuilt after a failure, and it is open where nothing has failed yet.

- **What is sound:**
  - No guest is found or stopped by pattern (P3). `vm-stop` is pidfd-exact, and the claims contract holds together (P5). Every walk checks every key press.
  - On today's image the guest suites cost what the record says (`02` § The guest cycle).
- **What is open:**
  - **Three tools can pass while proving nothing,** each shown on the guest (F-01, F-02, F-03).
  - **A default run's state assumes one user on the host:** the pair's disks in RAM-backed `/tmp`, and the QA cloud's state in the user's cache, which the walks reset (F-09, F-10).
  - **The cost concentrates in two suites:** `walks` and `scripts` are about 90 % of a 33-minute run (F-17).
  - **The value side shows:**
    - one suite, `exit`, with nothing recorded at all;
    - five more whose recorded failures were all the harness's own (F-16);
    - five tools nobody runs (F-14);
    - one fixture script for a retired migration (F-15).

The coordinator ruled at 19:33 on #659 that F-01, F-02 and F-03 are stage-D bugs, and that F-10 is a Q2/Q6 row.

## Acceptance-criteria scorecard

#659's 17 criteria, at stage B. The detail is in `02` § Phase 2.

| Met at stage B | Pending |
| --- | --- |
| 6 (`01` § Scope), 7 (coverage, 60), 8 (the controls), 9 (the guest cycle), 10 (nothing never-run), 11 (Q5 below), 12 (Q6 below), 13 (Q3 below), 14 (Q7 below), 15 (11 class cells = 11 PROOF lines) | 1 to 5 and 16 to 17: stages C to H |

## Code Quality Assessment

### Strengths

- **The guards name their own failure.** Each comment near a guard says what failed before it existed: #125, blindspots 39 and 40, #252, #454, #545.
- **The stop path is exact:** `vm-stop` uses a pidfd, re-checks identity, and keeps the pidfile when it times out.
- **Measurement tools refuse what they cannot read:** `signin-memory`, `es-launch-memory`'s bounds, and `raofflineproxy-installed-native-test`'s no-skips rule.

### Concerns

- **Pass-without-proving through arguments, and through the exit code** (F-01 to F-03). Each tool judges what ran and does not check that anything ran.
- **`assert` as a check** in seven tools (F-04).
- **Host defaults from a one-session host:** `/tmp` roots, a per-user QA cloud and fixed ports (F-09, F-10).

### Complexity Hotspots

- **`vm-qa`:** 541 lines, 17 suites and four fixture builders in one bash file. Its fixture seeding is unchecked (F-06).
- **`time-to-play`:** 1,593 lines, the slice's largest file. Its headline rule is sound for every cell that ran (F-02).

## Risk Assessment

| Risk | Shape | Today |
| --- | --- | --- |
| A green run that did not pass | F-01 (a SKIP), F-02, F-03 (an empty measurement) | Each is reached only through a SKIP or a hand-typed argument; the default `vm-qa` run is not affected except by F-01 |
| Two lanes on one host | the shared QA cloud state (F-10), `/tmp` sockets, pidfiles and ports (F-09) | Avoided on this cycle by five environment variables set by hand |
| Host memory under a build | the pair's disks in a RAM tmpfs (F-09) | About 6 GB per `up`, beside 2 × 8 GiB guests; a booted guest holds 2.54 GiB resident (P11) |
| A baseline nobody moves | F-18 | All 391 claims are against the 2026-09-26 cut |

## Coverage Boundary

- **Read:** the 60, line by line for `vm-qa`, `vm-pair`, `vm-stop`, `frame-diff` and `emulator-exit-test`. The rest are read for their exit and pass logic, their find/stop paths and their `/tmp` and legacy paths (`02` § Mechanical checks).
- **Run:** the three no-guest controls; one guest cycle (`vm-qa` with five suites and two argument probes); one host probe (P6).
- **Not run:**
  - `walks` (16.7 min, and the record holds 23 runs);
  - `pair-identity` (needs the pair);
  - `link` and `ra-offline` (opt-in; brief § 8);
  - `ra-offline-test`, `ra-ui-test`, the three `raofflineproxy-*` tests, `signin-memory`, `es-launch-memory`, `vm-upgrade-rehearsal`, `font-stems` and `ra-candidate-games`. Their costs come from the record, through the research helper.
  - `device-act` and `qa-accounts` are read only.
- **The record:** the 61 `vm-qa` reports under `docs/qa-logs/` (2026-10-03 to 10-15). The September runs are kept only as `docs/vm-qa-log.md` rows; their full reports are under `/workspace/artifacts`, which was not read.

## Finding Verification (Phase 4.5)

Each finding was re-read against its artifact, looking for the reading that would refute it.

| ID | The refutation tried | Verdict |
| --- | --- | --- |
| F-01 | Is exit 0 over a SKIP intended? The header promises `exits non-zero if any suite failed -- so a nightly can tell`. A SKIP is "not passed" in the report's own words (`:528`) and passed in its exit (`:541`). | Stands (P7). Whether a SKIP should fail the exit is the coordinator's contract question; that it reads as a pass is the bug. |
| F-02 | Does `--quick` make it unreachable? Yes, for `vm-qa`'s call (`:1017-1019`). A hand run is the documented form for proposing a register number (`vm-qa:332-333`), and that is where it is reached. | Stands, Low (P8) |
| F-03 | Same question; `vm-qa` passes the default `ABCD` | Stands, Low (P9) |
| F-04 | Does anyone run with `-O`? Nothing in the tree, nor in this host's environment. | Stands as a latent fail-open (P6), Low |
| F-05 | Does the walk's first `wake` / `dismiss-dialogs` fail on an absent EmulationStation? `settle` never fails (`vm-visual-qa:350-367`), and a framebuffer still exists, so it does not. `frame-diff` would catch it with a baseline. | Stands, Low |
| F-06 | Does a failed seed show elsewhere? The walks' frames would differ, which `frame-diff` catches only with a baseline; `time-to-play` refuses an unreachable remote (`:1324-1326`). | Stands, Low |
| F-07 | Its log says the register was checked without the interface's citations, and the report does not | Stands, Low |
| F-08 | `frame-diff` reports a MISSING frame as a FAIL when a baseline exists | Stands, Low, joined to F-01's SKIP |
| F-09 | Is `/tmp` a RAM tmpfs here? `findmnt`: `tmpfs 30.4G`. `vm-pair` documents the default and its override (`:28-32`). | Stands, Medium for the host's memory |
| F-10 | Does `vm-qa` set `CLOUD_QA_STATE`? No. The default is `${XDG_CACHE_HOME:-~/.cache}/rocknix-cloud-qa`, per user. | Stands |
| F-11 | Is the root absent? `ls` says so | Stands, #640 |
| F-12 | `sed -n '5,38p'` against the header's length | Stands, Low |
| F-13 | Re-derived against `next` (`q7-descriptions.txt`) | Stands, a rule drift: a lead |
| F-14 | Re-derived for three; the helper confirmed the other two | Stands, Renovation |
| F-15 | The guest: `cloud_migrate_layout` absent (P10) | Stands, Renovation |
| F-16 | Spot-checked three catches; the "nothing recorded" rows rest on the helper's search of the work logs, `docs/qa-logs` and the registers | Stands as recorded, Renovation |
| F-17 | Re-derived medians (P4) | Stands, Renovation |
| F-18 | `BASELINE.txt` and `claims.txt`'s heads | Stands, Low |
| F-19 | `du` on the host | Stands, Low |
| F-20 | `vm-upgrade-rehearsal:30` | Stands, Low |

**Withdrawn at Phase 4.5:** L2 (that `vm-qa` folds a real failure into a SKIP). Rc 3 is a deliberate skip in `last-good-scripts-test` and in the `frame-diff` suite, and `retroarch-wrapper-test`'s binary returns 0 or 1.

## Renovation face

### Q1 Modernize

| Row | Where | Reading |
| --- | --- | --- |
| Legacy build root | `es-syntax-check:53` | `/workspace/repos/rocknix.worktrees/generic-x64/build.ROCKNIX-GENERIC_X64.x86_64`, absent; rc 2 (F-11, #640) |
| Host `/tmp` roots | `vm-pair:37`, `:41`; `vm-qa:98-99`; `time-to-play:158`; `ra-offline-test:65-66`, `:259`, `:345` | They predate the inode exhaustion of 2026-10-24 and two lanes sharing one host (F-09) |
| `ES_SRC` default | `vm-qa:167` and five more | `~/Development/emulationstation-next.worktrees/qa-integration`, present at the pin `16dbac521`; a per-user path, not the canonical layout (#640's question) |
| Retired mechanism | `vm-walks/cloud-epic/migration-protocol.sh:9-12` | `cloud_migrate_layout` (D-CLOUD-175) (F-15) |
| QEMU and Python | the host | QEMU 10.2.1, Python 3.14.4. `pidfd_open`, `int.to_bytes`, f-strings and stdlib PNG all work (Q4) |

### Q2 Standards and best practices

| Row | Where | Reading |
| --- | --- | --- |
| Find/stop | the eight tools | pidfile and owned disk; no pattern (P3) |
| `assert` as a check | 7 tools | F-04 |
| Unchecked seeding | `vm-qa:389`, `:397-398`, `:408`, `:341` | F-06 |
| Shared state | `vm-qa:397`; `cloud-test-backend:93` | F-10 |
| An override honoured by some | `vm-upgrade-rehearsal:30` | F-20 |
| `pipefail` | `vm-qa` uses `set -u` only; `vm-pair` uses `set -euo pipefail` | `vm-qa`'s pipelines are not gating except `walk_all`'s `\| timeout … vm-visual-qa`, whose exit is the last command's, the one wanted |
| Credentials | `qa-accounts`, `ra-offline-test:263` | the account is masked (`sed "s/${ACCOUNT}/<account>/g"`); `qa-accounts` prints no value. Read, not run. |

### Q3 Bugs

**The pass-without-proving hunt, suite by suite.** A constructed input is named where one passes wrongly. "None" means the lane found none.

| Suite or tool | Line read | Constructed input that passes wrongly |
| --- | --- | --- |
| `vm-qa` (the runner) | `:141-148`, `:541` | any SKIP: `frame-diff` with no baseline, run on the guest: rc 0 (P7, F-01) |
| scripts | `last-good-scripts-test` tail | skipped checks: exit 3, then SKIP, then F-01 |
| lifetime | `vm-qa:166-175` | none: a missing checkout is rc 1 |
| wrapper | `retroarch-wrapper-test:216-226` | none: rc 2 with no source; the binary is 0 or 1 |
| vocabulary, french, quoting, menumap | `vm-qa:186-196` | none found; each fails on an absent checkout or a missing file (`es-untranslated` rc 2) |
| register | `vm-qa:205-215` | an absent ES checkout: checks less and passes (F-07) |
| pair-identity | `vm-qa:222-269` | none: every field asserted non-empty first; no mDNS line is a FAIL |
| fresh | `vm-qa:278-293` | none: the link targets are compared exactly; an unanswered SSH gives an empty target, which is a FAIL |
| round-trip | `vm-qa:295` → `cloud-round-trip` | none in the call (no `--only`); the tool is another slice's |
| exit | `emulator-exit-test:145-196` | `--only X`, run on the guest: `PASSED` rc 0 (P9, F-03); `vm-qa` passes `ABCD` |
| time-to-play | `time-to-play:994-1019`, `:1306-1332` | `--repeat 0`, run on the guest: rc 0 with empty cells (P8, F-02); `vm-qa` passes `--quick` |
| link | `vm-qa:349` | not run; its stamp parser was the harness's own failure (#398, recorded) |
| ra-offline | `vm-qa:358`; `ra-offline-test` | not run; a stale `exec.log` false PASS is blindspot 50, already fixed |
| walks | `vm-qa:426-513`; `vm-visual-qa:524-530` | an EmulationStation that never returns after the reboot (F-05); a monitor whose screendump fails (F-08); both leave rc 0 and are caught by `frame-diff` only with a baseline |
| frame-diff | `frame-diff:264-353` | none while a baseline exists; three whole-frame claims make three screens uncomparable (F-18) |
| `vm-manager-system-check` | `:12-15` | `PYTHONOPTIMIZE=1` (P6, F-04) |
| `es-launch-memory` | `:39-42`, `:157-161` | none: bounds required for acceptance |
| `signin-memory` | `:108-125` | none |
| `vm-upgrade-rehearsal` | `:35-51`, `:168-170` | none found |

**Every tool that touches a QEMU, classified:**

| Tool | Finds | Waits | Stops | Class |
| --- | --- | --- | --- | --- |
| `vm-pair` | its pidfile, checked against its disk (`:78-95`) | `vm-serial wait --up-to 300`, then SSH 100 tries | `vm-stop` pidfile + disk (`:129`) | pidfile-and-disk |
| `vm-stop` | pidfile; identity re-check | pidfd poll, 20 s | pidfd SIGTERM | pidfile-and-disk |
| `vm-qa` | reads `$RUNTIME/rocknix-qemu.pid` for the display line only (`:137-138`) | SSH 40 tries | never (`vm-pair down` when not `--skip-up`) | pidfile-and-disk |
| `time-to-play`, `ra-offline-test`, `emulator-exit-test`, `es-launch-memory`, `signin-memory` | none: SSH, serial or monitor to a running guest | their own bounded loops | none host-side | n/a (guest-side only) |
| `vm-upgrade-rehearsal` | through `vm-pair` | through `vm-pair` | through `vm-pair down` | pidfile-and-disk |

### Q4 Package currency

Not a package slice. The tools assume QEMU's monitor and `pidfd` (Python 3.9 or later), and the host has QEMU 10.2.1 and Python 3.14.4. The image the record ran on was mostly the M7 replacements, 2026-10-03 to 10-15. The newest image present is `069fc2704421` (2026-10-22), on which the cycle ran.

### Q5 Efficiency

**The cost table.** Minutes are medians from the 59 distinct reports (P4), with the cycle's figure where it ran. "Host" is what the suite holds while it runs. "Cadence" is from `vm-qa:64` and `release-candidates.md` step 3.

| Suite or measurement | Minutes (median / max) | Host it holds | Cadence |
| --- | --- | --- | --- |
| scripts | 13.0 / 15.1 | host only (busybox shims, bubblewrap) | every candidate |
| lifetime | 0.02 | host only, ES checkout | every candidate |
| wrapper | 0.0 | host only, a RetroArch source in a build root | every candidate |
| vocabulary | 0.0 | host only | every candidate |
| register | 0.03 | host only | every candidate (also the fork CI and the pre-push gate) |
| french | 0.0 | host only | every candidate |
| quoting | 0.0 | host only | every candidate |
| menumap | 0.0 | host only | every candidate |
| pair-identity | 0.02 | both guests | every candidate |
| fresh | 0.0 (cycle: 1 s) | guest a | every candidate |
| round-trip | 1.41 / 2.0 (cycle: 84 s) | guest a + the QA cloud | every candidate |
| exit | 0.47 / 0.48 (cycle: 27 s) | guest a | every candidate |
| time-to-play | 1.15 / 1.42 (cycle: 72 s) | guest a + the QA cloud | every candidate |
| link | 7.95 / 9.0 | guest a, serial, the QA cloud | opt-in (11 runs) |
| ra-offline | none in any report; standalone 4 to 5.7 | guest d, serial, the QA account | opt-in (0 runs in `vm-qa`) |
| walks | 16.7 / 17.2 | guest a, 16 reboots | every candidate |
| frame-diff | 0.02 | host only, the baseline (12 MB) | every candidate (SKIP without a baseline) |
| **a default run** | **33 (28 to 35)**, 19 full runs | **the pair (2 × 8 GiB, 8 vCPU) the whole run**, about 6 GB of `/tmp` disks | every candidate |
| `time-to-play` (standalone, `--repeat 5`) | no recorded run | one guest | by hand, for a register row |
| `signin-memory` | 1.4 to 1.5 | one guest (1 GiB form) | webkitgtk bumps |
| `es-launch-memory` | 7.0 for 50 cycles; 9.3 to 17.8 in combined jobs | one guest | no rule schedules it |
| `vm-upgrade-rehearsal` | about 1.9 (96 to 159 s), 19 runs | both guests | every candidate (step 3) |
| `ra-ui-test` | 7.7 to 8.6, 4 runs | one guest | proxy UI changes |
| `raofflineproxy-integration-test` | 0.3 | host only | proxy refreshes |
| `raofflineproxy-consent-test` | 0.8 | one isolated guest | proxy refreshes |

**What it says:**
- `walks` and `scripts` are about 30 of a default run's 33 minutes (F-17).
- The pair is held for the whole run, while one 1-second suite, `pair-identity`, needs guest b (F-17).
- Nine suites take under 3 seconds each.
- The record holds no full-cell `time-to-play` run.

### Q6 Dead ends

**The value table.** The source for every row is `/workspace/tmp/m6-t12/research-q6.md` (with path:line), spot-checked by the lane (`00`). "Catch" means a product or record defect the item found. "Positive" means a constructed failure it was seen to fail on. "Callers" means who runs it: `vm-qa`, the CI, a rule's instruction or a skill. `nobody` means none of those.

**Suites:**

| Suite | Last recorded catch | Recorded positive | Callers |
| --- | --- | --- | --- |
| scripts | #414, 2026-10-04 (a stale schema pin) | its sections' failing-copy cases; blindspots 60 and 61 | `vm-qa`; rules |
| lifetime | **nothing recorded** (its FAILs were its own test double, 2026-10-11) | the ASan pre-fix run, 2026-09-06 | `vm-qa` |
| wrapper | **nothing recorded** by the suite (written after #211) | 2017 runs of 2000 posts against the unfixed source | `vm-qa` |
| vocabulary | #148 at introduction, 2026-09-12 | 3 of 3 constructed violations | `vm-qa` |
| register | D-CLOUD-007 and a dangling citation (`vm-qa:202-203`) | `4b219ef937`, `f00ab3e163` | `vm-qa`, **CI** `fork-checks.yml:37`, `ceremony-check` |
| french | #152, 2026-09-17 | a probe string, `196f823c60` | `vm-qa` |
| quoting | blindspot 57, 2026-09-25 (`GuiMenu.cpp:7597`) | before and after ES `459fc168f` | `vm-qa` |
| menumap | #542, 2026-10-11 (CONNECTION SAVED) | `cc996bd0de` | `vm-qa` |
| pair-identity | **nothing recorded** but its own (blindspot 40) | a recorded lost race through a fake `ssh`, 2026-09-13 | `vm-qa` |
| fresh | audit #258 PL-001, 2026-09-24 (`es_savestates.cfg`) | the same run on `443028ff7a` | `vm-qa` |
| round-trip | #315, 2026-09-28/29 (and two stream-A regressions) | run 71's expected FAIL | `vm-qa`; rules |
| exit | **nothing recorded** | the debounce-stripped copy, `6b95a93d2f` | `vm-qa`; rule command |
| time-to-play | **nothing recorded** but its own (blindspots 39 and 56) | `ttp-263c`; four constructed logs | `vm-qa` |
| link | #401, 2026-10-03 | `test-stamp-assertion.py` 7/7 | opt-in in `vm-qa`; rule |
| ra-offline | **nothing recorded** but its own (blindspot 50) | none found | opt-in; `release-candidates.md:64` |
| walks | G-E2-O1 through `confirm-cloud-folder`, 2026-09-28 | none per walk; `frame-diff` is its comparator | `vm-qa`; `es-ui-style-guide.md:62` |
| frame-diff | G-E2-O1, 2026-09-28 | the missing-claim control rc 1, 2026-10-11 | `vm-qa`; `release-candidates.md:62` |

**Measurements and other scripts** (the drivers, `vm-pair`, `vm-serial`, `vm-stop`, `vm-visual-qa` and `png-blackout`, are infrastructure, not detectors):

| Script | Last recorded catch | Positive | Callers |
| --- | --- | --- | --- |
| `time-to-play` (standalone) | as its suite | as its suite | `vm-qa` only |
| `signin-memory` | **nothing recorded**; it was blindspot 59's false PASS | Dropbox FAIL, example.org PASS | **nobody** (index only) |
| `es-launch-memory` | #310, 2026-10-03 (ES leaks) | the RSS endurance control | **nobody** (index only) |
| `vm-upgrade-rehearsal` | **nothing recorded** (PASS every cut) | `24ceb9e15a` checks | `release-candidates.md` step 3 |
| `ra-ui-test` | **nothing recorded** | the refusal profile | rule mention |
| `raofflineproxy-integration-test` | **nothing recorded** | the wrong-duration negative, `8829907b12` | `release-candidates.md` (proxy) |
| `raofflineproxy-consent-test` | #457, 2026-10-06 | three assertions before patch 019 | rule mention |
| `raofflineproxy-installed-native-test` | **nothing recorded** | none found | **nobody** (descriptive paragraph) |
| `font-stems` | blindspot 54, 2026-09-24 | none found | **nobody** (descriptive mention) |
| `ra-candidate-games` | **nothing recorded** | none found | **nobody** (index only) |
| `es-untranslated` | #152 | `196f823c60` | `vm-qa` french |
| `es-syntax-check` | **nothing recorded** of an edit; its own silent FAIL is #699 | a broken copy FAILs | rule instruction |
| `emulator-exit-test` | **nothing recorded** | `6b95a93d2f` | `vm-qa` exit |
| `qa-accounts` | **nothing recorded** | proven both ways, `4e11497aa7` | `ra-offline-test` |
| `device-act` | a recorder; its own failures 2026-09-27 | none found | rule instruction |
| `vm-pair-test` | **nothing recorded** (no red CI run read) | the original source falsely says up | **CI** `fork-checks.yml:47` |
| `vm-upgrade-readiness-test` | **nothing recorded** after creation (#546's regression) | seven controls | **CI** `fork-checks.yml:48` |
| `vm-stop-test` | **nothing recorded** after creation | the corrected seventh case | rule mention |
| `vm-manager-system-check` | **nothing recorded** (written after #455) | its own controls | `vm-qa` |
| `vm-walks/cloud-epic/migration-protocol.sh` | **nothing recorded**; refuses on current images (P10) | none | `rasteratops-vm-cloud-epic:149` |
| `vm-walks/cloud-epic/vnc-grab.py` | **nothing recorded** | none | `rasteratops-vm-cloud-epic:67` |
| `vm-walks/fixtures/system-selected.sh` | **nothing recorded** | none | `vm-qa:473` |

**Walks** (16 in `suite.txt`, each run by `vm-qa`'s walks suite and keyed to `frame-diff` by its claims; P5):

| Walk | Claims | Last recorded catch |
| --- | ---: | --- |
| to-manage-cloud-storage | 3 | nothing recorded |
| back-up-page | 8 | nothing recorded |
| restore-page | 9 | nothing recorded |
| match-dialog | 19 | its 2026-09-07 cycle ("1 FILES", the preview's 0-byte line) |
| to-change-cloud-folder | 21 | its 2026-09-07 cycle (the editor's field) |
| confirm-cloud-folder | 32 | G-E2-O1, 2026-09-28 |
| tick-roms | 13 | nothing recorded |
| tick-settings | 13 | nothing recorded |
| tick-game-content | 13 | nothing recorded |
| continue-to-systems | 23 | nothing recorded |
| run-transfer-frames | 115 | its 2026-09-09 cycle (row 4 clipped, `e7e672524`) |
| run-transfer | 39 | nothing recorded as a defect (#278, the walk's state) |
| ui-settings-toggle | 6 | nothing recorded |
| manager-nes | 2 | nothing recorded (the standing #245/#250 guard) |
| manager-gb | 7 | its own (#455: it showed FBNeo) |
| manager-fbn | 68 | nothing recorded |

**The step files no suite walk replays,** and their callers:
- the four `docs/*.steps` (rocknix.org, #323), and `m7-cloud-sync` and `m7-retro-achievements` (M7's hand walks), each named in 24 to 41 record files and in the #603 audit's lead-verification config;
- `reset` and `wake`, utility legs.

**Fixtures:**
- **`nes-256x240-right.png` and `arcade-vertical-raw-left.png`:** read by `vm-qa:380-385`. They were the controls in #288's session proof, 2026-09-26.
- **`gb-160x144.png`:** read by `vm-qa:381`, `:384`; nothing recorded.

**The reconciliation** (P5): there are 391 claims and 16 walks; no claim's glob matches no walk, and no walk lacks a claim. All 391 are against `d72084ccad` (F-18).

### Q7 Clarity and structure

| Row | Where | Reading |
| --- | --- | --- |
| `vm-qa --help` | `:81` | prints lines 5 to 38, cutting four suites (F-12) |
| The header's suite list against `SUITES` | `:20-49`; `:63` | the same 17, in the same order |
| `release-candidates.md` step 3 against the default | `release-candidates.md` on `next` | "`tools/vm-qa` with every suite"; the default omits `link` and `ra-offline` (`vm-qa:64`). A reader cannot tell whether "every suite" means the default or all 17: **a lead for the coordinator** |
| The index against the owning rule | `instruction-files.md`; `generic-x64-vm-testing.md` (`next`) | six tools pointed at a rule that never names them; three walk scripts with no row (F-13): **a lead** |
| `suite.txt` | the brief | 16 walks, against the brief's 17 (a delta, `01`) |
| The image's identity | the brief; criterion 9 | the sha256 is in the `.img.gz.sha256` sidecar, not in `.identity.json`; corrected on #659 at 19:33 |
| `generic-x64-vm --daemonize`'s help | another slice's file | "stop it with kill $(cat pidfile)", against `vm-stop` (context for its slice, not a row here) |
| `device-builds.md`'s "about 2 GB" per guest | `next` | measured at 2.54 GiB resident after boot (P11): close. The profile allocates 8 GiB. |

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

- **"A guard judges that something ran, not only what ran."** F-01 to F-03 share one shape: the result is computed over an empty set. `engineering-practices.md` § Guards must fail closed says *a tool that reports numbers fails when the numbers are missing*; the empty set is that case one level up. **A proposal for the coordinator.**

### Codification Gaps (needs-new-rule)

- **A harness run's host state is named by the run.** The QA cloud's state, the pair's directory, the sockets and the ports are all defaults that assume one session on the host (F-09, F-10). The cycle set five variables by hand. **A proposal for the coordinator,** since the rules are not this lane's.

### Recommended Action Sequence

1. F-01 to F-03: the coordinator's stage-D bugs, with their inputs.
2. F-10 and F-09: the shared state.
3. F-04: the `assert` class.
4. F-14 to F-17: the coordinator's dispositions with the maintainer.
5. The Lows.

## Quality Self-Check

- **The coverage table** has 60 rows (`grep -c -E '^\| \`tools/'` gives 60).
- **The proof cells match:** 11 PROOF lines in `00` and 11 class cells in `02`.
- **Every finding has an artifact,** and the record-sourced rows name the helper's file and the lane's spot checks.
- **Every time** comes from `date -u` or an artifact's mtime.

## Second opinion (Phase 4.6)

At stage C.

## file, whole, at 8ebaf8daad: tools/device-act

```
    1  #!/bin/bash
    2  # device-act -- run one command on a device over ssh and record the act where it
    3  # cannot be argued with later.
    4  #
    5  #   tools/device-act <ssh target> <label> -- <remote command...>
    6  #   tools/device-act rgsp "reboot to apply 3ada78e181" -- 'sync; reboot'
    7  #   DEVICE_ACT_SSH_OPTS='-o Hostname=100.75.221.73' tools/device-act rgsp ... -- ...
    8  #   DEVICE_ACT_TIMEOUT=600 tools/device-act rg35xxsp 'hash the staged tar' -- 'sha256sum ...'
    9  #
   10  # The command is killed after DEVICE_ACT_TIMEOUT seconds (default 30) and
   11  # reported as rc=124. A sha256 of a 1.3 GB update tar on an A53 takes minutes,
   12  # so either raise the timeout or start the work detached on the device and
   13  # poll for its result file (2026-09-20: the default cut the hash off and the
   14  # staging chain stopped before the move, which is the safe direction).
   15  #
   16  # Why (blindspot 42, 2026-09-14): a device rebooted from a harness command, and the
   17  # harness then said "not me" twice because the tool result it was reading looked
   18  # like a check that never ran. The device's journal had the truth. So every action
   19  # that changes a device's state is written down BEFORE it runs, with the device's
   20  # boot id at that moment, and the outcome AFTER, with the boot id again -- a
   21  # changed boot id is a reboot, whatever the transcript says.
   22  #
   23  # The record is ${DEVICE_ACTIONS_LOG:-/workspace/artifacts/rocknix-device-actions.log},
   24  # outside the repo and outside any per-session scratch, one line per phase:
   25  #   <UTC time> <target> <label> BEGIN  boot_id=<id> host=<hostname>
   26  #   <UTC time> <target> <label> END    rc=<n> boot_id=<id or unreachable>
   27  # Read it before answering "did you do X" -- and read the device too.
   28  set -u
   29  LOG="${DEVICE_ACTIONS_LOG:-/workspace/artifacts/rocknix-device-actions.log}"
   30  SSH_OPTS=(-n -o ConnectTimeout=8 -o BatchMode=yes ${DEVICE_ACT_SSH_OPTS:-})
   31  TARGET="${1:?ssh target}"; LABEL="${2:?label}"; shift 2
   32  [ "${1:-}" = "--" ] && shift
   33  [ $# -ge 1 ] || { echo "device-act: no remote command after --" >&2; exit 2; }
   34  CMD="$*"
   35  mkdir -p "$(dirname "$LOG")"
   36  probe() { timeout 12 ssh "${SSH_OPTS[@]}" "$TARGET" 'echo "$(cat /proc/sys/kernel/random/boot_id 2>/dev/null) $(hostname)"' 2>/dev/null; }
   37  BEFORE=$(probe) || BEFORE="unreachable"
   38  printf '%s %s %q BEGIN boot_id=%s cmd=%q\n' "$(date -u +%FT%TZ)" "$TARGET" "$LABEL" "${BEFORE%% *}" "$CMD" >> "$LOG"
   39  timeout "${DEVICE_ACT_TIMEOUT:-30}" ssh "${SSH_OPTS[@]}" "$TARGET" "$CMD"; RC=$?
   40  sleep 2
   41  AFTER=$(probe) || AFTER="unreachable"
   42  printf '%s %s %q END rc=%s boot_id=%s\n' "$(date -u +%FT%TZ)" "$TARGET" "$LABEL" "$RC" "${AFTER%% *}" >> "$LOG"
   43  echo "device-act: $TARGET '$LABEL' rc=$RC; before boot_id=${BEFORE%% *} after=${AFTER%% *}; recorded in $LOG"
   44  exit $RC
   45  
```

## file, whole, at 8ebaf8daad: tools/emulator-exit-test

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # emulator-exit-test - the exit hotkey ends a game once, cleanly, with the save written.
    6  #
    7  #   ./tools/emulator-exit-test --port 10022 --identity /tmp/rocknix-vm-pair/qa-key [--vm] [--only BC]
    8  #
    9  # Why this exists. The exit hotkey (A+B+C on a handheld) sends SIGTERM to the
   10  # emulator through input_sense's execute_kill. RetroArch ends cleanly on the
   11  # first one, in about half a second, and writes the battery save on the way
   12  # out. A SECOND SIGTERM inside that half-second makes it exit(1) WITHOUT
   13  # writing the save -- and the combo re-fires on every further press while the
   14  # first button is held, so a thumb that lingers loses everything since the
   15  # last autosave (fork #117). Since D-LAUNCH-003 execute_kill drops a repeat
   16  # within three seconds. This cell proves, against the shipped input_sense:
   17  #
   18  #   A  one press: runemu.sh exits 0, the .srm exists and holds what the game wrote
   19  #   B  three presses in a row (a held combo): the same outcome -- the repeats are dropped
   20  #   C  the window closes: on a generic target, a press 4 s after the first goes through
   21  #   D  the exit-hotkey marker never outlives a launch
   22  #
   23  # It fails against an input_sense without the debounce -- B finds no .srm, C
   24  # finds the repeat went through -- which is what makes it a regression gate
   25  # rather than a demonstration (proven both ways on the VM, 2026-09-10). The
   26  # exit code alone is not the signal: since #92 runemu.sh reads a forced quit
   27  # as clean, so the save on disk is what decides. The
   28  # cartridge is built here -- 32 KiB, MBC1+RAM+BATTERY, writes $55 to $A000 and
   29  # spins -- so the save's content is known and nothing copyrighted travels.
   30  #
   31  # Runs over SSH against a guest or a handheld that already has gambatte
   32  # (every ROCKNIX image does). --vm sets RetroArch's video driver to gl for
   33  # the run and puts it back, because the QEMU guest has no Vulkan; never
   34  # pass it for a handheld. Nothing else on the device is changed, and every
   35  # file this writes is removed at the end.
   36  set -u
   37  HOST=root@127.0.0.1; PORT=22; KEY=""; VM=0; ONLY=ABCD
   38  while [ $# -gt 0 ]; do
   39    case "$1" in
   40      --host) HOST=$2; shift 2 ;;
   41      --port) PORT=$2; shift 2 ;;
   42      --identity) KEY=$2; shift 2 ;;
   43      --vm) VM=1; shift ;;
   44      --only) ONLY=$2; shift 2 ;;
   45      -h|--help) sed -n '5,32p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
   46      *) echo "unknown argument: $1" >&2; exit 2 ;;
   47    esac
   48  done
   49  SSHO=(-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=8 -o BatchMode=yes -p "$PORT")
   50  [ -n "$KEY" ] && SSHO+=(-i "$KEY")
   51  S() { ssh -n "${SSHO[@]}" "$HOST" "$@"; }
   52  FAILS=0
   53  check() { if [ "$1" = 0 ]; then echo "  PASS  $2"; else echo "  FAIL  $2"; FAILS=$((FAILS+1)); fi; }
   54  
   55  ROM=/storage/roms/gb/ExitProbe.gb; SRM=/storage/roms/gb/ExitProbe.srm
   56  TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
   57  
   58  # --- the cartridge -----------------------------------------------------------
   59  python3 - "$TMP/ExitProbe.gb" <<'PY'
   60  import sys
   61  rom = bytearray(0x8000)
   62  rom[0x100:0x104] = bytes([0x00, 0xC3, 0x50, 0x01])          # NOP ; JP $0150
   63  logo = bytes.fromhex("CEED6666CC0D000B03730083000C000D0008111F8889000EDCCC6EE6DDDDD999BBBB67636E0EECCCDDDC999FBBB9333E")
   64  rom[0x104:0x134] = logo
   65  rom[0x134:0x13D] = b"EXITPROBE"
   66  rom[0x147] = 0x03   # MBC1 + RAM + BATTERY
   67  rom[0x148] = 0x00   # 32 KiB ROM
   68  rom[0x149] = 0x02   # 8 KiB RAM
   69  rom[0x14A] = 0x01
   70  rom[0x14B] = 0x33
   71  x = 0
   72  for i in range(0x134, 0x14D):
   73      x = (x - rom[i] - 1) & 0xFF
   74  rom[0x14D] = x
   75  code = bytes([
   76      0xF3,                    # DI
   77      0x3E, 0x0A,              # LD A,$0A
   78      0xEA, 0x00, 0x00,        # LD ($0000),A   enable external RAM
   79      0x3E, 0x55,              # LD A,$55
   80      0xEA, 0x00, 0xA0,        # LD ($A000),A   the byte the test looks for
   81      0x18, 0xFE,              # JR -2          spin
   82  ])
   83  rom[0x150:0x150+len(code)] = code
   84  open(sys.argv[1], "wb").write(rom)
   85  PY
   86  scp -q "${SSHO[@]/#-p/-P}" "$TMP/ExitProbe.gb" "$HOST:/tmp/ExitProbe.gb" 2>/dev/null || { scp -q -P "$PORT" ${KEY:+-i "$KEY"} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR "$TMP/ExitProbe.gb" "$HOST:/tmp/ExitProbe.gb"; }
   87  
   88  # --- the device-side helpers -------------------------------------------------
   89  # press: the shipped execute_kill, extracted from the installed input_sense so
   90  # the signal and the marker come from the code under test, not a copy of it.
   91  S 'mkdir -p /storage/roms/gb && mv /tmp/ExitProbe.gb '"$ROM"' && cat > /tmp/exit-press <<"H"
   92  #!/bin/bash
   93  DEBUG=false; log() { :; }
   94  eval "$(sed -n "/^execute_kill()/,/^}/p" /usr/bin/input_sense)"
   95  for i in $(seq 1 "${1:-1}"); do execute_kill; [ "${1:-1}" -gt 1 ] && [ "${2:-0}" != 0 ] && sleep "${2}"; done
   96  H
   97  chmod +x /tmp/exit-press
   98  cat > /tmp/exit-launch <<"H"
   99  #!/bin/bash
  100  # launch through runemu.sh exactly as es_systems.cfg does, record its exit code
  101  rm -f /tmp/exit-rc
  102  /usr/bin/runemu.sh "$1" -Pgb --core=gambatte --emulator=retroarch --controllers= >/tmp/exit-launch.log 2>&1
  103  echo $? > /tmp/exit-rc
  104  H
  105  chmod +x /tmp/exit-launch; echo helpers-ready'
  106  
  107  VD=""
  108  if [ "$VM" = 1 ]; then
  109    VD=$(S 'grep -E "^video_driver" /storage/.config/retroarch/retroarch.cfg')
  110    S 'sed -i "s/^video_driver = .*/video_driver = \"gl\"/" /storage/.config/retroarch/retroarch.cfg'
  111  fi
  112  cleanup() {
  113    S "pkill -TERM -f '^/usr/bin/retroarch' 2>/dev/null; sleep 1; rm -f $ROM $SRM /storage/roms/gb/ExitProbe.rtc /tmp/exit-press /tmp/exit-launch /tmp/exit-rc /tmp/exit-launch.log; rmdir /storage/roms/gb 2>/dev/null; true"
  114    [ -n "$VD" ] && S "sed -i 's/^video_driver = .*/${VD//\//\\/}/' /storage/.config/retroarch/retroarch.cfg"
  115  }
  116  trap 'cleanup; rm -rf "$TMP"' EXIT
  117  
  118  launch() {  # start the game, wait for RetroArch, give the cartridge time to write
  119    S "rm -f $SRM; nohup /tmp/exit-launch $ROM >/dev/null 2>&1 &"
  120    local i; for i in $(seq 1 45); do S 'pgrep -f "^/usr/bin/retroarch" >/dev/null' && break; sleep 2; done
  121    S 'pgrep -f "^/usr/bin/retroarch" >/dev/null' || { echo "  RetroArch never started (see /tmp/exit-launch.log on the device)"; return 1; }
  122    # The cartridge writes its byte in its first frames, but RetroArch has to
  123    # get there first: on an RG35XX SP the first launch after a boot spends
  124    # longer than four seconds loading the core and compiling shaders, so a
  125    # fixed wait pressed the hotkey before the game had run and part A found
  126    # no .srm -- a warm launch then passed three times (2026-09-11). Wait for
  127    # the process to have burnt two seconds of CPU, which means the core is
  128    # running, then a margin for the write itself.
  129    # 200 ticks is a software-rendered RetroArch's signature: on hardware GL
  130    # (fork #291) the process burns about five ticks a second after some
  131    # thirty of init, and waited the whole loop out on every launch. In the
  132    # VM the rule is also met at thirty ticks once four polls have seen the
  133    # process up; a device keeps the two seconds.
  134    local up=0 t
  135    for i in $(seq 1 40); do
  136      t=$(S 'p=$(pgrep -f "^/usr/bin/retroarch" | head -1); [ -n "$p" ] && awk "{print \$14+\$15}" /proc/$p/stat 2>/dev/null || echo 0' | tr -d '\r'); t=${t:-0}
  137      [ "$t" -ge 200 ] && break
  138      [ "$t" -gt 0 ] && up=$((up+1))
  139      [ "$VM" = 1 ] && [ "$up" -ge 4 ] && [ "$t" -ge 30 ] && break
  140      sleep 1
  141    done
  142    sleep 3
  143  }
  144  wait_exit() {  # until runemu.sh has returned
  145    local i; for i in $(seq 1 30); do S 'test -f /tmp/exit-rc' && return 0; sleep 1; done; return 1
  146  }
  147  srm_ok() { S "test -f $SRM && [ \"\$(head -c1 $SRM | od -An -tx1 | tr -d ' ')\" = 55 ]"; }
  148  
  149  case "$ONLY" in *A*)
  150  echo "A  one press ends the game cleanly and the save is written"
  151  if launch; then
  152    S '/tmp/exit-press 1'; wait_exit; rc=$(S 'cat /tmp/exit-rc 2>/dev/null')
  153    check "$([ "$rc" = 0 ]; echo $?)" "runemu.sh exit code is 0 (got ${rc:-none})"
  154    check "$(srm_ok; echo $?)" ".srm exists and its first byte is 55"
  155    check "$(S 'test ! -e /tmp/.process-kill-requested'; echo $?)" "the exit-hotkey marker was consumed"
  156  else check 1 "launch"; fi ;; esac
  157  
  158  case "$ONLY" in *B*)
  159  echo "B  a held combo: three presses back to back end the game once, save intact"
  160  if launch; then
  161    S '/tmp/exit-press 3 0'; wait_exit; rc=$(S 'cat /tmp/exit-rc 2>/dev/null')
  162    check "$([ "$rc" = 0 ]; echo $?)" "runemu.sh exit code is 0 (got ${rc:-none})"
  163    check "$(srm_ok; echo $?)" ".srm exists and its first byte is 55 -- without the debounce there is no .srm"
  164  else check 1 "launch"; fi ;; esac
  165  
  166  case "$ONLY" in *C*)
  167  echo "C  the window closes: a press 4 s after the first goes through"
  168  # One process for the three presses, because the window is a variable inside
  169  # the long-running input_sense and a fresh shell per press would never see
  170  # it. The target is a script of its own -- `killall sleep` would also hit the
  171  # device's daemons, which respawn their sleeps and make the count meaningless.
  172  S 'cp /tmp/.process-kill-data /tmp/.process-kill-data.saved 2>/dev/null; printf "#!/bin/sh\nsleep 300\n" > /tmp/xprobe; chmod +x /tmp/xprobe; echo xprobe > /tmp/.process-kill-data
  173  cat > /tmp/exit-window <<"H"
  174  #!/bin/bash
  175  DEBUG=false; log() { :; }
  176  eval "$(sed -n "/^execute_kill()/,/^}/p" /usr/bin/input_sense)"
  177  n() { pgrep -x xprobe | wc -l; }
  178  (/tmp/xprobe >/dev/null 2>&1 </dev/null &); sleep 0.5
  179  execute_kill; sleep 0.5; echo "n1=$(n)"
  180  (/tmp/xprobe >/dev/null 2>&1 </dev/null &); sleep 0.5
  181  execute_kill; sleep 0.5; echo "n2=$(n)"
  182  sleep 4
  183  execute_kill; sleep 0.5; echo "n3=$(n)"
  184  H
  185  chmod +x /tmp/exit-window; /tmp/exit-window; pkill -x xprobe; rm -f /tmp/xprobe /tmp/exit-window /tmp/.process-kill-requested; mv -f /tmp/.process-kill-data.saved /tmp/.process-kill-data 2>/dev/null' > "$TMP/c.out" 2>&1
  186  n1=$(sed -n 's/^n1=//p' "$TMP/c.out"); n2=$(sed -n 's/^n2=//p' "$TMP/c.out"); n3=$(sed -n 's/^n3=//p' "$TMP/c.out")
  187  check "$([ "${n1:-x}" = 0 ]; echo $?)" "first press kills the target (survivors: ${n1:-?})"
  188  check "$([ "${n2:-x}" = 1 ]; echo $?)" "a repeat inside 3 s is dropped (survivors: ${n2:-?})"
  189  check "$([ "${n3:-x}" = 0 ]; echo $?)" "a press after the window goes through (survivors: ${n3:-?})"
  190  [ "${n1:-x}${n2:-x}${n3:-x}" = "010" ] || { echo "  --- raw:"; sed 's/^/  | /' "$TMP/c.out"; } ;; esac
  191  
  192  case "$ONLY" in *D*)
  193  echo "D  the marker never outlives a launch"
  194  check "$(S 'test ! -e /tmp/.process-kill-requested'; echo $?)" "no /tmp/.process-kill-requested left behind" ;; esac
  195  
  196  echo; if [ "$FAILS" = 0 ]; then echo "PASSED"; else echo "FAILED ($FAILS)"; exit 1; fi
  197  
```

## file, whole, at 8ebaf8daad: tools/es-launch-memory

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  """Measure EmulationStation launch/exit memory on an owned local QA VM (#310).
    5  
    6  Uses ES's launch API and the image's execute_kill function. Captures status,
    7  maps and smaps after every cycle; refuses a changed ES PID or a lost launch.
    8  It does not provision ROMs, change settings or enable cloud synchronization.
    9  Omit memory limits for diagnosis; supply both limits for an acceptance run.
   10  """
   11  import argparse
   12  import csv
   13  import json
   14  import re
   15  import shlex
   16  import subprocess
   17  import time
   18  from pathlib import Path
   19  
   20  
   21  def main():
   22      parser = argparse.ArgumentParser(description=__doc__)
   23      parser.add_argument('--port', type=int, default=10026)
   24      parser.add_argument('--process-name', default='emulationstation',
   25                          help='pgrep name expression (override only for instrumented diagnostics)')
   26      parser.add_argument('--identity', required=True)
   27      parser.add_argument('--rom', default='/storage/roms/gb/Ninoid.gb')
   28      parser.add_argument('--cycles', type=int, required=True)
   29      parser.add_argument('--warmup', type=int, default=0)
   30      parser.add_argument('--output', type=Path, required=True)
   31      parser.add_argument('--max-vmsize-kib', type=int)
   32      parser.add_argument('--max-rss-kib', type=int)
   33      parser.add_argument('--expect-exit-sync', action='store_true',
   34                          help='require a new successful exit-sync stamp on every cycle')
   35      parser.add_argument('--prepare-walk', type=Path,
   36                          help='optional VM UI walk before each launch (e.g. original diagnostic navigation)')
   37      parser.add_argument('--monitor', help='QEMU monitor required with --prepare-walk')
   38      args = parser.parse_args()
   39      if args.cycles < 1 or args.warmup < 0:
   40          parser.error('cycles must be positive and warmup nonnegative')
   41      if (args.max_vmsize_kib is None) != (args.max_rss_kib is None):
   42          parser.error('acceptance requires both memory limits')
   43      if args.prepare_walk and not args.monitor:
   44          parser.error('--prepare-walk requires --monitor')
   45      args.output.mkdir(parents=True, exist_ok=False)
   46      ssh = ['ssh', '-n', '-i', args.identity, '-p', str(args.port),
   47             '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=8',
   48             '-o', 'StrictHostKeyChecking=accept-new',
   49             '-o', f'UserKnownHostsFile={args.output}/known_hosts',
   50             '-o', 'LogLevel=ERROR', 'root@127.0.0.1']
   51  
   52      def guest(command):
   53          result = subprocess.run(ssh + [command], text=True, capture_output=True, timeout=40)
   54          if result.returncode:
   55              raise RuntimeError(f'guest command failed with status {result.returncode}')
   56          return result.stdout
   57  
   58      def wait_for(command, predicate, description, seconds=90):
   59          deadline = time.monotonic() + seconds
   60          while time.monotonic() < deadline:
   61              if predicate(guest(command)):
   62                  return
   63              time.sleep(0.5)
   64          raise RuntimeError(f'timed out waiting for {description}')
   65  
   66      idle = 'curl -sS -m 3 http://127.0.0.1:1234/isIdle || true'
   67      def is_idle(text):
   68          try:
   69              return json.loads(text) == [True]
   70          except ValueError:
   71              return False  # the interface may still be starting
   72      running = "pgrep -f '^/usr/bin/retroarch' || true"
   73      if guest(running).strip():
   74          raise RuntimeError('a game is already running')
   75      wait_for(idle, is_idle, 'idle interface')
   76      pid_command = 'pgrep -o -- ' + shlex.quote(args.process_name)
   77      pid = guest(pid_command).strip()
   78      if not pid.isdigit():
   79          raise RuntimeError('no unique interface PID')
   80      filtered = "grep -v -i -E 'key|pass|token|user|psk'"
   81      (args.output / 'os-release.txt').write_text(guest(f'cat /etc/os-release | {filtered}'))
   82      (args.output / 'binary.sha256').write_text(guest('sha256sum /usr/bin/emulationstation'))
   83      (args.output / 'mesa.sha256').write_text(guest('sha256sum /usr/lib/libgallium-*.so'))
   84      (args.output / 'sdl.sha256').write_text(guest('sha256sum /usr/lib/libSDL2-2.0.so.0'))
   85      (args.output / 'rom.sha256').write_text(guest('sha256sum ' + shlex.quote(args.rom)))
   86      (args.output / 'settings.txt').write_text(guest(
   87          '. /etc/profile >/dev/null 2>&1; '
   88          'for setting in cloudsaves.startup cloudsaves.gameexit global.retroachievements '
   89          'global.retroachievements.offlineproxy; do '
   90          'printf "%s=" "$setting"; get_setting "$setting"; done | ' + filtered))
   91      rows = []
   92  
   93      def snapshot(iteration):
   94          if guest(pid_command).strip() != pid:
   95              raise RuntimeError('interface PID changed; this cannot prove bounded growth')
   96          status = ''
   97          for kind in ('status', 'maps', 'smaps'):
   98              text = guest(f'cat /proc/{pid}/{kind} | {filtered}')
   99              (args.output / f'{iteration:03d}.{kind}').write_text(text)
  100              if kind == 'status':
  101                  status = text
  102          (args.output / f'{iteration:03d}.threads').write_text(
  103              guest(f'cat /proc/{pid}/task/*/comm | {filtered}'))
  104          fields = {}
  105          for name in ('VmSize', 'VmRSS', 'Threads'):
  106              match = re.search(rf'^{name}:\s+(\d+)', status, re.M)
  107              if not match:
  108                  raise RuntimeError(f'missing {name} in process status')
  109              fields[name] = int(match.group(1))
  110          row = [iteration, pid, int(time.time()), fields['VmSize'], fields['VmRSS'], fields['Threads']]
  111          rows.append(row)
  112          with (args.output / 'cycles.csv').open('w') as stream:
  113              writer = csv.writer(stream)
  114              writer.writerow(['cycle', 'pid', 'epoch', 'vmsize_kib', 'vmrss_kib', 'threads'])
  115              writer.writerows(rows)
  116          print(','.join(map(str, row)), flush=True)
  117  
  118      snapshot(0)
  119      stamp_command = "cat /storage/.cache/cloud_sync/last-sync-exit 2>/dev/null || true"
  120      for iteration in range(1, args.warmup + args.cycles + 1):
  121          wait_for(idle, is_idle, 'idle interface')
  122          previous_stamp = guest(stamp_command).strip() if args.expect_exit_sync else None
  123          if args.prepare_walk:
  124              with (args.output / f'{iteration:03d}.walk.log').open('w') as stream:
  125                  subprocess.run([str(Path(__file__).resolve().with_name('vm-visual-qa')),
  126                                  '--monitor', args.monitor, 'run', str(args.prepare_walk),
  127                                  '--outdir', str(args.output / f'{iteration:03d}-walk')],
  128                                 stdout=stream, stderr=subprocess.STDOUT, check=True, timeout=90)
  129          guest('curl -fsS -m 10 -X POST -H "Content-Type: text/plain" --data ' +
  130                shlex.quote(args.rom) + ' http://127.0.0.1:1234/launch')
  131          wait_for(running, lambda text: bool(text.strip()), 'RetroArch process')
  132          time.sleep(3)
  133          # execute_kill kills ES when no emulator exists, so check at the call.
  134          exit_status = guest("pgrep -f '^/usr/bin/retroarch' >/dev/null || exit 9; "
  135                "bash -c 'DEBUG=false; log() { :; }; "
  136                'eval "$(sed -n "/^execute_kill()/,/^}/p" /usr/bin/input_sense)"; execute_kill\'; result=$?; printf \"%s\\n\" \"$result\"')
  137          # killall can return nonzero for another named process after killing
  138          # RetroArch. Retain that status; the observed exit is the assertion.
  139          print(f'exit-helper return={exit_status.strip()}', flush=True)
  140          wait_for(running, lambda text: not text.strip(), 'RetroArch exit')
  141          wait_for(idle, is_idle, 'interface return')
  142          if args.expect_exit_sync:
  143              wait_for(stamp_command,
  144                       lambda text: bool(text.strip()) and text.strip() != previous_stamp,
  145                       'a new exit-sync stamp')
  146              stamp = guest(stamp_command).strip()
  147              (args.output / f'{iteration:03d}.exit-sync').write_text(stamp + '\n')
  148              fields = stamp.split()
  149              if len(fields) < 3 or fields[1:3] != ['0', 'completed']:
  150                  raise RuntimeError(f'exit sync did not complete on cycle {iteration}')
  151          time.sleep(3)
  152          snapshot(iteration)
  153      baseline, last = rows[args.warmup], rows[-1]
  154      result = {'pid': int(pid), 'cycles': args.cycles, 'warmup': args.warmup,
  155                'vmsize_growth_kib': last[3] - baseline[3],
  156                'rss_growth_kib': last[4] - baseline[4]}
  157      if args.max_vmsize_kib is not None:
  158          result['passed'] = (result['vmsize_growth_kib'] < args.max_vmsize_kib and
  159                              result['rss_growth_kib'] < args.max_rss_kib)
  160      (args.output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
  161      print(json.dumps(result), flush=True)
  162      return 0 if result.get('passed', True) else 1
  163  
  164  
  165  if __name__ == '__main__':
  166      raise SystemExit(main())
  167  
```

## file, whole, at 8ebaf8daad: tools/es-syntax-check

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # es-syntax-check - compile one EmulationStation source file with the image
    6  # build's own compiler and flags, syntax only, before the pin moves.
    7  #
    8  #   tools/es-syntax-check <path/to/File.cpp> [more .cpp files]
    9  #   tools/es-syntax-check --tree <es worktree> <File.cpp>...   # headers changed too
   10  #
   11  # An EmulationStation edit here has no compiler nearer than an image build:
   12  # the cross toolchain, the sysroot and the flags live in a build root, and a
   13  # mistake that any compiler would have caught costs a full build cycle to
   14  # find. On 2026-09-21 a loop body grew from one statement to three without
   15  # braces; the syntax was fine, the scoping was not, and GENERIC_X64 run 12
   16  # died at emulationstation with `'name' was not declared` twenty minutes
   17  # after the pin was bumped (blindspot 49).
   18  #
   19  # So: find the newest emulationstation build directory under the build root
   20  # (`ES_BUILD_ROOT`, default the generic-x64 worktree's), ask ninja for the
   21  # exact command it used on the object that corresponds to the file, point
   22  # that command at the edited file instead, drop the output and dependency
   23  # flags, add -fsyntax-only, and run it.
   24  #
   25  # Include roots (audit #258 PL-005). Every `#include "..."` must resolve to
   26  # ONE file, or `#pragma once` lets the same header in twice and the check
   27  # fails on redefinitions the compiler never sees in a real build: a .cpp's
   28  # own directory is searched first, so `#include "GuiRetroAchievements.h"`
   29  # from beside it found the worktree's copy while `#include
   30  # "guis/GuiRetroAchievements.h"` through the build's -I found the build
   31  # tree's -- byte-identical, different inodes and mtimes, two files to GCC.
   32  # Three of fifty-five in-range units failed that way on 2026-09-24. So:
   33  #
   34  #   plain          the worktree's own es-app/src and es-core/src (found up
   35  #                  from each .cpp) go in as -I ahead of the build's own -I
   36  #                  (and as -iquote): every include of an ES header, quoted
   37  #                  or <angled> -- InputManager.h writes <utils/Delegate.h>,
   38  #                  Settings.h "utils/Delegate.h" -- resolves to the worktree.
   39  #   --with <dir>   one more -iquote, ahead of those.
   40  #   --tree <wt>    a farm of symlinks with every header the worktree has
   41  #                  pointed at the worktree (the build tree's for any it
   42  #                  lacks), in as -I ahead of the build's and as -iquote; for
   43  #                  a worktree that is not where the .cpp lives.
   44  #
   45  # Either way the compiler checks the edited .cpp against the edited
   46  # headers, and headers of the same name reach it through one inode.
   47  #
   48  # Exit 0 when every file passes, 1 when one does not (the compiler's errors
   49  # are printed), 2 when the check cannot run -- no build root, no ninja
   50  # directory, no command for that object. A check that cannot run has not
   51  # passed (engineering-practices.md, "Guards must fail closed").
   52  set -uo pipefail
   53  ROOT_DEFAULT=/workspace/repos/rocknix.worktrees/generic-x64/build.ROCKNIX-GENERIC_X64.x86_64
   54  BROOT="${ES_BUILD_ROOT:-$ROOT_DEFAULT}"
   55  WITH=""
   56  TREE=""
   57  PRE=""     # -I dirs to put ahead of the build's own (the header above)
   58  FILES=()
   59  while [ $# -gt 0 ]; do
   60    case "$1" in
   61      --root) BROOT="${2:?}"; shift 2 ;;
   62      --with) WITH="$WITH -iquote${2:?}"; shift 2 ;;
   63      --tree) TREE="${2:?}"; shift 2 ;;
   64      -h|--help) sed -n '5,32p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
   65      *) FILES+=("$1"); shift ;;
   66    esac
   67  done
   68  [ ${#FILES[@]} -gt 0 ] || { echo "es-syntax-check: name at least one .cpp" >&2; exit 2; }
   69  [ -d "$BROOT" ] || { echo "es-syntax-check: no build root at $BROOT (ES_BUILD_ROOT, --root)" >&2; exit 2; }
   70  NINJA="$BROOT/toolchain/bin/ninja"; [ -x "$NINJA" ] || NINJA=$(command -v ninja || true)
   71  [ -n "$NINJA" ] || { echo "es-syntax-check: no ninja in $BROOT/toolchain/bin or on PATH" >&2; exit 2; }
   72  # The newest emulationstation build directory: a stale one has the right
   73  # flags too, and its headers differ only where the pin moved.
   74  BD=$(ls -td "$BROOT"/build/emulationstation-*/.x86_64-rocknix-linux-gnu "$BROOT"/build/emulationstation-*/.*-rocknix-linux-gnu* 2>/dev/null | head -1)
   75  [ -n "$BD" ] || { echo "es-syntax-check: no emulationstation build directory under $BROOT/build" >&2; exit 2; }
   76  echo "using $(basename "$(dirname "$BD")")"
   77  # --tree <worktree>: an edit that changed headers in both es-core and es-app.
   78  # Two plain --with dirs break on `#pragma once` -- a header reached through
   79  # the worktree in one place and through the build tree in another is two
   80  # files to the compiler (Delegate.h, 2026-09-22) -- so the farm below is
   81  # the build tree's es-core/src and es-app/src as symlinks (the build tree's
   82  # inodes), with only the headers that differ from the worktree's pointed at
   83  # the worktree. Every include then resolves to one file, and the edited
   84  # headers win.
   85  if [ -n "$TREE" ]; then
   86    [ -d "$TREE/es-core/src" ] && [ -d "$TREE/es-app/src" ] || { echo "es-syntax-check: --tree $TREE has no es-core/src and es-app/src" >&2; exit 2; }
   87    ESB=$(dirname "$BD"); FARM=$(mktemp -d "${TMPDIR:-/tmp}/es-syntax-farm.XXXXXX"); trap 'rm -rf "$FARM"' EXIT
   88    for part in es-core es-app; do
   89      cp -rs "$ESB/$part/src" "$FARM/$part"
   90      # Every header the worktree has points at the worktree, changed or not,
   91      # so a header reached by two names is one inode (see the header above);
   92      # only the changed ones are announced.
   93      while IFS= read -r h; do
   94        rel=${h#"$TREE/$part/src/"}
   95        mkdir -p "$FARM/$part/$(dirname "$rel")"; ln -sfn "$h" "$FARM/$part/$rel"
   96        if [ ! -e "$ESB/$part/src/$rel" ] || ! cmp -s "$h" "$ESB/$part/src/$rel"; then
   97          echo "  (header) $part/src/$rel from the tree"
   98        fi
   99      done < <(find "$TREE/$part/src" -name '*.h' -type f)
  100      WITH="$WITH -iquote$FARM/$part"
  101      PRE="${PRE:-} -I$FARM/$part"
  102    done
  103    # --with intentionally adds only quote-search directories. The full tree's
  104    # external root must also win for <libcheevos/cheevos.h> and other angled
  105    # includes; otherwise the cached build's older external header is selected.
  106    if [ -d "$TREE/external" ]; then
  107      PRE="${PRE:-} -I$TREE/external"
  108      echo "  (external) $TREE/external from the tree"
  109    fi
  110  fi
  111  fail=0
  112  for f in "${FILES[@]}"; do
  113    [ -f "$f" ] || { echo "  MISSING $f" >&2; fail=1; continue; }
  114    abs=$(readlink -f "$f")
  115    # es-app/src/guis/GuiCloudTransfer.cpp -> es-app/CMakeFiles/emulationstation.dir/src/guis/GuiCloudTransfer.cpp.o
  116    rel=${abs#*/es-app/}; comp=es-app; dir=emulationstation
  117    case "$abs" in
  118      */es-core/*) rel=${abs#*/es-core/}; comp=es-core; dir=es-core ;;
  119      */es-app/*) ;;
  120      *) echo "  SKIP    $f: not under es-app/ or es-core/" >&2; fail=1; continue ;;
  121    esac
  122    obj="$comp/CMakeFiles/$dir.dir/$rel.o"
  123    cmd=$("$NINJA" -C "$BD" -t commands "$obj" 2>/dev/null | tail -1)
  124    if [ -z "$cmd" ]; then
  125      # A file the build has never seen -- new in the edit -- borrows the
  126      # command of a sibling object in its directory: the flags are the
  127      # directory's, and the source is substituted below.
  128      sib=$("$NINJA" -C "$BD" -t targets all 2>/dev/null | sed -n "s#^\($(dirname "$obj")/[^/]*\.cpp\.o\):.*#\1#p" | grep -v "/$(basename "$rel").o\$" | head -1)
  129      [ -n "$sib" ] && cmd=$("$NINJA" -C "$BD" -t commands "$sib" 2>/dev/null | tail -1)
  130      [ -n "$cmd" ] && echo "  (new)   $f: borrowing the command of $(basename "$sib" .o)"
  131    fi
  132    [ -n "$cmd" ] || { echo "  NO-CMD  $f: ninja has no command for $obj and no sibling to borrow from" >&2; fail=1; continue; }
  133    new=$(printf '%s' "$cmd" | sed -E "s#-c [^ ]+\.(cpp|cc|cxx)( |\$)#-c ${abs} #; s# -o [^ ]+\.o# #; s# -MF [^ ]+# #; s# -MD # #; s# -MT [^ ]+# #")
  134    # The worktree this .cpp lives in: its es-app/src and es-core/src ahead of
  135    # the build's -I, so every quoted include is the worktree's (the header
  136    # above). --tree's farm already does this and comes first.
  137    wt=${abs%/es-app/*}; [ "$wt" = "$abs" ] && wt=${abs%/es-core/*}
  138    own=""; pre="$PRE"
  139    if [ -z "$TREE" ] && [ -d "$wt/es-app/src" ] && [ -d "$wt/es-core/src" ]; then
  140      own="-iquote$wt/es-core/src -iquote$wt/es-app/src"
  141      pre="-I$wt/es-core/src -I$wt/es-app/src"
  142    fi
  143    # The worktree's (or the farm's) -I ahead of the build's first -I, so an
  144    # <angled> include of an ES header finds the same file a quoted one does.
  145    [ -n "$pre" ] && new=$(printf '%s' "$new" | sed -E "s# -I# ${pre} -I#")
  146    new="$new $WITH $own -fsyntax-only"
  147    if out=$(cd "$BD" && eval "$new" 2>&1); then
  148      echo "  OK      $f"
  149    else
  150      echo "  FAIL    $f"; printf '%s\n' "$out" | grep -E 'error|note:' | head -12 | sed 's/^/          /'; fail=1
  151    fi
  152  done
  153  [ "$fail" = 0 ] && echo "PASS" || { echo "FAIL"; exit 1; }
  154  
```

## file, whole, at 8ebaf8daad: tools/es-untranslated

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # es-untranslated -- list the fork's EmulationStation strings that have no French.
    6  #
    7  # D-UI-051: a string the fork adds ships in English and French, written by hand into
    8  # locale/lang/fr/LC_MESSAGES/emulationstation2.po; a missing translation falls through
    9  # to English silently, which is why this exists (#152). A fork string is a `_("...")`
   10  # msgid in es-app/src or es-core/src that the upstream base carries neither in its
   11  # catalogue nor in its source; the reference is the upstream base (the merge base of
   12  # HEAD with the upstream branch, derived each run -- audit #258 PL-022), read from git,
   13  # so the list is exactly what the fork added. Its source counts as well as its .po
   14  # because upstream adds strings without regenerating the catalogue: after the
   15  # 2026-09-25 merge the fuel-gauge reset's two strings read as the fork's, and the
   16  # `french` suite failed on strings the fork never wrote. Upstream's untranslated
   17  # strings are still listed, after the summary, and do not fail the check. Untranslated means the msgid is absent from the current
   18  # French catalogue or has an empty msgstr. The msgid must match the source byte for
   19  # byte, because the build merges by msgid.
   20  #
   21  #   tools/es-untranslated [--es-src DIR] [--upstream COMMIT] [--quiet]
   22  #     ES_SRC=<checkout> tools/es-untranslated
   23  #
   24  # Prints one line per untranslated fork string, `file:line<TAB>msgid`, then a summary;
   25  # exits 1 while any remain and 0 when none do, so tools/vm-qa can run it on the host
   26  # beside `vocabulary` and `register`.
   27  import argparse, os, re, subprocess, sys
   28  
   29  def parse_po(text):
   30      """msgid -> msgstr for a gettext catalogue (single- and multi-line entries; plurals keep msgstr[0])."""
   31      out = {}
   32      cur_id = None; cur_str = None; mode = None
   33      def unesc(s):
   34          return bytes(s, "utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8")
   35      def flush():
   36          nonlocal cur_id, cur_str
   37          if cur_id is not None:
   38              out[cur_id] = cur_str or ""
   39          cur_id = None; cur_str = None
   40      for line in text.splitlines():
   41          line = line.strip()
   42          if not line or line.startswith("#"):
   43              continue
   44          m = re.match(r'^(msgid|msgid_plural|msgstr(?:\[\d+\])?|msgctxt)\s+"(.*)"$', line)
   45          if m:
   46              key, val = m.group(1), unesc(m.group(2))
   47              if key == "msgid":
   48                  flush(); cur_id = val; mode = "id"
   49              elif key == "msgstr" or key == "msgstr[0]":
   50                  cur_str = val; mode = "str"
   51              elif key.startswith("msgstr["):
   52                  mode = "other"
   53              else:
   54                  mode = "other"
   55              continue
   56          m = re.match(r'^"(.*)"$', line)
   57          if m:
   58              val = unesc(m.group(1))
   59              if mode == "id" and cur_id is not None: cur_id += val
   60              elif mode == "str" and cur_str is not None: cur_str += val
   61      flush()
   62      out.pop("", None)
   63      return out
   64  
   65  def source_strings(root):
   66      """(msgid, file:line) for every _("...") in es-app/src and es-core/src, adjacent literals joined."""
   67      found = {}
   68      pat = re.compile(r'_\(\s*((?:"(?:[^"\\]|\\.)*"\s*)+)\)')
   69      for sub in ("es-app/src", "es-core/src"):
   70          for dp, _dirs, files in os.walk(os.path.join(root, sub)):
   71              for f in files:
   72                  if not f.endswith((".cpp", ".h")):
   73                      continue
   74                  p = os.path.join(dp, f)
   75                  try:
   76                      text = open(p, encoding="utf-8", errors="replace").read()
   77                  except OSError:
   78                      continue
   79                  for m in pat.finditer(text):
   80                      lits = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
   81                      raw = "".join(lits)
   82                      try:
   83                          msgid = bytes(raw, "utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8")
   84                      except Exception:
   85                          msgid = raw
   86                      if not msgid:
   87                          continue
   88                      line = text.count("\n", 0, m.start()) + 1
   89                      found.setdefault(msgid, os.path.relpath(p, root) + ":" + str(line))
   90      return found
   91  
   92  def main():
   93      ap = argparse.ArgumentParser()
   94      ap.add_argument("--es-src", default=os.environ.get("ES_SRC", ""))
   95      ap.add_argument("--upstream", default="", help="the upstream base commit(s) whose catalogue defines the non-fork strings; default: every merge base of HEAD with ES_UPSTREAM_REF (rocknix/master)")
   96      ap.add_argument("--upstream-ref", default=os.environ.get("ES_UPSTREAM_REF", "rocknix/master"), help="the upstream branch the base is derived from (ES_UPSTREAM_REF)")
   97      ap.add_argument("--quiet", action="store_true")
   98      a = ap.parse_args()
   99      if not a.es_src or not os.path.isdir(os.path.join(a.es_src, "es-app", "src")):
  100          print("es-untranslated: --es-src (or ES_SRC) must name an EmulationStation checkout", file=sys.stderr); return 2
  101      po_path = os.path.join(a.es_src, "locale", "lang", "fr", "LC_MESSAGES", "emulationstation2.po")
  102      try:
  103          fr = parse_po(open(po_path, encoding="utf-8").read())
  104      except OSError as e:
  105          print("es-untranslated: cannot read " + po_path + ": " + str(e), file=sys.stderr); return 2
  106      # The base is derived, not remembered (audit #258 PL-022): a constant
  107      # outlives the rebase that moves it, and every string upstream added
  108      # since then is then counted as the fork's. `git merge-base --all` gives
  109      # every base of a criss-cross history; the union of their catalogues is
  110      # what upstream carried. Failing to find one is a check that cannot
  111      # run, not an empty upstream.
  112      bases = [b for b in a.upstream.split(",") if b]
  113      if not bases:
  114          r = subprocess.run(["git", "-C", a.es_src, "merge-base", "--all", "HEAD", a.upstream_ref], capture_output=True, text=True)
  115          if r.returncode != 0 or not r.stdout.strip():
  116              print("es-untranslated: no merge base of HEAD with " + a.upstream_ref + " -- fetch the upstream remote (git remote add rocknix https://github.com/ROCKNIX/emulationstation-next.git; git fetch rocknix master) or pass --upstream <commit>: " + r.stderr.strip(), file=sys.stderr); return 2
  117          bases = r.stdout.split()
  118      upstream_ids = set()
  119      for b in bases:
  120          try:
  121              up = subprocess.run(["git", "-C", a.es_src, "show", b + ":locale/lang/fr/LC_MESSAGES/emulationstation2.po"],
  122                                  capture_output=True, text=True, check=True).stdout
  123          except subprocess.CalledProcessError as e:
  124              print("es-untranslated: cannot read the upstream catalogue at " + b + ": " + e.stderr.strip(), file=sys.stderr); return 2
  125          upstream_ids |= set(parse_po(up).keys())
  126      # Upstream's own source at each base, for the strings its catalogue does not
  127      # carry yet. Extracted with git archive, so a base that cannot be read is a
  128      # check that cannot run, not an upstream with no strings.
  129      import tempfile
  130      upstream_src_ids = set()
  131      for b in bases:
  132          with tempfile.TemporaryDirectory(prefix="es-untranslated-") as tmp:
  133              arc = subprocess.run(["git", "-C", a.es_src, "archive", "--format=tar", b, "es-app/src", "es-core/src"], capture_output=True)
  134              if arc.returncode != 0:
  135                  print("es-untranslated: cannot read the upstream source at " + b + ": " + arc.stderr.decode(errors="replace").strip(), file=sys.stderr); return 2
  136              if subprocess.run(["tar", "-x", "-C", tmp], input=arc.stdout).returncode != 0:
  137                  print("es-untranslated: cannot unpack the upstream source at " + b, file=sys.stderr); return 2
  138              found = source_strings(tmp)
  139              if not found:
  140                  print("es-untranslated: the upstream source at " + b + " has no _() strings -- not a believable base", file=sys.stderr); return 2
  141              upstream_src_ids |= set(found)
  142      print("es-untranslated: upstream base " + ", ".join(b[:9] for b in bases) + (" (merge base of HEAD with " + a.upstream_ref + ")" if not a.upstream else " (given)"))
  143      src = source_strings(a.es_src)
  144      fork = {k: v for k, v in src.items() if k not in upstream_ids and k not in upstream_src_ids}
  145      upstream_untranslated = sorted((v, k) for k, v in src.items() if k in upstream_src_ids and k not in upstream_ids and not fr.get(k))
  146      missing = sorted(((v, k) for k, v in fork.items() if not fr.get(k)), key=lambda t: (t[0].split(":")[0], int(t[0].split(":")[1])))
  147      if not a.quiet:
  148          for where, msgid in missing:
  149              print(where + "\t" + msgid.replace("\n", "\\n"))
  150      print("es-untranslated: %d fork string(s) in the source, %d with French, %d without" % (len(fork), len(fork) - len(missing), len(missing)))
  151      if upstream_untranslated:
  152          print("es-untranslated: %d upstream string(s) not in upstream's catalogue and without French (upstream's, not counted):" % len(upstream_untranslated))
  153          if not a.quiet:
  154              for where, msgid in upstream_untranslated:
  155                  print("  " + where + "\t" + msgid.replace("\n", "\\n"))
  156      return 1 if missing else 0
  157  
  158  if __name__ == "__main__":
  159      sys.exit(main())
  160  
```

## file, whole, at 8ebaf8daad: tools/font-stems

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # font-stems - how sharp a face renders at each pixel size, measured, so the
    6  # widget sizes a panel gets are numbers in the tree rather than a guess
    7  # (fork #255, D-UI-086; the method is #251's solidity.py).
    8  #
    9  #   tools/font-stems <font.ttf> [--sizes 9-32] [--text "..."] [--json] [--no-hinting | --light] [--lib libfreetype.so]
   10  #
   11  # Renders the text with FreeType the way RetroArch's font driver does --
   12  # FT_Set_Pixel_Sizes at a whole number of pixels, FT_LOAD_DEFAULT hinting,
   13  # FT_RENDER_MODE_NORMAL, every glyph composited at an integer pen position
   14  # with its integer advance -- then reads the x-height row of the result:
   15  # a stroke is a maximal run of lit columns, its width is the coverage
   16  # summed across the run, and it has a solid core when one of its columns
   17  # is fully lit (within 12 % of full). A face whose stems land on the grid
   18  # reads sharp; one whose stems fall between two columns is two grey
   19  # half-columns wide and reads soft. The geometric stem of the letter l, in
   20  # em, is printed too: pixel size times that number is where the stems
   21  # would land with no hinting at all.
   22  #
   23  # The host's libfreetype (2.14 on the build box) stands in for the image's
   24  # (2.14.3): the same series, and the five points #251 measured on the
   25  # image's own frames -- 10 px 0.76 / 0 solid of 41, 14 px 1.19 / 16 of 44,
   26  # 15 px 1.40 / 10 of 46, 17 px 1.37 / 21 of 56, 24 px 1.87 / 51 of 56 --
   27  # are what this tool is checked against before its table is believed.
   28  
   29  import ctypes
   30  import ctypes.util
   31  import json
   32  import sys
   33  
   34  FT_LOAD_DEFAULT = 0
   35  FT_LOAD_RENDER = 1 << 2
   36  FT_LOAD_NO_SCALE = 1 << 0
   37  FT_LOAD_NO_HINTING = 1 << 1
   38  FT_LOAD_TARGET_LIGHT = 1 << 16
   39  LOAD_FLAGS = FT_LOAD_RENDER  # --no-hinting / --light change it
   40  
   41  
   42  class FT_Generic(ctypes.Structure):
   43      _fields_ = [("data", ctypes.c_void_p), ("finalizer", ctypes.c_void_p)]
   44  
   45  
   46  class FT_BBox(ctypes.Structure):
   47      _fields_ = [("xMin", ctypes.c_long), ("yMin", ctypes.c_long), ("xMax", ctypes.c_long), ("yMax", ctypes.c_long)]
   48  
   49  
   50  class FT_Vector(ctypes.Structure):
   51      _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
   52  
   53  
   54  class FT_Glyph_Metrics(ctypes.Structure):
   55      _fields_ = [(n, ctypes.c_long) for n in ("width", "height", "horiBearingX", "horiBearingY", "horiAdvance",
   56                                               "vertBearingX", "vertBearingY", "vertAdvance")]
   57  
   58  
   59  class FT_Bitmap(ctypes.Structure):
   60      _fields_ = [("rows", ctypes.c_uint), ("width", ctypes.c_uint), ("pitch", ctypes.c_int),
   61                  ("buffer", ctypes.POINTER(ctypes.c_ubyte)), ("num_grays", ctypes.c_ushort),
   62                  ("pixel_mode", ctypes.c_ubyte), ("palette_mode", ctypes.c_ubyte), ("palette", ctypes.c_void_p)]
   63  
   64  
   65  class FT_GlyphSlotRec(ctypes.Structure):
   66      _fields_ = [("library", ctypes.c_void_p), ("face", ctypes.c_void_p), ("next", ctypes.c_void_p),
   67                  ("glyph_index", ctypes.c_uint), ("generic", FT_Generic), ("metrics", FT_Glyph_Metrics),
   68                  ("linearHoriAdvance", ctypes.c_long), ("linearVertAdvance", ctypes.c_long),
   69                  ("advance", FT_Vector), ("format", ctypes.c_int), ("bitmap", FT_Bitmap),
   70                  ("bitmap_left", ctypes.c_int), ("bitmap_top", ctypes.c_int)]
   71  
   72  
   73  class FT_FaceRec(ctypes.Structure):
   74      _fields_ = [("num_faces", ctypes.c_long), ("face_index", ctypes.c_long), ("face_flags", ctypes.c_long),
   75                  ("style_flags", ctypes.c_long), ("num_glyphs", ctypes.c_long), ("family_name", ctypes.c_char_p),
   76                  ("style_name", ctypes.c_char_p), ("num_fixed_sizes", ctypes.c_int), ("available_sizes", ctypes.c_void_p),
   77                  ("num_charmaps", ctypes.c_int), ("charmaps", ctypes.c_void_p), ("generic", FT_Generic),
   78                  ("bbox", FT_BBox), ("units_per_EM", ctypes.c_ushort), ("ascender", ctypes.c_short),
   79                  ("descender", ctypes.c_short), ("height", ctypes.c_short), ("max_advance_width", ctypes.c_short),
   80                  ("max_advance_height", ctypes.c_short), ("underline_position", ctypes.c_short),
   81                  ("underline_thickness", ctypes.c_short), ("glyph", ctypes.POINTER(FT_GlyphSlotRec)),
   82                  ("size", ctypes.c_void_p), ("charmap", ctypes.c_void_p)]
   83  
   84  
   85  LIB = None  # --lib path: another libfreetype, such as the image sysroot's
   86  
   87  
   88  def load_freetype():
   89      name = LIB or ctypes.util.find_library("freetype") or "libfreetype.so.6"
   90      ft = ctypes.CDLL(name)
   91      ft.FT_Init_FreeType.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
   92      ft.FT_New_Face.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long, ctypes.POINTER(ctypes.POINTER(FT_FaceRec))]
   93      ft.FT_Set_Pixel_Sizes.argtypes = [ctypes.POINTER(FT_FaceRec), ctypes.c_uint, ctypes.c_uint]
   94      ft.FT_Load_Char.argtypes = [ctypes.POINTER(FT_FaceRec), ctypes.c_ulong, ctypes.c_int32]
   95      ft.FT_Library_Version.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
   96      lib = ctypes.c_void_p()
   97      if ft.FT_Init_FreeType(ctypes.byref(lib)):
   98          sys.exit("font-stems: FT_Init_FreeType failed")
   99      a, b, c = ctypes.c_int(), ctypes.c_int(), ctypes.c_int()
  100      ft.FT_Library_Version(lib, a, b, c)
  101      return ft, lib, "%d.%d.%d" % (a.value, b.value, c.value)
  102  
  103  
  104  def render(ft, face, text, px):
  105      """The text at px, as RetroArch draws it: integer pen, integer advance. Returns rows of coverage 0..255 and the baseline row."""
  106      if ft.FT_Set_Pixel_Sizes(face, 0, px):
  107          sys.exit("font-stems: FT_Set_Pixel_Sizes(%d) failed" % px)
  108      height = px * 3
  109      baseline = px * 2
  110      width = px * len(text) + 4 * px
  111      canvas = [[0] * width for _ in range(height)]
  112      pen = px
  113      for ch in text:
  114          if ft.FT_Load_Char(face, ord(ch), LOAD_FLAGS):
  115              continue
  116          slot = face.contents.glyph.contents
  117          bm = slot.bitmap
  118          for r in range(bm.rows):
  119              y = baseline - slot.bitmap_top + r
  120              if y < 0 or y >= height:
  121                  continue
  122              row = canvas[y]
  123              for c in range(bm.width):
  124                  x = pen + slot.bitmap_left + c
  125                  if 0 <= x < width:
  126                      v = bm.buffer[r * bm.pitch + c]
  127                      if v > row[x]:
  128                          row[x] = v
  129          pen += slot.advance.x >> 6
  130      return canvas, baseline
  131  
  132  
  133  def x_height_px(ft, face, px):
  134      ft.FT_Set_Pixel_Sizes(face, 0, px)
  135      if ft.FT_Load_Char(face, ord("x"), LOAD_FLAGS):
  136          return px // 2
  137      return face.contents.glyph.contents.bitmap_top
  138  
  139  
  140  def measure_row(row, lit=25, solid_from=224):
  141      """Strokes along one row: runs of columns lit above the threshold; each run's width is its coverage in pixels; solid when a column is fully lit."""
  142      strokes = []
  143      run = []
  144      for v in row + [0]:
  145          if v > lit:
  146              run.append(v)
  147          elif run:
  148              strokes.append((sum(run) / 255.0, max(run) >= solid_from))
  149              run = []
  150      return strokes
  151  
  152  
  153  def stem_em(ft, face):
  154      """The letter l's advance-free width in em: the stem, for a sans face, with nothing scaled or hinted."""
  155      if ft.FT_Load_Char(face, ord("l"), FT_LOAD_NO_SCALE):
  156          return None
  157      m = face.contents.glyph.contents.metrics
  158      return m.width / float(face.contents.units_per_EM)
  159  
  160  
  161  def main():
  162      args = sys.argv[1:]
  163      if not args or args[0] in ("-h", "--help"):
  164          print(open(__file__).read().split("\n\n")[1].replace("# ", "").replace("#", ""))
  165          return 0
  166      font = args[0]
  167      sizes = range(9, 33)
  168      text = 'RetroAchievements: Logged in as "player" (offline).'
  169      as_json = False
  170      i = 1
  171      while i < len(args):
  172          if args[i] == "--sizes":
  173              lo, hi = args[i + 1].split("-")
  174              sizes = range(int(lo), int(hi) + 1)
  175              i += 2
  176          elif args[i] == "--text":
  177              text = args[i + 1]
  178              i += 2
  179          elif args[i] == "--json":
  180              as_json = True
  181              i += 1
  182          elif args[i] == "--lib":
  183              global LIB
  184              LIB = args[i + 1]
  185              i += 2
  186          elif args[i] == "--no-hinting":
  187              global LOAD_FLAGS
  188              LOAD_FLAGS = FT_LOAD_RENDER | FT_LOAD_NO_HINTING
  189              i += 1
  190          elif args[i] == "--light":
  191              LOAD_FLAGS = FT_LOAD_RENDER | FT_LOAD_TARGET_LIGHT
  192              i += 1
  193          else:
  194              sys.exit("font-stems: unknown argument %s" % args[i])
  195      ft, lib, version = load_freetype()
  196      face = ctypes.POINTER(FT_FaceRec)()
  197      if ft.FT_New_Face(lib, font.encode(), 0, ctypes.byref(face)):
  198          sys.exit("font-stems: cannot open %s" % font)
  199      fam = (face.contents.family_name or b"?").decode(errors="replace")
  200      sty = (face.contents.style_name or b"?").decode(errors="replace")
  201      em = stem_em(ft, face)
  202      out = {"font": font, "family": fam, "style": sty, "freetype": version, "stem_em": em, "text": text, "sizes": []}
  203      for px in sizes:
  204          canvas, baseline = render(ft, face, text, px)
  205          xh = x_height_px(ft, face, px)
  206          # the x-height row: half way up the lower-case letters, where every stem crosses
  207          y = baseline - max(1, xh // 2)
  208          strokes = measure_row(canvas[y])
  209          n = len(strokes)
  210          solid = sum(1 for _, s in strokes if s)
  211          mean = (sum(w for w, _ in strokes) / n) if n else 0.0
  212          out["sizes"].append({"px": px, "strokes": n, "solid": solid, "mean_stem": round(mean, 2),
  213                               "geometric_stem": round(px * em, 2) if em else None})
  214      if as_json:
  215          print(json.dumps(out, indent=1))
  216          return 0
  217      print("%s %s (%s), FreeType %s, l stem %.4f em; text: %s" % (fam, sty, font, version, em or 0, text))
  218      print("%4s %8s %6s %9s %10s  %s" % ("px", "strokes", "solid", "mean_stem", "geometric", "share solid"))
  219      for r in out["sizes"]:
  220          share = (100.0 * r["solid"] / r["strokes"]) if r["strokes"] else 0
  221          print("%4d %8d %6d %9.2f %10s  %3.0f%% %s" % (r["px"], r["strokes"], r["solid"], r["mean_stem"],
  222                ("%.2f" % r["geometric_stem"]) if r["geometric_stem"] is not None else "-", share, "#" * int(share / 5)))
  223      return 0
  224  
  225  
  226  if __name__ == "__main__":
  227      sys.exit(main())
  228  
```

## file, whole, at 8ebaf8daad: tools/frame-diff

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # What changed on the screens a vm-qa run walked, against the frames of the
    6  # last cut the maintainer accepted -- so a visual change nobody meant fails
    7  # the cut instead of waiting for an eye on a handheld (fork #252).
    8  #
    9  # The START NEW GAME arrow in the SAVE STATE MANAGER was reshaped on the
   10  # fifth cut of a series and turned on the eleventh; ten cuts each carried a
   11  # proof that measured the thumbnail it meant to change and nothing else,
   12  # and the arrow sat on every one of their frames. A proof asserts what it
   13  # set out to change. This asserts everything else.
   14  #
   15  #   frame-diff compare <baseline-dir> <run-dir> [--masks F] [--claims F]
   16  #                      [--report F] [--min-pixels N]
   17  #   frame-diff accept  <run-dir> <baseline-dir> --build <id> [--note TEXT]
   18  #   frame-diff boxes   <a.png> <b.png> [--masks F] [--screen NAME]
   19  #
   20  # compare walks every PNG under <run-dir> (relative path = the screen's
   21  # name, e.g. back-up-page/02-back-up-page.png), decodes the run's frame and
   22  # the baseline's, and attributes differences to the claims file. A frame
   23  # the baseline lacks is NEW; one the run lacks is MISSING. A claim names the
   24  # baseline it was written against, a screen glob, a rectangle and its issue,
   25  # and each changed pixel is claimed when a live claim contains it. Claimed
   26  # pixels are attributed before clustering the remainder, so adjacent claims
   27  # can jointly explain a region without accepting their bounding-box gaps
   28  # (#591). Exit 0 when nothing is unclaimed or missing; 1 otherwise; 2 when the
   29  # baseline directory has no BASELINE.txt -- a check that cannot run has not
   30  # passed, and says so rather than staying quiet.
   31  #
   32  # masks: `<screen-glob> x0 y0 x1 y1 <why...>` per line; pixels inside are
   33  # not compared (the clock, a progress bar, a sampler's frames). Rectangles
   34  # are half-open, in the frame's own pixels. Keep them few and explained:
   35  # every masked pixel is one this tool can no longer see.
   36  #
   37  # claims: `<baseline-build|*> <screen-glob> x0 y0 x1 y1 <issue> <what...>`.
   38  # In both files a line that starts with # is a comment; after a rectangle,
   39  # the rest of the line is its reason, kept whole (so `#252` survives).
   40  # A claim against another baseline is stale and ignored, and reported so.
   41  # A whole-frame rectangle claims a NEW screen.
   42  #
   43  # accept copies a run's frames into the baseline directory and writes
   44  # BASELINE.txt (build, source, date). It never deletes claims: the claims
   45  # file is in git, and the person who moves the baseline prunes it.
   46  #
   47  # PNG is read with the stdlib (colour types 2 and 6, 8 bits, all five
   48  # filters, filter 0 on a fast path), so this runs anywhere vm-visual-qa
   49  # does, which writes filter-0 frames.
   50  
   51  import fnmatch
   52  import os
   53  import shutil
   54  import struct
   55  import sys
   56  import time
   57  import zlib
   58  
   59  CELL = 16  # pixels per clustering cell; boxes closer than this merge
   60  
   61  
   62  def read_png(path):
   63      """(width, height, rows) with rows as bytes of RGB triples."""
   64      d = open(path, 'rb').read()
   65      if d[:8] != b'\x89PNG\r\n\x1a\n':
   66          raise ValueError('%s: not a PNG' % path)
   67      p = 8
   68      idat = b''
   69      w = h = depth = ctype = 0
   70      while p < len(d):
   71          n = struct.unpack('>I', d[p:p + 4])[0]
   72          t = d[p + 4:p + 8]
   73          c = d[p + 8:p + 8 + n]
   74          p += 12 + n
   75          if t == b'IHDR':
   76              w, h, depth, ctype = struct.unpack('>IIBB', c[:10])
   77          elif t == b'IDAT':
   78              idat += c
   79          elif t == b'IEND':
   80              break
   81      if depth != 8 or ctype not in (2, 6):
   82          raise ValueError('%s: only 8-bit RGB/RGBA PNG is read (depth %d, colour type %d)' % (path, depth, ctype))
   83      bpp = 4 if ctype == 6 else 3
   84      stride = w * bpp
   85      raw = zlib.decompress(idat)
   86      rows = []
   87      prev = bytearray(stride)
   88      q = 0
   89      for _ in range(h):
   90          f = raw[q]
   91          q += 1
   92          line = raw[q:q + stride]
   93          q += stride
   94          if f == 0:
   95              cur = bytearray(line)
   96          else:
   97              cur = bytearray(line)
   98              if f == 1:
   99                  for i in range(bpp, stride):
  100                      cur[i] = (cur[i] + cur[i - bpp]) & 255
  101              elif f == 2:
  102                  for i in range(stride):
  103                      cur[i] = (cur[i] + prev[i]) & 255
  104              elif f == 3:
  105                  for i in range(stride):
  106                      a = cur[i - bpp] if i >= bpp else 0
  107                      cur[i] = (cur[i] + ((a + prev[i]) >> 1)) & 255
  108              elif f == 4:
  109                  for i in range(stride):
  110                      a = cur[i - bpp] if i >= bpp else 0
  111                      b = prev[i]
  112                      c = prev[i - bpp] if i >= bpp else 0
  113                      pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
  114                      pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
  115                      cur[i] = (cur[i] + pr) & 255
  116              else:
  117                  raise ValueError('%s: PNG filter %d' % (path, f))
  118          prev = cur
  119          if bpp == 4:
  120              rgb = bytearray(w * 3)
  121              rgb[0::3] = cur[0::4]
  122              rgb[1::3] = cur[1::4]
  123              rgb[2::3] = cur[2::4]
  124              rows.append(bytes(rgb))
  125          else:
  126              rows.append(bytes(cur))
  127      return w, h, rows
  128  
  129  
  130  def read_rects(path, with_head):
  131      """Lines `[head] <glob> x0 y0 x1 y1 <tail...>  # note` -> list of dicts."""
  132      out = []
  133      if not path or not os.path.exists(path):
  134          return out
  135      for ln, line in enumerate(open(path), 1):
  136          body = line.strip()
  137          if not body or body.startswith('#'):
  138              continue
  139          parts = body.split()
  140          try:
  141              if with_head:
  142                  head, glob = parts[0], parts[1]
  143                  x0, y0, x1, y1 = map(int, parts[2:6])
  144                  tail = ' '.join(parts[6:]).lstrip('# ')
  145              else:
  146                  head, glob = None, parts[0]
  147                  x0, y0, x1, y1 = map(int, parts[1:5])
  148                  tail = ' '.join(parts[5:]).lstrip('# ')
  149          except (IndexError, ValueError):
  150              sys.exit('%s:%d: cannot read `%s`' % (path, ln, body))
  151          out.append({'head': head, 'glob': glob, 'rect': (x0, y0, x1, y1), 'tail': tail, 'line': ln})
  152      return out
  153  
  154  
  155  def rects_for(screen, rects):
  156      return [r for r in rects if fnmatch.fnmatch(screen, r['glob'])]
  157  
  158  
  159  def inside(rect, x, y):
  160      x0, y0, x1, y1 = rect
  161      return x0 <= x < x1 and y0 <= y < y1
  162  
  163  
  164  def contains(outer, inner):
  165      return outer[0] <= inner[0] and outer[1] <= inner[1] and outer[2] >= inner[2] and outer[3] >= inner[3]
  166  
  167  
  168  def diff_boxes(a, b, masks, claims=(), claim_hits=None):
  169      """Half-open differing boxes; optionally attribute live claims before clustering.
  170  
  171      claim_hits receives each claim's actual changed-pixel extent/count. Its
  172      extent is reporting only: it never grants coverage to a gap. With no
  173      claims this retains the boxes command's original behavior.
  174      """
  175      wa, ha, ra = a
  176      wb, hb, rb = b
  177      if claims and claim_hits is None:
  178          raise ValueError('claim_hits is required when attributing claims')
  179      if (wa, ha) != (wb, hb):
  180          return [(0, 0, max(wa, wb), max(ha, hb), -1)]
  181      cells = {}
  182      for y in range(ha):
  183          la, lb = ra[y], rb[y]
  184          if la == lb:
  185              continue
  186          for x in range(wa):
  187              i = x * 3
  188              if la[i:i + 3] == lb[i:i + 3]:
  189                  continue
  190              if masks and any(inside(m['rect'], x, y) for m in masks):
  191                  continue
  192              who = next((c for c in claims if inside(c['rect'], x, y)), None)
  193              if who is not None:
  194                  # First matching live claim owns overlapping pixels, exactly
  195                  # once. Neither another claim's rectangle nor a cluster's
  196                  # bounding box can make an uncovered pixel disappear.
  197                  hit = claim_hits.get(who['line'])
  198                  if hit is None:
  199                      claim_hits[who['line']] = [x, y, x + 1, y + 1, 1, who]
  200                  else:
  201                      hit[0] = min(hit[0], x)
  202                      hit[1] = min(hit[1], y)
  203                      hit[2] = max(hit[2], x + 1)
  204                      hit[3] = max(hit[3], y + 1)
  205                      hit[4] += 1
  206                  continue
  207              key = (x // CELL, y // CELL)
  208              cell = cells.get(key)
  209              if cell is None:
  210                  cells[key] = [x, y, x, y, 1]
  211              else:
  212                  if x < cell[0]:
  213                      cell[0] = x
  214                  if x > cell[2]:
  215                      cell[2] = x
  216                  if y > cell[3]:
  217                      cell[3] = y
  218                  cell[4] += 1
  219      boxes = []
  220      seen = set()
  221      for key in cells:
  222          if key in seen:
  223              continue
  224          stack = [key]
  225          seen.add(key)
  226          x0, y0, x1, y1, n = cells[key]
  227          while stack:
  228              cx, cy = stack.pop()
  229              for dx in (-1, 0, 1):
  230                  for dy in (-1, 0, 1):
  231                      k = (cx + dx, cy + dy)
  232                      if k in cells and k not in seen:
  233                          seen.add(k)
  234                          stack.append(k)
  235                          c = cells[k]
  236                          x0, y0 = min(x0, c[0]), min(y0, c[1])
  237                          x1, y1 = max(x1, c[2]), max(y1, c[3])
  238                          n += c[4]
  239          boxes.append((x0, y0, x1 + 1, y1 + 1, n))
  240      boxes.sort(key=lambda t: (t[1], t[0]))
  241      return boxes
  242  
  243  
  244  def frames_under(root):
  245      out = {}
  246      for d, _, files in os.walk(root):
  247          for f in files:
  248              if f.lower().endswith('.png'):
  249                  full = os.path.join(d, f)
  250                  out[os.path.relpath(full, root)] = full
  251      return out
  252  
  253  
  254  def baseline_id(base):
  255      p = os.path.join(base, 'BASELINE.txt')
  256      if not os.path.exists(p):
  257          return None
  258      for line in open(p):
  259          if line.startswith('build '):
  260              return line.split(None, 1)[1].strip()
  261      return None
  262  
  263  
  264  def cmd_compare(argv):
  265      opts = {'--masks': None, '--claims': None, '--report': None, '--min-pixels': '1'}
  266      pos = []
  267      i = 0
  268      while i < len(argv):
  269          if argv[i] in opts:
  270              opts[argv[i]] = argv[i + 1]
  271              i += 2
  272          else:
  273              pos.append(argv[i])
  274              i += 1
  275      if len(pos) != 2:
  276          sys.exit(__doc__ or 'frame-diff compare <baseline-dir> <run-dir>')
  277      base, run = pos
  278      bid = baseline_id(base)
  279      if bid is None:
  280          print('frame-diff: no baseline at %s (no BASELINE.txt); accept a run first: frame-diff accept <run-dir>/walks %s --build <id>' % (base, base))
  281          return 2
  282      masks = read_rects(opts['--masks'], with_head=False)
  283      claims = read_rects(opts['--claims'], with_head=True)
  284      stale = [c for c in claims if c['head'] not in ('*', bid)]
  285      live = [c for c in claims if c['head'] in ('*', bid)]
  286      minpx = int(opts['--min-pixels'])
  287      bframes = frames_under(base)
  288      rframes = frames_under(run)
  289      screens = sorted(set(bframes) | set(rframes))
  290      lines = []
  291      unclaimed = 0
  292      claimed = 0
  293      missing = 0
  294      t0 = time.time()
  295      for s in screens:
  296          smasks = rects_for(s, masks)
  297          sclaims = rects_for(s, live)
  298          if s not in rframes:
  299              lines.append('| `%s` | MISSING from the run | | **FAIL** |' % s)
  300              missing += 1
  301              continue
  302          if s not in bframes:
  303              w, h, _ = read_png(rframes[s])
  304              whole = (0, 0, w, h)
  305              who = [c for c in sclaims if contains(c['rect'], whole)]
  306              if who:
  307                  lines.append('| `%s` | NEW screen | %dx%d | claimed by %s |' % (s, w, h, who[0]['tail'] or 'a claim'))
  308                  claimed += 1
  309              else:
  310                  lines.append('| `%s` | NEW screen | %dx%d | **UNCLAIMED** |' % (s, w, h))
  311                  unclaimed += 1
  312              continue
  313          claim_hits = {}
  314          boxes = diff_boxes(read_png(bframes[s]), read_png(rframes[s]), smasks,
  315                             sclaims, claim_hits)
  316          for x0, y0, x1, y1, n, who in sorted(claim_hits.values(), key=lambda hit: (hit[1], hit[0], hit[5]['line'])):
  317              if n < minpx:
  318                  continue
  319              where = 'x %d..%d, y %d..%d' % (x0, x1 - 1, y0, y1 - 1)
  320              lines.append('| `%s` | %s | %d px | claimed by %s |' % (s, where, n, who['tail'] or 'a claim'))
  321              claimed += 1
  322          for (x0, y0, x1, y1, n) in boxes:
  323              if n == -1:
  324                  lines.append('| `%s` | the frame size differs | %dx%d | **UNCLAIMED** |' % (s, x1, y1))
  325                  unclaimed += 1
  326                  continue
  327              if n < minpx:
  328                  continue
  329              where = 'x %d..%d, y %d..%d' % (x0, x1 - 1, y0, y1 - 1)
  330              # Only unclaimed pixels reached clustering. A reported rectangle
  331              # remains half-open in its suggested claim, as before.
  332              lines.append('| `%s` | %s | %d px | **UNCLAIMED** (claim as `%d %d %d %d`) |' % (s, where, n, x0, y0, x1, y1))
  333              unclaimed += 1
  334      dt = time.time() - t0
  335      head = ['# frame-diff', '',
  336              'baseline `%s` (build %s) against `%s`: %d screens in %.0f s.' % (base, bid, run, len(screens), dt),
  337              'masks: %s (%d); claims: %s (%d live, %d stale against another baseline).' % (
  338                  opts['--masks'] or 'none', len(masks), opts['--claims'] or 'none', len(live), len(stale)),
  339              '']
  340      if lines:
  341          head += ['| screen | box | pixels | verdict |', '| --- | --- | --- | --- |'] + lines
  342      else:
  343          head += ['Every walked screen is pixel-identical to the baseline outside the masks.']
  344      verdict = 'PASS' if (unclaimed == 0 and missing == 0) else 'FAIL'
  345      head += ['', '**%s** -- %d box(es) claimed, %d unclaimed, %d screen(s) missing.' % (verdict, claimed, unclaimed, missing)]
  346      for c in stale:
  347          head.append('- stale claim, line %d: against baseline `%s`, this one is `%s`: `%s %s` -- prune it.' % (
  348              c['line'], c['head'], bid, c['glob'], c['tail']))
  349      text = '\n'.join(head) + '\n'
  350      sys.stdout.write(text)
  351      if opts['--report']:
  352          open(opts['--report'], 'w').write(text)
  353      return 0 if verdict == 'PASS' else 1
  354  
  355  
  356  def cmd_boxes(argv):
  357      opts = {'--masks': None, '--screen': 'frame'}
  358      pos = []
  359      i = 0
  360      while i < len(argv):
  361          if argv[i] in opts:
  362              opts[argv[i]] = argv[i + 1]
  363              i += 2
  364          else:
  365              pos.append(argv[i])
  366              i += 1
  367      if len(pos) != 2:
  368          sys.exit('frame-diff boxes <a.png> <b.png> [--masks F] [--screen NAME]')
  369      masks = rects_for(opts['--screen'], read_rects(opts['--masks'], with_head=False))
  370      boxes = diff_boxes(read_png(pos[0]), read_png(pos[1]), masks)
  371      if not boxes:
  372          print('%s vs %s: identical outside %d mask(s)' % (pos[0], pos[1], len(masks)))
  373          return 0
  374      for (x0, y0, x1, y1, n) in boxes:
  375          if n == -1:
  376              print('the frame size differs')
  377          else:
  378              print('box x %d..%d, y %d..%d  (%dx%d, %d px differ)' % (x0, x1 - 1, y0, y1 - 1, x1 - x0, y1 - y0, n))
  379      return 1
  380  
  381  
  382  def cmd_accept(argv):
  383      opts = {'--build': None, '--note': ''}
  384      pos = []
  385      i = 0
  386      while i < len(argv):
  387          if argv[i] in opts:
  388              opts[argv[i]] = argv[i + 1]
  389              i += 2
  390          else:
  391              pos.append(argv[i])
  392              i += 1
  393      if len(pos) != 2 or not opts['--build']:
  394          sys.exit('frame-diff accept <run-dir> <baseline-dir> --build <id> [--note TEXT]')
  395      run, base = pos
  396      frames = frames_under(run)
  397      if not frames:
  398          sys.exit('frame-diff accept: no PNG under %s' % run)
  399      if os.path.isdir(base):
  400          old = baseline_id(base)
  401          keep = os.path.join(os.path.dirname(base.rstrip('/')), 'walk-baseline-%s-%s' % (old or 'unknown', time.strftime('%Y%m%d-%H%M')))
  402          shutil.move(base, keep)
  403          print('previous baseline (build %s) kept at %s' % (old, keep))
  404      os.makedirs(base)
  405      for rel, full in frames.items():
  406          dst = os.path.join(base, rel)
  407          os.makedirs(os.path.dirname(dst), exist_ok=True)
  408          shutil.copy2(full, dst)
  409      with open(os.path.join(base, 'BASELINE.txt'), 'w') as f:
  410          f.write('build %s\nfrom %s\naccepted %s\n' % (opts['--build'], os.path.abspath(run), time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())))
  411          if opts['--note']:
  412              f.write('note %s\n' % opts['--note'])
  413      print('baseline: build %s, %d frames from %s -> %s' % (opts['--build'], len(frames), run, base))
  414      print('the claims file is not touched: prune the claims written against the previous baseline.')
  415      return 0
  416  
  417  
  418  def main():
  419      if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
  420          print(open(__file__).read().split('\n\n')[0].replace('# ', '').replace('#', ''))
  421          return 0
  422      cmd, argv = sys.argv[1], sys.argv[2:]
  423      if cmd == 'compare':
  424          return cmd_compare(argv)
  425      if cmd == 'boxes':
  426          return cmd_boxes(argv)
  427      if cmd == 'accept':
  428          return cmd_accept(argv)
  429      sys.exit('frame-diff: compare | accept | boxes')
  430  
  431  
  432  if __name__ == '__main__':
  433      sys.exit(main())
  434  
```

## file, whole, at 8ebaf8daad: tools/png-blackout

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # png-blackout - paint a rectangle of a PNG black, with the standard library
    6  # only (the build host has no Pillow, and neither does tools/vm-visual-qa).
    7  #
    8  #   tools/png-blackout <in.png> <out.png> <x> <y> <width> <height>
    9  #
   10  # For the frames under docs/qa-frames/: a screendump whose title carries the
   11  # QA account's name is filed with that band painted out rather than not at
   12  # all (the README of each day says where the box is). Handles 8-bit RGB and
   13  # RGBA, non-interlaced, one IDAT stream, which is what QEMU's screendump
   14  # converted by vm-visual-qa produces; anything else is refused, not guessed.
   15  import struct, sys, zlib
   16  
   17  def chunks(data):
   18      pos = 8
   19      while pos < len(data):
   20          (length,) = struct.unpack(">I", data[pos:pos + 4])
   21          kind = data[pos + 4:pos + 8]
   22          yield kind, data[pos + 8:pos + 8 + length]
   23          pos += 12 + length
   24  
   25  def chunk(kind, body):
   26      return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)
   27  
   28  def main():
   29      if len(sys.argv) != 7:
   30          sys.exit(__doc__ or "usage: png-blackout <in> <out> <x> <y> <w> <h>")
   31      src, dst = sys.argv[1], sys.argv[2]
   32      x, y, w, h = (int(v) for v in sys.argv[3:7])
   33      data = open(src, "rb").read()
   34      if data[:8] != b"\x89PNG\r\n\x1a\n":
   35          sys.exit("not a PNG")
   36      ihdr = None; idat = b""; others = []
   37      for kind, body in chunks(data):
   38          if kind == b"IHDR": ihdr = body
   39          elif kind == b"IDAT": idat += body
   40          elif kind == b"IEND": pass
   41          else: others.append((kind, body))
   42      width, height, depth, ctype, comp, filt, interlace = struct.unpack(">IIBBBBB", ihdr)
   43      if depth != 8 or ctype not in (2, 6) or interlace != 0:
   44          sys.exit(f"unsupported PNG: depth {depth}, colour type {ctype}, interlace {interlace}")
   45      bpp = 3 if ctype == 2 else 4
   46      stride = width * bpp
   47      raw = zlib.decompress(idat)
   48      rows = []; prev = bytearray(stride)
   49      for r in range(height):
   50          off = r * (stride + 1)
   51          ftype = raw[off]; line = bytearray(raw[off + 1:off + 1 + stride])
   52          if ftype == 1:
   53              for i in range(bpp, stride): line[i] = (line[i] + line[i - bpp]) & 255
   54          elif ftype == 2:
   55              for i in range(stride): line[i] = (line[i] + prev[i]) & 255
   56          elif ftype == 3:
   57              for i in range(stride):
   58                  left = line[i - bpp] if i >= bpp else 0
   59                  line[i] = (line[i] + ((left + prev[i]) >> 1)) & 255
   60          elif ftype == 4:
   61              for i in range(stride):
   62                  a = line[i - bpp] if i >= bpp else 0; b = prev[i]; c = prev[i - bpp] if i >= bpp else 0
   63                  p = a + b - c; pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
   64                  pred = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
   65                  line[i] = (line[i] + pred) & 255
   66          elif ftype != 0:
   67              sys.exit(f"unsupported filter {ftype} on row {r}")
   68          rows.append(line); prev = line
   69      for r in range(max(0, y), min(height, y + h)):
   70          for c in range(max(0, x), min(width, x + w)):
   71              rows[r][c * bpp:c * bpp + 3] = b"\x00\x00\x00"
   72      out = b"".join(b"\x00" + bytes(row) for row in rows)
   73      png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
   74      for kind, body in others:
   75          if kind in (b"tEXt", b"iTXt", b"zTXt", b"pHYs", b"gAMA", b"sRGB"): png += chunk(kind, body)
   76      png += chunk(b"IDAT", zlib.compress(out, 9)) + chunk(b"IEND", b"")
   77      open(dst, "wb").write(png)
   78      print(f"{dst}: {width}x{height}, {w}x{h} at ({x},{y}) painted out")
   79  
   80  if __name__ == "__main__":
   81      main()
   82  
```

## file, whole, at 8ebaf8daad: tools/qa-accounts

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # qa-accounts - carry a QA test account from the build host into a QA guest,
    6  # so the pages that need a real RetroAchievements or ScreenScraper login can
    7  # be pressed on the VM without a credential ever passing through a chat, a
    8  # commit or a log (D-QA-016, D-INFRA-006's pattern).
    9  #
   10  # The accounts live in ~/.ROCKNIX/qa-accounts, mode 0600, as export lines:
   11  #
   12  #   export RA_QA_USER=...          RetroAchievements test account
   13  #   export RA_QA_PASSWORD=...
   14  #   export RA_QA_WEBKEY=...        its web API key (retroachievements.org > settings)
   15  #   export SS_QA_USER=...          ScreenScraper test account
   16  #   export SS_QA_PASSWORD=...
   17  #   export SS_QA_DEVID=...         a developer pair, if one may be used on the VM
   18  #   export SS_QA_DEVPASSWORD=...
   19  #
   20  #   tools/qa-accounts <ssh-port> ra             # RetroAchievements: system.cfg, live
   21  #   tools/qa-accounts <ssh-port> screenscraper  # ScreenScraper: es_settings.cfg, needs a reboot
   22  #   tools/qa-accounts <ssh-port> clear          # take both back out
   23  #
   24  # Prints the names it set and nothing else. Refuses a file that is not
   25  # 0600, and a port that is not one of the QA guests' (10022-10029).
   26  #
   27  # How a value travels (audit #151 PL-09, after D-INFRA-010): over ssh's
   28  # STDIN, both ways -- never as an argument, so it is in neither host's `ps`
   29  # nor the guest's `sh -c` while this runs. Every report here is what the
   30  # guest holds afterwards, read back, not what was asked: `clear` prints
   31  # `cleared:` only once the ssh has succeeded and the settings read back
   32  # empty; the ScreenScraper writer refuses a file with no `<config>` (a
   33  # missing or already-broken file is an error, not a new invalid file),
   34  # rebuilds beside the original, parses the rebuild on the host, and only
   35  # then puts it in place. `clear` takes out everything `ra` and `screenscraper`
   36  # wrote, and what the interface wrote from them: EmulationStation stores the
   37  # session token as global.retroachievements.token after a login (the page's
   38  # save and NetworkThread), and the guest is not clean while it holds one
   39  # (#166). Not the global.retroachievements switch itself, whose earlier value
   40  # it cannot know, and not the OFFLINE RETROACHIEVEMENTS toggle's keys: those
   41  # are the toggle's, not the account's, and only raofflineproxy-ctl disable
   42  # takes the toggle out with its marker and service. What the account left
   43  # on the guest through the proxy does go (audit #186 PL-13): the proxy's
   44  # folder under /storage/.config -- its cached sign-in with the session
   45  # token, its award queue, its cache -- and PPSSPP's token file, each
   46  # removed and named; the folder only while the toggle is off, since with it
   47  # on the service owns the folder, and then `clear` names what it left and
   48  # why and exits 1: the guest is not clean.
   49  set -uo pipefail
   50  FILE="${QA_ACCOUNTS:-$HOME/.ROCKNIX/qa-accounts}"
   51  PORT="${1:-}"; WHAT="${2:-}"
   52  KEY="${QA_KEY:-/tmp/rocknix-vm-pair/qa-key}"
   53  SSHO=(-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=8 -o BatchMode=yes)
   54  case "${PORT}" in 1002[2-9]) ;; *) echo "qa-accounts: <ssh-port> must be a QA guest's (10022-10029)" >&2; exit 2 ;; esac
   55  case "${WHAT}" in ra|screenscraper|clear) ;; *) echo "qa-accounts: ra, screenscraper or clear" >&2; exit 2 ;; esac
   56  CFG=/storage/.config/emulationstation/es_settings.cfg
   57  # What `ra` writes, and the token the interface writes from it.
   58  RA_KEYS="global.retroachievements.username global.retroachievements.password global.retroachievements.key global.retroachievements.token"
   59  g() { ssh -n -i "${KEY}" -p "${PORT}" "${SSHO[@]}" root@127.0.0.1 "$@"; }        # nothing on stdin
   60  feed() { ssh -i "${KEY}" -p "${PORT}" "${SSHO[@]}" root@127.0.0.1 "$@"; }        # the values, on stdin
   61  parse() { python3 -c 'import xml.etree.ElementTree as E,sys; E.parse(sys.stdin)' 2>/dev/null; }
   62  if [ "${WHAT}" = clear ]; then
   63      g '. /etc/profile; F=/storage/.config/emulationstation/es_settings.cfg; [ -f "$F" ] || exit 3
   64         for k in '"${RA_KEYS}"'; do set_setting $k default; done
   65         sed -i "/name=\"ScreenScraper\(User\|Pass\|DevId\|DevPass\)\"/d" "$F"' >/dev/null
   66      rc=$?
   67      case "${rc}" in
   68          0) ;;
   69          3) echo "qa-accounts: no ${CFG} on :${PORT}; nothing cleared" >&2; exit 1 ;;
   70          *) echo "qa-accounts: clear on :${PORT} did not run (ssh exit ${rc})" >&2; exit 1 ;;
   71      esac
   72      # What the guest holds now. Names only.
   73      left=$(g '. /etc/profile; for k in '"${RA_KEYS}"'; do [ -n "$(get_setting $k)" ] && printf "%s " "$k"; done
   74                grep -o "name=\"ScreenScraper\(User\|Pass\|DevId\|DevPass\)\"" /storage/.config/emulationstation/es_settings.cfg | tr "\n" " "; exit 0') \
   75          || { echo "qa-accounts: could not read :${PORT} back after clear" >&2; exit 1; }
   76      [ -z "${left// /}" ] || { echo "qa-accounts: still set on :${PORT}: ${left}" >&2; exit 1; }
   77      g "cat ${CFG}" | parse || { echo "qa-accounts: ${CFG} on :${PORT} does not parse after clear" >&2; exit 1; }
   78      # The proxy's folder and PPSSPP's token file: removed while the toggle is
   79      # off, named either way. Two lines back, names only.
   80      residue=$(g '. /etc/profile; D=/storage/.config/raofflineproxy; T=/storage/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat
   81          removed=""; kept=""
   82          if [ "$(get_setting global.retroachievements.offlineproxy)" = 1 ]; then
   83              [ -e "$D" ] && kept="$D (offline achievements are on; raofflineproxy-ctl disable first)"
   84          elif [ -e "$D" ]; then
   85              rm -rf "$D" && removed="$D"
   86          fi
   87          if [ -e "$T" ]; then rm -f "$T" && removed="${removed}${removed:+ }$T"; fi
   88          [ -e "$D" ] && [ -z "$kept" ] && kept="$D (could not be removed)"
   89          [ -e "$T" ] && kept="${kept}${kept:+; }$T (could not be removed)"
   90          echo "removed=$removed"; echo "kept=$kept"; exit 0') \
   91          || { echo "qa-accounts: could not read the proxy's folder on :${PORT} after clear" >&2; exit 1; }
   92      removed=$(printf '%s\n' "${residue}" | sed -n 's/^removed=//p'); kept=$(printf '%s\n' "${residue}" | sed -n 's/^kept=//p')
   93      echo "cleared: ${RA_KEYS} ScreenScraperUser ScreenScraperPass ScreenScraperDevId ScreenScraperDevPass${removed:+; removed: ${removed}}"
   94      [ -z "${kept}" ] || { echo "qa-accounts: left on :${PORT}: ${kept}" >&2; exit 1; }
   95      exit 0
   96  fi
   97  [ -f "${FILE}" ] || { echo "qa-accounts: no ${FILE} -- see the header for its shape" >&2; exit 1; }
   98  mode=$(stat -c %a "${FILE}"); [ "${mode}" = "600" ] || { echo "qa-accounts: ${FILE} is mode ${mode}, must be 600" >&2; exit 1; }
   99  # shellcheck disable=SC1090
  100  set -a; . "${FILE}"; set +a
  101  need() { for v in "$@"; do [ -n "${!v:-}" ] || { echo "qa-accounts: ${v} is not set in ${FILE}" >&2; exit 1; }; done; }
  102  oneline() { for v in "$@"; do case "${!v:-}" in *$'\n'*) echo "qa-accounts: ${v} holds a newline; a setting is one line" >&2; exit 1 ;; esac; done; }
  103  if [ "${WHAT}" = ra ]; then
  104      need RA_QA_USER RA_QA_PASSWORD RA_QA_WEBKEY
  105      oneline RA_QA_USER RA_QA_PASSWORD RA_QA_WEBKEY
  106      # key=value lines on stdin; the guest splits at the first = and sets each.
  107      printf '%s\n' "global.retroachievements=1" "global.retroachievements.username=${RA_QA_USER}" \
  108                    "global.retroachievements.password=${RA_QA_PASSWORD}" "global.retroachievements.key=${RA_QA_WEBKEY}" \
  109        | feed '. /etc/profile; while IFS= read -r line; do set_setting "${line%%=*}" "${line#*=}"; done' >/dev/null \
  110        || { echo "qa-accounts: the write to :${PORT} failed" >&2; exit 1; }
  111      # Report what the device holds, not what was intended.
  112      got=$(g '. /etc/profile; for k in global.retroachievements.username global.retroachievements.password global.retroachievements.key; do [ -n "$(get_setting $k)" ] && printf "%s " "$k"; done; exit 0') \
  113          || { echo "qa-accounts: could not read :${PORT} back" >&2; exit 1; }
  114      echo "set on :${PORT}: global.retroachievements=1 ${got}(read by the interface at its next start: reboot the guest)"
  115      case "${got}" in *username*password*key*) exit 0 ;; *) echo "qa-accounts: a value did not land" >&2; exit 1 ;; esac
  116  else
  117      # An account, a developer pair, or both -- whichever the file holds; which
  118      # combinations ScreenScraper accepts is #66's question (#151 PL-06), and
  119      # this writes what it is given. Only the names being written are
  120      # replaced; the other pair's lines stay.
  121      #
  122      # The lines travel over ssh's stdin, never through a second shell's
  123      # quoting: sent as an argument they lost their attribute quotes and left
  124      # es_settings.cfg unparseable, which the interface answered by ignoring
  125      # the whole file (2026-09-13). The guest rebuilds the file beside the
  126      # original and sends the rebuild back; it is parsed here, and only a
  127      # rebuild that parses is moved into place.
  128      xml() { printf '%s' "$1" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/"/\&quot;/g'; }
  129      oneline SS_QA_USER SS_QA_PASSWORD SS_QA_DEVID SS_QA_DEVPASSWORD
  130      lines=""; names=""; drop=""
  131      if [ -n "${SS_QA_USER:-}" ] && [ -n "${SS_QA_PASSWORD:-}" ]; then
  132          lines="$(printf '\t<string name="ScreenScraperUser" value="%s" />\n\t<string name="ScreenScraperPass" value="%s" />' "$(xml "${SS_QA_USER}")" "$(xml "${SS_QA_PASSWORD}")")"
  133          names="ScreenScraperUser ScreenScraperPass"; drop='User\|Pass'
  134      fi
  135      if [ -n "${SS_QA_DEVID:-}" ] && [ -n "${SS_QA_DEVPASSWORD:-}" ]; then
  136          more="$(printf '\t<string name="ScreenScraperDevId" value="%s" />\n\t<string name="ScreenScraperDevPass" value="%s" />' "$(xml "${SS_QA_DEVID}")" "$(xml "${SS_QA_DEVPASSWORD}")")"
  137          lines="${lines}${lines:+
  138  }${more}"; names="${names}${names:+ }ScreenScraperDevId ScreenScraperDevPass"; drop="${drop}${drop:+\|}DevId\|DevPass"
  139      fi
  140      [ -n "${names}" ] || { echo "qa-accounts: neither SS_QA_USER/SS_QA_PASSWORD nor SS_QA_DEVID/SS_QA_DEVPASSWORD is set in ${FILE}" >&2; exit 1; }
  141      printf '%s\n' "${lines}" | feed "F=/storage/.config/emulationstation/es_settings.cfg
  142          grep -q '<config>' \$F 2>/dev/null || exit 3
  143          grep -v '</config>' \$F | grep -v 'name=\"\{0,1\}ScreenScraper\(${drop}\)\"\{0,1\} ' > \$F.new
  144          cat >> \$F.new
  145          echo '</config>' >> \$F.new
  146          cat \$F.new" | parse
  147      st=("${PIPESTATUS[@]}")
  148      case "${st[1]}" in
  149          0) ;;
  150          3) echo "qa-accounts: ${CFG} on :${PORT} has no <config> (missing, or already not a settings file); nothing written" >&2; exit 1 ;;
  151          *) echo "qa-accounts: the write to :${PORT} failed (ssh exit ${st[1]})" >&2; exit 1 ;;
  152      esac
  153      [ "${st[2]}" = 0 ] || { g "rm -f ${CFG}.new"; echo "qa-accounts: the rebuilt es_settings.cfg does not parse; ${CFG} on :${PORT} left as it was" >&2; exit 1; }
  154      g "mv ${CFG}.new ${CFG}" || { echo "qa-accounts: the rebuild parses but could not be put in place on :${PORT}" >&2; exit 1; }
  155      got=$(g 'grep -o "name=\"ScreenScraper[A-Za-z]*\" value=\"[^\"][^\"]*\"" /storage/.config/emulationstation/es_settings.cfg | sed "s/^name=\"//; s/\" value=.*//" | tr "\n" " "; exit 0') \
  156          || { echo "qa-accounts: could not read :${PORT} back" >&2; exit 1; }
  157      echo "es_settings.cfg on :${PORT} now holds, with values: ${got}(the interface reads it at its next start: reboot the guest)"
  158      for n in ${names}; do case " ${got}" in *" ${n} "*) ;; *) echo "qa-accounts: ${n} did not land" >&2; exit 1 ;; esac; done
  159  fi
  160  
```

## file, whole, at 8ebaf8daad: tools/ra-candidate-games

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # ra-candidate-games -- homebrew titles whose first achievements are cheap
    6  # enough to drive, for the offline RetroAchievements runner's candidate pool.
    7  #
    8  # tools/ra-offline-test spends one of the QA account's unearned achievements
    9  # on every PASS, and only one has ever been routed to an award (Tobu's
   10  # Potato-tan Secret, D-RA-006). #211 then asked for two unlocks in a single
   11  # session, which the pool cannot supply at all. Rather than guess at titles,
   12  # this asks RetroAchievements two questions it can answer mechanically:
   13  #
   14  #   * which sets are homebrew -- RA prefixes those titles "~Homebrew~", which
   15  #     is the same population as the freely distributable itch.io releases the
   16  #     fixtures already come from (tools/../rocknix-qa-roms/itch-free-download.sh);
   17  #   * which of their achievements nearly every player has -- NumAwarded over
   18  #     NumDistinctPlayers. An achievement 95% of players hold is one that
   19  #     happens in the first minutes; one 4% hold is a speedrun.
   20  #
   21  # A game with two or more of the former is a candidate for a two-unlock
   22  # session. It is a candidate, not a route: a route nobody has driven to
   23  # `Awarding achievement` is a guard with no observed positive, so the output
   24  # of this tool is where to look, and ra-offline-test's CANDIDATES only grows
   25  # once a route has been seen to work.
   26  #
   27  #   tools/ra-candidate-games [--min-rate 70] [--min-count 2] [--systems 4,6,7]
   28  #
   29  # Credentials come from ~/.ROCKNIX/qa-accounts (RA_QA_WEBKEY, RA_QA_USER) or
   30  # the environment, are sent only to retroachievements.org, and are never
   31  # printed. Responses are cached under the cache dir, so a re-run costs no
   32  # requests; the live calls are paced at RA_MIN_REQUEST_INTERVAL_SECONDS, the
   33  # same 0.3 s courtesy the proxy's client uses, because their docs ask us to
   34  # be reasonable rather than naming a limit.
   35  
   36  from __future__ import annotations
   37  
   38  import argparse
   39  import json
   40  import os
   41  import sys
   42  import time
   43  import urllib.parse
   44  import urllib.request
   45  from pathlib import Path
   46  
   47  API = "https://retroachievements.org/API"
   48  PACE = 0.35  # seconds between calls; see the header
   49  DEFAULT_SYSTEMS = "1,3,4,5,6,7,8,11,15,25"  # what our devices emulate
   50  
   51  # A homebrew set is only useful to us if the ROM runs on a shipped system, so
   52  # the RA console maps to the ES system folder and the extensions that image
   53  # accepts (read from a running GENERIC_X64 image's es_systems.cfg,
   54  # 2026-09-18). A title whose only itch.io download is an HTML5 build, a
   55  # Windows .exe or a PICO-8 cart is not a candidate however cheap its
   56  # achievements are -- which is the check to apply before adding one.
   57  RUNNABLE = {
   58      1:  ("genesis/megadrive", ".bin .gen .md .sg .smd"),
   59      3:  ("snes", ".fig .sfc .smc .swc"),
   60      4:  ("gb", ".gb .gbc"),
   61      5:  ("gba", ".gba"),
   62      6:  ("gbc", ".gb .gbc"),
   63      7:  ("nes", ".nes .unf .unif"),
   64      8:  ("pcengine", ".bin .pce"),
   65      11: ("mastersystem", ".bin .sms"),
   66      15: ("gamegear", ".bin .gg"),
   67      25: ("atari2600", ".a26 .bin"),
   68  }
   69  ACCOUNTS = Path.home() / ".ROCKNIX" / "qa-accounts"
   70  
   71  
   72  def credentials() -> tuple[str, str]:
   73      user, key = os.environ.get("RA_QA_USER"), os.environ.get("RA_QA_WEBKEY")
   74      if not (user and key) and ACCOUNTS.exists():
   75          for line in ACCOUNTS.read_text(encoding="utf-8").splitlines():
   76              line = line.strip().removeprefix("export ").strip()
   77              name, _, value = line.partition("=")
   78              value = value.strip().strip('"').strip("'")
   79              if name == "RA_QA_USER" and not user:
   80                  user = value
   81              elif name == "RA_QA_WEBKEY" and not key:
   82                  key = value
   83      if not (user and key):
   84          print("ra-candidate-games: no RA_QA_USER / RA_QA_WEBKEY (env or "
   85                f"{ACCOUNTS})", file=sys.stderr)
   86          raise SystemExit(2)
   87      return user, key
   88  
   89  
   90  def get(endpoint: str, params: dict, cache: Path, name: str) -> object:
   91      """A cached GET. The cache key never contains the credentials."""
   92      cached = cache / f"{name}.json"
   93      if cached.exists():
   94          try:
   95              return json.loads(cached.read_text(encoding="utf-8"))
   96          except ValueError:
   97              cached.unlink()
   98      user, key = credentials()
   99      query = urllib.parse.urlencode({**params, "y": key, "z": user})
  100      time.sleep(PACE)
  101      # RetroAchievements answers 403 to a request with no user agent of its
  102      # own -- their Connect docs say never to call without one, and the web
  103      # API enforces the same. urllib's default is not enough.
  104      request = urllib.request.Request(
  105          f"{API}/{endpoint}?{query}",
  106          headers={"User-Agent": "ROCKNIX-qa-candidates/1.0 (+https://github.com/ROCKNIX)"},
  107      )
  108      with urllib.request.urlopen(request, timeout=30) as response:
  109          body = response.read().decode("utf-8")
  110      cache.mkdir(parents=True, exist_ok=True)
  111      cached.write_text(body, encoding="utf-8")
  112      return json.loads(body)
  113  
  114  
  115  # How RetroAchievements hashes a ROM, per console. Getting this wrong reads
  116  # as "the set does not know this ROM" when the file is in fact correct: the
  117  # NES rule cost a wrong verdict on Cookie Clicker on 2026-09-18, because its
  118  # .nes carries the 16-byte iNES header that rcheevos strips before hashing.
  119  # Whole-file is the common case; the exceptions are the headers dumpers add.
  120  HASH_RULE = {
  121      7:  ("nes", 16),    # iNES header stripped
  122      3:  ("snes", 512),  # copier header stripped when the file is 512 over a multiple of 1K
  123  }
  124  
  125  
  126  def ra_md5(path: Path, console_id: int) -> str:
  127      """The MD5 RetroAchievements would compute for this file."""
  128      import hashlib
  129      data = path.read_bytes()
  130      rule = HASH_RULE.get(console_id)
  131      if rule:
  132          _, header = rule
  133          if console_id == 7 and data[:4] == b"NES\x1a":
  134              data = data[16:]
  135          elif console_id == 3 and header and len(data) % 1024 == 512:
  136              data = data[512:]
  137      return hashlib.md5(data).hexdigest()
  138  
  139  
  140  def check(game_id: int, path: Path, cache: Path) -> int:
  141      """Does this file carry the set's achievements?"""
  142      detail = get("API_GetGameExtended.php", {"i": game_id}, cache, f"game-{game_id}")
  143      console = int(detail.get("ConsoleID") or 0)
  144      listing = get("API_GetGameHashes.php", {"i": game_id}, cache, f"hashes-{game_id}")
  145      known = listing.get("Results", listing if isinstance(listing, list) else [])
  146      ours = ra_md5(path, console)
  147      print(f"{path.name}")
  148      print(f"  {detail.get('Title')}  [{detail.get('ConsoleName')}]")
  149      print(f"  hashed as RetroAchievements would: {ours}")
  150      for row in known:
  151          their = str(row.get("MD5") or "").lower()
  152          print(f"  {'MATCH  ' if their == ours else '       '}{their}  {str(row.get('Name') or '')[:52]}")
  153      if any(str(row.get("MD5") or "").lower() == ours for row in known):
  154          print("  -> this ROM carries the set")
  155          return 0
  156      print(f"  -> NOT the build the set was made against ({len(known)} known hash(es))")
  157      return 1
  158  
  159  
  160  def main() -> int:
  161      parser = argparse.ArgumentParser(add_help=True)
  162      parser.add_argument("--min-rate", type=int, default=70,
  163                          help="percent of players holding an achievement for it to count as cheap")
  164      parser.add_argument("--min-count", type=int, default=2,
  165                          help="how many such achievements a game needs to be listed")
  166      parser.add_argument("--systems", default=DEFAULT_SYSTEMS)
  167      parser.add_argument("--cache", default=str(Path.home() / ".cache" / "rocknix-ra-candidates"))
  168      parser.add_argument("--limit", type=int, default=0, help="stop after N games (for a quick look)")
  169      parser.add_argument("--check", nargs=2, metavar=("GAME_ID", "FILE"),
  170                          help="does FILE carry that game's achievements? (hashed RA's way)")
  171      args = parser.parse_args()
  172      cache = Path(args.cache)
  173  
  174      if args.check:
  175          return check(int(args.check[0]), Path(args.check[1]), cache)
  176  
  177      homebrew = []
  178      for system in args.systems.split(","):
  179          listing = get("API_GetGameList.php", {"i": system, "f": 1}, cache, f"games-{system}")
  180          if isinstance(listing, list):
  181              homebrew += [g for g in listing if str(g.get("Title", "")).startswith("~Homebrew~")]
  182      print(f"{len(homebrew)} homebrew set(s) on systems {args.systems}", file=sys.stderr)
  183  
  184      rows = []
  185      for index, game in enumerate(sorted(homebrew, key=lambda g: -int(g.get("NumAchievements") or 0)), 1):
  186          if args.limit and index > args.limit:
  187              break
  188          gid = game["ID"]
  189          try:
  190              detail = get("API_GetGameExtended.php", {"i": gid}, cache, f"game-{gid}")
  191          except Exception as exc:
  192              print(f"  (game {gid}: {exc})", file=sys.stderr)
  193              continue
  194          players = int(detail.get("NumDistinctPlayers") or 0)
  195          achievements = (detail.get("Achievements") or {}).values()
  196          if players < 25 or not achievements:
  197              continue  # too few players for a rate to mean anything
  198          cheap = sorted(
  199              ((int(a.get("NumAwarded") or 0) * 100 // players, a) for a in achievements),
  200              key=lambda pair: -pair[0],
  201          )
  202          qualifying = [(rate, a) for rate, a in cheap if rate >= args.min_rate]
  203          if len(qualifying) >= args.min_count:
  204              rows.append((len(qualifying), players, detail, qualifying))
  205          if index % 50 == 0:
  206              print(f"  ...{index}/{len(homebrew)}", file=sys.stderr)
  207  
  208      rows.sort(key=lambda r: (-r[0], -r[1]))
  209      print(f"\n{len(rows)} title(s) with {args.min_count}+ achievements held by "
  210            f"{args.min_rate}%+ of players\n")
  211      for count, players, detail, qualifying in rows:
  212          title = str(detail.get("Title", "")).replace("~Homebrew~ ", "")
  213          folder, extensions = RUNNABLE.get(int(detail.get("ConsoleID") or 0), ("?", "?"))
  214          print(f"{title}  [{detail.get('ConsoleName')}]  game {detail.get('ID')}  "
  215                f"{players} players  {count} cheap of {detail.get('NumAchievements')}")
  216          print(f"    runs as: roms/{folder}   needs an itch.io upload ending {extensions}")
  217          for rate, a in qualifying[:4]:
  218              print(f"    {rate:3d}%  {str(a.get('Points')):>3} pts  {a.get('Title')}  (id {a.get('ID')})")
  219      return 0
  220  
  221  
  222  if __name__ == "__main__":
  223      sys.exit(main())
  224  
```

## file, whole, at 8ebaf8daad: tools/ra-offline-test

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # ra-offline-test - the offline RetroAchievements scenario on a QA guest, end to
    6  # end, with a PASS/FAIL line per assertion (fork #166, D-RA-001/002/004).
    7  #
    8  #   ./tools/ra-offline-test --port 10026 --identity /tmp/rocknix-vm-pair/qa-key \
    9  #       --monitor /tmp/rocknix-qemu-monitor-d.sock --serial /tmp/rocknix-qemu-serial-d.sock
   10  #   ./tools/ra-offline-test ... --control        # the toggle OFF: the same unlock is lost (#162)
   11  #   ./tools/ra-offline-test ... --game bobl      # this game, whatever the account holds
   12  #   ./tools/ra-offline-test ... --frames DIR     # frame exits and the reconnect send card (#465)
   13  #   ./tools/ra-offline-test --list-games         # the candidates, in the order they are tried
   14  #
   15  # What one run does, in order (the proxy on; --control differs where noted):
   16  #
   17  #   1 the three free homebrew titles with RetroAchievements sets
   18  #     (/workspace/artifacts/rocknix-qa-roms, README there) are on the guest, sha256
   19  #     checked; a ROM this had to copy means a reboot, so the interface scans it
   20  #   2 a cheap achievement the QA account has NOT earned is chosen, read from
   21  #     RetroAchievements' own API on the host (the web key from
   22  #     ~/.ROCKNIX/qa-accounts, never printed); all spent, or the API unreachable,
   23  #     is a FAIL that says so -- this never passes over nothing
   24  #   3 the QA account goes on (tools/qa-accounts), the toggle goes on
   25  #     (raofflineproxy-ctl enable; --control: disable), the award queue reads 0
   26  #   4 the game is launched online through EmulationStation's own launch path
   27  #     (POST /launch, the same code as pressing A): logged in, the set loaded,
   28  #     RetroArch talking to 127.0.0.1:8080 (--control: retroachievements.org),
   29  #     and no synthetic "Casual Only" award (D-RA-005)
   30  #   5 the link is cut on the QEMU monitor (set_link net0 off); the guest's
   31  #     eth0 reads down over serial, and the proxy's online_state.json reads
   32  #     false before any key is sent, so the award meets a proxy that already
   33  #     knows it is offline
   34  #   6 the game is driven over the monitor, one press at a time with the route
   35  #     for that title, until RetroArch logs `Awarding achievement <id>`
   36  #     (bounded, 4 min; Tobu's takes about 90 s); the proxy
   37  #     answered `queued_offline` and logged `Queued offline award`
   38  #     (--control: no such word anywhere -- RetroArch is on its own)
   39  #   7 the game is ended with the link still down, through the shipped
   40  #     execute_kill; `raofflineproxy-ctl pending` answers 1 (--control: 0)
   41  #   8 the link comes back; within 90 s the proxy logs `Flush complete ...
   42  #     flushed=1` and leaves its last-flush stamp; pending answers 0
   43  #   9 RetroAchievements' API shows the achievement earned (--control: NOT
   44  #     earned after 90 s -- #162's loss, reproduced); a relaunch online reads
   45  #     one more unlocked (--control: the same count as before)
   46  #  10 cleanup: toggle and RetroAchievements switches back as found, the
   47  #     account cleared, the proxy's folder removed where this turned the proxy
   48  #     on (its sqlite holds the cached session token), the link on
   49  #
   50  # Every guest line this prints goes through the credential filter
   51  # (generic-x64-vm-testing.md) with the account name masked: exec.log carries
   52  # `cheevos_password = "..."` from setsettings.sh, and RetroArch names the
   53  # account on login. Nothing here touches a handheld or a cloud account; the
   54  # only account is the QA RetroAchievements one, and one PASS spends one of
   55  # its cheap achievements (the candidates below are what it has to spend --
   56  # a repeat needs the dedicated account's softcore progress reset. #464 tracks
   57  # reset automation; the manual reset remains the fallback until qualified).
   58  #
   59  # Exit 0 when every assertion passed, 1 otherwise, 2 on usage or a
   60  # precondition that could not be checked. A guest that does not answer, a
   61  # ROM that is not there, a monitor or serial socket that is missing, are
   62  # FAILs before anything runs -- a guard that cannot run has not passed.
   63  set -u
   64  ROOT=$(cd "$(dirname "$0")/.." && pwd)
   65  HOST=root@127.0.0.1; PORT=10026; KEY=/tmp/rocknix-vm-pair/qa-key
   66  MONITOR=/tmp/rocknix-qemu-monitor-d.sock; SERIAL=/tmp/rocknix-qemu-serial-d.sock
   67  ROMS="${ROCKNIX_ARTIFACTS:-/workspace/artifacts}/rocknix-qa-roms"
   68  CONTROL=0; GAME=""; NETDEV=net0; FRAMES=""
   69  ACCOUNTS="${QA_ACCOUNTS:-$HOME/.ROCKNIX/qa-accounts}"
   70  # The three titles (all copied and checked), and the CANDIDATES among them:
   71  # an achievement with a route -- route_<key> below -- that has been driven
   72  # to `Awarding achievement` on a guest, not guessed at. One so far: Tobu's
   73  # hidden song from the title's menu, #166's proof (2026-09-13) and the same
   74  # cadence re-driven in hardcore on a pair guest with the link cut
   75  # (2026-09-14; hardcore because the softcore unlock was spent, and lost on
   76  # purpose: killed before the link came back). Böbl's Dive Ball and Niñoid's
   77  # double jump were tried the same day and are not routed: Böbl's bubble has
   78  # to be sprung over a pillar from a full dive on a timing no blind key
   79  # sequence hit, and Niñoid's tutorial kid did not jump on A, B or Up.
   80  # Adding a candidate means driving its route to the award once and saying
   81  # where; a route nobody has seen reach the unlock is a guard with no
   82  # observed positive.
   83  GAMES="tobu ninoid bobl"
   84  CANDIDATES="tobu"
   85  declare -A SYSTEM=([tobu]=gbc [ninoid]=gb [bobl]=nes)
   86  declare -A GAMEID=([tobu]=15738 [ninoid]=31199 [bobl]=4902)
   87  declare -A ACHID=([tobu]=100359 [ninoid]=474237 [bobl]=111764)
   88  declare -A TITLE=([tobu]="Potato-tan Secret" [ninoid]="Climbing Trees" [bobl]="Go Deeper")
   89  declare -A SRC=([tobu]="tobu/Tobu Tobu Girl Deluxe.gb" [ninoid]="ninoid/Ninoid.gb" [bobl]="bobl/Bobl (v1.2)-unpacked/böbl-1.2.nes")
   90  declare -A DST=([tobu]="/storage/roms/gbc/Tobu Tobu Girl Deluxe.gb" [ninoid]="/storage/roms/gb/Ninoid.gb" [bobl]="/storage/roms/nes/Bobl.nes")
   91  declare -A SHA=([tobu]=0a0e8018dbbc8d7f [ninoid]=a40191c169c68e66 [bobl]=025ec44d0d84ac46)
   92  while [ $# -gt 0 ]; do
   93    case "$1" in
   94      --host) HOST=$2; shift 2 ;;
   95      --port) PORT=$2; shift 2 ;;
   96      --identity) KEY=$2; shift 2 ;;
   97      --monitor) MONITOR=$2; shift 2 ;;
   98      --serial) SERIAL=$2; shift 2 ;;
   99      --roms) ROMS=$2; shift 2 ;;
  100      --netdev) NETDEV=$2; shift 2 ;;
  101      --control) CONTROL=1; shift ;;
  102      --game) GAME=$2; shift 2 ;;
  103      --frames) FRAMES=$2; shift 2 ;;
  104      --list-games) for g in $GAMES; do r=routed; case " $CANDIDATES " in *" $g "*) ;; *) r="no route yet" ;; esac; printf '%-7s %-4s game %-6s achievement %-7s %-18s %s\n' "$g" "${SYSTEM[$g]}" "${GAMEID[$g]}" "${ACHID[$g]}" "${TITLE[$g]}" "$r"; done; exit 0 ;;
  105      -h|--help) sed -n '5,62p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
  106      *) echo "unknown argument: $1" >&2; exit 2 ;;
  107    esac
  108  done
  109  [ -z "$GAME" ] || case " $CANDIDATES " in *" $GAME "*) ;; *) echo "ra-offline-test: --game is one of: $CANDIDATES (--list-games)" >&2; exit 2 ;; esac
  110  SSHO=(-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=8 -o BatchMode=yes -p "$PORT" -i "$KEY")
  111  S() { ssh -n "${SSHO[@]}" "$HOST" "$@"; }
  112  # The serial console: the channel that works with the link down (tools/vm-serial).
  113  # The console's lines end in CRLF; vm-serial strips only the outermost, so
  114  # a second line keeps its \r and "0" reads as "0<CR>" -- the control's
  115  # pending check failed on exactly that (2026-09-14).
  116  SER() { python3 "$ROOT/tools/vm-serial" --socket "$SERIAL" --timeout "${2:-25}" sh "$1" 2>/dev/null | tr -d '\r'; }
  117  MON() { printf '%s\n' "$1" | socat -t 1 - "UNIX-CONNECT:$MONITOR" >/dev/null 2>&1; }
  118  # With --frames: screendumps at an event, 0.6 s apart. Reconnect captures
  119  # start before the address returns; exit captures alone cannot show the
  120  # send card (D-RA-030, #465). A person still reviews the actual pixels.
  121  frames_after_exit() {
  122    [ -n "$FRAMES" ] || return 0
  123    mkdir -p "$FRAMES"; local i result=0
  124    for i in $(seq 1 "${2:-20}"); do "$ROOT/tools/vm-visual-qa" --monitor "$MONITOR" shot "$FRAMES/$1-$i.png" >/dev/null 2>&1 || result=1; sleep 0.6; done
  125    say "frames: $FRAMES/$1-1..${2:-20}.png"
  126    return "$result"
  127  }
  128  # A key on the monitor, held for ms (QEMU's default press is 100 ms; a
  129  # platformer wants longer holds), then a gap so the game sees it released.
  130  press() { MON "sendkey $1 ${2:-120}"; sleep "$(awk -v h="${2:-120}" -v g="${3:-150}" 'BEGIN{printf "%.3f", (h+g)/1000}')"; }
  131  FAILS=0; PASSES=0
  132  check() { if [ "$1" = 0 ]; then echo "  PASS  $2"; PASSES=$((PASSES+1)); else echo "  FAIL  $2"; FAILS=$((FAILS+1)); fi; }
  133  # Nothing read from the guest is printed raw: the account's name is masked
  134  # and any line shaped like a value is dropped (generic-x64-vm-testing.md).
  135  ACCOUNT=""
  136  mask() { grep -v -i -E 'passw|pass=|pass:|token=|key=' | { if [ -n "$ACCOUNT" ]; then sed "s/${ACCOUNT}/<account>/g"; else cat; fi; }; }
  137  say() { echo "  |     $*"; }
  138  now() { date +%s; }
  139  MODE="proxy on"; [ "$CONTROL" = 1 ] && MODE="control: toggle off"
  140  echo "ra-offline-test: guest :$PORT, $MODE, $(date -u '+%Y-%m-%d %H:%M UTC')"
  141  
  142  # --- 0 preconditions: every one a FAIL, none a silent skip ------------------
  143  echo "0  preconditions"
  144  have_all=0
  145  for t in socat curl jq python3 sha256sum; do command -v "$t" >/dev/null 2>&1 || { check 1 "$t on the host"; have_all=1; }; done
  146  [ -S "$MONITOR" ] || { check 1 "monitor socket $MONITOR"; have_all=1; }
  147  [ -S "$SERIAL" ] || { check 1 "serial socket $SERIAL"; have_all=1; }
  148  [ -f "$ACCOUNTS" ] || { check 1 "QA accounts file $ACCOUNTS"; have_all=1; }
  149  for g in $GAMES; do [ -f "$ROMS/${SRC[$g]}" ] || { check 1 "ROM on the host: $ROMS/${SRC[$g]}"; have_all=1; }; done
  150  BUILD=$(S 'sed -n "s/^BUILD_ID=//p" /etc/os-release' 2>/dev/null | tr -d '"' | cut -c1-10)
  151  [ -n "$BUILD" ] || { check 1 "guest :$PORT answers over ssh"; have_all=1; }
  152  [ "$have_all" = 0 ] || { echo; echo "FAILED ($FAILS) -- preconditions; nothing ran"; exit 1; }
  153  check 0 "guest :$PORT answers over ssh (build $BUILD); monitor, serial, ROMs and the accounts file are here"
  154  check "$(S 'test -x /usr/bin/raofflineproxy-ctl'; echo $?)" "/usr/bin/raofflineproxy-ctl is on the image"
  155  check "$(S 'pgrep -x emulationstation >/dev/null && curl -s -o /dev/null -m 5 http://127.0.0.1:1234/ >/dev/null 2>&1'; echo $?)" "EmulationStation is up and its HTTP API answers on the guest's loopback"
  156  ser_up=$(SER 'echo serial-ok' 8)
  157  check "$([ "$ser_up" = serial-ok ]; echo $?)" "the serial console answers"
  158  [ "$FAILS" = 0 ] || { echo; echo "FAILED ($FAILS) -- preconditions; nothing ran"; exit 1; }
  159  # The account's name, for masking, and the web key for the API -- sourced in
  160  # this shell, used in subshells, printed by nothing.
  161  mode=$(stat -c %a "$ACCOUNTS"); [ "$mode" = 600 ] || { check 1 "$ACCOUNTS is mode $mode, must be 600"; echo; echo "FAILED ($FAILS)"; exit 1; }
  162  # shellcheck disable=SC1090
  163  set -a; . "$ACCOUNTS"; set +a
  164  ACCOUNT="${RA_QA_USER:-}"
  165  [ -n "$ACCOUNT" ] && [ -n "${RA_QA_WEBKEY:-}" ] || { check 1 "RA_QA_USER and RA_QA_WEBKEY are set in $ACCOUNTS"; echo; echo "FAILED ($FAILS)"; exit 1; }
  166  
  167  # --- 1 the ROMs ---------------------------------------------------------------
  168  echo "1  the games with RetroAchievements sets are on the guest"
  169  copied=0
  170  for g in $GAMES; do
  171    dst="${DST[$g]}"
  172    # Copy when the file is missing OR carries other bytes: on chain 89 a
  173    # proof's own Ninoid.gb (a different build of the same title) sat at the
  174    # path and the test refused to launch instead of replacing it; the QA
  175    # guest's copy of these three titles is this test's to write.
  176    if [ "$(S "sha256sum '$dst' 2>/dev/null | cut -c1-16")" != "${SHA[$g]}" ]; then
  177      # Over ssh's stdin, not scp: the destination has spaces, and scp's two
  178      # protocols disagree about whether the remote path is quoted.
  179      ssh "${SSHO[@]}" "$HOST" "mkdir -p '$(dirname "$dst")' && cat > '$dst'" < "$ROMS/${SRC[$g]}"
  180      copied=1; say "copied ${SRC[$g]} -> $dst (missing, or other bytes were there)"
  181    fi
  182    got=$(S "sha256sum '$dst' 2>/dev/null | cut -c1-16")
  183    check "$([ "$got" = "${SHA[$g]}" ]; echo $?)" "$g: $dst sha256 ${SHA[$g]}... (got ${got:-none})"
  184  done
  185  [ "$FAILS" = 0 ] || { echo; echo "FAILED ($FAILS) -- a ROM is missing or wrong; nothing launched"; exit 1; }
  186  if [ "$copied" = 1 ]; then
  187    say "a ROM was copied: rebooting so EmulationStation scans it"
  188    S 'systemctl reboot' 2>/dev/null; sleep 8
  189    for i in $(seq 1 60); do S 'pgrep -x emulationstation >/dev/null' 2>/dev/null && break; sleep 3; done; sleep 15
  190    check "$(S 'pgrep -x emulationstation >/dev/null'; echo $?)" "EmulationStation back after the reboot"
  191  fi
  192  
  193  # --- 2 which achievement -------------------------------------------------------
  194  echo "2  a cheap achievement the QA account has not earned"
  195  # RetroAchievements' API, from the host: the account's progress on a game.
  196  # Prints `1 <DateEarned>` or `0` for the id, nothing when the API did not
  197  # answer (an unknown is never read as unearned -- it would launch a run that
  198  # can only end in a route timeout blamed on the route).
  199  earned() {  # game-id achievement-id
  200    # The URL, key and all, reaches curl as a config line on stdin (-K -),
  201    # never as an argument: a value in argv is in every `ps` for the length
  202    # of the request (#151 PL-09's rule; audit #186 PL-14).
  203    printf 'url = "https://retroachievements.org/API/API_GetGameInfoAndUserProgress.php?g=%s&u=%s&y=%s"\n' "$1" "${RA_QA_USER}" "${RA_QA_WEBKEY}" \
  204      | curl -s -m 20 -K - 2>/dev/null \
  205      | jq -r --arg id "$2" 'if (.Achievements|type)=="object" then (if .Achievements[$id].DateEarned then "1 \(.Achievements[$id].DateEarned)" else "0" end) else empty end' 2>/dev/null
  206  }
  207  PICK=""; spent=""; unknown=""
  208  for g in ${GAME:-$CANDIDATES}; do
  209    e=$(earned "${GAMEID[$g]}" "${ACHID[$g]}")
  210    case "$e" in
  211      0) say "$g: ${ACHID[$g]} ${TITLE[$g]} -- not earned"; PICK=$g; break ;;
  212      1*) say "$g: ${ACHID[$g]} ${TITLE[$g]} -- earned on the QA account ${e#1 }"; spent="${spent}${spent:+; }${ACHID[$g]} ${TITLE[$g]} (game ${GAMEID[$g]}, earned ${e#1 })" ;;
  213      *) say "$g: RetroAchievements' API did not answer for game ${GAMEID[$g]}"; unknown="${unknown}${unknown:+, }$g" ;;
  214    esac
  215  done
  216  if [ -z "$PICK" ]; then
  217    if [ -n "$unknown" ]; then check 1 "RetroAchievements' API did not answer for: $unknown -- whether the account has anything left to unlock is unknown, so nothing runs"
  218    else check 1 "the QA account has already earned every achievement this fixture can reach: ${spent} -- reset the dedicated QA account's softcore progress on that game at retroachievements.org and run again (#464 tracks reset automation)"; fi
  219    echo; echo "FAILED ($FAILS) -- no achievement to unlock; nothing launched"; exit 1
  220  fi
  221  check 0 "chosen: $PICK -- ${TITLE[$PICK]} (achievement ${ACHID[$PICK]}, game ${GAMEID[$PICK]}, ${SYSTEM[$PICK]})"
  222  ROM="${DST[$PICK]}"; AID="${ACHID[$PICK]}"; GID="${GAMEID[$PICK]}"
  223  
  224  # --- 3 account and toggle ------------------------------------------------------
  225  echo "3  the QA account on, the toggle $([ "$CONTROL" = 1 ] && echo off || echo on)"
  226  # As found, for the cleanup: the two RetroAchievements switches and the toggle.
  227  RA_WAS=$(S '. /etc/profile; get_setting global.retroachievements'); HC_WAS=$(S '. /etc/profile; get_setting global.retroachievements.hardcore')
  228  TOGGLE_WAS=$(S 'raofflineproxy-ctl status 2>/dev/null | sed -n "s/^enabled=//p"')
  229  say "as found: global.retroachievements=${RA_WAS:-unset} hardcore=${HC_WAS:-unset} toggle enabled=${TOGGLE_WAS:-?}"
  230  WE_ENABLED=0
  231  cleanup() {
  232    echo "10 cleanup"
  233    S 'pgrep -f ^/usr/bin/retroarch >/dev/null && /tmp/ra-offline-kill; sleep 2; pkill -f ^/usr/bin/retroarch 2>/dev/null; rm -f /tmp/ra-offline-kill; true' >/dev/null 2>&1
  234    MON "set_link $NETDEV on"
  235    SER 'nmcli device connect eth0 >/dev/null 2>&1' 30 >/dev/null
  236    for i in $(seq 1 20); do S true 2>/dev/null && break; sleep 3; done
  237    [ -n "${VD_WAS:-}" ] && S "sed -i 's/^video_driver = .*/${VD_WAS}/' /storage/.config/retroarch/retroarch.cfg" >/dev/null 2>&1
  238    if [ "${TOGGLE_WAS:-0}" = 1 ]; then S 'raofflineproxy-ctl enable' >/dev/null 2>&1; else S 'raofflineproxy-ctl disable' >/dev/null 2>&1; fi
  239    [ "$WE_ENABLED" = 1 ] && S 'raofflineproxy-ctl flushed >/dev/null 2>&1; rm -rf /storage/.config/raofflineproxy' >/dev/null 2>&1
  240    if [ "${ACCT_WAS:-0}" = 1 ]; then
  241      "$ROOT/tools/qa-accounts" "$PORT" ra 2>&1 | sed 's/^/  |     put back: /'
  242    else
  243      "$ROOT/tools/qa-accounts" "$PORT" clear 2>&1 | sed 's/^/  |     /'
  244    fi
  245    S ". /etc/profile; set_setting global.retroachievements '${RA_WAS:-default}'; set_setting global.retroachievements.hardcore '${HC_WAS:-default}'" >/dev/null 2>&1
  246    S 'systemctl restart essway' >/dev/null 2>&1
  247    st=$(S 'raofflineproxy-ctl status 2>/dev/null | tr "\n" " "'); link=$(S 'cat /sys/class/net/eth0/operstate 2>/dev/null')
  248    say "left: ${st}eth0=${link:-?} account cleared; global.retroachievements=${RA_WAS:-unset} hardcore=${HC_WAS:-unset} put back"
  249    echo; if [ "$FAILS" = 0 ]; then echo "PASSED ($PASSES)"; else echo "FAILED ($FAILS of $((FAILS+PASSES)))"; fi
  250    [ "$FAILS" = 0 ]
  251  }
  252  # Whether the guest already had an account (the walks' fixture on guest d
  253  # sets one and every walk from START assumes it: the MAIN MENU opens on
  254  # RETROACHIEVEMENTS when signed in). The name is tested for presence, never
  255  # printed; cleanup puts the account back rather than clearing it when it
  256  # was there before (chain 90, 2026-09-29: the clear left the proofs after
  257  # this test starting one row off).
  258  ACCT_WAS=0; [ -n "$(S '. /etc/profile; get_setting global.retroachievements.username' 2>/dev/null)" ] && ACCT_WAS=1
  259  "$ROOT/tools/qa-accounts" "$PORT" ra > /tmp/ra-offline-acct.$$ 2>&1; rc=$?
  260  # qa-accounts prints names and never values (its contract), so its line is
  261  # masked for the account's name but not dropped by the value filter, which
  262  # would eat it on the word "password".
  263  check "$rc" "tools/qa-accounts $PORT ra: $(sed "s/${ACCOUNT}/<account>/g" /tmp/ra-offline-acct.$$ | head -1)"; rm -f /tmp/ra-offline-acct.$$
  264  [ "$rc" = 0 ] || { echo; echo "FAILED ($FAILS) -- no account; nothing launched"; exit 1; }
  265  if [ "$CONTROL" = 1 ]; then
  266    S 'raofflineproxy-ctl disable' >/dev/null 2>&1
  267    st=$(S 'raofflineproxy-ctl status 2>/dev/null | tr "\n" " "')
  268    check "$(case "$st" in *"enabled=0 marker=0 service=inactive"*) echo 0 ;; *) echo 1 ;; esac)" "raofflineproxy-ctl status: ${st}(the toggle off)"
  269    check "$(S 'netstat -ltn 2>/dev/null | grep -q "127\.0\.0\.1:8080 "'; [ $? != 0 ]; echo $?)" "nothing listens on 127.0.0.1:8080"
  270  else
  271    S 'raofflineproxy-ctl enable' >/dev/null 2>&1; WE_ENABLED=1; [ "${TOGGLE_WAS:-0}" = 1 ] && WE_ENABLED=0
  272    st=$(S 'raofflineproxy-ctl status 2>/dev/null | tr "\n" " "')
  273    check "$(case "$st" in *"enabled=1 marker=1 service=active"*) echo 0 ;; *) echo 1 ;; esac)" "raofflineproxy-ctl status: ${st}(the toggle on)"
  274    # The unit is Type=simple, so `status` says active the moment python3 starts;
  275    # the socket appears about a second later (RC 31253072d6: t+1 s). Wait for it,
  276    # bounded, and fail closed if it never comes.
  277    port_rc=1
  278    for _i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  279      S 'netstat -ltn 2>/dev/null | grep -q "127\.0\.0\.1:8080 "' && { port_rc=0; break; }
  280      sleep 1
  281    done
  282    check "$port_rc" "the proxy listens on 127.0.0.1:8080 (waited up to 15 s for the socket)"
  283    p=$(S 'raofflineproxy-ctl pending 2>/dev/null'); prc=$(S 'raofflineproxy-ctl pending >/dev/null 2>&1; echo $?')
  284    check "$([ "$p" = 0 ] && [ "$prc" = 1 ]; echo $?)" "the award queue is empty before the run (pending=${p:-?} exit ${prc:-?})"
  285    S 'rm -f /storage/.config/raofflineproxy/last-flush' >/dev/null 2>&1
  286  fi
  287  [ "$FAILS" = 0 ] || { cleanup; exit 1; }
  288  # Shell-side settings do not update SystemConf's in-memory values. Restart
  289  # before launch so the reconnect UI sees the same toggle the ctl reads.
  290  es_before=$(S 'pidof emulationstation' 2>/dev/null)
  291  S 'systemctl restart essway' >/dev/null 2>&1
  292  es_after=""
  293  for _i in $(seq 1 60); do
  294    es_after=$(S 'pidof emulationstation' 2>/dev/null)
  295    [ -n "$es_after" ] && [ "$es_after" != "$es_before" ] && break
  296    sleep 1
  297  done
  298  check "$([ -n "$es_after" ] && [ "$es_after" != "$es_before" ]; echo $?)" "EmulationStation restarted after account/toggle changes (#465)"
  299  [ "$FAILS" = 0 ] || { cleanup; exit 1; }
  300  # The shipped exit hotkey, extracted from the installed input_sense so the
  301  # signal and its marker are the code under test (tools/emulator-exit-test).
  302  S 'cat > /tmp/ra-offline-kill <<"H"
  303  #!/bin/bash
  304  DEBUG=false; log() { :; }
  305  eval "$(sed -n "/^execute_kill()/,/^}/p" /usr/bin/input_sense)"
  306  execute_kill
  307  H
  308  chmod +x /tmp/ra-offline-kill; pgrep -f ^/usr/bin/retroarch >/dev/null && { /tmp/ra-offline-kill; sleep 3; }; true' >/dev/null 2>&1
  309  # A QEMU guest has no Vulkan. Until a5a03bd9fa the GENERIC_X64 profile
  310  # shipped `video_driver = "vulkan"`: left on it, RetroArch exits with 1
  311  # having pushed no frame, and step 4 stops at "RetroArch running" (guest d
  312  # on 664ad9ac64, 2026-09-25 -- the 2026-09-21 PASS ran on a guest someone
  313  # had left on GL). The profile ships gl now, and the boot quirk
  314  # 092-retroarch-surface moves a cfg still on vulkan to gl while the image
  315  # has no Vulkan driver. time-to-play and the exit test still swap the
  316  # driver for their run, for a guest whose cfg says otherwise; so does this,
  317  # and cleanup puts the guest's own line back.
  318  VD_WAS=$(S 'grep -E "^video_driver" /storage/.config/retroarch/retroarch.cfg' 2>/dev/null)
  319  S "sed -i 's/^video_driver = .*/video_driver = \"gl\"/' /storage/.config/retroarch/retroarch.cfg" >/dev/null 2>&1
  320  
  321  # --- 4 online launch -----------------------------------------------------------
  322  echo "4  the game launched online through the interface"
  323  launch() {  # ROM -> the HTTP status, and RetroArch running
  324    local http; http=$(S "curl -s -o /dev/null -w '%{http_code}' -m 20 -X POST -H 'Content-Type: text/plain' --data '$1' http://127.0.0.1:1234/launch")
  325    echo "$http"
  326  }
  327  wait_log() {  # over ssh: pattern, seconds -> 0 when exec.log has it
  328    local i; for i in $(seq 1 "$2"); do S "grep -q -E '$1' /var/log/exec.log 2>/dev/null" && return 0; sleep 1; done; return 1
  329  }
  330  # A fresh cartridge save, so the route starts where it was written from
  331  # (RetroArch keeps saves beside the ROM on this image: savefiles_in_content_dir).
  332  S "rm -f '${ROM%.*}.srm' '${ROM%.*}.rtc'" >/dev/null 2>&1
  333  # The previous launch's log goes first. runemu.sh writes exec.log afresh
  334  # per launch, but a launch that never happens leaves the old file in place,
  335  # and every log check below would then pass on lines another run wrote --
  336  # which is exactly what happened on 2026-09-21 (run 2 on d55169e59e: POST
  337  # /launch answered 200, RetroArch never appeared, and "logged in",
  338  # "Identified game" and "achievements active" all PASSed from a log three
  339  # hours old). No file, no false pass.
  340  S 'rm -f /var/log/exec.log' >/dev/null 2>&1
  341  # The interface on the carousel first. A page left open by a previous walk
  342  # -- a finished transfer page waiting on A or B, a dialog -- takes the
  343  # launch's 200 and launches nothing (2026-09-21, the same run as above).
  344  # vm-visual-qa's dismiss-dialogs presses B until the screen stops changing.
  345  printf 'dismiss-dialogs\nsettle\n' > /tmp/ra-offline-dismiss.steps
  346  "$ROOT/tools/vm-visual-qa" --monitor "$MONITOR" run /tmp/ra-offline-dismiss.steps --outdir /tmp >/dev/null 2>&1
  347  rm -f /tmp/ra-offline-dismiss.steps
  348  # And the interface idle. After a reboot with a copied ROM the hasher indexes
  349  # it, and HttpServerThread's /launch is refused while ThreadedHasher runs --
  350  # with a 200 and nothing launched (chain 90's run on 8dd6765af0, 2026-09-29:
  351  # the interface's last lines were the index completing). GET /isIdle answers
  352  # [ true ] (200) only when no hasher, scraper, installer, updater or game is
  353  # running; wait for it, bounded, and say how long it took.
  354  idle_wait() {  # seconds -> 0 when /isIdle answered true within them
  355    local i; for i in $(seq 1 "$1"); do
  356      [ "$(S "curl -s -o /dev/null -w '%{http_code}' -m 5 http://127.0.0.1:1234/isIdle" 2>/dev/null)" = 200 ] && { echo "$i"; return 0; }
  357      sleep 1
  358    done; echo "$1"; return 1
  359  }
  360  iw=$(idle_wait 180); say "the interface idle after ${iw} s (GET /isIdle)"
  361  http=$(launch "$ROM")
  362  for i in $(seq 1 45); do S 'pgrep -f ^/usr/bin/retroarch >/dev/null' 2>/dev/null && break; sleep 1; done
  363  if ! S 'pgrep -f ^/usr/bin/retroarch >/dev/null' 2>/dev/null; then
  364    # One more, after the interface says idle again: a launch the interface
  365    # took and dropped (a reload, a dialog it drew after the dismiss) is told
  366    # apart from a launch that cannot work by the second answer, and the
  367    # retry is said, never silent.
  368    iw2=$(idle_wait 60); say "no emulator after the first launch (HTTP ${http:-?}); idle again after ${iw2} s -- launching once more"
  369    http=$(launch "$ROM")
  370    for i in $(seq 1 45); do S 'pgrep -f ^/usr/bin/retroarch >/dev/null' 2>/dev/null && break; sleep 1; done
  371  fi
  372  check "$(S 'pgrep -f ^/usr/bin/retroarch >/dev/null'; echo $?)" "POST /launch $ROM -> HTTP ${http:-?}; RetroArch running"
  373  if ! S 'pgrep -f ^/usr/bin/retroarch >/dev/null' 2>/dev/null; then
  374    # Nothing below can be true without a running emulator; say what the
  375    # interface was doing instead and stop, rather than grade twelve more
  376    # lines against a log that does not exist.
  377    say "the interface's last lines: $(S 'tail -3 /var/log/es_log.txt 2>/dev/null | cut -c1-140' | mask | tr '\n' ' ')"
  378    say "exec.log after the launch: $(S 'ls -la /var/log/exec.log 2>&1 | cut -c1-100')"
  379    [ -n "$FRAMES" ] && "$ROOT/tools/vm-visual-qa" --monitor "$MONITOR" shot "$FRAMES/no-launch.png" >/dev/null 2>&1 && say "frame: $FRAMES/no-launch.png"
  380    cleanup; exit 1
  381  fi
  382  wait_log 'logged in successfully' 60; check $? "RetroArch: logged in"
  383  wait_log "Identified game: $GID " 60; check $? "RetroArch: Identified game: $GID"
  384  wait_log 'achievements active' 30; setline=$(S 'grep -m1 -o -E "Set [0-9]+: [0-9]+/[0-9]+ achievements active" /var/log/exec.log' | mask)
  385  check "$([ -n "$setline" ]; echo $?)" "RetroArch: ${setline:-no 'achievements active' line}"
  386  TOTAL=$(echo "$setline" | sed -n 's/.*: [0-9]*\/\([0-9]*\) achievements.*/\1/p'); ACTIVE0=$(echo "$setline" | sed -n 's/.*: \([0-9]*\)\/[0-9]* achievements.*/\1/p')
  387  hostline=$(S 'grep -m1 -o -E "Using host: [^ ]+" /var/log/exec.log' | mask)
  388  if [ "$CONTROL" = 1 ]; then check "$(case "$hostline" in *retroachievements.org*) echo 0 ;; *) echo 1 ;; esac)" "RetroArch direct: ${hostline:-no 'Using host' line}"
  389  else check "$(case "$hostline" in *127.0.0.1:8080*) echo 0 ;; *) echo 1 ;; esac)" "RetroArch through the proxy: ${hostline:-no 'Using host' line}"; fi
  390  if [ "$CONTROL" = 0 ]; then
  391    sleep 8   # the synthetic award fired five seconds into every proxied session before patch 002
  392    check "$(S 'grep -q "Awarding achievement 101000001" /var/log/exec.log'; [ $? != 0 ]; echo $?)" "no synthetic 'Casual Only' award (101000001) in the session (D-RA-005)"
  393  fi
  394  [ "$FAILS" = 0 ] || { cleanup; exit 1; }
  395  PROXYLOG=/storage/.config/raofflineproxy/service.log
  396  LOG0=$(S "[ -f $PROXYLOG ] && wc -l < $PROXYLOG || echo 0" 2>/dev/null); LOG0=${LOG0:-0}
  397  
  398  # --- 5 the link cut ------------------------------------------------------------
  399  echo "5  the link cut on the monitor"
  400  T_CUT=$(now)
  401  # QEMU link-off can leave an address assigned; the UI watches addresses.
  402  # Disconnect through NetworkManager as well, as an actual Wi-Fi toggle does.
  403  SER 'nmcli device disconnect eth0 >/dev/null 2>&1' 30 >/dev/null
  404  MON "set_link $NETDEV off"
  405  address_state=$(SER 'test -z "$(ip -4 -o addr show dev eth0 scope global)" && echo address-absent' 8)
  406  check "$([ "$address_state" = address-absent ]; echo $?)" "eth0 has no global IPv4 address while disconnected (#465)"
  407  down=1; for i in $(seq 1 10); do [ "$(SER 'cat /sys/class/net/eth0/operstate' 8)" = down ] && { down=0; break; }; sleep 1; done
  408  check "$down" "eth0 operstate=down over serial"
  409  if [ "$CONTROL" = 0 ]; then
  410    off=1; for i in $(seq 1 30); do case "$(SER 'cat /storage/.config/raofflineproxy/online_state.json 2>/dev/null' 8)" in *'"online": false'*|*'"online":false'*) off=0; break ;; esac; sleep 2; done
  411    check "$off" "the proxy's online_state.json reads false ($(( $(now) - T_CUT )) s after the cut)"
  412  fi
  413  [ "$FAILS" = 0 ] || { cleanup; exit 1; }
  414  
  415  # --- 6 the unlock, offline -----------------------------------------------------
  416  echo "6  the game driven over the monitor until the unlock"
  417  # A route is one PRESS per call from wherever the game stands (the loop
  418  # below reads the log after every press, so the award is seen the moment it
  419  # is logged rather than at the end of a pass). RetroArch's keys on the image:
  420  # A = x, B = z, START = ret, SELECT = shift_r, arrows.
  421  ROUTE_STEP=0
  422  route_tobu() {
  423    # The hidden song is heard from the title's MAIN MENU without playing:
  424    # past the "SOUND BY potato-tan" splash and the title with two STARTs
  425    # (a third would start PLAINS), then the left/right carousel -- PLAINS,
  426    # LOCKED entries, SCORES -- six right, six left, four and a half seconds
  427    # on each entry, over and over. #166's proof unlocked it this way by hand
  428    # in about two minutes (2026-09-13); this cadence, re-driven in hardcore
  429    # on a pair guest with the link cut, logged the award at the 18th press,
  430    # 90 s in (2026-09-14). One press per call.
  431    local keys="right right right right right right left left left left left left"
  432    if [ "$ROUTE_STEP" = 0 ]; then press ret 150 2500; press ret 150 2500
  433    else set -- $keys; local i=$(( (ROUTE_STEP - 1) % 12 + 1 )); press "${!i}" 150 4500; fi
  434    ROUTE_STEP=$((ROUTE_STEP+1))
  435  }
  436  awarded=1; T0=$(now)
  437  while [ $(( $(now) - T0 )) -lt 240 ]; do
  438    "route_$PICK"
  439    n=$(SER "grep -c 'Awarding achievement $AID' /var/log/exec.log 2>/dev/null" 10)
  440    [ "${n:-0}" != 0 ] 2>/dev/null && [ "${n:-0}" -gt 0 ] && { awarded=0; break; }
  441  done
  442  T_AWARD=$(now)
  443  line=$(SER "grep -m1 'Awarding achievement $AID' /var/log/exec.log" 10 | mask)
  444  check "$awarded" "RetroArch: ${line:-no 'Awarding achievement '$AID' ...' line within 240 s -- the route for $PICK did not reach it}"
  445  q=$(SER "grep -c 'Achievement $AID: queued_offline' /var/log/exec.log 2>/dev/null" 10)
  446  if [ "$CONTROL" = 0 ]; then
  447    check "$([ "${q:-0}" -gt 0 ] 2>/dev/null; echo $?)" "RetroArch: Achievement $AID: queued_offline (the proxy took it)"
  448    ql=$(SER "grep 'Queued offline award: achievementId=$AID' $PROXYLOG | tail -1" 10 | mask)
  449    check "$([ -n "$ql" ]; echo $?)" "proxy: ${ql#*INFO }"
  450  else
  451    check "$([ "${q:-0}" = 0 ]; echo $?)" "RetroArch: no queued_offline for $AID (no proxy: the award has nowhere to wait)"
  452    err=$(SER "grep -E 'Achievement $AID:|[Ee]rror awarding|award.*fail' /var/log/exec.log | tail -1" 10 | mask)
  453    say "RetroArch's own word on it: ${err:-nothing yet}"
  454  fi
  455  
  456  # --- 7 exit with the link down -------------------------------------------------
  457  echo "7  the game ended with the link still down"
  458  SER '/tmp/ra-offline-kill' 10 >/dev/null
  459  frames_after_exit exit-offline &
  460  gone=1; for i in $(seq 1 30); do [ "$(SER 'pgrep -f ^/usr/bin/retroarch | wc -l' 8)" = 0 ] && { gone=0; break; }; sleep 1; done
  461  wait
  462  check "$gone" "RetroArch gone after execute_kill (the interface's exit path ran with eth0 down)"
  463  check "$([ "$(SER 'pgrep -x emulationstation | wc -l' 8)" = 1 ]; echo $?)" "EmulationStation still up"
  464  p=$(SER 'raofflineproxy-ctl pending 2>/dev/null; echo "rc=$?"' 10); prc=${p##*rc=}; p=${p%%$'\n'*}
  465  if [ "$CONTROL" = 0 ]; then check "$([ "$p" = 1 ] && [ "$prc" = 0 ]; echo $?)" "raofflineproxy-ctl pending = ${p:-?} (exit ${prc:-?}): one award waiting"
  466  else check "$([ "$p" = 0 ] && [ "$prc" = 1 ]; echo $?)" "raofflineproxy-ctl pending = ${p:-?} (exit ${prc:-?}): nothing waits with the toggle off"; fi
  467  
  468  # --- 8 the link back -----------------------------------------------------------
  469  echo "8  the link back"
  470  frames_after_exit reconnect 60 &
  471  reconnect_capture=$!
  472  T_UP=$(now); MON "set_link $NETDEV on"
  473  SER 'nmcli device connect eth0 >/dev/null 2>&1' 30 >/dev/null
  474  for i in $(seq 1 30); do S true 2>/dev/null && break; sleep 2; done
  475  check "$(S true; echo $?)" "ssh back $(( $(now) - T_UP )) s after set_link on"
  476  if [ "$CONTROL" = 0 ]; then
  477    fl=""; for i in $(seq 1 45); do fl=$(S "tail -n +$((LOG0+1)) $PROXYLOG 2>/dev/null | grep -m1 'Flush complete:'" | mask); [ -n "$fl" ] && break; sleep 2; done
  478    fltext="${fl#*INFO }"; [ -n "$fl" ] || fltext="no 'Flush complete' line within 90 s"
  479    check "$(case "$fl" in *"flushed=1"*) echo 0 ;; *) echo 1 ;; esac)" "proxy: ${fltext} ($(( $(now) - T_UP )) s after the link returned)"
  480    # The proxy's stamp is taken by the interface's own send card at the link's
  481    # return (ProxyCards::takeFlushed through the ctl's `flushed`, #305: the
  482    # card that reports the batch removes it), so a `cat` seconds after the
  483    # flush races the card and loses (chain 90, 5b: 'none' with the flush
  484    # complete). Either artifact is the evidence: the stamp seen while it was
  485    # there, or the card's own link stamp saying it was sent after the link
  486    # returned -- /storage/.cache/cloud_sync/last-sync-link, "<epoch> 0 sent".
  487    stamp=""; link=""; ev=""
  488    for i in $(seq 1 25); do
  489      stamp=$(S 'cat /storage/.config/raofflineproxy/last-flush 2>/dev/null'); case "$stamp" in [0-9]*" 1") ev="the last-flush stamp read '${stamp}'"; break ;; esac
  490      link=$(S 'cat /storage/.cache/cloud_sync/last-sync-link 2>/dev/null'); case "$link" in [0-9]*" 0 sent"*) [ "${link%% *}" -ge "$T_UP" ] && { ev="the send card took the stamp and its link stamp reads '${link}'"; break; } ;; esac
  491      sleep 1
  492    done
  493    check "$([ -n "$ev" ]; echo $?)" "the flush left its stamp and it was read or taken: ${ev:-neither the last-flush stamp nor a 'sent' link stamp after the link returned (last-flush '${stamp:-none}', link '${link:-none}')}"
  494    p=$(S 'raofflineproxy-ctl pending 2>/dev/null'); check "$([ "$p" = 0 ]; echo $?)" "raofflineproxy-ctl pending = ${p:-?} after the flush"
  495  fi
  496  wait "$reconnect_capture"
  497  capture_rc=$?
  498  check "$capture_rc" "reconnect capture completed without screenshot errors (#465)"
  499  if [ "$CONTROL" = 0 ] && [ -n "$FRAMES" ]; then
  500    link=$(S 'cat /storage/.cache/cloud_sync/last-sync-link 2>/dev/null')
  501    link_ok=1
  502    case "$link" in [0-9]*" 0 sent"*) [ "${link%% *}" -ge "$T_UP" ] && link_ok=0 ;; esac
  503    check "$link_ok" "the reconnect UI recorded this batch as sent (#465)"
  504  fi
  505  
  506  # --- 9 recorded, or lost -------------------------------------------------------
  507  echo "9  RetroAchievements' answer, and a relaunch online"
  508  if [ "$CONTROL" = 0 ]; then
  509    # earned() answers `1 <DateEarned>` once it is there (the control's `0`
  510    # branch below compares whole; this one compares the first word -- the run
  511    # of 2026-09-14 02:49 failed here on '1 2026-09-14 02:51:28' = 1).
  512    e=""; for i in $(seq 1 9); do e=$(earned "$GID" "$AID"); [ "${e%% *}" = 1 ] && break; sleep 10; done
  513    check "$([ "${e%% *}" = 1 ]; echo $?)" "RetroAchievements' API: achievement $AID earned by the QA account (answer '${e:-none}')"
  514  else
  515    sleep 90; e=$(earned "$GID" "$AID")
  516    check "$([ "$e" = 0 ]; echo $?)" "RetroAchievements' API, 90 s after the link returned: achievement $AID NOT earned (answer '${e:-none}') -- #162's loss"
  517  fi
  518  http=$(launch "$ROM"); for i in $(seq 1 45); do S 'pgrep -f ^/usr/bin/retroarch >/dev/null' 2>/dev/null && break; sleep 1; done
  519  wait_log 'achievements active' 60; setline2=$(S 'grep -m1 -o -E "Set [0-9]+: [0-9]+/[0-9]+ achievements active" /var/log/exec.log' | mask)
  520  ACTIVE1=$(echo "$setline2" | sed -n 's/.*: \([0-9]*\)\/[0-9]* achievements.*/\1/p')
  521  if [ "$CONTROL" = 0 ]; then check "$([ -n "$ACTIVE0" ] && [ -n "$ACTIVE1" ] && [ "$ACTIVE1" = $((ACTIVE0-1)) ]; echo $?)" "relaunch: ${setline2:-?} -- one fewer active than ${ACTIVE0:-?}/${TOTAL:-?} before"
  522  else check "$([ -n "$ACTIVE0" ] && [ -n "$ACTIVE1" ] && [ "$ACTIVE1" = "$ACTIVE0" ]; echo $?)" "relaunch: ${setline2:-?} -- the same ${ACTIVE0:-?}/${TOTAL:-?} active as before: the unlock is not there"; fi
  523  S '/tmp/ra-offline-kill' >/dev/null 2>&1; frames_after_exit exit-online; sleep 3
  524  cleanup
  525  
```

## file, whole, at 8ebaf8daad: tools/ra-ui-test

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated
    4  """Installed reconnect-card proof on a disposable QA guest (Refs #465).
    5  
    6  Synthetic local award/account, installed Storage/flusher/ctl/ES, loopback HTTP.
    7  No real account or award is used. The ordinary provider proof remains separate.
    8  Run under a candidate-bound owner which verifies image/input hashes and cleanup.
    9  """
   10  import argparse
   11  import hashlib
   12  import json
   13  from pathlib import Path
   14  import struct
   15  import subprocess
   16  import time
   17  
   18  GUEST = r'''
   19  import dataclasses,json,sys,time,threading
   20  from pathlib import Path
   21  from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
   22  from urllib.parse import parse_qs,urlsplit
   23  from raofflineproxy import storage,cache_keys,flusher,config
   24  root=Path('/storage/.cache/ra-ui-qa');root.mkdir(exist_ok=True)
   25  assert Path(storage.__file__).is_relative_to('/usr/lib/python3.14/site-packages/')
   26  assert config.CONFIG_DIR==Path('/storage/.config/raofflineproxy')
   27  mode=sys.argv[1]
   28  if mode in ('seed','clear'):
   29      db=config.DATABASE_FILE
   30      assert not db.exists() or (root/'owned').exists(),'refuse preexisting unowned store'
   31      (root/'owned').touch()
   32      for name in [db.name,db.name+'-wal',db.name+'-shm','last-flush']:
   33          (config.CONFIG_DIR/name).unlink(missing_ok=True)
   34      st=storage.Storage()
   35      if mode=='clear':
   36          assert len(st.get_pending_awards())==0
   37          st.close();print('PASS cleared only owned synthetic fixture');sys.exit(0)
   38      st.upsert_cache(cache_keys.login('QA'),json.dumps({'User':'QA','Token':'local-ui-fixture'}))
   39      st.upsert_cache(cache_keys.patch(100,'QA'),json.dumps({'PatchData':{'ID':100,'Title':'Local UI fixture','Achievements':[{'ID':1}]}}))
   40      st.upsert_pending_award({'achievementId':1,'queryString':'/dorequest.php?r=awardachievement&a=1&u=QA&h=0','requestBody':'a=1&u=QA&h=0','userAgent':'Local-UI-QA','queuedAt':int(time.time()*1000)})
   41      assert len(st.get_pending_awards())==1
   42      st.close();print('PASS installed Storage wrote one synthetic softcore award')
   43  elif mode in ('accept','refuse'):
   44      requests=[]
   45      class Provider(BaseHTTPRequestHandler):
   46          def log_message(self,*a): pass
   47          def do_GET(self): self.api(False)
   48          def do_POST(self): self.api(True)
   49          def api(self,post):
   50              p=parse_qs(urlsplit(self.path).query)
   51              if post:p.update(parse_qs(self.rfile.read(int(self.headers.get('Content-Length','0'))).decode()))
   52              action=p.get('r',[''])[0];aid=int(p.get('a',['0'])[0]);game=int(p.get('g',['0'])[0]);code=200
   53              if action=='patch' and game==100:payload={'Success':True,'PatchData':{'ID':100,'Achievements':[{'ID':1}]}}
   54              elif action=='unlocks' and game==100:payload={'Success':True,'UserUnlocks':[]}
   55              elif action=='awardachievement' and aid==1:
   56                  code=200 if mode=='accept' else 503;payload={'Success':mode=='accept'}
   57              else:code=400;payload={'Success':False,'Error':'unexpected local fixture request'}
   58              requests.append({'action':action,'achievement':aid,'game':game,'status':code})
   59              data=json.dumps(payload).encode();self.send_response(code);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
   60      server=ThreadingHTTPServer(('127.0.0.1',0),Provider)
   61      thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
   62      st=storage.Storage()
   63      try:
   64          result=flusher.flush_pending_awards(st,{'upstream_host':f'http://127.0.0.1:{server.server_port}','upload_logs':False,'upload_usage_stats':False})
   65          assert result.flushed==(1 if mode=='accept' else 0)
   66          assert result.pending_remaining==(0 if mode=='accept' else 1)
   67          assert any(r['action']=='awardachievement' for r in requests)
   68          print(json.dumps({'outcome':dataclasses.asdict(result),'requests':requests,'installed_flusher':flusher.__file__}))
   69      finally:
   70          st.close();server.shutdown();server.server_close();thread.join(timeout=5)
   71      assert not thread.is_alive()
   72  else:raise ValueError(mode)
   73  '''
   74  
   75  
   76  def main():
   77      ap = argparse.ArgumentParser(description=__doc__)
   78      ap.add_argument('--identity', required=True)
   79      ap.add_argument('--port', type=int, default=10026)
   80      ap.add_argument('--monitor', required=True)
   81      ap.add_argument('--serial', required=True)
   82      ap.add_argument('--out', type=Path, required=True)
   83      ap.add_argument('--build-id', required=True)
   84      ap.add_argument('--language', choices=['en_US', 'fr_FR'], required=True)
   85      ap.add_argument('--resolution', choices=['640x480', '1280x960'], required=True)
   86      ap.add_argument('--failure-control', action='store_true')
   87      a = ap.parse_args()
   88      a.out.mkdir(parents=True, exist_ok=False)
   89      tools = Path(__file__).resolve().parent
   90      # Sealed owners can provide the immutable distribution tools directory.
   91      import os
   92      tools = Path(os.environ.get('RA_UI_TOOLS', str(tools)))
   93      ssh = ['ssh', '-i', a.identity, '-p', str(a.port), '-o', 'BatchMode=yes',
   94             '-o', 'ConnectTimeout=8', '-o', 'StrictHostKeyChecking=no',
   95             '-o', 'UserKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR', 'root@127.0.0.1']
   96      assertions = []
   97  
   98      def guest(command, check=True, data=None):
   99          return subprocess.run(ssh+[command], input=data, text=True, capture_output=True,
  100                                timeout=75, check=check)
  101  
  102      def check(ok, name):
  103          assertions.append({'assertion': name, 'passed': bool(ok)})
  104          (a.out/'assertions.json').write_text(json.dumps(assertions, indent=2)+'\n')
  105          print(('PASS ' if ok else 'FAIL ')+name, flush=True)
  106          if not ok: raise RuntimeError(name)
  107  
  108      def serial(command):
  109          return subprocess.run([str(tools/'vm-serial'), '--socket', a.serial,
  110                                 '--timeout', '45', 'sh', command], text=True,
  111                                capture_output=True, check=True, timeout=55).stdout.strip().replace('\r','')
  112  
  113      def shot(name):
  114          path = a.out/(name+'.png')
  115          subprocess.run([str(tools/'vm-visual-qa'), '--monitor', a.monitor,
  116                          'shot', str(path)], check=True, stdout=subprocess.DEVNULL, timeout=20)
  117          check(struct.unpack('>II', path.read_bytes()[16:24]) == tuple(map(int, a.resolution.split('x'))), name+' panel dimensions')
  118          return path
  119  
  120      def wait_ssh():
  121          for _ in range(40):
  122              if guest('true', check=False).returncode == 0: return
  123              time.sleep(1)
  124          raise RuntimeError('SSH did not return')
  125  
  126      def link_cycle(label):
  127          serial('nmcli device disconnect eth0 >/dev/null 2>&1; sleep 2; test -z "$(ip -4 -o addr show dev eth0 scope global)" && echo address-absent')
  128          check('address-absent' in serial('test -z "$(ip -4 -o addr show dev eth0 scope global)" && echo address-absent'), label+' actual address removed')
  129          # NetworkStateWatcher samples at five seconds; allow two observations.
  130          time.sleep(12)
  131          serial('nmcli device connect eth0 >/dev/null 2>&1; ip -4 -o addr show dev eth0 scope global | wc -l')
  132          wait_ssh()
  133          check(bool(guest('ip -4 -o addr show dev eth0 scope global').stdout.strip()), label+' actual address restored')
  134  
  135      check(guest('sed -n "s/^BUILD_ID=//p" /etc/os-release').stdout.strip().strip('"') == a.build_id, 'exact candidate BUILD_ID')
  136      check(guest('. /etc/profile >/dev/null 2>&1; test -z "$(get_setting global.retroachievements.username)"', check=False).returncode == 0, 'no configured real account')
  137      check(guest("pgrep -f '^/usr/bin/retroarch'", check=False).returncode == 1, 'no game running before UI proof')
  138      old_es = guest('pidof emulationstation').stdout.strip()
  139      identity_command='sha256sum /usr/bin/emulationstation /usr/bin/raofflineproxy-ctl; find /usr/lib/python3.14/site-packages/raofflineproxy -type f -exec sha256sum {} \\; | sort'
  140      before = guest(identity_command).stdout
  141      check(any('/raofflineproxy/flusher.pyc' in row for row in before.splitlines()) and len(before.splitlines())>20,
  142            'identity census includes installed compiled proxy modules')
  143      (a.out/'installed-before.sha256').write_text(before)
  144      guest('mkdir -p /storage/.cache/ra-ui-qa; cat > /storage/.cache/ra-ui-qa/fixture.py', data=GUEST)
  145      guest('systemctl stop essway; systemctl stop raofflineproxy; . /etc/profile >/dev/null 2>&1; '
  146            'set_setting global.retroachievements 0; set_setting global.retroachievements.offlineproxy 1; '
  147            'set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; set_setting system.language '+a.language)
  148      # A refusal deliberately leaves pending1. Clear the owned synthetic store
  149      # before the next ES restart so no startup card can contaminate that case.
  150      guest('python3 /storage/.cache/ra-ui-qa/fixture.py clear')
  151      check(guest('raofflineproxy-ctl pending', check=False).stdout.strip() == '0',
  152            'profile starts with an empty owned fixture')
  153      # Enable only diagnostics; no renderer override or packaged-code replacement.
  154      guest("python3 - <<'PY'\nfrom pathlib import Path\nimport re\np=Path('/storage/.emulationstation/es_settings.cfg')\ns=p.read_text();s=re.sub(r'<bool name=\"Debug\" value=\"[^\"]*\"\\s*/>', '',s);entry='\\n<bool name=\"Debug\" value=\"true\" />\\n';s=s.replace('</config>',entry+'</config>') if '</config>' in s else s+entry;p.write_text(s)\nPY")
  155      guest('rm -f /storage/.cache/cloud_sync/last-sync-link; systemctl start essway')
  156      for _ in range(90):
  157          r=guest('curl -s -m 3 http://127.0.0.1:1234/isIdle', check=False)
  158          if r.returncode == 0 and r.stdout.strip() == '[ true ]': break
  159          try:
  160              if json.loads(r.stdout)==[True]: break
  161          except ValueError: pass
  162          time.sleep(1)
  163      else: raise RuntimeError('ES not idle after settings reload')
  164      subprocess.run([str(tools/'vm-visual-qa'), '--monitor', a.monitor, 'dismiss'], check=True, stdout=subprocess.DEVNULL)
  165      time.sleep(6)
  166      check(guest('test ! -e /storage/.cache/cloud_sync/last-sync-link', check=False).returncode == 0,
  167            'no startup send outcome before reconnect stimulus')
  168      settings = guest('. /etc/profile >/dev/null 2>&1; test "$(get_setting global.retroachievements.offlineproxy)" = 1 && pidof emulationstation')
  169      check(bool(settings.stdout.strip()) and settings.stdout.strip() != old_es, 'settings loaded by restarted ES')
  170      lifecycle_command="p=$(pidof emulationstation); test -n \"$p\" && awk '{print $1, $22}' /proc/$p/stat"
  171      lifetime=guest(lifecycle_command).stdout.strip()
  172      (a.out/'es-before.txt').write_text(lifetime+'\n')
  173      shot('baseline')
  174      cases = ['accept', 'refuse'] if a.failure_control else ['accept']
  175      for mode in cases:
  176          guest('rm -f /storage/.cache/cloud_sync/last-sync-link; python3 /storage/.cache/ra-ui-qa/fixture.py seed')
  177          check(guest('raofflineproxy-ctl pending').stdout.strip()=='1', mode+' actual ctl pending1')
  178          log_offset=int(guest('wc -l < /var/log/es_log.txt').stdout.strip())
  179          link_cycle(mode)
  180          # Capture while pending is held; the actual flusher has not been invoked.
  181          time.sleep(7)
  182          shot(mode+'-sending')
  183          response=guest('python3 /storage/.cache/ra-ui-qa/fixture.py '+mode).stdout
  184          (a.out/(mode+'-flush.json')).write_text(response)
  185          expected='sent' if mode=='accept' else 'not-sent'
  186          stamp=''
  187          for i in range(60):
  188              stamp=guest('cat /storage/.cache/cloud_sync/last-sync-link 2>/dev/null', check=False).stdout.strip()
  189              if stamp: break
  190              time.sleep(.5)
  191          if mode=='refuse' and not stamp:
  192              for i in range(45):
  193                  stamp=guest('cat /storage/.cache/cloud_sync/last-sync-link 2>/dev/null', check=False).stdout.strip()
  194                  if stamp: break
  195                  time.sleep(.5)
  196          check(len(stamp.split())>=3 and stamp.split()[2]==expected, mode+' UI outcome stamp '+expected)
  197          shot(mode+'-outcome')
  198          (a.out/(mode+'-stamp.txt')).write_text(stamp+'\n')
  199          log=guest('tail -n +'+str(log_offset+1)+' /var/log/es_log.txt | grep -E "ProxyCards:|AsyncNotification" | grep -v -i -E "key|pass|token|user|psk"', check=False).stdout
  200          (a.out/(mode+'-ui.log')).write_text(log)
  201          check('send card ended '+expected in log, mode+' actual UI log matches outcome')
  202          pending=guest('raofflineproxy-ctl pending', check=False).stdout.strip()
  203          check(pending==('0' if mode=='accept' else '1'), mode+' queue state matches outcome')
  204          time.sleep(7)
  205          shot(mode+'-dismissed')
  206          if mode=='accept':
  207              link_cycle('empty repeat')
  208              time.sleep(8)
  209              repeated=guest('cat /storage/.cache/cloud_sync/last-sync-link').stdout.strip()
  210              check(repeated==stamp, 'empty reconnect writes no new send outcome')
  211              shot('empty-repeat')
  212      after=guest(identity_command).stdout
  213      (a.out/'installed-after.sha256').write_text(after)
  214      check(after==before, 'installed ES/ctl/compiled proxy bytes unchanged')
  215      after_lifetime=guest(lifecycle_command).stdout.strip()
  216      (a.out/'es-after.txt').write_text(after_lifetime+'\n')
  217      check(after_lifetime==lifetime, 'same ES PID and start ticks throughout proof')
  218      check(guest("pgrep -f '^/usr/bin/retroarch'", check=False).returncode == 1, 'no game running after UI proof')
  219      check(guest("pgrep -f '^python3 /storage/.cache/ra-ui-qa/fixture.py'", check=False).returncode == 1, 'all local provider/flusher processes exited')
  220      (a.out/'result.json').write_text(json.dumps({'assertions':len(assertions),'failures':0,'language':a.language,'resolution':a.resolution,'fixture':'synthetic local award; installed flusher, ctl and ES','visual_review':'pending','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
  221      print('PASS installed reconnect-card assertions; direct visual review required',flush=True)
  222  
  223  
  224  if __name__=='__main__':
  225      main()
  226  
```

## file, whole, at 8ebaf8daad: tools/raofflineproxy-consent-test

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated
    4  """Prove installed reporting consent in an isolated QA guest with no default route.
    5  
    6  Uses real packaged reporting functions, SQLite and loopback HTTP. Only the log
    7  upload destination constant is redirected; no reporting/consent function is
    8  replaced. Does not prove scheduler timing, UI consent or a real provider.
    9  """
   10  import argparse
   11  import hashlib
   12  import http.server
   13  import importlib
   14  import io
   15  import json
   16  import os
   17  from pathlib import Path
   18  import subprocess
   19  import sys
   20  import threading
   21  import time
   22  import zipfile
   23  
   24  
   25  def save(path, value):
   26      path.write_text(json.dumps(value, indent=2) + '\n')
   27  
   28  
   29  def child(root, name, endpoint, replay, require_early_uptime):
   30      state = root / name
   31      state.mkdir(mode=0o700, exist_ok=replay)
   32      os.environ['RAOFFLINEPROXY_CONFIG_DIR'] = str(state)
   33      os.environ['RAOFFLINEPROXY_USAGE_URL'] = endpoint + '/usage'
   34      modules = {n: importlib.import_module('raofflineproxy.' + n) for n in
   35                 ['config', 'cache_keys', 'storage', 'usage_stats', 'usage_report',
   36                  'storage_corruption', 'log_uploader', 'proxy_service']}
   37      loaded = {}
   38      for name_, module in modules.items():
   39          path = Path(module.__file__).resolve()
   40          if not path.is_relative_to('/usr/lib') or path.suffix != '.pyc':
   41              raise RuntimeError('Refusing non-installed bytecode: ' + str(path))
   42          loaded[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
   43      cfg, stats = modules['config'], modules['usage_stats']
   44      report, corruption = modules['usage_report'], modules['storage_corruption']
   45      uploader, service = modules['log_uploader'], modules['proxy_service']
   46      assert cfg.CONFIG_DIR.resolve() == state.resolve()
   47      uploader.REQUEST_UPLOAD_URL = endpoint + '/request-upload'
   48      # Deliberately synthetic cached sign-in: enough to make reporting eligible.
   49      synthetic_name, synthetic_session = 'QAConsentOnly', 'qa-' + 'only'
   50      store = modules['storage'].Storage()
   51      try:
   52          if not replay:
   53              store.upsert_cache(modules['cache_keys'].login(synthetic_name),
   54                                 json.dumps({'User': synthetic_name, 'Token': synthetic_session}))
   55              assert store.load_login_credentials() is not None
   56              value, version, logs, expected_usage, expected_logs = CASES[name]
   57              data = {'usage_stats_consent_version': version}
   58              if name != 'unanswered':
   59                  data['usage_stats_consent'] = value
   60                  data['upload_logs'] = logs
   61              cfg.save_config(data)
   62              stats.USAGE_STATS_FILE.write_text(json.dumps({'requests_emulator': 7}))
   63              if name == 'explicit-decline':
   64                  stats.save_consent(False)
   65                  assert not stats.USAGE_STATS_FILE.exists(), 'decline did not clear counters'
   66                  # Old on-disk counters must not bypass the consent guard either.
   67                  stats.USAGE_STATS_FILE.write_text(json.dumps({'requests_emulator': 7}))
   68              uptime = time.monotonic()
   69              stats.record_request(stats.SOURCE_EMULATOR, 200)
   70              stats.flush()
   71              actual = stats.snapshot().get('requests_emulator')
   72              expected = 8 if expected_usage else 7
   73              save(root / (name + '-counter-observation.json'),
   74                   {'uptime_seconds': uptime, 'actual': actual, 'expected': expected,
   75                    'installed_modules': loaded})
   76              if require_early_uptime and name == 'usage-only':
   77                  assert uptime < stats.CONSENT_CACHE_SECONDS, ('early boot window missed', uptime)
   78              assert actual == expected, (name, 'counter', actual, expected, 'uptime', uptime)
   79              corrupt_file = state / 'synthetic.json.corrupt-test'
   80              corrupt_file.write_text('{ invalid synthetic state')
   81              cfg.LOG_FILE.write_text('Synthetic QA incident only\n')
   82              corruption.record_incident(corrupt_file, 'synthetic QA incident',
   83                                         corrupt_file.stat().st_size, 1)
   84              assert corruption.load_incident()['reported'] is False
   85          else:
   86              expected_usage = expected_logs = False
   87              assert store.load_login_credentials() is not None
   88          before = corruption.load_incident()
   89          usage_sent = report.report_if_due(store)
   90          assert usage_sent is expected_usage, (name, 'usage result', usage_sent)
   91          service.retry_storage_corruption_report(cfg.load_config())
   92          after = corruption.load_incident()
   93          if expected_logs:
   94              assert after['reported'] is True and after['upload_id'] == 'qa-upload'
   95          else:
   96              assert after == before, 'refused/replayed incident changed'
   97          if expected_usage:
   98              assert stats.last_reported_at() > 0
   99              assert not stats.reportable(stats.snapshot()), 'sent counters not cleared'
  100          save(root / (name + ('-replay' if replay else '') + '-result.json'),
  101               {'case': name, 'replay': replay, 'usage_sent': usage_sent,
  102                'incident_reported': after['reported'], 'installed_modules': loaded})
  103      finally:
  104          store.close()
  105  
  106  
  107  # usage consent, consent version, independent log consent, expected usage/log sends
  108  CASES = {
  109      # Exercise the granted path first so a fast boot can prove #457 directly.
  110      'usage-only': (True, 1, False, True, False),
  111      'unanswered': (None, 1, None, False, False),
  112      'declined': (False, 1, False, False, False),
  113      'null': (None, 1, None, False, False),
  114      'zero': (0, 1, 0, False, False),
  115      'one': (1, 1, 1, False, False),
  116      'string-false': ('false', 1, 'false', False, False),
  117      'string-true': ('true', 1, 'true', False, False),
  118      'list': ([], 1, [], False, False),
  119      'object': ({}, 1, {}, False, False),
  120      'old-grant': (True, 0, False, False, False),
  121      'old-decline': (False, 0, False, False, False),
  122      'explicit-decline': (True, 1, False, False, False),
  123      'logs-only': (False, 1, True, False, True),
  124      'both-enabled': (True, 1, True, True, True),
  125  }
  126  
  127  
  128  def main():
  129      parser = argparse.ArgumentParser(description=__doc__)
  130      parser.add_argument('--output', type=Path, required=True)
  131      parser.add_argument('--expected-build')
  132      parser.add_argument('--case', choices=CASES)
  133      parser.add_argument('--endpoint')
  134      parser.add_argument('--replay', action='store_true')
  135      parser.add_argument('--require-early-uptime', action='store_true',
  136                          help='require the first granted counter before the 30-second cache interval')
  137      args = parser.parse_args()
  138      if args.case:
  139          if not args.endpoint or not args.endpoint.startswith('http://127.0.0.1:'):
  140              parser.error('child requires loopback endpoint')
  141          child(args.output, args.case, args.endpoint, args.replay, args.require_early_uptime)
  142          return 0
  143      identity = dict(line.split('=', 1) for line in Path('/etc/os-release').read_text().splitlines()
  144                      if '=' in line)
  145      if not args.expected_build or identity.get('BUILD_ID', '').strip('"') != args.expected_build:
  146          parser.error('exact expected BUILD_ID required')
  147      for family in ['-4', '-6']:
  148          routes = subprocess.check_output(['ip', family, 'route', 'show', 'default'], text=True)
  149          if routes.strip():
  150              parser.error('remove guest default routes before isolated proof')
  151      root = args.output.resolve()
  152      if not root.is_relative_to('/storage/.cache'):
  153          parser.error('output must be a fresh directory under /storage/.cache')
  154      root.mkdir(mode=0o700, exist_ok=False)
  155      events = []
  156  
  157      class Collector(http.server.BaseHTTPRequestHandler):
  158          def log_message(self, *unused):
  159              pass
  160  
  161          def do_POST(self):
  162              self.receive()
  163  
  164          def do_PUT(self):
  165              self.receive()
  166  
  167          def receive(self):
  168              body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
  169              event = {'method': self.command, 'path': self.path, 'bytes': len(body),
  170                       'sha256': hashlib.sha256(body).hexdigest()}
  171              response, code = b'{}', 200
  172              if self.path == '/usage' and self.command == 'POST':
  173                  payload = json.loads(body)
  174                  assert payload['counters']['requests_emulator'] == 8
  175                  assert b'QAConsentOnly' not in body and b'qa-only' not in body
  176                  event['payload_fields'] = sorted(payload)
  177              elif self.path == '/request-upload' and self.command == 'POST':
  178                  response = json.dumps({'id': 'qa-upload', 'uploadUrl': endpoint + '/upload'}).encode()
  179              elif self.path == '/upload' and self.command == 'PUT':
  180                  with zipfile.ZipFile(io.BytesIO(body)) as archive:
  181                      event['archive_members'] = sorted(archive.namelist())
  182                      assert 'storage_corruption.txt' in archive.namelist()
  183                      assert b'synthetic QA incident' in archive.read('storage_corruption.txt')
  184              else:
  185                  code = 404
  186              events.append(event)
  187              self.send_response(code)
  188              self.send_header('Content-Length', str(len(response)))
  189              self.end_headers()
  190              self.wfile.write(response)
  191  
  192      server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Collector)
  193      endpoint = 'http://127.0.0.1:' + str(server.server_port)
  194      thread = threading.Thread(target=server.serve_forever, daemon=True)
  195      thread.start()
  196      results = []
  197      try:
  198          for name, (_, _, _, usage, logs) in CASES.items():
  199              for replay in [False, True]:
  200                  before = len(events)
  201                  command = [sys.executable, '-I', str(Path(__file__).resolve()), '--output',
  202                             str(root), '--case', name, '--endpoint', endpoint]
  203                  if replay:
  204                      command.append('--replay')
  205                  if args.require_early_uptime:
  206                      command.append('--require-early-uptime')
  207                  run = subprocess.run(command, text=True, capture_output=True, timeout=45)
  208                  (root / (name + ('-replay' if replay else '') + '.log')).write_text(run.stdout + run.stderr)
  209                  assert run.returncode == 0, (name, replay, run.returncode)
  210                  observed = [(e['method'], e['path']) for e in events[before:]]
  211                  expected = [] if replay else ([('POST', '/usage')] if usage else []) + (
  212                      [('POST', '/request-upload'), ('PUT', '/upload')] if logs else [])
  213                  assert observed == expected, (name, replay, observed, expected)
  214                  results.append({'case': name, 'replay': replay, 'requests': len(observed)})
  215                  save(root / 'collector-events.json', events)
  216                  print('PASS', name, 'restart' if replay else 'first call', len(observed), 'HTTP requests', flush=True)
  217          save(root / 'summary.json', {'build_id': args.expected_build, 'checks': len(results),
  218                                      'results': results, 'external_provider_contact': False,
  219                                      'required_early_uptime': args.require_early_uptime,
  220                                      'scope': 'Installed reporting functions and actual loopback HTTP; no scheduler/UI proof'})
  221      finally:
  222          save(root / 'collector-events.json', events)
  223          server.shutdown()
  224          server.server_close()
  225          thread.join(timeout=5)
  226      return 0
  227  
  228  
  229  if __name__ == '__main__':
  230      sys.exit(main())
  231  
```

## file, whole, at 8ebaf8daad: tools/raofflineproxy-installed-native-test

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated (https://github.com/pixelelated)
    4  """Run unchanged upstream hashing tests against the image's installed proxy."""
    5  import argparse
    6  import hashlib
    7  import importlib.util
    8  import json
    9  from pathlib import Path
   10  import runpy
   11  import sys
   12  import types
   13  import unittest
   14  
   15  parser = argparse.ArgumentParser(description=__doc__)
   16  parser.add_argument('--tests', required=True, type=Path)
   17  parser.add_argument('--legacy-chd', required=True, type=Path)
   18  parser.add_argument('--library-sha256', required=True)
   19  parser.add_argument('--output', required=True, type=Path)
   20  args = parser.parse_args()
   21  
   22  import raofflineproxy
   23  from raofflineproxy import rom_browser, rom_hashing
   24  modules = {}
   25  for module in (rom_browser, rom_hashing):
   26      path = Path(module.__file__).resolve()
   27      if not str(path).startswith('/usr/lib/python') or '/site-packages/raofflineproxy/' not in str(path):
   28          sys.exit('refusing a proxy module outside the installed image: '+str(path))
   29      modules[module.__name__] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
   30  lib = rom_hashing.load_rchash()
   31  if lib is None:
   32      sys.exit('installed native library unavailable: '+str(rom_hashing._LIBRCHASH_ERROR))
   33  mapped = {line.split()[-1] for line in Path('/proc/self/maps').read_text().splitlines()
   34            if 'libraproxy_rchash.so' in line}
   35  if mapped != {'/usr/lib/libraproxy_rchash.so'}:
   36      sys.exit('unexpected native library mappings: '+repr(mapped))
   37  library = Path(next(iter(mapped)))
   38  digest = hashlib.sha256(library.read_bytes()).hexdigest()
   39  if digest != args.library_sha256:
   40      sys.exit('installed library differs from the accepted image')
   41  
   42  # Upstream imports linux.raofflineproxy from its repository layout. Bind that
   43  # namespace to these already-verified installed modules; do not copy product
   44  # source over the image or edit the upstream test file (#547).
   45  linux = types.ModuleType('linux')
   46  linux.__path__ = []
   47  linux.raofflineproxy = raofflineproxy
   48  sys.modules['linux'] = linux
   49  sys.modules['linux.raofflineproxy'] = raofflineproxy
   50  sys.modules['linux.raofflineproxy.rom_browser'] = rom_browser
   51  sys.modules['linux.raofflineproxy.rom_hashing'] = rom_hashing
   52  spec = importlib.util.spec_from_file_location('installed_native_test', args.tests)
   53  module = importlib.util.module_from_spec(spec)
   54  spec.loader.exec_module(module)
   55  assert module.rom_browser is rom_browser and module.rom_hashing is rom_hashing
   56  suite = unittest.defaultTestLoader.loadTestsFromModule(module)
   57  count = suite.countTestCases()
   58  if count == 0:
   59      sys.exit('upstream test discovery returned no cases')
   60  result = unittest.TextTestRunner(verbosity=2).run(suite)
   61  report = {'tests_discovered': count, 'tests_run': result.testsRun,
   62            'failures': len(result.failures), 'errors': len(result.errors),
   63            'skipped': len(result.skipped), 'modules': modules,
   64            'library': str(library), 'library_sha256': digest,
   65            'tests_sha256': hashlib.sha256(args.tests.read_bytes()).hexdigest()}
   66  report['legacy_chd'] = runpy.run_path(str(args.legacy_chd))['exercise'](lib)
   67  args.output.write_text(json.dumps(report, indent=2)+'\n')
   68  if result.testsRun != count or not result.wasSuccessful() or result.skipped:
   69      sys.exit('installed native tests failed or skipped; see retained report')
   70  print('PASS all %d installed native cases and legacy CHD controls; no skips' % count)
   71  
```

## file, whole, at 8ebaf8daad: tools/raofflineproxy-integration-test

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  """Exercise the shipped preparation helper against an unpacked patched proxy (#361).
    5  
    6  Uses actual queue/storage/helper code and synthetic game/HTTP boundaries. No
    7  personal account or provider is contacted. Image/service qualification is separate.
    8  """
    9  import argparse
   10  import contextlib
   11  import importlib.machinery
   12  import importlib.util
   13  import io
   14  import json
   15  import os
   16  from pathlib import Path
   17  import subprocess
   18  import sys
   19  import tempfile
   20  import unittest
   21  from unittest import mock
   22  
   23  ROOT = Path(__file__).resolve().parent.parent
   24  parser = argparse.ArgumentParser(description=__doc__)
   25  parser.add_argument('--source', type=Path, required=True, help='patched source containing linux/')
   26  parser.add_argument('--helper', type=Path, default=ROOT/'projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed')
   27  parser.add_argument('--predecessor-source', type=Path, required=True, help='actual older patched source containing linux/')
   28  args = parser.parse_args()
   29  config = tempfile.TemporaryDirectory(prefix='proxy-integration-')
   30  os.environ['RAOFFLINEPROXY_CONFIG_DIR'] = config.name
   31  sys.path[:0] = [str(args.source.resolve()), str(args.source.resolve()/'linux')]
   32  from linux.tests.test_linux_caching_queue import QueueTestCase, CREDENTIALS
   33  from linux.raofflineproxy import cache_budget, cache_keys, cache_queue, image_cache, rate_limit, rom_browser, rom_cache, storage
   34  # Upstream fixtures import linux.raofflineproxy; the shipped helper imports
   35  # raofflineproxy. Both must exercise the same module objects and real store.
   36  for name, value in list(sys.modules.items()):
   37      if name.startswith('linux.raofflineproxy'):
   38          sys.modules[name.removeprefix('linux.')] = value
   39  loader = importlib.machinery.SourceFileLoader('fork_preparation', str(args.helper.resolve()))
   40  spec = importlib.util.spec_from_loader(loader.name, loader)
   41  helper = importlib.util.module_from_spec(spec)
   42  loader.exec_module(helper)
   43  
   44  
   45  class PreparationCadence(unittest.TestCase):
   46      def test_existing_pause_boundaries_survive_removed_upstream_helper(self):
   47          # WholeLibrary mocks this boundary to exercise125 games quickly. Check
   48          # the real compatibility helper too, without waiting a minute in QA.
   49          with mock.patch.object(helper.time, 'sleep') as sleep, \
   50                  contextlib.redirect_stderr(io.StringIO()):
   51              paused = [count for count in range(126)
   52                        if helper.apply_scan_batch_cooldown(count)]
   53          self.assertEqual([50, 100], paused)
   54          self.assertEqual([mock.call(30.0), mock.call(30.0)], sleep.call_args_list)
   55  
   56  
   57  class WholeLibrary(QueueTestCase):
   58      def prepare(self, kind, count=125):
   59          paths = self.roms(*(str(i) for i in range(1,count+1)))
   60          self.game_ids.update({str(i):i for i in range(1,count+1)})
   61          jobs = self.root/'jobs.tsv'
   62          jobs.write_text(''.join(f'I\t{i}\t{i}\t{p}\n' if kind=='I' else f'H\t\t\t{p}\n'
   63                                  for i,p in enumerate(paths,1)))
   64          output = io.StringIO()
   65          with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()), \
   66                  mock.patch.object(sys,'argv',[str(args.helper),str(jobs)]), \
   67                  mock.patch.object(helper,'Storage',return_value=self.store), \
   68                  mock.patch.object(self.store,'close'), \
   69                  mock.patch.object(helper,'configure_logging'), \
   70                  mock.patch.object(helper,'load_config',return_value={}), \
   71                  mock.patch.object(helper,'resolve_credentials',return_value=CREDENTIALS), \
   72                  mock.patch.object(helper,'cache_game',side_effect=self.fake_cache_game), \
   73                  mock.patch.object(helper,'apply_scan_batch_cooldown') as cooldown, \
   74                  mock.patch.object(helper,'wait_for_badges'):
   75              self.assertEqual(0,helper.main())
   76          self.assertEqual(list(range(count)),[c.args[0] for c in cooldown.call_args_list])
   77          return output.getvalue()
   78  
   79      def assert_ready(self, output, count=125):
   80          self.assertEqual(count,sum(line.startswith('OK ') for line in output.splitlines()))
   81          self.assertEqual(count,len(self.store.cache_keys_by_prefix(cache_keys.PREFIX_PATCH)))
   82          self.assertEqual(0,cache_queue.count(self.store))
   83          for i in range(1,count+1):
   84              entry=self.store.get_cache(cache_keys.patch(i,CREDENTIALS['user']))
   85              self.assertEqual(f'/roms/{i}.nes',entry['sourceRomPath'])
   86              alias=self.store.get_cache(cache_keys.game_id(str(i)))
   87              self.assertEqual(i,json.loads(alias['responseBody'])['GameID'])
   88  
   89      def test_unindexed_125_games_are_cached_not_just_queued(self):
   90          self.assert_ready(self.prepare('H'))
   91  
   92      def test_indexed_125_games_are_cached_without_rom_lookup(self):
   93          self.assert_ready(self.prepare('I'))
   94          self.assertEqual([],self.lookups)
   95  
   96      def test_failure_and_retry_preserve_completed_games(self):
   97          self.fail_cache_for.add(61)
   98          first=self.prepare('H')
   99          self.assertIn('FAIL 61/125',first)
  100          self.assertEqual(124,len(self.cached))
  101          before={r['cacheKey']:r['responseBody'] for r in self.store.iter_cache_by_prefix(cache_keys.PREFIX_PATCH)}
  102          self.fail_cache_for.clear()
  103          self.assert_ready(self.prepare('H'))
  104          self.assertEqual(125,len(self.cached),'completed games were needlessly fetched again')
  105          for key,body in before.items(): self.assertEqual(body,self.store.get_cache(key)['responseBody'])
  106  
  107      def test_persisted_pause_never_reports_queued_games_ready(self):
  108          cache_budget.pause_until(self.store,storage.current_millis()+600000)
  109          output=self.prepare('H',3)
  110          self.assertNotIn('\nOK ', '\n'+output)
  111          self.assertIn('DONE cached=0 failed=3',output)
  112          self.assertEqual([],self.cached)
  113          self.assertEqual(3,cache_queue.count(self.store))
  114  
  115      def check_rate_limit(self,kind):
  116          attempts=[]
  117          def refused(*a,**kw):
  118              attempts.append(a[0])
  119              rate_limit.on_rate_limited(1200000)
  120              raise rate_limit.RateLimitedError('synthetic server pause')
  121          self.fake_cache_game=refused
  122          with mock.patch.object(rom_browser,'cache_game',side_effect=refused):
  123              output=self.prepare(kind,3)
  124          self.assertEqual([1],attempts,'work continued sending after429')
  125          self.assertNotIn('\nOK ','\n'+output)
  126          self.assertGreaterEqual(cache_budget.load(self.store).paused_until,storage.current_millis()+1199000)
  127          rate_limit.reset_for_tests()  # another process only has the persisted pause
  128          with mock.patch.object(rom_browser,'cache_game',side_effect=refused):
  129              self.prepare(kind,3)
  130          self.assertEqual([1],attempts,'restart ignored the persisted server pause')
  131  
  132      def test_unindexed_429_stops_requests_and_survives_restart(self): self.check_rate_limit('H')
  133      def test_indexed_429_stops_requests_and_survives_restart(self): self.check_rate_limit('I')
  134  
  135      def test_upstream_default_still_queues_at_100(self):
  136          self.use_budget(100)
  137          (rom,)=self.roms('later');self.game_ids['later']=9
  138          result=rom_browser.add_rom_to_cache(rom,self.store,{})
  139          self.assertTrue(result.success and result.queued)
  140          self.assertEqual([],self.cached)
  141  
  142  
  143  class Upgrade(unittest.TestCase):
  144      def test_actual_predecessor_store_and_image_paths_survive_reopen(self):
  145          with tempfile.TemporaryDirectory(prefix='proxy-old-store-') as directory:
  146              root=Path(directory)
  147              script=r'''
  148  import json,sys
  149  from pathlib import Path
  150  from raofflineproxy import cache_keys
  151  from raofflineproxy.storage import Storage
  152  root=Path(sys.argv[1]);store=Storage(database_path=root/'store.sqlite3')
  153  store.upsert_cache(cache_keys.login('QA'),json.dumps({'User':'QA','Token':'<synthetic>'}))
  154  store.upsert_cache(cache_keys.patch(100,'QA'),json.dumps({'PatchData':{'ID':100,'Title':'old cached game'}}),source_rom_path='/gb/game.gb')
  155  store.upsert_cache(cache_keys.achievementsets('abc','QA'),json.dumps({'GameId':100,'Sets':[{'GameId':100,'Achievements':[{'ID':1}]},{'GameId':200,'Achievements':[{'ID':2}]}]}))
  156  for i in (1,2):
  157   store.upsert_pending_award({'achievementId':i,'queryString':f'/dorequest.php?r=awardachievement&a={i}&u=QA&h=0','requestBody':f'a={i}&u=QA&h=0','userAgent':'RetroArch/QA','queuedAt':1700000000000})
  158  # Predecessors before7252fc expose the list API; current ones stream rows.
  159  # Read the actual old store through its own API, without changing its schema.
  160  rows = list(store.iter_cache_by_prefix('')) if hasattr(store, 'iter_cache_by_prefix') else store.get_all_cache_by_prefix('')
  161  (root/'before.json').write_text(json.dumps({'cache':rows,'awards':store.get_pending_awards()},sort_keys=True))
  162  store.close()
  163  legacy=root/'static/Badge/old.png';legacy.parent.mkdir(parents=True);legacy.write_bytes(b'previous cached image')
  164  '''
  165              env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(args.predecessor_source.resolve()/'linux'),RAOFFLINEPROXY_CONFIG_DIR=str(root/'config'))
  166              result=subprocess.run([sys.executable,'-c',script,str(root)],env=env,capture_output=True,text=True)
  167              self.assertEqual(0,result.returncode, 'predecessor fixture failed: ' + result.stderr)
  168              before=json.loads((root/'before.json').read_text())
  169              for _ in range(2):
  170                  store=storage.Storage(database_path=root/'store.sqlite3')
  171                  try:
  172                      self.assertEqual(sorted(before['cache'],key=lambda r:r['cacheKey']),
  173                                       sorted(store.iter_cache_by_prefix(''),key=lambda r:r['cacheKey']))
  174                      self.assertEqual(before['awards'],store.get_pending_awards())
  175                      self.assertEqual({1:100,2:200},rom_cache.find_achievement_game_ids(store,{1,2}))
  176                      self.assertEqual({'user':'QA','token':'<synthetic>'},store.load_login_credentials())
  177                      meta=store.cached_game_meta(100)
  178                      self.assertEqual({'patch:100:qa','achievementsets:abc:qa'},
  179                                       {row['cacheKey'] for row in meta})
  180                  finally: store.close()
  181              with mock.patch.object(image_cache,'STATIC_DIR',root/'static'):
  182                  self.assertEqual(b'previous cached image',image_cache.resolve_cached_static_asset('/Badge/old.png').read_bytes())
  183  
  184  
  185  class OSConsumers(unittest.TestCase):
  186      def setUp(self):
  187          self.directory=tempfile.TemporaryDirectory(prefix='proxy-consumers-')
  188          self.store=storage.Storage(database_path=Path(self.directory.name)/'store.sqlite3')
  189  
  190      def tearDown(self):
  191          self.store.close()
  192          self.directory.cleanup()
  193  
  194      def helper(self,name):
  195          path=ROOT/'projects/ROCKNIX/packages/network/raofflineproxy/sources'/name
  196          loader=importlib.machinery.SourceFileLoader(name.replace('-','_'),str(path))
  197          spec=importlib.util.spec_from_loader(loader.name,loader)
  198          module=importlib.util.module_from_spec(spec)
  199          loader.exec_module(module)
  200          return module
  201  
  202      def test_refresh_scope_and_session_removal_do_not_load_cache_bodies(self):
  203          refresh=self.helper('raofflineproxy-refresh')
  204          for game in (42,421):
  205              self.store.upsert_cache(cache_keys.patch(game,'qa'),'{"PatchData":{}}')
  206              self.store.upsert_cache(cache_keys.start_session(game,'qa'),'{"Success":true}')
  207          with mock.patch.object(self.store,'iter_cache_by_prefix',side_effect=AssertionError('loaded bodies')):
  208              keys=refresh.cached_games(self.store)
  209              self.assertEqual([42,421],refresh.game_ids(keys))
  210              self.assertEqual([42],refresh.proxy_service.due_refresh_game_ids(keys,{42,99}))
  211              self.assertEqual(1,refresh.drop_startsession(self.store,42))
  212              self.assertIsNotNone(self.store.get_cache(cache_keys.start_session(421,'qa')))
  213  
  214      def test_refresh_age_uses_newest_summary(self):
  215          refresh=self.helper('raofflineproxy-refresh')
  216          self.store.upsert_cache(cache_keys.patch(42,'older'),'{"PatchData":{}}',cached_at=1_700_000_000_000)
  217          self.store.upsert_cache(cache_keys.patch(42,'newer'),'{"PatchData":{}}',cached_at=1_700_000_099_000)
  218          with mock.patch.object(refresh.time,'time',return_value=1_700_000_100), \
  219                  mock.patch.object(self.store,'iter_cache_by_prefix',side_effect=AssertionError('loaded bodies')):
  220              self.assertIn('patch=1s',refresh.row_ages(self.store,42))
  221  
  222      def test_image_repair_reads_streamed_bodies(self):
  223          images=self.helper('raofflineproxy-cache-images')
  224          self.store.upsert_cache(cache_keys.patch(42,'qa'),json.dumps({'PatchData':{'ImageIcon':'/Images/42.png'}}))
  225          self.store.upsert_cache(cache_keys.achievementsets('hash','qa'),json.dumps({'GameId':42,'Achievements':[{'BadgeName':'/Badge/42.png'}]}))
  226          self.assertEqual({'/Images/42.png','/Badge/42.png'},images.all_paths(self.store))
  227          with mock.patch.object(images.image_cache,'resolve_cached_static_asset',return_value=None):
  228              paths,total,rows=images.missing_paths(self.store)
  229          self.assertEqual(['/Badge/42.png','/Images/42.png'],paths)
  230          self.assertEqual((2,2),(total,rows))
  231  
  232  
  233  if __name__=='__main__':
  234      try:
  235          # Discover new fork classes/methods automatically, but do not collect
  236          # imported fixtures or inherited upstream tests as fork-owned coverage.
  237          classes = {value for value in tuple(globals().values())
  238                     if isinstance(value, type) and issubclass(value, unittest.TestCase)
  239                     and value.__module__ == __name__}
  240          suite = unittest.TestSuite(
  241              cls(name)
  242              for cls in sorted(classes, key=lambda value: value.__name__)
  243              for name in unittest.defaultTestLoader.getTestCaseNames(cls)
  244              if name in cls.__dict__)
  245          result=unittest.TextTestRunner(verbosity=2).run(suite)
  246          sys.exit(0 if result.wasSuccessful() else 1)
  247      finally: config.cleanup()
  248  
```

## file, whole, at 8ebaf8daad: tools/signin-memory

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # signin-memory - what the cloud sign-in window costs in memory on a QA guest:
    6  # the peak resident size of the window and WebKit's processes while a page
    7  # loads, and the guest's free memory before and after (fork #228,
    8  # D-WORKFLOW-038: the number the webkitgtk bump is decided on).
    9  #
   10  #   tools/signin-memory <ssh-port> [--url URL] [--seconds N] [--key PATH] [--json]
   11  #
   12  # Over ssh to root@127.0.0.1:<port> (the vm-pair key by default): reads the
   13  # image's webkitgtk version from /usr/lib, opens /usr/bin/cloud-signin-window
   14  # on the guest's sway session the way cloud_oauth does (XDG_RUNTIME_DIR and
   15  # WAYLAND_DISPLAY from the running session, GDK_BACKEND=wayland), samples
   16  # VmRSS and VmHWM of cloud-signin-window, WebKitWebProcess and
   17  # WebKitNetworkProcess once a second for N seconds (default 30), then closes
   18  # the window and reports. The URL defaults to a provider's authorize page
   19  # with a made-up client id: it renders a real sign-in form and signs nobody
   20  # in, and it touches no account -- the page is the load, not the login.
   21  #
   22  # Two runs, one per image, are two rows in docs/vm-qa-log.md; the tool
   23  # prints the row's cells. A guest that shows no wayland session, a window
   24  # that never spawns a web process, or a page that never finishes loading (the
   25  # window's own "load finished" line) is a FAIL, not an empty measurement.
   26  #
   27  # The page is the load. Until 2026-09-25 the default was Dropbox's authorize
   28  # page, and on a QA guest that load fails inside WebKit ("WebKit encountered
   29  # an internal error", right after libsoup's HTTP/2 warning) under 2.52.6 and
   30  # 2.54 alike, so the window sat on "Opening the sign-in page..." and the
   31  # 246 MB baseline of #228 measured a failed load; frames showed it. The
   32  # default is now a page that loads on the guest (example.org), the allowed
   33  # host is the URL's own, and a provider's page is still --url away.
   34  
   35  import json
   36  import subprocess
   37  import sys
   38  import time
   39  
   40  DEFAULT_URL = "https://example.org/"
   41  # /proc/<pid>/comm is 15 characters: the helpers read WebKitWebProces and WebKitNetworkPr
   42  PROCS = ("cloud-signin-wi", "WebKitWebProces", "WebKitNetworkPr")
   43  
   44  
   45  def main():
   46      args = sys.argv[1:]
   47      if not args or args[0] in ("-h", "--help"):
   48          print("\n".join(line[2:] if line.startswith("# ") else "" for line in open(__file__).read().split("\n\n", 1)[0].splitlines()[4:]))
   49          return 0
   50      port = args[0]
   51      url, seconds, key, as_json = DEFAULT_URL, 30, "/tmp/rocknix-vm-pair/qa-key", False
   52      i = 1
   53      while i < len(args):
   54          if args[i] == "--url":
   55              url = args[i + 1]; i += 2
   56          elif args[i] == "--seconds":
   57              seconds = int(args[i + 1]); i += 2
   58          elif args[i] == "--key":
   59              key = args[i + 1]; i += 2
   60          elif args[i] == "--json":
   61              as_json = True; i += 1
   62          else:
   63              sys.exit("signin-memory: unknown argument %s" % args[i])
   64  
   65      def ssh(cmd, timeout=60):
   66          r = subprocess.run(["ssh", "-n", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=no",
   67                              "-o", "UserKnownHostsFile=/dev/null", "-o", "LogLevel=ERROR",
   68                              "-o", "ConnectTimeout=10", "-p", port, "-i", key, "root@127.0.0.1", cmd],
   69                             capture_output=True, text=True, timeout=timeout)
   70          return r.returncode, r.stdout.strip(), r.stderr.strip()
   71  
   72      rc, build, _ = ssh("grep -E '^(BUILD_ID|VERSION)=' /etc/os-release | tr '\\n' ' '; ls /usr/lib/libwebkit2gtk-4.1.so.* 2>/dev/null | head -1")
   73      if rc != 0:
   74          sys.exit("signin-memory: FAIL -- cannot reach root@127.0.0.1:%s (%s)" % (port, _))
   75      rc, sess, _ = ssh("for u in /run/user/* /var/run/*; do for d in \"$u\"/wayland-*; do case \"$d\" in *.lock) ;; *) [ -e \"$d\" ] && { echo \"$u $(basename \"$d\")\"; exit 0; }; esac; done; done; exit 1")
   76      if rc != 0 or not sess:
   77          sys.exit("signin-memory: FAIL -- no wayland session on the guest (is EmulationStation's sway up?)")
   78      runtime, display = sess.split()
   79      import urllib.parse
   80      host = urllib.parse.urlparse(url).hostname or ""
   81      if host.startswith("www."):
   82          host = host[4:]
   83      free_before = ssh("free -m | awk '/^Mem:/{print $7}'")[1]
   84      # the window, detached, its pid recorded
   85      ssh("XDG_RUNTIME_DIR=%s WAYLAND_DISPLAY=%s GDK_BACKEND=wayland CLOUD_SIGNIN_PAGE_FILE=/tmp/sm-page CLOUD_SIGNIN_DONE_FILE=/tmp/sm-done "
   86          "nohup /usr/bin/cloud-signin-window '%s' '%s' --exit-hint '' >/tmp/signin-memory.log 2>&1 & echo $! > /tmp/signin-memory.pid" % (runtime, display, url, host), timeout=20)
   87      peaks = {p: 0 for p in PROCS}
   88      seen = {p: False for p in PROCS}
   89      samples = []
   90      for t in range(seconds):
   91          rc, out, _ = ssh("for p in /proc/[0-9]*; do c=$(cat $p/comm 2>/dev/null); case \"$c\" in cloud-signin-wi|WebKitWebProces|WebKitNetworkPr) "
   92                           "echo \"$c $(awk '/^VmRSS/{r=$2} /^VmHWM/{h=$2} END{print r, h}' $p/status)\";; esac; done", timeout=20)
   93          row = {}
   94          for line in out.splitlines():
   95              parts = line.split()
   96              if len(parts) == 3:
   97                  c, rss, hwm = parts[0], int(parts[1]), int(parts[2])
   98                  row[c] = row.get(c, 0) + rss
   99                  seen[c] = True
  100                  peaks[c] = max(peaks[c], hwm)
  101          samples.append(row)
  102          time.sleep(1)
  103      page = ssh("cat /tmp/sm-page 2>/dev/null; tail -2 /tmp/signin-memory.log 2>/dev/null | cut -c1-200")[1]
  104      loaded = ssh("grep -c 'load finished' /tmp/signin-memory.log 2>/dev/null")[1].strip() not in ("", "0")
  105      ssh("kill $(cat /tmp/signin-memory.pid) 2>/dev/null; sleep 1; pkill -x WebKitWebProces 2>/dev/null; pkill -x WebKitNetworkPr 2>/dev/null; true", timeout=20)
  106      free_after = ssh("free -m | awk '/^Mem:/{print $7}'")[1]
  107      total_peak_rss = max((sum(r.values()) for r in samples), default=0)
  108      ok = seen["cloud-signin-wi"] and seen["WebKitWebProces"] and loaded
  109      out = {"loaded": loaded, "port": port, "guest": build, "url": url, "seconds": seconds, "wayland": display,
  110             "peak_hwm_kb": peaks, "peak_total_rss_kb": total_peak_rss,
  111             "free_mb_before": free_before, "free_mb_after": free_after, "page": page, "pass": ok}
  112      if as_json:
  113          print(json.dumps(out, indent=1)); return 0 if ok else 1
  114      print("guest: %s" % build)
  115      print("window: %s for %d s on %s; page: %s" % (url.split("?")[0], seconds, display, page.replace("\n", " | ")[:160]))
  116      print("peak resident (VmHWM), MB: " + ", ".join("%s %.0f" % (k, v / 1024.0) for k, v in peaks.items()))
  117      print("peak of the three together (VmRSS summed per sample), MB: %.0f" % (total_peak_rss / 1024.0))
  118      print("guest free memory, MB: %s before, %s after" % (free_before, free_after))
  119      if ok:
  120          print("PASS")
  121      elif not loaded and seen["cloud-signin-wi"] and seen["WebKitWebProces"]:
  122          print("FAIL -- the page never finished loading, so these numbers are a window on its placeholder; read /tmp/signin-memory.log on the guest")
  123      else:
  124          print("FAIL -- the window or its web process never appeared; read /tmp/signin-memory.log on the guest")
  125      return 0 if ok else 1
  126  
  127  
  128  if __name__ == "__main__":
  129      sys.exit(main())
  130  
```

## file, whole, at 8ebaf8daad: tools/time-to-play

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # time-to-play - the two numbers a player feels, measured on one VM guest.
    6  #
    7  #   tools/time-to-play --port 10025 --identity /tmp/rocknix-vm-pair/qa-key \
    8  #       --monitor /tmp/rocknix-qemu-monitor-c.sock --backend sftp \
    9  #       --repeat 5 --out /tmp/ttp
   10  #
   11  # WHY. Time to play is a first-class metric (D-CLOUD-098, #135): how long
   12  # from the interface to a game's first frame, and from one game's exit to
   13  # the next game's first frame. Budgets for both are register rows, and a row
   14  # is only ever set from a measurement (D-CLOUD-116) -- so something has to
   15  # take the measurement, on the VM and never on a console (vm-first.md).
   16  # This is that something.
   17  #
   18  # WHAT IT MEASURES, and how each number is defined:
   19  #
   20  #   launch    UI to game, at rest. From the POST that EmulationStation's own
   21  #             HTTP API turns into ViewController::launch -- the same code
   22  #             path as pressing A on the game -- to the first frame the game
   23  #             draws. "First frame" is the first screendump that differs from
   24  #             the one before it AT OR AFTER the RetroArch process exists;
   25  #             the screen leaves the carousel earlier than that (the interface
   26  #             tears its window down first), which is why the two are
   27  #             separate numbers here and the earlier one is not the answer.
   28  #             Corroborated by RetroArch's CPU ticks: the exit cell's rule is
   29  #             that RetroArch is drawing once utime+stime reach 200
   30  #             (awk '{print $14+$15}' /proc/<pid>/stat).
   31  #
   32  #   exit      The exit sync alone. From the shipped execute_kill (extracted
   33  #             from the installed input_sense, so the signal is the one under
   34  #             test) to (a) the last-sync-exit stamp being written -- the work
   35  #             ending -- and (b) the card leaving the screen, which is later
   36  #             by the linger the card holds its outcome for. Both are
   37  #             reported: the stamp is when the saves are safe, the card is
   38  #             when the player stops being told something is happening.
   39  #
   40  #   g2g       Game to game. The same exit, with a launch fired the moment the
   41  #             emulator is gone and STOP IT AND PLAY pressed half a second later
   42  #             (D-CLOUD-130: the launch asks before it stops the sync). What the
   43  #             launch does to the sync is read off the stamp's token afterwards
   44  #             -- `cancelled` is the answer's doing, `completed` would mean the
   45  #             sync ran to the end before the press -- so the cell reports what
   46  #             the build does rather than assuming.
   47  #
   48  #   startup   The startup sync: cloudsaves.startup=1, reboot, and time from
   49  #             the reboot to the last-sync-startup stamp; then a launch fired
   50  #             while the startup sync is still running. The setting is put
   51  #             back afterwards.
   52  #
   53  #   offline   D-CLOUD-112's benchmark: the same exit sync with no
   54  #             connectivity, four ways -- a refused port, no default route, a
   55  #             blackholed route to the endpoint, and a captive portal
   56  #             answering HTTP for everything -- each beside the online number,
   57  #             because the claim under test is that the offline exit reaches
   58  #             its outcome in about the time a successful one would have
   59  #             taken.
   60  #
   61  #   bounds    D-CLOUD-111's three bounds as they stand TODAY: the refused
   62  #             port, an endpoint that accepts and never answers, and the
   63  #             captive portal. How long until the sync ends, and with what
   64  #             outcome on the card. Frames every half second are kept.
   65  #
   66  # The payload. D-CLOUD-116 asks for a game exited with an auto-state plus a
   67  # couple of manual save states and their screenshots. Probe.nes through
   68  # RetroArch on the guest leaves a 514-byte auto-state and a 506-byte
   69  # thumbnail -- a payload so small that it measures the round trip and
   70  # nothing else -- so the cell seeds realistic files instead and says so in
   71  # its report: three states of ~180 KiB, three screenshots of ~18 KiB and an
   72  # 8 KiB battery save, sizes jittered per repeat so that a backend comparing
   73  # by size alone (WebDAV with vendor=other) still sees a change. --payload srm
   74  # seeds only the battery save, which is P-13's "one changed battery save".
   75  #
   76  # The AUTO-state in what actually moves is RetroArch's own, not the seeded
   77  # one: runemu.sh launches with -autosave 1, so RetroArch rewrites
   78  # Probe.state.auto and its thumbnail on the way out and the seeded pair is
   79  # replaced before the sync reads them. So a measured exit moves seven files
   80  # and about 440 KiB -- a real auto-state and its screenshot, two synthetic
   81  # manual states with theirs, and the battery save -- which is D-CLOUD-116's
   82  # shape with the one file that could be real being real. The cell reports
   83  # what it seeded (`du`); the run's rclone line in the log reports what moved.
   84  #
   85  # WHAT IT DOES TO THE GUEST, and puts back: the rclone remote's address (for
   86  # the offline and bounds cells), cloudsaves.startup (for the startup cell),
   87  # the guest's default route (for one offline cell), and the seeded saves.
   88  # Nothing else. A copy of rclone.conf is taken before the first change and
   89  # restored on every exit, including a signal.
   90  #
   91  # TIMING RESOLUTION. A screendump round trip through the QEMU monitor costs
   92  # about 0.2 s on a 640x480 guest, so every frame-derived number is quoted to
   93  # that. The SSH round trip (a ControlMaster is held open) is measured at the
   94  # start of the run and reported beside the numbers, because it sits inside
   95  # the launch number: the POST goes over it.
   96  import argparse
   97  import importlib.machinery
   98  import importlib.util
   99  import json
  100  import os
  101  import re
  102  import shutil
  103  import signal
  104  import statistics
  105  import subprocess
  106  import sys
  107  import tempfile
  108  import threading
  109  import time
  110  
  111  HERE = os.path.dirname(os.path.abspath(__file__))
  112  
  113  # vm-visual-qa is the fork's framebuffer tooling: the monitor client, the
  114  # byte-fraction frame comparison and its two thresholds, and the PPM->PNG
  115  # writer. Loaded as a module rather than shelled out to per frame -- a
  116  # subprocess per screendump would reconnect the monitor each time and put
  117  # the poll interval an order of magnitude above the numbers being measured.
  118  _loader = importlib.machinery.SourceFileLoader(
  119      "vm_visual_qa", os.path.join(HERE, "vm-visual-qa"))
  120  _spec = importlib.util.spec_from_loader("vm_visual_qa", _loader)
  121  vq = importlib.util.module_from_spec(_spec)
  122  _loader.exec_module(vq)
  123  
  124  ROM = "/storage/roms/nes/Probe.nes"
  125  RETROARCH_CFG = "/storage/.config/retroarch/retroarch.cfg"
  126  # Busybox pgrep -x compares the whole argv and RetroArch's argv[0] is its
  127  # full path, so -x never matches it (generic-x64-vm-testing.md). The bracket
  128  # keeps the pattern from matching the shell that carries it.
  129  RA_PROBE = ('p=$(pgrep -f "/usr/bin/retroarc[h]" | head -1); '
  130              '[ -n "$p" ] && echo "$p $(awk \'{print $14+$15}\' /proc/$p/stat 2>/dev/null || echo 0)"')
  131  STAMP_DIR = "/storage/.cache/cloud_sync"
  132  RCLONE_CONF = "/storage/.config/rclone/rclone.conf"
  133  CLOUD_CONF = "/storage/.config/cloud_sync.conf"
  134  # The two host fixtures the offline and bounds cells need, in the 9010-9099
  135  # range this fork reserves for QA services. 9011 is the refused port every
  136  # failure fixture already aims at and is never bound by anything.
  137  PORTAL_PORT = 9016
  138  STALL_PORT = 9017
  139  DEAD_PORT = 9011
  140  
  141  
  142  # --------------------------------------------------------------------------
  143  # the guest
  144  
  145  
  146  class Guest:
  147      """One SSH channel to the guest, held open.
  148  
  149      ControlMaster because the POST that starts a launch goes over it and the
  150      number being measured is in tenths of a second: a fresh TCP connection
  151      and key exchange per command would be most of the first repeat's answer.
  152      drop_master() exists because an admin-down link or a blackholed route
  153      does not reset an established connection -- it stalls it -- so anything
  154      that cuts the guest's path to 10.0.2.2 closes the master first."""
  155  
  156      def __init__(self, host, port, key):
  157          self.host, self.port, self.key = host, str(port), key
  158          self.cp = "/tmp/ttp-cm-%d" % os.getpid()
  159  
  160      def _opts(self, master=True):
  161          o = ["-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
  162               "-o", "LogLevel=ERROR", "-o", "ConnectTimeout=8", "-o", "BatchMode=yes"]
  163          if self.key:
  164              o += ["-i", self.key]
  165          if master:
  166              o += ["-o", "ControlMaster=auto", "-o", "ControlPath=" + self.cp,
  167                    "-o", "ControlPersist=120"]
  168          return o
  169  
  170      def sh(self, cmd, timeout=60, master=True):
  171          try:
  172              # errors="replace", not text=True: the guest's log is UTF-8 and
  173              # busybox `cut -c` counts BYTES, so a line trimmed for the report
  174              # can end mid-character. A whole run died on one 0xc3 while
  175              # collecting the portal cell's log (2026-09-12); a measurement
  176              # must not be lost to a byte in a diagnostic.
  177              p = subprocess.run(["ssh", "-n", "-p", self.port] + self._opts(master) + [self.host, cmd],
  178                                 capture_output=True, timeout=timeout,
  179                                 encoding="utf-8", errors="replace")
  180              return p.returncode, p.stdout.strip()
  181          except subprocess.TimeoutExpired:
  182              return 255, ""
  183  
  184      def put(self, local, remote):
  185          """scp's exit status: a copy that failed is said by the caller, never
  186          assumed done (a missing directory on a fresh guest made the conf
  187          copy fail silently, and two comparisons timed syncs to nowhere)."""
  188          return subprocess.run(["scp", "-q", "-P", self.port] + self._opts() + [local, self.host + ":" + remote],
  189                                capture_output=True).returncode
  190  
  191      def drop_master(self):
  192          subprocess.run(["ssh", "-O", "exit", "-o", "ControlPath=" + self.cp,
  193                          "-p", self.port, self.host], capture_output=True)
  194  
  195      def alive(self, timeout=8):
  196          return self.sh("true", timeout=timeout, master=False)[0] == 0
  197  
  198      def wait_alive(self, budget=180):
  199          end = time.monotonic() + budget
  200          while time.monotonic() < end:
  201              if self.alive(timeout=6):
  202                  return True
  203              time.sleep(2)
  204          return False
  205  
  206      # --- the things this cell asks the guest ------------------------------
  207  
  208      def retroarch(self):
  209          """(pid, cpu ticks) while RetroArch runs, else None."""
  210          rc, out = self.sh(RA_PROBE, timeout=15)
  211          if not out:
  212              return None
  213          parts = out.split()
  214          try:
  215              return int(parts[0]), int(parts[1])
  216          except (IndexError, ValueError):
  217              return None
  218  
  219      def stamp(self, name):
  220          """The raw last-sync-<name> line, or ''."""
  221          return self.sh("cat %s/last-sync-%s 2>/dev/null" % (STAMP_DIR, name), timeout=15)[1]
  222  
  223      def es_up(self):
  224          return self.sh("pgrep -x emulationstation >/dev/null && echo y", timeout=15)[1] == "y"
  225  
  226      def launch(self, rom=ROM):
  227          """EmulationStation's own launch path, as pressing A on the game is.
  228  
  229          The HTTP API listens on the guest's loopback only, so the POST is
  230          made from inside the guest. ViewController::launch is what handles
  231          it -- the same function the A press reaches -- so the exit sync,
  232          the launch gate and the splash all behave exactly as for a player."""
  233          return self.sh("curl -s -o /dev/null -w '%%{http_code}' -X POST "
  234                         "-H 'Content-Type: text/plain' --data '%s' "
  235                         "http://127.0.0.1:1234/launch" % rom, timeout=25)[1]
  236  
  237      def kill_game(self):
  238          """The shipped execute_kill, from the installed input_sense."""
  239          return self.sh("/tmp/ttp-kill", timeout=20)[0]
  240  
  241  
  242  def ppm_size(data):
  243      """Width and height from a P6 header, or None."""
  244      m = re.match(rb"P6\s+(\d+)\s+(\d+)\s+", data or b"")
  245      return (int(m.group(1)), int(m.group(2))) if m else None
  246  
  247  
  248  def surface_check(g, fr, rom=None):
  249      """RetroArch draws at the panel's size, or the frames lie (fork #263).
  250  
  251      The GENERIC_X64 image shipped video_fullscreen_x/y = 0, and under wayland
  252      that gave RetroArch a surface the size of the game (240x256 for an NES
  253      core) that sway scaled up to the 640x480 panel: every stem in every text
  254      read off a guest was two grey columns, whatever the font size, and the
  255      #251 measurements described that scaling. RetroArch's log says what it
  256      used; the panel is what the screendump is. A surface under the panel is
  257      not a pass, because nothing measured on its frames is what the device
  258      draws."""
  259      # The line is this launch's or it is nothing (blindspot 50): the first
  260      # "Using resolution" after the last "Loading content file" that names the
  261      # ROM just launched. Runs 29 and 30 on e506fcd8e5 took the file's last
  262      # "Using resolution" line whoever wrote it, and read 240x256 over frames
  263      # that show RetroArch drawing at the panel's size (2026-09-25).
  264      evidence = g.sh("grep -n 'Loading content file\\|Detecting screen resolution\\|Using resolution' /var/log/exec.log 2>/dev/null | tail -12; "
  265                      "ls -la --time-style=+%T /var/log/exec.log 2>/dev/null; date +%T", timeout=20)[1]
  266      line, seen_launch = "", rom is None
  267      for raw in (evidence or "").splitlines():
  268          if "Loading content file" in raw:
  269              seen_launch = rom is None or rom in raw
  270              line = ""
  271          elif seen_launch and not line and "Using resolution" in raw:
  272              line = raw
  273      m = re.search(r"Using resolution (\d+)x(\d+)", line or "")
  274      # The size RetroArch's own GPU screenshot comes out at IS the surface it
  275      # draws into: the GL framebuffer read back at the viewport's size
  276      # (video_gpu_screenshot, which --vm switches on for the run). Since fork
  277      # #291 it is the first source and the log line the fallback: under a GL
  278      # context "Using resolution" is written before the compositor's
  279      # fullscreen resize lands -- 240x256 on a 1280x800 guest whose game frame
  280      # is drawn pixel-sharp at the panel -- so it says what the surface was
  281      # for a few milliseconds, not what the frames are. Three presses of the
  282      # screenshot key, half a second held (#278); the file is removed so the
  283      # SCREENSHOTS walks that follow do not list it.
  284      shot = None
  285      if g.retroarch() is not None:
  286          before = (g.sh("ls /storage/roms/screenshots/ 2>/dev/null | wc -l")[1] or "").strip() or "0"
  287          probe = ('f=$(ls -t /storage/roms/screenshots/*.png 2>/dev/null | head -1); '
  288                   'n=$(ls /storage/roms/screenshots/ 2>/dev/null | wc -l); '
  289                   'if [ "$n" -gt BEFORE ] && [ -n "$f" ]; then python3 -c \'import struct,sys; d=open(sys.argv[1],"rb").read(24); '
  290                   'print("%dx%d" % struct.unpack(">II", d[16:24]))\' "$f" && rm -f "$f"; fi').replace("BEFORE", before)
  291          for _ in range(3):
  292              fr.mon.cmd("sendkey f8 500", settle=0.2)
  293              time.sleep(1.5)
  294              got = (g.sh(probe, timeout=20)[1] or "").strip()
  295              if re.match(r"^\d+x\d+$", got):
  296                  shot = got
  297                  break
  298      if shot:
  299          sw, sh = [int(v) for v in shot.split("x")]
  300      elif m:
  301          sw, sh = int(m.group(1)), int(m.group(2))
  302      else:
  303          sw = sh = None
  304      panel = ppm_size(fr.rest(timeout=10))
  305      out = {"surface": ("%dx%d" % (sw, sh)) if sw else None,
  306             "source": "RetroArch's GPU screenshot" if shot else ("the launch log's Using resolution line" if m else None),
  307             "panel": ("%dx%d" % panel) if panel else None, "scaled": None,
  308             "evidence": (evidence or "").splitlines()}
  309      if sw and panel:
  310          # The GPU screenshot is the viewport: with aspect correction it fills
  311          # one of the panel's dimensions (1067x800 under 1280x800 for a 4:3
  312          # game), so a surface the compositor scaled is short on BOTH. The
  313          # log line names the window, which is short on either when scaled.
  314          if shot:
  315              out["scaled"] = sw < panel[0] and sh < panel[1]
  316          else:
  317              out["scaled"] = sw < panel[0] or sh < panel[1]
  318      return out
  319  
  320  
  321  GB_PROBE = "/storage/roms/gb/TTProbe.gb"
  322  GB_LOGO = ("CEED6666CC0D000B03730083000C000D0008111F8889000EDC"
  323             "CC6EE6DDDDD999BBBB67636E0EECCCDDDC999FBBB9333E")
  324  
  325  
  326  def build_gb_probe(path):
  327      """A cartridge that does nothing but draw.
  328  
  329      The runner's guests carry no ROM of their own, and a cell that cannot
  330      press a game on a fresh pair is a cell that never runs. This is the
  331      exit test's cartridge with its job swapped: that one writes a battery
  332      save and this one turns the LCD on with a blank background, because
  333      what this cell needs from a game is a frame that is NOT the black
  334      handover screen. Not shared with tools/emulator-exit-test, because the
  335      two carts have no line of behaviour in common -- only the twenty bytes
  336      of header every Game Boy ROM has."""
  337      rom = bytearray(0x8000)
  338      rom[0x100:0x104] = bytes([0x00, 0xC3, 0x50, 0x01])      # NOP ; JP $0150
  339      rom[0x104:0x134] = bytes.fromhex(GB_LOGO)
  340      rom[0x134:0x13B] = b"TTPROBE"
  341      rom[0x147] = 0x00   # ROM ONLY; nothing here needs a battery
  342      rom[0x148] = 0x00   # 32 KiB
  343      rom[0x149] = 0x00
  344      rom[0x14A] = 0x01
  345      rom[0x14B] = 0x33
  346      x = 0
  347      for i in range(0x134, 0x14D):
  348          x = (x - rom[i] - 1) & 0xFF
  349      rom[0x14D] = x
  350      rom[0x150:0x15B] = bytes([
  351          0xF3,              # DI
  352          0x3E, 0xE4,        # LD A,$E4     the usual BGP
  353          0xE0, 0x47,        # LDH ($47),A
  354          0x3E, 0x91,        # LD A,$91     LCD on, BG on, tiles at $8000
  355          0xE0, 0x40,        # LDH ($40),A
  356          0x18, 0xFE,        # JR -2        spin
  357      ])
  358      with open(path, "wb") as fh:
  359          fh.write(bytes(rom))
  360  
  361  
  362  def ensure_rom(g, rom, workdir):
  363      """The game this cell presses, and whether it had to make one.
  364  
  365      EmulationStation launches what it has scanned, so a ROM dropped on the
  366      guest is invisible until it looks again -- and a restart is not enough
  367      to look at from here: screendump serves the previous instance's last
  368      frame for half a minute afterwards (generic-x64-vm-testing.md), which
  369      is exactly the window this cell measures in. A reboot costs about a
  370      minute and has neither problem."""
  371      if g.sh("test -f '%s' && echo y" % rom)[1] == "y":
  372          return rom, False
  373      local = os.path.join(workdir, "TTProbe.gb")
  374      build_gb_probe(local)
  375      g.sh("mkdir -p /storage/roms/gb")
  376      if g.put(local, GB_PROBE) != 0:
  377          sys.exit("time-to-play: could not copy the probe ROM to the guest's " + GB_PROBE)
  378      return GB_PROBE, True
  379  
  380  
  381  def reboot_guest(g):
  382      """Reboot and wait for EmulationStation, then a moment for its first frame."""
  383      g.sh("systemctl reboot")
  384      g.drop_master()
  385      time.sleep(8)
  386      g.wait_alive(240)
  387      for _ in range(60):
  388          if g.es_up():
  389              break
  390          time.sleep(2)
  391      time.sleep(12)
  392  
  393  
  394  def install_helpers(g):
  395      g.sh('cat > /tmp/ttp-kill <<"H"\n'
  396           '#!/bin/bash\n'
  397           'DEBUG=false; log() { :; }\n'
  398           'eval "$(sed -n "/^execute_kill()/,/^}/p" /usr/bin/input_sense)"\n'
  399           'execute_kill\n'
  400           'H\n'
  401           'chmod +x /tmp/ttp-kill; echo ok')
  402  
  403  
  404  # --------------------------------------------------------------------------
  405  # the payload
  406  
  407  
  408  def seed_payload(g, jitter, kind="full"):
  409      """The saves the exit sync has to move, with fresh mtimes.
  410  
  411      Sizes are jittered by the repeat index because WebDAV with vendor=other
  412      carries neither hashes nor modtimes: rclone compares by size alone
  413      there, so a byte-for-byte-different file of the same size is 'already
  414      uploaded' and the repeat would measure an empty transfer (#53's shape).
  415      Everything written here is inside cloud_sync-rules.txt's allowlist:
  416      /savestates/** wholesale, and *.srm by extension."""
  417      if kind == "srm":
  418          script = (
  419              'set -e; mkdir -p /storage/roms/nes\n'
  420              'dd if=/dev/urandom of=/storage/roms/nes/Probe.srm bs=1024 count=%d 2>/dev/null\n'
  421              'du -k /storage/roms/nes/Probe.srm | cut -f1\n' % (8 + jitter))
  422      else:
  423          script = (
  424              'set -e; d=/storage/roms/savestates/nes; mkdir -p "$d" /storage/roms/nes\n'
  425              'dd if=/dev/urandom of="$d/Probe.state.auto"  bs=1024 count=%d 2>/dev/null\n'
  426              'dd if=/dev/urandom of="$d/Probe.state.auto.png" bs=1024 count=%d 2>/dev/null\n'
  427              'dd if=/dev/urandom of="$d/Probe.state1"      bs=1024 count=%d 2>/dev/null\n'
  428              'dd if=/dev/urandom of="$d/Probe.state1.png"  bs=1024 count=%d 2>/dev/null\n'
  429              'dd if=/dev/urandom of="$d/Probe.state2"      bs=1024 count=%d 2>/dev/null\n'
  430              'dd if=/dev/urandom of="$d/Probe.state2.png"  bs=1024 count=%d 2>/dev/null\n'
  431              'dd if=/dev/urandom of=/storage/roms/nes/Probe.srm bs=1024 count=%d 2>/dev/null\n'
  432              'du -ck "$d" /storage/roms/nes/Probe.srm | tail -1 | cut -f1\n'
  433              % (180 + jitter, 18 + jitter, 181 + jitter, 17 + jitter,
  434                 179 + jitter, 19 + jitter, 8 + jitter))
  435      return g.sh(script, timeout=60)[1]
  436  
  437  
  438  # --------------------------------------------------------------------------
  439  # frames
  440  
  441  
  442  def is_blank(frame):
  443      """Is this the handover screen rather than a picture?
  444  
  445      Between the interface tearing its window down and the emulator drawing,
  446      the scanout is black -- 0.22 s after the press on this guest, a third of
  447      a second before RetroArch's first green frame at 0.63 s. Both are "the
  448      screen changed", and only the second is the number #135 asks for. A
  449      frame whose bytes are almost all zero is the handover; a game frame,
  450      even a dark one, is not (Probe.nes draws 0x0d3d0d, 8% of the byte range,
  451      on every pixel)."""
  452      if not frame:
  453          return True
  454      # Past the PPM header: three lines, then the pixel data.
  455      body = frame
  456      for _ in range(3):
  457          nl = body.find(b"\n")
  458          if nl < 0:
  459              break
  460          body = body[nl + 1:]
  461      if not body:
  462          return True
  463      return (len(body) - body.count(0)) / float(len(body)) < 0.01
  464  
  465  
  466  class Frames:
  467      """A monitor connection plus the bookkeeping every cell wants."""
  468  
  469      def __init__(self, path, outdir):
  470          self.mon = vq.Monitor(path)
  471          self.outdir = outdir
  472          os.makedirs(outdir, exist_ok=True)
  473  
  474      def frame(self):
  475          return self.mon.frame()
  476  
  477      def rest(self, timeout=25):
  478          """The screen with nothing happening on it: settle, then a frame.
  479  
  480          Every cell that asks 'is the card gone?' asks it against this."""
  481          vq.settle(self.mon.frame, timeout=timeout, quiet=1.2)
  482          return self.mon.frame()
  483  
  484      def save(self, name, data=None):
  485          ppm = os.path.join(self.outdir, name + ".ppm")
  486          png = os.path.join(self.outdir, name + ".png")
  487          if data is None:
  488              if not self.mon.screendump(ppm):
  489                  return None
  490          else:
  491              with open(ppm, "wb") as fh:
  492                  fh.write(data)
  493          try:
  494              vq.to_png(ppm, png)
  495          finally:
  496              try:
  497                  os.remove(ppm)
  498              except OSError:
  499                  pass
  500          return os.path.basename(png)
  501  
  502      def close(self):
  503          self.mon.close()
  504  
  505  
  506  # --------------------------------------------------------------------------
  507  # the cells
  508  
  509  
  510  def measure_launch(g, fr, tag, budget=45.0, rom=ROM):
  511      """UI to a game's first frame, from a screen at rest.
  512  
  513      Two clocks run at once and neither can be asked to wait for the other:
  514      the framebuffer says when a frame was drawn, /proc says when RetroArch
  515      existed and when it had burnt enough CPU to be drawing. The process poll
  516      is a thread so that a 15 ms SSH round trip does not sit between two
  517      screendumps."""
  518      base = fr.rest()
  519      result = {"tag": tag}
  520      ra = {"seen": None, "ticks200": None, "pid": None}
  521      stop = threading.Event()
  522      t0 = [None]
  523  
  524      def poll():
  525          while not stop.is_set():
  526              st = g.retroarch()
  527              now = time.monotonic()
  528              if st is not None:
  529                  if ra["seen"] is None:
  530                      ra["seen"] = now
  531                      ra["pid"] = st[0]
  532                  if ra["ticks200"] is None and drawing(st, ra["seen"], now):
  533                      ra["ticks200"] = now
  534              time.sleep(0.08)
  535  
  536      th = threading.Thread(target=poll, daemon=True)
  537      th.start()
  538      t0[0] = time.monotonic()
  539      http = g.launch(rom)
  540      result["http"] = http
  541      series, prev = [], base
  542      first_change = game_frame = None
  543      saved_first = saved_game = None
  544      blank_at = [None]
  545      while time.monotonic() - t0[0] < budget:
  546          t = time.monotonic()
  547          f = fr.frame()
  548          d_base = vq.frame_diff(base, f)
  549          d_prev = vq.frame_diff(prev, f)
  550          series.append([round(t - t0[0], 3), round(d_base, 6), round(d_prev, 6)])
  551          blank = is_blank(f)
  552          if first_change is None and d_base >= vq.CHANGED_MIN:
  553              first_change = t - t0[0]
  554              saved_first = fr.save("%s-01-left-carousel" % tag, f)
  555          if blank and blank_at[0] is None and d_base >= vq.CHANGED_MIN:
  556              blank_at[0] = t - t0[0]
  557          seen = ra["seen"]
  558          # The game's first frame: not the carousel, not the handover, and
  559          # not before the process that draws it exists. All three, because
  560          # each alone is wrong on its own -- the black screen satisfies the
  561          # first, a carousel redraw the second, and RetroArch exists for a
  562          # fifth of a second before it draws anything.
  563          if (game_frame is None and first_change is not None and seen is not None
  564                  and t > seen and not blank and d_base >= vq.CHANGED_MIN):
  565              game_frame = t - t0[0]
  566              saved_game = fr.save("%s-02-first-game-frame" % tag, f)
  567              break
  568          if f is not None:
  569              prev = f
  570      stop.set()
  571      th.join(timeout=5)
  572      result.update({
  573          "t_left_carousel": None if first_change is None else round(first_change, 3),
  574          "t_screen_blank": None if blank_at[0] is None else round(blank_at[0], 3),
  575          "t_retroarch_seen": None if ra["seen"] is None else round(ra["seen"] - t0[0], 3),
  576          "t_first_game_frame": None if game_frame is None else round(game_frame, 3),
  577          "frames": series,
  578          "png": [x for x in (saved_first, saved_game) if x],
  579      })
  580      # ticks200 usually lands after the first game frame; give it a moment
  581      # rather than reporting a corroboration that simply had not happened yet.
  582      end = time.monotonic() + 15
  583      while ra["ticks200"] is None and time.monotonic() < end:
  584          st = g.retroarch()
  585          if st is None:
  586              break
  587          if drawing(st, ra["seen"], time.monotonic()):
  588              ra["ticks200"] = time.monotonic()
  589          time.sleep(0.1)
  590      result["t_ticks200"] = None if ra["ticks200"] is None else round(ra["ticks200"] - t0[0], 3)
  591      return result, base
  592  
  593  
  594  def settle_sync(g, budget=60):
  595      """Back to a device with nothing running on it.
  596  
  597      It ENDS a leftover emulator rather than waiting one out: a repeat that
  598      began while the previous game was still up measured the previous game's
  599      exit, and a cell that waits for a condition it could create itself
  600      spends its budget proving the wait works."""
  601      if g.retroarch() is not None:
  602          g.kill_game()
  603      end = time.monotonic() + budget
  604      while time.monotonic() < end:
  605          busy = g.sh("pgrep -f 'rclon[e]' >/dev/null && echo busy || echo idle")[1]
  606          if g.retroarch() is None and busy == "idle":
  607              time.sleep(2)
  608              return True
  609          time.sleep(1)
  610      return False
  611  
  612  
  613  def drawing(st, seen, now):
  614      """The exit cell's readiness rule: RetroArch has burnt 2 s of CPU (200
  615      ticks) -- a software-rendered RetroArch's signature. On hardware GL (fork
  616      #291) the process burns about five ticks a second after some thirty of
  617      init, so the rule is also met at thirty ticks four seconds after the
  618      process was first seen; a guest on either path answers within seconds."""
  619      if st is None:
  620          return False
  621      if st[1] >= 200:
  622          return True
  623      return st[1] >= 30 and seen is not None and now - seen >= 4.0
  624  
  625  
  626  def wait_drawing(g, budget=60):
  627      """Until RetroArch is drawing by the rule above."""
  628      end = time.monotonic() + budget
  629      seen = None
  630      while time.monotonic() < end:
  631          st = g.retroarch()
  632          now = time.monotonic()
  633          if st is not None and seen is None:
  634              seen = now
  635          if drawing(st, seen, now):
  636              return True
  637          time.sleep(0.2)
  638      return False
  639  
  640  
  641  def parse_stamp(line):
  642      parts = (line or "").split()
  643      out = {"raw": line}
  644      if len(parts) >= 3:
  645          out.update({"epoch": parts[0], "rc": parts[1], "token": parts[2],
  646                      "why": " ".join(parts[3:])})
  647      return out
  648  
  649  
  650  def measure_exit(g, fr, tag, rest_ref, relaunch=False, budget=150.0,
  651                   frame_every=0.5, keep_frames=True, ssh_poll=True, rom=ROM):
  652      """The exit sync, from execute_kill to the stamp and to the card going.
  653  
  654      rest_ref is the screen before the game was launched: the card is gone
  655      when the screen matches it again. That comparison is why the whole cell
  656      starts from a settled screen -- a carousel with a dialog half-open on it
  657      would never match, and the cell would report the card as never leaving.
  658  
  659      The relaunch is fired from the poll thread the instant the emulator is
  660      gone, not from the frame loop: the frame loop runs at half a second and
  661      a player's thumb does not wait for a screendump. What the launch then
  662      does to the sync is not assumed -- it is read off the stamp's token
  663      afterwards.
  664  
  665      ssh_poll=False is for the one condition that cuts this channel (a
  666      blackhole route to 10.0.2.2, which the host's forwarded SSH also comes
  667      from): the frames still arrive, because the QEMU monitor is a host
  668      socket and owes the guest's routing table nothing."""
  669      before = g.stamp("exit") if ssh_poll else ""
  670      result = {"tag": tag, "stamp_before": before, "relaunch": relaunch}
  671      marks = {"gone": None, "stamp": None, "ra2": None, "relaunched": None, "answered": None}
  672      stop = threading.Event()
  673  
  674      def poll():
  675          while not stop.is_set():
  676              if marks["gone"] is None:
  677                  if g.retroarch() is None:
  678                      marks["gone"] = time.monotonic()
  679                      if relaunch:
  680                          result["http2"] = g.launch(rom)
  681                          marks["relaunched"] = time.monotonic()
  682              elif relaunch and marks["ra2"] is None:
  683                  if g.retroarch() is not None:
  684                      marks["ra2"] = time.monotonic()
  685              if marks["stamp"] is None:
  686                  now = g.stamp("exit")
  687                  if now and now != before:
  688                      marks["stamp"] = time.monotonic()
  689                      result["stamp_after"] = now
  690              if marks["stamp"] is not None and marks["gone"] is not None and not relaunch:
  691                  break
  692              time.sleep(0.12)
  693  
  694      # The guest's own clock, for the one condition that cannot be polled:
  695      # the stamp carries an epoch, so a run measured with no SSH channel
  696      # still has a duration, to the second.
  697      epoch0 = g.sh("date +%s")[1]
  698      th = None
  699      t0 = time.monotonic()
  700      g.kill_game()
  701      if ssh_poll:
  702          th = threading.Thread(target=poll, daemon=True)
  703          th.start()
  704      series, shots = [], []
  705      card_gone = game2 = None
  706      prev = None
  707      n = 0
  708      while time.monotonic() - t0 < budget:
  709          t = time.monotonic()
  710          f = fr.frame()
  711          d_rest = vq.frame_diff(rest_ref, f)
  712          d_prev = 1.0 if prev is None else vq.frame_diff(prev, f)
  713          series.append([round(t - t0, 3), round(d_rest, 6), round(d_prev, 6)])
  714          if keep_frames:
  715              shots.append(fr.save("%s-%03d" % (tag, n), f))
  716          n += 1
  717          if prev is not None:
  718              prev = f
  719          else:
  720              prev = f
  721          # The card is gone when the screen is the one the launch started
  722          # from again. Gated on the stamp where there is an SSH channel to
  723          # read it on, and on three seconds where there is not: between the
  724          # interface redrawing after the game and the card being created
  725          # there is a frame or two of plain carousel, and without a gate
  726          # the cell would call that the card leaving.
  727          if (not relaunch and card_gone is None and d_rest <= vq.SAME_MAX
  728                  and ((marks["stamp"] is not None and t > marks["stamp"])
  729                       or (not ssh_poll and t - t0 >= 3.0))):
  730              card_gone = t
  731              break
  732          # A card that never goes must not hold the cell for the whole budget:
  733          # the work ended at the stamp, and twenty seconds is far past every
  734          # linger the card has (a second and a half on success).
  735          if not relaunch and marks["stamp"] is not None and t - marks["stamp"] > 15:
  736              break
  737          # Since D-CLOUD-130 a launch over the running exit sync asks STOP IT
  738          # AND PLAY / KEEP WAITING instead of cancelling on its own. A player's
  739          # thumb answers, and so does this cell: A once, half a second after
  740          # the relaunch went -- from this thread, which owns the monitor
  741          # socket -- so the number measured is still exit to the next first
  742          # frame, the one press included. With no sync in flight the launch
  743          # has gone ahead and the A lands in the game, harmlessly.
  744          if (relaunch and marks["relaunched"] is not None and marks["answered"] is None
  745                  and time.monotonic() - marks["relaunched"] >= 0.5):
  746              fr.mon.sendkey("x")
  747              marks["answered"] = time.monotonic()
  748          if (relaunch and game2 is None and marks["ra2"] is not None
  749                  and t > marks["ra2"] and d_prev >= vq.CHANGED_MIN and not is_blank(f)):
  750              game2 = t
  751              shots.append(fr.save("%s-game2" % tag, f))
  752              break
  753          time.sleep(max(0.0, frame_every - (time.monotonic() - t)))
  754      stop.set()
  755      if th is not None:
  756          th.join(timeout=8)
  757      if marks["stamp"] is None and ssh_poll:
  758          after = g.stamp("exit")
  759          if after and after != before:
  760              marks["stamp"] = time.monotonic()
  761              result["stamp_after"] = after
  762      result.update({
  763          "t_emulator_gone": None if marks["gone"] is None else round(marks["gone"] - t0, 3),
  764          "t_sync_stamp": None if marks["stamp"] is None else round(marks["stamp"] - t0, 3),
  765          "t_card_gone": None if card_gone is None else round(card_gone - t0, 3),
  766          "t_relaunch_sent": None if marks["relaunched"] is None else round(marks["relaunched"] - t0, 3),
  767          "t_question_answered": None if marks["answered"] is None else round(marks["answered"] - t0, 3),
  768          "t_retroarch2_seen": None if marks["ra2"] is None else round(marks["ra2"] - t0, 3),
  769          "t_second_game_frame": None if game2 is None else round(game2 - t0, 3),
  770          "frames": series,
  771          "png": [x for x in shots if x],
  772      })
  773      result["stamp"] = parse_stamp(result.get("stamp_after", ""))
  774      result["epoch0"] = epoch0
  775      try:
  776          result["t_sync_stamp_clock"] = int(result["stamp"]["epoch"]) - int(epoch0)
  777      except (KeyError, ValueError, TypeError):
  778          result["t_sync_stamp_clock"] = None
  779      if result["t_sync_stamp"] is None:
  780          result["t_sync_stamp"] = result["t_sync_stamp_clock"]
  781      return result
  782  
  783  
  784  # --------------------------------------------------------------------------
  785  # host fixtures for the offline and bounds cells
  786  
  787  
  788  class Fixture:
  789      """A tiny host listener the guest's remote can be pointed at.
  790  
  791      portal: answers 302 then 200 with HTML to everything, which is what a
  792      hotel or an airport does to a device that thinks it is online.
  793      stall:  accepts the connection and never writes a byte, which is the
  794      one shape neither a refused port nor a missing route can produce and
  795      the only one that tests an idle timeout rather than a connect timeout."""
  796  
  797      def __init__(self, kind, port):
  798          self.kind, self.port = kind, port
  799          self.proc = None
  800  
  801      def up(self):
  802          code = PORTAL_SRC if self.kind == "portal" else STALL_SRC
  803          path = os.path.join(tempfile.mkdtemp(prefix="ttp-fix-"), self.kind + ".py")
  804          with open(path, "w") as fh:
  805              fh.write(code)
  806          self.path = path
  807          self.proc = subprocess.Popen([sys.executable, path, str(self.port)],
  808                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  809          for _ in range(50):
  810              import socket as _s
  811              try:
  812                  c = _s.create_connection(("127.0.0.1", self.port), 0.3)
  813                  c.close()
  814                  return True
  815              except OSError:
  816                  time.sleep(0.1)
  817          return False
  818  
  819      def down(self):
  820          if self.proc is not None:
  821              self.proc.terminate()
  822              try:
  823                  self.proc.wait(timeout=5)
  824              except subprocess.TimeoutExpired:
  825                  self.proc.kill()
  826              self.proc = None
  827          try:
  828              shutil.rmtree(os.path.dirname(self.path))
  829          except (OSError, AttributeError):
  830              pass
  831  
  832  
  833  PORTAL_SRC = '''import sys, socketserver, http.server
  834  class H(http.server.BaseHTTPRequestHandler):
  835      protocol_version = "HTTP/1.1"
  836      def _p(self):
  837          body = b"<html><head><title>Sign in to Wi-Fi</title></head><body>Sign in to continue</body></html>"
  838          if self.path != "/portal":
  839              self.send_response(302)
  840              self.send_header("Location", "http://10.0.2.2:%d/portal" % self.server.server_address[1])
  841              self.send_header("Content-Length", "0")
  842              self.end_headers()
  843              return
  844          self.send_response(200)
  845          self.send_header("Content-Type", "text/html")
  846          self.send_header("Content-Length", str(len(body)))
  847          self.end_headers()
  848          self.wfile.write(body)
  849      do_GET = do_HEAD = do_POST = do_PUT = do_DELETE = _p
  850      def do_PROPFIND(self): self._p()
  851      def do_OPTIONS(self): self._p()
  852      def do_MKCOL(self): self._p()
  853      def log_message(self, *a): pass
  854  class S(socketserver.ThreadingTCPServer):
  855      allow_reuse_address = True
  856  S(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
  857  '''
  858  
  859  STALL_SRC = '''import sys, socket, threading
  860  s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  861  s.bind(("127.0.0.1", int(sys.argv[1]))); s.listen(64)
  862  held = []
  863  while True:
  864      c, _ = s.accept()
  865      held.append(c)          # accepted, never answered, never closed
  866  '''
  867  
  868  
  869  # --------------------------------------------------------------------------
  870  # the conditions the offline and bounds cells run under
  871  
  872  
  873  def remote_stanza(backend, address_port, tool):
  874      """The guest's rclone stanza with its address moved to another port.
  875  
  876      Which field carries the address is the backend's business, not this
  877      cell's -- cloud-test-backend already answers that with dead-conf, so
  878      the refused case comes from there. For the portal and the stall the
  879      same substitution is made on a live stanza: a `url = http://...:PORT`
  880      for the two backends whose address is a URL, `port = N` for the rest."""
  881      out = subprocess.run([tool, "--backend", backend, "rclone-conf"],
  882                           capture_output=True, text=True).stdout
  883      lines = []
  884      for line in out.splitlines():
  885          s = line.strip()
  886          if s.startswith("url = "):
  887              value = s[len("url = "):]
  888              scheme, _, rest = value.partition("://")
  889              host = rest.split("/")[0].split(":")[0]
  890              line = "url = %s://%s:%d" % (scheme, host, address_port)
  891          elif s.startswith("port = "):
  892              line = "port = %d" % address_port
  893          lines.append(line)
  894      return "\n".join(lines) + "\n"
  895  
  896  
  897  def read_routes(g):
  898      """The guest's two default routes, verbatim, so they can be put back.
  899  
  900      `ip route show`'s own output is valid input to `ip route replace`, which
  901      is why this keeps the line rather than a gateway: a route re-added by
  902      hand came back without its src or its metric, and the next condition
  903      then measured a guest that was not the one the online run measured."""
  904      return {"v4": g.sh("ip -4 route show default | head -1")[1],
  905              "v6": g.sh("ip -6 route show default | head -1")[1]}
  906  
  907  
  908  # Every default route, not the first one. `ip route del default` deletes ONE
  909  # match, and a table that has picked up a second default -- which is what a
  910  # hand-added route with a different metric is -- then still has one. The
  911  # noroute cell measured a guest that was still online twice because of it.
  912  DEL_DEFAULTS = ("for i in 1 2 3 4 5 6; do ip -4 route show default | grep -q . || break; "
  913                  "ip -4 route del default; done; "
  914                  "for i in 1 2 3 4 5 6; do ip -6 route show default | grep -q . || break; "
  915                  "ip -6 route del default; done")
  916  
  917  
  918  def normalise_routes(g, routes):
  919      """Back to the routing table the online run was measured on."""
  920      cmds = ["ip route del blackhole 10.0.2.2/32 2>/dev/null",
  921              "ip link set eth0 up 2>/dev/null",
  922              "sleep 1", DEL_DEFAULTS]
  923      if routes.get("v4"):
  924          cmds.append("ip -4 route add %s" % routes["v4"])
  925      if routes.get("v6"):
  926          cmds.append("ip -6 route add %s" % routes["v6"])
  927      cmds.append("true")
  928      g.sh("; ".join(cmds))
  929      return g.sh("ip -4 route show default | head -1; ip -6 route show default | head -1")[1]
  930  
  931  
  932  def set_conf(g, text):
  933      # A fresh image has no /storage/.config/rclone -- the setup wizard makes
  934      # it -- so the copy is preceded by the directory, and a copy that fails
  935      # stops the run: on runs 99 and 100's comparisons it failed silently,
  936      # the guest had no remote, and every cell timed a sync that reached
  937      # nothing (2026-10-02; vm-qa makes the directory before it seeds).
  938      fh = tempfile.NamedTemporaryFile("w", suffix=".conf", delete=False)
  939      fh.write(text)
  940      fh.close()
  941      g.sh("mkdir -p " + os.path.dirname(RCLONE_CONF))
  942      rc = g.put(fh.name, RCLONE_CONF)
  943      os.remove(fh.name)
  944      if rc != 0:
  945          sys.exit("time-to-play: could not write the guest's %s (scp exited %d)" % (RCLONE_CONF, rc))
  946      g.sh("chmod 600 " + RCLONE_CONF)
  947  
  948  
  949  # --------------------------------------------------------------------------
  950  # statistics and the report
  951  
  952  
  953  def stats(values):
  954      vals = [v for v in values if v is not None]
  955      if not vals:
  956          return {"n": 0}
  957      return {"n": len(vals),
  958              "median": round(statistics.median(vals), 2),
  959              "mean": round(statistics.fmean(vals), 2),
  960              "max": round(max(vals), 2),
  961              "min": round(min(vals), 2),
  962              "all": [round(v, 2) for v in vals]}
  963  
  964  
  965  def fmt(st):
  966      if not st or st.get("n", 0) == 0:
  967          return "-"
  968      return "%.2f / %.2f / %.2f" % (st["median"], st["mean"], st["max"])
  969  
  970  
  971  def md_table(head, rows):
  972      out = ["| " + " | ".join(head) + " |",
  973             "| " + " | ".join("---" for _ in head) + " |"]
  974      for r in rows:
  975          out.append("| " + " | ".join("-" if c is None else str(c) for c in r) + " |")
  976      return "\n".join(out) + "\n"
  977  
  978  
  979  # --------------------------------------------------------------------------
  980  # main
  981  
  982  
  983  def main():
  984      ap = argparse.ArgumentParser(
  985          description="Measure time to play on one GENERIC_X64 guest (#135).",
  986          formatter_class=argparse.RawDescriptionHelpFormatter,
  987          epilog=__doc__)
  988      ap.add_argument("--host", default="root@127.0.0.1")
  989      ap.add_argument("--port", default="10022", help="the guest's forwarded SSH port")
  990      ap.add_argument("--identity", default="/tmp/rocknix-vm-pair/qa-key")
  991      ap.add_argument("--monitor", required=True, help="the guest's QEMU monitor socket")
  992      ap.add_argument("--backend", default=os.environ.get("CLOUD_QA_BACKEND", "webdav"),
  993                      help="which QA cloud the guest's remote points at")
  994      ap.add_argument("--repeat", type=int, default=5)
  995      ap.add_argument("--out", required=True)
  996      ap.add_argument("--only", default="launch,exit,g2g,startup,offline,bounds",
  997                      help="cells to run: launch,exit,g2g,startup,offline,bounds")
  998      ap.add_argument("--label", default="", help="the host state these numbers were taken under")
  999      ap.add_argument("--payload", default="full", choices=("full", "srm"),
 1000                      help="full: an auto-state, two manual states, their screenshots and a battery save "
 1001                           "(D-CLOUD-116). srm: one changed battery save (P-13).")
 1002      ap.add_argument("--rom", default=ROM)
 1003      ap.add_argument("--conditions", default="",
 1004                      help="only these offline/bounds cells, comma separated "
 1005                           "(dead,noroute,blackhole,linkdown,portal,stall)")
 1006      ap.add_argument("--stall-budget", type=float, default=420.0,
 1007                      help="how long to watch the stalled-endpoint cell before giving up")
 1008      ap.add_argument("--quick", action="store_true",
 1009                      help="the runner's bounded form: one repeat of launch+exit+g2g, no reboot, no fixtures")
 1010      ap.add_argument("--no-configure-remote", action="store_true",
 1011                      help="leave the guest's rclone.conf alone (it already points where you want)")
 1012      ap.add_argument("--vm", action="store_true",
 1013                      help="the guest is a QEMU VM with no Vulkan: set RetroArch's video driver to gl "
 1014                           "for the run and put it back after (the exit test's rule). Never for a handheld.")
 1015      args = ap.parse_args()
 1016  
 1017      if args.quick:
 1018          args.repeat = 1
 1019          args.only = "launch,exit,g2g"
 1020  
 1021      only = [c.strip() for c in args.only.split(",") if c.strip()]
 1022      out = os.path.abspath(args.out)
 1023      os.makedirs(out, exist_ok=True)
 1024      frames_dir = os.path.join(out, "frames")
 1025      tool = os.path.join(HERE, "cloud-test-backend")
 1026  
 1027      g = Guest(args.host, args.port, args.identity)
 1028      if not g.wait_alive(120):
 1029          print("time-to-play: guest at %s does not answer" % args.port, file=sys.stderr)
 1030          return 1
 1031      # EmulationStation reads cloudsaves.gameexit and cloudsaves.startup when
 1032      # it starts and keeps them in memory; set_setting changes the file and
 1033      # nothing else. So the values this cell needs go into the file BEFORE the
 1034      # boot the cell relies on, and a guest whose interface booted on other
 1035      # values is rebooted -- or the exit sync never runs, the stamp never
 1036      # appears, and the cell reports nothing (the runner's second dispatch,
 1037      # fresh pair, 2026-09-12: file 1, interface booted on 0, no stamp; a
 1038      # reboot with the file at 1, stamp `completed`).
 1039      saved_startup = g.sh(". /etc/profile; get_setting cloudsaves.startup")[1]
 1040      saved_gameexit = g.sh(". /etc/profile; get_setting cloudsaves.gameexit")[1]
 1041      g.sh(". /etc/profile; set_setting cloudsaves.gameexit 1; set_setting cloudsaves.startup 0", timeout=120)
 1042      settings_changed = (saved_gameexit != "1") or (saved_startup not in ("0", ""))
 1043      # Before the helpers: a seeded ROM costs a reboot, and /tmp is a tmpfs.
 1044      made = {"rom": False}
 1045      rom, made["rom"] = ensure_rom(g, args.rom, out)
 1046      if made["rom"] or settings_changed:
 1047          reboot_guest(g)
 1048      install_helpers(g)
 1049  
 1050      build = g.sh('sed -n "s/^BUILD_ID=//p" /etc/os-release')[1].strip('"')[:10]
 1051      report = {
 1052          "build": build, "backend": args.backend, "port": args.port,
 1053          "repeat": args.repeat, "payload": args.payload,
 1054          "host_state": args.label or "(not stated)",
 1055          "started": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
 1056          "rom": rom, "rom_seeded": made["rom"],
 1057          "interface_rebooted": bool(made["rom"] or settings_changed),
 1058          "settings_before": {"gameexit": saved_gameexit, "startup": saved_startup},
 1059          "cells": {},
 1060      }
 1061  
 1062      # Everything this cell changes on the guest, and the value to put back.
 1063      saved_conf = os.path.join(out, "rclone.conf.saved")
 1064      saved_cloud = os.path.join(out, "cloud_sync.conf.saved")
 1065      subprocess.run(["scp", "-q", "-P", g.port] + g._opts() +
 1066                     [g.host + ":" + RCLONE_CONF, saved_conf], capture_output=True)
 1067      subprocess.run(["scp", "-q", "-P", g.port] + g._opts() +
 1068                     [g.host + ":" + CLOUD_CONF, saved_cloud], capture_output=True)
 1069      # A QEMU guest has no Vulkan. On the vulkan the GENERIC_X64 profile
 1070      # shipped until a5a03bd9fa, RetroArch exists for a fifth of a second and
 1071      # never draws, the exit sync never runs, and every headline number below
 1072      # is a dash -- which is what the runner's first dispatch of this cell
 1073      # reported as a PASS (2026-09-12). The profile ships gl now, and the boot
 1074      # quirk 092-retroarch-surface moves a cfg still on vulkan to gl while the
 1075      # image has no Vulkan driver; the swap stays, for a guest whose cfg says
 1076      # otherwise. The exit test has always swapped the driver for its run.
 1077      saved_vd = ""
 1078      saved_gs = ""
 1079      if args.vm:
 1080          saved_vd = g.sh('grep -E "^video_driver" ' + RETROARCH_CFG)[1].strip()
 1081          g.sh("sed -i 's/^video_driver = .*/video_driver = \"gl\"/' " + RETROARCH_CFG)
 1082          # The surface check reads RetroArch's GPU screenshot (surface_check):
 1083          # on for the run, put back after it.
 1084          saved_gs = g.sh('grep -E "^video_gpu_screenshot" ' + RETROARCH_CFG)[1].strip()
 1085          g.sh("grep -q '^video_gpu_screenshot' %s && sed -i 's/^video_gpu_screenshot = .*/video_gpu_screenshot = \"true\"/' %s || echo 'video_gpu_screenshot = \"true\"' >> %s" % (RETROARCH_CFG, RETROARCH_CFG, RETROARCH_CFG))
 1086      fixtures = []
 1087  
 1088      def restore():
 1089          for f in fixtures:
 1090              f.down()
 1091          # Put back as found, and said when it could not be: a restore that
 1092          # fails leaves the guest on the run's settings.
 1093          if os.path.exists(saved_conf) and os.path.getsize(saved_conf) > 0:
 1094              if g.put(saved_conf, RCLONE_CONF) != 0:
 1095                  print("time-to-play: could not put the guest's rclone.conf back", file=sys.stderr)
 1096              g.sh("chmod 600 " + RCLONE_CONF)
 1097          if os.path.exists(saved_cloud) and os.path.getsize(saved_cloud) > 0:
 1098              if g.put(saved_cloud, CLOUD_CONF) != 0:
 1099                  print("time-to-play: could not put the guest's cloud_sync.conf back", file=sys.stderr)
 1100          g.sh("ip route show default | grep -q . || ip route add default via 10.0.2.2 dev eth0 2>/dev/null; "
 1101               "ip route del blackhole 10.0.2.2/32 2>/dev/null; true")
 1102          g.sh(". /etc/profile; set_setting cloudsaves.startup %s; set_setting cloudsaves.gameexit %s"
 1103               % (saved_startup or "0", saved_gameexit or "1"), timeout=120)
 1104          g.sh("rm -f /tmp/ttp-kill /tmp/ttp-arm.sh")
 1105          if args.vm and saved_vd:
 1106              g.sh("sed -i 's/^video_driver = .*/%s/' %s"
 1107                   % (saved_vd.replace("\\", "\\\\").replace("/", "\\/").replace("&", "\\&"), RETROARCH_CFG))
 1108          if args.vm:
 1109              if saved_gs:
 1110                  g.sh("sed -i 's/^video_gpu_screenshot = .*/%s/' %s"
 1111                       % (saved_gs.replace("\\", "\\\\").replace("/", "\\/").replace("&", "\\&"), RETROARCH_CFG))
 1112              else:
 1113                  g.sh("sed -i '/^video_gpu_screenshot = \"true\"$/d' " + RETROARCH_CFG)
 1114          if made["rom"]:
 1115              g.sh("rm -f %s; rmdir /storage/roms/gb 2>/dev/null; true" % GB_PROBE)
 1116  
 1117      def on_signal(signum, _frame):
 1118          restore()
 1119          sys.exit(128 + signum)
 1120  
 1121      signal.signal(signal.SIGINT, on_signal)
 1122      signal.signal(signal.SIGTERM, on_signal)
 1123  
 1124      fr = Frames(args.monitor, frames_dir)
 1125      try:
 1126          # The harness's own cost, reported beside the numbers rather than
 1127          # subtracted from them: the POST that starts a launch goes over the
 1128          # SSH channel, so its round trip is inside the launch number.
 1129          rtts = []
 1130          for _ in range(7):
 1131              a = time.monotonic()
 1132              g.sh("true")
 1133              rtts.append(time.monotonic() - a)
 1134          fps = []
 1135          for _ in range(5):
 1136              a = time.monotonic()
 1137              fr.frame()
 1138              fps.append(time.monotonic() - a)
 1139          report["ssh_rtt_median_s"] = round(statistics.median(rtts), 4)
 1140          report["frame_poll_median_s"] = round(statistics.median(fps), 4)
 1141  
 1142          if not args.no_configure_remote:
 1143              set_conf(g, subprocess.run([tool, "--backend", args.backend, "rclone-conf"],
 1144                                         capture_output=True, text=True).stdout)
 1145              # And the three remote PATHS, which are a different shape on every
 1146              # backend: a folder on WebDAV and FTP, a bucket or a share first on
 1147              # S3 and SMB, an absolute filesystem path on SFTP. Writing the
 1148              # stanza without writing these ran the whole cell against
 1149              # /ROCKNIX/Saves on an sshd that cannot create it.
 1150              prefix = subprocess.run([tool, "--backend", args.backend, "endpoint-prefix"],
 1151                                      capture_output=True, text=True).stdout.strip()
 1152              # The shipped folders, read from cloud_sync.conf.defaults through the
 1153              # backend tool, never a literal: this wrote /ROCKNIX/..., the
 1154              # previous default, after the default moved, so on the builds whose
 1155              # syncs checked an earlier folder first (until D-CLOUD-170) every
 1156              # measured exit sync paid that check, a cost the shipped default
 1157              # never pays (2026-10-01, blindspot 71's second instance).
 1158              def shipped(key):
 1159                  r = subprocess.run([tool, "shipped-default", key], capture_output=True, text=True)
 1160                  if r.returncode != 0 or not r.stdout.strip():
 1161                      sys.exit("time-to-play: no shipped default for %s: %s" % (key, r.stderr.strip()))
 1162                  return r.stdout.strip()
 1163              g.sh("sed -i 's#^SAVES_REMOTE=.*#SAVES_REMOTE=\"%s%s\"#; "
 1164                   "s#^SETTINGS_REMOTE=.*#SETTINGS_REMOTE=\"%s%s\"#; "
 1165                   "s#^CONTENT_REMOTE=.*#CONTENT_REMOTE=\"%s%s\"#' %s"
 1166                   % (prefix, shipped("SAVES_REMOTE"), prefix, shipped("SETTINGS_REMOTE"),
 1167                      prefix, shipped("CONTENT_REMOTE"), CLOUD_CONF))
 1168              report["remotes"] = g.sh(
 1169                  "grep -E '^(SAVES_REMOTE|SETTINGS_REMOTE|CONTENT_REMOTE)=' " + CLOUD_CONF)[1]
 1170          g.sh(". /etc/profile; set_setting cloudsaves.gameexit 1", timeout=120)
 1171          # Probed for up to a minute, for a guest whose link is still coming
 1172          # up; then the answer stands, and a "no" still fails the run. (The
 1173          # "no" that runs 99 and 100's comparisons read was a conf never
 1174          # written -- set_conf -- not a slow link, which this loop was first
 1175          # added for on a wrong reading, 2026-10-01.)
 1176          for _ in range(12):
 1177              report["remote_reachable"] = g.sh(
 1178                  "rclone lsd qa-cloud: --contimeout 10s --timeout 20s --low-level-retries 1 --retries 1 "
 1179                  ">/dev/null 2>&1 && echo yes || echo no", timeout=60)[1]
 1180              if report["remote_reachable"].strip() == "yes":
 1181                  break
 1182              time.sleep(5)
 1183  
 1184          def cycle(tag, relaunch, jitter, keep_frames=False):
 1185              """One whole online cycle: seed, launch, play, exit."""
 1186              size = seed_payload(g, jitter, args.payload)
 1187              # The screen the launch started from IS the screen the card
 1188              # will have to leave, so it is the one to compare against. It
 1189              # used to be re-taken after the game had started, which made
 1190              # the reference a picture of the game -- and the card then
 1191              # never "went", on any repeat.
 1192              L, rest_ref = measure_launch(g, fr, tag + "-launch", rom=rom)
 1193              if "surface" not in report:
 1194                  report["surface"] = surface_check(g, fr, rom)
 1195              L["payload_kib"] = size
 1196              wait_drawing(g)
 1197              E = measure_exit(g, fr, tag + "-exit", rest_ref, relaunch=relaunch,
 1198                               keep_frames=keep_frames, rom=rom)
 1199              E["payload_kib"] = size
 1200              E["log"] = g.sh("tail -25 /var/log/cloud_sync.log 2>/dev/null | cut -c1-200")[1]
 1201              if relaunch:
 1202                  # game two is running; end it and let its own sync settle
 1203                  wait_drawing(g, budget=30)
 1204                  settle_sync(g)
 1205              return L, E
 1206  
 1207          # --- launch + exit, the online baseline ---------------------------
 1208          if "launch" in only or "exit" in only:
 1209              L, E = [], []
 1210              for i in range(args.repeat):
 1211                  a, b = cycle("r%d" % (i + 1), False, i, keep_frames=(i == 0))
 1212                  L.append(a)
 1213                  E.append(b)
 1214                  settle_sync(g)
 1215              report["cells"]["launch"] = L
 1216              report["cells"]["exit"] = E
 1217  
 1218          # --- game to game -------------------------------------------------
 1219          if "g2g" in only:
 1220              G2 = []
 1221              for i in range(args.repeat):
 1222                  _, b = cycle("g%d" % (i + 1), True, i, keep_frames=(i == 0))
 1223                  G2.append(b)
 1224                  settle_sync(g)
 1225              report["cells"]["g2g"] = G2
 1226  
 1227          # --- the startup sync ---------------------------------------------
 1228          if "startup" in only:
 1229              report["cells"]["startup"] = measure_startup(g, fr, args, out, rom)
 1230  
 1231          # --- offline and bounds -------------------------------------------
 1232          conds = []
 1233          if "offline" in only:
 1234              conds += ["dead", "noroute", "blackhole", "linkdown", "portal"]
 1235          if "bounds" in only:
 1236              for c in ("dead", "stall", "portal"):
 1237                  if c not in conds:
 1238                      conds.append(c)
 1239          if args.conditions:
 1240              want = [c.strip() for c in args.conditions.split(",") if c.strip()]
 1241              conds = [c for c in want if c in conds] or want
 1242          results = {}
 1243          routes = read_routes(g) if conds else None
 1244          for cond in conds:
 1245              results[cond] = run_condition(g, fr, cond, args, tool, fixtures, rom, routes)
 1246              # put the remote back between conditions
 1247              if not args.no_configure_remote:
 1248                  set_conf(g, subprocess.run([tool, "--backend", args.backend, "rclone-conf"],
 1249                                             capture_output=True, text=True).stdout)
 1250              settle_sync(g)
 1251          if results:
 1252              report["cells"]["conditions"] = results
 1253      finally:
 1254          try:
 1255              fr.close()
 1256          except Exception:
 1257              pass
 1258          restore()
 1259          g.drop_master()
 1260  
 1261      report["finished"] = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
 1262      md = render(report)
 1263      # A run that ran cleanly and measured nothing is not a pass. The first
 1264      # dispatch from the runner printed every headline as "-" and exited 0
 1265      # (RetroArch never drew; see --vm), and the report table said PASS.
 1266      missing = headline_missing(report)
 1267      report["headline_missing"] = missing
 1268      over = over_budget(report)
 1269      report["over_budget"] = over
 1270      if missing:
 1271          md += "\n**Not a pass:** " + "; ".join(missing) + ".\n"
 1272      if over:
 1273          md += "\n**Over budget:** " + "; ".join(over) + ".\n"
 1274      with open(os.path.join(out, "time-to-play.json"), "w") as fh:
 1275          json.dump(report, fh, indent=1)
 1276      with open(os.path.join(out, "time-to-play.md"), "w") as fh:
 1277          fh.write(md)
 1278      print(md)
 1279      print("frames and json: %s" % out)
 1280      if missing or over:
 1281          print("time-to-play: FAIL -- " + "; ".join(missing + over), file=sys.stderr)
 1282          return 1
 1283      return 0
 1284  
 1285  
 1286  # The budgets the register carries, and a run over one fails the suite (#135
 1287  # AC 2). D-CLOUD-119 (2026-09-12): the exit sync of one changed battery save
 1288  # on a hashed cloud within 3 s -- measured 0.79 s on S3, 1.0-1.7 s with the
 1289  # full payload on WebDAV and SFTP. Judged on the median of the exit cell's
 1290  # stamp time, the same number the report's headline shows; a cell that did
 1291  # not run is not judged (headline_missing says so). No row yet bounds the
 1292  # launch (0.6-0.9 s measured) or the game-to-game number, so neither fails.
 1293  EXIT_SYNC_BUDGET_S = 3.0
 1294  
 1295  def over_budget(report):
 1296      out = []
 1297      rows = [r for r in (report["cells"].get("exit") or []) if r.get("t_sync_stamp") is not None]
 1298      if rows:
 1299          med = statistics.median(r["t_sync_stamp"] for r in rows)
 1300          if med > EXIT_SYNC_BUDGET_S:
 1301              out.append("the exit sync's stamp took %.2f s (median of %d), over D-CLOUD-119's %.0f s"
 1302                         % (med, len(rows), EXIT_SYNC_BUDGET_S))
 1303      return out
 1304  
 1305  
 1306  def headline_missing(report):
 1307      """The numbers this cell exists to report, and how many repeats lacked
 1308      each. An assertion that cannot fail is not evidence
 1309      (engineering-practices.md), and a table of dashes under a PASS line is
 1310      exactly that. Cells that did not run are not judged."""
 1311      checks = [("launch", "t_first_game_frame", "the game's first frame"),
 1312                ("exit", "t_sync_stamp", "the exit sync's stamp"),
 1313                ("g2g", "t_second_game_frame", "the next game's first frame")]
 1314      out = []
 1315      surf = report.get("surface") or {}
 1316      if surf.get("scaled"):
 1317          out.append("RetroArch drew into a %s surface under a %s panel, by %s: the frames are scaled (#263)" % (surf.get("surface"), surf.get("panel"), surf.get("source")))
 1318      elif report.get("cells", {}).get("launch") and surf.get("surface") is None:
 1319          out.append("RetroArch's surface size could not be read from the guest's exec.log (#263)")
 1320      # The online cells time a sync that reaches a cloud. On a guest whose cloud
 1321      # is not set up -- a lone --only run on a fresh pair, 2026-09-25 -- the sync
 1322      # ends at once with YOUR CLOUD STORAGE ISN'T SET UP YET, and its stamp
 1323      # comes in well under the budget for having done nothing.
 1324      if (report.get("cells", {}).get("exit") or report.get("cells", {}).get("g2g")) and report.get("remote_reachable") != "yes":
 1325          out.append("the exit sync had no cloud to reach (rclone lsd qa-cloud: %s): its stamp times a sync that did nothing"
 1326                     % (report.get("remote_reachable") or "not checked"))
 1327      for cell, field, what in checks:
 1328          rows = report["cells"].get(cell) or []
 1329          n = sum(1 for r in rows if r.get(field) is None)
 1330          if n:
 1331              out.append("%s missing in %d of %d %s repeat(s)" % (what, n, len(rows), cell))
 1332      return out
 1333  
 1334  
 1335  def measure_startup(g, fr, args, out, rom=ROM):
 1336      """Boot to the startup card's end, and a launch pressed while it runs."""
 1337      res = {}
 1338      g.sh(". /etc/profile; set_setting cloudsaves.startup 1", timeout=180)
 1339      seed_payload(g, 3, args.payload)
 1340      for arm, launch_during in (("boot", False), ("boot-launch", True)):
 1341          before = g.stamp("startup")
 1342          t0 = time.monotonic()
 1343          g.sh("systemctl reboot")
 1344          g.drop_master()
 1345          time.sleep(6)
 1346          entry = {"stamp_before": before}
 1347          if not g.wait_alive(240):
 1348              entry["error"] = "the guest did not come back"
 1349              res[arm] = entry
 1350              continue
 1351          entry["t_ssh_back"] = round(time.monotonic() - t0, 2)
 1352          # EmulationStation, then the stamp the startup sync writes
 1353          es = None
 1354          launched = None
 1355          gameframe = None
 1356          stamped = None
 1357          prev = None
 1358          end = time.monotonic() + 240
 1359          while time.monotonic() < end:
 1360              if es is None and g.es_up():
 1361                  es = time.monotonic()
 1362                  entry["t_es_up"] = round(es - t0, 2)
 1363              if stamped is None:
 1364                  now = g.stamp("startup")
 1365                  if now and now != before:
 1366                      stamped = time.monotonic()
 1367                      entry["stamp_after"] = now
 1368                      entry["t_startup_stamp"] = round(stamped - t0, 2)
 1369                      if not launch_during:
 1370                          break
 1371              if launch_during and es is not None and launched is None and stamped is None:
 1372                  # press a game while the startup sync is still running
 1373                  launched = time.monotonic()
 1374                  entry["http"] = g.launch(rom)
 1375                  entry["t_launch_sent"] = round(launched - t0, 2)
 1376              if launch_during and launched is not None and gameframe is None:
 1377                  f = fr.frame()
 1378                  if (prev is not None and vq.frame_diff(prev, f) >= vq.CHANGED_MIN
 1379                          and not is_blank(f) and g.retroarch() is not None):
 1380                      gameframe = time.monotonic()
 1381                      entry["t_game_frame_after_launch"] = round(gameframe - launched, 2)
 1382                      entry["png"] = fr.save("startup-%s-game" % arm, f)
 1383                  prev = f
 1384              if launch_during and gameframe is not None and stamped is not None:
 1385                  break
 1386              time.sleep(0.25)
 1387          entry["stamp_after"] = entry.get("stamp_after") or g.stamp("startup")
 1388          entry["stamp"] = parse_stamp(entry["stamp_after"])
 1389          entry["exit_stamp"] = parse_stamp(g.stamp("exit"))
 1390          if launch_during:
 1391              wait_drawing(g, budget=40)
 1392              g.kill_game()
 1393              time.sleep(10)
 1394          res[arm] = entry
 1395      g.sh(". /etc/profile; set_setting cloudsaves.startup 0", timeout=180)
 1396      return res
 1397  
 1398  
 1399  def run_condition(g, fr, cond, args, tool, fixtures, rom=ROM, routes=None):
 1400      """One offline or bounds cell: set the condition, exit a game, measure."""
 1401      entry = {"condition": cond}
 1402      if routes:
 1403          entry["routes_normalised"] = normalise_routes(g, routes)
 1404      live = subprocess.run([tool, "--backend", args.backend, "rclone-conf"],
 1405                            capture_output=True, text=True).stdout
 1406      fixture = None
 1407      if cond == "dead":
 1408          entry["how"] = "the remote points at the refused port %d" % DEAD_PORT
 1409          set_conf(g, subprocess.run([tool, "--backend", args.backend, "dead-conf"],
 1410                                     capture_output=True, text=True).stdout)
 1411      elif cond == "portal":
 1412          entry["how"] = ("a captive portal on 127.0.0.1:%d answering 302 then 200 to everything, "
 1413                          "with the remote pointed at it" % PORTAL_PORT)
 1414          fixture = Fixture("portal", PORTAL_PORT)
 1415          fixture.up()
 1416          fixtures.append(fixture)
 1417          set_conf(g, remote_stanza(args.backend, PORTAL_PORT, tool))
 1418      elif cond == "stall":
 1419          entry["how"] = ("an endpoint on 127.0.0.1:%d that accepts and never answers, "
 1420                          "with the remote pointed at it" % STALL_PORT)
 1421          fixture = Fixture("stall", STALL_PORT)
 1422          fixture.up()
 1423          fixtures.append(fixture)
 1424          set_conf(g, remote_stanza(args.backend, STALL_PORT, tool))
 1425      elif cond in ("noroute", "blackhole", "linkdown"):
 1426          entry["how"] = {
 1427              "noroute": "both default routes removed (v4 and v6: deleting only the v4 one leaves "
 1428                         "the v6 default, and the scripts' has_default_route reads that as online)",
 1429              "blackhole": "a blackhole route to 10.0.2.2 added 0.4 s after the exit, so the "
 1430                           "connection can open and then the path to the cloud goes",
 1431              "linkdown": "eth0 taken down 0.5 s after the exit -- a handheld leaving Wi-Fi",
 1432          }[cond]
 1433          set_conf(g, live)
 1434  
 1435      seed_payload(g, 7, args.payload)
 1436      entry["routes_before"] = g.sh("ip -4 route show")[1]
 1437      L, rest_ref = measure_launch(g, fr, "cond-%s-launch" % cond, rom=rom)
 1438      entry["launch"] = {k: L[k] for k in ("t_left_carousel", "t_retroarch_seen",
 1439                                           "t_first_game_frame", "t_ticks200")}
 1440      wait_drawing(g)
 1441  
 1442      if cond == "noroute":
 1443          # BOTH families. The QA endpoint is on the guest's own /24, so a
 1444          # missing v4 default does not cut it -- and the scripts do not test
 1445          # reachability first, they test `is there a default route`, which on
 1446          # this guest the v6 one answers yes to. Deleting only the v4 default
 1447          # left the exit sync completing normally in 1.3 s (2026-09-12).
 1448          entry["route_cmd"] = g.sh(DEL_DEFAULTS + "; echo 'left:'; "
 1449                                    "ip -4 route show default; ip -6 route show default")[1]
 1450          E = measure_exit(g, fr, "cond-%s" % cond, rest_ref, budget=120, rom=rom)
 1451          if routes:
 1452              normalise_routes(g, routes)
 1453      elif cond in ("blackhole", "linkdown"):
 1454          # SSH from the host arrives from 10.0.2.2, so a blackhole to it
 1455          # stalls this channel too -- an admin-down link does not reset an
 1456          # established connection. So the cut is armed inside the guest, the
 1457          # master is dropped, and the measurement runs on frames alone until
 1458          # the route comes back.
 1459          cut, back = (("ip route add blackhole 10.0.2.2/32",
 1460                        "ip route del blackhole 10.0.2.2/32 2>/dev/null")
 1461                       if cond == "blackhole" else
 1462                       ("ip link set eth0 down", "ip link set eth0 up"))
 1463          # Half a second, not two: the online exit sync ends in 1.4 s, and a
 1464          # cut armed for +2 s arrived after the sync had completed -- the cell
 1465          # reported `completed` and measured nothing (2026-09-12).
 1466          g.sh('cat > /tmp/ttp-arm.sh <<"H"\n'
 1467               '#!/bin/sh\n'
 1468               'sleep 0.5\n'
 1469               '%s\n'
 1470               'sleep 60\n'
 1471               '%s\n'
 1472               'H\n'
 1473               'chmod +x /tmp/ttp-arm.sh; setsid /tmp/ttp-arm.sh >/dev/null 2>&1 & echo armed'
 1474               % (cut, back))
 1475          E = measure_exit(g, fr, "cond-%s" % cond, rest_ref, budget=100,
 1476                           ssh_poll=False, rom=rom)
 1477          g.drop_master()
 1478          g.wait_alive(240)
 1479          if routes:
 1480              normalise_routes(g, routes)
 1481          E["stamp_after"] = g.stamp("exit")
 1482          E["stamp"] = parse_stamp(E["stamp_after"])
 1483          try:
 1484              E["t_sync_stamp_clock"] = int(E["stamp"]["epoch"]) - int(E["epoch0"])
 1485              E["t_sync_stamp"] = E["t_sync_stamp_clock"]
 1486          except (KeyError, ValueError, TypeError):
 1487              pass
 1488      else:
 1489          # The stall is the one cell with no bound behind it: nothing in the
 1490          # scripts or in rclone's flags ends a connection that was accepted
 1491          # and then went quiet before the handshake, so the budget here is
 1492          # the measurement, not a timeout of ours.
 1493          E = measure_exit(g, fr, "cond-%s" % cond, rest_ref,
 1494                           budget=(args.stall_budget if cond == "stall" else 150), rom=rom)
 1495  
 1496      E["log"] = g.sh("tail -30 /var/log/cloud_sync.log 2>/dev/null | cut -c1-200")[1]
 1497      entry["exit"] = E
 1498      entry["routes_after"] = g.sh("ip -4 route show")[1]
 1499      if fixture is not None:
 1500          fixture.down()
 1501          if fixture in fixtures:
 1502              fixtures.remove(fixture)
 1503      return entry
 1504  
 1505  
 1506  def render(r):
 1507      L = r["cells"].get("launch", [])
 1508      E = r["cells"].get("exit", [])
 1509      G = r["cells"].get("g2g", [])
 1510      C = r["cells"].get("conditions", {})
 1511      S = r["cells"].get("startup", {})
 1512      lines = ["# time to play -- %s on %s" % (r["build"], r["backend"]),
 1513               "",
 1514               "%s, guest at :%s, cloud `%s`, payload `%s`, %d repeat(s)."
 1515               % (r["started"], r["port"], r["backend"], r["payload"], r["repeat"]),
 1516               "",
 1517               "Host state: **%s**. SSH round trip %.0f ms (the launch POST goes over it); "
 1518               "one screendump %.0f ms, which is the resolution of every frame-derived number below."
 1519               % (r["host_state"], r.get("ssh_rtt_median_s", 0) * 1000,
 1520                  r.get("frame_poll_median_s", 0) * 1000),
 1521               "", "Seconds, as median / mean / max.", ""]
 1522  
 1523      if L:
 1524          lines.append("## UI to game, at rest\n")
 1525          lines.append(md_table(
 1526              ["from the press to", "median / mean / max", "n"],
 1527              [["the screen leaving the carousel", fmt(stats([x["t_left_carousel"] for x in L])), len(L)],
 1528               ["the handover (a black screen)", fmt(stats([x.get("t_screen_blank") for x in L])), len(L)],
 1529               ["RetroArch existing", fmt(stats([x["t_retroarch_seen"] for x in L])), len(L)],
 1530               ["**the game's first frame**", "**%s**" % fmt(stats([x["t_first_game_frame"] for x in L])), len(L)],
 1531               ["RetroArch drawing (200 CPU ticks, or 30 four seconds on)", fmt(stats([x["t_ticks200"] for x in L])), len(L)]]))
 1532      if E:
 1533          toks = {}
 1534          for x in E:
 1535              t = x.get("stamp", {}).get("token", "?")
 1536              toks[t] = toks.get(t, 0) + 1
 1537          lines.append("## The exit sync, on its own\n")
 1538          lines.append(md_table(
 1539              ["from execute_kill to", "median / mean / max", "n"],
 1540              [["the emulator gone", fmt(stats([x["t_emulator_gone"] for x in E])), len(E)],
 1541               ["**the last-sync-exit stamp**", "**%s**" % fmt(stats([x["t_sync_stamp"] for x in E])), len(E)],
 1542               ["the card gone from the screen", fmt(stats([x["t_card_gone"] for x in E])), len(E)]]))
 1543          # What was seeded, not what moved: RetroArch replaces the auto-state
 1544          # on its way out, so the transferred total is smaller. The rclone
 1545          # line in each cell's log is the authority on bytes.
 1546          lines.append("Outcomes: %s. Payload seeded %s KiB (RetroArch rewrites the auto-state on exit, "
 1547                       "so what moves is a little less; the log's rclone line has the bytes).\n"
 1548                       % (", ".join("%s x%d" % (k, v) for k, v in toks.items()),
 1549                          E[0].get("payload_kib", "?")))
 1550      if G:
 1551          toks = {}
 1552          for x in G:
 1553              t = x.get("stamp", {}).get("token", "?")
 1554              toks[t] = toks.get(t, 0) + 1
 1555          lines.append("## Game to game, with the exit sync in flight\n")
 1556          lines.append(md_table(
 1557              ["from execute_kill to", "median / mean / max", "n"],
 1558              [["the emulator gone", fmt(stats([x["t_emulator_gone"] for x in G])), len(G)],
 1559               ["the relaunch sent", fmt(stats([x["t_relaunch_sent"] for x in G])), len(G)],
 1560               ["the question answered (STOP IT AND PLAY, D-CLOUD-130)", fmt(stats([x.get("t_question_answered") for x in G])), len(G)],
 1561               ["**the next game's first frame**", "**%s**" % fmt(stats([x["t_second_game_frame"] for x in G])), len(G)],
 1562               ["the exit sync's stamp", fmt(stats([x["t_sync_stamp"] for x in G])), len(G)]]))
 1563          lines.append("What the launch did to the sync, from the stamp's token: %s.\n"
 1564                       % ", ".join("`%s` x%d" % (k, v) for k, v in toks.items()))
 1565      if S:
 1566          rows = []
 1567          for arm, e in S.items():
 1568              rows.append([arm, e.get("t_es_up"), e.get("t_startup_stamp"),
 1569                           e.get("t_launch_sent"), e.get("t_game_frame_after_launch"),
 1570                           e.get("stamp", {}).get("token")])
 1571          lines.append("## The startup sync\n")
 1572          lines.append(md_table(
 1573              ["arm", "ES up (s from reboot)", "startup stamp (s from reboot)",
 1574               "launch sent (s)", "launch to game frame (s)", "stamp token"], rows))
 1575      if C:
 1576          online = stats([x["t_sync_stamp"] for x in E]) if E else {}
 1577          rows = []
 1578          if online:
 1579              rows.append(["**online (%s)**" % r["backend"], "a successful sync",
 1580                           fmt(online), "completed"])
 1581          for cond, e in C.items():
 1582              ex = e.get("exit", {})
 1583              rows.append([cond, e.get("how", ""),
 1584                           "-" if ex.get("t_sync_stamp") is None else "%.2f" % ex["t_sync_stamp"],
 1585                           ex.get("stamp", {}).get("token", "?")])
 1586          lines.append("## Offline and bounds, beside the online run\n")
 1587          lines.append(md_table(
 1588              ["cell", "how", "execute_kill to the stamp (s)", "outcome token"], rows))
 1589      return "\n".join(lines) + "\n"
 1590  
 1591  
 1592  if __name__ == "__main__":
 1593      sys.exit(main())
 1594  
```

## file, whole, at 8ebaf8daad: tools/vm-manager-system-check

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated (https://github.com/pixelelated)
    4  """Refuse a manager walk whose requested system is absent or not selected."""
    5  import json
    6  import sys
    7  
    8  try:
    9      expected, selected = sys.argv[1:]
   10      systems = json.load(sys.stdin)
   11      matches = [s for s in systems if s.get('name') == expected]
   12      assert len(matches) == 1, 'requested system is missing or duplicated'
   13      assert matches[0].get('visible') == 'true', 'requested system is not visible'
   14      assert matches[0].get('visibleGames', 0) > 0, 'requested system has no visible games'
   15      assert selected == expected, 'actual selected system is %r, expected %r' % (selected, expected)
   16  except (ValueError, AssertionError, TypeError) as error:
   17      print('FAIL manager system: ' + str(error), file=sys.stderr)
   18      sys.exit(1)
   19  print('PASS actual selected manager system ' + expected)
   20  
```

## file, whole, at 8ebaf8daad: tools/vm-pair

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # Two GENERIC_X64 guests from one image, for the tests that need two devices
    6  # against one cloud: a conflict is a change on both sides since they last
    7  # agreed, and one guest cannot make one. Conflict and bisync testing runs
    8  # here and never on a handheld (D-QA-009).
    9  #
   10  #   ./tools/vm-pair up <ROCKNIX-GENERIC_X64...img.gz>   # two 16 GiB disks, two headless guests, a QA key in each
   11  #   ./tools/vm-pair ssh a 'uname -r'                     # a command over SSH (the harness's transport)
   12  #   ./tools/vm-pair serial b 'df -h /storage'            # a command over the serial console
   13  #   ./tools/vm-pair info                                 # ports, sockets, the key
   14  #   ./tools/vm-pair down                                 # both, by pidfile
   15  #   ./tools/vm-pair reimage b <other...img.gz>           # one guest rebuilt from another image, the other left running
   16  #
   17  # Guest a keeps generic-x64-vm's defaults (SSH 10022, monitor and serial at
   18  # $RUNTIME/rocknix-qemu-*.sock, pidfile $RUNTIME/rocknix-qemu.pid, VNC :9, the
   19  # profile's MAC 52:54:00:52:4E:58); guest b gets the same with a -b suffix,
   20  # SSH 10023, VNC :10 and its own MAC, 52:54:00:52:4E:59. Both sit behind
   21  # user-mode NAT, so a shared MAC would collide on no network -- but
   22  # cloud_device_id hashes the permanent MAC, and two guests on the profile's
   23  # address printed one id between them (fork #91): one settings folder, one
   24  # manifest, and two-device fixtures agreeing with themselves. The id is
   25  # derived on first boot and then stored on the disk, so a pair started before
   26  # guest b had its own address keeps the shared id until `up` rebuilds the
   27  # disks; clearing the stored id alone re-derives the same one. Both reach
   28  # the host's QA backend at 10.0.2.2. Disks live under $VM_PAIR_DIR
   29  # (default /tmp/rocknix-vm-pair): scratch, rebuilt from the image on every up.
   30  # RUNTIME is VM_QEMU_RUNTIME_DIR (default /tmp). Keep both VM_PAIR_DIR and
   31  # VM_QEMU_RUNTIME_DIR unchanged for up, info, SSH, serial, reimage and down;
   32  # commands do not discover or take ownership of guests under another root.
   33  set -euo pipefail
   34  HERE=$(cd "$(dirname "$0")" && pwd)
   35  ROOT=$(cd "$HERE/.." && pwd)
   36  VM_TOOL="$ROOT/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm"
   37  DIR="${VM_PAIR_DIR:-/tmp/rocknix-vm-pair}"
   38  KEY="$DIR/qa-key"
   39  # Keep short-lived socket/PID writes off a quota-limited /tmp when requested.
   40  # vm-qa uses the same root; the default remains compatible with standalone tools.
   41  RUNTIME="${VM_QEMU_RUNTIME_DIR:-/tmp}"
   42  [[ "$RUNTIME" = /* && ! "$RUNTIME" =~ [[:space:]] ]] || {
   43    echo 'vm-pair: VM_QEMU_RUNTIME_DIR needs an absolute path without whitespace' >&2; exit 2;
   44  }
   45  check_runtime() {
   46    local probe
   47    (umask 077; mkdir -p "$RUNTIME") || return 1
   48    probe=$(mktemp "$RUNTIME/.pixelelated-vm-write-XXXXXX") || return 1
   49    if ! printf 'pid-file-write-check\n' > "$probe"; then
   50      rm -f "$probe"; echo 'vm-pair: runtime directory cannot accept PID writes' >&2; return 1
   51    fi
   52    rm -f "$probe"
   53  }
   54  
   55  # VM_GL=none puts the guests on the software renderer; the launcher's default
   56  # is hardware GL through virgl on the host's first Mesa render node (#291), and
   57  # the harness takes its frames over the VNC display when the monitor has no surface.
   58  # Per-guest settings: letter -> monitor serial pidfile vnc sshport mac
   59  # (every `read` below names all six: the last variable takes the rest of the
   60  # line, so a field added here without a slot there lands in the one before it)
   61  settings() {
   62    case "$1" in
   63      a) echo "$RUNTIME/rocknix-qemu-monitor.sock $RUNTIME/rocknix-qemu-serial.sock $RUNTIME/rocknix-qemu.pid 9 10022 52:54:00:52:4E:58" ;;
   64      b) echo "$RUNTIME/rocknix-qemu-monitor-b.sock $RUNTIME/rocknix-qemu-serial-b.sock $RUNTIME/rocknix-qemu-b.pid 10 10023 52:54:00:52:4E:59" ;;
   65      *) echo "vm-pair: guest is a or b, not '$1'" >&2; exit 2 ;;
   66    esac
   67  }
   68  
   69  # One guest booted from its disk, with its own settings.
   70  start_one() {
   71    local mon ser pid vnc port mac
   72    read -r mon ser pid vnc port mac <<<"$(settings "$1")"
   73    local rc=0 started
   74    "$VM_TOOL" run --headless --daemonize ${VM_GL:+--gl "$VM_GL"} --monitor "$mon" --serial "$ser" --pidfile "$pid" --vnc "$vnc" --ssh-port "$port" --mac "$mac" "$DIR/vm-$1.qcow2" 2>&1 | grep -v pw.conf || rc=${PIPESTATUS[0]}
   75    if [ "$rc" != 0 ]; then
   76      echo "vm-pair: guest $1 launch failed ($rc)" >&2; return "$rc"
   77    fi
   78    started=$(cat "$pid") || { echo "vm-pair: guest $1 has no PID file" >&2; return 1; }
   79    # A successful launcher alone does not prove a guest. Refuse stale/wrong
   80    # PID files before claiming up or waiting for an unrelated serial endpoint.
   81    python3 - "$started" "$DIR/vm-$1.qcow2" <<'VERIFY_PID' || return 1
   82  from pathlib import Path
   83  import os, sys
   84  try:
   85      pid = int(sys.argv[1])
   86      if pid <= 1:
   87          raise ValueError('invalid PID')
   88      args = (Path('/proc') / str(pid) / 'cmdline').read_bytes().split(b'\0')
   89      drive = os.fsencode('if=none,id=rocknix,format=qcow2,file=' + sys.argv[2])
   90      if not Path(os.fsdecode(args[0])).name.startswith('qemu-system-') or not any(
   91              args[i] == b'-drive' and args[i + 1] == drive for i in range(len(args) - 1)):
   92          raise ValueError('PID does not own the expected QEMU disk')
   93  except (OSError, ValueError) as error:
   94      sys.exit('vm-pair: ' + str(error))
   95  VERIFY_PID
   96    echo "up: $1 (pid $started, ssh :$port, serial $ser, mac $mac)"
   97  }
   98  
   99  # The QA key in by serial, then SSH answering with the guest's BUILD_ID; 1
  100  # when it did not answer within 300 s. Polled with the bound tools/vm-qa
  101  # gives it, not one attempt: sshd comes up after the serial console does,
  102  # and on a host that is also building an image the gap is tens of seconds --
  103  # a single try reported "guest a did not answer" for a guest that answered
  104  # ten seconds later, and took the whole pair down with it (#125).
  105  ready_one() {
  106    local ser port pub who t0
  107    read -r _ ser _ _ port _ <<<"$(settings "$1")"
  108    "$HERE/vm-serial" --socket "$ser" wait --up-to 300 >/dev/null || return 1
  109    pub=$(cat "$KEY.pub")
  110    "$HERE/vm-serial" --socket "$ser" sh "mkdir -p /storage/.ssh && chmod 700 /storage/.ssh && echo '$pub' >> /storage/.ssh/authorized_keys && chmod 600 /storage/.ssh/authorized_keys" >/dev/null || return 1
  111    who=""; t0=$(date +%s)
  112    for _ in $(seq 1 100); do
  113      who=$(ssh -i "$KEY" -p "$port" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes -o LogLevel=ERROR -o ConnectTimeout=8 root@127.0.0.1 'grep ^BUILD_ID= /etc/os-release | cut -c11-20' 2>/dev/null || true)
  114      if [ -n "$who" ]; then break; fi
  115      sleep 3
  116    done
  117    if [ -n "$who" ]; then
  118      echo "ready: $1 on $who over ssh :$port (answered after $(( $(date +%s) - t0 ))s)"
  119    else
  120      echo "vm-pair: guest $1 did not answer over ssh within 300s" >&2; return 1
  121    fi
  122  }
  123  
  124  stop_one() {
  125    local pid
  126    read -r _ _ pid _ _ _ <<<"$(settings "$1")"
  127    # TERM only requests shutdown. Wait for this owned process to release its
  128    # disk and VNC port before a caller can immediately restart it (#454).
  129    "$HERE/vm-stop" "$pid" "$DIR/vm-$1.qcow2"
  130  }
  131  
  132  case "${1:-}" in
  133    up)
  134      img="${2:-}"; [ -f "$img" ] || { echo "usage: vm-pair up <ROCKNIX-GENERIC_X64...img.gz>" >&2; exit 2; }
  135      check_runtime
  136      stop_one a; stop_one b
  137      mkdir -p "$DIR"; rm -f "$DIR"/vm-*.qcow2 "$DIR"/vm-*.ovmf-vars.fd
  138      [ -f "$KEY" ] || ssh-keygen -q -t ed25519 -N '' -f "$KEY" -C vm-pair
  139      # one raw image, two disks
  140      gunzip -c "$img" > "$DIR/image.img"
  141      for g in a b; do
  142        qemu-img convert -f raw -O qcow2 "$DIR/image.img" "$DIR/vm-$g.qcow2"
  143        qemu-img resize "$DIR/vm-$g.qcow2" 16G >/dev/null
  144      done
  145      rm -f "$DIR/image.img"
  146      for g in a b; do start_one "$g"; done
  147      for g in a b; do ready_one "$g" || exit 1; done
  148      ;;
  149    reimage)
  150      # One guest rebuilt from another image while the other runs on: the
  151      # mixed-installation test's previous build beside a new one
  152      # (tools/cloud-pair-migration). Its own disk, settings, key and wait.
  153      g="${2:-}"; img="${3:-}"
  154      settings "$g" >/dev/null || exit 2
  155      [ -f "$img" ] || { echo "usage: vm-pair reimage <a|b> <ROCKNIX-GENERIC_X64...img.gz>" >&2; exit 2; }
  156      check_runtime
  157      stop_one "$g"
  158      mkdir -p "$DIR"; rm -f "$DIR/vm-$g.qcow2" "$DIR/vm-$g.ovmf-vars.fd"
  159      [ -f "$KEY" ] || ssh-keygen -q -t ed25519 -N '' -f "$KEY" -C vm-pair
  160      gunzip -c "$img" > "$DIR/image-$g.img" || exit 1
  161      qemu-img convert -f raw -O qcow2 "$DIR/image-$g.img" "$DIR/vm-$g.qcow2" || exit 1
  162      qemu-img resize "$DIR/vm-$g.qcow2" 16G >/dev/null || exit 1
  163      rm -f "$DIR/image-$g.img"
  164      start_one "$g"
  165      ready_one "$g" || exit 1
  166      ;;
  167    down) stop_one a; stop_one b ;;
  168    ssh)
  169      read -r _ _ _ _ port _ <<<"$(settings "${2:-}")"; shift 2
  170      exec ssh -i "$KEY" -p "$port" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes -o LogLevel=ERROR root@127.0.0.1 "$@" ;;
  171    scp)
  172      # vm-pair scp <a|b> <local file> <remote path>: the pair's key and the
  173      # guest's port, so a caller never carries them (vm-upgrade-rehearsal did,
  174      # audit #258 PL-030).
  175      read -r _ _ _ _ port _ <<<"$(settings "${2:-}")"; shift 2
  176      exec scp -q -i "$KEY" -P "$port" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes -o LogLevel=ERROR "$1" "root@127.0.0.1:$2" ;;
  177    port)
  178      read -r _ _ _ _ port _ <<<"$(settings "${2:-}")"; echo "$port" ;;
  179    serial)
  180      read -r _ ser _ _ _ _ <<<"$(settings "${2:-}")"; shift 2
  181      exec "$HERE/vm-serial" --socket "$ser" sh "$@" ;;
  182    info)
  183      for g in a b; do read -r mon ser pid vnc port mac <<<"$(settings "$g")"; printf '%s: ssh -i %s -p %s root@127.0.0.1   monitor %s   serial %s   pid %s   vnc :%s   mac %s\n' "$g" "$KEY" "$port" "$mon" "$ser" "$([ -f "$pid" ] && cat "$pid" || echo -)" "$vnc" "$mac"; done ;;
  184    *) sed -n '2,29p' "$0" | sed 's/^# \{0,1\}//'; exit 2 ;;
  185  esac
  186  
```

## file, whole, at 8ebaf8daad: tools/vm-pair-test

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated (https://github.com/pixelelated)
    4  """Exercise the actual vm-pair launch functions with controlled failures (#545)."""
    5  import argparse
    6  import os
    7  from pathlib import Path
    8  import subprocess
    9  import sys
   10  import tempfile
   11  
   12  parser = argparse.ArgumentParser(description=__doc__)
   13  parser.add_argument('--source', type=Path, default=Path(__file__).with_name('vm-pair'))
   14  args = parser.parse_args()
   15  source = args.source.resolve()
   16  prefix = source.read_text().split('case "${1:-}" in', 1)[0]
   17  assert 'start_one()' in prefix and 'ready_one()' in prefix
   18  with tempfile.TemporaryDirectory(prefix='vm-pair-test-') as scratch:
   19      root = Path(scratch)
   20      runtime = root / 'runtime'
   21      runtime.mkdir()
   22      disk = root / 'vm-a.qcow2'
   23      pidfile = runtime / 'rocknix-qemu.pid'
   24      launcher = root / 'launcher'
   25      launcher.write_text('#!/bin/sh\nexit "${LAUNCH_RC:-0}"\n')
   26      launcher.chmod(0o700)
   27      serial = root / 'vm-serial'
   28      serial.write_text('#!/bin/sh\nexit 23\n')
   29      serial.chmod(0o700)
   30      env = dict(os.environ, VM_PAIR_DIR=str(root), VM_QEMU_RUNTIME_DIR=str(runtime))
   31  
   32      def run(action='start_one a', **extra):
   33          return subprocess.run(['bash', '-c', prefix + '\nVM_TOOL="$1"\n' + action,
   34                                 str(source), str(launcher)], env=dict(env, **extra),
   35                                text=True, capture_output=True, timeout=3)
   36  
   37      result = run(LAUNCH_RC='17')
   38      assert result.returncode == 17 and 'up: a' not in result.stdout, result
   39      print('PASS launcher failure preserves exit17 with no false up message')
   40      result = run()
   41      assert result.returncode != 0 and 'up: a' not in result.stdout, result
   42      print('PASS zero-exit launcher without PID file is refused')
   43      for label, pid in [('wrong-process', os.getpid()), ('dead-process', 2147483646)]:
   44          pidfile.write_text(str(pid))
   45          result = run()
   46          assert result.returncode != 0 and 'up: a' not in result.stdout, result
   47          print('PASS ' + label + ' PID is refused')
   48      for label, owned in [('wrong-disk', False), ('owned-disk', True)]:
   49          child = subprocess.Popen(['qemu-system-fixture', '-c', 'import time; time.sleep(30)',
   50                                    '-drive', 'if=none,id=rocknix,format=qcow2,file=' +
   51                                    str(disk if owned else root / 'other.qcow2')],
   52                                   executable=sys.executable)
   53          try:
   54              pidfile.write_text(str(child.pid))
   55              result = run()
   56              assert (result.returncode == 0) == owned, result
   57              assert ('up: a' in result.stdout) == owned, result
   58              print('PASS ' + label + (' live PID is verified, silent launcher allowed' if owned else ' PID is refused'))
   59          finally:
   60              child.terminate()
   61              child.wait(timeout=3)
   62      # ready_one is intentionally used in a conditional by the caller. A
   63      # serial failure must return before SSH even with bash errexit suppressed.
   64      result = run('HERE="$DIR"; if ready_one a; then exit 42; else exit $?; fi')
   65      assert result.returncode == 1, result
   66      print('PASS failed serial readiness returns immediately from conditional call')
   67      bad = root / 'not-a-directory'
   68      bad.write_text('fixture')
   69      result = run('check_runtime', VM_QEMU_RUNTIME_DIR=str(bad))
   70      assert result.returncode != 0, result
   71      print('PASS unusable runtime root refuses preflight')
   72      result = run('check_runtime')
   73      assert result.returncode == 0 and not list(runtime.glob('.pixelelated-vm-write-*')), result
   74      print('PASS writable runtime root preflight leaves no probe')
   75  print('PASS 9 VM launch controls; fixtures are not a real boot claim')
   76  
```

## file, whole, at 8ebaf8daad: tools/vm-qa

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # vm-qa - every automated check the fork has, against one GENERIC_X64 image, one report.
    6  #
    7  #   ./tools/vm-qa <ROCKNIX-GENERIC_X64...img.gz>            # bring the pair up from the image, run everything
    8  #   ./tools/vm-qa --skip-up                                  # the pair is already up on the image under test
    9  #   ./tools/vm-qa <image> --only round-trip,exit             # a subset: scripts, round-trip, exit, walks, link
   10  #
   11  # Each run writes to qa-<build>-<backend>-<guest>-<date>, so a matrix of
   12  # backends against one image keeps a report each.
   13  #   ./tools/vm-qa <image> --link                             # also the seven link-loss cells (minutes each; need the serial console)
   14  #   ./tools/vm-qa --skip-up --only walks --guest b           # the walks on vm-pair's second guest
   15  #   ./tools/vm-qa --skip-up --only round-trip --backend sftp # the round trip against another cloud (#133)
   16  #   ./tools/vm-qa --skip-up --only ra-offline --guest d      # the offline-achievements scenario on the 640x480 guest (#166)
   17  #   ./tools/vm-qa --list                                     # the suite names --only takes, one per line
   18  #   ./tools/vm-qa --skip-up --only walks --walk manager-gb   # repeat --walk for a scoped follow-up
   19  #
   20  # What runs, in order, each with its own log and a PASS/FAIL line:
   21  #
   22  #   scripts     tools/last-good-scripts-test  -- the scripts under busybox shims, on the host
   23  #   lifetime    ES page lifetimes and GPU save callback safety, on the host (ES_SRC)
   24  #   wrapper     tools/retroarch-wrapper-test -- RetroArch's threaded video wrapper runs a posted command exactly once
   25  #               (#211, #225; patch 0015), against the source in the build root, on the host
   26  #   vocabulary  tools/vocabulary-check       -- back up / backup as verb / noun, ES strings and script lines, on the host
   27  #   register    tools/register-check         -- the decision register: every ID once, every citation names a row, on the host (ES_SRC)
   28  #   french      tools/es-untranslated        -- every fork string in the interface has French (D-UI-051, #152), on the host (ES_SRC)
   29  #   quoting     tests/credential-quoting.py  -- every command built from a typed credential reaches the shell quoted (#198), on the host (ES_SRC)
   30  #   menumap     tools/es-menu-map-check      -- docs/es-menu-map.md still describes the menus the image ships (D-UI-039), on the host (ES_SRC)
   31  #   pair-identity  the two guests' MACs, cloud_device_ids (#91) and hostnames (#50) differ, and each
   32  #               answers for its own name over mDNS (#50 box 6, #151 PL-01), over ssh
   33  #   fresh       a first boot of the image ended where an update ends: the three es_*.cfg the OS
   34  #               manages and the controller database are links into /usr/config, not copies
   35  #               (userconfig-setup vs post-update; audit #258 PL-001), over ssh to guest a
   36  #   round-trip  tools/cloud-round-trip        -- 27 steps over SSH against the QA cloud, guest a
   37  #   exit        tools/emulator-exit-test --vm -- the exit hotkey ends a game once, save written, guest a
   38  #   time-to-play tools/time-to-play --quick   -- UI to a game's first frame, and one game's exit to the
   39  #               next game's first frame, with the exit sync running (#135, D-CLOUD-098). Its own table
   40  #               goes at the end of the report; the suite row here says only whether it ran.
   41  #   link        tools/cloud-round-trip --only LINK1..LINK7 -- the link cut mid-run, seven ways (--link, or --only link)
   42  #   ra-offline  tools/ra-offline-test         -- an achievement unlocked with the link cut is queued by the offline
   43  #               proxy and sent when the link returns (#166); needs the serial console and the QA
   44  #               RetroAchievements account, and spends one of its cheap achievements per PASS, so it is
   45  #               opt-in like link (--ra-offline, or --only ra-offline); --control runs #162's loss instead
   46  #   walks       tools/vm-walks/*.steps        -- each step file replayed from a rebooted guest, frames kept
   47  #   frame-diff  tools/frame-diff              -- the walk frames against the last accepted cut's; a box no
   48  #                                               claim in tools/vm-walks/claims.txt covers is a FAIL (#252)
   49  #               (frames are kept for a person to read; comparing them to references is fork #120's third box)
   50  #
   51  # The report goes to $ROCKNIX_ARTIFACTS/rocknix-images/qa-<build>-<date>/report.md
   52  # (default /workspace/artifacts), beside the logs and frames, and this exits
   53  # non-zero if any suite failed -- so a nightly can tell. Nothing here touches a
   54  # handheld: the guests are tools/vm-pair's, on this host (fork #120, box 1).
   55  set -u
   56  ROOT=$(cd "$(dirname "$0")/.." && pwd)
   57  IMAGE=""; SKIP_UP=0; LINK=0; RA_OFFLINE=0; GUEST=a; WALKS=""
   58  # The default run is every suite in SUITES except the two that are opt-in
   59  # (link needs a second backend, ra-offline spends a QA achievement). It used
   60  # to be a second, hand-typed list here -- and menumap, added to SUITES on
   61  # 2026-09-19, never ran because this copy was not updated. One list.
   62  ONLY=""
   63  SUITES="scripts lifetime wrapper vocabulary register french quoting menumap pair-identity fresh round-trip exit time-to-play link ra-offline walks frame-diff"
   64  [ -n "$ONLY" ] || ONLY=$(printf '%s' "$SUITES" | tr ' ' '\n' | grep -vxE 'link|ra-offline' | paste -sd, -)
   65  # Which of the five QA clouds every suite here talks to (#133). It is one
   66  # variable and not a per-suite flag on purpose: the backend the endpoint is
   67  # brought up on, the stanza the walks seed, and the endpoint the round trip
   68  # reads back have to be the same one, and CLOUD_QA_BACKEND is what every
   69  # tool below reads.
   70  BACKEND="${CLOUD_QA_BACKEND:-webdav}"
   71  while [ $# -gt 0 ]; do
   72    case "$1" in
   73      --skip-up) SKIP_UP=1; shift ;;
   74      --only) ONLY=$2; shift 2 ;;
   75      --walk) WALKS="${WALKS:+$WALKS,}${2:?walk name required}"; shift 2 ;;
   76      --guest) GUEST=$2; shift 2 ;;
   77      --backend) BACKEND=$2; shift 2 ;;
   78      --link) LINK=1; shift ;;
   79      --ra-offline) RA_OFFLINE=1; shift ;;
   80      --list) printf '%s\n' $SUITES; exit 0 ;;
   81      -h|--help) sed -n '5,38p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
   82      *) IMAGE=$1; shift ;;
   83    esac
   84  done
   85  if [ -n "$WALKS" ]; then
   86    case ",$ONLY," in *,walks,*) ;; *) echo 'vm-qa: --walk requires the walks suite' >&2; exit 2 ;; esac
   87    for selected_walk in ${WALKS//,/ }; do
   88      [[ "$selected_walk" =~ ^[a-z0-9-]+$ && "$selected_walk" != default-pre ]] && grep -qE "^$selected_walk[[:space:]]*=" "$ROOT/tools/vm-walks/suite.txt" \
   89        || { echo "vm-qa: unknown walk $selected_walk" >&2; exit 2; }
   90    done
   91  fi
   92  [ "$SKIP_UP" = 1 ] || [ -n "$IMAGE" ] || { echo "vm-qa: an image, or --skip-up" >&2; exit 2; }
   93  # Which of tools/vm-pair's guests the suites drive. Guest a is the default
   94  # and the only one `up` is written around; --guest b exists because two
   95  # sessions share this host and the walks suite is the one that can run
   96  # anywhere -- it needs a monitor socket and a guest to reboot, nothing else.
   97  # Use the same run-owned key that vm-pair injects into the guests.
   98  KEY="${VM_PAIR_DIR:-/tmp/rocknix-vm-pair}/qa-key"
   99  RUNTIME="${VM_QEMU_RUNTIME_DIR:-/tmp}"
  100  # The ssh options every suite here runs with. Declared, not inherited: the
  101  # pair-identity suite used $SSHO without this line and passed for a night
  102  # because the shell that started the runner had it set; started under a
  103  # clean environment it failed on "unbound variable" (blindspot 40).
  104  SSHO="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=8 -o BatchMode=yes"
  105  case "$GUEST" in
  106    a) PORT=10022; MON="$RUNTIME"/rocknix-qemu-monitor.sock;   SERIAL="$RUNTIME"/rocknix-qemu-serial.sock ;;
  107    b) PORT=10023; MON="$RUNTIME"/rocknix-qemu-monitor-b.sock; SERIAL="$RUNTIME"/rocknix-qemu-serial-b.sock ;;
  108    # The 640x480 guest beside the pair (generic-x64-vm-testing.md § Frame at
  109    # the handheld's size): not vm-pair's, so `up` never touches it -- --skip-up.
  110    d) PORT=10026; MON="$RUNTIME"/rocknix-qemu-monitor-d.sock; SERIAL="$RUNTIME"/rocknix-qemu-serial-d.sock ;;
  111    *) echo "vm-qa: --guest is a, b or d, not '$GUEST'" >&2; exit 2 ;;
  112  esac
  113  [ "$LINK" = 1 ] && ONLY="$ONLY,link"
  114  [ "$RA_OFFLINE" = 1 ] && ONLY="$ONLY,ra-offline"
  115  SSH() { ssh -n -i "$KEY" -p "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=8 -o BatchMode=yes root@127.0.0.1 "$@"; }
  116  
  117  export CLOUD_QA_BACKEND="$BACKEND"
  118  "$ROOT/tools/cloud-test-backend" up >/dev/null 2>&1 || { echo "vm-qa: the $BACKEND QA cloud backend did not come up" >&2; exit 1; }
  119  if [ "$SKIP_UP" = 0 ]; then
  120    "$ROOT/tools/vm-pair" down >/dev/null 2>&1
  121    "$ROOT/tools/vm-pair" up "$IMAGE" 2>&1 | tail -2
  122  fi
  123  for i in $(seq 1 40); do SSH true 2>/dev/null && break; sleep 3; done
  124  BUILD=$(SSH 'sed -n "s/^BUILD_ID=//p" /etc/os-release' 2>/dev/null | tr -d '"' | cut -c1-10)
  125  [ -n "$BUILD" ] || { echo "vm-qa: guest $GUEST does not answer" >&2; exit 1; }
  126  # The backend and the guest are in the directory name, not only the build and
  127  # the minute. Two vm-qa runs against one image -- which is what a backend
  128  # matrix is (#133) -- started in the same minute, shared a directory, and the
  129  # second overwrote the first's report and logs: two runs, one answer, and the
  130  # surviving report named the other run's cloud.
  131  OUT="${ROCKNIX_ARTIFACTS:-/workspace/artifacts}/rocknix-images/qa-${BUILD}-${BACKEND}-${GUEST}-$(date +%Y%m%d-%H%M)"
  132  mkdir -p "$OUT/walks"
  133  REPORT="$OUT/report.md"
  134  # The guest's display, read from its QEMU's own command line (#291): hardware GL through virgl on a host
  135  # render node, or the software path. The renderer the guest's Mesa then reports is read at the end, from
  136  # the launch log the exit suite leaves, so a guest that fell back to softpipe says so on its report.
  137  case "$GUEST" in a) PIDF="$RUNTIME"/rocknix-qemu.pid ;; b) PIDF="$RUNTIME"/rocknix-qemu-b.pid ;; *) PIDF="$RUNTIME"/rocknix-qemu-$GUEST.pid ;; esac
  138  DISPLAY_MODE=$(ps -o args= -p "$(cat "$PIDF" 2>/dev/null)" 2>/dev/null | grep -o -E 'egl-headless,rendernode=[^ ]+' | sed 's/^egl-headless,rendernode=/GL through virgl on /'); DISPLAY_MODE=${DISPLAY_MODE:-software rendering (no GL display)}
  139  { echo "# vm-qa on $BUILD"; echo; echo "started $(date -u '+%Y-%m-%d %H:%M UTC'), guest $GUEST at :$PORT, cloud $BACKEND (port $("$ROOT/tools/cloud-test-backend" port), $("$ROOT/tools/cloud-test-backend" caps)), image ${IMAGE:-(already up)}, display: $DISPLAY_MODE"; echo; echo "| suite | result | time | log |"; echo "| --- | --- | --- | --- |"; } > "$REPORT"
  140  FAILS=0
  141  SKIPS=0  # a suite that could not run (rc 3) is shown as such, never folded into PASS
  142  run_suite() {  # name, log, command...
  143    local name=$1 log=$2; shift 2
  144    local t0=$(date +%s) rc
  145    "$@" > "$log" 2>&1; rc=$?
  146    local dt=$(( $(date +%s) - t0 ))
  147    local res=PASS
  148    if [ "$rc" = 3 ]; then res="SKIP"; SKIPS=$((SKIPS+1)); elif [ "$rc" != 0 ]; then res="FAIL ($rc)"; FAILS=$((FAILS+1)); fi
  149    printf '| %s | %s | %ds | `%s` |\n' "$name" "$res" "$dt" "$(basename "$log")" >> "$REPORT"
  150    echo "$name: $res in ${dt}s"
  151  }
  152  # The scripts harness carries cancel checks that send SIGINT to a run; a
  153  # background job (this runner under setsid -f, or a harness waiter) has
  154  # SIGINT ignored at entry, which a child shell cannot undo. Python can --
  155  # and Python itself ignores SIGPIPE at startup, which execv keeps, so both
  156  # are reset (audit of the fix round PL-025); the harness prints what it got:
  157  # reset the disposition and exec the harness in its place (2026-09-28).
  158  case ",$ONLY," in *,scripts,*)    run_suite scripts    "$OUT/scripts.log"    python3 -c 'import os, signal, sys; signal.signal(signal.SIGINT, signal.SIG_DFL); signal.signal(signal.SIGPIPE, signal.SIG_DFL); os.execv(sys.argv[1], sys.argv[1:])' "$ROOT/tools/last-good-scripts-test" ;; esac
  159  # EmulationStation's page-lifetime check (#144): the wizard's page-replacement
  160  # callbacks compiled under AddressSanitizer against small doubles, on the
  161  # host, in seconds. It had not compiled for a day and nothing ran it, so
  162  # nothing said so (audit 2026-09-12, F-01). ES_SRC names the checkout whose
  163  # GuiMenu.cpp is pinned by the image under test; a missing checkout is a
  164  # FAIL with the reason, never a silent skip -- a guard that cannot run has
  165  # not passed.
  166  lifetime_suite() {
  167    local es="${ES_SRC:-$HOME/Development/emulationstation-next.worktrees/qa-integration}"
  168    if [ ! -f "$es/tests/cloud-oauth-lifetime.py" ]; then
  169      echo "no EmulationStation checkout at $es (set ES_SRC); the lifetime check did not run"; return 1
  170    fi
  171    echo "GuiMenu.cpp from $es at $(git -C "$es" rev-parse --short HEAD 2>/dev/null || echo '?')"
  172    python3 "$es/tests/cloud-oauth-lifetime.py" || return
  173    # Closing System Settings must also survive absent hardware options (#436).
  174    python3 "$es/tests/gpu-governor-save.py"
  175  }
  176  case ",$ONLY," in *,lifetime,*)   run_suite lifetime   "$OUT/lifetime.log"   lifetime_suite ;; esac
  177  # The player-facing words held to their rules (es-player-text.md, player-language.md):
  178  # "back up" two words as a verb, "backup" one as a noun, across every _("")
  179  # string in the ES checkout the image pins and every sentence the scripts
  180  # print for a player. On the host, in a second (2026-09-12, the maintainer's ask).
  181  # RetroArch's threaded video wrapper, extracted from the source the image was
  182  # built from and driven 2000 times (#211's crash, #225's gate): it had a test
  183  # and no suite ran it (audit #258 PL-020), which is the shape blindspot 14
  184  # names. Seconds, on the host; 2 when no source is found, which is not a pass.
  185  case ",$ONLY," in *,wrapper,*) run_suite wrapper "$OUT/wrapper.log" "$ROOT/tools/retroarch-wrapper-test" ;; esac
  186  case ",$ONLY," in *,vocabulary,*) run_suite vocabulary "$OUT/vocabulary.log" env ES_SRC="${ES_SRC:-$HOME/Development/emulationstation-next.worktrees/qa-integration}" "$ROOT/tools/vocabulary-check" ;; esac
  187  # Every string the fork adds has French (D-UI-051): tools/es-untranslated lists the ones that do not and exits 1 while any remain (#152).
  188  case ",$ONLY," in *,french,*) run_suite french "$OUT/french.log" env ES_SRC="${ES_SRC:-$HOME/Development/emulationstation-next.worktrees/qa-integration}" "$ROOT/tools/es-untranslated" ;; esac
  189  # Every command built from a credential a player types reaches the shell quoted (fork #198):
  190  # the check reads the ES source the french suite reads.
  191  case ",$ONLY," in *,quoting,*) run_suite quoting "$OUT/quoting.log" python3 "${ES_SRC:-$HOME/Development/emulationstation-next.worktrees/qa-integration}/tests/credential-quoting.py" "${ES_SRC:-$HOME/Development/emulationstation-next.worktrees/qa-integration}" ;; esac
  192  # The menu map still describes what ships (D-UI-039): tools/es-menu-map-check reads the
  193  # screens in the ES commit the package pins and fails on one the map neither maps nor
  194  # declares under "## Not mapped". The rule predates the check by a month, and 30 screens
  195  # had drifted out by the time anybody counted (2026-09-18).
  196  case ",$ONLY," in *,menumap,*) run_suite menumap "$OUT/menumap.log" env ES_SRC="${ES_SRC:-$HOME/Development/emulationstation-next.worktrees/qa-integration}" "$ROOT/tools/es-menu-map-check" ;; esac
  197  # The decision register as a lookup table (D-WORKFLOW-013): every ID once,
  198  # and every `D-<AREA>-<n>` cited in a live document -- the rules, the
  199  # scripts, the tools, and EmulationStation's sources when the checkout the
  200  # image pins is on this host -- names a row. It had fired for real
  201  # (D-CLOUD-007, and a dangling citation the same week) and nothing ran it
  202  # but a hand (audit #151 PL-11). On the host, in a second, beside vocabulary.
  203  # Without the ES checkout the register is still checked; the log says what
  204  # was not.
  205  register_suite() {
  206    local es="${ES_SRC:-$HOME/Development/emulationstation-next.worktrees/qa-integration}"
  207    if [ -d "$es" ]; then
  208      echo "EmulationStation sources from $es at $(git -C "$es" rev-parse --short HEAD 2>/dev/null || echo '?')"
  209      env ES_SRC="$es" "$ROOT/tools/register-check"
  210    else
  211      echo "no EmulationStation checkout at $es (set ES_SRC): the register is checked without the interface's citations"
  212      env -u ES_SRC "$ROOT/tools/register-check"
  213    fi
  214  }
  215  case ",$ONLY," in *,register,*)   run_suite register   "$OUT/register.log"   register_suite ;; esac
  216  # The two guests are two devices (#91): different MACs, different
  217  # cloud_device_ids. The round trip's own guard for this (assert_two_devices)
  218  # runs only under --second-port, which also runs the two-device fixtures that
  219  # stay red until #22 -- so the default suite never fired it, and the pair
  220  # sharing an identity would have gone unnoticed (hygiene pass, 2026-09-12).
  221  # Seconds, over ssh, before anything else touches the pair.
  222  pair_identity_suite() {
  223    # Every check runs and every failure is printed before the suite fails, so
  224    # one shared name does not hide a wrong mDNS name behind it (#151 PL-01).
  225    local bad=0 ka kb ia ib
  226    ka=$(ssh -n -i "$KEY" -p 10022 $SSHO root@127.0.0.1 'cat /sys/class/net/eth0/address' 2>/dev/null)
  227    kb=$(ssh -n -i "$KEY" -p 10023 $SSHO root@127.0.0.1 'cat /sys/class/net/eth0/address' 2>/dev/null)
  228    ia=$(ssh -n -i "$KEY" -p 10022 $SSHO root@127.0.0.1 '. /etc/profile; cloud_device_id 2>/dev/null | head -1' 2>/dev/null)
  229    ib=$(ssh -n -i "$KEY" -p 10023 $SSHO root@127.0.0.1 '. /etc/profile; cloud_device_id 2>/dev/null | head -1' 2>/dev/null)
  230    echo "guest a: mac=${ka:-?} id=${ia:-?}"; echo "guest b: mac=${kb:-?} id=${ib:-?}"
  231    [ -n "$ka" ] && [ -n "$kb" ] && [ -n "$ia" ] && [ -n "$ib" ] || { echo "a guest did not answer; the pair's identity is unproven"; return 1; }
  232    [ "$ka" != "$kb" ] || { echo "FAIL: the guests share a MAC"; bad=1; }
  233    [ "$ia" != "$ib" ] || { echo "FAIL: the guests share a cloud_device_id"; bad=1; }
  234    # And two names (#50, D-NET-002): the shipped family name becomes the
  235    # unit's own at boot, so the kernel names differ and each equals the
  236    # cleaned form of its own stored setting. An image from before #50 fails
  237    # here with both guests named GENERIC-X64, which is the collision itself.
  238    local ha hb sa sb
  239    ha=$(ssh -n -i "$KEY" -p 10022 $SSHO root@127.0.0.1 'hostname' 2>/dev/null)
  240    hb=$(ssh -n -i "$KEY" -p 10023 $SSHO root@127.0.0.1 'hostname' 2>/dev/null)
  241    sa=$(ssh -n -i "$KEY" -p 10022 $SSHO root@127.0.0.1 '. /etc/profile; clean_hostname "$(get_setting system.hostname)"' 2>/dev/null)
  242    sb=$(ssh -n -i "$KEY" -p 10023 $SSHO root@127.0.0.1 '. /etc/profile; clean_hostname "$(get_setting system.hostname)"' 2>/dev/null)
  243    echo "guest a: hostname=${ha:-?} setting=${sa:-?}"; echo "guest b: hostname=${hb:-?} setting=${sb:-?}"
  244    [ -n "$ha" ] && [ -n "$hb" ] || { echo "a guest did not answer its hostname"; return 1; }
  245    [ "$ha" != "$hb" ] || { echo "FAIL: the guests share a hostname (${ha}): the shipped family name was not made the unit's own"; bad=1; }
  246    [ "$ha" = "$sa" ] && [ "$hb" = "$sb" ] || { echo "FAIL: a kernel hostname differs from its stored setting"; bad=1; }
  247    # And each answers for its own name over mDNS (#50 box 6, D-NET-003; audit
  248    # #151 PL-01): avahi logs `Host name is <x>.local` when it publishes, and
  249    # <x> has to be the kernel name network-base-setup wrote. The daemon reads
  250    # the kernel name when it comes up, so a unit that starts before the write
  251    # publishes the image's name for the whole boot -- on 519f40aa0c guest b
  252    # answered for ROCKNIX.local while named GENERIC-X64-0964, and nothing
  253    # corrected it. The last `Host name is` line is the one in force; none at
  254    # all is a FAIL too -- a responder that has not published, or a journal
  255    # this could not read, is not a responder proven to answer.
  256    local ma mb
  257    ma=$(ssh -n -i "$KEY" -p 10022 $SSHO root@127.0.0.1 'journalctl -b -u avahi-daemon -o cat 2>/dev/null | sed -n "s/.*Host name is \([^ .]*\)\.local.*/\1/p" | tail -1' 2>/dev/null)
  258    mb=$(ssh -n -i "$KEY" -p 10023 $SSHO root@127.0.0.1 'journalctl -b -u avahi-daemon -o cat 2>/dev/null | sed -n "s/.*Host name is \([^ .]*\)\.local.*/\1/p" | tail -1' 2>/dev/null)
  259    local pa=${ma:+$ma.local} pb=${mb:+$mb.local}
  260    echo "guest a: mdns=${pa:-?}"; echo "guest b: mdns=${pb:-?}"
  261    if [ -z "$ma" ] || [ -z "$mb" ]; then
  262      echo "FAIL: a guest's avahi journal has no 'Host name is' line: the responder has not published, or the journal could not be read"; bad=1
  263    else
  264      [ "$ma" = "$ha" ] || { echo "FAIL: guest a answers over mDNS for ${ma}.local while named ${ha}: the responder published before network-base-setup wrote the name"; bad=1; }
  265      [ "$mb" = "$hb" ] || { echo "FAIL: guest b answers over mDNS for ${mb}.local while named ${hb}: the responder published before network-base-setup wrote the name"; bad=1; }
  266    fi
  267    [ "$bad" = 0 ] || return 1
  268    echo "two devices, two names, each answering for its own over mDNS"
  269  }
  270  case ",$ONLY," in *,pair-identity,*) run_suite pair-identity "$OUT/pair-identity.log" pair_identity_suite ;; esac
  271  # A fresh boot lands where an update lands (upgrade-and-install.md, "The two
  272  # questions"). userconfig-setup copies /usr/config on first boot and then
  273  # links the files the OS manages; a file it did not exclude from the copy
  274  # stands where the link goes and the ln -s fails without a word, so a fresh
  275  # device carries a copy while an updated one carries a link. es_savestates.cfg
  276  # shipped that way for two weeks (audit #258 PL-001). Guest a is booted from
  277  # the image by this runner, so it is exactly the fresh device in question.
  278  fresh_suite() {
  279    local bad=0 f target
  280    for f in es_features.cfg es_systems.cfg es_savestates.cfg; do
  281      target=$(ssh -n -i "$KEY" -p 10022 $SSHO root@127.0.0.1 "readlink /storage/.config/emulationstation/$f" 2>/dev/null)
  282      echo "guest a: emulationstation/$f -> ${target:-(not a link)}"
  283      [ "$target" = "/usr/config/emulationstation/$f" ] || { echo "FAIL: /storage/.config/emulationstation/$f is not a link to /usr/config/emulationstation/$f on a fresh boot -- userconfig-setup copied it and the link was not made"; bad=1; }
  284    done
  285    target=$(ssh -n -i "$KEY" -p 10022 $SSHO root@127.0.0.1 'readlink /storage/.config/SDL-GameControllerDB/gamecontrollerdb.txt' 2>/dev/null)
  286    echo "guest a: SDL-GameControllerDB/gamecontrollerdb.txt -> ${target:-(not a link)}"
  287    [ "$target" = "/usr/config/SDL-GameControllerDB/gamecontrollerdb.txt" ] || { echo "FAIL: the controller database is not a link on a fresh boot"; bad=1; }
  288    local conf
  289    conf=$(ssh -n -i "$KEY" -p 10022 $SSHO root@127.0.0.1 '[ -e /storage/.configured ] && echo yes || echo no' 2>/dev/null)
  290    echo "guest a: /storage/.configured ${conf:-?}"
  291    [ "$conf" = yes ] || { echo "FAIL: /storage/.configured is absent: first-boot configuration did not finish, or the guest did not answer"; bad=1; }
  292    [ "$bad" = 0 ] || return 1
  293  }
  294  case ",$ONLY," in *,fresh,*) run_suite fresh "$OUT/fresh.log" fresh_suite ;; esac
  295  case ",$ONLY," in *,round-trip,*) run_suite round-trip "$OUT/round-trip.log" "$ROOT/tools/cloud-round-trip" --host root@127.0.0.1 --port "$PORT" --identity "$KEY" --backend "$BACKEND" ;; esac
  296  case ",$ONLY," in *,exit,*)       run_suite exit       "$OUT/exit.log"       "$ROOT/tools/emulator-exit-test" --port "$PORT" --identity "$KEY" --vm ;; esac
  297  # The walks open pages that refuse without a remote (NO CLOUD STORAGE IS SET
  298  # UP ON THIS DEVICE YET. SET IT UP NOW?), and the round-trip suite, which runs
  299  # first, puts the guest's rclone.conf back to how it found it -- on a fresh
  300  # pair, absent. Seven walks failed at that dialog on af2db4ab09 (2026-09-11)
  301  # while the same suite had read PASS on the image before, whose fixed-wait
  302  # walks passed whenever the tool ran (#125). Seed the QA remote when there is
  303  # none, the way seed-device does, and the folders the transfer page expects.
  304  ACTIVE_READER='if test -f "$(dirname "$(command -v cloud_remote)")/cloud_connections.py"; then cloud_remote active; else rclone listremotes 2>/dev/null | head -1; fi'
  305  ensure_remote() {
  306    [ -n "$(SSH "$ACTIVE_READER" 2>/dev/null)" ] && return 0
  307    # A saved account or an explicit no-selection is not a fresh guest.
  308    if SSH 'test -s /storage/.config/rclone/rclone.conf || test -e /storage/.config/rclone/active-connection' 2>/dev/null; then
  309      echo "vm-qa: choose the QA connection explicitly; saved connection state is present" >&2
  310      return 1
  311    fi
  312    local conf; conf=$(mktemp)
  313    "$ROOT/tools/cloud-test-backend" rclone-conf > "$conf"
  314    SSH 'mkdir -p /storage/.config/rclone' 2>/dev/null
  315    scp -q -i "$KEY" -P "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR "$conf" root@127.0.0.1:/storage/.config/rclone/rclone.conf
  316    rm -f "$conf"
  317    SSH "chmod 600 /storage/.config/rclone/rclone.conf; /usr/bin/cloud_sync_helper >/dev/null 2>&1; $(shipped_folders_cmd); echo \"vm-qa: seeded the QA remote \${r} (the guest had none)\"" 2>/dev/null
  318  }
  319  # The guest-side command that makes the shipped saves and backups folders in
  320  # the remote: their names from cloud_sync.conf.defaults, through the backend
  321  # tool, never a literal here (blindspot 71). Fails closed: a missing default
  322  # is a loud exit, not an empty folder name.
  323  shipped_folders_cmd() {
  324    local saves backups
  325    saves=$("$ROOT/tools/cloud-test-backend" shipped-default SAVES_REMOTE) || exit 2
  326    backups=$("$ROOT/tools/cloud-test-backend" shipped-default SETTINGS_REMOTE) || exit 2
  327    printf 'r=$(%s); [ -n "$r" ] || exit 1; rclone mkdir "${r}%s" >/dev/null 2>&1; rclone mkdir "${r}%s" >/dev/null 2>&1' "$ACTIVE_READER" "$saves" "$backups"
  328  }
  329  # Time to play (#135). --quick is the bounded form -- one repeat of the
  330  # launch, the exit sync and a game-to-game, no reboot and no host fixtures --
  331  # because this runs on every image and the offline and bounds cells are
  332  # minutes each. The full cell (--repeat 5, every condition) is run by hand
  333  # when a number is being proposed for a register row (D-CLOUD-116).
  334  case ",$ONLY," in *,time-to-play,*)
  335    # Its online cells time a sync that reaches the QA cloud. In the full run
  336    # an earlier suite has left a remote on guest a by now (run 29: reachable);
  337    # alone (--only time-to-play) on a fresh pair there is none, and the exit
  338    # sync ends at once with YOUR CLOUD STORAGE ISN'T SET UP YET (2026-09-25).
  339    # tools/time-to-play now fails such a run; this keeps the suite from
  340    # depending on its order.
  341    ensure_remote
  342    run_suite time-to-play "$OUT/time-to-play.log" "$ROOT/tools/time-to-play" \
  343      --host root@127.0.0.1 --port "$PORT" --identity "$KEY" --monitor "$MON" \
  344      --backend "$BACKEND" --out "$OUT/time-to-play" --quick --vm \
  345      --label "vm-qa on $(hostname -s), guest $GUEST" ;;
  346  esac
  347  # The link cells are timing-bound (a run must end within 90 s of the cut), so
  348  # they run before the walks and never while an image builds on this host.
  349  case ",$ONLY," in *,link,*)       run_suite link       "$OUT/link.log"       "$ROOT/tools/cloud-round-trip" --host root@127.0.0.1 --port "$PORT" --identity "$KEY" --backend "$BACKEND" --only LINK1,LINK2,LINK3,LINK4,LINK5,LINK6,LINK7 --serial-socket "$SERIAL" ;; esac
  350  # The offline-achievements scenario (#166): the QA account on, the toggle on,
  351  # a game with a RetroAchievements set launched online, the link cut on the
  352  # monitor, an achievement unlocked and queued, the game ended offline, the
  353  # link back, the award flushed and on the account. Serial console, monitor
  354  # and the QA account file are its preconditions and each is a FAIL when
  355  # missing; a PASS spends one cheap achievement on the QA account, which is
  356  # why it is opt-in. Timing-bound like link (the flush within 90 s), so never
  357  # while an image builds here.
  358  case ",$ONLY," in *,ra-offline,*) run_suite ra-offline "$OUT/ra-offline.log" "$ROOT/tools/ra-offline-test" --host root@127.0.0.1 --port "$PORT" --identity "$KEY" --monitor "$MON" --serial "$SERIAL" --frames "$OUT/ra-offline-frames" ;; esac
  359  # And the transfer walks tick ROMS AND BIOS and continue to the systems page,
  360  # which on a device with no ROMs is the dialog NO SYSTEM ON THIS DEVICE HOLDS
  361  # WHAT YOU TICKED (two walks, af2db4ab09). The round-trip suite works in a
  362  # scratch tree and leaves /storage/roms as it found it -- empty on a fresh
  363  # pair -- so seed the same fixture the walks were written against: the
  364  # backend's seed-content in the cloud and seed-device's ROMs on the guest.
  365  # The manager walks want a game per system with a capture to show (#252): a
  366  # NES game with a turn recorded beside its states (the record saying the turn
  367  # came from the game's own launch, or the fixed reader ignores it -- #288), a
  368  # Game Boy game as it is,
  369  # and an FBNeo game the core's own table turns. Stub ROMs, the fixture
  370  # pictures under tools/vm-walks/fixtures/ (a ring that is round only at the
  371  # right aspect, a green mark on the edge that is the game's top), and fixed
  372  # mtimes, so the tile dates read the same on every run and the frames compare.
  373  ensure_manager_fixture() {
  374    # match-dialog deliberately deletes the device-only GB ROMs. A surviving
  375    # FBNeo thumbnail says nothing about the later Game Boy fixture (#455).
  376    SSH 'test -f /storage/roms/savestates/fbn/mspacman.state.auto.png && test -f /storage/roms/nes/Bobl.nes && test -f /storage/roms/gb/Ninoid.gb && test -f /storage/roms/fbneo/mspacman.zip' 2>/dev/null && return 0
  377    local F="$ROOT/tools/vm-walks/fixtures" put
  378    put() { scp -q -i "$KEY" -P "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR "$1" "root@127.0.0.1:$2"; }
  379    SSH 'mkdir -p /storage/roms/nes /storage/roms/gb /storage/roms/fbneo /storage/roms/savestates/nes /storage/roms/savestates/gb /storage/roms/savestates/fbn /storage/roms/screenshots; for f in nes/Bobl.nes gb/Ninoid.gb fbneo/mspacman.zip; do head -c 4096 /dev/urandom > /storage/roms/$f; done; for s in nes/Bobl gb/Ninoid fbn/mspacman; do head -c 4096 /dev/urandom > /storage/roms/savestates/$s.state.auto; done; printf "turns=1\nfrom=checked-launch\n" > /storage/roms/savestates/nes/Bobl.rotation' 2>/dev/null
  380    put "$F/nes-256x240-right.png" /storage/roms/savestates/nes/Bobl.state.auto.png
  381    put "$F/gb-160x144.png" /storage/roms/savestates/gb/Ninoid.state.auto.png
  382    put "$F/arcade-vertical-raw-left.png" /storage/roms/savestates/fbn/mspacman.state.auto.png
  383    put "$F/nes-256x240-right.png" /storage/roms/screenshots/Bobl-260901-120000.png
  384    put "$F/gb-160x144.png" /storage/roms/screenshots/Ninoid-260901-120100.png
  385    put "$F/arcade-vertical-raw-left.png" /storage/roms/screenshots/mspacman-260901-120200.png
  386    SSH 'touch -d "2026-09-01 12:00:00" /storage/roms/savestates/*/* /storage/roms/screenshots/* /storage/roms/nes/* /storage/roms/gb/* /storage/roms/fbneo/*; sync; echo "walks: seeded the manager fixture (nes with a turn recorded, gb as is, fbn from the core table; mtimes 2026-09-01 12:00)"' 2>/dev/null
  387  }
  388  ensure_fixture() {
  389    ensure_remote
  390    SSH 'test -f /storage/roms/snes/shared.sfc' 2>/dev/null && return 0
  391    # The transfer walks upload the device-only ROMs, and the cloud keeps them:
  392    # a second run then frames a systems page and a phase line that count what
  393    # the first run left there (runs 17 and 18, 2026-09-23). The frame-diff
  394    # suite compares those frames, so the endpoint is put back to the seed
  395    # every time the guest is seeded, the way the round-trip suite does before
  396    # its own work.
  397    "$ROOT/tools/cloud-test-backend" reset >/dev/null 2>&1
  398    "$ROOT/tools/cloud-test-backend" seed-content >/dev/null 2>&1
  399    local scr; scr=$(mktemp)
  400    "$ROOT/tools/cloud-test-backend" seed-device > "$scr"
  401    scp -q -i "$KEY" -P "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR "$scr" root@127.0.0.1:/tmp/qa-seed-device.sh
  402    rm -f "$scr"
  403    SSH 'bash /tmp/qa-seed-device.sh >/dev/null 2>&1; rm -f /tmp/qa-seed-device.sh; echo "walks: seeded the content fixture (cloud seed-content, device ROMs) -- the guest had no ROMs"' 2>/dev/null
  404    # The shipped saves and backups folders beside the content, since the reset
  405    # took them: RESTORE FROM THE CLOUD's scan (D-CLOUD-167) reaches the options
  406    # page only when the cloud has the saves folder; without it the walk ends
  407    # on the offer to create one (D-CLOUD-161), which guest d's proofs cover.
  408    SSH "$(shipped_folders_cmd)" 2>/dev/null
  409  }
  410  # Folder navigation must not rewrite pointers/credentials or move payloads.
  411  # These guests and their endpoint are synthetic QA fixtures only. Keep each
  412  # command's result before sorting; a failed listing is not an empty witness.
  413  folder_walk_witness() {
  414    local dest=$1 rc=0
  415    mkdir -p "$dest"
  416    SSH 'sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf && stat -c "%a %n" /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf' > "$dest/config.txt" || rc=1
  417    SSH '/usr/bin/cloud_setup --validation-context' > "$dest/paths.json" || rc=1
  418    SSH "bash -o pipefail -c 'find /storage/roms -type f -print0 | xargs -0 -r sha256sum'" > "$dest/local.unsorted" || rc=1
  419    SSH "r=\$($ACTIVE_READER); [ -n \"\$r\" ] || exit 1; timeout 60 rclone hashsum SHA256 --download --retries 1 --contimeout 5s --timeout 10s \"\$r\"" > "$dest/cloud.unsorted" || rc=1
  420    LC_ALL=C sort "$dest/local.unsorted" > "$dest/local.txt" || rc=1
  421    LC_ALL=C sort "$dest/cloud.unsorted" > "$dest/cloud.txt" || rc=1
  422    printf '%s\n' "$rc" > "$dest/result"
  423    return "$rc"
  424  }
  425  
  426  case ",$ONLY," in *,walks,*)
  427    ensure_fixture
  428    ensure_manager_fixture
  429    # Every walk starts from a rebooted guest, which the README names as the
  430    # one deterministic start; a boot-time dialog is dismissed with B first.
  431    walk_all() {
  432      local rc=0 name legs w pre defpre=""
  433      # tools/vm-walks/suite.txt names the compositions: most walk files are a
  434      # leg that starts on a screen an earlier leg reaches, so replaying them
  435      # one at a time drove A presses into the carousel and counted the frames
  436      # as a pass (#125). The old behaviour is the fallback if the file is gone.
  437      local suite="$ROOT/tools/vm-walks/suite.txt"
  438      if [ ! -f "$suite" ]; then
  439        for w in "$ROOT"/tools/vm-walks/*.steps; do
  440          name=$(basename "$w" .steps)
  441          case "$name" in wake|reset) continue ;; esac
  442          printf '%s = %s\n' "$name" "$name"
  443        done > "$OUT/walks/suite.txt"
  444        suite="$OUT/walks/suite.txt"
  445      fi
  446      while IFS= read -r line; do
  447        line=${line%%#*}
  448        case "$line" in *=*) ;; *) continue ;; esac
  449        name=$(echo "${line%%=*}" | tr -d ' ')
  450        legs=${line#*=}
  451        # `<name> = <legs> | <shell>`: the part after | is a command run on the
  452        # guest BEFORE the reboot, for a walk whose starting screen depends on
  453        # state a reboot does not clear -- which the transfer page's switches
  454        # are: EmulationStation saves them into system.cfg when the page
  455        # closes and restores them at the next start, so a `tick-*` leg, which
  456        # FLIPS rather than sets, went the wrong way after any walk that had
  457        # left one on (#125).
  458        pre=""
  459        case "$legs" in *\|*) pre=${legs#*|}; legs=${legs%%|*} ;; esac
  460        # `default-pre = <shell>` is the reset every walk wants; a line's own
  461        # `| <shell>` runs after it, so a walk can override what it set.
  462        if [ "$name" = "default-pre" ]; then defpre=$legs; continue; fi
  463        [ -n "$name" ] || continue
  464        if [ -n "$WALKS" ]; then
  465          case ",$WALKS," in *,"$name",*) ;; *) continue ;; esac
  466        fi
  467        mkdir -p "$OUT/walks"
  468        [ -n "$defpre" ] && SSH "$defpre" >/dev/null 2>&1
  469        [ -n "$pre" ] && SSH "$pre" >/dev/null 2>&1
  470        case "$name" in manager-*)
  471          ensure_manager_fixture || { echo "walk $name: fixture failed"; rc=1; continue; }
  472          SSH 'mkdir -p /storage/.config/emulationstation/scripts/system-selected; rm -f /storage/.cache/vm-qa-selected-system' || { rc=1; continue; }
  473          scp -q -i "$KEY" -P "$PORT" $SSHO "$ROOT/tools/vm-walks/fixtures/system-selected.sh" "root@127.0.0.1:/storage/.config/emulationstation/scripts/system-selected/99-vm-qa.sh" || { rc=1; continue; }
  474          SSH 'chmod 700 /storage/.config/emulationstation/scripts/system-selected/99-vm-qa.sh' || { rc=1; continue; }
  475          ;; esac
  476        SSH 'systemctl reboot' 2>/dev/null; sleep 6
  477        for i in $(seq 1 45); do SSH 'pgrep -x emulationstation >/dev/null' 2>/dev/null && break; sleep 3; done; sleep 10
  478        case "$name" in manager-*)
  479          SSH 'curl -fsS -m 10 http://127.0.0.1:1234/systems' > "$OUT/walks/$name-systems.json"
  480          selected_system=$(SSH 'cat /storage/.cache/vm-qa-selected-system' 2>/dev/null)
  481          printf '%s\n' "$selected_system" > "$OUT/walks/$name-selected.txt"
  482          SSH 'rm -f /storage/.config/emulationstation/scripts/system-selected/99-vm-qa.sh'
  483          "$ROOT/tools/vm-manager-system-check" "${name#manager-}" "$selected_system" < "$OUT/walks/$name-systems.json" \
  484            > "$OUT/walks/$name-system-check.log" 2>&1 \
  485            || { echo "walk $name: requested system was not selected (see $name-system-check.log)"; rc=1; continue; }
  486          ;; esac
  487        case "$name" in to-change-cloud-folder|confirm-cloud-folder)
  488          folder_walk_witness "$OUT/walks/$name-before" || { echo "walk $name: initial preservation witness failed"; rc=1; continue; }
  489          ;; esac
  490        # wake, then dismiss-dialogs: the first key after a boot is eaten by the
  491        # screensaver, and a boot-time dialog (the journey prompt, the
  492        # RetroAchievements offer, FINISH RESTORE SETUP) has to go before any
  493        # walk. This was `key z` + `wait 2`, which is one B press: on a guest
  494        # with nothing open that press OPENS the carousel's GO TO dialog, and
  495        # the walk then ran a screen out of phase (#125).
  496        { printf 'wake\ndismiss-dialogs\n'
  497          for w in $legs; do printf '# --- %s ---\n' "$w"; cat "$ROOT/tools/vm-walks/$w.steps"; done
  498        } | timeout 900 "$ROOT/tools/vm-visual-qa" --monitor "$MON" run - --outdir "$OUT/walks/$name/" > "$OUT/walks/$name.log" 2>&1 \
  499          || { echo "walk $name: exit $?  (see walks/$name.log)"; rc=1; }
  500        case "$name" in to-change-cloud-folder|confirm-cloud-folder)
  501          if folder_walk_witness "$OUT/walks/$name-after"; then
  502            for witness in config.txt paths.json local.txt cloud.txt; do
  503              cmp "$OUT/walks/$name-before/$witness" "$OUT/walks/$name-after/$witness" || { echo "walk $name: preservation FAIL ($witness)"; rc=1; }
  504            done
  505          else
  506            echo "walk $name: final preservation witness failed"; rc=1
  507          fi
  508          ;; esac
  509        echo "walk $name: $(ls "$OUT/walks/$name/" 2>/dev/null | wc -l) frames  [$(echo $legs)]"
  510      done < "$suite"
  511      return $rc
  512    }
  513    run_suite walks "$OUT/walks.log" walk_all ;; esac
  514  # The walk frames against the last cut the maintainer accepted (#252): every
  515  # box of differing pixels outside tools/vm-walks/masks.txt must be inside a
  516  # claim in tools/vm-walks/claims.txt, or the suite fails. No baseline is a
  517  # SKIP the table shows, never a quiet pass -- accept one with
  518  #   tools/frame-diff accept <run>/walks <baseline> --build <id>
  519  # once a cut is on the device. WALK_BASELINE overrides the directory.
  520  frame_diff_suite() {
  521    local base="${WALK_BASELINE:-$(dirname "$OUT")/walk-baseline}"
  522    if [ ! -f "$base/BASELINE.txt" ]; then
  523      echo "frame-diff: no baseline at $base -- accept one: tools/frame-diff accept <run>/walks $base --build <id>"; return 3
  524    fi
  525    "$ROOT/tools/frame-diff" compare "$base" "$OUT/walks" --masks "$ROOT/tools/vm-walks/masks.txt" --claims "$ROOT/tools/vm-walks/claims.txt" --report "$OUT/frame-diff.md"
  526  }
  527  case ",$ONLY," in *,frame-diff,*) run_suite frame-diff "$OUT/frame-diff.log" frame_diff_suite ;; esac
  528  { echo; if [ "$FAILS" = 0 ] && [ "$SKIPS" = 0 ]; then echo "**PASSED** -- every suite that ran passed."; elif [ "$FAILS" = 0 ]; then echo "**PASSED with $SKIPS suite(s) SKIPPED** -- a skipped suite could not run (its log says why) and has not passed."; else echo "**FAILED** -- $FAILS suite(s) failed; see the logs beside this file."; fi; echo; echo "finished $(date -u '+%Y-%m-%d %H:%M UTC')"; } >> "$REPORT"
  529  # The time-to-play numbers go BELOW the footer, not into the suite table: the
  530  # table is one row per suite and this cell reports four of its own. No budget
  531  # row exists yet, so nothing here fails the run -- the numbers are reported
  532  # and a register row is proposed from them by hand (D-CLOUD-116).
  533  if [ -f "$OUT/time-to-play/time-to-play.md" ]; then
  534    # Demoted a level each, so the cell's own sections sit under its heading
  535    # rather than beside the report's.
  536    { echo; sed -e 's/^## /### /' -e '1s/^# /## /' "$OUT/time-to-play/time-to-play.md"; } >> "$REPORT"
  537  fi
  538  RENDERER=$(SSH 'grep -h -m1 "\[GL\].*Renderer:" /var/log/exec.log 2>/dev/null' 2>/dev/null | sed 's/.*Renderer: //' | tr -d '\r')
  539  { echo; echo "renderer: ${RENDERER:-(no RetroArch launch log on the guest)} -- the guest's Mesa, from the launch log; display: $DISPLAY_MODE"; } >> "$REPORT"
  540  echo; cat "$REPORT"; echo; echo "report: $REPORT"
  541  [ "$FAILS" = 0 ]
  542  
```

## file, whole, at 8ebaf8daad: tools/vm-serial

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # A root shell in a headless GENERIC_X64 guest, over its serial console.
    6  #
    7  # The image ships serial-debug-shell.service: an autologin root /bin/sh on
    8  # ttyS0. With `generic-x64-vm run --headless` that console is a unix socket
    9  # on the host, and this is the client for it. SSH is off on a fresh image
   10  # and resets mid-handshake on a busy one; the serial line is the channel
   11  # that works from the first boot.
   12  #
   13  #   vm-serial sh 'uname -a; df -h /storage'        # one command, its output
   14  #   vm-serial script setup.sh                       # a whole file, run with sh
   15  #   vm-serial wait                                  # until EmulationStation is up
   16  #   vm-serial wait --for 'test -f /storage/.done'   # until a shell test passes
   17  #
   18  # Every command is wrapped in unique BEG/END markers because the boot console
   19  # shares the line, and echo is switched off first so the command is not read
   20  # back as output. A script goes across as base64 in one line, so the line
   21  # discipline never sees a heredoc or a quote it might misparse.
   22  #
   23  # Busybox in the guest: no `pgrep -c`, no `comm`, no `find -printf`. The
   24  # default wait test uses `pgrep emulationstation | wc -l` for that reason.
   25  import argparse
   26  import base64
   27  import socket
   28  import sys
   29  import time
   30  import uuid
   31  
   32  DEFAULT_SOCKET = "/tmp/rocknix-qemu-serial.sock"
   33  
   34  
   35  class Serial:
   36      def __init__(self, path, timeout):
   37          self.timeout = timeout
   38          self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
   39          self.sock.settimeout(timeout)
   40          self.sock.connect(path)
   41          self.sock.sendall(b"\nstty -echo 2>/dev/null\n")
   42          self._drain(0.3)
   43  
   44      def _drain(self, seconds):
   45          self.sock.settimeout(seconds)
   46          try:
   47              while self.sock.recv(65536):
   48                  pass
   49          except (socket.timeout, TimeoutError):
   50              pass
   51          self.sock.settimeout(self.timeout)
   52  
   53      def run(self, command):
   54          """Run one shell command line; return (output, ok)."""
   55          tag = uuid.uuid4().hex[:8]
   56          beg, end = "BEG" + tag, "END" + tag
   57          self.sock.sendall(("echo %s; %s; echo %s\n" % (beg, command, end)).encode())
   58          buf = b""
   59          deadline = time.time() + self.timeout
   60          while time.time() < deadline:
   61              try:
   62                  chunk = self.sock.recv(65536)
   63              except (socket.timeout, TimeoutError):
   64                  break
   65              if not chunk:
   66                  break
   67              buf += chunk
   68              if end.encode() in buf:
   69                  break
   70          text = buf.decode(errors="replace")
   71          i, j = text.find(beg), text.find(end)
   72          if i >= 0 and j > i:
   73              return text[i + len(beg):j].strip("\r\n"), True
   74          return text, False
   75  
   76      def close(self):
   77          self.sock.close()
   78  
   79  
   80  def main():
   81      ap = argparse.ArgumentParser(description="a root shell in a headless GENERIC_X64 guest, over serial")
   82      ap.add_argument("--socket", default=DEFAULT_SOCKET, help="the VM's serial socket (default: %(default)s)")
   83      ap.add_argument("--timeout", type=float, default=60, help="seconds to wait for a command's END marker")
   84      sub = ap.add_subparsers(dest="command", required=True)
   85      sh = sub.add_parser("sh", help="run one command line and print its output")
   86      sh.add_argument("cmdline")
   87      sc = sub.add_parser("script", help="upload a file and run it with sh")
   88      sc.add_argument("path")
   89      sc.add_argument("--interpreter", default="sh")
   90      w = sub.add_parser("wait", help="poll until a shell test passes (default: EmulationStation is running)")
   91      w.add_argument("--for", dest="test", default='[ "$(pgrep emulationstation | wc -l)" = 1 ]')
   92      w.add_argument("--every", type=float, default=5)
   93      w.add_argument("--up-to", type=float, default=300, help="seconds before giving up")
   94      args = ap.parse_args()
   95  
   96      if args.command == "wait":
   97          deadline = time.time() + args.up_to
   98          started = time.time()
   99          while time.time() < deadline:
  100              try:
  101                  s = Serial(args.socket, min(args.timeout, 8))
  102                  out, ok = s.run("if %s; then echo READY; fi" % args.test)
  103                  s.close()
  104                  if ok and "READY" in out:
  105                      print("ready after ~%ds" % (time.time() - started))
  106                      return 0
  107              except (OSError, socket.timeout, TimeoutError):
  108                  pass
  109              time.sleep(args.every)
  110          print("not ready after %ds" % args.up_to, file=sys.stderr)
  111          return 1
  112  
  113      s = Serial(args.socket, args.timeout)
  114      try:
  115          if args.command == "sh":
  116              out, ok = s.run(args.cmdline)
  117          else:
  118              with open(args.path, "rb") as fh:
  119                  blob = base64.b64encode(fh.read()).decode()
  120              name = "/tmp/vm-serial-%s" % uuid.uuid4().hex[:6]
  121              out, ok = s.run("echo %s | base64 -d > %s && %s %s 2>&1" % (blob, name, args.interpreter, name))
  122      finally:
  123          s.close()
  124      if out:
  125          print(out)
  126      if not ok:
  127          print("vm-serial: no END marker within %.0fs (command still running, or the guest is down)" % args.timeout, file=sys.stderr)
  128          return 2
  129      return 0
  130  
  131  
  132  if __name__ == "__main__":
  133      sys.exit(main())
  134  
```

## file, whole, at 8ebaf8daad: tools/vm-stop

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated (https://github.com/pixelelated)
    4  """Stop the exact owned QEMU, awaiting exit before its ports may be reused."""
    5  import argparse
    6  import os
    7  from pathlib import Path
    8  import select
    9  import signal
   10  import sys
   11  
   12  
   13  def stop(pidfile, disk, timeout):
   14      try:
   15          recorded = pidfile.read_text()
   16      except FileNotFoundError:
   17          return
   18      pid = int(recorded.strip())
   19      if pid <= 1:
   20          raise ValueError('invalid guest PID')
   21      proc = Path('/proc') / str(pid)
   22      handle = None
   23      try:
   24          args = (proc / 'cmdline').read_bytes().split(b'\0')
   25          stat = (proc / 'stat').read_text()
   26          start = stat[stat.rfind(')') + 2:].split()[19]
   27          if args and args[0]:
   28              if not Path(os.fsdecode(args[0])).name.startswith('qemu-system-'):
   29                  raise ValueError('PID is not QEMU; refusing to signal it')
   30              drive = os.fsencode('if=none,id=rocknix,format=qcow2,file=' + str(disk))
   31              if not any(args[i] == b'-drive' and args[i + 1] == drive
   32                         for i in range(len(args) - 1)):
   33                  raise ValueError('QEMU does not own the expected disk; refusing to signal it')
   34              handle = os.pidfd_open(pid)
   35              current = (proc / 'stat').read_text()
   36              if (current[current.rfind(')') + 2:].split()[19] != start or
   37                      (proc / 'cmdline').read_bytes().split(b'\0') != args):
   38                  raise ValueError('process identity changed; refusing to signal it')
   39              signal.pidfd_send_signal(handle, signal.SIGTERM)
   40              poller = select.poll()
   41              poller.register(handle, select.POLLIN)
   42              if not poller.poll(round(timeout * 1000)):
   43                  raise TimeoutError('owned QEMU has not exited; retaining pidfile')
   44          # Empty cmdline is an exited zombie: its ports are already released.
   45      except (FileNotFoundError, ProcessLookupError):
   46          pass
   47      finally:
   48          if handle is not None:
   49              os.close(handle)
   50      try:
   51          if pidfile.read_text() != recorded:
   52              raise ValueError('pidfile changed; retaining it')
   53          pidfile.unlink()
   54      except FileNotFoundError:
   55          # Daemonized QEMU removes its own pidfile during normal shutdown.
   56          pass
   57      print('down: owned QEMU exited (pid %d)' % pid)
   58  
   59  
   60  def main():
   61      parser = argparse.ArgumentParser(description=__doc__)
   62      parser.add_argument('--timeout', type=float, default=20)
   63      parser.add_argument('pidfile', type=Path)
   64      parser.add_argument('disk', type=Path)
   65      args = parser.parse_args()
   66      if not 0 < args.timeout <= 60:
   67          parser.error('timeout must be greater than zero and at most 60 seconds')
   68      try:
   69          stop(args.pidfile, args.disk, args.timeout)
   70      except (OSError, ValueError, TimeoutError) as error:
   71          print('vm-stop: ' + str(error), file=sys.stderr)
   72          return 1
   73      return 0
   74  
   75  
   76  if __name__ == '__main__':
   77      sys.exit(main())
   78  
```

## file, whole, at 8ebaf8daad: tools/vm-stop-test

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated (https://github.com/pixelelated)
    4  """Delayed exit, timeout and wrong-owner controls for vm-stop (#454)."""
    5  from pathlib import Path
    6  import subprocess
    7  import socket
    8  import sys
    9  import tempfile
   10  import time
   11  
   12  tool = Path(__file__).resolve().with_name('vm-stop')
   13  fixture = '''import signal,socket,sys,time,os
   14  s=socket.socket();s.bind(('127.0.0.1',0));s.listen()
   15  def quit(signum,frame):
   16   time.sleep(0.2)
   17   if sys.argv[-1].startswith('remove:'):os.unlink(sys.argv[-1][7:])
   18   sys.exit(0)
   19  signal.signal(signal.SIGTERM, signal.SIG_IGN if sys.argv[-1]=='ignore' else quit)
   20  print(s.getsockname()[1],flush=True)
   21  while True: time.sleep(1)
   22  '''
   23  passed = 0
   24  with tempfile.TemporaryDirectory() as temp:
   25      root = Path(temp)
   26      disk = root/'owned.qcow2'
   27      pidfile = root/'guest.pid'
   28      for case in ['delayed-exit','self-removed-pidfile','timeout','wrong-disk','wrong-process']:
   29          argv0 = 'python-fixture' if case == 'wrong-process' else 'qemu-system-fixture'
   30          child = subprocess.Popen([argv0,'-c',fixture,'-drive',
   31              'if=none,id=rocknix,format=qcow2,file='+str(disk),
   32              'ignore' if case == 'timeout' else 'remove:'+str(pidfile) if case == 'self-removed-pidfile' else 'delay'], executable=sys.executable,
   33              stdout=subprocess.PIPE, text=True)
   34          try:
   35              port = int(child.stdout.readline())
   36              pidfile.write_text(str(child.pid)+'\n')
   37              start = time.monotonic()
   38              result = subprocess.run([str(tool),'--timeout','0.05' if case == 'timeout' else '2',
   39                  str(pidfile),str(root/'other.qcow2' if case == 'wrong-disk' else disk)],
   40                  capture_output=True,text=True,timeout=4)
   41              if case in ['delayed-exit','self-removed-pidfile']:
   42                  assert result.returncode == 0 and time.monotonic()-start >= 0.19, result
   43                  assert child.wait(timeout=1) == 0 and not pidfile.exists()
   44                  with socket.socket() as listener:
   45                      listener.bind(('127.0.0.1',port))
   46                  print('PASS '+case+' waits for exit and immediate port reuse')
   47              else:
   48                  assert result.returncode == 1 and child.poll() is None and pidfile.exists(), result
   49                  assert {'timeout':'retaining pidfile','wrong-disk':'expected disk',
   50                          'wrong-process':'not QEMU'}[case] in result.stderr,result.stderr
   51                  print('PASS '+case+' refuses completion and retains live process/pidfile')
   52              passed += 1
   53          finally:
   54              if child.poll() is None:
   55                  child.kill()
   56              child.wait(timeout=2)
   57              child.stdout.close()
   58              pidfile.unlink(missing_ok=True)
   59      # A dead owned PID and a missing pidfile are idempotent shutdowns.
   60      pidfile.write_text(str(child.pid)+'\n')
   61      assert subprocess.run([str(tool),str(pidfile),str(disk)],capture_output=True).returncode == 0
   62      assert not pidfile.exists()
   63      assert subprocess.run([str(tool),str(pidfile),str(disk)],capture_output=True).returncode == 0
   64      passed += 2
   65      print('PASS exited PID and missing pidfile are idempotent')
   66  print('PASS %d vm-stop controls' % passed)
   67  
```

## file, whole, at 8ebaf8daad: tools/vm-upgrade-readiness-test

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated (https://github.com/pixelelated)
    4  """Exercise the rehearsal's actual wait and guest query with disposable guest-query fixtures."""
    5  import argparse
    6  from pathlib import Path
    7  import subprocess
    8  import tempfile
    9  
   10  parser = argparse.ArgumentParser(description=__doc__)
   11  parser.add_argument('--rehearsal', type=Path,
   12                      default=Path(__file__).with_name('vm-upgrade-rehearsal'))
   13  args = parser.parse_args()
   14  try:
   15      source = args.rehearsal.read_text()
   16  except (OSError, UnicodeError) as error:
   17      parser.error(f'cannot read rehearsal {args.rehearsal}: {error}')
   18  _, start, remainder = source.partition('wait_for_storage() {')
   19  body, end, _ = remainder.partition('\n}\n')
   20  if not start or not end:
   21      parser.error(f'{args.rehearsal}: missing or incomplete wait_for_storage function')
   22  function = start + body + end
   23  
   24  with tempfile.TemporaryDirectory(prefix='upgrade-ready-') as directory:
   25      root = Path(directory)
   26      (root / 'shim').mkdir()
   27      unit = root / 'shim/systemctl'
   28      unit.write_text('''#!/bin/bash
   29  [ "$*" = 'is-active rocknix-autostart.service' ] || exit 64
   30  state=$(cat "$FIXTURE_G/state")
   31  printf '%s\\n' "$state"
   32  [ "$state" = active ]
   33  ''')
   34      unit.chmod(0o755)
   35      reader = root / 'shim/cat'
   36      reader.write_text('''#!/bin/bash
   37  case "$*" in
   38      /proc/sys/kernel/random/boot_id) exec /usr/bin/cat "$FIXTURE_G/boot_id" ;;
   39      /var/log/boot.log) exec /usr/bin/cat "$FIXTURE_G/var/log/boot.log" ;;
   40      *) exec /usr/bin/cat "$@" ;;
   41  esac
   42  ''')
   43      reader.chmod(0o755)
   44      shell = '''set -u
   45  G=$1; FINISH=$2; READY=$3; EXPECTED=$4; TRANSPORT=$5
   46  LOG="$G/log"
   47  sleep() { :; }
   48  ssha() {
   49      local n
   50      n=$(( $(cat "$G/polls") + 1 )); echo "$n" > "$G/polls"
   51      [ "$TRANSPORT" = absent ] && return 1
   52      if [ "$FINISH" != never ] && [ "$n" -ge "$FINISH" ]; then
   53          echo "$READY" > "$G/state"
   54      fi
   55      # Execute the source's unchanged query; only cat's two guest paths and
   56      # systemctl are fixture-backed. CI needs no namespace privilege/package.
   57      FIXTURE_G="$G" PATH="$G/../shim:$PATH" bash -c "$*"
   58  }
   59  ''' + function + '\nwait_for_storage "$EXPECTED"\n'
   60      cases = [
   61          # case, guest boot, finish poll, final state, expected boot, transport, rc, polls
   62          ('ready', 'current', '1', 'active', 'current', 'present', 0, 1),
   63          ('old-boot', 'previous', '1', 'active', 'current', 'present', 1, 30),
   64          ('failed', 'current', '1', 'failed', 'current', 'present', 1, 1),
   65          ('delayed', 'current', '4', 'active', 'current', 'present', 0, 4),
   66          ('never-ready', 'current', 'never', 'active', 'current', 'present', 1, 30),
   67          ('absent', 'current', '1', 'active', 'current', 'absent', 1, 30),
   68          ('no-identity', 'current', '1', 'active', '', 'present', 1, 0),
   69      ]
   70      for case, boot, finish, state, expected, transport, code, polls in cases:
   71          p = root / case
   72          (p / 'var/log').mkdir(parents=True)
   73          # A stale success must not short-circuit the current boot's unit check.
   74          (p / 'var/log/boot.log').write_text('Previous boot: Autostart complete...\n')
   75          (p / 'boot_id').write_text(boot+'\n')
   76          (p / 'state').write_text('activating\n')
   77          (p / 'polls').write_text('0\n')
   78          result = subprocess.run(
   79              ['bash', '-c', shell, 'fixture', str(p), finish, state, expected, transport],
   80              capture_output=True, text=True, timeout=15)
   81          observed_polls = int((p / 'polls').read_text())
   82          assert (result.returncode, observed_polls) == (code, polls), (
   83              case, result.returncode, observed_polls, result.stdout, result.stderr)
   84          assert not result.stderr, (case, result.stderr)
   85          assert ('PASS storage ready' if code == 0 else 'FAIL storage readiness') in result.stdout, (case, result.stdout)
   86          print(f'PASS {case}: return {code}, polls {polls}', flush=True)
   87  print('PASS 7 storage-readiness controls; actual guest query, synthetic states, no boot claim')
   88  
```

## file, whole, at 8ebaf8daad: tools/vm-upgrade-rehearsal

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # vm-upgrade-rehearsal -- the upgrade path, rehearsed in a VM before a handheld
    6  # takes it (upgrade-and-install.md: "boot a VM from the previous image, use it
    7  # enough to create state, then update it in place and confirm that state still
    8  # works").
    9  #
   10  #   tools/vm-upgrade-rehearsal <previous ROCKNIX-GENERIC_X64...img.gz> <new ROCKNIX-GENERIC_X64...tar> <expected new BUILD_ID prefix>
   11  #
   12  # Boots vm-pair's guest a from the previous image, seeds state a player would
   13  # have -- an auto save and two numbered save states, a battery save, a
   14  # setting, a marker file, a linked cloud (the local QA backend) with a saves
   15  # remote, and a settings backup -- then puts the new tar in /storage/.update,
   16  # reboots, and checks every piece against what was seeded. Every check is a
   17  # PASS/FAIL line; the exit code is 0 only when all pass. The fixture asserts
   18  # its own seeding before the step under test, so a fixture fault cannot be
   19  # booked to the build (2026-09-20, generic-x64-vm-testing.md).
   20  #
   21  # Output: a directory under /workspace/artifacts/rocknix-images/ named
   22  # qa-<new>-upgrade-from-<old>-<stamp>/ with rehearsal.log, the post-update
   23  # journal errors, and rc.
   24  set -u
   25  OLD=${1:?previous image (.img.gz)}; NEW=${2:?new update tar}; WANT=${3:?expected new BUILD_ID prefix}
   26  [ -f "$OLD" ] || { echo "no such image: $OLD" >&2; exit 2; }
   27  [ -f "$NEW" ] || { echo "no such tar: $NEW" >&2; exit 2; }
   28  cd "$(dirname "$0")/.." || exit 2
   29  OLDID=$(basename "$(dirname "$OLD")" | grep -oE '[0-9a-f]{10}$' || echo previous)   # the artifact directories end in the BUILD_ID
   30  OUT=/workspace/artifacts/rocknix-images/qa-${WANT}-upgrade-from-${OLDID}-$(date -u +%Y%m%d-%H%M); mkdir -p "$OUT"
   31  LOG=$OUT/rehearsal.log; : > "$LOG"
   32  say(){ echo "=== $(date -u '+%H:%M:%S') $*" | tee -a "$LOG"; }
   33  ssha(){ ./tools/vm-pair ssh a ". /etc/profile >/dev/null 2>&1; $*" 2>>"$LOG"; }
   34  fail=0
   35  check(){ if [ "$2" = "$3" ]; then echo "PASS $1" | tee -a "$LOG"; else echo "FAIL $1: got '$2' want '$3'" | tee -a "$LOG"; fail=1; fi; }
   36  
   37  # SSH answers before autostart has mounted the ROM tree. Readiness belongs to
   38  # the current boot, before seeding or reading retained state (#546).
   39  wait_for_storage() {
   40    local expected_boot=$1 observed i
   41    [ -n "$expected_boot" ] || { echo 'FAIL storage readiness: no boot identity' | tee -a "$LOG"; return 1; }
   42    for i in $(seq 1 30); do
   43      observed=$(ssha 'echo "$(cat /proc/sys/kernel/random/boot_id) $(systemctl is-active rocknix-autostart.service)"' 2>/dev/null)
   44      if [ "$observed" = "$expected_boot active" ]; then
   45        echo "PASS storage ready in boot $expected_boot after $i poll(s)" | tee -a "$LOG"
   46        return 0
   47      fi
   48      [ "$observed" = "$expected_boot failed" ] && break
   49      sleep 2
   50    done
   51    echo "FAIL storage readiness: expected $expected_boot active, got ${observed:-no answer}" | tee -a "$LOG"
   52    return 1
   53  }
   54  
   55  say "backend: $(./tools/cloud-test-backend status 2>&1 | head -1)"; ./tools/cloud-test-backend up >>"$LOG" 2>&1 || true
   56  say "pair up from $(basename "$OLD")"
   57  ./tools/vm-pair up "$OLD" >>"$LOG" 2>&1 || { say "vm-pair up FAILED"; echo 1 > "$OUT/rc"; exit 1; }
   58  for i in $(seq 1 40); do ssha 'echo ok' 2>/dev/null | grep -q '^ok$' && break; sleep 10; done
   59  BID0=$(ssha 'grep ^BUILD_ID= /etc/os-release | cut -d\" -f2'); echo "old build id: $BID0" | tee -a "$LOG"; check "old build id read" "$([ -n "$BID0" ] && echo yes)" "yes"
   60  
   61  SEED_BOOT=$(ssha 'cat /proc/sys/kernel/random/boot_id')
   62  wait_for_storage "$SEED_BOOT" || { echo 1 > "$OUT/rc"; exit 1; }
   63  
   64  say "seed state on guest a"
   65  ssha 'mkdir -p /storage/roms/savestates/nes /storage/roms/nes /storage/.config/rclone
   66  head -c 300000 /dev/urandom > /storage/roms/savestates/nes/Rehearsal.state.auto
   67  head -c 200000 /dev/urandom > /storage/roms/savestates/nes/Rehearsal.state1
   68  head -c 100000 /dev/urandom > /storage/roms/savestates/nes/Rehearsal.state2
   69  head -c 8192   /dev/urandom > /storage/roms/nes/Rehearsal.srm
   70  echo rehearsal-marker > /storage/.config/rehearsal-marker
   71  set_setting rehearsal.marker '"$WANT"'; sync' >>"$LOG" 2>&1
   72  SUMS0=$(ssha 'cd /storage/roms && sha256sum savestates/nes/Rehearsal.state.auto savestates/nes/Rehearsal.state1 savestates/nes/Rehearsal.state2 nes/Rehearsal.srm'); echo "$SUMS0" >> "$LOG"
   73  check "four seeded files exist" "$(echo "$SUMS0" | grep -c '^[0-9a-f]\{64\} ')" "4"
   74  check "set_setting is a function on the guest" "$(ssha 'command -v set_setting >/dev/null && echo yes')" "yes"
   75  check "setting reads back before the update" "$(ssha 'get_setting rehearsal.marker')" "$WANT"
   76  
   77  say "link the local WebDAV backend"
   78  CONF=$(./tools/cloud-test-backend rclone-conf 2>>"$LOG"); check "backend gave an rclone.conf" "$([ -n "$CONF" ] && echo yes)" "yes"
   79  ssha "cat > /storage/.config/rclone/rclone.conf <<'RC'
   80  $CONF
   81  RC
   82  chmod 600 /storage/.config/rclone/rclone.conf" >>"$LOG" 2>&1
   83  ACTIVE_READER='if test -f "$(dirname "$(command -v cloud_remote)")/cloud_connections.py"; then cloud_remote active; else rclone listremotes 2>/dev/null | head -1; fi'
   84  QA_REMOTE=$(./tools/cloud-test-backend remote-name)
   85  ssha "if test -e /storage/.config/rclone/active-connection; then printf '%s\n' '$QA_REMOTE' > /storage/.config/rclone/active-connection; fi" >>"$LOG" 2>&1
   86  ACTIVE0=$(ssha 'if test -e /storage/.config/rclone/active-connection; then sha256sum /storage/.config/rclone/active-connection; else echo absent; fi')
   87  REM0=$(ssha "$ACTIVE_READER"); echo "remote: $REM0" >> "$LOG"
   88  check "guest sees one remote" "$([ -n "$REM0" ] && echo yes)" "yes"
   89  ssha "rclone mkdir ${REM0}Rehearsal/Saves 2>>/dev/null; cloud_setup --set-saves-remote /Rehearsal/Saves" >>"$LOG" 2>&1
   90  CONFPATH=$(ssha 'ls /storage/.config/cloud_sync.conf 2>/dev/null || find /storage/.config -maxdepth 2 -name cloud_sync.conf | head -1')
   91  SR0=$(ssha "grep -E '^SAVES_REMOTE=' $CONFPATH 2>/dev/null"); echo "saves remote before: $SR0 ($CONFPATH)" >> "$LOG"
   92  check "saves remote set before the update" "$(echo "$SR0" | grep -c Rehearsal)" "1"
   93  check "rclone (previous) lists the remote" "$(ssha "rclone lsd ${REM0} >/dev/null 2>&1 && echo ok")" "ok"
   94  
   95  say "a settings backup"
   96  ssha 'backuptool backup >/dev/null 2>&1; ls /storage/roms/backup/ 2>/dev/null' >>"$LOG" 2>&1
   97  BK0=$(ssha 'ls /storage/roms/backup/ 2>/dev/null | wc -l'); echo "backups before: $BK0" >> "$LOG"
   98  
   99  say "seed what the retired GENERIC_X64 quirks left in /storage (#307 PL-019)"
  100  # Until 2026-09 the QEMU quirks 091-101 wrote these through the image's links
  101  # into /storage, and 097-disable-rescue-completely masked emergency.target
  102  # into /storage/.config/system.d; a guest that ran them keeps them across an
  103  # update. The new image's 091-retired-vm-fixes and 097-retired-rescue-masks
  104  # take them back by name until their stamps under /storage/.cache are
  105  # written; after that, only a file with an old quirk's own bytes (a
  106  # downgrade and back, which tools/last-good-scripts-test's F1r-b runs).
  107  # The fixture writes them itself, and removes those stamps, so the check does
  108  # not depend on which quirks the previous image carried -- a guest that ran
  109  # the old quirks has no stamp -- and beside them a file of the owner's own,
  110  # which must stay.
  111  RETIRED=".config/tmpfiles.d/20-x64-fd-improvements.conf .config/sysctl.d/10-generic-x64.conf .config/modules-load.d/x64-virtual-modules.conf .config/profile.d/091-generic-x64-services"
  112  ssha "cd /storage && rm -f .cache/retired-vm-fixes .cache/retired-rescue-masks && for f in $RETIRED; do mkdir -p \$(dirname \$f); echo '# seeded by vm-upgrade-rehearsal (#307 PL-019)' > \$f; done
  113  mkdir -p .config/system.d && ln -sfn /dev/null .config/system.d/emergency.target
  114  echo '# the owner'\''s own (vm-upgrade-rehearsal)' > .config/tmpfiles.d/50-rehearsal-owner.conf; sync" >>"$LOG" 2>&1
  115  check "retired quirk files seeded before the update" "$(ssha "cd /storage && ls $RETIRED .config/tmpfiles.d/50-rehearsal-owner.conf 2>/dev/null | wc -l; readlink .config/system.d/emergency.target" | tr '\n' ' ')" "5 /dev/null "
  116  
  117  say "seed a RetroArch cfg an owner changed, on a vulkan-era cfg (#307 PL-034, #308 claude F-VM-11)"
  118  # The fullscreen size set by hand must survive the update and the new
  119  # 092-retroarch-surface, which follows the guest's mode only for values of
  120  # its own; the driver the device shipped until 2026-09, vulkan, moves to gl
  121  # on an image with no Vulkan driver.
  122  RACFG=/storage/.config/retroarch/retroarch.cfg
  123  ssha "sed -i -e 's/^video_fullscreen_x = .*/video_fullscreen_x = \"1024\"/' -e 's/^video_fullscreen_y = .*/video_fullscreen_y = \"768\"/' -e 's/^video_driver = .*/video_driver = \"vulkan\"/' $RACFG; sync" >>"$LOG" 2>&1
  124  check "RetroArch cfg seeded before the update" "$(ssha "grep -E '^(video_fullscreen_x|video_fullscreen_y|video_driver) = ' $RACFG | sort | tr '\n' ' '")" 'video_driver = "vulkan" video_fullscreen_x = "1024" video_fullscreen_y = "768" '
  125  
  126  say "stage $(basename "$NEW") and reboot guest a"
  127  # The pair's key and port come from vm-pair, not from literals here (they
  128  # were, and a pair on other settings would have gone unrehearsed -- audit
  129  # #258 PL-030); the wait for the reboot is a poll, not a guess.
  130  ./tools/vm-pair scp a "$NEW" /storage/.update/ 2>>"$LOG" || { say "scp FAILED"; fail=1; }
  131  ssha 'sync; ls -la /storage/.update/' >>"$LOG" 2>&1
  132  BOOT0=$(ssha 'cat /proc/sys/kernel/random/boot_id' 2>/dev/null)
  133  ssha 'sync; reboot' >/dev/null 2>&1
  134  # Down, then up: the boot id changes when the new boot answers. Up to five
  135  # minutes for the update to unpack and the guest to come back.
  136  # BOOT1 is the new boot's id, kept for the autostart wait below.
  137  BID1=""; BOOT1=""; for i in $(seq 1 60); do
  138    B=$(ssha 'cat /proc/sys/kernel/random/boot_id' 2>/dev/null)
  139    if [ -n "$B" ] && [ "$B" != "$BOOT0" ]; then BID1=$(ssha 'grep ^BUILD_ID= /etc/os-release | cut -d\" -f2' 2>/dev/null); [ "${BID1:0:${#WANT}}" = "$WANT" ] && { BOOT1=$B; break; }; fi
  140    sleep 5
  141  done
  142  say "guest a back after $i polls"
  143  check "new build id is $WANT" "${BID1:0:${#WANT}}" "$WANT"
  144  wait_for_storage "$BOOT1" || { echo 1 > "$OUT/rc"; exit 1; }
  145  SUMS1=$(ssha 'cd /storage/roms && sha256sum savestates/nes/Rehearsal.state.auto savestates/nes/Rehearsal.state1 savestates/nes/Rehearsal.state2 nes/Rehearsal.srm')
  146  check "saves and save states byte-identical" "$SUMS1" "$SUMS0"
  147  check "marker file kept" "$(ssha 'cat /storage/.config/rehearsal-marker')" "rehearsal-marker"
  148  check "setting kept" "$(ssha 'get_setting rehearsal.marker')" "$WANT"
  149  check "active rclone remote kept" "$(ssha "$ACTIVE_READER")" "$REM0"
  150  check "active selection bytes/presence kept" "$(ssha 'if test -e /storage/.config/rclone/active-connection; then sha256sum /storage/.config/rclone/active-connection; else echo absent; fi')" "$ACTIVE0"
  151  check "rclone (new) lists the remote" "$(ssha "rclone lsd ${REM0} >/dev/null 2>&1 && echo ok")" "ok"
  152  check "saves remote kept" "$(ssha "grep -E '^SAVES_REMOTE=' $CONFPATH 2>/dev/null")" "$SR0"
  153  check "cloud conf gained the new defaults, kept the old values" "$(ssha "grep -cE '^(CONTENT_REMOTE|SAVES_REMOTE)=' $CONFPATH")" "2"
  154  check "backup archive kept" "$(ssha 'ls /storage/roms/backup/ 2>/dev/null | wc -l')" "$BK0"
  155  check "update queue empty" "$(ssha 'ls /storage/.update | wc -l')" "0"
  156  check "retired quirk files taken back after the update (#307 PL-019)" "$(ssha "cd /storage && ls $RETIRED 2>/dev/null | wc -l; [ -L .config/system.d/emergency.target ] && echo masked || echo unmasked" | tr '\n' ' ')" "0 unmasked "
  157  check "and the owner's file beside them kept" "$(ssha 'cat /storage/.config/tmpfiles.d/50-rehearsal-owner.conf')" "# the owner's own (vm-upgrade-rehearsal)"
  158  check "RetroArch fullscreen size set by hand kept, driver moved to gl (#307 PL-034, #308 claude F-VM-11)" "$(ssha "grep -E '^(video_fullscreen_x|video_fullscreen_y|video_driver) = ' $RACFG | sort | tr '\n' ' '")" 'video_driver = "gl" video_fullscreen_x = "1024" video_fullscreen_y = "768" '
  159  # --- release checks: assertions about one release's defects, not about the
  160  # upgrade path. Each names its issue; drop it when the issue's cause is gone
  161  # upstream (audit #258 PL-030 asked that a generic tool label these).
  162  check "release check #226: one libcairo.so.2.* (pango's fetched cairo is gone)" "$(ssha 'ls /usr/lib/libcairo.so.2.* | wc -l')" "1"
  163  check "release check #226: libcairo.so.2 is a link to that one file (#226 box 1; the seat's G-10 under #258)" "$(ssha 'readlink /usr/lib/libcairo.so.2')" "$(ssha 'basename $(ls /usr/lib/libcairo.so.2.*)')"
  164  echo "rclone after: $(ssha 'rclone version | head -1')" | tee -a "$LOG"
  165  ssha 'journalctl -b -p err --no-pager | tail -30' > "$OUT/journal-err-after.txt" 2>&1
  166  ssha 'ls -la /storage/roms/savestates/nes /storage/roms/nes; cat /etc/os-release' > "$OUT/state-after.txt" 2>&1
  167  say "pair down"; ./tools/vm-pair down >>"$LOG" 2>&1
  168  if [ $fail = 0 ]; then say "RESULT PASS"; else say "RESULT FAIL"; fi
  169  echo $fail > "$OUT/rc"; echo "$OUT"
  170  exit $fail
  171  
```

## file, whole, at 8ebaf8daad: tools/vm-visual-qa

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # Drive a running GENERIC_X64 QEMU VM through a UI script and capture what
    6  # it draws, so UI work can be reviewed (by a human or an image model)
    7  # without anyone flashing a device or taking phone photos of a handheld.
    8  #
    9  # It talks to QEMU's human monitor over a unix socket: `sendkey` presses
   10  # keys the guest sees as real input, and `screendump` writes the current
   11  # framebuffer as a PPM - both work with `-display none`, which is what
   12  # makes this usable on a headless build host.
   13  #
   14  #   vm-visual-qa --monitor /tmp/mon.sock run steps.txt --outdir shots/
   15  #   vm-visual-qa --monitor /tmp/mon.sock shot one.png
   16  #
   17  # A step file is one instruction per line, blank lines and # comments
   18  # ignored:
   19  #
   20  #   key down            # press a key (QEMU keyname, e.g. down, ret, esc)
   21  #   key down x4         # press it several times
   22  #   wait 2              # a fixed delay in seconds (see "Fixed waits", below)
   23  #   shot main-menu      # capture a frame, labelled
   24  #   settle              # wait until the screen stops changing
   25  #   wait-for-change     # wait until the last `key` has visibly landed
   26  #   wake                # the screensaver wake key, then settle
   27  #   dismiss-dialogs     # close whatever is open, ending on the carousel
   28  #
   29  # WHY THE FRAME STEPS EXIST (fork #125). A step file made of fixed delays is
   30  # a guess about a machine that is also building an image: a press one second
   31  # after a screen change is regularly eaten, and the walk then runs its whole
   32  # remainder one screen out of phase - a switch that did not toggle, a game
   33  # list that did not launch, a LATER that landed on the wrong row and typed
   34  # into a Wi-Fi password field. Three derails on 2026-09-10, two on
   35  # 2026-09-11. `settle` and `wait-for-change` replace the guess with the
   36  # framebuffer: they watch the frames QEMU is already able to hand us.
   37  #
   38  #   settle [timeout_s] [quiet_s]
   39  #       Poll until the frame has held still for quiet_s (default 1.2 s),
   40  #       giving up after timeout_s (default 20 s) and saying so. Use it
   41  #       before every `shot` and after anything that loads, scans or
   42  #       transfers. Bounded, and never fails a walk: a screen with a live
   43  #       element (a spinner, a running transfer's elapsed time) simply runs
   44  #       to the bound.
   45  #
   46  #       The quiet period is deliberately longer than two polls. "Two
   47  #       consecutive identical frames" is defeated by anything that repaints
   48  #       about once a second - a clock, a transfer timer - because two polls
   49  #       half a second apart can both land inside the same second.
   50  #
   51  #   wait-for-change [timeout_s] [retries]
   52  #       Wait until the frame differs from the one taken just before the
   53  #       most recent `key` step - and that frame is taken from a screen that
   54  #       has stopped moving, so the tail of the previous transition cannot
   55  #       be mistaken for this press landing. Gives up after timeout_s
   56  #       (default 12 s).
   57  #       On a timeout the key was eaten: the step is re-sent (default 1
   58  #       retry) and, if that changes nothing either, the walk FAILS naming
   59  #       the key and the line - loudly, instead of silently running the rest
   60  #       of the file against the wrong screen. `wait-for-change 12 0` turns
   61  #       the retry off where a second press would be harmful.
   62  #
   63  # `key` settles and captures the pre-press frame only when the file uses
   64  # `wait-for-change` somewhere, so old step files cost exactly what they
   65  # used to. That settle is why a walk written on these steps needs no
   66  # `wait 1` between presses: the tool is already waiting for the screen
   67  # rather than for the clock.
   68  #
   69  # Frames are compared by bytes, not by OCR: the fraction of differing bytes
   70  # in the PPM. Below SAME_MAX the screen is "unchanged" (a clock digit is
   71  # not a screen change); above CHANGED_MIN it has "changed". The gap between
   72  # them is the deliberate dead band.
   73  #
   74  # Fixed waits. `wait N` still exists and still has two honest uses: a
   75  # deliberate sampler (run-transfer-frames.steps takes a frame every three
   76  # seconds on purpose), and a pause where nothing on screen will change, so
   77  # there is nothing to settle on. Anywhere else it is the bug this file's
   78  # frame steps were added to remove.
   79  #
   80  # WHAT THE INTERFACE DOES, so a walk does not have to rediscover it:
   81  #
   82  #   - Keys: START = `ret`, A = `x`, B = `z`, X = `s`, Y = `a`,
   83  #     SELECT = `shift_r`, arrows for direction. Read
   84  #     /storage/.config/emulationstation/es_input.cfg on the guest rather
   85  #     than trusting this.
   86  #   - After five idle minutes the first key only wakes the screensaver.
   87  #     `wake` sends `shift`, which EmulationStation ignores, so it costs no
   88  #     press that a walk needed. Wake first, every time.
   89  #   - `up` from a page's first row lands on its BACK button, and only then
   90  #     wraps to the last row. The button bar is a focus stop on every page.
   91  #   - B on the system carousel does not close anything: it opens GO TO
   92  #     (GO TO LETTER or GO TO MANUFACTURER, by the SORT SYSTEMS setting).
   93  #     A fixed number of B presses therefore ends on a dialog as often as
   94  #     not; `dismiss-dialogs` presses B until the screen starts repeating
   95  #     itself, which is the carousel toggling GO TO, and stops there.
   96  #   - A boot-time dialog (the journey prompt, the RetroAchievements offer,
   97  #     FINISH RESTORE SETUP) must be dismissed before any walk. That is
   98  #     `wake` then `dismiss-dialogs`.
   99  #   - START on MAIN MENU closes it; a restarted (not rebooted)
  100  #     EmulationStation comes back on the last game list, not the carousel,
  101  #     and screendump can serve the previous ES's frame for half a minute.
  102  #     Walks start from a rebooted guest.
  103  #
  104  # PNG frames need nothing beyond the stdlib; the contact-sheet GIF needs
  105  # Pillow, and without it the frames are still written and everything else
  106  # works.
  107  
  108  import argparse
  109  import struct
  110  import os
  111  import re
  112  import socket
  113  import sys
  114  import tempfile
  115  import time
  116  
  117  # Frame comparison, as a fraction of differing bytes in the PPM. 640x480x3
  118  # is 921600 bytes, so 0.0004 is about 120 pixels and 0.001 about 300.
  119  #
  120  # Measured on guest b, build 88b82d94a7, 640x480, 2026-09-11:
  121  #
  122  #   a menu page with nothing moving       0.000000 over 100 s
  123  #   the carousel's clock ticking a minute 0.000276   <- must read as NO change
  124  #   a switch row toggled                  0.001969   <- must read as a change
  125  #   a selector bar moved one row          0.066 - 0.12
  126  #   a page opened, a dialog closed        0.24 - 1.0
  127  #
  128  # The switch is the tight one: 0.0020 against the clock's 0.00028, and the
  129  # whole point of #125 is a walk that notices a switch which did not toggle.
  130  # So the band sits between them, nearer the clock. Re-measure both numbers
  131  # if the panel size changes - they are pixel counts wearing percentages.
  132  SAME_MAX = 0.0004        # at or below this, the screen has not changed
  133  CHANGED_MIN = 0.001      # at or above this, it has
  134  
  135  SETTLE_TIMEOUT = 20.0
  136  SETTLE_QUIET = 1.2
  137  CHANGE_TIMEOUT = 12.0
  138  CHANGE_RETRIES = 1
  139  POLL = 0.35
  140  # The settle every tracked key does before it captures its pre-press frame:
  141  # short, because the screen is usually already still, and bounded low
  142  # because a key pressed into a page that never stops moving (a running
  143  # transfer) must not wait out a full settle.
  144  PRE_KEY_TIMEOUT = 6.0
  145  PRE_KEY_QUIET = 0.6
  146  
  147  
  148  def vnc_frame(host, port, timeout=10.0):
  149      """One frame from a VNC server as (width, height, RGB bytes): RFB 3.8,
  150      no security (QEMU's -vnc on loopback has none), raw encoding, one
  151      non-incremental update. The standard library only, like the rest of this
  152      file. This is the frame source under a GL scanout (fork #291)."""
  153      def read(n):
  154          b = b""
  155          while len(b) < n:
  156              c = s.recv(n - len(b))
  157              if not c:
  158                  raise OSError("vnc closed")
  159              b += c
  160          return b
  161      s = socket.create_connection((host, port), timeout=timeout)
  162      try:
  163          read(12)
  164          s.sendall(b"RFB 003.008\n")
  165          n = read(1)[0]
  166          if n == 0:
  167              rl = struct.unpack(">I", read(4))[0]
  168              raise OSError("vnc refused: " + read(rl).decode("utf-8", "replace"))
  169          if 1 not in read(n):
  170              raise OSError("vnc wants a security type this grabber does not speak")
  171          s.sendall(b"\x01")
  172          if struct.unpack(">I", read(4))[0] != 0:
  173              raise OSError("vnc security failed")
  174          s.sendall(b"\x01")
  175          w, h = struct.unpack(">HH", read(4))
  176          read(16)
  177          read(struct.unpack(">I", read(4))[0])
  178          # 32-bit true colour, little-endian, so a raw pixel is B G R x
  179          s.sendall(b"\x00\x00\x00\x00" + struct.pack(">BBBBHHHBBB", 32, 24, 0, 1, 255, 255, 255, 16, 8, 0) + b"\x00\x00\x00")
  180          s.sendall(b"\x02\x00" + struct.pack(">H", 1) + struct.pack(">i", 0))
  181          s.sendall(b"\x03\x00" + struct.pack(">HHHH", 0, 0, w, h))
  182          fb = bytearray(w * h * 4)
  183          covered = 0
  184          deadline = time.time() + timeout
  185          while covered < w * h and time.time() < deadline:
  186              mt = read(1)[0]
  187              if mt == 2:
  188                  continue
  189              if mt == 3:
  190                  read(3)
  191                  read(struct.unpack(">I", read(4))[0])
  192                  continue
  193              if mt != 0:
  194                  raise OSError("vnc message %d" % mt)
  195              read(1)
  196              for _ in range(struct.unpack(">H", read(2))[0]):
  197                  x, y, rw, rh, enc = struct.unpack(">HHHHi", read(12))
  198                  if enc != 0:
  199                      raise OSError("vnc encoding %d" % enc)
  200                  data = read(rw * rh * 4)
  201                  for row in range(rh):
  202                      o = ((y + row) * w + x) * 4
  203                      fb[o:o + rw * 4] = data[row * rw * 4:(row + 1) * rw * 4]
  204                  covered += rw * rh
  205      finally:
  206          s.close()
  207      if covered < w * h:
  208          raise OSError("vnc frame incomplete: %d of %d pixels" % (covered, w * h))
  209      rgb = bytearray(w * h * 3)
  210      rgb[0::3] = fb[2::4]
  211      rgb[1::3] = fb[1::4]
  212      rgb[2::3] = fb[0::4]
  213      return w, h, bytes(rgb)
  214  
  215  
  216  class Monitor:
  217      """A connection to QEMU's human monitor (HMP) over a unix socket."""
  218  
  219      def __init__(self, path, timeout=10):
  220          self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
  221          self.sock.settimeout(timeout)
  222          self.sock.connect(path)
  223          self._drain(0.5)
  224          self._scratch = None
  225  
  226      def _drain(self, seconds):
  227          """Absorb whatever the monitor has to say (banner, echoes, prompts)."""
  228          self.sock.settimeout(seconds)
  229          out = b""
  230          try:
  231              while True:
  232                  chunk = self.sock.recv(4096)
  233                  if not chunk:
  234                      break
  235                  out += chunk
  236          except (socket.timeout, TimeoutError):
  237              pass
  238          self.sock.settimeout(10)
  239          return out.decode("utf-8", "replace")
  240  
  241      def cmd(self, text, settle=0.3):
  242          self.sock.sendall((text + "\n").encode())
  243          return self._drain(settle)
  244  
  245      def sendkey(self, key, times=1, gap=0.15):
  246          for _ in range(times):
  247              self.cmd("sendkey " + key, settle=0.1)
  248              time.sleep(gap)
  249  
  250      def screendump(self, path, settle=0.3):
  251          # QEMU writes the file itself, so give it an absolute host path and
  252          # wait for it to appear rather than assuming it is instant. Remove
  253          # any previous file first: "it exists" is the only signal we have
  254          # that the dump landed, and a leftover from the last capture
  255          # answers that question with a stale frame.
  256          #
  257          # Under a GL scanout (a guest launched with virgl, fork #291) the
  258          # monitor answers "Error: no surface": the frame is a texture the
  259          # console never reads back. QEMU's VNC server does read it back for
  260          # a client, so the frame is taken over VNC instead -- the server the
  261          # monitor names in `info vnc` -- and written as the same P6 file.
  262          # Once seen, VNC is used for the rest of the session.
  263          try:
  264              os.remove(path)
  265          except OSError:
  266              pass
  267          if getattr(self, "_vnc", None):
  268              return self._vnc_screendump(path)
  269          answer = self.cmd("screendump " + path, settle=settle)
  270          if "no surface" in answer:
  271              return self._vnc_screendump(path)
  272          for _ in range(60):
  273              if os.path.exists(path) and os.path.getsize(path) > 0:
  274                  size = -1
  275                  # Wait for the size to stop changing; a partially written
  276                  # PPM decodes as a torn frame and wastes a review cycle.
  277                  while size != os.path.getsize(path):
  278                      size = os.path.getsize(path)
  279                      time.sleep(0.05)
  280                  return True
  281              time.sleep(0.05)
  282          return False
  283  
  284      def _vnc_endpoint(self):
  285          """(host, port) of the VNC server this QEMU runs, from `info vnc`."""
  286          answer = self.cmd("info vnc", settle=0.4)
  287          m = re.search(r"Server:\s+([0-9.]+):(\d+)", answer)
  288          if not m:
  289              return None
  290          return m.group(1), int(m.group(2))
  291  
  292      def _vnc_screendump(self, path):
  293          if getattr(self, "_vnc", None) is None:
  294              self._vnc = self._vnc_endpoint()
  295              if self._vnc is None:
  296                  return False
  297          try:
  298              w, h, rgb = vnc_frame(self._vnc[0], self._vnc[1])
  299          except (OSError, ValueError):
  300              return False
  301          with open(path, "wb") as fh:
  302              fh.write(b"P6\n%d %d\n255\n" % (w, h))
  303              fh.write(rgb)
  304          return True
  305  
  306      def frame(self):
  307          """The current framebuffer as bytes, or None if it did not arrive.
  308  
  309          For comparison only - `shot` keeps its own file. One scratch path is
  310          reused, so polling a screen for several seconds costs one file."""
  311          if self._scratch is None:
  312              self._scratch = os.path.join(
  313                  tempfile.mkdtemp(prefix="vm-visual-qa-"), "frame.ppm")
  314          if not self.screendump(self._scratch, settle=0.15):
  315              return None
  316          try:
  317              with open(self._scratch, "rb") as fh:
  318                  return fh.read()
  319          except OSError:
  320              return None
  321  
  322      def close(self):
  323          try:
  324              self.sock.close()
  325          except OSError:
  326              pass
  327          if self._scratch:
  328              try:
  329                  os.remove(self._scratch)
  330                  os.rmdir(os.path.dirname(self._scratch))
  331              except OSError:
  332                  pass
  333  
  334  
  335  def frame_diff(a, b):
  336      """How much two framebuffers differ, as a fraction of their bytes.
  337  
  338      A missing frame, or a resolution change, counts as completely
  339      different. The XOR goes through one big int so the whole comparison
  340      happens in C: a 640x480 pair takes about 2 ms, which matters when a
  341      settle polls a screen thirty times."""
  342      if a is None or b is None or len(a) != len(b) or not a:
  343          return 1.0
  344      if a == b:
  345          return 0.0
  346      x = (int.from_bytes(a, "big") ^ int.from_bytes(b, "big")).to_bytes(len(a), "big")
  347      return (len(x) - x.count(0)) / float(len(x))
  348  
  349  
  350  def settle(frame_fn, timeout=SETTLE_TIMEOUT, quiet=SETTLE_QUIET, poll=POLL):
  351      """Wait until the screen has held still for `quiet` seconds.
  352  
  353      Returns (ok, seconds). ok is False when the bound was reached with the
  354      screen still moving - a spinner, a running transfer's elapsed time -
  355      which is information, not a failure."""
  356      t0 = time.time()
  357      last = frame_fn()
  358      quiet_since = time.time()
  359      while time.time() - t0 < timeout:
  360          time.sleep(poll)
  361          cur = frame_fn()
  362          if frame_diff(cur, last) > SAME_MAX:
  363              quiet_since = time.time()
  364          last = cur
  365          if time.time() - quiet_since >= quiet:
  366              return True, time.time() - t0
  367      return False, time.time() - t0
  368  
  369  
  370  def wait_for_change(frame_fn, before, timeout=CHANGE_TIMEOUT, poll=POLL):
  371      """Wait until the screen differs from `before`. Returns (ok, seconds)."""
  372      t0 = time.time()
  373      while True:
  374          if frame_diff(frame_fn(), before) >= CHANGED_MIN:
  375              return True, time.time() - t0
  376          if time.time() - t0 >= timeout:
  377              return False, time.time() - t0
  378          time.sleep(poll)
  379  
  380  
  381  def dismiss_dialogs(frame_fn, sendkey_fn, key="z", limit=8, quiet=0.8, timeout=8.0):
  382      """Press B until nothing is open, ending on the system carousel.
  383  
  384      B closes a dialog, a menu or a game list; on the carousel it opens GO
  385      TO instead, so B alone never reaches a fixed point and a walk that
  386      presses it a fixed number of times ends on a dialog whenever it
  387      guessed the depth wrong (reset.steps did, for any odd number of open
  388      screens). What it does reach is a two-state cycle: carousel, GO TO,
  389      carousel. So press, settle, and stop the moment the screen matches a
  390      screen we have already stood on - that repeat is the carousel, with
  391      the cycle's dialog closed behind us.
  392  
  393      A press that changes nothing at all was eaten rather than obeyed, so it
  394      is re-sent instead of being read as the cycle. Returns how many presses
  395      moved the screen (the last of them is GO TO opening, not a close)."""
  396      settle(frame_fn, timeout=timeout, quiet=quiet)
  397      seen = [frame_fn()]
  398      closed = 0
  399      eaten = 0
  400      for _ in range(limit):
  401          sendkey_fn(key)
  402          settle(frame_fn, timeout=timeout, quiet=quiet)
  403          cur = frame_fn()
  404          if frame_diff(cur, seen[-1]) <= SAME_MAX:
  405              eaten += 1
  406              if eaten > 2:
  407                  return closed              # B does nothing here; stop pressing
  408              continue
  409          eaten = 0
  410          if any(frame_diff(cur, s) <= SAME_MAX for s in seen[:-1]):
  411              return closed                  # back on a screen we have had: the carousel
  412          seen.append(cur)
  413          closed += 1
  414      return closed
  415  
  416  
  417  def to_png(ppm_path, png_path):
  418      """PPM (P6) -> PNG. Pillow if present; otherwise the stdlib, because a
  419      frame nobody can open is a frame nobody reads -- the build host has no
  420      Pillow and the reviewers (people and image models) read PNG."""
  421      try:
  422          from PIL import Image
  423      except ImportError:
  424          return _ppm_to_png_stdlib(ppm_path, png_path)
  425      with Image.open(ppm_path) as im:
  426          im.convert("RGB").save(png_path)
  427      return True
  428  
  429  
  430  def _ppm_to_png_stdlib(ppm_path, png_path):
  431      import struct
  432      import zlib
  433  
  434      data = open(ppm_path, "rb").read()
  435      fields, pos = [], 0
  436      while len(fields) < 4:                      # P6 <width> <height> <maxval>
  437          while data[pos:pos + 1].isspace():
  438              pos += 1
  439          if data[pos:pos + 1] == b"#":
  440              while data[pos:pos + 1] not in (b"\n", b""):
  441                  pos += 1
  442              continue
  443          start = pos
  444          while not data[pos:pos + 1].isspace():
  445              pos += 1
  446          fields.append(data[start:pos])
  447      pos += 1
  448      if fields[0] != b"P6" or int(fields[3]) != 255:
  449          return False
  450      w, h = int(fields[1]), int(fields[2])
  451      px = data[pos:pos + w * h * 3]
  452      raw = b"".join(b"\x00" + px[y * w * 3:(y + 1) * w * 3] for y in range(h))
  453  
  454      def chunk(kind, body):
  455          return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)
  456  
  457      png = b"\x89PNG\r\n\x1a\n"
  458      png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
  459      png += chunk(b"IDAT", zlib.compress(raw, 6))
  460      png += chunk(b"IEND", b"")
  461      with open(png_path, "wb") as fh:
  462          fh.write(png)
  463      return True
  464  
  465  
  466  def to_gif(png_paths, gif_path, ms_per_frame=1200, scale=0.5):
  467      try:
  468          from PIL import Image
  469      except ImportError:
  470          return False
  471      frames = []
  472      for p in png_paths:
  473          im = Image.open(p).convert("RGB")
  474          if scale != 1:
  475              im = im.resize((int(im.width * scale), int(im.height * scale)))
  476          frames.append(im)
  477      if not frames:
  478          return False
  479      frames[0].save(
  480          gif_path,
  481          save_all=True,
  482          append_images=frames[1:],
  483          duration=ms_per_frame,
  484          loop=0,
  485          optimize=True,
  486      )
  487      return True
  488  
  489  
  490  class WalkFailed(Exception):
  491      """A step could not be satisfied, so every step after it would run
  492      against the wrong screen."""
  493  
  494  
  495  def parse_steps(lines):
  496      """[(lineno, verb, rest)] from a step file's lines."""
  497      out = []
  498      for n, raw in enumerate(lines, 1):
  499          line = raw.split("#", 1)[0].strip()
  500          if not line:
  501              continue
  502          verb, _, rest = line.partition(" ")
  503          out.append((n, verb, rest.strip()))
  504      return out
  505  
  506  
  507  def _floats(rest, *defaults):
  508      """The step's numeric arguments, each defaulted."""
  509      got = rest.split()
  510      return [float(got[i]) if i < len(got) else d for i, d in enumerate(defaults)]
  511  
  512  
  513  def run_steps(mon, steps, outdir):
  514      os.makedirs(outdir, exist_ok=True)
  515      parsed = parse_steps(steps) if not steps or isinstance(steps[0], str) else steps
  516      # Capturing the pre-press frame costs a screendump per key, so only do
  517      # it for a file that asks: an old step file must cost what it used to.
  518      tracking = any(v == "wait-for-change" for _, v, _ in parsed)
  519      shots = []
  520      index = 0
  521      before = None            # the frame taken just before the last key step
  522      last_key = None          # (lineno, keyname, times)
  523  
  524      def shot(label):
  525          nonlocal index
  526          index += 1
  527          label = re.sub(r"[^a-zA-Z0-9_-]+", "-", label or "frame").strip("-")
  528          base = os.path.join(outdir, "%02d-%s" % (index, label))
  529          ppm = base + ".ppm"
  530          if not mon.screendump(ppm):
  531              print("WARN: no frame captured for " + label, file=sys.stderr)
  532              return None
  533          png = base + ".png"
  534          if to_png(ppm, png):
  535              os.remove(ppm)
  536              shots.append(png)
  537              print("captured " + png)
  538              return png
  539          shots.append(ppm)
  540          print("captured " + ppm + " (PPM: the frame was not a P6/255 image)")
  541          return ppm
  542  
  543      for lineno, verb, rest in parsed:
  544          if verb == "key":
  545              m = re.match(r"^(\S+)(?:\s+x(\d+))?$", rest)
  546              if not m:
  547                  raise SystemExit("bad key step on line %d: %s" % (lineno, rest))
  548              name, times = m.group(1), int(m.group(2) or 1)
  549              if tracking:
  550                  # The pre-press frame has to come from a screen that has
  551                  # STOPPED moving, or the tail of the last transition
  552                  # satisfies this press's wait-for-change and an eaten key
  553                  # reads as a landed one. That is not hypothetical: on
  554                  # 2026-09-11 an A press on the ROMS AND BIOS switch was
  555                  # eaten, the row highlight from the `down` before it was
  556                  # still fading, and the walk carried on with the switch
  557                  # off - which is the exact failure #125 exists to catch,
  558                  # reproduced by the mechanism meant to catch it.
  559                  settle(mon.frame, timeout=PRE_KEY_TIMEOUT, quiet=PRE_KEY_QUIET)
  560                  before = mon.frame()
  561              last_key = (lineno, name, times)
  562              mon.sendkey(name, times)
  563  
  564          elif verb == "wait":
  565              time.sleep(float(rest))
  566  
  567          elif verb == "settle":
  568              timeout, quiet = _floats(rest, SETTLE_TIMEOUT, SETTLE_QUIET)
  569              ok, took = settle(mon.frame, timeout=timeout, quiet=quiet)
  570              print("settle: %s after %.1fs" % ("still" if ok else "still moving at the bound", took))
  571  
  572          elif verb == "wait-for-change":
  573              if last_key is None:
  574                  raise SystemExit("wait-for-change on line %d has no key step before it" % lineno)
  575              timeout, retries = _floats(rest, CHANGE_TIMEOUT, CHANGE_RETRIES)
  576              kline, kname, ktimes = last_key
  577              ok, took = wait_for_change(mon.frame, before, timeout=timeout)
  578              tries = 0
  579              while not ok and tries < int(retries):
  580                  tries += 1
  581                  print("wait-for-change: `key %s` (line %d) was eaten after %.1fs; re-sending (%d)"
  582                        % (kname, kline, took, tries), file=sys.stderr)
  583                  mon.sendkey(kname, ktimes)
  584                  ok, took = wait_for_change(mon.frame, before, timeout=timeout)
  585              if not ok:
  586                  shot("stuck-after-%s" % kname)
  587                  raise WalkFailed(
  588                      "wait-for-change (line %d): the screen did not change within %.0fs of `key %s`"
  589                      " on line %d, even after %d re-send(s). The press was eaten, so every step after"
  590                      " this one would run against the wrong screen. The frame is the last one in %s."
  591                      % (lineno, timeout, kname, kline, int(retries), outdir))
  592              print("changed after %.1fs (`key %s`, line %d%s)"
  593                    % (took, kname, kline, ", re-sent" if tries else ""))
  594  
  595          elif verb == "wake":
  596              # `shift` is a key EmulationStation ignores, so it wakes the
  597              # screensaver without spending a press the walk needed.
  598              mon.sendkey("shift")
  599              settle(mon.frame, timeout=_floats(rest, 8.0)[0], quiet=0.8)
  600  
  601          elif verb == "dismiss-dialogs":
  602              limit = int(_floats(rest, 8)[0])
  603              closed = dismiss_dialogs(mon.frame, mon.sendkey, limit=limit)
  604              print("dismiss-dialogs: %d press(es) moved the screen, back on the carousel" % closed)
  605  
  606          elif verb == "shot":
  607              shot(rest)
  608  
  609          else:
  610              raise SystemExit("unknown step on line %d: %s %s" % (lineno, verb, rest))
  611      return shots
  612  
  613  
  614  def main():
  615      ap = argparse.ArgumentParser(
  616          description="Drive a headless GENERIC_X64 guest through a UI walk and keep the frames.",
  617          epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  618      ap.add_argument("--monitor", required=True, help="QEMU monitor unix socket")
  619      sub = ap.add_subparsers(dest="command", required=True)
  620  
  621      r = sub.add_parser("run", help="run a step file and capture frames")
  622      r.add_argument("steps", help="step file, or - for stdin")
  623      r.add_argument("--outdir", default="vm-shots")
  624      r.add_argument("--gif", help="also write an animated GIF of the frames")
  625  
  626      s = sub.add_parser("shot", help="capture a single frame")
  627      s.add_argument("output", help="output .png (or .ppm)")
  628  
  629      k = sub.add_parser("key", help="send one key")
  630      k.add_argument("keyname")
  631      k.add_argument("--times", type=int, default=1)
  632  
  633      st = sub.add_parser("settle", help="wait until the screen stops changing")
  634      st.add_argument("--timeout", type=float, default=SETTLE_TIMEOUT)
  635      st.add_argument("--quiet", type=float, default=SETTLE_QUIET)
  636  
  637      sub.add_parser("dismiss", help="close whatever is open, ending on the carousel")
  638  
  639      args = ap.parse_args()
  640      mon = Monitor(args.monitor)
  641      try:
  642          if args.command == "run":
  643              src = sys.stdin if args.steps == "-" else open(args.steps)
  644              with src as fh:
  645                  shots = run_steps(mon, fh.readlines(), args.outdir)
  646              if args.gif and shots:
  647                  if to_gif(shots, args.gif):
  648                      print("wrote " + args.gif)
  649                  else:
  650                      print("GIF needs Pillow; frames are in " + args.outdir)
  651          elif args.command == "shot":
  652              ppm = args.output
  653              if ppm.endswith(".png"):
  654                  ppm = ppm[:-4] + ".ppm"
  655              if not mon.screendump(os.path.abspath(ppm)):
  656                  raise SystemExit("no frame captured")
  657              if args.output.endswith(".png") and to_png(ppm, args.output):
  658                  os.remove(ppm)
  659              print("captured " + args.output)
  660          elif args.command == "key":
  661              mon.sendkey(args.keyname, args.times)
  662          elif args.command == "settle":
  663              ok, took = settle(mon.frame, timeout=args.timeout, quiet=args.quiet)
  664              print("settle: %s after %.1fs" % ("still" if ok else "still moving at the bound", took))
  665          elif args.command == "dismiss":
  666              mon.sendkey("shift")
  667              print("%d press(es) moved the screen, back on the carousel"
  668                    % dismiss_dialogs(mon.frame, mon.sendkey))
  669      except WalkFailed as exc:
  670          print("WALK FAILED: %s" % exc, file=sys.stderr)
  671          raise SystemExit(3)
  672      finally:
  673          mon.close()
  674  
  675  
  676  if __name__ == "__main__":
  677      main()
  678  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/README.md

```
    1  # VM walks
    2  
    3  Step files for `tools/vm-visual-qa run`, one per screen worth reaching, so a
    4  QA cycle replays a walk instead of rediscovering the keys.
    5  
    6  ```bash
    7  W=tools/vm-walks
    8  cat $W/reset.steps $W/to-manage-cloud-storage.steps $W/back-up-page.steps \
    9      $W/tick-roms.steps $W/continue-to-systems.steps $W/run-transfer.steps \
   10    | tools/vm-visual-qa --monitor /tmp/rocknix-qemu-monitor.sock run - --outdir shots/
   11  ```
   12  
   13  ## The steps wait for the screen, not for the clock
   14  
   15  Every file here is written on `settle` and `wait-for-change` rather than
   16  `wait N`. The reason is in fork #125: a step file made of fixed delays is a
   17  guess about a machine that is also building an image, and a press one second
   18  after a screen change is regularly eaten. The walk then runs its whole
   19  remainder one screen out of phase -- a switch that did not toggle, a game
   20  list that did not launch, a `LATER` that landed on the wrong row and typed
   21  into a Wi-Fi password field. Three derails on 2026-09-10, two on 2026-09-11.
   22  
   23  - `settle [timeout_s] [quiet_s]` waits until the frame has held still, and
   24    never fails a walk: a page that is still scanning simply runs to the
   25    bound. Use it before a `shot`, and after anything that loads or transfers.
   26  - `wait-for-change [timeout_s] [retries]` waits until the frame differs from
   27    the one taken before the last `key`. An eaten press is re-sent once by
   28    default and then **fails the walk**, naming the key and the line, instead
   29    of letting every later step run against the wrong screen.
   30  - `wake` spends the screensaver's free press on a key EmulationStation
   31    ignores.
   32  - `dismiss-dialogs` closes whatever is open and ends on the carousel.
   33  
   34  `tools/vm-visual-qa --help` is the reference for all of them, including the
   35  frame-comparison thresholds and how they were measured. The two places a
   36  fixed `wait` is still right are a deliberate sampler
   37  (`run-transfer-frames.steps` wants a frame at a known offset, not a frame
   38  when the page stops moving) and a pause where nothing on screen will change.
   39  
   40  ## Where a walk starts
   41  
   42  The deterministic start is a **rebooted VM**: it comes up on the carousel,
   43  awake, with nothing open. `reset.steps` reaches the same state from wherever
   44  the interface happens to be, and is what to compose in front of a walk that
   45  follows another in the same session.
   46  
   47  A reboot is not a clean slate, though. The transfer pages' four class
   48  switches are saved as `cloudsync.pick.<direction>.<class>` in
   49  **`/storage/.config/system/configs/system.cfg`** when the page closes, and
   50  restored at the next start -- so a `tick-*` walk, which flips rather than
   51  sets, goes the wrong way after any earlier walk left one on. `suite.txt`'s
   52  `default-pre` resets them; a hand-composed walk should do the same:
   53  
   54  ```bash
   55  tools/vm-pair ssh b '. /etc/profile; for d in backup restore; do \
   56    for k in content media settings; do set_setting cloudsync.pick.$d.$k 0; done; \
   57    set_setting cloudsync.pick.$d.saves 1; done'
   58  ```
   59  
   60  (That path is not the `/storage/.config/system.cfg` the rest of the harness
   61  names, and a value written to it while ES is running does survive the
   62  reboot.)
   63  
   64  `reset.steps` used to be four B presses and now calls `dismiss-dialogs`,
   65  because four is a guess: B closes a dialog, a menu or a game list, but on
   66  the carousel it *opens* GO TO, so a fixed count lands on the carousel from
   67  an even depth and on a dialog from an odd one. `wake.steps` remains for a
   68  composition that needs only the wake; `reset.steps` wakes first itself.
   69  
   70  A **restarted** EmulationStation (`systemctl restart emustation`) is not a
   71  rebooted one: it restores the game list that was open, so a walk that
   72  assumes the carousel starts one screen deep and its `x` presses launch
   73  whatever is under the cursor (the File Manager, 2026-09-09). `screendump`
   74  can also serve the previous ES's frame for half a minute afterwards. Reboot.
   75  
   76  ## The suite
   77  
   78  `suite.txt` lists the compositions `tools/vm-qa --only walks` replays, one
   79  per line, each from a rebooted guest. It exists because most files here are
   80  a *leg* -- `back-up-page.steps` starts on the CLOUD hub, `run-transfer.steps`
   81  on the systems page -- and the runner used to replay each file on its own,
   82  so nine of them pressed A into the carousel and drove whatever game list was
   83  under the cursor. The frames were counted and the suite passed.
   84  
   85  `tools/vm-qa --skip-up --only walks --guest b` runs it against vm-pair's
   86  second guest, which is how it runs while another session holds guest a.
   87  
   88  ## What each file expects
   89  
   90  Every file states where it starts and where it leaves the focus, because the
   91  next file depends on it. Read the file; the notes below are only the ones
   92  that span files.
   93  
   94  - `to-change-cloud-folder.steps` reaches CLOUD FOLDERS, then opens its
   95    initially selected SAVES FOLDER row. `confirm-cloud-folder.steps` presses
   96    START once on that unchanged value, returns to CLOUD FOLDERS, and uses B
   97    to return to the hub. The unchanged value is a no-op on every provider,
   98    including MinIO; it no longer runs the old #78 provider probe. The suite
   99    compares configuration, selected paths, and local/cloud file witnesses
  100    before and after these walks (#527). Actual path changes/refusals have
  101    separate CF05 evidence in the canonical cloud-folder flow review.
  102    The hub still takes seven downs from BACK UP TO THE CLOUD; inspect the
  103    focused-row frame before trusting the count.
  104  - `ui-settings-toggle.steps` ends on USER INTERFACE SETTINGS with its last
  105    row -- SHOW RETROACHIEVEMENTS ICON, a Settings-backed switch -- toggled and
  106    focused; the next B closes the page and runs both settings writers
  107    (es_settings.cfg and system.cfg). It is the walk
  108    `tools/cloud-round-trip --only KILL13` drives before its power cuts, and
  109    that harness reads the file itself, so a changed row is fixed in one
  110    place. The toggle must stay the file's last `key x`: KILL13 truncates
  111    there for the trial that changes nothing. Frame-verified 2026-09-10 at
  112    1280x800 and 2026-09-11 at 640x480.
  113  - `match-dialog.steps` runs the third action from the hub -- MATCH THIS
  114    DEVICE TO THE CLOUD -- through its confirmation to its done page. It needs
  115    the seed fixture (`cloud-test-backend seed-content` + `seed-device`) so the
  116    device holds ROMs the cloud does not, and it must run **before** the
  117    transfer walks, which upload exactly those: after them it reaches THIS
  118    DEVICE ALREADY MATCHES YOUR CLOUD. THERE IS NOTHING TO REMOVE. `suite.txt`
  119    orders it accordingly.
  120  - The transfer flow is: hub -> transfer page (four class switches) ->
  121    CONTINUE (shown once ROMS AND BIOS or GAME CONTENT is on) -> the systems
  122    page -> BACK UP / RESTORE -> the transfer page -> PRESS ANY BUTTON TO
  123    CLOSE -> hub. The systems page's bar is BACK / SELECT ALL / BACK UP (or
  124    RESTORE), so from BACK the verb is two rights away, not one. The `tick-*`
  125    walks *flip* a switch rather than set it, which is deterministic only from
  126    a rebooted guest; read the frame.
  127  - `run-transfer.steps` presses SELECT ALL and then the verb, and **needs no
  128    system ticked when it starts**. The verb runs whatever the picker last
  129    saved to `/storage/.cache/cloud_sync/content-systems` -- saved on every
  130    close, BACK included, and kept across a reboot -- and with nothing ticked
  131    `cloud_content_backup --selected` exits 1
  132    before any rclone runs, so the page ends FAILED with rows 3-4 blank and
  133    the walk has exercised no transfer. SELECT ALL is a toggle that reads
  134    SELECT NONE once everything is on, so on a VM where an earlier walk
  135    already saved SELECT ALL the same press clears the selection and fails the
  136    same way. Empty it over SSH or serial before the composition,
  137    `cloud_content_restore --set-systems ""` (a fresh image has none), and
  138    read the `selected-all` frame -- every switch on, the button reading
  139    SELECT NONE -- before trusting the frames after it.
  140  
  141  What the keys mean is in `.claude/rules/generic-x64-vm-testing.md`
  142  § "Driving EmulationStation" and in `tools/vm-visual-qa --help`; the short
  143  version: `ret` is START, `x` is A, `z` is B, `shift` is the wake key, and
  144  `up` from a page's first row lands on its BACK button before it wraps to the
  145  last row.
  146  
  147  When a walk stops matching the interface (a row moved, a page was renamed),
  148  fix the walk in the same change as the interface -- a walk that no longer
  149  reaches its screen is the first thing the next cycle finds, and the
  150  cheapest. Since #125 it is also the first thing the *walk* finds: the run
  151  fails on the press that stopped landing, rather than four frames later.
  152  
  153  ## How a walk leaves a game
  154  
  155  Through the exit hotkey's own path: `execute_kill` from the image's
  156  `input_sense`, which touches the marker and stops RetroArch the way SELECT +
  157  START does on a handheld (`tools/emulator-exit-test` and `tools/time-to-play`
  158  quit the same way). Never through RetroArch's own exit -- Esc twice, or its
  159  menu's Quit. On the GENERIC_X64 guest that path leaves the screen black with
  160  EmulationStation alive (#239, seen three times on 2026-09-21), and a walk that
  161  takes it captures nothing afterwards. The guest is the only place it happens:
  162  ES's `HideWindow` defaults to false on x86, so ES keeps its window and GL
  163  context while a game runs and only raises it afterwards, where a handheld
  164  tears the renderer down and up (`Settings.cpp:366-370`, `Window.cpp:120-127`);
  165  that is the lead #239 works from, and until it is run down the hotkey's path
  166  is the one a walk may use.
  167  
  168  ## The frames are compared, not only counted
  169  
  170  Since #252 the `frame-diff` suite in `tools/vm-qa` diffs every frame a walk
  171  leaves against the same frame from the last cut accepted on a device
  172  (`walk-baseline/` beside the run directories; `tools/frame-diff` is the
  173  tool). Two files here steer it:
  174  
  175  - `masks.txt` -- rectangles it does not compare, one per line with the
  176    reason: the clock, a transfer's live lines. Measured, not guessed: a diff
  177    of two runs of near-identical cuts showed the clock and nothing else on
  178    61 of 63 frames.
  179  - `claims.txt` -- what a cut means to change: `<baseline-build> <screen-glob>
  180    x0 y0 x1 y1 <issue> <what>`. A box outside every claim fails the suite. A
  181    claim is written against a baseline build and goes stale when the baseline
  182    moves; the run says which ones to prune.
  183  
  184  The `manager-*` lines are the first walks added for it: the SAVE STATE
  185  MANAGER on a NES game with a turn recorded, a Game Boy game as it is, and an
  186  FBNeo game the core's table turns, over the pictures in `fixtures/` (a ring
  187  that is round only at the right aspect, a green mark on the edge that is the
  188  game's top), seeded by vm-qa with fixed mtimes so the tile dates never
  189  differ. Their frames are the ones to read for #243, #245, #248 and #250.
  190  
  191  Because the frames are compared, `default-pre` fixes everything a walked
  192  screen shows that an earlier suite could leave behind: the hub's two sync
  193  switches off and their stamps gone, the transfer picks reset, `StartupSystem`
  194  cleared. A run that only walks and a full run then frame the same screens.
  195  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/back-up-page.steps

```
    1  # Start: the CLOUD hub, focus on BACK UP TO THE CLOUD. End: BACK UP TO THE
    2  # CLOUD, focus on SAVES (its first row). Rows: SAVES, ROMS AND BIOS, GAME
    3  # CONTENT, SETTINGS; the ticks are remembered per direction, so what is on
    4  # depends on the last visit (defaults on a fresh image: SAVES on, the rest off).
    5  key x
    6  wait-for-change
    7  settle
    8  shot back-up-page
    9  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/claims.txt

```
    1  # What a cut means to change on the walked screens, one box per line:
    2  #   <baseline-build|*> <screen-glob> x0 y0 x1 y1 <issue>  # what
    3  # tools/frame-diff holds every differing box against these; a box no line
    4  # contains fails the frame-diff suite. A claim names the baseline it was
    5  # written against (the build in walk-baseline/BASELINE.txt), so it goes
    6  # stale -- and is reported as such -- when the baseline moves; prune it
    7  # then. A whole-frame rectangle claims a walk the baseline has not seen.
    8  
    9  # The #307 fix build (4234be0b6b, vm-qa run 68), against the d72084ccad baseline:
   10  d72084ccad confirm-cloud-folder/02-hub-change-folder-row.png 240 545 1040 575 #308  # CHANGE CLOUD FOLDER's line is YOUR SAVES ARE IN: <folder> -- one line under the row (ES 39d5a9d6d, 8-es claude F-ES-14, D-UI-023)
   11  d72084ccad to-change-cloud-folder/02-hub-change-folder-row.png 240 545 1040 575 #308  # the same row on the other walk
   12  d72084ccad run-transfer/07-transfer-running.png 400 555 880 580 #308  # the transfer page's footer no longer names a console letter: THIS CAN TAKE A WHILE. (ES 5a7afc4ca, F-RA-14/F-CS-07; es-ui-style-guide Interaction rules)
   13  d72084ccad run-transfer-frames/07-t02.png 400 555 880 580 #308  # the same footer, the frames walk
   14  d72084ccad continue-to-systems/05-systems-page.png 230 470 1050 680 #308  # PICO-8 listed, 1 FILE NOT YET IN YOUR CLOUD: a system whose only file is empty (the 0-byte Splore.png) was read as nothing to move and left out (ES 52ba93160, 8a gpt); the rows below it shift down
   15  d72084ccad run-transfer-frames/05-systems-page.png 230 470 1050 680 #308  # the same page on the frames walk
   16  d72084ccad run-transfer-frames/06-selected-all.png 230 470 1050 680 #308  # the same page, all selected
   17  d72084ccad run-transfer-frames/07-t02.png 670 320 710 345 #308  # ITEM 1 OF 5: the PICO-8 unit counted (same change)
   18  d72084ccad run-transfer-frames/07-t02.png 557 288 723 339 #439  # first observed transfer frame may still say PREPARING... instead of SAVES / ITEM 1 OF 4; actual09 completes24files/640KB at elapsed0:04. The historical t02 name is not a two-second timing assertion; no baseline or general mask changed.
   19  d72084ccad confirm-cloud-folder/04-folder-result.png 240 545 1040 575 #308  # the same row's line on the hub reopened after the folder change (ES 39d5a9d6d); the reopened hub sits on CHANGE CLOUD FOLDER again (ES 4313a8f53, G-E2-O1) so nothing else on the frame differs
   20  
   21  # The cloud epic (#354; 1acdaf2cce, vm-qa run 96), against the d72084ccad baseline:
   22  # (The t05 rectangles were first written as frame-diff printed the box, 565..714 inclusive, which a
   23  # half-open claim of 565 714 does not contain; widened after run 99 caught the same sample, 2026-10-01.)
   24  # Lowercase pixelelated renewal (#409/#415, 2026-10-04); original failed frames retained.
   25  d72084ccad confirm-cloud-folder/03-folder-editor.png 183 226 416 268 #409  # the editor now holds /pixelelated/Saves (D-CLOUD-174); measured lowercase text against the accepted ROCKNIX baseline, #415
   26  d72084ccad confirm-cloud-folder/05-after-dismiss.png 183 226 416 268 #409  # the same lowercase default after reopening the editor, #415
   27  d72084ccad to-change-cloud-folder/03-folder-editor.png 183 226 416 268 #409  # the same lowercase default on the other editor walk, #415
   28  d72084ccad run-transfer-frames/08-t05.png 560 284 720 342 #308  # the run carries PICO-8's files too (26 files, 1.1 MB against 23, 640 KB) and still ends at ELAPSED 0:03 (t08: COMPLETED); the t05 sample can catch ITEM 5 OF 5 a moment before the end
   29  d72084ccad run-transfer-frames/08-t05.png 495 556 788 578 #308  # the same sample: the footer still THIS CAN TAKE A WHILE.
   30  d72084ccad run-transfer-frames/08-t05.png 584 740 696 768 #308  # the same sample: the help bar still CANCEL
   31  d72084ccad run-transfer-frames/08-t05.png 415 412 866 427 #406  # replacement134e89's fixed t05 sample still shows the live files/bytes/rate line; t08 is COMPLETED,24 files/640KB, elapsed0:04. Actual baseline/current frames retained; no renderer change or whole-screen mask.
   32  d72084ccad restore-page/02-restore-page.png 240 460 1040 520 #349  # SETTINGS dimmed, its line NO SETTINGS BACKUP FROM THIS DEVICE YET and no switch: the QA cloud holds no settings backup from this device's label, so the scan offers none (D-CLOUD-162, D-CLOUD-164 string 3); since ES 551c5a762 the row keeps the rows' inset, where 1acdaf2cce..d9493fe339 drew it flush with the panel's edge
   33  
   34  # #455: these historical manager-gb frames actually showed FBNeo after the
   35  # match walk deleted the GB ROMs. The corrected first GB carousel/list/options
   36  # are new coverage; the baseline remains unchanged. The manager's common
   37  # START NEW GAME tile and bottom controls remain outside the claims below.
   38  d72084ccad manager-gb/01-0-carousel.png 0 0 1280 800 #455  # first verified Game Boy carousel, previously FBNeo
   39  d72084ccad manager-gb/02-1-list.png 0 0 1280 800 #455  # first verified Game Boy game list
   40  d72084ccad manager-gb/03-2-game-options.png 0 0 1280 800 #455  # options for Ninoid, previously Ms. Pac-Man
   41  d72084ccad manager-gb/04-3-manager.png 0 0 1280 355 #455  # actual Game Boy background and Ninoid title
   42  d72084ccad manager-gb/04-3-manager.png 260 415 535 735 #455  # unrotated Game Boy thumbnail and its date
   43  d72084ccad manager-gb/05-4-manager-next-tile.png 0 0 1280 355 #455  # same actual system/game backdrop
   44  d72084ccad manager-gb/05-4-manager-next-tile.png 260 415 535 735 #455  # same Game Boy thumbnail, selected
   45  # #455 comparison finding: restoring GB adds its Metroid neighbor panel to
   46  # the NES carousel and its far-right edge to FBNeo. The first scoped diff
   47  # remains failed and retained; direct before/after review confirmed these
   48  # two fixture-composition changes. Main logos and bottom controls stay checked.
   49  d72084ccad manager-nes/01-0-carousel.png 737 0 1280 708 #455  # restored GB neighbor and shifted next panel
   50  d72084ccad manager-fbn/01-0-carousel.png 1249 418 1280 708 #455  # narrow restored GB panel at the right edge
   51  
   52  # #527: reviewed replacement18 independent-folder navigation. Original wrong
   53  # selector/carousel/list captures remain rejected; unchanged values return to
   54  # CLOUD FOLDERS, then B returns to the hub. Eight640 and eight1280 frames,
   55  # before/after payload witnesses and initial unclaimed diffs are retained in
   56  # docs/qa-logs/2026-10-08-cloud-folder-walks/. No baseline or mask changes.
   57  d72084ccad to-change-cloud-folder/02-hub-change-folder-row.png 240 187 1040 640 #544  # #527 CHECK CLOUD FOLDERS/scrolling plus #537 CLOUD CONNECTIONS row and shorter subtitle; exact image19/baseline/prior-hub frames reviewed
   58  d72084ccad to-change-cloud-folder/03-folder-editor.png 552 146 729 192 #527  # SAVES FOLDER title and underlying CLOUD FOLDERS title replace CLOUD FOLDER/CLOUD
   59  d72084ccad to-change-cloud-folder/03-folder-editor.png 236 644 1044 719 #527  # shorter selector behind the keyboard replaces the old hub and its exposed BACK strip
   60  d72084ccad to-change-cloud-folder/*.png 1249 418 1280 708 #527  # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455
   61  d72084ccad confirm-cloud-folder/02-hub-change-folder-row.png 240 187 1040 640 #544  # #527 CHECK CLOUD FOLDERS/scrolling plus #537 CLOUD CONNECTIONS row and shorter subtitle; exact image19/baseline/prior-hub frames reviewed
   62  d72084ccad confirm-cloud-folder/03-folder-editor.png 552 146 729 192 #527  # SAVES FOLDER title and underlying CLOUD FOLDERS title replace CLOUD FOLDER/CLOUD
   63  d72084ccad confirm-cloud-folder/03-folder-editor.png 236 644 1044 719 #527  # shorter selector behind the keyboard replaces the old hub and its exposed BACK strip
   64  d72084ccad confirm-cloud-folder/*.png 1249 418 1280 708 #527  # scoped walk retains the GB fixture; old full run had removed it in MATCH, the same FBNeo neighbor edge documented by #455
   65  d72084ccad confirm-cloud-folder/04-folder-result.png 552 146 729 163 #527  # CLOUD FOLDERS after unchanged submission, rather than old CLOUD hub
   66  d72084ccad confirm-cloud-folder/04-folder-result.png 236 199 1044 719 #527  # three independent path rows and selector height replace the former hub return
   67  d72084ccad confirm-cloud-folder/05-after-dismiss.png 137 116 1143 719 #527  # B now returns to the hub instead of old A reopening the keyboard; exact surfaces reviewed
   68  d72084ccad confirm-cloud-folder/05-after-dismiss.png 274 743 1006 766 #527  # hub CLOSE/BACK/CHOOSE help replaces keyboard editing prompts
   69  
   70  # #544: image19 captures of the approved #538 RESET -> CLEAR label.
   71  # Exact button glyph and re-centered help row only; masks/baseline unchanged.
   72  d72084ccad confirm-cloud-folder/03-folder-editor.png 856 584 935 603 #544  # #538 CLEAR button replaces RESET; callback unchanged
   73  d72084ccad confirm-cloud-folder/03-folder-editor.png 273 743 1008 766 #544  # #538 CLEAR help caption replaces RESET and re-centers the same prompts
   74  d72084ccad to-change-cloud-folder/03-folder-editor.png 856 584 935 603 #544  # #538 CLEAR button replaces RESET; callback unchanged
   75  d72084ccad to-change-cloud-folder/03-folder-editor.png 273 743 1008 766 #544  # #538 CLEAR help caption replaces RESET and re-centers the same prompts
   76  
   77  # PROPOSAL ONLY. Do not use with the current single-box matcher.
   78  # #578 / ES d242000a5957ad8de5288a02fb15b21d7ef04715, composed in 3178b832b.
   79  # Absent collection preferences now enable the intended empty Last Played.
   80  # Its wrapped carousel panel shifts Favorites/Tools behind these exact screens.
   81  # Existing masks/baseline/claims stay unchanged. A strict union-of-claimed-pixels
   82  # matcher is required so neighboring foreground changes do not require enlarging
   83  # these background rectangles. No comparison or acceptance has been run.
   84  # Modal strips exclude all displayed text/controls; max8px include plain rounded
   85  # panel borders. FBN logo band claims only currently changed background runs,
   86  # leaving every unchanged logo pixel checked. NES keeps its title untouched.
   87  
   88  # back-up-page/01-cloud-hub.png
   89  d72084ccad back-up-page/01-cloud-hub.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
   90  d72084ccad back-up-page/01-cloud-hub.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
   91  d72084ccad back-up-page/01-cloud-hub.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
   92  
   93  # back-up-page/02-back-up-page.png
   94  d72084ccad back-up-page/02-back-up-page.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
   95  d72084ccad back-up-page/02-back-up-page.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
   96  d72084ccad back-up-page/02-back-up-page.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
   97  d72084ccad back-up-page/02-back-up-page.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
   98  d72084ccad back-up-page/02-back-up-page.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
   99  
  100  # confirm-cloud-folder/01-cloud-hub.png
  101  d72084ccad confirm-cloud-folder/01-cloud-hub.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  102  d72084ccad confirm-cloud-folder/01-cloud-hub.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  103  d72084ccad confirm-cloud-folder/01-cloud-hub.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  104  
  105  # confirm-cloud-folder/02-hub-change-folder-row.png
  106  d72084ccad confirm-cloud-folder/02-hub-change-folder-row.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  107  d72084ccad confirm-cloud-folder/02-hub-change-folder-row.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  108  d72084ccad confirm-cloud-folder/02-hub-change-folder-row.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  109  
  110  # confirm-cloud-folder/03-folder-editor.png
  111  d72084ccad confirm-cloud-folder/03-folder-editor.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  112  d72084ccad confirm-cloud-folder/03-folder-editor.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  113  d72084ccad confirm-cloud-folder/03-folder-editor.png 0 118 240 156 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  114  d72084ccad confirm-cloud-folder/03-folder-editor.png 0 156 152 157 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  115  d72084ccad confirm-cloud-folder/03-folder-editor.png 0 157 144 643 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  116  d72084ccad confirm-cloud-folder/03-folder-editor.png 0 643 152 644 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  117  d72084ccad confirm-cloud-folder/03-folder-editor.png 0 644 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  118  
  119  # confirm-cloud-folder/04-folder-result.png
  120  d72084ccad confirm-cloud-folder/04-folder-result.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  121  d72084ccad confirm-cloud-folder/04-folder-result.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  122  d72084ccad confirm-cloud-folder/04-folder-result.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  123  
  124  # confirm-cloud-folder/05-after-dismiss.png
  125  d72084ccad confirm-cloud-folder/05-after-dismiss.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  126  d72084ccad confirm-cloud-folder/05-after-dismiss.png 0 116 144 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  127  
  128  # continue-to-systems/01-cloud-hub.png
  129  d72084ccad continue-to-systems/01-cloud-hub.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  130  d72084ccad continue-to-systems/01-cloud-hub.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  131  d72084ccad continue-to-systems/01-cloud-hub.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  132  
  133  # continue-to-systems/02-back-up-page.png
  134  d72084ccad continue-to-systems/02-back-up-page.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  135  d72084ccad continue-to-systems/02-back-up-page.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  136  d72084ccad continue-to-systems/02-back-up-page.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  137  d72084ccad continue-to-systems/02-back-up-page.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  138  d72084ccad continue-to-systems/02-back-up-page.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  139  
  140  # continue-to-systems/03-roms-flipped.png
  141  d72084ccad continue-to-systems/03-roms-flipped.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  142  d72084ccad continue-to-systems/03-roms-flipped.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  143  d72084ccad continue-to-systems/03-roms-flipped.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  144  d72084ccad continue-to-systems/03-roms-flipped.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  145  d72084ccad continue-to-systems/03-roms-flipped.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  146  
  147  # continue-to-systems/04-continue-focused.png
  148  d72084ccad continue-to-systems/04-continue-focused.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  149  d72084ccad continue-to-systems/04-continue-focused.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  150  d72084ccad continue-to-systems/04-continue-focused.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  151  d72084ccad continue-to-systems/04-continue-focused.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  152  d72084ccad continue-to-systems/04-continue-focused.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  153  
  154  # continue-to-systems/05-systems-page.png
  155  d72084ccad continue-to-systems/05-systems-page.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  156  d72084ccad continue-to-systems/05-systems-page.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  157  d72084ccad continue-to-systems/05-systems-page.png 0 118 240 680 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  158  d72084ccad continue-to-systems/05-systems-page.png 0 680 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  159  
  160  # manager-fbn/01-0-carousel.png
  161  d72084ccad manager-fbn/01-0-carousel.png 0 0 552 350 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  162  d72084ccad manager-fbn/01-0-carousel.png 0 350 315 451 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  163  d72084ccad manager-fbn/01-0-carousel.png 0 451 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  164  d72084ccad manager-fbn/01-0-carousel.png 315 350 516 354 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  165  d72084ccad manager-fbn/01-0-carousel.png 315 354 515 357 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  166  d72084ccad manager-fbn/01-0-carousel.png 315 357 320 368 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  167  d72084ccad manager-fbn/01-0-carousel.png 401 357 515 358 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  168  d72084ccad manager-fbn/01-0-carousel.png 407 358 515 359 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  169  d72084ccad manager-fbn/01-0-carousel.png 410 359 515 360 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  170  d72084ccad manager-fbn/01-0-carousel.png 412 360 515 361 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  171  d72084ccad manager-fbn/01-0-carousel.png 413 361 515 362 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  172  d72084ccad manager-fbn/01-0-carousel.png 415 362 515 363 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  173  d72084ccad manager-fbn/01-0-carousel.png 416 363 515 364 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  174  d72084ccad manager-fbn/01-0-carousel.png 417 364 515 365 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  175  d72084ccad manager-fbn/01-0-carousel.png 418 365 514 367 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  176  d72084ccad manager-fbn/01-0-carousel.png 419 367 514 368 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  177  d72084ccad manager-fbn/01-0-carousel.png 315 368 323 369 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  178  d72084ccad manager-fbn/01-0-carousel.png 420 368 514 370 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  179  d72084ccad manager-fbn/01-0-carousel.png 315 369 326 370 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  180  d72084ccad manager-fbn/01-0-carousel.png 315 370 329 371 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  181  d72084ccad manager-fbn/01-0-carousel.png 421 370 514 372 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  182  d72084ccad manager-fbn/01-0-carousel.png 315 371 332 372 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  183  d72084ccad manager-fbn/01-0-carousel.png 315 372 335 373 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  184  d72084ccad manager-fbn/01-0-carousel.png 422 372 514 375 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  185  d72084ccad manager-fbn/01-0-carousel.png 315 373 338 374 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  186  d72084ccad manager-fbn/01-0-carousel.png 315 374 340 375 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  187  d72084ccad manager-fbn/01-0-carousel.png 315 375 343 376 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  188  d72084ccad manager-fbn/01-0-carousel.png 423 375 513 379 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  189  d72084ccad manager-fbn/01-0-carousel.png 315 376 346 377 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  190  d72084ccad manager-fbn/01-0-carousel.png 315 377 349 378 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  191  d72084ccad manager-fbn/01-0-carousel.png 315 378 352 379 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  192  d72084ccad manager-fbn/01-0-carousel.png 315 379 355 380 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  193  d72084ccad manager-fbn/01-0-carousel.png 423 379 449 391 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  194  d72084ccad manager-fbn/01-0-carousel.png 479 379 487 387 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  195  d72084ccad manager-fbn/01-0-carousel.png 495 379 505 420 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  196  d72084ccad manager-fbn/01-0-carousel.png 315 380 357 381 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  197  d72084ccad manager-fbn/01-0-carousel.png 315 381 360 382 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  198  d72084ccad manager-fbn/01-0-carousel.png 315 382 363 383 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  199  d72084ccad manager-fbn/01-0-carousel.png 315 383 366 384 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  200  d72084ccad manager-fbn/01-0-carousel.png 315 384 355 424 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  201  d72084ccad manager-fbn/01-0-carousel.png 357 384 369 385 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  202  d72084ccad manager-fbn/01-0-carousel.png 360 385 372 386 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  203  d72084ccad manager-fbn/01-0-carousel.png 363 386 374 387 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  204  d72084ccad manager-fbn/01-0-carousel.png 365 387 377 388 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  205  d72084ccad manager-fbn/01-0-carousel.png 457 387 487 396 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  206  d72084ccad manager-fbn/01-0-carousel.png 368 388 380 389 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  207  d72084ccad manager-fbn/01-0-carousel.png 371 389 383 390 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  208  d72084ccad manager-fbn/01-0-carousel.png 374 390 386 391 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  209  d72084ccad manager-fbn/01-0-carousel.png 377 391 449 392 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  210  d72084ccad manager-fbn/01-0-carousel.png 380 392 449 393 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  211  d72084ccad manager-fbn/01-0-carousel.png 382 393 449 394 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  212  d72084ccad manager-fbn/01-0-carousel.png 382 394 386 415 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  213  d72084ccad manager-fbn/01-0-carousel.png 423 394 449 415 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  214  d72084ccad manager-fbn/01-0-carousel.png 477 396 487 404 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  215  d72084ccad manager-fbn/01-0-carousel.png 457 404 487 420 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  216  d72084ccad manager-fbn/01-0-carousel.png 382 415 449 419 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  217  d72084ccad manager-fbn/01-0-carousel.png 392 419 449 420 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  218  d72084ccad manager-fbn/01-0-carousel.png 392 420 509 421 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  219  d72084ccad manager-fbn/01-0-carousel.png 392 421 508 432 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  220  d72084ccad manager-fbn/01-0-carousel.png 315 424 354 425 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  221  d72084ccad manager-fbn/01-0-carousel.png 315 425 351 426 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  222  d72084ccad manager-fbn/01-0-carousel.png 315 426 349 427 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  223  d72084ccad manager-fbn/01-0-carousel.png 315 427 346 428 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  224  d72084ccad manager-fbn/01-0-carousel.png 315 428 343 429 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  225  d72084ccad manager-fbn/01-0-carousel.png 315 429 342 442 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  226  d72084ccad manager-fbn/01-0-carousel.png 392 432 507 442 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  227  d72084ccad manager-fbn/01-0-carousel.png 315 442 506 451 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  228  
  229  # manager-nes/01-0-carousel.png
  230  d72084ccad manager-nes/01-0-carousel.png 0 0 40 382 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  231  
  232  # match-dialog/01-cloud-hub.png
  233  d72084ccad match-dialog/01-cloud-hub.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  234  d72084ccad match-dialog/01-cloud-hub.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  235  d72084ccad match-dialog/01-cloud-hub.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  236  
  237  # match-dialog/02-cloud-hub-match-row.png
  238  d72084ccad match-dialog/02-cloud-hub-match-row.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  239  d72084ccad match-dialog/02-cloud-hub-match-row.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  240  d72084ccad match-dialog/02-cloud-hub-match-row.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  241  
  242  # match-dialog/03-match-confirm.png
  243  d72084ccad match-dialog/03-match-confirm.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  244  d72084ccad match-dialog/03-match-confirm.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  245  d72084ccad match-dialog/03-match-confirm.png 0 118 240 164 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  246  d72084ccad match-dialog/03-match-confirm.png 0 164 128 165 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  247  d72084ccad match-dialog/03-match-confirm.png 0 165 120 172 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  248  d72084ccad match-dialog/03-match-confirm.png 0 172 112 627 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  249  d72084ccad match-dialog/03-match-confirm.png 0 627 120 636 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  250  d72084ccad match-dialog/03-match-confirm.png 0 636 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  251  
  252  # match-dialog/04-match-done.png
  253  d72084ccad match-dialog/04-match-done.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  254  d72084ccad match-dialog/04-match-done.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  255  d72084ccad match-dialog/04-match-done.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  256  d72084ccad match-dialog/04-match-done.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  257  d72084ccad match-dialog/04-match-done.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  258  
  259  # restore-page/01-cloud-hub.png
  260  d72084ccad restore-page/01-cloud-hub.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  261  d72084ccad restore-page/01-cloud-hub.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  262  d72084ccad restore-page/01-cloud-hub.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  263  
  264  # restore-page/02-restore-page.png
  265  d72084ccad restore-page/02-restore-page.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  266  d72084ccad restore-page/02-restore-page.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  267  d72084ccad restore-page/02-restore-page.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  268  d72084ccad restore-page/02-restore-page.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  269  d72084ccad restore-page/02-restore-page.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  270  
  271  # run-transfer/01-cloud-hub.png
  272  d72084ccad run-transfer/01-cloud-hub.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  273  d72084ccad run-transfer/01-cloud-hub.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  274  d72084ccad run-transfer/01-cloud-hub.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  275  
  276  # run-transfer/02-back-up-page.png
  277  d72084ccad run-transfer/02-back-up-page.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  278  d72084ccad run-transfer/02-back-up-page.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  279  d72084ccad run-transfer/02-back-up-page.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  280  d72084ccad run-transfer/02-back-up-page.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  281  d72084ccad run-transfer/02-back-up-page.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  282  
  283  # run-transfer/03-roms-flipped.png
  284  d72084ccad run-transfer/03-roms-flipped.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  285  d72084ccad run-transfer/03-roms-flipped.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  286  d72084ccad run-transfer/03-roms-flipped.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  287  d72084ccad run-transfer/03-roms-flipped.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  288  d72084ccad run-transfer/03-roms-flipped.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  289  
  290  # run-transfer/04-continue-focused.png
  291  d72084ccad run-transfer/04-continue-focused.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  292  d72084ccad run-transfer/04-continue-focused.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  293  d72084ccad run-transfer/04-continue-focused.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  294  d72084ccad run-transfer/04-continue-focused.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  295  d72084ccad run-transfer/04-continue-focused.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  296  
  297  # run-transfer/05-systems-page.png
  298  d72084ccad run-transfer/05-systems-page.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  299  d72084ccad run-transfer/05-systems-page.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  300  d72084ccad run-transfer/05-systems-page.png 0 118 240 604 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  301  d72084ccad run-transfer/05-systems-page.png 0 604 248 607 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  302  d72084ccad run-transfer/05-systems-page.png 0 607 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  303  
  304  # run-transfer/06-selected-all.png
  305  d72084ccad run-transfer/06-selected-all.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  306  d72084ccad run-transfer/06-selected-all.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  307  d72084ccad run-transfer/06-selected-all.png 0 118 240 604 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  308  d72084ccad run-transfer/06-selected-all.png 0 604 248 607 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  309  d72084ccad run-transfer/06-selected-all.png 0 607 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  310  
  311  # run-transfer/07-transfer-running.png
  312  d72084ccad run-transfer/07-transfer-running.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  313  d72084ccad run-transfer/07-transfer-running.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  314  d72084ccad run-transfer/07-transfer-running.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  315  d72084ccad run-transfer/07-transfer-running.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  316  d72084ccad run-transfer/07-transfer-running.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  317  
  318  # run-transfer/08-transfer-done.png
  319  d72084ccad run-transfer/08-transfer-done.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  320  d72084ccad run-transfer/08-transfer-done.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  321  d72084ccad run-transfer/08-transfer-done.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  322  d72084ccad run-transfer/08-transfer-done.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  323  d72084ccad run-transfer/08-transfer-done.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  324  
  325  # run-transfer-frames/01-cloud-hub.png
  326  d72084ccad run-transfer-frames/01-cloud-hub.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  327  d72084ccad run-transfer-frames/01-cloud-hub.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  328  d72084ccad run-transfer-frames/01-cloud-hub.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  329  
  330  # run-transfer-frames/02-back-up-page.png
  331  d72084ccad run-transfer-frames/02-back-up-page.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  332  d72084ccad run-transfer-frames/02-back-up-page.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  333  d72084ccad run-transfer-frames/02-back-up-page.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  334  d72084ccad run-transfer-frames/02-back-up-page.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  335  d72084ccad run-transfer-frames/02-back-up-page.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  336  
  337  # run-transfer-frames/03-roms-flipped.png
  338  d72084ccad run-transfer-frames/03-roms-flipped.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  339  d72084ccad run-transfer-frames/03-roms-flipped.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  340  d72084ccad run-transfer-frames/03-roms-flipped.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  341  d72084ccad run-transfer-frames/03-roms-flipped.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  342  d72084ccad run-transfer-frames/03-roms-flipped.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  343  
  344  # run-transfer-frames/04-continue-focused.png
  345  d72084ccad run-transfer-frames/04-continue-focused.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  346  d72084ccad run-transfer-frames/04-continue-focused.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  347  d72084ccad run-transfer-frames/04-continue-focused.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  348  d72084ccad run-transfer-frames/04-continue-focused.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  349  d72084ccad run-transfer-frames/04-continue-focused.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  350  
  351  # run-transfer-frames/05-systems-page.png
  352  d72084ccad run-transfer-frames/05-systems-page.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  353  d72084ccad run-transfer-frames/05-systems-page.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  354  d72084ccad run-transfer-frames/05-systems-page.png 0 118 240 680 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  355  d72084ccad run-transfer-frames/05-systems-page.png 0 680 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  356  
  357  # run-transfer-frames/06-selected-all.png
  358  d72084ccad run-transfer-frames/06-selected-all.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  359  d72084ccad run-transfer-frames/06-selected-all.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  360  d72084ccad run-transfer-frames/06-selected-all.png 0 118 240 680 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  361  d72084ccad run-transfer-frames/06-selected-all.png 0 680 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  362  
  363  # run-transfer-frames/07-t02.png
  364  d72084ccad run-transfer-frames/07-t02.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  365  d72084ccad run-transfer-frames/07-t02.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  366  d72084ccad run-transfer-frames/07-t02.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  367  d72084ccad run-transfer-frames/07-t02.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  368  d72084ccad run-transfer-frames/07-t02.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  369  
  370  # run-transfer-frames/08-t05.png
  371  d72084ccad run-transfer-frames/08-t05.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  372  d72084ccad run-transfer-frames/08-t05.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  373  d72084ccad run-transfer-frames/08-t05.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  374  d72084ccad run-transfer-frames/08-t05.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  375  d72084ccad run-transfer-frames/08-t05.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  376  
  377  # run-transfer-frames/09-t08.png
  378  d72084ccad run-transfer-frames/09-t08.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  379  d72084ccad run-transfer-frames/09-t08.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  380  d72084ccad run-transfer-frames/09-t08.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  381  d72084ccad run-transfer-frames/09-t08.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  382  d72084ccad run-transfer-frames/09-t08.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  383  
  384  # run-transfer-frames/10-t11.png
  385  d72084ccad run-transfer-frames/10-t11.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  386  d72084ccad run-transfer-frames/10-t11.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  387  d72084ccad run-transfer-frames/10-t11.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  388  d72084ccad run-transfer-frames/10-t11.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  389  d72084ccad run-transfer-frames/10-t11.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  390  
  391  # run-transfer-frames/11-t14.png
  392  d72084ccad run-transfer-frames/11-t14.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  393  d72084ccad run-transfer-frames/11-t14.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  394  d72084ccad run-transfer-frames/11-t14.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  395  d72084ccad run-transfer-frames/11-t14.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  396  d72084ccad run-transfer-frames/11-t14.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  397  
  398  # run-transfer-frames/12-t17.png
  399  d72084ccad run-transfer-frames/12-t17.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  400  d72084ccad run-transfer-frames/12-t17.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  401  d72084ccad run-transfer-frames/12-t17.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  402  d72084ccad run-transfer-frames/12-t17.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  403  d72084ccad run-transfer-frames/12-t17.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  404  
  405  # run-transfer-frames/13-t20.png
  406  d72084ccad run-transfer-frames/13-t20.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  407  d72084ccad run-transfer-frames/13-t20.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  408  d72084ccad run-transfer-frames/13-t20.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  409  d72084ccad run-transfer-frames/13-t20.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  410  d72084ccad run-transfer-frames/13-t20.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  411  
  412  # run-transfer-frames/14-t23.png
  413  d72084ccad run-transfer-frames/14-t23.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  414  d72084ccad run-transfer-frames/14-t23.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  415  d72084ccad run-transfer-frames/14-t23.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  416  d72084ccad run-transfer-frames/14-t23.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  417  d72084ccad run-transfer-frames/14-t23.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  418  
  419  # run-transfer-frames/15-t26.png
  420  d72084ccad run-transfer-frames/15-t26.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  421  d72084ccad run-transfer-frames/15-t26.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  422  d72084ccad run-transfer-frames/15-t26.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  423  d72084ccad run-transfer-frames/15-t26.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  424  d72084ccad run-transfer-frames/15-t26.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  425  
  426  # run-transfer-frames/16-t29.png
  427  d72084ccad run-transfer-frames/16-t29.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  428  d72084ccad run-transfer-frames/16-t29.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  429  d72084ccad run-transfer-frames/16-t29.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  430  d72084ccad run-transfer-frames/16-t29.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  431  d72084ccad run-transfer-frames/16-t29.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  432  
  433  # run-transfer-frames/17-t32.png
  434  d72084ccad run-transfer-frames/17-t32.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  435  d72084ccad run-transfer-frames/17-t32.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  436  d72084ccad run-transfer-frames/17-t32.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  437  d72084ccad run-transfer-frames/17-t32.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  438  d72084ccad run-transfer-frames/17-t32.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  439  
  440  # run-transfer-frames/18-t36.png
  441  d72084ccad run-transfer-frames/18-t36.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  442  d72084ccad run-transfer-frames/18-t36.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  443  d72084ccad run-transfer-frames/18-t36.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  444  d72084ccad run-transfer-frames/18-t36.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  445  d72084ccad run-transfer-frames/18-t36.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  446  
  447  # run-transfer-frames/19-t40.png
  448  d72084ccad run-transfer-frames/19-t40.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  449  d72084ccad run-transfer-frames/19-t40.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  450  d72084ccad run-transfer-frames/19-t40.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  451  d72084ccad run-transfer-frames/19-t40.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  452  d72084ccad run-transfer-frames/19-t40.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  453  
  454  # run-transfer-frames/20-t45.png
  455  d72084ccad run-transfer-frames/20-t45.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  456  d72084ccad run-transfer-frames/20-t45.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  457  d72084ccad run-transfer-frames/20-t45.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  458  d72084ccad run-transfer-frames/20-t45.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  459  d72084ccad run-transfer-frames/20-t45.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  460  
  461  # run-transfer-frames/21-t50.png
  462  d72084ccad run-transfer-frames/21-t50.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  463  d72084ccad run-transfer-frames/21-t50.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  464  d72084ccad run-transfer-frames/21-t50.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  465  d72084ccad run-transfer-frames/21-t50.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  466  d72084ccad run-transfer-frames/21-t50.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  467  
  468  # run-transfer-frames/22-t60.png
  469  d72084ccad run-transfer-frames/22-t60.png 0 0 552 174 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  470  d72084ccad run-transfer-frames/22-t60.png 0 174 112 175 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  471  d72084ccad run-transfer-frames/22-t60.png 0 175 104 625 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  472  d72084ccad run-transfer-frames/22-t60.png 0 625 112 626 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  473  d72084ccad run-transfer-frames/22-t60.png 0 626 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  474  
  475  # tick-game-content/01-cloud-hub.png
  476  d72084ccad tick-game-content/01-cloud-hub.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  477  d72084ccad tick-game-content/01-cloud-hub.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  478  d72084ccad tick-game-content/01-cloud-hub.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  479  
  480  # tick-game-content/02-back-up-page.png
  481  d72084ccad tick-game-content/02-back-up-page.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  482  d72084ccad tick-game-content/02-back-up-page.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  483  d72084ccad tick-game-content/02-back-up-page.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  484  d72084ccad tick-game-content/02-back-up-page.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  485  d72084ccad tick-game-content/02-back-up-page.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  486  
  487  # tick-game-content/03-game-content-flipped.png
  488  d72084ccad tick-game-content/03-game-content-flipped.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  489  d72084ccad tick-game-content/03-game-content-flipped.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  490  d72084ccad tick-game-content/03-game-content-flipped.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  491  d72084ccad tick-game-content/03-game-content-flipped.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  492  d72084ccad tick-game-content/03-game-content-flipped.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  493  
  494  # tick-roms/01-cloud-hub.png
  495  d72084ccad tick-roms/01-cloud-hub.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  496  d72084ccad tick-roms/01-cloud-hub.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  497  d72084ccad tick-roms/01-cloud-hub.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  498  
  499  # tick-roms/02-back-up-page.png
  500  d72084ccad tick-roms/02-back-up-page.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  501  d72084ccad tick-roms/02-back-up-page.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  502  d72084ccad tick-roms/02-back-up-page.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  503  d72084ccad tick-roms/02-back-up-page.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  504  d72084ccad tick-roms/02-back-up-page.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  505  
  506  # tick-roms/03-roms-flipped.png
  507  d72084ccad tick-roms/03-roms-flipped.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  508  d72084ccad tick-roms/03-roms-flipped.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  509  d72084ccad tick-roms/03-roms-flipped.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  510  d72084ccad tick-roms/03-roms-flipped.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  511  d72084ccad tick-roms/03-roms-flipped.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  512  
  513  # tick-settings/01-cloud-hub.png
  514  d72084ccad tick-settings/01-cloud-hub.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  515  d72084ccad tick-settings/01-cloud-hub.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  516  d72084ccad tick-settings/01-cloud-hub.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  517  
  518  # tick-settings/02-back-up-page.png
  519  d72084ccad tick-settings/02-back-up-page.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  520  d72084ccad tick-settings/02-back-up-page.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  521  d72084ccad tick-settings/02-back-up-page.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  522  d72084ccad tick-settings/02-back-up-page.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  523  d72084ccad tick-settings/02-back-up-page.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  524  
  525  # tick-settings/03-settings-flipped.png
  526  d72084ccad tick-settings/03-settings-flipped.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  527  d72084ccad tick-settings/03-settings-flipped.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  528  d72084ccad tick-settings/03-settings-flipped.png 0 118 240 594 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  529  d72084ccad tick-settings/03-settings-flipped.png 0 594 248 596 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  530  d72084ccad tick-settings/03-settings-flipped.png 0 596 552 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  531  
  532  # to-change-cloud-folder/01-cloud-hub.png
  533  d72084ccad to-change-cloud-folder/01-cloud-hub.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  534  d72084ccad to-change-cloud-folder/01-cloud-hub.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  535  d72084ccad to-change-cloud-folder/01-cloud-hub.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  536  
  537  # to-change-cloud-folder/02-hub-change-folder-row.png
  538  d72084ccad to-change-cloud-folder/02-hub-change-folder-row.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  539  d72084ccad to-change-cloud-folder/02-hub-change-folder-row.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  540  d72084ccad to-change-cloud-folder/02-hub-change-folder-row.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  541  
  542  # to-change-cloud-folder/03-folder-editor.png
  543  d72084ccad to-change-cloud-folder/03-folder-editor.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  544  d72084ccad to-change-cloud-folder/03-folder-editor.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  545  d72084ccad to-change-cloud-folder/03-folder-editor.png 0 118 240 156 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  546  d72084ccad to-change-cloud-folder/03-folder-editor.png 0 156 152 157 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  547  d72084ccad to-change-cloud-folder/03-folder-editor.png 0 157 144 643 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  548  d72084ccad to-change-cloud-folder/03-folder-editor.png 0 643 152 644 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  549  d72084ccad to-change-cloud-folder/03-folder-editor.png 0 644 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  550  
  551  # to-manage-cloud-storage/01-cloud-hub.png
  552  d72084ccad to-manage-cloud-storage/01-cloud-hub.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  553  d72084ccad to-manage-cloud-storage/01-cloud-hub.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  554  d72084ccad to-manage-cloud-storage/01-cloud-hub.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  555  
  556  # ui-settings-toggle/01-ui-settings-last-row.png
  557  d72084ccad ui-settings-toggle/01-ui-settings-last-row.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  558  d72084ccad ui-settings-toggle/01-ui-settings-last-row.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  559  d72084ccad ui-settings-toggle/01-ui-settings-last-row.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  560  
  561  # ui-settings-toggle/02-toggled.png
  562  d72084ccad ui-settings-toggle/02-toggled.png 0 0 552 116 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  563  d72084ccad ui-settings-toggle/02-toggled.png 0 116 248 118 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  564  d72084ccad ui-settings-toggle/02-toggled.png 0 118 240 708 #578  # Last Played backdrop; ES d242000a5; final fac608ff/3178b832b
  565  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/cloud-epic/migration-protocol.sh

```
    1  # Sourced only by rasteratops-vm-cloud-epic after its isolated guest/backend checks.
    2  # Runs the image's scripts and rclone; only the chosen provider operation is faulted.
    3  # No image binary is replaced. All cases reset their cloud, pointers and local record.
    4  PROTOCOL_ARMED=0
    5  protocol_cleanup() {
    6   [ "$PROTOCOL_ARMED" = 0 ] || G_ 'if [ -f /tmp/cloud-epic-protocol/remote.saved ]; then mv /tmp/cloud-epic-protocol/remote.saved /storage/.config/rclone/rclone.conf; fi; rm -f /storage/.config/profile.d/999-cloud-epic-qa.sh /storage/roms/gb/QAUnlinkedLocal.srm /storage/roms/gb/QAUnlinkedRemote.srm; rm -rf /tmp/cloud-epic-protocol /storage/qa-not-a-cloud' >/dev/null 2>&1
    7  }
    8  protocol_init() {
    9   # Even an explicitly sourced historical suite refuses before its first write.
   10   G_ 'test -x /usr/bin/cloud_migrate_layout' || {
   11    echo 'Migration protocol retired or unavailable; no fixture was changed.' >&2
   12    return 2
   13   }
   14   G_ 'test ! -e /storage/.config/profile.d/999-cloud-epic-qa.sh && test ! -e /tmp/cloud-epic-protocol' || return 1
   15   G_ 'mkdir -p /tmp/cloud-epic-protocol /storage/.config/profile.d' || return 1
   16   PROTOCOL_ARMED=1
   17   local script="$P/protocol-rclone"
   18   cat > "$script" <<'SH'
   19  #!/bin/sh
   20  if [ -f /tmp/cloud-epic-protocol/fault ] &&
   21     [ "$1 $2" = "$(cat /tmp/cloud-epic-protocol/fault)" ]; then
   22   printf '%s\n' "$1 $2" >> /tmp/cloud-epic-protocol/fired
   23   echo 'injected QA provider failure' >&2
   24   exit 5
   25  fi
   26  exec /usr/bin/rclone "$@"
   27  SH
   28   scp -q -i "$KEY" -P "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR \
   29    "$script" root@127.0.0.1:/tmp/cloud-epic-protocol/rclone || return 1
   30   G_ 'chmod 755 /tmp/cloud-epic-protocol/rclone; printf "export PATH=/tmp/cloud-epic-protocol:\$PATH\n" > /storage/.config/profile.d/999-cloud-epic-qa.sh' || return 1
   31   # Verify the production profile actually selects the shim; a fault not armed
   32   # at the image's call boundary cannot count as a successful negative control.
   33   G_ '. /etc/profile >/dev/null 2>&1; test "$(command -v rclone)" = /tmp/cloud-epic-protocol/rclone'
   34  }
   35  protocol_reset() {
   36   G_ 'systemctl stop essway; rm -f /tmp/cloud-epic-protocol/fault /tmp/cloud-epic-protocol/fired /storage/.config/cloud-layout-migration.json; rm -rf /storage/.cache/cloud_sync/scan' || return 1
   37   "$R/tools/cloud-test-backend" reset >/dev/null || return 1
   38   conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content >/dev/null || return 1
   39   mkdir -p "$DATA/ROCKNIX/Saves/gb" "$DATA/ROCKNIX/Backups/QA" "$DATA/ROCKNIX/Saves-replaced/gb" "$DATA/ROCKNIX/Content/ROMs/gb"
   40   printf 'save bytes\n' > "$DATA/ROCKNIX/Saves/gb/A.srm"
   41   printf 'settings bytes\n' > "$DATA/ROCKNIX/Backups/QA/settings.tar.gz"
   42   printf 'previous progress\n' > "$DATA/ROCKNIX/Saves-replaced/gb/A.srm"
   43   printf 'game bytes\n' > "$DATA/ROCKNIX/Content/ROMs/gb/A.gb"
   44  }
   45  protocol_snapshot() {
   46   python3 - "$DATA" <<'PY'
   47  import hashlib,json,sys
   48  from pathlib import Path
   49  root=Path(sys.argv[1])
   50  print(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
   51                   for p in sorted(root.rglob('*')) if p.is_file()},sort_keys=True))
   52  PY
   53  }
   54  protocol_pointers() { G_ "grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=|^LAYOUT_KEEP=' $CONF"; }
   55  protocol_payloads() { # pending: at least one intact copy; complete: current only
   56   python3 - "$DATA" "$1" <<'PY'
   57  from pathlib import Path
   58  import sys
   59  root=Path(sys.argv[1]); complete=sys.argv[2]=='complete'
   60  payloads={'Saves/gb/A.srm':b'save bytes\n','Backups/QA/settings.tar.gz':b'settings bytes\n',
   61            'Saves-replaced/gb/A.srm':b'previous progress\n','Content/ROMs/gb/A.gb':b'game bytes\n'}
   62  for name,data in payloads.items():
   63      old,new=(root/r/name for r in ('ROCKNIX','pixelelated'))
   64      if complete:
   65          assert new.is_file() and new.read_bytes()==data and not old.exists(), name
   66      else:
   67          assert any(p.is_file() and p.read_bytes()==data for p in (old,new)), name
   68  PY
   69  }
   70  protocol_call() { # tag, remote command; keep its real status, including a fault
   71   local tag="$1"; shift
   72   G_ "$@" > "$P/logs/$tag.log" 2>&1; PROTOCOL_RC=$?
   73   printf '%s\n' "$PROTOCOL_RC" > "$P/logs/$tag.rc"
   74  }
   75  protocol_main() {
   76   protocol_init || { check 1 'provider fault shim installed and selected'; return; }
   77   local kind="$1" operation stage tag remote before pointers
   78   remote=$(G_ '/usr/bin/rclone listremotes | head -1')
   79   # This value comes from the local QA backend installed by the parent runner.
   80   [[ "$remote" =~ ^[A-Za-z0-9_-]+:$ ]] || { check 1 'QA remote name'; return; }
   81   if [ "$kind" = T23 ]; then
   82    for operation in copy delete rcat; do
   83     for stage in Backups Saves Saves-replaced Content marker; do
   84      if [ "$operation" = rcat ]; then [ "$stage" = marker ] || continue
   85      else [ "$stage" != marker ] || continue; fi
   86      tag="T23-$operation-$stage"
   87      protocol_reset || { check 1 "$tag fixture reset"; return; }
   88      if [ "$stage" = marker ]; then
   89       G_ "printf '%s\n' '$operation ${remote}/pixelelated/.layout' > /tmp/cloud-epic-protocol/fault"
   90      else
   91       G_ "printf '%s\n' '$operation ${remote}/ROCKNIX/$stage' > /tmp/cloud-epic-protocol/fault"
   92      fi
   93      protocol_call "$tag-fault" '/usr/bin/cloud_migrate_layout --apply'
   94      [ "$PROTOCOL_RC" -ne 0 ]; check $? "$tag returns failure"
   95      G_ 'test -s /tmp/cloud-epic-protocol/fired'; check $? "$tag reaches injected provider operation"
   96      [ ! -e "$DATA/pixelelated/.layout" ]; check $? "$tag has no completion marker"
   97      protocol_payloads pending; check $? "$tag preserves every payload"
   98      protocol_pointers > "$P/logs/$tag-pointers-before.txt"
   99      G_ '/usr/bin/cloud_migrate_layout --needs-step && /usr/bin/cloud_scan --folder && grep -qx STATE=migration-pending /storage/.cache/cloud_sync/scan/state' > "$P/logs/$tag-pending.log" 2>&1
  100      check $? "$tag offered for retry by boot and scan"
  101      G_ 'rm -f /tmp/cloud-epic-protocol/fault'
  102      protocol_call "$tag-retry" '/usr/bin/cloud_migrate_layout --apply'
  103      [ "$PROTOCOL_RC" -eq 0 ]; check $? "$tag retry completes"
  104      protocol_payloads complete; check $? "$tag retry retains current bytes without old duplicates"
  105      cmp -s "$DATA/pixelelated/.layout" <(printf 'layout=2\n'); check $? "$tag publishes exact marker"
  106      G_ 'test ! -e /storage/.config/cloud-layout-migration.json'; check $? "$tag clears completed local record"
  107      protocol_snapshot > "$P/logs/$tag-cloud.json"; before=$(protocol_snapshot); pointers=$(protocol_pointers)
  108      protocol_call "$tag-repeat" '/usr/bin/cloud_migrate_layout --apply'
  109      [ "$PROTOCOL_RC" -eq 0 ] || [ "$PROTOCOL_RC" -eq 3 ]; check $? "$tag repeat succeeds"
  110      [ "$(protocol_snapshot)" = "$before" ] && [ "$(protocol_pointers)" = "$pointers" ]; check $? "$tag repeat changes no bytes/pointers"
  111      conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content >/dev/null
  112      protocol_call "$tag-follow" '/usr/bin/cloud_migrate_layout --follow'
  113      [ "$PROTOCOL_RC" -eq 0 ]; check $? "$tag clean follower configuration follows"
  114      G_ "grep -qx 'SAVES_REMOTE=\"/pixelelated/Saves\"' $CONF"; check $? "$tag follower points at current saves"
  115      [ "$(protocol_snapshot)" = "$before" ]; check $? "$tag follower changes no cloud bytes"
  116     done
  117    done
  118   elif [ "$kind" = T26 ]; then
  119    for stage in malformed future trailing; do
  120     for operation in apply follow settle seed scan; do
  121      tag="T26-$stage-$operation"
  122      protocol_reset || { check 1 "$tag fixture reset"; return; }
  123      mkdir -p "$DATA/pixelelated/Saves"
  124      case "$stage" in
  125       malformed) printf 'layout=banana\n';; future) printf 'layout=999\n';; trailing) printf 'layout=2\nextra=unrecognized\n';;
  126      esac > "$DATA/pixelelated/.layout"
  127      before=$(protocol_snapshot); pointers=$(protocol_pointers)
  128      case "$operation" in
  129       seed) protocol_call "$tag" '/usr/bin/cloud_setup --seed-folders';;
  130       scan) protocol_call "$tag" '/usr/bin/cloud_scan --folder';;
  131       *) protocol_call "$tag" "/usr/bin/cloud_migrate_layout --$operation";;
  132      esac
  133      [ "$PROTOCOL_RC" -ne 0 ]; check $? "$tag refuses unsupported layout"
  134      [ "$(protocol_snapshot)" = "$before" ] && [ "$(protocol_pointers)" = "$pointers" ]; check $? "$tag changes no bytes/pointers"
  135     done
  136    done
  137   elif [ "$kind" = T19 ]; then
  138    protocol_reset || { check 1 'T19 fixture reset'; return; }
  139    G_ 'cp -p /storage/.config/rclone/rclone.conf /tmp/cloud-epic-protocol/remote.saved; : > /storage/.config/rclone/rclone.conf; mkdir -p /storage/qa-not-a-cloud/gb /storage/roms/gb; printf "local-only sentinel\n" > /storage/qa-not-a-cloud/gb/QAUnlinkedRemote.srm; printf "local progress\n" > /storage/roms/gb/QAUnlinkedLocal.srm' || { check 1 'T19 empty-config fixture'; return; }
  140    conf /storage/qa-not-a-cloud /storage/qa-not-a-cloud/backup '' >/dev/null
  141    before=$(protocol_snapshot); pointers=$(protocol_pointers)
  142    for operation in cloud_backup cloud_restore; do
  143     for stage in direct automatic; do
  144      tag="T19-$operation-$stage"
  145      local automatic=""; [ "$stage" != automatic ] || automatic=--automatic
  146      protocol_call "$tag" "/usr/bin/$operation --yes --saves-only $automatic"
  147      [ "$PROTOCOL_RC" -ne 0 ] && grep -q "YOUR CLOUD STORAGE ISN'T SET UP YET" "$P/logs/$tag.log"; check $? "$tag refuses with setup outcome"
  148      G_ 'test ! -e /storage/qa-not-a-cloud/gb/QAUnlinkedLocal.srm && test ! -e /storage/roms/gb/QAUnlinkedRemote.srm && test "$(cat /storage/qa-not-a-cloud/gb/QAUnlinkedRemote.srm)" = "local-only sentinel"'; check $? "$tag does not treat a local path as cloud storage"
  149      [ "$(protocol_snapshot)" = "$before" ] && [ "$(protocol_pointers)" = "$pointers" ]; check $? "$tag changes no cloud bytes/pointers"
  150     done
  151    done
  152   else
  153    protocol_reset || { check 1 'T17 fixture reset'; return; }
  154    before=$(protocol_snapshot); pointers=$(protocol_pointers)
  155    G_ "printf '%s\n' 'lsd $remote' > /tmp/cloud-epic-protocol/fault"
  156    protocol_call T17-failed '/usr/bin/cloud_setup --seed-folders'
  157    [ "$PROTOCOL_RC" -ne 0 ]; check $? 'T17 failed settlement is returned'
  158    G_ 'test -s /tmp/cloud-epic-protocol/fired'; check $? 'T17 fault reached settlement provider probe'
  159    [ "$(protocol_snapshot)" = "$before" ] && [ "$(protocol_pointers)" = "$pointers" ]; check $? 'T17 no seeding or pointer writes on failure'
  160    G_ 'rm -f /tmp/cloud-epic-protocol/fault'
  161    protocol_call T17-recovered '/usr/bin/cloud_setup --seed-folders'
  162    [ "$PROTOCOL_RC" -eq 0 ]; check $? 'T17 later setup can recover'
  163    protocol_payloads pending; check $? 'T17 existing payloads survive recovery'
  164   fi
  165  }
  166  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/cloud-epic/vnc-grab.py

```
    1  #!/usr/bin/env python3
    2  """Frames from QEMU's VNC server on a cadence, each a PNG, with a per-frame signature so a card at the top or a
    3  dialog in the middle can be found without opening every file (fork #292 proof). RFB 3.8, raw, stdlib only.
    4      vnc-grab.py HOST:PORT OUTDIR PREFIX STOPFILE [cadence_s]
    5  Writes OUTDIR/PREFIX-NNNN.png and appends to OUTDIR/PREFIX.csv: n, epoch, top, mid -- the mean absolute
    6  difference (0..255) of the top band (rows 8..100) and the middle band (rows 170..320) against the FIRST frame."""
    7  import socket, struct, sys, zlib, time, os
    8  
    9  def read(s, n):
   10      b = b""
   11      while len(b) < n:
   12          c = s.recv(n - len(b))
   13          if not c: raise IOError("vnc closed")
   14          b += c
   15      return b
   16  
   17  def grab(host, port, timeout=2.0):
   18      s = socket.create_connection((host, port), timeout=timeout)
   19      read(s, 12); s.sendall(b"RFB 003.008\n")
   20      n = read(s, 1)[0]
   21      if n == 0:
   22          rl = struct.unpack(">I", read(s, 4))[0]; raise IOError("vnc refused: " + read(s, rl).decode(errors="replace"))
   23      types = read(s, n)
   24      if 1 not in types: raise IOError("vnc wants security %r" % (types,))
   25      s.sendall(b"\x01")
   26      if struct.unpack(">I", read(s, 4))[0] != 0: raise IOError("vnc security failed")
   27      s.sendall(b"\x01")
   28      w, h = struct.unpack(">HH", read(s, 4))
   29      read(s, 16); nl = struct.unpack(">I", read(s, 4))[0]; read(s, nl)
   30      s.sendall(b"\x00\x00\x00\x00" + struct.pack(">BBBBHHHBBB", 32, 24, 0, 1, 255, 255, 255, 16, 8, 0) + b"\x00\x00\x00")
   31      s.sendall(b"\x02\x00" + struct.pack(">H", 1) + struct.pack(">i", 0))
   32      s.sendall(b"\x03\x00" + struct.pack(">HHHH", 0, 0, w, h))
   33      fb = bytearray(w * h * 4); deadline = time.time() + timeout; covered = 0
   34      while covered < w * h and time.time() < deadline:
   35          mt = read(s, 1)[0]
   36          if mt != 0:
   37              if mt == 2: continue
   38              if mt == 3: read(s, 3); l = struct.unpack(">I", read(s, 4))[0]; read(s, l); continue
   39              raise IOError("vnc message %d" % mt)
   40          read(s, 1); nrect = struct.unpack(">H", read(s, 2))[0]
   41          for _ in range(nrect):
   42              x, y, rw, rh, enc = struct.unpack(">HHHHi", read(s, 12))
   43              if enc != 0: raise IOError("vnc encoding %d" % enc)
   44              data = read(s, rw * rh * 4)
   45              for row in range(rh):
   46                  o = ((y + row) * w + x) * 4
   47                  fb[o:o + rw * 4] = data[row * rw * 4:(row + 1) * rw * 4]
   48              covered += rw * rh
   49      s.close()
   50      return w, h, fb
   51  
   52  def png(path, w, h, fb):
   53      raw = b"".join(b"\x00" + bytes(v for px in range(w) for v in (fb[(r * w + px) * 4 + 2], fb[(r * w + px) * 4 + 1], fb[(r * w + px) * 4])) for r in range(h))
   54      def chunk(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
   55      open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))
   56  
   57  def band(fb, w, r0, r1):
   58      # every 4th pixel of every 2nd row, the green byte only: enough to see a card or a dialog
   59      return bytes(fb[(r * w + px) * 4 + 1] for r in range(r0, r1, 2) for px in range(0, w, 4))
   60  
   61  def diff(a, b):
   62      return sum(abs(x - y) for x, y in zip(a, b)) / max(1, len(a))
   63  
   64  if __name__ == "__main__":
   65      host, port = sys.argv[1].rsplit(":", 1); out = sys.argv[2]; prefix = sys.argv[3]; stop = sys.argv[4]
   66      cadence = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
   67      os.makedirs(out, exist_ok=True)
   68      csv = open(os.path.join(out, prefix + ".csv"), "a")
   69      first = None; n = 0
   70      while not os.path.exists(stop):
   71          t = time.time()
   72          try:
   73              w, h, fb = grab(host, int(port))
   74          except Exception as e:
   75              csv.write("%d,%.2f,err,%s\n" % (n, t, str(e).replace(",", ";"))); csv.flush(); time.sleep(cadence); continue
   76          top = band(fb, w, 8, min(100, h)); mid = band(fb, w, 170, min(320, h))
   77          if first is None: first = (top, mid)
   78          png(os.path.join(out, "%s-%04d.png" % (prefix, n)), w, h, fb)
   79          csv.write("%d,%.2f,%.1f,%.1f\n" % (n, t, diff(top, first[0]), diff(mid, first[1]))); csv.flush()
   80          n += 1
   81          rest = cadence - (time.time() - t)
   82          if rest > 0: time.sleep(rest)
   83      csv.close()
   84  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/confirm-cloud-folder.steps

```
    1  # Start: SAVES FOLDER on-screen keyboard, holding the current value.
    2  # START submits once and closes the keyboard. An unchanged value is a
    3  # no-op on every backend: no provider probe, path write or file transfer.
    4  # End: CLOUD hub, CHANGE CLOUD FOLDER focused, after leaving CLOUD FOLDERS.
    5  # The result frame is the three-row selector, not a provider outcome (#527).
    6  key ret
    7  wait-for-change 30 0
    8  settle
    9  shot folder-result
   10  key z
   11  wait-for-change
   12  settle
   13  shot after-dismiss
   14  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/continue-to-systems.steps

```
    1  # Start: a transfer page, focus on SAVES, with ROMS AND BIOS or GAME CONTENT
    2  # on (so the second button reads CONTINUE). End: the systems page, focus on
    3  # its first system row. Four rows down is the button bar on BACK; right is
    4  # CONTINUE; the scan behind the page takes a few seconds, which is what the
    5  # long settle waits out -- the page is static once the systems are listed.
    6  key down
    7  wait-for-change
    8  key down
    9  wait-for-change
   10  key down
   11  wait-for-change
   12  key down
   13  wait-for-change
   14  key right
   15  wait-for-change
   16  settle
   17  shot continue-focused
   18  key x
   19  wait-for-change 20
   20  settle 30
   21  shot systems-page
   22  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/docs/README.md

```
    1  # The walks behind the rocknix.org screenshots (#323)
    2  
    3  One step file per page, run with `tools/vm-visual-qa --monitor <sock> run
    4  <file> --outdir <dir>` on a GENERIC_X64 guest at 640x480, so every picture on
    5  a wiki page can be taken again when the screen changes. The frames land in
    6  the site checkout under `docs/_inc/images/<page>/`.
    7  
    8  Fixture: a cloud storage connected (the hub's rows read their stamps), and, for
    9  `networking.steps`, the stand-in `wifictl` from `proofs-307/guest/qa318-wifictl`
   10  bound over `/usr/bin/wifictl` (the guest has no Wi-Fi adapter; the stand-in
   11  answers Home Wi-Fi in use and Cafe saved). Each walk starts on a system or
   12  game list with nothing open and ends with `dismiss-dialogs`; each press has
   13  30 s and one re-send, since a loaded guest eats a press now and then. The MAIN MENU
   14  is walked from its bottom (up wraps through BACK to QUIT), so a guest signed
   15  in to RetroAchievements, whose menu opens on that extra row, walks the same.
   16  From the top row it is two presses to QUIT (BACK, then the wrap); until
   17  EmulationStation f1ae6bc25 the first press landed on an empty tab strip (#325,
   18  `main-menu-up-probe.steps`) and every MAIN MENU count here was one higher.
   19  
   20  A frame that shows an account's name is painted out with `tools/png-blackout`
   21  before it is filed: the RETROACHIEVEMENTS SETTINGS frame's USERNAME row, on a
   22  signed-in guest.
   23  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/docs/cloud-sync.steps

```
    1  # configure/cloud-sync.md: the cloud rows on GAME SETTINGS, the cloud hub,
    2  # the tick page behind BACK UP TO THE CLOUD, and CONNECT OR REPAIR CLOUD
    3  # STORAGE. GAME SETTINGS is eleven presses up from the MAIN MENU's top row
    4  # (BACK, QUIT, then nine rows); it opens on its first row, and up wraps
    5  # through BACK and PER SYSTEM ADVANCED CONFIGURATION to MANAGE CLOUD
    6  # STORAGE, the last row of the CLOUD SETTINGS group. On the hub, BACK UP TO
    7  # THE CLOUD is the first row and CONNECT OR REPAIR CLOUD STORAGE the eighth
    8  # press down (CONNECTED TO is a focus stop).
    9  # The MAIN MENU is reached from its bottom, so the walk is the same whether
   10  # the guest is signed in to RetroAchievements (the menu then opens on that
   11  # row, above GAME SETTINGS) or not: up from the top row lands on BACK, the
   12  # next on QUIT, and the rows above QUIT never move. (Until EmulationStation
   13  # f1ae6bc25 the first press landed on an empty tab strip, #325, and every
   14  # count here was one higher.)
   15  key ret
   16  wait-for-change 30 1
   17  settle
   18  key up
   19  wait-for-change 30 1
   20  key up
   21  wait-for-change 30 1
   22  key up
   23  wait-for-change 30 1
   24  key up
   25  wait-for-change 30 1
   26  key up
   27  wait-for-change 30 1
   28  key up
   29  wait-for-change 30 1
   30  key up
   31  wait-for-change 30 1
   32  key up
   33  wait-for-change 30 1
   34  key up
   35  wait-for-change 30 1
   36  key up
   37  wait-for-change 30 1
   38  key up
   39  wait-for-change 30 1
   40  settle
   41  key x
   42  wait-for-change 30 1
   43  settle
   44  key up
   45  wait-for-change 30 1
   46  key up
   47  wait-for-change 30 1
   48  key up
   49  wait-for-change 30 1
   50  settle
   51  shot game-settings-cloud-rows
   52  key x
   53  wait-for-change 30 1
   54  settle
   55  shot cloud-hub
   56  key x
   57  wait-for-change 30 1
   58  settle
   59  shot back-up-to-the-cloud
   60  key z
   61  wait-for-change 30 1
   62  settle
   63  key down
   64  wait-for-change 30 1
   65  key down
   66  wait-for-change 30 1
   67  key down
   68  wait-for-change 30 1
   69  key down
   70  wait-for-change 30 1
   71  key down
   72  wait-for-change 30 1
   73  key down
   74  wait-for-change 30 1
   75  key down
   76  wait-for-change 30 1
   77  key down
   78  wait-for-change 30 1
   79  settle
   80  key x
   81  wait-for-change 30 1
   82  settle
   83  shot connect-or-repair-cloud-storage
   84  dismiss-dialogs
   85  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/docs/main-menu-up-probe.steps

```
    1  # The probe behind the docs walks' counts: from the MAIN MENU's top row, one up at a time with a still after each (2026-09-29). Run with the menu open.
    2  shot top
    3  key up
    4  wait-for-change 30 1
    5  settle
    6  shot up-1
    7  key up
    8  wait-for-change 30 1
    9  settle
   10  shot up-2
   11  key up
   12  wait-for-change 30 1
   13  settle
   14  shot up-3
   15  key up
   16  wait-for-change 30 1
   17  settle
   18  shot up-4
   19  key up
   20  wait-for-change 30 1
   21  settle
   22  shot up-5
   23  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/docs/networking.steps

```
    1  # configure/networking.md: NETWORK SETTINGS, the Wi-Fi picker, a saved
    2  # network's dialog and SAVED NETWORKS. Needs the stand-in wifictl (README).
    3  # NETWORK SETTINGS is six presses up from the MAIN MENU's top row (BACK,
    4  # QUIT, SYSTEM SETTINGS, UPDATES & DOWNLOADS, SCRAPER, NETWORK SETTINGS); on
    5  # it, WI-FI NETWORK is five presses down from IP ADDRESS and MANAGE SAVED
    6  # NETWORKS two more. In the picker the stand-in lists Home Wi-Fi (in use)
    7  # first, Cafe (saved) second and Neighbour third; a press on Neighbour opens
    8  # the WI-FI KEY keyboard, where every key is a letter, so the count to Cafe
    9  # is one down, never two (the third capture typed "zz" into it).
   10  # The MAIN MENU is reached from its bottom, so the walk is the same whether
   11  # the guest is signed in to RetroAchievements (the menu then opens on that
   12  # row, above GAME SETTINGS) or not: up from the top row lands on BACK, the
   13  # next on QUIT, and the rows above QUIT never move. (Until EmulationStation
   14  # f1ae6bc25 the first press landed on an empty tab strip, #325, and every
   15  # count here was one higher.)
   16  key ret
   17  wait-for-change 30 1
   18  settle
   19  key up
   20  wait-for-change 30 1
   21  key up
   22  wait-for-change 30 1
   23  key up
   24  wait-for-change 30 1
   25  key up
   26  wait-for-change 30 1
   27  key up
   28  wait-for-change 30 1
   29  key up
   30  wait-for-change 30 1
   31  settle
   32  key x
   33  wait-for-change 30 1
   34  settle
   35  shot network-settings
   36  key down
   37  wait-for-change 30 1
   38  key down
   39  wait-for-change 30 1
   40  key down
   41  wait-for-change 30 1
   42  key down
   43  wait-for-change 30 1
   44  key down
   45  wait-for-change 30 1
   46  settle
   47  key x
   48  wait-for-change 30 1
   49  wait 5
   50  settle
   51  shot wifi-networks
   52  key down
   53  wait-for-change 30 1
   54  settle
   55  key x
   56  wait-for-change 30 1
   57  settle
   58  shot wifi-saved-network
   59  key z
   60  wait-for-change 30 1
   61  settle
   62  key z
   63  wait-for-change 30 1
   64  settle
   65  key down
   66  wait-for-change 30 1
   67  key down
   68  wait-for-change 30 1
   69  settle
   70  key x
   71  wait-for-change 30 1
   72  wait 3
   73  settle
   74  shot saved-networks
   75  key x
   76  wait-for-change 30 1
   77  settle
   78  shot forget-network
   79  dismiss-dialogs
   80  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/docs/retro-achievements.steps

```
    1  # play/retro-achievements.md: RETROACHIEVEMENTS SETTINGS and its OFFLINE
    2  # ACHIEVEMENTS (BETA) page. GAME SETTINGS is eleven presses up from the MAIN
    3  # MENU's top row; on it: UPDATE GAMELISTS, MOONLIGHT GAME STREAMING, then the
    4  # ACCOUNTS heading, then RETROACHIEVEMENTS SETTINGS -- two presses down, not
    5  # three (two exploratory walks counted the heading, 2026-09-29). On the
    6  # settings page: RETROACHIEVEMENTS, USERNAME, PASSWORD, WEB API KEY (fork
    7  # builds), then OPTIONS: HARDCORE MODE, OFFLINE ACHIEVEMENTS (BETA) -- five
    8  # presses down. The settings frame shows the account's name on its USERNAME
    9  # row: tools/png-blackout before it is filed.
   10  # The MAIN MENU is reached from its bottom, so the walk is the same whether
   11  # the guest is signed in to RetroAchievements (the menu then opens on that
   12  # row, above GAME SETTINGS) or not: up from the top row lands on BACK, the
   13  # next on QUIT, and the rows above QUIT never move. (Until EmulationStation
   14  # f1ae6bc25 the first press landed on an empty tab strip, #325, and every
   15  # count here was one higher.)
   16  key ret
   17  wait-for-change 30 1
   18  settle
   19  key up
   20  wait-for-change 30 1
   21  key up
   22  wait-for-change 30 1
   23  key up
   24  wait-for-change 30 1
   25  key up
   26  wait-for-change 30 1
   27  key up
   28  wait-for-change 30 1
   29  key up
   30  wait-for-change 30 1
   31  key up
   32  wait-for-change 30 1
   33  key up
   34  wait-for-change 30 1
   35  key up
   36  wait-for-change 30 1
   37  key up
   38  wait-for-change 30 1
   39  key up
   40  wait-for-change 30 1
   41  settle
   42  key x
   43  wait-for-change 30 1
   44  settle
   45  key down
   46  wait-for-change 30 1
   47  key down
   48  wait-for-change 30 1
   49  settle
   50  key x
   51  wait-for-change 30 1
   52  settle
   53  shot retroachievements-settings
   54  key down
   55  wait-for-change 30 1
   56  key down
   57  wait-for-change 30 1
   58  key down
   59  wait-for-change 30 1
   60  key down
   61  wait-for-change 30 1
   62  key down
   63  wait-for-change 30 1
   64  settle
   65  key x
   66  wait-for-change 30 1
   67  settle
   68  shot offline-achievements
   69  dismiss-dialogs
   70  
```

## PNG fixture (not attached): tools/vm-walks/fixtures/arcade-vertical-raw-left.png

2120 bytes, sha256 b6684e0b5a82249e8e1e148c1944df39c760ceb531311e8f75fdd07c41de22c2

## PNG fixture (not attached): tools/vm-walks/fixtures/gb-160x144.png

1095 bytes, sha256 0e1c0a1b6b4977ecfa3dabd949982895381a222f5aa9a075d73a299672a3461d

## PNG fixture (not attached): tools/vm-walks/fixtures/nes-256x240-right.png

2010 bytes, sha256 bb5953e6de7793bc01bf005cc5ab92d8bb053b226f33c2cf693004cc6a1e4499

## file, whole, at 8ebaf8daad: tools/vm-walks/fixtures/system-selected.sh

```
    1  #!/bin/sh
    2  # QA guest observation only; installed by vm-qa before a manager walk.
    3  printf '%s\n' "$1" > /storage/.cache/vm-qa-selected-system
    4  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/m7-cloud-sync.steps

```
    1  # #422: candidate fixture has global.retroachievements=0 and kodi.enabled=0.
    2  # GAME SETTINGS is first regardless of the optional Wi-Fi row. Capture the
    3  # entry before continuing; use only with this explicitly seeded fixture.
    4  key ret
    5  wait-for-change 30 1
    6  settle
    7  shot main-menu-entry
    8  key x
    9  wait-for-change 30 1
   10  settle
   11  shot game-settings-entry
   12  key up
   13  wait-for-change 30 1
   14  key up
   15  wait-for-change 30 1
   16  key up
   17  wait-for-change 30 1
   18  settle
   19  shot game-settings-cloud-rows
   20  key x
   21  wait-for-change 30 1
   22  settle
   23  shot cloud-hub
   24  key x
   25  wait-for-change 30 1
   26  settle
   27  shot back-up-to-the-cloud
   28  key z
   29  wait-for-change 30 1
   30  settle
   31  key down
   32  wait-for-change 30 1
   33  key down
   34  wait-for-change 30 1
   35  key down
   36  wait-for-change 30 1
   37  key down
   38  wait-for-change 30 1
   39  key down
   40  wait-for-change 30 1
   41  key down
   42  wait-for-change 30 1
   43  key down
   44  wait-for-change 30 1
   45  key down
   46  wait-for-change 30 1
   47  settle
   48  key x
   49  wait-for-change 30 1
   50  settle
   51  shot connect-or-repair-cloud-storage
   52  dismiss-dialogs
   53  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/m7-retro-achievements.steps

```
    1  # #422: candidate fixture has global.retroachievements=0 and kodi.enabled=0.
    2  # GAME SETTINGS is first regardless of the optional Wi-Fi row. Capture the
    3  # entry before continuing; use only with this explicitly seeded fixture.
    4  key ret
    5  wait-for-change 30 1
    6  settle
    7  shot main-menu-entry
    8  key x
    9  wait-for-change 30 1
   10  settle
   11  shot game-settings-entry
   12  key down
   13  wait-for-change 30 1
   14  key down
   15  wait-for-change 30 1
   16  settle
   17  key x
   18  wait-for-change 30 1
   19  settle
   20  shot retroachievements-settings
   21  key down
   22  wait-for-change 30 1
   23  key down
   24  wait-for-change 30 1
   25  key down
   26  wait-for-change 30 1
   27  key down
   28  wait-for-change 30 1
   29  key down
   30  wait-for-change 30 1
   31  settle
   32  key x
   33  wait-for-change 30 1
   34  settle
   35  shot offline-achievements
   36  dismiss-dialogs
   37  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/manager.steps

```
    1  # Start: the carousel on the system the suite line set with StartupSystem
    2  # (a game list's first entry is the fixture game). End: the carousel.
    3  #
    4  # The SAVE STATE MANAGER for the list's first game: carousel, list, X for
    5  # GAME OPTIONS, A for the manager, right to the capture tile, back out.
    6  # Read the manager frames for the START NEW GAME arrow (one arrow, one
    7  # direction, one size on every system -- #250) and the capture tile at the
    8  # system's aspect (#243) and turn (#245, #248).
    9  settle
   10  shot 0-carousel
   11  key x
   12  wait-for-change
   13  settle
   14  shot 1-list
   15  key s
   16  wait-for-change 6
   17  settle
   18  shot 2-game-options
   19  key x
   20  wait-for-change 10
   21  settle 10 2
   22  shot 3-manager
   23  key right
   24  wait-for-change 4
   25  settle
   26  shot 4-manager-next-tile
   27  key z
   28  wait-for-change
   29  settle
   30  key z
   31  wait-for-change
   32  settle
   33  dismiss-dialogs
   34  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/masks.txt

```
    1  # Pixels tools/frame-diff does not compare, `<screen-glob> x0 y0 x1 y1  # why`
    2  # per line: half-open rectangles in the frame's own pixels (the pair's guests
    3  # are 1280x800). Every line is a place the check is blind, so each says why,
    4  # and each was measured from a diff of two runs (2026-09-23, runs 15 and 16:
    5  # 63 frames, and outside these rectangles not one pixel differed).
    6  * 1110 36 1215 64                  # the clock, top right: HH:MM is the run's minute; the hour digit reaches x 1135 (runs 14 vs 16)
    7  run-transfer*/* 240 370 1040 396   # COMPARING N OF M FILES / UPLOADING N OF M: the phase line, centred, as wide as its numbers (x 333..948 seen)
    8  run-transfer*/* 250 448 1030 474   # the progress bar
    9  run-transfer*/* 560 508 720 536    # ELAPSED M:SS
   10  confirm-cloud-folder/* 416 222 432 272   # the CLOUD FOLDER editor's text caret after /Rasteratops/Saves (x 424..425 on 1acdaf2cce, run 96; 380..396 after /ROCKNIX/Saves before the epic): a 2 px white bar that blinks, on in the 443028ff7a baseline and off in run 25 (c8609558d4, 2026-09-24); the field's text stays compared
   11  to-change-cloud-folder/* 416 222 432 272   # the same editor's caret on the other walk, which frames it too (03-folder-editor)
   12  run-transfer/07-transfer-running.png 545 280 735 345   # the running sample is taken the moment the page appears, which races the run's first item: PREPARING... on run 97 (d9493fe339), SAVES / ITEM 1 OF 4 on run 96 (1acdaf2cce) and on the baseline, the same scripts both times; the frames walk shows each phase at fixed offsets, so this one sample's item line is not compared (2026-10-01)
   13  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/match-dialog.steps

```
    1  # Start: the CLOUD hub, focus on BACK UP TO THE CLOUD (where
    2  # to-manage-cloud-storage.steps leaves it). End: the transfer page after a
    3  # match, finished, waiting for any button.
    4  # MATCH THIS DEVICE TO THE CLOUD is the third row of BACKUP AND RESTORE. A
    5  # opens the compare (COMPARING YOUR ROMS AND BIOS FILES WITH THE CLOUD), a
    6  # network round trip per selected system; the confirmation follows. Needs
    7  # the seed fixture (cloud-test-backend seed-content + seed-device) so the
    8  # device holds ROMs the cloud does not -- gb entirely, snes/deviceonly.sfc --
    9  # and the preview has something to list. YES is the first button.
   10  #
   11  # Neither A press is re-sent: both start network work, and the settle after
   12  # each is what waits for it rather than a guess at how long it takes.
   13  key down
   14  wait-for-change
   15  key down
   16  wait-for-change
   17  settle
   18  shot cloud-hub-match-row
   19  key x
   20  wait-for-change 25 0
   21  settle 40
   22  shot match-confirm
   23  key x
   24  wait-for-change 25 0
   25  settle 60
   26  shot match-done
   27  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/reset.steps

```
    1  # Start: anywhere. End: the system carousel, awake, with nothing open --
    2  # the state every other walk assumes.
    3  #
    4  # This was four B presses, which is a guess about how deep the interface
    5  # is. B closes a dialog, a menu or a game list, but on the carousel it
    6  # OPENS the GO TO dialog (GO TO LETTER or GO TO MANUFACTURER, by the SORT
    7  # SYSTEMS setting; SystemView::showNavigationBar picks). So four presses
    8  # reach the carousel from an even depth and leave GO TO open from an odd
    9  # one: with a single dialog up -- the boot-time journey prompt, the
   10  # RetroAchievements offer, FINISH RESTORE SETUP -- the file written to
   11  # close things ended holding one (#85).
   12  #
   13  # `dismiss-dialogs` presses B until the screen repeats one it has already
   14  # stood on. That repeat is the carousel toggling GO TO, so it stops there
   15  # whatever the depth was, and a press that changes nothing at all is
   16  # re-sent rather than mistaken for the repeat.
   17  wake
   18  dismiss-dialogs
   19  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/restore-page.steps

```
    1  # Start: the CLOUD hub, focus on BACK UP TO THE CLOUD. End: RESTORE FROM THE
    2  # CLOUD's options page, focus on SAVES. Same rows and memory as the backup
    3  # page, per direction. Since the cloud epic (#350, D-CLOUD-167) the press
    4  # opens the scan page first and goes on to the options by itself; the
    5  # settle waits that out. The fixture seeds /pixelelated/Saves so the scan
    6  # does not stop at the offer to create the folder (vm-qa's ensure_fixture).
    7  key down
    8  wait-for-change
    9  key x
   10  wait-for-change
   11  settle
   12  shot restore-page
   13  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/run-transfer-frames.steps

```
    1  # Start: the systems page, focus on its first system row, NO SYSTEM TICKED
    2  # (see run-transfer.steps for why). End: the CLOUD hub. Like run-transfer
    3  # but a frame every three seconds for a minute, so every phase of a run
    4  # with settings, saves and several systems is caught on the page (#95).
    5  #
    6  # This is the one file where `wait N` is still right, and it is not a guess
    7  # about timing: the fixed waits here are a SAMPLER. The point is a frame at
    8  # regular offsets from the first observed transfer frame, so the phases can
    9  # be read off in order. The historical t02 name is that first changed frame,
   10  # not an assertion that two seconds elapsed (#439). Later waits are relative
   11  # to it. A settle would wait for the page
   12  # to stop moving, which is precisely what this file exists not to do. The
   13  # presses before the transfer starts still use the frame steps, because
   14  # those are waits for a screen and not samples of one.
   15  key up
   16  wait-for-change
   17  key right
   18  wait-for-change
   19  key x
   20  wait-for-change 15 0
   21  settle
   22  shot selected-all
   23  key right
   24  wait-for-change
   25  key x
   26  wait-for-change 25 0
   27  shot t02
   28  wait 3
   29  shot t05
   30  wait 3
   31  shot t08
   32  wait 3
   33  shot t11
   34  wait 3
   35  shot t14
   36  wait 3
   37  shot t17
   38  wait 3
   39  shot t20
   40  wait 3
   41  shot t23
   42  wait 3
   43  shot t26
   44  wait 3
   45  shot t29
   46  wait 3
   47  shot t32
   48  wait 4
   49  shot t36
   50  wait 4
   51  shot t40
   52  wait 5
   53  shot t45
   54  wait 5
   55  shot t50
   56  wait 10
   57  shot t60
   58  key x
   59  wait-for-change 15
   60  settle
   61  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/run-transfer.steps

```
    1  # Start: the systems page, focus on its first system row (where
    2  # continue-to-systems.steps leaves it), with NO SYSTEM TICKED -- the
    3  # precondition below. End: the CLOUD hub, after the transfer page has been
    4  # closed.
    5  #
    6  # Up from the first row is the button bar on BACK. The bar has three buttons
    7  # since SELECT ALL joined it (ES d57542662): BACK / SELECT ALL (or SELECT
    8  # NONE) / BACK UP (or RESTORE). The first right and A press SELECT ALL; the
    9  # second right and A press the verb. Without the first pair the verb runs
   10  # whatever selection the picker last saved -- it saves on every close, BACK
   11  # included -- and with nothing ticked cloud_content_backup --selected prints
   12  # "Nothing to back up" and exits 1: the page ends FAILED with rows 3-4 blank
   13  # and no transfer was exercised, which is how this walk shipped once (#85).
   14  #
   15  # The precondition, because the button is a toggle that reads as what it
   16  # would do next: once every system is on it says SELECT NONE, and on a VM
   17  # where an earlier walk already saved SELECT ALL this press clears the
   18  # selection and the run fails the same way. The selection lives in
   19  # /storage/.cache/cloud_sync/content-systems and survives an EmulationStation
   20  # restart, so a fresh ES is not enough. Make it true rather than guess: over
   21  # serial,
   22  #   cloud_content_restore --set-systems ""
   23  # empties the saved selection (a fresh image has none). The bar is rebuilt
   24  # on the UI thread after the press, which is what the settle waits for; read
   25  # the selected-all frame -- every switch on, the button now reading SELECT
   26  # NONE -- before trusting the frames after it.
   27  #
   28  # Neither A press is re-sent. SELECT ALL is a toggle, so a second press
   29  # clears what the first set; the verb starts a transfer, so a second press
   30  # would start another.
   31  #
   32  # `settle 90` is where the old `wait 16` was. The transfer page repaints its
   33  # elapsed time every second while it runs, so it is never still until the
   34  # job ends and the page reads PRESS ANY BUTTON TO CLOSE -- which makes "the
   35  # screen stopped moving" the same event as "the transfer finished", for a
   36  # small fixture and for a real library alike. The bound is the give-up, not
   37  # the expectation. Three quiet seconds, not the default 1.2: on vm-qa run 71
   38  # (320d2b2bea, 2026-09-28) the default returned at ELAPSED 0:02 with the
   39  # page still on ITEM 2 OF 4 -- the once-a-second repaint hid between the
   40  # polls -- and the done frame was the running page, an unclaimed box.
   41  key up
   42  wait-for-change
   43  key right
   44  wait-for-change
   45  key x
   46  wait-for-change 15 0
   47  settle
   48  shot selected-all
   49  key right
   50  wait-for-change
   51  key x
   52  wait-for-change 25 0
   53  shot transfer-running
   54  settle 90 3
   55  shot transfer-done
   56  key x
   57  wait-for-change 15
   58  settle
   59  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/suite.txt

```
    1  # The walks suite: one composition per line, `<name> = <steps file>...`,
    2  # replayed by tools/vm-qa in this order. Blank lines and # comments ignored.
    3  #
    4  # WHY COMPOSITIONS AND NOT FILES. Most walk files do not start on the
    5  # carousel -- back-up-page.steps starts on the CLOUD hub, run-transfer.steps
    6  # on the systems page -- because each one is a leg, and the legs are meant to
    7  # be `cat`ted together (README.md). The runner used to replay every file on
    8  # its own from a rebooted guest, so nine of them pressed A on the carousel
    9  # and drove whatever game list happened to be under the cursor. The frames
   10  # were still counted and the suite still passed: a walk that reached nothing
   11  # looked exactly like a walk that reached its screen.
   12  #
   13  # So the suite names the composition, and the last file in each line is the
   14  # walk being exercised -- its shots are the ones to read.
   15  #
   16  # Each line starts from a REBOOTED guest, which the runner handles: the
   17  # carousel, awake, with nothing open.
   18  #
   19  # `default-pre = <shell>` runs on the guest before every walk's reboot, and
   20  # a line's own `| <shell>` runs after it, so a walk can override what the
   21  # default set.
   22  #
   23  # The default exists because a reboot is NOT enough to put the transfer
   24  # pages back to their shipped state. EmulationStation saves the four class
   25  # switches as `cloudsync.pick.<direction>.<class>` in
   26  # /storage/.config/system/configs/system.cfg when the page closes, and
   27  # restores them at its next start -- so `tick-roms`, which FLIPS rather
   28  # than sets, turned ROMS AND BIOS *off* after any walk that had left it on,
   29  # and the walk after that backed up saves alone instead of reaching the
   30  # systems page. Three suite runs on 2026-09-11 failed there before the
   31  # switches were found; note that it is
   32  # /storage/.config/system/configs/system.cfg, not the
   33  # /storage/.config/system.cfg the rest of the harness talks about, and that
   34  # a value written while ES is running does survive the reboot.
   35  #
   36  # The default also empties the saved system selection, which is
   37  # run-transfer.steps' own precondition for a different reason: its SELECT
   38  # ALL is a toggle that reads SELECT NONE once everything is on.
   39  #
   40  # It also puts the CLOUD hub's two sync rows into one state -- both switches
   41  # off, no last-run stamp under either -- because a full vm-qa run reaches
   42  # the walks after the exit suite has turned the game-exit sync on and left
   43  # a COMPLETED stamp, and a `--only walks` run does not. The frame-diff
   44  # suite (#252) compares the hub's pixels, so the walks decide that state
   45  # rather than inherit it from whatever ran before. And it clears
   46  # StartupSystem, with essway stopped first, so a manager walk's landing
   47  # system does not become every later walk's.
   48  
   49  # THE ORDER IS LOAD-BEARING, once, at the top. match-dialog needs the
   50  # device to hold ROMs the cloud does not (the seed fixture: gb entirely,
   51  # snes/deviceonly.sfc) so its preview has something to list, and the
   52  # run-transfer walks upload exactly those. Run after them it reaches THIS
   53  # DEVICE ALREADY MATCHES YOUR CLOUD. THERE IS NOTHING TO REMOVE. -- a true
   54  # answer to a question the walk did not mean to ask (2026-09-11). Nothing
   55  # else here cares what ran before it.
   56  #
   57  # match-dialog is also the one line whose precondition SETS a selection
   58  # rather than clearing it: with none picked it answers YOU HAVEN'T PICKED
   59  # ANY SYSTEMS FOR THIS DEVICE YET, which is the same dead end reached from
   60  # the other direction.
   61  #
   62  # run-transfer-frames comes before run-transfer for a smaller version of
   63  # the same reason. Its whole purpose is a frame every three seconds so the
   64  # phases of a running transfer can be read off in order (#95), and whichever
   65  # of the two runs second finds the cloud already holding what the first
   66  # uploaded and reaches COMPLETED - NOTHING NEW in under two seconds. The
   67  # sampler is the one that needs something to sample; run-transfer's frames
   68  # are a completed page either way.
   69  #
   70  # For the same reason a second run of the whole suite wants the endpoint
   71  # re-seeded: the first run's transfers put the device-only files in the
   72  # cloud, and cloud-test-backend's seed-content does not take them back out.
   73  # What has to go back is the cloud's copy of what only the device should
   74  # have -- ROMs/gb, ROMs/pico-8 and ROMs/snes/deviceonly.sfc under the
   75  # endpoint's Content root.
   76  
   77  default-pre = systemctl stop essway; sed -i '/StartupSystem/d' /storage/.config/emulationstation/es_settings.cfg; . /etc/profile; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; rm -f /storage/.cache/cloud_sync/last-*; for d in backup restore; do for k in content media settings; do set_setting cloudsync.pick.$d.$k 0; done; set_setting cloudsync.pick.$d.saves 1; done; cloud_content_restore --set-systems ""
   78  
   79  to-manage-cloud-storage = to-manage-cloud-storage
   80  back-up-page            = to-manage-cloud-storage back-up-page
   81  restore-page            = to-manage-cloud-storage restore-page
   82  match-dialog            = to-manage-cloud-storage match-dialog | cloud_content_restore --set-systems "gb snes"
   83  to-change-cloud-folder  = to-manage-cloud-storage to-change-cloud-folder
   84  confirm-cloud-folder    = to-manage-cloud-storage to-change-cloud-folder confirm-cloud-folder
   85  tick-roms               = to-manage-cloud-storage back-up-page tick-roms
   86  tick-settings           = to-manage-cloud-storage back-up-page tick-settings
   87  tick-game-content       = to-manage-cloud-storage back-up-page tick-game-content
   88  continue-to-systems     = to-manage-cloud-storage back-up-page tick-roms continue-to-systems
   89  run-transfer-frames     = to-manage-cloud-storage back-up-page tick-roms continue-to-systems run-transfer-frames
   90  run-transfer            = to-manage-cloud-storage back-up-page tick-roms continue-to-systems run-transfer
   91  ui-settings-toggle      = ui-settings-toggle
   92  
   93  # The manager walks (#252). `StartupSystem` lands the rebooted carousel on
   94  # the system whose first game carries the fixture capture; essway is stopped
   95  # before the edit, since EmulationStation writes its settings back at exit
   96  # and would undo it at the reboot. default-pre clears the key again for every
   97  # other walk, and every walk, so the default start stays the default.
   98  manager-nes = manager | systemctl stop essway; sed -i 's|</config>|\t<string name="StartupSystem" value="nes" />\n</config>|' /storage/.config/emulationstation/es_settings.cfg; sync
   99  manager-gb  = manager | systemctl stop essway; sed -i 's|</config>|\t<string name="StartupSystem" value="gb" />\n</config>|' /storage/.config/emulationstation/es_settings.cfg; sync
  100  manager-fbn = manager | systemctl stop essway; sed -i 's|</config>|\t<string name="StartupSystem" value="fbn" />\n</config>|' /storage/.config/emulationstation/es_settings.cfg; sync
  101  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/tick-game-content.steps

```
    1  # Start: a transfer page, focus on SAVES. End: same page, focus on SAVES, the
    2  # GAME CONTENT switch flipped. Two rows down from SAVES.
    3  # The switch press takes no re-send (see tick-roms.steps).
    4  key down
    5  wait-for-change
    6  key down
    7  wait-for-change
    8  key x
    9  wait-for-change 12 0
   10  settle
   11  shot game-content-flipped
   12  key up
   13  wait-for-change
   14  key up
   15  wait-for-change
   16  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/tick-roms.steps

```
    1  # Start: a transfer page, focus on SAVES. End: same page, focus on ROMS AND
    2  # BIOS, its switch flipped. Flip, not set: the row remembers its last state.
    3  #
    4  # The switch press takes `wait-for-change <timeout> 0` -- no re-send. A
    5  # toggle is the one press where the tool's default retry would be wrong:
    6  # pressing it a second time puts the switch back, so an eaten press must be
    7  # reported rather than repaired. A flipped switch moves about 0.2% of the
    8  # screen, twice the tool's threshold and seven times the clock's tick.
    9  key down
   10  wait-for-change
   11  key x
   12  wait-for-change 12 0
   13  settle
   14  shot roms-flipped
   15  key up
   16  wait-for-change
   17  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/tick-settings.steps

```
    1  # Start: a transfer page, focus on SAVES. End: same page, focus on SAVES,
    2  # the SETTINGS switch flipped. Rows: SAVES, ROMS AND BIOS, GAME CONTENT,
    3  # SETTINGS -- three down from SAVES. Flip, not set: the row remembers its
    4  # last state, so read the frame.
    5  # The switch press takes no re-send (see tick-roms.steps).
    6  key down
    7  wait-for-change
    8  key down
    9  wait-for-change
   10  key down
   11  wait-for-change
   12  key x
   13  wait-for-change 12 0
   14  settle
   15  shot settings-flipped
   16  key up
   17  wait-for-change
   18  key up
   19  wait-for-change
   20  key up
   21  wait-for-change
   22  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/to-change-cloud-folder.steps

```
    1  # Start: the CLOUD hub, focus on BACK UP TO THE CLOUD. End: the CLOUD
    2  # FOLDERS selector, then the SAVES FOLDER editor with its current value.
    3  #
    4  # Seven downs reach CHANGE CLOUD FOLDER: RESTORE, MATCH, the two SAVE
    5  # MANAGEMENT switches, CONNECTED TO, CHECK CONNECTION, then it. It was six
    6  # until CHECK CONNECTION joined CLOUD STORAGE SETUP above it -- with six,
    7  # A ran the connection check and the walk sat on its WEBDAV ANSWERED.
    8  # YOU'RE CONNECTED. dialog, where START does nothing (2026-09-11, caught
    9  # by wait-for-change rather than by four wrong frames).
   10  #
   11  # Read the hub-change-folder-row frame before trusting the count: a row
   12  # added to this group moves the target again, and the frame is what says
   13  # where the focus actually is.
   14  key down
   15  wait-for-change
   16  key down
   17  wait-for-change
   18  key down
   19  wait-for-change
   20  key down
   21  wait-for-change
   22  key down
   23  wait-for-change
   24  key down
   25  wait-for-change
   26  key down
   27  wait-for-change
   28  settle
   29  shot hub-change-folder-row
   30  key x
   31  wait-for-change
   32  settle
   33  # CHANGE CLOUD FOLDER now opens three independent path rows (#508/#527).
   34  # SAVES FOLDER is focused initially; A opens its editor. Without this
   35  # press the old walk mislabelled the selector as a keyboard.
   36  key x
   37  wait-for-change
   38  settle
   39  shot folder-editor
   40  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/to-manage-cloud-storage.steps

```
    1  # Start: a system or game list, no menu open. End: the CLOUD hub, focus on
    2  # BACK UP TO THE CLOUD.
    3  # START opens MAIN MENU on GAME SETTINGS (its first row; START there again
    4  # would close it). GAME SETTINGS opens on its first row; up lands on BACK,
    5  # then wraps to the last row (PER SYSTEM ADVANCED CONFIGURATION), then
    6  # MANAGE CLOUD STORAGE, the last row of the CLOUD SETTINGS group.
    7  # Assumes no RetroAchievements sign-in: signed in, the MAIN MENU opens on
    8  # its RETROACHIEVEMENTS row (first, above GAME SETTINGS), so the x below
    9  # opens that page and every later press lands wrong (proofs-307
   10  # X-bios-alone on a signed-in guest, 2026-09-28). A signed-in guest
   11  # presses down once before it, or drives the keys itself.
   12  key ret
   13  wait-for-change
   14  settle
   15  key x
   16  wait-for-change
   17  settle
   18  key up
   19  wait-for-change
   20  key up
   21  wait-for-change
   22  key up
   23  wait-for-change
   24  settle
   25  key x
   26  wait-for-change
   27  settle
   28  shot cloud-hub
   29  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/ui-settings-toggle.steps

```
    1  # Start: the system carousel of a REBOOTED VM (awake, nothing open). End:
    2  # USER INTERFACE SETTINGS with its last row -- SHOW RETROACHIEVEMENTS ICON, a
    3  # Settings-backed switch -- toggled and focused. The next B (`z`) closes the
    4  # page and runs GuiSettings::save(): Settings::saveFile() writes
    5  # es_settings.cfg and SystemConf::saveSystemConf() writes system.cfg. KILL13
    6  # (tools/cloud-round-trip) sends that B itself, on the same monitor
    7  # connection as the system_reset that follows it; the harness drops every
    8  # step from the last `key x` on for the walk that changes nothing, so the
    9  # toggle press must stay the last `key x` in this file.
   10  #
   11  # MAIN MENU on ROCKNIX: GAME SETTINGS, CONTROLLER & BLUETOOTH SETTINGS, USER
   12  # INTERFACE SETTINGS, ... -- so START, down, down, A. The page opens on its
   13  # first row (THEME SET); up lands on BACK, up again wraps to the last row.
   14  # On ROCKNIX that is SHOW RETROACHIEVEMENTS ICON: the gun/wheel/trackball/
   15  # spinner rows after it are `#if !defined(ROCKNIX)` (GuiMenu.cpp).
   16  #
   17  # The toggle press takes no re-send: a second press would put the switch
   18  # back, and KILL13 judges itself on whether the switch was recorded, so a
   19  # silently doubled press would read as "the walk never reached the switch".
   20  wake
   21  key ret
   22  wait-for-change
   23  settle
   24  key down
   25  wait-for-change
   26  key down
   27  wait-for-change
   28  settle
   29  key x
   30  wait-for-change
   31  settle
   32  key up
   33  wait-for-change
   34  key up
   35  wait-for-change
   36  settle
   37  shot ui-settings-last-row
   38  key x
   39  wait-for-change 12 0
   40  settle
   41  shot toggled
   42  
```

## file, whole, at 8ebaf8daad: tools/vm-walks/wake.steps

```
    1  # Start: anywhere. End: the same place, awake.
    2  # After five idle minutes the first key only wakes the screensaver, so the
    3  # first key of a walk is eaten unless a key EmulationStation ignores spends
    4  # that press first. `wake` sends `shift` -- which the interface ignores --
    5  # and then settles, so it costs about a second on a screen that was already
    6  # awake and waits for the interface to come back on one that was not.
    7  wake
    8  
```

## read-only context, from next: .claude/rules/vm-first.md

```
    1  ---
    2  description: "Before any test, build proof or measurement: can this be done on the VM? Written down, answered, and only a reasoned no moves it elsewhere."
    3  ---
    4  
    5  # Can this be done on the VM?
    6  
    7  *No `paths:` glob, so this file loads every session: the question is asked
    8  before a test is written, which is before there is a file to match.*
    9  
   10  Maintainer, 2026-09-11: *"we should always ask the question: 'Can this be done on
   11  the VM?' Only if the answer is no should we move elsewhere."* Binding (D-QA-007,
   12  D-QA-015, D-QA-017). This file exists so the question is asked every session, by
   13  every agent, before every proof -- not remembered by one.
   14  
   15  ## The question, and where the answer goes
   16  
   17  Before a test, a measurement, a screenshot, a fixture, a reproduction or a proof
   18  of any kind, write the question and its answer **in the issue the work belongs to**
   19  (or the work log when there is no issue):
   20  
   21  > Can this be done on the VM? **Yes** -- <how>. / **No** -- <the one thing only a
   22  > device or a person's account can show>.
   23  
   24  **A synthetic input is named, and keeps its checkbox partial (audit #258, P-05).**
   25  When the VM cannot produce the real input -- a core that rotates, a process
   26  whose core exceeds the cap, a hotkey from a pad -- and the proof feeds a
   27  substitute (a hand-appended `SET_ROTATION` line, `/dev/zero` through the
   28  keeper, a command through the API where a button was meant), the tick names
   29  the substitute and the checkbox stays `- [ ]` with that note until a real input
   30  has been seen once, on the VM or on a device with its yes. Blindspot 8's rule
   31  (an assertion that only holds because nothing had happened yet) applied to
   32  the tick: a proof of the path is not a proof of the input.
   33  
   34  **And the criterion itself is written for an agent (D-QA-044).** The checkbox
   35  names the artifact that ticks it; a device checkbox names the fact and points at
   36  its row in `docs/releases/device-facts.md`; `tools/box-check` fails the rest
   37  (`issue-tracking.md` § A criterion is agent-first). D-QA-043 asked the same
   38  from this file's side -- is a frame at the panel's size the observation? --
   39  and is answered by D-QA-044.
   40  
   41  A "no" names a physical fact the GENERIC_X64 guest cannot have: a real panel's
   42  scaling, a board's DRAM surviving a reset, a battery, a GPU driver's exit path, a
   43  bootloader on a given board. **"A real provider" is not a no**: the build host
   44  runs WebDAV, S3, SFTP, SMB and FTP backends of its own (`tools/cloud-test-backend`,
   45  #133) and a VM guest can sign in to a hosted QA account. **"It already has the
   46  history" is not a no**: `upgrade-and-install.md` says how the VM gets it.
   47  
   48  For cloud qualification, D-QA-058 makes WebDAV, SFTP and local MinIO/S3 the
   49  standing baseline. Hosted accounts and offsite endpoints are optional; their
   50  absence does not hold a candidate or turn a local protocol test into a device
   51  test. Keep authenticated provider observations explicitly separate. The
   52  RetroAchievements award/reconnect proof is a different acceptance criterion.
   53  
   54  ## What the VM has
   55  
   56  The GENERIC_X64 image runs the same busybox, scripts, EmulationStation binary,
   57  fonts and 640x480 panel size as a handheld; `tools/vm-pair` gives two guests on
   58  one cloud; `tools/cloud-test-backend` the endpoint (and a dead port for
   59  failures); `tools/vm-qa` the runner with its four suites; `tools/vm-visual-qa`
   60  the frames and the walks; `tools/emulator-exit-test` the exit hotkey; the
   61  `.update` path an in-place upgrade. Anything these cannot reach is a gap in
   62  them to name and, usually, to close -- not a reason to reach for a device.
   63  
   64  ## When the answer is no
   65  
   66  Then, and only then, `engineering-practices.md` § "Nothing runs on a person's
   67  device without their yes" (D-QA-015): the device run is asked for by name, with
   68  what it shows, writes, sends and leaves behind -- including what the device's own
   69  automation (game-exit sync, startup sync, set-aside pruning) will do in response
   70  -- and it runs only on the yes, scoped to exactly the fact the VM could not show.
   71  A dedicated QA handheld with QA-only accounts (D-QA-016, #131) is the standing
   72  answer for the recurring "no"s; the maintainer's device is not a test bench.
   73  
   74  ## Why this file
   75  
   76  On 2026-09-11 a session ran the exit test and a provider proof on the
   77  maintainer's RG35XX SP and their Dropbox. Asked afterwards, the honest answer
   78  was that the forms needed no device at all, the exit path had a small real gap
   79  that could have waited, and the provider proof's gap was an account, not the
   80  VM. One of the runs made the scripts prune a set-aside folder of the
   81  maintainer's own saves (blindspot 38, #130, #132). The question, asked and
   82  written first, would have stopped all three.
   83  
```

## read-only context, from next: .claude/rules/generic-x64-vm-testing.md

```
    1  ---
    2  description: "How to build-test and QA the GENERIC_X64 (x86_64) VM image locally in QEMU/KVM."
    3  paths:
    4    - "projects/ROCKNIX/devices/GENERIC_X64/**"
    5    - "projects/ROCKNIX/packages/**"
    6    - "scripts/mkimage"
    7    - "scripts/image"
    8    # The harness is most of this file and none of it lived under the globs
    9    # above, so a session editing the runner, a walk or the QA endpoint had the
   10    # rule out of context (#147, 2026-09-12).
   11    - "tools/vm-qa"
   12    - "tools/pixelelated-vm-cloud-boundaries"
   13    - "tools/vm-serial"
   14    - "tools/vm-pair"
   15    - "tools/vm-stop"
   16    - "tools/vm-stop-test"
   17    - "tools/vm-manager-system-check"
   18    - "tools/vm-visual-qa"
   19    - "tools/vm-walks/**"
   20    - "tools/cloud-test-backend"
   21    - "tools/emulator-exit-test"
   22    - "tools/time-to-play"
   23    - "docs/vm-qa-log.md"
   24  ---
   25  
   26  # GENERIC_X64 local VM QA
   27  
   28  GENERIC_X64 is the x86_64 VM/QA target (fork issue #16): boot the image in QEMU so devs can
   29  test features (e.g. EmulationStation) without flashing hardware. The bare-metal x64 path and
   30  its concessions (llvmpipe vs hw GL, skipped cores) are tracked separately in issue #17.
   31  
   32  ## When to use it: first, whenever it can answer the question
   33  
   34  Maintainer's rule (2026-09-06, `engineering-practices.md`): anything the VM can
   35  test, it tests first. That is most things — config migrations, refusal paths,
   36  archive naming, every script under `projects/ROCKNIX/packages/network/rclone/`,
   37  the interface's strings and pages (`tools/vm-visual-qa` renders them), and the
   38  cloud paths against `tools/cloud-test-backend`. What it cannot answer is
   39  listed in that rule; everything else comes here before a handheld.
   40  
   41  ## Build
   42  
   43  Detached build from the worktree (the `.git` mount is **required** — a worktree's `.git` is a
   44  file pointing outside the mounted dir, and `scripts/image` runs `git rev-parse`):
   45  
   46  ```bash
   47  make docker-GENERIC_X64 \
   48    DOCKER_EXTRA_OPTS='-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git -v /workspace/cache/rocknix-sources:/workspace/repos/rocknix.worktrees/generic-x64/sources'
   49  ```
   50  
   51  **Both mounts, every time.** The worktree's `sources/` is not a directory of
   52  ours: it is the root-owned mount point Docker left behind, so a build
   53  without the second mount dies in its first minute with `mkdir: cannot create
   54  directory '.../sources/kernel-firmware': Permission denied` under a headline
   55  naming whichever package came first (`install kernel-firmware:target has
   56  failed`, 2026-09-12). The shared cache is `SOURCES_DIR` for every build root
   57  (`device-builds.md`).
   58  
   59  Image lands at `target/pixelelated-GENERIC_X64.x86_64-<build-identity>-from-ROCKNIX.img.gz`; see `docs/releases/versioning.md` for version/timestamp/hash identity. To re-image after a
   60  scripts/only change (e.g. `mkimage`), remove `build.*/.stamps/image/build_target` first —
   61  scripts aren't in a package deephash so the image won't rebuild otherwise.
   62  
   63  **The image step writes into the tree.** It regenerates
   64  `documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md`,
   65  a tracked file, so every build leaves the worktree dirty and
   66  `tools/fork-worktree sync` refuses it afterwards (it names the file). Discard
   67  it before syncing — `git -C <worktree> checkout -- documentation/` — it is
   68  build output, not a change to keep. A build started from an unsynced
   69  worktree builds the old pin and says nothing; check `git log -1` in the
   70  build worktree against `next` before `make`.
   71  
   72  ## Boot in QEMU
   73  
   74  **Environment parity is the acceptance criterion.** A qcow2 only carries disk bytes; it does
   75  not carry CPU, RAM, firmware, disk bus/sector geometry, GPU, network, audio, input, or serial
   76  configuration. Never treat a bootable qcow2 alone as the finished developer artifact.
   77  
   78  The versioned source of truth is
   79  `projects/ROCKNIX/devices/GENERIC_X64/vm/profile.json`. The adjacent `generic-x64-vm` tool
   80  generates both:
   81  
   82  ```bash
   83  VM_TOOL=projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm
   84  $VM_TOOL run target/ROCKNIX-GENERIC_X64.x86_64-<date>.qcow2
   85  $VM_TOOL utm target/ROCKNIX-GENERIC_X64.x86_64-<date>.qcow2 \
   86    --output target/ROCKNIX-GENERIC_X64.x86_64-<date>.utm.zip
   87  ```
   88  
   89  The baseline is Q35 + UEFI, **Haswell-v4** (the oldest fixed QEMU model satisfying this
   90  image's `x86-64-v3` build requirement), 4 vCPUs, 8 GiB RAM, 16 GiB VirtIO disk with explicit
   91  512-byte sectors, `virtio-gpu-gl-pci`, VirtIO network, Intel HDA, USB 3, and a serial console.
   92  Linux uses KVM when available; UTM necessarily uses QEMU TCG to emulate x86_64 on Apple
   93  silicon. Acceleration differs, but the guest-visible CPU model and devices come from the same
   94  profile. VirtualBox is not the common layer because its Apple-silicon build only runs Arm
   95  guests; it cannot run this x86_64 image.
   96  
   97  First boot resizes storage and reboots; the second boot is the real one. Release artifacts:
   98  `.utm.zip` for macOS/UTM and `.qcow2` + the generated launcher for Linux/QEMU.
   99  
  100  ## Headless, on a build host with no desktop
  101  
  102  `virtio-gpu-gl-pci` refuses `-display none`, a bare `-display none` captures
  103  black, and SSH is off on a fresh image — three separate discoveries that are
  104  now one flag:
  105  
  106  ```bash
  107  VM_TOOL=projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm
  108  $VM_TOOL run --headless --daemonize target/ROCKNIX-GENERIC_X64.x86_64-<date>.qcow2
  109  #   virtio-gpu-pci, -display none, -vnc 127.0.0.1:9 (a committed scanout for
  110  #   screendump), the serial console on /tmp/rocknix-qemu-serial.sock, a
  111  #   pidfile at /tmp/rocknix-qemu.pid, and QEMU returns once the VM is up
  112  tools/vm-serial wait                          # until EmulationStation is running
  113  tools/vm-serial sh 'df -h /storage'           # a root shell line, its output back
  114  tools/vm-serial script setup.sh               # a whole file, uploaded and run
  115  kill "$(cat /tmp/rocknix-qemu.pid)"           # stop it -- by PID, never by pattern
  116  ```
  117  
  118  The qcow2 comes from the raw image the same way every time: `gunzip -c
  119  <img.gz> > vm.img && qemu-img convert -f raw -O qcow2 vm.img vm.qcow2 &&
  120  qemu-img resize vm.qcow2 16G` (the 16 GiB is not optional; see below). First
  121  boot resizes storage and reboots itself; `vm-serial wait` returns on the
  122  second boot, twenty to thirty seconds in.
  123  
  124  **Tools that speak SSH** (`tools/cloud-round-trip`): `sshd` on the image is
  125  disabled but running, root login permitted, and there is no `/root` — the
  126  home is `/storage`. One serial command provisions a key and the profile's
  127  forward does the rest:
  128  
  129  ```bash
  130  tools/vm-serial sh "mkdir -p /storage/.ssh && chmod 700 /storage/.ssh && echo '$(cat key.pub)' >> /storage/.ssh/authorized_keys && chmod 600 /storage/.ssh/authorized_keys"
  131  ssh -i key -p 10022 -o StrictHostKeyChecking=no root@127.0.0.1 'echo ok'
  132  ```
  133  
  134  **`get_setting` and `set_setting` are shell functions, not files.** They come
  135  from `/etc/profile.d/001-functions`, which a non-interactive ssh shell never
  136  sources, so a fixture that runs `set_setting` over `vm-pair ssh` gets
  137  `command not found` on stderr and a silent no-op on stdout. The upgrade
  138  rehearsal of 2026-09-20 seeded a setting that way, asserted nothing about it,
  139  and reported the image had lost it after the update; the image had never been
  140  given it. Prefix guest commands with `. /etc/profile >/dev/null 2>&1;` and
  141  assert the read-back *before* the step under test, so the fixture's own
  142  failures cannot be booked to the build.
  143  
  144  **Two guests, one cloud (D-QA-009).** A conflict is a change on both sides
  145  since they last agreed, and one guest cannot make one; a handheld must
  146  never be asked to. `tools/vm-pair up <img.gz>` builds two disks from the
  147  image, boots both headless — guest `a` on the defaults above, guest `b`
  148  with a `-b` suffix on its sockets, SSH 10023, VNC :10 and its own MAC — and
  149  provisions the QA key in each over serial; `vm-pair ssh a '…'`, `vm-pair serial b
  150  '…'`, `vm-pair info`, `vm-pair down`. Both reach the host's backend at
  151  `10.0.2.2`, so the pair against `cloud-test-backend` is the venue for every
  152  fixture that manufactures a conflict or interrupts a transfer, run once on
  153  WebDAV and once on MinIO.
  154  
  155  **The pair through the harness.** `tools/cloud-round-trip --host
  156  root@127.0.0.1 --port 10022 --second-port 10023 --identity
  157  /tmp/rocknix-vm-pair/qa-key` runs the single-device suite on `a`, then the
  158  two-device fixtures of #35 (`--only A1,A9` for a subset; `--only CONTRACT
  159  --transport bisync` for #9's items, `--bisync-flags` for Gate 11's variants);
  160  both guests are put back on every exit. Scripts fixed on the host ride in
  161  `/tmp/qa-bin` on both guests through `--path-prefix`; the pair's `up` does
  162  not put them there.
  163  
  164  **Two guests must be two devices (#91).** `cloud_device_id` hashes the
  165  permanent MAC, and `generic-x64-vm` gives every guest the profile's fixed
  166  one, so two guests from one image printed one id between them
  167  (`GENERICX64-15ca35b6b4` on both, 2026-09-08) — one settings folder, one
  168  manifest, and pair fixtures agreeing with themselves. `vm-pair up` now
  169  starts `b` with `--mac 52:54:00:52:4E:59` (the profile's plus one; `a`
  170  keeps `…:58`, so its id does not move), and the harness reads both ids
  171  before it prepares either guest and refuses the two-device fixtures when
  172  they match or either is blank — nothing is written, so nothing needs
  173  putting back. The rewrite it used to do (`<id>-second` on `b` for the run)
  174  is gone: it ran every pair fixture on an identity the harness had invented.
  175  A pair started before this keeps its shared id until `vm-pair up` rebuilds
  176  the disks — the id is derived from the address on first boot and then
  177  stored, so clearing `b`'s stored id while the MACs match re-derives the
  178  same one. A11 alone clones `a`'s id onto `b`, on purpose, and puts it back;
  179  a run interrupted inside A11 leaves that clone behind, and the refusal's
  180  message tells the two cases apart by the MACs. The harness's stdout is block-buffered
  181  when redirected, so a run in the background shows nothing until it ends —
  182  wait for the `PASSED` / `N CHECK(S) FAILED` line rather than reading the
  183  file early.
  184  
  185  **Busybox `pgrep -x` compares the whole argv, not the comm.** On the guest
  186  `pgrep -x retroarch` returns 1 while `/usr/bin/retroarch` runs (its argv[0]
  187  is the full path); `pgrep -x emulationstation` happens to work because ES is
  188  started by its bare name. Match a process by a bracketed fragment of its
  189  path — `pgrep -f '/usr/bin/retroarc[h]'` — and kill by name with `killall`,
  190  which is what `input_sense` does. The bracket protects only the pattern's
  191  own literal: a `pkill -f 'f1-liv[e].sh'` still killed the shell running it
  192  because the same command line carried `rm -f /tmp/qa-bin/f1-live.sh`. When
  193  a command both matches and names the thing, put it in a script file and
  194  run the file (2026-09-08, twice in one hour; the reviewer hit it the same
  195  day with `pkill -f 'sleep 30'`).
  196  
  197  **Stop it by PID.** `pkill -f 'vm76[.]qcow2'` killed the shell that ran it,
  198  because the same command text held the literal in an `rm` three lines down,
  199  and `bash -c` carries the whole script in its argv. The pidfile exists so
  200  that this never has to be a pattern.
  201  
  202  **A stop waits for exit before the next start (#454).** TERM is a request,
  203  not evidence that QEMU has released its disk or VNC port. `vm-pair` uses
  204  `tools/vm-stop`: verify the exact owned disk, hold a pidfd, signal that
  205  process, await exit boundedly, then remove the pidfile. A wrong owner or
  206  timeout fails and keeps the pidfile. `tools/vm-stop-test` covers delayed
  207  exit/port reuse, wrong-process/disk refusal and timeout. A scoped continuation
  208  may use an independent, compared copy of an actual upgraded disk; retain the
  209  failed predecessor's result and original disk rather than relabel its run.
  210  
  211  **Socket paths under 107 bytes.** A session scratch directory is longer than
  212  that, and a longer path fails to bind with an error that names nothing. The
  213  tool refuses one.
  214  
  215  **A handheld's panel size is a flag.** `run --headless --res 640x480 …`
  216  appends `xres=640,yres=480` to the virtio-gpu device (desktop and headless
  217  alike), the guest's DRM takes it as the preferred mode, and EmulationStation
  218  renders at it; without the flag the guest is QEMU's 1280×800 as before (#97).
  219  So the 640×480 look of the picker rows and the transfer page (#85, #95, #94)
  220  is a VM check first and a handheld confirmation second (D-QA-007): walk it at
  221  1280×800, then again with `--res 640x480`; `tools/vm-visual-qa` and the
  222  walks need no change, a `screendump` simply comes back at the guest's size.
  223  
  224  **Cutting the guest's link (fault injection, #103).** `tools/vm-serial sh 'ip
  225  link set eth0 down'` cuts it; `... up` restores it. Serial is the only channel
  226  that survives the cut: the host's forwarded SSH arrives from `10.0.2.2` like
  227  everything else, so it goes with the link -- and it does not *die*, it
  228  **stalls**, because an admin-down does not reset an established TCP
  229  connection, so a command over a `ControlMaster` blocks for the whole outage.
  230  Close the master before the cut (`ssh -O exit`) and go back over SSH only once
  231  serial confirms the network. Inside the guest the routes vanish at once (a
  232  fresh connection fails in 20 ms, `network is unreachable`; rclone does not
  233  retry it), the IPv4 address lingers until NetworkManager notices ~8 s later
  234  and flushes it (`nmcli dev` -> `unavailable`), and in-flight transfers sit in
  235  `ESTABLISHED`. After `up` the address, default route and a ping to `10.0.2.2`
  236  are back in ~0.3 s -- a handheld's Wi-Fi takes seconds to reassociate, so
  237  *test for the return* (`ip -4 addr show eth0 | grep inet && ip -4 route show
  238  default | grep . && ping -c1 -W1 10.0.2.2`) rather than assume it. Read the
  239  interface off `ip -4 route show default` (`eth0` here, `wlan0` on a handheld).
  240  Two things this guest cannot stage: a *silent* black hole (no iptables/nft/tc
  241  on the image), and `ip route del default` does **not** cut the QA endpoint --
  242  `10.0.2.2` sits on the guest's own /24. Established TCP rides a short outage
  243  out and resumes on its retransmit schedule, so an *unbounded* rclone
  244  **completes** after a brief outage rather than hanging; the hang needs an
  245  outage longer than its timeout budget, and the load-bearing signal on a short
  246  one is the exit code and stamp. One backend sharp edge: `rclone serve webdav`
  247  fed a fully-buffered aborted PUT through slirp holds the destination name's
  248  lock and returns `423 Locked` to a re-PUT of the same name for minutes -- a
  249  VM-only artifact (a real provider resets the aborted PUT), so assert
  250  re-upload idempotency for a same-name upload on MinIO/S3 or a device. The
  251  same buffer has a second face since the deliberate run's stall ceiling
  252  (#153): a healthy 12 MiB re-run is taken by slirp at once and drained by
  253  the throttled server for ~40 s, during which rclone's counter reads 100%
  254  and moves nothing, so the ceiling ends an upload that is completing and
  255  the archive is whole afterwards (LINK5 on WebDAV, 4d7eb1f303, 2026-09-13).
  256  The cell SKIPs that signature on WebDAV only (D-CLOUD-128); KILL5's 6 MiB
  257  archive drains inside the ceiling, and on S3 the same re-run has passed.
  258  `tools/cloud-round-trip --only LINK1,...,LINK7 --serial-socket <sock>` does
  259  all of this against the throttled endpoint and refuses unless the console it
  260  holds is the device on `--host` (a nonce written over SSH, read over serial).
  261  The cells are off by default in the suite and skipped with a line when no
  262  serial socket is given, which is every handheld.
  263  
  264  **Lagging the guest's resolver (fault injection, #175).** A hotspot whose DNS
  265  answers seconds after its address is the case the network-up token retry
  266  exists for, and it is reproduced through the image's own override, not by
  267  editing what looks like the file. `/etc/resolv.conf` -> `/run/rocknix/resolv.conf`
  268  -> `/run/systemd/resolve/stub-resolv.conf`: two symlinks, and resolved
  269  regenerates the stub at every link change, so a `nameserver` written through
  270  them is gone the moment the link comes up (which is exactly when the test
  271  needed it). `network-base-setup` copies **`/storage/.config/resolv.conf`**,
  272  when present, into `/run/rocknix/resolv.conf` as a regular file at boot and
  273  nothing touches it afterwards. So: write `nameserver 127.0.0.1` there before
  274  the boot -- nothing listens, `getent`/curl fail in a millisecond with `Could
  275  not resolve host` -- and to end the lag remove the override and put the
  276  symlink back (`rm -f /storage/.config/resolv.conf /run/rocknix/resolv.conf;
  277  ln -sf /run/systemd/resolve/stub-resolv.conf /run/rocknix/resolv.conf`). The
  278  override is a supported user setting, so leave the guest without it. ES logs
  279  to `/var/log/es_log.txt` (`/var/log` is `/storage/.cache/log` bind-mounted by
  280  `var-log.mount`, the same files under either path); there is
  281  no `es_log.txt` under `/storage/.config/emulationstation/`, and a `grep -c`
  282  on that path over serial returns an error line whose digits are none, which
  283  `tr -dc '0-9'` turns into an empty count -- a FAIL that names the harness.
  284  
  285  ## The guests render in hardware, and the frames come over VNC (#291)
  286  
  287  Until 2026-09-26 every QA guest rendered with Mesa's **softpipe**: the
  288  image's options had said `LLVM_SUPPORT="yes"` for llvmpipe since the device
  289  was added, and `config/graphic` reset it to `no` before Mesa read it, so
  290  the interface, the compositor and RetroArch all drew on the CPU through the
  291  slowest software rasterizer -- RetroArch dropped six frames in ten, its
  292  udev poll could stall past a 100 ms key press (the #249 proof's misses),
  293  and the walks took twenty-two minutes. Nobody had read the renderer line;
  294  the options comment was taken as the behaviour.
  295  
  296  Two things changed, and both are the default now:
  297  
  298  - **`generic-x64-vm --headless` puts the guest on hardware GL through
  299    virgl** (`--gl auto`): `virtio-gpu-gl-pci` with `-display
  300    egl-headless,rendernode=<node>`, the node the first `/dev/dri/renderD*`
  301    whose driver is not `nvidia` (virglrenderer wants Mesa's EGL; on the
  302    build box that is the Intel iGPU, `renderD128`, with the RTX A1000 on
  303    `renderD129` under the proprietary driver). The image's Mesa carries the
  304    virgl driver, so RetroArch reports `Renderer: virgl (Mesa Intel(R)
  305    Graphics (ARL))` and drops one frame in two thousand. `--gl none` (or
  306    `VM_GL=none` through `vm-pair`) is the software path; the image also
  307    carries **llvmpipe** now for that path (the `config/graphic` reset keeps a
  308    device's explicit yes).
  309  - **The monitor's `screendump` has no surface under a GL scanout** (QEMU
  310    answers `Error: no surface`; the frame is a texture the console never
  311    reads back). `vm-visual-qa`'s `Monitor.screendump` -- and so `frame`,
  312    `shot`, every walk, `time-to-play`, `ra-offline-test`'s frames and
  313    `cloud-round-trip`'s walk steps -- takes the frame over the guest's VNC
  314    display instead, the server `info vnc` names, as the same P6 file; once
  315    seen, VNC is used for the rest of the session. The RFB client is in the
  316    tool, standard library only, raw encoding, about 0.1 s a frame at 640x480.
  317  
  318  `vm-qa`'s report says which display the guest had (`display: GL through
  319  virgl on /dev/dri/renderD128`, read from QEMU's own command line) and which
  320  renderer its Mesa reported (`renderer: virgl (...)`, from the launch log the
  321  exit suite leaves). A report that reads `softpipe` is a guest on the wrong
  322  path, whatever the options say. Hardware rendering moves pixels against the
  323  accepted walk baseline once; that accept is named in `docs/vm-qa-log.md`.
  324  
  325  ## A launch, a START or a walk waits for the interface to be idle (D-QA-057)
  326  
  327  `GET http://127.0.0.1:1234/isIdle` answers `[ true ]` with 200 only when no
  328  hasher, scraper, content installer, updater or game is running; while any of
  329  them runs, `POST /launch` answers 200 and starts nothing, and a page may still
  330  be loading. After a reboot with new ROMs the hasher runs for seconds to a
  331  minute on guest d. So a proof's reboot helper waits for `/isIdle`, for the
  332  startup sync's card to go and for a still screen before the script walks, and
  333  a launch through the API waits for `/isIdle` and dismisses dialogs first
  334  (`proofs-307/common.sh`, `tools/ra-offline-test`). A wait that expires says so
  335  in the log; a longer sleep is never the fix (blindspot 64).
  336  
  337  ## Driving EmulationStation from the monitor
  338  
  339  The keys the image maps (`/storage/.config/emulationstation/es_input.cfg`,
  340  read it on the guest rather than trusting this): **START = `ret`, A = `x`,
  341  B = `z`, X = `s`, Y = `a`, SELECT = `shift_r`**, arrows for direction. The
  342  things that cost a cycle each before they were written down:
  343  
  344  - **A page opens on its first row, and `up` from there lands on its BACK
  345    button** — the wrap runs rows → buttons → rows. So the bottom of GAME
  346    SETTINGS is three `up`s from the top (BACK, the last row, the one above),
  347    not one. The button bar is a focus stop on every page.
  348  - **Keep a BusyBox applet's invocation path separate from its binary identity.**
  349    Hash the resolved executable, but invoke the original installed applet path
  350    (or explicitly name its applet); `realpath unshare` may be `busybox`, whose
  351    argv then has different meaning. Check the installed help before borrowing
  352    util-linux flags. A private namespace fixture still owns timeout, descendant
  353    termination and reaping; dropping an unsupported flag alone is not cleanup
  354    proof (#579/#581, October13).
  355  - **Native text editors receive printable keyboard keys as text.** A monitor
  356    `z` can type a character instead of acting as the mapped controller Back.
  357    For a keyboard-driven `GuiTextEditPopupKeyboard` cancellation, use `esc`
  358    after verifying that exact editor handles `SDLK_ESCAPE`; retain a returned
  359    picker frame and a no-connect/no-write receipt. Controller input remains a
  360    separate path. A generic frame-change retry must not repeat printable
  361    characters into a field (#577, October13).
  362  - **START on MAIN MENU closes it.** START opens the menu from a system or
  363    game view; on the menu it is CLOSE. Sending it twice returns to where you
  364    were, and the next `x` launches whatever is under the cursor.
  365  - **After five idle minutes the first key only wakes the screensaver.** Send
  366    `shift` first — a key the interface ignores — or the walk starts one key
  367    late and every later press lands one screen off.
  368    This holds when you "know" the state: a walk composed without `wake.steps`
  369    because the previous walk had ended on the carousel five minutes earlier
  370    lost its first key to the screensaver, entered a game list on the second,
  371    and launched a game twice (2026-09-10). Wake first, every time, and begin
  372    from a frame, not from memory.
  373  - **`x` on a switch row toggles it; B closes the page and runs its save
  374    function.** So "flip a switch and see the effect" is `x`, `z`, then reopen.
  375  - **A transfer page ends on PRESS ANY BUTTON TO CLOSE and returns to the hub**
  376    with focus where it was, not to the transfer page.
  377  - **Do not time a page; watch it.** A frame taken early is the previous
  378    screen, and it reads as "the key did nothing". `settle` before every
  379    `shot` and `wait-for-change` after every press replace the old advice
  380    (2 s after a page opens, 7 s after one that scans the cloud), which was
  381    right on an idle host and wrong on a building one.
  382  - **A restarted EmulationStation comes back on the last game list, not the
  383    carousel.** `systemctl restart emustation` (and ES's own restarts) restore
  384    the list that was open -- TOOLS, MUSIC PLAYER, whatever the previous walk
  385    left -- so a walk that assumes the carousel starts one screen deep, and its
  386    `x` presses launch things: on 2026-09-09 one such run started the File
  387    Manager (`foot` + `commander.sh`) and every later key went to it. Only a
  388    full reboot lands on the carousel. After a restart, send one `z` (B) and
  389    read a frame before driving anything; when a frame shows a game list, that
  390    one B is the whole fix. A launched tool is killed by pid over SSH
  391    (`pgrep -a foot`), never by pattern, and ES then shows `UKNOWN ERROR : 230`
  392    (upstream's spelling) that one `x` dismisses.
  393  - **After an ES restart, `screendump` can serve the previous ES's last frame
  394    for half a minute or more.** Frames captured 7-34 s after a restart still
  395    showed the old hub page with its old clock, while the new ES was already
  396    running and its startup sync had come and gone. The surface caught up once
  397    keys were sent. A full `reboot` does not have the problem: capture
  398    continuously from about 15 s after issuing it and the boot-time card is in
  399    the frames (`SYNCING SAVES AT STARTUP` at t+25 s, `COMPLETED SUCCESSFULLY`
  400    at t+27 s on 2026-09-09). Note that on a fresh boot the guest clock reads
  401    from the RTC until NTP corrects it, so log timestamps from the first minute
  402    lag real time by up to a minute (blindspot 32); order by uptime, not by
  403    the clock.
  404  - **A serial or SSH command that hangs on `set_setting` is waiting on
  405    `/tmp/.system.cfg.lock`, and since #98 that means a live holder.** Until
  406    2026-09-09 `wait_lock` spun with no timeout and never checked whether the
  407    pid in the file was alive; one `set_setting cloudsaves.startup 1` took
  408    4 min 43 s after a tool had been killed from outside. It now removes a lock
  409    whose pid is dead (or whose file is empty or not a pid) and retries at
  410    once, and after 30 s of one live holder logs its pid once. So on a build
  411    that carries it, `journalctl -t wait_lock` names the holder to look at;
  412    on an older build, read the pid in the file and `kill -0` it yourself.
  413    `tools/wait-lock-test` proves both behaviours against any copy of
  414    `001-functions`.
  415  - **`vm-serial wait` returns at once if an ES is still up.** Right after
  416    `reboot` the old EmulationStation is still running for several seconds, so
  417    "ready after ~0s" means nothing; check that `uptime` has reset first.
  418  - **A press count is a claim about the page's order, and the manager's
  419    order moves.** The SAVE STATE MANAGER sorts its tiles by slot under DO NOT
  420    INCREMENT and by date, newest first, under INCREMENT PER SAVE
  421    (`GuiSaveState.cpp:239`), so "two rights is SLOT 1" was true on one run and
  422    landed on AUTO SAVE the next, once a save had changed the dates. Arrange
  423    the files so the tile you want is the last one and press past the end (the
  424    grid does not wrap), or read the selection from a frame before A; and let
  425    the proof read back what was launched (`-e <slot>`, the appendconfig)
  426    rather than trust the presses (#209, 2026-09-23).
  427  - **A screen that looks like the previous one is not proof the key was
  428    ignored.** Check `pgrep emulationstation` before re-driving input — an
  429    abort()ed ES restarts to the carousel, which looks the same.
  430  
  431  - **Wait for the frame, not for the clock.** Since #125 the walk steps are
  432    `settle` (until the screen holds still) and `wait-for-change` (until the
  433    last key has visibly landed), and every file in `tools/vm-walks/` is
  434    written on them. A fixed `wait N` between presses is a guess about a host
  435    that is also building: a press a second after a screen change is
  436    regularly eaten, and the rest of the walk then runs one screen out of
  437    phase. `wait-for-change` re-sends the eaten press once and then fails the
  438    walk naming the key and the line, so the wrong-screen frames are never
  439    produced at all.
  440  
  441  `tools/vm-visual-qa` writes PNG with the stdlib, so the frames are readable by
  442  anyone without Pillow. Read them; a walk whose frames nobody read has tested
  443  nothing. Reusable walks live in `tools/vm-walks/` — compose them with `cat`,
  444  or name the composition in `tools/vm-walks/suite.txt`, which is what
  445  `tools/vm-qa --only walks` replays (`--guest b` to drive vm-pair's second
  446  guest).
  447  
  448  ## Frame at the handheld's size, not only the pair's
  449  
  450  vm-pair's guests run at 1280x800. The maintainer's handhelds are 640x480,
  451  and two things differ under 720 px that 1280x800 never exercises:
  452  `Font::get` scales every requested size by 1.31 (1.5 under 320), and
  453  full-screen menus are on, so the window draws no help bar under a second
  454  page. #27's first cut was right at 1280x800 and truncated every label at
  455  640x480; four cuts were each caught by a 640x480 frame and none would have
  456  been caught at the pair's size (blindspot 41).
  457  
  458  So a UI change is framed at 640x480 before it is called done. A small guest
  459  beside the pair is one QEMU command: the pair's arguments with `-device
  460  virtio-gpu-pci,xres=640,yres=480`, its own disk from the same image, its own
  461  ports and sockets (`-d` suffix, SSH 10026, MAC `52:54:00:52:4E:5B`, VNC :12),
  462  the QA key written over serial with `tools/vm-serial`. **Its disk lives in
  463  its own directory on the disk-backed workspace** (`/workspace/tmp/rocknix-vm-d`),
  464  never in vm-pair's and not on `/tmp`. `/tmp` is a 31 GB tmpfs: a raw image is
  465  4.3 GB, each guest disk 2 GB, and a disk deleted under a running guest still
  466  counts until that guest exits. Two conversions at once ran it out of space
  467  and truncated both new disks silently -- 0.9 GB and 1.8 GB where 2.2 GB was
  468  right -- so the guests booted to the firmware's boot menu (2026-09-13, twice
  469  before the cause was found). Check `df /tmp` before a second conversion, and
  470  never in vm-pair's directory: `vm-pair up`
  471  begins with `rm -f "$DIR"/vm-*.qcow2`, so a third guest kept there loses its
  472  disk under it the moment the runner starts and boots into the firmware's
  473  "select boot device" menu, while its own conversion disturbs the pair's
  474  (2026-09-13, both at once). The session scratchpad's `rebuild-d.sh` does the
  475  rest and reboots the guest seeded with a NES ROM and three save states;
  476  making it a `vm-pair` guest is open. Read the small frame first: at that
  477  size a label that fits is the finding, and a bar that is missing is one too.
  478  
  479  ## Driving EmulationStation blind: what the 2026-09-21 walks taught
  480  
  481  Twenty-three checklist items were walked on guest d in one night; about a
  482  third of the walks landed somewhere other than intended. Every miss had the
  483  same shape -- a step count that assumed a starting state the interface did
  484  not have -- and each is now a rule for the next steps file:
  485  
  486  - **`dismiss-dialogs` ends on the carousel where it was**, not on the first
  487    system. Read the carousel frame before counting presses from it.
  488  - **The navigation bar (B on the carousel) opens on the current system's
  489    group** (NES -> NINTENDO), with four rows that wrap. So "SYSTEM" is one
  490    down from NINTENDO, two down from LEXALOFFLE, one *up* from COLLECTIONS.
  491    Shot the bar, then count.
  492  - **A on a game with save states opens the SAVE STATE MANAGER**, not the game;
  493    A again on START NEW GAME launches. A on a Tools entry launches the tool
  494    (the File Manager took a walk meant for NES; `pkill -x mc` over serial).
  495  - **The main menu's RETROACHIEVEMENTS row exists only with
  496    `RetroachievementsMenuitem` on** (a Settings bool) plus the toggle and a
  497    username; otherwise the entry lives under GAME SETTINGS. And ES reads the
  498    account at start: an account set while ES runs needs a **reboot** -- not a
  499    restart -- before the row appears and the login happens (a restarted ES
  500    also leaves the screendump stale, per the memory).
  501  - **`set_link net0 off` on the monitor is the link cut**; confirm with
  502    `cat /sys/class/net/eth0/carrier` over serial (0) before the first key.
  503    The proxy's `online_state.json` lags a few seconds behind the carrier.
  504  - **RetroArch quits on Esc twice** from the keyboard here; F8 did not take a
  505    screenshot (`input_screenshot` is unset; the hotkey enable is a pad
  506    button), so #82 on the VM is a file dropped into `/storage/roms/screenshots`
  507    during a session, not a key. **Esc twice is not dependable**: on
  508    2026-09-25 (`664ad9ac64`, GL, `quit_press_twice = "true"`) two presses 1 s
  509    and 0.4 s apart left RetroArch running. The exit hotkey's own
  510    `execute_kill`, extracted from `input_sense` the way `tools/ra-offline-test`
  511    does, quits it cleanly and writes the auto save -- use that, and read
  512    `pgrep -f ^/usr/bin/retroarch` after, not the screen.
  513  - **Redact the QA account's name** from any frame before filing (the summary
  514    title, the login toast): `docs/qa-frames/.../README.md` says where the painted band is.
  515  - **`scp` takes `-P` for the port**; `ssh -n` closes stdin, so a heredoc to a
  516    guest file needs a plain `ssh`. Both cost a walk each.
  517  
  518  ## A cut link is not the only way to be offline
  519  
  520  `set_link net0 off` on the monitor is the fixture every offline proof used,
  521  and it fails a name lookup at once: no route, `Network is unreachable`, the
  522  proxy's probe answered in milliseconds. A handheld goes offline the other
  523  way as often -- still associated to a hotspot whose uplink has gone, or with
  524  a Wi-Fi switch that leaves the interface up -- and then the interface has an
  525  address, a route, and a resolver that waits its full twenty seconds for a
  526  nameserver that never answers. Everything that bounds an HTTP call and not
  527  the lookup (`urlopen(timeout=...)`, curl's timeouts) waits with it. That is
  528  how #242 shipped in three candidates past proofs #190 and #193 that passed:
  529  the offline page had never been opened on a link with a resolver in it.
  530  
  531  So an offline proof runs in both shapes. The second is `repro-242.sh`'s:
  532  keep the address, `ip route del default`, and point `/etc/resolv.conf` (its
  533  `readlink -f`: systemd-resolved's stub) at a black hole with `options
  534  timeout:10 attempts:2`, then confirm over serial that `getaddrinfo` takes
  535  its twenty seconds before the first key. And a setting the fixture changes
  536  from the shell -- the offline toggle through the ctl -- is read by the
  537  interface at its next start only (§ below); reboot before the walk, or the
  538  page decides "toggle off" and asks the web.
  539  
  540  ## What the guest's busybox lacks
  541  
  542  The scripts run on the image, not on the host, and the host's coreutils hide
  543  that. Present: `mapfile` (bash), `stat -c`, `find -path`, `mktemp -d`,
  544  `sort -u`, `flock`, `base64 -d`. Absent: **`comm`**, **`pgrep -c`**,
  545  `find -printf`, `ls --time-style`, `realpath`. `comm ... | wc -l` reading 0
  546  on the image shipped once (2026-09-06, a difference count that said
  547  "identical"); `pgrep -c` prints usage and exits 1, which a `$(...)` reads as
  548  an empty string. And **`pgrep -x` matches the whole command line**, not the
  549  name: `pgrep -x retroarch` reads 0 while `/usr/bin/retroarch -L ...` runs
  550  (2026-09-26, two proofs reported a launch that had happened as one that had
  551  not; the #239 experiment's "RetroArch up: no" was the same). Poll a process
  552  by its argv with a self-excluding bracket, `pgrep -f 'retroarc[h] -L'`, on the
  553  guest and on a handheld alike. When a script reaches for a coreutils name,
  554  run it on the VM before believing the host.
  555  
  556  ## Fixtures for the cloud tier
  557  
  558  `tools/cloud-test-backend` serves a directory to the guest in **five
  559  protocols**, each on its own port so more than one can be up at a time
  560  (#133). The guest reaches every one of them at `10.0.2.2`.
  561  `seed-content` puts the content-tier fixture at the endpoint and
  562  `seed-device` prints the guest half — the remote, the conf, and device ROMs
  563  that pair with the fixture so every verdict a systems page can give has a
  564  system that produces it:
  565  
  566  ```bash
  567  tools/cloud-test-backend up && tools/cloud-test-backend reset      # WebDAV, the default
  568  tools/cloud-test-backend --backend sftp up                         # or any of the five
  569  tools/cloud-test-backend seed-content
  570  tools/cloud-test-backend seed-device > /tmp/seed.sh && tools/vm-serial script /tmp/seed.sh
  571  tools/vm-serial sh '/usr/bin/cloud_content_restore --scan'
  572  ```
  573  
  574  Then read the endpoint after a transfer (`cloud-test-backend ls`), never the
  575  page's COMPLETED SUCCESSFULLY — that is the check that found `MEDIA_EXCLUDES`
  576  being passed to nothing (blindspot 30).
  577  
  578  ### The five backends
  579  
  580  | `--backend` | Port | How it runs | Data under `~/.cache/rocknix-cloud-qa/` | Hashes | Modtimes | A PUT cut in flight |
  581  | --- | --- | --- | --- | --- | --- | --- |
  582  | `webdav` (default) | 9010 | `rclone serve webdav`, a host process | `data/` | no | **no** | leaves a short file |
  583  | `s3` | 9012 | MinIO in a container (`rocknix-cloud-qa`) | inside the container | MD5 | yes | **commits or nothing** |
  584  | `sftp` | 9013 | an unprivileged `sshd`, key auth only | `sftp/data/` | no | yes | leaves a short file |
  585  | `smb` | 9014 | Samba in a container (`rocknix-cloud-qa-smb`) | `smb/data/` | no | yes | leaves a short file |
  586  | `ftp` | 9015 | `pyftpdlib` in a venv, PASV 9060-9069 | `ftp/data/` | no | yes | leaves a short file |
  587  
  588  `caps` prints the last three columns for the selected backend; nothing binds
  589  **9011**, which is the dead port every failure fixture aims at
  590  (`dead-conf` writes the refusing stanza, in whichever field that backend
  591  carries its address).
  592  
  593  **The three shapes a remote path can have**, which is why no caller should
  594  hard-code one: on WebDAV and FTP the folder *is* the path (`/GAMES`); on S3
  595  the first component is the bucket and on SMB the share (`/rocknix-qa/GAMES`,
  596  `/qashare/GAMES`); on SFTP every path is absolute, because an sshd running as
  597  an ordinary user cannot chroot. `endpoint-prefix` states what to strip,
  598  `saves-remote` / `settings-remote` / `content-remote` state what to
  599  configure. A hard-coded `/QA-Custom` is a legal folder on Dropbox and an
  600  illegal *bucket name* on S3.
  601  
  602  **WebDAV is the harshest and stays the default.** With `vendor=other` it
  603  carries neither hashes nor modtimes, so rclone compares by size alone —
  604  which is the shape of #53. The other four all carry modtimes, so a bug only
  605  WebDAV can catch is one WebDAV must keep catching.
  606  
  607  ### What the matrix cannot do here
  608  
  609  - **Hosted-provider behavior is optional follow-up.** D-QA-041/D-QA-058
  610    remove hosted-account and offsite-endpoint dependencies from routine RC
  611    qualification. The standing local baseline is WebDAV, SFTP and MinIO/S3,
  612    using the image's installed rclone and separate reports. SMB/FTP remain
  613    broader local coverage under #133/#232. OAuth/token refresh and an actual
  614    provider-owned authenticated page are not proved by these tests; #463
  615    retains the optional Dropbox observation. No credentials need to be
  616    requested before proceeding. The separate RA award proof is unchanged.
  617  - **WebDAV and S3 can be throttled; the other three cannot.** For WebDAV
  618    `CLOUD_QA_BWLIMIT` is an `rclone serve` flag. For S3 (#151 PL-13,
  619    `96284d5544`) the same variable moves MinIO to loopback 9022 and fronts
  620    9012 with an inline token-bucket proxy shaped like rclone's (4 MiB burst,
  621    one bucket per direction), so the LINK constants calibrated on WebDAV
  622    hold; the host's own rclone bypasses it. `backend_throttled()` reads
  623    `<state>/<backend>.pid` for both. SFTP, FTP and the SMB tier have no
  624    throttle, so the LINK cells still cannot run against them. On S3 the LINK
  625    cells see rclone's S3 backend re-dial through the AWS SDK's backoff for
  626    `--low-level-retries 10` after a cut, which no `--timeout` covers -- the
  627    deliberate `--system-only` run completed 88.8 s after a 40 s cut and
  628    reported success (its own issue).
  629  - **Only S3 can prove an atomic PUT.** Four of the five write into the final
  630    name, so a file cut mid-body reads as truncated; KILL1's torn-file
  631    assertion is asserted on `--backend s3` and skipped, with the reason, on
  632    the rest.
  633  - **The host's rclone is not the guest's** (1.60 here, 1.75 on the image).
  634    Test rclone *behaviour* by running rclone on the guest against the
  635    endpoint, never on the host.
  636  
  637  ## Fixtures for the launch path
  638  
  639  `tools/emulator-exit-test --port <ssh> --identity <key> --vm` (fork-only;
  640  `--vm` swaps RetroArch to the gl driver for the run because the guest has no
  641  Vulkan, never pass it for a handheld). It builds a battery-backed Game Boy
  642  cartridge that writes a known byte, launches it through `runemu.sh` as
  643  `es_systems.cfg` does, and drives the shipped `execute_kill` from the
  644  installed `input_sense`: one press, a held combo, the debounce window on a
  645  target of its own, and the marker's lifetime. Against an `input_sense` with
  646  the debounce stripped it fails in two places (no `.srm`; the repeat went
  647  through), which is what makes it a gate (#117, #120). The exit code is not
  648  the signal -- since #92 a forced quit reads as clean -- the save on disk is.
  649  
  650  ## After every VM cycle
  651  
  652  A cycle that taught something and left it in the work log has taught the
  653  next cycle nothing. Before closing the cycle, sort what it found into:
  654  
  655  1. **A tool or a flag** — anything that was a procedure (a boot recipe, a
  656     fixture, a wait loop) becomes code here or in `tools/`, so it cannot be
  657     skipped by not reading it.
  658  2. **A walk** — any screen reached by hand becomes a `tools/vm-walks/*.steps`
  659     file, so the next cycle replays it.
  660  3. **A line in this file** — a gotcha, a key, a missing applet.
  661  4. **A row in `docs/vm-qa-log.md`** — the cycle itself: what the VM found,
  662     what it could not prove, and which of 1–3 it left behind. The next cycle
  663     starts by reading the last row.
  664  
  665  The work log keeps the narrative; it is not where the next cycle will look.
  666  
  667  ## UTM virtio-gpu cursor sprite
  668  
  669  UTM's virtio-gpu hardware cursor plane can display the **cursor graphic** upside down while
  670  movement and the primary display remain correctly oriented. Do not add a coordinate
  671  calibration or rotate the output—that would break correct pointer movement and UI orientation.
  672  For virtual DRM connectors (`Virtual-*`), `111-sway-init` writes
  673  `WLR_NO_HARDWARE_CURSORS=1` to Sway's environment, forcing wlroots to composite the cursor in
  674  the correctly oriented primary plane. Confirm in `/var/log/sway.log`:
  675  `Loading WLR_NO_HARDWARE_CURSORS option: 1`.
  676  
  677  ## Give the VM enough disk, or the UI silently breaks (16GB+)
  678  
  679  The raw `.img` ships a tiny (~33MB) `STORAGE` partition that **resizes to fill its disk on
  680  first boot** — but a bare `.img` is only ~4GB (`SYSTEM_SIZE=4096` + a small storage tail), so
  681  on a ~4GB disk storage stays ~33MB and hits **100% full**. The first-boot
  682  `rsync /usr/config → /storage/.config` then fails with **ENOSPC** and copies **0** of ES's 144
  683  resource files, so ES can't resolve its `:/` resources (blur shader, `ubuntu_condensed.ttf`,
  684  help icons). The result is a *rendering* ES with a **broken main menu** — no dimmed/blurred
  685  background, wrong fonts, missing help-button glyphs — which looks like a graphics/compositor
  686  bug but is **purely out-of-space**. Real hardware never hits this (storage resizes to fill the
  687  whole SD card *before* the rsync).
  688  
  689  Confirm from the serial shell: `df -h /storage` shows `100%`, and
  690  `journalctl | grep -i "no space"` shows `rsync: ... No space left on device`.
  691  
  692  - **Fix:** run on a **16GB+ disk**. `tools/fork-publish-release` converts the raw image into
  693    the sparse disk size defined by the canonical VM profile and packages that same qcow2 into
  694    `.utm.zip`; first-boot resize then gives ~12GB `STORAGE` and every resource populates. For
  695    a bare `.img`, grow the disk (`qemu-img resize <disk> 16G`, or a ≥16GB target) **before**
  696    first boot.
  697  - **Don't** chase weston / Mesa / `glBlitFramebuffer` for a missing menu dim — that is a red
  698    herring downstream of the missing `:/shaders/blur.glsl`. The compositor never changes ES's
  699    own Mesa GL context, so weston vs sway is irrelevant here.
  700  
  701  ## KVM access (important gotcha)
  702  
  703  `setfacl -m u:max:rw /dev/kvm` grants access but **logind resets it** on session changes, so it
  704  breaks between boots. The durable fix is group membership + `sg`:
  705  
  706  ```bash
  707  sudo usermod -aG kvm <user>     # once (persistent)
  708  sg kvm -c '<qemu command>'      # picks up the group with no re-login
  709  ```
  710  
  711  ## Inspect a headless VM
  712  
  713  - **Screenshot** (verify the UI without a display): QEMU monitor `screendump`
  714    `printf 'screendump /tmp/es.ppm\n' | socat - UNIX-CONNECT:/tmp/qmon.sock` (or a tiny
  715    Python `AF_UNIX` client). Convert PPM→PNG with stdlib `zlib`/`struct` if no image tools.
  716    Needs a display backend that commits the scanout — use `-vnc :N` (a bare `-display none`
  717    captures all-black). Drive input with the monitor: `sendkey ret` opens the ES main menu.
  718  - **Reliable in-guest shell over serial** (prefer this — SSH can reset mid-handshake with
  719    `kex_exchange_identification: Connection reset`): GENERIC_X64 ships
  720    `serial-debug-shell.service` (autologin root `/bin/sh` on `ttyS0`). `run --headless`
  721    puts it on a unix socket and `tools/vm-serial` is the client (echo off, unique
  722    `BEG`/`END` markers around every command because the boot console shares `ttyS0`).
  723    This is the channel that found the disk-size bug.
  724    **A reboot over it is a plain `reboot`** with a short END timeout
  725    (`tools/vm-serial --timeout 8 sh 'sync; reboot'`): the client waits for an
  726    END marker the guest never sends because it is going down, and returns when
  727    the timeout does. The backgrounded form, `(sleep 1; reboot) >/dev/null 2>&1 &`,
  728    returns cleanly and reboots nothing -- the first #175 proof run on RC-4
  729    (2026-09-14) read a 357 s uptime after its "offline boot", and every check
  730    after that was of the wrong boot. After `vm-serial wait`, read
  731    `/proc/uptime` and refuse the boot if it is not small.
  732  - **Live logs over SSH**: default login is `root` / `rocknix`; `PermitRootLogin yes`. No
  733    `sshpass` on the host — use `SSH_ASKPASS=<script-echoing-pw> SSH_ASKPASS_REQUIRE=force
  734    setsid -w ssh -p 10022 root@127.0.0.1 …`. ES logs to `/var/log/es_log.txt`,
  735    sway to `/var/log/sway.log`; `/var/log` is `/storage/.cache/log`
  736    bind-mounted (`var-log.mount`), not tmpfs, so `es_log.0.txt`..`es_log.3.txt`
  737    are the previous boots' files and survive a reboot.
  738    **The ES log file was late until ES `469441d4d` (RC-11, 2026-09-15; fork
  739    #178).** `AsyncLogger` (`es-core/src/Log.cpp`) flushed the stream every 8
  740    batches, so a line could sit unflushed for minutes on an idle carousel --
  741    on 2026-09-14 the token check's lines reached the file 100 s after they
  742    were logged, and a live `grep -c` said 0 for a line that was there. Since
  743    the fix the worker flushes after every batch: a WARNING line is in the
  744    file 5-12 ms after it is logged (ten trials, 2026-09-25), and a `reboot`
  745    2 s after one leaves it in `es_log.0.txt` (ten of ten). **ERROR and
  746    WARNING lines also go to stderr, which is the journal** (`journalctl -b
  747    -u essway` -- the unit is `essway.service`, whose `start_es.sh[pid]` lines
  748    these are; there is no `emustation` unit); INFO lines reach only the
  749    file and are not written at the shipped level. To provoke exactly one
  750    WARNING line on a guest with nothing else logging, ask the interface's
  751    API from a loopback address it does not treat as local:
  752    `curl --interface 127.0.0.2 http://127.0.0.1:1234/caps` (one 403, one
  753    `Access disabled for 127.0.0.2` line). And **the credential filter drops
  754    prose**: RetroAchievements' refusal reads `Invalid user/password
  755    combination`, so a `grep -v passw` read of the log or the journal says
  756    the line is not there when it is (the same run, twice). For a read whose
  757    answer may be that sentence, mask values rather than drop lines --
  758    `sed -E 's/((passw[a-z]*|token|key)[=:][ ]*)[^ ",]+/\1<masked>/gI'` --
  759    and keep the dropping filter for config files, where a value is the
  760    whole line.
  761  - **Offline logs** (VM off): `dd if=IMG of=/tmp/p2.ext4 bs=512 skip=<part2 start sector>`
  762    then `debugfs -R "cat /.config/emulationstation/es_settings.cfg" /tmp/p2.ext4` (toolchain
  763    `debugfs`/`mtools` are under `build.*/toolchain/bin`). Handy because `/var/log` is lost on
  764    shutdown; `/storage` (partition 2, ext4, label `STORAGE`) persists.
  765  
  766  ## Debug order
  767  
  768  When ES fails, check the layer below before blaming the app: read `sway.log` first — an ES
  769  "wayland not available"/renderer abort is usually sway having failed to find a GPU
  770  (`/dev/dri/cardN`), not an ES bug. See `engineering-practices.md`.
  771  
  772  ## Won't boot in UTM / a VM → check the disk logical sector size (4K vs 512)
  773  
  774  The image's GPT + ESP FAT are laid out for **512-byte** sectors. OVMF/UTM firmware **cannot
  775  UEFI-boot a disk exposed with 4096-byte logical sectors** — it misreads the 512b GPT (sees
  776  only the protective MBR), finds no ESP, and drops to the UEFI interactive shell. Symptom in
  777  the shell: `map` shows only `BLK0`/`BLK1`, **no `FS0:`**; firmware prints
  778  `BdsDxe: failed to load ... Not Found` → PXE.
  779  
  780  - The image is **not** at fault — it boots in every 512b firmware/bus (Ubuntu OVMF, upstream
  781    EDK2, qemu's own `edk2-x86_64-code.fd`; virtio and SATA). Don't "fix" the image.
  782  - **Fix is VM-side:** present the boot disk as **512-byte sectors** (UTM: use a VirtIO/SATA
  783    drive, not a 4K disk). A shipped VM artifact (`.utm`/OVA) must bake in a 512b disk config.
  784  - **Reproduce locally** with UTM's exact firmware:
  785    `curl -L .../pc-bios/edk2-x86_64-code.fd.bz2` (+ `edk2-i386-vars.fd.bz2`) from the qemu repo,
  786    then `-device virtio-blk-pci,drive=d0,logical_block_size=4096,physical_block_size=4096` →
  787    reproduces the shell drop; drop the two block-size args (→ 512b) → boots.
  788  - **Container format is irrelevant** to this: raw/qcow2/vdi/vmdk all decode to identical disk
  789    bytes; only the *sector size the VM presents* and the machine config matter. "Shareable dev
  790    image" = an appliance that carries machine config (`.utm` bundle for UTM, OVA for
  791    VirtualBox/VMware), not a bare disk — a bare disk still needs correct UEFI + 512b setup.
  792  
  793  ## One command for every check
  794  
  795  `tools/raofflineproxy-consent-test` runs inside a fresh isolated QA guest with
  796  no IPv4/IPv6 default route. Pass `--expected-build <full BUILD_ID> --output
  797  /storage/.cache/<fresh-owner>`. It imports only installed `/usr/lib` bytecode,
  798  seeds synthetic cached sign-in/counters/incidents, and captures real loopback
  799  usage/log HTTP requests. Unanswered, declined, malformed and stale consent
  800  must send nothing; independent explicit-true controls must send and restart
  801  must not duplicate them. The host checks loaded module hashes against the
  802  assembled candidate. This proves reporting functions, not scheduler timing,
  803  the consent UI or a real account. `--require-early-uptime` additionally refuses
  804  a granted counter observation outside the initial30second cache window;
  805  actual counter/uptime/module hashes are saved before assertion (#457).
  806  Preserve every failed attempt (#361).
  807  
  808  **Supervise long QA runs as well as builds (#395, D-WORKFLOW-143).** Use the
  809  shared `tools/watch-build` runner around the frozen checkout's test command.
  810  For long agent-owned runs, submit that runner through
  811  `tools/watch-build-submit --owner <fresh-owner> --` (D-WORKFLOW-148). A
  812  successful submission is only a launch receipt; check the eventual runner,
  813  command and watcher results and all owned guest processes before acceptance.
  814  Give each run a fresh `ROCKNIX_ARTIFACTS` directory and pass that same root as
  815  `--activity-dir DIR --recursive-activity`; suite logs below its generated
  816  report directory are the activity signal when the summary is quiet. Set
  817  `--interval 5 --stall-min 5` for the first M7 qualification runs. Monitor
  818  outputs stay outside that activity directory. Keep the runner/watcher copies
  819  unchanged while executing, along with the exact command and source identities.
  820  
  821  **A fresh owner creates its own runtime directories (#445).** Sealed source
  822  manifests do not capture empty directories from an older preparation. Create
  823  and validate private key/artifact directories inside the harness before image
  824  conversion or key generation; do not rely on a former owner having them.
  825  When rebinding a chain, verify directory contracts as well as source hashes
  826  and dependency paths. Preserve executed failures and prepare new owners.
  827  
  828  **Power-cut fixtures are durable only after their last write (#519).** Upload
  829  all required source and fixture files, verify their hashes, and synchronize the
  830  guest after the final upload before terminating QEMU. A sync earlier in setup
  831  does not cover a later helper upload. If a verifier loses such an input, retain
  832  the original failed result and bind a separate continuation to the actual
  833  surviving boot/checkpoint; do not manufacture a successful power-test result.
  834  
  835  **Reboot invalidates volatile fault fixtures (#446).** Arm `/tmp` shims and
  836  triggers after the final preparation reboot. Before driving the interface,
  837  verify the consumed executable, the intended failing operation and an actual
  838  fired marker while the independent connectivity control still succeeds. Stop
  839  on an unarmed fixture; a pre-reboot control cannot qualify a post-reboot fault.
  840  
  841  **A browser load event is not a rendered frame (#447).** Before accepting a
  842  panel screenshot after navigation, first require an observable transition to
  843  the intended document/state, then a bounded stable-screen observation and
  844  actual image review. A stable old page is not the requested outcome. `vm-visual-qa settle` can exit0 while reporting
  845  that the screen is still moving; test the reported state, not just the exit.
  846  Retain a visually rejected capture separately from its successful command.
  847  
  848  When host captures disagree with the loaded page, compare the actual QEMU
  849  viewer frame with a native compositor capture before changing product code.
  850  Record the graphics mode actually used. In #447, software `--gl none` kept
  851  stale or partially repainted host frames while native `grim` was correct;
  852  keeping VNC connected did not eliminate it. The canonical virgl profile
  853  produced matching frames. Neither a native capture alone nor a forced resize
  854  qualifies the host display. Use the declared profile and an intended-frame
  855  check with real stale/partial-frame rejection; preserve software-path limits
  856  explicitly. Save diagnostic requests before assertions so failed checks retain
  857  the input that failed. Import new helper dependencies in the runner's actual
  858  Python environment before launching a VM; syntax parsing alone is insufficient.
  859  
  860  Historical-image comparisons derive metadata and page expectations from that
  861  image, including expected absence. RC2 predates `CHASSIS=handset` and the
  862  Connected card (#448); adding those to its guest would change the baseline.
  863  Keep current-candidate requirements intact and record each deliberate
  864  baseline-specific assertion separately from the common rendering procedure.
  865  
  866  For a memory-budget guest, distinguish allocated RAM from Linux `MemTotal`
  867  (#362). Verify the actual QEMU allocation and guest firmware capacity, and
  868  record usable RAM and the kernel reservation log separately. A guessed lower
  869  bound for usable RAM rejected the correctly allocated 1GiB guest before any
  870  workload. Keep real wrong-allocation controls and the page-load, responsiveness,
  871  and no-OOM requirements; do not turn an allocation check into an RSS waiver.
  872  
  873  Pair the recorder with an active harness waiter, checked within 60 seconds.
  874  Announce named suite failures, stale/dead monitoring, suspected stalls and
  875  terminal results promptly. A suspected stall triggers process/log inspection,
  876  not automatic termination. An active waiter cannot alert after disconnection;
  877  that separate destination remains #395. Preserve failed runs and stop owned
  878  guests/endpoints when their job ends.
  879  
  880  `./tools/vm-qa <ROCKNIX-GENERIC_X64...img.gz>` brings the pair up from the
  881  image and runs the scripts test, the round-trip suite, the emulator-exit cell
  882  and every walk, leaving `report.md` and the logs and frames under
  883  `/workspace/artifacts/rocknix-images/qa-<build>-<backend>-<guest>-<date>/`;
  884  it exits non-zero if any suite failed. `--skip-up` for a pair already on the
  885  image, `--only` for a subset, `--link` for the seven link-loss cells (minutes
  886  each, never while an image builds on this host -- they are timing-bound).
  887  `--backend <name>` picks which of the five QA clouds every suite talks to
  888  (default `webdav`); the report header names the cloud, its port and its
  889  caps. Run it on every image before anything is staged (#120).
  890  `--ra-offline` (or `--only ra-offline`) adds the offline-achievements
  891  scenario, `tools/ra-offline-test` (#166): opt-in like `link` because it
  892  needs the serial console, the QA RetroAchievements account file, and spends
  893  one of that account's cheap achievements per PASS -- see § Games with
  894  RetroAchievements sets below. `--guest d` drives the 640x480 guest beside
  895  the pair (`--skip-up` with it: `up` is written around the pair only).
  896  
  897  Two runs fit on one host at once — `--guest a` against one backend and
  898  `--guest b` against another, which is how the matrix is walked:
  899  
  900  ```bash
  901  ./tools/vm-qa --skip-up --only round-trip --backend webdav --guest a &
  902  ./tools/vm-qa --skip-up --only round-trip --backend sftp   --guest b &
  903  ```
  904  
  905  The round trip takes about 130-160 s per backend on this host — except S3,
  906  which takes ~578 s, nearly all of it in one step against a refused endpoint
  907  (#143).
  908  
  909  ## Crash and hang recipes
  910  
  911  The profile carries QEMU's `i6300esb` watchdog with `-action watchdog=reset`,
  912  and the GENERIC_X64 kernel has pstore over UEFI variables (the guest boots
  913  OVMF, so a panic's kernel log lands in the variable store and comes back as
  914  `/sys/fs/pstore/dmesg-efi-*` on the next boot). That makes the whole of
  915  `handheld-evidence.md` provable here except H700 DRAM retention.
  916  
  917  - **A hard power cut**: `system_reset` on the monitor socket. No shutdown
  918    runs, so anything not yet synced is lost -- which is the point. The
  919    journal syncs every minute; write a marker with `logger`, wait past the
  920    interval, cut, and look for it in `journalctl -b -1`.
  921  - **A kernel panic**: `echo c > /proc/sysrq-trigger` (sysrq is on). The guest
  922    reboots itself after `kernel.panic` seconds; `systemd-pstore` then copies
  923    the dump into `/storage/.cache/log/pstore/`.
  924  - **A PID 1 that stops pinging**, which is what a hung kernel looks like to
  925    the watchdog: freeze it. The guest runs hybrid cgroups with a v1 freezer,
  926    so `mkdir /sys/fs/cgroup/freezer/wd; echo 1 > .../wd/tasks; echo FROZEN >
  927    .../wd/freezer.state` stops systemd cold, and the i6300esb resets the guest
  928    within `RuntimeWatchdogSec` (17 s observed against 15 s). The previous
  929    boot's journal then ends without a shutdown line, which is what a real
  930    hang looks like afterwards. **Do not try to starve PID 1 with RT busy
  931    loops**: since 6.12 the scheduler's fair deadline server
  932    (`/sys/kernel/debug/sched/fair_server/cpuN/runtime`, 50 ms/s) guarantees
  933    SCHED_OTHER tasks CPU regardless of `sched_rt_runtime_us`, and four
  934    `chrt -f 99` loops on four vCPUs left systemd pinging happily (2026-09-10).
  935  
  936  `journalctl --list-boots` is the quickest check that the journal is
  937  persistent at all: a volatile one lists exactly one boot, always.
  938  
  939  ## Spin a guest down when its job is done
  940  
  941  A guest costs about 2 GB of RAM for as long as it is up, and guests are
  942  routinely left running for days because nothing forces the question. On
  943  2026-09-19 two had been up for **one day and five days** while a cold build
  944  was taking the machine, and a third was OOM-killed outright during it — the
  945  build did not fail politely, it took the guest with it.
  946  
  947  So: **bring a guest up for a job, take it down when the job ends.** Not as
  948  tidiness — as the difference between a build that finishes and one that dies
  949  at its heaviest package.
  950  
  951  - `tools/build-preflight` lists what is up, how much each holds, and how long
  952    it has been there; `--stop-vms` stops them.
  953  - Disk state survives a stop, so taking a guest down costs the running state
  954    and nothing else. Anything worth keeping should already be off the guest.
  955  - A guest left up deliberately — mid-QA, holding a fixture someone is using —
  956    is fine, and is worth saying out loud rather than leaving for the next
  957    person to guess at.
  958  
  959  ## Automated visual QA (`tools/vm-visual-qa`)
  960  
  961  UI work can be reviewed without flashing a device or photographing a handheld.
  962  QEMU's human monitor exposes two primitives that both work under `-display none`,
  963  which is what makes this usable on a headless build host:
  964  
  965  - `sendkey <key>` — the guest sees real key events
  966  - `screendump <file>` — writes the current framebuffer as a PPM
  967  
  968  `tools/vm-visual-qa` wraps them: it runs a step file, converts frames to PNG
  969  (stdlib; no Pillow needed), and optionally assembles an animated GIF (that
  970  part does need Pillow). `tools/vm-walks/` holds the step files worth keeping.
  971  
  972  ```bash
  973  # boot headless with a monitor socket, then:
  974  tools/vm-visual-qa --monitor /tmp/mon.sock run steps.txt --outdir shots/ --gif walk.gif
  975  ```
  976  
  977  The step verbs are `key` / `wait` / `shot` and, since #125, `settle`,
  978  `wait-for-change`, `wake` and `dismiss-dialogs`. The last four compare
  979  framebuffers rather than counting seconds: `settle` waits until the screen
  980  holds still, `wait-for-change` until the last press has visibly landed (and
  981  fails the walk when it has not), `wake` spends the screensaver's free press
  982  on a key the interface ignores, and `dismiss-dialogs` presses B until the
  983  screen repeats itself, which is the carousel toggling GO TO — so it ends
  984  there whatever was open, where a fixed count of B presses ends on a dialog
  985  from an odd depth. `--help` carries the thresholds, how they were measured
  986  on a 640x480 guest, and the interface facts a walk would otherwise have to
  987  rediscover.
  988  
  989  **Neither a walk's result nor its timing is a fixed delay any more, and that
  990  is the point.** The frame steps are what make a walk survive a host that is
  991  also building — which is the normal state of this machine.
  992  
  993  **Cutting the guest's power (KILL12/13, #105).** `system_reset` over the
  994  monitor (`printf 'system_reset\n' | socat - UNIX-CONNECT:/tmp/rocknix-qemu-monitor.sock`)
  995  drops every dirty page in the guest and keeps QEMU up; the disk holds exactly
  996  what the guest issued. Close the SSH master first (`ssh -O exit`) -- a command
  997  over it stalls across the reset as across a link cut. Prove the reset landed
  998  before trusting `vm-serial wait`: read `/proc/sys/kernel/random/boot_id` and
  999  `/proc/uptime` over serial before, and require a new boot_id and an uptime
 1000  below what it would have read without a reset -- `uptime < u0` alone fails
 1001  when the previous boot was seconds ago. Then `pgrep emulationstation | wc -l`
 1002  = 1, the network test, and `flock -n /var/run/cloud_sync.lock true` (the
 1003  startup sync). `/var/log` does not survive, so anything to be read from
 1004  `es_log.txt` is read in the boot after the cut, and `Could not parse Settings
 1005  file` never lands there at all (Settings load before the log opens). A boot on
 1006  a reseeded `system.cfg` can come up with sshd off: `sshd.service` needs
 1007  `/storage/.cache/services/sshd.conf`, written from `ssh.enabled` at boot, so
 1008  recover over serial with `touch` of that marker then `systemctl start sshd`.
 1009  Once, a reset boot came up with a garbage command line and sat in the
 1010  initramfs shell on the VGA console (ESP intact); a second reset booted
 1011  normally, so give a silent boot 150 s and reset once more before calling it
 1012  dead. The virtio disk is not an SD card: the reset models a battery dying,
 1013  not a card's write cache or FTL, and on this disk a page close followed by a
 1014  cut within 200 ms already tears `system.cfg` written in place.
 1015  `tools/cloud-round-trip --only KILL12,KILL13 --serial-socket ... --monitor-socket ...`
 1016  does all of this.
 1017  
 1018  **Input mapping is the trap.** ES's *compiled* keyboard defaults (F1 = start) are
 1019  not what ships: `/storage/.config/emulationstation/es_input.cfg` on the image maps
 1020  **start = Enter, A/OK = `x`, B/back = `z`**, arrows for direction. Read that file
 1021  on the guest rather than assuming — a wrong mapping looks exactly like "input is
 1022  broken".
 1023  
 1024  Other sharp edges: menu lists **wrap**, so `up` from the top is the short path to
 1025  entries near the bottom -- through the BACK button, which is a focus stop on every
 1026  page. Put a `settle` step before every `shot` rather than a delay; the tool waits
 1027  for the PPM's size to stop changing itself, so a torn frame is no longer yours to
 1028  worry about.
 1029  
 1030  The frames are meant to be *read* — by a person or an image model — which catches
 1031  what code review cannot. Its first run found a shipped defect: Cloud Tools actions
 1032  rendered without their scope descriptions whenever no remote was configured.
 1033  
 1034  ## The credential filter is for a guest's files, not for a harness's verdicts
 1035  
 1036  Guest and device reads go through `grep -v -i -E 'key|pass|token|user|psk'` so a
 1037  value never lands in a transcript. Applied to a harness log it deletes every
 1038  `PASS` line -- a proofs run on 2026-09-13 lost its own verdicts that way. For
 1039  host-side harness output (`tools/vm-qa`, `tools/cloud-round-trip`,
 1040  `tools/last-good-scripts-test`) filter on the shapes a value would take,
 1041  `grep -v -i -E 'passw|pass=|pass:|token=|key='`, and keep the verdicts; the
 1042  strict filter stays for anything read from `/storage`.
 1043  
 1044  ## Games with RetroAchievements sets for the guests
 1045  
 1046  Three free homebrew titles with RetroAchievements sets live outside the repo at
 1047  `/workspace/artifacts/rocknix-qa-roms/` (README there: sources, sha256s, systems):
 1048  Tobu Tobu Girl Deluxe (GBC), Niñoid (GB), Böbl (NES). They are what an achievement
 1049  proof on a guest uses -- the fixture ROMs have no sets, so before 2026-09-13 an unlock
 1050  could only be shown on a handheld. Copy them under `/storage/roms/<system>/`, put the
 1051  QA account on with `tools/qa-accounts <port> ra`, and read RetroArch's log for the
 1052  unlock; with the offline proxy on, the proxy's `service.log` shows the queued award and
 1053  its flush. Do not commit them; the directory is the fixture home.
 1054  
 1055  `tools/ra-offline-test` drives the whole scenario (the `ra-offline` suite of
 1056  `tools/vm-qa`): account on, toggle on, the game launched online through the
 1057  interface's own launch path (`POST /launch` on the guest's loopback, as
 1058  `tools/time-to-play` does), the link cut on the monitor, the game driven over
 1059  `sendkey` until RetroArch logs `Awarding achievement`, the exit with the link
 1060  down, `pending`, the link back, `Flush complete ... flushed=1`, the stamp, and
 1061  RetroAchievements' own API saying the award landed. `--control` runs it with
 1062  the toggle off and asserts #162's loss instead.
 1063  
 1064  Three things about it that are not obvious from the outside:
 1065  
 1066  - **An achievement is spent by a PASS.** RetroAchievements records an unlock
 1067    once per account (softcore; hardcore is a second life, but the proxy is
 1068    casual-only), so the fixture first asks RA's API which of its routed
 1069    achievements the QA account has NOT earned, and FAILs naming the spent one
 1070    with its date when none is left -- never passes over nothing. The
 1071    maintainer resets the account's progress on the game at retroachievements.org
 1072    between runs (2026-09-14). D-QA-059/#464 reopens automated reset of the
 1073    dedicated QA account, refining D-QA-035: evaluate the supported browser/API
 1074    path and FOSS/self-hosting tradeoffs, verify account/game/softcore scope,
 1075    serialize fixture use and read back unearned state through RA's API. Until
 1076    that path is qualified, the current manual reset remains the fallback;
 1077    automation is backlog, not another RC gate. Do not treat hardcore as another
 1078    spend or create another account merely to evade the fixture's state.
 1079  - **A route is a key cadence someone has driven to the award.** Tobu's hidden
 1080    song: two STARTs to the MAIN MENU, then left/right through the carousel with
 1081    4.5 s on each entry -- the award at about the 18th press, 90 s in. Böbl's
 1082    Dive Ball and Niñoid's double jump have no route: Böbl's bubble must be
 1083    sprung over a pillar from a full dive on a timing no blind sequence hit, and
 1084    Niñoid's tutorial kid did not jump on A, B or Up (2026-09-14, on a pair guest
 1085    with the link cut so nothing was spent -- hardcore mode is how a spent
 1086    softcore achievement is re-driven for a route check: it fires again, and is
 1087    lost on purpose by killing RetroArch before the link returns).
 1088  - **The only channel with the link down is the serial console**, and its
 1089    lines end in CRLF. `tools/vm-serial` strips the outermost; a second line
 1090    keeps its `\r`, so `"0"` reads as `"0<CR>"` in a `[ = ]`. Pipe serial
 1091    output through `tr -d '\r'` before comparing it. Busybox `pgrep -x
 1092    retroarch` matches nothing (the process is `/usr/bin/retroarch`); use
 1093    `pgrep -f ^/usr/bin/retroarch`. And `exec.log` carries
 1094    `cheevos_password = "..."` from `setsettings.sh` -- every excerpt goes
 1095    through the credential filter with the account name masked.
 1096  
 1097  ## The interface runs under `essway.service`, and its PATH comes from `/etc/profile`
 1098  
 1099  On the VM image (and the handhelds' too) EmulationStation is not `emustation.service`'s
 1100  process: that unit is inactive, and `essway.service` runs `/usr/bin/start_es.sh`, which
 1101  sources `es_settings` -> `/etc/profile` -> `/etc/profile.d/*` (where `098-busybox` sets
 1102  `PATH="/usr/bin:/usr/sbin"`) -> `/storage/.config/profile.d/*`, then execs
 1103  `emulationstation`. So on 2026-09-14 a drop-in on `emustation.service` was loaded and
 1104  changed nothing, and `Environment=PATH=...` on `essway.service` reached `start_es.sh` and
 1105  was reset before the interface ran. A shim that must be first on the interface's PATH (a
 1106  `systemctl` that sleeps on stop, to watch a page stay alive during a ctl call) goes in as
 1107  a file under `/storage/.config/profile.d/` with `export PATH=/storage/.qa-shim:$PATH`, and
 1108  applies at the next boot -- to every shell that sources the profile, your own included.
 1109  Read the answer from `/proc/<pid>/environ` of the running interface, not from
 1110  `systemctl show`.
 1111  
 1112  Three more harness traps from the same day. Busybox `pgrep` has no `-c`; a poller that
 1113  runs `pgrep -c` prints a usage message every second and reads as "0" downstream -- use
 1114  `pgrep -f 'patter[n]' | wc -l`. `settle` compares frames with a dead band, so a row whose
 1115  counter moves by a digit or two (`SCANNING... - GAME 24 OF 57`) reads as still: the end
 1116  of a run is a fixed `wait` sized to the run, then a settle. And a press sent while the
 1117  interface thread is blocked (the Tailscale switch's `tailscale up --timeout=7s`) is
 1118  queued and lands when the block ends, racing whatever opens then -- the #174 walk's
 1119  second press landed on the switch instead of the popup and turned it off again, a
 1120  "regression" the journal (`tailscaled` started at 34.7 s, stopped at 42.5 s) refuted.
 1121  Never send a second press into a known block; wait it out.
 1122  
 1123  ## A game in the foreground swallows a whole proof run, and every check still "reads"
 1124  
 1125  2026-09-15, the RC-10 run: the walk's first START did not open the main menu (frame
 1126  `01-main-menu.png` showed the carousel), so the presses meant for GAME SETTINGS walked the
 1127  carousel, opened a game's save state manager and pressed LAUNCH. For the next hour every
 1128  "captured" frame was the game, two timers measured the game's animation and reported
 1129  176 s and 2.6 s, and greps of the interface's log returned zeros -- all of it graded as
 1130  if it were the interface. Nothing in the run noticed.
 1131  
 1132  So, in every proof script:
 1133  
 1134  - **Before any walk, `pgrep -f '^/usr/bin/retroarch'` on the guest must be 0.** A hit is a
 1135    FAIL of the phase, not a thing to work around: kill it, say so, and let the phase fail.
 1136  - **A press that must change the screen is proven to have changed it.** Opening the main
 1137    menu is a frame before START and a frame after, compared; three tries, then stop the
 1138    walk. `wait-for-change` alone is not that proof -- a carousel that moved is also a change.
 1139  - **After the walk, `pgrep` again.** A game that appeared during the walk means the walk
 1140    went somewhere else; the frames after that point say nothing about the interface.
 1141  - **A named frame proves nothing about its contents.** Open one before grading a phase.
 1142  
 1143  The session scripts carry these as `no_game` and `menu_open` (`rc6/guards.sh`).
 1144  
 1145  ## A settings change made from the shell is invisible to the running interface
 1146  
 1147  The interface loads `system.cfg` once at start. `set_setting` from ssh changes the
 1148  file, and every later read the interface makes still sees the old value, so a
 1149  proof that flips a toggle from the shell and then drives the interface is
 1150  driving yesterday's setting. 2026-09-15, RC-11 build 2: the proxy toggle was
 1151  turned on from the shell while the summary proofs ran; the interface, started
 1152  before that, still saw it off, opened a NOT CONNECTED dialog instead of the
 1153  offline list -- and the timer graded the dialog PASS because it held still.
 1154  
 1155  - After `set_setting` on a guest, restart the interface (`systemctl restart
 1156    essway`) or reboot before pressing anything that reads the setting. The
 1157    proof scripts' `ensure_toggle_on` (`rc6/guards.sh`) compares `system.cfg`'s
 1158    mtime with the interface process's start and restarts when the file is newer.
 1159  - **A screen that holds still is not the screen you asked for.** Grade the path,
 1160    not the stillness: the offline summary is proven by the interface's own
 1161    `raofflineproxy-ctl summary` call in its log (a dialog asks nothing), the
 1162    slot launch by `-e <slot>` in `exec.log`, a card by its words in the log.
 1163    A frame is the evidence for a human; the log line is the evidence for a check.
 1164  - `set_link off` leaves the guest's address in place, so the interface still
 1165    thinks it has a network; `nmcli dev disconnect eth0` over the serial console
 1166    is what "Wi-Fi off" means on a device. ssh dies with the link: read through
 1167    `tools/vm-serial` until `set_link on` and `nmcli dev connect eth0`.
 1168  
 1169  ### Reconnect-card proof without consuming another real award
 1170  
 1171  `tools/ra-ui-test` exercises installed ES, ctl, Storage and flusher against a
 1172  loopback HTTP provider on a disposable guest. Clear only the owned synthetic
 1173  store before each profile starts ES: a refusal intentionally leaves pending
 1174  state and must not trigger the next profile's startup card. Verify the empty
 1175  baseline directly before attributing a card to reconnect. Its synthetic account/award is
 1176  explicitly separate from `tools/ra-offline-test`'s real award/API proof. Use a
 1177  candidate-bound, sealed owner with the standard watcher; retain installed
 1178  **compiled** proxy-module checksums, actual ES restart/lifetime, address loss
 1179  and return, queue/stamp/log outcomes, frames and actual cleanup. Review the
 1180  sending, success, refusal/retry, dismissed and empty-repeat frames directly.
 1181  English/French at 640×480 and 1280×960 are the current matrix (#465).
 1182  
 1183  The ordinary award runner must reload shell-written toggles before launch and
 1184  capture reconnect as well as game exit. Game exit deliberately has no award
 1185  card (D-RA-030); a carousel frame there does not establish a product defect.
 1186  Do not repeat an already-consumed real award merely to collect the UI evidence.
 1187  
 1188  ## One writer per QA cloud folder
 1189  
 1190  `tools/cloud-test-backend` serves one directory to every guest, and the
 1191  round-trip suite's scenarios read that directory's state as their fixture --
 1192  "an empty endpoint" is a check, not a setup step. A proof on another guest
 1193  that backs up to the same `SAVES_REMOTE` (`/GAMES`) while the suites run on
 1194  the pair makes those checks lie: on 2026-09-15 a `cloud_restore` against
 1195  "an empty endpoint" exited 0 with a restore summary, because guest d's
 1196  #203 proof had just uploaded 471 KB of saves there, and build 5 read as a
 1197  FAIL it had not earned (the re-run alone passed). So: while `tools/vm-qa`
 1198  runs, no other guest points at the QA backend; a proof that needs the cloud
 1199  waits for the suites or uses a folder of its own (`SAVES_REMOTE=/GAMES-d`,
 1200  set on that guest alone) -- and a guest borrowed for a cloud proof gets its
 1201  `cloud_sync.conf` and `rclone.conf` put back before the next suite run.
 1202  
 1203  ## A RetroArch frame is evidence only when its surface was the panel (#263)
 1204  
 1205  RetroArch's own log says what it drew into, two lines apart:
 1206  
 1207  ```
 1208  [INFO] [GL] Detecting screen resolution: 640x480.
 1209  [INFO] [GL] Using resolution 240x256.
 1210  ```
 1211  
 1212  Under sway, RetroArch's fullscreen toplevel comes up at its splash size
 1213  (240x256) and is resized by the compositor's fullscreen configure; when
 1214  the first frame wins that race the surface stays small and sway scales it
 1215  to the panel, and every stem of every letter in every widget is two grey
 1216  columns wide whatever the font size. RetroArch knows the bug
 1217  (`gfx/common/wayland_common.c:87-104`, "a fullscreen sizing bug on some
 1218  hardware and/or compositors") and its detection does not always fire. The
 1219  H700 runs on KMS with `video_fullscreen_x = 640` and never draws this way.
 1220  Every RetroArch frame read off a guest before 2026-09-24 -- #251's stem
 1221  measurements among them -- was that scaled picture (blindspot 54).
 1222  
 1223  So, for any claim about RetroArch's text, widgets or picture on a guest:
 1224  
 1225  - **Read `Using resolution` from the guest's `/var/log/exec.log` after the
 1226    launch, and compare it with the screendump's size.** `tools/time-to-play`
 1227    does this after its first launch (`surface_check`) and is not a pass when
 1228    the surface is under the panel; a walk or a proof script that frames a
 1229    game does the same by hand until it grows the check.
 1230  - The GENERIC_X64 cfg ships `video_fullscreen_x/y = 640/480` and the boot
 1231    quirk `092-retroarch-surface` follows the guest's mode; that changes the
 1232    odds, not the race. A run whose log says the surface was small is
 1233    repeated, and its frames are not filed as evidence of anything but the
 1234    bug.
 1235  - `tools/font-stems` renders a face through the image's own FreeType the
 1236    way RetroArch's font driver does, and is the number to reason from when a
 1237    frame and a table disagree.
 1238  
 1239  ## The frames are compared, not only counted (#252)
 1240  
 1241  `tools/vm-qa`'s `frame-diff` suite holds every walk frame against the same
 1242  frame from the last cut the maintainer accepted on a device
 1243  (`$ROCKNIX_ARTIFACTS/rocknix-images/walk-baseline/`; `BASELINE.txt` names the
 1244  build), clusters the pixels that differ into boxes, and fails the run on any
 1245  box that no line in `tools/vm-walks/claims.txt` contains. A claim is the
 1246  baseline build, a screen glob, a rectangle and the issue that means the
 1247  change; a whole-frame rectangle claims a walk the baseline has not seen.
 1248  `tools/vm-walks/masks.txt` lists the few rectangles it does not compare --
 1249  the clock, a transfer's live lines -- each measured from a diff of two runs,
 1250  and each a place the check is blind. No baseline is a SKIP the report table
 1251  shows; it is never folded into a pass.
 1252  
 1253  Why: the SAVE STATE MANAGER's arrow changed shape on the fifth cut of a
 1254  series and direction on the eleventh, and ten cuts went by, each with a
 1255  proof on guest d that measured the thumbnail it meant to change and nothing
 1256  else. The arrow was on every one of those frames. The maintainer found it on
 1257  the handheld at the thirteenth (#250).
 1258  
 1259  So:
 1260  
 1261  - **A proof asserts what must not change, too**, and against the build
 1262    before the series' *first* change -- named in the acceptance checkbox,
 1263    with a frame kept from it. The previous cut is not a baseline: it can
 1264    already carry the defect, and #250's first checkbox named one that did.
 1265  - **Claim before you run.** A cut that changes a walked screen adds its
 1266    claim line with the change, the way it adds its change-log line. An
 1267    unclaimed box after the fact is the finding, not an inconvenience.
 1268  - **Move the baseline when a cut is accepted on the device**, not when it
 1269    passes the VM: `tools/frame-diff accept <run>/walks <baseline> --build
 1270    <id>`, then prune the claims written against the old one (the next run
 1271    reports them as stale).
 1272  - **A new walk is claimed whole**, and the screen it reaches gets a fixture
 1273    with fixed mtimes (`ensure_manager_fixture` in `vm-qa`), so its frames
 1274    compare from the first run.
 1275  - The manager walks (`manager-nes`, `manager-gb`, `manager-fbn`) land the
 1276    rebooted carousel with `StartupSystem`, with essway stopped first because
 1277    EmulationStation writes its settings back at exit; `default-pre` clears
 1278    the key before every walk.
 1279  - Recheck manager ROM fixtures immediately before each manager walk (#455).
 1280    The earlier match-to-cloud scenario deliberately removes the Game Boy ROMs;
 1281    a surviving FBNeo thumbnail does not prove that Game Boy still exists.
 1282    Require the loaded system list and ES's actual `system-selected` event to
 1283    agree with the requested system before framing it. An old baseline can
 1284    preserve an inherited wrong-system screenshot. `vm-qa --only walks --walk
 1285    NAME` selects a scoped replay; repeat `--walk` to include its destructive
 1286    predecessor. Keep that scope explicit in the report.
 1287  - **The walks decide the state they frame.** `default-pre` also turns both
 1288    sync switches off and removes the last-run stamps, because a full run
 1289    reaches the walks after the exit suite has left the game-exit sync on
 1290    with a COMPLETED stamp and a `--only walks` run does not -- the first
 1291    frame-diff run found the hub's row and switch differing for that reason,
 1292    and the backdrop and the systems page differing because the manager
 1293    fixture adds systems. Anything a walked screen shows is either fixed by
 1294    the suite or masked; nothing is inherited from what ran before.
 1295  
 1296  ## Private settings modes (#421)
 1297  
 1298  `tools/settings-modes-test` runs the actual profile/chksysconfig functions on
 1299  scratch paths with a copy of the candidate BusyBox. It checks all four shell
 1300  settings writers, backup and restore, private live/record modes, old temporary
 1301  files, and refused staging. `last-good-scripts-test` invokes it by default.
 1302  Supply `--profile`, `--chksysconfig`, `--busybox`, and `--output` for a scoped
 1303  old/new source control. Source checks do not replace installed VM proof.
 1304  
 1305  A recovery-race fixture must satisfy `chooseConfig`'s actual recovery
 1306  predicate. An incomplete non-prefix edit is deliberately kept as the live
 1307  file; a torn copy is a strict prefix of its complete, no-older record. Assert
 1308  that precondition and prove recovery occurred before claiming an interleaving
 1309  (#420). Linux truncates `/proc/PID/comm` to15 bytes; identify the running ES by
 1310  `/proc/PID/exe` when checking injected test instrumentation.
 1311  
 1312  ### Bind a restarted frontend only after observed readiness
 1313  
 1314  For state-bound operational fixtures, wait for the actual ES idle endpoint and
 1315  absence of the relevant cloud worker before capturing the apply binding. A
 1316  fixed sleep after systemctl start is not evidence that startup has settled.
 1317  Keep negative-test mutations separate from their expected baseline (copy it or
 1318  save the original scalar first); a shared dictionary can corrupt the oracle
 1319  itself. #519 executor02/04 retained their failures, and the final exact executor
 1320  qualified after those fixture corrections. Do not loosen production refusal
 1321  checks to accommodate an unready or self-modified fixture.
 1322  
 1323  ### USB descriptor revision controls
 1324  
 1325  `tools/usb-gadget-test --output <new-report.json>` runs the actual shared
 1326  revision assignment and both USB preparation functions in disposable filesystem
 1327  fixtures. Run on the host and GENERIC_X64 guest with its `/bin/sh`; retain the
 1328  old-source nonzero control using `--source`. The fixture models configfs-created
 1329  directories, checks all written identities/attributes/links, and cleans itself.
 1330  It does not model kernel write rejection, UDC binding, networking or MTP traffic.
 1331  GENERIC_X64 currently disables CONFIG_USB_GADGET, so do not claim enumeration
 1332  from these controls. The next assembled image still needs installed-script
 1333  verification (#531).
 1334  
 1335  ### VM runtime writes and launch failures (#545)
 1336  
 1337  A healthy /workspace does not prove that /tmp can accept PID files; the host
 1338  may enforce a per-user tmpfs quota. Set VM_QEMU_RUNTIME_DIR to a short, owned
 1339  /workspace/tmp directory for vm-pair and vm-qa together when needed. Keep Unix
 1340  socket paths under107 bytes and retain the selected runtime root in the run
 1341  manifest. vm-pair preflights a real write, preserves launcher failures, and
 1342  checks that the PID owns the expected disk before reporting up. Its failure
 1343  controls run in fork CI. A serial failure must return immediately even when
 1344  ready_one is called in a shell conditional; do not wait for a nonexistent guest.
 1345  Never alter a frozen build or an in-flight tool to recover a host failure:
 1346  seal the changed host-tool hashes separately and submit a fresh watched owner.
 1347  
 1348  The upgrade rehearsal waits for that boot's autostart before seeding and before
 1349  any retained-state comparison (#546). SSH availability is not storage readiness:
 1350  /storage/roms may not yet show the mounted library. Do not move this wait below
 1351  the save hashes; a later file inventory cannot repair an earlier failed check.
 1352  The boot identity and unit result are both required; readiness controls run in CI.
 1353  
 1354  Upstream RAOfflineProxy tests import the source-tree linux.raofflineproxy namespace;
 1355  the image installs raofflineproxy directly. tools/raofflineproxy-installed-native-test
 1356  binds the test namespace to verified installed modules and requires the accepted
 1357  library hash. Keep upstream test bytes unchanged, discover all cases, and reject
 1358  skips. An import failure is not format coverage; keep it and rerun the adapter (#547).
 1359  
 1360  ### Host fixture scratch and current readiness checks (#550, #551)
 1361  
 1362  Unsetting host TMPDIR keeps host-only paths out of bubblewrap guests, but also
 1363  sends later host compilers and patch commands back to host /tmp. Give those
 1364  host calls the owned fixture directory explicitly; keep each guest's private
 1365  /tmp independent. Validate both failure and success at that boundary. A healthy
 1366  filesystem or initial mktemp alone does not prove that later tools can write.
 1367  
 1368  When the upgrade wait changes, its main regression must exercise the current
 1369  function and guest query. Reuse tools/vm-upgrade-readiness-test rather than
 1370  keeping an obsolete text extractor in another suite. Stale boot, failed service,
 1371  missing response, empty identity and never-ready controls retain bounded refusal;
 1372  ready and delayed current boots must pass. The helper must remain runnable in
 1373  fork CI without requiring namespace privileges; the full host suite separately
 1374  exercises its bubblewrap fixtures.
 1375  
 1376  ### Optional hardware information (#548)
 1377  
 1378  Run tools/rocknix-info-test for complete-script missing/malformed/valid CPU, GPU,
 1379  temperature and optional-quirk controls. --baseline accepts the original script
 1380  for a failing control and exact valid-output comparison; --output retains every
 1381  original result channel. Missing VM sysfs metrics must not become blank units
 1382  or zero measurements. Installed INFORMATION proof still needs reviewed frames.
 1383  A startup journal is evidence only when it contains positive service-start
 1384  records; an empty journal cannot pass a negative-only error search.
 1385  
 1386  ### File bind mounts need mountinfo and byte identities (#570)
 1387  
 1388  On the accepted guest, `mountpoint -q /usr/bin/emulationstation` reports false
 1389  for a file bind. Rebinding over it can propagate through a shared mount and
 1390  overlay the fixture's own baseline path. Before switching binaries, stop the
 1391  owned frontend, remove only explicitly owned mountinfo targets, verify the
 1392  underlying baseline/candidate hashes, and make the new bind private. Read
 1393  `/proc/PID/exe`'s hash after readiness; a path name or successful mount command
 1394  is not executable identity. Preserve refused attempts. The exact bounded
 1395  cleanup helper is archived in
 1396  `docs/qa-logs/2026-10-13-es-trim-comparison/fixtures/clear-owned-mounts.py`; it
 1397  accepts only that disposable guest's named paths, not arbitrary live-device
 1398  mounts. Never replay its retired owner.
 1399  
```

## output: the no-guest controls at stage A

```
vm-pair-test :: PASS 9 VM launch controls; fixtures are not a real boot claim
vm-upgrade-readiness-test :: PASS 7 storage-readiness controls; actual guest query, synthetic states, no boot claim
vm-stop-test :: PASS 7 vm-stop controls
vm-manager-system-check-help :: FAIL manager system: not enough values to unpack (expected 2, got 1)
raofflineproxy-integration-test-help ::                         actual older patched source containing linux/
vm-qa-list :: frame-diff
time-to-play-help ::                         (the exit test's rule). Never for a handheld.
frame-diff-help :: does, which writes filter-0 frames.
vm-visual-qa-help ::   --monitor MONITOR     QEMU monitor unix socket
vm-pair-usage :: (default /tmp/rocknix-vm-pair): scratch, rebuilt from the image on every up.
es-syntax-check-noargs :: es-syntax-check: name at least one .cpp
(exits: vm-pair-test 0, vm-upgrade-readiness-test 0, vm-stop-test 0, vm-manager-system-check --help 1, raofflineproxy-integration-test --help 0, vm-qa --list 0 with 17 names, time-to-play --help 0, frame-diff --help 0, vm-visual-qa --help 0, vm-pair 2, es-syntax-check 2)
```

## output: the cycle: vm-qa --skip-up --only fresh,round-trip,exit,time-to-play,frame-diff (report.md)

```
# vm-qa on 069fc27044

started 2026-10-24 19:25 UTC, guest a at :10022, cloud webdav (port 19010, hash=none modtime=no commit=partial bucket=no), image (already up), display: GL through virgl on /dev/dri/renderD128

| suite | result | time | log |
| --- | --- | --- | --- |
| fresh | PASS | 1s | `fresh.log` |
| round-trip | PASS | 84s | `round-trip.log` |
| exit | PASS | 27s | `exit.log` |
| time-to-play | PASS | 72s | `time-to-play.log` |
| frame-diff | SKIP | 0s | `frame-diff.log` |

**PASSED with 1 suite(s) SKIPPED** -- a skipped suite could not run (its log says why) and has not passed.

finished 2026-10-24 19:28 UTC

## time to play -- 069fc27044 on webdav

2026-10-24 19:28 UTC, guest at :10022, cloud `webdav`, payload `full`, 1 repeat(s).

Host state: **vm-qa on serval, guest a**. SSH round trip 6 ms (the launch POST goes over it); one screendump 62 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.

### UI to game, at rest

| from the press to | median / mean / max | n |
| --- | --- | --- |
| the screen leaving the carousel | 0.10 / 0.10 / 0.10 | 1 |
| the handover (a black screen) | 0.10 / 0.10 / 0.10 | 1 |
| RetroArch existing | 0.56 / 0.56 / 0.56 | 1 |
| **the game's first frame** | **0.74 / 0.74 / 0.74** | 1 |
| RetroArch drawing (200 CPU ticks, or 30 four seconds on) | 4.64 / 4.64 / 4.64 | 1 |

### The exit sync, on its own

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.15 / 0.15 / 0.15 | 1 |
| **the last-sync-exit stamp** | **1.59 / 1.59 / 1.59** | 1 |
| the card gone from the screen | 3.51 / 3.51 / 3.51 | 1 |

Outcomes: completed x1. Payload seeded 616 KiB (RetroArch rewrites the auto-state on exit, so what moves is a little less; the log's rclone line has the bytes).

### Game to game, with the exit sync in flight

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.15 / 0.15 / 0.15 | 1 |
| the relaunch sent | 0.16 / 0.16 / 0.16 | 1 |
| the question answered (STOP IT AND PLAY, D-CLOUD-130) | 1.37 / 1.37 / 1.37 | 1 |
| **the next game's first frame** | **1.01 / 1.01 / 1.01** | 1 |
| the exit sync's stamp | - | 1 |

What the launch did to the sync, from the stamp's token: `?` x1.


renderer: virgl (Mesa Intel(R) Graphics (ARL)). -- the guest's Mesa, from the launch log; display: GL through virgl on /dev/dri/renderD128
```

## output: the cycle: time-to-play --repeat 0 --only launch,exit,g2g --vm (stdout)

```
# time to play -- 069fc27044 on webdav

2026-10-24 19:29 UTC, guest at :10022, cloud `webdav`, payload `full`, 0 repeat(s).

Host state: **(not stated)**. SSH round trip 4 ms (the launch POST goes over it); one screendump 61 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.


frames and json: /workspace/tmp/m6-t12/cycle/ttp-repeat0
```

## output: the cycle: emulator-exit-test --vm --only X (stdout)

```
helpers-ready

PASSED
```

## output: the cycle: guest checks

```
cloud_migrate_layout test -x rc=1
18
Mem:            7771         718        5985          48        1536        7052
VmHWM:	 2662384 kB
VmRSS:	 2662384 kB
```

## output: host probe: vm-manager-system-check with and without PYTHONOPTIMIZE

```
FAIL manager system: requested system is missing or duplicated
plain, no system and a wrong selection: rc=1
PASS actual selected manager system nes
PYTHONOPTIMIZE=1, same input: rc=0
PASS actual selected manager system nes
plain, correct input: rc=0
```
