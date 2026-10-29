# T16 running log: the cloud sync core (#663)

The flight recorder for M6.P2 T16 (`cloud-sync-core`), brief
`docs/reviews/briefs/cloud-sync-core.md` at `2cc743efd6` (version 2),
dispatched on #663 at 2026-10-25 11:32 UTC. Newest entries are last. Every
time comes from `date -u`.

## Header

| Field | Value |
| --- | --- |
| Executor | the T1 session (`m6-t1-os-launch`), **Opus 5.5** (`claude-opus-5-5`), **high** effort |
| Depth | **Extended**: two reviewers at Phase 4.6, through the local Facilitator: `gpt` (`openai/gpt-6-astra`, `max`) then `gemini-argon` (`google/gemini-4-argon`, `high`); each a probe, then one refutation, over a trimmed, scanned packet (D-WORKFLOW-195); **exactly four keyed invokes**, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`. A seat that cannot run is a named blocker on #663, never `--member gemini` |
| `reviewed-at` | the 14 read at **`8ebaf8daad`**'s bytes; at the dispatch tip `2389bfa3ed` none of the 14 differs from it (run r2), and nothing under `packages/` or `projects/` does |
| Upstream compared | **`651150fc88`** (upstream `next`, already in the repository; never fetched); merge base `c445081a59` |
| Worktree / branch | `/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-sync-core-663`, `feature/m6-cloud-sync-core-663` (tracks `origin/`), stacked on `feature/m6-p1-survey-641` at `2174265e9c`, the coordinator's `2cc743efd6` merged at `7cf9826140`; dispatch tip `2389bfa3ed` |
| Rules | `next`'s, except the paths the dispatch lists; `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` gives 9 files, 183+ 11- |
| Scratch | `TMPDIR=/workspace/tmp/m6-t16/tmp`; `.qa-scratch/t16/` (gitignored, `.gitignore:63`); the § 5 runner at `/workspace/tmp/m6-t16/runs.sh` |
| VM question | **Can this be done on the VM? Yes.** The host for every read, diff and log; one GENERIC_X64 guest runs the same scripts, busybox and rclone as a handheld, with `tools/cloud-test-backend`'s WebDAV on this lane's isolation under `/workspace/tmp/m6-t16/` as the cloud (D-QA-058: no hosted account), only inside the window the coordinator grants on #663 after stages A and B. **Nothing on a person's device or cloud** (D-QA-015; blindspot 38). The image is the M7 candidate `069fc2704421`, so the nine installed scripts are diffed against the tree before any guest verdict |

## 2026-10-25 11:32-11:34 UTC -- dispatch read, first commands

- #663's body (17 open criteria), its dispatch comment (11:32:01), the brief (read whole at `2cc743efd6`) and the seeded pointer were read.
- First commands (brief § 1), in the worktree only, **no fetch**:
  - `git status --short`: 0 lines; HEAD `2389bfa3ed`; `merge-base --is-ancestor 8ebaf8daad HEAD` and `2174265e9c HEAD`: both ancestors;
  - `git diff --stat 8ebaf8daad HEAD -- packages projects tools`: **not empty -- 15 files, +2130 / -8, every one under `tools/`** (P1's `renovation-{inventory,drift,status}`, `register-check`, `lint-audit-artifacts` and the lint's two renovation fixtures, from #641, #646 and #810). Under `packages projects` alone it is empty. **A delta to the brief's `# empty`**: the read's bytes are unaffected (none of the 14 is under `tools/`), and the removal check (run r24, against the dispatch tip) is empty;
  - `651150fc88` resolves locally; T13's `02` has 158 table lines on `feature/m6-cloud-harness-660` (tip `0b72904621`);
  - `tools/register-check`: `681 IDs, each once; every citation in the live documents names a row`; `D-WORKFLOW-209` is in the register; `tools/rules-check --quiet`: rc 0;
  - `grep -c gemini-argon`: `scripts/council-invoke.ts:7`, `tools/lint-audit-artifacts:4`.
- **Host file, last line:** `== M6 coordinator — 10:24 UTC: T22 SECOND GUEST WINDOW RETURN (the lane's post on #669); census qemu live 0, listeners on 9010-9099 and 10022: 0. M6 runs no guest now.`
- **Census (11:33 UTC):** `pgrep -x qemu-system-x86` (the pointer's spelling, the 15-character `comm` a QEMU guest carries): **0**; compilers (`pgrep -f -c 'cc1(plus)?$'`): **0**; `df -h /workspace`: 1.5T free (58%); `df -i /workspace`: 24%. **Corrected 11:51:** this line first gave `pgrep -x qemu-system-x86_64` as the census and called the pointer's name the short one. It is the other way round: pgrep matches `-x` against the 15-character `comm`, so `qemu-system-x86_64` can never match and reads 0 whatever runs (pgrep printed that warning). Only the pointer's spelling counted; it read 0 at 11:33, and the census is re-taken by `comm` and by command line at 11:51 (below).

## 2026-10-25 11:34-11:37 UTC -- stage A: the membership and the § 5 runs

- **Membership** (brief § 2's block, as written): `paths 14 lines 8316 {'shipped': 14} {'fork-own': 14}`; languages shell 9, recipe 1, text 1, other 2, config 1; `read 10 7827 fork-own 10`; the rclone directory 25 rows / 16,518 lines, of which T17's 11 / 8,202. `.qa-scratch/t16/paths.txt`: 14. **The inventory tool's own `slice_of`** (imported from `tools/renovation-inventory`, `load_slices` over `docs/reviews/slices.json`; no plan generated, nothing written): 14 paths, 8,316 lines, the same list as the block's. No delta.
- **The § 5 runs** (r1-r26), each with its exit and wall time in `.qa-scratch/t16/runs.txt`, run as one script file (`bash /workspace/tmp/m6-t16/runs.sh`). All 26 exited 0, each under 0.3 s. Every figure is the brief's except the deltas named in `01` § Scope (the stamp grep's `cloud_sync_helper` and `102-cloud-saves` hits). The figures and their *a FAIL would mean* go to `02` § The runs at stage B.
- **Friction (11:36):** the first form of the runner (`bash -c "$*"`) was held at a permission prompt and auto-denied, because one read's grep pattern held the text `rm `; **no command of it ran**. The coordinator's 11:37 UTC message: keep `rm` out of composite scripts. The runner was rewritten as a file with the pattern `r[m] ` and run; the friction line is in `docs/friction-log.md` with `issue: #663`.

## 2026-10-25 11:40-11:50 UTC -- stage B: 02 written

- **The stage-A acceptance** came pasted from the coordinator (11:4x UTC): go on with stage B, then ask for the window with its plan.
- **Read whole at `8ebaf8daad`** (`git show` copies in `/workspace/tmp/m6-t16/src/`):
  - `cloud_backup`;
  - `cloud_restore`: its 8 own functions and the 5 shared ones that differ, as diffs. The 34 identical shared bodies were read once in `cloud_backup` (`/workspace/tmp/m6-t16/fnbody.py` compares the bodies);
  - `cloud_capture`: 1-1110 and 1585-1704 line by line; 1110-1585 for its writes, removals, jq calls and exits;
  - the six small scripts, the four configuration files and `package.mk`.
- **Generated:** `tools/t16-oracle.py` (79 rows in; 25 / 46 / 8; 56 rows run one of the nine; no delta) and `tools/t16-functions.py` (45 + 47 + 40 = 132; 39 shared, 34 identical; 3 unrowed, all uncalled; no delta).
- **One host fixture** (`/workspace/tmp/m6-t16/fx/`, 11:46): `conf_valid` lifted from `cloud_backup` passes an empty and a commented `SAVESPATH`, which the `sed` reader of `cloud_saves_root`/`cloud_capture` reads as nothing.
- **Deltas to the brief:**
  - `last-restore` exists (a built name, `cloud_restore:724`);
  - `cloud_sync_helper`'s stamp names are a one-shot rename;
  - `102-cloud-saves`'s is a comment.
- **Twelve leads** listed in `02` § Leads, for stage C and the window.
- **Errata of my own, corrected before the commit:** six line numbers in the first draft of `02`'s leads were written from a comment-free listing, not the file; each was re-read with `grep -n` and corrected.
- No guest, no fetch, no seat call so far.
- **Census re-taken (11:51 UTC):** by `comm`, 0 processes whose name starts `qemu`. `pgrep -f '^qemu-system|/qemu-system'` read 2: both were the checking shell itself, whose argv carries the pattern (`ps -eo comm` lists none). Compilers: 0. Docker: 22 containers, every one another project's `postgres` (`gh-wt-*`, `groundhog_*`), none of M6's.

## 2026-10-25 11:56 UTC -- 2026-10-29 18:01 UTC -- the first window, cut; the lane resumed

- **START 11:56:21Z** (posted on #663). The guest booted in 44 s from M6's copy (`rec/boot.out`). Its `/etc/os-release` reads `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"` (`rec/os-release.txt`, 11:57).
- **The tree side** of the hash comparison is `rec/tree.sha256` (13 files at `8ebaf8daad`, 11:55).
- **The session then hit its usage limit (about 12:08).** No guest hash was read, the WebDAV never came up (`state/` and `artifacts/` are empty), and no cell, lead or timing ran. **No guest verdict exists from this window**, and RETURN was never posted by the lane.
- **The coordinator reconciled it on #663:**
  - 2026-10-26 04:47Z;
  - the stop, with the owner's yes, run by the M7 lane at 07:40 with `tools/vm-stop` on the pidfile; `/proc/4160936` was gone at 07:41;
  - the disk retained under D-INFRA-022 for this slice's re-granted window;
  - the re-grant, queued after M7's guest and T17's.
- **Re-read by the lane, 2026-10-29 18:01 UTC:**
  - `/workspace/tmp/m6-t16/vm-pair/vm-a.qcow2`: 2,310,799,360 bytes, mtime 2026-10-26 07:37:50, sha256 `27d1a5e5dac3c2de13a4e83127b520e1a8a7b1771def4ae0244c075f66ae79ee`, exactly as the coordinator recorded it;
  - `/workspace/tmp/m6-t16/` survived the 2026-10-28 reboot, being under `/workspace`;
  - census: qemu by `comm` 0, and 0 listeners on 9010-9099 and 10022-10023.
- **Carried for stage D:** D-CLOUD-185 (#663, 2026-10-26 07:38Z). The twins' `RCLONE_NET_OPTS` split (`cloud_restore:1406-1411`, `cloud_backup:1367-1371`) takes the same allowlist in the stage-D stream brief, with T17's fixture as the model.
- **The shared host file** is now `/workspace/tmp/m7-m6-host-coordination.txt`. Its 18:00 block says M6 runs nothing and asks for no window before T34 reaches stage B.
