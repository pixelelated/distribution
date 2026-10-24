# Session pointer: the renovation lane (M6)

> **Saved:** 2026-10-22 (see the commit)
> **Branch:** `feature/m6-renovation-plan-346` (a pointer; D-WORKFLOW-133)
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346`
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (the fresh clone of 2026-10-22, D-INFRA-025; the legacy `/workspace/repos/rocknix` serves M7 until #640)
> **Repository:** `pixelelated/distribution`; integration branch `next`

## Start here

1. Read `next:AGENTS.md`, the every-session rules under `.claude/rules/`, and
   check this worktree's rules are `next`'s:
   `git diff --quiet next -- .claude CLAUDE.md AGENTS.md || echo STALE`.
2. Read [the canonical next checkpoint](saved-session-state-next.md) for the
   M7 lane's state. **This lane does not edit it** while M7 owns it (the open
   question on #346); this pointer is the lane's state.
3. Read `docs/reviews/plan-for-the-plan.md` (the plan for the plan, #346), the
   live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #339 (the epic) and #640 (the checkout move).
4. Register rows this lane wrote: D-WORKFLOW-181, D-INFRA-025. The M7 lane
   holds D-WORKFLOW-171 to 180 and D-INFRA-024 unmerged on
   `feature/m7-audit-integration-603`; do not cite them on this branch until
   they reach `next` (`tools/register-check` refuses a citation of an absent
   row).

## Current focus

**2026-10-24, late morning.** P0 and every accepted slice branch wait for
the M7 lane's post-candidate merge to clear the push guard's W42 gate before
anything merges to `next` (never `--no-verify`); the order is in § Merge
notes. **Accepted:** P1 (#641), T1 (#648), T2 (#649), T3 (#650), T5 (#652),
T6 (#653). **Running:** T30 (#677, Extended) in the T3 session
(`m6-t3-emulators`), stage C: the GPT seat returned; the Gemini Argon seat
hit its output ceiling on the full packet and runs again on a trimmed one
(D-WORKFLOW-195, 10:10:57); a second guest cycle was named. **T7 (#654,
Local) dispatched 10:11 UTC** to the T5 session (`m6-t5-build-engine`) from
`docs/reviews/briefs/generic-packages-reached.md` version 2 (`e7978a1ca5`),
lane `feature/m6-generic-packages-reached-654` at `4ea87f17dd`, worktree
`distribution.worktrees/m6-generic-packages-reached-654`; its stage-D pause
is the coordinator's next act there (stream briefs, plan § 6b E). **Waiting
on the maintainer (#346):** T4's dispatch (#651, brief v2 `0921782112`; a
third lane); the `portaudio` re-hosting (#849). **Fix packets for M7**
(#802, #806, #825) are reviewed and named on the host file. **Filed today
by this lane:** #807 to #811, #838, #839, #842 to #844, #847 to #852. See
§ State at 2026-10-24.

## Next commands

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346
git fetch origin && git merge --no-edit next          # only when next moved; never another lane's feature branch
tools/register-check && tools/work-log-index --check && tools/ceremony-check
```

Then: **at every gate, re-read § The seed brief below and D-WORKFLOW-181 against
what is about to be accepted, and say on #641 what was checked** (maintainer,
2026-10-23, giving the yes on the order: *"It's incredibly important that we
remain aligned."*). Read #641's latest comments for P1's state. At its pass-7 gate, read
the proposed order against plan § 5 and § 6a and record the yes or the
changes on #641. After the M7 candidate's merge lands on `next`, merge this
branch to `next` first (`git switch next && git merge --no-ff
feature/m6-renovation-plan-346` in the primary checkout, the push guard's
checks green), then P1's branch when it hands back. Address every git
command to a worktree with `git -C <absolute path>` and every file by its
absolute path: a `cd` at the head of a call did not hold on 2026-10-22 and a
commit meant for this branch landed on P1's.

## Herdr lane map (2026-10-22, the planning session's record)

Workspace `wN` "pixelelated · Codebase renovation" (session `default`),
after the maintainer's Herdr layout: first tabs coordinate, each later tab is
one lane, one session per worktree (D-WORKFLOW-183).

| Tab | Label | Pane | Worktree | Agent name | Model | Role |
| --- | --- | --- | --- | --- | --- | --- |
| `wN:t1` | P0 planning (#346) | `wN:p1` | none (`/workspace/repos/pixelelated`) | (unnamed, Claude Fable 5.1) | Fable 5.1 | the session that planned P0 and started the lanes; closes once the coordinator has resumed |
| `wN:t2` | Coordinator (M6, #346) | `wN:p2` | this worktree | `m6-coordinator` | Fable 5.1 | plans, writes briefs, accepts at gates, integrates; keeper of the primary checkout |
| `wN:t3` | P1 Survey (#641) | `wN:p3` | `distribution.worktrees/m6-p1-survey-641` | `m6-p1-survey` | Opus 5.5 | executes `docs/reviews/briefs/p1-survey.md` |

Session ids are read fresh from `herdr agent list` (`agent_session.value`)
and recorded on #346 and #641 at each start; never from this table. Other
workspaces on this host (`w4` the M7 lane, `wG` the website, `w7` another
project) are never read, prompted, moved or closed from here. Questions only
the maintainer can answer go up through the coordinator, one at a time, and
the answer is recorded verbatim, marked RELAYED, where the question lives.

## Merge notes

This branch and the M7 lane both append to `docs/decision-register.md`, both
create `docs/work-logs/2026_10-work_logs/2026_10_22-work_log.md`, and both
regenerate `docs/work-logs/INDEX.md`. At merge: keep both appends in order,
keep both day-file entries, regenerate the index with
`tools/work-log-index --write`. Nothing here builds, touches a device, a
cloud or the M7 build worktrees.

- **This branch carries three of M7's commits as cherry-picks** (`-x`, 2026-10-23
  16:30 UTC): `033eb7ed23`, `0ceb2994c5`, `6874394d49` from `fac2129787`,
  `1c7d283ad5`, `a7a3bdda4e` on `feature/m7-audit-integration-603` (the
  Argon reviewer route and its pins, #636/#638). When the M7 candidate merges
  to `next` first, the merge of this branch sees them as duplicate patches;
  expect a clean or trivially identical resolution in `scripts/council-invoke.ts`,
  `tools/lint-audit-artifacts`, `verifier-pins.json`, `council-seat-efforts.json`
  and the two `docs/qa-logs/2026-10-22-*-638/` folders, and check for markers.
- **T2 accepted 2026-10-24 00:3x UTC** (#649: distribution `f16cf7fc28`, ES
  `55158d2a64`, 35 commits on the pin `16dbac5211`; `reviewed-at: f4e0f0a196`).
  Its `slices.json` row (`reviewed_at`, `fixed_at`, `es`) is written when this
  branch takes the P1 branch at integration. **The ES integration order:** the
  M7 lane's EmulationStation fixes of 2026-10-23 (#697/#698) reach
  `test/qa-integration` first, then T2's branch is merged there and the pin
  bumped in `package.mk` on this branch; both wait for D-WORKFLOW-191 (which
  build carries the renovation's pin bump). #649 stays open as `remediating`
  until that image proves the 21 walks; then it and the 24 `bug` issues close.
## State at 2026-10-23 (the coordinator's own update)

P0 is done on this branch; its merge waits on the M7 lane's post-candidate
merge (never `--no-verify`). P1's pass-7 gate: question 1 settled
(D-WORKFLOW-185/186), question 2 withdrawn (D-WORKFLOW-187: the renovation
gates no release), question 3 settled by D-WORKFLOW-184; the maintainer's yes
on the order's fourth version (`eb4763e3cc`, ledgers `00ca350666`) was given
on 2026-10-23 and relayed; P1 wrote the order's register row on its branch
(the next ID above 187). The question who authors the slice issues was
answered 2026-10-23 with a general rule, D-WORKFLOW-189: planning, the
division of work, the definition of work items and roadmap changes are this
lane's; a work lane executes. So the 46 slice issues are this lane's to file,
from P1's renderer (`tools/renovation-inventory --slice-issues DIR`, run
read-only against P1's tree into this lane's scratchpad). #644 and #645 are
the build-path read and its PR-process findings. The 46 are filed: #648 (T1) to #693
(T46), sub-issues of #339 on milestone M6, `tools/box-check` 0 fail over all
open issues (work log 05:40 UTC). P1 was accepted at hand-back and #641
closed completed on 2026-10-23 (P1's branch at `2174265e9c`; it merges to
`next` after this branch, after the M7 candidate). T1 is dispatched (2026-10-23): the area
epic #695 with its futro; the brief `docs/reviews/briefs/os-launch-control-state.md`
at version 2 (`968ba95993`); the lane `feature/m6-os-launch-control-state-648`
at `4228561fd2`, worktree `distribution.worktrees/m6-os-launch-control-state-648`,
an Opus 5.5 session at high effort in Herdr pane `wN:p4`, agent
`m6-t1-os-launch` (started from this pane: `herdr tab create --workspace wN
--cwd <worktree> --label ... --no-focus`, then `herdr agent start <name>
--kind claude --pane <id> -- --model claude-opus-5-5 --effort high`, then
`herdr agent prompt <name> "<seed>"`; the seed is kept in this session's
scratchpad and quoted in the 07:50 work-log entry). This lane's rules from
the futro: no merge of `next` into a slice branch between stage A and stage
D; every drift report read at every slice close and the re-open named;
`tools/box-check` on every issue a lane files, at the pause. Next: **T1 accepted at hand-back 2026-10-24 01:24** (`ba22eea867`; `reviewed-at efadfea08a`, `fixed-at 0f7558cff7`; 13 of 15 criteria ticked; one `Already written:` line owed on Q6's `installtointernal` row, asked of the lane; the simulated merge of this tip into the lane's conflicts only in the four ledgers; #796 and #797 filed from its stage F and retro). Both lanes are idle; the host is M7's from 2026-10-24 01:33 (H700 then SM8550 builds) until its return line, acknowledged with a census at 01:27, both lanes holding. **T3 is dispatched (2026-10-24 02:37):** the brief at version 2 (`f650d65522`, after the epic #798's futro `179093ffd6` and a stranger's proof), the lane `feature/m6-emulators-libretro-650` at `af35d54f87` in `distribution.worktrees/m6-emulators-libretro-650` (P1 `2174265e9c` + this tip merged at `16778b5f61`), Opus 5.5 at high effort in pane `wN:p6`, agent `m6-t3-emulators`; the dispatch comment is #650 issuecomment-6378830351. The host returned to M6 at 02:22 (acknowledged in the file at 02:23). **T5 is dispatched (2026-10-24 03:51) beside T3:** the brief at version 2 (`01ff4c0bcd`, after the epic #800's futro `fd46029257` with errata and a stranger's proof), the lane `feature/m6-build-engine-652` at `30b1bb38c0` in `distribution.worktrees/m6-build-engine-652` (P1 `2174265e9c` + this tip merged at `dcd70698f1`), Opus 5.5 at high effort in pane `wN:p7`, agent `m6-t5-build-engine`; the dispatch comment is #652 issuecomment-6379501933. **The host is M7's from 03:47** (handoff confirmed in the file; both lanes hold runtime until the return is relayed on #650 and #652). Read #650 and #652 at every turn; each lane's stage-D pause comes with its punch list, then its stream briefs are this lane's to write. Bugs filed today by this lane: #801 (the identity test's release-plan half, T14's), #802 (the default PlayStation core not where the launcher loads it: the base merge takes `c9820d0e89` adapted to `${DISTRONAME}`). **The research behind the brief (#650, `emulators-libretro`, Extended, currency; the 01:00 to 01:45 reads of this session: 344 paths, 31,961 lines, 10,185 read, RetroArch at `bdba046fa6` v1.22.2, 151 core recipes with 144 full-hash pins, one pin differing from `upstream/next`, 14 upstream commits on the paths since `c445081a59`, upstream's `retroarch-0100-ffmpeg9-lavc63.patch` absent here, `mk_es_systems` defined in T5's `distributions/ROCKNIX/config/functions:99` and called at `virtual/emulators/package.mk:1726`, `Install Steam.sh` 2,755 lines fork-own by M7's October commits).** At integration, T1's acceptance leaves (brief § 10: re-run the harness under
`QA_SYSTEM_ROOT` and `pkgcheck` once; the `fix-pending-image` rows stay open);
T2 accepted 2026-10-24 (above), its ES merge and pin bump held for the M7 ES
fixes and D-WORKFLOW-191; the merge order to `next` after
the M7 candidate (P0, P1, T1, T2, T3, T5, then T4 last so the doctrine's edits land once, each rule-file conflict resolved in this lane's favour and the slice's edit re-applied by the paragraph its stream brief names; **at the integration commit, after T3's S2 and T5's E4 are both on `next`: flip `add_es_system`'s zero-default `elif` in `distributions/ROCKNIX/config/functions` from the WARNING to `return 1` (E4 left it a warning because GENERIC_X64's `psx` default is S2's line) and regenerate the five tables once more, the diff being S2's and E4's intended lines only;** the ledgers united by whole entries; the change log for T1's player-visible lines the day it lands; `audit-completion.json` for T1 after #701 closes; the drift re-open over M7's `runemu.sh` hunks; the image proof of T1's nine fix-pending-image rows and T2's 21 walks, then #648/#649 and their bugs close, the three device-fact bugs as open items to test). **At the next base merge of `upstream/next`:** take upstream's `c9820d0e89` (the 32-bit PlayStation core installed where the launcher loads it, #802) and `yabadabadoo-lr`, and **rewrite their `build.${DISTRO}-${DEVICE}.arm` to `build.${DISTRONAME}-`** (the fork's roots since `43d0bc3bf4`; `DISTRO` is still `ROCKNIX`), with `git grep -F 'build.${DISTRO}-' -- projects packages` printing nothing on the merged tree as the check (T3's F-09); take upstream's `aethersx2-sa` deletion (`c4d353449e`, licensing; T3's F-07) rather than keep the recipe, as #644's finding 16 routes the retired overrides; the two calls open with the maintainer on
#346 (D-SYS-014, D-WORKFLOW-191); the host handoff file is read before any
runtime. **State at 2026-10-24 04:3x UTC:** T3 (#650) has stage C prepared and
waits for M7's return line for its Phase 4.6 (ten `bug` drafts at `00f535942a`;
context at 1 %, a compaction is expected); T5 (#652) is at stage B
(`da3e6559cc`, the 242-row coverage table); **T4 (#651) is briefed** at
version 1 (`docs/reviews/briefs/doctrine-rules.md`, `8a056c4a60`, Local),
the doctrine area epic **#807** filed (T4, T38 #685, T39 #686 retitled
`E807/T<k>`) with its futro (`docs/futros/2026-10-24-m6-doctrine.md`,
`12d163dd2c`, nine adjustments A1 to A9 for version 2), the stranger's proof
running, **the dispatch held for the maintainer's answer on #346 about a third
lane**; #808 (`bug`: `CLAUDE.md`'s rule table names 29 of 30) and #809
(Backlog: the inventory's three read-count renderings) filed from the
brief's re-derivation. **Two fix-packet streams for the M7 candidate**
(`docs/reviews/briefs/fix-packets-802-806.md`, `3f04de3342`, at the M7 lane's
request of about 04:30): #802 to T3 (`fix/m6-802-pcsx-rearmed32`, upstream
`c9820d0e89` with `${DISTRONAME}`), #806 to the T1 lane
(`fix/m6-806-grep-pcre2`); **both handed back and reviewed 04:3x**:
`a0defbd527` and `ea0af11d07`, one commit each on `8ebaf8daad`, told to M7
on the host file; M7 applies to its candidate tree and its images prove the
criteria; the two fix worktrees (`m6-802-pcsx-rearmed32`,
`m6-806-grep-pcre2`) are removed with `tools/fork-worktree remove` once M7
has consumed the packets. **M7 returned the host at 05:42** (relayed on #650 and #652); **both
lanes are at stage E** on their stream briefs (`docs/reviews/briefs/t3-streams.md`
S0 to S6 after audit issue #826 and bugs #813 to #825 -- #825 the security
defect in RetroArch patch 0012, the maintainer notified, M7 told, #585
given the row; `t5-streams.md` E1 to E8 after audit issue #837 and bugs
#827 to #836; D-WORKFLOW-193 written for E6). #838 and #839 filed for T3's
routed items. **S0 reviewed 06:3x**: `fix/m6-825-cheevos-hook-no-shell` at
`fac139dd43` (merged into the slice branch as `faac89ffc0`), the hook half
proven on the guest, the RetroArch half `fix-pending-image`; M7 told the
hash; the fix worktree stays until M7 consumes it. **T3 accepted at hand-back 07:1x** (`d9003d819f`; `reviewed-at d606301784`,
`fixed-at 3c47325fb2`; #826 closed completed; 14 of 15 ticked, the
`renovation-status` clause at the merge; its `slices.json` row written when
this branch takes P1's at integration; #823 and #841 close at the merge; the
eleven `fix-pending-image` items at the first image). **T5 accepted at hand-back 07:2x** (`52e6794ba7`; `reviewed-at 46f6c7d428`,
`fixed-at 877775e61e`; #837 closed completed; 15 of 16 ticked; the
coordinator's rows on #652: the container pin at the first M6 build, the three
base-merge files, the ccache measurement, `areas.json` at the P1 merge). Both
work lanes idle. **T6 accepted at hand-back 08:5x** (`ec5f7cf3fd`; `reviewed-at b96e1ca761`,
`fixed-at 820e413179`; #846 closed; 15 of 16 ticked; S1 #845's exit 2, S2 the
late-binding list widened; the sweep's leads on #654, #655, #657; the merge
after T5's, before T4's). **T6 dispatched 08:0x** (brief version 2 `3d60062ce5`; lane
`feature/m6-build-engine-upstream-tools-653` at `b96e1ca761` in
`m6-build-engine-upstream-tools-653`, the T5 session `m6-t5-build-engine`;
Local, no calls). **A merge recipe stops on the union script's failure and on a
non-empty marker grep before `git add`** (the first T6 push carried markers;
replaced within minutes; #696). **T30 dispatched 08:2x** (brief version 2 `b81fc193a1`; lane
`feature/m6-emulators-standalone-677` at `c7e3dfcc87` in `m6-emulators-standalone-677`,
the T3 session `m6-t3-emulators`; Extended, the two calls authorized; VNC 24,
SSH 10037). **Earlier:** T30 (`docs/reviews/briefs/emulators-standalone.md`, Extended, for the T3
session in `m6-emulators-standalone-677`), both at version 1 with futro
addenda, their stranger's proofs running at 07:3x; version 2, the issues'
sixteen criteria, the worktrees stacked on P1 + this tip, the seeds, then the
dispatch comments. **Tree exports go under `/workspace/tmp/m6-coordinator/`,
never the scratchpad on `/tmp`** (the tmpfs ran out of inodes at 07:13 under
two lanes' exports). **Rule edits by this lane
since `8ebaf8daad`** (the ledger the doctrine futro's A7 asks for; posted on
#651 once T4 is at stage A, and listed here as they happen):
`8c9b1d4721` `generic-x64-vm-testing.md` +7, lines 1225 to 1231 (`time-to-play`'s
reboot drops bind mounts, #797); `ab8f750784` `engineering-practices.md`
+7, a bullet under § A name is not a behaviour (a count or a line number is
a claim about one tree; blindspot 75's guard). **Accepted lanes' rule
edits, the coordinator's by acceptance, reaching `next` in the merge order:**
T2 `f16cf7fc28` `es-native-ui.md` +5/-1 (#699's `--root` paragraph). The
registers' and the friction log's appends are not rule edits. **T4's brief is
at version 2** (`0921782112`); #810 (the lint refuses Local at epic tier) is fixed on
`fix/m6-810-lint-local-epic` (`fa6bcdafa8`, T1's lane) and merged here at
`18747fbc52`; T4's dispatch now waits only on the maintainer's answer on #346. A
`fix/*` branch stays one commit; its work-log entry is this lane's. Both lanes report on their issues; nothing wakes this lane on a
post, so read #648 and #649 at every turn. **And nothing wakes a lane on a
comment:** a lane's turn ends when it posts a question, so every answer the
coordinator gives on an issue is also sent as `herdr agent prompt <lane>`,
the same minute (T1 sat idle 78 minutes on 2026-10-23 after an answer that
was only a comment). Before calling a lane idle, read its worktree's branch
and status, not the origin. **A seed ends with "do not end a turn on a post that asks nothing; post checkpoints and continue"** (T5 stopped after stage A on 2026-10-24 because its seed's list ended there), and the agent-state watch (`herdr agent get`, every 30 s, idle named at ten minutes) is armed for every working lane. A prompt that does not flip a lane to `working`
within a minute went nowhere: `herdr agent read <lane>` shows why (a settings or
usage dialog eats typed text; `herdr agent send-keys <lane> esc`, then the
prompt, then `send-keys enter`).

## State at 2026-10-24 (the coordinator's own update, midday)

The day's work log (`docs/work-logs/2026_10-work_logs/2026_10_24-work_log.md`)
is the narrative; this is the index of what a resuming agent must know.

- **Host.** M7 returned the host at 05:42 (its last block on
  `/tmp/m7-m6-host-coordination-20261023.txt`); M6 holds it. T30's guest
  cycles run under that hold with census lines; every M6 block on the file
  is an `== M6 coordinator -- HH:MM UTC:` ack with the census
  (`pgrep -c -x qemu-system-x86`, M6 pidfiles, compilers). Read the file
  before any runtime. `/tmp` is a tmpfs that ran out of inodes at 07:13:
  tree exports and simulated merges go under `/workspace/tmp/m6-coordinator/`
  after `df -i`.
- **Lanes and sessions.** `m6-t3-emulators` (pane `wN:p6`) ran T3 and runs
  T30 in `distribution.worktrees/m6-emulators-standalone-677`;
  `m6-t5-build-engine` (pane `wN:p7`) ran T5 and T6 and is free for T7; the
  T1 session ran the #802/#806/#825/#810 fix packets. A lane's worktree is
  read with `git -C`, never written. The agent-state watch (`herdr agent
  get` every 30 s, idle named at ten minutes) is re-armed for every working
  lane; before calling a lane idle, read its worktree and the host's
  processes (a Facilitator call in flight is a wait, not idleness).
- **Register and blindspots.** Decided rows end at D-WORKFLOW-195 on this
  branch (193: an archive without `PKG_SHA256` fails the fetch; 194: five
  archive versions in four recipes; 195: a seat cut by its output ceiling
  re-runs on a trimmed packet, same model and effort); the next free ID is
  196 and a lane may take it. Blindspot entries run to 75 (a corpus read on the wrong tree;
  its guard is `engineering-practices.md` bullet `ab8f750784`); 29 is used
  twice (#811).
- **Briefs and streams on this branch:** `docs/reviews/briefs/` holds the
  slice briefs (p1-survey, os-launch-control-state, es-launch-path,
  emulators-libretro, emulators-standalone, build-engine,
  build-engine-upstream-tools, doctrine-rules, generic-packages-reached v1),
  the stream briefs (`t1-` to `t6-streams.md`, `fix-packets-802-806.md`,
  `lint-local-epic-tier.md`); `docs/futros/2026-10-24-m6-*.md` the area
  futros (doctrine, build-engine, emulators-and-cores, generic-packages).
- **Issues filed by this lane today:** #807, #808, #809, #810 (fixed, merged
  here at `18747fbc52`), #811, #838, #839, #842, #843, #844, #847, #848, #849,
  #850. The lanes filed #813 to #837, #841, #845, #846.
- **Open with the maintainer on #346:** a third lane for T4; the #825
  disclosure timing; `LOCAL_SSH_KEYS_FILE` in Docker builds; D-SYS-014;
  D-WORKFLOW-191; the `portaudio` re-hosting (#849).
- **Integration (after the M7 candidate):** P0, P1, T1, T2, T3, T30, **`fix/m6-877-libfmt-sha256` (`cf3a8d8e62`, one commit: the empty `PKG_SHA256` T5's fetch would refuse)**, T5, T6,
  T7, T4; at integration flip `add_es_system`'s zero-default WARNING to
  `return 1` after T3's S2 and regenerate the five tables; the #802/#806/#825
  adaptations; close #823, #841, #845 and the other fixed bugs at the merge;
  the `fix-pending-image` rows are proved on the first image.

## The seed brief (2026-10-22, the planning session's handoff, verbatim)

The first message this lane received, pasted by the maintainer from the P0
planning session; kept here because the maintainer asked that the lane consult
it at each step (*"You should have a copy of the original seed I provided for
this exercise"*). The intent it serves is D-WORKFLOW-181's, in the maintainer's
words there.

> Started by the P0 planning session (Claude Fable 5.1, Herdr pane wN:p1, tab "P0 planning (#346)") on the maintainer's direction of 2026-10-22. You are the M6 coordinator lane (D-WORKFLOW-183): the renovation program's planner, brief-writer, gate-acceptor and integrator, running on Fable; the work lanes run on Opus 5.5. Your worktree is /workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346 on feature/m6-renovation-plan-346; the primary checkout /workspace/repos/pixelelated/distribution stays on next with no resident session, and you are its keeper. Read first, in this order: .github/sessions/saved-session-state-feature-m6-renovation-plan-346.md (your lane's pointer), docs/reviews/plan-for-the-plan.md, the live M6 milestone body, issues #346, #641 and #640 on pixelelated/distribution, then next:AGENTS.md and the every-session rules. The maintainer's direction, verbatim: "the coordinator will be Fable and the work will be Opus 5.5" and "we begin our work and ensure that everything is in the new work tree with the seeded session file to resume, and that there's a corresponding branch. We can then begin work there." Gates: nothing merges to next until the M7 lane's post-candidate merge clears the push guard, and never with --no-verify; the P1 lane (Herdr tab "P1 Survey (#641)", agent m6-p1-survey, worktree m6-p1-survey-641) pauses at its pass-7 gate on #641 for the maintainer's yes, which reaches it through you, one question at a time; you accept P1 at hand-back against brief section 10; one session per worktree, so never write in the P1 worktree. Report on #346 and #641. First action: read your pointer and the plan, confirm on #346 in one comment that you have resumed (your session id from herdr agent list, this pane, the time), then wait for P1's pass-7 post or the maintainer; do not start new work streams on your own.  Also: append this lane start to docs/work-logs/2026_10-work_logs/2026_10_22-work_log.md in your worktree (the planning session writes there no longer, one session per worktree), run tools/work-log-index --write, commit with Refs #346 and push; and note on #346 that Claude Code reports the 25 instruction files at 324.2k characters, over its 150k limit, so the rules load truncated in every lane, a finding for the doctrine slice.

