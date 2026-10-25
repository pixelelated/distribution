# Brief: M6.P2 T16, cloud sync: the sync, backup, restore and capture core (#663)

**Version 2, 2026-10-25, the coordinator's** (D-WORKFLOW-189; version 1 the same day, corrected by a stranger's proof -- seventeen corrections, listed at the end). Written from a read-only research digest taken at `2174265e9c` (P1's tip; for these 14
paths the same bytes as `next` at `8ebaf8daad`) and from T22's brief, the
model of an Extended read slice, and T13's, the sibling whose harness this
slice is judged by. The stranger's proof of version 1 ran before dispatch (nine commands, from the scratch clone); this version records what it found. Every number below was pasted from a command's
output at the hash named beside it; the lane re-derives each one and writes
the delta where it differs.

## 1. Identity

- **Issue:** #663 `M6.P2 E1047/T16: cloud-sync-and-saves: cloud sync: the
  sync, backup, restore and capture core`, slice `cloud-sync-core` (`k: 16`)
  in `docs/reviews/slices.json`, sixteenth in `docs/reviews/order.md` (its
  § T16 paths line: *"14 paths, 8,316 lines, 7,827 read, of which 7,827
  fork-own; 0 patch and config lines; reach shipped 14"*; its `why`: *"the
  state model players' saves depend on: the highest brittleness of the
  product areas"*; kind read; lens security, brittleness, new
  functionality). **Epic:** #1047 (the cloud area: T13 #660 accepted and
  closed out, this slice, then T17 #664-or-its-number `cloud-setup-content`),
  whose futro (`docs/futros/2026-10-25-m6-cloud-sync-and-saves.md`) carries a T16 kickoff addendum written with version 1. T17 is **#664**. **Milestone:** M6.
  **Predecessors:** #346, #641, **T13 #660** (`docs/reviews/briefs/cloud-harness.md`;
  its audit on `feature/m6-cloud-harness-660`: `02-forward-audit.md`
  § Assertion shapes, 79 rows, **the oracle this slice is read against**;
  its retro's *What T16 inherits*; its 17 bugs #1057-#1070, #1081, #1092,
  #1093 fixed at `3a653eaec4`, open until `next`), **T22 #669**
  (`os-system-services.md`: the Extended recipe, the guest cycle's
  conditions, its errata), **T1 #648** (`post-update`, which runs
  `cloud_sync_helper` after an update; `backuptool`, which `cloud_backup`'s
  settings phase calls), **T4 #651** (#909: the rule `rclone-cloud-sync.md`
  is under its drift bug; the scripts are the truth where they disagree),
  **T15 #662** (`tools/last-good-scripts-test`, the busybox shims these
  scripts are run under on the host), and the Backlogs #1078 (five fixed
  waits in the harness), #1097 (the needle lint), #1098 (the harness's
  direct puts). **Beside it:** T28 in the T5 session, T15's queue in the T3
  session (D-WORKFLOW-190); neither shares a path with this slice.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346, #585 or #909, or decide a question of scope:
  those are the coordinator's, reached through #663, one question at a
  time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves, with its trace and `Already written:`
  line (D-WORKFLOW-187). A fix lands only under a stream brief the
  coordinator writes at the stage-D pause. **Every file here is the fork's
  own**: a defect is the fork's to fix, and D-WORKFLOW-209's class decision
  does not apply (nothing upstream-carried is in the slice).
- **One worktree, one session.** Branch `feature/m6-cloud-sync-core-663` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-sync-core-663`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** (`docs/reviews/{order.md,slices.json,inventory.json,status.md}`
  are there and on no other branch) with the coordinator's tip merged in
  (the briefs, the futros, the rules edited since) and the lane's pointer
  seeded; the two hashes are in the dispatch comment on #663. Until that
  comment exists the pointer is not seeded, the first command's `cat`
  fails, and nothing starts. The session is the T1 lane's
  (`m6-t1-os-launch`), which ran T1, T13 and T22; its earlier worktrees
  stay idle beside this one, read with `git show` only (T13's audit is on
  its branch: `git show feature/m6-cloud-harness-660:docs/audits/2026_10_25-epic-m6-cloud-harness/<file>`).
- **Depth: Extended** -- two seats, as T22's stage C: GPT-6 Astra at `max`
  over a trimmed, scanned packet (D-WORKFLOW-195), a probe then one
  refutation; then Gemini 4 Argon at `high` over the same packet plus the
  lane's grades of Astra, a probe then one refutation; `review-plan.json`
  records depth `extended` and both reviewers with their served models;
  **exactly four keyed `tools/council/run invoke` calls**, every other
  `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`, `--help`
  included; the runtime from `npm install --offline`, no fetch. Every seat
  item is re-read at its lines before it is graded (T22's practice, which
  caught the lane's own errors there).
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the worktree):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-cloud-sync-core-663
cat .github/sessions/saved-session-state-feature-m6-cloud-sync-core-663.md     # the pointer: the dispatch's two hashes
git status --short | wc -l                                                      # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects tools | tail -1            # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
git show feature/m6-cloud-harness-660:docs/audits/2026_10_25-epic-m6-cloud-harness/02-forward-audit.md | grep -c '^| ' # T13's tables are reachable
tools/register-check >/dev/null && echo register-ok
```

## 2. Scope

**The membership block** (T22's shape over the inventory; the slice's rule
is the area, the directory and the eleven exclusions, which are T17's):

```bash
python3 -I - <<'PY'
import json, collections, os, fnmatch, re
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
sl = json.load(open("docs/reviews/slices.json"))
k16 = [s for s in sl["slices"] if s["k"] == 16][0]; sel = k16["select"]
def expand(g):   # one level of {a,b} brace alternation, which fnmatch does not know and the inventory's slice_of does
    mm = re.search(r'\{([^{}]*)\}', g)
    if not mm: return [g]
    return [x for alt in mm.group(1).split(",") for x in expand(g[:mm.start()] + alt + g[mm.end():])]
inc = [x for g in sel["globs"] if not g.startswith("!") for x in expand(g)]; exc = [x for g in sel["globs"] if g.startswith("!") for x in expand(g[1:])]
def m(p, g): return fnmatch.fnmatchcase(p, g) or (g.endswith("/**") and p.startswith(g[:-2]))
t16 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "cloud-sync-and-saves"
       and any(m(r["path"], g) for g in inc) and not any(m(r["path"], g) for g in exc)]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t16), "lines", L(t16), dict(collections.Counter(r["reach"] for r in t16)), dict(collections.Counter(r["tier"] for r in t16)))
print(dict(collections.Counter(r["language"] for r in t16)))
CODE = {"shell", "recipe", "udev", "python", "c", "make", "systemd"}
rd = [r for r in t16 if r["language"] in CODE]
print("read", len(rd), L(rd), "fork-own", sum(1 for r in rd if r["tier"] == "fork-own"))
d = [r for r in rows if r["tree"] == "distribution" and r["path"].startswith("projects/ROCKNIX/packages/network/rclone/")]
print("the rclone directory in the inventory", len(d), L(d), "of which T17's", len(d) - len(t16), L(d) - L(t16))
os.makedirs(".qa-scratch/t16", exist_ok=True)
open(".qa-scratch/t16/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t16, key=lambda r: r["path"])))
for r in sorted(t16, key=lambda r: r["path"]): print(r["lines"], r["language"], r["path"])
PY
wc -l .qa-scratch/t16/paths.txt     # 14
```

Recorded (2026-10-25, at `2174265e9c`; the inventory there was generated at
`eb4763e3cc`): **14 paths, 8,316 lines; read 10 files / 7,827 lines
(shell 9, recipe 1); fork-own 14; shipped 14**; the 489 unread lines are the
two configuration files and the two rules files, which the security lens
reads anyway (T22's precedent for its 30 config files). The rclone directory
holds 25 inventory rows: the other 11 (8,202 lines, every one added since
the base) are T17's (`cloud_oauth`, `cloud_setup`, `cloud_remote`,
`cloud_connections.py`, `cloud_content_{backup,restore,transfer}`,
`cloud_scan`, `cloud_device_id`, `cloud_folder_validate`, `cloud_log_scrub`).
(The block's glob matcher is a stand-in for `tools/renovation-inventory`'s `slice_of`, which expands braces; version 1's did not and wrote 25 paths; the lane runs both and records the delta, as T25 did.)

**The 14, with what each is** (lines at `8ebaf8daad`; functions by
`grep -n '^[a-z_]*()'`):

| File | Lines | What it is | Functions / entry | Writes |
| --- | ---: | --- | --- | --- |
| `sources/cloud_backup` | 2,510 | the deliberate back up (settings, saves, the automatic `--automatic` sync on exit) | 45; dispatch `:2407`, `:2510` | `last-backup`, `last-settings-backup`, `last-run`; the lock `/var/run/cloud_sync.lock` (`CLOUD_SYNC_LOCK` `:456`, `take_cloud_lock:457`, `flock -n 9` `:460`); `cloud_sync.conf` read in several places |
| `sources/cloud_restore` | 2,324 | the deliberate restore; **a copy-twin of `cloud_backup`** (39 function names shared; 1,622 differing lines by `diff`; the shared ones include `take_cloud_lock`, `bounded_rclone`, `conf_valid`, `load_config`, `record_last_run`, `rules_whole`, `network_lost_during_run`) | 47; dispatch `:2207`, `:2324` | `last-settings-restore`, `last-run` (there is no `last-restore`); the same lock (`:441`, `:442`, `:445`) |
| `sources/cloud_capture` | 1,704 | the capture of a session's saves after a game and `--full` at boot: **its own `.capture.lock` only** (`:249`, `flock` fd 8 `:259`; it never takes `cloud_sync.lock`), a seal under `STAGE="${CACHE}/stage"` (`:118`), `EXIT_BOUND_MS=100000` (`:221`) | 40; dispatch `:383` | `last-capture`, `capture-failures`, `captured_at`, the stage |
| `sources/cloud_sync_helper` | 625 | run by `post-update` after an update: the one-shot `.cloud_sync-*-applied` markers, `update_cloud_sync_rules:47`, `update_cloud_sync_config:335`, `conf_valid:240`, `trim_cloud_log:510`, `main:524` | 7 | `/storage/.config/cloud_sync.conf`, the markers |
| `sources/cloud_net_ready` | 217 | is the network ready (a default route, NetworkManager's state and connectivity, the carrier); called by `cloud_capture` | 7; dispatch `:63` | nothing |
| `sources/cloud_saves_root` | 205 | which card the saves are on: `identity:70`, `write_record:94`, `wait_for:106` | 5; dispatch `:117` | `/storage/.cache/cloud_sync/saves-root` (D-CLOUD-158) |
| `autostart/102-cloud-saves` | 57 | the boot hook: `cloud_log_scrub` (T17's), then a detached `cloud_capture --full`; **no boot sync any more** (its comment also says *Capture takes no lock*, while `cloud_capture` takes `.capture.lock`: a lead) | none | nothing of its own |
| `sources/rasteratops-settings-archive` | 43 | `select_settings_archives:8`, called by `cloud_restore` | 1 | nothing |
| `sources/cloud_sync_cleanup_duplicates.sh` | 31 | a cleaner called by `cloud_backup` | none | reads `cloud_sync.conf` |
| `sources/cloud_sync.conf` / `.defaults` | 160 / 140 | 16 keys and their 16 `DEFAULT_` twins (`SAVESPATH`, `SAVES_REMOTE`, `SETTINGS_*`, `RCLONEOPTS`, `BACKUPMETHOD`/`RESTOREMETHOD`, `CONTENT_REMOTE`, ...); `cloud_sync_helper` appends what is missing | -- | the conf under `/storage/.config/` |
| `sources/cloud_sync-rules.txt` / `.defaults` | 89 / 100 | the rclone filter file, **an allowlist**: `--delete-excluded` against it is catastrophic (`rclone-cloud-sync.md`) | -- | -- |
| `package.mk` | 111 | rclone 1.75.2 as a binary zip; installs 19 scripts by `cp`, the binary and the four configuration files; **no game-end hook and no TOOLS entries** (`:90`, `:102`) | `unpack:50`, `makeinstall_target:61` | -- |

**The three stamp families, and who owns which.** The twins write `last-backup`, `last-settings-backup`, `last-settings-restore` and `last-run` (`record_last_run`, `:716` / `:722`); the capture and `cloud_saves_root` write `last-capture`, `capture-failures`, `saves-root` and the stage; **`last-sync-<origin>` is EmulationStation's** (0 hits in the 14; written by `ThreadedCloudSync` and the cards, read by five tools on 17 lines: `es-launch-memory`, `ra-offline-test`, `ra-ui-test`, `rasteratops-vm-cloud-epic`, `time-to-play`). The locks are two: one `flock` on `/var/run/cloud_sync.lock` held by the twins alone (`take_cloud_lock`), and the capture's `.capture.lock`; the exits are `readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69` (`cloud_backup:20`, `cloud_restore:21`), and the bounded run's ceiling is `SYNC_CEILING_SECONDS_FALLBACK=90` (`:57` in both twins; D-CLOUD-118/121/137). **The rule's § "The game-exit sync" names 69 and 75 at `:331-333`, and its `:375` still says `tools/cloud-round-trip` "asserts the exit-4 timing"**: #909 (T4's) owns that drift; the scripts are read as the truth and the rule's stale sentences are cited, not re-filed.

**History and the upstream relation.** `git log --no-merges
--since='2026-06-01T00:00:00Z' 8ebaf8daad -- <the 14>`: **145 commits, every
one a fork identity** (Max Engel 131, blitterbot 10, rasterabot 4); 151
all-time, the first `9f1fab30f6` (2025-07-13, ROCKNIX Team) the only
upstream one. `651150fc88` carries the directory **at the base's bytes**
(`git diff --stat c445081a59 651150fc88 -- projects/ROCKNIX/packages/network/rclone`
empty; 0 upstream commits), and no generic `packages/network/rclone`
exists: the next base merge brings nothing here. Since the base the 14 are
**+6,976 / -338** (5 added: `102-cloud-saves`, `cloud_capture`,
`cloud_net_ready`, `cloud_saves_root`, `rasteratops-settings-archive`; 9
modified); the order's *"+28,279 lines"*, *"451 commits"*, *"19 blindspot
entries"* and *"47 closed bugs"* are the whole area's figures (the digest
reproduced +28,279 / -396 over 38 files, 465 commits by glob, 37
keyword-matching entries, 32 closed `bug` issues for `"cloud sync"`): the
brief states the slice's and names the area's as the order's.

**Who calls the 14 from outside the directory** (`git grep -l` at
`8ebaf8daad`): `rocknix/sources/post-update` (runs `cloud_sync_helper`; its loop at `:81-86` removes the legacy `cloud_backup.sh`/`cloud_restore.sh` symlinks, `rm -f` at `:84`),
`rocknix/sources/scripts/runemu.sh:572` and `scripts/run` (comments: the
capture and the exit sync are EmulationStation's `FileData::launchGame`,
D-UI-095), `backuptool` (comments), and
**`misc/modules/sources/gamelist.xml:64,76`, whose tool entries still point
at `./cloud_backup.sh` and `./cloud_restore.sh`** while `package.mk`
installs no TOOLS entries and `post-update` removes the symlinks: a dead
end for Q6, recorded here so it is not re-found (its owner is the modules
package's slice, the coordinator's lead). **The ES side** is named by path
and not read: `FileData.cpp`, `ThreadedCloudSync.cpp`, `GuiCloudTransfer.cpp`,
`CloudText.{h,cpp}`, `CloudExit.h`, `GuiMenu.cpp` in the separate
`ROCKNIX/emulationstation-next` fork (pinned `16dbac5211...` on
`test/qa-integration`); they are T18's and T19's rows.

**The T16 / T17 seam.** A call site is this slice's; the callee's internals
are the callee's slice's: `cloud_backup`'s settings phase calls
`backuptool` (T1's area) and `cloud_sync_cleanup_duplicates.sh` (here);
`cloud_restore` calls `rasteratops-settings-archive` (here) and
`cloud_scan` (T17's); `102-cloud-saves` calls `cloud_log_scrub` (T17's);
`cloud_capture` calls `cloud_net_ready` (here) and `cloud_saves_root`
(here). The lane reads what each call hands over and what it does with the
answer, and names the callee's slice for the rest.

**The decisions that bind the core** (every one a Decided row; none open):
D-CLOUD-075 (bounded timeouts), 077 (fail gracefully), 078 (the last known
good state: know you succeeded, replace after, remove the superseded copy
once); **D-CLOUD-076 (a launch cancels the sync) is superseded by
D-CLOUD-109 and D-CLOUD-130 (the launch waits for a bounded sync; STOP IT
AND PLAY / KEEP WAITING)** -- the read tree implements 109/130
(`cloud_backup`'s `--automatic` path and ES's question): the lane states
which it finds and does not file the superseded design as a bug;
D-CLOUD-118/121/137 (the bounds), 126, 142, 149, 151, 153-155 (the capture
and the retention), 054, 058/064/070, 158 (the saves root is the card's
identity) → 175 (`/pixelelated`, D-CLOUD-178/179: no automatic folder
migration), 181 (integrity inputs apart from published evidence), 184;
D-QA-058 (WebDAV, SFTP and MinIO/S3 are the baseline; no hosted account);
D-QA-063 (the exit lattice; `vm-qa` prints PASSED only at 0 FAIL 0 SKIP);
D-QA-015 (nothing on a person's device or cloud). The rule
`rclone-cloud-sync.md` (895 lines, 24 headings) is read whole, with #909's
caveat.

**The blindspots this slice is read against** (`docs/blindspot-register.md`, the entries whose text is about these scripts): **10** (fixing forward without the backward fix), **22** (a probe that cannot report absence), **28** (two one-way copies as a recency resolver), **31** (a harness that writes and reads through the same wrong path agrees with itself), **33** (a sentinel exit code borrowed from the wrapped tool's exit-code space), **36** (one backend's semantics mistaken for the contract), **38** (a category-level offer read as a standing yes), **39** (a PASS over a table of dashes), **43** (a safety claim in a header comment, never tested), **45** (proven at a fixture's speed), **56** (a timing run with no cloud to reach), **62** (the writer fixed, what it had written left to heal by play), **65** (a substitute passed where the real input failed), **71** (a fixture seeded a default by its literal name), **72** (a comment held an invariant the code had stopped keeping). Each is a
question to put to the code, not a finding to copy.

## 3. Read first

- `.github/sessions/saved-session-state-next.md` and this lane's own pointer.
- **The rules this work touches** (`working-principles.md` § Pre-flight):
  `rclone-cloud-sync.md` (whole; #909's drift named), `engineering-practices.md`
  (§ Verify the artifact; § A name is not a behaviour; § Guards must fail
  closed -- the `rc=$?` rule, the fixture rule; § Fail gracefully and the
  last known good state; § Nothing runs on a person's device without their
  yes; § Integrity inputs and published evidence are separate),
  `upgrade-and-install.md` (`Already written:`; § Every fix answers what was
  already written; § Current cloud setup policy), `time-to-play.md` (the
  exit sync's 3 s budget, D-CLOUD-119; the offline benchmark, D-CLOUD-112;
  two contracts, D-CLOUD-113), `least-surprise.md`, `es-player-text.md`
  (§ Outcome vocabulary: the `>>> why` sentences the scripts print and
  `ThreadedCloudSync`'s fallback map, which change on both sides or
  neither), `generic-x64-vm-testing.md` (the guest's busybox; the image is
  the candidate, not the read tree; the credential filter),
  `bugs-are-agent-first.md`, `issue-tracking.md`, `vm-first.md`,
  `adversarial-council.md`, `council-substrate-integrity.md`,
  `worktrees.md` (superseded by § 1).
- The code-auditor skill whole; *the plan* is `docs/reviews/plan-for-the-plan.md`
  (§ 4 the questions, § 6b the renovation face, § 6c the depth rule).
- **T13's audit** (`git show feature/m6-cloud-harness-660:docs/audits/2026_10_25-epic-m6-cloud-harness/<file>`):
  `02-forward-audit.md` § Assertion shapes (the 79 rows and the three
  oracle classes: *both ends*, *synthetic*, *device report*), § Positives
  and § The streams' positives, § The guest cycle, § The second window,
  § The third window; `04-analysis.md` § Q2 (the oracle verdict: 78 rows, 24 both ends, 8 device report, `CONTRACT` outside the 78 reading both ends; its `:228` list of the 24) and § Q6; `05-punch-list.md`; `tools/t13-shapes.py` (the table's generator); `stage-e/pos*` (the twelve drivers); and the retro `docs/retros/2026-10-25-m6-cloud-harness.md`, whose bold line *What T16 inherits* (`:42`) carries the verdicts T16 may trust at `fixed-at` `3a653eaec4` and the ones it may not. The audit's tip on that branch is `0b72904621`; in a clone the branch is `origin/feature/m6-cloud-harness-660`. **T22's audit** (`git show feature/m6-os-system-services-669:...`):
  `02` § The guest cycle and § The second window (the window's shape), its
  `second-opinions/` (the two-seat recipe), `tools/t22-packet.py` (the
  packet's scan).
- `docs/reviews/order.md` § T16 and § T13, § T17; `docs/futros/2026-10-25-m6-cloud-sync-and-saves.md`.
- `docs/vm-qa-log.md` (the suite's recorded runs: `WebDAV/SFTP/MinIO-S3
  round trips each 106 PASS/0 FAIL/0 SKIP` on 2026-10-06; 108 since),
  `docs/cloud-sync-changelog.md`, `docs/cloud-save-integrity.md`.
- Decisions: the chain in § 2; D-WORKFLOW-183, 187, 189, 195, D-QA-012.
- Issues: #663, #1047, #660, #1073, #1057-#1070, #1081, #1092, #1093 (T13's
  bugs: their fixes are in `tools/`, not here), #909, #1078, #1097, #1098,
  #585. Every `gh` call carries `--repo pixelelated/distribution`.

## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`guest`, `design`); the lens is security, brittleness and new
functionality, so Q3 and Q2 lead and Q6 is small:

- **Q3 Bugs -- the lead question.** For each of the nine scripts, the
  defects the lens finds: a write that is not checked (`cmd; rc=$?` on its
  own line), a pipeline whose status is its last stage's, an unquoted
  expansion that becomes rclone's argument, a probe that cannot report
  absence (blindspot 22), a success recorded from the exit status rather
  than the artifact (blindspot 33), a lock taken without a bound or
  released on a path that is not every path, a stamp written before the
  bytes are confirmed (D-CLOUD-078), a `--delete-excluded` or `sync`
  reachable without the allowlist, a credential that can reach a log or a
  stamp (`_rclone_conf_key:522`; the `>>> why` lines; `cloud_log_scrub` is
  T17's, but what these scripts *print* is theirs), the `--automatic`
  path's bound against D-CLOUD-109/130 and the 3 s budget (D-CLOUD-119),
  the no-network exit (69) and the lock-held exit (75) reaching the card
  with the right words (`es-player-text.md`'s table). **Each defect is a
  `bug` only with its trace and its `Already written:` line** (what the
  script left in `/storage/.cache/cloud_sync/`, the stamps, the conf and
  the cloud on devices that ran it) and its VM line (which cell or which
  fixture proves it); a defect in a copy-twin is one bug naming both files.
- **Q2 Standards.** The twins: `cloud_backup` and `cloud_restore` share
  most of their function list by copy (`diff` the two once, with the
  function list; read the shared body once and every divergence whole);
  `set -o pipefail` and `set -u` where pipelines and expansions reach
  rclone; the `>>> why` sentences against `es-player-text.md`'s table and
  `ThreadedCloudSync`'s fallback map (named, not read); the conf's 16 keys
  against their 16 `DEFAULT_` twins (a key in one and not the other is a
  finding: `upgrade-and-install.md`'s first row); the rules file against
  its `.defaults`; the scripts' busybox-safety (they run under the image's
  busybox: `tools/last-good-scripts-test`'s shims are the host's way,
  D-QA-063's lattice says a host-bash verdict is not device evidence).
- **Q4 Currency.** rclone 1.75.2 as a binary zip (`package.mk`): the
  author's release `CANNOT (no network)`, `tools/fork-package-freshness`
  named; the upstream relation is nil (the directory is the fork's); the
  fixes T13 made in `tools/` that these scripts' rows now depend on
  (#1059's exit 3, #1067's cache, KILL1, A15, CAP13) are named by bug.
- **Q1 Modernize.** The copy-twin as a design (one library sourced by both,
  deferred to the coordinator; no edit); the three stamp families and who
  owns which (a design sentence); `102-cloud-saves`' detached `--full`
  capture at boot against the boot's time to play (named, measured by the
  guest's journal if the window allows).
- **Q5 Efficiency.** The scripts' size by function (the twins' 92 functions
  and how many are identical by copy); what the exit path costs
  (D-CLOUD-119's 3 s: the `--automatic` path's steps and their bounds, read
  from the code and cited from `docs/vm-qa-log.md`'s measured medians, not
  re-measured here unless the window allows one `tools/time-to-play`
  run).
- **Q6 Dead ends.** Code no row and no caller reaches: functions in the 14
  with no caller (`grep -c '<name>' <file>` over the function list; a
  function defined and never called is a row), the `gamelist.xml` tool
  entries (above; the modules package's, named), any `--` option parsed
  and never used. Removals none here: a fork-own dead function is a
  proposal on the punch list, left for the coordinator (D-WORKFLOW-209's
  last clause).
- **Q7 Clarity and structure.** Can a reader tell, from the directory and
  the rule, which script runs when (boot, a game's exit, an update, a
  menu row), under which lock, writing which stamp, and which card the
  saves are on? The three stamp families and the two locks are the test;
  the rule's drift (#909) is cited where it misleads.

A finding is one question with its evidence; `Renovation` is the category
for everything here that is not a defect. The seats (Phase 4.6) grade the
findings and the dispositions; each seat's probe comes first.

**The oracle, written into `02` § The oracle.** From T13's § Assertion
shapes, one row per assertion that reads this slice's scripts: the row, the
script and function it exercises, the oracle class, and *what makes it
FAIL* (from T13's § Positives); **the rows that read both ends** (T13's `04` `:228`: steps 2, 5, 8, 17, 18, 19, 22, 23, 27, 32; A1, A2, A8, A9, A11, A14, RETENTION; LINK2, LINK3, LINK5, LINK6; KILL1, KILL4 (conditional), KILL5 -- 24 of 78, with `CONTRACT` the 79th row reading both ends) are the verdicts this slice may trust at `3a653eaec4` and later; the **synthetic** rows (46: CAP1-14 and the other planted inputs) prove the path, not the input; the **device-report** rows (8: `run_steps.3/.4/.6/.12/.21/.25`, `prepare_device.1`, `A5`) certify the code by its own output and are not evidence about it; A5 and RETENTION SKIP today (no `cloud_reconcile`, #1057), whatever their class. The table is generated from T13's `02`
by a script under the audit folder's `tools/` (the generator asserts 79 in,
N out), not typed. This is #1047's fifth criterion, met here.

## 5. The evidence floor

1. Tracker state is never sole evidence; every cell cites a command's
   output or a file:line at `8ebaf8daad`.
2. Mechanical evidence outranks reading: `diff` of the twins, `grep -n` on
   the scripts, `git log` with the three fork identities, the harness's
   rows; a comment is the author's claim (blindspot 31).
3. **The bench is the host first, then one guest.** **Can this be done on
   the VM? Yes** -- the host for every read, diff and log; the GENERIC_X64
   guest runs the same scripts, busybox and rclone as a handheld, with
   `tools/cloud-test-backend`'s WebDAV (and SFTP) as the cloud (D-QA-058:
   no hosted account, no Dropbox, nothing offsite); **nothing on a person's
   device or cloud** (D-QA-015; blindspot 38 is this slice's own history).
   `tools/council/run invoke` runs four times with the key, the two seats'
   probes and refutations.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`; a verdict from a *device-report* row is not a PASS of
   the code under test, and the exit lattice is D-QA-063's.
5. **A verdict from the guest is a verdict on the installed file** (T22's
   lesson, `generic-x64-vm-testing.md`): the image is the M7 candidate
   `069fc2704421`, and the nine installed scripts are diffed against the
   read tree's over serial **before any verdict is used** (§ The guest
   cycle, step 1); a difference is written beside every verdict it touches.

**What never runs in this slice:** a build, a compiler, a plan generation,
a fetch, a network read beyond the four seat calls, a hosted or offsite
cloud account, `--real-roms`, `cloud-census`, a command against a handheld
or a person's cloud, a read of an M7 build root, a guest outside the one
granted window, a `tools/council/run` call with the key beyond the four,
and a change to any file under `packages/`, `projects/` or `tools/` at
stages A to D.

**The runs, with what the coordinator read** (the lane runs each at stage
A and records the exit, the wall time and the summary line; `TMPDIR` under
`/workspace/tmp/m6-t16/`):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-sync-core-663
cd "$D"; export TMPDIR=/workspace/tmp/m6-t16/tmp; mkdir -p "$TMPDIR" .qa-scratch/t16
# the membership block (§ 2) -> .qa-scratch/t16/paths.txt (14)
wc -l < .qa-scratch/t16/paths.txt                                                                     # 14
tr '\n' '\0' < .qa-scratch/t16/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD -- | tail -1        # empty
for p in $(cat .qa-scratch/t16/paths.txt); do printf '%s ' "$(git show "8ebaf8daad:$p" | wc -l)"; done | awk '{s=0; for(i=1;i<=NF;i++) s+=$i; print s}'   # 8316
# the twins (expect 45 and 47 functions; the shared list; the diff's size)
R=projects/ROCKNIX/packages/network/rclone/sources; export LC_ALL=C
git show "8ebaf8daad:$R/cloud_backup" | grep -c -E '^[a-z_]+\(\)'; git show "8ebaf8daad:$R/cloud_restore" | grep -c -E '^[a-z_]+\(\)'   # 45 47
comm -12 <(git show "8ebaf8daad:$R/cloud_backup" | grep -o -E '^[a-z_]+\(\)' | sort) <(git show "8ebaf8daad:$R/cloud_restore" | grep -o -E '^[a-z_]+\(\)' | sort) | wc -l   # 39 shared names
diff <(git show "8ebaf8daad:$R/cloud_backup") <(git show "8ebaf8daad:$R/cloud_restore") | grep -c -E '^[<>]'   # 1622 differing lines
git show "8ebaf8daad:$R/cloud_capture" | grep -c -E '^[a-z_]+\(\)'                                      # 40
# the exits, the lock, the bound (expect readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69 at :20 / :21; SYNC_CEILING_SECONDS_FALLBACK=90 at :57; take_cloud_lock :457 / :442; bounded_rclone :251 / :238; record_last_run :716 / :722)
git show "8ebaf8daad:$R/cloud_backup" | grep -n -E '^(readonly )?EXIT_|^SYNC_CEILING|^(take_cloud_lock|bounded_rclone|record_last_run)\(\)' | cut -c1-80
git show "8ebaf8daad:$R/cloud_restore" | grep -n -E '^(readonly )?EXIT_|^SYNC_CEILING|^(take_cloud_lock|bounded_rclone|record_last_run)\(\)' | cut -c1-80
git show "8ebaf8daad:$R/cloud_capture" | grep -n -E 'capture.lock|^STAGE=|^EXIT_BOUND_MS|flock' | cut -c1-80   # :118 :221 :249 :259; no cloud_sync.lock
# the conf's keys against the defaults (expect 16 and 16; every key with a DEFAULT_ twin)
git show "8ebaf8daad:$R/cloud_sync.conf" | grep -c -E '^[A-Z_]+='; git show "8ebaf8daad:$R/cloud_sync.conf.defaults" | grep -c -E '^DEFAULT_[A-Z_]+='
comm -3 <(git show "8ebaf8daad:$R/cloud_sync.conf" | grep -o -E '^[A-Z_]+=' | tr -d = | sort) <(git show "8ebaf8daad:$R/cloud_sync.conf.defaults" | grep -o -E '^DEFAULT_[A-Z_]+=' | sed 's/^DEFAULT_//; s/=$//' | sort)   # expect nothing
# the rules file against its defaults (expect 23 differing lines)
diff <(git show "8ebaf8daad:$R/cloud_sync-rules.txt") <(git show "8ebaf8daad:$R/cloud_sync-rules.txt.defaults") | grep -c -E '^[<>]'
# the callers outside the directory (expect post-update, runemu.sh, run, backuptool, gamelist.xml)
git grep -l -E 'cloud_(backup|restore|capture|saves_root|sync_helper|net_ready)' 8ebaf8daad -- projects packages | grep -v 'packages/network/rclone/' | sed 's/^8ebaf8daad://'
git show 8ebaf8daad:projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml | grep -n 'cloud_' | cut -c1-80   # :64 :76 the dead tool entries
git show 8ebaf8daad:projects/ROCKNIX/packages/rocknix/sources/post-update | sed -n '78,88p' | grep -n -E 'cloud_|symlink|rm ' | cut -c1-100   # the loop :81-86, rm -f at :84
# the stamps: who writes which (expect last-backup / last-settings-backup / last-run in cloud_backup; last-settings-restore / last-run in cloud_restore; last-capture / capture-failures in the capture; saves-root in 102-cloud-saves, the capture and cloud_saves_root; last-sync in none)
for s in last-backup last-settings-backup last-settings-restore last-run last-capture capture-failures saves-root last-sync; do printf '%s: ' "$s"; tr '\n' '\0' < .qa-scratch/t16/paths.txt | xargs -0 git grep -c "$s" 8ebaf8daad -- 2>/dev/null | sed 's/^8ebaf8daad://' | tr '\n' ' '; echo; done
# the history with the three identities (expect 145 non-merge; 145 fork; 0 other) and the upstream relation (expect empty; 0)
tr '\n' '\0' < .qa-scratch/t16/paths.txt | xargs -0 git log --no-merges --format='%h %an' --since='2026-06-01T00:00:00Z' 8ebaf8daad -- > "$TMPDIR/hist.txt"; wc -l < "$TMPDIR/hist.txt"; grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt"
git diff --stat c445081a59 651150fc88 -- projects/ROCKNIX/packages/network/rclone | tail -1; git log --oneline c445081a59..651150fc88 -- projects/ROCKNIX/packages/network/rclone | wc -l
tr '\n' '\0' < .qa-scratch/t16/paths.txt | xargs -0 git diff --shortstat c445081a59 8ebaf8daad --                     # 14 files, +6976 / -338
# T13's oracle (expect 81 table lines = header, separator and 79 rows; the Oracle column 25 both ends (CONTRACT among them) / 46 synthetic / 8 device report, some cells marked (reviewed); in a clone the ref is origin/feature/m6-cloud-harness-660, the audit's tip 0b72904621)
git show feature/m6-cloud-harness-660:docs/audits/2026_10_25-epic-m6-cloud-harness/02-forward-audit.md | awk '/^## Assertion shapes/{p=1;next} /^## /{p=0} p' | grep -c -E '^\| '
git show feature/m6-cloud-harness-660:docs/audits/2026_10_25-epic-m6-cloud-harness/02-forward-audit.md | awk '/^## Assertion shapes/{p=1;next} /^## /{p=0} p' | grep -o -E '\| (both ends|synthetic|device report)( \(reviewed\))? \|' | sed 's/ (reviewed)//' | sort | uniq -c
# the harness's names for this slice (expect cloud_backup 70, cloud_capture 66, cloud_restore 33, cloud_saves_root 18, 102-cloud-saves 5, cloud_sync_helper 3; cloud_net_ready, rasteratops-settings-archive, cloud_sync_cleanup_duplicates.sh 0)
for s in cloud_backup cloud_capture cloud_restore cloud_saves_root 102-cloud-saves cloud_sync_helper cloud_net_ready rasteratops-settings-archive cloud_sync_cleanup_duplicates.sh; do printf '%s %s ' "$s" "$(git show 8ebaf8daad:tools/cloud-round-trip | grep -c "$s")"; done; echo
# the removal rule's own check against the dispatch tip (expect empty)
git diff --stat <dispatch tip> HEAD -- packages projects tools | tail -1
```

**The guest cycle** (one window, granted on #663 when the lane asks with
its plan, **after stages A and B**; the host reads first): one GENERIC_X64
guest from M6's copy of the `069fc2704421` image (`tools/vm-pair reimage a`),
the QA WebDAV from `tools/cloud-test-backend --backend webdav` on the lane's
own isolation (`CLOUD_QA_STATE`, `CLOUD_QA_PORT`, `CLOUD_QA_NAME` under
`/workspace/tmp/m6-t16/`, as T13's), **about 20 minutes, a 30-minute
bound**:

1. **Image versus tree, first:** each of the nine shell scripts as installed
   on the guest (`cat` over serial, through the credential filter) diffed
   against `git show 8ebaf8daad:<path>`; every difference written into
   `02` § The guest cycle before any verdict below is used, and named
   beside each verdict it touches (T22's PL-05: the image is the M7
   candidate).
2. The single-device suite over WebDAV whole (`tools/cloud-round-trip` with `--dump` into the window's record; about 2 minutes), its PASS line with its counts and its exit (D-QA-063: 0 is only all ran as evidence); then the both-ends hand cells of T13's `04` `:228` that have not run on a guest since `3a653eaec4` -- LINK2, LINK3, LINK5, LINK6, KILL4 (conditional), A1, A2, A8, A9, A11, A14 (T13's three windows ran KILL1, KILL5, A15, CAP13, A5 and RETENTION: cited, not re-run) -- each with `--dump`.
3. One `tools/time-to-play --vm` run if ten minutes remain (the exit sync's
   median against D-CLOUD-119's 3 s; `docs/vm-qa-log.md`'s last figure
   cited either way).
4. Stop by pidfile (`tools/vm-pair down`), the leftover check (0 qemu of
   the lane's, 0 listeners of the lane's, 0 containers named the lane's),
   every output and quoted journal line in the record directory before the
   stop (T13's retro, proposal 2).

START and RETURN on #663 with the clock time; the coordinator mirrors both
on the host coordination file. A proof that cannot run in the window is
`CANNOT` with its reason, never a pass; a window that overruns is stopped at
the bound and said so. Reads over serial go through the dropping filter
(`grep -v -i -E 'key|pass|token|user|psk'`) for anything config-shaped and
the mask for verdict lines; the QA backend's credentials are throwaway and
still never printed.

## 6. Outputs

As T22's brief § 6, with the folder `docs/audits/<yyyy_mm_dd>-epic-m6-cloud-sync-core/`:
`00` to `05`, `second-opinions/` (both seats' plans, the manifest with its
three-way scan, each probe and refutation with provenance), `guest-cycle/`
(the window's record: the image's identity, the image-versus-tree diffs,
the suite's dump, each cell's dump, the leftover check), the lint before D,
the audit issue (`Audit: M6 T16 the cloud sync core -- N findings (...)`, a
sub-issue of #663), the bugs, and the retro at
`docs/retros/<date>-m6-cloud-sync-core.md` (**what the slice did to the two
time-to-play numbers**: the exit sync's budget is this slice's, so the
answer is measured or cited, never "nothing" by default; **what T17
inherits**: the seam list, the stamp families, the oracle table). **`02`
carries § Coverage (14), § The functions (one row per function of the three
big scripts: the file, the name, the lines, its copy-twin's line or
`own`, the oracle rows that reach it or `unrowed`), § The oracle (the
generated table from T13's 79 rows), § The stamps and locks (the three
families, the two locks, the exits and the bound, who writes and reads
each), § The configuration (the 16 keys and their defaults, the rules
allowlist, what each script reads), § The runs (every § 5 command), § The
guest cycle, § Positives, and every proof with `proved:`.** The stage-D
pause as T22's: the punch list posted on #663, the lane waits for the
coordinator's dispositions and any stream brief.

## 7. Acceptance

The checklist on #663 becomes this section at dispatch, written there by
the coordinator in place of P1's five generated ones. Every checkbox names
the artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-cloud-sync-core/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-cloud-sync-core/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: extended` and two reviewers (`gpt`, `openai/gpt-6-astra`, `max`; `gemini-argon`, `google/gemini-4-argon`, `high`); each seat's probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named; `packet-manifest.json` lists every packet file with its sha256 and the three scans' results (0 hits), and no `rclone.conf`, QA credential or stamp with a token is in the packet.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #909, #585, T17's #664, an ES slice's issue the coordinator names), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the ticked and open counts read back by the coordinator.
- [ ] `reviewed-at:` and `fixed-at:` in the checklist's header carry the lane's commits; the read is on `8ebaf8daad`'s bytes for the 14 (`git diff --stat 8ebaf8daad <reviewed-at> -- $(cat .qa-scratch/t16/paths.txt)` empty) and nothing under `packages/`, `projects/` or `tools/` changes at stages A to D (`git diff --stat <dispatch tip> <stage-D tip> -- packages projects tools` empty).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (14 paths, 8,316 lines; read 10 / 7,827; fork-own 14; shipped 14; the directory's 25 rows, 11 of them T17's -- or the deltas beside them), the four unread files named as read, the history (145 non-merge since 2026-06-01, every one a fork identity; the directory at the base's bytes upstream; +6,976 / -338 since the base) and the area figures the order carries named as the area's.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `14`.
- [ ] `02-forward-audit.md` § The functions has one row per function of `cloud_backup`, `cloud_restore` and `cloud_capture` (45 + 47 + 40 = 132, or the counts the block prints), each with its lines, its copy-twin's line or `own`, and the oracle rows that reach it or `unrowed`; the twins' shared function list (39) and their divergence in lines (1,622) are stated with the `comm` and `diff` counts under `LC_ALL=C`; every `unrowed` function of the three, and every line of the six smaller scripts and the four files no row reads, is read whole and says so in its row.
- [ ] `02-forward-audit.md` § The oracle is generated from T13's § Assertion shapes by a script under the audit folder's `tools/` (79 rows in, the Oracle column read with its `(reviewed)` marks; the rows that read this slice's scripts out, each with the script, the function, the oracle class and *what makes it FAIL*), and `04` § Q2 states the counts (25 / 46 / 8 of 79, or the deltas), names the 24 both-ends rows of T13's `04` `:228`, and says which verdicts this slice trusts at `3a653eaec4`.
- [ ] `02-forward-audit.md` § The stamps and locks names the three stamp families with their writers and readers (`last-backup`, `last-settings-backup`, `last-settings-restore` and `last-run` the twins'; `last-capture`, `capture-failures` and `saves-root` the capture's and `cloud_saves_root`'s; `last-sync-<origin>` EmulationStation's, by path, read by five tools), the two locks with their holders (`cloud_sync.lock` the twins' alone; `.capture.lock` the capture's) and every release path, the exits 69 and 75 (`:20` / `:21`) and the 90 s ceiling (`:57`) with their lines, and the `>>> why` sentences each script prints against `es-player-text.md`'s table; § The configuration lists the 16 keys against their 16 defaults (the `comm` prints nothing under `LC_ALL=C`) and the rules allowlist against its defaults (23 differing lines).
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass.
- [ ] `02-forward-audit.md` § The guest cycle records the window the coordinator granted on #663 (the comment's time), the image by file name and BUILD_ID (read from the guest), the image-versus-tree diff of the nine installed scripts before any verdict (and every verdict a difference touches named), the suite's PASS line with its counts and exit, each hand cell's verdict with its dump in `guest-cycle/`, the `time-to-play` figure or `CANNOT`, the stop by pidfile and a leftover check of 0; the window's START and RETURN are on #663.
- [ ] `00-running-log.md` shows no build, no compiler, no plan generation, no fetch (the council runtime from `npm install --offline`), no handheld, no hosted or offsite account, no `--real-roms`, no `cloud-census` run, no M7 build root read, guests only inside the granted window, exactly four `tools/council/run invoke` calls (a probe and a refutation per seat), every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent` (`--help` included), and the VM line.
- [ ] `04-analysis.md` § Q3 states each bug decision with its trace, its `Already written:` line and its VM line, and says which of D-CLOUD-076 and D-CLOUD-109/130 the read tree implements; § Q2 the twins' and the configuration's findings; § Q6 the `gamelist.xml` tool entries and every uncalled function, removals none; § Q7 the stamp-and-lock clarity answer with #909's drift cited; § Second opinion grades every item of both seats with the seats' words quoted and the re-read lines named.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest` or `design`; every punch item carries `question:`; every `bug` passes `tools/box-check --issue N` and carries its `Already written:` line.
- [ ] The retro exists at `docs/retros/<date>-m6-cloud-sync-core.md`, is posted on #663, says what the slice did to the two time-to-play numbers with the exit sync's measured or cited median against D-CLOUD-119's 3 s, and what T17 inherits.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge).

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); the stage-D pause; an explicit maintainer pause on
#663; a blocker named on #663 (a seat that fails its provenance gate twice,
a backend that will not come up on the lane's ports, two commands that
disagree, a block whose output differs from § 2's beyond the deltas it
records); a branch that differs from `8ebaf8daad` on one of the 14 at stage
A; or an execution limit, stated as such with the running log current. A
checkpoint is not a stop. An idle session says it is idle on #663, **and
does not end a turn on a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#663`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #663` or the
  guard.
- The VM question written before any proof (§ 5: yes, the host first, then
  one guest window; nothing on a person's device or cloud).
- The mini-retro at stage G, posted on #663, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 where a fix landed (did the positive exercise
  the job the fix could break: #1067's lesson is this subsystem's).
- A register row the same session for any decision the slice forces (none
  expected); D-WORKFLOW-209 is the highest Decided row on the coordinator's
  branch (D-WORKFLOW-188 on the P1 branch only; the merge unites them); a
  row this slice forces takes an ID the coordinator assigns on #663.
- `tools/ceremony-check` before every push; never `--no-verify`; a merge
  with conflicts is checked for markers; the ledgers united by whole
  entries; **a commit names its paths**; anything temporary under
  `/workspace/tmp/m6-t16/` after `df -i`, never `/tmp`; the window's
  record kept on the branch, the guest disk retired after it with the
  retirement recorded in `00` (D-INFRA-022).
- Commit messages `docs: ...`, with `Refs #663`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#663's checkboxes against their artifacts; the lint's `PASS` line;
`review-plan.json` and the four provenance files (read with the current
reader) and the manifest's scans; the audit issue's checkboxes all at an
outcome; the coverage table's row count (14), § The functions' (133 or the
block's counts), § The oracle's (generated; the counts stated); every Q3
bug with its three lines; **re-running on a clone of the branch at the tip
under `/workspace/tmp/m6-coordinator/`: the membership block and every § 5
run in full** (no guest: the window's record is read, not repeated);
`register-check` on a simulated merge with the coordinator's tip (the
ledgers united); the retro's answers; the six exit codes. The lane posts one
hand-back comment naming the tip and each artifact by path, writes
`reviewed-at:` and `fixed-at:` into #663's body, then says it is idle.
After acceptance the coordinator closes the audit issue, prompts the lane
for `audit-completion.json` and the full lint, merges the branch in its
turn after the M7 candidate (after T22's), regenerates the ledgers, posts
any #585 lines in the shape the lane wrote, and closes #663 when every row
is proven.

**The readings before dispatch** (plan § 3, principle 3): the epic's futro
(#1047) carries a T16 kickoff addendum written with this version, and a
stranger's proof of this brief is run by a reader with no context before
dispatch; version 2 records what each found.

## Version 2: what the stranger's proof found (2026-10-25)

Nine commands from the scratch clone at `2174265e9c`; the per-file line
counts, the function line numbers, the dispatch lines, the history (145,
all fork identities), the upstream relation (nil) and every path and tool
named held. The corrections:

1. The membership block's `!` exclusions are brace globs, which `fnmatch`
   does not expand: version 1's block wrote 25 paths (the 14 and T17's 11).
   The block expands braces now, as `slice_of` does.
2. The both-ends list in § 4 was not T13's: it is T13's `04` `:228` (24 of
   78), `CONTRACT` the 79th row reading both ends; the oracle grep reads the
   `(reviewed)` cells; the table has 81 lines (header and separator).
3. `cloud_capture` has 40 functions; the functions table is 132 rows.
4. There is no `last-restore`: the twins write `last-backup`,
   `last-settings-backup`, `last-settings-restore` and `last-run`.
5. The capture holds only `.capture.lock`; `cloud_sync.lock` is the twins'.
6. The exits are `readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69` at `:20` /
   `:21`; the ceiling is `SYNC_CEILING_SECONDS_FALLBACK=90` at `:57`.
7. In a clone T13's branch is `origin/...`; the audit's tip is `0b72904621`.
8. `comm` and `sort` run under `LC_ALL=C`; 39 shared names, 1,622 differing
   lines, 23 rules-vs-defaults lines are recorded.
9. The rule names 69 and 75 at `:331-333`; only `:375`'s "exit-4 timing" is
   stale.
10. Blindspots 31 and 33 are glossed by their own titles now.
11. `package.mk` installs 19 scripts by `cp`.
12. `post-update`'s removal loop is `:81-86`.
13. The conf-read counts (x10, x16) are dropped: no pattern reproduces them.
14. `last-sync`'s readers are five tools on 17 lines.
15. T17 is #664; the ES slices' issues are named by the coordinator when
    needed.
16. The retro's *What T16 inherits* is a bold line at `:42`, not a heading.
17. #663's body still carried P1's five checkboxes and "under epic #339":
    rewritten at dispatch with § 7's seventeen and the VM line.
