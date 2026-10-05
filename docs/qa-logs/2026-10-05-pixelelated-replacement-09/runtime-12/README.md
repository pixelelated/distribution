# Inherited archive, timing and installed identity (#383, #409, #430)

Durable result08:32:24/all four job channels0; submission24679f was only launch.
Actual host observation bd3e21=0 at08:33:00 confirms runner248821, watcher248822,
command248852 and guest249581 absent; no QEMU. Original QA13 backing hash
matches after cleanup; source and candidate bundle reverified.

All14 archive checks,4 timing checks and13 installed-identity checks pass.
The actual RC2 settings archive survived upgrade and restores through both
local and cloud recovery with byte preservation. Installed OS identity,
retired reporting/update entry points, policy text and actual upgraded
Tools XML match the candidate. Alternating five-sample exit-sync medians
are269ms for the legacy path and245ms for the current path:24ms absolute
difference against the unchanged30ms limit, no migration journal activity.
This is the specified narrow timing comparison, not an overall game-launch
latency claim. All97 artifact hashes and93 public files are retained.
