---
slice: T22
id: os-system-services
issue: "#669"
epic: "#695"
area: os-scripts-and-launch
kind: read
lens: security, brittleness
depth: Extended
version: 3
written: 2026-10-25
author: the M6 coordinator (Fable 5.1, D-WORKFLOW-189)
read_refs:
  distribution: 8ebaf8daad
  p1: 2174265e9c
  upstream_next: 651150fc88
---

# T22: the OS's system services and platform quirks

## 1. Identity

- **Issue:** #669 (`M6.P2 E695/T22: os-scripts-and-launch: the OS's system
  services and platform quirks`, retitled from `E339` at dispatch), slice
  `os-system-services` (`k: 22`) in `docs/reviews/slices.json`,
  twenty-second in `docs/reviews/order.md` (its row: *422 | 16,604 |
  10,898 (3,002) | 0 | Extended*; its `why`: *busybox's configuration, the
  systemd units and the per-platform quirks run as root on every device;
  the inventory reads a whole package as reached, so `system-utils`'
  per-device sources [...] read `shipped` although `package.mk` installs
  only `${DEVICE}`'s: the slice first derives which the shipped pair (H700,
  SM8550, which have none) and the VM install, as T29 does for the quirks,
  reads those line by line, and records the rest as unshipped rows* --
  **half right, corrected in § 2: `system-utils` selects at install time,
  the quirks' platforms are all installed and selected at run time**).
  **Epic:** #695 (the OS scripts: T1 done; this slice; T29 the per-handheld
  quirks). **Milestone:** M6; its body holds the live order; read it first.
- **Predecessors that bear on these files:** **T1** (#648, the launch,
  control and state scripts, Extended, the model for this brief's two
  seats: its #740 lead on `userconfig-setup` is this slice's file and
  #669's one comment; `/bin/sh` is bash 5.3, not dash; its autostart
  fragment rows #723, #750, #751, #752; the `/storage/.config/autostart/`
  hook shape it recorded in its `04` -- the lane names the issue, if one
  carries it); **T14** (#661: #1000, `rocknix-autostart.service:9`'s
  argv is a constant `AUTOSTART_WRAPPER` in its tests with a drift check on
  the tree's unit -- a change to that unit here breaks T14's gate unless
  the constant moves with it; #997, busybox's provenance; D-QA-063, the
  exit lattice); **T15** (#662: #1015 and #1018, the silent host-busybox
  fallback; its F1 section reads the GENERIC_X64 quirks' history from git;
  #1029; #1038); **T29** (#676: `quirks/devices/**` is its, excluded here
  by the glob); **T13** (#660: nothing names this slice). Register:
  **D-WORKFLOW-184** (Extended = Astra plus Gemini 4 Argon),
  **D-SYS-002/003/008/009** and open **D-SYS-006**, **D-NET-001 to 006,
  009**, **D-CLOUD-064/072/078/079/080/082/147**, **D-INFRA-011/012/013**
  (the core keeper that upstream's journal crash logging collides with),
  **D-QA-042/053/063**, **D-UI-121**, **D-WORKFLOW-083**, **D-WORKFLOW-209**,
  **D-WORKFLOW-195**. Blindspots 16 (a unit naming a binary the image
  lacks), 33, 34 (busybox is not the host's tools), 37, 42, 54, 60, 74.
- **The division of labour (D-WORKFLOW-189)** and **the rule
  (D-WORKFLOW-209)** as T11's brief states them: the lane executes,
  changes none of the 422 and nothing under `packages/`, `projects/` or
  `tools/` at stages A to D; a dead end is a disposition; the class
  decision for anything upstream carries is the maintainer's on #346. A
  fix is a stage-E stream the coordinator writes after the stage-D pause.
- **One worktree, one session.** Branch `feature/m6-os-system-services-669`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-os-system-services-669`,
  created by the coordinator, stacked on `feature/m6-p1-survey-641` at
  `2174265e9c` with the coordinator's tip merged in and the lane's pointer
  seeded (the hashes are in the dispatch comment on #669). **Before that
  comment exists nothing runs in it.** The session is the T1 lane's
  (`m6-t1-os-launch`), after T13's close-out; its earlier worktrees stay
  beside this one, idle. **The rules in this worktree are `next`'s except
  the paths the dispatch comment lists.**
- **Model and effort:** Opus 5.5 at high effort. Record what ran in
  `00-running-log.md`'s header.
- **Review depth: Extended** (plan § 6c, D-WORKFLOW-184: a security slice).
  The primary auditor is this lane (Anthropic); **two reviewers from two
  other labs, each through the Facilitator and nothing else**, exactly as
  T1's audit ran them (`docs/audits/2026_10_23-epic-m6-os-launch-control-state/second-opinions/`
  on `feature/m6-os-launch-control-state-648` is the model: a probe and a
  refutation per seat, each with its `.provenance.json`; the packet manifest as T13's
  `second-opinions/packet-manifest.json` on `feature/m6-cloud-harness-660`;
  `review-plan.json` with two reviewers):
  - **GPT-6 Astra**: `tools/council/run invoke --member gpt --provider
    openrouter ...` at `max` (`openai/gpt-6-astra`, provider pinned to
    OpenAI, no fallbacks).
  - **Gemini 4 Argon**: `--member gemini-argon --provider openrouter` at
    `high` (`google/gemini-4-argon`). The route is in this tree
    (`scripts/council-invoke.ts`, the `gemini-argon` recipe) and the lint
    accepts the member (`tools/lint-audit-artifacts:59-99`: `google/gemini-4-argon`
    at `high`); `grep -c gemini-argon scripts/council-invoke.ts
    tools/lint-audit-artifacts` prints two non-zero counts at stage A, or
    the lane stops at Phase 4.6 as a named blocker on #669 and never calls
    `--member gemini` in its place.
  - Each seat: a probe first (identity, effort, provider from the
    provider's own field), then one refutation pass over one trimmed
    packet (D-WORKFLOW-195): the 29 units whole, `/usr/bin/autostart` and
    `profile.d/002-autostart`, `userconfig-setup`, `system-utils/package.mk`
    and `quirks/package.mk`, `busybox/package.mk` and the flagged lines of
    `busybox-target.conf` (not its 1,224 lines), `scripts/init` whole
    (1,383 lines, PID 1), the fork-own 24, `02`, `03`, `04` whole, and the
    context sections (the order's § T22, this brief's § 2 and § 4, the
    register rows named above). **Scanned before it is sent**
    (`tools/forbidden-terms-check --stdin`, the pre-commit's patterns, and
    T10's widened set read with `git show`); **every other `tools/council/run`
    call carries `COUNCIL_ENV_FILE=/nonexistent`, `--help` included.**
    Every seat item is graded in `04` § Second opinion (confirmed,
    narrowed, refuted, new), the decisive ones re-read at their lines.
- **The host:** M6's. **This slice's proofs are reads, and one guest cycle
  at most**: the order's closing evidence names *VM proofs for boot
  behaviour*, so stage A lists the behaviours only a booted guest shows
  (which units are enabled and run as root on the image, `shell.service`
  on tty1, the autostart hooks' order and identity, what `userconfig-setup`
  does on a first boot with seeded files) and asks for **one GENERIC_X64
  guest, under 30 minutes, as a plan on #669**; the coordinator grants it
  after the M7 lane's FINAL RETURN and after T13's cycle. Nothing boots
  before the grant; no build, no plan generation, no network at stages A
  to D; nothing on a handheld, ever. `TMPDIR` under `/workspace/tmp/m6-t22/`.
  Register: a row this slice forces takes D-WORKFLOW-210 or higher,
  D-QA-064, D-INFRA-033 or higher.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-os-system-services-669
cd "$D"
git branch --show-current                                            # feature/m6-os-system-services-669
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists
cat .github/sessions/saved-session-state-feature-m6-os-system-services-669.md   # seeded by the dispatch
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
df -i /tmp | tail -1                                                 # never export a tree under /tmp
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo "upstream/next at 651150fc88 is here"   # read, never fetched
grep -c gemini-argon scripts/council-invoke.ts tools/lint-audit-artifacts    # two non-zero counts
"$D/tools/rules-check" --quiet; echo "rc=$?"; "$D/tools/register-check" | tail -1
git push -u origin feature/m6-os-system-services-669
```

No `git fetch` of any kind.

## 2. Scope

**422 paths, 16,604 lines; 10,898 lines read by the survey's language rule
(shell, recipe, systemd, udev and one C file), 3,002 of them fork-own (24 paths);
0 patch and config lines; upstream-carried 398 paths; reach shipped 422.**
By group: the quirks 275 paths / 5,275 lines; systemd 41 / 1,732; busybox
36 / 6,507; `system-utils` 28 / 1,367; `autostart` 5 / 154; 23 other
`sysutils` packages. The membership is `slices.json` k 22's rule on
`inventory.json` at `2174265e9c`: area `os-scripts-and-launch`, reach
`shipped`, under `projects/ROCKNIX/packages/sysutils/**` and
`projects/ROCKNIX/packages/hardware/**`, **minus**
`projects/ROCKNIX/packages/hardware/quirks/devices/**` (T29's). The tool's
own `slice_of` (`tools/renovation-inventory:1237-1248`; `load_slices` at
`:1211-1236`) and the translator below agree on the set:

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,re,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
def rx(g):
    g=re.sub(r"\{([^}]*)\}", lambda m: "(?:"+"|".join(m.group(1).split(","))+")", g)
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i] in "(|)?:": out+=g[i]; i+=1
        else: out+=re.escape(g[i]); i+=1
    return re.compile("^"+out+"$")
INC=[rx("projects/ROCKNIX/packages/sysutils/**"), rx("projects/ROCKNIX/packages/hardware/**")]; EXC=rx("projects/ROCKNIX/packages/hardware/quirks/devices/**")
t=[r for r in rows if r["area"]=="os-scripts-and-launch" and r["reach"]=="shipped" and any(p.match(r["path"]) for p in INC) and not EXC.match(r["path"])]
READ={"shell","recipe","systemd","udev","c"}   # the survey counts these five as read; the dictionary below has no python or make
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t))
print("read",sum(r["lines"] or 0 for r in t if (r.get("language") or "") in READ),"fork-own read",sum(r["lines"] or 0 for r in t if (r.get("language") or "") in READ and r["tier"]=="fork-own"),"fork-own paths",sum(1 for r in t if r["tier"]=="fork-own"))
print("tier",dict(collections.Counter(r["tier"] for r in t)),"reach",dict(collections.Counter(r["reach"] for r in t)))
print("language",dict(collections.Counter((r.get("language") or "none") for r in t)))
g=collections.Counter("/".join(r["path"].split("/")[3:5]) for r in t); print("groups",dict(g.most_common(6)))
import os; os.makedirs(".qa-scratch/t22", exist_ok=True)
open(".qa-scratch/t22/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=lambda r:r["path"])))
print("written", len(t), ".qa-scratch/t22/paths.txt")'
# (the sorted(..., key=...) above is Python's keyword, not a credential: a reader applying the read filter to this block drops that line and sees nothing written -- run the block raw)
# paths 422 lines 16604
# read 10898 fork-own read 3002 fork-own paths 24
# tier {'upstream-carried': 398, 'fork-own': 24} reach {'shipped': 422}
# language {'shell': 299, 'recipe': 28, 'other': 7, 'none': 21, 'symlink': 2, 'systemd': 29, 'config': 30, 'c': 1, 'udev': 5}
# written 422 .qa-scratch/t22/paths.txt
```

A different count is a delta to record with the command, not a reason to
stop. (The five read languages are shell, recipe, systemd, udev and the one C
file, `evtest.c`; the stranger's proof found that set and no other sums
to 10,898.) **The read count excludes every `config` file**: the
three busybox configurations (3,648 lines), the sysctls, the tmpfiles and
the systemd drop-ins are in the slice and in no count the depth was sized
on; the security lens reads them anyway, so the slice is 16,604 lines of
reading, not 10,898.

**Two selection mechanisms, and the `why` named only one.**
*Install-time:* `projects/ROCKNIX/packages/sysutils/system-utils/package.mk:27-34`
installs the generic scripts (`:14-15` also `sources/autostart/common/*`
on every build) and then only `sources/devices/${DEVICE}/*` and
`sources/autostart/${DEVICE}` -- so **8 rows / 317 lines marked
`shipped` are installed by no shipped image** (AMD64's, RK3399's,
RK3566's, S922X's), the VM installs `GENERIC_X64/video_sense` (fork-own),
and H700 and SM8550 have no device directory; the device files are copied
*after* the generic ones into `/usr/bin`, so `RK3399|RK3566|S922X/headphone_sense`
overwrite the generic one on those builds. *Run-time:* the quirks'
`package.mk:18` copies **every** `platforms/*` into every image that has a
platform directory of its own (`:16`, true for H700, SM8550 and
GENERIC_X64; `:15` copies every `devices/*`); selection happens at boot by `${HW_DEVICE}` (from
`/etc/os-release`, written by `scripts/image:156`) in `/usr/bin/autostart:16-28` (the file is
`sysutils/autostart/sources/autostart`, 97 lines) and by `${QUIRK_DEVICE}`
(the device-tree model, or DMI vendor and product, set in
`autostart/profile.d/002-autostart:6-12`) at `/usr/bin/autostart:31-43` -- so **213 of the
264 platform files are shipped bytes that never run on H700, SM8550 or the
VM**. The slice's reachability table carries a third column, **runs on**
(H700 / SM8550 / VM / none), beside *installed on*, with the line that
decides each.

**The units: 29 files, 397 lines, none with `User=` or `Group=` -- all
root.** The lines the security lens reads first: `shell.service` (an
unauthenticated root shell on tty1, `exec /bin/sh`); `/usr/bin/autostart:71-77`
running `/storage/.config/autostart/*` as root (the `exec` at `:76`), and
`:50-54` running `/usr/lib/autostart/common/*` -- neither loop carries an
`-f` test;
`cron.service` (crond over `/storage/.cache/cron/crontabs`);
`udevil-mount@.service` (any inserted medium mounted, then `samba-autoshare`
in `ExecStartPost`); `userconfig-setup` (#740: copies `authorized_keys` and
the Wi-Fi files at first boot, and makes a *file* named `/storage/.ssh`);
`video.service` -> `/usr/bin/video_sense`, which only the GENERIC_X64 and
RK3399 builds install (`git ls-tree` of `system-utils/sources/devices/*/video_sense`;
blindspot 16's shape). **`system-utils/package.mk` has no `post_install`**
(one function, `makeinstall_target`), `scripts/install` only copies
`system.d/*`, and no `enable_service` under `sysutils/` or the quirks names
`video`, `headphones`, `input`, `fancontrol`, `batteryledstatus` or
`rocknix-autostart.service`: which build enables those six is decided
elsewhere (a preset, another package) -- `git grep -n -E 'enable_service|preset'
8ebaf8daad -- projects packages config` answers it, quoted; `rocknix-autostart.service:9`
(T14's constant). **busybox:** the effective pin is the override's
**1.36.1** (`busybox/package.mk:7`; a plain-http `PKG_URL` at `:11`); the
generic LibreELEC recipe says 1.38.0 and is shadowed (#997, T14's);
`busybox-target.conf` (1,224 lines, `config`): `CONFIG_FEATURE_SUID=y`
`:30`, `LOGIN` `:549`, `PASSWD` `:554`, `SU` `:556`, `HTTPD` `:888` with
`CGI` `:894`, `NC` `:950`, `UDHCPD` `:1010`; `scripts/init` is 1,383
fork-own lines, PID 1. **The fork-own 24** (3,002 lines): `scripts/init`,
`input_sense` (539 lines, which upstream has since rewritten in four
commits), the
five GENERIC_X64 quirks (a developer's tool, D-QA-053, rewritten in eight
commits on 2026-09-28 -- a punch item there is a harness item, not a
product item), `99-coredump.conf`, `sysctl.d/rocknix.conf`,
`hang-policy.conf`, and the rest the block lists; the slice names each
with its last fork commit.

**The read tree is three and a half weeks behind upstream in exactly this
area.** Merge base `c445081a59` (2026-10-01); at `651150fc88` **44 of the
422 differ (M), 20 are gone (D: 9 files upstream never had, 2 the fork
carries that upstream has removed -- `99-coredump.conf` by `8bce25b3b7`,
`sysctl.d/rocknix.conf` by `54acd9556f` --, and 9 real deletions --
`80-clock.rules`, `99-rocknix-networking.conf`, the `file` and `i2c-tools`
recipes, the SM6115 and RK3576 sleep hooks), and 42 are new under the
globs, plus 2 renames (A: busybox 1.38.0's seven patches, 0001 to 0006
and 0010, renames of the override's own `busybox-0X-*.patch` -- the fork
already carries `06-prevent-root-weak-passwd`; `075-scanout-offload` for
SM8550, six files; `games-swap.oomrule`; `20-crash.conf`; `60-rocknix.conf`;
and the rest the lane lists)**; upstream moved busybox to 1.38.0, systemd
to 261.2, util-linux to 2.42.4 (the override; the generic recipe says
2.42.2 at both hashes), added `games.slice` and oomd, replaced core files
with journal crash logging (`8bce25b3b7`, which removes the fork's
`99-coredump.conf` -- D-INFRA-013's keeper), shipped the sysctls in the
image (`54acd9556f`: `qdisc.conf`, `post-update`, `cdrom.conf`,
`99-rocknix-networking.conf` and `sysctl.d/rocknix.conf` deleted,
`60-rocknix.conf` new; `hang-policy.conf` is the fork's own with no
upstream history), and rewrote `input_sense` in four commits (the fork's
539-line fork-own copy). **Every finding on one of
the 44 names the file's state at `651150fc88` beside it**, and a finding
upstream has already fixed is *settled by the next base merge*, not a
bug. **The inventory's `last_upstream_commit` is upstream's tip, not the
read tree's** (`busybox-target.conf` reads `be9a5e4a81 2026-10-04`,
`scripts/init` `03204074ef 2026-10-08`, neither an ancestor of
`8ebaf8daad`): the column is cited as the tip's, never as the tree's.
**History since 2026-06-01 over the 422:** 87 non-merge commits, 33 the
fork's (`Max Engel|blitterbot|rasterabot`) and 54 upstream's (the quirks
48 of which 13 fork's; systemd 17 of which 13 fork's; `system-utils` 9;
busybox 7).

## 3. Read first

1. `.claude/rules/` from `next`: `engineering-practices.md`,
   `generic-x64-vm-testing.md`, `device-builds.md`, `upgrade-and-install.md`
   (D-WORKFLOW-050; the settings writers, #421), `vm-first.md`,
   `bugs-are-agent-first.md`, `handheld-evidence.md`, `packaging-and-patches.md`,
   `decision-register.md`, `issue-tracking.md`, `working-principles.md`,
   `adversarial-council.md`, `council-substrate-integrity.md`.
2. `docs/reviews/plan-for-the-plan.md` § 6b, § 6c (Extended); `docs/reviews/order.md`
   § T22, § T1, § T29; `docs/reviews/briefs/os-launch-control-state.md`
   (T1's, the area's model) and T1's retro on #648; `docs/futros/` for the
   area's kickoff futro (T1's) -- this slice's kickoff adds its own
   section there (the coordinator's).
3. The register rows named in § 1, by ID; the blindspots named.
4. T1's `02` and `04` (`feature/m6-os-launch-control-state-648`, `git
   show`); T14's #1000 and #997; T15's F1 section (`feature/m6-tooling-last-good-test-662`).
5. `scripts/image:156` (`HW_DEVICE` into `/etc/os-release`), `/usr/bin/autostart`
   and `autostart/profile.d/002-autostart` in the tree, `system-utils/package.mk`,
   `quirks/package.mk`, `systemd/package.mk`'s `post_install`, `busybox/package.mk`.

## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`guest`, `design`); the lens is security first:

- **Q3 Bugs and security -- the lead question.** For every unit and script
  that runs as root (all 29, and the autostart chain): what path it reads
  or executes that the player or a medium can write (`/storage/.config/autostart/*`,
  `/storage/.cache/cron/crontabs`, an inserted medium, `authorized_keys`
  at first boot), what guards it (a `-f` test, a mode, a mount option, an
  allowlist), and what a missing guard lets happen -- read, with the lines.
  A defect with a reachable consequence is a `bug` with its trace, its
  `Already written:` line (what the units have already left on devices:
  a `/storage/.ssh` file, a crontab) and its VM line; `shell.service`'s
  tty1 root shell is a finding with the register searched first
  (`tools/archaeology shell.service tty1`) -- a design upstream chose for
  a handheld, recorded as such unless a row says otherwise. `video.service`
  on a build without `video_sense`: a `bug` only if the unit is enabled
  there. #740 is cited, not re-filed.
- **Q4 Package currency.** busybox 1.36.1 against upstream's 1.38.0 with
  its seven patches (renames of the override's own; `06-prevent-root-weak-passwd`
  already here); systemd 255.8
  in the image against 261.2 upstream; util-linux; the plain-http
  `PKG_URL`; each as the pin at `8ebaf8daad`, at `651150fc88`, and
  `CANNOT (no network)` for the author's release (`tools/fork-package-freshness`
  named, D-WORKFLOW-024).
- **Q6 Dead ends.** The 8 `system-utils` rows no shipped image installs;
  the 213 platform files no shipped unit runs (one disposition per
  platform directory, *carried by placement*, D-WORKFLOW-185); the 9 files
  upstream deleted (*settled by the next base merge*). Removals none.
- **Q5 Efficiency.** The bytes every image carries and never runs (the
  213, with their sizes); the busybox configuration's enabled applets
  against what the scripts call (`SU`, `LOGIN`, `PASSWD`, `HTTPD`, `NC`,
  `UDHCPD`: which script or unit calls each -- `git grep` -- and which
  none does).
- **Q2 Standards.** The units' missing `User=`; the `-f` test absent at
  `autostart:50-54`; the two selection mechanisms documented nowhere a
  reader of `package.mk` lands; the `last_upstream_commit` column read as
  the tree's (an inventory reading, cited, T10's).
- **Q1 Modernize.** The `/storage/.config/autostart/` hook shape (T1's
  lead, a design the coordinator holds); the collisions upstream's next
  merge brings (`99-coredump.conf`, which `8bce25b3b7` removes;
  `sysctl.d/rocknix.conf`, which `54acd9556f` removes for `60-rocknix.conf`): what the fork keeps, what it yields -- a design
  sentence each, deferred to the coordinator, no edit.
- **Q7 Clarity and structure.** Can a reader tell, from the tree, which
  units run on which device and which quirks a boot selects? Does
  `quirks/package.mk` say it ships every platform?

## 5. The evidence floor

1. Tracker state is never sole evidence; every cell cites a command's
   output or a file:line at `8ebaf8daad`.
2. Mechanical evidence outranks reading: `git grep` for a caller, `diff`
   against `651150fc88`, `git log` with the three fork identities; a
   comment is the author's claim (blindspot 31).
3. **The bench is the host; one guest cycle at most, granted; no
   handheld.** **Can this be done on the VM? Yes, for the units and the
   GENERIC_X64 quirks; for the rest, no -- and the no is a read plus a
   `device-facts.md` row, never a device run:** the guest runs the 29
   units and `platforms/GENERIC_X64/*` (five fork-own files), so a
   behaviour claim about a unit (enabled, as root, on tty1, the autostart
   order, `userconfig-setup`'s first boot with seeded files) is proven on
   one GENERIC_X64 guest in the window the coordinator grants on #669
   after the M7 lane's FINAL RETURN and T13's cycle (stage A lists the
   proofs and their minutes, under 30); the H700 and SM8550 platform
   quirks, `002-device-switch`, `QUIRK_DEVICE`'s device-tree branch, the
   `sleep.d/` hooks and `volume-fixup.service` (RK3566) are read line by
   line and, where a claim needs a board, point at `docs/releases/device-facts.md`
   (D-QA-044) or are an open item to test (`bugs-are-agent-first.md`).
   Nothing runs on a handheld. Two `tools/council/run invoke` calls, the
   two seats.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.

**The runs, with what the coordinator read** (the lane runs each at stage
A and records the exit, the wall time and the summary line; `TMPDIR` under
`/workspace/tmp/m6-t22/`):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-os-system-services-669
cd "$D"; export TMPDIR=/workspace/tmp/m6-t22/tmp; mkdir -p "$TMPDIR" .qa-scratch/t22
# the membership block (§ 2) -> .qa-scratch/t22/paths.txt (422)
# the two selection mechanisms (expect system-utils package.mk:27-34 installs ${DEVICE}'s; quirks package.mk:15 and :18 copy all; autostart:16-27 and 002-autostart:6-12, :31-43 select)
git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/package.mk | sed -n '24,36p'
git show 8ebaf8daad:projects/ROCKNIX/packages/hardware/quirks/package.mk | grep -n -E 'cp |platforms|devices' | cut -c1-120
git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/packages/sysutils/system-utils/sources/devices projects/ROCKNIX/packages/sysutils/system-utils/sources/autostart | sed -E 's#.*/sources/(devices|autostart)/##' | cut -d/ -f1 | sort | uniq -c
git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/packages/hardware/quirks/platforms | cut -d/ -f7 | sort | uniq -c    # 264 files by platform; the shipped three are GENERIC_X64, H700, SM8550
git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/packages/sysutils/system-utils/sources/devices | grep video_sense   # GENERIC_X64 and RK3399
git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/sources/autostart | grep -n -E 'HW_DEVICE|QUIRK_DEVICE|/storage/.config/autostart|-f |exec' | cut -c1-120   # /usr/bin/autostart, 97 lines: 16-28, 31-43, 50-54, 71-77
git grep -n QUIRK_DEVICE 8ebaf8daad -- projects/ROCKNIX/packages/sysutils | cut -c1-120   # 002-autostart:6-12 sets it
# the units (expect 29; 0 with User=; the ExecStart lines masked)
git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/packages/sysutils projects/ROCKNIX/packages/hardware/quirks/system.d | grep -E '\.(service|timer|socket|target|mount|path)$' | tee "$TMPDIR/units.txt" | wc -l   # 29 (27 under sysutils, led-poweroff and volume-fixup under the quirks)
for u in $(cat "$TMPDIR/units.txt"); do printf '%s: User=%s Exec=%s\n' "$(basename "$u")" "$(git show "8ebaf8daad:$u" | grep -c '^User=')" "$(git show "8ebaf8daad:$u" | grep -m1 '^ExecStart' | cut -c1-70)"; done | sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'
# busybox (expect 1.36.1 at :7, http at :11; the flags at the lines named)
git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/busybox/package.mk | sed -n '5,12p'
git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/busybox/config/busybox-target.conf | grep -n -E '^CONFIG_(FEATURE_SUID|LOGIN|PASSWD|SU|HTTPD|FEATURE_HTTPD_CGI|NC|UDHCPD)=' | cut -c1-60
# the history with the three identities (expect 87; fork 33; upstream 54) and the upstream delta (expect 44 M, 20 D; the 42 A and 2 R listed by name)
tr '\n' '\0' < .qa-scratch/t22/paths.txt | xargs -0 git log --no-merges --format='%h %an' --since=2026-06-01 8ebaf8daad -- | tee "$TMPDIR/hist.txt" | wc -l; grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt"
tr '\n' '\0' < .qa-scratch/t22/paths.txt | xargs -0 git diff --name-status 8ebaf8daad 651150fc88 -- | awk '{print $1}' | sort | uniq -c
git diff --name-status 8ebaf8daad 651150fc88 -- projects/ROCKNIX/packages/sysutils projects/ROCKNIX/packages/hardware | grep -v 'quirks/devices/' | grep '^A' | cut -c1-120
git log --oneline 8ebaf8daad..651150fc88 -- projects/ROCKNIX/packages/sysutils/busybox projects/ROCKNIX/packages/sysutils/systemd | head -12
# the two seats' routes (expect two non-zero counts)
grep -c gemini-argon scripts/council-invoke.ts tools/lint-audit-artifacts
# the removal rule's own check against the dispatch tip (expect empty)
git diff --stat <dispatch tip> HEAD -- packages projects tools | tail -1
```

## 6. Outputs

As T11's brief § 6, with the folder `docs/audits/<yyyy_mm_dd>-epic-m6-os-system-services/`,
`second-opinions/` holding **two** seats' probes and refutations with
provenance and `review-plan.json` with two reviewers (T1's shape), the
audit issue `Audit: M6 T22 the OS's system services and platform quirks --
N findings (...)` as a sub-issue of #669, the bugs, and the retro at
`docs/retros/<date>-m6-os-system-services.md` (what T29 inherits: the
run-time selection lines, the *runs on* column; what the next base merge
settles). **`02` carries § The reachability table (one row per path, 422:
installed on / runs on / the deciding line), § The units (one row per
unit, 29: `ExecStart` masked, root, the writable path it touches, the
guard, enabled on which build), § busybox (the pin, the flagged applets
with their callers or `none`), § The upstream delta (the 44 M with each
finding's state at `651150fc88`, the 20 D, the 20 A), § The guest cycle
(the window's record, or *no window yet*), § The runs, § Proofs with
`proved:` cells, and a coverage table of 422.**

## 7. Acceptance

The checklist on #669 becomes this section at dispatch, written there by
the coordinator in place of P1's five generated ones. Every checkbox names
the artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-os-system-services/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-os-system-services/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: extended` and two reviewers from two other labs (`gpt` / `openai/gpt-6-astra` / `max`; `gemini-argon` / `google/gemini-4-argon` / `high`); each seat's probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named; `packet-manifest.json` lists every packet file with its sha256 and the scan's result; a seat that could not run is a named blocker on #669, never a substitute.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #346, #740, #797, #997, #1000, T29's #676), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the ticked and open counts read back by name.
- [ ] `reviewed-at:` and `fixed-at:` in the checklist's header carry the lane's commits; the read is on `8ebaf8daad`'s bytes for the 422 (`git diff --stat 8ebaf8daad <reviewed-at> -- $(cat .qa-scratch/t22/paths.txt)` empty) and nothing under `packages/`, `projects/` or `tools/` changes at stages A to D (`git diff --stat <dispatch tip> <stage-D tip> -- packages projects tools` empty; the dispatch tip is the one the dispatch comment names).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (422 paths, 16,604 lines; read 10,898 / fork-own 3,002 / 24 paths; tier 398 / 24; reach 422; written 422), the language dictionary with the `config` files named as read though not counted, the history (87; 33 fork; 54 upstream) and the upstream delta (44 M; 20 D of which 9 upstream never had, 2 upstream removed, 9 deleted; 42 A and 2 R), or each delta with its command.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `422`.
- [ ] `02-forward-audit.md` § The reachability table carries one row per path (422) with *installed on* and *runs on* (H700 / SM8550 / VM / none) and the deciding line (`system-utils/package.mk:14-15,27-34`, `quirks/package.mk:15-18`, `autostart:16-28,31-43`, `002-autostart:6-12`), its counts summing to 422 and naming the 8 install-time rows no shipped image installs and the 213 platform files no shipped unit runs.
- [ ] `02-forward-audit.md` § The units carries one row per unit (29): the file, `ExecStart` masked, `User=` present or root, the writable path it reads or runs (or none), the guard (or none), and enabled on which build (`system-utils/package.mk` has no `post_install`: the `enable_service` or preset that enables it, found by `git grep -n -E 'enable_service|preset' 8ebaf8daad -- projects packages config`, quoted, or *enabled by nothing in the tree* with that grep's empty result); `shell.service`, `autostart:71-77` and `:50-54`, `cron.service`, `udevil-mount@.service`, `userconfig-setup` and `video.service` each have their finding or their recorded design with the register searched (`tools/archaeology` quoted).
- [ ] `02-forward-audit.md` § busybox states the effective pin (1.36.1, `package.mk:7`, the http URL at `:11`, upstream's 1.38.0 with its seven patches named as renames of the override's own) and, for each flagged applet (`SUID`, `LOGIN`, `PASSWD`, `SU`, `HTTPD`+`CGI`, `NC`, `UDHCPD`), the caller in the tree (`git grep` quoted) or `none`.
- [ ] `02-forward-audit.md` § The upstream delta lists the 44 M with, for every finding on one of them, the file's state at `651150fc88` and whether the finding stands, is narrowed, or is *settled by the next base merge*; the 20 D split 9 never upstream's / 2 upstream removed / 9 deleted; the 42 A and 2 R by name; the two collisions (`99-coredump.conf` against `8bce25b3b7`; the sysctls against `54acd9556f`) each with a design sentence deferred to the coordinator.
- [ ] `02-forward-audit.md` § The guest cycle records the window the coordinator granted on #669 (the comment's time), the image by file name and BUILD_ID, each boot proof's line (the units enabled and their identities, tty1, the autostart order, `userconfig-setup`'s first boot), and the guest stopped by its pidfile -- or states *no window granted yet* with the proofs listed and their checkboxes open.
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass.
- [ ] `00-running-log.md` shows no build, no compiler, no plan generation, no fetch, no handheld, no guest outside the granted window, two `tools/council/run invoke` calls (the seats) and every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`, and no write under `/workspace/repos/rocknix*`, another lane's worktree or `/tmp`.
- [ ] `04-analysis.md` § Q3 carries the root-and-writable-path findings with their bug decisions and `Already written:` lines; § Q4 the pin table; § Q6 a disposition per unit (the 8, the 213 by platform directory, the 9), removals none; § Second opinion grades every item of both seats (confirmed, narrowed, refuted, new), the decisive ones re-read at their lines.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest` or `design`; every punch item carries `question:`; every `bug` passes `tools/box-check --issue N`.
- [ ] The retro exists at `docs/retros/<date>-m6-os-system-services.md`, is posted on #669, says what the slice did to the two time-to-play numbers (nothing, or the measured change if a unit on the launch path is named) and what T29 inherits.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge).

## 8. Stop conditions

As T11's brief § 8, with #669 for #658 and the 422 for the 58; **a failed
or unavailable seat is a named blocker at Phase 4.6, and `--member gemini`
is never called in Argon's place**; a guest boots only in the granted
window; nothing against a handheld.

**What never runs in this slice:** anything against a handheld; a guest outside the one window the coordinator grants on #669 (after the M7 lane's FINAL RETURN and T13's cycle); a third `tools/council/run invoke` beyond the two seats, or `--member gemini` in Argon's place; a build, a compiler, a plan generation, a fetch of any kind; any other `tools/council/run` call without `COUNCIL_ENV_FILE=/nonexistent` (`--help` included); an edit to any of the 422 or to anything under `packages/`, `projects/` or `tools/` at stages A to D; a push to any branch but the lane's own; `fork-worktree sync|remove|repair`; an edit to a rule, `CLAUDE.md`, `AGENTS.md`, a decided register row or `.github/sessions/saved-session-state-next.md`; a write under `/workspace/repos/rocknix*` or `/tmp` (use `/workspace/tmp/m6-t22/`); a credential-shaped literal written anywhere; `--no-verify`; bare `git stash`; `git worktree remove --force` or `rm -rf` on a worktree or a bare variable path.

## 9. Ceremonies owed

As T11's brief § 9, headed `#669`; `TMPDIR` under `/workspace/tmp/m6-t22/`;
commit messages `docs: ...` throughout (a read slice; a stage-E stream, if
any, comes with its own brief).

## 10. Hand-back

As T11's brief § 10, with `$S/t22-accept.sh` (the block; the two selection
greps; the units' `User=` count; the busybox lines; the history and the
upstream delta; the empty diffs; both seats' provenance; the lint; the
checkers; the simulated merge). After acceptance the coordinator carries
the *runs on* column and the units table into T29's brief. The merge
order: after T1's and T13's.

**The readings before dispatch** (plan § 3, principle 3): the area's
kickoff futro (T1's) gains a section for this slice from the coordinator;
a stranger's proof of this brief runs before dispatch; version 2 records
what each found.
