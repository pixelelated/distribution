# Brief: M6.P2 T12, the VM harness (#659)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #659 differ, #659 wins and the
coordinator corrects the brief in the same session. **Version 1
(2026-10-24):** written after T9 (#656, the supervision tools) was accepted
at `bf4445a13c` and while T10 (#657, the guards) runs its streams in the
other lane; the tooling area's futro
(`docs/futros/2026-10-24-m6-tooling-and-guards.md`, posted on #903) carries
this slice's kickoff addendum. Every figure below was produced by a command
on the tree at `8ebaf8daad`, on P1's tip `2174265e9c` for the inventory, or
on this host today, and says which; a stranger's proof precedes the dispatch
and version 2 records what it found. **Each command block sets its own
variables** (`D`): a Bash call in this harness starts a fresh shell. **This
is a read of the fork's VM harness through the lens the order gives it, cost
against value**: every behaviour proof this fork makes runs through these
sixty files (`vm-first.md`), and the question of the slice is what each
suite, walk and measurement costs in minutes and host, what it has caught
(the record names it, blindspot by blindspot), what it would miss, and what
runs nowhere. **Nothing here builds, flashes, touches a handheld or a
person's cloud, or starts a guest the host file has not been told about**;
the no-guest controls run in the lane's worktree, and one bounded guest cycle
is authorized in § 5 for the claims only a guest can show.

## 1. Identity

- **Issue:** #659 `M6.P2 E903/T12: tooling-and-guards: the VM harness`,
  slice `tooling-vm-harness` (`k: 12`) in `docs/reviews/slices.json`,
  twelfth in `docs/reviews/order.md` (its row: *60 | 8,790 | 7,140 (7,140)
  | 0 | Independent*; its `why`: *every behaviour proof runs through it
  (`vm-first.md`); read before the code it proves under D-WORKFLOW-186*).
  **Epic:** #903 (the tooling and guards: T9 accepted, T10 running, then this
  slice, T14 #661, T15 #662, T45 #692). **Milestone:** M6; its body holds the
  live order; read it first. **Predecessors:** #346 (the plan), #641 (the
  survey, closed), **T9 #656** (accepted: `build-preflight` lists guests and
  stops nothing, D-INFRA-028 -- the harness's `vm-stop` is the one stopping
  path, and the guest census is read from `pgrep -c -x qemu-system-x86`),
  **T8 #655** (accepted: its S3 and S4 ran five GENERIC_X64 guest cycles on
  this host with the census, the pidfile and the host-file lines this brief
  asks for; its `02` is the model of a recorded cycle), **T1 #648** (the OS
  launch path, accepted; the exit hotkey the harness's `emulator-exit-test`
  drives is its subject), **T10 #657** (running beside this slice,
  D-WORKFLOW-190: `box-check` and `ceremony-check` are its; the two share no
  path). **Beside it:** T10.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, edit a rule or a decided register row, or decide a question of
  scope: those are the coordinator's, reached through #659, one question at
  a time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for every defect it finds (D-WORKFLOW-187). Nothing else.
- **One worktree, one session.** Branch `feature/m6-tooling-vm-harness-659`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-vm-harness-659`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the hashes are in the dispatch comment on #659). **Before that
  comment exists nothing runs in it.** The session is the T5 lane's
  (`m6-t5-build-engine`), which ran T5, T6, T7, T8 and T9; those worktrees
  stay beside this one, idle, until their merges, and nothing is written
  there. The primary checkout `/workspace/repos/pixelelated/distribution`
  stays on `next` (D-INFRA-025); the legacy checkout and `rocknix.worktrees/*`
  are the M7 lane's, read only. **The rules in this worktree are `next`'s
  except the paths the dispatch comment lists.**
- **Model and effort:** Opus 5.5 (the maintainer, 2026-10-22: *"the work
  will be Opus 5.5"*) at high effort. Record what ran in `00-running-log.md`'s
  header.
- **Review depth: Independent** (plan § 6c, `slices.json` k 12: *an ordinary
  code slice*): one reviewer from another lab through the Facilitator
  (`tools/council/run invoke --member gpt --provider openrouter`): **GPT-6
  Astra at `max`**, a probe first (identity, effort, provider from the
  provider's own field), then one refutation pass over one packet, as T9's
  Phase 4.6 did (its `second-opinions/` on
  `feature/m6-tooling-build-supervision-656` is the model: the brief, the
  probe prompt, the provenance files beside each output). `npm install
  --prefix tools/council`, `verify-pins` and `test` first; the key is
  `~/.config/council/env`, sourced by `run`, never read into a transcript. **A
  failed seat is a hold**, never a self-grading; a seat cut by its output
  ceiling re-runs on a trimmed packet (D-WORKFLOW-195). The packet is the
  slice's text -- the 30 scripts and the 27 text files, **484,627 bytes (473
  KiB) at the hash less the three PNG fixtures**, which are named with their
  sizes and sha256 instead of attached -- plus, as read-only context,
  `generic-x64-vm-testing.md` and `vm-first.md` (what the harness promises).
  The packet is scanned with `tools/forbidden-terms-check --stdin` and the
  pre-commit's patterns before it is sent (T10's rule; `qa-accounts` carries
  the *shape* of a credential handoff and no value, and the scan proves it).
  `review-plan.json` records depth `independent`, scope `epic`, primary
  `anthropic/claude-opus-5-5` / lab `anthropic`, one reviewer `gpt`
  (`openai/gpt-6-astra`, `openai`, `max`), provider `openrouter`,
  `allow_fallbacks: false`.
- **The host, read on 2026-10-24 by the coordinator:** M6's since M7's 17:09
  return; census qemu 0, compilers 0. The newest GENERIC_X64 images on the
  host are under `/workspace/artifacts/` (`x64-all-20261002-b2378d9c33`,
  `x64-all-20261001-d9493fe339`, `x64-webkit254-20260925-*`) and the M7
  lane's QA images under `/workspace/artifacts/rocknix-images/`; **the lane
  names the image file and its sha256 sidecar before any boot**, and reads
  its `RECORD.txt` for what it was. T8's guest cycles (`docs/qa-logs/` of
  2026-10-24 on `feature/m6-image-packages-655`) are the recorded shape:
  the host file line before, the pidfile under `/workspace/tmp/m6-t12/`,
  `tools/vm-stop` to end it, the census after, the disk retired
  (D-INFRA-022).

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-vm-harness-659
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-tooling-vm-harness-659
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: this is not the lane's worktree (stacked on P1): stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists, nothing else
cat .github/sessions/saved-session-state-feature-m6-tooling-vm-harness-659.md
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -c -x qemu-system-x86   # the host file's last lines and the census, before anything
df -i /tmp | tail -1                                                 # never export a tree under /tmp
mkdir -p .qa-scratch/t12/at-hash && tr '\n' '\0' < .qa-scratch/t12/paths.txt 2>/dev/null | xargs -0 git archive 8ebaf8daad 2>/dev/null | tar -x -C .qa-scratch/t12/at-hash 2>/dev/null || echo "run § 2's block first, then this export"
"$D/tools/rules-check" --quiet; echo "rc=$?"; "$D/tools/register-check" | tail -1
git push -u origin feature/m6-tooling-vm-harness-659
```

## 2. Scope

**60 paths, 8,790 lines; all 60 fork-own; 20 Python, 10 shell, 22 `.steps`
walk files (`other`), 3 text, 2 Markdown, 3 PNG fixtures (`image`); reach
`n/a` 60; 484,627 bytes at the hash.** The membership is the inventory's at
P1's `2174265e9c` with the slice's rule (`k: 12`): the area
`tooling-and-guards` and the one brace glob
`tools/{vm-*,vm-walks/**,frame-diff,time-to-play,emulator-exit-test,es-launch-memory,signin-memory,png-blackout,qa-accounts,ra-*,raofflineproxy-*,device-act,es-syntax-check,es-untranslated,font-stems}`.
**The glob is written out as names here because a naive glob-to-regex
misreads a brace list** (T10's brief met it). The re-derivation, in the
lane's worktree:

```bash
python3 -I - <<'PY'
import json, collections, os, fnmatch
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
names = "vm-*,vm-walks/**,frame-diff,time-to-play,emulator-exit-test,es-launch-memory,signin-memory,png-blackout,qa-accounts,ra-*,raofflineproxy-*,device-act,es-syntax-check,es-untranslated,font-stems".split(",")
def sel(p):
    if not p.startswith("tools/"): return False
    rest = p[6:]
    for n in names:
        if n.endswith("/**"):
            if rest.startswith(n[:-3] + "/"): return True
        elif "/" not in rest and fnmatch.fnmatchcase(rest, n): return True
    return False
t12 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "tooling-and-guards" and sel(r["path"])]
print("paths", len(t12), "lines", sum(r["lines"] or 0 for r in t12), dict(collections.Counter(r["tier"] for r in t12)), dict(collections.Counter(r["reach"] for r in t12)), dict(collections.Counter(r["language"] for r in t12)))
print("the glob also selects, in other areas:", sum(1 for r in rows if r["tree"] == "distribution" and sel(r["path"]) and r["area"] != "tooling-and-guards"), "paths (expect 0)")
os.makedirs(".qa-scratch/t12", exist_ok=True)
open(".qa-scratch/t12/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t12, key=lambda r: r["path"])))
PY
wc -l < .qa-scratch/t12/paths.txt                                                                        # 60
while IFS= read -r p; do printf '%6d %s\n' "$(git show 8ebaf8daad:"$p" | wc -l)" "$p"; done < .qa-scratch/t12/paths.txt | awk '{s+=$1; print} END {print s " lines"}'   # 8790 (the PNGs count 0)
```

Recorded (2026-10-24; the thirty scripts, by size; the last fork commit from
`git log -1 --format='%h %ad' --date=short 8ebaf8daad -- <path>`):

| Lines | Path | Last fork commit | What it is |
| ---: | --- | --- | --- |
| 1,593 | `tools/time-to-play` | `a4617bfd4a` 2026-10-02 | the two numbers a player feels, measured on one guest (D-CLOUD-098, #135); fails on a missing headline (`headline_missing`, blindspot 39, D-QA-022); `--vm` puts the guest in the state the image does not ship |
| 677 | `tools/vm-visual-qa` | `9faf3d5026` 2026-09-26 | drives a running guest through a `.steps` script and captures frames |
| 541 | `tools/vm-qa` | `fa444d60ff` 2026-10-11 | the runner: 17 suites (`scripts lifetime wrapper vocabulary register french quoting menumap pair-identity fresh round-trip exit time-to-play link ra-offline walks frame-diff`), two opt-in (`link`, `ra-offline`), one report; a suite that could not run is shown as such, never folded into PASS |
| 524 | `tools/ra-offline-test` | `63675be4e1` 2026-10-06 | the offline RetroAchievements scenario on a QA guest, end to end (#166); `--control` |
| 433 | `tools/frame-diff` | `9aaaaa0f64` 2026-10-15 | the walk frames against the last accepted cut's (#252): boxes, masks, claims |
| 247 | `tools/raofflineproxy-integration-test` | `9f170ee741` 2026-10-11 | the shipped preparation helper against an unpacked patched proxy (#361) |
| 230 | `tools/raofflineproxy-consent-test` | `e4276a6743` 2026-10-06 | installed reporting consent in an isolated guest with no default route |
| 227 | `tools/font-stems` | `eb131d112f` 2026-09-24 | how sharp a widget face renders per pixel size, on FreeType |
| 225 | `tools/ra-ui-test` | `63675be4e1` 2026-10-06 | installed reconnect cards with local fixtures and full-panel frames (#465) |
| 223 | `tools/ra-candidate-games` | `17f5a1e4ba` 2026-09-18 | which homebrew titles have cheap achievements; does a ROM carry its set |
| 196 | `tools/emulator-exit-test` | `82cecb6475` 2026-09-26 | the exit hotkey ends a game once, save written (`--vm`) |
| 185 | `tools/vm-pair` | `9f170ee741` 2026-10-11 | two guests from one image, for the tests that need two devices against one cloud (D-QA-009) |
| 170 | `tools/vm-upgrade-rehearsal` | `fa444d60ff` 2026-10-11 | the upgrade path rehearsed in a guest (`upgrade-and-install.md`) |
| 166 | `tools/es-launch-memory` | `939e73a1d4` 2026-10-03 | EmulationStation launch/exit memory on an owned guest (#310) |
| 159 | `tools/es-untranslated` | `196f823c60` 2026-09-25 | which fork strings have no French (the `french` suite; on the host, `ES_SRC`) |
| 159 | `tools/qa-accounts` | `4e11497aa7` 2026-09-14 | carry a QA account into a guest without printing it (D-QA-016) |
| 153 | `tools/es-syntax-check` | `eefc2f40f5` 2026-10-14 | one EmulationStation file compiled syntax-only with the image build's own command |
| 133 | `tools/vm-serial` | `74c0ff9ad5` 2026-09-06 | a root shell in a headless guest over its serial socket |
| 129 | `tools/signin-memory` | `134e89c4fc` 2026-10-03 | the cloud sign-in window's peak memory on a guest (#228, D-WORKFLOW-038) |
| 87 | `tools/vm-upgrade-readiness-test` | `9f170ee741` 2026-10-11 | the rehearsal's wait and guest query with disposable fixtures; **in the fork CI** |
| 81 | `tools/png-blackout` | `2c5d28eb55` 2026-09-22 | paint a rectangle of a frame black with the standard library |
| 77 | `tools/vm-stop` | `d97f64ddfd` 2026-10-05 | stop the exact owned QEMU by pidfile and disk, awaiting exit |
| 75 | `tools/vm-pair-test` | `fa444d60ff` 2026-10-11 | `vm-pair`'s launch functions with controlled failures (#545); **in the fork CI** |
| 70 | `tools/raofflineproxy-installed-native-test` | `aae3ebac1e` 2026-10-11 | upstream's format tests against the installed modules |
| 66 | `tools/vm-stop-test` | `d97f64ddfd` 2026-10-05 | delayed exit, timeout and wrong-owner controls (#454) |
| 44 | `tools/device-act` | `f7152d84a4` 2026-09-20 | **a command on a person's device**, recorded with the boot id: read only here, never run (D-QA-015) |
| 19 | `tools/vm-manager-system-check` | `d97f64ddfd` 2026-10-05 | refuse a manager walk whose system is absent or not selected |
| 3 | `tools/vm-walks/fixtures/system-selected.sh` | `9aaaaa0f64` 2026-10-15 (the walks directory) | a fixture |
| 165 | `tools/vm-walks/cloud-epic/migration-protocol.sh` | (the walks directory) | the cloud epic's protocol walk |
| 83 | `tools/vm-walks/cloud-epic/vnc-grab.py` | (the walks directory) | a frame grab over VNC |

**And the thirty text files of the walks:** `tools/vm-walks/suite.txt` (17
named walks), `claims.txt` (391 claim lines: every box a frame may change,
with its owner -- the `frame-diff` suite fails a box no claim covers),
`masks.txt` (7 masks), `README.md` and `docs/README.md`, 22 `.steps` files
(the walks `vm-visual-qa` replays: `run-transfer*`, `m7-cloud-sync`,
`m7-retro-achievements`, `manager`, `match-dialog`, `to-*`, `tick-*`,
`confirm-cloud-folder`, `restore-page`, `back-up-page`, `reset`, `wake`,
`ui-settings-toggle`, `continue-to-systems`, and `docs/*.steps` for the
rocknix.org pages), and three PNG fixtures (`gb-160x144.png`,
`nes-256x240-right.png`, `arcade-vertical-raw-left.png`: the display-aspect
proofs of #243). The last commit touching the directory is `9aaaaa0f64`
(2026-10-15, the claims for the browser frames).

**Provenance.** None of the 60 is on `upstream/next` (`git cat-file -e
upstream/next:<path>` fails for every one). `git log --format=%h
c445081a59..8ebaf8daad -- <the 60> | wc -l` is **145** fork commits since the
base (144 without merges); their messages cite #383 (12 times), #258 (7),
#344, #315, #307, #166 and #135 (6 each), #409, #361, #308, #228 and #125 (5
each) among others -- the harness's own record is #120 (the pair), #133 (the
five QA clouds), #135 (time to play), #166 (offline achievements), #228
(the sign-in window), #243 (display aspect), #252 (frame-diff), #310, #454,
#465, #545 (the launch-failure control).

**Who runs what.** `tools/vm-qa` is the one caller of most of the slice: its
17 suites call `es-untranslated` (`french`), `emulator-exit-test --vm`
(`exit`), `time-to-play --quick`, `ra-offline-test`, the `.steps` through
`vm-visual-qa` (`walks`), `frame-diff`, and `vm-pair` to bring the pair up
and down; `register`, `vocabulary`, `menumap`, `quoting`, `lifetime`,
`wrapper`, `scripts`, `pair-identity`, `fresh`, `round-trip`, `link` call
tools of other slices (`register-check`, `vocabulary-check`,
`es-menu-map-check`, the cloud suites) and the image. The fork CI runs two
of the 60 on every push of `next` (`fork-checks.yml:45-48`: `vm-pair-test`,
`vm-upgrade-readiness-test`). `release-candidates.md` step 3 names `vm-qa`,
`frame-diff`, `vm-upgrade-rehearsal` and `ra-offline-test`;
`generic-x64-vm-testing.md` is the owning rule and names almost all of them;
thirteen rules name `vm-qa`. **A tool nobody calls** -- not `vm-qa`, not the
CI, not a rule's instruction, not a skill -- is a Q6 row (the candidates the
coordinator's read suggests: `ra-candidate-games`, `font-stems`,
`png-blackout`, `es-launch-memory`, `signin-memory`, `vm-serial`,
`device-act`, `raofflineproxy-installed-native-test`; the lane decides each
from the record).

**The record the lens reads.** `docs/vm-qa-log.md` (361 lines, 5 entries
since 2026-10-15; the per-cycle ledger `generic-x64-vm-testing.md` names);
the `vm-qa` reports and `time-to-play.log`s under `docs/qa-logs/` (ten
folders carry them, e.g. `2026-10-08-pixelelated-replacement-18/qa21/`);
`docs/releases/catalog.md` for which cut each suite ran on; and the
blindspots that name these tools: **39** (a PASS over missing numbers), 40,
41 (`vm-pair`), 47, 49 (`es-syntax-check`'s origin), 50 (`ra-offline-test`),
54 (`font-stems`, `time-to-play`), 55, 56, 57, 59 (`signin-memory`), 61, 63,
65 (the proxy tests), 71, 74 (`time-to-play`) -- sixteen entries, which is
the value side of the lens.

**The hash.** The 60 are read at `8ebaf8daad`'s bytes from the export
(`.qa-scratch/t12/at-hash/`); `reviewed-at:` is the branch `HEAD` at stage A.
The lane's branch differs from the hash on **none of the 60** (P1's tip and
the coordinator's branch touch no harness file); `tr '\n' '\0' <
.qa-scratch/t12/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD --` is
empty, and a non-empty result is the first lead. T9's D-INFRA-028 changed
`tools/build-preflight` (not this slice's) to list guests with the
`tools/vm-stop` command; T10's S4 changed `fork-worktree`; neither is a
harness file.

**The policy on change (plan § 5; D-WORKFLOW-187):** a defect here is the
fork's alone and is fixed under a stream brief at stage E, never at stage B;
a stream on a tool with a control (`vm-pair-test`, `vm-stop-test`,
`vm-upgrade-readiness-test`, `vm-manager-system-check`) extends the control
with the case that fails on the unfixed tool; a stream on a tool without one
adds its control under `tools/` (a new fork tool joins the three lists,
D-WORKFLOW-045) or under `docs/qa-logs/<date>-<tool>/`; a change to what a
suite *measures* or *refuses* (`time-to-play`'s headline rule, `frame-diff`'s
claims contract, `vm-qa`'s PASS/SKIP accounting) is a lead for the
coordinator (D-QA-022, D-QA-040, #252's contract), not a stream. **Cost
against value is the lens, not a licence to delete**: a suite the record
shows catching nothing is reported with its minutes and its last catch, and
the coordinator decides its fate with the maintainer (D-QA-040's cadences
are the open row).

## 3. Read first

- **The rules the work touches**, from `next`, this session
  (`working-principles.md` § Pre-flight): `generic-x64-vm-testing.md` (the
  owning rule: the harness, the keys, the headless recipe, *what the guest's
  busybox lacks*, *after every VM cycle*, the crash and hang recipes),
  `vm-first.md` (the question every proof answers first; *what the VM has*),
  `time-to-play.md` (D-CLOUD-098/119/122: the two numbers and the one budget),
  `upgrade-and-install.md` (the rehearsal), `release-candidates.md` step 3
  (what runs on a candidate), `engineering-practices.md` (§ Guards must fail
  closed: *a suite is not wired in until it has been seen to FAIL once*, the
  time-to-play case; § Nothing runs on a person's device; § If the VM can test
  it), `es-ui-style-guide.md` § Keep the flow and its visual evidence
  together (the walks and `frame-diff` as evidence), `worktrees.md` § One
  builder per build worktree (the guests are per host), `device-builds.md`
  (the memory the guests hold before a build), `decision-register.md`,
  `learning-capture.md`.
- **The registers for the scope:** D-QA-007/015/017 (the VM first; a
  person's device), D-QA-009 (conflict testing on the pair), D-QA-016 (the
  QA accounts), D-QA-022 (a tool that reports numbers fails when they are
  missing), D-QA-040 (open: the cadences), D-QA-043/044 (a frame at the
  panel's size as the observation; agent-first criteria), D-QA-058 (the local
  cloud baseline), D-CLOUD-098/112/113/119/122 (time to play, the offline
  benchmark, the two contracts, the exit-sync budget, the open rows),
  D-INFRA-021/022 (retain the record, retire the payload), D-WORKFLOW-038
  (`signin-memory` decided the webkitgtk bump), D-WORKFLOW-155/156 (the
  evidence index beside reviewed frames), D-UI-039 (the menu map and
  `menumap`). **Blindspots:** the sixteen named in § 2, and the class 8, 13,
  14, 22 (a probe that cannot report absence), 26, 34 (the guest's busybox).
- **The guards' recorded positives** (`engineering-practices.md` § The
  positive is recorded where the guard is wired): `time-to-play`'s
  `headline_missing` (2026-09-1x, blindspot 39: the first PASS over `-`
  cells), `frame-diff`'s uncovered box (#252's first run), `vm-qa`'s SKIP
  accounting (`SKIPS=0 -- a suite that could not run (rc 3) is shown as
  such`), `vm-pair-test` and `vm-stop-test` (their own cases), the walks'
  claims (`claims.txt`'s owners). A suite whose positive the lane cannot find
  in the record is a Q6 row saying so.
- **The two leads already on #659 or near it:** none from T4; from T8's and
  T9's reads: the guest census by `pgrep -f` (T9's F-03, fixed in
  `build-preflight`) -- hunt the same shape in `vm-qa`, `vm-pair`, `vm-stop`,
  `time-to-play`, `ra-offline-test` (how each finds, waits for and stops a
  QEMU: by pidfile and owned disk, or by pattern?); the `/tmp` roots
  (`/tmp/rocknix-qemu-monitor-*.sock`, `/tmp/ttp`) against the inode
  exhaustion of 2026-10-24 07:1x (the host file; a tool that exports a tree
  or writes frames under `/tmp` is a Q2 row).
- **The evidence folders**: T8's `docs/qa-logs/` of 2026-10-24 on its branch
  (five recorded guest cycles: the shape), `docs/vm-qa-log.md`, the ten
  `docs/qa-logs/` folders with `vm-qa` reports, `docs/releases/catalog.md`.
- **The stranger's proof of this brief** (version 2's errata).

## 4. The questions

All seven apply (plan § 4); **the lens is cost against value, so Q5
(efficiency: minutes and host per suite) and Q6 (brittleness and dead ends:
what each suite has caught, what nobody runs) carry the slice**, Q3 the
fail-open shapes in a harness whose job is to fail loudly, Q7 the three
descriptions of each tool (header, rule, index) against the code.

| Q | What is asked of these 60 | Where the answer lands |
| --- | --- | --- |
| Q1 Modernize | A tool that reads a layout or a path the tree has retired (`../rocknix.worktrees/`, `/workspace/repos/rocknix`, the legacy build roots: #640's rows); a `/tmp` root; a QEMU or Python construct the host no longer has; the image names the tools expect against what `/workspace/artifacts/` holds | the rows; #640 named, not changed |
| Q2 Standards | Fail-closed shapes: a count asserted, a missing number a FAIL, a guest found and stopped by pidfile and owned disk never by pattern (CLAUDE.md), `pipefail`, every expansion quoted, exits defined where named, nothing credential-shaped printed (`qa-accounts`'s contract) | a finding per violation, with the line |
| Q3 Bugs | **A proof that can pass without proving**: a suite whose rc 0 does not depend on the thing it measures (the blindspot-39 shape, hunted through every suite: `exit`, `walks`, `frame-diff`, `round-trip`'s call, `ra-offline`, `link`, `fresh`, `pair-identity`); a wait that cannot time out; a frame compared against itself; a claim in `claims.txt` that covers more than its owner meant; a guest the harness loses (the pidfile written after the launch, a stop that does not wait); a kill by pattern | a `bug` per defect, `Already written:` and the VM line, its fix under a stream with a case |
| Q4 Currency | Not a package slice. The row is the QEMU and Python the tools assume against the host's (`qemu-system-x86_64 --version`, `python3 --version`), and the image versions the record ran against the newest image available | one table |
| Q5 Efficiency | **The cost side of the lens:** for each of the 17 suites and each standalone measurement, the minutes it takes (from the record's reports and logs: `vm-qa`'s `started`/finished lines, `time-to-play.log`, the five cycles of 2026-10-24), the host it holds (guests, RAM, disk under `/workspace/tmp`), and what runs on every candidate against what is opt-in; the walks' 22 step files by frames captured | the figures with their source, one table |
| Q6 Dead ends and brittleness | **The value side of the lens:** for each suite, measurement and walk, what it has caught -- the blindspot or issue that names it, the cut it failed (`docs/releases/catalog.md`, `docs/vm-qa-log.md`) -- or **nothing recorded**, which is a finding; **a tool nothing runs** (the eight candidates in § 2, each confirmed or refuted from `vm-qa`, the CI, the rules and the skills); a walk no claim owns or a claim no walk exercises (`claims.txt` 391 lines against `suite.txt`'s 17 and the 22 step files); a fixture nothing reads | the table in `04` § Q6, every row sourced |
| Q7 Clarity | The three descriptions of each tool (its header, `generic-x64-vm-testing.md`'s sentence, `instruction-files.md`'s index row) against the code; `vm-qa`'s header list of suites against `SUITES`; `release-candidates.md` step 3 against what `vm-qa` runs by default | the rows; a drift in a rule is a lead for the coordinator |

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor):

1. Tracker state is never sole evidence: every verdict cites the tree
   (`git grep`, `git log`), a control's run with its exit, a recorded report
   (`docs/qa-logs/`, `docs/vm-qa-log.md`), or a guest cycle's own record.
2. Mechanical evidence outranks reading: a suite's behaviour is its run and
   its exit, not the comment above it.
3. **The bench is the host and one bounded guest cycle.** The no-guest
   controls run in the lane's worktree; a GENERIC_X64 guest is the bench for
   a behaviour claim about the harness itself (how `vm-qa` accounts a suite
   that cannot run, what `vm-stop` waits for, what a walk's frames are), and
   **one cycle is authorized here**: the newest local GENERIC_X64 image named
   with its sha256 and `RECORD.txt`, one guest (two if a claim needs the pair,
   said first), the host file line before (`== M6 T12 lane (#659) -- <UTC>:
   census qemu N; one GENERIC_X64 guest from <image>, pidfile
   /workspace/tmp/m6-t12/qemu.pid, <what runs>`), `generic-x64-vm run
   --headless --daemonize` as `generic-x64-vm-testing.md` gives it, `vm-qa
   --skip-up --only <the suites the cost table needs>` (the full default run
   is not required; `link` and `ra-offline` stay opt-in and are not run),
   `tools/vm-stop` by the pidfile to end it, the census after, the host file
   line after, the disk and frames retired after their compact record
   (D-INFRA-022) with the frames the claims need kept under the audit folder.
   **A second cycle needs a line on #659 first.** **No handheld, no person's
   cloud** (`device-act` is read, never run; `qa-accounts` is read, never run
   against a real account); the QA clouds are `tools/cloud-test-backend`'s
   local ones (D-QA-058), brought up by the lane if a suite needs one.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.

**The no-guest controls, with the baseline the coordinator read on
2026-10-24** (the lane runs each at stage A in its worktree and records the
exit; a control that fails is a finding):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-vm-harness-659
cd "$D"
python3 -I tools/vm-pair-test; echo "rc=$?"                                      # the fork CI runs it (fork-checks.yml:47)
python3 -I tools/vm-upgrade-readiness-test; echo "rc=$?"                         # the fork CI runs it (:48)
python3 -I tools/vm-stop-test; echo "rc=$?"                                      # #454's three controls
python3 -I tools/vm-manager-system-check --help 2>&1 | head -3                   # its modes; it reads a guest, so a run waits for the cycle
python3 -I tools/raofflineproxy-integration-test --help 2>&1 | head -3           # needs the unpacked proxy from a build root: read what it needs, run only if present
tools/vm-qa --list                                                               # the 17 suite names
tools/time-to-play --help 2>&1 | head -5; tools/frame-diff --help 2>&1 | head -5 # the modes; frame-diff runs on recorded frames without a guest
tools/vm-visual-qa --help 2>&1 | head -5; tools/vm-pair 2>&1 | head -3           # the usage lines, nothing started
tools/es-syntax-check 2>&1 | head -3                                             # exits 2 without a build root: that is not a pass (es-native-ui.md)
grep -nE 'pgrep|pkill|kill ' tools/vm-qa tools/vm-pair tools/vm-stop tools/time-to-play tools/ra-offline-test tools/emulator-exit-test tools/es-launch-memory tools/signin-memory | cut -c1-140   # Q2/Q3: how each finds and stops a guest
grep -nE '/tmp/' $(tr '\n' ' ' < .qa-scratch/t12/paths.txt) 2>/dev/null | cut -c1-120 | head -40   # Q1/Q2: the /tmp roots
```

**The reading, per file:** every suite of `vm-qa` matched to its tool, its
record and its positive (Q6's table); every QEMU find/wait/stop path read for
pidfile-and-disk against pattern (Q2/Q3); `claims.txt` reconciled with
`suite.txt` and the 22 step files; the ten recorded reports read for minutes
and verdicts (Q5); the eight no-caller candidates confirmed or refuted; the
three descriptions per tool (Q7).

**The seat (Phase 4.6, one seat):** `npm install --prefix tools/council`,
`tools/council/run verify-pins`, `tools/council/run test`; the packet
(`gpt-brief.md`: the 57 text files and the two rule sections, the three PNGs
named with sizes and sha256; `packet-manifest.json` with the sha256 of each)
**scanned before it is sent** (`tools/forbidden-terms-check --stdin` 0 hits;
the pre-commit's patterns 0 lines); the probe (`gpt-probe.md` with its
`.provenance.json`); the refutation (`gpt-audit.md` with its
`.provenance.json`), the seat asked first for `vm-qa`'s accounting,
`time-to-play`'s headline rule, `frame-diff`'s claims and `vm-stop`'s wait;
each item graded in `04` § Second opinion with the artifact that decided it;
a seat cut by its ceiling re-runs on a trimmed packet (D-WORKFLOW-195). The
call runs plainly with a harness waiter (T5's retro: `watch-build
--record-only` holds the worktree's lock).

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#659`
(`Refs #659`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-tooling-vm-harness/00-running-log.md` | the flight recorder: the model and effort, `reviewed-at` with `8ebaf8daad` beside it, the host file's last line and the census before each run, every § 5 command with its exit status, every `PROOF:` line, the guest cycle's lines (image, sha256, pidfile, start, stop, census after, retired), each time from `date -u` | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 60 re-derived with § 2's block and its output, the provenance (145 fork commits, none upstream), the branch's diff from the hash (empty); § Phase 1: what each suite and tool does, in the slice's words, and the no-guest controls' baseline with exits | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #659's checklist, plus **a coverage table with one row per path** (60; the first cell the path in backticks so ``grep -c -E '^\| `tools/'`` counts them), § Mechanical checks, § The controls (each run, its exit, *a FAIL would mean ...*), § The guest cycle (the record of the one cycle, or that none was needed and why), § The record (the ten reports read, with minutes); every proof with a `proved:` cell | B, then F |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: `vm-qa` x the cloud suites x the image; `frame-diff` x `claims.txt` x the walks x the menu map; `time-to-play` x the exit sync's budget (D-CLOUD-119); the pair x the host's memory (`device-builds.md`); the harness x the M7 lane's guests (the host file) | B |
| Analysis | `.../04-analysis.md` | Phase 4, § Finding Verification (4.5), § Second opinion (4.6), **§ Renovation face** Q1 to Q7, **Q5 carrying the cost table and Q6 the value table** (every suite with its minutes, its host, its last catch or `nothing recorded`, its caller or `nobody`) | C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (independent; `gpt` at `max`), the brief, `packet-manifest.json`, the probe prompt, the probe and the refutation with their `.provenance.json` | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (...)` with `review plan: independent, 2 model perspectives, 1 verified external calls` | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category, where (file:line at the hash), acceptance, `Already written:` and the VM line; the YAML `punch_index`; a suite with nothing recorded as a `Renovation` item with the coordinator's disposition pending; a tool nobody runs the same | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #659 | `Audit: M6 T12 the VM harness -- N findings (...)`; one checkbox per item, agent-first | D |
| Bugs | GitHub, label `bug`, milestone M6 | one per defect, with its code trace, `Already written:`, the VM line and the case that will prove the fix | D |
| Streams | the coordinator's brief `docs/reviews/briefs/t12-streams.md` | one per fix the coordinator briefs at the stage-D pause | E |
| Retro | `docs/retros/<date>-m6-tooling-vm-harness.md`, posted on #659 | the mini-retro, Instruction-Recommendations mode; what the slice did to the two time-to-play numbers (nothing, unless a stream changed the measurement -- then the before and after) | G |

## 7. Acceptance

The checklist on #659 becomes this section at dispatch, written there by the
coordinator in place of P1's five generated ones (until then #659 carries
those five). Every checkbox names the artifact that ticks it (D-QA-044); the
coordinator ticks at acceptance, from the artifacts, never from the
hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-tooling-vm-harness/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-tooling-vm-harness/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included: Q1 to Q7 answered in `04-analysis.md`, and every punch item's `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: independent`, one reviewer (`gpt`, `openai/gpt-6-astra`, `max`), and the probe and refutation outputs have a `.provenance.json` beside them whose served model is the seat's and whose verification is PASS; `packet-manifest.json` lists the 57 text files with their sha256 and the three PNGs by name, size and sha256, and `02` records the packet's own scan (`forbidden-terms-check --stdin` 0 hits, the credential patterns 0 lines) before it was sent.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (#640 for a legacy path; a `bug` for a defect; the coordinator's lead for a measurement or contract change, a suite with nothing recorded, or a tool nobody runs), or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits the read and the fixes were made at (the read on `8ebaf8daad`'s bytes for the 60; no EmulationStation path), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed`.
- [ ] `01-research-notes.md` § Scope records the read hash, the filter of brief § 2 with its output (60 paths, 8,790 lines; 60 fork-own; 20 Python, 10 shell, 22 `.steps`, 3 text, 2 Markdown, 3 PNG; reach `n/a` 60, or the deltas beside them), the provenance (145 fork commits since `c445081a59`; none on `upstream/next`), and the branch-vs-hash diff over the 60 (empty, or each hunk listed with its owner).
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c -E '^\| `tools/' 02-forward-audit.md`` prints 60; each row's Q1 to Q7 cells answered or `n/a` with a reason (a `.steps` file or a PNG answers Q6 and Q7 at least: who replays or reads it, and what claims it).
- [ ] `02-forward-audit.md` § The controls records every § 5 run with command, exit status and summary line, each with the sentence *a FAIL would mean ...*: `vm-pair-test`, `vm-upgrade-readiness-test`, `vm-stop-test` rc 0; `vm-qa --list` printing 17 names; the usage lines; `es-syntax-check` without a build root exiting 2 and recorded as not a pass; the QEMU find/stop grep and the `/tmp` grep with their lines.
- [ ] `02-forward-audit.md` § The guest cycle records the one authorized cycle (the image file and its sha256 and `RECORD.txt` line, the host file line before and after, the pidfile, the `vm-qa --skip-up --only <suites>` command with its report's summary and minutes per suite, `tools/vm-stop`'s exit, the census after, the disk and frames retired with the kept frames named) -- or records that no cycle was needed, with the claims that would have needed one listed and marked `proved: tree`.
- [ ] `00-running-log.md` shows no handheld action, no run of `device-act` or `qa-accounts` against anything real, no guest beyond the one cycle (a second only with a line on #659 quoted), no `link` or `ra-offline` suite, no build, no `fork-worktree sync|remove|repair`, no write under the M7 lane's trees, and the host file's lines before and after the cycle quoted.
- [ ] `04-analysis.md` § Renovation face Q5 carries the cost table: one row per `vm-qa` suite (17) and per standalone measurement (`time-to-play`, `signin-memory`, `es-launch-memory`, `vm-upgrade-rehearsal`, `ra-ui-test`, the two `raofflineproxy-*` guest tests), each with minutes (from the record's reports or the cycle), the host it holds, and whether it runs on every candidate, opt-in, or nowhere.
- [ ] `04-analysis.md` § Q6 carries the value table: one row per suite, measurement, walk (17) and fixture, each with its last recorded catch (the blindspot, issue or failed cut, by number and date) or `nothing recorded`, its recorded positive or `none`, and its caller (`vm-qa`, the CI, a rule, a skill) or `nobody`; `claims.txt`'s 391 lines reconciled against `suite.txt`'s 17 walks and the 22 step files (a claim no walk exercises and a walk no claim owns each listed).
- [ ] `04-analysis.md` § Q3 hunts the pass-without-proving shape through every suite by name (the eight § 4 lists and the rest), each with the line read and a constructed input that would pass wrongly or the statement that none can; and the find/wait/stop path of every tool that touches a QEMU, each classified pidfile-and-disk or pattern.
- [ ] `04-analysis.md` § Q7 reads each tool's three descriptions (header, `generic-x64-vm-testing.md`, the index) against the code, `vm-qa`'s header suite list against `SUITES`, and `release-candidates.md` step 3 against the default run, with each drift a Q7 row or a Q3 bug; a rule drift is a lead for the coordinator, not an edit here.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `guest` (a claim the cycle showed, with its frame or log named), `fix-tree`, `fix-case` (a fix proved by a control's new case that failed on the unfixed tool) or `fix-guest`; ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c '^PROOF:' 00-running-log.md``.
- [ ] Every punch item carries `question:`; every `bug` this lane files passes `tools/box-check --issue N`; no file under `tools/` is changed on this branch before a stream brief (`git diff --stat <the lane tip the dispatch comment names> <fixed-at> -- tools` is empty, or every hunk is a stream the coordinator briefed), and a stream on a tool records in `02` the control case that failed on the unfixed tool and passes on the fixed one.
- [ ] The retro exists at `docs/retros/<date>-m6-tooling-vm-harness.md`, is posted on #659, and says what the slice did to the two time-to-play numbers (nothing, or the measurement change named with its before and after).
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's branch is merged into it at hand-back, if a row cited lives there), and `tools/lint-audit-artifacts` prints `PASS` on the folder, each exit code in the hand-back comment.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #659; a blocker named on #659 with what is needed (the seat failed, no
GENERIC_X64 image on the host whose `RECORD.txt` the lane can read, a
control that cannot run for a reason outside the tree, two commands that
disagree); a branch that differs from `8ebaf8daad` on one of the 60 at
stage A; or an execution limit, stated as such with the running log
current. A checkpoint is not a stop; a differing count is a delta; `next`
moving is drift. An idle session says it is idle on #659, **and does not end
a turn on a post that asks nothing**.

**What never runs in this slice:** a handheld action of any kind
(`device-act`, `scp` to a device, a reboot, a launch; D-QA-015);
`qa-accounts` against a real account, or any read of a credential file
(`~/.config/council/env`, `~/.ROCKNIX/options`, `~/.config/rocknix/forbidden-terms`,
the QA accounts' store); a push to any branch but the lane's own; a second
guest cycle without a line on #659; the `link` or `ra-offline` suites; a
guest found or stopped by pattern (`pkill`, `kill $(pgrep ...)`): the
pidfile and `tools/vm-stop` only; a build; `fork-worktree sync|remove|repair`;
a write under `/workspace/repos/rocknix*`; a frame or a tree exported under
`/tmp` (use `/workspace/tmp/m6-t12/`); an edit to a rule, `CLAUDE.md`,
`AGENTS.md`, a decided register row, `docs/es-menu-map.md` or
`.github/sessions/saved-session-state-next.md`; a change to what a suite
measures or refuses outside a stream brief; `--no-verify`; bare `git stash`;
`git worktree remove --force` or `rm -rf` on a worktree.

## 9. Ceremonies owed

- A work-log entry per session headed `#659`, its time from `date -u` in
  the same command, its prose through a quoted heredoc or the Write tool;
  `tools/work-log-index --write` after it (in this worktree only).
- A friction line the moment something slows, with `issue: #659` or the
  guard.
- The VM question written before any proof (§ 5: the no-guest controls on
  the host; one authorized guest cycle for the harness's own behaviour
  claims; nothing on a device).
- The cycle's own ritual (`generic-x64-vm-testing.md` § After every VM
  cycle): an entry in `docs/vm-qa-log.md` for the cycle, with the image, the
  suites run, the minutes and the verdicts.
- The mini-retro at stage G, posted on #659, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator (D-WORKFLOW-189).
- A register row the same session for any decision the slice forces; the
  next Decided ID is checked on every pushed branch at the time (on
  2026-10-24 the highest Decided rows are D-WORKFLOW-202 and D-INFRA-030,
  the coordinator's; T10 runs beside this lane and may take 203); it goes at
  the end of `## Decided`, and a row is never edited.
- The merge notes: when `next` moves, the **coordinator** merges `next` into
  this branch, never between stage A and stage D; the coordinator merges its
  own branch into this one at hand-back before criterion 17's checkers run
  (as for T9 and T10); a merge with conflicts is checked for leftover
  markers before it is committed (#696), and the ledgers are united by whole
  entries.
- Commit messages `docs: ...` for the audit, `<tool>: ...` for a stream's
  fix, each with `Refs #659` and the attribution line; `git add -A` only
  after `git status --short` shows nothing a control left behind
  (`.qa-scratch/` is gitignored; frames the claims need go under the audit
  folder deliberately, the rest retired).

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#659's checkboxes against their artifacts; the lint's `PASS` line; the
seat's `review-plan.json` and provenance (served model, provider, effort,
verification) and the packet's recorded scan; the audit issue's checkboxes
all at an outcome (the ticked and open counts read by name); the coverage
table's row count (60), the cost table's and the value table's rows against
§ 7; **re-running on an export of the tip under `/workspace/tmp`: the
membership block, the file list with line counts, `vm-pair-test`,
`vm-upgrade-readiness-test`, `vm-stop-test`, `vm-qa --list`**; the guest
cycle's record read (host file lines, pidfile, census, retirement) and the
host checked for a guest or a payload left behind; `register-check` and
`rules-check` on a simulated merge with the coordinator's tip (the ledgers
united); the retro's four answers; the six exit codes. The lane posts one
hand-back comment naming the tip and each artifact by path, writes
`reviewed-at:` and `fixed-at:` into #659's body, then says it is idle. After
acceptance the coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the full lint, merges the branch in its turn
after the M7 candidate (after T10's, before T4's), regenerates the ledgers,
and closes #659 when every row is proven.

**The readings before dispatch** (plan § 3, principle 3): the area's futro
(#903) carries this slice's kickoff addendum, and a stranger's proof of this
brief is run by a reader with no context before dispatch; version 2 records
what each found.
