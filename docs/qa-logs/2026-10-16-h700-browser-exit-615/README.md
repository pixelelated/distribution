# #615 — bounded RG35XX SP browser-exit reproduction

**Loaded-page Escape remains inconclusive.** Source077197 / ES16dbac, same
physical H700 boot067a27f1 and frontend PID2696/start5810. No firmware, installed
source, configuration, service environment or browser debug flag was changed.
This is not a new full browser qualification or a demonstrated product fix.

The owner requested: “The RG35XX SP is still online. I'd recommend we try to
replicate the issue and see if we can isolate it as a one-time occurrence, a
misdiagnosed issue, or something that's able to be replicated.”

Can this be done on the VM? Portable input/exit paths already pass #614. This
run addresses the remaining physical H700 compositor/input timing and memory
conditions. A provider page alone is not the reason to use a device. Three
bounded attempts entered normal ES → Add connection → Dropbox → on-screen
keyboard, without credentials or cloud data operations. Original connection
configuration and automatic-sync-off state were preserved. All actions used
`tools/device-act` with strict host binding and exact boot/build assertions.

| Attempt | Actual result | Limit |
| --- | --- | --- |
| Early Escape, about18s | Kernel Escape down/up on event7, natural browser focus, browser gone by the2s observation, same frontend. Guard0. | Frame still shows opening spinner. Controller subsequently fails1 on duplicate `at` logging argument; preserve partial evidence, not a whole-trial PASS. |
| Longer page, Escape planned42s | Low-memory guard sends pidfd TERM at35.66s, before any test Escape. Available190476KiB (186.0MiB), PSI some8.67/full8.21 avg10 at intervention. | Observer1 and trial1 are preserved. Minimum184340KiB (180.0MiB); later some26.09/full20.81 avg10 and temporary D-state processes show pressure/recovery, not an OOM. No loaded-page screenshot was reached. |
| Normal close at25s | Installed `cloud_oauth close` returns0 in2.211632s; browser disappears, same frontend regains focus. Controller0 and observer0; no guard. | Pre-close frame has blank content and browser controls. Frame sampled at least3s after close is black; later cancellation and carousel frames prove recovery. No loaded-page or time-to-play claim. |

The first observer was healthy and continued independently after the controller
logging error. Its result is0; the failed controller stays1. Round02 fixes
the diagnostic dictionary merge in a new file/directory after the first run
stops. It also changes overall observer lifetime240→600s, input wait18→42s
and fallback timing assertion55→65s. Round03 returns observer lifetime to240s
and waits25s before normal close after memory recovers. Exceptions and original
systemd statuses remain recorded. The90s
emergency and low-memory thresholds were never relaxed. No fourth attempt ran.
`originals.tar.gz` retains all34 exported files, including all three executed
source sets, failures, input/focus/memory samples and six original unit outcomes.
No GTK key-handler debug was enabled; app consumption in the early case is
inferred from immediate exit after the kernel Escape, rather than a GTK log.

The observations do **not** establish a one-time glitch, incorrect focus, a
keyboard lifetime defect, or a browser bug. Neither the earlier90s deadline nor
this36s pressure guard is a spontaneous crash. The original loaded-page Escape
failure remains unexplained. Early exit and normal close now have native
observations; pressure under the actual page is the concrete remaining lead.
The monitor/controller's own overhead was not separately attributed, so the
entire pressure rise cannot be assigned to WebKit or a specific page script.

## Preservation and cleanup

All163 protected files/25,549,175bytes, selected settings/credential hashes,
paths/modes, recovery entries and markers compare equal. Autosync stays off.
Same boot/frontend, no game, cloud transfer, authentication, reboot or update.
An initial navigation selected the read-only achievements page before correction;
its personal screenshot is retained privately and excluded from this packet.
No credential value or private file inventory is published.

After export and exact per-file hash checks, all33 device diagnostic files in
three owned `/tmp` directories were removed. All six original services had
MainPID0 before retirement. Resetting the named transient units returned1
because some were already collected; independent readback shows no failed
units, browser, WebKit, OAuth, rclone or test keyboard, and all three directories
absent. Memory recovered to570156KiB (556.8MiB) available. No OOM/kernel errors
were observed. There is no remaining device/VM/build/diagnostic job.

## Next scoped experiment

#615 stays open for loaded-page attribution. Preserve #614's portable PASS and
#570's previously qualified repairs; neither promised a universal memory cure.
Before another long page attempt, compare a lean observer with the current
instrumentation and collect per-process PSS plus page-readiness evidence; keep
normal close early and retain the same emergency limits. Reuse existing VM
controls where possible; hardware claims remain limited to H700. A hypothetical
focus, proxy or WebKit fix is not selected without evidence. The upstream
inspection in `upstream.md` found no verified matching fix.

#613 remains the next independent package correction; #607–610 still precede
affected Nova deployment. Website and #528 public-source work remain separate.
The exact-source [frame index](frame-index.json) records this unchanged flow.
Run `python3 -I verify.py` from this directory for offline evidence verification.
