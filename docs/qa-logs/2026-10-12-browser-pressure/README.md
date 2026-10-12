# Browser pressure investigation — #570

The retained H700 DDR3 incident points to sustained memory pressure during
sign-in. Available memory fell from610MiB before the browser to94,75,and53MiB
in successive five-minute samples, then returned to628MiB after the owner's
reset. WebKit's web process occupied about480–500MiB during those samples.
The complete retained kernel journal has243 memory-pressure cache flushes,
with no matching recorded OOM kill, kernel panic, lockup, or storage I/O error.
No pstore files survived; a cold reset can erase ramoops, so absence does not
exclude a failure. Boot-time GPU/clock warnings precede browser launch and
reappear at the next boot; their relationship to this incident is unproved.

Raw device readbacks and the owner's report stay private. This packet contains
selected resource aggregates, source bindings, and credential-free VM evidence.
No mutation, screenshot, input, provider request, or cloud action was performed
on the owner device/account. The isolated VM requested the public login page
without entering credentials. The window log lived in /run and did not survive the reset.

## Source comparison

Accepted device bc9dfe8141 and VM20 1a02664844 have identical browser source,
cloud_oauth, WebKit recipe, and machine-info bytes; hashes are in the incident
summary. Compared with accepted October9 8b5113fa16, the browser gained bounded
sign-in popup handling, exact identity-provider host exceptions, history-key
handling, and French finishing copy. WebKit and CHASSIS did not change in that
interval. Compared with September29 69e6039f8f, WebKit changed2.54.0→2.54.1
and CHASSIS=handset was added. The owner's earlier responsive baseline is not
source-bound, so neither interval establishes the regression's cause.

The accepted ES pin c8dc72cf9e calls launchExternalWindow_before only after
the browser opens. Window::deinit unloads reloadable resources and the renderer;
the game database/process remains. This confirms intended release, not the
amount actually released in the incident. WEBKIT_DISABLE_DMABUF_RENDERER=1
is still set by the browser unless explicitly overridden. No live incident
environment was captured, so the active renderer override is unknown.

## Disposable VM comparison

Can this be done on the VM? Yes for source-controlled resource and navigation
experiments; the H700 memory/GPU/CPU behavior remains a hardware constraint.
The accepted image was booted with1024MiB assigned instead of canonical8192,
16GiB disk,640x480 and software rendering. Its visible MemTotal was791MiB,
not the device's974MiB, and the guest exposes no /proc/pressure/memory.
This is a diagnostic deviation, not new candidate or hardware qualification.

Existing tools/signin-memory loaded example.org for35s (peak summed RSS279MiB)
and the public provider login page for90s (385MiB). Both original runs ended0;
reviewed frames confirm a login page rather than a placeholder/error page.
The latter emitted WebKit memory-relief messages. It did not reproduce the
full hang, navigate through authentication, or measure phone input latency.
The helper starts the browser directly with the local keyboard and leaves ES
resident; it does not prove the real phone-keyboard handoff. Its immediate
post-close memory reading was transient; a subsequent read found all browser
processes gone and roughly401MiB available again.

## Remaining work

#570 remains open. Reproduce longer page/navigation and handoff behavior with
bounded resource/input observations, then qualify a low-memory recovery policy
before changing production limits. A per-process limit or forced termination
could prevent a hang while also breaking authentication; do not call it a fix
without successful ordinary navigation and controlled pressure/failure cases.
Upstream documents configurable memory-pressure handling, including the cost
of overly aggressive reclamation:
https://webkitgtk.org/reference/webkit2gtk/stable/struct.MemoryPressureSettings.html.
No browser setting or production source was changed in this investigation.

#571 separately owns phone status layout. cloud_oauth's probe already treats
open/loading as a live window, but the page changes a short padded Connected
banner to a longer unpadded loading paragraph. That changes control positions.
Keep connection health distinct from page/field readiness; only the latter
should gate queued typing. The compact accessible header and its EN/FR
navigation/failure/reconnect/ended-session frame proof remain to implement.
