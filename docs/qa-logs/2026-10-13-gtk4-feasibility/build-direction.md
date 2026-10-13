**Isolated source/build direction; not an executed build plan**

Use the pinned builder/toolchain and an independently owned diagnostic build
directory/staging prefix. The accepted cache supplies read-only reference
material only. Never run configure/install in it, repair its absolute symlinks,
or hardlink files that will be mutated. The coordinator must allocate resources
and the canonical container path; #493 precedes a full cache copy or full build.
The `preflight.py` census is safe to run without either operation.

Initial versions: WebKit2.54.1, GTK4.24.1, Graphene1.10.8. Keep the WebKit tarball
and both existing patches byte-identical to the GTK3 control. The first adds
`EventLoop.h` to DocumentLoader; the second adds the graphics include directory
for the GStreamer-GL/non-WebGL option set. No rationale exists here to remove
either. New package recipes remain work for the allocated build experiment;
this packet supplies exact upstream option names, not an unqualified package.

| Step | Required source direction |
| --- | --- |
| Graphene | Add a separate recipe with target GLib/GObject, Meson host tooling, GObject types enabled. Options: `-Dgobject_types=true -Dintrospection=disabled -Dgtk_doc=false -Dtests=false -Dinstalled_tests=false`. Keep architecture-appropriate SIMD defaults; do not transplant x86 flags to H700. |
| GTK4 | Separate recipe; use the dependency table in README and `--wrap-mode=nofallback` to prevent hidden subproject downloads. Options for the first Wayland/Cairo/GL spike: `-Dx11-backend=false -Dwayland-backend=true -Dbroadway-backend=false -Dwin32-backend=false -Dmacos-backend=false -Dandroid-backend=false -Dvulkan=disabled -Dmedia-gstreamer=disabled -Dprint-cups=disabled -Dprint-cpdb=disabled -Dcloudproviders=disabled -Dtracker=disabled -Dcolord=disabled -Daccesskit=disabled -Dsysprof=disabled -Dintrospection=disabled -Ddocumentation=false -Dman-pages=false -Dbuild-demos=false -Dbuild-testsuite=false -Dbuild-examples=false -Dbuild-tests=false`. |
| Sandbox dependencies | Stage actual bwrap and xdg-dbus-proxy executables, libseccomp and their ELF closure. Their addon recipes are not evidence of OS runtime installation. Declare runtime dependencies explicitly; use suitable scoped overrides instead of globally changing unrelated addon behavior. |
| WebKit6 | Copy the production option set into a distinct diagnostic recipe/name and build directory; switch `USE_GTK4=ON`, depend on GTK4, and link the6.0 API. Keep WaylandON/X11OFF, libsoup3, WebGL/media-stream/WebRTCOFF, video and GStreamer-GLON, profilerOFF, and the same compiler/release flags. |
| Sandbox-enabled diagnostic | Set `ENABLE_BUBBLEWRAP_SANDBOX=ON`; set `BWRAP_EXECUTABLE` and `DBUS_PROXY_EXECUTABLE` to absolute **guest** paths. Cross configure cannot discover them. A private `/run/pixgtk4` deployment, for example, must consistently configure `/run/pixgtk4/bin/bwrap` and `/run/pixgtk4/bin/xdg-dbus-proxy`, library/libexec/data paths, and its launcher environment. Do not use host paths. |
| Payload | Retain CMakeCache/Meson introspection, pkgcheck output for every new/changed recipe, binary/library hashes, ELF NEEDED/interpreter closure, schemas/fonts/loaders, WebKit subprocess/resources/injected bundle, and GStreamer scanner/plugin/controller closure. Test a fresh registry. A library that links is not an installed sign-in stack. |

Disabling GTK's own media widget backend does not disable WebKit video or remove
its GStreamer requirements. It is an explicitly narrower diagnostic GTK build,
not a general-purpose distro GTK recommendation. Vulkan is deliberately absent
from that first build; a Vulkan result must be marked unsupported until an
otherwise matched GTK build enables it and supplies a working native `glslc`,
target loader, and driver. Do not count `ngl` and `gl` as different4.24 renderers.

Source-imposed and chosen differences must appear separately in the result:

| Difference from accepted GTK3 | Reason / control |
| --- | --- |
| `USE_GTK4=ON`, `ENABLE_2022_GLIB_API=ON`, API4.1→6.0 | Unavoidable toolkit/API build switch |
| Cross-site process swapping enabled | Unavoidable WebKit6 context behavior; measure same-engine GTK3 with `process-swap-on-cross-site-navigation-enabled=TRUE` as an additional control |
| Network-session ownership/global network-process model | Unavoidable new API; do not fall back to the persistent default session |
| SandboxOFF→ON, bwrap/proxy/seccomp payload | Chosen to realize WebKit6's supported sandbox contract; not enforced by a GTK4 CMake fatal error. Keep an accepted GTK3 baseline and a separate sandboxON/process-swapON GTK3 control, so overhead is not attributed entirely to GTK4 |
| GTK rendering, theme/text metrics, widget layout | Unavoidable toolkit change; match actual CSS width/height/DPR, UA and keyboard policy and record differences |
| WebKit's ATK branch removed | GTK4 API branch; preserve required ATSPI closure |
| GSK renderer selection | Only meaningful on GTK4; observe the realized renderer and driver |

The aligned GTK3 control must also call
`webkit_web_context_set_sandbox_enabled(context, TRUE)` before loading a page;
building sandbox support alone does not enable it for this current application.
Use the GTK3 process-swap construct property when creating its ephemeral
context. The original accepted control stays separately identified.

Keep `WEBKIT_DISABLE_DMABUF_RENDERER=1` in the initial software-path comparison,
then allocate paired0/1 controls separately if needed. The exact2.54.1
`AcceleratedBackingStore.cpp` tests this variable; selecting a GSK GL renderer
does not itself demonstrate a WebKit hardware-accelerated page. Preserve
WebKit/GTK settings, UA, CSS dimensions/DPR, source/observer, content paths,
fresh-session policy, process headroom, and service state. Do not turn on a
sampling profiler or change WebKit's compositor at the same time. If attribution
needs profiling, give both comparison builds the same profiling configuration
and quantify observer cost separately.

The immediate executable preflight, from this worktree:

```bash
export TMPDIR=/workspace/tmp/pix570-parallel-20261013/tmp
python3 docs/qa-logs/2026-10-13-gtk4-feasibility/preflight.py \
  --sysroot /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/toolchain/x86_64-rocknix-linux-gnu/sysroot \
  --webkit-source /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/build/webkitgtk-2.54.1
```

Expected current exit2: Graphene/GTK4/WebKit6/libseccomp absent, plus the canonical
PNG alias not resolvable at this host path. This script reads metadata only and
does not prove buildability when it exits0. Re-run against the allocated
isolated sysroot after provisioning; do not change the accepted cache to make
the check pass.

The next compilation experiment, **only in that prepared isolated toolchain
environment**, is:

```bash
python3 docs/qa-logs/2026-10-13-gtk4-feasibility/compile-api-smoke.py \
  --cc "$GTK4_EXPERIMENT_CC" \
  --pkg-config "$GTK4_EXPERIMENT_PKG_CONFIG" \
  --output "$GTK4_EXPERIMENT_OUTPUT"
```

Those three paths must be allocated by the coordinator: compiler executable,
pkg-config wrapper selecting only the experiment sysroot, and a new binary path
whose parent already exists. The wrapper must provide correct cross sysroot
and library/include paths. The command refuses another GTK/WebKit version,
refuses an existing output, and **never executes the binary**. The compiler has
a 60-second communication timeout; each pkg-config call has 15 seconds. Each call
starts a private process group. A timeout sends SIGKILL to that group, then
allows five seconds to reap the direct child. A cleanup failure is an error
requiring coordinator teardown, not a successful resource release. See the
[correction and remaining containment limits](timeout-cleanup-correction.md).
The original `da0ecd8` host invocation is retained in `compile-api-smoke.log`:
exit2 before compiler invocation, under the original script hash in
`checks.json`. The corrected helper has not run. No fake headers or native host
libraries were substituted. Executing the resulting API program later needs a
disposable VM display and a coordinator lease; it checks ephemeral related-view
construction only and loads no page.

Stop this spike if a second independent dependency/toolchain expansion makes
it exceed its allocation. Return the first concrete configure/compiler failure
with the exact log; do not silently widen into a full OS rebuild. Production
adoption remains conditional on the complete keyboard port and VM acceptance.
