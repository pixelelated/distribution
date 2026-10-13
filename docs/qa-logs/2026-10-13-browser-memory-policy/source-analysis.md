# Exact-source findings

All `Source/…` and generated configuration paths below are relative to the
WebKit root in [inputs.json](inputs.json). That manifest binds full file bytes and
provides anchor line numbers. These are source deductions, not target observations.
The application baseline SHA256 is
`39af3e041d9871c4fb636cff71934ddf3ea13c690002e77af5ea6d82d8fff4f8`.

## Two different monitors, neither a browser PSS budget

| Mechanism | Exact 2.54.1 behavior | Consequence for #570 |
| --- | --- | --- |
| WebProcess periodic handler | `WTF/MemoryPressureHandler.cpp`: base = min(3 GiB, `ramSize()`), conservative = 0.33, strict = 0.50, poll = 30 seconds; optional kill fraction unset | Fractions apply independently to each process, not summed browser/ES/OS memory |
| Physical RAM | `WTF/AvailableMemory.cpp` uses Linux `sysinfo.totalram * mem_unit`, cached once; `RAMSize.cpp` caches that result too | This is kernel-visible RAM, not assigned VM RAM, current MemAvailable, or a cgroup limit; API override does not change JSC's `ramSize()` |
| Process footprint | `WTF/linux/MemoryFootprintLinux.cpp` returns resident pages from `/proc/self/statm` via `CurrentProcessMemoryStatus.cpp` | RSS, including shared resident pages, not PSS, private anonymous memory, or JS heap size |
| System monitor | `UIProcess/linux/MemoryPressureMonitor.cpp`: estimates used percentage from MemTotal and MemAvailable; polls every 1–5 seconds, noncritical at >=90%, critical at >=95% | Can request cleanup independently of the context's fractions; it does not kill the process itself |
| Cgroup branch of system monitor | Reads the UIProcess's `/proc/self/cgroup`, builds paths under `/sys/fs/cgroup`, takes the greater of system and usable cgroup usage percentages | Context settings neither replace nor configure this separate detector |

The generated `.x86_64-rocknix-linux-gnu/cmakeconfig.h` has
`ENABLE_PERIODIC_MEMORY_MONITOR=1`, `USE_SYSTEM_MALLOC=0`, `HAVE_MALLOC_TRIM=1`,
`USE_SKIA=1`, `ENABLE_JIT=1`, and `ENABLE_RESOURCE_USAGE=1`. The WebProcess enables
its timer if FastMalloc is enabled (or specific debugging options request it),
after applying the GLib creation parameters. Check actual allocator overrides in
the target launch environment before claiming the timer ran. A getter in the
UIProcess only proves the intended settings, not receipt or execution in a child.

For the historical 1,067,648 KiB MemTotal, physical base is 1042.625 MiB;
default conservative and strict boundaries are about 344.07 and 521.31 MiB RSS.
`strict35` moves only the latter to about 364.92 MiB. These are arithmetic source
predictions using a historical input, **not observed crossings**. API
`get_memory_limit()` truncates to whole MiB, so its printed 1042 must not be used
to recompute exact byte thresholds. Re-read the new guest's MemTotal/sysinfo.

[historical-input.json](historical-input.json) copies two existing breakpoint
samples nearest elapsed 30 seconds: desktop640 WebProcess RSS 375352 KiB
(366.55 MiB), desktop360 359880 KiB (351.45 MiB). A 40% strict fraction would not
activate at either point. The selected 35% fraction would classify the first
as strict and the second as conservative. This justifies a threshold that can
separate policies in an observed RSS range without also changing the base or
polling interval. The samples are not proved to coincide with child timer ticks,
and no new range/CPU/causation attribution is claimed. In this historical RAM
range, the conservative-only band narrows to about 344–365 MiB. The more frequent
critical cleanup that may result is precisely the CPU/latency tradeoff to test.

Cgroup details matter. The code first tries a v2 `memory.memsw.max` file (do not
assume such a file exists), then the minimum valid numeric `memory.max` and
`memory.high`. `max` text becomes unavailable, so one valid numeric file can
still supply the limit. Usage comes from `memory.current`; v1 prefers memsw
limit/usage, then memory limit/usage. The code does not walk ancestors or discover
arbitrary mount locations. It does not use `memory.swap.max` or PSI here. An
unlimited leaf under a limited ancestor can therefore differ from effective
kernel enforcement. Capture the UIProcess membership, mount layout, leaf AND
ancestor limits for interpretation; do not change limits to make the candidate
work. No current guest cgroup state was observed by this worker.

## Cleanup, GC, and termination are different outcomes

`MemoryPressureHandler::measurementTimerFired()` checks the kill boundary first.
It then classifies RSS: unrestricted below conservative, noncritical cleanup at
conservative, critical cleanup at strict. There is no hysteresis; every periodic
tick still above a threshold can repeat cleanup. Its direct `releaseMemory()`
call is separate from the Unix notification holdoff.

`WTF/unix/MemoryPressureHandlerUnix.cpp` throttles **notifications** for at least
5 seconds, at least 20 times cleanup duration when >=1 MiB was freed, or 30
seconds after poor relief. This does not add a holdoff to the independent
30-second periodic timer. `malloc_trim(0)` follows cleanup in this build.

`WebProcess/WebProcess.cpp` connects the handler to WebCore and each page.
Noncritical requests become critical when there are no pages in windows. In
`WebCore/page/MemoryRelease.cpp` noncritical cleanup prunes dead resource caches,
font/style/selector/layout caches, and detached renderers/nodes. Both levels also
purge Skia caches (`page/skia/MemoryReleaseSkia.cpp`). Critical cleanup additionally
prunes back/forward cache, discards decoded live-resource data, clears the local
cookie lookup cache, attempts deletion of compiled JS code, and schedules GC and
worker cleanup. Clearing that lookup cache is not deleting the NetworkProcess's
session cookies. Live JS objects and live DOM are not made collectible by policy.
Normal strict cleanup is asynchronous for GC; kill recovery uses synchronous
cleanup/GC. Recreating decoded data or compiled code can raise CPU, latency,
network use, and subsequent refaults even when immediate RSS falls.

**Do not claim `kill_fraction=0` disables termination.** The GLib setter converts
zero to an unset optional and its getter reports zero. The exact handler then
falls back to its own state-based kill boundary. On this 64-bit target, inactive
is min(3 GiB + page-count GiB, 90% of RAM); active is 7 GiB + page-count GiB on
RAM <=16 GiB (15 GiB base above that). `PerformanceMonitor.cpp` updates activity
state; visibility alone should not be assumed to prove which state is current.
If synchronous cleanup cannot get below the kill threshold, the callback informs
the UIProcess and `WebProcessProxy.cpp` requests `ExceededMemoryLimit`
termination. This differs from kernel OOM. The candidate does not set the kill
fraction, base, or activity state. No finite low kill limit is proposed.

## API location and ownership

`WebKitWebContext.cpp:602` defines `memory-pressure-settings` as write-only,
construct-only. Setting it after `webkit_web_context_new_ephemeral()` is too
late. Its setter copies the boxed settings; construction transfers the internal
configuration to the process pool and frees the temporary copy. The pool passes
it into each WebProcess creation, and `WebProcessGLib.cpp` applies it before the
periodic handler is enabled.

The candidate mirrors `webkit_web_context_new_ephemeral()` at lines 809–812:
create an ephemeral `WebKitWebsiteDataManager`, pass it to `g_object_new` for the
context, and release the local manager reference. It adds the pressure settings
in that same constructor, then frees its local settings. Both `default` and
`strict35` modes take this construction path. Only `strict35` calls the strict
fraction setter. Unknown mode strings fail before navigation; an ephemeral
assertion fails closed. The diagnostic log contains only scalar policy/version
data. The context remains owned as in the baseline application.

The existing `on_auth_create()` still uses a related view. Exact
`WebKitWebView.cpp` inherits its parent's context, ephemeral status, and settings;
the application retains its allowed-host, user-gesture, navigation, popup,
callback, keyboard, and exit code. The source validator reverses the insertion
and single call replacement to recover **all** original bytes. This is stronger
than checking a handful of strings, but does not substitute for target testing.

The separate `webkit_website_data_manager_set_memory_pressure_settings()` is
global for subsequently created NetworkProcesses and must precede manager
creation. It enables an otherwise disabled NetworkProcess periodic check
(`NetworkProcess/soup/NetworkProcessSoup.cpp:145`). The candidate never calls it.
System pressure notifications still reach both web and network processes.

## Cache and JSC alternatives: defer, do not remove functionality

The application's default is `WEBKIT_CACHE_MODEL_WEB_BROWSER`, regardless of its
ephemeral data store. `LegacyGlobalSettings.h` and `Shared/CacheModel.cpp` give
64 MiB WebCore resource-cache capacity, 16/32 MiB min/max dead cache, two
back/forward pages, and 60-second decoded-data deletion interval for the
historical 1024–1535 MiB RAM range. These are policies/capacities, not observed
resident allocations or a ceiling on all live resources.

`DOCUMENT_BROWSER` would nominally lower that capacity to 32 MiB in this range.
`DOCUMENT_VIEWER` additionally disables the GLib MemoryCache and sets back/forward
capacity zero. The setter changes legacy **global** settings despite taking a
context parameter. Both can trade repeat-load latency and network traffic for
cache space; neither bounds live JS. Do not combine them with the strict-fraction
control. No cache switch is selected for the first experiment.

The distinct cached-*process* policy in `WebProcessCache.cpp:321` has zero
capacity below 2 GiB or when process swapping is disabled; GTK3 context swapping
defaults to false and the application does not enable it. The non-Cocoa lifetime
is already five minutes. Shortening that lifetime cannot explain or repair the
historical ~1 GiB fresh-launch pressure under these conditions.

JSC `Heap.cpp` uses its own physical RAM input. Normal heap growth factors are
2, 1.5, and 1.24 as process footprint passes 25% and 50% of RAM; aggressive mode
starts at 16 GiB. `criticalGCMemoryThreshold=0.80` compares **this process's RSS /
physical RAM**, not system pressure or cgroup use. The context's base/fractions
do not rewrite those JSC inputs. Strict cleanup can nevertheless invoke JSC GC
and code deletion through WebCore. `JSC_gcMaxHeapSize` is a bytes-allocated-this-
cycle collection trigger in this version, not a safe hard cap on live heap.
`JSC_forceRAMSize`, GC/growth knobs, JIT toggles, forced allocation-count GC, and
script blocking are not selected. Without heap/CPU attribution they conflate
the proposed cause with throughput changes; disabling JS/JIT is not this task.

## What can be observed without an engine rebuild

- The added startup line binds mode, WebKit version, intended fractions/poll,
  and ephemeral assertion. It is not a child activation receipt.
- Linux sets `shouldEnableMemoryPressureReliefLogging=true` for WebProcesses.
  Even with release logging disabled, `ReliefLogger` prints `Memory pressure
  relief: Total` through `WTFLogAlways`. Despite legacy `res` / `res+swap` labels,
  the exact Linux implementation supplies RSS-minus-shared and RSS, respectively;
  neither is PSS, and the latter is not measured swap. Async GC may finish after
  that immediate delta. Sample subsequent footprint too.
- `ENABLE_RELEASE_LOG=0`, `ENABLE_JOURNALD_LOG=0`, Release/NDEBUG: do not promise
  policy-transition/debug channel lines from `WEBKIT_DEBUG=MemoryPressure`.
  The source has no public signal reporting the child's current policy.
- `JSC_logGC=1` (or `basic`) is a normal environment option in exact
  `runtime/Options.cpp`; `Heap.cpp` emits collection kind, before/after heap
  size, pause/cycle timings via DataLog, normally stderr. Set it identically
  for both diagnostic arms if the coordinator grants it. It has overhead,
  addresses in logs are not account data, and its existence is not proof the
  target child inherited it. Keep stderr bounded; missing GC lines are unknown,
  not zero GC. No heap dumps or object contents are needed.
- Record per-process PID/starttime, statm RSS, smaps_rollup PSS/anonymous,
  stat user/system ticks and fault counts; system MemAvailable, PSI totals and
  vmstat pgscan/pgsteal/allocstall/workingset_refault_file/pgmajfault deltas.
  These separate GC/CPU, kernel reclaim, shared mappings, and total browser cost.
  `JSC_logGC` timing is not CPU accounting; receipt time on shared stderr is not
  exact event time. Do not label GC overlap causal without matched evidence.
- Cached recipe/config disable sampling profiler and sysprof capture. Page
  heartbeat and per-process CPU can bound a stall but cannot assign CPU to an
  individual provider script. Inspector attachment changes the workload; it is
  not silently introduced by this candidate.
