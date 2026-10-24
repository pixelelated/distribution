---
description: "Building, publishing, and safely flashing images for the handheld devices we test on, as distinct from the GENERIC_X64 VM build."
paths:
  - "**"
---

# Device builds

Upstream's guide is <https://rocknix.org/contribute/build/> and is the reference
for prerequisites and options. This file covers what it does not: our fork's
worktree layout, the devices we actually target, and the publish path.

**One correction to the upstream guide:** it says images land in `release/`.
They land in **`target/`** — `config/path` sets `TARGET_IMG=$ROOT/target`, and
`release/` survives only in a cleanup line in `scripts/build_distro`.

## Our devices

| Hardware | Target | Arch | Notes |
|---|---|---|---|
| Anbernic RG353M | `RK3566` | aarch64 | cortex-a55, neon-fp-armv8 (no crypto ext) |
| Anbernic RG35XX SP | `H700` | aarch64 | cortex-a53, crypto-neon-fp-armv8; maintainer's unit is LPDDR4 and uses the DDR4 image (`vdd-dram` = 1.1 V, verified 2026-09-05) |
| Anbernic RG SP | `H700` | aarch64 | cortex-a53, crypto-neon-fp-armv8; maintainer's unit is LPDDR3 and uses the DDR3 image (stock boot0 `dram_type = 7`, then ROCKNIX `vdd-dram` = 1.2 V, verified 2026-09-05) |
| Anbernic RG351M | `RK3326` | aarch64 | |
| Retroid Pocket Nova | `SM8550` | aarch64 | cortex-a710 / cortex-x3 (`projects/ROCKNIX/devices/SM8550/options`), crypto-neon-fp-armv8; upstream release 20260901 lists it under SM8550 -- #150, D-QA-023. Check the current build inventory before deciding whether a cold build is needed. |
| VM / QA | `GENERIC_X64` | x86_64 | fork-only device; see `generic-x64-vm-testing` |

The RG353M, RG35XX SP, and RG351M are *different build families* — separate
`-mcpu` and SIMD feature sets — which is why savestate compatibility across
them is an open question (fork issue #10, gated on #19). The RG SP is the
same-H700 control for the RG35XX SP. Do not assume a state from one loads on
another.

## Where things live

Since 2026-09-04 the build tree is on serval's dedicated 4 TB volume, following
the fleet's `/workspace` convention (lorry `fleet/blueprints/build-box.yml`,
`docs/runbooks/00-workspace-disk.md`):

| Path | Holds |
|---|---|
| `/workspace/repos/rocknix` | primary checkout, stays on `next` |
| `/workspace/repos/rocknix.worktrees/<name>` | build worktrees, siblings of the primary |
| `/workspace/cache/rocknix-sources` | the shared download cache (`SOURCES_DIR`) |
| `/workspace/artifacts/rocknix-images` | published/kept images |

It used to be `~/Development/rocknix{,.worktrees}` on the 1 TB OS disk, which
four device build roots plus the cache had filled to 36 GB free.

## Where to build

Freeze each engineering build in its own **`build/*` branch and worktree**,
from the published `next` commit named by its input manifest. Compare product
paths with the qualified GENERIC_X64 source and explain every difference before
building. VM-specific behavior must remain scoped to GENERIC_X64; never import
an old VM-only branch's shared concessions into a handheld image.

```bash
git worktree add -b build/<run-name> ../rocknix.worktrees/<run-name> <verified-commit>
```

The earlier shared `devices` / `test/qa-integration` distribution-build recipe
is historical. EmulationStation's separate repository still uses its own
integration branch; do not confuse it with this distribution build source.
Keep a running build's tracked inputs frozen. Build roots are per-device and
architecture (`build.pixelelated-H700.arm`, `build.pixelelated-H700.aarch64`, …).

A warm cache is reusable after its accepted source/output provenance and the
changed package/dependency scope are checked. If the predecessor still needs its
cache, make an independent copy and verify contents and inode separation. If all
old cache consumers have finished or been explicitly rebound, the existing
admitted atomic ownership-transfer route may move the stopped cache on the same
filesystem. Verify current process/container dependencies, preserve original
results and old firmware, and record unchanged device/inode at the new path.
The old cache path then ceases to be runnable; do not create a shared alias or
fallback copy after a failed move. Preserve the container path expected by
generated files. Never hardlink mutable caches. Retire superseded payloads after
their immediate verification dependency ends; keep compact receipts and required
corresponding-source inputs (D-INFRA-022).

## The build command

Use the canonical `make docker-<DEVICE>` target rather than a hand-rolled
`docker run` — it generates `.env` (via `scripts/get_env`), wires up uid/gid,
and mounts `${HOME}/.ROCKNIX/options` if present.

Two mounts must be added by hand for our layout, both through
`DOCKER_EXTRA_OPTS`:

```bash
D=/workspace/repos/rocknix.worktrees/<run-name>
S=/workspace/cache/rocknix-sources          # shared download cache

cd "$D"
DOCKER_EXTRA_OPTS="-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git -v $S:$D/sources" \
  make docker-RK3566
```

- **The `.git` mount is mandatory from a worktree.** A worktree's `.git` is a
  pointer file, and `scripts/image` runs `git rev-parse`; without the main
  repo's real `.git` the image step fails.

- **The sources mount is an optimisation**, not a requirement — it reuses the
  ~38 GB download cache instead of re-fetching hundreds of tarballs into a fresh
  worktree. Safe because `sources/` is a content-addressed download cache; build
  sequentially rather than sharing it between concurrent builds.

  A native build needs no mount at all: `config/path` reads
  `SOURCES=${SOURCES_DIR:-$ROOT/sources}`, so pointing at the shared cache is
  one variable — `export SOURCES_DIR=/workspace/cache/rocknix-sources` — with
  no symlink inside each worktree.

### Temporary directories belong to their execution environment (#549)

A private host TMPDIR is not automatically mounted in Docker. scripts/get_env
forwards it, so an unmapped host path makes package initialization fail at
mktemp before compilation. When using a host-only temporary root, explicitly
set the container TMPDIR to a writable container path (for example add
`-e TMPDIR=/tmp` to DOCKER_EXTRA_OPTS), or mount an intentionally shared path.
Retain the actual container environment readback; do not infer it from the
host variable. Config.Env may retain duplicate entries; verify the effective
value and a real temporary-file operation inside the running container. Preserve the failed owner and submit a fresh one after correction.

## After rebasing onto upstream

A build root that predates a rebase carries the *previous* tree's installed
artifacts. Those are not cleaned by a package version bump, so an incremental
build can fail in ways a clean build never does. Two things to do before
rebuilding:

1. **Verify the pinned build container.** `Makefile` names the pixelelated
   mirror by digest. `make docker-image-pull` retrieves that exact image; record
   the digest actually consumed in the build inputs. A newer host-tool
   requirement needs an explicit pin update, not an unrecorded latest tag.
2. **Expect self-hosting tools to break.** `config/functions` exports
   `LIBTOOLIZE`, `AUTOCONF`, `ACLOCAL` and friends **only if the toolchain
   already contains them**. On a clean tree libtool builds with no libtoolize
   present (the container ships none), so its own new `m4/` macros survive. On a
   warm tree the *previous* libtool's `libtoolize` is found, runs
   `--copy --force`, and overwrites the new macros with its older ones — so
   `libtool 2.5.4 -> 2.6.2` fails with `LT_LANG: unsupported language:
   "Objective-C"`, an error that names nothing to do with the real cause.

   The fix is to reproduce the clean-tree condition for that one package rather
   than delete the whole build root:

   ```bash
   rm -rf build.*/toolchain/bin/libtool build.*/toolchain/bin/libtoolize \
          build.*/toolchain/share/libtool build.*/build/libtool-* \
          build.*/.stamps/libtool
   rm -f  build.*/toolchain/share/aclocal/lt*.m4
   ```

   Note the sysroot copy at `toolchain/*/sysroot/usr/share/aclocal/` is a
   *separate* stale copy. Clearing only that one moves the error from
   `sysroot/.../libtool.m4` to `m4/libtool.m4`, which looks like progress but is
   the same bug — `libtoolize` re-clobbers it on the second aclocal pass.

This is an upstream defect, not a fork one: any developer with an existing build
root hits it on a libtool bump, and CI never does because CI is always clean.

3. **Check how stale the root actually is before patching anything.** A
   `projects/ROCKNIX/packages/<pkg>` override that does
   `. ${ROOT}/packages/.../package.mk` inherits `PKG_VERSION` from the generic
   recipe — but `calculate_stamp` (`config/functions`) hashes `$PKG_DIR`, which
   resolves to the **override** directory. The generic file holding the version
   is never hashed, so bumping it does not invalidate the stamp and the old
   build silently stands. 53 ROCKNIX packages use that pattern.

   After a big rebase, enumerate the damage rather than discovering it one
   failure at a time — compare each override's **effective** `PKG_VERSION`
   against `build.*/build/<pkg>-*`. On the 2026-08-19 rebase that showed **35
   stale packages**, among them openssl (3.5.1→3.6.3), glib (2.85.1→2.89.3),
   curl, expat, zlib and libfmt (9.1.0→12.2.0, a major ABI break).

   *Effective* is load-bearing. An override may set its own `PKG_VERSION`
   **after** sourcing the generic recipe, deliberately holding a package back —
   `gcc` (pinned 15.2.0 against a generic 16.2.0), `iwd` and `opus` all do. A
   sweep that reads only the generic file reports those as stale when they are
   working as intended, and "the compiler is stale" is exactly the kind of
   alarming false positive that stampedes a decision.

   The same is true of `PKG_SHA256`, `PKG_URL` and `PKG_ARCH`: read every
   field the build reads as the build reads it, per plan, through
   `config/options <pkg>` with `PROJECT`, `DEVICE` and `ARCH` set. An
   override's `case` branch can empty a checksum for some devices only
   (`libfmt` 9.1.0, `PKG_SHA256=""` for every non-SM device; #877,
   D-WORKFLOW-196), and an override's `PKG_ARCH` can exclude an arch the
   plan lists (`btrfs-progs`, `aarch64` only; #879). A count over recipes is
   a count over effective values (T7, 2026-10-24).

   **When core libraries are among the genuinely stale, wipe the build roots.**
   Clearing stamps individually leaves consumers linked against sysroot copies
   that no longer match their recipes — an image nobody should flash. The
   targeted fix in (2) is right for one isolated bump and wrong at this scale.
   `sources/` is a separate directory, so a wipe costs rebuild time but no
   re-downloading.

## A metadata-only upstream change still rebuilds everything

`calculate_stamp` hashes the whole package directory, not the version in it.
So a sweep that adds `PKG_SHA256` to hundreds of recipes — changing no
version, no source, no flag — invalidates every one of their stamps.

The 2026-09-04 merge brought 446 changed `package.mk` files. Separating them
mattered:

- **220** changed *only* by upstream's checksum sweep
- **226** changed substantively

and the practical answer is the same for both, because all 446 rebuild. That
inverts the usual reasoning about a warm build root: the question is not "how
much is stale?" but "is anything still valid?", and after a sweep like that,
almost nothing is.

So when a rebase includes a repo-wide metadata pass, do not price an
incremental build against a wipe — they cost nearly the same, and the wipe
also buys the clean-tree condition that avoids the libtool class of failure
above. Check `df` first: on this machine four device roots plus the source
cache came to 598 GB against 37 GB free, which made "rebuild in place" the
option that could not actually run.

`sources/` is separate and worth carrying across; the build roots are not.

## Late binding bites hardest in a merge

`packages/README.md` says toolchain and path variables exist only after a
package loads, so they belong inside functions. A merge is where a violation
surfaces, because the conflict makes you read code nobody has read since it
was written.

`ppsspp-lr` carried a fork patch that stripped an aarch64-only compiler flag
on x86_64. It sat at **file scope** and referenced `${PKG_BUILD}`, which is
empty there — so the `sed -i` edited `/CMakeLists.txt` and had never once done
its job. Nothing failed: the build succeeded, and the flag it was meant to
remove was simply never removed. It moved into `post_unpack()` during the
merge (`7650de7dd6`).

When resolving a conflict in a fork-added block, check the block was ever
correct before preserving it. A conflict is the cheapest opportunity to
notice, and `tools/pkgcheck` will not catch a variable that is merely empty.

## A killed build poisons every package that was in flight

Builds run packages in parallel, so a `Ctrl-C`, a SIGTERM or a machine
reboot does not interrupt *a* package — it interrupts however many were
compiling at that moment. Each is left with objects on disk and archives
built from an incomplete set of them.

The resumed build then fails at **link** time, with a message that points
nowhere near the cause:

```
undefined reference to `T11'          # while obj/emu/cpu/t11/t11.o sits right there
undefined reference to `cp_find_first_component(char const*)'
```

The object exists; it was archived out. Nothing rebuilds it, because as
far as make is concerned the archive is newer than the source.

**Do not fix these one at a time.** Each attempt burns a build phase to
discover the next casualty — 2026-09-02 went `mame2015-lr`, then `gdb`,
before anyone asked how many there were. There were four.

Enumerate them instead. The signature is a build directory that contains
compiled output but has no `build_*` stamp:

```bash
R=build.pixelelated-<DEVICE>.<ARCH>
cd $R/build && for d in */; do d=${d%/}; p=$d
  while [ ! -d "$R/.stamps/$p" ] && [ "${p%-*}" != "$p" ]; do p=${p%-*}; done
  [ -d "$R/.stamps/$p" ] || continue
  ls "$R/.stamps/$p" | grep -q '^build_' && continue
  [ -n "$(find "$d" -name '*.o' -o -name '*.a' | head -1)" ] && echo "POISONED $p ($d)"
done
```

The object-file test matters: a package that is merely *unpacked* also has
a directory and no stamp, and cleaning it costs an unpack for nothing.
Only the ones with compiled output were mid-flight.

**Test for a configured build directory too.** A package killed during
`configure` has no object files yet, so the test above misses it, and it
fails on resume with a message that names nothing useful — meson says
"Directory already configured" and then cannot find its own `build.dat`
(`glu`, 2026-09-05, the second failure of a GENERIC_X64 cold build whose
first failure had killed 22 packages in flight). Add
`[ -d "$d/.<target-triple>" ]` to the condition — the per-target build
subdirectory (e.g. `.x86_64-rocknix-linux-gnu`) exists once configure has
started — and treat it as poisoned like compiled output.

Then `rm -rf $R/.stamps/<pkg> $R/build/<pkg>-*` for each and resume.

**Before resuming a failed build, copy `.threads/logs` somewhere.** The
per-thread logs are per *slot*, not per package: `109.log` is whichever
package thread 109 ran last, and a resume reuses every slot. On 2026-09-19 an
H700 failure (`libxcb` relinking against a `usr/lib32/libc.so` that `ld` said
did not exist) was resumed on a guess about the cause, and by the time anyone
went to check which package had been writing the sysroot at that moment, all
of those logs carried the resume's timestamps. The cause is now unknowable
from that run. The build scripts archive the logs on any non-zero exit for
this reason; if you run `make` by hand, do it yourself first.

**If a resume fails the same way again after that sweep, stop clearing
packages and wipe the arch's build root.** At that point the state is not
enumerable and the rebuild is cheaper than the next three guesses —
`sources/` is a separate directory, so it costs time, not downloads.

Related but distinct: the libtool case above is a *stale* artifact from a
previous tree. This one is a *partial* artifact from an interrupted run.
Same class of symptom, different cause, same instinct — reproduce the
clean-tree condition for the affected packages rather than trusting an
incremental build to notice.

## A build that fetches its own dependency

pango 1.58 needs cairo 1.18 and the ROCKNIX override pinned 1.17.8. For
three months nothing failed: meson's `cairo.wrap` fallback cloned cairo's
git master at configure time, built it inside pango and installed it over
the pinned copy. `[DONE] build pango:target`, every time; every GENERIC_X64
and H700 image carried `libcairo.so.2 -> libcairo.so.2.11805.5`, an
unpinned build nobody had chosen (#226, blindspot 47). The first container
without DNS failed pango, which is how it was found — and upstream's CI has
DNS, so upstream ships the same thing and cannot see it.

- `scripts/build` now passes `--wrap-mode=nodownload` to every meson
  configure, target and host. A subproject may be used only when it ships in
  the tarball (glib's gvdb, kmsxx's pixpat); one that would have to be
  fetched fails the configure, and the failure names the dependency that is
  really missing. That is the message to fix, not the flag to remove.
- After a build, list what was fetched anyway:

  ```bash
  find build.*/build -mindepth 4 -maxdepth 4 -path '*/subprojects/*/.git'
  ```

  Empty is the only good answer, and only on a root where every package
  configured under the guard — a warm root keeps old clones for packages
  that did not rebuild. On the 2026-09-19 roots this listed exactly two:
  pango's cairo (built in) and glib's sysprof (cloned, then disabled).
- cmake's `FetchContent`, cargo and go vendoring have no equivalent switch.
  A recipe that builds one of those wants the same question asked of it.
- A pinned version in a recipe is a claim about the image only once the
  image is read: `unsquashfs -ll SYSTEM usr/lib | grep libcairo`. The
  package's install tree is what `scripts/install` copies, so a subproject
  a package built is in *that package's* `install_pkg/`, not the library's
  — cleaning cairo would not have removed it; cleaning pango did.

## A link error the source contradicts is the compile cache's until shown otherwise

ROCKNIX's ccache runs with `sloppiness = pch_defines,time_macros`
(`build.*/.ccache/ccache.conf`), which is what lets it cache compiles that
use a precompiled header -- and, in its manual's words, it "can't detect
changes in #defines" around one. On 2026-09-24 webkitgtk 2.54.0 failed its
final link on `undefined reference to
Inspector::DOMFrontendDispatcher::powerEfficientPlaybackStateChanged`, was
read as a fourth wall in WebKit's option graph, and was pinned for the
candidate (D-WORKFLOW-041). It was JavaScriptCore's `.gch`, served from the
cache under the configuration of the 2026-09-20 attempts, when video was
off: `cmakeconfig.h` said `ENABLE_VIDEO 1`, the preprocessed bundle carried
the definition, and the object compiled against the cached PCH did not; the
same bundle against a freshly built `.gch` did (#228, 2026-09-25).

So, when a build fails on a symbol, a type or a macro that the source and
`cmakeconfig.h` say is there:

- **Compare the object with the preprocessed source before the code.**
  `-E` does not use a precompiled header and `-c` does; a definition in the
  `-E` output and absent from `nm` of the object is a PCH, not a bug.
- **Rebuild the package with the cache bypassed** --
  `CCACHE_RECACHE=1 PACKAGE=<pkg> make docker-package` after a
  `docker-package-clean` -- before any patch or option change is written
  against the error. It recompiles everything and rewrites the cache, so the
  next build of the same configuration is warm again.
- **After a package's options change, expect it.** A recipe that flips a
  feature switch, and a bump that follows a failed attempt with other
  switches, are exactly when a cached PCH carries the old configuration.

The rebuild with the cache bypassed (x64 run 47) linked, and its
JavaScriptCore exported the method the cached one had not: 24 of the
dispatcher's methods against 23 (D-WORKFLOW-048).

## Verify helpers with the interpreter that will run them

A host Python syntax check does not qualify an in-container proof helper.
Before launching a long build, exercise new helper code in the exact pinned
container, including the file-reading or hashing operation it will perform.
On 2026-10-08, host Python3.14 accepted a helper using `hashlib.file_digest`,
but the build container's Python3.10 lacked it. The startup gate stopped before
compilation; streamed hashing passed against the actual accepted FEX files,
while the original helper remained a failing control (#492).
Keep host-only and container-executed helpers explicit, and retain the actual
interpreter version and runtime proof alongside the source seal.

## A two-minute build can be a real one

ccache sits under every compile, so a warm root that rebuilds one package
with one changed source file finishes in about two minutes, image step
included (H700, 2026-09-08: a one-file RetroArch patch plus a script change
in rclone, 04:43:46 to 04:45:34). That is not the signature of a build that
skipped the work. Judge a rebuild by evidence, not by duration:

- the package's `build_target` stamp under `build.*/.stamps/<pkg>/` is newer
  than the moment `make` started;
- the object for the changed file (`obj-*/…/<file>.o` in the package's build
  directory) is newer than that moment too;
- the binary inside the new image's `SYSTEM` squashfs differs from the one in
  the previous image (`tar -xf … --wildcards '*/target/SYSTEM'`, then
  `unsquashfs -d <dir> -n SYSTEM usr/bin/<binary>`).

Grepping the log for a phrase such as `build retroarch:target` is not one of
those — the log's progress lines say `install`, and a guessed pattern that
matches nothing reads as "not rebuilt".

## Before a build: the machine is memory-bound, not disk-bound

**Build monitoring is automatic (D-WORKFLOW-142, #394).** Normal make device,
image and package targets, direct `scripts/build_distro`, `scripts/image`,
`scripts/build_compat`, `scripts/build` and `scripts/install` enter
`tools/watch-build`. Docker builds enter on the host, before the container;
the relative run marker crosses the mount, and nested scripts reuse the run.
Interactive `docker-shell` and non-build helpers keep their normal behavior;
building from that shell arms a monitor inside that container.

Each top-level run prints its private `.build-runs/<id>/` directory and keeps
the combined log, runner/command/watcher PIDs, atomic `build.rc`, heartbeat
and run-owned `watch-job` copy. The runner holds one build lock per worktree,
refuses to start when the watcher cannot arm, and discovers the current
worktree's `build.*/.threads/logs` as cold roots appear. Existing commands
require a current `PIXELELATED_BUILD_ADMISSION` prepared from the measured
retention report (#493). An ad-hoc build uses `tools/watch-build --admission
RECEIPT -- COMMAND`. The guard binds source/profile/volume/protected identities,
rechecks capacity against unconsumed shared reservations, and refuses stale or
reused receipts before the payload starts. Native multi-ABI targets share one
outer admission. See `tools/host-maintenance/build-admission.md` for plans,
original-result consumption and retained-output release conditions. This first
gate does not implement automatic artifact deletion. Non-compiling QA and
record jobs use `--record-only`; nested compilation cannot inherit that mode.
Never pre-set or copy `RASTERATOPS_BUILD_RUN`/`RASTERATOPS_WATCH_EXEC`: these
are internal nesting markers, not an opt-out. A stale marker is refused.

**Result files belong to their producer (#597).** Once a job is submitted,
read its receipts; do not create, replace or pre-fill `tool-wrapper.rc`,
`launcher-result.json`, `runner-result.json`, `build.rc`, or any other file the
live owner will publish. Submission exit0 describes submission only. Put any
coordinator observation in a separately named review record; it is never the
producer's original wait status. If result publication fails after the work,
preserve that failure and use an explicit reviewed recovery path. A missing
channel stays missing; do not manufacture a launcher receipt or rerun a
successful producer solely to obtain cleaner paperwork.

The CI lifecycle/routing controls exercise actual entrypoint prefixes and
Makefile recipes, including a removed-hook failing control. A run started
from an older frozen checkout keeps that checkout's tooling; attach a current
run-owned watcher explicitly, as M7 cold01 does, without advancing its source.
For all runs, status recording and notification remain separate. Before a
long run, verify the delivery path and follow active supervision in
`engineering-practices.md` (D-WORKFLOW-143, #395). Off-session notification
is not yet configured; do not describe a detached recorder as an alert
service. A runner killed outright may leave its command alive: inspect `command.pid`
before starting a replacement build.

`tools/build-preflight` reports it and `--stop-vms` stops guests explicitly.
Before a future cold build, `tools/build-preflight --reclaim-swap` can invoke
our installed root-owned fixed-target helper (D-INFRA-015, #410). Run this
**before** the watcher/build; the helper refuses active compilers, watchers
and guests. It needs used-swap RAM plus16GiB reserve, checks the actual
`/swap.img` configuration, and verifies reactivation. Default preflight stays
read-only. Installation uses a narrow exact-action sudo grant, never general
passwordless sudo or privileged Docker. See `tools/host-maintenance/README.md`
for reviewed installation, isolated tests, limitations and recovery. A
missing/refused helper is a failed preflight, not permission to bypass it.
Stop guests separately and wait for exit before requesting reclamation.

Recheck preflight after large cache preparation and before the compiler's
watcher starts. A file-copy workload can refill swap even when available RAM
is ample, so a passing check before that copy does not qualify the later
build. If reclamation is needed, first consume the cache job's terminal
results and verify its actual owner/watcher exits; then use the same guarded
helper while idle. Never recycle swap while the copy's watcher is active.

The two constraints are easy to confuse because one of them is never a problem:
`/workspace` has terabytes free while the box runs out of RAM. On 2026-09-19 a
cold GENERIC_X64 build reached `webkitgtk`, compiled WebCore at
`CONCURRENCY_MAKE_LEVEL=nproc=24`, and the kernel killed `cc1plus` twice:

```
x86_64-rocknix-linux-gnu-g++-15.2.0: fatal error: Killed signal terminated program cc1plus
```

**What made it expensive was the collateral, not the failure.** The same
pressure killed a running QA guest and a background watcher, so the first
symptom was silence: a build that had been dead for two hours, a guest whose
monitor socket had no owner, and nothing that said so. A memory failure does
not announce itself the way a compile error does.

So, before a cold build:

- **Stop the QA guests you are not using.** Each QEMU guest holds about 2 GB
  and they are routinely left up for days. They are also what the build kills
  first, so leaving one up is not a neutral choice — it is choosing to risk
  whatever state it holds.
- **Look at swap, not just RAM.** A full swap means the cushion is gone: the
  next spike has less cushion. Use the guarded pre-build helper above;
  do not run a broad swapoff or recycle during active work. Available RAM and
  memory pressure still need supervision after a passing preflight.
- **Cap the heavyweight packages rather than the whole build.** `webkitgtk`
  carries `PKG_MAKE_OPTS_TARGET="-j4"` for this reason; `ninja` takes the last
  `-j` it is given and `scripts/build` appends the package's options after
  `NINJA_OPTS`, so one package narrows without slowing the other six hundred.
  Find them one at a time with evidence rather than lowering
  `CONCURRENCY_MAKE_LEVEL` globally (maintainer, 2026-09-19: optimise for a
  build that finishes, even if it takes longer).

## Budget

- **Disk:** measure the actual target's roots, source cache, temporary copy and
  artifact reserve before starting. The accepted October 2026 H700 roots used
  about138 GB together and SM8550 about183 GB; a generic90 GB estimate is not
  a capacity gate. Recheck available space between sequential target builds.
- **Time:** hours for a first build of a device; minutes once its root is warm.
- Build sequentially. Parallel device builds contend for CPU and the sources
  cache, and a failure part-way is harder to attribute.

## Build credentials

Four optional secrets are compiled **into the EmulationStation binary** when
present in the build environment: `SCREENSCRAPER_DEV_LOGIN`
(`devid=…&devpassword=…`, a developer pair ScreenScraper issues via its forum —
a member login is not accepted in its place), `CHEEVOS_DEV_LOGIN`
(`z=<user>&y=<web API key>`, per RetroAchievements account), `GAMESDB_APIKEY`,
`HFS_DEV_LOGIN`. Without them the matching scraper is not built — **except
ScreenScraper on fork builds**: #64 enables `SCREENSCRAPER_RUNTIME_DEV_LOGIN`,
so the scraper remains available without a compiled pair. Under #566 /
D-WORKFLOW-166, pre_configure_target supplies the selected shared JELOS developer
identity when no explicit build override is set. Existing compiled-pair precedence
hides developer-entry rows; the player's account remains separate. An intentional
local override still works but does not receive the shared-identity release-check
exception. A build without a compiled pair retains the runtime developer rows.
#586 tracks replacement credentials later; it is not a current-candidate gate.
Recipe selection and selected-state controls passed on the VM; actual rebuilt
binary, UI/frame, backup and clean/upgrade image qualification remain under #566.
Never embed personal player credentials as the developer default.

They live in **`~/.ROCKNIX/options`, mode 0600, as `export` lines** — the
Makefile includes that file on the host and in the container. Nothing else
needs to know them. The maintainer's rule (D-INFRA-006): builds are local, so a
value in a build log is tolerable; a value leaving through a build or through
git is not. D-WORKFLOW-166 narrowly refines this for the selected shared
ScreenScraper developer identity; unrelated private values stay excluded.
Current controls and the historical guard boundary:

- `scripts/get_env` forwards the environment into the container **minus
  anything secret-shaped**, except those four by name. It used to forward
  everything, which put the developer's shell tokens into a world-readable
  `.env` and every container. `.env` is now 0600 and removed when the
  container exits.
- The ES recipe logs `USING: <key> (set)`, never the value.
- D-INFRA-007 describes a historical binary-credential guard. The current
  `tools/fork-publish-release --prepare` only prepares a release plan and runs
  #565's selected-state inspection, including known compiled ScreenScraper/RA
  pair patterns. #566 allows only the exact NUL-delimited shared developer pair
  in the ES ELF, not seeded settings or personal accounts. Credential surfaces
  outside that selected policy remain a separate gate. Do not claim the old binary scan or
  `FORK_ALLOW_EMBEDDED_CREDENTIALS` override still executes. #566 must qualify
  actual artifact checks for the chosen provisioning route, preserving private
  credential exclusions rather than disabling checks broadly.
- `.githooks/pre-push` scans every pushed branch (`fork-workflow.md`).

The maintainer's rule, verbatim: *"if the build is only being generated on my
build server and only being played by me, the key can be in my build, but
beyond that, it needs to be stripped out."* So personal credentials in the
options file are fine for images that stay here and on your own devices;
anything anyone else can download is built without those personal credentials.
The separately selected shared developer identity is covered by D-WORKFLOW-166.

## Publishing

**A cut is called a release candidate only after `tools/rc-preflight`
has run on its tree** (`release-candidates.md` step 0, #271): packages
current, both bases level with ROCKNIX, no bug without a disposition, the
record clean, or each finding accepted by a register row. Its last line --
`rc-preflight: <branch> at <id> -- MAY BE CUT` or the findings -- is
quoted on the round's issue and carried in the candidate's RECORD.txt.

New build identities follow `docs/releases/versioning.md` (D-WORKFLOW-157).
Image assembly freezes semantic version, UTC timestamp and source commit;
filenames and `.identity.json` sidecars carry that identity. Preserve a common
BUILD_TIMESTAMP for a coordinated device set, then use a fresh timestamp for
another set. Same-day outputs are distinct; existing identities cannot be
replaced. Source BUILD_ID and immutable manifest/SHA256 remain the provenance.

`tools/fork-publish-release --prepare <immutable-bundle>` emits a checked local
GitHub naming/asset plan only. The old date/newest-file/clobber/undraft path is
retired. Publication still requires #265/#344's qualified transaction and #528's
source/custody gates; preparation creates no tag, draft or public release.
D-WORKFLOW-159/#532 selects only public `-rc.N` and unqualified release versions;
`dev` remains engineering-only. Record a never-reused RC allocation per frozen
source/timestamp set; reset at1 for the next patch target. Tags/titles use the
release version, filenames retain UTC/source metadata. Reassemble and qualify
new bytes when dropping the RC suffix; never relabel prior firmware. The
reusable `tools/build-identity-test` verifies actual metadata/plan blocks with
synthetic fixtures. Actual next-image proof remains required.

## Installing on the device

**Ask before the transfer and before the reboot** (`engineering-practices.md`
§ "Never reboot, update, or power-cycle a device without asking"; D-QA-011).
Staging the tarball in `~/.update` is inert until the next boot, but the copy
is a question too — it can be answered once for a batch; the reboot is asked
for each time, by device.

For a fresh card, follow `docs/device-flashing-runbook.md`. It covers artifact
intake, physical board-variant evidence, removable-disk identification, full
byte readback, and the platforms where a device-specific file from
`device_trees/` must be activated as `/dtb.img` before first boot. Presence in
`device_trees/` alone does not make a card bootable when extlinux points to
`/dtb.img`.

For an in-place update, push the `.tar` to a running device's updater — `scp`
it to `root@<host>:~/.update` and reboot, which preserves settings. Do not use
the fresh-card procedure for an update.

H700 emits two flash images (DDR3 and DDR4) but **one update tar for both**.
The updater selects the RAM-specific bootloader and running model's DTB.
Follow the runbook's update section to stage outside `.update`, verify the
device-side checksum, then move the complete tar into the update queue. Keep
same-day builds in separate artifact directories and record `BUILD_ID` plus
checksums; the date and filename alone do not distinguish them.

## Iterating on EmulationStation

**Upstream PRs for ES go through a different fork.** `~/Development/emulationstation-next`'s
`origin` (`pixelelated/emulationstation`, from its `git remote -v`) is a GitHub fork of
*batocera-linux/batocera-emulationstation*, so it is outside ROCKNIX's fork
network and GitHub refuses a PR from it into `ROCKNIX/emulationstation-next`
("Head repository can't be blank"). The fork that works is
`maxengel/emulationstation-next-rocknix` (remote `rocknixfork` in the PR
worktrees under `~/Development/emulationstation-next.worktrees/`): branch from
`upstream/master`, cherry-pick the commit, push there, then
`gh pr create --repo ROCKNIX/emulationstation-next --base master --head maxengel:<branch>`
(2026-09-07, ES PR #33).


**`EMULATIONSTATION_SRC` only mounts the directory — it does not build from it.**
The `docker-%` target turns it into a `-v` bind mount and nothing else;
`emulationstation/package.mk` never reads the variable, so the package still
fetches and builds `PKG_VERSION` from `PKG_GIT_CLONE_BRANCH`. Setting it and
assuming the local tree was compiled produces an image with none of your
changes and no error to say so — the build log still reports
`[DONE] build emulationstation:target`, because it did build, just not your
source. Verify with `strings <image>/usr/bin/emulationstation | grep "<a
string you added>"` rather than trusting the build to have used it.

To actually ship an ES change: push the branch, merge it into the branch named
by `PKG_GIT_CLONE_BRANCH` (`test/qa-integration`), and bump `PKG_VERSION` to
the new commit. The mount is still worth setting alongside:

```bash
EMULATIONSTATION_SRC=~/Development/emulationstation-next.worktrees/<branch> \
  DOCKER_EXTRA_OPTS="..." make docker-RK3566
```

Note that a package's source change does **not** always retrigger a rebuild:
clear its stamp first (`build.*/.stamps/<pkg>/`), and delete
`build.*/.stamps/image/build_target` to force a fresh image.

## Reading a crash

Since the seventh cut of the 2026-09-22 round (#246), EmulationStation's
signal handler writes a backtrace to stderr before it dies of the signal:
in the journal, under `start_es.sh`, a line `EmulationStation crash
backtrace (innermost first; symbolise with addr2line):` followed by one
frame per line, `emulationstation(+0x...) [0x...]` or `libfoo.so(sym+0x..)`.
Before that the handler logged one line and called `exit()`, so the only
core the keeper could have caught described the teardown, not the fault.

Both builds' `emulationstation` binaries are unstripped, with debug info,
in the build root (`build.pixelelated-<DEVICE>.<ARCH>/build/emulationstation-<pin>/emulationstation`),
and both toolchains carry a symboliser -- **the build that produced the
image, so match the pin in the directory name to the device's BUILD_ID**:

```bash
# H700 (aarch64):
B=/workspace/repos/rocknix.worktrees/devices/build.pixelelated-H700.aarch64
$B/toolchain/bin/aarch64-rocknix-linux-gnu-addr2line -f -C -i \
  -e $B/build/emulationstation-<pin>/emulationstation 0x<addr> 0x<addr> ...
# GENERIC_X64:
X=/workspace/repos/rocknix.worktrees/generic-x64/build.pixelelated-GENERIC_X64.x86_64
$X/toolchain/bin/llvm-addr2line -f -C -i -e $X/build/emulationstation-<pin>/emulationstation 0x<addr> ...
```

`backtrace_symbols_fd` prints `emulationstation(+0xOFF)` for the main
binary; feed addr2line the `+0xOFF` value when the binary is
position-independent (`readelf -h | grep Type` says `DYN`), the absolute
`[0x...]` when it says `EXEC`. A frame in a shared library is symbolised
against that library from the same build root's `image/system/usr/lib`.

A core, when `rocknix-corekeep --on` has been armed on the device
(`/storage/.cache/log/cores/core.<exe>.<epoch>.<pid>.gz` + `.txt`), is
read with gdb on the host against the same unstripped binary -- the host
needs `gdb` (or `gdb-multiarch` for an aarch64 core) installed, which it
was not on 2026-09-22. The core holds whatever the process held, tokens
included: copy it with scp, read it here, delete it when done.
