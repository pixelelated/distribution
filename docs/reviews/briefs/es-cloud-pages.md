# Brief: M6.P2 T18, EmulationStation's cloud pages, cards and text, with their unit tests (#665)

**Version 1, 2026-10-26, the coordinator's** (D-WORKFLOW-189). Written from a
read-only research digest (sixteen commands over the EmulationStation
checkout at the pin and the distribution's scratch clone at `2174265e9c`,
every figure with its command and population), T2's brief
(`es-launch-path.md`, the model for an ES slice), T16's and T17's briefs (the
scripts' side of the seam) and the interface futro
(`docs/futros/2026-10-23-m6-interface.md`). A stranger's proof runs before
dispatch; version 2 records what it found (`docs/reviews/plan-for-the-plan.md`
§ 6b). The lens is **brittleness and new functionality**; the depth reason is
that `ThreadedCloudSync` and `CloudTransferJob` are on the plan's state list:
they are the cloud sync's EmulationStation half, the card and the page every
player sees a sync through.

## 1. Identity

- **Issue:** #665 `M6.P2 E339/T18: interface: EmulationStation's cloud
  pages, cards and text, with their unit tests` -- **retitled `E700/T18` and
  re-parented under the interface epic #700 at dispatch** by the
  coordinator (it carries `E339` until then); slice `es-cloud-pages`
  (`k: 18`) in `docs/reviews/slices.json`, eighteenth in
  `docs/reviews/order.md` (its § T18 paths line: *"30 paths, 11,193 lines,
  11,116 read, of which 11,116 fork-own; 0 patch and config lines; reach
  shipped 30"*; its `why`: *"36 interface files name the cloud scripts
  (cross-reference.md); the cards, the transfer page and the text rules are
  the fork's; the unit tests ride here because most test `CloudText`; a
  test of a T2 or achievements subject is read with it as context"*; kind
  read; lens brittleness, new functionality; depth Extended). **Epic:** #700
  (the interface: T2 #649 accepted and closed out; this slice; T20, T21,
  T26, T31 to T37, T44 after), whose futro takes a T18 kickoff addendum
  written with this version. **Milestone:** M6. **Predecessors:** #346,
  #641, **T2 #649** (`es-launch-path.md`: the two-worktree shape, the pin,
  `FileData::launchGame`'s question over a running sync, `ProxyCards`,
  `main.cpp`'s startup sync -- the callers of this slice's classes),
  **T16 #663** (`cloud-sync-core.md`: `cloud_backup` and `cloud_restore`,
  whose `>>> why`, `>>> doing`, `>>> tier` lines this slice parses; its
  stage-B finding that the rule's rc 3/4 and 7/8 sentences differ from the
  scripts'), **T17 #664** (`cloud-setup-content.md`: `cloud_scan`'s
  `>>> unit` and `>>> removed`, `cloud_setup:797`'s sentence changed by its
  S6 to `A SYNC IS ALREADY RUNNING`, `backuptool:1495`'s D-UI-117 sentence,
  `--set-systems`' new exit 1 -- all routed to this slice on #665), **T4
  #651** (#909: `es-player-text.md` is under its drift bug; the shipped
  strings are the truth where they disagree). **Beside it:** whatever lane
  runs when this is dispatched (D-WORKFLOW-190); no slice shares a path.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, **bump
  the EmulationStation pin in the distribution**, file a Backlog issue,
  post on #346, #585 or #909, or decide a question of scope: those are the
  coordinator's, reached through #665, one question at a time. What it does
  file: its own audit punch-list issue (stage D) and a `bug` issue for a
  defect it proves, with its trace and `Already written:` line
  (D-WORKFLOW-187). A fix lands only under a stream brief the coordinator
  writes at the stage-D pause, **on the ES branch**, and reaches an image
  only when the coordinator moves the pin at integration
  (`device-builds.md` § Iterating on EmulationStation: `EMULATIONSTATION_SRC`
  only mounts; the pin is what builds). **Every one of the 30 files is the
  fork's own by origin** (none exists at the merge base, § 2), so a defect
  is the fork's to fix and D-WORKFLOW-209 reaches nothing here.
- **Two worktrees, one session** (plan § 11 item 4; D-WORKFLOW-010: an ES
  slice runs in an ES worktree with the distribution checkout's rules):
  - **The distribution worktree**, where the audit artifacts, the work log,
    the pointer and every ceremony live: branch `feature/m6-es-cloud-pages-665`
    at `/workspace/repos/pixelelated/distribution.worktrees/m6-es-cloud-pages-665`,
    created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
    `2174265e9c`** (`docs/reviews/{order.md,slices.json,inventory.json,status.md}`
    are there and on no other branch) with the coordinator's tip merged in
    (the briefs, the futros, the rules edited since, D-CLOUD-185) and the
    lane's pointer seeded; the two hashes are in the dispatch comment on
    #665. Until that comment exists the pointer is not seeded, the first
    command's `cat` fails, and nothing starts. The primary checkout is
    `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025);
    `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7
    lane's, read only, never named in a run; **no M7 build root read**. The
    other ES checkouts under `~/Development/emulationstation-next.worktrees/`
    are other lanes' (the `m7-*` ones M7's): read with `git -C ... show`,
    never checked out or written.
  - **The EmulationStation worktree**, where the sources are read and the
    fixes are made:
    `/home/max/Development/emulationstation-next.worktrees/m6-es-cloud-pages-665`,
    branch `feature/m6-es-cloud-pages-665`, created by the coordinator at
    dispatch from **the pin `16dbac5211eea7e70db7394372033be2be7df829`**
    (what `projects/ROCKNIX/packages/ui/emulationstation/package.mk`'s
    `PKG_VERSION` names at `8ebaf8daad`, and what the image the guest boots
    was built from -- the window's first step checks that, § 5). The clean
    checkout at the pin that the research read is `.../qa-integration`
    (`test/qa-integration`, HEAD `16dbac5211`): read only. The ES repository's
    remote `upstream` is ROCKNIX's; its `upstream/master` tip is the merge
    base `bccd71570`, and the pin is 725 commits ahead of it and 0 behind.
- **Depth: Extended** -- two seats, as T16's and T17's stage C: GPT-6 Astra
  at `max` over a trimmed, scanned packet (D-WORKFLOW-195; T17's first
  packet was trimmed from 437 KB to 295 KB before any seat because Argon
  failed at that size on T30), a probe then one refutation; then Gemini 4
  Argon at `high` over the same packet plus the lane's grades of Astra, a
  probe then one refutation; `review-plan.json` records depth `extended`
  and both reviewers with their served models; **exactly four keyed
  `tools/council/run invoke` calls**, every other `tools/council/run` call
  with `COUNCIL_ENV_FILE=/nonexistent`, `--help` included; the runtime from
  `npm install --offline`, no fetch. The packet's three-way scan: these
  files carry `MaskSecretsTests.cpp` and the credential words in comments
  and test names, so every hit gets a disposition by shape and a value
  stops the packet; a test fixture's secret-shaped literal is itself a
  finding (#1061's shape). Every seat item is re-read at its lines before
  it is graded.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the distribution worktree, `W` the ES
  worktree):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-cloud-pages-665
cat .github/sessions/saved-session-state-feature-m6-es-cloud-pages-665.md      # the pointer: the dispatch's hashes
git status --short | wc -l                                                      # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                  # empty: the distribution is read at next's bytes
git diff --stat 8ebaf8daad HEAD -- tools | tail -1                              # P1's own 15 files under tools/ (#641, #646, #810), nothing else
grep -E '^PKG_VERSION=' projects/ROCKNIX/packages/ui/emulationstation/package.mk  # the pin, 16dbac5211...
W=/home/max/Development/emulationstation-next.worktrees/m6-es-cloud-pages-665
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l; git -C "$W" branch --show-current   # the pin; 0; feature/m6-es-cloud-pages-665
git -C "$W" merge-base upstream/master HEAD; git -C "$W" rev-list --count upstream/master..HEAD   # bccd71570; 725
tools/register-check >/dev/null && echo register-ok
tail -n 6 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200              # who holds the host; M7 writes timestamped lines, not == blocks
```

## 2. Scope

**The membership block** (T2's shape over the inventory: the rows whose
`tree` is `es` and whose path matches the three globs; the inventory's
`slice_of` is the authority, this is the re-derivation):

```bash
python3 -I - <<'PY'
import json, re, collections, os
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
pat = re.compile(r"^es-app/src/(CloudText|ThreadedCloudSync|CloudTransferJob)\.[^/]+$|^es-app/src/guis/GuiCloud[^/]*$|^es-app/tests/.+$")
t18 = [r for r in rows if r["tree"] == "es" and pat.match(r["path"])]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t18), "lines", L(t18), dict(collections.Counter(r["reach"] for r in t18)), dict(collections.Counter(r["tier"] for r in t18)))
print(dict(collections.Counter(r["language"] for r in t18)))
CODE = {"c++", "c-header", "cmake", "python", "c"}
rd = [r for r in t18 if r["language"] in CODE]
print("read", len(rd), L(rd), "unread", [r["path"] for r in t18 if r not in rd])
src = [r for r in t18 if r["path"].startswith("es-app/src/")]; tst = [r for r in t18 if r["path"].startswith("es-app/tests/")]
print("sources", len(src), L(src), "tests", len(tst), L(tst))
os.makedirs(".qa-scratch/t18", exist_ok=True)
open(".qa-scratch/t18/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t18, key=lambda r: r["path"])))
for r in sorted(t18, key=lambda r: r["path"]): print(r["lines"], r["language"], r["tier"], r["path"])
PY
wc -l .qa-scratch/t18/paths.txt     # 30
W=/home/max/Development/emulationstation-next.worktrees/m6-es-cloud-pages-665; PIN=16dbac5211eea7e70db7394372033be2be7df829
while IFS= read -r p; do printf '%6d %s\n' "$(git -C "$W" show "$PIN:$p" | wc -l)" "$p"; done < .qa-scratch/t18/paths.txt | awk '{s+=$1} END {print "wc -l lines", s}'   # 11193
while IFS= read -r p; do git -C "$W" cat-file -e "bccd71570:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t18/paths.txt | wc -l   # 0: all fork-own by origin
```

Recorded (2026-10-26, from the digest's `ls-tree -r -z` at the pin and
`git show | wc -l`; the inventory's figures the block prints): **30 paths,
11,193 lines; read 29 / 11,116 (c++ 23, c-header 5, cmake 1; `README.md`'s
77 lines are the unread file, read anyway); tier fork-own 30; shipped 30;
none exists at the merge base `bccd71570`** (`git cat-file -e` on each).
**Eight sources, 5,429 lines; 22 test files, 5,764 lines.** The inventory
records ES paths as `tree: "es"` (1,114 rows); the membership is `tree ==
"es"` and the path regex, as T2's.

**What the `GuiCloud*` glob reaches, and what it does not.** It selects
**only `GuiCloudTransfer.{cpp,h}`**. The setup wizard, the scan launch, the
connections and folder pages and the three cloud rows live in
`es-app/src/guis/GuiMenu.cpp` (7 `new GuiCloudTransfer` sites, 3
`ThreadedCloudSync::start` sites, seventy-odd script invocations), which is
**T26's**; `main.cpp:666-691` (the startup sync), `FileData.cpp:1310` (the
launch's question), `ProxyCards.cpp:34/118` and `JourneyTiers.h:142-151` are
T2's and the achievements slice's. **None of the eight sources invokes a
script by path**: `mCommand` is composed by the callers and handed in. So
this slice reads the card, the job, the page and the text as a library
whose callers are elsewhere, and names each caller's slice for what it hands
over.

**Read as context, not membership (the coordinator's answer to the digest's
membership question):** the ES repository's top-level `tests/app-unit/**`
(10 files, among them `ProxyCardsTests.cpp`, `JourneyTiersTests.cpp`,
`TextFitTests.cpp` and `fakes/ThreadedCloudSync.h`, a fake of this slice's
class) and the Python harnesses under `tests/` that name this slice's
subjects (`cloud-oauth-lifetime.py`, `cloud-sync-last-run.py`,
`maintenance-why.py`, `cloud-set-systems-quoting.py`, `cloud-gated-row.py`,
`cloud-folder-reopen.py`, `cloud-content-selection.py`, `cloud-oauth-await.py`).
No glob of the slice selects them; the coverage table stays at 30 and a
second table, § Context read, lists them with what each tests and whether
it ran. Re-cutting the slice is the coordinator's, not done.

**The 30, with what each is** (lines at the pin by `wc -l`; the digest's
functions by declaration regex for `CloudText.h`):

| File | Lines | What it is |
| --- | ---: | --- |
| `es-app/tests/unit/CloudTextTests.cpp` | 1,784 | 70 `TEST_CASE`s, 711 checks: every declared `CloudText` function |
| `es-app/src/CloudText.cpp` | 1,409 | the pure string code (40 declared functions in the header): `whySentences` (39 rows, 38 unique), `localizedWhy` / `isKnownWhy` (`:469-485`), `classifyProtocolLine` (`:561-616`: `>>> pid`, `doing`, `why`, `offer`, `tier`, `unit`, `removed`), the stamp map (`:186-189`), exit 75 (`:1386`), `outcomeCandidates`, `chooseThatFits`, `liveLine`, `cleanLine` |
| `es-app/src/guis/GuiCloudTransfer.cpp` | 1,077 | the fourth-tier page (D-UI-078): BACK is CANCEL while cancellable with per-kind confirm text, OK is TRY AGAIN; `delete this` at `:207` and `:328`; `postToUiThread([page, alive]...)` at `:1070`; every line fitted by `font->sizeText` against `mLineWidth` (`:585-1022`); `t->setSize(w, 0)` at `:74`; 67 `_( )` strings; constructed 7 times in `GuiMenu.cpp` and once in `main.cpp` |
| `es-app/tests/unit/AtomicFileTests.cpp` | 1,090 | 24 cases / 130 checks: `AtomicFileUtil` against real files (context: T2's and the state slice's subject) |
| `es-app/src/ThreadedCloudSync.cpp` | 949 | the automatic sync's card: `createAsyncNotificationComponent(true)` (`:46`), origins None / Startup / Exit / Manual, `whyForCode` (`:80-98`), the `popen("setsid sh -c ...")` at `:208` **without** the `trap '' PIPE` the job has, `cancelForLaunch` (`:784-862`: SIGTERM then SIGKILL at 1.5 s of a 2 s budget, a 20 ms spin), the 1.5 s / 5 s linger (`:731`), `ProxyCards::afterSync` at `:755`, the stamps `last-sync-<startup|exit|manual>` written tmp + `std::rename` (`:892-949`) and read by `stat` inode and mtime; 50 `_( )` strings; the thread detached (`:56`, PL-069) |
| `es-app/src/CloudTransferJob.cpp` | 751 | the page's worker: one shared job at a time (`sMutex`), `popen("setsid sh -c '{ trap '' PIPE; ... }'")` at `:637-638`, parses `Transferred:` / `Checks:` / ` * name:` and the glued block, 0 and 9 success, 130 stopped, `requestStop` SIGTERM / SIGKILL to the group (`:100-161`) |
| `es-app/src/CloudText.h` | 589 | the declarations and the long comments that are the contract |
| `es-app/tests/unit/SystemConfTests.cpp` | 506 | 10 cases / 76 checks (context: the settings writer, the state slice) |
| `es-app/tests/unit/WifiTextTests.cpp` | 352 | 19 / 136 (context: the Wi-Fi rows) |
| `es-app/tests/unit/OfflineAchievementsTextTests.cpp` | 350 | 15 / 132 (context: the achievements slice) |
| `es-app/tests/unit/MaskSecretsTests.cpp` | 242 | 12 / 85: the credential mask (its fixtures are run-time built or they are findings) |
| `es-app/src/guis/GuiCloudTransfer.h` | 236 | the page's class and its comment |
| `es-app/src/CloudTransferJob.h` | 217 | the job's members: `mUnitLabel`, `mDoing`, `mChecking`, the atomics `mPid`, `mStoppedForGame`, `mStoppedByPlayer`, `mStopSignal`, `mSignalSent` |
| `es-app/src/ThreadedCloudSync.h` | 201 | the card's class; its comment at `:93-98` still quotes the rule's older why words |
| `es-app/tests/unit/SaveStateJobQueueTests.cpp` | 170 | 10 / 66 (context) |
| `es-app/tests/unit/CaptureRotationTextTests.cpp` | 164 | 8 / 71 (context) |
| `es-app/tests/unit/CMakeLists.txt` | 159 | four binaries with the host compiler; rapidjson required, fails closed; `-DES_BUILD_TESTS=ON` off by default so the image build never sees it |
| `es-app/tests/unit/TimeTextTests.cpp` | 149 | 11 / 44 |
| `es-app/tests/unit/CheevosRetryTests.cpp` | 112 | 7 / 27 |
| `es-app/tests/unit/LaunchCommandTests.cpp` | 103 | 8 / 21 |
| `es-app/tests/unit/CloudFolderValidationTests.cpp` | 84 | 4 / 37: T17's validator's ES side |
| `es-app/tests/unit/AtomicFileWin32Tests.cpp` | 80 | 2 / 12 |
| `es-app/tests/unit/README.md` | 77 | the tests' contract (read, unscored) |
| `es-app/tests/unit/OfflineProxyUrlTests.cpp` | 65 | 4 / 28 |
| `es-app/tests/unit/CheevosIndexTests.cpp` | 62 | 6 / 24 |
| `es-app/tests/unit/DisplayAspectTextTests.cpp` | 54 | 3 / 31 |
| `es-app/tests/unit/CommandLineTests.cpp` | 53 | 2 / 10 |
| `es-app/tests/unit/LogPolicyTests.cpp` | 50 | 3 / 16 |
| `es-app/tests/unit/TabStopsTests.cpp` | 50 | 3 / 8 |
| `es-app/tests/unit/fakes/SDL_timer.h` | 8 | the clock double |

**221 `TEST_CASE`s in 19 test files**; 70 of them `CloudText`'s and 151 the
context subjects' (T2's, the achievements', the state slice's), read as
context for what they fake and what they prove.

**History** (`git -C <es> log --no-merges bccd71570..16dbac5211 -- <the
30>`): **181 commits**, **Max Engel 170, blitterbot 9, rasterabot 2**, from
2026-07-25 to 2026-10-11 (2 in July, 166 in September, 13 in October);
`ThreadedCloudSync.cpp` 56, `GuiCloudTransfer.cpp` 47, `CloudText.cpp` 39,
`CloudTextTests.cpp` 37, `CloudText.h` 35. The newest ten are M7's October
work on these files: `c8dc72cf9` (manage cloud connections and network
recovery), `1d76b3da7` (refused folder paths, #524), `1d5397fda` (translate
folder check failures and name scan contention), `baeea2a8c`, `1272b3405`,
`300f97d28` (replace migration with manual folder setup), `8beab9090`,
`bab4df649`, `39f888354` (#320), `e108699ea` (fork #363). **M7's branches
beyond the pin** (`m7-cloud-connections`, `m7-cloud-path-reasons`, ...) are
cited by issue number where a finding meets them and never read: the read
is the pin's bytes.

**The seam with the scripts (T16, T17), from this side.** The eight sources
run no script; they parse what the callers' commands print. What ES knows:
the protocol markers above; the exits `0` and `9` as success, `130` as
stopped, `75` as the lock (`CloudText.cpp:1386`), and `whyForCode`'s map
(`ThreadedCloudSync.cpp:84-93`: 3/4 `COULDN'T FIND YOUR CLOUD FOLDER`, 5 and
124 `YOUR CLOUD STOPPED ANSWERING`, 7/8 `YOUR CLOUD WOULDN'T TAKE THE
FILES`, 69 `YOU'RE NOT ONLINE`, 75 `A SYNC IS ALREADY RUNNING`, 130 `IT WAS
STOPPED`, NoFolder `YOUR CLOUD FOLDER ISN'T SET UP YET`, default `SOMETHING
WENT WRONG`); the stamps it writes (`last-sync-<origin>`, one line, the why
as printable ASCII) and reads (`readStamps` by `stat`, `CloudText.cpp:186-189`
maps each script to its stamp names). **The why table against the scripts**
(the digest's command 14, both sides at their pins): 37 literal script
sentences, 38 ES sentences (39 rows, one duplicate), **32 in both**; the
table lacks `ANOTHER CLOUD SYNC IS RUNNING` (`cloud_setup:797`, which T17's
S6 changes to `A SYNC IS ALREADY RUNNING` -- the table lacks that too, since
`A SYNC IS ALREADY RUNNING` is `whyForCode`'s word and the card's SKIPPED
string, not a `whySentences` row), `THIS BACKUP HOLDS FILES A RESTORE CAN'T
PUT BACK` (`backuptool:1495`, D-UI-117's proposed words) and one sentence
the digest's credential filter withheld (the lane re-derives it); six table
rows no script prints as a literal (`CHOOSE A CONNECTION BEFORE USING CLOUD
TOOLS`, `IT WAS STOPPED`, `SOME FILES DIDN'T FINISH`, `THE CLOUD TOOK TOO
LONG - IT'LL TRY AGAIN NEXT TIME`, `YOU WENT OFFLINE PART-WAY THROUGH`,
`YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED` -- some built from variables by
the eight `say_why "$var"` emitters the digest's population missed); and
**three wordings for exit 75** across ES, `cloud_setup` and `cloud_scan`.
**The fallback map's drift is in the rule and the header, not the code:**
`ThreadedCloudSync.cpp:84-86` and `cloud_scan:123-125` agree on the shipped
words; `es-player-text.md` § Outcome vocabulary and `ThreadedCloudSync.h:94-96`'s
comment still carry `WASN'T FOUND` and `REFUSED THE TRANSFER`, and the
rule's claim that the six are "duplicated verbatim" on both sides is false
of the shipped six. The rule's half is #909's (the coordinator posts the
line); the header comment is this slice's.

**The decisions that bind these surfaces** (every one a Decided row; 42 of
the 108 D-UI rows name a card, a page, a wizard or an outcome): **D-UI-022**
(the vocabulary), **023** (two lines per row), **028** and **030** (the
outcome words: `COMPLETED`, `COULDN'T FINISH - <why>`, `SKIPPED - <reason>`;
no middle word), **035** (candidates longest first, the last fits any
panel), **040** (the automatic cards say *sync*), **051** (English and
French), **052** (a composed sync's halves), **060** and **070** (the
transfer page's shape before D-UI-078), **075**, **078** (long work on a
foreground page with CANCEL; the fork's lanes only, D-UI-079), **085**,
**093** (one floating surface at a time), **095** and **096** (anything
automatic over the network is shown; the launch's question in one shape),
**107** (a card's title names the thing, its line says what happened),
**108** (the transfer line: file n of m, x of y); **D-CLOUD-109** (a launch
waits for a bounded sync), **113** (two contracts), **119** (the exit
sync's 3 s budget, which `tools/time-to-play` fails a run against), **129**
and **130** (the question over a running sync or transfer: STOP IT AND
PLAY / KEEP WAITING); **D-WORKFLOW-155/156** (every ES change with its flow
and screenshot evidence; the menu map updated in the same change,
D-UI-039); **D-QA-015**, **D-QA-058**, **D-QA-063**.

**The blindspots this slice is read against:** **13** (assumed-done), **22**
(a probe that cannot report absence: a `>>>` line the parser does not know,
a stamp missing), **35** (a card composed with no row to draw its action
on), **39** (a tool that reports numbers fails when they are missing), **44**
(a layout computed from what it last produced), **49** (an ES edit no
compiler saw before the pin moved), **35**, and the four ES rules'
case-studies (`es-code-traps.md`: the button bar, the piped progress, the
xgettext comment, the padded width, the three font facts, the `exists()`
cache, the use after free in a rescan).

## 3. Read first

1. `docs/reviews/plan-for-the-plan.md` § 6b (the per-slice procedure and the
   brief practice) and § 6c; `docs/reviews/order.md` § T18, § T2, § T16,
   § T17; `docs/futros/2026-10-23-m6-interface.md` whole, its T2 addendum
   and this slice's.
2. The four ES rules whole -- `es-native-ui.md`, `es-player-text.md`,
   `es-ui-style-guide.md`, `es-code-traps.md` -- and `docs/es-menu-map.md`
   § Cloud (our subtree) (`:231`, with § Visual evidence and flow coverage
   `:26`) and `docs/conflict-wizard-ia.md` (whether a conflict wizard exists
   in any ES source at the pin is a § 5 question); `engineering-practices.md`
   § Guards must fail closed, § Verify the artifact, § Change stays inside
   the fork's lanes; `time-to-play.md`; `vm-first.md`;
   `bugs-are-agent-first.md`; `generic-x64-vm-testing.md`;
   `device-builds.md` § Iterating on EmulationStation and § Reading a crash.
3. T2's audit on its branch (`feature/m6-es-launch-path-649`:
   `docs/audits/*es-launch-path*/02-forward-audit.md` § the launch's question
   over a sync, `04-analysis.md` § Q5 the two time-to-play numbers), T16's
   `02` § The oracle and § The stamps and locks, T17's `02` § The secrets'
   paths (what reaches a screen) -- each with `git show <branch>:<path>`.
4. The eight sources whole, in this order: `CloudText.h` then `CloudText.cpp`
   (the contract and the pure code), `CloudTransferJob.h` then `.cpp` (the
   protocol and the pipe), `GuiCloudTransfer.h` then `.cpp` (the page),
   `ThreadedCloudSync.h` then `.cpp` (the card); then `CloudTextTests.cpp`
   whole against the functions it names, `CMakeLists.txt` and `README.md`;
   then the 18 context test files for what they fake (`fakes/SDL_timer.h`)
   and prove; then the context read of § 2 (the callers in `GuiMenu.cpp`,
   `main.cpp`, `FileData.cpp`, `ProxyCards.cpp`, `JourneyTiers.h` for what
   they hand in; `tests/app-unit/**` and the Python harnesses for what they
   test of this slice).
5. The tools: `tools/es-syntax-check` (its header: `ES_BUILD_ROOT`, the exit
   2 conditions at `:68-86`; its default root is the legacy layout, #640),
   `tools/vm-visual-qa` and the eight cloud walks under `tools/vm-walks/`
   (`run-transfer.steps`, `run-transfer-frames.steps`, `restore-page.steps`,
   `m7-cloud-sync.steps`, `confirm-cloud-folder.steps`,
   `to-manage-cloud-storage.steps`, `to-change-cloud-folder.steps`,
   `cloud-epic`), `tools/frame-diff`, `tools/time-to-play`, `tools/es-untranslated`,
   `tools/es-menu-map-check`, `tools/vocabulary-check`.

## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a proof
in `02` (a `proved:` cell: `tree`, `history`, `fixture`, `unit-test`,
`pin-binary`, `design`); the lens is brittleness and new functionality, so
Q3 and Q2 lead and Q6 is small:

- **Q3 Bugs -- the lead question, in three families.** **(a) The protocol
  under a pipe.** Every line the job and the card read comes through
  `popen` from a `setsid sh -c` wrapper: the job's wrapper sets `trap ''
  PIPE` (`CloudTransferJob.cpp:637`) and the card's does not
  (`ThreadedCloudSync.cpp:207`) -- what happens to each when ES closes the
  pipe early (a cancel, a quit)? `classifyProtocolLine` knows seven
  markers: what does a `>>>` line it does not know become -- a why, a
  live line, nothing (blindspot 22)? The rclone parsing (`CloudTransferJob.cpp:475-531`):
  the 80-column cut, the glued block, the `%3d%%` separator, the U+2026
  shortening (`es-code-traps.md` § What rclone's piped progress actually
  looks like) -- each with a fixture line through the real parser
  (`CloudTextTests.cpp` has cases; name which trap each covers and which
  has none). **(b) Lifetimes and threads.** The job outlives the page by
  design (`CloudTransferJob.h`'s comment); the page `delete this` at `:207`
  and `:328` and posts `[page, alive]` at `:1070`; the card detaches its
  thread (`:56`) and deletes itself after a linger (`:731`); `cancelForLaunch`
  (`:784-862`) spins at 20 ms under `sInstanceLock` with a 2 s budget and
  SIGKILLs at 1.5 s -- against D-CLOUD-119's 3 s exit budget and
  D-CLOUD-109's bounded wait, is the budget the right one, and what does
  the player see at 1.5 s? `SystemData::rescanChangedFolders` posted from
  the page's callback at `:335` (#246's shape: who holds a pointer to what
  it deletes?). A test of each lifetime exists in `tests/app-unit/`
  (`fakes/ThreadedCloudSync.h`) or does not: say which. **(c) The words.**
  Every `_( )` string of the eight files (220) against `es-player-text.md`:
  the three outcome words, the why sentences, the in-place clauses, TRY
  AGAIN by position never by letter, the serial comma, *back up* / *backup*,
  Wi-Fi; `outcomeCandidates` (`ThreadedCloudSync.cpp:700`, D-UI-035) and
  every `chooseThatFits` / `sizeText` fit at 640x480 (a frame from the guest
  is the proof; `GuiCloudTransfer.cpp:74`'s `setSize(w, 0)` is the padded
  width trap); the why table against the scripts (§ 2: the rows it lacks,
  the three wordings for 75, the eight variable emitters re-derived); the
  header comment at `ThreadedCloudSync.h:94-96` against the code; the nine
  non-ASCII lines in `GuiCloudTransfer.cpp` and one each in
  `CloudTransferJob.{cpp,h}` -- string literals or comments near a `_( )`
  (the xgettext trap; `ThreadedCloudSync.cpp:167`'s `"\xC2\xB7"` escape is
  the pattern). **Each bug carries its trace, its `Already written:` line
  (a stamp an older card wrote in another shape; a `rclone.conf` or conf
  the page reads; a setting the wizard saved) and its VM line**; a fix is a
  stream on the ES branch, proven by `es-unit-tests` where the code is pure
  and by a frame at 640x480 where it draws, and reaches an image only when
  the coordinator moves the pin.
- **Q2 Standards.** The ES rules as a checklist over the eight files: the
  four surface tiers and which each surface is (`es-native-ui.md`); the
  confirmation shape and the back-button accelerator (`es-ui-style-guide.md`
  § Confirmations: the page's CANCEL confirm); `getHelpPrompts` accurate on
  every state; the three type sizes; `Utils::FileSystem::exists` nowhere in
  the eight (the digest: 0 calls -- the stamps go through `stat`), with the
  callers' `exists()` reads named as T26's; the `>>> why` sentences in
  English and French (`tools/es-untranslated` over the pin; the French
  catalog's rows for the 38); the unit tests' own standards (`CMakeLists.txt`
  fails closed without rapidjson; a fixture never carries a secret-shaped
  literal, #1061).
- **Q1 Modernize.** `CloudText` is the shape the rules ask for (pure code,
  tested); the card and the job parse the same protocol with two readers
  (`ThreadedCloudSync::run` and `CloudTransferJob::handleLine`): name the
  seam and what a shared reader would change, as a proposal. The two
  `popen` wrappers differing by a `trap` is the smallest version of the
  same question.
- **Q4 Currency.** The pin against ROCKNIX's `upstream/master` (the merge
  base is its tip; nothing upstream touches these files); M7's October
  commits on these files beyond the pin (`c8dc72cf9` and after on the
  `m7-*` branches: cited by number, never read); T17's S6 and S5 changing
  what the scripts print and exit (routed on #665); the ES syntax check's
  default root naming the legacy layout (#640).
- **Q5 Efficiency.** The two time-to-play numbers (`time-to-play.md`,
  D-CLOUD-098): the exit sync's card and `cancelForLaunch`'s 2 s budget
  against D-CLOUD-119's 3 s; `tools/time-to-play --vm` on the guest if the
  window allows, else `docs/vm-qa-log.md`'s last medians cited; the 20 ms
  spin and the 1.5 s / 5 s lingers as the costs they are.
- **Q6 Dead ends.** Functions of `CloudText.h` no caller in `es-app/src`
  reaches and no test names (the 40 declared against `git grep -w` over
  `es-app/src` and the tests); a `>>>` marker parsed and never produced by
  any script (`>>> tier` is GuiMenu's composition; `>>> offer` read by
  both); test cases whose subject is gone. Removals none: a dead function is
  a proposal on the punch list for the coordinator.
- **Q7 Clarity and structure.** Can a reader tell, from the four pairs of
  files and the rules, which surface shows a sync (the card) and which a
  transfer (the page), which words each may use, what each parses, and how
  each ends? The protocol table (§ 6) and the why table are the test; the
  rule's drift (#909) and the header comment's are cited where they
  mislead.

A finding is one question with its evidence; `Renovation` is the category
for everything here that is not a defect. The seats grade the findings and
the dispositions; each seat's probe comes first.

## 5. The evidence floor

1. Tracker state is never sole evidence; every cell cites a command's
   output or a file:line at the pin.
2. Mechanical evidence outranks reading: `es-unit-tests` run on the host,
   `tools/es-syntax-check` on every edited file, a frame at 640x480 from the
   guest, `git log` with the three fork identities, `git grep -w`; a comment
   is the author's claim (blindspot 31) -- the header comment at
   `ThreadedCloudSync.h:94-96` is the case in point. **A fixture is built at
   run time, never a secret-shaped literal at rest** (#1061).
3. **The bench is the host first, then one guest.** **Can this be done on
   the VM? Yes** -- the host for every read, the unit tests (`es-app/tests/unit`
   builds four binaries with the host compiler and no toolchain; rapidjson
   from an M6 GENERIC_X64 build root's `build/rapidjson-*/include`) and the
   syntax check (`tools/es-syntax-check` with `ES_BUILD_ROOT` set to an M6
   root that holds an `emulationstation-*` build directory -- five M6
   worktrees hold a `build.pixelelated-GENERIC_X64.x86_64`; whether any
   holds the ES build directory is **not verified** and is a § 5 run: a
   `CANNOT` with the tool's exit-2 line is the honest answer if none does,
   and the fix's compile check then waits for the integration build);
   **the GENERIC_X64 guest runs the pin's binary at 640x480** with
   `tools/cloud-test-backend`'s WebDAV as the cloud (D-QA-058), the eight
   cloud walks, `tools/vm-visual-qa` for frames, `tools/frame-diff` against
   the accepted baseline, `tools/time-to-play --vm`. **The window is asked
   for on #665 with its plan after stage B and granted in the host file's
   queue** (M7's windows and other lanes' first; the grant names the post
   contract: `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` in the post's
   first line, and what stops the guest at bound plus grace), one guest, 30
   minutes from START, T13's conditions (START and RETURN posted; stop by
   pidfile; the leftover check; outputs kept; the disk retired with its
   path, size and sha in `00`). **The window's first step identifies the
   installed EmulationStation against the pin**: the image's `BUILD_ID`
   from `/etc/os-release`, the distribution commit it names, that commit's
   `package.mk` `PKG_VERSION`, and a string the pin's last commit added
   found in `/usr/bin/emulationstation` by `strings`; a difference is
   written beside every guest verdict (the image is the M7 candidate
   `069fc2704421`, built from `next` at its own commit). **Nothing on a
   person's device or cloud** (D-QA-015). `tools/council/run invoke` runs
   four times with the key.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`; a frame is a PASS only with the string it shows read
   back (`tools/vm-visual-qa`'s OCR or the walk's expected text), and the
   exit lattice is D-QA-063's.
5. **A fix on the ES branch is proven twice before it is called fixed**
   (T2's `proved:` values): `fix-unit-test` where the code is pure (a case
   added to `CloudTextTests.cpp` or `tests/app-unit/` that fails before and
   passes after, run on the host), `fix-walk-pending-image` where it draws
   (the walk written and the frame owed to the integration build that
   carries the moved pin: the `pin-binary` frame of the unfixed behaviour
   from the window is the before). `tools/es-syntax-check` passes on every
   edited `.cpp` (`es-native-ui.md` § Before the pin moves, blindspot 49),
   and `grep -nP '^\s*//.*[^\x00-\x7F]'` is clean on every touched file.

**What never runs in this slice:** a build, a compiler beyond the host
compiler for `es-app/tests/unit` and `tools/es-syntax-check`'s syntax-only
replay, a plan generation, a fetch, a network read beyond the four seat
calls, a hosted or offsite cloud account, a command against a handheld or a
person's cloud, a read of an M7 build root or an `m7-*` ES worktree, a
checkout or write in any ES worktree but the lane's own, a guest outside
the one granted window, a `tools/council/run` call with the key beyond the
four, a credential-shaped literal written to any file at rest, a change to
the distribution's `packages/`, `projects/` or `tools/` at any stage (the
pin bump is the coordinator's), and a change to any ES file outside the 30
at stages A to D.

**The runs, with what the coordinator read** (the lane runs each at stage A
and records the exit, the wall time and the summary line; `TMPDIR` under
`/workspace/tmp/m6-t18/`; `W` the ES worktree, `PIN` the pin):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-cloud-pages-665
cd "$D"; export TMPDIR=/workspace/tmp/m6-t18/tmp; mkdir -p "$TMPDIR" .qa-scratch/t18
W=/home/max/Development/emulationstation-next.worktrees/m6-es-cloud-pages-665; PIN=16dbac5211eea7e70db7394372033be2be7df829
# the membership block (§ 2) -> .qa-scratch/t18/paths.txt (30); the wc -l sum (11,193); none in the merge base (0)
# the pin and the base (expect bccd71570 the merge base = upstream/master's tip; 725 ahead, 0 behind)
git -C "$W" merge-base upstream/master "$PIN"; git -C "$W" rev-list --count upstream/master.."$PIN"; git -C "$W" rev-list --count "$PIN"..upstream/master
# the sources and the tests (expect sources 8 / 5,429; tests 22 / 5,764; 221 TEST_CASE in 19 files; CloudTextTests 70 cases / 711 checks)
grep -c '^es-app/src/' .qa-scratch/t18/paths.txt; grep '^es-app/src/' .qa-scratch/t18/paths.txt | while IFS= read -r p; do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print s}'
grep '^es-app/tests/' .qa-scratch/t18/paths.txt | grep '\.cpp$' | while IFS= read -r p; do printf '%s %s %s\n' "$(git -C "$W" show "$PIN:$p" | grep -c 'TEST_CASE(')" "$(git -C "$W" show "$PIN:$p" | grep -c -E 'CHECK[A-Z_]*\(')" "$p"; done | awk '{c+=$1; k+=$2; n++} END {print "TEST_CASE", c, "checks", k, "files", n}'
git -C "$W" show "$PIN:es-app/tests/unit/CloudTextTests.cpp" | grep -c 'TEST_CASE('
# the declared CloudText functions and who calls each (expect 40 declared; the uncalled, by name, are Q6's)
git -C "$W" show "$PIN:es-app/src/CloudText.h" | grep -n -E '^\s+[A-Za-z_:<>,\s]+ [A-Za-z_]+\(.*\);' | wc -l
# the protocol markers and the exits (expect pid/doing/why/offer/tier/unit/removed at CloudText.cpp:561-616; 75 at :1386; 0 and 9 at CloudTransferJob.cpp:302 and GuiCloudTransfer.cpp:289/:440; whyForCode :80-98)
git -C "$W" show "$PIN:es-app/src/CloudText.cpp" | grep -n -E 'rfind\(">>> [a-z]+ ", 0\)' | cut -c1-80; git -C "$W" show "$PIN:es-app/src/CloudText.cpp" | grep -n 'exitCode == 75'
git -C "$W" show "$PIN:es-app/src/ThreadedCloudSync.cpp" | sed -n '80,98p'
# the two popen wrappers (expect the job's with trap '' PIPE at :637, the card's without at :207)
git -C "$W" grep -n -E 'setsid sh -c|trap .. PIPE' "$PIN" -- es-app/src/CloudTransferJob.cpp es-app/src/ThreadedCloudSync.cpp | sed "s/^$PIN://"
# the stamps (expect STAMP_DIR :892; readStamps :894; the writer :919-949 tmp + rename; the map CloudText.cpp:186-189; exists( 0 in the eight)
git -C "$W" show "$PIN:es-app/src/ThreadedCloudSync.cpp" | grep -n -E 'STAMP_DIR|readStamps|std::rename|writeAllText' | cut -c1-100; git -C "$W" grep -c -E 'FileSystem::exists\(' "$PIN" -- $(grep '^es-app/src/' .qa-scratch/t18/paths.txt | sed "s|^|$PIN:|" | sed "s|^$PIN:||") 2>/dev/null | sed "s/^$PIN://" ; echo "(no line = 0)"
# lifetimes and bounds (expect delete this :207 :328; postToUiThread :335 :1070; detach :56 and CloudTransferJob.cpp:65; linger :731; SIGKILL :859; 20 ms :862)
git -C "$W" grep -n -E 'delete this|postToUiThread|\.detach\(\)|sleep_for|SIGKILL' "$PIN" -- es-app/src/guis/GuiCloudTransfer.cpp es-app/src/ThreadedCloudSync.cpp es-app/src/CloudTransferJob.cpp | sed "s/^$PIN://" | cut -c1-120
# the why table against the scripts (expect 38 unique ES sentences from 39 rows; 37 script sentences; 32 shared; the lacked ones named; the eight variable emitters listed)
git -C "$W" show "$PIN:es-app/src/CloudText.cpp" | awk '/whySentences/{p=1} p' | grep -o -E '"[A-Z][A-Z0-9 ,.'"'"'?!-]+"' | sort -u | wc -l
git grep -h -o -E '>>> why [A-Z][A-Z0-9 ,.'"'"'?!-]+|say_why "[A-Z][^"]+"|\bwhy "[A-Z][^"]+"' 8ebaf8daad -- projects/ROCKNIX/packages/network/rclone/sources projects/ROCKNIX/packages/rocknix/sources/scripts projects/ROCKNIX/packages/network/raofflineproxy/sources | sed -E 's/^(>>> why |say_why "|why ")//; s/"$//' | sort -u | wc -l
git grep -n -E 'say_why "\$|why "\$' 8ebaf8daad -- projects/ROCKNIX/packages/network/rclone/sources projects/ROCKNIX/packages/rocknix/sources/scripts | sed 's/^8ebaf8daad://' | cut -c1-100
# the strings (expect 220 _( ) in the eight; 50 the card's, 67 the page's; BACKUP only as a noun; 0 WIFI; 0 lists without the serial comma)
git -C "$W" grep -o -h -E '_\("[^"]*"\)' "$PIN" -- es-app/src/CloudText.cpp es-app/src/CloudText.h es-app/src/CloudTransferJob.cpp es-app/src/CloudTransferJob.h es-app/src/guis/GuiCloudTransfer.cpp es-app/src/guis/GuiCloudTransfer.h es-app/src/ThreadedCloudSync.cpp es-app/src/ThreadedCloudSync.h | wc -l
# the xgettext trap (expect 0 non-ASCII // comment lines in the 30; the non-ASCII lines of GuiCloudTransfer.cpp (9) and CloudTransferJob.{cpp,h} (1 each) read and classed)
while IFS= read -r p; do n=$(git -C "$W" show "$PIN:$p" | grep -c -P '^\s*//.*[^\x00-\x7F]'); [ "$n" -gt 0 ] && echo "$n $p"; done < .qa-scratch/t18/paths.txt; echo "(no line = 0 comment lines)"
for f in es-app/src/guis/GuiCloudTransfer.cpp es-app/src/CloudTransferJob.cpp es-app/src/CloudTransferJob.h; do printf '%s %s\n' "$(git -C "$W" show "$PIN:$f" | grep -c -P '[^\x00-\x7F]')" "$f"; done
# the history with the three identities (expect 181 non-merge; 170 / 9 / 2; 2026-07-25 .. 2026-10-11)
tr '\n' '\0' < .qa-scratch/t18/paths.txt | xargs -0 git -C "$W" log --no-merges --format='%h %an' bccd71570.."$PIN" -- | tee "$TMPDIR/hist.txt" | wc -l; cut -d' ' -f2- "$TMPDIR/hist.txt" | sort | uniq -c | sort -rn
tr '\n' '\0' < .qa-scratch/t18/paths.txt | xargs -0 git -C "$W" log --no-merges --format=%ad --date=short bccd71570.."$PIN" -- | sort | sed -n '1p;$p'
# the callers outside the eight (expect GuiMenu.cpp 7 GuiCloudTransfer + 3 start; main.cpp 1 + 1; FileData.cpp :1310; ProxyCards.cpp :34/:118; JourneyTiers.h)
git -C "$W" grep -n -E 'new GuiCloudTransfer|ThreadedCloudSync::start|CloudTransferJob::' "$PIN" -- es-app/src | sed "s/^$PIN://" | grep -v -E '^es-app/src/(guis/GuiCloudTransfer|ThreadedCloudSync|CloudTransferJob|CloudText)\.' | cut -c1-110
# the unit tests built and run on the host (expect configure PASS with rapidjson named from an M6 build root; es-unit-tests PASS with its case count; CANNOT with the configure's words if no rapidjson copy exists)
B=$(ls -d /workspace/repos/pixelelated/distribution.worktrees/*/build.pixelelated-GENERIC_X64.x86_64 2>/dev/null | head -1); R=$(ls -d "$B"/build/rapidjson-*/include 2>/dev/null | head -1); echo "root $B rapidjson ${R:-none}"
[ -n "$R" ] && cmake -S "$W/es-app/tests/unit" -B "$TMPDIR/build-tests" -DCMAKE_CXX_COMPILER=/usr/bin/g++ -DRAPIDJSON_INCLUDE_DIR="$R" >/dev/null && cmake --build "$TMPDIR/build-tests" --target es-unit-tests >/dev/null && "$TMPDIR/build-tests/es-unit-tests" 2>&1 | tail -n 3 || echo "CANNOT: $( [ -n "$R" ] && echo 'the build or the run failed, see above' || echo 'no rapidjson copy under an M6 GENERIC_X64 build root')"
# the syntax check's readiness (expect PASS on an unchanged file, or the tool's exit-2 line naming what is missing)
for b in /workspace/repos/pixelelated/distribution.worktrees/*/build.pixelelated-GENERIC_X64.x86_64; do ls -d "$b"/build/emulationstation-* 2>/dev/null; done | head -n 3; ES_BUILD_ROOT="$B" tools/es-syntax-check --tree "$W" es-app/src/CloudText.cpp 2>&1 | tail -n 2
# the French coverage of the eight (expect tools/es-untranslated's count for these files, recorded; the why table's 38 rows against the catalog)
tools/es-untranslated --help 2>&1 | head -n 3; tools/es-untranslated "$W" 2>&1 | grep -E 'CloudText|CloudTransferJob|GuiCloudTransfer|ThreadedCloudSync|^[0-9]+ ' | head -n 12
# the menu map's cloud screens and the walks (expect § Cloud (our subtree) at :231; 8 cloud walks; es-menu-map-check's verdict for the pin)
grep -n -E '^## (Cloud|Visual evidence)' docs/es-menu-map.md; ls tools/vm-walks | grep -c -i -E 'cloud|sync|transfer|backup|restore'; tools/es-menu-map-check 2>&1 | tail -n 2
# the removal rule's own check against the dispatch tip (expect empty for the distribution; the ES worktree at the pin until stage E)
git diff --stat <dispatch tip> HEAD -- packages projects tools | tail -1; git -C "$W" diff --stat "$PIN" HEAD | tail -1
```

## 6. Outputs

As T2's and T17's briefs, with the folder `docs/audits/<yyyy_mm_dd>-epic-m6-es-cloud-pages/`:
`00` to `05`, `second-opinions/` (both seats' plans, the manifest with its
three-way scan and every hit's disposition, each probe and refutation with
provenance), `guest-cycle/` (the window's record: the image's identity
against the pin, the walks' frames at 640x480 with the strings read back,
the card during a sync against the QA WebDAV, the transfer page's live
line, `time-to-play`'s row or its `CANNOT`, the leftover check), the lint
before D, the audit issue (`Audit: M6 T18 EmulationStation's cloud pages,
cards and text -- N findings (...)`, a sub-issue of #665), the bugs, and
the retro at `docs/retros/<date>-m6-es-cloud-pages.md` (**what the slice
did to the two time-to-play numbers** -- the exit sync's card is this
slice's, so the answer is measured on the guest or cited from
`docs/vm-qa-log.md`, never "nothing" by default; **what T26 inherits**: the
callers' seams, the `exists()` reads, the composed commands). **`02`
carries § Coverage (30), § Context read (the `tests/app-unit/` files and
the Python harnesses, with what each tests of this slice and whether it
ran), § The protocol (one generated row per marker and per exit code: who
prints it, which reader parses it, what the player sees), § The why table
(generated from the two lists -- the ES rows and the scripts' literal and
variable emitters -- with the rows each side lacks named and the counts
asserted), § The surfaces (one row per surface: tier, what it shows, how
it ends, what it writes, its CANCEL and its question), § The lifetimes
(every `delete this`, detach, linger, lock and signal with what holds a
pointer across it), § The strings (the 220 against the rule, each failure
by file:line), § The tests (221 cases by subject; which trap each covers),
§ The runs (every § 5 command), § The guest cycle, § Positives, and every
proof with `proved:`.** The stage-D pause as T17's: the punch list posted
on #665, the lane waits for the coordinator's dispositions and any stream
brief.

## 7. Acceptance

The checklist on #665 becomes this section at dispatch, written there by
the coordinator in place of P1's five generated ones. Every checkbox names
the artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-es-cloud-pages/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-es-cloud-pages/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: extended` and two reviewers (`gpt`, `openai/gpt-6-astra`, `max`; `gemini-argon`, `google/gemini-4-argon`, `high`); each seat's probe and refutation have a `.provenance.json` beside them read directly (verification PASS, the seat's served model and provider, the output hash matching the sibling output, `facilitator_version` present), recorded in `stage-c/provenance-read.txt`; `manifest.json` lists every packet file with its sha256 and its three-way scan, every hit dispositioned, no value.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #909, #585, T26's issue, an M7 issue by number), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the issue closed by the coordinator with the lint's PASS quoted.
- [ ] `reviewed-at:`, `fixed-at:` and `fixed-at-es:` in the checklist's header carry the lane's commits (the distribution branch's HEAD at stage A with the pin beside it; the ES branch's HEAD after the streams); the read is of the pin's bytes (``tr '\n' '\0' < .qa-scratch/t18/paths.txt | xargs -0 git -C "$W" diff --stat 16dbac5211 <reviewed-at-es> --`` empty at stage A) and nothing under the distribution's `packages/`, `projects/` or `tools/` changes at any stage (`git diff --stat <dispatch tip> <hand-back tip> -- packages projects tools` empty).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (30 paths, 11,193 lines; read 29 / 11,116; fork-own 30; shipped 30; sources 8 / 5,429 and tests 22 / 5,764; 0 in the merge base; 725 ahead of `upstream/master`, 0 behind -- or the deltas beside them), the context read (the `tests/app-unit/` files and the harnesses named), the history (181 non-merge, 170 / 9 / 2, 2026-07-25 to 2026-10-11) and the callers outside the eight with their lines.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `30`; and a `## Context read` table with one row per file read as context.
- [ ] `02-forward-audit.md` § The protocol is generated by a script under the audit folder's `tools/` (asserting its row counts, exiting 1 on drift) with one row per `>>>` marker (`pid`, `doing`, `why`, `offer`, `tier`, `unit`, `removed`) and per mapped exit (0, 9, 3/4, 5, 124, 7/8, 69, 75, 130, NoFolder, default): the scripts or caller that print it (file:line at `8ebaf8daad` or in `es-app/src` at the pin), the reader that parses it (`CloudTransferJob::handleLine` or `ThreadedCloudSync::run`, by line), and what the player sees.
- [ ] `02-forward-audit.md` § The why table is generated from the ES rows and the scripts' emitters (38 unique rows from 39; 37 literal script sentences plus the eight variable emitters re-derived; 32 shared -- or the counts the generator asserts), naming every sentence one side lacks, the three wordings for exit 75, and the fallback map's six words against the code, the scripts and the rule, with the rule's half marked #909's and the header comment's drift marked this slice's.
- [ ] `02-forward-audit.md` § The lifetimes has one row per `delete this`, `detach()`, linger, lock and signal in the eight files (`GuiCloudTransfer.cpp:207`, `:328`, `:335`, `:1070`; `ThreadedCloudSync.cpp:56`, `:731`, `:784-862`; `CloudTransferJob.cpp:65`, `:100-161`), each with what holds a pointer or a reference across it and the test that covers it or `untested`.
- [ ] `02-forward-audit.md` § The strings states the 220 `_( )` strings of the eight files read against `es-player-text.md` and `es-ui-style-guide.md`, each failure by file:line, the fit of every `outcomeCandidates` and `chooseThatFits` list at 640x480 from a frame or the fonts, and the non-ASCII lines of `GuiCloudTransfer.cpp` and `CloudTransferJob.{cpp,h}` classed (literal or comment near `_( )`).
- [ ] `02-forward-audit.md` § The tests states `es-unit-tests` built on the host (the rapidjson copy named by path) and run with its summary line (221 cases, or the count the binary prints) and PASS, or `CANNOT` with the configure's or build's last lines; and one row per test file with its subject and the trap of `es-code-traps.md` it covers or `none`.
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass; `tools/es-syntax-check`'s readiness (PASS on an unchanged file with the root named, or its exit-2 line) is one of them.
- [ ] `02-forward-audit.md` § The guest cycle records the window the coordinator granted on #665 (the comment's time, its place in the host file's queue), the image by file name and `BUILD_ID`, **the installed EmulationStation identified against the pin before any verdict** (the build commit's `PKG_VERSION`; a pin-only string found by `strings`) with every verdict a difference touches named, the eight cloud walks' frames at 640x480 with their strings read back, the card during a sync against the QA WebDAV and the page's live line, `tools/time-to-play --vm`'s row or `CANNOT`, and the leftover check; or, if no window is granted before the hand-back, `CANNOT` with the host file's state and each guest proof named as moved or open.
- [ ] `00-running-log.md` shows no build, no compiler beyond the host compiler for `es-app/tests/unit` and `tools/es-syntax-check`, no plan generation, no fetch (the council runtime from `npm install --offline`), no handheld, no hosted or offsite account, no M7 build root or `m7-*` ES worktree read, no checkout or write in another ES worktree, guests only inside the granted window, exactly four `tools/council/run invoke` calls with the key and every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`, and no credential-shaped literal written to any file.
- [ ] `04-analysis.md` § Q3 states each bug decision with its trace, its `Already written:` line and its VM line in the three families (the protocol under a pipe; lifetimes and threads; the words), and names the `proved:` each fix would need (`fix-unit-test` or `fix-walk-pending-image`); § Q2 the rules' checklist; § Q4 M7's commits beyond the pin by number and T17's S5 and S6; § Q5 the two time-to-play numbers measured or cited and the 2 s budget against D-CLOUD-119; § Q6 every uncalled `CloudText` function and unproduced marker, removals none; § Q7 points at the two generated tables.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `fixture`, `unit-test`, `pin-binary`, `fix-unit-test`, `fix-walk-pending-image` or `design`; every punch item carries `question:`; every `bug` passes `tools/box-check --issue N` and carries its `Already written:` line; every fix on the ES branch has `tools/es-syntax-check` PASS and a clean non-ASCII comment grep recorded beside its commit.
- [ ] The retro exists at `docs/retros/<date>-m6-es-cloud-pages.md`, is posted on #665, says what the slice did to the two time-to-play numbers (measured on the guest or cited, with the exit sync's budget against D-CLOUD-119's 3 s), and what T26 inherits.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the distribution branch, and the ES fork's `.githooks/pre-push-test` on the ES branch, before their merges (after the coordinator's hand-back merge).

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and both
branches pushed (the hand-back); the stage-D pause; an explicit maintainer
pause on #665; a blocker named on #665 (a seat that fails its provenance
gate twice, a packet scan hit that is a value, two commands that disagree, a
block whose output differs from § 2's beyond the deltas it records, the
unit tests failing to build on the host with no rapidjson copy anywhere
M6 holds); the ES worktree not at the pin at stage A, or the distribution
branch not stacked on `2174265e9c`; or an execution limit, stated as such
with the running log current. A checkpoint is not a stop. An idle session
says it is idle on #665, **and does not end a turn on a post that asks
nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#665`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #665` or the
  guard.
- The VM question written before any proof (§ 5: yes, the host first, then
  one guest window in the host file's queue; nothing on a person's device
  or cloud).
- The mini-retro at stage G, posted on #665, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 where a fix landed.
- A register row the same session for any decision the slice forces (none
  expected); D-CLOUD-185 is the highest Decided cloud row and
  D-WORKFLOW-209 the highest workflow row on the coordinator's branch
  (D-WORKFLOW-188 on the P1 branch only; the merge unites them); a row this
  slice forces takes an ID the coordinator assigns on #665.
- `tools/ceremony-check --gate` before every push; never `--no-verify`; a
  merge with conflicts is checked for markers; the ledgers united by whole
  entries; **a commit names its paths**; anything temporary under
  `/workspace/tmp/m6-t18/` after `df -i`, never `/tmp`; the window's record
  kept on the branch, the guest disk retired after it with the retirement
  recorded in `00` (D-INFRA-022); **`rm -rf` only as `"${VAR:?}"/...` or a
  literal path, in its own short command, never inside a `bash -c` script**.
- Commit messages `docs: ...` on the distribution branch with `Refs #665`;
  on the ES branch the fork's `es: ...` shape (`fork-workflow.md`,
  D-WORKFLOW-012), `Refs #665` and the bug's number.
- **Every ES change keeps its flow and screenshot evidence** (D-WORKFLOW-155/156,
  D-UI-039): a stream that changes a screen's words or behaviour updates
  `docs/es-menu-map.md` § Cloud in the same change and names the frame it
  owes to the integration build; a stream with no visible effect names the
  exercised flow and the unchanged frame.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#665's checkboxes against their artifacts; the lint's `PASS` line;
`review-plan.json` and the four provenance files and the manifest's scans;
the audit issue's checkboxes all at an outcome; the coverage table's row
count (30), § Context read's rows, § The protocol's and § The why table's
generated counts, § The lifetimes' rows; every Q3 bug with its three lines
and its `proved:`; **re-running on a clone of both branches at their tips
under `/workspace/tmp/m6-coordinator/`: the membership block, every § 5 run
that needs no guest, `es-unit-tests` on the host where the tests changed,
and `tools/es-syntax-check` on every edited `.cpp`** (no guest: the
window's record is read, not repeated); `register-check` on a simulated
merge with the coordinator's tip (the ledgers united); the retro's answers;
the exit codes. The lane posts one hand-back comment naming both tips and
each artifact by path, writes `reviewed-at:`, `fixed-at:` and
`fixed-at-es:` into #665's body, then says it is idle. After acceptance the
coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the full lint, merges the distribution branch in
its turn after the M7 candidate (after T17's) and **moves the pin to the ES
branch's tip in the distribution's integration commit, the image build
proving the walks' pending frames**, regenerates the ledgers, posts any
#585 and #909 lines in the shape the lane wrote, and closes #665 when every
row is proven.

**The readings before dispatch** (plan § 3, principle 3; § 6b): the epic's
futro (#700) takes a T18 kickoff addendum written with this version
(streams predicted: two -- the header comment at `ThreadedCloudSync.h:94-96`
and the why table's missing rows), and a stranger's proof of this brief is
run by a reader with no context before dispatch; version 2 records what each
found.
