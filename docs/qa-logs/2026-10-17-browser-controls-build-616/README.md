# Runtime-control helper compilation — #616, October17

Both tiny diagnostic binaries compile and link against the retained GENERIC_X64
and H700 aarch64 toolchains in the pinned build container. The engine and OS
image were not rebuilt. Source is the immutable companion
[control packet](../2026-10-17-browser-controls-616/README.md), generated C
`c892ba759c81c9083512017c56aca240929e8afaa2db40f97be26fb87eb60202`.

The actual x86 binary passes all12 configuration-parser cases under its target
loader/libraries, with DISPLAY and WAYLAND_DISPLAY absent. Four valid cases0,
eight refusals78. No GTK initialization, WebView, provider, VM or device runs
occurred in this compile allocation. H700 is compiled/ELF checked, not executed.
The output sizes are52,544 and83,080bytes. ELF machine and gtk3/WebKit4.1 dynamic
links were checked; source/ELF metadata do not prove later browser functionality.

Original container command0,1.767s; watcher/runner/launcher0, all recorded owners
exited and exact container absent. Admission261514b9d3fa44cdaef8b34cbe9f07fd consumed.
Read-only caches, no network,1CPU/1GiB/128PIDs/180s and192MiB disk forecast; no
source-tree copy. Tiny helpers remain held only for the queued runtime proof.

The first consumption preparation mistakenly read the prelaunch receipt instead
of the run admission, raising KeyError before acceptance existed; consumer2
refused the missing file. The corrected acceptance reads original run outputs.
That bookkeeping failure is preserved separately and did not rerun compilation
or change its original successful results.

Host owner: /workspace/tmp/pix-browser-controls-compile-20261017-01.
Run: frozen checkout .build-runs/20261017T035952Z-4429942f.
Original helpers stay outside Git. The next separately admitted VM owns actual
HTTP/DOM UA, observer, field-visibility and frame checks; performance/GPU and real
provider measurements remain separate.

Original readelf text is stored as deterministic .txt.gz to preserve its trailing
spaces without treating tool-output formatting as source whitespace. Decompressed
bytes match the original acceptance hashes; no output was normalized.
