# Brief: M6.P2 T5, the build engine (#652)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #652 differ, #652 wins and the
coordinator corrects the brief in the same session. **Version 1
(2026-10-24):** written after T1's, T2's and T3's briefs had each been
through a futro and a stranger's proof (plan § 3, principle 3), so the
shapes those found wrong -- a count the executor cannot reproduce, a tool
absent from the host, a line number quoted from memory, a command whose
variables do not survive a Bash call, a path that belongs to another slice's
area, a seam described as agreement where the files disagree -- are
answered from the start; it goes through the same two readings before
dispatch, and version 2 records what they found. **Each command block below
sets its own variables** (`D`, `B`, `A`): a Bash call in this harness starts
a fresh shell, only the working directory persists, and the fork's tools are
run by absolute path from `$D`.

## 1. Identity

- **Issue:** #652 `M6.P2 E339/T5: build-engine: the build engine`, slice
  `build-engine` (`k: 5`) in `docs/reviews/slices.json`, fifth in
  `docs/reviews/order.md` (§ 3 of the order: *"The build process before any
  device and before the rest of the interface (D-WORKFLOW-186)"*; T5 to T9
  are one cluster, the engine first "so the engine is read whole before
  anything it builds"; the order's row is on the P1 branch). **Epic:** the
  area epic for **the build engine** (`build-engine` in
  `docs/reviews/areas.json`: T5 and T6 `build-engine-upstream-tools`), filed
  by the coordinator at this slice's dispatch with its futro, under the
  renovation epic #339; #652 and #653 are re-parented to it and retitled
  `E<epic>/T<k>` (`milestone-phase-naming.md`). **Milestone:** M6 (`M6:
  Codebase renovation`); its body holds the live order; read it first.
  **Predecessors:** #346 (the plan), #641 (the survey, the inventory and the
  order; closed 2026-10-23), #644 (the coordinator's read of ROCKNIX's
  documented build path against the fork's, `docs/reviews/build-path-read.md`,
  26 findings each with a carrier: **nine are this slice's**, § 3), T1 #648
  and T2 #649 (accepted 2026-10-24), T3 #650 (running beside this lane).
  **Beside it:** T3 (#650, RetroArch and the libretro cores) runs in its own
  lane (D-WORKFLOW-190: slices in different areas run in parallel; two
  slices never share a path). T3 reads `distributions/ROCKNIX/config/functions`
  as context for the launch table its metapackage writes; **that file is
  this slice's** (§ 2), and a defect T3 finds in it is posted to the
  coordinator as a lead for this lane, never fixed by T3. **The dispatch** is
  the coordinator's comment on #652 that names this brief's commit, the
  model and effort, and authorizes the two external reviewer calls and the
  `npm install` of § 1; the lane's first comment answers it.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, re-order anything, change a criterion, write a
  brief, move the M6 body, edit `slices.json`, `areas.json`, `order.md` or
  the plan, move the build container's pin, or decide a question of scope:
  those are the coordinator's, reached through #652, one question at a time.
  What this lane does file: its own audit punch-list issue (stage D, the
  code-auditor skill's Phase 6) and a `bug` issue for every defect it finds
  (D-WORKFLOW-187: a defect found by the renovation is a bug like any other;
  `bugs-are-agent-first.md` gives the shape, with its VM-verifiable
  criterion -- for an engine defect, the artifact is usually a recorded run
  or a sandboxed call of the function, § 5). Nothing else.
- **One worktree, one session.** The slice's paths are all in the
  distribution, so the lane holds one worktree: branch
  `feature/m6-build-engine-652` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-652`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** (which carries the P0 branch), with the coordinator's tip
  merged in and the lane's pointer seeded (the two hashes are in the
  dispatch comment on #652). The coordinator wrote there only before the lane
  started; from the dispatch on, one session per worktree (D-WORKFLOW-183)
  and the coordinator writes nothing there. **The rules in this worktree are
  `next`'s except four files:** P1's `fork-workflow.md` and
  `instruction-files.md` (the three renovation tools added to the fork-tool
  lists), the coordinator's `generic-x64-vm-testing.md` (a paragraph on
  `time-to-play`'s reboot, `8c9b1d4721`) and the council skill's
  `.claude/skills/council/IMPORTED-FROM.md` (M7's Argon route, cherry-picked
  onto the coordinator branch as `033eb7ed23`, `0ceb2994c5`, `6874394d49`);
  the first commands list the diff and the dispatch comment names the
  expected files. The primary checkout is
  `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025).
  `worktrees.md`, `device-builds.md`, `CLAUDE.md` and `AGENTS.md` still name
  the legacy layout (`/workspace/repos/rocknix`, `rocknix.worktrees/`); #640
  owns that drift, and this brief's paths are the ones to use. The legacy
  checkout and every worktree beside it are the M7 lane's: read from them (a
  build root, a `.build-runs/` record, a diff), never write. The T1, T2 and
  T3 worktrees beside this one are other lanes': read with `git -C`, never
  write.
- **Model and effort:** Opus 5.5 at high effort (the maintainer, 2026-10-22:
  *"the work will be Opus 5.5"*), unless the dispatch says otherwise.
  Record what actually ran in `00-running-log.md`'s header.
- **Review depth: Extended** (plan § 6c: *"a security, state-preservation or
  launch-path slice"*; `slices.json`: *"`scripts/get_env`'s secret
  forwarding is on the security list"*, plan § 5's Security lens, *"code
  that handles credentials"*). The primary auditor is this lane (Anthropic).
  The two reviewers come from two other labs, each through the Facilitator
  and nothing else (D-WORKFLOW-049, D-WORKFLOW-137; `adversarial-council.md`
  rule 4; the code-auditor skill's Phase 4.6):
  - **GPT-6 Astra**: `tools/council/run invoke --member gpt --provider
    openrouter --prompt-file <brief> --output <file>` at `max`, the installed
    recipe (`openai/gpt-6-astra`, provider pinned to OpenAI).
  - **Gemini 4 Argon** (Google): `--member gemini-argon --provider
    openrouter` at `high`. **Its route is in this tree**: the coordinator
    branch carries M7's three commits (`fac2129787`, `1c7d283ad5`,
    `a7a3bdda4e` cherry-picked, #636/#638), so `grep -c gemini-argon
    scripts/council-invoke.ts tools/lint-audit-artifacts` prints `7` and `4`;
    T1 and T2 each ran the seat on 2026-10-23 (served `google/gemini-4-argon`
    by `Google`; T1's call about nine minutes). The roster's `--member
    gemini` is never called in its place. A seat that fails identity
    verification is recorded as pending, never replaced, and at Extended
    depth that is the Phase 4.6 blocker (§ 8). **`scripts/council-invoke.ts`
    and the rest of the council toolchain under `scripts/` are not this
    slice's paths** (they are `tooling-and-guards`, T10's; § 2): the lane
    runs them, reads nothing of them as a finding.
  - Both reviewers run the **refutation pass alone** (the audit is epic
    tier; phases.md § Phase 4.6: two calls at Milestone tier, one otherwise),
    each prepared independently. `second-opinions/review-plan.json` is
    written before the first call (`templates.md` § Second opinion: depth
    `extended`, primary `anthropic/claude-opus-5-5`, lab `anthropic`,
    identity source the dispatch comment and the session's own metadata,
    two reviewers). Every seat item is a lead; the orchestrator re-reads the
    artifact before a row is written. **The reviewers' briefs carry no
    credential-shaped line and no `.env` content**: a reviewer is handed the
    scripts' text and the recorded facts, never a value.
  - The runner's dependencies are not in a fresh worktree: `tools/council/run`
    execs `tools/council/node_modules/.bin/tsx`, and `node_modules/` is
    gitignored. Install once, before Phase 4.6, with `npm install --prefix
    tools/council` in the worktree (a gitignored write; the npm registry;
    `node` v24 and `npm` 11 are on the host; record the `tsx` version in
    `00-running-log.md`), then `tools/council/run verify-pins` must print its
    `OK` line and `tools/council/run test` must pass (T1 saw routing
    127/127). The key is sourced from `~/.config/council/env` (present, never
    read into a transcript, never on a command line). The dispatch comment
    on #652 is the authorization for exactly these two external calls plus a
    probe of each seat first, its provenance naming the served model.
    **During a host window of § 5 the install waits too**: it is not a
    compiler, but the agreement with the M7 lane says no new runtime of any
    kind until the return line.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-652
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-build-engine-652
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md   # the four files § 1 names; any other file is STALE
grep -c 'Renovation face' tools/lint-audit-artifacts; grep -c gemini-argon tools/lint-audit-artifacts   # both non-zero: the merged lint carries P1's renovation face and M7's Argon receipts
ls tools/renovation-inventory tools/renovation-status tools/renovation-drift docs/reviews/inventory.json docs/reviews/slices.json docs/reviews/build-path-read.md   # P1's and #644's, present because the branch is stacked on P1 and carries the coordinator's tip
git rev-parse --short upstream/next                                  # record it: Q4's upstream, fetched now
git merge-base next upstream/next                                    # c445081a59 on 2026-10-24; record it
git diff --quiet 8ebaf8daad HEAD -- scripts config distributions/ROCKNIX Makefile Dockerfile .gitignore .merge-head .github/workflows .github/ISSUE_TEMPLATE .github/pull_request_template.md .github/scripts && echo "slice bytes are next's at 8ebaf8daad" || echo "the slice's bytes differ from 8ebaf8daad: record the diff --stat and stop (§ 8)"
git push -u origin feature/m6-build-engine-652                       # the lane's own branch, at the coordinator's merge until the first commit
test -f docs/reviews/briefs/build-engine.md || { echo "the brief is not in this tree: stop"; exit 1; }
test -f docs/futros/2026-10-24-m6-build-engine.md || echo "the epic's futro is not in this tree: ask the coordinator before the first audit commit"
cat .github/sessions/saved-session-state-feature-m6-build-engine-652.md   # the lane's seeded pointer
tail -5 /tmp/m7-m6-host-coordination-20261023.txt                   # the host's state (§ 5): a window open means no runtime
```

The order of the first session: § 3's reading first (it is the pre-flight,
`working-principles.md`; it fills the first hour), then stage A.

## 2. Scope

**242 paths of the distribution, 13,910 lines; the fork's own lines and the
engine's own scripts read line by line, the rest at Q4 and Q6 first.** The
membership is the inventory's, with the slice's one rule of `slices.json`
(`k: 5`) applied as `tools/renovation-inventory --order` applies it: the
rows of the slice's own area, `build-engine`, under the globs `scripts/**`,
`config/**`, `distributions/ROCKNIX/**`, `Makefile`, `Dockerfile`,
`.gitignore`, `.merge-head`, `.github/**`. **The area filter is the whole
point**: the globs alone would sweep in the council toolchain under
`scripts/` (46 paths, `tooling-and-guards`, T10's), the fork's own CI
workflows (`.github/workflows/fork-*.yml`, 6 paths, T10's) and every
`.github/sessions/**` checkpoint (353 paths, the `records` area). #652 says
the same set as `--order`'s membership; the filter below is the
re-derivation, because `--order` writes files (and `--slice-issues <dir>`
writes forty-six issue bodies into that directory: never run either in a
worktree you keep).

**The hash.** The slice's bytes are `next`'s at **`8ebaf8daad`** (the same
hash T1, T2 and T3 read at; `next` has not moved since the survey).
**`reviewed-at:` is the branch's `HEAD` at stage A** (the commit the read is
made at), recorded in `00-running-log.md` and `01-research-notes.md` § Scope.
The stop (§ 8) is the slice's bytes differing from `8ebaf8daad` at stage A:
then the slice was re-based under the read and the coordinator re-baselines
it. `next` moving later is not a stop; it is drift, § 2's last paragraph.

**The counts, recorded by the survey at `eb4763e3cc` and re-derived here.**
A count that differs is a delta beside the recorded one, not a stop; the
stop is a count that cannot be produced, or two commands for one quantity
that disagree. The inventory's line count is git's numstat against the
empty tree (`docs/reviews/README.md`):

```bash
python3 -I - <<'PY'
import json, re, collections
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
globs = ["scripts/**", "config/**", "distributions/ROCKNIX/**", "Makefile", "Dockerfile", ".gitignore", ".merge-head", ".github/**"]
def gm(p, g): return re.fullmatch(re.escape(g).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*"), p) is not None
t5 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "build-engine" and any(gm(r["path"], g) for g in globs)]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
CODE = {"shell", "python", "yaml", "recipe", "cmake", "udev", "systemd"}
print("paths", len(t5), "lines", L(t5), dict(collections.Counter(r["tier"] for r in t5)))
print("fork-own lines", L([r for r in t5 if r["tier"] == "fork-own"]), "| code-class lines", L([r for r in t5 if r["language"] in CODE]), "| of which fork-own", L([r for r in t5 if r["language"] in CODE and r["tier"] == "fork-own"]))
print("by language", dict(collections.Counter(r["language"] for r in t5)))
print("by directory", collections.Counter("/".join(r["path"].split("/")[:2]) if "/" in r["path"] else r["path"] for r in t5).most_common(12))
for r in sorted((r for r in t5 if r["tier"] == "fork-own"), key=lambda r: -(r["lines"] or 0)): print(r["lines"], r["language"], r["reach"], r["path"])
PY
git ls-files scripts config distributions/ROCKNIX Makefile Dockerfile .gitignore .merge-head .github/workflows .github/ISSUE_TEMPLATE .github/pull_request_template.md .github/scripts | wc -l   # more than 242: the council scripts under scripts/ and the fork-* workflows are T10's; list the difference
```

Recorded (the coordinator's run of this filter on 2026-10-24 against the
P1 tip's `inventory.json`): **242 paths, 13,910 lines; 18 fork-own paths,
3,266 lines; 224 upstream-carried, no vendor-carried row.** The order's row
prints `242 paths 13,910 lines 6,776 (2,419)`: its 6,776 is the inventory's
code classes summed whatever their tier (the tool's `read_lines`, line 999:
`recipe`, `shell`, `python`, `yaml`, `cmake`, `udev`, `systemd`) and the
2,419 the fork-own part of those; the 139 `config/emulators/*.conf` system
fragments, `config/functions` (1,936 lines, classed `none`), the
`config/arch.*` files and the `distributions/ROCKNIX` configuration are
outside the tool's `read` and inside this brief's (the lane states the
three figures beside its own). **By language:** `config` 139 files, `shell`
30, `yaml` 19, `none` 12, `image` 11 and the rest. **By directory:**
`config/emulators` 139 (the system fragments T3's launch table sources),
`.github/workflows` 19 (upstream's workflows as the fork carries them;
`validate-pull-request.yml` and `check-freeze-period.yml` are fork-own
edits), `config/noobs` 15, `config/addon` 7, `config/docker` 7,
`distributions/ROCKNIX` 5 (`config/functions` 400 fork-own, `options` 219
fork-own, `version` 11 fork-own, `kernel_options` 0 lines, and one more the
filter lists), `scripts/` 30 files 5,834 lines, `config/` 13 top-level
files, `.github/ISSUE_TEMPLATE` 2, `.github/pull_request_template.md`,
`.github/scripts` 2, and the five top-level files. **Not in the membership,
read only where the engine points at them:** the council toolchain under
`scripts/` (`council-*`, `lib/council-*`, `lint-council-*`, `verify-*`,
`write-step-seal.ts`, `owner-queue-lint.mjs`, `build-council-prompt.ts`,
`check-stale-blob-drift.ts`, `forge-write-status.mjs`,
`setup-council-mistral-tokenizer.mjs`, `__tests__/`: T10's); the fork's CI
`fork-checks.yml`, `fork-generic-x64.yml`, `fork-mirror-build-container.yml`,
`fork-wordlist.yml` and `.githooks/**` (T10's); `.github/sessions/**` (the
`records` area, nobody's slice); `tools/**` -- `tools/pkgcheck` (fork-own,
`build-engine` area, T6's by its `tools/**` glob), `tools/watch-build`,
`tools/watch-build-submit`, `tools/watch-job`, `tools/build-preflight`,
`tools/host-maintenance/**` (T9's, `tooling-build-supervision`: the watcher
the engine's entry points exec into, the admission the Makefile's targets
require, the swap helper), `tools/build-identity-test` (T9's area, though
it tests this slice's `config/build-identity`: run it, § 5);
`distributions/LibreELEC/**` and `distributions/LEIoT/**` (T6's, unreached);
`packages/**` and `projects/**` (the recipes the engine builds: T7, T8 and
the device slices; `packages/README.md` is read as the contract the engine
promises them).

**Where the code runs.** Nothing here ships on an image except what
`scripts/image` writes into it: `/etc/os-release`'s `BUILD_ID`,
`BUILD_BRANCH`, `BUILD_VERSION` and `BUILDER_VERSION` (the identity,
`config/build-identity` called at `scripts/image` 74 to 75), and the
`/etc/emulationstation/es_systems.cfg` and its document that
`distributions/ROCKNIX/config/functions`'s `mk_es_systems` and
`mk_system_doc` write when the `emulators` metapackage installs (T3's
caller, this slice's functions). Everything else runs **on the build host or
in the build container**: `make <DEVICE>` and `make docker-<DEVICE>`
(`Makefile`; the Docker targets pull the fork's mirror by digest, line 205
to 208, write `.env` owner-only through `scripts/get_env` and remove it on
exit, lines 138 to 195); every native entry point execs into
`tools/watch-build` first (`scripts/build` 9, `scripts/image` 9,
`scripts/install` 10, `scripts/build_distro` 11, `scripts/build_compat` 7:
the `RASTERATOPS_WATCH_EXEC` marker, D-WORKFLOW-142; `scripts/build_mt` and
`scripts/clean` do not, #644's finding 6, T9's); `scripts/build` configures,
builds and installs one package through the hooks `packages/README.md`
documents, with `--wrap-mode=nodownload` on every meson configure (lines
185 and 196, #226, blindspot 47) and `calculate_stamp` (`config/functions`
961) deciding whether a package rebuilds by hashing its `PKG_DIR`
(`device-builds.md` § After rebasing onto upstream, item 3: an override that
sources the generic recipe is never invalidated by the generic file's
change); `scripts/build_distro` builds a device's whole set;
`scripts/image` assembles the image (identity 60 to 75, the `target/`
collision refusal at 139 to 168); `scripts/install` copies a package's
install tree; `scripts/mkimage` writes the disk image; `scripts/unpack`,
`get`, `get_git`, `get_archive`, `get_file`, `extract`, `autoreconf`,
`checkdeps`, `pkgbuild`, `pkgjson`, `pkgbuilder.py`, `genbuildplan.py`,
`uboot_helper`, `create_addon`, `install_addon`, `create_docker_package`,
`update_packages`, `autoremove`, `ccache_stats`, `makefile_helper`,
`build_mt`, `clean` are the rest, each with its callers to find (Q6).
`config/options` is sourced by every script (the layered resolution
`CLAUDE.md` § Architecture describes: distribution, project, device, arch;
ccache at 91 to 118, `SOURCES_DIR` and `DISTRO_MIRROR` at 142 to 151);
`config/path` sets `TARGET_IMG` (`target/`, line 10), `SOURCES` (13) and the
build roots. The 19 upstream workflows under `.github/workflows/` run on
GitHub against the fork's repository (all active; `Build` ends
`startup_failure` daily, #644's finding 19 with T10); the fork builds
locally and nothing from CI is published (D-WORKFLOW-120).

**Five groups, read in this order** (the slice's reason to be fifth is
D-WORKFLOW-186: the engine before anything it builds; plan § 6a). Line
numbers are `next`'s at `8ebaf8daad`, from a read-only seam map the
coordinator made on 2026-10-24; each is a lead to re-read, not a verdict:

1. **The fork's own engine lines** (18 fork-own paths, read whole first):
   `scripts/build` (646; +12 against upstream: the watch entry 9 to 12 and
   `--wrap-mode=nodownload` at 185 and 196), `scripts/image` (481; +63/-54:
   the watch entry, the identity at 60 to 75 and 139 to 168 --
   `BUILD_TIMESTAMP`, `IMAGE_SUFFIX`, the refusal of an existing identity in
   `target/`, the `.identity.json` sidecar, D-WORKFLOW-157/159),
   `scripts/install` (196; +6, the watch entry), `scripts/build_distro`
   (106; +17/-11), `scripts/build_compat` (103; +6), `scripts/extract` (84;
   +1/-1), **`scripts/get_env` (22; +19/-2: the `KEEP` and `DROP` name
   patterns at 14 and 15 that decide which exported variables reach `.env`
   and the container; its own comment says a secret under an innocent name
   still leaks; D-INFRA-006; #644's finding 3)**, `Makefile` (208; +42/-7:
   the watch entry at 40, the `.env` lifecycle at 138 to 195, the container
   digest `sha256:988c0ba5…` and `ghcr.io/pixelelated/build` at 205 to 208;
   #644's findings 1, 2, 4), `config/build-identity` (44, new:
   `pixelelated_build_identity`, the MAJOR.MINOR.PATCH and `BUILD_QUALIFIER`
   rules, D-WORKFLOW-157/159, #532), `config/graphic` (168; +7/-1: the
   GL/GLES/Vulkan support flags every recipe reads), `config/show_config`
   (160; +1/-5), `distributions/ROCKNIX/config/functions` (400; +7/-1:
   `add_emu_doc` 50, `mk_system_doc` 64, `clean_es_cache` 80, `add_emu_core`
   88, `mk_es_systems` 99 with its `ls | sort` concatenation and its
   `xmlstarlet fo -t ... 2>/dev/null`, `add_system_dir` 117, `add_es_system`
   127 with `RUNCMD` at 128 and the `SYSTEM_COMMAND` default at 138 to 141 --
   T3's lead on the silenced formatter is **this slice's** to judge and fix),
   `distributions/ROCKNIX/options` (219; +9/-6: `DISTRONAME="pixelelated"`
   at 17, `DISTRO_VERSION="devel"`), `distributions/ROCKNIX/version` (11;
   +9/-3: `OS_VERSION="0.0.1"`, the `BUILD_QUALIFIER` comment,
   `IMAGE_SUFFIX="from-ROCKNIX"`, D-WORKFLOW-128), `.gitignore` (84),
   `.github/workflows/validate-pull-request.yml` (121) and
   `check-freeze-period.yml` (63) (both edited to `ubuntu` runners, #644's
   finding 19), and **`scripts/test-audit-review.py` (150; the code-auditor
   skill's own test script, classed into this area by the `scripts/**` glob:
   read it once to say so, a Q6 row, and the misfiling is a lead for the
   coordinator's `areas.json`, not this lane's edit)**. **The fork's 31
   commits on the membership since the merge base `c445081a59`** are the
   history of these lines (`git log --oneline c445081a59..8ebaf8daad -- <the
   membership's paths>`; the identity series `f10eec1306`, `40bc5469b9`; the
   watcher `1aac875e88`; the admission `d7e2d6be41`; the container pin
   `2c349c6d51`, `440ad22b68`, `a79b7f82a5`, `67cd0e6493`; the ARM
   compatibility root `43d0bc3bf4`; the lowercase identity `a9af618398`;
   the frozen source during documentation `5e2509a25a`); each fork line is
   read with its commit (`engineering-practices.md` § Verify design intent).
2. **The engine's upstream-carried core** (read whole; the fork runs every
   line of it on every build): `config/functions` (1,936 lines: the build
   helpers every recipe and script calls -- `calculate_stamp` 961,
   `get_pkg_version` 991, `get_pkg_directory` 1057, `enable_service` 1109,
   `die` 1700, the `LIBTOOLIZE`/`AUTOCONF` exports `device-builds.md` § After
   rebasing names at 6), `config/options` (197), `config/path` (105),
   `config/arch.{arm,aarch64,x86_64}` (87, 46, 22), `config/optimize` (102),
   `config/multithread` (72), `config/sources` (2), `config/blocklist` (29;
   still names `aethersx2-sa`, which upstream dropped in `c4d353449e`:
   Q4), `scripts/mkimage` (334), `unpack` (228), `get_git` (239), `get`
   (57), `get_archive` (59), `get_file` (6), `pkgbuild` (79), `pkgbuilder.py`
   (933: CI's parallel builder), `genbuildplan.py` (396: CI's staged graph),
   `uboot_helper` (586), `checkdeps` (345), `autoreconf` (36),
   `makefile_helper` (33), `clean` (51), `build_mt` (16), `autoremove` (18),
   `ccache_stats` (9), `update_packages` (82: `make update`), `pkgjson` (56),
   `create_addon` (207), `install_addon` (92), `create_docker_package` (184),
   `Dockerfile` (50: the build container upstream rebuilds from on every CI
   run and the fork mirrors by digest), `.merge-head` (one hash:
   `d43d166b7a…`; what reads it is a Q6 row).
3. **The system fragments** (139 `config/emulators/*.conf`, upstream-carried,
   10 keys each -- `SYSTEM_NAME`, `SYSTEM_FULLNAME`, `SYSTEM_MANUFACTURER`,
   `SYSTEM_RELEASE`, `SYSTEM_HARDWARE`, `SYSTEM_PATH`, `SYSTEM_EXTENSION`,
   `SYSTEM_PLATFORM`, `SYSTEM_THEME`, `SYSTEM_WIKI_PATH`; three set
   `SYSTEM_COMMAND`; one lacks `SYSTEM_NAME`, two lack `SYSTEM_RELEASE` and
   `SYSTEM_WIKI_PATH`): what `add_es_system` sources for each system T3's
   metapackage names. Read at Q4 and Q6: which fragments the five built
   devices' tables use (T3's Q6 lists the systems; the cross-check is a
   diff of names), which keys the interface reads (T2's `SystemData` rows),
   and the three `SYSTEM_COMMAND` overrides against the launch line.
4. **The other configuration trees** (`config/noobs/**` 15, `config/addon/**`
   7, `config/docker/**` 7): Raspberry Pi NOOBS, Kodi add-ons and the
   container recipe scaffolding the fork inherits; Q6 first (what reaches a
   fork image or a fork build: the five devices build no NOOBS and no
   add-on), a row each with `Already written:` where a removal is proposed
   (D-WORKFLOW-185's shape: unshipped is not dead when upstream reaches it;
   the fork merges upstream through these files).
5. **The workflows and templates** (19 upstream workflows the fork carries
   active -- `build-nightly.yml` 336 lines, the `build-aarch64-*` series,
   `build-device.yml`, `build-docker-image.yml`, `check-freeze-period.yml`,
   `retry-workflow.yml`, `trigger-fail-if-upstream-changed.yml`,
   `update-kernel-configs-docs.yml`, `update-mirror-sources.yml`,
   `validate-pull-request.yml`; `.github/ISSUE_TEMPLATE/`,
   `pull_request_template.md`, `.github/scripts/generate-*.sh`): #644's
   findings 18 to 21 name their state (all active on the fork; the daily
   `Build` fails at startup; the fork publishes nothing from CI). Q6 and Q4
   first, with T10 (the fork's own CI) as the neighbour: this slice says
   what each upstream workflow would do on the fork and whether anything
   reaches it; T10 decides the fork's gates.

**Upstream's side of Q4, at the first commands' fetch:** 4 commits of
`c445081a59..upstream/next` touch the membership (2026-10-24: `c4d353449e`
aethersx2 dropped for licensing -- `config/blocklist`; `71d8932b33` openabl
introduced; `76693a738d` the GitHub username in the release workflow;
`c200cc906d` the pull request template), against the fork's 31. **The
pinned build container** is the slice's other currency question: the
Makefile pins `ghcr.io/pixelelated/build@sha256:988c0ba5…`, a mirror of
upstream's image of 2026-09-25, while upstream's CI rebuilds
`ghcr.io/rocknix/rocknix-build:latest` from the unchanged `Dockerfile` on
every run (#644's finding 1: *"refresh the mirror from upstream's current
digest as its first act and say when the pin moves"* -- the refresh is the
coordinator's act, § 1; this lane records the two digests and their dates).
**The closed `bug` issues** that name an engine script are Phase 1's: `gh
issue list --repo pixelelated/distribution --label bug --state closed --limit
500 --json number,title,body`, grepped with word boundaries for
`scripts/build`, `scripts/image`, `get_env`, `calculate_stamp`, `mkimage`,
`build_distro`, `Makefile`, `.env`, `wrap-mode`, `build-identity` (the count
depends on the pattern, so record the pattern with the count).

**The branch scan**, by one predicate: a branch is *ahead* of `next` on the
membership when `git log --oneline next..<branch> -- <the membership's
paths>` prints a line. Record the predicate, the command and the list in
`01-research-notes.md`; a branch ahead of `next` on a slice path is a lead
for the coordinator, posted on #652, not a reason to read it.

**The M7 lane's unmerged delta (`next..069fc2704421` in the legacy
checkout, read-only):** on the membership's paths, **none** on 2026-10-24
(the one M7 commit under `.github/` touches `.github/sessions/**`, the
`records` area). The engine the M7 candidate builds with is the engine at
`8ebaf8daad`. If the fetch at stage A shows otherwise, the delta is listed
hunk by hunk in `01-research-notes.md` and announced on #652.

**Drift.** `next` is `8ebaf8daad` and has not moved since the survey; the
M7 candidate's merge will move it. When it does, the coordinator merges
`next` into this branch -- never between stage A and stage D (the read must
stay a fact about one hash, plan § 8); after stage D a merge re-baselines
the slice over the diff, recorded on #652. `tools/renovation-drift` is the
coordinator's at every slice close; this lane runs it to read, never to
write.

## 3. Read first

From `next`, in this order, before any analysis (this is the first
session's first hour; stage A follows it):

- `.github/sessions/saved-session-state-next.md` (the M7 lane's canonical
  checkpoint; read for what runs on this host, not for a work queue) and
  this lane's own pointer.
- **`docs/reviews/build-path-read.md` whole** (#644, the coordinator's
  read of ROCKNIX's documented build path against the fork's, 2026-10-23):
  § 1 the upstream pages read (`contribute/build/`, `build-gh/`, `modify/`,
  `packages/`, `contribute/`) with their dates, § 2 and § 3 the two paths,
  § 4 the 26 findings with carriers, § 5 what was verified by command.
  **The nine this slice carries, each a row in `02-forward-audit.md`'s
  findings with its disposition:** 1 (the container pin four weeks behind
  upstream's `latest`: record both digests and dates; the refresh is the
  coordinator's), 3 (the guide's `LOCAL_SSH_KEYS_FILE` and `LOCAL_WIFI_KEY`
  do not reach the container through `get_env`'s DROP: a sentence in
  `device-builds.md` § Build credentials or a `get_env` comment; no code
  change), 4 (`BUILDER_VERSION` into `/etc/os-release`: keep), 8 (compare
  `config/options`' `CCACHE_COMPRESSLEVEL=0` and `CCACHE_SLOPPINESS` with
  CI's `6` and its `include_file_*` additions, and decide with a
  measurement from a recorded run, never a build of this lane's), 9 (CI
  cleans `retroarch` and `emulationstation` before the final image because
  its base stage lacks 32-bit support and credentials: note it so nobody
  imports the step), 10 (`--wrap-mode=nodownload`: keep; #585's candidate
  contribution), 11 (the fork downloads from ROCKNIX's `DISTRO_MIRROR` and
  carries the mirror workflow: record the dependency; a mirror of our own is
  the maintainer's call only if upstream's goes away), 13 (the identity:
  keep; T9 reads `tools/build-identity-test`, this lane runs it, § 5), 22
  (the credentials' path from `~/.ROCKNIX/options` through `.env` by name:
  keep). The other seventeen are named with their carriers so this lane
  does not take them (2, 5, 14 T4; 6, 7 T9; 12, 23 T11 and T12; 15, 16 T7
  and T8; 17, 18 #645; 19, 21 T10; 20 #637's lane; 24 T6; 25 T32; 26 #585).
- The code-auditor skill whole: `.claude/skills/code-auditor/SKILL.md` and
  its `references/phases.md`, `review-levels.md`, `templates.md`,
  `anti-patterns.md`. The slice runs under its lifecycle with the renovation
  face added (plan § 6b); stage B's Phase 2 criteria are #652's checklist,
  and Phase 3 carries § 4 below as its renovation face beside the skill's
  own faces.
- `packages/README.md` whole: the contract the engine promises every recipe
  (the hooks `scripts/build` calls and in what order, late binding, the
  `PKG_*` fields `config/functions` reads, `PKG_SHA256`, the patch
  directories), and `packaging-and-patches.md`.
- Rules whose `paths:` match or whose subject is this slice: **`device-builds.md`
  whole** (§ The build command and `DOCKER_EXTRA_OPTS`; § Temporary
  directories belong to their execution environment, #549; § After rebasing
  onto upstream, items 1 to 3 -- the libtool clobber and the stale-stamp
  trap in `calculate_stamp`; § A metadata-only upstream change still
  rebuilds everything; § Late binding bites hardest in a merge; § A killed
  build poisons every package that was in flight; § A build that fetches its
  own dependency; § A link error the source contradicts is the compile
  cache's; § Verify helpers with the interpreter that will run them, #492;
  § A two-minute build can be a real one; § Before a build: the machine is
  memory-bound -- the watcher, the admission, the result-file ownership #597;
  § Budget; § Build credentials, D-INFRA-006/007, D-WORKFLOW-166;
  § Publishing, D-WORKFLOW-157/159 and `tools/rc-preflight`; § Iterating on
  EmulationStation for `EMULATIONSTATION_SRC`'s mount), `engineering-practices.md`
  (§ A promise is not a mechanism and its watch-build paragraphs,
  D-WORKFLOW-141/142/143/148; § Guards must fail closed; § Verify design
  intent; § Verify the artifact; § A name is not a behaviour; § Check
  upstream early, D-WORKFLOW-162; § Consider contributing every applicable
  fix upstream, D-WORKFLOW-164/165), `generic-x64-vm-testing.md` (§ Building
  the GENERIC_X64 image, for what `scripts/image` and `mkimage` produce for
  the VM; the `.update` path), `upgrade-and-install.md` (every fix answers
  *Already written*, D-WORKFLOW-050: the engine writes `/etc/os-release`,
  the identity sidecars and `target/`'s names, and every image already
  built carries the previous shape), `fork-workflow.md` (the personal paths
  that never reach upstream; `.githooks/pre-push`'s content rule; the PR
  recipe), `worktrees.md` (§ Build worktrees are on `build/*` branches;
  `BUILD_BRANCH` from `git branch --show-current`; § One builder per build
  worktree; § Review retention after qualification, D-INFRA-018/021/022/023),
  `change-log.md`, `release-candidates.md` (step 0's `rc-preflight`, the
  build inventory). Then the every-session set: `bugs-are-agent-first.md`,
  `vm-first.md`, `issue-tracking.md`, `decision-register.md`,
  `learning-capture.md`, `ceremonies.md`, `milestone-phase-naming.md`,
  `adversarial-council.md`, `working-principles.md` (§ Pre-flight: say
  which rules were read), `instruction-files.md` (the fork's tools and
  which rule documents each). Known stale facts so they do not cost an hour
  (#640): the legacy paths in `worktrees.md`, `device-builds.md`,
  `instruction-files.md`, `AGENTS.md`; `CLAUDE.md`'s `OS_VERSION/BUILD_DATE`
  sentence (#644's finding 14: only `BUILD_DATE` is honoured and the fork
  defaults it; T4 corrects the sentence).
- `docs/blindspot-register.md` whole, once (74 entries). The entries that
  touch the engine: **14** (a hook is proven by a constructed failure),
  **26** (`core.hooksPath` naming a directory that no longer exists runs
  nothing), **47** (pango fetched its own cairo: `--wrap-mode=nodownload`),
  **48** (an option changed without reading the log: four webkitgtk builds),
  **49** (an edit made blind to the compiler), **73** (a monitor of
  completion, not activity: `watch-job --build-progress`), **74** (a fixture
  or a stub that silently did not engage); and the general ones a reading
  repeats: 7 (host tools are not the device's), 13 (assumed done), 30 (a
  resumed session built on its own summary), 39 (a suite that passed over
  a table of dashes), 46 (a name read as a behaviour), 51 (an open checkbox
  is a claim).
- Prior audits under `docs/audits/`, **as provenance only**: which engine
  files were audited, when, at what tier; read after stage B's own Phase 2
  is written, compared then, never transcribed (plan § 7 item 3). The punch
  lists that name them, counted with `grep -c -E
  'scripts/(build|image|install|mkimage|get_env|build_distro)|config/(functions|options|build-identity)|Makefile|\.env|wrap-mode' 05-punch-list.md`
  (the lane records the count per folder with the command). **T1's, T2's and
  T3's artifacts are provenance too**, on their branches (`git -C <worktree>
  show <tip>:<path>`; T1 `d3aa6a19c5`, T2 `7041b0d710`, T3's tip on #650 at
  the time): T1's `02` § Mechanical checks records `pkgcheck rocknix` and
  the harness under the image's busybox, the engine's consumers' view; T3's
  `01` and `04` carry the launch table this slice's functions write and
  whatever lead T3 posted on `mk_es_systems`.
- Decisions by ID, cited and never re-argued. The engine: **D-INFRA-006 and
  D-INFRA-007** (build credentials live only in `~/.ROCKNIX/options`, 0600;
  the line is who can download the image), **D-WORKFLOW-166** (the shared
  ScreenScraper developer identity, #566), **D-WORKFLOW-119 and
  D-WORKFLOW-120** (the runner trust boundary; no CI image is ever attached
  to a Release; candidates in the immutable store), **D-WORKFLOW-128** (the
  adoption tar's `from-ROCKNIX` suffix), **D-WORKFLOW-157 and D-WORKFLOW-159**
  (the identity: version, UTC timestamp, commit; the two public rolling
  forms, #532), **D-WORKFLOW-141, 142, 143, 148** (the watcher observes
  activity; every build enters the shared runner; completion must reach the
  maintainer; durable submission), **D-INFRA-015, 018, 021, 022, 023**
  (swap reclamation; retention review; artifacts temporary; measure peaks),
  **D-INFRA-025** (the fresh clone), D-WORKFLOW-024 (a package the fork
  introduces at its latest release or the recipe says why), D-WORKFLOW-047
  (the release-candidate procedure, step 0), D-WORKFLOW-050 (*Already
  written*), D-QA-022, D-QA-057. The program: D-WORKFLOW-181, 183, 184,
  185, 186 (the maintainer's weight on the build process: the order's
  reason), 187, 188 (the order's fourth version, on the P1 branch), 189,
  190; D-WORKFLOW-137 (depth and the reviewer's lab), D-WORKFLOW-049 (every
  seat through the Facilitator), D-WORKFLOW-162 (check upstream early:
  ROCKNIX's `distribution` PRs and LibreELEC's for the engine; LibreELEC is
  the engine's upstream's upstream, `config/functions`' header says so),
  D-WORKFLOW-164/165 (consider contributing a fix upstream; submissions
  deferred; #585 is the queue), D-WORKFLOW-132 and D-QA-012, D-WORKFLOW-149,
  D-QA-007/015, D-QA-021, D-QA-044/045/051. `grep -iE
  'scripts/(build|image)|get_env|Makefile|build-identity|calculate_stamp|watch-build|admission'
  docs/decision-register.md` names the rows on 2026-10-24; the lane records
  the count with the command.
- Issues whose bodies name these files, read for the planned changes and
  the known leads, not as a work queue. **Open:** #644 (the read this
  slice carries nine findings of), #645 (upstream refuses PRs touching
  `packages/`; the fork's 21 files there cannot go upstream: #645's and
  T8's, not this slice's), #653 (T6, the area's other slice), #656 (T9,
  build supervision: the watcher and the admission this engine execs
  into), #493 (build storage and admission), #635 and #634 (memory
  admission; swap to 32 GiB), #395 (watcher alerts while disconnected),
  #233 (a self-hosted QA runner), #532 (identity, `tools/build-identity-test`),
  #528 (release component licences and corresponding source: what
  `scripts/image` would have to carry), #549 (TMPDIR in the container),
  #412 and #413 (`watch-job --build-progress`), #228 (webkitgtk held at
  2.52.6; the compile cache's PCH), #585 (the upstream contribution queue:
  `--wrap-mode=nodownload` is its candidate), #640 (the legacy paths in the
  rules), #650 (T3, beside this lane: its lead on `mk_es_systems`'s silenced
  formatter is this slice's function). **Closed, read for their history on
  these files:** #226 (pango's fetched cairo), #227 (`fork-package-freshness`),
  #492 (the helper verified with the container's interpreter), #394
  (`watch-build`), #393 (`watch-job`'s activity dir), #444 (`watch-build-submit`),
  #410 (`build-preflight --reclaim-swap`), #461 (the retention planner),
  #307 and #312 (the credential and wordlist guards the `.env` work sits
  beside), #16 (the GENERIC_X64 build). Every `gh` call carries `--repo
  pixelelated/distribution`.

## 4. The questions

All seven apply to this slice (plan § 4); none is struck. Provenance decides
the lens (plan § 3): the 18 fork-own paths get all seven in full; the
upstream-carried **engine core** (group 2) gets all seven too, because the
fork runs every line of it on every build and *"there is no longer anyone
to send them to"* (#339's Tier 2 words) -- a defect there is this program's
to fix, a Q1 or Q7 item there is recorded with `Renovation` and its upstream
named for #585; the **fragments, the other configuration trees and the
workflows** (groups 3 to 5) get **Q4 and Q6 first**, and the rest only where
the file stays and a lead points at it (an upstream-carried fragment's Q1,
Q2, Q3 and Q7 cells may read `n/a: upstream's, unchanged here`, and
criterion 7 accepts that cell). Per file, the evidence that answers each:

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | A shell idiom the rest of the tree has moved past: `[ $? -eq 0 ] && ... \|\| exit 1` where `set -e` or `die` already fails the build; `eval` and word-splitting where arrays exist; `ls` in a loop (`mk_es_systems` 106); `2>/dev/null` over a formatter that can fail (`mk_es_systems` 113); a Python 2 remnant or hand-rolled parsing in `pkgbuilder.py`, `genbuildplan.py`, `uboot_helper`; a Makefile recipe repeated per target where a pattern rule exists; a workflow pinned to a retired runner label or action version | the replacement named with its commit or its upstream line; `shellcheck`'s line read at its site (§ 5) |
| Q2 Standards | The rules § 3 names, cited by section: `engineering-practices.md` § Guards must fail closed on every pipeline, test and exit path in the 30 scripts (`set -o pipefail`, quoted expansions, a positive assertion over an absent error); `device-builds.md` on what the engine promises the watcher and the admission (the `RASTERATOPS_WATCH_EXEC` marker, the entry points that carry it and the two that do not, #644 finding 6); D-INFRA-006 on the `.env` lifecycle (`scripts/get_env`'s name patterns; the Makefile's owner-only write and exit removal; what `.env` holds at rest in a worktree); `packages/README.md` on the hook order `scripts/build` honours; `fork-workflow.md` on which of these files are personal paths (none: the engine goes upstream) and `.githooks/pre-push`'s content rule | the rule and section cited; the test or trace per guard; the `.env` lifecycle traced in the Makefile's recipe lines with their numbers |
| Q3 Bugs | Where each unit fails: `calculate_stamp` hashing `PKG_DIR` so a generic recipe's change never invalidates an override that sources it (`device-builds.md` § After rebasing, item 3: 53 ROCKNIX packages use the pattern -- a defect in the engine, or a documented limit, decided with a sandboxed call of the function over a fixture tree); `get_env`'s DROP by name (a secret under an innocent name reaches the container: the comment says so; is the fix a value-shape check, an allowlist, or the documented limit?); the `.env` left behind when a recipe fails before its removal (`67cd0e6493` says what happens); `scripts/image`'s refusal of a duplicate identity and what a same-day rebuild does (D-WORKFLOW-157); `mk_es_systems`'s empty table on a formatter error (T3's lead; the fix is this slice's, proven by the host regeneration § 5); `mkimage`'s partition arithmetic for the GENERIC_X64 16 GB rule; the TMPDIR trap (#549); a workflow that assumes a secret the fork does not hold (the daily `startup_failure`) | a reproduction in a sandbox (the function sourced with scratch variables), a recorded run's log (`.build-runs/<id>/build.log` in an M7 worktree, read-only), or a trace with file:line; the code-auditor evidence floor applies (host reasoning about a build's behaviour is a lead until a recorded run or a sandboxed call shows it) |
| Q4 Package currency | Two readings, each a table in `04`: (a) **the fork against ROCKNIX**: the 4 commits of `c445081a59..upstream/next` on the membership dispositioned one by one (merged already / not applicable to this fork / to merge, with the reason; `config/blocklist`'s `aethersx2-sa` among them), plus every membership file that differs textually from `upstream/next` (`git diff --stat upstream/next 8ebaf8daad -- <the membership>`), each difference named as the fork's (with its commit) or upstream's (with its commit); (b) **the build container**: the Makefile's pinned digest and its date against upstream's current `ghcr.io/rocknix/rocknix-build:latest` digest and date (`gh api` or `docker manifest inspect` without a pull, if the host has a token for GHCR; else the registry's public manifest; never a pull during a host window), the `Dockerfile` here against upstream's, and what changed in the container between the two dates as far as the registry's labels and upstream's commits say; the refresh itself is the coordinator's, recorded as `to merge` | the two tables with their commands and dates; the fetch's hash recorded; `tools/fork-package-freshness --list` run once to show it covers nothing here (the engine introduces no package) |
| Q5 Efficiency | What the engine costs a build and the host: the ccache settings (`config/options` 91 to 118) against CI's (#644 finding 8), decided from recorded runs' `ccache_stats` and the `.build-runs/` logs the M7 worktrees hold, never a build of this lane's; `calculate_stamp`'s granularity (a whole-directory hash: a metadata-only change rebuilds the package, `device-builds.md` § A metadata-only upstream change), with the count of packages a `PKG_SHA256` sweep would rebuild as the measure; the watch entry's overhead per entry point (one exec and a lock); `CONCURRENCY_MAKE_LEVEL` and the per-package `-j` caps as the host's memory rule; image assembly's steps and their times from a recorded `scripts/image` run; what the engine costs the player: nothing at run time except the identity read by `rocknix-info` | a recorded run's timings (`build.start`, `build.status`, `build.log` in an M7 `.build-runs/<id>/`), the ccache statistics a root's `.ccache/` reports read-only, or the named absence of a measurement |
| Q6 Dead ends | Is each unit reached: **by a fork build** (which of the 30 scripts the Makefile, `scripts/build_distro`, `scripts/build`, `scripts/image`, the workflows and `tools/watch-build` call -- `git grep -n -F -e "scripts/<name>" -e "SCRIPTS}/<name>" -e "/<name> "` for each, the hits listed; `genbuildplan.py` and `pkgbuilder.py` are CI's builder, `create_addon`, `install_addon`, `create_docker_package`, `pkgjson`, `uboot_helper`, `ccache_stats`, `makefile_helper`, `update_packages` are each a row; `.merge-head`'s reader; `config/noobs`, `config/addon`, `config/docker` against the five devices' options), **by a fork image** (what `scripts/image` writes that a device reads: the identity, the `es_systems.cfg` and its document), **by the fork's CI** (each of the 19 upstream workflows: its trigger, whether it runs on the fork, what it would need -- a secret, a runner, a PAT -- and whether anything reads its result; `Build`'s daily `startup_failure` is a row), and the 139 fragments against the systems the five devices' tables name (T3's list); the misfiled `scripts/test-audit-review.py` | the reachability tables in `04` Q6: one row per script (30) with its callers, one per workflow (19), one per configuration tree (3), one per fragment (139) with the devices whose table names it, one for `.merge-head`; the search commands and their output; every row marked unreached by any fork build, image or CI carries an `Already written:` line and what the unit exposed |
| Q7 Clarity | Can a reader new to it tell what each unit does and why in one pass: `config/functions` at 1,936 lines (how many responsibilities; which helpers nothing calls); `scripts/build` at 646 and `scripts/image` at 481 with the fork's identity hunk; the identity split across four files (`distributions/ROCKNIX/version`, `options`, `config/build-identity`, `scripts/image`) and `CLAUDE.md`'s sentence about it (#644 finding 14, T4's edit); the Makefile's `docker-%` recipe and its `.env` lifecycle as a reader follows it; comments that match the code (`get_env`'s does; `X64_SKIP_CORES`'s neighbour in T3 did not); headers that say where a script came from (LibreELEC, OpenELEC, JELOS, ROCKNIX) | the specific unit named with what a reader stumbles on; a duplicate named with its original and the diff's size |

A finding is one question with its evidence; severity and category are the
code-auditor's, with `Renovation` as the category for Q1, Q5, Q6 and Q7
items that are not defects. A Q3 finding that is a defect is also a `bug`
issue (D-WORKFLOW-187, § 1), filed with the VM-verifiable or sandbox-
verifiable artifact that would close it.

**The line this slice does not cross.** The engine builds; this lane does
not. A finding whose only proof is a build -- a stamp rule changed, a
`mkimage` arithmetic, an identity written differently -- is recorded with
the sandboxed or recorded-run evidence that can be had now, its fix (if
any) lands on the branch with `pkgcheck` and the sandbox as its first test,
and its proof on an image is `fix-pending-image` (§ 6), the coordinator's
at the first build after the merge. A change to what the engine *requires*
of a build (the admission, the watcher, the pin) is T9's or the
coordinator's: recorded as a lead on #652, never made here.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict, as its `SKILL.md`
§ Evidence floor lists them:

1. *Tracker state is never sole evidence.* Issue state, checked AC boxes,
   and retro summaries may corroborate but can never be the ONLY evidence
   for a PASS; every PASS cites at least one primary artifact (file:line,
   executed command output, or commit diff).
2. *Mechanical evidence outranks reading.* Where a check exists, RUN it and
   record the command, exit status and counts in the criterion entry.
3. *Run it on a device, not on the host.* A verdict about runtime behaviour
   needs evidence from the target. **For an engine, the target is a build**,
   and this lane builds nothing (D-WORKFLOW-183; `slices.json`'s closing:
   *"no image or package build (plan § 7 item 5)"*): a claim about what the
   engine does is proven by **a recorded run** (the M7 lane's
   `.build-runs/<id>/` records and `build.*` logs in the legacy worktrees,
   read-only; the image's `/etc/os-release` in a build root's
   `image/system`), by **a sandboxed call** of the function or script with
   every variable set to a scratch path (the host's bash is the container's
   bash for these scripts, since the container runs them under the same
   interpreter the host does -- say so where it matters and name the
   version read from the pinned image's labels), or by **the guest** for
   what the engine wrote into an image; a claim about what the engine would
   do after a fix is `fix-pending-image` (§ 6) and the hand-back says so per
   fix.
4. *An assertion that cannot fail is not evidence.* Before recording a PASS,
   ask what result would have produced a FAIL.
5. *Subagent output is a LEAD, never EVIDENCE.* Every fact that supports a
   verdict is re-read from the primary artifact before the verdict is
   written. Fan-out inside this lane is read-only research subagents only
   (D-WORKFLOW-183).

**What runs on the VM, and how.** Can this be done on the VM? **Yes** for
the one thing the engine writes into an image that a device reads: the
identity in `/etc/os-release` (and the launch table, T3's reach), read from
the install tree of the M7 GENERIC_X64 build root on the host first
(`image/system/etc/os-release`; the T3 brief § 2 describes that tree) and
confirmed on a guest only if a finding needs the running system's reading
(`rocknix-info`'s `BUILD ID` line, D-WORKFLOW-157). **Everything else the
engine does happens on the build host or in the build container, and the
VM has nothing to show about it**: the evidence is the recorded runs and
the sandbox. So this slice expects **no guest of its own**; if one is
needed, the brief's T3 sibling gives the recipe (its § 5) with this lane's
own ports (SSH 10035, VNC display 22, pidfile and sockets under
`/workspace/artifacts/m6-t5-<date>/`), and the host window protocol applies.
Nothing in this slice touches a handheld, a person's cloud, a shared QA
backend, or a QA guest another lane owns.

- **The host handoff is a wait, not a stop.** The agreement in
  `/tmp/m7-m6-host-coordination-20261023.txt` is that **M6 starts no runtime
  of any kind (no guest, no compiler, no `npm install`) while an M7 window
  is open; the coordinator's comment on #652 relaying M7's `resource return`
  is the signal this lane acts on**, and the file's last `== M7` block is
  read before any runtime (the first commands print it). The M7 lane held
  the host from 01:33 to 02:22 on 2026-10-24 and returned it; a later window
  may be open at dispatch. **This slice's work is almost all reading,
  `git`, `gh api`, shellcheck, `bash -n`, `python3 -m py_compile` and
  sandboxed shell**, none of which the window forbids; the only compiles
  are `tools/build-identity-test`'s and `tools/host-maintenance/test-build-monitor`'s
  Python (no compiler), so a window costs this lane nothing but a guest it
  does not expect to need.
- **The recorded runs.** The M7 lane's build worktrees under
  `/workspace/repos/rocknix.worktrees/` hold `.build-runs/<id>/` directories
  (`build.log`, `build.pid`, `build.rc`, `build.start`, `build.status`,
  `build.status.pid`, `command.pid`, `runner-result.json`, `watch-job`,
  `watcher.err`, `watcher.interval`, `watcher.pid`), each a run of this
  engine under the watcher: `m7-signin-build-20261022-07` (the GENERIC_X64
  image of 2026-10-22, BUILD_ID `069fc2704421`), `m7-pixelelated-h700-03`,
  `m7-signin-h700-build-20261023-05`, and the runs of 2026-10-24 from
  `08cc7ff6cd` (H700 and SM8550, the M7 window's). **Read-only, every one of
  them** (the M7 lane's; `ls`, `cat`, `grep`, `tail` only; never a write,
  never a process started there). A `build.log` names every package's
  configure line (the `--wrap-mode=nodownload` in a meson line is Q2's
  evidence that the engine passed it), every stamp decision, the image
  step's identity lines and timings; `build.status` is the watcher's record
  (`state`, `written`, `progress`). **A run's log may carry the build's
  credential-shaped defines** (`-DSCREENSCRAPER_DEV_LOGIN=`): every line
  read from a log passes `grep -v -i -E 'key|pass|token|user|psk|LOGIN'`
  or the masking `sed` below, and no `ninja -t commands` or `make` command
  line is ever pasted into an artifact, an issue or a transcript (T2's
  § 5 learned this; the pre-commit scan refuses it).
- **The sandbox.** A function from `config/functions` or
  `distributions/ROCKNIX/config/functions`, or a script such as `scripts/get_env`,
  is run under `bash` from a directory the lane owns under `.qa-scratch/`
  (gitignored), with **every variable it reads set to a scratch path**
  (`ROOT`, `BUILD`, `PKG_BUILD`, `PKG_DIR`, `INSTALL`, `ESTMP`, `TARGET_IMG`,
  `SOURCES`, `DEVICE`, `ARCH`, `PROJECT`, `DISTRO`, `TARGET_TYPE`: the lane
  lists them from the function's text first, as T3's brief § 5 says for the
  table), `config/options` sourced only where the function needs it and
  with `ROOT` pointing at the worktree; nothing under `/workspace/repos/rocknix*`,
  `/usr`, `/storage` or another worktree is a target. **For `get_env`**: a
  fixture environment built at run time (`env -i` with a handful of
  variables whose names match and do not match `KEEP` and `DROP`, their
  values the words `fixture-a`, `fixture-b`: never a real value, never a
  credential-shaped literal in the test file, `engineering-practices.md`
  § Guards must fail closed's fixture rule) and the script's output
  compared with the expected set; the case that would FAIL (a name the DROP
  pattern should catch and does not) is constructed and seen to fail before
  the pattern is called proven. **For `calculate_stamp`**: a fixture
  package directory and a generic twin it sources, the stamp computed, the
  generic file changed, the stamp computed again; whether it moves is the
  finding's evidence. **For `mk_es_systems`**: the recipe T3's brief § 5
  gives (the pre-format `.es_systems.cfg` through `python3 -I` and
  `xml.etree.ElementTree`; `xmlstarlet` is absent on the host, so the
  formatted file is empty and that emptiness is itself Q3's evidence for
  the silenced formatter).
- **The host-side checks that exist for these sources**, each run and its
  command, exit status and summary line recorded in `02-forward-audit.md`;
  a check that cannot run is recorded as such, never as a pass (each block
  sets its variables; the tools are `$D`'s, by absolute path):
  ```bash
  D=/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-652
  cd "$D"
  for f in $(git ls-files scripts | grep -vE 'scripts/(lib/|council|lint-council|verify-|write-step-seal|owner-queue-lint|build-council-prompt|check-stale-blob-drift|forge-|setup-council|__tests__)'); do head -1 "$f" | grep -q -E '^#!.*(bash|sh)' && { bash -n "$f" && echo "ok $f" || echo "FAIL $f"; }; done | sort | uniq -c | sort -rn | head    # bash -n over the membership's shell scripts; record the two counts
  for f in scripts/pkgbuilder.py scripts/genbuildplan.py scripts/uboot_helper scripts/test-audit-review.py; do python3 -I -m py_compile "$f" && echo "ok $f" || echo "FAIL $f"; done
  python3 -I "$D/tools/build-identity-test" --output .qa-scratch/t5/build-identity-test.json; echo "rc=$?"          # #532's identity controls over config/build-identity, scripts/image's blocks and the release plan (T9's tool, this slice's file); read its docstring for what it asserts
  python3 -I "$D/tools/host-maintenance/test-build-monitor" 2>&1 | tail -3; echo "rc=$?"                           # the watcher the entry points exec into (T9's tool): a trial that it runs here, not this slice's check
  "$D/tools/fork-package-freshness" --list | wc -l                                                                     # the engine introduces no package: record the line and that none is this slice's
  "$D/tools/pkgcheck" rocknix | tail -1                                                                                # pkgcheck is run where a recipe changes; the engine changes none, so this is the trial that the tool runs from this tree
  ```
  - **shellcheck** is not installed on the host. T1 downloaded the release
    `shellcheck-v0.11.0` into its `.qa-scratch/` (gitignored) and ran
    `shellcheck -f gcc <file>` with each file's own shebang (`-s bash` for a
    sourced fragment without one); do the same (a download into its own
    empty directory under `.qa-scratch/`, `sha256sum` against the release's
    published sum recorded, run by path, never from inside the download's
    directory) over the 30 scripts, `config/functions`, `config/options`,
    `config/path`, `config/graphic`, `config/show_config`,
    `config/build-identity`, the `config/arch.*` files,
    `distributions/ROCKNIX/config/functions`, `distributions/ROCKNIX/options`,
    `distributions/ROCKNIX/version` (sourced fragments: `-s bash`) and the
    `Makefile`'s recipe lines where they are shell; every error is read at
    its site before it is a finding, as T1's `02` § shellcheck errors does;
    a `Makefile` is not shellcheck's input, so its recipes are read.
  - **`actionlint` or an equivalent for the 19 workflows** is not on the
    host either: the workflows are read, and `gh workflow list` and `gh run
    list --workflow <file> --limit 3` record each one's state and last
    conclusions on the fork (#644's finding 19: `Build` ends
    `startup_failure` daily; the lane records the date it read).
  - **The container digests** (Q4 b): `docker manifest inspect
    ghcr.io/pixelelated/build@sha256:988c0ba5…` and `docker manifest inspect
    ghcr.io/rocknix/rocknix-build:latest` read a manifest without pulling
    (a network read, no runtime; if the host's docker has no GHCR token for
    the fork's mirror, `gh api` on the package versions or the registry's
    anonymous token flow is the alternative; the lane records which worked
    and never runs `docker pull`), their `created` labels and digests in the
    Q4 table beside the Makefile's pin and `docs/reviews/build-path-read.md`
    § 4 finding 1's dates.
  - **The guest**, only if a finding needs the running system's reading of
    the identity: T3's brief § 5 recipe with this lane's ports; the image's
    install tree on the host is the primary artifact for what the engine
    wrote.
  - of `tools/vm-qa`'s suites, none is this slice's; record that in `02`
    rather than running the runner.
- **A read is free and goes through the filter.** Every line read back from
  a build log, a `.env` (never read at all: it does not exist at rest after
  `67cd0e6493`, and if one is found in any worktree it is a finding reported
  by its path and size, never its content), a guest, or a config passes
  `grep -v -i -E 'key|pass|token|user|psk|LOGIN'`, or is masked with `sed -E
  's/((token|key|passw[a-z]*|psk|user|login)[=:])[^ ]*/\1***/Ig'` where the
  line's presence is the evidence (D-QA-021; `engineering-practices.md`
  § Nothing runs on a person's device). `~/.ROCKNIX/options` is never read,
  listed or stat'ed into a transcript beyond `test -f` and its mode
  (`stat -c %a`); its names are the four `KEEP` names and that is all the
  audit needs to say.

**What never runs in this slice:** a build of an image or a package in any
form (`make <DEVICE>`, `make docker-*`, `scripts/build`, `scripts/image`,
`scripts/install`, `scripts/build_distro`, `scripts/build_mt`, `scripts/clean`
against a real build root, `docker pull`, `docker run` of the build
container, `tools/watch-build` with a payload: a recipe or engine fix is
proven by the sandbox and recorded runs, and the build is the coordinator's
after the merge); a write under any `.build-runs/`, build root, `target/`,
`sources/` or `.ccache/` of any worktree; a credential-shaped line pasted
into any artifact, issue or transcript (a build log's defines, a `.env`'s
content, a `~/.ROCKNIX/options` line); a command on a handheld, a person's
cloud, a shared QA cloud backend, or a QA guest this lane did not start; a
runtime of any kind while an M7 window is open; an edit to any tool while a
run of it is in flight; `pkill -f` or `kill` by pattern; bare `git stash`;
`git worktree remove --force` or `rm -rf` of any worktree
(`tools/fork-worktree remove`, and only of this lane's own); a write under
`/workspace/repos/rocknix` or any `rocknix.worktrees/*`, or in the P0, P1,
T1, T2 or T3 worktrees; an edit to `.github/sessions/saved-session-state-next.md`
(the M7 lane's); `--no-verify` on any push; a model call outside
`tools/council/run`; a credential or the wordlist printed; a merge of
another lane's feature branch to refresh rules (read them from `next`);
`tools/renovation-inventory --slice-issues` or `--order` without `--no-write`
in a worktree that is kept; a change to `docs/reviews/order.md`,
`slices.json`, `areas.json`, the plan, the brief, #652's criteria or the M6
body (the coordinator's, D-WORKFLOW-189); **a move of the build container's
pin, a change to the admission's or the watcher's contract, or an edit to a
workflow's trigger** without a stream brief that says so (the pin is the
coordinator's act, #644 finding 1; the admission and the watcher are T9's;
the fork's CI gates are T10's); a GitHub issue other than the audit
punch-list issue and `bug` issues (§ 1).

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#652`
(`Refs #652` while any criterion is open, never a closing keyword); the
stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-build-engine/00-running-log.md` | the skill's append-only flight recorder, opened first: the model and effort that ran, `reviewed-at` (the branch `HEAD` at stage A) with `8ebaf8daad` beside it, `upstream/next`'s hash and the merge base the first commands fetch, the host file's state, every command with its exit status and time, each stage's entry, every wait; **every sandboxed call or recorded-run reading that stands as a proof announced on a line that begins `PROOF:`** with its time and its script or log path, the token criterion 12 counts | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 242 paths re-derived with the filter of § 2 and the deltas beside the recorded counts (the three figures: the filter's lines, the tool's `read`, the fork-own part); the five groups; what the globs would have swept in and the areas that own it; the interacting subsystems; the branch scan; the M7 delta (none, or the hunks); § Phase 1: the closed bugs grep with its pattern and count, the prior audits' counts per folder, upstream's trackers checked (D-WORKFLOW-162: ROCKNIX's `distribution` PRs on `scripts/` and `config/`, LibreELEC's on the same files since the engine's header names it as the origin) | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #652's checklist, plus a **coverage table with one row per path** (242 rows; the first cell the path in backticks, so ``grep -c -E '^\| `(scripts|config|distributions|Makefile|Dockerfile|\.gitignore|\.merge-head|\.github)' 02-forward-audit.md`` prints 242; then group, tier, Q1 to Q7 each answered or `n/a` with the reason, and for a fork-own path the fork commits read); § Mechanical checks (every check of § 5 with command, exit status, summary; a check that could not run says why); § Recorded runs (which `.build-runs/<id>/` were read, for what, read-only); § The nine #644 findings (one row each with the disposition § 3 names and what the reading found); § Proofs (each sandboxed call or recorded-run reading with its `proved:` cell, below) | B onward |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5's interaction audit for the seams § 2 names (the entry points x `tools/watch-build`'s marker and lock, T9's; `get_env` x the Makefile's `.env` recipe x `~/.ROCKNIX/options`; `calculate_stamp` x the 53 overrides that source a generic recipe, T8's; `mk_es_systems` x T3's metapackage; `scripts/image`'s identity x `tools/rc-preflight` and `fork-publish-release`, T9's and the release rules; the workflows x T10's fork CI) and the futro's predictions checked | B |
| Analysis | `.../04-analysis.md` | Phase 4, then § Finding Verification (4.5), then **§ Renovation face** with one subsection per question Q1 to Q7 (the lint requires all seven), **Q4 carrying the two currency tables** (the fork against ROCKNIX with the 4 dispositions and every textual difference named; the container digests with their dates), Q6 the five reachability tables, Q5 the recorded runs' measurements with their run ids, then § Second opinions (4.6) with the two seats' leads re-read | B, C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (written before the first call), `<member>-brief.md` (no credential-shaped line, no log excerpt with a define), the outputs, each call's `provenance.json`; the probe of each seat | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | prints `PASS pre-issue artifacts (does not certify resolution)`; recorded in the running log | C to D |
| Punch list | `.../05-punch-list.md` | Phase 5, every item with `question: Q1..Q7` (or `none` with a reason), severity, category (`Renovation` where it is not a defect), where (file:line at `8ebaf8daad`), acceptance; the YAML `punch_index` (`templates.md`); an item whose fix is the coordinator's or T9's or T10's marked for `deferred:<#652's lead comment>` / `deferred:#656` / `deferred:#<T10's issue>` with the reason; a removal with `removal: yes` and its `Already written:`; an upstream contribution candidate marked for #585 | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #652 | `Audit: M6 T5 the build engine -- N findings (X critical, Y high)`; one checkbox per item, each agent-verifiable (D-QA-044); `tools/box-check --issue N` run on it and its line recorded | D |
| Bug issues | GitHub, label `bug`, title `Bug: ...` (`milestone-phase-naming.md` § Reactive), milestone-less and not sub-issues (T1's, T2's and T3's shape) | one per defect (D-WORKFLOW-187, D-QA-051): the code trace shape (`release-candidates.md` step 0), the `Can this be done on the VM?` line answered honestly (for an engine defect, usually *No -- the sandbox or a recorded run shows it; the image proof is the coordinator's build*: `bugs-are-agent-first.md`'s classes apply, with the sandbox as the agent-verifiable artifact), a verifiable criterion, `Already written:` | D |
| **The stage-D pause** | #652 | the punch list posted on #652 with the audit issue's number and the `bug` issues' numbers; **the lane waits** while the coordinator writes one remediation brief per stream of related items (plan § 6b stage E: the D-WORKFLOW-056 shape, the files owned, the test first, the `Already written:` line, commits cut from intermediates only after a green run, a stub or a fixture part of the claim; D-WORKFLOW-189) | D to E |
| Remediation | the branches the stream briefs name | each stream as its brief specifies: an engine change with its sandbox case first (the failing run recorded), `bash -n`, shellcheck's line, `pkgcheck` where a recipe is touched, and `tools/build-identity-test` where the identity is; a `bug` issue's fix carries its `Already written:` and names its two runs; a change whose proof is a build is `fix-pending-image` | E |
| Verification | `02-forward-audit.md` appended; `.../audit-completion.json` | every behaviour claim proven where the sandbox or a recorded run can show it (§ 5); every proof's row carries a `proved:` cell with one of `recorded-run` (a `.build-runs/<id>/` log or status of the M7 lane's, read-only, named by id), `sandbox` (a function or script run with scratch variables, the case named), `image-set` (the install tree or the guest reading what the engine wrote at `069fc2704421`), `fix-sandbox` (a fix proven by its sandbox case; the build is the coordinator's), `fix-pending-image` (nothing but a build can show it: the coordinator proves it at the first build after the merge, plan § 6b stage H); the Phase 7 gate in `05` | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-build-engine.md`, and the same text as a comment on #652 | the mini-retro skill's four answers with its scoped audit, in Instruction-Recommendations mode (plan § 6b G: the scope is epic tier); findings that recur become a rule edit, a tool, a blindspot entry; **what the slice did to the two time-to-play numbers** (nothing, said in those words, unless the identity read moved: the engine is not on the launch path) | G |
| Hand-back | #652 | `reviewed-at:` (the branch `HEAD` at stage A) and `fixed-at:` (the branch's last commit on the slice's paths) written into #652's body by the executor; one comment naming the branch tip and each artifact by path, the six checker exit codes, and per fix its `proved:` class | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-build-engine-652.md` | seeded by the coordinator; the executor updates it at every checkpoint: start here, the worktree, current focus, the stage reached, next commands, merge notes | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session, headed `#652` and the thing decided or learned | every session |

Neither `tools/renovation-status` nor `tools/renovation-drift` nor
`tools/renovation-inventory` is run to write ledgers or edited here; a
defect in one is a lead on #652 (they are P1's tools, documented in
`docs/reviews/README.md`).

## 7. Acceptance

The checklist on #652 is the contract. Its first five items are plan § 6b's
contract for every slice; the rest are this slice's, written by the
coordinator with this brief (D-WORKFLOW-189). Each names the artifact that
ticks it; the coordinator ticks them at hand-back from the artifacts, not
from this lane's word.

- [ ] `docs/audits/<date>-epic-m6-build-engine/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-build-engine/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included: Q1 to Q7 answered in `04-analysis.md`, and every punch item's `question:` in the index.
- [ ] `second-opinions/review-plan.json` records Extended depth and two reviewers from two other labs, and each reviewer's provenance names its served model (plan § 6c, D-WORKFLOW-137).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue, or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits the read and the fixes were made at (the read made with the slice's bytes equal to `next`'s `8ebaf8daad`, the branch on the P1 tip; no EmulationStation path here, so no `fixed-at-es:`), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed` (the coordinator's regeneration).
- [ ] `01-research-notes.md` § Scope records the read hash `8ebaf8daad`, the filter of brief § 2 with its output (242 paths, 13,910 lines, 18 fork-own with 3,266 lines, 224 upstream-carried, or the deltas beside them, and the order row's 6,776 and 2,419 explained as the code classes), the list of what the globs would have swept in and the areas that own it (the council scripts, the fork workflows, the session files), the M7 delta on the membership (none, or the hunks), and the two upstream trackers checked with dates.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c -E '^\| `(scripts|config|distributions|Makefile|Dockerfile|\.gitignore|\.merge-head|\.github)' 02-forward-audit.md`` prints 242; each row's Q1 to Q7 cells answered or `n/a` with a reason (`n/a: upstream's, unchanged here` is a reason for a group 3 to 5 file's Q1, Q2, Q3 and Q7 cells, § 4).
- [ ] `02-forward-audit.md` records, with command, exit status and summary line, each of: `bash -n` over every shell script of the membership with the two counts, `python3 -I -m py_compile` over the four Python scripts, shellcheck over the shell sources named in § 5 with every error read at its site, `tools/build-identity-test`, `tools/host-maintenance/test-build-monitor`, the three sandboxed calls of § 5 (`get_env` with a constructed failing case, `calculate_stamp` over a fixture override and its generic twin, `mk_es_systems` with the pre-format table through `ElementTree`), the container manifest reads with both digests and dates, `gh workflow list` and the last three conclusions of each of the 19 workflows, and `tools/fork-package-freshness --list`'s line showing it covers nothing here; a check that could not run is recorded with the reason, never as a pass.
- [ ] `02-forward-audit.md` § The nine #644 findings carries one row per finding (1, 3, 4, 8, 9, 10, 11, 13, 22) with the disposition brief § 3 names and what the reading found, and names the other seventeen with their carriers so none is taken here.
- [ ] `04-analysis.md` § Renovation face Q4 carries the two currency tables: (a) the 4 commits of `c445081a59..upstream/next` on the membership each with a disposition (merged / not applicable / to merge, with the reason) and every membership file that differs textually from `upstream/next` named as the fork's or upstream's with its commit; (b) the Makefile's pinned container digest and its date beside upstream's current `latest` digest and date, the `Dockerfile` diff, and the refresh recorded as the coordinator's act.
- [ ] `04-analysis.md` § Renovation face Q5 carries the ccache settings beside CI's with a measurement from a recorded run or the words `not measured` with why, the stamp granularity's cost as the count of packages a metadata sweep rebuilds, and the recorded runs' timings with their run ids; the two time-to-play numbers are named as untouched by this slice, with the one identity read as the exception if it moved.
- [ ] `04-analysis.md` § Renovation face Q6 carries the five reachability tables of brief § 4 (30 scripts with their callers; 19 workflows with trigger, state and last conclusions on the fork; 3 configuration trees against the five devices' options; 139 fragments against the systems the five devices' tables name; `.merge-head`'s reader and `scripts/test-audit-review.py`'s misfiling), each with its search command and output; every row marked unreached by any fork build, image or CI carries an `Already written:` line and what the unit exposed.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `recorded-run`, `sandbox`, `image-set`, `fix-sandbox` or `fix-pending-image` (§ 6, Verification); ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c '^PROOF:' 00-running-log.md`` (the convention of § 6).
- [ ] Every punch item whose `punch_index` entry carries a `tracked: "#N"` has that `bug` issue carrying the `Can this be done on the VM?` line answered honestly and a verifiable criterion (the sandbox or a recorded run named where the VM cannot show it); every item whose entry carries `removal: yes` has an `Already written:` line in its row; no pin, admission, watcher or workflow-trigger change is applied on this branch without a stream brief; `tools/box-check --issue N` passes on the audit issue and on each `bug` issue this lane files.
- [ ] The retro exists at `docs/retros/<date>-m6-build-engine.md`, is posted on #652, and answers what the slice did to the two time-to-play numbers.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge; the five exit codes pasted on #652.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back, § 10; criterion 5's `renovation-status` clause and
the merge are the coordinator's, so that checkbox is not the lane's to
tick); **the stage-D pause** (the punch list and the audit issue posted on
#652; the lane waits for the coordinator's stream briefs and does no
remediation before them, D-WORKFLOW-189; #652's body says the same above
its checklist); **the Phase 4.6 blocker** (a reviewer seat failing identity
verification, or the route missing after all: the other pass done, the seat
recorded pending, the blocker named on #652, no Phase 5; § 1); an explicit
maintainer pause on #652; any other blocker, named on #652 with what is
needed (a count that cannot be produced or two commands that disagree; a
rule that forbids a step; the npm install failing; a recorded run the lane
needs that no M7 worktree holds; the registry refusing both manifest reads);
**a hash mismatch at stage A** (the slice's bytes not `8ebaf8daad`'s, or
the branch not on the P1 tip: the coordinator re-baselines); or an
execution limit, stated as such with the running log current. **The host's
window is a wait, not a stop**, and this slice's reading, sandboxing and
API reads go on through it. A checkpoint is not a stop (D-WORKFLOW-149):
write it and take the next stage. A differing count is a delta, not a
stop. `next` moving under the slice is drift, not a stop. An idle session
says it is idle on #652.

## 9. Ceremonies owed

- A work-log entry per session, headed by `#652`; `tools/work-log-index
  --write` after it; the weekly summary if the lane's week falls due
  (`ceremonies.md`; `tools/ceremony-check` names W42's as overdue on
  2026-10-24, the M7 lane's week, not this lane's).
- A friction line in `docs/friction-log.md` the moment something slows,
  with `issue: #652` or the guard.
- The VM question written before every proof (§ 5 answers it for the slice:
  the engine's behaviour is proven by recorded runs and the sandbox, the
  VM shows only what the engine wrote into an image; a proof that needs
  something else writes its own line in `02-forward-audit.md`); a row in
  `docs/vm-qa-log.md` per VM cycle, if any.
- The mini-retro skill at stage G, posted on #652, with its scoped audit, in
  Instruction-Recommendations mode.
- A register row the same session for any decision the slice forces (a fork
  resolved, an assumption invalidated). The ID: one above the highest
  `D-WORKFLOW` on every pushed branch (`git grep -ho 'D-WORKFLOW-[0-9]*'
  $(git branch -r --format='%(refname)') -- docs/decision-register.md | sort
  -t- -k3 -n | tail -1`) and in the M7 lane's worktree
  (`/workspace/repos/rocknix.worktrees/m7-player-setup/docs/decision-register.md`);
  on 2026-10-24 the highest Decided row on the coordinator branch is
  D-WORKFLOW-192 (191 is an open row; P1's branch carries 188 and 189; T1's,
  T2's and T3's carry 188 to 192 where they merged the coordinator's tip;
  the M7 lane holds 171 to 180 unmerged), so **the next Decided row is 193**
  unless T3 has taken it: check every branch at the time. A row goes at the
  end of the `## Decided` table, never after `## Open decisions`
  (`tools/register-check` refuses it there, #646). The lane's register is
  the union the stacked branch gives, and `tools/register-check` runs on the
  worktree before the first push.
- `tools/ceremony-check` before every push; what it reports as owed by this
  lane is paid first; what another lane owes is noted on #652. Never
  `--no-verify`. A merge with conflicts is checked for leftover markers
  before it is committed (#696), and a union of two ledgers is made by
  whole entries, never by an unanchored pattern over marker-shaped text.
- Commit messages scoped as `CLAUDE.md` says (`scripts/build - ...`,
  `config/functions - ...`, `Makefile - ...`) with `Refs #652` and the bug's
  number; `docs: ...` for the artifacts.
- `change-log.md`'s running log the day a player-visible change lands
  (stage E: only the identity a player can read in `rocknix-info`; the
  engine otherwise shows a player nothing).

## 10. Hand-back

The coordinator accepts the slice by reading, in this order, without
re-reviewing it: #652's checkboxes against their artifacts (§ 7); the lint's
`PASS` line on the audit folder; `second-opinions/` (two provenance files
naming two served models from two labs); the audit issue's checkboxes all
at an outcome; the coverage table's row count; `02-forward-audit.md`'s
check lines and the `proved:` cell on each proof; **re-running `bash -n`
over the scripts, `tools/build-identity-test` and the three sandboxed calls
once** rather than trusting the log alone; the Q4 tables' commands
spot-checked (the two manifest reads re-run); the retro's four answers; the
five checker exit codes on #652 (with `register-check` run on a simulated
merge with the coordinator tip, as T1's acceptance did). The lane posts one
hand-back comment on #652 naming the branch tip and each of those artifacts
by path, writes `reviewed-at:` and `fixed-at:` into #652's body, then says
it is idle. After acceptance the coordinator writes the hashes into
`slices.json`, merges the branch in its turn after the M7 candidate (P0,
P1, T1, T2, T3, T5), regenerates the ledgers (§ 6, Hand-back row), and
**closes #652 only when the first build after the merge has proved each
`fix-pending-image` row** (the slice is `remediating` until then, plan § 6b
stage H). A brief that needed the coordinator's help mid-slice, beyond the
stage-D pause, the Phase 4.6 blocker and the host's return line this brief
already names, is a defect in this brief: log the friction, and the
coordinator fixes the template in plan § 7 before the next brief.

**The two readings before dispatch** (plan § 3, principle 3): the area
epic's futro (`docs/futros/2026-10-24-m6-build-engine.md`, posted on the
epic) and a stranger's proof of this brief by a reader with no context given
this tree and the brief. Version 2 records what each found and where it is
answered.
