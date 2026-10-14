# #574 owner04 shared-runtime correction — source only, UNRUN

Owner03 reached the final link with the intended SDL dependency graph. The
private shared-C++ patch retained `-static-libgcc`, and the original linker
reported that shared libstdc++ needed **libgcc_s.so.1, not found**, followed by
17 unresolved GCC-versioned symbols. This packet proposes **explicit
`-shared-libgcc` with shared libstdc++**, preserving every other selected flag,
codec archive, feature, source pin and resource limit.

Only this new QA packet changes. Sealed1c0e93/7d4366/26a527/2608923 and all
failed receipts remain immutable. No export, patch program, generator, compiler,
linker, readelf/nm/ldd, binary load, container, VM or device operation ran here.

## Exact failure and SDK contract

`evidence/original-link-argv.txt` preserves the actual final G++ command. It
selects `-m64 -static-libgcc`, then the unchanged start/end group containing
utils, expat,7z,ocore_sdl,zlib,zstd,flac and utf8proc archives, followed by the
existing system libraries. No static libstdc++ flag is present. The original
stdout/stderr and child/container/attach/launcher/watchdog/cleanup receipts are
retained as exact gzip bytes with compressed and uncompressed hashes.

The first linker diagnostic names the SDK's shared libstdc++.so and its missing
libgcc_s.so.1 dependency. Subsequent errors include `_Unwind_Resume`,
`_Unwind_GetIPInfo@GCC_4.2.0`, other unwind accessors and GCC arithmetic helpers.
The actual versions are retained; these are not all GCC_3.0 symbols. Earlier
compiler warnings remain in stderr and were not the terminal failure.

`evidence/sdk-contract.json` records read-only file identities:

- The actual G++ wrapper invokes retained `g++-15.2.0` through ccache at the
  unchanged original container prefix. Its exact script is retained.
- SDK target `libstdc++.so` resolves to libstdc++.so.6.0.34, SHA256
  `7f12166a8c5e62340b67ff213b4859d002b45e49ed114550049bb895f26455cc`.
- Target libgcc_s.so and libgcc_s.so.1 are both regular178640-byte files, SHA256
  `421566e56262d76771c56578d1e87c80a2b33e702e4c21c29a4cf1e456fbe174`.
  Both exist beside the target C++ library; neither corresponding sysroot
  usr/lib pathname exists. Shared libgcc is present in the SDK. No library
  copy or modification of custody is needed by this proposal.
- Static libgcc/libgcc_eh remain present and unchanged. They do not eliminate
  shared libstdc++'s separately reported dependency.

The [official GCC15.2 link-options contract](https://gcc.gnu.org/onlinedocs/gcc-15.2.0/gcc/Link-Options.html)
documents explicit shared/static libgcc selection and G++'s shared-libgcc
default for C++ exception propagation. Exact cached GCC15.2 source snapshots
corroborate the mechanism: `gcc/cp/g++spec.cc:231–233` disables the driver's
shared-libgcc insertion when `-static-libgcc` is supplied; lines444–446 insert
the shared choice otherwise. `gcc/gcc.cc:1830–1856` distinguishes static
GCC/exception archives from shared-libgcc selection. No compiler was invoked
to print specs. The archive does not establish SDK build provenance.

The retained distribution recipe expresses shared runtime installation but
currently names GCC16.2 while the actual wrapper names15.2. It is recorded
only as source intent, **not** as the recipe proven to have built these ELFs.
`source_pins_verified` remains false. This is a local QA linkage mismatch;
no upstream compiler defect, release fix or pin change is asserted.

## Minimal prospective delta

The replacement private patch still touches only scripts/genie.lua: original
`"-static-libgcc -static-libstdc++"` becomes `"-shared-libgcc"`. The original
file SHA256 remains `b3dd93f153fa40fa69983f1cc24ee2119510a3459c22a378c6a4d80c4cef97d3`;
the proposed result is
`dfc5f38e72c2b459de6f00478abee1913452252bd799c5bea304b5b919ede288`.
The separate owner03 toolchain.lua OSD patch is byte-identical.

`changes.json` records exact small diffs against2608923:

- Replacement C++ runtime patch/name and expected patched-genie hash.
- The generated chdman release64 oracle requires exactly one shared-libgcc
  token and rejects both static runtime flags. No other oracle is removed.
- Two shared GCC library hashes join existing SDK input verification.
- Bindings select this prospective plan, retaining the old manifest in evidence.

Every make/configure argument and native/bootstrap/converter path is unchanged.
Export, source inventory checks, OSD patch,1-job lifecycle, Docker/watchdog,
admission consumption and original-exit handling are unchanged executable
copies. Codec archives remain static. O1/no LTO/no OpenMP, compiler selection,
release64, final output location and complete dependency graph remain required.
No exception removal, RPATH, ignore-unresolved option or sysroot modification
is proposed. The final VM must explicitly qualify shared libgcc together
with shared libstdc++ and the rest of the actual loader closure.

## Owner03 evidence and owner04 entry

Owner03 export/bootstrap/configure retain PASS0; original admissions were
consumed. Build retains selected make2, container/attach/launcher1, watchdog0,
normal cleanup and empty recorded descendants/cgroup. Its source-after check
still protected31411 original files. `evidence/owner03-summary.json` is derived
from the separately retained originals. The summary is not a new runtime result.

Required generated files and compact receipts are retained; this worker no
longer requires owner03's work directory. Coordinator owns retirement. Start a
fresh owner04 after byte-exact packet import, manifest verification and capacity
review. Do not transplant successful receipts, rewrite an old family or retry
its failed build. This first command only prepares the export-stage plan:

```sh
cd /workspace/repos/rocknix.worktrees/m7-player-setup
PIX574_REPO=$PWD
PIX574_PACKET=$PIX574_REPO/docs/qa-logs/2026-10-14-chdman-runtime-link-source
PIX574_OWNER=/workspace/tmp/pix574-chdman-build-20261014-04
PIX574_STAGE=chdman-export
python3 -I -S -B "$PIX574_PACKET/plan.py" \
  --checkout "$PIX574_REPO" --owner "$PIX574_OWNER" --stage "$PIX574_STAGE"
```

Use the unchanged serialized admission/submit sequence for each stage:

```sh
PIX574_STAGE_ROOT=$PIX574_OWNER/stages/$PIX574_STAGE
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$PIX574_STAGE_ROOT/retention-plan.json" \
  --output "$PIX574_STAGE_ROOT/retention-report.json"
# Consume original report/watcher channels and review fresh capacity first.
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$PIX574_STAGE_ROOT/admission-plan.json" \
  --output "$PIX574_STAGE_ROOT/admission.json"
tools/watch-build-submit --owner "$PIX574_STAGE_ROOT/submit" -- \
  --admission "$PIX574_STAGE_ROOT/admission.json" \
  --activity-dir "$PIX574_STAGE_ROOT/logs" -- \
  python3 -I -S -B "$PIX574_PACKET/run-stage.py" \
  --checkout "$PIX574_REPO" --owner "$PIX574_OWNER" --stage "$PIX574_STAGE"
```

Consume every original stage/watcher/launcher/cleanup channel through existing
build-admission before explicitly selecting the next stage. Export → bootstrap
→ configure → build; no loop or implicit retry. Fresh private inputs must
be recreated; owner03's completed acceptance is not erased or reclassified.

**Unchanged bounds:** one job,4GiB RAM/no swap,2 CPUs,6GiB sampled scratch stop
ceiling and one1800-second family clock, including every inter-stage review and
admission gap. The512MiB free-space floor, offline pinned builder, read-only SDK
mount,256-PID limit and bounded cleanup remain unchanged. The disk ceiling is
sampled, not a kernel quota; expiration refuses without extension.

## Static checks and remaining qualification

`static-check.py` parses AST, compares original/revised source and patch bytes,
verifies retained receipts and generated-file identities, checks the exact
oracle change and invokes only `bash -n`. It imports no runner and executes no
build code. `static-result.json` records the actual source-only result.

Patch application, new configure/link, resulting ELF dependencies/versioned
symbols and loader compatibility remain **UNRUN**. The proposed driver choice
is source-grounded, not a promise that every later link dependency is resolved.
Keep any next original failure. After a successful build, separately admitted
VM inspection must verify the actual ELF/loader closure (including both shared
runtimes), followed by existing synthetic CHD conversion/independent parity
controls. Compilation alone does not prove codec behavior, final-image
installation, native provenance or current-source qualification of old ELFs.
