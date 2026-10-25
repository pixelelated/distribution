# Session pointer: M6.P2 T13, the cloud test harness (#660)

> **Seeded:** 2026-10-25 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-cloud-harness-660`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tips merged in (`6aa2fbaadb` at `ef56509d36` (one merge, carrying versions 1 and 2)); the pointer seeded after the second merge
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-harness-660`; the T1 worktree (`m6-os-launch-control-state-648`) and the #1012 packet's (`m6-1012-ttp-runner`) beside it, idle until their merges; nothing is written there
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T1 session, `m6-t1-os-launch`), unless #660 says otherwise
> **Epic:** #1047 (cloud sync and saves: this slice first, then T16 and T17 at Extended depth, which inherit this slice's assertion-shape table); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat**, GPT-6 Astra at `max` through the local Facilitator (`tools/council/run invoke --member gpt --provider openrouter`, the one call that sources the key; every other `tools/council/run` call carries `COUNCIL_ENV_FILE=/nonexistent`); the packet scanned before it is sent; a failed seat is a hold
> **The lens:** brittleness, blindspot 31 -- what a PASS from each of the nine tools certifies, by what oracle, and what would have made it FAIL; the assertion-shape table (46 steps and 42 cells of `cloud-round-trip`) is the deliverable T16 waits for
> **The host:** M6's; the M7 lane holds the guest windows; **stage A is host-only** (the four bare tests, the backends up/ls/cat/down, `--list`); **the one guest cycle runs only in a window the coordinator grants on #660** after M7's FINAL RETURN, asked for at the end of stage A with the image, the backends, the cells and the minutes; `TMPDIR` under `/workspace/tmp/m6-t13/`; never `/tmp`; every backend brought down after its run
> **Never:** a handheld, a person's cloud, a hosted account, the maintainer's Dropbox; `cloud-census` run (read only); `--real-roms`; an edit under `tools/` before stage E, or to any file but the nine at stage E; the rule `rclone-cloud-sync.md` (under #909) edited
> **Register:** the three workflow IDs before 209 are the M7 lane's, 209 the coordinator's; a row this slice forces takes D-WORKFLOW-210 or higher, D-QA-064, D-INFRA-032; a row is never edited
> **The brief:** `docs/reviews/briefs/cloud-harness.md` at `6aa2fbaadb` (version 2, after a stranger's proof); #660's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Both guest windows are done.** The second (08:19-08:23 UTC, a pair; START 08:20 on #660, RETURN on #660) passed the SFTP suite 108/0/0 on the fixed endpoint (`7a71af7671`, #1067's cache fix), and A5/RETENTION across two guests SKIP on the fixed tree with the vacuous PASS lines on the unfixed one (#1057). Record: `stage-e/cycle2/`, 02 § The second window. #1057 and #1067 have every checkbox ticked; 05 reads 16 resolved, 8 deferred, 0 open; both lints PASS. **Next: the retention step** (held until this RETURN), then stage F (G-2 KILL1's 124 branch, G-3 A15's needle, as fixes with positives), G, H.

- **Guest criteria met:** #1062 (KILL1 to its verdict), #1064 (128 ES paths), #1065 (CAP13 present PASS / absent FAIL, after `a70b4889a3` corrected the needle in-window), #1069 (A15 to its verdict, the backup lands), #1070 (KILL5 at keep 3 and 2). #1057 met in the second window.
- **Found by the cycle, for stage F:**
  - G-1 (resolved): #1067's endpoint cache, fixed in `7a71af7671`, proven in the second window.
  - G-2: KILL1's re-run exits 124 under the 200k throttle; there is no `drained` branch like LINK's.
  - G-3: A15's two log-wording checks fail on both trees.
- **05:** 16 Resolved (PL-01 and PL-11 in the second window), 8 Deferred; pre-issue and resolution lints PASS.
- **Retention (06:52 ruling) is held until the second RETURN** (08:12 ruling). Then remove all of `/workspace/tmp/m6-t13/` with the D-INFRA-022 record in 00 (paths, size, df before and after).
- Then stage F: KILL1's 124 branch (G-2) and A15's needle (G-3) as fixes with positives (08:12 ruling); G-1..G-3 into 04/05, G (the retro, posted on #660), H (the hand-back).

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-harness-660
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the dispatch's paths
test -f docs/reviews/inventory.json && echo inventory
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
gh issue view 909 --repo pixelelated/distribution --json state,title --jq '"\(.state) \(.title)"'
sed -n '1,160p' docs/reviews/briefs/cloud-harness.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905; #1012 after T12's), T5, T6, T7,
T8, T23, T9, T10, T12, **then this branch**, then T14, T15, T45, then T4's
last. When `next` moves, the **coordinator** merges `next` into this
branch, and never between stage A and stage D; the coordinator merges its
own branch into this one at hand-back, before the last criterion's checkers
run. Never merge another lane's feature branch here. Every lane and the M7
lane append to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696), and a union of two ledgers is made by
whole entries. Nothing here builds, touches a device, a cloud account, a
hosted provider, a key file, the host's swap, another lane's worktree, or a
guest outside a granted window.
