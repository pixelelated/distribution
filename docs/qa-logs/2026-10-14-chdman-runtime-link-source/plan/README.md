# Prospective owner04 shared-runtime plan — UNRUN

This additive plan keeps owner03's source pin, SDL correction, selected tool,
all configure arguments, bundled codec archives, target/bootstrap paths,
toolchain, containment and resource bounds. The only proposed runtime-linkage
change is explicit shared libgcc alongside the existing shared libstdc++.

`chdman-shared-cxx-runtime.patch` replaces the original static C++/GCC pair with
`-shared-libgcc` in the same scripts/genie.lua line. It replaces the prior private
shared-libstdcxx patch, which retained `-static-libgcc`. The two patches must not
be stacked. Before/after source identities are in input-bindings.json; the old
patch is preserved in the parent evidence. The owner03 OSD patch is unchanged.

The generated-linkage check now requires exactly one `-shared-libgcc` token for
chdman and rejects both static runtime flags. Every other graph, archive,
compiler, optimization, source-inventory and output check stays unchanged.
The SDK's libgcc_s.so and libgcc_s.so.1 bytes are added to the existing immutable
toolchain input checks. No library is copied into the SDK/sysroot and no RPATH
or unresolved-symbol waiver is added.

Use the parent packet's fresh owner04 instructions. The owner03
link failure remains FAIL; revised configure/link/target-loader proof is UNRUN.
