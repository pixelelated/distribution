# Futro: the OS scripts and launch path area epic (#695), at T1's kickoff (#648)

**Prepared:** 2026-10-23, by the coordinator lane (Fable; D-WORKFLOW-189: the
futro of an area epic is planning).
**Scope of this futro:** the area epic #695 (`os-scripts-and-launch`: T1 #648,
T22 #669, T29 #676) at its first sub-issue's dispatch, T1, run from
`docs/reviews/briefs/os-launch-control-state.md`. It does not cover T22 or
T29 beyond what T1 learns for them; each gets its own kickoff note on this
epic when it is dispatched, and the rest of the order (T2 onward) gets its
own area epics and futros.

**Upstream retro consulted:** P1's, `docs/retros/2026-10-23-m6-p1-survey.md`
(#641 comment 6358092855), its § Discoveries that affect future slices and
§ Scoped audit findings included; no retro addendum exists (the hand-back
was accepted 06:05 UTC the same day).
**Inputs considered:** #695's and #648's bodies; the brief, version 1
(`f7fcafcddb`); `docs/reviews/order.md` § T1, § T22, § T29 and § The
security, state-preservation and launch-path files; `slices.json`'s T1
record; the inventory rows of the package (84, less `backuptool`);
`docs/reviews/plan-for-the-plan.md` § 3, § 4, § 6b, § 6c, § 7, § 8; the
nine prior punch lists that name these scripts; the 2026-09-10
graceful-degradation audit's README; blindspots 7, 13, 30, 32, 33, 34, 43,
51, 57, 64, 73; D-WORKFLOW-056 (the fix-round brief shape); #336, #644,
#645; the host's artifacts named below, each inspected.

## 1. What do we know and what are we assuming?

**The plan.** One Opus 5.5 session, in its own worktree stacked on the P1
tip, reads the 83 paths of `projects/ROCKNIX/packages/rocknix/` (less
`backuptool`) at `next`'s hash `8ebaf8daad` under the code-auditor
lifecycle with the renovation face (Q1 to Q7), proves every behaviour
claim on a GENERIC_X64 guest, takes two cross-lab second opinions through
the Facilitator, writes a punch list with a `question:` per item, files a
`bug` issue per defect, and pauses; the coordinator then writes the stream
briefs, the lane remediates and verifies, retro, close with
`reviewed-at` and `fixed-at`. The brief is the unit of handoff (plan § 3).

**Explicit assumptions, each with what was checked:**

- The slice's bytes on the lane's branch are `next`'s: `git -C <T1
  worktree> diff --quiet next HEAD -- projects/ROCKNIX/packages/rocknix/`
  exits 0 at `86d3a49f6c`; `next` and `origin/next` are both `8ebaf8daad`.
- The branch's base: the T1 branch is P0 and P1 ahead of `next` in docs and
  tools only (`git diff --stat next -- .claude CLAUDE.md AGENTS.md` lists
  exactly `fork-workflow.md` and `instruction-files.md`, 5 insertions and
  2 deletions: P1's three tools added to the fork-tool lists). The brief's
  version 1 said the rules diff must print nothing; that is false by those
  two files and is corrected in version 2.
- `upstream/next` is 43 commits past the merge base `c445081a59` on this
  package (`git log --oneline c445081a59..upstream/next --
  projects/ROCKNIX/packages/rocknix/ | wc -l` = 43), among them
  `installtointernal: allow RG55G1 in SM4450`, `rocknix: set default wifi
  country`, `rk3566: port to inputplumber`; Q4 has real work.
- Fork churn since June on the hot files (`git log --since=2026-06-01
  --oneline -- <path> | wc -l`): `001-functions` 26, `wifictl` 19,
  `post-update` 18, `chksysconfig` 13, `runemu.sh` 11, `setsettings.sh` 11,
  `rocknix-evidence` 6; last touched between 2026-09-23 and 2026-10-14.
  These are the brittleness lens's files and the ones the prior punch lists
  name most (28 mentions in `2026_09_25-milestone-rc-round-since-258`, 17 in
  `2026_09_24-milestone-rc-round-since-186`).
- The M7 candidate changes `runemu.sh` and `package.mk` ahead of `next`:
  `git -C /workspace/repos/rocknix log --oneline next..069fc2704421 --
  projects/ROCKNIX/packages/rocknix/` lists `d535e026b2`, `3b27b9a70d`,
  `069fc27044`; `rev-list --count` is 12 for the whole branch. The slice
  reads `next`; the drift tool re-opens it over that diff when the
  candidate lands (plan § 8).
- The image the lane uses is the M7 lane's newest GENERIC_X64 build:
  `-rw-r--r-- 2122289964 Oct 23 00:04
  .../m7-signin-build-20261022-07/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`,
  and its build root's `image/system/usr/bin/busybox` exists (182
  applets; `grep` is not one of them). The older
  `rc-device-fixes/build.ROCKNIX-GENERIC_X64.x86_64` has no
  `image/system/usr/bin/busybox` (`ls` fails): version 1 of the brief named
  it as an alternative and version 2 drops it.
- The image's shells and interpreters, read from that `image/system`:
  `/bin/sh -> dash` (not busybox `ash`, not bash), `/bin/bash` present,
  `/usr/bin/python` and `python3` both symlinks to `python3.14`. So
  `usbgadget`'s `#!/bin/sh` runs under dash and `rocknix-systems`'s
  `#!/usr/bin/env python` resolves; version 1 of the brief said the image's
  `sh` is busybox, which is wrong and is corrected.
- The host can run guests: `/dev/kvm` exists, the user is in the `kvm`
  group (`id -nG | grep -c '^kvm$'` = 1), no QEMU guest is running now
  (`pgrep -f qemu-system-x86_64 | wc -l` = 0) and the default instance
  files `/tmp/rocknix-qemu.pid` and `/tmp/rocknix-qemu-serial.sock` are
  absent. The VM tool takes `--pidfile` and `--serial` (lines 694 and 705
  of `generic-x64-vm`), so a lane can own its instance paths.
- The reviewer substrate: `~/.config/council/env` is present (not read);
  `node` v24.21.0 and `npm` 11.19.0 are on the host; `tools/council/node_modules`
  is absent in the T1 worktree (gitignored; P1 installed its own copy and
  ran the preliminary review on 2026-10-22, which is the only evidence
  the OpenRouter route works from the fresh clone). The Gemini 4 Argon
  route is absent from the tree (`grep -rli argon scripts tools/council`
  empty; present at `1c7d283ad5` on the legacy checkout's
  `feature/m7-audit-integration-603`).
- `shellcheck` is not on the host (`command -v shellcheck` empty).
- The lint and the renderer exist on the lane's branch
  (`tools/lint-audit-artifacts` lines 367 to 392 carry the renovation
  face; `tools/renovation-status`, `tools/renovation-drift` present).
- Substrate preconditions, enumerated: the guest (above); SSH into it (the
  profile's forward on 10022, a key provisioned over serial, § Headless);
  `tools/vm-serial`; the Facilitator and its key (above); `gh` with
  `--repo` on every call (the fresh clone has no default repo); `git` access
  to the legacy checkout for reads; Herdr for the lane's pane (this
  coordinator runs in `wN:p2`; `herdr agent start` and `herdr tab create`
  exist). No platform API beyond OpenRouter is involved, so the
  platform-probe mandate reduces to the seat probes the brief already
  requires at Phase 4.6.
- Build-vs-adopt: not applicable; this is a review and remediation of
  existing code, not a component choice.

**Confidence:** mixed. High on scope, hashes and the guest; lower on the
second-opinion substrate (one seat's route not in the tree, the other
proven once from this clone) and on the lane's discipline at the stage-D
pause, which no tool enforces.

## 2. What known unknowns need investigation?

| Unknown | Treatment | Owner |
| --- | --- | --- |
| Does the Argon route reach `next` before the lane's Phase 4.6? | Proceed without; the brief names the check (`grep -il argon scripts/council-invoke.ts`), the pending line and the coordinator's decision on #648 | the coordinator, when asked |
| Does `tools/time-to-play --vm` and `tools/emulator-exit-test --vm` work against a single `generic-x64-vm run --headless` guest with the profile's 10022 forward, rather than `tools/vm-pair`'s guests on 10025? | Investigate at stage A: both tools default to port 10022 (`time-to-play` line 989) and take `--port`; run each once against the lane's guest and record the outcome before the Q5 measurements | the executor |
| Does `tools/vm-qa --only scripts,lifetime,quoting,exit` run without bringing up the pair (`--skip-up` needs "the pair already up")? | Investigate at stage B: read `tools/vm-qa --list` and the `scripts` suite's line (`last-good-scripts-test` on the host); run the host suites directly where the runner wants the pair | the executor |
| Is the M7 image's busybox the same build as `next`'s? (`QA_SYSTEM_ROOT` points at a root built from `069fc2704421`) | Proceed without: busybox's recipe is not among the 12 commits (`git -C /workspace/repos/rocknix diff --stat next 069fc2704421 -- packages/sysutils/busybox projects/ROCKNIX/packages/sysutils/busybox` is empty, checked 2026-10-23); record the root's commit in `00-running-log.md` | the executor records |
| How much of `runemu.sh` is RetroArch-specific, and what #336 Step 1 actually replaces? | Investigate in Phase 1 from #336's body and the script; the brief's rule for it is below (§ 5) | the executor |
| Whether `shellcheck` can be had as a static binary under the lane's scratch without a system install | Proceed without; the brief allows it and accepts `shellcheck: not run` | the executor |
| Whether the lane's session keeps to the stage-D pause (the code-auditor lifecycle has no pause there) | Proceed with the brief's stop condition, #648's note and the coordinator's read of the audit issue before any stream brief exists; no tool enforces it | the coordinator |

## 3. What patterns from prior work apply that we haven't named?

- **The fix-round brief shape (D-WORKFLOW-056,
  `docs/audits/2026_09_25-milestone-rc-round-since-258/streams/briefs/`)**:
  the verdict's lines, the fix as a specification, the test first, the
  `Already written:` line, the files owned, the commit shape. The stream
  briefs the coordinator writes at the stage-D pause use it; the brief
  already says so. What that round taught, from its own audit (#258 P-01,
  P-02, P-04): a reversal sweeps its old words; a guard's positive is
  recorded where the guard is wired; success over a no-op is a defect.
  T1's remediation will trip all three unless each stream brief carries
  them as acceptance lines.
- **The 2026-09-10 graceful-degradation audit** read every writer of these
  scripts for D-CLOUD-077/078 (`scripts-and-writers.md`,
  `kill-fixtures-design.md`) and produced #105's fix list and
  `tools/last-good-scripts-test`. It is the closest prior read of the
  state group and the model for Q3 on `chksysconfig`, `set_setting` and
  the stamps: kill at every step, assert one record. Its verdicts are
  sequestered until Phase 2.5, but its *method* is the pattern.
- **Blindspot 34's lesson generalises past `tr`**: `last-good-scripts-test`
  now runs the applets through the image's busybox for exactly this
  package; but the image's `/bin/sh` is dash, and nothing runs a `#!/bin/sh`
  script under dash on the host. For `usbgadget` (and any fragment the
  autostart runner executes with `sh`), the proof is on the guest or under
  the image's dash, never under the host's bash.
- **P1's retro**: every count beside its command (a compaction mid-slice is
  the normal case: the running log is the resume point); rendering kept
  apart from filing; a guard proven by a constructed failure before it is
  trusted. T1's `02-forward-audit.md` coverage table and its mechanical
  checks follow the first; the brief's § 5 the third.
- **The #186 and #258 audits read these scripts at milestone tier** and put
  45 items on them between them; the one-call second opinion added a third
  of #186's list. The shape held and is kept; the difference now is the
  renovation face, which asks seven questions of a file that then had one.

## 4. What could we be missing?

**Agent-execution simulation.**

> Archetype 1: a fresh Opus 5.5 session in the T1 worktree, holding the
> pointer and the brief, at the first commands.

- **First commands (the rules diff):** version 1 says `git diff --quiet
  next -- .claude CLAUDE.md AGENTS.md || echo STALE` must print nothing;
  it prints STALE on this branch (P1's two edited rule files). A careful
  executor stops at a false stop.
  **Plan change:** version 2 names the two files as the expected
  difference and anything else as STALE.
- **The image copy and the guest:** 2.1 GB gunzipped to a raw image, then
  qcow2 at 16 GiB, in the lane's own artifacts directory; a lane that
  takes the default `--pidfile` and `--serial` collides with any M7 guest
  started later on the same defaults, and `vm-serial` then talks to the
  wrong guest.
  **Plan change:** version 2 gives the lane its own instance paths under
  its artifacts directory and says `vm-serial` is pointed at them.
- **`tools/last-good-scripts-test`:** version 1 says "runs the image's
  busybox from a build root" without the variable; the tool reads
  `QA_SYSTEM_ROOT` and refuses an unusable explicit root. An executor
  without the variable runs the host's tools and gets blindspot 34's
  false pass.
  **Plan change:** version 2 names `QA_SYSTEM_ROOT=<the M7 root>/image/system`
  and `tools/settings-modes-test`'s three required arguments
  (`--profile`, `--chksysconfig`, `--busybox`).
- **Q2 on `#!/bin/sh` scripts:** version 1 says the image's `sh` is busybox;
  the executor would review `usbgadget` against `ash`'s rules and miss
  dash's.
  **Plan change:** corrected in version 2 (dash; bash present; python is
  3.14).
- **The coverage table at 83 rows:** an executor under time pressure
  groups rows ("the autostart fragments") and the criterion
  (`grep -c` of rows equals the path count) fails at hand-back after the
  work is done.
  **Plan change:** none beyond the criterion as written; it is mechanical
  and the brief's § 6 says one row per unit of the 83 paths. The
  coordinator reads the count first at hand-back.
- **Phase 4.6 without Argon:** the executor, finding no route, might call
  the roster's `gemini` seat (`google/gemini-3.8-flash`) because the skill's
  table says "a third lab".
  **Plan change:** the brief forbids the substitution in so many words and
  names the pending line; kept.
- **The stage-D pause:** the code-auditor skill runs Phase 5, 6 and then
  the work; an executor following the skill rather than the brief starts
  fixing. The brief's § 8 names the pause; #648's body did not.
  **Plan change:** #648's body gains a line under its acceptance list:
  *the lane pauses after the punch list and the audit issue; the
  coordinator's stream briefs authorize remediation.*
- **`bug` issues with device checkboxes:** an executor who finds a device
  quirk writes "on the H700" as a criterion; `tools/box-check` fails it
  and the fork CI goes red.
  **Plan change:** none; the brief cites D-QA-044 and the checker; the
  coordinator runs `tools/box-check` on each new issue at the pause.

> Archetype 2: the coordinator, three weeks on, at the hand-back, after the
> M7 candidate merged mid-slice.

- **The hash moved under the slice:** the coordinator merged `next` into
  the T1 branch to refresh rules while the lane was between stages A and
  D; the slice's `runemu.sh` changed under the read, and `reviewed-at` no
  longer names what was read.
  **Plan change:** the coordinator's own rule, in its pointer: no merge of
  `next` into a slice branch between stage A and stage D; after D, a
  merge re-baselines the slice over the diff (plan § 8), recorded on the
  slice issue.
- **A proof of the image's `runemu.sh` taken as a proof of the tree's:**
  the hand-back cannot tell which copy a guest proof exercised.
  **Plan change:** already a criterion in version 1 (each proof says which,
  after a recorded diff); kept.

> Archetype 3: the lane that runs #336 Step 1, two months on.

- **T1's punch list is half about the RetroArch half of `runemu.sh`**
  (modernize its argument handling, its per-core settings, its logs),
  remediated in October and replaced in December.
  **Plan change:** a rule in the brief: Q1, Q5 and Q7 findings confined to
  the RetroArch-specific lines of `runemu.sh` and to `setsettings.sh`'s
  RetroArch settings are recorded on the punch list and carried as
  `deferred:#336` at Phase 7 unless the coordinator's stream brief says
  otherwise; Q3 defects and Q2 violations are fixed regardless (a player
  has them today; D-WORKFLOW-187). The order's lens already weighs the
  nearest planned change (plan § 6a); this makes it operative in the
  slice.

**Pre-mortem (30 days out).** *On 2026-11-22 the T1 audit folder passes the
lint and #648 is closed; the M7 candidate merges the next day with its 63
lines of `runemu.sh`; `tools/renovation-drift` re-opens T1 at Extended
depth over the diff; nobody reads it because the drift report is written
only on the slice issue and the M6 body says T1 is closed.* Root cause: the
drift re-open had no owner. **Plan change:** the M6 body's standing item 5
names the coordinator as the reader of every drift report at every slice
close, and the lane pointer's merge notes say the T1 drift from the M7
candidate is expected and who re-opens it. (Second story: *the second
opinion never ran because the npm install needed the registry and the
host was offline that hour*; the brief already makes that a recorded
blocker, not a skipped phase.)

**Blindspot check** (`docs/blindspot-register.md`, 73 entries): 7 and 34
(host tools versus the device's: addressed by `QA_SYSTEM_ROOT`, the dash
correction and the guest); 13 (assumed done: the nine prior punch lists are
provenance only, re-derived in Phase 2); 30 (a resumed session built on its
own summary: the running log carries commands, and the brief says a
compaction re-runs them); 32 and 33 (`automount`'s wall-clock ordering and
the autostart fragments' borrowed exit codes: both named in the brief's
read-first list for Phase 1); 43 (a header's safety claim untested:
`rocknix-evidence` and `setsettings.sh` headers are to be tested, not
quoted); 51 (an open checkbox is a claim: #648's criteria were written
today, the audit issue's will be read at the pause); 57 (a fix covering
fewer sites than named: every stream brief lists the sites, the
`grep -rlF` count beside it); 64 (a wait lengthened: a guest that will not
boot is read through § Debug order before any timeout moves); 73 (a monitor
of completion, not activity: a long guest run under `tools/watch-job` with
`--activity-dir`). **New blindspot:** none surfaces here. The merge commit
with conflict markers that the coordinator made today while cutting the
lane's branch (#696) is one instance, a friction line and an issue, not a
register entry.

**Replaced-mechanism archetype:** T1's reading replaces nothing. Its
remediation may remove a unit under Q6 (`rocknix-update`, `updateabl`,
`migrate_roms`, `show_changelog`, the `report-stats` pair are the
candidates); for each the brief already demands the survivor's list
(`engineering-practices.md` § Before deleting a duplicate) and the
`Already written:` line (what the unit left on devices: a stamp, a
`/storage` file, a timer's state). The archetype adds one question the
brief now carries: what the unit *exposed* (a `motd` line, an ES row
through `ApiSystem`, a systemd unit name another unit `After=`s) and where
that goes.

## 5. What adjustments or investigations must happen BEFORE execution?

**Plan edits applied** (the brief's version 2, `docs/reviews/briefs/os-launch-control-state.md`,
in the same commit as this futro; #648's body edited in the same session):

1. First commands: the rules diff is expected to list exactly
   `fork-workflow.md` and `instruction-files.md`; anything else is STALE.
2. The guest's instance paths are the lane's own (`--pidfile`, `--serial`
   under its artifacts directory), and `tools/vm-serial` is pointed at
   them; the default paths are never used by a lane.
3. `tools/last-good-scripts-test` is run with
   `QA_SYSTEM_ROOT=/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system`;
   the `rc-device-fixes` root is dropped (no busybox there);
   `tools/settings-modes-test` is named with its three arguments.
4. The image's `/bin/sh` is dash, bash is present, `python` is 3.14; Q2
   reads `#!/bin/sh` scripts against POSIX sh and proves them under dash.
5. The RetroArch-half rule for `runemu.sh` and `setsettings.sh` (archetype
   3): Q1/Q5/Q7 items there are `deferred:#336` at Phase 7 unless a stream
   brief says otherwise; Q2 and Q3 are fixed.
6. The stage-D pause stated in #648's body, not only in the brief.
7. The Q6 removal question gains "what the unit exposed" beside guarded
   and stamped.
8. The stranger's proof of the brief (plan § 3, principle 3), run on
   `86d3a49f6c` by a reader with no context, feeds the same version 2; its
   findings are recorded in the brief's § 10.

**Investigation tasks opened:** none as issues. The two executor-side
investigations of § 2 (the single-guest tools; `vm-qa` without the pair)
are lines in the brief's § 5 for stage A and B, with their outcome recorded
in `00-running-log.md`.

**Documented unresolved assumptions:**

- The Argon route reaches `next` with the M7 candidate before the lane's
  Phase 4.6; if not, the seat is pending and the coordinator decides on
  #648. Rationale: the lane's Phases 1 to 4 are days of work and the
  candidate's merge is the next M7 event.
- The OpenRouter route works from the fresh clone after `npm install
  --prefix tools/council`: proven once by P1 on 2026-10-22; a failure is
  a recorded blocker.
- The M7 image stands in for `next` for every file but `runemu.sh` and
  `package.mk`, which the brief's diff rule handles.

**Blindspot register updates:** none.

**The coordinator's own rules from this futro**, written into its lane
pointer: no merge of `next` into a slice branch between stage A and stage
D; the coordinator reads every drift report at every slice close and names
who re-opens a slice; `tools/box-check` on every issue a lane files, at the
pause.

**Futro complete. Ready to proceed to T1's dispatch once the brief's
version 2 is committed with these edits and the stranger's findings.**

## T22's kickoff (2026-10-25), and the errata from its brief's stranger's proof

T22 (#669, the OS's system services and platform quirks; Extended, two
seats as T1's) is briefed in `docs/reviews/briefs/os-system-services.md`
from a read-only research pass (`$S/t22-research.md`, 422 rows). What the
pass tested of the order's `why`: half right -- `system-utils` selects at
install time (`package.mk:27-34`; 8 rows / 317 lines shipped by no shipped
image), while the quirks' platforms are all installed into every image
with a platform directory of its own (`quirks/package.mk:15-18`) and
selected at run time by `HW_DEVICE` and `QUIRK_DEVICE` (`/usr/bin/autostart:16-28,
31-43`; `002-autostart:6-12`), so 213 of 264 platform files are shipped
bytes that never run on H700, SM8550 or the VM; the brief's reachability
table carries a *runs on* column. The 29 units all run as root; the read
tree is three and a half weeks behind upstream in exactly this area (44 M,
20 D, 42 A and 2 R at `651150fc88`); the inventory's `last_upstream_commit`
is upstream's tip, not the read tree's.

The stranger's proof (`$S/t22-proof.md`: 70 checks, 26 differed, 41
reproduced; 21 distinct findings) corrected version 1: the block never
wrote `paths.txt`; the read set is shell, recipe, systemd, udev and one C
file (10,898), not python; 23 other sysutils packages; the platforms copy
is under `:16`'s test; `/usr/bin/autostart` lives in `sysutils/autostart/sources/`
and both its loops lack `-f`; `:31-43` is the autostart's, not
`002-autostart`'s; the per-platform count needs `cut -f7`; the units count
needs the quirks' `system.d/`; `video_sense` is proved by `ls-tree`;
upstream's busybox carries seven patches that are renames of the
override's own; `system-utils` installs `autostart/common/*` on every build
and has no `post_install` -- enablement is a preset's or another
package's; the 20 D are 9 never upstream's, 2 upstream removed, 9 deleted;
the A list is 42 plus 2 renames, not 20; `54acd9556f` deletes
`sysctl.d/rocknix.conf` and does not touch `hang-policy.conf`; util-linux
is 2.42.4 upstream; `slice_of` is `:1237-1248`; T1's folder has no
`.run.log` for the GPT seat and no packet manifest (T13's is the model);
`input_sense` was rewritten in four commits; the GENERIC_X64 quirks in
eight on 2026-09-28; #797 is not the autostart hook-shape issue.
