# Runtime browser controls for #616

Diagnostic source for the October 15 frozen app, SHA256
`39af3e041d9871c4fb636cff71934ddf3ea13c690002e77af5ea6d82d8fff4f8`,
product commit `077197e6cd3ea31f33b28aaf3882a694b3423b53`.
No product file, package pin, OS image or personal configuration changes here.
The parent coordinator owns compilation admission, VM runs and device staging.

Can this be done on the VM? Yes. First compile and validate on GENERIC_X64;
real H700 GPU/ARM behavior is a later physical corroboration. This packet does
not authorize a device launch, bind mount or service operation.

## Per-launch controls

| Environment | Values | Default |
| --- | --- | --- |
| `QA616_UA` | `default`, `desktop`, `custom` | `default` |
| `QA616_OBSERVER` | `off`, `on` | `off` |
| `QA616_CUSTOM_UA` | printable ASCII, 1–512 bytes; only with `custom` | absent |

Unknown `QA616_` variables, empty/unknown enums, orphan custom values, control
characters, excessive lengths and incompatible engine identities refuse with
**exit 78 before GTK initialization**. The additional `--qa616-check` argument
validates configuration, prints the selected mode/observer state, and exits 0
without GTK, a WebView, network activity or an observer. It does not prove that
the selected UA is applied; the later local HTTP/DOM control must prove that.

`default` leaves WebKit's UA setting untouched, including its per-site quirks.
`desktop` derives WebKit's installed compatibility tokens, removes `Mobile`,
and uses `X11; Linux` with the target's actual `uname` architecture. On ARM this
is an ARM desktop identity; it is deliberately not an x86 impersonation. The
explicit UA override can suppress WebKit's normal per-site quirks: record that
limitation in a comparison. `custom` permits a separately reviewed platform
string but requires this engine's `AppleWebKit/605.1.15`, `Version/60.5` and
`Safari/605.1.15` tokens, rejecting Chrome/Chromium/Firefox/Edge claims. Those
are upstream compatibility tokens, **not** WebKitGTK's 2.54.1 release number.
Do not use an override to bypass a provider's embedded-browser restriction.

No zoom, CSS breakpoint, window size, keyboard, popup, host restriction or
ephemeral-context code changes. Popups retain the product's shared settings;
the observer samples the original view only, so popup readiness is unmeasured.
There is no JS-disable switch or resource blocklist in this packet.

The source already calls
`g_setenv("WEBKIT_DISABLE_DMABUF_RENDERER", "1", FALSE)`; a pre-existing value
is respected. This packet does not change that behavior. Renderer experiments
must record the actual stack and keep this variable separate from UA/observer.

## Observation and its limits

Off mode returns before adding any user script, JS evaluation, heartbeat or
diagnostic timer. Both modes emit a single fixed configuration line with an
effective-UA SHA256 and runtime WebKit version; no raw UA is logged. Default
mode's reported settings UA is not proof of the on-wire per-site UA.

On mode adds an isolated top-frame script world, a 250 ms heartbeat, and at
most one outstanding JS evaluation on a 2 s timer. Heartbeat scheduling stops
after six minutes per document; polling stops after six minutes per launch or
180 requests. Browser exit cancels the observer and removes its timer. A hung
request cannot queue additional evaluations. These are observation bounds,
**not a pressure/deadline guard**: the allocation must supply an independent
guard and terminate the browser at its recorded deadline.

Samples have a fixed numeric schema, never page strings, URLs, resource names,
query parameters, cookies, storage or field contents. `-1` means an invalid
or unavailable numeric field. `ready` is 0=loading, 1=interactive, 2=complete.
The probe considers at most 128 top-document text-like inputs. It checks the
clipped rectangle, direct computed style and center-point hit testing. This
does not cover cross-origin frames, shadow DOM, ancestor opacity, the entire
input area, disabled enclosing fieldsets or provider-specific form correctness.
It is a **readiness hint**, not proof of a usable sign-in. Reviewed unobscured
frames and bounded native input remain required. Cookie overlays and provider
policy/error/CAPTCHA outcomes must be recorded separately.

`eval_roundtrip_ms` includes IPC, JavaScript scheduling/execution and callback
delay. It is not input-to-paint latency or a measured JS heap. Heartbeat gaps
similarly do not identify the cause of a stall. The observer's off/on memory,
CPU and response cost remains to be measured. The current package disables
WebKit's sampling profiler; this helper does not enable full JS CPU profiling.

## Prepare, then compile under the parent's allocation

```sh
python3 -I PATH/prepare.py \
  --base REPO/projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c \
  --out OWNED_SCRATCH/prepared
```

The output directory must not exist. A changed base hash or duplicate/missing
insertion anchor refuses before output creation. The preparer writes only a
diagnostic C source and its provenance. Preserve the packet and provenance
hashes before compilation. Do not regenerate an admitted source in place.

Compile this small program against the existing target sysroot inside the
pinned build container, with no network, bounded resources and read-only
toolchain/cache mounts. Substitute the compiler, sysroot and pkg-config
executable from the same target. Preserve any historical absolute sysroot
mount paths the `.pc` files reference. For example, within that allocation:

```sh
export PKG_CONFIG_SYSROOT_DIR="$QA_SYSROOT"
export PKG_CONFIG_LIBDIR="$QA_SYSROOT/usr/lib/pkgconfig:$QA_SYSROOT/usr/share/pkgconfig"
export PKG_CONFIG_PATH=
"$QA_CC" --sysroot="$QA_SYSROOT" -O2 "$QA_SOURCE" -o "$QA_OUTPUT" \
  $("$QA_PKG_CONFIG" --cflags --libs gtk+-3.0 webkit2gtk-4.1) -latomic
```

Use `config-checks.py -- TARGET_LOADER --library-path TARGET_LIBS BINARY`
after compilation to exercise the **actual C parser** under the target loader
and libraries without a display. Twelve cases expect 0 or 78; the runner
exits 1 for any mismatch. This parser exercise does not constitute a WebKit
launch or performance test. Do not label unrun C checks as host PASS.

Once qualified, one temporary helper binary can serve many per-launch UA and
observer comparisons without rebuilding an OS image. The installed broker
uses `/usr/bin/cloud-signin-window` as an absolute path, so a PATH override
alone is insufficient. The coordinator must choose and record temporary
staging, the original hash, readback and restoration before use. No staging
or bind mount is performed by this packet.

## Local controls to run before real providers

Serve `input-control.html` only on the allocated loopback fixture. It has no
external resources, submit action, storage or network request. Fixed query
cases are `clean`, `blocked`, `disabled`, `hidden`, `offscreen` and `stall`.
Clean should provide a hittable text input; the four visibility/input-negative
cases must not. Stall adds a deliberate 400 ms busy loop every 2 s for heartbeat
sensitivity. Start from fresh contexts and keep viewport unchanged.

Inject synthetic text through the normal native input route. The fixture's
two animation frames expose the time from its input handler to a subsequent
animation frame, plus an alternating paint swatch. This is a browser scheduling
proxy; only external input timestamps and actual frame evidence establish
input-to-visible-paint latency. The fixture does not log typed text. Check the
HTTP User-Agent and `navigator.userAgent` separately using this local control;
store only the synthetic expected identity or its hash. Readiness and callback
behavior under navigation/normal exit must also be exercised on the VM.

## Prepared status

`static-checks.json` records exact-source preparation and tampered-base/existing
output refusals, Python AST parsing, and JavaScript syntax checking. Those are
source controls only. Compilation, the actual C parser matrix, WebKit launch,
observer-off proof at runtime, provider comparisons, frame review, and device
staging are **UNRUN by this packet's author**. The coordinator records subsequent
allocated results separately without rewriting this historical statement.
