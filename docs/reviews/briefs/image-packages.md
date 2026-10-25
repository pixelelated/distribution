# Brief: M6.P2 T8, the image's own packages (#655)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #655 differ, #655 wins and the
coordinator corrects the brief in the same session. **Version 1
(2026-10-24):** written after T7 (#654) was accepted the same morning, so
its method and its errata are built in -- the three-source table with the
mover named per row, the probe without `-L`, the mirror as the fetch's
second line, the per-plan expansion of every field the build reads, the
record's names checked against `-<digit>`, prose through a quoted heredoc
-- and every figure below was produced by a command at `8ebaf8daad` (the
tree) or in the inventory at P1's `2174265e9c` unless it says *branch*. It
went through a stranger's proof before dispatch. **Version 2 (2026-10-24):**
the proof reproduced 98 claims -- 76 right, 9 wrong, 8 partial, 5 uncheckable
(`/workspace/tmp/m6-coordinator/stranger-t8/report.md`); every wrong and
partial claim is corrected below. Its chief corrections: **fourteen of the
485 paths contain spaces**, so every loop reads the path lists with `while
IFS= read -r` (never `$(cat ...)`), and the (a) count is 87 modified, not
86; the record's unbuilt names are **the 12 virtual packages and `qcom-abl`**
-- the thirteen "real" ones have build directories whose version suffixes
begin with `v` or a letter, which a digit-stripping `sed` cannot see, so the
record is matched by name prefix; six of T7's seven overrides are here
(`libevdev` is the OS-scripts area's); `moonlight` makes nine hash pins in
`make update`'s set; `systemd-analyze` is on the host; the empty-checksum
grep is rewritten so it can match; the VM tool is
`projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm`. **Each command
block sets its own variables** (`D`): a Bash call in
this harness starts a fresh shell. **This is a currency slice at
Independent depth, the renovation's first**: it reads the recipes as code
(the 45 shell scripts, 30 systemd units and 65 configs in the set are code
too), it tables every pin against its movers, one GPT-6 Astra seat reviews
it through the Facilitator, and **it moves no pin, deletes nothing upstream
carries or has deleted, and runs no bump tool** (`make update`,
`scripts/update_packages`, `tools/update-pkg`: read, never run).

## 1. Identity

- **Issue:** #655 `M6.P2 E848/T8: generic-packages: the image's own
  packages (projects/ROCKNIX)`, slice `image-packages` (`k: 8`) in
  `docs/reviews/slices.json`, eighth in `docs/reviews/order.md` (its § T8
  paths line: *"485 paths, 20,644 lines, 13,145 read, of which 2,179
  fork-own; 0 patch and config lines; reach n/a 1, shipped 478, test 6"*;
  its `why`: *"the ROCKNIX recipes the image installs: apps, tools, virtual
  packages (the emulator list), graphics, audio, network; package currency,
  with the build engine under D-WORKFLOW-186 ..."*). **Epic:** #848 (the
  generic packages: T7 #654 accepted 2026-10-24, this slice, T23 #670
  after), whose futro (`docs/futros/2026-10-24-m6-generic-packages.md`)
  carries a T8 kickoff addendum (A1 to A8 are written into this version).
  **Milestone:** M6; its body holds the live order; read it first.
  **Predecessors:** #346, #641, #644 (findings **15** -- `make update`'s set
  and the fact that it has never run, this slice's half -- and **16** -- the
  22 orphans the freshness tool counts as the fork's, 11 of them in this
  set), **T7 #654** (accepted: `docs/audits/2026_10_24-epic-m6-generic-packages-reached/`
  on `feature/m6-generic-packages-reached-654` at `db6597356b` is the
  nearest reading -- its `04` § Q4 names the seven overrides of this slice
  that change what the build fetches, its `q4-table.md` is the table's
  shape, its `00` § Incident is why prose goes through a quoted heredoc),
  **T6 #653** (its late-binding lead on #655: `virtual/image:109,110`, now
  **#852**, this slice's to fix; `systemd:105`, #851, is the OS-scripts
  area's), **T5 #652** (the fetch; D-WORKFLOW-193/194/196), **T3 #650** and
  **T30 #677** (the emulators metapackage and the standalone recipes, both
  excluded from this set by the area and the slice globs). **Beside it:**
  T30 runs its streams in the other lane (D-WORKFLOW-190); the two share no
  path.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, post on #585 or #645, or decide a question of scope: those are the
  coordinator's, reached through #655, one question at a time. What it does
  file: its own audit punch-list issue (stage D) and a `bug` issue for every
  defect it finds (D-WORKFLOW-187). Nothing else.
- **One worktree, one session.** Branch `feature/m6-image-packages-655` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-image-packages-655`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's
  pointer seeded (the two hashes are in the dispatch comment on #655).
  **Before that comment exists there is no worktree at that path and none
  of the first commands can run.** The session is the T5 lane's
  (`m6-t5-build-engine`, pane `wN:p7`), which ran T5, T6 and T7; those
  worktrees stay beside this one, idle, until their merges, and nothing is
  written there. The primary checkout `/workspace/repos/pixelelated/distribution`
  stays on `next` (D-INFRA-025); the legacy checkout and
  `rocknix.worktrees/*` are the M7 lane's, read only, never a process
  started there (their five build roots' `build/` directories are listed,
  nothing more); every other lane's worktree is `git -C` only. **The rules
  in this worktree are `next`'s except the paths the dispatch comment
  lists** (eight on 2026-10-24: P1's `fork-workflow.md` and `instruction-files.md`;
  the coordinator's `generic-x64-vm-testing.md`, `engineering-practices.md`
  and `device-builds.md`; M7's `.claude/skills/council/IMPORTED-FROM.md`;
  `tools/lint-audit-artifacts` with the code-auditor `templates.md`). Known
  stale facts in the rules (the legacy layout, #640) do not cost an hour
  here: every rule the work touches is named in § 3.
- **Model and effort:** Opus 5.5 (the maintainer, 2026-10-22: *"the work
  will be Opus 5.5"*) at high effort. Record what ran in `00-running-log.md`'s
  header.
- **Review depth: Independent** (D-WORKFLOW-184: *Independent (the executor
  plus one GPT-6 Astra review through the Facilitator) for an ordinary
  code slice*; `slices.json` k 8 `depth_reason`: *an ordinary code slice*;
  the code-auditor's `review-levels.md`: *primary plus one external reviewer
  from another lab; Phase 4.6 remains required*). **One seat, GPT-6 Astra at
  `max`** through the Facilitator (`tools/council/run invoke --member gpt
  --provider openrouter`; `npm install --prefix tools/council`, `verify-pins`
  and `test` first; the key is `~/.config/council/env`, sourced by `run`,
  never read into a transcript): a probe first (identity, effort and
  provider read from the provider's own field), then one refutation pass
  over one bounded packet (§ 5), the provenance file beside each output, as
  T3's and T30's `second-opinions/` did with two seats. **A failed seat is a
  hold** (the coordinator's rule on #650: record, diagnose, one same-slug
  retry on a transient cause, then post; a ceiling cut is D-WORKFLOW-195's
  trimmed packet, the coordinator's call); never a Local fallback, never a
  second lab added. `second-opinions/review-plan.json`: `depth`
  `independent`, `scope` `epic`, primary `anthropic/claude-opus-5-5` /
  `anthropic` with its `identity_source`, `reviewers` one entry (`member`
  `gpt`, `model` `openai/gpt-6-astra`, `lab` `openai`, `effort` `max`,
  `provider` the pinned OpenAI route, `calls` the refutation, `probes` the
  probe, `status`), as T30's file is shaped. The dispatch comment
  authorizes the two calls (the probe and the refutation).

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-image-packages-655
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-image-packages-655
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: this is not the lane's worktree (stacked on P1): stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists, nothing else
mkdir -p .qa-scratch/t8/at-hash && git archive 8ebaf8daad projects/ROCKNIX/packages | tar -x -C .qa-scratch/t8/at-hash   # the read tree: 485 of its files are the slice's; small enough for .qa-scratch
ls tools/renovation-inventory tools/renovation-status tools/renovation-drift docs/reviews/slices.json   # P1's
"$D/tools/rules-check"; echo "rc=$?"; "$D/tools/register-check"; echo "rc=$?"; "$D/tools/ceremony-check"; echo "rc=$?"   # rc 1 on 2026-10-24: W42 OVERDUE (M7's week), not this lane's to pay
git push -u origin feature/m6-image-packages-655
test -f docs/reviews/briefs/image-packages.md || { echo "the brief is not in this tree: stop"; exit 1; }
cat .github/sessions/saved-session-state-feature-m6-image-packages-655.md
tail -3 /tmp/m7-m6-host-coordination-20261023.txt                   # the host's state: a guest cycle needs M6 to hold the host; read before any boot
df -i /tmp | tail -1                                                 # never export a tree under /tmp
gh api rate_limit --jq '.resources.core | "\(.remaining)/\(.limit)"'    # the API budget § 5 spends; below 1,500 the loops wait
test -f ~/.config/council/env && echo "council env present (never read into a transcript)"
```

## 2. Scope

**485 paths, 20,644 lines; 450 upstream-carried and 35 fork-own; reach
`shipped` 478, `test` 6, `n/a` 1; 260 recipes (`package.mk`) and 225 other
files (65 config, 45 shell, 38 image, 30 systemd, 11 other, 8 none, 7 make,
5 c++, 5 json, 4 text, 2 symlink, 2 udev, 1 script, 1 python, 1 xml).** The
membership is the inventory's at P1's `2174265e9c`, with the slice's rule
(`k: 8`): the rows of the `generic-packages` area under
`projects/ROCKNIX/**` less `projects/ROCKNIX/packages/virtual/emulators/**`
whose reach is `shipped`, `test` or `n/a`. **The area filter is what keeps
the fork's own subsystems out**: `areas.json` excludes
`projects/ROCKNIX/packages/{rocknix,sysutils,hardware,emulators,ui,linux,linux-drivers,linux-firmware,kernel-drivers}/**`
and `network/{rclone,cloud-signin-window,raofflineproxy,raofflineproxy-libchdr,raofflineproxy-rcheevos}/**`,
every `.patch` and every `linux*.conf`; the slice glob removes the
emulators metapackage (T3's and T30's). So `systemd`'s override (#851) is
not here, nor `rocknix`, nor a cloud or proxy package, however much one
looks like an image package. The one `n/a` row is
`projects/ROCKNIX/packages/initramfs/config/initramfs.x86_64.conf`. The
re-derivation:

```bash
python3 -I - <<'PY'
import json, re, collections, os
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
def gm(p, g): return re.fullmatch(re.escape(g).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*"), p) is not None
t8 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "generic-packages"
      and gm(r["path"], "projects/ROCKNIX/**") and not gm(r["path"], "projects/ROCKNIX/packages/virtual/emulators/**")
      and r["reach"] in ("shipped", "test", "n/a")]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t8), "lines", L(t8), dict(collections.Counter(r["tier"] for r in t8)), dict(collections.Counter(r["reach"] for r in t8)))
print(dict(collections.Counter(r["language"] for r in t8)))
pk = [r for r in t8 if r["path"].endswith("/package.mk")]
print("recipes", len(pk), "fork-own recipes", sum(1 for r in pk if r["tier"] == "fork-own"), "groups", dict(collections.Counter("/".join(r["path"].split("/")[2:4]) for r in pk)))
print("with patches", sum(1 for r in pk if r["patches"]))
os.makedirs(".qa-scratch/t8", exist_ok=True)
open(".qa-scratch/t8/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t8, key=lambda r: r["path"])))      # the 485, read by every later command
open(".qa-scratch/t8/recipes.txt", "w").write("".join(r["path"] + "\n" for r in sorted(pk, key=lambda r: r["path"])))    # the 260
for r in sorted(t8, key=lambda r: r["path"]): print(r["reach"], r["tier"], r["lines"], r["path"])
PY
wc -l .qa-scratch/t8/paths.txt .qa-scratch/t8/recipes.txt                                                                   # 485, 260
grep -c ' ' .qa-scratch/t8/paths.txt                                                                                         # 14: paths with spaces -- every loop below reads the list with `while IFS= read -r`, never `$(cat ...)`
```

Recorded (2026-10-24, at `2174265e9c`'s inventory, the tree at
`8ebaf8daad`): **485 paths, 20,644 lines**; tiers upstream-carried 450,
fork-own 35; reach `shipped` 478, `test` 6, `n/a` 1; **260 recipes** in
twenty-two groups (graphics 38, apps 29, devel 28, tools 26, x11 23, audio
19, network 18, multimedia 14, wayland 14, virtual 12, compress 8, textproc
7, lang 6, compat 5, fonts 3, security 3, rust 2, debug 1, misc 1, print 1,
python 1, web 1); **60 recipes carry patches** (T42's and T43's rows: a
patch is read here only to say what a bump would re-cut); **50 recipes
source a generic recipe** (`. ${ROOT}/packages/.../package.mk` or
`get_pkg_directory`) and so inherit its pin unless they override it.

**Provenance, by git and not by a tool's set.** Against the base
`c445081a59` and against `upstream/next` (`e0f9deb899`):

```bash
P=.qa-scratch/t8/paths.txt; R=.qa-scratch/t8/recipes.txt   # written by the block above; read with xargs -0 or while read -r: 14 paths carry spaces
tr '\n' '\0' < $P | xargs -0 git diff --name-status c445081a59 8ebaf8daad -- | awk '{print $1}' | sort | uniq -c            # 11 A, 24 M: the fork's 35 changes (27 recipes: 8 added, 19 edited; 8 other files)
tr '\n' '\0' < $P | xargs -0 git diff --name-status upstream/next 8ebaf8daad -- | awk '{print $1}' | sort | uniq -c        # 31 A (present here, absent upstream), 87 M (one of them `misc/modules/sources/Mount NFS.sh`, a path with a space)
tr '\n' '\0' < $P | xargs -0 git diff --name-status upstream/next 8ebaf8daad -- | awk -F'\t' '$1=="A"{print $2}' | grep package.mk | while IFS= read -r p; do git cat-file -e c445081a59:"$p" 2>/dev/null && echo "orphan $p" || echo "fork-added $p"; done | awk '{print $1}' | sort | uniq -c   # 11 orphan, 7 fork-added
tr '\n' '\0' < $P | xargs -0 git log --oneline c445081a59..upstream/next -- | wc -l                                         # 40 upstream commits on these paths since the base
tr '\n' '\0' < $P | xargs -0 git diff --name-only c445081a59 upstream/next -- | grep -c package.mk                          # 66 recipes upstream changed since the base
FRESHNESS_HEAD=8ebaf8daad FRESHNESS_BASE=upstream/next tools/fork-package-freshness --list | tr ' ' '\n' | grep -c '^projects/'   # 34: 11 fork-added, 22 orphans, 1 present upstream (its set is a diff, not a provenance: #644 finding 16); 7 of the 11 and 11 of the 22 are in this set, the rest are the cloud and proxy packages' and other areas'
```

Recorded: **the fork's 35 changes** are 27 recipes (**8 added:**
`gamescope-glm`, `gamescope-stb`, `mangohud-vulkan-headers`,
`mangohud-vulkan-utility-libraries`, `harfbuzz-icu`, `gst-plugins-bad`,
`gstreamer/gstreamer`, `gnutls`; **19 edited:** `gamescope`, `mangohud`,
`box86`, `lib32`, `cairo`, `glslang`, `spirv-tools`, `gcc`,
`gst-plugins-base`, `libplacebo`, `opusfile`, `avahi`, `enet`, `tailscale`,
`zerotier-one`, `rocknix-abl`, `rocknix-splash`, `virtual/network`, `sway`)
and 8 other files (added: `apps/m8c/config/GENERIC_X64/config.ini`,
`initramfs/config/initramfs.x86_64.conf`, `wayland/compositor/sway/scripts/sway-ready`;
edited: `misc/modules/sources/gamelist.xml`,
`network/avahi/system.d/avahi-daemon.service`,
`network/networkmanager/config/NetworkManager.conf`,
`tools/installer/scripts/installer`, `wayland/compositor/sway/autostart/111-sway-init`).
**Against `upstream/next`, 18 recipes present here are absent there**: the
**11 orphans** upstream deleted since the base (`libfreeaptx`, `opus`,
`libfmt`, `glslang`, `vulkan-headers`, `cargo`, `miniupnpc`, `rocknix-abl`,
`tllist`, `mtdev`, `swaybg`; #644 finding 16's class, half of the tool's 22)
and the 7 fork-added (`gstreamer/gstreamer` was **added on both sides**
since the base: a merge to pre-read, not an orphan and not fork-only).
**Upstream changed 66 of the 260 recipes since the base** (40 commits), so
tier (a) is live here where T7's was empty, and **the fork-edited recipes
upstream also changed are the base merge's conflicts**: the slice names
them (U-1 of the futro's addendum) before stage C.

**The pins at the hash** (top-level lines, comments stripped): 169 version
strings, 41 commit hashes, 50 recipes with no top-level `PKG_VERSION` -- 42
that source a generic recipe and inherit its pin, 3 that set it in a `case`
branch per device (`moonlight`, `sway`, `wlroots`), 5 virtual packages with
none. The 50 that source a generic recipe are a different fifty from these:
8 of them set their own pin after sourcing (the override shape). By
`PKG_URL`'s host, a coarse first count the lane replaces with the per-plan
expansion below: github.com 39, freedesktop.org 16 (gitlab.freedesktop.org
counted under gitlab, 6), gnu.org 5, sourceforge 4, kernel.org 3, no
top-level `PKG_URL` 50 (the sourcing and `case`-branch recipes), the rest
`other` (17 of them `PKG_URL=""`, the virtual packages). **The effective pin is
the override's**, read per plan through `config/options` (`device-builds.md`
§ After rebasing item 3, widened 2026-10-24 to every field the build
reads): six of T7's seven -- `opus` 1.5.2 (the generic 1.6.1), `gcc` 15.2.0
(16.2.0), `libfmt` 9.1.0 on every plan but the SM/AMD64 ones (12.2.0;
#877, fixed in a packet, read only here), `wavpack` and `zlib` with their
own URLs, `libfreeaptx` with its own checksum -- are this slice's rows
(`libevdev`'s override is `sysutils/`, the OS-scripts area's), and the 50
sourcing recipes are read for the same shape.
**Checksums:** every archive recipe is expected to carry `PKG_SHA256`; the
per-shape count (a top-level line or a `case` branch, and **an empty
assignment counts as missing**, D-WORKFLOW-196) is run over the 260 before
any row is written; T5's five archive versions (D-WORKFLOW-194) sit in four recipes, two
of them in this set: **`tools/atf` and `wayland/compositor/sway`** lack a
checksum at `8ebaf8daad` and gained theirs on T5's branch (`52e6794ba7`,
E6), not merged here yet; `rkbin`'s override is unreached (T23's) and
`libmali-vulkan` is `unshipped` (T23's too). So the per-shape count here
expects **exactly those two** and re-files neither; a third is the lead.

**Three movers, and what each moves (A1).**

| Mover | What it moves | Read how |
| --- | --- | --- |
| (a) the base merge (ROCKNIX) | the 450 upstream-carried paths; 66 recipes changed upstream since the base, 11 deleted (the orphans) | `git diff --quiet upstream/next 8ebaf8daad -- <path>` per path; the fork-edited ∩ upstream-changed set is the merge's conflicts, named per recipe with the hunks that collide |
| `make update` (`scripts/update_packages`) | the dependencies of the `emulators`, `es-themes` and `gamesupport` virtual packages, each to its repository's branch head, less `config/blocklist` (29 lines): 171 names for RK3588 (the Makefile's device; 147, 162 and 185 for the three shipped plans), **13 of this slice's recipes** among them, 9 hash-pinned (`box64`, `box86`, `gamecontrollerdb`, `jstest-sdl`, `rocknix-hotkey`, `sdljoytest`, `sdltouchtest`, `sixaxis`, and `moonlight` through its per-device `case` branch); `control-gen` and `portmaster` are blocklisted; it has **never run on the fork** (#644 finding 15) | the three virtual packages' `PKG_DEPENDS_TARGET` through `config/options` for RK3588 and for the three shipped plans; `config/blocklist` read; **`scripts/update_packages` read, never run** (T7's incident: it rewrote a recipe) |
| (c) the project | the 27 fork-own recipes (D-WORKFLOW-024: the fork keeps what it introduces current; `tools/fork-package-freshness`'s 11 `projects/` fork-added entries are a subset) and, informationally, the 11 orphans (frozen here while upstream dropped them) and the 41 hash pins | the freshness tool's handlers for the fork-own recipes; the API `compare` for GitHub hash pins; UNKNOWN stays UNKNOWN |

There is no LibreELEC column: these are ROCKNIX's own recipes.

**The record agrees with `shipped` (A5).** The five M7 build roots, read
only (`ls <root>/build`): a build directory is named `<name>-<version>`, and
**the version can begin with `v` or a letter** (`ecm-v6.16.0`,
`armsx2-turnip-axfl1-011`, `glfw-e2c9264`, `inih-r62`), so a digit-stripping
`sed` misreads the listing -- version 1 of this brief did, and called
thirteen built recipes unbuilt. **Match by name prefix instead**: a recipe
`<name>` is built in a root when the listing has an entry `<name>-...` and
no other recipe's name is a prefix of it (`arm` against `armsx2-turnip`:
check both ways). So read: **247 of the 260 names have a build directory in
at least one root; the 13 without are the 12 virtual packages** (`arm`,
`debug`, `es-themes`, `gamesupport`, `image`, `initramfs`, `libc`,
`linux-drivers`, `linux-firmware`, `network`, `swaywm-env`, `synctools`)
**and `qcom-abl`** (no URL of its own, a Qualcomm bootloader piece: read
whether a shipped plan builds it or a device condition holds it back, per
plan through `config/options`). `btrfs-progs`'s shape (#879) is the model
for a name the plan lists and `PKG_ARCH` excludes; none of the 260 showed
it in the first read.

```bash
ROOTS=/workspace/repos/rocknix.worktrees
for d in $ROOTS/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64 $ROOTS/m7-signin-h700-build-20261023-06/build.pixelelated-H700.aarch64 $ROOTS/m7-signin-h700-build-20261023-06/build.pixelelated-H700.arm $ROOTS/m7-signin-sm8550-build-20261023-03/build.pixelelated-SM8550.aarch64 $ROOTS/m7-signin-sm8550-build-20261023-03/build.pixelelated-SM8550.arm; do
  LC_ALL=C ls "$d/build" > ".qa-scratch/t8/listing-$(basename $d).txt"; done   # read only; never a process in those trees; the raw listing, not a stripped one
while IFS= read -r p; do n=$(basename "$(dirname "$p")"); hit=0; for l in .qa-scratch/t8/listing-*.txt; do grep -q -E "^${n}-[A-Za-z0-9]" "$l" && hit=1; done; echo "$hit $n"; done < .qa-scratch/t8/recipes.txt | sort | uniq -c | awk '{print $1, $2}' | sort | uniq -c   # 247 with 1, 13 with 0 on 2026-10-24
for dev in GENERIC_X64:x86_64 H700:aarch64 SM8550:aarch64; do PROJECT=ROCKNIX DEVICE=${dev%%:*} ARCH=${dev##*:} bash -c '. config/options qcom-abl >/dev/null 2>&1; printf "qcom-abl %s arch=%s version=%s url=%s\n" "$1" "${PKG_ARCH:-any}" "${PKG_VERSION:-none}" "${PKG_URL:-none}"' _ "${dev%%:*}"; done
```

**The hash.** The slice's bytes are `8ebaf8daad`'s; `reviewed-at:` is the
branch `HEAD` at stage A; the read is made on the at-hash tree
(`.qa-scratch/t8/at-hash/`). The branch differs from the hash on none of
the 485 on 2026-10-24 (P1 and the coordinator changed nothing under
`projects/ROCKNIX/packages/`), and the check is made over the slice's own
paths: `git diff --stat 8ebaf8daad HEAD -- $(cat .qa-scratch/t8/paths.txt)`
is empty; a non-empty result there is the first lead.

**The policy on change (plan § 5; D-WORKFLOW-187):** **no pin moves, no
upstream-carried file is deleted, no orphan is deleted** (the base merge
deletes them: each orphan's row says what the fork used it for and names
any fork-own dependant, which is the finding if there is one), **no bump
tool runs**. A fork-own recipe found BEHIND is a row whose disposition is a
Backlog issue in #839's shape (the coordinator files it). An
upstream-carried recipe behind `upstream/next` is dispositioned `follows
the base merge` with the hunk named; one the fork also edited is
`conflict at the base merge: <the hunks>`, the pre-read the next
candidate's step 0 will thank. A defect in a fork-own file (a script, a
unit, a config, a recipe's shape) is a `bug` with the code-trace shape,
`Already written:` and the VM line, and its fix lands under a stream brief
at stage E with the GENERIC_X64 guest as the bench where behaviour is
claimed; a defect in an upstream-carried file is a `bug` whose contained
fix is ours to make (`bugs-are-agent-first.md` rule 6) and a #585 candidate.
**#852 (`virtual/image`'s load-time symlink) is this slice's first stream
candidate**; **#877 (`libfmt`) is read, not touched** (the packet
`fix/m6-877-libfmt-sha256` carries the fix).

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
  artifact; § A name is not a behaviour with its bullet on counts, line
  numbers and hashes; § Check upstream early, D-WORKFLOW-162; § Consider
  contributing every applicable fix upstream, D-WORKFLOW-164/165; § Guards
  must fail closed; § Before deleting a duplicate -- for every orphan row:
  what the fork's copy did that upstream's deletion drops),
  `packaging-and-patches.md`, `device-builds.md` (§ After rebasing item 3
  with its 2026-10-24 paragraph: every field the build reads, per plan,
  through `config/options`; § A metadata-only upstream change still
  rebuilds everything), `fork-workflow.md` (§ When to merge up;
  `tools/fork-package-freshness`), `release-candidates.md` (step 0: where
  the base merge lands), `upgrade-and-install.md` (`Already written:` for
  every disposition and bug; a config or a unit the fork edited is read for
  what an upgraded device already has), `bugs-are-agent-first.md`,
  `issue-tracking.md`, `vm-first.md` (§ 5: yes, for behaviour claims),
  `generic-x64-vm-testing.md` (§ headless, `tools/vm-serial`, the census
  and pidfile discipline), `worktrees.md` (the layout, superseded by § 1).
- The code-auditor skill whole (`SKILL.md`, `references/phases.md`,
  `review-levels.md` -- Independent: one external reviewer, Phase 4.6
  required -- `templates.md` for the `review-plan.json` shape,
  `anti-patterns.md`); the renovation face is plan § 6b.
- **T7's audit** (`docs/audits/2026_10_24-epic-m6-generic-packages-reached/`
  at `db6597356b`, read with `git -C` or `git show`): `02-forward-audit.md`
  § Mechanical checks and § The fetch sweep (the loops this slice re-uses:
  the probe without `-L`, the streamed fetch on a redirect, the cache
  stamps, the mirror as the second line), `04-analysis.md` § Q4 (the seven
  overrides) and § Q6/Q7, `q4-table.md` (the table's shape),
  `00-running-log.md` § Incident, `01` § Brief erratum, and its retro's
  adjustments (now plan § 6b E bullets). **T6's audit** at `37d1d98aed`:
  `02-forward-audit.md` § Leads from the sweeps (`virtual/image:109,110`,
  #852) and the widened `tools/pkgcheck` at `44f64842b6` (run from this
  worktree over the 260, as T7 did). **T5's audit** at `52e6794ba7`: E6's
  checksum rows and D-WORKFLOW-193/194/196. **T30's** `second-opinions/`
  (the GPT seat's brief, probe and provenance files, and D-WORKFLOW-195's
  trimmed packet) as the model for Phase 4.6 with one seat.
- **`docs/reviews/build-path-read.md`** (#644): findings 15 and 16 whole
  with § 6's recommendations (*For the maintainer*); the others named with
  their carriers so none is taken here. **#645** (the move table: the
  sixteen `packages/` recipes T7 proposed moving *into* this slice's tree;
  nothing moves in this slice, but a row here may say what a moved recipe
  would shadow).
- `docs/blindspot-register.md` whole once (76 entries under the numbers 1
  to 75; 29 is used twice, #811), then **13**, **22**, **46**, **51**, **75**.
- Decisions by ID: D-WORKFLOW-184 (Independent for an ordinary code slice),
  D-WORKFLOW-186, D-WORKFLOW-187 (no release gate; every defect a bug; the
  no-bump rule is this brief's § 2 and plan § 5 -- the open row
  D-WORKFLOW-191 says *M6 builds nothing* in those words), D-WORKFLOW-164/165, D-WORKFLOW-162, D-WORKFLOW-024,
  D-WORKFLOW-193/194/196 (the fetch fails without a checksum; the count per
  shape; an empty assignment is missing), D-WORKFLOW-195 (a seat cut by its
  ceiling: the coordinator's call), D-UI-079, D-INFRA-022, D-INFRA-025/026,
  D-WORKFLOW-137 (the auditor is not the council), D-WORKFLOW-049 (every
  audit seat through the Facilitator on OpenRouter).
- Issues: #655 (this), #848, #654 (T7, accepted), #670 (T23: the generic
  copies the overrides shadow are its rows), #644/#645, #852 (this slice's
  bug, from T6), #877 and #879 (read), #841/#849/#880 to #883 (the dead-URL
  class and the mirror), #844 (the fetch check), #839/#878/#885 (the bump
  issues' shape), #585, #657, #810, #809, #576 (webkitgtk, T7's). Every `gh`
  call carries `--repo pixelelated/distribution`.
- Tools, read whole before run: `tools/fork-package-freshness`,
  `tools/pkgcheck`, `tools/viewplan`; **read, never run:**
  `scripts/update_packages`, `tools/update-pkg`, `tools/update-scan`.

## 4. The questions

All seven apply (plan § 4); for a currency slice at Independent depth Q4 is
the spine and Q2, Q3 and Q6 are read in full over the 485 (the 45 shell
scripts, 30 units and 65 configs are code), Q1, Q5 and Q7 as rows.

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | A recipe pinned to a retired series or host; a unit or config using a retired directive; the 11 orphans (upstream moved on: what replaced each) | the rows; the orphan table with upstream's replacing commit named |
| Q2 Standards | `tools/pkgcheck` over the 260 (the tree's copy, then T6's widened copy from this worktree; the baseline counts first); late binding in the 50 sourcing recipes (an override that reads a variable before the load); `bash -n` over every shell file (by shebang); `systemd-analyze verify` over a copy of each unit (`/usr/bin/systemd-analyze` is on the host; a dependency it cannot resolve there is a note), and each unit read against `systemd.unit(5)`'s shape | the two `pkgcheck` runs' counts and FAIL list; `bash -n` ok count; a FAIL on an upstream-carried file is `Renovation` with a #585 candidate unless a build or a boot would meet it |
| Q3 Bugs | A recipe that fails a build from an empty cache (the probe + the mirror + the cache stamps, T7's loops over the 260's archive recipes); an empty or missing checksum per shape; a script that writes where it should not, runs text as a command, or tests the wrong thing (T30's classes: `eval`, `echo | xargs`, redirection-as-comparison, delete-before-link); a unit whose `ExecStart` names a path the image lacks (read against the GENERIC_X64 install tree, `ls` only); #852's class (a write at load time) in any recipe | one `bug` per defect in the code-trace shape; the VM line *Yes* where a stream will prove it on the guest |
| Q4 Currency | **The table**: one row per recipe (260) with the effective pin per plan (GENERIC_X64, H700, SM8550), its shape, (a) `upstream/next` (`identical` / `differs` with the hunk / `absent-upstream: orphan` / `absent-upstream: fork-added`), the `make update` column (in its set or not, blocklisted or not), (c) the project for the 27 fork-own (the freshness tool's six classes) and for the 11 orphans (what upstream replaced them with), the `compare` distance for GitHub hash pins, and a disposition naming the mover: `current`; `follows the base merge: <hunk>`; `conflict at the base merge: <hunks>`; `orphan: dropped by the base merge; the fork used it for <x>; dependants <none|name>`; `fork's: Backlog bump proposed`; `make update's: moves to <head> if run`; `pinned on purpose`; `unknown: <why>` | § 5's loops; a row never reads `current` on a source whose cell is `not read`; the conflict set named as a list the coordinator reads at integration |
| Q5 Efficiency | What the fork-own recipes ask of a build (`gcc`'s hold at 15.2.0 and why; `box86`/`lib32`'s 32-bit chain; `gstreamer`'s plugins) -- read, not measured; the installer script's and `111-sway-init`'s cost on the boot path, read | reading only; `not measured` where a number would need a build or a boot |
| Q6 Dead ends | The 13 unbuilt names settled per plan (12 virtual by construction; `qcom-abl`'s plan or condition read); the 11 orphans' dependants; a unit no target pulls in; a config no script reads | the per-plan expansion outputs; `git grep` for each orphan's name over `projects/ROCKNIX` and `packages`; `grep -rn` of each unit's name over the install tree's `wants/` (read only) |
| Q7 Clarity | A fork edit that duplicates upstream's later fix (the fork-edited ∩ upstream-changed set read hunk by hunk: `same change, drop ours at the merge` / `different, keep ours` / `conflict`); an override that could be a smaller one; the 8 other fork-own files (a unit, two configs, a script, an autostart, a gamelist) each with what the fork changed and why, from `git log` | one row per fork-edited recipe and per other file, with the merge disposition |

A finding is one question with its evidence; `Renovation` is the category
for Q1, Q5, Q6 and Q7 items that are not defects. A Q3 finding is a `bug`
(D-WORKFLOW-187).

**The ladder (`working-principles.md` § Enforcement depth):** #844 (the
fetch check, mirror first, per plan) is this slice's guard too; a second
guard the slice may propose (an issue the coordinator files) is a
pre-merge read of the fork-edited ∩ upstream-changed set, run by
`rc-preflight`'s step-0 base check -- the conflict list this slice writes
by hand is what it would print.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor):

1. Tracker state is never sole evidence: every verdict cites the tree
   (`git grep`, `git log`, `git diff`), an API response saved to the
   scratch, a probe's status line, a fixture's run, a guest's frame or
   journal line, or a document's line.
2. Mechanical evidence outranks reading: a pin is a line in a recipe at a
   named hash expanded through `config/options` for a named plan.
3. **The target is the tree, the record, the release sources and the
   guest**: the at-hash recipes; `upstream/next`; the hosts the freshness
   tool reads; the mirror; the shared source cache's stamps and the five M7
   roots' `build/` listings and GENERIC_X64 install tree -- **read only,
   through the filter where a log or config is read, never a process
   started in an M7 worktree, never a file moved in the cache**; and the
   GENERIC_X64 guest for a behaviour a stream claims (a unit starts, a
   script's effect), under the host protocol (the host file read before
   every boot, census, pidfile, `tools/vm-stop`, content named before the
   boot, the T8 disk only).
4. An assertion that cannot fail is not evidence: the fork-own rows are
   the positive control for (a); the orphans for `absent-upstream`; a probe
   control on `portaudio`'s dead URL (#849) and on a live one.
5. Subagent output is a lead, never evidence; fan-out is read-only
   research only (D-WORKFLOW-183). **The GPT seat's output is a second
   opinion graded item by item against the artifact in `04` § Second
   opinion**, never a verdict on its own.

**What runs on the VM, and how.** Can this be done on the VM? **Yes, for
every behaviour claim; no guest is needed for the reading or the tables.**
A stream that changes a unit, a config, a script or `virtual/image`'s
install step proves it on the GENERIC_X64 guest (#852's fix: the image's
root still carries `/opt -> /storage/.opt`, read from the built image or
the guest). The host is M6's since 05:42; a new M7 block on the host file
ends a cycle at its next stop. Nothing here touches a handheld, a person's
cloud or a shared QA backend.

- **The host-side checks**, each run with its command, exit status and
  summary line in `02-forward-audit.md`; a check that cannot run is
  recorded as such, never as a pass:
  ```bash
  D=/workspace/repos/pixelelated/distribution.worktrees/m6-image-packages-655
  cd "$D"; mkdir -p .qa-scratch/t8/probe
  wc -l < .qa-scratch/t8/paths.txt; wc -l < .qa-scratch/t8/recipes.txt                                  # 485, 260
  tr '\n' '\0' < .qa-scratch/t8/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD -- | tail -1         # empty on 2026-10-24 (14 paths carry spaces: never $(cat ...))
  # (a) ROCKNIX, per path: identical / differs / absent-upstream, and the orphan-or-fork-added split; then the conflict set (11 paths on 2026-10-24: gamescope, cairo, glslang, spirv-tools, gcc, gst-plugins-base, gstreamer and rocknix-abl's recipes; gamelist.xml, NetworkManager.conf, 111-sway-init)
  while IFS= read -r p; do if git cat-file -e upstream/next:"$p" 2>/dev/null; then git diff --quiet upstream/next 8ebaf8daad -- "$p" && echo "identical $p" || echo "differs $p"; else git cat-file -e c445081a59:"$p" 2>/dev/null && echo "orphan $p" || echo "fork-added $p"; fi; done < .qa-scratch/t8/paths.txt > .qa-scratch/t8/q4a.txt; cut -d' ' -f1 .qa-scratch/t8/q4a.txt | sort | uniq -c   # 87 differs expected
  LC_ALL=C comm -12 <(tr '\n' '\0' < .qa-scratch/t8/paths.txt | xargs -0 git diff --name-only c445081a59 8ebaf8daad -- | LC_ALL=C sort) <(tr '\n' '\0' < .qa-scratch/t8/paths.txt | xargs -0 git diff --name-only c445081a59 upstream/next -- | LC_ALL=C sort) > .qa-scratch/t8/conflicts.txt; wc -l < .qa-scratch/t8/conflicts.txt   # 11: the base merge's conflict candidates, each read hunk by hunk
  # the effective fields per plan (every field the build reads), for every recipe; an empty or unset checksum beside a non-git URL is the lead
  for dev in GENERIC_X64:x86_64 H700:aarch64 SM8550:aarch64; do while IFS= read -r p; do n=$(basename "$(dirname "$p")"); PROJECT=ROCKNIX DEVICE=${dev%%:*} ARCH=${dev##*:} bash -c '. config/options "$1" >/dev/null 2>&1; printf "%s %s version=[%s] sha=[%s] shaset=%s arch=[%s] url=[%s]\n" "$2" "$1" "$PKG_VERSION" "$PKG_SHA256" "${PKG_SHA256+yes}" "${PKG_ARCH:-any}" "$PKG_URL"' _ "$n" "${dev%%:*}"; done < .qa-scratch/t8/recipes.txt; done > .qa-scratch/t8/effective.txt
  grep -E 'sha=\[\] ' .qa-scratch/t8/effective.txt | grep -E 'url=\[(https?|ftp)://' | grep -v -E 'url=\[[^]]*\.git\]|url=\[git' | sort -u   # on 2026-10-24: atf and sway (T5's E6 fixed them on 52e6794ba7, unmerged here; not re-filed) and nothing else
  # make update's set, for RK3588 and the three shipped plans
  for dev in RK3588:aarch64 GENERIC_X64:x86_64 H700:aarch64 SM8550:aarch64; do for v in emulators es-themes gamesupport; do PROJECT=ROCKNIX DEVICE=${dev%%:*} ARCH=${dev##*:} bash -c '. config/options "$1" >/dev/null 2>&1; echo $PKG_DEPENDS_TARGET' _ $v; done | tr ' ' '\n' | LC_ALL=C sort -u > ".qa-scratch/t8/update-set-${dev%%:*}.txt"; done; LC_ALL=C comm -12 <(sed 's#.*/\([^/]*\)/package.mk#\1#' .qa-scratch/t8/recipes.txt | LC_ALL=C sort -u) .qa-scratch/t8/update-set-RK3588.txt   # 13 on 2026-10-24 (171 names in the RK3588 set; 9 of the 13 hash-pinned, moonlight's in a case branch)
  git show 8ebaf8daad:config/blocklist | grep -v -E '^#|^$' | wc -l                                       # 29
  # (c) the freshness tool over the fork-own recipes it lists (read-only; network; UNKNOWN stays UNKNOWN); the GitHub hash pins by compare
  FRESHNESS_HEAD=8ebaf8daad FRESHNESS_BASE=upstream/next tools/fork-package-freshness $(FRESHNESS_HEAD=8ebaf8daad FRESHNESS_BASE=upstream/next tools/fork-package-freshness --list | tr ' ' '\n' | grep '^projects/' | xargs -n1 basename) | tee .qa-scratch/t8/q4c.txt; echo "rc=$?"
  gh api rate_limit --jq '.resources.core.remaining'                                                       # start the API loops above 1,500; serial, with a pause
  # the fetch sweep, T7's shape: HEAD without -L on the effective URL per plan (deduplicated), the mirror as the second line, a streamed fetch on a redirect only, the cache's stamps as the third witness
  awk '{print $NF}' .qa-scratch/t8/effective.txt | sed 's/^url=//' | grep -v '^none$' | sort -u > .qa-scratch/t8/urls.txt; wc -l < .qa-scratch/t8/urls.txt
  while read -r url; do printf '%s %s\n' "$(curl -sS -o /dev/null --head --max-time 30 -w '%{http_code} %{redirect_url}' "$url" 2>/dev/null)" "$url"; sleep 0.2; done < .qa-scratch/t8/urls.txt > .qa-scratch/t8/probe/head.txt; awk '{print $1}' .qa-scratch/t8/probe/head.txt | sort | uniq -c
  M=https://github.com/ROCKNIX/distribution-sources/releases/download/sources-v2   # distributions/ROCKNIX/options:186; the file name is PKG_SOURCE_NAME (config/functions:1350-1356)
  # pkgcheck, the tree's copy then T6's widened copy run from this worktree, over the 260
  for p in $(cat .qa-scratch/t8/recipes.txt); do tools/pkgcheck "$(basename "$(dirname "$p")")" >/dev/null 2>&1 && echo PASS || echo FAIL; done | sort | uniq -c
  git -C /workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-upstream-tools-653 show 44f64842b6:tools/pkgcheck > .qa-scratch/t8/pkgcheck-t6 && chmod +x .qa-scratch/t8/pkgcheck-t6
  for p in $(cat .qa-scratch/t8/recipes.txt); do .qa-scratch/t8/pkgcheck-t6 "$(basename "$(dirname "$p")")" >/dev/null 2>&1 && echo PASS || echo FAIL; done | sort | uniq -c   # the FAIL list is the Q2 lead list; #852's recipe is one
  # the scripts (every path whose first line is a shell shebang, spaces in names included) and the units
  while IFS= read -r f; do [ -f ".qa-scratch/t8/at-hash/$f" ] || continue; head -1 ".qa-scratch/t8/at-hash/$f" | grep -q -E '^#!.*(ba)?sh' || continue; bash -n ".qa-scratch/t8/at-hash/$f" 2>/dev/null && echo "ok $f" || echo "FAIL $f"; done < .qa-scratch/t8/paths.txt | cut -d' ' -f1 | sort | uniq -c   # 45 shell files in the inventory; the shebang count may differ: record both
  while IFS= read -r f; do [ -f ".qa-scratch/t8/at-hash/$f" ] && grep -q -E '^\[Unit\]' ".qa-scratch/t8/at-hash/$f" && echo "$f"; done < .qa-scratch/t8/paths.txt > .qa-scratch/t8/units.txt; wc -l < .qa-scratch/t8/units.txt   # the units; /usr/bin/systemd-analyze IS on the host: `systemd-analyze verify <unit>` on a copy of each, its output recorded (a dependency it cannot resolve on the host is noted, not a finding)
  # the record and the 13 (§ 2's block), then the GENERIC_X64 install tree for every unit's ExecStart path (ls only)
  I=/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system
  # sourcing config/options creates build.pixelelated-<DEVICE>.<ARCH>/.cache_package_{local,global} in this worktree (gitignored, so `git status` does not show them: `ls -d build.pixelelated-*`): remove each at the end only after 'find <dir> -type f | wc -l' prints 2
  ```
- **The guest**, only for a stream's behaviour claim (stage E) and only
  after the host file is read: `projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm
  run --headless --daemonize` (the rule's `VM_TOOL`) on the T8 disk, `tools/vm-serial` for the root shell, the
  census before and after, `tools/vm-stop` by pidfile; frames under
  `/workspace/artifacts/m6-t8-<date>/`; the cycle named on #655 before the
  boot with what it leaves.
- **Phase 4.6, one seat:** `npm install --prefix tools/council`,
  `tools/council/run verify-pins`, `tools/council/run test`; the probe
  (`--member gpt`, identity, effort `max` and provider OpenAI read from the
  provider's own field; its `.provenance.json` beside it); then one
  refutation pass over **one bounded packet**: `02` without its generated
  rows, `03`, `04`, the Q4 table, **the 35 fork-own files whole**, **the
  upstream-carried recipes as the fork's diff against `upstream/next`
  (`git diff upstream/next 8ebaf8daad -- <path>`) plus line-numbered
  excerpts of twenty lines either side of every cited line**, the conflict
  list, and the fixtures' outputs; **capped near 440 KB** (the GPT seat
  took T30's 438,502-byte packet whole; its size and sha256 are recorded in
  `00` beside the provenance). A seat that fails is a hold on #655 with the
  numbers (D-WORKFLOW-195's trimmed packet is the coordinator's call);
  never a Local fallback.
- **A read is free and goes through the filter** (`grep -v -i -E
  'key|pass|token|user|psk|login'` on any log or config read from an M7
  root, the install tree or the cache). The wordlist is never read; the
  council env is never read.

**What never runs in this slice:** a build; a compile; a container; a
command on a handheld, a cloud or a shared backend; a process in an M7
worktree; a model call outside `tools/council/run`, and none but the one
seat's probe and refutation; `make update`, `scripts/update_packages`,
`tools/update-pkg` or `tools/update-scan` (they edit recipes or read every
upstream); a full archive download except for a URL the probe redirected
(then once, streamed through `sha256sum`); `curl -L` on the probe; a move,
copy or deletion in the shared source cache; a pin change; a deletion of an
upstream-carried file or of an orphan; a change to a file outside the 485
(the emulators metapackage, `rocknix`, a cloud or proxy package, `systemd`'s
override, a quirk); an edit at stage B (a finding is a row; the edit waits
for its stream brief); a guest boot without the host file read and the
cycle named first; `--no-verify`; bare `git stash`; `git worktree remove
--force` or `rm -rf` of any worktree; a tree export under `/tmp` (use
`/workspace/tmp/m6-t8/` after `df -i`); an unquoted heredoc for prose; a
change to the order, the slices, the plan, this brief, #655's criteria or
the M6 body (D-WORKFLOW-189); a comment on #585 or #645; a GitHub issue
other than the audit punch-list issue and `bug` issues.

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#655`
(`Refs #655`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-image-packages/00-running-log.md` | the flight recorder: the model and effort, `reviewed-at` with `8ebaf8daad` beside it, every § 5 command with its exit status, the API budget before and after each loop, the Facilitator's probe and refutation with their times, the packet's size and sha256, every guest cycle's census and stop line, every `PROOF:` line, each time from `date -u` | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 485 re-derived with § 2's filter and its output, the provenance counts (35 fork changes: 8 added, 19 edited recipes, 8 other files; 18 absent upstream: 11 orphans, 7 fork-added; 66 upstream-changed; 40 commits), the conflict set's size, the branch's deltas from the hash (none expected); § Phase 1: the three movers in the slice's own words, the `make update` set, the 28 unbuilt settled | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #655's checklist, plus **a coverage table with one row per path** (485; the first cell the path in backticks so ``grep -c -E '^\| `projects/'`` counts them), § Mechanical checks (every § 5 block with command, exit status, summary), § The fetch sweep, § The conflict set (each fork-edited ∩ upstream-changed recipe with its hunks and the merge disposition), § The #644 findings (15 and 16 here; the others named with carriers); every proof with a `proved:` cell | B, then F |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: the base merge x the fork's 19 edits; `make update` x the 8 hash pins; the orphans x their dependants; #852 x `scripts/install`; the overrides x T7's generic recipes | B |
| Analysis | `.../04-analysis.md` | Phase 4, § Finding Verification (4.5), **§ Second opinion** (4.6: the GPT seat's probe and refutation graded item by item with the artifact that decided each, the packet's size named), **§ Renovation face** Q1 to Q7 (all seven), **Q4 carrying the currency table** (260 rows with the effective pin per plan, the (a), `make update` and (c) cells and the disposition naming the mover; also `q4-table.md` and `q4-pins.json` beside it), the orphan table (11 rows: what the fork used it for, dependants, upstream's replacement), the conflict list, Q6's 28 settled | C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (independent; `gpt` at `max`), the seat's brief, the probe prompt, `gpt-probe.md` and `gpt-audit.md` each with its `.provenance.json`, the packet's manifest (paths and sha256) | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (does not certify resolution)` | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category, where (file:line at `8ebaf8daad`), acceptance; the YAML `punch_index`; the fork-own BEHIND rows as items whose outcome is *a Backlog issue in #839's shape, the coordinator's*; the conflict list as one item whose outcome is *read at integration, the coordinator's* | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #655 | `Audit: M6 T8 the image's own packages -- N findings (...)`; one checkbox per item, agent-first (`tools/box-check --issue N` passes) | D |
| Bug issues | GitHub, label `bug`, `Bug:` title, milestone-less | one per defect (D-WORKFLOW-187): the code trace shape, `Already written:` (a config or a unit the fork edited: what an upgraded device already carries), the VM line | D |
| **The stage-D pause** | #655 | the punch list posted with the audit issue's and the bugs' numbers; the lane waits for the coordinator's stream briefs (plan § 6b E) -- meanwhile it drafts nothing under `projects/` | D |
| Remediation | the slice branch | each stream as its brief says; **no pin moved, nothing deleted**; a fix with its fixture or guest proof first, the stubs' counts printed, a commit naming its paths | E |
| Verification | `02-forward-audit.md` appended; `audit-completion.json` after the coordinator closes the audit issue | every proof's `proved:` cell one of `tree`, `history`, `fixture`, `fix-tree`, `fix-guest`, `fix-pending-image` | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-image-packages.md`, posted on #655 | the mini-retro's four answers with its scoped audit; **what the slice did to the two time-to-play numbers** (a boot-path change says so); its *adjustments* are proposals for the coordinator | G |
| Hand-back | #655 | `reviewed-at:` and `fixed-at:` in the body; one comment: the tip, each artifact by path, the six checker exit codes, each fix's `proved:` class, the seat's served model from its provenance, the API budget spent | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-image-packages-655.md` | seeded by the coordinator; updated at every checkpoint | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session headed `#655`, stamped from the clock, prose through a quoted heredoc | every session |

## 7. Acceptance

The checklist on #655 is the contract (its body carries these eighteen,
written there with version 2 in place of the five generated ones; where
the two differ, #655 wins and the coordinator corrects the brief). Each
names the artifact that ticks it; the coordinator ticks at hand-back.

- [ ] `docs/audits/<date>-epic-m6-image-packages/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-image-packages/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: independent`, one reviewer (`gpt`, `openai/gpt-6-astra`, `max`), and the seat's probe and refutation outputs each have a `.provenance.json` beside them whose served model is `openai/gpt-6-astra` by OpenAI (the field quoted on #655); `04` § Second opinion grades every item of the refutation against its artifact and names the packet's size and sha256.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (#585 for an upstream-carried file's defect, a Backlog issue in #839's shape for a fork-own bump, the integration for the conflict list), or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits the read and the fixes were made at (the read on `8ebaf8daad`'s bytes; no EmulationStation path), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed`.
- [ ] `01-research-notes.md` § Scope records the read hash, the filter of brief § 2 with its output (485 paths, 20,644 lines; 450 upstream-carried, 35 fork-own; 478 `shipped`, 6 `test`, 1 `n/a`; 260 recipes; 14 paths with spaces, or the deltas beside them), the provenance counts (35 fork changes; 87 modified against `upstream/next`; 18 absent upstream as 11 orphans and 7 fork-added; 66 recipes changed upstream; the conflict set of 11), and the branch-vs-hash diff over the 485 read with `xargs -0` (empty, or each hunk listed with its owner).
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c -E '^\| `projects/' 02-forward-audit.md`` prints 485; each row's Q1 to Q7 cells answered or `n/a` with a reason.
- [ ] `02-forward-audit.md` § Mechanical checks records, with command, exit status and summary line, each of: the branch-vs-hash diff over the slice's paths, the (a) loop with its four counts, the conflict set's derivation and size, the per-plan expansion of every field for the 260 (with the empty-or-unset-checksum rows: `atf` and `sway` expected, T5's, and nothing else), the `make update` set for RK3588 and the three shipped plans with the 13 named, the freshness tool's run with its exit code and each class, the fetch sweep's status-code histogram, the two `pkgcheck` runs' counts and FAIL lists, the `bash -n` sweep's counts by shebang, and the units' count with `systemd-analyze verify`'s outputs; a check that could not run is recorded with the reason, never as a pass.
- [ ] `04-analysis.md` § Renovation face Q4 carries the currency table: 260 rows (``grep -c -E '^\| `projects/' q4-table.md`` prints 260), each with the effective pin per plan, its shape, the (a), `make update` and (c) cells, and a disposition from § 4 Q4's list that names the mover; **no row reads `current` on a source whose cell is `not read`**; every fork-own BEHIND row is a punch item whose outcome names a Backlog issue in #839's shape.
- [ ] `04-analysis.md` carries the orphan table (11 rows: the recipe, what the fork used it for, its fork-own dependants or `none` from `git grep`, upstream's replacing commit or `none`), the conflict list (every fork-edited recipe upstream also changed since the base, each with its hunks and `same change` / `different, keep ours` / `conflict`), and § Q6's 13 unbuilt names settled (the 12 virtual by construction; `qcom-abl` with its plan or condition quoted), the record matched by name prefix with the five listings saved.
- [ ] `02-forward-audit.md` § The fetch sweep lists every effective `PKG_URL` whose HEAD probe did not answer 200 or a redirect that resolved to the recipe's sha256, with its status, the mirror's answer and its disposition; every gone or mismatched URL is a `bug` issue cited by number; the probe's two controls are recorded.
- [ ] `02-forward-audit.md` § The #644 findings carries findings 15 and 16 with their dispositions here (15: the `make update` set and its 13 named, never run, `scripts/update_packages`'s `PKG_PATH` line cited; 16: the 11 orphans separated from the 7 fork-added by the base, with the freshness tool's set compared) and names the other findings with their carriers so none is taken here.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `fixture`, `fix-tree`, `fix-guest` or `fix-pending-image`; ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c '^PROOF:' 00-running-log.md``; every guest cycle has its census and `tools/vm-stop` line in `00`.
- [ ] Every punch item carries `question:`; every `bug` this lane files passes `tools/box-check --issue N`; no file under `projects/` is changed on this branch before a stream brief (`git diff --stat 8ebaf8daad <fixed-at> -- projects packages` shows only stage-E commits), and no `PKG_VERSION` line changes on this branch at all (`git diff 8ebaf8daad <fixed-at> -- projects packages | grep -c '^[-+]PKG_VERSION='` prints 0); `tools/pkgcheck` passes on every recipe a stream touched.
- [ ] No upstream-carried or orphan file is deleted or renamed on this branch (`git diff --diff-filter=DR --name-only 8ebaf8daad <fixed-at> -- projects packages` is empty).
- [ ] #852's fix is on this branch under a stream brief, proved: `virtual/image`'s recipe writes nothing at global scope (a fresh export sourced through `config/options image` leaves no `build.*/image/system/opt`), and the image root still carries `opt -> /storage/.opt` (`fix-pending-image`, the first image).
- [ ] The retro exists at `docs/retros/<date>-m6-image-packages.md`, is posted on #655, and says what the slice did to the two time-to-play numbers (nothing, or the boot-path change named).
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge, and `tools/lint-audit-artifacts` prints `PASS` on the folder; the six exit codes pasted on #655.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #655; a blocker named on #655 with what is needed (the seat failed, a
count that cannot be produced, two commands that disagree, the host held
by M7 when a guest cycle is due); a branch that differs from `8ebaf8daad` on
one of the 485 at stage A in a hunk the dispatch comment did not name; or
an execution limit, stated as such with the running log current. A
checkpoint is not a stop; a differing count is a delta; `next` moving is
drift. An idle session says it is idle on #655, **and does not end a turn on
a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#655`, its time from `date -u` in
  the same command, its prose through a quoted heredoc or the Write tool;
  `tools/work-log-index --write` after it.
- A friction line the moment something slows, with `issue: #655` or the
  guard.
- The VM question written before any proof (§ 5: yes for a behaviour
  claim; the reading needs no guest).
- The mini-retro at stage G, posted on #655, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator (D-WORKFLOW-189).
- A register row the same session for any decision the slice forces; the
  next Decided ID is checked on every pushed branch at the time (on
  2026-10-24 the highest Decided row is D-WORKFLOW-196, the coordinator's;
  T30 runs beside this lane and may take 197); it goes at the end of `##
  Decided`.
- `tools/ceremony-check` before every push; what another lane owes (the
  W42 summary, M7's) is noted, not paid. Never `--no-verify`. A merge with
  conflicts is checked for markers (#696); the ledgers are united by whole
  entries. **A commit names its paths**; **a tree export goes under
  `/workspace/tmp/m6-t8/` after `df -i`, never under `/tmp`**.
- Commit messages `docs: ...` for the audit and `<package>: ...` for a
  recipe, script, unit or config change under a stream brief, with `Refs
  #655`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#655's checkboxes against their artifacts; the lint's `PASS` line;
`review-plan.json` and the seat's provenance (served model, provider,
effort); the audit issue's checkboxes all at an outcome; the coverage
table's row count (485) and the currency table's (260); no `current` beside
a `not read`; the orphan table and the conflict list; **re-running on an
export of the tip under `/workspace/tmp`: the membership block, the (a)
loop, the conflict set and the `pkgcheck` baseline in full, the per-plan
expansion for the 13 `make update` recipes and the 13 unbuilt real ones,
and the hash-pin `compare` on ten rows drawn with `shuf --random-source=<(yes
t8)` (the seed recorded), which must agree with the lane's rows** (A8);
`register-check` on a simulated merge with the coordinator's tip (the
ledgers united); the retro's four answers; the six exit codes. The lane
posts one hand-back comment naming the tip and each artifact by path,
writes `reviewed-at:` and `fixed-at:` into #655's body, then says it is
idle. After acceptance the coordinator closes the audit issue, prompts the
lane for `audit-completion.json` and the full lint, merges the branch in
its turn after the M7 candidate (after T7's, before T4's), regenerates the
ledgers, files the Backlog bumps, reads the conflict list at the base
merge, and closes #655 when every row is proven. A brief that needed the
coordinator's help mid-slice beyond the stage-D pause is a defect in this
brief: log the friction; the coordinator fixes the template.

**The readings before dispatch** (plan § 3, principle 3): the epic's futro
(#848) carries a T8 kickoff addendum written with this version, and a
stranger's proof of this brief is run by a reader with no context before
dispatch; version 2 records what each found.
