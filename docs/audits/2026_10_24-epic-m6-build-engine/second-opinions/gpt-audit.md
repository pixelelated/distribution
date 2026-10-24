## 1. Additional findings

These are conditional code defects and unsafe seams, not claims that a failed build or security incident was observed.

- **G-01 — High — `scripts/get_git:26–34,36–51,199`:** A failed `pushd` does not stop the cache check because the function is called in an `&&` list; an existing but inaccessible cache directory therefore sends `git clean -fdx` against the caller’s working tree. Rejection paths also return without balancing the successful `pushd`.
- **G-02 — Medium — `scripts/get_git:26–28,34,199`:** Cache cleaning leaves tracked working-tree edits intact: `git restore --staged .` resets the index, not those files. A failed `git clean` is also hidden when the following restore succeeds, allowing an incompletely cleaned cache to be accepted.
- **G-03 — Low — `scripts/get_git:194–206,239`:** Bare `main` drops the handler’s arguments, so `lock_source_dir "${1}"` and the GET message receive an empty package argument on every invocation.
- **G-04 — Low — `scripts/get_git:15–16,36–38`:** With enough refs, `grep -q -m1` exits while Git is still writing; Git’s resulting SIGPIPE makes `pipefail` reject a valid cache and unnecessarily enter the fetch/update path.
- **G-05 — Medium — `Makefile:179,205–208`:** Concurrent Docker targets in one worktree share `.env`; either invocation can remove, replace or clean up the other’s file before Docker reads it. The watcher starts after these operations, so its lock does not protect them.
- **G-06 — Medium — `scripts/get_env:16–22`; `Makefile:207–208`:** A failed `echo` is not retained as the script’s result. If a later, final iteration drops a variable and executes `continue`, the script exits successfully and the Makefile starts Docker with an incomplete `.env`.
- **G-07 — Medium — `Makefile:153,207–208`; `scripts/get_env:14–21`:** For an exported `EMULATIONSTATION_SRC`, the target-specific assignment replaces the source path with a `-v "source:source"` argument string; `get_env` forwards that string as the variable’s value, corrupting the container-side setting unless another configuration source restores it.
- **G-08 — Medium — `scripts/get_archive:4–11,57`:** `STAMP_URL` is checked only for existence. When `PKG_URL` changes but the cache filename stays the same and no checksum is supplied, the old URL’s archive is accepted without fetching the new source.
- **G-09 — Low — `scripts/get_archive:23,33–35,40–49`:** Unsetting `DISTRO_MIRROR` does not disable the mirror: the inserted slash makes `PACKAGE_MIRROR` nonempty, so a failed primary download is followed by a bogus `/…` fallback.
- **G-10 — Medium — `config/build-identity:36–43`:** A failing `git status` that produces no standard output is treated as a clean checkout; its exit status is discarded, and the function exports `BUILD_DIRTY=no` rather than refusing the identity.
- **G-11 — Low — `scripts/image:74–75,111–124`:** The sidecar writer does not JSON-escape strings. An image suffix containing a quote or backslash produces invalid JSON or a different decoded image name without making the writer fail.
- **G-12 — Medium — `scripts/image:74–81,111`:** The duplicate guard interprets the literal image name as a glob. With a suffix such as `[x]`, it does not match the existing filename containing literal brackets, so a direct image invocation can bypass the refusal and overwrite that identity’s files.
- **G-13 — Medium — `config/functions:1114,1126–1129`; `scripts/unpack:107–108`:** Stamps omit permission bits, symlink identity and dotfiles—even explicitly listed dotfile dependencies. Mode-only edits or symlink retargets to equal-content files leave the stamp unchanged although copying the sources can produce different installed files.
- **G-14 — Low — `config/functions:1180–1186,1201–1204`:** Wildcard lookup ignores the requested file type. A directory matching a file search, or a regular file matching a directory search, is accepted and prevents fallback to a correctly typed match.
- **G-15 — Low — `distributions/ROCKNIX/config/functions:144–157`:** Fragment values are inserted into XML without escaping; a literal `&` or `<` in metadata or a command corrupts the generated table.
- **G-16 — Medium — `scripts/build_distro:72–78`:** Every package-clean failure loses both its diagnostic and its status. A real failure to invalidate a package therefore lets the device build continue without the requested cleanup.
- **G-17 — Medium — `scripts/build_distro:44–64`:** `DEVICE_ROOT` link setup mishandles existing destinations: a dangling build symlink is never replaced, while an existing real `sources-${DEVICE}` directory receives a nested symlink instead of becoming the intended shared-cache link.
- **G-18 — Medium — `scripts/unpack:94–100,112–117`:** If the declared source directory is absent from the extraction, the fallback moves a same-named directory out of the shared build root without checking that this unpack created it; an unrelated package tree can become this package’s source.
- **G-19 — Medium — `scripts/mkimage:31–34,49,324–334`:** The SIGINT handler cleans up but does not exit. An interrupt after the last checked operation can resume execution and finish with status zero instead of reporting cancellation.

## 2. Review of the first reader’s findings

### F-01 — Survives, Medium

The name-filter failure is established, not merely suggested by naming conventions. P1’s `tools/sb-get-env.sh` output keeps the six listed names, and `Makefile:208` supplies the resulting file directly to Docker. The owner-only file mode does not prevent disclosure to container processes (`scripts/get_env:14–21`; `Makefile:207–208`).

**What would make it false:** a later filter that removes those variables, or a container invocation that does not consume them. The packet shows neither. It proves forwarding of fixture values, not leakage of an actual credential.

### F-02 — Survives, Medium; narrow the override claim

The newline injection is directly established by P1 and `scripts/get_env:21`. Importing an exported host value through a bare-name line rests on the Docker contract quoted in the packet, not a Docker execution.

The statement that “the rest” of the variables are not protected by later `-e` arguments is too broad: `RASTERATOPS_BUILD_RUN`, `BUILDER_NAME` and `BUILDER_VERSION` are also explicitly supplied, alongside `PROJECT`, `DEVICE` and `ARCH` (`Makefile:208`).

**What would make it false:** rejecting multiline values, rejecting the injected env-file syntax, or overriding every injected variable. P1 disproves the first; the quoted Docker contract contradicts the second; `Makefile:208` does not provide the third.

### F-03 — Survives, Medium

The installed wrong years are established by P7’s two install-tree readings. The command carry-over is independently established by P6, not inferred from the years. The cause is visible: sourcing into shared state, followed by a default only when `SYSTEM_COMMAND` is empty (`distributions/ROCKNIX/config/functions:127–153`).

Narrow “the next system appended launches nothing” to **a following system that does not supply its own command**. A fragment that explicitly sets its command does not have that failure.

**What would make it false:** resetting or initializing the fragment fields between registrations. The supplied function does not do that, and P6 demonstrates the resulting carry-over.

### F-04 — Survives, Medium; the proposed repair is incomplete

P4 establishes malformed XML and a failed build step; P5 establishes successful generation with two defaults. Case A is **not success reported over failure**: its reported status is 2. Its additional defects are the missing diagnostic and truncated output (`distributions/ROCKNIX/config/functions:113,209–214`; P4/P5 outputs).

Changing the selector to `core[last()]` fixes accidental marking of earlier cores. It does **not** enforce one default: two explicitly true rows would then produce two well-formed default attributes on different cores.

**What would make it false:** selecting only the intended core and independently rejecting multiple defaults. The packet shows neither. The clean current tables limit present exposure; they do not refute P4 or P5.

### F-09 — Survives, Medium

For the normal matching `./target` prefix, the ordering is decisive: deletion happens before `make image`, and the image guard checks for files that have already been removed (`scripts/build_distro:81–99`; `scripts/image:78–82`).

This establishes replacement risk in the worktree’s output directory. It does not establish replacement in a publication or candidate store: the destructive command names `./target` only.

**What would make it false:** checking the identity before deletion, excluding that identity from deletion, or using an output location outside the prune’s match. The supplied default route has neither of the first two protections. The three one-identity directory listings are consistent with the defect but are not its proof.

### F-16 — Survives as High, with a narrower statement

Unchecked copy or compression failures can be followed by successful cleanup and a zero exit. The later filesystem check does not verify that the expected kernel and `SYSTEM` bytes were copied; hashing the resulting archive does not establish that either (`scripts/mkimage:252–280,324–334`).

Two claims need correction:

- The script does **not always exit zero**: checked failures call `show_error`, which exits 1 (`scripts/mkimage:36–46,53`).
- A compression failure does **not guarantee a checksummed output**: the checksum command can also fail, and that failure is unchecked (`scripts/mkimage:324–330`).

**What would make the finding false:** an effective fatal-error guard covering these operations, or an enforced final contents check before success. Neither is shown in the writer. The sourced device/project hooks are omitted, so the specific assertion about the current SM8550 route remains unverified (`scripts/mkimage:260–263`).

**High is justified for the demonstrated error-handling design:** the artifact-producing stage can return success without a complete usable image. No damaged Nova image or device incident was demonstrated.

### F-17 — Survives, Medium; narrow it to missing invalidation

P12 proves that changing the selected device file does not change the stamp. The relevant recipe’s declared inputs and the engine’s hash inputs support that result (`projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk:10,39`; `config/functions:1112–1126`).

“Ships the old firmware set until someone cleans by hand” goes beyond that proof. The device entry has automatic clean lists whose contents are not supplied (`scripts/build_distro:69–78`).

**What would make the stale-firmware outcome false:** another hashed dependency covering the file, unconditional rebuilding on every applicable route, or reading the list afresh during installation without reusing stale package output. The packet disproves the first for its fixture; it does not settle the other two for real builds. The missing stamp dependency survives; an affected shipped image is not established.

### F-18 — Survives only as Medium; High is not established

P13 proves the faulty acceptance condition: a matching non-HEAD ref satisfies the check, and the cached path exits without running `_get_repo` (`scripts/get_git:36,199–212`).

The packet does **not** establish the claimed ordinary pin-bump-to-wrong-image sequence:

- It does not show how `PACKAGE` is keyed.
- It does not show whether extraction selects the requested commit independently.
- Exiting the fetch handler does not prove that its caller’s later extraction cannot select the pin (`scripts/unpack:84–85`).
- The displayed fresh-path verification compares HEAD with optional `PKG_GIT_SHA`; merely collecting HEAD is not itself a comparison with `PKG_VERSION` (`scripts/get_git:215–232`).

**What would make the wrong-source claim false:** version-separated caches or an extractor that always selects and verifies the requested commit. The packet shows neither guarantee, but it also omits the code needed to exclude them.

The cache-validation gap survives. **High does not survive on this evidence**, because the claimed wrong-source artifact has not been connected to the acceptance bug. A repair must also respect the documented abbreviated commit form (`scripts/get_git:8`).

### F-19 — Survives, Medium

The fresh-download condition is explicit: certificate verification is disabled, and an empty expected checksum accepts the download (`scripts/get_archive:25,43–45`). The updater deletes directly declared checksum lines and then searches for a placeholder it has deleted (`scripts/update_packages:50–61`).

Narrow the exposure: a fresh download with a correct, trusted expected checksum is still checked against that checksum. The packet does not count active image recipes lacking one. The updater’s broken checksum edit is established; its claimed effect on every possible inherited recipe arrangement is not.

**What would make it false:** mandatory verification of the actual archive against a trusted expected digest before use, or verified TLS on the otherwise-unhashed route. The supplied download path has neither. Existing cache acceptance also checks a stamp rather than archive bytes (`scripts/get_archive:4–7`).

### F-20 — Survives, Medium; “on every entry” is false

The script attempts host changes without an explicit setup-only boundary, but not on every invocation:

- Compiler changes require Debian/Ubuntu, `gcc-12`, `sudo`, and a query result without `gcc-12` (`scripts/checkdeps:296–306`).
- `/nix` preparation returns immediately when the directory is already writable (`scripts/checkdeps:324–326`).

The compiler query also does not mean “gcc-12 is selected”: it searches the entire alternatives query, including registered alternatives (`scripts/checkdeps:299–300`).

**What would make the surviving finding false:** restricting mutations to an explicit opt-in/setup action, or reporting unmet requirements without changing the host. The shown entry calls `checkdeps` directly, and `prepare_nix_dir` is called without such a gate (`scripts/build_distro:17`; `scripts/checkdeps:345`). No host mutation was executed by this audit.

### F-15 — Raise from Low to Medium

This is a functional entry-route mismatch, not just documentation. With credentials/settings only in the documented uppercase file, and without equivalent exported variables, a direct script invocation reads different configuration from Make (`Makefile:1,147`; `config/options:132–140`).

**What would make it false:** both spellings resolving to the same file, explicit loading of the uppercase file by the scripts, or all required settings already being exported. The packet’s `test -f`/`stat` checks establish separate paths on this host; the supplied script code does not load the uppercase file. The actual shell exports and compiled credentials were not inspected, so this is not proof of a particular credential-less image.

### F-22 — Split the verdict

**The `distclean` half survives, Low.** An unmatched build-root glob makes `chmod` fail under `set -e`, before removal of `.ccache` (`scripts/makefile_helper:6,25–27`).

**The statistics half does not survive for the shown image route.** `start_multithread_build` is called on the left side of `||`, which disables `errexit` within the function. The statistics pipeline does not assign failure to `result` (`scripts/image:104`; `config/multithread:62–69`).

**What would make the cleanup finding false:** handling the `chmod` failure or performing cleanup before it; neither is shown. **What would establish the statistics finding:** an unguarded caller with active `errexit`. The packet supplies no such caller. Keep the cleanup defect; withdraw the asserted statistics-induced image failure pending that evidence.

## 3. What the packet does not establish

- **End-to-end cached-source selection.** Supply the cache-path construction, `_get_repo`, extraction implementation and `lock_source_dir` body. P13 tests the acceptance predicate, not the final source tree used by a package; the empty argument at `scripts/get_git:196,239` also cannot be graded as a broken lock without the lock implementation.

- **The current SM8550 failure path.** The sourced bootloader hooks can alter shell options and control flow, but their bodies are absent (`scripts/mkimage:260–263`). A fault-injected copy/compression/checksum test would establish status propagation without requiring a complete firmware build. Bootability still requires an assembled image.

- **Actual warm-build firmware staleness and settings loss.** P12 proves a stamp omission, not a shipped stale firmware set. The automatic clean-list values are missing (`scripts/build_distro:69–78`). Likewise, the path mismatch in F-15 does not reveal what a real invoking shell exported (`config/options:132–140`).

- **Docker integration and concurrency.** P1 establishes generated text only. `test-build-monitor` reports 36 passes against stub payloads and a stub Docker command, not real env-file parsing or concurrent `.env` ownership. The 134-checkout `.env` scan establishes absence at inspection time, not safety during execution (`Makefile:205–208`; the recorded test and scan outputs).

- **Input restrictions for the serialization findings.** The displayed writers permit the conditional failures in G-11, G-12 and G-15; the packet does not establish whether all supported configuration inputs prohibit those characters (`scripts/image:74–81,111–124`; `distributions/ROCKNIX/config/functions:144–157`). No current malformed sidecar or fragment was demonstrated.

- **The unreviewed execution core and workflow steps.** Successful `py_compile` results do not establish scheduler, dependency-plan or bootloader-helper correctness. The planner and builder are on the live path (`config/multithread:49–62`). Workflow run conclusions establish the listed outcomes, not their causes: the three `update-kernel-configs-docs.yml` failures alone do not prove missing secrets caused every failure. `actionlint` was not run.

- **Release integration.** `tools/build-identity-test` reports **21 passed, 2 failed**, with `synthetic_only: true` and `assembled_image_tested: false`. That supports the named identity cases, not a completed public release plan or an assembled image’s identity contract. Calling the failures “expected” does not turn those two checks into passes.

- **Container contents and performance.** Manifest/config inspection establishes dates, platform and differing layer identifiers—not which packages or security fixes changed. Identical Dockerfiles do not prove that all differences are Ubuntu package updates. The recorded warm-run totals do not isolate image assembly, watcher overhead or ccache effectiveness; the packet reports no ccache statistics or time-to-play measurement.