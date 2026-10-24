# Research notes — M6.P2 T9, build supervision and host maintenance (#656)

## Scope

- **Read hash:** `8ebaf8daad`, in the export `.qa-scratch/t9/at-hash/` (115 files: the 18, the seven entry lines' files, the six evidence folders and `fork-checks.yml`).
- **`reviewed-at:`** the branch at stage A, `cdc45513b0`, whose bytes on the 18 equal the hash's.

**The filter** (brief § 2's block, run 2026-10-24 15:45 UTC in the lane's worktree, over P1's `docs/reviews/inventory.json`):

```
paths 18 lines 3795 {'fork-own': 18} {'n/a': 18}
{'shell': 3, 'python': 12, 'markdown': 3}
18
```

`git show 8ebaf8daad:<path> | wc -l` per path sums to **3,795 lines**, and `wc -c` sums to **201,453 bytes**. Both equal the brief. The list is `.qa-scratch/t9/paths.txt`:

| Lines | Path |
| ---: | --- |
| 124 | `tools/build-preflight` |
| 155 | `tools/fork-newdrive` |
| 141 | `tools/fork-publish-release` |
| 101 | `tools/host-maintenance/README.md` |
| 36 | `tools/host-maintenance/admission-test-fixture.py` |
| 493 | `tools/host-maintenance/build-admission` |
| 216 | `tools/host-maintenance/build-admission.md` |
| 184 | `tools/host-maintenance/install` |
| 242 | `tools/host-maintenance/reclaim-swap` |
| 313 | `tools/host-maintenance/retention-report` |
| 94 | `tools/host-maintenance/retention-report.md` |
| 218 | `tools/host-maintenance/test-build-admission` |
| 282 | `tools/host-maintenance/test-build-monitor` |
| 95 | `tools/host-maintenance/test-retention-report` |
| 507 | `tools/host-maintenance/test-swap-reclaim` |
| 223 | `tools/watch-build` |
| 101 | `tools/watch-build-submit` |
| 270 | `tools/watch-job` |

**Provenance:**
- `git cat-file -e upstream/next:<path>` fails for all 18: none is upstream's.
- `git log --format=%h c445081a59..8ebaf8daad -- <the 18> | wc -l` gives **35** fork commits, equal to the brief.

**The branch against the hash:** `tr '\n' '\0' < .qa-scratch/t9/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD --` is empty. No hunk, no owner to name.

**Deltas against the brief:**
- **The record's count.** There are 46 `.build-runs/` directories, as the brief says. They hold 1,902 run directories and 229 loose files (45 `active.lock` and 184 others): 2,131 entries, against the brief's "2,022 run ids". The newest directory mtime is 05:40:27 UTC today, so nothing was added while the slice ran. The commands are in `00` § Stage A.
- **The three failing controls' cause.** The brief names one layer (the fixtures lack `build-admission`). There is a second: `watch-build:96-98` refuses a run without an admission or `--record-only`. See `00` § Stage A.

**Interacting subsystems** (read-only context):
- **The entry lines:** `Makefile:40` and `:179`; `scripts/build:9`, `build_distro:11`, `image:9`, `install:10`, `build_compat:7` (T5's, accepted).
- **The fork CI's three controls:** `.github/workflows/fork-checks.yml:42-44`.
- **The M7 lane's `.build-runs/`**, the record.
- **The sudoers policy** the installer writes.
- **`docs/releases/versioning.md`**, which the release tool checks.
