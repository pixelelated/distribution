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

**Stage E done (S1, S2, S3; `fixed-at` `cee4bf481d`, `reviewed-at` `8a2518fa44`, both written into #660's body). The streams' hand-back and the guest-cycle plan are posted on #660 (https://github.com/pixelelated/distribution/issues/660#issuecomment-6394453385: 8 rows, about 30 minutes, one question on A5/RETENTION same-guest), waiting for the coordinator's answer and grant (M7's full build first). 05's gate: 10 Resolved, 6 Open (guest pending), 8 Deferred; pre-issue lint PASS.**

- **S1** (`cloud-test-backend`): `0cceb65207` #1058, `94c050ed5a` #1067 (its second criterion rewritten under the coordinator's 06:17 ruling and ticked, evidence on #1067), `91267b0dda` #1068, `7345a65e9d` #1060 (backend half).
- **S2** (`cloud-round-trip`): `7f0e527800` #1066, `1e28ba8f94` #1060 (harness half), `332bda1515` #1062, `539622b9d7` #1063, `09ca086062` #1057, `e71d077882` #1059, `bde357126c` #1064, `f7482f9684` #1065, `0c538b1f74` #1069, `77e7b16193` #1070. Post-S2: `--list` 45; the dead-device case rc 2.
- **Positives** are in 02 § The streams' positives (drivers under `/workspace/tmp/m6-t13/pos*/`; the unfixed clone `/workspace/tmp/m6-t13/unfixed`).
- **Guest halves owed by the held cycle:** #1057 (A5/RETENTION SKIP), #1062 (KILL1 to its verdict), #1064 (step 25's count), #1065 (CAP13 present/absent), #1069 (A15 to its verdict), #1070 (KILL5 at the default keep and at 2). The plan goes on #660 before the grant: controls from the unfixed clone, the fixed cells, then the suite over WebDAV and SFTP; under 45 minutes; `VM_PAIR_DIR`/`VM_QEMU_RUNTIME_DIR` under `/workspace/tmp/m6-t13/`; 10022 free and qemu 0 checked at START.
- **S3:** `1911fee4df` #1061, `bf2832ce5b` #1081; and `cee4bf481d`, #1059's follow-up under the 06:33 ruling (nothing checked exits 3).
- **The plan is approved (coordinator, 06:37 UTC):** rows 0-7 as posted, plus **step 5b**: `--only A5,RETENTION --second-port 10022`, with device b being **guest a itself**. 02 § The guest cycle must record that b was guest a. About 32 minutes in all, under the 45-minute bound. **Nothing boots before the grant**, which comes on #660 as its own comment at M7's FINAL RETURN; START and RETURN are posted on #660.
- **Idle (06:4x UTC)** until the grant; the idle post is on #660.
- **After the cycle:** 02 § The guest cycle; the six Open items to Resolved; the default (resolution) lint; then stages F, G (the retro) and H.

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
