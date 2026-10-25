# T13 research notes: the cloud test harness (#660)

Research for M6.P2 T13 (`cloud-harness`), the brief at `6aa2fbaadb`. The
nine tools are read at `8ebaf8daad`'s bytes (equal at the lane's dispatch
tip `e1d51b3a04`). Each figure carries the command that produced it, run in
the worktree on 2026-10-25.

## Scope

### The membership (the brief's § 2 block, at `2174265e9c`)

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
t=[r for r in rows if r["tree"]=="distribution" and r["area"]=="cloud-sync-and-saves" and r["path"].startswith("tools/")]
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t), dict(collections.Counter(r["tier"] for r in t)), dict(collections.Counter(r["language"] for r in t)), dict(collections.Counter(r["reach"] for r in t)))
[print(" ",r["path"],r["lines"],r["last_fork_commit"][:10]) for r in sorted(t,key=lambda r:-(r["lines"] or 0))]
import os; os.makedirs(".qa-scratch/t13", exist_ok=True)
open(".qa-scratch/t13/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=lambda r:r["path"])))'
```

Output:

```
paths 9 lines 10165 {'fork-own': 9} {'shell': 3, 'python': 6} {'n/a': 9}
  tools/cloud-round-trip 7808 bc2dceb406
  tools/cloud-test-backend 920 bc2dceb406
  tools/cloud-connections-test 307 bc2dceb406
  tools/cloud-census 306 4533dddc72
  tools/cloud-pair-migration 243 083f4fad86
  tools/cloud-save-integrity 219 1bd4554dc8
  tools/cloud-input-test 132 bc2dceb406
  tools/cloud-capture-stamp-test 116 080ceda7c5
  tools/cloud-save-integrity-test 114 1bd4554dc8
```

**9 paths, 10,165 lines, 9 fork-own, 6 Python and 3 shell, reach `n/a` 9**,
as the brief states. `.qa-scratch/t13/paths.txt` holds the nine, sorted.
`git diff --stat 8ebaf8daad e1d51b3a04 -- $(cat .qa-scratch/t13/paths.txt)`
is empty: the read is on `8ebaf8daad`'s bytes.

### History

| Count | Command | Value |
| --- | --- | --- |
| fork commits since the base | `git log --oneline c445081a59..8ebaf8daad -- <the nine> \| wc -l` | **108** |
| of those on `upstream/next` | `git log --oneline upstream/next -- <the nine> \| wc -l` | **0** |
| commits since 2026-06-01, the union | `git log --oneline --since=2026-06-01 8ebaf8daad -- <the nine> \| wc -l` | **108** |
| commits since 2026-06-01, summed per tool | the per-tool rows below, added | **124** (the brief's "124 in all": a commit touching two tools counts twice) |
| subjects naming a fix or a bug | `git log --format=%s --since=2026-06-01 8ebaf8daad -- <the nine> \| grep -c -i -E '\bfix\|bug'` | **10** (the brief says 6; its pattern is not stated, so this is a delta with its command) |

Per tool, since 2026-06-01 (`git log --oneline --since=2026-06-01 8ebaf8daad -- <path> | wc -l`):

| Tool | Commits |
| --- | ---: |
| `tools/cloud-round-trip` | 90 |
| `tools/cloud-test-backend` | 21 |
| `tools/cloud-pair-migration` | 6 |
| `tools/cloud-census` | 2 |
| `tools/cloud-capture-stamp-test` | 1 |
| `tools/cloud-connections-test` | 1 |
| `tools/cloud-input-test` | 1 |
| `tools/cloud-save-integrity` | 1 |
| `tools/cloud-save-integrity-test` | 1 |

### `cloud-round-trip`'s shape, by its AST at the hash

A preliminary count, made at stage A by `python3 -I` over `ast.parse` of
`tools/cloud-round-trip`; stage B's generator asserts the final figures for
§ Assertion shapes.

| Measure | Value | The brief's |
| --- | ---: | --- |
| `step()` calls in the file | 46 | 46 |
| in `run_steps` (lines 623-1716) | 32 | 32 |
| in `prepare_device` (`def` at line 304) | 2 | 2 (the brief puts it at 309, the first `step()` line) |
| `check()` calls | **460** | 461: the brief's `grep -c -E '(^\|[^a-z_])check\('` also matches `def check(cond, ok, bad):` at line 277 |
| `time.sleep` | 38 | 38 |
| `raise Fail` | 59 | 59 |
| registries | `CONTENT_FIXTURES` (181, dict of 3), `PAIR_FIXTURES` (2458, 10), `SOLO_FIXTURES` (2993, 1), `CAPTURE_FIXTURES` (4527, 14), `LINK_FIXTURES` (5720, 7), `KILL_FIXTURES` (7662, 12) | PAIR 10, SOLO 1, CAP 14, LINK 7, KILL 12 = 44 |
| `caps()`, `epath()` | lines 1792, 1803 | 1792 |
| cells `--list` prints | **45** | 44 + `CONTRACT` (#9's transport contract, `--transport`), listed in the two-device section beside the ten PAIR cells |

### Four descriptions of one suite

| Where | What it says |
| --- | --- |
| `tools/vm-qa:36` | `round-trip  tools/cloud-round-trip  -- 27 steps over SSH against the QA cloud` |
| the tool | 32 `step()` calls in `run_steps` (+2 in `prepare_device`), 460 `check()` calls in the file |
| `docs/vm-qa-log.md:175` (2026-10-06) | `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP;318 total` |
| `docs/work-logs/2026_10-work_logs/2026_10_08-work_log.md:111` | `Both ordinary VM round trips already passed 108 ...` |

### Two scripts the harness names that are not in the tree

- **`cloud_reconcile`: never added.** `git log --all --oneline --diff-filter=A -- '*cloud_reconcile' | wc -l` prints **0**. `tools/cloud-round-trip` names it at line 1771 (`APPLY = "cloud_reconcile --apply --unit {unit} --keep {side}"`), line 2441 (`pgrep -x cloud_reconcile`) and line 2443 (`pkill -9 -x cloud_reconcile`). The **open** decision D-CLOUD-051 (`docs/decision-register.md:760`, under `## Open decisions`) asks what the wizard's apply step is called from a shell.
- **`cloud_migrate_layout`: deleted.** `git log --oneline --diff-filter=D 8ebaf8daad -- '*cloud_migrate_layout'` prints `e6645cb5ea cloud: integrate explicit folder setup and save coverage`; `test -e projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout` is false. Still named **8** times by `tools/cloud-pair-migration` and **55** times by `tools/last-good-scripts-test` (T15's), **0** by `cloud-round-trip` (`grep -c`).

### The retired tool

`tools/cloud-pair-migration` lines 58-63 (at the hash):

```bash
# Historical migration proof only (D-CLOUD-175/#508). Refuse before
# creating guests, changing their state or resetting a synthetic backend.
if [ ! -f "${ROOT}/projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout" ]; then
  echo 'This migration suite is retired. Use a historical source checkout for historical firmware; #508 qualifies manual cloud setup.' >&2
  exit 2
fi
```

Run on 2026-10-25 05:00 UTC with three nonexistent arguments: **rc 2**, 0.00 s, the one sentence on stderr, nothing created. The guard is the deleted script's absence, so the tool refuses on every tree after `e6645cb5ea` and would run again on a checkout older than it.

### The vendored copy

`docs/qa-logs/2026-10-07-cloud-validator/roundtrip/tools/cloud-round-trip`:
7,795 lines, sha256 prefix `b534d17421b4`; the tool at `8ebaf8daad` is 7,808
lines, `9fe3545b19c6`. A frozen copy for that day's evidence, not the tool.

### The rule

`rclone-cloud-sync.md` on this tree is the stale one: #909 is OPEN
(`Bug: rclone-cloud-sync.md states five rclone facts the package has moved
past (PKG_SHA256, the version, tar.gz, exit 69, the content tier)`). This
slice's fact: the rule's line 375 says the no-network step checks *"the
exit-4 timing"*; the tool asserts exit 69 (`tools/cloud-round-trip:1469-1470`,
`fields.get("rc") == "69"`). T4's fix is `fcc7046f0e` on
`feature/m6-doctrine-rules-651`, not merged here; this lane reads both and
edits neither.
