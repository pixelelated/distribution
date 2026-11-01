# Futro: the generic-packages area epic (#848), at T7's kickoff (#654)

**Prepared:** 2026-10-24, by the M6 coordinator lane (D-WORKFLOW-189), from
the brief `docs/reviews/briefs/generic-packages-reached.md` version 1
(committed beside this file) and the tree at `next` = `8ebaf8daad`; the
inventory at P1's `2174265e9c` (`eb4763e3cc`'s `inventory.json`, sha256
`d17b9cac4b2c…`).
**Scope of this futro:** the area epic #848 (the generic packages: T7 #654
the recipes under `packages/**` a shipped or test image builds, T8 #655 the
image's own recipes under `projects/ROCKNIX/**`, T23 #670 the generic
recipes no image builds) at the kickoff of its first slice, T7. It covers
T7's execution under its brief and the order of T8 and T23 after it. It does
not cover T8's or T23's briefs (their own readings at their dispatch), the
emulators metapackage (T3's and T30's, excluded from T8 by its glob), or
the integration merges (the coordinator's, plan § 8).

**Upstream retros consulted:** T3's mini-retro (#650,
`docs/retros/2026-10-24-m6-emulators-libretro.md` on the T3 branch; its
adjustment 2 became #844, the empty-cache fetch check; its S6 found #841);
T5's (#652: D-WORKFLOW-193/194, the fetch that fails without a checksum;
E6's count per shape); T6's (#653: the late-binding sweep's leads on #654,
`jre.zulu/package.mk:12`, `mesa-reusable/package.mk:14`, the `wireplumber`
parser false positive routed to #657; the brief's wrong 0-FAIL `pkgcheck`
baseline, 12 FAILs on real recipes at the hash); P1's
(`docs/retros/2026-10-23-m6-p1-survey.md`). T30 is at stage B (its 09:02
post on #677: `portaudio`'s source gone, #849) and has no retro yet.
**Inputs considered:** the brief; #654's, #655's and #670's bodies; #848's
body; the plan (§ 3, § 4, § 5, § 6a to § 8); `docs/reviews/order.md` § T7,
§ T8, § T23 and its sizing table; `slices.json` entries 7, 8 and 23;
`areas.json`'s `generic-packages` entry (globs `packages/**` and
`projects/ROCKNIX/packages/**` less the emulation, kernel, firmware,
quirks, interface, cloud and proxy trees, patches and kernel configs);
`docs/reviews/build-path-read.md` (#644) findings 15, 16 and 17 and its
§ 5 recommendations; #645; `tools/fork-package-freshness` (its header and
`--list`), `scripts/update_packages`, `tools/update-pkg` and the 62
`tools/update-functions/` at the hash; the five M7 build roots' `build/`
listings (read only); one probe of the GitHub contents API against
`LibreELEC/LibreELEC.tv` master (`pciutils`: `3.15.0` on both sides);
#841, #849, #844, #839, #585, #576.

## 1. What do we know and what are we assuming?

**The plan, restated.** T7 is a table at Local depth (D-WORKFLOW-184: *the
executor alone; the lint and the counts are the check*) over the 266 paths
of the `generic-packages` area under `packages/**` whose reach is `shipped`
(256), `test` (7) or `n/a` (3): 243 recipes, 23 other files (6 `other`, 4
shell, 3 cmake, 3 config, 2 udev, 2 none, 1 markdown, 1 text, 1 systemd),
7,612 lines; 250 upstream-carried and 16 fork-own. Its lens is **package
currency**: for each recipe, the pin at `8ebaf8daad` and how far it stands
from what could be built instead. The deliverable is the table, one
disposition per row, and the findings the table turns up; **it moves no
pin** (a bump is a build, and the renovation builds nothing, D-WORKFLOW-187)
and **deletes nothing upstream carries**. T8 follows at Independent depth
over the image's own 485 paths (its overrides source T7's recipes, which is
why T7 is first); T23 tables the 1,604 paths no image builds after both
(its 620 `shadowed_by` copies need T7's and T8's rows to say which copy is
live).

**What the read established before this futro (every figure at the hash
or the inventory):**

- **Three sources of "current", and three different movers.** (a) ROCKNIX's
  `upstream/next` (`e0f9deb899`): **0 commits touching `packages/` since
  the base `c445081a59`** (325 commits overall), so every upstream-carried
  row is byte-identical to upstream today, and the check is one loop. (b)
  LibreELEC master: `packages/**` arrives in ROCKNIX only by merging
  `LibreELEC/master` (the last on `upstream/next` is `d43d166b7a`,
  2026-08-12, LibreELEC's PR #11671), so **LibreELEC master is the mover of
  every upstream-carried pin here**, and a pin behind it moves when ROCKNIX
  merges LibreELEC, not by anything the fork does. (c) The project's own
  release: the mover only for the 13 recipes the fork introduced
  (`tools/fork-package-freshness`'s set under `packages/`, D-WORKFLOW-024),
  and informational everywhere else.
- **`make update` is not T7's mover.** `scripts/update_packages` walks
  `projects/ROCKNIX/packages` only (its `PKG_PATH`), from the three virtual
  packages' dependency lists, to each repository's branch head; it never
  touches a `packages/**` recipe. #644 finding 15's T7 half is therefore
  answered before the slice starts: the base merge is the only mover, and
  the row says so. The T8 half (whether `make update` is ever run) is T8's.
- **Provenance by git, not by the freshness tool's set** (#644 finding 16:
  *a diff is not a provenance*). Against the base and against
  `upstream/next`: **13 recipes added by the fork and absent upstream**
  (brotli 1.2.0, ruby 3.3.12, unifdef 2.12, openjpeg 2.5.4, woff2 1.0.2,
  glib-networking 2.90.0, libtasn1 4.21.0, dmidecode 3.7, qrencode 4.1.1,
  ryzenadj 0.19.0, libpsl 0.23.3, libsoup 3.8.0, webkitgtk 2.54.1), **3
  upstream recipes the fork edited** (libyaml: `PKG_DEPENDS_HOST="ccache:host"`
  with its comment; libsamplerate: `--with-pic`; syslinux: two `cp` lines
  for `ldlinux.c32`), **227 untouched**. The freshness tool's `--list`
  names exactly those 13 under `packages/` (its other 34 entries are T8's,
  22 of them the orphans finding 16 describes). None of the 13 is an
  orphan: all are absent on `upstream/next` because the fork wrote them.
- **The fork's `packages/` files cannot go upstream where they are**
  (#645, finding 17: `trigger-fail-if-upstream-changed.yml` refuses any PR
  touching `packages/**`; upstream's `AGENTS.md` puts recipes under
  `projects/ROCKNIX/packages`). #645 carries the move table; T7 proposes a
  disposition per row there and moves nothing.
- **The pins' shapes:** 232 version strings, 10 commit hashes (x264,
  arm-mem, configtools, crossguid, heimdal, kmsxx, dbussy, fuse, udevil,
  populatefs), 1 recipe with no `PKG_VERSION` of its own (`harfbuzz-icu`
  sources `harfbuzz`'s). By `PKG_URL`'s host over the 242 with a version:
  other 78, github.com 73, freedesktop.org 39, gnu.org 23, kernel.org 12,
  gitlab 10, sourceforge 6, no `PKG_URL` 1.
- **Checksums:** every archive recipe in the set carries `PKG_SHA256`; the
  7 without one are the 6 virtual packages (alsa, autotools, corefonts,
  debug, misc-packages, toolchain: `PKG_URL=""`) and `harfbuzz-icu`. T5's
  five archive versions without one (D-WORKFLOW-194: `atf`, `rkbin`,
  `libmali-vulkan`, `sway`) are ROCKNIX overrides, outside this set; the
  generic `atf`, `rkbin` and `sway` copies are T23's `shadowed_by` rows.
  So T7 expects **no** missing-checksum finding, and a count other than 0
  is the first lead.
- **The record agrees with `shipped`, almost.** Of the 243 names, 236 have a
  build directory in at least one of the five M7 build roots (read only;
  GENERIC_X64 226, H700-aarch64 220, H700-arm 149, SM8550-aarch64 227,
  SM8550-arm 151). The 7 with none: the 6 virtual packages and
  `ntfs-3g_ntfsprogs`.
- **46 of the 243 recipes carry patches** (the inventory's `patches`
  column); the patches are T42's and T43's rows, and T7 reads one only to
  say what a bump would re-cut.
- **The GitHub API is the way to LibreELEC master** (no remote is added to
  the repository): `repos/LibreELEC/LibreELEC.tv/contents/<path>?ref=master`
  answered for `pciutils` with the same `PKG_VERSION` and `PKG_SHA256` as
  the hash; the budget is 5,000 calls an hour, shared with the
  coordinator's monitors (about 14 reads a minute).

**Assumptions the plan relies on that are not in its text:**

- A-1 The inventory's `shipped` is a fact about the plans, not about the
  roots. The 7 unbuilt names are the test: 6 are virtual (no build
  directory by construction) and `ntfs-3g_ntfsprogs` is not, so either a
  plan builds it and the roots predate that, or the resolution overstates.
  The slice settles it first.
- A-2 `upstream/next` stays at 0 `packages/` commits for the slice's
  duration. The read is a fact about `8ebaf8daad`; the next base merge is
  drift (`tools/renovation-drift`, the coordinator's).
- A-3 LibreELEC master is readable for 250 paths within the budget: 250
  calls at one every third of a second is two minutes and 5 % of the hour;
  a 404 means *absent on LibreELEC master* (a ROCKNIX-only generic recipe,
  or one LibreELEC deleted) and is a row class, not an error.
- A-4 The freshness tool runs read-only (GitHub API, `curl` to gnome, gnu,
  webkitgtk.org, ruby's cache, dotat.at) and exits 2 where a host cannot be
  read; UNKNOWN stays UNKNOWN in the table.
- A-5 `tools/pkgcheck` at the hash is the shipped check; T6's widened copy
  (`44f64842b6` on T6's branch, unmerged) is read from that branch and run
  from T7's own worktree; a row says which produced it.
- A-6 A HEAD request tells whether a `PKG_URL` still answers; a 301/302 is
  the finding (#841's class) and the one case where the archive is fetched
  in full to compare its sha256; a 404 or no answer is #849's class, a
  `bug`. The shared source cache's `.sha256` stamps are the record of what
  the bytes were when fetched; they are read, never moved.

**Substrate preconditions, and their evidence:** `gh` authenticated
(`gh api rate_limit` answers; 5,000/5,000 at 09:17 UTC); `python3 -I`;
`tools/pkgcheck` at the hash; `docs/reviews/inventory.json` in the
P1-stacked worktree; the five M7 roots' `build/` directories exist and are
listable; `/workspace/cache/rocknix-sources/<name>/` readable; `curl`. No
guest, no compiler, no container.

**Build-vs-adopt:** not applicable (a table). The one tooling question --
should the freshness tool's host handlers be extended to the 230
upstream-carried recipes? -- is answered *no* here: LibreELEC master is
their mover, so the handler would measure a distance the fork cannot close;
a Backlog proposal, if the slice wants one, goes to #657's epic through the
coordinator.

## 2. What known unknowns need investigation?

- U-1 How many of the 250 upstream-carried recipes differ from LibreELEC
  master today, and by how many releases. Knowable at stage B by the API
  loop; proceeding without it, because the answer is the table.
- U-2 Whether `ntfs-3g_ntfsprogs` is built by any shipped plan (A-1): one
  `tools/viewplan` read per plan in the lane's own worktree, before the
  row is written.
- U-3 How many `PKG_URL`s redirect or are gone (A-6): knowable by the HEAD
  sweep; #849 says at least one of the whole tree's is gone, T30's; T7's
  243 are unknown until probed.
- U-4 How far the 10 hash pins are behind their default branches: the
  freshness tool's method (`compare` through the API) for the GitHub ones;
  `x264` (`code.videolan.org`) and any non-GitHub host may stay UNKNOWN,
  said so.
- U-5 Whether the fork's three edits of upstream recipes are still needed
  (`libyaml`'s host dependency, `libsamplerate`'s `--with-pic`, `syslinux`'s
  `ldlinux.c32`): `git log` on both sides and LibreELEC master's current
  text answer the first part; whether a build still needs them is not
  answerable without a build and is recorded as such.
- U-6 Which of the 13 fork-introduced recipes `fork-package-freshness`
  reports BEHIND today: the run answers; each BEHIND becomes a Backlog
  issue in #839's shape, the coordinator's to file at acceptance.

## 3. What patterns from prior work apply that we haven't named?

- **T3's two-tier Q4** (`q4-pins-table.md`, `q4-pins.json` in its audit
  folder; T30's copy beside it): behind-upstream against behind-project,
  with a disposition per row. T7 adds the third source because `packages/`
  has a different mover than the emulators' recipes, and names the mover
  in every row.
- **#841's class, found by T3's S6:** a repository renamed under a
  `PKG_URL` changes the archive's top directory and its sha256; the shared
  cache hides it. T7's sweep is the HEAD-probe form of S6's fetch: no full
  download unless the probe redirects.
- **#849, T30's today:** the source gone outright, the cache the only copy.
  T7 counts its own such cases before any bug is filed, and names the
  cache as a retained input (D-INFRA-022) in each.
- **T5's count per shape (D-WORKFLOW-194):** a checksum lives in a `case`
  branch as often as at the top; T7's count tests both shapes, as T5's E6
  learned to.
- **T6's reachability table** shape: one row per path, a positive control
  beside every zero (blindspot 22), `proved:` classes, no deletion of an
  upstream-carried file; and its wrong baseline (0 expected, 12 real) --
  T7 records its own `pkgcheck` baseline over the 243 before reading one
  FAIL as a finding.
- **Blindspot 75** (a count from the wrong tree): every figure above is at
  `8ebaf8daad` or the inventory, and the brief says which.
- **#644 finding 16's lesson:** the freshness tool's set is a diff against
  `upstream/next`, so a recipe upstream deleted looks fork-introduced. T7
  states provenance with `git log --diff-filter=A` against both bases and
  found no orphan among its 13; T8 will.

## 4. What could we be missing?

**Agent-execution simulation** (a fresh Opus 5.5 lane with the brief and
the issue):

- S-1 It reads *currency table* and fetches 243 archives to compare
  hashes. → The brief forbids a full download except on a redirect; the
  HEAD probe and the cache's `.sha256` stamps are the evidence.
- S-2 It adds a `libreelec` remote to diff `packages/` against master. →
  Forbidden: a remote is a write to the shared repository every worktree
  sees; the contents API is the read.
- S-3 It reads *behind LibreELEC master* as actionable and proposes a bump
  per recipe (230 punch items). → A `packages/**` pin moves by the base
  merge; the disposition is `follows the base merge; LibreELEC master at
  <version>`, and the fork proposes nothing to LibreELEC (outside its
  lanes, D-UI-079's spirit). Only a fork-introduced recipe's bump is the
  fork's, one Backlog issue each in #839's shape, filed by the coordinator.
- S-4 It bumps a BEHIND fork-introduced recipe in the slice. → No:
  D-WORKFLOW-187; a bump is a build.
- S-5 It files 12 bugs on upstream recipes `pkgcheck` fails. → The
  baseline is a count; a FAIL on an upstream-carried recipe is one
  `Renovation` row class with a #585 candidate, a `bug` only where the
  shape would break a build (`bugs-are-agent-first.md` rule 6).
- S-6 It fires 250 API calls in parallel and trips the secondary rate
  limit, then reads the 403s as *absent on LibreELEC master*. → Serial,
  with a pause; `rate_limit` read before and after; a non-200 other than
  404 is *not read*, never *absent*.
- S-7 It runs `tools/update-pkg` or `scripts/update_packages` "to see what
  they would do" and edits recipes in place. → Both are on the never-run
  list; they write `package.mk` files.
- S-8 It sources a recipe at global scope to expand `PKG_URL` and the
  recipe's functions run. → Expansion goes through `config/options <pkg>`
  in the lane's worktree, as `scripts/update_packages` does, with
  `PROJECT`, `DEVICE` and `ARCH` set; the output is one line, the URL.
- S-9 It runs `tools/pkgcheck` *in* an M7 worktree to use T6's widened
  copy. → Never a process in an M7 worktree; T6's copy is read with `git
  show` from T6's branch and run from T7's worktree.
- S-10 It types a timestamp (T30 slipped twice today). → `date -u` in the
  same command (#843).
- S-11 It exports the tree under `/tmp`. → `.qa-scratch/t7/at-hash` for
  the 266 files (small), `/workspace/tmp/m6-t7/` for anything whole-tree,
  after `df -i`.
- S-12 It reads `PKG_SITE`'s host against `PKG_URL`'s as a signal of a
  personal-fork URL (portaudio's shape). → 159 of the recipes with both
  differ by host (a project page against a download host: `gtk.org`
  against `download.gnome.org`), so the mismatch is not the signal; the
  reading is of the 73 GitHub URLs' owners against the project the
  recipe names.

**Pre-mortem.** A month on, the table reads *243 rows, 0 pins moved*, and
the maintainer asks what the slice changed. The honest answer is: the
record of where every generic recipe stands against its three sources, the
dispositions that say which mover closes each gap, the gone and redirected
sources found before an empty-cache build finds them, the 13 recipes whose
home #645 settles, and the Backlog issues for the fork's own bumps. The
futro names that now so the hand-back can say it in those words; the
currency itself lands at `release-candidates.md` step 0, with the base
merge.

**Blindspot check.** 13 (assumed done: the freshness tool's last exit 0 is
`rc-preflight`'s business; the slice runs it again); 22 (a probe that
cannot report absence: a HEAD that is refused with 405 is not *gone*, the
`--range 0-0` GET is the second pattern; a 404 from the contents API is
*absent*, a 403 is *not read*); 46 (a name read as a behaviour: `PKG_SITE`
is a homepage, not a source); 51; 75 (the tree); 29/second use (#811): not
triggered.

**Replaced-mechanism archetype:** nothing is replaced; the slice adds a
table.

**Honesty check.** Second archetype, the coordinator at acceptance: can the
table be re-derived without re-spending the budget? The membership, the
tier (a) loop and the `pkgcheck` baseline re-run in full on an export; tier
(b) and the HEAD sweep re-run on twenty rows chosen by `shuf` with a
recorded seed, and the twenty must agree with the lane's rows.

## 5. What adjustments or investigations must happen BEFORE execution?

**Written into version 1 of the brief (before the stranger's proof):**

- A1 § 4 Q4 names the three sources and the mover of each; an
  upstream-carried row behind LibreELEC master is dispositioned `follows
  the base merge`, never a per-recipe bump; only a fork-introduced row's
  BEHIND becomes a Backlog issue (#839's shape, the coordinator files).
- A2 § 5's fetch sweep is a HEAD probe without `-L` plus the cache's
  `.sha256` stamps; a redirect is the one case of a full fetch; a 404 or no
  answer is a `bug` in #849's shape with the cache named as a retained
  input.
- A3 § 5 reads LibreELEC master through the contents API, serially, with
  `rate_limit` recorded before and after and a floor of 1,500 remaining
  before the loop starts; no remote is added.
- A4 § 2 states provenance from `git log --diff-filter=A` against both
  bases (13 added, 3 edited, 227 untouched) and reads the freshness tool's
  set as a cross-check, not a source.
- A5 § 2 and § 4 Q6 settle the 7 unbuilt names first (6 virtual by
  construction; `ntfs-3g_ntfsprogs` by `tools/viewplan` per plan) before
  any row says `shipped`.
- A6 § 3 reads T5's E6 and D-WORKFLOW-194 before any checksum row; the
  expected count of archive recipes without a checksum in this set is 0.
- A7 § 5 runs `tools/pkgcheck` at the hash over the 243 for a baseline,
  then T6's widened copy from T7's worktree; each row says which produced
  it; the two T6 leads are read directly.
- A8 § 4 Q7 proposes a disposition per fork-own row for #645's move table
  in `04-analysis.md`; the coordinator posts it on #645; the slice moves
  nothing.
- A9 § 10's acceptance re-runs the membership, tier (a) and the `pkgcheck`
  baseline in full, and tier (b) and the HEAD sweep on twenty seeded rows.

**Investigation tasks opened:** none beyond the slice's own stage B; U-2
is the slice's first row.

**Documented unresolved assumptions (proceeding without resolving):**

- Whether the maintainer wants the 13 fork-introduced recipes moved under
  `projects/ROCKNIX/packages` before the upstream series (#645's first
  criterion, M6-milestoned, unanswered on #346). Rationale: T7's rows
  propose; the move is #645's work either way.
- Whether `ntfs-3g_ntfsprogs` is `shipped`. Rationale: one row, settled at
  stage B.

**Blindspot register updates:** none. #849 is #841's class, and #844 is the
guard proposed for it; a third instance in T7's sweep makes the entry.

**Order of the area after T7:** T8 next (its 35 fork-own recipes are the
freshness tool's other 34 entries plus one; finding 16's orphan separation
is its), then T23 (its `shadowed_by` rows need T7's and T8's). Neither is
dispatched before T7's hand-back.

## Addendum: T8 at its kickoff (2026-10-24, from the brief `docs/reviews/briefs/image-packages.md` version 1)

**What we know and assume.** T8 is the area's second slice and the
renovation's **first Independent slice**: the image's own recipes under
`projects/ROCKNIX/**` less the emulators metapackage, reach `shipped`,
`test` or `n/a` -- **485 paths, 20,644 lines** (260 recipes, 65 configs, 45
shell scripts, 38 images, 30 systemd units, 7 makefiles, 5 C++ files and
the rest); **450 upstream-carried, 35 fork-own** (27 recipes and 8 other
files: 11 added by the fork, 24 edited). Unlike T7, every comparison here
is live: **upstream has changed 66 of the 260 recipes since the base** (93
files, 40 commits on these paths), **18 recipes present here are absent on
`upstream/next`** -- 11 orphans upstream deleted since the base (#644
finding 16: `libfreeaptx`, `opus`, `libfmt`, `glslang`, `vulkan-headers`,
`cargo`, `miniupnpc`, `rocknix-abl`, `tllist`, `mtdev`, `swaybg`) and 7 the
fork added (`gamescope-glm`, `gamescope-stb`, `mangohud-vulkan-headers`,
`mangohud-vulkan-utility-libraries`, `harfbuzz-icu`, `gst-plugins-bad`,
`gnutls`) -- and `gstreamer/gstreamer` was added on both sides (a merge to
pre-read). 50 recipes source a generic recipe and inherit its pin (the
effective pin is the override's: T7's seven, `opus`, `gcc`, `libfmt`,
`wavpack`, `zlib`, `libevdev`, `libfreeaptx`, are this slice's rows); 169
version pins, 41 commit hashes. **`make update` is this slice's mover for
13 recipes** (the three virtual packages' dependency lists for RK3588 name
171 packages; 13 are here, 8 of them hash-pinned: `box64`, `box86`,
`gamecontrollerdb`, `jstest-sdl`, `rocknix-hotkey`, `sdljoytest`,
`sdltouchtest`, `sixaxis`; `control-gen` and `portmaster` are on
`config/blocklist`), and it has never run on the fork (finding 15's T8
half). The record: 232 of the 260 names have a build directory in one of
the five M7 roots; the 28 without are 12 virtual packages, 3 recipes with
no URL of their own and **13 real recipes** (`armsx2-turnip`, `ecm`,
`enet`, `glfw`, `inih`, `inputplumber`, `layer-shell-qt`, `libsndfile`,
`m8c`, `renderdoc`, `rocknix-touchscreen-keyboard`, `speedtest-cli`,
`swayimg`) to settle per plan with `PKG_ARCH` expanded (plan § 6b E's new
bullet). Two bugs already stand in this set: #852 (`virtual/image`'s
load-time symlink) is this slice's to fix under a stream; #877 (`libfmt`'s
empty checksum) is fixed by a packet and read, not touched. #851
(`systemd`) is the OS-scripts area's, not this slice's.

**Known unknowns.** U-1 which of the fork's 19 edited recipes upstream also
changed (the base merge's conflicts, pre-read now). U-2 whether anything
fork-own depends on one of the 11 orphans (the base merge deletes them;
a fork dependant breaks). U-3 the 13 unbuilt real recipes: `PKG_ARCH`, a
plan condition, or a `shipped` claim to question. U-4 how far the 41 hash
pins are behind their default branches, and whether `make update` would
move any past a branch the recipe means to hold. U-5 the packet's size for
one GPT seat: 20,644 lines of recipes plus the analyses exceed what T30's
438 KB packet carried; the brief bounds it.

**Patterns.** T7's three-source Q4 with the mover named (here: (a) is
real, (b) does not exist -- these are ROCKNIX's recipes, not LibreELEC's --
(c) is the fork's for the 27 and the orphans' projects for the 11); T6's
late-binding leads (#852 here); T5's checksum policy (the per-shape count
over 260, including `case` branches: `libfmt`'s shape); T3's Phase 4.6 (one
probe, one refutation, the provenance beside each output), now with one
seat; the record's listing checked against names with `-<digit>` (T7's
`ntfs-3g`); `scripts/update_packages` read, never run (T7's incident).

**What could we be missing (simulation).** S-1 a lane runs `make update`
or `scripts/update_packages` "to see what moves": never-run, it edits
recipes and fetches. S-2 it deletes the 11 orphans as dead code: no -- the
base merge deletes them (D-WORKFLOW-187; `release-candidates.md` step 0),
the slice writes each one's row with what the fork used it for and whether
a fork-own recipe depends on it. S-3 it bumps a BEHIND fork-own recipe: a
build; Backlog in #839's shape. S-4 it edits the `rocknix` package, a cloud
or proxy package, a quirk or the emulators metapackage: outside the 485.
S-5 it hands the GPT seat every recipe in full and the seat's answer is cut
or the request refused: the packet is bounded by the brief (the analyses
whole; the 35 fork-own files whole; the upstream-carried recipes as the
fork's diff against `upstream/next` plus line-numbered excerpts around each
finding; a cap near T30's 438 KB, which the GPT seat took whole). S-6 it
reads a Gemini seat into the plan: Independent is one seat, GPT-6 Astra at
`max`; no second seat, no Local fallback, a failed seat is a hold. S-7 it
regenerates a table or a config with the host's locale: `env -i`, C locale.
S-8 an unquoted heredoc: the plan's bullet, re-read first. Pre-mortem: the
table says *66 behind upstream* and nothing happens until the base merge --
which is the point: the rows name what the merge brings, the conflicts it
meets and the orphans it deletes, so step 0 of the next candidate is a
read, not a discovery.

**Adjustments before execution (into version 1):** A1 Q4 has two live
tiers and one informational: (a) `upstream/next` per recipe with the
fork-edited ∩ upstream-changed set named as the merge's conflicts; (c)
the project for the 27 fork-own and the 11 orphans; `make update`'s 13 as
their own table; no LibreELEC column. A2 the orphans' dispositions are
*drop at the base merge*, each with its dependants searched. A3 the packet
is bounded as S-5 says, with its size and sha256 recorded beside the
provenance. A4 one seat, probe then refutation, the Facilitator installed
and verified first; a failure is a hold. A5 the 28 unbuilt names settled
per plan with `PKG_ARCH` expanded before any row says `shipped`. A6 #852's
fix is a stream of this slice; #877 is read only. A7 the 45 shell scripts,
30 units and 65 configs are read as code (Q2, Q3) with the GENERIC_X64
guest for any behaviour claim a stream makes. A8 the acceptance re-runs
the membership, the (a) loop and `pkgcheck` in full, the hash-pin `compare`
on ten seeded rows, and reads the provenance file's served model.

**Errata to the T8 addendum (version 2 of the brief, after the stranger's
proof: 98 claims, 76 right, 9 wrong, 8 partial).** The record's "13 real
recipes without a build directory" was the brief's own `sed` misreading
version suffixes that begin with `v` or a letter (`ecm-v6.16.0`,
`glfw-e2c9264`): all thirteen are built; the unbuilt are the 12 virtual
packages and `qcom-abl` (U-3 collapses to one name). Fourteen of the 485
paths carry spaces, so every list is read with `while IFS= read -r` or
`xargs -0`, and the (a) count is 87 modified, not 86. Six of T7's seven
overrides are in this set (`libevdev`'s is the OS-scripts area's).
`moonlight`'s per-device `case` pins make nine hash pins in `make update`'s
set, not eight. `systemd-analyze` is on the host. T5's `atf` and `sway` are
in this set and lack a checksum at the hash (fixed on T5's unmerged
branch): the per-shape count expects those two, not zero. The conflict set
is eleven paths. S-7's locale rule reaches `comm` too: `LC_ALL=C` on both
sides.

## Addendum: T23 at its kickoff (2026-10-25, from the brief `docs/reviews/briefs/generic-packages-dead-ends.md` version 1)

**What we know and assume.** T23 is the area's third and last slice, a
reachability table at Local depth over the 1,604 inventory rows (95,892
lines) of `generic-packages` whose reach is `unreached` or `unshipped`:
1,601 upstream-carried, 3 fork-own; 727 recipes in 731 recipe units; 260
rows in 93 units shadowed by a ROCKNIX override; 39 rows in 21 units
buildable only by devices the fork does not ship. The order's words were
*decides the removals*; the brief decides instead that **the lane removes
nothing and edits no recipe** (D-WORKFLOW-209): the dead set is upstream's
tree, the fork tracks `upstream/next`, and the futro above already held T7
to *deletes nothing upstream carries*. The table's product is a
disposition per unit and the one class decision the coordinator carries to
the maintainer with the counts. Assumed, and said in the brief: the
inventory's `reach` is one run of one tool on 2026-10-23
(`tools/renovation-inventory`, three plans); the lane's own three
`tools/viewplan` runs are the second command for the same quantity, and a
disagreement is a finding, never resolved either way in silence.

**Known unknowns.** The order's § T23 said 620 shadowed rows and the column
at `2174265e9c` holds 260: the table states the hash's figure. `installer`
is in the GENERIC_X64 plan while its row reads unreached: which directory
the plan resolves it to decides the row. Eleven files sit under a recipe
outside the set (unreached files under a reached recipe), which says
something about the tool's owning-directory rule. The `PKG_DEPENDS_UNPACK`
closure: 24 of the 727 recipes are named that way, and `spirv-headers` is
named by three recipes every plan builds, so the inventory's column is wrong
for it at least; the lane computes the rest. `cbindgen` is named by nothing
at the hash: possibly the only truly dead fork-own unit.

**Patterns from prior work.** T7's `t7-tables.py` (one generator for every
table, asserting the counts) and T45's `provenance.py`; the two-commands
rule from T45 (a column is a claim; the plan is the evidence); T15's
history-less export lesson, which does not bite here (the plans read
recipes, not history) but the worktree must be a full tree; T6's late-binding
sweep whose two unreached hits were parked on #670 for this table.

**What could be missing (the simulation).** A lane reading *decides the
removals* in the order and deleting 1,601 upstream files: the brief forbids
every edit under `packages/` and `projects/`, and § 7 checks both diffs
empty. A lane proving reachability by building a package: forbidden (no
build, no fetch; plan generation only). A lane matching package names to
plan lines by eye: the coordinator's own first parse read `build name:kind`
lines only and found 29 hits, the second read `install name` lines too and
found 84 -- the brief names the parse, and `get_pkg_directory` decides the
directory. A lane running `viewplan` with the wrong `ARCH`: the inventory's
header lists the configs its plans ran under; the brief names the three
and the lane records the header. The blindspot-75 shape (a count over the
wrong set) already struck this brief once in draft: the order's 620.

**Adjustments before execution.** The register row D-WORKFLOW-209 (the
removal rule) written at dispatch; § 2's figures all from `2174265e9c` or
from a command on the coordinator's tree dated 2026-10-25 and said so; the
stranger's proof before dispatch.

### Errata from the stranger's proof of T23's brief (version 2, 2026-10-25)

A read-only reader with no context checked 55 rows of version 1 (38
verified, 3 wrong, 12 partial, 2 uncheckable; 8 API calls). What version 2
corrects, each at the place it lands:

1. **"32 shadowed units carry a name no plan builds" was a count over the
   wrong unit set.** By the brief's own nearest-recipe rule and the three
   plans it is 5 (swig, amlogic-boot-fip, atf, rkbin, weston), and only 3 of
   their overrides are themselves dead. The 84 plan-named recipes, all
   shadowed, reproduce exactly. Blindspot 75's shape, a second time in this
   brief's drafting: the first grouping was a regex, the second the rule.
2. **"Upstream-carried" is the inventory's tier, not byte-identity today.**
   Eleven of the 1,601 differ from `upstream/next`: eight deleted there after
   the base (`projects/ROCKNIX/packages/{debug/strace,rust/*-snapshot,tools/grub,tools/qemu}`),
   three modified. Q1's cost paragraph now prices the two groups apart:
   `packages/` (0 upstream commits since the base) and `projects/ROCKNIX`
   (moved upstream, in the cheap direction).
3. **The `tools/` criterion could never have been ticked** against
   `8ebaf8daad`: the P1 tip adds 15 files there. Every "the lane changes
   nothing" check is now against the dispatch tip, the lane's own start.
4. **The `PKG_DEPENDS_UNPACK` evidence was cited from dead copies.** The
   three generic recipes named by file:line are rows of this slice; the
   plans build the ROCKNIX overrides, which name `spirv-headers` too. The
   conclusion stood; the citation did not. The namer grep takes indented
   declarations (`^\s*PKG_DEPENDS_UNPACK=`, 40 lines, not 38).
5. **`installer` was already decided by the hash**: `shadowed_by` set, the
   override's reach `test`.
6. **Eleven basename pairs sit in the set unmarked** (both copies dead, no
   `shadowed_by`, since the inventory marks only a built name):
   `spirv-headers` and `cbindgen` among them. The table resolves every pair
   with `get_pkg_directory`.
7. Smaller: the unshipped device list gains AMD64 and RK3399; "453
   LibreELEC merges" had no reproducible source and is dropped; `openssl`'s
   recipe is outside the set; T7's generator is under `tools/`; `viewplan`
   takes a second, not ten; D-WORKFLOW-204 is the status tool's states, not
   the reach column.

Not checked by the proof, and left to the lane's stage A: the inventory's
26 container plans (only the header's counts were read); `pkgcheck` over
the 727; the transitive `PKG_DEPENDS_UNPACK` closure beyond direct naming.
