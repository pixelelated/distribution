# Brief: M6.P2 T1, the OS scripts: launch, control and state (#648)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #648 differ, #648 wins and the
coordinator corrects the brief in the same session. **Version 2
(2026-10-23):** version 1 was read by the area epic's futro
(`docs/futros/2026-10-23-m6-os-scripts-and-launch.md`, #695) and by a
stranger's proof (plan § 3, principle 3), which together found thirteen
statements wrong or unverifiable and nineteen questions the text did not
answer; every one is answered below, and the proof is recorded at the end
of § 10.

## 1. Identity

- **Issue:** #648 `M6.P2 E695/T1: os-scripts-and-launch: the OS scripts:
  launch, control and state (Tier 1)`, slice `os-launch-control-state` in
  `docs/reviews/slices.json`, first in `docs/reviews/order.md` (the order's
  row is D-WORKFLOW-188). **Epic:** #695, the OS scripts and launch path
  (T1, T22, T29), under the renovation epic #339; its futro is the comment
  on #695 and the file named above. **Milestone:** M6 (`M6: Codebase
  renovation`); its body holds the live order; read it first.
  **Predecessors:** #346 (the plan), #641 (the survey, the inventory and
  the order; closed 2026-10-23). **The dispatch** is the coordinator's
  comment on #648 that names this brief's commit, the model and effort,
  and authorizes the two external reviewer calls and the `npm install` of
  § 1; the lane's first comment answers it.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, re-order anything, change a criterion, write a
  brief, move the M6 body, edit `slices.json`, `areas.json`, `order.md` or
  the plan, or decide a question of scope: those are the coordinator's,
  reached through #648, one question at a time. What this lane does file:
  its own audit punch-list issue (stage D, the code-auditor skill's Phase
  6) and a `bug` issue for every defect it finds (D-WORKFLOW-187: a defect
  found by the renovation is a bug like any other; `bugs-are-agent-first.md`
  gives the shape, with its VM-verifiable criterion). Nothing else.
- **Branch and worktree:** `feature/m6-os-launch-control-state-648` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-os-launch-control-state-648`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`**, which carries the P0 branch; the coordinator's tip merged
  in at `86d3a49f6c` and the lane's pointer seeded at `a9a46455d9`. The
  coordinator wrote in this worktree only before the lane started; from the
  dispatch on, one session per worktree (D-WORKFLOW-183) and the coordinator
  writes nothing here. `next` is gated until the M7 lane's candidate merges
  (never `--no-verify`), and the merge order after it is P0, P1, then this
  branch (D-WORKFLOW-182, plan § 8). Plan § 7 names the shape
  `feature/m6-<slice>` and `<slice>`; the lanes append the issue number, as
  the two renovation lanes before this one do. **The rules in this worktree
  are `next`'s except two files P1 extended** (`fork-workflow.md` and
  `instruction-files.md`: the three renovation tools added to the fork-tool
  lists, commits `9966dbcd12`, `af24589b1c`, `fc88815ccb`); the first
  commands check it. The primary checkout is
  `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025).
  **`worktrees.md`, `device-builds.md`, `CLAUDE.md` and `AGENTS.md` still
  name the legacy layout (`/workspace/repos/rocknix`, `rocknix.worktrees/`);
  #640 owns that drift, and this brief's paths are the ones to use.** The
  legacy checkout and every worktree beside it are the M7 lane's: read from
  them (an image, a build root, a diff), never write.
- **Model and effort:** Opus 5.5 at high effort (the maintainer, 2026-10-22:
  *"the work will be Opus 5.5"*), unless the dispatch says otherwise.
  Record what actually ran in `00-running-log.md`'s header.
- **Review depth: Extended** (plan § 6c; `slices.json`: launch path and
  state preservation). The primary auditor is this lane (Anthropic). The two
  reviewers come from two other labs, each through the Facilitator and
  nothing else (D-WORKFLOW-049, D-WORKFLOW-137; `adversarial-council.md`
  rule 4; the code-auditor skill's Phase 4.6):
  - **GPT-6 Astra**: `tools/council/run invoke --member gpt --provider
    openrouter --prompt-file <brief> --output <file>` at `max`, the installed
    recipe (`openai/gpt-6-astra`, provider pinned to OpenAI).
  - **Gemini 4 Argon** (Google), the third lab the M7 lane verified on
    #638/#639 (its row D-WORKFLOW-180 is on the M7 branch, unmerged). **Its
    route is `--member gemini-argon`, and it is not in this tree:** it
    arrives with two commits on the legacy checkout's
    `feature/m7-audit-integration-603`, `1c7d283ad5` (the route in
    `scripts/council-invoke.ts` and `council-seat-efforts.json`) and
    `a7a3bdda4e` (`tools/lint-audit-artifacts` accepting the member; this
    tree's lint refuses any member outside `claude`, `gpt`, `gemini`,
    `kimi`, `muse`). Neither touches a slice path. At Phase 4.6, `grep -c
    gemini-argon scripts/council-invoke.ts tools/lint-audit-artifacts` says
    whether both have arrived (two non-zero counts). If they have, invoke
    `--member gemini-argon --provider openrouter` at `high`. **If they have
    not:** run the Astra pass, write the Argon seat as pending in
    `04-analysis.md` § Second opinion, and **stop at Phase 4.6 as a named
    blocker on #648** (§ 8): the depth is incomplete, Phase 5 does not
    start (phases.md § 4.6), and the roster's `--member gemini`
    (`google/gemini-3.8-flash`) is never called in its place. The
    coordinator's remedy is its own: the two commits brought onto this
    branch, or the M7 candidate's merge waited for. A seat that fails
    identity verification is recorded, never replaced.
  - Both reviewers run the **refutation pass alone** (the audit is epic
    tier; phases.md § Phase 4.6: two calls at Milestone tier, one otherwise),
    each prepared independently. `second-opinions/review-plan.json` is
    written before the first call (`templates.md` § Second opinion: depth
    `extended`, primary `anthropic/claude-opus-5-5`, lab `anthropic`,
    identity source the dispatch comment and the session's own metadata,
    two reviewers). Every seat item is a lead; the orchestrator re-reads the
    artifact before a row is written.
  - The runner's dependencies are not in a fresh worktree: `tools/council/run`
    execs `tools/council/node_modules/.bin/tsx`, and `node_modules/` is
    gitignored. Install once, before Phase 4.6, with `npm install --prefix
    tools/council` (a gitignored write; the npm registry; `node` v24 and
    `npm` 11 are on the host; record the `tsx` version in
    `00-running-log.md`). The key is sourced from `~/.config/council/env`
    (present, never read into a transcript, never on a command line). The
    dispatch comment on #648 is the authorization for exactly these two
    external calls plus a probe of each seat first, its provenance naming
    the served model.

First commands:

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-os-launch-control-state-648
git fetch origin && git fetch upstream --no-tags
git rev-parse --short upstream/next                                  # record it: Q4's upstream pin for this slice
git branch --show-current                                            # feature/m6-os-launch-control-state-648
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md   # exactly fork-workflow.md and instruction-files.md; any other file is STALE
git diff --quiet 8ebaf8daad HEAD -- projects/ROCKNIX/packages/rocknix/ && echo "slice bytes are next's 8ebaf8daad"   # must print
test -f docs/reviews/briefs/os-launch-control-state.md || { echo "the brief is not in this tree: stop"; exit 1; }
test -f docs/futros/2026-10-23-m6-os-scripts-and-launch.md || echo "the epic's futro is not in this tree: ask the coordinator before the first audit commit"
cat .github/sessions/saved-session-state-feature-m6-os-launch-control-state-648.md   # the lane's seeded pointer
```

The order of the first session: § 3's reading first (it is the pre-flight,
`working-principles.md`; it fills the first hour), then stage A.

## 2. Scope

**One package, read line by line, less one script.** Every tracked path
under `projects/ROCKNIX/packages/rocknix/` except
`sources/scripts/backuptool`, which the area map places in
`cloud-sync-and-saves` and T17 (`cloud-setup-content`) reads with the
settings archives. The membership is the inventory's: the rows whose `area`
is `os-scripts-and-launch` and whose path starts with the package (#648
says the same set as `tools/renovation-inventory --order`'s membership; the
filter below is the re-derivation, because `--order` writes files).

**The hash.** The slice's bytes are `next`'s at `8ebaf8daad` (`next` and
`origin/next` were both there on 2026-10-23); the branch carries the same
bytes under the package, which the first commands prove. **`reviewed-at:`
is this branch's `HEAD` at stage A** (the commit the read is made at),
recorded with `8ebaf8daad` beside it in `00-running-log.md` and
`01-research-notes.md` § Scope. The stop (§ 8) is the branch's bytes under
the package differing from `8ebaf8daad`'s: then the slice was re-based under
the read and the coordinator re-baselines it. `next` moving later (the M7
candidate) is not a stop; it is drift, below.

**The counts, recorded by the survey at `eb4763e3cc` and re-derived here.**
A count that differs is a delta beside the recorded one, not a stop; the
stop is a count that cannot be produced, or two commands for one quantity
that disagree. The inventory's line count is git's numstat against the
empty tree (`docs/reviews/README.md`), so re-derive with the same
definition, not with `wc -l`:

```bash
git ls-files projects/ROCKNIX/packages/rocknix | grep -v -F 'sources/scripts/backuptool' | wc -l     # 83
python3 -I - <<'PY'
import json
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
t1 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "os-scripts-and-launch"
      and r["path"].startswith("projects/ROCKNIX/packages/rocknix/")]
print("paths", len(t1), "lines", sum(r["lines"] or 0 for r in t1),
      "fork-own paths", sum(1 for r in t1 if r["tier"] == "fork-own"),
      "upstream-carried paths", sum(1 for r in t1 if r["tier"] == "upstream-carried"),
      "fork-own lines", sum(r["lines"] or 0 for r in t1 if r["tier"] == "fork-own"))   # 83, 13327, 29, 54, 8369
for r in sorted(t1, key=lambda r: -(r["lines"] or 0)): print(r["lines"], r["tier"], r["language"], r["reach"], r["path"])
PY
git diff --numstat "$(git hash-object -t tree /dev/null)" 8ebaf8daad -- projects/ROCKNIX/packages/rocknix/ \
  | grep -v -F 'sources/scripts/backuptool' | awk '{s+=$1} END {print s}'                              # 13327
```

Recorded: **83 paths, 13,327 lines, all of them read line by line in this
slice** (the inventory's `read` figure for the slice, 11,560, counts code
languages only and leaves out the `none`-language `001-functions` and the
configuration files; this brief reads those too, `001-functions` being the
settings-lock code); **8,369 lines fork-own** (7,441 of them in code
languages); tiers fork-own 29 paths, upstream-carried 54. Every path is
`reach: shipped` in the inventory, which is package-level: within the
package, `profile.d/100-amd64-freqfunctions` is installed on x86_64 only
and `099-freqfunctions` on the others, and `hdmi-hotplug.path` is enabled
on H700 only (`package.mk` lines 119 to 126 and 116). Upstream carries 43
commits touching the package since the merge base (`git log --oneline
c445081a59..upstream/next -- projects/ROCKNIX/packages/rocknix/ | wc -l`,
merges included, at the `upstream/next` of 2026-10-23), Q4's list. The
closed `bug` issues that name these scripts are Phase 1's: `gh issue list
--repo pixelelated/distribution --label bug --state closed --limit 500
--json number,title,body`, grepped with word boundaries for the script
names of this package (`\b(runemu|setsettings|chksysconfig|post-update|...)\b`;
the count depends on the pattern, so record the pattern with the count).

**Where the files land on the image.** `package.mk` copies every file of
`sources/scripts/` to `/usr/bin/` at mode 0755, `sources/post-update` to
`/usr/share/post-update`, `config/*` to `/usr/config/` (with `/system` a
symlink to `/storage/.config/system`, so `system.cfg`'s live copy is the
player's), and edits `system.cfg` at build time (the device name, and under
`DEVELOPMENT_DEFAULTS` ssh, samba, wifi on and `system.loglevel=verbose`).
The build engine's `scripts/install` (lines 86 to 114) places the rest:
`profile.d/*` to `/etc/profile.d/` (every shell that sources
`/etc/profile`; `get_setting`, `set_setting` and `redact_credentials` are
functions from `001-functions`, not files), `autostart/*` to
`/usr/lib/autostart/common/` (run in order by
`projects/ROCKNIX/packages/sysutils/autostart`'s `autostart` under
`rocknix-autostart.service`, T22's), `system.d/*` to
`/usr/lib/systemd/system/` (five enabled by the recipe: `rocknix-autostart`,
`rocknix-memory-manager`, `save-sysconfig`, `rocknix-evidence.timer`,
`rocknix-sysconfig`; `hdmi-hotplug.path` on H700), `udev.d/*.rules` to
`/usr/lib/udev/rules.d/`. `/usr` is a read-only squashfs on the device,
which § 5 cares about. On the image, `/bin/sh` is a symlink to **dash**,
`/bin/bash` is present, `/usr/bin/python` and `python3` are symlinks to
`python3.14` (read from the build root's `image/system`, § 5).

**Three groups, read in this order** (the slice's reason to be first is the
launch path, plan § 6a; `slices.json`'s `why`):

1. **The launch path** (on the order's launch-path list): `runemu.sh` (626
   lines: configures and starts the emulator; #336 replaces its RetroArch
   half), `setsettings.sh` (1,479: the per-core RetroArch settings written at
   every launch), `run` (61), `profile.d/001-functions` (707:
   `get_setting`/`set_setting` under the settings lock, D-INFRA-012,
   D-SYS-011/012; `redact_credentials`, D-INFRA-011), the `profile.d`
   frequency, GPU and controller fragments the launch reads.
2. **State** (on the order's state-preservation list): `chksysconfig` (342:
   `verify` at sysinit from `rocknix-sysconfig.service`, `backup` at
   shutdown from `save-sysconfig.service`; D-CLOUD-078/079/080/082),
   `post-update` (251: run once after an update by `autostart/003-upgrade`
   when `/usr/share/post-update` exists; `userconfig-setup` in T22 only
   mentions it in comments; D-SYS-007; `upgrade-and-install.md` whole),
   `factoryreset`, `installtointernal`, `automount` (D-CLOUD-056/057 and
   `rocknix-automount.service`), `config/system/configs/system.cfg` (the
   defaults the recipe edits), `autostart/001-setup`, `003-upgrade`,
   `007-rootpw` with `setrootpass`.
3. **Control and services**: `rocknix-memory-manager` (+ its unit),
   `rocknix-evidence` (+ service and timer; D-SYS-005, D-INFRA-014;
   `handheld-evidence.md`), `rocknix-corekeep`, `usbgadget` (`#!/bin/sh`,
   dash; + the udev rule and `autostart/081-usbgadget`; #531), `wifictl`
   (D-WORKFLOW-040; #159, #201), `rocknix-bluetooth` and
   `rocknix-bluetooth-agent` (python, with `bluetooth-agent.service`),
   `rocknix-fake-suspend`, `suspendmode`, `brightness`, `volume`,
   `paneladj`, `led_flash`, `handle-hdmi-hotplug` (+ path and service),
   `rocknix-report-stats` (+ service and the two timer entries),
   `rocknix-config`, `rocknix-settings`, `rocknix-info`, `rocknix-update`
   (the manual-updates stub; #694 wants online updates), `rocknix-keyboard`,
   `rocknix-scraper`, `rocknix-retroachievements-info`, `updateabl`,
   `migrate_roms`, `show_changelog`, `vertical-check`, `getshaders`,
   `getoverlays`, `getfilters`, `amionline`, `say`, `timeinfo`, `error.sh`,
   `find.sh`, `controller-layout`, the remaining `autostart` fragments
   (006, 008, 009, 010, 050, 055, 080, 099), `config/system/configs/tz`,
   `motd`, `rocknix.target`, `package.mk` itself (the recipe:
   `tools/pkgcheck`, late binding, the `LOCAL_WIFI_KEY` it writes into a
   `.psk` at build time, which the credential filter of § 5 covers when it
   is read back). **Driven from the interface, not the launch:**
   `rocknix-es-thebezelproject` (641) and `rocknix-systems` (python, 250)
   are called only by EmulationStation's `ApiSystem.cpp` at the pin (the
   bezel installer and the systems list). **No caller found at all** (the
   survey's `grep -rlF` over `packages projects scripts tools` and the ES
   checkout at the pin, 2026-10-23): `setemu.sh` (30) and `bezels.sh` (217),
   Q6's first two candidates.

The security list names four of these (`setrootpass`, `wifictl`,
`usbgadget`, `rocknix-evidence`), the state list six (`chksysconfig`,
`factoryreset`, `installtointernal`, `automount`, `post-update`,
`setsettings.sh`), the launch-path list three (`runemu.sh`,
`setsettings.sh`, `run`); `order.md` § The security, state-preservation and
launch-path files. A finding in one of them is Extended-depth material by
definition.

**Interacting subsystems, read-only context** (never read line by line here,
never changed here; a defect found in one is a lead posted on #648 for its
own slice): the interface's launch path (T2: `FileData::getlaunchCommand`
builds `runemu.sh`'s argument line from the systems table's template,
`FileData::launchGame` runs it, `ViewController` launches, and
`LaunchCommand.h` only reads the finished line's `-P`, `--core=` and
`--emulator=` tokens, as whole shell words with the last one winning,
where `runemu.sh` reads `${ARGUMENTS##*-P}`, the last occurrence of the
letters anywhere in the line: the two readings differ by design note (the
header of `LaunchCommand.h`, lines 9 to 23: the launcher's side is the
launcher's to change, this slice's F-07 #730); version 2 said
`LaunchCommand.h` builds the line, corrected 2026-10-23 from T2's seam map
and its stranger's proof;
`ApiSystem` calls this package's scripts by name, T21); `es_systems.cfg`
and its generator `projects/ROCKNIX/packages/virtual/emulators`
(`mk_es_systems`, T3); the autostart runner and the systemd units, power and
sleep scripts of `projects/ROCKNIX/packages/sysutils/` (T22; `autostart`
runs this package's fragments from `/usr/lib/autostart/common/`, `sleep.sh`
reads the quirks, `userconfig-setup` seeds the player's config); the
per-handheld quirks under `projects/ROCKNIX/packages/hardware/quirks/`
(T29); the cloud scripts under
`projects/ROCKNIX/packages/network/rclone/sources/` that the exit path
reaches (T16, T17; `backuptool` with them); the offline achievements proxy
(T19); `system.cfg` and `es_settings.cfg` as the state these scripts read
and write. The EmulationStation checkout for the callers' side is
`/home/max/Development/emulationstation-next` at the pin in
`projects/ROCKNIX/packages/ui/emulationstation/package.mk`
(`16dbac5211eea7e70db7394372033be2be7df829`); its current branch is
somebody else's work, so read it with `git -C $ES grep -F <name> $PIN`
only, never by checking anything out there.

**Known incoming drift.** The M7 lane's candidate image is built from
`069fc2704421` in the legacy checkout, 12 commits ahead of `next` and not yet
on it; three of them touch this package (`d535e026b2`, `3b27b9a70d`,
`069fc27044`), changing `runemu.sh` by about 63 lines and `package.mk` by
two. Read that delta once, read-only, as context:

```bash
git -C /workspace/repos/rocknix log --oneline next..069fc2704421 -- projects/ROCKNIX/packages/rocknix/
git -C /workspace/repos/rocknix diff next 069fc2704421 -- projects/ROCKNIX/packages/rocknix/
```

The slice reads `next`'s copy. A finding whose lines M7 is changing is
recorded with that fact; the drift tool re-opens this slice over the diff
when the candidate lands, because `runemu.sh` is on the launch-path list
(plan § 8). The swarm rule holds the other way too: a punch item that would
touch those hunks is announced on #648 before any stream brief is written.

**Out of scope here:** every other package, the ES sources, `backuptool`,
the cloud scripts, the quirks, the devices' `options`, the kernel. A reading
of one of them for context is noted as such in `01-research-notes.md`; a
finding in one is a lead for its slice, posted on #648 with the slice named.

## 3. Read first

From `next`, in this order, before any analysis (this is the first
session's first hour; stage A follows it):

- `.github/sessions/saved-session-state-next.md` (the M7 lane's canonical
  checkpoint; read for what runs on this host, not for a work queue) and
  this lane's own pointer.
- The code-auditor skill whole: `.claude/skills/code-auditor/SKILL.md` and
  its `references/phases.md`, `review-levels.md`, `templates.md`,
  `anti-patterns.md`. The slice runs under its lifecycle with the renovation
  face added (plan § 6b); stage B's Phase 2 criteria are #648's checklist,
  and Phase 3 carries § 4 below as its renovation face beside the skill's
  own faces.
- Rules whose `paths:` match this slice, with the sections that bind these
  scripts: `packaging-and-patches.md` and `packages/README.md` (the recipe);
  `rclone-cloud-sync.md` (`rocknix/sources/scripts/**` is in its glob:
  § Critical gotchas, § Style, § Config conventions, § What the audit's fixes
  changed in the scripts' quiet behaviour, § What the audit of the fix round
  changed); `generic-x64-vm-testing.md` (§ Headless, § Fixtures for the
  launch path, § What the guest's busybox lacks, § A settings change made
  from the shell is invisible to the running interface, § Private settings
  modes, § Crash and hang recipes, § The interface runs under
  `essway.service`, § Spin a guest down, § After every VM cycle);
  `handheld-evidence.md` (what survives what; `rocknix-evidence`);
  `change-log.md` (a player-visible change written the day it lands; stage
  E); `upgrade-and-install.md` whole (every fix answers *Already written*,
  D-WORKFLOW-050). Then the every-session set: `engineering-practices.md`
  (§ Verify design intent, § Verify the artifact, § A name is not a
  behaviour, § Guards must fail closed, § Before deleting a duplicate,
  § Stop after three fixes, § Fail gracefully, § Nothing runs on a person's
  device, § Never edit a shell tool in flight), `time-to-play.md`,
  `least-surprise.md`, `player-language.md` and `es-player-text.md` (the
  strings these scripts print: the outcome vocabulary, the `>>> why` lines,
  no exit code or log path on a screen), `bugs-are-agent-first.md`,
  `vm-first.md`, `issue-tracking.md`, `decision-register.md`,
  `learning-capture.md`, `ceremonies.md`, `worktrees.md` (removal; its
  layout is superseded, § 1), `fork-workflow.md`,
  `milestone-phase-naming.md`, `adversarial-council.md`,
  `working-principles.md` (§ Pre-flight: say which rules were read). Known
  stale facts so they do not cost an hour (#640): the legacy paths in
  `worktrees.md`, `device-builds.md`, `instruction-files.md`, `AGENTS.md`
  and `tools/fork-worktree`'s hint; `device-builds.md` § Our devices is
  current.
- `docs/blindspot-register.md` whole, once (73 entries). The entries that
  touch these paths: **32** (causal order read from wall clocks that jumped
  mid-boot: `automount`), **33** (a sentinel exit code borrowed from the
  wrapped tool's space: the autostart fragments), **34** (a check written
  for the device, proven under the host's tools: `chksysconfig`,
  `system.cfg`, busybox `tr`), **43** (a safety claim in a header comment,
  never tested: `rocknix-evidence`, `setsettings.sh`), **57** (a fix that
  covered fewer sites than its issue named: `wifictl`); and the general ones
  a reading repeats: 7 (host tools are not the device's), 13 (assumed
  done), 30 (a resumed session built on its own summary), 51 (an open
  checkbox is a claim), 64 (read the cause before lengthening a wait), 73
  (a monitor of completion, not activity).
- Prior audits of these paths under `docs/audits/`, **as provenance only**:
  which paths were audited, when, at what tier; verdicts are sequestered
  until Phase 2.5 and never transcribed into Phase 2. The punch lists that
  name these scripts, counted with `grep -c -i -E
  'runemu|setsettings|post-update|chksysconfig|factoryreset|automount|installtointernal|001-functions|usbgadget|wifictl|rocknix-evidence|rocknix-info|corekeep'
  05-punch-list.md`: `2026_09_25-milestone-rc-round-since-258` (28),
  `2026_09_24-milestone-rc-round-since-186` (17),
  `2026_09_28-milestone-audit-of-the-fix-round` (8),
  `2026_09_14-epic-offline-retroachievements` (4),
  `2026_09_28-milestone-audit-of-the-fixes-307` (3),
  `2026_10_14-milestone-m7-next-candidate` (2),
  `2026_09_06-issue-device-flashing-runbook` (2),
  `2026_09_29-milestone-audit-of-the-313-fixes` (1),
  `2026_09_12-milestone-cloud-saves-since-60` (1); and
  `2026_09_10-graceful-degradation/` (no punch list; its README and three
  reports read every writer of these scripts for D-CLOUD-077/078).
- Decisions by ID, cited and never re-argued. The launch path: D-LAUNCH-001
  (an exit by the hotkey's signal reads as a clean exit), D-LAUNCH-004
  (`/var/log/exec.log` is one launch's), D-CLOUD-065 (the `cloud.backup`
  exit hook was removed from `runemu.sh`), D-CLOUD-098 and D-CLOUD-109/113
  (time to play; a visible sync is bounded, never cancelled; two contracts),
  D-UI-042/045. State: D-CLOUD-077/078/079/080/082 (fail gracefully; the
  last known good state; `system.cfg.backup`'s meaning; `chksysconfig
  verify` at sysinit), D-SYS-011/012 (`settings_base`; several settings
  written as one rename), D-INFRA-012 (the settings lock is pid-only),
  D-CLOUD-056/057 (`automount` waits for the expected card at no boot
  cost), D-SYS-007 (`post-update` removes a deprecated sysctl line, one line
  at a time), D-WORKFLOW-050 (*Already written*). Control: D-SYS-001 to
  D-SYS-005 (persistent logs, the watchdog, the hang policy, ramoops,
  `rocknix-evidence`; **D-SYS-006, a userspace watchdog, is an open
  question in the register's open table, not a decision**), D-INFRA-011 and
  D-INFRA-014 (`redact_credentials`; evidence collections serialised by an
  flock), D-WORKFLOW-040 (`wifictl forget`), D-QA-021 (the credential
  filter on every read). The program: D-WORKFLOW-181, 183, 184, 185, 186,
  187, 188, 189; D-WORKFLOW-137 (depth and the reviewer's lab),
  D-WORKFLOW-049 (every seat through the Facilitator), D-WORKFLOW-162 (check
  upstream early) and D-WORKFLOW-164/165 (consider contributing a fix
  upstream; submissions deferred), D-WORKFLOW-132 and D-QA-012 (an issue
  before work; the maintainer's words quoted), D-WORKFLOW-149 (a checkpoint
  is not a stop), D-QA-007/015 (the VM first; nothing on a person's
  device), D-QA-044/045/051 (criteria an agent ticks; say checkbox; what a
  bug is), D-UI-079 (change stays inside the fork's lanes: it governs a
  player-visible behaviour change to an upstream surface, which is put to the
  maintainer first through the coordinator; a defect or cruft in an
  upstream-carried script is this program's to find and fix, #339's
  Tier 2 words: *"there is no longer anyone to send them to"*).
- Open issues whose bodies name these paths (read for the planned changes
  and the known leads, not as a work queue): #336 (the libretro runner that
  replaces `runemu.sh`'s RetroArch half; its Step 1 is why this slice is
  first), #10, #18, #79, #104, #120, #159, #191, #196, #201, #256, #266,
  #292, #293, #309, #316, #322, #323, #326, #561, #694; #585 (the upstream
  contribution queue, where a fix that upstream would take is recorded);
  #644 and #645 (the build-path read: none of its findings ride this
  slice). Every `gh` call carries `--repo pixelelated/distribution`.

## 4. The questions

All seven apply to this slice (plan § 4); none is struck. Provenance decides
the lens (plan § 3): the 29 fork-own paths get all seven in full; the 54
upstream-carried paths get Q6 and Q4 first, and the rest only where the file
stays. Per path (a script, a unit file, a fragment, the recipe), the
evidence that answers each:

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | Bash idioms the rest of the tree has left (backticks, `[ ]` where `[[ ]]` is meant, `echo` where `printf` is, `cat` into `grep`); hand-rolled parsing of `system.cfg` or `es_settings.cfg` beside `get_setting`; a systemd unit written the old way (no `Type=`, no ordering, no hardening the others carry); the two python scripts' interpreter lines (`rocknix-systems` says `python`, `rocknix-bluetooth-agent` `/usr/bin/python`; on the image both `python` and `python3` are symlinks to `python3.14`); the `tz` list's currency against the image's zoneinfo | the replacement named with where the tree already uses it; `git log -S` for when the old form stopped being written |
| Q2 Standards | The rules § 3 names, cited by section; `set -euo pipefail` and quoting where the interpreter allows it (the scripts declare `bash`, `sh` and `python`; on the image `/bin/sh` is **dash**, `/bin/bash` is present, and busybox provides 182 applets without `grep`, § What the guest's busybox lacks: a `#!/bin/sh` script such as `usbgadget` is read against POSIX sh and proven under dash on the guest, never under the host's bash); late binding in `package.mk` (`tools/pkgcheck rocknix`); every string a script prints to a screen against `es-player-text.md` (`tools/last-good-scripts-test` case e checks the FORBIDDEN shapes; `tools/vocabulary-check`); upstream headers kept and a fork line added (`CLAUDE.md` § `package.mk` rules). **`shellcheck` is not installed on this host (2026-10-23).** Do not install a system package. A static release binary from the project's GitHub release, unpacked under the worktree's gitignored `.qa-scratch/` with its SHA-256 recorded in `00-running-log.md`, is acceptable (network to github.com for that one download); otherwise record `shellcheck: not run` once in `01-research-notes.md` § Scope and answer Q2 by reading against the conventions | the rule and section; `tools/pkgcheck` output; `shellcheck` output where it ran, or the recorded absence |
| Q3 Bugs | Where each unit fails: the unhandled branch, the race, the wrong default, the path that works on the host and not on the device. The hot spots: root at boot and at every launch; the updater path (`post-update` from `003-upgrade`); the destructive scripts (`factoryreset`, `installtointernal`); `automount`'s card detection and its retries; `chksysconfig`'s verify and backup semantics against a cut file; `setsettings.sh`'s per-core writes and what a kill mid-write leaves; `runemu.sh`'s argument parsing, exit status and logs; the settings lock | a reproduction on the GENERIC_X64 guest or a trace with `file:line`; host reasoning about device behaviour is a lead (§ 5) |
| Q4 Package currency | The package has no upstream tarball (`PKG_VERSION=""`, a meta package), so the question is ROCKNIX's copies of these files: every commit of `c445081a59..upstream/next` touching the package (43 at the `upstream/next` the first commands fetched and recorded; merges included and dispositioned as `merge`), dispositioned one by one (merged already / not applicable to this fork / to merge, with the reason); the inventory's `overlap` column names the paths both sides changed. Plus `tz` against the zoneinfo the image builds, and the python the image provides (3.14) | the `git log --oneline c445081a59..upstream/next -- projects/ROCKNIX/packages/rocknix/` list with a disposition per line; the fetch's hash recorded |
| Q5 Efficiency | What the launch path costs: the two time-to-play numbers on the guest at the image § 5 names, beside the baseline #336 records (a game's first frame 1.05 s from the press, the next game's 2.03 s from the exit, on the VM), with the guest's `system.loglevel` recorded beside them (this engineering image ships `verbose` under `DEVELOPMENT_DEFAULTS`; measure at the image's defaults, record them, and compare like with like); what `runemu.sh` does per launch, itemised, with `setsettings.sh` timed in the guest (`time bash /usr/bin/setsettings.sh <args>`, the arguments taken from `/var/log/exec.log` after a launch at `verbose`, D-LAUNCH-004); what runs every exit; what runs at boot in the autostart order and how long each fragment takes (`systemd-analyze blame` and the journal's timestamps); `rocknix-memory-manager`'s loop and `rocknix-evidence`'s five-minute page in memory on a 1 GiB handheld; the player's steps where a script drives a flow | `tools/time-to-play` output; a measurement in the guest with its command; or the named absence of one |
| Q6 Dead ends | Is each script, unit, fragment and function reached: by a built image (every path here is `reach: shipped` at package level; the two arch-exclusive fragments and the H700-only path are the exceptions, § 2), by any caller (`grep -rlF '<name>' packages projects scripts tools` in the distribution and `git -C $ES grep -lF '<name>' $PIN` in the interface at the pin, plus the units that `ExecStart` it and the udev rules), by any player path. Candidates the survey saw: `setemu.sh` and `bezels.sh` (no caller found anywhere, § 2), `rocknix-update` (a stub that prints manual-update text; #694), `updateabl`, `migrate_roms`, `show_changelog`, `rocknix-report-stats` (its service and the two timer entries), `say`, `find.sh`, `error.sh`, `getshaders`, `getoverlays`, `getfilters`, `controller-layout`, `rocknix-scraper`, `rocknix-keyboard`, `rocknix-retroachievements-info`, `vertical-check`; per-device branches inside the scripts for devices the fork does not ship (a row for the table, not a removal: `unshipped` is not `unreached`, D-WORKFLOW-185); `100-amd64-freqfunctions` (x86_64 only, by the recipe) | the reachability search as a command and its output, one row per script in `04-analysis.md` § Renovation face Q6; `engineering-practices.md` § Before deleting a duplicate before any removal; every removal carries `Already written:` (what the retired unit left on devices and in clouds) and names what the unit guarded, stamped and exposed (a `motd` line, an ES row through `ApiSystem`, a unit name another unit orders on) with a home for each |
| Q7 Clarity | Can a reader new to it tell what each unit does and why in one pass: `setsettings.sh` at 1,479 lines and `runemu.sh` at 626, one responsibility each or several; `001-functions` at 707 lines sourced into every shell; logic copied between `runemu.sh`, `setsettings.sh` and the interface (the launch command, the per-core defaults); comments that match the code; a header that says where the file came from (JELOS, ROCKNIX, this fork) | the unit named with what a reader stumbles on; a duplicate named with its original |

A finding is one question with its evidence; severity and category are the
code-auditor's, with `Renovation` as the category for Q1, Q5, Q6 and Q7
items that are not defects. A Q3 finding that is a defect is also a `bug`
issue (D-WORKFLOW-187, § 1), filed with the VM artifact that would close it.

**The RetroArch half.** #336 replaces the RetroArch half of `runemu.sh` and
the RetroArch settings `setsettings.sh` writes (the order's lens weighs the
nearest planned change, plan § 6a). Q1, Q5 and Q7 findings confined to those
lines are recorded on the punch list like any other and carried as
`deferred:#336` at Phase 7 unless the coordinator's stream brief says
otherwise; Q2 and Q3 findings there are fixed regardless, because a player
has them today (D-WORKFLOW-187). Phase 1 reads #336's body to draw the line
between the RetroArch-specific lines and the rest, and `01-research-notes.md`
§ Scope records where it was drawn.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict, as its `SKILL.md`
§ Evidence floor lists them (five rules under a heading that says three,
the last numbered 3 again; a lead for T38, posted on #685, not this slice's
to fix):

1. *Tracker state is never sole evidence.* Issue state, checked AC boxes,
   and retro summaries may corroborate but can never be the ONLY evidence
   for a PASS; every PASS cites at least one primary artifact (file:line,
   executed command output, or commit diff).
2. *Mechanical evidence outranks reading.* Where a check exists, RUN it and
   record the command, exit status and counts in the criterion entry (the
   skill's table names `tools/pkgcheck`, `tools/cloud-round-trip`,
   `tools/cloud-test-backend ls`, `tools/vm-visual-qa` and a device build;
   this slice's checks are listed below).
3. *Run it on a device, not on the host.* A verdict about runtime behaviour
   needs evidence from the target: a VM from `generic-x64-vm`, or hardware.
   Host-side reasoning about a device-side behaviour is a lead, never
   evidence.
4. *An assertion that cannot fail is not evidence.* Before recording a PASS,
   ask what result would have produced a FAIL.
5. *Subagent output is a LEAD, never EVIDENCE.* Every fact that supports a
   verdict is re-read from the primary artifact before the verdict is
   written. Fan-out inside this lane is read-only research subagents only
   (D-WORKFLOW-183).

**What runs on the VM, and how.** Can this be done on the VM? **Yes**, for
every behaviour claim about a script the GENERIC_X64 guest runs: the image
runs the same busybox, dash, bash, python, systemd units, EmulationStation
binary and 640x480 panel as a handheld (`vm-first.md`). **Where the guest
cannot show it**, the claim is a lead, written as such: the guest has no
backlight, LED, panel-rotation or suspend hardware (`brightness`,
`paneladj`, `led_flash`, `rocknix-fake-suspend`, `suspendmode`), no HDMI
hotplug path (`handle-hdmi-hotplug`, H700 only), no `099-freqfunctions`
(aarch64 only) and no internal storage for `installtointernal` to install
to; a Q3 finding there is a `bug` issue only when a trace at `file:line`
proves it, otherwise it is an *open item to test* or a *keep an eye on*
(D-QA-051), never a device run in this slice. Nothing in this slice touches
a handheld, a person's cloud, or a QA guest another lane owns.

- **The image.** Do not build one (D-WORKFLOW-183: lanes deliver branches;
  nothing in M6 builds). Use the newest GENERIC_X64 image on the host, which
  the M7 lane built on 2026-10-23 at
  `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`
  (2,122,289,964 bytes; source `069fc2704421`; its BUILD_ID is read from
  the guest's `/etc/os-release` and recorded in `00-running-log.md`). Copy
  the `.img.gz` into this lane's own artifacts directory first (a fresh
  `ROCKNIX_ARTIFACTS=/workspace/artifacts/m6-t1-<date>`); never write in the
  M7 worktree. Then `generic-x64-vm-testing.md` § Headless: `gunzip`,
  `qemu-img convert` to qcow2, `qemu-img resize ... 16G` (not optional),
  `generic-x64-vm run --headless --daemonize` **with the lane's own instance
  paths and ports**: `--pidfile $ROCKNIX_ARTIFACTS/qemu.pid --serial
  $ROCKNIX_ARTIFACTS/serial.sock --monitor $ROCKNIX_ARTIFACTS/monitor.sock`,
  a VNC display other than the default 9 (`--vnc`) and an SSH forward other
  than 10022 (`--ssh-port`, see the tool's `--help`) if any other guest is
  up on this host (`pgrep -f qemu-system-x86_64 | wc -l` before starting;
  the defaults `/tmp/rocknix-qemu.pid`, `/tmp/rocknix-qemu-serial.sock`,
  `/tmp/rocknix-qemu-monitor.sock` and 10022 are shared with every other
  lane's guest). `tools/vm-serial --socket $ROCKNIX_ARTIFACTS/serial.sock
  wait`, then a root shell through `tools/vm-serial --socket ... sh`.
  Provision an SSH key over serial as § Headless shows (the key lives under
  `$ROCKNIX_ARTIFACTS`, never in the tree). Stop the guest by its pidfile,
  never by pattern (§ Spin a guest down). Every VM cycle writes its row in
  `docs/vm-qa-log.md` (§ After every VM cycle; the row names the image, the
  guest's shape, what ran and what it did not prove).
- **The image is not the tree.** The image carries M7's `runemu.sh` and
  `package.mk` (§ 2, known incoming drift); every other *script* of this
  slice is byte-identical to `next`'s, while the configuration files carry
  the recipe's build-time edits (`system.cfg`: the device name,
  `DEVELOPMENT_DEFAULTS` on; `/etc/motd` with the issue banner) and the
  arch-exclusive fragment is absent. So, before a proof exercises a script,
  compare the installed copy with the tree's at the read hash
  (`tools/vm-serial --socket ... sh 'cat /usr/bin/<script>' | diff -
  <tree copy>`, or `diff` against the build root's `image/system/usr/bin/`
  on the host). Identical: the proof stands for the tree, say so.
  Different (`runemu.sh`): the proof is of the image's copy and says so; a
  proof of the tree's copy places it on the guest under `/storage` and runs
  it directly (`/usr` is read-only squashfs), which proves the script and
  not its callers, and the record says which.
- **Stage A's two tool trials.** Run `tools/time-to-play` and
  `tools/emulator-exit-test` once each against this single guest, before
  the Q5 measurements, and record in `00-running-log.md` that they work
  without `tools/vm-pair`: both default to port 10022 and take `--port` and
  `--identity`; `time-to-play` also requires `--monitor <the guest's monitor
  socket>` and `--out <a directory under $ROCKNIX_ARTIFACTS>`, takes `--vm`
  (RetroArch to the gl driver for the run; the guest has no Vulkan) and
  `--no-configure-remote` (it would otherwise set up a QA cloud remote
  through `tools/cloud-test-backend`, a shared backend this slice has no
  business in; `generic-x64-vm-testing.md` § One writer per QA cloud
  folder); `emulator-exit-test --vm` builds its own cartridge.
- **The mechanical checks that exist for these scripts**, each run and its
  command, exit status and summary line recorded in `02-forward-audit.md`;
  a check that cannot run is recorded as such, never as a pass. With
  `QA_SYSTEM_ROOT=/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system`
  (the newest GENERIC_X64 build root, read-only; its `usr/bin/busybox`
  exists; built from `069fc2704421`, whose 12 commits do not touch busybox's
  recipe, checked 2026-10-23):
  - `tools/pkgcheck rocknix` (the recipe);
  - `QA_SYSTEM_ROOT=... tools/last-good-scripts-test` (`chksysconfig`,
    `set_setting`, `write_stamp`, the FORBIDDEN strings, under the image's
    busybox; **without the variable the tool's own search cannot reach
    `/workspace/repos/rocknix.worktrees` and it falls back to the host's
    busybox**, blindspot 34's false pass, so the variable is not optional);
  - `tools/settings-modes-test --profile projects/ROCKNIX/packages/rocknix/profile.d/001-functions
    --chksysconfig projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig
    --busybox $QA_SYSTEM_ROOT/usr/bin/busybox --output <scratch>/settings-modes.json`
    (#421: the shell settings writers and the recovery writers preserve
    private modes under the image's applets);
  - `tools/wait-lock-test` (the settings lock's patience);
  - `tools/emulator-exit-test --port <ssh> --identity <key> --vm` (the exit
    hotkey through `runemu.sh` on the guest; § Fixtures for the launch path);
  - `tools/time-to-play --port <ssh> --identity <key> --monitor <socket>
    --out <dir> --no-configure-remote --vm` (the two numbers);
  - `tools/usb-gadget-test --output <scratch>/usb-gadget.json` (#531:
    `usbgadget`'s configfs preparation in a fixture);
  - `tools/rocknix-info-test` (the full script with fixture sysfs; see its
    `--help` for its arguments);
  - `tools/melonds-upgrade-test --post-update projects/ROCKNIX/packages/rocknix/sources/post-update
    --busybox $QA_SYSTEM_ROOT/usr/bin/busybox --output <scratch>/melonds.json`
    (#526: `post-update`'s melonDS half);
  - `tools/vocabulary-check` (the strings);
  - `tools/vm-upgrade-rehearsal <previous img.gz> <new tar> <new BUILD_ID prefix>`
    (`post-update` end to end): both inputs exist on the host without a
    build, the previous image
    `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-06/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T145625Z.g6e3a2165d415-from-ROCKNIX.img.gz`
    and the new tar beside the image above
    (`...20261022T235948Z.g069fc2704421-from-ROCKNIX.tar`); copy both under
    `$ROCKNIX_ARTIFACTS` first; it boots its own guest, so give it its own
    instance paths too, and record its summary line;
  - of `tools/vm-qa`'s suites, only `scripts` (which is
    `last-good-scripts-test` on the host) and `exit` (`emulator-exit-test`)
    cover this slice; `lifetime`, `quoting`, `register`, `french` and
    `menumap` are EmulationStation-source and ledger checks on the host and
    are not this slice's. Run the two directly, as above, rather than
    through the runner, which wants the pair up.
- **A read is free and goes through the filter.** Every line read back from
  the guest, from an image's config, from `rclone.conf`, `system.cfg`,
  `iwd/*.psk` or `get_setting`, passes `grep -v -i -E
  'key|pass|token|user|psk'`, or is masked with `sed -E
  's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'` where the line's
  presence is the evidence (D-QA-021; `engineering-practices.md` § Nothing
  runs on a person's device). The build-time `.psk` the recipe writes and
  the `LOCAL_SSH_KEYS_FILE` path are read that way too.

**What never runs in this slice:** a build of an image or a package; a
command on a handheld, a person's cloud, a shared QA cloud backend, or a QA
guest this lane did not start; an edit to any tool while a run of it is in
flight; `pkill -f` or `kill` by pattern; bare `git stash`; `git worktree
remove --force` or `rm -rf` of any worktree (`tools/fork-worktree remove`);
a model call outside `tools/council/run`; a credential or the wordlist
printed; a merge of another lane's feature branch to refresh rules (read
them from `next`); a write under `/workspace/repos/rocknix` or any
`rocknix.worktrees/*`, or in the P0 or P1 worktrees; an edit to
`.github/sessions/saved-session-state-next.md` (the M7 lane's);
`--no-verify` on any push; a change to `docs/reviews/order.md`,
`slices.json`, `areas.json`, the plan, the brief, #648's criteria or the M6
body (the coordinator's, D-WORKFLOW-189); a GitHub issue other than the
audit punch-list issue and `bug` issues (§ 1).

## 6. Outputs

All under this worktree, committed on the branch with messages that cite
`#648` (`Refs #648` while any criterion is open, never a closing keyword);
the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-os-launch-control-state/00-running-log.md` | the skill's append-only flight recorder, opened first: the model and effort that ran, `reviewed-at` (the branch `HEAD`) with `8ebaf8daad` beside it, the `upstream/next` hash the first commands fetched, the image's BUILD_ID, the guest's instance paths, the two tool trials' outcome, the `tsx` version, every checkpoint | A |
| Research notes | `.../01-research-notes.md` | § Scope: the 83 paths re-derived with the commands of § 2 and their deltas; the three groups; the interacting subsystems; the incoming M7 delta listed hunk by hunk; the RetroArch-half line drawn from #336; `shellcheck: run` (with the binary's hash) or `: not run`; the rules read, by name (`working-principles.md` § Pre-flight) | A |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #648's checklist, plus a **coverage table with one row per path** (83 rows; the first cell the path in backticks, so `grep -c '^| \`projects/ROCKNIX/packages/rocknix/' 02-forward-audit.md` prints 83; then group, tier, Q1 to Q7 each answered or `n/a` with the reason); the mechanical checks of § 5 with command, exit status and summary line; the proofs on the guest, each saying whether it proved the image's copy or the tree's | B |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5's interaction audit for the seams § 2 names (launch path x interface; settings writers x the lock; `post-update` x `/storage`; `automount` x the cloud scripts' saves root) | B |
| Analysis | `.../04-analysis.md` | Phase 4, then § Finding Verification (4.5), then **§ Renovation face** with one subsection per question Q1 to Q7 (the lint requires all seven), Q6 carrying the reachability table and Q5 the measurements beside the baseline with the guest's loglevel, then § Second opinion (4.6: the two seats, or one seat and the Argon seat's pending line, each with command, provenance path, served model, the grading table and the net-effect line) | B, C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (written before the first call), `<member>-brief.md`, the outputs, each call's `provenance.json`; the probe of each seat | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | prints `PASS pre-issue artifacts (does not certify resolution)`; recorded in the running log | C to D |
| Punch list | `.../05-punch-list.md` | Phase 5, every item with `question: Q1..Q7` (or `none` with a reason), severity, category (`Renovation` where it is not a defect), where, acceptance; the YAML `punch_index` (`templates.md`); RetroArch-half items marked for `deferred:#336` | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #648 | `Audit: M6 T1 the OS scripts: launch, control and state -- N findings (X critical, Y high)`; one checkbox per item, each agent-verifiable (D-QA-044); `tools/box-check --issue N` run on it and its line recorded | D |
| Bug issues | GitHub, label `bug`, milestone-less unless the coordinator places them | one per defect (D-WORKFLOW-187, D-QA-051): the code trace shape (`release-candidates.md` step 0), the `Can this be done on the VM?` line, the VM artifact that closes it; `tools/box-check --issue N` on each | D |
| **The stage-D pause** | #648 | the punch list posted on #648 with the audit issue's number and the `bug` issues' numbers; **the lane waits** while the coordinator writes one remediation brief per stream of related items (plan § 6b stage E: the D-WORKFLOW-056 shape, the files owned, the test first, the `Already written:` line, the commit shape). The coordinator's brief names the branch each stream lands on; the default is this branch, one commit series per stream, headed by the stream's name | D to E |
| Remediation | the branch the stream briefs name | each stream as its brief specifies; a `bug` issue's fix carries its `Already written:` line; a player-visible change updates the running change log the rule names (`change-log.md`) the same day; never a build | E |
| Verification | `02-forward-audit.md` appended; `.../audit-completion.json` | every behaviour claim proven on the guest (§ 5), the VM cycle's row in `docs/vm-qa-log.md`; Phase 7 outcomes re-derived from commands (each outcome names the command or the diff that shows it: a resolved item its commit and the check that passes, a deferred item its issue, a withdrawn item the artifact that refutes it); `tools/lint-audit-artifacts <folder>` prints `PASS` before H | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-os-launch-control-state.md`, and the same text as a comment on #648 | the mini-retro skill's four answers with its scoped audit, in Instruction-Recommendations mode (plan § 6b G: the scope is epic tier); findings that recur become a rule edit, a tool, a blindspot entry with its guard, or a work-log entry (`learning-capture.md`); what the slice did to time to play (`time-to-play.md`) | G |
| Hand-back | #648 | `reviewed-at:` (the branch `HEAD` at stage A) and `fixed-at:` (the branch's tip when the fixes are complete) written into #648's body by the executor, no `fixed-at-es:` (no ES path here); one comment naming the branch tip and each artifact above by path; then the lane says it is idle. **The coordinator** accepts (§ 10), closes #648, writes `reviewed_at` and `fixed_at` into `slices.json`, and after this branch merges to `next` regenerates the inventory, `tools/renovation-status --write docs/reviews/status.md` and `tools/renovation-drift --write docs/reviews/drift.md` (a drift diff `fixed-at..next` means something only once `fixed-at` is an ancestor of `next`) and moves the M6 body (D-WORKFLOW-189) | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-os-launch-control-state-648.md` | seeded by the coordinator; the executor updates it at every checkpoint: start here, current focus, the stage reached, next commands, merge notes | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session, headed `#648` and the thing decided or learned | every session |

Neither `tools/renovation-status` nor `tools/renovation-drift` nor
`tools/renovation-inventory` is run to write ledgers or edited here; a
defect in one is a lead on #648 (they are P1's tools, documented in
`docs/reviews/README.md`).

## 7. Acceptance

The checklist on #648 is the contract. Its first five items are plan § 6b's
contract for every slice; the rest are this slice's, written by the
coordinator with this brief (D-WORKFLOW-189). Each names the artifact that
ticks it; the coordinator ticks them at hand-back from the artifacts, not
from this lane's word.

- [ ] `docs/audits/<date>-epic-m6-os-launch-control-state/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-os-launch-control-state/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included: Q1 to Q7 answered in `04-analysis.md`, and every punch item's `question:` in the index.
- [ ] `second-opinions/review-plan.json` records Extended depth and two reviewers from two other labs, and each reviewer's provenance names its served model (plan § 6c, D-WORKFLOW-137).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue, or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` on #648 carry the lane's commits the read and the fixes were made at (the read commit's slice bytes equal to `next`'s `8ebaf8daad`; no EmulationStation path here, so no `fixed-at-es:`), and, after the coordinator closes #648 and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed` (the coordinator's regeneration).
- [ ] `01-research-notes.md` § Scope records the read hash `8ebaf8daad` for the slice's paths, the three counting commands of brief § 2 with their output (83 paths, 13,327 lines, 29 fork-own, 54 upstream-carried, or the deltas beside them), the image's BUILD_ID, and the M7 delta (`next..069fc2704421` on the package) listed hunk by hunk.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: `grep -c '^| \`projects/ROCKNIX/packages/rocknix/' 02-forward-audit.md` prints 83; each row's Q1 to Q7 cells answered or `n/a` with a reason.
- [ ] `02-forward-audit.md` records, with command, exit status and summary line, each of: `tools/pkgcheck rocknix`, `tools/last-good-scripts-test` (under `QA_SYSTEM_ROOT`), `tools/settings-modes-test`, `tools/wait-lock-test`, `tools/emulator-exit-test --vm`, `tools/time-to-play --vm`, `tools/usb-gadget-test`, `tools/rocknix-info-test`, `tools/melonds-upgrade-test`, `tools/vocabulary-check`; a check that could not run is recorded with the reason, never as a pass.
- [ ] `04-analysis.md` § Renovation face Q5 carries the two time-to-play numbers measured on the guest beside #336's baseline (1.05 s and 2.03 s), and a timed run of `setsettings.sh` in the guest with the arguments a launch passes.
- [ ] `04-analysis.md` § Renovation face Q6 carries one reachability row per script in `sources/scripts/` (the search command and its output); every row marked unreached by any caller carries an `Already written:` line and what the unit exposed.
- [ ] `04-analysis.md` § Renovation face Q4 lists every commit of `c445081a59..upstream/next` touching the package (43 on 2026-10-23) with a disposition each (merged / not applicable / to merge, with the reason).
- [ ] Every proof on the guest in `02-forward-audit.md` says whether it proved the image's copy or the tree's copy of the script, after a recorded diff of the two.
- [ ] Every defect on the punch list has a `bug` issue carrying the `Can this be done on the VM?` line and a VM-verifiable criterion; every proposed removal carries `Already written:`; `tools/box-check --issue N` passes on the audit issue and on each `bug` issue this lane files.
- [ ] The retro exists at `docs/retros/<date>-m6-os-launch-control-state.md`, is posted on #648, and answers what the slice did to the two time-to-play numbers.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge; the five exit codes pasted on #648.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back, § 10); **the stage-D pause** (the punch list and the
audit issue posted on #648; the lane waits for the coordinator's stream
briefs and does no remediation before them, D-WORKFLOW-189; #648's body
says the same above its checklist); **the Phase 4.6 blocker** (the Argon
route absent from this tree when the second opinions are due: the Astra
pass done, the seat recorded pending, the blocker named on #648, no Phase
5; § 1); an explicit maintainer pause on #648; any other blocker, named on
#648 with what is needed (a count that cannot be produced or two commands
that disagree; a rule that forbids a step; a guest that will not boot after
the recipes of `generic-x64-vm-testing.md` § Debug order; the npm install
failing); **a hash mismatch at stage A** (the branch's bytes under the
package not `8ebaf8daad`'s: the coordinator re-baselines); or an execution
limit, stated as such with the running log current. A checkpoint is not a
stop (D-WORKFLOW-149): write it and take the next stage. A reviewer seat
failing identity verification is a recorded pending line and, at Extended
depth, the same 4.6 blocker. A differing count is a delta, not a stop.
`next` moving under the slice is drift, not a stop. An idle session says it
is idle on #648.

## 9. Ceremonies owed

- A work-log entry per session, headed by `#648`; `tools/work-log-index
  --write` after it; the weekly summary if the lane's week falls due
  (`ceremonies.md`; the W42 summary is the M7 lane's and is not this
  lane's to write).
- A friction line in `docs/friction-log.md` the moment something slows,
  with `issue: #648` or the guard.
- The VM question written before every proof (§ 5 answers it for the slice,
  and names the scripts the guest cannot show; a proof that needs something
  else the guest lacks writes its own line in `02-forward-audit.md`); a row
  in `docs/vm-qa-log.md` per VM cycle.
- The mini-retro skill at stage G, posted on #648, with its scoped audit, in
  Instruction-Recommendations mode.
- A register row the same session for any decision the slice forces (a fork
  resolved, an assumption invalidated). The ID: one above the highest
  `D-WORKFLOW` on every pushed branch (`git grep -ho 'D-WORKFLOW-[0-9]*'
  $(git branch -r --format='%(refname)') -- docs/decision-register.md | sort
  -t- -k3 -n | tail -1`) and in the M7 lane's worktree
  (`/workspace/repos/rocknix.worktrees/m7-player-setup/docs/decision-register.md`);
  on 2026-10-23 the highest is D-WORKFLOW-189 (the M7 lane holds 171 to 180
  unmerged). A row goes at the end of the `## Decided` table, never after
  `## Open decisions` (`tools/register-check` refuses it there, #646).
- `tools/ceremony-check` before every push; what it reports as owed by this
  lane is paid first; what another lane owes is noted on #648. Never
  `--no-verify`. A merge with conflicts is checked for leftover markers
  before it is committed (#696).
- Commit messages in the fork's style (`docs: ...`, `rocknix: ...`), `Refs
  #648` while any criterion is open; a `bug` fix also `Refs` its bug.
- `change-log.md`'s running log the day a player-visible change lands
  (stage E).

## 10. Hand-back

The coordinator accepts the slice by reading, in this order, without
re-reviewing it: #648's checkboxes against their artifacts (§ 7); the lint's
`PASS` line on the audit folder; `second-opinions/` (two provenance files
naming two served models from two labs); the audit issue's checkboxes all
at an outcome; the coverage table's row count; `02-forward-audit.md`'s
mechanical-check lines and the image-or-tree note on each guest proof; the
retro's four answers; the five checker exit codes on #648. The lane posts
one hand-back comment on #648 naming the branch tip and each of those
artifacts by path, writes `reviewed-at:` and `fixed-at:` into #648's body,
then says it is idle. After acceptance the coordinator closes #648, writes
the two hashes into `slices.json`, merges the branch in its turn, and
regenerates the ledgers (§ 6, Hand-back row). A brief that needed the
coordinator's help mid-slice, beyond the stage-D pause and the Phase 4.6
blocker this brief already names, is a defect in this brief: log the
friction, and the coordinator fixes the template in plan § 7 before the
next brief.

**The stranger's proof** (plan § 3, principle 3), run 2026-10-23 on
`86d3a49f6c` by a reader with no context given this tree and version 1 of
this brief: 25 claims verified by command; 7 wrong (the rules diff, the
pointer not yet seeded, `userconfig-setup` as `post-update`'s caller, the
autostart install path, the Argon member name, the `rc-device-fixes` root,
an unreproducible bug count); 19 questions it would have had to ask; 22
statements wrong or unverifiable; 12 disagreements between the brief, the
plan, #648 and the pointer; 10 criteria it could not satisfy mechanically.
Version 2 answers each in the text: the first commands, § 2's hash and
counts and groups, § 3's D-SYS-006, § 4's dash and RetroArch rule, § 5's
image-versus-tree, hardware-bound scripts, tool arguments, `QA_SYSTEM_ROOT`
and instance paths, § 6's lint phases, pause, hand-back and ledgers, § 7's
row-count command and criterion 5, § 8's 4.6 blocker; the plan's § 6b
stages E and H, § 7 item 5 and § 9 were brought in line in the same commit,
and #648's criteria edited. The reading of § 3 alone fills the first hour,
which the brief now says.
