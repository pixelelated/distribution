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

**Stage C under way (05:25 UTC): the seat's refutation is running; the probe PASSed. Stage-B checkpoint: https://github.com/pixelelated/distribution/issues/660#issuecomment-6393859599 (answered 05:22: the mixed-installation proof is Backlog #1055, F-13). The guest window is held behind M7's full build; its grant comes on #660 at M7's FINAL RETURN.**

- The seat: `tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-brief.md --output second-opinions/gpt-audit.md --per-attempt-timeout-ms 3600000 --total-timeout-ms 10800000`, log `/workspace/tmp/m6-t13/audit.log`, started 05:25 UTC as the session's background task. **If this session is gone, check `audit.log` and `gpt-audit.md.provenance.json` before re-running anything; never start a second seat while one runs.**
- The packet: `second-opinions/gpt-brief.md` (746,882 bytes, sha256 `e4cda5bc...`), `packet-manifest.json` (15 sources, the nine 594,115 bytes, 1 redaction: `cloud-connections-test:37`'s fixture value under T10's widened pattern). Scan: forbidden 0; SECRET_PATTERNS 0 under all three sets after the redaction. Built by `tools/t13-packet.py`.
- The probe: `second-opinions/gpt-probe.md` plus provenance, PASS (openai/gpt-6-astra, OpenAI, max), Facilitator `council-facilitator@1.14.1-pixelelated.2`.
- **A rule broken and recorded** (00, 05:21 entry; friction line): `tools/council/run --help` ran once without `COUNCIL_ENV_FILE=/nonexistent` and sourced the key into a process that made no call. To report on #660 with the stage-C/D post.
- When the seat returns: scan `gpt-audit.md` (forbidden, SECRET_PATTERNS) before reading it; grade G-1.. in 04 § Second opinion; update `review-plan.json`'s status; write 05 (PL- items, `punch_index`, Phase 7 gate); `lint-audit-artifacts --phase pre-issue`. Then stage D: the `bug` issues (F-01/F-02, F-03, F-05, F-12, F-14 as candidates), the audit issue (labels `audit`, `punch-list`, milestone M6, a sub-issue of #660), then the stage-D pause on #660.

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
