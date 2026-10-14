# Steam full-caller and profile-path cases — #582

Current status: the corrected full caller and fresh profile-parent alias
cases pass. Existing-profile, child cleanup, failure recovery, and native
installation qualification remain. The first failed run is retained below.

## Original attempt

Can this be done on the VM? Yes. One fresh accepted VM20 with no network device,
8GiB RAM and executable3GiB scratch tmpfs ran the synthetic fresh-client case.
Real owner devices, accounts, cloud data and downloaded payload execution were
excluded. The exact synthetic AArch64 client exec was denied by the ptrace
boundary. Sourcea057a2a7e94c372642fd66ff9795125487f1fa75 is not promoted.

**Original FAIL1.** The exec boundary reached its80.01-second deadline (outer fixture89.62seconds),
while the unchanged full caller was in Proton-CachyOS setup. It did not return
an original installer exit. No setup or native-readiness PASS is claimed.
The per-syscall WNOHANG/1ms polling is a source-level overhead lead, not yet a
measured cause. The fixture, namespace and original process traces are retained
losslessly in attempt01/guest/steam/fixture-records.tar.gz.

Outer fixture supervision reported quiescent with no descendants or rescue.
The lifecycle finally flushed/unmounted output and stopped its owned QEMU;
all actual host owner/runner/command/watcher/QEMU PIDs were absent. Original
runner/command/lifecycle/launcher1 and monitor0 remain. Admission was consumed
failed-investigated. After export verification, the disposable VM/media/UEFI
directory was retired, releasing2,278,125,568 allocated bytes. No history disk.

Independent source review8aec3a found two actionable client-helper defects:
optional proc task/children cleanup is unavailable on the accepted kernel;
lexical normalization can resolve a nested profile symlink/parent to the wrong
support directory. See ../2026-10-14-steam-client-source-review/README.md.
The source lane is repairing those and the bounded fixture before a new
allocation. No retry, provider request, native Steam success or product pin move.

## Corrected caller and fresh profile alias — PASS within scope

Candidate03e130e4b3c244337f2e6d782b392a2c444c28e7 repairs the two findings and
uses alarm-bounded blocking trace waits. Independent review485d6d83c7 finds
both addressed in source and no additional concrete defect in that delta.
Neither old product/fixture source nor original attempt01 is relabelled.

Fresh no-NIC VM attempt02 passes the complete synthetic caller: original caller,
trace driver, fixture, lifecycle, launcher/runner0,15.47seconds outer/12.25 trace.
The busy control records8,009 syscall stops; the deliberately idle control hits
its2.01-second deadline with driver1/caller null, bounded cleanup and no survivor.
That expected negative remains1. The full caller records95,214 syscall stops,
zero main-loop polling sleeps, and one denied synthetic-client exec. This proves
the bounded fixture path, not native Steam readiness or a quantified product
speedup relative to the incomplete old run.

Separate fresh VM attempt03-profile-alias passes the concrete symlink/parent
case: actual resolved support receives aliases/registry, lexical decoy and
unrelated synthetic data remain unchanged. Original caller/trace/fixture/VM
owners0;15.94seconds total. Full exact manifests and guard receipts are in each
guest/steam/fixture-records.tar.gz. Neither case runs a provider or real payload.

Both completed allocations are consumed, all host/QEMU/child owners absent,
output unmounted and disks/media/UEFI retired. Together with attempt01,
6,834,425,856 allocated disposable bytes are removed. No history disks retained.
Remaining independent allocations: existing-profile-parent-alias,
detached-transfer-child, proc-census-error, then the real180s transport-timeout
case, plus the broader existing/recovery matrix and native/installed proof.
No source pin, product integration, firmware or RC designation follows here.
