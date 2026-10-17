GTK4/WebKit6 post-build readback

Strict status remains FAIL (original rc 1), with all 378 NEEDED/interpreter edges resolved across 94 ELF nodes: 11 new package artifacts and 83 accepted-image dependencies. All six package stamps, exact versions, configuration and all 11 package/sysroot loaded-byte comparisons pass.

Six search-path findings are inherited from the accepted image: FreeType, libgcrypt, libthai and libX11 contain an absolute build sysroot path; libwoff2dec and libwoff2common contain relative lib. They are not established runtime failures. No new overlay artifact has one.

Earlier failures remain in closure-01 (CMake parser), closure-02 (absent build-ID assumption), closure-03 (sparse sysroot is not a runtime root). Versioned tools and diffs remain in /tmp/pix-gtk4-postbuild-v2/v3/v4-20261017.

Next compilation remains UNRUN and needs coordinator admission. It may be scoped to compiler/API evidence after the coordinator accepts the complete dependency inventory plus inherited search-path findings; do not relabel the checker PASS.

Inside the admitted non-root pinned container, mount isolated m7-gtk4-build-20261017-01 at canonical /workspace/repos/rocknix.worktrees/m7-pixelelated, original postbuild packet read-only, and a separate output parent writable. Preserve required main git metadata mount. Reserve 1 CPU, 2GiB/no swap, 512MiB growth, 120 seconds total.

Command (UNRUN):
python3 -I /tmp/pix-gtk4-postbuild-20261017/compile-input.py --output-dir /tmp/pix-gtk4-input-compile-20261017 --execute

Compiler wrapper SHA256 23638b6efe12ec62fc61f0ad2c2dcc1bf5c01dcc6a0207e26e0c36570ace703b; source input-spike.c SHA256 015652f22b14b258352ca510e93c7a6179721690f3faa2b00a6ccac237f8ea6e. No source change requested. Compiler timeout 60 seconds, explicit GTK4/WebKit6 pkg-config versions and sysroot, ccache disabled. After compile, rerun v4 readback with --runtime-root pointing to accepted image/system and --extra-elf the host fixture path, retain strict inherited findings. Compilation never authorizes browser/VM launch. Root-run alone is not sandbox proof.
