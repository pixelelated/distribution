# Steam first full-caller case — #582

Can this be done on the VM? Yes. One fresh accepted VM20 with no network device,
8GiB RAM and executable3GiB scratch tmpfs ran the synthetic fresh-client case.
Real owner devices, accounts, cloud data and downloaded payload execution were
excluded. The exact synthetic AArch64 client exec was denied by the ptrace
boundary. Sourcea057a2a7e94c372642fd66ff9795125487f1fa75 is not promoted.

**Original FAIL1.** The exec boundary reached its deadline after89.6 seconds,
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
