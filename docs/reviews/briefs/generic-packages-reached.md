# Brief: M6.P2 T7, the generic packages the image builds (#654)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #654 differ, #654 wins and the
coordinator corrects the brief in the same session. **Version 1
(2026-10-24):** written after T3, T5 and T6 were accepted (#826, #837, #846
closed) and while T30 runs beside it, so the shapes their briefs' proofs
found wrong -- a count from the wrong tree, a baseline assumed, a tool
absent from the host, a line number from memory -- are answered from the
start, and every figure below was produced by a command at `8ebaf8daad`
(the tree) or in the inventory at P1's `2174265e9c` unless it says
*branch*. It goes through a stranger's proof before dispatch; version 2
records what it found. **Each command block sets its own variables**
(`D`): a Bash call in this harness starts a fresh shell. **This is a table
slice**: one row per recipe, read for currency against three sources; it
reads a recipe line by line only where a row needs it; **it moves no pin,
deletes nothing upstream carries and relocates no recipe** (the move table
is #645's).

## 1. Identity

- **Issue:** #654 `M6.P2 E848/T7: generic-packages: the generic packages
  the image builds`, slice `generic-packages-reached` (`k: 7`) in
  `docs/reviews/slices.json`, seventh in `docs/reviews/order.md` (its § T7
  paths line: *"266 paths, 7,612 lines, -- read, of which -- fork-own; 0
  patch and config lines; reach n/a 3, shipped 256, test 7"*; its `why`:
  *"upstream-carried recipes reached by a shipped plan or the test image's:
  pins against their projects' releases; with the build engine under
  D-WORKFLOW-186, the maintainer's weight on the build process ahead of any
  device target ('package updates ... fully up to date')"*). **Epic:** #848
  (the generic packages: this slice, T8 #655 the image's own recipes at
  Independent depth, T23 #670 the generic recipes no image builds), filed
  2026-10-24 with this brief; its futro is
  `docs/futros/2026-10-24-m6-generic-packages.md` (A1 to A9 are written
  into this version). **Milestone:** M6; its body holds the live order;
  read it first. **Predecessors:** #346 (the plan), #641 (the survey), #644
  (the build-path read: findings **15** -- *`make update` moves the three
  virtual packages' dependencies; LibreELEC's bumps reach `packages/`
  through the base merge; the fork has no check on the upstream-carried
  pins* -- **16** -- *the freshness tool's set is a diff, not a provenance*
  -- and **17** -- *upstream refuses any PR touching `packages/`*, #645),
  **T5 #652** (accepted: the fetch, `scripts/get_archive`, D-WORKFLOW-193/194),
  **T6 #653** (accepted: its late-binding sweep's leads on #654, posted
  08:57 UTC), **T3 #650** (accepted: the two-tier Q4 method of
  `docs/audits/2026_10_24-epic-m6-emulators-libretro/q4-pins-table.md` and
  `q4-pins.json`; #841's class). **Beside it:** T30 (#677, the standalone
  emulators) runs in the other lane (D-WORKFLOW-190); the two share no path
  (`portaudio` under `hatarisa/` is T30's row and #849; it is not in this
  set).
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, post on #645 or #585, or decide a question of scope: those are the
  coordinator's, reached through #654, one question at a time. What it does
  file: its own audit punch-list issue (stage D) and a `bug` issue for every
  defect it finds (D-WORKFLOW-187). Nothing else.
- **One worktree, one session.** Branch `feature/m6-generic-packages-reached-654`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-generic-packages-reached-654`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's
  pointer seeded (the two hashes are in the dispatch comment on #654).
  **Before that comment exists there is no worktree at that path and none
  of the first commands can run.** The session is the T5 lane's
  (`m6-t5-build-engine`, pane `wN:p7`), which has read the engine and its
  tools; its T5 and T6 worktrees stay beside this one, idle, until their
  merges, and nothing is written there. The primary checkout
  `/workspace/repos/pixelelated/distribution` stays on `next`
  (D-INFRA-025); the legacy checkout and `rocknix.worktrees/*` are the M7
  lane's, read only, never a process started there; the T1 to T6 and T30
  worktrees are other lanes', `git -C` only. **The rules in this worktree
  are `next`'s except the paths the dispatch comment lists** (on 2026-10-24
  for T6 they were seven: P1's `fork-workflow.md` and
  `instruction-files.md`; the coordinator's `generic-x64-vm-testing.md`
  paragraph `8c9b1d4721` and `engineering-practices.md` bullet
  `ab8f750784`; M7's `.claude/skills/council/IMPORTED-FROM.md`;
  `tools/lint-audit-artifacts` with `templates.md` from #810). Known stale
  facts in the rules (the legacy layout in eight files, #640) do not cost
  an hour here: every rule the work touches is named in § 3.
- **Model and effort:** Opus 5.5 (the maintainer, 2026-10-22: *"the work
  will be Opus 5.5"*) at high effort (the coordinator's setting for every
  lane since T1). Record what ran in `00-running-log.md`'s header.
- **Review depth: Local** (D-WORKFLOW-184: *Local (the executor alone; the
  lint and the counts are the check) for a dead-end table, a provenance
  table or a doctrine read*; `slices.json`'s `depth_reason`: *a currency
  table: each upstream-carried recipe's pin against its project's releases
  (plan § 6c)*). No external reviewer, no `npm install`, no Facilitator
  call. `second-opinions/review-plan.json` is still written: depth
  `local`, primary `anthropic/claude-opus-5-5`, lab `anthropic`, reviewers
  `[]`, **`"tier_exception": "D-WORKFLOW-184"` and `"reason": "plan § 6c
  and slices.json k 7: a currency table is Local"`** -- the two keys #810
  taught `tools/lint-audit-artifacts` to accept in an `-epic-` folder (its
  line prints `review-plan: local at epic tier under D-WORKFLOW-184 (...)`;
  T6's file is the model). Phase 4.6 is recorded as not applicable with the
  row cited; Phase 4.5 is done in full, and § 5's rule 4 -- what result
  would have produced a FAIL -- is asked of every PASS, because nobody else
  asks it here.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-generic-packages-reached-654
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-generic-packages-reached-654
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: this is not the lane's worktree (stacked on P1): stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists, nothing else
mkdir -p .qa-scratch/t7/at-hash && git archive 8ebaf8daad packages | tar -x -C .qa-scratch/t7/at-hash   # the read tree: 266 of its files are the slice's, the rest T23's; small enough for .qa-scratch
ls tools/renovation-inventory tools/renovation-status tools/renovation-drift docs/reviews/slices.json   # P1's
"$D/tools/rules-check"; echo "rc=$?"; "$D/tools/register-check"; echo "rc=$?"; "$D/tools/ceremony-check"; echo "rc=$?"   # rc 1 on 2026-10-24: W42 OVERDUE (M7's week), a retro DUE; neither is this lane's to pay
git push -u origin feature/m6-generic-packages-reached-654
test -f docs/reviews/briefs/generic-packages-reached.md || { echo "the brief is not in this tree: stop"; exit 1; }
cat .github/sessions/saved-session-state-feature-m6-generic-packages-reached-654.md
tail -3 /tmp/m7-m6-host-coordination-20261023.txt                   # the host's state: this slice needs no runtime, but the protocol is read
df -i /tmp | tail -1                                                 # never export a tree under /tmp: the tmpfs ran out of inodes on 2026-10-24
gh api rate_limit --jq '.resources.core | "\(.remaining)/\(.limit)"'    # the API budget § 5 spends; below 1,500 the loops wait
```

## 2. Scope

**266 paths, 7,612 lines; 250 upstream-carried and 16 fork-own; reach
`shipped` 256, `test` 7, `n/a` 3; 243 recipes (`package.mk`) and 23 other
files (6 `other`, 4 shell, 3 cmake, 3 config, 2 udev, 2 none, 1 markdown, 1
text, 1 systemd); every row read, no recipe read line by line unless a row
needs it.** The membership is the inventory's at P1's `2174265e9c`, with
the slice's rule (`k: 7`): the rows of the `generic-packages` area under
`packages/**` whose reach is `shipped`, `test` or `n/a`. **The area filter
is what keeps the emulation, kernel, firmware and driver trees out**
(`areas.json` excludes `packages/{emulation,linux,linux-firmware,linux-driver-addons}/**`,
every `.patch` and every `linux*.conf`), and the reach filter keeps T23's
1,604 unreached and unshipped rows out; a recipe under `packages/` that is
not in this slice's 266 is not this slice's, however much it looks like a
package. The three `n/a` rows are `packages/README.md`,
`packages/packages.mk.addon_template` and `packages/packages.mk.template`.
The seven `test` rows are the recipes only the GENERIC_X64 plan reaches:
`lm_sensors`, `slang`, `dmidecode`, `pciutils`, `ryzenadj`, `newt`,
`syslinux`. The re-derivation:

```bash
python3 -I - <<'PY'
import json, re, collections
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
def gm(p, g): return re.fullmatch(re.escape(g).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*"), p) is not None
t7 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "generic-packages"
      and gm(r["path"], "packages/**") and r["reach"] in ("shipped", "test", "n/a")]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t7), "lines", L(t7), dict(collections.Counter(r["tier"] for r in t7)), dict(collections.Counter(r["reach"] for r in t7)))
print(dict(collections.Counter(r["language"] for r in t7)))
pk = [r for r in t7 if r["path"].endswith("/package.mk")]
print("recipes", len(pk), "groups", dict(collections.Counter(r["path"].split("/")[1] for r in pk)))
print("with patches", sum(1 for r in pk if r["patches"]), "shadowed", sum(1 for r in pk if r["shadowed_by"]))
for r in sorted(t7, key=lambda r: r["path"]): print(r["reach"], r["tier"], r["lines"], r["path"])
PY
git ls-tree -r --name-only 8ebaf8daad -- packages | grep -v -E '^packages/(emulation|linux|linux-firmware|linux-driver-addons)/' | grep -c '/package.mk$'   # every generic recipe outside the excluded trees: the 243 are those the inventory reaches
```

Recorded (2026-10-24, at `2174265e9c`'s inventory, the tree at
`8ebaf8daad`): **266 paths, 7,612 lines**; tiers upstream-carried 250,
fork-own 16; reach `shipped` 256, `test` 7, `n/a` 3; **243 recipes** in
twenty groups: devel 45, x11 34, addons 25, sysutils 17, audio 16, graphics
16, python 15, network 14, textproc 10, compress 9, security 9, multimedia
7, tools 6, virtual 6, web 5, debug 3, lang 2, wayland 2, databases 1, print
1; **46 recipes carry patches** (T42's and T43's rows; this slice reads a
patch's header only to say what a bump would re-cut); **0 are shadowed by a
ROCKNIX override** (a shadowed generic copy is unreached, so T23's).
Reached by plan: GENERIC_X64-x86_64 234, SM8550-aarch64 234, H700-aarch64
227, SM8550-arm 152, H700-arm 150 of the 243.

**Provenance, by git and not by a tool's set (A4).** Against the base
`c445081a59` and against `upstream/next` (`e0f9deb899`):

```bash
P=.qa-scratch/t7/recipes.txt   # the 243 package.mk paths, from the block above
git diff --diff-filter=A --name-only c445081a59 8ebaf8daad -- $(cat $P) | wc -l      # 13: added by the fork
for f in $(git diff --diff-filter=A --name-only c445081a59 8ebaf8daad -- $(cat $P)); do git cat-file -e upstream/next:$f 2>/dev/null && echo "upstream-has $f" || echo "fork-only $f"; done | cut -d' ' -f1 | sort | uniq -c   # 13 fork-only
git diff --diff-filter=M --name-only c445081a59 8ebaf8daad -- $(cat $P)              # 3: libyaml, libsamplerate, syslinux
git diff --name-status upstream/next 8ebaf8daad -- packages/ | awk '{print $1}' | sort | uniq -c   # 16 A, 5 M over all of packages/: #645's 21 files (the 16 A are the 13 recipes, woff2's patch and webkitgtk's two)
FRESHNESS_HEAD=8ebaf8daad FRESHNESS_BASE=upstream/next tools/fork-package-freshness --list | tr ' ' '\n' | grep -c '^packages/'   # 13: the tool's set under packages/ equals the fork-added 13 (its other 34 entries are T8's)
```

Recorded: **13 recipes added by the fork and absent on `upstream/next`**
(brotli 1.2.0, ruby 3.3.12, unifdef 2.12, openjpeg 2.5.4, woff2 1.0.2,
glib-networking 2.90.0, libtasn1 4.21.0, dmidecode 3.7, qrencode 4.1.1,
ryzenadj 0.19.0, libpsl 0.23.3, libsoup 3.8.0, webkitgtk 2.54.1 -- the
sign-in window's chain, #576), **3 upstream recipes the fork edited**
(`libyaml`: `PKG_DEPENDS_HOST="ccache:host"` with a seven-line comment on the
cold-tree ordering it fixes; `libsamplerate`: `--with-pic`; `syslinux`: two
`cp` lines for `ldlinux.c32`), **227 byte-identical to both bases**. The
13 are the whole of `tools/fork-package-freshness`'s set under `packages/`;
none is an orphan of the kind #644 finding 16 describes (an orphan is
present at the base and deleted upstream; these were never upstream's).
**Every one of the 16 sits where upstream refuses it** (#645: a PR touching
`packages/**` fails `trigger-fail-if-upstream-changed.yml`; upstream's
`AGENTS.md` puts recipes under `projects/ROCKNIX/packages`); #645's first
criterion is a table of dispositions for the 21 files, and this slice
proposes the 16 recipes' rows for it (§ 4 Q7), moving nothing.

**The pins at the hash.** 232 version strings, 10 commit hashes (`x264`,
`arm-mem`, `configtools`, `crossguid`, `heimdal`, `kmsxx`, `dbussy`,
`fuse`, `udevil`, `populatefs`), 1 recipe with no `PKG_VERSION` of its own
(`harfbuzz-icu` sources `harfbuzz`'s recipe: the freshness tool's INHERITED
class). By `PKG_URL`'s host over the 242 with a version: other 78,
github.com 73, freedesktop.org 39, gnu.org 23, kernel.org 12, gitlab 10,
sourceforge 6, no `PKG_URL` 1 -- *other* is the lead class, read by host at
stage B. **Checksums:** every archive recipe carries `PKG_SHA256`; the 7
without one are the 6 virtual packages (`alsa`, `autotools`, `corefonts`,
`debug`, `misc-packages`, `toolchain`, each `PKG_URL=""`) and
`harfbuzz-icu`. T5's five archive versions without one (D-WORKFLOW-194:
`atf`, `rkbin`, `libmali-vulkan`, `sway`) are ROCKNIX overrides under
`projects/`, outside this set; the generic `atf`, `rkbin` and `sway` copies
at `packages/tools/` and `packages/wayland/compositor/` are shadowed, so
T23's. **The expected count of archive recipes without a checksum here is
0** (A6); any other number is the first lead.

**Three sources of "current", and the mover of each (A1).** This is what
makes the table honest, and the futro's § 1 carries the reasoning:

| Source | What it is | Its mover | Read how |
| --- | --- | --- | --- |
| (a) ROCKNIX | `upstream/next` at `e0f9deb899` | the base merge (`release-candidates.md` step 0) | `git diff --quiet upstream/next 8ebaf8daad -- <path>`; **0 commits touch `packages/` since the base** (`git log --oneline c445081a59..upstream/next -- packages/ \| wc -l` is 0, of 325 commits overall), so every upstream-carried row is identical today |
| (b) LibreELEC | `LibreELEC/LibreELEC.tv` master | ROCKNIX merging LibreELEC master (the last on `upstream/next` is `d43d166b7a`, 2026-08-12: LibreELEC's PR #11671) -- **the mover of every upstream-carried pin here**; the fork moves none of them | the GitHub contents API, `repos/LibreELEC/LibreELEC.tv/contents/<path>?ref=master`, one call per recipe (probed 2026-10-24 on `pciutils`: `3.15.0` and the same sha256 on both sides); **no remote is added to the repository** |
| (c) the project | the project's own current release | the fork, for the 13 it introduced (D-WORKFLOW-024); nobody the fork can move, for the 237 others | `tools/fork-package-freshness` for the 13 (its host handlers: GitHub releases and tags, GNOME's `cache.json`, GNU's listing, webkitgtk.org, ruby's cache, dotat.at); the API `compare` for the 10 hash pins where the host is GitHub; **not read** for the 227 untouched upstream-carried recipes, whose row says `follows LibreELEC` with (b)'s version |

`make update` is not a mover here: `scripts/update_packages` walks
`projects/ROCKNIX/packages` only (its `PKG_PATH` assignment), from the
emulators, es-themes and gamesupport virtual packages' dependency lists,
each to its repository's branch head, honouring `config/blocklist`; it
never touches a `packages/**` recipe. `tools/update-pkg` and the 62
`tools/update-functions/` are run by nobody (T6's Q6 table). So #644
finding 15's T7 half is settled before stage A -- the base merge is the
only mover of these pins -- and every row says so; the T8 half (is `make
update` ever run) is T8's.

**The record agrees with `shipped`, almost (A5).** The five M7 build roots
on this host, read only (`ls <root>/build`, the version suffix stripped):
236 of the 243 names have a build directory in at least one root
(GENERIC_X64 226, H700-aarch64 220, H700-arm 149, SM8550-aarch64 227,
SM8550-arm 151). The 7 with none are the 6 virtual packages (no build
directory by construction) and **`ntfs-3g_ntfsprogs`** (reach `shipped`,
`reachable_by` all three shipped plans; `PKG_SITE` github.com, `PKG_URL`
tuxera.com): the first row the slice settles, with `tools/viewplan` per
plan in its own worktree, before any row says `shipped` on the record's
authority.

```bash
R=/workspace/repos/rocknix.worktrees
for d in $R/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64 $R/m7-signin-h700-build-20261023-06/build.pixelelated-H700.aarch64 $R/m7-signin-h700-build-20261023-06/build.pixelelated-H700.arm $R/m7-signin-sm8550-build-20261023-03/build.pixelelated-SM8550.aarch64 $R/m7-signin-sm8550-build-20261023-03/build.pixelelated-SM8550.arm; do
  LC_ALL=C ls "$d/build" | sed -E 's/-[0-9][0-9a-zA-Z._+-]*$//; s/-[0-9a-f]{40}$//' | LC_ALL=C sort -u > ".qa-scratch/t7/built-$(basename $d).txt"; done   # read only; never a process in those trees
```

**The hash.** The slice's bytes are `8ebaf8daad`'s; `reviewed-at:` is the
branch `HEAD` at stage A; the read is made on the at-hash tree
(`.qa-scratch/t7/at-hash/packages/`, the first block). The branch differs
from the hash on none of the 266 on 2026-10-24 (P1 and the coordinator
changed nothing under `packages/`), and the check is made over the slice's
own paths: the § 2 block's path column is written to
`.qa-scratch/t7/paths.txt` and `git diff --stat 8ebaf8daad HEAD -- $(cat
.qa-scratch/t7/paths.txt)` is empty; a non-empty result there is the first
lead.

**The policy on change (plan § 5; D-WORKFLOW-187; D-UI-079's spirit):**
**no pin moves, no upstream-carried file is deleted, no recipe is
relocated.** A bump is a build, and the renovation builds nothing: a
fork-introduced recipe found BEHIND is a row whose disposition is a
Backlog issue in #839's shape (the coordinator files it at acceptance,
one per recipe, for the first build after the M7 candidate). An
upstream-carried recipe behind LibreELEC master is dispositioned `follows
the base merge; LibreELEC master at <version>` -- the fork proposes nothing
to LibreELEC, which is outside its lanes. The 16 fork-own recipes' homes
are #645's table; this slice writes the proposed rows (§ 4 Q7) and the
coordinator posts them. A defect (a URL gone or redirected, a checksum
that disagrees with the record, a recipe `pkgcheck` fails in a way a build
would meet) is a `bug` with the code-trace shape, `Already written:` and
the VM line; its fix, if contained, lands under a stream brief at stage E
(a `PKG_URL` or `PKG_SHA256` line is a fix the table can carry; a bump is
not).

**Drift.** `next` is `8ebaf8daad`; the M7 candidate's merge moves it after
this slice; the coordinator merges `next` into the branch never between
stage A and stage D, and re-baselines after. `tools/renovation-drift` is
the coordinator's; this lane runs it to read.

## 3. Read first

- `.github/sessions/saved-session-state-next.md` (the M7 lane's canonical
  checkpoint; what runs on this host, not a work queue) and this lane's own
  pointer.
- **The rules this work touches** (`working-principles.md` § Pre-flight:
  open them, say which were read): `engineering-practices.md` (§ Verify the
  artifact; § A name is not a behaviour, including its bullet *a count or a
  line number is a claim about one tree*; § Check upstream early,
  D-WORKFLOW-162; § Consider contributing every applicable fix upstream,
  D-WORKFLOW-164/165; § Guards must fail closed -- the HEAD probe that
  cannot answer is *not read*, never *answers*), `packaging-and-patches.md`
  (the `package.mk` fields; what `tools/pkgcheck` checks),
  `device-builds.md` (§ After rebasing item 3: an override's *effective*
  `PKG_VERSION`; § A metadata-only upstream change still rebuilds
  everything -- what a `PKG_SHA256` sweep costs; § A build that fetches its
  own dependency), `fork-workflow.md` (§ When to merge up:
  `tools/fork-package-freshness` exits 0 before an upstream PR; § Personal
  paths), `release-candidates.md` (step 0: where currency lands),
  `upgrade-and-install.md` (`Already written:` for every disposition and
  bug), `bugs-are-agent-first.md` (rule 6: an upstream defect contained is
  ours to close), `issue-tracking.md`, `vm-first.md` (§ 5 answers it: no, a
  table runs no guest), `worktrees.md` (the layout, superseded by § 1).
- The code-auditor skill whole (`SKILL.md`, `references/phases.md`,
  `review-levels.md`, `templates.md`, `anti-patterns.md`); the renovation
  face is plan § 6b; the Local depth plan file is § 1's.
- **T5's audit** (`docs/audits/2026_10_24-epic-m6-build-engine/` on
  `feature/m6-build-engine-652` at `52e6794ba7`, read with `git -C` or
  `git show`): its coverage rows for `scripts/get_archive`, `get_git` and
  `unpack` (what a fetch does with `PKG_URL`, `PKG_SHA256` and a redirect),
  its E6 stream in `docs/reviews/briefs/t5-streams.md` and D-WORKFLOW-193/194
  (the checksum policy and the per-shape count -- read before any checksum
  row here). **T6's audit** (`docs/audits/2026_10_24-epic-m6-build-engine-upstream-tools/`
  on its branch at `37d1d98aed`): `02-forward-audit.md` § Leads from the
  sweeps (the two late-binding leads on this slice's recipes and the
  `wireplumber` parser case, routed to #657), its Q6 table for
  `tools/update-pkg` and `tools/update-functions/` (unreached), and the
  widened `tools/pkgcheck` at `44f64842b6` (read from that branch with `git
  show`, run from this worktree; A7). **T3's audit** (`q4-pins-table.md`,
  `q4-pins.json`): the two-tier Q4 shape and its dispositions, and its S6
  (#841: a renamed repository's archive). **T30's** post of 09:02 UTC on
  #677 and #849: the gone source, and the cache as the only copy.
- **`docs/reviews/build-path-read.md`** (#644): findings 15, 16 and 17 whole
  with § 5's recommendations; the other findings named with their carriers
  so none is taken here. **#645** whole: the move table this slice feeds.
- `docs/blindspot-register.md` whole once (76 entries on the branch under
  the numbers 1 to 75; 29 is used twice, #811), then **13** (assumed done:
  the freshness tool's last exit 0), **22** (a probe that cannot report
  absence: a HEAD refused with 405 is not *gone*, the ranged GET is the
  second pattern; a 404 from the contents API is *absent*, a 403 is *not
  read*), **46** (a name read as a behaviour: `PKG_SITE` is a homepage, not
  a source -- 159 of these recipes name a site on one host and fetch from
  another), **51**, **75** (a corpus read on the wrong tree).
- Decisions by ID: D-WORKFLOW-184 (Local for a table), D-WORKFLOW-186 (the
  build process first), D-WORKFLOW-187 (no release gate; every defect a
  bug; no bump here), D-WORKFLOW-164/165 (upstream contributions prepared,
  submissions held), D-WORKFLOW-162 (check upstream early), D-WORKFLOW-024
  (`tools/fork-package-freshness`: the fork's own packages current -- its
  13 entries here are this slice's rows), D-WORKFLOW-193/194 (the fetch
  fails without a checksum; the count per shape), D-UI-079 (change stays
  inside the fork's lanes: LibreELEC's recipes are outside them),
  D-INFRA-022 (a required source input is retained: the cache's copy of a
  gone source), D-INFRA-025/026.
- Issues: #654 (this), #848 (the epic), #655 and #670 (T8 and T23: what
  they take so this slice does not), #644/#645, #841 and #849 (the two
  classes of a fetch that fails from an empty cache), #844 (the fetch check
  proposed as a tool; this slice's sweep is its manual form), #839 (the
  shape of a bump issue), #585 (the contribution queue: an upstream-carried
  recipe's defect lands there), #657 (T10: the fork's tooling, where a tool
  defect goes), #576 (webkitgtk), #810 (the lint's Local-at-epic rule), #809
  (the inventory's renderings). Every `gh` call carries `--repo
  pixelelated/distribution`.
- Tools, read whole before run: `tools/fork-package-freshness` (its header
  names the hosts it can read and its five classes), `scripts/update_packages`
  and `tools/update-pkg` (read, **never run**: both edit recipes in place),
  `tools/pkgcheck`, `tools/viewplan`.

## 4. The questions

All seven apply (plan § 4); for a currency table Q4 is the spine and Q3,
Q6 and Q7 hang off it; Q1, Q2 and Q5 apply in full to the 16 fork-own rows
and as counts to the rest.

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | A recipe pinned to a retired series or a retired host (a python2-era helper, a `sourceforge` download, a `PKG_URL` under a personal GitHub namespace rather than the project's -- portaudio's shape, #849), and for the 16 fork-own rows the recipe's own shape against `packages/README.md` | the `PKG_URL` host column; the 73 GitHub owners read against the project `PKG_SITE` names; one row per finding, `Renovation` unless a build would fail |
| Q2 Standards | `tools/pkgcheck` over the 243 at the hash: **the baseline count first** (T6 saw 12 FAILs on real recipes over the whole tree; this slice's own number over its 243 is recorded before one FAIL is read as a finding), then T6's widened copy from this worktree; each row says which copy produced it; the two leads `jre.zulu/package.mk:12` and `mesa-reusable/package.mk:14` read directly; `wireplumber`'s parser false positive is #657's and is cited, not re-found | the two runs' PASS/FAIL counts and the FAIL list; a FAIL on an upstream-carried recipe is a `Renovation` row with a #585 candidate unless the shape would break a build (then a `bug`, rule 6) |
| Q3 Bugs | A recipe that fails a build from an empty source cache: a `PKG_URL` that redirects (#841's class: the archive's sha256 may have changed) or is gone (#849's class); a `PKG_SHA256` that disagrees with the shared cache's `.sha256` stamp for the same file name; an archive recipe with no checksum (expected 0, A6); a recipe whose `PKG_VERSION` and `PKG_URL` disagree (a URL that names a version the pin does not) | § 5's sweep: the HEAD probe per URL (no `-L`), the cache stamps, the per-shape checksum count; one `bug` per defect in #849's shape with the cache named as a retained input |
| Q4 Currency | **The table**: one row per recipe (243) with the pin, its shape (version / hash / inherited), and the three sources -- (a) identical to `upstream/next` or not; (b) LibreELEC master's `PKG_VERSION` for the same path, or `absent`, or `not read`; (c) the project's release for the 13 fork-introduced (the freshness tool's class: CURRENT / BEHIND / PINNED / UNKNOWN) and the commits behind the default branch for the 10 hash pins where readable -- and **a disposition naming the mover**: `current`; `follows the base merge; LibreELEC master at <v>`; `fork's: Backlog bump proposed (#839's shape)`; `pinned on purpose (# freshness: pinned -- <why>)`; `unknown: <host> not readable` | § 5's three loops with their exit codes and counts; the 227 untouched rows' (c) cell reads `not read: follows LibreELEC`; a row never reads *current* on a source that was not read |
| Q5 Efficiency | For the 16 fork-own rows, what the recipe asks of a build (`webkitgtk`'s `-j4` cap and its 114 lines; `ruby`'s host build; a `PKG_BUILD_FLAGS` that disables a cache) -- read, not measured: no build runs; for the rest, a count of recipes whose `PKG_SHA256` sweep would restamp them (none here: the sweep is upstream's past) | reading only, each claim with its line; `not measured` is the honest cell everywhere a number would need a build |
| Q6 Dead ends | Within this set everything is reached by definition; the row class here is **claimed shipped, built in none of the five recorded roots**: the 6 virtual packages (by construction) and `ntfs-3g_ntfsprogs` (A5), settled by `tools/viewplan` per shipped plan in this worktree before the row stands; and any `test` row the GENERIC_X64 root did not build | the five `built-*.txt` files, the `comm` against the 243 names, and the `viewplan` outputs; a `shipped` row the record contradicts is a note for the inventory's owner (the coordinator files it under #657's epic), not a change here |
| Q7 Clarity | **The #645 rows**: for each of the 16 fork-own recipes a proposed disposition for #645's move table -- `move to projects/ROCKNIX/packages/<group>/<name>` (a ROCKNIX override that shadows nothing, since none exists upstream), `keep fork-only, excluded from docs/pr-series/map.txt`, or, for the 3 edited upstream recipes, `propose the hunk to LibreELEC through #585` or `drop at the next base merge` -- written in `04-analysis.md` for the coordinator to post; a `PKG_SITE` that names something other than the project (portaudio's shape); two recipes for one library (none expected: `shadowed_by` is 0 here) | one table of 16 rows with the reason per row; counts for the rest |

A finding is one question with its evidence; `Renovation` is the category
for Q1, Q5, Q6 and Q7 items that are not defects. A Q3 finding is a `bug`
(D-WORKFLOW-187).

**The ladder (`working-principles.md` § Enforcement depth):** the table's
own guard is #844 -- *does every archive recipe's URL still serve the bytes
its `PKG_SHA256` names?* -- which this slice runs by hand once and proposes
as the scheduled tool it already is on the Backlog, with what its sweep
learned about the hosts (which refuse HEAD, which redirect by policy).

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor; the file numbers its fifth rule `3.`, #685's lead):

1. Tracker state is never sole evidence: every verdict cites the tree
   (`git grep`, `git log`, `git diff`), an API response saved to the
   scratch, a probe's status line, or a document's line.
2. Mechanical evidence outranks reading: a version is a line in a recipe
   at a named hash or in an API body saved under `.qa-scratch/t7/`, not a
   memory of a release.
3. **For a currency table, the target is the tree, the record and the
   release sources**: the at-hash recipes; `upstream/next`; LibreELEC
   master through the contents API; the hosts the freshness tool reads; the
   shared source cache's `.sha256` stamps and the five M7 roots' `build/`
   listings -- **read only, through the filter where a log or config is
   read, never a process started in an M7 worktree, never a file moved in
   the cache**. No guest: a table runs nothing on a guest. No build.
4. An assertion that cannot fail is not evidence: before a row says
   *identical*, *current* or *answers*, the same command was seen to say
   *differs*, *behind* or *redirects* on a row where it should (the 16
   fork-own rows are the positive control for (a); the futro's #841 and
   #849 classes are the controls for the probe, reproduced on `fbalpha2019-lr`'s
   old URL and `portaudio`'s -- two recipes outside this set, probed for the
   control alone and recorded as such).
5. Subagent output is a lead, never evidence; fan-out is read-only
   research only (D-WORKFLOW-183).

**What runs on the VM, and how.** Can this be done on the VM? **No** -- the
slice is a currency table over recipes; its bench is the tree, the record
and the release sources, all read from the host. Nothing here touches a
handheld, a person's cloud, a shared QA backend, a QA guest or a build. The
host handoff file is read for the protocol alone.

- **The host-side checks**, each run with its command, exit status and
  summary line in `02-forward-audit.md`; a check that cannot run is
  recorded as such, never as a pass:
  ```bash
  D=/workspace/repos/pixelelated/distribution.worktrees/m6-generic-packages-reached-654
  cd "$D"; mkdir -p .qa-scratch/t7/le .qa-scratch/t7/probe
  # the paths and the recipes (§ 2's block writes both); the hash check over the slice's own paths
  wc -l < .qa-scratch/t7/paths.txt; wc -l < .qa-scratch/t7/recipes.txt                                  # 266, 243
  git diff --stat 8ebaf8daad HEAD -- $(cat .qa-scratch/t7/paths.txt) | tail -1                           # empty on 2026-10-24
  # (a) ROCKNIX: identical or differs, per recipe; 16 differs expected (13 absent upstream, 3 edited)
  while read -r p; do if git cat-file -e upstream/next:"$p" 2>/dev/null; then git diff --quiet upstream/next 8ebaf8daad -- "$p" && echo "identical $p" || echo "differs $p"; else echo "absent-upstream $p"; fi; done < .qa-scratch/t7/recipes.txt > .qa-scratch/t7/q4a.txt; cut -d' ' -f1 .qa-scratch/t7/q4a.txt | sort | uniq -c
  # (b) LibreELEC master, serially, the budget read first and last; a 404 is "absent", any other non-200 is "not read"
  gh api rate_limit --jq '.resources.core.remaining'                                                       # start only above 1,500
  while read -r p; do out=$(gh api "repos/LibreELEC/LibreELEC.tv/contents/$p?ref=master" --jq .content 2>.qa-scratch/t7/le/err); rc=$?; if [ $rc -eq 0 ]; then printf '%s\n' "$out" | base64 -d > ".qa-scratch/t7/le/$(echo "$p" | tr / _)"; printf '%s %s\n' "$p" "$(grep -m1 '^PKG_VERSION=' ".qa-scratch/t7/le/$(echo "$p" | tr / _)" | cut -d'"' -f2)"; elif grep -q 'HTTP 404' .qa-scratch/t7/le/err; then echo "$p absent"; else echo "$p not-read"; fi; sleep 0.4; done < .qa-scratch/t7/recipes.txt > .qa-scratch/t7/q4b.txt
  gh api rate_limit --jq '.resources.core.remaining'
  # (c) the project: the freshness tool over the 13 (read-only; network; exit 2 where a host cannot be read, recorded as UNKNOWN)
  FRESHNESS_HEAD=8ebaf8daad FRESHNESS_BASE=upstream/next tools/fork-package-freshness $(FRESHNESS_HEAD=8ebaf8daad FRESHNESS_BASE=upstream/next tools/fork-package-freshness --list | tr ' ' '\n' | grep '^packages/' | xargs -n1 basename) | tee .qa-scratch/t7/q4c.txt; echo "rc=$?"
  # the 10 hash pins: commits behind the default branch where the host is GitHub (the tool's own method); other hosts "unknown"
  # the fetch sweep: the URL expanded as the build expands it, probed with HEAD and no -L; a redirect is #841's class (then, and only then, a full fetch into an empty directory to compare sha256); 405 or 403 on HEAD -> a ranged GET; 404 or no answer is #849's class
  while read -r p; do n=$(basename "$(dirname "$p")"); url=$(PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 bash -c '. config/options "$1" >/dev/null 2>&1; printf "%s" "$PKG_URL"' _ "$n"); [ -z "$url" ] && { echo "$n no-url"; continue; }; printf '%s %s %s\n' "$n" "$(curl -sS -o /dev/null --head --max-time 30 -w '%{http_code} %{redirect_url}' "$url" 2>/dev/null || echo '000')" "$url"; sleep 0.2; done < .qa-scratch/t7/recipes.txt > .qa-scratch/t7/probe/head.txt; awk '{print $2}' .qa-scratch/t7/probe/head.txt | sort | uniq -c
  # the cache stamps against the recipes' checksums (read only; the cache is never moved)
  while read -r p; do n=$(basename "$(dirname "$p")"); s=$(grep -m1 '^PKG_SHA256=' ".qa-scratch/t7/at-hash/$p" | cut -d'"' -f2); for f in /workspace/cache/rocknix-sources/"$n"/*.sha256; do [ -f "$f" ] || continue; c=$(cut -c1-64 "$f"); [ "$c" = "$s" ] && echo "match $n" || echo "stamp-differs $n $(basename "$f")"; done; done < .qa-scratch/t7/recipes.txt | cut -d' ' -f1 | sort | uniq -c
  # the checksum count per shape (D-WORKFLOW-194): top-level or in a case branch
  while read -r p; do grep -q '^PKG_URL=' ".qa-scratch/t7/at-hash/$p" || continue; grep -q 'PKG_SHA256=' ".qa-scratch/t7/at-hash/$p" || echo "no-sha $p"; done < .qa-scratch/t7/recipes.txt   # 7 on 2026-10-24: the 6 virtual packages and harfbuzz-icu, none an archive
  # pkgcheck, baseline at the hash, then T6's widened copy run from this worktree
  for p in $(cat .qa-scratch/t7/recipes.txt); do tools/pkgcheck "$(basename "$(dirname "$p")")" >/dev/null 2>&1 && echo PASS || echo FAIL; done | sort | uniq -c
  git -C /workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-upstream-tools-653 show 44f64842b6:tools/pkgcheck > .qa-scratch/t7/pkgcheck-t6 && chmod +x .qa-scratch/t7/pkgcheck-t6   # read from T6's branch; run here, never there
  # the record: the five roots' built names against the 243 (§ 2's block), then viewplan for the 7 that match none
  LC_ALL=C comm -23 <(sed 's#.*/\([^/]*\)/package.mk#\1#' .qa-scratch/t7/recipes.txt | LC_ALL=C sort -u) <(cat .qa-scratch/t7/built-*.txt | LC_ALL=C sort -u)
  ```
- **A read is free and goes through the filter** (`grep -v -i -E
  'key|pass|token|user|psk|login'` on any log or config read from an M7
  root or the cache). The wordlist (`~/.config/rocknix/forbidden-terms`) is
  never read. The API responses are saved under `.qa-scratch/t7/le/` (the
  recipes' text, nothing private) so the table can be re-derived without
  re-spending the budget.

**What never runs in this slice:** a build; a guest; a command on a
handheld, a cloud or a shared backend; a process in an M7 worktree; a
model call outside `tools/council/run` (none expected: Local); `npm
install`; `git remote add` (the contents API is the read); `make update`,
`scripts/update_packages`, `tools/update-pkg` or `tools/update-scan` (they
edit recipes); a full archive download except for a URL the probe
redirected (then once, into an empty directory under `.qa-scratch/t7/`);
`curl -L` on the probe (the redirect is the finding); a move, copy or
deletion in `/workspace/cache/rocknix-sources/`; a pin change; a deletion
of an upstream-carried file; a recipe relocated; an edit at stage B (a
finding is a row; the edit waits for its stream brief); `--no-verify`;
bare `git stash`; `git worktree remove --force` or `rm -rf` of any
worktree; a write in another lane's worktree or under
`/workspace/repos/rocknix*`; a tree export under `/tmp` (use
`/workspace/tmp/m6-t7/` after `df -i`); a change to the order, the slices,
the plan, this brief, #654's criteria or the M6 body (D-WORKFLOW-189); a
comment on #645 or #585 (the coordinator posts the slice's proposals); a
GitHub issue other than the audit punch-list issue and `bug` issues.

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#654`
(`Refs #654`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-generic-packages-reached/00-running-log.md` | the skill's flight recorder: the model and effort, `reviewed-at` with `8ebaf8daad` beside it, every command of § 5 with its exit status, the API budget before and after each loop, every `PROOF:` line, the time of each entry from `date -u` | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 266 re-derived with § 2's filter and its output, the provenance block's counts (13 / 3 / 227), the branch's deltas from the hash (none expected); § Phase 1: the three sources and their movers in the slice's own words, the host classes, the record's 236 of 243 | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #654's checklist, plus **a coverage table with one row per path** (266; the first cell the path in backticks so ``grep -c -E '^\| `packages/'`` counts them), § Mechanical checks (every § 5 block with command, exit status, summary), § The fetch sweep (the status-code histogram, every non-200 row with its disposition), § The #644 findings (15, 16, 17 with their dispositions here; the others named with their carriers); every proof with a `proved:` cell | B, then F |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: the fetch (T5's `get_archive`) x the sweep; the freshness tool (D-WORKFLOW-024) x the 13; `shadowed_by` (T23) x this set's 0; #645 x the 16 | B |
| Analysis | `.../04-analysis.md` | Phase 4, § Finding Verification (4.5 in full), **§ Renovation face** Q1 to Q7 (all seven required), **Q4 carrying the currency table** (243 rows: pin, shape, (a), (b), (c), disposition naming the mover; also written as `q4-table.md` and `q4-pins.json` beside it, T3's shape), **Q7 carrying the 16 proposed #645 rows**, Q6 the record's seven; Phase 4.6 `not applicable` with the row cited | C |
| Second opinions | `.../second-opinions/review-plan.json` | § 1's Local plan file with `tier_exception` and `reason`; no call, no provenance file | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (does not certify resolution)`, with the line `review-plan: local at epic tier under D-WORKFLOW-184 (...)` | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category (`Renovation` where not a defect), where (file:line at `8ebaf8daad`), acceptance; the YAML `punch_index`; the fork-introduced BEHIND rows as items whose outcome is *a Backlog issue in #839's shape, the coordinator's*; the #645 rows as one item whose outcome is *posted on #645 by the coordinator* | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #654 | `Audit: M6 T7 the generic packages the image builds -- N findings (...)`; one checkbox per item, agent-first (`tools/box-check --issue N` passes) | D |
| Bug issues | GitHub, label `bug`, `Bug:` title, milestone-less | one per defect (D-WORKFLOW-187): the code trace shape, `Already written:` (for a fetch defect: *nothing on devices; the cache's stamp*), the VM line (*n/a -- a fetch property, proved on the host*), the cache named as a retained input where the bytes have no other copy (D-INFRA-022, #849's shape) | D |
| **The stage-D pause** | #654 | the punch list posted with the audit issue's and the bugs' numbers; the lane waits for the coordinator's stream briefs (plan § 6b E; D-WORKFLOW-189) -- meanwhile it drafts nothing under `packages/` | D |
| Remediation | the branches the stream briefs name | each stream as its brief says; **no pin moved, no upstream-carried file deleted, no recipe relocated**; a `PKG_URL` or `PKG_SHA256` fix with its empty-directory fetch as the test | E |
| Verification | `02-forward-audit.md` appended; `audit-completion.json` after the coordinator closes the audit issue | every proof's `proved:` cell one of `tree`, `history`, `fixture`, `fix-tree`, `fix-pending-image` (a URL fix is proved by a fetch into an empty directory: `fix-tree`) | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-generic-packages-reached.md`, posted on #654 | the mini-retro's four answers with its scoped audit; **what the slice did to the two time-to-play numbers** (nothing: say so); its *adjustments* are proposals for the coordinator | G |
| Hand-back | #654 | `reviewed-at:` and `fixed-at:` in the body; one comment: the tip, each artifact by path, the six checker exit codes, each fix's `proved:` class, the API budget spent | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-generic-packages-reached-654.md` | seeded by the coordinator; updated at every checkpoint | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session headed `#654`, stamped from the clock | every session |

## 7. Acceptance

The checklist on #654 is the contract (its body carries these seventeen,
written there with version 2 in place of the five generated ones; where
the two differ, #654 wins and the coordinator corrects the brief). Each
names the artifact that ticks it; the coordinator ticks at hand-back.

- [ ] `docs/audits/<date>-epic-m6-generic-packages-reached/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-generic-packages-reached/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included and the line `review-plan: local at epic tier under D-WORKFLOW-184` in its output.
- [ ] `second-opinions/review-plan.json` records `depth: local`, `reviewers: []`, `tier_exception: D-WORKFLOW-184` and a `reason` naming plan § 6c and `slices.json`'s `k: 7`.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (#585 for an upstream-carried recipe's defect, #645 for the 16 rows, #657 for a fork tool's defect, a Backlog issue in #839's shape for a fork-introduced bump), or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits the read and the fixes were made at (the read on `8ebaf8daad`'s bytes; no EmulationStation path), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed`.
- [ ] `01-research-notes.md` § Scope records the read hash, the filter of brief § 2 with its output (266 paths, 7,612 lines; 250 upstream-carried, 16 fork-own; 256 `shipped`, 7 `test`, 3 `n/a`; 243 recipes, or the deltas beside them), the provenance counts from the two bases (13 added and absent upstream, 3 edited, 227 untouched), and `git diff --stat 8ebaf8daad HEAD -- $(cat .qa-scratch/t7/paths.txt)` (empty, or each hunk listed with its owner).
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c -E '^\| `packages/' 02-forward-audit.md`` prints 266; each row's Q1 to Q7 cells answered or `n/a` with a reason.
- [ ] `02-forward-audit.md` § Mechanical checks records, with command, exit status and summary line, each of: the branch-vs-hash diff over the slice's paths, the (a) loop with its `identical` / `differs` / `absent-upstream` counts, the (b) loop with its row count and the API budget before and after, the freshness tool's run over the 13 with its exit code and each recipe's class, the fetch sweep's status-code histogram, the cache-stamp comparison's counts, the per-shape checksum count (expected 7, none an archive), and the two `pkgcheck` runs' PASS/FAIL counts; a check that could not run is recorded with the reason, never as a pass.
- [ ] `04-analysis.md` § Renovation face Q4 carries the currency table: 243 rows (``grep -c -E '^\| `packages/' q4-table.md`` prints 243), each with the pin, its shape, the (a), (b) and (c) cells, and a disposition from the five of § 4 Q4 that names the mover; **no row reads `current` on a source whose cell is `not read`**, and every `BEHIND` row of the 13 is a punch item whose outcome names a Backlog issue in #839's shape.
- [ ] `04-analysis.md` § Renovation face Q7 carries sixteen proposed rows for #645's move table (one per fork-own recipe, with the reason), and § Q6 settles the seven names built in none of the five recorded roots (six virtual by construction; `ntfs-3g_ntfsprogs` by `tools/viewplan` per shipped plan, outputs quoted).
- [ ] `02-forward-audit.md` § The fetch sweep lists every `PKG_URL` whose HEAD probe did not answer 200 with its status, its disposition and, for a redirect, the sha256 of the archive fetched from the redirect target against the recipe's `PKG_SHA256`; every gone or mismatched URL is a `bug` issue cited by number; the two control probes (`fbalpha2019-lr`'s old URL, `portaudio`'s) are recorded as controls.
- [ ] `02-forward-audit.md` § The #644 findings carries findings 15, 16 and 17 with their dispositions here (15: the base merge is the only mover of these pins, with `scripts/update_packages`'s `PKG_PATH` line cited; 16: none of the 13 is an orphan, by the `--diff-filter=A` block; 17: the sixteen rows handed to #645) and names the other findings with their carriers so none is taken here.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `fixture`, `fix-tree` or `fix-pending-image`; ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c '^PROOF:' 00-running-log.md``.
- [ ] Every punch item carries `question:`; every `bug` this lane files passes `tools/box-check --issue N`; no file under `packages/` is changed on this branch before a stream brief (`git diff --stat 8ebaf8daad <fixed-at> -- packages` shows only stage-E commits), and no `PKG_VERSION` line changes on this branch at all (`git diff 8ebaf8daad <fixed-at> -- packages | grep -c '^[-+]PKG_VERSION='` prints 0).
- [ ] No upstream-carried file is deleted or renamed on this branch (`git diff --diff-filter=DR --name-only 8ebaf8daad <fixed-at> -- packages` is empty).
- [ ] The retro exists at `docs/retros/<date>-m6-generic-packages-reached.md`, is posted on #654, and says in those words that the slice did nothing to the two time-to-play numbers.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge, and `tools/lint-audit-artifacts` prints `PASS` on the folder; the six exit codes pasted on #654.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #654; a blocker named on #654 with what is needed (an API budget that
does not recover, a count that cannot be produced, two commands that
disagree); a branch that differs from `8ebaf8daad` on one of the 266 at
stage A in a hunk the dispatch comment did not name; or an execution limit,
stated as such with the running log current. A checkpoint is not a stop; a
differing count is a delta; `next` moving is drift. An idle session says it
is idle on #654, **and does not end a turn on a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#654`, its time from `date -u` in
  the same command; `tools/work-log-index --write` after it.
- A friction line the moment something slows, with `issue: #654` or the
  guard.
- The VM question written before any proof (§ 5: no; the tree, the record
  and the release sources are the bench).
- The mini-retro at stage G, posted on #654, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator (D-WORKFLOW-189).
- A register row the same session for any decision the slice forces; the
  next Decided ID is checked on every pushed branch at the time (on
  2026-10-24 the highest Decided row is D-WORKFLOW-194, the coordinator's;
  T30 runs beside this lane and may take 195); it goes at the end of `##
  Decided`.
- `tools/ceremony-check` before every push; what another lane owes (the
  W42 summary, M7's) is noted, not paid. Never `--no-verify`. A merge with
  conflicts is checked for markers (#696); the ledgers are united by whole
  entries. **A commit names its paths** (`git add -- <files>`, `git status
  --short` read before each commit as well as after); **a tree export goes
  under `/workspace/tmp/m6-t7/` after `df -i`, never under `/tmp`**.
- Commit messages `docs: ...` for the audit and `<package>: ...` for a
  recipe change under a stream brief, with `Refs #654`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#654's checkboxes against their artifacts; the lint's `PASS` line with the
`D-WORKFLOW-184` line beside it; `review-plan.json`; the audit issue's
checkboxes all at an outcome; the coverage table's row count (266) and the
currency table's (243); no `current` beside a `not read`; the sixteen #645
rows; **re-running on an export of the tip under `/workspace/tmp`: the
membership block, the (a) loop and the `pkgcheck` baseline in full, and the
(b) loop and the HEAD probe on twenty rows drawn with `shuf --random-source=<(yes
t7)` (the seed recorded), which must agree with the lane's rows** (A9);
`register-check` on a simulated merge with the coordinator's tip; the
retro's four answers; the six exit codes. The lane posts one hand-back
comment naming the tip and each artifact by path, writes `reviewed-at:`
and `fixed-at:` into #654's body, then says it is idle. After acceptance
the coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the full lint, writes the hashes into
`slices.json`, merges the branch in its turn after the M7 candidate (after
T6's, before T4's), regenerates the ledgers, posts the sixteen rows on #645
and the upstream-carried defects' proposals on #585 in the shape the lane
wrote, files the Backlog bump issues, and closes #654 when every row is
proven. A brief that needed the coordinator's help mid-slice beyond the
stage-D pause is a defect in this brief: log the friction; the coordinator
fixes the template.

**The readings before dispatch** (plan § 3, principle 3): the epic's futro
(#848, `docs/futros/2026-10-24-m6-generic-packages.md`) was written with
this version, and a stranger's proof of this brief is run by a reader with
no context before dispatch; version 2 records what each found.
