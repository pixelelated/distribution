# Browser stack accounting review — #570, 2026-10-13

This packet starts with a source/evidence review and continues with eight bounded
physical browser controls. The initial RG SP census timed out before execution.
The owner then identified the separate RG35XX SP as the browser bench (D-QA-060);
its identity/source/power were verified and all measurements below use that device.
#570 quotes both requests and the VM-first/physical-driver boundary.

## Confirmed source behavior

Accepted ES c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78:
ApiSystem.cpp478–504/561 onward keeps the ES process, opens cloud_oauth, then
calls launchExternalWindow_before (audio/volume deinit, Window::deinit). Window.cpp
unloads reloadable resources, renderer and input; it does not discard the whole
application/game database. The main thread waits for cloud_oauth, then reinitializes.
Other ES worker threads are not proved suspended. There is a launch/return overlap
to measure: cloud_oauth open waits for the process to exist, not for a rendered
frame, and returns before ES renderer teardown. Recent diagnostic direct launches
bypassed this normal handoff and kept ES resident/rendering.

cloud-signin-window.c949 sets WEBKIT_DISABLE_DMABUF_RENDERER=1 unless the environment
already supplies a value. This is deliberate D-WORKFLOW-048/#228, commit4137690ec1,
introduced after a low-memory VM failure. Exact WebKit2.54.1 source confirms:
AcceleratedBackingStore.cpp86 returns an empty transport-mode set for this value;
canUseHardwareAcceleration returns false; HardwareAccelerationManager.cpp40 disables
accelerated compositing; WebPreferencesGtk.cpp34 disables hardware acceleration,
forced compositing and threaded scrolling. A hardware-policy setting cannot
force acceleration through this capability guard. This describes the browser's
rendering policy, not whether Sway or other clients use the GPU.

The October12 public-virgl fixture supplies no override, so it retained the browser
disable flag even with a GPU-enabled guest. Its roughly391MiB PSS result is NOT a
browser-acceleration on/off comparison. Re-read prior conclusions with that limit.
No production flag is changed by this review.

## Existing memory and concurrency evidence

October12 bounded H700 direct-launch public-page samples: browser peak501.79MiB PSS,
ES71.22–99.21MiB PSS. Those are time-varying observations, not simultaneous values to
add. Public source: ../2026-10-12-browser-isolation/handheld.json.
The incident's retained snapshots also show Sway, PipeWire, Tailscale,
NetworkManager, Python support processes and kernel reclaim activity around the
browser workload. These CPU-sorted snapshots are incomplete memory censuses;
RSS is not summed or equated with PSS. Other services are not ruled out.

Anonymous memory dominates the measured WebKit page process; supplying corrected
GStreamer dependencies removed warnings without materially lowering PSS. This does
not identify the allocations within that process as JavaScript versus graphics.
Kernel slab, page tables, graphics allocations, shared memory and reserved/CMA
usage must accompany process PSS in the next accounting. MemAvailable cannot be
reconstructed by naively subtracting a few process PSS values from total RAM.

The x86 VM uses software graphics or virtual virgl, not the H700's Cortex-A53/Mali-G31
and Panfrost stack. Guest-visible RAM and CMA differ. Prior boot logs show a GPU
clock-lock warning and CPU boost warnings before browser launch; these are leads,
not proof of renderer fallback, throttling, or the browser incident's cause.
Earlier #310 SDL/Mesa renderer-reload leaks were fixed and qualified; that history
supports measuring reloads, not assuming those defects have returned.

## Upstream check and next proof

Checked2026-10-13: official [graphics architecture](https://docs.webkit.org/Ports/WebKitGTK%20and%20WPE%20WebKit/Graphics.html)
and [2.54 rendering changes](https://webkitgtk.org/2026/09/16/webkitgtk-2.54-highlights.html).
GPU drawing, browser compositing/transport, video decoding and the desktop compositor
are separate layers. GPU capability is not evidence an application uses it, and
GPU buffers can add memory rather than automatically reducing it. No newly confirmed
upstream fix or production setting change follows from this review.

Next #570 order: whole-process/kernel/graphics census through normal ES launch,
steady page/navigation and return; matched acceleration-off/on runs with actual
policy/driver/buffer evidence and CPU/latency/PSS/pressure/recovery; physical H700
corroboration only for its driver/clock facts; earlier2.52.6 comparison afterward.
Keep the original older-engine/runtime and failed-matrix evidence. All three diagnostic owners have completed and exited. The physical controls below
are complete; normal ES handoff, navigation/input and recovery qualification remain
open. No root cause or production fix is established.

## RG35XX SP bench results

D-QA-060 permits repeated browser diagnostics and diagnostic builds on this named
bench while protecting saves and other owner data. The separate RG SP stays off.
Installed source bc9dfe8141, WebKit2.54.1, native640x480, Panfrost,998120KiB visible
RAM,32768KiB CMA and no swap. External power,100% battery. The VM's larger CMA
reservation and x86/virgl do not reproduce these physical facts.

Idle census covers all readable process smaps, kernel memory, services and GPU nodes.
Approximate PSS: RAOfflineProxy105.4MiB (PID644, confirmed by service cgroup),
ES101.9MiB, Tailscale43.1MiB, Sway26.5MiB; available556.1MiB. Under pressure the
proxy and ES remain around76–78MiB and74–76MiB respectively. These are observations,
not proof of a leak. File-backed pages can be reclaimed; a busy-looking process is
not necessarily the memory cause. No service was stopped to improve a result.

| Control | Page loaded | Observed peak browser PSS | End / limit |
| --- | --- | --- | --- |
| Simple, acceleration off | Yes; frame reviewed | 133.65MiB | 25s duration |
| Simple, acceleration on | Yes; frame reviewed | 163.70MiB | 25s duration |
| Public, initial off | Yes in log; early frame still opening | 481.10MiB | memory guard at41.5s |
| Public, initial on | No | Not comparable | pressure guard before page process |
| Public, settled on/off retries | Neither | Not comparable | PSI guard with ample available RAM |
| Public, accounted on | Yes; frame reviewed | 373.46MiB | pressure/headroom guard at25.5s |
| Public, accounted off | Yes; frame reviewed | 483.27MiB | headroom guard at46.7s |

**The final public peaks do not establish a memory advantage:** both runs were
truncated by guards at different times and their public-page presentation/timing
varied (cookie banner in the on-frame). These are preliminary ordered observations,
not repeated fixed-workload benchmarks. They establish that both paths can load
on H700, acquire different GPU resources, and still encounter pressure.

The accelerated page process holds a Panfrost DRM client with about17.2MiB resident
buffers on the simple page and27.9MiB in the final public sample. With acceleration
disabled the page process has no DRM client; the GTK parent still opens one. This
is application-path evidence beyond merely enabling a GPU for the guest. Do not
sum duplicate client descriptors, shared DRM buffers or GPU bytes with PSS: see the
[kernel DRM accounting reference](https://kernel.org/doc/html/next/gpu/drm-usage-stats.html).

The first PSI-only retries stopped at520/429MiB available before load. PSI measures
stall time, including refault/reclaim, not unused capacity; see
[kernel PSI documentation](https://www.kernel.org/doc/html/latest/accounting/psi.html).
The final harness retains the sampled160MiB available cutoff and requires
available<256MiB for the additional PSI>5 cutoff. These are sampled thresholds,
not guaranteed memory reservations. It also records vmstat/process faults and
requires three settled baseline samples. On/off final runs show13283/33415 file
refaults,3020/666 direct scans,42/1 normal allocation stalls and281/642 major faults.
This confirms reclaim/refault work occurred, without isolating its original cause.
All original incomplete outcomes remain in trials.json and owner records.

All three watched owners, wrapper/build channels and actual launcher exits are0;
that means the guarded experiment completed, not that the browser passed load or
stress acceptance in every case. All owned browser processes exited. Exact-result
hashes were checked before deleting the three temporary device directories
(~17.6MB). Final read-only census shows the same boot and ES PID2697, with546.7MiB
available. No reboot, game, credential/config edit, account sign-in or cloud action
occurred; no save-writing operation was invoked. A full save-byte comparison was
not part of this experiment. No product code, pin or permanent graphics setting
changed. All measurements use direct launch with ES/services resident; normal ES
resource-release handoff remains the next VM software control.

manifest.json binds firmware/browser/ES hashes and five reviewed frames. trials.json
is the compact outcome index; samples.json holds sanitized process/kernel/GPU
measurements without argv, arbitrary environment, owner configuration or account
content. Exact frozen fixtures and original channels remain alongside them.
