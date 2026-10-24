# Brief: M6.P2 T24, emulator recipes and files no shipped image builds (#671)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #671 differ, #671 wins and the
coordinator corrects the brief in the same session. **Version 2
(2026-10-24, after the stranger's proof of version 1 -- 77 claims: 55 right, 13
wrong, 5 partial, 4 uncheckable -- each wrong one corrected in place and listed
in the futro addendum's errata):** written after T3 (#650) and T30 (#677), the area's other two
slices, were accepted, so their Q6 tables are this slice's starting rows;
every figure below was produced by a command at `8ebaf8daad` (the tree) or
in the inventory at P1's `2174265e9c` unless it says *branch*. It goes
through a stranger's proof before dispatch; version 2 records what it found.
**Each command block sets its own variables** (`D`). **This is a table
slice**: one row per path for reachability; it reads no file line by line
unless a row needs it; **it removes nothing upstream carries and relocates
nothing**. Prose goes into a log through a quoted heredoc or the Write tool
(plan § 6b E).

## 1. Identity

- **Issue:** #671 `M6.P2 E798/T24: emulators-and-cores: emulator recipes
  and files no shipped image builds, and the rest of the area`, slice
  `emulators-dead-ends` (`k: 24`, `select: rest`) in `docs/reviews/slices.json`,
  twenty-fourth in `docs/reviews/order.md` (its § T24 paths line: *"86 paths,
  2,399 lines, -- read, of which -- fork-own; 0 patch and config lines;
  reach unreached 84, unshipped 2"*; its `why`: *"the generic
  `packages/emulation` recipes and the cores only unshipped devices
  build"*). **Epic:** #798 (the emulators and cores: T3 #650 accepted, T30
  #677 accepted, this slice), whose futro
  (`docs/futros/2026-10-24-m6-emulators-and-cores.md`) carries a T24
  kickoff addendum (A1 to A6 are written into this version).
  **Milestone:** M6. **Predecessors:** #346, #641, #644 (finding 24's class:
  what the base merge carries that no ROCKNIX workflow uses), **T3 #650**
  (`docs/audits/2026_10_24-epic-m6-emulators-libretro/04-analysis.md` § Q6
  at `b3cb4ec8c5` names the five ROCKNIX recipes of this set as *carried by
  no built device* with their `Already written:`; its coverage table is the
  shape), **T30 #677** (its launch-table rows #857 and #873 are the route
  side of the same emulators), **T6 #653** (the reachability-table method:
  one row per path, a positive control beside every zero). **Beside it:** T8
  (#655) runs in the other lane (D-WORKFLOW-190); the two share no path.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, post on #585, or decide a question of scope: those are the
  coordinator's, reached through #671, one question at a time. What it does
  file: its own audit punch-list issue (stage D) and a `bug` issue for a
  defect, should a table find one (D-WORKFLOW-187). Nothing else.
- **One worktree, one session.** Branch `feature/m6-emulators-dead-ends-671`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-dead-ends-671`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's
  pointer seeded (the two hashes are in the dispatch comment on #671).
  **The worktree exists (cut 2026-10-24 at `77141a45c7`: P1's `2174265e9c`
  with the coordinator's `152c4ee3c3` merged, since re-merged at version 2);
  until the dispatch comment exists the pointer is not seeded, the first
  command's `cat` fails, and nothing starts.** The session is the T3 lane's
  (`m6-t3-emulators`, pane `wN:p6`), which ran T3 and T30; those worktrees
  stay beside this one, idle, until their merges, and nothing is written
  there. The primary checkout stays on `next` (D-INFRA-025); the legacy
  checkout and `rocknix.worktrees/*` are the M7 lane's, read only (`ls` of
  their `build/` directories and install trees, nothing more); every other
  lane's worktree is `git -C` only. **The rules in this worktree are
  `next`'s except the paths the dispatch comment lists** (eight on
  2026-10-24, as T8's). Known stale facts in the rules (the legacy layout,
  #640) do not cost an hour here: every rule the work touches is named in
  § 3.
- **Model and effort:** Opus 5.5 at high effort. Record what ran in
  `00-running-log.md`'s header.
- **Review depth: Local** (D-WORKFLOW-184: *Local for a dead-end table*;
  `slices.json` k 24 `depth_reason`: *a reachability table*). No external
  reviewer, no `npm install`, no Facilitator call.
  `second-opinions/review-plan.json`: depth `local`, primary
  `anthropic/claude-opus-5-5` / `anthropic`, reviewers `[]`,
  `"tier_exception": "D-WORKFLOW-184"`, `"reason": "plan § 6c and
  slices.json k 24: a dead-end table is Local"` (#810; T6's and T7's files
  are the model). Phase 4.6 is recorded as not applicable with the row
  cited; Phase 4.5 is done in full, and § 5's rule 4 -- what result would
  have produced a FAIL -- is asked of every PASS.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-dead-ends-671
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-emulators-dead-ends-671
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: this is not the lane's worktree (stacked on P1): stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists, nothing else
mkdir -p .qa-scratch/t24/at-hash && git archive 8ebaf8daad packages/emulation projects/ROCKNIX/packages/emulators/libretro | tar -x -C .qa-scratch/t24/at-hash   # the read tree, 474 files: 86 are the slice's; the rest are T3's recipes and T40's 16 patch files under packages/emulation
ls tools/renovation-inventory tools/renovation-status tools/renovation-drift docs/reviews/slices.json   # P1's
"$D/tools/rules-check"; echo "rc=$?"; "$D/tools/register-check"; echo "rc=$?"; "$D/tools/ceremony-check"; echo "rc=$?"   # rc 1 on 2026-10-24: W42 OVERDUE (M7's week), not this lane's to pay
git push -u origin feature/m6-emulators-dead-ends-671
test -f docs/reviews/briefs/emulators-dead-ends.md || { echo "the brief is not in this tree: stop"; exit 1; }
cat .github/sessions/saved-session-state-feature-m6-emulators-dead-ends-671.md
tail -3 /tmp/m7-m6-host-coordination-20261023.txt                   # the host's state: this slice needs no runtime
df -i /tmp | tail -1                                                 # never export a tree under /tmp
gh api rate_limit --jq '.resources.core | "\(.remaining)/\(.limit)"'    # the API budget § 5 spends (about 90 reads); below 1,500 the loop waits
```

## 2. Scope

**86 paths, 2,399 lines; every one upstream-carried; reach `unreached` 84,
`unshipped` 2; 85 recipes and one cmake file.** The membership is the
inventory's at P1's `2174265e9c`, with the slice's rule (`k: 24`,
`select: rest`): the rows of the `emulators-and-cores` area that no earlier
slice of the area took -- in practice, every row whose reach is `unreached`
or `unshipped` (T3's and T30's took the `shipped` and `test` rows; the
area's two `n/a` rows are T3's). The re-derivation:

```bash
python3 -I - <<'PY'
import json, collections, os
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
t24 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "emulators-and-cores" and r["reach"] in ("unreached", "unshipped")]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t24), "lines", L(t24), dict(collections.Counter(r["tier"] for r in t24)), dict(collections.Counter(r["reach"] for r in t24)))
print(dict(collections.Counter(r["language"] for r in t24)))
pk = [r for r in t24 if r["path"].endswith("/package.mk")]
print("recipes", len(pk), "under packages/emulation", sum(1 for r in t24 if r["path"].startswith("packages/emulation/")), "under projects", sum(1 for r in t24 if r["path"].startswith("projects/")), "with patches", sum(1 for r in pk if r["patches"]), "shadowed", sum(1 for r in pk if r["shadowed_by"]), "spaces", sum(1 for r in t24 if " " in r["path"]))
print("unshipped:", [(r["path"].split("/")[-2], r["buildable_by"]) for r in t24 if r["reach"] == "unshipped"])
os.makedirs(".qa-scratch/t24", exist_ok=True)
open(".qa-scratch/t24/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t24, key=lambda r: r["path"])))
open(".qa-scratch/t24/recipes.txt", "w").write("".join(r["path"] + "\n" for r in sorted(pk, key=lambda r: r["path"])))
for r in sorted(t24, key=lambda r: r["path"]): print(r["reach"], r["tier"], r["lines"], r["path"])
PY
wc -l .qa-scratch/t24/paths.txt .qa-scratch/t24/recipes.txt     # 86, 85
```

Recorded (2026-10-24): **86 paths, 2,399 lines; 86 upstream-carried; 84
`unreached`, 2 `unshipped`; languages recipe 85, cmake 1.** **81 are under
`packages/emulation/`**: LibreELEC's 77 `libretro-*` cores (the ones
Kodi's RetroPlayer builds, from `libretro-2048` to `libretro-yabause`),
`cyclone68000`, `libretro-common` (the 78th `libretro-*` recipe) and
`rcheevos` (its `package.mk` and one cmake file) -- 80 recipes and the
cmake file; with the five ROCKNIX recipes, 86. (Version 1 said 83 and 79;
§ 2's own block prints 81, and the stranger's proof counted the cores.) ROCKNIX builds none of them: it carries its own cores as
`projects/ROCKNIX/packages/emulators/libretro/<name>-lr` (151 `package.mk` files in that directory: T3's 137 by its own
`04`, this slice's five, and the RetroArch frontend's own packages), and the inventory's `shadowed_by` is 0 for all 86 because the
duplication is by content, not by directory name (`libretro-snes9x` against
`snes9x-lr`). **5 are ROCKNIX's own recipes** under
`projects/ROCKNIX/packages/emulators/libretro/`: `boom3-lr` and
`vitaquake3-lr` (`unshipped`, `buildable_by` AMD64-x86_64 only: `idtech-lr`
adds them on x86_64, where GENERIC_X64 skips `idtech-lr`), `mame2003-lr`,
`panda3ds-lr` and `play-lr` (`unreached`). T3's `04` § Q6 named exactly
these five as *carried by no built device: exactly the five outside the
membership, all T24's* with their `Already written:` (*no fork image
carries their `.so`; only `core-info`'s `.info` files for `boom3`,
`vitaquake3` and others ship*). **Twelve recipes carry patches**
(`libretro-bsnes-hd`, `libretro-bsnes-mercury-performance`, `libretro-bsnes`,
`libretro-cannonball`, `libretro-dosbox-pure`, `libretro-mame2010`,
`libretro-mupen64plus-nx`, `libretro-picodrive`, `libretro-scummvm`,
`libretro-stella`, `panda3ds-lr`, `play-lr`): the patches are T40's rows
(`patches-dead`, `k: 40`, reach `unreached`; T43 is `patches-unshipped` and
holds none of these); this slice reads none. No path carries a space.

**Provenance, by git.** Against the base `c445081a59`: **the fork changed
none of the 86.** Against `upstream/next` (`e0f9deb899`): 81 identical (the 81 LibreELEC files), **5
differ**, all by upstream's one commit on these paths since the base,
`af70bd435b` (*libretro-cores: add retroarch as PKG_DEPENDS_TARGET*), which
touched the five ROCKNIX recipes -- so the base merge brings that hunk and
meets no fork edit.

```bash
P=.qa-scratch/t24/paths.txt
tr '\n' '\0' < $P | xargs -0 git diff --name-status c445081a59 8ebaf8daad -- | wc -l                      # 0
tr '\n' '\0' < $P | xargs -0 git diff --name-status upstream/next 8ebaf8daad -- | awk '{print $1}' | sort | uniq -c   # 5 M
tr '\n' '\0' < $P | xargs -0 git log --oneline c445081a59..upstream/next -- | cat                          # af70bd435b, one commit
git log -1 --format='%h %cs' 8ebaf8daad -- packages/emulation/libretro-snes9x/package.mk                  # 2dd698ba24 2026-06-02 for snes9x; the latest touch among the 81 is e46157185c 2026-07-22 (libretro-cannonball): tr '\n' '\0' < $P | xargs -0 git log -1 --format='%h %cs %s' 8ebaf8daad --
```

**Where these would run, and do not.** A recipe is built when a plan
resolves it: `tools/viewplan` for each shipped device, the three virtual
packages' dependency lists (`make update`'s set, T8's finding: none of the
86 is in it), the emulators metapackage (`projects/ROCKNIX/packages/virtual/emulators/package.mk`,
T3's file: the `add_emu_core` rows name `*-lr` recipes, never a
`packages/emulation/libretro-*`), or a device's `packages/`. The 81 under
`packages/emulation/` arrive by ROCKNIX's merges of LibreELEC master (the
last on `upstream/next`: `d43d166b7a`, 2026-08-12) and are carried for Kodi,
which ROCKNIX does not ship; **LibreELEC master still carries them**
(`libretro-snes9x`'s pin there is `fae2fea08f…` against our `185488cd83…`;
`libretro-mgba`'s is the same `6dce57eef1…`), so every base merge brings
them again. The record: none of the 86 names has a build directory in any
of the five M7 roots (the lane confirms by name prefix, § 5), while their
ROCKNIX twins do (`snes9x-lr-890b5d4455…`, `mgba-lr-e31759b24e…` in the
GENERIC_X64 root).

**The hash.** The slice's bytes are `8ebaf8daad`'s; `reviewed-at:` is the
branch `HEAD` at stage A; the read is made on the at-hash tree
(`.qa-scratch/t24/at-hash/`). The branch differs from the hash on none of
the 86 (P1 and the coordinator changed nothing here): `tr '\n' '\0' <
.qa-scratch/t24/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD --` is
empty; a non-empty result is the first lead.

**The policy on change (plan § 5; D-UI-079's spirit; D-WORKFLOW-187):**
**an upstream-carried file is not removed, moved or edited by this slice.**
The 81 LibreELEC files are the base merge's: a proposal to ROCKNIX on #585
(the merge carries a tree ROCKNIX never builds -- the lane counts the files,
lines and bytes, and names which cores have a ROCKNIX twin and which have
none; the coordinator posts it) is the whole remedy, and each row's
disposition is `kept: upstream's; #585 candidate` with an `Already
written:` line (nothing: no fork image carries them). The five ROCKNIX
recipes are ROCKNIX's too: `kept: upstream's; no shipped device builds it`
(the two `unshipped` ones name AMD64 as their builder), with T3's
`Already written:` cited. A defect found in a recipe (a late-binding use,
a dead URL) is a `bug` in the code-trace shape with a #585 candidate, as
rule 6 asks, and is fixed under a stream brief only where the fix is
contained; nothing is expected.

**Drift.** `next` is `8ebaf8daad`; the M7 candidate's merge moves it after
this slice; the coordinator merges `next` into the branch never between
stage A and stage D. `tools/renovation-drift` is the coordinator's.

## 3. Read first

- `.github/sessions/saved-session-state-next.md` and this lane's own pointer.
- **The rules this work touches** (`working-principles.md` § Pre-flight):
  `engineering-practices.md` (§ Verify the artifact; § A name is not a
  behaviour with its bullet on counts, line numbers and hashes; § Before
  deleting a duplicate -- the test for every row, even where nothing is
  deleted: what the file guards, stamps or exposes; § Consider contributing
  every applicable fix upstream, D-WORKFLOW-164/165), `packaging-and-patches.md`,
  `device-builds.md` (§ After rebasing item 3: every field per plan),
  `fork-workflow.md`, `release-candidates.md` (step 0), `upgrade-and-install.md`
  (`Already written:`), `bugs-are-agent-first.md`, `issue-tracking.md`,
  `vm-first.md` (§ 5: no), `worktrees.md` (superseded by § 1).
- The code-auditor skill whole; the renovation face is plan § 6b; the Local
  plan file is § 1's.
- **T3's audit** (`b3cb4ec8c5`): `04-analysis.md` § Q6 (the five recipes'
  rows and the `core-info` note), its coverage table's shape, its Q4 method
  (`q4-pins-table.md`). **T30's**: #857 and #873 (the launch table's dead
  routes). **T6's**: the reachability table's shape, the positive control
  beside every zero. **T8's** stage B (#655): `make update`'s set.
- `docs/reviews/build-path-read.md` (#644) finding 24 (dead tooling the
  merge carries) as the class.
- `docs/blindspot-register.md` entries **13**, **22**, **46**, **51**, **75**.
- Decisions: D-WORKFLOW-184, 186, 187, 164/165, 162, D-UI-079, D-INFRA-025/026.
- Issues: #671, #798, #650, #677, #655, #585, #857, #873, #810, #809. Every
  `gh` call carries `--repo pixelelated/distribution`.

## 4. The questions

All seven apply (plan § 4); for a reachability table Q6 is the spine, Q4
and Q7 hang off it, and Q1, Q2, Q3 and Q5 apply as counts.

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | A recipe pinned to a retired host or series among the 86 (rows only) | the `PKG_URL` hosts |
| Q2 Standards | `tools/pkgcheck` over the 85 recipes (the tree's copy; T6's widened copy from this worktree as a second pass), the baseline counts first | the two runs' counts and FAIL lists; a FAIL on an upstream-carried recipe is `Renovation` with a #585 candidate |
| Q3 Bugs | A dead primary `PKG_URL` among the 85 (a HEAD probe without `-L`; the mirror as the second line, T7's method) -- informational for files nothing builds, filed as a `bug` only where ROCKNIX's own five are concerned | the probe's histogram |
| Q4 Currency | (a) `upstream/next` per path (81 identical, 5 upstream's `af70bd435b`); (b) LibreELEC master per `packages/emulation` recipe through the contents API (identical / moved / absent), serially, the budget read first and last; the five ROCKNIX recipes' pins against their projects as T3's Q4 did | the loops' outputs; a disposition per row naming the mover (the base merge for all 86) |
| Q5 Efficiency | What the 81 cost the tree (files, lines, bytes: `git ls-tree -r -l` over the path list; `packages/emulation` whole also holds T40's 16 patch files) and the base merge (every conflict-free merge of LibreELEC master re-imports them); `not measured` for a build: nothing builds them | the counts |
| Q6 Dead ends | **The table**: one row per path (86) -- `reached by <file:line>` / `unreached`, the plan reads that decided it (`tools/viewplan` per shipped device: absent; the emulators metapackage: no `add_emu_core` names it; `git grep -F <name>` over `projects packages`: the hits, each classed), the record (no build directory by name prefix in the five roots; the `.info` trace in the install trees for the five), the tier, the (a) and (b) states, the disposition (`kept: upstream's; #585 candidate` / `kept: upstream's; no shipped device builds it`), and **`Already written:` on every row** | the commands with outputs; a reached row found by the same commands is the positive control (e.g. `snes9x-lr`) |
| Q7 Clarity | **The twin map**: for each of the 77 LibreELEC cores, its ROCKNIX `*-lr` twin by name and by source (`PKG_SITE`/`PKG_URL`), or `no twin`; the pins side by side where a twin exists; `libretro-common`'s and `rcheevos`'s standing (ROCKNIX's cores vendor their own) | one table of 77 rows |

A finding is one question with its evidence; `Renovation` is the category
for everything here that is not a defect; a Q3 finding on a ROCKNIX recipe
is a `bug`.

**The ladder:** the guard for this class is the inventory's reach
(`tools/renovation-inventory`, P1's) and `tools/renovation-drift`; the
slice proposes nothing new unless the table shows a shape they miss.

## 5. The evidence floor

1. Tracker state is never sole evidence: every verdict cites the tree
   (`git grep`, `git log`, `git diff`), an API response saved to the scratch,
   a plan read, a listing of a build root, or a document's line.
2. Mechanical evidence outranks reading.
3. **For a table, the target is the tree and the record**: the at-hash
   files, `upstream/next`, LibreELEC master through the API, `tools/viewplan`
   in this worktree per shipped device, the five M7 roots' `build/`
   listings and the GENERIC_X64/H700/SM8550 install trees -- **read only,
   never a process started in an M7 worktree**. No guest, no build.
4. An assertion that cannot fail is not evidence: `snes9x-lr` (reached,
   built) is the positive control for every reachability command before a
   row says `unreached`; `libretro-snes9x`'s moved pin is the control for
   the API read before a row says `identical`.
5. Subagent output is a lead, never evidence (D-WORKFLOW-183).

**Can this be done on the VM? No** -- a reachability table over files no
image carries; its bench is the tree, the record and the API. Nothing here
touches a handheld, a cloud, a shared backend, a guest or a build.

- **The host-side checks**, each with its command, exit status and summary
  line in `02-forward-audit.md`:
  ```bash
  D=/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-dead-ends-671
  cd "$D"; mkdir -p .qa-scratch/t24/le .qa-scratch/t24/probe
  wc -l < .qa-scratch/t24/paths.txt                                                                        # 86
  tr '\n' '\0' < .qa-scratch/t24/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD -- | tail -1           # empty
  # (a) ROCKNIX
  while IFS= read -r p; do git diff --quiet upstream/next 8ebaf8daad -- "$p" && echo "identical $p" || echo "differs $p"; done < .qa-scratch/t24/paths.txt | cut -d' ' -f1 | sort | uniq -c   # 81 / 5
  # (b) LibreELEC master for the packages/emulation recipes (80 reads -- the recipes under `packages/emulation`, the cmake file aside -- serial; a row says `pin identical`, since only the pin is compared (`libretro-mgba`'s master file differs by a `pre_make_target` at the same pin); a 404 is absent, any other non-200 is not-read)
  gh api rate_limit --jq '.resources.core.remaining'                                                        # start above 1,500
  grep '^packages/emulation/' .qa-scratch/t24/recipes.txt | while IFS= read -r p; do out=$(gh api "repos/LibreELEC/LibreELEC.tv/contents/$p?ref=master" --jq .content 2>.qa-scratch/t24/le/err); rc=$?; if [ $rc -eq 0 ]; then printf '%s\n' "$out" | base64 -d > ".qa-scratch/t24/le/$(echo "$p" | tr / _)"; printf '%s %s\n' "$p" "$(grep -m1 '^PKG_VERSION=' ".qa-scratch/t24/le/$(echo "$p" | tr / _)" | cut -d'"' -f2)"; elif grep -q 'HTTP 404' .qa-scratch/t24/le/err; then echo "$p absent"; else echo "$p not-read"; fi; sleep 0.4; done > .qa-scratch/t24/q4b.txt
  gh api rate_limit --jq '.resources.core.remaining'
  # reachability: the plans, the metapackage, the grep, with snes9x-lr as the control
  for dev in GENERIC_X64:x86_64 H700:aarch64 SM8550:aarch64; do d=${dev%%:*}; PROJECT=ROCKNIX DEVICE=$d ARCH=${dev##*:} tools/viewplan > ".qa-scratch/t24/plan-$d.txt" 2> ".qa-scratch/t24/plan-$d.err" || echo "viewplan $d: rc $?"; done; grep -c . .qa-scratch/t24/plan-*.txt   # the device comes from the environment (DEVICE defaults to SM8550); an argument is a build target and fails the plan; each line is 'step name (wants: ...)'
  while IFS= read -r p; do n=$(basename "$(dirname "$p")"); printf '%s plan=%s meta=%s grep=%s\n' "$n" "$(awk -v n="$n" '$2==n' .qa-scratch/t24/plan-*.txt 2>/dev/null | wc -l)" "$(git grep -c -F "$n" 8ebaf8daad -- projects/ROCKNIX/packages/virtual/emulators/package.mk | cut -d: -f3)" "$(git grep -l -w -F "$n" 8ebaf8daad -- projects packages | grep -v -F "$p" | wc -l)"; done < .qa-scratch/t24/recipes.txt > .qa-scratch/t24/reach.txt; grep -c 'plan=0 meta= ' .qa-scratch/t24/reach.txt   # the plans and the metapackage decide; the grep column is a lead per hit, classed in the table by the hitting file's reach (the 78 Kodi game.libretro.* addon recipes under packages/mediacenter name every core and are themselves unreached, so grep=0 is rare by construction; -w keeps snes9x from matching snes9x2002)
  n=snes9x-lr; printf 'control %s plan=%s\n' "$n" "$(awk -v n="$n" '$2==n' .qa-scratch/t24/plan-*.txt | wc -l)"   # 3 expected: the control is in each device's plan; a 0 here is the command, not the core
  # the record, by name prefix (never a stripping sed), and the .info trace
  ROOTS=/workspace/repos/rocknix.worktrees; for d in $ROOTS/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64 $ROOTS/m7-signin-h700-build-20261023-06/build.pixelelated-H700.aarch64 $ROOTS/m7-signin-h700-build-20261023-06/build.pixelelated-H700.arm $ROOTS/m7-signin-sm8550-build-20261023-03/build.pixelelated-SM8550.aarch64 $ROOTS/m7-signin-sm8550-build-20261023-03/build.pixelelated-SM8550.arm; do LC_ALL=C ls "$d/build" > ".qa-scratch/t24/listing-$(basename $d).txt"; done
  while IFS= read -r p; do n=$(basename "$(dirname "$p")"); hit=0; for l in .qa-scratch/t24/listing-*.txt; do grep -q -E "^${n}-[A-Za-z0-9]" "$l" && hit=1; done; echo "$hit $n"; done < .qa-scratch/t24/recipes.txt | cut -d' ' -f1 | sort | uniq -c   # 85 with 0 expected
  grep -q -E '^snes9x-lr-' .qa-scratch/t24/listing-build.pixelelated-GENERIC_X64.x86_64.txt && echo "control: snes9x-lr built"
  for n in boom3 boom3_xp vitaquake3 mame2003 panda3ds play; do f=$ROOTS/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/lib/libretro/${n}_libretro.info; [ -f "$f" ] && echo "info $n" || echo "no-info $n"; done   # the .info trace T3 named (read only): the 320 .info files live in usr/lib/libretro, not usr/share; all six present; a prefix grep over-matches (mame2003 -> 3)
  # pkgcheck, the tree's copy then T6's widened copy run from this worktree
  for p in $(cat .qa-scratch/t24/recipes.txt); do tools/pkgcheck "$(basename "$(dirname "$p")")" >/dev/null 2>&1 && echo PASS || echo FAIL; done | sort | uniq -c
  git -C /workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-upstream-tools-653 show 44f64842b6:tools/pkgcheck > .qa-scratch/t24/pkgcheck-t6 && chmod +x .qa-scratch/t24/pkgcheck-t6; for p in $(cat .qa-scratch/t24/recipes.txt); do .qa-scratch/t24/pkgcheck-t6 "$(basename "$(dirname "$p")")" >/dev/null 2>&1 && echo PASS || echo FAIL; done | sort | uniq -c
  # Q5: what the 81 weigh: the directory whole prints 97 files, 106,103 bytes (T40's 16 patch files inside); the 86 paths print 86 files, 91,552 bytes
  git ls-tree -r -l 8ebaf8daad -- packages/emulation | awk '{s+=$4} END {print NR " files, " s " bytes"}'; tr '\n' '\0' < .qa-scratch/t24/paths.txt | xargs -0 git ls-tree -r -l 8ebaf8daad -- | awk '{s+=$4} END {print NR " files, " s " bytes"}'
  ```
  (`tools/viewplan` sources `config/options` and writes
  `build.pixelelated-<DEVICE>.<ARCH>/.cache_package_*` into the worktree,
  gitignored (`config/path:19`); `pkgcheck` writes nothing. The at-hash export is two directories under `.qa-scratch/`.)
- **A read is free and goes through the filter** on any log or config read
  from an M7 root.

**What never runs in this slice:** a build; a guest; a command on a
handheld, a cloud or a shared backend; a process in an M7 worktree; a model
call; `npm install`; `git remote add`; an archive download (a HEAD probe
without `-L` at most); a deletion, move or edit of any upstream-carried file
(every file here is one); a change to a patch (T40's); an edit at stage B;
`--no-verify`; bare `git stash`; `git worktree remove --force` or `rm -rf`
of any worktree; a write in another lane's worktree or under
`/workspace/repos/rocknix*`; a tree export under `/tmp`; an unquoted
heredoc for prose; a change to the order, the slices, the plan, this brief,
#671's criteria or the M6 body; a comment on #585; a GitHub issue other
than the audit punch-list issue and a `bug`.

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#671`
(`Refs #671`); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-emulators-dead-ends/00-running-log.md` | the flight recorder: model and effort, `reviewed-at` with `8ebaf8daad` beside it, every § 5 command with its exit status, the API budget before and after, every `PROOF:` line, each time from `date -u` | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 86 re-derived with § 2's filter and its output, the provenance (0 fork changes; 81 identical, 5 upstream's `af70bd435b`), the branch's deltas from the hash (none expected); § Phase 1: how the 81 arrive and why nothing builds them, in the slice's own words | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #671's checklist, plus **a coverage table with one row per path** (86; the first cell the path in backticks so ``grep -c -E '^\| `(packages|projects)/'`` counts them), § Mechanical checks (every § 5 block with command, exit status, summary), § The reachability commands (the plans, the metapackage, the grep, the record, the control); every proof with a `proved:` cell | B, then F |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: the base merge x the 81; T3's `*-lr` twins x the 77; T40's patches x the 12 | B |
| Analysis | `.../04-analysis.md` | Phase 4, § Finding Verification (4.5), **§ Renovation face** Q1 to Q7, **Q6 carrying the reachability table** (86 rows, each with `Already written:`), **Q7 carrying the twin map** (77 rows), Q4 the (a) and (b) states, Q5 the weight; Phase 4.6 `not applicable` with the row cited | C |
| Second opinions | `.../second-opinions/review-plan.json` | § 1's Local plan file with `tier_exception` and `reason`; no call | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (...)` with the `review-plan: local at epic tier under D-WORKFLOW-184` line | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`; the #585 proposal (the 81 and the twin map's count) as one `Renovation` item whose outcome names the coordinator's post; the five ROCKNIX rows as one item citing T3 | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #671 | `Audit: M6 T24 emulator recipes and files no shipped image builds -- N findings (...)`; one checkbox per item, agent-first | D |
| **The stage-D pause** | #671 | the punch list posted; the lane waits for the coordinator's dispositions (no stream is expected: nothing here changes) | D |
| Verification | `02-forward-audit.md` appended; `audit-completion.json` after the coordinator closes the audit issue | every proof's `proved:` cell one of `tree`, `history`, `tool-run` | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-emulators-dead-ends.md`, posted on #671 | the mini-retro's four answers; **what the slice did to the two time-to-play numbers** (nothing: say so) | G |
| Hand-back | #671 | `reviewed-at:` and `fixed-at:` in the body (the same commit when nothing changed); one comment: the tip, each artifact by path, the six checker exit codes, the API budget spent | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-emulators-dead-ends-671.md` | seeded by the coordinator; updated at every checkpoint | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session headed `#671`, stamped from the clock, prose through a quoted heredoc | every session |

## 7. Acceptance

The checklist on #671 is the contract (its body carries these fourteen,
written there with version 2 in place of the five generated ones; where
the two differ, #671 wins and the coordinator corrects the brief). Each
names the artifact that ticks it; the coordinator ticks at hand-back.

- [ ] `docs/audits/<date>-epic-m6-emulators-dead-ends/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-emulators-dead-ends/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included and the line `review-plan: local at epic tier under D-WORKFLOW-184` in its output.
- [ ] `second-opinions/review-plan.json` records `depth: local`, `reviewers: []`, `tier_exception: D-WORKFLOW-184` and a `reason` naming plan § 6c and `slices.json`'s `k: 24`.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (#585 for the proposal, T40's issue for a patch row), or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits (the same commit where nothing changed; no EmulationStation path), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed`.
- [ ] `01-research-notes.md` § Scope records the read hash, the filter of brief § 2 with its output (86 paths, 2,399 lines; 86 upstream-carried; 84 `unreached`, 2 `unshipped`; 85 recipes and 1 cmake file, or the deltas beside them), the provenance (0 fork changes since the base; 81 identical to `upstream/next` and 5 differing by upstream's `af70bd435b`), and the branch-vs-hash diff over the 86 (empty, or each hunk listed with its owner).
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c -E '^\| `(packages|projects)/' 02-forward-audit.md`` prints 86; each row's Q1 to Q7 cells answered or `n/a` with a reason.
- [ ] `02-forward-audit.md` § Mechanical checks records, with command, exit status and summary line, each of: the branch-vs-hash diff, the (a) loop (81 / 5), the (b) loop (80 rows: pin identical / moved / absent / not-read, with the API budget before and after), the three `viewplan` reads with the control, the metapackage and `git grep` reads per name, the record by name prefix over the five roots (85 with no build directory, the control built) and the `.info` trace, the two `pkgcheck` runs' counts, and the weight of the 81 (files, lines, bytes); a check that could not run is recorded with the reason, never as a pass.
- [ ] `04-analysis.md` § Renovation face Q6 carries the reachability table: 86 rows, each with the reads that decided it, the tier, the (a) and (b) states, the disposition (`kept: upstream's; #585 candidate` for the 81, `kept: upstream's; no shipped device builds it` for the five with T3's `Already written:` cited), and **an `Already written:` line on every row**; no row's disposition is a deletion, move or edit.
- [ ] `04-analysis.md` § Renovation face Q7 carries the twin map: 77 rows (the LibreELEC core, its ROCKNIX `*-lr` twin by name and by source or `no twin`, the two pins where a twin exists); § Q5 states the weight of the 81 in files, lines and bytes.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history` or `tool-run`; ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c 'PROOF:' 00-running-log.md``.
- [ ] Every punch item carries `question:`; the #585 proposal is one `Renovation` item whose outcome names the coordinator's post; no file under `packages/` or `projects/` is changed on this branch (`git diff --stat 8ebaf8daad <fixed-at> -- packages projects` is empty, or every hunk is a stream the coordinator briefed), and `git diff --diff-filter=DR --name-only 8ebaf8daad <fixed-at> -- packages projects` is empty.
- [ ] The retro exists at `docs/retros/<date>-m6-emulators-dead-ends.md`, is posted on #671, and says in those words that the slice did nothing to the two time-to-play numbers.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge, and `tools/lint-audit-artifacts` prints `PASS` on the folder; the six exit codes pasted on #671.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); the stage-D pause; an explicit maintainer pause on
#671; a blocker named on #671 (an API budget that does not recover, a
`viewplan` that will not run, two commands that disagree); a branch that
differs from `8ebaf8daad` on one of the 86 at stage A; or an execution
limit, stated as such with the running log current. A checkpoint is not a
stop. An idle session says it is idle on #671, **and does not end a turn on
a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#671`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #671` or the
  guard.
- The VM question written before any proof (§ 5: no).
- The mini-retro at stage G, posted on #671, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator.
- A register row the same session for any decision the slice forces (none
  expected); the highest Decided row on 2026-10-24 is D-WORKFLOW-197, the
  coordinator's; T8 runs beside this lane and may take 198.
- `tools/ceremony-check` before every push; never `--no-verify`; a merge
  with conflicts is checked for markers; the ledgers united by whole
  entries; **a commit names its paths**; the read tree under
  `.qa-scratch/t24/at-hash/` (§ 1); a whole-tree export, when one is wanted,
  under `/workspace/tmp/m6-t24/` after `df -i`, never `/tmp`.
- Commit messages `docs: ...`, with `Refs #671`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#671's checkboxes against their artifacts; the lint's `PASS` line with the
D-WORKFLOW-184 line; `review-plan.json`; the audit issue's checkboxes all at
an outcome; the coverage table's row count (86) and the twin map's (77);
every Q6 row's `Already written:` and no deletion; **re-running on an export
of the tip under `/workspace/tmp`: the membership block, the (a) loop, the
record by name prefix and the `pkgcheck` baseline in full, and the (b) read
on ten rows drawn with `shuf --random-source=<(yes t24)`** (A6);
`register-check` on a simulated merge with the coordinator's tip (the
ledgers united); the retro's four answers; the six exit codes. The lane
posts one hand-back comment naming the tip and each artifact by path,
writes `reviewed-at:` and `fixed-at:` into #671's body, then says it is
idle. After acceptance the coordinator closes the audit issue, prompts the
lane for `audit-completion.json` and the full lint, merges the branch in its
turn after the M7 candidate (after T30's), regenerates the ledgers, posts
the #585 proposal in the shape the lane wrote, and closes #671 when every
row is proven.

**The readings before dispatch** (plan § 3, principle 3): the epic's futro
(#798) carries a T24 kickoff addendum written with this version, and a
stranger's proof of this brief is run by a reader with no context before
dispatch; version 2 records what each found.
