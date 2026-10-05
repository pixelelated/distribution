# Matched software renderer control

Issue #447. VM-first: yes. The same frozen cf511ce/79d560 candidate and
software virtio GPU were used throughout. The temporary systemd drop-in
selects a renderer; the temporary wrapper changes only Sway's debug flag.
Installed binaries, pages and product source remain unchanged.

| Experiment | Actual compositor and allocator | Host versus native frames |
| --- | --- | --- |
| Diagnostic14 | Pixman, DRM dumb allocator, atomic DRM | All nine correct and exactly equal to the unchanged canonical reference |
| Diagnostic15 | GLES2/llvmpipe, GBM allocator, atomic DRM | Host old/torn0, old/partial5, correct15; native correct throughout |

All eighteen actual comparison frames were directly viewed. The two actual
QEMU command lines match after replacing only the owner path, and their
page/capture Python files are byte-identical. Both restart the compositor and
enable the same debug logging. This isolates the renderer/allocation path
from those setup effects; it does not identify a particular erroneous
Mesa, wlroots, kernel or QEMU instruction. Earlier legacy DRM diagnostic07
did not resolve the fault and is not a proposed workaround.

Diagnostic14: durable18:30:37/all four rc0; actual640329 cleanup18:31:45.
Diagnostic15: durable18:33:00/all four rc0; actual13c712 cleanup18:33:38.
These are completed experiments, not candidate-wide acceptance.

## Full sign-in proof with Pixman

Original full signin-ui12 reached27 checks and six intended frames, then
failed on persistent observer TimeoutError. Its original four rc1 results,
330 received frames and actual ab6ec0 cleanup remain preserved. The failing
read phase was not recorded. #449's corrected observer distinguishes idle
between messages from bounded initial/partial reads, and verifies unique
pixel coverage. Its nine real loopback controls pass; see
[observer evidence](../../2026-10-05-vnc-observer/README.md).

Fresh signin-ui13 completed18:41:40/all four rc0. All27 assertions pass and
all six actual intended frames were directly reviewed. The finishing capture
matches the unchanged canonical reference exactly; real old/partial frames
reject. Redirect, HTTP/navigator Mobile UA, public Dropbox/OAuth and actual
390px Checking/Connected margins remain intact. The observer stopped cleanly
after354 frames with no recorded error. Public-provider peak RSS696352KiB
on8GiB is a measurement, not a newly invented memory ceiling. Actualbc4afc
cleanup18:42:00 proves owner/guest processes absent and no QEMU. Current
source and bundle verify before/after. No authenticated trust-page claim.

## Next implementation boundary

Pixman is a validated runtime workaround for this software VM sign-in path.
It is not yet a persistent or automatically selected configuration. #447
remains open. Next: choose a narrowly scoped GENERIC_X64 software fallback,
preserve accelerated guests and handheld renderer settings, and verify clean
boot/upgrade selection plus relevant ES, emulator, visual and performance
regressions. If product bytes change, freeze/build and requalify those bytes
before the P4 review. Do not apply a global handheld renderer override or
declare the unmodified software profile repaired.

An older upstream [Sway report](https://github.com/swaywm/sway/issues/7644)
also describes slow non-virgl/llvmpipe rendering. It is context for further
source investigation, not proof that its cause equals ours. Our local
matched images, renderer logs, captures and controls are the evidence here.
