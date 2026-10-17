# GTK4/WebKit6 post-build preparation

Prepared for source commit `969354955741d6c0ca8ce816e1c59ad338b1605b` in the
isolated `m7-gtk4-build-20261017-01` checkout. The engine build remains owned by
the coordinator. No compiler, target program, VM, or browser is launched by
preparation. Do not run the verifier until all six package builds have finished.

`verify-closure.py` writes only JSON to stdout. It uses host `readelf` on target
ELF files, never `ldd` or target code. It requires completed package stamps,
the intended WebKit configuration and package versions, and critical artifacts
in both `install_pkg/<name>-<version>` and the isolated sysroot. This build
system calls the directory `install_pkg`, not `.install_pkg`.

The build strips `install_pkg` after copying unstripped binaries to the sysroot.
The verifier records both SHA256 values and requires matching ELF metadata and
GNU build IDs (or identical bytes), rather than incorrectly requiring identical
stripped and unstripped hashes. Absolute symlinks are resolved within virtual
target roots; they never accidentally select the old canonical host checkout.

The dependency report follows ELF interpreters and NEEDED entries through the
six new package payloads, isolated sysroot, then accepted baseline sysroot.
Each result identifies its layer and whether its bytes match the accepted
baseline. Missing dependencies fail. Baseline-only fallback is explicitly
`PASS_WITH_BASELINE_FALLBACK`: those files still need an identified guest source.
The checker does not prove symbol-version ABI, `dlopen` modules, schemas, fonts, certificates,
loader cache/hwcaps, functional input, performance, or sandbox isolation.

After package success, on the host under the coordinator's read-only allocation:

```sh
python3 -I /tmp/pix-gtk4-postbuild-20261017/verify-closure.py
```

Capture stdout in a **new** result file outside the build checkout. Default
ceilings are 180 seconds and 512 resolved ELF nodes; readelf has a per-call
timeout. There are no source/cache writes. The accepted baseline is read-only
fallback at `m7-p5-build-20261015-03/build.pixelelated-GENERIC_X64.x86_64`.

`input-source/` was produced by the existing reviewed preparation tool without
changing any fixture source. `compile-input.py` only prints the plan unless
`--execute` is supplied. The command below remains **UNRUN** and needs a new
allocation, after closure review:

```sh
python3 -I /tmp/pix-gtk4-postbuild-20261017/compile-input.py \
  --output-dir /tmp/pix-gtk4-input-compile-20261017
```

Actual compilation: run the same command with `--execute` **inside** the pinned
non-root builder with the isolated checkout mounted at
`/workspace/repos/rocknix.worktrees/m7-pixelelated`, this packet mounted read-only
at its existing absolute path, and a separately writable output parent. Reserve
1 CPU, 2GiB/no swap, 512MiB scratch and 120 seconds for the entire owner; the
compiler itself is bounded at 60 seconds. The outer owner still provides
resource observation and signal/descendant cleanup. GCC and pkg-config come
from the new canonical sysroot/toolchain. No config/options is sourced and no
package build or shared ccache writes occur. Original compiler exit, output,
resolved arguments, versions and binary SHA256 are retained in the new output.

After successful compilation, add `--extra-elf <host-path-to-input-spike>` to a
new verifier run to include its ELF closure. This is still read-only. It does
not authorize launching the reviewed runtime fixture.

For a later disposable-guest allocation, keep the WebKit sandbox enabled.
Root-run success alone is not sandbox evidence. The privileged uinput broker
and the browser's UID/capabilities/namespace contract need deliberate review;
observe actual isolation, renderer, trusted DOM events and cleanup separately.

Validation performed on this preparation: Python AST parsing, JSON parsing,
manifest hashes, exact fixture-source preservation, and text inspection only.
The post-build verifier and compiler wrapper have not been executed.
