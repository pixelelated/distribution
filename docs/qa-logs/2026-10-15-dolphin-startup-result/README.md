# Dolphin NoGUI RetroAchievements startup — #584

The one-object compile/relink and four-case no-network VM proof passed on
October15. Source patch018 is committed at d3e684dd4b; the frozen fac608ff image
is unchanged. This fixes the missing launcher lifecycle in the tested private
candidate; installation in the next firmware and native gameplay remain separate.

Build run20261015T004107Z-f7c5c978: all compile/link/strip/readelf, container,
watchdog, command and watcher original exits0. Peak cgroup memory1,290,883,072
bytes; about20.7MB scratch.103 named frozen inputs and actual compiler/linker
dependencies are recorded. Read-only frozen input hashes stayed unchanged.
The exact container exited normally and was removed; observed owners were absent.
Admission aea323d1f79149c4a16e34e4ef5a5c66 is consumed qualified.

Startup run20261015T004309Z-7bfdcf48 used actual installed baseline e6c6207d and
private candidate5cb5dacafbcd2227627ef687a65318e61890ef343e5c6553f07c0fb11231fea5.
The normal8GiB/4CPU/no-NIC guest and all original outer channels exited0.
Admission5a3e47bfcb9948598dd27ebaadf47780 is consumed qualified.

| Case | Actual observation | Original process exit |
| --- | --- | --- |
| Installed baseline, enabled | Live CPU thread/ticks; no manager lifecycle or HTTP request. Known defect reproduced. | 0 after normal SIGTERM |
| Candidate, enabled | Live CPU thread/ticks; one initialization, one synthetic login POST to127.0.0.1:8080/dorequest.php, one shutdown. | 0 after normal SIGTERM |
| Candidate, disabled | Live CPU thread/ticks; no lifecycle or request. | 0 after normal SIGTERM |
| Candidate, absent boot file | Actual BootCore failure; one initialization/request/shutdown; scope guard executes on early return. | 1, expected refusal |

There were no forced stops, surviving Dolphin children, endpoint errors or
cleanup failures. The endpoint rejected synthetic credentials; no real login,
award, proxy service, rendering or gameplay is claimed. The DOL is a self-authored
four-byte CPU loop. Every raw guest file except the immediate-use executable is
archived; its exact bytes/identity remain in the full original manifest.

The original engineering NoGUI link and this candidate emit exactly the same20
warning messages/counts. Retained compilation mixes Dolphin C++23 with fmt's
compiler-default mode; fmt's C++20-dependent no_unique_address layout supports
that existing cause. Matching warnings and successful tests do not establish ABI
safety or prove harmlessness. The baseline excerpt and original candidate stderr
are retained without suppression. No unrelated flag or library change was added.

The upstream opportunity remains Dolphin's NoGUI lifecycle plus a ROCKNIX
packaging backport, queued under#585 after the initial qualified build. No upstream
submission occurred. See the earlier sealed relink plan for source/toolchain bounds.
