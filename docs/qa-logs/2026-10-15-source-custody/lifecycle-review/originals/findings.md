# Final inventory lifecycle review — sealed485b9937

Disposition: two concrete lifecycle corrections are required before allocation. Root independently read and agreed with both findings. This is a finite local source/evidence review, not execution or external audit. No collector, preparer or helper was imported or executed; no cache traversal, network, runtime, registry or shared source mutation occurred.

## P2 — cleanup does not bind the process identity it signals

`templates/run.py:46–54` calls killpg using only child.pid, including after line107 has already waited/reaped the leader. Once the original group becomes empty, that numeric identity can be reused. A later census can therefore identify and signal an unrelated newly created group; the check and kill also race a legitimate group's disappearance. `child_groups` retains numeric identifiers for the entire150-minute family, so final runtime/consumer censuses can also mistake an unrelated reused group for an original survivor (`run.py:157`, `consume.py:37–40`). No reproduction is claimed; these are direct source ownership gaps.

Minimum correction: reuse the qualified numeric /proc identity/census and pidfd signal path, with PID/start-ticks and ancestry ownership rather than raw group-number authority. A child-subreaper can retain direct/adopted descendants when the collector exits; signal only verified owned identities through pidfds, retain actual signal observations, and fail on unknown census/ownership. Preserve direct Popen wait ownership. Treat an already-gone identity as gone, never as a replacement process to kill. Successful final consumption should recheck recorded identities and the owned-descendant census rather than historical numeric PGIDs alone. Keep the existing finite cleanup allowance; no generic process-management framework or broader host claim is needed.

Exact existing qualified pattern: `/workspace/tmp/pix-m7-audit-ui-20261015-02/source/audit-ui/worker-observer.py`, SHA256 `239a3977dd5800ee30b6ad56fb9655e200a24cb7a561e1e6d78e38cfca45bff0`. Identity/census/tree/same/pidfd helpers are lines18–97; subreaper setup130; direct-wait-safe, error-aware cleanup/finalizer180–230. Reuse its custody mechanics, not its Wi-Fi fixture assertions or any old runtime receipt. This source locator/hash was sent to the author.

## P2 — family interruption discards the observed child return status

`templates/run.py:63–66` raises on SIGTERM/SIGINT. If GNU timeout's family deadline interrupts the wait at107, control skips the child's `.exit`, profile status and result writes at112–132. The finalizer calls cleanup_child at156, which waits/reaps and returns the actual code at59–61, but discards that value. Thus a known original child outcome is lost even though outer.rc correctly preserves124 and inner.rc records1. This is a forensic/status-retention gap, not a success bypass.

Minimum correction: keep an explicit active-child record (profile, command key, process identity, output paths and whether its result was recorded). In the finalizer, capture the real Popen wait result exactly once and publish it with an interrupted/timeout, nonqualified disposition; write an incomplete per-profile/family result best-effort without overwriting already completed originals. If wait/reaping or receipt writing fails, keep the outcome unknown with explicit errors, not synthetic0. Preserve the shell's actual timeout/process status in outer.rc separately from inner.rc. The qualified observer above demonstrates protected Popen status and error-aware receipt finalization. Fatal SIGKILL outside cleanup still cannot promise a final receipt and must remain failed/unknown.

## Checks that found no additional blocker

All36 sealed payload hashes matched root seal485b9937. All13 known original metadata references matched their recorded hashes. Actual H700 bundle inputs equal corrected reader inputs12fadf79, its output-file map equals bundle32f7a652, and current ARM manifest is18ec6c1d. Actual VM reader-consumption has the required run/disposition/expected_rc/evidence fields; its consumed receipt has numeric0 command/monitor/runner. The accepted VM result remains distinct from the producer's #597 failed-reporting closeout with null original launcher status.

The seven final SM references are required, all nulls refuse, and the proposed SM field shape matches its current acceptance/output source templates. Preparation checks normalized exact Git blobs/raw symlinks and labels the new VM full source map as inventory-time provenance. This review did not read active SM build/cache outputs or qualify a future SM result.

Ordinary frozen admission uses the exact frozen tool digest, five explicit profiles and a cleared PROJECT/DEVICE/ARCH gateway; this host-only command does not invoke the nested build entrypoint that previously required an explicit device tuple. Fresh owner/exclusive receipts, held outputs/deleted0, timeout124 versus inner status, numeric runner/launcher zero checks and retained publication holds remain appropriately separated. Consumption accepts only the five current inventory results, not the historical build failures. No collector changes were re-audited; the prior finite collector review remains applicable.

## Subsequent source dependency

After this sealed packet, root reported #600 changes only the SM ABL package source. Its `prepare-owner.py:48` all-three-source-maps-equal assertion and fixed COMMIT checks are therefore no longer a launch-ready binding for that new mixed-source family. This is an explicit subsequent dependency, not permission to weaken the existing guard: an additive derivative must bind the exact reviewed one-path SM delta and its actual final commit/acceptance while preserving VM/H700 f863 identities. That source change needs its own finite review after the corrected runtime packet; the present report does not qualify it.

No new implementation or tests were performed. Root owns correction allocation, final source-delta review and all execution. The candidate seal remains immutable.
