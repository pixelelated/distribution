# What GTK4 might improve on this image

The GTK3-versus-GTK4 distinction is more specific than Cairo versus GPU.
WebKit2.54.1 already uses Skia for page painting and its compositor. Its release
announcement describes benefits shared across the GTK and WPE ports; those
numbers are not GTK4-versus-GTK3 measurements on H700. GTK3 WebKit on Wayland
also had an EGL-accelerated UI path before the current engine. Our small GTK3
loading spinner still uses Cairo, and GTK3's fallback buffer presentation also
uses Cairo; neither establishes that all page rendering does.
[WebKit2.54 highlights](https://www.webkitgtk.org/2026/09/16/webkitgtk-2.54-highlights.html),
[WebKit developer's Wayland/GTK architecture](https://notes.igalia.com/p/3AG5PqBJx).

There is a concrete GTK4 advantage to test in **our exact2.54.1 source**:
`Source/WebKit/UIProcess/gtk/AcceleratedBackingStore.cpp` at329–372 selects
GdkDmabufTextureBuilder for GTK>=4.13.4 and gives it the previous texture plus
changed rectangles. At560–594 and662–693, GTK>=4.16 does the equivalent for
mapped GBM/shared-memory textures, whereas the older branch ignores those
update-region arguments and wraps a Cairo surface. Our proposed GTK4.24.1 meets
both thresholds. The source is already present in our engine; the GTK3 build
cannot use those GTK4 APIs. This is a credible mechanism for avoiding
unnecessary texture update work, not a quantified CPU/RAM improvement.
[Upstream damage support issue269452](https://bugs.webkit.org/show_bug.cgi?id=269452),
[exact2.54.1 backing-store source](https://github.com/WebKit/WebKit/blob/webkitgtk-2.54.1/Source/WebKit/UIProcess/gtk/AcceleratedBackingStore.cpp).

The current application defaults WEBKIT_DISABLE_DMABUF_RENDERER=1. The exact
backing-store transport selector at81–100 returns before enabling that renderer
when the variable is nonzero. Therefore setting GSK_RENDERER=gl alone cannot
prove the page took the desired DMA-BUF path. Compare a matched GTK3/GTK4 pair
with this variable controlled independently, and record realized GSK class,
actual WebKit transport/buffer type and Panfrost driver evidence. The related
FORCE_SHM control is a separate variable, not equivalent to disabling the whole
renderer. Existing October13 accelerated H700 evidence was guard-truncated and
provides no performance ranking. Vulkan is not assumed; the first overlay
explicitly enables the Wayland/GL candidate and disables Vulkan.

GTK's renderer developers explicitly warned that GPU renderer changes are not
universally faster and may expose driver issues. That2024 report is architectural
background, not current4.24 performance evidence. No directly applicable
GTK4-versus-GTK3 Dropbox/1GiB/H700 benchmark was established by this bounded
research. The experiment is justified by the texture/damage mechanism and the
owner's hypothesis; only local measurement can establish its value here.
[GTK renderer design and limits](https://blog.gtk.org/2024/01/28/new-renderers-for-gtk/).

Separate the measurements: a synthetic input/API test first; then unchanged
real-provider URL/UA/CSS viewport/engine/policy with low-overhead CPU/PSS/reclaim,
readiness and input-to-paint observations; GTK3 stock and sandbox/process-swap
aligned GTK3 controls against GTK4. The new API's session/process model and
sandbox addition are confounders and need explicit results. Profile/script
changes do not belong in the first renderer comparison. GSK Cairo is useful as
a GTK4 toolkit control but does not turn Skia page painting into Cairo.

This packet makes no adoption decision, performance ranking, no-memory-pressure
claim or provider compatibility claim. Full runtime work remains unrun.
