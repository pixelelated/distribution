# Blink feasibility for #617

Prepared October 17, 2026. **Source-only; all compile, listener, browser, VM and
device experiments below remain UNRUN.** No product package, pin, configuration,
shared record, cloud account or device changed. This is a renderer and synthetic
interaction probe, not a replacement for the sign-in application.

The practical next step is a **CEF Views probe using the matching prebuilt
Chromium engine**, initially x86_64 in a disposable VM. That avoids a full
Chromium engine build while testing the actual Blink/V8/Ozone stack. The official
index has matching Linux x86_64 and ARM64 distributions at CEF
`154.0.34+g14c5a08+chromium-154.0.8037.98`, CEF source
`14c5a089e8452874cb1a556dc3fde26ed2d87723`. This was the highest numeric Chromium
version labelled stable in the fetched index, which is not sorted by version.
It is an experiment pin, not a claim that all current security fixes are included.
Recheck release/security status before fetching or considering distribution.
[Official build index](https://cef-builds.spotifycdn.com/index.html),
[pinned Chromium compatibility](https://github.com/chromiumembedded/cef/blob/14c5a089e8452874cb1a556dc3fde26ed2d87723/CHROMIUM_BUILD_COMPATIBILITY.txt).

## What the graphics evidence supports

Chromium Ozone has a native Wayland path; CEF Views can use it. Mesa lists Mali-G31
as Bifrost v7 with OpenGL ES 3.1 capability, and our H700 options select
`panfrost`, `PREFER_GLES=yes` and the existing Sway compositor. Those facts make
hardware rendering plausible. They establish **neither a faster Dropbox page
nor less memory use** on this hardware. The published API capability is not a
claim of G31-specific conformance, or of the installed application's renderer.
[Ozone source at the selected Chromium tag](https://chromium.googlesource.com/chromium/src/+/refs/tags/154.0.8037.98/docs/ozone_overview.md),
[Mesa Panfrost](https://docs.mesa3d.org/drivers/panfrost.html).

Current WebKitGTK 2.54.1 already uses Skia for page painting. GTK's widget
renderer, page rasterization, compositing, buffer transport, JavaScript and
reclaim are separate costs. A Chromium change also changes the engine and V8,
so an improvement cannot be attributed just to eliminating GTK/Cairo.
Our retained October13 H700 proof shows a Panfrost DRM client in the accelerated
WebKit page process; guard-truncated runs did not rank performance.
See [the existing stack evidence](../2026-10-13-browser-stack/README.md),
[WebKit graphics architecture](https://docs.webkit.org/Ports/WebKitGTK%20and%20WPE%20WebKit/Graphics.html).

For a useful comparison, retain Chromium's GPU feature status and GL/ANGLE
renderer, browser/GPU/renderer PIDs, loaded Mesa libraries, render-node FDs and
deduplicated DRM client accounting. A GPU process or an EGL library alone is
insufficient. `SwiftShader`, `llvmpipe`, disabled compositing or fallback must be
reported, not silently turned into a successful hardware run. Separate internal
`chrome://gpu/` and `chrome://sandbox/` report launches are prepared; they are
not part of the timed page baseline. No forced GPU-blocklist bypass or Vulkan
override is proposed. On H700, report CPU temperatures/frequencies and visible
RAM/CMA alongside process PSS; GPU buffer bytes must not simply be added to PSS.

## Concrete integration constraints

1. **Existing package is unusable.** `packages/addons/browser/chromium/package.mk`
   is an empty, broken, x86_64-only removed-addon recipe. It is not evidence of an
   existing Blink implementation or an ARM package. `product-inputs.json` binds
   these observations to current `next` at `f511766e17fb`.
2. **Use Views, not the downloaded cefclient sample.** At the selected CEF pin,
   `cefclient_gtk.cc` forces the GTK X11 backend and calls `gtk_init`; its native
   embedding path is not a clean Wayland-only baseline. `cefsimple_linux.cc`
   has no GTK initialization and its main app defaults to Views. It still has
   optional X11 code and the standard CMake template links `X11`, so ELF
   dependencies must be checked even when the runtime uses Wayland. Native
   Wayland embedding into our GTK widget is not assumed: upstream
   [CEF #2804](https://github.com/chromiumembedded/cef/issues/2804) remains a
   separate embedding proposal. A top-level Views window is sufficient for
   the first probe.
3. **Sandbox and privileges are a real prerequisite.** Our broker starts its
   browser in the existing Sway session. Chromium's pinned zygote source
   refuses root with sandbox enabled. The probe requires a non-root guest UID,
   working user-namespace/seccomp sandbox and narrowly granted access to the
   existing Wayland socket/render node. Do not relax global permissions or add
   `--no-sandbox`. The fixture refuses sandbox-disable switches and a build
   with `USE_SANDBOX=OFF`. UID/namespace access setup and actual sandbox proof
   are not supplied by this packet. If they fail, that cell is blocked before
   any provider page. [Pinned zygote source](https://chromium.googlesource.com/chromium/src/+/refs/tags/154.0.8037.98/content/browser/zygote_host/zygote_host_impl_linux.cc).
4. **Prebuilt ABI is unverified.** Inspect the downloaded SDK's `libcef.so` and
   `cefsimple` with `readelf` for ELF machine, interpreter, `DT_NEEDED`, RPATH
   and required symbol versions; compare every dependency with the exact
   GENERIC/H700 sysroot. Do not infer compatibility from the name ARM64, run
   `ldd` on an unexamined binary or silently add a distribution's host libraries.
   H700 builds contain both arm and aarch64 roots; the installed browser's ELF
   machine and loader determine the required artifact. Only the aarch64 route
   was selected here.
5. **Product behavior is substantially larger than the probe.** The current
   broker calls `/usr/bin/cloud-signin-window` directly, so a PATH shim is not
   enough. A production CEF shell needs the real provider/related-login host
   rules, ephemeral related windows, callback handling, phone page/field files,
   native keyboard, trusted input, controller exit and normal ES teardown and
   restoration. The synthetic probe preserves none of those by implication.
   Existing credentials and cloud selected paths remain untouched.

CEF supplies native APIs for navigation, popup, keyboard and lifecycle callbacks.
`cefsimple-probe.patch.gz` exercises those API surfaces against pinned sample
source, but is **not compiled or API-qualified**. Header signatures were read;
that is not a successful build. External resources are not comprehensively
filtered by its navigation callbacks: the first guest must have no external
NIC/network, and the supplied page loads only loopback resources.
[CEF general usage](https://chromiumembedded.github.io/cef/general_usage),
[pinned navigation interface](https://github.com/chromiumembedded/cef/blob/14c5a089e8452874cb1a556dc3fde26ed2d87723/include/cef_request_handler.h).

## Prepared files and what they prove

- `upstream-inputs.json`: official index hash, exact selected records including
  archive lengths and publisher SHA-1 identifiers, pinned source hashes and
  failed source URL lookups. No binary archive was downloaded. Publisher SHA-1
  is an identity check; acquire and retain a local SHA-256 and acquisition
  receipt before any use. This is not an independent authenticity attestation.
- `product-inputs.json`: exact recipe, broker and H700 source identities.
- `probe-inputs.json` and `cefsimple-probe.patch.gz`: four exact input/output
  file hashes and raw patch hash. The overlay sets a unique root cache with an
  empty profile cache (CEF incognito semantics), requires sandbox/non-root,
  opens a fullscreen Views window, restricts navigations and related popup URLs
  to a specified `127.0.0.1` port, and closes all windows on Escape.
- `prepare.py`: refuses different source bytes, checks the patch hash, dry-runs
  with zero fuzz, applies only the overlay and checks all output hashes. It
  expects a separately admitted/extracted **standard** SDK, not the minimal or
  client archive. It does not build or launch anything.
- `loopback.py`: bounded 120-second loopback HTTP fixture, maximum180 seconds,
  one input accepting only literal `fixture` for the dummy callback. It reports
  actual viewport, DPR, unobscured center hit test, trusted input and two-RAF
  latency, related-window message and old cookie/storage presence. The dummy
  authorization code is literally `fixture-only`; it is not OAuth. A two-RAF
  measurement is a scheduling proxy, not proof of physical scanout or total
  controller-to-paint latency. No input values or arbitrary request paths are
  logged. Requested host is exact; unrelated navigation points only to
  `localhost` for a denied-host control, never a real provider.
- `plan.py`: prints an argument-array proposal using caller-supplied absolute
  binary/owner and non-root UID/port. It executes nothing and explicitly lists
  the missing lifecycle, admission and integration controls. It does not change
  HOME or reuse any existing profile. Creating those paths belongs to the
  allocated guest runner.
- `CEF-LICENSE.txt`: retained BSD license for the sample-derived overlay.

The host preparation initially refused on an incorrect exact comment anchor,
before producing a patch. The anchor was corrected against the fetched source.
That is a source-preparation failure, not a compiler or browser failure. Static
verification also caught and corrected a fixture ordering error: cookie/storage
presence is sampled before setting the fixture values, rather than in a later
animation callback. No runtime result is claimed for either correction.

## Next executable experiment, after coordinator admission

Can this be done on the VM? **Yes** for ABI, sandbox, Views, loopback navigation,
input, popup/exit, profile isolation and browser-wide measurements. Only actual
Mali-G31/Panfrost/ARM resource behavior requires H700 corroboration later.

1. Admit a fresh source/build owner. Acquire the exact **linux64 standard SDK**
   record from `upstream-inputs.json`: 689,351,019 compressed bytes. Read its
   README/license payload and inspect archive paths before extraction; never
   extract outside the owned root. Verify publisher digest and record SHA-256.
   Source and dependency checks precede all execution. No account needed.
2. On that disposable SDK, run `python3 -I prepare.py --sdk ABSOLUTE_SDK_ROOT`.
   Configure its own CMake sample build with `-DCMAKE_BUILD_TYPE=Release
   -DUSE_SANDBOX=ON`, then build **only cefsimple** with at most2 jobs, using the
   admitted build container and compatible exact target sysroot/toolchain.
   The upstream CMake sandbox hook prints a manual sudo command; it does not
   execute one. Do not run that printed command on the host. Prefer the guest's
   verified user-namespace sandbox. Stop on an ABI or package gap and retain it.
3. Proposed bounds, **estimates not allocations**: first ABI/download/build
   phase25 minutes, at most4GiB additional disk and4GiB host RAM,2CPU, with a
   watchdog and ENOSPC stop. This is a small sample/wrapper compile linked to an
   existing engine, not a new Chromium build. Extraction size and dependency
   inventory must fit before proceeding. The ARM64 standard archive is
   891,100,151 bytes and is deferred until x86_64 feasibility passes.
4. Fresh admitted GENERIC guest, initially2GiB RAM/4vCPU,16GiB virtual disk,
   no external NIC. Do not mistake virtual disk capacity for actual occupied
   build space. Preserve normal ES handoff and background-service state. Allocate
   the non-root diagnostic UID and exact Wayland/render access only in this
   disposable guest, retaining modes and sandbox evidence. Root/context policy
   is a blocker until this is proved; no host security policy change is needed.
5. Run the loopback fixture and proposed probe argv under the coordinator's
   independent180-second deadline and pressure guard. Prove: native frame and
   actual640x480 viewport; six trusted characters; matching dummy callback;
   related popup message/close; denied-host control never reaches server; Escape
   closes all browser children; ES returns; second fresh context reports no old
   cookie/storage. Keep original exits and failure cells. Internal renderer and
   sandbox report runs are separate from timing. If any compile/runtime surface
   differs, fix it before provider testing; the source overlay has not passed yet.
6. Only after functional readiness, compare the same fixed page with current
   WebKit under matched RAM/viewport/UA/service conditions, with observer-off/on
   controls and reordered repetitions. Measure all child-process PSS/anonymous
   memory, CPU, reclaim, input latency and renderer status. Then the separately
   admitted real-provider phase can test viability without submitting accounts.
   An error/CAPTCHA/policy page is not successful sign-in. Do not spoof around
   provider restrictions.
7. Export small logs, reviewed frames, original results and hashes; then retire
   owned SDK/output/profile/guest disks when no longer needed. Source/notices
   custody required for a delivered build is a separate protected retention set.

A full engine build is the fallback if the upstream ABI cannot fit. Chromium's
official Linux instructions describe at least100GB free disk, substantial RAM,
Clang/libc++ and the depot_tools/GN toolchain; it would need a separate package,
cross-compilation and cache plan, not an unbounded experiment launched here.
[Chromium build requirements](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md).

## FOSS and contribution disposition

CEF and Chromium's own top-level licenses are BSD-style, but bundled components
retain their individual licenses. Any adopted distribution needs the exact
source/notice manifest and redistribution files through #528; CEF's top-level
license alone is insufficient. Preserve the engine's notices, locales, Unicode
and V8 data and required runtime dependencies. Do not substitute proprietary
Chrome or add Widevine/proprietary codecs for this sign-in task. The prebuilt
binary's complete payload/configuration has not been inspected; strict FOSS
acceptance and provenance therefore remain a prerequisite to adoption.
[CEF licensing and update guidance](https://github.com/chromiumembedded/cef/blob/14c5a089e8452874cb1a556dc3fde26ed2d87723/README.md),
[redistribution components](https://github.com/chromiumembedded/cef/blob/14c5a089e8452874cb1a556dc3fde26ed2d87723/tools/distrib/linux/README.redistrib.txt).

Disposition: **proceed to the bounded VM feasibility proposal when admitted;
do not select a production engine yet.** There is a maintained native Wayland
route and a reusable source probe, with concrete sandbox/ABI/integration gates.
No measured performance claim or H700-memory saving exists. A new Chromium bug
or reusable fix should be recorded for CEF/Chromium and #585; no upstream defect
or submission has been asserted by this source-only preparation.

## Static verification performed

`static-checks.json` records three Python AST parses, JavaScript parse exit0,
zero-fuzz patch dry-run and application exits0 against four exact pinned source
files, and every resulting source hash. The preparer CLI, C++ compilation and
all browser/VM/device runtime remain UNRUN. No source text substitution is a
claim of working navigation, sandbox, keyboard, graphics or memory behavior.
