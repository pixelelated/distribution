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

### [Phase 2] 07:34 — Mechanical checks and the image-versus-tree sweep

- `02-forward-audit.md` opened: image vs tree (78 same; `runemu.sh`, `system.cfg`, `motd` differ; `099-freqfunctions` absent on x86_64; all as the brief predicts); the host checks: pkgcheck 0, last-good-scripts-test 0 `PASSED` (1,379 PASS, 0 FAIL, image busybox), settings-modes 0, wait-lock 0, usb-gadget 0 on the host (dash) and 0 on the guest (bash as sh), rocknix-info 0, melonds 0, vocabulary-check 0 but **reads none of this slice's paths** (default `--scripts` is the rclone sources plus backuptool; scoped, it judged only backuptool's strings).
- shellcheck v0.11.0 over 63 shell files: 16 errors, 319 warnings, 542 notes; the 16 errors tabled as leads, each to be read at its site.
- Next: group 1 (the launch path), file by file, writing each unit's row and findings before the next.
- 07:44 `runemu.sh` read whole; F-01 to F-08 written. F-01 (a governor value executed as a command; ES offers `default` and, on the H700, `conservative`/`userspace` with no function) is the first proposed bug; F-02 (`onlinethreads` missing on x86_64) and F-03 (exit restores racing the next launch) next. Guest proofs owed for F-01, F-02, F-03.
- 07:58 `setsettings.sh` read whole (the RetroArch half). F-09 to F-19: four proposed bugs of Medium weight (F-09 `add_setting`'s `&`, F-10 `match()` substring, F-14 the netplay host into `eval`, F-16/F-17 the MAME 2003-Plus and Gambatte option files truncated), one race to prove (F-11 the staged sed file), Lows. Both truncations date from the import `9f1fab30f6`. Guest proofs batched next, after group 1's remaining files.
