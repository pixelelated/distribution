# Prospective owner03 plan — source only, UNRUN

This additive copy preserves the sealed 1c0e93 plan's archive/pin, selected
chdman target, arguments, bootstrap, target paths, toolchain and resource bounds.
The complete historical README and static receipt are retained in
`../evidence/original-plan-README.md` and `original-plan-static-checks.json`.
Those historical receipts do not qualify this revised plan.

The existing `chdman-shared-libstdcxx.patch` is byte-identical. The additional
`chdman-preserve-selected-osd.patch` guards three libretro-only Lua assignments
by the explicitly selected retro OSD. It preserves the requested SDL OSD for
this standalone chdman build. All configure options remain unchanged, including
NO_X11 and both XInput disables. `build-stage.sh` adds only an exact post-patch
toolchain.lua hash precondition. There is no generator/bootstrap or converter
path change. The two exact before/after source hashes are in input-bindings.json.

Use only the parent packet's runner, manifests and fresh owner03 instructions.
No source archive export, native generator, compiler, container or target was
executed to prepare this revision. The first actual patch/configure result is
still owed; generated graph/flags/version acceptance remains unchanged.
