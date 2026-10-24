# Brief: M6.P2 T30, the standalone emulators (#677)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #677 differ, #677 wins and the
coordinator corrects the brief in the same session. **Version 1
(2026-10-24):** written after T3's audit of the libretro half of this area
(#826, closed 2026-10-24) and T1's of the launcher that starts these
emulators (#648, accepted), by the coordinator who dispatched both, so the
leads they routed here are named in § 3 and the shapes their stranger's
proofs found wrong -- a count from the wrong tree, a line number from
memory, a glob that reached another slice's files, a guest proof claimed
for an input the guest cannot have -- are answered from the start; every
figure below was produced by a command at `8ebaf8daad` unless it says
*branch*. It goes through a stranger's proof before dispatch; version 2
records what it found. **Each command block sets its own variables** (`D`,
`P`): a Bash call in this harness starts a fresh shell. **This is a currency
slice with a launch-path lens**: its fork-own lines are read line by line,
the rest for reachability and currency (plan § 2), and every start script is
read as the thing a player's press runs.

## 1. Identity

- **Issue:** #677 `M6.P2 E798/T30: emulators-and-cores: the standalone
  emulators`, slice `emulators-standalone` (`k: 30`) in
  `docs/reviews/slices.json`, thirtieth in `docs/reviews/order.md` (its
  sizing row: `| 30 | the standalone emulators | emulators-and-cores |
  currency | launch path, brittleness | 543 | 157,365 | 10,695 (3,104) | 0 |
  Extended |`; its `why`: *"the start scripts and configuration of every
  standalone emulator the image ships"*). **Epic:** #798 (the emulators and
  cores: T3 #650 accepted 2026-10-24, this slice, T24 #671 after it), whose
  futro (`docs/futros/2026-10-24-m6-emulators-and-cores.md`) covers T30's
  order and gains a kickoff addendum with this brief's version 2.
  **Milestone:** M6; its body holds the live order. **Predecessors:** #346,
  #641, **T3 #650** (the libretro half: its audit folder
  `docs/audits/2026_10_24-epic-m6-emulators-libretro/` on
  `feature/m6-emulators-libretro-650` at `b3cb4ec8c5`, whose Q4 tooling
  (`tools/q4-pins.py`, `q4c-patches.sh`), Q6 tables and S2 regeneration
  check (`s2-regen-check.sh`, `regen-es-systems.sh`) this slice reuses by
  path parameter, and whose dispositions already name three of this
  slice's recipes: `aethersx2-sa` (class 1, upstream's `c4d353449e` deletes
  it at the base merge), `rpcs3-sa`'s exit-hotkey target (upstream's
  `eeb33c5a37`, base merge), `steam`'s `Install Steam.sh` (`deferred:M7-merge`
  with the M7 hunk `6101242e14`; the script is T3's file, the `steam`
  recipe is this slice's)), **T1 #648** (the launcher: `runemu.sh`'s
  standalone arms start these scripts, `input_sense` ends them with
  `killall ${TO_KILL}` from `/tmp/.process-kill-data`, which
  `001-functions:511` writes -- T1's F-24 is this slice's class: the name
  written must be the process the emulator runs as). **Beside it:** T6
  (#653) runs in the other lane (D-WORKFLOW-190); the two share no path.
- **The division of labour (D-WORKFLOW-189).** This lane executes; the
  coordinator plans. The lane files its audit punch-list issue (stage D) and
  a `bug` per defect (D-WORKFLOW-187); nothing else; a question of scope goes
  on #677, one at a time.
- **One worktree, one session.** Branch `feature/m6-emulators-standalone-677`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-standalone-677`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the hashes are in the dispatch comment on #677). **Before that
  comment exists there is no worktree at that path and none of the first
  commands can run.** The session is the T3 lane's (`m6-t3-emulators`, pane
  `wN:p6`), which knows the area and its tools; its T3 worktree stays
  beside this one, idle, until the merge, and nothing is written there.
  The primary checkout `/workspace/repos/pixelelated/distribution` stays on
  `next` (D-INFRA-025); the legacy checkout and `rocknix.worktrees/*` are
  the M7 lane's, read only (the three install trees § 5 names are read
  there, never written, never a process started there); the other lanes'
  worktrees are `git -C` only. **The rules in this worktree are `next`'s
  except six files** (P1's `fork-workflow.md` and `instruction-files.md`;
  the coordinator's `generic-x64-vm-testing.md` paragraph `8c9b1d4721` and
  `engineering-practices.md` bullet `ab8f750784`; M7's
  `.claude/skills/council/IMPORTED-FROM.md`; `tools/lint-audit-artifacts`
  with `templates.md` from #810). Known stale facts in the rules (the legacy
  layout in eight files, #640; `tools/es-syntax-check`'s default root,
  #699) do not cost an hour: every rule the work touches is named in § 3.
- **Model and effort:** Opus 5.5 at high effort. Record what ran in
  `00-running-log.md`'s header.
- **Review depth: Extended** (plan § 6c: the start scripts are on the launch
  path; D-WORKFLOW-184). Two reviewers from two labs through the
  Facilitator (`tools/council/run invoke --member gpt|gemini-argon
  --provider openrouter`): **GPT-6 Astra at `max`** and **Gemini 4 Argon at
  `high`**, each a probe first (identity, effort, provider from the
  provider's own field), then a refutation pass over one packet given to
  both independently, as T3's Phase 4.6 did (its `second-opinions/` is the
  model: the briefs, the probe prompts, the provenance files beside each
  output). `npm install --prefix tools/council`, `verify-pins` and `test`
  first. A failed seat is a hold, never a one-seat grading (the
  coordinator's rule on #650, 2026-10-24: record, diagnose, one same-slug
  retry on a transient cause, then post; escalation is the coordinator's).
  The dispatch comment authorizes the two calls.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-standalone-677
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-emulators-standalone-677
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: this is not the lane's worktree (stacked on P1): stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # the six files § 1 names, nothing else
mkdir -p .qa-scratch/t30/at-hash && git archive 8ebaf8daad projects/ROCKNIX/packages/emulators/standalone | tar -x -C .qa-scratch/t30/at-hash   # the read tree; every line number in the artifacts is this tree's unless marked branch
git diff --stat 8ebaf8daad HEAD -- projects/ROCKNIX/packages/emulators/standalone   # empty on 2026-10-24 (T3's streams touched libretro/, virtual/emulators and retroarch, not standalone/): a non-empty result is the first lead
"$D/tools/rules-check"; echo "rc=$?"; "$D/tools/register-check"; echo "rc=$?"; "$D/tools/ceremony-check"; echo "rc=$?"   # rc 1 on 2026-10-24: W42 OVERDUE (M7's week), a retro DUE; neither is this lane's
git push -u origin feature/m6-emulators-standalone-677
test -f docs/reviews/briefs/emulators-standalone.md || { echo "the brief is not in this tree: stop"; exit 1; }
cat .github/sessions/saved-session-state-feature-m6-emulators-standalone-677.md
tail -3 /tmp/m7-m6-host-coordination-20261023.txt                   # the host: a guest runs only when M6 holds the host; census first, pidfile, stop after
df -i /tmp | tail -1                                                 # never export a tree under /tmp (the tmpfs ran out of inodes on 2026-10-24); exports go under /workspace/tmp/m6-t30/
test -f ~/.config/council/env && echo "council env present (never read into a transcript)"
```

## 2. Scope

**543 paths, 157,365 lines; 55 fork-own (7,421 lines) and 488
upstream-carried; every path `reach: shipped`; 10,695 lines in the code
classes to read line by line, 3,104 of them fork-own.** The membership is
the inventory's at P1's `eb4763e3cc`, with the slice's rule (`k: 30`): the
rows of the `emulators-and-cores` area under
`projects/ROCKNIX/packages/emulators/standalone/**` with reach `shipped`,
`test` or `n/a` (all 543 are `shipped` today). **Not in the membership:**
the libretro recipes and RetroArch (T3's), the `emulators` metapackage and
its `sources/` scripts including `Install Steam.sh` and `Start *.sh` (T3's:
the device arms that name which standalone emulator each device gets, and
the tools-system launchers), the quirks (T29's), `runemu.sh` and
`input_sense` (T1's, accepted, read-only context), the cloud sync's save
layout (`cloud-sync-core`'s, read-only context). The re-derivation:

```bash
python3 -I - <<'PY'
import json, re, collections
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
t30 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "emulators-and-cores"
       and r["path"].startswith("projects/ROCKNIX/packages/emulators/standalone/") and r["reach"] in ("shipped", "test", "n/a")]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
CODE = {"shell", "python", "recipe", "c", "c++", "c-header", "c++-header", "javascript", "typescript", "make", "cmake", "systemd", "udev", "script", "perl", "lua", "rust", "go", "assembly", "shader", "docker", "kconfig", "html", "css"}
read = [r for r in t30 if r["language"] in CODE]
print("paths", len(t30), "lines", L(t30), dict(collections.Counter(r["tier"] for r in t30)), dict(collections.Counter(r["reach"] for r in t30)))
print("read", len(read), "lines", L(read), "fork-own read lines", L([r for r in read if r["tier"] == "fork-own"]))
print("languages", dict(collections.Counter(r["language"] for r in t30)))
print("recipes", sorted({r["path"].split("/")[5] for r in t30}))
PY
git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/packages/emulators/standalone | wc -l           # 543
git ls-tree --name-only 8ebaf8daad -- projects/ROCKNIX/packages/emulators/standalone/ | wc -l             # 35 recipe directories
```

Recorded (2026-10-24): **543 paths, 157,365 lines; fork-own 55 (7,421
lines), upstream-carried 488; all `shipped`; code classes 10,695 lines
(shell 55 files, recipe 47, python 2, c 1), 3,104 of them fork-own.**
Languages: config 277, symlink 80, shell 55, other 52, recipe 47, xml 13,
yaml 9, json 2, python 2, c 1, image 1, font 1, text 1, none 2. **No
patch** in the membership (0 `.patch` files). **35 recipe directories**:
`aethersx2-sa amiberry ares-sa armsx2-sa azahar-sa bigpemu-sa cemu-sa
daedalusx64-sa dolphin-sa drastic-sa dsperate-sa duckstation-sa flycast-sa
gopher64-sa gzdoom-sa hatarisa heroic hypseus-singe mednafen melonds-sa
mupen64plus-sa nanoboyadvance-sa openbor pico-8 ppsspp-sa rpcs3-sa
scummvm-sa skyemu-sa steam supermodel-sa touchhle-sa vice-sa vita3k-sa
xemu-sa yabasanshiro-sa` (47 `package.mk` with `mupen64plus-sa`'s
sub-recipes). **Thirteen `package.mk` are fork-own** (the fork changed
them: `aethersx2-sa`, `amiberry`, `bigpemu-sa`, `daedalusx64-sa`,
`dolphin-sa`, `drastic-sa`, `duckstation-sa`, two of `mupen64plus-sa`'s,
`openbor`, `ppsspp-sa`, `steam`, `yabasanshiro-sa`); the rest of the 55
fork-own files are the GENERIC_X64 configs (the VM device's: eleven
one-line files that are symlinks or includes, `rpcs3-sa`'s, `dolphin-sa`'s,
`cemu-sa`'s, `drastic-sa`'s, `supermodel-sa`'s, `mupen64plus`'s 664-line
`mupen64plus.cfg`), `duckstation-sa`'s nine per-device `settings.ini`
(200 to 323 lines each), the cheevos scripts (`cheevos_armsx2.sh`,
`cheevos_dolphin.sh`, `cheevos_melonds.sh`, `cheevos_ppsspp.sh` fork-own;
`cheevos_aethersx2.sh`, `cheevos_duckstation.sh`, `cheevos_flycast.sh`,
`cheevos_skyemu.sh` upstream-carried -- eight in all), `dolphin-sa`'s
`dolphin-save-paths`, `start_dolphin_gc.sh` (478), `start_dolphin_wii.sh`
(442), `duckstation-sa`'s `start_duckstation.sh`, `duckstation_screenshot_path`
and `Start Duckstation.sh`, `mupen64plus-sa-core`'s `start_mupen64plus.sh`.
**The largest files are data**: `aethersx2-sa/sources/resources/GameIndex.yaml`
(62,331 lines; the recipe upstream deleted), `mednafen/config/common/mednafen.template`
(17,652), `vita3k-sa/sources/vita-gamelist.txt` (4,583) -- read for what
they are (provenance, currency) and never line by line.

**The hash.** `8ebaf8daad`'s bytes; `reviewed-at:` the branch `HEAD` at
stage A; the branch's diff from the hash on the membership is empty on
2026-10-24 (the first block checks it).

**Where these run.** `runemu.sh` (T1's, at `8ebaf8daad`) starts a
standalone emulator through its start script: the generic arm
`RUNTHIS='${RUN_SHELL} "/usr/bin/start_${CORE%-*}.sh" "${ROMNAME}" "${PLATFORM}"'`
(`runemu.sh:391`), and named arms for `start_mednafen.sh` (236),
`start_scummvm.sh` (314), `start_dolphin_gc.sh`/`start_dolphin_wii.sh`
(365, 369). **Forty start scripts** are in the membership
(`scripts/start_*.sh`: `start_aethersx2.sh start_amiberry.sh start_ares.sh
start_armsx2.sh start_azahar.sh start_bigpemu.sh start_cemu.sh
start_daedalusx64.sh start_dolphin_gc.sh start_dolphin_wii.sh
start_drastic.sh start_dsperate.sh start_duckstation.sh start_flycast.sh
start_gopher64.sh start_gzdoom.sh start_hatari.sh start_heroic_authenticate.sh
start_heroic_play.sh start_heroic_play_gamescope.sh start_hypseus.sh
start_mednafen.sh start_melonds.sh start_mupen64plus.sh start_nanoboyadvance.sh
start_OpenBOR.sh start_pico8.sh start_ppsspp.sh start_rpcs3.sh start_scummvm.sh
start_skyemu.sh start_steam.sh start_steam_arm64.sh start_steam_x86.sh
start_supermodel.sh start_touchhle.sh start_vice.sh start_vita3k.sh
start_xemu.sh start_yabasanshiro.sh`), installed to `/usr/bin/`; each is
on the launch path for its emulator. **The exit:** `input_sense`
(`projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/input_sense:179-224`,
T1's) runs `killall ${TO_KILL}` with the names `001-functions:511` wrote to
`/tmp/.process-kill-data` -- so for every standalone emulator the name
written must be the process it runs as, which is T1's F-24 (`rpcs3` for a
binary `rpcs3-sa`, fixed upstream by `eeb33c5a37`) generalised: **a Q3 sweep
of all 35**. **Which device ships which** is the `emulators` metapackage's
device arms (`projects/ROCKNIX/packages/virtual/emulators/package.mk:12-94`,
`PKG_EMUS`; T3's file, read-only here): the base set `amiberry
duckstation-sa flycast-sa gzdoom-sa hatarisa hypseus-singe moonlight
mupen64plus-sa openbor pico-8 ...` plus per-device additions (H700 adds
`drastic-sa mednafen`; SM8550 adds `aethersx2-sa azahar-sa bigpemu-sa
cemu-sa dolphin-sa heroic mednafen melonds-sa nanoboyadvance-sa rpcs3-sa
supermodel-sa ...`; the arms are read for the exact lists). **What the
GENERIC_X64 image ships** (the M7 root's install tree, read only):
`dolphin-emu`, `duckstation-sa`, `flycast`, `hatarisa`, `hypseus`,
`moonlight`, `ppsspp`, `scummvm`, the `mupen64plus` set, and their start
scripts -- nine standalone emulators the guest can start; the rest are
aarch64-only or absent on x86_64 and are proven on the host (`image-set`
from the H700 and SM8550 trees) or marked for the first image.

**The pins (Q4).** 35 `PKG_VERSION` lines of five shapes: a full commit hash
(23: `amiberry`, `ares-sa`, `armsx2-sa`, `azahar-sa`, `cemu-sa`,
`daedalusx64-sa`, `dolphin-sa`, `flycast-sa`, `gopher64-sa`, `hatarisa`,
`hypseus-singe`, `melonds-sa`, `nanoboyadvance-sa`, `openbor`, `pico-8`
(no URL: the binary is the player's), `ppsspp-sa`, `rpcs3-sa`, `skyemu-sa`,
`supermodel-sa`, `touchhle-sa`, `vita3k-sa`, `xemu-sa`, `yabasanshiro-sa`);
a tag (`gzdoom-sa` `g4.14.2`, `scummvm-sa` `2026.1.0`, `vice-sa` `3.8`,
`mednafen` `1.32.1` from a fork's tag); a release asset (`duckstation-sa`
`0.1-10998`, an AppImage per arch; `dsperate-sa` `2.0.1`; `bigpemu-sa`
`v119`, a binary tarball; `steam` `1.0.0.85`, a `.deb`); **a tarball on a
moving branch** (`aethersx2-sa` `1.5-3606` from
`ROCKNIX/packages/raw/refs/heads/main/aethersx2.tar.gz`, `drastic-sa` `1.0`
from `ROCKNIX/packages/raw/main/drastic.tar.gz` -- the bytes can change
under the version; `PKG_SHA256` is the only pin, D-WORKFLOW-193's class,
and #844's check is the guard); and metapackages with no source
(`mupen64plus-sa`, `heroic` `1.0`). T3's `tools/q4-pins.py` takes the
recipe root as a parameter and reads a GitHub recipe's pin, default branch
and head through `gh api` (no clone): run it over `standalone/` for the 23
hashes and the tags; the release assets and the moving tarballs are rows
of their own shape (the asset's current release; the tarball's current
sha256 against `PKG_SHA256`, downloaded into `/workspace/tmp/m6-t30/`,
never the shared cache). **Upstream's side:** `git diff --stat
upstream/next 8ebaf8daad -- projects/ROCKNIX/packages/emulators/standalone`
for the recipes the fork changed (thirteen `package.mk` are fork-own: for
each, upstream's pin and the fork's, and the reason the fork's differs --
T3's two-tier Q4, `behind-upstream` actionable and `behind-project`
informational); `git log --oneline 8ebaf8daad..upstream/next --
projects/ROCKNIX/packages/emulators/standalone` for upstream's commits
since the base (`c4d353449e` deletes `aethersx2-sa`; `eeb33c5a37` fixes
`Start RPCS3.sh`'s target, T3's file; others the lane lists), each `to
merge` with the base merge, `superseded` or `conflicts`, in
`q4a-dispositions.md` as T3 did.

**Drift.** `next` is `8ebaf8daad`; the M7 candidate's merge moves it; the
coordinator merges `next` into the branch never between stage A and stage
D, and re-baselines after.

## 3. Read first

- `.github/sessions/saved-session-state-next.md` and this lane's pointer.
- **The rules this work touches** (`working-principles.md` § Pre-flight):
  `engineering-practices.md` (§ Change stays inside the fork's lanes --
  the standalone emulators are inside them: the launch path, game saves and
  save states, the offline achievements; § Verify the artifact; § A name is
  not a behaviour; § Guards must fail closed; § Nothing runs on a person's
  device; § If the VM can test it), `packaging-and-patches.md` (the
  `package.mk` rules; `tools/pkgcheck` after every edit), `time-to-play.md`
  (a start script is on the launch path: nothing added there unless it
  must; the two numbers measured on the guest for the standalone emulators
  it ships), `least-surprise.md`, `rclone-cloud-sync.md` and
  `docs/cloud-save-integrity.md` (the save layout cloud sync moves: a
  standalone emulator's save path is what `tools/pixelelated-save-layout-test`
  derives from source, #520 -- a config change here can move a save out of
  the sync's reach), `upgrade-and-install.md` (`Already written:` for every
  config change: a device keeps its own emulator configs under `/storage`),
  `generic-x64-vm-testing.md` (the guest, SSH and the walks),
  `vm-first.md`, `bugs-are-agent-first.md`, `issue-tracking.md`,
  `device-builds.md`, `fork-workflow.md`, `worktrees.md`.
- The code-auditor skill whole; the renovation face is plan § 6b.
- **T3's audit** (read with `git -C` or `git show` on
  `feature/m6-emulators-libretro-650` at `b3cb4ec8c5`): `04-analysis.md`
  § Q4 (the two-tier method and its tables), `q4a-dispositions.md` (the
  upstream commits to merge, three of them this slice's), `q6-tables.md`,
  `05-punch-list.md`'s dispositions (PL-004 `aethersx2-sa`, PL-010
  `rpcs3`, PL-023 the rotation hook, PL-008/009/021/022 `Install Steam.sh`),
  the tools under its folder (`q4-pins.py`, `q4c-patches.sh`,
  `regen-es-systems.sh`, `s2-regen-check.sh` with its `XS=` line,
  `punch-items.py`, `coverage-table.py`, `audit-issue-body.py`,
  `set-outcome.py`) -- reuse them by path, copied into this slice's folder
  with their headers saying where they came from. **T1's audit**
  (`docs/audits/2026_10_24-epic-m6-os-launch-control-state/` at
  `d3aa6a19c5`): `runemu.sh`'s standalone arms and F-24 (the kill target),
  the `001-functions` writer of `.process-kill-data`, and
  `tools/emulator-exit-test`'s scope (it drives RetroArch only on
  2026-10-24: `grep -o retroarch tools/emulator-exit-test` finds it, no
  standalone name appears -- the harness gap § 5 names).
- **`docs/reviews/build-path-read.md`** (#644): none of its 26 findings is
  this slice's; say so.
- `docs/blindspot-register.md` whole once, then **8** (an assertion that
  holds only because nothing had happened yet: a kill target that works
  because the emulator has never been exited by hotkey on that device),
  **22** (a probe that cannot report absence), **46**, **65** (a substitute
  input passing where the real one fails: a homebrew ROM is not a
  commercial one), **74**, **75**.
- Decisions by ID: D-WORKFLOW-184/186/187/164/165, D-WORKFLOW-193/194 (a
  recipe without `PKG_SHA256` fails its fetch: every recipe here is checked
  for one, per `case` branch), D-WORKFLOW-024 (fork-introduced packages
  current), D-UI-079 (the lanes), D-CLOUD-098/119 (time to play and the
  exit sync's budget), D-QA-015 (nothing on a person's device), D-QA-051,
  D-RA-* rows on the offline achievements proxy (the cheevos scripts write
  the player's RetroAchievements settings into each emulator's config: read
  those rows before judging them), D-LAUNCH-002 (the kill marker).
- Issues: #677 (this), #650, #648, #671 (T24, the dead-end table after
  this), #802 (`pcsx_rearmed32`: not this slice's, but `duckstation-sa` is
  `psx`'s default on GENERIC_X64 since S2), #825 (the hook that ran a title
  through a shell: **the question to ask of every cheevos script and every
  start script that builds a command from a game's name or a server's
  answer**), #839/#842/#844 (the bump and check issues T3 produced),
  #520 (the standalone save layout), #10 (save-state compatibility across
  devices), #585 (the contribution queue: `eeb33c5a37`'s class), #336
  (the headless libretro runner: not this slice's, named so it is not
  taken). Every `gh` call carries `--repo pixelelated/distribution`.

## 4. The questions

All seven apply (plan § 4); Q3 and Q4 are the spine of a currency slice
with a launch-path lens; Q6 is reachability per device.

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | A start script written against a mechanism the tree has retired: a path under `/storage` the save layout moved (D-CLOUD rows; `dolphin-save-paths` is the fork's own answer), a setting key the interface renamed (the `testunofficial` spelling `cheevos_*.sh` still reads *before 2026-09*), a `jslisten`/`gptokeyb` call the quirks replaced, a `${CORE%-*}` naming that a renamed recipe broke; a config shipped for a device the fork no longer builds (D-WORKFLOW-185: H700 and SM8550 ship; the other devices' configs are carried for the unshipped tables, T25's) | the retiring row or commit beside the line; the current mechanism's line |
| Q2 Standards | `tools/pkgcheck` on all 47 recipes (late binding; T3's S1 found it catches global-scope `PKG_BUILD`); `bash -n` on the 55 shell files, shellcheck not runnable on the host (recorded); the fork's header kept on the thirteen changed recipes; `PKG_SHA256` present per `case` branch (D-WORKFLOW-193) | the commands and their counts |
| Q3 Bugs | **The exit sweep:** for each of the 35, the name written to `/tmp/.process-kill-data` (by `001-functions`' caller in `runemu.sh` or the start script) against the binary's process name in the install tree (`comm` on the guest for the nine it ships) -- F-24's class; **the shell-line sweep (#825's class):** every start script and cheevos script that builds a command, a config line or a file name from `${ROMNAME}`, a game's title, or a server's answer, with the quoting read (a ROM named `$(…).iso` is a player's file; a title is the set's text); a script that writes the player's RetroAchievements credentials into a config with the wrong mode or logs them (`LOG_FILE=/var/log/cheevos.log`: what goes in it?); a start script whose failure leaves the player on a black screen with no return to the interface; a config that points at a BIOS or a path that does not exist on the device; `duckstation-sa`'s AppImage strip override and its `install -m 0755` into `/usr/bin` | the artifact: the install tree's binary name, the guest's `comm`, a fixture under `.qa-scratch/t30/` that feeds a crafted name, the script's own log; every finding a `bug` with its VM line |
| Q4 Currency | Two tiers as T3's: **behind-upstream** (the thirteen fork-own recipes against `upstream/next`'s, and every upstream commit since the base on `standalone/`, each `to merge`, `superseded` or `conflicts`) is actionable; **behind-project** (each of the 35 pins against its project's default branch head and release, through `q4-pins.py` for the GitHub hashes and tags, by hand for the release assets, the two moving tarballs and the fork-sourced `mednafen`) is informational, with a disposition per row: bump proposed (#842's shape, the coordinator files), kept with the reason in the recipe (D-WORKFLOW-024), or no project (`pico-8`, `heroic`, `mupen64plus-sa`'s meta) | the two tables with no empty cell (T3's rule); `q4-pins.json`/`.md`; `q4a-dispositions.md` |
| Q5 Efficiency | **Time to play for the standalone emulators the guest ships**: `tools/time-to-play` measures interface → first frame and game → game for RetroArch; for the nine standalones, the launch's own wall time from `runemu.sh`'s start to the emulator's first frame (the guest's screen) and from the exit hotkey to the interface, measured once each where free content exists (§ 5), reported beside T1's and T3's numbers; what a start script does before `exec` (a `sleep`, a config rewrite on every launch, a `find` over `/storage/roms`) is the cost to name; the configs' size against what the emulator reads | the measurements with their method; a `Renovation` item per avoidable step on the launch path |
| Q6 Dead ends | Per device: which of the 35 each shipped device gets (the metapackage's arms) and which the GENERIC_X64 image ships (nine); a start script no arm names (`start_heroic_*` on which devices? `start_steam_x86.sh` on an aarch64-only set?); a per-device config directory for a device no table builds (T25's rows: named, not removed here); a cheevos script for an emulator that has no RetroAchievements support in its pinned version; `aethersx2-sa` whole (deleted upstream: every row of its 60-odd files is `deferred: base merge, class 1`, read for what the deletion leaves on a device -- its saves and configs under `/storage`, `Already written:`) | the reachability table: one row per recipe (35) with its devices, its start scripts, its configs per device, and the guest's yes/no; per-file rows only where a file's reach differs from its recipe's |
| Q7 Clarity | Two start scripts that do one job (`start_dolphin_gc.sh` 478 lines and `start_dolphin_wii.sh` 442: how much is shared?); eight cheevos scripts of one shape (a shared function's worth?); `duckstation-sa`'s nine `settings.ini` of 200 to 323 lines (what differs per device, and is the difference the device's?); a start script's comments against what it does | the pairs named with a diff of their words or their shared lines counted |

A finding is one question with its evidence; `Renovation` is the category
for Q1, Q5, Q6 and Q7 items that are not defects. **A Q3 finding is a `bug`**
(D-WORKFLOW-187), and a start-script defect on the launch path is graded
with time to play and least surprise in mind: a black screen with no way
back is High.

**The ladder:** a finding found twice (two emulators with the same kill
name mismatch; two scripts with the same quoting) is a tool proposal --
#838's cousin for the kill names (*every name in `.process-kill-data`
matches a binary the image carries*), filed by the coordinator -- not a
per-script fix only.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor):

1. Tracker state is never sole evidence.
2. Mechanical evidence outranks reading: `pkgcheck`, `bash -n`, the install
   tree's `ls`, the guest's `comm`, a measured launch.
3. **Run it on a device, not on the host: the GENERIC_X64 guest for the
   nine standalone emulators it ships, with free content**; the H700 and
   SM8550 install trees (read only, from the M7 roots) for the rest's
   presence and names; a fixture for a script's quoting. A claim about a
   launch the guest cannot make (an aarch64-only emulator, a commercial
   ROM, a BIOS the project does not ship) is a lead and an open item to
   test, never a verdict (blindspot 65: a homebrew title is a substitute
   input and the tick says so).
4. An assertion that cannot fail is not evidence: for every PASS, what
   result would have produced a FAIL.
5. Subagent output is a lead; fan-out is read-only research only.

**What runs on the VM, and how.** Can this be done on the VM? **Yes, for
the nine standalone emulators the GENERIC_X64 image ships and for every
script's quoting; no for the twenty-six it does not ship** (aarch64-only
builds, or absent from the x86_64 image), whose presence and names are read
from the H700 and SM8550 install trees and whose launch is an open item to
test (D-QA-051). **Free content for the guest:** ScummVM's freeware games
(the project's own downloads), EmuTOS for `hatarisa` (free TOS
replacement), a homebrew `.pbp` for `ppsspp`, a homebrew N64 ROM for
`mupen64plus`, a homebrew `.dol` for `dolphin`; `duckstation-sa` needs a
PlayStation BIOS and `flycast` a Dreamcast one (the open items), `hypseus`
laserdisc content, `moonlight` a streaming host -- each a row saying so.
Nothing in this slice touches a handheld, a person's cloud, a shared QA
backend or a guest another lane owns.

- **The host handoff is a wait, not a stop.** The guest runs only when M6
  holds the host (`/tmp/m7-m6-host-coordination-20261023.txt`; the
  coordinator relays); census first (`pgrep -c -x qemu-system-x86` 0),
  pidfile under `/workspace/tmp/m6-t30/qemu.pid`, `tools/vm-stop` after,
  the census again. **The guest:** T3's recipe (its brief § 5; the image
  `069fc2704421` the M7 lane's GENERIC_X64 build left, read only), with
  this lane's ports **VNC display 24 and SSH 10037** (T1 19/10032, T2
  20/10033, T3 21/10034, T4 23/10036 reserved). SSH is disabled on a fresh
  image: `tools/vm-serial` is the way in; `tools/qa-accounts` carries any
  QA credential without printing it.
- **The host-side checks**, each run with its command, exit status and
  summary line recorded in `02-forward-audit.md`:
  ```bash
  D=/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-standalone-677
  P=projects/ROCKNIX/packages/emulators/standalone
  cd "$D"; mkdir -p .qa-scratch/t30 /workspace/tmp/m6-t30
  for r in $(git ls-tree -r --name-only 8ebaf8daad -- $P | grep 'package.mk$'); do d=$(dirname $r); n=$(basename $d); tools/pkgcheck "$n" >/dev/null 2>&1; echo "$? $n"; done | sort | uniq -c | sort -rn | head        # Q2: pkgcheck over the 47 recipes (a name that is a sub-recipe directory is checked by its own name)
  for f in $(git ls-tree -r --name-only 8ebaf8daad -- $P | grep '\.sh$'); do bash -n ".qa-scratch/t30/at-hash/$f" 2>/dev/null && echo ok || echo "FAIL $f"; done | sort | uniq -c    # Q2: bash -n over the 55 shell files
  for r in $(git ls-tree -r --name-only 8ebaf8daad -- $P | grep 'package.mk$'); do n=$(grep -c 'PKG_SHA256=' ".qa-scratch/t30/at-hash/$r"); u=$(grep -c 'PKG_URL=' ".qa-scratch/t30/at-hash/$r"); echo "$u urls $n sha256 $r"; done | grep -v '^0 urls' | awk '$1 > $3' | head   # D-WORKFLOW-193: a URL branch without a checksum (none expected after T5's E6 count; the per-branch read decides)
  git grep -n -F '.process-kill-data' 8ebaf8daad -- projects/ROCKNIX/packages/rocknix/profile.d/001-functions projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh $P | head   # who writes the kill name; then, per emulator, the name against the install tree's binary
  R=/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system; H=/workspace/repos/rocknix.worktrees/m7-signin-h700-build-20261023-06/build.pixelelated-H700.aarch64/image/system; S=/workspace/repos/rocknix.worktrees/m7-signin-sm8550-build-20261023-03/build.pixelelated-SM8550.aarch64/image/system
  for t in "$R" "$H" "$S"; do echo "== $t"; ls "$t/usr/bin" | grep -E '^start_.*\.sh$' | tr '\n' ' '; echo; done   # image-set: the start scripts each image carries (read only; the roots are M7's)
  grep -n -E 'eval|\$\(|`' .qa-scratch/t30/at-hash/$P/*/scripts/*.sh | grep -i -E 'ROMNAME|title|name|game' | head -20    # #825's class: a command or a line built from a name; each hit is read, not graded by the grep
  grep -n -E 'LOG_FILE|>>|tee' .qa-scratch/t30/at-hash/$P/*/scripts/cheevos_*.sh | head                                          # what the cheevos scripts log; never print the values a setting holds
  git log --oneline 8ebaf8daad..upstream/next -- $P | cat                                                                        # upstream's commits since the base on the membership: each a q4a row
  git diff --stat upstream/next 8ebaf8daad -- $P | tail -1                                                                       # how far the fork's standalone/ is from upstream's today
  ```
- **A read is free and goes through the filter** (`grep -v -i -E
  'key|pass|token|user|psk|login'`, or the masking `sed`) on any config,
  log or `get_setting` output read from a guest or a build root; the cheevos
  scripts handle the player's RetroAchievements sign-in, so **a line from
  their log or a config they wrote is read masked, always**. The wordlist is
  never read.
- **The guest proofs**, each a `GUEST-PROOF:` line in the running log with
  the command and the frame or the `comm`: the nine shipped emulators'
  kill names against their running process (`cat /proc/<pid>/comm` while a
  free title runs, against `/tmp/.process-kill-data`), the exit hotkey's
  path for those with free content (`tools/emulator-exit-test` covers
  RetroArch only today: the standalone launch and exit are driven by hand
  through `tools/vm-walks`' shape or the API, and **the harness gap --
  the exit test's standalone coverage -- is proposed as an issue the
  coordinator files**, `bugs-are-agent-first.md` rule 3), the two
  time-to-play measurements per shipped emulator with free content, and a
  crafted ROM name through a start script's quoting.

**What never runs in this slice:** a build; a guest while M7 holds the
host, or without the census, the pidfile and the stop; a command on a
handheld, a person's cloud or a shared QA backend; a process in an M7
worktree; a download into the shared sources cache (a tarball's checksum is
taken from a copy under `/workspace/tmp/m6-t30/`); a tree export under
`/tmp`; a model call outside `tools/council/run`; an edit at stage B; a
grading from one seat; `--no-verify`; bare `git stash`; `git worktree
remove --force` or `rm -rf` of any worktree; a write in another lane's
worktree or under `/workspace/repos/rocknix*`; a change to the order, the
slices, the plan, this brief, #677's criteria or the M6 body
(D-WORKFLOW-189); a GitHub issue other than the audit punch-list issue and
`bug` issues; **printing a value from a cheevos script's log or a config it
wrote**.

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#677`
(`Refs #677`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-emulators-standalone/00-running-log.md` | the skill's flight recorder: the model and effort, `reviewed-at` with `8ebaf8daad` beside it, every command with its exit status and time (from `date -u`, never typed), each stage's entry; **every guest check that stands as a proof on a line that begins `GUEST-PROOF:`** (criterion 12's token) and every host proof on `PROOF:`; each stage-B session's last line records `git status --short -- projects/ROCKNIX/packages/emulators/standalone` empty | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 543 re-derived with § 2's filter and its output, the 35 recipes, the thirteen fork-own `package.mk`, the branch's deltas (none expected); § Phase 1: T3's and T1's leads named with their dispositions, #644's none, the metapackage's device arms as a table (device × recipe) | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #677's checklist, plus **a coverage table with one row per path** (543; the first cell the path in backticks so ``grep -c -E '^\| `projects/ROCKNIX/packages/emulators/standalone/' 02-forward-audit.md`` prints 543, generated by T3's `coverage-table.py` adapted; Q1 to Q7 each answered or `n/a` with a reason); § Mechanical checks (every check of § 5); § The leads (T3's three, T1's F-24 class, #825's class per script); § Proofs with a `proved:` cell each | B onward |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: start scripts x `runemu.sh`'s arms x `input_sense`'s kill; cheevos scripts x the offline proxy's rows x #825; configs x the save layout (#520) x the cloud sync; `duckstation-sa` x S2's `psx` default on GENERIC_X64; the futro's predictions checked | B |
| Analysis | `.../04-analysis.md` | Phase 4, § Finding Verification (4.5), **§ Second opinion** (4.6: both seats' probes and refutations graded item by item with the artifact that decided each, as T3's), **§ Renovation face** Q1 to Q7 (Q4's two tables, Q6's reachability table, Q5's measurements) | B, C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (extended; `gpt` and `gemini-argon`), the briefs, the probe prompts, each output with its `.provenance.json` beside it | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts` after the two provenance files exist | C to D |
| Punch list | `.../05-punch-list.md` | Phase 5 with the YAML `punch_index` (T3's `punch-items.py`); every item with `question:`, severity, category, where (file:line at `8ebaf8daad`), acceptance, `tracked:` for a `bug`; `deferred: base merge, class 1` for `aethersx2-sa`'s rows and `eeb33c5a37`'s; the ladder's tool proposals named for the coordinator | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #677 | `Audit: M6 T30 the standalone emulators -- N findings (...)`; one checkbox per item; `box-check --issue N` once | D |
| Bug issues | GitHub, label `bug`, `Bug:` title, milestone-less | one per defect: the code trace, `Already written:` (a device keeps its own configs and saves under `/storage`: what the old script or config left there, and what the fix does with it), the VM line (yes for the nine; no with the open item for the rest), an agent-verifiable criterion | D |
| **The stage-D pause** | #677 | the punch list posted; the lane waits for the coordinator's stream briefs (D-WORKFLOW-189), drafting the retro's answers meanwhile and editing nothing of the 543 | D to E |
| Remediation | the branches the stream briefs name | each stream as its brief says: a start-script fix proven on the guest by `fix-guest-copy` (the script bind-mounted over the squashfs copy, the launch and the exit run, the `comm` read) for the nine, `fix-pending-image` for the rest; a config change with its `Already written:` (the device's own copy under `/storage` is untouched; the shipped default changes for fresh installs and missing keys); a recipe change with `pkgcheck` and `fix-pending-image`; a cheevos-script change proven with a fixture that feeds a synthetic sign-in and reads the written config's mode and the log's lines masked | E |
| Verification | `02-forward-audit.md` appended; `audit-completion.json` after the coordinator closes the audit issue | every proof's `proved:` cell one of `image-set`, `guest`, `fixture`, `history`, `fix-guest-copy`, `fix-pending-image`; `grep -c 'proved:' 02` = `grep -c '^GUEST-PROOF:\|^PROOF:' 00` | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-emulators-standalone.md`, posted on #677 | the four answers with the scoped audit; **what the slice did to the two time-to-play numbers**, with the standalone measurements beside RetroArch's | G |
| Hand-back | #677 | `reviewed-at:` and `fixed-at:` in the body; one comment: the tip, each artifact by path, the six checker exit codes, each fix's `proved:` class | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-emulators-standalone-677.md` | seeded by the coordinator; updated at every checkpoint | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session headed `#677`, stamped from the clock | every session |

## 7. Acceptance

The checklist on #677 is the contract (its body carries these sixteen,
written there with version 2 in place of the five generated ones; where the
two differ, #677 wins and the coordinator corrects the brief). Each names
the artifact that ticks it; the coordinator ticks at hand-back.

- [ ] `docs/audits/<date>-epic-m6-emulators-standalone/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-emulators-standalone/` prints `PASS` (its default `resolution` phase, at close; `--phase pre-issue` prints `PASS pre-issue artifacts` before stage D), the renovation face included.
- [ ] `second-opinions/review-plan.json` records Extended depth with `gpt` (`openai/gpt-6-astra`, `max`) and `gemini-argon` (`google/gemini-4-argon`, `high`), and each seat's probe and refutation output has its `.provenance.json` beside it naming the served model from the provider's own field.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue or the base merge (class 1 for `aethersx2-sa`'s rows and `eeb33c5a37`), or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits the read and the fixes were made at (the read on `8ebaf8daad`'s bytes; no EmulationStation path), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed`.
- [ ] `01-research-notes.md` § Scope records the read hash, the filter of brief § 2 with its output (543 paths, 157,365 lines; 55 fork-own and 488 upstream-carried; 10,695 code-class lines; 35 recipes; thirteen fork-own `package.mk`, or the deltas beside them), `git diff --stat 8ebaf8daad HEAD -- projects/ROCKNIX/packages/emulators/standalone` (empty, or each hunk with its owner), and the device × recipe table from the metapackage's arms.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c -E '^\| `projects/ROCKNIX/packages/emulators/standalone/' 02-forward-audit.md`` prints 543; each row's Q1 to Q7 cells answered or `n/a` with a reason.
- [ ] `02-forward-audit.md` § Mechanical checks records, with command, exit status and summary line, each of: `tools/pkgcheck` over the 47 recipes, `bash -n` over the 55 shell files, the `PKG_SHA256`-per-branch read, the `.process-kill-data` writer grep, the three install trees' `start_*.sh` lists, the #825-class grep with every hit read, the cheevos scripts' logging grep, and the two upstream greps; shellcheck recorded as not runnable.
- [ ] `04-analysis.md` § Renovation face Q3 carries **the exit sweep**: for each of the 35 emulators, the name written to `/tmp/.process-kill-data` beside the binary's name in the install tree (and the guest's `comm` for the nine the GENERIC_X64 image ships), each row `matches`, `differs` (a `bug`) or `not shipped on any built image`; and **the shell-line sweep**: every start and cheevos script that builds a command, a config line or a file name from a ROM's name, a title or a server's answer, with its quoting verdict.
- [ ] `04-analysis.md` § Renovation face Q4 carries the two currency tables with no empty cell: the thirteen fork-own recipes and every upstream commit since the base on the membership (`behind-upstream`, each `to merge` / `superseded` / `conflicts`, in `q4a-dispositions.md`), and the 35 pins against their projects (`behind-project`) by shape (hash, tag, release asset, moving tarball, no project), each with a disposition.
- [ ] `04-analysis.md` § Renovation face Q5 carries the standalone launch and exit measurements for the shipped emulators with free content on the guest (method, n, the numbers beside T1's and T3's), and names each start script's work before `exec`; § Q6 carries the reachability table (35 recipes × the devices that ship them × the guest's yes/no, with the per-file rows where a file's reach differs); every `aethersx2-sa` row reads `deferred: base merge, class 1` with its `Already written:`.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `image-set`, `guest`, `fixture`, `history`, `fix-guest-copy` or `fix-pending-image`; ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c -E '^(GUEST-PROOF|PROOF):' 00-running-log.md``; every guest proof names its input and whether it was a substitute (blindspot 65).
- [ ] Every punch item carries `question:`; every `bug` passes `tools/box-check --issue N`; every finding found in two scripts names the tool that would hold it (the ladder) for the coordinator to file; no file under the membership is changed on this branch before a stream brief (`git diff --stat 8ebaf8daad <fixed-at> -- projects/ROCKNIX/packages/emulators/standalone` shows only stage-E commits).
- [ ] Every guest run is preceded by the census and followed by `tools/vm-stop` and the census, recorded in the running log; no guest ran while the host file said M7 held the host; the guest's pidfile is under `/workspace/tmp/m6-t30/`.
- [ ] The retro exists at `docs/retros/<date>-m6-emulators-standalone.md`, is posted on #677, and gives the standalone time-to-play measurements beside RetroArch's.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge, and `tools/lint-audit-artifacts` prints `PASS` on the folder; the six exit codes pasted on #677.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #677; **a seat that fails after the Facilitator's retries** (hold, post,
the coordinator decides); a blocker named on #677 with what is needed; a
branch that differs from `8ebaf8daad` on the membership at stage A in a
hunk the dispatch comment did not name; or an execution limit, stated as
such with the running log current. The host handoff is a wait. A
checkpoint is not a stop; a differing count is a delta; `next` moving is
drift. An idle session says it is idle on #677, **and does not end a turn on
a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#677`, stamped from `date -u`;
  `tools/work-log-index --write` after it; a row in `docs/vm-qa-log.md`
  for every guest cycle (the image, the ports, what ran, the frames'
  paths, the stop).
- A friction line the moment something slows, with `issue: #677` or the
  guard.
- The VM question written before every proof (§ 5 answers it per emulator).
- The mini-retro at stage G, posted on #677; its adjustments are proposals
  for the coordinator.
- A register row the same session for any decision the slice forces; the
  next Decided ID is checked on every pushed branch at the time (on
  2026-10-24 the highest Decided row is D-WORKFLOW-194; T6 runs beside this
  lane and may take 195); it goes at the end of `## Decided`.
- `tools/ceremony-check` before every push; what another lane owes is noted,
  not paid. Never `--no-verify`. Conflict markers checked (#696); ledgers
  united by whole entries. **A commit names its paths**; **a tree export
  goes under `/workspace/tmp/m6-t30/` after `df -i`**; **a regeneration or
  a fixture sets its own environment** (`env -i`, the C locale), as T3's
  `s2-regen-check.sh` does; **a stub or a fixture is part of the claim**
  (its call count and the bound file's hash printed before the verdict,
  #797).
- Commit messages `<package>: <text>` for a recipe or script,
  `docs: ...` for the audit, with `Refs #677` and the bug's number.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#677's checkboxes against their artifacts; the lint's `PASS`; the review
plan and the four provenance files; the audit issue's checkboxes all at an
outcome; the coverage table's row count (543); the exit sweep's 35 rows;
**re-running `tools/pkgcheck` on the thirteen fork-own recipes, the three
install trees' `start_*.sh` lists, and the Q4 `behind-upstream` table's
`git log` once on an export of the tip made under `/workspace/tmp`**;
`register-check` on a simulated merge with the coordinator's tip; the
retro's four answers; the six exit codes. The lane posts one hand-back
comment naming the tip and each artifact by path, writes `reviewed-at:` and
`fixed-at:` into #677's body, then says it is idle. After acceptance the
coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the full lint, writes the hashes into
`slices.json`, merges the branch in its turn after the M7 candidate (after
T3's, with T3's; before T5's), regenerates the ledgers, files the tool
proposals the ladder named, and closes #677 when every `fix-guest-copy` row
is proven and every `fix-pending-image` row has its image. A brief that
needed the coordinator's help mid-slice beyond the stage-D pause and the
host relay is a defect in this brief: log the friction; the coordinator
fixes the template.

**The readings before dispatch** (plan § 3, principle 3): the epic's futro
(#798) gains a T30 kickoff addendum, and a stranger's proof of this brief
is run by a reader with no context; version 2 records what each found.
