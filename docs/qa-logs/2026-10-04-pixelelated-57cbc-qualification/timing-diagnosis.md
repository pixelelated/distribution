# Current candidate timing diagnosis — #429 / fixture #430

Can this be done on the VM? **Yes.** All work uses private COW guests on exact
candidate57cbc/bundled4007387. Frozen source and completed owners are immutable.
No physical device or personal cloud is involved.

runtime06/tool38117 failed1 after14 inherited-archive checks. Its five
alternating samples/layout gave medians286ms legacy/250ms current:36ms exceeds
the unchanged30ms gate. Every transferred save hash matched and migration
journal delta was0. This remains a valid failed qualification. Identity was
not reached; backing and actual process cleanup passed.

Guarded idle host reclaim/tool41496 exited0 (8191MiB swap free,36565MiB RAM
available). This establishes resource preparation, not proof that swap caused
the original timing difference.

Diagnostic01/tool36748 failed1 before its first batch completed: a second
consecutive current-folder write returned0/152ms but did not transfer its new
same-size bytes. The live hash4ff90268… differed from previous/remote c8629db9….
A fixed1.15 host-second pause did not prove that the guest write timestamp
exceeded WebDAV's host upload time and comparison window. Its samples are
not acceptance. Actual owner processes exited and the original disk is kept.

A separate COW inspection/tool13481 exited0. The prior persisted guest save
mtime was1135ms behind its remote upload; live guest clock was about703ms
behind the host observation. The last dirty write had not persisted at abrupt
VM stop: the rebooted disk contained the *previous* c8629db9… hash, explicitly
not the original live failing hash. This readback cannot establish the lost
last live timestamp or prove a cloud data-loss defect.

#430's fresh helper waits **outside the measurement** until the guest's actual
clock is beyond the previous remote upload+2s, writes normally, then verifies
the new mtime exceeds previous upload+1s. It never sets clocks or future
mtimes. Same-time, within-window and exact-boundary controls refuse; a later
time passes. Every sample records timestamps, return code and both hashes
before asserting. A failed command's sanitized outcome is retained before
teardown. Production comparison, command and30ms threshold are unchanged.

Diagnostic02/tool43491 completed all three predeclared batches:

| Batch | Legacy median | Current median | Difference | Migration journal delta |
| --- | ---: | ---: | ---: | ---: |
| 1 |276ms|253ms|23ms|0|
| 2 |275ms|246ms|29ms|0|
| 3 |278ms|252ms|26ms|0|

All30 measured and6 warmup transfers matched their real save bytes; every
new timestamp predicate passed. The independent parent directory listing
measured27/24/25/24/23/24/23/24/24/23ms (median24ms). The source retains the
required per-run missing-folder guard and explicit directory slash; it does
not cache presence or perform migration preparation during an exit sync.

Diagnostic02 still exited1: its subsequent optional trace parser saw no
expected prefixes. Trace-only owner96170 resolved collection without repeating
the three timing batches. Actual guest probe proves root Bash ignored PS4 from
the environment; setting it inside the diagnostic shell produces990 parsed
legacy rows and988 current rows. Actual tool/result channels0, product and
source hashes unchanged, backing and cleanup pass01:00:06. Raw expanded
traces remain private; safe summaries omit command arguments. Instrumented
trace durations are not acceptance measurements.

The original36ms result has not been relabeled. No single host condition is
proved to have caused it. Fresh runtime07 is justified by the verified fixture
correction, all three predeclared diagnostics and successful trace collection;
it must independently pass the original30ms gate, archive checks and identity.
runtime07 actual29491/allrc0 now passes:14 archive assertions,4 timing
assertions and13 identity/Tools-consumer assertions. Medians272/244ms give
28ms against unchanged30ms, all12 real transfers match and all timestamp
boundaries pass, no migration-journal activity. Frozen source/bundle and
actual-upgrade backing reverify. Actual01:02:20 runner892481/watcher892482/
command892511/guest892922 and owned backend absent. Receipt runtime-07/.
The original failure remains retained; #429/#430 await publication/closure
with these scoped results. Only unstarted proxy05 was rebound to runtime07;
its former launcher/seal remain. No product bytes changed in this diagnosis.

Evidence directories here: `runtime-06`, `timing-diagnostic-01`,
`timing-inspect-01`, `timing-diagnostic-02`, `timing-trace-01`.
