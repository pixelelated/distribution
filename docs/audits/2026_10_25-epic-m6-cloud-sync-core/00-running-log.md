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

## 2026-10-29 18:05-22:33 UTC -- the merge; the re-granted window, overrun; the disks retired

- **18:06:** the coordinator's `0721307c0c` merged as `1bb8ad08e7`.
  - The allowed conflicts only: two ledgers by `ledger-union.py`, every line of both sides kept and checked line by line; `INDEX.md` taken from theirs and regenerated.
  - Markers 0; `register-check`, `work-log-index --check`, `rules-check --quiet` and `ceremony-check --gate` green.
  - Nothing under `packages/`, `projects/` or `tools/`.
- **18:09 grant.** START 18:10:18Z (census qemu 0); the bound 18:40:18, the grace 18:45:18.
  - Guest a was reimaged into `vm-pair-2` in 41 s; `BUILD_ID` `069fc270442134fe771258418adf4e666e0473fb`.
  - **All 13 installed files are byte-identical to `8ebaf8daad`** (`guest-cycle/image-vs-tree.txt`), so every guest verdict below is a verdict on the read bytes.
- **The suite over WebDAV:**
  - The first run is **void**. The `--shared` clone checks out `tools/` only, and `cloud-test-backend` reads the shipped folder names from `../projects/…/cloud_sync.conf.defaults`. So the suite ran with `SAVES_REMOTE=""` and failed 3 checks for that reason.
  - The re-run, with `CLOUD_QA_DEFAULTS` pointing at the `8ebaf8daad` copy (identical to the installed file): `PASSED -- backend webdav ...: 108 passed, 0 failed, 0 skipped`, rc 0, 82 s.
- **The cells:**
  - KILL15 (cells-1): the refusal holds. One FAIL: `cloud_saves_root`'s last line is not an outcome sentence.
  - KILL2, LINK1, LINK2, LINK6 at 200k (cells-3): 53 passed, 3 failed, all in KILL2. After the stop, two saves are absent from `SAVESPATH` in each arm, and in 2b three `*.partial` remain. Graded at stage C against the code.
- **The overrun.**
  - This session hit its usage limit again at about 18:19, while supervising the last cell, and ran again at 22:30.
  - Stopped by pidfile at **22:31:21**, 3 h 46 min after the grace; M7's window had been queued behind it since 18:17. The guest sat idle.
  - RETURN was posted on #663 and on the host file. A friction line with `issue: #663` is in the log.
- **Disks retired (D-INFRA-022), `guest-cycle/retire.txt`:**
  - `/workspace/tmp/m6-t16/vm-pair/vm-a.qcow2`: 2,310,799,360 bytes, sha256 `27d1a5e5dac3c2de13a4e83127b520e1a8a7b1771def4ae0244c075f66ae79ee` (the retained one, as ruled at the RETURN).
  - `/workspace/tmp/m6-t16/vm-pair-2/vm-a.qcow2`: 2,331,246,592 bytes, sha256 `bc8e8a19988b08e02cc1fbfc50847ea872d4c3d3ba7068c4e79167cff0bc0475`.
  - Both directories (each holding the disk, its OVMF vars and a QA key) were removed by literal path. `df` avail went from 1,499,053,215,744 to 1,503,696,261,120 bytes (+4,643,045,376).
- **Not run:** leads (a) to (e), the brief's extra cells and `time-to-play`.

## 2026-10-30 05:15-05:39 UTC -- the leads ruled; the host leads; KILL2 and KILL15 graded; three corrections

- **05:15, the coordinator's ruling** (#663, comment 6515562455):
  - no second window now;
  - (a), (b), (d) and (e) run on the host, with the image's own binaries, as stage-C cells under `guest-cycle/host-leads/`;
  - (c), and whatever a host run cannot show, are `(window)`-pending for stage E and the integration window.
- **The host cells, 05:24-05:35.**
  - Opened and closed on the host file (05:24:09Z, 05:34:11Z).
  - One QA WebDAV on 127.0.0.1:9010, its state under `/workspace/tmp/m6-t16/hl/state`. It was restarted at 100k for (e) and stopped by its pidfile; pids 1534987 and 1610039 are gone, 0 listeners on 9010.
  - No guest, compiler or build; qemu 0 throughout.
- **The donor root** `/workspace/artifacts/m6-donor/1a0266484423`:
  - `sha256sum -c ../../SHA256SUMS` reads OK for busybox, rclone and os-release, in every cell's `out`.
  - **It holds no cloud script.** The ruling's sentence says it does; its `RECORD.txt` lists busybox, rclone and os-release only.
  - So the scripts and `/usr/config` come from `git show 8ebaf8daad`, 12 of 12 sha256-equal to the guest's installed bytes.
  - Host bash 5.3.9, GNU coreutils 9.7 (by `gnu<name>`, the host's default being uutils), grep 3.12, python3 and `ip` stand in where the donor has nothing. That is named in `02` § The host leads.
- **Two retries, both kept in the record:**
  - (b)'s first run refused at `cloud_remote`: `cloud_connections.py` was missing from the sandbox's `/usr/bin`, my root's list. It was rebuilt as `root2` and re-run with a control arm.
  - (e)'s 2 MiB save finished before the +9 s KILL, so the arm did not test what it was for. It was re-run at 6 MiB; the first try is `out.2mib`.
- **Graded** (`02` § The host leads and § Positives; `04`):
  - **F-02 re-graded Low.** Nothing is copied into `/`: rclone's `--backup-dir` overlap check refuses first, and the why blames the cloud.
  - **F-03 proved on the host:** the orphan's rename replaces a save written after the stop, with no copy kept.
  - **F-14 new (Medium):** `--backup-dir` moves the saves aside before the transfer, so a stopped restore leaves them absent.
  - **F-15 new (oracle):** KILL15's FAIL is the harness's.
  - F-05 and F-06 gain the `--progress-terminal-width` probe, which never matches on 1.75.2.
  - F-09 gains `cloud_restore:764` (busybox awk has `gensub`).
- **Three corrections, asked by the coordinator:**
  1. **The RETURN post's sentence was wrong.** It said `time-to-play` was marked CANNOT "with the last logged figure cited". `02`:457 said CANNOT and pointed at `04` § Q5 for a figure, and `04` § Q5 cited none. Both lines now say what happened: not run, no figure.
  2. **The 22:34 post counted 38 files** under `guest-cycle/`. `git show --name-only --format= 34b6d28ee6 | grep -c 'guest-cycle/'` prints **39**.
  3. **The pointer's Next commands tailed `/tmp/m7-m6-host-coordination-20261023.txt`**, which the 2026-10-28 reboot removed. The host file is `/workspace/tmp/m7-m6-host-coordination.txt`.
- **Scratch kept:** `/workspace/tmp/m6-t16/hl/` (`root1`, `root2`, `cells/`, `state/`).
  - The cells' `rclone.conf` copies hold the QA backend's throwaway sign-in, and are never printed.
  - Removed at close-out by literal path.

## 2026-10-30 09:2x UTC -- the packet and the plan, before the first call

- **Resumed at about 09:20 UTC** after the session's usage limit. The coordinator's 05:4x message on #663 reads the 05:40 post and says to go on through stage C to the stage-D pause.
- **One fix to the 05:3x record:** the host leads' `proved:` cells read `host`, which is outside the brief's vocabulary (`tree`, `history`, `tool-run`, `fixture`, `guest`, `design`). They now read `fixture` (a constructed input ran a script, or the donor's rclone, whole) or `tool-run` (the donor's binary asked directly), in `02` and `04` alike.
- **The council runtime:** `npm install --offline --prefix tools/council --no-audit --no-fund`: rc 0, 0 s, esbuild's install script declined. `package-lock.json` sha256 `ad7b535894875b35…`, the same as T22's. Both files are gitignored (`.gitignore:66-67`); nothing under `tools/` changes. `COUNCIL_ENV_FILE=/nonexistent tools/council/run invoke --help` runs.
- **The packet** (`tools/t16-packet.py`), trimmed per D-WORKFLOW-195 from the start, as the brief says:
  - `02`, `03` and `04` whole;
  - four contexts: the order's § T16, the brief's § 4, `es-player-text.md` § Outcome vocabulary, and the 22 register rows the brief's §§ 1-4 name (none missing);
  - the eleven smaller files whole;
  - the three large scripts as excerpts: `cloud_backup` 423 of 2,510 lines, `cloud_restore` 658 of 2,324, `cloud_capture` 270 of 1,704. That is every line `02` and `04` cite, 8 lines either side, each head, trap and main, the restore's `bounded_rclone` and `rclone()` whole (identical in the twins, `02` § The functions), and the capture's five cited regions by hand;
  - the evidence: both fixtures, the host leads' records, KILL2's and KILL15's guest lines, and the harness's `fx_kill15`.
  - **Built in three passes.** The first read function ranges from `02`'s tables as citations, and a `last-good-scripts-test:8983` landed on `cloud_restore` (497,041 bytes). The citation pattern was tightened. The third pass added the wrappers.
  - The body is 376,779 bytes, sha256 `afe63258652d11fa…`.
- **Scanned before any brief was written:** `tools/forbidden-terms-check --stdin` 0 hits; `.githooks/secret-patterns` 0 lines; T10's widened set (`git show feature/m6-tooling-guards-657:.githooks/secret-patterns`) 0 lines; the QA backend's credential shapes 0 lines. No redaction. `second-opinions/packet-manifest.json` records every source's sha256, the excerpted spans and the scan.
- **`gpt-brief.md`:** the preamble, then the body, 381,240 bytes. Re-scanned: 0 and 0.
- **`review-plan.json`:** depth `extended`, the two reviewers, four calls planned. Committed with this entry, before the first call.

## 2026-10-30 09:26-09:49 UTC -- three keyed calls, Astra graded, Argon's refutation running

- **The `invoke` calls so far:** three of the four, a probe and a refutation for Astra and a probe for Argon. Every other `tools/council/run` call carried `COUNCIL_ENV_FILE=/nonexistent` (the `--help`).
  1. **Astra probe** (`--member gpt --provider openrouter --prompt-file .../gpt-probe-prompt.md --output .../gpt-probe.md`), 09:26:11-09:26:20: rc 0, `council-facilitator@1.14.1-pixelelated.2`, outcome success, 1 attempt. Verification PASS: observed `openai/gpt-6-astra` (`provider_response`), provider OpenAI, effort `max` (222 reasoning tokens). The reply was `READY unknown`; identity is taken from the provider's fields.
  2. **Astra refutation:** `tools/watch-build --record-only -- tools/council/run invoke --member gpt --provider openrouter --prompt-file .../gpt-brief.md --output .../gpt-audit.md --per-attempt-timeout-ms 1800000 --total-timeout-ms 3600000`, 09:26:35-09:43:20.
     - Watch-build rc 0, `build.rc` 0, state finished (`.build-runs/20261030T092635Z-597bc6f5/`). The watcher read `stalled` from 09:41 (no log write for 15 min, the buffered transport's shape); the facilitator was alive at 912 s.
     - `attempt=1/4 ... model=openai/gpt-6-astra providers=["OpenAI"] effort=max reasoning=41752 content=25758b finish=stop outcome=success duration=1002690ms`.
     - Verification, provider and effort PASS. Output sha256 `c872717a1a8ea3b8…`.
  3. **Argon probe** (`--member gemini-argon`), 09:26:51-09:26:58: rc 0, success, verification PASS (`google/gemini-4-argon`, `provider_response`), provider Google, effort PASS (228 reasoning tokens). Reply `READY Gemini 4 Argon`.
- **Astra graded** in `04` § Second opinion. Each of its 19 items was re-read at its lines at `8ebaf8daad`.
  - **G-01 was run:** `guest-cycle/host-leads/g01-timeout-pgid`. GNU `timeout` keeps its own process group, so a TERM to the script's group leaves `timeout` and its child running. **F-03's condition widens:** any stop that does not reach `timeout`'s group.
  - Grades: G-01 High (into F-03); G-02 and G-14 Medium; G-08 a design; G-11 narrowed; the rest confirmed Low. G-17 joins F-10, and G-19 joins F-09.
  - Taken from Astra: F-01's `Already written:` correction (a refused line runs as root); F-02 Medium in two parts; F-05 Low until measured; F-14 High, with its ordering claim narrowed. F-07's re-grade is not taken (owner-made in two ways); F-08 stays Low until #1057.
- **My slip:** G-01's first cell wrote a pid file to `/tmp`, which this slice keeps out of. It was removed by literal path, the cell moved to `/workspace/tmp/m6-t16/g01.pids`, and the cell was re-run. The committed `cmd.sh` and `out` are the second run.
- **The Argon refutation**, running since 09:48:28: the same command with `--member gemini-argon` and `gemini-argon-brief.md`.
  - The brief is 393,482 bytes: Argon's preamble, the Astra brief unchanged, and `04` § Second opinion appended. Scanned four ways: 0, 0, 0, 0.
  - **What watches it:** the record `.build-runs/20261030T094828Z-ae27bab7`, a monitor on its state, and the harness's background task.
