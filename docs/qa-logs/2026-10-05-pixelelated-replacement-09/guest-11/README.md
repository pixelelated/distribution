# Full cloud qualification after durable submission (#444, #383)

All19 independently reset cases pass249 assertions with zero failures on the
exact replacement09 candidate. Submission497141=0 was only a launch receipt;
actual durable result08:25:35 is0, with inner/outer/wrapper/build results all0.
Host observation eee27c=0 at08:26:26 confirms runner27508, watcher27512,
command27541 and guest28263 absent, no QEMU. Launcher is also finished.
Local cloud endpoint stopped; source and14-member bundle reverified.

All32 selected original frames were directly reviewed, covering all15cases
with UI output. The four protocol cases T17/T19/T23/T26 have no UI frames;
their assertions verify actual file bytes, pointers, markers and refusals.
1708 original artifact hashes are retained;140 selected public files include
only reviewed PNGs. Keys, disks and unreviewed captures remain outside Git.

The checks cover old/current/custom folder discovery, explicit move/keep/
create/defer behavior, three-boot migration, offline recovery, restore-marker
ordering, connection repair, refused scans, backup choices, startup writes,
failed settlement, missing remote configuration, faulted migration/retries,
idempotence/followers and malformed/future layout refusal. Exact source and
candidate were unchanged throughout. This does not substitute for the next
archive/timing/identity, proxy, memory, UI, account or P4 gates.

Original guest10/tool143 interruption stays in guest-10-interrupted/. It was
never relabelled successful and none of its missing result files were filled.
