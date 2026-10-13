# Script cost, GSK and GTK4: bounded follow-ups

## Included scripts

The owner's question is recorded in [#570](https://github.com/pixelelated/distribution/issues/570#issuecomment-6138563287).
Actual authorization loads provider bundles and paths for analytics/marketing,
fingerprinting, CAPTCHA and identity providers. Their presence is not proof of
high execution cost. The user-agent comparison establishes different modern and
fallback bundles; responsive widths do not change that split. Later heartbeat and
single-outstanding-evaluation stalls establish page-process unresponsiveness, not
which script or whether execution, rendering or reclaim caused it.

Next attribution should correlate JavaScript/CPU activity, input-to-paint and
kernel reclaim on a controlled page/session, then isolate a justified factor.
The current WebKit recipe disables ENABLE_SAMPLING_PROFILER and USE_SYSPROF_CAPTURE;
a full profiler may require an isolated diagnostic build. Resource timing duration
is not CPU execution time, cross-origin zero sizes may reflect access restrictions,
and response content lengths are not measured total traffic. Do not equate a broken
or blocked sign-in page with a performance fix. No script blocker was introduced.
Upstream tools: [Web Inspector timelines](https://webkit.org/web-inspector/timelines-tab/)
and [CPU timeline](https://webkit.org/blog/8993/cpu-timeline-in-web-inspector/).

## Renderer applicability

The current package depends on gtk3 and pkg-config gtk+-3.0/webkit2gtk-4.1;
[the compiled binary readback](linked-gtk.txt) confirms GTK3 libraries. WebKit's
recipe sets USE_GTK4=OFF. GSK_RENDERER selects GTK4 renderers, so there is no GSK
comparison on this GTK3 app. The earlier DMA-BUF/Panfrost controls are a different
layer; neither their truncated public-page peaks nor a GPU-enabled VM with browser
acceleration still disabled establishes a renderer winner.

The owner asks “Should we try GTK4?” [#576](https://github.com/pixelelated/distribution/issues/576)
tracks a bounded isolated experiment. WebKitGTK6 is the GTK4 API, not engine version6.
Same-engine GTK3/GTK4 controls must disclose unavoidable dependency, API, process
and sandbox changes. Keyboard injection, GTK layout/drawing/lifecycle, temporary
network sessions, related popups and callbacks all need compatibility proof.
GTK4 does not remove the page's JavaScript workload. The GTK4 experiment has not
been compiled or run in this packet. Do not claim it uniquely brings the new
WebKit2.54 rendering architecture to a browser already using WebKit2.54.

Upstream references checked October13:
[GTK4 running/renderers](https://docs.gtk.org/gtk4/running.html),
[GTK3 migration](https://docs.gtk.org/gtk4/migrating-3to4.html),
[WebKit6 migration](https://github.com/WebKit/WebKit/blob/main/Source/WebKit/gtk/migrating-to-webkitgtk-6.0.md),
[WebKit2.54 highlights](https://www.webkitgtk.org/2026/09/16/webkitgtk-2.54-highlights.html).
The worker must check exact source versions and available backends before claiming
build feasibility or selecting a renderer. No incident-specific upstream GTK4 fix
has been established.
