# SM8550 warm resume02 — #503 / #492

The original failed attempt is retained. Guarded host preflight passed at
15:49:27 UTC after the copy-proof guest and its watchers exited: swap restored
8GiB free with35.6GB available RAM. Watched recovery preserved all eight
interrupted scopes and the partial image by same-filesystem rename, archived
thread/stamp records, and fast-forwarded only the stopped build checkout at its
original absolute path. Recovery returned fourzero channels, seven intact seals
and independently verified exits at15:49:57. No payload was deleted.

Fresh source inventory includes the new FEX patch; the only product delta from
failed40f80 is that patch. Freeze6b627a38ae3182bf73310ff8819ae4f17da79e36 keeps
ES72494 and does not absorb the parallel prompt change. Original ARM7946files,
807symlinks and245stamps remain byte-identical; its manifest is copied into the
new mounted owner and sealed. Root review caught that the draft verifier named
an old owner absent from the container; the dependency was corrected before
launch. A private independently hashed Nix copy and read-only exact nixpkgs
snapshot preserve the compiler control inputs. The existing upstream installer
is still mutable; package verification rejects version/toolchain/rootfs drift.

At15:50:04 the actual pinned container and required mounts were verified.
Build owner `/workspace/tmp/pixelelated-m7-sm8550-build-02` runs FEX first,
verifies the complete installed package and both guest architectures, then
continues warm aarch64 build_distro. It never reruns the accepted ARM stage.
Acceptance02 follows actual builder/process/container exit, then verifies
independent firmware custody, raw/update payload equality, ABL, installed
identity, ARM handoff and FEX byte equality. Sequence02 supervises the pair and
writes local tracker handoffs. The primary updates #492/#503/M7 and actively
consumes results. Local watches do not provide disconnected chat alerts (#395).

This packet records accepted recovery and launch, not completed firmware.
Current terminal outcomes remain at the owners and must be consumed separately.
Interrupted intermediates/private Nix are retained only for this immediate
build, and retire after its acceptance/source-custody dependencies end.

## Terminal outcome — #506

Build02 compiled/installed the complete FEX package at15:50:49UTC, then its
verifier used the wrong CMake external-project directory: guest-libs/build.ninja
rather than Guest/build.ninja (and Guest_32 for32-bit). It failed before
build_distro or firmware assembly. Build returned four2 channels/eightseals and
verified exits15:51:05; acceptance returned four1 and sequence stopped15:51:35.
These remain FAILED. #506 owns the corrected checker/fresh03 continuation;
the successful target package is retained, with no reason to reclean it.
