# Browser provider and script attribution — October 16, 2026

[#616](https://github.com/pixelelated/distribution/issues/616) owns the owner's
verbatim request and the VM-first comparison plan. D-WORKFLOW-169 refines the
current order: page/provider attribution precedes implementing service suspension.
#587's busy-stop safety finding remains independently required before adopting
any proxy stop policy. #570's accepted allocator/recovery fixes remain accepted.

## What this work actually ran

Read-only reanalysis of eight retained October13 real Dropbox authorization
trials. No new browser, VM, service, provider request, device operation or build.
`retained-analysis.json` binds the original compressed samples, analysis and
script sets by SHA256. Reproduce from the repository root:

```sh
python3 -I docs/qa-logs/2026-10-16-browser-provider-attribution-616/analyse-retained.py --repo .
```

At aggregate browser peak, WebKitWebProcess accounts for **365.00–415.57 MiB
PSS**, of **456.59–510.94 MiB total browser PSS**. Its anonymous memory at those
points is **292.58–370.73 MiB**. These are process allocations, not JavaScript heap
measurements. No proxy service ran. All eight trials record allocation stalls and
file reclaim/refault work over their complete observer windows. These counters
are not timed proof that reclaim caused an individual heartbeat stall.

The current handset identity received Dropbox fallback bundles; the other tested
identities received modern bundles. Both desktop observations had shorter maximum
heartbeat gaps (538/590 ms versus handset1931/5079 ms), while RAM remained similar.
Other modern-bundle identities also stalled. Two observations do not establish
a winning UA, a leaking script, a historical regression or a provider ranking.

**Scope:** 1280 MiB assigned /1042.625 MiB visible, software rendering, historical
browser/frontend, unauthenticated actual rclone OAuth page, untouched cookie
overlay, no physical phone. Read the JSON limits and original
[packet](../2026-10-13-dropbox-user-agents/README.md). The October16 26.27 MiB
proxy result uses a different synthetic workload and cannot be subtracted from
these browser figures to predict a usable H700 session. The historical device
proxy footprint also differs from the tiny synthetic cache.

## Browser controls exist, but do not constitute a fix

`source-capabilities.json` records exact2.54.1 source support for
`webkit_settings_set_enable_javascript`, file-backed JSON user content filters
and attaching them to the content manager. Historical GENERIC configuration
enables content extensions, remote inspector and resource usage. The current
product sign-in window does not configure a JS switch or content filter. No new
installed ABI, diagnostic compilation or product filter was tested here.

Official references checked October16:
- [JavaScript setting](https://webkitgtk.org/reference/webkit2gtk/2.42.5/property.Settings.enable-javascript.html).
- [JSON content filters](https://webkitgtk.org/reference/webkit2gtk/stable/class.UserContentFilterStore.html).
- [Inspector profiling](https://webkit.org/web-inspector/timelines-tab/): JavaScript,
  CPU, layout and memory views exist; memory/heap recording itself adds overhead.
- [Google OAuth embedded-browser error](https://developers.google.com/identity/protocols/oauth2/native-app#disallowed_useragent):
  a policy-error page is not a faster successful login.

Full-JavaScript-off is only a diagnostic subtraction. Selective blocking should
follow measured resource/execution attribution and preserve authentication,
security checks, navigation and recovery. A downloaded analytics-looking filename
does not prove execution, high cost, or independence from a shared auth bundle.
Provider bundles and hashed filenames can change. No blocklist or default UA
change is selected. Memory-cleanup policies can free dead objects/caches but
cannot make the live page working set disappear; additional GC may cost CPU.

## Next experiment, still UNRUN

Can this be done on the VM? Yes. The issue fixes the staged comparison: a light
local page plus real unauthenticated Dropbox/Google Drive/OneDrive authorization,
same engine/UA/viewport/frontend/background state, fresh contexts, reordered
repeats and separate provider-error outcomes. First establish a profile with RAM
headroom, then repeat changing only RAM to1GiB. Measure browser processes,
reclaim and usable-page/input latency with a lean observer; measure observer cost.
Use separate bounded profiling passes for script CPU/heap/layout attribution.
Compare the historically relevant UA separately. Any subsequent one-resource
filter/polling/GC experiment must preserve working sign-in and original failures.

Fresh admission, owned watchers, independent guards and compact retirement are
required before launch. No credentials, persistent remote or personal cloud data
are needed for initial-page work. H700 corroboration follows portable attribution;
the physical loaded-page exit question in #615 remains inconclusive. The shared
library/API source review is not a new engine benchmark. No runtime is active.
