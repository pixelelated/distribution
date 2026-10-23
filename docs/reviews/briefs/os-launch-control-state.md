# Brief: M6.P2 T1, the OS scripts: launch, control and state (#648)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #648 differ, #648 wins and the
coordinator corrects the brief in the same session. Version 1 (2026-10-23),
the first slice brief of the renovation; its stranger's proof is recorded at
the end of § 10.

## 1. Identity

- **Issue:** #648 `M6.P2 E339/T1: os-scripts-and-launch: the OS scripts:
  launch, control and state (Tier 1)`, slice `os-launch-control-state` in
  `docs/reviews/slices.json`, first in `docs/reviews/order.md` (the order's
  row is D-WORKFLOW-188). **Epic:** #339 until the area epic for
  `os-scripts-and-launch` is filed at this dispatch; the coordinator then
  re-parents #648 under it, retitles it `M6.P2 E<epic>/T1: ...` and writes
  the number here. **Milestone:** M6 (`M6: Codebase renovation`); its body
  holds the live order; read it first. **Predecessors:** #346 (the plan),
  #641 (the survey, the inventory and the order; closed 2026-10-23).
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, re-order anything, change a criterion, write a
  brief, move the M6 body or decide a question of scope: those are the
  coordinator's, reached through #648. What this lane does file: its own
  audit punch-list issue (stage D, the code-auditor skill's Phase 6) and a
  `bug` issue for every defect it finds (D-WORKFLOW-187: a defect found by
  the renovation is a bug like any other; `bugs-are-agent-first.md` gives the
  shape, with its VM-verifiable criterion). Nothing else.
- **Branch and worktree:** `feature/m6-os-launch-control-state-648` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-os-launch-control-state-648`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`**, which carries the P0 branch: `next` is gated until the M7
  lane's candidate merges (never `--no-verify`), and the merge order after it
  is P0, P1, then this branch (D-WORKFLOW-182, plan § 8). Plan § 7 names the
  shape `feature/m6-<slice>` and `<slice>`; the lanes append the issue
  number, as the two renovation lanes before this one do. The rules in this
  worktree are `next`'s (P0 and P1 touched none); check it with the first
  commands. The primary checkout is `/workspace/repos/pixelelated/distribution`
  on `next` (D-INFRA-025). **`worktrees.md`, `device-builds.md`, `CLAUDE.md`
  and `AGENTS.md` still name the legacy layout (`/workspace/repos/rocknix`,
  `rocknix.worktrees/`); #640 owns that drift, and this brief's paths are the
  ones to use.** The legacy checkout and every worktree beside it are the M7
  lane's: read from them (an image, a build root, a diff), never write.
- **Model and effort:** Opus 5.5 at high effort (the maintainer, 2026-10-22:
  *"the work will be Opus 5.5"*), unless #648 says otherwise at dispatch.
  Record what actually ran in `00-running-log.md`'s header.
- **Review depth: Extended** (plan § 6c; `slices.json`: launch path and
  state preservation). The primary auditor is this lane (Anthropic). The two
  reviewers come from two other labs, each through the Facilitator and
  nothing else (D-WORKFLOW-049, D-WORKFLOW-137; `adversarial-council.md`
  rule 4; the code-auditor skill's Phase 4.6):
  - **GPT-6 Astra**: `tools/council/run invoke --member gpt --provider
    openrouter --prompt-file <brief> --output <file>` at `max`, the installed
    recipe (`openai/gpt-6-astra`, provider pinned to OpenAI).
  - **Gemini 4 Argon** (Google), the third lab D-WORKFLOW-180 verified on
    #638/#639. **Its route is not yet in this tree:** it lives in the M7
    lane's unmerged `feature/m7-audit-integration-603` (commits
    `1c7d283ad5`, `a7a3bdda4e`; `git -C /workspace/repos/rocknix branch
    --contains 1c7d283ad5`) and reaches `next` with the M7 candidate. At
    Phase 4.6, `grep -il argon scripts/council-invoke.ts` says whether it has
    arrived. If it has, invoke it with the recipe that commit documents
    (`--member gemini`, the Argon route, effort `high`). If it has not, do
    **not** substitute the roster's `google/gemini-3.8-flash` and do not call
    any model another way: record the seat as pending in
    `04-analysis.md` § Second opinion, run the Astra call, and ask the
    coordinator on #648 (the coordinator decides between waiting for the
    merge and another recipe). A seat that fails identity verification is
    recorded, never replaced.
  - Both reviewers run the **refutation pass alone** (the audit is epic tier;
    phases.md § Phase 4.6: two calls at Milestone tier, one otherwise), each
    prepared independently. `second-opinions/review-plan.json` is written
    before the first call (`templates.md` § Second opinion: depth
    `extended`, primary `anthropic/claude-opus-5-5`, lab `anthropic`,
    identity source this brief and the session's own metadata, two
    reviewers). Every seat item is a lead; the orchestrator re-reads the
    artifact before a row is written.
  - The runner's dependencies are not in a fresh worktree: `tools/council/run`
    execs `tools/council/node_modules/.bin/tsx`, and `node_modules/` is
    gitignored. Install once, before Phase 4.6, with `npm install --prefix
    tools/council` (a gitignored write; the npm registry; record the `tsx`
    version in `00-running-log.md`). The key is sourced from
    `~/.config/council/env`; it is never printed, never on a command line.
    The dispatch of this slice on #648 is the authorization for exactly
    these two external calls (plus a probe of each seat first, its
    provenance naming the served model).

First commands:

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-os-launch-control-state-648
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-os-launch-control-state-648
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
git diff --quiet next -- .claude CLAUDE.md AGENTS.md || echo STALE          # must print nothing
git diff --quiet next HEAD -- projects/ROCKNIX/packages/rocknix/ && echo "slice paths equal next's"   # must print
test -f docs/reviews/briefs/os-launch-control-state.md || { echo "the brief is not in this tree: stop"; exit 1; }
cat .github/sessions/saved-session-state-feature-m6-os-launch-control-state-648.md   # the lane's seeded pointer
```

## 2. Scope

**One package, read line by line, less one script.** Every tracked path
under `projects/ROCKNIX/packages/rocknix/` except
`sources/scripts/backuptool`, which the area map places in
`cloud-sync-and-saves` and T17 (`cloud-setup-content`) reads with the
settings archives. The exact membership is the inventory's: the rows whose
`area` is `os-scripts-and-launch` and whose path starts with the package.

**The hash.** The slice is read at `next` as this branch carries it:
`8ebaf8daad` for these paths (the branch tip `2174265e9c` carries the same
bytes under the package; the first commands prove it). Record both hashes in
`00-running-log.md` and `01-research-notes.md` § Scope before reading a
line. A hash that is not `8ebaf8daad` under these paths is a stop (§ 8): the
tree moved under the slice, and the coordinator re-baselines it.

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
      "fork-own", sum(1 for r in t1 if r["tier"] == "fork-own"),
      "upstream-carried", sum(1 for r in t1 if r["tier"] == "upstream-carried"))   # 83, 13327, 29, 54
for r in sorted(t1, key=lambda r: -(r["lines"] or 0)): print(r["lines"], r["tier"], r["language"], r["path"])
PY
git diff --numstat "$(git hash-object -t tree /dev/null)" 8ebaf8daad -- projects/ROCKNIX/packages/rocknix/ \
  | grep -v -F 'sources/scripts/backuptool' | awk '{s+=$1} END {print s}'                              # 13327
```

Recorded: **83 paths, 13,327 lines, of which 11,560 are read line by line**
(code languages, reached by a shipped plan: shell, python, the recipe, the
systemd units, the udev rule; `config/system/configs/tz`, `system.cfg`,
`motd` and the `none`-language profile fragments are read too, as
configuration) **and 7,441 are fork-own**; tiers fork-own 29,
upstream-carried 54; every path `reach: shipped` (in the H700 and SM8550
plans, D-WORKFLOW-185). Twenty-two closed `bug` issues name these scripts
(`gh issue list --repo pixelelated/distribution --label bug --state closed
--limit 500 --json number,title,body`, grepped for the script names); that
history is Phase 1's.

**Where the files land on the image** (`package.mk`): every file of
`sources/scripts/` to `/usr/bin/` at mode 0755; `sources/post-update` to
`/usr/share/post-update`; `config/*` to `/usr/config/` (with `/system` a
symlink to `/storage/.config/system`, so `system.cfg`'s live copy is the
player's); `profile.d/*` to `/etc/profile.d/` (every shell, interactive or
not, that sources `/etc/profile`; `get_setting`, `set_setting` and
`redact_credentials` are functions from `001-functions`, not files);
`autostart/*` to `/usr/lib/autostart/`, run in order by
`projects/ROCKNIX/packages/sysutils/autostart` (`rocknix-autostart.service`,
T22's); `system.d/*` to `/usr/lib/systemd/system/`, five enabled by the
recipe (`rocknix-autostart`, `rocknix-memory-manager`, `save-sysconfig`,
`rocknix-evidence.timer`, `rocknix-sysconfig`), `hdmi-hotplug.path` on H700
only; the two `freqfunctions` fragments are arch-exclusive. `/usr` is a
read-only squashfs on the device, which § 5 cares about.

**Three groups, read in this order** (the slice's reason to be first is the
launch path, plan § 6a; `slices.json`'s `why`):

1. **The launch path** (on the order's launch-path list): `runemu.sh` (626
   lines: configures and starts the emulator; #336 replaces its RetroArch
   half), `setsettings.sh` (1,479: the per-core RetroArch settings written at
   every launch), `run` (61), `setemu.sh`, `bezels.sh` and
   `rocknix-es-thebezelproject` (bezels at launch), `profile.d/001-functions`
   (707: `get_setting`/`set_setting` under the settings lock, D-INFRA-012,
   D-SYS-011/012; `redact_credentials`, D-INFRA-011), `rocknix-systems`
   (python: the systems list), the `profile.d` frequency, GPU and controller
   fragments the launch reads.
2. **State** (on the order's state-preservation list): `chksysconfig` (342:
   `verify` at sysinit from `rocknix-sysconfig.service`, `backup` at
   shutdown from `save-sysconfig.service`; D-CLOUD-078/079/080/082),
   `post-update` (251: runs once after an update from
   `sysutils/systemd/scripts/userconfig-setup` and `autostart/003-upgrade`;
   D-SYS-007; `upgrade-and-install.md` whole), `factoryreset`,
   `installtointernal`, `automount` (D-CLOUD-056/057 and
   `rocknix-automount.service`), `config/system/configs/system.cfg` (the
   defaults the recipe edits per device and per `DEVELOPMENT_DEFAULTS`),
   `autostart/001-setup`, `003-upgrade`, `007-rootpw` with `setrootpass`.
3. **Control and services**: `rocknix-memory-manager` (+ its unit),
   `rocknix-evidence` (+ service and timer; D-SYS-005, D-INFRA-014;
   `handheld-evidence.md`), `rocknix-corekeep`, `usbgadget` (+ the udev rule
   and `autostart/081-usbgadget`; #531), `wifictl` (D-WORKFLOW-040; #159,
   #201), `rocknix-bluetooth` and `rocknix-bluetooth-agent` (python, with
   `bluetooth-agent.service`), `rocknix-fake-suspend`, `suspendmode`,
   `brightness`, `volume`, `paneladj`, `led_flash`, `handle-hdmi-hotplug`
   (+ path and service), `rocknix-report-stats` (+ service and the two timer
   entries), `rocknix-config`, `rocknix-settings`, `rocknix-info`,
   `rocknix-update` (the manual-updates stub; #694 wants online updates),
   `rocknix-keyboard`, `rocknix-scraper`, `rocknix-retroachievements-info`,
   `updateabl`, `migrate_roms`, `show_changelog`, `vertical-check`,
   `getshaders`, `getoverlays`, `getfilters`, `amionline`, `say`,
   `timeinfo`, `error.sh`, `find.sh`, `controller-layout`, the remaining
   `autostart` fragments (006, 008, 009, 010, 050, 055, 080, 099),
   `config/system/configs/tz`, `motd`, `rocknix.target`, and `package.mk`
   itself (the recipe: `tools/pkgcheck`, late binding, the `LOCAL_WIFI_KEY`
   it writes into a `.psk` at build time, which the credential filter of § 5
   covers when it is read back).

The security list names four of these (`setrootpass`, `wifictl`,
`usbgadget`, `rocknix-evidence`), the state list six (`chksysconfig`,
`factoryreset`, `installtointernal`, `automount`, `post-update`,
`setsettings.sh`), the launch-path list three (`runemu.sh`,
`setsettings.sh`, `run`); `order.md` § The security, state-preservation and
launch-path files. A finding in one of them is Extended-depth material by
definition.

**Interacting subsystems, read-only context** (never read line by line here,
never changed here; a defect found in one is a lead posted on #648 for its
own slice): the interface's launch path (T2: `FileData::launchGame`,
`ViewController`, `LaunchCommand.h` build `runemu.sh`'s argument line;
`ApiSystem` calls these scripts by name, T21); `es_systems.cfg` and its
generator `projects/ROCKNIX/packages/virtual/emulators` (`mk_es_systems`,
T3); the autostart runner and the systemd units, power and sleep scripts of
`projects/ROCKNIX/packages/sysutils/` (T22; `autostart` runs this package's
fragments, `sleep.sh` reads the quirks, `userconfig-setup` runs
`post-update`); the per-handheld quirks under
`projects/ROCKNIX/packages/hardware/quirks/` (T29); the cloud scripts under
`projects/ROCKNIX/packages/network/rclone/sources/` that `runemu.sh`'s
callers and the exit path reach (T16, T17; `backuptool` with them); the
offline achievements proxy (T19); `system.cfg` and `es_settings.cfg` as the
state these scripts read and write. The EmulationStation checkout for the
callers' side is `/home/max/Development/emulationstation-next` at the pin in
`projects/ROCKNIX/packages/ui/emulationstation/package.mk`
(`16dbac5211eea7e70db7394372033be2be7df829`); read it with `git -C ... grep`
at the pin, never from its current branch and never by checking anything
out there.

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

From `next`, in this order, before any analysis:

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
- `docs/blindspot-register.md` whole, once. The entries that touch these
  paths: **32** (causal order read from wall clocks that jumped mid-boot:
  `automount`), **33** (a sentinel exit code borrowed from the wrapped tool's
  space: the autostart fragments), **34** (a check written for the device,
  proven under the host's tools: `chksysconfig`, `system.cfg`, busybox `tr`),
  **43** (a safety claim in a header comment, never tested:
  `rocknix-evidence`, `setsettings.sh`), **57** (a fix that covered fewer
  sites than its issue named: `wifictl`); and the general ones a reading
  repeats: 7 (host tools are not the device's), 13 (assumed done), 51 (an
  open checkbox is a claim), 64 (read the cause before lengthening a wait).
- Prior audits of these paths under `docs/audits/`, **as provenance only**:
  which paths were audited, when, at what tier; verdicts are sequestered
  until Phase 2.5 and never transcribed into Phase 2. Punch lists that name
  these scripts, with the count of mentions:
  `2026_09_25-milestone-rc-round-since-258` (28),
  `2026_09_24-milestone-rc-round-since-186` (17),
  `2026_09_28-milestone-audit-of-the-fix-round` (8),
  `2026_09_14-epic-offline-retroachievements` (4),
  `2026_09_28-milestone-audit-of-the-fixes-307` (3),
  `2026_10_14-milestone-m7-next-candidate` (2),
  `2026_09_06-issue-device-flashing-runbook` (2),
  `2026_09_29-milestone-audit-of-the-313-fixes` (1),
  `2026_09_12-milestone-cloud-saves-since-60` (1).
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
  D-SYS-006 (persistent logs, the watchdog, ramoops, `rocknix-evidence`),
  D-INFRA-011 and D-INFRA-014 (`redact_credentials`; evidence collections
  serialised by an flock), D-WORKFLOW-040 (`wifictl forget`), D-QA-021 (the
  credential filter on every read). The program: D-WORKFLOW-181, 183, 184,
  185, 186, 187, 188, 189; D-WORKFLOW-137 (depth and the reviewer's lab),
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
stays. Per unit (a script, a unit file, a fragment, the recipe), the
evidence that answers each:

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | Bash idioms the rest of the tree has left (backticks, `[ ]` where `[[ ]]` is meant, `echo` where `printf` is, `cat` into `grep`); hand-rolled parsing of `system.cfg` or `es_settings.cfg` beside `get_setting`; a systemd unit written the old way (no `Type=`, no ordering, no hardening the others carry); the two python scripts' interpreter lines (`rocknix-systems` says `python`, `rocknix-bluetooth-agent` `/usr/bin/python`: what the image installs under those names); the `tz` list's currency against the image's zoneinfo | the replacement named with where the tree already uses it; `git log -S` for when the old form stopped being written |
| Q2 Standards | The rules § 3 names, cited by section; `set -euo pipefail` and quoting where the interpreter allows it (the scripts declare `bash`, `sh` and `python`; the image's `sh` is busybox, § What the guest's busybox lacks); late binding in `package.mk` (`tools/pkgcheck rocknix`); every string a script prints to a screen against `es-player-text.md` (`tools/last-good-scripts-test` case e checks the FORBIDDEN shapes; `tools/vocabulary-check`); upstream headers kept and a fork line added (`CLAUDE.md` § `package.mk` rules). **`shellcheck` is not installed on this host (2026-10-23).** Do not install a system package. A static release binary unpacked under the lane's gitignored scratch with its hash recorded is acceptable; otherwise record `shellcheck: not run` once in `01-research-notes.md` § Scope and answer Q2 by reading against the conventions | the rule and section; `tools/pkgcheck` output; `shellcheck` output where it ran, or the recorded absence |
| Q3 Bugs | Where each unit fails: the unhandled branch, the race, the wrong default, the path that works on the host and not on the device. The hot spots: root at boot and at every launch; the updater path (`post-update`, `003-upgrade`, `userconfig-setup`); the destructive scripts (`factoryreset`, `installtointernal`); `automount`'s card detection and its retries; `chksysconfig`'s verify and backup semantics against a cut file; `setsettings.sh`'s per-core writes and what a kill mid-write leaves; `runemu.sh`'s argument parsing, exit status and logs; the settings lock | a reproduction on the GENERIC_X64 guest or a trace with `file:line`; host reasoning about device behaviour is a lead (§ 5) |
| Q4 Package currency | The package has no upstream tarball (`PKG_VERSION=""`, a meta package), so the question is ROCKNIX's copies of these files: every commit on `upstream/next` since the merge base `c445081a59` that touches the package, dispositioned one by one (merged already / not applicable to this fork / to merge, with the reason); the inventory's `overlap` column names the paths both sides changed. Plus `tz` against the zoneinfo the image builds, and the python interpreter the image provides | `git log --oneline c445081a59..upstream/next -- projects/ROCKNIX/packages/rocknix/` with a disposition per line; the date checked |
| Q5 Efficiency | What the launch path costs: the two time-to-play numbers on the guest at the image § 5 names, beside the baseline #336 records (a game's first frame 1.05 s from the press, the next game's 2.03 s from the exit, on the VM); what `runemu.sh` does per launch, itemised, with `setsettings.sh`'s 1,479 lines timed in the guest (`time bash /usr/bin/setsettings.sh ...` with the arguments a launch passes); what runs every exit; what runs at boot in the autostart order and how long each fragment takes (`systemd-analyze blame` and the journal's timestamps); `rocknix-memory-manager`'s loop and `rocknix-evidence`'s five-minute page in memory on a 1 GiB handheld; the player's steps where a script drives a flow | `tools/time-to-play` output; a measurement in the guest with its command; or the named absence of one |
| Q6 Dead ends | Is each script, unit, fragment and function reached: by a built image (every path here is `reach: shipped`, so the question is callers), by any caller (`grep -rlF '<name>' packages projects scripts tools` in the distribution and `git -C $ES grep -lF '<name>' $PIN` in the interface at the pin, plus the units that `ExecStart` it and the udev rules), by any player path. Candidates the survey saw: `rocknix-update` (a stub that prints manual-update text; #694), `updateabl`, `migrate_roms`, `show_changelog`, `rocknix-report-stats` (its service and the two timer entries), `say`, `find.sh`, `error.sh`, `getshaders`, `getoverlays`, `getfilters`, `controller-layout`, `rocknix-scraper`, `rocknix-keyboard`, `rocknix-retroachievements-info`, `vertical-check`; per-device branches inside the scripts for devices the fork does not ship (a row for the table, not a removal: `unshipped` is not `unreached`, D-WORKFLOW-185); the `100-amd64-freqfunctions` fragment (x86_64 only, by the recipe) | the reachability search as a command and its output, one row per unit in `04-analysis.md` § Renovation face Q6; `engineering-practices.md` § Before deleting a duplicate before any removal; every removal carries `Already written:` (what the retired unit left on devices and in clouds) |
| Q7 Clarity | Can a reader new to it tell what each unit does and why in one pass: `setsettings.sh` at 1,479 lines and `runemu.sh` at 626, one responsibility each or several; `001-functions` at 707 lines sourced into every shell; logic copied between `runemu.sh`, `setsettings.sh` and the interface (the launch command, the per-core defaults); comments that match the code; a header that says where the file came from (JELOS, ROCKNIX, this fork) | the unit named with what a reader stumbles on; a duplicate named with its original |

A finding is one question with its evidence; severity and category are the
code-auditor's, with `Renovation` as the category for Q1, Q5, Q6 and Q7
items that are not defects. A Q3 finding that is a defect is also a `bug`
issue (D-WORKFLOW-187, § 1), filed with the VM artifact that would close it.

## 5. The evidence floor

The code-auditor skill's rules, verbatim from `SKILL.md` § Evidence floor,
apply to every verdict:

1. *Tracker state is never sole evidence.* Issue state, checked AC boxes,
   and retro summaries may corroborate but can never be the ONLY evidence
   for a PASS -- every PASS cites at least one primary artifact (file:line,
   executed command output, or commit diff).
2. *Mechanical evidence outranks reading.* Where a check exists, RUN it and
   record the command, exit status and counts in the criterion entry.
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
every behaviour claim this slice makes: the GENERIC_X64 image runs the same
busybox, scripts, systemd units, EmulationStation binary and 640x480 panel
as a handheld (`vm-first.md`). Nothing in this slice touches a handheld, a
person's cloud, or a QA guest another lane owns.

- **The image.** Do not build one (D-WORKFLOW-183: subagents and lanes
  deliver branches; nothing in M6 builds). Use the newest GENERIC_X64 image
  on the host, which the M7 lane built on 2026-10-23 at
  `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`
  (source `069fc2704421`; its BUILD_ID is read from the guest's
  `/etc/os-release` and recorded in `00-running-log.md`). Copy the `.img.gz`
  into this lane's own artifacts directory first (a fresh
  `ROCKNIX_ARTIFACTS=/workspace/artifacts/m6-t1-<date>`); never write in the
  M7 worktree. Then `generic-x64-vm-testing.md` § Headless: `gunzip`,
  `qemu-img convert` to qcow2, `qemu-img resize ... 16G` (not optional),
  `generic-x64-vm run --headless --daemonize`, `tools/vm-serial wait`, and a
  root shell through `tools/vm-serial sh`. Stop the guest by its pidfile,
  never by pattern (§ Spin a guest down).
- **The image is not the tree.** The image carries M7's `runemu.sh` and
  `package.mk` (§ 2, known incoming drift); every other file of this slice
  is byte-identical to `next`'s. So, before a proof exercises a script,
  compare the installed copy with the tree's at the read hash
  (`tools/vm-serial sh 'cat /usr/bin/<script>' | diff - <tree copy>`, or
  `unsquashfs` of the image's `SYSTEM` on the host). Identical: the proof
  stands for the tree, say so. Different (`runemu.sh`): the proof is of the
  image's copy and says so; a proof of the tree's copy places it on the
  guest under `/storage` and runs it directly (`/usr` is read-only
  squashfs), which proves the script and not its callers, and the record
  says which.
- **The mechanical checks that exist for these scripts**, each run and its
  command, exit status and summary line recorded in `02-forward-audit.md`;
  a check that cannot run is recorded as such, never as a pass:
  `tools/pkgcheck rocknix` (the recipe); `tools/last-good-scripts-test`
  (`chksysconfig`, `set_setting`, `write_stamp`, the FORBIDDEN strings; it
  runs the image's busybox from a GENERIC_X64 build root: read-only use of
  `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64`,
  the newest, or `rc-device-fixes/build.ROCKNIX-GENERIC_X64.x86_64`; name
  which); `tools/settings-modes-test` (#421: the shell settings writers and
  the recovery writers preserve private modes under the image's applets);
  `tools/wait-lock-test` (the settings lock's patience);
  `tools/emulator-exit-test --port <ssh> --identity <key> --vm` (the exit
  hotkey through `runemu.sh` on the guest; § Fixtures for the launch path);
  `tools/time-to-play --port <ssh> --identity <key>` (the two numbers);
  `tools/usb-gadget-test` (#531: `usbgadget`'s configfs preparation in a
  fixture); `tools/rocknix-info-test` (the full script with fixture sysfs);
  `tools/melonds-upgrade-test` (#526: `post-update`'s melonDS half);
  `tools/vocabulary-check` (the strings); the `scripts`, `lifetime`,
  `quoting` and `exit` suites of `tools/vm-qa` where they cover these paths
  (`tools/vm-qa --help` lists them). `tools/vm-upgrade-rehearsal` proves
  `post-update` end to end but needs the previous image and a new `.tar`;
  run it only if both exist on the host without a build, else record why
  not.
- **A read is free and goes through the filter.** Every line read back from
  the guest, from an image's config, from `rclone.conf`, `system.cfg`,
  `iwd/*.psk` or `get_setting`, passes `grep -v -i -E
  'key|pass|token|user|psk'`, or is masked with `sed -E
  's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'` where the line's
  presence is the evidence (D-QA-021; `engineering-practices.md` § Nothing
  runs on a person's device). The build-time `.psk` the recipe writes and
  the `LOCAL_SSH_KEYS_FILE` path are read that way too.

**What never runs in this slice:** a build of an image or a package; a
command on a handheld, a person's cloud, or a QA guest this lane did not
start; an edit to any tool while a run of it is in flight; `pkill -f` or
`kill` by pattern; bare `git stash`; `git worktree remove --force` or `rm
-rf` of any worktree (`tools/fork-worktree remove`); a model call outside
`tools/council/run`; a credential or the wordlist printed; a merge of
another lane's feature branch to refresh rules (read them from `next`); a
write under `/workspace/repos/rocknix` or any `rocknix.worktrees/*`, or in
the P0 or P1 worktrees; an edit to `.github/sessions/saved-session-state-next.md`
(the M7 lane's); `--no-verify` on any push; a change to `docs/reviews/order.md`,
`slices.json`, `areas.json`, the plan, the brief, #648's criteria or the M6
body (the coordinator's, D-WORKFLOW-189); a GitHub issue other than the
audit punch-list issue and `bug` issues (§ 1).

## 6. Outputs

All under this worktree, committed on the branch with messages that cite
`#648` (`Refs #648` while any criterion is open, never a closing keyword);
the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-os-launch-control-state/00-running-log.md` | the skill's append-only flight recorder, opened first: the model and effort that ran, both hashes, the image's BUILD_ID, the `tsx` version, every checkpoint | A |
| Research notes | `.../01-research-notes.md` | § Scope: the 83 paths re-derived with the commands of § 2 and their deltas; the three groups; the interacting subsystems; the incoming M7 delta listed hunk by hunk; `shellcheck: run` or `: not run`; the rules read, by name (`working-principles.md` § Pre-flight) | A |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #648's checklist, plus a **coverage table with one row per unit of the 83 paths** (unit, group, tier, Q1 to Q7 each answered or `n/a` with the reason); the mechanical checks of § 5 with command, exit status and summary line; the proofs on the guest, each saying whether it proved the image's copy or the tree's | B |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5's interaction audit for the seams § 2 names (launch path x interface; settings writers x the lock; `post-update` x `/storage`; `automount` x the cloud scripts' saves root) | B |
| Analysis | `.../04-analysis.md` | Phase 4, then § Finding Verification (4.5), then **§ Renovation face** with one subsection per question Q1 to Q7 (the lint requires all seven), Q6 carrying the reachability table and Q5 the measurements beside the baseline, then § Second opinion (4.6: the two seats, or one seat and the Argon seat's pending line, each with command, provenance path, served model, the grading table and the net-effect line) | B, C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (written before the first call), `<member>-brief.md`, the outputs, each call's `provenance.json`; the probe of each seat | C |
| Punch list | `.../05-punch-list.md` | Phase 5, every item with `question: Q1..Q7` (or `none` with a reason), severity, category (`Renovation` where it is not a defect), where, acceptance; the YAML `punch_index` (`templates.md`) | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #648 | `Audit: M6 T1 the OS scripts: launch, control and state -- N findings (X critical, Y high)`; one checkbox per item, each agent-verifiable (D-QA-044) | D |
| Bug issues | GitHub, label `bug`, milestone-less unless the coordinator places them | one per defect (D-WORKFLOW-187, D-QA-051): the code trace shape (`release-candidates.md` step 0), the `Can this be done on the VM?` line, the VM artifact that closes it | D |
| **Pause for the stream briefs** | #648 | the punch list posted on #648 with the audit issue's number; **the lane waits** while the coordinator writes one remediation brief per stream of related items (plan § 6b stage E is the coordinator's under D-WORKFLOW-189: the D-WORKFLOW-056 shape, the files owned, the test first, the `Already written:` line, the commit shape). The coordinator's brief names the branch each stream lands on; the default is this branch, one commit series per stream, headed by the stream's name | D to E |
| Remediation | the branch(es) the stream briefs name | each stream as its brief specifies; a `bug` issue's fix carries its `Already written:` line; a player-visible change updates `docs/cloud-sync-changelog.md` or the running change log the rule names (`change-log.md`) the same day; never a build | E |
| Verification | `02-forward-audit.md` appended; `.../audit-completion.json` | every behaviour claim proven on the guest (§ 5); Phase 7 outcomes re-derived from commands; `tools/lint-audit-artifacts <folder>` PASS before D and again before H | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-os-launch-control-state.md`, and the same text as a comment on #648 | the mini-retro skill's four answers with its scoped audit; findings that recur become a rule edit, a tool, a blindspot entry with its guard, or a work-log entry (`learning-capture.md`); what the slice did to time to play (`time-to-play.md`) | G |
| Close | #648; `docs/reviews/status.md`; `docs/reviews/drift.md` | `reviewed-at: <hash>` (the read) and `fixed-at: <hash>` (the fixes' tip) written in #648's body by the executor, with `fixed-at-es:` absent (no ES path here); `tools/renovation-status --write docs/reviews/status.md` and `tools/renovation-drift --write docs/reviews/drift.md` run and committed; the hand-back posted (§ 10). The M6 body's current/next and the issue's closure are the coordinator's | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-os-launch-control-state-648.md` | seeded by the coordinator; the executor updates it at every checkpoint: start here, current focus, the stage reached, next commands, merge notes | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session, headed `#648` and the thing decided or learned | every session |

Neither `tools/renovation-status` nor `tools/renovation-drift` is edited
here; a defect in one is a lead on #648 (they are P1's tools, documented in
`docs/reviews/README.md`).

## 7. Acceptance

The checklist on #648 is the contract. Its first five items are plan § 6b's
contract for every slice; the rest are this slice's, written by the
coordinator with this brief (D-WORKFLOW-189). Each names the artifact that
ticks it; the coordinator ticks them at hand-back from the artifacts, not
from this lane's word.

- [ ] `docs/audits/<date>-epic-m6-os-launch-control-state/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-os-launch-control-state/` prints `PASS`, the renovation face included: Q1 to Q7 answered in `04-analysis.md`, and every punch item's `question:` in the index.
- [ ] `second-opinions/review-plan.json` records Extended depth and two reviewers from two other labs, and each reviewer's provenance names its served model (plan § 6c, D-WORKFLOW-137).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue, or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` on #648 carry the commits the read and the fixes were made at, and `tools/renovation-status` lists this slice as `closed`.
- [ ] `01-research-notes.md` § Scope records the read hash `8ebaf8daad` for the slice's paths, the three commands of brief § 2 with their output (83 paths, 13,327 lines, 29 fork-own, 54 upstream-carried, or the deltas beside them), the image's BUILD_ID, and the M7 delta (`next..069fc2704421` on the package) listed hunk by hunk.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per unit of the 83 paths (`grep -c` of its rows equals the path count), each cell Q1 to Q7 answered or `n/a` with a reason.
- [ ] `02-forward-audit.md` records, with command, exit status and summary line, each of: `tools/pkgcheck rocknix`, `tools/last-good-scripts-test`, `tools/settings-modes-test`, `tools/wait-lock-test`, `tools/emulator-exit-test --vm`, `tools/time-to-play`, `tools/usb-gadget-test`, `tools/rocknix-info-test`, `tools/melonds-upgrade-test`, `tools/vocabulary-check`; a check that could not run is recorded with the reason, never as a pass.
- [ ] `04-analysis.md` § Renovation face Q5 carries the two time-to-play numbers measured on the guest beside #336's baseline (1.05 s and 2.03 s), and a timed run of `setsettings.sh` in the guest with the arguments a launch passes.
- [ ] `04-analysis.md` § Renovation face Q6 carries one reachability row per script in `sources/scripts/` (the search command and its output); every row marked unreached by any caller carries an `Already written:` line.
- [ ] `04-analysis.md` § Renovation face Q4 lists every commit of `c445081a59..upstream/next` touching the package with a disposition each (merged / not applicable / to merge, with the reason).
- [ ] Every proof on the guest in `02-forward-audit.md` says whether it proved the image's copy or the tree's copy of the script, after a recorded diff of the two.
- [ ] Every defect on the punch list has a `bug` issue carrying the `Can this be done on the VM?` line and a VM-verifiable criterion; every proposed removal carries `Already written:`.
- [ ] The retro exists at `docs/retros/<date>-m6-os-launch-control-state.md`, is posted on #648, and answers what the slice did to the two time-to-play numbers.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge; the five exit codes pasted on #648.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back, § 10); **the stage-D pause** (the punch list and the
audit issue posted on #648; the lane waits for the coordinator's stream
briefs and does no remediation before them, D-WORKFLOW-189); an explicit
maintainer pause on #648; a blocker, named on #648 with what is needed (the
Argon route absent at Phase 4.6, § 1; a count that cannot be produced or two
commands that disagree; a rule that forbids a step; a guest that will not
boot after the recipes of `generic-x64-vm-testing.md` § Debug order); **a
hash mismatch at stage A** (the slice's paths not at `8ebaf8daad`: the
coordinator re-baselines); or an execution limit, stated as such with the
running log current. A checkpoint is not a stop (D-WORKFLOW-149): write it
and take the next stage. A reviewer seat failing verification is a recorded
pending line, not a stop. A differing count is a delta, not a stop. An idle
session says it is idle on #648.

## 9. Ceremonies owed

- A work-log entry per session, headed by `#648`; `tools/work-log-index
  --write` after it; the weekly summary if the lane's week falls due
  (`ceremonies.md`; the W42 summary is the M7 lane's and is not this
  lane's to write).
- A friction line in `docs/friction-log.md` the moment something slows,
  with `issue: #648` or the guard.
- The VM question written before every proof (§ 5 answers it for the slice;
  a proof that needs something the guest lacks writes its own line in
  `02-forward-audit.md`).
- The mini-retro skill at stage G, posted on #648, with its scoped audit.
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
  `--no-verify`.
- Commit messages in the fork's style (`docs: ...`, `rocknix: ...`), `Refs
  #648` while any criterion is open; a `bug` fix also `Refs` its bug.
- `change-log.md`'s running log the day a player-visible change lands
  (stage E).

## 10. Hand-back

The coordinator accepts the slice by reading, in this order, without
re-reviewing it: #648's checkboxes against their artifacts (§ 7); the lint's
PASS line on the audit folder; `second-opinions/` (two provenance files
naming two served models from two labs, or one and the pending line with
the coordinator's recorded decision); the audit issue's checkboxes all at an
outcome; the coverage table's row count; `docs/reviews/status.md`'s row for
`os-launch-control-state` (`closed`, both hashes); `tools/renovation-drift`'s
output; the retro's four answers; the five checker exit codes on #648. The
lane posts one hand-back comment on #648 naming the branch tip and each of
those artifacts by path, then says it is idle. A brief that needed the
coordinator's help mid-slice, beyond the stage-D pause and the Argon
decision this brief already names, is a defect in this brief: log the
friction, and the coordinator fixes the template in plan § 7 before the next
brief.

**The stranger's proof** (plan § 3, principle 3): before dispatch, a reader
with no context was given this tree and this brief and asked for its first
hour's plan and every question it would have to ask; the questions were
answered in the text above. Recorded here by the coordinator at dispatch:
_pending_.
