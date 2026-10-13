**Proposed coordinator-owned VM experiment; none executed here**

Can this be done on the VM? **Yes.** Dependency loading, input, synthetic auth,
session disposal, sandbox behavior, CPU/memory pressure, and return to ES require
no owner account or physical device. Panfrost-specific GPU allocation/recovery
is a later physical fact, after VM success and an applicable named bench scope.
The coordinator records this plan with resource and stop limits in #576 before
runtime. No previous guest/PID/port is reusable: today's22 trials are retired.

Use an independently owned disposable GENERIC_X64 guest and synthetic account
state. All diagnostics receive a hard deadline, memory guard, pidfile, and
actively consumed watcher/result/exit channels. Fix the RAM/visible headroom,
CPU, renderer, panel, service state, and cleanup baseline. A first compile or
API construction success does not license a provider benchmark.

| Required observation | Artifact that accepts it |
| --- | --- |
| Exact toolkit/engine/library loading | Build/installed manifest, ELF dependency closure, pkg-config/runtime versions, process maps, and source hashes; no unintended GTK3 libraries in GTK4 process |
| Actual sandbox | WebProcess namespace/seccomp observations and a synthetic forbidden-file negative control; API sandbox enablement alone is insufficient. Normal TLS certificate failure remains a failure |
| Parent/related session | API fixturePASS plus real synthetic popup/opener return; identical ephemeral session, shared cookie during one attempt, only one popup, rejected second/nested/disallowed popup |
| Fresh-attempt isolation | Cookie/local-storage/IndexedDB synthetic marker is visible within the related attempt and absent after complete exit/relaunch; private profile/artifact census shows no leaked persistent default session |
| Native OSK input | Pad walking/tapping types all supported printable ASCII and space; shift/symbol toggle, delete, Enter, Tab, and modified input preserve key/input/beforeinput order and native trusted events on a provider-style validating form |
| Phone ordering | None/idle/active phone cases; queued typing waits for the current page's field, move precedes click, navigation clears stale field/queued ownership, no duplication or dropped Enter/Backspace while OSK is visible |
| Keyboard focus | Email→password script transition, hidden/read-only/disabled fields, consent overlay, iframe/captcha-like controls, and popup return; no automatic re-raise after a deliberate hide without a field change |
| Navigation/security | Allowed host/subdomain and exact identity-provider tests; reject suffix tricks and disallowed gesture navigation/popups; retain needed cross-origin resources and non-gesture auth redirects. Test the current policy, not an invented total host firewall |
| Local callback | Synthetic local broker receives the expected redirect; page file/log/phone state never includes synthetic callback code; correct finishing page until the original ES frontend is ready |
| Lifecycle | Close during load/probe, popup close during evaluation, page failure/retry, phone close, Escape, pad exit, timeout, and repeated sign-in; no use-after-free, stale timers, orphan WebKit/bwrap processes, stuck input, or lost focus |
| Native layout | Reviewed640×480 and1280×800 EN/FR frames for loading, OSK letters/symbols/shift, page, popup, finishing, and ES return; frame index binds source, branch, size, language, expected state |
| ES and offline awards | Normal broker/ES launch-wait-return, same frontend PID and ready frame; synthetic offline queue/DB unchanged, reconnect delivery/readiness still passes, no service suspension to manufacture a memory result |

The API fixture supplies only the first construction assertion within the third
row. It has no window, page, main loop, input implementation, or storage-disposal
test, and cannot satisfy the other rows. Missing fixtures remain named work;
this table is an acceptance specification, not a runnable suite or a PASS list.

After functionality, compare three2.54.1 sources: accepted GTK3; GTK3 with
sandbox/process-swap aligned; and GTK4. Use the same authenticated-free synthetic
page first, then separately the actual unauthenticated authorization endpoint
if allocated. Keep UA, exact observed CSS viewport and DPR, content variant,
cookie-overlay state, keyboard policy, network/resource observations, observer
cost, and DMA-BUF flag fixed. Repeat reordered with settled baselines. Public
content can change between trials; record that limitation.

GTK4 cases: default, Cairo, current GL, and Vulkan only if compiled and supported.
Record `G_OBJECT_TYPE_NAME(gtk_native_get_renderer(GTK_NATIVE(window)))` after
realization, selected GDK backend, GL/Vulkan driver, and actual WebKit page-process
DRM/transport evidence. `GSK_RENDERER=help`, an environment variable, or a GPU fd
in the GTK parent alone does not prove the selected page renderer. GTK4.24
`ngl`/`gl` are aliases, not an independent pair. Treat fallback/unsupported cases
as such; do not rank them under their requested names.

Measure full browser process-tree PSS/anonymous/file/shmem, CPU, faults/refaults,
direct reclaim/allocstalls/PSI, MemAvailable, kernel/cgroup totals, WebKit process
swaps, and GPU buffers without double counting shared allocations. Retain
event-issued, acknowledged, and visibly-applied input times. Heartbeat/evaluation
latency measures process availability; it is not touch-to-paint. Capture actual
native frames and ES return/recovery. Use paired budgets declared before the
run, and compare complete trajectories rather than unequal guard-truncated peaks.
Do not call a page usable merely because `load-finished` fired or an occluded
field has positive width.

An adopt recommendation requires repeatable responsiveness/memory/recovery
improvement on matched complete cases with every functional/security row passing.
A tie, unsupported renderer, unresolved keyboard/security regression, or
guard-truncated run does not establish a GTK4 benefit. A production proposal
then needs clean/retained VM image qualification, normal protocols/time-to-play,
independent audit, and later physical-fact confirmation. None is waived by this
feasibility packet; a smaller #570 fix may make the port unnecessary for this RC.
