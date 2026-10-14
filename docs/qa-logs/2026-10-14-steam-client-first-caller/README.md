# Steam full-caller and profile-path cases — #582

Current status: corrected full caller, fresh/existing profile-parent alias,
detached child, census-failure and real transport-timeout cases pass. Broader
recovery/compatibility and native/installed-image qualification remain.
Historical first failures and earlier next-work notes are retained below;
the October14 targeted-results table supersedes those next-work notes.

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

## Existing profile-parent alias — PASS, 14:48 UTC

Fresh no-network VM attempt04-existing-profile passes with the unchanged
03e130 candidate: complete caller, trace, fixture and lifecycle all exit 0.
The fixture took 15.01 seconds and preserved all 22 protected entries, including
the existing client/channel, resolved profile, lexical decoy and unrelated data.
The synthetic client exec was denied; native Steam readiness is still unproved.
Original guard results, manifests and output are retained in the attempt packet.
Every host/QEMU/child owner exited, the admission is consumed, and 2,277,924,864
allocated disposable bytes were retired. No run from this owner remains active.
The remaining targeted cases are detached child, census failure and transport
timeout, followed by the broader recovery and native/installed qualification.

## October14 remaining targeted caller checks

All four targeted cases passed on separate fresh no-network VM20 guests with the unchanged03e130 installer/fixture. These are synthetic caller/transaction proofs, not native Steam execution or complete installed-image qualification.

| Packet | Original observations | Scope/result |
| --- | --- | --- |
| attempt04-existing-profile | 15.010742164s; caller0;22 protected entries unchanged | Existing profile and parent alias preserved; native client denied |
| attempt05-detached-child | 15.365351534s; caller0;13 entries unchanged; child45 exit-9 | Product cleanup ends detached descriptor holder; no harness rescue |
| attempt06-admission-refusal | launcher/runner125 before command; no command.pid, VM or registry reservation | Checkpoint edit raced source fingerprint; retained original refusal, never admitted |
| attempt06b-census-error | 24.818389396s; intended callers1,1;13 entries unchanged | Unknown-live state stays held; second attempt refuses before install; independent fixture actor releases child77, not product quiescence |
| attempt07-transport-timeout | 196.987076506s; intended caller1;13 entries unchanged; child exit-9 | Real180s product timeout, original230s trace/240s fixture; no installed state or harness rescue |

Each admitted run has original fixture/namespace/lifecycle/watcher/launcher0, exported original traces, actual host/process exits, consumed admission and retirement receipt. The negative installer exits remain negative. Total four disposable VM allocations retired:9,112,907,776bytes. Broader19-case recovery/compatibility matrix and native/installed-image proof remain; the6bebc365 aggregate proposal is HELD/UNRUN and was not used. Prior a057 failure remains unchanged.
