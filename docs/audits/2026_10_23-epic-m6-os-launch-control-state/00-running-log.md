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

### [Phase 2] 08:04 — Group 3, the security list, the Q6 table, the shellcheck verdicts

- Read: `wifictl`, `rocknix-evidence` (+unit, timer), `usbgadget` (+rule, 081), `rocknix-corekeep`, `rocknix-memory-manager` (+unit), `rocknix-es-thebezelproject`, the stubs (`rocknix-update`, `rocknix-report-stats`, its masked timer), the nine unreached scripts. F-47 to F-57.
- Guest facts: `redact_credentials` misses `nmcli ... password <v>`, `cryptpw ... <v>` and `...psk <v>`; the snapshot's `top` prints names only, so no live path (F-47 narrowed); `gzip -l` works on the image's gzip; the report-stats timer is masked; `espeak` present (`say` reached); `/usr/sbin/quantum` absent and `050-audio` errors every boot (F-56); `paneladj`'s `>`/`<` clamp every value and write a stray file (F-57); `updates.batocera.org` lists answer 200 (the bezel installer alive).
- `04-analysis.md` drafted with § Renovation face Q6: 47 rows, 9 unreached (all since the import), 1 hand-run, 37 reached.
- The 16 shellcheck errors all have a verdict: 7 defects (F-09, F-10's four sites, F-16, F-56, F-57), 4 in unreached scripts, 4 benign.
