# FEX dependency/source disposition (#528)

Exact retained source separates the ArchLinux guest runtime from the Nix development sysroot. The shipped GL thunk is a matching provider candidate, but overlay selection is conditional; native ARM libraries do not establish x86 guest providers. An unspecified separately selected guest rootfs does not create an automatic bundled-source requirement.

This packet preserves13 exact header notices, eight proposed flat source archive identities, three exact historical reuses and separately scoped Nixpkgs/libglvnd/patch custody. No download, runtime execution or whole compiler-closure gate is claimed. Read the archived README and machine-readable dispositions for exact scope and limits.
