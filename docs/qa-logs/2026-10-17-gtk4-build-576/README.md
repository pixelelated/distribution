# GTK4 dependency compilation — #576

Work in progress. The isolated GENERIC build branch is `build/m7-gtk4-20261017-01`,
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

WebKit6 compilation is now active in a separate owner,
/workspace/tmp/pix-webkit6-build-20261017-01. Its fresh CMake cache selects GTK4,
Wayland, Skia, GBM and sandboxing; memory samplerON and sampling profilerOFF are
different features. No old GTK3 CMake tree is reused. A present WEBKIT_SAMPLE_MEMORY
environment variable enables sampling even with value0; it is not selected here.
Native input, runtime sandbox properties, browser memory and H700 performance
remain unrun. Source review confirms all31 fixture calls have public declarations,
but that is not compile/runtime proof. API6 process/injected-bundle closure and
actual UID/capability/namespace/seccomp observations remain required; root-run
success alone does not prove sandbox isolation. No production source or pin was promoted. No device/cloud operation.
