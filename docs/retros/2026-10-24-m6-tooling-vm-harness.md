# Mini Retro: M6.P2 T12, the VM harness (#659)

**Completed:** 2026-10-24
**Scope of this retro:** the T12 lane, Independent depth, covering:
- stage A, the slice's 60 paths, read with the bytes equal to `next`'s `8ebaf8daad`;
- the audit, stages A to D (`docs/audits/2026_10_24-epic-m6-tooling-vm-harness/`, #984's 23 items);
- the fix streams S1 to S13 of the coordinator's `t12-streams.md`, plus S5b, which the scripts suite's runs turned up;
- the two short guest cycles;
- the close-out.

Not retro'd here, because they are not this lane's:
- the coordinator's acceptance;
- the merge to `next`;
- the frame baseline, which is the maintainer's on #346.

**Commits:** `reviewed-at` `facb2ae523`, `fixed-at` `159ed33562`. The tool fixes run from `0ecbbb9339` to `3eba8ce4b0`, 45 commits under `tools/`.

## What the slice did to the two time-to-play numbers

**The slice changed neither number.** Each figure is one sample on guest a, image `069fc2704421`, `webdav`:

| Number | 2026-10-06 record (`docs/vm-qa-log.md`) | cycle 1, 22:29 (`cycle-e/time-to-play.md`) | cycle 2, 22:57 (`cycle-e2/time-to-play.md`) |
| --- | ---: | ---: | ---: |
| interface to a game's first frame | 0.603 s | 0.69 s | 0.76 s |
| the exit sync's stamp (budget 3 s, D-CLOUD-119) | 1.33 s | 1.33 s | 1.32 s |
| game to game, the next game's first frame | 1.017 s | 1.01 s | 1.01 s |

No stream changed what is timed or how. The launch path is unchanged: every change in the slice runs on the host or over the serial and ssh channels.

**What changed is the judgement** (S6: `7c5d15b2d8`, `a09bfc5718`; the cycle-found `327e743189`):
- A cell that produced no number fails.
- A sync is timed only on a completed stamp.
- The game-to-game row needs its exit-sync stamp.

The before and after:
- **Before:** on 2026-10-06 the row had "no new stamp for rapidrelaunch", and the run still passed.
- **After:** on cycle 2 the same shape reads `Not a pass: a game-to-game row has no exit sync stamp`. The cause is in the product, not the harness: the exit sync stopped by the relaunch writes no stamp. That is **product #1012**, the cloud lane's.

Cycle 1's other two lines were defects in this slice's own S6 fix, not the product's, and both are fixed (`327e743189`):
- `killall` exits 1 after a clean kill, and S6 read that as a failure;
- the repeat did not wait for its stamp.

## What each stream did to a refusal

| Stream | Commits | The refusal it added or made true |
| --- | --- | --- |
| S1 | `0ecbbb9339`, `3c0b9d53c6`, `fc8754b29b` | `vm-qa`: a SKIP exits 3; an unknown or empty selection exits 2; `--help` is whole; the report directory is claimed with an O_EXCL file, because this host's `mkdir` is not exclusive under a race |
| S2 | `9df1c65c68`, `813e4dd270` | `vm-qa` refuses to judge a pair it did not bring up cleanly, and refuses a guest whose BUILD_ID is not the image's; the pair is taken down at the end; `fresh` reads the selected guest's port |
| S3 | `5edb265e59`, `a68bfadcd5`, `ca0bf841d2` | no destructive walk without the QA endpoint; seeding is checked; a reboot wait needs a new boot id and an answering interface; the ES suites SKIP when `ES_SRC` is not the image's pin |
| S4 | `33b1bb8845`, `eddd21d7a2` | `vm-pair` will not remove a disk a process holds, and rolls back a partial up; `vm-stop` reads a missing pidfile as nothing to stop (exit 3) and uses one descriptor from read to unlink |
| S5, S5b | `3f5998bbaf`, `373a366e40`, `f1331aba83`, `3eba8ce4b0` | the host state belongs to the checkout (D-INFRA-031); a held port is refused; the run's scratch is short, in the runtime directory, and removed at exit, so a socket fits 107 bytes |
| S6 | `7c5d15b2d8`, `a09bfc5718`, `327e743189` | `time-to-play` refuses `--repeat` below 1 and an empty `--only`; every cell that ran is judged; a kill is judged by its effect |
| S7 | `00b8760457`, `c1569b7bc6` | `emulator-exit-test --only` needs a known part; `device-act` will not act without its BEGIN line; a failed END fails the run |
| S8 | `ff10d77c28`, `2e790e7e52`, `05117efe58`, `1d5dc8a698` | a missing frame fails; a partial framebuffer fails; `vm-serial` returns the command's status, has deadlines on its channels, and reads until the status has arrived |
| S9 | `9a1300f141`, `33efb4d801`, `15b8f11334` | `qa-accounts` reads back equality; in `ra-offline-test`, a negative check needs a read and cleanup is counted; `vm-qa`'s exit trap speaks on the run's own stderr |
| S10 | `82b5edf1ee` | `vm-upgrade-rehearsal` needs a positive archive count, checks sizes and hashes against the seed, and fails when a stop fails |
| S11 | `36138c8da5`, `476ab6e69b` | `frame-diff` refuses an empty baseline and a zero-size PNG; a proposal claim is inert |
| S12 | `6ca9da4831` to `930ea05d70` | seven Python tools' refusals survive `python3 -O`; the consent test records an event before it judges it |
| S13 | `3edb5f2b89` to `95241c0158` | seven small tools (nine cases) refuse the empty or unreadable input that each used to pass over |

Every stream's case fails on the unfixed export (`facb2ae523`) and passes on the fix. `streams/<sN>-unfixed.txt` and `<sN>-fixed.txt` hold each pair. For `vm-stop-test` no positive was found (S12), as `02` records.

## What worked well

- **One control for the whole harness.**
  - `tools/vm-harness-test` (78 cases) puts doubles for ssh, scp, `cloud-test-backend`, `vm-pair`, `mktemp` and `mkdir` around the real tools.
  - `--tools-from` runs the same case against any export.
  - So every fix had a failing-then-passing pair without a guest, and the guests were spent only on what doubles cannot show.
- **The guest found what the doubles could not, and quickly.** Two short cycles found two defects that no double modelled:
  - `vm-serial` split a reply across reads (`1d5dc8a698`);
  - `killall` returns 1 after a clean kill (`327e743189`).

  Each became a case before the fix.
- **The host file kept two lanes off each other's guests.** With START and RETURN lines, and the order rule from the coordinator (22:43), the M7 lane and this one shared the host's guest ports, and each cycle ended with a census of 0 (`cycle-e/census-after.txt`, `cycle-e2/census-after.txt`).
- **Settling a FAIL by varying one thing.** The scripts suite was run three ways that differed only in TMPDIR. That split its 326 failures into 7 that were this slice's (S5b) and 319 that are not (#1015). No argument was needed.

## What was harder than expected

- **Fixtures wrong before the code was.** Several were caught only by reading the reason a case gave:
  - a case passing for the wrong reason, until its message was read;
  - the environment dropped in the wrong order;
  - fixture guests leaking until they were stopped by PID;
  - the unfixed tools writing under `/tmp` during a run, until the `mktemp` double redirected them.
- **The guard placement under `-O`.** In S12's first cut, one guard fell after an import, so `--help` beat it. Another relied on a `sys` import that existed only in an embedded script. A stage commit also lacked its `guarded` helper and was redone. Nothing broken was committed, but each one cost a round.
- **A trap runs under the interrupted command's redirections.** `vm-qa`'s and `ra-offline-test`'s cleanup reports went to a suite's log or to `/dev/null`, until the run's fds were saved at the start (`15b8f11334`).
- **The host is not the image.** Two cases:
  - uutils `mkdir` answers 0 to both of two racing calls (friction line, `fc8754b29b`);
  - the scripts suite uses the host's busybox when a worktree has no build root. The 10-06 PASS ran on the image's v1.36.1, and the runs here on Ubuntu's 1.37.0 (#1015's comment).

## What we discovered

- **A long checkout path breaks unix sockets.** The 107-byte cap made the scratch location S5 chose fail seven scripts checks. Anything that binds a socket under TMPDIR wants a short root.
- **The g2g row could never fail.** An exit sync stopped by a relaunch writes no stamp, and that shape passed as `?`. It has done so since at least 2026-10-06 (#1012).
- **The ES pin of an image built from an unpushed commit is unreadable.** Six suites SKIP on such an image. The coordinator filed it as Backlog #1013, under #800.
- **The frame baseline is a month old,** and 64 of the 65 boxes the fixed compare leaves unclaimed are the Last Played backdrop. Cycle 1's PASS had rested on them (`cycle-e/frame-diff-fixed.md`). Deciding the baseline is the maintainer's, on #346.

## Adjustments, Instruction-Recommendations mode

These are leads for the coordinator. The lane edits no rule.

1. **`generic-x64-vm-testing.md` (and `engineering-practices.md` § Guards must fail closed):**
   - scratch that may hold a unix socket goes under the runtime directory, never under the checkout (S5b);
   - a Python tool's refusal is an explicit check, never `assert`, which `-O` removes (S12; seven tools).
2. **`engineering-practices.md` § Guards must fail closed:** an EXIT trap first restores the run's own stderr, saved at the start. Two instances so far (`vm-qa`, `ra-offline-test`), one short of the rule of three, so it stays a lead and goes in the friction log if it recurs.
3. **`upgrade-and-install.md` § Verify on a device, not on the host:** a host-side suite whose fixtures need the image's applets refuses (exit 2) without a build root, rather than running on the host's. That is #1015's second checkbox; the rule follows its fix.
4. **`time-to-play.md`:** the game-to-game number now fails on this image until #1012 lands. The rule's "a cell that produced no number is never a pass" already covers it, so no edit is needed. The run log should cite #1012 until then.

## Scoped audit (the close-out's own checks)

- `tools/lint-audit-artifacts docs/audits/2026_10_24-epic-m6-tooling-vm-harness`: `PASS`.
- `proved:` cells 35 equal `PROOF:` lines 35.
- The coverage table has 60 rows (``grep -c -E '^\| `tools/'``).
- #984: 23 of 23 at a Phase 7 outcome:
  - 19 Resolved, each with its commits;
  - 4 Deferred: PL-19 to #986, PL-20 to #987, PL-21 to #640, PL-22 to #988.

  `tools/box-check --issue 984`: 0 fail.
- #1015, filed by this lane: `tools/box-check --issue 1015`: 0 fail.
- `vm-harness-test` 78 PASS, rc 0, at `3eba8ce4b0` (`streams/vm-harness-test-3eba8ce4b0.txt`). `vm-pair-test`, `vm-stop-test` and `vm-upgrade-readiness-test` rc 0 at `930ea05d70`. No tool changed after that except S5b and the comment-only `6e2d204987`.
- `rules-check --quiet` rc 0; `work-log-index --check` rc 0.
- `register-check` rc 1. Every finding is a citation of D-INFRA-031, D-QA-061 or D-QA-062. Those are the coordinator's rows (no register copies here, the 21:15 directive), and the check is red until the coordinator's merge.
- No handheld action, no `device-act` or `qa-accounts` against anything real, no build, no guest beyond the two cycles granted on #659, no `fork-worktree sync|remove|repair`. `00` carries the host file's lines before and after each cycle.
