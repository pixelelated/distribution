# #1481: a cached git source deleted and fetched again on every get

**Before** (`before-SM8550-*-ppsspp-sa.txt`). Each run of today's patch replays logged, against a complete clone:
- `ERROR: …: failed to determine git HEAD`
- then `Directory … already exists and is not empty. Removing it.`
- then a fresh clone of ppsspp-sa and its `ffmpeg` submodule, 1.7 GB.

That happened at 14:50, 15:08 and 16:04.

**The cause** (`ppsspp-old-and-new-check.txt`). Read-only, on the cached ppsspp-sa clone, which has 90 refs and 7,007 bytes of `ls-remote` output:
- **The old check** (`git ls-remote . | grep -q -m1 "^${PKG_VERSION}"` under pipefail) fails with rc 141, statuses `141 0`: `ls-remote` dies of SIGPIPE once `grep` has its first line. That takes neither a huge ref list nor a full pipe buffer.
- **The new check** reads `ls-remote`'s output whole first, then greps it: rc 0.
- **A 5,000-ref throwaway repository** gives the same result: the old form fails 6 times out of 6; the new one passes for the cloned version and fails for one that is not there (work log, 16:18).

**After** (`second-get.txt`). `scripts/get ppsspp-sa` from the round with the fix returns 0 at once with an empty log, which is `_repo_exists_and_valid && exit 0`, and the clone's directory inode is unchanged.

**Where the fix is.**
- The round, `6aefb77d60`.
- `next`'s `scripts/get_git`, byte-identical.
- `docs/pr-series/map.txt`, under the first bucket (build: recipes fetch nothing at configure), so it goes upstream with the series.
