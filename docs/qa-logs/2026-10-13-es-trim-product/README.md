# Actual ES allocator candidate — #570

Candidate `f7b71db0a70e1c48627f70847ecbc95bb1cb4a43` in the separate ES repo is
compiled from accepted `c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`. The exact
seven-line proposal was already retained in the earlier memory-state packet.
The distribution pin is unchanged; this is source/binary and component proof.

## What passed

The actual cached target compiler passes syntax, object compilation, linking and
stripping. The linked cloud-sign-in function calls frontend teardown, `malloc_trim`,
the normal wait, then frontend restore, in that order. Only the expected source,
object/dependency outputs and binary changed. All frozen baseline bytes remain
unchanged; no full OS cache was copied. The stripped binary is11,798,768bytes,
SHA256 `5c08a1713e9af08054e6ec01480894987f48e9335b44fbf8e02462109438ca6f`.

Compile02 took10.19seconds including manifest rechecks. Container peak memory was
749,096,960bytes with zero OOM events;11host samples observed zero swap-in/out.
This is one translation unit and relink, not a full-image resource forecast.
The host's full swap was reclaimed by the installed guarded helper before work.
Both compiler attempts and the guest used fresh #493 admissions; original results
and actual process exits were consumed before reservations were released.

A fresh standard-profile640×480 VM, launched with `--gl auto`, ran the exact candidate binary (verified
through `/proc/PID/exe`) over accepted VM20. The synthetic authorization page is
local; no account, hosted authentication or personal cloud was used. Native mode
loaded the page, accepted a QEMU keyboard character with its on-screen keyboard
visible, and returned. Phone mode used the actual remote keyboard page in host
Chromium, applying16characters on each of two pages across navigation, then
returned to the normal waiting dialog. Both preserve ES PID2679 and the same
boot. The provider-start error and normal Back route were also reviewed; this
error arose before browser launch and does not qualify a browser-open failure.
Final broker status is idle, browser absent and remote list empty.

The native input is virtual-keyboard input, not physical gamepad selection proof.
The waiting/cancel frame retains a temporary QR privately. The13reviewed frames
are indexed by source and binary;11are public. No screen text, flow or baseline
mask changed. The phone status ribbon is still the current design (#571 open).

## Original failures and scope

Compile01 failed1 because ccache attempted a write against the deliberately
read-only toolchain mount. Compile02 disables ccache and verifies the same copy.
The original failed source/result stays. A non-existing observation directory
caused native-owner to refuse2 before running; fresh native02 passed. An initial
provision submission lacked cwd/tools/watch-build and was refused before launch.

Provision's original readiness check incorrectly matched 'active' in 'inactive'
for a nonexistent autostart.service alias. Its alias claim is invalidated. A
strict follow-up refused; corrected readback proves the actual
rocknix-autostart.service ran successfully in this boot and ES was idle. The
initial synthetic authorize handler omitted the HEAD/302 provider redirect;
its failure was cancelled, then the already qualified redirect/page fixtures
were used. Early 'keyboard-choice' captures were still startup overlays and are
not included as completed-choice evidence. These are fixture corrections, not
shipped fixes or rewritten results.

All15watched owners are consumed:13return0, original compile1 and submission2
remain. QEMU, fixture server, phone tunnel and browser automation owners exited.
Disposable guest disk/UEFI/keys and the isolated compile copy are removed:
3,172,134,912allocated file bytes retired. The11.8MB candidate binary alone is
held for the immediately queued #570 qualification. Cleanup here was explicit;
#493 automatic retirement/reconciliation remains open.

Can this be done on the VM? Yes; planned in #570 before launch. The VM proves
these input/return paths, not a physical memory-pressure cure. Still owed before
pin promotion: constrained-memory comparison on the actual binary, repeated
lifecycle and remaining success/failure cases, wider flow qualification and
source-bound evidence; designated bench corroboration remains separate. The runtime renderer string and live QEMU argv were not separately retained;
`--gl auto` records requested policy, not independently verified GPU use. No
1280×800/French, authenticated sign-in, full image, independent audit, device
fix or RC readiness is claimed here. Historical diagnostic reclaim75.73–77.64MiB
is not re-labelled as this binary's measured saving.

Fixture sources are archived evidence, with original absolute paths and completed
owners. Do not replay them. Start fresh owners/ports/disks and current admissions.
