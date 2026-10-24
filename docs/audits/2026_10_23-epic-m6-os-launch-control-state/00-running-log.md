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

## [Stage E, S1] 17:20 — Stream S1, the netplay host and the eval: PL-001 F-14 #702 (High), PL-007 F-15 #708

- The coordinator's tip `5ac1b27eed` was merged as `0f68957266` (the friction log conflicted, both lines kept; no markers). `docs/reviews/briefs/t1-streams.md` (from `289a95eb05`) was read whole.
- **One difference from the document, reported on #648:** it says a `#!/bin/sh` script is "proven under dash". The image has no dash: its `/bin/sh` is bash (stage A, on the guest; `$QA_SYSTEM_ROOT/usr/bin/dash` is absent). So S1's cases run under the image's own bash 5.3 (`$QA_SYSTEM_ROOT/usr/bin/bash`), and both scripts are `#!/bin/bash`.
- **The test first:** `tools/last-good-scripts-test` sections **ai** (#702, with A-05) and **aj** (#708). They lift `set_netplay`, `add_setting`, `clear_setting` and `game_setting` from `setsettings.sh`, and the `EXTRAOPTS` splice from `runemu.sh`, then `eval` through a stub RetroArch that records its argv, under the image's bash.
- **The failing run, on the unfixed tree** (`0f68957266`, 17:10:43-17:19:09, `QA_SYSTEM_ROOT=<M7 build root>/image/system tools/last-good-scripts-test`, rc 1): `8 CHECK(S) FAILED, 0 SKIPPED`, all eight in ai and aj, and every other section passed:
  - the marker was created;
  - the argv was cut to `[-L][/tmp/core.so][--connect][127.0.0.1]`;
  - no refusal was logged;
  - the host was written into the appendconfig;
  - A-05's stray line ran;
  - the client's port was written as `55435 = "55435"`;
  - the TGB Dual options were cut to the four link keys.

  The controls (an IPv4 host, an IPv6 host, the link key written once) passed.
- **Sibling sites** (`03` § 3.6.5, section B):
  - fixed here: `setsettings.sh:683`, `:688` -> `runemu.sh:355`, `:500`;
  - `:787` (`--set-shader`): its `eval` half is closed by `runemu.sh`'s check, and the quoting of a space is S2's (the document gives S2 that line);
  - `:1048-1087` and `:1123`: S2 (F-19); `runemu.sh:378` and `:385`: S3 (G-05); `rocknix-memory-manager:99` and `rocknix-config:39`: S7.
- **Queued for the guest** (until `resource return`): (1) #702: `global.netplay.host='127.0.0.1;touch /tmp/t1-f14-marker;'`, a client launch through the tree's `runemu.sh` with the stub bound over `/usr/bin/retroarch` (`group1.sh`'s F-14 block), expecting no marker, the full argv and the refusal line in the log; the control `127.0.0.1`. (2) #708: a `tgbdual` client launch keeping a custom `TGB Dual.opt` line, with `netplay_ip_port` in `/tmp/.retroarch.cfg`.
- **17:29: the first passing run found a fault in the test.** On the fixed tree (17:19:45-17:28:10, rc 1), all of ai and two of aj's three checks passed. The third failed with `the link key is not written exactly once`, which meant the TGB Dual block's `sed -i` deleted nothing before the `>>`. Read directly, the program (backslash-newline between its four commands) is accepted by the image's busybox `sed`, which deletes the keys, and refused by the host's GNU `sed` 4.9 (`unterminated address regex`). `np_run` was running the lifted functions on the host's PATH. So the failure was the test using host tools, against the briefs' rule, not the fix. `np_run` now puts the harness's busybox shims (`${TMP}/bbin`) first on PATH, and the section counts a SKIP when no image busybox is given.
- A rerun from a copy of the harness in the scratchpad was a mistake (its root comes from its own path: `source checkout has no rclone recipe`). It was stopped by its task id, and nothing was left running. The pair of runs then started from the tree's harness: `BASE_REF=40a274d736 --old` (the unfixed scripts), then the tree.

## [Stage F, guest cycle 1] 18:35-18:43 — S1's and S2's guest proofs and the four verifications; the guest down again

- `resource return` (M7's line 18:34:04, relayed on #648 issuecomment-6372059653). The guest was booted from the kept `t1.qcow2` at 18:35:02 (`generic-x64-vm run --headless --daemonize --pidfile $A/qemu.pid ... --vnc 19 --ssh-port 10032`, pid 3167085). SSH answered at 18:35:10, with BUILD_ID `069fc270442134fe771258418adf4e666e0473fb` as at stage A.
- **S1** (`.qa-scratch/t1/proofs/s1-guest.sh`, `.out`; S1's committed `runemu.sh` and `setsettings.sh` at `f3261a5b78` bound over the image's copies; a stub RetroArch):
  - The first run passed no netplay arguments. `runemu.sh` deletes `netplay.mode` and sets it from the launch's own `--connect`/`--host` (`:239-255`), so the block never ran and nothing was shown. The proof now launches with `--connect 192.0.2.1 --nick T1`, as the interface does.
  - **#702:** no marker; the full argv `[-L] ... [--config] ... [--appendconfig] ... [T1Test.nes]`; `exec.log` carries `setsettings: Refused the netplay host (35 characters): ...` and 0 lines with the value. My first count read `exec.log` from a saved line number, and `runemu.sh` starts the file again at each launch; the whole file has the line. The control `127.0.0.1` reaches `[--connect] [127.0.0.1]`.
  - **#708:** `TGB Dual.opt` keeps `t1_custom_option` with each link key once; `netplay_ip_port = "55435"`; `[--connect] [192.0.2.1]`.
  - #702 and #708 are ticked with these artifacts; PL-001 and PL-007 are resolved in `05` and #701.
- **The four verifications** (`verify-guest.sh`, `a10-guest.sh`, and their `.out`; the image's own scripts; a 32 KiB cartridge built from `tools/emulator-exit-test`'s recipe, named `T1 Verify.gb`):
  - **F-08's timing:** `game-guides-tool` takes 5 ms on each of three runs. That half is withdrawn; F-08's Q7 half stays in S3.
  - **F-27:** a default launch (no `shaderset`, so `--set-shader /tmp/shaders/`) logs only RetroArch's own GLSL stock shaders found, with no error or failed load. **Withdrawn.**
  - **A-10:** a launch through the interface's `POST /launch` puts five `sh -c` wrapper lines first in `ps`, each with the path escaped (`T1\ Verify.gb`), and `vertical-check`'s parse gives the whole path. Only a launch made outside the interface, with the script's own argv first, cuts it at the space (`[/storage/roms/gb/T1]`); no player path does that. **Withdrawn.**
  - **F-18:** confirmed. RetroArch runs with `global_core_options = "false"` and `rgui_config_directory = ~/.config/retroarch/config`, so it reads `config/<Core>/<Core>.opt`, and `setsettings.sh` writes Kronos under `Kronos/config/Kronos/`. Filed as **#762** (`box-check` 0 fail), fixed in S2 as group 7 with harness case au.
- **S2** (`s2-guest.sh`, `.out`; the working tree's `setsettings.sh`, S2's final state, sha256 `193d2934eecd87d7...`, bound over the image's copy):
  - #705: hardcore `false` under netplay; analogue unset `"1"`, `0` `"0"`.
  - #707: 0 of 200 rounds lost a key.
  - #706: neogeo `true`/`true`, neogeocd `false`/`false`.
  - #731: the 64-bit core (ELF class 2) gets `.../64bit/video/Normal2x.filt`.
  - #709: three lines kept, tate `enabled`.
  - #710: custom and link mode kept, each palette key once after two launches.
  - #711: the overlay applies under the shipped `thebezelproject`. The guest's settings set the N64 video core, so this run did not exercise the unset half; harness case aq proves it.
  - #732: `config_save_on_exit = "false"`.
  - #733 and #760: with two fixture pads bound over `/proc/bus/input/devices`, no marker, and the hotkeys from `Pad One.cfg`.
  - #762: `config/Kronos/Kronos.opt` reads `2x`, and no `Kronos/` folder is made.
- **A mistake in the S2 proof's restore, repaired.** `/tmp/joypads` is an overlay mount (`tmp-joypads.mount`: lower `/usr/share/libretro/autoconfig`, upper `/storage/joypads`). The restore's `rm -rf /tmp/joypads` whited out all 518 image autoconfigs in the upper layer, and the `cp -a` back nested the backup as `/tmp/joypads/s2.joypads/`. The merged view then had no autoconfig at its top level.
  - Before the proof, the merged view matched the image layer exactly (518 of 518 identical, none extra), so the upper layer had held nothing that showed.
  - Repair: `systemctl stop tmp-joypads.mount`; remove the 518 whiteouts and the nested directory from `/storage/joypads`; `systemctl start tmp-joypads.mount`. The merged view is the image's 518 again, all identical, with the upper layer empty.
  - The proof now removes only the fixture file it added.
- The guest was stopped at 18:43:40 by `tools/vm-stop` (rc 0, pid 3167085 exited), with the queue empty. It comes up again for S3's proofs.

## [Stage E, S2] 19:00 — Stream S2, `setsettings.sh`: eleven items in seven commits

- **Items:** #705 F-09, #707 F-11, #706 F-10, #731 F-10b, #709 F-16, #710 F-17, #711 F-19, #732 F-12, #733 F-13, #760 A-06, and #762 F-18 (from the verification).
- **The test first:** `tools/last-good-scripts-test` sections ak to au. Every function and array in `setsettings.sh` is lifted (43 in the unfixed file, 47 in the fixed) and run under the image's bash and busybox. Each case runs in a `bwrap` sandbox with its own `/storage` and `/tmp`, and the pad cases bind a fixture over `/proc/bus/input/devices`.
- **Four faults of my own, caught before any commit:**
  1. The lift ended `get_bezel_infos` at its JSON heredoc's bare `}`; the lift now skips heredoc bodies.
  2. `s2_new` did not create `ra/`, so `al`'s first round and its refusal fixture failed for the fixture's sake.
  3. The library's own `log` replaced the stub; the stub now comes after the library.
  4. **A bug in the #760 fix itself:** in busybox `awk`, `exit` inside a rule still runs `END`, so the pad's name was printed twice and no autoconfig matched. The fix now sets a `done` flag. The harness caught it, and it would have shipped otherwise.

  After faults 1 and 3 changed the harness, both runs were repeated.
- **Found while reading:** with F-17 fixed, Gambatte's four palette keys (`twb64_1` to `_3`, `pixelshift_1`) would have piled up, one more copy per launch, because the old one-line cut had been hiding it. #710's fix deletes them before re-adding them.
- **The failing run** (`BASE_REF=f3261a5b78 tools/last-good-scripts-test --old`, 18:41:20-18:49:51, rc 1): 15 checks failed, all in ak to au, and none before ak.
- **The passing run** (`tools/last-good-scripts-test`, 18:49:51-18:58:32, rc 0): `PASSED`.
- **The guest:** 18:42 (stage F, cycle 1 above), all eleven items hold.

## [Stage E/F, S3] 19:28 — Stream S3, `runemu.sh` and the launch helpers: eleven bugs and two renovation items in seven commits

- **Items:**
  - **bugs:** #704 F-01, #726 F-02, #736 F-25, #727 F-03, #728 F-04, #729 F-06, #730 F-07, #757 G-05, #737 F-26, #734 F-20, #735 F-23;
  - **renovation:** F-05 (Q6) and F-08 (Q7).

  A-10 was withdrawn at cycle 1.
- **Lines kept untouched:** the M7 candidate's (`runemu.sh` 1-10, 331-340) and S1's (320-360, 495-505).
- **The test first:** `tools/last-good-scripts-test` sections av to bf. Functions are lifted (heredoc bodies skipped) and top-level blocks lifted between their bounding lines. `s3_block` passes its regexes through `ENVIRON`, since `awk -v` strips backslashes. The cases run under the image's bash and busybox in a private sandbox.
- **The failing run** (the unfixed tree at `3352bba83e`, 19:08:03-19:16:44, rc 1): 12 checks failed, all in av to bf. The two controls passed, and nothing before av failed.
- **The passing run** (19:17:13-19:25:55, rc 0): `PASSED`.
- **Two things decided by reading:**
  - **#737:** the issue's "fix the doubled `>`" would drop every `</inputConfig>` closing tag. The fix removes that dead half instead and keeps the output unchanged (said on #737, issuecomment-6372835323).
  - **#730:** `--core=` and `--emulator=` are read as whole arguments with the last one winning, as the launcher reads them (the T1 brief's corrected seam sentence).
- **The guest** (cycle 2, 19:26:18-19:27:18; the tree's `runemu.sh` with `run`, `001-functions`, `100-gamecontroller-functions` and S2's `setsettings.sh` bound over the image's copies, and a stub RetroArch; `.qa-scratch/t1/proofs/s3-guest.sh` and its `.out`):
  - #704: no `command not found`, and the fallback line in `exec.log`.
  - #726: no `onlinethreads` error.
  - #727: a launch over a 3-second restore waits for it (4.4 s, including the 1-second settle).
  - #729: the NVRAM is removed, and `My` and the ROM are kept.
  - #730: the core is `nestopia`.
  - #757: `mapper.txt` reads back the name verbatim.
  - #737, on the real `xmlstarlet`: the unfixed functions print `[: too many arguments` twice (`line 139`) and the fixed ones print nothing, with the same db line. The image has no `/usr/bin/list-guid`, so `build_connected_devices_es_input` was replaced in the shell by a copy of the fixture.
  - #734/#735: nothing printed into the callers.
  - #728 has no fan on the guest; harness case az is its proof.
  - The guest was stopped by `tools/vm-stop`, rc 0.
- **Deferred to stage F's end** (the briefs list them again at the branch tip): `tools/emulator-exit-test --vm` and `tools/time-to-play --vm` beside the stage-B numbers, once all seven streams are in the scripts they measure.

## [Stage E, S4] 19:55 — Stream S4, the settings library: three bugs and one comment, written small

- **Items:**
  - **fixed:** #756 G-03 (the `=` boundary), #759 A-02 (`printf '%s\n'`, literal dots in keys), #758 A-01 (`set_setting_value`), and F-22 (a comment at `wait_lock`'s trap).
  - **deferred and moved:** F-21 #712 is deferred to #563 (said on #712). F-24's fix needs `automount`, which is S6's, so it moves there (the briefs' rule for a file outside the stream).
- **#758's shape differs from the issue's** (said on #758, issuecomment-6373181296): `default` as "remove" is a contract `raofflineproxy-ctl:539`, `wifictl:383` and the harness's section c rely on. So S4 adds `set_setting_value` and keeps `set_setting` as it is; `setrootpass:45` (S6) and `wifictl:460` (S7) move to the new function in their own streams.
- **The test first:** `tools/last-good-scripts-test` sections bg to bi, in S3's sandbox under the image's bash and busybox.
  - **unfixed** (`BASE_REF=b11644ce58 --old`, 19:36:02-19:44:46, rc 1): 3 checks failed, all in bg to bi.
  - **fixed** (19:44:46-19:53:28, rc 0): `PASSED`.
- **Queued for the guest** (S4 and S5 together): the `get_setting` readings #756 and #759 name, and #758's criterion 1, once S7 has moved `wifictl`.

## [Stage E, S5] 21:41 — Stream S5, the updater, the sysconfig unit and the defaults

- **Items, in the briefs' order:** #713 G-01 and #738 F-28 (`003-upgrade`), #715 F-32 and #721 F-44, #716 F-33, #740 F-34, #741 F-35 (`post-update`), #739 F-30 (`save-sysconfig.service`), #724 F-63 (`package.mk`, `post-update`), G-02 (a comment), F-65 (`rocknix-settings`), F-62 (`package.mk`). F-46 stays as it is, with the reason on #694. F-45 #745 is deferred to #563.
- **The test first:** `tools/last-good-scripts-test` sections bj to bt. `post-update`'s blocks are lifted between their bounding lines and `003-upgrade` runs whole with a stub `post-update`, all in S3's sandbox under the image's bash and busybox, with the image's `/usr/config` moved to a fixture.
  - **unfixed** (`BASE_REF=4ded5446cb --old`, from the tree, 21:32:06-21:40:50, rc 1): 15 checks failed, all in bj to bt.
  - A first unfixed run (21:23:07-21:31:29) ran a copy of the harness from the scratchpad. It failed the same 15 checks plus five outside S5, because the copy looks for `tools/vm-qa`, `tools/melonds-upgrade-test` and others beside itself. It is not evidence; the run from the tree is.
- **M7 window** (the coordinator, 21:36): the guest was already down (since 19:27:18). Acknowledged on #648 at 21:41 and in the host coordination file.
  - **fixed** (from the tree, 21:42:03-21:50:49, rc 0): `PASSED`; the 18 checks in bj to bt pass.
  - `tools/pkgcheck rocknix`: rc 0, no findings, on the series' last recipe. `tools/melonds-upgrade-test` over the fixed `post-update` with the image's busybox: rc 0, every control PASS.
- **Commits:** head `d0ee0f568e`; `9c4001b0b6` (#713, #738), `9f688bb0b6` (#715, #721), `a3d6cecee6` (#716), `fa8b12610d` (#740), `c1e02af9e5` (#741), `78967e7237` (#739), `e5e3a36c1f` (#724), `3e555f72d5` (G-02), `97f5423b4a` (F-65), `ac466e5a39` (F-62), `f324507c1d` (a comment S4's `cadc16429d` had put between `set_settings` and its comment).
  - One correction before the push: #715's message first said the unfixed `bl` waited 0 ms; the run's line is 3 ms. Groups 2 to 11 were recommitted from their intermediates with the line corrected.
- **Shapes that differ from an issue's fix line, said where they belong:**
  - **#721:** the `dpms` delete is removed, not put behind a marker. The old shipped value is `1`, the same as a player's choice, so a one-time delete would still take a player's choice away once.
  - **F-46 is withdrawn:** EmulationStation reads all three `updates.*` keys (`GuiMenu.cpp:1527-1539`, `NetworkThread.cpp:87` at the pin `16dbac5211`). And `system.cfg` cannot carry a comment, because `chksysconfig`'s `valid()` refuses a line without `=` and the shutdown backup would stop. The note is on #694.
  - **F-65:** a write to `system.cfg` is refused rather than locked. The S4 brief gave these lines to S4 for #758, which did not need them; they are changed here with the row.
- **Found and not fixed (outside S5's files):** `userconfig-setup` (the systemd package) makes the same two copies at first boot as #740's, and with no `/storage/.ssh` it makes a file of that name. Said on #740.
- **Queued for the guest** (after resource return, with S4's readings): #713 and #738 (`003-upgrade` with a stub), #715, #716, #721, #740, #741 (`post-update`'s blocks against the tree), #724's live file and record, and F-65's refusal. #724's seed mode and #739's `systemctl show` need an image built from this branch, so they wait for stage F's image, or are recorded as such there.

## [Stage E, S6] 22:20 — Stream S6, the destructive and state scripts

- **Items, in the briefs' order:**
  - `updateabl`: #703 F-67 (High).
  - `installtointernal`: #717 F-39, #718 F-40, #744 G-04.
  - `automount`: #719 F-42 with F-24 (moved from S4), and #720 F-43 with F-43b.
  - `factoryreset`: #742 F-37, #743 F-38.
  - `setrootpass`: #714 F-29, with #758's carry-over to `set_setting_value`.
  - Renovation: F-36 (`factoryreset`), F-41 (`automount`), F-31 (the unit).
- **The test first:** `tools/last-good-scripts-test` sections bu to bF. Nothing touches a device: the ABL slots are files, the internal card is fixture `/proc` and `/sys` listings, and parted, mount, smbpasswd, syncthing and systemctl are stubs that record their calls. Everything runs under the image's bash and busybox.
  - **unfixed** (`BASE_REF=52acfb315a --old`, from the tree, 22:10:30-22:19:19, rc 1): 14 checks failed, all in bu to bF.
  - **A first unfixed run** (22:00:33-22:09:21) had a fault in my own `bF` case: it ran the untransformed `setrootpass`, which sources the host's `/etc/profile`, where `set_setting` does not exist. The case was corrected and the run repeated; the repeat is the evidence.
  - **fixed** (from the tree, 22:29:47-22:38:38, rc 0): `PASSED`. `tools/pkgcheck rocknix`: rc 0.
  - **The first passing run (22:19:45-22:28:33, rc 1) caught three of my faults, now fixed:**
    - my new `disk_of` and `internal_disk` carried a comment after `{`, so the harness's lifter missed them;
    - I had refactored `external_node_present` onto them, which broke #308 F-PB-13's case, which lifts that function alone; it is now left as it was;
    - #714's new `$6$` contract refused the #198 case's fake `cryptpw` (`CRYPT<hex>`). That fixture now prints the `$6$` prefix the real one does, and its profile gives `set_setting_value`, in #714's own commit, so the head's harness is the one the failing run used.
- **Commits:** head `e2771ee374`; then:
  - `5f0e3d8a60` (#703), `55ff8ffde7` (#717), `e631f7793f` (#718), `98b30dca58` (#744);
  - `2710c17f43` (#719, F-24), `f9108ae7d3` (#720, F-43b);
  - `f09c3df562` (#742), `faffa32bd7` (#743), `5944a8c1bc` (#714, #758);
  - `5707827267` (F-36), `9434ea7fda` (F-41), `3c9b9dc891` (F-31).
- **Shapes that differ from an issue's fix line:**
  - **#720:** the card under `/storage` is never a candidate (the fork's rule since #308). The issue's "the removable card's own path" is not done: whether sysfs marks an SD card removable, and what a UFS disk shows when the device boots from SD, are device facts the VM cannot give, and a wrong rule unmounts every handheld's games card. Said on #720.
  - **#743:** the image's XDG-state readers come from the build root's library strings: GLib, Qt6Core, mpv and pipewire. The guest's listing is queued.
- **Queued for the guest** (after resource return):
  - every S6 bug's criterion 1, run against loop files and fixtures;
  - F-24's ten boots;
  - F-36's, F-41's and F-43b's readings.
  - F-31's `systemctl cat` needs an image built from the branch.

## [Stage E, S7] 23:00 — Stream S7, the control scripts and fragments

- **Items, in the briefs' order:**
  - **Bugs:** #722 (`paneladj`), #723 (`008-perfmode`), #750 (`050-audio`), #751 (`055-hdmi-check`), #752 (`handle-hdmi-hotplug`, with a `pause` verb in `usbgadget`), #761 (`suspendmode`), #753 (`volume`), #748 (`rocknix-memory-manager`), #749 (the bezel project), #746 (`wifictl`'s gate), #758 (`wifictl:460` and `:388`, with `set_settings_values` in `001-functions`), and #754 with #755 (`rocknix-config`).
  - **Renovation:** F-50, F-51, F-52, F-66, F-69, A-11a, A-11b.
  - **Not changed:**
    - F-47: the briefs change the filter only if a value is printed today, and the audit's guest check found none.
    - F-55: eight of the scripts are upstream's and stay, with a line on #585. `rocknix-retroachievements-info` goes with #563, since upstream removed it in `03204074ef`.
  - **Deferred:** F-49 #747 to #563, and F-68 #725 to D-SYS-014.
- **The test first:** `tools/last-good-scripts-test` sections bG to bY. Panels, radios, the gadget and every service are stubs; sysfs and `/proc` are fixtures. The bezel project runs whole in the sandbox, against local lists.
  - **unfixed** (`BASE_REF=eb1442f5a7 --old`, from the tree, 23:10:40-23:19:33, rc 1): 22 checks failed, all in bG to bY.
  - **A first unfixed run** (22:50:30-22:59:29, rc 1, the same 22) had two faults in my own cases. The first passing run showed them:
    - `bM`'s stub `pactl` was never reached, because `001-functions` puts `/usr/bin` first on `PATH`;
    - `bQ` stopped at `saved_state`, which the lifter misses (a comment after its `{`).

    Both cases were corrected in this head and the run repeated; the repeat is the evidence.
  - **fixed** (from the tree, 23:20:09-23:28:58, rc 0): `PASSED`. `tools/pkgcheck rocknix`: rc 0.
  - **The first passing run (22:59:58-23:08:53, rc 1, 6 failed)** showed my two case faults above, and four older `wifictl` join cases failing. Those cases' `001-functions` stand-ins (section u's profile and the p7 Wi-Fi block's) had no `set_settings_values`. They gain it in #758's own commit, as the contract now has it.
  - `tools/vocabulary-check`, run against the local ES checkout (not the pin): 135 strings judged where the old tool judged 122. None of the 13 new ones is wrong, and its 15 failures are the same 15 before and after, all in that checkout's interface strings.
- **Commits:** head `4019b8d093`; then:
  - `2c6d15f89e` (#722), `69c9a01ed6` (#723), `875b2f101a` (#750), `8665eaf291` (#751), `d34ca8a56f` (#752);
  - `0e6db61073` (#761), `082f79c56f` (#753), `b41a9dc3c2` (#748), `0152f17fe0` (#749), `4836351958` (#746);
  - `852954094b` (#758), `f92f35d5fc` (#754, #755);
  - `57da0b3b21` (F-50), `05312fd5d2` (F-51), `41ba51701f` (F-52), `ff35688a26` (F-66), `557b6368f4` (F-69), `9b131d110b` (A-11a), `7fc0d2a58e` (A-11b).
- **Shapes that differ from an issue's fix line:**
  - **#722:** the range stays the script's 1 to 100. The brief's "reads the panel's range from the kernel" needs `drm_tool`'s range output, which no panel on the VM shows; the fix line is the numeric comparison.
  - **#752:** `usbgadget` gains `pause`, because `stop` writes `USB_MODE=disabled` and would turn off the player's choice for good.
  - **#754:** `setRootPassword` refuses rather than being removed, since upstream carries the script.
  - **#746:** only the five network verbs exit 2.
- **For the coordinator:** #761's criterion says "leaves `sleep.conf` without `SuspendState=` (the freeze shape)", but the freeze shape the script writes is `SuspendState=freeze standby mem`. The harness checks that shape.
- **#701:** 33 of 84 checkboxes ticked: PL-074, PL-077 and PL-084 resolved, PL-057 withdrawn (this line first said 32, a miscount). PL-065 is deferred to #585.

## [Stage E, tails] 23:45 — the two tails on S1's lines: T2's nick lead (#730) and D-WORKFLOW-192's launcher side

- **Items:**
  - **#730, T2's lead (#648, 20:30):** `runemu.sh` takes the argument after `--nick`, `--port`, `--connect` and `--netplaymode` as that flag's value, so a nick that is itself an option word is not read as the core.
  - **D-WORKFLOW-192 (#648, 21:29):** the netplay markers are read from whole arguments, with the spectator before the client. `set_netplay` gains a spectator case (`netplay_start_as_spectator`). `--mitm-session=<id>` reaches RetroArch's command when it is a word. Refs #702, #708, #776.
- **The test first:** `tools/last-good-scripts-test` sections bZ, ca, cb, cc (cb through the S1 netplay runner).
  - **unfixed** (`BASE_REF=377f9545d4 --old`, from the tree, 23:34:33-23:43:25, rc 1): 6 checks failed, all in bZ to cc.
  - **fixed** (from the tree, 23:43:59-23:52:47, rc 0): `PASSED`.
- **Commits:** head `d8d2b5e9c0`, `9011f1e4a0` (#730), `0f7558cff7` (D-WORKFLOW-192).

## [Stage F, host half] 00:00 — the stage-B checks again at the branch tip (`991c10e651`), during the M7 window

The guest was not brought up at the 23:47 return: the tails were finishing on source, and the 00:07 window followed. It was acknowledged on #648 and in the host coordination file at 23:53. The host-side checks need no guest, so they ran now. Output is in `.qa-scratch/t1/checks-f/`.

| Check | Stage B | Stage F (00:00:30-00:00:39) |
| --- | --- | --- |
| `tools/pkgcheck rocknix` | 0 | 0 |
| `tools/settings-modes-test` (the tree's `001-functions`, `chksysconfig`, the image's busybox) | 0, `PASS refuse-rename` | 0, `PASS refuse-rename` |
| `tools/wait-lock-test` | 0, `PASSED` | 0, `PASSED` |
| `tools/usb-gadget-test` (host `sh`) | 0, 72/72 | 0, 72/72; and under the image's bash, 0, 72/72 |
| `tools/rocknix-info-test` | 0, 12 controls | 0, 12 controls |
| `tools/melonds-upgrade-test` | 0 | 0 |
| `tools/vocabulary-check` (default) | 0, 163 judged, 0 wrong | 0, 176 judged, 0 wrong (the 13 from A-11b's three scripts) |
| `tools/vocabulary-check --scripts .../rocknix/sources/scripts` | 0, 128 judged | 0, 141 judged, 0 wrong |
| `tools/last-good-scripts-test` (`QA_SYSTEM_ROOT`) | 0, `PASSED` | 0, `PASSED` (23:43:59-23:52:47, at `0f7558cff7`, the last code commit) |
| `tools/box-check --issue N`, #701 and #702 to #762 | - | 0 fail on every one |
| `tools/lint-audit-artifacts` (resolution) | - | 1: 46 rows still Open, each waiting for its guest or image reading; `--phase pre-issue` PASS |

- **The guest half waits for resource return:** batches q1 (S3's open criteria, S4, S5), q2 (S6) and q3 (S7 and the tails), then `emulator-exit-test --vm` and `time-to-play --vm --quick` with the tree's `runemu.sh`, `setsettings.sh` and `001-functions` bound over the image's for the run. The cycle is driven by `.qa-scratch/t1/proofs/qrun.sh` (`up`, `copy`, `batch qN`, `ttp`, `down`), and the guest goes down between batches when a window asks for it.
- **A first `vocabulary-check` run** used the local ES checkout, which is not the pin; it showed that checkout's 15 interface failures. The default checkout, `qa-integration` at the pin `16dbac521`, is stage B's and the evidence.

## [Stage F, guest half] 00:44 — the three batches, the two timing runs, the lint and the checkbox checker

The coordinator's resource return was at 00:24. Each batch had its own boot from `t1.qcow2` (SSH 10032, VNC 19), with `tools/vm-stop` between them. Before every batch the tree's scripts at `ff95b3a211` were copied to `/storage/.qa-t1/`, and their sha256 matched the tree. The driver is `.qa-scratch/t1/proofs/qrun.sh`.

- **q1** (S3's open criteria, S4, S5), 00:25-00:27:09.
  - Ticked: #727, #736, #756, #759, #713, #738, #715, #721, #716, #740, #741.
  - Open: #728 (the fan input was synthetic: `DEVICE_HAS_FAN` forced; P-05) and #724 (the seed's mode needs an image).
  - A first run (00:25:42) had a fault in my proof: a `sed` rewrote a path it had just inserted, so #740's block was skipped. The rerun at 00:26:36 is the evidence.
- **q2** (S6), 00:30-00:31:55. Loop devices, a private mount namespace, nothing on the guest's own disk.
  - Ticked: #703, #717, #744, #718, #719, #742, #743, #714, and F-36's list.
  - Open: #720, whose criterion asks for loop devices and removability, not the fix's shape. Put to the coordinator.
  - Two faults in my proof, rerun on the same boot: #744's stub was not executable (rerun 00:31:11), and #714 sourced the image's `001-functions` (rerun 00:31:30 with the tree's bound).
- **q3** (S7, the tails), 00:32-00:43:23.
  - Ticked: #722, #751, #752, #761, #753, #749, #746, #754, #755; F-50, F-52 and A-11a shown; the tails' argv (#730, D-WORKFLOW-192).
  - Open:
    - #723 and #750: their boot-journal halves need an image.
    - #748: this kernel has no swap and the image no `swapon`; the H700 build roots have it.
    - #758: the guest has no Wi-Fi device.
  - #755's edit is from a rerun (00:33:19): my lifter missed `bato_config_set_value () {`, with its space before `()`.
- **Criterion 2** (the unfixed run first, both runs in the fix commit) ticked on all thirty S5-S7 bugs, from their harness runs.
- **`tools/emulator-exit-test --vm`** (00:33:3x-00:33:58, the tree's `runemu.sh`, `setsettings.sh` and `001-functions` bound): `PASSED`.
- **`tools/time-to-play --vm --quick`** with the tree's scripts: first frame **0.73 s**, next game's first frame **1.01 s** (n=1).
  - Stage B measured 0.64 s and 1.01 s. With the image's own scripts, stage A read 0.76 s and stage B 0.64 s, a 0.12 s spread at n=1 that covers the difference, so no stream is named as having moved a number.
  - The run ends `Not a pass` on the exit sync with no cloud, as in stage B under `--no-configure-remote`.
  - **Two runs did not count** (00:33:58 and 00:38:14): the tool reboots the guest when it seeds its ROM or changes the two cloud settings, and the reboot dropped the binds, so those runs measured the image's `runemu.sh` (hash `a81a2bd04cea`, not the tree's `3fca2f25ada9`).
  - The counted run (00:40:56-00:43:07) bound the scripts from a temporary `/storage/.config/autostart/` hook; the guest's `runemu.sh` hashed as the tree's after the tool's reboot. The hook was removed, the cloud settings put back unset as before, and the probe ROMs are gone.
- **`05`:** 66 rows Resolved or Withdrawn, 18 Deferred:
  - 9 to a fix-pending-image row, the coordinator's after the merge: #723's and #750's journals, #724's seed, #739, F-24, F-31, F-41, F-43b and F-51;
  - 3 as device facts: #728, #748, #758;
  - #720's wording, put to the coordinator;
  - and the five from the briefs: #563 (F-21, F-45, F-49), D-SYS-014 (F-68), #585 (F-55).
  - `tools/lint-audit-artifacts` (resolution): **PASS**.
- **#701:** 66 of 84 ticked. `tools/box-check`: 0 fail on #701 and on #702-#762.
