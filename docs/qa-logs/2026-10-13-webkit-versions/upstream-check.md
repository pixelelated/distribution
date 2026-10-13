## Upstream release and issue check — 2026-10-13

Maintainer:
> Is there a version newer than the one we currently have? Also, have we checked to see if any of these issues are addressed or if any issues are reported?

Our WebKitGTK recipe remains 2.54.1. The [official release directory](https://webkitgtk.org/releases/) still identifies 2.54.1 (October 2) as the latest stable release; no newer published stable tarball was found. [2.54.1 notes](https://webkitgtk.org/2026/10/02/webkitgtk2.54.1-released.html) describe rendering, tile-raster and crash fixes but do not establish a fix for this Dropbox memory case.

- [319590](https://bugs.webkit.org/show_bug.cgi?id=319590): Skia font-variation memory growth, fixed in August and backported to 2.52.6. Inspected the exact cached 2.54.1 source and freshly verified 2.54.0 source: both contain the variation-typeface cache and pressure-release calls from commit 6b324fb4b79e. This is already present, not a missing upgrade fix. Source hashes are retained with the diagnostic packet.
- [305401](https://bugs.webkit.org/show_bug.cgi?id=305401) fixed one GTK3 DMA-BUF release defect. Follow-up [306430](https://bugs.webkit.org/show_bug.cgi?id=306430) remains NEW; its reporter reproduced continuing buffer growth on X11 with DMA-BUF in 2.50.4. Our Wayland browser explicitly disables that renderer, so applicability is not established.
- [268477](https://bugs.webkit.org/show_bug.cgi?id=268477) is an older reopened memory-pressure/cache report. It is a lead, not a confirmed match or an available fix for our source.
- [2.54.0 notes](https://webkitgtk.org/2026/09/16/webkitgtk2.54.0-released.html) identify the compositor switch from TextureMapper to Skia. The boundary remains worth measuring; no causal claim follows from the release note.

At the initial check, the 2.54.0 package-only build was running; it has since completed. The README records the subsequent failed low-memory matrix and successful headroom controls. Current-engine diagnostics completed all three bounded probes, with no surviving browser processes or forced cleanup: clean Dropbox peak browser PSS 380.98 MiB/minimum MemAvailable 64.97 MiB; instrumented Dropbox 387.88/61.86 MiB. Sampler instrumentation is separate evidence because it can change allocation. Native frames show the public login page. These are reproduction measurements, not successful authenticated sign-in or usability acceptance.

The standing requirement to make this check early in future investigations is #573 (D-WORKFLOW-162). No production pin or owner-device state was changed.
