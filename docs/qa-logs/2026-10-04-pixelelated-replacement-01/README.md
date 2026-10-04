# Corrected pixelelated replacement preparation — #383/#409/#414

Prepared October4 after actual #410 host rollout. This is engineering build
preparation, not an image or qualification result.

New build/m7-pixelelated-replacement01 is frozen at published next1600d78fe5.
The6547-file/180-symlink manifest361e0da0f17c is immutable under
/workspace/tmp/pixelelated-m7-replacement-01. Product delta from completed
coldb137 is only two proxy comment lines. Host watch-build/watch-job also
include the already-tested #412 progress correction. Live package freshness
passes: proxyec60 is still upstream HEAD; coupled dependencies keep their
recorded parent pins.

The original tree,104GB completed cold root, input manifest and candidate
bundle are preserved. copy-cache.sh uses independent rsync files, checksums
both roots and checks that no file inode is shared across them. Unchanged
tracked source mtimes are preserved to avoid timestamp-only recompilation.
Makefile's existing DOCKER_WORK_DIR keeps the cache's canonical absolute
container path, while binding the new host tree there. A read-only non-root
container probe proves the replacement git commit/branch/root and compiler
sysroot resolve correctly. No toolchain, library or package pin changes.

Copy/verification started16:19:21 in shared run20261004T161921Z-038d2995;
runner586477/watcher586493,5-second checks/5-minute suspected inactivity.
The copy finished around16:24; checksum comparison found no differences,
and all2,525,852 regular files have independent inodes. Command, watcher and
outer tool returned0; preparation finished16:31:43. A quiet verification
phase triggered the five-minute warning; actual rsync CPU and /proc/PID/io
counters proved continued progress, so no process was restarted. Large
progress output is retained only in the run log, not committed here.

Copy and inode verification passed. Idle reclaim and preflight passed, then
build.sh started16:33:10UTC through watch-build in run20261004T163309Z-9d636475
(runner647033/watcher647034). Actual container0fbef91a3724 matches the pinned
digest and uid1000:1000; its canonical path binds only the replacement tree. It cleans
only raofflineproxy and invalidates the new root's image stamp, then uses the
normal make docker-GENERIC_X64 assembly. It checks source inputs before/after,
exact assembled proxy bytes, BUILD_ID/branch and licence payload. outer.sh
records its result inside the watched boundary; the outer tool result remains
an independent observation.

Fresh QA owners qa/link/guest/runtime-02 are hash-bound and unstarted. They
use this new tree/manifest, preserve the old failed owners, and retain their
preceding-success guards. QA adds an installed proxy-script byte/mode check
on clean and actual RC2-upgraded guests. The required sequence remains
15defaults and actualRC2 → WebDAV/S3 link matrices →19 independent guest
cases → actual-upgraded archive/timing/identity → remaining P3/P4. No physical
device, personal-cloud or release publication action is implied.
