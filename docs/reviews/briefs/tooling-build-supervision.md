# Brief: M6.P2 T9, build supervision and host maintenance (#656)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #656 differ, #656 wins and the
coordinator corrects the brief in the same session. **Version 2
(2026-10-24, after the stranger's proof of version 1 -- 72 claims: 54 right, 4
wrong, 6 partial, 1 uncounted, 7 uncheckable -- each wrong or partial one
corrected in place and listed in the futro's errata):** written after the tooling area's futro
(`docs/futros/2026-10-24-m6-tooling-and-guards.md`, posted on #903), whose
adjustments A1 to A8 are written into this version, and after T5, T6, T7,
T8, T30 and T24 were accepted, so their retros' *adjustments for the next
lane* are this brief's starting rules. Every figure below was produced by a
command on the tree at `8ebaf8daad`, on an export of it under
`/workspace/tmp/m6-coordinator/t9-hash/`, or on the host this afternoon, and
says which; a stranger's proof precedes the dispatch and version 2 records
what it found. **Each command block sets its own variables** (`D`): a Bash
call in this harness starts a fresh shell. **This is a read of the fork's
own guards at Independent depth**: eighteen files, none of them upstream's,
that decide what the fork trusts about its builds and its host; their tests
are the bench; **nothing in this slice builds, reclaims, installs, stops a
guest, formats a disk or publishes** -- the tools are read, their isolated
tests are run in the lane's own worktree, and every mutating entry point is
named in § 8 as a stop.

## 1. Identity

- **Issue:** #656 `M6.P2 E903/T9: tooling-and-guards: build supervision and
  host maintenance`, slice `tooling-build-supervision` (`k: 9`) in
  `docs/reviews/slices.json`, ninth in `docs/reviews/order.md` (its § T9
  paths line: *"18 paths, 3,795 lines, 3,384 read, of which 3,384 fork-own;
  0 patch and config lines; reach n/a 18"*; its `why`: *"`watch-*`, the
  admission guard and the swap helper keep long jobs honest; with the build
  engine under D-WORKFLOW-186, the maintainer's weight on the build process
  ahead of any device target ("the actual build process"), #644's findings an
  input"*). **Epic:** #903 (the tooling and guards: this slice first, then
  T10 #657, T12 #659, T14 #661, T15 #662, T45 #692), whose futro carries
  this slice's kickoff. **Milestone:** M6; its body holds the live order;
  read it first. **Predecessors:** #346 (the plan), #641 (the survey), #644
  (the build-path read: its *Our build path* paragraph is where every build
  enters `tools/watch-build`), **T5 #652** (accepted: the build engine these
  tools wrap; its retro's adjustments), **T6 #653** and **T8 #655**
  (accepted: their retros' adjustments, § 3). **Beside it:** T4 (#651, the
  doctrine) runs in the other lane (D-WORKFLOW-190); the two share no path,
  and T4 reads the rules that name these tools (`device-builds.md` § Before
  a build, `engineering-practices.md` § A promise is not a mechanism) while
  this slice reads the tools.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, edit a rule or a decided register row, or decide a question of
  scope: those are the coordinator's, reached through #656, one question at a
  time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for every defect it finds (D-WORKFLOW-187). Nothing else.
- **One worktree, one session.** Branch `feature/m6-tooling-build-supervision-656`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-build-supervision-656`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the two hashes are in the dispatch comment on #656). **Before that
  comment exists there is no worktree at that path and none of the first
  commands can run.** The session is the T5 lane's (`m6-t5-build-engine`,
  pane `wN:p7`), which ran T5, T6, T7 and T8; those worktrees stay beside this
  one, idle, until their merges, and nothing is written there. The primary
  checkout `/workspace/repos/pixelelated/distribution` stays on `next`
  (D-INFRA-025); the legacy checkout and `rocknix.worktrees/*` are the M7
  lane's, read only, never a process started there -- **their `.build-runs/`
  directories are this slice's evidence of what the watcher met in real
  runs, listed and read through the credential filter, never written**
  (#597: a result file belongs to its producer). Every other lane's worktree
  is `git -C` only. **The rules in this worktree are `next`'s except the paths
  the dispatch comment lists.** Known stale facts in the rules (the legacy
  layout, #640) do not cost an hour here: every rule the work touches is
  named in § 3.
- **Model and effort:** Opus 5.5 (the maintainer, 2026-10-22: *"the work
  will be Opus 5.5"*) at high effort. Record what ran in `00-running-log.md`'s
  header.
- **Review depth: Independent** (D-WORKFLOW-184: *Independent (the executor
  plus one GPT-6 Astra review through the Facilitator) for an ordinary code
  slice*; `slices.json` k 9 `depth_reason`: *an ordinary code slice*; the
  code-auditor's `review-levels.md`: *primary plus one external reviewer
  from another lab; Phase 4.6 remains required*). **One seat, GPT-6 Astra at
  `max`** through the Facilitator (`tools/council/run invoke --member gpt
  --provider openrouter`; `npm install --prefix tools/council`,
  `verify-pins` and `test` first; the key is `~/.config/council/env`,
  sourced by `run`, never read into a transcript): a probe first (identity,
  effort and provider read from the provider's own field), then one
  refutation pass over one bounded packet (§ 5), the provenance file beside
  each output, as T8's `second-opinions/` did with one seat. **A failed seat
  is a hold**, not a Local fallback (D-WORKFLOW-195: a seat cut by its output
  ceiling re-runs on a trimmed packet, the coordinator's call). The packet is
  the whole slice: 18 files, 3,795 lines, 201,453 bytes (197 KiB) at the
  hash, plus the seven entry lines (`Makefile:40`, `:179`;
  `scripts/{build,build_distro,image,install,build_compat}`'s `exec
  ./tools/watch-build --entry`, at `build:9`, `build_distro:11`, `image:9`,
  `install:10`, `build_compat:7`) as read-only context; **the seat is asked first for `reclaim-swap`, `install`
  and `build-admission`** -- the sudo helper and the guard that admits a
  compiler -- where a second lab's eye matters most (futro A6).
  `review-plan.json` records depth `independent`, scope `epic`, primary
  `anthropic/claude-opus-5-5` / lab `anthropic`, one reviewer `gpt`, model
  `openai/gpt-6-astra`, lab `openai`, effort `max`, provider `openrouter`
  pinned to OpenAI with `allow_fallbacks: false`.
- **The host is the substrate, and it is shared (futro A1).** Read on
  2026-10-24 by the coordinator: `/usr/local/sbin/pixelelated-reclaim-swap`
  installed (root, 0755); `/etc/sudoers.d/zz-pixelelated-reclaim-swap` present
  beside `zz-fleet-hardening`; `sudo -n -l` lists the helper's `--reclaim`
  alone, as root, without a password and with `NOSETENV`, **and above it the
  fleet's `(ALL : ALL) ALL` for `max`**; `/swap.img` 8 GiB with 8 GiB used;
  Docker 29.8.2; `.build-runs/` in **45** M7 worktrees under
  `/workspace/repos/rocknix.worktrees/` (2,022 run ids; `conflict-resolution`
  alone 362) and in `/workspace/repos/rocknix/` itself -- version 1 said
  three, the first three of an `ls | head -3`; host Python 3.14 (the
  container's is 3.10, #492; these tools run on the host). **The lane changes
  none of it.** No build, no `tools/build-preflight --reclaim-swap` or
  `--stop-vms` (report mode only), no `host-maintenance/install`, no
  `fork-newdrive` (it moves the worktrees and re-mounts -- `sudo mv`, an
  `fstab` line, `mount`, `rsync`; the `parted` and `mkfs` lines in its header
  are the operator's, as comments; no dry run), no `fork-publish-release`
  past `--prepare` (a plan file, never a tag, a draft or an asset), no
  `watch-build` entry around a real command. The isolated tests run in the
  lane's worktree after the host file is read and the census recorded
  (`pgrep -c -x qemu-system-x86`), and `.gitignore:84` (`/.build-runs/`) and
  `:63` (`/.qa-scratch/`) are read before the first commit so a test's
  leavings are never staged.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-build-supervision-656
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-tooling-build-supervision-656
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: this is not the lane's worktree (stacked on P1): stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists, nothing else
cat .github/sessions/saved-session-state-feature-m6-tooling-build-supervision-656.md
tail -3 /tmp/m7-m6-host-coordination-20261023.txt                   # the host's state: read before any test that arms a watcher
pgrep -c -x qemu-system-x86                                          # the census, recorded in 00 before the first test run
df -i /tmp | tail -1                                                 # never export a tree under /tmp
grep -nE 'build-runs|qa-scratch' .gitignore                          # :84 and :63 on 2026-10-24
mkdir -p .qa-scratch/t9/at-hash && git archive 8ebaf8daad tools/watch-build tools/watch-job tools/watch-build-submit tools/build-preflight tools/fork-newdrive tools/fork-publish-release tools/host-maintenance Makefile scripts/build scripts/build_distro scripts/image scripts/install scripts/build_compat docs/qa-logs/2026-10-03-watch-job docs/qa-logs/2026-10-04-watch-progress docs/qa-logs/2026-10-05-watch-submit docs/qa-logs/2026-10-13-build-admission docs/qa-logs/2026-10-04-host-swap-rollout docs/qa-logs/2026-10-03-watch-delivery .github/workflows/fork-checks.yml | tar -x -C .qa-scratch/t9/at-hash   # the read tree (A1 of the futro): every line number below is this tree's
"$D/tools/rules-check"; echo "rc=$?"; "$D/tools/register-check"; echo "rc=$?"; "$D/tools/ceremony-check"; echo "rc=$?"   # rc 1 on 2026-10-24: W42 OVERDUE (M7's week), not this lane's to pay
git push -u origin feature/m6-tooling-build-supervision-656
```

## 2. Scope

**18 paths, 3,795 lines; every one fork-own; 12 Python, 3 bash, 3 Markdown;
reach `n/a` 18.** The membership is the inventory's at P1's `2174265e9c`
with the slice's rule (`k: 9`, globs
`tools/{watch-*,host-maintenance/**,build-preflight,fork-newdrive,fork-publish-release}`).
The re-derivation, in the lane's worktree (which carries P1's inventory):

```bash
python3 -I - <<'PY'
import json, collections, os, re
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
pat = re.compile(r"^tools/(watch-[^/]+|host-maintenance/.+|build-preflight|fork-newdrive|fork-publish-release)$")
t9 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "tooling-and-guards" and pat.match(r["path"])]
print("paths", len(t9), "lines", sum(r["lines"] or 0 for r in t9), dict(collections.Counter(r["tier"] for r in t9)), dict(collections.Counter(r["reach"] for r in t9)))
print(dict(collections.Counter(r["language"] for r in t9)))
os.makedirs(".qa-scratch/t9", exist_ok=True)
open(".qa-scratch/t9/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t9, key=lambda r: r["path"])))
PY
wc -l < .qa-scratch/t9/paths.txt                                                             # 18
while IFS= read -r p; do printf '%6d %s\n' "$(git show 8ebaf8daad:"$p" | wc -l)" "$p"; done < .qa-scratch/t9/paths.txt | awk '{s+=$1; print} END {print s " lines"}'   # 3795
```

Recorded (2026-10-24, the export of the hash):

| Lines | Path | Last fork commit | What it is |
| ---: | --- | --- | --- |
| 223 | `tools/watch-build` | `d7e2d6be41` 2026-10-13 | the runner every build enters (`--entry`, `--docker`, `--record-only`, `--admission`; D-WORKFLOW-142) |
| 270 | `tools/watch-job` | `de4cf0e34a` 2026-10-04 | the status file that tells the truth about a long job: `running`, `stalled`, `finished`, `died`, `error` (D-WORKFLOW-141, 143) |
| 101 | `tools/watch-build-submit` | `d7e2d6be41` 2026-10-13 | the durable submission around the runner (D-WORKFLOW-148, #444) |
| 124 | `tools/build-preflight` | `f8a320c8f6` 2026-10-04 | what the machine has before a build: RAM, swap, guests, disk; `--stop-vms`, `--reclaim-swap` |
| 155 | `tools/fork-newdrive` | `4a1c6d898b` 2026-09-04 | move the worktrees to a fresh disk; **legacy defaults at `:20-21`** (#640) |
| 141 | `tools/fork-publish-release` | `d9f428e1a0` 2026-10-13 | `--prepare BUNDLE`: a checked naming and asset plan, never a publication (D-WORKFLOW-159) |
| 493 | `tools/host-maintenance/build-admission` | `26d2f6abce` 2026-10-15 | `prepare`, `consume`, `consume-reporting-failure`: the single-use admission a compiler needs (#493, #597) |
| 216 | `tools/host-maintenance/build-admission.md` | `26d2f6abce` | its guide |
| 242 | `tools/host-maintenance/reclaim-swap` | `f8a320c8f6` 2026-10-04 | the root-owned fixed-target swap helper (D-INFRA-015, #410) |
| 184 | `tools/host-maintenance/install` | `6e4ab570ed` 2026-10-04 | the one-time administrator installer of the helper and its sudoers policy |
| 101 | `tools/host-maintenance/README.md` | `6e4ab570ed` | the helper's guide |
| 313 | `tools/host-maintenance/retention-report` | `510196b072` 2026-10-07 | the read-only capacity and retention report (#461, D-INFRA-018) |
| 94 | `tools/host-maintenance/retention-report.md` | `d7e2d6be41` | its guide |
| 36 | `tools/host-maintenance/admission-test-fixture.py` | `d7e2d6be41` | synthetic admission inputs for the tests |
| 218 | `tools/host-maintenance/test-build-admission` | `26d2f6abce` | negative admission and lifecycle controls, synthetic roots |
| 282 | `tools/host-maintenance/test-build-monitor` | `d7e2d6be41` | the real entrypoint prefixes and Makefile with isolated payloads |
| 95 | `tools/host-maintenance/test-retention-report` | `510196b072` | retention refusals with real temporary QCOW files and processes |
| 507 | `tools/host-maintenance/test-swap-reclaim` | `6e4ab570ed` | isolated guard and recovery tests; never a real swap command |

**Provenance.** `git cat-file -e upstream/next:<path>` fails for all 18: none
is upstream's. `git log --format=%h c445081a59..8ebaf8daad -- <the 18> | wc
-l` is **35** fork commits since the base; their messages cite #383 (6
times), #410 (3), and #489, #471, #461, #409, #395, #394, #393, #344, #265
(2 each), and once each #597, #565, #532, #530, #529, #493, #491, #490,
#444, #413, #412, #411, #371, #368, #367, #310: the watcher (#393 to #395), the swap
helper (#410), retention and admission (#461, #489, #493, #597), the release
identity (#532, #565), the build-path read (#644 is the input, #383 the
earlier record). **The entry points** are outside the slice and read-only
context: `Makefile:40` (`./tools/watch-build -- $(MAKE) $@`) and `:179` (the
`docker-%` target's `BUILD_WATCH`), and `scripts/{build,build_distro,image,
install,build_compat}` each `exec ./tools/watch-build --entry -- "$0" "$@"`
at `build:9`, `build_distro:11`, `image:9`, `install:10` and
`build_compat:7` -- seven entry lines in six files, T5's accepted. **The fork CI** runs three of the
controls (`.github/workflows/fork-checks.yml:42-44`): `test-watch-job.py
tools/watch-job`, `test-build-monitor`, `test-build-admission`.

**The hash.** The slice's bytes are `8ebaf8daad`'s; `reviewed-at:` is the
branch `HEAD` at stage A; the read is made on the at-hash tree
(`.qa-scratch/t9/at-hash/`). The branch differs from the hash on none of
the 18 (P1 and the coordinator changed nothing here): `tr '\n' '\0' <
.qa-scratch/t9/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD --` is
empty; a non-empty result is the first lead.

**The policy on change (plan § 5; D-WORKFLOW-187):** a defect here is the
fork's alone and is fixed under a stream brief at stage E, never at stage B
as a reading's side effect; **a stream on `watch-job` or `watch-build`
proves on a read-only copy of a recorded M7 run's logs beside the synthetic
control, and says what it did to the watcher's silence modes** (futro A7;
`engineering-practices.md` § Say how the watch fails); a stream on the swap
helper or the installer proves only through `test-swap-reclaim`'s doubles,
never a real swap command or a real installation (D-INFRA-015: the owner's);
a change to a guard's contract (D-WORKFLOW-141, 142, 143, 148; D-INFRA-015)
is a lead for the coordinator, not a stream. The two legacy-layout lines
(`fork-newdrive:20-21`, `watch-job:36`) are #640's rows: recorded, unchanged
(futro A5).

## 3. Read first

- **The rules the work touches**, from `next`, this session (`working-principles.md`
  § Pre-flight): `engineering-practices.md` (§ A promise is not a mechanism,
  all of it: *Recorded is not delivered*, *Submit long agent-owned jobs
  durably*, *Read host processes from the host namespace*, *Say how the
  watch fails*; § Guards must fail closed, with *The positive is recorded
  where the guard is wired* and *Success reported over a no-op*; § Never
  edit a shell tool while a run of it is in flight), `device-builds.md`
  (§ Before a build: the machine is memory-bound, § Budget, § Publishing,
  § Temporary directories belong to their execution environment),
  `worktrees.md` (§ Review retention after qualification, D-INFRA-021/022),
  `release-candidates.md` (§ Publishing's identity rules the release tool
  checks), `vm-first.md`, `issue-tracking.md`, `learning-capture.md`,
  `ceremonies.md`, `decision-register.md`.
- **The registers for the scope:** D-WORKFLOW-141 (the monitor observes
  activity logs), 142 (every build enters the runner), 143 (watchers deliver
  as well as record), 148 (durable submission), D-INFRA-015 (the guarded swap
  helper), 018 (retention review after qualification), 021, 022 (large
  artifacts are temporary), 023 (measure peaks on the next build); the
  guides beside the tools (`host-maintenance/README.md`, `build-admission.md`,
  `retention-report.md`) are the tools' own claims, read against the code.
  Blindspot 73 (a monitor observed package completion instead of build
  activity) is the area's own; 8, 14, 22, 26, 42 are its class.
- **The evidence folders** under `docs/qa-logs/`: `2026-10-03-watch-job/`
  (`baseline.log`, the live status files, `test-watch-job.py`,
  `test-watch-build.py` -- the historical routing fixture, #413),
  `2026-10-03-watch-delivery/` (`probe.py`, the four scenario folders),
  `2026-10-04-watch-progress/` (`test-progress.py`, `test-watch-build.py`
  -- the current routing control, `source-hashes.json`),
  `2026-10-05-watch-submit/` (`test-submit.py`, `controls.json`),
  `2026-10-13-build-admission/` (the controls' logs and `host-proof.json`),
  `2026-10-04-host-swap-rollout/` (the installed helper's proofs:
  `installed.json`, `busy-proof.json`, `healthy-noop.txt`). They are what
  each guard was seen to catch when it was wired; the slice reads whether
  that positive still holds.
- **The retros' adjustments** (futro § 3): T5's *run the real script over
  fixture files when its tools can be borrowed read-only* and *before a guard
  fails closed, read what the recorded builds show it would meet*; T6's *run
  a lint over the whole tree before quoting what it should print* and *a
  fixture resolves its scratch path first*; T8's *run a fork script once at
  stage B when it can run* and *count processes by `/proc/*/comm` with a
  prefix, and expect a pipeline's subshell*.
- **#644** (*Our build path*: the entry, the admission, the mounts); **#506**
  (a sandbox's `/proc` hides host PIDs: the watcher's process reads); **#549**
  (a host-only `TMPDIR` in Docker); **#597** (result files belong to their
  producer; the launcher receipt collision the guide's last section
  recovers); **#640** (the legacy layout); **#492** (host Python against the
  container's).
- **The stranger's proof of this brief settled the futro's U-1**: three
  qa-logs controls fail at the hash in any checkout, not for want of `.git`.
  `test-watch-build.py` (2026-10-04), `test-progress.py` and
  `test-submit.py` copy only `watch-build` and `watch-job` into their
  fixture trees, while `watch-build:50-51` loads `build-admission` beside
  itself (the receipts `test-submit.py` leaves say `[Errno 2] No such file
  or directory: '<fixture>/tools/host-maintenance/build-admission'`);
  `test-build-monitor` passes because `admission-test-fixture.py:16-18`
  copies it, and `2026-10-04-watch-progress/source-hashes.json` records an
  older `watch-build` (`9c15e068...` against the hash's `44a6d875...`). Three
  recorded controls stopped running when the admission guard landed and
  nothing said so: **a finding at the hash, the lane's at stage A**, its fix
  (the fixtures copy the admission module too, and the CI runs them) a
  stream the coordinator briefs. `test-submit.py` also leaves its `mkdtemp`
  directories under `/tmp` (four `pixelelated-watch-submit-*` on
  2026-10-24): a Q3 lead. `test-watch-job.py tools/watch-job` passes (rc 0,
  10 s).

## 4. The questions

All seven apply (plan § 4); for guards at Independent depth **Q6 (brittleness)
and Q3 (bugs) are the lenses the order names**, Q2 the shape of the code,
Q5 what a build pays for its supervision.

| Q | What is asked of these 18 | Where the answer lands |
| --- | --- | --- |
| Q1 Modernize | A hardcoded host path or layout (`fork-newdrive:20-21`, `watch-job:36`: #640's rows); a Python construct the host's 3.14 and the container's 3.10 read differently (#492); a dependency on a tool the host may lack | the rows; #640 named, not changed |
| Q2 Standards | Fail-closed shapes (`engineering-practices.md` § Guards must fail closed): exit codes defined, pipelines with `pipefail`, every expansion quoted, a count asserted not echoed; the credential filter on every host read; `set -u`; a shell tool never edited mid-run | a finding per violation, with the line |
| Q3 Bugs | A guard that can report success over a no-op; a status that can read `running` while the process is gone; an admission that can be reused; a receipt a second owner can overwrite (#597); a kill by pattern; a watch whose silent-failure mode is unnamed; a mode or ownership check the helper skips | a `bug` per defect, `Already written:` and the VM line, its fix under a stream |
| Q4 Currency | Not a currency slice: the tools pin nothing. The row is the Python and bash features they require against the host's versions, and whether `tools/council` is the only `npm` consumer | one paragraph |
| Q5 Efficiency | What a build pays for its supervision: the runner's startup, the watcher's interval, the admission's checks, from the code and the recorded runs' timings (read-only), never a new build | the figures with their source |
| Q6 Dead ends and brittleness | **The guard table** (futro A3): for each guard the tools wire -- `watch-job`'s `running`/`stalled`/`died`/`error`; `watch-build`'s lock, admission check, marker refusal (`RASTERATOPS_BUILD_RUN`), record-only route; the submit launcher's receipts; `build-admission`'s stale, reused and capacity refusals; `reclaim-swap`'s ownership, mode, priority, busy and memory refusals and its reactivation; `retention-report`'s refusals; `build-preflight`'s exits; `fork-publish-release`'s plan checks; and the ones the stranger's proof found unlisted: `install`'s eleven checks (ownership, modes, the sudoers include, the validation and its rollback), `watch-build`'s lock refusal (*another monitored build owns this worktree*) and its inherited-run staleness checks, the submit launcher's duplicate-owner refusal (rc 2), `reclaim-swap`'s lock, hard-link, namespace and `fstab` refusals, `build-admission`'s checkout, plan and schema identity refusals -- the control that constructs its failure, by file and test name, or **none**, which is a finding | the table in `04` § Q6, every row sourced |
| Q7 Clarity | A guide (`README.md`, `build-admission.md`, `retention-report.md`) that claims what the code does not do, or omits what it does; the rules' descriptions of these tools against the code (`device-builds.md` § Before a build, `engineering-practices.md`): a drift is a lead for T4, named on #651 by the coordinator | the rows; T4's leads |

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor):

1. Tracker state is never sole evidence: every verdict cites the tree
   (`git grep`, `git log`, `git diff`), a control's run with its exit, a
   recorded run's status file (read-only), or a document's line.
2. Mechanical evidence outranks reading: a guard's behaviour is the control
   that constructs its failure and the exit the tool returns, not the
   comment above it.
3. **The target is the tree, the controls and the record**: the at-hash
   tools; their tests run in the lane's worktree; the recorded M7 runs'
   `.build-runs/<id>/` status, rc and launcher files (`ls`, `cat` through
   `grep -v -i -E 'key|pass|token|user|psk'`, read only, never written); the
   qa-logs evidence folders. **No build, no reclamation, no installation, no
   guest stop, no disk format, no release action.**
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.

**The controls, with the baseline from the export of the hash** (the
coordinator, 2026-10-24, `/workspace/tmp/m6-coordinator/t9-hash/`, a bare
export without `.git`; futro A2 and U-1). The lane runs all eight at stage A
in its worktree and records each exit; a control that fails at the hash in
a checkout is a finding with its traceback, never a nuisance:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-build-supervision-656
cd "$D"; tail -3 /tmp/m7-m6-host-coordination-20261023.txt; pgrep -c -x qemu-system-x86   # read, and recorded, before the first run
python3 -I tools/host-maintenance/test-swap-reclaim        2>&1 | tail -3      # export: Ran 37 tests, rc 0, under 1 s
python3 -I tools/host-maintenance/test-retention-report    2>&1 | tail -3      # export: rc 0, 7 s
python3 -I tools/host-maintenance/test-build-admission     2>&1 | tail -3      # export: rc 0, 18 s
python3 -I tools/host-maintenance/test-build-monitor       2>&1 | tail -3      # export: rc 0, 64 s; runs the real entrypoint prefixes and the Makefile with isolated payloads in THIS worktree; .build-runs/ is gitignored (:84)
python3 -I docs/qa-logs/2026-10-03-watch-job/test-watch-job.py tools/watch-job 2>&1 | tail -3        # needs the watcher's path; --baseline is its other mode; the CI's form (fork-checks.yml:42); export: rc 0, 10 s
python3 -I docs/qa-logs/2026-10-04-watch-progress/test-progress.py "$D" 2>&1 | tail -3               # needs a root; FAILS at the hash in any checkout (all 10 case checks): its fixture lacks build-admission (§ 3)
python3 -I docs/qa-logs/2026-10-04-watch-progress/test-watch-build.py 2>&1 | tail -3                 # FAILS at the hash in any checkout: AssertionError "shared runner observes nested QA logs and retains terminal result"; the fixture copies watch-build and watch-job, not build-admission, which watch-build:50-51 loads (§ 3)
python3 -I docs/qa-logs/2026-10-05-watch-submit/test-submit.py 2>&1 | tail -3                        # FAILS at the hash in any checkout (the AssertionError at :42, raised from :49's submit(base / 'success', 0)): the same cause; it also leaves its mkdtemp under /tmp
.githooks/hooks-test 2>&1 | tail -1                                                                  # T10's bench, run here as a control of the worktree, not of this slice
```

**The record, read only:**

```bash
ls -d /workspace/repos/rocknix.worktrees/*/.build-runs /workspace/repos/rocknix/.build-runs 2>/dev/null | wc -l   # 46 on 2026-10-24: 45 worktrees and the legacy checkout; 2,022 run ids in all, conflict-resolution alone 362
for d in /workspace/repos/rocknix.worktrees/*/.build-runs/*/; do printf '%s ' "$d"; ls "$d" | tr '\n' ' '; echo; done 2>/dev/null | head -20   # the files a run leaves: status, rc, launcher receipts, the log
cat /workspace/repos/rocknix.worktrees/<wt>/.build-runs/<id>/*.status 2>/dev/null | grep -v -i -E 'key|pass|token|user|psk' | head   # what the watcher said of a real run
```

**The reading, per file:** every function and every exit path of the 12
Python and 3 bash files, each guard matched to its control (Q6's table);
every claim of the three guides checked against a line of code; the
`.build-runs/<id>/` layout as written by `watch-build` against what
`watch-build-submit` and `build-admission consume` read back; the sudoers
policy the installer generates against what the README says it is; the
preflight's thresholds against `device-builds.md`'s.

**The seat (Phase 4.6, one seat):** `npm install --prefix tools/council`,
`tools/council/run verify-pins`, `tools/council/run test`; the probe
(`gpt-probe.md` with its `.provenance.json`: served model, provider,
effort); then the refutation over the packet (`gpt-brief.md`, the 18 files
and the seven entry lines, `packet-manifest.json` with the sha256 of each),
asked first for `reclaim-swap`, `install` and `build-admission`
(`gpt-audit.md` with its `.provenance.json`); each item graded in `04` §
Second opinion with the artifact that decided it. `tools/watch-build
--record-only` holds the worktree's build lock even for a network call (T5's
retro), so the two seat calls run plainly, with a harness waiter each.

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#656`
(`Refs #656`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-tooling-build-supervision/00-running-log.md` | the flight recorder: the model and effort, `reviewed-at` with `8ebaf8daad` beside it, the host file's last line and the census before the first test, every § 5 command with its exit status, every `PROOF:` line, each time from `date -u` | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 18 re-derived with § 2's block and its output, the provenance (35 fork commits, none upstream), the branch's deltas from the hash (none expected); § Phase 1: what each tool is for, in the slice's words, and the eight controls' baseline with exits | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #656's checklist, plus **a coverage table with one row per path** (18; the first cell the path in backticks so ``grep -c -E '^\| `tools/'`` counts them), § Mechanical checks (every § 5 block with command, exit status, summary), § The controls (eight rows: command, exit, what a FAIL would mean), § The record (the `.build-runs/` listing and what the status files said); every proof with a `proved:` cell | B, then F |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: the runner x the Makefile and the five scripts; the admission x the retention report; the submit launcher x the runner's receipts; the preflight x the helper; the release tool x `docs/releases/versioning.md` | B |
| Analysis | `.../04-analysis.md` | Phase 4, § Finding Verification (4.5), **§ Second opinion** (4.6: the seat's probe and refutation graded item by item), **§ Renovation face** Q1 to Q7, **Q6 carrying the guard table** (every guard with its control or `none`), Q5 the figures | C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (independent; `gpt` at `max`), `gpt-brief.md`, `packet-manifest.json`, the probe prompt, `gpt-probe.md` and `gpt-audit.md` each with its `.provenance.json` | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (...)` with `review plan: independent, 2 model perspectives, 1 verified external calls` | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category, where (file:line at `8ebaf8daad`), acceptance, `Already written:` and the VM line; the YAML `punch_index`; a guard with no control as a `Renovation` item; a #640 row per legacy path, deferred to #640 | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #656 | `Audit: M6 T9 build supervision and host maintenance -- N findings (...)`; one checkbox per item, agent-first | D |
| Bugs | GitHub, label `bug`, milestone M6 | one per defect, with its code trace, `Already written:`, the VM line and the control that will prove the fix | D |
| Streams | the coordinator's brief `docs/reviews/briefs/t9-streams.md` | one per fix the coordinator briefs at the stage-D pause; a stream on a watcher proves on a copied real run's logs beside the synthetic control (futro A7) | E |
| Retro | `docs/retros/<date>-m6-tooling-build-supervision.md`, posted on #656 | the mini-retro, Instruction-Recommendations mode; what the slice did to the two time-to-play numbers (nothing, say so); what it did to the watcher's silence modes, if a stream touched one | G |

## 7. Acceptance

The checklist on #656 becomes this section at dispatch, written there by
the coordinator in place of P1's five generated ones (until then #656
carries those five).
Every checkbox names the artifact that ticks it (D-QA-044); the coordinator
ticks at acceptance, from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-tooling-build-supervision/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-tooling-build-supervision/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included: Q1 to Q7 answered in `04-analysis.md`, and every punch item's `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: independent`, one reviewer (`gpt`, `openai/gpt-6-astra`, `max`), and the seat's probe and refutation outputs each have a `.provenance.json` beside them whose served model is `openai/gpt-6-astra` and whose verification is PASS; `packet-manifest.json` lists the 18 files and the seven entry lines with their sha256.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (#640 for a legacy path; a `bug` for a defect; the coordinator's lead for a contract change), or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits the read and the fixes were made at (the read on `8ebaf8daad`'s bytes; no EmulationStation path), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed`.
- [ ] `01-research-notes.md` § Scope records the read hash, the filter of brief § 2 with its output (18 paths, 3,795 lines; 18 fork-own; 12 Python, 3 bash, 3 Markdown; reach `n/a` 18, or the deltas beside them), the provenance (35 fork commits since `c445081a59`; none of the 18 on `upstream/next`), and the branch-vs-hash diff over the 18 (empty, or each hunk listed with its owner).
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c -E '^\| `tools/' 02-forward-audit.md`` prints 18; each row's Q1 to Q7 cells answered or `n/a` with a reason.
- [ ] `02-forward-audit.md` § The controls records all eight of brief § 5 with command, exit status and summary line, run in the lane's checkout at stage A, each with the sentence *a FAIL would mean ...*; the three that fail at the hash (`test-watch-build.py` of 2026-10-04, `test-progress.py`, `test-submit.py`: their fixtures copy no `build-admission`, brief § 3) are findings with their tracebacks and that cause, never worked around; `test-watch-job.py` and the four `host-maintenance` tests pass.
- [ ] `02-forward-audit.md` § The record lists the M7 `.build-runs/` directories (45 worktrees and the legacy checkout on 2026-10-24, 2,022 run ids) and the ones read (`ls`, through the credential filter) and what each status file said, with no write under any of them (the directories' mtimes before and after the slice, quoted).
- [ ] `00-running-log.md` records the host file's last line and the census (`pgrep -c -x qemu-system-x86`) before the first test run, and no command in it is a build, `--reclaim-swap`, `--stop-vms`, `host-maintenance/install`, `fork-newdrive`, or `fork-publish-release` without `--prepare`; `grep -c -E 'reclaim-swap|stop-vms|host-maintenance/install|fork-newdrive ' 00-running-log.md` counts only lines that quote this brief or a reading.
- [ ] `04-analysis.md` § Renovation face Q6 carries the guard table: one row per guard brief § 4 names (its list read against the code: every guard the code wires is a row, including the ones the stranger's proof added), each with the control that constructs its failure by file and test name, or `none`; every `none` is a punch item.
- [ ] `04-analysis.md` § Q1 carries the two legacy-layout rows (`tools/fork-newdrive:20-21`, `tools/watch-job:36`) deferred to #640, with the lines quoted and unchanged on the branch (`git diff 8ebaf8daad <fixed-at> -- tools/fork-newdrive tools/watch-job` touches neither line, or a stream brief names the change).
- [ ] `04-analysis.md` § Q7 reads each claim of the three guides (`README.md`, `build-admission.md`, `retention-report.md`) against a line of code, with the sudoers policy the installer writes quoted from `install`'s source beside the README's sentence about it, and any drift between a rule's description of these tools and the code named as a lead for T4 (posted on #651 by the coordinator).
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fix-tree`, `fix-control` (a fix proved by a control re-run in the worktree) or `fix-pending-build` (a fix whose proof is the next real build's own run, the coordinator's); ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c '^PROOF:' 00-running-log.md``.
- [ ] Every punch item carries `question:`; every `bug` this lane files passes `tools/box-check --issue N`; no file under `tools/` is changed on this branch before a stream brief (`git diff --stat 8ebaf8daad <fixed-at> -- tools` is empty, or every hunk is a stream the coordinator briefed), and a stream on `tools/watch-job` or `tools/watch-build` records in `02` the recorded M7 run whose copied logs it was proved against beside the synthetic control.
- [ ] The retro exists at `docs/retros/<date>-m6-tooling-build-supervision.md`, is posted on #656, says what the slice did to the two time-to-play numbers (nothing, or the change named), and, if a stream touched a watcher, what it did to the watcher's silence modes.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge, and `tools/lint-audit-artifacts` prints `PASS` on the folder, each exit code in the hand-back comment.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #656; a blocker named on #656 with what is needed (the seat failed, a
control that cannot run for a reason outside the tree, two commands that
disagree); a branch that differs from `8ebaf8daad` on one of the 18 at stage
A in a hunk the dispatch comment did not name; or an execution limit, stated
as such with the running log current. A checkpoint is not a stop; a
differing count is a delta; `next` moving is drift. An idle session says it
is idle on #656, **and does not end a turn on a post that asks nothing**.

**Never run in this slice:** a build or `make` target outside
`test-build-monitor`'s own isolated run; `tools/build-preflight --reclaim-swap`
or `--stop-vms`; `tools/host-maintenance/install` or `reclaim-swap` directly;
`tools/fork-newdrive`; `tools/fork-publish-release` without `--prepare`, or
any `gh release`; `tools/watch-build` around a real command; a write of any
kind under `/workspace/repos/rocknix*`; a Facilitator call outside the
Phase 4.6 pair; `npm install` anywhere but `tools/council`; an edit to a
rule, `CLAUDE.md`, `AGENTS.md`, a decided register row, or
`.github/sessions/saved-session-state-next.md`; `--no-verify`; bare `git
stash`; `git worktree remove --force` or `rm -rf` on a worktree; an edit to
a shell tool while a run of it is in flight.

## 9. Ceremonies owed

- A work-log entry per session headed `#656`, its time from `date -u` in
  the same command, its prose through a quoted heredoc or the Write tool;
  `tools/work-log-index --write` after it.
- A friction line the moment something slows, with `issue: #656` or the
  guard.
- The VM question written before any proof (§ 5: the bench is the host and
  the controls; a guest only for a behaviour claim about a guest, named on
  #656 first with the host file read and the census recorded).
- The mini-retro at stage G, posted on #656, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator (D-WORKFLOW-189).
- A register row the same session for any decision the slice forces; the
  next Decided ID is checked on every pushed branch at the time (on
  2026-10-24 the highest Decided row is D-WORKFLOW-199, the coordinator's;
  T4 runs beside this lane and may take 200); it goes at the end of `##
  Decided`, and a row is never edited.
- The merge notes (futro A8): `tools/watch-build` and
  `tools/host-maintenance/build-admission` are files the M7 lane also
  changed for #597; the branch merges after the M7 candidate in its turn,
  and a conflict there is resolved in the coordinator's hands with the
  stream's paragraph re-applied, as T4's rules are. When `next` moves, the
  **coordinator** merges `next` into this branch, never between stage A and
  stage D; a merge with conflicts is checked for leftover markers before it
  is committed (#696), and the ledgers are united by whole entries.
- Commit messages `docs: ...` for the audit, `<tool>: ...` for a stream's
  fix, each with `Refs #656` and the attribution line; `git add -A` only
  after `git status --short` shows nothing a test left behind.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#656's checkboxes against their artifacts; the lint's `PASS` line;
`review-plan.json` and the seat's provenance (served model, provider,
effort, verification); the audit issue's checkboxes all at an outcome (the
ticked and open counts read by name); the coverage table's row count (18)
and the guard table's rows against § 4's list; **re-running on an export of
the tip under `/workspace/tmp`: the membership block, the file list with
line counts, the eight controls (the two that need a checkout from a
detached worktree of the tip), and the `.build-runs/` listing read-only**;
`register-check` on a simulated merge with the coordinator's tip (the
ledgers united); the retro's four answers; the six exit codes. The lane
posts one hand-back comment naming the tip and each artifact by path,
writes `reviewed-at:` and `fixed-at:` into #656's body, then says it is
idle. After acceptance the coordinator closes the audit issue, prompts the
lane for `audit-completion.json` and the full lint, merges the branch in its
turn after the M7 candidate, regenerates the ledgers, and closes #656 when
every row is proven.

**The readings before dispatch** (plan § 3, principle 3): the area's futro
(#903) is this slice's kickoff, and a stranger's proof of this brief is run
by a reader with no context before dispatch; version 2 records what each
found.
