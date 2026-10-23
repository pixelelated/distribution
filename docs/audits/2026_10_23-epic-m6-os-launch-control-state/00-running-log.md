# Epic Audit Running Log — M6.P2 T1, the OS scripts: launch, control and state

**Auditor:** Code Auditor skill (v1.13.0, identical to `next`'s copy: `diff -q` against `git show next:.claude/skills/code-auditor/SKILL.md`, no output), with the renovation face of `docs/reviews/plan-for-the-plan.md` § 4
**Primary model:** Claude Opus 5.5 (`claude-opus-5-5`, lab Anthropic) at high effort, in Claude Code; identity sources: the coordinator's dispatch on #648 (issuecomment of 2026-10-23T07:04:27Z) and the session's own metadata
**Session:** herdr agent `m6-t1-os-launch`, session `33bed370-5d5d-4a1e-a4e2-38ef09d04359`, pane `wN:p4`
**Started:** 2026-10-23 07:05 UTC
**Scope:** slice `os-launch-control-state` (#648, `M6.P2 E695/T1`), area epic #695, renovation epic #339, milestone M6; every tracked path under `projects/ROCKNIX/packages/rocknix/` except `sources/scripts/backuptool` (T17's)
**Spec:** `docs/reviews/briefs/os-launch-control-state.md` version 2 (its § 7 is #648's checklist); `docs/reviews/plan-for-the-plan.md`
**Depth:** Extended (two reviewers from two other labs: GPT-6 Astra, Gemini 4 Argon)
**Branch / worktree:** `feature/m6-os-launch-control-state-648` at `/workspace/repos/pixelelated/distribution.worktrees/m6-os-launch-control-state-648`

---

## Log Entries

### [Phase 0] 07:05 — The brief's first commands

- `HEAD` `4228561fd2cfbb398cee9bd55aec7720536cbeea`; stacked on the P1 tip `2174265e9c` (`merge-base --is-ancestor` exit 0).
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md`: `fork-workflow.md` (2 +-), `instruction-files.md` (5 ++++-); nothing else. As the brief expects.
- `git diff --quiet 8ebaf8daad HEAD -- projects/ROCKNIX/packages/rocknix/`: exit 0. The slice's bytes are `next`'s `8ebaf8daad` (`next` = `origin/next` = `8ebaf8daad`).
- `upstream/next` after `git fetch upstream --no-tags`: **`8b70f693b8`** (`8b70f693b87464efb2ad0febe570db8eb67b6563`); the fetch moved it from `c1f1746828`. This is the slice's Q4 upstream pin.
- `git log --oneline c445081a59..upstream/next -- projects/ROCKNIX/packages/rocknix/ | wc -l`: 43 (the brief's count; the newly fetched upstream commits do not touch the package).
- The brief and the epic's futro (`docs/futros/2026-10-23-m6-os-scripts-and-launch.md`) are in the tree.
- `node` v24.21.0, `npm` 11.19.0 on the host; `tools/council/node_modules` absent (the § 1 install comes before Phase 4.6).

### [Phase 0] ~07:06 — Start confirmed, lane-start committed

- Start comment on #648: issuecomment-6359466876.
- Work-log entry `07:05 UTC — #648 T1 lane started`, `tools/work-log-index --write` and `--check` (current); commit `a0d9e39101`, pushed.
- `tools/ceremony-check --gate` exits 1 on `weekly: 2026-W42 summary missing`. The brief § 9 makes W42 the M7 lane's; the pre-push hook enforces the gate only on pushes of `next` (`.githooks/pre-push`, the `refs/heads/next` branch at line 326), so the feature push went through without `--no-verify`. To be noted on #648 as owed by another lane.

### [Phase 0] ~07:07 — Reading (§ 3, the pre-flight) begun

- Read whole: `.claude/skills/code-auditor/SKILL.md`, `references/phases.md`.
- Read whole: `references/review-levels.md`, `templates.md`, `anti-patterns.md`; `.claude/rules/packaging-and-patches.md`, `change-log.md` (both equal to `next`'s).
- Read the sections the brief names in `generic-x64-vm-testing.md` (§ Headless, § What the guest's busybox lacks, § Fixtures for the launch path, § After every VM cycle, § Crash and hang recipes, § Spin a guest down, § The interface runs under `essway.service`, § A settings change made from the shell is invisible, § Private settings modes) and in `rclone-cloud-sync.md` (§ Config conventions, § Critical gotchas, § Style, § What the audit's fixes changed, § What the audit of the fix round changed). Both files equal `next`'s.
- Every-session rules: loaded this session from the worktree, which differs from `next` only in the two P1 files.
- Points carried into the read: `get_setting`/`set_setting` need `. /etc/profile` in a non-interactive ssh shell; busybox `pgrep -x` matches the whole argv and has no `-c`; `comm`, `realpath`, `find -printf` are absent on the guest; the interface reads `system.cfg` once at start; `exists()` caching is ES-side, not this slice's.
- `docs/blindspot-register.md`: entries 7, 13, 30, 32, 33, 34, 43, 51, 57, 64, 72, 73 read in full; the titles of all 73 read (the opening table of 1 to 28 is 32 KB, its rows read by title). Not every entry's body was read; a later entry that bears on a finding is opened when the finding is written. Carried: 34 (busybox `tr`/applets: run the check under the image's busybox), 43 (a header's safety claim is a hope: `rocknix-evidence`, `setsettings.sh`'s verbose log), 33 (sentinels collide with a wrapped tool's codes), 32 (monotonic time for boot ordering), 57 (count the call sites against the issue's count), 72 (a stop inside `$(...)` ends only the subshell).
- Read: the epic's futro whole (`docs/futros/2026-10-23-m6-os-scripts-and-launch.md`); #648's body (identical to the brief § 7) and its two comments; #695's body and comments (the futro comment is the file's text); the M6 body (T1 CURRENT, the stage-D pause and the 4.6 blocker are the coordinator's NEXT); #339's body; #346's body grepped for T1 and its last three comments; `.github/sessions/saved-session-state-next.md` (saved 2026-10-17, read for runtime only: every M7 build/VM owner complete, "do not reuse old run owners").
- Host at ~07:09: `pgrep -f qemu-system-x86_6[4] | wc -l` = 0; no `make docker-[A-Z]`; `/tmp/rocknix-qemu.pid` and the default serial socket absent; `free -g`: 49 GiB available, **swap 7 of 7 GiB used**. Whether this shell sees the host's process table is checked before the guest starts (#506).
- Not yet read, opened when their phase needs them: `packages/README.md` (with `package.mk` in Phase 2), the decisions by ID (from the register as each is cited), the open issues of brief § 3 (Phase 1), the prior audits' punch lists (counts only, Phase 1).

### [Stage A] ~07:10 — Scope re-derived
- (Clerical, 07:11: the four headings above carried times written by estimate, not read from the clock; corrected to `~` approximations bracketed by the 07:05:05 first-commands timestamp and `date -u` 07:11:18. From here every time is read from `date -u`.)
- Counts (brief § 2's three commands): `git ls-files ... | grep -v -F backuptool | wc -l` = **83**; the inventory filter = `paths 83 lines 13327 fork-own paths 29 upstream-carried paths 54 fork-own lines 8369`; numstat against the empty tree at `8ebaf8daad` = **13327**. No delta from the brief.
- M7 delta (`git -C /workspace/repos/rocknix diff next 069fc2704421 -- projects/ROCKNIX/packages/rocknix/`; the legacy checkout's `next` is also `8ebaf8daad`): three commits, `package.mk` +2/-1 (`Python3 coreutils` added to `PKG_DEPENDS_TARGET`, #642), `runemu.sh` +62/-1 (a lifecycle-admission prologue before `. /etc/profile`, and `exec 199>&-` before the proxy start). Hunks in `01-research-notes.md` § Scope.
- RetroArch half (#336 Step 1: a runner for 2D cores chosen per core; RetroArch stays for GL cores and netplay): `runemu.sh` lines 238 to 357 (the `retroarch)` branch of `case ${EMULATOR}`) and `setsettings.sh` whole (called only from `runemu.sh:327`, to be confirmed by Q6's search).
- shellcheck: v0.11.0 static binary from the project's GitHub release, into `.qa-scratch/shellcheck-v0.11.0/` (gitignored, `.gitignore:63`); archive SHA-256 `8c3be12b05d5c177a04c29e3c78ce89ac86f1595681cab149b65b97c4e227198` equals the digest GitHub publishes for the asset; binary SHA-256 `4da528ddb3a4d1b7b24a59d4e16eb2f5fd960f4bd9a3708a15baddbdf1d5a55b`.
- Image: copied to `ROCKNIX_ARTIFACTS=/workspace/artifacts/m6-t1-20261023` with its `.tar`, `.identity.json` and the previous image `...20261022T145625Z.g6e3a2165d415...img.gz`; `sha256sum -c` OK on all three. The build root's `image/system/etc/os-release` says `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`, `BUILD_BRANCH="build/m7-signin-20261022-07"`; to be confirmed from the guest. Its `bin/sh -> dash`; `usr/bin/busybox` present.

### [Stage A] 07:12 — The guest

- `qemu-img`: `t1.qcow2`, 16 GiB virtual. Booted `generic-x64-vm run --headless --daemonize --pidfile $A/qemu.pid --serial $A/serial.sock --monitor $A/monitor.sock --vnc 19 --ssh-port 10032 $A/t1.qcow2` (`A=/workspace/artifacts/m6-t1-20261023`; OVMF vars default beside the disk, `t1.ovmf-vars.fd`); QEMU pid **2334316**; `vm-serial --socket $A/serial.sock wait`: ready after ~30 s at 07:12:50. No other guest was up (`pgrep -f qemu-system-x86_6[4]` = 0; this shell sees the host's table: PID 1 `systemd`, 681 processes).
- **BUILD_ID from the guest's `/etc/os-release`: `069fc270442134fe771258418adf4e666e0473fb`**, `BUILD_VERSION="0.0.1-dev+20261022T235948Z.g069fc2704421"`, `BUILD_BRANCH="build/m7-signin-20261022-07"`; `/storage` 11.9G.
- **Delta against the brief: `/bin/sh` is bash, not dash.** Guest: `/bin -> /usr/bin`, `/usr/bin/sh -> bash` (GNU bash 5.3.0), no `/usr/bin/dash`. The build root agrees once read without following its absolute `bin -> /usr/bin` link on the host (`ls -ld $R/usr/bin/sh` -> `bash`; `$R/usr/bin/dash` absent). The brief's and the futro's "dash" is the host's own `/usr/bin/sh`. So a `#!/bin/sh` script (`usbgadget`) runs under bash in POSIX mode on the image; Q2 reads it against POSIX sh and proves it on the guest. Friction line written (07:14); reported on #648 for the coordinator's brief correction.
- Confirmed as the brief says: `python`, `python3` -> `python3.14`; `/usr/bin/env -> busybox`; busybox 182 applets, `grep` not among them (`/usr/bin/grep` is GNU's).

### [Stage A] 07:13 — SSH and the two tool trials

- QA key `ssh-keygen -t ed25519` at `$A/qa-key` (outside the tree), provisioned over serial into `/storage/.ssh/authorized_keys`; `ssh -i $A/qa-key -p 10032 root@127.0.0.1` works; `get_setting system.loglevel` (after `. /etc/profile`) = **`verbose`** (the engineering image's `DEVELOPMENT_DEFAULTS`).
- **`tools/emulator-exit-test --port 10032 --identity $A/qa-key --vm`**: 07:13:57 to 07:14:25, **rc 0, `PASSED`** (A, B, C, D all PASS). Works on a single guest without `tools/vm-pair`. It exercised the **image's** `runemu.sh` (the M7 copy, which differs from the tree's by the lifecycle prologue). Log `$A/trial-exit-test.log`.
- **`tools/time-to-play --port 10032 --identity $A/qa-key --monitor $A/monitor.sock --out $A/ttp-trial --no-configure-remote --vm --quick --label m6-t1-stage-a-trial`**: 07:14:31 to 07:16:44, **rc 1**: `Not a pass: the exit sync had no cloud to reach (rclone lsd qa-cloud: no)`. Expected with `--no-configure-remote` on a guest with no remote (blindspot 56's guard firing as designed); the launch and game-to-game cells measured (first frame 0.76 s, next game's first frame 1.01 s, n=1, the trial only, not the Q5 measurement). Works on a single guest. Consequence for Q5: the exit-sync cell will always read "no cloud" under the brief's `--no-configure-remote`; the two time-to-play numbers do not depend on it. Output `$A/ttp-trial/`.

### [Stage A] 07:18 — Committed; reviewed-at

- Stage A committed and pushed as **`efadfea08a`**: this is **`reviewed-at`** (`git diff --quiet 8ebaf8daad efadfea08a -- projects/ROCKNIX/packages/rocknix/` exit 0). Reported on #648 (issuecomment-6359668939) with the `/bin/sh` brief defect and the W42 gate owed by the M7 lane.

### [Phase 1] 07:19 — Research begun
- 07:21: open issues of brief § 3 read for leads (bodies under `.qa-scratch/t1/`); 28 of 139 closed `bug` issues name the package's scripts (pattern: `\b(<53 names>)\b`, the names list in the research notes' generator, excluding bare `run` and `brightness`); 162 fork commits on the package since `c445081a59`; the nine prior punch-list counts equal the brief's. Phase 1 summary written in `01-research-notes.md` § 1.6. Red flags: #316 (upstream's `wifictl` refactor), #120 (scripts tests cover three areas only), three closed credential bugs on the security list.

### [Phase 2] ~07:33 — Mechanical checks and the image-versus-tree sweep

- `02-forward-audit.md` opened: image vs tree (78 same; `runemu.sh`, `system.cfg`, `motd` differ; `099-freqfunctions` absent on x86_64; all as the brief predicts); the host checks: pkgcheck 0, last-good-scripts-test 0 `PASSED` (1,379 PASS, 0 FAIL, image busybox), settings-modes 0, wait-lock 0, usb-gadget 0 on the host (dash) and 0 on the guest (bash as sh), rocknix-info 0, melonds 0, vocabulary-check 0 but **reads none of this slice's paths** (default `--scripts` is the rclone sources plus backuptool; scoped, it judged only backuptool's strings).
- shellcheck v0.11.0 over 63 shell files: 16 errors, 319 warnings, 542 notes; the 16 errors tabled as leads, each to be read at its site.
- Next: group 1 (the launch path), file by file, writing each unit's row and findings before the next.
- (between 07:34 and 07:44, time not read) `runemu.sh` read whole; F-01 to F-08 written. F-01 (a governor value executed as a command; ES offers `default` and, on the H700, `conservative`/`userspace` with no function) is the first proposed bug; F-02 (`onlinethreads` missing on x86_64) and F-03 (exit restores racing the next launch) next. Guest proofs owed for F-01, F-02, F-03.
- (before 07:44:42, time not read) `setsettings.sh` read whole (the RetroArch half). F-09 to F-19: four proposed bugs of Medium weight (F-09 `add_setting`'s `&`, F-10 `match()` substring, F-14 the netplay host into `eval`, F-16/F-17 the MAME 2003-Plus and Gambatte option files truncated), one race to prove (F-11 the staged sed file), Lows. Both truncations date from the import `9f1fab30f6`. Guest proofs batched next, after group 1's remaining files.
- (before 07:44:42, time not read) group 1 read whole (`runemu.sh`, `setsettings.sh`, `run`, `001-functions`, the four fragments). F-01 narrowed (ES drops `default` on save, `SystemConf.cpp:387`): the misfire is the H700's `conservative`/`userspace`. F-20 to F-26 written. Next: the guest proof batch for group 1 (F-01, F-02, F-09, F-10, F-11, F-14, F-16, F-17, F-21), then group 2.
- (Clerical, 07:47, the second time: times written by estimate again despite the 07:11 note. Clock reads this phase: 07:30:04, 07:30:41, 07:32:10, 07:44:42, 07:44:50. The 07:31/07:33/07:34 marks are now `~`; the 07:39 to 08:06 marks in this log and in `02-forward-audit.md` were wrong (all that work precedes 07:44:42) and are replaced by "time not read". From here a time is written only beside a `date -u` in the same command.)

### [Phase 2] 07:44:42 — The group 1 guest proofs

- `.qa-scratch/t1/proofs/group1.sh` on the guest, 07:44:42-07:44:50 (`date -u` before and after), output `.qa-scratch/t1/proofs/group1.out`. The guest's `/usr/bin/setsettings.sh` and the tree's hash alike (`02e110af2f2697db`); `runemu.sh` run as the **tree's** copy from `/storage/.qa-t1/`, with `/usr/bin/retroarch` file-bound to a stub that records its argv.
- Proven: F-01 (`runemu.sh: line 467: conservative: command not found`; the `powersave` control prints nothing), F-02 (`line 560: onlinethreads: command not found`), F-21 (plain name `[powersave]`, `[!]` name `[]`), F-14 (the marker created; RetroArch's argv cut at `127.0.0.1`; rc 1; the plain-host control makes no marker), F-10 (neogeo `rewind_enable = "false"`, run-ahead off; snes `true`), F-09 (`cheevos_hardcore_mode_enable = "1"` under netplay), F-16 and F-17 (3 lines to 1), F-11 (keys lost in 9 of 200 concurrent iterations; serial control 96 of 96).
- **The script's restore did not run: F-22 on my own fixture.** The script set `trap restore EXIT` and then called `set_setting`, whose `wait_lock` installed its own `trap ... INT TERM EXIT` (`001-functions:255`) over it. So `system.cfg` kept the script's deletions (`global.netplay=0` and `global.retroachievements.hardcore=0` gone, `diff` at 07:45 guest time), RetroArch's config kept the fixtures, and the stub stayed bound (`/proc/self/mountinfo` 1 entry; `mountpoint -q` said "unbound", which is the #570 trap for a file bind). Restored by hand at ~07:46: unbound (mountinfo 0, `/usr/bin/retroarch` starts `\177E`), `system.cfg` and `/storage/.config/retroarch` copied back and compared equal, fixtures removed. No game was launched while the stub was bound. Friction line owed; the proof script gains an explicit restore and a mountinfo check.
- New from the proofs: every launch on the default config passes `--set-shader /tmp/shaders/` (no `shaderset` key in the shipped `system.cfg`, so `set_shader`'s `*)` branch enables a shader with an empty name: F-27, to read against RetroArch's log). `analogue` reads `1` from the shipped `global.analogue=1`, so F-09's `:989` half has no visible effect today.

### [Phase 2] 07:53:47 — Group 2 read and proven

- Group 2 read whole (`chksysconfig` and its units, `001-setup`, `003-upgrade`, `007-rootpw`, `setrootpass`, `post-update`, `factoryreset`, `installtointernal`, `automount`, `system.cfg`): F-28 to F-46. Guest facts read on the way: busybox `find` supports `-regex`/`-delete` and returns 0 after a failing `-exec cp` (F-40); the overlay units' option order (F-36); `cryptpw` present and the shadow root line in the expected shape (F-29 latent).
- Proofs 07:53:47 (`group2.sh`, explicit restore, all `same`): F-29 (empty root hash, rc 0), F-44 (DPMS `1` deleted), F-28 (`upgrade.log` overwritten), F-19 (no overlay under the default bezel; upgraded to Medium). **F-32 corrected**: busybox `sed` completes the half line rather than joining it, which is the G2-E-core-03 shape.
- Next: group 3 (62 paths), then the coverage table, Q4/Q5/Q6, Phase 3/4.

### [Phase 2] ~08:03 — Group 3, the security list, the Q6 table, the shellcheck verdicts

- Read: `wifictl`, `rocknix-evidence` (+unit, timer), `usbgadget` (+rule, 081), `rocknix-corekeep`, `rocknix-memory-manager` (+unit), `rocknix-es-thebezelproject`, the stubs (`rocknix-update`, `rocknix-report-stats`, its masked timer), the nine unreached scripts. F-47 to F-57.
- Guest facts: `redact_credentials` misses `nmcli ... password <v>`, `cryptpw ... <v>` and `...psk <v>`; the snapshot's `top` prints names only, so no live path (F-47 narrowed); `gzip -l` works on the image's gzip; the report-stats timer is masked; `espeak` present (`say` reached); `/usr/sbin/quantum` absent and `050-audio` errors every boot (F-56); `paneladj`'s `>`/`<` clamp every value and write a stray file (F-57); `updates.batocera.org` lists answer 200 (the bezel installer alive).
- `04-analysis.md` drafted with § Renovation face Q6: 47 rows, 9 unreached (all since the import), 1 hand-run, 37 reached.
- The 16 shellcheck errors all have a verdict: 7 defects (F-09, F-10's four sites, F-16, F-56, F-57), 4 in unreached scripts, 4 benign.
- (time not read, between 08:03:44 and 08:10) group 3 finished: `package.mk` (F-62 undeclared runtime tools, all 36 present; F-63 `system.cfg` mode 645), `rocknix-config`/`rocknix-settings` (F-64 Batocera's dependencies missing: `rocknix-encode`, `rocknix-resolution`; F-65 a third unguarded `system.cfg` writer, unreached), `rocknix-scraper` (F-66 a dead chain; the Q6 row corrected), `updateabl` (F-67; the skip-check suspicion cleared by the ELF's 63 x 4,096 bytes), `rocknix-bluetooth` (F-68 link keys under `/storage/roms/backups`), the rest in outline (depth stated per file), `tz` (F-69). Every one of the 83 paths now has a reading recorded; next, the coverage table.

### [Phase 2] 08:20 — Criteria, summary, boundary; two notices on #648

- `02-forward-audit.md`: the 15 criterion entries (7 PASS, 2 PARTIAL, 1 FAIL expected, 5 UNTESTABLE for later stages), the summary, the Coverage Boundary (62 paths whole, 21 in outline).
- `tools/lint-audit-artifacts --phase pre-issue` at 08:18: 13 contract failures, the list of what Phases 3 to 5 must write.
- The Argon route is absent (`grep -c gemini-argon ...`: 0, 0); notice on #648 (issuecomment-6360631186) ahead of the 4.6 blocker.
- `tools/vm-upgrade-rehearsal` not run: it uses the shared QA backend and `vm-pair` with no instance options, which brief § 5 rules out for this lane while also listing the tool; asked on #648 (one question), not run before an answer.

### [Phase 3-4.5] 08:24 — The retrospective and the analysis

- `03-retrospective.md` written: conformance (rules, blindspots, invariants), five seams, the gaps with their search trail, five sibling tables (§ 3.6.5).
- `04-analysis.md` assembled around the measured Q4/Q5/Q6: 68 findings, **0 Critical, 0 High, 19 Medium, 49 Low** (the risk table generated from `02`'s headings; two parser shapes needed before the count matched the 68 headings: a first count of 58 was wrong and was never published). Phase 4.5: the 19 Mediums survive; five findings changed by refutation before it (F-01, F-09's fix shape, F-32, F-47, F-67).
- Pre-issue lint: the remaining failures are `05` (stage D) and the second opinion (4.6).

### [Phase 4.6] 08:26 — The Astra seat: probe, brief, the call in flight

- `npm install --prefix tools/council` (08:24:44, rc 0): `tsx v4.23.15`, `node v24.21.0`; npm declined esbuild's postinstall under its install-scripts gating, and `tsx` runs (the probe below proves the toolchain end to end).
- `second-opinions/review-plan.json` written before the first call: depth `extended`, primary `anthropic/claude-opus-5-5` (identity: the dispatch on #648 and the session's metadata), reviewers `gpt` (`openai/gpt-6-astra`, `max`, provider pinned OpenAI) and `gemini-argon` **pending** (route absent).
- **Probe** (`tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-probe-prompt.md --output second-opinions/gpt-probe.md`, 08:25:36-08:25:49): rc 0, `council-facilitator@1.14.0`, `outcome: success`, `model_field: openai/gpt-6-astra`, `served_provider: OpenAI`, `model_identity_source: provider_response`, 0 retries.
- **Brief** `second-opinions/gpt-brief.md` (151,087 bytes, sha256 `64c9dc3240a3b169...`): the template's three asks, `02` whole, `03` whole, `04` through § Finding Verification. Before sending: 0 fixture values, 0 credential-shaped lines, `forbidden-terms-check --stdin` 0 hits, 0 `secret-patterns` hits.
- **Refutation pass in flight** since 08:26:47 UTC: `tools/watch-build --record-only -- tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-brief.md --output second-opinions/gpt-audit.md --per-attempt-timeout-ms 1800000 --total-timeout-ms 3600000`. What watches it: the watcher's record `.build-runs/20261023T082647Z-e7167ae6/` (status, `build.rc`) and a harness background task that delivers the result to this session when the command ends. Its silent-failure mode: if the session is killed, the harness task dies with it and only the record remains.

### [Phase 4.6] 08:42 — Astra graded; the Argon seat pending; stopped at the blocker

- The refutation pass ended rc 0 (`.build-runs/20261023T082647Z-e7167ae6/`): `model_field openai/gpt-6-astra`, `served_provider OpenAI`, identity `provider_response`, 664,487 ms, output sha256 `df20875d97a70456...`, `gpt-audit.md` + `.provenance.json`.
- Every item was graded against the cited lines, re-read 08:30-08:41, into `04-analysis.md` § Second opinion:
  - 7 new findings: G-01 Medium; G-02 to G-07 Low; G-02, G-04 and G-05 narrowed.
  - Raised to High: F-14 and F-67.
  - Lowered to Low: F-19.
  - Raised to Medium: F-15, F-33, F-42, F-43 and F-63.
  - The seat was refuted on two points: F-40's High (the source card is not touched) and F-57's minimum branch (the `elif` never runs).
  - The first reader was corrected by the seat on two points: F-54's `../` example and F-57's `1`-file sentence.
  - F-09's fix shape is replaced; F-10 and F-43 split in Phase 5.
- Provisional tally: **75: 0 Critical, 2 High, 22 Medium, 51 Low**.
- `review-plan.json`: the gpt seat is marked complete; gemini-argon is still `pending`.
- **Stopped at Phase 4.6 (brief § 1, the named blocker):** `grep -c gemini-argon scripts/council-invoke.ts tools/lint-audit-artifacts` is still `0`, `0`. No Phase 5, no audit issue and no bug issues until the route is on this branch (`1c7d283ad5` + `a7a3bdda4e`) or the M7 merge lands. The guest stays up (QEMU pid in `/workspace/artifacts/m6-t1-20261023/qemu.pid`) for the stage-D proofs.

## [Phase 4.6] 16:26 — Unblocked: the Argon route merged, verified, the probe clean, the refutation in flight

- The coordinator's reply on #648 (issuecomment-6369533517, written 16:21 UTC) names the remedy: the coordinator tip `6874394d49`, carrying `fac2129787`, `1c7d283ad5` and `a7a3bdda4e` picked as `033eb7ed23`, `0ceb2994c5` and `6874394d49`. It answers the rehearsal question (b): skip and record it, now in `04` § Coverage Boundary.
- **Merge `7dd89b86dc`** (16:22-16:24). It also brought `b5f1fa136e`, which the reply said this branch already carried; it did not. The day's work log and `INDEX.md` conflicted. Both sides' entries are kept in time order and the index is regenerated (`tools/work-log-index --check`: current). `grep -rl -E '^(<<<<<<< |>>>>>>> )' . --exclude-dir=.git` prints nothing (#696).
- **The gates on the merged tree:** `tools/council/run verify-pins`: `OK - verifier pins match current files and every re-pin is accountable.` `tools/council/run test` (no provider calls): toolchain 39/39, **routing 127/127** (the Argon cases are among them; M7's commit recorded 119), seat efforts 19/19. `grep -c gemini-argon scripts/council-invoke.ts tools/lint-audit-artifacts`: `7`, `4`.
- **Argon probe** (`tools/council/run invoke --member gemini-argon --provider openrouter --prompt-file <abs>/second-opinions/gemini-argon-probe-prompt.md --output <abs>/second-opinions/gemini-argon-probe.md`, 16:24:47-16:24:53): rc 0, `council-facilitator@1.14.1-pixelelated.2`, `outcome success`, `model_field google/gemini-4-argon`, `served_provider Google`, `model_identity_source provider_response`, verification `semantic`, 0 retries; the reply `READY Gemini 4 Argon`. A first attempt with paths relative to the audit folder was refused locally (`local_config_error`, ENOENT: the runner resolves from the repository root); nothing was sent.
- **The refutation brief** `second-opinions/gemini-argon-brief.md` (163,754 bytes): a third-reader preamble, the Astra packet unchanged from its first `---` (checked byte-identical with `cmp`), and `04` § Second opinion (the Astra grades) appended, as the coordinator directed. It asks for new items as A-xx, a refutation of both readers at Medium and above (the 2 High and 22 Medium), a check of each of the first reader's grades of Astra, and what it could not judge.
- **Refutation pass in flight** since 16:25:30 UTC: `tools/watch-build --record-only -- tools/council/run invoke --member gemini-argon --provider openrouter --prompt-file <abs>/gemini-argon-brief.md --output <abs>/gemini-argon-audit.md --per-attempt-timeout-ms 1800000 --total-timeout-ms 3600000`. What watches it: the watcher's record `.build-runs/20261023T162530Z-c144c2c1/` and harness background task `bhfar4v12`, which delivers the result to this session when the command ends. Its silent-failure mode: if the session is killed, the harness task dies with it and only the record remains.

## [Phase 4.6] 16:37 — The guest stopped for the host handoff

- The Argon pass returned at 16:34:19 (rc 0). At the M7 coordinator's host request (#648 issuecomment-6369834541, read 16:37) the guest was stopped at **16:37:49 UTC**: `tools/vm-stop /workspace/artifacts/m6-t1-20261023/qemu.pid /workspace/artifacts/m6-t1-20261023/t1.qcow2`, rc 0, `down: owned QEMU exited (pid 2334316)`; no `qemu-system-*` left on the host. `t1.qcow2` is kept for stage F. Logged in `docs/vm-qa-log.md` and as `M6 guest down` in `/tmp/m7-m6-host-coordination-20261023.txt`. No runtime starts until M7 writes `resource return` there.
- The request said "before grading"; grading had begun at 16:34 with reads of the tree, the interface pin and the proof output, and one read over SSH of the guest's `sleep.conf.d` (credential filter applied) between 16:34:48 and 16:37:49 (no clock was read at the read itself), before the comment was seen. Nothing was written on the guest.

## [Phase 4.6 → 5] 16:42 — The Argon seat graded; the punch list written (84 items)

- The refutation pass ended rc 0 at 16:34:19 (`.build-runs/20261023T162530Z-c144c2c1/`, `build.rc` 0): `model_field google/gemini-4-argon`, `served_provider Google` (pin `google-vertex/global` PASS), identity `provider_response`, effort `high` PASS, 0 retries, 527,419 ms, output sha256 `1f63422ddf79530f...`, `gemini-argon-audit.md` + `.provenance.json`.
- Every item was graded against the cited lines, the interface at `16dbac52` and the proofs' output, into `04-analysis.md` § Second opinion, "Argon's items":
  - 6 new findings, all Low: A-01 (`default` deletes a value), A-02 (`get_setting`'s unquoted `echo`), A-06 (two pads join their names), A-07 (a restored suspend mode never applied), A-10 (`vertical-check`, to verify), A-11 (Python 2 remnants; `vocabulary-check`'s scope).
  - Refuted by the code: A-03 (`NETPLAY_PORT` is the same key as `OS_SETTING`, and the seed sets it) and A-04 (the `wait` at `:1441` separates the two `Gambatte.opt` writers).
  - Folded: A-05 into F-14, A-08 into F-35 (my "`cd -` restores it" was wrong), A-09 into F-04.
  - Re-graded: F-03 down to Low (unmeasured); F-19 back up to Medium (the proof's `0` means neither bezel nor overlay; the Astra grade misread it). F-13 kept Low; F-43's `:239` moved into its Medium half; G-07 keeps its scope (`package.mk:115-119`).
- **Final tally: 81 findings, 0 Critical, 2 High, 22 Medium, 57 Low.** Executive Summary, AC-03 and the Quality Self-Check updated.
- `review-plan.json`: the probes moved under `probes` (the lint takes an epic reviewer's `calls` as the refutation alone).
- **Phase 5:** `05-punch-list.md` generated from the graded findings: 84 items (F-10, F-43 and A-11 split), 60 defects (a `bug` issue each), 21 renovation items and 3 items to verify. Every item carries `question:` in the `punch_index`, no item is `deferred:#336`, and the Phase 7 gate has every row `Open`. `tools/lint-audit-artifacts --phase pre-issue`: `PASS pre-issue artifacts`. All 84 criteria pass `tools/box-check`'s patterns, run offline before anything was filed.

## [Phase 6 → stage D] 16:50 — The audit issue #701 and 60 bug issues filed; paused at stage D

- **Audit issue #701**: `Audit: M6 T1 the OS scripts: launch, control and state -- 81 findings (0 critical, 2 high)`, labels `audit`, `punch-list`, milestone M6, a sub-issue of #648; one checkbox per item (84). `tools/box-check --issue 701`: `box-check: 1 issue(s), 84 open checkbox(es), 0 fail`. Its first run failed one checkbox: PL-003's title said "on the H700", which the checker reads as a device check. The title (and #704's) was reworded to name the kernel's governors, since the device is the defect's scope, not the check.
- **60 bug issues, #702 to #761**, one per defect (D-QA-051), label `bug`, no milestone, titles `Bug: ...`. Each carries the code trace (how it was found, the defect at its source from `02`, the fix, the sibling-site table, what reading cannot prove, the `Already written:` line), the `Can this be done on the VM?` line and two VM-checkable criteria. `tools/box-check --issue N` on each: `0 fail` on all 60. Before posting, all bodies passed `tools/forbidden-terms-check --stdin` (0 hits) and a credential-value scan (none).
- `05-punch-list.md` now names each item's tracker; `tools/lint-audit-artifacts --phase pre-issue`: PASS.
- Clerical: the previous entry was first headed "16:52", an estimate written without reading the clock. It is corrected to 16:42, the time of its commit `55d9bc967b` (`git log -1 --format=%cI`: `16:42:38Z`); the grading window in `04` is corrected the same way (16:34-16:42).
- **Paused at stage D.** The punch list and #701 are posted on #648, and the lane waits for the coordinator's stream briefs. The guest is down (16:37:49), and nothing runs until M7 writes `resource return`.

## [Stage E] 17:04 — The stream briefs' commit does not carry the document; stopped before S1

- The coordinator's dispatch named `docs/reviews/briefs/t1-streams.md` on `4cb05330c5`. Merged as `9634665a04` (no markers; the friction log, the work log and the index conflicted, and both sides were kept in time order). The commit carries only the work log and its index, and no ref holds the document: it is an untracked file in the coordinator's worktree, which was not read. Raised on #648 (issuecomment-6370350718). S1 starts when the document is committed and merged.
