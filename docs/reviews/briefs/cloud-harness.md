---
slice: T13
id: cloud-harness
issue: "#660"
epic: "#1047"
area: cloud-sync-and-saves
kind: read
lens: brittleness
depth: Independent
version: 1
written: 2026-10-25
author: the M6 coordinator (Fable 5.1, D-WORKFLOW-189)
read_refs:
  distribution: 8ebaf8daad
  p1: 2174265e9c
---

# T13: the cloud test harness (a brittleness read of the nine tools that prove the cloud)

**Version 1, 2026-10-25, by the coordinator.** A brief for a lane that has
never seen this project, in the shape of T14's
(`docs/reviews/briefs/tooling-state-tests.md`, the state tests: an
Independent read of tests, with a seat) for **the nine fork-own tools under
`tools/cloud-*` that prove the cloud slices**. The order's § T13
(`docs/reviews/order.md`, P1's `2174265e9c`) is the slice's definition; this
brief is the work. Its lens is brittleness, and its origin is blindspot 31:
*a harness that agrees with itself*. The question every row of this slice
answers is **what a PASS from this tool certifies, by what oracle, and what
would have made it FAIL** -- because T16 and T17, the two Extended slices
after it, close on this harness's verdicts. Every figure here was produced
by a command run at the hash named beside it (the read-only research notes
behind § 2 carry each command); a stranger's proof precedes dispatch, and
version 2 records what it found.

## 1. Identity

- **Issue:** #660 `M6.P2 E1047/T13: cloud-sync-and-saves: the cloud test
  harness`, slice `cloud-harness` (`k: 13`) in `docs/reviews/slices.json`,
  thirteenth in `docs/reviews/order.md` (its row: *9 | 10,165 | 10,165
  (10,165) | 0 | Independent*; its `why`: *`tools/cloud-round-trip` (7,808
  lines) and the backends that prove the cloud slices; a harness that agrees
  with itself is blindspot 31; read before the code it proves under
  D-WORKFLOW-186*). **Epic:** #1047 (cloud sync and saves: T13, then T16 and
  T17 at Extended depth; this slice is the area's first, and the epic's
  criterion says T16 is not dispatched until this slice's assertion-shape
  table exists). Its futro is `docs/futros/2026-10-25-m6-cloud-sync-and-saves.md`.
  **Milestone:** M6; its body holds the live order; read it first.
  **Predecessors that bear on these files:** **T12** (#659, the VM harness,
  accepted: `vm-qa`, `vm-pair`, `vm-serial`, `vm-visual-qa` -- the guests
  and the walks `cloud-round-trip` drives; `vm-visual-qa` is under an open
  bug, #972, and `cloud-round-trip` imports it as a module); **T14** (#661,
  the state tests, accepted: `settings-modes-test` and the busybox rule --
  a test that runs the device's scripts runs them under the image's busybox
  or says whose tools judged, D-QA-063); **T15** (#662, at stage E:
  `last-good-scripts-test` carries 55 lines naming `cloud_migrate_layout`,
  guarded by existence, and the stale-name check of blindspot 71 was
  re-pointed at that script before it was deleted -- a lead this slice hands
  back, not fixes); **T10** (#657: the push guard's credential patterns, the
  shape every packet is scanned against). **The rule:**
  `rclone-cloud-sync.md` (895 lines), **under the open drift bug #909** (five
  stale rclone facts, one of them this slice's: the rule says the no-network
  step asserts exit-4 timing; the tool asserts exit 69 at lines 1460-1470),
  and whose `paths:` names three of the nine tools (`cloud-round-trip`,
  `cloud-test-backend`, `cloud-census`): opening the other six loads no rule.
  **The policy:** D-QA-058 (local WebDAV, SFTP and MinIO/S3 are the standing
  cloud baseline; no hosted account is a prerequisite), D-CLOUD-181 (an
  integrity verifier binds manifests before and after; a lossy filter is not
  an inventory), D-QA-015 and `vm-first.md` (nothing runs on a person's
  device or cloud), D-WORKFLOW-186 (the harness is weighed ahead of any
  device target). **Beside it:** T15 in the T3 session and T23 in the T5
  session, on different file sets (D-WORKFLOW-190).
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, edit a rule or a decided register row, or decide a question of
  scope: those are the coordinator's, reached through #660, one question at
  a time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves (D-WORKFLOW-187). **A fix to one of
  the nine is stage E's**, under a stream brief the coordinator writes after
  the stage-D pause (the tools are the fork's own, so a defect here is ours
  to fix); at stages A to D the lane changes no file under `tools/`.
- **One worktree, one session.** Branch `feature/m6-cloud-harness-660` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-harness-660`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the hashes are in the dispatch comment on #660). **Before that
  comment exists nothing runs in it.** The session is the T1 lane's
  (`m6-t1-os-launch`), which ran T1 and the #1012 packet; the T1 and
  `m6-1012-ttp-runner` worktrees stay beside this one, idle, until their
  merges, and nothing is written there. The primary checkout stays on
  `next` (D-INFRA-025); the legacy checkout and `rocknix.worktrees/*` are the
  M7 lane's, read only. **The rules in this worktree are `next`'s except the
  paths the dispatch comment lists.**
- **Model and effort:** Opus 5.5 (the maintainer, 2026-10-22: *"the work
  will be Opus 5.5"*) at high effort. Record what ran in `00-running-log.md`'s
  header.
- **Review depth: Independent** (plan § 6c, `slices.json` k 13: *an ordinary
  code slice*): one reviewer from another lab through the Facilitator
  (`tools/council/run invoke --member gpt --provider openrouter`): **GPT-6
  Astra at `max`**, a probe first (identity, effort, provider from the
  provider's own field), then one refutation pass over one packet, as T9's,
  T12's and T14's Phase 4.6 did (T14's `second-opinions/` on
  `feature/m6-tooling-state-tests-661` is the model). `npm install --prefix
  tools/council`, `verify-pins` and `test` first; the key is
  `~/.config/council/env`, sourced by `run` for this one call, never read
  into a transcript (every other `tools/council/run` call carries
  `COUNCIL_ENV_FILE=/nonexistent`). The Facilitator on this branch is the
  local `council-facilitator@1.14.1-pixelelated.2` (#636/#638; T45's F-01,
  Backlog #1045) and the record says so. **A failed seat is a hold**, never
  a self-grading; a seat cut by its output ceiling re-runs on a trimmed
  packet (D-WORKFLOW-195). The packet is the slice's nine files, **594,115
  bytes (580 KiB) at the read refs**, plus, as read-only context,
  `rclone-cloud-sync.md` § "Testing it without a cloud account" and § "Five
  backends", and blindspot 31's entry. **The packet is scanned before it is
  sent** (`tools/forbidden-terms-check --stdin` 0 hits; the pre-commit's
  patterns 0 lines): `cloud-test-backend` writes an sshd host key, runs
  `rclone obscure` and composes connection strings, so the scan decides
  whether a line is carried or redacted as T14's PL-012 did.
  `review-plan.json` records depth `independent`, scope `epic`, primary
  `anthropic/claude-opus-5-5` / lab `anthropic`, one reviewer `gpt`
  (`openai/gpt-6-astra`, `openai`, `max`), provider `openrouter`,
  `allow_fallbacks: false`.
- **The host, read on 2026-10-25 by the coordinator:** M6's; the M7 lane
  holds a component-qualification window (guests one at a time, its own) and
  has said a full GENERIC/H700/SM8550 build window follows. **This slice's
  stage A is host-only** (§ 5): the four bare tests, the backends' `up`,
  `ls`, `down` for WebDAV and SFTP (host processes) and S3 (a MinIO
  container; `docker` is usable by this user), `cloud-round-trip --list`
  with no device. **The one guest cycle this slice needs -- the single-device
  suite of `cloud-round-trip` over WebDAV and SFTP on one GENERIC_X64 guest,
  about two minutes, plus the CAP cells by hand -- runs only in a window the
  coordinator grants on #660**, after the M7 lane's FINAL RETURN of its
  current window (the standing rule: both M6 guest cycles are held behind
  it); the lane asks for it at the end of stage A with what it will run and
  how long, and does stage B's reading meanwhile. `rclone` 1.60.1-DEV,
  `sshd`, `ssh-keygen`, `python3` and `docker` are present on the host;
  `xmlstarlet` is not (T23's #1053, not this slice's). Register: the three
  workflow IDs before 209 are the M7 lane's, 209 the coordinator's; a row
  this slice forces takes **D-WORKFLOW-210 or higher**, D-QA-064,
  D-INFRA-032.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-harness-660
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-cloud-harness-660
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists
cat .github/sessions/saved-session-state-feature-m6-cloud-harness-660.md         # seeded by the dispatch
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
df -i /tmp | tail -1                                                 # never export a tree under /tmp
git diff --stat 8ebaf8daad HEAD -- tools/cloud-round-trip tools/cloud-test-backend tools/cloud-connections-test tools/cloud-census tools/cloud-pair-migration tools/cloud-save-integrity tools/cloud-input-test tools/cloud-capture-stamp-test tools/cloud-save-integrity-test | tail -1   # empty
gh issue view 909 --repo pixelelated/distribution --json state,title --jq '"\(.state) \(.title)"'   # the rule's drift bug, open
"$D/tools/rules-check" --quiet; echo "rc=$?"; "$D/tools/register-check" | tail -1
git push -u origin feature/m6-cloud-harness-660
```

## 2. Scope

**Nine paths, 10,165 lines (the inventory's column); all nine fork-own; reach
`n/a` 9; 6 Python, 3 shell; 108 fork commits since the base `c445081a59`,
none on `upstream/next`; byte-equal between `8ebaf8daad` and the coordinator's
tip.** The membership is the inventory's rows in area `cloud-sync-and-saves`
under `tools/**` (`slices.json` k 13; the area's glob `tools/cloud-*` in
`areas.json`). The block, at `2174265e9c`:

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
t=[r for r in rows if r["tree"]=="distribution" and r["area"]=="cloud-sync-and-saves" and r["path"].startswith("tools/")]
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t), dict(collections.Counter(r["tier"] for r in t)), dict(collections.Counter(r["language"] for r in t)), dict(collections.Counter(r["reach"] for r in t)))
[print(" ",r["path"],r["lines"],r["last_fork_commit"][:10]) for r in sorted(t,key=lambda r:-(r["lines"] or 0))]
import os; os.makedirs(".qa-scratch/t13", exist_ok=True)
open(".qa-scratch/t13/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=lambda r:r["path"])))'
# paths 9 lines 10165 {'fork-own': 9} {'python': 6, 'shell': 3} {'n/a': 9}
```

**The nine, at `8ebaf8daad`, by what each runs against and by what oracle:**

| Tool | Lines | Last fork commit | Runs against | Oracle | Caller | Recorded run |
| --- | ---: | --- | --- | --- | --- | --- |
| `cloud-round-trip` | 7,808 | `bc2dceb406` 2026-10-11 | a guest (or a handheld) over SSH; `cloud-test-backend` on the host; QEMU serial and monitor for the LINK and KILL cells | **both ends**: the device's file against the endpoint's object (`epath()`, the existence-checking `cat`, blindspot 31's fix) | `vm-qa`'s `round-trip` suite (the single-device suite) and the opt-in `link` suite (LINK1-7); CAP (14), KILL (12) and PAIR (9) cells by hand | 6 lines in `docs/vm-qa-log.md`; the newest PASS 2026-10-08, *108 checks each over local WebDAV and SFTP* |
| `cloud-test-backend` | 920 | `bc2dceb406` | the host: WebDAV `:9010` (`rclone serve webdav`; no hashes, no modtimes, the harshest), S3 `:9012` (MinIO in a container, `quay.io/minio/minio:latest`), SFTP `:9013` (an unprivileged sshd), SMB `:9014` (`dperson/samba:latest`), FTP `:9015` (`pyftpdlib`, pip-installed into a venv at first `up`), a dead port `9011` never bound | none: it is the endpoint; `cat` checks existence first because MinIO's `rclone cat` of a missing key exits 0 | `vm-qa` (`up`, `port`, `rclone-conf`, `shipped-default`, `reset`, `seed-content`, `seed-device`) | rows 37/39 (2026-09-06/07) |
| `cloud-connections-test` | 307 | `bc2dceb406` | the host's Python, importing `cloud_connections` from the package sources into a tempdir | the module itself (no second implementation); the host's rclone, not the device's | nobody | 0 lines |
| `cloud-census` | 306 | `4533dddc72` 2026-09-07 | **a handheld over SSH** (`--host root@192.168.1.81` in its text): reads `/storage`, the cloud log, the ES log; *the device's own scripts are not run* | reading only | nobody | 0 lines |
| `cloud-pair-migration` | 243 | `083f4fad86` 2026-10-08 | two guests on `vm-pair` and a backend -- **but it exits 2 before anything** (lines 58-63: *Historical migration proof only (D-CLOUD-175/#508)*; it requires `cloud_migrate_layout`, deleted by `e6645cb5ea` the same day) | -- | nobody | row 32 (2026-10-01, #354's runs 96-99), before its retirement |
| `cloud-save-integrity` | 219 | `1bd4554dc8` 2026-10-08 | files on the host: `before.json`/`after.json` (`rclone lsjson --hash-type Dropbox`), ordered and read manifests, payloads; checks the Dropbox content hash, RZIP v1, RASTATE v1, PNG structure (#517, D-CLOUD-181) | its sibling test's synthetic corruption | nobody | 0 lines |
| `cloud-input-test` | 132 | `bc2dceb406` | the host's shell with shims (`nmcli` as a Python stub, `iwctl`, `iw`, `sleep`) over the real `wifictl`; `cloud_oauth` on two lines | the script itself under shims | nobody | 0 lines |
| `cloud-capture-stamp-test` | 116 | `080ceda7c5` 2026-09-09 | the host's bash over `finish()` lifted out of `cloud_capture` by `sed`, with `date` faked | **its own documented control**: `git show f451252587:...cloud_capture` FAILs | nobody (`cloud-round-trip`'s CAP12 mirrors it) | 0 lines |
| `cloud-save-integrity-test` | 114 | `1bd4554dc8` | the host; `runpy` over `cloud-save-integrity`; `--rclone <path>` as an independent Dropbox-hash oracle | **a second implementation** (rclone's hash) -- the only tool of the nine whose oracle is not the code under test | nobody | 0 lines |

**Churn, since 2026-06-01 at the hash:** `cloud-round-trip` 90 commits (74 in
September; 4,953 to 6,700 lines on 2026-09-10 alone; now 77% of the slice;
461 `check()` calls, 59 `raise Fail`, 46 `step()` calls in the single-device
suite, 38 `time.sleep` waits of which ten are 2 s, around SSH, serial and
monitor actions), `cloud-test-backend` 21 (one fix subject),
`cloud-pair-migration` 6, `cloud-census` 2, the other five 1 each; 124 in
all, 6 with a fix or bug subject. **Blindspot and friction entries:** 31
(the MinIO double bucket, the harness agreeing with itself), 71 (a stale
fixture name; its stale-name guard re-pointed at `cloud_migrate_layout
--superseded` on 2026-10-02, six days before that script was deleted); the
friction lines of 2026-09-15 (two guests on one QA folder: *the one
round-trip FAIL was mine*) and 2026-10-02 (eleven checks failed on a `/GAMES`
default, #366). **Issues:** no issue has ever been titled after a harness
tool; the 19 `bug` issues naming `cloud-round-trip` are product bugs it
proved (#53, #141-#143, #315, ...) plus #366. **Three counts for one
suite:** `vm-qa` line 36 says *27 steps*; the tool has 46 `step()` calls and
461 `check()` calls; the 2026-10-08 work log says *108 checks*. **Two
scripts the harness names that do not exist:** `cloud_reconcile` (line 1771,
`APPLY = "cloud_reconcile --apply --unit {unit} --keep {side}"`, the pair
registry's apply step; never added to the tree -- `git log --all
--diff-filter=A -- '*cloud_reconcile'` is empty; the comment says *the
command fails today and the fixtures with it*; D-CLOUD-051 named it) and
`cloud_migrate_layout` (deleted 2026-10-08, still named 8 times by
`cloud-pair-migration` and 55 times by T15's suite). **A vendored copy of
the whole tool** sits under `docs/qa-logs/2026-10-07-cloud-validator/`.
**The no-network step** (lines 1460-1467) fakes the network with a stub
`ip` first on `PATH` (a synthetic input, `vm-first.md`); the real link cut is
the LINK registry's, over the serial console.

**What this slice does not touch:** the cloud scripts the harness drives
(T16's and T17's rows); `vm-qa` and the VM tools (T12's, accepted: a stale
count there is a lead handed to the coordinator, not an edit here); the
rule (the coordinator's; #909 is open); any device; any person's cloud.

## 3. Read first

1. `next:AGENTS.md`; the every-session rules; **`vm-first.md`** and
   `engineering-practices.md` § "Nothing runs on a person's device without
   their yes" (D-QA-015: `cloud-census` is read, never run; no handheld, no
   Dropbox); `engineering-practices.md` § Guards must fail closed and § A
   name is not a behaviour (a PASS line is a claim; the assertion is the
   evidence); `upgrade-and-install.md` § Verify on a device, not on the host
   (the host's rclone is not the device's).
2. **`rclone-cloud-sync.md` whole, with #909 open beside it** -- its
   § "Testing it without a cloud account", § "Five backends", § "Runbook"
   and § "What the QA backends compare by" are the harness's own
   documentation, and the five facts #909 names are the ones not to trust.
3. `docs/reviews/plan-for-the-plan.md` whole (§ 4; § 6c on Independent
   depth); `docs/reviews/order.md` § T13, § T16, § T17; this brief whole;
   the area futro; `docs/blindspot-register.md` entries 22, 31, 32, 38, 71.
4. The nine tools at the hash, `cloud-round-trip` first (its registries at
   lines 309-1714; `epath()`, `caps()` at 1792, the `check()`/`step()`
   helpers; `assert_two_devices`; the LINK and KILL classes); then
   `cloud-test-backend` (the `up`/`ls`/`down`/`cat`/`port`/`rclone-conf`
   subcommands, the five backends and the dead port); then the seven small
   ones. T14's `02-forward-audit.md` § The runs and its brittleness table
   (the shape); T12's audit for `vm-qa`'s cloud suites; `docs/vm-qa-log.md`
   rows 28 to 39 and 146 (every recorded round-trip verdict).
5. The live M6 body; #660 (with its comments); #1047 (the epic, its futro
   comment); #339; #346; #909, #972, #366, #517, #354 (the harness's own
   history); the register rows D-QA-058, D-CLOUD-181, D-CLOUD-051,
   D-CLOUD-158, D-CLOUD-175, D-WORKFLOW-186, D-WORKFLOW-187, D-WORKFLOW-189,
   D-WORKFLOW-195, D-QA-063.

## 4. The questions

The seven renovation questions of plan § 4, with **brittleness** as the lens
and the assertion-shape table as the answer T16 and T17 wait for:

- **Q3 Bugs -- the harness's own.** `cloud_reconcile` (what the A5 and
  retention-ordering fixtures do today: FAIL on every run, skip, or never
  run; whether any recorded PASS covered them; the fix is a device script
  T16's, or a fixture that says it waits); `cloud-pair-migration` (retired
  by code: a tool that exits 2 is not a test); the three counts for one
  suite (a PASS line that says how many assertions it certifies); the
  no-network step's exit (#909's item 4: the rule or the tool is wrong);
  MinIO's `cat` and every other probe that cannot report absence (blindspot
  22); the sleeps (blindspot 32: a wall-clock wait standing in for an
  ordering). Each a `bug` on the fork when proven, with its constructed
  case; the fix a stage-E stream.
- **Q6 Dead ends -- what the harness carries and nobody runs.** The seven
  tools without a caller, each with its disposition: wired into `vm-qa`
  (a lead for the coordinator, T12's file), kept as a hand-run tool with a
  recorded procedure, or retired (`cloud-pair-migration`, with its
  `Already written:` and the mixed-installation gate D-CLOUD-158 it guarded
  named as guarded elsewhere or not); `cloud-census` (a handheld-only tool
  under the cloud prefix; `cloud-input-test` (a Wi-Fi test under the cloud
  prefix: the OS scripts area's subject); the vendored copy under
  `docs/qa-logs/`; the two never-existing scripts.
- **Q2 Standards -- the oracle question, blindspot 31.** For every assertion
  in `cloud-round-trip` that says *reached the cloud*, *restored*, *stamped*,
  *nothing else changed*: does it read the other end (`epath()`, the
  endpoint's `cat` with its existence check) or the device's own report?
  Does `caps()` mark rather than skip where a backend cannot hold a step
  (the tool's promise: *nothing is skipped in silence*)? Which tools run the
  host's rclone where the rule says the device's (`cloud-connections-test`
  by the module's choice; `cloud-save-integrity-test` by design, as an
  oracle)? Which run the host's bash where the scripts run under busybox
  (`cloud-capture-stamp-test`, `cloud-input-test`; T14's busybox rule,
  D-QA-063)? The unpinned `:latest` images and the pip install under the
  standing baseline (D-QA-058).
- **Q1 Modernize:** the one-file harness (7,808 lines, 77% of the slice,
  grown 1,747 lines in a day) against the shape T14 found good (one test,
  one subject, one oracle); the registries by hand (CAP, KILL, PAIR) and
  what wiring them into `vm-qa` would cost in guest minutes; the rule's
  `paths:` (three of nine) and #909 -- both the coordinator's to change, the
  lane's to name.
- **Q4 Package currency:** `quay.io/minio/minio:latest`,
  `dperson/samba:latest`, `pyftpdlib` unpinned (the version each `up`
  resolved on the day, from the container and the venv), and the host's
  rclone 1.60.1-DEV against the device's 1.75.2 (D-QA-058's baseline runs
  the image's rclone on a guest; the two host-rclone tools say what they
  prove with the host's).
- **Q5 Efficiency:** the single-device suite's wall time (81 s recorded) and
  what each registry would add; the guest minutes a full run costs on a
  shared host.
- **Q7 Clarity and structure:** can a reader tell from a PASS line what was
  certified, by which oracle, against which backend; the three descriptions
  of the harness (`vm-qa`'s comment, the rule's runbook, the tool's own
  header) against the code.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor):

1. Tracker state is never sole evidence: every cell cites a command's
   output (a test's exit and its own PASS/FAIL lines, a backend's `ls`, the
   tool's `--list`, `git log`) or a file:line.
2. Mechanical evidence outranks reading: a header's claim about an oracle is
   a claim; the assertion's code is the evidence; a recorded PASS is a claim
   about one run on one backend.
3. **The bench is the host first, and one guest in a granted window.** **Can
   this be done on the VM? Yes -- and most of it on the host:** the four
   self-contained tests (`cloud-connections-test`, `cloud-input-test`,
   `cloud-capture-stamp-test`, `cloud-save-integrity-test --rclone
   $(command -v rclone)`) run bare on the host; the backends' `up`/`ls`/
   `cat`/`down` for WebDAV and SFTP (host processes, `down` matters) and S3
   (a MinIO container) run on the host; `cloud-round-trip --list` and its
   `--dump` paths read without a device. **The guest cycle** -- the
   single-device suite over WebDAV then SFTP on one GENERIC_X64 guest (the
   image under `/workspace/artifacts/rocknix-images/`, the newest qualified
   cut named in `docs/vm-qa-log.md`), plus CAP1-14 by hand, about two
   minutes per backend plus the guest's boot -- **runs only in a window the
   coordinator grants on #660** (asked for at the end of stage A, with the
   image, the backends, the cells and the minutes; run after the M7 lane's
   FINAL RETURN; stopped by its pidfile, never by pattern). **No handheld,
   no person's cloud, no hosted account, ever** (`cloud-census` is read, not
   run; nothing with `--real-roms`; the QA folder is the backend's own).
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`: for each tool, the constructed input that makes it fail
   (the order's *each guard's positive recorded*), run where the tool runs
   on the host, named as `none` where the lane could not construct one.

**The runs, with what the coordinator read** (the lane runs each at stage A
in its worktree and records the exit, the wall time and the summary line;
`TMPDIR` under `/workspace/tmp/m6-t13/`; every credential-shaped line the
backends print goes through the masking filter before it reaches a log or a
transcript):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-harness-660
cd "$D"; export TMPDIR=/workspace/tmp/m6-t13/tmp; mkdir -p "$TMPDIR" .qa-scratch/t13
MASK='s/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'
# the four bare tests (host; each prints its own PASS/FAIL lines)
for t in cloud-connections-test cloud-input-test cloud-capture-stamp-test; do s=$(date +%s); tools/$t > ".qa-scratch/t13/$t.out" 2>&1; echo "$t rc=$? $(( $(date +%s) - s ))s $(grep -c -E '^(PASS|ok)' ".qa-scratch/t13/$t.out") pass-lines $(grep -c -E '^(FAIL|not ok)' ".qa-scratch/t13/$t.out") fail-lines"; done
s=$(date +%s); tools/cloud-save-integrity-test --rclone "$(command -v rclone)" > .qa-scratch/t13/cloud-save-integrity-test.out 2>&1; echo "cloud-save-integrity-test rc=$? $(( $(date +%s) - s ))s $(grep -c '^PASS' .qa-scratch/t13/cloud-save-integrity-test.out) PASS $(grep -c '^FAIL' .qa-scratch/t13/cloud-save-integrity-test.out) FAIL"; rclone version | head -1
# the documented positive of cloud-capture-stamp-test (the old finish() FAILs)
git show f451252587:projects/ROCKNIX/packages/network/rclone/sources/cloud_capture > "$TMPDIR/old-cloud_capture"; tools/cloud-capture-stamp-test "$TMPDIR/old-cloud_capture" > .qa-scratch/t13/stamp-positive.out 2>&1; echo "stamp positive rc=$? (expect non-zero)"
# the retired tool (expect exit 2 and its sentence; nothing else runs)
tools/cloud-pair-migration /nonexistent/a.img.gz /nonexistent/b.img.gz /nonexistent/c.tar > .qa-scratch/t13/pair-migration.out 2>&1; echo "cloud-pair-migration rc=$? $(head -c 160 .qa-scratch/t13/pair-migration.out | tr '\n' ' ')"
# the backends on the host (down matters: WebDAV, SFTP and FTP are host processes that survive the session)
for b in webdav sftp s3; do s=$(date +%s); tools/cloud-test-backend up --backend "$b" > ".qa-scratch/t13/backend-$b-up.out" 2>&1; rc=$?; echo "backend $b up rc=$rc $(( $(date +%s) - s ))s port=$(tools/cloud-test-backend port --backend "$b" 2>/dev/null)"; tools/cloud-test-backend ls --backend "$b" 2>&1 | sed -E "$MASK" | head -3; tools/cloud-test-backend cat --backend "$b" no/such/object > /dev/null 2>&1; echo "cat of a missing object rc=$? (expect non-zero: blindspot 22/31)"; tools/cloud-test-backend down --backend "$b" > /dev/null 2>&1; echo "down rc=$?"; done
tools/cloud-test-backend status 2>&1 | sed -E "$MASK" | head -5 || true    # or whatever the tool's listing subcommand is; nothing left running
# the harness without a device
tools/cloud-round-trip --list > .qa-scratch/t13/rt-list.out 2>&1; echo "round-trip --list rc=$? $(grep -c -E '^(A|CAP|LINK|KILL)[0-9]' .qa-scratch/t13/rt-list.out) cells"
grep -n -E 'cloud_reconcile|cloud_migrate_layout' tools/cloud-round-trip tools/cloud-pair-migration | cut -c1-120
grep -c 'time.sleep(' tools/cloud-round-trip; grep -c -E '(^|[^a-z_])check\(' tools/cloud-round-trip; grep -c -E '^\s+step\(f?"' tools/cloud-round-trip
# the counts the three descriptions give (vm-qa's comment, the rule, the tool)
grep -n -E 'round-trip.*steps' tools/vm-qa | head -2; grep -n -E 'exit (4|69)' .claude/rules/rclone-cloud-sync.md tools/cloud-round-trip | head -6
# the unpinned images and the pip install
grep -n -E 'IMAGE=|pip install' tools/cloud-test-backend
```

**The reading, per tool:** `cloud-round-trip` assertion by assertion for
the oracle each uses (a table: the step, what it claims, the command that
reads the other end or the device's own report, the backends where `caps()`
marks it); `cloud-test-backend` subcommand by subcommand for what each
guarantees (existence, hash, modtime, atomic PUT) per backend, against the
rule's measured table; the seven small tools for their subject, oracle,
positive and caller; `cloud_reconcile`'s two fixtures for what they report
today; the sleeps for the ordering each stands in for.

**The seat (Phase 4.6, one seat):** `npm install --prefix tools/council`,
`COUNCIL_ENV_FILE=/nonexistent tools/council/run verify-pins`,
`COUNCIL_ENV_FILE=/nonexistent tools/council/run test`; the packet
(`gpt-brief.md`: the nine files and the three context sections;
`packet-manifest.json` with the sha256 of each) **scanned before it is sent**
(`tools/forbidden-terms-check --stdin` 0 hits; the pre-commit's patterns 0
lines -- a hit is a finding and the packet redacts it); the probe
(`gpt-probe.md` with its `.provenance.json`); the refutation (`gpt-audit.md`
with its `.provenance.json`), the seat asked first for the assertion-shape
table's gaps (which "reached the cloud" claims read one end only), the two
never-existing scripts, the no-network step's synthetic input, and the
retired tool's disposition; each item graded in `04` § Second opinion with
the artifact that decided it; a seat cut by its ceiling re-runs on a
trimmed packet (D-WORKFLOW-195). The call runs plainly with a harness
waiter; its provenance names the served model and the Facilitator version.

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#660`
(`Refs #660`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-cloud-harness/00-running-log.md` | the flight recorder: the model and effort, `reviewed-at` with `8ebaf8daad`, the host file's last line and census before each run, every § 5 command with its exit and wall time, the backends brought up and down, the guest cycle's window (granted when, on what comment) and its lines | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the nine re-derived with § 2's block, the churn and the recorded runs, the two never-existing scripts, the retired tool, the rule's `paths:` and #909 | A |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #660's checklist; **a coverage table with one row per path under `## Coverage`** (9); **§ Assertion shapes: one row per `step()` of the single-device suite (46) and per CAP, LINK, KILL and PAIR cell (42): the claim, the oracle (both ends / the device's report / synthetic input), the backends where `caps()` marks it, the recorded verdicts**; § The runs (each § 5 run with exit, wall time, *a FAIL would mean ...*); § The guest cycle (the window, the image, the suite's PASS lines with their check counts per backend, or that it waited); § Positives (one row per tool: the constructed input that makes it FAIL, run, or `none`); § Proofs with `proved:` cells | B, then F |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: the harness x `vm-qa`'s suites x the QA backends x the guests x T15's shims x the rule under #909 x `vm-visual-qa` under #972 | B |
| Analysis | `.../04-analysis.md` | Phase 4 § Finding Verification; § Second opinion (4.6); **§ Renovation face Q1 to Q7, Q2 carrying the oracle table's verdict, Q6 the seven uncalled tools' dispositions and the two scripts, Q4 the unpinned rows**; § Instruction File Recommendations (the rule's `paths:`, #909's five facts, `vm-qa`'s comment -- proposals for the coordinator) | C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (independent; `gpt` at `max`), `gpt-brief.md`, `packet-manifest.json`, the probe and the refutation with their `.provenance.json` | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (...)` | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category, where, acceptance, `Already written:`, the VM line; the YAML `punch_index` | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #660 | `Audit: M6 T13 the cloud test harness -- N findings (...)` | D |
| Bugs | GitHub, label `bug`, milestone M6 | one per defect proven by a run or a constructed case (a never-existing script a fixture calls; a PASS over nothing; a probe that cannot report absence; a count that lies); the fix a stage-E stream | D |
| Retro | `docs/retros/<date>-m6-cloud-harness.md`, posted on #660 | the mini-retro; what the slice did to the two time-to-play numbers (nothing); what T16 inherits (the assertion-shape table and the list of verdicts it may trust) | G |

## 7. Acceptance

The checklist on #660 becomes this section at dispatch, written there by the
coordinator in place of P1's five generated ones (until then #660 carries
those five). Every checkbox names the artifact that ticks it (D-QA-044); the
coordinator ticks at acceptance, from the artifacts, never from the
hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-cloud-harness/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-cloud-harness/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: independent`, one reviewer (`gpt`, `openai/gpt-6-astra`, `max`), and the probe and refutation outputs have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named; `packet-manifest.json` lists the 9 files and the 3 context sections with their sha256, and `02` records the packet's own scan (`forbidden-terms-check --stdin` 0 hits; the pre-commit's patterns 0 lines, or the redactions made).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #909 or #972 for the rule and the VM tool), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the ticked and open counts read back by name.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits; the read is on `8ebaf8daad`'s bytes for the nine (`git diff --stat 8ebaf8daad <reviewed-at> -- $(cat .qa-scratch/t13/paths.txt)` empty) and nothing under `tools/` other than the nine changes at any stage (`git diff --stat <dispatch tip> <fixed-at> -- tools | grep -v -E 'tools/cloud-'` prints no file line).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (9 paths, 10,165 lines, 9 fork-own, 6 Python and 3 shell, reach `n/a` 9), the 108 fork commits since the base (`git log --oneline c445081a59..8ebaf8daad -- <the 9> | wc -l`), the per-tool churn since 2026-06-01, the two never-existing scripts with the commands that show it, and the retired tool's exit-2 lines.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `9`.
- [ ] `02-forward-audit.md` § Assertion shapes carries one row per `step()` of the single-device suite and per CAP, LINK, KILL and PAIR cell (``awk '/^## Assertion shapes/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints the lane's count, asserted equal to the tool's registries at the hash: 46 plus 42), each with its claim, its oracle (*both ends*, *the device's report*, *synthetic input*), the backends `caps()` marks it on, and its recorded verdicts; the rows whose oracle is the device's own report are listed as a class with a count.
- [ ] `02-forward-audit.md` § The runs records the four bare tests, the stamp test's documented positive, the retired tool's exit 2, the three backends' `up`/`ls`/`cat`-of-a-missing-object/`down` (each exit; `cat` non-zero), `cloud-round-trip --list`'s cell count, and the three descriptions' counts (`vm-qa`'s comment, the tool's registries, the work log's 108), each with exit, wall time and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass; no backend process or container is left running after the runs (`tools/cloud-test-backend` reports none, or `pgrep` of the sshd/rclone-serve/minio it started is empty, quoted).
- [ ] `02-forward-audit.md` § The guest cycle records the window the coordinator granted on #660 (the comment's time), the image by file name and BUILD_ID, the single-device suite's PASS/FAIL line and its check count over WebDAV and over SFTP, the CAP cells' lines, and the guest stopped by its pidfile -- or states that no window was granted before the hand-back and which criteria that leaves partial.
- [ ] `02-forward-audit.md` § Positives carries one row per tool: the constructed input that makes it FAIL, the command, the FAIL line observed, or `none` with why; `cloud-capture-stamp-test`'s and `cloud-save-integrity-test`'s rows cite their runs.
- [ ] `00-running-log.md` shows no handheld, no hosted account, no `--real-roms`, no `cloud-census` run (read only), no guest outside the granted window, no `tools/council/run invoke` but the one Phase 4.6 call, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`, no write under `/workspace/repos/rocknix*` or `/tmp`, and every credential-shaped line masked.
- [ ] `04-analysis.md` § Q2 states the oracle verdict (the count of assertions that read both ends, the device's report, a synthetic input; whether `caps()` marks or skips, with the lines) and the host-rclone and host-bash rows; § Q6 carries a disposition for each of the seven uncalled tools, the two never-existing scripts, the vendored copy and the retired tool (its `Already written:` and the D-CLOUD-158 gate it guarded); § Q4 the three unpinned rows with the versions resolved on the day; § Q3 each proven defect as a `bug` with its constructed case.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest` or `design`; every punch item carries `question:`; every `bug` passes `tools/box-check --issue N`.
- [ ] The retro exists at `docs/retros/<date>-m6-cloud-harness.md`, is posted on #660, says what the slice did to the two time-to-play numbers (nothing) and names what T16 inherits (the assertion-shape table; the verdicts it may trust and the ones it may not).
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge).

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #660; a blocker named on #660 with what is needed; a branch that differs
from `8ebaf8daad` on one of the nine at stage A; a failed seat (a hold, with
the provenance quoted); or an execution limit, stated as such with the
running log current. A checkpoint is not a stop; a differing count is a
delta; `next` moving is drift; **a guest window not yet granted is not a
stop** -- stage B's reading goes on and § 7's guest criterion says what it
waits for. An idle session says it is idle on #660, **does not end a turn
on a post that asks nothing**, and **updates its session pointer at every
checkpoint** (#1014).

**What never runs in this slice:** anything against a handheld, a person's
cloud, a hosted account or the maintainer's Dropbox (D-QA-015; `cloud-census`
is read, never run; `--real-roms` never); a guest outside a window the
coordinator granted on #660; a build; a fetch of any source; a
`tools/council/run invoke` other than the one Phase 4.6 seat, or any other
`tools/council/run` call without `COUNCIL_ENV_FILE=/nonexistent`; an edit to
any file under `tools/` at stages A to D, and at stage E an edit to any file
but the nine; a push to any branch but the lane's own; `fork-worktree
sync|remove|repair`; an edit to a rule (`rclone-cloud-sync.md` under #909
included), `CLAUDE.md`, `AGENTS.md`, a decided register row or
`.github/sessions/saved-session-state-next.md`; a write under
`/workspace/repos/rocknix*` or `/tmp` (use `/workspace/tmp/m6-t13/`); a
backend left running after a run; a credential-shaped literal written
anywhere; `--no-verify`; bare `git stash`; `git worktree remove --force` or
`rm -rf` on a worktree or a bare variable path.

## 9. Ceremonies owed

- A work-log entry per session headed `#660`, its time from `date -u` in
  the same command, its prose through a quoted heredoc or the Write tool;
  `tools/work-log-index --write` after it (in this worktree only).
- A friction line the moment something slows, with `issue: #660` or the
  guard.
- The VM question written before any proof (§ 5: the host first; one guest
  in a granted window; no device, no person's cloud).
- The mini-retro at stage G, posted on #660, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator.
- A register row the same session for any decision the slice forces; the
  next Decided ID is D-WORKFLOW-210 or higher, D-QA-064, D-INFRA-032; it
  goes at the end of `## Decided`, and a row is never edited.
- The merge notes: when `next` moves, the **coordinator** merges `next`
  into this branch, never between stage A and stage D; the coordinator
  merges its own branch into this one at hand-back before the last
  criterion's checkers run; a merge with conflicts is checked for leftover
  markers before it is committed (#696), and the ledgers are united by
  whole entries.
- Commit messages `docs: ...` until stage E (then `<tool>: ...` per stream),
  each with `Refs #660` and the attribution line; `git add -A` only after
  `git status --short` shows nothing a run left behind (`.qa-scratch/` and
  `tools/council/node_modules/` are gitignored).

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#660's checkboxes against their artifacts; the lint's `PASS` line; the
seat's `review-plan.json` and provenance and the packet's recorded scan; the
audit issue's checkboxes all at an outcome (the ticked and open counts read
by name); the coverage table's row count (9) and the assertion-shape table's
count against the registries; **re-running on an export of the tip under
`/workspace/tmp`: the membership block, the four bare tests and the stamp
test's positive, the retired tool's exit 2, the three backends' `up`/`cat`
-of-a-missing-object/`down`, `cloud-round-trip --list`, the empty diffs
under `tools/` outside the nine;** `register-check` and `rules-check` on a
simulated merge with the coordinator's tip (the ledgers united; the archive
carrying `projects/`); the retro's answers. The lane posts one hand-back
comment naming the tip and each artifact by path, writes `reviewed-at:` and
`fixed-at:` into #660's body, then says it is idle. After acceptance the
coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the full lint, carries the assertion-shape
table's verdict into T16's brief, merges the branch in its turn after the
M7 candidate (after T12's, before T14's), and closes #660 when every row is
proven.

**The readings before dispatch** (plan § 3, principle 3): the area's futro
(#1047) carries this slice's kickoff, and a stranger's proof of this brief
is run by a reader with no context before dispatch; version 2 records what
each found.
