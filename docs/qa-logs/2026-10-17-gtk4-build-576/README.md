# GTK4 dependency compilation — #576

Dependency compilation complete. The isolated GENERIC build branch is `build/m7-gtk4-20261017-01`,
commit969354955741d6c0ca8ce816e1c59ad338b1605b, based on published4c3eda48c7.
Only the previously reviewed six-recipe overlay is staged there. This packet
records actual package compilation, distinct from the original source-only packet.

Graphene1.10.8 builds and installs successfully. The source archive matches its
pinned SHA256. Sysroot and package ELF both hash to
`0cd11e3355f90bb9150772cf2d186b575bb98084ece4ef83ea5e7e8588fba00d`.
All original successful run channels are0; admission234eb2e is consumed.

The first attempt failed before compilation because the pinned container Python
lacks `hashlib.file_digest`. The original failure remains in failed01; its admission
365fb883 is consumed as failed-investigated. A fresh helper uses streaming SHA256
and verifies the already copied toolchain rather than duplicating it. All121,054
regular toolchain files,1,647 symlinks,651 stamps and config pass contents/modes
and independent-inode checks. All three accepted-cache mounts are read-only in
the actual Docker observation. Native generator Python is a different interpreter
from the container helper Python; host AST checks do not establish that runtime API.

The successful owner took31.55s, including25.17s of copy verification. Its2GiB
cgroup peak includes file-cache-heavy verification and is not compiler RSS or a
target browser memory measurement. No OOM or host swap-out occurred. The copied
seed is6.5GB; the entire historical build tree was not duplicated. Sparse seeding
is enough for these package builds, but does not establish full-image installation
payload availability. Original compact logs and executable helpers are retained.

GTK4 4.24.1 and all three sandbox packages compile/install successfully; actual
ELF/stamps and original result channels pass. GTK4 took147.18s with717,467,648B
cgroup peak; whole dependency owner163.83s, no OOM or host swap-out. The independent
build root is6,897,287,168B after these packages. Admission9c736bd7 consumed.

WebKit6 subsequently compiled successfully under
/workspace/tmp/pix-webkit6-build-20261017-01; original channels0 and admission
consumed. Its fresh CMake cache selects GTK4, Wayland, Skia, GBM and sandboxing.
See [engine results](../2026-10-17-gtk4-engine-576/README.md) and the
[compiled input fixture](../2026-10-17-gtk4-input-compile-576/README.md).
The [strict closure readback](../2026-10-17-gtk4-closure-576/README.md) retains six
inherited search-path findings; compilation is not runtime/sandbox/performance
proof. Leave WEBKIT_SAMPLE_MEMORY unset, even value0 enables sampling. No product
source/pin promotion, device/cloud operation or active runtime remains.
