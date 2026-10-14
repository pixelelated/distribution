# Generated documentation and frozen build admission: source proposal

Source-only follow-up to the engineering plan at commit
`ca47c2e314f6dc67821de50164f8b09726acb584`. No production file was changed and
no fixture, compiler, Docker container, VM, service, or package hook ran here.
Root owns issue recording, runtime allocation, integration and publication.

The expected next image build has a concrete source-level admission conflict:
the emulator metapackage generates a tracked documentation file, and a later
image task must re-enter the admission guard which requires unchanged tracked
source. This packet proposes redirecting that generated output into the admitted
build root. It does not weaken `source_state()` or exempt tracked documentation
from real-source mutation detection.

## Archaeology and exact later boundary

Read full live #493 body/comments on2026-10-14 and its current implementation
commit `d7e2d6be411675003d04e92f8801e49ed587cc8b`. The published admission packet
explicitly proves synthetic/fake-Docker routing and a1KiB host lifecycle, with
no actual full image build. Neither the implementation nor #493 contains a
generated-document exception. `source_state()` has not changed since that
introduction. No original full-image admission failure is claimed here.

`tools/archaeology --no-gh 'generated' 'doc'` and `--no-gh 'admission'` completed.
The former found the existing generated-output lesson in
`f61d1a1bbe54fad35a3ec6c1789b787d00e7bcdd`: upstream Dolphin intentionally creates
scmrev.h and Flatpak metadata after configuration. That packet classified those
byproducts instead of weakening source checks; it did not handle this distro
documentation path. Earlier accepted replacement20 predates admission.

`git log -S` and blame show the documentation generator and path originated in
`2de9ea57e64647d5c564ec5d12e2de26a59b292e` (July2025). Its source-tree output was
intentional. The proposal preserves that behavior for direct documentation
generation without a watched-build marker.

The causal call chain is:

1. `scripts/build_distro` cleans `emulators` through CLEAN_OS_BASE; image assembly
   invokes `start_multithread_build image` in `scripts/image`.
2. `config/multithread` obtains the real package plan through pkgjson/genbuildplan
   and pkgbuilder. The image package depends on emulators. The retained accepted
   replacement20 plan confirms the `image:target`→`emulators:target` edge.
3. `pkgbuilder.py.execute()` invokes `scripts/pkgbuild`; its package_worker calls
   `${SCRIPTS}/${task} ${pkgname}`. For emulators this is scripts/install, which
   calls scripts/build; makeinstall_target calls clean_doc_cache,
   start_system_doc and mk_system_doc.
4. `distributions/ROCKNIX/options` sets SYSDOCROOT inside tracked documentation.
   `start_system_doc` removes/truncates the old file; mk_system_doc appends rows.
5. After that dependency completes, `scripts/install image:target` must start.
   Its entry prefix calls watch-build; inherited run handling calls unchanged
   `build-admission.nested()`, which compares full `git diff --binary HEAD --`
   with admission's initial fingerprint. A generated tracked difference fails.

This is more than a possible parallel timing window. The original accepted joblog
records emulators task641 finishing epoch1791748070.4092 (19:47:50UTC), followed
by image task643 starting1791748078.4010 (19:47:58UTC). Those old tasks passed
under the pre-admission source. Its generated documentation still differs by
4669 diff bytes today. A synthetic control is required to demonstrate the new
guard conflict and candidate behavior; it has not been run in this source lane.
`causal-source.json` binds those original plan/log bytes and selected records.

## Minimal patch and compatibility

`generated-doc-output.patch` changes only
`distributions/ROCKNIX/config/functions`: six lines select
`${BUILD}/documentation/PER_DEVICE_DOCUMENTATION/${DEVICE}` when
RASTERATOPS_BUILD_RUN is set; `mkdir -p` creates that nested output directory.
BUILD is required in this branch, preventing accidental output under `/` when a
caller omitted build context. The existing configured SYSDOCROOT/SYSDOC path is
preserved when the marker is absent. Templates, sorting, row contents, temporary
doc cache and installed es_systems generation are unchanged.

The selection occurs inside start_system_doc, when config/path has established
BUILD. It does not use a toolchain path at early distribution-options load time.
All normal native/Docker build entrypoints already carry the validated marker.
The Docker recipe writes its private .env through scripts/get_env, which does
not filter RASTERATOPS_BUILD_RUN. It also passes explicit
`-e RASTERATOPS_BUILD_RUN` to docker run: this matters for a direct Docker target,
where the host watcher creates the marker after .env generation. watch-build
passes its modified environment to Docker; the relative `.build-runs/...` path
resolves through the admitted host→container checkout mount. Package/image
prefixes unset only RASTERATOPS_WATCH_EXEC, leaving the build-run marker inherited
through pkgbuild/install/build. No environment-reset command removes it in that
chain. These are source contract checks, not a newly launched Docker proof.

Every final documentation write in start_system_doc and mk_system_doc uses
SYSDOC; none hardcodes the old source-tree path. add_system_doc/add_emu_doc write
only DOCTMP staging, already ignored. mk_system_doc reads that staging and writes
`${SYSDOC}.tmp` and `${SYSDOC}.md`, so both temporary and final output follow the
redirect. The variable is named SYSDOC in this codebase, not SYSTEM_DOC.

BUILD is per device/architecture/suffix and already owned by the admission plan;
generated files therefore inherit its cleanup/retention ownership. The existing
root `.gitignore` ignores `/build.*/`; redirected external BUILD_DIR outputs are
outside tracked source and already have admission output requirements.

Manual generation with no watcher marker retains the previous tracked output.
No admission tool, package pin, target configuration, runtime filesystem or
player-facing flow changes. The new generated file must be included in the
build's compact artifact record if documentation is to be reviewed/published.
Do not later copy it into tracked source during an active build.

Exact baseline/candidate function-file hashes and patch hash are in bindings.json.
`candidate-functions` is the exact complete candidate file for independent diff
review and the future fixture; it is not installed into any checkout here.

## Coordinator control and next command

`fixture.py` creates only a new tiny Git fixture. It uses the exact real shell
documentation functions, real templates and unchanged real admission nested()
function. No build entrypoint, compiler, VM, Docker or network is invoked. Six
documentation cases cover baseline guard refusal after generation, candidate accepted output
with equal generated bytes, unchanged direct/manual behavior, H700 arm/aarch64
output locations and missing-BUILD refusal. Each watched candidate additionally
mutates a tracked product input and requires the same guard to refuse it.
An additional control runs actual scripts/get_env under a tiny non-secret
environment and verifies marker forwarding plus Makefile's explicit -e contract.
The fake nested receipt/marker exists only inside the isolated fixture; it is
not passed to the real watch-build entrypoint or used as compilation authority.

Before testing, root records the host-tool/synthetic-fixture VM-first rationale
in #493. Then from the coordinator checkout, whose original function file still
matches baseline bindings:

```bash
TASK_DOC_PACKET=/workspace/repos/rocknix.worktrees/m7-browser-memory-570/docs/qa-logs/2026-10-14-generated-doc-output-internal
TASK_DOC_OWNER=/workspace/tmp/pix493-generated-doc-control-20261014-01
mkdir -m 700 "$TASK_DOC_OWNER"
tools/watch-build-submit --owner "$TASK_DOC_OWNER" -- --record-only --activity-dir "$TASK_DOC_OWNER" -- python3 -I "$TASK_DOC_PACKET/fixture.py" --checkout /workspace/repos/rocknix.worktrees/m7-player-setup --scratch "$TASK_DOC_OWNER/fixture" --output "$TASK_DOC_OWNER/result.json"
```

The fixture fails if the exact original function bytes have changed. Do not reuse
an executed owner or silently change expected hashes. Consume original runner,
watcher and launcher results and actual process exit before accepting controls.
After passing, root can apply the patch to the assembled distribution, repeat
applicable shell/source checks and freeze the final engineering source. Full
image build remains the real integration proof. This packet provides only
source/hash/AST/bash-syntax checks and a proposed runtime fixture.
