# Browser rendering alternatives — October17

Refs #616, #576, #617; D-WORKFLOW-170. This is a source/upstream review and
parallel-work record, not a new browser benchmark. Product firmware remains
077197/ES16dbac. No production toolkit, engine, graphics policy or UA changed.

## What can change performance

| Candidate | Relevant change | Current evidence and limit |
| --- | --- | --- |
| Existing GTK3/WebKit, acceleration enabled | Enables WebKit page compositing/DMA-BUF instead of the product's shared-memory path | October13 H700 page process acquired a Panfrost DRM client and both paths loaded. Public-page runs hit guards at different times/states, so they do not rank speed or memory. |
| GTK4 / WebKit6 API | Changes widget rendering, frame import/composition and application/input APIs, keeping WebKit/JavaScriptCore2.54.1 | Exact dependency/API inventory exists; no GTK4 compile or runtime result. New parallel spike prepares concrete overlays and native-input solution. |
| Blink via Chromium/CEF | Changes page engine and JavaScript engine as well as integration and GPU process architecture | Official Ozone supports Wayland; local Chromium addon is removed. ARM64 packaging, sandbox, input/redirect/cleanup and actual GPU use must be proved. No local Blink benchmark. |

Current WebKit is **2.54.1**, GTK3, webkit2gtk-4.1 API. The4.1 is not GTK4.
Exact OptionsGTK sets USE_SKIA ON and USE_CAIRO OFF; retained GENERIC_X64 and
H700 CMake caches confirm USE_SKIA ON / USE_GTK4 OFF. Cairo remains a toolkit
dependency, not this engine's page painter. The current engine also disables
the sampling profiler; full JavaScript CPU attribution may require a separate
engine build. Runtime UA changes do not require such a rebuild.

The parallel [GTK4 spike](../2026-10-17-gtk4-spike/performance.md) identifies a
specific improvement to test: exact2.54.1 `AcceleratedBackingStore.cpp` passes
previous textures and changed regions through GTK4 DMA-BUF APIs (>=4.13.4),
and newer memory-texture APIs (>=4.16). The older fallback wraps a Cairo surface
and ignores those update-region arguments. That final presentation layer is
where GTK4 may avoid work, even though the page painter is already Skia.
This is source-backed opportunity, not a measured speedup or memory saving.

The sign-in app defaults WEBKIT_DISABLE_DMABUF_RENDERER=1 with overwrite=FALSE,
so an explicit launch environment can select the other path without rebuilding
the image. Exact source analysis and prior H700 evidence in
[browser-stack](../2026-10-13-browser-stack/README.md) show this also gates WebKit
hardware compositing. A GPU-enabled compositor/VM alone does not mean the page
process is accelerated. No default change follows from this observation.

## Upstream evidence, checked October17

[WebKit2.54 highlights](https://webkitgtk.org/2026/09/16/webkitgtk-2.54-highlights.html)
document the Skia compositor and removal of Cairo page rendering. Their reported
Raspberry Pi4 MotionMark gains (about36%, composition-focused about45%) concern
the shared engine changes, not a GTK3-to-GTK4 comparison. Our current engine is
already in that series; those percentages are not a forecast for H700 or Dropbox.

[WebKit graphics architecture](https://docs.webkit.org/Ports/WebKitGTK%20and%20WPE%20WebKit/Graphics.html)
describes shared-memory and DMA-BUF transport, and recent GTK texture imports.
[GTK rendering documentation](https://docs.gtk.org/gtk4/question_index.html)
describes GL/Vulkan widget rendering. The dated
[GTK renderer announcement](https://blog.gtk.org/2024/01/28/new-renderers-for-gtk/)
also illustrates why a newer GPU renderer is not automatically faster. Its2024
renderer rankings are historical, not a current4.24 benchmark.

[Chromium Ozone](https://chromium.googlesource.com/chromium/src/+/main/docs/ozone_overview.md)
documents Wayland and accelerated graphics platform support. It does not show
that Blink consumes less memory or outperforms WebKit on this login page.
[Mesa Panfrost](https://docs.mesa3d.org/drivers/panfrost.html) documents Mali-G31
GLES3.1 support; H700's recipe selects g31/panfrost, GLES preference and Wayland.
The current upstream table also lists Vulkan for this family, with experimental
driver caveats. That is not proof the installed image has a usable Vulkan path.
Start with observed GLES/GL; keep Vulkan as a separately verified variable.

## Parallel ownership and next proof

The owner requested GTK4/Blink exploration and independent tests in parallel.
Existing Herdr w4:p7/p8 failed login refresh before work. Active-session internal
agents took over; they are not working Herdr lanes. No authentication settings
were changed and no duplicate worker has write authority.

| Owner | Checkout / write scope | Deliverable |
| --- | --- | --- |
| Coordinator, Herdr w4:p2 | m7-player-setup; shared records/integration | Runtime admission, verification, provider matrix and result delivery |
| Internal gtk4_spike | m7-gtk4-576; only2026-10-17-gtk4-spike packet | Build-overlay/native-input candidate and exact dependency/renderer evidence |
| Internal blink_feasibility | m7-browser-memory-570; only2026-10-17-blink-feasibility packet | ARM64/Wayland route, synthetic comparison fixture and concrete integration constraints |
| Internal runtime_browser_controls | m7-player-setup; only2026-10-17-browser-controls-616 packet | Exact-source small diagnostic helper, per-launch UA and observer toggle |

Can this be done on the VM? **Yes** for compilation, synthetic auth and
provider/UA functionality. Only the H700's real GPU/buffer/clock/recovery facts
need later physical corroboration. Independent source work is concurrent;
performance runs sharing CPU/GPU resources remain serialized unless isolation
is explicitly established. All new graphics/runtime comparisons are UNRUN here.

The useful comparison is actual usable-page/input latency, total browser PSS,
CPU, reclaim/refaults, realized renderer and normal frontend return. Hold content,
viewport, RAM and ES/service handoff fixed; separate GPU, UA and engine changes.
GPU allocation can consume more shared system RAM while improving CPU latency.
No workaround may discard native/phone input, popup sessions, redirect allowlists,
ephemeral cleanup, saves or offline achievements. No provider error page counts
as working login. #616's broader actual-provider attribution remains current;
#587 service-stop safety and #615 physical loaded-page exit remain unresolved.

## Completed preparation and immediate order

All three source workers completed. GTK4 and Blink packets are integrated in
0d05ce9e60 and4dd24cd038. Runtime-control helpers compile for GENERIC/H700 and
pass12 actual parser checks; the separately recorded VM diagnostic results are
in [controls results](../2026-10-17-browser-controls-results-616/README.md).
Neither toolkit/engine alternative has been compiled or benchmarked. GTK4 is
first among migration builds because it preserves WebKit/JavaScriptCore; Blink
stays a fallback comparison. Next: isolated Graphene, GTK4/sandbox dependencies,
then WebKit6; preserve existing toolchains and allocate each stage separately.
