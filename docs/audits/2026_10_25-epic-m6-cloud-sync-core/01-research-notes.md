# T16 research notes: the cloud sync core (#663)

Research for M6.P2 T16 (`cloud-sync-core`), from the brief at `2cc743efd6`
(version 2). The 14 paths are read at `8ebaf8daad`'s bytes and compared
with upstream `next` at `651150fc88`. Each figure carries the command that
produced it, run in the worktree on 2026-10-25 between 11:34 and 11:37 UTC.
The raw outputs are in `.qa-scratch/t16/` (gitignored; `runs.txt` holds r1
to r26 with each exit and wall time), re-made by the commands.

## Scope

### The membership (the brief's § 2 block, at `2389bfa3ed`)

The block was run as the brief writes it, over `docs/reviews/inventory.json`
(generated at `eb4763e3cc`) and `docs/reviews/slices.json`'s `k: 16`. It
expands one level of `{a,b}`, which `fnmatch` does not. Its output:

```text
paths 14 lines 8316 {'shipped': 14} {'fork-own': 14}
{'shell': 9, 'recipe': 1, 'text': 1, 'other': 2, 'config': 1}
read 10 7827 fork-own 10
the rclone directory in the inventory 25 16518 of which T17's 11 8202
57 shell projects/ROCKNIX/packages/network/rclone/autostart/102-cloud-saves
111 recipe projects/ROCKNIX/packages/network/rclone/package.mk
2510 shell projects/ROCKNIX/packages/network/rclone/sources/cloud_backup
1704 shell projects/ROCKNIX/packages/network/rclone/sources/cloud_capture
217 shell projects/ROCKNIX/packages/network/rclone/sources/cloud_net_ready
2324 shell projects/ROCKNIX/packages/network/rclone/sources/cloud_restore
205 shell projects/ROCKNIX/packages/network/rclone/sources/cloud_saves_root
89 text projects/ROCKNIX/packages/network/rclone/sources/cloud_sync-rules.txt
100 other projects/ROCKNIX/packages/network/rclone/sources/cloud_sync-rules.txt.defaults
160 config projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf
140 other projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults
31 shell projects/ROCKNIX/packages/network/rclone/sources/cloud_sync_cleanup_duplicates.sh
625 shell projects/ROCKNIX/packages/network/rclone/sources/cloud_sync_helper
43 shell projects/ROCKNIX/packages/network/rclone/sources/rasteratops-settings-archive
```

- **The brief's figures all hold:** 14 paths, 8,316 lines; read 10 files / 7,827 lines (shell 9, recipe 1); fork-own 14; shipped 14; the directory's 25 rows, 11 of them (8,202 lines) T17's.
- **The block against `slice_of`.** The inventory tool's own `slice_of` was imported from `tools/renovation-inventory` with `load_slices` (no plan generated, nothing written). It gives the same 14 paths and 8,316 lines. No delta.
- **The block's `fork-own 10` counts the read rows only.** The tier count over all 14 is `{'fork-own': 14}`.
- **The four unread files are read anyway** (T22's precedent for its configuration): `cloud_sync.conf` (160), `cloud_sync.conf.defaults` (140), `cloud_sync-rules.txt` (89) and `cloud_sync-rules.txt.defaults` (100). Together they are the 489 lines between 8,316 and 7,827. They are read whole in `02` § The configuration under the security lens.

### Line counts at `8ebaf8daad`

- r3, the sum of `git show 8ebaf8daad:<p> | wc -l` over the 14: **8316**.
- r2, `git diff --stat 8ebaf8daad HEAD --` over the 14: empty. The read is of `next`'s bytes.

### History and the upstream relation

- **r18**, `git log --no-merges --since='2026-06-01T00:00:00Z' 8ebaf8daad --` over the 14: **145 commits, 145 of them a fork identity** (Max Engel 131, blitterbot 10, rasterabot 4).
- **r25, all-time:** 151 commits. The first, `9f1fab30f6` (ROCKNIX Team, 2025-07-13), is the only upstream one.
- **r19, upstream:** `git diff --stat c445081a59 651150fc88 -- projects/ROCKNIX/packages/network/rclone` is empty, and `git log c445081a59..651150fc88` over it counts 0 commits. Upstream carries the directory at the base's bytes. No generic `packages/network/rclone` exists, so the next base merge brings nothing here.
- **r20, since the base:** `git diff --shortstat c445081a59 8ebaf8daad --` over the 14 gives `14 files changed, 6976 insertions(+), 338 deletions(-)`.
- **The area's figures are the order's, not the slice's.** The order's § T16 says *"19 blindspot entries, 47 closed bugs, 451 commits since June"* and *"+28,279 lines since the base"*. These are the whole `cloud-sync-and-saves` area's figures (38 files by the brief's digest). This slice's are the four lines above.

### The structure (r4 to r13)

- **Function counts:** `cloud_backup` 45, `cloud_restore` 47, `cloud_capture` 40.
- **The twins under `LC_ALL=C`:** 39 shared function names (`comm -12`) and 1,622 differing lines (`diff | grep -c '^[<>]'`).
- **The exits, bound and functions in `cloud_backup`:**
  - `:20` `readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69`;
  - `:57` `SYNC_CEILING_SECONDS_FALLBACK=90`;
  - `bounded_rclone:251`, `take_cloud_lock:457`, `record_last_run:716`.
- **The same in `cloud_restore`:** `:21`, `:57`, `:238`, `:442`, `:722`.
- **`cloud_capture`:**
  - `STAGE=:118`, `EXIT_BOUND_MS=100000` `:221`;
  - `CAPTURE_LOCK="${CACHE}/.capture.lock"` `:249`, `capture_lock() :252`, `flock -n 8` `:259`;
  - the lock is taken at `:303` and `:1599`;
  - `cloud_sync.lock` hits: **0**.
- **The conf against its defaults:** 16 keys and 16 `DEFAULT_` keys; `comm -3` prints nothing.
- **The rules file against its `.defaults`:** 23 differing lines.

### The callers outside the directory (r14 to r16)

- **r14, `git grep -l` at `8ebaf8daad` over `projects packages`, the directory excluded:**
  - `misc/modules/sources/gamelist.xml`;
  - `rocknix/sources/post-update`;
  - `rocknix/sources/scripts/backuptool`;
  - `rocknix/sources/scripts/run`;
  - `rocknix/sources/scripts/runemu.sh`.

  These are the five the brief names.
- **r15:** `gamelist.xml:64` `<path>./cloud_backup.sh</path>` and `:76` `<path>./cloud_restore.sh</path>`. These are the dead tool entries, a Q6 row named for the modules package's slice.
- **r16:** `post-update:81` `for tool in cloud_backup cloud_restore; do`, with the `rm -f "${link}"` at `:84`. The loop is `:81-86`.

### The stamps (r17), who names which

| Stamp | Files that name it (count of lines) |
| --- | --- |
| `last-backup` | `cloud_backup` 1 |
| `last-settings-backup` | `cloud_backup` 1, **`cloud_sync_helper` 1** |
| `last-settings-restore` | `cloud_restore` 1, **`cloud_sync_helper` 1** |
| `last-run` | `cloud_backup` 3, `cloud_restore` 1, **`cloud_sync_helper` 1** |
| `last-capture` | `cloud_capture` 7 |
| `capture-failures` | `cloud_capture` 6 |
| `saves-root` | `102-cloud-saves` 1, `cloud_capture` 1, `cloud_saves_root` 3 |
| `last-sync` | none of the 14 (EmulationStation's) |

**Deltas to the brief:** `cloud_sync_helper` names `last-settings-backup`, `last-settings-restore` and `last-run`. `102-cloud-saves` names `saves-root`. Stage B reads each of these lines to settle whether it writes, reads or only comments.

### The oracle and the harness (r21 to r23)

- **r21, T13's `02` § Assertion shapes** (on `feature/m6-cloud-harness-660`, tip `0b72904621`): 81 table lines, which are the header, the separator and 79 rows.
- **r22, its Oracle column**, the `(reviewed)` marks read: both ends **25** (`CONTRACT` among them), synthetic **46**, device report **8**. These are the brief's figures.
- **r23, `tools/cloud-round-trip`'s mentions at `8ebaf8daad`:**

  | Script | Mentions |
  | --- | ---: |
  | `cloud_backup` | 70 |
  | `cloud_capture` | 66 |
  | `cloud_restore` | 33 |
  | `cloud_saves_root` | 18 |
  | `102-cloud-saves` | 5 |
  | `cloud_sync_helper` | 3 |
  | `cloud_net_ready` | 0 |
  | `rasteratops-settings-archive` | 0 |
  | `cloud_sync_cleanup_duplicates.sh` | 0 |

  The three scripts the harness never names are read whole at stage B.

### The removal rule's check (r24)

`git diff --stat 2389bfa3ed HEAD -- packages projects tools` is empty at stage A. The dispatch tip is `2389bfa3ed`.

One delta from the § 1 commands is recorded in `00`. `git diff --stat 8ebaf8daad HEAD -- packages projects tools` shows P1's 15 files under `tools/` (#641, #646, #810), not empty. None of them is among the 14, and `packages projects` alone is empty.
