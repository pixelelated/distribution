**GTK4/WebKit6 feasibility, October 13, 2026 — #576 / #570**

**Decision: defer a production port; proceed only with a separately allocated
dependency/API and keyboard spike.** GTK4 is a viable upstream build direction,
but a functional replacement is not a bounded container/API rename. The native
on-screen keyboard has no direct public GTK4 event-construction equivalent, and
the available environment cannot compile a GTK4/WebKit6 program. There is no
GTK4 memory, responsiveness, recovery, or sign-in success measurement in this
packet. No production recipe, pin, broker, or offline-award behavior changed.

Evidence level: exact-source inspection, upstream release/API verification,
read-only target development-metadata inventory, and observed prerequisite
failure. **No compiler ran, binary was produced, VM was booted, or browser was
launched.** The included C file is an API construction fixture, not a reduced
sign-in application or an implemented port. Its execution belongs to the
coordinator's future disposable VM allocation.

The whole [owning issue](issue.json), including its VM-first answer, and its
[empty comments readback](issue-comments.json) were read. The source base is
`4a1274ab806bf583c78646d01fb82bb6fb8f9ef7`, identical to `next` at entry; the
instruction-file comparison was clean. Canonical every-session rules were
opened, together with packaging, handheld evidence, VM guidance, and device
policy. `tools/archaeology --no-gh --since 2026-09-01 GTK4` found no register
decision adopting GTK4. The supplied assignment and October13 parallel-lane
handoff override the older checkpoint's commands and delivery owners.

The read-only coordinator packets now describe **22 completed and retired
trials**. UA changes and CSS-width screening did not establish a memory fix;
all ran WebKit2.54.1/GTK3. The linked source-bound handoff assigns this worker
source preparation only. [Input hashes](inputs.json) bind those packets, the
handoff, current sign-in/broker source, recipes, patches, and the cached WebKit
tarball. The tarball's SHA256 was read and matches the production recipe:
`ea0bbb02dbdbc596874a4e7ad35b66645b3e0a232bd0e4081de5ed92eb0a397d`.

**What the exact sources establish**

WebKit2.54.1's `Source/cmake/OptionsGTK.cmake` selects GTK >=4.6.0 when
`USE_GTK4=ON`, `webkitgtk-6.0`, and `ENABLE_2022_GLIB_API=ON`. It still uses
libsoup3 and the same WebKit/JavaScriptCore release. WebKit6 is an API name, not
engine version6. Common requirements include GLib2.70, Cairo1.16, HarfBuzz2.7.4
with ICU, ICU70.1, epoxy1.5.4, libxml2 2.9.13, and GStreamer1.18.4 with the
required components. Keep video, GL, and MPEG-TS requirements and the corrected
#572 plugin/scanner/controller payload. The current recipe disables sampling
profiling; changing that would introduce another experimental variable.
Exact source locations, full-file hashes, and excerpts are in
[WebKit evidence](research/webkit-evidence.json).

The latest stable GTK release observed on October13 is **4.24.1**, released
October1. Its tag resolves to `2ea935e3ec680fb122f245b28e18c3495df8c344`.
Graphene's latest published GitHub release observed is **1.10.8**. GTK4.24.1
requires Graphene >=1.10.0, including its GObject library. Its GLib requirement
is literally >=2.89.3 even though its API version macros name2.90; the cached
GLib headers define `GLIB_VERSION_2_90`. Do not substitute a guessed GLib2.90
minimum. [GTK release index](https://download.gnome.org/sources/gtk/4.24/),
[exact GTK source](https://github.com/GNOME/gtk/blob/2ea935e3ec680fb122f245b28e18c3495df8c344/meson.build),
[Graphene release](https://github.com/ebassi/graphene/releases/tag/1.10.8).

| GTK4.24.1 prerequisite | Current effective target metadata | Result |
| --- | --- | --- |
| GLib >=2.89.3; Pango/PangoFT2/PangoCairo >=1.58 | 2.89.3; 1.58.2 | Present |
| Cairo/Cairo-GObject >=1.18.2 | 1.18.4 | Present |
| HarfBuzz and subset >=8.4; FriBidi >=1.0.6 | 14.3.0; 1.0.16 | Present |
| GdkPixbuf >=2.30; epoxy >=1.4 | 2.42.10; 1.5.10 | Present |
| Wayland >=1.24; protocols >=1.48; xkbcommon >=0.2 | 1.26.0; 1.49; 1.8.0 | Present |
| JPEG, TIFF, PNG; libdrm headers | JPEG/TIFF/libdrm present; libpng16.pc present | PNG alias needs canonical build mount |
| Graphene-GObject >=1.10 | No recipe or target module | Add isolated dependency |
| GTK4 >=4.6 for WebKit; chosen experiment4.24.1 | No GTK4 recipe or module | Add isolated dependency |
| WebKitGTK6 exact2.54.1 | Only GTK3/API4.1 built | Separate WebKit build required |
| Meson >=1.8 for GTK | Recipe1.11.2 | Recipe exists; native tool execution untested |
| Optional GTK GStreamer media >=1.28 | play/gl metadata1.29.2 | Available metadata; diagnostic GTK media can be disabled |
| Optional Vulkan >=1.3 and native glslc | Target Vulkan1.4.347; target shaderc recipe2025.3 | Native glslc still needs qualification |

These are metadata checks, not ELF/link/install closure. Project overrides win:
generic GdkPixbuf2.44.7, xkbcommon1.13.2, libdrm2.4.134, and at-spi2-core2.61.1
are not the effective target selections. Effective values include
GdkPixbuf2.42.10, xkbcommon1.8.0, libdrm2.4.133, at-spi2-core2.45.1, and
at-spi2-atk2.38.0. WebKit's existing ATSPI probe asks for2.5.3; GTK4 stops
using WebKit's GTK3 ATK branch. There is no libadwaita requirement here.
The [recipe inventory](package-inventory.json) binds generic and override files;
[installed-reference receipt](installed-reference.json) binds the baseline
browser and absent sandbox payload in the accepted image tree.

The accepted cache remains immutable. Its `libpng.pc` is an absolute symlink
into the historical `m7-pixelelated` container path; its sibling `libpng16.pc`
exists. This is a mount/path constraint, not evidence that PNG must be rebuilt.
The preflight reports `BROKEN_SYMLINK` rather than inventing a working host
configuration or repairing the cache. [Inventory](preflight.json) retains the
actual module versions, hashes, and selected existing WebKit CMake flags.

**Sandbox and source-port limits**

The WebKit6 API mandates sandbox enablement and cross-site process swapping.
The current GTK3 recipe builds `ENABLE_BUBBLEWRAP_SANDBOX=OFF`; its application
does not enable the optional process-swap property. The exact CMake checks do
**not** forbid a GTK4 build with sandbox support compiled out. In that case,
the launcher has an ordinary subprocess fallback. Therefore neither a WebKit6
API name nor a successful GTK4 build proves sandbox isolation.

A supported sandbox experiment should add `libseccomp`, `bubblewrap`, and
`xdg-dbus-proxy`, enable the WebKit sandbox build, set the two absolute target
executable paths, and verify isolation inside the guest. Recipes already exist
for versions2.6.1,0.11.2,0.1.7 respectively; the two executable recipes carry
`PKG_BUILD_FLAGS="-sysroot"` for their addon use. They need deliberate OS
staging/dependency treatment. The accepted image has neither executable nor
libseccomp; the sysroot lacks `libseccomp.pc`. GENERIC_X64's kernel source enables
user namespaces and seccomp, which is necessary source evidence, not a runtime
sandbox pass. Do not bypass a failed sandbox with a disable environment variable.

[Port map](port-map.md) binds keyboard injection, drawing/layout, lifecycle,
session construction, related popup state, and navigation/callback handling to
the current C source. It explains why a fake DOM keyboard or private GDK symbol
would not preserve functionality. No such substitute is supplied.

**Next executable experiment and acceptance**

[Build direction](build-direction.md) specifies the isolated dependencies,
same-engine controls, flag deltas, and compile command. The first executable
step is the included preflight against the coordinator's chosen isolated
sysroot; it currently exits2 with named missing prerequisites. Once the exact
pair is provisioned, `compile-api-smoke.py` compiles only the small construction
fixture and never runs it. The original script at commit
`da0ecd80473037708dab38e82ea458708cc8c1b6` exited2 before invoking a compiler.
[Checks](checks.json) retain the original script hashes, both outcomes, and the
missing-input negative control (exit1). The subsequent
[timeout-cleanup correction](timeout-cleanup-correction.md) has static review
only; those historical receipts are not execution evidence for the new source.
No pkgcheck/build/install PASS is claimed because no package recipe was edited
and no package build was attempted.

The coordinator must record a precise VM plan and allocate runtime exclusively
before executing even the API fixture. #493 still precedes any full cache copy
or full build. The next functional experiment must settle native keyboard
delivery and related-view session sharing before provider benchmarking.
[VM acceptance](vm-acceptance.md) names the required artifacts and controls.
No immediate dependency on an owner account or physical device exists.

GSK settings do not affect the current GTK3 binary. In GTK4.24.1, `cairo` and
`gl` are distinct candidates; `opengl` is a GL alias and `ngl` selects that same
current GL implementation with a warning. Vulkan requires a build with Vulkan
support and a usable driver. A requested renderer can fall back, so record the
realized renderer type. GSK Cairo does not change WebKit2.54's Skia page painter
into Cairo. Keep WebKit DMA-BUF/acceleration and GTK GSK selection separate.
This is grounded in the
[exact renderer source](https://github.com/GNOME/gtk/blob/2ea935e3ec680fb122f245b28e18c3495df8c344/gsk/gskrenderer.c)
and retained [upstream excerpts](research/upstream-evidence.json).

The dated upstream check found no incident-specific GTK4 fix to adopt.
WebKit's [2.54 announcement](https://www.webkitgtk.org/2026/09/16/webkitgtk-2.54-highlights.html)
describes Skia/compositing changes shared with WPE; its benchmark is not a
GTK3-versus-GTK4 memory comparison. [2.54.1 release notes](https://www.webkitgtk.org/2026/10/02/webkitgtk2.54.1-released.html)
describe rendering/input fixes and an Amazon Luna UA quirk, not a confirmed
Dropbox GTK4 memory fix. GTK4.24.1's release notes include OSK/input and graphics
fixes, not a measured benefit for this application. WebKit
[268477](https://bugs.webkit.org/show_bug.cgi?id=268477) remains a reopened,
2024 memory-pressure report, with no matching fixed version established here.
Its symptom alone does not diagnose #570. The browser fetch of306430 failed;
this packet makes no new claim about that report. Search coverage is limited,
not proof that upstream has no relevant defect.

No background job remains from this assignment. All subprocess calls completed
synchronously. Coordinator owns GitHub/status, shared work-log/register updates,
integration, and any later build or runtime. This packet supplies a bounded
feasibility result; it does not close #576's functional or measurement criteria.
