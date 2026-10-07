# SM8550 FEX guest-header controls — #503

The failed device build exported the aarch64 pkg-config sysroot into FEX's
x86 guest compilation. The upstream helper removed plain `/usr/include`, but
not its sysroot-prefixed equivalent. ARM64 libc headers consequently shadowed
the x86 headers and made the i686 C++ limits header attempt a 12-to-16-byte
long-double/float128 bit cast.

The paired syntax controls reproduced both failing Wayland and GL sources
with the original Nix snapshot, compiler paths and custom rootfs identity.
Removing only the ARM64 standard include path made both succeed. A fresh
CMake/Ninja control, outside nix-shell and with its injected flags cleared,
then reproduced the original 32-bit failure and built all six configured
32-bit and nine configured 64-bit guest libraries with the proposed patch.
Their ELF class/machine, hashes and sizes are in libraries/control-result.json.
No source pin, compiler version or supported guest architecture was changed.
This proves the isolated compilation fix, not full device firmware or runtime.

Both controls mounted the failed SM8550 tree read-only. Their owners are
`/workspace/tmp/pixelelated-m7-fex-header-control-01` and
`/workspace/tmp/pixelelated-m7-fex-guest-controls-02`. Each has four zero result
channels, five intact input seals and independently verified process exits;
no control container remained at the 15:31 UTC readback. The original build's
730 thread logs (300001391 bytes before compression) and per-file hashes were
preserved in the first owner's artifacts before any warm build retry.

Can this be done on the VM? This is a host cross-compilation fault; the pinned
build container runs the exact original target/compiler inputs without a
physical handheld. No device or cloud access is involved.

The first control restores Nix 2.35.2 and the exact cached nixpkgs release
26.11pre1086972.7dd199b0e299, rather than silently selecting a newer moving
channel. Restored Nix data is held only for the immediately queued full-build
repair. The retained scripts describe their owner-local input paths; all logs
and scripts here are compact proof, not retained guest/build disks.

The warm-resume scan must check target-specific stamps: FEX had a valid host
stamp while its target failed. Seven concurrent packages were interrupted too.
Recreate all eight scopes, preserve completed packages and carry the independently
rehashed ARM stage forward. The full SM8550 image remains unaccepted until its
new watched build and artifact verification actually finish.
