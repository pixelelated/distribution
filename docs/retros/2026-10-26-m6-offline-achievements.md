# Mini Retro: T19, the offline achievements proxy (#666)

**Completed:** 2026-10-26.
**Scope:** the T19 slice audit, stages A to F, `docs/audits/2026_10_26-epic-m6-offline-achievements/` (#1156), and its ten fix streams on `feature/m6-offline-achievements-666` (`7de4ece06d..8a0ca781c1`).
**Delta:**
- 24 punch items carrying 42 findings: 14 Resolved, 5 Deferred (#667 three, #585 two), 5 Withdrawn as recorded.
- Ten `bug`s, all Low: #1157 to #1165 from the punch list, and #1166 found in S5. Each has every criterion ticked from a host fixture, with `fixed-at`.
- One new fork patch: `022-offline-login-requires-credential.patch`. 13 cases; upstream's suite went from 866 to 879 OK.
- Eleven fixtures under the audit's `tools/`, on one bubblewrap harness (`t19-ctl-sandbox.sh`). `tools/last-good-scripts-test` stays at 1313 PASS, with five changes all ruled.

## What worked well

- **The real script in a sandbox, every time.** Each stream's before and after ran the shipped ctl, helper or service in `bwrap --clearenv`, with the image's busybox, nothing rewritten outside the scratch root, and real failures rather than shims wherever one could be made:
  - an EROFS bind for S2;
  - a stand-in listener in a private network namespace for S3;
  - a PID namespace per case for S4;
  - a read-only folder for S7's EACCES;
  - no network at all for S1's service and S9's lookup.
- **Trial worktrees ahead of the commit.** S8's and S9's suite runs went in two scratch worktrees while S7 waited for its ruling. They showed that S8 reverses nothing, and S9's 48 FAILs one stream before it landed, so no stream sat idle waiting on a 12-minute suite.
- **Asking with evidence in hand.** Both suite questions (14:33 and 15:50) went to the coordinator with the attribution runs and a trial of the proposed change already made. Each ruling came back within minutes.

## What was harder than expected

- **The suite encodes the behaviour it guards.** `tools/last-good-scripts-test` asserted two of the defects (S1, S3). Its fixtures leaned on two more: an absent image helper read as clean (S7), and the old job protocol in its stand-in (S9). The brief's two rules, the suite passing before a ctl commit and nothing changing under `tools/`, could not both hold. That cost two rulings (D-WORKFLOW-210, 211) and about forty minutes.
- **The register cannot see the coordinator's rows until hand-back.** S1's patch and S2's sources cited D-RA-049 and D-RA-050, and `register-check` failed on both. S1's failure was hidden behind `| tail -1` and committed. The amend is in the friction log. Sources cite their bug numbers now.
- **A positive that wasn't one.** At 15:49 I called #188's top-up check a check S7 reverses. The run on the ctl before S7 showed it passes there too, once the image helper exists. Corrected at 16:10 on #666, in `02` and in the commit.

## What did we discover

- **F-42 (#1166):** `exec 6<>... 2>/dev/null` sent the ctl's stderr to `/dev/null` for the rest of a run. It was found only because S5's fixture read `say`'s output from stderr.
- **The image's busybox has no `grep` or `sort`.** A harness that wraps every applet name it expects gets "applet not found" from the image's binary, not the tool. The harness now wraps only what `busybox --list` holds.
- **The host cannot hash a ROM**: the client's native module is absent. A fixture whose failure must come from the network has to use an index job (S9's case D), or every lookup is "Hash failed" and indistinguishable from the stop word.
- **022 changes the upgrade path for the player.** RetroArch signs in with the password. A device that updates and plays offline before any online launch has no recorded hash, and its offline login is refused until one online launch. This is ruled and recorded for the integration's change log (`02` § What T20 inherits).

## What adjustments are needed

Instruction-Recommendations mode: proposals for the coordinator, none applied.
- **A stream brief that touches a covered script says up front how the suite is treated** -- D-WORKFLOW-210/211's two rules -- rather than finding it at the first commit. Proposed for `docs/reviews/` stream-brief practice.
- **A row a brief rules (D-RA-049, D-RA-050) lands on the lane's branch with the brief**, or the brief says "cite the bug in sources until hand-back", because `register-check` fails closed on a source citation that names no row.
- **`set -o pipefail` in every check chain a lane writes.** One friction line so far; a second makes it a hook question.

## Time to play

The proxy sits on the launch path twice, and on the exit path once:
- **At launch, `setsettings.sh:536-540`'s port check:** one `netstat -ltn` and a grep, with no wait and no retry. A miss launches direct (T1's, unchanged).
- **At launch, RetroArch's login** reaches the proxy's `login2`. When the link is down, the proxy answers from the store.
- **At exit, the cards:**
  - the send card waits up to 10 s for the flush stamp once the queue is empty;
  - the top-up card is bounded by `TOPUP_TIMEOUT` (900 s), with the launch question over a running job (D-UI-095);
  - both are `ProxyCards`, T2's.

The record's last numbers (`docs/vm-qa-log.md`, 2026-10-05, the M7.P3 installed fallback row): interface to first frame 0.570 / 0.636 s, the exit sync's stamp 1.324 / 1.673 s, game to game 1.012 / 1.011 s. That row does not say whether the offline toggle was on.

What this slice did to them, read rather than measured (nothing was built):
- **S1:**
  - An offline login presenting a password now pays one PBKDF2 at 20000 rounds: 1.76 ms on the host; an H700 is `fix-walk-pending-image`.
  - An online login records it once, after the answer.
  - An offline login that is refused does not delay the launch; it changes what RetroArch is told.
- **S4: on the launch path.** STOP IT AND PLAY over a running top-up signals the ctl "and waits for it to be gone" (`FileData.cpp:1028` at `16dbac5211`). The ctl's EXIT trap now waits up to 5 s for the helper it ends. Before, it killed the helper and returned at once. A helper that ends on TERM takes milliseconds, so the bound is the worst case, not the usual one. That launch's number is the integration's to measure.
- **S2:** the `private-modes` pass runs at every service start (`ExecStartPre`), before the interface (`Before=emustation.service`). The first start after an upgrade chmods every file of the image cache, which may be thousands. Every later start walks the folder and changes nothing. That is time to the interface, not to play, and it is unmeasured.
- **S3 and S5 to S10** touch nothing on either path. Their runs are the scan and the top-up, which the player watches or backgrounds.

The integration build's `time-to-play` with the toggle on is the measurement. This retro names what to look for.

## What T20 inherits

All in `02` § What T20 inherits, which is the list to read:
- **The stamps and strings the pages read:**
  - `ready=unknown`;
  - `why=` tokens new to the table: `STAMP_UNWRITABLE`, `RESULT_UNREADABLE`, and `TOOK_TOO_LONG` in `topUpWhy`;
  - the page's `done ...|unknown|...` line.
- **The ctl subcommands they run:**
  - `disable`'s new exits, 2 and 1, where it exited 0;
  - `stop`'s exit 1 on a failed stop;
  - `account`'s exit 2 on a malformed row;
  - the new `private-modes` verb.
- **The consent setting's name:** `usage_stats_consent` (unchanged).
- **The handed items:**
  - PL-13's staleness contract;
  - PL-17's refresh helper, with #224's row;
  - PL-18's `NO_GAMES_FOUND` row and the `have_account` comment.
- **022's refusal,** as RetroArch shows it, and the upgrade path that goes with it.

## Scoped audit findings (Step 2.5)

- **AC conformance:** PASS on the host. Every bug's criteria are ticked with their `stage-e/` artifacts. What a guest or an image must show is named `fix-walk-pending-image` in each bug and in `02` § The streams.
- **Cornerstone spot-check:** PASS.
  - Fixtures fail closed: exit 2 on a run that could not be made.
  - Guards fail closed: `cannot_tell` over a guess.
  - Every writer is read back. No `rm -rf` outside the removal shape.
- **Interaction-defect scan:** PARTIAL.
  - S4's watchdog and S5's `stamp()` exits meet in the EXIT traps; read, and both run in the S4 and S5 fixtures.
  - 022 against RetroArch's own login retry is not run: no emulator on the host.
- **Futro prediction verification:** n/a. No futro predicted the stage-E streams; the area epic's futro predicted the suite as a guard, 1 of 1 confirmed.
- **Housekeeping (full-suite scan):** PASS.
  - `tools/last-good-scripts-test` 1313 PASS at every stream's commit.
  - Upstream's own suite 879 OK on the pin plus 022.
- **Harness self-coverage:** PASS.
  - The harness's two defects (missing applets; `say` hidden by F-42) were each found by a fixture that failed for the wrong reason.
  - Both are fixed and noted in `00`.
- **Check 7, step 5, where a fix landed:** every fix's FAIL is recorded before it, on the real script.

## Addendum, after the retro (the ruling of 16:42 UTC on #666)

- **The upgrade-path discovery became stream S1b** (D-RA-051, #1157). 022 is amended: while no hash is recorded for the configured account, its password is answered unverified, as before, and said once in the service's log; the first online login records the hash.
  - Before: 2 of 15 FAIL on 022 as landed. After: 15 of 15; upstream's suite 881 OK.
  - `stage-e/s1b-before.txt`, `s1b-after.txt`.
  - The player meets no change on the upgrade path. The change-log note this retro anticipated is no longer owed.
  - **Time to play:** the no-hash path compares nothing, so it costs less than S1's PBKDF2.
- **The three proposals, ruled:**
  1. A stream brief that touches a covered script says up front how the suite is treated: adopted; plan § 6b.
  2. *A source cites the bug, the docs cite the row*: adopted, plan § 6b.
  3. `set -o pipefail`: one friction line; a second makes it a hook question.
