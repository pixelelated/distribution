# GTK4 build overlay and native-input spike — #576

**Prepared source only. No compiler, package build, container, VM, browser, device,
or input device ran.** This packet advances the October13 inventory into six
concrete recipe candidates and an executable native-input API fixture. It does
not complete #576's build, keyboard, renderer, memory or adoption criteria.

The assigned branch diverges from current `next`; its history is preserved.
Every production input comes from exact `f511766e17fbdb2f3fd5ec61ee8b469a18758273`,
not this stale checkout's product files. Integrate only this packet's commit.
Coordinator owns shared issue/work-log/decision records and build admission.

The owner asked to explore GTK4 and Blink in parallel for potentially larger GPU
performance gains. `performance.md` identifies a real GTK4 texture/damage path in
our pinned WebKit source, while separating it from Skia page painting already
present in GTK3. There is no established H700 performance ranking.

## Delivered pieces

- `overlay/` contains Graphene1.10.8, GTK4.24.1, WebKit2.54.1 GTK4/API6.0,
  and sandbox dependency overrides. Production WebKit patches and all unrelated
  feature flags are preserved. `source-patches/` stores the original patch bytes
  in gzip files so patch-context whitespace is not misread as new source.
  `prepare-overlay.py --output "$GTK4_OWNER/overlay"` materializes recipes and
  hash-verifies/decompresses both patches, without compiling or editing a checkout.
  Source release checksum indexes were checked
  October17; the GTK/Graphene archive bytes were not downloaded/rehashed here.
- `input-spike.c` uses public GTK4 controllers and WebKit6 ephemeral/related-view
  APIs. Its five native-input buttons send an inherited Unix socket request to
  the existing product `RemoteKeyboard` implementation, which emits genuine
  kernel input. It includes only synthetic inline content and refuses external
  navigation. It is a proof fixture, **not a complete cloud-signin-window port**.
- `prepare-input-spike.py` extracts only the exact pinned literal key mappings
  and `RemoteKeyboard` class into an owned source directory, without importing
  the production broker. Its generated helper suppresses log content.
- `run-input-spike.py` is an **unrun** bounded disposable-QEMU-guest driver. It
  requires a compiled binary's hash, inherited local socket, uinput and a display.
  It may only run under the coordinator's independent VM/pressure supervisor.
  It never imports personal configuration, starts an OAuth listener, or submits
  account data. It does not prove descendant/cgroup cleanup by itself.
- `keyboard-contract.md` defines how distinct pad-control commands avoid the
  Return/Backspace feedback loop and what still needs production integration.
- `sources.json`, `inputs.json`, `checks.json` and `SHA256SUMS` bind evidence.

Can this be done on the VM? **Yes**, as recorded in #576: compilation, synthetic
native/phone input, popup/session/callback/lifecycle, and comparative resource
work belong there. H700 Panfrost/DRAM observations follow portable success and
need their named physical allocation. Nothing here requires owner credentials.

## First bounded command

Source preparation only, under a fresh coordinator-owned parent:

```sh
python3 -I docs/qa-logs/2026-10-17-gtk4-spike/prepare-input-spike.py \
  --repo /workspace/repos/rocknix.worktrees/m7-player-setup \
  --output "$GTK4_OWNER/input-source"
```

The parent must already exist; output must not. This writes roughly25KiB of
source/receipt, invokes no compiler, and has no network/service operation.
After source integration, use the coordinator's current `tools/pkgcheck` from
the materialized staging tree containing `projects/` and `packages/`
to reproduce the recipe lint. The packet also provides a bounded repeatable
check: `python3 -I docs/qa-logs/2026-10-17-gtk4-spike/verify.py --repo .`.
It uses and removes its own temporary source/lint directory. `checks.json`
records the exact executed checks.

**Next compiled step requires a separate admission.** First stage this overlay
in a clean dedicated `build/*` checkout based on the bound source; use a new
owned writable sysroot/build root. The accepted build roots stay immutable.
A new name alone is not enough: verify the effective package paths, cache paths,
absolute symlink mount layout, inherited stamps and installed closure before
compiling. Do not copy an entire accepted build tree as a shortcut.

Start with `PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 ./scripts/build graphene`
under the normal watcher and fresh admission. Stop at its first configure/build
failure and retain it. Then GTK4 and the sandbox closure; only after those pass
allocate the separate WebKit6 compile. Do not pretend the full WebKit build fits
inside the source-spike allowance.

Provisional reservation requests, **estimates rather than measured use**:
Graphene1CPU/2GiB RAM/2GiB new disk/10min; GTK4 and sandbox closure2CPU/8GiB/12GiB/
45min; WebKit4CPU/20GiB/100GiB/6h. Shared host interference, source/sysroot staging
and the current cache census must be added by admission. These are ceilings to
revisit from actual logs, not a promise that the package fits. No quota or
allocation has been consumed by this packet.

After exact GTK4.24.1 and webkitgtk-6.0 2.54.1 are present in that isolated sysroot,
compile `input-spike.c` with the allocated target compiler, its matching
pkg-config wrapper, `gtk4 webkitgtk-6.0` flags, and `-latomic`; output must be new.
Capture the original compiler result and ELF dependency closure. A compile
success is not authorization to launch the guest. The earlier October13 wrapper
can be adapted to this source, but its fixed source filename must be changed and
its timeout controls qualified before claiming it guards this fixture.

## Remaining functional gates

Run synthetic native input before provider benchmarking: all printable ASCII,
modifier release, deletion, Tab, Enter, pad controls and phone requests queued
without interleaving; no OSK recursion; trusted DOM events and field values;
close during pending input; popup return and inherited ephemeral session;
repeated clean launch; deliberate denied navigation and callback-secret
suppression in the **full port**, not only this restricted fixture. Record the
actual renderer, driver, native frames and return to ES. The fixture's emission
count is not a DOM-delivery count. Its one-in-flight request and five buttons
are a narrow probe; a usable product requires its complete keyboard/layout,
busy feedback, bounded ordering and broker integration.

Preserve the product host/identity-provider allowlist, localhost callback
handling, phone protocol, page/field/done files, pad exit, ephemeral cleanup,
TLS and loading/finishing presentation. Their October13 port-map remains the
contract. No behavior is dropped to make the benchmark easy. Clean and retained
storage qualification, exact-source UI flow/frames and audit remain required
before promotion. The packet changes no player flow or selected cloud paths.

Current `next` packaging, instruction-files, VM-first, engineering-practices,
worktrees/fork workflow, learning-capture, decision-register,
handheld-evidence and upgrade/install rules were consulted. No shared rules,
tracker, work log, production recipe, source, pin or image was changed here.

Packaging note: the first staged whitespace check identified inherited context
whitespace in WebKit patch0002. Raw patch bytes were not changed; the final
compressed-source/materializer form avoids that check ambiguity. Earlier small
preparation receipts remain private in `/tmp/pix-gtk4-static-prepared-20261017-01`
and `-02`; neither launched any runtime. Final checks below use the materializer.
