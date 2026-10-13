# Official upstream checks — 2026-10-13 UTC

Checked early, before selecting the diagnostic. Exact packaged source and its
generated build flags govern applicability; public GTK3 reference pages currently
identify older library documentation (2.42.5), so they are not exact-pin evidence.

| Official source | Finding and pin applicability |
| --- | --- |
| [WebKitGTK release index](https://webkitgtk.org/) and [2.54.1 release notes](https://webkitgtk.org/2026/10/02/webkitgtk2.54.1-released.html) | Index lists 2.54.1 as current stable, dated October 2. Notes include rendering and input fixes, with no named memory-policy fix. Already the packaged version; no new version/pin proposed. |
| [MemoryPressureSettings](https://webkitgtk.org/reference/webkit2gtk/stable/struct.MemoryPressureSettings.html) and [context property](https://webkitgtk.org/reference/webkit2gtk/stable/property.WebContext.memory-pressure-settings.html) | API exists since 2.34, targets context WebProcesses, warns of poor performance from aggressive settings. Exact source confirms construction placement and separate network API. |
| [Kill setter documentation](https://webkitgtk.org/reference/webkit2gtk/stable/method.MemoryPressureSettings.set_kill_threshold.html) | Documents zero as disabling kill. Exact 2.54.1 setter/handler path instead reaches fallback state-based thresholds. This discrepancy is recorded, not patched or filed by this worker. |
| [Bug 222738](https://bugs.webkit.org/show_bug.cgi?id=222738) | RESOLVED FIXED in 2021; introduced the configurable per-process handler. Already in pin. Its discussion distinguishes system-pressure notifications from per-process thresholds; not a missing fix to import. |
| [Bug 205806](https://bugs.webkit.org/show_bug.cgi?id=205806) / [duplicate 264036](https://bugs.webkit.org/show_bug.cgi?id=264036) | GMemoryMonitor proposal remains NEW; duplicate resolved as duplicate. Exact source still uses the hand-written polling/cgroup monitor. No ready replacement proven here; no new daemon selected. |
| [Bug 268477](https://bugs.webkit.org/show_bug.cgi?id=268477) | REOPENED report of GTK pressure/cache relief failure. Similar symptoms are not a confirmed match to this fresh ephemeral one-view flow. No landed remedy established by this report. |
| [Bug 262780](https://bugs.webkit.org/show_bug.cgi?id=262780) | RESOLVED FIXED: non-Cocoa cached-process lifetime shortened to five minutes. Exact source has it; low-RAM cache capacity is also zero. Useful negative evidence, not a candidate. |
| [Bug 164052](https://bugs.webkit.org/show_bug.cgi?id=164052) | Historical report of stalls/high disk use after memory relief. Motivation to measure reclaim and CPU cost, not evidence that today's incident has the same cause. The current Unix source already contains holdoff logic. |

A search also surfaced a purported newer cgroup path refactor,
`7ad86054636f7249776d73ae651ecbf49d2f0837` / bug 324563. Official
[commit](https://github.com/WebKit/WebKit/commit/7ad86054636f7249776d73ae651ecbf49d2f0837),
[canonical link](https://commits.webkit.org/321435@main), and
[bug](https://bugs.webkit.org/show_bug.cgi?id=324563) fetches failed in the web
tool (cache miss/not accessible). Its alleged contents are **unverified**, not
used to select this candidate or claimed as a missing fix. Exact cached 2.54.1
still uses CString and snprintf for those paths. This lookup limitation remains
visible instead of turning a search excerpt into an upstream verification.
